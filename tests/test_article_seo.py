"""Article SEO layer: dates, reading time, anchors, table of contents and structured data."""
import json
import re
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / 'website/blog'
BUILDER = runpy.run_path(str(ROOT / 'scripts/build-blog.py'))


def test_every_article_carries_consistent_seo_layer():
    posts = json.loads((BLOG / 'posts.json').read_text())
    for post in posts:
        folder = BLOG / post['slug']
        html, md = ((folder / f'index.{suffix}').read_text() for suffix in ('html', 'md'))
        assert html.count('<!-- ARTICLE-META -->') == 1 and html.count('<!-- ARTICLE-TOC -->') == 1
        assert md.count('<!-- ARTICLE-META-MD -->') == 1
        assert BUILDER['render_article_seo'](html, md, post) == (html, md), post['slug']
        schemas = [json.loads(s) for s in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)]
        article = next(s for s in schemas if s.get('@type') == 'TechArticle')
        crumbs = next(s for s in schemas if s.get('@type') == 'BreadcrumbList')
        assert article['wordCount'] == BUILDER['article_words'](html) > 300
        assert article['timeRequired'] == f"PT{-(-article['wordCount'] // 230)}M"
        assert article['url'] == crumbs['itemListElement'][-1]['item'] == f"https://abliterated.cloud/blog/{post['slug']}/"
        assert article['keywords'] and article['datePublished'] == post['published_at']
        assert f'<meta property="article:published_time" content="{post["published_at"]}">' in html
        assert f'<time datetime="{post["published_at"]}">' in html
        assert 'min read' in html and 'min read' in md
        toc = re.findall(r'<nav class="article-toc".*?</nav>', html, re.S)[0]
        anchors = re.findall(r'href="#([^"]+)"', toc)
        assert anchors and len(anchors) == len(set(anchors))
        for anchor in anchors:
            assert f'id="{anchor}"' in html, (post['slug'], anchor)
        # Every heading before the shared notice is reachable from the table of contents.
        body = html[:html.index('<aside class="archive-notice"')]
        assert len(re.findall(r'<h2\b', body)) == len(anchors)


def test_seo_layer_is_reversible_and_fails_without_prerequisites():
    post = json.loads((BLOG / 'posts.json').read_text())[0]
    folder = BLOG / post['slug']
    html, md = ((folder / f'index.{suffix}').read_text() for suffix in ('html', 'md'))
    stripped = (BUILDER['strip_article_seo'](html), BUILDER['strip_article_seo'](md))
    assert '<!-- ARTICLE-' not in stripped[0] and '<!-- ARTICLE-' not in stripped[1]
    assert BUILDER['render_article_seo'](*stripped, post) != stripped
    with pytest.raises(ValueError, match='TL;DR'):
        BUILDER['render_article_seo'](BUILDER['strip_reading_notes'](stripped[0]), stripped[1], post)
