---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 从CTR到满意度与uplift：先定义监督对象，再决定怎样共享

[搜广推](../index.md) · 更新 2026-10-27 · 35 篇主题资料 / 5 篇重点对照

ESMM约束点击—转化漏斗概率，MMoE和PLE安排不同任务怎样共享专家，FLVM尝试把消费、主动参与和正负方向分开，Incrementality则比较采取与不采取动作的潜在结果。预测更多头、共享更多参数或拆出潜因子，都不自动解决因果识别。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/recommendation/feedback-multitask-causality.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：标签是条件事件、反馈测量还是潜在结果差 · 任务共享发生在哪些参数和路由上 · 观测缺失、混杂与反事实假设 · 局部机制正确与真实策略增量的证据差别

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate](../../../reproductions/1804.07931-esmm/README.md) · [原始来源](https://arxiv.org/abs/1804.07931)<br>章节：背景与主要改动、核心公式、本地复现 | 全曝光空间监督CTR和CTCVR，用p(click&amp;conversion)=pCTR·pCVR连接条件转化塔。 | 借漏斗关系缓解只在点击样本训练的选择问题和稀疏性，但未点击不是CVR条件负例；概率关系本身不证明随机干预下的增量。 |
| [Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts](../../../reproductions/kdd2018-mmoe-mmoe/README.md) · [原始来源](https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/)<br>章节：背景与主要改动、核心公式 | 一组共享experts供所有任务使用，每个任务有独立softmax gate，按样本组合专家。 | 提供灵活共享而非全独立模型，但专家仍共同承接任务梯度；门控存在不代表任务冲突或曝光偏差已经消除。 |
| [Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations](../../../reproductions/recsys2020-ple-ple/README.md) · [原始来源](https://doi.org/10.1145/3383313.3412236)<br>章节：背景与主要改动、核心公式 | 将共享专家与任务专属专家分组，CGC逐层抽取共同信息和任务特定信息。 | 专属路径有助于表达冲突任务，但增加容量与路由复杂度；是否缓解跷跷板须分任务看，不能由总体均值判定全部改善。 |
| [Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation](../../../reproductions/2609.32839-flvm/README.md) · [原始来源](https://arxiv.org/abs/2609.32839)<br>章节：背景与主要改动、核心公式、本地复现 | 三维潜因子表达消费、主动参与、正负方向；反馈头按固定稀疏语义路由，叠加停止梯度的受限基线。 | 把时长等测量因素与偏好通道分开，但该结构不自动识别真实因果偏好；原文mask未公开，本地路由是明确的可检验选择，缺失反馈也不能补零标签。 |
| [From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation](../../../reproductions/2608.10182-incrementality/README.md) · [原始来源](https://arxiv.org/abs/2608.10182)<br>章节：背景与主要改动、核心公式、复现边界 | 估计处理/不处理的潜在结果差，再按uplift及不确定度在固定触达预算下分配动作。 | 目标是动作带来的额外价值，不是高响应人群本来的结果；需要可信处理对照和识别条件，本地代理任务不能证明真实用户增量。 |

</div>

## 取舍分析 {#analysis}

### 共享机制不替代标签语义

ESMM先把CTR、条件CVR和联合CTCVR说清，MMoE与PLE再决定这些或其他任务怎样共享参数。即便换成PLE，如果把未点击一律写成条件CVR负例，训练含义仍然错误；反过来，概率链正确也不表示任务梯度不会冲突。标签定义、可观测性和网络共享必须分别审计。

对照来源：[esmm](../../../reproductions/1804.07931-esmm/README.md) · [mmoe](../../../reproductions/kdd2018-mmoe-mmoe/README.md) · [ple](../../../reproductions/recsys2020-ple-ple/README.md)

### 分离测量因素不等于证明策略增量

FLVM用受限基线和三因子路由区分观看、主动参与与正负方向，试图避免把长视频观看直接当喜欢。Incrementality要求比较同一动作有无干预时的潜在结果。前者是观测反馈的表示/测量设计，后者是反事实决策目标；更准的满意度代理仍不能替代可信对照。

对照来源：[flvm](../../../reproductions/2609.32839-flvm/README.md) · [incrementality](../../../reproductions/2608.10182-incrementality/README.md) · [esmm](../../../reproductions/1804.07931-esmm/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 把ESMM的两塔换成MMoE或PLE，是否就可以不再区分CVR与CTCVR？ {#cross-probability-chain-versus-expert-sharing}

??? note "展开答案与例子"

    **答案：** 不能。MMoE/PLE改变参数共享路径，ESMM的条件概率定义仍成立：CVR以已点击为条件，CTCVR是曝光后点击且转化的联合事件。网络再灵活也不能把两种标签混用，更不能把无点击样本直接当成条件CVR的负例。

    **教学例子：** 示意：1000次曝光有100次点击、20次转化，CTR为10%、条件CVR为20%、CTCVR为2%；换专家门控不会把这三个分母变成同一个。

    对照来源：[esmm](../../../reproductions/1804.07931-esmm/README.md) · [mmoe](../../../reproductions/kdd2018-mmoe-mmoe/README.md) · [ple](../../../reproductions/recsys2020-ple-ple/README.md)

### MMoE已经每任务独立gate，PLE为什么还要增加任务专属专家？ {#cross-gates-versus-private-paths}

??? note "展开答案与例子"

    **答案：** MMoE的gate不同，但被组合的专家仍供所有任务共享，任务梯度可能在同一组参数里冲突。PLE再划出专属专家，给任务保留不必与其他任务共用的变换路径，同时维持共享部分。这是共享边界的改变，不是保证每个任务指标都更好。

    **教学例子：** 示意：点击喜欢吸睛标题，满意度可能惩罚标题党；两个gate若仍反复调用同一专家会争改参数，专属路径允许各自保留一部分处理方式。

    对照来源：[mmoe](../../../reproductions/kdd2018-mmoe-mmoe/README.md) · [ple](../../../reproductions/recsys2020-ple-ple/README.md)

### FLVM预测某用户很喜欢内容，为什么Incrementality仍可能决定不额外触达他？ {#cross-engagement-not-incrementality}

??? note "展开答案与例子"

    **答案：** FLVM估计的是反馈背后的潜在价值方向；触达决策还要比较用户不受干预时是否本来也会消费。Incrementality在预算下看潜在结果差及不确定度，高自然偏好人群的额外收益可能很低。观测预测和因果增量对应不同问题。

    **教学例子：** 示意：用户本来有90%概率回访，触达后92%；另一人从10%到20%。前者绝对回访率高，后者的触达增量更大；数字仅为教学算例。

    对照来源：[flvm](../../../reproductions/2609.32839-flvm/README.md) · [incrementality](../../../reproductions/2608.10182-incrementality/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较esmm、mmoe、ple、flvm、incrementality，围绕标签是条件事件、反馈测量还是潜在结果差与任务共享发生在哪些参数和路由上建立分析和跨论文问答。

覆盖 35 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 35 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Statistical Learning from Attribution Sets](../../../recommendation-components/2602.06276-attribution-sets/README.md)
- [BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests](../../../reproductions/2609.08725-baff/README.md)
- [Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking](../../../recommendation-components/2610.27423-baseline-incremental/README.md)
- [CASI: Credit Assignment via Set Intervention for Agentic Retrieval](../../../reproductions/2610.20293-casi/README.md)
- [Causal Representation Learning for Generalisable Recommendation](../../../reproductions/2605.27043-causal-representation/README.md)
- [Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest](../../../reproductions/2607.14161-causal-retrieval/README.md)
- [Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations](../../../reproductions/2507.15113-click-a-buy-b/README.md)
- [Learned Cross-Task Relationships in Multi-Task Models](../../../recommendation-components/2609.28776-cross-task-relationships/README.md)
- [Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time](../../../reproductions/2406.07932-cwm/README.md)
- [DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems](../../../reproductions/2605.17863-dadf/README.md)
- [Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System](../../../reproductions/2607.12578-danet/README.md)
- [DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search](../../../reproductions/2608.25635-dceo/README.md)
- [Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation](../../../reproductions/2601.20215-easq/README.md)
- [Effective Knowledge Transfer for Multi-Task Recommendation Models](../../../reproductions/2605.05730-ektm/README.md)
- [Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate](../../../reproductions/1804.07931-esmm/README.md)
- [Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation](../../../reproductions/2609.32839-flvm/README.md)
- [Generative Pseudo-Labeling for Pre-Ranking with LLMs](../../../reproductions/2602.20995-gpl-prerank/README.md)
- [Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion](../../../recommendation-components/2610.32420-hge/README.md)
- [From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation](../../../reproductions/2608.10182-incrementality/README.md)
- [Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems](../../../reproductions/2609.25433-light-heads/README.md)
- [LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation](../../../reproductions/2608.03382-llm-ts-prior/README.md)
- [Macro Graph of Experts for Billion-Scale Multi-Task Recommendation](../../../reproductions/2506.10520-mgoe/README.md)
- [Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts](../../../reproductions/kdd2018-mmoe-mmoe/README.md)
- [Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling](../../../reproductions/2605.05855-pa-bridge/README.md)
- [PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation](../../../reproductions/2605.21752-pearl-percentile/README.md)
- [PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest](../../../reproductions/2607.22518-pinequalizer/README.md)
- [Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations](../../../reproductions/recsys2020-ple-ple/README.md)
- [Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify](../../../reproductions/2601.02306-podcast-mtl/README.md)
- [Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems](../../../reproductions/2609.34229-promptshift/README.md)
- [RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways](../../../reproductions/2607.17473-ramp/README.md)
- [Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems](../../../reproductions/2606.00282-scalr/README.md)
- [SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity](../../../reproductions/2602.09386-smes/README.md)
- [TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising](../../../reproductions/2607.25404-twice/README.md)
- [Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting](../../../reproductions/2608.04455-twitch-mor/README.md)
- [Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework](../../../reproductions/2602.12972-unimvt/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/recommendation/feedback-multitask-causality.md) · [返回全部精读卡片](../index.md)
