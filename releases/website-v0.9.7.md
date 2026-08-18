# ABLITERATED.cloud website v0.9.7

- **Two new model field notes** (16 total, newest first):
  - `Goodoldjam/DiffusionGemma-26B-E38-Abliterated-NVFP4` — the first
    abliterated diffusion LLM. Google's 25.2B A4B DiffusionGemma, E38
    middle-layer abliteration, quantized 51.68 GB → 18.86 GB NVFP4.
    Publisher measurements: 0/402 target refusals, 0/249 benign false
    refusals, 1,053.64 tok/s aggregate on one RTX PRO 6000 Blackwell.
    Estimated ≈ $5.45/h (1 × H200; NVFP4 fits a 32 GB consumer GPU).
  - `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF` (RVN) — a
    triple-pass ARA abliteration of Qwen3.8-27B: KL 0.0535 → 0.0085,
    refusals 3/100 → 0–1/100 (publisher measured, prefix-forced), 106K
    downloads in four days. 25 GGUF quants; the card documents a corrupted
    IQ3_M quant incident and the community pushback threads in full.
    Estimated ≈ $5.45/h (1 × H200; Q4_K_M fits a 24 GB GPU).
- Homepage "Latest uncensored releases" list, blog index, RSS, sitemap,
  `llms.txt` and `llms-full.txt` regenerated from the manifest.
- 82 tests pass; local agent-readiness verification passes.
