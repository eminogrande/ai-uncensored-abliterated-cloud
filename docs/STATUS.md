# Operating status and evidence

**A100 STOPPED. No inference tested.** This is a dated owner-account snapshot,
**not a live monitor**. Use the [operating guide](OPERATIONS.md) for the current path.

## Current Vast state and rates

Source: [read-only recheck, 2026-09-05 20:12 UTC](evidence/2026-09-05-vast-recheck.json).

| Item | Observed state |
| --- | --- |
| Inventory | `total_instances=1`, one enumerated row, `next_token=null`; **0 running instances**. Previous V100 `49365403` is not listed. |
| Retained contract | `49433042`, A100 PCIe 40 GB; actual `exited`, current/intended `stopped`. |
| Storage | 120 GB container allocation, still billed while stopped; no separate volume was provisioned for this setup. |
| Costs | [Running and stopped estimates](../README.md#cost), calculated from the rechecked contract rates; exclude variable transfer charges, taxes and other provider fees. |

No GPU was started, redeployed or destroyed, and no inference request was made.
Retained model files were not reread while stopped; model autostart and automatic
idle shutdown remain unverified.

## Modal and local health: earlier check

Source: [original audit, 2026-09-05 19:39 UTC](evidence/2026-09-05-status.json).
These checks were **not refreshed by the later Vast rate/state recheck**.

- Local `http://127.0.0.1:8080/health` refused the connection; it was not usable.
- Four Modal apps remained deployed with zero tasks: `mn-uncensored-api`,
  `mn-god-qwen36-35b`, `mn-code-ornith-35b` and `mn-fast-qwythos-9b`.
  They were not removed or decommissioned. Storage/other charges were not audited;
  zero tasks does not prove a zero bill or an enforced shutdown.

Modal is retired/not in use for this project's cost budget, not a current operating
alternative or a market-wide price ranking. Its [source archive](../archive/modal/README.md)
preserves the old implementation, not instructions to restart it.

## Last configuration, not current inference proof

| Field | Recorded value | Evidence boundary |
| --- | --- | --- |
| Model repository | `OBLITERATUS/Qwen3.8-27B-OBLITERATED` | Historical session record; immutable revision not captured |
| Model file | `Qwen3.8-27B-OBLITERATED-Q6_K.gguf` | Historical listing; file hash not independently captured |
| Runtime | llama.cpp on A100 PCIe 40 GB | Build pin missing |
| Context | `262144` | Configured server/client capacity, not a full-length evaluation |
| Clients | Pi `uncensored`; OpenCode `uncensored`; historical Hermes `v100-local` | Pi/OpenCode config inspected; no fresh end-to-end generation |

Alias `qwen3.8-27b-obl` is not proof of loaded weights, and multiple aliases do not
load multiple models. In the next approved paid session, capture model revision and
SHA-256, llama.cpp commit/build flags, GPU, context and sampling. Check model identity,
short streaming/non-streaming output and a bounded tool round trip. Test long-context
quality, retrieval, timing and VRAM separately; then stop and record final cloud state.

## Evidence limits

- Small, incompletely preserved prompt probes (including the earlier six-probe
  set) do not establish universal zero refusals, coding quality or agent reliability.
- Quantization, sampling and other settings changed together; no isolated evidence
  establishes that Q6 or temperature alone fixed every failure.
- V100/A100 speed observations used different quants and short inputs; reproducible
  benchmark artifacts are missing. No speedup, "fastest" or "best coder" ranking is
  established. A100 lacks native FP8 Tensor Core acceleration; backend
  support/emulation does not establish speed.
- Stop retains billed storage; destroy deletes the container disk. Neither a local
  timer nor a static badge proves shutdown or availability.

## Inventory details

Inventory uses `GET https://cloud.vast.ai/api/v1/instances/?limit=100`; follow
`next_token` and reconcile rows with `total_instances`. The earlier collection
endpoint `/api/v0/instances/` returned HTTP 410, while individual lookup
`GET /api/v0/instances/49433042/?owner=me` worked. Stale `status_msg` prose said
"running" while actual/current/intended states were stopped; use the state fields.

Published evidence excludes credentials, account credit, host addresses and session
content. Keep future evidence free of raw user prompts and generated sensitive content.
