# The base of the wave: Muse-Glimmer-30B's measured de-refusal

Published 12 August 2026. Exact artifact: `jorkle/Muse-Glimmer-30B-Abliterated`, revision `f98c6e1f6a268fa79d1e704c6b69fa89a61ddda6`.

Muse-Glimmer-30B is Meta's dense 29.8B agentic model (29,776,626,688 parameters including the ~1.8B ViT-G/14 perception encoder), released 9 August 2026 under Apache-2.0: 52 layers, hidden 6656, GQA at 32 query / 2 KV heads, a local-local-local-global attention cycle with a 2048 sliding window, SwiGLU, and a 131,072+ token context. It is not an MoE — every parameter participates per token. It is distilled from Muse Spark and ships with a DFlash block-diffusion drafter for speculative decoding.

Three days after the release, jorkle (Kyle Walters) published this de-refusal build. It is not the first abliterated Muse-Glimmer — darkc0de's "heretic" build and Blackfrost-AI's abliterated BF16 + GGUF ladder shipped 10 August, and mlasli's direction ablation on 11 August — but it is the first that documents its method fully. The method is a KL-conserving, best-of-N steered LoRA SFT (loss `CE(compliance) + λ·KL(tuned‖base)`, λ_KL = 1.0, r=16, 544 refusal-filtered prompts, 48-pair holdout, LoRA on `o_proj`/`down_proj`, 31.1M trained params, 0.10% of the model), folded into base weights. Not a weight ablation.

Reported results: 13/100 refusals on harmful_behaviors where the base scores 100/100 (~87% reduction) at mean response-token KL 0.0988 against base; 5/100 over-refusals on or-bench; 1/2 correct refusals on cyber-policy-refuse; two genuinely malicious-sounding prompts still refused. Benchmarks were skipped by request — the card publishes a KL table instead of a benchmark table, and ships base Q8_0/Q4_K_M reference files in the sibling GGUF repo so the KL math is reproducible. An Aggressive twin (λ_KL = 0.5: 0/100 refusals, KL 0.1697, ~1.7× drift) was published the same minute; SHS-Lab re-uploaded it 17 August with zero downloads.

The ecosystem around the model is the story: the base's quant zoo (unsloth GGUF at 755k downloads, lmstudio-community, bartowski, mlx-community, NVFP4, exl3, ROCmFPX, Jundot's oQ4e) exploded within days, while the de-refusal fork splits on method — direction ablation versus KL-bounded SFT. The most-downloaded abliterated artifact is Blackfrost's GGUF ladder (68,580 downloads); this model, the most methodologically documented of the wave, has 344 downloads and one like.

## The idea, in plain words

**How you measure that an edited model is still the same model** — KL divergence is the ruler: it measures how far a model's answer distribution drifted from the original. A de-refusal that reports a KL table instead of benchmark scores is telling you the trade — refusals removed, but exactly how much the behavior moved. It's the honesty meter of the edit.

Primary sources:

- [jorkle model card](https://huggingface.co/jorkle/Muse-Glimmer-30B-Abliterated) and [pinned files](https://huggingface.co/jorkle/Muse-Glimmer-30B-Abliterated/tree/f98c6e1f6a268fa79d1e704c6b69fa89a61ddda6)
- [jorkle aggressive card](https://huggingface.co/jorkle/Muse-Glimmer-30B-Abliterated-Aggressive) and [jorkle GGUF repo](https://huggingface.co/jorkle/Muse-Glimmer-30B-Abliterated-GGUF)
- [SHS-Lab aggressive re-upload](https://huggingface.co/SHS-Lab/Muse-Glimmer-30B-Abliterated-Aggressive) (17 August 2026)
- [Official Meta model card](https://huggingface.co/meta-models/Muse-Glimmer-30B) and [release article](https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model)
- [mlasli abliteration card](https://huggingface.co/mlasli/Muse-Glimmer-30B-Abliterated-BF16) and [method JSON](https://huggingface.co/mlasli/Muse-Glimmer-30B-Abliterated-BF16/raw/main/abliteration_info.json)
- [Blackfrost-AI abliterated card](https://huggingface.co/Blackfrost-AI/Muse-Glimmer-30B-Abliterated-BF16) and [GGUF ladder](https://huggingface.co/Blackfrost-AI/Muse-Glimmer-30B-Abliterated-GGUF)
- [cvgro GGUF card](https://huggingface.co/cvgro/Muse-Glimmer-30B-Abliterated-GGUF), [Jundot oQ4e card](https://huggingface.co/Jundot/Muse-Glimmer-30B-oQ4e)
- [Raschka architecture notes](https://sebastianraschka.com/blog/2026/muse-glimmer-30b-architecture-notes.html) (independent analysis)
- [r/LocalLLaMA "Glimmer seems pretty censored?"](https://www.reddit.com/r/LocalLLaMA/comments/1vkkw6n/glimmer_seems_pretty_censored/) (community discussion)
- Hugging Face model API records for jorkle, Blackfrost-AI, mlasli, SHS-Lab, Jundot, unsloth and meta-models repositories

We pin the BF16 normal variant and serve it as text-generation on one H200 (about $5.45/hour, approximate managed price estimate). Vision behavior after the fold is not re-verified by the publisher, so we do not claim it. The card retains 13% refusals on its own eval: this is refusal-reduced with documented drift, not a zero-refusal model. Verify behavior for your use case before deployment.
