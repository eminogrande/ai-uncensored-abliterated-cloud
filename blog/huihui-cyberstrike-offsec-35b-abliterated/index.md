<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# A pentesting model, with the refusals taken out

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
