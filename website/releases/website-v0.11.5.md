# ABLITERATED.cloud website v0.11.5

## apetersson/DeepSeek-V4-Flash-Vision-Exp-Abliterated — eleven hours, then a paper trail

- New field note: **apetersson/DeepSeek-V4-Flash-Vision-Exp-Abliterated** — the
  first abliteration of DeepSeek's first open multimodal model,
  DeepSeek-V4-Flash-Vision-Exp (285B total / 13B active MoE, 43 layers,
  256 experts top-6, 32-layer vision encoder, DSpark self-draft, 1,048,576-token
  context, MIT, published 31 Aug 2026 06:16 UTC). Andreas Petersson's rank-1
  edit (targeted projection edits, not gradient fine-tuning) landed 17:12 UTC
  the same day, ten hours and fifty-six minutes after the base: 33 attention
  output projection tensors in layers 10–42, one refusal direction, pinned
  revision 71e308af…6ddd5c94. Honest boundary: text and focused image smoke
  tests pass, broader quality/safety/production evaluation pending, no
  refusal-rate benchmark published (`zero_refusal: false`).
- The descendant pipeline: within 24 hours s-zaizen grafted the same edit onto
  an NVFP4 quant (one rank-1 direction at strength 3.5, L2-preserving, 3 FP8
  requant passes, build receipt pinned; 48/48 shards matched against donor,
  8/8 safe-boundary prompts answered with zero refusals, GSM8K 99/100, +3.0 vs
  its own unedited base) and audreyt baked it into an IQ2_XXS ds4 GGUF
  (86.72 GB, HTTP-Range graft of Q8_0 payloads, SHA-256-verified; refusal
  direction traced back to drowzeys's 0731 DSpark abliteration). msuiche
  shipped a fourth, cyber-flavored take the same day.
- Hosting math: ~202 GB FP8-native checkpoint (experts FP4, attention FP8, BF16
  vision tower). Estimated managed price $10.90/hour (2 × H200, 50–400B MoE
  band). vLLM/SGLang with DSpark self-draft per DeepSeek card; Mac path via
  antirez's ds4 runtime and the Basic128-Routed-IQ2_M profile (95.76 GiB,
  resident-128-GiB, ~23.4 tok/s text on M1 Ultra per card).
- Editor profile: apetersson = Andreas Petersson (7 models), the 0731
  abliteration specialist whose DS4-Headroom128 GGUF (83,938 downloads) and FP8
  build (18,794 downloads) already powered this site's readers; no socials or
  donation links, the catalog is the brand. Base: DeepSeek-AI. Descendants:
  s-zaizen (Model Optimizer / DGX Spark lineage, zaizen.me), audreyt.
- Reddit community search blocked (HTTP 403), gap noted in the post; community
  signal sourced from the base repo's own discussions (DGX Spark support, MLX
  requests, DSpark acceptance rate).
- Blog now covers **26 field notes**; homepage latest-releases list, blog index,
  RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated.
