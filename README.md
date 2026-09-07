# ABLITERATED.cloud website

**Intelligence, freed.** A static service website for human-assisted cloud GPU renting and self-hosting of uncensored and abliterated models, with LLM router/app integration help. [Signal](https://signal.me/#p/+13103408213) is the human contact path; the blog publishes model news and practical guides. No public self-service inference or checkout is offered.

## Current operating docs and sources of truth

- [Operating guide](../docs/OPERATIONS.md): the current private Vast.ai + llama.cpp path, SSH access, client setup and manual start/stop.
- [Status evidence](../docs/STATUS.md): the operator's dated checks, not live telemetry. The retained instance was stopped at the recorded audit.
- `.well-known/project-status.json`: canonical operating snapshot. Update only from evidence, without credentials, private host details or account credits. Its scope is the operator runtime, not the whole service or publication.
- `index.html`, `index.md`, `llms.txt`, `llms-full.txt`: service overview and reading guides. The build owns the marked status, cost and article-link sections. The root README cost section uses the same rates. Do not hand-edit generated blocks.
- `blog/posts.json` and article HTML/Markdown: an active publication, not deployment inventory. Preserve exact model IDs, publication/revision dates, primary sources, per-model licenses and historical price/benchmark context. The legacy `content_status: editorial_archive` field describes retained dated reporting, not a discontinued blog.
- `openapi.json`: public read-only document GETs, explicit no authentication, with document examples. No inference, model-loading, payment or account API.
- `.well-known/ai-catalog.json`: real overview, current documentation, skill and model-news resources, each with a stable identifier, media type and representative queries.
- `skills/abliterated-cloud/SKILL.md`: choosing models, reading sources and arranging a human-consented connection. Regenerate its discovery digest after edits.

## Costs and limits

The [root README cost table](../README.md#cost) shows dated example infrastructure costs, not a service quote. Agree assistance scope and current provider charges before spending. Manual start/stop is required; stopped disk remains billed and automatic idle shutdown is unverified.

Public reading is unauthenticated. Private runtime access needs separate authorization; the site does not issue API keys, offer OAuth, run a public MCP/A2A service or accept automated payments. Static Pages cannot implement `Accept: text/markdown` negotiation or configurable discovery response headers. Explicit Markdown URLs and honest catalogs do not imply those features, and no scanner score is guaranteed.

## Local preview and verification

From the repository root:

```sh
python3 -I scripts/build-blog.py
python3 -I scripts/build-blog.py --check
uv run pytest tests/test_website.py tests/test_current_docs.py -q
python3 -m http.server 8788 --bind 127.0.0.1 --directory website
```

With that server running:

```sh
node scripts/verify-agent-ready.mjs http://127.0.0.1:8788 --local-only
```

The build synchronizes generated sections, pagination, RSS, sitemap and discovery digests. Tests cover local links, metadata, assets, evidence and read-only discovery. `--check` detects stale outputs. Reading or building the site never requires a GPU or inference call. The old optional Worker and protocol implementations under `archive/` are historical, not current services.

## Model news and guides

Add an HTML/Markdown article pair and a dated `posts.json` entry using the existing `content_status: editorial_archive` metadata convention, then build and test. Keep article bodies, original model-license facts and evidence dates intact when refreshing shared navigation or notices. Use `historical_estimated_usd_per_hour`, not a current-looking price field. Scope refusal claims to the publisher, test and settings; never add a global zero-refusal badge.

Keep the homepage's latest links selective and let the paginated blog indexes, RSS and agent reading lists expose the full publication. The AI catalog should link only real resources; do not invent MCP, OAuth or payment endpoints to satisfy a scanner.

## Publish

From a clean, signed `main` matching `origin/main`, with an unused version and curated notes under `website/releases/`:

```sh
./scripts/deploy-website.sh website-vX.Y.Z
```

The script verifies tests, signatures, Pages configuration and the deployed build before creating the release. Read back public content after an authorized deployment; a local test or Git push alone is not deployment proof.

## Design and licensing

Use system fonts, semantic HTML, visible wrapping navigation, native links and keyboard focus styles. No JavaScript, external fonts, health polling, background artwork or animation is required. Critical homepage HTML, CSS and SVG identity assets must total less than 25 KB uncompressed. Article tables scroll locally and long IDs wrap.

MIT covers project-owned website/code only. Upstream/model licenses and attributed third-party materials keep their terms. Release notes and retired implementation docs remain historical.
