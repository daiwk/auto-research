# Unified evaluation protocol for LLM post-training

<!-- source-sha256: e70cbcf0533fcf58a5cf2db97d8701eebe9b4b05acd41ec05642abe10652edc0 -->

[简体中文](../../post-training/benchmark.md)

This protocol compares algorithmic mechanisms and provides a consistent interface for small real LLMs, Linux CPU runs, and GPU training. All tables must distinguish **results reported in papers** from **local reproduction results**.

## Evaluation levels

| Level | Data | Purpose | Supported conclusion |
|---|---|---|---|
| L0 | `arithmetic-smoke` | Verify sampling, reward, update, and reporting in seconds | The implementation runs |
| L1 | `gsm8k-candidate` | Candidate-policy training on public data | The core mechanism works in a fixed candidate space |
| L2 | `arithmetic-generate` / `gsm8k-generate` | Real tokenizer, free generation, and verifier | Local free-generation mechanisms can be compared |
| L3 | Paper-scale models and data | Match the paper's setup | High-fidelity paper reproduction |

Candidate methods have stable L1 results. IPO, SimPO, LUSPO, and CoBA-RL reach local L2. L2 exact generation accuracy is not comparable to L1 candidate accuracy and does not establish L3.

## Data and fair comparisons

- Use public GSM8K with fixed sets of 512 training and 128 validation examples.
- Use the same six candidate answers for each question and measure validation exact-answer accuracy.
- Start every method from the same untrained policy, with 300 steps and seed 42.
- Do not use validation answers for tuning. New methods report accuracy, mean reward, and KL(reference).
- Multi-objective methods also report reward axes and drift events. Distillation methods also report teacher call counts.
- L2 fixes the character tokenizer, GRU causal LM, SFT warmup, and seeds 42/43/44. Report means and standard deviations for exact generation, format rate, and response length.

## Stable results

| Method | accuracy | mean reward | KL(reference) |
|---|---:|---:|---:|
| Untrained policy | 0.1641 | 0.3126 | 0.0000 |
| DPO | 0.8047 | 0.8347 | 0.0683 |
| KTO | 0.8359 | 0.8560 | 0.0143 |
| ORPO | **0.8438** | **0.8618** | 0.8973 |
| GRPO | 0.7812 | 0.8169 | 1.0401 |
| DAPO | 0.7578 | 0.7996 | 1.0870 |
| GSPO | 0.8281 | 0.8509 | 0.7017 |
| PPO-RLHF | 0.8125 | 0.8335 | 0.8731 |
| RLOO | 0.8281 | 0.8509 | 0.5707 |
| ReMax | 0.7031 | 0.7554 | 0.7939 |
| Lightning OPD | **0.8359** | **0.8561** | 0.8269 |
| GPRL | 0.3672 | 0.5002 | 1.1022 |
| TCR | **0.8359** | 0.8560 | 0.5629 |
| Constitutional AI | **0.8438** | **0.8617** | 1.0214 |
| RRHF | 0.8125 | 0.8401 | 0.8344 |
| RAFT | **0.8438** | **0.8617** | 0.8789 |
| SLiC-HF | 0.7812 | 0.8074 | 0.2512 |
| SteerLM | 0.8516 | 0.8654 | 0.9112 |
| SPIN | **0.8594** | **0.8691** | 0.1294 |
| VAD (120 steps / 256 examples) | 0.7969 | 0.8153 | 0.0092 |

GPRL targets open-ended multidimensional preferences. A lower exact-answer score does not refute the paper's conclusions. The result calls for further evaluation with a multidimensional judge such as AlpacaEval, not hiding the unfavorable result.

VAD uses the quick-regression setup for this batch: 256 training examples, 64 validation examples, and 120 steps. Do not rank it against the 300-step results above. The run verifies evidence intervention, support and opposition budgets, one-sided projection, and target reconstruction. The process-quality axis does not use actual visual inputs, so these results are not comparable to the paper's six visual benchmarks.

- Stable candidate data: [post-training-gsm8k-candidate-seed42.json](../../experiments/post-training-gsm8k-candidate-seed42.json).
- Classic RL: [classic-post-training-gsm8k-seed42.json](../../experiments/classic-post-training-gsm8k-seed42.json).
- Free generation: [free-generation-post-training-seeds42-44.json](../../experiments/free-generation-post-training-seeds42-44.json).
- Classic gaps in this batch: [p0-missing-post-training-gsm8k-seed42.json](../../experiments/p0-missing-post-training-gsm8k-seed42.json).
- P1 candidates: [p1-alignment-candidates-gsm8k-seed42.json](../../experiments/p1-alignment-candidates-gsm8k-seed42.json).

## Running and artifacts

```bash
auto-research post-train --algorithm rloo \
  --dataset gsm8k-candidate --maximum-examples 512 \
  --steps 300 --seed 42

auto-research post-train --algorithm luspo \
  --dataset arithmetic-generate --maximum-examples 48 \
  --steps 6 --seeds 42,43,44 --offline
```

Each run writes to `runs/post-training/<algorithm>-<dataset>-seed<seed>/`:

- `metrics.json`: machine-readable metrics, configuration, and algorithm diagnostics.
- `report.md`: Chinese experiment conclusions and reproduction limits.
- Checkpoints stay local and are not committed to GitHub.

## Accepting new methods

New candidate methods must pass L0 and L1. Methods that depend on sequence length, online rollouts, or capability boundaries must reach L2, run with multiple seeds, and pass the strict MkDocs build. Explicitly state when a large-model judge or teacher is not connected.

## Additional OPD and token-credit diagnostics

Relay-OPD reports failed prefixes, teacher handoffs, relay budget, and student recovery as well as final accuracy. CoRT reports counterfactual replay count, rubric contrast, and token-weight range, and verifies that no auxiliary token scorer is used. Both retain the same candidate policy, train/validation split, step count, and seed.

GKD reports student-generated rollouts, on-policy fraction, and online teacher scoring. MiniLLM reports reverse KL, teacher-mixed sampling, variance-reduction baseline, and length normalization. Neither teacher-call cost should be conflated with Lightning OPD's zero online calls during training.

ReCo reports response expected-count weights, token variance ratios, the fraction of unsaturated positions, and rollout-policy refresh. Reusing GRPO or adding entropy regularization alone is not ReCo.

TIS, IcePop, and Online IcePop report policy staleness and training/inference engine ratios separately. TIS applies only one-sided upper truncation to the latter and must not drop low-ratio samples. IcePop zeros gradients outside a fixed two-sided interval and preserves original correction weights inside. Online IcePop updates once per rollout batch, keeps the policy ratio at 1, and disables PPO clipping. Fixed-seed snapshots: [rl-papers-summary-seed42.json](../../experiments/rl-papers-summary-seed42.json).

OPSD additionally reports privileged-context teacher calls, on-policy student rollouts, token-level divergence, and pointwise clipping. OPCD distinguishes the experience-conditioned teacher from the context-free student, and reports the experience cache, reverse-KL update, and context-free inference after training. See [omitted-agentic-rl-opd-seed42.json](../../experiments/omitted-agentic-rl-opd-seed42.json) for fixed-seed candidate-suite snapshots. Candidate classification accuracy is not a reproduction of the paper's large-model benchmark.
