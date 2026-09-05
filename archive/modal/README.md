# Modal archive — retired, not in use

**The current operating path is Vast.ai + llama.cpp:** use the
[root README](../../README.md) and [operating guide](../../docs/OPERATIONS.md).
Modal was retired for this project's cost budget, not because it is universally
the most expensive provider. This directory is historical source, not a current
inference deployment or a website installation step.

**Source archival is not cloud decommissioning.** The
[2026-09-05 19:39 UTC audit](../../docs/evidence/2026-09-05-status.json) records four
remaining deployed Modal apps with zero tasks; storage/other charges were not
audited. No cloud resources were moved or deleted. Any resource removal requires
a separate owner-authorized action.

## Provenance

Frozen source: `2888dbfb99b81a87ceadb937d29ac2c61632619d`, the fetched `origin/main`
when the archive was made. This identifies source, **not proof of deployment**.
[MANIFEST.json](MANIFEST.json) records original/archive paths, original and retained
SHA-256 values, and the limited archival adjustments.

Legacy-only files were moved together; shared root material was copied from that
revision before the root was updated. No model weights, credentials, environments
or runtime state are included. Preserved contents:

| Location | Purpose |
| --- | --- |
| `modal_gateway.py`, `modal_vllm.py`, `src/mn_uncensored/` | Modal/vLLM entry points; legacy `mn` CLI, gateway, settings and security helpers |
| `config/`, `scripts/` | Model catalog, Pi settings, installation/deployment helpers and shared secret-scanner snapshot |
| `tests/`, `pyproject.toml`, `uv.lock` | Isolated legacy unit tests, Python project and original dependency resolution |
| `test_endpoint.py`, `run-pi.sh`, `deployment.env.example` | Historical endpoint/interactive helpers and environment example |
| `docs/`, `CHANGELOG.md`, `SECURITY.md` | Old operations, attribution, releases, cost incident and security records |
| `README.original.md` | Byte-for-byte original README; not current instructions |
| `.gitignore`, `.dockerignore` | Original local-state exclusions, scoped to this archive |

Original document paths such as `website/` and `LICENSE` refer to the frozen
revision's root; use Git at that revision for link context. Historical "current",
"live", "deployed", prices and model counts are not present-day assertions.
Disagreements between old notes and configuration, including the 397B
`deployment_enabled` policy, are preserved rather than silently corrected.

## Local unit tests only

From this directory:

```sh
uv sync --locked --group dev --python 3.11
uv run --locked python -m pytest -q
```

This project has its own `.venv`. The root [website checks](../../README.md#work-on-the-website)
are separate. Legacy tests import the editable `src/mn_uncensored` package, use
adjacent configs/scripts and mock backend/network/lifecycle behavior. Pytest
collects `tests/`, not `test_endpoint.py`, which makes a real endpoint request.
Dependency installation downloads packages; the unit suite requires no Modal
authentication, model downloads or GPU.

Do **not** validate the archive with `test_endpoint.py`, `scripts/smoke-catalog.py`,
`mn start/auto/wake`, `run-pi.sh`, secret-sync or deployment scripts: they can contact
services, change credentials, start billable compute or publish releases. The
macOS installer changes `~/.local/bin/mn`. These tools were not executed during
cleanup and are not recommended current operations.

## Relocation and licensing

Moving the complete layout preserves source-relative `PROJECT_ROOT`, catalog,
helper and `.venv` lookups. `extract-release-notes.py` reads the archived changelog;
`check-secrets.sh` resolves the real Git root for staged paths. Archive ignores
retain Pi credential/state exclusions. Only archive labels, package
license/description metadata and the nested secret-scanner path resolution differ
from the frozen source, as recorded in the manifest; no lifecycle behavior was added.

The owner's archived code is covered by the current root [MIT license](../../LICENSE).
The original revision and historical releases retain their Apache-2.0 terms;
[the original license text](../licenses/Apache-2.0.txt), historical README and release
statements remain preserved. Metadata changes do not rewrite old releases or
relicense third-party code, dependencies, weights or upstream notices. See
[current licensing](../../docs/LICENSING.md) and [model attribution](docs/MODELS.md).
