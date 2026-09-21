# ABLITERATED.cloud website v0.12.8

A live, self-hosting cost table by model size, refreshed from the GPU
marketplace by a script instead of typed by hand. The site previously showed
only one dated operator-instance cost block, which answered "what does our A100
cost" but never "what would *my* model cost to run myself".

## Self-hosting costs by model size

- New page **`/costs/`** (`website/costs/index.html` + `index.md`): one row per
  model size class, from up-to-14B through 1T-and-larger, with the cheapest
  supported GPU, its VRAM, the requested disk, and the price per hour, per day,
  per month at 24/7 and per month at two hours a day. Every row names the
  models it covers, so a reader can find their model's price directly.
- New script **`scripts/fetch-gpu-prices.py`**: a read-only public Vast.ai
  bundles search. No account key, no instance created, started or stopped.
  Writes `website/.well-known/gpu-prices.json` with the GPU rate, the disk rate
  and every derived figure, so the arithmetic can be checked by hand:
  `disk = storage_cost_per_gb_month / 720`, `total = dph_base + disk`.
  `--check` re-verifies the committed file.
- The build renders that JSON into `/costs/`, `index.md`, `llms.txt`,
  `llms-full.txt` and the root README, and **fails closed** if the file is
  missing or not Vast.ai data. A hand-edited or stale table cannot ship.
- The homepage keeps only a short summary line and a link, so its critical
  payload stays at 22.8 KB against the 25 KB budget.
- Every published model maps to exactly one tier, derived from the parameter
  count in its own `posts.json` kicker. Tests assert the tier count, the
  arithmetic and that coverage equals the article inventory.

## Honesty in the table

- Prices are marketplace quotes **at fetch time**, with the fetch date printed.
  The note says they move by the minute rather than implying a stable price.
- The two-hours-a-day column keeps paying the disk, because storage is billed
  while the instance is stopped. That is stated, not buried.
- Excluded GPU families are recorded with a reason in the JSON: pre-Pascal
  cards and mining-only silicon that the current llama.cpp CUDA build does not
  support. A test fails if a tier ever resolves to one of them.
- The 70-80B row is a single live offer at reliability 0.9798, below the 0.98
  floor used elsewhere; that exception is recorded in the JSON filters rather
  than quietly widened. No covered model is published at that size yet.

## Discovery and navigation

- `Costs` added to the site navigation on every page; `/costs/` added to the
  sitemap, the AI resource catalog and the documentation OpenAPI document.
- `llms.txt` and `llms-full.txt` link the cost table from their documentation
  lists; `docs/SELFHOST.md` now points its hand-typed rate ranges at the live
  table instead of competing with it.
- `website/README.md` documents the refresh command sequence.

## Verification

- `python3 -I scripts/fetch-gpu-prices.py` — 7 tiers written from live offers.
- `python3 -I scripts/fetch-gpu-prices.py --check` — arithmetic verified.
- `python3 -I scripts/build-blog.py` and `--check` — built 30 articles,
  4 archive pages and all generated surfaces, clean.
- `pytest -q` — **57 passed** (was 48): new `tests/test_gpu_prices.py` (8 tests)
  and a model-size table contract in `tests/test_website.py`.
- `node scripts/verify-agent-ready.mjs http://127.0.0.1:8788 --local-only` —
  passed (30 model articles, no public inference, no live polling).
- Local HTTP check: `/`, `/costs/`, `/costs/index.md`, `/index.md`, `/llms.txt`,
  `/llms-full.txt`, `.well-known/gpu-prices.json` and `openapi.json` all 200;
  no unresolved internal links on the new page.
- No GPU was rented, started or stopped for this release.
