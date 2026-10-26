---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 长上下文：注意力、递归状态与记忆

[基础模型](index.md) / 31 个问题 · 31 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">31 个问题 · 31 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:openattention" data-paper-title="OpenAttention: One Percent Is Enough with Tail Proxies" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="OpenAttention: One Percent Is Enough with Tail Proxies 基础模型 Sogang University 2026-10-22 低读取率稀疏注意力不只需要选出少量重要 KV，还需要处理未读取的尾部。OpenAttention 在 query 二阶矩定义的几何空间内聚类，以 ErrorGate 估计簇内代理误差并分配精确读取预算；每个簇的未读部分成为一个带计数的均值代理。它不是单纯的 top-k 截断或均值池化。 完整实验成本过高，不复现（审查 DONE）。该小规模诊断仅核对公式与可执行性，不是语言模型能力比较。fit_cache、qgs_scores、errorgate、waterfill、residual_proxy_attention、attend 真实执行完整单头算子链。为便于独立核对，残余均值直接从未读行重算，而不是移植 Triton 的缓存和减法实现。全零误差按等权 water filling 处理；排序并列按原位置，空簇保持无代理，均为显式确定性边界。  高效注意力 KV缓存与稀疏推理 基础模型 长上下文：注意力、递归状态与记忆 OpenAttention只精读少量KV，为什么还要给未读尾部留一个带计数的代理？ 直接top-k会把未读token的softmax质量全部丢掉。OpenAttention按查询相关几何聚类，给高估计误差的簇更多精读预算；剩余token以均值key/value代理参与归一化，并在logit中加入对数数量。这样保留尾部的总质量近似，但簇内分布与误差估计仍有假设，不能视为精确attention。 教学例子：100个相似尾部token各自权重不大，合起来却很可观；一个无计数的均值代理只算一次，会低估它们，加入数量修正才能近似这100项的总贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-openattention-57f03e45" class="ar-learning-paper-anchor"></span>
<h2 id="qa-deccca2f42b3b93c">OpenAttention只精读少量KV，为什么还要给未读尾部留一个带计数的代理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopenattention">OpenAttention: One Percent Is Enough with Tail Proxies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sogang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接top-k会把未读token的softmax质量全部丢掉。OpenAttention按查询相关几何聚类，给高估计误差的簇更多精读预算；剩余token以均值key/value代理参与归一化，并在logit中加入对数数量。这样保留尾部的总质量近似，但簇内分布与误差估计仍有假设，不能视为精确attention。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>100个相似尾部token各自权重不大，合起来却很可观；一个无计数的均值代理只算一次，会低估它们，加入数量修正才能近似这100项的总贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30951v1">原论文</a> · <a href="../../../../foundation-models/2610.30951-openattention/">实现解读</a> · <a href="#qa-deccca2f42b3b93c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttr-compressor" data-paper-title="Rethinking Sequence Compression with Test-time Regression" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Rethinking Sequence Compression with Test-time Regression 基础模型 The Chinese University of Hong Kong 2026-10-22 固定池化或投影分别聚合 token，难以按当前输入的相关结构调整压缩。TTR 把一组 token 视作回归观测：由 token 方向构造 key，由保留模长的原始 token 生成可学习标量 target；每次前向精确求解 ridge 系数，直接把系数作为压缩表示。外层任务 loss 通过闭式求解训练 target 投影与正则。“test-time”指输入相关的回归系数在前向内重新拟合，不表示推理时更新模型参数。基础版本只有个可训练参数，不是另建一个 agent 或训练时读取正确压缩答案。 完整模型训练和多基准评估成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列。三个 seed 不会把机制诊断升级成能力复现。ttr_compress 独立实现正对角 generalized ridge 与 dual Cholesky；TTRCompressor 将注册成可训练参数。diagnostic(seed, device=&#x27;cpu&#x27;) 生成4组、每组7个12维 token，执行外层反传和一次真实 SGD 更新，返回严格的 seed/metrics/checks。既不下载数据或权重，也不调用 pretrained 模型。  序列压缩 可微测试时回归 基础模型 长上下文：注意力、递归状态与记忆 TTR为什么只归一化key，却让回归target保留原始token的模长？ key的单位化让回归按方向组织观测，target仍保留输入强度；二者的这种不对称使系数反映当前token集合。若target也由归一化key的同一个静态投影产生，固定向量就能平凡拟合，失去输入相关压缩意义。每次前向求回归系数，不等于推理时更新模型的持久参数。 教学例子：两个token方向相同、模长分别1和3；key相同但target不同，回归必须权衡两次观测。若两边都归一化，它们会变成同一个监督点，强度差异随之消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-ttr-compressor-1230f560" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0f87d6fafc5bcc63">TTR为什么只归一化key，却让回归target保留原始token的模长？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attr-compressor">Rethinking Sequence Compression with Test-time Regression</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>key的单位化让回归按方向组织观测，target仍保留输入强度；二者的这种不对称使系数反映当前token集合。若target也由归一化key的同一个静态投影产生，固定向量就能平凡拟合，失去输入相关压缩意义。每次前向求回归系数，不等于推理时更新模型的持久参数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个token方向相同、模长分别1和3；key相同但target不同，回归必须权衡两次观测。若两边都归一化，它们会变成同一个监督点，强度差异随之消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31574v1">原论文</a> · <a href="../../../../foundation-models/2610.31574-ttr-compressor/">实现解读</a> · <a href="#qa-0f87d6fafc5bcc63">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stratified-sparse-attention" data-paper-title="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity 基础模型 Rice University 2026-10-20 只保留 top-k 会丢掉尾部质量；均匀抽样又浪费预算。SSA先确定保留高概率项，再按残差代理分布抽样。关键不是“top-k加采样”的外形，而是有放回抽样后去重，按每个token至少出现一次的包含概率修正。论文的自适应 Algorithm 1 与实际优化内核的固定 heavy fraction 版本不同；本地实现前者，不冒充后者的速度。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不自动重试。L1诊断不是正式能力比较，不参与Evolve晋级。stratified_sparse_attention 接受单query、keys、values和外部代理分数，真实执行water-filling、离散采样和精确选中项打分。梯度只通过实际选中Q/K/V；代理分配是detached离散步骤。没有声称实现PQCache代理、层级采样或paged KV runtime。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 SSA有放回采样后先去重，为什么还要按“至少抽中一次”的概率修正？ 一个token可能在多次抽样中重复出现；去重后，它是否进入最终集合的概率不再等于单次抽样概率。SSA用包含概率一减一减p的m次方作修正，并让确定保留的重项概率为1。最终是自归一化比值估计，不能把这种修正继续夸成输出严格无偏。 教学例子：某token每次被抽中的概率为0.2，抽两次时至少出现一次的概率是0.36；去重只算一行时，应按0.36而不是0.2修正它的贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-stratified-sparse-attention-869759f6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-80e8ff6ac2401e91">SSA有放回采样后先去重，为什么还要按“至少抽中一次”的概率修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astratified-sparse-attention">Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rice University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个token可能在多次抽样中重复出现；去重后，它是否进入最终集合的概率不再等于单次抽样概率。SSA用包含概率一减一减p的m次方作修正，并让确定保留的重项概率为1。最终是自归一化比值估计，不能把这种修正继续夸成输出严格无偏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某token每次被抽中的概率为0.2，抽两次时至少出现一次的概率是0.36；去重只算一行时，应按0.36而不是0.2修正它的贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28441v1">原论文</a> · <a href="../../../../foundation-models/2610.28441-stratified-sparse-attention/">实现解读</a> · <a href="#qa-80e8ff6ac2401e91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:kronlstm" data-paper-title="Kronecker Delta Rule for Long Context Linear Attention" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Kronecker Delta Rule for Long Context Linear Attention 基础模型 Johannes Kepler University Linz 2026-10-19 标准 DeltaNet 用向量误差更新矩阵记忆，会干扰与当前 key 重叠的其他关联。Kronecker Delta Rule 修正的是一个 key-value 对的标量关联；记忆修订沿的单一矩阵方向进行。KronLSTM 再加入 key 轴逐通道遗忘和分离 erase/write 门。 完整实验显著超出单张 A100/A30 或本地 Mac 的日常预算，成本过高，不复现（审查 DONE）。kronecker_update 保存标量关联擦除与 key 轴忘记；TinyKronLSTM 包含真实投影、短卷积、归一化、四类输入相关门、循环记忆和输出投影。它不是把普通 DeltaNet 换个名字，也不是仅记录配置。当前是 PyTorch 循环版，未实现论文 Appendix A8 的融合 chunkwise 前后向内核，不宣称相同吞吐量。  注意力与长上下文 线性注意力与递归记忆 基础模型 长上下文：注意力、递归状态与记忆 KronLSTM擦写的是整个value向量，还是一个key–value的标量关联？ Kronecker Delta Rule用v转置Sk衡量一个key与value方向的标量关联，沿vk转置这一矩阵方向擦写；它不同于直接用整段向量误差修改记忆。对另一个关联的干扰同时取决于key和value的重叠，任一方向正交都能阻断这次干扰。KronLSTM还分开遗忘、擦除与写入门，不能把写入系数误乘擦除门。 教学例子：两条关联使用相近的key，但value方向正交。沿第一条的vk转置更新时，第二条的标量关联不会因此被同样擦掉；这仍不保证所有后续写入都无干扰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-kronlstm-ae88fcaa" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a233b49ed9960b21">KronLSTM擦写的是整个value向量，还是一个key–value的标量关联？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Akronlstm">Kronecker Delta Rule for Long Context Linear Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johannes Kepler University Linz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Kronecker Delta Rule用v转置Sk衡量一个key与value方向的标量关联，沿vk转置这一矩阵方向擦写；它不同于直接用整段向量误差修改记忆。对另一个关联的干扰同时取决于key和value的重叠，任一方向正交都能阻断这次干扰。KronLSTM还分开遗忘、擦除与写入门，不能把写入系数误乘擦除门。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条关联使用相近的key，但value方向正交。沿第一条的vk转置更新时，第二条的标量关联不会因此被同样擦掉；这仍不保证所有后续写入都无干扰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26834">原论文</a> · <a href="../../../../foundation-models/2610.26834-kronlstm/">实现解读</a> · <a href="#qa-a233b49ed9960b21">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:memory-mosaics-plus" data-paper-title="Open-world AI: a Tale of Three Requirements" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Open-world AI: a Tale of Three Requirements 基础模型 FAIR, Meta 2026-10-14 固定任务的 IID 泛化不等于在开放世界中学习新任务。论文提出推理时学习、丰富表示和预测性解耦三个要求。§3.2 的 Mosaics+ 用短期模块先处理近期依赖，再以 Gaussian-kernel 长期记忆检索预测关联；two-stage 版本分别估计当前任务与相关任务，避免一锅混池让不相关历史越多越有害。 单张 A100/A30 不适合完整多臂训练，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。不下载公开语料或 checkpoint。固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1，seeds42/43/44；每个 seed 使用2条8-token、16维随机输入和明确文档边界。短窗2、skip1 是缩小的算子配置，不等于原文256/64设定。随机目标只用于确认训练路径，不是任务测试答案。  网络架构 关联记忆与推理时学习 基础模型 长上下文：注意力、递归状态与记忆 Mosaics+为何分别归一化当前任务和相关任务记忆，不能直接混成一个softmax？ 把两类记忆混池后，它们会在同一个分母中竞争；数量很多但无关的旧任务可能稀释当前任务证据。two-stage路径分别求两类记忆的归一化预测，再合并结果，使证据来源保持可分。短期模块负责近期依赖，长期记忆保存预测关联；读取也要跳过不合法的未来位置。 教学例子：当前文档只有3条有用关联，历史库却有1000条其他任务记录。混池可能让后者挤占权重；分开归一化后，当前文档的预测不会仅因旧记录数量增长而被同样稀释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-memory-mosaics-plus-a2cfe6c3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b087fe5457f11f79">Mosaics+为何分别归一化当前任务和相关任务记忆，不能直接混成一个softmax？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amemory-mosaics-plus">Open-world AI: a Tale of Three Requirements</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR, Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把两类记忆混池后，它们会在同一个分母中竞争；数量很多但无关的旧任务可能稀释当前任务证据。two-stage路径分别求两类记忆的归一化预测，再合并结果，使证据来源保持可分。短期模块负责近期依赖，长期记忆保存预测关联；读取也要跳过不合法的未来位置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前文档只有3条有用关联，历史库却有1000条其他任务记录。混池可能让后者挤占权重；分开归一化后，当前文档的预测不会仅因旧记录数量增长而被同样稀释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20782">原论文</a> · <a href="../../../../foundation-models/2610.20782-memory-mosaics-plus/">实现解读</a> · <a href="#qa-b087fe5457f11f79">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oal" data-paper-title="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels 基础模型 The Chinese University of Hong Kong, Shenzhen 2026-10-09 预训练 attention 的 QK 各维度贡献不均匀，少量高贡献坐标包含较多 softmax 近似误差。OAL 先在 post-RoPE QK 上计算因果贡献，以 prompt bootstrap 识别高贡献尾部的稳定边界；随后学习共享组和组对系数的二次核。正半定参数化保证分母严格正，并用真实 attention 输出 MSE 校准，而不是仅拟合 attention 权重。校准之后保留前后 softmax 层，对中间层进行转换，并在所有层的 q/k/v/o 上做 LoRA，联合训练核系数。 小规模诊断不作稳定提升声明，相对原文效果百分比不适用。cpu-contracts.json记录已重跑的 5 个测试：因果贡献公式、bootstrap/无人工组数上限、正核与 dense/HD 等价、输出校准梯度、实际 Qwen 模块转换与 LoRA 梯度。每项先固定 seed 42，递推等价/校准专用用例内部使用 seed 11/2；不是独立多 seed 能力实验。没有 CPU 单测到 A100 完成的自动晋级。core_mechanism / L1：保留 QK 分组、正核、真实输出校准和真实 Base checkpoint 的 LoRA 联合更新。小 batch 训练使用精确 dense kernel；  推理与系统效率 注意力线性化 基础模型 长上下文：注意力、递归状态与记忆 OAL为什么按QK维度贡献分组，还要用attention输出误差校准二次核？ 少数坐标可能主导softmax近似误差，统一处理所有维度会浪费近似能力。OAL先在post-RoPE空间识别稳定贡献分组，再学习共享组与组对的正定二次核。校准对齐最终聚合输出，而不只是权重，因为相同权重误差乘上不同value会产生不同后果；正定约束也保护归一化分母。 教学例子：两个注意力近似都错了相同权重，但一处value很大、另一处value几乎相同，输出影响不同。应比较最终读出的向量，而不只看权重图接近程度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-oal-9fb61fc3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5ef7344fcef7af22">OAL为什么按QK维度贡献分组，还要用attention输出误差校准二次核？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoal">Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>少数坐标可能主导softmax近似误差，统一处理所有维度会浪费近似能力。OAL先在post-RoPE空间识别稳定贡献分组，再学习共享组与组对的正定二次核。校准对齐最终聚合输出，而不只是权重，因为相同权重误差乘上不同value会产生不同后果；正定约束也保护归一化分母。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个注意力近似都错了相同权重，但一处value很大、另一处value几乎相同，输出影响不同。应比较最终读出的向量，而不只看权重图接近程度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13674">原论文</a> · <a href="../../../../reproductions/2610.13674-oal/">实现解读</a> · <a href="#qa-5ef7344fcef7af22">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:orthros" data-paper-title="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers 基础模型 The Hong Kong Polytechnic University 2026-10-09 长 prompt、短回答的推理中，prefill 与 decode 的计算角色不同。Orthros 保留两个 token 流：base tokens 对所有位置执行固定窗口 SWA，并构建完整的逐层 KV；output-specific tokens 只在需预测输出的位置出现，用共享 KV 做全历史 causal cross-attention。FFN、norm 和主要 Q/K/V/O 权重共享，但两种 query 各有可学习 affine 变换。 单seed/短序列结果仅L1，不复现论文21.9×、长上下文能力或生产吞吐。本地对照口径：共享小型预训练起点继续训练的Transformer为基线，转换并真实适配的Orthros为实验组；论文吞吐相对收益不适用，本地只报告固定预算NLL与cached/batch一致性。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 Orthros的prefill使用局部窗口，为什么decode还能够检索完整历史？ base流在每个位置执行滑窗注意力，但仍构建并保留全部逐层KV；只有需要预测输出的位置另开output-specific流，读取共享的全历史KV。输出流不写入KV。这里线性prefill指固定窗口下的计算规模，不是把历史换成线性attention状态，也不意味着完整缓存成本消失。 教学例子：长文档prefill时每个base位置只读邻近词，最后一个提示位置复制出输出查询去全局取证；开始回答后，每个新输出位置都可再次检索已保存的历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-orthros-ce7b4e60" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d753314406f18da1">Orthros的prefill使用局部窗口，为什么decode还能够检索完整历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aorthros">Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>base流在每个位置执行滑窗注意力，但仍构建并保留全部逐层KV；只有需要预测输出的位置另开output-specific流，读取共享的全历史KV。输出流不写入KV。这里线性prefill指固定窗口下的计算规模，不是把历史换成线性attention状态，也不意味着完整缓存成本消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长文档prefill时每个base位置只读邻近词，最后一个提示位置复制出输出查询去全局取证；开始回答后，每个新输出位置都可再次检索已保存的历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13735">原论文</a> · <a href="../../../../reproductions/2610.13735-orthros/">实现解读</a> · <a href="#qa-d753314406f18da1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rea" data-paper-title="Role-aware Heuristic Episodic Attention for Conversational LLMs" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Role-aware Heuristic Episodic Attention for Conversational LLMs 基础模型 原文首页未列第一作者机构 2026-10-01 把全局指令放入持久前缀，把多轮交互放入 episodic memory；检索时按角色决定保留原文、压缩表示或省略。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行角色分离与 episodic top-k；不调用压缩 LLM。执行角色分离与 episodic top-k；不调用压缩 LLM。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长上下文 会话记忆 注意力 基础模型 长上下文：注意力、递归状态与记忆 REA为何把全局指令保留为持久前缀，而不让它与聊天片段一起按相关性竞争？ 聊天记忆的某次相关性排序不应顺便删除持续有效的全局约束。REA把持久指令和情节记忆分开，对后者检索，并按角色决定保留原文、压缩或省略。它控制的是构成当前上下文的材料，而不是保证压缩后所有信息都可恢复；角色和检索规则仍需核验。 教学例子：用户早先规定输出必须用中文，最近谈论电影；电影片段可按问题相关性选择，而中文约束不应只因和电影关键词无关就被挤出上下文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-rea-ef53c923" class="ar-learning-paper-anchor"></span>
<h2 id="qa-958b8fd9fb9bf5ff">REA为何把全局指令保留为持久前缀，而不让它与聊天片段一起按相关性竞争？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Area">Role-aware Heuristic Episodic Attention for Conversational LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>聊天记忆的某次相关性排序不应顺便删除持续有效的全局约束。REA把持久指令和情节记忆分开，对后者检索，并按角色决定保留原文、压缩或省略。它控制的是构成当前上下文的材料，而不是保证压缩后所有信息都可恢复；角色和检索规则仍需核验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户早先规定输出必须用中文，最近谈论电影；电影片段可按问题相关性选择，而中文约束不应只因和电影关键词无关就被挤出上下文。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00958">原论文</a> · <a href="../../../../foundation-models/2610.00958-rea/">实现解读</a> · <a href="#qa-958b8fd9fb9bf5ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:triadic-linear-attention" data-paper-title="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling 基础模型 MIT / MIT-IBM Watson AI Lab 2026-09-29 普通线性注意力写入的二维状态；Triadic 再加入第二 key，写入，读取时用收缩两个 key 轴。第二 key 维度为时，状态容量乘以，只新增两组 projection；严格退化为普通线性注意力。 复现级别：L1 递推机制。复现级别：L1 递推机制。实现论文 Eq. (2)–(3) 的写入、双 query 收缩和按第二 key 轴衰减。triadic_linear_attention 是透明的 recurrent reference，测试对照显式求和、检查因果性、退化与梯度；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现论文 Triton chunkwise kernel、Gated DeltaNet upcycling 或长书语言建模，不能把小张量一致性当成论文效果复现。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 Triadic Linear Attention增加第二个key，容量和检索条件如何改变？ 普通线性attention把key与value写入二维状态；Triadic再加入第二个key轴，查询时用两组query共同收缩。这样关联同时受两种地址条件约束，状态容量随第二key维度增大，而不是免费扩容。第二维退化为1时应回到普通线性attention，是检查实现是否保留核心机制的边界。 教学例子：用人物和场景作为两种地址，同一个人物在不同场景对应不同value；第二key可帮助区分，但也需要保存更大的联合状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-triadic-linear-attention-debbb585" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6d8ba49e4e0aa0df">Triadic Linear Attention增加第二个key，容量和检索条件如何改变？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atriadic-linear-attention">Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT / MIT-IBM Watson AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通线性attention把key与value写入二维状态；Triadic再加入第二个key轴，查询时用两组query共同收缩。这样关联同时受两种地址条件约束，状态容量随第二key维度增大，而不是免费扩容。第二维退化为1时应回到普通线性attention，是检查实现是否保留核心机制的边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用人物和场景作为两种地址，同一个人物在不同场景对应不同value；第二key可帮助区分，但也需要保存更大的联合状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36529">原论文</a> · <a href="../../../../foundation-models/2609.36529-triadic-linear-attention/">实现解读</a> · <a href="#qa-6d8ba49e4e0aa0df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frac-ssm" data-paper-title="Fractional State Space Transition for Long Sequence Modeling" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Fractional State Space Transition for Long Sequence Modeling 基础模型 Huawei Noah&#x27;s Ark Lab, Montreal Research Center 2026-09-28 以对数间隔的有限指数模态逼近分数阶动力学的幂律记忆，在有界递归状态下兼顾长尾记忆和并行训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  状态空间模型 长上下文 基础模型 长上下文：注意力、递归状态与记忆 有限个递归状态，怎样近似分数阶系统很长的幂律记忆？ 单个指数模式只有一种衰减时间尺度；方法用对数间隔的多个指数模式共同逼近幂律尾部。快速模式追踪近期变化，慢速模式保留更远历史，组合后获得更宽的有效记忆范围。它仍是有限模式近似，因此状态容量和近似区间有限，不能据此宣称无限精确记忆。 教学例子：用快、中、慢三条衰减通道同时记录一次事件；短期主要由快通道贡献，过很久后由慢通道贡献。三者相加能比单一衰减更接近长尾影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-frac-ssm-9d35422b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-70c0b6310e5e85f1">有限个递归状态，怎样近似分数阶系统很长的幂律记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afrac-ssm">Fractional State Space Transition for Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab, Montreal Research Center</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个指数模式只有一种衰减时间尺度；方法用对数间隔的多个指数模式共同逼近幂律尾部。快速模式追踪近期变化，慢速模式保留更远历史，组合后获得更宽的有效记忆范围。它仍是有限模式近似，因此状态容量和近似区间有限，不能据此宣称无限精确记忆。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用快、中、慢三条衰减通道同时记录一次事件；短期主要由快通道贡献，过很久后由慢通道贡献。三者相加能比单一衰减更接近长尾影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36314">原论文</a> · <a href="../../../../foundation-models/2609.36314-frac-ssm/">实现解读</a> · <a href="#qa-70c0b6310e5e85f1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ms-gla" data-paper-title="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution 基础模型 International Institute of Information Technology Hyderabad 2026-09-28 单一时间分辨率的线性注意力容易形成表征瓶颈。MS-GLA 把 head budget 分配给多个尺度：先做无重叠 masked average pooling，再分别执行 GLA，最后以因果 hold 方式恢复到 token 分辨率，并由输入相关 softmax 路由融合。 未复现论文的 Flash kernel 和等参数训练。复现级别：L1 架构机制 + 真实 A100 前后向。复现级别：L1 架构机制 + 真实 A100 前后向。保留多尺度分解、因果 hold 对齐与输入相关融合；未复现论文的 Flash kernel 和等参数训练。当前 recurrent kernel 面向正确性而非吞吐，没有复刻 Triton/Flash 实现或论文参数规模。尚未接入 Evolve，避免把结构名登记误称为已可搜索与公平评价。MultiScaleGLA 是可前后向的紧凑 PyTorch 层；A100 receipt 只证明 CUDA 路径可运行。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 MS-GLA把几个token池化到一起后，怎样避免把未来信息漏给块前部？ 粗尺度分支先对不重叠块做masked平均，再运行GLA；一个块的汇总只有在块末token到达后才能对外可见。恢复token分辨率时使用因果hold，而不是把整块结果提前填回每个位置。多个时间尺度最后由输入相关权重融合，从而兼顾细粒度变化和更长时间范围。 教学例子：尺度4的块包含位置1到4；位置2不能读取由位置3、4共同形成的平均值。必须等到位置4结束后，后续位置才能使用这块的粗尺度状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-ms-gla-a1875a93" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ea64391758996402">MS-GLA把几个token池化到一起后，怎样避免把未来信息漏给块前部？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ams-gla">MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · International Institute of Information Technology Hyderabad</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>粗尺度分支先对不重叠块做masked平均，再运行GLA；一个块的汇总只有在块末token到达后才能对外可见。恢复token分辨率时使用因果hold，而不是把整块结果提前填回每个位置。多个时间尺度最后由输入相关权重融合，从而兼顾细粒度变化和更长时间范围。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>尺度4的块包含位置1到4；位置2不能读取由位置3、4共同形成的平均值。必须等到位置4结束后，后续位置才能使用这块的粗尺度状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35664">原论文</a> · <a href="../../../../foundation-models/2609.35664-ms-gla/">实现解读</a> · <a href="#qa-ea64391758996402">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oda" data-paper-title="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall 基础模型 Southern University of Science and Technology 2026-09-17 默认只读局部 KV，由轻量 recall head 在全局注意力发生前预测其收益；仅高收益 token 触发全局读取，完整 KV 仍保留。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。  注意力与长上下文 推理效率 基础模型 长上下文：注意力、递归状态与记忆 On-Demand Attention默认只读局部KV，什么时候才调用全局检索？ 轻量recall head先预测一次全局注意力的预期收益，在真正执行昂贵全局读取前作决定；只有值得的token才触发。完整KV仍被保存，所以省掉的是部分解码位置的读取计算，不能据此声称缓存已经被删除或压缩。判断器漏判时，也可能失去本应使用的远程证据。 教学例子：连续生成固定格式标点时可能仅靠局部状态；到了需要引用开头编号的位置，再触发全局读取。这个触发决定必须先作，不能先花全局成本再宣称省掉了它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-oda-5fd8c6ed" class="ar-learning-paper-anchor"></span>
<h2 id="qa-63a2a877c0ad9062">On-Demand Attention默认只读局部KV，什么时候才调用全局检索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoda">On-Demand Attention: Efficient Long-Context Decoding with Learned Recall</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southern University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轻量recall head先预测一次全局注意力的预期收益，在真正执行昂贵全局读取前作决定；只有值得的token才触发。完整KV仍被保存，所以省掉的是部分解码位置的读取计算，不能据此声称缓存已经被删除或压缩。判断器漏判时，也可能失去本应使用的远程证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续生成固定格式标点时可能仅靠局部状态；到了需要引用开头编号的位置，再触发全局读取。这个触发决定必须先作，不能先花全局成本再宣称省掉了它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20734">原论文</a> · <a href="../../../../foundation-models/2609.20734-oda/">实现解读</a> · <a href="#qa-63a2a877c0ad9062">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sas-attention" data-paper-title="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking 基础模型 Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST 2026-09-11 硬 Top-K 只能改变被选中的索引，语言模型损失无法沿离散索引直接训练 selector。SAS 不再蒸馏 dense attention：selector 先给历史块连续打分，训练时保留 Top-K 块的连续 gate，并把 log(gate) 加到注意力 logits 内。这样最终 token prediction loss 可直接优化“哪些上下文真正影响预测”。历史块 gate 共同 softmax 归一化，当前块始终使用单位 gate，避免历史上下文整体权重漂移。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地真实训练冻结主干后的 selector，执行 softmax 归一化 gate、历史块 Top-K、当前块常驻和 attention softmax 内的 log-gate；不把 PyTorch 参考实现宣称为 Triton 加速实现。本地实现物化稠密注意力矩阵，仅用于验证论文的选择与梯度机制；没有复刻 Qwen3-4B/8B/14B、OLMo3-7B、OpenR1-Math-220k、LongBench、BFCL、VitaBench，也没有接入原文 Triton/FlashAttention kernel 和 SGLang benchmark。  sparse-attention long-context post-training context-ranking 基础模型 长上下文：注意力、递归状态与记忆 Top-K索引不可导，SAS怎样仍让语言模型损失训练上下文selector？ 它没有声称让离散索引本身变得可导，而是在选中历史块后保留连续gate，并把log gate加进attention的softmax内部。最终预测损失可以沿这些连续数值更新selector。历史gate共同归一化，当前块固定单位gate，避免整体历史权重无约束漂移。 教学例子：两个选中块都进入attention，但gate从0.8、0.2变为0.6、0.4会改变最终输出；损失可据此学习。只留下两个整数索引而丢掉gate，就没有这条梯度通路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-sas-attention-90d42e99" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d6b2dc7c35d29a0f">Top-K索引不可导，SAS怎样仍让语言模型损失训练上下文selector？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asas-attention">SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它没有声称让离散索引本身变得可导，而是在选中历史块后保留连续gate，并把log gate加进attention的softmax内部。最终预测损失可以沿这些连续数值更新selector。历史gate共同归一化，当前块固定单位gate，避免整体历史权重无约束漂移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个选中块都进入attention，但gate从0.8、0.2变为0.6、0.4会改变最终输出；损失可据此学习。只留下两个整数索引而丢掉gate，就没有这条梯度通路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13141">原论文</a> · <a href="../../../../reproductions/2609.13141-sas-attention/">实现解读</a> · <a href="#qa-d6b2dc7c35d29a0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:olmpool-long-context" data-paper-title="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension 基础模型 Ai2 2026-08-10 以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 olmpool-long-context；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 网络架构 基础模型 长上下文：注意力、递归状态与记忆 比较两种长上下文扩展方法时，为什么只对齐模型参数量仍然不够？ 相同参数规模的模型也可能采用不同归一化、GQA、预训练窗口和滑窗结构；这些选择会共同改变长上下文行为。受控模型池把这些因素分开比较，防止把底座差异误归因于扩展方法。一个模型在某个长度上成功，不等于某种位置或注意力改动在所有底座上都有效。 教学例子：A模型训练时已见更长窗口，B模型只见短窗口；扩展后A更强，不能直接归功于其扩展算法。应先固定底座条件，再改变待研究的因素。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-olmpool-long-context-26415a28" class="ar-learning-paper-anchor"></span>
<h2 id="qa-43e1a94b62bc3646">比较两种长上下文扩展方法时，为什么只对齐模型参数量仍然不够？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aolmpool-long-context">Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ai2</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同参数规模的模型也可能采用不同归一化、GQA、预训练窗口和滑窗结构；这些选择会共同改变长上下文行为。受控模型池把这些因素分开比较，防止把底座差异误归因于扩展方法。一个模型在某个长度上成功，不等于某种位置或注意力改动在所有底座上都有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A模型训练时已见更长窗口，B模型只见短窗口；扩展后A更强，不能直接归功于其扩展算法。应先固定底座条件，再改变待研究的因素。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10296">原论文</a> · <a href="../../../../reproductions/2608.10296-olmpool-long-context/">实现解读</a> · <a href="#qa-43e1a94b62bc3646">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:autonomy-heads" data-paper-title="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry 基础模型 Institute of Computing Technology, Chinese Academy of Sciences 2026-08-07 直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 autonomy-heads；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 没有校准样本，Autonomy-of-Heads凭什么给不同head分配不同稀疏模式？ 它检查冻结的Q/K投影所形成的几何结构，用奇异值分布的谱有效秩描述头的潜在匹配能力，再区分偏检索和偏流式处理的头。选择依据来自模型参数，而非额外样本上运行一个门控器。因此省掉校准与运行时选择成本，但参数几何不能替代真实任务上的效果验证。 教学例子：两个头拥有相同窗口预算，但一个投影只突出很少方向，另一个能区分更多方向；方法先据此分配注意力方式，再检查任务是否真的保留所需证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-autonomy-heads-2d7238b5" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6d644b6b25fc1e45">没有校准样本，Autonomy-of-Heads凭什么给不同head分配不同稀疏模式？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aautonomy-heads">Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它检查冻结的Q/K投影所形成的几何结构，用奇异值分布的谱有效秩描述头的潜在匹配能力，再区分偏检索和偏流式处理的头。选择依据来自模型参数，而非额外样本上运行一个门控器。因此省掉校准与运行时选择成本，但参数几何不能替代真实任务上的效果验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个头拥有相同窗口预算，但一个投影只突出很少方向，另一个能区分更多方向；方法先据此分配注意力方式，再检查任务是否真的保留所需证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06849">原论文</a> · <a href="../../../../reproductions/2608.06849-autonomy-heads/">实现解读</a> · <a href="#qa-6d644b6b25fc1e45">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dart" data-paper-title="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling 基础模型 Zhejiang University 2026-08-03 保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 dart；单 seed 变化为 +3.12% 个百分点。  网络架构 注意力与长上下文 基础模型 长上下文：注意力、递归状态与记忆 DART为何保留多个chunk的递归状态，而不是只用最后一个状态回答问题？ 单个递归状态把很多历史合并到固定容量，某条旧信息可能被之后的更新覆盖。DART保留分块产生的状态贡献，把它们解码成可查询的K/V，再让当前token通过attention选择相关状态，并与Mamba路径融合。它为递归摘要增加了可寻址的记忆入口，代价是额外保存和检索状态。 教学例子：一章记作者、一章记年份；最终状态可能偏重后一章。查询作者时，可回到前一块的状态贡献，而不必指望最后状态仍完整携带两项信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-dart-ebf1e36e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c3968b3b16484d2a">DART为何保留多个chunk的递归状态，而不是只用最后一个状态回答问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adart">DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个递归状态把很多历史合并到固定容量，某条旧信息可能被之后的更新覆盖。DART保留分块产生的状态贡献，把它们解码成可查询的K/V，再让当前token通过attention选择相关状态，并与Mamba路径融合。它为递归摘要增加了可寻址的记忆入口，代价是额外保存和检索状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一章记作者、一章记年份；最终状态可能偏重后一章。查询作者时，可回到前一块的状态贡献，而不必指望最后状态仍完整携带两项信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02032">原论文</a> · <a href="../../../../reproductions/2608.02032-dart/">实现解读</a> · <a href="#qa-c3968b3b16484d2a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttcd" data-paper-title="Learning What to Remember: Test-Time Training via Context Distillation" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Learning What to Remember: Test-Time Training via Context Distillation 基础模型 Princeton University 2026-08-03 长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 ttcd；单 seed 变化为 +78.12% 个百分点。  注意力与长上下文 测试时训练 基础模型 长上下文：注意力、递归状态与记忆 TTCD让短窗口学生学习长窗口教师的什么，而不只是模仿最终答案？ 长窗口教师提供隐藏状态层面的目标，监督学生的fast weights保留对后续预测有用的上下文信息。学生有限记忆需要学会筛选，而不是平均压缩每个历史token。隐藏状态蒸馏能表达中间信息差距，但仍不保证压缩记忆完整保存教师看到的所有细节。 教学例子：长文开头定义了一个变量，教师到结尾仍能直接读取；短窗口学生需把该定义写进fast weights，使后续状态接近教师，而不仅背下某一次结尾答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-ttcd-fe56ef12" class="ar-learning-paper-anchor"></span>
<h2 id="qa-62897b0d29fdf49d">TTCD让短窗口学生学习长窗口教师的什么，而不只是模仿最终答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attcd">Learning What to Remember: Test-Time Training via Context Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长窗口教师提供隐藏状态层面的目标，监督学生的fast weights保留对后续预测有用的上下文信息。学生有限记忆需要学会筛选，而不是平均压缩每个历史token。隐藏状态蒸馏能表达中间信息差距，但仍不保证压缩记忆完整保存教师看到的所有细节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长文开头定义了一个变量，教师到结尾仍能直接读取；短窗口学生需把该定义写进fast weights，使后续状态接近教师，而不仅背下某一次结尾答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01672">原论文</a> · <a href="../../../../reproductions/2608.01672-ttcd/">实现解读</a> · <a href="#qa-62897b0d29fdf49d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:transmem" data-paper-title="TransMem: Transforming Hidden States into Memory for Large Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="TransMem: Transforming Hidden States into Memory for Large Language Models 基础模型 Authors did not disclose affiliation 2026-07-31 将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 transmem；单 seed 变化为 +12.50% 个百分点。  注意力与长上下文 Agent 记忆 基础模型 长上下文：注意力、递归状态与记忆 TransMem把历史hidden states转成参数记忆，与一直保留原始历史有什么区别？ 它抽取冻结骨干的稀疏历史状态，再变换成可复用的记忆增量，并通过门控制其对当前状态的影响。原始上下文不再每次逐token参与同样的检索，信息经过变换与压缩，因此可复用性与细节保真之间有取舍。学习门控也不代表骨干本体已随每段历史重新训练。 教学例子：把一段已读说明压成可调用的记忆增量，后续问题可利用这份信息；如果压缩时丢了一个精确编号，记忆模块不能仅凭复用就保证把编号还原出来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-transmem-2625c67f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-322b52536e46b91b">TransMem把历史hidden states转成参数记忆，与一直保留原始历史有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atransmem">TransMem: Transforming Hidden States into Memory for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它抽取冻结骨干的稀疏历史状态，再变换成可复用的记忆增量，并通过门控制其对当前状态的影响。原始上下文不再每次逐token参与同样的检索，信息经过变换与压缩，因此可复用性与细节保真之间有取舍。学习门控也不代表骨干本体已随每段历史重新训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把一段已读说明压成可调用的记忆增量，后续问题可利用这份信息；如果压缩时丢了一个精确编号，记忆模块不能仅凭复用就保证把编号还原出来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29032">原论文</a> · <a href="../../../../reproductions/2607.29032-transmem/">实现解读</a> · <a href="#qa-322b52536e46b91b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gzip-sparse-attention" data-paper-title="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection 基础模型 Pennsylvania State University 2026-07-23 固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。50% heads 只看 local、25% 只看 literal long-range、25% 使用两者并集。 Fidelity: 核心机制复现。真实逐块执行 gzip、生成样本自适应 mask 并训练同参数 ByteLM；缩小 context、模型和训练步数。本地实现确实逐样本调用 gzip 并执行三类 head mask，但 PyTorch 仍计算 dense score matrix 后 masking，所以 edge 数下降不等于 wall-clock 加速。没有下载 28,602 本 PG-19、训练 92M 模型或使用 8K context；小预算负结果不能反驳论文的长上下文训练结论。  llm sparse-attention long-context compression 基础模型 长上下文：注意力、递归状态与记忆 gzip压不动的block为什么获得长程连接，这是否等于找到了重要内容？ 方法把较难压缩的字节块视为literal信息较丰富，以样本平均压缩率为阈值，让这些块之间建立长程边，同时保留局部窗口与因果约束。压缩率是无需训练的内容选择信号，并非语义重要性的真值；随机噪声也可能难压缩，而且literal块过多时长程边仍会变贵。 教学例子：重复模板容易压缩，独特编号往往更难压缩，后者可能需要跨段读取；但一段随机乱码也难压缩，所以还得验证这种连接是否服务于实际问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-gzip-sparse-attention-4236c23c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ff5a539f7aa258a3">gzip压不动的block为什么获得长程连接，这是否等于找到了重要内容？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agzip-sparse-attention">Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pennsylvania State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>方法把较难压缩的字节块视为literal信息较丰富，以样本平均压缩率为阈值，让这些块之间建立长程边，同时保留局部窗口与因果约束。压缩率是无需训练的内容选择信号，并非语义重要性的真值；随机噪声也可能难压缩，而且literal块过多时长程边仍会变贵。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>重复模板容易压缩，独特编号往往更难压缩，后者可能需要跨段读取；但一段随机乱码也难压缩，所以还得验证这种连接是否服务于实际问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21752">原论文</a> · <a href="../../../../reproductions/2607.21752-gzip-sparse-attention/">实现解读</a> · <a href="#qa-ff5a539f7aa258a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mobius-rope" data-paper-title="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable 基础模型 Independent researcher 2026-07-23 标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为；其余 heads 保留标准 RoPE，以维持语言建模能力。 未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；Fidelity: 核心机制复现。真实训练 standard RoPE 与 25% heads Möbius RoPE；缩小模型、语料和随机种子规模。未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；本地 needle task 是可审计的机制验证，且两组都接受相同 retrieval curriculum。本地对照口径：基线为 standard RoPE；  llm-architecture positional-encoding long-context 基础模型 长上下文：注意力、递归状态与记忆 Möbius位置编码跨训练窗口旋转成负单位阵，和标准RoPE有何不同？ 它为部分头使用反周期频率，使相隔一个训练窗口的旋转为负单位阵、两个窗口后回到单位阵。这样显式约束长距离位置关系；其余头保留标准RoPE以兼顾语言建模。它是改变某些头的位置几何，不是增加可访问的历史内容，也不自动保证所有长度上的检索。 教学例子：窗口长度为N时，相隔N的位置在这些头上受到统一反向旋转，而相隔2N回到同向；内容是否被正确检索，仍需由查询、键和训练共同决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-mobius-rope-d829e106" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9cea57bf909d2052">Möbius位置编码跨训练窗口旋转成负单位阵，和标准RoPE有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amobius-rope">Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它为部分头使用反周期频率，使相隔一个训练窗口的旋转为负单位阵、两个窗口后回到单位阵。这样显式约束长距离位置关系；其余头保留标准RoPE以兼顾语言建模。它是改变某些头的位置几何，不是增加可访问的历史内容，也不自动保证所有长度上的检索。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>窗口长度为N时，相隔N的位置在这些头上受到统一反向旋转，而相隔2N回到同向；内容是否被正确检索，仍需由查询、键和训练共同决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21405">原论文</a> · <a href="../../../../reproductions/2607.21405-mobius-rope/">实现解读</a> · <a href="#qa-9cea57bf909d2052">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:naju" data-paper-title="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory 基础模型 Independent researchers 2026-07-23 Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent 方向、短程因果卷积、直接 feedthrough 与输出调制。 Fidelity: 核心机制复现。真实执行 native-discrete selective recurrence 的完整 block；缩小模型与预训练预算。Python sequential recurrence 与论文 affine scan 数学等价，但没有作者 fused parallel kernel。未复跑 1.2B-token WikiText-103、Mamba/Mamba-2/xLSTM 和完整 LRA/MQAR；本地负结果只适用于当前规模。本地对照口径：基线为同 token、optimizer、70 steps 的 96-d、3-layer Transformer；  llm-architecture state-space-model long-context 基础模型 长上下文：注意力、递归状态与记忆 Naju为什么把保留门和写入门分开，不能只用一个互补门？ 若写入量固定等于一减保留量，强保留旧信息就会同时压低新信息写入。Naju直接参数化离散转移，并独立控制retain和write，所以可以同时较强地保留旧状态并接收新线索。token相关读写方向、局部卷积和直通路径仍各有作用，不应把它简化为一个固定指数滑动平均。 教学例子：已有状态记录人物名字，当前token补充其年龄；独立门允许保留名字并写入年龄，而不是为了增加年龄信息就被迫按同一比例擦掉旧状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-naju-616fb3d6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2e4296cda59e007b">Naju为什么把保留门和写入门分开，不能只用一个互补门？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anaju">Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若写入量固定等于一减保留量，强保留旧信息就会同时压低新信息写入。Naju直接参数化离散转移，并独立控制retain和write，所以可以同时较强地保留旧状态并接收新线索。token相关读写方向、局部卷积和直通路径仍各有作用，不应把它简化为一个固定指数滑动平均。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>已有状态记录人物名字，当前token补充其年龄；独立门允许保留名字并写入年龄，而不是为了增加年龄信息就被迫按同一比例擦掉旧状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21000">原论文</a> · <a href="../../../../reproductions/2607.21000-naju/">实现解读</a> · <a href="#qa-2e4296cda59e007b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:conv-llm" data-paper-title="Convolution for Large Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Convolution for Large Language Models 基础模型 Huawei / Peking University / Tsinghua University 2026-07-20 自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 kernel=3 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 0.01%。 未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；Fidelity: 核心机制复现。真实预训练同预算 Transformer 与 post-QKV residual depthwise Conv1D；缩小模型和语料规模。未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；本地结论只支持小模型短预算下的方向性收益。本地对照口径：基线是相同 96-d、3-layer、60-step Transformer；实验组仅增加 QKV 后残差 depthwise Conv1D，test perplexity 相对降低 0.29%。  llm-architecture attention depthwise-convolution 基础模型 长上下文：注意力、递归状态与记忆 Conv-LLM已经有attention，为什么还在Q/K/V投影后加三点卷积？ attention按内容在历史中选择位置，短卷积先给每个位置注入附近顺序模式。这里卷积作用于投影后的Q/K/V，并通过残差保留原值，再进入attention；它不是把整个全局交互替换为卷积。逐通道卷积控制额外参数，因果左填充避免提前读到后面的词。 教学例子：读取“不是很好”时，局部卷积可先把否定词与相邻词结合，再让增强后的查询去匹配远处上下文；卷积不能读取尚未出现的“好”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-conv-llm-13d560f4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ca1d3cdc7932365e">Conv-LLM已经有attention，为什么还在Q/K/V投影后加三点卷积？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aconv-llm">Convolution for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / Peking University / Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>attention按内容在历史中选择位置，短卷积先给每个位置注入附近顺序模式。这里卷积作用于投影后的Q/K/V，并通过残差保留原值，再进入attention；它不是把整个全局交互替换为卷积。逐通道卷积控制额外参数，因果左填充避免提前读到后面的词。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>读取“不是很好”时，局部卷积可先把否定词与相邻词结合，再让增强后的查询去匹配远处上下文；卷积不能读取尚未出现的“好”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18413">原论文</a> · <a href="../../../../reproductions/2607.18413-conv-llm/">实现解读</a> · <a href="#qa-ca1d3cdc7932365e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:minimax-sparse-attention" data-paper-title="MiniMax Sparse Attention" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MiniMax Sparse Attention 基础模型 MiniMax 2026-06-11 长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。Index branch、每 GQA 组 top-k block 和精确 sparse attention 均真实训练；109B 预训练与 fused kernel 未复刻。WikiText-2 上训练同初始化/同预算的 tiny dense GQA 与 blockwise MSA，报告 PPL、训练时间和实际 attention pair ratio。  llm sparse-attention gqa long-context 基础模型 长上下文：注意力、递归状态与记忆 MSA先选block再做精确attention，省掉的是哪一步，保留的又是什么？ 轻量索引分支先用较便宜的块级匹配缩小历史范围，主注意力仅对命中块内的token计算精确权重。因此不是把所有token都换成一个块均值；块摘要用于筛选，细粒度交互仍在被选区域发生。若索引漏掉答案所在块，后续精确attention也无法弥补。 教学例子：十页文档先选两页，再逐字寻找日期。省下的是其他八页的主注意力计算；若索引先删掉唯一包含日期的一页，细读剩余页面也找不到答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-minimax-sparse-attention-fdb70645" class="ar-learning-paper-anchor"></span>
<h2 id="qa-be7681bf09e68302">MSA先选block再做精确attention，省掉的是哪一步，保留的又是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aminimax-sparse-attention">MiniMax Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轻量索引分支先用较便宜的块级匹配缩小历史范围，主注意力仅对命中块内的token计算精确权重。因此不是把所有token都换成一个块均值；块摘要用于筛选，细粒度交互仍在被选区域发生。若索引漏掉答案所在块，后续精确attention也无法弥补。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十页文档先选两页，再逐字寻找日期。省下的是其他八页的主注意力计算；若索引先删掉唯一包含日期的一页，细读剩余页面也找不到答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.13392">原论文</a> · <a href="../../../../reproductions/2606.13392-minimax-sparse-attention/">实现解读</a> · <a href="#qa-be7681bf09e68302">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:switch-attention" data-paper-title="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers 基础模型 Peking University / Huawei Technologies 2026-03-27 静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。 Fidelity: 核心机制复现。实现逐 token 动态选择 full/local attention 的可学习 router。本地使用可微 soft router，未复刻论文 STE 硬路由、32K continual pretraining 和 branch-selective fused kernel。本地对照口径：基线是 full-attention tiny Transformer；实验组动态混合 full 与 16-token local attention；30-step perplexity 相对 +0.19%（近似持平但略差）。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 Switch Attention是给每层固定一种模式，还是逐token决定是否需要全局attention？ 它用细粒度router决定当前token走全局还是局部注意力，因此同一层里不同位置可以使用不同读取范围。训练需处理这种选择的离散性，不能把硬路由当作普通可微操作。计算收益取决于实际全局调用比例和实现开销，选择更稀疏本身不保证质量保持。 教学例子：一句话中多数连接词只需局部上下文，引用开头人名的位置则可能需要全局检索；固定整层都走全局，会把两类位置支付的成本混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-switch-attention-753b5e50" class="ar-learning-paper-anchor"></span>
<h2 id="qa-145fabe3734e92b3">Switch Attention是给每层固定一种模式，还是逐token决定是否需要全局attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswitch-attention">Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University / Huawei Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用细粒度router决定当前token走全局还是局部注意力，因此同一层里不同位置可以使用不同读取范围。训练需处理这种选择的离散性，不能把硬路由当作普通可微操作。计算收益取决于实际全局调用比例和实现开销，选择更稀疏本身不保证质量保持。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一句话中多数连接词只需局部上下文，引用开头人名的位置则可能需要全局检索；固定整层都走全局，会把两类位置支付的成本混在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26380">原论文</a> · <a href="../../../../reproductions/2603.26380-switch-attention/">实现解读</a> · <a href="#qa-145fabe3734e92b3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gated-attention" data-paper-title="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free 基础模型 Qwen / Alibaba 2025-05-10 softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。 未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；Fidelity: 核心机制复现。真实训练论文最优的 head-specific sigmoid gate，并记录门控分布。未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；本地只验证论文最优门控位置的实际训练路径。本地对照口径：基线是同预算 llama_modern；实验组只增加 post-SDPA 逐头 sigmoid gate，WikiText-2 LM loss 5.7471→5.7398，相对 -0.13%，PPL 相对 -0.72%。  llm-architecture attention-gating long-context 基础模型 长上下文：注意力、递归状态与记忆 Gated Attention的门为何放在SDPA输出之后，而不是先改attention分数？ 先完成每个头的注意力聚合，再用由当前输入产生的sigmoid门调制聚合结果，最后进入输出投影。这样门控制的是“当前头已经读出的信息该送出多少”，并在原本较线性的聚合到投影之间引入非线性。它与改变某个历史位置的softmax权重是不同控制对象。 教学例子：一个头读出了格式标记，另一个头读出了答案证据；当前查询的门可以抑制前者的整段输出，而不是重新指定每个历史token的注意力概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-gated-attention-0685e39f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6609c4e775bab9c1">Gated Attention的门为何放在SDPA输出之后，而不是先改attention分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agated-attention">Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先完成每个头的注意力聚合，再用由当前输入产生的sigmoid门调制聚合结果，最后进入输出投影。这样门控制的是“当前头已经读出的信息该送出多少”，并在原本较线性的聚合到投影之间引入非线性。它与改变某个历史位置的softmax权重是不同控制对象。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个头读出了格式标记，另一个头读出了答案证据；当前查询的门可以抑制前者的整段输出，而不是重新指定每个历史token的注意力概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.06708">原论文</a> · <a href="../../../../reproductions/2505.06708-gated-attention/">实现解读</a> · <a href="#qa-6609c4e775bab9c1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:moba" data-paper-title="MoBA: Mixture of Block Attention for Long-Context LLMs" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MoBA: Mixture of Block Attention for Long-Context LLMs 基础模型 Moonshot AI 2025-02-18 把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际将历史划分为 8-token blocks，以 query 对 block key centroid 的相似度选择 top-2 causal blocks，再在命中块内执行精确 attention；PyTorch reference 未复刻百万上下文 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 moba；相对 PPL +0.49%。  sparse-attention long-context block-routing 基础模型 长上下文：注意力、递归状态与记忆 MoBA选择少数远程block时，为什么还要保留当前的因果block？ 块级路由负责寻找远处相关区域，当前块则承载尚未完成的近邻上下文。保留当前因果块可避免路由遗漏局部连续信息，并通过因果掩码限制可见位置；命中块内部仍执行token级attention。稀疏收益来自少读一些块，不意味着任意删块都能保持相同分布。 教学例子：当前句子的主语刚出现在本块，而远处章节包含背景知识。即便路由更偏爱远程章节，也不能把刚出现的主语一起排除，更不能读取当前块尚未生成的后缀。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-moba-f8997c1b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-627cf3d7c1d91b13">MoBA选择少数远程block时，为什么还要保留当前的因果block？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amoba">MoBA: Mixture of Block Attention for Long-Context LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>块级路由负责寻找远处相关区域，当前块则承载尚未完成的近邻上下文。保留当前因果块可避免路由遗漏局部连续信息，并通过因果掩码限制可见位置；命中块内部仍执行token级attention。稀疏收益来自少读一些块，不意味着任意删块都能保持相同分布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前句子的主语刚出现在本块，而远处章节包含背景知识。即便路由更偏爱远程章节，也不能把刚出现的主语一起排除，更不能读取当前块尚未生成的后缀。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13189">原论文</a> · <a href="../../../../reproductions/2502.13189-moba/">实现解读</a> · <a href="#qa-627cf3d7c1d91b13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:native-sparse-attention" data-paper-title="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention 基础模型 DeepSeek 2025-02-16 全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。 未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；Fidelity: 核心机制复现。真实训练压缩、选择和滑窗三条注意力分支；未复刻论文的 Triton kernel 与 27B 训练。未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；结果只支持“核心三路算子可训练且在当前短预算有效”，不能外推论文的规模或速度结论。本地对照口径：基线是同维度、层数、token、AdamW 和 30-step 预算的 llama_modern；  llm-architecture sparse-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 NSA已经有压缩历史，为什么还要选择原始块和保留滑动窗口？ 压缩块提供便宜的全局轮廓，却可能抹掉关键token细节；选择分支再根据当前查询读取重要原始块，滑窗保留近期精确信息。三条路径承担不同信息粒度，从预训练起一起学习并融合，不是训练结束后临时删掉部分attention。三路都必须保持因果性。 教学例子：压缩摘要能告诉模型某章讲日期，却可能分不清两个年份；选中该章后读取原始token来区分，同时从滑窗保留当前句子的限定条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-native-sparse-attention-6720d24e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f731030c47e87c33">NSA已经有压缩历史，为什么还要选择原始块和保留滑动窗口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anative-sparse-attention">Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>压缩块提供便宜的全局轮廓，却可能抹掉关键token细节；选择分支再根据当前查询读取重要原始块，滑窗保留近期精确信息。三条路径承担不同信息粒度，从预训练起一起学习并融合，不是训练结束后临时删掉部分attention。三路都必须保持因果性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>压缩摘要能告诉模型某章讲日期，却可能分不清两个年份；选中该章后读取原始token来区分，同时从滑窗保留当前句子的限定条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.11089">原论文</a> · <a href="../../../../reproductions/2502.11089-native-sparse-attention/">实现解读</a> · <a href="#qa-f731030c47e87c33">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hymba" data-paper-title="Hymba: A Hybrid-head Architecture for Small Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Hymba: A Hybrid-head Architecture for Small Language Models 基础模型 NVIDIA 2024-11-20 同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在每层并行执行 causal attention 与深度卷积状态分支，并以输入相关 gate 融合；未复刻 1.5B 参数、meta tokens 和 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 hymba；相对 PPL +8.53%。  hybrid-attention-ssm small-language-model architecture 基础模型 长上下文：注意力、递归状态与记忆 Hymba为什么在同一层并行放attention和SSM，而不简单轮流堆两种层？ 并行分支让同一份当前输入同时获得显式历史读取和递归状态摘要，再融合两种输出。attention可补充直接检索，SSM提供另一种历史压缩路径；两者在一次层更新中协作。这样安排并不意味着两个分支免费运行，融合方式、KV缓存与状态预算仍共同影响成本。 教学例子：当前词既需要找回前文的一个名字，又依赖持续累积的语法状态；同层可分别读取具体位置与递归摘要，再把两种信号交给下一层。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-hymba-2cf1482a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-957edc876261c0c0">Hymba为什么在同一层并行放attention和SSM，而不简单轮流堆两种层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahymba">Hymba: A Hybrid-head Architecture for Small Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>并行分支让同一份当前输入同时获得显式历史读取和递归状态摘要，再融合两种输出。attention可补充直接检索，SSM提供另一种历史压缩路径；两者在一次层更新中协作。这样安排并不意味着两个分支免费运行，融合方式、KV缓存与状态预算仍共同影响成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前词既需要找回前文的一个名字，又依赖持续累积的语法状态；同层可分别读取具体位置与递归摘要，再把两种信号交给下一层。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13676">原论文</a> · <a href="../../../../reproductions/2411.13676-hymba/">实现解读</a> · <a href="#qa-957edc876261c0c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mamba" data-paper-title="Mamba: Linear-Time Sequence Modeling with Selective State Spaces" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Mamba: Linear-Time Sequence Modeling with Selective State Spaces 基础模型 Carnegie Mellon University / Princeton University 2023-12-01 Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。 Fidelity: 核心机制复现。实现输入相关的 selective SSM、因果 depthwise convolution 与门控输出。未使用 fused parallel scan CUDA kernel，也没有 2.8B 规模预训练；短预算结果不代表论文规模结论。本地对照口径：基线是 tiny Transformer；实验组是原生 PyTorch selective scan；WikiText-2 30-step perplexity 相对 +48.82%（变差）。  llm-architecture state-space-model classic 基础模型 长上下文：注意力、递归状态与记忆 Mamba的“选择性”具体改变了SSM的什么，而不只是给输出加一个门？ 它让步长及读写方向随当前token变化，从而改变旧状态保留多久、当前输入写入哪里，以及状态怎样被读出。选择发生在递归更新内部，不只是最后对固定SSM结果做缩放。历史通过有限状态传播，长序列计算可保持线性，但精确找回任意旧token仍受状态容量影响。 教学例子：连续读到无关填充词时可以尽量保留已有状态，遇到关键编号时改变写入方向；之后回答编号仍取决于那部分信息是否被状态保留下来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-mamba-0b65990c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-53597ba087ad9762">Mamba的“选择性”具体改变了SSM的什么，而不只是给输出加一个门？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amamba">Mamba: Linear-Time Sequence Modeling with Selective State Spaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University / Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它让步长及读写方向随当前token变化，从而改变旧状态保留多久、当前输入写入哪里，以及状态怎样被读出。选择发生在递归更新内部，不只是最后对固定SSM结果做缩放。历史通过有限状态传播，长序列计算可保持线性，但精确找回任意旧token仍受状态容量影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续读到无关填充词时可以尽量保留已有状态，遇到关键编号时改变写入方向；之后回答编号仍取决于那部分信息是否被状态保留下来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.00752">原论文</a> · <a href="../../../../reproductions/2312.00752-mamba/">实现解读</a> · <a href="#qa-53597ba087ad9762">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alibi" data-paper-title="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation 基础模型 University of Washington / Meta AI 2021-08-27 不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际移除位置 embedding，并对各 attention head 加不同斜率的因果距离线性 bias；WikiText-2 小模型未复跑论文 WikiText-103 1.3B 参数实验。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 alibi；相对 PPL +0.06%。  position-encoding length-extrapolation attention 基础模型 长上下文：注意力、递归状态与记忆 ALiBi不加位置向量，模型怎样知道两个token离得有多远？ 它直接在每个注意力头的匹配分数上减去与距离成正比的偏置。距离越远，读到该位置需要更强的内容匹配来抵消惩罚；不同头的斜率提供不同距离偏好。偏置可以在更长位置上计算，不依赖一张只训练到固定长度的位置表，但这不保证任意长上下文都能正确检索。 教学例子：两个历史词的内容分数相同，一个距离2、一个距离20；距离惩罚让较近者得到更高权重。若远处包含独特答案，它仍需凭更强内容匹配胜出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-alibi-69e595a8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d919373883619f72">ALiBi不加位置向量，模型怎样知道两个token离得有多远？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalibi">Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它直接在每个注意力头的匹配分数上减去与距离成正比的偏置。距离越远，读到该位置需要更强的内容匹配来抵消惩罚；不同头的斜率提供不同距离偏好。偏置可以在更长位置上计算，不依赖一张只训练到固定长度的位置表，但这不保证任意长上下文都能正确检索。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个历史词的内容分数相同，一个距离2、一个距离20；距离惩罚让较近者得到更高权重。若远处包含独特答案，它仍需凭更强内容匹配胜出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2108.12409">原论文</a> · <a href="../../../../reproductions/2108.12409-alibi/">实现解读</a> · <a href="#qa-d919373883619f72">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rope" data-paper-title="RoFormer: Enhanced Transformer with Rotary Position Embedding" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="RoFormer: Enhanced Transformer with Rotary Position Embedding 基础模型 Zhuiyi Technology 2021-04-20 对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际对每个注意力 head 的 Q/K 执行复数平面旋转并由相对相位进入 dot product；WikiText-2 64d 小模型替代论文中文 RoFormer 预训练。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 rope；相对 PPL +0.00%。  position-encoding long-context architecture 基础模型 长上下文：注意力、递归状态与记忆 RoPE给Q和K分别加了绝对位置旋转，为什么点积却能表达相对位置？ 位置m、n对应的旋转在点积中组合，前一个旋转的转置抵消共同的绝对部分，留下与n减m相关的旋转。因此内容匹配中自然带上相对位移。被旋转的是Q/K子空间，不是把value直接标成位置；能计算更远位置也不等于经过训练的检索能力无限外推。 教学例子：把两个词同时从位置3、8平移到13、18，二者距离仍是5；位置旋转在点积中的相对关系保持一致，而内容本身仍由投影决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-rope-baa4b020" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9430b8ac22a0b9f9">RoPE给Q和K分别加了绝对位置旋转，为什么点积却能表达相对位置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arope">RoFormer: Enhanced Transformer with Rotary Position Embedding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhuiyi Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置m、n对应的旋转在点积中组合，前一个旋转的转置抵消共同的绝对部分，留下与n减m相关的旋转。因此内容匹配中自然带上相对位移。被旋转的是Q/K子空间，不是把value直接标成位置；能计算更远位置也不等于经过训练的检索能力无限外推。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把两个词同时从位置3、8平移到13、18，二者距离仍是5；位置旋转在点积中的相对关系保持一致，而内容本身仍由投影决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2104.09864">原论文</a> · <a href="../../../../reproductions/2104.09864-rope/">实现解读</a> · <a href="#qa-9430b8ac22a0b9f9">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

上下文变长时，模型保留的是可寻址的历史 token，还是压缩后的递归状态？

## 记住这一点

先分清位置关系、信息访问和状态容量。RoPE 对 Q/K 的二维子空间作位置相关旋转，让点积表达相对位移；它仍允许注意力访问窗口内历史。Mamba 则让状态更新的步长和读写参数依赖当前输入，把历史汇入递归状态。稀疏注意力和混合结构在两端之间选择：只读部分历史，或让部分层保留完整访问。

## 一个例子

假设文档开头定义变量 x，三万 token 后要找回定义。完整注意力可以直接查询对应位置；递归模型必须把所需信息持续保存在状态里。若只保留局部窗口，就要检查有没有全局层或额外记忆，而不能只看宣传的上下文长度。

## 什么时候要小心

线性复杂度不保证长距离精确检索，也不保证真实硬件更快。RoPE 不是无限长度外推保证；状态、窗口、训练长度和位置缩放都要一起核对。当前本地小模型结果不代表论文规模的能力。

## 先读这几篇

先读 RoFormer 的 Q/K 旋转，理解位置与相对关系；再读 Mamba 的输入相关状态更新，比较“直接读取历史”和“把历史写入状态”。之后按需要进入稀疏注意力、混合结构或外部记忆。

1. [RoFormer: Enhanced Transformer with Rotary Position Embedding](../../../reproductions/2104.09864-rope/README.md) · [原论文](https://arxiv.org/abs/2104.09864)
2. [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](../../../reproductions/2312.00752-mamba/README.md) · [原论文](https://arxiv.org/abs/2312.00752)

## 自测一下

两个模型都支持 32k 输入，是否说明它们能同样准确地找回首段的任意细节？

??? note "展开参考答案"

    不能。输入长度只说明接口或运行范围；直接寻址、窗口裁剪、状态容量和训练分布不同，可能造成不同遗忘。应在同预算下用位置与干扰长度受控的检索任务验证。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
