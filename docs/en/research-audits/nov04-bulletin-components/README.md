# November 4 bulletin: fourteen papers and low-cost mechanism components

<!-- source-sha256: 4b510655a9749f721835ca67b9f09b29c4bef920b7fec30ded8795e46bd1d4c6 -->

[简体中文](../../../research-audits/nov04-bulletin-components/README.md)

This batch uses the actually retrieved **November 4, 2026 arXiv bulletin**. It delivers twelve low-cost components and two reference-only high-cost papers. New collection does not mean publication today: twelve papers came from new sections, RuntimeTickets from a cross-list, and RSI-Dojo is a late-announced backfill first published October 29. None of the fourteen first became public after the previous capture.

## Fixed delivery scope

| Area | Paper | Local delivery | Complete experiment not reproduced |
| --- | --- | --- | --- |
| Industrial recommendation | [ReuseGR](../../../recommendation-components/2611.04259-reusegr/README-en.md) | CPU whole-row leave-one-out depth labels, ancestor reuse criterion, routing and composite scoring | Learned BudgetCut, PathKD and private advertising retrieval |
| Industrial recommendation | [SPADE](../../../recommendation-components/2611.04662-spade-local-search/README-en.md) | CPU OA-BPE nonoverlapping merges and one SDBS expansion | STAR training, MARS-DPO and production search |
| Industrial recommendation | [OneTrans GSR](../../../recommendation-components/2611.04720-onetrans-gsr/README-en.md) | CPU reference constraints, rewards and separate advantage normalization | Learned RM, GMRPO and production slate serving; local FP64 is not the paper's bitwise FP32 implementation |
| Foundation models | [Semantic-Block Sparse Attention](../../../foundation-models/2611.04313-semantic-block-sparse-attention/README-en.md) | CUDA semantic-block routing, GQA aggregation and causal visibility | Real long-context models and end-to-end throughput matrix |
| Foundation models | [Anchor KV](../../../foundation-models/2611.04327-anchor-kv/README-en.md) | CUDA externally written state, layer-specific read maps and gates | Full LaCT momentum/Muon inner-loop training and large-model evaluation |
| Post-training | [Density-Aware Reward Scaling](../../../post-training/2611.04792-dars/README-en.md) | CUDA Gaussian KDE including self-density, reward scaling and group normalization | Complete RL training; stable key `dars-density` does not replace existing Dependency-Aware DARS |
| Post-training | [P²-MOPD](../../../post-training/2611.03953-p2-mopd/README-en.md) | CUDA parameter-prior optimizer and two-channel gradient reference | Multiple teacher LLMs and full on-policy distillation |
| Post-training | [Shuffled OPSD](../../../post-training/2611.04958-shuffled-opsd/README-en.md) | CUDA input transforms, fixed reference selection and signed per-vocabulary weights | Full teacher/student training and task comparisons |
| Post-training | [Targeted Guidance](../../../post-training/2611.05266-targeted-guidance/README-en.md) | CUDA failed-turn reverse KL and stopped-gradient teacher targets | Agent rollouts, hint generation and complete GRPO optimization |
| Agent/RSI | [Meta²](../../../agent-research/2611.05139-meta-square/README-en.md) | CPU frozen meta-skill, task-local edit lifecycle and public-checkpoint isolation contracts | Real meta-agents/LLMs and full environment search |
| Agent/RSI | [Continual Autoresearch](../../../agent-research/2611.05108-continual-autoresearch/README-en.md) | CPU post-close initialization, best-so-far curve and final-selection scoring, plus paired protocols | Actual continual training, model calls and large experiments |
| Agent security | [RuntimeTickets](../../../agent-research/2611.03772-runtime-tickets/README-en.md) | CPU authorization tightening, send gate and local HMAC audit chain | Real network-egress deployment across frameworks; a local chain is not global trusted monitoring |
| Foundation models | [Multi-Layer Indexer](../../../foundation-models/2611.03768-multi-layer-indexer/README-en.md) | Reference and method review only | The original eight-H200 serving matrix |
| Agent/RSI | [RSI-Dojo](../../../agent-research/2611.03698-rsi-dojo/README-en.md) | Reference and method review only | Model-training environments taking roughly five to ten hours per task and complete trajectory training |

All fourteen complete experiments are **not reproduced due to cost (review complete)**, without automatic retry. The twelve runnable components are L1 mechanism diagnostics, not complete capability reproduction, production-lift reproduction, end-to-end serving acceleration or executable Evolve integration. The two reference-only papers have no fabricated operators or metrics.

## Actual execution and identity isolation

[Preflight](../../../research-audits/nov04-bulletin-components/preflight.json), [frozen-source proof](../../../research-audits/nov04-bulletin-components/frozen-sources.json), [raw CPU](../../../research-audits/nov04-bulletin-components/raw-cpu.json), [raw CUDA](../../../research-audits/nov04-bulletin-components/raw-cuda.json), [per-paper scope](../../../research-audits/nov04-bulletin-components/task-scope.json).

CPU executes twelve components across three seeds, and A100 executes six CUDA components across the same seeds 42/43/44. Only small tensors, arithmetic and state contracts are used: zero pretrained-model calls and no data/checkpoint downloads. Internal runner times are 2.900 and 1.689 seconds, excluding research, startup and transfer; these are not full-training times. Each paper has separate metrics, and six CUDA components each have a sanitized [GPU receipt](../../gpu-validation.md).

The old Dependency-Aware Reward Shaping identity `post-training:dars` and its learning history remain unchanged. The new paper uses `post-training:dars-density`. The execution-time short label `dars` remains in the immutable raw results and maps explicitly to the new identity; no numbers, seeds or frozen sources were altered.

Cross-review added nonnegative-reward constraints, stable zero loss under extreme finite logits, and a fix for OneTrans constraint iterators being exhausted across candidates. All fixes preceded source freezing and actual CPU/A100 execution. Normalized metrics use `math.fsum` to avoid last-bit aggregation differences across Python versions.

## Sources, priority institutions and coverage boundaries

[Source receipts](../../../research-audits/nov04-bulletin-components/source-coverage.json) and [bulletin identities](../../../research-audits/nov04-bulletin-components/bulletin-records.json) cover cs.AI, cs.CL, cs.CV, cs.IR, cs.LG, cs.RO, cs.SD and eess.AS. Direct `/new` and `?show=2000` routes agree on date, counts and identities: 1,472 category entries including cross-lists/replacements and 1,094 distinct identities. This is recall volume, **not 1,094 completed full-text reviews**.

[Google/Meta priority review](../../../research-audits/nov04-bulletin-components/priority-review.json): thirty Google directory pages and six Meta pages timed out in this capture; their deltas are unknown, not zero. Nine DeepMind pages were retrieved, without a claim that every detail identity was reviewed. Official GitHub queries for recently created repositories and search are bounded supplements. None of the selected fourteen has a verified Google/Meta author affiliation. **Meta² is a method name, not a Meta company paper.**

The fourteen-paper fixed scope is delivered; unread bulletin identities and unavailable sources are not relabelled review-DONE. The global review watermark remains **October 15, 2026**. This batch does not claim whole-window exhaustion or advance that watermark.

## Learning cards and bilingual updates

Each paper adds basics, mechanism, comparison and implementation questions: 56 total. Corresponding topic membership, representative-method comparisons, analyses, cross-paper self-tests and dated records bound to current README fingerprints are updated. Original figures and attribution are retained. New prose, questions and deep-dive units have individually reviewed English counterparts.

[Recent Q&As](../../learning/recent.md), [all questions](../../learning/all.md), [deep dives](../../learning/deep-dives/index.md).
