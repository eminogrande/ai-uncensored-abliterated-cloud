# ABLITERATED.cloud website v0.11.0

## Two new field notes — the 180B race and the 320B crack

- New field note: **dealignai/Qwen3.8-Flash-Next-ABLITERATED-FP8** — the
  Qwen4-experimental architecture (180B total / ~6B active, Gated DeltaNet +
  micro-block QSA sparse attention + 512-expert MoE + a 51.2B-parameter n-gram
  lookup table) abliterated five ways within 48 hours of Qwen's 24 August
  release. dealignai's official-FP8 build is the served, measured one:
  HarmBench-320 greedy real-harm compliance 100% (reasoning low) / 99.6%
  (xhigh) / 97.1% (off), MMLU 86.36 → 83.86 (−2.50pp), ~81% MTP draft
  acceptance, image + video working. Jiunsong's BF16 edit is the
  architecture-aware method: 36 storage tensors → 6,168 logical output
  projections, 842-pair corpus, hash-verified. Honest catch: released
  vLLM/SGLang still do not support `qwen4_exp` (PRs #53896 / #36497 open).
- New field note: **dealignai/GLM-5.3-Flash-ABLITERATED-FP8** — Zhipu's first
  natively multimodal GLM-5 (320B total / 18B active, hybrid KDA linear +
  sparse attention, MIT) cracked at the weight level in official FP8:
  HarmBench-320 greedy 320/320 complied with 0 refusals, 30/30 at temp 1.0 /
  top_p 0.95, MMLU-logit 86.74 → 86.26 (−0.48pp), decode 163 → 211 tok/s with
  the cracked MTP head (75.9% acceptance) on 4×H200. NVFP4 twin (~165B
  safetensors) and an UNCENSORED-FP8 mirror with identical weights.
- Blog now covers **21 field notes** (3 pages); homepage latest-releases list,
  blog index, RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated.
- Estimated managed prices: **$10.90/hour** (2 × H200 class) for both the
  180B Qwen4-preview MoE and the 320B GLM-5.3-Flash MoE.
