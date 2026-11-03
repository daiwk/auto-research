# 2026-09-28: Executable mechanisms from three papers

<!-- source-sha256: 68afb1f80417e672bd7d15235e1e7792fec67918e26171fcea308c755127cf0a -->

[简体中文](../../experiments/sep28-three-mechanisms.md)

> **Status: Scaled mechanism experiments, not full reproductions.** Checked equations were implemented as testable code. No answer or plan enters agent inputs; synthetic states and small-model runs are not paper benchmarks. Amazon-M2 is unavailable, so CMRec is excluded.

## GRAFT: Credit assignment across a trajectory graph

| Paper information | Value |
|---|---|
| Paper | [arXiv:2609.28963v1](https://arxiv.org/html/2609.28963v1) |
| First-author affiliation | Shanghai Jiao Tong University; work during a Tencent AI Platform internship |
| First published | 2026-09-24 |
| Original author code | The paper says it will be released. The [linked repository](https://github.com/xcyao00/GRAFT) returned 404 during review; no usable source found. |
| Local key and code | `graft-mechanism`; `src/auto_research/agent_research/graft.py` |

The paper merges task rollouts into a state–action graph, assigns outcomes to terminal nodes, solves intermediate values by Bellman iteration, and uses `γV(s')−V(s)` for step credit. The local implementation follows exact state matching in Eqs. 5–10, with empirical transition probabilities from raw edge counts and Graph GAE. Tests confirm an early useful action can receive positive credit in a failed rollout and one terminal state cannot carry conflicting labels.

With all empirical edges and exact Bellman convergence, the mean TD residual at each successor is zero, so Graph GAE reduces numerically to one-step TD. This does not refute approximate graph or training settings. No LLM policy updates, ALFWorld/WebShop runs, or embedding-based state merges were performed.

### Trainable policy comparison in a public tool environment

The local gold-free `toolroute-l2.1-v1` environment trains a tabular softmax tool policy. The policy sees only public observations, tool tags, and live feedback. After training, separate validation and test task families are evaluated. Terminal outcome REINFORCE controls for tasks, epochs, and learning rate. The policy is not an LLM and the environment is not ALFWorld/WebShop, so this is a diagnostic without a formal GRAFT adapter.

```bash
PYTHONPATH=src python scripts/run_graft_public.py \
  --seeds 42,43,44 --train-episodes 36 --evaluation-episodes 60 \
  --epochs 4 --learning-rate 0.25
```

Each seed trains 36 tasks for 4 epochs, with 60 validation and 60 test tasks. Three-seed test joint success is `0.7778` for both methods; step F1 is `0.8535` and average tool cost is `5.3176` for both. **No measurable gain from graph credit** in this budget. Near-zero multistep mean TD residual and public tags that leave just one plausible action on most steps both limit the experiment. See [per-seed metrics](../../experiments/metrics/graft-public-toolroute-l21.json). This does not justify formal L2 promotion or proven Evolve integration.

## KITE: Two towers with KV written only by the prefiller

| Paper information | Value |
|---|---|
| Paper | [arXiv:2609.27294v1](https://arxiv.org/html/2609.27294v1) |
| First-author affiliation | StepFun |
| First published | 2026-09-23 |
| Original author code | No verifiable model or training source in the paper; no public code found. |
| Local key and code | `kite-sst-small`; `src/auto_research/foundation_models/kite_sst.py`, `scripts/run_kite_sst.py` |

Train a two-layer prefiller, expand a two-layer decoder from its parameters, then train both. Decoder layers read corresponding prefiller KV and never write KV. Bulk prefill skips decoder history and runs it only at the final prompt position. Incremental single-token decode and full-forward last logits differ by less than `1e-5`; gradients reach the prefiller KV projections and decoder query.

CPU-only, with separate public WikiText-2 train, validation, and test files:

```bash
PYTHONPATH=src python scripts/run_kite_sst.py --data-root data \
  --source-steps 30 --continuation-steps 30
```

Fixed seeds 42/43/44 use 8×33 byte train samples and 64×33 byte examples each for validation and test. SST and source-only share data, 60 updates, and a midpoint optimizer reset; SST expands midway. The result is negative:

| NLL (lower is better) | SST 2+2 layers | Source-only 2 layers |
|---|---:|---:|
| Validation, three-seed mean | 3.6152 | 3.5942 |
| Test, three-seed mean | 3.6241 | 3.6057 |

SST has 64,704 parameters versus 43,648 and does not improve this tiny-budget quality. `last_only` and full-decoder last logits differ by at most `7.2e-7` across seeds. This verifies KV invariants and small-model training, not 67B MoE, equal-FLOP scaling, end-to-end prefill latency, or downstream gains. The script emits per-seed results and WikiText-2 SHA-256 for reruns.

## DeltaS: Keep KV according to state drift in linear attention

| Paper information | Value |
|---|---|
| Paper | [arXiv:2609.27470v1](https://arxiv.org/html/2609.27470v1) |
| First-author affiliation | Maum AI Inc. / Seoul National University |
| First published | 2026-09-23 |
| Original author code | The [paper's repository](https://github.com/MaumAI-Company/DeltaS) was accessible but empty at review; no runnable code found. |
| Local key and code | `deltas-eviction`; `src/auto_research/multimodal/deltas_eviction.py` |

The implementation follows Eq. 3 for layer-averaged relative Frobenius change and keeps attention sinks, recent tokens, and high-drift older tokens by time bucket. Unused bucket capacity goes to remaining high scores. Repeated eviction preserves original positions and does not reorder by future questions. Tests cover drift, fixed budgets, time buckets, and repeated eviction. Real Gated DeltaNet inference must supply states. No Qwen3.5-9B video checkpoint, Video-MME, or MLVU was run, so no accuracy or throughput claim.

## Next steps and limits

None is a formal reproduction adapter or exposed to Evolve: fair downstream selection is not established. Further work needs a trainable GRAFT agent and gold-free environment; equal-FLOP KITE scaling and real latency; and a Qwen3.5 video state/KV adapter with matched public evaluation for DeltaS. See [Meta MaD-RL](mad-rl-mechanism.md) separately; real-checkpoint math/code tasks are still pending.
