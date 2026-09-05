---
title: ABLITERATED.cloud — Private model evaluation
description: Private on-demand evaluation on Vast.ai with llama.cpp. Public documentation and editorial archive, not public inference.
canonical: https://abliterated.cloud/
---

# ABLITERATED.cloud

Private model evaluation on Vast.ai with llama.cpp. This website publishes documentation and an editorial archive, not a hosted model catalog or a public inference API.

## Dated operating snapshot

<!-- PROJECT-STATUS -->
Stopped. Provider snapshot: 2026-09-05 20:12 UTC, not live polling. 1 Vast.ai instance: 49433042, A100 PCIE 40960 MB, 120 GB disk. actual_status=exited; intended_status=stopped.

Last local health check (2026-09-05T19:39 UTC): localhost:8080 connection refused. No current inference test. Stopped storage remains billed.

Last serving configuration: Qwen3.8-27B OBLITERATED, Q6_K, llama.cpp, 262144 tokens configured. Not serving now; long-context quality is unvalidated.

Modal: Retired and not used by this project because of its cost budget. Four old apps still existed with zero tasks at the 2026-09-05 19:39 UTC audit; they were not decommissioned. Possible legacy storage charges remain unaudited.
<!-- /PROJECT-STATUS -->

## Running cost

<!-- RUNNING-COSTS -->
| Usage | Cost |
| --- | ---: |
| Running: GPU + disk / hour | **$0.63333** |
| Running continuously / 24 hours | **$15.20** |
| Running continuously / 30 days | **$456.00** |
| Stopped: retained disk / 30 days | **$24.00** |
| 2 hours running per day / 30 days, disk retained throughout | **$60.00** |

USD, contract quote checked 2026-09-05. GPU $0.60/hour plus storage $0.03333/hour. GPU time is billed while running, even without requests. Storage is billed continuously. Bandwidth, applicable taxes and other services are excluded. No automatic idle shutdown.
<!-- /RUNNING-COSTS -->

[Machine-readable snapshot](https://abliterated.cloud/.well-known/project-status.json).

## Current workflow

1. The operator checks the current instance, disk, quote and authorized spending scope, then starts it manually.
2. Connect privately to localhost:8080 through an operator-controlled SSH tunnel. Confirm the actual loaded model before testing.
3. Stop manually and verify the stopped instance state. Stopping retains disk and ongoing storage charges; it is not deletion. No automatic idle shutdown is proven.

This website cannot start a GPU. There is no public inference, customer billing, inference OAuth, or live MCP service. See the [access boundary](https://abliterated.cloud/auth.md) and [operator repository](https://github.com/eminogrande/ai-uncensored-abliterated-cloud).

## Evidence limits

262144 is configured context only, not long-context validation. There is no current best-model or performance claim: old runs used different artifacts, settings and tests. Abliteration is not a zero-refusal, capability or correctness guarantee.

The old Modal approach is archived, not the current operating path. Archived notes are history, not available products.

## Editorial archive

These are source-linked articles at their publication dates, not live models, a current price list, or proof we evaluated each model. Per-model licenses, historical estimates and publisher claims remain in the articles. Noncomparable benchmarks do not establish a current ranking; results on one refusal test do not guarantee general behavior.

<!-- ABLITERATED-LATEST-RELEASES-MD -->
- 2026-08-31: [Eleven hours from DeepSeek drop to uncensor.](https://abliterated.cloud/blog/deepseek-v4-flash-vision-exp-abliterated/)
- 2026-08-30: [Why would a translation model refuse? Tencent's Hy-MT2, decensored](https://abliterated.cloud/blog/tencent-hy-mt2-30b-a3b-uncensored/)
- 2026-08-30: [The 118B coding MoE nobody has refused](https://abliterated.cloud/blog/laguna-s-2-1-uncensored-heretic/)
<!-- /ABLITERATED-LATEST-RELEASES-MD -->

[All field notes](https://abliterated.cloud/blog/) · [RSS](https://abliterated.cloud/blog/feed.xml)

## Licenses

MIT covers our own website and code only. Upstream code, model weights and derivatives retain their own licenses and restrictions. Public availability is not blanket commercial-use permission.
