# MaD-RL: Lightweight diagnostic of distribution-matching rewards

<!-- source-sha256: 4e26fc4d2ecd4822b9ed51901a284e47054c770f584b5efb2be2723bc65ffcf4 -->

[简体中文](../../experiments/mad-rl-mechanism.md)

> This runnable **mechanism diagnostic** links to the [shared paper page](../../post-training/2609.31644-mad-rl/README-en.md) but has no formal paper adapter. It includes multi-seed character-GRU comparisons and a single-token real-checkpoint Qwen3-4B diagnostic. Neither uses the original math or code benchmarks or reproduces the paper's scores.

## Paper information

| Field | Value |
|---|---|
| Paper | [arXiv 2609.31644](https://arxiv.org/abs/2609.31644); [official Meta publication](https://ai.meta.com/research/publications/mad-rl-matching-distributions-for-calibrating-llms-with-reinforcement-learning/) |
| Organization | Meta Superintelligence Labs |
| First public release | 2026-09-12 11:12:59 UTC (arXiv v1). Meta's listing is dated September 24; the PDF date does not supersede first publication. |
| Upstream code | No public source found as of 2026-09-29 |
| Local adapter / CLI key | `mad-rl` (standalone mechanism experiment, not a formal paper adapter) |
| Local code | Rewards and character policy: `src/auto_research/post_training/mad_rl.py`; Qwen3-4B CUDA diagnostic: `scripts/mad_rl_qwen_choice.py` |

## Cost decision and catalog links

This page preserves the original diagnostic and negative results. The paper resource key `mad-rl` is not the GPU diagnostic key `mad-rl-qwen-choice`. The latter's existing A100 receipt is unchanged and not rebound. No new CUDA work is claimed.

The [paper's §3.2 protocol](https://arxiv.org/html/2609.31644v1#S3.SS2) uses Qwen3-4B: synthetic training at 6,000 steps, group size 32, and 48 runs; math and code at 1,200 steps, group size 16, multiple recipes, and three seeds. The complete campaign is **too expensive and not reproduced (review DONE)**. This update links the catalog and corrects the date without retraining. `adapter: null` means there is no formal paper adapter, not that existing diagnostics are removed or promoted to capability reproduction.

The paper estimates category frequencies over a group of outputs, then constructs per-example rewards from differences between target and empirical distributions. The implementation includes L2, forward KL, reverse KL, and Jensen–Shannon rewards, with correctness-only reward as control. All five options are valid responses. During training, target options are not given to the policy as individual answers. Invalid outputs remain in the frequency denominator and receive a fixed penalty. Zero-probability target categories are smoothed in logarithmic rewards.

Local runs use a 32-dimensional character GRU, single-token free sampling, group-relative advantages, and clipped policy updates. Balanced SFT warmup on training topics precedes 60 training steps. The 8 training, 2 validation, and 2 test topics are disjoint. Each reward starts from the same initial policy per seed and runs independently for 42, 43, and 44. Test is read only after training.

```bash
auto-research mad-rl --target 0,0,0.3333333333333333,0.3333333333333333,0.3333333333333333 \
  --seeds 42,43,44 --steps 60 --group-size 16 --device cpu \
  --output-dir runs/post-training/mad-rl-peaked

auto-research mad-rl --target 0.2,0.2,0.2,0.2,0.2 \
  --seeds 42,43,44 --steps 60 --group-size 16 --device cpu \
  --output-dir runs/post-training/mad-rl-uniform
```

The table gives three-seed mean test Jensen–Shannon divergence **conditional on valid options**, lower is better. Invalid-output rates are recorded separately; those outputs are not hidden from the sampling denominator.

| Reward | Peaked target: JSD before → after ↓ | Uniform target: JSD before → after ↓ |
|---|---:|---:|
| Correctness only | 0.1749 → 0.1521 | 0.0064 → 0.0101 |
| L2 | 0.1749 → 0.0159 | 0.0064 → 0.0048 |
| Forward KL | 0.1749 → 0.0048 | 0.0064 → 0.0076 |
| Reverse KL | 0.1749 → 0.0064 | 0.0064 → 0.0061 |
| Jensen–Shannon | 0.1749 → 0.0052 | 0.0064 → 0.0072 |

For the peaked target, distribution rewards better match the target than correctness alone. The uniform target begins with low JSD, and not all rewards improve it. This demonstrates a runnable **small-model distribution-matching mechanism**, not the paper's large-model findings or cross-task generalization. The commands produce auditable per-seed JSON and Markdown reports.

## Real Qwen3-4B checkpoint diagnostic on A100

The public `Qwen/Qwen3-4B-Instruct-2507` checkpoint runs the same five-option task with rank-8 LoRA, 15 balanced warmup steps, and 8 group-relative updates using the paper's Jensen–Shannon category reward. Each group uses 16 **real next-token samples**, with invalid tokens in the full denominator. Train/validation/test topics are 8/2/2. This exercises actual model parameters and category rewards, not the paper's multilingual GSM8K or code free generation.

```bash
PYTHONPATH=src python scripts/mad_rl_qwen_choice.py \
  --checkpoint /path/to/Qwen3-4B-Instruct-2507 \
  --output runs/post-training/mad-rl-qwen-choice.json \
  --seed 42 --warmup-steps 15 --steps 8 --group-size 16 \
  --eval-samples 16 --divergence jsd
```

| Validation metric | After warmup, before RL | After 8 steps |
|---|---:|---:|
| Target JSD among valid categories ↓ | 0.4127 | 0.4127 |
| Valid output rate ↑ | 1.0000 | 1.0000 |
| Category counts A/B/C/D/E (32 samples) | 16/0/16/0/0 | 16/0/16/0/0 |

The L2 change in trainable LoRA parameters was `0.0982`, but the 32 validation samples did not move toward the C/D/E mixture. This does not establish successful large-model distribution matching. The isolated post-training test JSD was `0.6398`; the sample is too small for generalization claims. See the [sanitized GPU receipt](../../gpu-validations/mad-rl-qwen-choice-a100-20260929.json) for the GPU, public revision, and command.

### Additional three-seed same-budget diagnostic

On the same A100, public checkpoint, and topic split, run L2, forward KL, and Jensen–Shannon rewards for seeds `42/43/44`. Each arm uses 4 balanced warmup steps, 4 RL updates, group size 8, and 16 samples per validation or test topic. Select rewards by validation JSD conditioned on valid options only. Report invalid-output rates separately. Test does not select the method.

| Reward | Validation JSD (42/43/44, ↓) | Test JSD (42/43/44, ↓) |
|---|---|---|
| L2 | 0.4127 / 0.4127 / 0.4127 | 0.5078 / 0.4483 / 0.4695 |
| Forward KL | 0.4127 / 0.4127 / 0.4127 | 0.5078 / 0.4483 / 0.4695 |
| Jensen–Shannon | 0.4127 / 0.4127 / 0.4127 | 0.5078 / 0.4483 / 0.4695 |

Validation ties across all arms; the predefined tie-break retains the L2 control. Test results also tie. The three validation invalid-output rates are zero, which does not remove invalid tokens from the training sampling denominator. This verifies real Qwen parameter updates and a same-budget comparison, not the paper's math/code distribution matching: the task remains a synthetic five-choice topic exercise. See [sanitized per-seed metrics](../../experiments/evidence/mad-rl-qwen-choice-seeds42-44.json). The selection script is `scripts/compare_mad_rl_qwen_choice.py`.

For each seed `42,43,44` and `--divergence l2 / forward-kl / jsd`, run the Qwen script with `--warmup-steps 4 --steps 4 --group-size 8 --eval-samples 16`. Name outputs like `l2-42.json`, then run:

```bash
PYTHONPATH=src python scripts/compare_mad_rl_qwen_choice.py \
  --directory runs/mad-paired --output runs/mad-paired-summary.json
```

## Full experiment boundary

- The [paper page](../../post-training/2609.31644-mad-rl/README-en.md) maintains the original source, key figure, and exact date. This page preserves the diagnostic without duplicating them.
- The paper's math and code free generation, multiple target distributions, and baseline matrix are **too expensive and not reproduced (review DONE)**. These GRU and Qwen3-4B single-token diagnostics do not substitute for them, and they are not a retraining TODO.
