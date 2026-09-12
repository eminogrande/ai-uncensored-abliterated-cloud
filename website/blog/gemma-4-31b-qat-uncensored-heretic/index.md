# Gemma 4 31B, uncensored from the QAT checkpoint<!-- READING-TLDR -->

## TL;DR

- Google's Gemma 4 31B is a 30.7-billion-parameter dense model from March 2026; a Q4_0 quantisation-aware checkpoint followed on 28 April.
- Four months of Heretic edits have uncensored it: coder3101's April run reports 15 of 100 refusals, wnfldchen's August rebuild 8 of 100 at KL 0.0900.
- OS-Software's September build reports 0 of 100 refusals at KL 0.0083, made with a development build of Heretic (v2.0.0.dev0).
- The uncensored pack is a 17.29 GB Q4_0 GGUF plus a 0.81 or 1.20 GB vision projector; no GPU was rented and no dated rental quote is claimed.

## Basically, the facts

**What Gemma 4 31B is**

Basically, Google's Gemma 4 31B arrived in March 2026; the Q4_0 quantisation-aware checkpoints followed on 28 April.

**The April edit: 15 of 100 refusals**

Basically, coder3101's April Heretic edit reports Gemma 4 31B refusals down from 99 to 15 of 100, at KL 0.0434.

**The August rebuild: 8 of 100, reproducible**

Basically, wnfldchen's August QAT-checkpoint run reports 8 of 100 refusals and ships a reproduction kit with its trial pinned.

**September: 0 of 100 with a Heretic development build**

Basically, OS-Software's September Gemma 4 31B build reports 0 of 100 refusals at KL 0.0083, using a Heretic development build.

**The requant week**

Basically, All three Heretic edits drew requants within days, from a 4-bit EXL3 conversion to same-parameter republications.

**How to run it**

Basically, The uncensored Gemma 4 31B ships as a 17.29 GB Q4_0 file plus a vision projector, sized for a single 24 GB GPU.

**The idea, in plain words**

Basically, Gemma 4's QAT checkpoints are trained to stay close to bfloat16 quality at 4 bits, and uncensored copies inherit that.
<!-- /READING-TLDR -->
<!-- ARTICLE-META-MD -->
_Published 12 September 2026 · 11 min read · Canonical: https://abliterated.cloud/blog/gemma-4-31b-qat-uncensored-heretic/_
<!-- /ARTICLE-META-MD -->

*Published 12 September 2026 · Revision-pinned · Primary sources only*

**Model:** [OS-Software/gemma-4-31B-it-qat-q4_0-uncensored-heretic-GGUF](https://huggingface.co/OS-Software/gemma-4-31B-it-qat-q4_0-uncensored-heretic-GGUF) · pinned revision `c0fa1000…38a13518` (created 8 September 2026, 04:06 UTC) · weight-level sibling: [OS-Software/gemma-4-31B-it-qat-q4_0-unquantized-uncensored-heretic](https://huggingface.co/OS-Software/gemma-4-31B-it-qat-q4_0-unquantized-uncensored-heretic) (13 safetensors shards, 03:43 UTC)
**Base:** [google/gemma-4-31B-it-qat-q4_0-unquantized](https://huggingface.co/google/gemma-4-31B-it-qat-q4_0-unquantized) (28 April 2026) · 30.7 billion dense parameters, 60 layers, 256,000-token context, text and image input · Apache 2.0 · no dated rental quote in this article

Gemma 4 31B might be the most repeatedly uncensored model of 2026. This year alone it has collected an April edit by coder3101, a reproducible August rebuild by wnfldchen, and a separate line from Madras1, all aimed at the same thing: taking the refusals out of Google's 30.7-billion-parameter flagship open model. The newest release, published on 8 September 2026 by the Hugging Face label OS-Software, is made against Google's Q4_0 quantisation-aware checkpoint with a development build of Heretic, and its card reports the sharpest numbers yet: 0 of 100 refusals claimed against 100 of 100 for the stock checkpoint, at a KL divergence of 0.0083.

## What Gemma 4 31B is

Gemma 4 31B arrived in March 2026 as the largest dense tier of Google's Gemma 4 family, and it is the tier this site would point a single-GPU reader at first: 30.7 billion parameters across 60 layers, a 256,000-token context, text and image input through a vision encoder of roughly 550 million parameters, and a hybrid attention stack that interleaves sliding-window attention of 1,024 tokens with global layers using unified keys and values and proportional RoPE. The card lists configurable thinking modes, native system prompt support and 140-plus languages, and the license is Apache 2.0 through the Gemma 4 license page. At fetch time the instruction-tuned release carried 3,768 likes and 8,676,676 downloads, which makes it the most popular uncensoring target Google has shipped this year.

Then came the quantisation-aware re-release. From late April 2026, Google republished the family as QAT checkpoints, described on the card as trained to keep quality close to bfloat16 at a fraction of the memory, in four shapes: GGUF Q4_0 for deployment, compressed-tensors W4A16 for vLLM, a mobile wNa8o8 schema, and the interesting one for editors, the unquantized Q4_0 checkpoints: half-precision weight sets pulled out of the QAT pipeline and published for exactly this kind of downstream work, in the card's own words, "ideal for custom downstream compilation and research". The 31B unquantized QAT checkpoint went up on 28 April 2026 and sat at 42 likes and 10,438 downloads when this article was researched. Three of the edits below end up editing it, because weights that were trained to survive 4-bit compression are weights whose uncensored copies can still ship small.

## The April edit: 15 of 100 refusals

The line starts before the QAT checkpoints existed. coder3101's repository, created on 2 April 2026, decensored the plain `google/gemma-4-31B-it` weights with Heretic v1.2.0 and the Arbitrary-Rank Ablation method the tool had just gained, with row-norm preservation. The selected intervention ran across the whole stack, layers 1 through 59, with a behavior-preservation weight of 0.8438, a steering weight of 0.0002, an overcorrection weight of 1.0760 and 15 neighbors. The card's numbers: a KL divergence of 0.0434 and refusals at 15 of 100, against 99 of 100 for the stock model on the same screen. Both are publisher measurements, like every refusal number in this article.

The edit became the reference point for the model. At fetch time it carried 75 likes and 8,906 downloads, the strongest community response of any 31B uncensor in this scan, and the September derivatives below borrow it as a base. coder3101 also edited the small sibling in June: the E4B edit reports 5 refusals of 100 against 98 of 100 for its stock checkpoint, at KL 0.0065, and it is the artifact a newer Q4_0 requant targets this week.

## The August rebuild: 8 of 100, reproducible

The second editor brought infrastructure. wnfldchen published a Heretic adapter in July and then, on 14 August 2026, a merged checkpoint plus a deployment variant in W4A16 compressed-tensors format. This run targeted `google/gemma-4-31B-it-qat-q4_0-unquantized`, pinned to base commit `1e4d8bee…87bf311f`, making it the earliest QAT-checkpoint edit this scan found. The optimizer picked trial 6 of its search: attention output projections only, an arbitrary-rank ablation of 256, layers 24 through 54, with a preservation weight of 0.1182 and a steering weight of 0.0050. The performance table reads 8 of 100 refusals against 99 of 100 for the stock checkpoint, at KL 0.0900, and the repository ships a reproduction kit with the trial journal, pinned prompt datasets and export settings, so the run can be checked rather than trusted.

The W4A16 variant is the one artifact in this line with a published capability table, and it is honest about the cost of the edit. Against Google's official W4A16 base, PIQA drops 0.71 points, WinoGrande 0.16 and CommonsenseQA 0.16, which the card notes are "smaller than their standard errors", while EQ-Bench moves up 4.05 points with parseability down 4.68. That is what a decent automatic run looks like: refusals far down, benchmarks roughly flat, one generative metric visibly shifted.

## September: 0 of 100 with a Heretic development build

OS-Software is a Hugging Face label whose catalog held 32 models at fetch time and leans on Japanese-targeted Heretic edits, including an earlier gemma-4-12B and gemma-4-26B-A4B line; this site's Hy-MT2 translation-model coverage in August listed their GGUF quants of that edit. Their September week reads like a small production line. On 7 September 2026 they published a third iteration of the 12B QAT uncensor (552 downloads at fetch) and a second iteration of the 26B A4B (438). On 8 September, at 03:43 UTC, the weight-level 31B repository went up; twenty-three minutes later, at 04:06 UTC, the GGUF repository followed with a Q4_0 file and two vision projectors. On 11 September they added an expert-pruned 26B A4B variant, with the card stating that prunings below 72 experts per layer were omitted because they could not maintain acceptable quality.

The 31B card names its tool as Heretic v2.0.0.dev0+custom, a development build ahead of the newest public release, v1.4.0 from 14 June 2026, and the parameter table reads like a different generation of the tool than the runs above. It edits layers 30 through 41 of the 60-layer stack, targeting attention output and MLP down projections, with a Gaussian transport step of rank 4 and entropy regularization 0.1, a rank-128 LoRA merge, covariance regularization 0.01, a maximum weight change of 1.0, a behavior-preservation weight of 1.0 against a steering weight of 0.0001, and no row normalization. The performance table: refusals at 0 of 100 against 100 of 100 for the stock checkpoint, at KL 0.0083.

Set the two QAT-checkpoint numbers side by side and the interesting claim is not the refusal count. In August the same checkpoint measured 8 of 100 at KL 0.0900; in September it measures 0 of 100 at 0.0083, roughly a tenth of the drift while claiming fewer refusals. If the card is right, the improvement came from the tool's development line rather than from the model, and the bar for these edits is moving in both directions at once. That is why the version string on the card is worth more attention than the zero.

## The requant week

Whatever the tool version, this line gets copied quickly. On 8 September, hours after OS-Software's release, an EXL3 conversion of coder3101's April edit appeared at 4.00 bits per weight. On 12 September a requant of the September build went up under a different account whose card repeats the identical parameter table, down to the same ridge constant, the mirror pattern this site noted on the DeepSeek V4.1 day-one coverage. The E4B edit got the same treatment: a Q4_0 requant of coder3101's June run landed on 11 September, the same day a separate editor, Alfredofrog, published his own E4B decensor claiming refusals at 7 of 100 against 99 of 100, at KL 0.0043, editing only the attention output projections across layers 8 through 36.

And there is a fourth line for readers who track formats rather than tools. On 6 September, Madras1 published Gemma-4-31B-Abliterated-Uncensored, a classic weight-orthogonalization edit rather than a Heretic run: a dual-subspace projection at alpha 1.35 across layers 12 to 51, touching output, down and gate projections, with a 30-prompt refusal suite described on the card and detailed breakdowns promised in a companion repository. Its mradermacher conversion chain, static and imatrix quants posted the same day, gathered 6,495 and 3,407 downloads by fetch time, the largest numbers any single recent Gemma 4 31B uncensored artifact in this scan collected.

## How to run it

The release shape is friendly. OS-Software's Q4_0 file measures 17,287,669,696 bytes, about 17.29 GB, with a vision projector at 1,200,726,080 bytes in BF16 or 809,541,440 bytes in Q8_0; the two-file pattern that llama.cpp-family runtimes expect for multimodal GGUF. Google's own Q4_0 GGUF release for this tier, published on 1 May 2026 and sitting at 477,215 downloads, ships the same pair of files, so the uncensored pack rides a format the stock model already proved. The weight-level sibling comes as 13 safetensors shards for custom pipelines, and the 12B and 26B A4B QAT GGUFs from the same week cover smaller cards; the E4B requant's card pitches a roughly 4 GB Q4_0 file for phones and laptops.

Where it fits: about 18.1 GB of weight files plus context, which is tight but workable on a 24 GB card and comfortable inside a 40 GB one. This site does not serve Gemma 4 31B, and no dated rental quote appears in this article; the documented reference is a stopped A100 40 GB Vast.ai instance from the 5 September snapshot, and no GPU was rented, started or billed for this piece. If you want one number to carry away, it is this: a 30.7-billion-parameter flagship now has an uncensored build that runs in the same footprint a 24 GB card handles for the stock model.

## One honest line

Every refusal count and KL value here is a publisher's own measurement on Heretic's 100-prompt screen, a low KL shows small drift rather than preserved capability, the guardrails these edits remove were real, and nothing in this article was independently reproduced: no GPU was rented, no inference was run, and the numbers belong to the cards until someone checks them.

## The idea, in plain words

**What abliteration is.** A refusal is not a switch inside a model; it behaves like a direction in the model's internal activations, and abliteration is the practice of finding that direction and subtracting it, either baked into the weights, where it is permanent and travels with the file, or applied at runtime with a scaled projection. Heretic automates the search for where in the stack and how strongly to intervene, scoring each candidate on two numbers: how many harmful prompts still get refused, and the KL divergence, which measures how far the edited model's output distribution has drifted from the original's on harmless text. The tension you are watching across this article, refusals against KL, is the whole game of automatic uncensoring.

**Why "QAT" keeps appearing in the file names.** Google trained the late-2026 Gemma 4 checkpoints with quantization-aware training, described on the card as "preserving similar quality to bfloat16 while dramatically reducing the memory requirements", then published the half-precision weights "extracted from the QAT pipeline" as the unquantized checkpoints for downstream work. An edit made on those weights inherits the training that teaches the model to tolerate 4-bit compression, which is why September's uncensored release can ship as a single 17.29 GB Q4_0 file that still claims bfloat16-like behaviour, instead of a half-precision checkpoint someone would have to quantise after the fact. The checkpoint choice is the quiet technical decision of this whole line.

*Coverage gaps: this article is built from Hugging Face model cards, repository files, file trees and the Hugging Face API, fetched 12 September 2026. All refusal counts, KL values and benchmarks are publisher-reported; none were independently reproduced, no GPU was rented and no inference was run for this article. Download and like counts are community signal, not measurement. Discussion threads on the anchor repository: none existed at fetch time. No dated rental quote is claimed.*

## Primary sources

- [OS-Software/gemma-4-31B-it-qat-q4_0-uncensored-heretic-GGUF (card: Heretic v2.0.0.dev0+custom parameter table, 0/100 refusals, KL 0.0083, GGUF files)](https://huggingface.co/OS-Software/gemma-4-31B-it-qat-q4_0-uncensored-heretic-GGUF) · [pinned revision `c0fa1000…38a13518`](https://huggingface.co/OS-Software/gemma-4-31B-it-qat-q4_0-uncensored-heretic-GGUF/tree/c0fa10008dcb1fe6ce9315284069d63138a13518) · [weight-level sibling](https://huggingface.co/OS-Software/gemma-4-31B-it-qat-q4_0-unquantized-uncensored-heretic) · [pinned `244246e6…d03e625b`](https://huggingface.co/OS-Software/gemma-4-31B-it-qat-q4_0-unquantized-uncensored-heretic/tree/244246e628015845fc3b1d0bb4e97549d03e625b)
- OS-Software line, same week: [12B v3 GGUF](https://huggingface.co/OS-Software/gemma-4-12B-it-qat-q4_0-uncensored-heretic-v3-GGUF) (`7e1f9bc1…7588bee6`) · [26B A4B v2 GGUF](https://huggingface.co/OS-Software/gemma-4-26B-A4B-it-qat-q4_0-uncensored-heretic-v2-GGUF) (`754b6d40…bdc88ac1`) · [26B A4B expert-pruned GGUF](https://huggingface.co/OS-Software/gemma-4-26B-A4B-it-qat-q4_0-heretic-japanese-pruned-GGUF) (`b58aca87…3a0e07b4`) · [OS-Software profile](https://huggingface.co/OS-Software)
- [coder3101/gemma-4-31B-it-heretic (card: Heretic v1.2.0 + ARA, layers 1-59, 15/100 vs 99/100, KL 0.0434)](https://huggingface.co/coder3101/gemma-4-31B-it-heretic) · [pinned `9a1c7f5d…363cd9e7`](https://huggingface.co/coder3101/gemma-4-31B-it-heretic/tree/9a1c7f5d851541f279cd104329e093cb363cd9e7) · [E4B edit (5/100 vs 98/100, KL 0.0065)](https://huggingface.co/coder3101/gemma-4-E4B-it-qat-q4_0-unquantized-heretic)
- [wnfldchen merged checkpoint (card: trial 6, ARA rank 256, 8/100 vs 99/100, KL 0.0900, reproduce directory)](https://huggingface.co/wnfldchen/gemma-4-31B-it-qat-q4_0-unquantized-heretic-merged) · [pinned `e9a15cd7…e38aef8e`](https://huggingface.co/wnfldchen/gemma-4-31B-it-qat-q4_0-unquantized-heretic-merged/tree/e9a15cd70afc35f049f1f790762b6eae38aef8e8) · [W4A16 variant with the capability table](https://huggingface.co/wnfldchen/gemma-4-31B-it-qat-w4a16-ct-heretic-merged-direct)
- Requants and mirrors: [sjoe1244 EXL3 4.00 bpw](https://huggingface.co/sjoe1244/gemma-4-31B-it-heretic-exl3-4.00bpw-h6) · [musafa901 Q4_0 requant](https://huggingface.co/musafa901/gemma-4-31B-it-qat-q4_0-uncensored-heretic-GGUF) · [guga112 E4B Q4_0 requant](https://huggingface.co/guga112/gemma-4-E4B-it-heretic-QAT-GGUF) · [Alfredofrog E4B edit (7/100 vs 99/100, KL 0.0043)](https://huggingface.co/Alfredofrog/gemma-4-E4B-it-uncensored-heretic)
- The parallel line: [Madras1/Gemma-4-31B-Abliterated-Uncensored (card: dual-subspace orthogonalization, alpha 1.35, layers 12-51)](https://huggingface.co/Madras1/Gemma-4-31B-Abliterated-Uncensored) · [mradermacher static quants](https://huggingface.co/mradermacher/Gemma-4-31B-Abliterated-Uncensored-GGUF) · [imatrix quants](https://huggingface.co/mradermacher/Gemma-4-31B-Abliterated-Uncensored-i1-GGUF)
- Upstream: [google/gemma-4-31B-it (official card, 11 March 2026)](https://huggingface.co/google/gemma-4-31B-it) · [Q4_0 quantisation-aware checkpoint (28 April 2026)](https://huggingface.co/google/gemma-4-31B-it-qat-q4_0-unquantized) · [pinned revision `1e4d8bee…87bf311f`](https://huggingface.co/google/gemma-4-31B-it-qat-q4_0-unquantized/tree/1e4d8beecacb8b7590c1d8bedd7335f687bf311f) · [official GGUF release (1 May 2026)](https://huggingface.co/google/gemma-4-31B-it-qat-q4_0-gguf)
- Tooling and method: [Heretic, fully automatic censorship removal (AGPL-3.0)](https://github.com/p-e-w/heretic) · [Arbitrary-Rank Ablation pull request](https://github.com/p-e-w/heretic/pull/211) · [heretic-project.org](https://heretic-project.org)
- HF API facts: [anchor derivative](https://huggingface.co/api/models/OS-Software/gemma-4-31B-it-qat-q4_0-uncensored-heretic-GGUF) · [QAT checkpoint](https://huggingface.co/api/models/google/gemma-4-31B-it-qat-q4_0-unquantized) · [April edit](https://huggingface.co/api/models/coder3101/gemma-4-31B-it-heretic)
- Prior coverage: [the Hy-MT2 translation-model decensor with OS-Software quants, 30 Aug 2026](https://abliterated.cloud/blog/tencent-hy-mt2-30b-a3b-uncensored/) · [the MiniCPM5-2B reproducible Heretic kit, 9 Sep 2026](https://abliterated.cloud/blog/minicpm5-2b-heretic-abliterated-reproducible/) · [the DeepSeek-V4.1-Flash day-one wave, 11 Sep 2026](https://abliterated.cloud/blog/deepseek-v4-1-flash-day-one-uncensoring/)

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Want this model running for you, on a private cloud GPU or your own machine? [Request access on Signal](https://signal.me/#p/+13103408213) or [see how it works](https://abliterated.cloud/#how).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
