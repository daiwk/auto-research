# SIS: Turning Off-Policy Tokens On-Policy

- 论文：[arXiv 2607.04728](https://arxiv.org/abs/2607.04728)
- Adapter：`sis`
- 代码：`src/auto_research/reproductions/sis/`
- 数据：Tiny Shakespeare

## 实现范围

实现论文 Algorithm 1 与公式 10–11：top-K behavior-policy envelope、token rejection sampling、接受后 importance ratio 置为 1，未接受时保留原始 ratio。

## 实验设置

字符 bigram；前 45% 拟合 stale behavior policy，随后 35% 拟合 current policy；每个种子采样 50,000 token；top-K=10。Baseline 为标准 token-level importance sampling。

## 已确认结果（2026-07-13）

| Seed | SIS weight-variance reduction | SIS accept rate |
|---:|---:|---:|
| 41 | 14.56% | 68.67% |
| 42 | 4.78% | 68.65% |
| 43 | 0.53% | 68.81% |
| Mean | **6.62%** | **68.71%** |

三个种子均降低 importance-weight 方差，但收益幅度有明显随机性。这是核心 ratio 转换机制验证，不等价于论文的 Qwen + GRPO/DAPO 完整训练结果。
