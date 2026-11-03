# Targeted new-announcement review, incomplete coverage: 2026-10-05

<!-- source-sha256: 23ad755aa0fdbccb1b30a6aab0df527ddc7d7f458b7963bc7757487a79f9d8bd -->

[简体中文](../recent-paper-scan-20261005.md)

Keep the October 2 watermark and October 1 overlap. October 5 announcements in [cs.LG](https://arxiv.org/list/cs.LG/recent), [cs.CL](https://arxiv.org/list/cs.CL/recent), [cs.AI](https://arxiv.org/list/cs.AI/recent) and [cs.IR](https://arxiv.org/list/cs.IR/recent) include v1s actually submitted **October 2**. No DeepXiv. Recommendation API stalled at the first batch and was stopped; other tracks and Google/Meta did not finish full paging. coverage_complete=false; targeted reading is not high-recall coverage.

[LESSER](../post-training/2610.03702-lesser/README-en.md) implements output-layer analytic gradients, shared two-sided Rademacher projection and round-robin selection. Three-seed CPU autodiff identity checks are L1, not LLM post-training or paper speed. First author at University of Pennsylvania; no author code link found.

| Lead | Mechanism | Required checks |
|---|---|---|
| [Recursive Harness Self-Improvement](https://arxiv.org/abs/2610.03548) | RSI/agent data, fixed verifier, real generator, same-cohort cost gate | Verify code/model and public tasks; no static self-evolution |
| [RC-OPD](https://arxiv.org/abs/2610.03515) | Student first-error repair and continuation | Real teacher/student correction trajectories, matched baseline and A100/A30 before CUDA claim |
| [DepGPO](https://arxiv.org/abs/2610.03634) | Terminal read/write graph and actual verifier reads | Auditable trace, no gold leakage, real policy updates |
| [AIMS](https://arxiv.org/abs/2610.02600) | Industrial recommendation + LLM; abstract offline Recall/NDCG | Check full text for A/B/full traffic; otherwise exclude from industrial |

Google/Meta remain priority; incomplete source review cannot establish no qualifying papers since October 1. These priorities are not terminal decisions. Complete full-text/source checks without treating delayed announcements or omissions as new publications.
