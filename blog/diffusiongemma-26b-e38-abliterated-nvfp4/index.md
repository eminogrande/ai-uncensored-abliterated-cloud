<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# The first abliterated diffusion LLM: DiffusionGemma-26B E38 NVFP4

Published 16 August 2026. Exact artifact: `Goodoldjam/DiffusionGemma-26B-E38-Abliterated-NVFP4`, revision `2430478f0cc94c27623d3684ad03c7f05e858a7d`.

Every "abliterated" model on the Hub is an autoregressive transformer — until now. Goodoldjam abliterated Google's DiffusionGemma 26B A4B, a model that generates text by denoising 256-token blocks instead of predicting one token at a time, then compressed the result to NVFP4: 51.68 GB down to 18.86 GB, and 1,053.64 tok/s aggregate on a single RTX PRO 6000 Blackwell. Parameters: 25.2B total, 3.8B active through 8 of 128 routed experts plus one shared; encoder-decoder discrete text diffusion, 30 layers, up to 256K context, Apache-2.0. Approximate managed price estimate: ≈ $5.45/h on one H200; the NVFP4 checkpoint fits a 32 GB consumer GPU.

## Why abliterating a diffusion model is a different problem

[DiffusionGemma 26B A4B](https://huggingface.co/google/diffusiongemma-26B-A4B-it) is Google DeepMind's open-weights diffusion LLM. It does not generate autoregressively. An autoregressive model emits one token and feeds it back; DiffusionGemma instead denoises an entire 256-token "canvas" in parallel with a diffusion sampler — iterative refinement from noise to coherent text — then appends the finished canvas to the context via its encoder and starts the next one. Google's headline claim is 1,000+ generation tok/s on an H100 (FP8) and 700+ on an RTX 5090. The official card reports 2,069,942 downloads and 1,177 likes on the base since 9 June 2026.

Abliterating that is not a drop-in job. The heretic/ARA toolchain was built around autoregressive layers, and refusal behavior in a diffusion LLM lives partly in the encoder (which caches the prompt) and partly in how the decoder denoises. Goodoldjam's E38 release (BF16, 15 August) describes a "deeply tested middle-layer abliteration" — 20 modified tensors, later preserved in exact BF16 inside the NVFP4 quant. The E38 name refers to the abliteration recipe, not a parameter count. There is no published specification of exactly which layers the pass rewrites or how refusal was targeted in a denoising decoder — the card gives measurements, not a full recipe.

## The NVFP4 quant is the actual story

The BF16 checkpoint is the frozen reference; the release people should run is the [NVFP4 derivative](https://huggingface.co/Goodoldjam/DiffusionGemma-26B-E38-Abliterated-NVFP4). NVIDIA's FP4 format packs two values per byte, and NVFP4 specifically is the quantization scheme designed for Blackwell's fifth-generation Tensor Cores — the same 4-bit path that vLLM's NVFP4 MoE kernels target. Here it cuts the checkpoint from 51.68 GB to 18.86 GB, and 18.86 GB is small enough to fit inside a 32 GB RTX 5090 with room left for KV cache and CUDA graphs. That single fact changes who can run this model: from workstation-class 96 GB hardware down to a consumer card.

The publisher's throughput table, all on one RTX PRO 6000 Blackwell Workstation Edition (96 GB GDDR7, 1.792 TB/s bandwidth, CUDA 13/SM120): 660.44 tok/s at the 48-step quality operating point, 827.28 tok/s single-stream at 16 steps, and 1,053.64 tok/s aggregate at concurrency 8 — with compiled vLLM execution, CUDA graphs, and FlashInfer CUTLASS NVFP4 MoE kernels. The same card publishes the honest comparison: eager execution on the same checkpoint and quality target ran 276.74 tok/s; compiled graphs raised it to 636.46 tok/s, a 2.30× gain, with mean latency down from 1.574 s to 0.690 s.

**Read the step-count asterisk.** Google's 1,008 gen tok/s H100 figure uses 16 maximum denoising steps, a 1024-token canvas, concurrency 1 and ignore-eos on 100 synthetic prompts — a performance benchmark, not a quality measurement. Goodoldjam's E38 quality configuration allows up to 48 denoising steps per 256-token canvas (t_max 0.80, t_min 0.40, entropy bound 0.1, adaptive stopping), chosen after a 2,400-generation study. Adaptive stopping means the 48-step budget is a ceiling, not a per-canvas cost, but the two configs have fundamentally different refinement budgets. The 1,053.64 tok/s aggregate number also runs at 16 steps. "A thousand tokens a second" is real and it is a serving-throughput number at a specific operating point — quality-max is 660 tok/s.

## The measurements on refusal

The publisher's aligned evaluation reports 0/402 target refusals and 0/249 benign false refusals, plus 20/20 multimodal and 24/24 matched multi-turn generations, and 137/200 direct aligned NVFP4-objective validation against the BF16 reference. These are publisher measurements on the publisher's own prompt sets — no independent third-party rerun is published, and the repo has no open discussions yet. Claim: measured zero on the publisher's set. Boundary: same as always — a measured set, not a universal guarantee.

## The creator: Goodoldjam (Atom)

The publisher behind both repos is the Hugging Face user [Goodoldjam](https://huggingface.co/Goodoldjam) — a PRO account, no organization page, and exactly two model repos: the BF16 E38 abliteration and this NVFP4 derivative. The project is funded through [Ko-fi](https://ko-fi.com/goodoldjam), and the card is explicit about what the money buys: GPU compute, throughput optimization, larger validation runs, "diffusion-trajectory analysis", and the next research phase — a mixed-precision quant search. His stated framing: "The expensive part is not making another quant. The expensive part is proving which quant is actually worth releasing." That is a hosting-research workflow, not a one-off edit, and it shows in the evaluation tables.

## The RTX 5090 question

The card ends with a target, not a claim: the RTX 5090 shares the RTX PRO 6000's 1.792 TB/s memory bandwidth and Blackwell FP4 Tensor Cores, and the 18.86 GB checkpoint fits its 32 GB VRAM — so "1,000+ tok/s on a 5090" is described as a plausible experimental target, explicitly not yet validated on this checkpoint. Anyone with a 5090 is implicitly invited to test it.

## How to run it

No Ollama page exists — diffusion LLMs are not in Ollama's runtime — so the path is vLLM with the compiled NVFP4 kernels the card targets, on a Blackwell GPU:

```sh
vllm serve Goodoldjam/DiffusionGemma-26B-E38-Abliterated-NVFP4 \
  --quantization nvfp4 --max-model-len 32768
```

ABLITERATED.cloud's approximate managed price estimate for the 26B-class MoE (3.8B active) is **≈ $5.45/h** on one H200; the NVFP4 checkpoint at 18.86 GB opens a cheaper single-consumer-GPU path.

## How we treat it

This is the strongest refusal claim in our catalogue so far: a measured 0/402 target and 0/249 benign on the publisher's aligned sets, at a real operating point, with the evaluation methodology stated. It still is a publisher claim — independent reruns do not exist yet. The quant work is independently inspectable: NVFP4, 20 abliteration-modified tensors preserved in exact BF16, sizes and throughputs published. One honest line: this output is refusal-reduced by design — 0/402 measured on the publisher's set, a number you can check, not a universal guarantee.

## The idea, in plain words

**Writing by denoising: 256 tokens at once, instead of one at a time** — Autoregressive models are stuck reading what they just wrote: one token per step. DiffusionGemma instead starts with a block of noisy tokens and refines the whole block toward coherent text over many denoising steps, then moves to the next block. Parallel refinement is why a diffusion LLM can push a thousand tokens per second: it spends compute on whole blocks, not single tokens. Abliteration on top of that means removing refusal behavior from a model whose answers are denoised rather than typed out.

Primary sources:

- [Exact model card (NVFP4)](https://huggingface.co/Goodoldjam/DiffusionGemma-26B-E38-Abliterated-NVFP4)
- [Pinned artifact](https://huggingface.co/Goodoldjam/DiffusionGemma-26B-E38-Abliterated-NVFP4/tree/2430478f0cc94c27623d3684ad03c7f05e858a7d)
- [E38 BF16 reference card](https://huggingface.co/Goodoldjam/DiffusionGemma-26B-E38-Abliterated-BF16)
- [Official Google DiffusionGemma card](https://huggingface.co/google/diffusiongemma-26B-A4B-it)
- [Google launch blog](https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation/)
- [Hugging Face model API](https://huggingface.co/api/models/Goodoldjam/DiffusionGemma-26B-E38-Abliterated-NVFP4)
- [Project funding page](https://ko-fi.com/goodoldjam)
