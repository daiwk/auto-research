# 2026-10-12: 16 implementations and fixed-window review closeout

<!-- source-sha256: 4809e171110543cc999fede1afbf2ac35052600280defb3c63ab4f8993bd8d4e -->

[简体中文](../../design/oct12-papers-and-review.md)

The user accepted all previous P0/P1 candidates and two October 8 omissions in one MR. In parallel, close four tracks, two discovery channels, and Google/Meta source review before advancing October 7 to October 12. Implementing the short list cannot substitute for reviewing the complete candidate pool.

Discovery froze at 2026-10-12T12:55:18+08:00 for October 8–12, with preceding announcement overlap and identifier-month catch-up. Coverage refers to actual sources at that time, not the end of the day or the whole web.

| Priority | Paper/facility | arXiv | Scope | Actual status |
|---|---|---|---|---|
| P0 | Evo² | 2610.13025 | Agent/RSI | Implemented; [A100](../../gpu-validations/oct12-evo2-a100.json) SFT and four real GRPO updates; eight GSM search diagnostics; circle failures retained |
| P0 | FORTE | 2610.13806 | Industrial recommendation | Implemented; [three A100 seeds](../../gpu-validations/oct12-forte-a100.json) all retained baseline and did not select offline features |
| P0 | RSI-Anything | 2610.13912 | Agent/RSI | Implemented; [A100](../../gpu-validations/oct12-rsi-anything-a100.json) predictor updates and pair gate; zero circle gain |
| P0 | BranchOPD | 2610.13481 | Post-training | Implemented; [A100](../../gpu-validations/branch-opd-a100-20261012.json) 12 branches, eight PBR constraints, actual updates |
| P0 | CAST OPD | 2610.13257 | Post-training | Implemented; [A100](../../gpu-validations/cast-opd-a100-20261012.json) cross-tokenizer alignment on 512 tokens; separate `cast-opd` namespace |
| P1 | Road MOPD | 2610.13521 | Post-training | Implemented; [A100](../../gpu-validations/road-mopd-a100-20261012.json) conflicts/projections across 39 tensors; arithmetic subdomains, not original expert teachers |
| P1 | MSAR | 2610.13630 | Foundation model | Implemented; [three A100 seeds](../../gpu-validations/oct12-msar-a100.json) actual byte-model training; unmatched parameters preclude formal gains |
| P1 | Orthros | 2610.13735 | Foundation model | Implemented; [three A100 seeds](../../gpu-validations/oct12-orthros-a100.json) training/KV equivalence; negative NLL retained |
| P1 | DualQuant | 2610.13767 | Foundation model | Implemented; [A100](../../gpu-validations/oct12-dualquant-a100.json) all linear layers of public 135M weights; software quantization, not native FP4 acceleration |
| P1 | BoundaryEvo | 2610.13285 | Post-training | Implemented; [A100](../../gpu-validations/boundary-evo-a100-20261012.json) one actual stage-two update under original gates; second round skipped without eligible teacher traces; prior failures retained |
| P1 | JANUS | 2610.13194 | Agent/RSI | Implemented; [A100](../../gpu-validations/oct12-janus-a100.json) real SDPA search, execution, and skill evolution; negative execution and old eager OOM retained |
| P1 | T2Mem | 2610.13348 | Agent | Implemented; [A100](../../gpu-validations/oct12-t2mem-a100.json) all 98 sessions for two official queries; external token F1 zero |
| P1 | RATED | 2610.13889 | Agent tool retrieval | Implemented; [A100](../../gpu-validations/oct12-rated-a100.json) dual-encoder training and feedback bandit; original API missing, execution failures retained |
| P1 facility | Jev Agent workflow evaluation | 2610.13092 | Jev/Agent | Implemented; [three A100 seeds](../../gpu-validations/oct12-jev-workflow-measurement-a100.json) actual checkpoint generation, cost accounting, and sandbox; not JeV weight reproduction |
| Omission | WOVEN | 2610.12417 | Multimodal | Implemented; [A100](../../gpu-validations/oct12-woven-a100.json) original images and transition training; negative test retained |
| Omission | Unsupervised Multimodal Reward Modeling | 2610.12707 | Multimodal/reward | Implemented; [A100](../../gpu-validations/oct12-umrm-a100.json) frozen VLM probe, verifier bootstrapping/retraining; no best-of-N gains measured |

ECC 2610.13066 and Google's user simulator 2610.13617 need source material and are outside the 16 implementation commitments, but must receive explicit defer/exclude/accept decisions. Record final decisions for other recalled candidates too.

## Required checks

- Preserve defining models, objectives, policies, and actual paths. Fixed candidates or fixture scores are not capability evidence.
- Chinese paper pages include complete metadata, methods, equations, architecture, original figures and results, runnable entry, and local scope.
- Separate L0/L1/L2 from paper capability gains; retain negatives, truncation, failures, and no-op updates.
- Run CUDA paths on real A100/A30 with pinned public checkpoints/data and source commits, committing sanitized receipts only.
- Controllers cannot read gold and test cannot select. Evolve integration requires actual execution and reevaluation.
- Leave the dirty original checkout and `uv.lock` untouched, and deliver one reviewable MR without merge/deploy.
- Move the watermark only after both channels across four tracks, candidate review, official Google/Meta sources, and nonblocking exceptions pass coverage audit.

## Resume point

Branch `codex/oct12-papers-and-review` builds on `origin/main` including merged PR #199. Sixteen bounded implementations and actual GPU runs are complete, not sixteen full capability reproductions. Closed source review advanced the watermark to October 12. Other reviewed candidates remain independently tracked.

## Label and counter audit

`fidelity-source-inventory.json` indexes review, not capability evidence.

| Path | Allowed use | Prohibited use and checks |
|---|---|---|
| `GSMHarnessEvaluator` | Official train-only validation answers in external numeric scorer; executor gets question and generated PROMPT | Evolution receives question/output SHA and correctness, not answers or raw executor text; `test_oct12_agent_gsm_harness.py` checks isolation and splits |
| T2Mem entry | `memory.answer` is generation; query answer is used after generation for external token F1 | Do not pass labels into memory or generation; this is not paper LLM-judge accuracy |
| WOVEN/COCO loaders | WOVEN correct letter after rotation for training and post-output scoring; COCO captions for train/validation | `woven_prompt` receives question, choices, image only; split by public source group before training/layer selection; no test selection |
| BoundaryEvo | External analyzer can see train answers; fresh teacher outputs enter SFT only after external `verified_reward` checks | Generators see no reference, no fabricated value on invalid analysis, and no stage two without passing; covered by `test_oct12_post_training.py` |
| Harness execution counters | `calls` counts attempts, alongside actual sandbox, frozen-weight digest, and output hashes | Counts do not establish execution, gradients, or updates. Momentum drift with zero advantage is not GRPO learning. |

These are bounded L1 runs, not original capabilities automatically upgraded by seed count, receipts, or syntax audits.

## Final local acceptance

- `python -m pytest -q`: 1,857 passed, exit 0. Boundary was not excluded and assertions were not weakened.
- Sixteen real GPU receipts validated; 93 execution-source SHA256 values match actual commits, not retrospectively filled from final HEAD.
- `compileall`, Ruff, paper specs, fidelity inventory, minimal base-wheel install, and CLI manifest passed; registry has 387 adapters.
- Schema-v2 metrics audited for 739 artifacts; platform completeness, strict paper coverage, and implementation reconciliation passed. This does not mean formal capability comparisons are complete.
- Manifest/catalog and 696 public dashboard entries regenerated without diff; `mkdocs build --strict` passed.
- Caches, checkpoints, raw model outputs, machine connections, and `uv.lock` excluded. Local checks are not remote CI; use actual final PR checks.
