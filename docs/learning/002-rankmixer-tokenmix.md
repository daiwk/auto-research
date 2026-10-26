# 学习卡片 002：RankMixer 的特征怎么交互？

阅读预算：约 3 分钟。日期：2026-10-26。关联论文：[RankMixer](https://arxiv.org/html/2507.15551v3)（ByteDance，首次公开于 2025-07-21；本卡依据 v3）。

## 这期只记一件事

**固定重排负责让特征相遇，每个 token 独立的 FFN 负责学习如何组合。**

用户、商品、上下文等特征来自不同语义空间。RankMixer 在这些 feature tokens 之间用 TokenMix 交换信息，再用 per-token FFN 建模；注意力仍可用于上游的序列处理。[原文 §3.2–3.3](https://arxiv.org/html/2507.15551v3#S3.SS2)

## 用四行看懂

下面只用两个 token、每个拆成两个 head；每个小写符号代表一段向量：

```text
输入：A=[a1,a2]，B=[b1,b2]
重排：S1=[a1,b1]，S2=[a2,b2]
学习：Y1=FFN1(S1)，Y2=FFN2(S2)
堆叠：重复重排与独立 FFN，最后汇总打分
```

TokenMix 让每个输出都拿到所有输入 token 的一部分。FFN 的独立参数绑定在混合后的 token 位置；重排规则固定，FFN 参数通过训练学习。完整 block 还有残差和归一化。原文取 head 数等于 token 数，以保持重排前后形状一致。[原文 §3.3，式 1、3–7](https://arxiv.org/html/2507.15551v3#S3.SS3)

## 和上一期接起来

上一期比较历史状态如何传播，其中 SlimPer 还联合处理用户与候选侧信息。本期聚焦 RankMixer 对 feature tokens 的交互；独立序列模块产出的兴趣摘要，是它可以接收的一类输入。[原文 §3.2](https://arxiv.org/html/2507.15551v3#S3.SS2)

## 30 秒自测

TokenMix 本身没有可训练参数，为什么整个模型仍能学习用户和候选之间的关系？

<details markdown="1">
<summary>展开答案与证据边界</summary>

**答案：**重排把多个输入的分量放进同一个 FFN；FFN 能学习这些分量的非线性组合，输入投影等模块也可训练。“无参数”只描述重排操作。

**论文证据：**v3 §4.7 报告完整生产系统全流量部署后的 active days +0.3%、in-app duration +1.08%。收益同时包含模型与系统设计，不能全部归因于一次重排；v1 的线上数字不同，本卡固定引用 v3。[原文 §4.7](https://arxiv.org/html/2507.15551v3#S4.SS7)

**本地证据：**[历史指标](../reproductions/2507.15551-rankmixer/metrics/movielens-100k-seed42.json)只有 seed 42，属于 smoke。Shared FFN 与 Dense per-token 的 NDCG@10 分别约为 0.00196、0.01363；两组都包含 TokenMix，且参数量不同，无法据此验证 TokenMix 优于 attention，或宣称稳定提升。

本地 Sparse MoE 也没有追平 Dense；[当前路由代码](https://github.com/daiwk/auto-research/blob/main/src/auto_research/reproductions/rankmixer/model.py)与原文双 router 的 DTSI 仍有差异。本期只核验既有来源，没有新跑训练或测量生产 MFU、QPS。

</details>

## 继续查阅

[上一期：长历史要不要每层都重新计算？](001-hstu-longer-slimper.md) · [完整实现说明](../reproductions/2507.15551-rankmixer/README.md) · [学习卡片汇总](index.md)
