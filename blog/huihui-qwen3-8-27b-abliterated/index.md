# The 48-hour abliteration race

Published 16 August 2026. Exact artifact: `huihui-ai/Huihui-Qwen3.8-27B-abliterated`, revision `d42ca8978c5a66e92c3446d46e8adfe03ef692ff`.

Qwen3.8-27B is a dense 27,781,427,952-parameter BF16 model: 64 hybrid layers (three Gated DeltaNet blocks per full-attention block), a 27-layer vision encoder, multi-token prediction, and a 262,144-token native context. The upstream repository appeared 5 August 2026; the quantizations the community could actually download (official FP8, unsloth GGUF and NVFP4) are timestamped 13 August. Huihui-ai published this abliterated edit at 08:22 UTC on 16 August — inside 48 hours of the community's 14–15 August "release" moment — and its GGUF companion with twelve quants, BF16 and a vision projector followed at 13:18 UTC the same day.

The edit's boundaries are documented on the card: the first 15 of 64 layers were retained without ablation, and MTP and the visual encoder were not modified. The card calls the implementation a crude proof of concept built on Sumandora's pure-Transformers refusal-direction removal. No refusal-rate benchmark and no post-edit rerun are published.

Upstream Qwen claims include 73.0 Terminal Bench 2.1, 61.7 SWE-bench Pro, 42.2 DeepSWE 1.1, 79.0 QwenSWEBench, 89.2 GPQA Diamond, 30.8 HLE and 84.3 OSWorld-Verified. Those belong to Qwen's checkpoint, not to the abliterated derivative — Huihui publishes no corresponding measurement.

The variant wave around Qwen3.8-27B passed a hundred repositories within a week (GGUF, NVFP4, MLX, AWQ, AutoRound, FP8, exl3, MTP-tagged builds). For this exact artifact the useful paths are huihui's own GGUF via Ollama (18 GB, 256K context, image support), NVFP4 on Blackwell hardware, MLX on Apple Silicon, and the BF16 repository on a single H200 — which our prepared profile pairs with a conservative 131,072-token context at an approximate managed price estimate of $5.45/hour.

How to run it:

```sh
ollama run huihui_ai/Qwen3.8-abliterated
```

The GGUF companion ships twelve quantizations plus BF16 and an mmproj vision projector for llama.cpp, LM Studio and MLX. vLLM serves the exact Hugging Face repository; the ABLITERATED.cloud endpoint uses the same pinned revision.

## The creator: huihui.ai

Qwen built and trained the base model. The checkpoint itself comes from the operator behind [huihui-ai](https://huggingface.co/huihui-ai) — huihui.ai — whose profile describes work on model ablations with the open-source NLP community and who maintains more than 180 model repositories. One-person-scale, not a lab: PRO user, "Open to Work", and the fastest abliteration pipeline in the open ecosystem — edit public inside 48 hours of the Qwen3.8 weights, GGUF ladder the same afternoon, announced on X. It runs on coffee and donations: updates on [@support_huihui](https://x.com/support_huihui), funding via [Ko-fi](https://ko-fi.com/huihuiai) or Bitcoin `bc1qqnkhuchxw0zqjh2ku3lu4hq45hc6gy84uk70ge`, collected in the [Qwen3.8 abliterated collection](https://huggingface.co/collections/huihui-ai/qwen38-abliterated).

## The idea, in plain words

**Predicting several words at once** — Most models predict one next token, then the next. Qwen3.8 adds multi-token prediction (MTP): it guesses several tokens ahead in one step, which speeds generation and nudges quality up. Its Gated DeltaNet layers are a cheaper form of attention that keeps a compact memory of what came before — part of why the 3.8 generation feels faster for the same size.

Primary sources:

- [Exact model card](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated)
- [Pinned artifact](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated/tree/d42ca8978c5a66e92c3446d46e8adfe03ef692ff)
- [Model discussions](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated/discussions)
- [Huihui GGUF companion](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF)
- [Official upstream Qwen card](https://huggingface.co/Qwen/Qwen3.8-27B)
- [Qwen3.8 release article](https://qwen.ai/blog?id=qwen3.8)
- [Original refusal-direction paper](https://arxiv.org/abs/2406.11717)
- [Implementation linked by huihui-ai](https://github.com/Sumandora/remove-refusals-with-transformers)

The card says safety filtering is significantly reduced — which is the whole point of this one. "Abliterated" means refusal-reduced, and what you do with that is your call.
