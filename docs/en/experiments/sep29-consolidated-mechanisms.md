# Combined Agent and post-training batch: executable boundaries

<!-- source-sha256: 7ce7209d4d8904a2f92bc7397805cc498930d9f528ce513d7e36d5e420255329 -->

[简体中文](../../experiments/sep29-consolidated-mechanisms.md)

This branch combines Agent/inference efficiency and post-training. Mechanism tests, small public-model diagnostics, and complete paper reproduction are distinct evidence levels.

## Independently runnable units

- [ToolSearcher](https://arxiv.org/html/2609.30906): `toolsearcher_credit.py` implements first-discovery events, within-group credit normalization, and search-before-selection gating. `toolsearcher_objective.py` implements differentiable event-level clipped policy loss; gradient tests exclude returned retrieval text from policy/KL updates. The [author repository](https://github.com/zhenlongDai/ToolSearcher) has StableToolBench/AppWorld training. Local Qwen RL, retriever, and AppWorld were not run.
- [ActKV](https://arxiv.org/html/2609.31395): `actkv_policy.py` implements Algorithm 1 action-region attention-aware LRFU selection. `actkv_budget.py` implements Algorithm 2 confidence trend and budget increases. The token formula uses surprisal sign, but the paper's downward-trigger criterion describes confidence; convert to confidence before fitting to avoid the opposite trigger. Paged restoration, in-place CUDA compaction, actual agent turns, and throughput are not implemented, so this is not end-to-end ActKV.
- `paired_public_comparison.py` requires at least three seeds, matched checkpoint/data versions, updates and token caps, validation-only selection, and paired test deltas. [Recursive OPSD official GSM8K diagnostic](../../reproductions/2609.30652-recursive-opsd/README-en.md) and [MaD-RL Qwen diagnostic](mad-rl-mechanism.md) ran three seeds on A100 without gains. MaD-RL uses synthetic five-choice tasks, not original math/code benchmarks.
- [KITE matched-FLOPs diagnostic](sep29-kite-equal-flops.md): public WikiText-2 compares 2+2 SST and four-layer dense with approximately matched FLOPs across three seeds. A100 random-initialized small-model CUDA prefill/decode found no clear latency gain. Neither result represents the paper's 67B MoE.
- Code-Based Skills: pinned public CodeHack and custom NLE wheel; real `MiniHack-Room-5x5-v0` on isolated Linux with primitive/skill/mixed spaces, three seeds each, nine episodes, no runtime errors. See `scripts/run_codehack_minihack.py` and [sanitized evidence](../../experiments/evidence/codehack-minihack-seeds42-44.json). The controller was seeded uniform random and action spaces differ, so completion rates are not fair method comparisons. The author baseline repository establishes version only; its single-GPU LLM evaluation and eight-GPU training were not executed.

Re-run the environment check on Linux with author's `codehack` and custom NLE wheel:

```bash
python scripts/run_codehack_minihack.py \
  --seeds 42,43,44 --max-decisions 8 --primitive-budget 64 \
  --output runs/codehack-minihack-smoke.json
```

## Evidence needed for full reproduction

| Work | Missing evidence |
|---|---|
| ToolSearcher | Pinned public StableToolBench and 16k tool index, budget-matched Qwen2.5-7B/Qwen3-4B RL and baseline, isolated AppWorld test |
| ActKV | Real action KV, equal-budget FullKV/SnapKV/R-KV, matching paged kernel, A100/A30 throughput and memory |
| Code-Based Skills | [CodeHack](https://github.com/BartekCupial/codehack) `3026cdb7`, [baselines](https://github.com/BartekCupial/codehack-baselines) `ba2c532b`, and custom NLE verified. Nine actual MiniHack episodes ran, but random control is not the original LLM policy. Compare all three modes with the same model, data, decisions, and primitive-step budgets. |
| GRAFT/DeltaS | Original tasks, model environments, and fair-budget evaluation; bounded diagnostics cannot substitute |
| KITE | Original model/corpus scale, real long context and throughput; measured small CUDA paths are launch-bound microbenchmarks, not paper speed |
| Recursive OPSD and MaD-RL | Budget-matched Qwen3-4B runs and isolated test across three seeds are negative. Original training distributions, benchmarks, and budgets remain absent, so these are mechanism/public-task diagnostics. |
| MuSeR | Auditable public product semantics, cache refresh, and fair offline/online controls; KuaiRand tags are not the original semantic encoder |

A CUDA upgrade is complete only after actual A100/A30 execution and a sanitized receipt accepted by `scripts/validate_gpu_evidence.py`. Preserve missing public data or author environments as gaps rather than calling synthetic substitutes formal results.
