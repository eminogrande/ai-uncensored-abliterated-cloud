# Private on-demand GPU operations

Use [the authenticated router controls](https://router.paymentrequired.com/abliterated/).
The public `abliterated.cloud` website is static; it only links to these controls.
Never put a Vast account key into the browser, Pi configuration or this repository.

## Start a session

1. Unlock the panel with the owner's private router bearer. It remains only in
   that browser tab's memory; reloading the page requires authentication again.
2. Select **Start / Automatik erlauben** and confirm paid operation. This creates
   the Vast endpoint/workergroup and allows authorized inference to recruit a GPU.
3. Select `abliterated/qwen3.8-27b` through Pi's `abliterated` provider. Use a fresh
   session and a bounded request. The configured context is 32768 tokens.
4. Allow time for provisioning, downloads and model loading. A readiness timeout
   is not permission to silently rent unlimited replacement workers.

Owner inference uses `https://router.paymentrequired.com/v1/internal`; the same
router bearer authenticates it. This model is not exposed on the public paid path,
public model-test endpoint or background inference-probe list.

## CLI and MCP

The owner's local CLI supports `abliterated status`,
`abliterated start --confirm-paid` and `abliterated stop --confirm-delete`.
`abliterated mcp` exposes the same controls through stdio MCP as `gpu_status`,
`gpu_start` and `gpu_stop`. Start sends one fixed response probe; MCP returns
while it boots so status can be polled. See the router's
[client guide](https://github.com/nuri-com/router-paymentrequired-com/blob/feat/abliterated-controls/docs/ABLITERATED.md).

Only provider-supplied download percentages are displayed. Otherwise the client
reports the current phase with unknown percentage. Its boot check reaches 100%
only after an actual nonempty model answer. That acceptance gate is still open
in the latest bounded live trial; do not claim inference is ready.

## Fully off

Select **Aus: GPU und Worker-Speicher löschen** and confirm. This is intentionally
destructive for this endpoint's temporary workers, not for unrelated resources.

- Automatic restarts are blocked before cleanup starts. Existing requests are
  aborted; a Pi request receives an error rather than overriding manual Off.
- The native Vast endpoint/workergroup and its workers are deleted, including
  the temporary model download. No separate volume is created.
- Wait until `state=off`, `enabled=false` and `zero_resources_verified=true`.
  The status also reports the last cleanup-verification timestamp.
- A cleanup error is not Off. The router retries cleanup every 30 seconds.
  Inspect the provider inventory if cleanup does not complete.

The existing router server remains separately billed. Removal does not refund
previous GPU time, downloads or storage use. Unique files do not belong on these
workers: save them elsewhere before any destructive operation.

## Automatic idle cleanup

With automatic operation enabled, the router deletes the endpoint after 1260
seconds without active requests, checked every 30 seconds. Activity is recorded
at request completion, and active streaming requests block idle cleanup. Unlike
manual Off, idle cleanup leaves automatic operation armed for the next authorized
inference request. Status reads and public health checks never wake the GPU.

Native Vast scaling also has zero minimum load, zero cold-worker floor and a
one-worker ceiling. Do not confuse zero active workers with zero total workers:
retained inactive workers can still incur storage charges. The router's complete
endpoint removal is the stronger shutdown path.

## Deployment and verification

The implementation is in the
[router repository](https://github.com/nuri-com/router-paymentrequired-com/tree/feat/abliterated-controls):
`abliterated.mjs`, `abliterated.config.json` and the private template source in
`docs/abliterated-vast-template.json`. Model revision and runtime are configured
in the template itself; overriding `--image` in workergroup launch arguments did
not override the legacy template image during testing.

Preserve the existing router's payment journal and unrelated providers. Back up
before a release, retain the previous image, and require explicit server-change
and paid-test approval. Keep `ABLITERATED_VAST_KEY` server-side. The lifecycle
controller currently assumes one router process, not multiple replicas.

Before claiming a release works, verify cold-start streaming, one harmless tool
round trip, manual Off, denied restart while off and idle cleanup. Read back
provider inventory after deletion. See [status](STATUS.md) for actual evidence;
configuration alone is not a successful inference test.

## Historical setup

The earlier private SSH/llama.cpp instance used a retained disk. Ordinary Vast
Stop has different semantics: **GPU compute stops; storage billing continues**.
There was **no verified automatic idle shutdown** in that earlier audit. Its
2026-09-05 snapshot and rates remain historical evidence, not instructions to
reuse an old instance ID or SSH destination. The old gateway and tunnel services
were disabled when moving to the router path.
