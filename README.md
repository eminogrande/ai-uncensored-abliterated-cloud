# ABLITERATED.cloud website

A dependency-free, static website for private on-demand evaluation on Vast.ai with llama.cpp. No public inference service or hosted model catalog. No JavaScript, graphics background, animation, analytics, external fonts or health polling is needed to read or navigate it.

## Source of truth

- `.well-known/project-status.json`: dated operator snapshot, not live telemetry. Update only from evidence, without private keys, host addresses or account credits.
- `index.html`, `index.md`, `llms.txt`, `llms-full.txt`: the build synchronizes marked status and cost sections from that snapshot. The root README cost section is generated from the same rates.
- `blog/posts.json`: historical editorial metadata, not deployment inventory. Price estimates are explicitly historical; publisher refusal measurements are not a general guarantee.
- Article HTML/Markdown: original reporting, licenses and source links remain. The build adds consistent archive framing and navigation without rewriting article bodies.
- `openapi.json`: read-only public documentation resources only. No inference contract, model catalog, wake endpoint or credentials.
- Obsolete MCP, A2A, OAuth and WebMCP discovery cards are removed rather than advertising services that are not offered. The old optional Worker is preserved under `archive/edge/` and is not the current runtime.

## Local preview and verification

From the repository root:

```sh
python3 -I scripts/build-blog.py
python3 -I scripts/build-blog.py --check
uv run pytest tests/test_website.py -q
python3 -m http.server 8788 --bind 127.0.0.1 --directory website
```

With that server running:

```sh
node scripts/verify-agent-ready.mjs http://127.0.0.1:8788 --local-only
```

The verifier checks the real static-site contract, article routes, the snapshot, archive labels and reading indexes. Unit tests check generated pagination, local links, metadata, assets and discovery digests. Static Pages does not provide dynamic Link headers, Markdown content negotiation, MCP or OAuth; the retired Worker/scanner are archival only.

From a clean, signed `main` matching `origin/main`, publish with:

```sh
./scripts/deploy-website.sh website-vX.Y.Z
```

Use an unused version with curated notes under `website/releases/`. The script verifies tests, signatures, Pages configuration and the deployed build before creating the GitHub release. Read back public content as a final check; a local test or a Git push alone is not deployment.

## Editorial archive

Add an HTML/Markdown article pair and a dated `posts.json` entry with `content_status: editorial_archive`, then run the build and tests. Keep exact artifact identity, pinned revisions, per-model license facts and primary sources. Use `historical_estimated_usd_per_hour`, not a current-looking price field. Keep refusal claims scoped to their publisher, test and settings; never add a global zero-refusal badge.

The build generates paginated archive indexes, the RSS feed, sitemap and agent reading lists. The homepage shows only three article links, not the entire archive. `--check` fails if generated outputs are stale.

## Design and budgets

System fonts, semantic HTML, visible wrapping navigation at mobile widths, native links and keyboard focus styles. No JavaScript required. Critical homepage HTML, CSS and SVG identity assets must total less than 25 KB uncompressed. No hero asset request/preload, canvas, blur or decorative animation. Article tables scroll locally and long IDs wrap.

MIT covers project-owned website/code only. Upstream/model licenses are unchanged. Release notes remain historical and are labeled as such.
