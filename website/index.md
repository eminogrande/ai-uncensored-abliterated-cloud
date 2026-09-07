---
title: Uncensored AI Cloud & Self-Hosting | ABLITERATED.cloud
description: Run uncensored and abliterated LLMs on rented cloud GPUs or your own hardware. Get hands-on setup, llama.cpp and app integration help. Free MIT-licensed code.
canonical: https://abliterated.cloud/
---

# Intelligence, freed.

Rent cloud GPUs and self-host uncensored, abliterated AI.

Your model. Your GPU. Your rules. Run an uncensored LLM with our MIT code, or get personal help renting, self-hosting and connecting it.

[Talk on Signal](https://signal.me/#p/+13103408213) · [Self-hosting guide](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/OPERATIONS.md) · [Read the model blog](https://abliterated.cloud/blog/)

[Services](https://abliterated.cloud/#services) · [Self-host](https://abliterated.cloud/#self-host) · [Blog & guides](https://abliterated.cloud/blog/) · [Signal](https://signal.me/#p/+13103408213)

<a id="services"></a>
## Open code. Human help. Your infrastructure.

Bring your model and budget. Get a scoped setup, a client connection test and clear start/stop instructions.

<a id="cloud"></a>
### Rent a cloud GPU

Try a larger model without buying a server. We help choose the GPU and quantization, check costs and set up private access. Our current cloud path is **Vast.ai + llama.cpp**.

[See reference GPU costs](https://abliterated.cloud/#cost)

<a id="self-host"></a>
### Use your own hardware

Run an uncensored LLM on a compatible workstation or server. Get help with model fit, llama.cpp and local access. Our code is free under MIT; hardware, operating costs and model licenses are separate.

[Read the self-hosting guide](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/OPERATIONS.md)

<a id="integrations"></a>
### Connect your app or router

Connect your chat app, coding client or LLM router to llama.cpp's OpenAI-compatible interface. We help set the base URL and model ID, then test your client. This is integration help, not a hosted routing API.

[Discuss your integration on Signal](https://signal.me/#p/+13103408213)

<a id="workflow"></a>
## Keep control of your setup.

1. **Bring your use case.** Send your model, app and hardware or rental budget. We agree the setup, tests and assistance price.
2. **Run it privately.** Start the Vast.ai GPU deliberately, connect to llama.cpp over SSH, then test the loaded model in your client.
3. **Know how to stop.** Keep the configuration and operating steps. Stop cloud instances manually and verify the state. Retained disks still cost money.

Your app connects to your model server, not this website. [Read the access details](https://abliterated.cloud/auth.md).

<a id="archive"></a>
## Read the facts. Find your next model.

Uncensored model news, benchmarks and self-hosting research. Skim the TL;DR and Basically facts, check the sources, then choose what to run.

<!-- ABLITERATED-LATEST-RELEASES-MD -->
- 2026-09-06: [Day ten for Spark X2.5: the uncensor wave on the 1M-context 4B](https://abliterated.cloud/blog/spark-x2-5-uncensor-wave/)
- 2026-08-31: [Eleven hours from DeepSeek drop to uncensor.](https://abliterated.cloud/blog/deepseek-v4-flash-vision-exp-abliterated/)
- 2026-08-30: [Why would a translation model refuse? Tencent's Hy-MT2, decensored](https://abliterated.cloud/blog/tencent-hy-mt2-30b-a3b-uncensored/)
<!-- /ABLITERATED-LATEST-RELEASES-MD -->

[Read all models & guides](https://abliterated.cloud/blog/) · [Subscribe via RSS](https://abliterated.cloud/blog/feed.xml)

Coverage does not imply testing or hosting. Check each article's date, sources and license. [Ask about running a model](https://signal.me/#p/+13103408213).

<a id="cost"></a>
## Know what the machine costs.

**Reference GPU provider rates** from our dated Vast.ai contract, not customer service prices or a current rental offer. Assistance is scoped and priced separately on Signal.

<!-- RUNNING-COSTS -->
| Usage | Cost |
| --- | ---: |
| Running: GPU + disk / hour | **$0.63333** |
| Running continuously / 24 hours | **$15.20** |
| Running continuously / 30 days | **$456.00** |
| Stopped: retained disk / 30 days | **$24.00** |
| 2 hours running per day / 30 days, disk retained throughout | **$60.00** |

USD, contract quote checked 2026-09-05. GPU $0.60/hour plus storage $0.03333/hour. Stopped disk: $0.80/day. Two hours/day for 30 days: $36.00 GPU + $24.00 disk. GPU time is billed while running, even without requests. Storage is billed continuously. Bandwidth, applicable taxes and other services are excluded. No automatic idle shutdown.
<!-- /RUNNING-COSTS -->

<a id="limits"></a>
## Questions before you start.

### What is an abliterated LLM?

An abliterated LLM has been modified to reduce learned refusal behavior. Uncensored is a broader label, not a guarantee. A modified model can still refuse, make mistakes or lose capabilities.

### Can I run uncensored AI for free?

Our project-owned code is free to self-host under MIT. GPU rentals, storage, electricity and setup assistance are not free. Model weights have separate licenses. We scope and price assistance on Signal before work begins.

### Does zero refusal AI mean it answers everything?

No. Zero refusal AI can describe results on a particular test set, not a universal guarantee. Behavior depends on the model, prompt and runtime. We help test your workload without promising zero refusals, accuracy or reliable tool use.

### Is there a public inference API I can use now?

No. We offer human setup help, code and guides, not instant API keys or an always-on hosted catalog. The current cloud workflow uses manually started Vast.ai compute and llama.cpp over private SSH. Contact us on Signal.

<a id="contact"></a>
## Bring the model. We'll help with the rest.

Send a model link, your hardware or GPU budget, and the app you want to connect.

[Talk on Signal](https://signal.me/#p/+13103408213) · [Explore the open-source code](https://github.com/eminogrande/ai-uncensored-abliterated-cloud)

<a id="status"></a>
## Our reference setup.

**STOPPED · 2026-09-05 20:12 UTC.** Reference instance snapshot, not live availability. No current inference test.

<!-- PROJECT-STATUS -->
Stopped. Provider snapshot: 2026-09-05 20:12 UTC, not live polling. 1 Vast.ai instance: 49433042, A100 PCIE 40960 MB, 120 GB disk. actual_status=exited; intended_status=stopped.

Last local health check (2026-09-05T19:39 UTC): localhost:8080 connection refused. No current inference test. Stopped storage remains billed.

Last serving configuration: Qwen3.8-27B OBLITERATED, Q6_K, llama.cpp, 262144 tokens configured. Not serving now; long-context quality is unvalidated.

Modal: Retired and not used by this project because of its cost budget. Four old apps still existed with zero tasks at the 2026-09-05 19:39 UTC audit; they were not decommissioned. Possible legacy storage charges remain unaudited.
<!-- /PROJECT-STATUS -->

Historical runs do not establish a best model or comparable speed. Vast.ai is the only current cloud path; Modal docs are historical.

[Snapshot JSON](https://abliterated.cloud/.well-known/project-status.json) · [Agent operating notes](https://abliterated.cloud/skills/abliterated-cloud/SKILL.md)

<a id="license"></a>
## Free code. Yours to self-host.

Our website and code use MIT: inspect, adapt and self-host without a software license fee. Compute and assistance cost separately. Model weights and third-party code keep their own licenses; public availability does not imply commercial-use permission.

[Source repository](https://github.com/eminogrande/ai-uncensored-abliterated-cloud) · [Website notice](https://abliterated.cloud/NOTICE.md)

---

ABLITERATED.cloud — Intelligence, freed.

[Agent index](https://abliterated.cloud/llms.txt) · [Documentation schema](https://abliterated.cloud/openapi.json) · [Updates](https://abliterated.cloud/RELEASE_NOTES.md)
