<!-- ARCHIVE-NOTICE -->
> Editorial archive — not a live model listing. This article preserves reporting at its publication date, including model-specific licenses, publisher claims and historical hosting estimates. Those estimates are not current prices or offers. Benchmarks from different artifacts, runtimes and tests are not a current ranking. Reported refusal results do not guarantee zero refusals. The current project is private on-demand evaluation on Vast.ai with llama.cpp; no public inference. [Current project status](https://abliterated.cloud/).
<!-- /ARCHIVE-NOTICE -->

# The workhorse: Huihui-Qwen3.6-27B-abliterated, four months in

Published 23 April 2026. Exact artifact: `huihui-ai/Huihui-Qwen3.6-27B-abliterated`, revision `27502c8717fd5a2f8c0c77188c10c243fd4f672e`.

Qwen released the dense, multimodal Qwen3.6-27B on 21 April 2026; huihui-ai published this abliterated derivative two days later. Four months on it is the most-used abliterated Qwen we track: 18,760 downloads and 72 likes on the exact repository per the Hugging Face model API, an Ollama tag, a ModelScope mirror, and an MTP-GGUF sibling that has out-downloaded the parent (66,484 downloads).

The checkpoint is dense: 27,781,427,952 BF16 parameters, 64 layers, 5,120-wide hidden dimension, laid out as sixteen repetitions of three Gated DeltaNet blocks followed by one Gated Attention block. It is natively multimodal (vision encoder, image and video tokens, thinking and non-thinking modes), carries a 262,144-token native context, and occupies about 55.6 GB in BF16. The edit is refusal-direction abliteration via Sumandora's pure-Transformers implementation — a weight edit, not a jailbreak — and the card itself calls it "a crude, proof-of-concept implementation".

What users report is mixed and specific: Concedo's thread "Still seems censored" ("It's a bit better than the base, but not perfect"), a single-stack report of vision not detecting images, and, on the other side, a community five-method comparison (85 GPU-hours, r/LocalLLaMA) crediting huihui's variant with the smallest benchmark deltas and near-complete safety removal. A researcher asked how to cite the model in a paper; another user runs it for red-teaming. Upstream Qwen claims 77.2 SWE-bench Verified, 59.3 Terminal-Bench 2.0, 87.8 GPQA Diamond and 94.1 AIME 2026 — those belong to the unedited checkpoint; huihui publishes no post-edit rerun.

The newer Huihui-Qwen3.8-27B-abliterated (August 2026) uses a different recipe — first 15 layers retained, MTP and vision untouched — and a stronger base on paper. The 3.6 abliteration remains the one with four months of real-world mileage: settled quantization paths, a working Ollama tag, and a body of user reports. Newer is not the same as proven.

We pin the exact revision, budget one H200 at roughly $5.45/hour (approximate managed price estimate), and do not transfer upstream benchmarks to our endpoint until the exact artifact is measured. "Abliterated" means refusal-reduced, not zero-refusal, correct or harmless.

## The idea, in plain words

**How a language model sees images** — An LLM only reads tokens, so multimodal models bolt on a vision encoder that cuts an image into patches and turns them into tokens the language model can read. 'Image-text-to-text' means the model takes pictures and words in, and answers with words — the vision half is a separate organ that the abliteration usually leaves alone.

Primary sources:

- [Exact model card](https://huggingface.co/huihui-ai/Huihui-Qwen3.6-27B-abliterated) and [pinned files](https://huggingface.co/huihui-ai/Huihui-Qwen3.6-27B-abliterated/tree/27502c8717fd5a2f8c0c77188c10c243fd4f672e)
- [Hugging Face model API](https://huggingface.co/api/models/huihui-ai/Huihui-Qwen3.6-27B-abliterated)
- [Official upstream Qwen card](https://huggingface.co/Qwen/Qwen3.6-27B) and [Qwen release article](https://qwen.ai/blog?id=qwen3.6-27b)
- [Discussion: Still seems censored](https://huggingface.co/huihui-ai/Huihui-Qwen3.6-27B-abliterated/discussions/4) · [no vision support](https://huggingface.co/huihui-ai/Huihui-Qwen3.6-27B-abliterated/discussions/3) · [citation](https://huggingface.co/huihui-ai/Huihui-Qwen3.6-27B-abliterated/discussions/2) · [FP8 request](https://huggingface.co/huihui-ai/Huihui-Qwen3.6-27B-abliterated/discussions/1)
- [Community comparison: 85 GPU-hours, 5 abliteration methods](https://www.reddit.com/r/LocalLLaMA/comments/1tfmocw/85_gpuhours_comparing_5_abliteration_methods_on/) (r/LocalLLaMA; fetched via search index — direct access blocked)
- [Ollama model page](https://ollama.com/huihui_ai/Qwen3.6-abliterated:27b) and [MTP-GGUF sibling](https://huggingface.co/huihui-ai/Huihui-Qwen3.6-27B-abliterated-MTP-GGUF)
- [Newer Huihui-Qwen3.8-27B-abliterated card](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated) and [upstream Qwen3.8-27B card](https://huggingface.co/Qwen/Qwen3.8-27B)
- [Original refusal-direction paper](https://arxiv.org/abs/2406.11717) and [implementation linked by huihui-ai](https://github.com/Sumandora/remove-refusals-with-transformers)

The publisher warns that safety filtering is reduced and recommends controlled research use. "Abliterated" means refusal-reduced, not zero-refusal, correct, legal or harmless.
