# 2026-10-10 paper batch: complete scope of one PR

<!-- source-sha256: b050e451793df9674032204227ebc7aea3c5b5aab254b5cf25ccca94a56f2817 -->

[简体中文](../../design/oct10-paper-batch.md)

This records the accepted scope. Completion means implementation, relevant verification, and documentation; a registry entry or formula unit test is not sufficient.

| Priority | Paper | arXiv | Acceptance focus | Status |
| --- | --- | --- | --- | --- |
| P0 | DIAL-OPD | 2610.11659 | Real student rollout, teacher scoring, and sparse token updates | Core and short A100 checkpoint training completed |
| P0 | MetaOPD | 2610.11989 | Differentiable virtual AdamW, training reference stream, meta-gradients, and actual student updates | Core and short A100 checkpoint training completed, including zero-gradient stability regression |
| P0 | MASS | 2610.12176 | Same-model workflow optimization, evaluation and SFT internalization; isolated external test across rounds | Two real LM workflow/SFT rounds; A100 rerun passed after repairing role coverage |
| P0 | RACE | 2610.12061 | Likelihood-constrained compression of every downstream action; closed SFT/RL loop | Actual LM tool trajectories, compression, and on-policy updates completed |
| P1 | GRPODropout | 2610.11854 | Group filtering, negative advantage restoration, probability-weighted centering, and actual GRPO updates | Actual rollouts for two seeds; retain both updates and post-filter zero-gradient results |
| P1 | Residual Advantage / Co-RA | 2610.11519 | Full-vocabulary residuals, response centering, same-batch teacher LoRA, and next-round scoring | Both RA and Co-RA performed actual A100 updates |
| P1 | Semi-OPD | 2610.11291 | Initial student cache, one teacher scoring pass, and refreshed student advantages | Core and short A100 checkpoint training completed |
| P1 | Elastic Expert Routing | 2610.11575 | Training with fixed expected budget and inference with fixed actual budget | Real sparse LM controls on A30, three seeds; small negative result retained |
| P1 | ViMoD | 2610.12060 | Recoverable coarse/fine DART groups and dynamic fine TRACE evidence | DART/Joint-KV used a real checkpoint; three-stage TRACE was only a CUDA gradient diagnostic with auxiliary fixtures |
| P1 | Hippocam | 2610.12124 | Hierarchical intent, protected tail, abstract-to-detail retrieval, and reconsolidation | Actual LM and controlled archive diagnostics ran; autonomous execution did not trigger archival |
| P1 | EvoAlloc | 2610.12086 | Full/Partial/Discard, counterfactual audit, shadow-policy controls | Actual LM and sandbox evaluation; A100 rerun after evidence-isolation fix passed, without improved effectiveness |
| P1 | JEV capability benchmark | 2610.11978 | 13 tasks, language groups, missing coverage, and separate cited and measured results | All 13 interfaces/contracts completed; NanoJev ran all 1,172 ARC questions, not the other 12 tasks |

## Shared acceptance criteria

- Standalone Chinese paper pages with complete metadata, original mechanism, equations/architecture, original results, local results, and boundaries.
- Runnable entry points and real inputs. Diagnostics are not official benchmarks or capability gains.
- Run new CUDA paths on A100/A30 and commit sanitized, verifiable receipts.
- Regenerate indexes, check docs, run behavioral tests and all quality gates.
- Verify scope, checks, and unfinished items before handing off the single PR.

This batch does not itself advance the complete review watermark. Unverified candidates stay in the review queue.

## Explicitly not claimed

This batch covers core mechanisms and runnable paths, not original-scale benchmark replication for all twelve papers. Short training does not demonstrate improvement, and these diagnostics are not Evolve promotion evidence. Agent experiments use bounded tool/workflow environments, not official coding tasks. ViMoD's official teacher annotations, original checkpoint, and full evaluation remain unverified. JEV's closed paper results and local NanoJev measurements remain separate.

## Audit of label and counter paths

New fidelity inventory entries were reviewed by role. Post-training answers are used only by external verifiers, training reference losses, and post-training validation scoring, never in student rollout prompts. The JEV loader retains references; provider requests contain only the problem and options, and the evaluator compares predictions with references. Hippocam serials, EvoAlloc proposal counts, and ViMoD causal positions are runtime state, not standalone capability evidence. Behavior tests cover label-free requests, real tool execution, protection of incomplete rounds, mutually exclusive historical experience, and role training coverage.
