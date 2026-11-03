<!-- source-sha256: e3c86f360f3741da81e3f9e0152558195d5dd3235c2b99024bb81ad61777b999 -->

# UniRank public benchmark integration

[简体中文](../unirank.md) · [Evolution protocol](model-evolution.md)

[UniRank](https://arxiv.org/abs/2607.19987) is an open ranking benchmark that brings together sequence modeling and feature interaction. The [official code](https://github.com/salmon1802/UniRank) covers 15 models and five large datasets: QK-Video, KuaiRand, TAAC-25, Taobao, and MerRec.

This project supports two levels of integration:

1. `evolve --benchmark-suite unirank` enables a compatible protocol on the existing MovieLens data. It uses chronological targets, deterministic unseen negatives, global pointwise AUC and log loss, and slices including overall, long-history, tail, and recent-only. This is suitable for local multi-round search.
2. `auto_research.evolution.unirank.upstream_command` generates an auditable `run_expid.py` command for a full official checkout. Confirm final large-scale conclusions on the official five-dataset protocol.

```bash
auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "Compare architectures for unified sequence modeling and feature interaction" \
  --benchmark-suite unirank \
  --fitness-metric unirank_composite \
  --generations 3 \
  --population 6
```

`unirank_composite = 0.5 × NDCG@10 + 0.5 × pointwise AUC`. Select candidates using validation only and evaluate on the test set at the end. MovieLens provides only implicit positive feedback, so this compatibility mode does not replace the official multi-feedback benchmark. Reports retain that distinction.
