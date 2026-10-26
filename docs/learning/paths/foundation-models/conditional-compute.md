---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 按需计算：专家、弹性深宽与查表记忆

[基础模型](index.md) / 子主题导学 · 约 3 分钟 · 26 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 26 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Rethinking Routing Exploration in Modern Mixture-of-Experts 基础模型 ETH Zurich 2026-10-15 共享专家占据较多输出后，改变路由专家带来的表征差异减弱，而细粒度分割又扩大组合空间。MirrorMoE 不简单增噪，而是以镜像选择暂时抑制部分专家，随训练退火恢复普通路由。主源是 §3 的公式 3–6。 现有单 A100/A30/Mac 不运行此完整预训练，成本过高，不复现（审查 DONE）。CUDA 诊断记录与真实GPU回执列出设备与源码 hash。revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1；无 checkpoint、公共语料或能力 benchmark。固定种子 42/43/44 初始化 8 维、6 个可路由专家、2 个共享专家、top-3 的真实可训练小网络。每 seed 仅一个 SGD 更新核验梯度，不是语言模型训练。  网络架构 混合专家路由 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-mirror-moe-43695dbb">Rethinking Routing Exploration in Modern Mixture-of-Experts</h2>
<p class="ar-learning-card__meta">ETH Zurich · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>共享专家占据较多输出后，改变路由专家带来的表征差异减弱，而细粒度分割又扩大组合空间。MirrorMoE 不简单增噪，而是以镜像选择暂时抑制部分专家，随训练退火恢复普通路由。主源是 §3 的公式 3–6。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>现有单 A100/A30/Mac 不运行此完整预训练，成本过高，不复现（审查 DONE）。CUDA 诊断记录与真实GPU回执列出设备与源码 hash。revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1；无 checkpoint、公共语料或能力 benchmark。固定种子 42/43/44 初始化 8 维、6 个可路由专家、2 个共享专家、top-3 的真实可训练小网络。每 seed 仅一个 SGD 更新核验梯度，不是语言模型训练。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22353">原论文</a> · <a href="../../../../foundation-models/2610.22353-mirror-moe/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Patch where the text is new: a compression view of where byte-level models should spend compute 基础模型 Independent Researcher, Chile 2026-10-15 Byte-level 模型按 patch 调用全局模型。本文用近期重复程度预测替代纯熵边界；离线计算匹配标签，在线只查前两字节。主源位置为 §3 方法、§4-7 结果及负结果、§8 限制和 Code and data。 这一多臂完整链路超出单张 A100/A30 或 Mac 的本轮低成本预算，故成本过高，不复现（审查 DONE）。仅实现训练标签、两级低频回退、训练集阈值和严格因果边界。原文 4 MB 拟表在本次缩为 262,144 byte 的已有公开训练文本；不训练 BLT、不评测答案准确率。  字节级模型 因果patch边界 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-novelty-patching-3454dd1e">Patch where the text is new: a compression view of where byte-level models should spend compute</h2>
<p class="ar-learning-card__meta">Independent Researcher, Chile · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>Byte-level 模型按 patch 调用全局模型。本文用近期重复程度预测替代纯熵边界；离线计算匹配标签，在线只查前两字节。主源位置为 §3 方法、§4-7 结果及负结果、§8 限制和 Code and data。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>这一多臂完整链路超出单张 A100/A30 或 Mac 的本轮低成本预算，故成本过高，不复现（审查 DONE）。仅实现训练标签、两级低频回退、训练集阈值和严格因果边界。原文 4 MB 拟表在本次缩为 262,144 byte 的已有公开训练文本；不训练 BLT、不评测答案准确率。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22100">原论文</a> · <a href="../../../../foundation-models/2610.22100-novelty-patching/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Multi-Stream Attention Residuals 基础模型 Shanghai Jiao Tong University 2026-10-09 标准残差把历史更新压成一个累加向量；AttnRes 能逐层检索，但只有一个深度注意力流。MSAR 保留每个完整 hidden 向量，用序列上下文产生不同尺度的完整视图，再对每个流独立做深度 softmax。与切分通道的多头不同，它不破坏 value 的全维表示。Block MSAR 只持久保存 embedding、已完成 block 的单流摘要和当前 block 的部分和，消费时再展开；不会把所有卷积视图永久写回。卷积 kernel 为 4/8/12，加 identity 流共四流； 正式本地相对收益不适用，当前只有机制诊断，少量步骤/单 seed 不能支持稳定提升结论。本地对照口径：匹配的真实 dense causal Transformer 为基线，MSAR 为实验组；正式本地相对收益不适用，当前只有机制诊断，少量步骤/单 seed 不能支持稳定提升结论。  llm-architecture depth-attention residual-mixing 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-msar-f6753b95">Multi-Stream Attention Residuals</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>标准残差把历史更新压成一个累加向量；AttnRes 能逐层检索，但只有一个深度注意力流。MSAR 保留每个完整 hidden 向量，用序列上下文产生不同尺度的完整视图，再对每个流独立做深度 softmax。与切分通道的多头不同，它不破坏 value 的全维表示。Block MSAR 只持久保存 embedding、已完成 block 的单流摘要和当前 block 的部分和，消费时再展开；不会把所有卷积视图永久写回。卷积 kernel 为 4/8/12，加 identity 流共四流；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>正式本地相对收益不适用，当前只有机制诊断，少量步骤/单 seed 不能支持稳定提升结论。本地对照口径：匹配的真实 dense causal Transformer 为基线，MSAR 为实验组；正式本地相对收益不适用，当前只有机制诊断，少量步骤/单 seed 不能支持稳定提升结论。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13630">原论文</a> · <a href="../../../../reproductions/2610.13630-msar/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="CoTS: Competitive Token Selection for Latent Reasoning in Large Language Models 基础模型 Xiaomi AI Lab 2026-10-08 连续 reasoning 的 soft token 可能偏离离散轨迹。CoTS 用 top-2 概率竞争分配 soft 混合强度，保留 sampled token 至少半数权重，并在结束推理后锁定纯离散输出。主源为 §3.1-3.3 的公式 1-6；实验配置和消融见 §4。 按公开配置，完整研究超出本轮单 A100/A30 或 Mac 低成本预算，成本过高，不复现（审查 DONE）。只实现概率竞争、top-k soft embedding、离散锚点、逐样本不可逆 phase-lock 和 EOS 状态；sampled token 可在 top-k 之外。输入概率与 embedding 的 autograd 链路均保留，未转 numpy、未以 straight-through 伪梯度代替。保护 token ID 与 tokenizer/end-think ID 由调用方明确提供，不猜默认表。  连续推理 概率竞争与离散锚点 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-cots-9dd74b8e">CoTS: Competitive Token Selection for Latent Reasoning in Large Language Models</h2>
<p class="ar-learning-card__meta">Xiaomi AI Lab · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>连续 reasoning 的 soft token 可能偏离离散轨迹。CoTS 用 top-2 概率竞争分配 soft 混合强度，保留 sampled token 至少半数权重，并在结束推理后锁定纯离散输出。主源为 §3.1-3.3 的公式 1-6；实验配置和消融见 §4。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>按公开配置，完整研究超出本轮单 A100/A30 或 Mac 低成本预算，成本过高，不复现（审查 DONE）。只实现概率竞争、top-k soft embedding、离散锚点、逐样本不可逆 phase-lock 和 EOS 状态；sampled token 可在 top-k 之外。输入概率与 embedding 的 autograd 链路均保留，未转 numpy、未以 straight-through 伪梯度代替。保护 token ID 与 tokenizer/end-think ID 由调用方明确提供，不猜默认表。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20642">原论文</a> · <a href="../../../../foundation-models/2610.20642-cots/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Smoothing the Top-k Exposure Boundary for Sparse Mixture-of-Experts 基础模型 Shanghai AI Laboratory / Shanghai Jiao Tong University 2026-10-08 固定 Top-k 会让排序边界外的专家长期缺少训练曝光。该方法训练时为每个 token、每层独立抽取邻近的专家预算，在不改变期望预算的情况下，让边界附近专家参与真实稀疏计算。部署时恢复固定 k。 本地结果标为诊断。实现真实因果自回归 Transformer + 稀疏 MoE，包含 router、专家梯度、辅助均衡损失和固定 k 推理。不是把所有专家都计算一遍后乘零。相同参数形状、初始化、训练位置和预算对照 radius=0 与 radius=1。  稀疏专家与路由 网络架构 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-elastic-expert-routing-bd240699">Smoothing the Top-k Exposure Boundary for Sparse Mixture-of-Experts</h2>
<p class="ar-learning-card__meta">Shanghai AI Laboratory / Shanghai Jiao Tong University · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>固定 Top-k 会让排序边界外的专家长期缺少训练曝光。该方法训练时为每个 token、每层独立抽取邻近的专家预算，在不改变期望预算的情况下，让边界附近专家参与真实稀疏计算。部署时恢复固定 k。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地结果标为诊断。实现真实因果自回归 Transformer + 稀疏 MoE，包含 router、专家梯度、辅助均衡损失和固定 k 推理。不是把所有专家都计算一遍后乘零。相同参数形状、初始化、训练位置和预算对照 radius=0 与 radius=1。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11575">原论文</a> · <a href="../../../../foundation-models/2610.11575-elastic-expert-routing/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference 基础模型 Westlake University 2026-10-08 固定文本的 teacher-forcing 激活不等于模型自回归生成时的激活。该方法让稠密模型先从任务问题生成回答，只保存逐 token 解码激活、排除 prefill，再用这些统计量执行剪枝。校准协议与剪枝后端分离：原文主要使用 SparseGPT，也报告 Wanda 消融。系统部分针对 batch-one 解码的矩阵向量乘法：每连续 32 列用一个 32-bit word 标记保留位置；50% 稀疏时恰有 16 个 set bit，按递增列位置打包数值并固定遍历 16 次。 已实现 decoding-only 校准、Wanda N:M 剪枝和真实 Triton bitmask SpMV，并在 A100 运行 Qwen3-4B。当前是 L1 机制诊断；本地结果质量下降且没有加速，不代表原论文大模型实验复现。此入口要求 NVIDIA CUDA 与 Linux Triton；Mac 可以运行公式和打包单测，不能运行稀疏 GPU 路径。公开 checkpoint 下载、训练集派生 holdout 见运行指南。  推理与系统效率 动态计算与模型压缩 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-sparse-decoding-1beb4b13">SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference</h2>
<p class="ar-learning-card__meta">Westlake University · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>固定文本的 teacher-forcing 激活不等于模型自回归生成时的激活。该方法让稠密模型先从任务问题生成回答，只保存逐 token 解码激活、排除 prefill，再用这些统计量执行剪枝。校准协议与剪枝后端分离：原文主要使用 SparseGPT，也报告 Wanda 消融。系统部分针对 batch-one 解码的矩阵向量乘法：每连续 32 列用一个 32-bit word 标记保留位置；50% 稀疏时恰有 16 个 set bit，按递增列位置打包数值并固定遍历 16 次。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>已实现 decoding-only 校准、Wanda N:M 剪枝和真实 Triton bitmask SpMV，并在 A100 运行 Qwen3-4B。当前是 L1 机制诊断；本地结果质量下降且没有加速，不代表原论文大模型实验复现。此入口要求 NVIDIA CUDA 与 Linux Triton；Mac 可以运行公式和打包单测，不能运行稀疏 GPU 路径。公开 checkpoint 下载、训练集派生 holdout 见运行指南。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12327">原论文</a> · <a href="../../../../foundation-models/2610.12327-sparse-decoding/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Cross-Entropy Guided Routing in Mixture-of-Experts Large Language Models 基础模型 Bar-Ilan University 2026-09-29 在原生 MoE affinity 旁增加逐 expert token-error head，并用预测误差的 started-log 对路由 logit 做衰减；高预测错误的 expert 在 Top-K 前被降权，同时误差头由真实 next-token CE 监督。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 error-aware routing 公式；未训练 Granite MoE。执行 error-aware routing 公式；未训练 Granite MoE。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  MoE 路由 Token error 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-ce-guided-moe-5d9cde32">Cross-Entropy Guided Routing in Mixture-of-Experts Large Language Models</h2>
<p class="ar-learning-card__meta">Bar-Ilan University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>在原生 MoE affinity 旁增加逐 expert token-error head，并用预测误差的 started-log 对路由 logit 做衰减；高预测错误的 expert 在 Top-K 前被降权，同时误差头由真实 next-token CE 监督。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 error-aware routing 公式；未训练 Granite MoE。执行 error-aware routing 公式；未训练 Granite MoE。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37751">原论文</a> · <a href="../../../../foundation-models/2609.37751-ce-guided-moe/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Pretraining Latent Information Feedback Transformers with Teacher Supervision 基础模型 Tel Aviv University 2026-09-29 普通 Transformer 的深层信息只能通过下一个离散 token 回到浅层。LIFT 把 teacher 的下一 token top-k 分布预计算成连续状态；训练时 token 与 teacher state 并行输入，同时预测下一 token 和下一 state；推理时改用模型自己的 state。核心目标是 token CE 加 teacher top-k 分布的前向 KL。 复现级别：L1 核心机制。复现级别：L1 核心机制。实现 top-k 分布状态、token/state SwiGLU 融合和 CE + state KL；未训练 135M–1B 模型。lift_topk_state 保留并归一化 top-k logits；lift_fuse 用共享 embedding 投影 state 并做 residual SwiGLU；lift_loss 组合两个目标。测试覆盖稀疏归一化、反馈改变输出及 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。  网络架构 潜状态反馈 预训练 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-lift-feedback-608d6327">Pretraining Latent Information Feedback Transformers with Teacher Supervision</h2>
<p class="ar-learning-card__meta">Tel Aviv University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>普通 Transformer 的深层信息只能通过下一个离散 token 回到浅层。LIFT 把 teacher 的下一 token top-k 分布预计算成连续状态；训练时 token 与 teacher state 并行输入，同时预测下一 token 和下一 state；推理时改用模型自己的 state。核心目标是 token CE 加 teacher top-k 分布的前向 KL。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 核心机制。复现级别：L1 核心机制。实现 top-k 分布状态、token/state SwiGLU 融合和 CE + state KL；未训练 135M–1B 模型。lift_topk_state 保留并归一化 top-k logits；lift_fuse 用共享 embedding 投影 state 并做 residual SwiGLU；lift_loss 组合两个目标。测试覆盖稀疏归一化、反馈改变输出及 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38149">原论文</a> · <a href="../../../../foundation-models/2609.38149-lift-feedback/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Telescopic Language Models 基础模型 University of Cambridge 2026-09-28 每步随机抽一个网络深度前缀做 next-token 监督，同时保留全深度 anchor，使同一 checkpoint 的每个深度都成为可用语言模型。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。验证随机深度和 full anchor 的梯度路径；未做 20B-token 预训练。验证随机深度和 full anchor 的梯度路径；未做 20B-token 预训练。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  网络架构 弹性深度 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-telescopic-lm-c2ab9fe1">Telescopic Language Models</h2>
<p class="ar-learning-card__meta">University of Cambridge · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>每步随机抽一个网络深度前缀做 next-token 监督，同时保留全深度 anchor，使同一 checkpoint 的每个深度都成为可用语言模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。验证随机深度和 full anchor 的梯度路径；未做 20B-token 预训练。验证随机深度和 full anchor 的梯度路径；未做 20B-token 预训练。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35769">原论文</a> · <a href="../../../../foundation-models/2609.35769-telescopic-lm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Persistent Recurrent Memory Between Transformer Layers Improves Language Model Generalization 基础模型 FITec Labs / Ericsson São Paulo 2026-09-15 在 Transformer 上下半层之间插入 observe–GRU update–gated influence 的持久状态通路。 未复现 TinyStories 完整训练曲线。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行拓扑 reference kernel；未复现 TinyStories 完整训练曲线。本地执行拓扑 reference kernel；未复现 TinyStories 完整训练曲线。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  网络架构 持久记忆 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-persistent-recurrent-memory-f4545966">Persistent Recurrent Memory Between Transformer Layers Improves Language Model Generalization</h2>
<p class="ar-learning-card__meta">FITec Labs / Ericsson São Paulo · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>在 Transformer 上下半层之间插入 observe–GRU update–gated influence 的持久状态通路。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>未复现 TinyStories 完整训练曲线。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行拓扑 reference kernel；未复现 TinyStories 完整训练曲线。本地执行拓扑 reference kernel；未复现 TinyStories 完整训练曲线。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17251">原论文</a> · <a href="../../../../foundation-models/2609.17251-persistent-recurrent-memory/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Data Scarcity and Model Sparsity: Mixtures-of-Experts Overfit More to Repeated Data 基础模型 Stanford University 2026-09-10 研究重复数据下 MoE 比 Dense 更早过拟合的问题，并用更强 masking/dropout 抑制 expert 记忆化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地实现随重复倍数和稀疏度变化的正则 schedule；未进行大规模预训练。本地实现随重复倍数和稀疏度变化的正则 schedule；未进行大规模预训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  MoE 数据重复与正则化 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-repeat-aware-moe-d00603e8">Data Scarcity and Model Sparsity: Mixtures-of-Experts Overfit More to Repeated Data</h2>
<p class="ar-learning-card__meta">Stanford University · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>研究重复数据下 MoE 比 Dense 更早过拟合的问题，并用更强 masking/dropout 抑制 expert 记忆化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地实现随重复倍数和稀疏度变化的正则 schedule；未进行大规模预训练。本地实现随重复倍数和稀疏度变化的正则 schedule；未进行大规模预训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11917">原论文</a> · <a href="../../../../foundation-models/2609.11917-repeat-aware-moe/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="SWRouter: Similarity-Contractive Window Routing for Multi-Turn Large Language Model Conversations 基础模型 Shanghai Jiao Tong University 2026-09-10 按相邻语义相似度收缩多轮窗口，再用对比路由器选模型，并分开评测上下文构造和路由正确性。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行窗口分段和 profile overlap 路由；未训练论文对比 encoder。本地执行窗口分段和 profile overlap 路由；未训练论文对比 encoder。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  模型路由 多轮上下文 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-swrouter-da0aa5dd">SWRouter: Similarity-Contractive Window Routing for Multi-Turn Large Language Model Conversations</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong University · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>按相邻语义相似度收缩多轮窗口，再用对比路由器选模型，并分开评测上下文构造和路由正确性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行窗口分段和 profile overlap 路由；未训练论文对比 encoder。本地执行窗口分段和 profile overlap 路由；未训练论文对比 encoder。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11414">原论文</a> · <a href="../../../../foundation-models/2609.11414-swrouter/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations 基础模型 Beijing University of Posts and Telecommunications / Kuaishou Technology 2026-09-03 Lngram v2 把 backbone hidden state 投影成多路二进制地址，以最近 1/2-gram 的离散组合 O(1) 查 memory table；多个 route token 经 GQA 读回主干。硬地址保证表示可解释，反事实邻接地址提供训练梯度，零 Sink 允许模型拒绝无用记忆。 复现级别：核心机制 + 真实 VLM checkpoint GPU 验证。复现级别：核心机制 + 真实 VLM checkpoint GPU 验证。实现多路离散寻址、精确 n-gram 查表、反事实 surrogate gradient 和带零 Sink 的 GQA 读出。未执行 Keye 2B/30B 全量预训练或论文规模语料；GPU 验证只声明真实公开 VLM hidden state 上的机制、梯度和显存可执行，可作为 LLM/多模态 Evolve memory 算子。CPU 三 seed 机制结果见 metrics/public-seeds42-44.json；  multimodal-foundation-model conditional-memory discrete-routing model-architecture 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-lngram-v2-f7907f6f">Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations</h2>
<p class="ar-learning-card__meta">Beijing University of Posts and Telecommunications / Kuaishou Technology · 论文公开：2026-09-03</p>
<p><strong>方法要点：</strong>Lngram v2 把 backbone hidden state 投影成多路二进制地址，以最近 1/2-gram 的离散组合 O(1) 查 memory table；多个 route token 经 GQA 读回主干。硬地址保证表示可解释，反事实邻接地址提供训练梯度，零 Sink 允许模型拒绝无用记忆。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 真实 VLM checkpoint GPU 验证。复现级别：核心机制 + 真实 VLM checkpoint GPU 验证。实现多路离散寻址、精确 n-gram 查表、反事实 surrogate gradient 和带零 Sink 的 GQA 读出。未执行 Keye 2B/30B 全量预训练或论文规模语料；GPU 验证只声明真实公开 VLM hidden state 上的机制、梯度和显存可执行，可作为 LLM/多模态 Evolve memory 算子。CPU 三 seed 机制结果见 metrics/public-seeds42-44.json；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.03426">原论文</a> · <a href="../../../../reproductions/2609.03426-lngram-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models 基础模型 Huazhong University of Science and Technology 2026-08-21 Dense LLM 的 activation steering 直接用于 MoE 时会改变 router logits，token 被送往不同专家后，原估计的行为方向失效。RARE 将任意 steering direction 投影到 router 的零空间，并在后续保护层再次移除传播产生的 router-visible 分量，在保留原专家路径的同时改变行为表征。 未加载 DeepSeek-V2-Lite、Mixtral、Phi、Qwen3 或 GPT-OSS，也未运行 JailbreakBench、TruthfulQA、CounterFact。Fidelity: 核心机制复现。真实执行 router 行空间 SVD、零空间投影、路由一致性和下游校正；未加载论文六个大 MoE checkpoint。未加载 DeepSeek-V2-Lite、Mixtral、Phi、Qwen3 或 GPT-OSS，也未运行 JailbreakBench、TruthfulQA、CounterFact。这里验证的是论文式 (8) 的精确路由不变性，不把合成 steering 指标冒充论文下游效果。  llm-architecture mixture-of-experts representation-steering model-editing 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-rare-2c269dff">RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models</h2>
<p class="ar-learning-card__meta">Huazhong University of Science and Technology · 论文公开：2026-08-21</p>
<p><strong>方法要点：</strong>Dense LLM 的 activation steering 直接用于 MoE 时会改变 router logits，token 被送往不同专家后，原估计的行为方向失效。RARE 将任意 steering direction 投影到 router 的零空间，并在后续保护层再次移除传播产生的 router-visible 分量，在保留原专家路径的同时改变行为表征。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未加载 DeepSeek-V2-Lite、Mixtral、Phi、Qwen3 或 GPT-OSS，也未运行 JailbreakBench、TruthfulQA、CounterFact。Fidelity: 核心机制复现。真实执行 router 行空间 SVD、零空间投影、路由一致性和下游校正；未加载论文六个大 MoE checkpoint。未加载 DeepSeek-V2-Lite、Mixtral、Phi、Qwen3 或 GPT-OSS，也未运行 JailbreakBench、TruthfulQA、CounterFact。这里验证的是论文式 (8) 的精确路由不变性，不把合成 steering 指标冒充论文下游效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21236">原论文</a> · <a href="../../../../reproductions/2608.21236-rare/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="MACRO: Markov Chain Routing of Transformer Layers 基础模型 Heinrich Heine University Düsseldorf 2026-08-06 主题：动态层路由。固定顺序执行所有 Transformer 层并非总是最优。MACRO 用上下文条件 Markov policy 表示 skip、repeat、residual-add 等操作，再用反馈更新路由分布和 top-k Viterbi 解码候选程序，不修改底座权重。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。在确定性分类 mini-suite 搜索 81 条 skip/repeat/residual 路由；同时作为 micro-LLM evolve 的可选结构。  network-architecture dynamic-routing inference-efficiency 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-macro-6eaa3033">MACRO: Markov Chain Routing of Transformer Layers</h2>
<p class="ar-learning-card__meta">Heinrich Heine University Düsseldorf · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>主题：动态层路由。固定顺序执行所有 Transformer 层并非总是最优。MACRO 用上下文条件 Markov policy 表示 skip、repeat、residual-add 等操作，再用反馈更新路由分布和 top-k Viterbi 解码候选程序，不修改底座权重。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。在确定性分类 mini-suite 搜索 81 条 skip/repeat/residual 路由；同时作为 micro-LLM evolve 的可选结构。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05872">原论文</a> · <a href="../../../../reproductions/2608.05872-macro/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Role-Decoupled Attention Residuals 基础模型 Kehan Wang（论文未列机构） 2026-08-03 Block AttnRes 让注意力层从全部历史 residual sources 动态读取，但 Q、K、V 共用一条深度路由。论文指出 QK 负责匹配、V 负责承载内容，两者偏好的深度未必相同；RD-AttnRes 在不改变 residual sources 和 attention 主体的情况下，只为 V 增加一个 model-width 路由向量。 Fidelity：核心机制复现。以共享路由的 Block AttnRes 为严格匹配基线，只增加 V 专属路由。未复刻 120M/343M 预训练规模和原论文语料；本地仅验证匹配的结构消融与 evolve 接入。本地对照口径：基线为共享深度路由的 Block AttnRes，实验组仅解耦 QK/V route；相对基线 PPL +0.61%（变差）。  foundation-model attention residual-routing 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-rd-attnres-0af1c94e">Role-Decoupled Attention Residuals</h2>
<p class="ar-learning-card__meta">Kehan Wang（论文未列机构） · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>Block AttnRes 让注意力层从全部历史 residual sources 动态读取，但 Q、K、V 共用一条深度路由。论文指出 QK 负责匹配、V 负责承载内容，两者偏好的深度未必相同；RD-AttnRes 在不改变 residual sources 和 attention 主体的情况下，只为 V 增加一个 model-width 路由向量。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。以共享路由的 Block AttnRes 为严格匹配基线，只增加 V 专属路由。未复刻 120M/343M 预训练规模和原论文语料；本地仅验证匹配的结构消融与 evolve 接入。本地对照口径：基线为共享深度路由的 Block AttnRes，实验组仅解耦 QK/V route；相对基线 PPL +0.61%（变差）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01075">原论文</a> · <a href="../../../../reproductions/2608.01075-rd-attnres/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning 基础模型 EIT-NLP / LMU Munich 2026-07-30 静态剪枝无法按 token 难度分配算力，动态深度又过于粗粒度。WIDE 对每个 token 分别路由 attention head group 和 FFN channel group，并将 mask reorder、block skip 与设备内跳过联合设计。 Fidelity: 核心机制复现。实际训练 attention-head group 与 FFN-channel group router，并接入 LLM evolve。PyTorch dense kernel 不会因 mask 自动加速，因此只验证 router、稀疏率和质量变化，不冒充论文 CUDA 性能。本地对照口径：基线为同预算 dense LLaMA；实验组固定激活 50% head/channel，相对基线 perplexity +0.81%（轻微退化）。  llm-architecture dynamic-pruning inference-efficiency 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-wide-0e0ca0da">WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning</h2>
<p class="ar-learning-card__meta">EIT-NLP / LMU Munich · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>静态剪枝无法按 token 难度分配算力，动态深度又过于粗粒度。WIDE 对每个 token 分别路由 attention head group 和 FFN channel group，并将 mask reorder、block skip 与设备内跳过联合设计。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际训练 attention-head group 与 FFN-channel group router，并接入 LLM evolve。PyTorch dense kernel 不会因 mask 自动加速，因此只验证 router、稀疏率和质量变化，不冒充论文 CUDA 性能。本地对照口径：基线为同预算 dense LLaMA；实验组固定激活 50% head/channel，相对基线 perplexity +0.81%（轻微退化）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28418">原论文</a> · <a href="../../../../reproductions/2607.28418-wide/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Penelope: Localized Latent Recurrence for Efficient Structured Reasoning 基础模型 Academic author team 2026-07-28 只在一个 decoder 边界执行共享权重的 latent recurrence，用门控状态反复精炼表示，避免整条 decoder 重跑。 Fidelity: 核心机制复现。本地执行局部潜在递归与门控状态更新；不复刻原论文的大模型训练规模。12-step 本地预算不包含论文规模 checkpoint 和 CoT-to-latent curriculum，只验证真实 PyTorch 结构路径。本地对照口径：基线为 llama_modern，实验组为 penelope；composite loss 从 6.9539 降到 6.9100，相对改善 0.63%。  llm-architecture latent-reasoning recurrence efficiency 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-penelope-d7b5f7a1">Penelope: Localized Latent Recurrence for Efficient Structured Reasoning</h2>
<p class="ar-learning-card__meta">Academic author team · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>只在一个 decoder 边界执行共享权重的 latent recurrence，用门控状态反复精炼表示，避免整条 decoder 重跑。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行局部潜在递归与门控状态更新；不复刻原论文的大模型训练规模。12-step 本地预算不包含论文规模 checkpoint 和 CoT-to-latent curriculum，只验证真实 PyTorch 结构路径。本地对照口径：基线为 llama_modern，实验组为 penelope；composite loss 从 6.9539 降到 6.9100，相对改善 0.63%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25915">原论文</a> · <a href="../../../../reproductions/2607.25915-penelope/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs 基础模型 Huawei ACS Lab / Southern University of Science and Technology 2026-07-23 固定比例的 Mixture-of-Depths 会给每一层相同 token budget，但不同层对表示的改写强度并不相同。AdaDSF 先在 dense teacher 上测量各层输入/输出 cosine similarity，再把更多计算分给变化更大的层；每层 MLP router 只把 Top-K token 送入原 Transformer block，其他 token 走 residual bypass。最后同时对齐中间 hidden states 和输出分布。 Fidelity: 核心机制复现。真实执行 dense calibration、逐层 token budget 分配、Top-K router 和特征对齐；缩小模型与训练预算。未下载 GPT-NeoX-130M/Qwen2.5 和 WikiText-103，而是在本地 WikiText-2 微型 decoder 上验证算法链路；normalized active-token fraction 不是 GPU kernel 的实测 FLOPs。Top-K block 确实只处理选中 token，不是输出后 masking，但没有论文大模型 kernel 优化与六项完整 commonsense 评测。  llm-architecture efficient-inference token-routing 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-adadsf-0ee93157">Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs</h2>
<p class="ar-learning-card__meta">Huawei ACS Lab / Southern University of Science and Technology · 论文公开：2026-07-23</p>
<p><strong>方法要点：</strong>固定比例的 Mixture-of-Depths 会给每一层相同 token budget，但不同层对表示的改写强度并不相同。AdaDSF 先在 dense teacher 上测量各层输入/输出 cosine similarity，再把更多计算分给变化更大的层；每层 MLP router 只把 Top-K token 送入原 Transformer block，其他 token 走 residual bypass。最后同时对齐中间 hidden states 和输出分布。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。真实执行 dense calibration、逐层 token budget 分配、Top-K router 和特征对齐；缩小模型与训练预算。未下载 GPT-NeoX-130M/Qwen2.5 和 WikiText-103，而是在本地 WikiText-2 微型 decoder 上验证算法链路；normalized active-token fraction 不是 GPU kernel 的实测 FLOPs。Top-K block 确实只处理选中 token，不是输出后 masking，但没有论文大模型 kernel 优化与六项完整 commonsense 评测。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21291">原论文</a> · <a href="../../../../reproductions/2607.21291-adadsf/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers 基础模型 University of Maryland / Meta AI 2026-07-16 Looped Transformer 重复使用同一组权重，但不同 loop 的 KV cache 仍重复占内存。LLA 学习跨 loop 共享的低秩 K/V latent，服务时按 loop 重建专用 K/V，从 recurrence 冗余中换取近无损压缩。 Fidelity: 核心机制复现。训练权重共享的 looped block，并在共享 latent 中保存 K/V。本地从头训练 64d 模型，不是对大 checkpoint 训练 post-hoc codec，也没有 fused serving kernel。本地对照口径：基线是两层 llama_modern；实验组用一个权重共享 block 循环两次并采用 2× K/V latent，LM loss 5.7471→5.8012，相对 +0.94%（更差），参数 139584→80576。  llm-architecture kv-cache looped-transformer 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-looped-latent-attention-49effa17">Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers</h2>
<p class="ar-learning-card__meta">University of Maryland / Meta AI · 论文公开：2026-07-16</p>
<p><strong>方法要点：</strong>Looped Transformer 重复使用同一组权重，但不同 loop 的 KV cache 仍重复占内存。LLA 学习跨 loop 共享的低秩 K/V latent，服务时按 loop 重建专用 K/V，从 recurrence 冗余中换取近无损压缩。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。训练权重共享的 looped block，并在共享 latent 中保存 K/V。本地从头训练 64d 模型，不是对大 checkpoint 训练 post-hoc codec，也没有 fused serving kernel。本地对照口径：基线是两层 llama_modern；实验组用一个权重共享 block 循环两次并采用 2× K/V latent，LM loss 5.7471→5.8012，相对 +0.94%（更差），参数 139584→80576。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15456">原论文</a> · <a href="../../../../reproductions/2607.15456-looped-latent-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory 基础模型 Tsinghua University / Microsoft Research Asia 2026-05-20 Engram 的大容量条件记忆需要随主模型从零训练。Memory Grafting 先统计高频 2/3/4-gram，用已经预训练的 grafting model 离线编码每个短语最后 token 的中间 hidden state并冻结；recipient 在线只做期望的最长后缀精确查询。未命中时回退到可训练 hash Engram，命中值经独立投影、上下文门控、短卷积后写回 residual stream。 结果说明完整 grafting 路径有效且优于无记忆模型，但当前 bank 太小，未验证相对 Engram 的增益。Fidelity: 核心机制复现。实际训练 grafting model 与 recipient，执行冻结 n-gram hidden bank、最长精确匹配、Engram fallback、query-key gate、短卷积和残差写入。64-d dense recipient、微型 teacher 与 192-entry bank 替代论文 0.92B/2.8B MoE、Qwen3.5/DeepSeek grafting model、50B/100B tokens 和 3M-entry bank；  llm-pretraining conditional-memory offline-knowledge-transfer 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-memory-grafting-16992e0e">Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory</h2>
<p class="ar-learning-card__meta">Tsinghua University / Microsoft Research Asia · 论文公开：2026-05-20</p>
<p><strong>方法要点：</strong>Engram 的大容量条件记忆需要随主模型从零训练。Memory Grafting 先统计高频 2/3/4-gram，用已经预训练的 grafting model 离线编码每个短语最后 token 的中间 hidden state并冻结；recipient 在线只做期望的最长后缀精确查询。未命中时回退到可训练 hash Engram，命中值经独立投影、上下文门控、短卷积后写回 residual stream。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>结果说明完整 grafting 路径有效且优于无记忆模型，但当前 bank 太小，未验证相对 Engram 的增益。Fidelity: 核心机制复现。实际训练 grafting model 与 recipient，执行冻结 n-gram hidden bank、最长精确匹配、Engram fallback、query-key gate、短卷积和残差写入。64-d dense recipient、微型 teacher 与 192-entry bank 替代论文 0.92B/2.8B MoE、Qwen3.5/DeepSeek grafting model、50B/100B tokens 和 3M-entry bank；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.20948">原论文</a> · <a href="../../../../reproductions/2605.20948-memory-grafting/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Optimized Deferral for Imbalanced Settings 基础模型 Google Research 2026-04-30 少数覆盖的专用专家容易被多数专家淹没。论文通过对不同专家设置不同margin约束来平衡学习。保留训练奖励而非以argmin成本生成单一硬标签；这是v1 §5.3 mild目标、§4.2 margin建议的低成本实现。 原完整图像200epoch、多专家、5run及多LLM评测成本过高，不复现（审查DONE），不为这轮下载大型专家。4条自建线性可分夹具，仅作100步目标优化与解析梯度有限差分检查，不是泛化test。对齐原文分数并列时选择最高专家索引。稳定结果见metrics/component-cpu-seed42.json，diagnostic_only=true，不提供真实专家能力或evolve改善证据。  模型路由 不平衡cost-sensitive学习 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-mild-b3546e10">Optimized Deferral for Imbalanced Settings</h2>
<p class="ar-learning-card__meta">Google Research · 论文公开：2026-04-30</p>
<p><strong>方法要点：</strong>少数覆盖的专用专家容易被多数专家淹没。论文通过对不同专家设置不同margin约束来平衡学习。保留训练奖励而非以argmin成本生成单一硬标签；这是v1 §5.3 mild目标、§4.2 margin建议的低成本实现。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原完整图像200epoch、多专家、5run及多LLM评测成本过高，不复现（审查DONE），不为这轮下载大型专家。4条自建线性可分夹具，仅作100步目标优化与解析梯度有限差分检查，不是泛化test。对齐原文分数并列时选择最高专家索引。稳定结果见metrics/component-cpu-seed42.json，diagnostic_only=true，不提供真实专家能力或evolve改善证据。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.27723">原论文</a> · <a href="../../../../foundation-models/2604.27723-mild/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models 基础模型 DeepSeek 2026-01-12 MoE 只增加条件计算，模型仍需用计算层反复重建静态局部模式。Engram 把规范化 n-gram 哈希到大 embedding table，进行确定性的 lookup，并在早期层门控注入，让 attention/FFN 留给组合推理。 未执行 27B/MoE 规模预训练、分布式表和异步预取；Fidelity: 核心机制复现。真实训练 hashed n-gram memory、门控融合，并接入 LLM evolve。未执行 27B/MoE 规模预训练、分布式表和异步预取；本地验证的是可学习查表路径，而非论文 benchmark 复刻。本地对照口径：基线是同预算 llama_modern；实验组加入 4096-bucket trigram memory，WikiText-2 LM loss 5.7471→6.1533，相对 +7.07%（更差），PPL 313.27→470.27。  llm-architecture conditional-memory sparsity 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-engram-7eeee5b9">Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models</h2>
<p class="ar-learning-card__meta">DeepSeek · 论文公开：2026-01-12</p>
<p><strong>方法要点：</strong>MoE 只增加条件计算，模型仍需用计算层反复重建静态局部模式。Engram 把规范化 n-gram 哈希到大 embedding table，进行确定性的 lookup，并在早期层门控注入，让 attention/FFN 留给组合推理。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未执行 27B/MoE 规模预训练、分布式表和异步预取；Fidelity: 核心机制复现。真实训练 hashed n-gram memory、门控融合，并接入 LLM evolve。未执行 27B/MoE 规模预训练、分布式表和异步预取；本地验证的是可学习查表路径，而非论文 benchmark 复刻。本地对照口径：基线是同预算 llama_modern；实验组加入 4096-bucket trigram memory，WikiText-2 LM loss 5.7471→6.1533，相对 +7.07%（更差），PPL 313.27→470.27。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.07372">原论文</a> · <a href="../../../../reproductions/2601.07372-engram/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="mHC: Manifold-Constrained Hyper-Connections 基础模型 DeepSeek-AI 2025-12-31 Hyper-Connections 把单一 residual stream 扩为多个流并动态混合，但任意残差矩阵会破坏 identity mapping，深层组合可能放大信号。mHC 将投影到 Birkhoff polytope（非负、行列和均为 1），同时约束、非负；这样既保留跨流信息交换，又让每层残差映射非扩张。论文另提供融合 kernel、activation 重计算和 DualPipe 重叠以控制系统开销。 实验组 mHC validation PPL 468.903→472.031，变化 -0.67%（未验证效果提升），但残差谱范数 1.0892→1.0000、行列和最大误差 0.11→0。Fidelity: 核心机制复现。在小型 causal Transformer 中实际训练动态两流 HC/mHC，对残差映射做 20 次 Sinkhorn-Knopp，并测量行列约束与谱范数。未复刻 3B/9B/27B MoE、超深训练、TileLang 融合 kernel、分段重计算和 DualPipe；小模型只验证 mHC 数学路径与短程训练，不声称复现论文规模收益。  llm-architecture hyper-connections training-stability 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-mhc-cde7f1ea">mHC: Manifold-Constrained Hyper-Connections</h2>
<p class="ar-learning-card__meta">DeepSeek-AI · 论文公开：2025-12-31</p>
<p><strong>方法要点：</strong>Hyper-Connections 把单一 residual stream 扩为多个流并动态混合，但任意残差矩阵会破坏 identity mapping，深层组合可能放大信号。mHC 将投影到 Birkhoff polytope（非负、行列和均为 1），同时约束、非负；这样既保留跨流信息交换，又让每层残差映射非扩张。论文另提供融合 kernel、activation 重计算和 DualPipe 重叠以控制系统开销。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>实验组 mHC validation PPL 468.903→472.031，变化 -0.67%（未验证效果提升），但残差谱范数 1.0892→1.0000、行列和最大误差 0.11→0。Fidelity: 核心机制复现。在小型 causal Transformer 中实际训练动态两流 HC/mHC，对残差映射做 20 次 Sinkhorn-Knopp，并测量行列约束与谱范数。未复刻 3B/9B/27B MoE、超深训练、TileLang 融合 kernel、分段重计算和 DualPipe；小模型只验证 mHC 数学路径与短程训练，不声称复现论文规模收益。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.24880">原论文</a> · <a href="../../../../reproductions/2512.24880-mhc/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Byte Latent Transformer: Patches Scale Better Than Tokens 基础模型 Meta FAIR 2024-12-13 直接处理 byte，并依据 next-byte entropy 动态形成 patch；全局 Transformer 在 patch 级计算，局部编码器/解码器恢复 byte。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际执行可学习 surprisal boundary、相邻低熵位置 latent patch 共享并展开回原目标；当前 evaluator 的 512-symbol tokenizer 只近似 byte alphabet，未复刻 8B BLT 与完整 local encoder/decoder。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 blt；相对 PPL -2.13%。  tokenizer-free byte-model dynamic-patching architecture 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-blt-d95f5fc6">Byte Latent Transformer: Patches Scale Better Than Tokens</h2>
<p class="ar-learning-card__meta">Meta FAIR · 论文公开：2024-12-13</p>
<p><strong>方法要点：</strong>直接处理 byte，并依据 next-byte entropy 动态形成 patch；全局 Transformer 在 patch 级计算，局部编码器/解码器恢复 byte。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际执行可学习 surprisal boundary、相邻低熵位置 latent patch 共享并展开回原目标；当前 evaluator 的 512-symbol tokenizer 只近似 byte alphabet，未复刻 8B BLT 与完整 local encoder/decoder。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 blt；相对 PPL -2.13%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.09871">原论文</a> · <a href="../../../../reproductions/2412.09871-blt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/conditional-compute" data-search="Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity 基础模型 Google Brain 2021-01-11 Switch 把 dense FFN 替换为每个 token 只激活一个专家的稀疏 MoE，在近似固定 FLOPs 下扩大参数容量。 Fidelity: 核心机制复现。实现 token-level top-1 expert routing 与负载均衡辅助损失。未复刻万亿参数训练、expert capacity overflow 和跨设备 all-to-all。本地对照口径：基线是参数预算内 dense Transformer；实验组是四专家 top-1 Switch FFN；WikiText-2 30-step perplexity 相对 -3.29%（越低越好）。  llm-architecture mixture-of-experts classic 基础模型 按需计算：专家、弹性深宽与查表记忆">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 按需计算：专家、弹性深宽与查表记忆</a></p>
<h2 id="paper-foundation-models-switch-transformer-9afbb109">Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity</h2>
<p class="ar-learning-card__meta">Google Brain · 论文公开：2021-01-11</p>
<p><strong>方法要点：</strong>Switch 把 dense FFN 替换为每个 token 只激活一个专家的稀疏 MoE，在近似固定 FLOPs 下扩大参数容量。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现 token-level top-1 expert routing 与负载均衡辅助损失。未复刻万亿参数训练、expert capacity overflow 和跨设备 all-to-all。本地对照口径：基线是参数预算内 dense Transformer；实验组是四专家 top-1 Switch FFN；WikiText-2 30-step perplexity 相对 -3.29%（越低越好）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2101.03961">原论文</a> · <a href="../../../../reproductions/2101.03961-switch-transformer/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
