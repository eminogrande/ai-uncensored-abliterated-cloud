<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# The MIT vision sleeper that resurfaced in August

Published 9 December 2025, updated 17 August 2026. Exact artifact: `huihui-ai/Huihui-GLM-4.6V-Flash-abliterated`, revision `7d7926ee0a8d02e46bdab97ead8d5396bfc071df`.

On 9 December 2025, huihui-ai published an abliterated copy of Zhipu's GLM-4.6V-Flash, one of the few serious open vision models released under MIT. The exact artifact is a text-side weight edit of a 10,292,777,472-parameter BF16 image-text-to-text model (`Glm4vForConditionalGeneration`, about 20.6 GB in five shards), created roughly at release speed: the upstream repo appeared 7 December, Z.ai's blog followed 8 December, and huihui-ai's repository went up 9 December — before the upstream repo's final touch that same day. The model card is explicit that "only the text part was processed, not the image part."

Abliteration is the refusal-direction weight surgery from Arditi et al., implemented here via Sumandora's remove-refusals-with-transformers (linked on the card). Because only the text pathway was edited, "uncensored vision model" means "an uncensored language model that can see": whether image-conditioned refusals survive is unmeasured — neither huihui nor anyone else has published a refusal-rate or capability-retention evaluation, and upstream vision benchmarks (SoTA-in-class claims on MMBench, MathVista, OCRBench; 128K training context; native function calling) belong to Zhipu's checkpoint. Zhipu's self-admitted limits (weak pure-text QA, overthinking, unreliable counting and person identification) carry over.

The sleeper framing is literal. The exact artifact has 99 downloads and 18 likes, while its December 2025 GGUF shadow (seanbailey518) drew 2,051 downloads and an Ollama port (AliBilge) has logged over 9,000 pulls. The first quant wave stalled at the runtime: in the model's only discussion thread, huihui-ai replied that Ollama "crashes when trying to recognize images." On 17 August 2026, mradermacher published two fresh GGUF repos — a standard ladder and an i1-imatrix ladder — and the standard one ships `.mmproj` vision-projector files, the first supply-side sign that llama.cpp-family runtimes can now actually see with this model. Both had zero downloads at the time of writing. This is a runtime-maturity signal, not a demand spike.

Our prepared profile pins revision `7d7926ee0a8d02e46bdab97ead8d5396bfc071df`, serves one L40S at an approximate managed price estimate of $2.34/hour, and treats the edit as text-only. The publisher warns that safety filtering is significantly reduced and recommends research and controlled environments. "Abliterated" means refusal-reduced, not zero-refusal, capability-preserved or safe.

## The idea, in plain words

**Why an MIT license matters more than the benchmark table** — MIT is the 'do whatever you want' license: commercial use, modification, redistribution, no strings attached. Most capable vision models are not MIT. For a company, license terms decide whether a model is usable at all — which is why a smaller MIT model can beat a bigger restricted one in practice.

Primary sources:

- [Exact model card](https://huggingface.co/huihui-ai/Huihui-GLM-4.6V-Flash-abliterated)
- [Pinned artifact](https://huggingface.co/huihui-ai/Huihui-GLM-4.6V-Flash-abliterated/tree/7d7926ee0a8d02e46bdab97ead8d5396bfc071df)
- [Hugging Face model API record](https://huggingface.co/api/models/huihui-ai/Huihui-GLM-4.6V-Flash-abliterated)
- [Official upstream Zhipu card](https://huggingface.co/zai-org/GLM-4.6V-Flash) and [release blog](https://z.ai/blog/glm-4.6v)
- [Ollama discussion thread (incl. publisher reply)](https://huggingface.co/huihui-ai/Huihui-GLM-4.6V-Flash-abliterated/discussions/1)
- [mradermacher GGUF (with mmproj)](https://huggingface.co/mradermacher/Huihui-GLM-4.6V-Flash-abliterated-GGUF) and [i1-imatrix variant](https://huggingface.co/mradermacher/Huihui-GLM-4.6V-Flash-abliterated-i1-GGUF)
- [AliBilge GGUF port](https://huggingface.co/AliBilge/Huihui-GLM-4.6V-Flash-abliterated) and [Ollama page](https://ollama.com/alibilge/Huihui-GLM-4.6V-Flash-abliterated:q4_k_m)
- [seanbailey518 GGUF](https://huggingface.co/seanbailey518/Huihui-GLM-4.6V-Flash-abliterated-GGUF)
- [Refusal-direction paper](https://arxiv.org/abs/2406.11717)
- [Implementation linked by huihui-ai](https://github.com/Sumandora/remove-refusals-with-transformers)
- [r/LocalLLaMA release thread (community)](https://www.reddit.com/r/LocalLLaMA/comments/1phaaon/glm46v_108b_has_been_released/)

Note: Reddit API access was rate-limited (HTTP 403) during research, so the r/LocalLLaMA thread is cited for its existence from web-search results, not read directly. Community corroboration of the text-only abliteration also appears in a [July 2026 uncensored-model roundup](https://note.com/keity717/n/na12c237cd70d) and an [April 2026 local-models list](https://www.latent.space/p/ainews-top-local-models-list-april).
