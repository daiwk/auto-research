# Google EMNLP: review of 25 historical leads and affordable components

<!-- source-sha256: a6667238cb322141b2191f71bd8d2bf12107d331499396a3dfcb0eea7ac53a15 -->

[简体中文](../../../research-audits/google-emnlp25-closure/README.md)

This round covers exactly the **25 authorized historical leads**, not treating conference publication, first discovery, or revision date as new first release. Outcomes: **14 independent L1 components, eight expensive full experiments not reproduced, and three declined**. Four other conference-page link exceptions are outside these 25 and were not claimed reviewed.

See [per-paper decisions](../../../research-audits/google-emnlp25-closure/review-decisions.json) and [frozen scope/acceptance](../../../research-audits/google-emnlp25-closure/task-scope.json) for methods, exact v1 UTC, first-author primary affiliation, Google collaboration, pinned code/license, costs, and decisions. The [original metadata snapshot](../../../research-audits/oct25-priority-components/google-emnlp-title-identity-audit.json) remains unchanged.

## 14 affordable components

These run actual operators, gradients, or offline protocols, not 14 full LLMs/agents. Do not replace required SAE, model outputs, teacher scores, verifiers, or environments with heuristics. All are `L1 / diagnostic_only`, not formal capability comparisons or Evolve promotions.

| Paper/component | Implemented scope | Full path not implemented |
| --- | --- | --- |
| [SCAR](../../../post-training/2505.20417-scar-shapley-credit/README-en.md) | Exact small-game Shapley, signed credit, end-of-span reward, alpha interpolation | No real reward-model scoring, syntax segmentation, Owen approximation, or RLHF |
| [Probabilistic autorater](../../../post-training/2510.00263-probabilistic-autorater/README-en.md) | Piecewise Brier/clipped log reward and invalid-parse penalty | No text autorater training; numerical gradients do not backpropagate through text parsing |
| [RM memorization protocol](../../../post-training/2607.24484-rm-memorization-protocol/README-en.md) | Per-run TM/TG/CM on probabilities and user split consistency | Does not generate 25 RMs or infer memorization from synthetic scores |
| [Benchmark self-bias](../../../post-training/2509.26600-benchmark-self-bias/README-en.md) | Segment rankings, leave-self-out bias, explicit direction/ties | No translation or LLM judge; peer consensus is not truth |
| [DMAST](../../../agent-research/2603.04364-dmast/README-en.md) | Attack-mode isolation, shared-role raw group statistics, length penalty, clipped GRPO/IS/KL | No browser, attacker generation, multistage SFT, or actual self-play |
| [SOPBench protocol](../../../agent-research/2503.08669-sopbench-protocol/README-en.md) | Single/And/Or/Chain procedures and three-part acceptance | Post-hoc scoring only, no seven-domain tools or agents rebuilt |
| [FinanceHarness protocol](../../../agent-research/2607.27853-finance-harness-protocol/README-en.md) | PIT search/read date gates, invalid-run rejection, equal-question rubric | No private corpus, ranker, judge, or financial research intelligence |
| [Cue2Narrate DRL](../../../multimodal-models/2609.01725-cue2narrate-drl/README-en.md) | Masked SFT and current-policy positive/negative caption ranking loss | No localizer, movies, negative-caption generation, or VLM training |
| [POLARIS HRI](../../../post-training/2606.04095-polaris-hri/README-en.md) | Policy-only statistics, human-reference warmup, shared clipped surrogate | No copyrighted human stories, LLM rubric judge, or 9B training |
| [TaskPress](../../../foundation-models/2608.03276-taskpress/README-en.md) | Task attention × value quantization scale, per-head top-k, actual KV gather and positions | No task-guide generation/evolution, GQA policy, quantized kernel, or speed claim |
| [Combinatorial watermark](../../../foundation-models/2510.01637-combinatorial-watermark/README-en.md) | Pattern logit bias, cyclic matching, global/local edit scores | No secret partition generation, real LLM outputs, or formal FPR calibration |
| [Interpolated null calibration](../../../foundation-models/2609.17764-interpolated-null-calibration/README-en.md) | Interpolation over aligned three-pass scores, endpoints and order | No attention extractor or retrieval capability comparison; choose weights on validation only |
| [XLGoBench](../../../foundation-models/2605.30788-xlgobench/README-en.md) | Structural generation for five algorithm categories, exact scorer, gold-isolated callback | No official seven-language templates, human translation validation, or LLM results |
| [Mechanistic ETM](../../../foundation-models/2507.23220-mechanistic-etm/README-en.md) | Binomial ELBO with frozen SAE encoder, topic steering with separate decoder | No real SAE/LLM, topic judge, or full eight-dataset matrix |

## Eight expensive full experiments not reproduced

These are **review DONE / not reproduced**, not pending compute. No fabricated metrics, runnable interfaces, GPU receipts, or retries. Full model experiments for the 14 components above were also not run.

| Paper | Cost/reproduction boundary |
| --- | --- |
| [AgentDebugX](../../../agent-research/2607.18754-agentdebugx/README-en.md) | 9B/27B and multiple API diagnostics, long searches and reruns. Some attribution uses reference answers, not gold-free capability. |
| [LifeAgentBench](../../../agent-research/2601.13880-lifeagentbench/README-en.md) | Reported 300–500 GPU-hours across 13 models. A generic scorer cannot replace LifeAgent. |
| [CoReflect](../../../agent-research/2601.12208-coreflect/README-en.md) | 953 scenarios, three rounds, large models and reflective analyzer. A state machine does not reproduce semantic co-evolution. |
| [Sparse-to-Dense Principle](../../../post-training/2605.12483-sparse-to-dense-reward-principle/README-en.md) | Direct GRPO about 50.2 H200-hours, teacher-first roughly 4–6×. Existing KL operators do not reproduce the pipeline. |
| [Cross-script knowledge transfer](../../../post-training/2603.17070-cross-script-knowledge-transfer/README-en.md) | 120B/30B, real LoRA and long multilingual inference; no regex transliteration or manual prompt substitute. |
| [Cross-lingual exploration](../../../foundation-models/2606.24579-cross-lingual-exploration/README-en.md) | Roughly 234K exploration paths and several frontier models/LLM aggregation judges; no string-vote substitute. |
| [NaijaS2ST](../../../multimodal-models/2604.16287-naijas2st/README-en.md) | Roughly 269 hours of speech, multi-direction training, ASR/TTS and human review; no exact-text substitute. |
| [MVEB](../../../multimodal-models/2606.14958-mveb/README-en.md) | 33 checkpoints and 23/184 tasks; reported 31.9/302.7 hours on one H100 for one model. |

## Three declined

- [AgenticTagger](https://arxiv.org/abs/2602.05945v1): private ranking data supports offline results, not quantified production A/B or authorized full-traffic evidence. Google collaboration is priority, not a waiver. Target-item critique leakage cannot count as fair gains.
- [How Coding Agents Fail Their Users](https://arxiv.org/abs/2605.29442v1): observational sessions and human qualitative research, not an executable coding policy. Do not invent a rule classifier as its method.
- [What Limits Us?](https://arxiv.org/abs/2609.15191v1): research meta-analysis with human-reviewed codebook, not an autonomous RSI method.

## Acceptance and integrity

All 14 passed cost screening before small diagnostics; ten have CUDA paths and four CPU protocols/reference implementations. No large checkpoints, raw media, private data, or big indexes were downloaded; no costly full probe ran.

See [CPU raw results](../../../research-audits/google-emnlp25-closure/raw-cpu.json), [A100 raw results](../../../research-audits/google-emnlp25-closure/raw-cuda.json), and [portable Git evidence](../../../research-audits/google-emnlp25-closure/frozen-sources.json). Paper metrics are `metrics/component-<device>-seeds42-44.json`. Receipts include model/accelerator, commands, seeds, commits, and values without host/user/driver details.

Frozen source `4cce1ab4d701df8daaed9a8abe8671f3eef9d168`: CPU 14 × three seeds about 2.00s and actual A100 ten × three seeds about 1.61s. These are component times excluding imports, connections, transfers, and tests, **not complete model training**. DMAST zero-IS and disabled-KL extremes actually ran on this A100 rather than reusing pre-fix results.

```bash
python scripts/curate_google_emnlp25_evidence.py --check
python -m pytest tests/test_google_emnlp25_closure.py
```

Acceptance checks 25 exact identities, original titles, dates/organizations/catalog aliases, dispositions, 14 check/metric sets and numeric gates, three seeds, actual per-seed device, same CPU/CUDA source, and raw→paper metrics→receipt consistency. Missing, duplicate, wrong identity, CPU-as-GPU, capability inflation, or requeued expensive work fails.

Cross-review fixed POLARIS NaN backward in clipped exponentials, mETM encoder/decoder mixing, and unused exponentials in DMAST zero IS. Fix numerical evaluation or restore formulas, not additional clamps changing objectives. All 22 original figures retain pinned sources, revisions, licenses, and SHAs. Method revisions are separate from v1 dates; group by first-author first affiliation.

**All 25 have explicit dispositions and are no longer unread; full experiments are not claimed implemented. Global review remains 2026-10-15**, not exhaustive across Google or time.
