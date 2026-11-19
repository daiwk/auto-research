---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 长上下文不是一条轴：位置、读取与状态压缩

[基础模型](../index.md) · 更新 2026-11-19 · 47 篇主题资料 / 21 篇重点对照

先问历史以什么形式存在，再问当前 token 怎样读它。RoPE 改变相对位置关系，Mamba 把历史写入递归状态，NSA 在多条读取路径间分工，OpenAttention 为未精读部分保留代理，TTR 则为当前输入求一个压缩表示。这些方法不能只按“支持多长”排成一列。 MERLIN在多个压缩状态之外保留routing key矩统计，改变段间读取权重，而不替换每段内部的递归写入。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/foundation-models/context-and-state.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：历史保存为逐 token KV、递归状态还是输入相关压缩系数 · 当前 query 是否能回到原始细节 · 未读取历史是省略、摘要代理还是已写入状态 · 额外代价发生在训练、前向求解还是索引读取

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [RoFormer: Enhanced Transformer with Rotary Position Embedding](../../../reproductions/2104.09864-rope/README.md) · [原始来源](https://arxiv.org/abs/2104.09864)<br>章节：背景与主要改动、核心公式 | 旋转 Q/K 的二维子空间，使点积通过相对位移表达位置；它仍可配合完整注意力。 | 解决位置表达，不负责减少历史条数或 KV 带宽；本地小模型旋转路径不证明任意长度外推。 |
| [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](../../../reproductions/2312.00752-mamba/README.md) · [原始来源](https://arxiv.org/abs/2312.00752)<br>章节：背景与主要改动、核心公式、复现边界 | 让步长和读写向量依赖当前 token，把历史持续折入有界递归状态。 | 不必逐 token 保留完整 KV，但未来只能利用状态中留下的信息；本地是原生 PyTorch scan，没有论文融合内核。 |
| [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](../../../reproductions/2502.11089-native-sparse-attention/README.md) · [原始来源](https://arxiv.org/abs/2502.11089)<br>章节：背景与主要改动、核心公式、复现边界 | 压缩块提供全局轮廓，query 选块取细节，滑窗保留近期精确信息，三路门控融合。 | 仍需设计与训练不同读取通路；选择错误时压缩概览未必能恢复细节。本地三路可训练，不代表论文长序列吞吐。 |
| [OpenAttention: One Percent Is Enough with Tail Proxies](../../../foundation-models/2610.30951-openattention/README.md) · [原始来源](https://arxiv.org/abs/2610.30951v1)<br>章节：背景与主要改动、核心公式 | 用 query 几何聚类，按代理误差估计分配精读预算，未读簇以带计数均值代理参与 softmax。 | 尾部没有直接清零，但均值代理仍会丢失簇内差异；ErrorGate 依赖近似假设。本地仅单头算子诊断，完整实验高成本未复现。 |
| [Rethinking Sequence Compression with Test-time Regression](../../../foundation-models/2610.31574-ttr-compressor/README.md) · [原始来源](https://arxiv.org/abs/2610.31574v1)<br>章节：背景与主要改动、核心公式 | 将一组 token 当作回归观测，每次前向解正则化最小二乘，以输入相关系数表示该组。 | 不是推理时训练参数，也不是免费池化；dual 求解含 T³ 项，只有组长远小于维度时才适合简化成本。当前为机制诊断。 |
| [Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training](../../../foundation-models/2610.36794-select-ttt/README.md) · [原始来源](https://arxiv.org/abs/2610.36794v1)<br>章节：背景与主要改动、核心公式 | 对query token的低CE位置top-k聚合，T×softmax分配并clip写入倍率。 | 必须传入真实冻结head/RMSNorm与NTP对齐特征；不含LLM或分布式内核。 |
| [Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories](../../../foundation-models/2606.03979-sleep-lti/README.md) · [原始来源](https://arxiv.org/abs/2606.03979v2)<br>章节：背景与主要改动、核心公式 | 把外部语义二元奖励与阈值化token编辑相似度混合。 | 只做LTI奖励，不实现CMS、梦境、知识播种或LoRA，完整Sleep高成本不复现。 |
| [Multi-State Linear Attention with Generalized Second-Order Routing](../../../foundation-models/2610.37645-merlin/README.md) · [原始来源](https://arxiv.org/abs/2610.37645v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 保存每段routing key均值与原始二阶矩，恢复query对齐方差；两路分别softmax再按门控混合外部state readouts。 | 增加分段状态和矩存储，不精确重建逐token softmax；当前未完成段需外部递归处理，完整中期训练不复现。 |
| [Coarse Semantic Blocks for Efficient Training-Free Sparse Attention](../../../foundation-models/2611.04313-semantic-block-sparse-attention/README.md) · [原始来源](https://arxiv.org/abs/2611.04313)<br>章节：背景与主要改动、核心公式、成本判断与复现边界 | 按逐prompt、逐KV head的球面key聚类形成非连续语义块；各GQA query head独立softmax后求和，惩罚可见块大小，整块选择后对原始QKV做注意力。 | 保留原始KV而非把centroid当value；整块预算可超额。全prompt拟合centroid使因果支持不等于严格流式因果不变性。本地仅L1索引与注意力参考，不含论文融合kernel或完整长文能力实验。 |
| [Anchor: Augmented Cross-Layer Recurrent State for Long-Context Retrieval in Test-Time Training](../../../foundation-models/2611.04327-anchor-kv/README.md) · [原始来源](https://arxiv.org/abs/2611.04327)<br>章节：背景与主要改动、核心公式、成本判断与复现边界 | 一组层共享recurrent KV state，以各reader的identity初始化线性read-map调整坐标基，再由输入相关sigmoid gate与局部SWA输出融合。 | 共享内容不代表共享坐标；完整训练仍需真实LaCT/Muon内层writer，且interior TTT只在部署时移除。本地接外部状态，只验证跨层读映射、gate和状态版本，不能称完整TTT或检索能力复现。 |
| [ConvPE: Convolutional Position Embedding Improves Transformers](../../../foundation-models/2611.07749-convpe/README.md) · [原始来源](https://arxiv.org/abs/2611.07749)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 将原始隐状态低维投影，经只在左侧补零的因果卷积，为每个查询生成相对距离偏置；注意力头按取模共享偏置头，在 softmax 前加到分数。 | 窗口外偏置为零而不是屏蔽。需要最近 W−1 个原始隐状态才能在分块解码中重建偏置；不减少 KV 条数。本地只验证默认一维偏置，不复现完整长上下文训练、融合核或吞吐。 |
| [ADIndex: Layer-Adaptive Sparse Attention Indexing via Group-Level Distillation](../../../foundation-models/2611.12956-adindex/README.md) · [原始来源](https://arxiv.org/abs/2611.12956v1)<br>章节：核心公式、数据协议与代码映射、结果与复现边界 | 按层校准组大小与共享候选库，用逐query标准化softmax后逐token max/Top-P教师蒸馏组索引器；只扫描anchor历史，再补新可见token并保留逐query DSA精排。 | 共享候选不等于共享最终Top-K，也不提供OpenAttention的未读尾部代理；teacher运算顺序、anchor因果边界和最大并集容量不可替换。L1训练KL降低不证明长文质量或B300 serving加速。 |
| [A Unified Model and Document Representation for On-Device Retrieval-Augmented Generation](../../../foundation-models/2604.14403-ecg-rag/README.md) · [原始来源](https://arxiv.org/abs/2604.14403v1)<br>章节：背景与主要改动、核心机制与公式、原文结果与限制、本地复现 | 设备端RAG既要控制文档索引磁盘占用，也要限制生成时的上下文/KV开销。ECG不是简单把检索器输出拼进prompt，而是只存一份多向量检索表示，再经投影转成同一decoder可消费的压缩上下文，避免独立检索向量和压缩向量重复存储。 | 不是。ECG压缩文档为共享语义向量并生成；ADIndex在模型注意力内部共享候选库，再逐query精排并补新token。外部文档表示压缩与因果KV索引的可见性、精度和成本单位不同。 |
| [Federated Vector Retrieval across Heterogeneous VectorDBs](../../../foundation-models/2611.01514-hvmap/README.md) · [原始来源](https://arxiv.org/abs/2611.01514v2)<br>章节：核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 四层归一化映射用跨目标fuzzy loss锚定异构空间；native/mapped双分数联合取K，spoke最多经hub两次映射。 | ECG-RAG让检索与压缩生成共享表示，HVMap不生成答案而对齐已存在的异构库。局部fuzzy loss与ECG联合loss均不代表完整RAG效果。 |
| [InfuseLoop: Cross-Trajectory Latent Injection for Scalable Parallel Looped Transformers](../../../foundation-models/2611.22426-infuseloop/README.md) · [原始来源](https://arxiv.org/abs/2611.22426v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 并行loop在同一执行周期同时推进多个预测轨迹。InfuseLoop让第r轮聚合上一周期已完成、但来自更浅loop的状态，而非仅传递本轨迹前一轮。未来轨迹位置不等于未来未生成token，合法性由执行周期决定。 | Anchor跨层共享外部TTT状态并学习read-map，InfuseLoop共享的是可用计算图中的轨迹latent；不能把任意跨层平均或持久缓存叫作InfuseLoop。 |
| [FM-Mamba: An Efficient Native 2D Selective State Space Model with Stability-Aware Discretization](../../../foundation-models/2611.22061-fm-mamba/README.md) · [原始来源](https://arxiv.org/abs/2611.22061v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 原生2D FM状态同时接收上、左与左上三个前驱，不通过展平扫描把二维关系退化为一条链。两个输入相关步长分别控制两个轴；a0/(a1a2)决定是否需要给步长施加上界。 | Mamba的一维selective SSM让步长、B/C依赖当前token并配合因果卷积和门控；FM-Mamba原生二维递推同时读取上、左、左上三前驱，使用两个轴步长及ratio相关稳定约束。展平成一维Mamba不是FM-Mamba，Python参考一致也不等于融合scan或PSD提速。 |
| [GaugeRoPE: RoPE-Compatible Executable Latent Attention](../../../foundation-models/2611.20524-gaugerope/README.md) · [原始来源](https://arxiv.org/abs/2611.20524v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 任意低秩K在潜空间通常不保留RoPE作用，需要逐历史token重建。GaugeRoPE只在相同频率块内拟合复数carrier，另用能量平衡后的joint PCA存residual K与V；query吸收decoder，聚合后才解码输出。 | Anchor让多个层共享TTT状态并学习read-map；GaugeRoPE保留每层token历史但改变其坐标/低秩表示。跨层共享和每token潜缓存压缩不是同一个操作。 |
| [SIMQ: A Single Graph-based Index for Multi-Vector Query](../../../foundation-models/2611.22079-simq/README.md) · [原始来源](https://arxiv.org/abs/2611.22079v1)<br>章节：背景与主要改动、核心公式、同主题对照、高成本完整实验 | ColBERT式MaxSim需要逐query token匹配文档token。SIMQ先均匀抽样token作初始聚合点，通过临时图分配剩余token，对过大cluster递归二分，归一化均值后建立一个质心图。查询只导航到少量质心，经质心到文档映射生成候选，最后才访问候选原始token精确重排，避免全query×centroid矩阵。 | HVMap解决不同编码器向量空间不能直接比较的问题，通过hub映射和双空间SCORE2联合重排；SIMQ假定同一规范化token空间，改变候选图组织和晚交互计算。前者的映射质量不由SIMQ的计数验证，后者的图效率也不由HVMap小张量loss证明。 |
| [UniGraph: A Unified Graph-based Index for Dynamic Hybrid Dense-Sparse Vector Retrieval](../../../foundation-models/2611.20758-unigraph/README.md) · [原始来源](https://arxiv.org/abs/2611.20758v1)<br>章节：背景与主要改动、核心公式、同主题对照、高成本完整实验 | 分别检索dense和sparse再合并可能过早漏掉仅在混合距离下优秀的向量。UniGraph在多个离散alpha下取近邻，按跨alpha入选频次合并成一个有界出度图；查询时不重构图，直接按自己的alpha遍历。稀疏或稠密guide给出入口，减少到目标区域的混合距离计算。 | HVMap学的是异构库之间的表示转换，UniGraph学不到新的向量映射，而是保留dense/sparse原分量并改变跨权重邻域组织。SCORE2的native/mapped双空间权重与UniGraph的语义／词汇alpha含义不同，不能共享一个未经验证的权重解释。 |
| [Deal With It: On Better Schedules for Listwise Reranking](../../../foundation-models/2611.22392-dealrank/README.md) · [原始来源](https://arxiv.org/abs/2611.22392v1)<br>章节：背景与主要改动、核心公式、同主题对照、高成本完整实验 | 并行listwise重排要把候选分组，每组只晋级固定配额。连续切块会把初始召回前部的好文档挤进同一组，越好的retriever越可能被配额误切。DealRank按retriever名次轮流发牌，使每个前缀在各组尽量平衡，再并行排序、按配额晋级并最终合并，不依赖补救认证轮。 | HVMap改变异构向量候选怎么映射和打分，DealRank不训练表示，而是安排已有候选进入ranker的组合。它们可串在同一检索流水线，但更少调用不是更好向量对齐，SCORE2正确也不能证明listwise配额无损。 |
| [Kernel Ridge Attention: Nonlinear Memory with Selective Forgetting](../../../foundation-models/2611.23896-kernel-ridge-attention/README.md) · [原始来源](https://arxiv.org/abs/2611.23896v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | KRA把历史关联写入固定大小的回归矩阵，同时保留后验协方差。共享可学习Fourier特征形成非线性核；内容相关OU时钟既衰减旧系数，也把协方差恢复到先验，使已经遗忘的方向重新可写。读取发生在当前值写入之后。 | Mamba用输入相关步长和读写向量控制SSM状态；KRA额外维护后验协方差来处理相关key方向的干扰。两者都是有界状态，但KRA每头还承担D平方协方差存储，不能仅按线性序列复杂度认为成本相同。 |

</div>

## 取舍分析 {#analysis}

### 位置可表达，不等于历史可访问

RoPE 决定 query 与 key 如何携带相对位置信息；即使旋转完全正确，全注意力仍需处理可见历史。Mamba 则改变历史的存储与传播方式，用状态替代逐项访问。因而“位置外推失败”和“状态没记住一个细节”是两种故障：前者不能只靠加状态容量解释，后者也不能只靠换位置编码修好。选型时应先确认任务需要精确回查，还是主要依靠可持续更新的状态。

对照来源：[rope](../../../reproductions/2104.09864-rope/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

### 压缩之后，还留不留回到细节的路

NSA 的压缩分支旁边仍有 query 条件的精细选块；OpenAttention 把预算分给精确行，并让剩余内容以 log-count 均值代理留在归一化中。TTR 则把整个组映射成回归系数，没有因此承诺逐项可逆。三者都减少某种处理负担，但细节的恢复路径不同。比较时要追踪遗漏信息去了哪里，而不能仅比较输出向量数；这里的本地公式或短训练记录也不足以排序它们的长文能力。

对照来源：[native-sparse-attention](../../../reproductions/2502.11089-native-sparse-attention/README.md) · [openattention](../../../foundation-models/2610.30951-openattention/README.md) · [ttr-compressor](../../../foundation-models/2610.31574-ttr-compressor/README.md)

### 10月29日：新方法与来源变化

Select-TTT根据当前query的token概率质量调整上下文chunk写入fast weight的力度，apply-before-write保留时序；clip后总写入预算可能低于chunk数，不能再归一化伪装守恒。Sleep则把活跃与离线巩固分阶段，本地仅其LTI奖励。与冻结参数的状态更新相比，后者完整方法要训练扩展参数，不能把一个奖励核当成记忆已写入模型。

对照来源：[rope](../../../reproductions/2104.09864-rope/README.md) · [select-ttt](../../../foundation-models/2610.36794-select-ttt/README.md) · [sleep-lti](../../../foundation-models/2606.03979-sleep-lti/README.md)

### 先写入状态，再决定读哪个段

Mamba的选择性递推决定历史如何进入单个状态；MERLIN假设已有多个分段状态及其readout，再决定当前query该偏向哪个段。相同key均值可以掩盖一段内少数强匹配项，原始二阶矩使query能恢复对齐方差；但这只是聚合线索，不能把丢在段内压缩中的信息精确找回。Eq9还要求均值与方差各自归一化再混合，先混logits后softmax是另一个算法。等长段和因果可见性也都是接口前提。

对照来源：[merlin](../../../foundation-models/2610.37645-merlin/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

### 保留原始历史与共享压缩状态，是两条不同读取路线

NSA用概览、选中块和滑窗保留不同细节路径；CSB不重新训练模型，而是把原始KV按语义重分块后整块读取。Anchor则让多层共享已经压缩的recurrent state，利用各层read-map协调坐标基，再门控融合局部输出。CSB的centroid负责选择，不代替被读value；Anchor的共享状态仍依赖真实writer，外部注入一个矩阵不等于完成TTT。另须分开因果支持与索引构建：CSB虽然mask未来位置，整prompt聚类仍可能让未来key改变早期路由，不能据此声称严格流式因果语言模型。两项本地L1组件都不提供完整模型能力、端到端加速或Evolve晋级证据。

对照来源：[native-sparse-attention](../../../reproductions/2502.11089-native-sparse-attention/README.md) · [semantic-block-sparse-attention](../../../foundation-models/2611.04313-semantic-block-sparse-attention/README.md) · [anchor-kv](../../../foundation-models/2611.04327-anchor-kv/README.md)

### 位置偏置有窗口，不等于可见历史有窗口

RoPE 旋转 Q/K 并通过相对位移进入点积；ConvPE 从最近隐状态预测一个随内容变化的分数修正，超出偏置窗口的可见 key 仍按原 QK 参与 softmax。CSB 则选取整组原始 KV 改变读取支持。三者改动的是点积表示、加性分数或支持集合，不应把 W 直接记为 KV 预算。分块解码时 ConvPE 还需要调用方提供真实左侧隐状态；分块与整序列切片的一致性验证的是偏置合同，不是完整长文能力或速度。

对照来源：[rope](../../../reproductions/2104.09864-rope/README.md) · [convpe](../../../foundation-models/2611.07749-convpe/README.md) · [semantic-block-sparse-attention](../../../foundation-models/2611.04313-semantic-block-sparse-attention/README.md)

### 省掉全前缀扫描，还是近似未读取尾部，先分清成本对象

ADIndex复用相邻query的候选扫描，再由各query精排，共享库只可使用anchor历史，后续query补入新可见token。OpenAttention则把精读之外的剩余KV转成带计数均值代理，与精确行联合softmax。前者不保证保留所有未读质量，后者的代理也不等于精确细节；不能只按读取比例把二者写成相同压缩方案。

对照来源：[adindex](../../../foundation-models/2611.12956-adindex/README.md) · [openattention](../../../foundation-models/2610.30951-openattention/README.md)

### ECG：检索和上下文压缩共享一套表示：先区分干预对象和可用证据

不是。ECG压缩文档为共享语义向量并生成；ADIndex在模型注意力内部共享候选库，再逐query精排并补新token。外部文档表示压缩与因果KV索引的可见性、精度和成本单位不同。 `SharedRepresentation` 真正让compression依赖stored E_ret；`joint_loss` 固定teacher logits/relevance，不让teacher获得梯度，保留α与温度梯度。FKL按答案token求和再按题平均；只有显式hard negatives进入margin，正例不能混入负例mask。gate的大正bias原文无确数，本地5是明确初始化约定。未带pretrained decoder、索引、特殊token注入或完整训练管道。

对照来源：[ecg-rag](../../../foundation-models/2604.14403-ecg-rag/README.md) · [adindex](../../../foundation-models/2611.12956-adindex/README.md)

### 共享一份表示与对齐多种表示，是不同的系统选择

ECG-RAG为避免重复存储而联合学习检索与压缩表示，依赖decoder训练；HVMap接受库已由不同编码器生成，通过配对映射和候选双空间评分消除部分不兼容。fuzzy loss对角锚定绝对对应，RKD只保相对几何不够；SCORE2还要保留每库native向量而不是总偏hub。小张量梯度不证明跨模态召回或索引吞吐，不能将完整campaign的作者结果搬进本地看板。

对照来源：[hvmap](../../../foundation-models/2611.01514-hvmap/README.md) · [ecg-rag](../../../foundation-models/2604.14403-ecg-rag/README.md)

### InfuseLoop：在上一执行周期聚合跨轨迹潜状态

Anchor跨层共享外部TTT状态并学习read-map，InfuseLoop共享的是可用计算图中的轨迹latent；不能把任意跨层平均或持久缓存叫作InfuseLoop。 keys和values都用无参数RMS归一化，文档边界在softmax前屏蔽。所有新状态读同一旧缓冲，完成整周期后再commit；聚合替换原跨loop输入，不能重复加上旧状态。

对照来源：[infuseloop](../../../foundation-models/2611.22426-infuseloop/README.md) · [anchor-kv](../../../foundation-models/2611.04327-anchor-kv/README.md)

### 先比较状态依赖图，再比较状态空间复杂度

实读Mamba README的递推是h_t=exp(Delta_t A)h_(t-1)+Delta_t B_t x_t，一条一维历史链支持selective scan；本地短预算WikiText负结果不代表原论文规模。FM-Mamba的两个轴指数交叉进入ZOH状态系数，并保留可能非零的对角前驱；同一反对角才能并行。其冻结系数逐位置稳定条件不构成任意时变场的全局证明。两者的输入依赖性相似，但拓扑、离散化和并行实现不同。

对照来源：[fm-mamba](../../../foundation-models/2611.22061-fm-mamba/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

### GaugeRoPE：可执行RoPE carrier与残余KV双支缓存

Anchor让多个层共享TTT状态并学习read-map；GaugeRoPE保留每层token历史但改变其坐标/低秩表示。跨层共享和每token潜缓存压缩不是同一个操作。 carrier在保留子空间中精确保持RoPE，但RKV把残余位置相关分数近似为不旋转的校正。因此整体attention一般仍是近似；不能因为carrier兼容就宣称压缩无损。PCA只用显式校准输入，不借测试答案选秩。

对照来源：[gaugerope](../../../foundation-models/2611.20524-gaugerope/README.md) · [anchor-kv](../../../foundation-models/2611.04327-anchor-kv/README.md)

### SIMQ：单质心图上的多向量检索与计数候选选择：区别机制与能力

§III/Alg1–2保留抽样、图引导分配、deferred二分、质心归一化、每token候选和精确MaxSim重排。§V/Alg3的SIMQ+在每token原始文档pool中按文档去重计数，不做TopDocs截断；边界count并列必须全部保留，候选数可以超过Nmin。当前Index用小型exact kNN邻接构图和有限Lloyd二分代替可扩展HNSW/VSAG后端，是明确的小数据后端差异，不复现工业build/QPS。 HVMap解决不同编码器向量空间不能直接比较的问题，通过hub映射和双空间SCORE2联合重排；SIMQ假定同一规范化token空间，改变候选图组织和晚交互计算。前者的映射质量不由SIMQ的计数验证，后者的图效率也不由HVMap小张量loss证明。

对照来源：[simq](../../../foundation-models/2611.22079-simq/README.md) · [hvmap](../../../foundation-models/2611.01514-hvmap/README.md)

### UniGraph：支持逐查询混合权重的统一稠密稀疏图：区别机制与能力

Alg1先对每alpha取top-kg，按出现次数选M个邻居；Alg2维护candidate与ef-sized结果集，使用逐query混合距离。dense-first用Cauchy–Schwarz范数界决定是否需要sparse内积：gamma=1是安全下界，gamma<1只是不保证安全的更激进估计。原主实验gamma=0.3；本地诊断用gamma=1核对不改变未剪枝beam结果。guide在alpha>0.5时选dense，否则sparse，0.5是相近量纲下的原实验约定。 HVMap学的是异构库之间的表示转换，UniGraph学不到新的向量映射，而是保留dense/sparse原分量并改变跨权重邻域组织。SCORE2的native/mapped双空间权重与UniGraph的语义／词汇alpha含义不同，不能共享一个未经验证的权重解释。

对照来源：[unigraph](../../../foundation-models/2611.20758-unigraph/README.md) · [hvmap](../../../foundation-models/2611.01514-hvmap/README.md)

### DealRank：按召回名次轮发候选，减少配额切掉好文档：区别机制与能力

§2.1的100候选配置是5组×20、每组留4、最后20再排，共6调用2轮。一致ranker只给最前q=4的最坏情况恢复保证，不是top10保证。500配置25组留3再4组留5，1000配置50组留2再5组留4，均三轮；被后轮淘汰的排在早轮前。调用回调必须返回原候选的一次排列，真正ThreadPool并发只验证调度，不产生LLM排序内容。 HVMap改变异构向量候选怎么映射和打分，DealRank不训练表示，而是安排已有候选进入ranker的组合。它们可串在同一检索流水线，但更少调用不是更好向量对齐，SCORE2正确也不能证明listwise配额无损。

对照来源：[dealrank](../../../foundation-models/2611.22392-dealrank/README.md) · [hvmap](../../../foundation-models/2611.01514-hvmap/README.md)

### KRA：在遗忘时恢复不确定性，用协方差决定写入方向

Mamba用输入相关步长和读写向量控制SSM状态；KRA额外维护后验协方差来处理相关key方向的干扰。两者都是有界状态，但KRA每头还承担D平方协方差存储，不能仅按线性序列复杂度认为成本相同。 a、b由同一组cos/sin频率映射，范数为1。P不是可省略的标量门；它会旋转并缩放写入方向。独立dual参考求解内容Gram与OU时间Gram的乘积核，按每个因果prefix核对输出。

对照来源：[kernel-ridge-attention](../../../foundation-models/2611.23896-kernel-ridge-attention/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 任务漏掉很早出现的一次性编号，换 RoPE 与换成递归状态，为什么不能视为同一种修复？ {#cross-position-versus-memory}

??? note "展开答案与例子"

    **答案：** RoPE 改变位置进入 QK 点积的方式，不会自动增加原始证据的访问机会；Mamba 改变历史如何被选择性写入状态，早期编号若没有被保留下来，后续也无原始 KV 可直接查询。应先诊断是位置关系失真、历史不可见，还是状态压缩遗漏，再决定是否需要 NSA 这类保留细节读取路径的结构。

    **教学例子：** 教学例：合同首页只有一次订单号，末尾才提问。正确相对位置并不等于模型必然读中该处；有界状态也不保证保存每个编号。

    对照来源：[rope](../../../reproductions/2104.09864-rope/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md) · [native-sparse-attention](../../../reproductions/2502.11089-native-sparse-attention/README.md)

### NSA 选中少数块，与 OpenAttention 同时保留未读簇代理，对遗漏内容做了什么不同处理？ {#cross-tail-proxy-versus-selection}

??? note "展开答案与例子"

    **答案：** NSA 把概览、选中块和近期滑窗作为不同分支，门控融合其输出；OpenAttention 在精确读取部分行后，把每个剩余簇作为带数量修正的代理放进同一注意力计算。前者依靠多路覆盖，后者近似未读尾部的质量与 value；二者都可能漏掉簇内或块内关键差异，不能把未直接读取写成没有误差。

    **教学例子：** 教学例：一百条记录中九十九条相似，一条含例外。概览或均值都可能稀释例外，需要检查选择器能否把它送入精读。

    对照来源：[native-sparse-attention](../../../reproductions/2502.11089-native-sparse-attention/README.md) · [openattention](../../../foundation-models/2610.30951-openattention/README.md)

### TTR 每次输入都重新拟合，和 Mamba 每个 token 都更新状态，是否意味着模型在部署时训练了权重？ {#cross-input-adaptation-versus-parameter-update}

??? note "展开答案与例子"

    **答案：** 都不能这样推断。TTR 在前向内用当前组求解回归系数，目标投影与正则参数由外层训练得到；Mamba 按固定参数和当前 token 更新递归状态。变化的是输入条件表示或运行状态，不是自动执行优化器。两者成本也不同：前者有线性方程求解，后者有逐步状态递推。

    **教学例子：** 教学例：同一冻结模型读两段不同文本会得到不同状态和系数；这与保存一份新的训练 checkpoint 是两件事。

    对照来源：[ttr-compressor](../../../foundation-models/2610.31574-ttr-compressor/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

### query条件写入系数变化，与Sleep奖励变化，分别能证明哪一步真的执行了？ {#cross-oct29-method-boundary}

??? note "展开答案与例子"

    **答案：** Select-TTT本地参考实际更新小fast-weight矩阵，可检查写入前输出和最终状态；Sleep本地只返回奖励，没有优化器或参数扩展。两者均不证明长上下文能力，更不能把奖励值直接解释为长期记忆保持率。

    **教学例子：** 教学例：一份记忆表的数值真的改变，和给一段续写打0.9分，是不同的执行证据。

    对照来源：[rope](../../../reproductions/2104.09864-rope/README.md) · [select-ttt](../../../foundation-models/2610.36794-select-ttt/README.md) · [sleep-lti](../../../foundation-models/2606.03979-sleep-lti/README.md)

### MERLIN多保存一个二阶矩，就把Mamba式有界状态变成了完整attention吗？ {#cross-merlin-routing-not-state-recurrence}

??? note "展开答案与例子"

    **答案：** 没有。二阶矩用于估计query与每段routing keys对齐的方差，帮助段间readout聚合；原模型仍压缩每段内容，并没有保留所有token的值与逐项softmax。它增加一条读取线索而非撤销状态压缩。

    **教学例子：** 教学示意：两段key均值同为1，一段全是1，另一段是-1与3；均值路由分不清，方差可区分，但仍不能从两个矩恢复段内所有原始记录。

    对照来源：[merlin](../../../foundation-models/2610.37645-merlin/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

### CSB只选历史位置、Anchor只共享一份state，为什么两者都不能由一个causal mask就证明完整长上下文能力？ {#cross-nov04b-routing-versus-shared-state}

??? note "展开答案与例子"

    **答案：** CSB对原始QKV的支持集屏蔽未来，但其全prompt聚类可能让未来key影响centroid与早期选择；mask没有消除建索引的信息依赖。Anchor的read-map和gate只决定怎样读外部共享state，记忆内容是否正确还取决于真实TTT writer和训练。本地分别验证选择/注意力以及共享读出的L1合同，既不证明严格流式因果不变性，也不证明长距离检索能力。

    **教学例子：** 教学例：在末尾加一批新key后重做聚类，早期选块可能变化；给Anchor手工填入一份矩阵后reader输出正确，也不能说明模型曾学会把订单号写进去。

    对照来源：[semantic-block-sparse-attention](../../../foundation-models/2611.04313-semantic-block-sparse-attention/README.md) · [anchor-kv](../../../foundation-models/2611.04327-anchor-kv/README.md)

### ConvPE 偏置窗口 W=4 时，距离 8 的因果 key 会消失吗？这和 CSB 哪一步不同？ {#cross-nov06-bias-window-not-support}

??? note "展开答案与例子"

    **答案：** 不会。ConvPE 对该项加零偏置，原 QK 分数与因果 mask 仍在；CSB 若没选择该历史 key 所在块且不在无条件区域，该 key 不进入注意力支持。ConvPE 的 W=4 还表示分块首项最多需要 3 个左侧原始隐状态，不是只允许看 4 个历史位置。

    **教学例子：** 教学例：距离 8 的 key 本来分数很高，ConvPE 加 0 后仍可能获高权重；被 CSB 排除则不能以原始 value 参与当前读出。

    对照来源：[convpe](../../../foundation-models/2611.07749-convpe/README.md) · [semantic-block-sparse-attention](../../../foundation-models/2611.04313-semantic-block-sparse-attention/README.md)

### ADIndex共享库和OpenAttention尾部代理，能用相同的漏读解释吗？ {#cross-shared-bank-versus-tail-proxy}

??? note "展开答案与例子"

    **答案：** 不能。ADIndex共享候选搜索后仍按query选最终Top-K，库外位置没有自动的代理质量。OpenAttention为未精读簇保留带计数代理，但其内容近似且必须移除已精读行。二者要分别核对索引覆盖和残余softmax质量。

    **教学例子：** 教学例：一个位置不在ADIndex候选并集就不能进入本次精排；在OpenAttention里它可能仍通过所在簇的剩余均值和计数参与，但不会保留该位置的全部细节。

    对照来源：[adindex](../../../foundation-models/2611.12956-adindex/README.md) · [openattention](../../../foundation-models/2610.30951-openattention/README.md)

### 它与ADIndex都减少读取成本，是否是同一稀疏检索？ {#cross-nov13-colm-ecg-rag}

??? note "展开答案与例子"

    **答案：** 不是。ECG压缩文档为共享语义向量并生成；ADIndex在模型注意力内部共享候选库，再逐query精排并补新token。外部文档表示压缩与因果KV索引的可见性、精度和成本单位不同。

    **教学例子：** ECG少存一套文档向量，不等于ADIndex少扫描历史key；二者的召回损失也不能同口径相加。

    对照来源：[ecg-rag](../../../foundation-models/2604.14403-ecg-rag/README.md) · [adindex](../../../foundation-models/2611.12956-adindex/README.md)

### ECG式共享表示与HVMap的低fuzzy loss能共同证明RAG质量提升吗？ {#cross-cross-nov18-hvmap-alignment}

??? note "展开答案与例子"

    **答案：** 不能。两者改变不同链路且本地都缺完整训练/检索/答案评估；HVMap还须验证语义配对泛化与联合排序，ECG须验证压缩上下文生成。诊断loss不是端到端能力。

    **教学例子：** 教学例：反向传播成功并不说明一个相关文档进入top10，更不说明答案正确。

    对照来源：[hvmap](../../../foundation-models/2611.01514-hvmap/README.md) · [ecg-rag](../../../foundation-models/2604.14403-ecg-rag/README.md)

### 与Anchor跨层共享状态有什么差别？ {#cross-nov18-infuseloop}

??? note "展开答案与例子"

    **答案：** Anchor读外部TTT记忆并结合局部attention；InfuseLoop依执行周期聚合多个轨迹的hidden states，状态语义和写入时机都不同。

    **教学例子：** 把一份KV矩阵广播给所有loop，没有实现所需的跨轨迹索引。

    对照来源：[infuseloop](../../../foundation-models/2611.22426-infuseloop/README.md) · [anchor-kv](../../../foundation-models/2611.04327-anchor-kv/README.md)

### 把图像展平后运行Mamba，为什么还不能叫FM-Mamba？ {#cross-nov18-fm-mamba}

??? note "展开答案与例子"

    **答案：** 它改变了二维依赖图：FM-Mamba每个位置同时读取上、左、左上并使用两个轴步长和稳定投影，而展平scan只沿选定的一维顺序递推。

    **教学例子：** 教学例：左上脉冲可经显式对角前驱影响下一格；删去该项后即使仍称SSM，也不是同一递推。

    对照来源：[fm-mamba](../../../foundation-models/2611.22061-fm-mamba/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

### GaugeRoPE与Anchor都减少状态，有何不同？ {#cross-nov18-gaugerope}

??? note "展开答案与例子"

    **答案：** 前者减少每token每层的坐标维数并保留频率结构；后者跨层共用递归状态，依赖外部writer和reader映射。

    **教学例子：** 同样减少一半字节，不代表历史信息或读写语义相同。

    对照来源：[gaugerope](../../../foundation-models/2611.20524-gaugerope/README.md) · [anchor-kv](../../../foundation-models/2611.04327-anchor-kv/README.md)

### SIMQ能代替HVMap做异构编码器对齐吗？ {#cross-cross-nov18-latest-simq}

??? note "展开答案与例子"

    **答案：** 不能。SIMQ在同一token空间内改变候选索引，HVMap学习跨空间映射。

    **教学例子：** 教学例：不同编码器的同维向量也不能直接靠SIMQ内积变得可比。

    对照来源：[simq](../../../foundation-models/2611.22079-simq/README.md) · [hvmap](../../../foundation-models/2611.01514-hvmap/README.md)

### UniGraph的alpha等于HVMap的native权重吗？ {#cross-cross-nov18-latest-unigraph}

??? note "展开答案与例子"

    **答案：** 不等于。前者混合dense和sparse距离，后者混合候选native与mapped空间分数。

    **教学例子：** 教学例：提高alpha不等于更相信候选所属数据库。

    对照来源：[unigraph](../../../foundation-models/2611.20758-unigraph/README.md) · [hvmap](../../../foundation-models/2611.01514-hvmap/README.md)

### 它能代替HVMap双空间重排吗？ {#cross-cross-nov18-latest-dealrank}

??? note "展开答案与例子"

    **答案：** 不能。DealRank决定哪些候选同场比较，HVMap定义跨编码器的可比分数。

    **教学例子：** 教学例：轮流发牌不能修正未对齐的embedding。

    对照来源：[dealrank](../../../foundation-models/2611.22392-dealrank/README.md) · [hvmap](../../../foundation-models/2611.01514-hvmap/README.md)

### 与Mamba相比，多保留了什么状态？ {#cross-nov19-kernel-ridge-attention}

??? note "展开答案与例子"

    **答案：** 除回归系数外还有每头D乘D协方差；它描述已约束方向。Mamba的selective scan并不维护同一后验几何。

    **教学例子：** 教学例：D翻倍时，协方差元素从D平方变成4D平方，即使上下文长度不变。

    对照来源：[kernel-ridge-attention](../../../foundation-models/2611.23896-kernel-ridge-attention/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-19** · Mamba用输入相关步长和读写向量控制SSM状态；KRA额外维护后验协方差来处理相关key方向的干扰。两者都是有界状态，但KRA每头还承担D平方协方差存储，不能仅按线性序列复杂度认为成本相同。 本地组件合同和高成本不复现分别记录。

涉及：[kernel-ridge-attention](../../../foundation-models/2611.23896-kernel-ridge-attention/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

**2026-11-18** · 本地ranker是确定性一致排序回调，不是模型；true_top只给quota_cuts外层诊断，不进入schedule。没有RankGPT提示、token费用或真实API延迟，机制计数不作NDCG／速度证据。作者提供mixedbread-ai/dealrank链接，但2026-11-18仓库／main commit API返回404，未核实公开源码或许可，不执行外部代码。完整多模型及27B计时矩阵高成本不复现。分组和最后晋级排序必须按原文层级配置核对，不能把所有情况压成一个generic topk。 完整实验高成本不复现，未作能力或Evolve晋级证据。

涉及：[dealrank](../../../foundation-models/2611.22392-dealrank/README.md) · [hvmap](../../../foundation-models/2611.01514-hvmap/README.md)

**2026-11-18** · 本地exact all-pairs构图和exact guide查找是有限诊断后端，不是论文C++可扩展候选构造；没有BGE-M3编码、SINDI、百万级索引或QPS对照。安全剪枝只相对同一beam插入规则成立，不能推出全局ANN召回完备；gamma<1必须显式保留风险。完整矩阵高成本不复现。 完整实验高成本不复现，未作能力或Evolve晋级证据。

涉及：[unigraph](../../../foundation-models/2611.20758-unigraph/README.md) · [hvmap](../../../foundation-models/2611.01514-hvmap/README.md)

**2026-11-18** · 没有ColBERT编码、百万级token索引、残差压缩、完整HNSW或公平吞吐实验。重复seed不使随机向量变成语义能力评测；SIMQ+保留完整边界并列意味着rerank参数不是它的硬候选上限。完整五数据集矩阵成本过高，不复现（审查DONE）。 完整实验高成本不复现，未作能力或Evolve晋级证据。

涉及：[simq](../../../foundation-models/2611.22079-simq/README.md) · [hvmap](../../../foundation-models/2611.01514-hvmap/README.md)

**2026-11-18** · Anchor让多个层共享TTT状态并学习read-map；GaugeRoPE保留每层token历史但改变其坐标/低秩表示。跨层共享和每token潜缓存压缩不是同一个操作。 本地边界与完整高成本不复现分别记录。

涉及：[gaugerope](../../../foundation-models/2611.20524-gaugerope/README.md) · [anchor-kv](../../../foundation-models/2611.04327-anchor-kv/README.md)

**2026-11-18** · Mamba的一维selective SSM让步长、B/C依赖当前token并配合因果卷积和门控；FM-Mamba原生二维递推同时读取上、左、左上三前驱，使用两个轴步长及ratio相关稳定约束。展平成一维Mamba不是FM-Mamba，Python参考一致也不等于融合scan或PSD提速。 本次实读已有同主题代表README，按真实研究轴比较，不借比较对象改变算法或宣称跨论文效果复现。

涉及：[fm-mamba](../../../foundation-models/2611.22061-fm-mamba/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

**2026-11-18** · Anchor跨层共享外部TTT状态并学习read-map，InfuseLoop共享的是可用计算图中的轨迹latent；不能把任意跨层平均或持久缓存叫作InfuseLoop。 本地边界与完整高成本不复现分别记录。

涉及：[infuseloop](../../../foundation-models/2611.22426-infuseloop/README.md) · [anchor-kv](../../../foundation-models/2611.04327-anchor-kv/README.md)

**2026-11-18** · 补HVMap跨空间fuzzy锚定、native权重与无配额联合检索；对照共享RAG表示，明确L1小张量与高成本完整实验的边界。

涉及：[hvmap](../../../foundation-models/2611.01514-hvmap/README.md) · [ecg-rag](../../../foundation-models/2604.14403-ecg-rag/README.md)

**2026-11-13** · 补入固定Google COLM历史来源论文及L1组件，比较核心定义与证据边界；完整实验明确不复现，不把本地诊断当模型能力或Evolve改进。

涉及：[ecg-rag](../../../foundation-models/2604.14403-ecg-rag/README.md) · [adindex](../../../foundation-models/2611.12956-adindex/README.md)

**2026-11-11** · 加入ADIndex，将组内候选扫描复用与OpenAttention的尾部质量代理分开；保留标准化softmax→max→Top-P教师、anchor可见边界和新token补回。仅L1索引器与训练算术，完整长文/serving矩阵不复现。

涉及：[adindex](../../../foundation-models/2611.12956-adindex/README.md) · [openattention](../../../foundation-models/2610.30951-openattention/README.md)

**2026-11-06** · 增加 ConvPE，与 RoPE、CSB 区分点积表示、窗口化加性偏置与可见支持；注明分块原始隐状态条件及完整训练、融合核不复现。

涉及：[convpe](../../../foundation-models/2611.07749-convpe/README.md)

**2026-11-04** · 增加CSB与Anchor，比较原始KV的语义选块与共享recurrent state的坐标变换读出；明确全prompt聚类的非流式因果边界、外部writer不等于完整TTT，以及两项仅L1组件、完整高成本实验不复现。

涉及：[semantic-block-sparse-attention](../../../foundation-models/2611.04313-semantic-block-sparse-attention/README.md) · [anchor-kv](../../../foundation-models/2611.04327-anchor-kv/README.md)

**2026-10-30** · 精读MERLIN Eq7-9，将raw二阶矩、对齐方差和两softmax门控聚合与Mamba递归写入分开；注明因果已完成段、外部当前段以及非精确attention边界。

涉及：[merlin](../../../foundation-models/2610.37645-merlin/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

**2026-10-29** · Select-TTT根据当前query的token概率质量调整上下文chunk写入fast weight的力度，apply-before-write保留时序；clip后总写入预算可能低于chunk数，不能再归一化伪装守恒。Sleep则把活跃与离线巩固分阶段，本地仅其LTI奖励。与冻结参数的状态更新相比，后者完整方法要训练扩展参数，不能把一个奖励核当成记忆已写入模型。

涉及：[select-ttt](../../../foundation-models/2610.36794-select-ttt/README.md) · [sleep-lti](../../../foundation-models/2606.03979-sleep-lti/README.md)

**2026-10-27** · 首版：比较位置编码、选择性状态、三路稀疏读取、尾部代理与前向回归压缩，明确历史信息的保存和恢复路径。

覆盖 31 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 47 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](../../../reproductions/2108.12409-alibi/README.md)
- [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](../../../reproductions/2608.06849-autonomy-heads/README.md)
- [Convolution for Large Language Models](../../../reproductions/2607.18413-conv-llm/README.md)
- [DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling](../../../reproductions/2608.02032-dart/README.md)
- [Fractional State Space Transition for Long Sequence Modeling](../../../foundation-models/2609.36314-frac-ssm/README.md)
- [Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free](../../../reproductions/2505.06708-gated-attention/README.md)
- [Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection](../../../reproductions/2607.21752-gzip-sparse-attention/README.md)
- [Hymba: A Hybrid-head Architecture for Small Language Models](../../../reproductions/2411.13676-hymba/README.md)
- [Kronecker Delta Rule for Long Context Linear Attention](../../../foundation-models/2610.26834-kronlstm/README.md)
- [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](../../../reproductions/2312.00752-mamba/README.md)
- [Open-world AI: a Tale of Three Requirements](../../../foundation-models/2610.20782-memory-mosaics-plus/README.md)
- [MiniMax Sparse Attention](../../../reproductions/2606.13392-minimax-sparse-attention/README.md)
- [MoBA: Mixture of Block Attention for Long-Context LLMs](../../../reproductions/2502.13189-moba/README.md)
- [Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable](../../../reproductions/2607.21405-mobius-rope/README.md)
- [MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution](../../../foundation-models/2609.35664-ms-gla/README.md)
- [Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory](../../../reproductions/2607.21000-naju/README.md)
- [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](../../../reproductions/2502.11089-native-sparse-attention/README.md)
- [Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels](../../../reproductions/2610.13674-oal/README.md)
- [On-Demand Attention: Efficient Long-Context Decoding with Learned Recall](../../../foundation-models/2609.20734-oda/README.md)
- [Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension](../../../reproductions/2608.10296-olmpool-long-context/README.md)
- [OpenAttention: One Percent Is Enough with Tail Proxies](../../../foundation-models/2610.30951-openattention/README.md)
- [Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers](../../../reproductions/2610.13735-orthros/README.md)
- [Role-aware Heuristic Episodic Attention for Conversational LLMs](../../../foundation-models/2610.00958-rea/README.md)
- [RoFormer: Enhanced Transformer with Rotary Position Embedding](../../../reproductions/2104.09864-rope/README.md)
- [SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking](../../../reproductions/2609.13141-sas-attention/README.md)
- [Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity](../../../foundation-models/2610.28441-stratified-sparse-attention/README.md)
- [Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers](../../../reproductions/2603.26380-switch-attention/README.md)
- [TransMem: Transforming Hidden States into Memory for Large Language Models](../../../reproductions/2607.29032-transmem/README.md)
- [Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling](../../../foundation-models/2609.36529-triadic-linear-attention/README.md)
- [Learning What to Remember: Test-Time Training via Context Distillation](../../../reproductions/2608.01672-ttcd/README.md)
- [Rethinking Sequence Compression with Test-time Regression](../../../foundation-models/2610.31574-ttr-compressor/README.md)
- [Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training](../../../foundation-models/2610.36794-select-ttt/README.md)
- [Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories](../../../foundation-models/2606.03979-sleep-lti/README.md)
- [Multi-State Linear Attention with Generalized Second-Order Routing](../../../foundation-models/2610.37645-merlin/README.md)
- [Coarse Semantic Blocks for Efficient Training-Free Sparse Attention](../../../foundation-models/2611.04313-semantic-block-sparse-attention/README.md)
- [Anchor: Augmented Cross-Layer Recurrent State for Long-Context Retrieval in Test-Time Training](../../../foundation-models/2611.04327-anchor-kv/README.md)
- [ConvPE: Convolutional Position Embedding Improves Transformers](../../../foundation-models/2611.07749-convpe/README.md)
- [ADIndex: Layer-Adaptive Sparse Attention Indexing via Group-Level Distillation](../../../foundation-models/2611.12956-adindex/README.md)
- [A Unified Model and Document Representation for On-Device Retrieval-Augmented Generation](../../../foundation-models/2604.14403-ecg-rag/README.md)
- [Federated Vector Retrieval across Heterogeneous VectorDBs](../../../foundation-models/2611.01514-hvmap/README.md)
- [InfuseLoop: Cross-Trajectory Latent Injection for Scalable Parallel Looped Transformers](../../../foundation-models/2611.22426-infuseloop/README.md)
- [FM-Mamba: An Efficient Native 2D Selective State Space Model with Stability-Aware Discretization](../../../foundation-models/2611.22061-fm-mamba/README.md)
- [GaugeRoPE: RoPE-Compatible Executable Latent Attention](../../../foundation-models/2611.20524-gaugerope/README.md)
- [SIMQ: A Single Graph-based Index for Multi-Vector Query](../../../foundation-models/2611.22079-simq/README.md)
- [UniGraph: A Unified Graph-based Index for Dynamic Hybrid Dense-Sparse Vector Retrieval](../../../foundation-models/2611.20758-unigraph/README.md)
- [Deal With It: On Better Schedules for Listwise Reranking](../../../foundation-models/2611.22392-dealrank/README.md)
- [Kernel Ridge Attention: Nonlinear Memory with Selective Forgetting](../../../foundation-models/2611.23896-kernel-ridge-attention/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/context-and-state.md) · [返回全部精读卡片](../index.md)
