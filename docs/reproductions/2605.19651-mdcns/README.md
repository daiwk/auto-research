# MDCNS: Divergence Meets Consensus

- 论文：[arXiv 2605.19651](https://arxiv.org/abs/2605.19651)
- 作者代码：[SIGIR26-MDCNS](https://github.com/Lyz103/SIGIR26-MDCNS)
- Adapter：`mdcns`
- 代码：`src/auto_research/reproductions/mdcns/`
- 数据：MovieLens 100K

## 实现范围

实现两个 sequential embedding 模型、Self/Peer/Ensemble 三源负例、disagreement 增强重排和 ensemble soft-target KL distillation。Baseline 为 Uniform 与 DNS。

## 实验设置

评分 >= 4 作为正反馈；938 用户、53,485 个训练转移、1,682 items；per-user leave-last-one-out；4 epochs；30 个候选负例；top-K=5。

## 已确认结果（2026-07-13）

### NDCG@10

| Seed | Uniform | DNS | MDCNS |
|---:|---:|---:|---:|
| 41 | 0.037983 | 0.005209 | **0.041190** |
| 42 | 0.033805 | 0.017046 | **0.042000** |
| 43 | 0.038493 | 0.016176 | **0.043333** |
| Mean | 0.036761 | 0.012810 | **0.042174** |

MDCNS 的平均 NDCG@10 比 Uniform 高 14.72%，三个种子均为正向。DNS 在轻量 backbone 上明显退化，因此不把相对 DNS 的巨大百分比当作主要结论。

这是论文核心采样与蒸馏路径的缩小版复现，不是六数据集、多个 neural backbone 的 headline number 复刻。
