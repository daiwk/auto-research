# Self-Evolving Recommendation System

- 论文：[arXiv 2602.10226](https://arxiv.org/abs/2602.10226)，2026-02-10，Google/YouTube
- Adapter：`self-evolving-rec`
- 代码：`src/auto_research/reproductions/self_evolving_rec/`
- 数据：MovieLens 100K
- 运行：`auto-research reproduce --paper self-evolving-rec --seed 42`

## 论文线上证据

这是与 auto-research 项目最直接相关的工业论文。Google 披露 Gemini agent 发现的 RMSProp、GLU 和复合 reward 在 YouTube/surface 指标上取得 **+0.03%–+0.14%** 的线上提升，多项达到 95% 统计显著。

## 实现范围

实现 experiment journal、离线候选 funnel、验证集 promotion、未触碰测试集 outer-loop proxy，以及论文披露的 Adagrad→RMSProp、GLU gating、recency-aware multi-objective reward 候选。为保证本地确定性，候选生成器是固定搜索空间，不调用 Gemini；测试集不是线上 A/B。

## 实验协议

评分 >= 4 作为正反馈；per-user leave-two-out；每个 seed 分别训练 Adagrad、RMSProp、RMSProp+GLU、RMSProp+GLU+复合 reward 四个候选。inner loop 只读取 validation，晋级候选与人工 baseline 才在 test 上比较；三个 seed。

## 本机结果（2026-07-13）

| Workflow | Hit@10 | NDCG@10 |
|---|---:|---:|
| Human baseline | 0.0833 ± 0.0043 | 0.0399 ± 0.0018 |
| Promoted candidate | **0.0894 ± 0.0075** | **0.0427 ± 0.0038** |

## 结论与边界

NDCG@10 平均 **+7.13%**。三个 seed 分别晋级 `RMSProp+GLU+reward`、`RMSProp` 和原始 baseline，说明自动 funnel 的价值不仅是找增益，也包括拒绝退化方案。

本地候选生成器是确定性代理，不等价于 Gemini agent 自动编写生产代码；test holdout 也不等价于真实线上 A/B。
