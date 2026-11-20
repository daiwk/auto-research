<!-- source-sha256: 88455e4cba860f5ffea74a05a31f5af232b3469b4b3fa71d8ae7c5f5a601e360 -->
# November20 paper scan and delivery

[简体中文](../../../research-audits/nov20-latest/README.md)

11 items:7 first releases from November19,3 November18 papers announced today, and1 historical November12 Canon paper. Nine bounded components/interfaces and2 review-only high-cost papers. Four CUDA components actually ran on an A100 with seeds42/43/44;44 individually reviewed bilingual questions and11 same-topic updates are included.

## Scope and evidence

The1884 overlapping metadata identities and1081 bulletin identities are recall pools, not counts of new papers or pending implementations. Primary review is limited to the fixed intake and explicit exclusions. This is not all-source exhaustion, and the global review watermark remains November15. Publication, announcement, directory observation and repository pushes remain distinct.

Google BuggyMLE and Meta fleet feature optimization receive priority. Canon's current first-author affiliation is Allen-Zhu Research; FAIR/Meta describes experiment provenance, not a rewritten current byline. LSER's online A/B did not enable auxiliary LLM features, so whole-stack online gains cannot be attributed to them.

All local runs are L0/L1 diagnostics, not model capability, online lift or Evolve promotion. High-cost full campaigns are not reproduced, review DONE, without automatic retry. VisAlloc half-precision and HiSA unsigned-position defects were fixed before the final freeze; the earlier unexecuted snapshot and prior independent CPU facts remain preserved. GrepMem operates on explicit component logs, not this user's Codex history, and is not disk compression.

## Complete list

| Domain | Paper | First publication | Local delivery |
| --- | --- | --- | --- |
| agent-research | [BuggyMLE: Scaling Machine Learning Engineering Difficulty with Bug Injection](../../../agent-research/2611.25088-buggymle-cci/README-en.md) | 2026-11-18 | l0_interface |
| agent-research | [Forget Freely, Grep Later: Lossless, Index-Free Memory for Long-Horizon LLM Agents](../../../agent-research/2611.25123-grepmem/README-en.md) | 2026-11-18 | l1_mechanism |
| system-one | [Stop Going in Circles:Loop-Triggered Routing for System 1 Decision Agents](../../../system-one/2611.25363-looproute/README-en.md) | 2026-11-19 | l1_mechanism |
| foundation-models | [HiSA: Sparsifying the Hidden Dimension of RoPE Attention in LLMs](../../../foundation-models/2611.26363-hisa/README-en.md) | 2026-11-19 | l1_mechanism |
| foundation-models | [Physics of Language Models: Part 4.2, Canon Layers at Scale where Synthetic Pretraining Resonates in Reality](../../../foundation-models/2611.24963-canon-layers-scale/README-en.md) | 2026-11-12 | Review only; not reproduced |
| post-training | [Policy Improvement-Guided Replay for Continual Reinforcement Learning](../../../post-training/2611.25989-colir-replay/README-en.md) | 2026-11-19 | l1_mechanism |
| post-training | [VisAlloc: Allocating Visual Supervision for On-Policy Self-Distillation](../../../post-training/2611.25069-visalloc/README-en.md) | 2026-11-18 | l1_mechanism |
| recommendation | [Cost-Aware Agentic Feature Optimization System for Fleet-Scale Ranking Models](../../../recommendation-components/2611.26531-fleet-feature-optimization/README-en.md) | 2026-11-19 | l1_mechanism |
| recommendation | [DNA: Unlocking Depth Scaling in CTR Models](../../../recommendation-components/2611.25659-dna/README-en.md) | 2026-11-19 | l1_mechanism |
| recommendation | [From Sessions to Serving: Integrating LLM-Based Embeddings into Retrieval for Production Content Recommendation](../../../recommendation-components/2611.26096-lser-serving/README-en.md) | 2026-11-19 | l0_interface |
| recommendation | [Antom 3-in-1 Transformer: A Payment Foundation Model](../../../recommendation-components/2611.25403-antom-3-in-1/README-en.md) | 2026-11-19 | Review only; not reproduced |
