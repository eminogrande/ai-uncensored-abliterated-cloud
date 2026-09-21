# ABLITERATED.cloud

**Intelligence, freed.** Human-assisted cloud GPU renting and self-hosting for
uncensored and abliterated models. Get help choosing a model and connecting it to
your LLM router, chat app or coding tools.

[Talk on Signal](https://signal.me/#p/+13103408213) about your workload, model,
hardware budget and client. Scope, access and any costs are agreed with a human
before setup. The public website offers service information, documentation and
[model news and guides](https://abliterated.cloud/blog/), not self-service inference
or account checkout.

## Current operating docs

- [Operating guide](docs/OPERATIONS.md): the private **Vast.ai + llama.cpp** path,
  SSH access, client configuration and manual start/stop.
- [Status evidence](docs/STATUS.md): dated checks, last configuration and untested claims.
- [Licensing scope](docs/LICENSING.md): project-owned MIT work versus upstream model terms.
- [Website](https://abliterated.cloud/) · [Agent reading index](website/llms.txt) ·
  [Website development](website/README.md)

## Current state

**A100 STOPPED — operator state and rates rechecked 2026-09-05 at 20:12 UTC.**
The [read-only snapshot](docs/evidence/2026-09-05-vast-recheck.json) found one A100
PCIe 40 GB instance (`49433042`), actual `exited` / intended `stopped`, with a
120 GB retained disk **still billed while stopped**. No inference was tested.
This is not live availability or a statement about service enquiries.

Last serving configuration: `OBLITERATUS/Qwen3.8-27B-OBLITERATED`,
`Qwen3.8-27B-OBLITERATED-Q6_K.gguf`, llama.cpp, through a private SSH tunnel to
`http://127.0.0.1:8080/v1`. The local endpoint was unreachable at the earlier
19:39 UTC audit. Verify the actual loaded model before reconnecting.

Modal is retired from this project's operating path for its cost budget. The
[implementation is archived](archive/modal/README.md), not decommissioned:
four legacy apps had zero tasks at the earlier audit; remaining storage/other
charges were not audited. It is not the current setup guide.

## Cost

Example infrastructure costs from the [20:12 UTC Vast recheck](docs/evidence/2026-09-05-vast-recheck.json),
not a customer service quote or live public billing. Confirm current provider rates
and the scope of assistance before authorizing spend. Running rates are not the
stopped bill.

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

**Stop retains the disk and ends GPU compute billing; destroy deletes the instance
and its container disk.** A normal pause is a stop, never a destroy.

## Self-hosting costs by model size

What it costs to run a model yourself, refreshed from the live marketplace by
[`scripts/fetch-gpu-prices.py`](scripts/fetch-gpu-prices.py) rather than typed by
hand. The same table is published at [abliterated.cloud/costs](https://abliterated.cloud/costs/).

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

## Connect with consent

1. Agree the model, provider/account, GPU/storage budget and client with the operator.
2. Obtain explicit consent before paid compute, configuration changes or sharing
   connection details. Use the [operating guide](docs/OPERATIONS.md), not old tokens
   or archived wake routes.
3. Verify the server and loaded artifact, connect through private SSH, then test
   a bounded response and the intended LLM router/app. A client alias does not load
   or switch model weights; model autostart is not verified.
4. Stop after use and read back provider state. **Automatic idle shutdown is not
   verified**; disk billing continues. Never destroy an instance as a routine stop.

## Evidence limits

- **No universal zero-refusal guarantee.** Publisher claims and small prompt probes
  do not establish general refusal rates, coding quality or agent reliability.
- **No validated 262k workload.** `262144` is a recorded context setting, not proof
  of long-context quality. Model/build pins and controlled speed benchmarks are missing.
- **Human-assisted setup, not a public inference API.** No public self-service
  endpoint, API-key issuance, account checkout, MCP service or automated billing is
  deployed. Availability and setup scope must be agreed with a human.

[Status](docs/STATUS.md) records what was checked and what still needs a paid-session
test. The active blog's field notes retain their publication dates, model licenses
and historical estimates; coverage is not a hosted-model inventory or current price.

## Work on the website

```sh
uv sync --group dev
uv run python -I scripts/build-blog.py
uv run pytest -q
python3 -m http.server 8788 --bind 127.0.0.1 --directory website
```

Open `http://127.0.0.1:8788/`. Reading the static site requires no GPU, inference
call, external font service or background artwork. See the
[website guide](website/README.md) for publishing and verification.

Current operations and evidence live in `docs/`; site content in `website/`;
build, verification and signed Pages publishing helpers in `scripts/`; checks in
`tests/`. `archive/modal/` is historical. This repository is the documentation
source of truth, not stale status JSON or "live" badges in the earlier
`ai-uncensored-selfhost` experiment repository.

## License and history

Our own code, documentation and website are [MIT licensed](LICENSE) from this
release. Previous Apache-2.0 releases keep their terms; that license was a project
choice, not a Vast.ai, Modal or llama.cpp requirement. Model weights, dependencies
and third-party materials retain their upstream licenses; see
[licensing scope](docs/LICENSING.md).

The [changelog](CHANGELOG.md) and [release notes](docs/RELEASE_NOTES.md) preserve
release history and earlier claim corrections without changing the current path.
