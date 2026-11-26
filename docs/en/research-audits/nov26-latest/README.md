<!-- source-sha256: 075e6fbb253feed50fe4286f30f0477baa6c2b799aca7a0f0c253f24431066bb -->
# November26 incremental paper selection

[简体中文](../../../research-audits/nov26-latest/README.md)

All eleven selected papers first appeared November25, not eleven releases today. Delivery comprises seven L1 components(RAP, DuoMI, BRIAR, FEAST, HoMe, OneQuery, CAMAR), one L0 callback interface(DualPM), and three high-cost review-only entries(JEPA EU, CARE-OPD, Agentic LongLive). OneQuery/CAMAR full-text production A/B results are distinguished from local component evidence.

The 1200 metadata identities and 1157 current bulletin identities are recall pools. Newly captured recent first-release dates relative to the previous batch are {'2026-11-24': 194, '2026-11-25': 595}, not qualified-paper counts or an implementation backlog. Coverage records distinguish dates; selected announcement dates are not guessed. This finite selection does not close the full window; the watermark remains November15.

Eight components/interfaces completed CPU three-seed diagnostics, and CAMAR additionally ran on one real A100. RAP's core CPU experiments are affordable but its complete public evaluation matrix was outside this intake; it is not_run_scope_limited, not falsely cost-deferred. Other full campaigns assessed as expensive are terminally not reproduced(review DONE), without retries. No checkpoints/training data downloads, APIs, full capability reproduction or Evolve promotion.

Google/Meta priority records distinguish the new Google blog for already-cataloged FUSE from new papers, and historical code releases from maintenance. The official SCALE4D report has a separate primary cost review and first-publication-date limitation; an arXiv submission placeholder is not a public arXiv identity.

## Complete list

| Domain | Paper | Original publication | Delivery |
| --- | --- | --- | --- |
| foundation-models | [RAP: Radial-Angular Random Projection for Hyperbolic Representations](../../../foundation-models/2611.34298-rap/README-en.md) | 2026-11-25 | L1 component |
| foundation-models | [DuoMI: Dual Mutual Information Regularization for Expert Reuse in Looped Transformers](../../../foundation-models/2611.33952-duomi/README-en.md) | 2026-11-25 | L1 component |
| foundation-models | [Not all world models can doubt: how training objective and architecture shape epistemic uncertainty in JEPA and RSSM world models](../../../foundation-models/2611.34830-jepa-eu/README-en.md) | 2026-11-25 | High cost, not reproduced |
| agent-research | [HoMe: Toward Practical Harness Optimization of Memory Systems for AI Assistants](../../../agent-research/2611.34624-home/README-en.md) | 2026-11-25 | L1 component |
| agent-research | [Failure Broadens, Success Sharpens: Continual Adaptation of Tool-Use Agents Across Diverse Tasks with Dual-Polarity Memory](../../../agent-research/2611.33612-dualpm/README-en.md) | 2026-11-25 | L0 interface |
| multimodal-models | [Agentic LongLive: Asynchronous Agentic Memory for Long Video Generation](../../../multimodal-models/2611.34907-agentic-longlive/README-en.md) | 2026-11-25 | High cost, not reproduced |
| post-training | [BRIAR: Martingale Belief Smoothing on Bifurcation-Guided Reasoning Trees](../../../post-training/2611.34746-briar/README-en.md) | 2026-11-25 | L1 component |
| post-training | [FEAST: Fair and Efficient Adaptive Sampling for Task-Free On-Policy Learning](../../../post-training/2611.33827-feast/README-en.md) | 2026-11-25 | L1 component |
| post-training | [Collect for Coverage, Replay with Evidence: Adaptive and Efficient On-Policy Distillation for Long-Horizon Agents](../../../post-training/2611.34756-care-opd/README-en.md) | 2026-11-25 | High cost, not reproduced |
| recommendation | [OneQuery: Unified Sequence-to-Structure Generation for Multilingual E-commerce Query Understanding](../../../recommendation-components/2611.33653-onequery/README-en.md) | 2026-11-25 | L1 component |
| recommendation | [Multi-Modal Causal Disentanglement for Multi-Domain Sequential Audio Recommendation](../../../recommendation-components/2611.33628-camar/README-en.md) | 2026-11-25 | L1 component |
