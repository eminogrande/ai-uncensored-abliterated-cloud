from __future__ import annotations

import json
import shutil
import sys
import re
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).parents[1]
WEBSITE = ROOT / "website"
BLOG = WEBSITE / "blog"
ORIGIN = "https://abliterated.cloud"
LATEST_LIMIT = 10
PAGE_SIZE = 9


def load_posts() -> list[dict[str, str]]:
    posts = json.loads((BLOG / "posts.json").read_text())
    slugs: set[str] = set()
    required = {"slug", "type", "kicker", "title", "card_title", "summary", "published_at", "modified_at"}
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
        for name in ("index.html", "index.md"):
            if not (BLOG / slug / name).is_file():
                raise ValueError(f"{slug} missing {name}")
        html = (BLOG / slug / "index.html").read_text()
        markdown = (BLOG / slug / "index.md").read_text()
        canonical = f'{ORIGIN}/blog/{slug}/'
        if f'<link rel="canonical" href="{canonical}">' not in html:
            raise ValueError(f"{slug} has no exact canonical URL")
        if post["title"] not in html and post["card_title"] not in html:
            raise ValueError(f"{slug} HTML does not contain its title")
        if "Primary sources" not in html or "Primary sources" not in markdown:
            raise ValueError(f"{slug} needs a Primary sources section")
    dates = [post["published_at"] for post in posts]
    if dates != sorted(dates, reverse=True):
        raise ValueError("posts.json must list newest posts first")
    return posts


def title_with_break(value: str) -> str:
    owner, separator, name = value.partition("/")
    return f"{escape(owner)}/{'<wbr>' if separator else ''}{escape(name)}"


def render_index(posts: list[dict[str, str]], page: int = 1, total_pages: int = 1) -> str:
    start = (page - 1) * PAGE_SIZE
    page_posts = posts[start : start + PAGE_SIZE]
    cards = "\n".join(
        f'      <a class="blog-card" href="/blog/{escape(post["slug"])}/"><span>{escape(post["kicker"])}</span><h2>{title_with_break(post["card_title"])}</h2><p>{escape(post["summary"])}</p><strong>Read article →</strong></a>'
        for post in page_posts
    )
    canonical = f"{ORIGIN}/blog/" if page == 1 else f"{ORIGIN}/blog/page/{page}/"
    if page == 1:
        prev_link = ""
        next_link = f'<a href="page/2/">Older →</a>' if total_pages > 1 else ""
    elif page == total_pages:
        prev_link = f'<a href="{"/blog/" if page == 2 else f"../{page - 1}/"}">← Newer</a>'
        next_link = ""
    else:
        prev_link = f'<a href="{"/blog/" if page == 2 else f"../{page - 1}/"}">← Newer</a>'
        next_link = f'<a href="../{page + 1}/">Older →</a>'
    pagination = f'<nav class="article-next" aria-label="Pagination"><span>Page {page} of {total_pages}</span>{prev_link}{next_link}<a href="/blog/">All field notes</a></nav>' if total_pages > 1 else ""
    item_list = [
        {"@type": "ListItem", "position": start + index, "url": f'{ORIGIN}/blog/{post["slug"]}/', "name": post["title"]}
        for index, post in enumerate(page_posts, 1)
    ]
    structured = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Blog", "name": "ABLITERATED.cloud field notes", "url": canonical, "publisher": {"@type": "Organization", "name": "ABLITERATED.cloud", "url": f"{ORIGIN}/"}},
            {"@type": "ItemList", "itemListElement": item_list},
        ],
    }, separators=(",", ":"))
    title_suffix = "" if page == 1 else f" — Page {page}"
    feed_href = "/blog/feed.xml"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Field notes{title_suffix} — ABLITERATED.cloud</title>
  <meta name="description" content="Source-linked reporting on uncensored and abliterated open models, their creators, evaluations, communities and practical deployment.">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <link rel="canonical" href="{canonical}"><link rel="alternate" type="application/rss+xml" title="ABLITERATED.cloud field notes" href="{feed_href}">
  <meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:title" content="Field notes{title_suffix} — ABLITERATED.cloud"><meta property="og:description" content="The model, the numbers, who made it, and what changed after abliteration."><meta property="og:image" content="{ORIGIN}/assets/og-card.png">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" sizes="any"><link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32"><link rel="shortcut icon" href="/favicon.ico"><link rel="stylesheet" href="/styles.css">
  <script type="application/ld+json">{structured}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="nav" aria-label="Primary navigation"><div class="nav-inner"><a class="brand" href="/"><img src="/assets/logo.svg" width="32" height="32" alt=""><span>ABLITERATED.cloud</span></a><nav class="desktop-links" aria-label="Site sections"><a href="/">Home</a><a href="/#models">Models</a><a href="/blog/" aria-current="page">Blog</a><a href="/#api">API</a></nav><a class="github-button" href="https://github.com/eminogrande/mn-uncensored" rel="noopener noreferrer"><span>Star on GitHub</span><span aria-hidden="true">↗</span></a></div></header>
  <main class="blog-page-main" id="main"><header class="blog-index-hero"><p class="kicker">MODEL FIELD NOTES</p><h1>Inside the models.</h1><p>New uncensored and abliterated checkpoints, traced through their architecture, lineage, published scores, creators and community response. Primary facts stay separate from benchmark claims and opinion.</p></header><section class="blog-index-grid" aria-label="Articles"><div class="blog-card-grid">
{cards}
  </div></section>{pagination}</main>
  <footer class="footer"><div><a class="brand" href="/"><img src="/assets/logo.svg" width="28" height="28" alt=""><span>ABLITERATED.cloud</span></a><p>Intelligence, freed.<br>© 2026 ABLITERATED.cloud</p></div><nav aria-label="Footer navigation"><a href="/">Home</a><a href="/#models">Exact models</a><a href="/openapi.json">OpenAPI</a><a href="https://signal.me/#p/+13103408213">Request access</a></nav></footer>
</body></html>
'''


def render_feed(posts: list[dict[str, str]]) -> str:
    newest = datetime.fromisoformat(posts[0]["modified_at"]).replace(tzinfo=timezone.utc)
    items = []
    for post in posts:
        published = datetime.fromisoformat(post["published_at"]).replace(tzinfo=timezone.utc)
        url = f'{ORIGIN}/blog/{post["slug"]}/'
        items.append(f'''    <item><title>{escape(post["title"])}</title><link>{url}</link><guid isPermaLink="true">{url}</guid><pubDate>{format_datetime(published)}</pubDate><description>{escape(post["summary"])}</description></item>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>ABLITERATED.cloud field notes</title><link>{ORIGIN}/blog/</link><description>Source-linked reporting on uncensored and abliterated open models.</description><language>en</language><lastBuildDate>{format_datetime(newest)}</lastBuildDate><atom:link href="{ORIGIN}/blog/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel></rss>
'''


def render_sitemap(posts: list[dict[str, str]]) -> str:
    static = [
        ("/", "weekly", "1.0"), ("/index.md", "weekly", "0.8"), ("/llms.txt", "daily", "0.8"),
        ("/openapi.json", "weekly", "0.6"), ("/blog/", "daily", "0.9"), ("/blog/feed.xml", "daily", "0.5"),
    ]
    latest = max(post["modified_at"] for post in posts)
    urls = [f"  <url><loc>{ORIGIN}{path}</loc><lastmod>{latest}</lastmod><changefreq>{frequency}</changefreq><priority>{priority}</priority></url>" for path, frequency, priority in static]
    page_count = (len(posts) + PAGE_SIZE - 1) // PAGE_SIZE
    urls.extend(
        f'  <url><loc>{ORIGIN}/blog/page/{page}/</loc><lastmod>{latest}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>'
        for page in range(2, page_count + 1)
    )
    urls.extend(f'  <url><loc>{ORIGIN}/blog/{post["slug"]}/</loc><lastmod>{post["modified_at"]}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>' for post in posts)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"


def render_latest_html(posts: list[dict[str, str]]) -> str:
    cards = []
    for post in posts[:LATEST_LIMIT]:
        price = post.get("estimated_usd_per_hour")
        chip = f" · ≈ ${price:.2f}/h" if price else ""
        badge = "ZERO REFUSALS · " if post.get("zero_refusal") else ""
        cards.append(
            f'        <a class="blog-card" href="blog/{escape(post["slug"])}/"><span>{badge}{escape(post["kicker"])}{chip}</span><h3>{title_with_break(post["card_title"])}</h3><p>{escape(post["summary"])}</p><strong>Read the review →</strong></a>'
        )
    return "\n".join(cards) + "\n"


def render_latest_md(posts: list[dict[str, str]]) -> str:
    lines = []
    for post in posts[:LATEST_LIMIT]:
        price = post.get("estimated_usd_per_hour")
        price_line = f" (≈ ${price:.2f}/h estimate)" if price else ""
        refusal_line = f" — {post['refusal_claim']}" if post.get("refusal_claim") else ""
        lines.append(
            f'- [{post["title"]}](blog/{post["slug"]}/){price_line}{refusal_line} — {post["summary"]}'
        )
    return "\n".join(lines) + "\n"


def replace_section(path: Path, start: str, end: str, body: str) -> None:
    text = path.read_text()
    pattern = re.compile(rf"{re.escape(start)}.*?(?={re.escape(end)})", re.DOTALL)
    replacement = f"{start}\n\n{body.rstrip()}\n\n"
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise ValueError(f"could not update {path}: {start}")
    path.write_text(updated)


def main() -> None:
    posts = load_posts()
    if "--check" in sys.argv:
        return
    page_count = (len(posts) + PAGE_SIZE - 1) // PAGE_SIZE
    (BLOG / "index.html").write_text(render_index(posts, 1, page_count))
    for page in range(2, page_count + 1):
        page_dir = BLOG / "page" / str(page)
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(render_index(posts, page, page_count))
    page_dir = BLOG / "page"
    if page_dir.is_dir():
        for stale in sorted(page_dir.iterdir(), reverse=True):
            if stale.is_dir() and stale.name.isdigit() and int(stale.name) > page_count:
                shutil.rmtree(stale)
    (BLOG / "feed.xml").write_text(render_feed(posts))
    (WEBSITE / "sitemap.xml").write_text(render_sitemap(posts))
    links = "\n".join(f'- [{post["title"]}]({ORIGIN}/blog/{post["slug"]}/index.md): {post["summary"]}' for post in posts)
    replace_section(WEBSITE / "llms.txt", "## Model field notes", "## Exact models and API identifiers", links)
    full_links = "\n".join(f'- [{post["title"]}]({ORIGIN}/blog/{post["slug"]}/index.md)' for post in posts)
    replace_section(WEBSITE / "llms-full.txt", "## Source-linked model field notes", "## Safe lifecycle", full_links + "\n\nEach article labels exact derivative facts, upstream benchmark claims, third-party measurements and community reports separately. Creator biographies require a primary profile, company page or direct statement.")
    replace_section(WEBSITE / "index.html", "<!-- ABLITERATED-LATEST-RELEASES -->", "<!-- /ABLITERATED-LATEST-RELEASES -->", render_latest_html(posts))
    replace_section(WEBSITE / "index.md", "<!-- ABLITERATED-LATEST-RELEASES-MD -->", "<!-- /ABLITERATED-LATEST-RELEASES-MD -->", render_latest_md(posts))
    print(f"Built {len(posts)} blog posts and every discovery surface.")


if __name__ == "__main__":
    main()
