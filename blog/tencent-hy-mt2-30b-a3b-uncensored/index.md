# Why would a translation model refuse? Tencent's Hy-MT2, decensored

Published 30 August 2026. Exact artifact: `0xSojalSec/Tencent-Hy-30B-A3B-uncensored-heretic`, revision `abe0aae382c7abce58b4be4eda48953af034025b`.

Tencent's Hy-MT2-30B-A3B is a dedicated machine-translation model: 30 billion stored parameters, about three billion active per token across 128 experts, built to translate between 33 languages. It is a specialist, not a chatbot. And Tencent aligned it so thoroughly that a keyword screen triggered a refusal on all 100 test prompts — the base would rather refuse than render some text. On 30 August 2026, an independent editor published a decensored build that measures 0/100 on the same screen, at KL divergence 0.0276 from the original.

## A translator that refuses is a broken translator

The whole point of Hy-MT2 is speed and fidelity on real translation jobs: Tencent's card and the [Hy-MT2 report](https://arxiv.org/abs/2605.22064) claim the 7B and 30B-A3B sizes beat DeepSeek-V4-Pro and Kimi K2.6 in fast-thinking translation mode, with the 1.8B beating Microsoft and Doubao's commercial APIs overall. Tencent also open-sourced IFMTBench for instruction-following translation and partnered with WMT26 on the video subtitle task. It is a serious production tool.

A translation model with a refusal gate is a tool that randomly stops working: you feed it a paragraph, it returns a lecture instead of the target language. Most uncensored models we cover are general chat or coding models where refusal is one behavior among many. Here refusal was bolted onto a narrow specialist — which is exactly why the edit is worth a closer look.

## What the edit actually does

The card describes a Heretic v1.4.0+custom run using the **Arbitrary-Rank Ablation (ARA)** method: instead of the classic "estimate one refusal direction and project it out of the weights" orthogonalization, this run fits a LoRA adapter that counteracts the refusal direction while preserving row norms, between layers 18 and 28. The published parameters: preserve-good-behavior weight 1.0000, steer-bad-behavior weight 0.1441, overcorrect relative weight 2.2030, neighbor count 1, optimizer `ot_ridge` with ridge regularization 0.0003.

The result, publisher-measured on a custom mixed-language evaluation set (Japanese-language datasets used only to measure KL divergence and refusal rate):

| Metric | This model | Original |
| :----- | :--------: | :------: |
| Refusal keywords | 0/100 | 100/100 |
| KL divergence | 0.0276 | 0 (by definition) |

KL 0.0276 is genuinely low — meaning the edit stays unusually close to the base's distribution while removing the refusal screen. That is a publisher-measured number on the editor's own evaluation set; no third party has re-run it and the exact prompt set is not published.

## How to run it

There is no Ollama page for this model family yet, so the direct path is vLLM with the architecture Tencent's own card documents as transformers/vLLM/SGLang-compatible:

```sh
pip install vllm
vllm serve "0xSojalSec/Tencent-Hy-30B-A3B-uncensored-heretic"
```

The BF16 checkpoint is **60.14 GB across 13 safetensors shards** (verified via the files-tree API) — one H200 comfortably. GGUF quants exist at [OS-Software/Hy-MT2-30B-A3B-uncensored-heretic-GGUF](https://huggingface.co/OS-Software/Hy-MT2-30B-A3B-uncensored-heretic-GGUF): Q4_K_M at ~18.2 GB, Q5_K_M ~21.4 GB, Q6_K ~24.7 GB, Q8_0 ~32 GB — the Q4_K_M fits a 24 GB consumer card. mradermacher also carries i1-imatrix IQ quants. Tencent's own FP8 twin of the base (`tencent/Hy-MT2-30B-A3B-FP8`, 5,407 downloads) is the cheaper aligned fallback if you don't need the uncensor.

ABLITERATED.cloud's approximate managed price estimate for this one: **≈ $5.45/h on 1 × H200** (the ~30B MoE band of our formula); the Q4_K_M GGUF path runs far cheaper on a single 24 GB GPU.

## The creator: Md Ismail Sojal, and the OS-Software label

The uploader is [0xSojalSec](https://huggingface.co/0xSojalSec) — profile name **Md Ismail Sojal**, describing himself as a re-searcher working on post-training, reasoning models and RAG, with seven public models including a Muse-Glimmer-30B GGUF, an Ornith-1.5-9B-OBLITERATED and GLM-5.3-Flash uncensored FP8. The identical card content also ships under the org handle [OS-Software](https://huggingface.co/OS-Software), whose nineteen models are mostly **Japanese-targeted Heretic edits** ("heretic-ja" series: Ternary-Bonsai-27B, Qwen3.8-27B-MTP, gemma-4-12B, gemma-4-26B-A4B, Ornith-1.5-35B-A3B) — the card disclaimer credits OS-Software as the provider. The Japanese-language eval note on this card fits that pattern: this group's decensor pipeline is built around Japanese refusal datasets. No donation page or socials are linked on this card; the base model's creators are Tencent's Hunyuan team (the report lists Mao Zheng, Zheng Li, Tao Chen and six more authors).

## One honest line

Safety filtering is substantially reduced here — that is the whole point, and it means this translator will render text the aligned base refused, so you own whatever you do with the output.

## The idea, in plain words

**Arbitrary-Rank Ablation (ARA)** — Classic abliteration finds one "refusal direction" in the network and erases it from the weights. ARA instead trains a small LoRA adapter that cancels that direction across a chosen range of layers while keeping every weight row's norm intact. Less surgery, smaller behavioral drift: which is why this edit stays at KL 0.0276 instead of drifting into a different model.

Primary sources:

- [Exact uncensored model card](https://huggingface.co/0xSojalSec/Tencent-Hy-30B-A3B-uncensored-heretic) and [HF model API (revision, params, license)](https://huggingface.co/api/models/0xSojalSec/Tencent-Hy-30B-A3B-uncensored-heretic)
- [Pinned files](https://huggingface.co/0xSojalSec/Tencent-Hy-30B-A3B-uncensored-heretic/tree/abe0aae382c7abce58b4be4eda48953af034025b) (config.json: hy_v3, 128 experts, 262,144-token context)
- [Official Tencent Hy-MT2-30B-A3B card](https://huggingface.co/tencent/Hy-MT2-30B-A3B) and [README_CN](https://huggingface.co/tencent/Hy-MT2-30B-A3B/blob/main/README_CN.md)
- [Hy-MT2 report (arXiv 2605.22064)](https://arxiv.org/abs/2605.22064)
- [Tencent-Hunyuan/Hy-MT2 GitHub](https://github.com/Tencent-Hunyuan/Hy-MT2) and [Tencent Hy announcement on X](https://x.com/TencentHunyuan/status/2057384034544804136)
- [Local AI News coverage](https://www.localainews.co/news/llm/tencent-ships-hy-mt2-30b-a3b-33-language-translator-that-runs-locally/)
- [OS-Software GGUF quants](https://huggingface.co/OS-Software/Hy-MT2-30B-A3B-uncensored-heretic-GGUF) and [mradermacher i1-imatrix quants](https://huggingface.co/mradermacher/Hy-MT2-30B-A3B-uncensored-heretic-i1-GGUF)
- [0xSojalSec profile](https://huggingface.co/0xSojalSec) and [OS-Software profile](https://huggingface.co/OS-Software)
- [Heretic project](https://heretic-project.org)

Community note: Reddit community search returned HTTP 403 for this run, so the reaction on r/LocalLLaMA is a known gap; the one thread we can cite (Tencent Hy 30B/7B/1.8B, r/LocalLLaMA 1tjien7) predates the uncensor and covers the base release.
