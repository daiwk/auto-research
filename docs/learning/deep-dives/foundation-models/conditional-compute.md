---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 按需算力：选择专家、跳过计算，还是查回旧知识

[基础模型](../index.md) · 更新 2026-10-27 · 26 篇主题资料 / 6 篇重点对照

参数容量、每 token 激活量与部署时延是三件事。Switch 选择计算专家，Engram 和 Memory Grafting 查局部模式；AdaDSF、Telescopic LM 与 WIDE 则分别从 token—层、整体深度和组宽度分配计算。先识别路由对象，才能讨论容量和省算。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/foundation-models/conditional-compute.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：选择的是专家、层、head/channel 组还是离散记忆条目 · 容量保存在可训练网络还是冻结查表值 · 预算按 token、层、整个请求还是部署深度约束 · 稀疏分支是否真的跳过内核计算

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](../../../reproductions/2101.03961-switch-transformer/README.md) · [原始来源](https://arxiv.org/abs/2101.03961)<br>章节：背景与主要改动、核心公式、复现边界 | 每 token 仅激活一个 FFN 专家，以稀疏计算扩大总参数容量，并用辅助项控制负载。 | 存储、专家容量和跨设备通信仍存在；本地 top-1 MoE 未复刻容量溢出与 all-to-all。 |
| [Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models](../../../reproductions/2601.07372-engram/README.md) · [原始来源](https://arxiv.org/abs/2601.07372)<br>章节：背景与主要改动、核心公式、复现边界 | 规范化 n-gram 走哈希表，查出的可训练记忆经上下文门控注入早期层。 | 擅长存局部模式，不替代组合推理；哈希冲突与表规模仍需考虑。本地可训练查表已执行，短预算结果并非论文收益。 |
| [Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory](../../../reproductions/2605.20948-memory-grafting/README.md) · [原始来源](https://arxiv.org/abs/2605.20948)<br>章节：背景与主要改动、核心公式、复现边界 | 用预训练模型离线编码高频短语并冻结，在线最长后缀精确命中，未命中回退 hash Engram。 | 把一部分知识获取成本移到离线 bank，命中覆盖与接口对齐成为新条件；本地 bank 小，未验证相对 Engram 的规模增益。 |
| [Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs](../../../reproductions/2607.21291-adadsf/README.md) · [原始来源](https://arxiv.org/abs/2607.21291)<br>章节：背景与主要改动、核心公式、复现边界 | 用 dense teacher 的层间变化分配层预算，再由逐层 router 只处理 Top-K token，其余走残差旁路。 | 全局活跃比例要校准，token 路由需对齐教师；活跃 token 数不等于 GPU 实测 FLOPs 或时延。 |
| [Telescopic Language Models](../../../foundation-models/2609.35769-telescopic-lm/README.md) · [原始来源](https://arxiv.org/abs/2609.35769)<br>章节：背景与主要改动 | 训练随机深度前缀并保留全深 anchor，让同一 checkpoint 在多个完整前缀深度可用。 | 控制的是可部署深度，不等于每个 token 都有细粒度层路由；本地只验证随机深度和 anchor 梯度路径。 |
| [WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning](../../../reproductions/2607.28418-wide/README.md) · [原始来源](https://arxiv.org/abs/2607.28418)<br>章节：背景与主要改动、核心公式、复现边界 | 每 token 分别选择 attention head group 与 FFN channel group，使计算粒度细于整层。 | 需要 mask 重排和设备内 block skip 才兑现速度；本地 dense kernel 下的稀疏率不能直接当加速。 |

</div>

## 取舍分析 {#analysis}

### 计算专家与条件记忆，不是同一类容量

Switch 把输入送到一个网络专家执行非线性变换；Engram 根据离散局部片段取表值，再由上下文判断是否使用。Memory Grafting 进一步把部分表值来源改成冻结预训练模型的离线表示。相同的“大容量、少激活”描述掩盖了不同训练对象：专家权重、联合训练记忆表和冻结 bank 需要不同维护方式。查表仍要传输和融合，不能把期望常数时间寻址理解成整个层零成本。

对照来源：[switch-transformer](../../../reproductions/2101.03961-switch-transformer/README.md) · [engram](../../../reproductions/2601.07372-engram/README.md) · [memory-grafting](../../../reproductions/2605.20948-memory-grafting/README.md)

### 先写清预算的单位，再谈按需

AdaDSF 的层预算控制有多少 token 进入各层；Telescopic LM 使一个深度前缀整体可用；WIDE 则把某个 token 的注意力组和 FFN 组分别路由。它们可以产生相近的平均活跃比例，却有不同的数据依赖、负载和内核形状。部署中若仍执行 dense matmul 后乘零，理论省算并没有变成时延收益。选型必须把训练兼容性和实际跳过粒度一起列出。

对照来源：[adadsf](../../../reproductions/2607.21291-adadsf/README.md) · [telescopic-lm](../../../foundation-models/2609.35769-telescopic-lm/README.md) · [wide](../../../reproductions/2607.28418-wide/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 高频短语重复出现时，增加一个 Switch 专家与加入 Engram/Memory Grafting，分别让系统多学了什么？ {#cross-lookup-versus-expert}

??? note "展开答案与例子"

    **答案：** Switch 增加可被 router 选中的计算函数，仍需对当前 hidden 执行专家网络；Engram 学习离散 n-gram 对应表值，Memory Grafting 则复用外部预训练模型冻结的短语表示，并在未命中时回退。前者扩大条件计算，后两者分担局部模式的存取；它们都不能保证复杂组合关系由局部记忆直接回答。

    **教学例子：** 教学例：反复出现的产品名可由查表提供稳定线索；比较两个产品的适用条件，仍需要上下文与组合计算。

    对照来源：[switch-transformer](../../../reproductions/2101.03961-switch-transformer/README.md) · [engram](../../../reproductions/2601.07372-engram/README.md) · [memory-grafting](../../../reproductions/2605.20948-memory-grafting/README.md)

### 同样写“只用一半计算”，AdaDSF、Telescopic LM 和 WIDE 为什么可能产生不同执行图？ {#cross-budget-unit}

??? note "展开答案与例子"

    **答案：** AdaDSF 可让不同 token 在不同层参与计算，Telescopic LM 使用某个完整深度前缀，WIDE 可在同一层为各 token 选择不同 head/channel 组。平均比例相同并不约束最慢路径、组形状或访存；需要分别记录 token—层分配、实际深度和组激活，才能确认是否满足相同部署预算。

    **教学例子：** 教学例：半数 token 跑全层、所有 token 跑半深度、每个 token 用半宽度，平均活跃量相近，却不是同一次前向。

    对照来源：[adadsf](../../../reproductions/2607.21291-adadsf/README.md) · [telescopic-lm](../../../foundation-models/2609.35769-telescopic-lm/README.md) · [wide](../../../reproductions/2607.28418-wide/README.md)

### 为什么 Switch 的专家稀疏与 WIDE 的组稀疏，不能仅凭 mask 数量推算同样的加速？ {#cross-sparsity-versus-latency}

??? note "展开答案与例子"

    **答案：** 专家选择可能引入分发与负载不均，组路由需要让硬件跳过相应块；两者的矩阵形状和访存方式不同。若本地参考先算完全部分支再屏蔽，mask 只改变数值；即使真正只算选中部分，也要计路由、重排和通信。应测目标负载下完整路径，而不能用理论激活比例替代时延。

    **教学例子：** 教学例：一层激活半数 FFN 通道，但为此多次小矩阵调用和重排，可能比一次大 dense 矩阵更慢。

    对照来源：[switch-transformer](../../../reproductions/2101.03961-switch-transformer/README.md) · [wide](../../../reproductions/2607.28418-wide/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较专家计算、离散查表、冻结短语嫁接与深度/宽度路由，区分容量、预算单位和硬件兑现条件。

覆盖 26 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 26 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs](../../../reproductions/2607.21291-adadsf/README.md)
- [Byte Latent Transformer: Patches Scale Better Than Tokens](../../../reproductions/2412.09871-blt/README.md)
- [Cross-Entropy Guided Routing in Mixture-of-Experts Large Language Models](../../../foundation-models/2609.37751-ce-guided-moe/README.md)
- [CoTS: Competitive Token Selection for Latent Reasoning in Large Language Models](../../../foundation-models/2610.20642-cots/README.md)
- [Smoothing the Top-k Exposure Boundary for Sparse Mixture-of-Experts](../../../foundation-models/2610.11575-elastic-expert-routing/README.md)
- [Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models](../../../reproductions/2601.07372-engram/README.md)
- [Pretraining Latent Information Feedback Transformers with Teacher Supervision](../../../foundation-models/2609.38149-lift-feedback/README.md)
- [Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations](../../../reproductions/2609.03426-lngram-v2/README.md)
- [Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers](../../../reproductions/2607.15456-looped-latent-attention/README.md)
- [MACRO: Markov Chain Routing of Transformer Layers](../../../reproductions/2608.05872-macro/README.md)
- [Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory](../../../reproductions/2605.20948-memory-grafting/README.md)
- [mHC: Manifold-Constrained Hyper-Connections](../../../reproductions/2512.24880-mhc/README.md)
- [Optimized Deferral for Imbalanced Settings](../../../foundation-models/2604.27723-mild/README.md)
- [Rethinking Routing Exploration in Modern Mixture-of-Experts](../../../foundation-models/2610.22353-mirror-moe/README.md)
- [Multi-Stream Attention Residuals](../../../reproductions/2610.13630-msar/README.md)
- [Patch where the text is new: a compression view of where byte-level models should spend compute](../../../foundation-models/2610.22100-novelty-patching/README.md)
- [Penelope: Localized Latent Recurrence for Efficient Structured Reasoning](../../../reproductions/2607.25915-penelope/README.md)
- [Persistent Recurrent Memory Between Transformer Layers Improves Language Model Generalization](../../../foundation-models/2609.17251-persistent-recurrent-memory/README.md)
- [RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models](../../../reproductions/2608.21236-rare/README.md)
- [Role-Decoupled Attention Residuals](../../../reproductions/2608.01075-rd-attnres/README.md)
- [Data Scarcity and Model Sparsity: Mixtures-of-Experts Overfit More to Repeated Data](../../../foundation-models/2609.11917-repeat-aware-moe/README.md)
- [SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference](../../../foundation-models/2610.12327-sparse-decoding/README.md)
- [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](../../../reproductions/2101.03961-switch-transformer/README.md)
- [SWRouter: Similarity-Contractive Window Routing for Multi-Turn Large Language Model Conversations](../../../foundation-models/2609.11414-swrouter/README.md)
- [Telescopic Language Models](../../../foundation-models/2609.35769-telescopic-lm/README.md)
- [WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning](../../../reproductions/2607.28418-wide/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/conditional-compute.md) · [返回全部精读卡片](../index.md)
