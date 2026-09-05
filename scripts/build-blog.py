"""Build deterministic editorial indexes and shared, truthful site surfaces."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from decimal import Decimal
from email.utils import format_datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).parents[1]
WEBSITE = ROOT / "website"
BLOG = WEBSITE / "blog"
ORIGIN = "https://abliterated.cloud"
LATEST_LIMIT = 3
PAGE_SIZE = 9
ARCHIVE_NOTE = (
    "Editorial archive — not a live model listing. This article preserves reporting "
    "at its publication date, including model-specific licenses, publisher claims and "
    "historical hosting estimates. Those estimates are not current prices or offers. "
    "Benchmarks from different artifacts, runtimes and tests are not a current ranking. "
    "Reported refusal results do not guarantee zero refusals. The current project is "
    "private on-demand evaluation on Vast.ai with llama.cpp; no public inference."
)
NAV = '''<header class="nav"><div class="nav-inner"><a class="brand" href="/"><img src="/assets/logo.svg" width="32" height="32" alt=""><span>ABLITERATED.cloud</span></a><nav class="desktop-links" aria-label="Primary navigation"><a href="/#status">Status</a><a href="/#cost">Cost</a><a href="/#workflow">Workflow</a><a href="/blog/">Archive</a><a href="https://github.com/eminogrande/ai-uncensored-abliterated-cloud">GitHub ↗</a></nav></div></header>'''
FOOTER = '''<footer class="footer"><p>ABLITERATED.cloud<br>Private evaluation. Public notes.</p><nav aria-label="Footer navigation"><a href="/">Project status</a><a href="/blog/">Archive</a><a href="/RELEASE_NOTES.md">Updates</a><a href="/llms.txt">Agent index</a><a href="/NOTICE.md">Licenses</a></nav></footer>'''


def load_posts() -> list[dict]:
    posts = json.loads((BLOG / "posts.json").read_text())
    slugs: set[str] = set()
    required = {"slug", "type", "kicker", "title", "card_title", "summary", "published_at", "modified_at"}
    if not posts:
        raise ValueError("posts.json must not be empty")
    for post in posts:
        missing = required - post.keys()
        if missing:
            raise ValueError(f"{post.get('slug', 'post')} missing {sorted(missing)}")
        slug = post["slug"]
        if slug in slugs or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"invalid or duplicate slug: {slug}")
        slugs.add(slug)
        datetime.fromisoformat(post["published_at"])
        datetime.fromisoformat(post["modified_at"])
        if post.get("content_status") != "editorial_archive":
            raise ValueError(f"{slug}: identify editorial content explicitly")
        if "zero_refusal" in post or "estimated_usd_per_hour" in post:
            raise ValueError(f"{slug}: unscoped refusal flag or current-looking price")
        for name in ("index.html", "index.md"):
            if not (BLOG / slug / name).is_file():
                raise ValueError(f"{slug} missing {name}")
        html = (BLOG / slug / "index.html").read_text()
        markdown = (BLOG / slug / "index.md").read_text()
        canonical = f"{ORIGIN}/blog/{slug}/"
        if f'<link rel="canonical" href="{canonical}">' not in html:
            raise ValueError(f"{slug} has no exact canonical URL")
        if post["title"] not in html and post["card_title"] not in html:
            raise ValueError(f"{slug} HTML does not contain its title")
        if "Primary sources" not in html or "Primary sources" not in markdown:
            raise ValueError(f"{slug} needs a Primary sources section")
    if [p["published_at"] for p in posts] != sorted((p["published_at"] for p in posts), reverse=True):
        raise ValueError("posts.json must list newest posts first")
    return posts


def title_with_break(value: str) -> str:
    owner, separator, name = value.partition("/")
    return escape(owner) + ("/<wbr>" + escape(name) if separator else "")


def render_index(posts: list[dict], page: int, total_pages: int) -> str:
    start = (page - 1) * PAGE_SIZE
    page_posts = posts[start:start + PAGE_SIZE]
    cards = "\n".join(
        f'<a class="blog-card" href="/blog/{p["slug"]}/"><span>Archived field note · <time datetime="{p["published_at"]}">{p["published_at"]}</time></span><h2>{title_with_break(p["card_title"])}</h2><p>{escape(p["summary"])}</p><strong>Read the article →</strong></a>'
        for p in page_posts
    )
    canonical = f"{ORIGIN}/blog/" if page == 1 else f"{ORIGIN}/blog/page/{page}/"
    prev_url = "/blog/" if page == 2 else f"/blog/page/{page - 1}/"
    pagination = f'<nav class="article-next" aria-label="Pagination"><span>Page {page} of {total_pages}</span>'
    if page > 1:
        pagination += f'<a href="{prev_url}">← Newer</a>'
    if page < total_pages:
        pagination += f'<a href="/blog/page/{page + 1}/">Older →</a>'
    pagination += '</nav>'
    structured = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "name": "ABLITERATED.cloud editorial archive", "url": canonical,
         "description": ARCHIVE_NOTE, "publisher": {"@type": "Organization", "name": "ABLITERATED.cloud"}},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": start + i, "url": f'{ORIGIN}/blog/{p["slug"]}/', "name": p["title"]}
            for i, p in enumerate(page_posts, 1)]}
    ]}, separators=(",", ":"))
    suffix = "" if page == 1 else f" — Page {page}"
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Editorial archive{suffix} — ABLITERATED.cloud</title>
<meta name="description" content="Historical, source-linked model field notes. An editorial archive, not a live model catalog, current price list or hosting offer.">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{canonical}"><link rel="alternate" type="application/rss+xml" title="Editorial archive" href="/blog/feed.xml">
<meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:title" content="Editorial archive{suffix} — ABLITERATED.cloud"><meta property="og:description" content="Source-linked field notes, not live models."><meta property="og:image" content="{ORIGIN}/assets/icon-512.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">{structured}</script>
</head><body><a class="skip-link" href="#main">Skip to content</a>
{NAV}
<main class="blog-page-main" id="main"><header class="blog-index-hero"><p class="kicker">EDITORIAL ARCHIVE</p><h1>Field notes, not live models.</h1><p>{escape(ARCHIVE_NOTE)}</p><p><a href="/#status">Read the current project status →</a></p></header>
<section class="blog-index-grid" aria-label="Archived articles"><div class="blog-card-grid">{cards}</div></section>{pagination}</main>
{FOOTER}
</body></html>
'''


def render_article(html: str) -> str:
    # Replace shared chrome only; leave article claims, facts and licenses intact.
    html, count = re.subn(r'<header class="(?:nav|site-header)"[^>]*>.*?</header>', NAV, html, count=1, flags=re.S)
    if count != 1:
        raise ValueError("article has no recognized site navigation")
    html, count = re.subn(r'<footer\b[^>]*>.*?</footer>', FOOTER, html, count=1, flags=re.S)
    if count != 1:
        raise ValueError("article has no footer")
    notice = f'<aside class="archive-notice" aria-label="Archive notice"><p>{escape(ARCHIVE_NOTE)}</p><p><a href="/#status">Current project status →</a></p></aside>'
    html = re.sub(r'<aside class="archive-notice".*?</aside>\s*', '', html, flags=re.S)
    html, count = re.subn(r'(<article\b[^>]*>)\s*', lambda m: m[1] + "\n    " + notice + "\n    ", html, count=1)
    if count != 1:
        raise ValueError("article has no article element")
    # A small SVG favicon replaces the legacy multi-resolution ICO request.
    html = re.sub(r'<link\b[^>]*rel="shortcut icon"[^>]*>\s*', '', html)
    # Metadata also identifies the article as historical when read without body text.
    html = re.sub(r'(<meta (?:name|property)="(?:description|og:description)" content=")(?!Editorial archive: )', r'\1Editorial archive: ', html)
    return html


def render_article_md(markdown: str) -> str:
    notice = "<!-- ARCHIVE-NOTICE -->\n> " + ARCHIVE_NOTE + f" [Current project status]({ORIGIN}/).\n<!-- /ARCHIVE-NOTICE -->\n\n"
    markdown = re.sub(r'<!-- ARCHIVE-NOTICE -->.*?<!-- /ARCHIVE-NOTICE -->\n\n', '', markdown, flags=re.S)
    # Keep YAML frontmatter at byte zero, if present.
    frontmatter = re.match(r'\A---\n.*?\n---\n\n?', markdown, re.S)
    split = frontmatter.end() if frontmatter else 0
    return markdown[:split] + notice + markdown[split:]


def render_feed(posts: list[dict]) -> str:
    newest = datetime.fromisoformat(max(p["modified_at"] for p in posts)).replace(tzinfo=timezone.utc)
    items = []
    for post in posts:
        published = datetime.fromisoformat(post["published_at"]).replace(tzinfo=timezone.utc)
        url = f'{ORIGIN}/blog/{post["slug"]}/'
        items.append(f'<item><title>{escape(post["title"])}</title><link>{url}</link><guid isPermaLink="true">{url}</guid><pubDate>{format_datetime(published)}</pubDate><description>{escape(ARCHIVE_NOTE + " " + post["summary"])}</description></item>')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>ABLITERATED.cloud editorial archive</title><link>{ORIGIN}/blog/</link><description>{escape(ARCHIVE_NOTE)}</description><language>en</language><lastBuildDate>{format_datetime(newest)}</lastBuildDate><atom:link href="{ORIGIN}/blog/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
</channel></rss>
'''


def render_sitemap(posts: list[dict], page_count: int, snapshot_date: str) -> str:
    static = ["/", "/index.md", "/llms.txt", "/llms-full.txt", "/auth.md", "/openapi.json", "/blog/", "/blog/feed.xml"]
    paths = [(p, snapshot_date) for p in static]
    paths += [(f"/blog/page/{p}/", snapshot_date) for p in range(2, page_count + 1)]
    # Archive framing changed, but original article publication dates stay intact.
    paths += [(f'/blog/{p["slug"]}/', max(snapshot_date, p["modified_at"])) for p in posts]
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f'<url><loc>{ORIGIN}{path}</loc><lastmod>{date}</lastmod></url>' for path, date in paths) + '\n</urlset>\n'


def replace_section(text: str, marker: str, body: str) -> str:
    start, end = f"<!-- {marker} -->", f"<!-- /{marker} -->"
    result, count = re.subn(re.escape(start) + r'.*?' + re.escape(end), lambda _: start + "\n" + body.rstrip() + "\n" + end, text, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f"missing generated section {marker}")
    return result


def cost_rows(status: dict) -> list[tuple[str, str]]:
    rates = status["current"]["running_quote_usd_per_hour"]
    gpu, disk, total = (Decimal(str(rates[k])) for k in ("gpu", "disk", "total"))
    if min(gpu, disk) < 0 or abs(gpu + disk - total) > Decimal("0.000001"):
        raise ValueError("invalid or inconsistent running rates")
    return [
        ("Running: GPU + disk / hour", f"${total:.5f}"),
        ("Running continuously / 24 hours", f"${total * 24:.2f}"),
        ("Running continuously / 30 days", f"${total * 720:.2f}"),
        ("Stopped: retained disk / 30 days", f"${disk * 720:.2f}"),
        ("2 hours running per day / 30 days, disk retained throughout", f"${gpu * 60 + disk * 720:.2f}"),
    ]


def render_costs(status: dict, html: bool = False) -> str:
    rates = status["current"]["running_quote_usd_per_hour"]
    note = (f'USD, contract quote checked {status["snapshot_at"][:10]}. '
            f'GPU ${rates["gpu"]:.2f}/hour plus storage ${rates["disk"]:.5f}/hour. '
            'GPU time is billed while running, even without requests. Storage is billed continuously. '
            'Bandwidth, applicable taxes and other services are excluded. No automatic idle shutdown.')
    rows = cost_rows(status)
    if html:
        return '<table><caption>Vast.ai A100 40 GB + 120 GB disk</caption><thead><tr><th scope="col">Usage</th><th scope="col">Cost</th></tr></thead><tbody>' + ''.join(f'<tr><th scope="row">{escape(label)}</th><td>{cost}</td></tr>' for label, cost in rows) + '</tbody></table><p>' + escape(note) + '</p>'
    return '| Usage | Cost |\n| --- | ---: |\n' + '\n'.join(f'| {label} | **{cost}** |' for label, cost in rows) + '\n\n' + note


def status_paragraphs(status: dict) -> list[str]:
    current, history = status["current"], status["historical_configuration"]
    stamp = datetime.fromisoformat(status["snapshot_at"].replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")
    state = current["actual_status"]
    label = "Stopped" if state in ("exited", "stopped") else state.capitalize()
    return [
        f'{label}. Provider snapshot: {stamp}, not live polling. {current["instance_count"]} Vast.ai instance: {current["instance_id"]}, {current["gpu"]} {current["gpu_memory_mb"]} MB, {current["disk_gb"]} GB disk. actual_status={state}; intended_status={current["intended_status"]}.',
        f'Last local health check ({status["local_health_checked_at"][:16]} UTC): {current["local_health"]}. No current inference test. Stopped storage remains billed.',
        f'Last serving configuration: {history["model"]}, {history["quantization"]}, {history["runtime"]}, {history["context_tokens_configured"]} tokens configured. Not serving now; long-context quality is unvalidated.',
        f'Modal: {status["legacy"]["modal"]}',
    ]


def build_outputs(posts: list[dict]) -> dict[Path, str]:
    status = json.loads((WEBSITE / ".well-known/project-status.json").read_text())
    paragraphs = status_paragraphs(status)
    page_count = (len(posts) + PAGE_SIZE - 1) // PAGE_SIZE
    outputs = {BLOG / "index.html": render_index(posts, 1, page_count)}
    outputs.update({BLOG / "page" / str(p) / "index.html": render_index(posts, p, page_count) for p in range(2, page_count + 1)})
    for post in posts:
        folder = BLOG / post["slug"]
        outputs[folder / "index.html"] = render_article((folder / "index.html").read_text())
        outputs[folder / "index.md"] = render_article_md((folder / "index.md").read_text())
    outputs[BLOG / "feed.xml"] = render_feed(posts)
    outputs[WEBSITE / "sitemap.xml"] = render_sitemap(posts, page_count, status["snapshot_at"][:10])
    latest_html = '\n'.join(f'<li><time datetime="{p["published_at"]}">{p["published_at"]}</time><a href="/blog/{p["slug"]}/">{escape(p["title"])}</a></li>' for p in posts[:LATEST_LIMIT])
    latest_md = '\n'.join(f'- {p["published_at"]}: [{p["title"]}]({ORIGIN}/blog/{p["slug"]}/)' for p in posts[:LATEST_LIMIT])
    links = '\n'.join(f'- [{p["title"]}]({ORIGIN}/blog/{p["slug"]}/index.md): archived field note, {p["published_at"]}.' for p in posts)
    for name in ["index.html", "index.md", "llms.txt", "llms-full.txt"]:
        text = (WEBSITE / name).read_text()
        body = '<div class="status-panel">' + ''.join(f'<p>{escape(p)}</p>' for p in paragraphs) + '</div>' if name.endswith('.html') else '\n\n'.join(paragraphs)
        text = replace_section(text, "PROJECT-STATUS", body)
        text = replace_section(text, "RUNNING-COSTS", render_costs(status, html=name.endswith(".html")))
        if name == "index.html":
            text = replace_section(text, "ABLITERATED-LATEST-RELEASES", latest_html)
        elif name == "index.md":
            text = replace_section(text, "ABLITERATED-LATEST-RELEASES-MD", latest_md)
        else:
            text = replace_section(text, "ARCHIVE-LINKS", links)
        outputs[WEBSITE / name] = text
    readme = ROOT / "README.md"
    outputs[readme] = replace_section(readme.read_text(), "RUNNING-COSTS", render_costs(status))
    index = WEBSITE / ".well-known/agent-skills/index.json"
    skills = json.loads(index.read_text())
    skills["skills"][0]["digest"] = "sha256:" + hashlib.sha256((WEBSITE / "skills/abliterated-cloud/SKILL.md").read_bytes()).hexdigest()
    outputs[index] = json.dumps(skills, indent=2) + "\n"
    return outputs


def main() -> None:
    posts = load_posts()
    outputs = build_outputs(posts)
    page_count = (len(posts) + PAGE_SIZE - 1) // PAGE_SIZE
    stale = [p for p in (BLOG / "page").glob("*") if p.is_dir() and p.name.isdigit() and int(p.name) > page_count]
    if "--check" in sys.argv:
        dirty = [str(p.relative_to(ROOT)) for p, content in outputs.items() if not p.is_file() or p.read_text() != content]
        if dirty or stale:
            raise SystemExit("Generated files are stale: " + ", ".join(dirty + [str(p) for p in stale]))
        print(f"Checked {len(posts)} articles, {page_count} archive pages and all generated surfaces.")
        return
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    for path in stale:
        shutil.rmtree(path)
    print(f"Built {len(posts)} articles, {page_count} archive pages and all generated surfaces.")


if __name__ == "__main__":
    main()
