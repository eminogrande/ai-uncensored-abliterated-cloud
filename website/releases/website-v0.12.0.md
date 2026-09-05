# ABLITERATED.cloud website v0.12.0

Vast.ai is the only current operating path. Modal is retired and not in use because its cost did not fit this experiment.

## Vast-only, with a lighter website

The front page now describes our actual private Vast.ai + llama.cpp experiment.
It no longer advertises the old Modal model catalog as the current operating path.
Model field notes remain available as an explicitly labeled editorial archive.

Removed the animated canvas, background illustrations and runtime JavaScript.
The site uses native navigation, system fonts and static HTML/CSS. No GPU request,
external font service, analytics or application bundle is needed to read it.

## Correct status and costs

The 2026-09-05 provider snapshot found one stopped A100 instance. The retained disk
still costs approximately $0.80/day, or $24 per 30 days. Running costs $0.63333/hour including GPU and disk: $15.20/day or $456 per 30 days continuously. Two hours of GPU use daily costs $60 per 30 days with disk retained. Bandwidth, applicable taxes and other services are excluded. Four legacy Modal apps have
zero tasks but remain deployed. Archiving source does not delete cloud resources.

A configured 262144 context, short historical smoke tests and a model named
"uncensored" do not establish full-context reliability or a zero-refusal guarantee.
No model was started, benchmarked or destroyed for this website update.

## Archive and licensing

The old Modal implementation, CLI, configs, tests and operating documents are
preserved under `archive/modal/`. The old optional Worker and decorative assets
are also archived, not part of the production site payload.

Our own code, documentation and website now use MIT. Previous releases keep their
original Apache-2.0 terms; model weights, dependencies and third-party materials
keep their respective licenses.

## Review and deployment

The current root README, OPERATIONS, STATUS, LICENSING and CHANGELOG documents
explain the changes and remaining limits. Local tests and desktop/mobile previews
are checked before the separate signed Pages deployment. Local tests do not start inference.

Local verification: 13 current tests and 66 archived tests passed. All 31 HTML pages
were rendered at desktop and iPhone 13 sizes (62 renders), without page horizontal
overflow. The homepage transferred 21,603 bytes versus 97,081 bytes for the baseline
in cold local Chrome contexts, approximately 77.75% less. This is a local payload
comparison, not an Internet latency or model-speed benchmark.

[Verification evidence](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/evidence/website-v0.12.0-checks.json)


[Full changelog](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/CHANGELOG.md)
· [Operating guide](https://github.com/eminogrande/ai-uncensored-abliterated-cloud/blob/main/docs/OPERATIONS.md)
