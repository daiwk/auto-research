# 学习卡片 001：长历史要不要每层都重新计算？

阅读预算：约 5 分钟。日期：2026-10-26。关联论文：HSTU、LONGER、SlimPer。

<p>逐篇问题库：<a href="../all/?paper=recommendation%3Ahstu">HSTU 问答</a> · <a href="../all/?paper=recommendation%3Alonger">LONGER 问答</a> · <a href="../all/?paper=recommendation%3Aslimper">SlimPer 问答</a>。</p>

## 这期只记一件事

**把“历史信息还能不能读取”和“历史表示会不会逐层更新”分开看。**

这期用同一个问题串起三篇论文：哪些历史信息仍可访问，哪些表示会继续更新，以及多个候选能共享哪部分计算。

## 三篇放在同一张图景里

| 方法 | 每层主要做什么 | 传给下一层什么 | 需要记住的取舍 |
| --- | --- | --- | --- |
| HSTU | 输入窗口内，历史 token 通过因果注意力读取更早 token | 整个窗口的 token 状态 | 保留逐层的历史间交互，历史首算较重 |
| LONGER | 首层用少量 Query 读长 K/V；后续在短序列上做 self-attention | 首层输出的短序列 | 后续不再直接读完整长 K/V，依赖首层输出承载信息 |
| SlimPer | 每层用小知识库查询用户 token 池，再做 Select–Match–Refine | 固定槽位的 user-item 知识库 | 可反复访问输入证据，但不逐层更新完整用户池 |

机制出处：[HSTU v3 §3](https://arxiv.org/html/2402.17152v3#S3)、[LONGER v1 §3.4–3.5](https://arxiv.org/html/2505.04421v1#S3.SS4)、[SlimPer v1 §2.3–2.7](https://arxiv.org/html/2607.12281v1#S2)。

## 与旧笔记相比，补上三个认识

1. **小状态不等于只看过一次历史。** SlimPer 每层还能重读用户池；LONGER 的后续层沿短状态继续计算。LONGER 还可以先做 Token Merge，因此其长 K/V 也可能已是合并后的表示。
2. **不更新完整历史，不等于完全没有历史交互。** SlimPer 的输入编码可包含局部上下文；LONGER 有组内 InnerTrans 和短序列 self-attention。它们都与 HSTU 的逐层窗口内交互不同。
3. **历史首算成本和多候选增量成本要分开。** HSTU 有 M-FALCON，LONGER 有用户侧 KV cache，SlimPer 有请求内用户 token 共享。共同前提是共享部分不能依赖当前候选；候选相关路径仍需计算。[HSTU Appendix H](https://arxiv.org/html/2402.17152v3#A8)、[LONGER §3.6.3](https://arxiv.org/html/2505.04421v1#S3.SS6.SSS3)、[SlimPer §2.4](https://arxiv.org/html/2607.12281v1#S2.SS4)

## 怎么用于判断

下面是根据计算图提出的选型假设，需要同数据、同预算实验检验：

- 若认为历史之间的多层交互很关键，先验证 HSTU 路线的价值。
- 若希望首层提取后在短序列上继续建模，关注 LONGER 的压缩与查询策略。
- 若希望小状态能多轮回看用户信息，关注 SlimPer；同时检查槽位容量是否成为瓶颈。

## 30 秒自测

同一请求要给 100 个候选打分：SlimPer 的用户 token 可以共享，为什么不能连 knowledge base 的更新结果也全部共享？

<details markdown="1">
<summary>展开答案与证据边界</summary>

**答案：**用户输入可以相同，但知识库由 item/cross 等非用户侧信息初始化；Query、匹配分数及更新后的知识库都可能随候选变化。共享用户池，只省去了可复用的那部分计算。

**论文证据：**HSTU v3 Table 7 与 LONGER v1 Table 4 报告各自完整系统的线上 A/B；SlimPer v1 §4.3 报告 Reels/Feed 全流量发布，但未披露具体线上 lift。这些不同系统的结果不能用于三篇直接排名。[HSTU](https://arxiv.org/html/2402.17152v3#S4)、[LONGER](https://arxiv.org/html/2505.04421v1#S4)、[SlimPer](https://arxiv.org/html/2607.12281v1#S4.SS3)

**本地证据：**本期只核验既有代码与历史产物，没有新跑训练。

- [HSTU 历史指标](../reproductions/2402.17152-hstu/metrics/movielens-100k-seeds42-44.json)：MovieLens-100K、3 seeds，相对匹配 SASRec 的 NDCG@10 为 −17.73%；不覆盖生产 M-FALCON。
- [LONGER 当前代码](https://github.com/daiwk/auto-research/blob/main/src/auto_research/reproductions/longer/model.py)：`encode` 拼接 global/merged/recent 后调用单层 self-attention，没有论文的首层短 Q/长 K/V 路径，也未施加 causal mask。[历史指标](../reproductions/2505.04421-longer/metrics/movielens-100k-seeds42-44.json)的 −21.37% 不能作为论文 hybrid attention 的验证；历史产物也未记录原始代码 commit。
- [SlimPer 历史指标](../reproductions/2607.12281-slimper/metrics/movielens-100k-seed42.json)：相对参数近似匹配 Transformer 的 NDCG@10 为 +1.29%，仅 seed 42 的 smoke；未实测生产 QPS 或显存。

三组基线、样本和训练预算不同，不构成统一横评。

</details>

## 继续查阅

[全部论文小卡片](all.md) · [学习卡片汇总](index.md)
