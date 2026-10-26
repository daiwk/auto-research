---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 按需计算：专家、弹性深宽与查表记忆

[基础模型](index.md) / 26 个问题 · 26 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">26 个问题 · 26 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mirror-moe" data-paper-title="Rethinking Routing Exploration in Modern Mixture-of-Experts" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Rethinking Routing Exploration in Modern Mixture-of-Experts 基础模型 ETH Zurich 2026-10-15 共享专家占据较多输出后，改变路由专家带来的表征差异减弱，而细粒度分割又扩大组合空间。MirrorMoE 不简单增噪，而是以镜像选择暂时抑制部分专家，随训练退火恢复普通路由。主源是 §3 的公式 3–6。 现有单 A100/A30/Mac 不运行此完整预训练，成本过高，不复现（审查 DONE）。CUDA 诊断记录与真实GPU回执列出设备与源码 hash。revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1；无 checkpoint、公共语料或能力 benchmark。固定种子 42/43/44 初始化 8 维、6 个可路由专家、2 个共享专家、top-3 的真实可训练小网络。每 seed 仅一个 SGD 更新核验梯度，不是语言模型训练。  网络架构 混合专家路由 基础模型 按需计算：专家、弹性深宽与查表记忆 MirrorMoE用镜像概率选专家，最终输出也要用这份混合概率加权吗？ 不应把选择与输出权重混为一谈。方法把原路由与反向logit产生的镜像概率混合，用于探索选择；被选路由专家的输出仍按原概率加权，并随训练逐步退出镜像探索。负载统计也区分实际派发和原概率。改成用混合概率输出或随意重归一化会改变论文机制。 教学例子：某专家原概率较小，镜像选择让它偶尔被执行；这不代表它的输出权重也突然变大。获得训练曝光和主导最终输出是两件事。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-mirror-moe-43695dbb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2750f3a34fee37eb">MirrorMoE用镜像概率选专家，最终输出也要用这份混合概率加权吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amirror-moe">Rethinking Routing Exploration in Modern Mixture-of-Experts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ETH Zurich</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不应把选择与输出权重混为一谈。方法把原路由与反向logit产生的镜像概率混合，用于探索选择；被选路由专家的输出仍按原概率加权，并随训练逐步退出镜像探索。负载统计也区分实际派发和原概率。改成用混合概率输出或随意重归一化会改变论文机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某专家原概率较小，镜像选择让它偶尔被执行；这不代表它的输出权重也突然变大。获得训练曝光和主导最终输出是两件事。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22353">原论文</a> · <a href="../../../../foundation-models/2610.22353-mirror-moe/">实现解读</a> · <a href="#qa-2750f3a34fee37eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:novelty-patching" data-paper-title="Patch where the text is new: a compression view of where byte-level models should spend compute" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Patch where the text is new: a compression view of where byte-level models should spend compute 基础模型 Independent Researcher, Chile 2026-10-15 Byte-level 模型按 patch 调用全局模型。本文用近期重复程度预测替代纯熵边界；离线计算匹配标签，在线只查前两字节。主源位置为 §3 方法、§4-7 结果及负结果、§8 限制和 Code and data。 这一多臂完整链路超出单张 A100/A30 或 Mac 的本轮低成本预算，故成本过高，不复现（审查 DONE）。仅实现训练标签、两级低频回退、训练集阈值和严格因果边界。原文 4 MB 拟表在本次缩为 262,144 byte 的已有公开训练文本；不训练 BLT、不评测答案准确率。  字节级模型 因果patch边界 基础模型 按需计算：专家、弹性深宽与查表记忆 Novelty Patching离线使用匹配长度作标签，线上为什么只查前两个byte？ 较长的近期重复匹配用于训练新颖度目标，在线则用由历史前缀字节索引的统计表预测边界。它把昂贵或涉及待处理片段的标签构造与部署决策分开；低计数情况还要按规则回退。不能把离线可计算的真实匹配长度直接当作推理时已知的未来信息。 教学例子：训练时可回看一段字节是否复用了近期模板；生成时尚不知道后面的完整片段，只能由已生成的前两个字节查统计预期，决定是否开启新patch。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-novelty-patching-3454dd1e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b724f96d1642e069">Novelty Patching离线使用匹配长度作标签，线上为什么只查前两个byte？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anovelty-patching">Patch where the text is new: a compression view of where byte-level models should spend compute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher, Chile</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>较长的近期重复匹配用于训练新颖度目标，在线则用由历史前缀字节索引的统计表预测边界。它把昂贵或涉及待处理片段的标签构造与部署决策分开；低计数情况还要按规则回退。不能把离线可计算的真实匹配长度直接当作推理时已知的未来信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时可回看一段字节是否复用了近期模板；生成时尚不知道后面的完整片段，只能由已生成的前两个字节查统计预期，决定是否开启新patch。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22100">原论文</a> · <a href="../../../../foundation-models/2610.22100-novelty-patching/">实现解读</a> · <a href="#qa-b724f96d1642e069">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:msar" data-paper-title="Multi-Stream Attention Residuals" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Multi-Stream Attention Residuals 基础模型 Shanghai Jiao Tong University 2026-10-09 标准残差把历史更新压成一个累加向量；AttnRes 能逐层检索，但只有一个深度注意力流。MSAR 保留每个完整 hidden 向量，用序列上下文产生不同尺度的完整视图，再对每个流独立做深度 softmax。与切分通道的多头不同，它不破坏 value 的全维表示。Block MSAR 只持久保存 embedding、已完成 block 的单流摘要和当前 block 的部分和，消费时再展开；不会把所有卷积视图永久写回。卷积 kernel 为 4/8/12，加 identity 流共四流； 正式本地相对收益不适用，当前只有机制诊断，少量步骤/单 seed 不能支持稳定提升结论。本地对照口径：匹配的真实 dense causal Transformer 为基线，MSAR 为实验组；正式本地相对收益不适用，当前只有机制诊断，少量步骤/单 seed 不能支持稳定提升结论。  llm-architecture depth-attention residual-mixing 基础模型 按需计算：专家、弹性深宽与查表记忆 MSAR的多流与普通多头切分通道有什么不同，哪一步需要softmax归一化？ 每个MSAR流都保留完整hidden向量，只用不同序列尺度形成视图，再分别在深度来源上做softmax检索；它不是把value通道切成几份。各流取回结果后由sigmoid mixer融合，流间权重不要求和为1。把流融合误换成softmax，或永久缓存所有展开视图，都会改变方法与成本。 教学例子：同一段表示可以形成原始、短程和长程三个完整视图；每个视图各自选择哪些历史层重要，再独立控制输出量，而不是先把向量的不同三段分给它们。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-msar-f6753b95" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9afa7d02b04dbe76">MSAR的多流与普通多头切分通道有什么不同，哪一步需要softmax归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amsar">Multi-Stream Attention Residuals</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个MSAR流都保留完整hidden向量，只用不同序列尺度形成视图，再分别在深度来源上做softmax检索；它不是把value通道切成几份。各流取回结果后由sigmoid mixer融合，流间权重不要求和为1。把流融合误换成softmax，或永久缓存所有展开视图，都会改变方法与成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一段表示可以形成原始、短程和长程三个完整视图；每个视图各自选择哪些历史层重要，再独立控制输出量，而不是先把向量的不同三段分给它们。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13630">原论文</a> · <a href="../../../../reproductions/2610.13630-msar/">实现解读</a> · <a href="#qa-9afa7d02b04dbe76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:cots" data-paper-title="CoTS: Competitive Token Selection for Latent Reasoning in Large Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="CoTS: Competitive Token Selection for Latent Reasoning in Large Language Models 基础模型 Xiaomi AI Lab 2026-10-08 连续 reasoning 的 soft token 可能偏离离散轨迹。CoTS 用 top-2 概率竞争分配 soft 混合强度，保留 sampled token 至少半数权重，并在结束推理后锁定纯离散输出。主源为 §3.1-3.3 的公式 1-6；实验配置和消融见 §4。 按公开配置，完整研究超出本轮单 A100/A30 或 Mac 低成本预算，成本过高，不复现（审查 DONE）。只实现概率竞争、top-k soft embedding、离散锚点、逐样本不可逆 phase-lock 和 EOS 状态；sampled token 可在 top-k 之外。输入概率与 embedding 的 autograd 链路均保留，未转 numpy、未以 straight-through 伪梯度代替。保护 token ID 与 tokenizer/end-think ID 由调用方明确提供，不猜默认表。  连续推理 概率竞争与离散锚点 基础模型 按需计算：专家、弹性深宽与查表记忆 CoTS混入soft token后，怎样避免把实际采样的离散轨迹完全冲掉？ 混合强度由top-2概率的竞争程度决定，并被限制在不超过一半；所以即使采样token不在soft集合中，其embedding也至少占半数。模型发出结束推理标记后关闭soft路径并保持离散输出，特定格式保护还可只影响当前步。它不是用概率均值无限延续替代实际轨迹。 教学例子：top-2概率为0.6与0.4时，基础混合强度为0.4，采样token仍占0.6；若第一名远高于第二名，soft混合会更弱，而不是统一采用固定一半。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-cots-9dd74b8e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-54d3e8b20e547876">CoTS混入soft token后，怎样避免把实际采样的离散轨迹完全冲掉？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acots">CoTS: Competitive Token Selection for Latent Reasoning in Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaomi AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>混合强度由top-2概率的竞争程度决定，并被限制在不超过一半；所以即使采样token不在soft集合中，其embedding也至少占半数。模型发出结束推理标记后关闭soft路径并保持离散输出，特定格式保护还可只影响当前步。它不是用概率均值无限延续替代实际轨迹。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>top-2概率为0.6与0.4时，基础混合强度为0.4，采样token仍占0.6；若第一名远高于第二名，soft混合会更弱，而不是统一采用固定一半。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20642">原论文</a> · <a href="../../../../foundation-models/2610.20642-cots/">实现解读</a> · <a href="#qa-54d3e8b20e547876">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:elastic-expert-routing" data-paper-title="Smoothing the Top-k Exposure Boundary for Sparse Mixture-of-Experts" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Smoothing the Top-k Exposure Boundary for Sparse Mixture-of-Experts 基础模型 Shanghai AI Laboratory / Shanghai Jiao Tong University 2026-10-08 固定 Top-k 会让排序边界外的专家长期缺少训练曝光。该方法训练时为每个 token、每层独立抽取邻近的专家预算，在不改变期望预算的情况下，让边界附近专家参与真实稀疏计算。部署时恢复固定 k。 本地结果标为诊断。实现真实因果自回归 Transformer + 稀疏 MoE，包含 router、专家梯度、辅助均衡损失和固定 k 推理。不是把所有专家都计算一遍后乘零。相同参数形状、初始化、训练位置和预算对照 radius=0 与 radius=1。  稀疏专家与路由 网络架构 基础模型 按需计算：专家、弹性深宽与查表记忆 Elastic expert routing随机改变每个token的专家数，为什么期望计算预算还能保持不变？ 训练预算分布以k为中心、支持集对称且合法，使多选与少选的机会抵消，期望专家数仍为k。边界外专家由此得到真实稀疏执行的曝光；部署恢复固定k。维持期望不代表每个token成本相同，负载统计必须按实际派发计算，不能继续假设每行固定数量。 教学例子：以同等概率选择1、2、3个专家，平均仍为2；偶尔选择第3个能让它接收训练，但一次选3个的token确实比选1个多做了计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-elastic-expert-routing-bd240699" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fd11a9699c42f50d">Elastic expert routing随机改变每个token的专家数，为什么期望计算预算还能保持不变？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aelastic-expert-routing">Smoothing the Top-k Exposure Boundary for Sparse Mixture-of-Experts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory / Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练预算分布以k为中心、支持集对称且合法，使多选与少选的机会抵消，期望专家数仍为k。边界外专家由此得到真实稀疏执行的曝光；部署恢复固定k。维持期望不代表每个token成本相同，负载统计必须按实际派发计算，不能继续假设每行固定数量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>以同等概率选择1、2、3个专家，平均仍为2；偶尔选择第3个能让它接收训练，但一次选3个的token确实比选1个多做了计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11575">原论文</a> · <a href="../../../../foundation-models/2610.11575-elastic-expert-routing/">实现解读</a> · <a href="#qa-fd11a9699c42f50d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sparse-decoding" data-paper-title="SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference 基础模型 Westlake University 2026-10-08 固定文本的 teacher-forcing 激活不等于模型自回归生成时的激活。该方法让稠密模型先从任务问题生成回答，只保存逐 token 解码激活、排除 prefill，再用这些统计量执行剪枝。校准协议与剪枝后端分离：原文主要使用 SparseGPT，也报告 Wanda 消融。系统部分针对 batch-one 解码的矩阵向量乘法：每连续 32 列用一个 32-bit word 标记保留位置；50% 稀疏时恰有 16 个 set bit，按递增列位置打包数值并固定遍历 16 次。 已实现 decoding-only 校准、Wanda N:M 剪枝和真实 Triton bitmask SpMV，并在 A100 运行 Qwen3-4B。当前是 L1 机制诊断；本地结果质量下降且没有加速，不代表原论文大模型实验复现。此入口要求 NVIDIA CUDA 与 Linux Triton；Mac 可以运行公式和打包单测，不能运行稀疏 GPU 路径。公开 checkpoint 下载、训练集派生 holdout 见运行指南。  推理与系统效率 动态计算与模型压缩 基础模型 按需计算：专家、弹性深宽与查表记忆 SparseDecoding为何排除prefill，只用真实逐token生成激活来校准剪枝？ 剪枝要服务于自回归解码，而固定真值文本的teacher forcing与prefill产生的激活分布未必代表部署时的解码状态。方法先让稠密模型真实生成，收集解码激活，再交给剪枝后端重构权重。校准数据怎么取得与使用SparseGPT还是Wanda是两个维度，不能把换校准协议等同于实现了所有后端。 教学例子：模型自己生成了一个偏离参考答案的前缀，后面会访问不同状态；只在参考文本上校准，可能剪掉这些实际解码状态所需的通道。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-sparse-decoding-1beb4b13" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f80ad83e68dcf05f">SparseDecoding为何排除prefill，只用真实逐token生成激活来校准剪枝？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asparse-decoding">SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Westlake University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>剪枝要服务于自回归解码，而固定真值文本的teacher forcing与prefill产生的激活分布未必代表部署时的解码状态。方法先让稠密模型真实生成，收集解码激活，再交给剪枝后端重构权重。校准数据怎么取得与使用SparseGPT还是Wanda是两个维度，不能把换校准协议等同于实现了所有后端。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型自己生成了一个偏离参考答案的前缀，后面会访问不同状态；只在参考文本上校准，可能剪掉这些实际解码状态所需的通道。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12327">原论文</a> · <a href="../../../../foundation-models/2610.12327-sparse-decoding/">实现解读</a> · <a href="#qa-f80ad83e68dcf05f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ce-guided-moe" data-paper-title="Cross-Entropy Guided Routing in Mixture-of-Experts Large Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Cross-Entropy Guided Routing in Mixture-of-Experts Large Language Models 基础模型 Bar-Ilan University 2026-09-29 在原生 MoE affinity 旁增加逐 expert token-error head，并用预测误差的 started-log 对路由 logit 做衰减；高预测错误的 expert 在 Top-K 前被降权，同时误差头由真实 next-token CE 监督。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 error-aware routing 公式；未训练 Granite MoE。执行 error-aware routing 公式；未训练 Granite MoE。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  MoE 路由 Token error 基础模型 按需计算：专家、弹性深宽与查表记忆 CE-guided MoE为什么在原路由分数之外再预测每个expert的错误？ 原affinity表示路由倾向，却未必反映专家处理该token的预期损失。方法用token-error head预测专家误差，在Top-K前对高预测错误专家的logit衰减，再由真实next-token交叉熵训练误差头。选择时用的是可提前预测的误差，不能偷偷读取当前未知正确答案的真实CE。 教学例子：两个专家的原路由分数接近，一个误差头预期它不擅长当前片段，修正后可让另一专家进入Top-K；真正答案只用于训练误差预测，不作为线上路由输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-ce-guided-moe-5d9cde32" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2471437b84bb1aef">CE-guided MoE为什么在原路由分数之外再预测每个expert的错误？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ace-guided-moe">Cross-Entropy Guided Routing in Mixture-of-Experts Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bar-Ilan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原affinity表示路由倾向，却未必反映专家处理该token的预期损失。方法用token-error head预测专家误差，在Top-K前对高预测错误专家的logit衰减，再由真实next-token交叉熵训练误差头。选择时用的是可提前预测的误差，不能偷偷读取当前未知正确答案的真实CE。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个专家的原路由分数接近，一个误差头预期它不擅长当前片段，修正后可让另一专家进入Top-K；真正答案只用于训练误差预测，不作为线上路由输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37751">原论文</a> · <a href="../../../../foundation-models/2609.37751-ce-guided-moe/">实现解读</a> · <a href="#qa-2471437b84bb1aef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lift-feedback" data-paper-title="Pretraining Latent Information Feedback Transformers with Teacher Supervision" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Pretraining Latent Information Feedback Transformers with Teacher Supervision 基础模型 Tel Aviv University 2026-09-29 普通 Transformer 的深层信息只能通过下一个离散 token 回到浅层。LIFT 把 teacher 的下一 token top-k 分布预计算成连续状态；训练时 token 与 teacher state 并行输入，同时预测下一 token 和下一 state；推理时改用模型自己的 state。核心目标是 token CE 加 teacher top-k 分布的前向 KL。 复现级别：L1 核心机制。复现级别：L1 核心机制。实现 top-k 分布状态、token/state SwiGLU 融合和 CE + state KL；未训练 135M–1B 模型。lift_topk_state 保留并归一化 top-k logits；lift_fuse 用共享 embedding 投影 state 并做 residual SwiGLU；lift_loss 组合两个目标。测试覆盖稀疏归一化、反馈改变输出及 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。  网络架构 潜状态反馈 预训练 基础模型 按需计算：专家、弹性深宽与查表记忆 LIFT为什么同时预测下一token和下一连续state，推理时的state又来自哪里？ 训练把教师下一token的top-k分布变为连续状态，与token并行输入，并监督token预测和状态预测。这样深层信息可以经连续反馈进入后续步骤，不只依赖一个离散token。推理时改为模型自己的state，因此教师提供的是训练目标，不能在部署时继续假定能免费读取教师未来分布。 教学例子：离散采样选了一个词，但连续状态还能携带其他高概率候选的信息；下一步使用模型自己预测的状态，错误也可能随反馈累积，需要单独检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-lift-feedback-608d6327" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c82cf42eda4038aa">LIFT为什么同时预测下一token和下一连续state，推理时的state又来自哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alift-feedback">Pretraining Latent Information Feedback Transformers with Teacher Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tel Aviv University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练把教师下一token的top-k分布变为连续状态，与token并行输入，并监督token预测和状态预测。这样深层信息可以经连续反馈进入后续步骤，不只依赖一个离散token。推理时改为模型自己的state，因此教师提供的是训练目标，不能在部署时继续假定能免费读取教师未来分布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>离散采样选了一个词，但连续状态还能携带其他高概率候选的信息；下一步使用模型自己预测的状态，错误也可能随反馈累积，需要单独检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38149">原论文</a> · <a href="../../../../foundation-models/2609.38149-lift-feedback/">实现解读</a> · <a href="#qa-c82cf42eda4038aa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:telescopic-lm" data-paper-title="Telescopic Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Telescopic Language Models 基础模型 University of Cambridge 2026-09-28 每步随机抽一个网络深度前缀做 next-token 监督，同时保留全深度 anchor，使同一 checkpoint 的每个深度都成为可用语言模型。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。验证随机深度和 full anchor 的梯度路径；未做 20B-token 预训练。验证随机深度和 full anchor 的梯度路径；未做 20B-token 预训练。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  网络架构 弹性深度 基础模型 按需计算：专家、弹性深宽与查表记忆 Telescopic LM为什么要训练多个深度前缀，而不直接把训练好的深模型截短？ 普通深模型主要在完整路径上接受监督，中间层截断后未必形成可用语言模型。Telescopic训练时抽取不同深度前缀做next-token监督，并保留全深度anchor，使同一checkpoint的多个深度都被显式训练。它提供可选计算预算，但浅层与深层的能力差距仍需分别评估。 教学例子：服务可按预算运行前8层或全部24层；如果训练一直只监督24层输出，前8层未必能独立预测。对不同前缀训练，才给这种切换提供依据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-telescopic-lm-c2ab9fe1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ede6a79b9ddd5bb5">Telescopic LM为什么要训练多个深度前缀，而不直接把训练好的深模型截短？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atelescopic-lm">Telescopic Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通深模型主要在完整路径上接受监督，中间层截断后未必形成可用语言模型。Telescopic训练时抽取不同深度前缀做next-token监督，并保留全深度anchor，使同一checkpoint的多个深度都被显式训练。它提供可选计算预算，但浅层与深层的能力差距仍需分别评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>服务可按预算运行前8层或全部24层；如果训练一直只监督24层输出，前8层未必能独立预测。对不同前缀训练，才给这种切换提供依据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35769">原论文</a> · <a href="../../../../foundation-models/2609.35769-telescopic-lm/">实现解读</a> · <a href="#qa-ede6a79b9ddd5bb5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:persistent-recurrent-memory" data-paper-title="Persistent Recurrent Memory Between Transformer Layers Improves Language Model Generalization" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Persistent Recurrent Memory Between Transformer Layers Improves Language Model Generalization 基础模型 FITec Labs / Ericsson São Paulo 2026-09-15 在 Transformer 上下半层之间插入 observe–GRU update–gated influence 的持久状态通路。 未复现 TinyStories 完整训练曲线。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行拓扑 reference kernel；未复现 TinyStories 完整训练曲线。本地执行拓扑 reference kernel；未复现 TinyStories 完整训练曲线。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  网络架构 持久记忆 基础模型 按需计算：专家、弹性深宽与查表记忆 把持久递归记忆放在Transformer上下半层之间，改变了哪条信息通路？ 模型先从中间表示观察当前信息，用GRU更新持久状态，再由门控把状态影响交给后续层。它不是只在输入前拼一段固定摘要，也不是无条件把全部旧状态相加；观察、更新与影响三个动作分开，使当前计算能够决定记什么、何时使用。状态仍有容量和重置边界。 教学例子：上半层识别到新约束后写入状态，下半层可按门控使用它；如果当前线索无关，则可少写或少读，而不是让每条历史信息都同等进入输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-persistent-recurrent-memory-f4545966" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a0437ea764b0b567">把持久递归记忆放在Transformer上下半层之间，改变了哪条信息通路？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apersistent-recurrent-memory">Persistent Recurrent Memory Between Transformer Layers Improves Language Model Generalization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FITec Labs / Ericsson São Paulo</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型先从中间表示观察当前信息，用GRU更新持久状态，再由门控把状态影响交给后续层。它不是只在输入前拼一段固定摘要，也不是无条件把全部旧状态相加；观察、更新与影响三个动作分开，使当前计算能够决定记什么、何时使用。状态仍有容量和重置边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>上半层识别到新约束后写入状态，下半层可按门控使用它；如果当前线索无关，则可少写或少读，而不是让每条历史信息都同等进入输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17251">原论文</a> · <a href="../../../../foundation-models/2609.17251-persistent-recurrent-memory/">实现解读</a> · <a href="#qa-a0437ea764b0b567">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:repeat-aware-moe" data-paper-title="Data Scarcity and Model Sparsity: Mixtures-of-Experts Overfit More to Repeated Data" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Data Scarcity and Model Sparsity: Mixtures-of-Experts Overfit More to Repeated Data 基础模型 Stanford University 2026-09-10 研究重复数据下 MoE 比 Dense 更早过拟合的问题，并用更强 masking/dropout 抑制 expert 记忆化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地实现随重复倍数和稀疏度变化的正则 schedule；未进行大规模预训练。本地实现随重复倍数和稀疏度变化的正则 schedule；未进行大规模预训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  MoE 数据重复与正则化 基础模型 按需计算：专家、弹性深宽与查表记忆 训练token总数相同，为什么大量重复数据对MoE和Dense可能产生不同影响？ 相同token预算不代表相同独立信息量；路由专家可能更快记住反复出现的样本，使MoE在重复训练中更早过拟合。研究因此检查更强masking或dropout对专家记忆化的抑制，而不是仅靠增加重复轮数扩大“数据规模”。效果需要在隔离数据上判断，训练loss继续下降不足以证明泛化改善。 教学例子：把同一小语料重复十遍和加入十份新语料都消耗近似token预算，但前者更容易形成专家专记的模式；比较时应分别报告唯一数据量与重复次数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-repeat-aware-moe-d00603e8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0ca7b821059ada2f">训练token总数相同，为什么大量重复数据对MoE和Dense可能产生不同影响？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arepeat-aware-moe">Data Scarcity and Model Sparsity: Mixtures-of-Experts Overfit More to Repeated Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同token预算不代表相同独立信息量；路由专家可能更快记住反复出现的样本，使MoE在重复训练中更早过拟合。研究因此检查更强masking或dropout对专家记忆化的抑制，而不是仅靠增加重复轮数扩大“数据规模”。效果需要在隔离数据上判断，训练loss继续下降不足以证明泛化改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把同一小语料重复十遍和加入十份新语料都消耗近似token预算，但前者更容易形成专家专记的模式；比较时应分别报告唯一数据量与重复次数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11917">原论文</a> · <a href="../../../../foundation-models/2609.11917-repeat-aware-moe/">实现解读</a> · <a href="#qa-0ca7b821059ada2f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:swrouter" data-paper-title="SWRouter: Similarity-Contractive Window Routing for Multi-Turn Large Language Model Conversations" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="SWRouter: Similarity-Contractive Window Routing for Multi-Turn Large Language Model Conversations 基础模型 Shanghai Jiao Tong University 2026-09-10 按相邻语义相似度收缩多轮窗口，再用对比路由器选模型，并分开评测上下文构造和路由正确性。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行窗口分段和 profile overlap 路由；未训练论文对比 encoder。本地执行窗口分段和 profile overlap 路由；未训练论文对比 encoder。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  模型路由 多轮上下文 基础模型 按需计算：专家、弹性深宽与查表记忆 SWRouter为什么要把上下文收缩质量和选模型正确率分开评测？ 前一步按相邻语义相似度合并或收缩对话窗口，后一步才由路由器选择模型；上下文若先丢掉关键约束，后面选对强模型也可能失败。反过来，完整上下文也不保证路由合适。拆开评测才能定位到底是材料构造还是模型选择造成差异，避免把两个环节的收益混成一个数字。 教学例子：两轮话题相似但用户在第二轮改了预算；若收缩时漏掉预算变化，最终失败不能全怪被选模型，应先检查构造出的上下文是否保留了修改。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-swrouter-da0aa5dd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d67fa349937aa021">SWRouter为什么要把上下文收缩质量和选模型正确率分开评测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswrouter">SWRouter: Similarity-Contractive Window Routing for Multi-Turn Large Language Model Conversations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前一步按相邻语义相似度合并或收缩对话窗口，后一步才由路由器选择模型；上下文若先丢掉关键约束，后面选对强模型也可能失败。反过来，完整上下文也不保证路由合适。拆开评测才能定位到底是材料构造还是模型选择造成差异，避免把两个环节的收益混成一个数字。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两轮话题相似但用户在第二轮改了预算；若收缩时漏掉预算变化，最终失败不能全怪被选模型，应先检查构造出的上下文是否保留了修改。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11414">原论文</a> · <a href="../../../../foundation-models/2609.11414-swrouter/">实现解读</a> · <a href="#qa-d67fa349937aa021">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lngram-v2" data-paper-title="Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations 基础模型 Beijing University of Posts and Telecommunications / Kuaishou Technology 2026-09-03 Lngram v2 把 backbone hidden state 投影成多路二进制地址，以最近 1/2-gram 的离散组合 O(1) 查 memory table；多个 route token 经 GQA 读回主干。硬地址保证表示可解释，反事实邻接地址提供训练梯度，零 Sink 允许模型拒绝无用记忆。 复现级别：核心机制 + 真实 VLM checkpoint GPU 验证。复现级别：核心机制 + 真实 VLM checkpoint GPU 验证。实现多路离散寻址、精确 n-gram 查表、反事实 surrogate gradient 和带零 Sink 的 GQA 读出。未执行 Keye 2B/30B 全量预训练或论文规模语料；GPU 验证只声明真实公开 VLM hidden state 上的机制、梯度和显存可执行，可作为 LLM/多模态 Evolve memory 算子。CPU 三 seed 机制结果见 metrics/public-seeds42-44.json；  multimodal-foundation-model conditional-memory discrete-routing model-architecture 基础模型 按需计算：专家、弹性深宽与查表记忆 Lngram v2使用硬二进制地址查表，为什么还需要反事实邻接地址和零Sink？ 硬地址使记忆访问离散且可解释，但不能沿普通索引直接获得平滑梯度；邻接地址提供反事实比较信号，帮助训练地址选择。查出的多路token再通过GQA读回，并加入零Sink，使模型可选择不使用当前记忆。能命中表项不意味着它必定有用，更不该强制把所有查表结果写回。 教学例子：当前地址查到不相关短语，邻接地址可能提供更合适关联；若两者都无帮助，注意力可转向零Sink，避免为了“有记忆”就注入噪声。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-lngram-v2-f7907f6f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-194361272e173289">Lngram v2使用硬二进制地址查表，为什么还需要反事实邻接地址和零Sink？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alngram-v2">Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications / Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>硬地址使记忆访问离散且可解释，但不能沿普通索引直接获得平滑梯度；邻接地址提供反事实比较信号，帮助训练地址选择。查出的多路token再通过GQA读回，并加入零Sink，使模型可选择不使用当前记忆。能命中表项不意味着它必定有用，更不该强制把所有查表结果写回。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前地址查到不相关短语，邻接地址可能提供更合适关联；若两者都无帮助，注意力可转向零Sink，避免为了“有记忆”就注入噪声。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.03426">原论文</a> · <a href="../../../../reproductions/2609.03426-lngram-v2/">实现解读</a> · <a href="#qa-194361272e173289">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rare" data-paper-title="RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models 基础模型 Huazhong University of Science and Technology 2026-08-21 Dense LLM 的 activation steering 直接用于 MoE 时会改变 router logits，token 被送往不同专家后，原估计的行为方向失效。RARE 将任意 steering direction 投影到 router 的零空间，并在后续保护层再次移除传播产生的 router-visible 分量，在保留原专家路径的同时改变行为表征。 未加载 DeepSeek-V2-Lite、Mixtral、Phi、Qwen3 或 GPT-OSS，也未运行 JailbreakBench、TruthfulQA、CounterFact。Fidelity: 核心机制复现。真实执行 router 行空间 SVD、零空间投影、路由一致性和下游校正；未加载论文六个大 MoE checkpoint。未加载 DeepSeek-V2-Lite、Mixtral、Phi、Qwen3 或 GPT-OSS，也未运行 JailbreakBench、TruthfulQA、CounterFact。这里验证的是论文式 (8) 的精确路由不变性，不把合成 steering 指标冒充论文下游效果。  llm-architecture mixture-of-experts representation-steering model-editing 基础模型 按需计算：专家、弹性深宽与查表记忆 RARE怎样改变MoE表征，同时避免steering顺便把token送到另一组专家？ 直接加steering向量会改router可见的分量，导致原有专家路径发生变化。RARE把方向投影到router零空间，让当前层路由logit保持不变；传播到后续保护层时，再移除新产生的可见漂移。保护路由与改变行为表示被分开，但这不等于所有后续非线性影响都可忽略。 教学例子：一条行为方向同时带有“改回答风格”和“改专家选择”的分量；投影先去掉后一部分，并在受保护的后续层继续纠偏，减少专家路径变更造成的混杂。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-rare-2c269dff" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1cea8b60a2a7e1dd">RARE怎样改变MoE表征，同时避免steering顺便把token送到另一组专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arare">RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接加steering向量会改router可见的分量，导致原有专家路径发生变化。RARE把方向投影到router零空间，让当前层路由logit保持不变；传播到后续保护层时，再移除新产生的可见漂移。保护路由与改变行为表示被分开，但这不等于所有后续非线性影响都可忽略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条行为方向同时带有“改回答风格”和“改专家选择”的分量；投影先去掉后一部分，并在受保护的后续层继续纠偏，减少专家路径变更造成的混杂。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21236">原论文</a> · <a href="../../../../reproductions/2608.21236-rare/">实现解读</a> · <a href="#qa-1cea8b60a2a7e1dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:macro" data-paper-title="MACRO: Markov Chain Routing of Transformer Layers" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="MACRO: Markov Chain Routing of Transformer Layers 基础模型 Heinrich Heine University Düsseldorf 2026-08-06 主题：动态层路由。固定顺序执行所有 Transformer 层并非总是最优。MACRO 用上下文条件 Markov policy 表示 skip、repeat、residual-add 等操作，再用反馈更新路由分布和 top-k Viterbi 解码候选程序，不修改底座权重。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。在确定性分类 mini-suite 搜索 81 条 skip/repeat/residual 路由；同时作为 micro-LLM evolve 的可选结构。  network-architecture dynamic-routing inference-efficiency 基础模型 按需计算：专家、弹性深宽与查表记忆 MACRO不改底座权重，怎样仍能改变模型对一个输入的计算过程？ 它把层执行顺序表示为上下文条件的路由程序，允许跳过、重复或残差相加等操作。反馈更新的是路由分布，再用候选程序搜索选择执行路径；底座参数保持不变。因而收益来自怎样调用已有层，不能写成底座学到了新权重，程序选择也必须避免读取隔离测试答案。 教学例子：一个输入可跳过某层，另一个输入重复使用该层；两次调用相同权重，得到的总计算路径不同。选择路径时可用验证反馈，不能按测试真值逐题挑最优程序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-macro-6eaa3033" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9feb28422bcc1fc0">MACRO不改底座权重，怎样仍能改变模型对一个输入的计算过程？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amacro">MACRO: Markov Chain Routing of Transformer Layers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Heinrich Heine University Düsseldorf</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把层执行顺序表示为上下文条件的路由程序，允许跳过、重复或残差相加等操作。反馈更新的是路由分布，再用候选程序搜索选择执行路径；底座参数保持不变。因而收益来自怎样调用已有层，不能写成底座学到了新权重，程序选择也必须避免读取隔离测试答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个输入可跳过某层，另一个输入重复使用该层；两次调用相同权重，得到的总计算路径不同。选择路径时可用验证反馈，不能按测试真值逐题挑最优程序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05872">原论文</a> · <a href="../../../../reproductions/2608.05872-macro/">实现解读</a> · <a href="#qa-9feb28422bcc1fc0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rd-attnres" data-paper-title="Role-Decoupled Attention Residuals" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Role-Decoupled Attention Residuals 基础模型 Kehan Wang（论文未列机构） 2026-08-03 Block AttnRes 让注意力层从全部历史 residual sources 动态读取，但 Q、K、V 共用一条深度路由。论文指出 QK 负责匹配、V 负责承载内容，两者偏好的深度未必相同；RD-AttnRes 在不改变 residual sources 和 attention 主体的情况下，只为 V 增加一个 model-width 路由向量。 Fidelity：核心机制复现。以共享路由的 Block AttnRes 为严格匹配基线，只增加 V 专属路由。未复刻 120M/343M 预训练规模和原论文语料；本地仅验证匹配的结构消融与 evolve 接入。本地对照口径：基线为共享深度路由的 Block AttnRes，实验组仅解耦 QK/V route；相对基线 PPL +0.61%（变差）。  foundation-model attention residual-routing 基础模型 按需计算：专家、弹性深宽与查表记忆 RD-AttnRes为什么只为V增加一条深度路由，而让Q/K继续共用另一条？ Q/K决定怎样匹配位置，V承载实际取回的内容，两种角色需要的历史层组合可能不同。方法保持同一组残差来源和attention主体，为V单独学习深度选择，使内容来源可以与匹配依据分离。额外的是路由自由度，不能解释成凭空增加了原先不存在的残差信息。 教学例子：较浅层更保留词面细节，较深层更适合语义匹配；Q/K可偏向语义组合，而V仍取用较浅的细节，不必强迫三者使用完全相同的深度权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-rd-attnres-0af1c94e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2c920aab21c83511">RD-AttnRes为什么只为V增加一条深度路由，而让Q/K继续共用另一条？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ard-attnres">Role-Decoupled Attention Residuals</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kehan Wang（论文未列机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Q/K决定怎样匹配位置，V承载实际取回的内容，两种角色需要的历史层组合可能不同。方法保持同一组残差来源和attention主体，为V单独学习深度选择，使内容来源可以与匹配依据分离。额外的是路由自由度，不能解释成凭空增加了原先不存在的残差信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>较浅层更保留词面细节，较深层更适合语义匹配；Q/K可偏向语义组合，而V仍取用较浅的细节，不必强迫三者使用完全相同的深度权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01075">原论文</a> · <a href="../../../../reproductions/2608.01075-rd-attnres/">实现解读</a> · <a href="#qa-2c920aab21c83511">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wide" data-paper-title="WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning 基础模型 EIT-NLP / LMU Munich 2026-07-30 静态剪枝无法按 token 难度分配算力，动态深度又过于粗粒度。WIDE 对每个 token 分别路由 attention head group 和 FFN channel group，并将 mask reorder、block skip 与设备内跳过联合设计。 Fidelity: 核心机制复现。实际训练 attention-head group 与 FFN-channel group router，并接入 LLM evolve。PyTorch dense kernel 不会因 mask 自动加速，因此只验证 router、稀疏率和质量变化，不冒充论文 CUDA 性能。本地对照口径：基线为同预算 dense LLaMA；实验组固定激活 50% head/channel，相对基线 perplexity +0.81%（轻微退化）。  llm-architecture dynamic-pruning inference-efficiency 基础模型 按需计算：专家、弹性深宽与查表记忆 WIDE的动态宽度与跳过整层相比，细在哪里？ 它按token分别选择attention head组和FFN通道组，在一层内部改变参与计算的宽度，而不是只能整层执行或跳过。要得到实际节省，还需把mask重排、块跳过和设备端执行配合起来；仅把dense张量某些位置乘零，并没有自动省掉原先的矩阵计算。 教学例子：一个简单token可用较少head和FFN组，另一个难token在同一层使用更宽路径；如果内核依旧完整计算所有组，再置零，逻辑稀疏并未兑现成延迟收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-wide-0e0ca0da" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c2aef9a999c0cef5">WIDE的动态宽度与跳过整层相比，细在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awide">WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · EIT-NLP / LMU Munich</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它按token分别选择attention head组和FFN通道组，在一层内部改变参与计算的宽度，而不是只能整层执行或跳过。要得到实际节省，还需把mask重排、块跳过和设备端执行配合起来；仅把dense张量某些位置乘零，并没有自动省掉原先的矩阵计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个简单token可用较少head和FFN组，另一个难token在同一层使用更宽路径；如果内核依旧完整计算所有组，再置零，逻辑稀疏并未兑现成延迟收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28418">原论文</a> · <a href="../../../../reproductions/2607.28418-wide/">实现解读</a> · <a href="#qa-c2aef9a999c0cef5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:penelope" data-paper-title="Penelope: Localized Latent Recurrence for Efficient Structured Reasoning" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Penelope: Localized Latent Recurrence for Efficient Structured Reasoning 基础模型 Academic author team 2026-07-28 只在一个 decoder 边界执行共享权重的 latent recurrence，用门控状态反复精炼表示，避免整条 decoder 重跑。 Fidelity: 核心机制复现。本地执行局部潜在递归与门控状态更新；不复刻原论文的大模型训练规模。12-step 本地预算不包含论文规模 checkpoint 和 CoT-to-latent curriculum，只验证真实 PyTorch 结构路径。本地对照口径：基线为 llama_modern，实验组为 penelope；composite loss 从 6.9539 降到 6.9100，相对改善 0.63%。  llm-architecture latent-reasoning recurrence efficiency 基础模型 按需计算：专家、弹性深宽与查表记忆 Penelope增加latent推理步时，为什么不用把整条decoder反复运行？ 递归被局限在一个decoder边界，用共享变换与门控状态反复精炼该处表示，再继续后续计算。它增加的是局部表示更新次数，而不是每一步都重跑所有层。这样控制额外成本，但多次精炼是否真的帮助任务仍需测量；循环次数不能直接当作有效推理能力。 教学例子：把一道结构化题的中间表示在一个局部模块里更新3次，再交给后半段网络；前面已经完成的所有decoder层无需跟着重复3次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-penelope-d7b5f7a1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7b2c14cdd216b4ff">Penelope增加latent推理步时，为什么不用把整条decoder反复运行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apenelope">Penelope: Localized Latent Recurrence for Efficient Structured Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Academic author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>递归被局限在一个decoder边界，用共享变换与门控状态反复精炼该处表示，再继续后续计算。它增加的是局部表示更新次数，而不是每一步都重跑所有层。这样控制额外成本，但多次精炼是否真的帮助任务仍需测量；循环次数不能直接当作有效推理能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把一道结构化题的中间表示在一个局部模块里更新3次，再交给后半段网络；前面已经完成的所有decoder层无需跟着重复3次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25915">原论文</a> · <a href="../../../../reproductions/2607.25915-penelope/">实现解读</a> · <a href="#qa-7b2c14cdd216b4ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adadsf" data-paper-title="Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs 基础模型 Huawei ACS Lab / Southern University of Science and Technology 2026-07-23 固定比例的 Mixture-of-Depths 会给每一层相同 token budget，但不同层对表示的改写强度并不相同。AdaDSF 先在 dense teacher 上测量各层输入/输出 cosine similarity，再把更多计算分给变化更大的层；每层 MLP router 只把 Top-K token 送入原 Transformer block，其他 token 走 residual bypass。最后同时对齐中间 hidden states 和输出分布。 Fidelity: 核心机制复现。真实执行 dense calibration、逐层 token budget 分配、Top-K router 和特征对齐；缩小模型与训练预算。未下载 GPT-NeoX-130M/Qwen2.5 和 WikiText-103，而是在本地 WikiText-2 微型 decoder 上验证算法链路；normalized active-token fraction 不是 GPU kernel 的实测 FLOPs。Top-K block 确实只处理选中 token，不是输出后 masking，但没有论文大模型 kernel 优化与六项完整 commonsense 评测。  llm-architecture efficient-inference token-routing 基础模型 按需计算：专家、弹性深宽与查表记忆 AdaDSF为何把更多token计算预算分给输入输出相似度较低的层？ 相似度低表示该层对表示改写更大，固定每层相同稀疏率可能把关键变换一并跳过。AdaDSF先测dense教师的层级变化，将预算映射并校正到全局总量，再由每层router选择token，其余走残差旁路。预算分配与学生对齐训练分工不同，不能只复制一个全局Top-K比例。 教学例子：一层几乎原样传递输入，另一层明显重组信息；同样跳过一半token并不等价。总预算固定时，可把更多块执行机会分给改写更强的一层。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-adadsf-0ee93157" class="ar-learning-paper-anchor"></span>
<h2 id="qa-641401c9edeae52a">AdaDSF为何把更多token计算预算分给输入输出相似度较低的层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadadsf">Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei ACS Lab / Southern University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似度低表示该层对表示改写更大，固定每层相同稀疏率可能把关键变换一并跳过。AdaDSF先测dense教师的层级变化，将预算映射并校正到全局总量，再由每层router选择token，其余走残差旁路。预算分配与学生对齐训练分工不同，不能只复制一个全局Top-K比例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一层几乎原样传递输入，另一层明显重组信息；同样跳过一半token并不等价。总预算固定时，可把更多块执行机会分给改写更强的一层。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21291">原论文</a> · <a href="../../../../reproductions/2607.21291-adadsf/">实现解读</a> · <a href="#qa-641401c9edeae52a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:looped-latent-attention" data-paper-title="Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers 基础模型 University of Maryland / Meta AI 2026-07-16 Looped Transformer 重复使用同一组权重，但不同 loop 的 KV cache 仍重复占内存。LLA 学习跨 loop 共享的低秩 K/V latent，服务时按 loop 重建专用 K/V，从 recurrence 冗余中换取近无损压缩。 Fidelity: 核心机制复现。训练权重共享的 looped block，并在共享 latent 中保存 K/V。本地从头训练 64d 模型，不是对大 checkpoint 训练 post-hoc codec，也没有 fused serving kernel。本地对照口径：基线是两层 llama_modern；实验组用一个权重共享 block 循环两次并采用 2× K/V latent，LM loss 5.7471→5.8012，相对 +0.94%（更差），参数 139584→80576。  llm-architecture kv-cache looped-transformer 基础模型 按需计算：专家、弹性深宽与查表记忆 Looped Transformer共享权重后，为什么跨loop的KV缓存仍有压缩空间？ 共享计算参数并不意味着每个loop产生的KV相同，直接缓存仍可能按loop重复存储。LLA学习可共享的低秩latent，再按loop使用专用映射重建K/V，把跨loop冗余转成存储节省。节省程度受latent秩和重建误差约束，也可能增加重建计算，不能由权重共享自动推出缓存已共享。 教学例子：同一组网络权重运行4轮，各轮状态不同；可以保存一份较小latent及4组重建映射，而不是保存4份完整KV，但要验证重建后的读取仍可靠。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-looped-latent-attention-49effa17" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e51c5322d385eee9">Looped Transformer共享权重后，为什么跨loop的KV缓存仍有压缩空间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alooped-latent-attention">Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享计算参数并不意味着每个loop产生的KV相同，直接缓存仍可能按loop重复存储。LLA学习可共享的低秩latent，再按loop使用专用映射重建K/V，把跨loop冗余转成存储节省。节省程度受latent秩和重建误差约束，也可能增加重建计算，不能由权重共享自动推出缓存已共享。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一组网络权重运行4轮，各轮状态不同；可以保存一份较小latent及4组重建映射，而不是保存4份完整KV，但要验证重建后的读取仍可靠。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15456">原论文</a> · <a href="../../../../reproductions/2607.15456-looped-latent-attention/">实现解读</a> · <a href="#qa-e51c5322d385eee9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:memory-grafting" data-paper-title="Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory 基础模型 Tsinghua University / Microsoft Research Asia 2026-05-20 Engram 的大容量条件记忆需要随主模型从零训练。Memory Grafting 先统计高频 2/3/4-gram，用已经预训练的 grafting model 离线编码每个短语最后 token 的中间 hidden state并冻结；recipient 在线只做期望的最长后缀精确查询。未命中时回退到可训练 hash Engram，命中值经独立投影、上下文门控、短卷积后写回 residual stream。 结果说明完整 grafting 路径有效且优于无记忆模型，但当前 bank 太小，未验证相对 Engram 的增益。Fidelity: 核心机制复现。实际训练 grafting model 与 recipient，执行冻结 n-gram hidden bank、最长精确匹配、Engram fallback、query-key gate、短卷积和残差写入。64-d dense recipient、微型 teacher 与 192-entry bank 替代论文 0.92B/2.8B MoE、Qwen3.5/DeepSeek grafting model、50B/100B tokens 和 3M-entry bank；  llm-pretraining conditional-memory offline-knowledge-transfer 基础模型 按需计算：专家、弹性深宽与查表记忆 Memory Grafting为什么先离线编码常见短语，查不到时又要回退到hash Engram？ 离线grafting model把常见n-gram编码成冻结记忆，recipient在线进行最长后缀精确查询，避免每次重新运行该模型。精确表只覆盖预先准备的短语，未命中时由可训练hash记忆补充；命中结果也需经过独立投影与上下文门控。离线知识来源与线上使用成本因此被分开。 教学例子：一个高频三元短语可以直接命中离线向量，生僻的新组合则进入hash回退路径；无论哪路，都还要判断它对当前上下文是否有帮助。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-memory-grafting-16992e0e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bda5b2f934f9e644">Memory Grafting为什么先离线编码常见短语，查不到时又要回退到hash Engram？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amemory-grafting">Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University / Microsoft Research Asia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线grafting model把常见n-gram编码成冻结记忆，recipient在线进行最长后缀精确查询，避免每次重新运行该模型。精确表只覆盖预先准备的短语，未命中时由可训练hash记忆补充；命中结果也需经过独立投影与上下文门控。离线知识来源与线上使用成本因此被分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个高频三元短语可以直接命中离线向量，生僻的新组合则进入hash回退路径；无论哪路，都还要判断它对当前上下文是否有帮助。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.20948">原论文</a> · <a href="../../../../reproductions/2605.20948-memory-grafting/">实现解读</a> · <a href="#qa-bda5b2f934f9e644">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mild" data-paper-title="Optimized Deferral for Imbalanced Settings" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Optimized Deferral for Imbalanced Settings 基础模型 Google Research 2026-04-30 少数覆盖的专用专家容易被多数专家淹没。论文通过对不同专家设置不同margin约束来平衡学习。保留训练奖励而非以argmin成本生成单一硬标签；这是v1 §5.3 mild目标、§4.2 margin建议的低成本实现。 原完整图像200epoch、多专家、5run及多LLM评测成本过高，不复现（审查DONE），不为这轮下载大型专家。4条自建线性可分夹具，仅作100步目标优化与解析梯度有限差分检查，不是泛化test。对齐原文分数并列时选择最高专家索引。稳定结果见metrics/component-cpu-seed42.json，diagnostic_only=true，不提供真实专家能力或evolve改善证据。  模型路由 不平衡cost-sensitive学习 基础模型 按需计算：专家、弹性深宽与查表记忆 mild在专家不均衡时，为何调整各专家的margin，而不只给少数专家加类别权重？ 不同margin改变损失中专家分数差的尺度，影响怎样形成分离边界；类别权重主要改变某类损失的总体分量，并不等价。mild保留训练时各专家的成本或奖励信息，避免先用最小成本压成一个硬标签。margin依据训练数据估计，推理router不能读取当前样本未知的全专家真成本。 教学例子：一个专家擅长少数但重要的样本；把所有样本先标成“成本最小专家”可能丢掉接近的备选关系，而保留完整成本并调margin可表达这些差别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-mild-b3546e10" class="ar-learning-paper-anchor"></span>
<h2 id="qa-389a19e2fa152f10">mild在专家不均衡时，为何调整各专家的margin，而不只给少数专家加类别权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amild">Optimized Deferral for Imbalanced Settings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同margin改变损失中专家分数差的尺度，影响怎样形成分离边界；类别权重主要改变某类损失的总体分量，并不等价。mild保留训练时各专家的成本或奖励信息，避免先用最小成本压成一个硬标签。margin依据训练数据估计，推理router不能读取当前样本未知的全专家真成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个专家擅长少数但重要的样本；把所有样本先标成“成本最小专家”可能丢掉接近的备选关系，而保留完整成本并调margin可表达这些差别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.27723">原论文</a> · <a href="../../../../foundation-models/2604.27723-mild/">实现解读</a> · <a href="#qa-389a19e2fa152f10">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:engram" data-paper-title="Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models 基础模型 DeepSeek 2026-01-12 MoE 只增加条件计算，模型仍需用计算层反复重建静态局部模式。Engram 把规范化 n-gram 哈希到大 embedding table，进行确定性的 lookup，并在早期层门控注入，让 attention/FFN 留给组合推理。 未执行 27B/MoE 规模预训练、分布式表和异步预取；Fidelity: 核心机制复现。真实训练 hashed n-gram memory、门控融合，并接入 LLM evolve。未执行 27B/MoE 规模预训练、分布式表和异步预取；本地验证的是可学习查表路径，而非论文 benchmark 复刻。本地对照口径：基线是同预算 llama_modern；实验组加入 4096-bucket trigram memory，WikiText-2 LM loss 5.7471→6.1533，相对 +7.07%（更差），PPL 313.27→470.27。  llm-architecture conditional-memory sparsity 基础模型 按需计算：专家、弹性深宽与查表记忆 Engram的稀疏为什么是“条件记忆”，而不是再增加一组MoE专家？ MoE根据输入选择计算网络；Engram把规范化短语的n-gram映射到记忆表，确定性查表后经门控注入状态。常见局部模式可由存储补充，让计算层集中处理组合关系。查表虽然便宜，仍有表容量、哈希碰撞、带宽及融合成本，不能把存储参数都当作免费激活计算。 教学例子：常见固定短语反复出现时，可查到相应记忆向量；要判断这个短语在本句中的含义，仍需要当前上下文与后续网络，而不是只返回一条表项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-engram-7eeee5b9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-89a8dbb57f4df6dc">Engram的稀疏为什么是“条件记忆”，而不是再增加一组MoE专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aengram">Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MoE根据输入选择计算网络；Engram把规范化短语的n-gram映射到记忆表，确定性查表后经门控注入状态。常见局部模式可由存储补充，让计算层集中处理组合关系。查表虽然便宜，仍有表容量、哈希碰撞、带宽及融合成本，不能把存储参数都当作免费激活计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>常见固定短语反复出现时，可查到相应记忆向量；要判断这个短语在本句中的含义，仍需要当前上下文与后续网络，而不是只返回一条表项。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.07372">原论文</a> · <a href="../../../../reproductions/2601.07372-engram/">实现解读</a> · <a href="#qa-89a8dbb57f4df6dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mhc" data-paper-title="mHC: Manifold-Constrained Hyper-Connections" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="mHC: Manifold-Constrained Hyper-Connections 基础模型 DeepSeek-AI 2025-12-31 Hyper-Connections 把单一 residual stream 扩为多个流并动态混合，但任意残差矩阵会破坏 identity mapping，深层组合可能放大信号。mHC 将投影到 Birkhoff polytope（非负、行列和均为 1），同时约束、非负；这样既保留跨流信息交换，又让每层残差映射非扩张。论文另提供融合 kernel、activation 重计算和 DualPipe 重叠以控制系统开销。 实验组 mHC validation PPL 468.903→472.031，变化 -0.67%（未验证效果提升），但残差谱范数 1.0892→1.0000、行列和最大误差 0.11→0。Fidelity: 核心机制复现。在小型 causal Transformer 中实际训练动态两流 HC/mHC，对残差映射做 20 次 Sinkhorn-Knopp，并测量行列约束与谱范数。未复刻 3B/9B/27B MoE、超深训练、TileLang 融合 kernel、分段重计算和 DualPipe；小模型只验证 mHC 数学路径与短程训练，不声称复现论文规模收益。  llm-architecture hyper-connections training-stability 基础模型 按需计算：专家、弹性深宽与查表记忆 mHC为何把残差混合矩阵约束成双随机矩阵，而不是允许任意跨流混合？ 多个残差流若用任意矩阵反复混合，深层组合可能持续放大信号并破坏稳定的残差通路。双随机约束要求非负且行列和为1，让残差交换更受控，同时保留跨流沟通。约束的是残差混合部分，不能把它夸成整个含非线性分支的网络输出一定不增长。 教学例子：两个流可按0.7/0.3交换信息，另一行相应保持和为1；若每层都无约束地把两流相加，反复叠加的幅度可能快速放大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-mhc-cde7f1ea" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d5c14b4fa80176f3">mHC为何把残差混合矩阵约束成双随机矩阵，而不是允许任意跨流混合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amhc">mHC: Manifold-Constrained Hyper-Connections</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个残差流若用任意矩阵反复混合，深层组合可能持续放大信号并破坏稳定的残差通路。双随机约束要求非负且行列和为1，让残差交换更受控，同时保留跨流沟通。约束的是残差混合部分，不能把它夸成整个含非线性分支的网络输出一定不增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个流可按0.7/0.3交换信息，另一行相应保持和为1；若每层都无约束地把两流相加，反复叠加的幅度可能快速放大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.24880">原论文</a> · <a href="../../../../reproductions/2512.24880-mhc/">实现解读</a> · <a href="#qa-d5c14b4fa80176f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:blt" data-paper-title="Byte Latent Transformer: Patches Scale Better Than Tokens" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Byte Latent Transformer: Patches Scale Better Than Tokens 基础模型 Meta FAIR 2024-12-13 直接处理 byte，并依据 next-byte entropy 动态形成 patch；全局 Transformer 在 patch 级计算，局部编码器/解码器恢复 byte。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际执行可学习 surprisal boundary、相邻低熵位置 latent patch 共享并展开回原目标；当前 evaluator 的 512-symbol tokenizer 只近似 byte alphabet，未复刻 8B BLT 与完整 local encoder/decoder。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 blt；相对 PPL -2.13%。  tokenizer-free byte-model dynamic-patching architecture 基础模型 按需计算：专家、弹性深宽与查表记忆 BLT直接读byte，为什么全局Transformer不必给每个byte都付同样计算？ 局部模块处理字节，熵信号决定在哪里形成新patch；全局Transformer只在patch级进行交互，局部解码再恢复字节预测。规则允许简单片段聚成较长patch、困难片段使用更细粒度。因此省的是全局交互次数，并非跳过所有字节处理，也不等同于使用固定的分词表。 教学例子：重复格式可以被局部模块概括成较长patch，难预测的片段触发更多边界；两段字节长度相同，调用全局模型的次数可以不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-blt-d95f5fc6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d5226d54fcb95718">BLT直接读byte，为什么全局Transformer不必给每个byte都付同样计算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ablt">Byte Latent Transformer: Patches Scale Better Than Tokens</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta FAIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部模块处理字节，熵信号决定在哪里形成新patch；全局Transformer只在patch级进行交互，局部解码再恢复字节预测。规则允许简单片段聚成较长patch、困难片段使用更细粒度。因此省的是全局交互次数，并非跳过所有字节处理，也不等同于使用固定的分词表。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>重复格式可以被局部模块概括成较长patch，难预测的片段触发更多边界；两段字节长度相同，调用全局模型的次数可以不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.09871">原论文</a> · <a href="../../../../reproductions/2412.09871-blt/">实现解读</a> · <a href="#qa-d5226d54fcb95718">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:switch-transformer" data-paper-title="Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity 基础模型 Google Brain 2021-01-11 Switch 把 dense FFN 替换为每个 token 只激活一个专家的稀疏 MoE，在近似固定 FLOPs 下扩大参数容量。 Fidelity: 核心机制复现。实现 token-level top-1 expert routing 与负载均衡辅助损失。未复刻万亿参数训练、expert capacity overflow 和跨设备 all-to-all。本地对照口径：基线是参数预算内 dense Transformer；实验组是四专家 top-1 Switch FFN；WikiText-2 30-step perplexity 相对 -3.29%（越低越好）。  llm-architecture mixture-of-experts classic 基础模型 按需计算：专家、弹性深宽与查表记忆 Switch每个token只选一个专家，为什么仍需要负载均衡损失？ top-1控制单token激活成本，却不能保证token均匀分散；router可能把大量输入送到少数专家，造成拥塞与其他专家缺少训练。辅助损失结合实际派发比例与平均路由概率，约束这种偏斜。扩大总专家参数不等于所有参数同时参与每个token，也不自动带来吞吐同比增长。 教学例子：8个专家中一个收走90%的token，虽然每个token都只算一个FFN，服务仍可能堵在这个专家；负载问题与每行top-1数量是不同约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<span id="paper-foundation-models-switch-transformer-9afbb109" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5ef6fd08ba273212">Switch每个token只选一个专家，为什么仍需要负载均衡损失？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswitch-transformer">Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Brain</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>top-1控制单token激活成本，却不能保证token均匀分散；router可能把大量输入送到少数专家，造成拥塞与其他专家缺少训练。辅助损失结合实际派发比例与平均路由概率，约束这种偏斜。扩大总专家参数不等于所有参数同时参与每个token，也不自动带来吞吐同比增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>8个专家中一个收走90%的token，虽然每个token都只算一个FFN，服务仍可能堵在这个专家；负载问题与每行top-1数量是不同约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2101.03961">原论文</a> · <a href="../../../../reproductions/2101.03961-switch-transformer/">实现解读</a> · <a href="#qa-5ef6fd08ba273212">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

同一参数预算下，每个 token 应该激活哪些参数、运行多少步？

## 记住这一点

Switch Transformer 用 top-1 路由让 token 只进入一个专家，并以负载均衡损失防止少数专家拥塞；Engram 用 n-gram 哈希查表补充可学习记忆，减少局部模式反复由计算层重建。动态深度、宽度和循环方法进一步决定本次输入值得运行多少计算。共同问题是把总容量与单次激活成本分开。

## 一个例子

八个专家、每 token 选一个，可以增大总参数而不让每 token 都执行八个 FFN；但热门专家仍可能排队。常见短语若走哈希记忆表，又把一部分计算换成查表和带宽。这两种稀疏并不消除通信、寻址或参数驻留成本。

## 什么时候要小心

专家数增加不等于吞吐按比例提高；路由不均、容量溢出和 all-to-all 可能主导成本。查表存在碰撞与容量权衡，循环层也会增加时延。不要把随机路由诊断或新增 registry 标签当作能力或 evolve 集成证据。

## 先读这几篇

先读 Switch 的 top-1 专家和均衡约束，再读 Engram 的确定性查表与门控融合，区分条件计算和条件记忆；随后按瓶颈选择动态深宽、循环或路由工作。

1. [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](../../../reproductions/2101.03961-switch-transformer/README.md) · [原论文](https://arxiv.org/abs/2101.03961)
2. [Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models](../../../reproductions/2601.07372-engram/README.md) · [原论文](https://arxiv.org/abs/2601.07372)

## 自测一下

一个 80B MoE 每 token 激活 8B 参数，是否就只需要存放 8B 参数？

??? note "展开参考答案"

    不是。激活参数描述本次计算，所有可被路由到的专家仍需驻留或从其他存储加载；显存、通信和单步 FLOPs 是不同预算。应同时报告总参数、激活参数及实测运行成本。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
