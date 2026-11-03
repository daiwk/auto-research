# October 17: Twelve affordable components and the Meta/AMD systems report

<!-- source-sha256: f16139c752c35d97fcaa7f971c30e79c79f960e89327d7e1d659bdf73573260b -->

[简体中文](../../../research-audits/oct17-components/README.md)

One MR covers twelve independent components. **All full experiments are too expensive and not reproduced (review DONE)**. Component checks are not capability, pretraining gains, robot success, or serving throughput. No large model downloads, long rollouts, full model/dataset matrices, or automatic evolve integration.

## Scope and cost basis

| Domain | Paper / key | Implemented | Why full reproduction is excluded |
|---|---|---|---|
| Foundation | [DropKV](https://arxiv.org/abs/2610.22130) / `drop-kv` | Attention output perturbation scores, GQA, and KV selection | 7B/8B, multiple models and KV budgets, full 4K–128K evaluation |
| Foundation | [MirrorMoE](https://arxiv.org/abs/2610.22353) / `mirror-moe` | Mirrored expert choice, forward probability aggregation, annealing | 2–4 H100s, 4.4B–12.8B tokens, multi-model pretraining |
| Foundation | [BitSparse](https://arxiv.org/abs/2610.22256) / `bit-sparse` | Lossless bitmask/value storage, restoration, and backward | About seven hours per arm extrapolated from RTX3090 step time, not measured A100 time |
| Foundation | [LCT](https://arxiv.org/abs/2610.22179) / `lct` | Bounded BF16-exponent Huffman, sign/mantissa, overflow, reconstruction | About 8.5 hours per arm extrapolated from RTX3090 steps; full fused optimizer/kernel throughput not reproduced |
| Foundation | [RoleQ](https://arxiv.org/abs/2610.21808) / `roleq` | Role axes, exact ternary fitting, resident-bit accounting | Paper 8B uses 3–4 A100 hours, two-plane phase under ten hours |
| Post-training | [SRD](https://arxiv.org/abs/2610.22080) / `shared-residual-distillation` | Peer/control residuals, minmod targets, clipped loss | 1.7/4/8B, 100 steps, multiple frozen teachers and 20K/32K lengths |
| Post-training | [PRM4RL](https://arxiv.org/abs/2610.22056) / `progress-reward` | Progress state machine, potential rewards, subtask representation | Four RTX3090s, five seeds, paper simulator training 1–10 hours per task. NeurIPS 2025 backfill |
| Post-training | [EliteReplay](https://arxiv.org/abs/2610.22290) / `elite-replay` | Quality-diversity archive, replacement/sampling, mixed GRPO/replay | Four A100-80GB GPUs, full-parameter 4B, long rollouts and 128 evaluations per question |
| Post-training | [CleanRM](https://arxiv.org/abs/2610.21138) / `clean-rm` | Joint OT noise-rate estimate and corrected loss | Two-stage 8–70B reward models, multiple training arms, external judge |
| Agent | [Shortcut Sensitivity](https://arxiv.org/abs/2610.22243) / `shortcut-sensitivity` | Offline LODO and interaction-weighted audit | No all-guard/model rerun. Diagnostic labels are not evaluated-agent inputs |
| Agent | [Disagreement Routing](https://arxiv.org/abs/2610.22245) / `disagreement-routing` | Corrected disagreement, gold-free target, validation budget calibration | 8B, multiple samples/models, long BFCL/WebShop rollouts |
| Agent | [TRACER](https://arxiv.org/abs/2610.21267) / `tracer` | Trajectory trie, experience/semantic priors, learned blend | Six environments × four models × five folds × multiple budgets; upstream artifacts unreleased |
| Research material | [Meta/AMD Hardware Diversity](https://arxiv.org/abs/2610.22230) / `hardware-diversity` | Metadata, method, original figure, and production training evidence; no algorithm entry point | 8–128 MI350X/B200 GPUs and private jobs cannot be matched on one NVIDIA GPU |

Costs reflect published configurations, not current measurements. BitSparse and LCT hours are extrapolated from step times and counts. Meta/AMD production training is not a user-facing A/B result.

## Verification contract

- Formulas and structures require independent references, boundary/failure inputs, real negative controls, and gradients or bitwise roundtrips, not shapes alone.
- Training/calibration read only their splits. Gold goes to an independent scorer, not routing or agents. Synthetic fixtures are not public capability benchmarks.
- Freeze source before a bounded single-A100/A30 run. Receipts bind algorithm/runner SHA-256, seed, device, command, data, and initialization. Do not claim CUDA acceptance until verified.
- Each paper keeps metrics JSON with `diagnostic_only: true`, `promotion_eligible: false`, `evolve_integrated: false`. No automatic full-experiment reruns.

## Status

Twelve components implemented. Meta/AMD is research material only, not a fabricated algorithm or performance entry point.

- **Nine CUDA components:** Frozen `2b9c5f4dc5757c14692654f700d2c40d90ffbfa1` ran on one NVIDIA A100-SXM4-80GB with seeds 42/43/44. Foundation about 2.03 seconds and post-training about 2.18 seconds, bounded operators/small networks only. Detail pages retain per-paper metrics and source-bound commands/inputs.
- **Three CPU agent components:** Official-record audit, independent training probe, or trajectory retrieval on the same frozen source. Shortcut audits original records once; three seeds vary grouped CV splits, not three independent trainings. Disagreement Routing and TRACER are synthetic diagnostics.
- **Numerical and failure limits:** Cross-review added rejection of nonfinite BitSparse inputs, RoleQ support invariance at extreme scales, and rejection of out-of-range EliteReplay importance ratios, then re-froze and reran A100. Evidence import rejects failed/partial runs rather than treating the last snapshot as success.
- **Negative results:** LCT full-exponent stress encodes 1,979 bytes versus 1,024 dense BF16. Small-matrix RoleQ including scale overhead uses about 7.48 bits/weight, not ideal 1.59. Router budgets calibrate on validation; test call rates can drift, not a hard quota.

Tests cover formulas, gradients, archives, noise learning, bitwise reconstruction, calibration isolation, and invalid inputs. No native FP8/Triton fusion, full LLM/robot training, production serving, or complete benchmark; no implicit rerun queue.

The source inventory adds only the `EliteArchive.sample_balanced` rotating cursor for per-question balance, not optimizer steps or success. Shortcut training-fold labels are explicitly table diagnostics; held-out labels do not reach predictors. TRACER target tools are for training and scoring only, not retrieval inputs or gold plans.

FDE-Gym and other high-cost candidates were outside the twelve-item scope. All results are ineligible for promotion and not connected to evolve.

About 350 MB of temporary build files, duplicate PDFs, and visual montages were removed. Metrics, receipts, original runs, and pinned small public audit caches were preserved. Unrelated files untouched.

## Delivery checks

Local full pytest: **3669 passed, 1 skipped**. Compileall, Ruff, minimal-install, source-role inventory, paper specs, discovery reconciliation, idempotent schema check for 857 metrics, platform completion, GPU evidence, and strict MkDocs passed. Manifest/catalog/dashboard and batch ledger regenerated without changes. CLI still reports 410 executable paper adapters; standalone components do not inflate that count. See the PR for remote checks.

## Date and watermark

Most came from October 15 releases surfaced in October 16 announcements. PRM4RL is a 2025 work newly on arXiv, not a 2026 research result. This is not all-source review closure and **does not advance the full review watermark**.
