# On-demand endpoints: audit and deployment options

Checked 2026-09-27 against `main` at `1cb9c33`, open PR #18 at
`93ca859c290f63c079718abd68da8da372453810`, the public homepage and current Vast
documentation. The initial review is preserved below. Subsequent authorized
inspection and deployment findings are recorded in [STATUS.md](STATUS.md).
The new router implementation uses native Vast Serverless, not PR #18.

## Observed state

- The public website is static GitHub Pages. It has no GPU control backend.
- `https://api.abliterated.cloud/health` returned HTTP 502. The response does not
  prove that the GPU is stopped: the model, tunnel or gateway could be unavailable.
- PR #18 contains a gateway, browser control panel and autopilot. It remains open.
  Its 48 local tests pass, but they do not prove the safety claims below.
- During subsequent authorized inspection, the Vast account had zero instances.
  The deployed legacy gateway referenced a missing instance, and its reaper timer
  was inactive. Public `/health` had entered that unsafe wake path; no GPU started.
- The legacy gateway, tunnel and reaper were disabled after backup. The new
  authenticated router controls are deployed. Inference validation remains
  separate; consult current status evidence rather than the historical snapshot.

## Existing autopilot: do not enable unattended yet

Source references refer to the head of
[PR #18](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/pull/18),
not files already merged into `main`.

1. **Public health requests can start paid compute.** `gateway/gateway.py`
   exempts `/health` and `/v1/health` from authentication, then sends both through
   `_proxy`'s wake/activity path. Monitoring can start or keep a GPU running.
   Health must be passive; only authorized inference or explicit start actions
   may wake compute.
2. **Concurrent cold requests do not wait for readiness.** `autopilot.wake`
   returns `state=waking` immediately when another wake holds the lock. The
   gateway ignores `_wake_upstream`'s result and proceeds to the unavailable
   upstream. Also, wake logs share stdout with the JSON result, breaking the
   gateway's JSON parser. Separate logs from results and wait with a bounded
   deadline before proxying.
3. **Request lifetime and shutdown are not coordinated.** Activity is recorded
   at request arrival, not throughout streaming or at completion. The reaper
   does not track in-flight work or lock out newly arriving requests before
   stopping. Active work can be interrupted. Use shared request-lifetime state
   and serialize start/stop decisions.
4. **Failure cleanup is incomplete.** A stale wake lock blocks reaping; a failed
   wake can leave a start queued because the reaper ignores non-running states.
   A stop response is reported as `stopped` without confirming provider state.
   Cancel failed queued starts, recover stale locks safely and verify actual
   stopped state before reporting success.
5. **Panel start is not endpoint start.** `control.start` only changes the Vast
   instance state; it does not ensure llama-server or its SSH tunnel is ready.
   A manual start also does not update autopilot activity. The panel and gateway
   need the same lifecycle path, authenticated controls and truthful state.

The claim “never pay for an idle GPU” is false even after these fixes: the idle
window and shutdown delay are paid time. With the historical $0.60/hour GPU and
$24/month retained disk, one four-hour session daily plus 30–35 idle minutes
costs **$105–106.50 per 30 days**, before boot time, bandwidth, gateway hosting
and taxes. $96 excludes the idle window. Cold-start time is not measured here.

## Recommended path: Vast Serverless

Evaluate the provider's lifecycle before maintaining a custom scheduler. Keep a
stable client URL; let Vast recruit and release workers. The exact existing
GGUF/llama.cpp artifact is not a validated drop-in for the vLLM template. First
verify the chosen model format, quantization, GPU memory and tool parser.

For a single-user trial, explicitly configure:

- `max_workers = 1`: prevent multi-worker scale-out; this is not a spending cap.
- `min_load = 0`: permit zero active workers.
- `cold_workers = 0` and any applicable minimum-worker setting to zero: target
  zero total workers, not merely zero active workers.
- A positive `inactivity_timeout`, for example `600` seconds: a proposed
  ten-minute idle grace period, not a guaranteed shutdown deadline.
- A GPU price ceiling and approved trial budget before any provisioning.

The documentation uses both `min_workers` and `cold_workers`; API and guide
examples also disagree on defaults. Inspect the installed CLI/API schema, set
values explicitly and read back the effective configuration. Do not rely on a
quickstart's defaults: they can retain multiple workers and active capacity.

Zero active workers still incur storage charges when cold workers remain.
Zero total workers avoids retaining those workers' disks but requires fresh
provisioning/downloads. Loading and idle grace periods cost GPU time; bandwidth
and separate storage may still cost money. Do not destroy an existing retained
instance or unique files as part of this trial.

Vast advertises an OpenAI-compatible vLLM proxy at
`https://openai.vast.ai/<ENDPOINT_NAME>`. Its cURL example targets
`/<ENDPOINT_NAME>/v1/chat/completions`, while its SDK base URL example omits
`/v1`. Verify the exact client URL rather than assuming the examples agree.
The proxy supports text and streaming; tool calling depends on the model and
parser, and `parallel_tool_calls` is not supported. Its request `model` field
is ignored: `MODEL_NAME` on the endpoint selects the actual weights.

Sources, read 2026-09-27:

- [Scaling to zero](https://docs.vast.ai/guides/serverless/managing-scale)
- [Endpoint parameters](https://docs.vast.ai/guides/serverless/serverless-parameters)
- [Worker and endpoint billing](https://docs.vast.ai/guides/serverless/pricing)
- [OpenAI-compatible proxy](https://docs.vast.ai/guides/serverless/openai-compatible-api)
- [Instance stop/restart lifecycle](https://docs.vast.ai/guides/instances/manage-instances)

## Router, Pi and website

The requested client entry point is **`router.paymentrequired.com`**, not a
second public endpoint that every client must configure separately. Reuse its
existing upstream-provider integration if the deployed gateway supports it.

Authorized inspection confirmed that neither the deployed router nor CLIProxyAPI
contained an Abliterated upstream before this change. The new integration adds
owner-only model `abliterated/qwen3.8-27b`; the unrelated OpenRouter Qwen model is
not this GPU. Existing providers and payment configuration are preserved.

The router source has background inference probes and removes unhealthy models
from the available model catalog. A sleeping GPU must not be treated as a broken
model or repeatedly awakened by probes. Validate cold-start timeouts and keep
passive status checks separate from inference before exposing the model.

Pi already has a local `uncensored` provider pointing to
`http://127.0.0.1:8080/v1`. That requires a working SSH tunnel; it is not evidence
of router integration. Preserve existing providers. Add or update a router model
only after verifying the deployed model ID, authentication and endpoint behavior.
Do not expose the Vast management key to browser clients or distribute it as an
inference token. Pi token-cost estimates do not measure hourly GPU charges.

The static website links to the owner-authenticated router panel. It contains no
management key or automatic start call. Manual Off blocks automatic wake before
deleting the endpoint and temporary workers. The panel distinguishes pending
cleanup from confirmed zero resources. Opening the website or polling status is
passive. Current prices are not inferred from historical website quotes.

## Acceptance before enabling automatic operation

1. Inspect the deployed router, gateway and Vast configuration read-only. Record
   exact model ID, artifact/runtime versions, current rates and effective limits.
2. With explicit paid-test approval, run one bounded streaming response and one
   harmless Pi tool round trip through the router.
3. Send concurrent cold requests; prove one wake and no premature forwarding.
   Prove unauthenticated requests and monitoring never wake compute.
4. Let the idle window expire; prove active requests survive and provider state
   reaches zero total workers and retained worker disks. Test failed starts, queued starts and manual
   Stop behavior as well.
5. Read back actual charges and final state. Only then publish the controls or
   describe automation as working. Deployment alone does not satisfy these gates;
   see STATUS.md for the actually completed checks.
