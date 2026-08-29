# ABLITERATED.cloud website v0.11.2

## SecureLayer7/AFM-4.5B-Uncensored-Abliterated — the security vendor uncensor

- New field note: **Securelayer7/AFM-4.5B-Uncensored-Abliterated** — the first
  Arcee Foundation Model abliteration, published by offensive-security vendor
  SecureLayer7 on 28 August 2026. Heretic / Optuna TPE refusal-direction edit
  on the attention output projections and MLP down-projections across all 36
  layers, merged into the weights (no adapter). Publisher-measured: refusals
  92/100 on the base to 3/100 at KL 0.0200; NOTICE file carries the same
  numbers and the copyright line "SecureLayer7 (Waxspace)".
- Base context: arcee-ai/AFM-4.5B (Apache-2.0, dense 4.5B, 4,619,189,760
  params, 8T training tokens, GQA + ReLU² activations, DatologyAI curation,
  TorchTitan/Axolotl/Verifiers pipeline, 11 languages, 10,691 downloads / 101
  likes). Config: hidden 2560, 36 layers, 20 heads / 4 KV, 65,536-token native
  context (YaRN ×20), ~8.6 GiB across two safetensors shards.
- Publisher: SecureLayer7 (Pune and Austin, CREST / CERT-In / SOC 2 / ISO
  27001 per its own site) — fifth uncensored release since 16 August
  (Qwythos-9B 568 dl, Ling-3.0-tiny 409 dl, Qwen3.8-27B LoRA 20 dl), plus the
  promptpurify guardrail. Honest boundary: 3/100 is a partial edit, no
  independent re-test, no discussions, zero downloads at research time
  (`zero_refusal: false`); the card itself requires serving-layer filtering.
- Reddit community search blocked (HTTP 403) — gap noted in the post.
- Blog now covers **23 field notes**; homepage latest-releases list, blog
  index, RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated.
- Estimated managed price: $2.34/hour (1 × L40S class); 8.6 GiB weights fit a
  24 GB consumer card.
