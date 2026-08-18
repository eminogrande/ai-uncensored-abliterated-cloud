# Three ARA passes: how RVN got Qwen3.8-27B down to 0–1/100 refusals

Published 14 August 2026. Exact artifact: `0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF`, revision `d8a1b834aa6f08e7b60dd4fb7586b90fd5a44363`.

Most abliteration is a single surgery: find the refusal direction, subtract it, ship. RVN is the opposite approach — abliteration as a matrix optimization problem, run three times in a row. 0bserverx published it on 14 August 2026 as a GGUF-only release, and in four days it pulled 106,110 downloads and 121 likes, making it the most-downloaded uncensored Qwen3.8-27B variant on Hugging Face right now. Parameters: 27B dense (27,781,427,952 in the base), qwen3_5_text architecture (16 full attention + 48 Gated DeltaNet layers), 262,144-token native context, Apache-2.0, 25 GGUF quants from F16 (53.81 GB) down to IQ1_S (7.15 GB). Approximate managed price estimate: ≈ $5.45/h on one H200; Q4_K_M fits a single 24 GB GPU.

## Why three passes instead of one

RVN starts from [trohrbaugh/Qwen3.8-27B-heretic-ara](https://huggingface.co/trohrbaugh/Qwen3.8-27B-heretic-ara), Tim Rohrbaugh's ARA abliteration of Qwen3.8-27B, published the same day. That first pass already measured well: 3/100 refusals at KL 0.0535 against the base. 0bserverx's own evaluation still found three harmful-prompt categories refusing — a racism website, malware, and government database hacking — so he ran the ARA procedure *again* on the result, and then a third time. The final numbers on the card: 0–1/100 refusals (the single survivor is a chemical-weapon WMD prompt, a guardrail deliberately kept), with KL damage against the base dropping from 0.0535 to 0.0085 — roughly a sixfold improvement in behavioral preservation.

That "KL drops as you pass again" result is the interesting part. A naive expectation would be that each extra edit adds damage. Instead the measurement says the opposite: a well-tuned ARA pass can remove more refusal behavior *and* land closer to the original model's behavior, because residual refusals were forcing the model off-manifold in the first place. The card reports both numbers as publisher measurements, verified on two rented GPU machines with prefix-forced (real-answer) refusal measurement.

## ARA is a different animal from directional abliteration

Classic directional abliteration — the [refusal-direction method from the Arditi et al. paper](https://arxiv.org/abs/2406.11717) — estimates one direction in activation space and projects it out of selected weights. It is a one-shot, low-rank surgery, and it is what most "abliterated" repos on the Hub actually ran. ARA (Arbitrary-Rank Ablation), implemented in [p-e-w/heretic](https://github.com/p-e-w/heretic) — 27,784 stars, "Fully automatic censorship removal for language models" — treats the edit as a matrix optimization instead.

For every target module (attention out-projection and MLP down-projection), the tool collects activations on harmless and harmful prompt sets, then an LBFGS optimizer rewrites the weight matrix with three objectives: preserve outputs on good prompts (KL kept low), steer outputs on bad prompts toward the good-prompt manifold via k-nearest-neighbor distances, and overcorrect by pushing bad-prompt outputs away from their original values to break multi-stage refusal chains. Because the weight matrix is optimized directly rather than reduced to a single direction, ARA can carve out a much richer refusal-removal subspace. RVN's passes use the same tight parameter set throughout: layers 26–56, preserve weight 0.9432, steer 0.0009, overcorrect 0.5038, neighbor count 10.

Rohrbaugh's own [-ara card](https://huggingface.co/trohrbaugh/Qwen3.8-27B-heretic-ara) publishes its numbers plainly: 0/100 refusals on its own harmful-prompt set, KL 0.0535, Apache-2.0, tagged "reproducible" — and it is the first heretic output to handle Qwen3.8's Gated DeltaNet hybrid layers at all, thanks to Rohrbaugh's upstream contributions to the heretic codebase (row-norm preservation, Qwen3.5 MoE/DeltaNet handling).

## The GGUF-only release, and the KV math behind it

RVN ships only as GGUF — 25 quants from F16 down to IQ1_S, all converted with `--no-nextn` so the MTP/NextN draft tensors are excluded. The recommended file is Q4_K_M at 16.55 GB, sized for a 24 GB card. The card includes a full GPU memory guide: 8 GB cards get IQ1/IQ2, 16 GB gets Q3_K_M plus a 16K context, and 64 GB-class hardware can hold F16.

The context math matters more than usual here because this base has a huge native window: 262,144 tokens. With GQA (4 KV heads, head_dim 256) across 64 layers, the KV cache costs 256 KiB per token in FP16 — so 16K context is about 4.2 GB, 32K is 8.4 GB, 64K is 16.8 GB, and Q8_0 KV halves all of it. The card's rule of thumb: pick the largest quant that leaves at least 4 GB for KV cache and compute buffers. That is the practical bottleneck on this family, not raw parameter count.

## A corrupted quant, caught by the community

The release also produced one of the more honest quant incidents on the Hub. On 16 August, users reported that `RVN-IQ3_M.gguf` generated nothing but `/` characters in every backend. 0bserverx's tensor-level audit found the cause: NaN/Inf block scales and fully zeroed tensors — `token_embd` alone held roughly 39.6 million NaN values — from a bad quantize run, not a llama.cpp regression. The file was pulled, re-quantized from F16 with a freshly computed imatrix, generation-tested ("The capital of France is" → Paris, 70+ t/s), and re-uploaded on 17 August, with the whole incident documented in the card, including the exact re-quantization provenance.

**The loud comment section.** The repo's discussion tab is a useful honesty check. Threads titled "Not uncensored. Lots of refusals.", "Censored" and "Still censored" all ran this week. Testers (Zen Crab, Max Vision, anonymous accounts) reported refusals on early quants and on thinking-enabled runs; 0bserverx replied to each thread, swapped the bugged uploads, and asked people to re-download. One tester's last word: "only uncensored when thinking is disabled". The threads are closed, the publisher's own measurement claims 0–1/100, and the community's experience has ranged from "good" to "still refusing" depending on quant, thinking mode, and prompt. That range is the real picture of this model.

## The creator: 0bserverx (Efe Buken)

The publisher behind RVN is the Hugging Face user [0bserverx](https://huggingface.co/0bserverx) — Efe Buken, a PRO account with 21 followers and just two public model repos: this one and [Muse-Glimmer-30B-Heretic-Uncensored-GGUF](https://huggingface.co/0bserverx/Muse-Glimmer-30B-Heretic-Uncensored-GGUF) (39,216 downloads). The RVN repo is his breakout: 106,110 downloads and 121 likes four days after creation. He credits the foundation to Tim Rohrbaugh ([trohrbaugh](https://huggingface.co/trohrbaugh)), a PRO account with 120 followers and 54 model repos — a prolific heretic/ARA producer whose catalogue spans Gemma, Nemotron, Ling and the Qwen3.5/3.6 families. Both operate as individuals, no organization page, no paywall, Apache-2.0 throughout. RVN is a refinement play: take someone else's strong ARA result, squeeze it twice more, publish the measurements.

## How to run it

No Ollama page exists for this model, so the practical path is a GGUF runtime. The Q4_K_M file fits a 24 GB GPU; Q6_K and Q8_0 need 32 GB.

```sh
llama-server -m RVN-Q4_K_M.gguf -ngl 99 -c 32768
# vLLM loads a single GGUF file explicitly (the repo holds 25 quants):
vllm serve ./RVN-Q4_K_M.gguf --quantization gguf --load-format gguf
```

ABLITERATED.cloud's approximate managed price estimate for the dense 27B class is **≈ $5.45/h** on one H200; the Q4_K_M path drops the hardware requirement to a single 24 GB GPU.

## How we treat it

The refusal story here is a measured partial: 0–1/100 on a prefix-forced 100-prompt set, published by the publisher, with the surviving refusal deliberately kept and the community threads documenting real variance. That is not a zero-refusal claim — it is a specific, checkable number with a documented incident log, which is more than most abliteration cards ship. The base Qwen3.8-27B itself is Apache-2.0, and so are both derivatives in the chain. The one honest line: this is refusal-reduced by design — a measured 0–1/100 on the publisher's set, not zero on every prompt, and some users still hit refusals.

## The idea, in plain words

**Layers 26–56, rewritten so "bad" prompts behave like "good" ones** — ARA treats the model's weights as the thing to optimize, not a single activation direction. For each targeted layer it collects examples of the model answering and refusing, then uses a numeric optimizer to adjust the weight matrices so harmless requests barely change while harmful requests stop triggering the refusal circuitry — and pushes the refusal answers even further away to break multi-stage refusal chains. Run that procedure three times, measure, and you have RVN.

Primary sources:

- [Exact model card](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)
- [Pinned artifact](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/tree/d8a1b834aa6f08e7b60dd4fb7586b90fd5a44363)
- [Hugging Face model API](https://huggingface.co/api/models/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)
- [trohrbaugh/Qwen3.8-27B-heretic-ara card](https://huggingface.co/trohrbaugh/Qwen3.8-27B-heretic-ara)
- [Official Qwen3.8-27B card](https://huggingface.co/Qwen/Qwen3.8-27B)
- [p-e-w/heretic — ARA implementation](https://github.com/p-e-w/heretic)
- [Repo discussions](https://huggingface.co/api/models/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/discussions)
- [Original refusal-direction paper](https://arxiv.org/abs/2406.11717)
