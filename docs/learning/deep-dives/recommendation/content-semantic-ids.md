---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 知识、协同向量与语义码：相同内容怎样进入不同推荐接口？

[搜广推](../index.md) · 更新 2026-10-27 · 60 篇主题资料 / 4 篇重点对照

KAR生成外部知识后适配既有推荐器，NoteLLM用共读监督训练可检索压缩状态，Dual-purpose SID让短码兼顾身份与内容重建，FineSID则保留细粒度token和完整交互骨干做阶段迁移。它们不只是“都用LLM或SID”：对齐信号、压缩对象与下游继承内容各不相同。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/recommendation/content-semantic-ids.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：输入知识来自生成常识、内容还是交互关系 · 传递对象是向量、短码还是完整预测器状态 · 内容重建与个性化目标如何共同约束 · 离线缓存、冷启动与完整复现边界

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models](../../../reproductions/2306.10933-kar/README.md) · [原始来源](https://arxiv.org/abs/2306.10933)<br>章节：背景与主要改动、核心公式、本地复现 | 分别生成用户偏好推理知识和物品事实知识，以hybrid-expert adapter压缩，再与原ID表示一起送入推荐模型。 | 可预生成知识以移出在线自回归成本，但生成描述不是真实偏好标签，缓存也有刷新与事实核验成本；并非LLM直接在线做全部推荐。 |
| [NoteLLM: A Retrievable Large Language Model for Note Recommendation](../../../reproductions/2403.01744-notellm/README.md) · [原始来源](https://arxiv.org/abs/2403.01744)<br>章节：背景与主要改动、核心公式、本地复现 | compression prompt把内容压到特殊token状态，GCL用共读关系学习检索空间，CSFT从同一状态生成hashtag/category。 | 协同对比与生成监督共同塑造表示，仍需处理共读关系的曝光偏差；内容相似和行为互补并非天然相同，生成能力也不能只凭检索分数推断。 |
| [Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems](../../../reproductions/2607.24865-dual-sid/README.md) · [原始来源](https://arxiv.org/abs/2607.24865)<br>章节：背景与主要改动、核心公式、复现边界 | 层次SID承载协同身份，并通过SiDec从各层离散码重建内容embedding，供召回、排序和低I/O重建使用。 | 短码与重建降低内容传输需求，也引入量化碰撞和信息瓶颈；重建MSE与最终推荐必须分测。本地genre替代多模态内容，未复刻生产码本与在线重建。 |
| [Progressive Learning from Content to Relevance to Personalization for CTR Prediction](../../../recommendation-components/2610.29138-finesid/README.md) · [原始来源](https://arxiv.org/abs/2610.29138v1)<br>章节：背景与主要改动、三阶段结构、成本判定：不执行复现 | 保留多尺度视觉/字段文本token，先训练完整query-item相关性预测器，再保留共享dense、embedding与归一化状态并切换CTR头。 | 迁移对象比单个embedding丰富，但要求阶段一致的骨干和状态管理；不等于只接SID lookup。本库仅方法及线上证据收录，成本过高未实现完整训练。 |

</div>

## 取舍分析 {#analysis}

### 先问传过去的是什么

KAR传递的是生成知识经adapter得到的特征，NoteLLM传递协同训练过的压缩向量，Dual-purpose SID传递可重建内容的离散身份，FineSID则连交互预测器的共享参数与归一化状态一起迁移。若只给既有CTR模型加一张随机码表，既没有KAR的知识来源，也没有FineSID的阶段继承，不能凭接口同为token就视作等价。

对照来源：[kar](../../../reproductions/2306.10933-kar/README.md) · [notellm](../../../reproductions/2403.01744-notellm/README.md) · [dual-sid](../../../reproductions/2607.24865-dual-sid/README.md) · [finesid](../../../recommendation-components/2610.29138-finesid/README.md)

### 内容保真与推荐相关性需要两把尺

Dual-purpose SID的内容重建项检验码里能还原多少embedding，NoteLLM的GCL则用共读关系调整哪些内容应相近；二者约束的几何不同。FineSID再用相关性软目标和个性化CTR分阶段训练同一骨干。更低重建误差不自动带来更好的点击排序，LLM说得更像也不等于用户更喜欢。

对照来源：[dual-sid](../../../reproductions/2607.24865-dual-sid/README.md) · [notellm](../../../reproductions/2403.01744-notellm/README.md) · [finesid](../../../recommendation-components/2610.29138-finesid/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### Dual-purpose SID和FineSID都用离散token，为什么不能用同一个SID lookup实验同时证明两篇？ {#cross-same-token-different-transfer}

??? note "展开答案与例子"

    **答案：** Dual-purpose SID要求短码同时服务协同身份与内容重建；FineSID还要求细粒度、多尺度位置保留，并把相关性阶段的完整共享预测器迁移到CTR。单个lookup只能覆盖接口的一小部分，缺少各自重建目标或阶段继承，就没有验证其定义性机制。

    **教学例子：** 示意：给鞋图分配三个码后能还原大致内容，是一个压缩问题；先学query—鞋图相关性，再继承整套交互网络预测某用户点击，是另一条训练链路。

    对照来源：[dual-sid](../../../reproductions/2607.24865-dual-sid/README.md) · [finesid](../../../recommendation-components/2610.29138-finesid/README.md)

### KAR生成的偏好描述为什么不能替代NoteLLM使用的共读监督？ {#cross-generated-knowledge-not-click-label}

??? note "展开答案与例子"

    **答案：** KAR提供常识和偏好推理的候选知识，是否有用还要由推荐目标学习；NoteLLM的共读pair来自行为关系，直接约束检索空间。前者可能补足日志没有的语义，也可能生成错误解释；后者有真实交互依据，却受曝光和流行度影响。两种信号可互补，不能互当真值。

    **教学例子：** 示意：LLM说露营者可能喜欢登山鞋，只是一条知识假设；用户实际常把某双鞋与防水袜一起阅读，则是平台行为关系，二者证据性质不同。

    对照来源：[kar](../../../reproductions/2306.10933-kar/README.md) · [notellm](../../../reproductions/2403.01744-notellm/README.md)

### SID重建更准确、文本生成更流畅，为什么推荐NDCG仍可能下降？ {#cross-reconstruction-versus-preference}

??? note "展开答案与例子"

    **答案：** 重建保留内容，CSFT保留生成接口，但排序还需要用户—物品的协同区分。Dual-purpose SID码本可能更偏重内容而牺牲偏好，NoteLLM要靠GCL补充行为几何，FineSID则继续训练个性化CTR。应分别看重建、碰撞、相关性和隔离测试排序，不能把某一辅助目标当最终效果。

    **教学例子：** 示意：两件外观近似的外套被重建得很准，但一个适合骑行、一个适合通勤；若码没有保留用户群差异，视觉保真并不能保证点击次序正确。

    对照来源：[dual-sid](../../../reproductions/2607.24865-dual-sid/README.md) · [notellm](../../../reproductions/2403.01744-notellm/README.md) · [finesid](../../../recommendation-components/2610.29138-finesid/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较kar、notellm、dual-sid、finesid，围绕输入知识来自生成常识、内容还是交互关系与传递对象是向量、短码还是完整预测器状态建立分析和跨论文问答。

覆盖 60 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 60 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale](../../../reproductions/2604.23522-adasid/README.md)
- [AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation](../../../reproductions/2610.01705-agent-web-rec/README.md)
- [From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs](../../../reproductions/2605.23310-akt-rec/README.md)
- [Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations](../../../reproductions/2606.10357-atomic-intent/README.md)
- [Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors](../../../reproductions/2403.19347-bahe/README.md)
- [CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval](../../../reproductions/2608.30255-camie/README.md)
- [ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning](../../../reproductions/2608.10187-connectionmind/README.md)
- [Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music](../../../reproductions/2603.28994-cross-domain-kd/README.md)
- [Douyin Multimodal Embedding Model Technical Report](../../../reproductions/2608.02148-dme/README.md)
- [DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan](../../../reproductions/2602.04460-dos/README.md)
- [Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems](../../../reproductions/2607.24865-dual-sid/README.md)
- [From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation](../../../reproductions/2608.21012-dynamic-codebook/README.md)
- [FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation](../../../reproductions/2502.16924-filterllm/README.md)
- [Progressive Learning from Content to Relevance to Personalization for CTR Prediction](../../../recommendation-components/2610.29138-finesid/README.md)
- [FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation](../../../reproductions/2605.21832-fluid/README.md)
- [Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation](../../../reproductions/2606.20554-g2rec/README.md)
- [GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System](../../../reproductions/2607.29213-gala/README.md)
- [GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation](../../../reproductions/2603.22916-gatesid/README.md)
- [Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)](../../../reproductions/2610.01533-gris/README.md)
- [IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs](../../../reproductions/2603.01590-idproxy/README.md)
- [Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models](../../../reproductions/2306.10933-kar/README.md)
- [Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation](../../../reproductions/2608.02738-kgd/README.md)
- [KuaFu: Compressing Long User Behavior into Understanding at Billion Scale](../../../reproductions/2609.31045-kuafu/README.md)
- [L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation](../../../reproductions/2605.26717-l2rec/README.md)
- [Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application](../../../reproductions/2405.03988-learn/README.md)
- [A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation](../../../reproductions/2403.13574-lsvcr/README.md)
- [Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model](../../../reproductions/2502.08309-lum/README.md)
- [LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation](../../../reproductions/2605.18771-lwgr/README.md)
- [M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems](../../../reproductions/2205.08084-m6rec/README.md)
- [Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations](../../../reproductions/2604.18146-marc/README.md)
- [MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling](../../../reproductions/2502.00321-mim/README.md)
- [A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems](../../../reproductions/2605.09338-mm-llm/README.md)
- [Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta](../../../reproductions/2607.24015-mosaic/README.md)
- [Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction](../../../reproductions/2412.06860-msd/README.md)
- [MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music](../../../reproductions/2605.27103-muchator/README.md)
- [Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery](../../../reproductions/2609.23877-music-rationales/README.md)
- [Multimedia Asset Personalization via Multimodal Embeddings at Netflix](../../../reproductions/2608.18322-netflix-mediafm/README.md)
- [NoteLLM: A Retrievable Large Language Model for Note Recommendation](../../../reproductions/2403.01744-notellm/README.md)
- [Building a User Foundation Model for the Open Web](../../../reproductions/2607.28019-open-web-ufm/README.md)
- [Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations](../../../reproductions/sigir2026-pin-scale-pin-scale/README.md)
- [PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest](../../../reproductions/2603.03544-pinclip/README.md)
- [Fine-Tuned LLM as a Complementary Predictor Improving Ads System](../../../reproductions/2605.27856-pinterest-ads-llm/README.md)
- [PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation](../../../reproductions/2602.08530-pit/README.md)
- [PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information](../../../reproductions/2412.06308-precise/README.md)
- [Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb](../../../reproductions/2607.12246-proximity-features/README.md)
- [Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale](../../../reproductions/2603.00632-quasid/README.md)
- [RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation](../../../reproductions/2607.15730-recap/README.md)
- [RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation](../../../reproductions/2605.04726-recgpt-mobile/README.md)
- [RecGPT-V2 Technical Report](../../../reproductions/2512.14503-recgpt-v2/README.md)
- [RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation](../../../reproductions/2607.25901-reco-reward/README.md)
- [RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction](../../../reproductions/2602.12593-rq-gmm/README.md)
- [SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking](../../../reproductions/2602.09401-sarm/README.md)
- [SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation](../../../reproductions/2508.01375-saviorrec/README.md)
- [Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models](../../../reproductions/2502.13539-seral/README.md)
- [SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search](../../../reproductions/2604.10471-sid-coord/README.md)
- [Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search](../../../recommendation-components/2610.26105-sid-topology/README.md)
- [SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control](../../../reproductions/2609.11752-sirf/README.md)
- [SSRLive: Live Streaming Recommendation with Dynamic Semantic ID](../../../reproductions/2606.06970-ssrlive/README.md)
- [TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation](../../../reproductions/2603.21481-tagllm/README.md)
- [TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems](../../../reproductions/2606.25147-tokenminds/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/recommendation/content-semantic-ids.md) · [返回全部精读卡片](../index.md)
