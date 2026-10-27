---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 视觉证据预算：选 Token、选帧与按需回看

[多模态](index.md) / 64 个问题 · 16 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<div class="ar-learning-levels" role="group" aria-label="学习层次">
<span>学习层次</span>
<button type="button" data-learning-level="" aria-pressed="true">全部</button>
<button type="button" data-learning-level="basics" aria-pressed="false">基础理解</button>
<button type="button" data-learning-level="mechanism" aria-pressed="false">核心机制</button>
<button type="button" data-learning-level="comparison" aria-pressed="false">方法对比</button>
<button type="button" data-learning-level="implementation" aria-pressed="false">实现细节</button>
</div>
<p class="ar-learning-status" data-learning-status role="status">64 个问题 · 16 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muse-glimmer-30b" data-paper-title="Muse Glimmer 30B: An On-Device Agentic Model" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Muse Glimmer 30B: An On-Device Agentic Model 基础模型 Meta Superintelligence Labs 2026-10-17 模型瞄准有32GB专用内存的端侧Agent：语言骨干用稠密Transformer而非MoE，在相同内存预算下用缩放实验选架构；约1.8B冻结视觉编码器支持图文交错输入。52层采用三层2048窗口局部注意力接一层全局注意力，32Q/2KV的GQA，局部层使用RoPE，全局层不再施加RoPE。训练从Muse Spark logits蒸馏起步，预训练末段切CE处理top-k截断偏差，之后权重平均和两阶段mid-training，再SFT、学生前缀上的OPD与多目标RL。 成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；“单卡可装下”不等于本项目低成本可完成训练和完整评测。BF16权重约55.7GB，量化LM目标低于20GB仍需KV、视觉编码器和drafter空间；长Agent轨迹与多模型对照远非一次前向。完整过程依赖前沿教师、多阶段大规模蒸馏、128K上下文与多域Agent环境，成本过高，不复现（审查 DONE）。本轮只取论文与仓库元数据，不下载权重、不开长推理或训练，不提供本地能力分数、GPU回执或Evolve整合声明。  网络架构 端侧多模态Agent模型 多模态 视觉证据预算：选 Token、选帧与按需回看 Muse Glimmer 为什么同时强调模型权重内存和 KV、视觉、drafter 空间？ 端侧可用内存要容纳整个推理过程，而不只是语言权重。长 Agent 上下文会增加 KV cache，图像编码器与投机头也有占用，因此量化语言模型后小于某个体积不等于系统已适合 32GB 设备；必须按实际输入与部署配置联合核算。 例如语言权重低于二十 GB，仍可能因长轨迹 KV 和视觉前向的临时张量超过设备剩余空间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-muse-glimmer-30b-d492f01f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c695941cc5721c5a">Muse Glimmer 为什么同时强调模型权重内存和 KV、视觉、drafter 空间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuse-glimmer-30b">Muse Glimmer 30B: An On-Device Agentic Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>端侧可用内存要容纳整个推理过程，而不只是语言权重。长 Agent 上下文会增加 KV cache，图像编码器与投机头也有占用，因此量化语言模型后小于某个体积不等于系统已适合 32GB 设备；必须按实际输入与部署配置联合核算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如语言权重低于二十 GB，仍可能因长轨迹 KV 和视觉前向的临时张量超过设备剩余空间。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与结构；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24628v1">原论文</a> · <a href="../../../../foundation-models/2610.24628-muse-glimmer-30b/">实现解读</a> · <a href="#qa-c695941cc5721c5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muse-glimmer-30b" data-paper-title="Muse Glimmer 30B: An On-Device Agentic Model" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Muse Glimmer 30B: An On-Device Agentic Model 基础模型 Meta Superintelligence Labs 2026-10-17 模型瞄准有32GB专用内存的端侧Agent：语言骨干用稠密Transformer而非MoE，在相同内存预算下用缩放实验选架构；约1.8B冻结视觉编码器支持图文交错输入。52层采用三层2048窗口局部注意力接一层全局注意力，32Q/2KV的GQA，局部层使用RoPE，全局层不再施加RoPE。训练从Muse Spark logits蒸馏起步，预训练末段切CE处理top-k截断偏差，之后权重平均和两阶段mid-training，再SFT、学生前缀上的OPD与多目标RL。 成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；“单卡可装下”不等于本项目低成本可完成训练和完整评测。BF16权重约55.7GB，量化LM目标低于20GB仍需KV、视觉编码器和drafter空间；长Agent轨迹与多模型对照远非一次前向。完整过程依赖前沿教师、多阶段大规模蒸馏、128K上下文与多域Agent环境，成本过高，不复现（审查 DONE）。本轮只取论文与仓库元数据，不下载权重、不开长推理或训练，不提供本地能力分数、GPU回执或Evolve整合声明。  网络架构 端侧多模态Agent模型 多模态 视觉证据预算：选 Token、选帧与按需回看 三层局部注意力接一层全局注意力，为什么不同于把整个模型窗口都缩短？ 局部层限制多数层的读写范围以节省成本，全局层仍能在更长范围交换信息，因此模型并非每层都永久看不到远处内容。GQA 又减少 KV 头数，针对另一部分缓存成本；这些结构取舍不等于已经复现整套蒸馏、后训练和端侧运行效果。 例如远处的标题可在全局层影响当前段落，而相邻句子的加工由局部层承担；全部改成短窗口会失去这条长程通路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1e53a66d94151563">三层局部注意力接一层全局注意力，为什么不同于把整个模型窗口都缩短？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuse-glimmer-30b">Muse Glimmer 30B: An On-Device Agentic Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部层限制多数层的读写范围以节省成本，全局层仍能在更长范围交换信息，因此模型并非每层都永久看不到远处内容。GQA 又减少 KV 头数，针对另一部分缓存成本；这些结构取舍不等于已经复现整套蒸馏、后训练和端侧运行效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如远处的标题可在全局层影响当前段落，而相邻句子的加工由局部层承担；全部改成短窗口会失去这条长程通路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与结构；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24628v1">原论文</a> · <a href="../../../../foundation-models/2610.24628-muse-glimmer-30b/">实现解读</a> · <a href="#qa-1e53a66d94151563">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muse-glimmer-30b" data-paper-title="Muse Glimmer 30B: An On-Device Agentic Model" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Muse Glimmer 30B: An On-Device Agentic Model 基础模型 Meta Superintelligence Labs 2026-10-17 模型瞄准有32GB专用内存的端侧Agent：语言骨干用稠密Transformer而非MoE，在相同内存预算下用缩放实验选架构；约1.8B冻结视觉编码器支持图文交错输入。52层采用三层2048窗口局部注意力接一层全局注意力，32Q/2KV的GQA，局部层使用RoPE，全局层不再施加RoPE。训练从Muse Spark logits蒸馏起步，预训练末段切CE处理top-k截断偏差，之后权重平均和两阶段mid-training，再SFT、学生前缀上的OPD与多目标RL。 成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；“单卡可装下”不等于本项目低成本可完成训练和完整评测。BF16权重约55.7GB，量化LM目标低于20GB仍需KV、视觉编码器和drafter空间；长Agent轨迹与多模型对照远非一次前向。完整过程依赖前沿教师、多阶段大规模蒸馏、128K上下文与多域Agent环境，成本过高，不复现（审查 DONE）。本轮只取论文与仓库元数据，不下载权重、不开长推理或训练，不提供本地能力分数、GPU回执或Evolve整合声明。  网络架构 端侧多模态Agent模型 多模态 视觉证据预算：选 Token、选帧与按需回看 三局部一全局注意力与全部全局层有何结构取舍？ 局部层在 2048 窗口内处理上下文，全局层周期性连接远处信息，以减少长上下文每层全局注意力的开销。它以传播路径和计算范围换成本，不代表远距关系与全局模型完全相同；还需与 GQA、量化及训练一起评估。 例如两条相隔很远的事件不会在每个局部层直接交互，需要经过周期性的全局层连接；这与全层全局访问不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-228de77c3730310a">三局部一全局注意力与全部全局层有何结构取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuse-glimmer-30b">Muse Glimmer 30B: An On-Device Agentic Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部层在 2048 窗口内处理上下文，全局层周期性连接远处信息，以减少长上下文每层全局注意力的开销。它以传播路径和计算范围换成本，不代表远距关系与全局模型完全相同；还需与 GQA、量化及训练一起评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条相隔很远的事件不会在每个局部层直接交互，需要经过周期性的全局层连接；这与全层全局访问不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与结构；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24628v1">原论文</a> · <a href="../../../../foundation-models/2610.24628-muse-glimmer-30b/">实现解读</a> · <a href="#qa-228de77c3730310a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muse-glimmer-30b" data-paper-title="Muse Glimmer 30B: An On-Device Agentic Model" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Muse Glimmer 30B: An On-Device Agentic Model 基础模型 Meta Superintelligence Labs 2026-10-17 模型瞄准有32GB专用内存的端侧Agent：语言骨干用稠密Transformer而非MoE，在相同内存预算下用缩放实验选架构；约1.8B冻结视觉编码器支持图文交错输入。52层采用三层2048窗口局部注意力接一层全局注意力，32Q/2KV的GQA，局部层使用RoPE，全局层不再施加RoPE。训练从Muse Spark logits蒸馏起步，预训练末段切CE处理top-k截断偏差，之后权重平均和两阶段mid-training，再SFT、学生前缀上的OPD与多目标RL。 成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；“单卡可装下”不等于本项目低成本可完成训练和完整评测。BF16权重约55.7GB，量化LM目标低于20GB仍需KV、视觉编码器和drafter空间；长Agent轨迹与多模型对照远非一次前向。完整过程依赖前沿教师、多阶段大规模蒸馏、128K上下文与多域Agent环境，成本过高，不复现（审查 DONE）。本轮只取论文与仓库元数据，不下载权重、不开长推理或训练，不提供本地能力分数、GPU回执或Evolve整合声明。  网络架构 端侧多模态Agent模型 多模态 视觉证据预算：选 Token、选帧与按需回看 52 层的注意力和 RoPE 配置能按一个统一全局模板实现吗？ 不能。配置是 [Local,Local,Local,Global] 重复十三次，32 个 query 头对应 2 个 KV 头；局部层使用 RoPE，全局层不再施加 RoPE。视觉分支另用 2×2 压缩把 1024 patch 变成 256 token，单层演示不等于完整 29.6B 模型。 例如把所有层都加 RoPE，或把三局部一全局误作交替局部全局，都会改变论文结构，即使总层数仍是五十二。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-79ddf2ee2885b4c8">52 层的注意力和 RoPE 配置能按一个统一全局模板实现吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuse-glimmer-30b">Muse Glimmer 30B: An On-Device Agentic Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。配置是 [Local,Local,Local,Global] 重复十三次，32 个 query 头对应 2 个 KV 头；局部层使用 RoPE，全局层不再施加 RoPE。视觉分支另用 2×2 压缩把 1024 patch 变成 256 token，单层演示不等于完整 29.6B 模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把所有层都加 RoPE，或把三局部一全局误作交替局部全局，都会改变论文结构，即使总层数仍是五十二。</p>
<p class="ar-learning-sources">依据：核心公式与结构、本地复现与成本判断；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24628v1">原论文</a> · <a href="../../../../foundation-models/2610.24628-muse-glimmer-30b/">实现解读</a> · <a href="#qa-79ddf2ee2885b4c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sink-sparse" data-paper-title="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers 基础模型 Xi&#x27;an Jiaotong University 2026-10-16 扩散Transformer在每个去噪步重复执行昂贵的attention。本文观察到某些层/头中的高概率block关系在不同提示和seed下较稳定，因此一次离线校准即可得到静态稀疏支持；另用低分辨率全局KV分支补回分散上下文，无需改权重或采样schedule。原文Figure 4是两阶段方法总览，见Section4。 成本过高，不复现（审查 DONE）。不下载视频checkpoint，不跑完整生成或宣称端到端加速，禁止Evolve基于本诊断晋级。本地执行真实精确概率质量校准、最短前缀、静态mask复用、选中block实际gather计算、全局均值池化及稳定sigmoid融合。Python循环仅用于正确性，不是FlashAttention/Triton生产kernel，不以稀疏比例换算实测加速。  推理与系统效率 扩散模型稀疏注意力 多模态 视觉证据预算：选 Token、选帧与按需回看 静态 sink mask 是从新提示在线挑出的高分块吗？ 不是。它由独立离线校准的 dense 注意力概率，先聚合精确 block mass，再逐行取达到质量阈值的最短前缀；新输入复用该 mask。静态性降低在线选择开销，也依赖模式能跨提示和 seed 稳定，不能测试时重新挑 mask 后仍称离线复用。 例如校准时某 query block 总关注两个区域，部署固定读取它们；新提示出现另一高分区域时，不会偷偷重选静态 mask。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-sink-sparse-7f23b46b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-89e77ff6c5528806">静态 sink mask 是从新提示在线挑出的高分块吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asink-sparse">Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xi&#x27;an Jiaotong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它由独立离线校准的 dense 注意力概率，先聚合精确 block mass，再逐行取达到质量阈值的最短前缀；新输入复用该 mask。静态性降低在线选择开销，也依赖模式能跨提示和 seed 稳定，不能测试时重新挑 mask 后仍称离线复用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如校准时某 query block 总关注两个区域，部署固定读取它们；新提示出现另一高分区域时，不会偷偷重选静态 mask。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22975">原论文</a> · <a href="../../../../foundation-models/2610.22975-sink-sparse/">实现解读</a> · <a href="#qa-89e77ff6c5528806">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sink-sparse" data-paper-title="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers 基础模型 Xi&#x27;an Jiaotong University 2026-10-16 扩散Transformer在每个去噪步重复执行昂贵的attention。本文观察到某些层/头中的高概率block关系在不同提示和seed下较稳定，因此一次离线校准即可得到静态稀疏支持；另用低分辨率全局KV分支补回分散上下文，无需改权重或采样schedule。原文Figure 4是两阶段方法总览，见Section4。 成本过高，不复现（审查 DONE）。不下载视频checkpoint，不跑完整生成或宣称端到端加速，禁止Evolve基于本诊断晋级。本地执行真实精确概率质量校准、最短前缀、静态mask复用、选中block实际gather计算、全局均值池化及稳定sigmoid融合。Python循环仅用于正确性，不是FlashAttention/Triton生产kernel，不以稀疏比例换算实测加速。  推理与系统效率 扩散模型稀疏注意力 多模态 视觉证据预算：选 Token、选帧与按需回看 全局补偿分支为什么连 sink 块也池化，而不是只处理被稀疏分支漏掉的块？ 补偿分支提供低分辨率的全局背景，其定义覆盖全部 token；稀疏分支则保留选中关系的精细计算。两者按各自归一化量融合，不是把遗漏部分简单相加。若擅自排除 sink，就改变了补偿分布，离线校准得到的静态支持也不能在测试题上重新挑选。 例如稀疏分支精读中心区域，全局分支仍粗读整张图包括中心；它补的是全局上下文，不是把剩余区域拼成第二张图。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fa3282e27f8322fe">全局补偿分支为什么连 sink 块也池化，而不是只处理被稀疏分支漏掉的块？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asink-sparse">Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xi&#x27;an Jiaotong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>补偿分支提供低分辨率的全局背景，其定义覆盖全部 token；稀疏分支则保留选中关系的精细计算。两者按各自归一化量融合，不是把遗漏部分简单相加。若擅自排除 sink，就改变了补偿分布，离线校准得到的静态支持也不能在测试题上重新挑选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如稀疏分支精读中心区域，全局分支仍粗读整张图包括中心；它补的是全局上下文，不是把剩余区域拼成第二张图。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22975">原论文</a> · <a href="../../../../foundation-models/2610.22975-sink-sparse/">实现解读</a> · <a href="#qa-fa3282e27f8322fe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sink-sparse" data-paper-title="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers 基础模型 Xi&#x27;an Jiaotong University 2026-10-16 扩散Transformer在每个去噪步重复执行昂贵的attention。本文观察到某些层/头中的高概率block关系在不同提示和seed下较稳定，因此一次离线校准即可得到静态稀疏支持；另用低分辨率全局KV分支补回分散上下文，无需改权重或采样schedule。原文Figure 4是两阶段方法总览，见Section4。 成本过高，不复现（审查 DONE）。不下载视频checkpoint，不跑完整生成或宣称端到端加速，禁止Evolve基于本诊断晋级。本地执行真实精确概率质量校准、最短前缀、静态mask复用、选中block实际gather计算、全局均值池化及稳定sigmoid融合。Python循环仅用于正确性，不是FlashAttention/Triton生产kernel，不以稀疏比例换算实测加速。  推理与系统效率 扩散模型稀疏注意力 多模态 视觉证据预算：选 Token、选帧与按需回看 为什么补偿分支不能只池化未选中 token，或简单与稀疏输出平均？ 论文补偿分支池化全部 KV，包括 sink 块，两分支支持存在重叠；融合依据各自行 log-normalizer 并加入池化倍率修正。只池化遗漏部分改变支持定义，固定平均则忽略概率质量，因此都不是同一混合注意力。 例如稀疏分支占大部分归一化质量时，其权重应更高；固定各一半会让较弱补偿分支获得过大影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d518dd72ce9680f3">为什么补偿分支不能只池化未选中 token，或简单与稀疏输出平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asink-sparse">Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xi&#x27;an Jiaotong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>论文补偿分支池化全部 KV，包括 sink 块，两分支支持存在重叠；融合依据各自行 log-normalizer 并加入池化倍率修正。只池化遗漏部分改变支持定义，固定平均则忽略概率质量，因此都不是同一混合注意力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如稀疏分支占大部分归一化质量时，其权重应更高；固定各一半会让较弱补偿分支获得过大影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22975">原论文</a> · <a href="../../../../foundation-models/2610.22975-sink-sparse/">实现解读</a> · <a href="#qa-d518dd72ce9680f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sink-sparse" data-paper-title="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers 基础模型 Xi&#x27;an Jiaotong University 2026-10-16 扩散Transformer在每个去噪步重复执行昂贵的attention。本文观察到某些层/头中的高概率block关系在不同提示和seed下较稳定，因此一次离线校准即可得到静态稀疏支持；另用低分辨率全局KV分支补回分散上下文，无需改权重或采样schedule。原文Figure 4是两阶段方法总览，见Section4。 成本过高，不复现（审查 DONE）。不下载视频checkpoint，不跑完整生成或宣称端到端加速，禁止Evolve基于本诊断晋级。本地执行真实精确概率质量校准、最短前缀、静态mask复用、选中block实际gather计算、全局均值池化及稳定sigmoid融合。Python循环仅用于正确性，不是FlashAttention/Triton生产kernel，不以稀疏比例换算实测加速。  推理与系统效率 扩散模型稀疏注意力 多模态 视觉证据预算：选 Token、选帧与按需回看 校准 block mass 能否先平均 Q/K 再做 softmax 近似？ 不能。应先计算 token 级 dense 概率，再按 query block 平均、key block 求和，保证每行质量和为一。softmax 非线性使平均 Q/K 后的结果不同；本地 Python gather 仅作正确性验证，不能用 mask 稀疏比例换算真实 kernel 加速。 例如两个 query 分别关注左右两端，平均 query 可能关注中间；先平均再 softmax 会丢失两端的真实概率质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-366fd7b1d91c36e5">校准 block mass 能否先平均 Q/K 再做 softmax 近似？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asink-sparse">Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xi&#x27;an Jiaotong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。应先计算 token 级 dense 概率，再按 query block 平均、key block 求和，保证每行质量和为一。softmax 非线性使平均 Q/K 后的结果不同；本地 Python gather 仅作正确性验证，不能用 mask 稀疏比例换算真实 kernel 加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个 query 分别关注左右两端，平均 query 可能关注中间；先平均再 softmax 会丢失两端的真实概率质量。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本判断与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22975">原论文</a> · <a href="../../../../foundation-models/2610.22975-sink-sparse/">实现解读</a> · <a href="#qa-366fd7b1d91c36e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adaloop-vision" data-paper-title="AdaLoop: Thinking with the Vision Encoder" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="AdaLoop: Thinking with the Vision Encoder 基础模型 Harvard University 2026-10-15 普通 VLM 对所有问题只编码图像一次。视觉 AdaLoop 保持预训练视觉权重冻结，以问题池化向量调制共享视觉块，再循环更新内部视觉状态。它将“看几次”与问题联系起来，而不是让语言模型独自承担全部推理。 单卡完整多臂成本过高，成本过高，不复现（审查 DONE）。临时线性分类器只供梯度诊断，不替代真实语言模型。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。使用3条随机视觉/问题 token、16维、2层、3次循环；冻结 attention/MLP 与 normalization，只训练问题池化、调制器和 connector。临时线性分类器只供梯度诊断，不替代真实语言模型。  多模态基础模型 问题条件视觉循环 多模态 视觉证据预算：选 Token、选帧与按需回看 视觉 AdaLoop 的循环状态和冻结视觉权重有什么区别？ 权重是每次循环共享的变换规则，状态是经过变换后不断更新的视觉表示。模型可保持预训练注意力和 MLP 冻结，同时训练问题池化、调制器与 connector，让同一组视觉块按问题多次处理状态；冻结权重并不意味着表示每轮不变。 例如同一照片问数量和问位置，可以产生不同调制向量；每轮仍调用同一视觉块，但输入状态及关注信息会变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-adaloop-vision-ed1ee6f4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b5b64a38a09f4bf8">视觉 AdaLoop 的循环状态和冻结视觉权重有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadaloop-vision">AdaLoop: Thinking with the Vision Encoder</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harvard University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>权重是每次循环共享的变换规则，状态是经过变换后不断更新的视觉表示。模型可保持预训练注意力和 MLP 冻结，同时训练问题池化、调制器与 connector，让同一组视觉块按问题多次处理状态；冻结权重并不意味着表示每轮不变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一照片问数量和问位置，可以产生不同调制向量；每轮仍调用同一视觉块，但输入状态及关注信息会变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21323">原论文</a> · <a href="../../../../foundation-models/2610.21323-adaloop-vision/">实现解读</a> · <a href="#qa-b5b64a38a09f4bf8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adaloop-vision" data-paper-title="AdaLoop: Thinking with the Vision Encoder" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="AdaLoop: Thinking with the Vision Encoder 基础模型 Harvard University 2026-10-15 普通 VLM 对所有问题只编码图像一次。视觉 AdaLoop 保持预训练视觉权重冻结，以问题池化向量调制共享视觉块，再循环更新内部视觉状态。它将“看几次”与问题联系起来，而不是让语言模型独自承担全部推理。 单卡完整多臂成本过高，成本过高，不复现（审查 DONE）。临时线性分类器只供梯度诊断，不替代真实语言模型。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。使用3条随机视觉/问题 token、16维、2层、3次循环；冻结 attention/MLP 与 normalization，只训练问题池化、调制器和 connector。临时线性分类器只供梯度诊断，不替代真实语言模型。  多模态基础模型 问题条件视觉循环 多模态 视觉证据预算：选 Token、选帧与按需回看 视觉编码器权重被冻结时，反复循环为什么仍可能改变模型看到的内容？ 冻结权重不等于冻结视觉状态。每轮把更新后的状态送回共享块，并由问题向量调制计算，因此同一组参数可以围绕问题逐步重新组织表示。深度监督约束不同循环的答案，停止规则只能比较已产生预测，不能偷偷依赖正确答案。 例如同一幅图先问物体种类、再问遮挡关系，问题调制可让循环关注不同信息；这并非每轮都换一个新编码器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-403999afca57c3bc">视觉编码器权重被冻结时，反复循环为什么仍可能改变模型看到的内容？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadaloop-vision">AdaLoop: Thinking with the Vision Encoder</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harvard University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结权重不等于冻结视觉状态。每轮把更新后的状态送回共享块，并由问题向量调制计算，因此同一组参数可以围绕问题逐步重新组织表示。深度监督约束不同循环的答案，停止规则只能比较已产生预测，不能偷偷依赖正确答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一幅图先问物体种类、再问遮挡关系，问题调制可让循环关注不同信息；这并非每轮都换一个新编码器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21323">原论文</a> · <a href="../../../../foundation-models/2610.21323-adaloop-vision/">实现解读</a> · <a href="#qa-403999afca57c3bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adaloop-vision" data-paper-title="AdaLoop: Thinking with the Vision Encoder" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="AdaLoop: Thinking with the Vision Encoder 基础模型 Harvard University 2026-10-15 普通 VLM 对所有问题只编码图像一次。视觉 AdaLoop 保持预训练视觉权重冻结，以问题池化向量调制共享视觉块，再循环更新内部视觉状态。它将“看几次”与问题联系起来，而不是让语言模型独自承担全部推理。 单卡完整多臂成本过高，成本过高，不复现（审查 DONE）。临时线性分类器只供梯度诊断，不替代真实语言模型。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。使用3条随机视觉/问题 token、16维、2层、3次循环；冻结 attention/MLP 与 normalization，只训练问题池化、调制器和 connector。临时线性分类器只供梯度诊断，不替代真实语言模型。  多模态基础模型 问题条件视觉循环 多模态 视觉证据预算：选 Token、选帧与按需回看 视觉循环与让语言模型多写几段思考，在计算位置上有何不同？ 语言思考主要沿文本序列继续推理，视觉 AdaLoop 则把额外计算放在问题条件化的视觉编码路径，并共享块权重。它让视觉状态随问题更新，但是否优于更多语言 token 需匹配训练与预算比较，不能仅凭循环次数推断视觉推理提高。 例如数遮挡物体时可再次处理视觉状态，而不是只在原有一次编码结果上继续生成文字；两者消耗的计算位置不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-15a64e71d1ec71fe">视觉循环与让语言模型多写几段思考，在计算位置上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadaloop-vision">AdaLoop: Thinking with the Vision Encoder</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harvard University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言思考主要沿文本序列继续推理，视觉 AdaLoop 则把额外计算放在问题条件化的视觉编码路径，并共享块权重。它让视觉状态随问题更新，但是否优于更多语言 token 需匹配训练与预算比较，不能仅凭循环次数推断视觉推理提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数遮挡物体时可再次处理视觉状态，而不是只在原有一次编码结果上继续生成文字；两者消耗的计算位置不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21323">原论文</a> · <a href="../../../../foundation-models/2610.21323-adaloop-vision/">实现解读</a> · <a href="#qa-15a64e71d1ec71fe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adaloop-vision" data-paper-title="AdaLoop: Thinking with the Vision Encoder" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="AdaLoop: Thinking with the Vision Encoder 基础模型 Harvard University 2026-10-15 普通 VLM 对所有问题只编码图像一次。视觉 AdaLoop 保持预训练视觉权重冻结，以问题池化向量调制共享视觉块，再循环更新内部视觉状态。它将“看几次”与问题联系起来，而不是让语言模型独自承担全部推理。 单卡完整多臂成本过高，成本过高，不复现（审查 DONE）。临时线性分类器只供梯度诊断，不替代真实语言模型。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。使用3条随机视觉/问题 token、16维、2层、3次循环；冻结 attention/MLP 与 normalization，只训练问题池化、调制器和 connector。临时线性分类器只供梯度诊断，不替代真实语言模型。  多模态基础模型 问题条件视觉循环 多模态 视觉证据预算：选 Token、选帧与按需回看 答案稳定停止能否用 gold 答案判定当前循环已足够？ 不能。部署停止只比较连续预测答案是否稳定，不能读 gold。训练则对多个深度分别监督，权重为正且总和为一；本地 C 接口还要求外部提供并 detach 草稿 embeddings 和固定 separator，不具备自动生成草稿的完整语言模型。 例如连续两轮都预测“三个”可触发稳定规则，即使真值是“四个”；稳定不是正确性的 oracle。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-acf4971fdf9cd572">答案稳定停止能否用 gold 答案判定当前循环已足够？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadaloop-vision">AdaLoop: Thinking with the Vision Encoder</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harvard University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。部署停止只比较连续预测答案是否稳定，不能读 gold。训练则对多个深度分别监督，权重为正且总和为一；本地 C 接口还要求外部提供并 detach 草稿 embeddings 和固定 separator，不具备自动生成草稿的完整语言模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如连续两轮都预测“三个”可触发稳定规则，即使真值是“四个”；稳定不是正确性的 oracle。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21323">原论文</a> · <a href="../../../../foundation-models/2610.21323-adaloop-vision/">实现解读</a> · <a href="#qa-acf4971fdf9cd572">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rr-vlm" data-paper-title="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones 基础模型 University of Tübingen 2026-10-15 预训练 VLM 的语言层可以剪掉一段，再共享循环保留核心块；但直接手术会破坏语言能力及图文对齐。RR-VLM 用一个线性 adapter 融合 prelude 上下文与循环状态，并依次执行文本恢复、projector 对齐、全模型指令恢复；文本和最终阶段加入原始未剪模型蒸馏。 即使1.4B模型能放入单卡，完整恢复仍过重，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机6层、16维因果 Transformer，连续删除2层，保留1/2/1的 prelude/core/coda，核心循环3次。2条随机文本与视觉特征只检查结构和优化路径，不是模型能力数据。  多模态基础模型 剪枝与循环恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 RR-VLM 的“循环深度”为什么不等于存储层数？ prelude 与 coda 各执行一次，核心块重复执行多轮但共享参数，所以展开深度是 p+rb+c，而不同层参数只存 p+b+c。循环可用较少参数承担更深计算，但每次重复仍有计算和状态成本，参数减少不能直接等价为推理 FLOPs 下降。 例如 prelude 一层、core 两层、coda 一层，循环三次时执行八层变换，却只存四层不同参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-rr-vlm-3b3af466" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e52481933a1636d3">RR-VLM 的“循环深度”为什么不等于存储层数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arr-vlm">Retrofitting Recurrent Vision-Language Models from Pretrained Backbones</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Tübingen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>prelude 与 coda 各执行一次，核心块重复执行多轮但共享参数，所以展开深度是 p+rb+c，而不同层参数只存 p+b+c。循环可用较少参数承担更深计算，但每次重复仍有计算和状态成本，参数减少不能直接等价为推理 FLOPs 下降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 prelude 一层、core 两层、coda 一层，循环三次时执行八层变换，却只存四层不同参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22075">原论文</a> · <a href="../../../../foundation-models/2610.22075-rr-vlm/">实现解读</a> · <a href="#qa-e52481933a1636d3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rr-vlm" data-paper-title="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones 基础模型 University of Tübingen 2026-10-15 预训练 VLM 的语言层可以剪掉一段，再共享循环保留核心块；但直接手术会破坏语言能力及图文对齐。RR-VLM 用一个线性 adapter 融合 prelude 上下文与循环状态，并依次执行文本恢复、projector 对齐、全模型指令恢复；文本和最终阶段加入原始未剪模型蒸馏。 即使1.4B模型能放入单卡，完整恢复仍过重，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机6层、16维因果 Transformer，连续删除2层，保留1/2/1的 prelude/core/coda，核心循环3次。2条随机文本与视觉特征只检查结构和优化路径，不是模型能力数据。  多模态基础模型 剪枝与循环恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 共享循环块为什么能减少存储层数，却不保证减少执行深度？ 同一核心块重复执行多次只保存一份参数，但总计算仍包含每次循环。剪层还会破坏原有语言能力和图文接口，所以需要先恢复文本、再对齐 projector、再做指令恢复；参数变少和推理步数变少是两个不同目标，不能混报为同一种加速。 例如五层核心循环三次相当于执行十五次块计算，却只存五层核心权重；循环次数越多，存储优势未必变成延迟优势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-beec2c2a8e3eaa21">共享循环块为什么能减少存储层数，却不保证减少执行深度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arr-vlm">Retrofitting Recurrent Vision-Language Models from Pretrained Backbones</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Tübingen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一核心块重复执行多次只保存一份参数，但总计算仍包含每次循环。剪层还会破坏原有语言能力和图文接口，所以需要先恢复文本、再对齐 projector、再做指令恢复；参数变少和推理步数变少是两个不同目标，不能混报为同一种加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如五层核心循环三次相当于执行十五次块计算，却只存五层核心权重；循环次数越多，存储优势未必变成延迟优势。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22075">原论文</a> · <a href="../../../../foundation-models/2610.22075-rr-vlm/">实现解读</a> · <a href="#qa-beec2c2a8e3eaa21">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rr-vlm" data-paper-title="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones 基础模型 University of Tübingen 2026-10-15 预训练 VLM 的语言层可以剪掉一段，再共享循环保留核心块；但直接手术会破坏语言能力及图文对齐。RR-VLM 用一个线性 adapter 融合 prelude 上下文与循环状态，并依次执行文本恢复、projector 对齐、全模型指令恢复；文本和最终阶段加入原始未剪模型蒸馏。 即使1.4B模型能放入单卡，完整恢复仍过重，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机6层、16维因果 Transformer，连续删除2层，保留1/2/1的 prelude/core/coda，核心循环3次。2条随机文本与视觉特征只检查结构和优化路径，不是模型能力数据。  多模态基础模型 剪枝与循环恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 剪枝后直接循环与分阶段恢复相比，后者为何需要单独 projector 对齐？ 层手术会同时影响语言处理与图文接口。分阶段先恢复文本，再仅对齐视觉 projector，最后恢复整体指令行为，可分别处理这些破坏；直接循环不保证保留原能力。projector 阶段不加入 KD，与前后两个蒸馏恢复阶段有明确区别。 例如文字续写先恢复正常后，再让图像投影适应循环骨干，避免一开始将语言损伤和视觉失配混在同一训练信号里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ad08559b372ace80">剪枝后直接循环与分阶段恢复相比，后者为何需要单独 projector 对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arr-vlm">Retrofitting Recurrent Vision-Language Models from Pretrained Backbones</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Tübingen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层手术会同时影响语言处理与图文接口。分阶段先恢复文本，再仅对齐视觉 projector，最后恢复整体指令行为，可分别处理这些破坏；直接循环不保证保留原能力。projector 阶段不加入 KD，与前后两个蒸馏恢复阶段有明确区别。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如文字续写先恢复正常后，再让图像投影适应循环骨干，避免一开始将语言损伤和视觉失配混在同一训练信号里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22075">原论文</a> · <a href="../../../../foundation-models/2610.22075-rr-vlm/">实现解读</a> · <a href="#qa-ad08559b372ace80">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rr-vlm" data-paper-title="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones 基础模型 University of Tübingen 2026-10-15 预训练 VLM 的语言层可以剪掉一段，再共享循环保留核心块；但直接手术会破坏语言能力及图文对齐。RR-VLM 用一个线性 adapter 融合 prelude 上下文与循环状态，并依次执行文本恢复、projector 对齐、全模型指令恢复；文本和最终阶段加入原始未剪模型蒸馏。 即使1.4B模型能放入单卡，完整恢复仍过重，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机6层、16维因果 Transformer，连续删除2层，保留1/2/1的 prelude/core/coda，核心循环3次。2条随机文本与视觉特征只检查结构和优化路径，不是模型能力数据。  多模态基础模型 剪枝与循环恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 冻结教师和循环间 KV sharing 在本地实现中各是什么状态？ 教师需保留完整未剪模型的独立冻结副本并停止梯度；学生各阶段只更新规定参数。本地核对共享核心调用和手工展开等价，但未实现循环间 KV sharing 的增量推理，因此不能把结构循环已执行说成缓存复用或真实模型吞吐已验证。 例如三次 core 调用都指向同一模块可检查参数共享；它并不说明三轮生成已正确共享同一份 KV cache。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-85813119e6b229df">冻结教师和循环间 KV sharing 在本地实现中各是什么状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arr-vlm">Retrofitting Recurrent Vision-Language Models from Pretrained Backbones</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Tübingen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师需保留完整未剪模型的独立冻结副本并停止梯度；学生各阶段只更新规定参数。本地核对共享核心调用和手工展开等价，但未实现循环间 KV sharing 的增量推理，因此不能把结构循环已执行说成缓存复用或真实模型吞吐已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三次 core 调用都指向同一模块可检查参数共享；它并不说明三轮生成已正确共享同一份 KV cache。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22075">原论文</a> · <a href="../../../../foundation-models/2610.22075-rr-vlm/">实现解读</a> · <a href="#qa-85813119e6b229df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:softcache" data-paper-title="SoftCache: Adaptive Step Size Caching for Diffusion Transformers" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="SoftCache: Adaptive Step Size Caching for Diffusion Transformers 基础模型 Tel Aviv University 2026-10-15 动态缓存通常只决定“刷新/重用”，仍沿固定时间网格走。SoftCache 将累计陈旧度距离阈值的 headroom 转成连续步长：缓存越可靠就走得更远。它用两次新鲜残差作时间外推，并重新排布剩余节点，使跳过的节点不会又被访问。 完整实验不适合当前单卡，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。固定 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1、seeds42/43/44。不下载生成模型。8维小 MLP 先做一次真实梯度更新，再在同一初值和20步网格上比较 SoftCache、hard-cache 与全量 Euler；所有差异包括负结果保留。  推理与系统效率 扩散缓存与自适应采样 多模态 视觉证据预算：选 Token、选帧与按需回看 SoftCache 的 headroom 代表什么，而不是答案质量置信度？ headroom 是累计缓存陈旧度距离阈值的剩余空间，用便宜 probe 的相对变化估计。它决定本次缓存步长可扩大多少，不是生成内容正确或好看的概率；缓存可靠时走更远仍是数值近似，需要与未缓存输出和实际质量分别评估。 例如累计变化只用了阈值的一小部分，可允许更大时间步；这不表示当前图像有九成概率符合提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-softcache-596bc18d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cd266037ebd633fe">SoftCache 的 headroom 代表什么，而不是答案质量置信度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asoftcache">SoftCache: Adaptive Step Size Caching for Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tel Aviv University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>headroom 是累计缓存陈旧度距离阈值的剩余空间，用便宜 probe 的相对变化估计。它决定本次缓存步长可扩大多少，不是生成内容正确或好看的概率；缓存可靠时走更远仍是数值近似，需要与未缓存输出和实际质量分别评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如累计变化只用了阈值的一小部分，可允许更大时间步；这不表示当前图像有九成概率符合提示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22369">原论文</a> · <a href="../../../../foundation-models/2610.22369-softcache/">实现解读</a> · <a href="#qa-cd266037ebd633fe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:softcache" data-paper-title="SoftCache: Adaptive Step Size Caching for Diffusion Transformers" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="SoftCache: Adaptive Step Size Caching for Diffusion Transformers 基础模型 Tel Aviv University 2026-10-15 动态缓存通常只决定“刷新/重用”，仍沿固定时间网格走。SoftCache 将累计陈旧度距离阈值的 headroom 转成连续步长：缓存越可靠就走得更远。它用两次新鲜残差作时间外推，并重新排布剩余节点，使跳过的节点不会又被访问。 完整实验不适合当前单卡，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。固定 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1、seeds42/43/44。不下载生成模型。8维小 MLP 先做一次真实梯度更新，再在同一初值和20步网格上比较 SoftCache、hard-cache 与全量 Euler；所有差异包括负结果保留。  推理与系统效率 扩散缓存与自适应采样 多模态 视觉证据预算：选 Token、选帧与按需回看 SoftCache 的步长控制为什么不只是“这一层缓存刷新还是复用”？ 普通缓存沿固定时间节点选择是否重算，SoftCache 还依据陈旧度余量改变前进距离，并重新安排剩余节点。因此少算一次不应之后又访问被跳过的节点。残差外推需要新鲜锚点支撑，在变化太快或早期受限区域不能无条件继续扩大步长。 例如原计划经过十个去噪节点，可靠缓存允许跨过中间两个节点；后续网格也要重排，不能绕一圈再把它们算回来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8d790da7252145cc">SoftCache 的步长控制为什么不只是“这一层缓存刷新还是复用”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asoftcache">SoftCache: Adaptive Step Size Caching for Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tel Aviv University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通缓存沿固定时间节点选择是否重算，SoftCache 还依据陈旧度余量改变前进距离，并重新安排剩余节点。因此少算一次不应之后又访问被跳过的节点。残差外推需要新鲜锚点支撑，在变化太快或早期受限区域不能无条件继续扩大步长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原计划经过十个去噪节点，可靠缓存允许跨过中间两个节点；后续网格也要重排，不能绕一圈再把它们算回来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22369">原论文</a> · <a href="../../../../foundation-models/2610.22369-softcache/">实现解读</a> · <a href="#qa-8d790da7252145cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:softcache" data-paper-title="SoftCache: Adaptive Step Size Caching for Diffusion Transformers" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="SoftCache: Adaptive Step Size Caching for Diffusion Transformers 基础模型 Tel Aviv University 2026-10-15 动态缓存通常只决定“刷新/重用”，仍沿固定时间网格走。SoftCache 将累计陈旧度距离阈值的 headroom 转成连续步长：缓存越可靠就走得更远。它用两次新鲜残差作时间外推，并重新排布剩余节点，使跳过的节点不会又被访问。 完整实验不适合当前单卡，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。固定 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1、seeds42/43/44。不下载生成模型。8维小 MLP 先做一次真实梯度更新，再在同一初值和20步网格上比较 SoftCache、hard-cache 与全量 Euler；所有差异包括负结果保留。  推理与系统效率 扩散缓存与自适应采样 多模态 视觉证据预算：选 Token、选帧与按需回看 SoftCache 与固定网格上的刷新或复用，为什么不只是同一种缓存规则？ 固定网格 hard cache 只选择是否重新计算网络，仍访问原节点；SoftCache 还改变连续步长并重新排布剩余节点，真正跳过原节点。它同时近似残差与积分时间安排，因此调用减少要连同端点误差报告，不能只比较刷新次数。 例如从时间零点四直接走到零点六后，原来零点五的节点不应再访问，否则所谓跳步并未改变时间网格。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-170562c8fa83951d">SoftCache 与固定网格上的刷新或复用，为什么不只是同一种缓存规则？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asoftcache">SoftCache: Adaptive Step Size Caching for Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tel Aviv University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定网格 hard cache 只选择是否重新计算网络，仍访问原节点；SoftCache 还改变连续步长并重新排布剩余节点，真正跳过原节点。它同时近似残差与积分时间安排，因此调用减少要连同端点误差报告，不能只比较刷新次数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从时间零点四直接走到零点六后，原来零点五的节点不应再访问，否则所谓跳步并未改变时间网格。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22369">原论文</a> · <a href="../../../../foundation-models/2610.22369-softcache/">实现解读</a> · <a href="#qa-170562c8fa83951d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:softcache" data-paper-title="SoftCache: Adaptive Step Size Caching for Diffusion Transformers" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="SoftCache: Adaptive Step Size Caching for Diffusion Transformers 基础模型 Tel Aviv University 2026-10-15 动态缓存通常只决定“刷新/重用”，仍沿固定时间网格走。SoftCache 将累计陈旧度距离阈值的 headroom 转成连续步长：缓存越可靠就走得更远。它用两次新鲜残差作时间外推，并重新排布剩余节点，使跳过的节点不会又被访问。 完整实验不适合当前单卡，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。固定 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1、seeds42/43/44。不下载生成模型。8维小 MLP 先做一次真实梯度更新，再在同一初值和20步网格上比较 SoftCache、hard-cache 与全量 Euler；所有差异包括负结果保留。  推理与系统效率 扩散缓存与自适应采样 多模态 视觉证据预算：选 Token、选帧与按需回看 只有一个新鲜残差锚点时，能否使用两点线性外推公式？ 不能。两点外推需要两个不同时间的新鲜残差；只有一个时保持常数。早期 t&lt;0.1 或 probe 相对变化超过 0.18 时禁止跳步，步长还需截到终点；每个新样本必须创建独立缓存，不能沿用上一样本状态。 例如第一轮刚得到一个残差，没有前一锚点可计算斜率；硬套除以时间差的公式会制造无定义或错误的外推。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-809bbd8b8fe862a3">只有一个新鲜残差锚点时，能否使用两点线性外推公式？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asoftcache">SoftCache: Adaptive Step Size Caching for Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tel Aviv University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。两点外推需要两个不同时间的新鲜残差；只有一个时保持常数。早期 t&lt;0.1 或 probe 相对变化超过 0.18 时禁止跳步，步长还需截到终点；每个新样本必须创建独立缓存，不能沿用上一样本状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第一轮刚得到一个残差，没有前一锚点可计算斜率；硬套除以时间差的公式会制造无定义或错误的外推。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22369">原论文</a> · <a href="../../../../foundation-models/2610.22369-softcache/">实现解读</a> · <a href="#qa-809bbd8b8fe862a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vcola" data-paper-title="V-CoLA: Vision Token Compression with Linear Attention" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="V-CoLA: Vision Token Compression with Linear Attention 多模态大模型 Alibaba Cloud Computing / Alibaba Group 2026-10-08 传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。方法见官方正文第 3 节。原论文架构图为Figure 5，比较原始混合模型与压缩后的前向路径；图像及版权属于原作者。 本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。原始 Qwen3.5-9B checkpoint 的视觉编码器和全部语言层已在真实 A100 执行；重要性不是随机分数、像素相似度或隐藏答案。仅 4 张公开训练留出图片，不代表完整 VLM 质量结论。本地对照口径：同一个冻结原始 Qwen3.5-9B，比较 dense、第一层保留 50% / 25% 且第 24 层后退出视觉的三条真实前向。固定公共 CIFAR-10 官方训练集尾部留出图像；不读取官方 test，不训练、不择优调参。  多模态推理效率 视觉 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 线性注意力模型为什么不能直接读取完整 softmax 矩阵做视觉筛选？ Gated DeltaNet 将历史信息压入递推状态，没有相同形式的全 token softmax 注意力矩阵。V-CoLA 因而从真实状态读取长期保留程度，并检查单次更新对短期 query 响应的变化，重要性定义必须适应模型实际计算结构。 例如视觉 token 处理后只留下状态矩阵，不能假造一个标准 Transformer 的注意力行，再称其为原模型实际关注分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-multimodal-models-vcola-a4fb5eab" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-65f29f75fc6da94d">线性注意力模型为什么不能直接读取完整 softmax 矩阵做视觉筛选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avcola">V-CoLA: Vision Token Compression with Linear Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Cloud Computing / Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Gated DeltaNet 将历史信息压入递推状态，没有相同形式的全 token softmax 注意力矩阵。V-CoLA 因而从真实状态读取长期保留程度，并检查单次更新对短期 query 响应的变化，重要性定义必须适应模型实际计算结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如视觉 token 处理后只留下状态矩阵，不能假造一个标准 Transformer 的注意力行，再称其为原模型实际关注分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现选择；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11251">原论文</a> · <a href="../../../../multimodal-models/2610.11251-vcola/">实现解读</a> · <a href="#qa-65f29f75fc6da94d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vcola" data-paper-title="V-CoLA: Vision Token Compression with Linear Attention" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="V-CoLA: Vision Token Compression with Linear Attention 多模态大模型 Alibaba Cloud Computing / Alibaba Group 2026-10-08 传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。方法见官方正文第 3 节。原论文架构图为Figure 5，比较原始混合模型与压缩后的前向路径；图像及版权属于原作者。 本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。原始 Qwen3.5-9B checkpoint 的视觉编码器和全部语言层已在真实 A100 执行；重要性不是随机分数、像素相似度或隐藏答案。仅 4 张公开训练留出图片，不代表完整 VLM 质量结论。本地对照口径：同一个冻结原始 Qwen3.5-9B，比较 dense、第一层保留 50% / 25% 且第 24 层后退出视觉的三条真实前向。固定公共 CIFAR-10 官方训练集尾部留出图像；不读取官方 test，不训练、不择优调参。  多模态推理效率 视觉 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 为什么 Gated DeltaNet 的视觉压缩不能直接照搬 softmax attention 权重？ 线性递归状态并不显式保存同样的完整注意力矩阵，其信息由状态更新与遗忘共同决定。V-CoLA 用最终状态能否回读某 token 衡量长期保留，再测短窗口 query 对更新的响应变化补充独特性，之后连续分块合并；这些分数并非普通相似度排序。 例如一个 patch 刚写入时很显眼，却在后续状态中被覆盖，最终回读分数就会降低；单看当时的局部相似度会漏掉遗忘。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-92ed529fc5dae5c4">为什么 Gated DeltaNet 的视觉压缩不能直接照搬 softmax attention 权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avcola">V-CoLA: Vision Token Compression with Linear Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Cloud Computing / Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>线性递归状态并不显式保存同样的完整注意力矩阵，其信息由状态更新与遗忘共同决定。V-CoLA 用最终状态能否回读某 token 衡量长期保留，再测短窗口 query 对更新的响应变化补充独特性，之后连续分块合并；这些分数并非普通相似度排序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个 patch 刚写入时很显眼，却在后续状态中被覆盖，最终回读分数就会降低；单看当时的局部相似度会漏掉遗忘。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现选择；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11251">原论文</a> · <a href="../../../../multimodal-models/2610.11251-vcola/">实现解读</a> · <a href="#qa-92ed529fc5dae5c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vcola" data-paper-title="V-CoLA: Vision Token Compression with Linear Attention" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="V-CoLA: Vision Token Compression with Linear Attention 多模态大模型 Alibaba Cloud Computing / Alibaba Group 2026-10-08 传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。方法见官方正文第 3 节。原论文架构图为Figure 5，比较原始混合模型与压缩后的前向路径；图像及版权属于原作者。 本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。原始 Qwen3.5-9B checkpoint 的视觉编码器和全部语言层已在真实 A100 执行；重要性不是随机分数、像素相似度或隐藏答案。仅 4 张公开训练留出图片，不代表完整 VLM 质量结论。本地对照口径：同一个冻结原始 Qwen3.5-9B，比较 dense、第一层保留 50% / 25% 且第 24 层后退出视觉的三条真实前向。固定公共 CIFAR-10 官方训练集尾部留出图像；不读取官方 test，不训练、不择优调参。  多模态推理效率 视觉 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 V-CoLA 的长期保留分数与短期独特性分别避免哪种遗漏？ 长期分数检查某 token 的 value 能否从最终状态回读，短期分数衡量其更新是否带来不同响应。前者关注最终记忆，后者补充局部新增信息，两者按 0.9 与 0.1 结合；随后连续分块合并，而非只按单一静态相似度删除。 例如一个 token 与旧内容相似但长期保留很好，另一个提供短时新细节；两路信号让选择不完全被其中一种特征支配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6e0889ed1df84227">V-CoLA 的长期保留分数与短期独特性分别避免哪种遗漏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avcola">V-CoLA: Vision Token Compression with Linear Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Cloud Computing / Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长期分数检查某 token 的 value 能否从最终状态回读，短期分数衡量其更新是否带来不同响应。前者关注最终记忆，后者补充局部新增信息，两者按 0.9 与 0.1 结合；随后连续分块合并，而非只按单一静态相似度删除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个 token 与旧内容相似但长期保留很好，另一个提供短时新细节；两路信号让选择不完全被其中一种特征支配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现选择；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11251">原论文</a> · <a href="../../../../multimodal-models/2610.11251-vcola/">实现解读</a> · <a href="#qa-6e0889ed1df84227">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vcola" data-paper-title="V-CoLA: Vision Token Compression with Linear Attention" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="V-CoLA: Vision Token Compression with Linear Attention 多模态大模型 Alibaba Cloud Computing / Alibaba Group 2026-10-08 传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。方法见官方正文第 3 节。原论文架构图为Figure 5，比较原始混合模型与压缩后的前向路径；图像及版权属于原作者。 本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。原始 Qwen3.5-9B checkpoint 的视觉编码器和全部语言层已在真实 A100 执行；重要性不是随机分数、像素相似度或隐藏答案。仅 4 张公开训练留出图片，不代表完整 VLM 质量结论。本地对照口径：同一个冻结原始 Qwen3.5-9B，比较 dense、第一层保留 50% / 25% 且第 24 层后退出视觉的三条真实前向。固定公共 CIFAR-10 官方训练集尾部留出图像；不读取官方 test，不训练、不择优调参。  多模态推理效率 视觉 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 转置状态约定和 query probe 差异为什么必须写进实现说明？ 论文采用 value×key，本地沿官方后端使用 key×value，递推乘法必须相应转置。正文 Equation 7 使用 query probe，附录写 shifted keys，本地明确选择前者；再用官方 kernel 重放门槛验证真实状态，不能把两种规格默认为完全等价。 例如状态轴写反可能仍得到合法矩阵形状，却读错 key 与 value 关系；数值重放可比只检查 shape 更早发现这种错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dc06a879fde2db3d">转置状态约定和 query probe 差异为什么必须写进实现说明？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avcola">V-CoLA: Vision Token Compression with Linear Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Cloud Computing / Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>论文采用 value×key，本地沿官方后端使用 key×value，递推乘法必须相应转置。正文 Equation 7 使用 query probe，附录写 shifted keys，本地明确选择前者；再用官方 kernel 重放门槛验证真实状态，不能把两种规格默认为完全等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如状态轴写反可能仍得到合法矩阵形状，却读错 key 与 value 关系；数值重放可比只检查 shape 更早发现这种错误。</p>
<p class="ar-learning-sources">依据：核心公式与实现选择、本地复现、复现边界与 Evolve；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11251">原论文</a> · <a href="../../../../multimodal-models/2610.11251-vcola/">实现解读</a> · <a href="#qa-dc06a879fde2db3d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vimod" data-paper-title="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning 多模态大模型 City University of Hong Kong / Zhejiang University 2026-10-08 一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。 scripts/validate_vimod_cuda_runtime.py 另外在同一真实 checkpoint 上执行 TRACE 三阶段 CUDA 梯度诊断。已实现 DART 容量约束/隐式梯度、总量整数舍入、置信度硬分组、八轮 Sinkhorn、共享 residual Value 编码；TRACE 层融合、四尺度 SSM、区域边界、HOLD/UPDATE 与真实 Fine KV 恢复。checkpoint backend 支持 SmolVLM/Idefics3，而非声称兼容 Qwen3-VL 的多模态 RoPE。  视觉 Token 压缩 动态证据恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 Coarse KV 常驻时，为什么还要保留 Fine KV？ Coarse 表示提供低成本概览，但一次压缩可能遗漏后续问题需要的局部细节。ViMoD 保存原始 Fine KV 及粗细成员映射，让 TRACE 随已生成文本按需恢复证据；节省的是活跃工作集读取，并不表示原始视觉信息存储成本完全消失。 例如粗表示知道桌上有标签，推理到需要读标签文字时，再恢复对应原始 Fine KV，而不必事先把所有细节都常驻读取。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-multimodal-models-vimod-74b5d3f4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d872360a8c146634">Coarse KV 常驻时，为什么还要保留 Fine KV？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avimod">Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Coarse 表示提供低成本概览，但一次压缩可能遗漏后续问题需要的局部细节。ViMoD 保存原始 Fine KV 及粗细成员映射，让 TRACE 随已生成文本按需恢复证据；节省的是活跃工作集读取，并不表示原始视觉信息存储成本完全消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如粗表示知道桌上有标签，推理到需要读标签文字时，再恢复对应原始 Fine KV，而不必事先把所有细节都常驻读取。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12060">原论文</a> · <a href="../../../../multimodal-models/2610.12060-vimod/">实现解读</a> · <a href="#qa-d872360a8c146634">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vimod" data-paper-title="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning 多模态大模型 City University of Hong Kong / Zhejiang University 2026-10-08 一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。 scripts/validate_vimod_cuda_runtime.py 另外在同一真实 checkpoint 上执行 TRACE 三阶段 CUDA 梯度诊断。已实现 DART 容量约束/隐式梯度、总量整数舍入、置信度硬分组、八轮 Sinkhorn、共享 residual Value 编码；TRACE 层融合、四尺度 SSM、区域边界、HOLD/UPDATE 与真实 Fine KV 恢复。checkpoint backend 支持 SmolVLM/Idefics3，而非声称兼容 Qwen3-VL 的多模态 RoPE。  视觉 Token 压缩 动态证据恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 TRACE 的 UPDATE 为什么替换活跃 Fine 工作集，而不是不断累加？ 不断累加会使活跃上下文随推理增长，失去预算约束。ViMoD 让 Coarse 表示持续存在，而 Fine 细节按当前生成历史保持或替换，原始细节仍可恢复；被替换的是当前参与注意力的工作集，不是把底层 Fine 缓存永久删除。 例如先取左侧标签，再转向右侧仪表时替换细节工作集；粗图仍在，之后也能按需重新取回左侧标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fc110d35d7abbcbf">TRACE 的 UPDATE 为什么替换活跃 Fine 工作集，而不是不断累加？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avimod">Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不断累加会使活跃上下文随推理增长，失去预算约束。ViMoD 让 Coarse 表示持续存在，而 Fine 细节按当前生成历史保持或替换，原始细节仍可恢复；被替换的是当前参与注意力的工作集，不是把底层 Fine 缓存永久删除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先取左侧标签，再转向右侧仪表时替换细节工作集；粗图仍在，之后也能按需重新取回左侧标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12060">原论文</a> · <a href="../../../../multimodal-models/2610.12060-vimod/">实现解读</a> · <a href="#qa-fc110d35d7abbcbf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vimod" data-paper-title="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning 多模态大模型 City University of Hong Kong / Zhejiang University 2026-10-08 一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。 scripts/validate_vimod_cuda_runtime.py 另外在同一真实 checkpoint 上执行 TRACE 三阶段 CUDA 梯度诊断。已实现 DART 容量约束/隐式梯度、总量整数舍入、置信度硬分组、八轮 Sinkhorn、共享 residual Value 编码；TRACE 层融合、四尺度 SSM、区域边界、HOLD/UPDATE 与真实 Fine KV 恢复。checkpoint backend 支持 SmolVLM/Idefics3，而非声称兼容 Qwen3-VL 的多模态 RoPE。  视觉 Token 压缩 动态证据恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 TRACE 的 UPDATE 与不断累加所有访问过的区域有什么差别？ UPDATE 用新选择的 Fine 区域替换原工作集，HOLD 则保持现状；不断累加会让工作集随推理增长，破坏固定预算。多时间尺度 SSM 从因果文本状态决定访问，因此不能提前读取未来文本或参考答案帮助选择区域。 例如先检查左侧物体再检查右侧时，替换可释放左侧工作集；若两者永远累积，长推理最终会退化为读取全量视觉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bf5803f7913a539b">TRACE 的 UPDATE 与不断累加所有访问过的区域有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avimod">Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>UPDATE 用新选择的 Fine 区域替换原工作集，HOLD 则保持现状；不断累加会让工作集随推理增长，破坏固定预算。多时间尺度 SSM 从因果文本状态决定访问，因此不能提前读取未来文本或参考答案帮助选择区域。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先检查左侧物体再检查右侧时，替换可释放左侧工作集；若两者永远累积，长推理最终会退化为读取全量视觉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12060">原论文</a> · <a href="../../../../multimodal-models/2610.12060-vimod/">实现解读</a> · <a href="#qa-bf5803f7913a539b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vimod" data-paper-title="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning 多模态大模型 City University of Hong Kong / Zhejiang University 2026-10-08 一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。 scripts/validate_vimod_cuda_runtime.py 另外在同一真实 checkpoint 上执行 TRACE 三阶段 CUDA 梯度诊断。已实现 DART 容量约束/隐式梯度、总量整数舍入、置信度硬分组、八轮 Sinkhorn、共享 residual Value 编码；TRACE 层融合、四尺度 SSM、区域边界、HOLD/UPDATE 与真实 Fine KV 恢复。checkpoint backend 支持 SmolVLM/Idefics3，而非声称兼容 Qwen3-VL 的多模态 RoPE。  视觉 Token 压缩 动态证据恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 DART 前向硬分组时，训练梯度为什么仍能跨组传播？ 容量受总和约束并通过隐式 Jacobian 反传，池化采用 hard+soft-stopgrad(soft) 的直通形式，使前向保留硬组、反向利用 Sinkhorn 连续容量。阶段训练还需真实 Fine-index 标注或在线 teacher；缺少这些条件时应报错，不能制造伪证据标签。 例如前向把一个 patch 分到甲组，反向仍可通过连续分配调整容量；但没有真实监督时，不能用预设答案区域冒充学会检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-85c9904410c3762f">DART 前向硬分组时，训练梯度为什么仍能跨组传播？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avimod">Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>容量受总和约束并通过隐式 Jacobian 反传，池化采用 hard+soft-stopgrad(soft) 的直通形式，使前向保留硬组、反向利用 Sinkhorn 连续容量。阶段训练还需真实 Fine-index 标注或在线 teacher；缺少这些条件时应报错，不能制造伪证据标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前向把一个 patch 分到甲组，反向仍可通过连续分配调整容量；但没有真实监督时，不能用预设答案区域冒充学会检索。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12060">原论文</a> · <a href="../../../../multimodal-models/2610.12060-vimod/">实现解读</a> · <a href="#qa-85c9904410c3762f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:video-encoder-selection" data-paper-title="Video Encoders Built on Image Representations" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Video Encoders Built on Image Representations 基础模型 Stanford University 2026-10-05 逐帧图像编码保留可寻址的单帧证据，却产生很长的视觉序列。论文先逐帧冻结编码，再结合问题相关性、帧内多样性和跨帧对应，在固定预算内选择原始 token；可选 learned refiner 在选择完成后读取额外邻帧上下文，只更新已保留的锚点，不增加输出长度。 单张A100/A30或Mac不适合该完整campaign，因此完整 refiner/全表实验成本过高，不复现（审查 DONE）。CPU 单元测试核验最大 cosine、质量归一化、DPP 核、独立 determinant ratio、Schur residual、对应边阈值、pair complementarity/平局、奇数/零/满预算、原始源位置与中间 stream 恒等，以及非法 quota、NaN、重复身份、无答案输入合同。人工张量只用于这些公式测试，不作为视觉能力证据。  视频理解 训练免费视觉token选择 多模态 视觉证据预算：选 Token、选帧与按需回看 这里的 training-free selection 为什么仍需要问题向量？ 视觉 encoder 冻结并逐帧编码，选择器用问题及选项片段的输入 embedding 判断相关性，再结合帧内多样性与跨帧对应。training-free 指选择阶段不额外训练，并非不读取问题；也不能把答案标签塞进问题向量来增强相关性。 例如问哪一帧出现钥匙时，可用“钥匙”的问题表示选择原始 patch；正确帧编号不能作为隐藏输入参与选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-video-encoder-selection-2d465377" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-79eabead0b3ea73d">这里的 training-free selection 为什么仍需要问题向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avideo-encoder-selection">Video Encoders Built on Image Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视觉 encoder 冻结并逐帧编码，选择器用问题及选项片段的输入 embedding 判断相关性，再结合帧内多样性与跨帧对应。training-free 指选择阶段不额外训练，并非不读取问题；也不能把答案标签塞进问题向量来增强相关性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问哪一帧出现钥匙时，可用“钥匙”的问题表示选择原始 patch；正确帧编号不能作为隐藏输入参与选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.06616">原论文</a> · <a href="../../../../foundation-models/2610.06616-video-encoder-selection/">实现解读</a> · <a href="#qa-79eabead0b3ea73d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:video-encoder-selection" data-paper-title="Video Encoders Built on Image Representations" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Video Encoders Built on Image Representations 基础模型 Stanford University 2026-10-05 逐帧图像编码保留可寻址的单帧证据，却产生很长的视觉序列。论文先逐帧冻结编码，再结合问题相关性、帧内多样性和跨帧对应，在固定预算内选择原始 token；可选 learned refiner 在选择完成后读取额外邻帧上下文，只更新已保留的锚点，不增加输出长度。 单张A100/A30或Mac不适合该完整campaign，因此完整 refiner/全表实验成本过高，不复现（审查 DONE）。CPU 单元测试核验最大 cosine、质量归一化、DPP 核、独立 determinant ratio、Schur residual、对应边阈值、pair complementarity/平局、奇数/零/满预算、原始源位置与中间 stream 恒等，以及非法 quota、NaN、重复身份、无答案输入合同。人工张量只用于这些公式测试，不作为视觉能力证据。  视频理解 训练免费视觉token选择 多模态 视觉证据预算：选 Token、选帧与按需回看 learned refiner 为什么只更新保留下来的锚点，而不再增加视觉 Token？ 选择阶段先在固定预算内保留原始可寻址证据，refiner 随后让这些锚点读取邻帧上下文来改善表示。这样增加的是每个保留位置的信息，而非输出序列长度；若不断追加邻帧 token，就破坏固定预算，也混淆了选择与上下文补充两项收益。 例如先保留十个关键 patch，refiner 为它们读取邻帧运动线索后仍输出十个；不能再追加二十个邻帧位置并声称预算不变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4a106f0ffb777141">learned refiner 为什么只更新保留下来的锚点，而不再增加视觉 Token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avideo-encoder-selection">Video Encoders Built on Image Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>选择阶段先在固定预算内保留原始可寻址证据，refiner 随后让这些锚点读取邻帧上下文来改善表示。这样增加的是每个保留位置的信息，而非输出序列长度；若不断追加邻帧 token，就破坏固定预算，也混淆了选择与上下文补充两项收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先保留十个关键 patch，refiner 为它们读取邻帧运动线索后仍输出十个；不能再追加二十个邻帧位置并声称预算不变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.06616">原论文</a> · <a href="../../../../foundation-models/2610.06616-video-encoder-selection/">实现解读</a> · <a href="#qa-4a106f0ffb777141">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:video-encoder-selection" data-paper-title="Video Encoders Built on Image Representations" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Video Encoders Built on Image Representations 基础模型 Stanford University 2026-10-05 逐帧图像编码保留可寻址的单帧证据，却产生很长的视觉序列。论文先逐帧冻结编码，再结合问题相关性、帧内多样性和跨帧对应，在固定预算内选择原始 token；可选 learned refiner 在选择完成后读取额外邻帧上下文，只更新已保留的锚点，不增加输出长度。 单张A100/A30或Mac不适合该完整campaign，因此完整 refiner/全表实验成本过高，不复现（审查 DONE）。CPU 单元测试核验最大 cosine、质量归一化、DPP 核、独立 determinant ratio、Schur residual、对应边阈值、pair complementarity/平局、奇数/零/满预算、原始源位置与中间 stream 恒等，以及非法 quota、NaN、重复身份、无答案输入合同。人工张量只用于这些公式测试，不作为视觉能力证据。  视频理解 训练免费视觉token选择 多模态 视觉证据预算：选 Token、选帧与按需回看 选择原始 token 与可选 learned refiner 的输出边界有什么不同？ selection-only 返回固定预算内的原始 token、位置及中间流的同一组索引，不平均或重设坐标。refiner 可再读邻帧上下文更新已选锚点，但不增加输出数量；因此训练免费选择器与含训练 refiner 的完整结果不能混为一项。 例如保留五十个源 token 后，refiner 可让这五十个吸收邻帧信息，却不能偷偷加回五十个新 token 再宣称相同预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6879eb4eb04dbefb">选择原始 token 与可选 learned refiner 的输出边界有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avideo-encoder-selection">Video Encoders Built on Image Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>selection-only 返回固定预算内的原始 token、位置及中间流的同一组索引，不平均或重设坐标。refiner 可再读邻帧上下文更新已选锚点，但不增加输出数量；因此训练免费选择器与含训练 refiner 的完整结果不能混为一项。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保留五十个源 token 后，refiner 可让这五十个吸收邻帧信息，却不能偷偷加回五十个新 token 再宣称相同预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.06616">原论文</a> · <a href="../../../../foundation-models/2610.06616-video-encoder-selection/">实现解读</a> · <a href="#qa-6879eb4eb04dbefb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:video-encoder-selection" data-paper-title="Video Encoders Built on Image Representations" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Video Encoders Built on Image Representations 基础模型 Stanford University 2026-10-05 逐帧图像编码保留可寻址的单帧证据，却产生很长的视觉序列。论文先逐帧冻结编码，再结合问题相关性、帧内多样性和跨帧对应，在固定预算内选择原始 token；可选 learned refiner 在选择完成后读取额外邻帧上下文，只更新已保留的锚点，不增加输出长度。 单张A100/A30或Mac不适合该完整campaign，因此完整 refiner/全表实验成本过高，不复现（审查 DONE）。CPU 单元测试核验最大 cosine、质量归一化、DPP 核、独立 determinant ratio、Schur residual、对应边阈值、pair complementarity/平局、奇数/零/满预算、原始源位置与中间 stream 恒等，以及非法 quota、NaN、重复身份、无答案输入合同。人工张量只用于这些公式测试，不作为视觉能力证据。  视频理解 训练免费视觉token选择 多模态 视觉证据预算：选 Token、选帧与按需回看 最佳 pair 与 singleton 打平时如何选择，为什么仍能填满奇数预算？ 只有 pair 的每 token 增益严格更大才一次加入两个端点，否则取 singleton；每步遵守帧 quota 和剩余预算。即使增益为负或没有跨帧边，也继续完成恰好 B 个互异索引。当前外部均匀 quota 与 scene proxy 是已标注差异，未实现 SITE allocator。 例如预算剩一个时只能选 singleton；若两个端点平均增益恰与单点相同，也取单点，而不是超额凑成一对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-378b6dec7ef4d3ae">最佳 pair 与 singleton 打平时如何选择，为什么仍能填满奇数预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avideo-encoder-selection">Video Encoders Built on Image Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有 pair 的每 token 增益严格更大才一次加入两个端点，否则取 singleton；每步遵守帧 quota 和剩余预算。即使增益为负或没有跨帧边，也继续完成恰好 B 个互异索引。当前外部均匀 quota 与 scene proxy 是已标注差异，未实现 SITE allocator。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预算剩一个时只能选 singleton；若两个端点平均增益恰与单点相同，也取单点，而不是超额凑成一对。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、本地结果与验收边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.06616">原论文</a> · <a href="../../../../foundation-models/2610.06616-video-encoder-selection/">实现解读</a> · <a href="#qa-378b6dec7ef4d3ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mwop" data-paper-title="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs 基础模型 原文首页未列第一作者机构 2026-10-01 在同一注意力头内分别剪 V2V/T2V/T2T 路径，并为视觉、文本执行选择不同 FFN 通道；注意力剪枝后重新估计 FFN 重要性。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态大模型 结构剪枝 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 MWOP 中同一个注意力头为什么仍能有不同模态路径的重要性？ 一个头可同时承担视觉到视觉、文本到视觉和文本到文本的信息传递，这些路径对任务的贡献可能不同。MWOP 在头内分别评估并剪枝，而非把整个头视为单一不可分单元；保留某路径也不意味着该头所有模态交互都要保留。 例如某个头主要用于文本读取图像，视觉内部交互贡献较小，按路径剪枝可保留前者而减少后者。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-mwop-c24139ed" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4b6ef536b9d9ff84">MWOP 中同一个注意力头为什么仍能有不同模态路径的重要性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amwop">MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个头可同时承担视觉到视觉、文本到视觉和文本到文本的信息传递，这些路径对任务的贡献可能不同。MWOP 在头内分别评估并剪枝，而非把整个头视为单一不可分单元；保留某路径也不意味着该头所有模态交互都要保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某个头主要用于文本读取图像，视觉内部交互贡献较小，按路径剪枝可保留前者而减少后者。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01434">原论文</a> · <a href="../../../../foundation-models/2610.01434-mwop/">实现解读</a> · <a href="#qa-4b6ef536b9d9ff84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mwop" data-paper-title="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs 基础模型 原文首页未列第一作者机构 2026-10-01 在同一注意力头内分别剪 V2V/T2V/T2T 路径，并为视觉、文本执行选择不同 FFN 通道；注意力剪枝后重新估计 FFN 重要性。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态大模型 结构剪枝 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 为什么剪完注意力路径后，还要重新估计 FFN 通道的重要性？ 注意力剪枝改变了进入 FFN 的信息分布，原先的重要性排序可能已经过时。MWOP 还把视觉到视觉、文本到视觉等路径和不同模态的 FFN 通道分开处理，避免用一个总分掩盖模态差异；剪枝后的质量与真实速度仍要分别验证。 例如删除部分文本读取视觉的路径后，一些负责融合视觉的 FFN 通道贡献会变化，不能继续沿用手术前的通道排名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e71e27b14980f452">为什么剪完注意力路径后，还要重新估计 FFN 通道的重要性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amwop">MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>注意力剪枝改变了进入 FFN 的信息分布，原先的重要性排序可能已经过时。MWOP 还把视觉到视觉、文本到视觉等路径和不同模态的 FFN 通道分开处理，避免用一个总分掩盖模态差异；剪枝后的质量与真实速度仍要分别验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删除部分文本读取视觉的路径后，一些负责融合视觉的 FFN 通道贡献会变化，不能继续沿用手术前的通道排名。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01434">原论文</a> · <a href="../../../../foundation-models/2610.01434-mwop/">实现解读</a> · <a href="#qa-e71e27b14980f452">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mwop" data-paper-title="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs 基础模型 原文首页未列第一作者机构 2026-10-01 在同一注意力头内分别剪 V2V/T2V/T2T 路径，并为视觉、文本执行选择不同 FFN 通道；注意力剪枝后重新估计 FFN 重要性。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态大模型 结构剪枝 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 与统一剪掉相同 FFN 通道相比，模态相关通道选择改变了什么？ 视觉与文本 token 可使用不同的 FFN 通道集合，允许共享模型在两类输入上保留不同计算容量。统一通道剪枝为所有模态使用同一掩码，可能忽略贡献差异；这种灵活性也需要实际执行支持，掩码稀疏不自动等于硬件更快。 例如文本常用的通道与视觉纹理通道不重合，分别保留可以比统一交集更有表达空间，但 kernel 仍须真正跳过计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5c9fc2d7d0b259f3">与统一剪掉相同 FFN 通道相比，模态相关通道选择改变了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amwop">MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视觉与文本 token 可使用不同的 FFN 通道集合，允许共享模型在两类输入上保留不同计算容量。统一通道剪枝为所有模态使用同一掩码，可能忽略贡献差异；这种灵活性也需要实际执行支持，掩码稀疏不自动等于硬件更快。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如文本常用的通道与视觉纹理通道不重合，分别保留可以比统一交集更有表达空间，但 kernel 仍须真正跳过计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01434">原论文</a> · <a href="../../../../foundation-models/2610.01434-mwop/">实现解读</a> · <a href="#qa-5c9fc2d7d0b259f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mwop" data-paper-title="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs 基础模型 原文首页未列第一作者机构 2026-10-01 在同一注意力头内分别剪 V2V/T2V/T2T 路径，并为视觉、文本执行选择不同 FFN 通道；注意力剪枝后重新估计 FFN 重要性。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态大模型 结构剪枝 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 为什么注意力剪枝后需要重新估计 FFN 重要性？ 注意力改变 token 表示及后续梯度，旧 FFN 重要性可能已不适用于新网络。基于权重与损失梯度乘积幅值的估计应在修改后重算；本地只执行独立路径及通道 mask，没有模型级精度或定制 kernel 加速证据。 例如删掉一条视觉交互路径后，某 FFN 通道收到的信息改变，直接沿用原排名可能把现在关键的通道误删。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-82b1ce006c57fdb6">为什么注意力剪枝后需要重新估计 FFN 重要性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amwop">MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>注意力改变 token 表示及后续梯度，旧 FFN 重要性可能已不适用于新网络。基于权重与损失梯度乘积幅值的估计应在修改后重算；本地只执行独立路径及通道 mask，没有模型级精度或定制 kernel 加速证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删掉一条视觉交互路径后，某 FFN 通道收到的信息改变，直接沿用原排名可能把现在关键的通道误删。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01434">原论文</a> · <a href="../../../../foundation-models/2610.01434-mwop/">实现解读</a> · <a href="#qa-82b1ce006c57fdb6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:veto" data-paper-title="VETO: Video Efficient Token Optimization for Vision Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VETO: Video Efficient Token Optimization for Vision Language Models 基础模型 National Taiwan University 2026-10-01 先在帧内合并语义近邻 token，再对压缩后的 frame representation 做跨帧去冗余；空间先行显著降低全局时间匹配成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  视频 VLM Token 压缩 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 VETO 的空间压缩和时间压缩分别作用于什么冗余？ 空间阶段在单帧内合并语义近邻 token，时间阶段再处理跨帧重复内容。先减少每帧表示长度可降低后续全局时间匹配的规模；这是有顺序的两轴操作，不能只把所有帧 token 混在一起随便挑一批就称为同一设计。 例如每帧都有大量相似墙面，先在帧内压缩墙面，再比较相邻帧的剩余表示，可少做许多重复跨帧匹配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-veto-75da8cb3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-893d97b86bd46781">VETO 的空间压缩和时间压缩分别作用于什么冗余？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aveto">VETO: Video Efficient Token Optimization for Vision Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National Taiwan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>空间阶段在单帧内合并语义近邻 token，时间阶段再处理跨帧重复内容。先减少每帧表示长度可降低后续全局时间匹配的规模；这是有顺序的两轴操作，不能只把所有帧 token 混在一起随便挑一批就称为同一设计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如每帧都有大量相似墙面，先在帧内压缩墙面，再比较相邻帧的剩余表示，可少做许多重复跨帧匹配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01785">原论文</a> · <a href="../../../../foundation-models/2610.01785-veto/">实现解读</a> · <a href="#qa-893d97b86bd46781">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:veto" data-paper-title="VETO: Video Efficient Token Optimization for Vision Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VETO: Video Efficient Token Optimization for Vision Language Models 基础模型 National Taiwan University 2026-10-01 先在帧内合并语义近邻 token，再对压缩后的 frame representation 做跨帧去冗余；空间先行显著降低全局时间匹配成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  视频 VLM Token 压缩 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 先帧内合并、再跨帧去冗余，为什么不是任意可交换的两步？ 帧内合并先减少每帧的候选数量，让跨帧匹配面对更短的表示，降低时间维比较成本。若先在所有原始 patch 间做全局时间匹配，就已经支付了更大的搜索开销，得到的对应关系也可能不同；两步顺序本身就是机制的一部分。 例如每帧一百个 patch 先压成二十个，再找相邻帧重复内容；反过来先匹配全部原始 patch 就省不下同一部分计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ffd7d671be8de7d4">先帧内合并、再跨帧去冗余，为什么不是任意可交换的两步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aveto">VETO: Video Efficient Token Optimization for Vision Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National Taiwan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>帧内合并先减少每帧的候选数量，让跨帧匹配面对更短的表示，降低时间维比较成本。若先在所有原始 patch 间做全局时间匹配，就已经支付了更大的搜索开销，得到的对应关系也可能不同；两步顺序本身就是机制的一部分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如每帧一百个 patch 先压成二十个，再找相邻帧重复内容；反过来先匹配全部原始 patch 就省不下同一部分计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01785">原论文</a> · <a href="../../../../foundation-models/2610.01785-veto/">实现解读</a> · <a href="#qa-ffd7d671be8de7d4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:veto" data-paper-title="VETO: Video Efficient Token Optimization for Vision Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VETO: Video Efficient Token Optimization for Vision Language Models 基础模型 National Taiwan University 2026-10-01 先在帧内合并语义近邻 token，再对压缩后的 frame representation 做跨帧去冗余；空间先行显著降低全局时间匹配成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  视频 VLM Token 压缩 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 空间先行与先做全序列时间匹配，在计算负担上有何差别？ 全序列时间匹配先面对原始的大量 token，空间先行则先缩小候选集合再跨帧处理，重点是降低后段匹配规模。顺序也可能改变保留证据，因此只比较理论候选数不能证明质量不变，更不能代替真实视频时延。 例如十帧各一百个 token，先各压到二十个，时间阶段处理二百个而非一千个；但压掉的细节仍可能影响任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-29587d13df18756f">空间先行与先做全序列时间匹配，在计算负担上有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aveto">VETO: Video Efficient Token Optimization for Vision Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National Taiwan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全序列时间匹配先面对原始的大量 token，空间先行则先缩小候选集合再跨帧处理，重点是降低后段匹配规模。顺序也可能改变保留证据，因此只比较理论候选数不能证明质量不变，更不能代替真实视频时延。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十帧各一百个 token，先各压到二十个，时间阶段处理二百个而非一千个；但压掉的细节仍可能影响任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01785">原论文</a> · <a href="../../../../foundation-models/2610.01785-veto/">实现解读</a> · <a href="#qa-29587d13df18756f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:veto" data-paper-title="VETO: Video Efficient Token Optimization for Vision Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VETO: Video Efficient Token Optimization for Vision Language Models 基础模型 National Taiwan University 2026-10-01 先在帧内合并语义近邻 token，再对压缩后的 frame representation 做跨帧去冗余；空间先行显著降低全局时间匹配成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  视频 VLM Token 压缩 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 本地最远点代表验证保留了什么，又缺少什么？ 本地用确定性最远点代表检查空间先行、时间后继的双轴顺序与预算，并在 GPU 执行对应压缩。它没有加载论文 7B VLM 或真实视频 benchmark，代表点启发式也不能冒充完整语义合并能力；因此只报告机制诊断，不复述作者吞吐为本地收益。 例如压缩后 token 数符合预算，可证明两阶段都运行；它不说明模型仍能识别被合并区域中的小物体动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-45257d5781bda87f">本地最远点代表验证保留了什么，又缺少什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aveto">VETO: Video Efficient Token Optimization for Vision Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National Taiwan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地用确定性最远点代表检查空间先行、时间后继的双轴顺序与预算，并在 GPU 执行对应压缩。它没有加载论文 7B VLM 或真实视频 benchmark，代表点启发式也不能冒充完整语义合并能力；因此只报告机制诊断，不复述作者吞吐为本地收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如压缩后 token 数符合预算，可证明两阶段都运行；它不说明模型仍能识别被合并区域中的小物体动作。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01785">原论文</a> · <a href="../../../../foundation-models/2610.01785-veto/">实现解读</a> · <a href="#qa-45257d5781bda87f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hawk" data-paper-title="HAWK: Rethinking Multimodal Drafting for Speculative Decoding" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="HAWK: Rethinking Multimodal Drafting for Speculative Decoding 基础模型 原文首页未列第一作者机构 2026-09-30 从 target 多层隐藏状态学习混合，给浅层 drafter 提供压缩视觉表示，并用 drafter 自己提议后的 shifted trajectory 训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行层混合与 shifted target 隔离；未实现专用解码 kernel。执行层混合与 shifted target 隔离；未实现专用解码 kernel。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态推理 投机解码 蒸馏 多模态 视觉证据预算：选 Token、选帧与按需回看 HAWK 的 target 与 drafter 在投机解码中分别负责什么？ drafter 用较低成本提出候选 token，target 负责验证候选并保持最终生成分布的约束。HAWK 从 target 多层隐藏状态学习压缩表示供浅层 drafter 使用，重点是提高有效提议，而不是把 drafter 当作无需验证的替代大模型。 例如浅层模型一次提出几个词，大模型统一检查能接受多少；草稿更准可减少浪费，但未被接受的词不能直接当最终输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-hawk-938adaa0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-969c6e9709068ac4">HAWK 的 target 与 drafter 在投机解码中分别负责什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahawk">HAWK: Rethinking Multimodal Drafting for Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>drafter 用较低成本提出候选 token，target 负责验证候选并保持最终生成分布的约束。HAWK 从 target 多层隐藏状态学习压缩表示供浅层 drafter 使用，重点是提高有效提议，而不是把 drafter 当作无需验证的替代大模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如浅层模型一次提出几个词，大模型统一检查能接受多少；草稿更准可减少浪费，但未被接受的词不能直接当最终输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00623">原论文</a> · <a href="../../../../foundation-models/2610.00623-hawk/">实现解读</a> · <a href="#qa-969c6e9709068ac4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hawk" data-paper-title="HAWK: Rethinking Multimodal Drafting for Speculative Decoding" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="HAWK: Rethinking Multimodal Drafting for Speculative Decoding 基础模型 原文首页未列第一作者机构 2026-09-30 从 target 多层隐藏状态学习混合，给浅层 drafter 提供压缩视觉表示，并用 drafter 自己提议后的 shifted trajectory 训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行层混合与 shifted target 隔离；未实现专用解码 kernel。执行层混合与 shifted target 隔离；未实现专用解码 kernel。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态推理 投机解码 蒸馏 多模态 视觉证据预算：选 Token、选帧与按需回看 为什么 drafter 要在自己提出 token 后的 shifted trajectory 上训练？ 草稿会把系统带到自己的前缀分布，始终在教师理想前缀训练会掩盖这些偏移。移位后的轨迹让监督与实际提议后的状态对齐，多层教师状态混合再提供压缩视觉信息；草稿是否被接纳仍须目标模型验证，不能靠训练损失替代接受率测量。 例如草稿第一步选了另一种说法，第二步就应在这个真实前缀上学习目标分布，而非假装第一步与教师完全相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a6e2431346cfbada">为什么 drafter 要在自己提出 token 后的 shifted trajectory 上训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahawk">HAWK: Rethinking Multimodal Drafting for Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>草稿会把系统带到自己的前缀分布，始终在教师理想前缀训练会掩盖这些偏移。移位后的轨迹让监督与实际提议后的状态对齐，多层教师状态混合再提供压缩视觉信息；草稿是否被接纳仍须目标模型验证，不能靠训练损失替代接受率测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如草稿第一步选了另一种说法，第二步就应在这个真实前缀上学习目标分布，而非假装第一步与教师完全相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00623">原论文</a> · <a href="../../../../foundation-models/2610.00623-hawk/">实现解读</a> · <a href="#qa-a6e2431346cfbada">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hawk" data-paper-title="HAWK: Rethinking Multimodal Drafting for Speculative Decoding" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="HAWK: Rethinking Multimodal Drafting for Speculative Decoding 基础模型 原文首页未列第一作者机构 2026-09-30 从 target 多层隐藏状态学习混合，给浅层 drafter 提供压缩视觉表示，并用 drafter 自己提议后的 shifted trajectory 训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行层混合与 shifted target 隔离；未实现专用解码 kernel。执行层混合与 shifted target 隔离；未实现专用解码 kernel。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态推理 投机解码 蒸馏 多模态 视觉证据预算：选 Token、选帧与按需回看 训练自己提议后的 shifted trajectory 与只看 teacher 的标准前缀有何区别？ drafter 自身提议会改变后续访问的前缀，训练这些移位后的状态可缩小训练与真实草拟过程的分布差距。只在 teacher 标准轨迹上拟合，不一定覆盖草稿错误后的状态；这是监督分布差异，不能只用训练损失推断解码加速。 例如草稿先提出了一个不同形容词，后续预测应学习该实际前缀的 target 分布，而不是一直假装前文仍是教师原句。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-08951b88c5bc06ae">训练自己提议后的 shifted trajectory 与只看 teacher 的标准前缀有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahawk">HAWK: Rethinking Multimodal Drafting for Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>drafter 自身提议会改变后续访问的前缀，训练这些移位后的状态可缩小训练与真实草拟过程的分布差距。只在 teacher 标准轨迹上拟合，不一定覆盖草稿错误后的状态；这是监督分布差异，不能只用训练损失推断解码加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如草稿先提出了一个不同形容词，后续预测应学习该实际前缀的 target 分布，而不是一直假装前文仍是教师原句。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00623">原论文</a> · <a href="../../../../foundation-models/2610.00623-hawk/">实现解读</a> · <a href="#qa-08951b88c5bc06ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hawk" data-paper-title="HAWK: Rethinking Multimodal Drafting for Speculative Decoding" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="HAWK: Rethinking Multimodal Drafting for Speculative Decoding 基础模型 原文首页未列第一作者机构 2026-09-30 从 target 多层隐藏状态学习混合，给浅层 drafter 提供压缩视觉表示，并用 drafter 自己提议后的 shifted trajectory 训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行层混合与 shifted target 隔离；未实现专用解码 kernel。执行层混合与 shifted target 隔离；未实现专用解码 kernel。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态推理 投机解码 蒸馏 多模态 视觉证据预算：选 Token、选帧与按需回看 多层混合与 shifted target 的本地验证包含专用解码 kernel 吗？ 不包含。层权重经过 softmax 后对 target 隐状态加权，监督目标来自移位后的 target 分布，并要保持目标路径隔离。本地只验证该混合及目标隔离，不含完整投机验证循环或专用 kernel，因此不能用算子通过声称端到端无损提速。 例如三层混合权重和为一可检查表示计算；它没有测量一次实际生成能接受几个草稿 token 或节省多少时间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1e1157c08ff9a8f8">多层混合与 shifted target 的本地验证包含专用解码 kernel 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahawk">HAWK: Rethinking Multimodal Drafting for Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不包含。层权重经过 softmax 后对 target 隐状态加权，监督目标来自移位后的 target 分布，并要保持目标路径隔离。本地只验证该混合及目标隔离，不含完整投机验证循环或专用 kernel，因此不能用算子通过声称端到端无损提速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三层混合权重和为一可检查表示计算；它没有测量一次实际生成能接受几个草稿 token 或节省多少时间。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00623">原论文</a> · <a href="../../../../foundation-models/2610.00623-hawk/">实现解读</a> · <a href="#qa-1e1157c08ff9a8f8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:stacktok" data-paper-title="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection 多模态大模型 Sichuan University 2026-09-15 把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视觉 Token 选择 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 StackTok 为什么同时考虑问题相关性与视觉覆盖？ 只挑与问题相似的 token 可能重复保留同一局部，漏掉支撑判断的其他区域；只追覆盖又可能把预算花在无关背景。StackTok 将相关性作为目标、覆盖作为随预算变化的支撑约束，逐步选择时协调两者，而不是把两种分数随意相加。 例如问桌上有几种餐具，许多高相关 token 都来自同一只碗；保留一定区域覆盖可避免漏掉另一侧的叉子。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-multimodal-models-stacktok-c22648c2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1f465fb879831c02">StackTok 为什么同时考虑问题相关性与视觉覆盖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Astacktok">StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sichuan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只挑与问题相似的 token 可能重复保留同一局部，漏掉支撑判断的其他区域；只追覆盖又可能把预算花在无关背景。StackTok 将相关性作为目标、覆盖作为随预算变化的支撑约束，逐步选择时协调两者，而不是把两种分数随意相加。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问桌上有几种餐具，许多高相关 token 都来自同一只碗；保留一定区域覆盖可避免漏掉另一侧的叉子。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16841">原论文</a> · <a href="../../../../multimodal-models/2609.16841-stacktok/">实现解读</a> · <a href="#qa-1f465fb879831c02">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:stacktok" data-paper-title="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection 多模态大模型 Sichuan University 2026-09-15 把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视觉 Token 选择 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 为何相关性最高的视觉 Token 不一定组成最好的固定预算子集？ 它们可能集中在同一区域，重复提供相同信息而遗漏全图结构。StackTok 以相关性为主要目标，并用随预算变化的覆盖参考检查当前缺口，再切换选取准则；覆盖并非固定比例的装饰项，不同问题与预算需要不同程度的支持。 例如问整幅场景布局时，只选人物脸部的一堆高相关 patch 可能漏掉门的位置；补覆盖能保留另一类必要证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-146cde1710f5ee82">为何相关性最高的视觉 Token 不一定组成最好的固定预算子集？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Astacktok">StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sichuan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它们可能集中在同一区域，重复提供相同信息而遗漏全图结构。StackTok 以相关性为主要目标，并用随预算变化的覆盖参考检查当前缺口，再切换选取准则；覆盖并非固定比例的装饰项，不同问题与预算需要不同程度的支持。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问整幅场景布局时，只选人物脸部的一堆高相关 patch 可能漏掉门的位置；补覆盖能保留另一类必要证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16841">原论文</a> · <a href="../../../../multimodal-models/2609.16841-stacktok/">实现解读</a> · <a href="#qa-146cde1710f5ee82">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:stacktok" data-paper-title="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection 多模态大模型 Sichuan University 2026-09-15 把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视觉 Token 选择 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 预算自适应覆盖约束与固定比例混合两个排序有什么区别？ 固定混合始终以相同比例偏好相关性和覆盖，预算改变时未必合适；自适应约束会按当前支撑缺口切换选择准则。机制的重点是选择过程中的约束状态，而非额外计算一个静态多样性分数；效果仍需真实 VLM 与固定预算评估。 例如只剩两个名额且关键区域尚未覆盖时，可以优先补支撑；预算宽松、覆盖已足够时再优先问题相关 token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-47fcf43099b85610">预算自适应覆盖约束与固定比例混合两个排序有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Astacktok">StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sichuan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定混合始终以相同比例偏好相关性和覆盖，预算改变时未必合适；自适应约束会按当前支撑缺口切换选择准则。机制的重点是选择过程中的约束状态，而非额外计算一个静态多样性分数；效果仍需真实 VLM 与固定预算评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只剩两个名额且关键区域尚未覆盖时，可以优先补支撑；预算宽松、覆盖已足够时再优先问题相关 token。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16841">原论文</a> · <a href="../../../../multimodal-models/2609.16841-stacktok/">实现解读</a> · <a href="#qa-47fcf43099b85610">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:stacktok" data-paper-title="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection 多模态大模型 Sichuan University 2026-09-15 把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视觉 Token 选择 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 本地 single-crop selector 的通过能说明五种论文 VLM 已加速吗？ 不能。本地仅执行 reference-gated 的单 crop 选择，三 seed fixture 验证排序、门控与预算等状态不变量，未加载论文中的五个 VLM。选择索引正确不等于模型前向真的缩短，更不能从保留比例推算生成时延或准确率。 例如返回十个互异索引且满足预算只验证选择器；若下游仍读取全部视觉 token，实际推理成本就没有相应降低。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eccf1fd02dc72752">本地 single-crop selector 的通过能说明五种论文 VLM 已加速吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Astacktok">StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sichuan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地仅执行 reference-gated 的单 crop 选择，三 seed fixture 验证排序、门控与预算等状态不变量，未加载论文中的五个 VLM。选择索引正确不等于模型前向真的缩短，更不能从保留比例推算生成时延或准确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如返回十个互异索引且满足预算只验证选择器；若下游仍读取全部视觉 token，实际推理成本就没有相应降低。</p>
<p class="ar-learning-sources">依据：核心公式与实现对应、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16841">原论文</a> · <a href="../../../../multimodal-models/2609.16841-stacktok/">实现解读</a> · <a href="#qa-eccf1fd02dc72752">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:videomm" data-paper-title="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs 多模态大模型 University of Science and Technology of China 2026-09-15 先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视频理解 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 VideoMM 的 Macro Proxy 为什么不是最终高保真视觉证据？ Macro Proxy 用低分辨率信息便宜地定位相关区域并形成宏观判断，细节不足时才激活 Micro Tokens。低分辨率内容可能足以判断场景，却无法可靠读取小字或细微动作，因此两级接口的价值在于按需要补充证据，而非把粗表示当完整视频。 例如宏观代理能定位到人物进门片段，但要看胸牌上的字，就应读取相应位置的高保真 token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-multimodal-models-videomm-bc3e057a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-581d21dad7641725">VideoMM 的 Macro Proxy 为什么不是最终高保真视觉证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avideomm">VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Macro Proxy 用低分辨率信息便宜地定位相关区域并形成宏观判断，细节不足时才激活 Micro Tokens。低分辨率内容可能足以判断场景，却无法可靠读取小字或细微动作，因此两级接口的价值在于按需要补充证据，而非把粗表示当完整视频。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如宏观代理能定位到人物进门片段，但要看胸牌上的字，就应读取相应位置的高保真 token。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16722">原论文</a> · <a href="../../../../multimodal-models/2609.16722-videomm/">实现解读</a> · <a href="#qa-581d21dad7641725">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:videomm" data-paper-title="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs 多模态大模型 University of Science and Technology of China 2026-09-15 先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视频理解 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 低分辨率 Macro Proxy 已经定位区域，为什么还需要按条件激活 Micro Tokens？ 粗粒度表示能快速筛去大量无关内容，却可能无法区分小字或细微动作。只有宏观证据不足时才追加高保真细节，可以把预算集中到不确定之处；这要求保留粗到细的取证路径，而不是把所有问题都固定压到同一份低清摘要。 例如粗看知道有人举牌，问是否举牌可直接回答；问牌上数字则可能需要激活对应区域的高分辨率 token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-db0d078e8b45aa47">低分辨率 Macro Proxy 已经定位区域，为什么还需要按条件激活 Micro Tokens？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avideomm">VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>粗粒度表示能快速筛去大量无关内容，却可能无法区分小字或细微动作。只有宏观证据不足时才追加高保真细节，可以把预算集中到不确定之处；这要求保留粗到细的取证路径，而不是把所有问题都固定压到同一份低清摘要。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如粗看知道有人举牌，问是否举牌可直接回答；问牌上数字则可能需要激活对应区域的高分辨率 token。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16722">原论文</a> · <a href="../../../../multimodal-models/2609.16722-videomm/">实现解读</a> · <a href="#qa-db0d078e8b45aa47">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:videomm" data-paper-title="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs 多模态大模型 University of Science and Technology of China 2026-09-15 先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视频理解 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 按共识触发 Micro 与固定给每段相同高分辨率预算有什么取舍？ 固定预算不依赖当前证据充分性，容易在简单区域重复花费；共识不足再触发 Micro 可集中开销，但路由错误也可能漏掉细节。应把“触发策略不同”与“实际问答更好”分开，后者需要相同视频、问题和成本下的比较。 例如大部分片段只问场景类型，不必都读取细节；遇到区分相似工具的问题，宏观一致也未必足够，需要可靠触发条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-25f7d8e5c3ad0407">按共识触发 Micro 与固定给每段相同高分辨率预算有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avideomm">VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定预算不依赖当前证据充分性，容易在简单区域重复花费；共识不足再触发 Micro 可集中开销，但路由错误也可能漏掉细节。应把“触发策略不同”与“实际问答更好”分开，后者需要相同视频、问题和成本下的比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如大部分片段只问场景类型，不必都读取细节；遇到区分相似工具的问题，宏观一致也未必足够，需要可靠触发条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16722">原论文</a> · <a href="../../../../multimodal-models/2609.16722-videomm/">实现解读</a> · <a href="#qa-25f7d8e5c3ad0407">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:videomm" data-paper-title="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs 多模态大模型 University of Science and Technology of China 2026-09-15 先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视频理解 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 本地 macro 选择和 micro 激活的 GPU receipt 能覆盖完整视频 MLLM 吗？ 不能。receipt 只证明相应状态转换在 A100 上实际运行，本地没有加载完整视频 MLLM。门控触发次数、选中索引与预算检查属于机制证据，不能改称 LongVideoBench 分数或端到端吞吐，也不意味着语义共识判断已得到真实验证。 例如测试里故意给出低共识值后成功激活 Micro，证明分支可达；它没有测试模型能否从真实画面估计该共识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c9eec1fc577aafde">本地 macro 选择和 micro 激活的 GPU receipt 能覆盖完整视频 MLLM 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Avideomm">VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。receipt 只证明相应状态转换在 A100 上实际运行，本地没有加载完整视频 MLLM。门控触发次数、选中索引与预算检查属于机制证据，不能改称 LongVideoBench 分数或端到端吞吐，也不意味着语义共识判断已得到真实验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试里故意给出低共识值后成功激活 Micro，证明分支可达；它没有测试模型能否从真实画面估计该共识。</p>
<p class="ar-learning-sources">依据：核心公式与实现对应、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16722">原论文</a> · <a href="../../../../multimodal-models/2609.16722-videomm/">实现解读</a> · <a href="#qa-c9eec1fc577aafde">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frames-on-demand" data-paper-title="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding 基础模型 Queen Mary University of London 2026-09-10 视频只做一次 caption memory；visual-need router 判断文本证据不足时，才在固定预算内读取相关帧。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  长视频理解 视觉预算路由 多模态 视觉证据预算：选 Token、选帧与按需回看 一次 caption memory 与后续按需看帧分别保存什么信息？ caption memory 提供便宜、可复用的文字索引，后续问题先基于它判断证据是否充足；只有需要视觉细节时才消耗帧预算。文字记忆可能遗漏颜色、空间关系或瞬时动作，因此按需看帧是补充证据的路径，而非保证 caption 已无损保存视频。 例如字幕记忆写“有人走进房间”，问进入时间可查记忆，问手里拿什么可能需要回看对应帧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-frames-on-demand-ec1c6746" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2f9ed6ab63e2f74a">一次 caption memory 与后续按需看帧分别保存什么信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aframes-on-demand">Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Queen Mary University of London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>caption memory 提供便宜、可复用的文字索引，后续问题先基于它判断证据是否充足；只有需要视觉细节时才消耗帧预算。文字记忆可能遗漏颜色、空间关系或瞬时动作，因此按需看帧是补充证据的路径，而非保证 caption 已无损保存视频。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如字幕记忆写“有人走进房间”，问进入时间可查记忆，问手里拿什么可能需要回看对应帧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11899">原论文</a> · <a href="../../../../foundation-models/2609.11899-frames-on-demand/">实现解读</a> · <a href="#qa-2f9ed6ab63e2f74a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frames-on-demand" data-paper-title="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding 基础模型 Queen Mary University of London 2026-09-10 视频只做一次 caption memory；visual-need router 判断文本证据不足时，才在固定预算内读取相关帧。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  长视频理解 视觉预算路由 多模态 视觉证据预算：选 Token、选帧与按需回看 先写 caption memory 后，为什么还需要 visual-need router？ 文字记忆能覆盖粗粒度事件，却可能遗漏以后问题需要的细节。路由器判断现有文字证据是否足够，只有不足时才花视觉预算读取相关帧；这样控制的是追加取证的成本，不是把描述当成无损视频，也不能把路由决定本身视为答案正确。 例如记忆只写“有人拿起盒子”，问盒子上的编号时就需回读帧；问是否有人取物则可能直接利用已有文字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d5d97e558e97b297">先写 caption memory 后，为什么还需要 visual-need router？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aframes-on-demand">Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Queen Mary University of London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文字记忆能覆盖粗粒度事件，却可能遗漏以后问题需要的细节。路由器判断现有文字证据是否足够，只有不足时才花视觉预算读取相关帧；这样控制的是追加取证的成本，不是把描述当成无损视频，也不能把路由决定本身视为答案正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如记忆只写“有人拿起盒子”，问盒子上的编号时就需回读帧；问是否有人取物则可能直接利用已有文字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11899">原论文</a> · <a href="../../../../foundation-models/2609.11899-frames-on-demand/">实现解读</a> · <a href="#qa-d5d97e558e97b297">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frames-on-demand" data-paper-title="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding 基础模型 Queen Mary University of London 2026-09-10 视频只做一次 caption memory；visual-need router 判断文本证据不足时，才在固定预算内读取相关帧。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  长视频理解 视觉预算路由 多模态 视觉证据预算：选 Token、选帧与按需回看 这种路由与每个问题都重新均匀采样视频有什么取舍？ 均匀重采样为每个问题重复支付视觉开销，按需路线复用一次文字记忆并把预算集中到疑点帧。它可能节省成本，也可能因 caption 漏记或路由判断错误而错过关键证据；机制比较不能替代相同问题与预算下的实际质量验证。 例如连续十个问题都问已有事件顺序时，可复用记忆；若第十问涉及极短动作，仍需正确定位并读取该帧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-78351d40c96d69a6">这种路由与每个问题都重新均匀采样视频有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aframes-on-demand">Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Queen Mary University of London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均匀重采样为每个问题重复支付视觉开销，按需路线复用一次文字记忆并把预算集中到疑点帧。它可能节省成本，也可能因 caption 漏记或路由判断错误而错过关键证据；机制比较不能替代相同问题与预算下的实际质量验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如连续十个问题都问已有事件顺序时，可复用记忆；若第十问涉及极短动作，仍需正确定位并读取该帧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11899">原论文</a> · <a href="../../../../foundation-models/2609.11899-frames-on-demand/">实现解读</a> · <a href="#qa-78351d40c96d69a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frames-on-demand" data-paper-title="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding 基础模型 Queen Mary University of London 2026-09-10 视频只做一次 caption memory；visual-need router 判断文本证据不足时，才在固定预算内读取相关帧。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  长视频理解 视觉预算路由 多模态 视觉证据预算：选 Token、选帧与按需回看 本地 caption/query gate 的三 seed 输出能验证 learned visual-need router 吗？ 不能。当前只执行 caption 与 query 的 gate、Top-K 帧选择等 reference 状态转换，未运行长视频 VLM 或训练语义路由器。它能检查预算和选择接口，不能证明系统确实知道哪些问题仅凭文字即可回答，也不能复刻原文帧消耗收益。 例如规则门能保证最多选择三帧，但三帧是否包含问题答案仍需真实视频与语义模型，不能由计数检查得出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8d826d052ddc75b2">本地 caption/query gate 的三 seed 输出能验证 learned visual-need router 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aframes-on-demand">Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Queen Mary University of London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前只执行 caption 与 query 的 gate、Top-K 帧选择等 reference 状态转换，未运行长视频 VLM 或训练语义路由器。它能检查预算和选择接口，不能证明系统确实知道哪些问题仅凭文字即可回答，也不能复刻原文帧消耗收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规则门能保证最多选择三帧，但三帧是否包含问题答案仍需真实视频与语义模型，不能由计数检查得出。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11899">原论文</a> · <a href="../../../../foundation-models/2609.11899-frames-on-demand/">实现解读</a> · <a href="#qa-8d826d052ddc75b2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:omnikvquant" data-paper-title="OmniKVQuant: KV Cache Quantization for Omni-LLMs" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="OmniKVQuant: KV Cache Quantization for Omni-LLMs 基础模型 KAIST 2026-09-10 按短时间窗确定 key 量化范围，并按模态分别旋转 value，处理 temporal drift 与异构几何。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  多模态推理 KV Cache 量化 多模态 视觉证据预算：选 Token、选帧与按需回看 OmniKVQuant 为什么分别处理 key 的时间漂移与 value 的模态几何？ key 的数值范围可随时间变化，短窗口量化让尺度更贴近当前片段；不同模态的 value 分布几何也可能不同，分别旋转旨在使低位量化更合适。两种操作针对不同张量特性，不能把它们简化成所有 cache 共用一个全局缩放值。 例如前半段音频与后半段图像 token 的分布不同，单一全序列范围可能被局部极值占据，使多数值分辨率很低。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-omnikvquant-a8e321c1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f9bc9fa701552ac3">OmniKVQuant 为什么分别处理 key 的时间漂移与 value 的模态几何？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aomnikvquant">OmniKVQuant: KV Cache Quantization for Omni-LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>key 的数值范围可随时间变化，短窗口量化让尺度更贴近当前片段；不同模态的 value 分布几何也可能不同，分别旋转旨在使低位量化更合适。两种操作针对不同张量特性，不能把它们简化成所有 cache 共用一个全局缩放值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前半段音频与后半段图像 token 的分布不同，单一全序列范围可能被局部极值占据，使多数值分辨率很低。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11582">原论文</a> · <a href="../../../../foundation-models/2609.11582-omnikvquant/">实现解读</a> · <a href="#qa-f9bc9fa701552ac3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:omnikvquant" data-paper-title="OmniKVQuant: KV Cache Quantization for Omni-LLMs" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="OmniKVQuant: KV Cache Quantization for Omni-LLMs 基础模型 KAIST 2026-09-10 按短时间窗确定 key 量化范围，并按模态分别旋转 value，处理 temporal drift 与异构几何。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  多模态推理 KV Cache 量化 多模态 视觉证据预算：选 Token、选帧与按需回看 多模态 KV 为什么不宜共享一套全局量化范围和旋转？ Key 的数值分布可能随时间漂移，长期统一范围会让局部有效精度变差；不同模态 Value 的几何结构也不一致。短窗范围与模态专属旋转分别处理时间变化和模态差异，不能把两种校准合并成一套静态规则后仍假设误差同样可控。 例如前段音频 Key 的幅度较小、后段视频 Key 较大，全局范围可能挤压前者精度；Value 也需按模态检查结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-936078904d8b48d2">多模态 KV 为什么不宜共享一套全局量化范围和旋转？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aomnikvquant">OmniKVQuant: KV Cache Quantization for Omni-LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Key 的数值分布可能随时间漂移，长期统一范围会让局部有效精度变差；不同模态 Value 的几何结构也不一致。短窗范围与模态专属旋转分别处理时间变化和模态差异，不能把两种校准合并成一套静态规则后仍假设误差同样可控。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前段音频 Key 的幅度较小、后段视频 Key 较大，全局范围可能挤压前者精度；Value 也需按模态检查结构。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11582">原论文</a> · <a href="../../../../foundation-models/2609.11582-omnikvquant/">实现解读</a> · <a href="#qa-936078904d8b48d2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:omnikvquant" data-paper-title="OmniKVQuant: KV Cache Quantization for Omni-LLMs" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="OmniKVQuant: KV Cache Quantization for Omni-LLMs 基础模型 KAIST 2026-09-10 按短时间窗确定 key 量化范围，并按模态分别旋转 value，处理 temporal drift 与异构几何。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  多模态推理 KV Cache 量化 多模态 视觉证据预算：选 Token、选帧与按需回看 模态独立旋转与所有 value 使用同一旋转矩阵的假设差别是什么？ 统一旋转假定各模态可由同一坐标变换改善量化；独立旋转允许音频、视觉和文本具有不同合适坐标系。它增加模态相关处理，但结果仍取决于校准及真实分布，不能从旋转存在就推断所有任务都保留同等精度。 例如图像 value 的大方差方向与音频不同，分别旋转可分别展开数值；强制共用矩阵可能只适合其中一种。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b1f98617e99f9653">模态独立旋转与所有 value 使用同一旋转矩阵的假设差别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aomnikvquant">OmniKVQuant: KV Cache Quantization for Omni-LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一旋转假定各模态可由同一坐标变换改善量化；独立旋转允许音频、视觉和文本具有不同合适坐标系。它增加模态相关处理，但结果仍取决于校准及真实分布，不能从旋转存在就推断所有任务都保留同等精度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图像 value 的大方差方向与音频不同，分别旋转可分别展开数值；强制共用矩阵可能只适合其中一种。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11582">原论文</a> · <a href="../../../../foundation-models/2609.11582-omnikvquant/">实现解读</a> · <a href="#qa-b1f98617e99f9653">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:omnikvquant" data-paper-title="OmniKVQuant: KV Cache Quantization for Omni-LLMs" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="OmniKVQuant: KV Cache Quantization for Omni-LLMs 基础模型 KAIST 2026-09-10 按短时间窗确定 key 量化范围，并按模态分别旋转 value，处理 temporal drift 与异构几何。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  多模态推理 KV Cache 量化 多模态 视觉证据预算：选 Token、选帧与按需回看 本地 2-bit NumPy reference 可以证明 GPU KV kernel 加速吗？ 不能。本地实现窗口量化与模态独立旋转，用于检查低位表示和变换公式；Triton 等实际 kernel 仍需真实 A100 或 A30 验证。内存位宽下降与端到端时延之间还隔着打包、解包、访存和融合开销，不能按压缩比直接换算加速。 例如每个值理论只占两位，若实现仍以浮点数组存储和解码，就尚未获得真实两位 cache 的显存或带宽收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4cd2907c3a53ebaf">本地 2-bit NumPy reference 可以证明 GPU KV kernel 加速吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aomnikvquant">OmniKVQuant: KV Cache Quantization for Omni-LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地实现窗口量化与模态独立旋转，用于检查低位表示和变换公式；Triton 等实际 kernel 仍需真实 A100 或 A30 验证。内存位宽下降与端到端时延之间还隔着打包、解包、访存和融合开销，不能按压缩比直接换算加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如每个值理论只占两位，若实现仍以浮点数组存储和解码，就尚未获得真实两位 cache 的显存或带宽收益。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11582">原论文</a> · <a href="../../../../foundation-models/2609.11582-omnikvquant/">实现解读</a> · <a href="#qa-4cd2907c3a53ebaf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pace-vlm" data-paper-title="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference 基础模型 Sun Yat-sen University 2026-08-27 VLM 的视觉 token 一方面在 prefill 阶段带来大量计算，另一方面在抽取阶段仍会保留大量与问题无关的内容。PACE 将两个阶段拆开处理：APC 用浅层 ViT preview 同时估计全局语义密度和局部细节，按图像难度自适应缩放；DDAE 再融合 LLM 与视觉编码器的注意力，以置信度决定两种证据各占多少权重，而不是固定只信一种注意力图。 复现级别：核心机制 + 真实 checkpoint 公开数据验证。复现级别：核心机制 + 真实 checkpoint 公开数据验证。APC、DDAE 公式和 Qwen2.5-VL 自适应分辨率路径均实际执行；没有把小样本结果冒充论文完整 benchmark。本地正式结果是小型 RealWorldQA checkpoint smoke，不覆盖论文完整 11 个 benchmark；当前 runner 实测 APC 主路径，DDAE 以独立公式和单测验证，尚未复制作者约 2,000 行的模型 fork 与定制 kernel。本地对照口径：基线是同一 Qwen2.5-VL checkpoint 的原始视觉分辨率；  multimodal-foundation-model visual-token-compression inference-serving 多模态 视觉证据预算：选 Token、选帧与按需回看 PACE 为什么把 condense 和 extract 分成两段？ 输入分辨率会影响视觉编码与 prefill 成本，而编码后保留哪些 token 又影响后续读取。APC 在完整编码前用浅层预览分配图像预算，DDAE 在提取阶段融合视觉与语言注意力。两个阶段控制不同开销，不能只做后段筛选就宣称避免了前段编码。 例如先把简单图像缩小可减少初始 token，之后再保留与问题相关部分；若先全分辨率编码再删 token，前段成本已付出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-pace-vlm-f64143ef" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-73728e1c45489aa8">PACE 为什么把 condense 和 extract 分成两段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apace-vlm">PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>输入分辨率会影响视觉编码与 prefill 成本，而编码后保留哪些 token 又影响后续读取。APC 在完整编码前用浅层预览分配图像预算，DDAE 在提取阶段融合视觉与语言注意力。两个阶段控制不同开销，不能只做后段筛选就宣称避免了前段编码。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先把简单图像缩小可减少初始 token，之后再保留与问题相关部分；若先全分辨率编码再删 token，前段成本已付出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27206">原论文</a> · <a href="../../../../reproductions/2608.27206-pace-vlm/">实现解读</a> · <a href="#qa-73728e1c45489aa8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pace-vlm" data-paper-title="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference 基础模型 Sun Yat-sen University 2026-08-27 VLM 的视觉 token 一方面在 prefill 阶段带来大量计算，另一方面在抽取阶段仍会保留大量与问题无关的内容。PACE 将两个阶段拆开处理：APC 用浅层 ViT preview 同时估计全局语义密度和局部细节，按图像难度自适应缩放；DDAE 再融合 LLM 与视觉编码器的注意力，以置信度决定两种证据各占多少权重，而不是固定只信一种注意力图。 复现级别：核心机制 + 真实 checkpoint 公开数据验证。复现级别：核心机制 + 真实 checkpoint 公开数据验证。APC、DDAE 公式和 Qwen2.5-VL 自适应分辨率路径均实际执行；没有把小样本结果冒充论文完整 benchmark。本地正式结果是小型 RealWorldQA checkpoint smoke，不覆盖论文完整 11 个 benchmark；当前 runner 实测 APC 主路径，DDAE 以独立公式和单测验证，尚未复制作者约 2,000 行的模型 fork 与定制 kernel。本地对照口径：基线是同一 Qwen2.5-VL checkpoint 的原始视觉分辨率；  multimodal-foundation-model visual-token-compression inference-serving 多模态 视觉证据预算：选 Token、选帧与按需回看 PACE 为什么把图像缩放与问题相关 Token 抽取拆成两个阶段？ 缩放先控制视觉输入本身的成本，抽取再控制哪些内容进入后续处理；只在末端丢 token，已经支付的编码成本不会消失。浅层预览估计图像难度，抽取又按置信度融合语言与视觉注意力，避免始终盲信单一路径或固定压缩所有图像。 例如空白背景图可先缩小，密集菜单则保留较多细节；之后再根据问题选择相关区域，而非两张图都按同一比例裁减。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0da1b5df32b59d4e">PACE 为什么把图像缩放与问题相关 Token 抽取拆成两个阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apace-vlm">PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缩放先控制视觉输入本身的成本，抽取再控制哪些内容进入后续处理；只在末端丢 token，已经支付的编码成本不会消失。浅层预览估计图像难度，抽取又按置信度融合语言与视觉注意力，避免始终盲信单一路径或固定压缩所有图像。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如空白背景图可先缩小，密集菜单则保留较多细节；之后再根据问题选择相关区域，而非两张图都按同一比例裁减。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27206">原论文</a> · <a href="../../../../reproductions/2608.27206-pace-vlm/">实现解读</a> · <a href="#qa-0da1b5df32b59d4e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pace-vlm" data-paper-title="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference 基础模型 Sun Yat-sen University 2026-08-27 VLM 的视觉 token 一方面在 prefill 阶段带来大量计算，另一方面在抽取阶段仍会保留大量与问题无关的内容。PACE 将两个阶段拆开处理：APC 用浅层 ViT preview 同时估计全局语义密度和局部细节，按图像难度自适应缩放；DDAE 再融合 LLM 与视觉编码器的注意力，以置信度决定两种证据各占多少权重，而不是固定只信一种注意力图。 复现级别：核心机制 + 真实 checkpoint 公开数据验证。复现级别：核心机制 + 真实 checkpoint 公开数据验证。APC、DDAE 公式和 Qwen2.5-VL 自适应分辨率路径均实际执行；没有把小样本结果冒充论文完整 benchmark。本地正式结果是小型 RealWorldQA checkpoint smoke，不覆盖论文完整 11 个 benchmark；当前 runner 实测 APC 主路径，DDAE 以独立公式和单测验证，尚未复制作者约 2,000 行的模型 fork 与定制 kernel。本地对照口径：基线是同一 Qwen2.5-VL checkpoint 的原始视觉分辨率；  multimodal-foundation-model visual-token-compression inference-serving 多模态 视觉证据预算：选 Token、选帧与按需回看 DDAE 与固定各占一半的注意力融合有何区别？ DDAE 根据两路归一化注意力的离散度，通过温度 softmax 生成置信度权重，允许不同输入上更信某一路。固定平均不随证据分布变化；离散度只是该方法采用的置信度信号，不应直接当成校准后的答案正确概率。 例如语言注意力较集中、视觉注意力分散时，融合可偏向前者；若换一个问题，两路权重也可随之变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7b6eb0d63a176892">DDAE 与固定各占一半的注意力融合有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apace-vlm">PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DDAE 根据两路归一化注意力的离散度，通过温度 softmax 生成置信度权重，允许不同输入上更信某一路。固定平均不随证据分布变化；离散度只是该方法采用的置信度信号，不应直接当成校准后的答案正确概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如语言注意力较集中、视觉注意力分散时，融合可偏向前者；若换一个问题，两路权重也可随之变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27206">原论文</a> · <a href="../../../../reproductions/2608.27206-pace-vlm/">实现解读</a> · <a href="#qa-7b6eb0d63a176892">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pace-vlm" data-paper-title="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference 基础模型 Sun Yat-sen University 2026-08-27 VLM 的视觉 token 一方面在 prefill 阶段带来大量计算，另一方面在抽取阶段仍会保留大量与问题无关的内容。PACE 将两个阶段拆开处理：APC 用浅层 ViT preview 同时估计全局语义密度和局部细节，按图像难度自适应缩放；DDAE 再融合 LLM 与视觉编码器的注意力，以置信度决定两种证据各占多少权重，而不是固定只信一种注意力图。 复现级别：核心机制 + 真实 checkpoint 公开数据验证。复现级别：核心机制 + 真实 checkpoint 公开数据验证。APC、DDAE 公式和 Qwen2.5-VL 自适应分辨率路径均实际执行；没有把小样本结果冒充论文完整 benchmark。本地正式结果是小型 RealWorldQA checkpoint smoke，不覆盖论文完整 11 个 benchmark；当前 runner 实测 APC 主路径，DDAE 以独立公式和单测验证，尚未复制作者约 2,000 行的模型 fork 与定制 kernel。本地对照口径：基线是同一 Qwen2.5-VL checkpoint 的原始视觉分辨率；  multimodal-foundation-model visual-token-compression inference-serving 多模态 视觉证据预算：选 Token、选帧与按需回看 当前真实 checkpoint 路径完整验证了 DDAE 吗？ 没有。README 的小样本真实 checkpoint smoke 主要验证 APC，DDAE 由独立公式与单测检查，未复制作者完整模型 fork 和 kernel。APC 的全局密度排除对角自相似，局部项取偏离均值最大的 Top-K，压缩方向通过也不等于质量无损。 例如八个样本压缩前后同为五题正确，只是小样本观察；不能据此把 DDAE 也标为实际生成链路已验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-79280489155e740b">当前真实 checkpoint 路径完整验证了 DDAE 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apace-vlm">PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。README 的小样本真实 checkpoint smoke 主要验证 APC，DDAE 由独立公式与单测检查，未复制作者完整模型 fork 和 kernel。APC 的全局密度排除对角自相似，局部项取偏离均值最大的 Top-K，压缩方向通过也不等于质量无损。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如八个样本压缩前后同为五题正确，只是小样本观察；不能据此把 DDAE 也标为实际生成链路已验证。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27206">原论文</a> · <a href="../../../../reproductions/2608.27206-pace-vlm/">实现解读</a> · <a href="#qa-79280489155e740b">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

视觉输入太长时，哪些细节可以暂时不读，哪些必须保留恢复入口？

## 记住这一点

StackTok 把问题相关性作为目标、覆盖度作为随预算变化的约束，依据当前不足在两种选取准则之间切换。ViMoD 用 DART 形成持久粗粒度表示并保留到原始 Fine tokens 的映射，再由 TRACE 根据已生成前缀决定保持或替换活跃细节。前者主要在解码前选子集，后者为推理中途改变证据需求保留回看通道。

## 一个例子

先问“图里有哪些物体”需要覆盖整图，接着比较某件商品标签时需要放大局部。一次压缩若永久删掉标签 token，后续推理无法凭空找回；可恢复方案可以再取细节，但必须计入原始 Fine KV 的存储和取回成本。长视频同样要考虑关键帧与时间覆盖。

## 什么时候要小心

视觉 Token 减少比例不等于整机显存或延迟同比下降；视觉 encoder、文本解码、缓存和路由都要计费。可恢复细节也不是免费保留。StackTok 本地只有 reference selector，ViMoD 有真实 checkpoint 运行与梯度验证，但均不能把机制通过说成原文能力提升已复现。

## 先读这几篇

先读 StackTok 的相关性/覆盖度切换，理解一次性预算分配；再读 ViMoD 的 Coarse/Fine 与 HOLD/UPDATE，理解为什么多步推理可能需要重新取证。其余选帧、层宽剪枝和视觉缓存方法再按瓶颈进入。

1. [StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection](../../../multimodal-models/2609.16841-stacktok/README.md) · [原论文](https://arxiv.org/abs/2609.16841)
2. [Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning](../../../multimodal-models/2610.12060-vimod/README.md) · [原论文](https://arxiv.org/abs/2610.12060)

## 自测一下

保留可恢复 Fine KV 后，是否可以把总视觉存储记成只有 Coarse tokens？

??? note "展开参考答案"

    不可以。Coarse 只是常驻的活跃上下文，Fine KV 及映射仍占存储，动态恢复还需带宽和路由计算。应分别报告活跃 attention 预算、总缓存存储和端到端时延。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
