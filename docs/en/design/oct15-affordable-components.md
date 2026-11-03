# October 15: five affordable components and interfaces

<!-- source-sha256: 45418d44fff02e3a762f77fcaeca7ac898f3d6beeb24d60e659890f81f461e20 -->

[简体中文](../../design/oct15-affordable-components.md)

This batch builds on merged PR #203. The user requested affordable components and interfaces from the afternoon candidates, not reopening expensive full experiments. Review watermark, prior decisions, and implementation acceptance stay separate.

## Fixed scope and acceptance

| Paper | Runnable scope | Verification | Full work not run |
| --- | --- | --- | --- |
| CASI, 2610.20293 | Immutable one-retrieval snapshot, deduplication, coalition-value cache, exact/permutation Shapley, shared group standard deviation, bounded zero-sum projection, and token/action advantage mapping | Additivity, interaction, negative marginals, frozen snapshots, query counts, mean/bounds, and actual bounded runs | Private auctions, LLM generation and multi-round policy training, production lift |
| PN-Mix, 2610.19605 | RoPE pair-norm precision allocation, 1-bit midpoint correction, sink/residual protection; quantized states enter real attention/cache consumption | CPU formula/boundary controls and actual A100/A30 inference diagnostic | Full 8B–32B, 32K-generation, multi-task sweeps and production throughput |
| SMRC / PMRC, 2610.19844 | Out-of-subspace residual, basis-change correction, paper optimizer updates, and actual optimizer checkpoint/resume | Numerical updates, basis-change/full-rank/zero-gradient boundaries, parameter updates and CUDA | Multi-scale pretraining on 2–8 cards, up to 26.84B tokens |
| Meta AutoformBench | Pinned upstream 341-task manifest, source-free boundary, export/execution config, official result import, protocol validation | Parse actual public tasks/results; reject unknown/duplicate/missing tasks, budget, and condition mismatch | Long Lean runs for nine frontier model groups; no textbook download or reuse of official source-present results as local source-free scores |
| JEPA prediction vs planning, 2610.19375 | Frozen decoder representation/prediction/excess error, shared training variance, episode isolation, paired planning, stratified paired bootstrap, degeneration/noise checks | Unequal episodes, paired seeds, zero variance, negative results, and controlled better prediction without better planning | Retraining three environments, full checkpoint ladder and decoder/planning seed study |

Results are component/interface or L0/L1 mechanism evidence, `diagnostic_only` and not automatic Evolve promotion evidence. Do not substitute private auction simulations, gold policies, or fabricated Lean successes for the paper.

## Cost and execution rules

- One A100 or A30 at a time; prefer existing public data/checkpoint caches.
- Finish CPU contracts and resource bounds first. GPU validation lasts minutes per component, not hours for the batch.
- Pin runs to immutable source commits; sync only relevant code/scripts and retain sanitized receipts and failures.
- Stop large, unresolved, or over-budget full experiments and mark **too costly; not reproduced (review DONE)**. Do not relax checks, hide failures, or use cheap substitutes to claim completion.
- AutoformBench paper front-page, software citation, and release-page dates mean different things. Do not invent an unverified first public date.

## Actual state

All full expensive experiments remain **not reproduced (review DONE)**. This was not a new discovery scan and does not change the review cutoff `2026-10-15T15:39:55+08:00`.

| Item | Implementation | Local/public-input run | CUDA where applicable |
| --- | --- | --- | --- |
| [CASI](../../reproductions/2610.20293-casi/README-en.md) | Snapshot, credit, and advantage complete | Five actions, 31 subsets, three-seed permutation diagnostic; not policy training | CPU only |
| [PN-Mix](../../reproductions/2610.19605-pn-mix/README-en.md) | Real bit packing and cache consumption | CPU/A100 random initialization; not pretrained LM evaluation | [Three A100 seeds and unified CLI](../../gpu-validations/pn-mix-a100-20261015.json) |
| [SMRC / PMRC](../../reproductions/2610.19844-smrc-pmrc/README-en.md) | Real optimizer and save/resume | Six controls on quadratic problem/small MLP; negative results retained | [Three A100 seeds and unified CLI](../../gpu-validations/smrc-pmrc-a100-20261015.json), including FP16/BF16 |
| [AutoformBench](../../agent-research/autoformbench/README-en.md) | Manifest, execution plan, and result/protocol interfaces | 341 tasks and 3,069 rows across nine CSVs; strict budget rejects actual excessive rows | Lean/model runs not executed |
| [JEPA protocol](../../foundation-models/2610.19375-jepa-prediction-planning/README-en.md) | Frozen decoder, error decomposition, and paired statistics | Actual MLP fitting on controlled arrays; leakage, aggregation, and negative-result tests; no new planning traces | CPU only |

## Real failures and integration review

Initial A100 SMRC/PMRC exposed a missing LAPACK dependency in the independent CPU oracle. Matching NumPy FP64 SVD/QR passed without changing CUDA optimizer, formulas, or tolerance. Both PN-Mix and SMRC/PMRC fixed a unified CLI silently falling back to CPU. Scripts and CLI then ran on A100 with matching key seed-42 values. Receipts retain failures and fixes.

All five gained Chinese method pages, complete metadata, and important paper figures. Catalogs show actual component/interface status. AutoformBench's first public date remains unknown. There is no new automatic Evolve promotion or hours-long training.

## Local verification

- Full regression: `3254 passed, 1 skipped` in roughly 4 min 55 sec. CUDA unit check skipped on Mac; separate A100 receipt records actual execution.
- Base-only wheel passed metadata and CLI checks without importing Torch/Transformers.
- Ruff, spec generation/checks, metric schemas, GPU receipts, platform integrity, review coverage, and implementation reconciliation passed; regeneration produced no diff.
- Strict docs passed. Removed roughly 412 MB of temporary environments, site output, and duplicate PDFs; retained public inputs and small evidence artifacts.

The optional PN-Mix real-checkpoint extraction path was not accepted end to end with actual weights and is outside the default cache receipt. It is not advertised as verified model adaptation. Use the latest PR commit's GitHub checks. Deliver all five in one MR, checking generated docs, GPU receipts, and required CI; do not auto-merge or deploy.
