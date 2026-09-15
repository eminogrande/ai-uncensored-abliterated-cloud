# Operating status and evidence

**All instances STOPPED.** Dated owner-account snapshots, **not a live monitor**.
Use the [self-hosting guide](SELFHOST.md) for the current path, and
[operations](OPERATIONS.md) for the owner-only account procedure.

## Current Vast state and rates

Sources: owner-account recheck, 2026-09-05 20:12 UTC
([evidence](evidence/2026-09-05-vast-recheck.json)); live CLI checks
2026-09-13 and 2026-09-15.

| Instance | GPU | Actual | Intended | Disk | Rate (running) |
| --- | --- | --- | --- | --- | --- |
| `49433042` | A100 PCIe 40 GB | `exited` | `stopped` | 120 GB retained | $0.60/h + $0.0333/h storage |
| `50934401` | A100 SXM4 80 GB | `exited` | `stopped` | 90 GB retained | $0.99/h, label `ab-refusal-test` |

Both stopped at last check. **Stopped disk keeps billing**: ~$0.80/day for
`49433042`, ~$0.60/day for `50934401`. No GPU is consuming compute right now.
A start attempt on `49433042` on 2026-09-13 returned *"Required resources are
currently unavailable, state change queued"* and never booted in 20 minutes of
polling — a live reminder that **restart availability is not guaranteed**.

## Last tested configuration (2026-09-13)

| Field | Value | Evidence boundary |
| --- | --- | --- |
| Model A | `OBLITERATUS/Qwen3.8-27B-OBLITERATED` Q6_K, 22,430,991,392 B | hash verified on disk |
| Model B | `OS-Software/Qwen3.8-27B-Uncensored-Heretic-v3-UD` Q6_K_XL, 24,948,050,656 B | hash verified on disk |
| Runtime | llama.cpp commit `5f436dddb440a288ee5611d7d1eca564a6aca9f4`, `-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=80` | build flags recorded |
| Server flags | `-ngl 99 -fa on -c 16384 --no-webui --jinja` | smoke-tested |
| Endpoint | private SSH tunnel → `http://127.0.0.1:8080/v1` | loopback only, never public |
| Public API | **none** | no self-service endpoint, keys or checkout |
| Clients tested | raw OpenAI-compatible API | no client UI tested this session |

## 12-prompt refusal probe (2026-09-13)

`mlabonne/harmful_behaviors`, seed 42, temperature 0, keyword scoring,
identical GPU/quant class/sampler. Small probe, **not a benchmark**:

| Model | Mode | Keyword refusals | Empty outputs |
| --- | --- | --- | --- |
| `OBLITERATED` Q6_K | thinking off | **0/12** | 0/12 |
| `Heretic-v3-UD` Q6_K_XL | thinking off | 5/12 | 0/12 |
| `Heretic-v3-UD` Q6_K_XL | thinking on, 4k budget | 0/12 | 7/12 |

See `abliterated-score-review/ab-test-2026-09-13/AB-REPORT.md` for the full
table and per-prompt honesty notes.

**Reading it honestly:** OBLITERATED has the lowest keyword count, but on two
extreme prompts it lectured instead of answering. Keyword absence is not
compliance. Heretic-v3 with thinking on was the most genuinely compliant, but
returned empty bodies on 7/12 prompts (reasoning consumed the token budget) —
unusable in that configuration. **Coding quality was not tested.**

## Monthly budget arithmetic (2026-09-15 live offers)

| Setup | Rate | 24/7 month | Hours for $100 / $200 |
| --- | --- | --- | --- |
| RTX 3090 24 GB (HU) | $0.174/h | **$125** | 575 / 1,150 |
| A100 PCIE 40 GB (existing) | $0.633/h | $456 | 158 / 315 |
| RTX PRO 6000 96 GB | $1.28–1.52/h | $922–1,094 | 66–78 / 131–156 |
| 2× RTX PRO 6000 96 GB | $2.27–2.67/h | $1,634–1,922 | 37–44 / 75–88 |
| 4× H200 (DeepSeek V4.1 FP8) | $18.37/h | $13,224 | 5.4 / 10.9 |
| 8× H100 (Kimi K3 minimum) | $19.37/h | $13,944 | 5.2 / 10.3 |

Live marketplace quotes, not reservations; exclude bandwidth and taxes.
A previous 96-GB offer at $1.283/h was quoted on 2026-09-15 at
`42871298` (Utah, reliability 0.97). Offer availability is volatile.

## What remains untested

- **Coding quality** of any model in this repo — no HumanEval, SWE-bench or
  agentic loop was run. The 12-prompt set measures refusal behavior only.
- **`262144` context** is a configured capacity, not a long-context quality
  test. Last probe used `16384`.
- **Automatic idle shutdown** — still not implemented anywhere. Stopping is
  manual; see [operations](OPERATIONS.md#4-stop-and-verify).
- **Model autostart** — `onstart` was null on both instances. After any restart
  the server must be launched manually over SSH.
- **Agent reliability** — Cline/Pi/OpenCode tool loops were not tested against
  either model. A 27B model behind an agent harness stalls more often than a
  frontier model; assume nothing until one bounded task passes.
- **Vast account credit** — a `create instance` call on 2026-09-15 failed with
  *"Your account lacks credit; see the billing page."* No new GPU can start
  until the account is topped up. This is an account state, not a provider
  outage.

## Inventory details

Inventory uses `GET https://cloud.vast.ai/api/v1/instances/?limit=100`; follow
`next_token` and reconcile rows with `total_instances`. The earlier collection
endpoint `/api/v0/instances/` returned HTTP 410, while individual lookup
`GET /api/v0/instances/49433042/?owner=me` worked. Stale `status_msg` prose
said "running" while actual/current/intended states were stopped; use the state
fields.

Published evidence excludes credentials, account credit, host addresses and
session content. Keep future evidence free of raw user prompts and generated
sensitive content.
