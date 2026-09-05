"""Static Pages contracts: links, accessibility, discovery and archive integrity."""
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
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
        assert str(status["current"]["instance_id"]) in text
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
            assert "Editorial archive" in text
        for target in ("sitemap.xml", "blog/feed.xml", "llms.txt", "llms-full.txt"):
            assert f"/blog/{post['slug']}/" in (SITE / target).read_text()
    ET.parse(SITE / "sitemap.xml")
    ET.parse(SITE / "blog/feed.xml")


def test_generated_outputs_are_reproducible():
    subprocess.run([sys.executable, "-I", "scripts/build-blog.py", "--check"], cwd=ROOT, check=True)


def test_homepage_payload_budget():
    critical = ["index.html", "styles.css", "assets/logo.svg", "assets/favicon.svg"]
    assert sum((SITE / path).stat().st_size for path in critical) < 25000
    assert not (SITE / "app.js").exists()
    css = (SITE / "styles.css").read_text()
    assert "hero-brain" not in css and "@import" not in css
    assert "focus-visible" in css
