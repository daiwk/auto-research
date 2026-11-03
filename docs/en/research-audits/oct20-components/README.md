# October 20, 2026: New announcement, ten low-cost components and three high-cost references

<!-- source-sha256: 29273be141d4aabcc32e3eac6c3885cef0525672bb9e823e46eb2f69fa02b4c5 -->

[简体中文](../../../research-audits/oct20-components/README.md)

We deduplicated after batch #211 merged. The arXiv announcement is October 20, but v1 dates differ. Announcement, catalog, and PDF cover dates are not first-publication dates. Historical backfills and material revisions are not mixed into new-identity counts.

## Fixed scope

| Area | Paper | Local scope |
| --- | --- | --- |
| Recommendation | [SID Topology](../../../recommendation-components/2610.26105-sid-topology/README-en.md) | CPU frozen old paths, HC buckets, new-item insertion, and drift auditing; semantic prefixes supplied externally |
| Foundation | [t-Muon](../../../foundation-models/2610.24938-t-muon/README-en.md) | A100 M-transform, slice-wise polar decomposition, inverse transform, and Nesterov update |
| Foundation / JEPA | [Time-JEPA](../../../foundation-models/2610.23982-time-jepa/README-en.md) | A100 physical-sequence alignment/pooling, training statistics, shared two-path video, and EMA isolation |
| Foundation | [KronLSTM](../../../foundation-models/2610.26834-kronlstm/README-en.md) | A100 Kronecker scalar associative erase, key-axis forgetting, and full small mixer |
| Post-training | [SPOD](../../../post-training/2610.25034-spod/README-en.md) | A100 full action probability, success-conflict gate, soft floor, three-level averaging, and actual tiny-policy updates |
| Post-training | [APSD](../../../post-training/2610.25973-apsd/README-en.md) | A100 same-policy feedback self-teacher, student-dependent PoE targets, and reverse-KL gradients |
| Post-training | [TAR](../../../post-training/2610.24236-tar-adaptive-replay/README-en.md) | A100 FPS over verified base trajectories, two-level suppression gates, detached replay, and actual tiny-policy updates |
| Agent | [MemPrice](../../../agent-research/2610.24955-memprice/README-en.md) | CPU exact multiple-choice knapsack, dynamic prices, and persistent long-run queue |
| Agent | [SCOPE](../../../agent-research/2610.23128-scope-replay/README-en.md) | CPU stateful API replay, aliasing and side effects, and instance-local authentication; no untrusted code execution |
| Agent | [TokenWorth](../../../agent-research/2610.26453-tokenworth/README-en.md) | CPU logistic prior, kernel residual, diagonal AGOP, end-of-task feedback, and admission/replacement gate |
| Foundation / Agent | [Meta Muse Glimmer 30B](../../../foundation-models/2610.24628-muse-glimmer-30b/README-en.md) | Priority reference; no 30B weights, full training, or long-trajectory evaluation |
| Industrial ads | [MAPS](../../../recommendation-components/2610.25748-maps-creative/README-en.md) | Quantified online A/B in the body; full eight-H100 video ad system not reproduced |
| Agent / RSI | [World of SWECraft](../../../agent-research/2610.24061-world-of-swecraft/README-en.md) | >10,000-hour software-ecosystem collaboration not reproduced; project source-release status unverified |

All 13 full experiments are **too costly, not reproduced (review DONE)**. The ten components separately passed bounded mechanism checks. All results are `l1_mechanism` and `diagnostic_only=true`, ineligible for evolve promotion; no full-paper capability or production gain is reproduced.

## Execution and traceability

Six CUDA components ran on one actual A100, each with seeds 42, 43, and 44, independent numerical/gradient references, real parameter updates, and negative controls. Four CPU components ran the same seeds. Frozen recipes define synthetic inputs; no weights, real corpora, or private data were downloaded. Paper pages link metrics; receipts are in `docs/gpu-validations/*-a100-20261020.json`.

CUDA code and runners were committed before execution. [Frozen-source Merkle proof](../../../research-audits/oct20-components/frozen-sources.json) supports offline checks after shallow clones or squash merges. Raw successes and early foundation diagnostics with mismatched aggregate types remain in ignored `runs/oct20-components/`. Public metrics only retain scalars, recipe/source/artifact hashes, and audit summaries.

Cross-review fixed SCOPE dictionary ordering, signed floating zero, and tuple alias authentication, with terminal-state mutation and unsupported-object regressions. TAR now rejects positive log-probabilities and guards extreme norm overflow. Early GPU numerics passed but aggregation converted booleans to numbers; the runner was corrected, frozen again, and rerun without weakening checks.

The label/count AST inventory added seven count positions across two files. MemPrice clocks only affect resource prices. TokenWorth fit, feedback, accesses, and hits update only after tasks finish; they do not expose current gold or establish execution capability. Growth from 153 to 155 files is an audit index, not proof of semantic safety; behavioral regressions and diagnostic limits still apply.

## Sources and exceptions

[Capture receipt](../../../research-audits/oct20-components/source-coverage.json): 29 Google, six scoped Meta, nine DeepMind, and eight new arXiv announcement pages, 52 pages total. The eight categories have 2,920 entries **including cross-category duplicates and replacements**, not 2,920 new papers. Google added four URLs, Meta one, and DeepMind zero; catalog additions are not qualifying papers.

Meta Muse Glimmer received priority review of full text and official resources. DuoLM has a DeepMind coauthor but body evidence is public benchmarks and H100 throughput, not production A/B or approved full rollout, so the industrial gate was unchanged. Google's Claim-Gated listing lacks a resolvable publication and source; it remains an unconfirmed archive exception rather than an invented implementation. Unread full texts and unexhausted institutional pages were not declared closed.

The fixed 13 deliveries do **not advance the global watermark** beyond 2026-10-15. High-cost entries do not queue, automatically retry, or block a future watermark; advancing requires a separate review closure for the window.

## Maintenance checks

```bash
PYTHONPATH=src python scripts/curate_oct20_component_evidence.py finalize
PYTHONPATH=src python -m pytest tests/test_oct20_component_contracts.py
PYTHONPATH=src python scripts/validate_gpu_evidence.py
```

Initial curation requires real raw JSON, not prefilled pass labels. Figures come from the papers with accurate captions; performance plots, motivation diagrams, and pseudocode are not all labeled architecture.
