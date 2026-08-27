---
title: ABLITERATED.cloud - Intelligence, freed.
description: Private access to exact uncensored and abliterated Hugging Face models through one controlled OpenAI-compatible cloud API.
canonical: https://abliterated.cloud/
---

# ABLITERATED.cloud

Intelligence, freed.

ABLITERATED.cloud is an open-source control plane and private evaluation service for exact pinned Hugging Face model artifacts described upstream as uncensored, decensored or abliterated. Ask more, think for yourself, and know exactly which checkpoint answers.

The model files are free to download from Hugging Face. Managed cloud inference is not free: H200 and L40S GPUs, startup, storage and operations cost money. Models run with vLLM on scale-to-zero Modal GPUs. Client devices do not download model weights.

## Request access

Private-beta access is available through Signal. Mention ABLITERATED.cloud in
your message:

<https://signal.me/#p/+13103408213>

## Latest uncensored releases

The most interesting recent abliterated checkpoints from Hugging Face, each
with an approximate managed price estimate and a source-linked review:

<!-- ABLITERATED-LATEST-RELEASES-MD -->

- [The 180B abliteration race on the model nobody can serve yet](blog/qwen3-8-flash-next-abliterated-race/) (≈ $10.90/h estimate) — HarmBench-320 greedy real-harm compliance 100% (reasoning low) / 99.6% (xhigh) / 97.1% (off), MMLU −2.50pp (publisher measured) — Qwen released Qwen3.8-Flash-Next on 24 August as the experimental preview of the Qwen4 architecture — 180B total parameters, ~6B active, hybrid Gated DeltaNet + micro-block sparse attention + 512-expert MoE + a 51B-parameter n-gram lookup table. Within 48 hours at least five editors raced to abliterate it. dealignai's FP8 build is the served, measured one: 100%/99.6% HarmBench-320 real-harm compliance at greedy decoding, MMLU 86.36→83.86, ~81% MTP draft acceptance. Jiunsong's BF16 edit is the architecture-aware method: 36 storage tensors → 6,168 logical output projections, 842-pair corpus. The catch: released vLLM/SGLang still don't support qwen4_exp.
- [GLM-5.3-Flash, cracked open: 320B total, 18B active, 320/320](blog/glm-5-3-flash-crack/) (≈ $10.90/h estimate) — 320/320 HarmBench behaviors complied, 0 refusals (greedy); 30/30 at temp 1.0/top_p 0.95 (publisher measured) — Zhipu's first natively multimodal GLM-5 (320B total / 18B active, hybrid KDA linear + sparse attention, MIT) landed 25 August. dealignai's CRACK edit removes refusals at the weight level in official FP8: 320/320 HarmBench-320 greedy compliance, 0 refusals, 30/30 at temp 1.0/top_p 0.95, MMLU 86.74→86.26 (−0.48pp), 163→211 tok/s with the cracked MTP head (75.9% acceptance) on 4×H200. NVFP4 twin (~165B) and an UNCENSORED-FP8 mirror with identical weights.
- [The first Nemotron-H abliteration: 3,126 tensors, 0.000160 leakage](blog/darkstar-nemotron-3-5-lightning-30b-a3b-abliterated/) (≈ $5.45/h estimate) — 200/200 harmful compliance, 0/83 safe over-refusals (publisher measured, disclosed marker set, temp 0) — NVIDIA's newest open model is a hybrid — Mamba-2 state-space blocks interleaved with MoE and sparse attention, 30B total / ~3B active, built for agent execution. Two weeks after launch, Darkstar removed the refusal direction from 3,126 residual-writing tensors with a numbered edit contract: max residual leakage 0.000160, 200/200 harmful compliance / 0/83 safe over-refusals publisher-measured, plus a ~22 GB NVFP4 twin that keeps Mamba tensors in BF16 and scores GPQA 71.2% on one GPU.
- [One base, three uncensors: the Ornith-1.5 task-vector transplant](blog/ornith-1-5-35b-a3b-uncensored-transplant/) (≈ $5.45/h estimate) — 0/16 heuristic refusals, 4/4 capability passes (publisher measured, llama.cpp Q4_K_M, disclosed regex screen) — DeepReinforce's self-improving Ornith-1.5-35B-A3B, uncensored three ways in 48 hours: a streamed task-vector transplant that adds Qwen3.6's measured uncensoring delta to Ornith's weights (102 tensors changed, vision and MTP intact, 0/16 heuristic refusals on Q4_K_M), plus two classic orthogonalization edits.
- [The lossless aggressive: Qwen3.8 27B Uncensored FP8](blog/qwen3-8-27b-uncensored-aggressive/) (≈ $5.45/h estimate) — aggressive, fully unlocked (publisher claim); no measured refusal rate published — The most-liked Qwen3.8 uncensored on Hugging Face (553 likes): orcarouter's lossless aggressive edit, block-FP8 with the vision tower at full precision, served gated on OrcaRouter at $0.40/$4.21 per 1M tokens.
- [Small uncensored agents: what a 4.5B Heretic distill is for](blog/qwen3-5-4b-emperoai-qwen3-8-distill-heretic-abliterated/) (≈ $2.34/h estimate) — 6/100 refusals (measured) — A source-linked field note on insraq's Heretic v1.4.0 decensor of EmperoAI's Qwen3.8-4B distill: what the 4.5B class is for, and what it trades away.
- [What 'Aggressive' means: Muse-Glimmer-30B abliterated to 0/100 refusals](blog/muse-glimmer-30b-abliterated-aggressive/) (≈ $5.45/h estimate) — 0/100 refusals (measured, harmful_behaviors) — A relaxed-KL LoRA de-abliteration of Meta's 29.8B agentic model claiming 0/100 refusals at ~1.7x KL drift — a mirror upload with the benchmarks left unmeasured.
- [The 2.78-trillion-parameter abliteration nobody can run](blog/kimi-k3-abliterated-modal/) (≈ $87.20/h estimate) — 98% of safeguard signal attenuated (publisher claim) — An abliterated re-upload of Moonshot's 2.78T-parameter Kimi K3 — any-to-any, MXFP4, 96 shards, ~1.56 TB — with zero downloads and no deployment: the scale math behind why nobody can run it.
- [The first abliterated diffusion LLM: 1,000+ tokens a second on one GPU](blog/diffusiongemma-26b-e38-abliterated-nvfp4/) (≈ $5.45/h estimate) — 0/402 target refusals, 0/249 benign false refusals (publisher measured) — Abliterating a model that doesn't generate autoregressively, then quantizing it to NVFP4: 0/402 target refusals and 1,053.64 tok/s aggregate on one RTX PRO 6000, 51.68 GB cut to 18.86 GB.
- [The 48-hour abliteration race](blog/huihui-qwen3-8-27b-abliterated/) (≈ $5.45/h estimate) — no refusal benchmark published (crude PoC) — Within 48 hours of Qwen3.8-27B's community release, huihui-ai published a 27.8B-parameter abliterated edit that leaves the first 15 layers, MTP and the vision tower untouched, and its GGUF companion landed the same afternoon.
- [Three ARA passes: how RVN got Qwen3.8-27B down to 0–1/100 refusals](blog/qwen3-8-27b-rvn-heretic-abliterated-uncensored/) (≈ $5.45/h estimate) — 0–1/100 refusals (publisher measured, prefix-forced) — Abliteration as a matrix optimization problem, run three times: KL 0.0535 → 0.0085, refusals 3/100 → 0–1/100, 106K downloads in four days, one corrupted quant and a loud community pushback.
- [DeepSeek V4 Flash, uncensored by dial: 757 KB against 284B](blog/huihui-deepseek-v4-flash-0731-abliterated/) (≈ $10.90/h estimate) — 0/10 refusals at lambda 1.5 (measured) — A 757 KB refusal-directions file turns DeepSeek V4 Flash 0731 abliteration into a runtime λ dial, with measured proof that the baked λ=2.5 checkpoint overshoots and inverts the direction.
- [The base of the wave: Muse-Glimmer-30B's measured de-refusal](blog/muse-glimmer-30b-abliterated/) (≈ $5.45/h estimate) — 13/100 refusals (measured, ~87% removed) — jorkle's KL-measured LoRA-SFT de-refusal of Meta's dense 29.8B agentic model — the Normal twin of a three-repo family with its own GGUF ladder and base-reference quants.
- [A pentesting model, with the refusals taken out](blog/huihui-cyberstrike-offsec-35b-abliterated/) (≈ $5.45/h estimate) — no refusal benchmark published (crude PoC) — An abliterated fine-tune of the CyberStrike-OffSec-35B offensive-security model: a Qwen3.6-35B-A3B tool-calling base, refusal weights edited out, no post-edit evaluations published.
- [Qwythos 9B: a model with three lives](blog/qwythos-9b-claude-mythos-5-1m-abliterated/) (≈ $2.34/h estimate) — Qwen architecture, Empero post-training and huihui-ai's final refusal-reduction pass, with a 1M label that deserves a closer look.
- [Inside Huihui-Qwen3.6: 256 experts and one refusal direction](blog/qwen3-6-35b-a3b-abliterated/) (≈ $5.45/h estimate) — The multimodal proof of concept: how huihui-ai applied abliteration to a 36-billion-parameter mixture-of-experts checkpoint, and why uncensored still needs caveats.
- [Ornith 397B: surgery on a model too large to hold at once](blog/ornith-1-0-397b-abliterated-w4a16/) (≈ $10.90/h estimate) — A shard-by-shard abliteration and W4A16 conversion of a 396.8-billion-parameter sparse model that still produces nearly 196 GiB of weights.
- [Ornith 35B: can self-scaffolding survive abliteration?](blog/ornith-1-0-35b-abliterated/) (≈ $5.45/h estimate) — DeepReinforce's coding scaffold, YuYu1015's corrected weights and the boundary between upstream and derivative benchmarks.
- [The workhorse: Huihui-Qwen3.6-27B-abliterated, four months in](blog/huihui-qwen3-6-27b-abliterated/) (≈ $5.45/h estimate) — no refusal benchmark published (crude PoC) — 18,760 downloads in four months: what the community actually runs a dense 27B Qwen abliteration for, from red-teaming to quantization, and what its users report back.
- [The quiet classic: how Huihui-Qwen3.5-9B-abliterated became the small-model default](blog/huihui-qwen3-5-9b-abliterated/) (≈ $2.34/h estimate) — no refusal benchmark published (crude PoC) — Abliterated Qwen3.5-9B (9,653,104,368 params, Apache-2.0) published 9 March 2026: 9,195 downloads and 125 likes on the base, with 58 downstream repos — GGUF/AWQ/MLX conversions and a preference-tuned Grimoire family — holding 64,688 combined downloads.
- [The MIT vision sleeper that resurfaced in August](blog/huihui-glm-4-6v-flash-abliterated/) (≈ $2.34/h estimate) — no refusal benchmark published (text-only edit) — MIT-licensed text-side abliteration of Zhipu's GLM-4.6V-Flash vision model (10,292,777,472 params), published 9 December 2025, dormant for eight months, freshly re-quantized with vision-projector files on 17 August 2026.

<!-- /ABLITERATED-LATEST-RELEASES-MD -->

"abliterated", "decensored" and "uncensored" describe publisher claims about reduced refusal behavior. They do not guarantee zero refusals, correctness, safety, legality or unrestricted capability. The two model cards that publish measurements still report non-zero refusal rates.

## Model field notes

Long-form, source-linked articles trace the architecture, lineage, publishers,
abliteration method, benchmark boundary, and hosting reality of each artifact:

- [Huihui-Qwen3.6 35B A3B](blog/qwen3-6-35b-a3b-abliterated/)
- [YuYu1015 Ornith 1.0 35B](blog/ornith-1-0-35b-abliterated/)
- [Huihui Qwythos 9B Claude Mythos 5](blog/qwythos-9b-claude-mythos-5-1m-abliterated/)
- [cebeuq Ornith 1.0 397B W4A16](blog/ornith-1-0-397b-abliterated-w4a16/)

Every benchmark is attributed either to the upstream publisher or the exact
derivative publisher. No upstream score is presented as an endpoint result.

## How it works

1. An invited user receives a revocable ABLITERATED.cloud Bearer token.
2. The client sends an OpenAI Chat Completions request to one gateway.
3. The gateway validates the token and resolves the exact model ID.
4. Modal starts only the selected private vLLM backend when its lifecycle is armed.
5. The GPU scales to zero after five idle minutes, or the operator hard-stops it immediately.

Five minutes is an idle tail, not a total cost limit. Startup, model loading, inference, retries, and open streams remain billable.

## API compatibility

Directly supported:

- OpenAI Chat Completions request shape
- Bearer authentication
- model listing
- streaming
- structured tool calls
- Hermes Agent
- Pi
- OpenCode
- OpenAI SDKs
- cURL and server-side applications

Cursor is a compatibility target, not a promise of complete feature parity.

## Model prices

- The exact model weight files have no purchase price on Hugging Face.
- Qwen3.6 35B A3B (`huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated`): $5.45/hour.
- Ornith 1.0 35B (`YuYu1015/YuYu1015-Ornith-1.0-35B-abliterated`): $5.45/hour.
- Qwythos 9B Claude Mythos 5 (`huihui-ai/Huihui-Qwythos-9B-Claude-Mythos-5-1M-abliterated`): $2.34/hour.
- Ornith 1.0 397B W4A16 (`cebeuq/Ornith-1.0-397B-abliterated-W4A16`): $10.90/hour.

Automated billing is not live yet. Private-beta access is invitation-based
while customer metering, payments and invoicing remain roadmap work.

## Cloud and security boundary

- Model weights remain in Hugging Face and persistent Modal volumes.
- No model weights are downloaded to the operator's Mac.
- API access requires an ABLITERATED.cloud Bearer token.
- Gateway-to-backend traffic uses separate private Modal proxy credentials.
- Token digests, not recoverable plaintext tokens, are stored in the shared lifecycle state.
- The public landing page never calls, polls, wakes, or embeds the inference API.

## Open source

The control plane, website, configuration, tests, deployment workflow, and documentation are public:

<https://github.com/eminogrande/mn-uncensored>

Our code uses the Apache-2.0 open-source license. Hugging Face currently displays Apache-2.0 metadata for the first three model repositories and MIT for the 397B repository. Each model still retains upstream attribution, warnings and commercial-use caveats; public weights are not automatic resale clearance.

## Development roadmap

The four profiles we host are documented in the public catalog. Newer releases are covered in the Latest uncensored releases section above; expensive hardware profiles require an operator-approved budget and explicit cost acknowledgement before deployment.

Roadmap:

1. Confirm the Modal Workspace hard budget.
2. Validate all four model profiles before production use.
3. Add per-token model permissions, quotas, and rate limits.
4. Add usage metering and customer billing.
5. Complete commercial model-license and provider-term review.
6. Explore Lightning, Cashu, and Routstr payment layers.

## Machine-readable resources

- LLM index: <llms.txt>
- Full LLM context: <llms-full.txt>
- OpenAPI description: <openapi.json>
- Authentication guide: <auth.md>
- Agent skill: <skills/abliterated-cloud/SKILL.md>
- Source repository: <https://github.com/eminogrande/mn-uncensored>
