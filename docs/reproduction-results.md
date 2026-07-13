# Paper reproduction results

运行日期：2026-07-13。所有结果均在本项目当前 Mac 环境本地生成。

## LLM：Selective Importance Sampling（SIS）

- 论文：[Turning Off-Policy Tokens On-Policy](https://arxiv.org/abs/2607.04728)
- 实现：`sis_topk_weight`，对应论文 Algorithm 1、公式 10–11。
- 数据：Tiny Shakespeare。
- 设置：字符 bigram；前 45% 拟合 stale behavior policy，随后 35% 拟合 current policy；每个种子采样 50,000 token；top-K=10。
- Baseline：标准 token-level importance sampling。

| Seed | SIS weight-variance reduction | SIS accept rate |
|---:|---:|---:|
| 41 | 14.56% | 68.67% |
| 42 | 4.78% | 68.65% |
| 43 | 0.53% | 68.81% |
| Mean | **6.62%** | **68.71%** |

结论：三个种子均降低 importance-weight 方差，但收益幅度有明显随机性。这个实验验证 SIS 的核心 ratio 转换机制，不等价于论文的 Qwen + GRPO/DAPO 训练结果。

## 推荐：Multi-source Divergence-Consensus Negative Sampling（MDCNS）

- 论文：[Divergence Meets Consensus](https://arxiv.org/abs/2605.19651)
- 作者代码：[SIGIR26-MDCNS](https://github.com/Lyz103/SIGIR26-MDCNS)
- 实现：两个 sequential embedding 模型；Self/Peer/Ensemble 三源负例；disagreement 增强重排；ensemble soft target KL distillation。
- 数据：MovieLens 100K；评分 >= 4 作为正反馈。
- 设置：938 用户、53,485 个训练转移、1,682 items；per-user leave-last-one-out；4 epochs；30 个候选负例；top-K=5。

### NDCG@10

| Seed | Uniform | DNS | MDCNS |
|---:|---:|---:|---:|
| 41 | 0.037983 | 0.005209 | **0.041190** |
| 42 | 0.033805 | 0.017046 | **0.042000** |
| 43 | 0.038493 | 0.016176 | **0.043333** |
| Mean | 0.036761 | 0.012810 | **0.042174** |

MDCNS 的平均 NDCG@10 比 Uniform 高 **14.72%**，三个种子均为正向；DNS 在该轻量 sequential embedding backbone 上明显退化，因此不把相对 DNS 的巨大百分比当作主要结论。

## 复现边界

这些结果是论文核心机制的缩小版对照实验。它们不是论文全部实验的数值复刻：SIS 原文使用大语言模型和 RL 后训练，MDCNS 原文使用多个 neural sequential backbone 和六个数据集。这里的目标是确认“论文特有代码路径确实执行，并相对明确 baseline 是否产生正向信号”。
