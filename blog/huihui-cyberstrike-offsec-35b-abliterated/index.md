# A pentesting model, with the refusals taken out<!-- READING-TLDR -->

## TL;DR

- CyberStrike's base card describes tool-call alignment with 300 examples.
- Huihui applied a refusal-direction weight edit to the CyberStrike fine-tune.
- Huihui’s CyberStrike derivative card reports neither refusal measurements nor a post-edit tool-call rerun.

## Basically, the facts

**A fine-tune that admits it didn’t add knowledge**

Basically, CyberStrike's base card describes targeted tool-call training, not a capability upgrade.

**Then huihui-ai took the refusals out**

Basically, Huihui's CyberStrike release applies a refusal-direction weight edit to the fine-tune.

**What abliterating a security model changes**

Basically, Resecurity's July 2026 analysis described CyberStrike-OffSec as a dual-use model.

**What the card does and doesn’t claim**

Basically, Huihui's CyberStrike card has no measured refusal rate or post-edit tool-call evaluation.

**The paper trail so far**

Basically, The CyberStrike article recorded a GGUF release after a user asked for the format.

**How we treat it**

Basically, Huihui's CyberStrike publisher warns that the model has significantly reduced safety filtering.

**The idea, in plain words**

Basically, CyberStrike's base card reports 18 correct tool calls out of 24 after targeted training.
<!-- /READING-TLDR -->

Published 10 August 2026. Exact artifact: `huihui-ai/Huihui-CyberStrike-OffSec-35B-abliterated`, revision `01521758ee85df1ed4edaf494c48e20704b80204`.

CyberStrike-OffSec-35B is a fine-tune of Qwen3.6-35B-A3B built by Orhan Yıldırım (oyildirim) to emit structured tool calls for the CyberStrike offensive-security harness. Its card calls the work “a small, targeted alignment, not a capability upgrade”: a 300-example dataset that fixed the tool-call collapse of the previous model, which had hallucinated whole engagements. On 10 August 2026, huihui-ai abliterated the fine-tune — a refusal-direction weight edit per Arditi et al., implemented as a crude proof of concept with remove-refusals-with-transformers — and restored the Qwen3.6 MTP module: 35,951,822,704 parameters versus the fine-tune’s 35,107,181,936.

The base’s A/B tool-call evaluation (18/24 genuine structured calls versus the previous model’s 0/24) is an upstream claim; the abliterated card publishes no refusal-rate measurement and no post-edit rerun. Third-party coverage (Resecurity, 30 July 2026) treats the OffSec model as dual-use: local GGUF execution without telemetry, weights that “lower the skill floor for adversaries.”

## The idea, in plain words

**How a model learns to call tools instead of guessing** — Base models often hallucinate function calls. Supervised fine-tuning (SFT) fixes that with examples: here, a ~300-example dataset taught the model to emit structured tool calls, and the base card measured the difference — 18 of 24 correct tool calls after, 0 of 24 before. That's what 'tool-calling' means in practice: the model doesn't know tools, it was shown when and how to call them.

Primary sources:

- [Exact model card](https://huggingface.co/huihui-ai/Huihui-CyberStrike-OffSec-35B-abliterated)
- [Pinned artifact](https://huggingface.co/huihui-ai/Huihui-CyberStrike-OffSec-35B-abliterated/tree/01521758ee85df1ed4edaf494c48e20704b80204)
- [CyberStrike-OffSec-35B card](https://huggingface.co/oyildirim/CyberStrike-OffSec-35B) and [EVALUATION.md](https://huggingface.co/oyildirim/CyberStrike-OffSec-35B/blob/main/EVALUATION.md)
- [Resecurity: When AI Becomes the Attacker](https://www.resecurity.com/blog/article/when-ai-becomes-the-attacker-understanding-autonomous-offensive-security-agents)
- [Official Qwen3.6-35B-A3B card](https://huggingface.co/Qwen/Qwen3.6-35B-A3B)
- [Refusal-direction paper](https://arxiv.org/abs/2406.11717) and [implementation linked by huihui-ai](https://github.com/Sumandora/remove-refusals-with-transformers)
- [HF discussion: “GGUF of this model is needed”](https://huggingface.co/huihui-ai/Huihui-CyberStrike-OffSec-35B-abliterated/discussions/1) and [GGUF repo](https://huggingface.co/huihui-ai/Huihui-CyberStrike-OffSec-35B-abliterated-GGUF)
- [Creator posts on LinkedIn](https://www.linkedin.com/posts/orhan-yildirim_cybersecurity-penetrationtesting-opensource-activity-7440165985984204800-ow_a)
- [r/AgenticCybersecurity thread](https://www.reddit.com/r/AgenticCybersecurity/comments/1vi8hji/oyildirimcyberstrikeoffsec35b_hugging_face_i_dont/) and [r/Pentesting thread](https://www.reddit.com/r/Pentesting/comments/1qu4zbq/i_built_a_pentesting_platform_that_lets_al/) — linked, not quoted; Reddit blocked access at research time

The publisher warns that safety filtering is significantly reduced. “Abliterated” means refusal-reduced — not authorized, not legal, and not harmless.

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Want this model running for you, on a private cloud GPU or your own machine? [Request access on Signal](https://signal.me/#p/+13103408213) or [see how it works](https://abliterated.cloud/#how).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
