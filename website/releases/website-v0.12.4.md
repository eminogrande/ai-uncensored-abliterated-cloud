# website-v0.12.4 — Exact numbers in plain-language facts

2026-09-07

## Why

An independent truth review of the plain-language rewrite found ten statements
that softened a measured value or dropped a qualifier that changes the claim.

## Changed

- Throughput restored as aggregate across 8 parallel requests, not single-stream speed.
- Ornith 0 of 16 refusals labelled as keyword screening, not human review.
- Bonsai 1.125 bits per weight stated exactly; benchmark deltas and KL drift values
  restored; DeepSeek 256K context claim named.
- No article text, evidence excerpts, sources or dates changed.

## Checks

28 root tests, generator check, secret scan, diff check. No GPU start, payment
service or DNS change.
