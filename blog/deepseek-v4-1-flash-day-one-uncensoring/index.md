# DeepSeek-V4.1-Flash, uncensored within a day<!-- READING-TLDR -->

## TL;DR

- DeepSeek released V4.1-Flash on 10 September 2026: a 552-billion-parameter backbone, a one-million-token context, MIT license.
- The first uncensored build, s-zaizen's Heretic edit, appeared 8 hours and 41 minutes after the base repository.
- dealignai's weight-level edit reports all 320 HarmBench prompts answered, versus 137 of 320 for the stock model (publisher-measured).
- No released mainstream runtime serves the architecture yet; the working paths are preview branches and community forks.

## Basically, the facts

**What DeepSeek-V4.1-Flash is**

Basically, DeepSeek released V4.1-Flash on 10 September 2026: a 552-billion-parameter backbone, a million-token context.

**The first edit: 97 of 100 to 24**

Basically, s-zaizen's Heretic edit cut DeepSeek V4.1-Flash refusals from 97 to 24 out of 100 measured prompts.

**The weightless route: 800 KB, no weights touched**

Basically, msuiche's 800 KB vector raised compliance on 32 cyber prompts from 5 to 31, with no weight changes.

**The alpha ladder: 0.5 works, 2.0 backfires**

Basically, Doubling msuiche's steering strength to 1.0 slipped Chinese words into English answers; at 2.0 refusals returned.

**The weight-level crack: 137 of 320 to 320**

Basically, dealignai's weight-level edit measured all 320 HarmBench prompts answered, up from 137 for the stock model.

**The day-one shrink wave**

Basically, Day-one shrink work took V4.1-Flash from 510 GB to 169.92 GB at best, still needing datacenter-class hardware.

**What actually serves it**

Basically, No released mainstream runtime serves V4.1-Flash yet; preview branches and community forks do.

**The editors**

Basically, s-zaizen, msuiche and dealignai all had prior releases this site covered in August.

**The idea, in plain words**

Basically, Uncensoring can edit the weights or subtract a refusal direction at runtime; V4.1-Flash got both on day one.
<!-- /READING-TLDR -->
<!-- ARTICLE-META-MD -->
_Published 11 September 2026 · 13 min read · Canonical: https://abliterated.cloud/blog/deepseek-v4-1-flash-day-one-uncensoring/_
<!-- /ARTICLE-META-MD -->

*Published 11 September 2026 · Revision-pinned · Primary sources only*

**Model:** [dealignai/DeepSeek-V4.1-Flash-UNCENSORED-FP8](https://huggingface.co/dealignai/DeepSeek-V4.1-Flash-UNCENSORED-FP8) · pinned revision `86392f73…1a60a99a` (created 10 September 2026, 21:02 UTC) · same-day siblings: [s-zaizen/DeepSeek-V4.1-Flash-Abliterated](https://huggingface.co/s-zaizen/DeepSeek-V4.1-Flash-Abliterated) (`23da584e…c9bb0ad6`, 10:59 UTC) and [msuiche/DeepSeek-V4.1-Flash-abliterated-cyber-GLP-39-L1-39-a0.5](https://huggingface.co/msuiche/DeepSeek-V4.1-Flash-abliterated-cyber-GLP-39-L1-39-a0.5) (`3a278522…c4eac71f`, 13:47 UTC, gated behind a use agreement)
**Base:** [deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) (MIT, 10 September 2026) · 552 billion backbone parameters, 8 billion active per token in prefill and 16 billion in decode · 48-shard checkpoint of about 510 GB, native FP8 with FP4 experts · one-million-token context · no dated rental quote in this article

DeepSeek released V4.1-Flash on 10 September 2026 at 02:17 UTC, and the uncensoring community did not wait for anyone to make it servable. Eight hours and 41 minutes after the repository appeared, s-zaizen published the first abliterated conversion of the checkpoint. Eleven and a half hours in, msuiche shipped something stranger: a control vector under one megabyte that removes refusals at runtime without touching a single weight. Eighteen hours and 44 minutes in, dealignai published a weight-level edit whose card reports compliance on every HarmBench prompt it tested. Three teams, three methods, one checkpoint of roughly 510 gigabytes, all inside one day, and none of it runnable on stable released software yet.

## What DeepSeek-V4.1-Flash is

The model card titles the release "Pushing the Limits of KV Cache Compression", and that is the honest headline: 552 billion backbone parameters in a mixture-of-experts design that activates 8 billion per token during prefill and 16 billion during decode, a one-million-token context, and a redesigned attention stack. The causal encoder-decoder layout runs 20 encoder layers and then 20 decoder layers, projecting the decoder's global KV cache from the encoder's final hidden states instead of each layer's own, and compressed sparse attention keeps that cache at roughly 890 bytes per token, about a quarter of what DeepSeek-V4-Flash needs. Two Engram tables, sized at 196 billion parameters in the card, work as a hashed n-gram lookup with a DSpark draft head built in for speculative decoding, and the DeepSeek-ViT vision tower makes it multimodal. The whole thing is MIT-licensed.

Pre-training ran 45 trillion tokens with sparse attention at 64K sequence length and the context extended to one million tokens, and there is no Jinja chat template: DeepSeek published a reference `encoding.py` plus a separate Rust toolkit, `deepseek-recipe`. The card's benchmark table lists Terminal-Bench 2.1 at 90.6, Codeforces at 3471, DeepSWE v1.1 at 74.2 and MMLU-Pro at 74.1, with a note that scores within 0.3 of each other count as equivalent; those are vendor results from an internal framework, not independent reproductions. The checkpoint measures about 510 GB across 48 shards of FP8 weights with FP4 experts. Within its first day the base repository collected 1,516 likes, and at research time it stood at main revision `dba1be0a…60a90277`.

## The first edit: 97 of 100 to 24

The first uncensored artifact was not the loudest. s-zaizen, a converter who has worked the DeepSeek V4 line since late August, abliterated the base with [Heretic](https://github.com/p-e-w/heretic) at commit `3521f864…35fac7e6`, through a native V4.1 compatibility adapter built on Heretic's residual-direction construction. The selected `per_all_4p5` intervention applies projected per-layer directions to all 40 attention output projections with full row normalization and a rank-3 norm-preserving LoRA merge, and it leaves the expert, Engram, vision, embedding and MTP tensors untouched. The release keeps the source formats across 48 safetensors shards totaling 510.297 GB.

Heretic's own keyword screen, run over 100 examples from the standard `mlabonne/harmful_behaviors` test split with a 100-token response cap, batch size 4, temperature 0, chat thinking mode and seed 42, counted 97 refusals for the stock model and 24 after the edit. The card states plainly that this is not a general capability benchmark, and the number is not zero. That contrast is the useful part: the day's loudest claim is 320 of 320, but the first published refusal count for an uncensored V4.1-Flash is 24 of 100, stated on the card without decoration, and the prompts and settings are named.

## The weightless route: 800 KB, no weights touched

The second artifact is the one that only makes sense on a model too big to edit twice. msuiche's release is a control vector, and its gating note says so in one line: "This is not a model. It is an 800 KB control vector that removes safety refusals from `deepseek-ai/DeepSeek-V4.1-Flash` at inference time." The file holds 39 direction vectors, one per layer for layers 1 through 39, each a unit-norm 5120-dimensional row in fp32, applied at the post-layer residual stream by projecting the activation onto the direction and subtracting it, scaled by alpha, with alpha 0.5 baked in. No weights are modified; this is the difference, not the model. The card pins its calibration to base revision `fb2764a5…f477c16d`, the commit that stood six hours after the repository appeared, and says other revisions and quants are not validated.

The vector is the newest entry in msuiche's GLP series, which has shipped the same runtime treatment to a dozen models since August, from Kimi K3 to GLM-5.3, including the Qwen3.8-Flash-Next build noted in this site's [abliteration-race coverage](https://abliterated.cloud/blog/qwen3-8-flash-next-abliterated-race/) and a DeepSeek-V4-Flash-0731 vector related to the [refusal-direction dial covered here on 13 August](https://abliterated.cloud/blog/huihui-deepseek-v4-flash-0731-abliterated/). The file sits behind a responsible-use agreement on Hugging Face.

The validation numbers are small-n and the card says so. On a 32-prompt refusal screen, compliance rose from 4 of 32 stock to 24 of 32 at alpha 0.5. On a 32-prompt offensive-security screen, it rose from 5 to 31. On a 32-prompt benign holdout, the steered model answered 31, where the single flagged item is described as a classifier false positive verified by reading the completion. An alpha 0.0 arm reproduced the stock labels exactly on both gate suites, which is the no-op check that makes the rest credible. The card's own resolution note: with n=32 per arm, read the rates as approximate.

## The alpha ladder: 0.5 works, 2.0 backfires

The most useful part of the card is the negative space. The strength ladder is not monotone. Alpha 0.5 delivers 24 of 32 with zero measurable collateral. Alpha 1.0 delivers 25 of 32 but slips Chinese phrases into 2 to 7 of 32 English answers. Alpha 2.0 regresses, dropping back to 19 of 32 with code-switching on 13 to 21 of 32 items. The mean dose at alpha 1 runs from 3 percent of the residual norm at layer 1 to 41 percent at layer 30, and the card's warning follows from the measurements: do not port this 0.5 anywhere else, and re-run the ladder for every model, because the curve is sharply non-monotone.

The application point is just as specific. The file is projective-only, meant for a reader that applies it at the post-layer residual stream, and the card says a reader that applies only the older V4-0731 hook must refuse the file. That discipline is the difference between a vector and a party trick. And the serving footnote is the quiet bombshell for the whole day: "No released vLLM loads `deepseek_v41` today", so even 800 KB assumes a source build of an unmerged pull request.

## The weight-level crack: 137 of 320 to 320

The third artifact is the one this site has seen twice before: a CRACK-brand weight-level edit by [dealignai](https://huggingface.co/dealignai), drop-in, with no runtime hooks and no steering vectors, because the refusal circuitry is projected out of the tensors themselves. This time the headline number is total. On HarmBench-320, graded by the publisher's four-tier classifier (HARD_REF, SOFT_RED, HEDGE, COMPLY) with an LLM judge over the reasoning trace at maximum effort, the stock model complies with 137 of 320 prompts at reasoning off (42.81 percent) and just 5 of 320 at maximum effort (1.56 percent), because thinking surfaces safety concerns before answering. The cracked build measures 320 of 320 at both settings; all seven HarmBench categories reach 100 percent; and the card claims zero HARD_REF, zero SOFT_RED and zero HEDGE outcomes. Those are publisher gradings of the publisher's runs.

Capability retention is where the card gets careful. On MMLU-14k, the full test set at temperature 0, accuracy drops from 86.96 percent to 82.74 percent, minus 4.22 points. Excluding the ethics cluster, where refusal-adjacent behaviour is graded, the delta is minus 1.1 points, inside the card's own 3-point knowledge-preservation target. The full per-subject table, published in the card, shows where the rest went: moral scenarios falls 39.89 points, by far the largest single drop, with professional law down 7.04 and abstract algebra down 6. A model whose ethics answers move that much is doing something structural, and the card does not hide it.

The extended validation list covers a 1000-token coherence stress without loops, a four-turn conversation on a harmful topic with no late-turn reversion, a vision-path check, and a compatibility suite spanning streaming, logprobs, tool calls, image input, reasoning-effort tiers and a 40k-word prompt. The build is 48 shards at 510.31 GB, ablated on 10 September, and it carried 9 likes at research time.

## The day-one shrink wave

None of that changes the physics: the checkpoint is 510 GB, and the same day the uncensored builds landed, the packagers started the only fight that matters for actually using it. LibertAIDAI's NVFP4 conversion is the most instructive: 475.2 GiB down to 399.9 GiB, minus 15.8 percent, with the routed experts transcoded to NVFP4 bit-exactly and the two Engram tables moved from FP8 to FP4. The card is upfront that the usual NVFP4 shrink of around 70 percent does not exist for this model, because most of its weight is not in the experts, and the residue is the real story: everything except the two Engram tables is 302.3 GiB and must be resident, so two 120 GB unified-memory machines cannot hold it. s-zaizen's own NVFP4 conversion of V4.1-Flash landed at 491.1 GiB, larger than the original, because the expert transcode grows the files.

A GGUF pack by apetersson squeezes the routed experts to 2.25 bits per weight, 169.92 GB across five shards with SHA256SUMS, but it ships without the Engram tables, which stay at 202.75 GB in the source checkpoint and must be attached from it; the working shapes are a single B200 180 GB or B300 288 GB card plus host memory, or four RTX PRO 6000 cards. pipenetwork's MLX build for Apple Silicon lands at 427.6 GB and ships with its own port repository, because `deepseek_v41` exists in no runtime at all, not even transformers or mlx-lm; 512 GB of unified memory is called tight. rapid-mlx's REAP 2-bit experiment fits a 256 GiB Mac at about 199 GiB and labels itself an experimental research artifact, not a product. A vcruz305 GGUF ladder promising Q2_K_M through Q5_K_M collected 18 likes while the repository was still empty of weights. And the mirrors began: by the next morning, an account called Solstice-AI had republished dealignai's checkpoint under a new repository with the same card text.

## What actually serves it

The state of the serving stack, all of it from the builders' own notes. SGLang: a preview branch, `dsv4.1` (pull request 38798), is the one stack dealignai validated the crack on, including a Docker image tagged `dev-dsv41`; the reference run is four H200s in tensor parallel with the Engram host table enabled, which moves about 203 GB of lookup tables into system memory and leaves 76 GB of weights per GPU, at the cost of roughly 200 GB of host RAM. Cold start is about 28 minutes, single-stream decode about 101 tokens per second, 126 aggregate across eight concurrent streams. vLLM: the model definitions merged to main, but the registry still has no DeepseekV41 entry, so no released build serves it; msuiche's lane runs on an unmerged branch built from source. llama.cpp: cannot load any V4.1 file yet, because the relevant pull request is converter-only. MLX: community ports only. DGX Spark: a four-node community recipe wrapped around a vLLM fork serves it today with the Engram tables on NVMe, and bot-lab-21's 3.5-bit EXL3 expert pack, finished this morning, targets exactly that line, freeing about 15 GB of KV space per node.

This site does not serve V4.1-Flash, and no dated rental quote appears in this article. The documented path is a single stopped A100 40 GB reference box from the 5 September snapshot, and no published reduction of this checkpoint fits that class; the four-GPU runs above are their authors' validation runs, not offers. The honest positioning for now: nothing about this model is self-hosting territory on a normal budget.

## The editors

All three day-one releases come from independent editors, and all three have history here. s-zaizen works the DeepSeek V4 line specifically; this site's [coverage of the V4-Flash-Vision-Exp abliteration](https://abliterated.cloud/blog/deepseek-v4-flash-vision-exp-abliterated/) noted his NVFP4 graft the same day. msuiche's GLP series since August spans Kimi K3, GLM-5.3, Qwen3.8-27B and more, always as gated, tightly calibrated runtime vectors; the card is signed Matt Suiche. dealignai is the CRACK brand this site covered for [Qwen3.8-Flash-Next](https://abliterated.cloud/blog/qwen3-8-flash-next-abliterated-race/) in August and [GLM-5.3](https://abliterated.cloud/blog/glm-5-3-flash-crack/) before that, a catalog of at least 100 repositories at fetch time with one steady promise: permanent weight-level removal rather than runtime tricks. This week they shipped both flavors at once, and the ABLITERATED-FP8 sibling repo is now just a pointer to the UNCENSORED-FP8 one. What is new is the base: an official DeepSeek release, uncensored three independent ways within a day.

## One honest line

Every refusal number in this article is a publisher's own measurement on a screen of a few dozen or a few hundred prompts, the checkpoint takes four datacenter GPUs to load, and the guardrails these edits remove were real; whatever you run it for is on you.

## The idea, in plain words

**Two ways to take a refusal out.** Refusal lives in a direction of a model's internal activations, and there are two ways to remove it: bake the subtraction into the weights, which is permanent and works in any runtime that loads the model, or subtract the direction during inference with a scaled projection, which keeps the checkpoint stock and is reversible but tied to one exact revision, one hook point and one carefully calibrated strength. On small models either route is routine. On a 552-billion-parameter checkpoint the interesting part is that both arrived on day one, because the runtime vector is the only version of this surgery that does not require shipping 510 GB of edited weights.

*Coverage gaps: this article is built from Hugging Face model cards, repository files, file trees and the Hugging Face API, fetched 11 September 2026. All refusal counts and benchmarks are publisher-reported; none were independently reproduced, no GPU was rented and no inference was run for this article. Download and like counts are community signal, not measurement. Serving recipes above are their authors' published validation runs, not offers, and no dated rental quote is claimed.*

## Primary sources

- [dealignai/DeepSeek-V4.1-Flash-UNCENSORED-FP8 (card: HarmBench-320 2x2, MMLU per-subject table, SGLang recipe, hardware notes)](https://huggingface.co/dealignai/DeepSeek-V4.1-Flash-UNCENSORED-FP8) · [pinned revision `86392f73…1a60a99a`](https://huggingface.co/dealignai/DeepSeek-V4.1-Flash-UNCENSORED-FP8/tree/86392f733ccdb50fd6bbc0ffe95cff401a60a99a) · [ABLITERATED-FP8 pointer repo](https://huggingface.co/dealignai/DeepSeek-V4.1-Flash-ABLITERATED-FP8)
- [s-zaizen/DeepSeek-V4.1-Flash-Abliterated (card: Heretic commit, 97/100 to 24/100, untouched component list)](https://huggingface.co/s-zaizen/DeepSeek-V4.1-Flash-Abliterated) · [pinned revision `23da584e…c9bb0ad6`](https://huggingface.co/s-zaizen/DeepSeek-V4.1-Flash-Abliterated/tree/23da584e06e57ec43c896d286b44b822c9bb0ad6)
- [msuiche/DeepSeek-V4.1-Flash-abliterated-cyber-GLP-39-L1-39-a0.5 (card: alpha ladder, validation suites, hook spec, serving shape)](https://huggingface.co/msuiche/DeepSeek-V4.1-Flash-abliterated-cyber-GLP-39-L1-39-a0.5) · [pinned revision `3a278522…c4eac71f`](https://huggingface.co/msuiche/DeepSeek-V4.1-Flash-abliterated-cyber-GLP-39-L1-39-a0.5/tree/3a278522b127db0645c67e6327a41776c4eac71f)
- [deepseek-ai/DeepSeek-V4.1-Flash (official card: architecture, benchmarks, license, 10 Sep 2026)](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) · [pinned revision `dba1be0a…60a90277`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/tree/dba1be0a40aa45a94ad051997016db3960a90277) · [base revision used by the vector `fb2764a5…f477c16d`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/tree/fb2764a5cf321eaa5070ca8f9e892818f477c16d)
- Quantization and serving builds: [LibertAIDAI NVFP4](https://huggingface.co/LibertAIDAI/DeepSeek-V4.1-Flash-NVFP4) · [apetersson mixed-Q2 GGUF](https://huggingface.co/apetersson/DeepSeek-V4.1-Flash-MixedQ2-GGUF) · [pipenetwork MLX](https://huggingface.co/pipenetwork/DeepSeek-V4.1-Flash-MLX-mixed-4_8bit) · [MLX port repository](https://github.com/PipeNetwork/deepseek-v41-mlx) · [rapid-mlx REAP 2-bit](https://huggingface.co/rapid-mlx/DeepSeek-V4.1-Flash-REAP-2bit-MLX) · [bot-lab-21 EXL3](https://huggingface.co/bot-lab-21/DeepSeek-V4.1-Flash-EXL3-3.5bpw-Pollard) · [tonyd2wild DGX Spark recipe](https://github.com/tonyd2wild/DeepSeek-V4.1-Flash-vLLM-DGX-Spark) · [vcruz305 GGUF ladder](https://huggingface.co/vcruz305/DeepSeek-V4.1-Flash-GGUF) · [s-zaizen NVFP4](https://huggingface.co/s-zaizen/DeepSeek-V4.1-Flash-NVFP4)
- Serving stack references: [SGLang pull request 38798](https://github.com/sgl-project/sglang/pull/38798) · [vLLM pull request 56201 (steering lane)](https://github.com/vllm-project/vllm/pull/56201) · [vLLM pull request 56214](https://github.com/vllm-project/vllm/pull/56214) · [vLLM pull request 56228](https://github.com/vllm-project/vllm/pull/56228)
- [Heretic tool (AGPL-3.0) and the conversion commit](https://github.com/p-e-w/heretic/tree/3521f8648a0dccf6e12a92666862632235fac7e6) · [msuiche profile](https://huggingface.co/msuiche) · [s-zaizen profile](https://huggingface.co/s-zaizen) · [dealignai profile](https://huggingface.co/dealignai)
- Prior coverage: [the refusal-direction dial for V4-Flash-0731, 13 Aug 2026](https://abliterated.cloud/blog/huihui-deepseek-v4-flash-0731-abliterated/) · [the Qwen3.8-Flash-Next abliteration race, 27 Aug 2026](https://abliterated.cloud/blog/qwen3-8-flash-next-abliterated-race/) · [the GLM-5.3-Flash crack, 26 Aug 2026](https://abliterated.cloud/blog/glm-5-3-flash-crack/) · [the V4-Flash-Vision-Exp abliteration, 31 Aug 2026](https://abliterated.cloud/blog/deepseek-v4-flash-vision-exp-abliterated/)
- HF API facts: [dealignai derivative](https://huggingface.co/api/models/dealignai/DeepSeek-V4.1-Flash-UNCENSORED-FP8) · [s-zaizen derivative](https://huggingface.co/api/models/s-zaizen/DeepSeek-V4.1-Flash-Abliterated) · [msuiche vector](https://huggingface.co/api/models/msuiche/DeepSeek-V4.1-Flash-abliterated-cyber-GLP-39-L1-39-a0.5) · [upstream](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4.1-Flash)

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Want this model running for you, on a private cloud GPU or your own machine? [Request access on Signal](https://signal.me/#p/+13103408213) or [see how it works](https://abliterated.cloud/#how).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
