# UniRank 公共评测接入

[UniRank](https://arxiv.org/abs/2607.19987) 是统一序列建模与特征交互的开放排序 benchmark；[官方代码](https://github.com/salmon1802/UniRank)包含 15 个模型和 QK-Video、KuaiRand、TAAC-25、Taobao、MerRec 五个大规模数据集。

本项目提供两级接入：

1. `evolve --benchmark-suite unirank` 在现有 MovieLens 数据上启用兼容协议：时间顺序 target、确定性未见负例、global pointwise AUC/logloss，并保留 overall、long-history、tail、recent-only 等切片。这适合本地多轮搜索。
2. `auto_research.evolution.unirank.upstream_command` 为完整官方 checkout 生成可审计的 `run_expid.py` 命令。最终大规模结论应在官方五数据集协议上确认。

```bash
auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "比较统一序列建模与特征交互结构" \
  --benchmark-suite unirank \
  --fitness-metric unirank_composite \
  --generations 3 \
  --population 6
```

`unirank_composite = 0.5 × NDCG@10 + 0.5 × pointwise AUC`，只使用 validation 选型；test 仍只在最后评估。MovieLens 只有隐式正反馈，因此该兼容模式不能替代官方多反馈 benchmark，报告会保留这一区别。
