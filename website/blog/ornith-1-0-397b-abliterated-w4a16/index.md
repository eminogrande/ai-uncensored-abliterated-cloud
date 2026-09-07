# Ornith 397B: surgery on a model too large to hold at once<!-- READING-TLDR -->

## TL;DR

- The Ornith 397B W4A16 artifact still occupies about 195.7 GiB across 47 shards.
- cebeuq reported Ornith 397B refusals fell from 30.0% for the reference W4A16 quant to 7.5% after editing on 40 harmful prompts.
- The Ornith 397B article’s two-H200 profile was deployment-disabled, not a live model offer.

## Basically, the facts

**A 397B model that activates about 17B**

Basically, Ornith 397B activates roughly 17B parameters per token, but the quantized artifact still exceeds 195 GiB.

**Why upstream Ornith attracted attention**

Basically, Ornith's upstream 82.4 SWE-bench Verified score was not rerun on the W4A16 derivative.

**W4A16, translated**

Basically, Ornith W4A16 stores selected weights at four bits while keeping activations at 16 bits.

**The shard-by-shard operation**

Basically, Ornith's publisher describes editing and requantizing tensors while streaming the source shards.

**What the publisher actually tested**

Basically, Ornith W4A16's reported checks are publisher smoke tests, not independent benchmarks.

**Who built the derivative?**

Basically, The Ornith W4A16 release explicitly disclaims affiliation with DeepReinforce.

**Why our route remains disabled**

Basically, The Ornith 397B article described a disabled two-H200 deployment profile with a 32K context.

**The idea, in plain words**

Basically, Ornith's four-bit weight storage reduces memory needs without making every tensor four-bit.
<!-- /READING-TLDR -->

Published 18 July 2026. Exact artifact: `cebeuq/Ornith-1.0-397B-abliterated-W4A16`, revision `e5651d291be1c65ff1360eee47ab533ab13b3d97`.

Upstream Ornith contains 396,802,360,816 BF16 parameters, with roughly 17B active per token. The W4A16 derivative still occupies 210.1 GB decimal, or about 195.7 GiB, in 47 shards. Most selected language weights are symmetric four-bit integers while activations, embeddings, routers, gates, norms and the vision tower remain 16-bit.

The publisher describes a streaming pipeline that never materializes the roughly 794 GB BF16 language model. It derives refusal directions from 128 harmful and 128 harmless prompts, streams 122 source shards, projects the direction out of selected residual-writing matrices and immediately requantizes each edited tensor.

On 40 harmful prompts, the publisher reports refusal falling from 30.0% for the reference W4A16 quant to 7.5% after editing. Other reported checks include coding, structured tools, image and video smoke tests, and needle retrieval at about 127K and 252K. These are publisher tests, not independent benchmarks. Upstream Ornith’s 82.4 SWE-bench Verified score was not rerun on this derivative.

The tested deployment uses two 128 GB DGX Spark systems over 200 GbE. Our two-H200 profile remains explicitly deployment-disabled and uses a conservative 32K context.

## The idea, in plain words

**How 4-bit weights make a giant model almost portable** — Quantization shrinks numbers: store each weight at 4 bits instead of 16, and a 397-billion-parameter model drops from ~780 GB of storage to ~196 GB. The 'W4A16' tag means weights live at 4 bits while the math runs at 16-bit precision — enough accuracy to keep the model usable, cheap enough to fit on two H200s instead of a small supercomputer.

Primary sources:

- [Exact model card](https://huggingface.co/cebeuq/Ornith-1.0-397B-abliterated-W4A16)
- [Pinned artifact](https://huggingface.co/cebeuq/Ornith-1.0-397B-abliterated-W4A16/tree/e5651d291be1c65ff1360eee47ab533ab13b3d97)
- [Pinned quantization configuration](https://huggingface.co/cebeuq/Ornith-1.0-397B-abliterated-W4A16/blob/e5651d291be1c65ff1360eee47ab533ab13b3d97/quantization_config.json)
- [Official Ornith article](https://deep-reinforce.com/ornith_1_0.html)
- [Official Qwen architecture card](https://huggingface.co/Qwen/Qwen3.5-397B-A17B)
- [Original refusal-direction paper](https://arxiv.org/abs/2406.11717)
- [Intel AutoRound](https://github.com/intel/auto-round)

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Need help with cloud GPUs, self-hosting or app integration? [Talk on Signal](https://signal.me/#p/+13103408213) or [explore self-hosting](https://abliterated.cloud/#workflow).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
