# ABLITERATED.cloud website v0.12.1

One new field note in the editorial archive: the day-ten uncensor wave on
Spark-X2.5. No runtime, cost snapshot or hosting change: the Vast.ai instance
stays stopped, and this release only extends the editorial archive and its
regenerated indexes.

## spark-x2-5-uncensor-wave

- New field note: **soyaakinohara/Spark-X2.5-4B-Heretic** — the first measured
  uncensor wave on XHToken (SparkLLM)'s Spark-X2.5 small models (4.1B and 1.7B,
  Apache-2.0, released 24 Aug 2026, hybrid full/sliding-window attention,
  up-to-1M-token context claimed, trained on Huawei Ascend).
- Ten days after the base drop, two independent edits landed with measurements:
  soyaakinohara's BF16 Heretic of the 4B (58 → 3/100 refusals at KL 0.0118,
  base revision pinned, Japanese-adapted twin, GGUF ladder to Q4_K_M ~2.5 GiB)
  and darioooooo0o's 1.7B ablation (0 real refusals on 337 eye-audited
  generations vs 186/300 stock on the same sealed prompts), including the
  editor's methodology essay on why marker counts mislead on thinking models.
- Historical hosting estimate recorded at the publication date: ≈ $2.34/h
  managed BF16-class on 1 × L40S; Q4 GGUF rungs fit an 8 GB card, the 1.7B
  fits ~1 GB. Estimates are editorial history, not current prices or offers.
- Refusal honesty: the 4B anchor edit measured 3/100, so the entry carries no
  zero-refusal badge; the sibling 1.7B's 0/337 is reported with its bucket
  ruler and eye-audit disclosure.
- Community gaps noted in the article: Reddit unreachable (HTTP 403), the
  general web-search backend was down at writing, the base repo's HF
  discussions API returned no threads, and the vendor's 1M-context claim has
  an open GitHub reproduction request.
- Blog archive grows to **27 field notes**; homepage latest list, blog index,
  RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated deterministically.

## Verification

- `env -u PYTHONPATH uv run python -I scripts/build-blog.py` — built 27
  articles, 3 archive pages and all generated surfaces.
- `env -u PYTHONPATH uv run pytest -q` — 13 passed.
- `npm run verify:agent-ready:local` — passed (27 archived articles, no
  public inference, no live polling).
- `git diff --check` clean. Commit SSH-signed; deployment via the signed
  Pages pipeline on `gh-pages`.
