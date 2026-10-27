---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# DIN、HSTU、LONGER、SlimPer、RankMixer：究竟让谁与谁交互？

[搜广推](../index.md) · 更新 2026-10-27 · 73 篇主题资料 / 5 篇重点对照

比较排序骨干前先画三条边：历史到历史、候选到历史、字段到字段。DIN按候选激活历史，HSTU在输入窗口内逐层改写历史状态，LONGER先合并再以短查询读长KV，SlimPer反复读取用户池但只传播小知识库，RankMixer则更换异构字段交互。它们可处于同一流水线的不同位置，不能按一个长度变量或一张本地结果表排总名次。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/recommendation/history-ranking-backbones.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：交互对象：历史内部、目标读取还是字段混合 · 每层传播的状态及原始历史是否持续可读 · 候选依赖如何限制用户缓存共享 · 复杂度变量与本地/生产证据的适用范围

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Deep Interest Network for Click-Through Rate Prediction](../../../reproductions/1706.06978-din/README.md) · [原始来源](https://arxiv.org/abs/1706.06978)<br>章节：背景与主要改动、核心公式 | 候选q与每条历史行为计算local activation，再池化出目标相关兴趣；不是先构造一个对全部候选相同的最终用户兴趣。 | 目标相关性直接，但每个候选需要自己的激活/聚合；当前所述主路径不建立HSTU式逐层历史—历史交互。 |
| [Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations](../../../reproductions/2402.17152-hstu/README.md) · [原始来源](https://arxiv.org/abs/2402.17152)<br>章节：背景与主要改动、核心公式、本地复现 | 输入窗口内历史token经因果pointwise聚合、post-pooling normalization和U gate逐层更新，保留历史内部依赖。 | 去softmax不使全配对交互自动变线性。原论文M-FALCON可复用候选无关历史KV，但目标侧查询/输出仍相关；本地尚未实现M-FALCON，不能把这种复用当作已实测能力。 |
| [LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders](../../../reproductions/2505.04421-longer/README.md) · [原始来源](https://arxiv.org/abs/2505.04421)<br>章节：背景与主要改动、核心公式、本地复现 | 相邻行为先Token Merge；首层少量global/recent queries读长KV，输出长度跟随query，后续只在短输出上继续self-attention。 | 合并与短query压缩是两步，可能牺牲细粒度地址；合并还增加宽度/投影成本，收益有条件。本地当前仅实现InnerTrans/聚合后的普通self-attention，未实现论文首层短Q/长KV cross-causal attention及causal mask；旧指标不能验证该核心路径或缓存吞吐。 |
| [SlimPer: Make Personalization Model Slim and Smart](../../../reproductions/2607.12281-slimper/README.md) · [原始来源](https://arxiv.org/abs/2607.12281)<br>章节：背景与主要改动、核心公式、复现边界 | 候选相关的固定槽位知识库逐层Select–Match–Refine，每层重新读取共享用户token池，层间传播小KB而非全历史隐状态。 | 用户池仍随历史长度增长，初始编码可有局部上下文交互；共享的是候选无关用户编码，不是不同候选的最终KB。本地短历史没有验证生产长序列QPS。 |
| [RankMixer: Scaling Up Ranking Models in Industrial Recommenders](../../../reproductions/2507.15551-rankmixer/README.md) · [原始来源](https://arxiv.org/abs/2507.15551)<br>章节：背景与主要改动、核心公式、本地复现 | 异构feature tokens按head/token做固定重排，输出位置各有独立FFN；用不同分量相遇后学习组合，替代字段交互中的attention。 | token数与head/宽度约束必须匹配；这不禁止上游历史模块使用attention，也不自动处理超长行为压缩。Sparse路由和本地实现状态需另看，不能泛化全模型无attention。 |

</div>

## 取舍分析 {#analysis}

### 先比层间状态，再比算量

HSTU沿输入窗口逐层更新历史，LONGER首层之后沿短query输出继续，SlimPer则让原始用户池一直可读但只传递小KB。三者节省或保留的对象不同：没有全长层间状态不代表没有全历史读取，没有softmax也不代表没有历史两两配对。DIN的目标聚合和RankMixer的字段混合更不应直接塞进同一张N²对N表。

对照来源：[hstu](../../../reproductions/2402.17152-hstu/README.md) · [longer](../../../reproductions/2505.04421-longer/README.md) · [slimper](../../../reproductions/2607.12281-slimper/README.md) · [din](../../../reproductions/1706.06978-din/README.md) · [rankmixer](../../../reproductions/2507.15551-rankmixer/README.md)

### “用户侧”这个名字不能保证跨候选复用

DIN的兴趣池化已读取候选；SlimPer的KB从item/cross信息出发，不能把候选A精炼后的KB交给B。HSTU的M-FALCON和LONGER的用户KV复用则要求共享路径尚未混入目标依赖。RankMixer常在后段混合候选、序列摘要和字段，其最终状态同样不是天然可复用的用户缓存。依赖方向比模块命名更可靠。

对照来源：[din](../../../reproductions/1706.06978-din/README.md) · [slimper](../../../reproductions/2607.12281-slimper/README.md) · [hstu](../../../reproductions/2402.17152-hstu/README.md) · [longer](../../../reproductions/2505.04421-longer/README.md) · [rankmixer](../../../reproductions/2507.15551-rankmixer/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### LONGER和SlimPer都压缩状态，为什么“压完一次后再也不看长历史”只符合其中部分路径？ {#cross-which-history-remains-readable}

??? note "展开答案与例子"

    **答案：** LONGER首层用短query读长KV，之后主要沿该短输出继续；SlimPer每层的小KB都重新查询用户token池，原始证据并未在第一层后退出。HSTU则逐层更新窗口内历史。比较应问各层还能访问什么，而不是把三者都叫短序列压缩。

    **教学例子：** 示意：第一层没注意到三年前的园艺行为，SlimPer后层仍可再次查询用户池；LONGER后续短序列里若没保留这条证据，就不能把它当全长历史重新读取。

    对照来源：[longer](../../../reproductions/2505.04421-longer/README.md) · [slimper](../../../reproductions/2607.12281-slimper/README.md) · [hstu](../../../reproductions/2402.17152-hstu/README.md)

### 同一个用户评分100个候选时，DIN的兴趣、SlimPer的KB和HSTU历史KV能否一起缓存一次？ {#cross-candidate-dependent-cache}

??? note "展开答案与例子"

    **答案：** 不能一概而论。DIN兴趣依赖候选，SlimPer最终KB也依赖候选；可共享的是它们尚未读目标的基础编码。HSTU在M-FALCON约束下能复用候选无关历史KV，但每个目标仍需自身查询与输出。缓存条件是依赖不变，不能用同一用户作充分条件。

    **教学例子：** 示意：猫粮候选使KB聚焦养猫记录，园艺工具候选应读种花记录；把猫粮KB原样复用给园艺工具，会把一次目标选择当成用户的通用状态。

    对照来源：[din](../../../reproductions/1706.06978-din/README.md) · [slimper](../../../reproductions/2607.12281-slimper/README.md) · [hstu](../../../reproductions/2402.17152-hstu/README.md)

### RankMixer不用attention做交互，为什么仍能和LONGER或HSTU放在同一模型里？ {#cross-field-mixing-not-history-replacement}

??? note "展开答案与例子"

    **答案：** RankMixer处理的是异构字段token之间的交互；LONGER和HSTU重点处理行为历史及其状态。历史模块可以先产出摘要/状态，再作为字段交给TokenMix与PFFN。字段数T和历史长度N不是同一变量，替换字段attention不能直接推出全模型成本或长序列能力。

    **教学例子：** 示意：历史模块输出近期兴趣和长期兴趣两个向量，再与价格、设备、候选类别一起组成五个字段token；后段TokenMix不会倒过来替代前面的历史检索与编码。

    对照来源：[rankmixer](../../../reproductions/2507.15551-rankmixer/README.md) · [longer](../../../reproductions/2505.04421-longer/README.md) · [hstu](../../../reproductions/2402.17152-hstu/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较din、hstu、longer、slimper、rankmixer，围绕交互对象：历史内部、目标读取还是字段混合与每层传播的状态及原始历史是否持续可读建立分析和跨论文问答。

覆盖 73 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 73 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System](../../../reproductions/2501.15816-adaf2m2/README.md)
- [Scaling Recommender Transformers to One Billion Parameters](../../../reproductions/2507.15994-argus/README.md)
- [Behavior Sequence Transformer for E-commerce Recommendation in Alibaba](../../../reproductions/1905.06874-bst/README.md)
- [CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer](../../../reproductions/2602.11410-cadet/README.md)
- [CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent](../../../reproductions/2607.28070-ccformer/README.md)
- [ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling](../../../reproductions/2609.12375-chronicle-rec/README.md)
- [ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling](../../../reproductions/2607.26369-clockrope/README.md)
- [CMSL: Constructive Multi-Sequence Learning for Recommendation Systems](../../../reproductions/2606.28533-cmsl/README.md)
- [DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems](../../../reproductions/2008.13535-dcn-v2/README.md)
- [DeepFM: A Factorization-Machine based Neural Network for CTR Prediction](../../../reproductions/1703.04247-deepfm/README.md)
- [Deep Interest Evolution Network for Click-Through Rate Prediction](../../../reproductions/1809.03672-dien/README.md)
- [Deep Interest Network for Click-Through Rate Prediction](../../../reproductions/1706.06978-din/README.md)
- [ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling](../../../recommendation-components/2610.28569-echo-selector-loss/README.md)
- [FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer](../../../reproductions/2502.03036-fuxi-alpha/README.md)
- [Towards Large-scale Generative Ranking](../../../reproductions/2505.04180-genrank/README.md)
- [GenRec: An LLM-Backed Recommendation Ranker at Netflix](../../../reproductions/2608.10257-genrec-netflix/README.md)
- [Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study](../../../reproductions/2607.27577-ha-moe/README.md)
- [HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation](../../../reproductions/2609.37183-helix/README.md)
- [HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders](../../../reproductions/2602.21009-hisac/README.md)
- [Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations](../../../reproductions/2603.00980-hpgr/README.md)
- [Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations](../../../reproductions/2402.17152-hstu/README.md)
- [HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction](../../../reproductions/2601.12681-hyformer/README.md)
- [IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation](../../../reproductions/2608.09634-inthq/README.md)
- [JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling](../../../reproductions/2606.19108-journeyformer/README.md)
- [Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design](../../../reproductions/2602.10016-kunlun/README.md)
- [LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training](../../../reproductions/2609.14978-lazformer/README.md)
- [An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking](../../../reproductions/2602.12354-linkedin-feed-sr/README.md)
- [LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation](../../../reproductions/2601.20083-llatte/README.md)
- [Long-History User Transformers for Real-Time Ad Ranking](../../../reproductions/2607.14331-long-history-transformer/README.md)
- [LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders](../../../reproductions/2505.04421-longer/README.md)
- [MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization](../../../reproductions/2602.07520-mdl/README.md)
- [Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation](../../../reproductions/2605.24051-memento/README.md)
- [MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders](../../../reproductions/2602.14110-mixformer/README.md)
- [ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest](../../../reproductions/2602.09194-ml-dcn/README.md)
- [Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems](../../../reproductions/2602.12041-mlcc/README.md)
- [MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation](../../../reproductions/2602.07526-msn/README.md)
- [Not Only NTP: Extending Training Signal Coverage for Generative Recommendation](../../../reproductions/2607.12277-nontp/README.md)
- [OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking](../../../reproductions/2608.18606-onemodel/README.md)
- [OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking](../../../reproductions/2509.18091-onepiece/README.md)
- [OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation](../../../reproductions/2606.16838-onerank/README.md)
- [OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender](../../../reproductions/2510.26104-onetrans/README.md)
- [OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender](../../../reproductions/2609.28589-onetrans-v2/README.md)
- [PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform](../../../reproductions/2507.12704-pinfm/README.md)
- [POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation](../../../reproductions/2606.29946-poem/README.md)
- [RankMixer: Scaling Up Ranking Models in Industrial Recommenders](../../../reproductions/2507.15551-rankmixer/README.md)
- [RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems](../../../reproductions/2604.17878-rankup/README.md)
- [Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction](../../../reproductions/2609.37905-recap-ctr/README.md)
- [Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders](../../../reproductions/2610.01270-repair-state/README.md)
- [From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs](../../../reproductions/2609.01240-rest/README.md)
- [Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy](../../../reproductions/2607.12714-sam/README.md)
- [Self-Attentive Sequential Recommendation](../../../reproductions/1808.09781-sasrec/README.md)
- [Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling](../../../reproductions/2606.07546-semantic-native-longseq/README.md)
- [SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching](../../../reproductions/2609.08443-sequenceo1/README.md)
- [Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction](../../../reproductions/2006.05639-sim/README.md)
- [SlimPer: Make Personalization Model Slim and Smart](../../../reproductions/2607.12281-slimper/README.md)
- [SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders](../../../reproductions/2603.03988-sort-ranking/README.md)
- [Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction](../../../reproductions/2601.17836-sparsectr/README.md)
- [SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation](../../../reproductions/2607.24025-specformer/README.md)
- [Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation](../../../reproductions/2608.07055-tm20k/README.md)
- [TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search](../../../reproductions/2607.13398-tmallgs/README.md)
- [TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders](../../../reproductions/2602.06563-tokenmixer-large/README.md)
- [TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation](../../../reproductions/2506.02267-transact-v2/README.md)
- [TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings](../../../reproductions/2607.28940-transx/README.md)
- [TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery](../../../reproductions/2605.23702-tubifm/README.md)
- [TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou](../../../reproductions/2407.16357-twin-v2/README.md)
- [Bending the Scaling Law Curve in Large-Scale Recommendation Systems](../../../reproductions/2602.16986-ultra-hstu/README.md)
- [UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation](../../../reproductions/2606.27058-uniformer/README.md)
- [UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems](../../../reproductions/2609.11052-unirec/README.md)
- [UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking](../../../reproductions/2603.24226-uniscale/README.md)
- [UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence](../../../reproductions/2605.09040-uxsid/README.md)
- [WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture](../../../reproductions/2607.17017-whale/README.md)
- [Wide &amp; Deep Learning for Recommender Systems](../../../reproductions/1606.07792-wide-deep/README.md)
- [Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation](../../../reproductions/2601.21285-zenith/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/recommendation/history-ranking-backbones.md) · [返回全部精读卡片](../index.md)
