# 2026-10-19 evening announcement: Low-cost components and a revision upgrade

<!-- source-sha256: 1e7cff5f20ea5ce6026946c6ea507bfcb286b73032c0146a830361f81e7c4edb -->

[简体中文](../../../research-audits/oct19-evening-components/README.md)

One MR covers **14 papers: 11 executable components or interfaces and three documentation-only entries**. Thirteen identities are newly listed in the October 19 announcement, with first releases mostly October 15–16. UniRec is a **substantive v3 update** to a September paper, not a fourteenth same-day first release. Priority Google/Meta review included MSU/Meta ProPerAgent and ASU/Meta EgoP²C.

## Full scope

| Domain / priority | Paper | Executable local scope | Verification |
| --- | --- | --- | --- |
| Agent / P0 | [ProPerAgent](../../../agent-research/2610.22671-proper-agent/README-en.md) | Causal graph memory, PPR, source-admission gate, and joint content × timing score; external extraction and semantic models | CPU, 42/43/44 |
| Agent / P1 | [HDA](../../../agent-research/2610.22466-harness-decomposition/README-en.md) | Four-arm paired bootstrap, human-confirmed controls, and signed decomposition of compute, overfitting, and residual upper bound | CPU, 42/43/44 |
| Agent / P1 | [DRAGO](../../../agent-research/2610.22568-drago/README-en.md) | Grounded STRIPS delete relaxation, complete BFS diagnostics, and repair gate that rejects weakened problems | CPU, 42/43/44 |
| Multimodal / P0 | [EgoP²C](../../../foundation-models/2610.22681-ego-p2c/README-en.md) | Role FFN/LoRA, context allowlist, actual segment sampling, and MOPD with assigned frozen teachers | A100, 42/43/44 |
| Foundation models / P1 | [BMuon](../../../foundation-models/2610.23571-bmuon/README-en.md) | Global-channel-budget MM allocation and bilateral weighted polar update; exact SVD, not a fast kernel | A100, 42/43/44 |
| Foundation models / P1 | [Sink-Sparse](../../../foundation-models/2610.22975-sink-sparse/README-en.md) | Calibration block mass, coverage prefix mask, and correct pooled-KV/LSE fusion | A100, 42/43/44 |
| Post-training / P1 | [TreeOPSD](../../../post-training/2610.23181-treeopsd/README-en.md) | Shared complete prefix tree, policy probability backup, bounded posterior KL, and actual tiny-policy updates | A100, 42/43/44 |
| Post-training / P1 | [SimOPD](../../../post-training/2610.23306-simopd/README-en.md) | Student generation, paired pre-update FIFO bank, and relational-distribution KL across hidden dimensions | A100, 42/43/44 |
| Post-training / P1 | [GR-OPD](../../../post-training/2610.23042-gr-opd/README-en.md) | Discounted means, group-relative sequence credit, response-balanced PPO, and frozen teacher | A100, 42/43/44 |
| Search/ads/recs / P0 upgrade | [UniRec v3](../../../reproductions/2609.11052-unirec/README-en.md) | CPPA/CAPP, within-group AGRR KL, and stop-gradient cross-stage objective; old heuristics relabeled concept demo | A100, 42/43/44 |
| JEV / P1 | [Portuguese IR](../../../foundation-models/2610.23346-jev-portuguese-ir/README-en.md) | Batched ranking by independent probabilities, exact coverage, linear nDCG/MRR, κ/τ-b, plus recomputation of published tables | CPU, 42/43/44; no JEV calls |
| World models / P1 | [PPMem](../../../foundation-models/2610.23795-ppmem/README-en.md) | Method, metadata, original figure, code availability, and cost assessment only | Full experiment not reproduced, DONE |
| Post-training / P1 | [MGE-PO](../../../post-training/2610.23245-mge-po/README-en.md) | Documentation only: four-quadrant credit, curriculum, entropy KL, and experimental limits | Full experiment not reproduced, DONE |
| Post-training / P1 | [MultiAgent-OPD](../../../post-training/2610.23234-multiagent-opd/README-en.md) | Documentation and cost assessment only: two-stage teacher/student teams and role-specific supervision | Full experiment not reproduced, DONE |

## Original sources and dates

The [source receipts](../../../research-audits/oct19-evening-components/source-coverage.json) cover 51 actual pages: eight arXiv category announcements, 28 Google pages, six Meta pages, and nine DeepMind pages. All eight announcements display **2026-10-19**, with 1,344 parsed category entries including cross-lists and replacements. **That does not mean 1,344 new papers.** Parsed totals match displayed totals, not completed full-text review.

Official catalogs were compared with the previous SHA256 snapshot. Google 417, Meta 144, and DeepMind 265 unique URLs show no additions or field changes. A static catalog does not mean Meta has no new arXiv papers; two priority papers were identified from full-text affiliations. Complete abstracts stay in local audit inputs. Git retains URL, time, SHA256, counts, and comparison baseline per page instead of megabytes of abstract snapshots.

This is a **selected implementation batch**, not exhaustive coverage. Missing A/B wording in abstracts was not used to reject industrial papers. UniRec v3 full text specifies nine weeks of monitoring, 5% randomized traffic, final-week KPIs, and full deployment; old documentation's 20%/one-week numbers and mechanism evidence level were corrected.

Other candidates reviewed did not automatically become components: QART/Ori were not in this scope. Flash RNN-T's defining contribution is kernel fusion and recomputation, not a PyTorch wrapper. For AuditKIT and Tool Recommendation, avoid duplicating mature upstream or treating a closed-service retrieval shell as a model. Candidates without completed full-text review are not marked implemented or fully closed.

## Actual runs and evidence levels

Pin execution source to `73a1e8b818bdddcdc33be13902e4d4c335c8fa26` before running seven items on a real **NVIDIA A100-SXM4-80GB**, each with three seeds. Three GPU runner groups took roughly 1.68 s, 2.23 s, and 1.44 s, excluding SSH and loading. No dataset or checkpoint downloads or long experiments. Small tensors and random tiny policies verify mechanisms, not production, language, or vision tasks.

Per-seed metrics and GPU receipts are linked from the paper pages. The [frozen-source Merkle proof](../../../research-audits/oct19-evening-components/frozen-sources.json) supports offline shallow-clone validation after squash without requiring old branches. Receipts retain accelerator model, public synthetic recipe, command, commit, seed, outcomes, and hashes, not host aliases, usernames, or driver build strings. Full raw traces are stored locally in `runs/oct19-evening-components/`; Git per-seed files contain only scalars and audit hashes instead of thousands of duplicate trace lines.

All outputs use `diagnostic_only=true`, `promotion_eligible=false`, and `evolve_integrated=false`. EgoP²C's fixed PLAN/DIRECT skeleton and random frozen teacher, deterministic Agent callbacks, and the inert JEV provider are diagnostics, not language, video, or agent capabilities. The [JEV published confusion-matrix arithmetic check](../../../research-audits/oct19-evening-components/jev-published-table-arithmetic.json) is separately labeled recomputation of published aggregates, not new-model inference.

## Fixes and acceptance in this batch

- Preserve the distinct level-1 meanings for Quati and JurisTCU; check both probabilities for finiteness and normalization to prevent NaN bypass.
- GR-OPD chooses an equivalent PPO branch in log-ratio space to avoid `0×inf` backward NaNs after positive-advantage clipping. Reject unrepresentable negative-advantage branches explicitly.
- SimOPD rejects zero hidden dimensions and dtype changes. BMuon restores the global step and fixes allocation at subnormal scores.
- Review paper figures visually, correct ProPerAgent's PDF Figure 5 versus HTML numbering, and remove unrelated text from HDA/BMuon/MultiAgent-OPD crops.
- Preserve UniRec's historical −12.58% NDCG@10 result, correcting only the concept-demo evidence label. New operators do not retroactively upgrade old adapter fidelity.

All 14 **full experiments** are too expensive and not reproduced (review DONE). They do not retry automatically, enter the implementation queue, or block the batch. Eleven component acceptances are recorded separately from full-paper reproduction.

## Coverage and watermark

Full-text review across all sources and announcements is not closed, so **the review watermark remains 2026-10-15**. Announcement observation dates, closed candidates, passing components, and full-window watermark are different fields. Eleven passes do not advance coverage to today.
