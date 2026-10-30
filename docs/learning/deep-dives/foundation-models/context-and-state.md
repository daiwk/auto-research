---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 长上下文不是一条轴：位置、读取与状态压缩

[基础模型](../index.md) · 更新 2026-10-30 · 34 篇主题资料 / 8 篇重点对照

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

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-30** · 精读MERLIN Eq7-9，将raw二阶矩、对齐方差和两softmax门控聚合与Mamba递归写入分开；注明因果已完成段、外部当前段以及非精确attention边界。

涉及：[merlin](../../../foundation-models/2610.37645-merlin/README.md) · [mamba](../../../reproductions/2312.00752-mamba/README.md)

**2026-10-29** · Select-TTT根据当前query的token概率质量调整上下文chunk写入fast weight的力度，apply-before-write保留时序；clip后总写入预算可能低于chunk数，不能再归一化伪装守恒。Sleep则把活跃与离线巩固分阶段，本地仅其LTI奖励。与冻结参数的状态更新相比，后者完整方法要训练扩展参数，不能把一个奖励核当成记忆已写入模型。

涉及：[select-ttt](../../../foundation-models/2610.36794-select-ttt/README.md) · [sleep-lti](../../../foundation-models/2606.03979-sleep-lti/README.md)

**2026-10-27** · 首版：比较位置编码、选择性状态、三路稀疏读取、尾部代理与前向回归压缩，明确历史信息的保存和恢复路径。

覆盖 31 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 34 篇资料</summary>

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

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/context-and-state.md) · [返回全部精读卡片](../index.md)
