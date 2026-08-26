# ABLITERATED.cloud website v0.10.0

## Darkstar Nemotron-3.5-Lightning 30B-A3B — the first Nemotron-H abliteration

- New field note: **HangGlidersRule/Darkstar-Nemotron-3.5-Lightning-30B-A3B-Abliterated-BF16**
  — the first Nemotron-H coverage on this site. NVIDIA's newest open model is a
  hybrid of Mamba-2 state-space blocks, mixture-of-experts and sparse attention,
  30B total / ~3B active, built for the agent execution layer. Published 11
  August 2026; the Darkstar edit landed 25 August 2026.
- The edit contract is unusually explicit: refusal direction measured at layer 34
  (320 harmful / 320 harmless prompts), projected out of 3,126 residual-writing
  tensors — 2,944 routed-expert down-projections, 23 shared-expert
  down-projections, 6 attention o_proj, 23 Mamba out_proj, MTP head tensors, and
  the embedding weight — in float32 shard-by-shard. Verified 3,126/3,126 edited,
  max normalized residual leakage 0.000160 (gate 0.01).
- Publisher-measured behavior gate: **200/200 harmful compliance, 0/83 safe
  over-refusals, 0 errors** → `zero_refusal: true`.
- NVFP4 twin (~22 GB, 3 shards) quantizes 5,934 expert projections to
  W4A16-NVFP4 while keeping Mamba/SSM tensors, norms, embeddings, lm_head and
  MTP head in BF16; GPQA Diamond 141/198 = 71.2% on a single RTX PRO 6000
  Blackwell, delta to NVIDIA's 75.44 explicitly attributed to serving-stack
  config, not to the edit.
- Estimated managed price: **$5.45/hour** (1 × H200 profile, 30B-A3B class).
- Blog now covers **19 field notes**; homepage latest-releases list, blog index,
  RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated (3 blog pages now).
- Local agent-readiness verification passed (wrangler dev @ localhost:8788).
