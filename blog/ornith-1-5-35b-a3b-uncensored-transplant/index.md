# One base, three uncensors: the Ornith-1.5 task-vector transplant

Published 20 August 2026. Exact artifact: `0xKitkat/Ornith-1.5-35B-A3B-Uncensored`, revision `9ce64447864049ac16f7546265ae11d2a04fe9fb`.

DeepReinforce's Ornith-1.5-35B-A3B trains itself — it generates its own tasks, builds its own scaffolds and rolls out its own solutions for reinforcement learning. Two days after release, the uncensoring community attacked it three different ways: one edit used a task-vector transplant, taking the "uncensoredness" of a Qwen model and adding it to Ornith's weights like arithmetic; the other two used classic refusal-direction projection. The transplant one is the only one with measured numbers: 0/16 heuristic refusals on a Q4_K_M build, 4/4 capability passes.

## The base: a model that writes its own homework

The [official Ornith-1.5 card](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B) and the [release blog post](https://ornith.ai/ornith_1_5.html) describe the family in one phrase: a major step toward building foundation models through end-to-end self-improvement. Where Ornith-1.0 optimized a fixed human-curated task set through scaffold and rollout optimization, 1.5 expands the loop — the model proposes new training tasks, generates task-specific scaffolds, and produces solution rollouts, then improves its policy with reinforcement learning on all three. That is the lineage of the model this site covered as [Ornith 35B](ornith-1-0-35b-abliterated/) and [Ornith 397B](ornith-1-0-397b-abliterated-w4a16/); 1.5 is the same family, one loop deeper.

Architecturally it stays Qwen3.5-MoE-shaped: 40 hybrid layers — 30 linear-attention blocks (Gated DeltaNet class, with a 4-wide convolution) and 10 full-attention blocks at every fourth layer — 256 routed experts with 8 active per token plus a shared expert, a 27-layer vision encoder, and a multi-token-prediction (MTP) head. The pinned base [configuration](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B/raw/main/config.json) puts the total at 35,951,822,704 parameters, ~3.1B active, in a 262,144-token native context. Publisher-reported numbers: Terminal-Bench 2.1 67.8 (Terminus-2 harness) and 68.5 (Claude Code harness), SWE-bench Verified 79, SWE-bench Pro 59.6, SWE-bench Multilingual 71.4, DeepSWE 22, Frontier-Bench 5.1 — beating Qwen3.6-35B-A3B across the board on the same card's table. The base is MIT-licensed, 1,713 downloads and 241 likes in its first three days.

## Method one: transplant a task vector

The most interesting edit came from [0xKitkat](https://huggingface.co/0xKitkat/Ornith-1.5-35B-A3B-Uncensored) on 20 August, and it is not an ablation in the usual sense. The card describes a *streamed task-vector transplant*:

```
output = Ornith-1.5 + 1.0 × (Qwen3.6-Abliterated − Qwen3.6-Base)
```

The donor delta comes from [wangzhang/Qwen3.6-35B-A3B-abliterated](https://huggingface.co/wangzhang/Qwen3.6-35B-A3B-abliterated), an Abliterix-produced edit whose own card documents LoRA rank-1 steering, expert-granular ablation, router suppression, orthogonalized steering vectors and a Gaussian layer decay, with a measured 7/100 refusals (LLM-judged) at KL 0.0189. 0xKitkat's formula subtracts the unedited Qwen base from its abliterated sibling — isolating what "uncensoring" did to Qwen's weights — and adds exactly that difference to Ornith. Because both share the Qwen3.5-MoE architecture, only name-and-shape-compatible tensors are eligible: 1,811 target tensors, 693 compatible, of which 102 were actually modified; the other 591 compatible tensors were left unchanged, and all 1,118 Ornith-only tensors — the vision tower, the MTP head, the self-improvement-specific post-training — were copied through untouched.

All arithmetic ran in float32 and rounded once to BF16. The repository ships `task_vector_report.json` with per-shard SHA-256 hashes and the 100 largest deltas, and `validation_report.json` covering checkpoint validity, a NaN/Inf scan of all 71.9 GB of scanned weights, and a llama.cpp smoke evaluation of the Q4_K_M build: 16 refusal prompts, 0 heuristic refusals (no-refusal rate 1.0), 4 capability prompts, 4 passes. The method is disclosed: public prompts, deterministic generation, a regex screen. That is a real measurement, and a modest one — 20 prompts total, heuristic rather than LLM-judged.

## Method two and three: the classic projections

The same base got two conventional orthogonalization edits within hours. [alztrk's](https://huggingface.co/alztrk/Ornith-1.5-35B-A3B-Abliterated) variant projects the refusal direction out of attention and MLP down-projection matrices across all 40 layers, then ships a dynamic GGUF ladder — Q3_K_M 15.61 GB, Q4_K_M 19.71 GB, Q5_K_M 23.03 GB, Q8_0 34.37 GB — with attention matrices kept at higher precision while MoE feed-forwards are quantized. That Q4_K_M fits a 12–16 GB consumer GPU. [pottokao's](https://huggingface.co/pottokao/Ornith-1.5-35B-A3B-abliterated) variant is the classic single-direction ablation — 64 harmful plus 64 harmless prompts, probe layer 24, the refusal direction subtracted from every output projection — exported text-only (no vision tower, no MTP head) at 65 GB BF16, with an NVFP4 sibling at 20 GB that runs on 2×16 GB GPUs and carries its own benchmarks.

Three teams, one base, three philosophies: reuse someone else's measured uncensoring delta (0xKitkat), project a freshly probed direction out of every layer (alztrk), or project one direction out of the cleanest possible text-only export (pottokao). Only the transplant has a published refusal number.

## What the transplant numbers do and don't say

0/16 heuristic refusals on a Q4_K_M build is the only measured number in the set — but the evaluation ran 20 prompts in total, used regex screening rather than an LLM judge, and measured a quantized build rather than the BF16 artifact. The wangzhang donor card itself carries a warning worth quoting: many abliterated models claim near-perfect scores, and numbers without fully documented methodology deserve skepticism. The transplant's 102 modified tensors are a real, inspectable claim — the report file lists every one of them with hashes — but "no refusals on these 16 prompts" is not "no refusals."

Also unmeasured so far: what the transplant did to Ornith's self-improvement behavior. The 1,118 Ornith-only tensors were preserved, which is the right kind of claim, but nobody has rerun Terminal-Bench on the edited weights. The base's coding numbers belong to the unedited checkpoint; the edit's capability retention is asserted by construction, not measured.

## How to run it

The pinned repository is a standard transformers checkpoint — 16 BF16 shards, vision tower and MTP head included:

```
vllm serve 0xKitkat/Ornith-1.5-35B-A3B-Uncensored --limit-mm-per-prompt image=4 \
  --max-model-len 131072 --tensor-parallel-size 1
```

For consumer hardware, [alztrk's GGUF suite](https://huggingface.co/alztrk/Ornith-1.5-35B-A3B-Abliterated) is the practical path: the dynamic Q4_K_M is 19.71 GB and the card includes a ready Ollama Modelfile, so `ollama create ornith-35b-abliterated -f Modelfile` then `ollama run ornith-35b-abliterated` gets you the same spirit of model on one GPU. Safety filtering is significantly reduced in all three edits — that is the point of them. ABLITERATED.cloud's prepared profile pins revision `9ce64447864049ac16f7546265ae11d2a04fe9fb` with a conservative 131,072-token context on one H200 at an approximate managed price estimate of $5.45/hour.

## The creator: 0xKitkat

The publisher's model card says to follow [@procrastiness](https://twitter.com/procrastiness) on X for new model releases and updates. The Hugging Face user API returns no profile page for 0xKitkat at the time of writing, and the card carries no biography, funding links or team details — so we state exactly that: an individual operator, working solo, who publishes task-vector edits with unusually complete machine-readable reports. The base itself comes from the DeepReinforce team publishing as [ornith-ai](https://huggingface.co/ornith-ai), the same group behind Ornith-1.0, whose self-improvement research blog ([ornith.ai/ornith_1_5.html](https://ornith.ai/ornith_1_5.html)) documents the training loop the way a paper would.

## The idea, in plain words

**A task vector is a recipe for "one model, minus another"** — If you take an abliterated model's weights and subtract the original model's weights, what's left is a direction describing what the edit changed. Add that direction to a different model with the same architecture, and you transplant the behavior without redoing the surgery. That's weight arithmetic: no probes, no gradient steps, no training — just 102 tensors rearranged in float32.

Primary sources:

- [Exact 0xKitkat model card](https://huggingface.co/0xKitkat/Ornith-1.5-35B-A3B-Uncensored)
- [Pinned artifact](https://huggingface.co/0xKitkat/Ornith-1.5-35B-A3B-Uncensored/tree/9ce64447864049ac16f7546265ae11d2a04fe9fb)
- [Official Ornith-1.5-35B-A3B card](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B) and [pinned configuration](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B/raw/main/config.json)
- [Ornith-1.5 release blog](https://ornith.ai/ornith_1_5.html)
- [wangzhang donor card — Abliterix method and 7/100 LLM-judged refusals](https://huggingface.co/wangzhang/Qwen3.6-35B-A3B-abliterated)
- [alztrk orthogonalization edit + dynamic GGUF suite](https://huggingface.co/alztrk/Ornith-1.5-35B-A3B-Abliterated)
- [pottokao text-only ablation + NVFP4 sibling](https://huggingface.co/pottokao/Ornith-1.5-35B-A3B-abliterated)
- [Refusal in Language Models Is Mediated by a Single Direction](https://arxiv.org/abs/2406.11717)

The 0/16 figure is a publisher measurement on 16 prompts with disclosed regex screening, not a guarantee. The base's benchmark table is a publisher claim on the unedited checkpoint; capability retention after the edit is asserted by construction, not yet measured.
