# The 2.78-trillion-parameter abliteration nobody can run

Published 17 August 2026. Exact artifact: `Resggg/Kimi-K3-Abliterated-modal`, revision `b3a52d265b56551c0011b24d299ba3f8f1393e42`.

`Resggg/Kimi-K3-Abliterated-modal` is an abliterated Kimi K3 with 2,779,931,837,184 parameters, about 1.56 TB of storage across 96 safetensors shards, and zero downloads, likes or discussions at review. Its card text is a verbatim re-upload of the SHS-Lab/Kimi-K3-Abliterated card (badges, logo asset and code examples all still reference SHS-Lab). The base model, Moonshot's Kimi K3, has 2.16 million downloads.

The scale math: FP16 would be ~5.1 TiB; the repo ships MXFP4-packed weights (2.72T U8 elements plus unquantized BF16 pieces), landing at roughly 1.35 TiB of weights. One H200 holds 141 GB, so weights alone need ~11 H200s. A 16×H200 node (~2.1 TiB) is our honest ballpark, at an approximate managed price estimate of $87.20/hour — highly speculative. No inference provider lists the model.

Upstream claims (Moonshot's card, not our measurements): 2.8T-parameter MoE on Kimi Delta Attention and Attention Residuals, 93 layers, 896 experts with 16 routed plus 2 shared, 1M-token context, MXFP4/MXFP8 quantization-aware training, Kimi K3 License ("other"). The derivative's "98%+ refusal signal removed" and video-modality claims are SHS-Lab publisher claims copied into this repo — unverified, since zero downloads means zero community verification exists.

Abliterated Kimi K3 variants are plentiful (Uniboshi V1, Blackfrost Q2_K GGUF, penclaw GGUF, SHS-Lab original), but runnable ones are not. The r/LocalLLaMA thread "Waiting for someone to abliterate Kimi K3 and host it" captures the community state. We do not host this artifact; this is a field note on an unrunnable upload.

Primary sources:

- [Exact model card](https://huggingface.co/Resggg/Kimi-K3-Abliterated-modal)
- [Pinned artifact](https://huggingface.co/Resggg/Kimi-K3-Abliterated-modal/tree/b3a52d265b56551c0011b24d299ba3f8f1393e42)
- [HF model API metadata](https://huggingface.co/api/models/Resggg/Kimi-K3-Abliterated-modal)
- [SHS-Lab/Kimi-K3-Abliterated](https://huggingface.co/SHS-Lab/Kimi-K3-Abliterated)
- [Official Moonshot Kimi K3 card](https://huggingface.co/moonshotai/Kimi-K3)
- [Kimi tech blog](https://www.kimi.com/blog/kimi-k3)
- [Uniboshi/Kimi-K3-Abliterated-V1](https://huggingface.co/Uniboshi/Kimi-K3-Abliterated-V1) · [Blackfrost Q2_K GGUF](https://huggingface.co/Blackfrost-AI/KIMI-K3-Q2_K-GGUF-ABLITERATED) · [penclaw GGUF](https://huggingface.co/audnai/penclaw-Kimi-K3.0-abliterated-GGUF)
- [r/LocalLLaMA thread (community opinion)](https://www.reddit.com/r/LocalLLaMA/comments/1v8h269/waiting_for_someone_to_abliterate_kimi_k3_and/)
- [Tom's Hardware release coverage](https://www.tomshardware.com/tech-industry/artificial-intelligence/moonshot-ai-releases-weights-for-kimi-k3-firing-a-shot-across-the-bow-of-openai-and-anthropic-open-weight-model-performs-almost-as-well-as-frontier-models-while-being-2-3x-easier-to-run)
- [Refusal in Language Models Is Mediated by a Single Direction](https://arxiv.org/abs/2406.11717)

Uploaded, licensed and endpoints-compatible — and entirely unrun. "Abliterated" here means refusal-reduced per publisher claim: not verified, not zero-refusal, and not once executed.
