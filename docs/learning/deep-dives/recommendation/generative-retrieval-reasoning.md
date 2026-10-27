---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 生成一个物品，先后跨过码本、模型分布与合法目录三道关

[搜广推](../index.md) · 更新 2026-10-27 · 60 篇主题资料 / 5 篇重点对照

TIGER把物品变成层次码并学习下一码序列，COBRA在稀疏码后补回条件稠密向量，PLUM把已有LLM通过继续预训练接到行为/SID空间。STATIC不改表示而改变合法解码的执行方式，Reward Guided Decoding则在既有支持上倾斜业务偏好。先定位改变的是哪一关，再判断它能否找回漏掉的物品。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/recommendation/generative-retrieval-reasoning.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：物品表示：离散码、稀疏—稠密级联与LLM继续预训练 · 学习分布与推理搜索分别改变什么 · 合法目录约束与业务reward的区别 · 先验支持、beam预算和本地缩比证据

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Recommender Systems with Generative Retrieval](../../../reproductions/2305.05065-tiger/README.md) · [原始来源](https://arxiv.org/abs/2305.05065)<br>章节：背景与主要改动、核心公式、本地复现 | RQ-VAE逐层量化内容残差，加碰撞消解token形成物品SID，encoder-decoder自回归预测下一物品码序列。 | 共享语义前缀便于参数共享，但码本碰撞和早期路径错误会影响可达性。本地按有效物品ID累加token log-prob评分，不能将其等同生产beam吞吐。 |
| [Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations](../../../reproductions/2503.02453-cobra/README.md) · [原始来源](https://arxiv.org/abs/2503.02453)<br>章节：背景与主要改动、核心公式、本地复现 | 先生成稀疏code，再以该code和历史为条件生成dense query，beam code分数与dense相似度级联召回。 | 为量化丢失的细节增加区分通道，也引入稠密索引、融合权重和两阶段预算；若目标code根本未进入beam，后段dense通常无从补回。 |
| [PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations](../../../reproductions/2510.07784-plum/README.md) · [原始来源](https://arxiv.org/abs/2510.07784)<br>章节：背景与主要改动、核心公式、本地结果 | 从已有MoE LLM初始化，以行为和视频元数据CPT对齐，再做next-SID召回；SID-v2同时约束重建、量化和共现。 | 容量从大型ID表转向可扩展主干，但依赖CPT配方和预训练资源。线上生成SID不用点积索引，不代表没有SID映射、目录维护与解码成本。 |
| [Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md) · [原始来源](https://arxiv.org/abs/2602.22647)<br>章节：背景与主要改动、核心公式、结果与边界 | 将合法token路径编成加速器内CSR迁移，先全词表log-softmax，再非法项置负无穷，并同步维护beam前缀和node状态。 | 改变约束执行的成本与合法性，不会创造模型未学到的偏好；不能在每个合法子集重新归一化后还声称保持同一条原模型路径分数。 |
| [Reward Guided Decoding for Generative Recommendation](../../../reproductions/2607.25344-reward-guided-decoding/README.md) · [原始来源](https://arxiv.org/abs/2607.25344)<br>章节：背景与主要改动、核心公式、复现边界 | 固定生成先验P0，用exp(R/β)倾斜得到Q，以KL温度限制偏离，不重新训练生成器。 | reward可重排既有支持，却不能令P0为零的路径凭空出现；代理reward和线上价值不同，本地MovieLens构造任务不等于生产收益。 |

</div>

## 取舍分析 {#analysis}

### 先看物品能否到达，再看排名是否正确

TIGER和PLUM先决定物品怎样映射到SID以及每步码的概率；COBRA再在已提名的稀疏区域内补细节。若码碰撞没有消解、前缀被错误排除或合法目录缺失，单纯扩大reward权重无法恢复目标。应把token预测、有效物品覆盖和最终排序分别测量，beam变宽也不能证明码本更好。

对照来源：[tiger](../../../reproductions/2305.05065-tiger/README.md) · [plum](../../../reproductions/2510.07784-plum/README.md) · [cobra](../../../reproductions/2503.02453-cobra/README.md) · [reward-guided-decoding](../../../reproductions/2607.25344-reward-guided-decoding/README.md)

### 合法性与偏好不是同一个分数

STATIC回答某前缀下哪些token能通向合法目录，Reward Guided Decoding回答在允许的分布中怎样偏向reward。前者的非法负无穷是可行域，后者的指数倾斜是软偏好；把库存违规只当有限惩罚，仍可能选出高reward的非法项。约束编译、原模型概率和业务价值应保留各自语义。

对照来源：[static-constraint-decoding](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md) · [reward-guided-decoding](../../../reproductions/2607.25344-reward-guided-decoding/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### COBRA多了dense向量后，为什么仍不能保证找回TIGER式早期码路径里漏掉的物品？ {#cross-dense-cannot-recover-pruned-code}

??? note "展开答案与例子"

    **答案：** COBRA的dense query以稀疏code为条件，通常在beam已提名的区域内细排；目标code若未进入搜索，后段并不自动遍历全部遗漏区域。它补的是量化后同区域的细粒度区分，不能把级联后段当成无条件召回修复器。

    **教学例子：** 示意：第一层beam只保留跑鞋类，摄影类整支被剪掉；即使跑鞋类的dense排序完美，也不会突然召回相机。

    对照来源：[cobra](../../../reproductions/2503.02453-cobra/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

### STATIC的合法路径掩码和Reward Guided Decoding的高reward，冲突时应该怎样理解？ {#cross-legal-mask-and-reward-tilt}

??? note "展开答案与例子"

    **答案：** 合法掩码先定义哪些结果允许出现，reward只在可行结果间表达偏好。指数倾斜仍乘原先验，先验或掩码给零支持的结果不能因reward高而复活。若把约束改成有限扣分，就变成了另一个允许违规被补偿的优化问题。

    **教学例子：** 示意：库存为零的商品本来预测收益很高，仍应被合法目录排除；不能靠把它的收益减一点就假定永远不会被选中。

    对照来源：[static-constraint-decoding](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md) · [reward-guided-decoding](../../../reproductions/2607.25344-reward-guided-decoding/README.md)

### TIGER和PLUM都预测SID，为什么不能只比较同一个next-token loss就判断训练路线相同？ {#cross-same-sid-not-same-training}

??? note "展开答案与例子"

    **答案：** TIGER从内容量化与序列生成建立链路；PLUM还继承LLM并通过行为、文本/ASR等混合CPT对齐语言与协同空间，SID-v2本身也加入共现和渐进深度重建。相同目标接口不代表初始化、数据与表示训练相同，比较效果需固定评估目录和预算。

    **教学例子：** 示意：两模型都预测三层码，一个只学行为序列，另一个先看元数据与行为混合语料；最后一层交叉熵的名称相同，并没有抹去前面的训练差异。

    对照来源：[tiger](../../../reproductions/2305.05065-tiger/README.md) · [plum](../../../reproductions/2510.07784-plum/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较tiger、cobra、plum、static-constraint-decoding、reward-guided-decoding，围绕物品表示：离散码、稀疏—稠密级联与LLM继续预训练与学习分布与推理搜索分别改变什么建立分析和跨论文问答。

覆盖 60 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 60 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation](../../../reproductions/2603.19710-aigq/README.md)
- [One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations](../../../reproductions/2609.18296-angle/README.md)
- [Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation](../../../reproductions/2607.21028-barge/README.md)
- [Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following](../../../reproductions/2602.13581-climber-pilot/README.md)
- [Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations](../../../reproductions/2503.02453-cobra/README.md)
- [Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL](../../../reproductions/2605.14434-cq-sid/README.md)
- [DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation](../../../reproductions/2602.09744-diffureason/README.md)
- [DualGR: Generative Retrieval with Long and Short-Term Interests Modeling](../../../reproductions/2511.12518-dualgr/README.md)
- [EGR: Embedding-Native Generative Retrieval with a Shared LLM](../../../reproductions/2607.23038-egr/README.md)
- [From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation](../../../reproductions/2607.27789-feedback-policy/README.md)
- [Generative End-to-end Ad Retrieval at Douyin](../../../reproductions/2609.39327-gear/README.md)
- [GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation](../../../reproductions/2604.14878-genrec/README.md)
- [Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify](../../../reproductions/2603.17540-glide/README.md)
- [Generative Recommendation for Large-Scale Advertising](../../../reproductions/2602.22732-gr4ad/README.md)
- [Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation](../../../reproductions/2602.23639-grc/README.md)
- [Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search](../../../reproductions/2605.17994-growthgr/README.md)
- [GRP v0.1 Technical Report](../../../reproductions/2609.36688-grp/README.md)
- [Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation](../../../reproductions/2608.06213-gryphon-v2/README.md)
- [Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap](../../../reproductions/2607.26073-guess-where-you-go/README.md)
- [Hierarchical Residual Policy Optimization for Generative Recommendations](../../../reproductions/2608.00750-hrpo/README.md)
- [IntSR: An Integrated Generative Framework for Search and Recommendation](../../../reproductions/2509.21179-intsr/README.md)
- [LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System](../../../reproductions/2411.13789-leadre/README.md)
- [MBGR: Multi-Business Generative Recommendation](../../../reproductions/2604.02684-mbgr/README.md)
- [OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models](../../../recommendation-components/2610.30675-onelatent/README.md)
- [OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce](../../../reproductions/2601.21770-onemall/README.md)
- [OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation](../../../reproductions/2603.02999-oneranker/README.md)
- [OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment](../../../reproductions/2502.18965-onerec/README.md)
- [OneRec-V2 Technical Report](../../../reproductions/2508.20900-onerec-v2/README.md)
- [OxygenREC-v2: Internalizing Discrimination into Generative Recommendation](../../../reproductions/2607.24255-oxygenrec-v2/README.md)
- [PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems](../../../reproductions/2504.10507-pinrec/README.md)
- [PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations](../../../reproductions/2510.07784-plum/README.md)
- [PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations](../../../reproductions/2601.04674-promise/README.md)
- [PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation](../../../reproductions/2608.07989-pushdualgen/README.md)
- [From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark](../../../reproductions/2605.25514-qgs/README.md)
- [Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale](../../../reproductions/2606.25496-rag-generation/README.md)
- [Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment](../../../reproductions/2602.01023-rag-qac/README.md)
- [RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation](../../../reproductions/2603.28124-rclrec/README.md)
- [RecGPT-V3 Technical Report](../../../reproductions/2607.15591-recgpt-v3/README.md)
- [Reward Guided Decoding for Generative Recommendation](../../../reproductions/2607.25344-reward-guided-decoding/README.md)
- [RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems](../../../reproductions/2602.12968-rgalign-rec/README.md)
- [Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning](../../../reproductions/2602.13134-rolegen/README.md)
- [S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage](../../../reproductions/2602.10606-s-grec/README.md)
- [S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation](../../../reproductions/2601.18664-s2gr/README.md)
- [SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation](../../../reproductions/2502.10157-sessionrec/README.md)
- [SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress](../../../reproductions/2602.22913-sigma/README.md)
- [LLM-Based Generative Retrieval for Snapchat Content Recommendation](../../../reproductions/2607.28895-snaplgr/README.md)
- [Sona Technical Report](../../../reproductions/2608.11015-sona/README.md)
- [SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs](../../../recommendation-components/2610.27898-spar-prefix-balance/README.md)
- [Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md)
- [TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising](../../../reproductions/2608.24034-tagr/README.md)
- [TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning](../../../reproductions/2609.00986-tgr/README.md)
- [Recommender Systems with Generative Retrieval](../../../reproductions/2305.05065-tiger/README.md)
- [TSGR: Taobao Search Generative Retrieval](../../../reproductions/2607.18796-tsgr/README.md)
- [UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation](../../../reproductions/2609.23718-unique/README.md)
- [Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence](../../../reproductions/2607.24439-unir2/README.md)
- [UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute](../../../reproductions/2604.12234-unirec-coa/README.md)
- [UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation](../../../reproductions/2610.16132-unisgr-v2/README.md)
- [Unified Value Alignment for Generative Recommendation in Industrial Advertising](../../../reproductions/2605.05803-univa/README.md)
- [WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat](../../../reproductions/2610.16979-wegr/README.md)
- [X-Rec Technical Report](../../../reproductions/2609.29180-xrec/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/recommendation/generative-retrieval-reasoning.md) · [返回全部精读卡片](../index.md)
