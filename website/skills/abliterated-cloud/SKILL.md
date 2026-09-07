---
name: abliterated-cloud
description: Choose uncensored models and arrange self-hosting help.
license: MIT
metadata:
  homepage: https://abliterated.cloud/
  repository: https://github.com/eminogrande/ai-uncensored-abliterated-cloud
---

# ABLITERATED.cloud

Help a user choose an uncensored or abliterated model, read its sources, and arrange human-assisted cloud GPU renting, self-hosting or LLM router/app integration. The public site offers documentation and model news, not a public inference API or automated checkout.

## When to use

- Compare model candidates for a workload, hardware budget or client.
- Read current operating docs and dated evidence before recommending a setup.
- Prepare a human handoff or, with explicit consent, help connect an authorized private runtime.

Do not use this skill to buy compute, send messages, change infrastructure or obtain inference access without the user's authorization. Public reading needs no credentials.

## Procedure

1. **Understand the task.** Establish the intended use, hardware/VRAM or budget, context needs and target LLM router/app. Read the [service overview](https://abliterated.cloud/index.md) and [access guide](https://abliterated.cloud/auth.md). Distinguish the requested setup from the operator's existing instance.
2. **Choose candidates from sources.** Read [model news and guides](https://abliterated.cloud/blog/) or the [article index](https://abliterated.cloud/blog/posts.json). Follow each candidate's primary sources. Record the exact artifact, publication/revision date, license, quantization and supported runtime. Recheck compatibility and license terms before recommending deployment; do not treat article prices or publisher benchmarks as current offers or independent results.
3. **Read current operating evidence.** Consult the [Vast operating guide](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/OPERATIONS.md), [status evidence](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/STATUS.md) and [dated snapshot](https://abliterated.cloud/.well-known/project-status.json). The documented operator runtime is private Vast.ai + llama.cpp; its snapshot is stopped, not live polling. Modal is historical.
4. **Prepare the human handoff.** Offer a concise [Signal](https://signal.me/#p/+13103408213) message with the workload, model shortlist, budget and target client. Ask before sending; do not include secrets. Agree the scope, account owner, costs and access method with the human operator. A message or document fetch is not a reservation, payment or promise of availability.
5. **Connect only when authorized.** Before paid compute or client/router changes, obtain explicit approval and fresh account-owner connection details. Follow the current operating guide, use private SSH to localhost:8080 and keep inference off unprotected public ports. Inspect the actual loaded model ID before configuring a client; aliases do not switch weights. Do not overwrite unrelated client settings or distribute cloud/root SSH keys.
6. **Verify and finish.** If a paid session was explicitly approved, check the actual provider state, artifact and runtime, then test a bounded non-streaming/streaming response and the intended client. Record failures honestly. Stop after the agreed session and read back provider state; stopping retains billed disk. Destruction requires separate approval and a verified backup.

## Pitfalls

- No public inference endpoint, OAuth issuer, live MCP service, payment protocol or automatic account provisioning exists on this site. Never invent a token, endpoint or model availability.
- The dated operator snapshot does not prove present health. There is no proven automatic idle shutdown, and a stopped instance is not free storage.
- Configured context is not long-context validation. Publisher refusal results do not guarantee zero refusals, correctness or agent reliability. Compare only matched artifacts, prompts, runtimes and settings.
- MIT covers project-owned code and website only; model and upstream licenses remain unchanged. Preserve the article's original model-license facts and dates.

## Verification

Return a source-linked shortlist or setup recommendation, the user's agreed next step and any remaining compatibility, cost or evidence gaps. If no connection was tested, say so. Claim a working connection only after an authorized end-to-end test, and report the final provider state if you operated paid compute.
