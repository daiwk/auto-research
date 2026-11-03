# Continued overlap scan, sources incomplete: 2026-10-05

<!-- source-sha256: 33d2b7b4023055daad8bef55d7972cbf47652139950946c2f33b58cf46d41d44 -->

[简体中文](../recent-paper-scan-20261005-followup.md)

Following [targeted October 5 review](recent-paper-scan-20261005.md), overlap from **2026-10-01**, last complete watermark **2026-10-02**. Official API/full text/author repositories and Google Research, DeepMind, Meta pages; no DeepXiv.

| Source | Status | Limit |
|---|---|---|
| arXiv post-training/foundations | Batch paging done; some ID checks hit 429 | Window hits only, not affiliation coverage |
| arXiv agents/industrial | 429, paging incomplete | Not a four-track scan; retry |
| Google Research/Meta | Timeouts | Cannot rule out priority omissions |
| Google DeepMind | Readable, reconciliation incomplete | Recheck with other official sources |

Raw new counts include older month-ID and out-of-scope hits, not October 2 publications or qualified papers. Full text and evidence gate determine candidates. coverage_complete=false; next overlap October 1.

- [Follow the Winners](../post-training/2610.03361-follow-the-winners/README-en.md): FIFO replay, repeated minibatch top-$K$ and KL-regularized CE projection; three-seed CPU bandit L1, not Search-R1/Sokoban or LLM capability.
- [AdaStep](../agent-research/2610.03223-adastep/README-en.md): action-grouped variance attribution at anchor states and step credit; three-seed synthetic rewards, not genuine agent training or task comparison.

Both v1 submissions **October 2**, announced **October 5**. Paper results and local diagnostics are separate.

[Meta AIMS](https://arxiv.org/html/2610.02600) has offline Recall/NDCG and industrial logs, but no randomized production A/B or full-traffic effect found in full text; not eligible for industrial implementation. [Pivot-SD](https://arxiv.org/html/2610.03665) needs real LLaDA-style denoising and training, not sampling heuristics. [RC-OPD](https://arxiv.org/html/2610.03515) has checkpoints/evaluations but pending training code; verify first-error repair, continuation and equal-budget controls. [DepGPO](https://arxiv.org/html/2610.03634) needs terminal dependency graph, verifier reads, training and no gold leakage. [Recursive Harness Self-Improvement](https://arxiv.org/html/2610.03548) needs a real generator, fixed verifier and same-cohort cost gate. [KV²](https://arxiv.org/html/2610.03198) links [author code](https://anonymous.4open.science/r/KVsquared-0B97/); CUDA claims require sanitized A100/A30 receipt.

These are review leads, not implementations or qualified decisions. Retry incomplete arXiv and affiliation sources first.
