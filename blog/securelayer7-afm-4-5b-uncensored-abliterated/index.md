<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# The security vendor uncensor: AFM-4.5B from 92/100 refusals to 3/100

Published 28 August 2026. Exact artifact: `Securelayer7/AFM-4.5B-Uncensored-Abliterated`, revision `38236c07c1fda2334dbc8e109ff746f0af9a3ff4`.

SecureLayer7 is an offensive security company that sells pentests and sells a prompt-injection guardrail. On 28 August it published an abliterated Arcee AI model whose card says the weights now answer "for legitimate security research where aligned models refuse." The edit itself is routine. Who did it, and what the card openly does and does not claim, is the story.

## A security vendor walks into Hugging Face

The Hugging Face account [Securelayer7](https://huggingface.co/Securelayer7) has published exactly five model repos, and you can read the business model off the list. On 16 August: [Qwythos-9B uncensored](https://huggingface.co/Securelayer7/Qwythos-9B-Claude-Mythos-Uncensored-Abliterated-1M) (568 downloads). On 18 August: [Ling-3.0-tiny uncensored](https://huggingface.co/Securelayer7/Ling-3.0-tiny-Uncensored-Abliterated) (409 downloads). On 21 August: a [Qwen3.8-27B LoRA adapter](https://huggingface.co/Securelayer7/Qwen3.8-27B-Uncensored-Abliterated) (20 downloads). On 28 August: [AFM-4.5B-Uncensored-Abliterated](https://huggingface.co/Securelayer7/AFM-4.5B-Uncensored-Abliterated) (zero downloads at research time, twelve hours after publish). Back in May the same account published [promptpurify](https://huggingface.co/Securelayer7/promptpurify), an ONNX prompt-injection guardrail classifier, MIT-licensed.

That is the whole two-product sandwich in miniature. The company website leads with "PromptPurify is live, a tiny, powerful prompt guardrail" and "BugDazz Autonomous is live: the pentester that runs itself". One product tries to stop injected instructions; the other product attacks systems that have been instructed. An uncensored model is not a product page on the site, but it is exactly the tooling an autonomous pentest agent wants: a model that does not refuse the request mid-operation. That reading is mine, clearly labeled as such; what is fact is that the same vendor publishes guardrail models and refusal-reduced models under one account.

## The base: an enterprise 4.5B with ReLU² instead of SwiGLU

The base, [arcee-ai/AFM-4.5B](https://huggingface.co/arcee-ai/AFM-4.5B), is Arcee AI's first [Arcee Foundation Model](https://www.arcee.ai/blog/deep-dive-afm-4-5b-the-first-arcee-foundational-model), announced 18 June 2025 and uploaded 29 July 2025. The card describes an 8-trillion-token training run (6.5T general pretraining, then 1.5T midtraining with an emphasis on mathematical reasoning and code), supervised fine-tuning with Axolotl, reinforcement learning on verifiable rewards plus human preference via a modified Verifiers stack, pretraining on a modified TorchTitan, and data curation in collaboration with DatologyAI. Apache-2.0, eleven languages, 10,691 downloads and 101 likes on the base as of writing.

The architecture detail worth pausing on: grouped-query attention with 20 heads sharing 4 KV heads, and `hidden_act: relu2` in the [derivative's config](https://huggingface.co/Securelayer7/AFM-4.5B-Uncensored-Abliterated/raw/main/config.json), inherited unchanged from the base. The base card says ReLU² replaces SwiGLU "to enable sparsification". The base also ships a chat template that instructs the model to be "calm, intelligent, and personable", to "think aloud, step by step", a "wise, thoughtful companion" persona. That is the persona whose refusals got edited out. The base card publishes benchmark claims as a single image from an internal harness, with no machine-readable table, so no benchmark numbers are repeated here.

## What the edit actually changed

The derivative card and its [NOTICE file](https://huggingface.co/Securelayer7/AFM-4.5B-Uncensored-Abliterated/raw/main/NOTICE) agree on the method: refusal-direction abliteration with [Heretic](https://github.com/p-e-w/heretic) (p-e-w's "fully automatic censorship removal for language models", 28,541 stars) under an Optuna TPE multi-objective search that minimizes refusals and KL divergence together, applied to the attention output projections (`o_proj`) and MLP down-projections (`down_proj`) across all 36 layers, then merged into the weights. The repo tree confirms the merge: two safetensors shards, a LICENSE, a NOTICE, a chat template, no adapter files. You download it and it is just a model.

The published result: the base refused 92 of 100 harmful-topic probes, the edit refuses 3 of 100, at KL divergence 0.0200. Those are SecureLayer7's own measurements, disclosed in the card and the NOTICE; there is no independent re-measurement, and the card's claim that "math and factual probes remain correct" is a publisher claim, not a published eval. Method-wise this sits at a different point of the design space than other edits covered on this site: huihui leaves the first 15 layers untouched, RVN runs three ARA passes, s3nh publishes a direction index. This one is a projection-only pass at full BF16 on every layer, with nothing left over to load.

**What is proven here:** the artifact is fully inspectable: pinned revision, config, NOTICE and two shards. The 92/100 to 3/100 movement and KL 0.0200 are publisher measurements, openly disclosed as such. What is not proven: any independent refusal re-test, any capability rerun after the edit, and the claim that the result is useful for security work. The card itself insists the weights carry no guard and that lawful deployment is the operator's job.

## 3/100 is not 0/100

The card's "Responsible use" section is worth quoting because it is unusually direct for this genre: it says the model exists "for legitimate research and authorized security work", and it says, verbatim, "Illegal content (incl. CSAM) must be blocked at the serving layer; the weights carry no such guard, and the operator is responsible for a lawful, policy-gated deployment." No publisher can stop you from serving this over a public endpoint without filters; this one says so in plain text on the card.

The refusal measurement is a partial edit, honestly labeled: 3/100 is a 96.7% reduction, not a zero. The manifest therefore sets `zero_refusal: false`. The repository has no discussions yet, no community benchmarks, and at research time no downloads. For calibration, SecureLayer7's earlier uncensored releases show the audience exists: Ling-3.0-tiny has 409 downloads, Qwythos-9B has 568. This one is a day old.

One honest line: safety filtering is significantly reduced in this artifact, which is the entire point of it, and the only refusal measurement that exists is SecureLayer7's own. Treat 3/100 as a claim about their probe set, not a guarantee about yours.

## How to run it

No Ollama page exists yet and the tree is safetensors-only, so there is no GGUF ladder to grab; the supported path is transformers or vLLM. The card's quick start, bfloat16:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
m = "Securelayer7/AFM-4.5B-Uncensored-Abliterated"
tok = AutoTokenizer.from_pretrained(m)
model = AutoModelForCausalLM.from_pretrained(m, torch_dtype=torch.bfloat16, device_map="auto")
```

The serving line, if you want it over HTTP:

```bash
vllm serve Securelayer7/AFM-4.5B-Uncensored-Abliterated --max-model-len 32768
```

The base card recommends temperature 0.5, top_k 50, top_p 0.95, repeat_penalty 1.1. On cost: 8.6 GiB of weights for a dense 4.5B means a single L40S is overkill and a 24 GB consumer card fits comfortably; the approximate managed price estimate is **$2.34/hour** (1 × L40S class). If you want llama.cpp, convert the shards yourself with the llama.cpp convert script and quantize to taste; nobody has done it for you yet.

## The creator: SecureLayer7

SecureLayer7 is an offensive security company, Pune and Austin, self-described on [securelayer7.net](https://securelayer7.net) as CREST-approved, CERT-In empanelled, SOC 2 and ISO 27001 certified, with "14 years of CVE research", "130+ published CVEs, 1500+ pentests", and products including the BugDazz autonomous pentest agent and an on-prem API scanner. Those are the company's own claims from its own site; there is no independent verification of the CVE count. The NOTICE file carries the copyright line "SecureLayer7 (Waxspace)".

The HF catalog shows how they operate: one uncensored release every few days through August, small models first (9B, then a 3B-class MoE, then a 27B LoRA), full merges for the small ones, adapters for the large one, every card tagged cybersecurity, red-teaming, no-refusal, uncensored-llm. This is a company publishing for its own use case, not a community editor with a Ko-fi. And the base's developer: Arcee AI, whose [docs](https://docs.arcee.ai/arcee-foundation-models/getting-started-afm-4.5b) position AFM-4.5B as "a 4.5 billion parameter small language model, which delivers enterprise performance comparable to much larger models". The derivative's NOTICE explicitly disclaims any Arcee trademark endorsement.

## The idea, in plain words

**Why ReLU² is the interesting ingredient** — Most modern LLMs use an activation called SwiGLU. This model uses ReLU² instead: a plain activation that turns every negative value into exactly zero. Zeroed values cost nothing to compute on sparsity-aware hardware, which is why a 4.5B can claim enterprise-grade throughput, and it is the detail that makes this base unusual. The abliteration is a separate, older trick: measure the direction in activation space that correlates with refusing, then rewrite the projections that write into that direction so the model cannot go there. 36 layers of o_proj and down_proj, one direction removed, KL drift held to 0.02.

Primary sources:

- [SecureLayer7 AFM-4.5B model card](https://huggingface.co/Securelayer7/AFM-4.5B-Uncensored-Abliterated)
- [HF API record](https://huggingface.co/api/models/Securelayer7/AFM-4.5B-Uncensored-Abliterated), pinned [config.json](https://huggingface.co/Securelayer7/AFM-4.5B-Uncensored-Abliterated/raw/main/config.json) and [NOTICE](https://huggingface.co/Securelayer7/AFM-4.5B-Uncensored-Abliterated/raw/main/NOTICE)
- [arcee-ai/AFM-4.5B base card](https://huggingface.co/arcee-ai/AFM-4.5B), [Arcee launch post](https://www.arcee.ai/blog/deep-dive-afm-4-5b-the-first-arcee-foundational-model) and [Arcee docs](https://docs.arcee.ai/arcee-foundation-models/getting-started-afm-4.5b)
- [Heretic (p-e-w) repository](https://github.com/p-e-w/heretic)
- [SecureLayer7 website](https://securelayer7.net) and [about page](https://securelayer7.net/about-us) (company self-description)
- [SecureLayer7 HF catalog (API)](https://huggingface.co/api/models?author=Securelayer7)
- [TorchTitan paper](https://arxiv.org/abs/2410.06511)

Reddit search for "AFM-4.5B", "SecureLayer7" and "Arcee AFM" returned HTTP 403 during research (read-only tool blocked), so community coverage there is not included.
