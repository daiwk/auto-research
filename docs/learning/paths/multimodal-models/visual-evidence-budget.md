---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 视觉证据预算：选 Token、选帧与按需回看

[多模态](index.md) / 16 个问题 · 16 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">16 个问题 · 16 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muse-glimmer-30b" data-paper-title="Muse Glimmer 30B: An On-Device Agentic Model" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Muse Glimmer 30B: An On-Device Agentic Model 基础模型 Meta Superintelligence Labs 2026-10-17 模型瞄准有32GB专用内存的端侧Agent：语言骨干用稠密Transformer而非MoE，在相同内存预算下用缩放实验选架构；约1.8B冻结视觉编码器支持图文交错输入。52层采用三层2048窗口局部注意力接一层全局注意力，32Q/2KV的GQA，局部层使用RoPE，全局层不再施加RoPE。训练从Muse Spark logits蒸馏起步，预训练末段切CE处理top-k截断偏差，之后权重平均和两阶段mid-training，再SFT、学生前缀上的OPD与多目标RL。 成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；“单卡可装下”不等于本项目低成本可完成训练和完整评测。BF16权重约55.7GB，量化LM目标低于20GB仍需KV、视觉编码器和drafter空间；长Agent轨迹与多模型对照远非一次前向。完整过程依赖前沿教师、多阶段大规模蒸馏、128K上下文与多域Agent环境，成本过高，不复现（审查 DONE）。本轮只取论文与仓库元数据，不下载权重、不开长推理或训练，不提供本地能力分数、GPU回执或Evolve整合声明。  网络架构 端侧多模态Agent模型 多模态 视觉证据预算：选 Token、选帧与按需回看 三层局部注意力接一层全局注意力，为什么不同于把整个模型窗口都缩短？ 局部层限制多数层的读写范围以节省成本，全局层仍能在更长范围交换信息，因此模型并非每层都永久看不到远处内容。GQA 又减少 KV 头数，针对另一部分缓存成本；这些结构取舍不等于已经复现整套蒸馏、后训练和端侧运行效果。 例如远处的标题可在全局层影响当前段落，而相邻句子的加工由局部层承担；全部改成短窗口会失去这条长程通路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-muse-glimmer-30b-d492f01f" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sink-sparse" data-paper-title="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers 基础模型 Xi&#x27;an Jiaotong University 2026-10-16 扩散Transformer在每个去噪步重复执行昂贵的attention。本文观察到某些层/头中的高概率block关系在不同提示和seed下较稳定，因此一次离线校准即可得到静态稀疏支持；另用低分辨率全局KV分支补回分散上下文，无需改权重或采样schedule。原文Figure 4是两阶段方法总览，见Section4。 成本过高，不复现（审查 DONE）。不下载视频checkpoint，不跑完整生成或宣称端到端加速，禁止Evolve基于本诊断晋级。本地执行真实精确概率质量校准、最短前缀、静态mask复用、选中block实际gather计算、全局均值池化及稳定sigmoid融合。Python循环仅用于正确性，不是FlashAttention/Triton生产kernel，不以稀疏比例换算实测加速。  推理与系统效率 扩散模型稀疏注意力 多模态 视觉证据预算：选 Token、选帧与按需回看 全局补偿分支为什么连 sink 块也池化，而不是只处理被稀疏分支漏掉的块？ 补偿分支提供低分辨率的全局背景，其定义覆盖全部 token；稀疏分支则保留选中关系的精细计算。两者按各自归一化量融合，不是把遗漏部分简单相加。若擅自排除 sink，就改变了补偿分布，离线校准得到的静态支持也不能在测试题上重新挑选。 例如稀疏分支精读中心区域，全局分支仍粗读整张图包括中心；它补的是全局上下文，不是把剩余区域拼成第二张图。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-sink-sparse-7f23b46b" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adaloop-vision" data-paper-title="AdaLoop: Thinking with the Vision Encoder" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="AdaLoop: Thinking with the Vision Encoder 基础模型 Harvard University 2026-10-15 普通 VLM 对所有问题只编码图像一次。视觉 AdaLoop 保持预训练视觉权重冻结，以问题池化向量调制共享视觉块，再循环更新内部视觉状态。它将“看几次”与问题联系起来，而不是让语言模型独自承担全部推理。 单卡完整多臂成本过高，成本过高，不复现（审查 DONE）。临时线性分类器只供梯度诊断，不替代真实语言模型。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。使用3条随机视觉/问题 token、16维、2层、3次循环；冻结 attention/MLP 与 normalization，只训练问题池化、调制器和 connector。临时线性分类器只供梯度诊断，不替代真实语言模型。  多模态基础模型 问题条件视觉循环 多模态 视觉证据预算：选 Token、选帧与按需回看 视觉编码器权重被冻结时，反复循环为什么仍可能改变模型看到的内容？ 冻结权重不等于冻结视觉状态。每轮把更新后的状态送回共享块，并由问题向量调制计算，因此同一组参数可以围绕问题逐步重新组织表示。深度监督约束不同循环的答案，停止规则只能比较已产生预测，不能偷偷依赖正确答案。 例如同一幅图先问物体种类、再问遮挡关系，问题调制可让循环关注不同信息；这并非每轮都换一个新编码器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-adaloop-vision-ed1ee6f4" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rr-vlm" data-paper-title="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Retrofitting Recurrent Vision-Language Models from Pretrained Backbones 基础模型 University of Tübingen 2026-10-15 预训练 VLM 的语言层可以剪掉一段，再共享循环保留核心块；但直接手术会破坏语言能力及图文对齐。RR-VLM 用一个线性 adapter 融合 prelude 上下文与循环状态，并依次执行文本恢复、projector 对齐、全模型指令恢复；文本和最终阶段加入原始未剪模型蒸馏。 即使1.4B模型能放入单卡，完整恢复仍过重，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。seeds42/43/44；revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机6层、16维因果 Transformer，连续删除2层，保留1/2/1的 prelude/core/coda，核心循环3次。2条随机文本与视觉特征只检查结构和优化路径，不是模型能力数据。  多模态基础模型 剪枝与循环恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 共享循环块为什么能减少存储层数，却不保证减少执行深度？ 同一核心块重复执行多次只保存一份参数，但总计算仍包含每次循环。剪层还会破坏原有语言能力和图文接口，所以需要先恢复文本、再对齐 projector、再做指令恢复；参数变少和推理步数变少是两个不同目标，不能混报为同一种加速。 例如五层核心循环三次相当于执行十五次块计算，却只存五层核心权重；循环次数越多，存储优势未必变成延迟优势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-rr-vlm-3b3af466" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:softcache" data-paper-title="SoftCache: Adaptive Step Size Caching for Diffusion Transformers" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="SoftCache: Adaptive Step Size Caching for Diffusion Transformers 基础模型 Tel Aviv University 2026-10-15 动态缓存通常只决定“刷新/重用”，仍沿固定时间网格走。SoftCache 将累计陈旧度距离阈值的 headroom 转成连续步长：缓存越可靠就走得更远。它用两次新鲜残差作时间外推，并重新排布剩余节点，使跳过的节点不会又被访问。 完整实验不适合当前单卡，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。固定 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1、seeds42/43/44。不下载生成模型。8维小 MLP 先做一次真实梯度更新，再在同一初值和20步网格上比较 SoftCache、hard-cache 与全量 Euler；所有差异包括负结果保留。  推理与系统效率 扩散缓存与自适应采样 多模态 视觉证据预算：选 Token、选帧与按需回看 SoftCache 的步长控制为什么不只是“这一层缓存刷新还是复用”？ 普通缓存沿固定时间节点选择是否重算，SoftCache 还依据陈旧度余量改变前进距离，并重新安排剩余节点。因此少算一次不应之后又访问被跳过的节点。残差外推需要新鲜锚点支撑，在变化太快或早期受限区域不能无条件继续扩大步长。 例如原计划经过十个去噪节点，可靠缓存允许跨过中间两个节点；后续网格也要重排，不能绕一圈再把它们算回来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-softcache-596bc18d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vcola" data-paper-title="V-CoLA: Vision Token Compression with Linear Attention" data-learning-pending="false" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="V-CoLA: Vision Token Compression with Linear Attention 多模态大模型 Alibaba Cloud Computing / Alibaba Group 2026-10-08 传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。方法见官方正文第 3 节。原论文架构图为Figure 5，比较原始混合模型与压缩后的前向路径；图像及版权属于原作者。 本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。本地定位：L1 核心机制诊断，非论文完整 benchmark 复现。原始 Qwen3.5-9B checkpoint 的视觉编码器和全部语言层已在真实 A100 执行；重要性不是随机分数、像素相似度或隐藏答案。仅 4 张公开训练留出图片，不代表完整 VLM 质量结论。本地对照口径：同一个冻结原始 Qwen3.5-9B，比较 dense、第一层保留 50% / 25% 且第 24 层后退出视觉的三条真实前向。固定公共 CIFAR-10 官方训练集尾部留出图像；不读取官方 test，不训练、不择优调参。  多模态推理效率 视觉 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 为什么 Gated DeltaNet 的视觉压缩不能直接照搬 softmax attention 权重？ 线性递归状态并不显式保存同样的完整注意力矩阵，其信息由状态更新与遗忘共同决定。V-CoLA 用最终状态能否回读某 token 衡量长期保留，再测短窗口 query 对更新的响应变化补充独特性，之后连续分块合并；这些分数并非普通相似度排序。 例如一个 patch 刚写入时很显眼，却在后续状态中被覆盖，最终回读分数就会降低；单看当时的局部相似度会漏掉遗忘。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-multimodal-models-vcola-a4fb5eab" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:vimod" data-paper-title="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning" data-learning-pending="false" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning 多模态大模型 City University of Hong Kong / Zhejiang University 2026-10-08 一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。 scripts/validate_vimod_cuda_runtime.py 另外在同一真实 checkpoint 上执行 TRACE 三阶段 CUDA 梯度诊断。已实现 DART 容量约束/隐式梯度、总量整数舍入、置信度硬分组、八轮 Sinkhorn、共享 residual Value 编码；TRACE 层融合、四尺度 SSM、区域边界、HOLD/UPDATE 与真实 Fine KV 恢复。checkpoint backend 支持 SmolVLM/Idefics3，而非声称兼容 Qwen3-VL 的多模态 RoPE。  视觉 Token 压缩 动态证据恢复 多模态 视觉证据预算：选 Token、选帧与按需回看 TRACE 的 UPDATE 为什么替换活跃 Fine 工作集，而不是不断累加？ 不断累加会使活跃上下文随推理增长，失去预算约束。ViMoD 让 Coarse 表示持续存在，而 Fine 细节按当前生成历史保持或替换，原始细节仍可恢复；被替换的是当前参与注意力的工作集，不是把底层 Fine 缓存永久删除。 例如先取左侧标签，再转向右侧仪表时替换细节工作集；粗图仍在，之后也能按需重新取回左侧标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-multimodal-models-vimod-74b5d3f4" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:video-encoder-selection" data-paper-title="Video Encoders Built on Image Representations" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Video Encoders Built on Image Representations 基础模型 Stanford University 2026-10-05 逐帧图像编码保留可寻址的单帧证据，却产生很长的视觉序列。论文先逐帧冻结编码，再结合问题相关性、帧内多样性和跨帧对应，在固定预算内选择原始 token；可选 learned refiner 在选择完成后读取额外邻帧上下文，只更新已保留的锚点，不增加输出长度。 单张A100/A30或Mac不适合该完整campaign，因此完整 refiner/全表实验成本过高，不复现（审查 DONE）。CPU 单元测试核验最大 cosine、质量归一化、DPP 核、独立 determinant ratio、Schur residual、对应边阈值、pair complementarity/平局、奇数/零/满预算、原始源位置与中间 stream 恒等，以及非法 quota、NaN、重复身份、无答案输入合同。人工张量只用于这些公式测试，不作为视觉能力证据。  视频理解 训练免费视觉token选择 多模态 视觉证据预算：选 Token、选帧与按需回看 learned refiner 为什么只更新保留下来的锚点，而不再增加视觉 Token？ 选择阶段先在固定预算内保留原始可寻址证据，refiner 随后让这些锚点读取邻帧上下文来改善表示。这样增加的是每个保留位置的信息，而非输出序列长度；若不断追加邻帧 token，就破坏固定预算，也混淆了选择与上下文补充两项收益。 例如先保留十个关键 patch，refiner 为它们读取邻帧运动线索后仍输出十个；不能再追加二十个邻帧位置并声称预算不变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-video-encoder-selection-2d465377" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mwop" data-paper-title="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs 基础模型 原文首页未列第一作者机构 2026-10-01 在同一注意力头内分别剪 V2V/T2V/T2T 路径，并为视觉、文本执行选择不同 FFN 通道；注意力剪枝后重新估计 FFN 重要性。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态大模型 结构剪枝 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 为什么剪完注意力路径后，还要重新估计 FFN 通道的重要性？ 注意力剪枝改变了进入 FFN 的信息分布，原先的重要性排序可能已经过时。MWOP 还把视觉到视觉、文本到视觉等路径和不同模态的 FFN 通道分开处理，避免用一个总分掩盖模态差异；剪枝后的质量与真实速度仍要分别验证。 例如删除部分文本读取视觉的路径后，一些负责融合视觉的 FFN 通道贡献会变化，不能继续沿用手术前的通道排名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-mwop-c24139ed" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:veto" data-paper-title="VETO: Video Efficient Token Optimization for Vision Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VETO: Video Efficient Token Optimization for Vision Language Models 基础模型 National Taiwan University 2026-10-01 先在帧内合并语义近邻 token，再对压缩后的 frame representation 做跨帧去冗余；空间先行显著降低全局时间匹配成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  视频 VLM Token 压缩 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 先帧内合并、再跨帧去冗余，为什么不是任意可交换的两步？ 帧内合并先减少每帧的候选数量，让跨帧匹配面对更短的表示，降低时间维比较成本。若先在所有原始 patch 间做全局时间匹配，就已经支付了更大的搜索开销，得到的对应关系也可能不同；两步顺序本身就是机制的一部分。 例如每帧一百个 patch 先压成二十个，再找相邻帧重复内容；反过来先匹配全部原始 patch 就省不下同一部分计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-veto-75da8cb3" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hawk" data-paper-title="HAWK: Rethinking Multimodal Drafting for Speculative Decoding" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="HAWK: Rethinking Multimodal Drafting for Speculative Decoding 基础模型 原文首页未列第一作者机构 2026-09-30 从 target 多层隐藏状态学习混合，给浅层 drafter 提供压缩视觉表示，并用 drafter 自己提议后的 shifted trajectory 训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行层混合与 shifted target 隔离；未实现专用解码 kernel。执行层混合与 shifted target 隔离；未实现专用解码 kernel。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态推理 投机解码 蒸馏 多模态 视觉证据预算：选 Token、选帧与按需回看 为什么 drafter 要在自己提出 token 后的 shifted trajectory 上训练？ 草稿会把系统带到自己的前缀分布，始终在教师理想前缀训练会掩盖这些偏移。移位后的轨迹让监督与实际提议后的状态对齐，多层教师状态混合再提供压缩视觉信息；草稿是否被接纳仍须目标模型验证，不能靠训练损失替代接受率测量。 例如草稿第一步选了另一种说法，第二步就应在这个真实前缀上学习目标分布，而非假装第一步与教师完全相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-hawk-938adaa0" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:stacktok" data-paper-title="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection" data-learning-pending="false" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection 多模态大模型 Sichuan University 2026-09-15 把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视觉 Token 选择 推理效率 多模态 视觉证据预算：选 Token、选帧与按需回看 为何相关性最高的视觉 Token 不一定组成最好的固定预算子集？ 它们可能集中在同一区域，重复提供相同信息而遗漏全图结构。StackTok 以相关性为主要目标，并用随预算变化的覆盖参考检查当前缺口，再切换选取准则；覆盖并非固定比例的装饰项，不同问题与预算需要不同程度的支持。 例如问整幅场景布局时，只选人物脸部的一堆高相关 patch 可能漏掉门的位置；补覆盖能保留另一类必要证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-multimodal-models-stacktok-c22648c2" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:videomm" data-paper-title="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs" data-learning-pending="false" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs 多模态大模型 University of Science and Technology of China 2026-09-15 先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  视频理解 Token 压缩 多模态 视觉证据预算：选 Token、选帧与按需回看 低分辨率 Macro Proxy 已经定位区域，为什么还需要按条件激活 Micro Tokens？ 粗粒度表示能快速筛去大量无关内容，却可能无法区分小字或细微动作。只有宏观证据不足时才追加高保真细节，可以把预算集中到不确定之处；这要求保留粗到细的取证路径，而不是把所有问题都固定压到同一份低清摘要。 例如粗看知道有人举牌，问是否举牌可直接回答；问牌上数字则可能需要激活对应区域的高分辨率 token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-multimodal-models-videomm-bc3e057a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frames-on-demand" data-paper-title="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding 基础模型 Queen Mary University of London 2026-09-10 视频只做一次 caption memory；visual-need router 判断文本证据不足时，才在固定预算内读取相关帧。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  长视频理解 视觉预算路由 多模态 视觉证据预算：选 Token、选帧与按需回看 先写 caption memory 后，为什么还需要 visual-need router？ 文字记忆能覆盖粗粒度事件，却可能遗漏以后问题需要的细节。路由器判断现有文字证据是否足够，只有不足时才花视觉预算读取相关帧；这样控制的是追加取证的成本，不是把描述当成无损视频，也不能把路由决定本身视为答案正确。 例如记忆只写“有人拿起盒子”，问盒子上的编号时就需回读帧；问是否有人取物则可能直接利用已有文字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-frames-on-demand-ec1c6746" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:omnikvquant" data-paper-title="OmniKVQuant: KV Cache Quantization for Omni-LLMs" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="OmniKVQuant: KV Cache Quantization for Omni-LLMs 基础模型 KAIST 2026-09-10 按短时间窗确定 key 量化范围，并按模态分别旋转 value，处理 temporal drift 与异构几何。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  多模态推理 KV Cache 量化 多模态 视觉证据预算：选 Token、选帧与按需回看 多模态 KV 为什么不宜共享一套全局量化范围和旋转？ Key 的数值分布可能随时间漂移，长期统一范围会让局部有效精度变差；不同模态 Value 的几何结构也不一致。短窗范围与模态专属旋转分别处理时间变化和模态差异，不能把两种校准合并成一套静态规则后仍假设误差同样可控。 例如前段音频 Key 的幅度较小、后段视频 Key 较大，全局范围可能挤压前者精度；Value 也需按模态检查结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-omnikvquant-a8e321c1" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pace-vlm" data-paper-title="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/visual-evidence-budget" data-search="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference 基础模型 Sun Yat-sen University 2026-08-27 VLM 的视觉 token 一方面在 prefill 阶段带来大量计算，另一方面在抽取阶段仍会保留大量与问题无关的内容。PACE 将两个阶段拆开处理：APC 用浅层 ViT preview 同时估计全局语义密度和局部细节，按图像难度自适应缩放；DDAE 再融合 LLM 与视觉编码器的注意力，以置信度决定两种证据各占多少权重，而不是固定只信一种注意力图。 复现级别：核心机制 + 真实 checkpoint 公开数据验证。复现级别：核心机制 + 真实 checkpoint 公开数据验证。APC、DDAE 公式和 Qwen2.5-VL 自适应分辨率路径均实际执行；没有把小样本结果冒充论文完整 benchmark。本地正式结果是小型 RealWorldQA checkpoint smoke，不覆盖论文完整 11 个 benchmark；当前 runner 实测 APC 主路径，DDAE 以独立公式和单测验证，尚未复制作者约 2,000 行的模型 fork 与定制 kernel。本地对照口径：基线是同一 Qwen2.5-VL checkpoint 的原始视觉分辨率；  multimodal-foundation-model visual-token-compression inference-serving 多模态 视觉证据预算：选 Token、选帧与按需回看 PACE 为什么把图像缩放与问题相关 Token 抽取拆成两个阶段？ 缩放先控制视觉输入本身的成本，抽取再控制哪些内容进入后续处理；只在末端丢 token，已经支付的编码成本不会消失。浅层预览估计图像难度，抽取又按置信度融合语言与视觉注意力，避免始终盲信单一路径或固定压缩所有图像。 例如空白背景图可先缩小，密集菜单则保留较多细节；之后再根据问题选择相关区域，而非两张图都按同一比例裁减。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉证据预算：选 Token、选帧与按需回看</a></p>
<span id="paper-foundation-models-pace-vlm-f64143ef" class="ar-learning-paper-anchor"></span>
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
