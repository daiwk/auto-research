# Cluster GOOBS: LLM-clustered hard negatives

- 论文：[arXiv 2607.00448](https://arxiv.org/abs/2607.00448)，2026-07-01，Meta
- Adapter：`cluster-goobs`
- 代码：`src/auto_research/reproductions/cluster_goobs/`
- 数据：MovieLens 100K
- 运行：`auto-research reproduce --paper cluster-goobs --seed 42`

## 论文线上证据

论文使用 3% control 与 3% test 用户做线上 A/B，报告 CTR **+53%**、训练 QPS -1.4%、top-100 物品曝光贡献从 50% 降到 32%。这是本轮最明确的“LLM + 召回采样”生产证据。

## 实现范围

实现论文 Algorithm 2 的同 cluster 实时 OOB 负采样，并按 MovieLens 设置使用 1:15 的随机/cluster 负例比例。由于 Meta 的多模态 LLM item embedding 不公开，公开数据实验使用 MovieLens genre cluster；轻量双塔 sequential embedding 替代生产模型与分布式 GOOBS 哈希池。

## 实验协议

评分 >= 4 作为正反馈；per-user leave-two-out；完整 item catalog 排序；随机 OOB 与 1:15 random/cluster OOB 对照；三个 seed。

## 本机结果（2026-07-13）

| Sampler | Hit@10 | NDCG@10 | Head share@10 |
|---|---:|---:|---:|
| Random OOB | 0.0851 ± 0.0048 | **0.0421 ± 0.0022** | 0.9705 ± 0.0038 |
| Cluster GOOBS (1:15) | 0.0840 ± 0.0044 | 0.0403 ± 0.0007 | **0.9614 ± 0.0017** |

## 结论与边界

Cluster GOOBS 的 NDCG@10 下降 **4.36%**，head-share@10 下降 **0.94%**。genre 标签能复现降低热门集中度的方向，但没有复现 CTR/排序收益；最可能的差距是 genre cluster 远弱于论文的 300 个多模态 LLM clusters，同时 MovieLens 100K 的 item 规模太小。
