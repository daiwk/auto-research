# Harness² and Google/Meta historical discovery repairs

<!-- source-sha256: 88f8bc8e675442c2310471db954c273eeb5487392677de65487397e8d33d7edf -->

[简体中文](../../../research-audits/harness2-priority-repair/README.md)

> October 21 correction: 54 and 521 describe the original October 20 reconciliation, not additive implementation TODOs. The 521 included 31 deferred leads and missed 14 acceptances. Split the 54 into 39 pending 2026 reviews, nine earlier references, and six non-implementation dispositions. See [subsequent reconciliation](../historical-backlog-reconciliation-20261021/README.md).

This round adds **one affordable CPU controller**, **12 expensive-paper references**, and links **one existing diagnostic**. It records independent decisions for **22 paper identities** whose method/resource sections were actually checked. All 22 full model/API experiments are **too costly, not reproduced (review DONE)**. Only the bounded Harness² CPU component was implemented; new references are not implementations. No new CUDA path, A100/A30 run, paid API, or model download.

## Harness²: implemented scope

See [paper and one-command run](../../../agent-research/2610.14224-harness2/README-en.md):

- Fix model, environment, starting harness, and improver versions. Execute within-task Propose–Probe–Compose.
- Widen in parallel and deepen sequentially; verify $4k$ executions and $3k$ edit stages.
- Selector sees public tasks and anonymized prior final artifacts, not gold, rubrics, or source harness.
- Persist prior same-domain experience; full harness adoption, referenced execution comparisons, conflict rejection, and failures retained.

Seeds 42/43/44, two modes, and two pipelined tasks per mode produced **96 actual Python subprocesses** and 72 edits in about 1.78 seconds. Deterministic editors/selectors are mechanism substitutes: **L1 evidence**, not LLM capability, official benchmark results, or Evolve integration. See [paper metrics](../../../agent-research/2610.14224-harness2/metrics/component-cpu-seeds42-44.json).

## Discovery defects repaired

| Old behavior | New behavior |
| --- | --- |
| Any ledger entry counted as reviewed | Date/identity screening does not close method review, and generic `new` remains unreviewed |
| Pre-window release closed later discovery | Official Google/Meta evidence can recall older papers separately, not count them as today's v1; explicitly future releases stay outside backfill |
| Priority relied on named queries | Recognize official sources, exact GitHub owners, and organization fields; do not infer Meta from “meta-learning” |
| Generic known/review_done hid accepted but undelivered | Show `implementation-pending` separately in candidate summary |
| First ID observation won | Catalog first, then substantive method/cost/source closure, then pending delivery, then generic labels; keep frozen snapshots |

Explicit high-cost decisions remain final, even with older metadata-only labels. `record_discovery_review.py` rejects date screening and pending delivery as new terminal decisions. Google/Meta full-text source requirements no longer depend only on query names.

## Added or linked references

Historical omissions, not today's releases. Full experiments were not reproduced.

| Paper | Delivered |
| --- | --- |
| [Harmony Harness](../../../agent-research/2610.15150-harmony-harness/README-en.md) | Multi-objective bounded harness evolution and function/safety trade-offs, with costs |
| [SEER](../../../agent-research/2610.04109-seer-forecasting/README-en.md) | Retrieval, reflective memory, matured feedback, frozen test, and costs |
| [MARS](../../../agent-research/2602.02660-mars-research/README-en.md) | Modular research, budgeted search, execution experience, and costs |
| [ECO](../../../foundation-models/2601.22101-eco-optimizer/README-en.md) | Momentum with quantization error and no master weights, with costs |
| [SA-DPO](../../../post-training/2604.27733-sa-dpo/README-en.md) | Semantic-distance adaptive preference margins and costs |
| [FUSE](../../../foundation-models/2604.18547-fuse-verifiers/README-en.md) | Unlabeled verifier ensemble and independence assumptions |
| [Prompt-Level Distillation](../../../post-training/2602.21103-prompt-level-distillation/README-en.md) | Teacher-rule abstraction, clustering, conflict resolution, and costs |
| [RL for Code Optimization](../../../post-training/2607.25970-code-optimization-rl/README-en.md) | Code optimization RL and multi-node costs |
| [AutoformBot](../../../agent-research/2605.29955-autoformbot/README-en.md) | Math formalization agent and resource costs |
| [AIRS-Bench](../../../agent-research/2602.06855-airs-bench/README-en.md) | AI research evaluation protocol, not an integrated evaluation |
| [MetaEncoder](../../../foundation-models/2610.11316-metaencoder/README-en.md) | Dual-tower natural-language decisions and official 30B evaluation costs |
| [Raw Video Mid-Training](../../../multimodal-models/2610.11019-raw-video-midtraining/README-en.md) | Continuous visual next-token training and matched controls |
| [MaD-RL](../../../post-training/2609.31644-mad-rl/README-en.md) | Correct first date, link old character-model/A100 diagnostics and negatives; no measurement rewrite, implementation duplication, or new GPU run |

Existing Meta Logbook, Render2Reason, PAT, CanonQ, Mixture of Layers, Omni-Diffusion-Distill, X-AgentRed, and Compute Optimal Tokenization also gained resource decisions. [Per-paper closure](../../../research-audits/harness2-priority-repair/closure-decisions.json) closes only full experiments without claiming components or a detail page for all.

## Coverage and remaining work

- Google: enumerated 102 saved historical leads and 27 DeepMind 2026 catalog records, checked 198 date-archive identities, and read targeted method/experiment/resource/release sections for seven papers.
- Meta: reconciled 48 saved 2026 official catalog records, reviewing nine historical accepted but undelivered entries with source-specific costs.
- 83 identified papers: seven existing component/implementation pages and 22 review decisions, leaving 54 without substantive closure. This is neither eligibility nor full reading.
- The original ledger had 521 purported accepted-undelivered items. This made them visible without implementing them or mass-labeling high cost. They were not commitments; prioritize institutions, topic, and cost.

See [Google/DeepMind audit](../../../research-audits/harness2-priority-repair/google-audit.json), [Meta audit](../../../research-audits/harness2-priority-repair/meta-audit.json), [reconciliation](../../../research-audits/harness2-priority-repair/backfill-inventory.json), and [22 decisions](../../../research-audits/harness2-priority-repair/closure-decisions.json). Unverified identity/date/full text remains an explicit exception, not acceptance, full-text closure, or implementation. Not exhaustive across history or sources; watermark remains 2026-10-15.

## Verification and rerun

```bash
PYTHONPATH=src python -m pytest tests/agent_research/test_harness2_component.py \
  tests/test_historical_priority_discovery.py tests/test_harness2_priority_delivery.py \
  tests/test_harness2_meta_reference_catalog.py
PYTHONPATH=src python scripts/audit_historical_priority_backfill.py --check
```

Shared discovery, source, review-write, and watermark tests are also required. Commands are not evidence of execution; check delivered results and PR CI.

Actual checks passed: 196 discovery/review regressions, 95 new targeted checks, 30 docs tests, minimal wheel contract, metrics/GPU evidence validation, and strict build. Removed about 478 MiB of temporary sites, isolated installs, build caches, and upstream clones. Kept raw CPU runs (including early diagnostics), metrics, figures, and shared public data/model caches.
