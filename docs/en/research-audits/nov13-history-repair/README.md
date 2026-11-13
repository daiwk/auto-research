<!-- source-sha256: 1486e89f0263bdf21cf70edd97654696405e1f2155a6d4b0f7bad534b7633cbf -->
# November 13: ScientistTwo and Google/Meta historical backfills

[简体中文](../../../research-audits/nov13-history-repair/README.md)

This batch delivers **six historical backfills: four low-cost CPU control components and two review-only references**. None is a November 13 first publication. No full model or scientific campaign ran. Five have original-source scale evidence and are explicitly **not reproduced due to high cost; review DONE**. DS-STAR's development cost per task is not high; its complete commercial-model evaluation has a separate dependency disposition rather than invented large-training costs.

| Paper | Original v1 date, UTC | Delivery |
| --- | --- | --- |
| [ScientistTwo](../../../agent-research/2609.19644-scientist-two/README-en.md) | 2026-09-17 | Bounded stages, subset escalation, successful/failed history, strict improvement and review budgets |
| [DS-STAR](../../../agent-research/2509.21825-ds-star/README-en.md) | 2025-09-26 | External verifier/router append or backtrack control; the last budget-exhausted draft remains unverified |
| [ERA](../../../agent-research/2509.06503-era-flat-puct/README-en.md) | 2025-09-08 | Flat all-node PUCT, normalized ranks, ancestor visits and validation selection |
| [EnvHarness](../../../agent-research/2608.19880-envharness/README-en.md) | 2026-08-20 | Reachable replay, I/O contracts, shared-budget serial composition and original-verifier conjunction |
| [MLE-STAR](../../../agent-research/2506.15692-mle-star/README-en.md) | 2025-05-27 | Review of real ablation-guided two-level refinement and resources; no local Agent |
| [AlphaEvolve](../../../agent-research/2506.13131-alphaevolve/README-en.md) | 2025-06-16 | Review of program evolution, asynchronous cascaded evaluation and author artifacts; no local search experiment |

Google/DeepMind priority follows verified bylines or official research provenance, not the word “Meta” in a title or a citation. First-author institutional grouping is separate: EnvHarness's first author is at Washington University in St. Louis; Google internship and coauthor evidence do not justify changing that affiliation to Google. The bounded Meta check established no additional fixed paper identity in this focused family. Unavailable directories and other limits remain explicit, not a claim that Meta has no omissions anywhere.

## Why ScientistTwo was absent

Before repair, the identity was absent from the canonical manifest, ledger, retained review records and implementation. The September 19 summary claimed September 15–18 coverage but omitted it. Retained captures cannot reconstruct the complete historical recall chain. **No particular query, deduplicator or P2 decision is established as the sole cause.**

The demonstrated process gap is that recent deltas, first/last-page checks and date/abstract-level dispositions do not replace independent historical identity reconciliation. Old records remain snapshots; this is a new backfill, not a rewrite claiming earlier review. The [priority review](../../../research-audits/nov13-history-repair/priority-inventory-review.json) and [ScientistTwo review](../../../research-audits/nov13-history-repair/scientist-two-review.json) record sources, original dates, affiliations, code availability and method/cost locations.

## Discovery changes

The [historical reconciliation tool](history-reconciliation.md) now runs in default discovery:

- Preserve exact arXiv identities, visible versions, actual page URLs, capture times and decoded-text hashes before recent-date filtering.
- Match the canonical manifest and substantive method/cost terminals independently. Old P2 selection, date screening and generic known labels cannot close protected Google/Meta method review. Explicit high-cost and archived-source decisions do not retry automatically.
- Embed the report in the main payload and save `paper-candidates-*-historical-review.json`; the daily workflow uploads both.
- Existing Google, DeepMind and Meta pages and the new COLM source retain bounded budgets. Configuration, HTTP success and an empty recent delta do not prove exhaustive history.

The captured Google COLM 2026 page exposes **28 unique identities**. A committed [source observation](../../../research-audits/nov13-history-repair/historical-source-observation.json) supports [offline reconciliation](../../../research-audits/nov13-history-repair/historical-source-reconciliation.json). This cross-domain event inventory is not 28 qualifying omissions or implementation tasks. Unreviewed identities remain explicitly unreviewed. PolicyBank is a traceable lead outside this batch's selected focus, not an implemented algorithm. The watermark remains **November 9, 2026**; no newer full window is closed here.

## Execution and evidence tier

Four components actually ran seeds **42, 43 and 44** after source freezing. See the [portable source proof](../../../research-audits/nov13-history-repair/frozen-sources.json), [raw CPU results](../../../research-audits/nov13-history-repair/raw-cpu.json), and per-paper `metrics/component-cpu-seeds42-44.json` files.

```bash
PYTHONPATH=src:scripts python scripts/run_nov13_history_components.py --check
PYTHONPATH=src python scripts/reconcile_priority_history.py \
  --artifact docs/research-audits/nov13-history-repair/historical-source-observation.json \
  --output /tmp/priority-history-current.json
```

The first command checks committed sources, Git-object proofs, raw results and metrics offline; the second recomputes identity status against the current manifest/ledger. Neither reads uncommitted `.cache` captures, accesses the network or trains.

Seeds vary explicit control fixtures, not independent scientific tasks. LLMs, semantic judgments, generated code/sandboxes, scientific execution, file analysis, EnvRigger and real benchmark bridges are not fabricated. Evidence remains `l1_mechanism / diagnostic_only`, with no capability comparison, Evolve promotion or executable integration. There is no advertised CUDA path, so no A100/A30 receipt is needed or invented.

Full campaigns do not download resources, call commercial models, start long training or retry merely to test their cost. DS-STAR's reported USD 0.23 is an author average on ten development tasks, not a local cost or timing for its complete three-benchmark matrix; the commercial-dependency disposition remains separate.

## Learning and bilingual delivery

All six papers have complete metadata, an original key figure, Chinese explanations and individually reviewed English pages. Each adds separate basics, mechanism, comparison and implementation questions: **24 questions** in total. Topic deep dives include actual comparison papers, source fingerprints and reviewed English. Learning pages and the dashboard regenerate from per-paper facts; review-only references do not fabricate metrics.

The [fixed scope](../../../research-audits/nov13-history-repair/task-scope.json) distinguishes completed components, full campaigns not reproduced, unselected leads, source exceptions and non-exhaustive limits instead of collapsing them into “all history complete.”
