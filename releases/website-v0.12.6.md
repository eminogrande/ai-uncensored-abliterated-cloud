# ABLITERATED.cloud website v0.12.6

One new field note in the editorial archive: the day-one uncensoring wave on
DeepSeek's official V4.1-Flash. No runtime, cost snapshot or hosting change:
the Vast.ai reference instance stays stopped at the 5 September snapshot, and
this release only extends the editorial archive and its regenerated indexes.

## deepseek-v4-1-flash-day-one-uncensoring

- New field note: **DeepSeek-V4.1-Flash** (552B backbone, 8B active per token
  in prefill and 16B in decode, causal encoder-decoder, 384 routed experts,
  Engram memory, 1M-token context, MIT, released 10 Sep 2026, 1,516 likes in
  its first day) uncensored three independent ways within 19 hours.
- **s-zaizen/DeepSeek-V4.1-Flash-Abliterated** (10:59 UTC, +8h41m): Heretic
  at commit 3521f864, `per_all_4p5` on all 40 attention output projections,
  keyword-screen refusals 97/100 to 24/100 on the same 100-prompt screen
  (seed 42, temp 0). Publisher-measured; the card says it is not a general
  capability benchmark.
- **msuiche/DeepSeek-V4.1-Flash-abliterated-cyber-GLP-39** (13:47 UTC,
  +11h30m): a gated 800 KB control vector, 39 unit-norm directions at layers
  1-39, applied at the post-layer residual stream with alpha 0.5 baked in;
  compliance 4/32 to 24/32 on a refusal set and 5/32 to 31/32 on a cyber
  set; alpha 1.0 code-switches, alpha 2.0 regresses to 19/32. No weights
  modified; calibrated to base revision fb2764a5 only.
- **dealignai/DeepSeek-V4.1-Flash-UNCENSORED-FP8** (21:02 UTC, +18h44m): a
  CRACK-brand weight-level edit reporting 320/320 HarmBench-320 compliance
  versus 137/320 stock at reasoning off (and 5/320 stock at max effort);
  MMLU-14k 86.96% to 82.74% (-4.22pp; -1.1pp excluding the ethics cluster,
  with the moral-scenarios drop of 39.89pp disclosed). Publisher-measured.
- Serving and size reality documented from primary sources: SGLang `dsv4.1`
  preview branch (PR 38798, validated on 4x H200), vLLM PRs 56201/56214/56228
  still unmerged, llama.cpp converter-only (cannot load V4.1), community MLX
  port, 4x DGX Spark recipe; day-one reductions (NVFP4 399.9 GiB, mixed-Q2
  GGUF 169.92 GB, MLX 427.6 GB, REAP 2-bit ~199 GiB, EXL3 3.5 bpw) all stay
  datacenter-sized. No dated rental quote is claimed: every published quant
  is outside this site's stopped 40 GB reference class.
- Blog archive grows to **29 field notes** (4 archive pages); homepage latest
  list, blog index, RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated
  deterministically.

## Verification

- `env -u PYTHONPATH uv run --locked python -I scripts/build-blog.py` —
  built 29 articles, 4 archive pages and all generated surfaces.
- `env -u PYTHONPATH uv run --locked python -I scripts/build-blog.py --check`
  — clean.
- `env -u PYTHONPATH uv run --locked pytest -q` — 28 passed.
- `node scripts/verify-agent-ready.mjs http://localhost:8788 --local-only` —
  passed (29 archived articles, no public inference, no live polling).
- In-page check (headless Chrome, 1280 px and 390 px): 9 `Basically,`
  callouts and the TL;DR render, all 11 table-of-contents anchors resolve,
  reading time and 35 source links present, no horizontal overflow, no
  console errors on article, blog index or homepage.
- `git diff --check` clean. Commit SSH-signed; deployment via the signed
  Pages pipeline on `gh-pages`.
