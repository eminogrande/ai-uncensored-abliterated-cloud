<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# The 118B coding MoE nobody has refused

Published 30 August 2026. Exact artifact: `llmfan46/Laguna-S-2.1-Uncensored-Heretic`, revision `c8a210847c1092c2c89ce814dc6a623b8afb0320`.

Poolside's Laguna S 2.1 is an agentic coding foundation model: 118B total parameters, ~8B active per token, 256 routed experts (top-10) plus one shared expert, 48 layers, a 1,048,576-token context window, and interleaved thinking with tool calls. Poolside's release post (21 July 2026) reports Terminal-Bench 2.1 70.2% and DeepSWE 40.4%, and says the model went from the start of training to launch in under nine weeks.

On 30 August 2026 the independent publisher llmfan46 released a Heretic-based weight edit that removes the refusal behavior. The card reports 6/100 refusals vs 97/100 on the base at KL divergence 0.0300 — a publisher-measured number on the editor's own evaluation set, not independently re-run. The derivative keeps the base's OpenMDW-1.1 license and ships as BF16: 218.99 GiB across 48 safetensors shards, verified via the files-tree API. The card's performance table mislabels the "Original model" as Qwen3-Coder-Next (a copy-paste from another llmfan46 card), and its GGUF link points to a doubled name that errors; the Vision-GGUF repo exists but is empty as of writing. The reliable quant path today is the upstream poolside GGUF/MLX on Ollama (`ollama run laguna-s-2.1`, q4_K_M ~96 GB).

A second, independent uncensored build of the same base — Bizarrrr/Laguna-S-2.1-Uncensored on FriendliAI (base revision 00af5a51) — publishes measurements with the pinned NousResearch/Minos-v1 classifier: English refusals 92.71% (636/686) → 2.33% (16/686), German refusals 74.49% (511) → 4.23% (29) via NLLB-200 back-translation, XSTest over-refusal 8.88% → 1.87%, HumanEval pass@1 90.24% → 85.37%. Those numbers belong to that other checkpoint, not to llmfan46's.

Estimated managed price: ≈ $10.90/h (2 × H200) — the 50–400B MoE band of our pricing formula. Hosting command: `vllm serve "llmfan46/Laguna-S-2.1-Uncensored-Heretic"`.

The creator: llmfan46 — Hugging Face PRO, 1,947 followers, 204 models, funded via ko-fi.com/llmfan46 (vote on models, request specific abliterations). Cards carry a banner that Hugging Face's free storage limit has been reached; several models were published the same day. No member-since date is published; biographical details trace to the profile, card banner and Ko-fi link.

## The idea, in plain words

**Why 118 billion parameters only cost 8 billion per answer** — This is a mixture of experts (MoE) with a token-choice router: 256 specialized 'expert' modules plus one always-on shared expert, and for each token the model wakes up just ten of them. You store the full brain — 118B parameters, 219 GB of weights — but each thought only pays compute for the ~8B experts it needs. That is how a model too big for one GPU can still respond at interactive speed, and why '8B active' never means 'small download'.

Primary sources:

- [Exact uncensored model card](https://huggingface.co/llmfan46/Laguna-S-2.1-Uncensored-Heretic)
- [HF model API (architecture, revision, license)](https://huggingface.co/api/models/llmfan46/Laguna-S-2.1-Uncensored-Heretic)
- [Official poolside Laguna S 2.1 card](https://huggingface.co/poolside/Laguna-S-2.1)
- [Poolside release post (21 July 2026)](https://poolside.ai/blog/introducing-laguna-s-2-1)
- [OpenRouter listing (pricing, 1M context)](https://openrouter.ai/poolside/laguna-s-2.1)
- [Ollama base page (GGUF/MLX tags)](https://ollama.com/library/laguna-s-2.1)
- [FriendliAI: independent uncensored build with measured EN/DE refusals](https://friendli.ai/models/Bizarrrr/Laguna-S-2.1-Uncensored)
- [llmfan46 profile](https://huggingface.co/llmfan46) and [Ko-fi](https://ko-fi.com/llmfan46)
- [OpenMDW license](https://openmdw.ai/)

Safety filtering is significantly reduced in this edit — that is the whole point, and it changes both what the model says and, as an agent, what it does with a tool.
