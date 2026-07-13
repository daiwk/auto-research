# G2Rec: Graph interest tokens for generative recommendation

- 论文：[arXiv 2606.20554](https://arxiv.org/abs/2606.20554)，2026-06-18，Meta
- Adapter：`g2rec`
- 代码：`src/auto_research/reproductions/g2rec/`
- 数据：MovieLens 100K
- 运行：`auto-research reproduce --paper g2rec --seed 42`

## 论文线上证据

论文披露 7 天和长期线上 A/B：in-session 指标 **>+0.03%**，time spent、likes、shares 等 engagement 指标提升 **0.06%–0.19%**。

## 实现范围

从训练用户历史构建 item-item co-engagement graph，用归一化图谱的谱分解得到 12 维 soft interest prototypes，并组合 item token 与 interest-profile token 打分。验证集选择融合权重；轻量 graph next-token scorer 替代论文的 Llama 2 13B + LoRA。

## 实验协议

评分 >= 4 作为正反馈；per-user leave-two-out；完整 item catalog 排序；validation 从候选融合权重中选择 graph-token weight，test 不参与调参；图构建是确定性的。

## 本机结果（2026-07-13）

| Tokenization | Hit@10 | NDCG@10 | Head share@10 |
|---|---:|---:|---:|
| Item only | 0.0622 | 0.0246 | 0.2436 |
| Item + interest tokens | **0.0676** | **0.0284** | 0.5715 |

## 结论与边界

NDCG@10 提升 **15.45%**，但 head-share@10 从 24.36% 升到 57.15%。结论是图兴趣 token 明显提高命中质量，同时在这个实现中放大热门偏差；上线前必须加入去偏或多样性约束。

本地 graph next-token scorer 不等价于论文的 Llama 2 13B + LoRA 生成模型。
