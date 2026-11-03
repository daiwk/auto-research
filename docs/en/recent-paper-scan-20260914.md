# Recent paper scan: 2026-09-14

<!-- source-sha256: 18e516899d443f890f5a89d052d172c7741150cabd3c036d59015f0534370a14 -->

[简体中文](../recent-paper-scan-20260914.md)

## Coverage

September 9–11, 2026 revisits the interval previously limited by the API. Tracks: industrial search/ads/recommendation and risk, foundations/Evolve, post-training and agents. Sources include official arXiv recent/HTML/PDF, Google Research publications/blog and author repositories. Google/Meta priority and full-text industrial evidence remain. This is a verified public batch, not an exhaustive claim based on no weekend submissions September 12–14. Keep overlap from September 11.

| Priority | Track | Paper | Key | Mechanism or boundary |
|---|---|---|---|---|
| P0 | Industrial risk | SIRF (2609.11752) | sirf | Rule interaction internalization and P95 threshold; not 8B CPT |
| P0 | Post-training | NSD (2609.11699) | nsd | Negative teacher and reasoning gate, candidate-policy diagnostic |
| P0 | Agent | COBRA-Skills (2609.11682) | cobra-skills | Contextual UCB skill budget and feedback admission |
| P0 | Agent | Ecdysis (2609.11677) | ecdysis | Cross-instance failure clustering and FDCR triggers |
| P0 | Agent | Grounding Agent Memory (2609.11060) | grounded-memory | Read-only probes, conflict rejection and memory gate |
| P0 | Foundation | OmniKVQuant (2609.11582) | omnikvquant | 2-bit windowed key quantization and modality-specific value rotation |
| P0 | Agent | ToolGrad (2508.04086) | toolgrad | Backfilled Google answer-first textual gradients |
| P0 | Agent/systems | PROMPTS (MLSys 2026) | prompts | Profiler evidence ranking and constrained sharding proposals |
| P1 | Multimodal foundation | SenseNova-U1.5 (2609.11929) | sensenova-u1-5 | Spatial patch targets and multi-expert OPD reference |
| P1 | Multimodal foundation | Caption-once, Frames-on-Demand (2609.11899) | frames-on-demand | Visual-need gate and frame budgets |
| P1 | Foundation | Data Scarcity and Model Sparsity (2609.11917) | repeat-aware-moe | Repeat/sparsity-aware regularization |
| P1 | Post-training | Unified Per-Token OPD Gate (2609.11768) | adaptive-opd-gate | Four-signal token-level FKL/RKL gate |
| P1 | Post-training | LOCUS (2609.11739) | locus | Task-aware SVD low-rank update space |
| P1 | Foundation | Musec (2609.11655) | musec | Smooth spectral clipping of Muon momentum |
| P1 | Foundation | SWRouter (2609.11414) | swrouter | Similarity shrinking windows and routing |
| P1 | Post-training | TASCO (2609.11393) | tasco | Neighborhood perturbation stability for test-time adaptation |
| P1 | Agent | SearchAtlas (2609.10901) | searchatlas | Query–evidence–answer graph audit |
| P1 | Agent | When Synthetic Data Hurts (2609.10750) | skill-retention | Real-data replay and anti-forgetting anchors |
| P1 | Agent | T1 (2609.11042) | t1-terminal-rl | Exact-token and MoE route replay diagnostics |

All entries have detail pages, metadata, original figures, three-seed mechanism artifacts and explicit boundaries. Post-training/agent Evolve tests require mutations to change actual execution/intermediates; a registry name is insufficient. OmniKVQuant is a NumPy reference, not a completed Triton/CUDA path or GPU receipt.
