"""Build deterministic editorial indexes and shared, truthful site surfaces."""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import sys
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from email.utils import format_datetime
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).parents[1]
WEBSITE = ROOT / "website"
BLOG = WEBSITE / "blog"
ORIGIN = "https://abliterated.cloud"
LATEST_LIMIT = 3
PAGE_SIZE = 9
ARCHIVE_NOTE = (
    "Model research, dated at publication. Model licenses, publisher benchmarks and "
    "hosting estimates are specific to each article, not a live availability or price list. "
    "Reported zero-refusal results are test-specific, not a universal guarantee."
)
SIGNAL = "https://signal.me/#p/+13103408213"
BLOG_DESCRIPTION = "Uncensored and abliterated AI model news, cloud GPU costs and self-hosting research. Find a model worth running, then get help deploying it."
NAV = f'''<header class="nav"><div class="nav-inner"><a class="brand" href="/"><img src="/assets/logo.svg" width="32" height="32" alt=""><span>ABLITERATED.cloud</span></a><nav class="desktop-links" aria-label="Primary navigation"><a href="/#models">Models</a><a href="/#how">How it works</a><a href="/blog/">Blog</a><a href="/#faq">FAQ</a><a href="{SIGNAL}">Request access ↗</a></nav></div></header>'''
FOOTER = f'''<footer class="footer"><p>ABLITERATED.cloud<br>Intelligence, freed.</p><nav aria-label="Footer navigation"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/RELEASE_NOTES.md">Updates</a><a href="/llms.txt">Agent index</a></nav></footer>'''


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
        f'<a class="blog-card" href="/blog/{p["slug"]}/"><span>Model research · <time datetime="{p["published_at"]}">{p["published_at"]}</time></span><h2>{title_with_break(p["card_title"])}</h2><p>{escape(p["summary"])}</p><strong>Read the article →</strong></a>'
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
        {"@type": "Blog", "name": "Uncensored AI models & self-hosting guides", "url": canonical,
         "description": BLOG_DESCRIPTION, "publisher": {"@type": "Organization", "name": "ABLITERATED.cloud", "url": ORIGIN}},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": start + i, "url": f'{ORIGIN}/blog/{p["slug"]}/', "name": p["title"]}
            for i, p in enumerate(page_posts, 1)]}
    ]}, separators=(",", ":"))
    suffix = "" if page == 1 else f" — Page {page}"
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Uncensored AI Models &amp; Self-Hosting Guides{suffix} | ABLITERATED.cloud</title>
<meta name="description" content="{escape(BLOG_DESCRIPTION)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{canonical}"><link rel="alternate" type="application/rss+xml" title="Uncensored AI model news" href="/blog/feed.xml">
<link rel="alternate" type="text/markdown" href="{canonical}index.md"><link rel="ai-catalog" href="/.well-known/ai-catalog.json">
<meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:title" content="Uncensored AI Models &amp; Self-Hosting Guides{suffix} | ABLITERATED.cloud"><meta property="og:description" content="{escape(BLOG_DESCRIPTION)}"><meta property="og:image" content="{ORIGIN}/assets/icon-512.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">{structured}</script>
</head><body><a class="skip-link" href="#main">Skip to content</a>
{NAV}
<main class="blog-page-main" id="main"><header class="blog-index-hero"><p class="kicker">UNCENSORED AI MODEL NEWS</p><h1>Find your next model.</h1><p>{escape(BLOG_DESCRIPTION)}</p><p>Release notes, source links, license details and reported benchmarks. Read the research. Choose your stack. Make it yours.</p><p><a href="{SIGNAL}">Need help running a model? Talk on Signal ↗</a></p></header>
<section class="blog-index-grid" aria-label="Model articles"><div class="blog-card-grid">{cards}</div></section>{pagination}<p>{escape(ARCHIVE_NOTE)}</p></main>
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
    notice = f'<aside class="archive-notice" aria-label="Self-hosting help and research context"><h2>Want this model running for you?</h2><p>We set it up on a private cloud GPU or your own machine and connect the apps you already use.</p><p><a class="button" href="{SIGNAL}">Request access on Signal</a> <a href="/#how">How it works →</a></p><p>{escape(ARCHIVE_NOTE)}</p></aside>'
    html = re.sub(r'<aside class="archive-notice".*?</aside>\s*', '', html, flags=re.S)
    html, count = re.subn(r'\s*</article>', lambda m: "\n    " + notice + "\n  </article>", html, count=1)
    if count != 1:
        raise ValueError("article has no article element")
    # A small SVG favicon replaces the legacy multi-resolution ICO request.
    html = re.sub(r'<link\b[^>]*rel="shortcut icon"[^>]*>\s*', '', html)
    # Keep unique article descriptions rather than a boilerplate archive prefix.
    html = re.sub(r'(<meta (?:name|property)="(?:description|og:description)" content=")Editorial archive: ', r'\1', html)
    if 'rel="ai-catalog"' not in html:
        html = html.replace('</head>', '<link rel="ai-catalog" href="/.well-known/ai-catalog.json">\n</head>')
    return html


def render_article_md(markdown: str) -> str:
    notice = "<!-- ARCHIVE-NOTICE -->\n## Run this model on your terms\n\nWant this model running for you, on a private cloud GPU or your own machine? " + f"[Request access on Signal]({SIGNAL}) or [see how it works]({ORIGIN}/#how).\n\n> " + ARCHIVE_NOTE + "\n<!-- /ARCHIVE-NOTICE -->\n"
    markdown = re.sub(r'<!-- ARCHIVE-NOTICE -->.*?<!-- /ARCHIVE-NOTICE -->\s*', '', markdown, flags=re.S)
    return markdown.rstrip() + "\n\n" + notice


def strip_reading_notes(text: str) -> str:
    return re.sub(r'<!-- READING-(?:TLDR|BASICALLY) -->.*?<!-- /READING-(?:TLDR|BASICALLY) -->', '', text, flags=re.S)


def plain_html(text: str) -> str:
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', text)).split())


def article_headings(html: str) -> list[str]:
    headings = [plain_html(h) for h in re.findall(r'<h2\b[^>]*>(.*?)</h2>', strip_reading_notes(html), re.S)]
    return [h for h in headings[:headings.index('Primary sources')] if h != 'One honest line']


def validate_reading_notes(notes: dict, html: str, markdown: str) -> None:
    # Validate against the original prose, never against generated summaries themselves.
    html, markdown = strip_reading_notes(html), strip_reading_notes(markdown)
    if not isinstance(notes.get('tldr'), list) or not 2 <= len(notes['tldr']) <= 4:
        raise ValueError('reading notes need 2-4 TL;DR facts')
    if any(not isinstance(line, str) or not line.strip() or len(line) > 240 or '\n' in line or '—' in line for line in notes['tldr']):
        raise ValueError('invalid TL;DR fact')
    sections = notes.get('sections', [])
    if [s['heading'] for s in sections] != article_headings(html):
        raise ValueError('Basically notes must cover each substantive heading in order')
    statements = []
    for section in sections:
        statement, evidence = section['statement'], section['evidence']
        if not isinstance(statement, str) or not 1 <= len(statement) <= 140 or '\n' in statement or '—' in statement:
            raise ValueError('Basically statement must be one line, at most 140 characters, no em dash')
        if re.match(r'^(?:it|this|that|these|they)\b', statement, re.I):
            raise ValueError('Basically statement needs an explicit subject')
        if not isinstance(evidence, str) or not evidence.strip() or not (evidence in markdown or ' '.join(evidence.split()) in plain_html(html)):
            raise ValueError(f'Basically evidence not found: {section["heading"]}')
        statements.append(statement)
    if len(set(statements)) != len(statements):
        raise ValueError('duplicate Basically statement')


def render_reading_notes(html: str, markdown: str, notes: dict) -> tuple[str, str]:
    html, markdown = strip_reading_notes(html), strip_reading_notes(markdown)
    validate_reading_notes(notes, html, markdown)
    facts = ''.join(f'<li>{escape(line)}</li>' for line in notes['tldr'])
    summary = '<!-- READING-TLDR --><aside class="article-callout" aria-label="TL;DR"><strong>TL;DR</strong><ul>' + facts + '</ul></aside><!-- /READING-TLDR -->'
    html, count = re.subn(r'(</h1>)', lambda m: m[0] + summary, html, count=1)
    if count != 1:
        raise ValueError('article needs H1 for TL;DR')
    by_heading = {s['heading']: s['statement'] for s in notes['sections']}

    def insert(match):
        heading = plain_html(match[1])
        if heading not in by_heading:
            return match[0]
        return match[0] + '<!-- READING-BASICALLY --><aside class="article-callout" aria-label="Basically"><strong>Basically,</strong><p>' + escape(by_heading[heading]) + '</p></aside><!-- /READING-BASICALLY -->'

    html = re.sub(r'<h2\b[^>]*>(.*?)</h2>', insert, html, flags=re.S)
    digest = '\n\n## TL;DR\n\n' + '\n'.join('- ' + line for line in notes['tldr'])
    digest += '\n\n## Basically, the facts\n\n' + '\n\n'.join('**' + s['heading'] + '**\n\nBasically, ' + s['statement'] for s in notes['sections']) + '\n'
    markdown, count = re.subn(r'(^# [^\n]+)', lambda m: m[0] + '<!-- READING-TLDR -->' + digest + '<!-- /READING-TLDR -->', markdown, count=1, flags=re.M)
    if count != 1:
        raise ValueError('Markdown article needs H1 for TL;DR')
    return html, markdown


def strip_article_seo(text: str) -> str:
    return re.sub(r'\n?<!-- ARTICLE-(?:META|TOC)(?:-MD)? -->.*?<!-- /ARTICLE-(?:META|TOC)(?:-MD)? -->', '', text, flags=re.S)


def article_words(html: str) -> int:
    body = strip_article_seo(strip_reading_notes(html))
    body = re.sub(r'<aside class="archive-notice".*?</aside>', '', body, flags=re.S)
    body = re.sub(r'<(p|div) class="article-meta">.*?</\1>', '', body, flags=re.S)
    main = re.search(r'<main\b.*?</main>', body, re.S)
    return len(plain_html(main[0] if main else body).split())


def heading_id(heading: str, used: set[str]) -> str:
    base = re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-') or 'section'
    candidate, n = base, 2
    while candidate in used or candidate in {'main', 'top'}:
        candidate, n = f'{base}-{n}', n + 1
    used.add(candidate)
    return candidate


def render_article_seo(html: str, markdown: str, post: dict) -> tuple[str, str]:
    """Add machine-readable dates, reading time, section anchors and a table of contents."""
    html, markdown = strip_article_seo(html), strip_article_seo(markdown)
    published, modified = (datetime.fromisoformat(post[k]) for k in ('published_at', 'modified_at'))
    words = article_words(html)
    minutes = max(1, math.ceil(words / 230))
    long = lambda d: f'{d.day} {d:%B %Y}'
    meta_parts = [f'Published {long(published)}'] + ([f'Updated {long(modified)}'] if modified > published else []) + [f'{minutes} min read', 'Sources linked below']
    meta_text = ' · '.join(meta_parts)
    meta_html = f'<div class="article-meta"><time datetime="{post["published_at"]}">{meta_parts[0]}</time>' + ''.join(f'<span>{part}</span>' for part in meta_parts[1:]) + '</div>'
    html, count = re.subn(r'<(p|div) class="article-meta">.*?</\1>', lambda m: meta_html, html, count=1, flags=re.S)
    if count != 1:
        raise ValueError('article needs one article-meta block')
    description = unescape(re.search(r'<meta name="description" content="(.*?)">', html)[1])
    image = re.search(r'<meta property="og:image" content="(.*?)">', html)[1]
    url = f'{ORIGIN}/blog/{post["slug"]}/'
    # Section anchors: stable ids for deep links, added once and never changed.
    used: set[str] = set(re.findall(r'\bid="([^"]+)"', html))
    toc: list[tuple[str, str]] = []

    def anchor(match):
        attrs, inner = match[1], match[2]
        heading = plain_html(inner)
        existing = re.search(r'\bid="([^"]+)"', attrs)
        section_id = existing[1] if existing else heading_id(heading, used)
        toc.append((section_id, heading))
        return f'<h2{attrs} id="{section_id}">{inner}</h2>' if not existing else match[0]

    notice = re.search(r'<aside class="archive-notice".*?</aside>', html, re.S)
    head, tail = (html[:notice.start()], html[notice.start():]) if notice else (html, '')
    head = re.sub(r'<h2((?:\s[^>]*)?)>(.*?)</h2>', anchor, head, flags=re.S)
    html = head + tail
    toc_html = '<!-- ARTICLE-TOC --><nav class="article-toc" aria-label="In this article"><strong>In this article</strong><ol>' + ''.join(f'<li><a href="#{i}">{escape(h)}</a></li>' for i, h in toc) + '</ol></nav><!-- /ARTICLE-TOC -->'
    html, count = re.subn(r'<!-- /READING-TLDR -->', lambda m: m[0] + toc_html, html, count=1)
    if count != 1:
        raise ValueError('article needs rendered TL;DR before its table of contents')
    schema, count = re.subn(r'<script type="application/ld\+json">(.*?)</script>', lambda m: m[0], html, count=1, flags=re.S)
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if not match:
        raise ValueError('article needs TechArticle JSON-LD')
    article = json.loads(match[1])
    if article.get('@type') != 'TechArticle':
        raise ValueError('article JSON-LD must be a TechArticle')
    article.update({'description': description, 'image': image, 'url': url, 'inLanguage': 'en', 'wordCount': words,
                    'timeRequired': f'PT{minutes}M', 'keywords': [k.strip() for k in post['kicker'].split('·') if k.strip()],
                    'articleSection': 'Uncensored AI model research', 'isAccessibleForFree': True,
                    'datePublished': post['published_at'], 'dateModified': post['modified_at']})
    html = html[:match.start(1)] + json.dumps(article, ensure_ascii=False, separators=(',', ':')) + html[match.end(1):]
    breadcrumbs = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'ABLITERATED.cloud', 'item': f'{ORIGIN}/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Models & guides', 'item': f'{ORIGIN}/blog/'},
        {'@type': 'ListItem', 'position': 3, 'name': article['headline'], 'item': url}]}, ensure_ascii=False, separators=(',', ':'))
    head_meta = ('<!-- ARTICLE-META -->'
                 f'<meta property="article:published_time" content="{post["published_at"]}"><meta property="article:modified_time" content="{post["modified_at"]}">'
                 '<meta property="article:section" content="Uncensored AI model research">'
                 f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(article["headline"], quote=True)}"><meta name="twitter:description" content="{escape(description, quote=True)}"><meta name="twitter:image" content="{image}">'
                 f'<script type="application/ld+json">{breadcrumbs}</script>'
                 '<!-- /ARTICLE-META -->')
    html, count = re.subn(r'\n?</head>', lambda m: '\n' + head_meta + '\n</head>', html, count=1)
    if count != 1:
        raise ValueError('article needs a head element')
    md_meta = f'\n<!-- ARTICLE-META-MD -->\n_{meta_text.replace(" · Sources linked below", "")} · Canonical: {url}_\n<!-- /ARTICLE-META-MD -->'
    markdown, count = re.subn(r'<!-- /READING-TLDR -->', lambda m: m[0] + md_meta, markdown, count=1)
    if count != 1:
        raise ValueError('Markdown article needs rendered TL;DR before its metadata')
    return html, markdown


def render_feed(posts: list[dict]) -> str:
    newest = datetime.fromisoformat(max(p["modified_at"] for p in posts)).replace(tzinfo=timezone.utc)
    items = []
    for post in posts:
        published = datetime.fromisoformat(post["published_at"]).replace(tzinfo=timezone.utc)
        url = f'{ORIGIN}/blog/{post["slug"]}/'
        items.append(f'<item><title>{escape(post["title"])}</title><link>{url}</link><guid isPermaLink="true">{url}</guid><pubDate>{format_datetime(published)}</pubDate><description>{escape(ARCHIVE_NOTE + " " + post["summary"])}</description></item>')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>ABLITERATED.cloud: uncensored AI models and self-hosting</title><link>{ORIGIN}/blog/</link><description>{escape(BLOG_DESCRIPTION)}</description><language>en</language><lastBuildDate>{format_datetime(newest)}</lastBuildDate><atom:link href="{ORIGIN}/blog/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
</channel></rss>
'''


def render_sitemap(posts: list[dict], page_count: int, snapshot_date: str) -> str:
    static = ["/", "/index.md", "/llms.txt", "/llms-full.txt", "/auth.md", "/openapi.json", "/blog/", "/blog/feed.xml", "/about/", "/contact/", "/privacy/"]
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
    gpu, disk = (Decimal(str(rates[k])) for k in ("gpu", "disk"))
    note = (f'USD, contract quote checked {status["snapshot_at"][:10]}. '
            f'GPU ${rates["gpu"]:.2f}/hour plus storage ${rates["disk"]:.5f}/hour. '
            f'Stopped disk: ${disk * 24:.2f}/day. Two hours/day for 30 days: ${gpu * 60:.2f} GPU + ${disk * 720:.2f} disk. '
            'GPU time is billed while running, even without requests. Storage is billed continuously. '
            'Bandwidth, applicable taxes and other services are excluded. No automatic idle shutdown.')
    rows = cost_rows(status)
    if html:
        return '<table><caption>Vast.ai A100 40 GB + 120 GB disk</caption><thead><tr><th scope="col">Usage</th><th scope="col">Cost</th></tr></thead><tbody>' + ''.join(f'<tr><th scope="row">{escape(label)}</th><td>{cost}</td></tr>' for label, cost in rows) + '</tbody></table><p>' + escape(note) + '</p>'
    return '| Usage | Cost |\n| --- | ---: |\n' + '\n'.join(f'| {label} | **{cost}** |' for label, cost in rows) + '\n\n' + note


def plain_costs(status: dict, html: bool = False) -> str:
    rates = status["current"]["running_quote_usd_per_hour"]
    gpu, disk, total = (Decimal(str(rates[k])) for k in ("gpu", "disk", "total"))
    rows = [
        ("One hour, while it runs", f"about ${total.quantize(Decimal('0.01'), ROUND_HALF_UP)}"),
        ("A full day, non-stop", f"${total * 24:.2f}"),
        ("About two hours a day, for a month", f"${gpu * 60 + disk * 720:.2f}"),
        ("Switched off, model kept ready", f"${disk * 720:.2f} a month"),
    ]
    caption = f"Example: one A100 cloud GPU with 120 GB of storage, rates checked {status['snapshot_at'][:10]}"
    note = ("You only pay while it runs. A switched-off machine keeps paying for storage until you delete it. "
            "Setup help is priced separately, before we start. Taxes and other services are extra.")
    if html:
        return f'<table><caption>{escape(caption)}</caption><thead><tr><th scope="col">What you use</th><th scope="col">What it costs</th></tr></thead><tbody>' + ''.join(f'<tr><th scope="row">{escape(label)}</th><td>{cost}</td></tr>' for label, cost in rows) + '</tbody></table><p>' + escape(note) + '</p>'
    return caption + '\n\n| What you use | What it costs |\n| --- | ---: |\n' + '\n'.join(f'| {label} | **{cost}** |' for label, cost in rows) + '\n\n' + note


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
    for page in range(1, page_count + 1):
        folder = BLOG if page == 1 else BLOG / "page" / str(page)
        page_posts = posts[(page - 1) * PAGE_SIZE:page * PAGE_SIZE]
        outputs[folder / "index.md"] = "# Uncensored AI models & self-hosting guides\n\n" + BLOG_DESCRIPTION + "\n\n" + "\n".join(f'- [{p["title"]}]({ORIGIN}/blog/{p["slug"]}/): {p["published_at"]}. {p["summary"]}' for p in page_posts) + f"\n\n[Get self-hosting help on Signal]({SIGNAL}) · [All articles]({ORIGIN}/blog/)\n\n" + ARCHIVE_NOTE + "\n"
    reading_notes = json.loads((BLOG / "reading-notes.json").read_text())
    if set(reading_notes) != {post['slug'] for post in posts}:
        raise ValueError('reading-notes.json must cover exactly the published article inventory')
    for post in posts:
        folder = BLOG / post["slug"]
        html = render_article((folder / "index.html").read_text())
        markdown = render_article_md((folder / "index.md").read_text())
        html = re.sub(r'("dateModified"\s*:\s*")[^"]+(")', lambda m: m[1] + post['modified_at'] + m[2], html)
        html, markdown = render_reading_notes(html, markdown, reading_notes[post['slug']])
        outputs[folder / "index.html"], outputs[folder / "index.md"] = render_article_seo(html, markdown, post)
    for slug in ("about", "contact", "privacy"):
        file = WEBSITE / slug / "index.html"
        text = re.sub(r'<header class="nav".*?</header>', NAV, file.read_text(), count=1, flags=re.S)
        outputs[file] = re.sub(r'<footer\b[^>]*>.*?</footer>', FOOTER, text, count=1, flags=re.S)
    outputs[BLOG / "feed.xml"] = render_feed(posts)
    outputs[WEBSITE / "sitemap.xml"] = render_sitemap(posts, page_count, max("2026-09-06", status["snapshot_at"][:10]))
    latest_html = '\n'.join(f'<a class="blog-card" href="/blog/{p["slug"]}/"><span>{escape(p["kicker"])}</span><h3>{title_with_break(p["card_title"])}</h3><p>{escape(p["title"])}</p><strong>Read the review →</strong></a>' for p in posts[:LATEST_LIMIT])
    latest_md = '\n'.join(f'- **{p["card_title"]}**: {p["title"]} [Read the review]({ORIGIN}/blog/{p["slug"]}/)' for p in posts[:LATEST_LIMIT])
    links = '\n'.join(f'- [{p["title"]}]({ORIGIN}/blog/{p["slug"]}/index.md): model research, {p["published_at"]}.' for p in posts)
    # The full guide carries each article's TL;DR so agents can answer without fetching every page.
    full_links = '\n'.join(f'- [{p["title"]}]({ORIGIN}/blog/{p["slug"]}/index.md): model research, {p["published_at"]}.\n' + '\n'.join(f'  - {fact}' for fact in reading_notes[p["slug"]]["tldr"]) for p in posts)
    for name in ["index.html", "index.md", "llms.txt", "llms-full.txt"]:
        text = (WEBSITE / name).read_text()
        is_html = name.endswith(".html")
        if name.startswith("index"):
            # The landing page speaks plainly; operating detail stays in the agent index and status JSON.
            text = replace_section(text, "RUNNING-COSTS", plain_costs(status, html=is_html))
            text = replace_section(text, "ABLITERATED-LATEST-RELEASES" if is_html else "ABLITERATED-LATEST-RELEASES-MD", latest_html if is_html else latest_md)
        else:
            text = replace_section(text, "PROJECT-STATUS", '\n\n'.join(paragraphs))
            text = replace_section(text, "RUNNING-COSTS", render_costs(status))
            text = replace_section(text, "ARCHIVE-LINKS", full_links if name == "llms-full.txt" else links)
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
