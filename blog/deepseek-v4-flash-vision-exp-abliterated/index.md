<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# Eleven hours from DeepSeek drop to uncensor.

*Published 31 August 2026 · Revision-pinned · Primary sources only*

**Model:** [apetersson/DeepSeek-V4-Flash-Vision-Exp-Abliterated](https://huggingface.co/apetersson/DeepSeek-V4-Flash-Vision-Exp-Abliterated) · pinned revision `71e308af…6ddd5c94`
**Base:** [deepseek-ai/DeepSeek-V4-Flash-Vision-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp) (MIT) · 304,646,824,126 params on the base checkpoint (upstream card lists 285B total / 13B active MoE) · 43 layers, 256 experts (6 active), 32-layer vision encoder, DSpark self-draft · 1,048,576-token context · ~202 GB FP8-native (experts FP4) · ≈ $10.90/h managed BF16-class (2 × H200); NVFP4/IQ2 variants run on a single GPU or 128 GB Mac

DeepSeek's first open multimodal model landed at 06:16 UTC on Monday, 31 August 2026, an experimental build whose agent-benchmark scores immediately crowded the commercial frontier. At 17:12 UTC the same day, Andreas Petersson published a rank-1 abliteration of it. Within twenty-four hours two more builders had grafted that same edit onto an NVFP4 quant and a ds4 GGUF recipe, and every one of them pinned the donor's exact revision, so the whole uncensored family re-derives from one forty-character string.

## Eleven hours

The base model is not a rumor spread, it is a release: deepseek-ai/DeepSeek-V4-Flash-Vision-Exp, created 31 August 2026 at 06:16:18 UTC, MIT-licensed, 17,893 downloads and 462 likes inside its first two days. DeepSeek calls it the first experimental multimodal model in the V4 family: the V4-Flash MoE backbone with visual modules bolted on and continued training on top, so the text-only agent behavior that made the 0731 revision a local favorite carries over while multimodal agent scores jump. The [vLLM recipe page](https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp) reads like a hardware flex: 285B total / 13B active, 1,048,576-token context, and 83.5% on OCRBench from a single GB200 NVL4 tray.

The upstream card's own numbers, text and multimodal, line up against the earlier V4-Flash-0731 revision and Opus-4.8 (upstream benchmark claims, straight from the card; † marks where the 0731 revision ignores the multimodal parts of the prompt):

| Benchmark | V4-Flash-Vision-Exp | V4-Flash-0731 | Opus-4.8 |
|---|---|---|---|
| Terminal Bench 2.1 | 83.9 | 82.7 | 85.0 |
| NL2Repo | 57.7 | 54.2 | 69.7 |
| DeepSWE | 59.3 | 54.4 | 58.0 |
| Toolathlon-Verified | 75.9 | 70.3 | 76.2 |
| DSBench-Hard | 63.6 | 59.6 | 71.7 |
| ApexBench (Pass@1) | 36.5 | 26.2 † | 39.4 |
| Agents' Last Exam | 27.3 | 25.2 † | 25.7 |
| ZeroBench (Pass@5) | 35.0 | – | 34.0 |
| Chartography | 64.3 | – | 65.0 |

Then the clock. The abliterated derivative was created at 17:12:13 UTC the same day, ten hours and fifty-six minutes after the base appeared. DeepSeek published on a Monday; the uncensored version existed before most of Europe had dinner. That is the community this site covers: not waiting for a v2, not waiting for an Ollama page, surgery on day zero.

## What the edit actually is

From apetersson's card, quoted exactly: this is a rank-1 abliterated derivative, produced by targeted projection edits, not gradient fine-tuning. One refusal direction, one rank, projected out of the attention output projection tensors, and that is nearly the entire footprint of the change. The target set: the 33 attention output writer tensors in layers 10 through 42, plus their scales. Everything else, the vision encoder, the routers, the shared experts, the MTP head, the embeddings, is left byte-identical to the base.

The practical notes are refreshingly honest for the genre: text and focused image smoke tests pass, and broader quality, safety and production-runtime evaluation is pending. No refusal-rate table, no heroic 0/100 claim. That candor is why there is no zero-refusal badge on this entry.

What makes this release structurally interesting is not just the edit, it is the provenance. The repo is a catalog, not a dump: `Reference-Native-FP8/`, `Reference-Native-GGUF/` (155.98 GB, ~145.26 GiB), and `Basic128-Routed-IQ2_M/` (102.83 GB, ~95.76 GiB, a resident-128-GiB profile). The card walks through the whole conversion: 129 routed-expert and 559 compatible tensors copied byte-for-byte, 338 F32 plain/control tensors downcast to F16, 345 F16 dense projections to Q8_0, and a custom routed-expert recipe (gate/up at IQ2_XXS, down at Q2_K, ten routed layers kept at MXFP4). The original source-preserving receiver, 164.7 GB and incompatible with mainstream runtimes, is no longer published; what remains is what actually runs.

## The descendant pipeline

Here is where the day gets weird in the best way. The abliteration itself is a 33-tensor edit, which means it is portable: anyone serving a quantized copy of this model can graft the edit on instead of re-deriving it. Two people did, within hours, and both published receipts.

[s-zaizen/DeepSeek-V4-Flash-Vision-Exp-Abliterated-NVFP4](https://huggingface.co/s-zaizen/DeepSeek-V4-Flash-Vision-Exp-Abliterated-NVFP4) is an NVFP4 build (NVIDIA Model Optimizer lineage, tagged for DGX Spark) that keeps the NVFP4 routed experts from its own base quant and replaces only the 33 FP8 attention output writers, pulling the payloads from apetersson's pinned native abliterated reference. Its card documents the edit: one rank-1 refusal direction at strength 3.5, each edited output row's L2 norm preserved, three FP8 fixed-point requantization passes, recipe pinned in an `ABLITERATION_BUILD_RECEIPT.json`. Validation is the most rigorous of the three: 48/48 shards structurally matched against the donor, text and vision generation passing exact checks, a safe-boundary suite at 8/8 answered with zero refusals, and GSM8K at 99/100, three points above its own unedited NVFP4 base. That last number is why the edit is worth studying: a refusal-direction removal that measurably improves a math benchmark, because the refusal behavior was costing it correct answers.

[audreyt/DeepSeek-V4-Flash-Vision-Exp-Abliterated-GGUF](https://huggingface.co/audreyt/DeepSeek-V4-Flash-Vision-Exp-Abliterated-GGUF) is the Mac path: an IQ2_XXS language GGUF (86.72 GB, ~80.76 GiB) with the same rank-1 edit baked into those 33 tensors, made by HTTP-Range-fetching the already-quantized Q8_0 payloads straight out of apetersson's Basic128 build and SHA-256-verifying every destination against the pinned source. Its card traces the direction's family tree: the refusal direction itself was transferred from drowzeys's earlier 0731 DSpark abliteration. A smoke test on an M5 Max 128 GB: a 512×507 photo in, 169 image tokens, 285.75 tok/s prefill and 44.94 tok/s generation. A fourth builder, msuiche, shipped its own cyber-flavored Vision-Exp edit the same day. One base, four independent uncensored takes, all within 24 hours, all of them MIT.

## How to run it

There is no Ollama page for this model yet, so pick your path:

**Local Mac, best quality per gigabyte.** The Basic128-Routed-IQ2_M profile was built to be resident in 128 GiB, and the card lists ~23.4 tok/s text on an M1 Ultra at 32K context via antirez's ds4 runtime:

```sh
./ds4-server --model "…/Basic128-Routed-IQ2_M/DeepSeek-V4-Flash-Vision-Exp-Abliterated-Basic128-Routed-IQ2_M.gguf" \
  --vision "…/Basic128-Routed-IQ2_M/mmproj-DeepSeek-V4-Flash-Vision-Exp-F16.gguf" \
  --metal --ctx 32000 --tokens 4000 --prefill-chunk 1024 --host 127.0.0.1 --port 18080
```

**Datacenter, full native quality.** Serve the official base with vLLM (the DeepSeek-recommended image, 4×GB300-class node, DSpark self-draft enabled) or SGLang with `--speculative-algorithm DSPARK`, or point the same stack at the ~202 GB FP8-native abliterated reference and skip the aligned base entirely.

**Hosted.** ABLITERATED.cloud's approximate managed price estimate for the BF16-class model is ≈ $10.90/h on 2 × H200; the NVFP4 and IQ2 variants open a cheaper single-GPU or 128 GB Mac class. Treat the estimate as a managed-hosting ballpark, not a quote.

## The creator: Andreas Petersson

The Hugging Face profile behind the surgery reads simply: Andreas Petersson, 17 followers, and a catalog that tells the real story. He had already done this exact job once. His 0731 abliterations from the start of August are the family jewels: the FP8 abliterated DeepSeek-V4-Flash-0731 at 18,794 downloads, the DS4 GGUF builds at 31,138 and 83,938 downloads. That last one, `DeepSeek-V4-Flash-0731-Abliterated-DS4-Headroom128`, is the model this site's readers already know, the proof he understands both halves of the problem: how to cut the refusal direction out of the weights, and how to package a ~145 GB class model so a 128 GB Mac can actually breathe. When the Vision-Exp base dropped with a whole new vision stack attached, he did not ship a half-tested text-only edit. He shipped the reference-native FP8, a reference GGUF, a routed IQ2 profile, and a detailed map of which tensors were copied, which were downcast, and which were left alone. No socials on the profile, no Ko-fi, no donation address: the work is the brand. The base is DeepSeek-AI's, and the runtime is antirez's ds4, but the eleven-hour turnaround and the immaculate provenance trail are his.

## One honest line

Safety filtering is significantly reduced here, which is the whole point: this is a vision agent that will describe, draw, or act on things the aligned base refused, so you own whatever you do with its output.

## The idea, in plain words

**Rank-1 refusal-direction projection.** Classic abliteration finds the one direction in activation space that a model uses to refuse, then erases it from the weights. This edit goes narrower still: one direction, one rank, projected out of just 33 attention-output tensors spread across layers 10 to 42, with every row's length preserved so the network keeps its shape. Same refusal, much smaller scar, and small enough a scar that other people can transplant it into their own quants, which is exactly what happened here within a day.

*Coverage gaps: Reddit was unreachable from this machine (HTTP 403) and no independent press coverage of the abliteration itself had appeared at writing time. Community signal here comes from the base repo's own discussions: threads on DGX Spark support, MLX quant requests, and DSpark acceptance-rate questions, i.e. the base's popularity is local-first and quant-first. Revisions, cards, and receipts above are the factual sources.*

## Primary sources

- [deepseek-ai/DeepSeek-V4-Flash-Vision-Exp (model card, benchmarks, 31 Aug 2026)](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp)
- [apetersson/DeepSeek-V4-Flash-Vision-Exp-Abliterated (card, catalog layout, provenance)](https://huggingface.co/apetersson/DeepSeek-V4-Flash-Vision-Exp-Abliterated)
- [s-zaizen/DeepSeek-V4-Flash-Vision-Exp-Abliterated-NVFP4 (card, build receipt, validation)](https://huggingface.co/s-zaizen/DeepSeek-V4-Flash-Vision-Exp-Abliterated-NVFP4)
- [audreyt/DeepSeek-V4-Flash-Vision-Exp-Abliterated-GGUF (card, recipe, smoke test)](https://huggingface.co/audreyt/DeepSeek-V4-Flash-Vision-Exp-Abliterated-GGUF)
- [vLLM recipe page for DeepSeek-V4-Flash-Vision-Exp](https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp)
- [HF API: base model facts](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp)
- [HF API: derivative facts (pinned sha 71e308af…6ddd5c94)](https://huggingface.co/api/models/apetersson/DeepSeek-V4-Flash-Vision-Exp-Abliterated)
- [HF discussions on the base repo](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp/discussions?limit=20)
- Creator profiles: [apetersson](https://huggingface.co/apetersson) · [s-zaizen](https://huggingface.co/s-zaizen) · [audreyt](https://huggingface.co/audreyt)
- [antirez/ds4 runtime (referenced by all derivative cards)](https://github.com/antirez/ds4)
