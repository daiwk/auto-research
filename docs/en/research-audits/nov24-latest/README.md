<!-- source-sha256: e507956b66c37c18291a020ff25628be7fe1c6fe60ad67d8e27f8d882618dc55 -->
# November24 incremental selection and Google historical backfill

[简体中文](../../../research-audits/nov24-latest/README.md)

Eight papers: six first appearedNovember23, Pinterest Weight Coding onNovember22, and DCA is a historical backfill triggered by Google's latest blog (February10,2025 original; July23,2025v2 reviewed). These are not eight papers published today. VOPD has a Google DeepMind coauthor but a Stanford first author; DCA's first author remains UCI.

The2597 metadata records and883 November23 bulletin identities are recall pools. Newly captured recent first releases relative to the preceding batch are{'2026-11-20': 406, '2026-11-21': 302, '2026-11-22': 300, '2026-11-23': 464}, not equal counts of qualifying methods or a backlog. NoNovember24 first release was observed; selection announcement dates are not guessed. This finite selection does not close all-source review; the watermark staysNovember15.

Seven L1 components completed CPU three-seed diagnostics; DCA also ran on one real A100. MORSE is review-only. All high-cost full campaigns are not reproduced (review DONE), without retries. No checkpoint/data downloads or APIs, capability ranking or Evolve promotion. Weight Coding's Section4.7/Table4 is real production A/B, but its source-attributed lift is not site-wide lift.

## Complete list

| Domain | Paper | Original publication | Delivery |
| --- | --- | --- | --- |
| foundation-models | [DeepCrossAttention: Supercharging Transformer Residual Connections](../../../foundation-models/2502.06785-deep-cross-attention/README-en.md) | 2025-02-10 | L1 component |
| foundation-models | [The KL Divergence Is Never Negative, Except in PyTorch](../../../foundation-models/2611.30835-stablekl/README-en.md) | 2026-11-23 | L1 component |
| agent-research | [Optimistic Online Learning for Coding Agents with Aggregate Feedback](../../../agent-research/2611.30405-ooas/README-en.md) | 2026-11-23 | L1 component |
| agent-research | [Transport-Safe Evaluation of LLM Agents: Trajectory-Dependent Judge Error and Anytime-Valid Auditing](../../../agent-research/2611.30742-transport-safe-audit/README-en.md) | 2026-11-23 | L1 component |
| agent-research | [MORSE: Optimizing Streaming Memory Design via Open-World Auto-Research](../../../agent-research/2611.30011-morse/README-en.md) | 2026-11-23 | High cost, not reproduced |
| post-training | [Verifiable On-Policy Distillation](../../../post-training/2611.30325-vopd/README-en.md) | 2026-11-23 | L1 component |
| post-training | [Sparse Hodge Preference Optimization: Fine-Tuning Language Models toward Alignment beyond Transitive Preferences](../../../post-training/2611.30135-shpo/README-en.md) | 2026-11-23 | L1 component |
| recommendation | [Weight Coding: Evolving Web-Scale Recommenders through Direct Weight Edits with LLM Agents](../../../recommendation-components/2611.29613-weight-coding/README-en.md) | 2026-11-22 | L1 component |
