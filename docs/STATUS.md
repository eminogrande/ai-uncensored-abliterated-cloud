# Operating status and evidence

**Private streamed chat and confirmed worker deletion are verified.** This is
an evidence record, not a live availability monitor. Follow the
[operating guide](OPERATIONS.md) and inspect the authenticated panel before use.

## Successful chat trial: 2026-09-27, 14:29 UTC

MCP started the model at 14:12:50 UTC. The response check passed at 14:27:59 UTC.
A real streamed request through `router.paymentrequired.com/v1/internal` asked
for 17 times 23; `OBLITERATUS/Qwen3.8-27B-OBLITERATED` answered **391** in 24 content
chunks. The test immediately called Off. Deletion was confirmed at 14:28:20 UTC;
independent inventory at 14:29:05 UTC found zero instances, owned endpoints and
workergroups. An inference request while Off returned HTTP 409 without waking.

The previous 20-minute request limit interrupted a healthy model during native
benchmarking. The deployed limit and Pi's global HTTP idle timeout are now
30 minutes. Runtime revision: `e00c00118f5b553bdcda5b2c913e9c39b2bfb3fd`.
199 local tests and 10 focused deployed-image checks pass.

The 21-minute idle threshold is configured and clock-tested, but its full live
idle cycle remains unverified. Pi tool calling is also not yet verified. This
proves owner-only chat, not public customer access or universal client compatibility.

[Successful chat evidence](https://github.com/nuri-com/router-paymentrequired-com/blob/feat/abliterated-controls/docs/abliterated-chat-verification-2026-09-27.json)

## Earlier follow-up trial: 2026-09-27, 13:11 UTC

The actual engine failure was captured: **`No space left on device (os error 28)`**
during model reconstruction. The temporary 100 GB disk was insufficient. The
private template and worker now request 200 GB; the real worker allocation was
verified as 200 GB and its usage passed the old failure threshold.

CLI and stdio MCP now provide owner-approved start, passive status and destructive
Off. Live MCP started a worker, reported `loading_model`, then confirmed deletion.
The corrected worker was still loading when the remaining authorized test window
ended; **no model answer is verified yet**. No additional paid retry was started.

The idle threshold is now 1260 seconds (21 minutes), checked every 30 seconds.
Clock-based tests prove the boundary and that status reads do not extend it.
A full 21-minute live idle cycle remains untested. Percentages are shown only
when measurable; the response check does not claim 100% without a real answer.

Final independent inventory at 13:11 UTC: **zero instances, zero owned endpoints,
zero owned workergroups**, manual Off and healthy router. Runtime revision:
`108c05bf27b1657bc6d1e7179d16628d78a0f1a2`. Existing expert/Kimi work was preserved.
199 local router tests pass; nine focused checks passed in the deployed image.
An intermediate deployment rolled back after a configuration-file permission
failure; the final release passed its health check without a payment-state rollback.

[Detailed follow-up evidence](https://github.com/nuri-com/router-paymentrequired-com/blob/feat/abliterated-controls/docs/abliterated-verification-2026-09-27.json)
· [CLI/MCP source and usage](https://github.com/nuri-com/router-paymentrequired-com/blob/feat/abliterated-controls/docs/ABLITERATED.md)

The following earlier observations retain their original scope and counts.

## Authorized inspection and implementation: 2026-09-27

- Initial account inventory contained zero Vast instances. The legacy gateway
  referenced a missing instance and its reaper timer was inactive. A public
  `/health` request entered an unsafe wake path but did not start a GPU.
- The existing router and CLIProxyAPI contained no Abliterated provider. The
  new owner-only route and controls now run behind `router.paymentrequired.com`.
  Existing payment settings and providers were preserved; deployment kept
  state backups and rollback containers.
- The legacy gateway, tunnel and reaper services were disabled after backup.
  Open [PR #18](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/pull/18)
  remains experimental historical code, not the new serving implementation.
- Pi lists the added `abliterated` provider. This is configuration proof only,
  not a successful model answer or tool round trip.
- Router tests pass: 168 in the deployed image, 170 locally after adding two
  regression checks. Website/documentation tests pass: 28. The control page
  returns HTTP 200; unauthenticated control requests return HTTP 401.

## Paid trial findings

The target is `OBLITERATUS/Qwen3.8-27B-OBLITERATED`, pinned to revision
`a58c3b53b3ce71551eafde2ed5ec8df48e0f4ff8`. The checkpoint declares architecture
`Qwen3_5ForConditionalGeneration` and contains approximately 55.56 GB of
safetensors. The owner template sets a 32768-token context and uses
`vastai/vllm:v0.30.0-cuda-13.0`; eager execution avoids graph compilation at the
cost of some runtime optimization. It is not the historical GGUF configuration.

Trials identified and corrected these integration issues:

1. The usable proxy route is `/<endpoint>/chat/completions`; inserting `/v1`
   returned HTTP 404.
2. Cold proxy requests timed out around 60 seconds. The router now polls the
   native routing protocol before forwarding the user prompt, with a bounded
   20-minute total request deadline.
3. Workergroup `--image` did not override the legacy template's vLLM image.
   A private template now selects vLLM 0.30.0 directly, confirmed in the actual
   worker inventory and startup log.

**Remaining blocker:** the corrected worker still reported `RuntimeError: Engine`
during model initialization. Native Vast retried/replaced that worker. A
replacement remained in image-loading state during observation. No successful
streamed model answer or Pi tool round trip has been recorded. Do not describe
this model as ready, and do not mistake passing lifecycle tests for inference
proof. Live idle-shutdown acceptance remains pending.

The router commit deployed in that earlier trial was `86860d0af4a3e9c0d028ed904421070475b93374`.
The [final read-back at 09:11 UTC](evidence/2026-09-27-router-on-demand.json)
confirmed `enabled=false`, `state=off`, `zero_resources_verified=true`, zero
instances, zero owned endpoints and zero owned workergroups. An authenticated
inference request while off returned HTTP 409 without creating resources.
The initial Off request returned HTTP 503 during cleanup; retry/reconciliation
then confirmed complete removal. No temporary worker or its disk remains.
The router server is still separately billed; settled charges were not audited.

See [the endpoint audit](ENDPOINTS.md) for the legacy defects and acceptance gates.
Historical evidence below has not been overwritten.

## Historical Vast state and rates

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
load multiple models. For any future test of this historical configuration, capture
model revision and SHA-256, llama.cpp commit/build flags, GPU, context and sampling. Check model identity,
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
