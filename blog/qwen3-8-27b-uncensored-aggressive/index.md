# The lossless aggressive: Qwen3.8 27B Uncensored FP8

Published 19 August 2026. Exact artifact: `orcarouter/Qwen3.8-27B-Uncensored-FP8`, revision `9228df5c6c9c509e1019f83b4e085cf643118bac`.

While huihui-ai raced out its "crude proof of concept" abliteration, a second edit quietly became the most-liked Qwen3.8 uncensored on Hugging Face: orcarouter's block-FP8 build, 553 likes in four days, 45,465 downloads, served gated behind an API at $0.40 per million input tokens. Same Qwen3.8-27B base — 27,781,427,952 parameters, 64 hybrid layers, 27-layer vision encoder, 262,144-token context — but a bolder promise: the card calls it lossless, capabilities preserved while refusal behavior is removed, shipped already quantized to block-FP8 with the vision tower at full precision.

"Aggressive" here means fully unlocked per the OrcaRouter listing: direct, complete responses across a wide prompt range, occasionally appending brief informational disclaimers inherited from base training — which it states are not refusals. That is a publisher claim; no measured refusal-rate table is published, so this artifact does not carry a ZERO REFUSALS badge.

Third-party numbers (Artificial Analysis, evaluated 14 August 2026): AA Coding 68.1 (#30 of 133), AA Intelligence 52.0 (#29 of 135), GPQA Diamond 90.5, Humanity's Last Exam 33.9, Long-Context Recall 77.3, SciCode 44.7, terminalbench v2.1 79.8, tau_banking 48.0. What is missing: a public refusal-reduction measurement for this exact edit and a capability-retention A/B against the unedited base.

The edit and serving build come from [orcarouter](https://huggingface.co/orcarouter), the company behind the [OrcaRouter gateway](https://www.orcarouter.ai/) — 197 models, 16 providers, zero token markup. The same crew ships the other "obsidian" uncensored builds (Qwen3.6 35B A3B Aggressive, Gemma4 26B A4B Balanced).

## How to run it

The API is OpenAI-compatible and gated:

```python
from openai import OpenAI
client = OpenAI(base_url="https://api.orcarouter.ai/v1", api_key="ORCAROUTER_API_KEY")
resp = client.chat.completions.create(model="obsidian/Qwen3.8-27B", messages=[{"role":"user","content":"Build it."}])
```

$0.40 per million input tokens, $4.21 per million output, 262K context, image and video input. For self-hosting, the exact pinned repository serves in vLLM on one H200; the ABLITERATED.cloud prepared profile estimates $5.45/hour managed.

## The idea, in plain words

**Why FP8 is the boring hero of this story** — Neural networks normally store every weight as a 16-bit number. Block-FP8 packs them into 8 bits with per-block scaling: half the memory, near-identical inference quality, which turns a 55 GB download into a model you can serve on one GPU. Quantization is why "open weights" and "usable API" are different things.

Primary sources:

- [Exact orcarouter model card](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8)
- [Pinned artifact](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8/tree/9228df5c6c9c509e1019f83b4e085cf643118bac)
- [OrcaRouter model page — pricing and benchmarks](https://www.orcarouter.ai/models/obsidian/Qwen3.8-27B)
- [OrcaRouter gateway](https://www.orcarouter.ai/) and [orcarouter profile](https://huggingface.co/orcarouter)
- [Official upstream Qwen card](https://huggingface.co/Qwen/Qwen3.8-27B)
- [Artificial Analysis benchmark source](https://artificialanalysis.ai/)

"Lossless" and "fully unlocked" are the publisher's claims; the third-party benchmarks are the only independent measurement, and no refusal-rate measurement exists. Unlock comes with the usual trade — you verify what comes back.
