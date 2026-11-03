# 2026-10-13 implementation checklist and acceptance scope

<!-- source-sha256: bd2f2f44acee5680885e442fa7241a388ce8dae36b19d8b805a58cf8817fbed6 -->

[简体中文](../../design/oct13-implementation-scope.md)

Based on main after merged PR #200, this batch accepted three P0 and 16 P1 papers plus scanner improvements in one PR. This is an execution checklist, not proof of implementation, execution, or watermark movement.

**Scope change, 2026-10-14: 18 runnable mechanism implementations and scanner improvements; MagicBeanStalk retained as research material, experiment source, and failure evidence only.** The user deferred MBS acceptance and added a mandatory cost gate. MBS was marked too costly and not reproduced for now, removed from runnable registry and public runner, and its original CUDA spec archived unchanged. No fabricated receipts or weakened gates. The fixed 19-paper review list remains and does not mean 19 implementations. Review remains at 2026-10-12; implementation does not advance it.

## Fixed paper list

| Priority | Paper / planned key | Original | Defining path |
| --- | --- | --- | --- |
| P0 | UxSID / `uxsid` | [2605.09040v4](https://arxiv.org/html/2605.09040v4) | Res-KmeansFSQ, interest anchor compression, two-level semantic probing, and actual training |
| P0 | State-OPD / `state-opd` | [2610.13238v1](https://arxiv.org/html/2610.13238v1) | Executed-state isolation from old reasoning, same-prefix teacher supervision, entropy budget, actual updates |
| P0 | MagicBeanStalk / `magicbeanstalk` | [2610.12659v1](https://arxiv.org/html/2610.12659v1) | Decomposition validity, verifiable synthesis, policy difficulty calibration, nonzero-advantage RLVR |
| P1 | GPPO / `gppo-framework` | [2610.13015v1](https://arxiv.org/html/2610.13015v1) | Actual proximal objective for f-divergence × estimator |
| P1 | TAPO / `tapo-trajectory` | [2610.13020v1](https://arxiv.org/html/2610.13020v1) | Geometric prefix ratio, length-aware clipping, local stop-gradient |
| P1 | CV-OPD / `cv-opd` | [2610.13264v1](https://arxiv.org/html/2610.13264v1) | Positive/negative crops of the same image, JSD, margin contrast, token/sample gates, actual VLM updates |
| P1 | OAL / `oal` | [2610.13674v1](https://arxiv.org/html/2610.13674v1) | QK outlier grouping, separable quadratic kernel, output calibration, LoRA conversion |
| P1 | ReplaySSM / `replayssm` | [2610.13778v1](https://arxiv.org/html/2610.13778v1) | Checkpoint/input buffers, rollback, separate state precision, actual CUDA |
| P1 | LeWAM / `lewam` | [2610.12818v1](https://arxiv.org/html/2610.12818v1) | Leakage-free dual-branch attention, latent prediction, action flow, latent regularization, control/planning |
| P1 | SmolWAM / `smolwam` | [2610.13740v1](https://arxiv.org/html/2610.13740v1) | Real Cosmos trunk, single-frame interface, one-step distillation, layout curriculum, LIBERO action evaluation |
| P1 | NEAR / `near` | [2610.13314v1](https://arxiv.org/html/2610.13314v1) | Neighborhood residuals, cluster query reference, scale fusion, single-index retrieval |
| P1 | Beyond the Final Embedding / `beyond-final-embedding` | [2610.13277v1](https://arxiv.org/html/2610.13277v1) | Frozen token sparse matching, memory-ID aggregation, global fusion, optional query adapter |
| P1 | SkillDreamer / `skilldreamer` | [2609.01642v2](https://arxiv.org/html/2609.01642v2) | Pseudo-skill generation, hybrid retrieval, execution-time reassessment and skill calls |
| P1 | SynthSelf / `synthself` | [2610.13113v1](https://arxiv.org/html/2610.13113v1) | Same-family aligner, rejection sampling, offline training, acquisition and retention tests |
| P1 | UPTURN / `upturn` | [2610.13672v1](https://arxiv.org/html/2610.13672v1) | Frozen encoder/MLP, failure-label training, new user-turn intervention, budget controls |
| P1 | DoubleCat / SemiCat / `doublecat-semicat` | [2610.13834v1](https://arxiv.org/html/2610.13834v1) | Two-layer continuous interpolation without extra forwards, discrete reveal, real diffusion LM training |
| P1 | SOAR / `soar` | [2610.13157v1](https://arxiv.org/html/2610.13157v1) | Internal/external knowledge streams, source-consistency reward, real policy updates |
| P1 | GRPO difficulty curriculum / `grpo-difficulty-curriculum` | [2610.13669v1](https://arxiv.org/html/2610.13669v1) | Current-policy difficulty estimation, dynamic bands, too-hard regression control |
| P1 | Uncertainty-guided progressive contraction / `progressive-contraction` | [2610.12933v1](https://arxiv.org/html/2610.12933v1) | Monte Carlo reasoning trees, teacher-pool contraction, student-aware routing, teacher costs |

UxSID v1 is 2026-05-09; SkillDreamer v1 is 2026-08-28. Substantive revisions are not October v1s. DuoRate and VETR are outside scope. GPPO/TAPO key names avoid overwriting existing 2508.07629 and 2607.27973 implementations.

## Scanner scope

1. Use arXiv announcements independently, preserving date, category, new/cross-list/replacement, version, and provenance. Keyword failures do not discard announcement entries.
2. Add OPD, RLVR, LLM, JEPA, world-action, memory retrieval, and variants; prioritize Google/Meta full-text verification.
3. Save reviewed versions and metadata digests; substantive updates enter a separate review queue. Separate new v1, retrospective discoveries, and revisions.
4. Record failed queries, expired announcements, and unfinished full text as coverage exceptions. Zero hits do not prove source exhaustion or advance the watermark.

## Acceptance and handoff

- The 18 accepted papers have independent runnable paths, behavior tests, Chinese pages, metadata, and auditable metrics. MBS keeps unaccepted evidence only.
- Separate real public-data runs from paper results. Label reduced scale, benchmarks not run, failures, and diagnostic levels.
- Agent policies cannot see gold answers/plans. External verifiers see labels only for training reward and offline evaluation.
- Run CUDA on designated A100/A30 and commit sanitized receipts bound to actual execution commits.
- Run applicable algorithms, generator parity, GPU gates, and full CI. Explicitly report incomplete work. Open one PR; do not merge/deploy.

## Execution checkpoint (not closed)

| Part | Verifiable progress | Remaining boundary |
| --- | --- | --- |
| Scanner | Independent announcement recall, acronym queries, version review queue, Google/Meta priority, bounded retries, regressions. All 19 reviewed versions and fixed full-text sources recorded in `paper-discovery-versions.json` | No inferred baselines for other historical records; close future scan coverage/exceptions independently |
| UxSID | Four structures; MovieLens-100K, 943 users, three real A100 seeds; same-SID cache parity; adapter/spec/Chinese page and source-bound metrics | Global generation/CI; no stable gain or industrial online replication |
| State-OPD | `6aabe57a`: three A100 seeds each for default, full-history OPD, and no expanded sampling; nine real updates, source/raw SHA verified. Eight-question accuracy zero both before and after | Global CI; none of original three benchmarks ran; no gain |
| GPPO / TAPO | Original snapshot: three A100 seeds with actual updates, plus three independent GRPO controls; local and paper metrics separate | Unified metrics/catalog/CI; eight questions are mechanism evidence only |
| DoubleCat-SemiCat | Corrected no-extra-forward core ran three A30 seeds on new snapshot; parameter changes, call counts, negative results verified | Global CI; no full original benchmark or reuse of old standard SC |
| CV-OPD / OAL / ReplaySSM | Three A100 seeds with controls/replay and sanitized receipts; CV-OPD six arms negative, OAL seed 44 did not improve, ReplaySSM compiler boundary retained | Global CI; not full capability or serving comparison |
| NEAR / Beyond | Eight A30 runs: three shared-bank seeds each and one strict bank-disjoint run each; frozen encoders, splits, raw SHA checked | Global CI; same data across seeds is not independent replication; strict test has two items, not official benchmark |
| SkillDreamer | `47f0e9ce` A100 three arms × seeds 42/43/44 verified: 1,931 responses, 195,501 tokens, 348 CSI, loads on 44 questions, 285 successful calculator calls in the method; no-skills 20.83%, direct/method both zero. Independent observer `27adb791` reproduces seven fields from raw/trace | L1 only, zero submissions and negatives retained; final CI/sync pending. Seed 42 overlapped a short teacher diagnostic and 43/44 ran in parallel; no wall-clock comparison |
| LeWAM | `0f5dca9f` three A100 seeds of native joint training and new three-arm candidate loop verified; no planning advantage | Global CI; goals from training trajectories, not holdout; full original budget not run |
| SmolWAM | `2b84c377` three A100 seeds of teacher KD, two-layout curriculum, same-initial-state student loop; 24 real updates, student and no-op zero successes; source/raw/new weights independently checked | Global CI; previous adapter input failure retained; scaled one-task diagnostic only |
| SynthSelf / Progressive contraction | Native 42/43/44 and independent receipts recomputed from actual raw results. SynthSelf seed 43 retention zero; Contraction matched full SFT on all three seeds | Final catalog/CI; no stable capability or total-compute savings claim |
| UPTURN | Seeds 42/43 have rescue signal; 44 all-zero rescue advantage and only entropy gradient, retained as failed-no-rescue-signal. Native failure and full cohort verified | Final sync/CI; no false all-pass receipt or selective budget |
| MagicBeanStalk (deferred) | `4c4710cd` greedy A100 path finished in 314.887 s, 34,814 tokens; 77 responses and construction audit independently replayed. Root 4 new student/teacher baseline 25%/100%, no-experience student zero success; root 7/8 teachers failed independently, no valid descendants or RL. Short teacher diagnostic separate | Too costly; not reproduced. No passing whole-method receipt; seeds 43/44 not started. Removed from runnable scope per user; retain original specs and failures |
| SOAR | `b9086275` A100 seeds 42/43/44 × two arms verified; 12 method and 10 ablation updates, zero accuracy for ablation seed 43 retained; independent three-seed receipt | Final catalog/CI; four validation examples/seed are L1 only |
| Difficulty curriculum | `b9086275` A30 seeds 42/43/44 × five arms, 15 runs independently recalculated and source-receipted; 151 real updates, 38 equal-value groups skipped; staged seed 42 accuracy zero and too-hard nonzero updates retained | Final catalog/CI; L1 only, no reuse of anomalous controls or stable gains |

Original snapshot `ccad3e67` and later immutable snapshots remain preserved. Do not interchange their evidence. All 15 repaired curriculum runs and SkillDreamer's full three-seed plan finished. MBS is outside executable delivery and lacks a whole-method receipt. GPU gates still cover active CUDA adapters. The table does not establish final acceptance for all 19; registry, unit tests, and commits do not replace execution.

Catalog/figure contracts, base-wheel install, and strict build passed. After adding short teacher diagnostics and strict SkillDreamer cost excerpts, full regression yielded 2,878 passes, 24 warnings, and 304.79 seconds. Then 174 targeted checks of `4c4710cd` teacher sampling isolation passed, and another full run pinned to inner source exited 0 with 24 warnings. Later evidence tools still needed targeted and integrated verification. This was not a claim that GPU gates or remote CI had passed. See the [local closeout checkpoint (Chinese)](../../research-audits/oct13-local-closeout.md).

One UxSID CPU diagnostic used a pinned public SmolLM2-135M attribute encoder, 100 users, 10,719 training examples, 100 validation and 100 test, one epoch, seed 42. Validation selected `agnostic`; UxSID test AUC was 0.5848 versus 0.5916. Retain this small negative result, not a paper or stable capability comparison. Cache/direct maximum difference was zero.

Label audit: `proximal_checkpoint` and `state_opd/checkpoint` send answers only to independent verifiers. `ArithmeticEnvironment`'s `arguments.answer` is a model submission, not reference. Evaluated policies receive no reference; behavior tests verify it. SynthSelf's offline aligner and self-builder read train gold in their defined roles, distinct from answer-free student evaluation. Step counts only record actual `step` calls, not standalone ability.

Four earlier A100 runs have receipts bound to `7e125fd0`. On October 13 the new snapshot's SSH connection closed during authentication, so the job was not shown to start. Large transfers preserved resume points, and old results do not cover new paths. The user authorized three domain agents and relevant source/scripts and pinned public inputs up to 20 GB, without private data, keys, or the workspace. Use October 14 rows and source-bound receipts for later execution. Extra MBS paired roots use train labels only at construction-verifier/RL reward boundaries.

Cleanup was also requested: inspect usage, remove rebuildable site/build/package leftovers, and retain code, uncommitted changes, positive and negative results, verification evidence, and reusable public inputs/checkpoints. Cleanup does not delete research history.
