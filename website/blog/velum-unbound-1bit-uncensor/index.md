# The 1-bit uncensor: can a refusal direction survive 1.125 bits per weight?

Published 28 August 2026. Exact artifact: `guell00/Velum-Unbound-Uncensored`, revision `97e4ecf9dd6dc2f2e263c60e8de8e17aafedddb9`.

The Bonsai family is the most downloaded 1-bit experiment of the summer, roughly three million downloads across its three public packs. Early this morning a Brazilian creator published the uncensored branch: a Heretic-decensored 27B repacked to 1.125 bits per weight, with a speculative drafter riding along.

## The chain

- **Prism ML built Bonsai-27B**, a Qwen3.6-27B derivative stored as one sign bit per weight plus a shared scale per 128-weight group. The full-size repo is gated; the GGUF and MLX packs are public.
- **s3nh decensored it** on 14 July with Heretic v1.4.0 from the FP16 unpack: refusals 81/100 to 6/100, KL 0.0033, with published edit parameters (direction index 29.58). Editor's own measurements on the FP16 edit.
- **tommytracx quantized the decensor** to Q1_0 GGUF on 1 August as Thox1-27b (THOX.ai).
- **guell00 repackaged it** on 28 August as Velum-Unbound-Uncensored: the Q1_0 weights plus a dspark drafter, a fresh card, a Brazil flag, and an MTP story.

The artifact is two files: `VELUM-UNBOUND-Q1_0.gguf` (4,667,606,336 bytes) and `dspark/dspark-VELUM-UNBOUND-Q1_0.gguf` (1,946,393,568 bytes), per the HF model API. Nothing in the chain is gated.

## Why a 1-bit model is the vehicle

The Bonsai 1-bit GGUF carries 636,606 downloads and 813 likes; the MLX 1-bit carries 1,954,689 downloads; the ternary twin carries 557,054 downloads and 1,246 likes. Prism ML's published case: true 1.125 bits per weight, ~3.9 GB deployed versus ~54 GB FP16, 262,144-token context, 44 tok/s on an Apple M5 Pro, 104.8 tok/s on an H100, math benchmarks that hold near FP16 while conventional 2-bit builds collapse. Those are upstream publisher claims, and the discussion threads show not everyone gets the advertised speed.

## The edit happened in FP16. The squeeze came after.

s3nh's card publishes the abliteration parameters: direction index 29.58, attention output projection max weight 1.43 at position 38.82, MLP down-projection max weight 1.39 at position 39.20, using Heretic v1.4.0. Measured on the FP16 edit: 6/100 refusals versus the original's 81/100, KL 0.0033.

Then the result went through the 1-bit grinder: every weight becomes +scale or −scale. A projection followed by sign quantization is not the same projection. Nobody has published a refusal re-test on the Q1_0 pack; the Velum card lists every benchmark as TBD. The 6/100 belongs to the FP16 edit, not to this artifact.

**What is proven here:** the lineage is fully sourced, and the decensor's parameters and KL are published by the editor. What is not proven is the behavior of the final Q1_0 artifact: no refusal re-measurement, no capability rerun, no speed claim on the Velum files themselves.

## How to run it

This is a llama.cpp model. The Q1_0 format needs the [PrismML llama.cpp fork](https://github.com/PrismML-Eng/llama.cpp) with the low-bit kernels. No Ollama page exists for any model in this chain as of writing:

```bash
git clone https://github.com/PrismML-Eng/llama.cpp
cmake -B build -DGGML_CUDA=ON && cmake --build build -j
huggingface-cli download guell00/Velum-Unbound-Uncensored --include '*.gguf' --local-dir ./velum
./build/bin/llama-cli -m ./velum/VELUM-UNBOUND-Q1_0.gguf -p "Hello" -n 256 --temp 0.7 --top-p 0.95 -ngl 99
```

The drafter is a DSpark speculative-decoding layer, a six-layer block-parallel transformer adding roughly 0.5 GB at serving precision, with a measured 1.37x end-to-end decode speedup on the CUDA path per the Bonsai card. Verification is lossless, so the drafter affects speed, not output. Whether the Velum pack's drafter was trained against this exact uncensored target is not documented; measure acceptance before trusting the speedup.

Cost: primary estimate for a 27B dense class is **$5.45/hour** managed (1 × H200). A 3.9 GB weight file serves comfortably on a single L40S or consumer GPU, closer to the $2.34/hour class, and on a laptop it costs only electricity.

## The creator: guell00 (and the chain behind the edit)

guell00 is Miguel p r, a non-Pro HF user with six models and two followers: VELUM-Coder (4,990 downloads), Nexora-Qwen-Coder-4B (4,061), Nexora-Gemma-4-Coder (2,705). A small independent operator shipping local-first packs. The card is explicit: "Local · Unbound · MTP", "MADE IN BRAZIL", multilingual Portuguese and English. No socials, no Ko-fi, no donation address on the card; the funding model is not documented.

The edit itself is s3nh's work, 273 models and 267 followers. tommytracx operates the THOX.ai label ("Your AI. Your Data. Your Rules."), which published the intermediate Q1_0 quant. The original Bonsai comes from Prism ML, with its [whitepaper](https://github.com/PrismML-Eng/Bonsai-demo), demo repo and Discord. Four independent parties, one chain, zero coordination visible.

One honest line: safety filtering is significantly reduced across this lineage, which is the entire point of the chain, and the refusal measurement that exists was made on the FP16 intermediate, not on the 1-bit file you would actually download.

## The idea, in plain words

**What "1.125 bits per weight" means** — Every number in a normal model is a precise value of 16 bits or more. A 1-bit model throws almost all of that away: each weight becomes just a sign, + or −, and one shared scale value covers each group of 128 weights. That is how a 27-billion-parameter model shrinks from ~54 GB to ~3.9 GB. Abliteration normally needs precise activation measurements to find and remove the refusal direction; this model had that done at full precision first, then got crushed down to signs. Whether the refusal removal still works after the crush is the honest open question.

Primary sources:

- [Velum-Unbound-Uncensored model card](https://huggingface.co/guell00/Velum-Unbound-Uncensored)
- [HF API record for Velum](https://huggingface.co/api/models/guell00/Velum-Unbound-Uncensored)
- [s3nh decensor card (Heretic v1.4.0, 6/100, KL 0.0033)](https://huggingface.co/s3nh/Bonsai-27B-unpacked-abliterated-uncensored)
- [Thox1-27b card (intermediate Q1_0, config)](https://huggingface.co/tommytracx/Thox1-27b)
- [Prism ML Bonsai-27B 1-bit GGUF card](https://huggingface.co/prism-ml/Bonsai-27B-gguf) and [MLX twin](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit)
- [Bonsai whitepaper and demo repo](https://github.com/PrismML-Eng/Bonsai-demo)
- [Community discussions on the Bonsai GGUF](https://huggingface.co/prism-ml/Bonsai-27B-gguf/discussions)

Reddit search for "Bonsai 27B" returned HTTP 403 during research (read-only tool blocked), so community coverage there is not included.
