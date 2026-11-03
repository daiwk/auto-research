# 2026 historical P0: Fixed implementation roadmap

<!-- source-sha256: 64edff5080d30f518d9e4aae55541541c61540505e41091024dc3756feae9523 -->

[简体中文](../../paper-audits/2026-historical-p0-implementation-roadmap.md)

This roadmap freezes the **55 P0 papers** promoted in the full-text review [decision file](../../paper-audits/2026-historical-fulltext-decisions.json). Each paper appears once. Implementation follows H01→H07 instead of selecting from chat history. See the [full-text audit](2026-historical-fulltext-review.md) for titles, text fingerprints, evidence sections, and online metrics.

`DONE` means the adapter, detail page, public-data metrics, tests, and applicable evolve mappings were committed. `QUEUED` means a paper is on the fixed implementation list but not yet implemented.

| Batch | Status | Count | Fixed paper list |
|---|---:|---:|---|
| H01 · Google / Meta highest priority | DONE | 4 | `2607.25110` Memory Layer; `2606.00282` SCALR; `2604.12965` HILL; `2606.07546` Semantic-Native Long Sequence Modeling |
| H02 · 2026-08 to 2026-07, first group | DONE | 8 | `2608.12778`, `2608.10182`, `2608.07055`, `2607.28940`, `2607.28895`, `2607.26427`, `2607.26418`, `2607.25344` |
| H03 · 2026-07 to 2026-06, second group | DONE | 9 | `2607.24025`, `2607.23038`, `2607.10910`, `2607.10239`, `2606.29946`, `2606.27058`, `2606.25496`, `2606.16838`, `2606.16641` |
| H04 · 2026-06 to 2026-05 | DONE | 9 | `2606.10357`, `2606.08466`, `2606.06970`, `2606.03866`, `2607.19357`, `2605.27103`, `2605.27043`, `2605.16479`, `2605.05855` |
| H05 · 2026-04 to 2026-02, first group | DONE | 10 | `2604.18146`, `2604.17878`, `2604.10471`, `2603.28124`, `2603.21481`, `2603.19665`, `2603.04227`, `2603.00980`, `2602.13581`, `2602.13134` |
| H06 · 2026-02, second group, to 2026-01 | DONE | 8 | `2602.12972`, `2602.12593`, `2602.12564`, `2602.12041`, `2602.10455`, `2602.09386`, `2602.08530`, `2601.21285` |
| H07 · 2026-01, final group | DONE | 7 | `2601.20215`, `2601.18664`, `2601.17836`, `2601.14333`, `2601.06873`, `2601.04674`, `2601.02955` |

## Batch acceptance contract

Each batch must complete all of the following:

1. Include the original publication, first author affiliation, exact v1 date, upstream code status, adapter, and local directory.
2. Run the paper's defining mechanism. Identify public-data substitutions and production components not reproduced. An interface stub is not a reproduction.
3. Preserve per-seed metrics, means, standard deviations, and 95% confidence intervals, including negative results.
4. Include the paper's key original figure and source.
5. Register composable mechanisms as traceable evolve operators.
6. Add documentation-contract, mechanism, and catalog-generation tests. A path advertised as requiring CUDA needs a sanitized A100/A30 receipt.

## Completeness

Batch counts sum to `4 + 8 + 9 + 9 + 10 + 8 + 7 = 55`. Other historical candidates stay in the audit JSON and are not mislabeled as pending P0 implementations.
