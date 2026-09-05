# ABLITERATED.cloud

**Private, on-demand inference on Vast.ai + llama.cpp.** The public website is
static documentation and model field notes, not an inference API or model host.

[Operating guide](docs/OPERATIONS.md) · [Status evidence](docs/STATUS.md) ·
[Website](https://abliterated.cloud/)

## Current state

**A100 STOPPED — state and rates rechecked 2026-09-05 at 20:12 UTC.** No inference
was tested. This [read-only snapshot](docs/evidence/2026-09-05-vast-recheck.json)
is not a live uptime monitor.

| Component | State |
| --- | --- |
| Vast instance | One A100 PCIe 40 GB, actual `exited` / intended `stopped`; no running GPU in the account inventory. The previous V100 is no longer listed. |
| Storage | 120 GB container disk, retained and **still billed while stopped**. No separate volume was provisioned. |
| Last serving configuration | `OBLITERATUS/Qwen3.8-27B-OBLITERATED`, `Qwen3.8-27B-OBLITERATED-Q6_K.gguf`, llama.cpp. Recorded configuration, not a model serving today. |
| Access | Private SSH tunnel to `http://127.0.0.1:8080/v1`; the local endpoint was unreachable at the earlier 19:39 UTC audit. |

Modal is **retired and not in use for this project because of its cost budget**,
not because Modal is universally the most expensive provider. The implementation
is [archived](archive/modal/README.md), not decommissioned: four legacy apps remained
deployed with zero tasks in the [19:39 UTC audit](docs/evidence/2026-09-05-status.json),
which also checked local health. Remaining Modal storage/other charges were not audited.

## Cost

Rates from the [20:12 UTC Vast recheck](docs/evidence/2026-09-05-vast-recheck.json).
Hourly quotes are rounded; estimates assume unchanged rates and exclude variable
transfer charges, taxes and other provider fees. Running rates are not the current
stopped bill.

<!-- RUNNING-COSTS -->
| Usage | Cost |
| --- | ---: |
| Running: GPU + disk / hour | **$0.63333** |
| Running continuously / 24 hours | **$15.20** |
| Running continuously / 30 days | **$456.00** |
| Stopped: retained disk / 30 days | **$24.00** |
| 2 hours running per day / 30 days, disk retained throughout | **$60.00** |

USD, contract quote checked 2026-09-05. GPU $0.60/hour plus storage $0.03333/hour. GPU time is billed while running, even without requests. Storage is billed continuously. Bandwidth, applicable taxes and other services are excluded. No automatic idle shutdown.
<!-- /RUNNING-COSTS -->

**Stop retains the disk and ends GPU compute billing; destroy deletes the instance
and its container disk.** A normal pause is a stop, never a destroy.

## Use the one operating path

```text
Local browser / Pi / OpenCode / Hermes
  -> localhost:8080 (private SSH tunnel)
  -> Vast.ai A100 + llama-server -> one selected GGUF

GitHub Pages: documentation only, separate from inference
```

1. Inspect the account state and current rate before starting paid compute.
2. Start the existing instance deliberately; verify the server, model identity,
   tunnel and a bounded response. Model autostart is not verified.
3. Use the built-in llama-server browser UI for plain chat, or Pi/OpenCode for a
   coding workflow. A client alias does not load or switch model weights.
4. Stop after use and read back the actual cloud state. **Automatic idle shutdown
   is not verified**; disk billing continues.

The [operating guide](docs/OPERATIONS.md) contains the commands and client setup.
It is the only current runtime guide; archived deployment instructions are not
part of this path.

## Evidence limits

- **No universal zero-refusal guarantee.** Publisher claims and small prompt probes
  do not establish general refusal rates, coding quality or agent reliability.
- **No validated 262k workload.** `262144` is a recorded context setting, not proof
  of long-context quality. Model/build pins and controlled speed benchmarks are missing.
- **No public multi-user product.** No public authenticated Vast inference endpoint,
  per-user quotas, prepaid billing or production availability commitment is deployed.

[Status](docs/STATUS.md) records what was checked and what still needs a paid-session
test. Historical field notes are editorial coverage, not a hosted-model catalog.

## Work on the website

```sh
uv sync --group dev
uv run python -I scripts/build-blog.py
uv run pytest -q
python3 -m http.server 8788 --bind 127.0.0.1 --directory website
```

Open `http://127.0.0.1:8788/`. Reading the static site requires no GPU, inference
call, external font service or background artwork. See the
[website guide](website/README.md) for publishing and verification.

Current operations and evidence live in `docs/`; site content in `website/`;
build, verification and signed Pages publishing helpers in `scripts/`; checks in
`tests/`. `archive/modal/` is historical. This repository is the documentation
source of truth, not stale status JSON or "live" badges in the earlier
`ai-uncensored-selfhost` experiment repository.

## License and history

Our own code, documentation and website are [MIT licensed](LICENSE) from this
release. Previous Apache-2.0 releases keep their terms; that license was a project
choice, not a Vast.ai, Modal or llama.cpp requirement. Model weights, dependencies
and third-party materials retain their upstream licenses; see
[licensing scope](docs/LICENSING.md).

The [changelog](CHANGELOG.md) and [release notes](docs/RELEASE_NOTES.md) preserve
release history and earlier claim corrections without changing the current path.
