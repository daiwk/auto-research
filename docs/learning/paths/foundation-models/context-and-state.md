---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 长上下文：注意力、递归状态与记忆

[基础模型](index.md) / 子主题导学 · 约 3 分钟 · 31 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 31 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="OpenAttention: One Percent Is Enough with Tail Proxies 基础模型 Sogang University 2026-10-22 低读取率稀疏注意力不只需要选出少量重要 KV，还需要处理未读取的尾部。OpenAttention 在 query 二阶矩定义的几何空间内聚类，以 ErrorGate 估计簇内代理误差并分配精确读取预算；每个簇的未读部分成为一个带计数的均值代理。它不是单纯的 top-k 截断或均值池化。 完整实验成本过高，不复现（审查 DONE）。该小规模诊断仅核对公式与可执行性，不是语言模型能力比较。fit_cache、qgs_scores、errorgate、waterfill、residual_proxy_attention、attend 真实执行完整单头算子链。为便于独立核对，残余均值直接从未读行重算，而不是移植 Triton 的缓存和减法实现。全零误差按等权 water filling 处理；排序并列按原位置，空簇保持无代理，均为显式确定性边界。  高效注意力 KV缓存与稀疏推理 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-openattention-57f03e45">OpenAttention: One Percent Is Enough with Tail Proxies</h2>
<p class="ar-learning-card__meta">Sogang University · 论文公开：2026-10-22</p>
<p><strong>方法要点：</strong>低读取率稀疏注意力不只需要选出少量重要 KV，还需要处理未读取的尾部。OpenAttention 在 query 二阶矩定义的几何空间内聚类，以 ErrorGate 估计簇内代理误差并分配精确读取预算；每个簇的未读部分成为一个带计数的均值代理。它不是单纯的 top-k 截断或均值池化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。该小规模诊断仅核对公式与可执行性，不是语言模型能力比较。fit_cache、qgs_scores、errorgate、waterfill、residual_proxy_attention、attend 真实执行完整单头算子链。为便于独立核对，残余均值直接从未读行重算，而不是移植 Triton 的缓存和减法实现。全零误差按等权 water filling 处理；排序并列按原位置，空簇保持无代理，均为显式确定性边界。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30951v1">原论文</a> · <a href="../../../../foundation-models/2610.30951-openattention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Rethinking Sequence Compression with Test-time Regression 基础模型 The Chinese University of Hong Kong 2026-10-22 固定池化或投影分别聚合 token，难以按当前输入的相关结构调整压缩。TTR 把一组 token 视作回归观测：由 token 方向构造 key，由保留模长的原始 token 生成可学习标量 target；每次前向精确求解 ridge 系数，直接把系数作为压缩表示。外层任务 loss 通过闭式求解训练 target 投影与正则。“test-time”指输入相关的回归系数在前向内重新拟合，不表示推理时更新模型参数。基础版本只有个可训练参数，不是另建一个 agent 或训练时读取正确压缩答案。 完整模型训练和多基准评估成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列。三个 seed 不会把机制诊断升级成能力复现。ttr_compress 独立实现正对角 generalized ridge 与 dual Cholesky；TTRCompressor 将注册成可训练参数。diagnostic(seed, device=&#x27;cpu&#x27;) 生成4组、每组7个12维 token，执行外层反传和一次真实 SGD 更新，返回严格的 seed/metrics/checks。既不下载数据或权重，也不调用 pretrained 模型。  序列压缩 可微测试时回归 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-ttr-compressor-1230f560">Rethinking Sequence Compression with Test-time Regression</h2>
<p class="ar-learning-card__meta">The Chinese University of Hong Kong · 论文公开：2026-10-22</p>
<p><strong>方法要点：</strong>固定池化或投影分别聚合 token，难以按当前输入的相关结构调整压缩。TTR 把一组 token 视作回归观测：由 token 方向构造 key，由保留模长的原始 token 生成可学习标量 target；每次前向精确求解 ridge 系数，直接把系数作为压缩表示。外层任务 loss 通过闭式求解训练 target 投影与正则。“test-time”指输入相关的回归系数在前向内重新拟合，不表示推理时更新模型参数。基础版本只有个可训练参数，不是另建一个 agent 或训练时读取正确压缩答案。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整模型训练和多基准评估成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列。三个 seed 不会把机制诊断升级成能力复现。ttr_compress 独立实现正对角 generalized ridge 与 dual Cholesky；TTRCompressor 将注册成可训练参数。diagnostic(seed, device=&#x27;cpu&#x27;) 生成4组、每组7个12维 token，执行外层反传和一次真实 SGD 更新，返回严格的 seed/metrics/checks。既不下载数据或权重，也不调用 pretrained 模型。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31574v1">原论文</a> · <a href="../../../../foundation-models/2610.31574-ttr-compressor/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity 基础模型 Rice University 2026-10-20 只保留 top-k 会丢掉尾部质量；均匀抽样又浪费预算。SSA先确定保留高概率项，再按残差代理分布抽样。关键不是“top-k加采样”的外形，而是有放回抽样后去重，按每个token至少出现一次的包含概率修正。论文的自适应 Algorithm 1 与实际优化内核的固定 heavy fraction 版本不同；本地实现前者，不冒充后者的速度。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不自动重试。L1诊断不是正式能力比较，不参与Evolve晋级。stratified_sparse_attention 接受单query、keys、values和外部代理分数，真实执行water-filling、离散采样和精确选中项打分。梯度只通过实际选中Q/K/V；代理分配是detached离散步骤。没有声称实现PQCache代理、层级采样或paged KV runtime。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-stratified-sparse-attention-869759f6">Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity</h2>
<p class="ar-learning-card__meta">Rice University · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>只保留 top-k 会丢掉尾部质量；均匀抽样又浪费预算。SSA先确定保留高概率项，再按残差代理分布抽样。关键不是“top-k加采样”的外形，而是有放回抽样后去重，按每个token至少出现一次的包含概率修正。论文的自适应 Algorithm 1 与实际优化内核的固定 heavy fraction 版本不同；本地实现前者，不冒充后者的速度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不自动重试。L1诊断不是正式能力比较，不参与Evolve晋级。stratified_sparse_attention 接受单query、keys、values和外部代理分数，真实执行water-filling、离散采样和精确选中项打分。梯度只通过实际选中Q/K/V；代理分配是detached离散步骤。没有声称实现PQCache代理、层级采样或paged KV runtime。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28441v1">原论文</a> · <a href="../../../../foundation-models/2610.28441-stratified-sparse-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Kronecker Delta Rule for Long Context Linear Attention 基础模型 Johannes Kepler University Linz 2026-10-19 标准 DeltaNet 用向量误差更新矩阵记忆，会干扰与当前 key 重叠的其他关联。Kronecker Delta Rule 修正的是一个 key-value 对的标量关联；记忆修订沿的单一矩阵方向进行。KronLSTM 再加入 key 轴逐通道遗忘和分离 erase/write 门。 完整实验显著超出单张 A100/A30 或本地 Mac 的日常预算，成本过高，不复现（审查 DONE）。kronecker_update 保存标量关联擦除与 key 轴忘记；TinyKronLSTM 包含真实投影、短卷积、归一化、四类输入相关门、循环记忆和输出投影。它不是把普通 DeltaNet 换个名字，也不是仅记录配置。当前是 PyTorch 循环版，未实现论文 Appendix A8 的融合 chunkwise 前后向内核，不宣称相同吞吐量。  注意力与长上下文 线性注意力与递归记忆 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-kronlstm-ae88fcaa">Kronecker Delta Rule for Long Context Linear Attention</h2>
<p class="ar-learning-card__meta">Johannes Kepler University Linz · 论文公开：2026-10-19</p>
<p><strong>方法要点：</strong>标准 DeltaNet 用向量误差更新矩阵记忆，会干扰与当前 key 重叠的其他关联。Kronecker Delta Rule 修正的是一个 key-value 对的标量关联；记忆修订沿的单一矩阵方向进行。KronLSTM 再加入 key 轴逐通道遗忘和分离 erase/write 门。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验显著超出单张 A100/A30 或本地 Mac 的日常预算，成本过高，不复现（审查 DONE）。kronecker_update 保存标量关联擦除与 key 轴忘记；TinyKronLSTM 包含真实投影、短卷积、归一化、四类输入相关门、循环记忆和输出投影。它不是把普通 DeltaNet 换个名字，也不是仅记录配置。当前是 PyTorch 循环版，未实现论文 Appendix A8 的融合 chunkwise 前后向内核，不宣称相同吞吐量。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26834">原论文</a> · <a href="../../../../foundation-models/2610.26834-kronlstm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Open-world AI: a Tale of Three Requirements 基础模型 FAIR, Meta 2026-10-14 固定任务的 IID 泛化不等于在开放世界中学习新任务。论文提出推理时学习、丰富表示和预测性解耦三个要求。§3.2 的 Mosaics+ 用短期模块先处理近期依赖，再以 Gaussian-kernel 长期记忆检索预测关联；two-stage 版本分别估计当前任务与相关任务，避免一锅混池让不相关历史越多越有害。 单张 A100/A30 不适合完整多臂训练，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。不下载公开语料或 checkpoint。固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1，seeds42/43/44；每个 seed 使用2条8-token、16维随机输入和明确文档边界。短窗2、skip1 是缩小的算子配置，不等于原文256/64设定。随机目标只用于确认训练路径，不是任务测试答案。  网络架构 关联记忆与推理时学习 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-memory-mosaics-plus-a2cfe6c3">Open-world AI: a Tale of Three Requirements</h2>
<p class="ar-learning-card__meta">FAIR, Meta · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>固定任务的 IID 泛化不等于在开放世界中学习新任务。论文提出推理时学习、丰富表示和预测性解耦三个要求。§3.2 的 Mosaics+ 用短期模块先处理近期依赖，再以 Gaussian-kernel 长期记忆检索预测关联；two-stage 版本分别估计当前任务与相关任务，避免一锅混池让不相关历史越多越有害。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>单张 A100/A30 不适合完整多臂训练，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。不下载公开语料或 checkpoint。固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1，seeds42/43/44；每个 seed 使用2条8-token、16维随机输入和明确文档边界。短窗2、skip1 是缩小的算子配置，不等于原文256/64设定。随机目标只用于确认训练路径，不是任务测试答案。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20782">原论文</a> · <a href="../../../../foundation-models/2610.20782-memory-mosaics-plus/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels 基础模型 The Chinese University of Hong Kong, Shenzhen 2026-10-09 预训练 attention 的 QK 各维度贡献不均匀，少量高贡献坐标包含较多 softmax 近似误差。OAL 先在 post-RoPE QK 上计算因果贡献，以 prompt bootstrap 识别高贡献尾部的稳定边界；随后学习共享组和组对系数的二次核。正半定参数化保证分母严格正，并用真实 attention 输出 MSE 校准，而不是仅拟合 attention 权重。校准之后保留前后 softmax 层，对中间层进行转换，并在所有层的 q/k/v/o 上做 LoRA，联合训练核系数。 小规模诊断不作稳定提升声明，相对原文效果百分比不适用。cpu-contracts.json记录已重跑的 5 个测试：因果贡献公式、bootstrap/无人工组数上限、正核与 dense/HD 等价、输出校准梯度、实际 Qwen 模块转换与 LoRA 梯度。每项先固定 seed 42，递推等价/校准专用用例内部使用 seed 11/2；不是独立多 seed 能力实验。没有 CPU 单测到 A100 完成的自动晋级。core_mechanism / L1：保留 QK 分组、正核、真实输出校准和真实 Base checkpoint 的 LoRA 联合更新。小 batch 训练使用精确 dense kernel；  推理与系统效率 注意力线性化 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-oal-9fb61fc3">Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels</h2>
<p class="ar-learning-card__meta">The Chinese University of Hong Kong, Shenzhen · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>预训练 attention 的 QK 各维度贡献不均匀，少量高贡献坐标包含较多 softmax 近似误差。OAL 先在 post-RoPE QK 上计算因果贡献，以 prompt bootstrap 识别高贡献尾部的稳定边界；随后学习共享组和组对系数的二次核。正半定参数化保证分母严格正，并用真实 attention 输出 MSE 校准，而不是仅拟合 attention 权重。校准之后保留前后 softmax 层，对中间层进行转换，并在所有层的 q/k/v/o 上做 LoRA，联合训练核系数。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>小规模诊断不作稳定提升声明，相对原文效果百分比不适用。cpu-contracts.json记录已重跑的 5 个测试：因果贡献公式、bootstrap/无人工组数上限、正核与 dense/HD 等价、输出校准梯度、实际 Qwen 模块转换与 LoRA 梯度。每项先固定 seed 42，递推等价/校准专用用例内部使用 seed 11/2；不是独立多 seed 能力实验。没有 CPU 单测到 A100 完成的自动晋级。core_mechanism / L1：保留 QK 分组、正核、真实输出校准和真实 Base checkpoint 的 LoRA 联合更新。小 batch 训练使用精确 dense kernel；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13674">原论文</a> · <a href="../../../../reproductions/2610.13674-oal/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers 基础模型 The Hong Kong Polytechnic University 2026-10-09 长 prompt、短回答的推理中，prefill 与 decode 的计算角色不同。Orthros 保留两个 token 流：base tokens 对所有位置执行固定窗口 SWA，并构建完整的逐层 KV；output-specific tokens 只在需预测输出的位置出现，用共享 KV 做全历史 causal cross-attention。FFN、norm 和主要 Q/K/V/O 权重共享，但两种 query 各有可学习 affine 变换。 单seed/短序列结果仅L1，不复现论文21.9×、长上下文能力或生产吞吐。本地对照口径：共享小型预训练起点继续训练的Transformer为基线，转换并真实适配的Orthros为实验组；论文吞吐相对收益不适用，本地只报告固定预算NLL与cached/batch一致性。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-orthros-ce7b4e60">Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers</h2>
<p class="ar-learning-card__meta">The Hong Kong Polytechnic University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>长 prompt、短回答的推理中，prefill 与 decode 的计算角色不同。Orthros 保留两个 token 流：base tokens 对所有位置执行固定窗口 SWA，并构建完整的逐层 KV；output-specific tokens 只在需预测输出的位置出现，用共享 KV 做全历史 causal cross-attention。FFN、norm 和主要 Q/K/V/O 权重共享，但两种 query 各有可学习 affine 变换。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>单seed/短序列结果仅L1，不复现论文21.9×、长上下文能力或生产吞吐。本地对照口径：共享小型预训练起点继续训练的Transformer为基线，转换并真实适配的Orthros为实验组；论文吞吐相对收益不适用，本地只报告固定预算NLL与cached/batch一致性。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13735">原论文</a> · <a href="../../../../reproductions/2610.13735-orthros/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Role-aware Heuristic Episodic Attention for Conversational LLMs 基础模型 原文首页未列第一作者机构 2026-10-01 把全局指令放入持久前缀，把多轮交互放入 episodic memory；检索时按角色决定保留原文、压缩表示或省略。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行角色分离与 episodic top-k；不调用压缩 LLM。执行角色分离与 episodic top-k；不调用压缩 LLM。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长上下文 会话记忆 注意力 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-rea-ef53c923">Role-aware Heuristic Episodic Attention for Conversational LLMs</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>把全局指令放入持久前缀，把多轮交互放入 episodic memory；检索时按角色决定保留原文、压缩表示或省略。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行角色分离与 episodic top-k；不调用压缩 LLM。执行角色分离与 episodic top-k；不调用压缩 LLM。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00958">原论文</a> · <a href="../../../../foundation-models/2610.00958-rea/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling 基础模型 MIT / MIT-IBM Watson AI Lab 2026-09-29 普通线性注意力写入的二维状态；Triadic 再加入第二 key，写入，读取时用收缩两个 key 轴。第二 key 维度为时，状态容量乘以，只新增两组 projection；严格退化为普通线性注意力。 复现级别：L1 递推机制。复现级别：L1 递推机制。实现论文 Eq. (2)–(3) 的写入、双 query 收缩和按第二 key 轴衰减。triadic_linear_attention 是透明的 recurrent reference，测试对照显式求和、检查因果性、退化与梯度；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现论文 Triton chunkwise kernel、Gated DeltaNet upcycling 或长书语言建模，不能把小张量一致性当成论文效果复现。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-triadic-linear-attention-debbb585">Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling</h2>
<p class="ar-learning-card__meta">MIT / MIT-IBM Watson AI Lab · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>普通线性注意力写入的二维状态；Triadic 再加入第二 key，写入，读取时用收缩两个 key 轴。第二 key 维度为时，状态容量乘以，只新增两组 projection；严格退化为普通线性注意力。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 递推机制。复现级别：L1 递推机制。实现论文 Eq. (2)–(3) 的写入、双 query 收缩和按第二 key 轴衰减。triadic_linear_attention 是透明的 recurrent reference，测试对照显式求和、检查因果性、退化与梯度；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现论文 Triton chunkwise kernel、Gated DeltaNet upcycling 或长书语言建模，不能把小张量一致性当成论文效果复现。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36529">原论文</a> · <a href="../../../../foundation-models/2609.36529-triadic-linear-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Fractional State Space Transition for Long Sequence Modeling 基础模型 Huawei Noah&#x27;s Ark Lab, Montreal Research Center 2026-09-28 以对数间隔的有限指数模态逼近分数阶动力学的幂律记忆，在有界递归状态下兼顾长尾记忆和并行训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  状态空间模型 长上下文 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-frac-ssm-9d35422b">Fractional State Space Transition for Long Sequence Modeling</h2>
<p class="ar-learning-card__meta">Huawei Noah&#x27;s Ark Lab, Montreal Research Center · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>以对数间隔的有限指数模态逼近分数阶动力学的幂律记忆，在有界递归状态下兼顾长尾记忆和并行训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36314">原论文</a> · <a href="../../../../foundation-models/2609.36314-frac-ssm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution 基础模型 International Institute of Information Technology Hyderabad 2026-09-28 单一时间分辨率的线性注意力容易形成表征瓶颈。MS-GLA 把 head budget 分配给多个尺度：先做无重叠 masked average pooling，再分别执行 GLA，最后以因果 hold 方式恢复到 token 分辨率，并由输入相关 softmax 路由融合。 未复现论文的 Flash kernel 和等参数训练。复现级别：L1 架构机制 + 真实 A100 前后向。复现级别：L1 架构机制 + 真实 A100 前后向。保留多尺度分解、因果 hold 对齐与输入相关融合；未复现论文的 Flash kernel 和等参数训练。当前 recurrent kernel 面向正确性而非吞吐，没有复刻 Triton/Flash 实现或论文参数规模。尚未接入 Evolve，避免把结构名登记误称为已可搜索与公平评价。MultiScaleGLA 是可前后向的紧凑 PyTorch 层；A100 receipt 只证明 CUDA 路径可运行。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-ms-gla-a1875a93">MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution</h2>
<p class="ar-learning-card__meta">International Institute of Information Technology Hyderabad · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>单一时间分辨率的线性注意力容易形成表征瓶颈。MS-GLA 把 head budget 分配给多个尺度：先做无重叠 masked average pooling，再分别执行 GLA，最后以因果 hold 方式恢复到 token 分辨率，并由输入相关 softmax 路由融合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未复现论文的 Flash kernel 和等参数训练。复现级别：L1 架构机制 + 真实 A100 前后向。复现级别：L1 架构机制 + 真实 A100 前后向。保留多尺度分解、因果 hold 对齐与输入相关融合；未复现论文的 Flash kernel 和等参数训练。当前 recurrent kernel 面向正确性而非吞吐，没有复刻 Triton/Flash 实现或论文参数规模。尚未接入 Evolve，避免把结构名登记误称为已可搜索与公平评价。MultiScaleGLA 是可前后向的紧凑 PyTorch 层；A100 receipt 只证明 CUDA 路径可运行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35664">原论文</a> · <a href="../../../../foundation-models/2609.35664-ms-gla/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall 基础模型 Southern University of Science and Technology 2026-09-17 默认只读局部 KV，由轻量 recall head 在全局注意力发生前预测其收益；仅高收益 token 触发全局读取，完整 KV 仍保留。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。  注意力与长上下文 推理效率 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-oda-5fd8c6ed">On-Demand Attention: Efficient Long-Context Decoding with Learned Recall</h2>
<p class="ar-learning-card__meta">Southern University of Science and Technology · 论文公开：2026-09-17</p>
<p><strong>方法要点：</strong>默认只读局部 KV，由轻量 recall head 在全局注意力发生前预测其收益；仅高收益 token 触发全局读取，完整 KV 仍保留。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20734">原论文</a> · <a href="../../../../foundation-models/2609.20734-oda/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking 基础模型 Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST 2026-09-11 硬 Top-K 只能改变被选中的索引，语言模型损失无法沿离散索引直接训练 selector。SAS 不再蒸馏 dense attention：selector 先给历史块连续打分，训练时保留 Top-K 块的连续 gate，并把 log(gate) 加到注意力 logits 内。这样最终 token prediction loss 可直接优化“哪些上下文真正影响预测”。历史块 gate 共同 softmax 归一化，当前块始终使用单位 gate，避免历史上下文整体权重漂移。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地真实训练冻结主干后的 selector，执行 softmax 归一化 gate、历史块 Top-K、当前块常驻和 attention softmax 内的 log-gate；不把 PyTorch 参考实现宣称为 Triton 加速实现。本地实现物化稠密注意力矩阵，仅用于验证论文的选择与梯度机制；没有复刻 Qwen3-4B/8B/14B、OLMo3-7B、OpenR1-Math-220k、LongBench、BFCL、VitaBench，也没有接入原文 Triton/FlashAttention kernel 和 SGLang benchmark。  sparse-attention long-context post-training context-ranking 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-sas-attention-90d42e99">SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking</h2>
<p class="ar-learning-card__meta">Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST · 论文公开：2026-09-11</p>
<p><strong>方法要点：</strong>硬 Top-K 只能改变被选中的索引，语言模型损失无法沿离散索引直接训练 selector。SAS 不再蒸馏 dense attention：selector 先给历史块连续打分，训练时保留 Top-K 块的连续 gate，并把 log(gate) 加到注意力 logits 内。这样最终 token prediction loss 可直接优化“哪些上下文真正影响预测”。历史块 gate 共同 softmax 归一化，当前块始终使用单位 gate，避免历史上下文整体权重漂移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地真实训练冻结主干后的 selector，执行 softmax 归一化 gate、历史块 Top-K、当前块常驻和 attention softmax 内的 log-gate；不把 PyTorch 参考实现宣称为 Triton 加速实现。本地实现物化稠密注意力矩阵，仅用于验证论文的选择与梯度机制；没有复刻 Qwen3-4B/8B/14B、OLMo3-7B、OpenR1-Math-220k、LongBench、BFCL、VitaBench，也没有接入原文 Triton/FlashAttention kernel 和 SGLang benchmark。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13141">原论文</a> · <a href="../../../../reproductions/2609.13141-sas-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension 基础模型 Ai2 2026-08-10 以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 olmpool-long-context；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 网络架构 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-olmpool-long-context-26415a28">Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension</h2>
<p class="ar-learning-card__meta">Ai2 · 论文公开：2026-08-10</p>
<p><strong>方法要点：</strong>以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 olmpool-long-context；单 seed 变化为 +92.19% 个百分点。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10296">原论文</a> · <a href="../../../../reproductions/2608.10296-olmpool-long-context/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry 基础模型 Institute of Computing Technology, Chinese Academy of Sciences 2026-08-07 直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 autonomy-heads；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-autonomy-heads-2d7238b5">Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry</h2>
<p class="ar-learning-card__meta">Institute of Computing Technology, Chinese Academy of Sciences · 论文公开：2026-08-07</p>
<p><strong>方法要点：</strong>直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 autonomy-heads；单 seed 变化为 +92.19% 个百分点。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06849">原论文</a> · <a href="../../../../reproductions/2608.06849-autonomy-heads/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling 基础模型 Zhejiang University 2026-08-03 保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 dart；单 seed 变化为 +3.12% 个百分点。  网络架构 注意力与长上下文 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-dart-ebf1e36e">DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 dart；单 seed 变化为 +3.12% 个百分点。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02032">原论文</a> · <a href="../../../../reproductions/2608.02032-dart/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Learning What to Remember: Test-Time Training via Context Distillation 基础模型 Princeton University 2026-08-03 长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 ttcd；单 seed 变化为 +78.12% 个百分点。  注意力与长上下文 测试时训练 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-ttcd-fe56ef12">Learning What to Remember: Test-Time Training via Context Distillation</h2>
<p class="ar-learning-card__meta">Princeton University · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 ttcd；单 seed 变化为 +78.12% 个百分点。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01672">原论文</a> · <a href="../../../../reproductions/2608.01672-ttcd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="TransMem: Transforming Hidden States into Memory for Large Language Models 基础模型 Authors did not disclose affiliation 2026-07-31 将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 transmem；单 seed 变化为 +12.50% 个百分点。  注意力与长上下文 Agent 记忆 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-transmem-2625c67f">TransMem: Transforming Hidden States into Memory for Large Language Models</h2>
<p class="ar-learning-card__meta">Authors did not disclose affiliation · 论文公开：2026-07-31</p>
<p><strong>方法要点：</strong>将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 transmem；单 seed 变化为 +12.50% 个百分点。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29032">原论文</a> · <a href="../../../../reproductions/2607.29032-transmem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection 基础模型 Pennsylvania State University 2026-07-23 固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。50% heads 只看 local、25% 只看 literal long-range、25% 使用两者并集。 Fidelity: 核心机制复现。真实逐块执行 gzip、生成样本自适应 mask 并训练同参数 ByteLM；缩小 context、模型和训练步数。本地实现确实逐样本调用 gzip 并执行三类 head mask，但 PyTorch 仍计算 dense score matrix 后 masking，所以 edge 数下降不等于 wall-clock 加速。没有下载 28,602 本 PG-19、训练 92M 模型或使用 8K context；小预算负结果不能反驳论文的长上下文训练结论。  llm sparse-attention long-context compression 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-gzip-sparse-attention-4236c23c">Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection</h2>
<p class="ar-learning-card__meta">Pennsylvania State University · 论文公开：2026-07-23</p>
<p><strong>方法要点：</strong>固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。50% heads 只看 local、25% 只看 literal long-range、25% 使用两者并集。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。真实逐块执行 gzip、生成样本自适应 mask 并训练同参数 ByteLM；缩小 context、模型和训练步数。本地实现确实逐样本调用 gzip 并执行三类 head mask，但 PyTorch 仍计算 dense score matrix 后 masking，所以 edge 数下降不等于 wall-clock 加速。没有下载 28,602 本 PG-19、训练 92M 模型或使用 8K context；小预算负结果不能反驳论文的长上下文训练结论。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21752">原论文</a> · <a href="../../../../reproductions/2607.21752-gzip-sparse-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable 基础模型 Independent researcher 2026-07-23 标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为；其余 heads 保留标准 RoPE，以维持语言建模能力。 未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；Fidelity: 核心机制复现。真实训练 standard RoPE 与 25% heads Möbius RoPE；缩小模型、语料和随机种子规模。未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；本地 needle task 是可审计的机制验证，且两组都接受相同 retrieval curriculum。本地对照口径：基线为 standard RoPE；  llm-architecture positional-encoding long-context 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-mobius-rope-d829e106">Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable</h2>
<p class="ar-learning-card__meta">Independent researcher · 论文公开：2026-07-23</p>
<p><strong>方法要点：</strong>标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为；其余 heads 保留标准 RoPE，以维持语言建模能力。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；Fidelity: 核心机制复现。真实训练 standard RoPE 与 25% heads Möbius RoPE；缩小模型、语料和随机种子规模。未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；本地 needle task 是可审计的机制验证，且两组都接受相同 retrieval curriculum。本地对照口径：基线为 standard RoPE；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21405">原论文</a> · <a href="../../../../reproductions/2607.21405-mobius-rope/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory 基础模型 Independent researchers 2026-07-23 Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent 方向、短程因果卷积、直接 feedthrough 与输出调制。 Fidelity: 核心机制复现。真实执行 native-discrete selective recurrence 的完整 block；缩小模型与预训练预算。Python sequential recurrence 与论文 affine scan 数学等价，但没有作者 fused parallel kernel。未复跑 1.2B-token WikiText-103、Mamba/Mamba-2/xLSTM 和完整 LRA/MQAR；本地负结果只适用于当前规模。本地对照口径：基线为同 token、optimizer、70 steps 的 96-d、3-layer Transformer；  llm-architecture state-space-model long-context 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-naju-616fb3d6">Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory</h2>
<p class="ar-learning-card__meta">Independent researchers · 论文公开：2026-07-23</p>
<p><strong>方法要点：</strong>Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent 方向、短程因果卷积、直接 feedthrough 与输出调制。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。真实执行 native-discrete selective recurrence 的完整 block；缩小模型与预训练预算。Python sequential recurrence 与论文 affine scan 数学等价，但没有作者 fused parallel kernel。未复跑 1.2B-token WikiText-103、Mamba/Mamba-2/xLSTM 和完整 LRA/MQAR；本地负结果只适用于当前规模。本地对照口径：基线为同 token、optimizer、70 steps 的 96-d、3-layer Transformer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21000">原论文</a> · <a href="../../../../reproductions/2607.21000-naju/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Convolution for Large Language Models 基础模型 Huawei / Peking University / Tsinghua University 2026-07-20 自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 kernel=3 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 0.01%。 未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；Fidelity: 核心机制复现。真实预训练同预算 Transformer 与 post-QKV residual depthwise Conv1D；缩小模型和语料规模。未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；本地结论只支持小模型短预算下的方向性收益。本地对照口径：基线是相同 96-d、3-layer、60-step Transformer；实验组仅增加 QKV 后残差 depthwise Conv1D，test perplexity 相对降低 0.29%。  llm-architecture attention depthwise-convolution 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-conv-llm-13d560f4">Convolution for Large Language Models</h2>
<p class="ar-learning-card__meta">Huawei / Peking University / Tsinghua University · 论文公开：2026-07-20</p>
<p><strong>方法要点：</strong>自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 kernel=3 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 0.01%。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；Fidelity: 核心机制复现。真实预训练同预算 Transformer 与 post-QKV residual depthwise Conv1D；缩小模型和语料规模。未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；本地结论只支持小模型短预算下的方向性收益。本地对照口径：基线是相同 96-d、3-layer、60-step Transformer；实验组仅增加 QKV 后残差 depthwise Conv1D，test perplexity 相对降低 0.29%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18413">原论文</a> · <a href="../../../../reproductions/2607.18413-conv-llm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MiniMax Sparse Attention 基础模型 MiniMax 2026-06-11 长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。Index branch、每 GQA 组 top-k block 和精确 sparse attention 均真实训练；109B 预训练与 fused kernel 未复刻。WikiText-2 上训练同初始化/同预算的 tiny dense GQA 与 blockwise MSA，报告 PPL、训练时间和实际 attention pair ratio。  llm sparse-attention gqa long-context 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-minimax-sparse-attention-fdb70645">MiniMax Sparse Attention</h2>
<p class="ar-learning-card__meta">MiniMax · 论文公开：2026-06-11</p>
<p><strong>方法要点：</strong>长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。Index branch、每 GQA 组 top-k block 和精确 sparse attention 均真实训练；109B 预训练与 fused kernel 未复刻。WikiText-2 上训练同初始化/同预算的 tiny dense GQA 与 blockwise MSA，报告 PPL、训练时间和实际 attention pair ratio。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.13392">原论文</a> · <a href="../../../../reproductions/2606.13392-minimax-sparse-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers 基础模型 Peking University / Huawei Technologies 2026-03-27 静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。 Fidelity: 核心机制复现。实现逐 token 动态选择 full/local attention 的可学习 router。本地使用可微 soft router，未复刻论文 STE 硬路由、32K continual pretraining 和 branch-selective fused kernel。本地对照口径：基线是 full-attention tiny Transformer；实验组动态混合 full 与 16-token local attention；30-step perplexity 相对 +0.19%（近似持平但略差）。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-switch-attention-753b5e50">Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers</h2>
<p class="ar-learning-card__meta">Peking University / Huawei Technologies · 论文公开：2026-03-27</p>
<p><strong>方法要点：</strong>静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现逐 token 动态选择 full/local attention 的可学习 router。本地使用可微 soft router，未复刻论文 STE 硬路由、32K continual pretraining 和 branch-selective fused kernel。本地对照口径：基线是 full-attention tiny Transformer；实验组动态混合 full 与 16-token local attention；30-step perplexity 相对 +0.19%（近似持平但略差）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26380">原论文</a> · <a href="../../../../reproductions/2603.26380-switch-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free 基础模型 Qwen / Alibaba 2025-05-10 softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。 未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；Fidelity: 核心机制复现。真实训练论文最优的 head-specific sigmoid gate，并记录门控分布。未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；本地只验证论文最优门控位置的实际训练路径。本地对照口径：基线是同预算 llama_modern；实验组只增加 post-SDPA 逐头 sigmoid gate，WikiText-2 LM loss 5.7471→5.7398，相对 -0.13%，PPL 相对 -0.72%。  llm-architecture attention-gating long-context 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-gated-attention-0685e39f">Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free</h2>
<p class="ar-learning-card__meta">Qwen / Alibaba · 论文公开：2025-05-10</p>
<p><strong>方法要点：</strong>softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；Fidelity: 核心机制复现。真实训练论文最优的 head-specific sigmoid gate，并记录门控分布。未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；本地只验证论文最优门控位置的实际训练路径。本地对照口径：基线是同预算 llama_modern；实验组只增加 post-SDPA 逐头 sigmoid gate，WikiText-2 LM loss 5.7471→5.7398，相对 -0.13%，PPL 相对 -0.72%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.06708">原论文</a> · <a href="../../../../reproductions/2505.06708-gated-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MoBA: Mixture of Block Attention for Long-Context LLMs 基础模型 Moonshot AI 2025-02-18 把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际将历史划分为 8-token blocks，以 query 对 block key centroid 的相似度选择 top-2 causal blocks，再在命中块内执行精确 attention；PyTorch reference 未复刻百万上下文 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 moba；相对 PPL +0.49%。  sparse-attention long-context block-routing 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-moba-f8997c1b">MoBA: Mixture of Block Attention for Long-Context LLMs</h2>
<p class="ar-learning-card__meta">Moonshot AI · 论文公开：2025-02-18</p>
<p><strong>方法要点：</strong>把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际将历史划分为 8-token blocks，以 query 对 block key centroid 的相似度选择 top-2 causal blocks，再在命中块内执行精确 attention；PyTorch reference 未复刻百万上下文 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 moba；相对 PPL +0.49%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13189">原论文</a> · <a href="../../../../reproductions/2502.13189-moba/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention 基础模型 DeepSeek 2025-02-16 全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。 未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；Fidelity: 核心机制复现。真实训练压缩、选择和滑窗三条注意力分支；未复刻论文的 Triton kernel 与 27B 训练。未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；结果只支持“核心三路算子可训练且在当前短预算有效”，不能外推论文的规模或速度结论。本地对照口径：基线是同维度、层数、token、AdamW 和 30-step 预算的 llama_modern；  llm-architecture sparse-attention long-context 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-native-sparse-attention-6720d24e">Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention</h2>
<p class="ar-learning-card__meta">DeepSeek · 论文公开：2025-02-16</p>
<p><strong>方法要点：</strong>全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；Fidelity: 核心机制复现。真实训练压缩、选择和滑窗三条注意力分支；未复刻论文的 Triton kernel 与 27B 训练。未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；结果只支持“核心三路算子可训练且在当前短预算有效”，不能外推论文的规模或速度结论。本地对照口径：基线是同维度、层数、token、AdamW 和 30-step 预算的 llama_modern；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.11089">原论文</a> · <a href="../../../../reproductions/2502.11089-native-sparse-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Hymba: A Hybrid-head Architecture for Small Language Models 基础模型 NVIDIA 2024-11-20 同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在每层并行执行 causal attention 与深度卷积状态分支，并以输入相关 gate 融合；未复刻 1.5B 参数、meta tokens 和 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 hymba；相对 PPL +8.53%。  hybrid-attention-ssm small-language-model architecture 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-hymba-2cf1482a">Hymba: A Hybrid-head Architecture for Small Language Models</h2>
<p class="ar-learning-card__meta">NVIDIA · 论文公开：2024-11-20</p>
<p><strong>方法要点：</strong>同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在每层并行执行 causal attention 与深度卷积状态分支，并以输入相关 gate 融合；未复刻 1.5B 参数、meta tokens 和 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 hymba；相对 PPL +8.53%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13676">原论文</a> · <a href="../../../../reproductions/2411.13676-hymba/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Mamba: Linear-Time Sequence Modeling with Selective State Spaces 基础模型 Carnegie Mellon University / Princeton University 2023-12-01 Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。 Fidelity: 核心机制复现。实现输入相关的 selective SSM、因果 depthwise convolution 与门控输出。未使用 fused parallel scan CUDA kernel，也没有 2.8B 规模预训练；短预算结果不代表论文规模结论。本地对照口径：基线是 tiny Transformer；实验组是原生 PyTorch selective scan；WikiText-2 30-step perplexity 相对 +48.82%（变差）。  llm-architecture state-space-model classic 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-mamba-0b65990c">Mamba: Linear-Time Sequence Modeling with Selective State Spaces</h2>
<p class="ar-learning-card__meta">Carnegie Mellon University / Princeton University · 论文公开：2023-12-01</p>
<p><strong>方法要点：</strong>Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现输入相关的 selective SSM、因果 depthwise convolution 与门控输出。未使用 fused parallel scan CUDA kernel，也没有 2.8B 规模预训练；短预算结果不代表论文规模结论。本地对照口径：基线是 tiny Transformer；实验组是原生 PyTorch selective scan；WikiText-2 30-step perplexity 相对 +48.82%（变差）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.00752">原论文</a> · <a href="../../../../reproductions/2312.00752-mamba/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation 基础模型 University of Washington / Meta AI 2021-08-27 不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际移除位置 embedding，并对各 attention head 加不同斜率的因果距离线性 bias；WikiText-2 小模型未复跑论文 WikiText-103 1.3B 参数实验。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 alibi；相对 PPL +0.06%。  position-encoding length-extrapolation attention 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-alibi-69e595a8">Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation</h2>
<p class="ar-learning-card__meta">University of Washington / Meta AI · 论文公开：2021-08-27</p>
<p><strong>方法要点：</strong>不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际移除位置 embedding，并对各 attention head 加不同斜率的因果距离线性 bias；WikiText-2 小模型未复跑论文 WikiText-103 1.3B 参数实验。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 alibi；相对 PPL +0.06%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2108.12409">原论文</a> · <a href="../../../../reproductions/2108.12409-alibi/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="RoFormer: Enhanced Transformer with Rotary Position Embedding 基础模型 Zhuiyi Technology 2021-04-20 对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际对每个注意力 head 的 Q/K 执行复数平面旋转并由相对相位进入 dot product；WikiText-2 64d 小模型替代论文中文 RoFormer 预训练。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 rope；相对 PPL +0.00%。  position-encoding long-context architecture 基础模型 长上下文：注意力、递归状态与记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<h2 id="paper-foundation-models-rope-baa4b020">RoFormer: Enhanced Transformer with Rotary Position Embedding</h2>
<p class="ar-learning-card__meta">Zhuiyi Technology · 论文公开：2021-04-20</p>
<p><strong>方法要点：</strong>对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际对每个注意力 head 的 Q/K 执行复数平面旋转并由相对相位进入 dot product；WikiText-2 64d 小模型替代论文中文 RoFormer 预训练。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 rope；相对 PPL +0.00%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2104.09864">原论文</a> · <a href="../../../../reproductions/2104.09864-rope/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
