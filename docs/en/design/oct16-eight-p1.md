# October 16: eight bounded P1 components and evaluation interfaces

<!-- source-sha256: 7022e500ba538cc4930ebbc44ff581b1ccd5eb9a965edb8b5854c6d109b745ab -->

[简体中文](../../design/oct16-eight-p1.md)

The user requested all eight in one MR, no expensive full experiments, and actual A100/A30 verification for CUDA. This closes implementation scope, not a new review round; the review watermark stays `2026-10-15T15:39:55+08:00`.

## Fixed scope

| Item | Required execution | Verification and limits |
| --- | --- | --- |
| OOB Regularization | Gaussian-quantile / spherical CPU anchor cache, actual training and refreshes, matched in-batch baseline | Fixed official CIFAR train subset with train/validation separation, bounded CUDA steps, not the full multi-dataset 100-epoch study |
| transparent-compact | Preserve exact dialogue, tool stubs, explicit omission markers, and recovery index | Real CPU message inputs; no fabricated memory accuracy or full 27B/128K multi-arm evaluation |
| FormCraft | Independently implement typed sequence composition, validation admission, persistent library, and recursive reuse | Real CPU operators and independent holdout; do not vendor without explicit license or call sequence-domain gains LLM capability |
| DrOPD | Top-k union/JS routing, candidate rewards, PPO-clipped updates, actual online token rollout | Tiny autoregressive model, public text, frozen teacher, isolated validation; not the original 11.83-hour math study |
| RAP-Walk | Clarity/cycle reliability, stationary credit, entropy tempering, GRPO advantage mixture | CPU graph/numeric controls and CUDA backward; no video model or large judge training, no video-quality claims |
| CTXGAP | Recompute pinned public tables and clustered intervals, isolate observer/reference, import external results | Historical recalculation is not independent reevaluation; T_public differs from T_full, retain failures, no original 37-run collection |
| Selective Reasoning | Recompute author's small release on CPU and implement gate/read/stop | Retain missing prefix trace/cache boundaries; recomputation is not online model ability |
| CLASHarness | Official format/trace analysis, gold-view isolation, defect and fairness audit import | Do not execute untrusted trace commands; mocks are diagnostic; no 8.5 GB full download or 15-model paid rerun |

## Cost and evidence gates

- Use one A100 or A30 at a time.
- Pin small public sources by revision/hash; prefer existing CUDA caches, with no new GB-scale checkpoint.
- Keep CUDA checks to minutes, recording step/sample caps and timeouts. Retain failures and negative results.
- Mark full expensive experiments **too costly; not reproduced (review DONE)** with `not_reproduced_high_cost`; do not auto-retry or queue them.
- Receipts bind actual execution commit/hash, public input revision, seed, command, metrics, and accelerator. Exclude hostnames, SSH aliases, usernames, drivers, and machine-specific build strings.
- Components, recalculations, and interfaces cannot automatically promote through Evolve. Tests and three seeds do not upgrade evidence.

## Executed acceptance

| Item | Actual result | Entry point and evidence |
| --- | --- | --- |
| OOB Regularization | A100 three seeds, four arms at 40 steps each, 512 train and 128 validation images; four CPU anchor refreshes per OOB arm; CLI and standalone agree by seed | [Paper and code](../../reproductions/2610.20158-oob-regularization/README-en.md), [CUDA receipt](../../gpu-validations/oob-regularization-a100-20261016.json) |
| transparent-compact | 196 actual public Pi messages, 54 original spans retained, 145 omitted payloads restored exactly by hash; no model calls | [Paper, commands, and CPU artifact](../../agent-research/2610.20116-transparent-compact/README-en.md) |
| FormCraft | Real three-seed CPU search and persisted libraries reloaded cold; final paired test used 12 targets and 24 observations per seed | [Paper and sequence results](../../agent-research/2610.19414-formcraft/README-en.md) |
| DrOPD | Three A100 seeds, independently initialized tiny autoregressive students, 64 actual online tokens and two PPO updates per seed; frozen teacher unchanged | [Paper and scope](../../post-training/2610.19572-divergence-routed-opd/README-en.md), [CUDA receipt](../../gpu-validations/divergence-routed-opd-a100-20261016.json) |
| RAP-Walk | Three A100 seeds and two explicit diagnostic graphs each; stationary residual below 1e-9; actual GRPO backward and updates | [Paper and scope](../../post-training/2610.20089-rap-walk/README-en.md), [CUDA receipt](../../gpu-validations/rap-walk-a100-20261016.json) |
| CTXGAP | 37 official tasks, 4,799 valid probes, 10,000 cluster bootstrap resamples; matches all fixed references and provides public-input/scoring isolation | [Paper and CPU statistics](../../agent-research/2610.20003-ctxgap/README-en.md) |
| Selective Reasoning | Nine groups and 29,808 author measurement rows, all 16,888 fixed values verified; gold-free start/read/stop interface | [Paper and CPU checks](../../system-one/2610.19644-selective-reasoning/README-en.md) |
| CLASHarness | Imported 775 audit checks, a 306-item conservative union, and 104 curated reference records. Retained one unscorable zero-required case; incomplete inventory cannot mean complete success. | [Paper and interface](../../agent-research/2610.19128-clasharness/README-en.md) |

OOB Gaussian and Contrastive each averaged **+0.02083** under the short A100 budget; Gaussian's across-seed standard deviation was 0.05083, and a CPU seed produced two negative deltas. This does not establish stable gains. DrOPD is tiny-model evidence; RAP-Walk did not call a video model or judge. CTXGAP, Selective, and CLASH author scores are not local model scores. None of the eight automatically promote in Evolve. Expensive full work remains `not_reproduced_high_cost`, review DONE.

### Failures found and fixed

- DrOPD kept the student in eval mode. CPU allowed backward, but cuDNN rejected RNN backward. Use temporary eval and explicit training forwards. Appendix-aligned `round(ρN)` kth-largest routing also covers K=0 and ties; regression and A100 rerun completed.
- The OOB unified entry called the shared device function with incorrect parameters. Fixed the runtime contract, including CPU/CUDA, explicit index, and MPS rejection, and ran the unified CUDA entry point.
- CTXGAP added zero-mass clusters, finite numeric weights, and plan checks before external calls; exact official recomputation was unchanged.
- CLASH cannot report complete success with partial verdicts. Caller-declared public input is the trust boundary; field filtering does not prove the entire text is answer-free.
- Transparent compaction preserved Pi toolCallId, errors, and execution metadata and reran the public session. Final active JSON is 138,550 characters; 129,010 is the pre-fix result only.
- FormCraft previously returned only in-memory counts. It now writes immutable per-seed snapshots and runs paired arms from cold-loaded libraries without changing splits or search counts.

## Delivery checks

Deliver separate code, commands, boundary tests, bounded evidence, Chinese paper pages, original figures, metadata, and classifications. Run spec, metadata, metrics, GPU evidence, full regression, and strict docs gates, then verify the single PR URL, diff, and CI. Report incomplete work instead of renaming evidence or weakening assertions.
