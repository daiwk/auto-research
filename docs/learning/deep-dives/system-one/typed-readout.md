---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 同样输出候选分布，读出位置与缓存边界为何不同？

[结构化决策](../index.md) · 更新 2026-11-19 · 11 篇主题资料 / 6 篇重点对照

类型化决策先把输出空间限定下来，但“无需生成长句”并不指定唯一架构。LLM2Jev读选项标签的语言概率，System One重排读首答案位置的候选字母，MJev-Spatial复用原生注意力Q/K，MetaEncoder则把请求和候选独立编码。先看打分依赖谁，再判断是否可缓存、能否开放检索，以及连续输出怎样离散化。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/system-one/typed-readout.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：评分来自语言词表、原生注意力还是向量相似度 · 候选是否联合上下文化及哪些表示可以缓存 · 输出是闭集选择、开放检索还是多阶段空间细化 · 训练读出与本地验证范围

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [LLM2Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them](../../../foundation-models/2610.02076-llm2jev/README.md) · [原始来源](https://arxiv.org/abs/2610.02076)<br>章节：背景与主要改动、核心公式、复现边界 | 对括号数字选项的token对数概率求和并在有限选项中形成分布；微调组合listwise决策损失与基础模型辅助输出的KL锚定。 | 可沿用语言模型读出，但多token标签需要完整计分；有限候选概率不自动具备候选不变性。本地仅候选打分/KL组件，未跑4B模型JevBench。 |
| [MetaEncoder: Exploring the Limit of Bi-Encoders for Multimodal System One Decision Making with Natural Language Interface](../../../foundation-models/2610.11316-metaencoder/README.md) · [原始来源](https://arxiv.org/abs/2610.11316)<br>章节：背景与主要改动、核心公式与原文效果、本地复现与成本决策 | 共享因果编码器分别编码请求和候选，取归一化末token向量，以温度缩放余弦分数做决策或检索。 | 候选独立编码便于预计算；请求可含选项，不能据此宣称请求表示对候选集合不变。双塔压缩限制细粒度联合推理，完整30B评测成本过高未复现。 |
| [MJev-Spatial: System One Spatial Intelligence via Native Attention Matching](../../../foundation-models/2610.22276-mjev-spatial/README.md) · [原始来源](https://arxiv.org/abs/2610.22276)<br>章节：背景与主要改动、核心公式、代码映射与边界 | decision marker的原生Q与各candidate-end marker的原生K打分，不增加独立分类头；计数分桶，二维点用三级区域选择。 | 连续空间任务变成可约束的离散步骤，但裁剪/分桶改变了分辨率与调用次数；多阶段问题应先题内平均损失，不能把阶段多当成样本更多。 |
| [Multimodal Reranking Is a System One Decision](../../../multimodal-models/2610.28435-system-one-rerank/README.md) · [原始来源](https://arxiv.org/abs/2610.28435v1)<br>章节：背景与主要改动、核心公式、复现边界 | query和首阶段top-K候选进入同一多模态prompt，在首答案位置读取不同单token字母logits并候选内归一化。 | 联合看候选便于setwise比较，候选表示不能直接当独立缓存。只重排top-K，外部保持原序；本地是诊断组件，未复现完整大模型检索矩阵或decision head训练。 |
| [Jeveration: System One Models Now Generate](../../../system-one/2611.24738-jeveration/README.md) · [原始来源](https://arxiv.org/abs/2611.24738v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 把图像表示为128个离散code的联合Choice，所有位置共享随机状态，而不是把各位置的边缘分布独立采样。冻结Qwen3.5-4B配共享LoRA与任务head，先学masked图像分布，再以distribution matching和置信纠正训练单步决策；同一checkpoint还做图到图与dense prediction。 | LLM2Jev把候选标签读成有限决策分布；Jeveration还必须协调空间上众多输出，并学会使用共同随机状态。单选候选打分成功，不证明整图联合分布或图像质量。 |
| [EgoJev: Finding Evidence in Egocentric Video by Reading VLM Decisions](../../../system-one/2611.24616-egojev/README.md) · [原始来源](https://arxiv.org/abs/2611.24616v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 同一冻结VLM把带数字标签的候选缩略图放在一个prompt中，读取完整标签的条件概率而不是生成时间文本。粗分布决定细看窗口，细分布先保留窗口粗概率总量，再与对应粗分布做几何平均。最后在时间的分段均匀分布上取中点分位数，分配有限回答帧。 | System One多模态重排把一个联合候选分布用于排序；EgoJev将分布用于时间预算分配。前者单token字母读出不能不加检查地替代后者多token数字标签概率，frame quantile也不是单纯top-k帧。 |

</div>

## 取舍分析 {#analysis}

### 把“单步”拆成读出与任务流程

LLM2Jev和System One重排都能直接读概率，但一个选项标签可能包含多个token，重排还须核对字母确为单token。MJev-Spatial的单次候选读出也不表示整项空间任务只调用一次：点定位连续选三个3×3区域，计数用分级表示。应比较完成同一任务的总前向次数与输入，而非只比较最后一层输出形式。

对照来源：[llm2jev](../../../foundation-models/2610.02076-llm2jev/README.md) · [system-one-rerank](../../../multimodal-models/2610.28435-system-one-rerank/README.md) · [mjev-spatial](../../../foundation-models/2610.22276-mjev-spatial/README.md)

### 缓存收益来自依赖关系

MetaEncoder的候选只按自己的内容编码，适合离线建向量索引；System One重排让候选共同进入上下文，换一组对手可能改变其上下文化结果。MetaEncoder闭集请求还可以包含选项，因此候选缓存可复用不等于请求向量对选项变化不变。前者偏向可索引性，后者保留联合比较，不能从接口直接判定准确率胜负。

对照来源：[metaencoder](../../../foundation-models/2610.11316-metaencoder/README.md) · [system-one-rerank](../../../multimodal-models/2610.28435-system-one-rerank/README.md)

### Jeveration：以共享随机状态协调一次前向图像决策

LLM2Jev把候选标签读成有限决策分布；Jeveration还必须协调空间上众多输出，并学会使用共同随机状态。单选候选打分成功，不证明整图联合分布或图像质量。 给定共享xi后可并行选择，但对xi求混合后各位置不再必须独立。仅添加随机噪声不够：原文指出直接监督可忽略该状态。纠正target在训练时重mask最低置信的一半位置，由冻结的第一阶段模型补全；推理仍是一次生成前向，不是把训练辅助步骤算成免费。

对照来源：[jeveration](../../../system-one/2611.24738-jeveration/README.md) · [llm2jev](../../../foundation-models/2610.02076-llm2jev/README.md)

### EgoJev：以决策分布几何融合与分位数分配视频帧

System One多模态重排把一个联合候选分布用于排序；EgoJev将分布用于时间预算分配。前者单token字母读出不能不加检查地替代后者多token数字标签概率，frame quantile也不是单纯top-k帧。 细读窗口的局部分布归一后乘该窗口的粗概率总量；未细读窗口均摊其窗口质量。平方根不同于普通乘积，后者过度锐化。k=0直接保留单层粗分布。分位数需在bin内插值而不是一律取bin中心。标签如17]可能多token，完整读出需逐条件概率相乘并含终止]，本地不实现这部分。

对照来源：[egojev](../../../system-one/2611.24616-egojev/README.md) · [system-one-rerank](../../../multimodal-models/2610.28435-system-one-rerank/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 都只输出候选概率，为什么MetaEncoder能预编码候选，而System One重排通常不能照搬？ {#cross-candidate-cache-dependency}

??? note "展开答案与例子"

    **答案：** MetaEncoder独立运行候选编码器，候选向量不读取本次请求或其他候选；联合重排中，候选在同一prompt里上下文化，缓存一个脱离该集合的表示不能保证得到同样分数。可缓存的是依赖不变的计算，不能由输出是概率来推断。

    **教学例子：** 示意：同一份工具说明可在双塔中编码一次供千次请求检索；把它与另外五个工具一同交给VLM比较时，换掉五个对手就改变了联合输入。

    对照来源：[metaencoder](../../../foundation-models/2610.11316-metaencoder/README.md) · [system-one-rerank](../../../multimodal-models/2610.28435-system-one-rerank/README.md)

### 如何把计数和点定位变成选择题，又为什么不能把它等同一次普通多选？ {#cross-spatial-choice-granularity}

??? note "展开答案与例子"

    **答案：** MJev-Spatial把数值拆成有界离散决策，点定位通过多轮区域细化逐步提高分辨率；LLM2Jev则对已给出的有限选项形成分布。前者的下一步输入依赖上一步所选区域，任务误差也会沿阶段传播，因而要核算完整流程而不是只看每步的softmax。

    **教学例子：** 示意：先在九宫格选右上角，再在原图该区域内细分；第一步选错区域，第二步再精确也不能找回已排除的位置。

    对照来源：[mjev-spatial](../../../foundation-models/2610.22276-mjev-spatial/README.md) · [llm2jev](../../../foundation-models/2610.02076-llm2jev/README.md)

### 候选内最高概率为0.9，就能说模型有90%把握选对吗？ {#cross-conditional-mass-confidence}

??? note "展开答案与例子"

    **答案：** 不能。System One重排只在候选字母间归一化，即使这些字母在全词表里总质量很小，也会得到一个和为一的分布。MetaEncoder的温度softmax同样表达当前候选间相对匹配。是否校准到真实正确率，需要独立标注数据检验；相对份额本身不是正确性保证。

    **教学例子：** 示意：两个候选字母在全词表中的概率为0.009和0.001，候选内就得到0.9与0.1，但模型其余0.99质量落在别的token上。

    对照来源：[system-one-rerank](../../../multimodal-models/2610.28435-system-one-rerank/README.md) · [metaencoder](../../../foundation-models/2610.11316-metaencoder/README.md)

### 与LLM2Jev有限候选Choice多了什么困难？ {#cross-nov19-jeveration}

??? note "展开答案与例子"

    **答案：** 整图有多个位置，既要符合提示又要跨位置协调；单个候选softmax没有学习空间联合分布的负担。

    **教学例子：** 教学例：选一张现成图片与生成128个相互一致的code不是同一任务。

    对照来源：[jeveration](../../../system-one/2611.24738-jeveration/README.md) · [llm2jev](../../../foundation-models/2610.02076-llm2jev/README.md)

### 与System One多模态重排的候选排序有何不同？ {#cross-nov19-egojev}

??? note "展开答案与例子"

    **答案：** 这里用分布的逆CDF选择时间中点分位数，而不是按概率取top-k；分位数可能在同一高质量bin内取多个不同时间。

    **教学例子：** 教学例：后半段概率为1、总时长10秒、预算2时为6.25和8.75秒，不是两个7.5秒。

    对照来源：[egojev](../../../system-one/2611.24616-egojev/README.md) · [system-one-rerank](../../../multimodal-models/2610.28435-system-one-rerank/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-19** · System One多模态重排把一个联合候选分布用于排序；EgoJev将分布用于时间预算分配。前者单token字母读出不能不加检查地替代后者多token数字标签概率，frame quantile也不是单纯top-k帧。 高成本完整实验不复现，组件与能力证据分开。

涉及：[egojev](../../../system-one/2611.24616-egojev/README.md) · [system-one-rerank](../../../multimodal-models/2610.28435-system-one-rerank/README.md)

**2026-11-19** · LLM2Jev把候选标签读成有限决策分布；Jeveration还必须协调空间上众多输出，并学会使用共同随机状态。单选候选打分成功，不证明整图联合分布或图像质量。 高成本完整实验不复现，组件与能力证据分开。

涉及：[jeveration](../../../system-one/2611.24738-jeveration/README.md) · [llm2jev](../../../foundation-models/2610.02076-llm2jev/README.md)

**2026-10-27** · 首版：比较llm2jev、metaencoder、mjev-spatial、system-one-rerank，梳理评分来自语言词表、原生注意力还是向量相似度与候选是否联合上下文化及哪些表示可以缓存，并补充跨论文问答。

覆盖 9 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 11 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Chinese-Jev: Bringing System One Model to Chinese-Language Tasks](../../../foundation-models/2609.36965-chinese-jev/README.md)
- [EditJev: System One Routing for Image Editing Models](../../../foundation-models/2610.32635-editjev/README.md)
- [GLiClass: Generalist Lightweight Model for Sequence Classification Tasks](../../../foundation-models/2508.07662-gliclass/README.md)
- [Jev-as-a-Judge for Brazilian Portuguese Information Retrieval: Relevance Assessment and Reranking](../../../foundation-models/2610.23346-jev-portuguese-ir/README.md)
- [LLM2Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them](../../../foundation-models/2610.02076-llm2jev/README.md)
- [MetaEncoder: Exploring the Limit of Bi-Encoders for Multimodal System One Decision Making with Natural Language Interface](../../../foundation-models/2610.11316-metaencoder/README.md)
- [MJev-Spatial: System One Spatial Intelligence via Native Attention Matching](../../../foundation-models/2610.22276-mjev-spatial/README.md)
- [PathJev: Decision-Native Vision–Language Modelling for Histopathology](../../../foundation-models/2610.32478-pathjev/README.md)
- [Multimodal Reranking Is a System One Decision](../../../multimodal-models/2610.28435-system-one-rerank/README.md)
- [Jeveration: System One Models Now Generate](../../../system-one/2611.24738-jeveration/README.md)
- [EgoJev: Finding Evidence in Egocentric Video by Reading VLM Decisions](../../../system-one/2611.24616-egojev/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/system-one/typed-readout.md) · [返回全部精读卡片](../index.md)
