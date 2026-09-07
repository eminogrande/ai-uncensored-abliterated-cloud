# Search and agent-readiness verification

## Scope

The service positioning is **Intelligence, freed.**: human-assisted uncensored and abliterated AI cloud GPU rental setup, self-hosting and LLM router/app integration. Original Signal contact: https://signal.me/#p/+13103408213.

The current website is static GitHub Pages. The private Vast.ai + llama.cpp reference instance is separately operated. Website scores are not proof of running inference or a publicly payable API.

## Live baseline, before this copy change

Measured 2026-09-06 at approximately 15:35–15:37 UTC against https://abliterated.cloud/.

| Scanner | Actual result | Scope |
| --- | --- | --- |
| PageSpeed Insights, mobile | Performance 100; accessibility 100; best practices 100; SEO 100; Agentic Browsing 100 | Lighthouse 13.4.1, fetch 15:35:23.511 UTC |
| PageSpeed Insights, desktop | Performance 100; accessibility 100; best practices 100; SEO 100; Agentic Browsing 100 | Lighthouse 13.4.1, fetch 15:35:23.947 UTC |
| isitagentready.com | 40/100 default UI; 38/100 exhaustive API | Default: 6 passing / 15 scored checks. Exhaustive: 6 / 16. Neutral checks excluded. |
| Circle Seller Readiness | 25/100 | Origin-hosted OpenAPI found; no payable operation. |
| is-agentic.com | 72/100 | Report timestamp 15:35:36.118 UTC; 29 eligible checks. |

PageSpeed's WebMCP audits were not applicable; its 100 does not mean WebMCP exists. None of these scores establishes search ranking, AI citation frequency or all-site performance.

## Implemented in this working change

- Restore exact headline, original Signal CTAs and service-first landing-page and Markdown copy. Add matching visible/structured FAQs, Organization and Service data.
- Keep the model blog active. Preserve article sources, dates and licenses; add self-hosting contact paths and real Markdown pagination.
- Add a real AI resource catalog, an `Auth.md` heading, public-document examples and concise OpenAPI agent guidance. Keep all advertised routes read-only and real.
- Add About, Contact and Privacy pages; maintain canonical URLs, sitemap and crawler access. No third-party scripts or background graphics.
- Preserve the dated stopped-GPU snapshot and distinguish reference provider rates from assistance pricing. No runtime, DNS or payment changes.

## Why universal 100 is not a copy-only deliverable

GitHub Pages does not provide configurable Link headers, Accept-based Markdown negotiation, API JSON errors or application rate-limit headers. These require an edge/server layer. The existing DNS-AID records lack validated DNSSEC; protocol records must describe actual deployed services before being signed or expanded.

OAuth discovery, MCP and WebMCP checks require real corresponding capabilities. They must not be implemented as static claims about nonexistent transports. A public-information service does not need a fictional login issuer.

Circle awards payment points for actual payable operations, protocol metadata, supported networks and a live unpaid HTTP 402. Human-assisted Signal enquiries do not meet that contract. Do not add fake prices, payment challenges or checkout endpoints solely to raise the score.

Infrastructure migration and a real agent-payable product are separate scope decisions. Re-run all public scanners after an approved deployment; pre-deploy and local results cannot be presented as post-deploy results.

## Local verification

The working change passed 16 current tests and 66 unchanged Modal archive tests. The generator check and local discovery verifier pass. All 35 HTML pages were rendered on desktop and iPhone emulation (70 renders), with no horizontal overflow and a Signal contact on every page.

Final local Lighthouse 13.4.1 measurements at 2026-09-06 16:00 UTC returned 100 in performance, accessibility, best practices, SEO and Agentic Browsing on both mobile and desktop. These are **local** results, not post-deployment public scores. The measured homepage SHA-256 is `097ea8efbaf18f38c0944c1c5b54e8411b0d2d1b9c866731d82dc1144c1c7b90`; assets were checked unchanged across measurement. Independent review returned GO for user preview.

User visual QA precedes merge/deployment. Full local scan and screenshot artifacts are held outside the deployable website, under the local `abliterated-score-review` directory. No 100/100 claim for all four public scanners is made.
