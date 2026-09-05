<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# The 180B abliteration race on the model nobody can serve yet

Published 27 August 2026. Exact artifact: `dealignai/Qwen3.8-Flash-Next-ABLITERATED-FP8`, revision `8d5a44586872fe3a22cfd14398894bc0fd054e29`.

On 24 August, Qwen published Qwen3.8-Flash-Next as "the experimental preview of the architecture that will underpin Qwen4". Counting every parameter group, it is a 180-billion-parameter model — 125B in the language stack, 51B in a new n-gram lookup table, 4B in a multi-token-prediction head — yet only about 6B are active per token. Within 48 hours at least five independent editors were racing to remove its refusal behavior, and here is the part nobody leads with: the serving ecosystem still cannot run this architecture on released software.

The pinned FP8 build by dealignai is the one with measured, served numbers. On HarmBench-320 at greedy decoding and temperature 0, it reports 100% real-harm compliance with reasoning set to low, 99.6% at xhigh, 97.1% with reasoning off — meaning its own editor rates it essentially complete refusal removal as long as reasoning is on. MMLU drops from 86.36% to 83.86% (−2.50 points), MTP speculative decoding keeps ~81% draft acceptance, and image plus video inputs both work. That is the fastest-moving uncensored artifact of the week.

## The base is a Qwen4 preview, not a Qwen3.8

The upstream card is explicit that this is the architecture Qwen4 will be built on. Qwen's own summary highlights four components, all of them relevant to anyone editing the weights:

- **Qwen Sparse Attention (QSA)** — sparse attention that selects at the micro-block level instead of per-token, which Qwen says cuts long-context latency, a gain aimed at agentic workloads.
- **Gated DeltaNet** — the linear-attention (state-space-style) path, paired with QSA instead of full attention.
- **Gated Residual** — residual streams widened to four branches, each with an element-wise data-dependent read gate and a per-branch scalar write gate, bottleneck rank 320.
- **N-gram Embedding** — a 51.2B-parameter lookup table indexed by bigrams and trigrams at layer 2, which Qwen frames as a way to scale parameters "with less computation and more amenable to offloading than MoE".

The numbers on the official card are 48 layers, 512 routed experts per MoE layer with top-10 plus one shared expert, a 2,560-dimensional hidden layout, 262,144-token native context (extensible to 1M), a 27-layer vision encoder, and a Muon/AdamW split training recipe with no batch-size warmup. Three days after release the base already carried 3,753 likes on Hugging Face. All of that is Qwen's own published description — label it upstream publisher claims.

## Five editors, one new architecture

The race field, oldest to newest:

- **orcarouter/Qwen3.8-Flash-Next-Uncensored** (26 Aug) — the most-liked of the set early on, but gated behind auto-approval, so we could not read its card. Skipped as a gated repo.
- **msuiche/Qwen3.8-Flash-Next-abliterated-GLP-47** (27 Aug) — a GGUF control-vector build, also gated. The runtime refusal-direction dial angle is already covered on this site, so we did not chase it.
- **Jiunsong/SuperQwen3.8-Flash-Next-abliterated** (27 Aug, BF16) — the methodologically deepest edit. Its card describes an "architecture-aware Qwen4-Exp refusal-subspace edit": an 842-pair harmful/harmless corpus, a refusal direction measured in the four-stream hyper-connection read mix (width 2,560), then a rank-1 projection at strength 2.0 applied to layers 33–47. The whole edit changes just 36 storage tensors, which expand to 6,168 logical output projections once fused routed experts are counted. Vision, the n-gram table, routers, gates, normalization and MTP are deliberately untouched, and the card publishes SHA-256 hashes for every verification artifact. It is pinned to upstream `f5d08274…`, and its BF16 file set is 337 GiB — too large to serve as an original-weight checkpoint across the two 128 GiB DGX Spark nodes the editor had, so no served BF16 claim is made.
- **dealignai/Qwen3.8-Flash-Next-ABLITERATED-FP8** (27 Aug) — the one featured here, official FP8, served and measured (numbers above).
- **windowsxp811203/Qwen3.8-Flash-Next-Abliterated-NVFP4** (26 Aug) — a W4A16 build that cuts 336 GiB to 173.6 GiB by quantizing only the MoE experts to 4-bit NVFP4, keeping the n-gram table and the vision tower in BF16. Its own card admits the checkpoint was never served end to end.

## The catch: released runtimes don't support qwen4_exp

This is the honest part. windowsxp811203's card is blunt: "no released inference server supports `qwen4_exp` yet", citing vLLM PR #53896 and SGLang PR #36497 still open, with people running those branches. Jiunsong's card confirms the pattern — upstream Transformers support lands in a specific commit that was not yet in a released version at the time of writing, and a full 337 GiB BF16 instantiation was never run. dealignai's served numbers come from a vLLM recipe that uses `trust_remote_code=True` and a PLE CPU-offload environment flag (`VLLM_PLE_CPU_OFFLOAD=1`).

In other words the bottleneck right now is not the editors — five people uncensored a brand-new 180B architecture in two days — it is the toolchain. If you want to run any of these today, you are on a patched branch or a custom recipe, not a stable release. That will change within weeks, and the abliterated artifacts are already sitting at the top of the stack for the moment it does.

## The n-gram table is the weird part of the size math

Qwen3.8-Flash-Next is 180B total largely because of a 51.2B-parameter lookup table that behaves almost nothing like a neural-network weight matrix. It is why the NVFP4 build is still 173.6 GiB instead of roughly 70: the editor chose to keep the table in BF16 (95.4 GiB) rather than quantize it, reasoning that quantizing to FP8 makes correctness depend on a runtime taking a special FP8 code path for the embedding, which nobody has yet demonstrated. That is the kind of decision that only appears when you are abliterating and quantizing an architecture before anyone has written a stable loader for it.

## How to run it

The served path is vLLM. dealignai's recipe:

```python
from vllm import LLM, SamplingParams
llm = LLM(model="dealignai/Qwen3.8-Flash-Next-ABLITERATED-FP8",
          tensor_parallel_size=2, trust_remote_code=True)
# reasoning via chat_template_kwargs: {"enable_thinking": True, "reasoning_effort": "xhigh"}  # low | medium | xhigh
```

Set `VLLM_PLE_CPU_OFFLOAD=1` for the n-gram table, and `speculative_config={"method": "qwen3_8_flash_next_mtp", "num_speculative_tokens": 1}` for MTP. Expect to be on a patched vLLM branch until qwen4_exp support ships. The BF16 artifact is 337 GiB and needs far more than two 128 GiB DGX Sparks; the NVFP4 W4A16 twin is 173.6 GiB and unquantized-path-friendly but has not been served. Our approximate managed price estimate for the 180B MoE class is **$10.90/hour** (2 × H200), which is where ABLITERATED.cloud would host it when the toolchain stabilizes.

## The creator: dealignai

dealignai runs the CRACK brand — permanent, weight-level uncensoring with "no cheap template tricks, no fine tuning", as their profile tagline puts it. On Hugging Face they have 99 models, 1,482 followers and a status set to "Open to Work"; they are not a Pro account and appear to work independently, crediting compute on the GLM card to X user @jordanschenck. Their catalogue spans Gemma-4, DeepSeek-V4-Flash, MiniMax, Bonsai, Ornith, Nemotron and the Qwen3.5/3.6/3.8 lines, with the biggest hit being Gemma-4-31B-JANG_4M-CRACK at 1,707 likes. They publish on X as @dealignai. The sibling editor Jiunsong (Jun Song, 1,072 followers, Ko-fi at ko-fi.com/jiunsong) did the architecture-aware BF16 edit covered above — worth a follow if you care about edit-method detail. The base architecture comes from the Qwen team.

One honest line: safety filtering is significantly reduced here — that is the whole point of the edit — and the numbers above are the publisher's own measurements on disclosed prompt sets, not independent testing.

## The idea, in plain words

**A 51-billion-parameter lookup table that scales the model without scaling the compute** — Qwen's n-gram embedding is not trained to "understand" anything; it is a giant dictionary keyed by short token pairs and triples at layer 2, so the model can look up a much richer representation of the input than a normal embedding provides. Because a lookup table does not multiply matrices on every token, it can be enormous and still cheap to run, and it can be offloaded to CPU while the rest of the model stays on the GPU. That is how a 180B-parameter model gets to 6B active per token.

Primary sources:

- [Exact dealignai model card](https://huggingface.co/dealignai/Qwen3.8-Flash-Next-ABLITERATED-FP8) and [pinned revision](https://huggingface.co/dealignai/Qwen3.8-Flash-Next-ABLITERATED-FP8/tree/8d5a44586872fe3a22cfd14398894bc0fd054e29)
- [Official Qwen3.8-Flash-Next card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) (base facts and benchmarks)
- [Jiunsong architecture-aware BF16 edit card](https://huggingface.co/Jiunsong/SuperQwen3.8-Flash-Next-abliterated)
- [windowsxp811203 NVFP4 build card](https://huggingface.co/windowsxp811203/Qwen3.8-Flash-Next-Abliterated-NVFP4) (runtime-support and size analysis)
- [vLLM qwen4-exp PR #53896](https://github.com/vllm-project/vllm/pull/53896) and [SGLang qwen4-exp PR #36497](https://github.com/sgl-project/sglang/pull/36497)
- [Qwen3.8-Flash-Next technical report](https://github.com/QwenLM/Qwen3.8-Flash-Next/blob/main/tech_report.pdf)
