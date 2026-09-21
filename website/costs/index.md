---
title: Self-Hosting Costs by Model Size | ABLITERATED.cloud
description: What it costs to run an uncensored or abliterated model yourself - live cloud GPU prices per hour, per day and per month, for every model size we cover.
canonical: https://abliterated.cloud/costs/
---

# Self-hosting costs, by model size.

These are live prices from the GPU marketplace, for the cheapest card that fits each size of model we cover. Not a quote from us: your own account, your own bill.

Every model on the site fits one of these rows. Pick your size, see the price, then [ask on Signal](https://signal.me/#p/+13103408213) if you want us to set it up.

## The whole table

<!-- MODEL-SIZE-PRICES -->
| Model size | Cheapest supported offer | Per hour | Per day | Per month, 24/7 | Per month, 2 h/day | Models covered |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Up to 14B | RTX 3060, 12 GB VRAM, 40 GB disk | **$0.0511** | $1.23 | $36.80 | $10.40 | MiniCPM5-2B-heretic-abliterated, Spark-X2.5-4B-Heretic, AFM-4.5B-Uncensored-Abliterated +4 more |
| 27-35B | Tesla V100, 32 GB VRAM, 70 GB disk | **$0.1589** | $3.81 | $114.40 | $35.20 | gemma-4-31B-it-qat-q4_0-uncensored, Tencent-Hy-30B-A3B-uncensored-here, Velum-Unbound-Uncensored +12 more |
| 70-80B | Q RTX 8000, 48 GB VRAM, 92 GB disk | **$0.2922** | $7.01 | $210.40 | $34.40 | no covered model published yet |
| 118-120B MoE | RTX PRO 6000 Max-Q, 96 GB VRAM, 120 GB disk | **$1.0556** | $25.33 | $760.00 | $100.00 | Laguna-S-2.1-Uncensored-Heretic |
| 180-400B MoE | 2x RTX PRO 6000 Max-Q, 191 GB VRAM | **$2.2583** | $54.20 | $1,626.00 | $218.00 | DeepSeek-V4-Flash-Vision-Exp-Ablit, Qwen3.8-Flash-Next-ABLITERATED, GLM-5.3-Flash-ABLITERATED +1 more |
| 550B-1T | 4x RTX PRO 6000 S, 382 GB VRAM | **$6.6489** | $159.57 | $4,787.20 | $985.60 | DeepSeek-V4.1-Flash-UNCENSORED, Ornith-1.0-397B-abliterated |
| 1T and larger | 8x RTX PRO 6000 WS, 765 GB VRAM | **$11.94** | $286.58 | $8,597.33 | $853.33 | Kimi-K3-Abliterated-modal |

Cheapest supported offer per size class, fetched 2026-09-21, reliability 0.98 and above. GPU time is billed while running, even with no requests. Storage is billed continuously, including while the instance is stopped, which is what the two-hours-a-day column keeps paying. Bandwidth, taxes and other provider services are excluded. Prices move by the minute: the timestamp above is the honest date, not the moment you read this.
<!-- /MODEL-SIZE-PRICES -->

## How to read this table

The **2 hours a day** column is what most people actually pay: you start the GPU when you need it and stop it afterwards. It still pays for the disk that keeps your downloaded model between sessions.

The **24/7** column is the price of forgetting to stop it. Nothing here shuts itself down for you.

A bigger model is not automatically a better one. A 27B model on a cheap card answers most questions; a 400B model costs forty times as much per hour and still makes mistakes.

Prices are marketplace quotes at fetch time and change by the minute. A card that is cheap today can be gone in an hour, and a stopped instance can come back unavailable. The fetch date is the honest date.

[Get help choosing a model](https://signal.me/#p/+13103408213) · [How it works](https://abliterated.cloud/#how) · [Model news and guides](https://abliterated.cloud/blog/)
