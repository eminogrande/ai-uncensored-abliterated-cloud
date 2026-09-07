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

The [operating guide](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/OPERATIONS.md) covers private Vast.ai + llama.cpp, with localhost:8080 reached through an operator-controlled SSH tunnel. Keep inference off unprotected public ports. The [dated snapshot](https://abliterated.cloud/.well-known/project-status.json) recorded the operator instance as stopped; it is not live telemetry or an availability promise.

Start and stop manually with explicit authorization. Verify provider state after each change. No automatic idle shutdown is proven. Stopping retains disk and ongoing storage charges; destruction is a separate, destructive action requiring separate approval. Old Modal tokens and wake routes are historical, not this runtime's access contract.

## References

- [Service overview](https://abliterated.cloud/index.md)
- [Model news and guides](https://abliterated.cloud/blog/)
- [Agent selection and connection skill](https://abliterated.cloud/skills/abliterated-cloud/SKILL.md)
- [Status evidence](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/STATUS.md)
