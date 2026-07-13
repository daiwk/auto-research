# CMSL: Constructive Multi-Sequence Learning

- 论文：[arXiv 2606.28533](https://arxiv.org/abs/2606.28533)，2026-06-26，Meta
- Adapter：`cmsl`
- 代码：`src/auto_research/reproductions/cmsl/`
- 数据：MovieLens 100K
- 运行：`auto-research reproduce --paper cmsl --seed 42`

## 论文线上证据

论文公开了 Meta surface 5 的线上 A/B：四个 engagement 指标分别提升 **0.116%、0.158%、0.171%、0.092%**。排名场景还在四个 surface 报告了生产模型 NE 改善，但没有把 NE 当作线上 A/B。

## 实现范围

实现多序列构造、各兴趣 strand 独立建模、二阶多项式线性注意力近似和候选感知聚合。公开实验用 MovieLens genre 聚类初始化 6 个兴趣 strand，以轻量 sequential embedding 替代 Meta 的生产 HSTU 与内部特征。

## 实验协议

评分 >= 4 作为正反馈；per-user leave-two-out；完整 item catalog 排序；三个 seed；每个 seed 的融合权重只由 validation 选择，test 不参与调参。

## 本机结果（2026-07-13）

| Model | Hit@10 | NDCG@10 |
|---|---:|---:|
| Single sequence | 0.0726 ± 0.0013 | 0.0351 ± 0.0014 |
| CMSL | 0.0726 ± 0.0027 | **0.0355 ± 0.0016** |

## 结论与边界

平均 NDCG@10 提升 **0.95%**，但提升小于跨 seed 波动，结论是“方向正向、证据不足”，不能声称在 MovieLens 上稳定复现生产收益。

MovieLens genre 聚类只是 latent sequence construction 的公开代理，不等价于 Meta 的可学习构造模块、HSTU kernel 和生产特征。
