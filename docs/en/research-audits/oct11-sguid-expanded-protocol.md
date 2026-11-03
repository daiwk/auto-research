# SGUID expanded training preregistration (2026-10-11)

<!-- source-sha256: 2e1f4b750cbbcac198c3800c201ff302ba420101f7df08cd7a47e1f262d23c25 -->

[简体中文](../../research-audits/oct11-sguid-expanded-protocol.md)

**Fixed before execution; both rounds were later executed.** Budgets and criteria retain preregistered values. Measurements appear separately; the protocol is not rewritten around results. Preserve two earlier failures, source commits, metrics, and docs.

## Data, model, and ordering

Use cached public `Qwen/Qwen3.5-9B` revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`. Reinitialize zero-output LoRA from the original checkpoint, not a failed run or its first-round weights. Fix seed 42 without searching for a passing seed.

Use official **train** only from `openai/grade-school-math` revision `3101c7d5072418e28b9008a6636bde82a006892c`, preserving the verified deterministic split and order. Train on first 200; each round's candidates derive from current-student traces on first 32 train items. Do not select by error, skill activity, or validation accuracy. The first four validation items are external scoring only; official test unread. Train answers are for the verifier and offline skill generation only, never student, retrieval, or validation inputs.

## Fixed two-round budget

| Item | Value |
|---|---:|
| Training questions | 200 |
| Candidate skill generation attempts per round | 32 |
| Probe update attempts per round | 200 |
| Compact update attempts per round | 32 |
| Student train response limit | 1024 tokens |
| Skill generation limit | 256 tokens |
| Independent validation response limit | 3072 tokens |
| Validation questions | 4 |
| Retrieved skills | At most 6 |
| Kept skills K, two rounds | 6 / 3 |
| Gate κ / support clip / rate decay τ | 0.05 / 3 / 5 |
| Late positive activity threshold h | 2 |
| AdamW learning rate / weight decay | 5e-6 / 0 |
| Gradient norm cap / LoRA rank | 0.1 / 8 |
| Seed / co-evolution rounds | 42 / 2 |

`--evaluation-max-tokens 3072` only controls baseline/final validation, not training, generation of skills, retrieval, selection, or later budgets. Use the same cap before/after. Do not alter budget, choose checkpoints, or append runs based on validation. Omission or programmatic None preserves the old shared `--max-tokens`; old missing fields are interpreted with old budgets, not backfilled.

If both rounds finish, there are **464 optimizer attempts** (400 probe and 64 compact). Only finite nonzero gradients advance the optimizer. Also budget 64 source rollouts, 64 skill generations, and eight validation generations. Failed parses, duplicates, or filtered skills are not backfilled by hand. Actual counts can be lower; neither success nor time is guaranteed.

## Windows, acceptance, and reproduction limits

The L1 implementation uses first 100 of 200 probe steps as early and last 100 as late. The paper's [Table 5](https://arxiv.org/html/2610.12367v1#A1) uses 75/100 in R1, h=10, all-linear rank-64 LoRA, 200 training steps, and DAPO-Math-17K / AIME-HMMT. This is **not** the full setup. Retrieval still allows six skills; round-two probes are not presented as the paper's three teachers. Compact uses at most three selected skills.

The hybrid Qwen3.5 text network differs from original Qwen3. Vision is frozen and unused; q/v LoRA applies only to full-attention text layers. LM hidden-state cosine is not the paper's embedding checkpoint. Full-vocabulary signed forward KL is allowed by the generalized divergence, not original bounded SGSD discrepancy. Negative coefficients remain; stability from the bounded method does not transfer. Finite gradients do not establish paper capability.

Require actual current-student skills, live same-weight no-grad teacher alignment on student responses, unchanged coefficient signs and gates, and positive activity only when c>0. Enforce AE>0, AL≥2, QL≥QE/5 and order by AL/QL. Restore θr exactly after probing and recreate the optimizer before compact distillation. Regenerate the next candidate pool from the updated policy. Passing receipt requires two completed rounds, nonzero finite gradients and parameter movement, and matching source SHA and frozen commit. Missing eligible skills or errors stay failures with traces.

Report EOS separately from truncation. Preserve all four validation outcomes. Even two successful rounds establish only bounded L1 execution, not benchmark gains from one seed, four items, or higher output budget.

## Pinned command with replaceable paths

```bash
PYTHONPATH=src python scripts/run_sguid_checkpoint.py \
  --checkpoint-path checkpoints/qwen3.5-9b \
  --checkpoint-id Qwen/Qwen3.5-9B \
  --checkpoint-revision c202236235762e1c871ad0ccb60c8ee5ba337b9a \
  --train-path data/gsm8k-holdout/train.jsonl \
  --validation-path data/gsm8k-holdout/validation.jsonl \
  --split-manifest data/gsm8k-holdout/split.json \
  --dataset-revision 3101c7d5072418e28b9008a6636bde82a006892c \
  --training-examples 200 --validation-examples 4 --rounds 2 \
  --candidate-count 32 --retrieve-count 6 --late-minimum 2 \
  --probe-steps 200 --internalization-steps 32 \
  --max-tokens 1024 --skill-tokens 256 --evaluation-max-tokens 3072 \
  --seed 42 --device cuda --output runs/sguid-expanded-seed42.json
```

Requires real NVIDIA CUDA. Preregistration and CPU wiring are not passing receipts. Use a separate output file rather than overwriting failures.

## Measured results (verified 2026-10-12)

Executed frozen post-preregistration commit `319008f69ac6224ad0a2dfe3146d551c1999f5e3`. Both rounds finished 200 probe and 32 compact steps, with 464 finite nonzero gradient updates. Each made 32 candidates and retained 6/3 under unchanged gates. Each probe restored starting weights exactly before recreating the optimizer. Round two generated skills from the updated round-one policy.

On four fixed questions baseline/final EM was 0.75/0.25. Both runs had two EOS completions and two truncations. **Negative result, not gain.** One seed, four items, and truncation are not a formal capability comparison. Stable results and the [passing mechanism receipt](../../gpu-validations/sguid-a100-20261012.json) keep `diagnostic_only=true` and `capability_passed=false`; old failures unchanged.
