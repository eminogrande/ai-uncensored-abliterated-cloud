# Security and access boundary

## Current setup

The active operating path is a private Vast.ai instance running one llama-server,
reached through an SSH tunnel bound to local loopback. The public GitHub Pages site
contains documentation only; it is not a public inference API. Historical Modal
security documentation is preserved in [the archive](archive/modal/SECURITY.md).

The last recorded inference setup did not use a llama-server API key. A client value
such as `none` is only a placeholder; it does not secure a public endpoint. Keep the
server bound to loopback and do not publicly forward its port without authentication,
TLS, access controls and an explicit spending/concurrency policy.

## Credentials and host trust

Do not publish Vast account tokens, SSH private keys, model download tokens, local
client credential stores, raw sessions or account billing details. Public evidence
must use explicit non-secret fields rather than dumping whole API responses.

Use SSH host-key verification. A hosted GPU is a third-party machine; do not treat
its container as a secrets vault or assume the host operator cannot access files.
Invited users must not receive the owner's root SSH key or Vast account key.

## Data and cost safety

Use `stop` to pause compute while retaining disk. Storage billing continues.
`destroy` permanently deletes the instance's container disk and requires separate
confirmation plus verified backup of unique data. A stopped instance can lose resume
availability, and retained disk is not an independent backup.

A health check proves server readiness, not model identity, quality or tool safety.
Do not turn a model's name, a tiny prompt sample or a successful HTTP status into a
"zero refusal" or "works for every agent" guarantee.

## Reporting

Report repository issues without including credentials or private prompts. If a secret
is exposed, revoke or rotate it through its provider and check repository history and
published artifacts. Review `git diff --check` and `scripts/check-secrets.sh` before
publishing. Keep existing signed-commit and signed-release checks.
