---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 生成路径：草稿验证、并行去噪与少步迭代

[基础模型](index.md) / 子主题导学 · 约 3 分钟 · 15 张论文卡

## 先想一个问题

如何减少逐 token 串行生成的等待，同时说清输出分布是否改变？

## 记住这一点

推测解码先由便宜草稿提出多个 token，再让目标模型批量验证；正确的接受概率与拒绝残差采样可保持目标分布。扩散语言模型则把生成改成多位置去噪，例如 dQwen3.5 需把含递归层的因果骨干改为双向传播。少步生成与共享网络迭代又重新安排精炼轨迹；它们改变的不是同一个层面。

## 一个例子

草稿一次提四个 token，如果目标只接受前两个，后面需要校正和继续生成；加速取决于接受率和验证成本。扩散模型可以一轮更新多个位置，但可能要多轮反复去噪。应比较整段输出质量和总时延，不能只比较一次前向写出多少位置。

## 什么时候要小心

精确推测采样的分布保证依赖完整接受与校正算法，不自动适用于任何多头草稿。扩散或蒸馏后的新模型也不因此与原自回归目标等价。本地 Markov 草稿、参考 kernel 或调用次数不能冒充大型模型的真实加速。

## 先读这几篇

先读 Fast Inference 的提出、验证与校正采样，明确保证条件；再读 dQwen3.5 的双向混合骨干与并行解码，区分“重排执行”与“训练新生成机制”。随后看自草稿、缓存和少步精炼。

1. [Fast Inference from Transformers via Speculative Decoding](../../../reproductions/2211.17192-speculative-decoding/README.md) · [原论文](https://arxiv.org/abs/2211.17192)
2. [dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models](../../../foundation-models/2609.20751-dqwen35/README.md) · [原论文](https://arxiv.org/abs/2609.20751)

## 自测一下

“推测解码不改变分布”能否直接用来描述把 AR 骨干改成扩散模型？

??? note "展开参考答案"

    不能。前者在既定目标分布下用接受/拒绝校正重排执行；后者改变模型传播方式、训练目标与解码过程。它需要独立质量评估，不能继承前者的等价采样保证。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 15 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Designing Transformers for Continuous Diffusion Language Models 基础模型 Dots Studio, Xiaohongshu 2026-10-15 连续扩散语言模型要从带高斯噪声的 token 嵌入恢复离散分布。原文§3把架构改动分为三个位置：backbone 的 RMS/QK 归一与噪声条件容量；词表 likelihood shortcut 的显式码本梯度路由和有界校准；训练期 bootstrap self-conditioning 的置信度衰减。LangFlow 的表示、交叉熵和采样器保持不变；Plaid 适配只迁移兼容子集，不能把两套梯度规则混为一谈。 成本过高，不复现（审查 DONE）。修复后已重新在 A100 覆盖四种极值及梯度检查，诊断记录与GPU回执绑定最终执行源码。无公开大数据/模型下载。revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1，seeds42/43/44。实际微型 denoiser 为2层、16维、2 heads、19词，保留球面码本、RMS/QK归一、RoPE、噪声条件残差门、未绑定词表head、零初始化输入融合和校准。  扩散语言模型 噪声条件与自条件 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-langdit-ba73a77f">Designing Transformers for Continuous Diffusion Language Models</h2>
<p class="ar-learning-card__meta">Dots Studio, Xiaohongshu · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>连续扩散语言模型要从带高斯噪声的 token 嵌入恢复离散分布。原文§3把架构改动分为三个位置：backbone 的 RMS/QK 归一与噪声条件容量；词表 likelihood shortcut 的显式码本梯度路由和有界校准；训练期 bootstrap self-conditioning 的置信度衰减。LangFlow 的表示、交叉熵和采样器保持不变；Plaid 适配只迁移兼容子集，不能把两套梯度规则混为一谈。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。修复后已重新在 A100 覆盖四种极值及梯度检查，诊断记录与GPU回执绑定最终执行源码。无公开大数据/模型下载。revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1，seeds42/43/44。实际微型 denoiser 为2层、16维、2 heads、19词，保留球面码本、RMS/QK归一、RoPE、噪声条件残差门、未绑定词表head、零初始化输入融合和校准。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22330">原论文</a> · <a href="../../../../foundation-models/2610.22330-langdit/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On the Design Space of Continuous Diffusion Language Models 基础模型 University of Oxford / Apple（在 Apple 期间完成） 2026-10-09 One-hot continuous flow 在接近终点时训练几乎只看见低熵顶点，但推理跟随有熵 denoiser 概率，产生轨迹错配。DoubleCat 在高斯路径内部再插入 simplex prior 到 one-hot 的插值，把训练质量移到更像推理的 simplex 内部。另一个问题是高维高斯噪声范数约，而 one-hot 信号范数仅为 1，已有 token 难以辨识。 cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。三模型参数 L2 变化分别约 0.1345；  扩散语言模型 Self-conditioning 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-doublecat-semicat-01018306">On the Design Space of Continuous Diffusion Language Models</h2>
<p class="ar-learning-card__meta">University of Oxford / Apple（在 Apple 期间完成） · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>One-hot continuous flow 在接近终点时训练几乎只看见低熵顶点，但推理跟随有熵 denoiser 概率，产生轨迹错配。DoubleCat 在高斯路径内部再插入 simplex prior 到 one-hot 的插值，把训练质量移到更像推理的 simplex 内部。另一个问题是高维高斯噪声范数约，而 one-hot 信号范数仅为 1，已有 token 难以辨识。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。三模型参数 L2 变化分别约 0.1345；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13834">原论文</a> · <a href="../../../../reproductions/2610.13834-doublecat-semicat/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Few-Step Generation via Data-Space Iteration 基础模型 ByteDance Seed 2026-10-08 常规 few-step flow generator 需要预设时间离散化，每步在加噪/去噪轨迹上前进。Data-Space Iteration 改为固定同一份噪声，用共享网络反复改进数据预测；每步 index 只表示 refinement，不是 flow time。训练沿用 distribution matching distillation：真实冻结 teacher 与逐步拟合生成分布的 fake 给出方向，前缀 rollout 无梯度，仅当前 refinement 更新 generator。 本地定位：L1 实际训练核心机制诊断。本地定位：L1 实际训练核心机制诊断。已在真实 A100 从公开图像训练 flow teacher，再执行冻结 teacher、可训练 fake model 与共享 generator 的交替 DMD；不是随机教师、固定合成 reward 或只画迭代示意图。三个种子有正有负，不能宣称稳定质量提升。安装实际运行依赖（包含距离计算所需的 SciPy）：python -m pip install -e &#x27;.[data-space-gpu]&#x27;。  生成模型 少步生成与蒸馏 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-data-space-iteration-cef25f24">Few-Step Generation via Data-Space Iteration</h2>
<p class="ar-learning-card__meta">ByteDance Seed · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>常规 few-step flow generator 需要预设时间离散化，每步在加噪/去噪轨迹上前进。Data-Space Iteration 改为固定同一份噪声，用共享网络反复改进数据预测；每步 index 只表示 refinement，不是 flow time。训练沿用 distribution matching distillation：真实冻结 teacher 与逐步拟合生成分布的 fake 给出方向，前缀 rollout 无梯度，仅当前 refinement 更新 generator。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>本地定位：L1 实际训练核心机制诊断。本地定位：L1 实际训练核心机制诊断。已在真实 A100 从公开图像训练 flow teacher，再执行冻结 teacher、可训练 fake model 与共享 generator 的交替 DMD；不是随机教师、固定合成 reward 或只画迭代示意图。三个种子有正有负，不能宣称稳定质量提升。安装实际运行依赖（包含距离计算所需的 SciPy）：python -m pip install -e &#x27;.[data-space-gpu]&#x27;。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12102">原论文</a> · <a href="../../../../foundation-models/2610.12102-data-space-iteration/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On Trajectory-Aware Training for Masked Diffusion Language Models 基础模型 Apple 2026-09-29 训练时沿模型自己的 progressive-unmasking 轨迹连续展开多个 denoising step，把隐藏 carry 传给下一步，并在固定窗口内通过时间反向传播，使前一步学会产生对后续有用的 carry。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Trajectory-aware training BPTT 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-pumba-d6ea4c98">On Trajectory-Aware Training for Masked Diffusion Language Models</h2>
<p class="ar-learning-card__meta">Apple · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>训练时沿模型自己的 progressive-unmasking 轨迹连续展开多个 denoising step，把隐藏 carry 传给下一步，并在固定窗口内通过时间反向传播，使前一步学会产生对后续有用的 carry。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37974">原论文</a> · <a href="../../../../foundation-models/2609.37974-pumba/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation 基础模型 The University of Texas at Austin 2026-09-29 将昂贵 anchor network 的潜表示跨多个反向扩散步缓存，只周期性刷新；小型 fusion module 根据当前状态门控修正陈旧 anchor，再交给轻量 denoiser。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Latent cache 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-tadm-0fb9bc3b">Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation</h2>
<p class="ar-learning-card__meta">The University of Texas at Austin · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>将昂贵 anchor network 的潜表示跨多个反向扩散步缓存，只周期性刷新；小型 fusion module 根据当前状态门控修正陈旧 anchor，再交给轻量 denoiser。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37924">原论文</a> · <a href="../../../../foundation-models/2609.37924-tadm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models 基础模型 University of Texas at Austin 2026-09-17 把 Qwen3.5 的注意力/RNN 混合骨干改成双向状态传播，再以掩码去噪目标训练为 diffusion language model。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。  扩散语言模型 网络架构 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-dqwen35-77ccc4a5">dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models</h2>
<p class="ar-learning-card__meta">University of Texas at Austin · 论文公开：2026-09-17</p>
<p><strong>方法要点：</strong>把 Qwen3.5 的注意力/RNN 混合骨干改成双向状态传播，再以掩码去噪目标训练为 diffusion language model。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20751">原论文</a> · <a href="../../../../foundation-models/2609.20751-dqwen35/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ASPIRE: Asynchronous Batch Self-Speculative Decoding 基础模型 University of Southern California 2026-09-16 每个请求依据在线接受率与当前 batch 成本独立选择 draft 长度，并周期性用全注意力 refresh layer 校正自推测状态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-aspire-a1351704">ASPIRE: Asynchronous Batch Self-Speculative Decoding</h2>
<p class="ar-learning-card__meta">University of Southern California · 论文公开：2026-09-16</p>
<p><strong>方法要点：</strong>每个请求依据在线接受率与当前 batch 成本独立选择 draft 长度，并周期性用全注意力 refresh layer 校正自推测状态。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17943">原论文</a> · <a href="../../../../foundation-models/2609.17943-aspire/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding 基础模型 Wuhan University 2026-09-15 用早层高频探索与末层低频权威校验组成双循环；两侧 bonus logits 协同补树，并保留精确拒绝采样校正。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-echo-675d4c78">ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding</h2>
<p class="ar-learning-card__meta">Wuhan University · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>用早层高频探索与末层低频权威校验组成双循环；两侧 bonus logits 协同补树，并保留精确拒绝采样校正。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17241">原论文</a> · <a href="../../../../foundation-models/2609.17241-echo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers 基础模型 Seoul National University / KAIST 2026-09-15 利用循环深度的中间预测做自推测，并以流水线残差提案隐藏验证等待。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  推测解码 循环 Transformer 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-loopspec-856a7101">LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers</h2>
<p class="ar-learning-card__meta">Seoul National University / KAIST · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>利用循环深度的中间预测做自推测，并以流水线残差提案隐藏验证等待。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17184">原论文</a> · <a href="../../../../foundation-models/2609.17184-loopspec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Register Tokens for Bounded-State Reasoning in Diffusion Language Models 基础模型 University of Wisconsin–Madison 2026-09-14 清除上一段文本后仅携带固定数量的连续 register hidden states，让扩散语言模型跨 chunk 推理。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  扩散语言模型 长程推理 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-register-tokens-dllm-e9299172">Register Tokens for Bounded-State Reasoning in Diffusion Language Models</h2>
<p class="ar-learning-card__meta">University of Wisconsin–Madison · 论文公开：2026-09-14</p>
<p><strong>方法要点：</strong>清除上一段文本后仅携带固定数量的连续 register hidden states，让扩散语言模型跨 chunk 推理。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16372">原论文</a> · <a href="../../../../foundation-models/2609.16372-register-tokens-dllm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding 基础模型 Huawei Technologies Canada 2026-08-05 主题：推测解码。并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。DBLast 用跨位置共享的低秩 latent mixture 建模依赖，并以期望验证长度为训练目标。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。用 32-token Markov target 比较 unigram 独立 proposal 与 rank-4 条件 proposal，并按精确 speculative acceptance 估计接受长度。  speculative-decoding inference-efficiency stochastic-decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-dblast-5689bd49">DBLast: Dependent Block Drafting for Stochastic Speculative Decoding</h2>
<p class="ar-learning-card__meta">Huawei Technologies Canada · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>主题：推测解码。并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。DBLast 用跨位置共享的低秩 latent mixture 建模依赖，并以期望验证长度为训练目标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。用 32-token Markov target 比较 unigram 独立 proposal 与 rank-4 条件 proposal，并按精确 speculative acceptance 估计接受长度。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05448">原论文</a> · <a href="../../../../reproductions/2608.05448-dblast/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context 基础模型 NVIDIA 2026-07-23 内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近个 token，同时 target 继续读取完整上下文并验证所有候选。因此窗口只影响接受率和速度，不改变 target 决定的输出分布。 Fidelity: 核心机制复现。真实训练 MTP draft、切换 KV key 集并执行 target verification；缩小模型、context 和 serving runtime。本地实现训练了共享 target token embedding 的轻量 MTP head，并实际执行 sink+window attention 和逐 token target verification；没有复刻 SGLang paged-KV/Triton ring buffer、连续 batching、B200/H100 或百万 token 测试。  llm-serving speculative-decoding kv-cache long-context 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-windowed-mtp-ad617a2b">Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context</h2>
<p class="ar-learning-card__meta">NVIDIA · 论文公开：2026-07-23</p>
<p><strong>方法要点：</strong>内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近个 token，同时 target 继续读取完整上下文并验证所有候选。因此窗口只影响接受率和速度，不改变 target 决定的输出分布。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。真实训练 MTP draft、切换 KV key 集并执行 target verification；缩小模型、context 和 serving runtime。本地实现训练了共享 target token embedding 的轻量 MTP head，并实际执行 sink+window attention 和逐 token target verification；没有复刻 SGLang paged-KV/Triton ring buffer、连续 batching、B200/H100 或百万 token 测试。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21535">原论文</a> · <a href="../../../../reproductions/2607.21535-windowed-mtp/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion 基础模型 University of Illinois Urbana-Champaign / Google Research 2026-03-06 先以集合级复合奖励产生对齐目标，再把目标编译到单次扩散式 fan-out 检索器。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  生成式检索 RL 编译 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-r4t-4721c6f0">Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign / Google Research · 论文公开：2026-03-06</p>
<p><strong>方法要点：</strong>先以集合级复合奖励产生对齐目标，再把目标编译到单次扩散式 fan-out 检索器。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.06397">原论文</a> · <a href="../../../../foundation-models/2603.06397-r4t/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads 基础模型 Together AI / Princeton University / University of Illinois Urbana-Champaign 2024-01-19 在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 token 转移模型上执行多 future head、候选树和 backbone 验证；未复刻 GPU tree-attention kernel。本地相对变化不得与原文指标混写。本地对照口径：基线为 single-head greedy，实验组为 three future heads + tree verification，只改变论文核心机制；backbone_calls 160.0000 → 80.0000，相对基线 -50.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-medusa-8eb57905">Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads</h2>
<p class="ar-learning-card__meta">Together AI / Princeton University / University of Illinois Urbana-Champaign · 论文公开：2024-01-19</p>
<p><strong>方法要点：</strong>在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 token 转移模型上执行多 future head、候选树和 backbone 验证；未复刻 GPU tree-attention kernel。本地相对变化不得与原文指标混写。本地对照口径：基线为 single-head greedy，实验组为 three future heads + tree verification，只改变论文核心机制；backbone_calls 160.0000 → 80.0000，相对基线 -50.00%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10774">原论文</a> · <a href="../../../../reproductions/2401.10774-medusa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Fast Inference from Transformers via Speculative Decoding 基础模型 Google Research 2022-11-30 小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 拟合 target/draft token 模型，真实执行提议、验证和拒绝回退；target 是小型 Markov LM，不等同于 T5-XXL kernel 延迟。本地相对变化不得与原文指标混写。本地对照口径：基线为 target-only greedy decoding，实验组为 four-token draft and exact target verification，只改变论文核心机制；target_calls 160.0000 → 40.0000，相对基线 -75.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<h2 id="paper-foundation-models-speculative-decoding-bd568875">Fast Inference from Transformers via Speculative Decoding</h2>
<p class="ar-learning-card__meta">Google Research · 论文公开：2022-11-30</p>
<p><strong>方法要点：</strong>小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 拟合 target/draft token 模型，真实执行提议、验证和拒绝回退；target 是小型 Markov LM，不等同于 T5-XXL kernel 延迟。本地相对变化不得与原文指标混写。本地对照口径：基线为 target-only greedy decoding，实验组为 four-token draft and exact target verification，只改变论文核心机制；target_calls 160.0000 → 40.0000，相对基线 -75.00%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.17192">原论文</a> · <a href="../../../../reproductions/2211.17192-speculative-decoding/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
