<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# What 'Aggressive' means: Muse-Glimmer-30B abliterated to 0/100 refusals

Published 17 August 2026. Exact artifact: `SHS-Lab/Muse-Glimmer-30B-Abliterated-Aggressive`, revision `0e74fc7c36d24c58b22cc213c14d7f0512d9f7f1`.

Muse-Glimmer-30B is Meta Superintelligence Lab's dense ~29.6B causal transformer with a ~1.8B ViT-G/14 perception encoder, distilled from Muse Spark, Apache-2.0, 52 layers, hidden size 6656, 202,048-token vocabulary and 131,072+ context. SHS-Lab's "Aggressive" abliterated variant is a KL-conserving LoRA SFT (loss `CE(compliance) + λ·KL(tuned‖base)`) where λ_KL was lowered from 1.0 to 0.5 compared to the "normal" twin. Same LoRA footprint — r=16, targets `o_proj`/`down_proj`, 31.1M trained parameters (0.10%) — so "Aggressive" here means a relaxed KL guardrail, not a stronger projection or more layers touched. Contrast that with TrevorS's norm-preserving biprojected abliteration (all 52 layers) or Blackfrost's α=1.5 three-pass residual-write edit: the same label maps to different knobs per toolchain.

Publisher-measured claims (its own harness, upstream claims): refusal rate on harmful_behaviors is 0/100 for this variant versus 13/100 for the normal twin; naive response-token KL to base is 0.1697 mean (~1.7× the normal 0.0988), p50 0.1560, p99 0.2912; over-refusal (or-bench) is 5/100 for both; correct refusals on cyber-policy-refuse drop to 0/2 because the aggressive edit "scrubs even genuinely-harmful refusals." Benchmarks were explicitly skipped: the card says capability preservation is expected to be lower than the normal variant "but was not re-measured here." Entropy-weighted KL passes (<0.02) while naive KL drifts — two meters, two readings.

This SHS-Lab upload (17 August 2026) is a mirror of jorkle's identically named release (12 August 2026, 365 downloads): card text, metrics and parameter count match to the letter. The SHS-Lab repo ships only the two BF16 shards (~56 GB); the GGUF quants (`abliterated-aggressive-Q8_0.gguf` ~28 GB, `abliterated-aggressive-Q4_K_M.gguf` ~16 GB) live in `jorkle/Muse-Glimmer-30B-Abliterated-GGUF`. At 0 downloads and 0 likes, no independent community evaluation exists yet.

Community opinion on the base's refusal behavior is split — see the "overly cencored?" thread on the base model's discussions. The only third-party measurement we found is TrevorS's harness: 128/150 (85.3%) base refusals dropping to 3/150 (2.0%) after projection, with prompt-injection and scope-adherence resistance unchanged on a 30-probe agentic axis. Meta's own base-model benchmark claims (SWE-Bench Verified 76.0, MCP Atlas 75.5, AIME 2026 94.7) do not transfer to this artifact.

## The idea, in plain words

**Two schools of removing refusals** — School one is weight projection (classic abliteration): find the refusal direction and carve it out of the weights. School two is a LoRA de-refusal: train a tiny adapter that nudges behavior without retraining the model. 'Aggressive' in this family means the scrub was turned up — 0/100 refusals measured — which also means more drift from the original model's behavior. Nothing is free.

Primary sources:

- [Exact SHS-Lab model card](https://huggingface.co/SHS-Lab/Muse-Glimmer-30B-Abliterated-Aggressive)
- [Pinned artifact](https://huggingface.co/SHS-Lab/Muse-Glimmer-30B-Abliterated-Aggressive/tree/0e74fc7c36d24c58b22cc213c14d7f0512d9f7f1)
- [jorkle "normal" variant card](https://huggingface.co/jorkle/Muse-Glimmer-30B-Abliterated)
- [jorkle aggressive twin](https://huggingface.co/jorkle/Muse-Glimmer-30B-Abliterated-Aggressive) and [GGUF quant repo](https://huggingface.co/jorkle/Muse-Glimmer-30B-Abliterated-GGUF)
- [Official Meta base model card](https://huggingface.co/meta-models/Muse-Glimmer-30B)
- [TrevorS: Muse Glimmer abliteration, method and measurements](https://github.com/TrevorS/muse-glimmer-abliteration)
- [Blackfrost GGUF abliteration card](https://huggingface.co/cvgro/Muse-Glimmer-30B-Abliterated-GGUF)
- [Base model discussion: "overly cencored?" (community opinions)](https://huggingface.co/meta-models/Muse-Glimmer-30B/discussions/47)
- [Original refusal-direction paper](https://arxiv.org/abs/2406.11717)

The 0/100 refusal figure is a publisher claim on its own 100-prompt harness; capability preservation was not re-measured, and this aggressive variant refuses fewer genuinely-harmful requests (0/2 correct refusals) than the normal twin. Verify against your own workload before deployment.
