# ABLITERATED.cloud website v0.11.3

## llmfan46/Laguna-S-2.1-Uncensored-Heretic — the 118B coding MoE nobody has refused

- New field note: **llmfan46/Laguna-S-2.1-Uncensored-Heretic** — a Heretic weight
  edit of poolside's Laguna S 2.1 (118B total / ~8B active, 256 routed experts
  top-10 + 1 shared, 48 layers, 1,048,576-token context, OpenMDW-1.1), published
  30 August 2026 by independent editor llmfan46 (HF PRO, 1,947 followers, 204
  models, Ko-fi-funded). Publisher-measured: 6/100 refusals vs 97/100 base at KL
  0.0300. Honest boundary: editor's own evaluation set, no independent re-run;
  card's comparison table mislabels the original as Qwen3-Coder-Next (copy-paste
  bug), GGUF link broken/empty at writing (`zero_refusal: false`).
- Cross-check: a second independent uncensored build of the same base
  (Bizarrrr/Laguna-S-2.1-Uncensored, FriendliAI, base revision 00af5a51)
  publishes measured EN refusals 92.71%→2.33% (686 prompts, Minos-v1), DE
  74.49%→4.23% (NLLB-200 back-translation), XSTest 8.88%→1.87%, HumanEval
  90.24%→85.37%.
- Hosting math angle: "8B active" is routing, not storage — 218.99 GiB BF16
  across 48 shards; estimated managed price $10.90/hour (2 × H200, 50–400B MoE
  band). vLLM command from the model page: `vllm serve
  "llmfan46/Laguna-S-2.1-Uncensored-Heretic"`. Base on Ollama (q4_K_M ~96 GB).
- Reddit community search blocked (HTTP 403), gap noted in the post.
- Blog now covers **24 field notes**; homepage latest-releases list, blog index,
  RSS, sitemap, `llms.txt` and `llms-full.txt` regenerated.
