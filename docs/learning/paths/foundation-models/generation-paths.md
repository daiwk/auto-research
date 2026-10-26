---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 生成路径：草稿验证、并行去噪与少步迭代

[基础模型](index.md) / 15 个问题 · 15 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">15 个问题 · 15 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:langdit" data-paper-title="Designing Transformers for Continuous Diffusion Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Designing Transformers for Continuous Diffusion Language Models 基础模型 Dots Studio, Xiaohongshu 2026-10-15 连续扩散语言模型要从带高斯噪声的 token 嵌入恢复离散分布。原文§3把架构改动分为三个位置：backbone 的 RMS/QK 归一与噪声条件容量；词表 likelihood shortcut 的显式码本梯度路由和有界校准；训练期 bootstrap self-conditioning 的置信度衰减。LangFlow 的表示、交叉熵和采样器保持不变；Plaid 适配只迁移兼容子集，不能把两套梯度规则混为一谈。 成本过高，不复现（审查 DONE）。修复后已重新在 A100 覆盖四种极值及梯度检查，诊断记录与GPU回执绑定最终执行源码。无公开大数据/模型下载。revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1，seeds42/43/44。实际微型 denoiser 为2层、16维、2 heads、19词，保留球面码本、RMS/QK归一、RoPE、噪声条件残差门、未绑定词表head、零初始化输入融合和校准。  扩散语言模型 噪声条件与自条件 基础模型 生成路径：草稿验证、并行去噪与少步迭代 LangDiT为什么只detach似然shortcut中的显式码本，而不把带噪输入整体detach？ 显式shortcut与输入构造共享码本，切断前者可控制该路径的梯度，码本仍应通过带噪输入路径学习；整体detach会错误阻断这条训练关系。训练期自条件用熵衰减不可靠反馈，推理却使用未加权后验均值，不能把训练门控直接搬到采样器。 例如同一张词向量表既生成带噪输入又参与快捷打分，只冻结快捷乘法的一侧；把输入也冻结，会让本来应学习的码本通路消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-langdit-ba73a77f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-999cd9aaee6ecf4c">LangDiT为什么只detach似然shortcut中的显式码本，而不把带噪输入整体detach？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alangdit">Designing Transformers for Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dots Studio, Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>显式shortcut与输入构造共享码本，切断前者可控制该路径的梯度，码本仍应通过带噪输入路径学习；整体detach会错误阻断这条训练关系。训练期自条件用熵衰减不可靠反馈，推理却使用未加权后验均值，不能把训练门控直接搬到采样器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一张词向量表既生成带噪输入又参与快捷打分，只冻结快捷乘法的一侧；把输入也冻结，会让本来应学习的码本通路消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22330">原论文</a> · <a href="../../../../foundation-models/2610.22330-langdit/">实现解读</a> · <a href="#qa-999cd9aaee6ecf4c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doublecat-semicat" data-paper-title="On the Design Space of Continuous Diffusion Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On the Design Space of Continuous Diffusion Language Models 基础模型 University of Oxford / Apple（在 Apple 期间完成） 2026-10-09 One-hot continuous flow 在接近终点时训练几乎只看见低熵顶点，但推理跟随有熵 denoiser 概率，产生轨迹错配。DoubleCat 在高斯路径内部再插入 simplex prior 到 one-hot 的插值，把训练质量移到更像推理的 simplex 内部。另一个问题是高维高斯噪声范数约，而 one-hot 信号范数仅为 1，已有 token 难以辨识。 cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。三模型参数 L2 变化分别约 0.1345；  扩散语言模型 Self-conditioning 基础模型 生成路径：草稿验证、并行去噪与少步迭代 DoubleCat的双层插值与SemiCat的永久reveal，为什么是两个不同的修正？ 双层插值把训练分布移向更接近推理的单纯形内部，缓解低熵端点错配；永久揭示则让已确定词元成为干净信号，不再被高维噪声淹没。后者只监督未揭示位置并保持已揭示结果，条件揭示概率需随剩余时间调整，两者也不默认增加自条件前向。 例如一句话里已确定的主语可永久保留，其他位置继续去噪；训练输入中模拟有熵概率结构，则是在解决另一种轨迹分布差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-doublecat-semicat-01018306" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d81c0b5a5fbc8665">DoubleCat的双层插值与SemiCat的永久reveal，为什么是两个不同的修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoublecat-semicat">On the Design Space of Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Oxford / Apple（在 Apple 期间完成）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>双层插值把训练分布移向更接近推理的单纯形内部，缓解低熵端点错配；永久揭示则让已确定词元成为干净信号，不再被高维噪声淹没。后者只监督未揭示位置并保持已揭示结果，条件揭示概率需随剩余时间调整，两者也不默认增加自条件前向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一句话里已确定的主语可永久保留，其他位置继续去噪；训练输入中模拟有熵概率结构，则是在解决另一种轨迹分布差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13834">原论文</a> · <a href="../../../../reproductions/2610.13834-doublecat-semicat/">实现解读</a> · <a href="#qa-d81c0b5a5fbc8665">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-space-iteration" data-paper-title="Few-Step Generation via Data-Space Iteration" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Few-Step Generation via Data-Space Iteration 基础模型 ByteDance Seed 2026-10-08 常规 few-step flow generator 需要预设时间离散化，每步在加噪/去噪轨迹上前进。Data-Space Iteration 改为固定同一份噪声，用共享网络反复改进数据预测；每步 index 只表示 refinement，不是 flow time。训练沿用 distribution matching distillation：真实冻结 teacher 与逐步拟合生成分布的 fake 给出方向，前缀 rollout 无梯度，仅当前 refinement 更新 generator。 本地定位：L1 实际训练核心机制诊断。本地定位：L1 实际训练核心机制诊断。已在真实 A100 从公开图像训练 flow teacher，再执行冻结 teacher、可训练 fake model 与共享 generator 的交替 DMD；不是随机教师、固定合成 reward 或只画迭代示意图。三个种子有正有负，不能宣称稳定质量提升。安装实际运行依赖（包含距离计算所需的 SciPy）：python -m pip install -e &#x27;.[data-space-gpu]&#x27;。  生成模型 少步生成与蒸馏 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Data-Space Iteration为什么固定同一噪声反复改进预测，而不把迭代编号当flow时间？ 共享生成器在数据空间逐步修正同一预测，编号表示细化轮次，原始噪声保持不变。训练仍用真实教师与拟合生成分布的假模型给出DMD方向，前缀无梯度，仅当前细化更新；不是每轮直接回归真实图片。本地微型实验不能替代原文大规模图像指标。 例如从同一个噪声起点先画轮廓再修细节，后一步利用前一步预测；若每轮换噪声或随意当作新的扩散时间，就改变了迭代机制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-data-space-iteration-cef25f24" class="ar-learning-paper-anchor"></span>
<h2 id="qa-039b91ebbdf6cbe4">Data-Space Iteration为什么固定同一噪声反复改进预测，而不把迭代编号当flow时间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-space-iteration">Few-Step Generation via Data-Space Iteration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享生成器在数据空间逐步修正同一预测，编号表示细化轮次，原始噪声保持不变。训练仍用真实教师与拟合生成分布的假模型给出DMD方向，前缀无梯度，仅当前细化更新；不是每轮直接回归真实图片。本地微型实验不能替代原文大规模图像指标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从同一个噪声起点先画轮廓再修细节，后一步利用前一步预测；若每轮换噪声或随意当作新的扩散时间，就改变了迭代机制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12102">原论文</a> · <a href="../../../../foundation-models/2610.12102-data-space-iteration/">实现解读</a> · <a href="#qa-039b91ebbdf6cbe4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pumba" data-paper-title="On Trajectory-Aware Training for Masked Diffusion Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On Trajectory-Aware Training for Masked Diffusion Language Models 基础模型 Apple 2026-09-29 训练时沿模型自己的 progressive-unmasking 轨迹连续展开多个 denoising step，把隐藏 carry 传给下一步，并在固定窗口内通过时间反向传播，使前一步学会产生对后续有用的 carry。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Trajectory-aware training BPTT 基础模型 生成路径：草稿验证、并行去噪与少步迭代 PUMBA为什么要让梯度穿过多个去噪步骤的carry，而不把每步当独立训练样本？ 隐藏carry会影响后续去噪，独立训练只要求当前步预测好，未必鼓励它留下对下一步有用的状态。沿模型自身逐步揭示轨迹展开，在固定窗口内反传，可让早期carry承担后续损失；窗口间仍截断，以限制成本。本地未训练完整扩散语言模型。 例如前一步留下某种实体约束，后一步据此填空，后一步误差应能指导前一步如何编码约束；每步都detach会丢掉这种关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-pumba-d6ea4c98" class="ar-learning-paper-anchor"></span>
<h2 id="qa-295de760f5896ce6">PUMBA为什么要让梯度穿过多个去噪步骤的carry，而不把每步当独立训练样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apumba">On Trajectory-Aware Training for Masked Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>隐藏carry会影响后续去噪，独立训练只要求当前步预测好，未必鼓励它留下对下一步有用的状态。沿模型自身逐步揭示轨迹展开，在固定窗口内反传，可让早期carry承担后续损失；窗口间仍截断，以限制成本。本地未训练完整扩散语言模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前一步留下某种实体约束，后一步据此填空，后一步误差应能指导前一步如何编码约束；每步都detach会丢掉这种关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37974">原论文</a> · <a href="../../../../foundation-models/2609.37974-pumba/">实现解读</a> · <a href="#qa-295de760f5896ce6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tadm" data-paper-title="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation 基础模型 The University of Texas at Austin 2026-09-29 将昂贵 anchor network 的潜表示跨多个反向扩散步缓存，只周期性刷新；小型 fusion module 根据当前状态门控修正陈旧 anchor，再交给轻量 denoiser。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Latent cache 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 TADM周期缓存anchor后，为什么还需要依当前扩散状态进行门控修正？ 跨多个反向步复用昂贵潜表示可减少主网络调用，但当前状态不断变化，旧anchor会陈旧。轻量融合模块用当前条件预测修正并门控，再交给较小去噪器，平衡复用与适配。门控不能保证陈旧信息完全恢复，本地修正核未运行完整大模型生成评测。 例如早期缓存只表达粗略句子结构，后续已确定更多词元，融合模块据新状态修正旧表示；一直原样复用可能忽略这些新约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-tadm-0fb9bc3b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0b7ec87ec23ca88a">TADM周期缓存anchor后，为什么还需要依当前扩散状态进行门控修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atadm">Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>跨多个反向步复用昂贵潜表示可减少主网络调用，但当前状态不断变化，旧anchor会陈旧。轻量融合模块用当前条件预测修正并门控，再交给较小去噪器，平衡复用与适配。门控不能保证陈旧信息完全恢复，本地修正核未运行完整大模型生成评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如早期缓存只表达粗略句子结构，后续已确定更多词元，融合模块据新状态修正旧表示；一直原样复用可能忽略这些新约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37924">原论文</a> · <a href="../../../../foundation-models/2609.37924-tadm/">实现解读</a> · <a href="#qa-0b7ec87ec23ca88a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dqwen35" data-paper-title="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models 基础模型 University of Texas at Austin 2026-09-17 把 Qwen3.5 的注意力/RNN 混合骨干改成双向状态传播，再以掩码去噪目标训练为 diffusion language model。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。  扩散语言模型 网络架构 基础模型 生成路径：草稿验证、并行去噪与少步迭代 dQwen3.5把混合骨干改成双向传播，为什么不只是把注意力的因果mask去掉？ 混合骨干还包含递归状态，若只有注意力能看双向，递归分支仍可能保留单向信息约束。双向状态传播配合掩码去噪，才适应同时恢复多个位置的扩散任务。传播核可执行不表示检查点已经完成适配，本地未加载完整模型或复现预训练损失曲线。 例如句首空位需要句末线索，注意力分支看到了后文，而单向递归分支仍读不到；只改一个mask无法让两条路径都拥有相同信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-dqwen35-77ccc4a5" class="ar-learning-paper-anchor"></span>
<h2 id="qa-628204eccd8870fd">dQwen3.5把混合骨干改成双向传播，为什么不只是把注意力的因果mask去掉？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adqwen35">dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>混合骨干还包含递归状态，若只有注意力能看双向，递归分支仍可能保留单向信息约束。双向状态传播配合掩码去噪，才适应同时恢复多个位置的扩散任务。传播核可执行不表示检查点已经完成适配，本地未加载完整模型或复现预训练损失曲线。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如句首空位需要句末线索，注意力分支看到了后文，而单向递归分支仍读不到；只改一个mask无法让两条路径都拥有相同信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20751">原论文</a> · <a href="../../../../foundation-models/2609.20751-dqwen35/">实现解读</a> · <a href="#qa-628204eccd8870fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:aspire" data-paper-title="ASPIRE: Asynchronous Batch Self-Speculative Decoding" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ASPIRE: Asynchronous Batch Self-Speculative Decoding 基础模型 University of Southern California 2026-09-16 每个请求依据在线接受率与当前 batch 成本独立选择 draft 长度，并周期性用全注意力 refresh layer 校正自推测状态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 ASPIRE为什么让同一batch内的请求独立选择草稿长度，而不是统一一个长度？ 不同请求的接受率和剩余状态不同，统一长度会让低接受率请求浪费验证或让高接受率请求错失收益。调度还需结合当前批成本，而非只追求最长草稿；周期全注意力刷新用于纠正自投机状态。本地只验证调度和刷新门控，没有改造完整推理引擎。 例如一个请求连续接受较深草稿，另一个常在首词拒绝，可给它们不同长度；但批处理开销也会改变选择，不能只按单请求接受率算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-aspire-a1351704" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3be38b55eeb6ffa7">ASPIRE为什么让同一batch内的请求独立选择草稿长度，而不是统一一个长度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaspire">ASPIRE: Asynchronous Batch Self-Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同请求的接受率和剩余状态不同，统一长度会让低接受率请求浪费验证或让高接受率请求错失收益。调度还需结合当前批成本，而非只追求最长草稿；周期全注意力刷新用于纠正自投机状态。本地只验证调度和刷新门控，没有改造完整推理引擎。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个请求连续接受较深草稿，另一个常在首词拒绝，可给它们不同长度；但批处理开销也会改变选择，不能只按单请求接受率算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17943">原论文</a> · <a href="../../../../foundation-models/2609.17943-aspire/">实现解读</a> · <a href="#qa-3be38b55eeb6ffa7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:echo" data-paper-title="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding 基础模型 Wuhan University 2026-09-15 用早层高频探索与末层低频权威校验组成双循环；两侧 bonus logits 协同补树，并保留精确拒绝采样校正。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 ECHO用早层探索和末层校验，为什么bonus logits不能直接当最终采样分布？ 早层高频提出候选，末层较低频进行权威验证，两侧额外分数用于协同补充候选树，提高有效提议覆盖。探索分布可以不同于目标分布，最终仍需精确拒绝采样校正。省略校正会改变输出分布，本地候选合并与张量路径也不能证明论文吞吐。 例如早层补出一条末层原树未包含的分支，可以拿来验证；不能因它扩展了候选就直接接受，否则把草稿偏好混成了目标答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-echo-675d4c78" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bdd24109fa6354ee">ECHO用早层探索和末层校验，为什么bonus logits不能直接当最终采样分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aecho">ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早层高频提出候选，末层较低频进行权威验证，两侧额外分数用于协同补充候选树，提高有效提议覆盖。探索分布可以不同于目标分布，最终仍需精确拒绝采样校正。省略校正会改变输出分布，本地候选合并与张量路径也不能证明论文吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如早层补出一条末层原树未包含的分支，可以拿来验证；不能因它扩展了候选就直接接受，否则把草稿偏好混成了目标答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17241">原论文</a> · <a href="../../../../foundation-models/2609.17241-echo/">实现解读</a> · <a href="#qa-bdd24109fa6354ee">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:loopspec" data-paper-title="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers 基础模型 Seoul National University / KAIST 2026-09-15 利用循环深度的中间预测做自推测，并以流水线残差提案隐藏验证等待。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  推测解码 循环 Transformer 基础模型 生成路径：草稿验证、并行去噪与少步迭代 LoopSpec为什么利用循环深度的中间预测，而不必另训练一个完全独立草稿模型？ 循环Transformer不同深度的状态可形成便宜的早期预测，再用更深计算验证；流水线残差提案试图把等待时间与后续工作重叠。中间预测只是提议，不自动拥有深层质量，真实收益取决于接受与调度开销。本地深度调度参考核没有证明GPU端到端吞吐。 例如同一模型浅循环先提议下一段，深循环随后核验；若提议常被拒绝，虽然省了独立草稿模型，也可能无法抵消流水线成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-loopspec-856a7101" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2ca2ea44d8975e44">LoopSpec为什么利用循环深度的中间预测，而不必另训练一个完全独立草稿模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aloopspec">LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University / KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>循环Transformer不同深度的状态可形成便宜的早期预测，再用更深计算验证；流水线残差提案试图把等待时间与后续工作重叠。中间预测只是提议，不自动拥有深层质量，真实收益取决于接受与调度开销。本地深度调度参考核没有证明GPU端到端吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一模型浅循环先提议下一段，深循环随后核验；若提议常被拒绝，虽然省了独立草稿模型，也可能无法抵消流水线成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17184">原论文</a> · <a href="../../../../foundation-models/2609.17184-loopspec/">实现解读</a> · <a href="#qa-2ca2ea44d8975e44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:register-tokens-dllm" data-paper-title="Register Tokens for Bounded-State Reasoning in Diffusion Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Register Tokens for Bounded-State Reasoning in Diffusion Language Models 基础模型 University of Wisconsin–Madison 2026-09-14 清除上一段文本后仅携带固定数量的连续 register hidden states，让扩散语言模型跨 chunk 推理。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  扩散语言模型 长程推理 基础模型 生成路径：草稿验证、并行去噪与少步迭代 扩散模型清除上一段文本后只带固定register，为什么仍可能跨段推理又受信息瓶颈限制？ 连续register隐藏状态保存上一段提炼的信息，以固定大小传给下一段，避免上下文随段数无限增长。保留的是压缩状态而非完整文字历史，重要细节能否被编码并长期维持需要训练与评测。状态大小有界不等于推理记忆无损，本地未加载完整扩散检查点。 例如上一段确定人物关系后把摘要状态传入下一段，原句已删除；若某个姓名未进入register，后文无法凭固定状态保证精确恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-register-tokens-dllm-e9299172" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8ccfd44bd0885c4e">扩散模型清除上一段文本后只带固定register，为什么仍可能跨段推理又受信息瓶颈限制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aregister-tokens-dllm">Register Tokens for Bounded-State Reasoning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续register隐藏状态保存上一段提炼的信息，以固定大小传给下一段，避免上下文随段数无限增长。保留的是压缩状态而非完整文字历史，重要细节能否被编码并长期维持需要训练与评测。状态大小有界不等于推理记忆无损，本地未加载完整扩散检查点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如上一段确定人物关系后把摘要状态传入下一段，原句已删除；若某个姓名未进入register，后文无法凭固定状态保证精确恢复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16372">原论文</a> · <a href="../../../../foundation-models/2609.16372-register-tokens-dllm/">实现解读</a> · <a href="#qa-8ccfd44bd0885c4e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dblast" data-paper-title="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding 基础模型 Huawei Technologies Canada 2026-08-05 主题：推测解码。并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。DBLast 用跨位置共享的低秩 latent mixture 建模依赖，并以期望验证长度为训练目标。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。用 32-token Markov target 比较 unigram 独立 proposal 与 rank-4 条件 proposal，并按精确 speculative acceptance 估计接受长度。  speculative-decoding inference-efficiency stochastic-decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 DBLast共享latent为什么能弥补并行草稿各位置独立采样的缺陷？ 各位置在给定隐变量后可以并行，但共享隐变量使边缘联合分布带有跨位置依赖，避免把互相矛盾的高概率词元简单拼接。训练面向期望验证长度，而不只追求单位置命中率。混合结构仍需目标验证器确认，本地机制可执行不等于原文服务速度已复现。 例如后续短语需要共同选择单数或复数，共享隐变量能协调多个位置；若各自独立挑最高概率词，可能拼出不一致的语法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-dblast-5689bd49" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f6c6be038ac0c88f">DBLast共享latent为什么能弥补并行草稿各位置独立采样的缺陷？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adblast">DBLast: Dependent Block Drafting for Stochastic Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies Canada</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各位置在给定隐变量后可以并行，但共享隐变量使边缘联合分布带有跨位置依赖，避免把互相矛盾的高概率词元简单拼接。训练面向期望验证长度，而不只追求单位置命中率。混合结构仍需目标验证器确认，本地机制可执行不等于原文服务速度已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如后续短语需要共同选择单数或复数，共享隐变量能协调多个位置；若各自独立挑最高概率词，可能拼出不一致的语法。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05448">原论文</a> · <a href="../../../../reproductions/2608.05448-dblast/">实现解读</a> · <a href="#qa-f6c6be038ac0c88f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:windowed-mtp" data-paper-title="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context 基础模型 NVIDIA 2026-07-23 内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近个 token，同时 target 继续读取完整上下文并验证所有候选。因此窗口只影响接受率和速度，不改变 target 决定的输出分布。 Fidelity: 核心机制复现。真实训练 MTP draft、切换 KV key 集并执行 target verification；缩小模型、context 和 serving runtime。本地实现训练了共享 target token embedding 的轻量 MTP head，并实际执行 sink+window attention 和逐 token target verification；没有复刻 SGLang paged-KV/Triton ring buffer、连续 batching、B200/H100 或百万 token 测试。  llm-serving speculative-decoding kv-cache long-context 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Windowed-MTP只缩小draft窗口，为什么能省读取又不直接改变target输出分布？ 草稿只读起始保留项与近期窗口，降低其上下文读取开销；目标验证器仍读完整历史并校正所有提议。窗口改变提议质量、接受率及速度，不应改变精确验证定义的目标分布。若连验证器也截窗则条件改变，本地延迟也不能外推到原文生产硬件。 例如旧历史线索被草稿忽略导致猜错，完整目标仍可拒绝并纠正；为了再省一点内存把目标历史也删掉，就失去原分布保证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-windowed-mtp-ad617a2b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-869f887ecd35e200">Windowed-MTP只缩小draft窗口，为什么能省读取又不直接改变target输出分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awindowed-mtp">Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>草稿只读起始保留项与近期窗口，降低其上下文读取开销；目标验证器仍读完整历史并校正所有提议。窗口改变提议质量、接受率及速度，不应改变精确验证定义的目标分布。若连验证器也截窗则条件改变，本地延迟也不能外推到原文生产硬件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧历史线索被草稿忽略导致猜错，完整目标仍可拒绝并纠正；为了再省一点内存把目标历史也删掉，就失去原分布保证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21535">原论文</a> · <a href="../../../../reproductions/2607.21535-windowed-mtp/">实现解读</a> · <a href="#qa-869f887ecd35e200">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:r4t" data-paper-title="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion 基础模型 University of Illinois Urbana-Champaign / Google Research 2026-03-06 先以集合级复合奖励产生对齐目标，再把目标编译到单次扩散式 fan-out 检索器。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  生成式检索 RL 编译 基础模型 生成路径：草稿验证、并行去噪与少步迭代 R4T为什么先对检索集合整体对齐，再把结果编译进扩散式fan-out检索器？ 多路检索的价值不只由每条结果单独相关决定，还取决于集合覆盖与多样性。集合级复合奖励先定义这些取舍，再通过训练让单次扩散检索接近对齐目标，减少在线优化负担。奖励设计可能偏移真实需求，本地只有集合目标核，没有训练完整扩散检索器。 例如三条都高度相关却重复同一证据，可能不如覆盖不同要点的结果组；不能只把单条相关分数分别提高，就称为集合多样性优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-r4t-4721c6f0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-106925b5c8b75df1">R4T为什么先对检索集合整体对齐，再把结果编译进扩散式fan-out检索器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ar4t">Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多路检索的价值不只由每条结果单独相关决定，还取决于集合覆盖与多样性。集合级复合奖励先定义这些取舍，再通过训练让单次扩散检索接近对齐目标，减少在线优化负担。奖励设计可能偏移真实需求，本地只有集合目标核，没有训练完整扩散检索器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三条都高度相关却重复同一证据，可能不如覆盖不同要点的结果组；不能只把单条相关分数分别提高，就称为集合多样性优化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.06397">原论文</a> · <a href="../../../../foundation-models/2603.06397-r4t/">实现解读</a> · <a href="#qa-106925b5c8b75df1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:medusa" data-paper-title="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads 基础模型 Together AI / Princeton University / University of Illinois Urbana-Champaign 2024-01-19 在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 token 转移模型上执行多 future head、候选树和 backbone 验证；未复刻 GPU tree-attention kernel。本地相对变化不得与原文指标混写。本地对照口径：基线为 single-head greedy，实验组为 three future heads + tree verification，只改变论文核心机制；backbone_calls 160.0000 → 80.0000，相对基线 -50.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Medusa的多个future-token head为什么需要候选树验证，而不能各自取最高概率后直接拼接？ 各头从当前状态预测不同未来位置，预测之间未必构成一致的自回归条件链。候选树组织多种组合，主干再验证可接受分支，才可能减少串行步骤。多头训练损失本身不证明任意拼接正确，也不自动给出采样分布保证；本地小模型未复刻GPU树注意力内核。 例如第二个头预测名词、第三个头预测动词，各自首选未必能连成句子；树验证检查组合，而不是把独立预测当作已知历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-medusa-8eb57905" class="ar-learning-paper-anchor"></span>
<h2 id="qa-91bfb6f20f55ba61">Medusa的多个future-token head为什么需要候选树验证，而不能各自取最高概率后直接拼接？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amedusa">Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / Princeton University / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各头从当前状态预测不同未来位置，预测之间未必构成一致的自回归条件链。候选树组织多种组合，主干再验证可接受分支，才可能减少串行步骤。多头训练损失本身不证明任意拼接正确，也不自动给出采样分布保证；本地小模型未复刻GPU树注意力内核。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第二个头预测名词、第三个头预测动词，各自首选未必能连成句子；树验证检查组合，而不是把独立预测当作已知历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10774">原论文</a> · <a href="../../../../reproductions/2401.10774-medusa/">实现解读</a> · <a href="#qa-91bfb6f20f55ba61">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:speculative-decoding" data-paper-title="Fast Inference from Transformers via Speculative Decoding" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Fast Inference from Transformers via Speculative Decoding 基础模型 Google Research 2022-11-30 小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 拟合 target/draft token 模型，真实执行提议、验证和拒绝回退；target 是小型 Markov LM，不等同于 T5-XXL kernel 延迟。本地相对变化不得与原文指标混写。本地对照口径：基线为 target-only greedy decoding，实验组为 four-token draft and exact target verification，只改变论文核心机制；target_calls 160.0000 → 40.0000，相对基线 -75.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 推测解码拒绝草稿时，为什么要从正残差分布采样，而不能直接重采一次目标分布？ 草稿按目标与提议概率比接受，接受部分已经贡献了部分目标概率质量。拒绝后从目标减去提议的正残差归一化采样，才能补足剩余质量；直接重采目标会重复计入已接受部分，改变最终分布。本地小型词转移模型验证流程，不等于大模型内核延迟。 例如草稿过度偏好某个词，拒绝事件应补偿它欠覆盖的其他词；若拒绝后仍按原目标重采，就没有正确扣除先前接受的质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-speculative-decoding-bd568875" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bd026bc4bd6ddae3">推测解码拒绝草稿时，为什么要从正残差分布采样，而不能直接重采一次目标分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aspeculative-decoding">Fast Inference from Transformers via Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>草稿按目标与提议概率比接受，接受部分已经贡献了部分目标概率质量。拒绝后从目标减去提议的正残差归一化采样，才能补足剩余质量；直接重采目标会重复计入已接受部分，改变最终分布。本地小型词转移模型验证流程，不等于大模型内核延迟。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如草稿过度偏好某个词，拒绝事件应补偿它欠覆盖的其他词；若拒绝后仍按原目标重采，就没有正确扣除先前接受的质量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.17192">原论文</a> · <a href="../../../../reproductions/2211.17192-speculative-decoding/">实现解读</a> · <a href="#qa-bd026bc4bd6ddae3">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
