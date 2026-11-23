---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 能力证据：准确打分、节省观测与解释预测

[基础模型](../index.md) · 更新 2026-11-23 · 29 篇主题资料 / 21 篇重点对照

先区分“正确答案怎样定义”“下一题测谁”“多个裁判怎样融合”和“预测怎样解释”。XLGoBench、ProEval、FUSE、TCAB 与 DetectorScope 分别改变这些环节；观测更少或解释可加，不等于被测能力本身更强。XLA from the Trenches还提醒：评分之前，编译后程序本身就可能静默偏离原始数值语义，不能把编译成功当作执行正确。

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
| [XLA from the Trenches: Correctness on TPU Workloads at Scale](../../../foundation-models/2611.00624-xla-trenches/README.md) · [原始来源](https://arxiv.org/abs/2611.00624)<br>章节：核心机制与数值例子、论文工程与线上证据、资源与复现边界 | 在合法输入和目标TPU数值语义下做差分检查，从大图隔离到完整fusion内部VREG，避免调试拆图改变故障。 | 编译器正确性证据不是模型能力分数；内部生产图和TPU工具不可用，公开OpenXLA只是部分链路，本地review-only且无CUDA替身。 |
| [Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics](../../../foundation-models/2508.11017-rosetta-unification/README.md) · [原始来源](https://arxiv.org/abs/2508.11017v1)<br>章节：背景与主要改动、核心机制与公式、原文结果与限制、本地复现 | 同一事实以不同语言出现时，模型可能把它们存成互不相通的表征。作者在受控合成知识图谱上从零训练小型 Transformer，分别改变平行事实比例、语言频率差异和语言可提取性，发现同语言准确率接近满分并不代表跨语言迁移良好。 | Rosetta观察/干预预训练语言分布及表示统一度；Thinking to Recall分析推理时自生成事实及其正确性。前者的相似度不是事实真值judge，后者的oracle条件准确率也不证明跨语言表示统一。 |
| [Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs](../../../foundation-models/2603.09906-thinking-to-recall/README.md) · [原始来源](https://arxiv.org/abs/2603.09906v1)<br>章节：背景与主要改动、核心机制与公式、原文结果与限制、本地复现 | 推理不仅可能分解复杂任务，也可能通过额外计算和相关事实的自检索帮助单跳知识召回。论文控制同一 hybrid 模型的 reasoning ON/OFF，区分计算缓冲与 factual priming，同时发现中间事实幻觉会连带增加最终答案错误。 | 本地实现不能；它使用事后外部标注的事实真值模拟条件期望，只是离线oracle分析。要部署还需要不看gold的可靠事实验证器，并计入调用成本和误判；这不是由汇总公式自动得到的。 |
| [Improving Latent Generalization Using Test-time Compute](../../../foundation-models/2604.01430-latent-generalization/README.md) · [原始来源](https://arxiv.org/abs/2604.01430v1)<br>章节：背景与主要改动、核心机制与公式、原文结果与限制、本地复现 | 模型记住 A&gt;B 并不必然推出 B&lt;A，记住多个关系也不保证能答出未显式训练的组合。论文把知识获取、会思考的轨迹引导、正确性RL分开，研究在一个结构训练出的推理能力能否迁移到仅做知识SFT的另一个结构。 | 前者用受控知识获取和结构划分考察未显式答案的泛化；后者研究已有参数事实如何因计算和factual priming被读出。两者都不能把gold-conditioned teacher或事后标注暴露给最终actor。 |
| [The Illusion of Stochasticity in LLMs](../../../foundation-models/2604.06543-llm-stochasticity/README.md) · [原始来源](https://arxiv.org/abs/2604.06543v1)<br>章节：核心机制与公式、原文结果与限制、本地复现 | 以固定计数的外部已完成样本，分别检验边缘分布拟合与时间依赖；卡方/KS的p值是检验统计证据，不是某个输出事件的概率。 | 解码约束Beam对明确top-k归一化后的路径分布累加质量，给目标近逐字事件的确定性LB与可能质量bank；它不证明随机数独立。反过来，直方图未拒绝均匀不能替代路径风险界。两者都须固定被审计的分布、协议与证据侧边界。 |
| [Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics](../../../foundation-models/2510.22028-qe-length-normalization/README.md) · [原始来源](https://arxiv.org/abs/2510.22028v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 在质量受控的同文档前缀上诊断长度漂移，训练错误密度R/\|h\|并在推理恢复评分；本地为目标/控制协议组件。 | 这不是对冻结QE分数做后处理；Interpolated Null Calibration从真实三次模型读出扣除可插值的null基线，不改变QE监督目标。两者均须validation选择可调项，不用测试结果反推校准。 |
| [Steering LLMs for Culturally Localized Generation](../../../foundation-models/2603.23301-cultural-cue/README.md) · [原始来源](https://arxiv.org/abs/2603.23301v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 对外部SAE token激活取max，以累计文化MI选维度，再按国家原型差和decoder构造残差干预。 | MI估计/SAE/语言模型和judge外置；国家等权不是样本等权。与DetectorScope描述mask及稀疏检测头的监督目标不同。 |
| [Estimating near-verbatim extraction risk in language models with decoding-constrained beam search](../../../foundation-models/2603.24917-decoding-constrained-beam/README.md) · [原始来源](https://arxiv.org/abs/2603.24917v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 在实际top-k解码分布上累积精确路径概率，用可行性剪枝和末步全扩展给近逐字事件的确定性概率界。 | 需要外部模型logits与目标后缀；不是来源检测或无偏完整风险估计。bank是潜在质量，不是已验证成功；无可选τ早停/KV模型。 |
| [StoryScope: Investigating idiosyncrasies in AI fiction](../../../foundation-models/2604.03136-storyscope/README.md) · [原始来源](https://arxiv.org/abs/2604.03136v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 语义叙事赋值经prompt匹配分析和真实SHAP统计选稳定跨模型核心；本地精确执行核心合取与prompt-block索引。 | 叙事特征不是SAE随机列，分类重要性不是生成因果；外部LLM/XGBoost/SHAP阶段与未量化指纹门槛不伪造。 |
| [Inherited Weights: Measuring the Tokenization Premium and the Sovereignty Cost of Language Models for the Global South](../../../foundation-models/2611.13441-tokenization-premium/README.md) · [原始来源](https://arxiv.org/abs/2611.13441v1)<br>章节：背景与主要改动、核心公式、论文离线与线上效果 | 先拼接相同UDHR共同条款再一次编码，比较总token成本并排除UNK坍缩；同时约束全样本ECE、覆盖率/风险与全程能量分母。 | XLGoBench固定抽象算法实例与复杂度来比较跨语言任务能力，token溢价只测相同内容的输入成本。两者都需语言内容可比，但token数不能替代模型错误率；本地两个scorer均不等于完整多语能力矩阵。 |
| [Inference Validation for Regulated AI: A Governed Decision Pipeline for LLM Serving](../../../foundation-models/2611.12737-runway-inference-protocol/README.md) · [原始来源](https://arxiv.org/abs/2611.12737v2)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界 | 在原样AIPerf前后构建配置/缓存身份、声明式SLA和每成功请求成本，明确缓存命中只复用既有证据。 | XLA from the Trenches验证目标TPU编译数值正确性；Runway验证某serving配置是否满足指标和契约。CPU协议既不证明TPU语义，也不测CUDA吞吐；模型/引擎名字相同不能保证缓存身份相同。 |
| [Mixed Signals: Weight-Space Programming for EEG and ECG](../../../foundation-models/2611.13758-mixed-signals-weights/README.md) · [原始来源](https://arxiv.org/abs/2611.13758v1)<br>章节：核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 用原子参数补丁和受限practice反馈表达WSP接口，测试标签留在外部评价器，不用SGD替代推理编辑。 | AMS从固定激活读出结构差异，不写参数也不认证安全；WSP问能否推理改权重。当前L0线性harness不含LLM、TinyEEGNet或被试数据。 |
| [Rich Insights from Cheap Signals: Efficient Evaluations via Tensor Factorization](../../../foundation-models/2603.02029-efficient-evals-tensor/README.md) · [原始来源](https://arxiv.org/abs/2603.02029v1)<br>章节：背景与主要改动、核心公式、同主题对照、高成本完整实验 | 本文将模型、prompt和rater三者的能力张量作低rank CP分解，先用大量廉价autorater评分学共享表示，再冻结表示、只拟合人类rater向量及有序cutoff。它保留prompt异质性和rater偏好差异，不把某个自动judge分数直接当人类真值。2026-11-16是Google官方代码新仓库，不是论文首发；v1首发为2026-03-02 16:12:46 UTC。 | ProEval用其他模型历史逐题分数建立GP先验并主动决定下一题；本篇用多rater廉价数据学prompt/model表示再做人类对齐。前者的采样后验不等于后者的rater偏差校准，条件置信界也不能无条件覆盖共享表示估计误差。 |
| [Sequential Anytime Valid Tests for Efficient Inference-Time Alignment](../../../foundation-models/2611.26413-e-rwsc/README.md) · [原始来源](https://arxiv.org/abs/2611.26413v1)<br>章节：背景与主要改动、与已有方法的关系、结果、负控与边界 | 纯stdlib、CPU-only的RWSC聚合、前缀可预测下注、逐答案log资本与首现权重、首次出现跳过、认证终止和显式未认证预算回退。诊断使用明确的合成答案/奖励流，检查因果顺序、领先变化不重置、错误答案也可能被认证、softmax极值和均匀tie。没有LLM、reward model、答案解析或公开benchmark运行；不把合成流叫模型输出，不接Evolve晋级。 | LLM Stochasticity区分边缘分布拟合与时序依赖；e-RWSC的保证需要固定政策的iid响应，不能由平衡答案直方图或“请随机回答”提示推导。前者的统计诊断可暴露某些依赖，却不能证明后者的全部假设。e-RWSC也不估计答案是否符合现实：即使输入真独立，政策总偏向错误答案时仍可快速发多数证书。 |
| [Reliable Behavior Discovery via False Discovery Rate Control](../../../foundation-models/2611.27104-disco/README.md) · [原始来源](https://arxiv.org/abs/2611.27104v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | DISCO以冻结e-process与粗分箱选择接口控制行为发现集合的FDR，允许最终使用实际假设数；本地仅有未boosted二分箱统计核心。 | e-RWSC认证单题某答案的政策多数概率，不等于正确性；DISCO控制多行为假设集合的误发现比例，并为自适应假设池施加分箱、冻结与null分布校正约束。相同的e-process工具不使两类错误和证书等价。 |
| [Don&#x27;t Pause! Every prediction matters in a streaming video](../../../foundation-models/2604.24317-spot-bench/README.md) · [原始来源](https://arxiv.org/abs/2604.24317v2)<br>章节：背景与主要改动、与已有方法的关系、结果、负控与边界 | 纯CPU、stdlib的非对称timeliness、按原时间索引语义矩阵、开放slot逐时吸收与K关闭、加权P/R/F1。合成trace负控包括错误语义、空输出、7次重复超过K=5、多slot重叠和早晚惩罚；完美合成trace得1只是定义检查，不是任何Agent能力。无Ctrl-SPOT的持久query/CPU-GPU KV/检索/总结，无视频、LLM或付费judge调用，不接Evolve晋级。 | e-RWSC依据固定政策iid答案流，检验的是多数占优而非答案真实正确；SPOT的slot则用评测gold时间和显式语义匹配计及时性，不提供在线显著性证书。两者都可在输入完美时给出漂亮数值，但一个是采样分布假设下的停止证据，一个是给定trace的离线计分，不能混作模型能力。 |

</div>

## 取舍分析 {#analysis}

### 确定性评分与概率替身，各自回答什么

XLGoBench 由算法生成精确答案，适合判断一次结构化输出是否合规；ProEval 不是替任务重新定义正确性，而是利用已观测分数推断未全测模型的总体表现。后验均值和方差来自模型关系，不是每道题已被真实评分。两者可以组合：先确保 scorer 与 gold 隔离，再决定哪些真实评分最值得付费，保留预测与已测两种状态。

对照来源：[xlgobench](../../../foundation-models/2605.30788-xlgobench/README.md) · [proeval](../../../foundation-models/2604.23099-proeval/README.md)

### 多一层证据，不等于无条件可靠

FUSE 试图利用多个验证器而不直接读取真实标签，但其后验仍受相关性和识别假设限制。DetectorScope 的线性结构可精确分解 logit，却只证明某个池化特征对预测的数值贡献，不证明概念描述或输入文本的因果关系。TCAB 则约束共享反馈时的边际分布。三者把不同环节做得更可检查，不能互相代替，更不能仅凭解释流畅或反馈复用率高宣布能力已验证。

对照来源：[fuse-verifiers](../../../foundation-models/2604.18547-fuse-verifiers/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md) · [tcab](../../../reproductions/2608.12831-tcab/README.md)

### 参考语义也必须匹配被测执行环境

XLGoBench强调scorer与gold隔离，XLA案例进一步显示：即使测试题和标签合法，编译后的计算也可能因寄存器舍入或融合调度偏离原程序。差分参考既不能接受非法输入制造NaN伪警，也不能把合法TPU近似函数误报为故障。拆fusion后正确不代表原fusion正确；A100上算对也不证明TPU lowering正确。因此本轮保留TPU环境缺失，不用CPU/CUDA演示替代硬件结论。

对照来源：[xlgobench](../../../foundation-models/2605.30788-xlgobench/README.md) · [xla-trenches](../../../foundation-models/2611.00624-xla-trenches/README.md)

### Rosetta：跨语言表征统一度与知识迁移：先区分干预对象和可用证据

Rosetta观察/干预预训练语言分布及表示统一度；Thinking to Recall分析推理时自生成事实及其正确性。前者的相似度不是事实真值judge，后者的oracle条件准确率也不证明跨语言表示统一。 `average_cosine` 与 `unification_score` 实现有限、非零表示的集合余弦和逐组比值，拒绝接近零的分母。诊断验证尺度不变性、平均比值及集合自相似不等于对角线常数1。外部特征没有由本地模型生成；诊断不证明跨语言准确率提高。

对照来源：[rosetta-unification](../../../foundation-models/2508.11017-rosetta-unification/README.md) · [thinking-to-recall](../../../foundation-models/2603.09906-thinking-to-recall/README.md)

### Thinking to Recall：事实干净轨迹的离线条件准确率：先区分干预对象和可用证据

本地实现不能；它使用事后外部标注的事实真值模拟条件期望，只是离线oracle分析。要部署还需要不看gold的可靠事实验证器，并计入调用成本和误判；这不是由汇总公式自动得到的。 `conditional_expected_accuracy` 只返回汇总统计、保留/剔除题数，绝不返回被oracle选中的轨迹、行动或训练样本；默认严格要求每题100条。`pass_at_k` 使用无偏组合数估计。负控同时覆盖共同题目mask、逐题宏平均而非微平均、空事实集合和缺失子集。诊断中的真值数组是显式教学输入，不是Agent任务成绩。

对照来源：[thinking-to-recall](../../../foundation-models/2603.09906-thinking-to-recall/README.md) · [rosetta-unification](../../../foundation-models/2508.11017-rosetta-unification/README.md)

### Latent Generalization：区分已见答案与隐含答案的集合评测：先区分干预对象和可用证据

前者用受控知识获取和结构划分考察未显式答案的泛化；后者研究已有参数事实如何因计算和factual priming被读出。两者都不能把gold-conditioned teacher或事后标注暴露给最终actor。 `score_completion` 要求heldout是all的子集，primary属于heldout，且gold集合非空；`exact_set_pass_at_n` 对已经完成的独立尝试计算无偏pass估计。负控显示：train recall=1可以同时heldout recall=0；heldout recall=1也能因额外误答导致exact=0。纯CPU离线评测，无模型训练、语义judge、Evolve或能力晋级。

对照来源：[latent-generalization](../../../foundation-models/2604.01430-latent-generalization/README.md) · [thinking-to-recall](../../../foundation-models/2603.09906-thinking-to-recall/README.md)

### 样本检验的p值，与指定解码分布下的事件质量不是同一概率

LLM Stochasticity从有限样本检查输出是否偏离目标边缘分布，并用时序统计揭示周期或依赖；检验未拒绝不等于目标分布成立，更不证明独立。解码约束Beam固定每步top-k内的归一化概率，不把距离剪枝后剩余分支重归一化，再对可行完整路径求LB并把可能的丢弃质量计入bank。这是事件质量界，不是GoF p值。两者结合时应分别报告采样协议与风险事件，不能把p=1写成100%随机或100%提取概率。本地两组件都只验数值/协议，未加载LLM执行完整审计。

对照来源：[llm-stochasticity](../../../foundation-models/2604.06543-llm-stochasticity/README.md) · [decoding-constrained-beam](../../../foundation-models/2603.24917-decoding-constrained-beam/README.md)

### 训练监督的计量单位与推理分数的基线扣除，是两种校准机制

QE长度归一先改变训练标签尺度，让模型预测每单位长度的错误，再恢复总评分；Interpolated Null Calibration保留已训练模型，利用query+instruction、带instruction的null与bare null三次真实观测扣除混杂分量。前者不能由冻结评分除长度替代，后者λ=0仍在减bare null，不等于无校准。两个方法共同要求明确被控制的因素和validation选择，但所需模型阶段、观测和误差来源不同；数值变换正确不证明未执行的QE重训或三pass提取已完成。

对照来源：[qe-length-normalization](../../../foundation-models/2510.22028-qe-length-normalization/README.md) · [interpolated-null-calibration](../../../foundation-models/2609.17764-interpolated-null-calibration/README.md)

### 同一稀疏表征可以支持检测，也可以支持干预，但不能偷换验收对象

CuE和DetectorScope都把逐token SAE激活池化，却对特征提出不同证据要求：CuE用与文化标签的互信息和国家原型组织方向，DetectorScope检验特征描述并学习稀疏检测权重。前者需要decoder对齐和真实生成评价来支持干预，后者的特征贡献只解释给定检测头的logit。把pooling相同当作方法等价，会把分类相关性误认成文化控制，或把合成方向范数误认成真实忠实度。

对照来源：[cultural-cue](../../../foundation-models/2603.23301-cultural-cue/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

### 可生成性、近目标概率与文本来源是不同统计问题

CBS问的是给定前缀后模型以何概率生成目标邻域，DetectorScope问的是文本特征是否支持特定来源标签。公开常见句既可能容易生成，也可能由人类独立写作；来源检测分数高也不给训练样本的提取概率。CBS的已枚举路径质量可以形成严格下界，宽beam和距离预算只改变找回多少质量，不把未观察路径变成成功。原文负控和概率分布约束都是验收条件，不能只贴一个greedy命中率。

对照来源：[decoding-constrained-beam](../../../foundation-models/2603.24917-decoding-constrained-beam/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

### 解释的粒度与数据依赖要随特征来源一起保留

StoryScope的单位是人类可问的叙事结构，DetectorScope的单位是内部稀疏激活及描述；它们都有模型误差与抽取成本，而不是解释文字越自然越可靠。StoryScope必须把共享prompt的六个故事作为相关组隔离和重采样，且跨模型spread阻止把单模型偏好混成普遍AI核心。DetectorScope的稀疏贡献解释的是分类头本身，不自动证明整篇故事采用某种叙事。两者应保留各自输入和验收，不用通用特征fixture缩短语义过程。

对照来源：[storyscope](../../../foundation-models/2604.03136-storyscope/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

### 相同内容的价格差与相同任务的能力差应分轴

Tokenization Premium的作者脚本先按编号拼27共同条款，独立分词后求和会受边界合并影响。XLGoBench则控制算法实例与复杂度，答案留在独立scorer。若未来研究token预算对跨语言推理的影响，应同时固定内容、翻译与预算，并使用真实模型输出；不能从阿姆哈拉语6.76倍成本推出6.76倍错误，也不能用UNK变少作为胜利。

对照来源：[tokenization-premium](../../../foundation-models/2611.13441-tokenization-premium/README.md) · [xlgobench](../../../foundation-models/2605.30788-xlgobench/README.md)

### 可重复生成报告不等于重复获得独立测量

XLA审计强调保留目标硬件语义；Runway强调保留测量配置及raw AIPerf结果。两者都不能被CPU fixture替代。本地缓存更保守地哈希engine config、数据/模型revision和warm-up，cache-only缺失必须报错；SLA单位错配必须拒绝。重用一份raw结果审查两个SLA是两次决策、不是两份独立样本，不能缩小置信区间。

对照来源：[runway-inference-protocol](../../../foundation-models/2611.12737-runway-inference-protocol/README.md) · [xla-trenches](../../../foundation-models/2611.00624-xla-trenches/README.md)

### 读出差异与修复能力不能靠同一个诊断标签混为一谈

AMS的方向/漂移是检测信号，存在结构保持攻击盲区；Mixed Signals的推理写权重还要求受限反馈和独立未见被试评价。原子写入、失败消耗预算和正确balanced accuracy是必要工程合同，却不创造会编辑的LLM。SGD违规替换和test反馈泄漏都改变了问题。完整campaign高成本不复现，保留L0接口与实际CUDA加载前向证据，不拿作者医学结果背书。

对照来源：[mixed-signals-weights](../../../foundation-models/2611.13758-mixed-signals-weights/README.md) · [activation-model-scanner](../../../foundation-models/2608.05578-activation-model-scanner/README.md)

### Efficient Evals：借廉价评分学能力张量，再用少量人类标签校准：区别机制与能力

§3的ordinal likelihood支持单侧评分和成对能力差及平局；首尾类别用0/1 CDF边界。第二阶段只给human向量／cutoff梯度，模型和prompt因子冻结。条件Wald区间把第一阶段表示当高精度固定量，并用Bonferroni处理多比较；Sigma是渐近协方差，需除m。可选全参数human fine-tune可能改善点预测，却使这些条件区间失效，不能两种好处同时声称。 ProEval用其他模型历史逐题分数建立GP先验并主动决定下一题；本篇用多rater廉价数据学prompt/model表示再做人类对齐。前者的采样后验不等于后者的rater偏差校准，条件置信界也不能无条件覆盖共享表示估计误差。

对照来源：[efficient-evals-tensor](../../../foundation-models/2603.02029-efficient-evals-tensor/README.md) · [proeval](../../../foundation-models/2604.23099-proeval/README.md)

### 答案直方图均匀，是否就满足iid保证？

LLM Stochasticity区分边缘分布拟合与时序依赖；e-RWSC的保证需要固定政策的iid响应，不能由平衡答案直方图或“请随机回答”提示推导。前者的统计诊断可暴露某些依赖，却不能证明后者的全部假设。e-RWSC也不估计答案是否符合现实：即使输入真独立，政策总偏向错误答案时仍可快速发多数证书。 不能。返回的是reward-weighted self-consistency回退，certified必须为false。还要检查当前下注只看旧前缀，新响应的答案和极端reward都不能倒灌到刚才的stake。

对照来源：[e-rwsc](../../../foundation-models/2611.26413-e-rwsc/README.md) · [llm-stochasticity](../../../foundation-models/2604.06543-llm-stochasticity/README.md)

### DISCO与e-RWSC：发现集合错误不等于单题多数

e-RWSC认证单题某答案的政策多数概率，不等于正确性；DISCO控制多行为假设集合的误发现比例，并为自适应假设池施加分箱、冻结与null分布校正约束。相同的e-process工具不使两类错误和证书等价。 DISCO的pre-hoc证书给出无条件epsilon-alpha加delta界；post-hoc证书依赖无null退出条件，须同时保留delta失败概率。有限null路径穷举只验收本地公式与接口，不验证真实LLM的p值有效性，也不替代原文三分箱/boosted发现器及独立复验。

对照来源：[disco](../../../foundation-models/2611.27104-disco/README.md) · [e-rwsc](../../../foundation-models/2611.26413-e-rwsc/README.md)

### T-F1=1是否像e-RWSC证书一样有统计保证？

e-RWSC依据固定政策iid答案流，检验的是多数占优而非答案真实正确；SPOT的slot则用评测gold时间和显式语义匹配计及时性，不提供在线显著性证书。两者都可在输入完美时给出漂亮数值，但一个是采样分布假设下的停止证据，一个是给定trace的离线计分，不能混作模型能力。

对照来源：[spot-bench](../../../foundation-models/2604.24317-spot-bench/README.md) · [e-rwsc](../../../foundation-models/2611.26413-e-rwsc/README.md)

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

### 如果XLGoBench有精确gold，为什么仍不能靠“程序跑完了”保证本次模型评测可信？ {#cross-nov04-labels-versus-execution-semantics}

??? note "展开答案与例子"

    **答案：** 精确gold只定义正确输出，不证明模型的编译执行保持原语义。XLA显示静默错编译能在不崩溃时改变数值；还需合法输入、匹配硬件的差分参考与故障隔离。把正确标签和正确执行分开检查，才能判断错误来自模型还是后端。

    **教学例子：** 教学例：数学gold为非零量化残差，TPU fused kernel却因省略cast全输出0；即使scorer完全准确，也只能判本次输出错，不能自动归因于模型不会该题。

    对照来源：[xlgobench](../../../foundation-models/2605.30788-xlgobench/README.md) · [xla-trenches](../../../foundation-models/2611.00624-xla-trenches/README.md)

### Rosetta与Thinking to Recall都涉及事实，干预位置有什么不同？ {#cross-nov13-colm-rosetta-unification}

??? note "展开答案与例子"

    **答案：** Rosetta观察/干预预训练语言分布及表示统一度；Thinking to Recall分析推理时自生成事实及其正确性。前者的相似度不是事实真值judge，后者的oracle条件准确率也不证明跨语言表示统一。

    **教学例子：** 提高两语言表示相似度，不会自动判断某条中间生日事实是否幻觉；过滤正确事实也不保证低资源语言可读出知识。

    对照来源：[rosetta-unification](../../../foundation-models/2508.11017-rosetta-unification/README.md) · [thinking-to-recall](../../../foundation-models/2603.09906-thinking-to-recall/README.md)

### 这种“优先正确事实轨迹”能像在线Agent策略一样部署吗？ {#cross-nov13-colm-thinking-to-recall}

??? note "展开答案与例子"

    **答案：** 本地实现不能；它使用事后外部标注的事实真值模拟条件期望，只是离线oracle分析。要部署还需要不看gold的可靠事实验证器，并计入调用成本和误判；这不是由汇总公式自动得到的。

    **教学例子：** 用gold确认哪条轨迹正确，再展示该轨迹给actor，会泄漏答案，不能算推理提升。

    对照来源：[thinking-to-recall](../../../foundation-models/2603.09906-thinking-to-recall/README.md) · [rosetta-unification](../../../foundation-models/2508.11017-rosetta-unification/README.md)

### 它与Thinking to Recall的协议分别定位什么问题？ {#cross-nov13-colm-latent-generalization}

??? note "展开答案与例子"

    **答案：** 前者用受控知识获取和结构划分考察未显式答案的泛化；后者研究已有参数事实如何因计算和factual priming被读出。两者都不能把gold-conditioned teacher或事后标注暴露给最终actor。

    **教学例子：** 同一事实被更容易召回，不等于模型学会了未训练关系反转；两者需要不同holdout。

    对照来源：[latent-generalization](../../../foundation-models/2604.01430-latent-generalization/README.md) · [thinking-to-recall](../../../foundation-models/2603.09906-thinking-to-recall/README.md)

### 均匀循环序列的卡方p=1，与解码约束Beam给出的近逐字风险LB=0.1，能否当作同一类概率比较？ {#cross-nov13-colm-llm-stochasticity}

??? note "展开答案与例子"

    **答案：** 不能。p=1表示该边缘频率检验没有拒绝均匀，确定性循环仍可能完全可预测；它不是输出事件概率。LB=0.1则是在明确top-k解码分布和目标距离事件下，已枚举路径的质量下界。两者的对象、假设和分母不同，时序独立性也不由任一数值自动保证。

    **教学例子：** 0,1,2,3循环1024次可有完美均匀直方图，但下一项由前一项确定。另一个模型的top-k概率树里枚举到目标邻域质量0.1，说明该事件至少有这部分质量，不说明模型采样是否使用独立随机源。

    对照来源：[llm-stochasticity](../../../foundation-models/2604.06543-llm-stochasticity/README.md) · [decoding-constrained-beam](../../../foundation-models/2603.24917-decoding-constrained-beam/README.md)

### 同样称“校准”，训练错误密度能否由三pass的null分数扣除替代？ {#cross-cross-density-versus-temperature}

??? note "展开答案与例子"

    **答案：** 不能。密度训练改变R/|h|监督，再乘回长度；null校准在已有模型读出上扣除λ插值基线。只执行后者没有训练QE密度模型，只执行前者也没有得到三次attention读出。两者的可调项只允许validation选择。

    **教学例子：** 教学例：s(q,I)=0.8、s(null,I)=0.3、s(bare)=0.1、λ=0.5时null校准为0.6；这不等于为长度10、错误评分−5的样本训练目标−0.5。

    对照来源：[qe-length-normalization](../../../foundation-models/2510.22028-qe-length-normalization/README.md) · [interpolated-null-calibration](../../../foundation-models/2609.17764-interpolated-null-calibration/README.md)

### CuE 和 DetectorScope 都对SAE特征max-pool，为何不是同一方法？ {#cross-cross-cue-versus-detectorscope}

??? note "展开答案与例子"

    **答案：** 池化只是共享表示操作。CuE以特征–文化MI和国家原型差构造残差干预；DetectorScope用描述验证mask和稀疏检测头作预测与特征归因。前者方向不自动构成检测器，后者头权重也不等于文化干预。

    **教学例子：** 教学例：一个食物特征能区分国家，却不一定区分人类与AI文本；检测头贡献大也不意味着沿该方向生成就文化忠实。

    对照来源：[cultural-cue](../../../foundation-models/2603.23301-cultural-cue/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

### CBS概率下界能否替代DetectorScope的AI文本来源检测分数？ {#cross-cross-logprob-bound-versus-detector}

??? note "展开答案与例子"

    **答案：** 不能。CBS假定有目标后缀并能访问模型条件概率，衡量该前缀下近目标生成质量；DetectorScope从文本的SAE特征预测来源。一个文本容易被模型生成不等于它真的由该模型写成，两类统计也不共享标签含义。

    **教学例子：** 教学例：公开常见句在模型下概率很高，仍可能完全由人类撰写；高来源检测分数也不给某段训练原文的提取概率。

    对照来源：[decoding-constrained-beam](../../../foundation-models/2603.24917-decoding-constrained-beam/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

### StoryScope与DetectorScope的可解释性来自哪里，能互换特征吗？ {#cross-cross-storyscope-versus-detectorscope}

??? note "展开答案与例子"

    **答案：** StoryScope把叙事问题转成外部语义赋值，靠分类器/SHAP定位核心与指纹；DetectorScope依赖模型内部SAE特征和稀疏线性头的可加归因。两者解释单位、获取成本与错误模式不同，不能把未生成的叙事特征拿SAE随机列替代。

    **教学例子：** 教学例：“结尾主题是否明说”要检查全文；SAE某列的激活贡献是另一个观测，不能凭列编号宣称它语义上等于该叙事问题。

    对照来源：[storyscope](../../../foundation-models/2604.03136-storyscope/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

### 某语言token比英语多一倍，是否可以预测其XLGoBench准确率减半？ {#cross-nov18-tokenization-premium}

??? note "展开答案与例子"

    **答案：** 不可以。token溢价是等内容的成本比，XLGoBench准确率还受训练覆盖、翻译、推理能力与预算约束影响；需匹配实例、验证模板和真实模型评测才能研究两者关系。

    **教学例子：** 同一最短路实例可以保持正确路径不变而换语言；输入从100变200token并不改变算法答案，不能把成本比直接换成准确率比。

    对照来源：[tokenization-premium](../../../foundation-models/2611.13441-tokenization-premium/README.md) · [xlgobench](../../../foundation-models/2605.30788-xlgobench/README.md)

### 同一缓存配置反复生成报告，能当多次硬件复验吗？ {#cross-cross-nov18-runway-cache-evidence}

??? note "展开答案与例子"

    **答案：** 不能。Runway cache-hit明确跳过测量，增加的是决策/报告次数而不是独立观测。与XLA要求真实目标TPU确认相似，声明必须绑定实际执行环境和原始证据，不得从fixture或cache-hit推导硬件通过。

    **教学例子：** 教学例：一条AIPerf结果生成10份报告仍只有1次测量；engine开启MTP需新身份而非沿用旧数值。

    对照来源：[runway-inference-protocol](../../../foundation-models/2611.12737-runway-inference-protocol/README.md) · [xla-trenches](../../../foundation-models/2611.00624-xla-trenches/README.md)

### AMS检查通过、权重补丁接口也通过，能标成成功修复吗？ {#cross-cross-nov18-wsp-not-ams}

??? note "展开答案与例子"

    **答案：** 不能。AMS仅给激活结构诊断，接口仅给原子性/预算合同；修复需要真实推理编辑器在权限隔离的practice反馈下操作，并在未见被试上独立评价。

    **教学例子：** 教学例：把线性层取负确实改了forward，但不能当EEG模型准确率提高。

    对照来源：[mixed-signals-weights](../../../foundation-models/2611.13758-mixed-signals-weights/README.md) · [activation-model-scanner](../../../foundation-models/2608.05578-activation-model-scanner/README.md)

### 它与ProEval都省评测费，方法是否相同？ {#cross-cross-nov18-latest-efficient-evals-tensor}

??? note "展开答案与例子"

    **答案：** 不同。ProEval主动选目标问题并更新GP；本篇校准多个rater到人类尺度。

    **教学例子：** 教学例：多一个便宜judge评分不等于主动选了一道人类问题。

    对照来源：[efficient-evals-tensor](../../../foundation-models/2603.02029-efficient-evals-tensor/README.md) · [proeval](../../../foundation-models/2604.23099-proeval/README.md)

### 答案直方图均匀，是否就满足iid保证？ {#cross-nov21-e-rwsc}

??? note "展开答案与例子"

    **答案：** 不满足。LLM Stochasticity说明边缘分布平衡仍可有确定性时序依赖；e-RWSC的固定政策独立抽样假设不能靠均匀图或随机提示替代。

    **教学例子：** 教学例：0、1、2、3无限循环时各值频率相等，但下一值可由上一值确定；这不是四分类iid采样。

    对照来源：[e-rwsc](../../../foundation-models/2611.26413-e-rwsc/README.md) · [llm-stochasticity](../../../foundation-models/2604.06543-llm-stochasticity/README.md)

### DISCO和e-RWSC都累积e-process，为什么不能共用一种成功证书？ {#cross-nov23-disco}

??? note "展开答案与例子"

    **答案：** e-RWSC认证同一题某答案在固定政策iid采样中的多数概率，不保证答案正确。DISCO控制多个行为假设最终集合的误发现比例，并有自适应假设池的分箱、冻结和校正约束。认证对象与错误定义不同。

    **教学例子：** 教学例：某LLM每次都答错同一个答案，e-RWSC仍可能很快发多数证书；这不证明十个新提出的行为规律有九个真的存在，也不能代替DISCO的FDR证书。

    对照来源：[disco](../../../foundation-models/2611.27104-disco/README.md) · [e-rwsc](../../../foundation-models/2611.26413-e-rwsc/README.md)

### T-F1=1是否像e-RWSC证书一样有统计保证？ {#cross-nov23-spot-bench}

??? note "展开答案与例子"

    **答案：** 不是。T-F1只是给定trace/标注/语义匹配的离线分数。e-RWSC也只在固定政策iid假设下证明多数占优，不证明真实正确。

    **教学例子：** 教学例：手工给一个正确时刻和True语义标签就可得1；这没有执行任何视觉模型，也不是Agent能力。

    对照来源：[spot-bench](../../../foundation-models/2604.24317-spot-bench/README.md) · [e-rwsc](../../../foundation-models/2611.26413-e-rwsc/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-23** · 纯CPU、stdlib的非对称timeliness、按原时间索引语义矩阵、开放slot逐时吸收与K关闭、加权P/R/F1。合成trace负控包括错误语义、空输出、7次重复超过K=5、多slot重叠和早晚惩罚；完美合成trace得1只是定义检查，不是任何Agent能力。无Ctrl-SPOT的持久query/CPU-GPU KV/检索/总结，无视频、LLM或付费judge调用，不接Evolve晋级。

涉及：[spot-bench](../../../foundation-models/2604.24317-spot-bench/README.md) · [e-rwsc](../../../foundation-models/2611.26413-e-rwsc/README.md)

**2026-11-23** · e-RWSC认证单题某答案的政策多数概率，不等于正确性；DISCO控制多行为假设集合的误发现比例，并为自适应假设池施加分箱、冻结与null分布校正约束。相同的e-process工具不使两类错误和证书等价。 DISCO的pre-hoc证书给出无条件epsilon-alpha加delta界；post-hoc证书依赖无null退出条件，须同时保留delta失败概率。有限null路径穷举只验收本地公式与接口，不验证真实LLM的p值有效性，也不替代原文三分箱/boosted发现器及独立复验。 完整API发现/复验矩阵成本过高，不复现（审查DONE）；不进入自动重试。

涉及：[disco](../../../foundation-models/2611.27104-disco/README.md) · [e-rwsc](../../../foundation-models/2611.26413-e-rwsc/README.md)

**2026-11-21** · 纯stdlib、CPU-only的RWSC聚合、前缀可预测下注、逐答案log资本与首现权重、首次出现跳过、认证终止和显式未认证预算回退。诊断使用明确的合成答案/奖励流，检查因果顺序、领先变化不重置、错误答案也可能被认证、softmax极值和均匀tie。没有LLM、reward model、答案解析或公开benchmark运行；不把合成流叫模型输出，不接Evolve晋级。 完整实验成本过高不复现；组件不构成能力晋级。

涉及：[e-rwsc](../../../foundation-models/2611.26413-e-rwsc/README.md) · [llm-stochasticity](../../../foundation-models/2604.06543-llm-stochasticity/README.md)

**2026-11-18** · 官方google-research/efficient_evals固定b4421d929d1078631ee890f8e4a776442c816d36、Apache2.0。本地只执行CP、ordinal概率、冻结human NLL和外部Sigma的条件区间算术；不含完整Adam/BFGS拟合、30切分或真实评分重收集。上游CPU notebook估约1小时，完整多judge矩阵高成本不复现，CUDA只验算子。 完整实验高成本不复现，未作能力或Evolve晋级证据。

涉及：[efficient-evals-tensor](../../../foundation-models/2603.02029-efficient-evals-tensor/README.md) · [proeval](../../../foundation-models/2604.23099-proeval/README.md)

**2026-11-18** · 补WSP权重补丁、预算和评价接口，对照AMS检测而非编辑的边界；不调用LLM、不替代TinyEEGNet，完整实验高成本不复现。

涉及：[mixed-signals-weights](../../../foundation-models/2611.13758-mixed-signals-weights/README.md) · [activation-model-scanner](../../../foundation-models/2608.05578-activation-model-scanner/README.md)

**2026-11-18** · 补入推理缓存/SLA/成本证据协议，强调缓存不等于重复采样、单位必须匹配、硬件能力需真测；完整多引擎实例矩阵高成本不复现。

涉及：[runway-inference-protocol](../../../foundation-models/2611.12737-runway-inference-protocol/README.md) · [xla-trenches](../../../foundation-models/2611.00624-xla-trenches/README.md)

**2026-11-18** · 补齐配对token成本与拒答安全读出，比较XLGoBench的能力轴；记录2026-09-22原始Zenodo首发和真实公开测量脚本，不误当11月新首发。

涉及：[tokenization-premium](../../../foundation-models/2611.13441-tokenization-premium/README.md) · [xlgobench](../../../foundation-models/2605.30788-xlgobench/README.md)

**2026-11-13** · 补入叙事语义与prompt组级证据，精确核心阈值不等同指纹判据；与SAE检测解释粒度分开。

涉及：[storyscope](../../../foundation-models/2604.03136-storyscope/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

**2026-11-13** · 补入top-k约束概率界、Hamming/带状Levenshtein及bank，区分可生成性与来源检测，不把穷举教学分布称真实泄漏结论。

涉及：[decoding-constrained-beam](../../../foundation-models/2603.24917-decoding-constrained-beam/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

**2026-11-13** · 补入文化MI累计质量与国家原型干预，区分SAE检测与生成控制，保留层decoder/MI外部边界与国家代理限制。

涉及：[cultural-cue](../../../foundation-models/2603.23301-cultural-cue/README.md) · [detector-scope](../../../foundation-models/2610.30006-detector-scope/README.md)

**2026-11-13** · 改为同卡片的训练密度与三pass null校准比较，区分监督单位、真实观测基线、λ0口径和未运行模型边界。

涉及：[qe-length-normalization](../../../foundation-models/2510.22028-qe-length-normalization/README.md) · [interpolated-null-calibration](../../../foundation-models/2609.17764-interpolated-null-calibration/README.md)

**2026-11-13** · 把随机采样统计诊断与同卡解码概率界作对照：区分GoF p值、时序依赖和目标事件质量，固定各自被审计分布与边界；两个L1组件都不冒充完整LLM能力或安全审计。

涉及：[llm-stochasticity](../../../foundation-models/2604.06543-llm-stochasticity/README.md) · [decoding-constrained-beam](../../../foundation-models/2603.24917-decoding-constrained-beam/README.md)

**2026-11-13** · 补入固定Google COLM历史来源论文及L1组件，比较核心定义与证据边界；完整实验明确不复现，不把本地诊断当模型能力或Evolve改进。

涉及：[latent-generalization](../../../foundation-models/2604.01430-latent-generalization/README.md) · [thinking-to-recall](../../../foundation-models/2603.09906-thinking-to-recall/README.md)

**2026-11-13** · 补入固定Google COLM历史来源论文及L1组件，比较核心定义与证据边界；完整实验明确不复现，不把本地诊断当模型能力或Evolve改进。

涉及：[thinking-to-recall](../../../foundation-models/2603.09906-thinking-to-recall/README.md) · [rosetta-unification](../../../foundation-models/2508.11017-rosetta-unification/README.md)

**2026-11-13** · 补入固定Google COLM历史来源论文及L1组件，比较核心定义与证据边界；完整实验明确不复现，不把本地诊断当模型能力或Evolve改进。

涉及：[rosetta-unification](../../../foundation-models/2508.11017-rosetta-unification/README.md) · [thinking-to-recall](../../../foundation-models/2603.09906-thinking-to-recall/README.md)

**2026-11-04** · 补入Google XLA:TPU编译器正确性研究，区分合法评分、参考硬件语义、静默错编译及工程bug计数；完整内部TPU实验高成本不复现，审查DONE。

涉及：[xla-trenches](../../../foundation-models/2611.00624-xla-trenches/README.md)

**2026-10-27** · 首版：比较精确算法评分、概率评测替身、无标签验证器融合、反馈耦合与可加概念解释，明确观测和推断的边界。

覆盖 13 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 29 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [XLA from the Trenches: Correctness on TPU Workloads at Scale](../../../foundation-models/2611.00624-xla-trenches/README.md)
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
- [Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics](../../../foundation-models/2508.11017-rosetta-unification/README.md)
- [Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs](../../../foundation-models/2603.09906-thinking-to-recall/README.md)
- [Improving Latent Generalization Using Test-time Compute](../../../foundation-models/2604.01430-latent-generalization/README.md)
- [The Illusion of Stochasticity in LLMs](../../../foundation-models/2604.06543-llm-stochasticity/README.md)
- [Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics](../../../foundation-models/2510.22028-qe-length-normalization/README.md)
- [Steering LLMs for Culturally Localized Generation](../../../foundation-models/2603.23301-cultural-cue/README.md)
- [Estimating near-verbatim extraction risk in language models with decoding-constrained beam search](../../../foundation-models/2603.24917-decoding-constrained-beam/README.md)
- [StoryScope: Investigating idiosyncrasies in AI fiction](../../../foundation-models/2604.03136-storyscope/README.md)
- [Inherited Weights: Measuring the Tokenization Premium and the Sovereignty Cost of Language Models for the Global South](../../../foundation-models/2611.13441-tokenization-premium/README.md)
- [Inference Validation for Regulated AI: A Governed Decision Pipeline for LLM Serving](../../../foundation-models/2611.12737-runway-inference-protocol/README.md)
- [Mixed Signals: Weight-Space Programming for EEG and ECG](../../../foundation-models/2611.13758-mixed-signals-weights/README.md)
- [Rich Insights from Cheap Signals: Efficient Evaluations via Tensor Factorization](../../../foundation-models/2603.02029-efficient-evals-tensor/README.md)
- [Sequential Anytime Valid Tests for Efficient Inference-Time Alignment](../../../foundation-models/2611.26413-e-rwsc/README.md)
- [Reliable Behavior Discovery via False Discovery Rate Control](../../../foundation-models/2611.27104-disco/README.md)
- [Don&#x27;t Pause! Every prediction matters in a streaming video](../../../foundation-models/2604.24317-spot-bench/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/evaluation-and-evidence.md) · [返回全部精读卡片](../index.md)
