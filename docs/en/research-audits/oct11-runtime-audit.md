# October 11 runtime failures and evidence corrections

<!-- source-sha256: ac794964c1c95e1fb3eb26a0b0edccc837003e98504423e2db1a7b7e9a9bad9c -->

[简体中文](../../research-audits/oct11-runtime-audit.md)

This page preserves failed or ineligible runs without converting them into passing GPU receipts.

| Method | Observation | Disposition and limits |
|---|---|---|
| VFold, four calibration questions | BF16 logit relative error 0.0211506 exceeds fixed 0.02 threshold | Rejected. Calibrating on 32 training questions lowered error to 0.0172934, not exact equivalence |
| VFold, old Cache interface | `lazy_initialization` signature differs from local version; decode failed | Adapted to bound signature, with real small Qwen regressions for both interfaces. Later A100 full decode passed |
| OPD representation diagnostic | Remote `hidden_states` is a final tensor, not layer tuple; iterating the batch axis caused a shape failure | No reshaping workaround. Hooks on embedding, intermediate layers, and final norm collected 37 locations; A100 completed |
| ZCPO, first eight steps | Equal-reward groups all skipped; no updates. Official test passed as validation, while report claimed `test_read=false` | Retracted eligibility. Not successful training or independent validation. Later runs derive holdout from official train; preserve zero effective groups |
| ZCPO, old 24-step report | Nine effective groups and nonzero updates, before split-manifest validation was added | Do not relabel the old run. Rerun from traceable source and manifest; old values are diagnostic |
| ReCal, old four-question control | ReCal 1.0 after SFT and 0.75 after OPD; control 1.0 after OPD | Retain negative result, not capability gain. Rerun with pre-execution split-manifest check |
| ReCal / ZCPO, current-source rerun | Train-only holdout manifest verified before execution. ReCal negative result and ZCPO nine effective groups/0.625 EM match previous runs | New receipts bind executed commits. Old reports are not overwritten |
| Option-Channel, early evidence tier | Native synthetic safety probe mislabeled `diagnostic_only=false` | Corrected to L1 mechanism diagnostic and reran on A100. ASR and no-denominator result unchanged; not agent capability or production safety |
| SparseDecoding, first Triton build | JIT local scope did not bind `tl`; A100 compile failed | Moved to lazily imported Triton module. Four real N:M kernels passed numerical checks |
| SparseDecoding, 128-token first run | All 12 validation answers truncated across dense and two sparse recipes; numeric scores zero | No quality claim. Log EOS/truncation, remove needless terminal forward, warm up on training inputs, pin source and expand to 512 tokens |
| SparseDecoding, 512-token comparison | Dense 4/4 completed and matched; fixed text sparse matched 2/4 and decode-calibrated sparse 1/4, both truncating 3/4. Sparse throughput slower | Retain failures. Only decoding-only calibration and actual bitmask kernel execution verified, not accuracy, speed, or evolve gains |
| PIVOT, public dependencies | A100 Hugging Face timed out. Existing same-vocab 4B attempt also reset downloading official Banking77 | No three-recipe GPU training or passing receipt at this point. Source, isolation, and routing tests are not GPU validation. Public data/weight sync needs separate authorization |
| PIVOT, authorized three-arm run | Pinned 0.5B student and 7B teacher, shared SFT→OPD warmup, eight real steps per arm. All three 0% on eight validation items; PIVOT mixed OPD/GRPO routing | Training and routing execute, not capability gains from displacement or heterogeneous reward. Retain negatives |
| Memento3, real frozen 7B | Initial observation admitted one generated model; first real action contradicted it, repair failed, zero valid models, task incomplete | Record `falsified_generated_model`. GPU pass covers safe interpretation, validation, and mismatch only; `capability_passed=false`. No handwritten navigation fallback |
| SGUID, first 4B probe | Eight actual gradient steps and updates but all skill support nonpositive, no persistent selection. Instruct-2507 template does not switch thinking | Retain failure and thresholds. Cannot establish thinking behavior or two rounds. Verify actual rendering, not accepted arguments |
| SGUID, 9B two-round run | Thinking toggle verified. First 32-step probe kept six skills and completed 16 distillation steps. Second 32-step probe had at most one late positive per skill, below fixed h=2 | [Failure artifact](../../research-audits/oct11-sguid-failed-selection.json) binds source. Exactly restored round-one weights; no second compact pass. All four baseline/final items truncated, EM=0; no passing receipt |
| SGUID, preregistered 9B expansion | Two rounds of 200 probe and 32 compact updates, 464 real updates, six/three skills. Four-question EM 0.75→0.25; two truncated before and after | [New receipt](../../gpu-validations/sguid-a100-20261012.json) passes L1 mechanism only; `capability_passed=false`. Keep original failures, no formal capability gain |
| V-CoLA, remote PR CI | Transformers 5.19 moved instance kernel to module function. Previous capture raised AttributeError; three small real-model tests failed | Isolated target-instance globals preserve official decorator and dispatch. 29 tests passed on each version. A100 5.19 passed 12 paired forwards, baseline error 0, max state error 0.001648. Receipt binds new source. Remote checks passed for fix `6a3298e0`, not the old failure |
| Data-Space, dependencies and cache | Missing SciPy, then empty CIFAR dir mistaken for cache; remote official download slow | Installed dependency in temporary directory. With user authorization synced only five public train files and checked each official MD5; no test sync/read |
| Data-Space, first actual backward | Student/fake deep copies of frozen teacher inherited `requires_grad=False`, causing backward failure | No passing evidence. Fixed trainability, added actual train→freeze→DMD backward regression, then reran pinned source. Unit tests cannot replace GPU validation |

Passing receipts establish execution of the specified command and protocol, not all paper experiments, statistical gains, or evolve integration. See [full scope](oct11-implementation-scope.md).

## Data roles and manual source review

- SGUID gold is restricted to the training rollout verifier, training-skill preparation, and external validation scoring. Student, retrieval, and generation do not read gold. Actual rendered prefixes verify thinking, not just the accepted `enable_thinking` argument.
- V-CoLA uses public class definitions, not image labels in model input. External scoring follows actual logits. Four constrained-letter images are not full generation accuracy or compression-rate selection.
- Data-Space splits official training data into train/holdout. Verify teacher, fake, and generator updates, freezes, and parameter digests separately. Iteration count is not execution evidence.
- Memento3 sees public grid and actual interactions only. A bounded AST interpreter runs generated Python without `exec/eval` or hidden transitions/gold plans. Handwritten test models are not runtime fallbacks.

`fidelity-source-inventory.json` is a supporting AST inventory, not semantic correctness or capability certification. SHA-256 of four actual 9B weight files matched the pinned official Hugging Face revision. Source digests matched immutable commits and remote files.

All 38 execution-source digests in registered receipts match their immutable commits. Shared `oct11_objectives.py` later added PIVOT frozen-reference KL parameters and branches. Per-section diff review confirmed ZCPO was unchanged; old receipts retain their original digest.
