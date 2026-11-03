# October 16: Two P0s, twelve P1s, and the TransX upgrade

<!-- source-sha256: a000a4214dcc28a073d803e578a1f04f22f9688a7208fe7749f43eca577ddf53 -->

[简体中文](../../../research-audits/oct16-components/README.md)

One MR covers the accepted bounded components and public evaluation interfaces, not empty shells for full experiments. High-cost complete experiments are **too expensive, not reproduced (review DONE)** and do not enter automatic retries or count as implementation completion.

## Scope and costs

| Priority | Paper / key | Implemented and verified | Full-experiment cost and decision |
|---|---|---|---|
| P0 historical backfill | [STATIC](https://arxiv.org/abs/2602.22647) / `static-constraint-decoding` | CSR trie, vectorized constraints, beam state, and bounded GPU comparison | TPU v6e, 1B model, private YouTube online study; not reproduced, DONE |
| P0 historical review | [Cross-Task Relationships](https://arxiv.org/abs/2609.28776) / `cross-task-relationships` | Paired auxiliary heads, valid multi-feedback labels, actual small-net gradients, matched ablation | Billions of private daily samples, multi-week training, full YouTube policy; not reproduced, DONE |
| Existing method upgrade | [TransX report](https://arxiv.org/abs/2610.20913) / `transx` | Exact local/global memory at multiple cutoffs, differentiable prefix reuse, sparse row optimizer | 32 H200s, about 13 hours to production convergence; not reproduced, DONE |
| P1 | [Novelty Patching](https://arxiv.org/abs/2610.22100) / `novelty-patching` | Strict causal lookup, train-only threshold, boundary diagnostics | 1.9 GB and multiple models/rules/seeds; not reproduced, DONE |
| P1 | [RoPERelay](https://arxiv.org/abs/2610.21126) / `rope-relay` | RoPE inversion and repositioning, masks, later query consistency | Multiple selectors, 128K, 32B judge; not reproduced, DONE |
| P1 | [CoTS](https://arxiv.org/abs/2610.20642) / `cots` | Probability-competition scheduling, discrete/soft mixing, phase lock | 9B/12B and multiple long-reasoning benchmarks; not reproduced, DONE |
| P1 | [TF-OPD](https://arxiv.org/abs/2610.22236) / `tf-opd` | Teacher generation statistics, Gram shrinkage, fused linear solve | Two 7B models and about 10 GPU-hours excluding evaluation; not reproduced, DONE |
| P1 | [Waypoint-OPD](https://arxiv.org/abs/2610.21601) / `waypoint-opd` | Three-snapshot early/late shift gate, loss, scorer | 8B and about 64.31 GPU-hours excluding evaluation; not reproduced, DONE |
| P1 | [GGPO](https://arxiv.org/abs/2610.20814) / `ggpo` | Stable gap objective and real small-policy updates | Four GH200s, 8,000 updates, multiple benchmarks; not reproduced, DONE |
| P1 | [STOPD](https://arxiv.org/abs/2610.21337) / `stopd` | Pregeneration cutoff, natural EOS, IPW, expected gradient | Two H100s per run, long rollouts × three seeds; not reproduced, DONE |
| P1 | [CCE-OPD](https://arxiv.org/abs/2610.21195) / `cce-opd` | Dual conditional views, support, entropy gate, and PPO-OPD | 8B teacher, multiple students/arms, mask annotation; not reproduced, DONE |
| P1 | [SIF](https://arxiv.org/abs/2610.21392) / `sif` | Eligibility, two-level votes, group normalization, and two loss masks | Eight A100-40GB GPUs, full-parameter training, multiple benchmarks; not reproduced, DONE |
| P1 public evaluation | [ToolBottleneckBench](https://arxiv.org/abs/2610.21098) / `tool-bottleneck-bench` | Official bounded tasks, tool state, exact grader, budget and failure denominator | 26,576 conditions and USD 768.38 in hosted collection; not reproduced, DONE |
| P1 public results | [Librarian Agents](https://arxiv.org/abs/2610.22273) / `librarian-agents` | Recompute official compact records; filesystem/provenance contracts | 4B builder, 35B executor, 60K-token traces and external services; not reproduced, DONE |
| P1 public evaluation | [SciPIvot](https://arxiv.org/abs/2610.21082) / `scipivot` | Published options-only evaluation in two orders with isolated scoring | Five frontier models × twelve conditions, private project histories; full experiment not reproduced, DONE |

Costs come from published or official configurations, not local measurement. Small networks, controlled tensors, and recomputed results are diagnostics, not paper-level improvements or automatic evolve integration.

## Acceptance

All 15 bounded components/interfaces are implemented. Eleven CUDA paths actually ran on **NVIDIA A100-SXM4-80GB** with seeds `42,43,44`. Four CPU paths fit deterministic tables or audit official records without invented seeds or hosted model APIs. Each paper includes original figures, formulas, code, upstream versions, and metrics.

| Group | Delivered | Evidence and limits |
|---|---|---|
| Recommendation / CUDA | STATIC, Cross-Task, TransX report | [STATIC](../../../gpu-validations/static-constraint-decoding-a100-20261016.json), [Cross-Task](../../../gpu-validations/cross-task-relationships-a100-20261016.json), [TransX](../../../gpu-validations/transx-report-components-a100-20261016.json); bounded decoding, actual small-net ablations, exact differentiable memory and optimizer, not production gains |
| Foundation / CUDA | RoPERelay, CoTS | [RoPERelay](../../../gpu-validations/rope-relay-a100-20261016.json), [CoTS](../../../gpu-validations/cots-a100-20261016.json); position and mixture operators with gradients, not long-context or reasoning capability |
| Post-training / CUDA | TF-OPD, Waypoint-OPD, GGPO, STOPD, CCE-OPD, SIF | [TF](../../../gpu-validations/tf-opd-a100-20261016.json), [Waypoint](../../../gpu-validations/waypoint-opd-a100-20261016.json), [GGPO](../../../gpu-validations/ggpo-a100-20261016.json), [STOPD](../../../gpu-validations/stopd-a100-20261016.json), [CCE](../../../gpu-validations/cce-opd-a100-20261016.json), [SIF](../../../gpu-validations/sif-a100-20261016.json); actual tiny-policy generation/fusion/updates on public text, not a pretrained LM benchmark |
| Foundation / CPU | Novelty Patching | [Train-only table fit](../../../foundation-models/2610.22100-novelty-patching/metrics/component-cpu.json), 262,144 bytes and 494 train documents, patch rate 0.100296, no BLT training |
| Agents / CPU | ToolBottleneckBench, Librarian Agents, SciPIvot | [216 plan audits](../../../agent-research/2610.21098-tool-bottleneck-bench/README-en.md), [443 official answers recomputed](../../../agent-research/2610.22273-librarian-agents/README-en.md), [248 cases and 60 aggregate rows](../../../agent-research/2610.21082-scipivot/README-en.md); interfaces and prior results, not local agent capability |

Cross-Task arms share initialization and minibatches; test is read after 32 fixed steps. Mean validation BCE baseline 0.668841 versus cross-label 0.668480; test 0.664956 versus 0.665026 (lower better), **no stable improvement**. Retain negatives without seed shopping or evolve promotion. TransX shared/direct maximum forward error 8.89e-16 and gradient error 5.33e-15. Preserve old fixed NumPy scores but correct the evidence label to concept demo; a new operator cannot upgrade old fidelity.

The [first CUDA run](../../../research-audits/oct16-components/first-cuda-failure.json) failed because Waypoint had no effective gradient. Fixes changed tiny-teacher causal first-action REINFORCE, fixed the 8×64 budget and 0/4/8 snapshots, not gates or nonzero-gradient assertions. Frozen commit `781a8178f12069c5c3691093b5f3ba79a48b5322` passed actual runs with source-bound receipts.

All 15 **full experiments** remain high-cost no-reproduction (review DONE), no automatic retries. Components are `diagnostic_only: true`, `promotion_eligible: false`, and `evolve_integrated: false`. No claim of full reproduction or capability gains.

## Dates and discovery

STATIC and Cross-Task are historical implementation backfills; TransX adds evidence from a new report on an existing method. P1 papers mix recent first releases and earlier discoveries surfaced by the October 16 announcement. Implementation does not close that entire announcement window or advance its watermark.
