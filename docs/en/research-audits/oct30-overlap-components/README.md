# October 30 overlap backfill: zero source increment, ten new low-cost components

<!-- source-sha256: a0390b3411062fc7d03b36c0e30b33b7ecef7f51505800e67dcf6c4453b5d360 -->

[简体中文](../../../research-audits/oct30-overlap-components/README.md)

These are not ten papers first published in one day. The latest visible arXiv announcement was **2026-10-28**; eight new lists matched prior identities and shared recent dates yielded none. Bounded Google/Meta/DeepMind catalogs were unchanged. This batch reviews and implements recent overlap and historical Google leads, not every full text in the window.

## Scope

| Priority | Paper | Low-cost delivery | Full experiment not run |
| --- | --- | --- | --- |
| P0 · Google collaboration | [CONCUR](../../../post-training/2610.36437-concur/README-en.md) | CPU reward gates, order-preserving ceiling projection, earned-trust accumulation, and batch whitening | 32 GPUs per run, multi-model/task RL; too costly, review DONE |
| P0 · DeepMind collaboration | [MERLIN](../../../foundation-models/2610.37645-merlin/README-en.md) | CUDA raw segment moments, query-direction mean/variance, double-softmax gating, and causal visible segments | Large-scale pre/mid-training and long-context matrix; review DONE |
| P0 · Google historical backfill | [CROP](../../../agent-research/2604.14214-crop/README-en.md) | CPU external text-gradient callback and cost-regularized prompt selection with validation isolation | Gemini/7B multiround optimization and API evaluation matrix; review DONE |
| P0 · Industrial A/B | [PinGER](../../../recommendation-components/2610.33435-pinger/README-en.md) | CUDA asymmetric masks, one-layer prefix penalty, all-prefix DPO plus NTP anchor | Private tokenizer/recommender, billion-item catalog, serving and A/B; review DONE |
| P0 · Industrial A/B | [Pinterest RLBP](../../../recommendation-components/2610.33248-pinterest-rlbp/README-en.md) | CUDA nine actions, two-head TD, reward/fusion/top-K, and IPS | Private campaigns, auction/PID deployment, and paid traffic; review DONE |
| P1 | [FoldBias](../../../foundation-models/2610.36520-fold-bias/README-en.md) | CUDA constrained ridge direction and value refit after actual BF16 rounding | Large-model KV, long-context, and serving comparisons; review DONE |
| P1 | [SWIM](../../../foundation-models/2610.36662-swim/README-en.md) | CUDA gated inverse dynamics, cyclic contrastive loss, frozen `sqrt(g)` geometry | Full visual JEPA world model and CEM planning; review DONE |
| P1 | [MPOPD](../../../post-training/2610.36477-mpopd/README-en.md) | CUDA geometric proposal target, one-token-lagged single-step weight, and two reverse KL terms | Real LM rollouts, parameter resets, and long-chain distillation; review DONE |
| P1 | [EMMA](../../../agent-research/2610.35966-emma/README-en.md) | CPU memory ownership, single-edit/inheritance/capacity guards, and overflow concatenation | Semantic safety services, LLM reflection, AppWorld and other tasks; review DONE |
| P1 | [EvalAlloc](../../../agent-research/2610.37276-evalalloc/README-en.md) | CPU Beta acquisition, MAP with fixed external response model, paired-round corrections, and cache budget | MIRT warmup/two-fold refit and full LLM search controller; review DONE |

CROP was first published in April; the other nine first appeared October 23–27. MPOPD uses pinned v2 for reading and records v1 separately, not as a second paper. First-author affiliations stay CMU for CONCUR and Princeton for MERLIN despite Google collaborations.

## Execution and evidence

Frozen commit `af9b9245aa85b4cbeb3da27ca701cc01cb94da86`. Portable Git proof binds 15 execution, specification, and scope files. Only about 88 KB of public source was synchronized, not a workspace, data, credentials, or checkpoints.

- CPU: ten components × three seeds, about **3.43 seconds**.
- Real **NVIDIA A100-SXM4-80GB**: six CUDA components × three seeds, about **1.69 seconds**.
- Runner component times exclude startup, transfer, research, and tests. No model download, LLM/API calls, or full training.
- [Execution spec](../../../research-audits/oct30-overlap-components/execution-spec.json) · [Raw CPU](../../../research-audits/oct30-overlap-components/raw-cpu.json) · [Raw CUDA](../../../research-audits/oct30-overlap-components/raw-cuda.json) · [Frozen source](../../../research-audits/oct30-overlap-components/frozen-sources.json) · [Per-paper scope](../../../research-audits/oct30-overlap-components/task-scope.json)
- Per-paper `metrics/component-{cpu,cuda}-seeds42-44.json` and six independent GPU receipts: [MERLIN](../../../gpu-validations/merlin-a100-20261030.json), [FoldBias](../../../gpu-validations/fold-bias-a100-20261030.json), [SWIM](../../../gpu-validations/swim-a100-20261030.json), [MPOPD](../../../gpu-validations/mpopd-a100-20261030.json), [PinGER](../../../gpu-validations/pinger-a100-20261030.json), and [RLBP](../../../gpu-validations/pinterest-rlbp-a100-20261030.json). Validators bind each, not a batch table presented as capability evidence.

These verify formulas, gradients, numerics, and state contracts, not business value, agent success, LLM accuracy, or evolve gains. Full cost closures are terminal and recorded separately, with no auto-retry or implementation queue.

## Sources and limits

[Coverage](../../../research-audits/oct30-overlap-components/source-coverage.json) retains 16 complete fetch/parse receipts, category identities, and shared recent-date diffs. Cross-listings and replacements do not count as new papers; unread wide-recall identities are not full-text reviewed.

[Official directory review](../../../research-audits/oct30-overlap-components/official-directory-check.json) compares committed October 29 full baselines: 44/44 pages succeeded, with identical parsed Google 435, Meta 144, and DeepMind 266 URLs. Only new receipts and baseline references are stored. [Priority review](../../../research-audits/oct30-overlap-components/priority-review.json) separately records official sites, blogs, new public repos, and bounded activity. Push time does not prove code release, and Meta six pages are not exhaustive.

No October 29 or 30 announcement was claimed. Code activity and historical finds are not first publications. **The global watermark stays 2026-10-15**; these ten deliveries do not close all October 16–30 sources.

## Learning material and quality checks

Ten papers received four levels of Chinese QA each, **40 questions** in all, with concrete examples and actual section references. Nine existing deep dives updated mechanisms, analysis, and cross-paper questions while retaining IDs and history and binding README fingerprints.

[Recent learning cards](../../learning/recent.md) · [All questions](../../learning/all.md) · [Deep dives](../../learning/deep-dives/index.md)

Cross-review fixed derived NaN/Inf from huge finite inputs, CONCUR mutable history, MERLIN group-wise gradients, the SWIM fixed-action-chunk formula, and externalized RLBP undisclosed numeric preprocessing. 122 independent mechanism and 40 source/evidence contract tests passed. Full regression exposed a missing CROP figure copyright notice; affected docs, cards, and source contracts were rechecked. Strict docs and base wheel installation passed, not full paper capability.
