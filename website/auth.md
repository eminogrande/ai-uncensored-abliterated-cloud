# Auth.md — ABLITERATED.cloud authentication

ABLITERATED.cloud uses revocable Bearer access tokens for the OpenAI-compatible inference API.

## Request header

```http
Authorization: Bearer sk-mn-...
```

The public website never contains or retrieves a token.

## Token behavior

- A missing token returns an OpenAI-style `401` error.
- An invalid or revoked token returns an OpenAI-style `401` error.
- Tokens are created and revoked by the operator.
- The shared gateway stores token digests, not recoverable plaintext tokens.
- User tokens are separate from Modal account credentials.
- Gateway-to-backend proxy credentials are separate from user tokens.

## Lifecycle requirement

A valid token cannot wake a hard-stopped route. The operator must explicitly arm or start one model first.

The 397B route additionally requires explicit operator cost acknowledgement for start, automatic mode, wake, or agent launch.

## Public agent registration

Agents can register anonymously for a read-only website credential. This does not authorize model inference.

### Step 1 — discover

```http
GET https://abliterated.cloud/.well-known/oauth-protected-resource
Accept: application/json
```

```http
GET https://abliterated.cloud/.well-known/oauth-authorization-server
Accept: application/json
```

The authorization metadata publishes:

- `agent_auth.skill`: `https://abliterated.cloud/auth.md`
- `agent_auth.register_uri`: `https://abliterated.cloud/agent/auth`
- `agent_auth.identity_types_supported`: `anonymous`
- `agent_auth.anonymous.credential_types_supported`: `access_token`

### Step 2 — register

```http
POST https://abliterated.cloud/agent/auth
Content-Type: application/json
Accept: application/json

{"type":"anonymous","requested_credential_type":"access_token"}
```

The response contains an `access_token` credential with the single scope `public:read`. Public HTML, Markdown, model metadata and MCP tools remain readable without it. The model API itself uses operator-issued Bearer tokens; inference OAuth is not implemented.

## Request access

Contact through Signal and mention ABLITERATED.cloud:
https://signal.me/#p/+13103408213
