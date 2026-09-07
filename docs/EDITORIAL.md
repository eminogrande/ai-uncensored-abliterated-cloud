# Fast-reading editorial contract

## Why

Readers should be able to identify the model, the real claim and the practical
constraint without reading a full field note. The blog now uses the same TL;DR
and standalone `Basically,` writing rules as Nuri's voice publishing workflow,
without importing Nuri's deployment, illustration or translation stack.

## One data source

`website/blog/reading-notes.json` maps every `posts.json` slug to:

- `tldr`: 2-4 short source-backed facts below the title.
- `sections`: ordered `heading`, `statement`, `evidence` records for every
  substantive H2 before `Primary sources`, excluding `One honest line`.

Headings match decoded HTML exactly. Statements name their subject, make one
complete claim, target 60-110 characters and never exceed 140 characters,
excluding the `Basically,` label. Keep measurement attribution, uncertainty and
historical context in the statement itself. No fake quotes or em dashes.

Evidence is an exact excerpt from the original Markdown or normalized visible
HTML, not from generated summaries. Excerpt existence is a mechanical guard,
not proof of entailment: review whether each fact follows from its source.

The generator adds visible section callouts to HTML and a complete facts digest
to Markdown. Older Markdown twins sometimes abbreviate the HTML narrative;
the digest still includes every HTML section's takeaway without deleting the
original Markdown. Existing callout CSS is reused; no additional scripts or
styles are required.

Do not edit `READING-TLDR` or `READING-BASICALLY` interiors. Change the ledger and
run the builder. Generated reading blocks can be removed without changing the
original article prose. Publication dates stay original; modification dates
track editorial changes, not a claim of freshly rechecked research.

## Verify

```sh
env -u PYTHONPATH uv run --locked python -I scripts/build-blog.py
env -u PYTHONPATH uv run --locked python -I scripts/build-blog.py --check
env -u PYTHONPATH uv run --locked pytest -q
git diff --check
```

Tests cover the complete inventory, HTML/Markdown parity, section coverage,
source excerpts, length limits, duplicate rejection, HTML escaping and
idempotence. A self-referential generated summary cannot serve as evidence.
Check the blog/homepage navigation and mobile/desktop appearance separately.

## Automation

The existing local Hermes job `53316fb09055` remains daily at `0 9 * * *`.
It loads `abliterated-daily-editorial`, which loads the shared reference:
`nuri-voice-blog-publishing/references/basically-editorial-contract.md`.
No duplicate job, schedule/provider change, GPU operation or paid inference is
part of this migration.

The daily job requires the reading-notes generator and tests on clean main.
Until this interactive migration is reviewed and merged, it must report the
missing migration rather than publish another old-format post. Existing daily
auto-publish authorization does not authorize absorbing pending interactive
changes. Skill/job changes are local Hermes configuration; repository changes
are not live until separately deployed and read back.
