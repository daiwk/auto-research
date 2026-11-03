# 2026-10-13 GPU verification closeout and remaining work

<!-- source-sha256: 67cea9aa6ea0b7cb38b5bc42a2d98c710b556d93300592d13da767c71faeb344 -->

[简体中文](../../research-audits/oct13-gpu-todo.md)

On October 13 the user paused A100/A30 connections, transfers, and new runs while networking was unstable. On October 14 the user explicitly resumed access. Read-only SSH checks on both accelerator types passed and existing run directories remained. Verify source and resource SHA before resuming; reconnecting is not acceptance. Do not erase failures, weaken GPU gates, or claim all 19 accepted.

Source checkpoint: `ccad3e679787f6f5383b8bd3dd1c7b58e7c8c5d0`. Later documentation/tool closure follows the branch. See [local closeout](oct13-local-closeout.md) for checks, repaired failures, and final limits. Resume source bundles bind `4496283a`, `34148c2e`, and `6aabe57a` per experiment. Skill, robot, and MBS fixes snapshot `0f5dca9f7f0319c6e3bb57aa578cfe26499a6e7e`. Bundles contain public source and scripts only, no workspace caches, private data, or credentials. Never overwrite old run directories; commit a new snapshot before running fixes.

## Verified actual results

| Paper | Verified | Outside scope |
|---|---|---|
| UxSID | A100, 42/43/44, 943 users, four real architectures, cache equivalence | Production lift and full XLong/KuaiRec; no stable local gain |
| State-OPD | A100 `6aabe57a`; state/full-history-opd/state-no-expansion each 42/43/44. Two updates in each of nine runs; 52 sources and raw result hashes independently checked | All three arms have zero before/after accuracy on eight items. Actual response pools and token costs differ; not a formal gain or original environment comparison |
| GPPO / TAPO | Original A100 snapshot, three seeds each plus independent three-seed GRPO control; 3 rollout groups × 2 inner updates = 6 optimizer updates | Large long-trajectory capability. Eight items are diagnostic |
| DoubleCat / SemiCat | New A30 core, 42/43/44, 40 real steps and 32 NFE | Original TinyGSM/OWT scale; one-hot/DoubleCat collapse retained |
| OAL | A100 42/43/44, actual grouping/calibration and matched OAL/softmax LoRA, verified raw/source hashes | One intermediate layer, three steps, 32-token blocks; seed 44 not better. No full-scale or efficiency result |
| NEAR / Beyond | A30 shared-bank 100 queries at three seeds each and strict bank-disjoint 30-query diagnostic each. Eight raw artifacts and source hashes verified | Nonofficial split of official evaluation examples. Seeds on same data are not replications. Strict protocol has only two test queries; do not pool |
| CV-OPD | A100 CDL and without-CDL each 42/43/44, all six real nonzero updates. 24 outputs/logs/states and pinned source verified | Mean test 4.17% versus 12.5%, paired −8.33 pp. Equal caps but actual token costs differ; not formal capability |
| ReplaySSM | A100 48 steps × 42/43/44. Author kernels at four precisions and independent CUDA GDN/Mamba replay, rejection and refresh | Preserve old compilation failure. Transparent JIT compatibility layer, not native serving. Random inputs do not establish LM quality or HBM gains |

See individual pages for metrics and receipts. Old standard SC evidence does not validate the new DoubleCat core.

LeWAM's `0f5dca9f` three-seed A100 native joint training and three-arm candidate loop had four nonzero updates per seed. All arms 16.67% ± 28.87%; no planning advantage. Goals came from training trajectories, not holdout. SmolWAM `2b84c377` ran actual teacher KD, two-layout curriculum, and new-student loop at three A100 seeds, eight updates and 38 policy queries each. Student and no-op both 0/2. Six raw files, requests, and new weights were independently bound.

SynthSelf and Progressive Contraction ran default 42/43/44 through full core paths; native and three-seed receipts were independently recalculated per field. SynthSelf acquisition mean 0.5 versus gold-SFT 0.6667; retention 0.3333 both. Contraction matches full-SFT seedwise, mean 0.5833. No stable advantage. Exposure ratio is SFT example exposure, not total compute.

UPTURN ran 42/43/44: 42/43 had rescue, 44 had zero rescue reward and advantage; entropy alone updated parameters and the seed remains failed. Keep failed execution cohort and older passing seed-42 receipt, not a three-seed pass or gain.

SOAR `b9086275` A100 42/43/44 × two arms completed. Six raw files independently recomputed into native records and receipt. Method and ablation made 12 and ten actual updates. Ablation seed 43 accuracy zero and equal-reward skips remain. Four validation examples per seed, L1 only, not stable capability or original benchmark.

The corrected A30 difficulty curriculum completed five arms × 42/43/44; all 15 independently recalculated with a [new receipt](../../gpu-validations/grpo-difficulty-curriculum-a30-20261014-seeds42-44.json). 151 real updates and 38 exactly skipped equal-reward groups. Keep staged42 accuracy zero, nonzero too-hard updates, and rejection costs. Old single-seed runs and negative evidence remain separate. L1 only.

Historical three-arm A100 seed 42 at `6aabe57a` received its own mechanism receipt (8/9/11 updates). Independent review found real reward differences in signed groups, not false updates. This is not verification of corrected later source.

A30 `51b4718a` unfiltered/static seed 42 and unfiltered/static/fixed seed 43 ran, but FP32 mean rounding residuals were amplified by standard-deviation normalization. Equal rewards falsely updated 12/32 unfiltered42 and 3/8 static42 groups. Reject the controls without dropping bad groups. The old queue stopped only this run's processes; preserve interruption, no seed 44. Rerun all five arms × three seeds on identical corrected source, device, and budget. Different A100/A30 starting accuracies are not paired controls.

## Remaining verification

**October 14 decision: Defer MagicBeanStalk acceptance and deliver the rest.** Do not expand candidate pool, add seeds, or run more diagnostics automatically. Keep failures and missing receipt. Mandatory cost gate applies: more training has uncertain cost and signal; mark too costly to reproduce now. Old resume notes do not authorize restarting. Separate it from accepted delivery; deferral does not turn missing CUDA evidence into completion.

Pin public checkpoints and data revisions and never overwrite outputs. Default 42/43/44. Adjust budget only from train/validation, not test. Retain failures and zero gradients.

| Priority | Paper | Full path if reopened |
|---|---|---|
| Deferred; do not start | MagicBeanStalk | Too costly for now. Full teacher→Goldilocks→RLVR and controls still await acceptance. Deliver other work first |

MBS's original CUDA spec remains in `src/auto_research/reproductions/magicbeanstalk/deferred-spec.json` with `requires_gpu_validation=True`. Do not fabricate a receipt. Registry does not load it, the old adapter refuses execution, and the public runner excludes it. Preserved source is not CUDA acceptance.

October 14 added OAL, NEAR, Beyond, CV-OPD, ReplaySSM, LeWAM, SmolWAM, SynthSelf, Progressive Contraction, SOAR, corrected five-arm curriculum, and SkillDreamer full three-seed mechanism evidence. UPTURN retains one valid seed and a three-seed record with failure. The GPU evidence gap was MBS only; integration checks remained. State-OPD three-arm receipt is separate from its older snapshot. After MBS deferral there are 18 active implementations; the gate still checks all active CUDA adapters. No MBS or all-19 completion claim.

## Resources and environments

- New public transfer budget ≤20 GB. No private data, credentials, whole workspace, or returned training checkpoints.
- Locally verified pinned Qwen Base, SmolWAM, Wan VAE, LeWAM release/ToolHang, and Cosmos teacher/single-task demo files and hashes. Transfer checkpoints do not verify remote completeness.
- Acquired LIBERO source archive `8f1084e3132a39270c3a13ebe37270a43ece2a01`. Use per-file SHA for archives without .git; do not invent HEAD.
- Two A100 simulator overlays failed pip from inherited non-UTF-8 metadata. Use exact small deps in isolated overlays with `--target/--no-deps/--ignore-installed`. Do not modify shared metadata or reinstall Torch.
- October 14 A30 MiniLM, LongMem text, and raw-only provenance verified bytewise. Eight NEAR/Beyond outputs and receipts saved. Shared Torch unchanged; see [memory resume](oct13-memory-resume-notes.md).
- SkillDreamer `6aabe57a` seed 43 lacked output fields and remains failed. Corrected `0f5dca9f` three seeds ran but zero CSI, actual skill loads, or SkillDreamer tool actions; 48/48 episodes did not complete the core. No passed receipt or old seed42 mixing. Use independent validation probes, not evaluation IDs.
- SmolWAM `2a061dd6` input failure retained. Fix extracts native latent adapter without teacher architecture changes. `2b84c377` three seeds verified. 24 updates and new-candidate controls establish scaled execution only, not gain from zero successes.
- Initial MBS had no normally terminating verified-hard roots. SynthSelf failed Eq.6 and needs consistent gold/rewrite EOS handling. UPTURN boundary misses and zero rescue are distinct. See [independent failure audit](oct14-post-failure-review.md) for failures, costs, and hashes. Parameter movement alone cannot pass.
- SkillDreamer per seed needs actual CSI assessment, gallery loading, and tool execution. Keep failures; three seeds alone do not establish the defining path.
- Independent 7B SkillDreamer probe on eight validation items ran seven PSG/HSR, two CSI/loads, and zero tools. Prompt omitted required format and four decision words. Clarify wording only, freeze new source, and rerun without weakening parser or overwriting failures.
- MBS bounded `0f5dca9f` found three naturally ending hard roots, no qualifying descendants or RL updates. SOAR `57b2314d` 7B train-only probe failed all eight first responses, no retrieval/training. Old probes lack response text; hashes cannot diagnose format. Log raw/rejection stages before retrying without weakening gates.
- Numerical fix keeps GRPO and `std + 1e-6`: CPU FP64 shift then center, exact zeros for equal groups, then cast to policy precision. SOAR trajectory normalization reuses it. No tolerance erases genuine differences, and gates, rewards, and budgets stay fixed. Verify new GPU source.
- MBS `b9086275` took 343.08 seconds, no qualifying descendants. Second subproblem omitted required setup and independent checks rejected it; teacher solved two other roots incorrectly. No relaxing verifier. SOAR same-source train-only probe took 35.97 seconds, three valid traces and two source matches with real retrieval. No training/evaluation; format unblock only.
- Two MBS format runs remain failures: `f92413aa` attempt06 374.297 seconds and 36,728 tokens, all four subquestions fail; `ce4a4a34` attempt07 351.713 seconds and 36,425 tokens, one subquestion passes after question→trace→answer ordering, still no qualified offspring, paired roots, or RL updates. No passing receipt. CPU and CUDA parsing do not establish teacher/verification quality or explain all failures.
- Full SkillDreamer three arms × 42/43/44 completed and verified per field. [Receipt](../../gpu-validations/oct13-skilldreamer-a100.json) passes shared mechanism contract: 348 CSI, 44 skill loads, 285 successful calculator calls, zero submissions. No-skill 20.83%, direct retrieval and method zero. L1 only. Overlapping short seed42 and parallel 43/44 wall times are not efficiency evidence.
- `dd54035d` MBS teacher A100 short probe: 14 outputs and 3,876 tokens; one of three train roots independently solved, two root-4 subproblems verified; four-item random/greedy validation 50%/75%. No student, optimizer, or full path. `4c4710cd` optional `construction_teacher_sample=False` controls teacher solving/JSON only; student calibration, sampled effectivity, independent verification, and all gates unchanged. Need frozen-source full check, not this probe.
- `4c4710cd` full seed42 ended exit 1, 314.887 seconds, 34,814 tokens. Of three selected hard roots, root4 new independent baseline was student 25%/teacher 100%, failing zero-success; root7/8 teacher verification failed. No descendants or RL. Independent CPU replay matched 77 responses, audit, and pairing. Do not replace measured 1/4 with earlier 0/4. No seeds 43/44 or passed receipt; pool expansion needs user choice, no blind retry.

If the user explicitly resumes after cost disclosure, verify source and actual resource bytes before executing. Collect JSON/logs per paper and verify real nonzero updates or explicit negative-control limits before sanitized receipts and unified gate. Preserve large resources needed for resume; after runs clean rebuildable staging copies, site/build/render artifacts, not results or failures.
