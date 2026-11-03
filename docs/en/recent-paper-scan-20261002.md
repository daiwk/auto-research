# P0/P1 scan and implementation closeout: 2026-10-02

<!-- source-sha256: a1c6bb382d05564efced28d6737d10afb806c472c79ffeaec7df7d76bd5a4dc9 -->

[简体中文](../recent-paper-scan-20261002.md)

September 30–October 2, plus Google's May 15 enterprise-LLM full-text backfill. Official arXiv abstracts/HTML/PDF, Google Research and author repositories/project pages; no DeepXiv. Deduplicate arXiv IDs, titles, adapter keys and ledger. Google/Meta first; industrial full-text deployment/experiments required. **17 implementations: 7 P0 and 10 P1**, each with detail page, original figure, mechanism, three-seed L1 and boundaries.

| Priority | Paper | Area | Admission and local mechanism |
|---|---|---|---|
| P0 | Gemini for Google | Foundation | Blind A/B with 29,000 developers; enterprise and general replay mixture |
| P0 | GEAR | Industrial | Douyin seven-day A/B at 5% per arm; BasisVQ and collision reranking |
| P0 | DARS | Post-training | Dependency rewards: invalidation, repairs and potential differences |
| P0 | ActiveSaddler | Agent | Active harness curriculum: dynamic failure arms and exploration/exploitation |
| P0 | Safety Must Survive Self-Improvement | Agent/RSI | Current-state validation and founder rollback |
| P0 | Range-GRPO | Post-training | Pairwise interval-relative advantages |
| P0 | VeriHarness | Agent | Evidence support, conflict and consensus challenge for long tasks |
| P1 | Effective Training Time | Industrial infrastructure | Approved deployment exception, not recommendation A/B; ETT decomposition and loss attribution |
| P1 | TACO | Foundation | Sparse column direction and low-precision state; CUDA receipt required |
| P1 | VETO | Multimodal foundation | Spatial then temporal compression; CUDA receipt required |
| P1 | Mem++ | Agent | Organizational memory with nondestructive write, as-of and hybrid search |
| P1 | DeFA | Agent | Backpropagate dependencies and find decisive error |
| P1 | My FAULT | Post-training | Verified self-diagnosis and conserved terminal credit |
| P1 | FloWright | Agent/RSI | Workflow evolution with topology-aware hierarchical credit |
| P1 | Where-OPD | Multimodal post-training | On-policy KL over spatial masks |
| P1 | GrIS | Generative recommendation | Approved academic/Evolve exception, no A/B; graph-guided hierarchical SIDs |
| P1 | REPAIR | Personalization | Approved academic/Evolve exception, no A/B; preference-state repair on frozen cache |

GEAR/Gemini online results are author evidence only. ETT/GrIS/REPAIR are named exceptions excluded from industrial lift conclusions. DARS repo said code was in preparation; repo existence is not release. TACO/VETO completion requires accepted real CUDA receipts on A100/A30. Next overlap at least two days from October 1.
