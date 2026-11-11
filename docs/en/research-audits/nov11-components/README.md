# November 11, 2026: Priority Papers, Low-Cost Components, and Bilingual Learning Material

<!-- source-sha256: 0158c3f1b705194fe5790a115ba63091d2de07d33f8790178d5dc1c0f138fefd -->

[简体中文](../../../research-audits/nov11-components/README.md)

This fixed delivery contains **17 papers: 16 low-cost L1 components and one cost-and-mechanism review-only reference**. All 16 components have three-seed CPU diagnostics; four CUDA paths also ran with three seeds on a real single A100. All full paper-scale experiments are **not reproduced because of high cost; review DONE**. Mechanism checks are not advertised as model capability or Evolve gains.

**The review watermark remains November 9, 2026.** This bounded selection and delivery does not close the entire November 10–11 review window. One query in the actual four-track/two-mode capture is capped, and Meta's publication directory has an actual access limitation; see [source coverage](../../../research-audits/nov11-components/source-coverage.json).

## Fixed Cohort

Dates below are the original v1 timestamps in UTC; AlphaProof Code has an official publication day only. Relative to the November 9 watermark in Asia/Shanghai, 13 first releases are later and four are historical or overlap backfills. Discovery dates, announcement dates, and identifier months do not substitute for first publication.

| Paper / reference | Original publication, UTC | Local delivery | Full experiments |
| --- | --- | --- | --- |
| [ReproBridge](../../../agent-research/2611.08452-reprobridge/README-en.md), Google collaboration | 2026-11-05 18:45:36; backfill | CPU: private-reference isolation, Student-t prediction interval, four-part artifact and audit-evidence contracts | Not reproduced |
| [LiSA](../../../agent-research/2605.14454-lisa/README-en.md), Google collaboration | 2026-05-14 06:47:35; backfill | CPU: Beta lower bound, average-linkage clustering, local conflicts, memory reuse | Not reproduced |
| [MaxIM](../../../post-training/2611.12825-maxim/README-en.md), Google Research | 2026-11-09 18:25:42 | CPU: normalized PMI / incremental-summary reward kernel | Not reproduced |
| [Excursion TD](../../../post-training/2611.13275-excursion-td/README-en.md), Google DeepMind collaboration | 2026-11-09 21:41:23 | CPU: exact finite-MDP operators, excursion weights, and targets for given trajectories | Not reproduced |
| [DRD-MOPD](../../../post-training/2611.13249-drd-mopd/README-en.md) | 2026-11-09 21:21:41 | CPU + A100: gradient routing over full-parameter deltas and independent per-delta AdamW; no teacher distillation loss | Not reproduced |
| [MCPO](../../../post-training/2611.14015-mcpo/README-en.md) | 2026-11-10 12:51:43 | CPU: margin uncertainty, advantage-sign weighting, per-response normalization | Not reproduced |
| [Stochastic Rounding](../../../foundation-models/2611.13545-stochastic-rounding/README-en.md) | 2026-11-10 04:07:19 | CPU + A100: actual stochastic-rounding numerics and device path | Not reproduced |
| [WikiTrace](../../../agent-research/2611.14320-wikitrace/README-en.md) | 2026-11-10 16:46:59 | CPU: source-linked memory, explicit drill-down, read-only evidence | Not reproduced |
| [FGSE](../../../agent-research/2611.14326-fgse/README-en.md) | 2026-11-10 16:52:25 | CPU: joint admission gates for transfer gain, falsification risk, and old-task damage | Not reproduced |
| [PASE](../../../agent-research/2611.14019-pase/README-en.md) | 2026-11-10 12:53:12 | CPU: skill-program pairs and transactional patches accepted or rolled back by held-out validation | Not reproduced |
| [RETRACE](../../../agent-research/2611.14492-retrace/README-en.md) | 2026-11-10 18:49:47 | CPU: guards, typed dependency IR, parameter provenance, and ordered-rule dispatch; no planner | Not reproduced |
| [ARE-Bench](../../../agent-research/2611.14364-are-bench/README-en.md) | 2026-11-10 17:21:31 | CPU: task-context isolation, strict checklist conjunction, and task-macro scoring interfaces | Not reproduced |
| [RS-JEPA](../../../multimodal-models/2611.14496-rs-jepa/README-en.md) | 2026-11-10 18:51:05 | CPU + A100: scanpaths, GRL, and four neighbor KL terms; no complete predictor | Not reproduced |
| [ADIndex](../../../foundation-models/2611.12956-adindex/README-en.md) | 2026-11-07 06:35:09; backfill | CPU + A100: group-index distillation, frozen backbone, causal sparse selection | Not reproduced |
| [B3](../../../foundation-models/2611.14387-b3/README-en.md) | 2026-11-10 17:40:24 | CPU: lagged self-calibrated spawn gate and block-causal mask | Not reproduced |
| [StepRefine](../../../multimodal-models/2611.12901-steprefine/README-en.md) | 2026-10-14 07:52:29; backfill | CPU: entropy spikes, soft embeddings, KL stopping, budget accounting | Not reproduced |
| [AlphaProof Code](../../../agent-research/alphaproof-code/README-en.md), Google DeepMind / Google | 2026-11-10, day precision | Official report, proof repository, and cost review only; no local verifier, adapter, or metrics | Not reproduced |

Individual paper pages, the [fixed scope](../../../research-audits/nov11-components/task-scope.json), and three review artifacts retain methods, source locations, affiliations, author-code status, local execution boundaries, and cost evidence: [priority institutions](../../../research-audits/nov11-components/priority-review.json), [post-training](../../../research-audits/nov11-components/post-training-review.json), and [Agent / JEPA](../../../research-audits/nov11-components/agent-review.json). No whole-paper reading claim is made: the reviewed method, evaluation-configuration, and cost sections are explicitly bounded.

## Google / Meta and the Industrial Evidence Gate

Google-priority delivery includes ReproBridge, LiSA, MaxIM, Excursion TD, and the review-only AlphaProof Code reference. Institutions are checked against original bylines. B3's first author is at Technion / Amazon Web Services; model names or author impressions do not establish Google affiliation.

The Meta / NUS paper [2611.13539, Exploiting Feature-invariant Scaling Laws for Efficient A/B Experimentation in Recommendation Systems](https://arxiv.org/html/2611.13539v1), was checked in Sections 5 and 8–10 but is **not accepted or implemented in this batch**. Its A/B comparisons are offline architecture/feature experiments. Criteo training on 4.2 billion examples with last-day validation, MovieLens20M, and LLM fine-tuning do not establish randomized production traffic and quantified online uplift. A/B in the title, absence in the abstract, or online-data motivation cannot replace full-text production evidence. The paper is not relocated into foundation models or evaluation infrastructure to bypass this gate; no classic-paper exception is invented.

This rejection is separately recorded in the ledger and excluded from the 17 deliverables. The published cost is factual context, not acceptance disguised as high-cost deferral. e-means and GSLM2 are known entries, not new papers. A remote-sensing application and OSS/governance studies newly visible in the official directory have separate bounded dispositions.

## Execution Evidence and Limits

- [Preflight](../../../research-audits/nov11-components/preflight.json): 16 fixed components, seeds 42/43/44, at most 180 seconds per run; no API calls, pretrained-model calls, model/data downloads, or full experiments.
- [Frozen source](../../../research-audits/nov11-components/frozen-sources.json): actual execution commit and source SHA-256 values, not a later commit label substituted for execution provenance.
- [Raw CPU results](../../../research-audits/nov11-components/raw-cpu.json): 16 components × three seeds. [Raw CUDA results](../../../research-audits/nov11-components/raw-cuda.json): four components × three seeds.
- Actual A100 receipts: [DRD-MOPD](../../../gpu-validations/drd-mopd-a100-20261111.json), [Stochastic Rounding](../../../gpu-validations/stochastic-rounding-a100-20261111.json), [RS-JEPA](../../../gpu-validations/rs-jepa-a100-20261111.json), and [ADIndex](../../../gpu-validations/adindex-a100-20261111.json). Public inputs are source-defined small tensors, finite MDPs, and explicit contract fixtures, not real checkpoints.

All results retain `diagnostic_only: true` and `evaluation_tier: l1_mechanism`. They do not reproduce paper accuracy, throughput, or production uplift. Three seed labels on the same deterministic contract do not create three independent capability samples. Evaluator references, success thresholds, and answers remain isolated from actors. Registering a local operator is not unified Evolve integration: `promotion_eligible` and `evolve_integrated` remain false.

Each paper gains four-level learning questions and reviewed English versions, with corresponding topic deep-dive updates. These explain methods and local limits without promoting evidence tiers. Original figures, sources, and extraction methods are preserved in paper pages and the figure manifest.

## Coverage and Remaining Leads

The batch reuses actual November 11 four-track/two-mode CI captures: requested October 28–November 11, with effective overlap from October 27. **A capture file does not mean every candidate has received method review.** The foundation late-index `LLM` query is capped at 2,000; the other seven captures exhaust their configured queries. The supplemental post-training Atom search returned the first 100 of 111 keyword results only.

Official-source review is bounded to Google first/last pages and relevant details, DeepMind's publication landing page and AlphaProof project/announcement, and the attempted Meta directory. Meta's directory returned unavailable content; an unchanged curated home page does not establish no new papers sitewide. Google's count increase from 450 to 462 is not twelve new papers. Actual URLs, content hashes, failures, and limitations are in [source-coverage.json](../../../research-audits/nov11-components/source-coverage.json).

Limited leads without completed method review remain: Bootstrapped OPD (2611.13680), Coverage Collapse / Reference Resets (2611.14467), and Action-Sequence Alignment OPD (2611.13135). They are not automatic implementation tasks or high-cost DONE decisions. Repairing the capped query and reviewing the entire window are separate future work required before another watermark advance; this batch makes no incidental completion promise.

## Rechecking the Record

```bash
PYTHONPATH=src python scripts/record_nov11_components.py --check
PYTHONPATH=src python scripts/audit_paper_coverage.py --strict
```

The recording script appends only after matching raw execution, frozen source, leaf metrics, and A100 receipts. It refuses to overwrite an accepted batch; `--check` is read-only. Expensive full experiments are not retried or queued for automatic training, implementation, or Evolve. Reopening requires an explicit user request after reviewing the cost.
