---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 召回覆盖从哪里来：用户表示、正例组织与负例难度

[搜广推](../index.md) · 更新 2026-10-27 · 36 篇主题资料 / 4 篇重点对照

候选生成先决定后续排序能看见什么。YouTube DNN说明单用户向量如何进入近邻检索，Airbnb EBR把监督放回搜索—浏览—预订旅程，MIMA让同请求多正例分配给互补兴趣，MDCNS改变负例的难度与多视角监督。这四种改动分别作用于表示、标签、兴趣分工和梯度，不能用召回数变大统一解释。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/recommendation/retrieval-matching.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：召回接口：单向量还是多兴趣通道 · 正例来自下一行为、旅程还是同请求集合 · 负例难度与教师监督如何改变梯度 · 固定候选预算及库存/数据替代边界

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Deep Neural Networks for YouTube Recommendations](../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/README.md) · [原始来源](https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/)<br>章节：背景与主要改动、核心公式、本地复现 | 聚合观看历史和上下文，经DNN形成用户向量，以下一视频大规模分类训练，服务时按与视频向量的点积近邻检索。 | 独立物品向量便于索引，单个用户向量需承载多种兴趣；召回阶段仍需与精排分工。本地公开小数据不等于百万级生产索引。 |
| [Applying Embedding-Based Retrieval to Airbnb Search](../../../reproductions/2601.06873-airbnb-ebr/README.md) · [原始来源](https://arxiv.org/abs/2601.06873)<br>章节：背景与主要改动、核心公式、复现边界 | 仍使用query/item内积双塔，但按搜索、浏览、预订旅程构造正例与hard negatives，并用流量replay对齐首阶段召回。 | 训练标签更贴近市场旅程，实际覆盖还受地理过滤、库存更新和索引影响；本地MovieLens代理不能验证住宿库存约束或线上收益。 |
| [MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment](../../../reproductions/2609.12842-mima/README.md) · [原始来源](https://arxiv.org/abs/2609.12842)<br>章节：背景与主要改动、核心公式、复现边界 | causal decoder产生多个兴趣，同请求多正例用一对一最优匹配监督，再以兴趣激活概率校准多通道分数。 | 排他分配抑制所有正例挤到同一兴趣，但依赖真实多正例集合及路由校准；本地相邻行为组替代同请求成交，不能直接证明生产兴趣分解。 |
| [Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation](../../../reproductions/2605.19651-mdcns/README.md) · [原始来源](https://arxiv.org/abs/2605.19651)<br>章节：背景与主要改动、核心公式、本地复现 | Self、Peer、Teacher多视角在候选池上评分，以模型分歧修正难负例排序，再把Teacher整池软分布蒸馏回Self。 | 比单一高分负例提供更多监督，但难负例仍可能是假负例，分歧也不等于标签真错；需要对齐候选池、采样预算和训练成本。 |

</div>

## 取舍分析 {#analysis}

### 先判断瓶颈在覆盖、监督还是兴趣坍缩

YouTube DNN把历史压到一个用户向量，Airbnb EBR保留类似检索接口而重新组织旅程监督；这两者不能仅凭双塔外形判成同一训练问题。MIMA的关键也不只是多输出几个向量，而是同请求多正例的一对一分配，否则多个兴趣仍可能追同一个正例。比较必须固定最终返回预算，才能分清表示改进和检索更多的收益。

对照来源：[youtube-dnn](../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/README.md) · [airbnb-ebr](../../../reproductions/2601.06873-airbnb-ebr/README.md) · [mima](../../../reproductions/2609.12842-mima/README.md)

### 难负例与多正例承担不同职责

MDCNS从未交互候选中寻找模型认为困难且有分歧的负例，让Self接收整池教师信号；MIMA则从真实正例集合学习兴趣分工。把未点击候选一律当负例，或把时间相邻行为自动当同请求互补正例，都会改变监督含义。Airbnb EBR的旅程定义提醒我们：先记录行为阶段和曝光条件，再解释损失变小意味着什么。

对照来源：[mdcns](../../../reproductions/2605.19651-mdcns/README.md) · [mima](../../../reproductions/2609.12842-mima/README.md) · [airbnb-ebr](../../../reproductions/2601.06873-airbnb-ebr/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### MIMA返回多个兴趣后Recall上升，怎样区分兴趣互补与单纯多取候选？ {#cross-more-interests-not-more-budget}

??? note "展开答案与例子"

    **答案：** 把多个通道合并去重后的总K固定，再与单向量召回比较；检查不同兴趣的正例分配和命中是否互补。MIMA的一对一监督与激活校准才是机制，YouTube DNN的单向量接口是比较起点。若每个兴趣都额外拿K个候选，覆盖上升不能单独归功于兴趣建模。

    **教学例子：** 示意：跑步与摄影两个通道各取50条，合并后固定100条；应与单通道100条比较，不能与单通道50条比较后宣称兴趣翻倍有效。

    对照来源：[mima](../../../reproductions/2609.12842-mima/README.md) · [youtube-dnn](../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/README.md)

### 为什么Airbnb EBR和MDCNS都强调负例，却不能直接把模型最高分的未点击项当最好的负例？ {#cross-hard-negative-is-not-ground-truth}

??? note "展开答案与例子"

    **答案：** Airbnb的难负例要放在搜索旅程和行为阶段中解释，MDCNS再用多视角分歧避免只追Self偏好。未点击可能来自未充分曝光、替代关系或标注缺失；最高分只表示当前模型认为相近，不保证它确实无关。应同时控制假负例、多样性及采样预算。

    **教学例子：** 示意：用户只预订了一家房，另两家同样合适但已满房。把这两家当绝对无关负例，会把库存结果错误写成语义偏好。

    对照来源：[airbnb-ebr](../../../reproductions/2601.06873-airbnb-ebr/README.md) · [mdcns](../../../reproductions/2605.19651-mdcns/README.md)

### 精排更强为什么仍补不回召回漏掉的兴趣，换训练目标又能改变哪一步？ {#cross-recall-versus-ranking-boundary}

??? note "展开答案与例子"

    **答案：** 精排只在已有候选中排序，无法创造未入池物品。YouTube DNN明确分开召回与精排，MIMA用多正例分工改变哪些兴趣能提出候选，MDCNS改变检索表征接收的负例梯度。三者应分别检查候选覆盖、固定K质量和后续排序，不能只看最终点击就定位瓶颈。

    **教学例子：** 示意：100个候选全是跑鞋时，精排无法展示相机；多兴趣召回先提名相机，精排才有机会比较它与跑鞋的当前价值。

    对照来源：[youtube-dnn](../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/README.md) · [mima](../../../reproductions/2609.12842-mima/README.md) · [mdcns](../../../reproductions/2605.19651-mdcns/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较youtube-dnn、airbnb-ebr、mima、mdcns，围绕召回接口：单向量还是多兴趣通道与正例来自下一行为、旅程还是同请求集合建立分析和跨论文问答。

覆盖 36 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 36 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Applying Embedding-Based Retrieval to Airbnb Search](../../../reproductions/2601.06873-airbnb-ebr/README.md)
- [Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro](../../../reproductions/2609.05063-allecompanion/README.md)
- [ASARL: Autonomous Social-Aware Relevance Learning for QQ Search](../../../reproductions/2607.26593-asarl/README.md)
- [Large Language Model based Long-tail Query Rewriting in Taobao Search](../../../reproductions/2311.03758-beque/README.md)
- [CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval](../../../reproductions/2602.12564-capts/README.md)
- [Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval](../../../reproductions/2607.00448-cluster-goobs/README.md)
- [CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search](../../../reproductions/2607.24417-core-relevance/README.md)
- [From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance](../../../reproductions/2510.11056-crsd/README.md)
- [CS3: Efficient Online Capability Synergy for Two-Tower Recommendation](../../../reproductions/2604.19269-cs3/README.md)
- [Multilingual Semantic Retrieval for Apple Music Search](../../../reproductions/2607.10239-elise/README.md)
- [Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling](../../../reproductions/2608.27413-friend-gnn/README.md)
- [GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce](../../../reproductions/2603.19665-genfacet/README.md)
- [Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking](../../../reproductions/2603.03770-hap/README.md)
- [HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval](../../../reproductions/2605.23572-harness-lm/README.md)
- [Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation](../../../reproductions/2604.12965-hill-index/README.md)
- [LLM Retrieval for Stable and Predictable Ad Recommendations](../../../reproductions/2605.21969-llm-ad-retrieval/README.md)
- [Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation](../../../reproductions/2605.19651-mdcns/README.md)
- [Melo: A Production LLM-Powered Music Recommendation Agent](../../../reproductions/2607.23718-melo/README.md)
- [MESH: Scaling Up Retrieval with Heterogeneous Content Unification](../../../reproductions/2607.12392-mesh/README.md)
- [Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System](../../../reproductions/2602.16124-mfli/README.md)
- [MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment](../../../reproductions/2609.12842-mima/README.md)
- [MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever](../../../reproductions/2508.20400-mpformer/README.md)
- [MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling](../../../reproductions/2609.23677-muser/README.md)
- [NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model](../../../reproductions/2607.24789-next-vlm/README.md)
- [OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval](../../../reproductions/2607.27475-oneshot-index/README.md)
- [PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn](../../../recommendation-components/2610.30941-pair/README.md)
- [Policy-Grounded Dynamic Facet Suggestions for Job Search](../../../reproductions/2605.16479-policy-facet/README.md)
- [RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation](../../../reproductions/2606.18379-rankgraph2/README.md)
- [RPTune: Learned Context Curation for LLM Catalog Search](../../../reproductions/2610.00964-rptune/README.md)
- [SetMIR: Multi-Interest Retrieval as Set Prediction](../../../reproductions/2608.30251-setmir/README.md)
- [LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising](../../../reproductions/2610.14550-snap-dpa-relevance/README.md)
- [SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search](../../../reproductions/2608.01738-spear/README.md)
- [ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants](../../../reproductions/2606.08466-toolrec/README.md)
- [TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation](../../../reproductions/2608.25528-transretrieval/README.md)
- [Deep Neural Networks for YouTube Recommendations](../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/README.md)
- [ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation](../../../reproductions/2607.10910-zorro/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/recommendation/retrieval-matching.md) · [返回全部精读卡片](../index.md)
