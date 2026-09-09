# MiniCPM5-2B, uncensored and reproducible<!-- READING-TLDR -->

## TL;DR

- OpenBMB released MiniCPM5-2B, a 2.5B Apache-2.0 dense model with 128K context, on 6 September 2026.
- insraq measured the stock model refusing 99 of 100 prompts and the Heretic edit 5 of 100.
- The edit pins its base commit, prompt datasets, RNG seed and weight hashes, so the rebuild is byte-checkable.
- GGUF and Apple MLX packs of the edit arrived within two days, the smallest rung at 1.23 GB.

## Basically, the facts

**What MiniCPM5-2B is**

Basically, OpenBMB released MiniCPM5-2B on 6 September 2026 with Apache-2.0 and a 128K-token context window.

**The refusal wall: 99 of 100**

Basically, insraq measured 99 refusals in 100 prompts on the stock MiniCPM5-2B before the edit.

**Heretic, trial 254**

Basically, Heretic's search ran 254 trials and chose trial 254: 5 refusals in 100 prompts at KL 0.0391.

**A kit, not just a model**

Basically, insraq ships a kit of pinned base, datasets, seed and hashes so anyone can rebuild the edit byte for byte.

**The ladder that followed**

Basically, Two days after the edit, packagers added GGUF and Apple MLX builds down to 1.23 GB.

**How to run it**

Basically, The edited model keeps the standard Llama architecture, so llama.cpp, Ollama and MLX load it without forks.

**The editor: insraq**

Basically, The kit follows insraq's house pattern from his August Heretic on Empero's Qwen3.8-4B.

**The idea, in plain words**

Basically, Abliteration subtracts a refusal direction found per layer; the search here picks how far, trial by trial.
<!-- /READING-TLDR -->
<!-- ARTICLE-META-MD -->
_Published 9 September 2026 · 9 min read · Canonical: https://abliterated.cloud/blog/minicpm5-2b-heretic-abliterated-reproducible/_
<!-- /ARTICLE-META-MD -->

*Published 9 September 2026 · Revision-pinned · Primary sources only*

**Model:** [insraq/MiniCPM5-2B-heretic-abliterated](https://huggingface.co/insraq/MiniCPM5-2B-heretic-abliterated) · pinned revision `8d83eaf4…cd8ef0d8` (created 7 September 2026, 21:13 UTC)
**Base:** [openbmb/MiniCPM5-2B](https://huggingface.co/openbmb/MiniCPM5-2B) (Apache-2.0, 6 September 2026) · 2,516,756,480 params, 1,981,982,720 non-embedding · dense `LlamaForCausalLM`, 42 layers, 16 Q / 2 KV heads · 131,072-token context · BF16 ≈ 4.7 GiB, GGUF Q4_K_M ≈ 1.5 GiB · base revision pinned by editor: `3497c460…647f1177` · no dated rental quote in this article

On 6 September 2026, OpenBMB released MiniCPM5-2B, the second model of its MiniCPM5 family and its first proper 2B-class flagship: Apache-2.0, dense, 128K native context, a full open-data release behind it, and a benchmark card that claims the top of the 2B class with agent scores above several 4B rivals. The stock model is also extremely reluctant. On the editor's 100-prompt screen it refused 99 of 100. Thirty-four hours after the base appeared, insraq shipped a Heretic edit that measures 5 refusals out of 100 on the same screen, and the edit is not a trust-me binary: it comes with the base commit, the prompt sets, the random seed and the weight hashes needed to rebuild it byte for byte.

## What MiniCPM5-2B is

MiniCPM5-2B is a text-only, dense causal model from OpenBMB, the lab behind the MiniCPM family, and the second release in the MiniCPM5 series after MiniCPM5-1B. The card lists a plain `LlamaForCausalLM` architecture with no custom kernels: 2,516,756,480 parameters (1,981,982,720 non-embedding), 42 layers, grouped-query attention with 16 query heads and 2 key-value heads, 130,560-token vocabulary and a 131,072-token native context window. It is licensed Apache-2.0 and speaks English and Chinese. Post-training runs SFT, RL and OPD: roughly 400B tokens of deep-thinking SFT, specialized RL teachers for math, code, agentic work and writing, and On-Policy Distillation that merges 16 expert models back into one release checkpoint. The training data is public too, the UltraData family: UltraX-Preview web data, tiered UltraData-Code, 500K agent SFT samples and 80K+ RL samples among them.

The card's headline claim is a 2B-class open-source SOTA with an average of 53.9 across its comparison set, above LFM2.5-2.6B at 33.2, Qwen3.5-2B at 28.0 and Gemma-4-E2B-it at 24.6, and also above every larger model listed, including Qwen3.5-4B at 51.1. The strongest cells are coding, math, long context and agents: AIME 2026 at 86.5, SWE-bench Verified at 46.4, τ²-bench Telecom at 97.1. Those are publisher measurements from the OpenBMB card: cells marked with a dagger come from the official Artificial Analysis release and the rest were reproduced internally by the vendor, and none were independently reproduced for this article. Community appetite is visible in the numbers: 2,879 downloads and 758 likes inside its first three days, with base-repo discussions already proposing NPU, browser and local-runtime builds (community signal, not measurement).

## The refusal wall: 99 of 100

What interests this site is the stock behavior the marketing table does not show. Small models trained hard for agentic usefulness are usually trained hard against refusal too, and MiniCPM5-2B sits at the reluctant end of that trade. insraq's published screen compares the stock model with the edited one on the same prompts, and the stock model refused 99 of the 100. The prompts are not secret: the reproduction kit pins the bad-prompt set to [mlabonne/harmful_behaviors](https://huggingface.co/datasets/mlabonne/harmful_behaviors) at commit `01cead01…ebba7` and the good-prompt set to [mlabonne/harmless_alpaca](https://huggingface.co/datasets/mlabonne/harmless_alpaca) at commit `02c6a92c…b587f`, the standard public suites of this genre. So the 99/100 is a publisher measurement on a 100-prompt harmful-behaviors screen, narrow by design, and this article reports it as that, not as a universal property. A 2B model that refuses almost everything on that screen is exactly the shape of model the uncensor ecosystem exists for.

## Heretic, trial 254

The edit was made with [Heretic](https://github.com/p-e-w/heretic) v1.4.0 (p-e-w, AGPL-3.0), the same toolchain insraq used for his August edit of Empero's Qwen3.8-4B distill, covered on this site on 17 August. Heretic is abliteration by search: a TPE-based optimizer powered by Optuna co-minimizes two goals at once, fewer refusals and less KL divergence from the original model, and the operator exports a trial from the resulting Pareto front. For MiniCPM5-2B the search ran 254 trials, and the published artifact is trial 254: 5 refusals out of 100 on the same screen that counted 99 on the stock model, at a KL divergence of 0.0391 from the base (0 by definition for the base itself). The card publishes the resulting per-layer direction parameters, including projection weights up to 1.47 concentrated in the upper half of the 42 layers, which is the signature of a deeper edit than his previous run, where trial 128 of the Qwen3.8-4B distill measured 6/100 at KL 0.0167.

The derivative went up 7 September at 21:13 UTC, about thirty-four hours after the base repo appeared, and had 510 downloads and 1 like when this article's facts were fetched on 9 September. Everything in this paragraph is publisher-reported, but it is reported with receipts, which is the point of the next section.

## A kit, not just a model

The `reproduce/` directory inside the model repo is what separates this release from most of the genre. It contains a reproduction guide, an exact `requirements.txt`, a `config.toml` with the configuration including the RNG seed, the full Optuna study journal as `openbmb--MiniCPM5-2B.jsonl` so the other 253 trials are inspectable rather than just claimed, and a `SHA256SUMS` file over both weight shards. The base model is pinned to openbmb/MiniCPM5-2B commit `3497c460…647f1177`, the good and bad prompt sets are pinned to their dataset commits, and the environment is documented: Heretic v1.4.0 from PyPI and PyTorch 2.12.1+cu130. The guide's suggested command is `heretic --reproduce reproduce.json`, which automates the run and its verification steps. Anybody with a GPU can download the kit and rebuild the published weights, then check them with `sha256sum -c SHA256SUMS`; byte-identical output is the acceptance test. Most uncensors ask you to trust a name and a download count. This one publishes the receipts first.

## The ladder that followed

The quantization wave started the same week, all on the standard Llama architecture so no custom conversion code was needed. [mondk](https://huggingface.co/mondk) published a GGUF ladder of the edit on 8 September: F16 at 5.04 GB, Q8_0 at 2.68 GB, Q6_K at 2.07 GB, Q5_K_M at 1.81 GB, Q4_K_M at 1.56 GB, IQ4_XS at 1.42 GB, Q3_K_L at 1.38 GB and IQ3_M at 1.23 GB, file sizes from the Hugging Face tree at research time. The same packager added a safetensors repack on 8 September and an MLX 4-bit build for Apple Silicon on 9 September. [mradermacher](https://huggingface.co/mradermacher) shipped an imatrix GGUF pack (`MiniCPM5-2B-heretic-abliterated-i1-GGUF`) and [Abiray](https://huggingface.co/Abiray) a GGUF pack, both on 8 September. The derivative itself is the 2B of this family, so every rung is a laptop file: the smallest is 1.23 GB and even the F16 checkpoint is about 4.7 GiB. At research time these packs showed zero downloads while the source edit had 510, which is the usual lag between a fresh edit and the ecosystem catching up.

## How to run it

Because the edited model keeps the standard `LlamaForCausalLM` shape, the usual runtimes load it without forks. The GGUF rungs run in upstream llama.cpp, Ollama and LM Studio; the MLX build runs on Apple Silicon; the BF16 checkpoint loads in transformers, vLLM and SGLang the same way the official model does, with the same 131,072-token context ceiling. A working llama.cpp start for the mid rungs looks like this:

```sh
llama-cli -m minicpm5-2b-abliterated-Q4_K_M.gguf \
  -c 32768 -n 512 --temp 1.0 --top-p 0.95
```

One honest sizing note: the weight file is only part of the memory bill. At the full 131,072-token context the attention cache alone is on the order of 5 GiB for this shape (2 KV heads, 128-dim head, 42 layers, 16-bit cache), so very long contexts want 16 GB-class hardware or a quantized cache, while everyday contexts run on any 8 GB card and most laptops. This site does not currently serve the edited model: the project's documented path stays private on-demand evaluation on Vast.ai with llama.cpp, and its reference box was stopped at the 5 September snapshot. No dated rental quote is claimed in this article; a fresh provider quote for a 2B serving box was not fetched, and a model whose largest rung is 5 GB does not need the GPU class this site's snapshot describes anyway.

## The editor: insraq

insraq is the same editor this site covered on 17 August for [Qwen3.5-4B-EmperoAI-Qwen3.8-Distill-Heretic-Abliterated](https://huggingface.co/insraq/Qwen3.5-4B-EmperoAI-Qwen3.8-Distill-Heretic-Abliterated), and the two releases share the same house pattern: an Optuna study journal, a config file with the RNG seed, pinned prompt sets and a SHA256SUMS file, with the chosen trial and its refusal and KL numbers stated plainly on the card. What changed is the base: the August run edited a community distill of Qwen3.8, while this run edits an official OpenBMB release three days after it shipped, with 758 likes and a vendor org behind it. That is the pattern that matters for the genre: measured, reproducible edits arriving days after an official Apache-2.0 release, so the refusal behavior of a popular small model does not stay the last word on it.

## One honest line

The safety filtering on an agent-capable official model is significantly reduced by this edit, so anything you have it do, you own, and a 5-out-of-100 score on one narrow screen is not a zero-refusal guarantee of anything.

## The idea, in plain words

**Direction surgery.** A model's refusals are not a switch; they live in directions of its internal activations that were reinforced during training. Abliteration finds the refusal direction and subtracts it, scaled, from the activations, and Heretic automates the fiddly part: it searches per layer for how strongly to subtract, balancing two goals, fewer refusals and less drift from the original model, measured as KL divergence. Because that search involves randomness, the same recipe can land on different trials, which is why the artifact here is not just "an uncensored MiniCPM5-2B" but "trial 254 of 254, with this seed, these prompts and these hashes". The numbers become checkable claims instead of marketing.

*Coverage gaps: this article is built from Hugging Face model cards, repo files and the Hugging Face API, fetched 9 September 2026. All refusal counts and benchmarks are publisher-reported; none were independently reproduced, no GPU was rented and no inference was run for this article. Community signal is limited to download counts and base-repo discussion threads and is labeled as such.*

## Primary sources

- [insraq/MiniCPM5-2B-heretic-abliterated (card: Heretic v1.4.0, refusal and KL table, direction parameters)](https://huggingface.co/insraq/MiniCPM5-2B-heretic-abliterated) · [pinned revision `8d83eaf4…cd8ef0d8`](https://huggingface.co/insraq/MiniCPM5-2B-heretic-abliterated/tree/8d83eaf42e30f4e4f164b8685be0ecdccd8ef0d8)
- [reproduce/README.md (base and dataset commit pins, trial 254, environment, reproduce steps)](https://huggingface.co/insraq/MiniCPM5-2B-heretic-abliterated/blob/main/reproduce/README.md) · [SHA256SUMS](https://huggingface.co/insraq/MiniCPM5-2B-heretic-abliterated/blob/main/reproduce/SHA256SUMS) · [config.toml](https://huggingface.co/insraq/MiniCPM5-2B-heretic-abliterated/blob/main/reproduce/config.toml)
- [openbmb/MiniCPM5-2B (official card: architecture, benchmarks, training recipe, 6 Sep 2026)](https://huggingface.co/openbmb/MiniCPM5-2B)
- [HF API: derivative facts (created 2026-09-07T21:13:33Z, sha 8d83eaf4, downloads/likes)](https://huggingface.co/api/models/insraq/MiniCPM5-2B-heretic-abliterated)
- [HF API: base facts (created 2026-09-06T11:12:19Z, downloads/likes)](https://huggingface.co/api/models/openbmb/MiniCPM5-2B)
- [mondk GGUF ladder (file sizes from HF tree, 8 Sep 2026)](https://huggingface.co/mondk/MiniCPM5-2B-Abliterated-Uncensored-GGUF) · [MLX 4-bit](https://huggingface.co/mondk/MiniCPM5-2B-Abliterated-Uncensored-MLX-4Bit) · [safetensors repack](https://huggingface.co/mondk/MiniCPM5-2B-Abliterated-Uncensored-Safetensors)
- [mradermacher imatrix GGUF pack](https://huggingface.co/mradermacher/MiniCPM5-2B-heretic-abliterated-i1-GGUF) · [Abiray GGUF pack](https://huggingface.co/Abiray/MiniCPM5-2B-heretic-abliterated-GGUF)
- [mlabonne/harmful_behaviors (pinned `01cead01…ebba7`)](https://huggingface.co/datasets/mlabonne/harmful_behaviors) · [mlabonne/harmless_alpaca (pinned `02c6a92c…b587f`)](https://huggingface.co/datasets/mlabonne/harmless_alpaca)
- [Heretic tool and project](https://github.com/p-e-w/heretic) · [prior coverage: insraq's Qwen3.8-4B distill edit, 17 Aug 2026](https://abliterated.cloud/blog/qwen3-5-4b-emperoai-qwen3-8-distill-heretic-abliterated/)
- [insraq profile](https://huggingface.co/insraq) · [openbmb/MiniCPM GitHub](https://github.com/OpenBMB/MiniCPM)

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Want this model running for you, on a private cloud GPU or your own machine? [Request access on Signal](https://signal.me/#p/+13103408213) or [see how it works](https://abliterated.cloud/#how).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
