---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 能力证据：准确打分、节省观测与解释预测

[基础模型](../index.md) · 更新 2026-10-27 · 13 篇主题资料 / 5 篇重点对照

先区分“正确答案怎样定义”“下一题测谁”“多个裁判怎样融合”和“预测怎样解释”。XLGoBench、ProEval、FUSE、TCAB 与 DetectorScope 分别改变这些环节；观测更少或解释可加，不等于被测能力本身更强。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/foundation-models/evaluation-and-evidence.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：输出是任务正确标签、总分后验、候选排序还是可加解释 · 真实标签何时可见、由谁持有 · 依赖算法确定性、跨模型相关性还是验证器识别假设 · 节约的是评分调用、重复反馈还是解释成本

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks](../../../foundation-models/2605.30788-xlgobench/README.md) · [原始来源](https://arxiv.org/abs/2605.30788v1)<br>章节：背景与主要改动、核心公式、复现边界 | 用确定性算法任务与精确 scorer 定义答案，模型只见 task/problem，不读取评分器 gold。 | 检查的是给定算法族和复杂度，不自动覆盖开放问答；本地五任务小实例没有完整多语言或复杂度矩阵。 |
| [ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation](../../../foundation-models/2604.23099-proeval/README.md) · [原始来源](https://arxiv.org/abs/2604.23099)<br>章节：背景与主要改动、核心公式、代码映射与边界 | 根据历史模型逐题相关性建立经验GP，对目标总分和不确定度建模，选择有价值的新观测。 | 后验依赖历史关系可迁移；目标分数只能查询后揭示。本地四题数学夹具不构成真实模型评测节省。 |
| [FUSE: Ensembling Verifiers with Zero Labeled Data](../../../foundation-models/2604.18547-fuse-verifiers/README.md) · [原始来源](https://arxiv.org/abs/2604.18547v1)<br>章节：背景与主要改动、核心公式、本地复现与成本判断 | 从多个验证器的分数矩阵估计质量与正确后验，再学习集成，真实正确标签留给外部评价。 | 依赖多数优于随机、条件独立等识别假设，不保证相关裁判下可靠；本地尚未实现集成器。 |
| [Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing](../../../reproductions/2608.12831-tcab/README.md) · [原始来源](https://arxiv.org/abs/2608.12831)<br>章节：背景与主要改动、核心公式、复现边界 | 最大耦合让自适应策略在相同决策时共享反馈，以树结构组织共享，同时维持各策略边际轨迹。 | 节省反馈要求正确耦合，不能任意复制异动作回报；本地 mini-suite 不证明理论渐近节约或生产A/B收益。 |
| [Building Auditable AI Text Detectors with Sparse Autoencoders](../../../foundation-models/2610.30006-detector-scope/README.md) · [原始来源](https://arxiv.org/abs/2610.30006v1)<br>章节：背景与主要改动、核心公式、代码映射与边界 | 把外部SAE概念筛选后交给稀疏线性头，输出可由池化特征置零核验的logit贡献。 | 解释是特征级而非改写文本的因果效果；本地只验合成激活上的L1组件，未训练完整检测器或SAE。 |

</div>

## 取舍分析 {#analysis}

### 确定性评分与概率替身，各自回答什么

XLGoBench 由算法生成精确答案，适合判断一次结构化输出是否合规；ProEval 不是替任务重新定义正确性，而是利用已观测分数推断未全测模型的总体表现。后验均值和方差来自模型关系，不是每道题已被真实评分。两者可以组合：先确保 scorer 与 gold 隔离，再决定哪些真实评分最值得付费，保留预测与已测两种状态。

对照来源：[xlgobench](../../../foundation-models/2605.30788-xlgobench/README.md) · [proeval](../../../foundation-models/2604.23099-proeval/README.md)

### 多一层证据，不等于无条件可靠

FUSE 试图利用多个验证器而不直接读取真实标签，但其后验仍受相关性和识别假设限制。DetectorScope 的线性结构可精确分解 logit，却只证明某个池化特征对预测的数值贡献，不证明概念描述或输入文本的因果关系。TCAB 则约束共享反馈时的边际分布。三者把不同环节做得更可检查，不能互相代替，更不能仅凭解释流畅或反馈复用率高宣布能力已验证。

对照来源：[fuse-verifiers](../../../foundation-models/2604.18547-fuse-verifiers/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md) · [tcab](../../../reproductions/2608.12831-tcab/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 用 ProEval 少测一批模型时，为什么仍需像 XLGoBench 那样明确真实 scorer 和 gold 隔离？ {#cross-oracle-versus-surrogate}

??? note "展开答案与例子"

    **答案：** ProEval 只改变评分获取和总分估计方式，真实观测仍必须来自合法任务评价。若目标答案提前进入模型输入，或未选题的目标分数进入后验，相关性再漂亮也在估计被污染结果。应把未查询预测、已查询分数和评分器内部答案分开；精确 scorer 的存在也不授权策略读取它的隐藏状态。

    **教学例子：** 教学例：代理选择第二题后才能拿到第二题分数；若初始化就用整张目标分数表建模型，就不能再声称通过少量查询估计。

    对照来源：[proeval](../../../foundation-models/2604.23099-proeval/README.md) · [xlgobench](../../../foundation-models/2605.30788-xlgobench/README.md)

### FUSE 估计的“正确后验”与 DetectorScope 的“概念贡献”，为什么都不能直接当作事实正确证明？ {#cross-posterior-versus-explanation}

??? note "展开答案与例子"

    **答案：** FUSE 后验由验证器分数和识别假设估计，若裁判共同犯错或假设失效，概率也会偏；DetectorScope 的贡献精确说明池化特征置零后的 logit 差，却不证明概念解释真实或原文因果关系。一个是选择可靠性的统计模型，一个是预测函数的可加结构，需要分别接受独立标签与解释验证。

    **教学例子：** 教学例：几个裁判都偏爱长答案会共同误判；一个检测特征贡献很大，也可能只是数据集线索，而非真正的生成来源原因。

    对照来源：[fuse-verifiers](../../../foundation-models/2604.18547-fuse-verifiers/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

### TCAB 共享同一决策的反馈，与 ProEval 根据历史相关性推断未测分数，为什么不能混记为真实观测？ {#cross-shared-feedback-versus-imputed-feedback}

??? note "展开答案与例子"

    **答案：** TCAB 的共享建立在耦合后相同决策可复用实际反馈，同时维持各策略边际过程；ProEval 则根据历史协方差对尚未查询项形成后验。后者是推断值，前者也只有满足共享条件才可复用。无论哪种节省，都不能把不同动作的未知回报或未测题分数写成已经执行的结果。

    **教学例子：** 教学例：两个策略同选动作甲可复用甲的反馈；策略乙选了动作乙，就不能把甲的成功抄给它，哪怕历史上二者表现相关。

    对照来源：[tcab](../../../reproductions/2608.12831-tcab/README.md) · [proeval](../../../foundation-models/2604.23099-proeval/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较精确算法评分、概率评测替身、无标签验证器融合、反馈耦合与可加概念解释，明确观测和推断的边界。

覆盖 13 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 13 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Detecting Safety Training Modification in Language Models via Activation Analysis](../../../foundation-models/2608.05578-activation-model-scanner/README.md)
- [Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking](../../../foundation-models/2510.01637-combinatorial-watermark/README.md)
- [CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes](../../../foundation-models/2608.27455-criticl/README.md)
- [Cross-Lingual Exploration for Parametric Knowledge](../../../foundation-models/2606.24579-cross-lingual-exploration/README.md)
- [DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia](../../../foundation-models/2610.26155-deepsea/README.md)
- [Building Auditable AI Text Detectors with Sparse Autoencoders](../../../foundation-models/2610.30006-detector-scope/README.md)
- [FUSE: Ensembling Verifiers with Zero Labeled Data](../../../foundation-models/2604.18547-fuse-verifiers/README.md)
- [Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4](../../../foundation-models/2609.30716-gemma-priority-protocol/README.md)
- [How Calibration Content Shapes Attention-Based Reranking](../../../foundation-models/2609.17764-interpolated-null-calibration/README.md)
- [Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders](../../../foundation-models/2507.23220-mechanistic-etm/README.md)
- [ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation](../../../foundation-models/2604.23099-proeval/README.md)
- [Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing](../../../reproductions/2608.12831-tcab/README.md)
- [XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks](../../../foundation-models/2605.30788-xlgobench/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/evaluation-and-evidence.md) · [返回全部精读卡片](../index.md)
