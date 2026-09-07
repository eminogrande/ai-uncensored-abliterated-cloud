"""Nuri-style reading notes: complete, grounded, deterministic and reversible."""
import copy
import json
import re
import runpy
from html import escape
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / 'website/blog'
BUILDER = runpy.run_path(str(ROOT / 'scripts/build-blog.py'))


def test_every_article_has_matching_reading_notes_without_losing_source():
    posts = json.loads((BLOG / 'posts.json').read_text())
    notes = json.loads((BLOG / 'reading-notes.json').read_text())
    assert set(notes) == {p['slug'] for p in posts}
    for post in posts:
        folder = BLOG / post['slug']
        html, md = ((folder / f'index.{suffix}').read_text() for suffix in ('html', 'md'))
        entry = notes[post['slug']]
        rendered = BUILDER['render_reading_notes'](html, md, entry)
        assert rendered == (html, md), post['slug']
        assert BUILDER['render_reading_notes'](*rendered, entry) == rendered
        for original, result in zip((html, md), rendered):
            assert BUILDER['strip_reading_notes'](result) == BUILDER['strip_reading_notes'](original)
            assert original.count('<!-- READING-TLDR -->') == 1
        assert html.count('aria-label="Basically"') == len(entry['sections'])
        assert html.index('aria-label="TL;DR"') < html.index('class="article-lead"')
        assert md.index('## TL;DR') < md.index('## Basically, the facts')
        for fact in entry['tldr']:
            assert f'<li>{escape(fact)}</li>' in html
            assert '- ' + fact in md
        for section in entry['sections']:
            assert f'<p>{escape(section["statement"])}</p>' in html
            assert 'Basically, ' + section['statement'] in md
        schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
        article = next(json.loads(s) for s in schemas if json.loads(s).get('@type') == 'TechArticle')
        assert article['dateModified'] == post['modified_at']
        assert article['datePublished'] == post['published_at']


HTML = '<h1>Sample</h1><p class="article-lead">Lead</p><h2>Model</h2><p>Sample stores 9B parameters.</p><h2>Primary sources</h2>'
MD = '# Sample\n\nSample stores 9B parameters.\n\n## Primary sources\n'
NOTES = {'tldr': ['Sample stores 9B parameters.', 'Sample is the subject of this article.'],
         'sections': [{'heading': 'Model', 'statement': 'Sample stores 9B parameters.', 'evidence': 'Sample stores 9B parameters.'}]}


def test_reading_notes_escape_html_and_preserve_original_bytes():
    notes = copy.deepcopy(NOTES)
    notes['tldr'][0] = 'Sample uses <special> tokens & strings.'
    html, md = BUILDER['render_reading_notes'](HTML, MD, notes)
    assert '&lt;special&gt;' in html and '<special>' not in html
    assert BUILDER['strip_reading_notes'](html) == HTML
    assert BUILDER['strip_reading_notes'](md) == MD
    assert BUILDER['render_reading_notes'](html, md, notes) == (html, md)


@pytest.mark.parametrize('mutation', ['missing-section', 'long-statement', 'em-dash', 'vague-subject', 'fake-evidence', 'empty-tldr', 'duplicate-section'])
def test_invalid_reading_notes_fail_closed(mutation):
    notes = copy.deepcopy(NOTES)
    section = notes['sections'][0]
    if mutation == 'missing-section':
        notes['sections'] = []
    elif mutation == 'long-statement':
        section['statement'] = 'S' * 141
    elif mutation == 'em-dash':
        section['statement'] = 'Sample — stores parameters.'
    elif mutation == 'vague-subject':
        section['statement'] = 'It stores 9B parameters.'
    elif mutation == 'fake-evidence':
        section['evidence'] = 'Sample is a verified public inference API.'
    elif mutation == 'empty-tldr':
        notes['tldr'] = []
    else:
        notes['sections'].append(copy.deepcopy(section))
    with pytest.raises(ValueError):
        BUILDER['render_reading_notes'](HTML, MD, notes)


def test_generated_notes_cannot_be_used_as_their_own_evidence():
    html, md = BUILDER['render_reading_notes'](HTML, MD, NOTES)
    bad = copy.deepcopy(NOTES)
    bad['sections'][0]['evidence'] = 'Sample is the subject of this article.'
    with pytest.raises(ValueError, match='evidence not found'):
        BUILDER['render_reading_notes'](html, md, bad)
