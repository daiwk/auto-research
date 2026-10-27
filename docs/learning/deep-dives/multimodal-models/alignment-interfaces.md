---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 多模态对齐到底对齐什么：向量、视觉接口还是证据依赖

[多模态](../index.md) · 更新 2026-10-27 · 20 篇主题资料 / 6 篇重点对照

CLIP与EmbeddingGemma 2产出可比较向量，BLIP-2与LLaVA连接视觉到条件生成，CV-OPD训练证据依赖，UMRM给回答评分。它们的输出合同和监督对象不同，不是同一条从小到大的能力排行榜。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/multimodal-models/alignment-interfaces.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：输出对象：检索向量、视觉token、生成回答、reward · 训练部件：双塔、连接器、策略分布、冻结表征上的头 · 证据约束：配对相似、指令监督、视图对照、扰动偏好 · 成本位置：视觉token长度、embedding维度、教师与评分器

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Learning Transferable Visual Models From Natural Language Supervision](../../../reproductions/2103.00020-clip/README.md) · [原始来源](https://arxiv.org/abs/2103.00020)<br>章节：背景与主要改动、核心公式、复现边界 | 独立图文encoder映射到单位球面，用对称批内对比目标学习相似度。 | 类别文本可作零样本原型，但相似度不是开放回答；本地服饰图像双塔不代表四亿图文预训练。 |
| [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../../../reproductions/2301.12597-blip2/README.md) · [原始来源](https://arxiv.org/abs/2301.12597)<br>章节：背景与主要改动、核心公式、复现边界 | 固定数量learnable query经Q-Former交叉注意力提取视觉信息，接给冻结LLM。 | 可训练瓶颈控制视觉接口长度，也可能遗漏细节；本地四query未复刻两阶段大模型训练。 |
| [Visual Instruction Tuning](../../../reproductions/2304.08485-llava/README.md) · [原始来源](https://arxiv.org/abs/2304.08485)<br>章节：背景与主要改动、核心公式、复现边界 | projector将视觉特征接入语言token空间，再用多模态指令监督学习条件回答。 | 形状对齐不能代替语义与指令训练；本地轻量问答头未执行GPT-4指令数据生成或LLaVA-13B。 |
| [EmbeddingGemma 2: Open Multimodal Embeddings](../../../multimodal-models/embeddinggemma2/README.md) · [原始来源](https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/)<br>章节：背景与主要改动、核心公式、结果与边界 | 独立模态塔输出统一768维向量，MRL支持规定前缀截断后再归一化。 | 缩短向量与压缩视觉输入是不同预算；本地使用官方checkpoint仅验证文本、图像，未接全四模态。 |
| [CV-OPD: Contrastive Vision On-policy Distillation](../../../reproductions/2610.13264-cv-opd/README.md) · [原始来源](https://arxiv.org/abs/2610.13264)<br>章节：背景与主要改动、核心公式、本地结果与边界、2026-10-14 A100 实测 | 学生读全图，正负教师只改crop且共享学生前缀，用JSD和CDL约束正确视觉依赖。 | 负crop构造、样本门与token门都影响监督；本地有真实VLM L1更新及A100诊断，非完整视觉能力复现。 |
| [Unsupervised Multimodal Reward Modeling](../../../reproductions/2610.12707-umrm/README.md) · [原始来源](https://arxiv.org/abs/2610.12707)<br>章节：背景与主要改动、核心公式、数据协议与verifier边界、本地结果与验证状态 | 冻结VLM中间层，只池化response并训练无bias奖励头，以caption扰动构造偏好。 | 无人工偏好不等于全流程无标签；development选层和bootstrap verifier仍使用监督，局部奖励准度不保证真实policy选择效用。 |

</div>

## 取舍分析 {#analysis}

### 统一空间与语言输入空间，不能只因维度相同就互换

CLIP和EmbeddingGemma 2要求向量在任务相似度下可比较，后者还允许规定维度的MRL读取。BLIP-2的query输出与LLaVA的视觉投影则是LLM条件输入，需要语言生成训练接纳这些信号。一个检索向量语义相近，不等于它已经是能被任意LLM直接读取的视觉软提示。

对照来源：[clip](../../../reproductions/2103.00020-clip/README.md) · [embedding-gemma2](../../../multimodal-models/embeddinggemma2/README.md) · [blip2](../../../reproductions/2301.12597-blip2/README.md) · [llava](../../../reproductions/2304.08485-llava/README.md)

### 回答看起来好，与回答确实利用图像是两个问题

UMRM从caption扰动学习reward，进一步检验policy自产候选的选择效用，避免只在人工负例上自证。CV-OPD则在相同学生前缀上改变教师视觉证据，直接约束正负视图的分布关系。前者是评价器与负样本分布，后者是策略蒸馏关系；它们可以互补，却不能用一个reward benchmark证明完整视觉归因。

对照来源：[umrm](../../../reproductions/2610.12707-umrm/README.md) · [cv-opd](../../../reproductions/2610.13264-cv-opd/README.md) · [llava](../../../reproductions/2304.08485-llava/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### CLIP或EmbeddingGemma 2把图片检索对了，为什么不能直接算作LLaVA已经会回答图像问题？ {#cross-embedding-versus-answer}

??? note "展开答案与例子"

    **答案：** 检索要求在候选表示间找到匹配，LLaVA要求根据图像、问题与历史生成回答token。前者没有自动提供生成接口或指令监督；EmbeddingGemma 2的统一空间也不改变这一点。要比较，应先固定同一种输出任务，而不是把相似度命中与回答正确合并成一列。

    **教学例子：** 教学例子：找到“桌上有杯子”的图片，不等于能按用户要求回答杯子数量、说明依据并遵守输出格式。

    对照来源：[clip](../../../reproductions/2103.00020-clip/README.md) · [embedding-gemma2](../../../multimodal-models/embeddinggemma2/README.md) · [llava](../../../reproductions/2304.08485-llava/README.md)

### BLIP-2减少query数量，与EmbeddingGemma 2缩短embedding维度，节约的是同一类开销吗？ {#cross-two-compression-axes}

??? note "展开答案与例子"

    **答案：** 不是。Q-Former query数影响送给语言侧的视觉序列长度，MRL维度影响最终检索向量的存储与相似度计算。两者都可能损失信息，但压缩位置不同；MRL还要求使用训练规定前缀并重新归一化，不能用删向量坐标代替视觉token聚合。

    **教学例子：** 教学例子：送给LLM的32个视觉token与每条检索向量256维，是序列长度和向量宽度两个数字，不可直接比较大小。

    对照来源：[blip2](../../../reproductions/2301.12597-blip2/README.md) · [embedding-gemma2](../../../multimodal-models/embeddinggemma2/README.md)

### UMRM能分辨caption颜色扰动，就足以证明CV-OPD学生依赖了正确图像区域吗？ {#cross-reward-versus-visual-dependence}

??? note "展开答案与例子"

    **答案：** 不够。UMRM测试奖励头在某类负样本上如何排序，真实policy错误分布可能不同；CV-OPD要比较同前缀下正负crop教师与学生的分布关系。奖励头判对、学生获得该信号、学生实际改为使用证据，是不同环节，需要各自验证。

    **教学例子：** 教学例子：裁判能发现“红”被改成“蓝”，不表示学生训练后已停止只凭常见物体颜色猜答案。

    对照来源：[umrm](../../../reproductions/2610.12707-umrm/README.md) · [cv-opd](../../../reproductions/2610.13264-cv-opd/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较CLIP/EmbeddingGemma 2检索空间、BLIP-2/LLaVA视觉接口、CV-OPD证据依赖与UMRM奖励；已阅20篇摘要，精读6篇。

覆盖 20 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 20 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../../../reproductions/2301.12597-blip2/README.md)
- [Learning Transferable Visual Models From Natural Language Supervision](../../../reproductions/2103.00020-clip/README.md)
- [From Visual Cues to Spoken Narration: Rethinking Audio Description](../../../multimodal-models/2609.01725-cue2narrate-drl/README.md)
- [CV-OPD: Contrastive Vision On-policy Distillation](../../../reproductions/2610.13264-cv-opd/README.md)
- [EmbeddingGemma 2: Open Multimodal Embeddings](../../../multimodal-models/embeddinggemma2/README.md)
- [FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation](../../../multimodal-models/2610.32976-flexglue/README.md)
- [Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction](../../../reproductions/2608.12209-gas/README.md)
- [LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation](../../../foundation-models/2610.22182-lamp/README.md)
- [Visual Instruction Tuning](../../../reproductions/2304.08485-llava/README.md)
- [MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations](../../../reproductions/2608.25575-mllmclip/README.md)
- [MVEB: Massive Video Embedding Benchmark](../../../multimodal-models/2606.14958-mveb/README.md)
- [NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages](../../../multimodal-models/2604.16287-naijas2st/README.md)
- [Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation](../../../foundation-models/2610.02148-omni-embed-mini/README.md)
- [Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes](../../../reproductions/2608.05000-physics-mm-pretraining/README.md)
- [ReToken: One Token to Improve Vision–Language Models for Visual Retrieval](../../../reproductions/2607.28627-retoken/README.md)
- [SenseNova-U1.5: Towards Native Unified Visual Intelligence](../../../foundation-models/2609.11929-sensenova-u1-5/README.md)
- [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](../../../reproductions/2502.14786-siglip2/README.md)
- [SmolVLM: Redefining small and efficient multimodal models](../../../reproductions/2504.05299-smolvlm/README.md)
- [Unsupervised Multimodal Reward Modeling](../../../reproductions/2610.12707-umrm/README.md)
- [WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report](../../../reproductions/2608.24053-wemm-embedding/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/multimodal-models/alignment-interfaces.md) · [返回全部精读卡片](../index.md)
