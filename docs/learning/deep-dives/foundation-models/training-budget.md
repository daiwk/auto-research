---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 训练预算：改数据、改更新方向，还是改比较口径

[基础模型](../index.md) · 更新 2026-10-27 · 28 篇主题资料 / 6 篇重点对照

同一预算内训练得更好，可能来自更合适的数据、逐样本处理、更有效更新或更低状态开销。DoReMi、Mixing Laws、DataOrchestra、Muon 和 ECO 改动不同环节；Muon Paired Budget 则提醒先冻结选参规则，再分别回答等数据和等时间问题。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/foundation-models/training-budget.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：改变数据出现频率、数据内容还是参数更新 · 使用在线反馈、先导拟合或离线教师 · 成本包含预处理、试验选参与优化器开销到哪一层 · 比较按数据量、墙钟还是冻结候选池预算

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining](../../../reproductions/2305.10429-doremi/README.md) · [原始来源](https://arxiv.org/abs/2305.10429)<br>章节：背景与主要改动、核心公式、复现边界 | 小 proxy 根据各域相对 reference 的 excess loss 做 group DRO，再把学得配比交给目标模型。 | 依赖 proxy 的域价值可迁移；本地两域 unigram 只核验配比路径，不能代替大型 target 的训练结果。 |
| [Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance](../../../reproductions/2403.16952-data-mixing-laws/README.md) · [原始来源](https://arxiv.org/abs/2403.16952)<br>章节：背景与主要改动、核心公式、复现边界 | 先执行多组 pilot mixture，拟合域损失随比例与规模的变化，再搜索未训练配比。 | 需要为先导实验付费，并承担模型与预算外推误差；本地小 proxy 不等于真实多规模 scaling curve。 |
| [DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data](../../../reproductions/2607.24717-data-orchestra/README.md) · [原始来源](https://arxiv.org/abs/2607.24717)<br>章节：背景与主要改动、核心公式、复现边界 | 逐 chunk 选择 Drop、Untouch 或 Clean，清洗时再安排去噪、表面修复与教学增强。 | 改变内容而非只改采样率，必须防止过度删除和改写；本地规则工具的负结果保留，不冒充原文大模型清洗。 |
| [Muon is Scalable for LLM Training](../../../reproductions/2502.16982-muon/README.md) · [原始来源](https://arxiv.org/abs/2502.16982)<br>章节：背景与主要改动、核心公式、复现边界 | 以 momentum 矩阵近似极分解形成隐藏矩阵更新方向，其他参数仍用辅助 AdamW。 | 每步更新几何不同，正交化与辅助优化器也有时间开销；本地短预算没有复现论文规模效率。 |
| [When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark](../../../foundation-models/2610.21555-muon-paired-budget/README.md) · [原始来源](https://arxiv.org/abs/2610.21555)<br>章节：背景与主要改动、核心公式、代码映射与边界 | 固定初始化、数据顺序与开发候选池，分别用数据 AUC、时间 AUC 和选参 regret 评价优化器。 | 它是比较协议而非新优化公式；本地只做合成轨迹诊断，没有训练 Muon 或 AdamW。 |
| [ECO: Quantized Training without Full-Precision Master Weights](../../../foundation-models/2601.22101-eco-optimizer/README.md) · [原始来源](https://arxiv.org/abs/2601.22101v1)<br>章节：背景与主要改动、核心公式、本地复现与成本判断 | 直接更新低精度权重，把重量化误差注入已有动量，避免常驻 master weights。 | Adam 需逐元素有效步长，格式与舍入会影响误差；无缓冲规则不是任意情况精确等价。本地未实现或训练，完整实验高成本。 |

</div>

## 取舍分析 {#analysis}

### 选更多某域，与把该域内容改写，是两个干预

DoReMi 根据 excess loss 调整域频率，Mixing Laws 通过 pilot 曲线预测配比，两者主要改变见到什么比例。DataOrchestra 直接决定每个 chunk 是否保留和如何编辑，会改变监督本身。清洗后语料更多或平均 loss 更低，都不能说明目标任务必然获益；要区分数据量变化、内容变化以及预处理费用。一个可复核实验应明确固定的是原始 token、处理后 token 还是训练步数。

对照来源：[doremi](../../../reproductions/2305.10429-doremi/README.md) · [data-mixing-laws](../../../reproductions/2403.16952-data-mixing-laws/README.md) · [data-orchestra](../../../reproductions/2607.24717-data-orchestra/README.md)

### 预算口径可以让结论反转

Muon 改变每步下降方向，ECO 改变持久状态与量化更新，二者都可能改变每步耗时。Muon Paired Budget 的价值在于把等数据与等时间分开，并冻结开发阶段选参，不为每种报告口径重新挑冠军。训练比较还要包括辅助 AdamW、预处理或 pilot 的实际成本；本地公式诊断与合成曲线只验证这些记账规则，不能作为真实训练效率胜负。

对照来源：[muon](../../../reproductions/2502.16982-muon/README.md) · [eco-optimizer](../../../foundation-models/2601.22101-eco-optimizer/README.md) · [muon-paired-budget](../../../foundation-models/2610.21555-muon-paired-budget/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 某个数据域训练效果差，为什么提高 DoReMi 权重与让 DataOrchestra 清洗它，可能朝相反方向改变训练集？ {#cross-mixture-versus-rewrite}

??? note "展开答案与例子"

    **答案：** DoReMi 将相对 reference 欠拟合的域赋予更多采样机会，默认域内内容仍值得学习；DataOrchestra 可能把某些 chunk 删除、保留或重写，直接改变有效内容。若差来自噪声，提高频率可能重复坏监督；若内容本来干净，强清洗又可能删掉有用信息。应先辨别问题，再用相同训练预算比较干预。

    **教学例子：** 教学例：罕见但正确的公式相对reference的excess loss高，可能值得更多曝光；乱码也可能难学，却应先清理。要区分域级学习价值与样本质量。

    对照来源：[doremi](../../../reproductions/2305.10429-doremi/README.md) · [data-orchestra](../../../reproductions/2607.24717-data-orchestra/README.md)

### DoReMi 与 Data Mixing Laws 都用小实验选大模型配比，依赖的迁移假设有什么不同？ {#cross-proxy-feedback-versus-law}

??? note "展开答案与例子"

    **答案：** DoReMi 依赖 proxy 的 excess-loss 动态能识别值得提高权重的域；Mixing Laws 依赖先导配比与规模数据足以拟合损失面，并预测未执行的组合。前者把反馈转成更新，后者把实验转成可外推模型，都可能被 proxy 与目标模型差异破坏。先导成本和独立目标评测都应保留，不能拿拟合值当已训练结果。

    **教学例子：** 教学例：小 proxy 认为代码域最欠拟合，但大模型可能已掌握它；同样，拟合曲线也可能在极端配比外推失败。

    对照来源：[doremi](../../../reproductions/2305.10429-doremi/README.md) · [data-mixing-laws](../../../reproductions/2403.16952-data-mixing-laws/README.md)

### Muon 在相同 token 下 loss 更低，为什么还不能宣布它在固定训练时间内更划算？ {#cross-equal-steps-versus-time}

??? note "展开答案与例子"

    **答案：** 相同 token 控制了数据暴露，未控制单步正交化、辅助 AdamW 或系统吞吐开销。Paired Budget 应在共同实际时间范围比较验证曲线，并沿用已冻结开发选择，而不是为时间结果重新挑配置。ECO 的状态节省也需另测：减少存储不保证每步更快，质量与资源必须分别报告。

    **教学例子：** 教学例：方案甲每步更有效但慢一倍，方案乙在同一小时可多看数据；等步数赢家未必仍是等时间赢家。

    对照来源：[muon](../../../reproductions/2502.16982-muon/README.md) · [muon-paired-budget](../../../foundation-models/2610.21555-muon-paired-budget/README.md) · [eco-optimizer](../../../foundation-models/2601.22101-eco-optimizer/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较域配比学习、配比曲线外推、逐样本处理、矩阵优化与低精度状态，并用配对预算协议解释结论口径。

覆盖 28 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 28 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization](../../../foundation-models/2610.12444-adamw4bit/README.md)
- [AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models](../../../foundation-models/2610.01395-af-muon/README.md)
- [BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks](../../../foundation-models/2610.22256-bit-sparse/README.md)
- [BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility](../../../foundation-models/2610.23571-bmuon/README.md)
- [Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance](../../../reproductions/2403.16952-data-mixing-laws/README.md)
- [DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data](../../../reproductions/2607.24717-data-orchestra/README.md)
- [Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models](../../../foundation-models/2603.01293-data-quality-lsa/README.md)
- [DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining](../../../reproductions/2305.10429-doremi/README.md)
- [ECO: Quantized Training without Full-Precision Master Weights](../../../foundation-models/2601.22101-eco-optimizer/README.md)
- [GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries](../../../reproductions/2607.20757-gaugequant/README.md)
- [Customizing an LLM for Enterprise Software Engineering](../../../foundation-models/2605.16517-gemini-for-google/README.md)
- [Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs](../../../foundation-models/2610.22230-hardware-diversity/README.md)
- [Hierarchical Latent Prediction for Language Models](../../../reproductions/2608.05806-hilp/README.md)
- [LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning](../../../foundation-models/2610.31911-lazyflash/README.md)
- [LCT: Losslessly Compressed Tensors with GPU friendly execution for Training](../../../foundation-models/2610.22179-lct/README.md)
- [Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement](../../../foundation-models/2601.21149-me-pois/README.md)
- [A Theoretical Framework for Modular Learning of Robust Generative Models](../../../foundation-models/2602.17554-modular-robust-generative/README.md)
- [Muon is Scalable for LLM Training](../../../reproductions/2502.16982-muon/README.md)
- [When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark](../../../foundation-models/2610.21555-muon-paired-budget/README.md)
- [Musec: MomentUm SpEctral Clipping for Stable Muon-type Training](../../../foundation-models/2609.11655-musec/README.md)
- [OPEN-1B: A Fully Auditable Training Run](../../../foundation-models/2609.17380-open-1b-audit/README.md)
- [OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research](../../../reproductions/2607.16669-open-language-model/README.md)
- [PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning](../../../reproductions/2607.18199-ppl-factory/README.md)
- [Reverse-KL Policy Distillation: Statistical Guarantees and Limits](../../../foundation-models/2610.30844-rkl-policy-distillation/README.md)
- [Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon](../../../reproductions/2610.19844-smrc-pmrc/README.md)
- [T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training](../../../foundation-models/2610.24938-t-muon/README.md)
- [TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning](../../../foundation-models/2610.02199-taco-optimizer/README.md)
- [TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)](../../../foundation-models/2610.02092-tess/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/training-budget.md) · [返回全部精读卡片](../index.md)
