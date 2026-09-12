# ABLITERATED.cloud website v0.12.7

One new field note in the editorial archive: the four-month uncensoring line
on Google's Gemma 4 31B, anchored on the newest edit made against the Q4_0
quantisation-aware checkpoint. No runtime, cost snapshot or hosting change:
the Vast.ai reference instance stays stopped at the 5 September snapshot, and
this release only extends the editorial archive and its regenerated indexes.

## gemma-4-31b-qat-uncensored-heretic

- New field note: **Gemma 4 31B** (30.7B dense, 60 layers, 256K context,
  text and image input, Apache 2.0, 11 March 2026, 3,768 likes and 8,676,676
  downloads at fetch) and the three Heretic editors working it this year.
- Anchor: **OS-Software/gemma-4-31B-it-qat-q4_0-uncensored-heretic-GGUF**
  (8 September 2026 04:06 UTC, pinned c0fa1000) with its weight-level sibling
  (03:43 UTC, 13 shards), edited from google/gemma-4-31B-it-qat-q4_0-unquantized
  with a Heretic v2.0.0.dev0+custom development build (v1.4.0 from 14 June is
  the newest public release). Card: refusals 0/100 vs 100/100 for the stock
  checkpoint at KL 0.0083; parameter table (layers 30-41, attn.o_proj +
  mlp.down_proj, Gaussian transport rank 4, rank-128 LoRA merge) quoted in
  the article. Publisher-measured; no zero-refusal badge.
- Lineage documented from primary sources: coder3101's April edit on the
  plain -it weights (Heretic v1.2.0 + ARA, 15/100 vs 99/100, KL 0.0434,
  75 likes / 8,906 downloads); wnfldchen's 14 August rebuild on the QAT
  checkpoint (trial 6, 8/100 vs 99/100, KL 0.0900, reproduction kit, plus a
  W4A16 variant with a capability table against Google's official W4A16
  base: PIQA -0.71pp, WinoGrande -0.16pp, CommonsenseQA -0.16pp, EQ-Bench
  +4.05, parseability -4.68pp); the requant week (sjoe1244 EXL3 4.00 bpw,
  musafa901 same-parameter republication, guga112 E4B Q4_0, Alfredofrog E4B
  7/100 at KL 0.0043); and the separate Madras1 orthogonalization line
  (alpha 1.35, layers 12-51) whose mradermacher quants carry the largest
  download counts in the scan (6,495 / 3,407).
- Sizes and serving reality: Q4_0 GGUF 17,287,669,696 bytes plus vision
  projector 1,200,726,080 (BF16) or 809,541,440 (Q8_0) bytes; Google's own
  Q4_0 GGUF for the tier ships the same two-file shape (477,215 downloads);
  about 18.1 GB of weights fits a single 24 GB card and the site's stopped
  40 GB A100 reference class. No dated rental quote is claimed; no GPU was
  rented or started.
- Blog archive grows to **30 field notes** (4 archive pages); homepage latest
  list, blog index, RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated
  deterministically.

## Verification

- `env -u PYTHONPATH uv run --locked python -I scripts/build-blog.py` —
  built 30 articles, 4 archive pages and all generated surfaces.
- `env -u PYTHONPATH uv run --locked python -I scripts/build-blog.py --check`
  — clean.
- `env -u PYTHONPATH uv run --locked pytest -q` — 28 passed.
- `node scripts/verify-agent-ready.mjs http://localhost:8788 --local-only` —
  passed (30 model articles, no public inference, no live polling).
- In-page check (headless Chrome, 1280 px and 390 px): the TL;DR and 7
  `Basically,` callouts render, all 9 table-of-contents anchors resolve,
  11 min read, 11 fact rows and 34 source links present, no horizontal
  overflow, no console errors or failed requests on the article, blog index
  or homepage.
- `git diff --check` clean. Commit SSH-signed; deployment via the signed
  Pages pipeline on `gh-pages`.
