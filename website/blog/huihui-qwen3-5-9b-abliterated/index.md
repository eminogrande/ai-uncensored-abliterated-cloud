# The quiet classic: how a 9B abliteration became the small-model default<!-- READING-TLDR -->

## TL;DR

- Huihui-Qwen3.5-9B has roughly 19.3 GB of BF16 weights and a vision encoder.
- The Huihui-Qwen3.5-9B article counted 58 downstream repos, including conversions and further fine-tunes.
- Huihui's proof-of-concept card included no post-edit benchmark results.

## Basically, the facts

**Released quietly, reused constantly**

Basically, The Qwen3.5-9B article counted 58 derivative repositories with 64,688 combined downloads.

**A dense 9B with a hybrid spine**

Basically, Huihui-Qwen3.5-9B has a dense 32-layer architecture with a vision encoder.

**A proof of concept, published on purpose**

Basically, Huihui's Qwen3.5-9B card calls the edit a crude proof of concept and supplies no post-edit benchmarks.

**The derivative economy**

Basically, Huihui-Qwen3.5-9B derivatives include format conversions and Grimoire preference fine-tunes.

**Word of mouth, not benchmarks**

Basically, A user said Huihui-Qwen3.5-9B fit an RTX 3060; the article did not specify the quantization.

**The numbers that don't exist**

Basically, Qwen3.5-9B's upstream benchmark results were not rerun on Huihui's abliterated artifact.

**How we treat it**

Basically, The Huihui-Qwen3.5-9B article's $2.34 hourly L40S figure was an estimate, not a live offer.

**The idea, in plain words**

Basically, Quantized model formats package weights for different hardware and runtimes.
<!-- /READING-TLDR -->
<!-- ARTICLE-META-MD -->
_Published 9 March 2026 · Updated 6 September 2026 · 4 min read · Canonical: https://abliterated.cloud/blog/huihui-qwen3-5-9b-abliterated/_
<!-- /ARTICLE-META-MD -->

Published 9 March 2026. Exact artifact: `huihui-ai/Huihui-Qwen3.5-9B-abliterated`, revision `05b9e7c9b978ba29bdb8f50a49c30e4b91183339`.

A dense, multimodal Qwen3.5-9B abliteration: 9,653,104,368 BF16 parameters, about 19.3 GB, 32 layers in a hybrid Gated DeltaNet / Gated Attention layout, vision encoder, 262,144-token native context, Apache-2.0. As of this writing the Hugging Face API shows 9,195 downloads and 125 likes — modest — while 58 derivative repositories built on it hold 64,688 combined downloads. mradermacher's GGUF alone out-downloads the base 3.7 to one.

huihui-ai published it 9 March 2026, weeks after Qwen3.5's February release and after the publisher's own 27B and 35B-A3B abliterations (27 February). The 27B sibling has 161,669 downloads; the 9B is the quiet member of the family that became the default for small hardware. The model card calls the work a crude proof of concept and ships no post-edit benchmarks. Derivatives include GGUF/AWQ/GPTQ/exl3/NVFP4/MLX conversions and nbeerbower's Grimoire preference-tuning family (ORPO, SFT, DPO, KTO, SimPO, TIES), whose cards declare this exact repo as base.

Upstream claims on Qwen's own checkpoint: MMLU-Pro 82.5, GPQA Diamond 81.7, IFEval 91.5, LiveCodeBench v6 65.6, BFCL-V4 66.1, AA-LCR 63.0. Those numbers are not rerun for the abliterated artifact. Community evidence is word of mouth: the first discussion reports it fits an RTX 3060; a later thread discusses extending the recipe to other bases.

## The idea, in plain words

**Why one model becomes 58 repositories** — Same brain, different suitcases. GGUF, Q4_K_M, AWQ, MLX, FP8 — these are compression formats tuned for different hardware: llama.cpp, Apple Silicon, NVIDIA, AMD. Every one of the 58 derivative repos is the same Qwen3.5-9B under a different packing, which is why downloads stack up across the family instead of on the base.

Primary sources:

- [Exact model card](https://huggingface.co/huihui-ai/Huihui-Qwen3.5-9B-abliterated)
- [Pinned artifact](https://huggingface.co/huihui-ai/Huihui-Qwen3.5-9B-abliterated/tree/05b9e7c9b978ba29bdb8f50a49c30e4b91183339)
- [Official upstream Qwen3.5-9B card](https://huggingface.co/Qwen/Qwen3.5-9B)
- [Derivative index via HF search](https://huggingface.co/models?search=Huihui-Qwen3.5-9B-abliterated) and [Grimoire-ORPO base declaration](https://huggingface.co/nbeerbower/Huihui-Qwen3.5-9B-abliterated-Grimoire-ORPO)
- [Discussion: "Perfect size"](https://huggingface.co/huihui-ai/Huihui-Qwen3.5-9B-abliterated/discussions/1) and [Discussion: "Ablirated Model Creation"](https://huggingface.co/huihui-ai/Huihui-Qwen3.5-9B-abliterated/discussions/2)
- [Ollama build](https://ollama.com/huihui_ai/qwen3.5-abliterated:9b)
- [HackerNoon roundup](https://hackernoon.com/huihui-qwen35-9b-abliterated-what-this-uncensored-model-does)
- [Implementation linked by huihui-ai](https://github.com/Sumandora/remove-refusals-with-transformers)
- [Original refusal-direction paper](https://arxiv.org/abs/2406.11717)

The publisher warns that safety filtering is reduced and recommends controlled research use. "Abliterated" means refusal-reduced, not zero-refusal, correct, legal or harmless. Approximate managed price estimate: $2.34/hour (1× L40S).

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Want this model running for you, on a private cloud GPU or your own machine? [Request access on Signal](https://signal.me/#p/+13103408213) or [see how it works](https://abliterated.cloud/#how).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
