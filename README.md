# ABLITERATED.cloud

**Intelligence, freed.** Model research and human-assisted hosting of uncensored
and abliterated models. [Website](https://abliterated.cloud/) ·
[Model news](https://abliterated.cloud/blog/) ·
[Setup help on Signal](https://signal.me/#p/+13103408213)

## Private on-demand endpoint

**Private chat and full deletion are verified.** On 2026-09-27, MCP started the
model, a streamed router request returned the correct result for 17 × 23, and
Off removed the workers and their temporary storage. Cold start took about
15 minutes. Final inventory: zero instances, owned endpoints and workergroups.
The real 21-minute idle cycle and Pi tool calling remain unverified; this is not
a public self-service endpoint. See [the evidence](docs/STATUS.md).

The owner integration is behind **`router.paymentrequired.com`**, not the static
website. Its implementation lives in the
[router repository](https://github.com/nuri-com/router-paymentrequired-com/tree/feat/abliterated-controls).
This repository contains the website, operating instructions and dated evidence.

- **Controls:** [Start / fully off](https://router.paymentrequired.com/abliterated/).
  A private router bearer is required; the page does not issue credentials.
- **OpenAI-compatible base URL:** `https://router.paymentrequired.com/v1/internal`.
- **Model ID:** `abliterated/qwen3.8-27b`.
- **Configured weights:** `OBLITERATUS/Qwen3.8-27B-OBLITERATED`, revision
  `a58c3b53b3ce71551eafde2ed5ec8df48e0f4ff8`, vLLM, 32768-token context.
  This is the new serving configuration, not the old Q6_K GGUF/llama.cpp instance.
- **Verification:** see [status and evidence](docs/STATUS.md). A working panel or
  model-catalog entry does not by itself prove inference or tool calling.

Access remains private and human-assisted. There is no public signup, self-service
API-key issuance, checkout or GPU management key in the website.

## What Start and Off mean

1. **Start / enable automatic operation** creates an endpoint configuration and
   permits authorized inference to recruit a GPU. Model download and loading can
   take several minutes. Opening the website, polling status or running router
   background probes does not start this model.
2. **Automatic idle cleanup** deletes the endpoint and its temporary workers after
   21 minutes without active router requests, checked every 30 seconds. Automatic
   operation stays enabled, so a later authorized inference can start again.
3. **Manual Off** first blocks automatic restarts and aborts active requests. It
   then deletes this endpoint and its workers, including temporary model storage.
   Pi requests cannot override manual Off; enable Start again explicitly.
4. **Wait for confirmed removal.** Cleanup failures remain visible and are retried.
   Do not assume zero resource costs while cleanup is pending. After confirmed
   removal, no GPU worker or worker disk is retained for this endpoint.

The existing router server remains separately billed. Model loading, active time,
the idle grace period and transfer can cost money. This is not a zero-cost service
or a zero-cost cold start. No standalone storage volume is created by this setup.
Keep unique files outside disposable workers.

This differs from ordinary Vast **Stop**, which retains a container disk that is
**still billed while stopped**. The new Off control deliberately uses deletion,
not pause. Never apply that deletion policy to unrelated instances or unique data.

[Operating guide](docs/OPERATIONS.md) · [Implementation audit and design](docs/ENDPOINTS.md)

## Connect Pi

Merge this provider into `~/.pi/agent/models.json`; preserve unrelated providers:

```json
{
  "providers": {
    "abliterated": {
      "baseUrl": "https://router.paymentrequired.com/v1/internal",
      "api": "openai-completions",
      "apiKey": "${ABLITERATED_ROUTER_KEY}",
      "models": [{
        "id": "abliterated/qwen3.8-27b",
        "name": "Abliterated Qwen3.8 27B (Vast on demand)",
        "reasoning": false,
        "input": ["text"],
        "contextWindow": 32768,
        "maxTokens": 4096
      }]
    }
  }
}
```

Provide the private **router** key through your environment or secret store, never
the Vast management key. `/model` reloads model definitions. Start with a fresh
session; an existing frontier-model conversation may exceed this model's context.
A client-side alias or context setting does not change the loaded weights.

For long cold starts, Pi supports `httpIdleTimeoutMs: 1800000` in its settings;
this is a global 30-minute timeout, not a per-provider setting. Use a smaller
per-model compaction budget for this 32K model. Pi's token-cost display does not
measure hourly GPU charges. Configuration is not proof of agent reliability.

## Cost

Current Vast offers vary. The owner template allows one worker maximum, with a
GPU-offer search ceiling of $2.50/hour and bounded transfer-price filters. This is
not a total spending cap: storage during use, transfer and taxes are separate.
Confirm current rates before enabling a session.

The following is a **historical retained-instance quote from 2026-09-05**, not the
current on-demand tariff or an assertion that this A100 still exists. The private
**Vast.ai + llama.cpp** path is historical. Its disk charge explains why pause was
not sufficient for the new zero-retained-resource requirement.

<!-- RUNNING-COSTS -->
| Usage | Cost |
| --- | ---: |
| Running: GPU + disk / hour | **$0.63333** |
| Running continuously / 24 hours | **$15.20** |
| Running continuously / 30 days | **$456.00** |
| Stopped: retained disk / 30 days | **$24.00** |
| 2 hours running per day / 30 days, disk retained throughout | **$60.00** |

USD, contract quote checked 2026-09-05. GPU $0.60/hour plus storage $0.03333/hour. Stopped disk: $0.80/day. Two hours/day for 30 days: $36.00 GPU + $24.00 disk. GPU time is billed while running, even without requests. Storage is billed continuously. Bandwidth, applicable taxes and other services are excluded. This historical manual setup had no automatic idle shutdown.
<!-- /RUNNING-COSTS -->

## Evidence limits

- **No universal zero-refusal guarantee.** Publisher claims and small probes do
  not establish general refusal rates, coding quality or agent reliability.
- **No validated 262k workload.** Historical `262144` settings were not proof of
  long-context quality. The new template is configured for 32768 tokens.
- The model-news catalog is not an inventory of hosted models. Licenses,
  benchmark claims and estimates retain their publication dates and sources.
- The old `api.abliterated.cloud` gateway is not the new router entry point.
  Its unsafe SSH wake path was disabled. Open PR #18 is historical experimental
  code, not the deployed native-Serverless implementation.
- Modal is retired from this project's operating path. Its
  [archive](archive/modal/README.md) is not a current setup guide or proof that
  all historical Modal resources have been decommissioned.

## Website development

```sh
uv sync --group dev
uv run python -I scripts/build-blog.py
uv run pytest -q
python3 -m http.server 8788 --bind 127.0.0.1 --directory website
```

Open `http://127.0.0.1:8788/`. Reading or building the static site does not start a
GPU. [Website guide](website/README.md) · [Agent reading index](website/llms.txt)

## License and history

Project-owned code, documentation and website are [MIT licensed](LICENSE).
Earlier Apache-2.0 releases retain their terms. Model weights, dependencies and
third-party material retain their upstream licenses; see
[licensing scope](docs/LICENSING.md). [Changelog](CHANGELOG.md) ·
[Release history](docs/RELEASE_NOTES.md)
