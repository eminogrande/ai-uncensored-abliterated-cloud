# ABLITERATED.cloud website v0.12.5

One new field note in the editorial archive: the reproducible Heretic uncensor of
OpenBMB's MiniCPM5-2B. No runtime, cost snapshot or hosting change: the Vast.ai
instance stays stopped, and this release only extends the editorial archive and
its regenerated indexes.

## minicpm5-2b-heretic-abliterated-reproducible

- New field note: **insraq/MiniCPM5-2B-heretic-abliterated** — the first
  reproducible decensor of OpenBMB's official MiniCPM5-2B (2,516,756,480
  params, dense LlamaForCausalLM, 131,072-token context, Apache-2.0, released
  6 Sep 2026 with the open UltraData family). Stock, the editor's screen
  measured 99 refusals of 100 prompts.
- The edit uses Heretic v1.4.0 and is published as trial 254 of a 254-trial
  Optuna Pareto search: 5/100 refusals at KL 0.0391 on the same screen,
  publisher-measured, with the base commit, prompt datasets, RNG seed, full
  Optuna journal and SHA256SUMS shipped in `reproduce/` so a rebuild is
  byte-checkable. No zero-refusal badge is attached.
- Community quant wave within two days of the edit: mondk GGUF ladder (F16
  5.04 GB down to IQ3_M 1.23 GB) plus MLX 4-bit and safetensors repack,
  mradermacher imatrix GGUF and Abiray GGUF, all on the unmodified Llama
  architecture.
- No dated rental quote is claimed in this article: a fresh provider quote for
  a 2B serving box was not fetched, and the largest rung (F16, ~4.7 GiB) is
  below the GPU class of this site's stopped reference snapshot. Historical
  estimates elsewhere in the archive stay historical.
- Blog archive grows to **28 field notes** (4 archive pages); homepage latest
  list, blog index, RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated
  deterministically.

## Verification

- `env -u PYTHONPATH uv run python -I scripts/build-blog.py` — built 28
  articles, 4 archive pages and all generated surfaces.
- `env -u PYTHONPATH uv run python -I scripts/build-blog.py --check` — clean.
- `env -u PYTHONPATH uv run pytest -q` — 28 passed.
- `node scripts/verify-agent-ready.mjs http://localhost:8788 --local-only` —
  passed (28 archived articles, no public inference, no live polling).
- `git diff --check` clean. Commit SSH-signed; deployment via the signed Pages
  pipeline on `gh-pages`.
