# Qwythos has three lives: Qwen bones, 500M reasoning tokens and an abliterated refusal circuit<!-- READING-TLDR -->

## TL;DR

- Qwythos combines Qwen3.5-9B architecture, Empero reasoning training and Huihui abliteration.
- Empero reports smoke testing near 137K tokens, not across the configured million-token window.
- Huihui published no post-edit refusal test or benchmark rerun.

## Basically, the facts

**Life one: Qwen builds the skeleton**

Basically, Qwythos starts with dense Qwen3.5-9B architecture and occupies roughly 19.3 GB in BF16.

**Life two: Empero changes the behavior**

Basically, Empero says Qwythos learned from more than 500 million tokens of reasoning traces.

**The “1M” in the name**

Basically, Qwythos has a million-token setting, but Empero reports smoke testing only around 137K.

**Life three: huihui edits refusal again**

Basically, Huihui's Qwythos derivative has no published post-abliteration refusal test or benchmark rerun.

**A tiny tool-use demo, not a giant benchmark**

Basically, Empero reported seven successful tool-use prompts for upstream Qwythos, not Huihui’s later abliterated derivative.

**The people behind the lineage**

Basically, Qwythos combines Qwen architecture, Empero's reasoning fine-tune and Huihui's refusal edit.

**Why this is our inexpensive route**

Basically, The Qwythos article paired the small BF16 model with one L40S for experimentation.

**The idea, in plain words**

Basically, Qwythos's million-token label is a configured limit, not proof of reasoning quality at that length.
<!-- /READING-TLDR -->

Published 18 July 2026. Exact artifact: `huihui-ai/Huihui-Qwythos-9B-Claude-Mythos-5-1M-abliterated`, revision `efcc73cac15ff8fc5d46b8d41b53c22d571cf97d`.

Qwythos begins as dense Qwen3.5-9B architecture, then receives a full-parameter reasoning fine-tune from Empero, then goes through huihui-ai’s refusal-reduction process. The exact child has 9,653,104,368 BF16 parameters and occupies roughly 19.3 GB.

Empero says it trained the text backbone on more than 500 million tokens of Claude Mythos, Claude Fable and in-house reasoning traces. Its 100-example matched evaluation reports large MMLU and GSM8K gains, a small ARC gain, and a GPQA Diamond regression. The vision tower was frozen and not evaluated.

The model is configured for 1,048,576 tokens through static YaRN, but Empero reports smoke testing at roughly 137K. Our hosted profile therefore uses 131,072. The million-token label is configuration, not proof of million-token reasoning quality.

Huihui publishes no post-abliteration refusal test or benchmark rerun. Empero’s numbers belong to the pre-edit checkpoint.

## The idea, in plain words

**Why a 1-million-token context is a big deal** — Attention — the mechanism that lets a model connect what it reads — grows quadratically with length. Reading a million tokens means the model has to hold a whole book series in working memory at once, and every new token re-checks against all of them. That's why '1M' is a configured ceiling, not a promise that quality stays flat all the way up.

Primary sources:

- [Exact Huihui model card](https://huggingface.co/huihui-ai/Huihui-Qwythos-9B-Claude-Mythos-5-1M-abliterated)
- [Pinned artifact](https://huggingface.co/huihui-ai/Huihui-Qwythos-9B-Claude-Mythos-5-1M-abliterated/tree/efcc73cac15ff8fc5d46b8d41b53c22d571cf97d)
- [Empero Qwythos card, training and evaluations](https://huggingface.co/empero-ai/Qwythos-9B-Claude-Mythos-5-1M)
- [Official Empero site](https://empero.org/)
- [Official Qwen3.5-9B repository](https://huggingface.co/Qwen/Qwen3.5-9B)
- [Original refusal-direction paper](https://arxiv.org/abs/2406.11717)

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Want this model running for you, on a private cloud GPU or your own machine? [Request access on Signal](https://signal.me/#p/+13103408213) or [see how it works](https://abliterated.cloud/#how).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
