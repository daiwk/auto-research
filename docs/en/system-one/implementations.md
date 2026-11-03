# Open Jev implementations: selection and integration roadmap

<!-- source-sha256: 84d0145a05d7e4aca5c306b907ec0336b2ea7c98ad21f735fb80d5d83a15eb3b -->

[简体中文](../../system-one/implementations.md)

This is not a ranking of which project is closest to official Jev. It identifies what each open implementation solves. Community projects reproduce **System One interface or decision behavior**. TypeSafe has not published Jev weights, training data, RLCD algorithm, or internal network in this snapshot. None should be called officially equivalent.

See the [complete 48-entry snapshot](implementation-tracker.md). This page focuses on plausible choices and shared evaluation targets.

## Official boundary {#official-jev}

| Implementation | Verifiable | Not public | Repository status |
|---|---|---|---|
| [TypeSafe Jev](https://docs.typesafe.ai/introduction) | Choice, Score, Noul, probabilities, confidence, and hosted API | Weights, data, architecture, RLCD loss, and training recipe | Typed contract and optional HTTPS provider integrated; local baselines are not Jev reproductions |

## Five technical routes

| Route | Mechanism | What to test | What it does not mean |
|---|---|---|---|
| Direct logits / parallel constrained decoding | Reuse an LM and read candidate token or branch logits after one prefill | Latency, interface, candidate scaling, serving | A newly trained Jev-like model |
| Trained decision head or fine-tuned model | Train Choice, Score, Noul, or typed-schema heads on a public base | Calibration, generalization, objectives, checkpoints | Reproduction of unreleased RLCD |
| Diffusion language models | Use DiffusionGemma or similar parallel generation/discrimination for one-step decisions | Parallel and nonautoregressive decisions | Jev's calibration |
| Prior classification or extraction | Dynamic labels, schema extraction, or specialist discrimination | Lineage and strong nongenerative baselines | A community Jev reproduction |
| Evaluation and behavioral studies | Measure accuracy, Brier, ECE, latency, OOD, and interface behavior | Shared evaluation and detection of false reproduction claims | A deployable model |

## P0: Public checkpoints for shared evaluation

| Project | Public assets | Defining mechanism | Main limits | Recommendation |
|---|---|---|---|---|
| [Bespoke Nimble](https://github.com/bespokelabsai/nimble) | 9B checkpoint, training data and recipe; MLX/CUDA | Reads flat typed-schema enum/Boolean logits without generating JSON | Authors do not guarantee calibration; Score and nested schemas incomplete | **P0 checkpoint comparison** for actual model, latency, and Choice/Noul |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | Qwen3-0.6B weights, data, training and serving code | Set-attention decision head; Choice, Boolean, Score; proper loss | Small community model/data do not represent product quality | **Real checkpoint integrated:** typed provider, pinned revision, A100 Banking77 OOD smoke |
| [Laya](https://github.com/NandhaKishorM/laya) | Checkpoint, demo, fine-tuning notebook | Typed decisions and temperature calibration | Zero-shot near random, fine-tuned domain dependence, token budget at large candidate counts | **P0 calibration control:** ECE/Brier and validation-only temperature fit |

Integration requires a pinned public revision, the same split, actual execution, and metrics. At this roadmap snapshot, NanoJev had completed the first real-checkpoint interoperability smoke. Bespoke Nimble and Laya were cataloged but not yet integrated, and not shown as local experiment results.

## P1: Engineering and serving baselines

| Project | Route | Reuse | Role |
|---|---|---|---|
| [SemIf](https://github.com/TheoLeeCJ/SemIf), formerly OpenJev | Direct option logits | Shared-state prefill, fixed revision/fixture, latency control | First parallel constrained-decoding baseline |
| [Reflex](https://github.com/kshetrajna12/reflex) | Logits / typed decisions | Jev-style interface and local execution | API and contract interoperability |
| [openjev-sglang](https://github.com/ekzhang/openjev-sglang) | SGLang serving | High-throughput parallel constrained decoding | GPU serving baseline |
| [LitJev](https://github.com/zhengxuyu/litjev) / [snapjudge](https://github.com/Micha0827/snapjudge) | Lightweight decoding wrappers | Minimal runnable implementations and interfaces | Teaching or smoke, not an ability ceiling |
| [jeff](https://github.com/logan-markewich/jeff) | Trained schema head | GLiFormer/GLiNER structured extraction | Adjacent dynamic-candidate baseline |

These can evaluate complexity, throughput, and contract compatibility. CUDA paths need real A100/A30 execution and a sanitized receipt before integration is complete.

## P1: Evaluation resources

| Project | Purpose | Plan |
|---|---|---|
| [jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks) | Jev-style tasks and comparisons | Verify licenses and gold isolation, then map to common protocol |
| [jev-ood-calibration](https://github.com/scienthoon/jev-ood-calibration) | OOD and calibration | Extend coverage–risk, ECE/Brier, and OOD candidates |
| [jev-behavior-study](https://github.com/RINNECODER/jev-behavior-study) | Hosted API behavior | Black-box evidence only; do not infer official internals |
| [typesafe-ai-benchmark](https://github.com/iammrduncan/typesafe-ai-benchmark) | TypeSafe API comparisons | Fixed public examples only with a user-provided key |

## Pick by goal

| Goal | First choice | Alternatives | Why |
|---|---|---|---|
| Public-checkpoint comparison | Bespoke Nimble | NanoJev, Laya | Actual weights, data, or training recipes |
| Choice / Score / Noul | NanoJev | Laya | Multiple primitives and objectives |
| Low-latency engineering | SemIf | openjev-sglang | No autoregressive JSON; measurable prefill/candidate scaling |
| Calibration and OOD | Laya + jev-ood-calibration | NanoJev | Temperature calibration, proper metrics, and coverage–risk |
| Apple Silicon trials | Bespoke Nimble MLX | PocketJev, jevmlx | Training assets versus mainly runtime wrappers |
| Diffusion research | DiffusionGemma / vLLM | LocalJev, open-jev | Separate experiment, not a shared trained-head ranking |

## Integration gate

1. Pin public model, data, and code revisions and record licenses.
2. Distinguish trained models, inference decoders, and concept diagnostics.
3. Implement at least one Choice, Score, or Noul typed contract.
4. Select on validation and reserve test for final reporting. Record accuracy, NLL, Brier, ECE, cost, and latency.
5. Keep gold answers and plans out of model inputs. Label interface fixtures diagnostic.
6. Run CUDA paths on real A100/A30 hardware and commit sanitized evidence.

Tracker entries are not local implementations. Cataloged, in adaptation, and evaluated remain distinct dashboard states.
