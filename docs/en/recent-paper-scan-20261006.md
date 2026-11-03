# October overlap follow-up and DepGPO implementation: 2026-10-06

<!-- source-sha256: 74670f4eaabba562f05669894f226d45f1cabb366c05d4ba3bb11cb1e151b52c -->

[简体中文](../recent-paper-scan-20261006.md)

Continue [incomplete October 5 scan](recent-paper-scan-20261005-followup.md) with **2026-10-01** overlap and last complete watermark **2026-10-02**. Official arXiv API/full text and Google/Meta sources, no DeepXiv.

| Track | Coverage | Remaining boundary |
|---|---|---|
| Industrial arXiv | Paging succeeded; two unreviewed titles in window, both out of scope | Three Google Research and two Meta pages timed out |
| Agent arXiv | Paging succeeded; 48 unreviewed window hits | Title recall includes robotics, applications, safety and evaluations; not 48 implementations or full reviews |
| Foundation/post-training | Prior completed paging plus targeted official full text | No renewed full affiliation reconciliation |
| Google DeepMind/Google/Meta | DeepMind readable; directory timeouts for Google Research/Meta with some browser fallback | Targeted checks only; no overall advance |

Unreviewed counts include historical and late-index work. Use actual v1 submission dates, not time of a successful 429 retry. Local scan receipts carry machine details; page records review conclusions.

[DepGPO](../agent-research/2610.03634-depgpo/README-en.md), v1 October 2, implements structured read/write traces, verifier-related writes, supporting reads and step/token advantage normalization. Hand traces and property tests pass; L1 only, no terminal tracer, Qwen policy training or Terminal-Bench lift. [Meta AIMS](https://arxiv.org/html/2610.02600) remains ineligible industrially: offline logs only, no verified production A/B/full traffic.

1. [FrugalEvo](https://arxiv.org/html/2610.03675), [author code](https://github.com/chchenhui/frugalevo): budgets, strong-model planning/weak coding, BA-AUC and shared-prefix cache suit Evolve. Need fixed public task/call costs, not formula-only.
2. [Sentry](https://arxiv.org/abs/2610.02994): conditional failure recovery, store only successful recoveries. Need real failure detection, isolated tasks and no reward leakage.
3. [Dynamic Expert Pruning](https://arxiv.org/abs/2610.02951): prompt-conditioned MoE pruning needs checkpoint, predictor training and quality/memory/latency comparison; CUDA requires A100/A30.
4. [RC-OPD](https://arxiv.org/html/2610.03515), [Recursive Harness Self-Improvement](https://arxiv.org/html/2610.03548), [Pivot-SD](https://arxiv.org/html/2610.03665), [KV²](https://arxiv.org/html/2610.03198): retain full mechanism and data/GPU gates.

These leads are not implemented. Continue October 1 overlap and official-source checks; new-paper increments start from the last reviewed date, not PR date.
