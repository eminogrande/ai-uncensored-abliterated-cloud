# The first Nemotron-H abliteration: 3,126 tensors, 0.000160 leakage

Published 25 August 2026. Exact artifact: `HangGlidersRule/Darkstar-Nemotron-3.5-Lightning-30B-A3B-Abliterated-BF16`, revision `f3723fc56c3e05bf8a9499b985dec8cced37027c`.

NVIDIA's newest open release — Nemotron 3.5 Lightning, a 30B-total/~3B-active hybrid of Mamba-2 state-space blocks, mixture-of-experts and sparse attention — is built for the execution layer of always-on agents. Two weeks after its 11 August launch, publisher HangGlidersRule edited it under the Darkstar brand: the refusal direction measured at layer 34 projected out of 3,126 residual-writing tensors, verified in a numbered edit contract. This is the first Nemotron-H abliteration covered on this site.

The edit contract is unusually explicit. Using 320 harmful and 320 harmless chat-templated prompts, the refusal direction (dimension 2688, norm 1.0000) was measured at layer 34 and projected out of 3,126 tensors: 2,944 routed-expert down-projections, 23 shared-expert down-projections, 6 attention output projections, 23 Mamba output projections, the MTP head's o_proj and 128 expert down-projections, and the embedding weight. All in float32, shard-by-shard, re-rounded to BF16. The contract reports 3,126/3,126 edited, maximum normalized residual leakage 0.000160 (gate 0.01), MTP head intact, all non-edited weights byte-identical to upstream. Publisher-measured behavior gate: 200/200 harmful compliance, 0/83 safe over-refusals, 0 errors.

The NVFP4 twin (~22 GB, 3 shards) quantizes only the 5,934 expert up/down projections to W4A16-NVFP4 while keeping Mamba/SSM tensors, norms, embeddings, lm_head and MTP head in BF16. On a single RTX PRO 6000 Blackwell it scores GPQA Diamond 141/198 = 71.2%, with the card explicitly attributing the gap to NVIDIA's 75.44 to serving-stack config (vLLM version, FP8 KV, TP2, temp 1.0, 8 repeats) rather than to abliteration or quantization damage. Throughput with MTP10: 554.7 tok/s weighted across 4K/16K/48K contexts.

NVIDIA's official benchmarks on the base: GPQA Diamond 75.44, MMLU Pro 81.94, SWE-bench Verified 51.56, Terminal-Bench 2.1 24.58, PinchBench 85.37. The 3B-active design means a small model's speed with a much larger model's knowledge; NVIDIA pairs it with NeMo Switchyard for routing.

## How to run it

BF16 edit, vLLM:

```bash
vllm serve HangGlidersRule/Darkstar-Nemotron-3.5-Lightning-30B-A3B-Abliterated-BF16 \
  --max-model-len 131072 --kv-cache-dtype bfloat16 --reasoning-parser nemotron_v3 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":12}'
```

Single consumer GPU: the NVFP4 twin (~22 GB) with the same flags at 10 speculative tokens. No GGUF/Ollama page exists for the edit yet; the upstream NVIDIA checkpoint has an official ggml-org GGUF for local devices. Safety filtering is significantly reduced in this edit — that's the point.

## The creator: HangGlidersRule

A Hugging Face PRO publisher running the model-forge GitHub repository — "reproducible model transformation, quantization, serving, evaluation, and Darkstar release catalog" — with pinned recipes, fail-closed validators, sha256 manifests, and a public/private separation between published records and operation archives. The GitHub profile names the operator "bob" in Washington DC, an account from 2011. The same Darkstar brand shipped a Qwen3.8-27B abliteration family in late August. The base is NVIDIA's, released under OpenMDW-1.1 with weights, data and recipes; the derivative retains the license.

## The idea, in plain words

**A state-space block is a way to remember without a cache** — Normal transformers replay the whole past conversation for every new token; a Mamba-2 state-space block compresses history into a fixed-size internal state and updates it as it goes, which is faster and far less memory-hungry per token. Nemotron 3.5 Lightning interleaves those blocks with classic mixture-of-experts layers, firing only ~3B of its 30B parameters per token. Abliterating that hybrid means removing the refusal direction from the Mamba output projections and expert down-projections too — the edit touches every kind of residual writer the architecture has.

Primary sources:

- [Exact Darkstar BF16 card](https://huggingface.co/HangGlidersRule/Darkstar-Nemotron-3.5-Lightning-30B-A3B-Abliterated-BF16)
- [Pinned artifact](https://huggingface.co/HangGlidersRule/Darkstar-Nemotron-3.5-Lightning-30B-A3B-Abliterated-BF16/tree/f3723fc56c3e05bf8a9499b985dec8cced37027c)
- [Darkstar NVFP4 twin and quantization contract](https://huggingface.co/HangGlidersRule/Darkstar-Nemotron-3.5-Lightning-30B-A3B-Abliterated-ModelOpt-W4A16-NVFP4)
- [Official NVIDIA BF16 card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) and [NVFP4 card with benchmark table](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4)
- [NVIDIA technical blog — Nemotron 3.5 Lightning launch](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/)
- [model-forge — reproducible Darkstar pipeline](https://github.com/HangGlidersRule/model-forge)
- [Refusal in Language Models Is Mediated by a Single Direction](https://arxiv.org/abs/2406.11717)

The publisher measured 200/200 harmful compliance and 0/83 safe over-refusals on both artifacts — a real, disclosed measurement, not a general "never refuses" claim.
