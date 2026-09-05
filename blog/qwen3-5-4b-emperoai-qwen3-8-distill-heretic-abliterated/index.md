<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# Small uncensored agents: what a 4.5B Heretic distill is for

Published 17 August 2026. Exact artifact: `insraq/Qwen3.5-4B-EmperoAI-Qwen3.8-Distill-Heretic-Abliterated`, revision `ef859957528c1fceda193c54a7630c2ac9aad423`.

A decensored version of `empero-ai/Qwen3.8-4B` made with Heretic v1.4.0: 4,539,265,536 parameters, about 9.1 GB of BF16 weights, 262,144-token native context, Apache-2.0. Empero's Qwen3.8-4B is a full-parameter distillation of Qwen3.8 2.4T A95B into the Qwen3.5-4B architecture, trained on ~45,000 curated teacher traces of dense chain-of-thought with native function calling per the Qwen3.5 spec. The fine-tune is text-only; vision is inherited but was not evaluated.

Heretic (p-e-w, AGPL-3.0) differs from classic abliteration by automating the search: a TPE-based optimizer powered by Optuna co-minimizes refusals and KL divergence from the base. The pinned reproduction package records the base commit (c83cb7a), prompt datasets, RNG seed, an Optuna study journal and SHA256SUMS; `heretic --reproduce reproduce.json` should rebuild the weights hash-identical. Selected trial 128: the publisher reports 6/100 refusals (vs 99/100) and KL divergence 0.0167 (vs 0 by definition) — publisher claims, though auditable ones. Abliteration parameters include a direction index of 20.01 and projection weights up to 1.50, an over-projection concentrated in the upper layers.

Empero's upstream benchmark claims for the distill (lm-evaluation-harness, identical settings vs Qwen3.5-4B): gsm8k_cot 0.785 vs 0.850, MMLU CoT 0.553 vs 0.354. Those belong to the distill, not the decensored artifact, which has no independent evaluation: at the time of writing the repo had zero downloads, zero likes and zero discussions. Empero's card notes the linear-attention layers require Gated DeltaNet kernels and that greedy decoding is a known repetition-loop failure mode; recommended sampling is temperature 0.6, top_p 0.95, top_k 20.

Our serving estimate is approximately $2.34/hour on one L40S (approximate managed price estimate). The 4B class buys refusal-free, local, tool-calling text at that price; it does not buy frontier reasoning, and decensored does not mean truthful or harmless.

## The idea, in plain words

**A 2.4-trillion-parameter teacher writing homework for a 4-billion student** — Knowledge distillation trains a small model on the outputs of a huge one. The student copies how the teacher answers, compressed into a fraction of the size — here, a 4.5B model that fits in ~8 GB and runs on a laptop. You lose some ceiling, but you get a model you can actually run anywhere, uncensored.

Primary sources:

- [Exact model card](https://huggingface.co/insraq/Qwen3.5-4B-EmperoAI-Qwen3.8-Distill-Heretic-Abliterated)
- [Pinned artifact](https://huggingface.co/insraq/Qwen3.5-4B-EmperoAI-Qwen3.8-Distill-Heretic-Abliterated/tree/ef859957528c1fceda193c54a7630c2ac9aad423)
- [Reproduction guide](https://huggingface.co/insraq/Qwen3.5-4B-EmperoAI-Qwen3.8-Distill-Heretic-Abliterated/blob/ef859957528c1fceda193c54a7630c2ac9aad423/reproduce/README.md)
- [Base distill card (empero-ai)](https://huggingface.co/empero-ai/Qwen3.8-4B)
- [Architecture base (Qwen)](https://huggingface.co/Qwen/Qwen3.5-4B)
- [Heretic tool](https://github.com/p-e-w/heretic) and [project site](https://heretic-project.org)
- [Original refusal-direction paper](https://arxiv.org/abs/2406.11717)
- [Hugging Face model API entry](https://huggingface.co/api/models/insraq/Qwen3.5-4B-EmperoAI-Qwen3.8-Distill-Heretic-Abliterated)
- [r/LocalLLaMA Heretic thread](https://old.reddit.com/r/LocalLLaMA/comments/1oymku1/heretic_fully_automatic_censorship_removal_for/) (community opinion, via Heretic README)

Coverage note: a direct Reddit search for "4B uncensored" returned HTTP 403, so community coverage here is limited to what the Heretic README quotes.
