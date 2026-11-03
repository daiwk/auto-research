# Complete snapshot of community Jev implementations

<!-- source-sha256: 397d4d3e9c5727b41b60fb1b7e4fd01c507df6d55c69e54967b14cd2852e3184 -->

[简体中文](../../system-one/implementation-tracker.md)

This page records the public [Jev Reproductions Tracker](https://huggingface.co/spaces/multimodalart/jev-reproductions-tracker) entries on **2026-09-19** for deduplication and selection. The tracker is community-maintained and not affiliated with TypeSafe. “Jev,” “RLCD,” or “System One” in a name does not imply access to official weights, data, or training algorithms.

## Snapshot counts

| Category | Count | Meaning |
|---|---:|---|
| Direct logits or parallel constrained decoding | 17 | Existing models and inference techniques, usually no new training |
| Diffusion language models | 4 | One-step decisions with nonautoregressive models such as DiffusionGemma |
| Trained models and decision heads | 16 | Offer or claim trained checkpoints, heads, LoRA, or fine-tunes; one unreleased |
| Prior work | 2 | Earlier dynamic classification, extraction, or specialized discriminators |
| Evaluation, behavior studies, and indexes | 9 | Benchmarks, black-box studies, explanations, and curated lists |
| **Total** | **48** | Integration requires this repository's execution gates |

## Direct logits and parallel constrained decoding (17) {#decode-routes}

| Project | Primary form | Notes |
|---|---|---|
| [Qwen-2.5-1B-RLCD](https://huggingface.co/harshatheg/Qwen-2.5-1B-RLCD) | Qwen checkpoint and [parallel constrained decoding demo](https://huggingface.co/spaces/drinkmoonshine/parallel-constrained-decoding) | Distinguish checkpoint claims from verifiable training evidence |
| [openjev-sglang](https://github.com/ekzhang/openjev-sglang) | SGLang parallel constrained decoding | GPU serving approach |
| [SemIf](https://github.com/TheoLeeCJ/SemIf) | Direct option logits | Formerly OpenJev; canonical repository renamed |
| [PocketJev](https://github.com/NullPo-jp/PocketJev) | Lightweight local wrapper | Interface and inference focus |
| [jevmlx](https://github.com/bnsd55/jevmlx) | Local MLX inference | Apple Silicon approach |
| [jev-on-a-laptop](https://github.com/rorshopping/jev-on-a-laptop) | Local laptop execution | Engineering demo |
| [jevfire](https://github.com/kikoncuo/jevfire) | Jev-style inference wrapper | Evaluation boundaries need independent review |
| [LFM2.5-RLCD 350M](https://huggingface.co/notnotsamuel/LFM2.5-350M-RLCD) / [2.6B](https://huggingface.co/monotykamary/LFM2.5-2.6B-RLCD) | LFM checkpoint | Verify training assets and typed contract |
| [parallelConstraintDecoding](https://github.com/stephanj/parallelConstraintDecoding) | Parallel constrained decoding | General inference technique |
| [system-one](https://github.com/snellingio/system-one) | Typed decision wrapper | Community interface implementation |
| [open-jev](https://github.com/daseinlabs/open-jev) | Logits and wrapper | Independent community implementation |
| [openvons](https://github.com/genai-craft/openvons) | Open System One interface | Independent community implementation |
| [openjev](https://github.com/zhihz/openjev) | Jev-style inference | Independent community implementation |
| [system-one](https://github.com/sgoedecke/system-one) | Minimal System One demo | Engineering and teaching baseline |
| [Reflex](https://github.com/kshetrajna12/reflex) | Typed decision API | Candidate interoperability baseline |
| [LitJev](https://github.com/zhengxuyu/litjev) | Lightweight Jev-style implementation | Smoke-test candidate, not a capability ceiling |
| [snapjudge](https://github.com/Micha0827/snapjudge) | One-step discrimination and interface wrapper | Suitable for interface comparison |

## Trained models and decision heads (16) {#trained-routes}

| Project | Public assets or method | Status |
|---|---|---|
| [Bespoke Nimble](https://github.com/bespokelabsai/nimble) / [9B checkpoint](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B) | Qwen3.5-9B LoRA, data, and recipe; flat-schema enum/Boolean logits | **P0 candidate**; authors do not guarantee calibration |
| [jevlike](https://github.com/vinnylarouge/jevlike) | Option attention and candidate probabilities | Community-trained implementation |
| [openjev](https://huggingface.co/AlexWortega/openjev) / [source](https://github.com/mikesmullin/openjev) | Public model and code | Training and evaluation protocol need review |
| [decider-2b](https://github.com/Mapika/decider) / [checkpoint](https://huggingface.co/Mapika/decider-2b) | Decision model and a vision variant | Typed primitives need review |
| [jeff](https://github.com/logan-markewich/jeff) | GLiFormer/GLiNER | Adjacent schema-head baseline |
| [Verdict](https://github.com/Heman10x-NGU/Verdict-open-jev) / [rlcd-modernbert-151m](https://huggingface.co/heman10x/rlcd-modernbert-151m) | ModernBERT decision model | RLCD and data claims need review |
| [open-jev](https://huggingface.co/spaces/pngwn/open-jev) / [scorer](https://huggingface.co/pngwn/system-one-qwen3.5-4b-scorer-v2b) | Qwen3.5 scorer | Checkpoint revision and protocol need review |
| [jevbetter](https://github.com/olanotolu/jevbetter) | Community-trained implementation | Public assets need review |
| [system-one-open](https://github.com/mithalouni/system-one-open) | Open System One model | Training evidence needs review |
| [qwen-rlcd](https://github.com/shamazharikh/qwen-rlcd) | Qwen decision fine-tuning | RLCD definition and data need review |
| [system-one-gemma](https://github.com/akash-kamat/system-one-gemma) | Gemma decision fine-tuning | Training and calibration need review |
| [Laya](https://github.com/NandhaKishorM/laya) / [checkpoint](https://huggingface.co/convaiinnovations/laya) | Typed decisions, temperature calibration, demo and notebook | **P0 candidate**; domain dependence and high candidate-count limits |
| [System One Mini](https://huggingface.co/DavidHatley/system-one-mini) | Small public checkpoint | Data and evaluation need review |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) / [checkpoint](https://huggingface.co/C-Tianyu/NanoJev) | Qwen3-0.6B and decision heads; Choice/Boolean/Score | **P0 candidate**; public training and serving |
| [mini-jev](https://github.com/r-ms/mini-jev) | Small trained reproduction | Training assets need review |
| Archer Hume open-weight Jev-like model | Preview or description only | **Not released**; not a runnable implementation |

## Diffusion language models (4) {#diffusion-routes}

| Project | Primary form | Limits |
|---|---|---|
| [vLLM DiffusionGemma PR #57250](https://github.com/vllm-project/vllm/pull/57250) | DiffusionGemma serving support | Infrastructure, not a Jev checkpoint |
| [razorback16/openjev](https://github.com/razorback16/openjev) | DiffusionGemma-as-Jev | Independent behavior reproduction |
| [JoshuaSP/open-jev](https://github.com/JoshuaSP/open-jev) | Diffusion-model decisions | Independent behavior reproduction |
| [LocalJev](https://github.com/githubnext/localjev) | Local experiment from GitHub Next | Calibration and throughput need separate verification |

## Prior work (2) {#prior-work}

| Project | Relation to System One | Limits |
|---|---|---|
| [GLiNER 2.5 models](https://huggingface.co/collections/fastino/gliner25-models) | Dynamic entity/schema representations and discrimination | Prior method, not a Jev reproduction |
| [DeepMost sales conversion model](https://huggingface.co/DeepMostInnovations/sales-conversion-model-reinf-learning) | Specialized probabilistic decision model | Domain classifier; interpret under the paper's task |

## Evaluation, behavior studies, and indexes (9) {#evaluation-resources}

| Project | Type | Use |
|---|---|---|
| Archer Hume Jev architecture speculation | Explanatory article | Community speculation, not official architecture evidence |
| [jev-ood-calibration](https://github.com/scienthoon/jev-ood-calibration) | OOD and calibration | **P1 evaluation candidate** |
| Matija Sosic Jev explainer | Video explanation | Background |
| [typesafe-ai-benchmark](https://github.com/iammrduncan/typesafe-ai-benchmark) | API benchmark | **P1 online black-box protocol candidate** |
| [awesome-jev](https://github.com/AnotiaWang/awesome-jev) / [awesome-jev](https://github.com/hellogumbo/awesome-jev) | Index | Discovery and deduplication, not implementation |
| [jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks) | Benchmark | **P1 public evaluation candidate** |
| hhkkmon community thread | Discussion | Not technical evidence |
| mygtmhire long-form warning | Opinion article | Risk note, not an implementation |
| [jev-behavior-study](https://github.com/RINNECODER/jev-behavior-study) | Black-box behavior study | **P1 protocol evidence candidate** |

## Maintenance rules

- Add a project here with its technical route before deciding whether it belongs in the [integration roadmap](implementations.md).
- A Jev or RLCD name does not establish fidelity. Verify weights, data, objective, evaluation splits, and licensing.
- Self-reported README figures are leads only. The local dashboard shows executed results that meet the data-isolation contract.
- Retain snapshot dates for removed or renamed projects; link changes do not count as local verification.
