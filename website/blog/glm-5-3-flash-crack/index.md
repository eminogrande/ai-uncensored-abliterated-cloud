# GLM-5.3-Flash, cracked open: 320B total, 18B active, 320/320

Published 26 August 2026. Exact artifact: `dealignai/GLM-5.3-Flash-ABLITERATED-FP8`, revision `68fdc7b6c6ef90c40583f5f9224d402cc8fdf8b7`.

A day after Zhipu released GLM-5.3-Flash — the first natively multimodal model in the GLM-5 series, 320B total parameters with just 18B active — dealignai published a "CRACK" release that removes refusal behavior at the weight level, in official FP8, and then measured the result hard enough to matter. The headline number is 320/320: every behavior in a HarmBench-320 evaluation complied at greedy decoding, with zero refusals, zero soft refusals and zero garbage, and it holds at sampling parameters too (30/30 on the harshest set). Capability loss is −0.48 points on MMLU-logit. That is an unusually well-documented uncensored release for a 320-billion-parameter model.

## The base: Zhipu's first natively multimodal GLM-5

GLM-5.3-Flash landed on Hugging Face on 25 August and picked up over a thousand likes within two days. The <a href="https://huggingface.co/zai-org/GLM-5.3-Flash">official card</a> introduces it as the first natively multimodal model in the GLM-5 series, with 320B total and 18B active parameters, "outperform[ing] GLM-5.2 across benchmarks and real-world workloads at one-tenth the price, while approaching Claude Opus 4.8 on coding and agentic benchmarks". For the first time in the GLM series it uses a hybrid architecture combining sparse and linear attention — cutting long-context serving cost while keeping long-context precision — plus Manifold-Constrained Hyper-Connections (mHC) and a 30-trillion-token multimodal pre-training corpus. License is MIT. Those are Zhipu's own claims from the card and the GLM-5 technical report (arXiv:2602.15763), not independent tests.

## The crack: a permanent edit with receipts

dealignai's CRACK brand means no fine-tuning, no LoRA, no adapters, no steering vectors, no runtime hooks — a direct modification baked into the tensors, so stock vLLM serves it with the standard chat template. On this release the edit also extends to the MTP draft head, which has its own fused 512-expert MoE.

The published measurements, all from the editor's card:

- **HarmBench-320, greedy:** Standard 159/159, Contextual 81/81, Copyright 80/80 → 320/320 complied, 0 refusals.
- **Sampling robustness:** the 6 harshest behaviors sampled 5× each at temperature 1.0, top_p 0.95 → 30/30 complied, 0 refusals, 0 soft refusals, 0 garbage. The card explicitly argues this is not a greedy-decoding artifact.
- **Capability:** MMLU-logit over 1,026 questions: 86.74% base → 86.26% cracked, −0.48 points.
- **Speed (TP4, native FP8 on H200):** 163 tok/s decode, 211 tok/s with MTP speculative decoding (75.9% acceptance), ~19,400 tok/s prefill.
- **Vision:** the GLM-4.1V vision tower works, shipping the correct multimodal chat template.

The card also includes a short essay on why KL divergence is not the right quality metric for a refusal ablation: changing refusal end-to-end is supposed to shift the distribution on refusal-adjacent tokens, so KL against the base mostly measures the intended change, not damage. Capability preservation is the metric that matters, and here it is essentially flat.

## The hosting math: what the refusals were costing

The interesting angle of this particular crack is that it is cheap. Removing refusals cost 0.48 MMLU points and nothing on throughput — FP8 is native on Hopper, so the edit runs at the same tensor-core speed as the base. Turning on the cracked MTP head actually makes it ~30% faster (163 → 211 tok/s) while holding ~75.9% draft acceptance on un-refused, benign and copyright prompts alike. In other words, at 320B scale you no longer have to choose between an uncensored model and a fast one.

What it costs to run is a separate question. dealignai measured at TP4 on H200 — four GPUs. Our site-consistent approximate managed estimate for the 320B MoE class is **$10.90/hour** (2 × H200) for a servable deployment, with the full TP4 speed config closer to **$21.80/hour** (4 × H200). The NVFP4 twin (`dealignai/GLM-5.3-Flash-ABLITERATED-NVFP4`, ~165B safetensors) is the cheaper-memory path. There is also an `UNCENSORED-FP8` mirror with identical weights under a different name.

## How to run it

Native FP8 on Hopper, stock vLLM:

```bash
vllm serve dealignai/GLM-5.3-Flash-ABLITERATED-FP8 \
  --tensor-parallel-size 4 \
  --tool-call-parser glm47 --reasoning-parser glm45 --enable-auto-tool-choice \
  --speculative-config '{"method":"mtp","num_speculative_tokens":1}'
```

OpenAI-compatible chat/completions, tools, reasoning and vision (`image_url`) all work, and MTP speculative decoding is on by that flag. The card notes DeepGEMM JIT-compiles a block-FP8 kernel at startup, so keep `nvcc` on `PATH`. Our approximate managed price estimate for the 320B MoE class is **$10.90/hour**; that is what ABLITERATED.cloud would host it for, with the TP4 high-throughput config as the premium option.

## The creator: Zhipu AI, and the editor dealignai

The base is from **Zhipu AI's GLM-5 team** — the card credits "GLM-5-Team" with the <a href="https://arxiv.org/abs/2602.15763">GLM-5 technical report</a> ("from Vibe Coding to Agentic Engineering") and a long author list. Zhipu runs Z.ai as its API platform, and GLM-5.3-Flash is positioned there as the cheap agentic workhorse of the GLM-5 line. The crack comes from **dealignai** (X: @dealignai), the same independent editor behind the Qwen3.8-Flash-Next FP8 build covered in the other field note today — 99 Hugging Face models under the CRACK brand, 1,482 followers, "Open to Work" on their profile, compute on this release credited to X user @jordanschenck. Their profile tagline — "No cheap template tricks, no fine tuning here. Do the hard work of actually understanding." — matches how this card reads.

One honest line: guardrails are removed here, which is the entire point of a CRACK release, and the 320/320 is the editor's own measurement on the editor's disclosed prompt set.

## The idea, in plain words

**Multi-token prediction (MTP): the model guesses its own next token while it writes the current one.** A small extra "draft head" proposes the token that comes after, so on the next step the main model mostly verifies instead of generating from scratch. When ~3 of every 4 drafts are accepted (75.9% here), the model effectively emits two tokens per forward pass — that is why the same 320B model jumps from 163 to 211 tok/s. The draft head is separate from the main weights, which is also why it has to be uncensored separately: dealignai cracked the head too, so the speed-up survives on un-refused prompts.

Primary sources:

- [Exact dealignai model card](https://huggingface.co/dealignai/GLM-5.3-Flash-ABLITERATED-FP8) and [pinned revision](https://huggingface.co/dealignai/GLM-5.3-Flash-ABLITERATED-FP8/tree/68fdc7b6c6ef90c40583f5f9224d402cc8fdf8b7)
- [NVFP4 twin card](https://huggingface.co/dealignai/GLM-5.3-Flash-ABLITERATED-NVFP4)
- [Official Zhipu GLM-5.3-Flash card](https://huggingface.co/zai-org/GLM-5.3-Flash)
- [GLM-5 technical report](https://arxiv.org/abs/2602.15763)
- [GLM-5.3-Flash blog](https://z.ai/blog/glm-5.3-flash)
- [dealignai profile](https://huggingface.co/dealignai)
