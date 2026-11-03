# October 26, 2026: New announcement and Google-priority backfill

<!-- source-sha256: 664b68be035be0a1105fda278bba55f316446a1cae7cf97144895949e2b7f695 -->

[简体中文](../../../research-audits/oct26-components/README.md)

This batch delivers **eight low-cost L1 components and eight references**. All eight components ran from one frozen revision on CPU and a real **NVIDIA A100** with seeds 42/43/44. Full large-model, private-log, API, and multi-GPU experiments are **too costly, not reproduced (review DONE)** and not automatically retried.

## What was actually new

All eight official arXiv pages changed to the **October 26 announcement**: 1,180 category entries, 835 identities, with 446 new, 289 cross-list, and 445 replacement records. Versus the prior snapshot, 802 identities and 832 version strings were added. **These are not new-paper counts or 835 full-text reviews.** Cross-listing, revisions, and weekend submissions are not 1,180 first publications.

Most selected announcement v1s were submitted October 22–23 and all predated the end of the October 25 capture. Therefore zero selected entries were first published after that capture. Keep announcement and first-publication counts separate.

Official priority catalogs returned Google 29/29 pages, Meta 6/6, and DeepMind 9/9. Google's 430 versus 428 records added two URLs: **2025 Watch and Learn** and **April 2026 PaperOrchestra**, both historical backfills. Meta 144 and DeepMind 265 had no bounded additions, not proof that the organizations or web had none. DetectorScope was a recent official-code discovery; repository creation and historical commit times are separate.

[Source coverage](../../../research-audits/oct26-components/source-coverage.json) contains counts, IDs, times, and hashes. [Fixed scope](../../../research-audits/oct26-components/task-scope.json) contains delivery and dates. This bounded delivery does not exhaust a period or the web; **the global watermark remains 2026-10-15**.

## Low-cost components

| Priority | Paper / institution | Actual coverage | Limits |
| --- | --- | --- | --- |
| P0 | [DetectorScope, Google DeepMind collaboration](../../../foundation-models/2610.30006-detector-scope/README-en.md) | SAE-feature max pool, description-verification masks, training RMS, proximal sparse head, and exact logit attribution | No SAE/LLM training, description generation, or text detection capability claims |
| P0 | [OPST, Google](../../../post-training/2610.32770-opst/README-en.md) | External verification-observation gate, equal-response aggregation, and EMA | PDF divergence weights are ambiguous; no canonical JSD or silent formula rewrite |
| P1 | [HGE, Meituan](../../../recommendation-components/2610.32420-hge/README-en.md) | HSAE, PLL, and signed residual/per-example gated fusion | No DIN/DCN, full Dice tower, or 712M private logs; online +1.42% is the authors' result |
| P1 | [Frontier-OPD, Tsinghua](../../../agent-research/2610.32802-frontier-opd/README-en.md) | Signed disagreement, trajectory-balanced node ranking, and measured same-length bridge admission | Environment, teacher, real replay, and distillation are external; admission is not task success |
| P1 | [MART-GRPO, University of Hong Kong](../../../post-training/2610.32431-mart-grpo/README-en.md) | External event boundaries, pre-failure prefix mask, and clipped PG with original denominator | No event VLM/VLA training or proof of ideal martingale unbiasedness |
| P1 | [DT-JEPA, Southeast University](../../../foundation-models/2610.32657-dt-jepa/README-en.md) | Gaussian future targets, reparameterization, AdaLN, BC, and double-critic multistep targets | Caller provides modules; no replacement for real DT, D4RL, or an environment |
| P1 | [EditJev, Peking University](../../../foundation-models/2610.32635-editjev/README-en.md) | Offline preference loss, non-padding hidden head, and quality/speed routing | No image generation, test quality input, Qwen, or candidate editors |
| P1 | [UniAction, Stanford](../../../multimodal-models/2610.32977-uniaction/README-en.md) | Shared semantic codebook, native positional callback, and cardinality-calibrated joint attention | No substitute RoPE, video world model, or custom-kernel speedup claim |

[Execution spec](../../../research-audits/oct26-components/execution-spec.json) fixes thresholds and negative controls. [Raw CPU](../../../research-audits/oct26-components/raw-cpu.json), [raw A100](../../../research-audits/oct26-components/raw-cuda.json), and [portable Git proof](../../../research-audits/oct26-components/frozen-sources.json) bind snapshot `fae525e8939a003d97452bef78b283389c718376`. Individual metrics and receipts are on paper pages, not pooled into fictitious common accuracy.

## High-cost references: reviewed and not reproduced

| Priority | Paper | Why full experiments were not run |
| --- | --- | --- |
| P0 | [FlexGlue, Google collaboration](../../../multimodal-models/2610.32976-flexglue/README-en.md) | DINOv3 plus nine-layer matcher, multiple H200s and days; softmax is not entmax/Fenchel–Young |
| P0 | [Watch and Learn, Google collaboration](../../../agent-research/2510.04673-watch-and-learn/README-en.md) | 8×A100 IDM training, 53K video trajectories, 7B computer agent, and real desktops |
| P0 | [PaperOrchestra, Google](../../../agent-research/2604.05018-paperorchestra/README-en.md) | Multi-agent writing, web retrieval, figures, extensive API/human evaluation; community skills are not author implementations |
| P1 | [LazyFlash](../../../foundation-models/2610.31911-lazyflash/README-en.md) | 8×H200, 65K context, 2,500 steps, custom backward kernel; ordinary masks do not establish speedup |
| P1 | [PathJev](../../../foundation-models/2610.32478-pathjev/README-en.md) | Pathology data, specialized models, long multi-seed training, and generative controls |
| P1 | [ImageRSI](../../../agent-research/2610.32120-image-rsi/README-en.md) | Full loop of real generation, external multidimensional judging/repair, and judge training |
| P1 | [RSI-Opt](../../../agent-research/2610.32026-rsi-opt/README-en.md) | API coding agent repeatedly edits and trains optimizers across tasks/seeds; holdout lineage contamination concern retained |
| P1 | [HarnessMM](../../../agent-research/2610.32813-harnessmm/README-en.md) | Native harness, real callback certificates and billing, multiple API benchmarks; no fabricated receipt |

None has a runnable operator, metrics, or GPU pass claim. Cost review does not implement experiments or leave a hidden retry queue.

## Verification and sources

```bash
PYTHONPATH=src python scripts/curate_oct26_components.py --check
python -m pytest tests/test_oct26_component_evidence.py \
  tests/test_oct26_foundation_components.py tests/test_detector_scope.py \
  tests/post_training/test_oct26_post_agent_components.py tests/reproductions/test_hge.py
```

The GPU package carried only this batch's public source and frozen proof, not models, data, credentials, or the workspace. The initial isolated export failed because the existing JEV parent package eagerly imported an omitted benchmark dependency; it emitted no passing receipt. The verifier was changed to frozen-file loading, checked separately from normal package imports. Final CPU/A100 results use one corrected snapshot, not the partial first run.

Temporary local sites and source archives and this round's remote temporary directory were cleaned after acceptance. Source, raw results, failure notes, and sanitized receipts were retained.
