# Inside Huihui-Qwen3.6: 256 experts, 3B active parameters, and one refusal direction<!-- READING-TLDR -->

## TL;DR

- Huihui-Qwen3.6 stores nearly 36B parameters while activating about 3B per token.
- Huihui describes the refusal-direction edit as an uncensored proof of concept.
- Qwen's upstream scores were not rerun on the abliterated checkpoint.

## Basically, the facts

**Sparse computation is not a small model**

Basically, Qwen3.6 35B A3B activates about 3B parameters per token but stores nearly 36B.

**Three days from release to abliteration**

Basically, Huihui published its Qwen3.6 derivative three days after Qwen's April 2026 release.

**What abliteration actually edits**

Basically, Huihui's Qwen3.6 abliteration edits selected weights rather than using a jailbreak prompt.

**The upstream numbers—and the honest boundary**

Basically, Qwen's benchmark scores do not establish how Huihui's edited Qwen3.6 checkpoint performs.

**Who made it?**

Basically, Qwen supplied the original Qwen3.6 model; huihui-ai published the edited derivative.

**How we treat it**

Basically, Huihui's Qwen3.6 publisher recommends controlled research use because safety filtering is reduced.

**The idea, in plain words**

Basically, Qwen3.6 routes each token through eight selected experts plus one shared expert.
<!-- /READING-TLDR -->

Published 18 July 2026. Exact artifact: `huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated`, revision `8f0ee727aff5e771ea72466d64d13ecd851d2cc7`.

Qwen3.6 35B A3B is a sparse multimodal mixture-of-experts model with 35,951,822,704 stored BF16 parameters and about 3B active for each token. Its 40 language layers combine 256-expert MoE blocks, Gated DeltaNet and periodic full attention. Native context is 262,144 tokens; the repository is roughly 71.9 GB.

Qwen released the upstream checkpoint on 15 April 2026. Huihui published this abliterated derivative three days later, describing it as an uncensored proof of concept. Abliteration compares activations produced by harmful and harmless prompts, estimates a direction associated with refusal, and projects that direction out of selected weights. It is a weight edit, not a prompt jailbreak or conventional fine-tune.

The upstream Qwen model reports 73.4 SWE-bench Verified, 67.2 SWE-bench Multilingual, 49.5 SWE-bench Pro, 51.5 Terminal-Bench 2.0 and 37.0 MCPMark. Those results do **not** belong to the abliterated derivative: Huihui publishes no post-edit benchmark or refusal-rate evaluation for this checkpoint.

## The idea, in plain words

**A 36-billion-parameter model that only spends 3 billion per answer** — This is a mixture of experts (MoE). The weights hold 256 specialized 'expert' modules, and for every token the model wakes up just eight of them plus one shared expert. Big knowledge, small compute bill: you store a giant brain, but each thought only lights up the shelves it needs.

Primary sources:

- [Exact model card](https://huggingface.co/huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated)
- [Pinned artifact](https://huggingface.co/huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated/tree/8f0ee727aff5e771ea72466d64d13ecd851d2cc7)
- [Official upstream Qwen card](https://huggingface.co/Qwen/Qwen3.6-35B-A3B)
- [Official Qwen release article](https://qwen.ai/blog?id=qwen3.6-35b-a3b)
- [Original refusal-direction paper](https://arxiv.org/abs/2406.11717)
- [Implementation linked by huihui-ai](https://github.com/Sumandora/remove-refusals-with-transformers)

The publisher warns that safety filtering is reduced and recommends controlled research use. “Abliterated” means refusal-reduced, not zero-refusal, correct, legal or harmless.

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Need help with cloud GPUs, self-hosting or app integration? [Talk on Signal](https://signal.me/#p/+13103408213) or [explore self-hosting](https://abliterated.cloud/#workflow).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
