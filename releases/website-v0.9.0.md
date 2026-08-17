# ABLITERATED.cloud website v0.9.0 — Latest uncensored releases

## New homepage section

The landing page now carries a **Latest uncensored releases** section next to
the four-model catalog. It lists the ten newest covered abliterated releases
with an approximate managed price estimate per model, updated automatically
from the blog manifest.

## Ten new field notes

- **huihui-ai/Huihui-Qwen3.8-27B-abliterated** — the 48-hour abliteration race (≈ $5.45/h)
- **SHS-Lab/Muse-Glimmer-30B-Abliterated-Aggressive** — what "Aggressive" means (≈ $5.45/h)
- **jorkle/Muse-Glimmer-30B-Abliterated** — the base of the wave (≈ $5.45/h)
- **Resggg/Kimi-K3-Abliterated-modal** — the 2.78T-parameter abliteration nobody can run (≈ $87.20/h, speculative)
- **pocharlies/deepseek-v4-flash-0731-uncensored-abliterated-refusal-directions** — uncensored by dial (≈ $10.90/h)
- **huihui-ai/Huihui-CyberStrike-OffSec-35B-abliterated** — pentesting, refusals out (≈ $5.45/h)
- **insraq/Qwen3.5-4B-EmperoAI-Qwen3.8-Distill-Heretic-Abliterated** — small uncensored agents (≈ $2.34/h)
- **huihui-ai/Huihui-Qwen3.6-27B-abliterated** — the workhorse, four months in (≈ $5.45/h)
- **huihui-ai/Huihui-Qwen3.5-9B-abliterated** — the quiet classic (≈ $2.34/h)
- **huihui-ai/Huihui-GLM-4.6V-Flash-abliterated** — the MIT vision sleeper (≈ $2.34/h)

Every article is source-linked, pins an exact Hugging Face revision, labels
upstream benchmarks separately from publisher claims, and cites community
response where found. Prices are estimates, not quotes.

## Blog pagination

The blog index now paginates (nine posts per page) so every field note stays
reachable. Pagination pages are included in the sitemap and verified by the
agent-readiness checks.

## Publishing foundation

- One `blog/posts.json` manifest drives the blog index, RSS, sitemap,
  `llms.txt`, `llms-full.txt`, and the homepage releases section.
- `npm run build:blog` regenerates every discovery surface from the manifest.
- Markdown content negotiation now works on the homepage and every article.
- `auth.md` documents the anonymous agent registration flow.

## Agent-readiness

- Homepage and article Markdown negotiation verified locally and in preview.
- Article, pagination, and manifest routes covered by the local verifier.
- All 82 regression tests pass.
