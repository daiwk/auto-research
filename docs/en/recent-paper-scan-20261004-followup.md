# Seven backfilled papers from the October 2 announcements: 2026-10-04

<!-- source-sha256: 4c15d7b3142089e62684b2f48bef353b52af95989cda10ccd6eab6f9a4e6c888 -->

[简体中文](../recent-paper-scan-20261004-followup.md)

Three user-approved P0 and four P1 items from the October 2 announced window, not seven papers published within hours. Official arXiv full text and author links, no DeepXiv. No new full scan or complete Google/Meta rerun; coverage_complete=false, watermark **2026-10-02**, overlap from **2026-10-01**.

| Priority | Method | Executable part | Boundary |
|---|---|---|---|
| P0 | [Jev lookahead](../agent-research/2610.01834-jev-lookahead/README-en.md) | Cloned simulator, newly available actions, System One provider | Diagnostic provider, not ALFWorld success |
| P0 | [T2SPO](../post-training/2610.00388-t2spo/README-en.md) | Real TabPFN, support standardization/SVD, credit and clipping | Official CPU checkpoint, synthetic states |
| P0 | [Weakest-Link](../post-training/2610.00332-weakest-link/README-en.md) | All prefixes, absorbing penalty, immediate full-vocabulary gradient | Real small-policy update, not LLM distillation |
| P1 | [CMP](../agent-research/2610.02070-causal-memory-policy/README-en.md) | Randomized retrieval exposure, Hájek and risk decisions | Intervention measurement, not long-run deletion |
| P1 | [TESS](../foundation-models/2610.02092-tess/README-en.md) | Sequential two-model training, PVM selector and independent pool scoring | Synthetic classifiers, not LM lift |
| P1 | [RLCPR](../post-training/2610.01458-rlcpr/README-en.md) | Entropy buckets and concentrated-posterior length penalty | Formula/gradient checks |
| P1 | [Mingbird](../agent-research/2610.02001-mingbird/README-en.md) | Portable M1/M3/M4/M5 and real tool acceptance loop | Scripted policy, not agent accuracy |

Callable L1 APIs are not end-to-end reproduce adapters or registry-only Evolve integrations.

```bash
PYTHONPATH=src python scripts/run_oct04_seven_papers.py
python -m pytest tests/test_oct04_seven_papers.py
```

T2SPO pins tabpfn==2.2.1 in a separate environment; see its page for checkpoint revision. Three-seed MAEs 0.00290, 0.00138 and 0.00234 on synthetic learnable remaining distance are not real environment prediction or the paper's encoder/RL. Weakest-Link mean expensive-action probability 0.3546→0.01036; TESS PVM 0.0803→0.0129; CMP 100 exposures per memory. All diagnostic_only=true regardless of seeds.

Full benchmarks, LLM/hosted Jev, cross-task memory utility and large training remain on the [roadmap](../research-roadmap.md). No new CUDA claim/A100/A30 verification. CMRec Amazon-M2 and other earlier boundaries remain.
