# Ornith 35B: can self-scaffolding survive abliteration?<!-- READING-TLDR -->

## TL;DR

- DeepReinforce trained Ornith to propose a problem-solving scaffold and work inside it.
- YuYu1015 replaced the first edited weights after reporting reasoning damage.
- YuYu1015 reported roughly 5% hard refusals for its corrected Ornith 35B derivative on its own tests.

## Basically, the facts

**Ornith’s unusual idea: learn the harness too**

Basically, DeepReinforce trained Ornith to propose a problem-solving scaffold and then solve inside it.

**A middleweight MoE with a large address book**

Basically, Ornith 35B stores over 35 billion BF16 parameters and selects eight routed experts per token.

**The first edit was not good enough**

Basically, YuYu1015 replaced Ornith's edited weights in June 2026 after reporting reasoning damage.

**Sampling is part of the model**

Basically, YuYu1015 warns that a 1.05 repetition penalty can truncate Ornith's output.

**Who stands behind the two stages?**

Basically, DeepReinforce created upstream Ornith; YuYu1015 published the refusal-reduced derivative.

**What we can and cannot conclude**

Basically, YuYu1015's corrected Ornith still had roughly 5% hard refusals in the publisher's tests.

**The idea, in plain words**

Basically, Abliteration projects a refusal-linked direction out of selected model weights.
<!-- /READING-TLDR -->

Published 18 July 2026. Exact artifact: `YuYu1015/YuYu1015-Ornith-1.0-35B-abliterated`, revision `86065d1a9008773086a177637d54ec6dc2a56cbf`.

DeepReinforce trained upstream Ornith around “self-scaffolding”: the model proposes a problem-solving scaffold, then solves inside it, with reinforcement-learning reward applied to both stages. The publisher reports 75.6 SWE-bench Verified, 50.4 SWE-bench Pro and 64.2 Terminal-Bench 2.1 for the upstream 35B checkpoint.

YuYu1015 produced a weights-only abliterated derivative. The first version reportedly damaged reasoning, so the publisher replaced the weights on 30 June 2026. For the corrected version, YuYu1015 reports hard refusals falling from roughly 99% to 5%, moralizing from roughly 95% to 14%, and GSM8K remaining at 80%. These are small publisher evaluations, not independent results. Upstream Ornith’s coding scores have not been rerun on the derivative.

The model contains 35,107,181,936 BF16 parameters, 40 layers, 256 routed experts, eight selected experts per token and a shared expert. It retains multimodal and structured-tool machinery plus thinking blocks. YuYu1015 strongly recommends repetition penalty 1.0 and warns that 1.05 can truncate output.

## The idea, in plain words

**Editing weights vs retraining a model** — Abliteration is surgery, not schooling: instead of feeding a model new training data, you find one direction in its internal math that correlates with refusal and project it out of the weights. No dataset, no GPU weeks. 'Weights-only' means nothing else about the model's learned behavior was touched — a much lighter intervention than a fine-tune.

Primary sources:

- [Exact model card](https://huggingface.co/YuYu1015/YuYu1015-Ornith-1.0-35B-abliterated)
- [Pinned artifact](https://huggingface.co/YuYu1015/YuYu1015-Ornith-1.0-35B-abliterated/tree/86065d1a9008773086a177637d54ec6dc2a56cbf)
- [Official Ornith article and benchmarks](https://deep-reinforce.com/ornith_1_0.html)
- [Upstream Ornith repository](https://huggingface.co/deepreinforce-ai/Ornith-1.0-35B)
- [Official Qwen architecture card](https://huggingface.co/Qwen/Qwen3.5-35B-A3B)

The publisher’s own numbers are not zero refusal, and architecture alone does not prove post-edit vision or tool quality.

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Want this model running for you, on a private cloud GPU or your own machine? [Request access on Signal](https://signal.me/#p/+13103408213) or [see how it works](https://abliterated.cloud/#how).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
