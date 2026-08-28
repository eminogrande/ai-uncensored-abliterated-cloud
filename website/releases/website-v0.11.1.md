# ABLITERATED.cloud website v0.11.1

## Velum-Unbound-Uncensored — the 1-bit uncensor

- New field note: **guell00/Velum-Unbound-Uncensored** — a Heretic v1.4.0
  decensor of Prism ML's 1-bit Bonsai-27B (itself a Qwen3.6-27B derivative),
  repacked to Q1_0 GGUF at 1.125 bits per weight with a DSpark speculative
  drafter. Full lineage traced and sourced: gated Bonsai base → s3nh's FP16
  edit (refusals 81/100 → 6/100, KL 0.0033, editor-measured) → Thox1-27b Q1_0
  intermediate → Velum, published 28 August 2026 from Brazil (MIT card
  license). Honest boundary: the refusal measurement belongs to the FP16
  intermediate; the Q1_0 pack has no published re-test and every Velum
  benchmark is TBD.
- The Bonsai family context: ~3.1M total downloads across the 1-bit GGUF,
  MLX 1-bit and ternary packs; ~3.9 GB deployed footprint for a 27B-class
  model; runs on llama.cpp (PrismML fork) including laptops.
- Blog now covers **22 field notes**; homepage latest-releases list, blog
  index, RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated.
- Estimated managed price: $5.45/hour (1 × H200 class); noted cheaper
  single-L40S path since the weight file is ~3.9 GB.
