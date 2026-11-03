# Overlap scan and closeout: 2026-09-30

<!-- source-sha256: b4a21d356a2153b268380e5043dc36eb8eedc2bca82176d1b4948f96e00afc0c -->

[简体中文](../recent-paper-scan-20260930.md)

Requested September 27–30 across four arXiv tracks. All live pages complete with zero cache fallback. Hits 197/1081/569/976 are broad query pools with overlap, not one day's eligible papers. Filtering to v1 after September 29 leaves 8/127/62/78, still needing full text, deduplication and reproducibility review. Institutional pages timed out during TLS read: **arXiv complete, cross-source incomplete, watermark unchanged**. No DeepXiv or third-party substitutes.

| Paper | Area / priority | Result |
|---|---|---|
| [HELIX](../reproductions/2609.37183-helix/README-en.md) | Industrial P0 | TikTok e-commerce full-traffic A/B (§3.5 Tables 4–5); three token streams, one-way reusable cache, MPTF |
| [STEPQuant](../foundation-models/2609.38169-stepquant/README-en.md) | Foundation P1 | Author code; temporal lifetime × spatial impact bit allocation and dual-axis scale |
| [LeapQuant](../foundation-models/2609.38166-leapquant/README-en.md) | Foundation P1 | Window quantization, compensation tokens and residual smoothing |
| [Chinese-Jev](../foundation-models/2609.36965-chinese-jev/README-en.md) | System One P1 | Chinese candidate marker head and CE/RLCD |
| [Dr. OPD](../post-training/2609.38025-dr-opd/README-en.md) | Post-training P1 | Author code; dual-level question token credit and weighted OPD |
| [SIPO](../post-training/2609.36742-sipo/README-en.md) | Post-training P1 | Author code; dual-context contrastive teacher and token advantage |
| [ReMem](../agent-research/2609.37311-remem/README-en.md) | Agent P1 | Author code; temporal memory and Multi-Memory GRPO |
| [Video-RSI](../agent-research/2609.37950-video-rsi/README-en.md) | Agent/RSI P1 | Author code; accuracy–visual cost Pareto gate |

[PR #180](https://github.com/daiwk/auto-research/pull/180) already implemented ROFT, LSPD, Harness Learning, MS-GLA and GraphHCA; update ledger/roadmap only. RECAP (2609.37905), Google Research, lacks quantified A/B or accepted full traffic and fails the industrial gate. SelfSearch (2609.37968) is deferred for real search, reward-free trajectory filtering and equal-budget agent comparisons. VACE (2609.37105) is deferred for editable multi-tool agents, execution feedback and fair intergenerational cost. Next overlap at least three days and retry Google/Meta/DeepMind; don't call the historical pool new papers or advance before auditable states.
