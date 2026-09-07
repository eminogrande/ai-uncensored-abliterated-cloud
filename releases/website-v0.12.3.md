# website-v0.12.3 — Plain-language facts, article SEO layer

2026-09-07

## Why

Every article already carried a TL;DR and `Basically,` facts, but many lines
used model jargon a stranger could not read alone. Readers and agents also
lacked section anchors, reading time and full structured data.

## Changed

- 164 TL;DR and `Basically,` statements rewritten in plain English against the
  shared Nuri editorial contract. Sources, dates and evidence excerpts unchanged.
- Article SEO layer generated from the reading notes: H2 anchors, table of
  contents, reading time, article/Twitter meta, BreadcrumbList, TechArticle
  wordCount and keywords, TL;DR per article in llms-full.txt.
- `llms.txt` gains explicit when-to-use guidance for agents.
- Stylesheet inlined at build time; no render-blocking CSS request.

## Checks

28 root tests and 66 archive tests passed; generator check clean; 54
desktop/iPhone article renders with zero overflow; 193 Basically statements
verified visible. No GPU start, payment service or DNS change.
