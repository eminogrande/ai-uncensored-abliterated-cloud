# ABLITERATED.cloud website v0.11.4

## 0xSojalSec/Tencent-Hy-30B-A3B-uncensored-heretic — the translator that refused

- New field note: **0xSojalSec/Tencent-Hy-30B-A3B-uncensored-heretic** — the first
  decensor of a dedicated translation model. Tencent's Hy-MT2-30B-A3B (30B total /
  ~3B active, hy_v3, 48 layers, 128 experts top-8, 262,144-token context,
  33 languages, Apache-2.0, published 11 May 2026) is a specialist translation
  tool that Tencent aligned so thoroughly its refusal screen triggered on 100/100
  keyword prompts. The 30 August 2026 edit by 0xSojalSec (Md Ismail Sojal) /
  OS-Software uses Heretic v1.4.0+custom with Arbitrary-Rank Ablation (ARA): a
  LoRA adapter with row-norm preservation on layers 18–28, optimizer ot_ridge.
  Publisher-measured: refusal keywords 100/100 → 0/100 at KL 0.0276
  (`zero_refusal: true`), on a custom mixed-language set (Japanese only for
  KLD/refusal rate). Honest boundary: publisher-measured, no independent re-run,
  prompt set unpublished.
- Hosting math: BF16 checkpoint 60.14 GB across 13 shards — one H200.
  Estimated managed price $5.45/hour (1 × H200, ~30B MoE band). vLLM:
  `vllm serve "0xSojalSec/Tencent-Hy-30B-A3B-uncensored-heretic"`. GGUF quants
  from OS-Software (Q4_K_M ~18.2 GB fits 24 GB GPU) and mradermacher i1-imatrix
  (IQ1–IQ4). No Ollama page for the family yet; Tencent's own FP8 twin
  (tencent/Hy-MT2-30B-A3B-FP8, 5,407 downloads) is the aligned fallback.
- Editor profile: 0xSojalSec = Md Ismail Sojal (7 models), org label OS-Software
  (19 models, mostly Japanese-targeted "heretic-ja" Heretic edits); no donation
  link on this card. Base creators: Tencent Hunyuan (arXiv 2605.22064, 13
  authors), WMT26 video-subtitle partner.
- Reddit community search blocked (HTTP 403), gap noted; cited base-release
  thread predates the uncensor.
- Blog now covers **25 field notes**; homepage latest-releases list, blog index,
  RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated.
