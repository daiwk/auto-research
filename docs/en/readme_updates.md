# Delivery and research audit record

<!-- source-sha256: 87088dae740f5c22857346d249da6fc4c915a26cb198f653533db459dc683ef9 -->

[简体中文](../readme_updates.md)

[Project README](project-readme.md) · [Documentation home](index.md)

This record preserves historical batches, experiment limits, and review cutoffs. For specific conclusions, use the individual write-ups and execution receipts. Ongoing updates are in the [commit history](https://github.com/daiwk/auto-research/commits/main/).

## 2026-10-27: Four learning levels and project navigation

Paper questions cover basics, core mechanisms, method comparisons, and implementation details. Readers can filter by level and use a stable link to each question. Publication is blocked when a new paper lacks any of the four levels. Questions added to older papers also appear in the topic bank and recent list. The root README now focuses on capabilities and navigation, with a sub-minute site tour. Installation, experiments, development, and audit history have separate guides. See the [learning home](learning/index.md) and [media receipt](../assets/media/site-tour.json).

## Audited paper implementations

[Google/Meta historical lead closeout, October 21](research-audits/google-meta-closeout-20261021/README.md): Individually reviewed 39 leads from official Google sources, closed nine full-experiment cost or source decisions, and implemented bounded SpecGuard and Video Encoders components. Review acceptance, catalog entry, L1 component, and full capability reproduction are distinct counts. The former 521 undelivered entries are not an automatic implementation commitment. High-cost full experiments are not reproduced. Accepted but unimplemented opportunities stay separate and do not count as done merely because the full text was read or a catalog entry exists.

[Harness² and Google/Meta historical backfill](research-audits/harness2-priority-repair/README.md): Added the low-cost two-level recursive controller, executing 96 CPU Python probes. Full model/API benchmarks are too costly and not reproduced. Fixed date screening and deduplication that treated accepted but undelivered records as closed. Historical discoveries and first publications are recorded separately. Mechanism tests are not capability evidence and do not automatically enter Evolve.

[October 17 follow-up: nine components, two evaluators, and three high-cost references](research-audits/oct17-supplement/README.md): Added Prism-1, LangDiT, OPRD reminder, OpCredit, SSR, RSIFlow, LEASH, PROBE, Terminal-RSI, and GACC-Bench / Muon paired-budget interfaces. Four CUDA paths passed three-seed A100 mechanism runs; seven passed CPU diagnostics. Gemini Minecraft, Hy-Memory, and Athanor are references only; the full experiments are not reproduced. Components do not establish full capability or Evolve integration. The new `oprd-reminder` does not replace `oprd`.

[October 17: twelve affordable components and Meta/AMD systems references](research-audits/oct17-components/README.md): Covers KV eviction, MoE routing, lossless compression, ternary quantization, distillation, reward, replay, and agent audit, routing, and retrieval. Nine CUDA components passed three-seed A100 mechanism diagnostics; three agent components were checked on CPU. Costly full experiments are marked not reproduced (review DONE). Component results do not establish the paper's full capability or enter Evolve automatically.

[Two Google P0 items, twelve P1 items, and the TransX report upgrade](research-audits/oct16-components/README.md): Provides constrained decoding, cross-task auxiliary heads, exact multi-cutoff memory, post-training objectives, and public agent evaluator interfaces. Costly full experiments are not reproduced (review DONE). Small-network updates, operator diagnostics, and official-result recomputations are reported separately. Passing a component does not demonstrate benchmark gains. The old fixed-weight TransX example is now correctly labeled a concept demo.

[October 16: eight P1 components and interfaces](design/oct16-eight-p1.md): OOB full-data anchor regularization, transparent context compression, FormCraft typed composition, divergence-routed DrOPD, RAP-Walk preference credit, CTXGAP, Selective Reasoning, and the CLASHarness evaluation interface. Distinguishes executed low-cost algorithms, public statistical replay, and interfaces. Author results are not local model capability; costly full experiments are not reproduced (review DONE). CUDA results and failure corrections are in the delivery checklist. None automatically promotes to Evolve capability.

[October 15: five components and interfaces](design/oct15-affordable-components.md): CASI frozen-snapshot credit assignment, PN-Mix KV quantization, SMRC/PMRC optimizers, Meta AutoformBench task/result interfaces, and JEPA prediction–planning evaluation. Only affordable executable parts are delivered. Full production training, large-model sweeps, and multi-environment retraining are not reproduced (review DONE). Interface and component success does not establish official benchmarks or stable gains. See the checklist for actual runs and CUDA receipts.

[October 14: cost-bounded delivery](research-audits/2026-10-14-delivery.md): Scaled WeGR training, the MemCon controller, recomputation of public JEV predictions and request audit, and the official EmbeddingGemma 2 checkpoint path. Five other costly papers had Chinese write-ups and disabled plans only, without registered training commands, invented metrics, or automatic Evolve integration. The batch did not advance an exhaustive-source review. Current cutoff and coverage are in the [discovery audit](paper-discovery-audit.md).

[October 13 implementation checkpoint](design/oct13-implementation-scope.md): Retains the fixed review scope of 19 papers. Eighteen have scaled mechanism entry points validated on real GPUs. At the user's decision, MBS was marked costly and not reproduced for this batch; research notes and failed evidence are retained without an executable registration. Mechanism validation is not original benchmark reproduction or capability improvement. See [all implementation statuses](reproductions/README.md). Future high-cost papers are marked without running expensive trials.

[October 4: seven historical omissions](recent-paper-scan-20261004-followup.md): Jev lookahead, T2SPO, Weakest-Link, CMP, TESS, RLCPR, and Mingbird all have bounded L1 mechanism APIs. T2SPO also ran the real official TabPFN checkpoint on CPU for three seeds. None is a full LLM or agent benchmark reproduction.

[October 11: implementation and closeout](research-audits/oct11-implementation-scope.md): Records actual status for 12 papers, OPD diagnostics, and four closeout items. Real GPU commands, pinned model/data versions, negative results, and unfinished original benchmarks remain in the paper pages and [runtime audit](research-audits/oct11-runtime-audit.md). Passing a mechanism run is not model improvement or automatic Evolve integration.

The repository registers **410** paper adapters. The shared source is [`docs/research-manifest.json`](../research-manifest.json). The [paper implementation index](reproductions/README.md) supports browsing by domain, institution, topic, and year. Write-ups retain source links, first-author affiliation, first publication, upstream code status, local adapter and path, architecture and equations, paper online/offline results, and local public-data conclusions.

Industrial search, ads, and recommendation require quantified online A/B or user-approved full-traffic evidence. Named classic baselines are recorded exceptions. Foundation models use public benchmarks and matched training budgets. Historical metrics were migrated to schema v2 without changing seed counts. Fewer than 3 seeds is a smoke result, not a stable gain.

CI checks registry, manifest, paper metadata, evidence location, experiment protocol, and historical metric schema when adapters change. The old hand-maintained 186-line README list is no longer the source of record.
