# Auth.md

ABLITERATED.cloud offers human-assisted cloud GPU renting, self-hosting and LLM router/app integration for uncensored and abliterated models. [Talk on Signal](https://signal.me/#p/+13103408213) to agree a model, budget, provider/account and client before setup.

## Public documents: no authentication

The service overview, model news and guides, Markdown files, resource catalogs and dated status snapshot are public read-only documents. **No authentication is required:** no API key, bearer token, OAuth flow, account or payment is needed to read them. [OpenAPI](https://abliterated.cloud/openapi.json) describes only these static document GETs, not inference.

The site does not issue inference credentials or OAuth tokens, register agents, accept automated payments, or provide account checkout, a public inference endpoint or a live MCP service. A Signal enquiry starts a human conversation; it is not an API provisioning or payment request.

## Human-assisted private setup

1. Share your intended workload, candidate model, available hardware or budget, and the LLM router/app you want to connect. Do not put secrets in a public issue or document.
2. Agree the scope, provider/account, spending limit and access method with the operator. Obtain explicit user consent before sending messages, provisioning resources or changing client configuration.
3. Use credentials supplied by the authorized account owner through an agreed private channel. This website does not grant account access or issue tokens. Never distribute root SSH keys or cloud account keys to inference clients.
4. Verify the actual runtime, loaded artifact and a bounded response before treating the connection as usable. Reading a document or submitting an enquiry does not establish inference availability.

## Currently documented runtime

The [operating guide](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/OPERATIONS.md) describes the private Vast Serverless/vLLM integration. [Owner controls](https://router.paymentrequired.com/abliterated/) and `https://router.paymentrequired.com/v1/internal` require the owner's router bearer. The page keeps that bearer only in tab memory. Never use the Vast management key as a client key.

Enable paid operation only with explicit authorization. Manual Off blocks restarts and deletes this endpoint's workers and temporary storage; confirm the destructive action and wait for verified removal. Automatic idle cleanup leaves later authorized wake-up enabled. The router server is separately billed. Ordinary Vast Stop retains billed disk and is not this Off control.

The [dated snapshot](https://abliterated.cloud/.well-known/project-status.json) describes the older retained instance, not current availability. Old Modal tokens, SSH tunnels and wake routes are historical. See status evidence for completed end-to-end tests.

## References

- [Service overview](https://abliterated.cloud/index.md)
- [Model news and guides](https://abliterated.cloud/blog/)
- [Agent selection and connection skill](https://abliterated.cloud/skills/abliterated-cloud/SKILL.md)
- [Status evidence](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/STATUS.md)
