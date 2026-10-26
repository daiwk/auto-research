---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 视觉证据预算：选 Token、选帧与按需回看

[多模态](index.md) / 子主题导学 · 约 3 分钟 · 16 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 16 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Muse Glimmer 30B: An On-Device Agentic Model 基础模型 Meta Superintelligence Labs 2026-10-17 模型瞄准有32GB专用内存的端侧Agent：语言骨干用稠密Transformer而非MoE，在相同内存预算下用缩放实验选架构；约1.8B冻结视觉编码器支持图文交错输入。52层采用三层2048窗口局部注意力接一层全局注意力，32Q/2KV的GQA，局部层使用RoPE，全局层不再施加RoPE。训练从Muse Spark logits蒸馏起步，预训练末段切CE处理top-k截断偏差，之后权重平均和两阶段mid-training，再SFT、学生前缀上的OPD与多目标RL。 成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；“单卡可装下”不等于本项目低成本可完成训练和完整评测。BF16权重约55.7GB，量化LM目标低于20GB仍需KV、视觉编码器和drafter空间；长Agent轨迹与多模型对照远非一次前向。完整过程依赖前沿教师、多阶段大规模蒸馏、128K上下文与多域Agent环境，成本过高，不复现（审查 DONE）。本轮只取论文与仓库元数据，不下载权重、不开长推理或训练，不提供本地能力分数、GPU回执或Evolve整合声明。  网络架构 端侧多模态Agent模型 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-muse-glimmer-30b-d492f01f">Muse Glimmer 30B: An On-Device Agentic Model</h2>
<p class="ar-learning-card__meta">Meta Superintelligence Labs · 论文公开：2026-10-17</p>
<p><strong>方法要点：</strong>模型瞄准有32GB专用内存的端侧Agent：语言骨干用稠密Transformer而非MoE，在相同内存预算下用缩放实验选架构；约1.8B冻结视觉编码器支持图文交错输入。52层采用三层2048窗口局部注意力接一层全局注意力，32Q/2KV的GQA，局部层使用RoPE，全局层不再施加RoPE。训练从Muse Spark logits蒸馏起步，预训练末段切CE处理top-k截断偏差，之后权重平均和两阶段mid-training，再SFT、学生前缀上的OPD与多目标RL。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；“单卡可装下”不等于本项目低成本可完成训练和完整评测。BF16权重约55.7GB，量化LM目标低于20GB仍需KV、视觉编码器和drafter空间；长Agent轨迹与多模型对照远非一次前向。完整过程依赖前沿教师、多阶段大规模蒸馏、128K上下文与多域Agent环境，成本过高，不复现（审查 DONE）。本轮只取论文与仓库元数据，不下载权重、不开长推理或训练，不提供本地能力分数、GPU回执或Evolve整合声明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24628v1">原论文</a> · <a href="../../../../foundation-models/2610.24628-muse-glimmer-30b/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers 基础模型 Xi&#x27;an Jiaotong University 2026-10-16 扩散Transformer在每个去噪步重复执行昂贵的attention。本文观察到某些层/头中的高概率block关系在不同提示和seed下较稳定，因此一次离线校准即可得到静态稀疏支持；另用低分辨率全局KV分支补回分散上下文，无需改权重或采样schedule。原文Figure 4是两阶段方法总览，见Section4。 成本过高，不复现（审查 DONE）。不下载视频checkpoint，不跑完整生成或宣称端到端加速，禁止Evolve基于本诊断晋级。本地执行真实精确概率质量校准、最短前缀、静态mask复用、选中block实际gather计算、全局均值池化及稳定sigmoid融合。Python循环仅用于正确性，不是FlashAttention/Triton生产kernel，不以稀疏比例换算实测加速。  推理与系统效率 扩散模型稀疏注意力 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-sink-sparse-7f23b46b">Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers</h2>
<p class="ar-learning-card__meta">Xi&#x27;an Jiaotong University · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>扩散Transformer在每个去噪步重复执行昂贵的attention。本文观察到某些层/头中的高概率block关系在不同提示和seed下较稳定，因此一次离线校准即可得到静态稀疏支持；另用低分辨率全局KV分支补回分散上下文，无需改权重或采样schedule。原文Figure 4是两阶段方法总览，见Section4。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。不下载视频checkpoint，不跑完整生成或宣称端到端加速，禁止Evolve基于本诊断晋级。本地执行真实精确概率质量校准、最短前缀、静态mask复用、选中block实际gather计算、全局均值池化及稳定sigmoid融合。Python循环仅用于正确性，不是FlashAttention/Triton生产kernel，不以稀疏比例换算实测加速。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22975">原论文</a> · <a href="../../../../foundation-models/2610.22975-sink-sparse/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="AdaLoop: Thinking with the Vision Encoder 基础模型 Harvard University 2026-10-15 普通 VLM 对所有问题只编码图像一次。视觉 AdaLoop 保持预训练视觉权重冻结，以问题池化向量调制共享视觉块，再循环更新内部视觉状态。它将“看几次”与问题联系起来，而不是让语言模型独自承担全部推理。 单卡完整多臂成本过高，成本过高，不复现（审查 DONE）。临时线性分类器只供梯度诊断，不替代真实语言模型。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。使用3条随机视觉/问题 token、16维、2层、3次循环；冻结 attention/MLP 与 normalization，只训练问题池化、调制器和 connector。临时线性分类器只供梯度诊断，不替代真实语言模型。  多模态基础模型 问题条件视觉循环 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-adaloop-vision-ed1ee6f4">AdaLoop: Thinking with the Vision Encoder</h2>
<p class="ar-learning-card__meta">Harvard University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>普通 VLM 对所有问题只编码图像一次。视觉 AdaLoop 保持预训练视觉权重冻结，以问题池化向量调制共享视觉块，再循环更新内部视觉状态。它将“看几次”与问题联系起来，而不是让语言模型独自承担全部推理。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>单卡完整多臂成本过高，成本过高，不复现（审查 DONE）。临时线性分类器只供梯度诊断，不替代真实语言模型。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。使用3条随机视觉/问题 token、16维、2层、3次循环；冻结 attention/MLP 与 normalization，只训练问题池化、调制器和 connector。临时线性分类器只供梯度诊断，不替代真实语言模型。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21323">原论文</a> · <a href="../../../../foundation-models/2610.21323-adaloop-vision/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones 基础模型 University of Tübingen 2026-10-15 预训练 VLM 的语言层可以剪掉一段，再共享循环保留核心块；但直接手术会破坏语言能力及图文对齐。RR-VLM 用一个线性 adapter 融合 prelude 上下文与循环状态，并依次执行文本恢复、projector 对齐、全模型指令恢复；文本和最终阶段加入原始未剪模型蒸馏。 即使1.4B模型能放入单卡，完整恢复仍过重，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机6层、16维因果 Transformer，连续删除2层，保留1/2/1的 prelude/core/coda，核心循环3次。2条随机文本与视觉特征只检查结构和优化路径，不是模型能力数据。  多模态基础模型 剪枝与循环恢复 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-rr-vlm-3b3af466">Retrofitting Recurrent Vision-Language Models from Pretrained Backbones</h2>
<p class="ar-learning-card__meta">University of Tübingen · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>预训练 VLM 的语言层可以剪掉一段，再共享循环保留核心块；但直接手术会破坏语言能力及图文对齐。RR-VLM 用一个线性 adapter 融合 prelude 上下文与循环状态，并依次执行文本恢复、projector 对齐、全模型指令恢复；文本和最终阶段加入原始未剪模型蒸馏。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>即使1.4B模型能放入单卡，完整恢复仍过重，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机6层、16维因果 Transformer，连续删除2层，保留1/2/1的 prelude/core/coda，核心循环3次。2条随机文本与视觉特征只检查结构和优化路径，不是模型能力数据。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22075">原论文</a> · <a href="../../../../foundation-models/2610.22075-rr-vlm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="SoftCache: Adaptive Step Size Caching for Diffusion Transformers 基础模型 Tel Aviv University 2026-10-15 动态缓存通常只决定“刷新/重用”，仍沿固定时间网格走。SoftCache 将累计陈旧度距离阈值的 headroom 转成连续步长：缓存越可靠就走得更远。它用两次新鲜残差作时间外推，并重新排布剩余节点，使跳过的节点不会又被访问。 完整实验不适合当前单卡，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。固定 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1、seeds42/43/44。不下载生成模型。8维小 MLP 先做一次真实梯度更新，再在同一初值和20步网格上比较 SoftCache、hard-cache 与全量 Euler；所有差异包括负结果保留。  推理与系统效率 扩散缓存与自适应采样 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-softcache-596bc18d">SoftCache: Adaptive Step Size Caching for Diffusion Transformers</h2>
<p class="ar-learning-card__meta">Tel Aviv University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>动态缓存通常只决定“刷新/重用”，仍沿固定时间网格走。SoftCache 将累计陈旧度距离阈值的 headroom 转成连续步长：缓存越可靠就走得更远。它用两次新鲜残差作时间外推，并重新排布剩余节点，使跳过的节点不会又被访问。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验不适合当前单卡，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。固定 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1、seeds42/43/44。不下载生成模型。8维小 MLP 先做一次真实梯度更新，再在同一初值和20步网格上比较 SoftCache、hard-cache 与全量 Euler；所有差异包括负结果保留。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22369">原论文</a> · <a href="../../../../foundation-models/2610.22369-softcache/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="V-CoLA: Vision Token Compression with Linear Attention 多模态大模型 Alibaba Cloud Computing / Alibaba Group 2026-10-08 传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。方法见官方正文第 3 节。原论文架构图为Figure 5，比较原始混合模型与压缩后的前向路径；图像及版权属于原作者。 本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。原始 Qwen3.5-9B checkpoint 的视觉编码器和全部语言层已在真实 A100 执行；重要性不是随机分数、像素相似度或隐藏答案。仅 4 张公开训练留出图片，不代表完整 VLM 质量结论。本地对照口径：同一个冻结原始 Qwen3.5-9B，比较 dense、第一层保留 50% / 25% 且第 24 层后退出视觉的三条真实前向。固定公共 CIFAR-10 官方训练集尾部留出图像；不读取官方 test，不训练、不择优调参。  多模态推理效率 视觉 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-multimodal-models-vcola-a4fb5eab">V-CoLA: Vision Token Compression with Linear Attention</h2>
<p class="ar-learning-card__meta">Alibaba Cloud Computing / Alibaba Group · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。方法见官方正文第 3 节。原论文架构图为Figure 5，比较原始混合模型与压缩后的前向路径；图像及版权属于原作者。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。原始 Qwen3.5-9B checkpoint 的视觉编码器和全部语言层已在真实 A100 执行；重要性不是随机分数、像素相似度或隐藏答案。仅 4 张公开训练留出图片，不代表完整 VLM 质量结论。本地对照口径：同一个冻结原始 Qwen3.5-9B，比较 dense、第一层保留 50% / 25% 且第 24 层后退出视觉的三条真实前向。固定公共 CIFAR-10 官方训练集尾部留出图像；不读取官方 test，不训练、不择优调参。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11251">原论文</a> · <a href="../../../../multimodal-models/2610.11251-vcola/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning 多模态大模型 City University of Hong Kong / Zhejiang University 2026-10-08 一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。 scripts/validate_vimod_cuda_runtime.py 另外在同一真实 checkpoint 上执行 TRACE 三阶段 CUDA 梯度诊断。已实现 DART 容量约束/隐式梯度、总量整数舍入、置信度硬分组、八轮 Sinkhorn、共享 residual Value 编码；TRACE 层融合、四尺度 SSM、区域边界、HOLD/UPDATE 与真实 Fine KV 恢复。checkpoint backend 支持 SmolVLM/Idefics3，而非声称兼容 Qwen3-VL 的多模态 RoPE。  视觉 Token 压缩 动态证据恢复 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-multimodal-models-vimod-74b5d3f4">Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning</h2>
<p class="ar-learning-card__meta">City University of Hong Kong / Zhejiang University · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>scripts/validate_vimod_cuda_runtime.py 另外在同一真实 checkpoint 上执行 TRACE 三阶段 CUDA 梯度诊断。已实现 DART 容量约束/隐式梯度、总量整数舍入、置信度硬分组、八轮 Sinkhorn、共享 residual Value 编码；TRACE 层融合、四尺度 SSM、区域边界、HOLD/UPDATE 与真实 Fine KV 恢复。checkpoint backend 支持 SmolVLM/Idefics3，而非声称兼容 Qwen3-VL 的多模态 RoPE。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12060">原论文</a> · <a href="../../../../multimodal-models/2610.12060-vimod/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Video Encoders Built on Image Representations 基础模型 Stanford University 2026-10-05 逐帧图像编码保留可寻址的单帧证据，却产生很长的视觉序列。论文先逐帧冻结编码，再结合问题相关性、帧内多样性和跨帧对应，在固定预算内选择原始 token；可选 learned refiner 在选择完成后读取额外邻帧上下文，只更新已保留的锚点，不增加输出长度。 单张A100/A30或Mac不适合该完整campaign，因此完整 refiner/全表实验成本过高，不复现（审查 DONE）。CPU 单元测试核验最大 cosine、质量归一化、DPP 核、独立 determinant ratio、Schur residual、对应边阈值、pair complementarity/平局、奇数/零/满预算、原始源位置与中间 stream 恒等，以及非法 quota、NaN、重复身份、无答案输入合同。人工张量只用于这些公式测试，不作为视觉能力证据。  视频理解 训练免费视觉token选择 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-video-encoder-selection-2d465377">Video Encoders Built on Image Representations</h2>
<p class="ar-learning-card__meta">Stanford University · 论文公开：2026-10-05</p>
<p><strong>方法要点：</strong>逐帧图像编码保留可寻址的单帧证据，却产生很长的视觉序列。论文先逐帧冻结编码，再结合问题相关性、帧内多样性和跨帧对应，在固定预算内选择原始 token；可选 learned refiner 在选择完成后读取额外邻帧上下文，只更新已保留的锚点，不增加输出长度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>单张A100/A30或Mac不适合该完整campaign，因此完整 refiner/全表实验成本过高，不复现（审查 DONE）。CPU 单元测试核验最大 cosine、质量归一化、DPP 核、独立 determinant ratio、Schur residual、对应边阈值、pair complementarity/平局、奇数/零/满预算、原始源位置与中间 stream 恒等，以及非法 quota、NaN、重复身份、无答案输入合同。人工张量只用于这些公式测试，不作为视觉能力证据。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.06616">原论文</a> · <a href="../../../../foundation-models/2610.06616-video-encoder-selection/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs 基础模型 原文首页未列第一作者机构 2026-10-01 在同一注意力头内分别剪 V2V/T2V/T2T 路径，并为视觉、文本执行选择不同 FFN 通道；注意力剪枝后重新估计 FFN 重要性。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态大模型 结构剪枝 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-mwop-c24139ed">MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>在同一注意力头内分别剪 V2V/T2V/T2T 路径，并为视觉、文本执行选择不同 FFN 通道；注意力剪枝后重新估计 FFN 重要性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01434">原论文</a> · <a href="../../../../foundation-models/2610.01434-mwop/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VETO: Video Efficient Token Optimization for Vision Language Models 基础模型 National Taiwan University 2026-10-01 先在帧内合并语义近邻 token，再对压缩后的 frame representation 做跨帧去冗余；空间先行显著降低全局时间匹配成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  视频 VLM Token 压缩 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-veto-75da8cb3">VETO: Video Efficient Token Optimization for Vision Language Models</h2>
<p class="ar-learning-card__meta">National Taiwan University · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>先在帧内合并语义近邻 token，再对压缩后的 frame representation 做跨帧去冗余；空间先行显著降低全局时间匹配成本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01785">原论文</a> · <a href="../../../../foundation-models/2610.01785-veto/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="HAWK: Rethinking Multimodal Drafting for Speculative Decoding 基础模型 原文首页未列第一作者机构 2026-09-30 从 target 多层隐藏状态学习混合，给浅层 drafter 提供压缩视觉表示，并用 drafter 自己提议后的 shifted trajectory 训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行层混合与 shifted target 隔离；未实现专用解码 kernel。执行层混合与 shifted target 隔离；未实现专用解码 kernel。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态推理 投机解码 蒸馏 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-hawk-938adaa0">HAWK: Rethinking Multimodal Drafting for Speculative Decoding</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-09-30</p>
<p><strong>方法要点：</strong>从 target 多层隐藏状态学习混合，给浅层 drafter 提供压缩视觉表示，并用 drafter 自己提议后的 shifted trajectory 训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行层混合与 shifted target 隔离；未实现专用解码 kernel。执行层混合与 shifted target 隔离；未实现专用解码 kernel。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00623">原论文</a> · <a href="../../../../foundation-models/2610.00623-hawk/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection 多模态大模型 Sichuan University 2026-09-15 把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视觉 Token 选择 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-multimodal-models-stacktok-c22648c2">StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection</h2>
<p class="ar-learning-card__meta">Sichuan University · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16841">原论文</a> · <a href="../../../../multimodal-models/2609.16841-stacktok/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs 多模态大模型 University of Science and Technology of China 2026-09-15 先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视频理解 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-multimodal-models-videomm-bc3e057a">VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16722">原论文</a> · <a href="../../../../multimodal-models/2609.16722-videomm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding 基础模型 Queen Mary University of London 2026-09-10 视频只做一次 caption memory；visual-need router 判断文本证据不足时，才在固定预算内读取相关帧。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  长视频理解 视觉预算路由 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-frames-on-demand-ec1c6746">Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding</h2>
<p class="ar-learning-card__meta">Queen Mary University of London · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>视频只做一次 caption memory；visual-need router 判断文本证据不足时，才在固定预算内读取相关帧。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11899">原论文</a> · <a href="../../../../foundation-models/2609.11899-frames-on-demand/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="OmniKVQuant: KV Cache Quantization for Omni-LLMs 基础模型 KAIST 2026-09-10 按短时间窗确定 key 量化范围，并按模态分别旋转 value，处理 temporal drift 与异构几何。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  多模态推理 KV Cache 量化 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-omnikvquant-a8e321c1">OmniKVQuant: KV Cache Quantization for Omni-LLMs</h2>
<p class="ar-learning-card__meta">KAIST · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>按短时间窗确定 key 量化范围，并按模态分别旋转 value，处理 temporal drift 与异构几何。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11582">原论文</a> · <a href="../../../../foundation-models/2609.11582-omnikvquant/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference 基础模型 Sun Yat-sen University 2026-08-27 VLM 的视觉 token 一方面在 prefill 阶段带来大量计算，另一方面在抽取阶段仍会保留大量与问题无关的内容。PACE 将两个阶段拆开处理：APC 用浅层 ViT preview 同时估计全局语义密度和局部细节，按图像难度自适应缩放；DDAE 再融合 LLM 与视觉编码器的注意力，以置信度决定两种证据各占多少权重，而不是固定只信一种注意力图。 复现级别：核心机制 + 真实 checkpoint 公开数据验证。复现级别：核心机制 + 真实 checkpoint 公开数据验证。APC、DDAE 公式和 Qwen2.5-VL 自适应分辨率路径均实际执行；没有把小样本结果冒充论文完整 benchmark。本地正式结果是小型 RealWorldQA checkpoint smoke，不覆盖论文完整 11 个 benchmark；当前 runner 实测 APC 主路径，DDAE 以独立公式和单测验证，尚未复制作者约 2,000 行的模型 fork 与定制 kernel。本地对照口径：基线是同一 Qwen2.5-VL checkpoint 的原始视觉分辨率；  multimodal-foundation-model visual-token-compression inference-serving 多模态 视觉证据预算：选 Token、选帧与按需回看">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<h2 id="paper-foundation-models-pace-vlm-f64143ef">PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference</h2>
<p class="ar-learning-card__meta">Sun Yat-sen University · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>VLM 的视觉 token 一方面在 prefill 阶段带来大量计算，另一方面在抽取阶段仍会保留大量与问题无关的内容。PACE 将两个阶段拆开处理：APC 用浅层 ViT preview 同时估计全局语义密度和局部细节，按图像难度自适应缩放；DDAE 再融合 LLM 与视觉编码器的注意力，以置信度决定两种证据各占多少权重，而不是固定只信一种注意力图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 真实 checkpoint 公开数据验证。复现级别：核心机制 + 真实 checkpoint 公开数据验证。APC、DDAE 公式和 Qwen2.5-VL 自适应分辨率路径均实际执行；没有把小样本结果冒充论文完整 benchmark。本地正式结果是小型 RealWorldQA checkpoint smoke，不覆盖论文完整 11 个 benchmark；当前 runner 实测 APC 主路径，DDAE 以独立公式和单测验证，尚未复制作者约 2,000 行的模型 fork 与定制 kernel。本地对照口径：基线是同一 Qwen2.5-VL checkpoint 的原始视觉分辨率；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27206">原论文</a> · <a href="../../../../reproductions/2608.27206-pace-vlm/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
