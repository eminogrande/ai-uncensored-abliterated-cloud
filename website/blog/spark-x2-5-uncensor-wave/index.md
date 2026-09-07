# Day ten for Spark X2.5: the uncensor wave on the 1M-context 4B<!-- READING-TLDR -->

## TL;DR

- Spark X2.5's vendor claims up to 1M tokens of native context; community reproduction was unresolved.
- soyaakinohara reported 3/100 refusals for the 4B edit, down from 58/100 on the base.
- darioooooo0o reported no real refusals in 337 Spark 1.7B generations; flagged outputs were manually audited.

## Basically, the facts

**Day ten**

Basically, Spark X2.5's first 1.7B uncensor appeared on 3 September 2026, ten days after the base.

**What Spark X2.5 is**

Basically, Spark X2.5's vendor claims 1M-token context, but community tests had not reproduced it.

**The wall of no**

Basically, soyaakinohara measured 58 refusals in 100 prompts on the stock Spark X2.5 4B.

**Two edits, one argument about rulers**

Basically, darioooooo0o argues that short keyword tests misread Spark X2.5's thinking traces.

**How to run it**

Basically, Spark X2.5 GGUF builds used the vendor's llama.cpp fork at publication.

**The creator: XHToken (SparkLLM)**

Basically, XHToken publishes Spark's runtime tools as well as the model weights.

**The editors: soyaakinohara and darioooooo0o**

Basically, soyaakinohara's Spark release paired an uncensored base with a Japanese-tuned version.

**The idea, in plain words**

Basically, Spark X2.5 mixes full-attention layers with roughly three times as many sliding-window layers.
<!-- /READING-TLDR -->

*Published 6 September 2026 · Revision-pinned · Primary sources only*

**Model:** [soyaakinohara/Spark-X2.5-4B-Heretic](https://huggingface.co/soyaakinohara/Spark-X2.5-4B-Heretic) · pinned revision `d9cbf6a0…67c6b91b`; sibling ablation [darioooooo0o/Spark-X2.5-1.7B-Abliterated-GGUF](https://huggingface.co/darioooooo0o/Spark-X2.5-1.7B-Abliterated-GGUF) `0193e8f9…d8f6c6c5`
**Base:** [XHToken/Spark-X2.5-4B](https://huggingface.co/XHToken/Spark-X2.5-4B) and [1.7B](https://huggingface.co/XHToken/Spark-X2.5-1.7B) (Apache-2.0, 24 Aug 2026) · 4,112,079,360 / 1,707,657,216 params · hybrid attention (one full-attention layer per three sliding-window layers) · up to 1M-token native context (vendor claim) · BF16 ≈ 7.7 GiB · ≈ $2.34/h managed BF16-class (1 × L40S); Q4_K_M 2.5 GiB on an 8 GB card, 1.7B Q4 ~1.0 GB

On 24 August 2026, XHToken's SparkLLM team published two compact Apache-2.0 models, Spark-X2.5-4B and Spark-X2.5-1.7B, with a hybrid-attention design that gives a 4.1B model a 1M-token native context and agent scores its vendor places above 9B and 12B rivals. The stock checkpoints refuse hard: one editor measured 186 refusals out of 300 sealed prompts on the 1.7B. Ten days after the drop, two independent editors shipped measured uncensors of both sizes, one full-precision BF16 merge and one GGUF ablation ladder, and then spent the rest of the week arguing about how to count a refusal on a thinking model at all.

## Day ten

The base is XHToken/Spark-X2.5-4B, created 24 August 2026 at 06:34 UTC, 4,755 downloads and 558 likes inside its first thirteen days, Apache-2.0, with a 1.7B sibling. XHToken is the Hugging Face home of SparkLLM, the company behind the Spark model family; its profile describes the org as building general-purpose foundation models and professional AI agent products, and its card lists the socials a serious vendor lists: Slack, Discord, YouTube, Bluesky, X, Zhihu. The ecosystem response was immediate. The [official GGUF repo](https://huggingface.co/XHToken/Spark-X2.5-4B-GGUF) (28 August) sits at 18,982 downloads today; by 2 September a dozen independent quant packs had joined it, with abenzerps's at 8,158 and darioooooo0o's at 2,234 and 1,933 downloads.

Then the uncensors. [darioooooo0o/Spark-X2.5-1.7B-Abliterated-GGUF](https://huggingface.co/darioooooo0o/Spark-X2.5-1.7B-Abliterated-GGUF) went up 3 September at 10:44 UTC, ten days and four hours after the base appeared. [soyaakinohara/Spark-X2.5-4B-Heretic](https://huggingface.co/soyaakinohara/Spark-X2.5-4B-Heretic), the full-precision BF16 edit of the 4B, followed the next morning at 02:08 UTC, with a Japanese-adapted twin and a GGUF ladder an hour earlier. A third, same-day GGUF pack ([SC117](https://huggingface.co/SC117/Spark-X2.5-4B-abliterated-FIT-GGUF)) carries "abliterated" in its name but names the untouched *Base* checkpoint as its quantization source, so read that card before you trust the label. Four days, three publishers, one base family: that is the pace this site exists to record, and this time the edits came with measurements worth arguing about.

## What Spark X2.5 is

Spark-X2.5 is a text-only, dense, thinking-model line aimed squarely at on-device and edge agents. The vendor card's architecture claims, quoted straight: a hybrid attention design that combines one full-attention layer with three sliding-window attention layers, cutting the compute and KV-cache cost of long context; a native context window of up to 1M tokens, trained in a dedicated long-context stage of hundreds of billions of tokens; support for more than 200 languages; roughly 20 trillion pretraining tokens; and post-training that consolidates domain-specialized RL teacher policies through MOPD. The models were trained on Huawei Ascend clusters. Custom model code ships with every derivative (`configuration_spark.py`, `modeling_spark.py`, `trust_remote_code=True`), and the vendor maintains its own llama.cpp fork, MLX build and Spark-plugin for serving.

The vendor's benchmark table compares both sizes against Qwen3.5-9B/4B/2B and Gemma-4-12B/E4B/E2B (upstream claims, straight from the card; asterisked cells are the vendor's own marks for numbers reported elsewhere, and nothing here is independently reproduced):

| Benchmark | Spark-X2.5-4B | Qwen3.5-9B | Gemma4-12B |
|---|---|---|---|
| τ³-bench (agent) | **30.4** | 9.3 | 13.3 |
| MCP-Atlas | **54.6** | 47.4* | 30.5* |
| BFCL-V4 | 65.1 | 66.1* | 37.4 |
| τ²-bench | 75.1 | 79.1* | 69.0* |
| SWE-Bench Multilingual | **53.3** | 43.3 | 32.5* |
| AIME 2026 | **90.7** | 88.2 | 82.1* |
| HMMT Feb 2026 | **81.2** | 70.8 | 65.6 |
| BrowseComp | **40.9** | 8.3 | 10.0 |

Read those the way the vendor writes them: a 4.1B model claiming to out-agent 9B and 12B competitors on multi-turn tool work (τ³-bench 30.4 is more than three times Qwen3.5-9B's 9.3), while the 1.7B quietly beats the 9B on BrowseComp. Scepticism is healthy and the community is exercising it: the GitHub org's issue tracker for Spark-X2.5 currently holds an open thread asking for an official reproduction config because NeedleBench-style 1M-token tests did not reproduce, plus threads on vLLM startup failures and on upstream llama.cpp not supporting the architecture. The 1M context and the 200-language claims come with vendor asterisks attached, and this article keeps them labeled.

## The wall of no

What makes this release interesting to this site is not the marketing table. It is what the stock models do under pressure, measured by the people who uncensor for a hobby. darioooooo0o ran the 1.7B against a marker suite of 3,911 unique harmful prompts and counted 2,014 refusals, 51.5%, before any edit. On a sealed multilingual set of 200 prompts across 7 languages, the stock 1.7B refused 86, 43%; on a sealed English set of 100 adversarial prompts it refused all 100. soyaakinohara's separate measurement of the 4B counted 58 refusals out of 100 on his own suite. These are small models, sized for laptops and edge boxes, and they refuse like models ten times their weight: the RL-heavy post-training that made them agent-competitive also made them extremely reluctant. That combination, capable on-device agent plus heavy refusal behavior, is exactly the combination the uncensor community cannot leave alone.

## Two edits, one argument about rulers

[soyaakinohara's 4B edit](https://huggingface.co/soyaakinohara/Spark-X2.5-4B-Heretic) is the clean one: full-precision BF16 merge, Heretic refusal attenuation, measured 58 → 3 refusals out of 100 at KL divergence 0.0118, the base revision pinned in the card (`1e4c2477…`), no capability fine-tune on top. It is the starting weight for his Japanese-adapted release, which adds continued training on Japanese wiki data and a Japanese tool-calling set, and the whole family ships a GGUF ladder from BF16 at 7.7 GiB down to Q4_K_M at ~2.5 GiB, the smallest rung explicitly verified for full think-to-answer output. His rig for the job, disclosed on the card: two RTX 5060 Ti 16 GB cards and 32 GB of RAM with swap.

[darioooooo0o's 1.7B ablation](https://huggingface.co/darioooooo0o/Spark-X2.5-1.7B-Abliterated-GGUF) is the argumentative one, and it is the most honest refusal measurement this site has seen in weeks. Method: a single-round rank-1 refusal-direction ablation (heretic) over a frozen, manifest-hashed pool of 6,292 prompts, multilingual, balanced so every language family gets equal votes, with the winning configuration picked as trial 33 of a 50-trial Optuna search. Results are reported on sealed sets the editor never trained or trial-scored against: 300 sealed generations plus 37 answer-level generations, every flagged output audited by eye. Headline: 0 real refusals, against a stock model that refused 186 of those same 300 prompts. The 21 regex flags on the sealed sets all turned out to be complying answers whose reasoning traces contained words like "illegal". Average refusal preamble length collapsed from 247 to 96 characters on the multilingual set and from 435 to 145 on the English one.

Then the essay. Standard refusal evals generate ~100 tokens and string-match for "sorry" or "as an AI"; on a thinking model, darioooooo0o argues, that ruler fails in two opposite directions at once, because 100 tokens never exit the thinking trace, so compliance-planning thoughts get flagged while genuine non-answers score as neither refusal nor compliance. His ruler: 600+ token generations, thinking split from the answer on `</think>`, every generation bucketed as complied, refused or non-answer, everything flagged audited by eye. His closing line, aimed at the whole release genre: anyone comparing a "0/300" bucket count against a marker-count "0/465" is comparing different rulers. Demand the bucket table. Both editors' numbers above are bucket counts, and the 1.7B's marker matrix still dropped from 51.5% to 6.7% after the edit, which he prints for comparability while telling you not to trust it.

## How to run it

There is no Ollama page for this model yet, and upstream llama.cpp does not support the architecture as of writing, so the runnable paths are the vendor fork and transformers:

**Local GGUF (both sizes).** Serve with the vendor's llama.cpp fork ([github.com/XHToken/llama.cpp](https://github.com/XHToken/llama.cpp), `spark2_5` arch). The 1.7B ablation ladder runs Q8_0 ~1.8 GB down to IQ4_XS ~0.9 GB; darioooooo0o's card is explicit that `--reasoning-budget` is load-bearing, because median thinking length is 1,500+ tokens:

```sh
llama-server -m Spark-X2.5-1.7B-Abliterated-Q4_K_M.gguf \
  --chat-template-file chat_template.jinja \
  -c 65536 -n 4096 -ngl 99 -fa on -ctk f16 -ctv f16 \
  --temp 1.0 --top-p 0.95 --reasoning-budget 2000 \
  --jinja --reasoning-format deepseek
```

**Full precision.** soyaakinohara's BF16 merges load in transformers with `trust_remote_code=True`; his card shows the chat-template call with `enable_thinking=False` for plain answers, and notes thinking mode needs 1024+ generated tokens. The 4B at BF16 is ~7.7 GiB, the Q8_0 ~4.1 GiB, the Q4_K_M ~2.5 GiB.

**Hosted.** ABLITERATED.cloud's approximate managed price estimate for the BF16-class model is ≈ $2.34/h on a single L40S-class GPU; the Q4 rungs run on an 8 GB consumer card and the 1.7B fits in a gigabyte. Treat the estimate as a managed-hosting ballpark, not a quote.

## The creator: XHToken (SparkLLM)

The vendor behind the base is XHToken, the Hugging Face account of SparkLLM, which describes itself as focused on general-purpose foundation models and professional AI agent products built around its proprietary Spark model family. The Spark-X2.5 card is the company's own: 4B and 1.7B, Apache-2.0, trained on Ascend, tooled for Codex, Claude Code, OpenClaw and Hermes. XHToken publishes the runtime stack itself, a llama.cpp fork, an MLX build, a Spark-plugin and LlamaFactory/vLLM/SGLang forks under one GitHub org, and its Spark-X2.5 repository (152 stars at writing) runs an open Edge-Agent challenge alongside the bug reports. The social layer is real: X, Bluesky, YouTube, dev.to, Zhihu, Slack and Discord, plus a WeChat channel. No donation links, no Ko-fi: this is a company release with company support channels, which is rarer in the uncensor ecosystem than it should be.

## The editors: soyaakinohara and darioooooo0o

soyaakinohara's profile reads "LLMとか", Japanese for "LLMs and such", which undersells a catalog built around a specialty: low-bit abliterated quants sized to fit 12–16 GB GPUs, plus Japanese adaptation. His qwen3.8-27b abliterated 3.69bpw MTP GGUF has 31,946 downloads; his Gemma-4-31B Heretic sits at 3.68 bpw for 14 GB cards. The Spark release follows the house pattern, an uncensored base weight plus a Japanese-tuned twin plus a full GGUF ladder, and by the morning this article went up he had already moved on to a Heretic of the newly released K2-Horizon-32B. No socials, no donation address on the profile: the catalog is the brand, same as most of the people this site covers.

darioooooo0o is the quant-ladder maker turned measurement maximalist: he shipped the early Spark-X2.5 GGUF packs (2,234 and 1,933 downloads before the abliteration), then the ablation, then a methodology essay that belongs in the genre's canon. His profile links an X account, @imdariotoo. He also quantized the new K2-Horizon family the same week, which suggests a workflow: when a fresh Apache-2.0 base lands with a big quant wave behind it, he runs the ladder, then he runs the ruler.

## One honest line

Safety filtering is significantly reduced on both edits, which is the whole point of a day-ten uncensor on an agentic model, so anything you have it do, you own.

## The idea, in plain words

**Hybrid sliding-window attention.** Full attention lets every token look at every earlier token, which is why long prompts get expensive so fast: the cost grows with the square of the context length. A sliding-window layer only lets each token look at a fixed-size neighborhood behind it, so cost stays flat no matter how long the prompt grows. Spark-X2.5 interleaves the two, roughly one full-attention layer for every three window layers, so the model keeps the ability to look anywhere when it needs to while most of its layers run at window cost. That is how a 4.1B model can claim a 1M-token native context without a 1M-token memory bill, and it is also why the community is asking for reproduction configs: the architecture is new enough that the marketing numbers still need proving.

*Coverage gaps: Reddit was unreachable from this machine (HTTP 403), and the general web-search backend was down at writing time, so no independent press or community-thread coverage was fetched; community signal here comes from the vendor GitHub org's issue tracker and quant download counts. The Hugging Face discussions API returned no threads on the base repo at writing time. Benchmarks are vendor card claims (asterisked cells are the vendor's own marks, none independently reproduced); refusal numbers are editor measurements on editor sets, reported with their rulers. SC117's same-day "abliterated" GGUF names the unedited Base checkpoint as its quantization source and is not counted as a verified uncensor here.*

## Primary sources

- [XHToken/Spark-X2.5-4B (model card, architecture, vendor benchmarks, 24 Aug 2026)](https://huggingface.co/XHToken/Spark-X2.5-4B)
- [soyaakinohara/Spark-X2.5-4B-Heretic (card, method, refusal audit, pinned base revision)](https://huggingface.co/soyaakinohara/Spark-X2.5-4B-Heretic)
- [soyaakinohara/Spark-x2.5-4B-Heretic-jp (Japanese adaptation, datasets)](https://huggingface.co/soyaakinohara/Spark-x2.5-4B-Heretic-jp) · [jp GGUF ladder](https://huggingface.co/soyaakinohara/Spark-X2.5-4B-Heretic-jp-gguf)
- [darioooooo0o/Spark-X2.5-1.7B-Abliterated-GGUF (sealed-set measurements, methodology essay)](https://huggingface.co/darioooooo0o/Spark-X2.5-1.7B-Abliterated-GGUF)
- [darioooooo0o/Spark-X2.5-1.7B-GGUF (sibling repo, runtime notes)](https://huggingface.co/darioooooo0o/Spark-X2.5-1.7B-GGUF)
- [HF API: derivative facts (created 2026-09-04T02:08:15Z, pinned sha d9cbf6a0)](https://huggingface.co/api/models/soyaakinohara/Spark-X2.5-4B-Heretic)
- [HF API: base facts (created 2026-08-24T06:34:34Z, sha 5e10fcc0, downloads/likes)](https://huggingface.co/api/models/XHToken/Spark-X2.5-4B)
- [github.com/XHToken/Spark-X2.5 (community issues incl. 1M-context reproduction request)](https://github.com/XHToken/Spark-X2.5)
- [github.com/XHToken/llama.cpp (Spark fork, spark2_5 arch)](https://github.com/XHToken/llama.cpp) · [Spark-plugin](https://github.com/XHToken/Spark-plugin)
- [XHToken (SparkLLM) profile](https://huggingface.co/XHToken) · [soyaakinohara profile](https://huggingface.co/soyaakinohara) · [darioooooo0o profile](https://huggingface.co/darioooooo0o) · [@imdariotoo (X)](https://x.com/imdariotoo)

<!-- ARCHIVE-NOTICE -->
## Run this model on your terms

Want this model running for you, on a private cloud GPU or your own machine? [Request access on Signal](https://signal.me/#p/+13103408213) or [see how it works](https://abliterated.cloud/#how).

> Model research, dated at publication. Model licenses, publisher benchmarks and hosting estimates are specific to each article, not a live availability or price list. Reported zero-refusal results are test-specific, not a universal guarantee.
<!-- /ARCHIVE-NOTICE -->
