# 2026-10-11 implementation batch: Scope and actual status

<!-- source-sha256: d8e78cd15961e8d479e5aaa43c0ca67ff37ec9e0a1681b097240aad4320eef32 -->

[简体中文](../../research-audits/oct11-implementation-scope.md)

This resumed the October 8 batch of 12 papers, one diagnostic facility, and four evidence closeout items. It was not a new scan. Unfinished work remains explicit; formulas, registration, or short GPU smoke tests do not substitute for full implementation.

| Priority | Item | arXiv | Status |
|---|---|---|---|
| P0 | ZIP-SR / ZE-EDEN | 2610.12444 | Core, real evolve behavior tests, and three-seed A100 WikiText-2 comparison complete. Static eager implementation; negative results retained |
| P0 | VFold | 2610.12338 | CCA, Hungarian head matching, function-preserving folding, and actual shared cache implemented. A100 exposed BF16 calibration and cache API issues; compatibility fixed and rerun. Original LongBench/RULER incomplete |
| P0 | Option-Channel Attack | 2610.12292 | Six strategies, calibration-only label selection, isolated evaluation, conditional ASR, paired intervals, and real Laya on A100. Some strategies already fail on clean inputs; undefined ASR retained. Full model/shield datasets incomplete |
| P0 | ReCal | 2610.11332 | Actual FFN deletion, damage weights, SFT→OPD runner, tests, and A100 control. Four-item diagnostic with negative post-OPD result, not four-domain benchmark |
| P0 | ZCPO | 2610.12161 | Core, boundary tests, and actual 24-step A100 updates. Current source and train-only manifest rerun passed; metrics/receipt/docs registered. Retain original all-skipped and mislabeled test audit. Not full-scale capability reproduction |
| P1 | SparseDecoding | 2610.12327 | Decoding-only Wanda, 32-bit masks, and actual Triton SpMV. Four A100 numerical modes and 4B three-recipe control. Negative quality and throughput retained. Not original SparseGPT/long-text benchmarks or author kernels |
| P1 | V-CoLA | 2610.11251 | Real Qwen3.5-9B delta-state capture/replay, visual merging, and layer-24 exit verified on A100. Four held-out CIFAR constrained first-letter items, not full answers, original benchmarks, or speedup |
| P1 | Data-Space Iteration | 2610.12102 | Alternating DMD updates of shared generator, real frozen teacher, and trainable fake on A100 across three seeds. One improves, two regress. Pixel-pooled Fréchet is not Inception FID |
| P1 | OnTrack | 2610.12375 | Streaming UFGW, lifecycle/gate, 16 numeric/behavior/isolation tests, and pinned CPU trace rerun. On 64 examples AUROC 0.6021; difference interval crosses zero and calibrated stop policy is inert. Not live SWE-bench or production safety |
| P1 | Memento3 | 2610.11794 | Real frozen 7B generated bounded Python worlds with safe AST interpretation, replay, and actual interaction. First action falsified model; repair and task failed. No paid calls or handwritten navigation fallback |
| P1 | PIVOT | 2610.11167 | Loss, reference KL, domain reward, 385/77 train-only split, real 0.5B/7B shared-teacher SFT→OPD and three A100 recipes. Eight real steps per arm, auditable routing, all 0% on eight validation items. Negative result, not full-budget/full-parameter capability |
| P1 | SGUID | 2610.12367 | Preregistered 9B A100 two rounds of 200 probes / 32 compact steps; 464 updates and 6/3 skills. Verified source chain, restoration, current-student candidate generation, and sanitized receipt. Four-item EM 75%→25%, two truncations both times. L1 execution only; two old failures retained |
| P1 infrastructure | OPD Learning Signals | 2610.11247 | Residual loss, pre-clip gradient proxy, two-fold occupancy, parameter displacement, and FP64 CKA. Three A100 steps collected all 37 representation positions with receipt; not the 200-step plateau |

## Four closeout items

1. **Review/delivery reconciliation:** Generated `oct07-review-closure/implementation-status.*` without changing frozen reviews. The 494 accepted identities were not counted as implemented. Strict source-exhaustiveness remains retired.
2. **Actual training evidence:** CUDA paths have bounded A100 runs and sanitized receipts. SGUID two-round expansion passed independent mechanism checks. Retain failures, truncations, and mismatches. More seeds do not promote diagnostics or reproduce original budgets.
3. **Evolve:** ZIP/ZE have executable optimizers and source-bound validation tests. Register other operators only after working controller execution.
4. **Regression, compatibility, and CI:** Added reconciliation and algorithm tests. Before SGUID evidence, 1,609 local tests and remote quality/docs passed. Later results are below; old green checks do not cover new commits.

## Resume checkpoints

The ordinary sandbox terminal still reported ENOENT. Approved explicit `/bin/bash` could read the checkout, run tests, and SSH; the default launcher was not shown fixed.

Current SparseDecoding A100 source was verified file by file against local hashes. User-authorized public 0.5B weights, Banking77 train-only partitions, and five CIFAR-10 train files were synchronized with provenance and checksum checks. No test, private data, or full workspace transfer. PIVOT SFT→OPD→three recipes ran; Data-Space and V-CoLA used real training images for their bounded experiments. Initial download and backward failures remain in the runtime audit.

SGUID two-round GPU acceptance finished October 12. Old 9B failures remain tied to original source. The expansion is separate and negative. PR #199's V-CoLA dependency failure was fixed: 29 checks passed per old/new version, real 9B A100 paired forwards on 5.19 were rerun, and a new receipt was registered. Commit `6a3298e0` passed contracts, minimal-install, and docs build; PR deploy skipped by design. Merge/deploy remain user decisions.

After the user chose to continue SGUID, [preregistered expansion](oct11-sguid-expanded-protocol.md) fixed first 200 train questions, 32 candidates, 200 probes and 32 compact steps per round, and independent 3072-token validation. No h or gate changes, error-based selection, or seed shopping. CPU tests verify independent budget; actual two-round updates, persistence selection, and weight chain were checked.

A100 expansion binds `319008f6`; all five executed source files match that commit and train/validation match public split digests. Independent artifacts and original 5.14 environment were used. V-CoLA 5.19 ran from an isolated install without changing shared training. Final adapter displacement 0.173899; four-item EM fell 0.75→0.25, two truncations each. [Receipt](../../gpu-validations/sguid-a100-20261012.json) states `capability_passed=false`, not formal comparison or evolve promotion.

First full regression found math-delimiter and Memento3 original-figure contract failures. After repair, 1,583 tests passed (323 seconds), plus the dependency contract. Ruff, compilation, isolated base-wheel install, strict docs, specs, GPU gate, metric migration, and generator idempotence passed. SGUID evidence required separate documentation/metric/registration rechecks. Local success is not remote CI.

All work was kept in PR #199. Original-budget experiments, 494 historical acceptances, and complete evolve capability are not claimed.

After compatibility and independent-budget changes, **1,609 tests passed** in 344 seconds with 23 existing warnings. New V-CoLA A100 gate, Ruff/compile, specs, reconciliation, generators, zero-change metric migration, and strict docs passed. This did not replace SGUID expansion acceptance or pending remote CI.

## Final October 12 closeout

Registered SGUID stable metrics, source-bound receipt, specification, and organization/topic/year catalogs. One public dashboard experiment was added, with existing experiments unchanged. The card shows baseline/final and negative delta as L1, not formal comparison; a new regression verifies single-seed display. Old failures unchanged; no weights, private data, or machine identity committed.

After adding SGUID, **1,612 full-suite tests passed**. Final metric/display changes passed 47 targeted tests. Ruff, JS syntax, compilation, strict docs, specs, reconciliation, GPU gate, zero-change migration for 723 metrics, and generator idempotence passed. See [PR #199](https://github.com/daiwk/auto-research/pull/199) for actual final remote checks. No merge or deployment performed.

The 12 papers, one facility, and four closeout items are complete under the stated protocols. Original full-budget benchmarks, formal capability gains, 494 uncataloged historical acceptances, and evolve mappings without controller evaluation are outside this claim.
