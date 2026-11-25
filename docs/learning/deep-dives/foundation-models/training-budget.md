---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 训练预算：改数据、改更新方向，还是改比较口径

[基础模型](../index.md) · 更新 2026-11-25 · 39 篇主题资料 / 17 篇重点对照

同一预算内训练得更好，可能来自更合适的数据、逐样本处理、更有效更新或更低状态开销。DoReMi、Mixing Laws、DataOrchestra、Muon 和 ECO 改动不同环节；Muon Paired Budget 则提醒先冻结选参规则，再分别回答等数据和等时间问题。ProLand改变LoRA乘积空间的更新几何，GAVAGAI则给captioning增加显式词区域对齐目标，二者不能仅因都改善训练就混为一类。

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
| [ProLand: A New Infeasible Manifold Optimization Method for LoRA Fine-Tuning](../../../foundation-models/2611.00236-proland/README.md) · [原始来源](https://arxiv.org/abs/2611.00236)<br>章节：核心公式、检查与负控、成本判断与复现边界 | 在BA乘积空间重投影动量并求谱方向，以水平DB协调两因子，同时独立用Landing恢复B正交性。 | 不是给A/B各做Muon；小核节省状态不消除病态伪逆。本地只验精确thin-factor更新，完整多模型微调高成本不复现。 |
| [GAVAGAI: Referential Alignment for Infant-Scale Vision-Language Models via Balanced Optimal Transport](../../../foundation-models/2611.00319-gavagai/README.md) · [原始来源](https://arxiv.org/abs/2611.00319)<br>章节：核心公式、检查与负控、成本判断与复现边界 | 以Nothing吸收非指称词，以视觉列容量上界约束区域竞争，再将固定plan成本和caption CE相加。 | 改变监督而非优化器；8次缩放不保证行边际已收敛，v1未定义Nothing hinge的额外反传。本地不声称完整防塌缩或SAYCam训练。 |
| [Closing the BF16-FP16 Convergence Speed Gap in RL Post-Training with Stochastic Rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md) · [原始来源](https://arxiv.org/abs/2611.13545v1)<br>章节：核心公式、数据协议与代码映射、结果、负控与边界 | 保留FP32主权重，以距离比例在相邻BF16/FP16值间随机选择，使量化后的条件期望等于更新值，缓解小更新被nearest舍入吞没。 | 不同于ECO通过动量补偿并移除主权重，SR本身不节省master存储；无偏不等于每步更准或必然更快。trainer/rollout仍需加载同一量化权重，L1标量核不证明64卡RL曲线。 |
| [Do Depth-Grown Models Overcome the Curse of Depth? An In-Depth Analysis](../../../foundation-models/2512.08819-lidas/README.md) · [原始来源](https://arxiv.org/abs/2512.08819v1)<br>章节：背景与主要改动、核心机制与公式、原文结果与限制、本地复现 | 深层 Transformer 后半段可能对最终预测贡献很小。论文比较从浅到深逐步生长与固定深度预训练，并提出 LIDAS：以层而不是固定块的中点选择复制区域，使偶数块时的初始化区别于 MIDAS。 | LIDAS改变层数、初始化和优化器状态继承；随机舍入改变FP32主权重进入低精度参数时的量化分布。两者的控制变量、预算和误差来源不同，需分别验证，再做同预算组合实验。 |
| [ContinuousBench: Can Differentially Private Synthetic Text Improve Capabilities?](../../../foundation-models/2606.01849-continuousbench/README.md) · [原始来源](https://arxiv.org/abs/2606.01849v1)<br>章节：背景与主要改动、核心机制与公式、原文结果与限制、本地复现 | 若benchmark已经被基座模型做得很好，合成数据是否真正传递新知识就难以区分。ContinuousBench定期生成或整理未见知识语料及相应QA，统一训练/evaluator设置，并与未经该语料训练的同一基座比较；关注高重复公共事实的utility，不要求DP模型记住单条私有记录。 | 不说明。gain评估合成数据utility，ε/δ隐私来自明确DP机制和会计；不应混淆高重复事实可学与单条私有记录可记忆。本地没有DP训练/会计，也没有复现News的LLMjudge。 |
| [ArchSpace: Recording, Reviewing, and Referencing LLM Architecture Research](../../../foundation-models/2611.17332-archspace/README.md) · [原始来源](https://arxiv.org/abs/2611.17332v1)<br>章节：背景与主要改动、核心公式、论文离线与线上效果 | 固定数据和tokenizer，用FLOPs/token、训练token数及LR/BS耦合曲面比较架构；最终衰减checkpoint和11域等权validation是比较协议的一部分。 | Data Mixing Laws改变域比例并从pilot拟合配比；ArchSpace控制架构规模与LR/BS。两类曲面系数不能交换，公开算术复算也不等于重新拟合或执行自动架构搜索。 |
| [The Kernel Reality Check: Benchmarking and Distilling Efficient Attention at Scale](../../../foundation-models/2611.22947-lara-plus-plus/README.md) · [原始来源](https://arxiv.org/abs/2611.22947v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 本文重新核查核化attention的真实效率，并用确定性proposal均值代替随机采样、相似性聚类代替连续切块改善LARA质量。与复杂度口号不同，cluster数量随序列增长时k-center成本为二次；近softmax质量不等于比FlashAttention快。 | LazyFlash保持前向dense而稀疏反向；LARA++近似前向softmax并需要蒸馏适配。两者改变的计算与误差对象不同，不能都归纳成“线性attention更快”。 |
| [Latent Feedback Is a Compute and Data Amplifier](../../../foundation-models/2611.20404-latent-feedback-scaling/README.md) · [原始来源](https://arxiv.org/abs/2611.20404v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | latent feedback把上一token的顶层状态注入下一token输入，花更多每token计算。本文不只在相同token数比较，而让普通Transformer把相同FLOPs用于更多epoch，并同时控制unique数据和模型规模。 | ArchSpace比较架构/超参的匹配预算曲面；本篇专门研究重复数据及feedback的额外计算。两种拟合系数不可交换，单独输出预测loss不等于已训练候选。 |
| [Accelerating Muon with Spectral Residual Correction](../../../foundation-models/2611.27077-aimuon/README.md) · [原始来源](https://arxiv.org/abs/2611.27077v1)<br>章节：背景与主要改动、与已有方法的关系、结果、负控与边界 | 仅矩阵参数的函数式Algorithm1、NS5和20步合成二次矩阵损失autograd诊断。检查相同动量的步长匹配、c=0退回Muon、独立变换不等于预混合、零矩阵、转置和BF16溢出拒绝；没有语言模型预训练、FineWeb读取、超参数搜索或Evolve算子。CPU与真实A100三seed的指标是数值/机制诊断，不是模型能力比较。 | AF-Muon处理tied embedding上稀疏输入与稠密输出的冲突，以support/cap词表方向和一维RMS去掉AdamW；AIMuon改变的是矩阵参数的谱残差方向，不解决共享词表support问题，也不能自动替代AF-Muon全参数分工。相同步长只排除纯尺度效应，不保证新方向一定更优。 |
| [The KL Divergence Is Never Negative, Except in PyTorch](../../../foundation-models/2611.30835-stablekl/README.md) · [原始来源](https://arxiv.org/abs/2611.30835v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 近等分布的真实KL是二阶小量，但教科书公式往往由一阶或常数量相减得到，容易返回零、负数或错误梯度。StableKL把闭式KL重写成非负小量的组合，配合差值、补偿算术和解析梯度；它还区分F.kl_div算子误差与输入log-prob本身已丢失的信息。本地只选择其中Exponential族的Rewrite核。 | 随机舍入处理的是FP32小更新转BF16时落回同一格点，靠随机相邻格点在条件期望上保留变化。StableKL处理的是已存参数上的确定性代数消去，靠公式重写与解析梯度减少误差。前者不修复错误KL公式，后者也不能恢复输入量化前已经消失的更新；提高precision、clamp和随机舍入都不是可互换的补丁。 |
| [Weight Scale Rebalancing: Transferable Training Recipes for Transformers](../../../foundation-models/2611.32866-udvr/README.md) · [原始来源](https://arxiv.org/abs/2611.32866v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | UDVR固定U列/V行的长度，把尺度移入不参与优化的D；attention双侧吸收，FFN仅吸收U侧。它通过不同分支正则与形状规则设置更新尺度，不是训练一个独立幅值参数。 | ProLand协调LoRA乘积空间谱方向，并独立恢复B的Stiefel约束；UDVR不要求正交，只固定长度。长度相等不保证方向独立，QR与单独Muon不是替代实现；两个L1诊断都不支持跨模型训练效果比较。 |

</div>

## 取舍分析 {#analysis}

### 选更多某域，与把该域内容改写，是两个干预

DoReMi 根据 excess loss 调整域频率，Mixing Laws 通过 pilot 曲线预测配比，两者主要改变见到什么比例。DataOrchestra 直接决定每个 chunk 是否保留和如何编辑，会改变监督本身。清洗后语料更多或平均 loss 更低，都不能说明目标任务必然获益；要区分数据量变化、内容变化以及预处理费用。一个可复核实验应明确固定的是原始 token、处理后 token 还是训练步数。

对照来源：[doremi](../../../reproductions/2305.10429-doremi/README.md) · [data-mixing-laws](../../../reproductions/2403.16952-data-mixing-laws/README.md) · [data-orchestra](../../../reproductions/2607.24717-data-orchestra/README.md)

### 预算口径可以让结论反转

Muon 改变每步下降方向，ECO 改变持久状态与量化更新，二者都可能改变每步耗时。Muon Paired Budget 的价值在于把等数据与等时间分开，并冻结开发阶段选参，不为每种报告口径重新挑冠军。训练比较还要包括辅助 AdamW、预处理或 pilot 的实际成本；本地公式诊断与合成曲线只验证这些记账规则，不能作为真实训练效率胜负。

对照来源：[muon](../../../reproductions/2502.16982-muon/README.md) · [eco-optimizer](../../../foundation-models/2601.22101-eco-optimizer/README.md) · [muon-paired-budget](../../../foundation-models/2610.21555-muon-paired-budget/README.md)

### 改变怎样更新，与改变要学什么，必须拆开验证

ProLand保持给定损失，通过乘积空间谱方向和Landing改变LoRA更新；GAVAGAI把词区域指称变量加入训练目标，并用Nothing/容量处理错误监督。前者的下降与约束恢复不能证明新增对齐目标有用，后者的小矩阵传输可行也不证明真实图像grounding提升。若未来组合，应先固定数据、骨干和预算，独立消融目标变化与更新几何；本轮二者都是L1组件，不启动高成本联合训练。

对照来源：[proland](../../../foundation-models/2611.00236-proland/README.md) · [gavagai](../../../foundation-models/2611.00319-gavagai/README.md)

### 低精度更新可见性与高精度状态内存，不要混成一个收益

随机舍入论文保留FP32主权重，处理它的小变化在BF16 rollout中不可见的问题；ECO移除主权重，把重量化误差按有效步长注入已有动量，目标是状态内存—损失权衡。随机舍入可以是一种量化选择，却不自动实现ECO的补偿规则；ECO也不能仅凭无主权重就保证小更新在每次rollout都可见。要分开报告存储、量化偏差、同步与收敛。

对照来源：[stochastic-rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md) · [eco-optimizer](../../../foundation-models/2601.22101-eco-optimizer/README.md)

### LIDAS：按中间层生长 Transformer 并继承优化器状态：先区分干预对象和可用证据

LIDAS改变层数、初始化和优化器状态继承；随机舍入改变FP32主权重进入低精度参数时的量化分布。两者的控制变量、预算和误差来源不同，需分别验证，再做同预算组合实验。 `grow_layers` 对实际 `nn.ModuleList` 和 AdamW 状态执行变换，保留列表外的embedding/head；不自动改任意模型的配置或位置索引。拒绝跨层绑权重，避免悄悄破坏权重共享语义。`prop1_schedule` 保留总预算；整数化使用明确的最大余数约定。负控覆盖AMSGrad所有状态不alias、scheduler不重启、复制层确有梯度和参数变化。

对照来源：[lidas](../../../foundation-models/2512.08819-lidas/README.md) · [stochastic-rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md)

### ContinuousBench：衡量合成文本带来的新能力而非旧题记忆：先区分干预对象和可用证据

不说明。gain评估合成数据utility，ε/δ隐私来自明确DP机制和会计；不应混淆高重复事实可学与单条私有记录可记忆。本地没有DP训练/会计，也没有复现News的LLMjudge。 `score_geminon` 独立实现固定作者代码的清洗/匹配语义；`capability_gain`要求两臂题目ID、问题、gold与release revision完全一致，基线必须显式给出；`select_validation_checkpoint`拒绝test行。不得把contains与exact混为一谈：Flying and Normal可覆盖Normal and Flying的两类型，但不是相同字符串。无模型调用、HF大下载、DP-SGD或News自动judge。

对照来源：[continuousbench](../../../foundation-models/2606.01849-continuousbench/README.md) · [data-orchestra](../../../reproductions/2607.24717-data-orchestra/README.md)

### 拟合损失之前先固定干预变量和预算单位

相同loss输出不意味着相同研究任务。Data Mixing Laws的输入有mixture simplex，ArchSpace把数据固定并用C=MD计训练FLOPs。M不是参数量，LR条件最优随batch平方根变化；未重跑新架构的pilot就不能用旧基线系数宣称收益。

对照来源：[archspace](../../../foundation-models/2611.17332-archspace/README.md) · [data-mixing-laws](../../../reproductions/2403.16952-data-mixing-laws/README.md)

### LARA++：确定性proposal与相似性分组的核注意力

LazyFlash保持前向dense而稀疏反向；LARA++近似前向softmax并需要蒸馏适配。两者改变的计算与误差对象不同，不能都归纳成“线性attention更快”。 本地固定作者commit的mis-opt路径。论文§7描述query-only和随机首中心，而公开源码用归一化Q+K联合特征、确定性首中心，CLS单独保留。这里明确执行源码变体，不把差异消除：proposal生成不反传，当前Q/K特征与V聚合仍可微。

对照来源：[lara-plus-plus](../../../foundation-models/2611.22947-lara-plus-plus/README.md) · [lazyflash](../../../foundation-models/2610.31911-lazyflash/README.md)

### Latent Feedback：在重复数据下比较相同计算预算

ArchSpace比较架构/超参的匹配预算曲面；本篇专门研究重复数据及feedback的额外计算。两种拟合系数不可交换，单独输出预测loss不等于已训练候选。 R<1时有效数据改为RU；R>=1时重复收益逐渐饱和。capacity multiplier与每token额外计算成本不同，loss预测依赖重新拟合和外推验证，不是重复token越多越省的无条件结论。

对照来源：[latent-feedback-scaling](../../../foundation-models/2611.20404-latent-feedback-scaling/README.md) · [archspace](../../../foundation-models/2611.17332-archspace/README.md)

### AIMuon能替代AF-Muon的tied embedding处理吗？

AF-Muon处理tied embedding上稀疏输入与稠密输出的冲突，以support/cap词表方向和一维RMS去掉AdamW；AIMuon改变的是矩阵参数的谱残差方向，不解决共享词表support问题，也不能自动替代AF-Muon全参数分工。相同步长只排除纯尺度效应，不保证新方向一定更优。

对照来源：[aimuon](../../../foundation-models/2611.27077-aimuon/README.md) · [af-muon](../../../foundation-models/2610.01395-af-muon/README.md)

### The KL Divergence Is Never Negative, Except in PyTorch

随机舍入处理的是FP32小更新转BF16时落回同一格点，靠随机相邻格点在条件期望上保留变化。StableKL处理的是已存参数上的确定性代数消去，靠公式重写与解析梯度减少误差。前者不修复错误KL公式，后者也不能恢复输入量化前已经消失的更新；提高precision、clamp和随机舍入都不是可互换的补丁。 Exponential的x先由原始rate之差计算，避免先取ratio再减1。在−0.75≤x≤3上，FP32用K=17的Horner级数计算φ；两侧使用条件良好的log1p或log(rate_q/rate_p)分支。自定义autograd直接返回两rate解析导数。末端非负截断只是稳定公式的边界约定，不是对原始消去公式clamp就算修复。原文strict模式、区间算术与其他分布的误差自由变换不在本地范围。

对照来源：[stablekl](../../../foundation-models/2611.30835-stablekl/README.md) · [stochastic-rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md)

### Weight Scale Rebalancing: Transferable Training Recipes for Transformers

ProLand协调LoRA乘积空间谱方向，并独立恢复B的Stiefel约束；UDVR不要求正交，只固定长度。长度相等不保证方向独立，QR与单独Muon不是替代实现；两个L1诊断都不支持跨模型训练效果比较。 原文FFN的D更新不含V侧尺度，故GELU路径不函数守恒；attention才有精确UDV守恒。D必须是buffer，真实任务梯度与分支正则先更新U/V，之后再重平衡，不能把投影放在梯度前充数。

对照来源：[udvr](../../../foundation-models/2611.32866-udvr/README.md) · [proland](../../../foundation-models/2611.00236-proland/README.md)

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

### ProLand与GAVAGAI都能对训练产生影响，为什么不能只看一次loss下降就归为同一种改进？ {#cross-nov04-objective-versus-geometry}

??? note "展开答案与例子"

    **答案：** ProLand在给定目标上改变参数更新和约束恢复；GAVAGAI直接改变目标，引入词区域分配和Nothing。两种loss甚至可能不可直接比较。需要固定任务和数据，分别检查更新等价性、传输约束、独立验证效果与总成本，不能让小矩阵下降代替能力证据。

    **教学例子：** 教学例：把原CE加上一个可能为负的对齐成本，数值变低不等于caption质量改善；同样，ProLand让MSE下降也不代表学到了图像中的词所指。

    对照来源：[proland](../../../foundation-models/2611.00236-proland/README.md) · [gavagai](../../../foundation-models/2611.00319-gavagai/README.md)

### 把nearest改成随机舍入，是否已经实现了ECO的无主权重训练？ {#cross-rounding-is-not-master-removal}

??? note "展开答案与例子"

    **答案：** 没有。随机舍入改变FP32值如何投到低精度格点，本地仍以FP32主值为输入；ECO还移除常驻master并补偿动量，Adam需要逐元素有效步长。二者的状态与更新合同不同。

    **教学例子：** 教学例：1+1/1024以1/8概率上舍到BF16邻居，只验证量化期望；它没有说明FP32 master是否被删除，也没有进行任何动量误差补偿。

    对照来源：[stochastic-rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md) · [eco-optimizer](../../../foundation-models/2601.22101-eco-optimizer/README.md)

### LIDAS与随机舍入都影响训练，为什么收益不能混算？ {#cross-nov13-colm-lidas}

??? note "展开答案与例子"

    **答案：** LIDAS改变层数、初始化和优化器状态继承；随机舍入改变FP32主权重进入低精度参数时的量化分布。两者的控制变量、预算和误差来源不同，需分别验证，再做同预算组合实验。

    **教学例子：** 层生长保持Adam moments；SR保持量化条件期望。两项都通过L1，不等于组合模型会更快达到同精度。

    对照来源：[lidas](../../../foundation-models/2512.08819-lidas/README.md) · [stochastic-rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md)

### 有更高capability gain就说明DP更安全吗？ {#cross-nov13-colm-continuousbench}

??? note "展开答案与例子"

    **答案：** 不说明。gain评估合成数据utility，ε/δ隐私来自明确DP机制和会计；不应混淆高重复事实可学与单条私有记录可记忆。本地没有DP训练/会计，也没有复现News的LLMjudge。

    **教学例子：** 一个非DP数据生成器可有很高QA准确率，仍不满足任何声称的隐私预算。

    对照来源：[continuousbench](../../../foundation-models/2606.01849-continuousbench/README.md) · [data-orchestra](../../../reproductions/2607.24717-data-orchestra/README.md)

### Data Mixing Laws与ArchSpace都能预测loss，为什么不能直接串起来就说完成了架构进化？ {#cross-nov15-archspace}

??? note "展开答案与例子"

    **答案：** 它们分别拟合数据配比与架构/超参预算关系；串接需要真实候选训练、验证各自外推范围并统一预算。仅注册或调用公开系数没有执行和评测新候选。

    **教学例子：** 改变语料配比同时改变架构后，loss下降仍需要对照区分数据与结构贡献。

    对照来源：[archspace](../../../foundation-models/2611.17332-archspace/README.md) · [data-mixing-laws](../../../reproductions/2403.16952-data-mixing-laws/README.md)

### 论文和当前作者实现的聚类是否完全相同？ {#cross-nov18-lara-plus-plus}

??? note "展开答案与例子"

    **答案：** 不完全。论文写query相似性与随机初始点，固定源码用归一化Q+K、确定性初始点并保留CLS。本地记录源码变体，不声称两者无差别。

    **教学例子：** 两个query相同但key不同的token，在joint特征里可能分到不同簇。

    对照来源：[lara-plus-plus](../../../foundation-models/2611.22947-lara-plus-plus/README.md) · [lazyflash](../../../foundation-models/2610.31911-lazyflash/README.md)

### 能直接把ArchSpace的loss系数填进本篇吗？ {#cross-nov18-latent-feedback-scaling}

??? note "展开答案与例子"

    **答案：** 不能。两者控制变量和函数形式不同，本篇包含repeat saturation与feedback capacity factor；需要自己的拟合。

    **教学例子：** 即使都预测validation loss，参数N与FLOPs/token M也不是相同量。

    对照来源：[latent-feedback-scaling](../../../foundation-models/2611.20404-latent-feedback-scaling/README.md) · [archspace](../../../foundation-models/2611.17332-archspace/README.md)

### AIMuon能替代AF-Muon的tied embedding处理吗？ {#cross-nov23-aimuon}

??? note "展开答案与例子"

    **答案：** 不能直接推断。AF-Muon管词表support/cap及向量更新；AIMuon只定义矩阵谱残差。组合需要明确参数分工和真实验证。

    **教学例子：** 教学例：一个训练step中只出现两个词，词表输入梯度稀疏；矩阵残差修正不会自动给未出现词定义support约束。

    对照来源：[aimuon](../../../foundation-models/2611.27077-aimuon/README.md) · [af-muon](../../../foundation-models/2610.01395-af-muon/README.md)

### StableKL与随机舍入能互相替代吗？ {#cross-nov24-stablekl}

??? note "展开答案与例子"

    **答案：** 不能。随机舍入解决量化格点吞掉更新，并引入受控随机性；StableKL解决已存输入上的确定性消去。丢失在输入表示中的信息也不属于KL算子能恢复的范围。

    **教学例子：** 教学例：BF16把两个rate先都存成1，StableKL只能正确给0；若FP32仍保留两者差值，它才可通过重写恢复小的正KL。

    对照来源：[stablekl](../../../foundation-models/2611.30835-stablekl/README.md) · [stochastic-rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md)

### UDVR和ProLand都约束因子，约束相同吗？ {#cross-nov25-udvr}

??? note "展开答案与例子"

    **答案：** 不相同。UDVR逐列/行固定长度而允许方向相关；ProLand围绕B的正交性与乘积空间谱更新。二者的几何和优化顺序不能互换。

    **教学例子：** 教学例：两列完全一样但范数都为目标值可满足UDVR，却不满足B转置B=I。

    对照来源：[udvr](../../../foundation-models/2611.32866-udvr/README.md) · [proland](../../../foundation-models/2611.00236-proland/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-25** · ProLand协调LoRA乘积空间谱方向，并独立恢复B的Stiefel约束；UDVR不要求正交，只固定长度。长度相等不保证方向独立，QR与单独Muon不是替代实现；两个L1诊断都不支持跨模型训练效果比较。 完整实验按成本终态收录，不以L1诊断或资料收录晋级Evolve。

涉及：[udvr](../../../foundation-models/2611.32866-udvr/README.md) · [proland](../../../foundation-models/2611.00236-proland/README.md)

**2026-11-24** · 随机舍入处理的是FP32小更新转BF16时落回同一格点，靠随机相邻格点在条件期望上保留变化。StableKL处理的是已存参数上的确定性代数消去，靠公式重写与解析梯度减少误差。前者不修复错误KL公式，后者也不能恢复输入量化前已经消失的更新；提高precision、clamp和随机舍入都不是可互换的补丁。 完整实验不复现与本地L1组件分开，不晋级Evolve。

涉及：[stablekl](../../../foundation-models/2611.30835-stablekl/README.md) · [stochastic-rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md)

**2026-11-23** · 仅矩阵参数的函数式Algorithm1、NS5和20步合成二次矩阵损失autograd诊断。检查相同动量的步长匹配、c=0退回Muon、独立变换不等于预混合、零矩阵、转置和BF16溢出拒绝；没有语言模型预训练、FineWeb读取、超参数搜索或Evolve算子。CPU与真实A100三seed的指标是数值/机制诊断，不是模型能力比较。

涉及：[aimuon](../../../foundation-models/2611.27077-aimuon/README.md) · [af-muon](../../../foundation-models/2610.01395-af-muon/README.md)

**2026-11-18** · ArchSpace比较架构/超参的匹配预算曲面；本篇专门研究重复数据及feedback的额外计算。两种拟合系数不可交换，单独输出预测loss不等于已训练候选。 本地边界与完整高成本不复现分别记录。

涉及：[latent-feedback-scaling](../../../foundation-models/2611.20404-latent-feedback-scaling/README.md) · [archspace](../../../foundation-models/2611.17332-archspace/README.md)

**2026-11-18** · LazyFlash保持前向dense而稀疏反向；LARA++近似前向softmax并需要蒸馏适配。两者改变的计算与误差对象不同，不能都归纳成“线性attention更快”。 本地边界与完整高成本不复现分别记录。

涉及：[lara-plus-plus](../../../foundation-models/2611.22947-lara-plus-plus/README.md) · [lazyflash](../../../foundation-models/2610.31911-lazyflash/README.md)

**2026-11-15** · 补入固定版本方法、低成本组件或明确资料收录，分开原文结果、本地诊断及高成本不复现范围。

涉及：[archspace](../../../foundation-models/2611.17332-archspace/README.md) · [data-mixing-laws](../../../reproductions/2403.16952-data-mixing-laws/README.md)

**2026-11-13** · 补入固定Google COLM历史来源论文及L1组件，比较核心定义与证据边界；完整实验明确不复现，不把本地诊断当模型能力或Evolve改进。

涉及：[continuousbench](../../../foundation-models/2606.01849-continuousbench/README.md) · [data-orchestra](../../../reproductions/2607.24717-data-orchestra/README.md)

**2026-11-13** · 补入固定Google COLM历史来源论文及L1组件，比较核心定义与证据边界；完整实验明确不复现，不把本地诊断当模型能力或Evolve改进。

涉及：[lidas](../../../foundation-models/2512.08819-lidas/README.md) · [stochastic-rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md)

**2026-11-11** · 加入NVIDIA随机舍入，与Google ECO区分小更新的量化可见性和移除master的状态节省；保留有限范围、负数/subnormal、条件无偏与同步约束。仅L1数值核，64H100/64B200完整训练不复现。

涉及：[stochastic-rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md) · [eco-optimizer](../../../foundation-models/2601.22101-eco-optimizer/README.md)

**2026-11-04** · 加入ProLand与GAVAGAI，区分乘积空间更新几何和新增对齐监督；新增独立参考、有限迭代与反传边界，二者完整训练高成本不复现。

涉及：[proland](../../../foundation-models/2611.00236-proland/README.md) · [gavagai](../../../foundation-models/2611.00319-gavagai/README.md)

**2026-10-27** · 首版：比较域配比学习、配比曲线外推、逐样本处理、矩阵优化与低精度状态，并用配对预算协议解释结论口径。

覆盖 28 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 39 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [GAVAGAI: Referential Alignment for Infant-Scale Vision-Language Models via Balanced Optimal Transport](../../../foundation-models/2611.00319-gavagai/README.md)
- [ProLand: A New Infeasible Manifold Optimization Method for LoRA Fine-Tuning](../../../foundation-models/2611.00236-proland/README.md)
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
- [Closing the BF16-FP16 Convergence Speed Gap in RL Post-Training with Stochastic Rounding](../../../foundation-models/2611.13545-stochastic-rounding/README.md)
- [Do Depth-Grown Models Overcome the Curse of Depth? An In-Depth Analysis](../../../foundation-models/2512.08819-lidas/README.md)
- [ContinuousBench: Can Differentially Private Synthetic Text Improve Capabilities?](../../../foundation-models/2606.01849-continuousbench/README.md)
- [ArchSpace: Recording, Reviewing, and Referencing LLM Architecture Research](../../../foundation-models/2611.17332-archspace/README.md)
- [The Kernel Reality Check: Benchmarking and Distilling Efficient Attention at Scale](../../../foundation-models/2611.22947-lara-plus-plus/README.md)
- [Latent Feedback Is a Compute and Data Amplifier](../../../foundation-models/2611.20404-latent-feedback-scaling/README.md)
- [Accelerating Muon with Spectral Residual Correction](../../../foundation-models/2611.27077-aimuon/README.md)
- [The KL Divergence Is Never Negative, Except in PyTorch](../../../foundation-models/2611.30835-stablekl/README.md)
- [Weight Scale Rebalancing: Transferable Training Recipes for Transformers](../../../foundation-models/2611.32866-udvr/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/training-budget.md) · [返回全部精读卡片](../index.md)
