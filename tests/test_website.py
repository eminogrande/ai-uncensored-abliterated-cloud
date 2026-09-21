"""Static Pages contracts: links, accessibility, discovery and archive integrity."""
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"
ORIGIN = "https://abliterated.cloud"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def test_all_html_links_assets_metadata_and_accessibility():
    for file in SITE.rglob("*.html"):
        text = file.read_text()
        page = Page(text)
        assert sum(tag == "h1" for tag, _ in page.tags) == 1, file
        assert any(tag == "html" and attrs.get("lang") for tag, attrs in page.tags), file
        assert any(tag == "main" for tag, _ in page.tags), file
        assert any(tag == "a" and "skip-link" in attrs.get("class", "") for tag, attrs in page.tags), file
        base = ORIGIN + "/" + str(file.relative_to(SITE))
        for tag, attrs in page.tags:
            if tag == "img":
                assert "alt" in attrs, file
            if tag == "script":
                assert attrs.get("type") == "application/ld+json" and not attrs.get("src"), file
            assert tag != "canvas", file
            targets = [attrs[key] for key in ("href", "src") if attrs.get(key)]
            if tag == "meta" and attrs.get("property") == "og:image":
                targets.append(attrs["content"])
            for target in targets:
                url = urlparse(urljoin(base, target))
                if url.netloc != "abliterated.cloud":
                    continue
                resolved = SITE / unquote(url.path).lstrip("/")
                if resolved.is_dir():
                    resolved /= "index.html"
                assert resolved.is_file(), (file, target)
                if url.fragment and resolved.suffix == ".html":
                    ids = {a.get("id") for _, a in Page(resolved.read_text()).tags}
                    assert unquote(url.fragment) in ids, (file, target)
        for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S):
            assert json.loads(raw)


def test_public_schema_only_advertises_existing_static_gets():
    schema = json.loads((SITE / "openapi.json").read_text())
    assert schema["x-public-inference"] is False
    assert schema["x-public-mcp"] is False
    for route, methods in schema["paths"].items():
        assert set(methods) == {"get"}
        assert (SITE / route.lstrip("/")).is_file()
    status = json.loads((SITE / ".well-known/project-status.json").read_text())
    assert status["live_polling"] is False
    assert status["historical_configuration"]["long_context_validated"] is False
    for file in [SITE / "index.html", SITE / "index.md", SITE / "llms.txt", SITE / "llms-full.txt"]:
        text = file.read_text()
        assert status["snapshot_at"][:10] in text
        assert "storage" in text.lower()
    for file in [SITE / "llms.txt", SITE / "llms-full.txt"]:
        assert str(status["current"]["instance_id"]) in file.read_text()
    landing = (SITE / "index.html").read_text()
    assert "actual_status" not in landing and "localhost" not in landing and str(status["current"]["instance_id"]) not in landing
    index = json.loads((SITE / ".well-known/agent-skills/index.json").read_text())
    expected = hashlib.sha256((SITE / "skills/abliterated-cloud/SKILL.md").read_bytes()).hexdigest()
    assert index["skills"][0]["digest"] == "sha256:" + expected


def test_archive_preserves_articles_and_all_indexes():
    posts = json.loads((SITE / "blog/posts.json").read_text())
    slugs = [p["slug"] for p in posts]
    assert slugs and len(slugs) == len(set(slugs))
    for post in posts:
        assert post["content_status"] == "editorial_archive"
        assert "zero_refusal" not in post and "estimated_usd_per_hour" not in post
        article = SITE / "blog" / post["slug"]
        for extension in ("html", "md"):
            text = (article / f"index.{extension}").read_text()
            assert "Primary sources" in text
            assert "Model research, dated at publication" in text
            assert "https://signal.me/#p/+13103408213" in text
            assert "Private evaluation. Public notes." not in text
        for target in ("sitemap.xml", "blog/feed.xml", "llms.txt", "llms-full.txt"):
            assert f"/blog/{post['slug']}/" in (SITE / target).read_text()
    ET.parse(SITE / "sitemap.xml")
    ET.parse(SITE / "blog/feed.xml")


def test_generated_outputs_are_reproducible():
    subprocess.run([sys.executable, "-I", "scripts/build-blog.py", "--check"], cwd=ROOT, check=True)


def test_model_size_price_table_is_live_arithmetic_and_matches_models():
    prices = json.loads((SITE / ".well-known/gpu-prices.json").read_text())
    assert prices["provider"] == "Vast.ai"
    assert prices["method"].startswith("GET public bundles search")
    assert datetime.fromisoformat(prices["generated_at"])
    tiers = prices["tiers"]
    assert len(tiers) >= 5
    labels = [tier["label"] for tier in tiers]
    assert len(labels) == len(set(labels))
    posts = json.loads((SITE / "blog/posts.json").read_text())
    assert sum(tier["covered_models"] for tier in tiers) == len(posts)
    for tier in tiers:
        recomputed = tier["gpu_usd_hour"] + tier["disk_usd_hour"]
        assert abs(recomputed - tier["total_usd_hour"]) <= 1e-5, tier["label"]
        for key, exact in (
            ("usd_day", recomputed * 24),
            ("usd_month_24_7", recomputed * prices["hours_per_month"]),
            ("usd_month_2h_day", tier["gpu_usd_hour"] * 60 + tier["usd_stopped_month"]),
        ):
            assert abs(exact - tier[key]) <= 0.01, (tier["label"], key)
        assert tier["gpus"] >= 1 and tier["vram_per_gpu_mb"] > 0 and tier["disk_gb"] > 0
        assert 0 < tier["reliability"] <= 1 and tier["offers_in_tier"] >= 1
        assert tier["gpu_name"] and tier["location"]
        # A tier must never be a GPU the current llama.cpp build cannot run.
        families = [row["family"] for row in prices["filters"]["excluded_gpu_families"]]
        assert not any(family in tier["gpu_name"] for family in families), tier["label"]
    # The published table must be reproduced exactly by the builder, in both formats.
    import runpy
    builder = runpy.run_path(str(ROOT / "scripts/build-blog.py"))
    html = builder["render_model_size_prices"](prices, html=True)
    markdown = builder["render_model_size_prices"](prices)
    assert html.count("<tr>") == len(tiers) + 1  # one header row plus one per tier
    assert markdown.count("\n| ") == len(tiers) + 1  # separator plus one per tier; the header starts the block
    assert prices["generated_at"][:10] in html and prices["generated_at"][:10] in markdown
    for target in ("costs/index.html", "costs/index.md", "llms.txt", "llms-full.txt"):
        text = (SITE / target).read_text()
        assert "<!-- MODEL-SIZE-PRICES -->" in text and "<!-- /MODEL-SIZE-PRICES -->" in text, target
        assert f"${tiers[0]['total_usd_hour']:.2f}" in text or tiers[0]["label"] in text, target
    assert "/costs/" in (SITE / "sitemap.xml").read_text()
    assert (SITE / "costs/index.html").read_text().count("<h1") == 1


def test_shared_article_rendering_is_idempotent():
    import runpy
    builder = runpy.run_path(str(ROOT / "scripts/build-blog.py"))
    posts = json.loads((SITE / "blog/posts.json").read_text())
    for post in posts:
        for suffix, render in (("html", builder["render_article"]), ("md", builder["render_article_md"])):
            source = (SITE / "blog" / post["slug"] / f"index.{suffix}").read_text()
            rendered = render(source)
            assert render(rendered) == rendered, (post["slug"], suffix)
            assert "Primary sources" in rendered


def test_homepage_payload_budget():
    # The stylesheet is inlined at build time, so the first paint needs only these requests.
    critical = ["index.html", "assets/logo.svg", "assets/favicon.svg"]
    assert sum((SITE / path).stat().st_size for path in critical) < 25000
    for file in SITE.rglob("*.html"):
        text = file.read_text()
        assert text.count('<style id="site-css">') == 1 and 'styles.css"' not in text, file
    assert not (SITE / "app.js").exists()
    css = (SITE / "styles.css").read_text()
    assert "hero-brain" not in css and "@import" not in css
    assert "focus-visible" in css


def test_service_positioning_and_structured_answers():
    from html import unescape
    html = (SITE / "index.html").read_text()
    markdown = (SITE / "index.md").read_text()
    assert re.search(r'<h1[^>]*>Intelligence, freed\.</h1>', html)
    for text in (html, markdown):
        assert "https://signal.me/#p/+13103408213" in text
        for word in ("uncensored", "abliterated", "self-host", "router"):
            assert word in text.lower()
        assert "Private model evaluation" not in text
    structured = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert structured
    graph = json.loads(structured[1])["@graph"]
    assert {"Organization", "WebSite", "Service", "FAQPage"} <= {row["@type"] for row in graph}
    visible = unescape(re.sub(r'<script\b.*?</script>', '', html, flags=re.S))
    visible = ' '.join(re.sub(r'<[^>]+>', ' ', visible).split())
    faq = next(row for row in graph if row["@type"] == "FAQPage")
    for question in faq["mainEntity"]:
        assert question["name"] in visible
        assert question["acceptedAnswer"]["text"] in visible


def test_ai_catalog_points_to_real_documents():
    catalog = json.loads((SITE / ".well-known/ai-catalog.json").read_text())
    assert catalog["specVersion"] == "1.0"
    assert catalog["host"]["displayName"] == "ABLITERATED.cloud"
    assert catalog["entries"]
    for entry in catalog["entries"]:
        assert entry["identifier"] and entry["displayName"]
        assert ("url" in entry) != ("data" in entry)
        assert 2 <= len(entry["representativeQueries"]) <= 5
        if "url" in entry:
            url = urlparse(entry["url"])
            if url.netloc == "abliterated.cloud":
                path = SITE / url.path.lstrip("/")
                assert path.is_file() or (path / "index.html").is_file()
