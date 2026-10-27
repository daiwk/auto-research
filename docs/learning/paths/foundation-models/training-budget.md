---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 训练预算：数据配比、目标与优化器

[基础模型](index.md) / 112 个问题 · 28 篇论文

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
<p class="ar-learning-status" data-learning-status role="status">112 个问题 · 28 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lazyflash" data-paper-title="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning 基础模型 Microsoft 2026-10-22 与稀疏前向attention不同，LazyFlash保留训练和部署前向完全dense。它按query block的dO Frobenius范数衡量梯度贡献，用gradient-mass budget约束预计丢弃量，并importance采样反向block。必须在tiled FlashAttention反向内部跳过内存访问/计算，才能兑现论文速度；用PyTorch dense backward后置零或toy mask不构成该方法的低成本完整实现。 成本过高，不复现（审查 DONE）。原文8张H200、65,536长度、2500steps，多个Qwen3模型和语音50K小时训练数据；所有计时在H200。自定义FlashAttention反向kernel及跨长度/模型/精度验证本身也超过本轮单卡低成本范围。不安装/编译kernel或加载权重来“试试”。无本地operator、metrics或GPUreceipt；无capability/evolve声明。原方法的定义性产物是可执行的tiled backward kernel，本轮不以通用softmax/mask代理充数。已读方法、实验及附录后终结完整复现成本审查。  推理与系统效率 长上下文训练 基础模型 训练预算：数据配比、目标与优化器 LazyFlash 为什么在训练时保留 dense 前向，却压缩反向工作？ 前向决定模型读取的完整上下文；反向不同query块的梯度贡献可能很不均匀。方法把节省放在训练梯度计算上，避免把部署时的可见信息范围改成稀疏前向。 示意：模型仍看全文作预测，但本次训练反向只抽取部分贡献块并做相应重权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-lazyflash-43455fcb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1694bf608c608052">LazyFlash 为什么在训练时保留 dense 前向，却压缩反向工作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alazyflash">LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前向决定模型读取的完整上下文；反向不同query块的梯度贡献可能很不均匀。方法把节省放在训练梯度计算上，避免把部署时的可见信息范围改成稀疏前向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型仍看全文作预测，但本次训练反向只抽取部分贡献块并做相应重权。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31911v1">原论文</a> · <a href="../../../../foundation-models/2610.31911-lazyflash/">实现解读</a> · <a href="#qa-1694bf608c608052">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lazyflash" data-paper-title="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning 基础模型 Microsoft 2026-10-22 与稀疏前向attention不同，LazyFlash保留训练和部署前向完全dense。它按query block的dO Frobenius范数衡量梯度贡献，用gradient-mass budget约束预计丢弃量，并importance采样反向block。必须在tiled FlashAttention反向内部跳过内存访问/计算，才能兑现论文速度；用PyTorch dense backward后置零或toy mask不构成该方法的低成本完整实现。 成本过高，不复现（审查 DONE）。原文8张H200、65,536长度、2500steps，多个Qwen3模型和语音50K小时训练数据；所有计时在H200。自定义FlashAttention反向kernel及跨长度/模型/精度验证本身也超过本轮单卡低成本范围。不安装/编译kernel或加载权重来“试试”。无本地operator、metrics或GPUreceipt；无capability/evolve声明。原方法的定义性产物是可执行的tiled backward kernel，本轮不以通用softmax/mask代理充数。已读方法、实验及附录后终结完整复现成本审查。  推理与系统效率 长上下文训练 基础模型 训练预算：数据配比、目标与优化器 LazyFlash前向仍是dense，为什么训练加速来自反向，而不是减少可见上下文？ 它保持前向完整注意力，用输出梯度的块范数分配反向保留概率，再对采样块按概率倒数重加权，估计dense梯度。要真正节省时间，必须在tiled反向内核里跳过相应访存与计算。先完整反传再把梯度置零，不具备同样成本；单次随机梯度也不会逐元素等于dense。 教学例子：某query块的梯度贡献很小，可降低其反向执行概率；前向仍看过全部证据。只有没有实际执行被跳过块的反向工作，才可能获得相应速度收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-73f4f2504e86cd44">LazyFlash前向仍是dense，为什么训练加速来自反向，而不是减少可见上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alazyflash">LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它保持前向完整注意力，用输出梯度的块范数分配反向保留概率，再对采样块按概率倒数重加权，估计dense梯度。要真正节省时间，必须在tiled反向内核里跳过相应访存与计算。先完整反传再把梯度置零，不具备同样成本；单次随机梯度也不会逐元素等于dense。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某query块的梯度贡献很小，可降低其反向执行概率；前向仍看过全部证据。只有没有实际执行被跳过块的反向工作，才可能获得相应速度收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31911v1">原论文</a> · <a href="../../../../foundation-models/2610.31911-lazyflash/">实现解读</a> · <a href="#qa-73f4f2504e86cd44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lazyflash" data-paper-title="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning 基础模型 Microsoft 2026-10-22 与稀疏前向attention不同，LazyFlash保留训练和部署前向完全dense。它按query block的dO Frobenius范数衡量梯度贡献，用gradient-mass budget约束预计丢弃量，并importance采样反向block。必须在tiled FlashAttention反向内部跳过内存访问/计算，才能兑现论文速度；用PyTorch dense backward后置零或toy mask不构成该方法的低成本完整实现。 成本过高，不复现（审查 DONE）。原文8张H200、65,536长度、2500steps，多个Qwen3模型和语音50K小时训练数据；所有计时在H200。自定义FlashAttention反向kernel及跨长度/模型/精度验证本身也超过本轮单卡低成本范围。不安装/编译kernel或加载权重来“试试”。无本地operator、metrics或GPUreceipt；无capability/evolve声明。原方法的定义性产物是可执行的tiled backward kernel，本轮不以通用softmax/mask代理充数。已读方法、实验及附录后终结完整复现成本审查。  推理与系统效率 长上下文训练 基础模型 训练预算：数据配比、目标与优化器 LazyFlash 的 importance backward 与固定 top-k 梯度块截断，估计性质一样吗？ importance采样按保留概率倒数重权，以dense梯度为无偏估计目标；固定截断一般没有这一保证。无偏针对随机性的期望，也不表示每一次抽样反向都与dense完全相同。 示意：某块只以一半概率保留，保留时需按对应概率补偿，而非永远删除低排名块。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-67cc8c10b70561d5">LazyFlash 的 importance backward 与固定 top-k 梯度块截断，估计性质一样吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alazyflash">LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>importance采样按保留概率倒数重权，以dense梯度为无偏估计目标；固定截断一般没有这一保证。无偏针对随机性的期望，也不表示每一次抽样反向都与dense完全相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某块只以一半概率保留，保留时需按对应概率补偿，而非永远删除低排名块。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31911v1">原论文</a> · <a href="../../../../foundation-models/2610.31911-lazyflash/">实现解读</a> · <a href="#qa-67cc8c10b70561d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lazyflash" data-paper-title="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning 基础模型 Microsoft 2026-10-22 与稀疏前向attention不同，LazyFlash保留训练和部署前向完全dense。它按query block的dO Frobenius范数衡量梯度贡献，用gradient-mass budget约束预计丢弃量，并importance采样反向block。必须在tiled FlashAttention反向内部跳过内存访问/计算，才能兑现论文速度；用PyTorch dense backward后置零或toy mask不构成该方法的低成本完整实现。 成本过高，不复现（审查 DONE）。原文8张H200、65,536长度、2500steps，多个Qwen3模型和语音50K小时训练数据；所有计时在H200。自定义FlashAttention反向kernel及跨长度/模型/精度验证本身也超过本轮单卡低成本范围。不安装/编译kernel或加载权重来“试试”。无本地operator、metrics或GPUreceipt；无capability/evolve声明。原方法的定义性产物是可执行的tiled backward kernel，本轮不以通用softmax/mask代理充数。已读方法、实验及附录后终结完整复现成本审查。  推理与系统效率 长上下文训练 基础模型 训练预算：数据配比、目标与优化器 在 PyTorch dense backward 后把梯度置零，为什么不算 LazyFlash kernel？ 主要访存与计算已经完成，后置mask没有省掉定义性反向工作。必须在tiled FlashAttention反向内部跳过相应操作；当前文档明确无本地operator或GPU回执，不以toy mask冒充实现。 示意：算完所有块再丢掉一半结果，不能报告为只计算了一半反向块。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-360bcff30d297860">在 PyTorch dense backward 后把梯度置零，为什么不算 LazyFlash kernel？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alazyflash">LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主要访存与计算已经完成，后置mask没有省掉定义性反向工作。必须在tiled FlashAttention反向内部跳过相应操作；当前文档明确无本地operator或GPU回执，不以toy mask冒充实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>算完所有块再丢掉一半结果，不能报告为只计算了一半反向块。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31911v1">原论文</a> · <a href="../../../../foundation-models/2610.31911-lazyflash/">实现解读</a> · <a href="#qa-360bcff30d297860">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rkl-policy-distillation" data-paper-title="Reverse-KL Policy Distillation: Statistical Guarantees and Limits" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Reverse-KL Policy Distillation: Statistical Guarantees and Limits 基础模型 University of Virginia 2026-10-22 反向 KL 的风险取决于候选策略自己的访问分布。仅在过往 rollout 状态上重新拟合 token KL，会把“候选自己很少到达的状态”算得过重。本文的在线 full-feedback Algorithm 1 同时截断累计 KL 和前缀重要性比，通过有界候选/rollout 比较更新策略空间中的指数权重。 状态为 not_run_scope_limited_protocol，不是“成本过高”或“已实证验证”。bounded_prefix_comparisons 实现 Eq.2/Eq.6；exponential_weights 固定 1/256；learn_online 实现 Algorithm 1。teacher 接口只能按 (h,state) 查询完整动作分布，每 episode 恰好查询次，不接收全局风险、最优候选或 gold trajectory。evaluate_exact_moments 是独立评估入口，用有限状态前向概率递推精确计算、和该 fixture 的最小可用；只能在训练返回之后运行。  策略蒸馏理论 有限策略空间在线学习 基础模型 训练预算：数据配比、目标与优化器 反向 KL 策略蒸馏为什么关注学生自己会访问哪些状态？ 目标是在候选策略自身访问分布下累积teacher与student的KL。不同策略走到的状态不同，把所有历史状态等权重拟合，可能偏离某候选实际需要控制的风险。 示意：某学生几乎不会进入的一条分支，不应仅因它曾在旧rollout出现就占同等风险权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-rkl-policy-distillation-fa9bc42e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c4f08e6c96bf34d9">反向 KL 策略蒸馏为什么关注学生自己会访问哪些状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arkl-policy-distillation">Reverse-KL Policy Distillation: Statistical Guarantees and Limits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是在候选策略自身访问分布下累积teacher与student的KL。不同策略走到的状态不同，把所有历史状态等权重拟合，可能偏离某候选实际需要控制的风险。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某学生几乎不会进入的一条分支，不应仅因它曾在旧rollout出现就占同等风险权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30844v1">原论文</a> · <a href="../../../../foundation-models/2610.30844-rkl-policy-distillation/">实现解读</a> · <a href="#qa-c4f08e6c96bf34d9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rkl-policy-distillation" data-paper-title="Reverse-KL Policy Distillation: Statistical Guarantees and Limits" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Reverse-KL Policy Distillation: Statistical Guarantees and Limits 基础模型 University of Virginia 2026-10-22 反向 KL 的风险取决于候选策略自己的访问分布。仅在过往 rollout 状态上重新拟合 token KL，会把“候选自己很少到达的状态”算得过重。本文的在线 full-feedback Algorithm 1 同时截断累计 KL 和前缀重要性比，通过有界候选/rollout 比较更新策略空间中的指数权重。 状态为 not_run_scope_limited_protocol，不是“成本过高”或“已实证验证”。bounded_prefix_comparisons 实现 Eq.2/Eq.6；exponential_weights 固定 1/256；learn_online 实现 Algorithm 1。teacher 接口只能按 (h,state) 查询完整动作分布，每 episode 恰好查询次，不接收全局风险、最优候选或 gold trajectory。evaluate_exact_moments 是独立评估入口，用有限状态前向概率递推精确计算、和该 fixture 的最小可用；只能在训练返回之后运行。  策略蒸馏理论 有限策略空间在线学习 基础模型 训练预算：数据配比、目标与优化器 反向KL蒸馏为何不能只在旧rollout状态上重拟合token KL？ 目标风险按候选策略自己的访问分布计算，旧策略频繁到达的状态可能被候选很少访问。该算法用截断的前缀重要性比与累计KL增量，构造有界候选比较，再更新整条策略的权重。前缀比不包含当前动作，同一个比值要乘在比较差的两项上；这与普通旧数据KL回归不同。 教学例子：旧策略常走一条失败支路，新候选几乎不会进入；不修正访问分布，就可能把这条支路上的token误差算得过重，掩盖候选真正会遇到的状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c10cf8835375ff57">反向KL蒸馏为何不能只在旧rollout状态上重拟合token KL？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arkl-policy-distillation">Reverse-KL Policy Distillation: Statistical Guarantees and Limits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标风险按候选策略自己的访问分布计算，旧策略频繁到达的状态可能被候选很少访问。该算法用截断的前缀重要性比与累计KL增量，构造有界候选比较，再更新整条策略的权重。前缀比不包含当前动作，同一个比值要乘在比较差的两项上；这与普通旧数据KL回归不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旧策略常走一条失败支路，新候选几乎不会进入；不修正访问分布，就可能把这条支路上的token误差算得过重，掩盖候选真正会遇到的状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30844v1">原论文</a> · <a href="../../../../foundation-models/2610.30844-rkl-policy-distillation/">实现解读</a> · <a href="#qa-c10cf8835375ff57">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rkl-policy-distillation" data-paper-title="Reverse-KL Policy Distillation: Statistical Guarantees and Limits" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Reverse-KL Policy Distillation: Statistical Guarantees and Limits 基础模型 University of Virginia 2026-10-22 反向 KL 的风险取决于候选策略自己的访问分布。仅在过往 rollout 状态上重新拟合 token KL，会把“候选自己很少到达的状态”算得过重。本文的在线 full-feedback Algorithm 1 同时截断累计 KL 和前缀重要性比，通过有界候选/rollout 比较更新策略空间中的指数权重。 状态为 not_run_scope_limited_protocol，不是“成本过高”或“已实证验证”。bounded_prefix_comparisons 实现 Eq.2/Eq.6；exponential_weights 固定 1/256；learn_online 实现 Algorithm 1。teacher 接口只能按 (h,state) 查询完整动作分布，每 episode 恰好查询次，不接收全局风险、最优候选或 gold trajectory。evaluate_exact_moments 是独立评估入口，用有限状态前向概率递推精确计算、和该 fixture 的最小可用；只能在训练返回之后运行。  策略蒸馏理论 有限策略空间在线学习 基础模型 训练预算：数据配比、目标与优化器 full-feedback teacher 分布与只给一个采样答案，监督信息有什么差异？ 本算法在到访状态查询完整动作分布，才能计算候选各动作的反向KL与比较量；单个采样答案不直接提供相同信息。还需teacher在候选正概率动作上有支持，否则KL可能无穷。 示意：只看到老师这次选A，不能据此知道它给B和C分别多少概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9d74e89df11f1c35">full-feedback teacher 分布与只给一个采样答案，监督信息有什么差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arkl-policy-distillation">Reverse-KL Policy Distillation: Statistical Guarantees and Limits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本算法在到访状态查询完整动作分布，才能计算候选各动作的反向KL与比较量；单个采样答案不直接提供相同信息。还需teacher在候选正概率动作上有支持，否则KL可能无穷。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只看到老师这次选A，不能据此知道它给B和C分别多少概率。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30844v1">原论文</a> · <a href="../../../../foundation-models/2610.30844-rkl-policy-distillation/">实现解读</a> · <a href="#qa-9d74e89df11f1c35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rkl-policy-distillation" data-paper-title="Reverse-KL Policy Distillation: Statistical Guarantees and Limits" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Reverse-KL Policy Distillation: Statistical Guarantees and Limits 基础模型 University of Virginia 2026-10-22 反向 KL 的风险取决于候选策略自己的访问分布。仅在过往 rollout 状态上重新拟合 token KL，会把“候选自己很少到达的状态”算得过重。本文的在线 full-feedback Algorithm 1 同时截断累计 KL 和前缀重要性比，通过有界候选/rollout 比较更新策略空间中的指数权重。 状态为 not_run_scope_limited_protocol，不是“成本过高”或“已实证验证”。bounded_prefix_comparisons 实现 Eq.2/Eq.6；exponential_weights 固定 1/256；learn_online 实现 Algorithm 1。teacher 接口只能按 (h,state) 查询完整动作分布，每 episode 恰好查询次，不接收全局风险、最优候选或 gold trajectory。evaluate_exact_moments 是独立评估入口，用有限状态前向概率递推精确计算、和该 fixture 的最小可用；只能在训练返回之后运行。  策略蒸馏理论 有限策略空间在线学习 基础模型 训练预算：数据配比、目标与优化器 前缀重要性比为什么必须排除当前 action，并同时乘差值两项？ 文档r_h的乘积只到u&lt;h，用同一个截断比加权candidate与rollout累计KL增量之差。把当前动作算进去或仅重权一项，会改变比较loss及其有界性质。 示意：比较第3个状态时，前缀只含前两步动作，不能先把第3步选择也纳入状态到达比。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c4630ce509123309">前缀重要性比为什么必须排除当前 action，并同时乘差值两项？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arkl-policy-distillation">Reverse-KL Policy Distillation: Statistical Guarantees and Limits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档r_h的乘积只到u&lt;h，用同一个截断比加权candidate与rollout累计KL增量之差。把当前动作算进去或仅重权一项，会改变比较loss及其有界性质。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>比较第3个状态时，前缀只含前两步动作，不能先把第3步选择也纳入状态到达比。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30844v1">原论文</a> · <a href="../../../../foundation-models/2610.30844-rkl-policy-distillation/">实现解读</a> · <a href="#qa-c4630ce509123309">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:t-muon" data-paper-title="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training 基础模型 University of California, Santa Barbara 2026-10-18 普通 Muon 逐矩阵求 polar。本文先把结构相关矩阵放进三阶张量，再在第三轴变换域分别求 polar；这不是把张量任意展平后运行普通 Muon。分组方式与变换方式是两个独立选择：论文比较相邻层、QKV、单矩阵的 head、QKV 的 head-stack。 与单张 A100/A30 或本地 Mac 的低成本验证目标不匹配，完整训练成本过高，不复现（审查 DONE）。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。A100的polar参考误差均值约1.31e-14、参数更新参考误差约1.34e-16；只证明小矩阵实现一致，不证明论文PPL改善、预训练稳定性或内核加速。见实际指标和GPU回执，执行源码绑定冻结提交324217ed26fe2e297e25879ad092281eb0960b87。  预训练与数据 优化器与张量几何 基础模型 训练预算：数据配比、目标与优化器 T-MUON 为什么把结构相关矩阵放进第三个张量轴？ 它希望联合利用层、QKV或head之间的结构关系，在第三轴变换后逐切片求polar，再逆变换还原矩阵更新。相关矩阵的分组与所选变换都是方法的一部分。 示意：将Q/K/V作为相关切片组织，比把三个矩阵当作毫无关系的独立对象多了一种耦合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-t-muon-99464230" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7bd4af109e8d4f82">T-MUON 为什么把结构相关矩阵放进第三个张量轴？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3At-muon">T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它希望联合利用层、QKV或head之间的结构关系，在第三轴变换后逐切片求polar，再逆变换还原矩阵更新。相关矩阵的分组与所选变换都是方法的一部分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>将Q/K/V作为相关切片组织，比把三个矩阵当作毫无关系的独立对象多了一种耦合。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24938">原论文</a> · <a href="../../../../foundation-models/2610.24938-t-muon/">实现解读</a> · <a href="#qa-7bd4af109e8d4f82">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:t-muon" data-paper-title="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training 基础模型 University of California, Santa Barbara 2026-10-18 普通 Muon 逐矩阵求 polar。本文先把结构相关矩阵放进三阶张量，再在第三轴变换域分别求 polar；这不是把张量任意展平后运行普通 Muon。分组方式与变换方式是两个独立选择：论文比较相邻层、QKV、单矩阵的 head、QKV 的 head-stack。 与单张 A100/A30 或本地 Mac 的低成本验证目标不匹配，完整训练成本过高，不复现（审查 DONE）。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。A100的polar参考误差均值约1.31e-14、参数更新参考误差约1.34e-16；只证明小矩阵实现一致，不证明论文PPL改善、预训练稳定性或内核加速。见实际指标和GPU回执，执行源码绑定冻结提交324217ed26fe2e297e25879ad092281eb0960b87。  预训练与数据 优化器与张量几何 基础模型 训练预算：数据配比、目标与优化器 T-MUON为何先把相关矩阵组成三阶张量，而不是直接展平后做普通Muon？ 它在第三轴的变换域中分别求polar，再逆变换回各矩阵，使结构相关矩阵能够在该轴上耦合。矩阵如何分组与选择什么变换是独立设计，任意展平会丢掉这层定义。还原后的形状缩放依据原矩阵，零秩切片不能因任意零空间基产生虚假更新。 教学例子：把相邻层或Q/K/V作为第三轴的几片，先在该轴混合再分别正交化，与把所有数拼成一张长矩阵正交化，约束和结果都不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1d73398509874a34">T-MUON为何先把相关矩阵组成三阶张量，而不是直接展平后做普通Muon？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3At-muon">T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它在第三轴的变换域中分别求polar，再逆变换回各矩阵，使结构相关矩阵能够在该轴上耦合。矩阵如何分组与选择什么变换是独立设计，任意展平会丢掉这层定义。还原后的形状缩放依据原矩阵，零秩切片不能因任意零空间基产生虚假更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把相邻层或Q/K/V作为第三轴的几片，先在该轴混合再分别正交化，与把所有数拼成一张长矩阵正交化，约束和结果都不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24938">原论文</a> · <a href="../../../../foundation-models/2610.24938-t-muon/">实现解读</a> · <a href="#qa-1d73398509874a34">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:t-muon" data-paper-title="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training 基础模型 University of California, Santa Barbara 2026-10-18 普通 Muon 逐矩阵求 polar。本文先把结构相关矩阵放进三阶张量，再在第三轴变换域分别求 polar；这不是把张量任意展平后运行普通 Muon。分组方式与变换方式是两个独立选择：论文比较相邻层、QKV、单矩阵的 head、QKV 的 head-stack。 与单张 A100/A30 或本地 Mac 的低成本验证目标不匹配，完整训练成本过高，不复现（审查 DONE）。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。A100的polar参考误差均值约1.31e-14、参数更新参考误差约1.34e-16；只证明小矩阵实现一致，不证明论文PPL改善、预训练稳定性或内核加速。见实际指标和GPU回执，执行源码绑定冻结提交324217ed26fe2e297e25879ad092281eb0960b87。  预训练与数据 优化器与张量几何 基础模型 训练预算：数据配比、目标与优化器 T-MUON 的分组方式与变换方式，为什么应作为两条独立消融轴？ 分组决定哪些矩阵一起处理，变换决定这些切片如何混合；同一组可用不同M，不同组也可用同一类变换。把二者同时换掉，就难判断更新差异来自哪一项。 示意：QKV-stack配DCT与head-stack配DFT同时不同，不能只归因为DFT。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-75bd9f5e9dcf98a8">T-MUON 的分组方式与变换方式，为什么应作为两条独立消融轴？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3At-muon">T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分组决定哪些矩阵一起处理，变换决定这些切片如何混合；同一组可用不同M，不同组也可用同一类变换。把二者同时换掉，就难判断更新差异来自哪一项。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>QKV-stack配DCT与head-stack配DFT同时不同，不能只归因为DFT。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24938">原论文</a> · <a href="../../../../foundation-models/2610.24938-t-muon/">实现解读</a> · <a href="#qa-75bd9f5e9dcf98a8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:t-muon" data-paper-title="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training 基础模型 University of California, Santa Barbara 2026-10-18 普通 Muon 逐矩阵求 polar。本文先把结构相关矩阵放进三阶张量，再在第三轴变换域分别求 polar；这不是把张量任意展平后运行普通 Muon。分组方式与变换方式是两个独立选择：论文比较相邻层、QKV、单矩阵的 head、QKV 的 head-stack。 与单张 A100/A30 或本地 Mac 的低成本验证目标不匹配，完整训练成本过高，不复现（审查 DONE）。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。A100的polar参考误差均值约1.31e-14、参数更新参考误差约1.34e-16；只证明小矩阵实现一致，不证明论文PPL改善、预训练稳定性或内核加速。见实际指标和GPU回执，执行源码绑定冻结提交324217ed26fe2e297e25879ad092281eb0960b87。  预训练与数据 优化器与张量几何 基础模型 训练预算：数据配比、目标与优化器 T-MUON 的 fan 比例应该按 head 切片还是原权重矩阵计算？ 文档还原后使用原始矩阵fan_out/fan_in缩放，不能改成拆出的head形状。零秩切片还应返回零更新，避免薄SVD任意零空间基产生虚假方向；当前精确SVD不等于生产polar内核速度。 示意：一张矩阵拆成多个head处理后，缩放仍需回到原矩阵的维度口径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1f0938a0551233c2">T-MUON 的 fan 比例应该按 head 切片还是原权重矩阵计算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3At-muon">T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档还原后使用原始矩阵fan_out/fan_in缩放，不能改成拆出的head形状。零秩切片还应返回零更新，避免薄SVD任意零空间基产生虚假方向；当前精确SVD不等于生产polar内核速度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一张矩阵拆成多个head处理后，缩放仍需回到原矩阵的维度口径。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24938">原论文</a> · <a href="../../../../foundation-models/2610.24938-t-muon/">实现解读</a> · <a href="#qa-1f0938a0551233c2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bmuon" data-paper-title="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility 基础模型 Inria 2026-10-16 Muon的spectral-norm更新不一定产生容易按隐藏通道剪枝的权重。BMuon不在前向额外加gate，也不只是对训练好的Muon模型剪枝；它让所有MLP块的隐藏通道共享同一分配预算，并在每个通道的输入行/输出列两侧共同改变更新几何。原文Figure 1展示结构化剪枝结果；核心方法最直接的来源为Algorithm1和Eq7/8。该结果图不是本地测量。 完整实验成本过高，不复现（审查 DONE）。BudgetMuon接受多个真实配对MLP，执行梯度、Nesterov动量、全局预算MM及双边参数更新。当前采用小矩阵精确SVD polar，不是原文生产实现的5步Newton–Schulz；不宣称运行速度相同。支持FP32/FP64；FP16/BF16明确拒绝，不默许低精度数值问题。缺失一侧梯度也拒绝，避免破坏通道耦合。  预训练与数据 优化器与结构化可压缩性 基础模型 训练预算：数据配比、目标与优化器 BMuon 希望优化器学出哪种更容易剪枝的结构？ 它针对MLP隐藏通道，改变成对输入行与输出列的更新几何，使所有块在同一个通道预算下分配资源。它不是前向额外加gate，也不是训练后随意按幅度删权重。 示意：一个隐藏通道的输入行与输出列是一对，需要一起考虑其保留价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-bmuon-2e7cc5f8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-18648aced26656c9">BMuon 希望优化器学出哪种更容易剪枝的结构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abmuon">BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它针对MLP隐藏通道，改变成对输入行与输出列的更新几何，使所有块在同一个通道预算下分配资源。它不是前向额外加gate，也不是训练后随意按幅度删权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个隐藏通道的输入行与输出列是一对，需要一起考虑其保留价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23571">原论文</a> · <a href="../../../../foundation-models/2610.23571-bmuon/">实现解读</a> · <a href="#qa-18648aced26656c9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bmuon" data-paper-title="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility 基础模型 Inria 2026-10-16 Muon的spectral-norm更新不一定产生容易按隐藏通道剪枝的权重。BMuon不在前向额外加gate，也不只是对训练好的Muon模型剪枝；它让所有MLP块的隐藏通道共享同一分配预算，并在每个通道的输入行/输出列两侧共同改变更新几何。原文Figure 1展示结构化剪枝结果；核心方法最直接的来源为Algorithm1和Eq7/8。该结果图不是本地测量。 完整实验成本过高，不复现（审查 DONE）。BudgetMuon接受多个真实配对MLP，执行梯度、Nesterov动量、全局预算MM及双边参数更新。当前采用小矩阵精确SVD polar，不是原文生产实现的5步Newton–Schulz；不宣称运行速度相同。支持FP32/FP64；FP16/BF16明确拒绝，不默许低精度数值问题。缺失一侧梯度也拒绝，避免破坏通道耦合。  预训练与数据 优化器与结构化可压缩性 基础模型 训练预算：数据配比、目标与优化器 BMuon的通道预算为什么要跨全部MLP共享，还同时作用于输入行和输出列？ 一个隐藏通道由输入矩阵的一行和输出矩阵的一列共同定义；只改变一侧不完整。BMuon让所有MLP通道竞争同一总分配预算，并在两侧的Muon更新几何中使用该分配，使不同层之间也能重新分配可压缩性。它是在训练更新中塑造结构，不是额外前向gate或事后各层独立剪枝。 教学例子：总共只留100份通道预算时，两层不必各拿50；更有贡献的一层可拿更多，但每个通道的入边和出边都应按同一分配一起处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-90c13d183e56fedd">BMuon的通道预算为什么要跨全部MLP共享，还同时作用于输入行和输出列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abmuon">BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个隐藏通道由输入矩阵的一行和输出矩阵的一列共同定义；只改变一侧不完整。BMuon让所有MLP通道竞争同一总分配预算，并在两侧的Muon更新几何中使用该分配，使不同层之间也能重新分配可压缩性。它是在训练更新中塑造结构，不是额外前向gate或事后各层独立剪枝。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>总共只留100份通道预算时，两层不必各拿50；更有贡献的一层可拿更多，但每个通道的入边和出边都应按同一分配一起处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23571">原论文</a> · <a href="../../../../foundation-models/2610.23571-bmuon/">实现解读</a> · <a href="#qa-90c13d183e56fedd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bmuon" data-paper-title="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility 基础模型 Inria 2026-10-16 Muon的spectral-norm更新不一定产生容易按隐藏通道剪枝的权重。BMuon不在前向额外加gate，也不只是对训练好的Muon模型剪枝；它让所有MLP块的隐藏通道共享同一分配预算，并在每个通道的输入行/输出列两侧共同改变更新几何。原文Figure 1展示结构化剪枝结果；核心方法最直接的来源为Algorithm1和Eq7/8。该结果图不是本地测量。 完整实验成本过高，不复现（审查 DONE）。BudgetMuon接受多个真实配对MLP，执行梯度、Nesterov动量、全局预算MM及双边参数更新。当前采用小矩阵精确SVD polar，不是原文生产实现的5步Newton–Schulz；不宣称运行速度相同。支持FP32/FP64；FP16/BF16明确拒绝，不默许低精度数值问题。缺失一侧梯度也拒绝，避免破坏通道耦合。  预训练与数据 优化器与结构化可压缩性 基础模型 训练预算：数据配比、目标与优化器 全局通道预算 BMuon，与每层各保留相同比例有什么不同？ 全局约束允许不同MLP块竞争同一预算，总和为K；逐层固定比例提前限制了每层分配。两者即使最终通道总数相同，也可能把资源放在不同层。 示意：一层可得到较多通道、另一层较少，而不是每层机械地裁掉50%。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2a048970da0e26b7">全局通道预算 BMuon，与每层各保留相同比例有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abmuon">BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局约束允许不同MLP块竞争同一预算，总和为K；逐层固定比例提前限制了每层分配。两者即使最终通道总数相同，也可能把资源放在不同层。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一层可得到较多通道、另一层较少，而不是每层机械地裁掉50%。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23571">原论文</a> · <a href="../../../../foundation-models/2610.23571-bmuon/">实现解读</a> · <a href="#qa-2a048970da0e26b7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bmuon" data-paper-title="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility 基础模型 Inria 2026-10-16 Muon的spectral-norm更新不一定产生容易按隐藏通道剪枝的权重。BMuon不在前向额外加gate，也不只是对训练好的Muon模型剪枝；它让所有MLP块的隐藏通道共享同一分配预算，并在每个通道的输入行/输出列两侧共同改变更新几何。原文Figure 1展示结构化剪枝结果；核心方法最直接的来源为Algorithm1和Eq7/8。该结果图不是本地测量。 完整实验成本过高，不复现（审查 DONE）。BudgetMuon接受多个真实配对MLP，执行梯度、Nesterov动量、全局预算MM及双边参数更新。当前采用小矩阵精确SVD polar，不是原文生产实现的5步Newton–Schulz；不宣称运行速度相同。支持FP32/FP64；FP16/BF16明确拒绝，不默许低精度数值问题。缺失一侧梯度也拒绝，避免破坏通道耦合。  预训练与数据 优化器与结构化可压缩性 基础模型 训练预算：数据配比、目标与优化器 BMuon 完成预算 MM 更新后，能沿用旧分配的 polar 更新吗？ 不能。旧分配用于计算MM分数，新分配求出后必须重算双边polar更新；跨全部块共用一个预算乘子。缺失配对一侧梯度也不能静默继续，否则破坏输入行/输出列耦合。 示意：通道预算从0.2改到0.8后，参数方向需反映新权重，而非仍用旧μ算出的方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-711aa2a30cd60dce">BMuon 完成预算 MM 更新后，能沿用旧分配的 polar 更新吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abmuon">BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。旧分配用于计算MM分数，新分配求出后必须重算双边polar更新；跨全部块共用一个预算乘子。缺失配对一侧梯度也不能静默继续，否则破坏输入行/输出列耦合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>通道预算从0.2改到0.8后，参数方向需反映新权重，而非仍用旧μ算出的方向。</p>
<p class="ar-learning-sources">依据：核心公式、实现与运行；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23571">原论文</a> · <a href="../../../../foundation-models/2610.23571-bmuon/">实现解读</a> · <a href="#qa-711aa2a30cd60dce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bit-sparse" data-paper-title="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks 基础模型 University of Cambridge 2026-10-15 ReLU 家族已有大量精确零；BitSparse 保存 bitmask、正值和 tile prefix，在反向时无损重建，避免靠有损量化或额外前向换空间。§3 定义格式，公式 1–2 与 Appendix C 定义 ReLU/ReLU² 线性层反向。 按原文 RTX3090 约 7.4–7.7秒/步×3350 步推算单臂约 7小时，成本过高，不复现（审查 DONE）；CUDA诊断记录与真实GPU回执保存设备、种子及执行源码身份。无模型或数据下载。三个 seed 的合成输入 revision 为 synthetic-formula-and-bit-patterns@oct17-foundation-components-v1。BF16 33×37 激活检验含 padding 的 tile 格式；另以双精度 9×13 输入、7×13 权重做独立 dense 前向/反向参考。tile 8 是有意缩小的格式验收，不是原文默认 tile64 的性能测试。  训练与系统效率 无损激活压缩 基础模型 训练预算：数据配比、目标与优化器 BitSparse 为什么适合 ReLU 家族产生的大量精确零？ 精确零不必逐项保存数值，只需用bitmask记录位置、压紧保存正值，再用tile前缀定位。反向可无损重建需要的激活，不依赖把非零数值近似量化。 示意：十个位置只有两个正值时，保存两个值及其位置，而非十份浮点数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-bit-sparse-b3242cb0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-91e3e0af62bbebf1">BitSparse 为什么适合 ReLU 家族产生的大量精确零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abit-sparse">BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>精确零不必逐项保存数值，只需用bitmask记录位置、压紧保存正值，再用tile前缀定位。反向可无损重建需要的激活，不依赖把非零数值近似量化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十个位置只有两个正值时，保存两个值及其位置，而非十份浮点数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22256">原论文</a> · <a href="../../../../foundation-models/2610.22256-bit-sparse/">实现解读</a> · <a href="#qa-91e3e0af62bbebf1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bit-sparse" data-paper-title="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks 基础模型 University of Cambridge 2026-10-15 ReLU 家族已有大量精确零；BitSparse 保存 bitmask、正值和 tile prefix，在反向时无损重建，避免靠有损量化或额外前向换空间。§3 定义格式，公式 1–2 与 Appendix C 定义 ReLU/ReLU² 线性层反向。 按原文 RTX3090 约 7.4–7.7秒/步×3350 步推算单臂约 7小时，成本过高，不复现（审查 DONE）；CUDA诊断记录与真实GPU回执保存设备、种子及执行源码身份。无模型或数据下载。三个 seed 的合成输入 revision 为 synthetic-formula-and-bit-patterns@oct17-foundation-components-v1。BF16 33×37 激活检验含 padding 的 tile 格式；另以双精度 9×13 输入、7×13 权重做独立 dense 前向/反向参考。tile 8 是有意缩小的格式验收，不是原文默认 tile64 的性能测试。  训练与系统效率 无损激活压缩 基础模型 训练预算：数据配比、目标与优化器 BitSparse为什么可以无损减少激活存储，却不需要额外重跑一次前向？ ReLU家族激活已有精确零，方法只保存非零值、每位置一bit的mask与分块前缀，反向时重建原激活。它利用结构性零而非降低非零值精度，也不靠重新计算补回丢掉的信息。能否节省空间取决于零比例和元数据成本，不能只看到用了bitmask就忽略仍需保存的正值。 教学例子：8个激活中6个为零，可保存8位mask加2个原精度数值；反向按mask把两个数放回原位，不必再次执行生成这些激活的网络。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8d6a729d709d628c">BitSparse为什么可以无损减少激活存储，却不需要额外重跑一次前向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abit-sparse">BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ReLU家族激活已有精确零，方法只保存非零值、每位置一bit的mask与分块前缀，反向时重建原激活。它利用结构性零而非降低非零值精度，也不靠重新计算补回丢掉的信息。能否节省空间取决于零比例和元数据成本，不能只看到用了bitmask就忽略仍需保存的正值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>8个激活中6个为零，可保存8位mask加2个原精度数值；反向按mask把两个数放回原位，不必再次执行生成这些激活的网络。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22256">原论文</a> · <a href="../../../../foundation-models/2610.22256-bit-sparse/">实现解读</a> · <a href="#qa-8d6a729d709d628c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bit-sparse" data-paper-title="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks 基础模型 University of Cambridge 2026-10-15 ReLU 家族已有大量精确零；BitSparse 保存 bitmask、正值和 tile prefix，在反向时无损重建，避免靠有损量化或额外前向换空间。§3 定义格式，公式 1–2 与 Appendix C 定义 ReLU/ReLU² 线性层反向。 按原文 RTX3090 约 7.4–7.7秒/步×3350 步推算单臂约 7小时，成本过高，不复现（审查 DONE）；CUDA诊断记录与真实GPU回执保存设备、种子及执行源码身份。无模型或数据下载。三个 seed 的合成输入 revision 为 synthetic-formula-and-bit-patterns@oct17-foundation-components-v1。BF16 33×37 激活检验含 padding 的 tile 格式；另以双精度 9×13 输入、7×13 权重做独立 dense 前向/反向参考。tile 8 是有意缩小的格式验收，不是原文默认 tile64 的性能测试。  训练与系统效率 无损激活压缩 基础模型 训练预算：数据配比、目标与优化器 BitSparse 的无损打包，与 activation checkpointing 或低比特量化有什么区别？ checkpointing通常以额外前向重算换存储，量化以数值误差换位宽；BitSparse利用精确零的稀疏性压紧数值并重建。实际节省取决于稀疏度及mask/prefix开销，不等于总训练显存同幅下降。 示意：稀疏率很低时，额外索引开销可能抵消一部分压紧收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e0e29b6ea78fe4f7">BitSparse 的无损打包，与 activation checkpointing 或低比特量化有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abit-sparse">BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>checkpointing通常以额外前向重算换存储，量化以数值误差换位宽；BitSparse利用精确零的稀疏性压紧数值并重建。实际节省取决于稀疏度及mask/prefix开销，不等于总训练显存同幅下降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>稀疏率很低时，额外索引开销可能抵消一部分压紧收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、结果与独立对照；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22256">原论文</a> · <a href="../../../../foundation-models/2610.22256-bit-sparse/">实现解读</a> · <a href="#qa-e0e29b6ea78fe4f7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bit-sparse" data-paper-title="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks 基础模型 University of Cambridge 2026-10-15 ReLU 家族已有大量精确零；BitSparse 保存 bitmask、正值和 tile prefix，在反向时无损重建，避免靠有损量化或额外前向换空间。§3 定义格式，公式 1–2 与 Appendix C 定义 ReLU/ReLU² 线性层反向。 按原文 RTX3090 约 7.4–7.7秒/步×3350 步推算单臂约 7小时，成本过高，不复现（审查 DONE）；CUDA诊断记录与真实GPU回执保存设备、种子及执行源码身份。无模型或数据下载。三个 seed 的合成输入 revision 为 synthetic-formula-and-bit-patterns@oct17-foundation-components-v1。BF16 33×37 激活检验含 padding 的 tile 格式；另以双精度 9×13 输入、7×13 权重做独立 dense 前向/反向参考。tile 8 是有意缩小的格式验收，不是原文默认 tile64 的性能测试。  训练与系统效率 无损激活压缩 基础模型 训练预算：数据配比、目标与优化器 为什么 BitSparse 的 mask 不能用每元素一字节 bool 冒充？ 文档格式是每位置1 bit，另存tile prefix与正值；bool每元素1 byte会改变空间口径。还需核对padding、零符号和反向公式，例如ReLU²的输入梯度含2H因子。 示意：32个位置的bitmask应约4字节，而非32字节布尔数组。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c1d398da0aac882a">为什么 BitSparse 的 mask 不能用每元素一字节 bool 冒充？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abit-sparse">BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档格式是每位置1 bit，另存tile prefix与正值；bool每元素1 byte会改变空间口径。还需核对padding、零符号和反向公式，例如ReLU²的输入梯度含2H因子。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>32个位置的bitmask应约4字节，而非32字节布尔数组。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与运行；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22256">原论文</a> · <a href="../../../../foundation-models/2610.22256-bit-sparse/">实现解读</a> · <a href="#qa-c1d398da0aac882a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hardware-diversity" data-paper-title="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs 基础模型 Meta 2026-10-15 CUDA 程序能够转换为 HIP，不代表跨硬件性能相同。本文以推荐训练为案例，联合修改模型/并行与内存策略，用分析模型选择 GEMM 配置，并用 Agent 辅助编译、调试和内核移植；它是系统研究报告，而非单一新推荐模型。 成本过高且硬件不匹配，不复现（审查 DONE）。研究资料；成本过高且硬件不匹配，不复现（审查 DONE）。不下载生产模型、不尝试集群训练，不注册可执行 adapter，不接入 Evolve；下文结果均来自论文，不是本地 GPU 测量。状态为成本过高，不复现（审查 DONE），不是待自动重试 TODO，也不是算法已实现。资料收录不阻塞其他组件或审查水位；若以后明确要求实现某个公开算子，应重新界定该算子、硬件和验证合同，不冒充完整生产系统复现。本轮仅完成元数据、正文与成本审查。原配置依赖 MI350X/B200 集群和私有工作负载，现有一张 A100 或 A30 无法等价复现；不启动下载、性能探跑或完整训练。  训练系统 硬件模型协同设计 推荐训练系统 基础模型 训练预算：数据配比、目标与优化器 Meta/AMD 硬件多样性报告为什么被归为系统协同设计？ 它以推荐训练为案例同时调整模型、并行、内存策略、GEMM配置和内核移植，并非只提出一个新的推荐网络。性能来自整条系统链路的匹配，而非CUDA转成HIP这一件事。 示意：算子可以编译，并不说明其tile、访存和并行布局适合目标设备。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-hardware-diversity-2c171dec" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-853280a6dfb4900a">Meta/AMD 硬件多样性报告为什么被归为系统协同设计？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahardware-diversity">Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它以推荐训练为案例同时调整模型、并行、内存策略、GEMM配置和内核移植，并非只提出一个新的推荐网络。性能来自整条系统链路的匹配，而非CUDA转成HIP这一件事。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>算子可以编译，并不说明其tile、访存和并行布局适合目标设备。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22230">原论文</a> · <a href="../../../../foundation-models/2610.22230-hardware-diversity/">实现解读</a> · <a href="#qa-853280a6dfb4900a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hardware-diversity" data-paper-title="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs 基础模型 Meta 2026-10-15 CUDA 程序能够转换为 HIP，不代表跨硬件性能相同。本文以推荐训练为案例，联合修改模型/并行与内存策略，用分析模型选择 GEMM 配置，并用 Agent 辅助编译、调试和内核移植；它是系统研究报告，而非单一新推荐模型。 成本过高且硬件不匹配，不复现（审查 DONE）。研究资料；成本过高且硬件不匹配，不复现（审查 DONE）。不下载生产模型、不尝试集群训练，不注册可执行 adapter，不接入 Evolve；下文结果均来自论文，不是本地 GPU 测量。状态为成本过高，不复现（审查 DONE），不是待自动重试 TODO，也不是算法已实现。资料收录不阻塞其他组件或审查水位；若以后明确要求实现某个公开算子，应重新界定该算子、硬件和验证合同，不冒充完整生产系统复现。本轮仅完成元数据、正文与成本审查。原配置依赖 MI350X/B200 集群和私有工作负载，现有一张 A100 或 A30 无法等价复现；不启动下载、性能探跑或完整训练。  训练系统 硬件模型协同设计 推荐训练系统 基础模型 训练预算：数据配比、目标与优化器 CUDA代码转成HIP后能运行，为什么还不能认为跨硬件性能已经迁移？ 接口兼容只解决能否执行；计算单元、内存层次、tile形状与并行策略会改变实际瓶颈。该研究联合模型、内存、并行与内核选型，并用分析模型估计计算、访存和尾部空转。硬件常数与最佳配置依设备而变，不能把一张卡的选型结果直接搬到另一张卡当作已测加速。 教学例子：同一个GEMM tile在一类设备上充分占满计算单元，换设备后却可能受共享内存或尾部工作量限制；成功编译并不会自动修复这种布局不匹配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1a1c64a8f0514de8">CUDA代码转成HIP后能运行，为什么还不能认为跨硬件性能已经迁移？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahardware-diversity">Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>接口兼容只解决能否执行；计算单元、内存层次、tile形状与并行策略会改变实际瓶颈。该研究联合模型、内存、并行与内核选型，并用分析模型估计计算、访存和尾部空转。硬件常数与最佳配置依设备而变，不能把一张卡的选型结果直接搬到另一张卡当作已测加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一个GEMM tile在一类设备上充分占满计算单元，换设备后却可能受共享内存或尾部工作量限制；成功编译并不会自动修复这种布局不匹配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22230">原论文</a> · <a href="../../../../foundation-models/2610.22230-hardware-diversity/">实现解读</a> · <a href="#qa-1a1c64a8f0514de8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hardware-diversity" data-paper-title="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs 基础模型 Meta 2026-10-15 CUDA 程序能够转换为 HIP，不代表跨硬件性能相同。本文以推荐训练为案例，联合修改模型/并行与内存策略，用分析模型选择 GEMM 配置，并用 Agent 辅助编译、调试和内核移植；它是系统研究报告，而非单一新推荐模型。 成本过高且硬件不匹配，不复现（审查 DONE）。研究资料；成本过高且硬件不匹配，不复现（审查 DONE）。不下载生产模型、不尝试集群训练，不注册可执行 adapter，不接入 Evolve；下文结果均来自论文，不是本地 GPU 测量。状态为成本过高，不复现（审查 DONE），不是待自动重试 TODO，也不是算法已实现。资料收录不阻塞其他组件或审查水位；若以后明确要求实现某个公开算子，应重新界定该算子、硬件和验证合同，不冒充完整生产系统复现。本轮仅完成元数据、正文与成本审查。原配置依赖 MI350X/B200 集群和私有工作负载，现有一张 A100 或 A30 无法等价复现；不启动下载、性能探跑或完整训练。  训练系统 硬件模型协同设计 推荐训练系统 基础模型 训练预算：数据配比、目标与优化器 分析模型预测的 tile 周期，与真实端到端吞吐包含的信息相同吗？ 分析模型估算计算、分层访存、流水线和尾部空转；端到端测量还取决于实际系统与工作负载。硬件常数不能跨设备照搬，局部tile最优也不自动等于整个训练最优。 示意：某tile的矩阵乘更快，可能仍被同步或其它阶段耗时抵消。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1cf4361c1253ac31">分析模型预测的 tile 周期，与真实端到端吞吐包含的信息相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahardware-diversity">Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分析模型估算计算、分层访存、流水线和尾部空转；端到端测量还取决于实际系统与工作负载。硬件常数不能跨设备照搬，局部tile最优也不自动等于整个训练最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某tile的矩阵乘更快，可能仍被同步或其它阶段耗时抵消。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22230">原论文</a> · <a href="../../../../foundation-models/2610.22230-hardware-diversity/">实现解读</a> · <a href="#qa-1cf4361c1253ac31">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hardware-diversity" data-paper-title="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs 基础模型 Meta 2026-10-15 CUDA 程序能够转换为 HIP，不代表跨硬件性能相同。本文以推荐训练为案例，联合修改模型/并行与内存策略，用分析模型选择 GEMM 配置，并用 Agent 辅助编译、调试和内核移植；它是系统研究报告，而非单一新推荐模型。 成本过高且硬件不匹配，不复现（审查 DONE）。研究资料；成本过高且硬件不匹配，不复现（审查 DONE）。不下载生产模型、不尝试集群训练，不注册可执行 adapter，不接入 Evolve；下文结果均来自论文，不是本地 GPU 测量。状态为成本过高，不复现（审查 DONE），不是待自动重试 TODO，也不是算法已实现。资料收录不阻塞其他组件或审查水位；若以后明确要求实现某个公开算子，应重新界定该算子、硬件和验证合同，不冒充完整生产系统复现。本轮仅完成元数据、正文与成本审查。原配置依赖 MI350X/B200 集群和私有工作负载，现有一张 A100 或 A30 无法等价复现；不启动下载、性能探跑或完整训练。  训练系统 硬件模型协同设计 推荐训练系统 基础模型 训练预算：数据配比、目标与优化器 只有一张 A100/A30，能等价复跑报告的 MI350X/B200 生产系统吗？ 不能。文档原配置依赖相应集群和私有工作负载，本轮仅收录和成本审查，明确不复现。若实现某个公开算子，应重新规定该算子的硬件与验收，不把它当完整生产系统。 示意：在A100上跑一个小GEMM，不足以验证另一硬件集群的端到端训练吞吐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-752b38d08848c516">只有一张 A100/A30，能等价复跑报告的 MI350X/B200 生产系统吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahardware-diversity">Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。文档原配置依赖相应集群和私有工作负载，本轮仅收录和成本审查，明确不复现。若实现某个公开算子，应重新规定该算子的硬件与验收，不把它当完整生产系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>在A100上跑一个小GEMM，不足以验证另一硬件集群的端到端训练吞吐。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22230">原论文</a> · <a href="../../../../foundation-models/2610.22230-hardware-diversity/">实现解读</a> · <a href="#qa-752b38d08848c516">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lct" data-paper-title="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training 基础模型 University of Cambridge 2026-10-15 浮点指数往往比 sign/mantissa 更可压缩，但训练需要反复编码。LCT 将两部分分开，以固定模型预计算短码，运行时中心变换适应量级，循环 stream 在固定预算之外保留原始指数尾。主源 §4、Appendix B/C；不是用通用 zlib 压缩替代算法。 完整链路成本过高，不复现（审查 DONE），不启动探跑；CUDA诊断记录与真实GPU回执保存设备、种子与源码身份。不下载模型或语料。revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，seeds42/43/44。使用公开定义的合成 BF16 位模式：512个元素中的前256个覆盖所有指数，另改变 sign/fraction；固定码表模型不是根据测试输入拟合。16 streams×32-bit预算故意产生 overflow；另以充足预算及其他中心检查还原。  训练与系统效率 无损浮点编码 基础模型 训练预算：数据配比、目标与优化器 LCT 为什么把浮点指数与 sign/mantissa 分开存储？ 指数分布常更集中，适合重复编码；sign/fraction位则保持原样。LCT用固定概率模型产生有界短码，再处理运行时中心变化，以无损还原为约束，而非丢掉低频位。 示意：很多数值共享相近指数时，可压缩指数部分，同时不改动原来的小数位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-lct-f385814a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8f32908d4070ebe7">LCT 为什么把浮点指数与 sign/mantissa 分开存储？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alct">LCT: Losslessly Compressed Tensors with GPU friendly execution for Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>指数分布常更集中，适合重复编码；sign/fraction位则保持原样。LCT用固定概率模型产生有界短码，再处理运行时中心变化，以无损还原为约束，而非丢掉低频位。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>很多数值共享相近指数时，可压缩指数部分，同时不改动原来的小数位。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22179">原论文</a> · <a href="../../../../foundation-models/2610.22179-lct/">实现解读</a> · <a href="#qa-8f32908d4070ebe7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lct" data-paper-title="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training 基础模型 University of Cambridge 2026-10-15 浮点指数往往比 sign/mantissa 更可压缩，但训练需要反复编码。LCT 将两部分分开，以固定模型预计算短码，运行时中心变换适应量级，循环 stream 在固定预算之外保留原始指数尾。主源 §4、Appendix B/C；不是用通用 zlib 压缩替代算法。 完整链路成本过高，不复现（审查 DONE），不启动探跑；CUDA诊断记录与真实GPU回执保存设备、种子与源码身份。不下载模型或语料。revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，seeds42/43/44。使用公开定义的合成 BF16 位模式：512个元素中的前256个覆盖所有指数，另改变 sign/fraction；固定码表模型不是根据测试输入拟合。16 streams×32-bit预算故意产生 overflow；另以充足预算及其他中心检查还原。  训练与系统效率 无损浮点编码 基础模型 训练预算：数据配比、目标与优化器 LCT压缩指数时，罕见符号或stream超预算为什么也不能丢掉？ 目标是逐bit可还原，因此罕见指数使用escape加原始符号，流预算耗尽后的剩余项进入原始指数尾。sign与fraction部分单独保留，固定码表避免反复学习编码。它是在可压缩部分和回退路径之间组织存储，而不是通过舍弃低概率值变成有损量化。 教学例子：常见指数用短码，遇到罕见指数先写escape再写原8位；即使压缩流满了，余下指数仍原样保存，不能为了达到目标大小就把它们改成零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-74b7ca86cd3c25c0">LCT压缩指数时，罕见符号或stream超预算为什么也不能丢掉？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alct">LCT: Losslessly Compressed Tensors with GPU friendly execution for Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是逐bit可还原，因此罕见指数使用escape加原始符号，流预算耗尽后的剩余项进入原始指数尾。sign与fraction部分单独保留，固定码表避免反复学习编码。它是在可压缩部分和回退路径之间组织存储，而不是通过舍弃低概率值变成有损量化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>常见指数用短码，遇到罕见指数先写escape再写原8位；即使压缩流满了，余下指数仍原样保存，不能为了达到目标大小就把它们改成零。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22179">原论文</a> · <a href="../../../../foundation-models/2610.22179-lct/">实现解读</a> · <a href="#qa-74b7ca86cd3c25c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lct" data-paper-title="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training 基础模型 University of Cambridge 2026-10-15 浮点指数往往比 sign/mantissa 更可压缩，但训练需要反复编码。LCT 将两部分分开，以固定模型预计算短码，运行时中心变换适应量级，循环 stream 在固定预算之外保留原始指数尾。主源 §4、Appendix B/C；不是用通用 zlib 压缩替代算法。 完整链路成本过高，不复现（审查 DONE），不启动探跑；CUDA诊断记录与真实GPU回执保存设备、种子与源码身份。不下载模型或语料。revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，seeds42/43/44。使用公开定义的合成 BF16 位模式：512个元素中的前256个覆盖所有指数，另改变 sign/fraction；固定码表模型不是根据测试输入拟合。16 streams×32-bit预算故意产生 overflow；另以充足预算及其他中心检查还原。  训练与系统效率 无损浮点编码 基础模型 训练预算：数据配比、目标与优化器 LCT 的专用有界指数编码，与直接用 zlib 压缩张量有什么区别？ LCT定义固定码表、最大码长、escape和stream预算及原始overflow尾，适合反复编码的格式约束；通用压缩不会自动实现同样的数据布局。任何方案都需把码表与metadata计入总字节。 示意：payload变小，但加上独立码表和索引后总大小仍可能膨胀。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-95b48be5b7b4f2f3">LCT 的专用有界指数编码，与直接用 zlib 压缩张量有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alct">LCT: Losslessly Compressed Tensors with GPU friendly execution for Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>LCT定义固定码表、最大码长、escape和stream预算及原始overflow尾，适合反复编码的格式约束；通用压缩不会自动实现同样的数据布局。任何方案都需把码表与metadata计入总字节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>payload变小，但加上独立码表和索引后总大小仍可能膨胀。</p>
<p class="ar-learning-sources">依据：背景与主要改动、结果与独立对照；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22179">原论文</a> · <a href="../../../../foundation-models/2610.22179-lct/">实现解读</a> · <a href="#qa-95b48be5b7b4f2f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lct" data-paper-title="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training 基础模型 University of Cambridge 2026-10-15 浮点指数往往比 sign/mantissa 更可压缩，但训练需要反复编码。LCT 将两部分分开，以固定模型预计算短码，运行时中心变换适应量级，循环 stream 在固定预算之外保留原始指数尾。主源 §4、Appendix B/C；不是用通用 zlib 压缩替代算法。 完整链路成本过高，不复现（审查 DONE），不启动探跑；CUDA诊断记录与真实GPU回执保存设备、种子与源码身份。不下载模型或语料。revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，seeds42/43/44。使用公开定义的合成 BF16 位模式：512个元素中的前256个覆盖所有指数，另改变 sign/fraction；固定码表模型不是根据测试输入拟合。16 streams×32-bit预算故意产生 overflow；另以充足预算及其他中心检查还原。  训练与系统效率 无损浮点编码 基础模型 训练预算：数据配比、目标与优化器 LCT 的 round-trip 为什么要比较原始 bits，而不只比较浮点数值？ 有符号零、subnormal、Inf及NaN payload都属于无损格式应保留的信息，普通数值比较可能遗漏或不适用。还需测试全部指数、不同中心和预算溢出路径。 示意：+0与-0数值比较相等，但其符号位不同，逐bit验收才能发现丢失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-549e6e120af7ef04">LCT 的 round-trip 为什么要比较原始 bits，而不只比较浮点数值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alct">LCT: Losslessly Compressed Tensors with GPU friendly execution for Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有符号零、subnormal、Inf及NaN payload都属于无损格式应保留的信息，普通数值比较可能遗漏或不适用。还需测试全部指数、不同中心和预算溢出路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>+0与-0数值比较相等，但其符号位不同，逐bit验收才能发现丢失。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与运行；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22179">原论文</a> · <a href="../../../../foundation-models/2610.22179-lct/">实现解读</a> · <a href="#qa-549e6e120af7ef04">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon-paired-budget" data-paper-title="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark 基础模型 论文未列一作机构 2026-10-15 优化器每步效果更好不等于同时间更好，也不意味着更容易调参。论文在单A100上对齐初始化、数据顺序和开发候选数，分别比较数据、训练时间、冻结调参池三种预算。它不是新的Muon优化公式，主要贡献是谨慎分离比较口径。测试数据在选参和轨迹分析冻结后只评一次。 按可用单卡预算，完整实验成本过高，不复现（审查 DONE）。三种子是协议随机性诊断，不是模型稳定提升。不训练Muon/AdamW、不下载FineWeb/CIFAR。固定合成轨迹revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1，seeds42/43/44；每seed构造可手算的分段线性validation曲线、较慢但等数据更优的替代策略、三个合成配对replication IDs，以及23个固定候选AUC。三种子是协议随机性诊断，不是模型稳定提升。  优化与训练效率 公平预算评测协议 基础模型 训练预算：数据配比、目标与优化器 Muon paired-budget 为什么把数据、训练时间和调参成本分开报告？ 每步质量、每秒质量与找到好参数的难度是不同问题。同一优化器可能在等数据下更好、等时间下更差，协议因此分别对齐这些预算，不把一种优势外推到所有口径。 示意：处理同样token更低loss，但每步慢很多，固定一小时内未必更优。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-muon-paired-budget-6bbbedd2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9a0c27dfaf4180bd">Muon paired-budget 为什么把数据、训练时间和调参成本分开报告？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon-paired-budget">When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列一作机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每步质量、每秒质量与找到好参数的难度是不同问题。同一优化器可能在等数据下更好、等时间下更差，协议因此分别对齐这些预算，不把一种优势外推到所有口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>处理同样token更低loss，但每步慢很多，固定一小时内未必更优。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21555">原论文</a> · <a href="../../../../foundation-models/2610.21555-muon-paired-budget/">实现解读</a> · <a href="#qa-9a0c27dfaf4180bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon-paired-budget" data-paper-title="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark 基础模型 论文未列一作机构 2026-10-15 优化器每步效果更好不等于同时间更好，也不意味着更容易调参。论文在单A100上对齐初始化、数据顺序和开发候选数，分别比较数据、训练时间、冻结调参池三种预算。它不是新的Muon优化公式，主要贡献是谨慎分离比较口径。测试数据在选参和轨迹分析冻结后只评一次。 按可用单卡预算，完整实验成本过高，不复现（审查 DONE）。三种子是协议随机性诊断，不是模型稳定提升。不训练Muon/AdamW、不下载FineWeb/CIFAR。固定合成轨迹revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1，seeds42/43/44；每seed构造可手算的分段线性validation曲线、较慢但等数据更优的替代策略、三个合成配对replication IDs，以及23个固定候选AUC。三种子是协议随机性诊断，不是模型稳定提升。  优化与训练效率 公平预算评测协议 基础模型 训练预算：数据配比、目标与优化器 Muon同样步数下更低loss，为什么仍不足以宣布同算力或同调参成本更优？ 每步耗时、数据吞吐和调参开销可能不同。配对基准固定初始化、数据顺序与候选池，分别按已处理数据、实际训练时间和冻结调参预算比较；参数只在开发阶段选择，测试冻结后读取。相同步数只是一个横轴，不能代替另外两种成本口径。 教学例子：A每步进步更大但耗时翻倍，100步更好不代表十分钟内更好；若又为时间指标单独重挑A的最佳配置，就混入了额外调参优势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-01050f98565ed331">Muon同样步数下更低loss，为什么仍不足以宣布同算力或同调参成本更优？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon-paired-budget">When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列一作机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每步耗时、数据吞吐和调参开销可能不同。配对基准固定初始化、数据顺序与候选池，分别按已处理数据、实际训练时间和冻结调参预算比较；参数只在开发阶段选择，测试冻结后读取。相同步数只是一个横轴，不能代替另外两种成本口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A每步进步更大但耗时翻倍，100步更好不代表十分钟内更好；若又为时间指标单独重挑A的最佳配置，就混入了额外调参优势。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21555">原论文</a> · <a href="../../../../foundation-models/2610.21555-muon-paired-budget/">实现解读</a> · <a href="#qa-01050f98565ed331">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon-paired-budget" data-paper-title="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark 基础模型 论文未列一作机构 2026-10-15 优化器每步效果更好不等于同时间更好，也不意味着更容易调参。论文在单A100上对齐初始化、数据顺序和开发候选数，分别比较数据、训练时间、冻结调参池三种预算。它不是新的Muon优化公式，主要贡献是谨慎分离比较口径。测试数据在选参和轨迹分析冻结后只评一次。 按可用单卡预算，完整实验成本过高，不复现（审查 DONE）。三种子是协议随机性诊断，不是模型稳定提升。不训练Muon/AdamW、不下载FineWeb/CIFAR。固定合成轨迹revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1，seeds42/43/44；每seed构造可手算的分段线性validation曲线、较慢但等数据更优的替代策略、三个合成配对replication IDs，以及23个固定候选AUC。三种子是协议随机性诊断，不是模型稳定提升。  优化与训练效率 公平预算评测协议 基础模型 训练预算：数据配比、目标与优化器 冻结候选池的随机访问 regret，为什么不是前瞻自适应 HPO 的成绩？ 它在预先固定的候选集合上分析随机访问顺序，衡量有限候选预算的损失；自适应HPO会依据前面结果产生或选择新候选。两者的决策信息与时间成本不同。 示意：随机翻看既有23个配置，与运行中根据反馈提出第24个配置，不是同一种搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4682ad997eed076f">冻结候选池的随机访问 regret，为什么不是前瞻自适应 HPO 的成绩？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon-paired-budget">When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列一作机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它在预先固定的候选集合上分析随机访问顺序，衡量有限候选预算的损失；自适应HPO会依据前面结果产生或选择新候选。两者的决策信息与时间成本不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>随机翻看既有23个配置，与运行中根据反馈提出第24个配置，不是同一种搜索。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21555">原论文</a> · <a href="../../../../foundation-models/2610.21555-muon-paired-budget/">实现解读</a> · <a href="#qa-4682ad997eed076f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon-paired-budget" data-paper-title="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark 基础模型 论文未列一作机构 2026-10-15 优化器每步效果更好不等于同时间更好，也不意味着更容易调参。论文在单A100上对齐初始化、数据顺序和开发候选数，分别比较数据、训练时间、冻结调参池三种预算。它不是新的Muon优化公式，主要贡献是谨慎分离比较口径。测试数据在选参和轨迹分析冻结后只评一次。 按可用单卡预算，完整实验成本过高，不复现（审查 DONE）。三种子是协议随机性诊断，不是模型稳定提升。不训练Muon/AdamW、不下载FineWeb/CIFAR。固定合成轨迹revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1，seeds42/43/44；每seed构造可手算的分段线性validation曲线、较慢但等数据更优的替代策略、三个合成配对replication IDs，以及23个固定候选AUC。三种子是协议随机性诊断，不是模型稳定提升。  优化与训练效率 公平预算评测协议 基础模型 训练预算：数据配比、目标与优化器 做配对 bootstrap 时，为什么两种优化器必须抽同一组 seed 索引？ 配对比较依赖同seed的初始化和数据顺序对应，错配会破坏相关结构。AUC还必须在共同测量域积分，配置先按开发validation冻结，不能为时间口径重新挑最优配置。 示意：抽到seed42时，两种优化器都取seed42的轨迹，而非另一边随机取seed44。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d0920c3cb6a09d74">做配对 bootstrap 时，为什么两种优化器必须抽同一组 seed 索引？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon-paired-budget">When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列一作机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>配对比较依赖同seed的初始化和数据顺序对应，错配会破坏相关结构。AUC还必须在共同测量域积分，配置先按开发validation冻结，不能为时间口径重新挑最优配置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>抽到seed42时，两种优化器都取seed42的轨迹，而非另一边随机取seed44。</p>
<p class="ar-learning-sources">依据：核心公式、结果与独立对照；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21555">原论文</a> · <a href="../../../../foundation-models/2610.21555-muon-paired-budget/">实现解读</a> · <a href="#qa-d0920c3cb6a09d74">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smrc-pmrc" data-paper-title="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon 基础模型 Nanjing University / Alibaba Token Hub 2026-10-14 低秩优化器只存投影后的动量，能减少持久状态；但梯度主奇异方向可能被噪声占据，直接丢掉子空间外分量会遗漏有效下降方向。本文让低秩动量负责投影内更新，原始梯度的正交残差负责其余方向，不额外保存一个全尺寸残差状态。SMRC 使用 EMA 动量，PMRC 对低维动量取矩阵符号；二者不能简单替换成同一个“投影 SGD”。 完整实验：成本过高，不复现（审查 DONE）。L1 组件诊断。Fidelity: 核心机制复现；L1 组件诊断。这里交付可直接更新真实参数的 PyTorch 优化器和有界验证入口，不代表完整 LLM 预训练、SFT 或论文大规模效果已复现。完整实验：成本过高，不复现（审查 DONE）。本地对照口径：基线为全空间 EMA-SGD、精确矩阵符号 Muon 和 AdamW，实验组为 SMRC、理论 PMRC、实用 PMRC；参数初始化、梯度噪声/输入与更新次数一致；固定小预算，仅作机制诊断，跨算法下游效果相对提升不适用。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 SMRC/PMRC 为什么不能只保留低秩投影里的梯度？ 主奇异子空间可能被噪声占据，子空间外仍有有效下降方向。方法以低维动量处理投影内部分，每步从真实梯度计算正交残差补回，不持久保存全尺寸残差动量。 示意：当前投影关注一个大方向，另一个较小但有用的方向不应因此永远没有更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-smrc-pmrc-96d2a34c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0d48cc4c8b783203">SMRC/PMRC 为什么不能只保留低秩投影里的梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmrc-pmrc">Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University / Alibaba Token Hub</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主奇异子空间可能被噪声占据，子空间外仍有有效下降方向。方法以低维动量处理投影内部分，每步从真实梯度计算正交残差补回，不持久保存全尺寸残差动量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前投影关注一个大方向，另一个较小但有用的方向不应因此永远没有更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19844">原论文</a> · <a href="../../../../reproductions/2610.19844-smrc-pmrc/">实现解读</a> · <a href="#qa-0d48cc4c8b783203">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smrc-pmrc" data-paper-title="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon 基础模型 Nanjing University / Alibaba Token Hub 2026-10-14 低秩优化器只存投影后的动量，能减少持久状态；但梯度主奇异方向可能被噪声占据，直接丢掉子空间外分量会遗漏有效下降方向。本文让低秩动量负责投影内更新，原始梯度的正交残差负责其余方向，不额外保存一个全尺寸残差状态。SMRC 使用 EMA 动量，PMRC 对低维动量取矩阵符号；二者不能简单替换成同一个“投影 SGD”。 完整实验：成本过高，不复现（审查 DONE）。L1 组件诊断。Fidelity: 核心机制复现；L1 组件诊断。这里交付可直接更新真实参数的 PyTorch 优化器和有界验证入口，不代表完整 LLM 预训练、SFT 或论文大规模效果已复现。完整实验：成本过高，不复现（审查 DONE）。本地对照口径：基线为全空间 EMA-SGD、精确矩阵符号 Muon 和 AdamW，实验组为 SMRC、理论 PMRC、实用 PMRC；参数初始化、梯度噪声/输入与更新次数一致；固定小预算，仅作机制诊断，跨算法下游效果相对提升不适用。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 SMRC/PMRC只存低秩动量，怎样补上子空间外的有效梯度？ 投影内部分由低维动量更新，当前原始梯度的正交残差提供其余方向，不额外持久保存全尺寸残差状态。SMRC对低维动量作EMA，PMRC还改变矩阵方向处理；换基时二者规则也不同。节省动量存储不意味着可以把残差删掉，或把两种方法都简化成同一个投影SGD。 教学例子：主要子空间抓住两个高能方向，但较小的第三方向仍有下降信息；用当前梯度残差补这部分，同时无需为它再保留一整张长期动量矩阵。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-00d2545fa87f1553">SMRC/PMRC只存低秩动量，怎样补上子空间外的有效梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmrc-pmrc">Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University / Alibaba Token Hub</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投影内部分由低维动量更新，当前原始梯度的正交残差提供其余方向，不额外持久保存全尺寸残差状态。SMRC对低维动量作EMA，PMRC还改变矩阵方向处理；换基时二者规则也不同。节省动量存储不意味着可以把残差删掉，或把两种方法都简化成同一个投影SGD。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>主要子空间抓住两个高能方向，但较小的第三方向仍有下降信息；用当前梯度残差补这部分，同时无需为它再保留一整张长期动量矩阵。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19844">原论文</a> · <a href="../../../../reproductions/2610.19844-smrc-pmrc/">实现解读</a> · <a href="#qa-00d2545fa87f1553">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smrc-pmrc" data-paper-title="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon 基础模型 Nanjing University / Alibaba Token Hub 2026-10-14 低秩优化器只存投影后的动量，能减少持久状态；但梯度主奇异方向可能被噪声占据，直接丢掉子空间外分量会遗漏有效下降方向。本文让低秩动量负责投影内更新，原始梯度的正交残差负责其余方向，不额外保存一个全尺寸残差状态。SMRC 使用 EMA 动量，PMRC 对低维动量取矩阵符号；二者不能简单替换成同一个“投影 SGD”。 完整实验：成本过高，不复现（审查 DONE）。L1 组件诊断。Fidelity: 核心机制复现；L1 组件诊断。这里交付可直接更新真实参数的 PyTorch 优化器和有界验证入口，不代表完整 LLM 预训练、SFT 或论文大规模效果已复现。完整实验：成本过高，不复现（审查 DONE）。本地对照口径：基线为全空间 EMA-SGD、精确矩阵符号 Muon 和 AdamW，实验组为 SMRC、理论 PMRC、实用 PMRC；参数初始化、梯度噪声/输入与更新次数一致；固定小预算，仅作机制诊断，跨算法下游效果相对提升不适用。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 SMRC 与 PMRC 都存低维动量，为什么仍不是同一个优化器？ SMRC直接使用EMA动量映回；PMRC对低维动量取矩阵符号。stage边界也不同：SMRC有参数修正，PMRC理论算法没有同样平移，不能以一个投影SGD函数代替两者。 示意：相同低维M经过原值映回与msign后映回，通常产生不同更新方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-52517eeea8c6108e">SMRC 与 PMRC 都存低维动量，为什么仍不是同一个优化器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmrc-pmrc">Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University / Alibaba Token Hub</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SMRC直接使用EMA动量映回；PMRC对低维动量取矩阵符号。stage边界也不同：SMRC有参数修正，PMRC理论算法没有同样平移，不能以一个投影SGD函数代替两者。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相同低维M经过原值映回与msign后映回，通常产生不同更新方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19844">原论文</a> · <a href="../../../../reproductions/2610.19844-smrc-pmrc/">实现解读</a> · <a href="#qa-52517eeea8c6108e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smrc-pmrc" data-paper-title="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon 基础模型 Nanjing University / Alibaba Token Hub 2026-10-14 低秩优化器只存投影后的动量，能减少持久状态；但梯度主奇异方向可能被噪声占据，直接丢掉子空间外分量会遗漏有效下降方向。本文让低秩动量负责投影内更新，原始梯度的正交残差负责其余方向，不额外保存一个全尺寸残差状态。SMRC 使用 EMA 动量，PMRC 对低维动量取矩阵符号；二者不能简单替换成同一个“投影 SGD”。 完整实验：成本过高，不复现（审查 DONE）。L1 组件诊断。Fidelity: 核心机制复现；L1 组件诊断。这里交付可直接更新真实参数的 PyTorch 优化器和有界验证入口，不代表完整 LLM 预训练、SFT 或论文大规模效果已复现。完整实验：成本过高，不复现（审查 DONE）。本地对照口径：基线为全空间 EMA-SGD、精确矩阵符号 Muon 和 AdamW，实验组为 SMRC、理论 PMRC、实用 PMRC；参数初始化、梯度噪声/输入与更新次数一致；固定小预算，仅作机制诊断，跨算法下游效果相对提升不适用。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 SMRC 刷新基之前，为什么必须先修正参数并重新做 backward？ 文档stage末先修正真实参数、清零动量，下次forward/backward在新参数上产生新梯度后才刷新基。沿用修正前旧梯度会错配状态；本地beta还是新梯度系数，需避免与常见API相反。 示意：stage边界后参数已改变，不能拿改变前那次梯度当作新起点的梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-078fd6cd71d93be1">SMRC 刷新基之前，为什么必须先修正参数并重新做 backward？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmrc-pmrc">Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University / Alibaba Token Hub</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档stage末先修正真实参数、清零动量，下次forward/backward在新参数上产生新梯度后才刷新基。沿用修正前旧梯度会错配状态；本地beta还是新梯度系数，需避免与常见API相反。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>stage边界后参数已改变，不能拿改变前那次梯度当作新起点的梯度。</p>
<p class="ar-learning-sources">依据：核心公式、已实现的组件；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19844">原论文</a> · <a href="../../../../reproductions/2610.19844-smrc-pmrc/">实现解读</a> · <a href="#qa-078fd6cd71d93be1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adamw4bit" data-paper-title="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization 基础模型 University of California, Berkeley / Nubank 2026-10-08 AdamW 的量化误差会进入后续矩递推。ZIP-SR 在预条件器空间随机舍入第二矩；ZE-EDEN 排除零码点并校准块尺度。两者使用 NF4 第一矩，训练末尾 10% 对 LM head 第一矩随机舍入。原文 真实训练使用公开数据，但本批产物按 L1 有界机制诊断登记；WikiText-2 官方 train/valid/test；字节 tokenizer，训练前 100 万字节，验证和测试仅评估固定 16 个 64-token 片段。相同初始化、批次、200 步、学习率和模型结构；所有方案统一使用独立 LM head。仅以验证集选方案，选定后才打开 test。  训练优化与稳定性 低精度训练 基础模型 训练预算：数据配比、目标与优化器 为什么 AdamW 的状态量化会影响后续很多步，而不只影响当前存储？ 第一、第二矩会跨步递推，保存时的量化误差在下次解码后继续参与优化。4-bit方案因此不仅要压缩字节，还要控制误差如何影响预条件器和后续参数更新。 示意：第二矩被持续舍入偏小，可能连续多步放大有效学习率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-adamw4bit-715c8ec7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0b06e014d4785862">为什么 AdamW 的状态量化会影响后续很多步，而不只影响当前存储？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadamw4bit">Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley / Nubank</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第一、第二矩会跨步递推，保存时的量化误差在下次解码后继续参与优化。4-bit方案因此不仅要压缩字节，还要控制误差如何影响预条件器和后续参数更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第二矩被持续舍入偏小，可能连续多步放大有效学习率。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12444">原论文</a> · <a href="../../../../foundation-models/2610.12444-adamw4bit/">实现解读</a> · <a href="#qa-0b06e014d4785862">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adamw4bit" data-paper-title="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization 基础模型 University of California, Berkeley / Nubank 2026-10-08 AdamW 的量化误差会进入后续矩递推。ZIP-SR 在预条件器空间随机舍入第二矩；ZE-EDEN 排除零码点并校准块尺度。两者使用 NF4 第一矩，训练末尾 10% 对 LM head 第一矩随机舍入。原文 真实训练使用公开数据，但本批产物按 L1 有界机制诊断登记；WikiText-2 官方 train/valid/test；字节 tokenizer，训练前 100 万字节，验证和测试仅评估固定 16 个 64-token 片段。相同初始化、批次、200 步、学习率和模型结构；所有方案统一使用独立 LM head。仅以验证集选方案，选定后才打开 test。  训练优化与稳定性 低精度训练 基础模型 训练预算：数据配比、目标与优化器 4-bit AdamW为什么要在预条件器空间控制第二矩舍入，而不只让第二矩数值接近？ 第二矩经过偏差校正、开平方和取倒数后才影响更新，原数值上相近的误差在这个非线性映射后可能不等价。ZIP-SR据预条件器值决定随机舍入概率，ZE-EDEN则处理码点与尺度；状态误差还会进入后续递推。当前工作矩先用于参数更新，再量化存储，顺序也属于机制。 教学例子：两个很小的第二矩数值只有一点差别，取倒数平方根后却可能明显改变步长；应保护实际乘到梯度上的尺度，而不只比较压缩前后的均方误差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c8a13b370455cc00">4-bit AdamW为什么要在预条件器空间控制第二矩舍入，而不只让第二矩数值接近？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadamw4bit">Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley / Nubank</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第二矩经过偏差校正、开平方和取倒数后才影响更新，原数值上相近的误差在这个非线性映射后可能不等价。ZIP-SR据预条件器值决定随机舍入概率，ZE-EDEN则处理码点与尺度；状态误差还会进入后续递推。当前工作矩先用于参数更新，再量化存储，顺序也属于机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个很小的第二矩数值只有一点差别，取倒数平方根后却可能明显改变步长；应保护实际乘到梯度上的尺度，而不只比较压缩前后的均方误差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12444">原论文</a> · <a href="../../../../foundation-models/2610.12444-adamw4bit/">实现解读</a> · <a href="#qa-c8a13b370455cc00">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adamw4bit" data-paper-title="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization 基础模型 University of California, Berkeley / Nubank 2026-10-08 AdamW 的量化误差会进入后续矩递推。ZIP-SR 在预条件器空间随机舍入第二矩；ZE-EDEN 排除零码点并校准块尺度。两者使用 NF4 第一矩，训练末尾 10% 对 LM head 第一矩随机舍入。原文 真实训练使用公开数据，但本批产物按 L1 有界机制诊断登记；WikiText-2 官方 train/valid/test；字节 tokenizer，训练前 100 万字节，验证和测试仅评估固定 16 个 64-token 片段。相同初始化、批次、200 步、学习率和模型结构；所有方案统一使用独立 LM head。仅以验证集选方案，选定后才打开 test。  训练优化与稳定性 低精度训练 基础模型 训练预算：数据配比、目标与优化器 ZIP-SR 与 ZE-EDEN 在第二矩存储上采取了什么不同策略？ ZIP-SR在预条件器空间做随机舍入；ZE-EDEN排除零码点并校准块尺度。二者都不是把任意数值直接四舍五入到同一个4-bit表，比较还需报告损失与实际持久状态字节。 示意：相邻码点间如何随机选取，与重新调块尺度避免零码点，是不同的误差控制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a2ee36b4cc02d185">ZIP-SR 与 ZE-EDEN 在第二矩存储上采取了什么不同策略？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadamw4bit">Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley / Nubank</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ZIP-SR在预条件器空间做随机舍入；ZE-EDEN排除零码点并校准块尺度。二者都不是把任意数值直接四舍五入到同一个4-bit表，比较还需报告损失与实际持久状态字节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相邻码点间如何随机选取，与重新调块尺度避免零码点，是不同的误差控制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12444">原论文</a> · <a href="../../../../foundation-models/2610.12444-adamw4bit/">实现解读</a> · <a href="#qa-a2ee36b4cc02d185">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adamw4bit" data-paper-title="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization 基础模型 University of California, Berkeley / Nubank 2026-10-08 AdamW 的量化误差会进入后续矩递推。ZIP-SR 在预条件器空间随机舍入第二矩；ZE-EDEN 排除零码点并校准块尺度。两者使用 NF4 第一矩，训练末尾 10% 对 LM head 第一矩随机舍入。原文 真实训练使用公开数据，但本批产物按 L1 有界机制诊断登记；WikiText-2 官方 train/valid/test；字节 tokenizer，训练前 100 万字节，验证和测试仅评估固定 16 个 64-token 片段。相同初始化、批次、200 步、学习率和模型结构；所有方案统一使用独立 LM head。仅以验证集选方案，选定后才打开 test。  训练优化与稳定性 低精度训练 基础模型 训练预算：数据配比、目标与优化器 4-bit AdamW 当前步应该先量化工作矩，再用量化值更新参数吗？ 文档先由解码旧状态和当前梯度形成工作矩，用未量化工作矩更新参数，再量化并打包作为持久状态。顺序反过来会把本次量化误差提前引入当前更新，改变算法。 示意：工作矩算出v后先得到本步预条件更新，再把v压缩供下一步使用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8b106936b90fd09d">4-bit AdamW 当前步应该先量化工作矩，再用量化值更新参数吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadamw4bit">Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley / Nubank</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档先由解码旧状态和当前梯度形成工作矩，用未量化工作矩更新参数，再量化并打包作为持久状态。顺序反过来会把本次量化误差提前引入当前更新，改变算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工作矩算出v后先得到本步预条件更新，再把v压缩供下一步使用。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12444">原论文</a> · <a href="../../../../foundation-models/2610.12444-adamw4bit/">实现解读</a> · <a href="#qa-8b106936b90fd09d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:af-muon" data-paper-title="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models 基础模型 原文首页未列第一作者机构 2026-10-01 矩阵继续用 Muon 谱范数方向，稀疏输入查表与稠密输出分类器共享的词表采用 support-aware 有限帽 LMO，一维参数用 RMS 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行词表 support/cap 方向；未完成论文规模预训练。执行词表 support/cap 方向；未完成论文规模预训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  优化器 Muon 显存效率 基础模型 训练预算：数据配比、目标与优化器 AF-Muon 为什么要为模型里的不同参数类型设置不同更新？ 隐藏矩阵、共享词表与一维参数的几何和梯度支持不同。文档分别使用Muon矩阵方向、词表support-aware有限帽方向及一维RMS更新，避免把所有参数都当普通稠密矩阵。 示意：只被少数输入词访问的embedding行，与一个每步都参与计算的hidden矩阵不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-af-muon-b7027d08" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-31b949c759ccfa99">AF-Muon 为什么要为模型里的不同参数类型设置不同更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaf-muon">AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>隐藏矩阵、共享词表与一维参数的几何和梯度支持不同。文档分别使用Muon矩阵方向、词表support-aware有限帽方向及一维RMS更新，避免把所有参数都当普通稠密矩阵。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只被少数输入词访问的embedding行，与一个每步都参与计算的hidden矩阵不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01395">原论文</a> · <a href="../../../../foundation-models/2610.01395-af-muon/">实现解读</a> · <a href="#qa-31b949c759ccfa99">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:af-muon" data-paper-title="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models 基础模型 原文首页未列第一作者机构 2026-10-01 矩阵继续用 Muon 谱范数方向，稀疏输入查表与稠密输出分类器共享的词表采用 support-aware 有限帽 LMO，一维参数用 RMS 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行词表 support/cap 方向；未完成论文规模预训练。执行词表 support/cap 方向；未完成论文规模预训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  优化器 Muon 显存效率 基础模型 训练预算：数据配比、目标与优化器 AF-Muon为何不能把tied embedding当普通隐藏矩阵统一做Muon更新？ 共享词表同时承担稀疏输入查表与稠密输出分类，两种梯度结构并不相同。AF-Muon对隐藏矩阵保留Muon式谱方向，对共享词表使用support-aware有限帽方向，对一维参数另用RMS更新。不能仅按输入中出现的词判断支持集，因为输出分类路径也可能给许多词表行提供梯度。 教学例子：一个词没在输入中出现，却作为输出候选受到分类损失影响；若只更新输入命中的行，就会漏掉共享输出头的有效梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bc1646d03073e9ba">AF-Muon为何不能把tied embedding当普通隐藏矩阵统一做Muon更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaf-muon">AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享词表同时承担稀疏输入查表与稠密输出分类，两种梯度结构并不相同。AF-Muon对隐藏矩阵保留Muon式谱方向，对共享词表使用support-aware有限帽方向，对一维参数另用RMS更新。不能仅按输入中出现的词判断支持集，因为输出分类路径也可能给许多词表行提供梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个词没在输入中出现，却作为输出候选受到分类损失影响；若只更新输入命中的行，就会漏掉共享输出头的有效梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01395">原论文</a> · <a href="../../../../foundation-models/2610.01395-af-muon/">实现解读</a> · <a href="#qa-bc1646d03073e9ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:af-muon" data-paper-title="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models 基础模型 原文首页未列第一作者机构 2026-10-01 矩阵继续用 Muon 谱范数方向，稀疏输入查表与稠密输出分类器共享的词表采用 support-aware 有限帽 LMO，一维参数用 RMS 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行词表 support/cap 方向；未完成论文规模预训练。执行词表 support/cap 方向；未完成论文规模预训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  优化器 Muon 显存效率 基础模型 训练预算：数据配比、目标与优化器 support-aware 有限帽方向，与把每个词表行都归一化成同样长度有什么区别？ 它保留零梯度支持边界，并以cap限制行方向幅度；小梯度不必被强行放大到统一长度。简单逐行单位归一化会改变这一幅度控制，也可能给无支持行带来数值问题。 示意：梯度范数小于cap时，不能仅为了单位化就把它放大成与大梯度行相同长度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-91844685fea05438">support-aware 有限帽方向，与把每个词表行都归一化成同样长度有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaf-muon">AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它保留零梯度支持边界，并以cap限制行方向幅度；小梯度不必被强行放大到统一长度。简单逐行单位归一化会改变这一幅度控制，也可能给无支持行带来数值问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>梯度范数小于cap时，不能仅为了单位化就把它放大成与大梯度行相同长度。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01395">原论文</a> · <a href="../../../../foundation-models/2610.01395-af-muon/">实现解读</a> · <a href="#qa-91844685fea05438">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:af-muon" data-paper-title="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models 基础模型 原文首页未列第一作者机构 2026-10-01 矩阵继续用 Muon 谱范数方向，稀疏输入查表与稠密输出分类器共享的词表采用 support-aware 有限帽 LMO，一维参数用 RMS 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行词表 support/cap 方向；未完成论文规模预训练。执行词表 support/cap 方向；未完成论文规模预训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  优化器 Muon 显存效率 基础模型 训练预算：数据配比、目标与优化器 AF-Muon 在零梯度词表行上，怎样避免归一化产生 NaN？ 公式中1[g_i≠0]对应显式支持分支：零梯度行方向应为0，不能先算g/‖g‖再指望乘0清掉NaN。当前记录验证的是support/cap方向，未完成论文规模预训练。 示意：本批次未出现也没有输出梯度的一行，应保持零更新方向，而不是出现0/0。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-62d1acd180b32cf2">AF-Muon 在零梯度词表行上，怎样避免归一化产生 NaN？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaf-muon">AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式中1[g_i≠0]对应显式支持分支：零梯度行方向应为0，不能先算g/‖g‖再指望乘0清掉NaN。当前记录验证的是support/cap方向，未完成论文规模预训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>本批次未出现也没有输出梯度的一行，应保持零更新方向，而不是出现0/0。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01395">原论文</a> · <a href="../../../../foundation-models/2610.01395-af-muon/">实现解读</a> · <a href="#qa-62d1acd180b32cf2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:taco-optimizer" data-paper-title="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning 基础模型 University of Central Florida 2026-10-01 每个二维权重列只保留绝对值最大的梯度分量及符号，形成 column-wise one-sparse steepest direction；低精度列状态替代逐参数 dense optimizer state。 未复现 13B/32B 全参微调或论文精度。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  优化器 显存效率 全参微调 基础模型 训练预算：数据配比、目标与优化器 TACO 为什么把每列更新压到一个梯度位置？ 它为二维权重的每列选择绝对梯度最大的位置及符号，形成column-wise one-sparse方向，以列级低精度状态替代逐参数dense优化器状态。更新结构与普通稠密梯度下降不同。 示意：一列有很多非零梯度，本步只保留绝对值最大的那个位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-taco-optimizer-aae79ac1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0322355f6e4728e8">TACO 为什么把每列更新压到一个梯度位置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ataco-optimizer">TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Central Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它为二维权重的每列选择绝对梯度最大的位置及符号，形成column-wise one-sparse方向，以列级低精度状态替代逐参数dense优化器状态。更新结构与普通稠密梯度下降不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一列有很多非零梯度，本步只保留绝对值最大的那个位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02199">原论文</a> · <a href="../../../../foundation-models/2610.02199-taco-optimizer/">实现解读</a> · <a href="#qa-0322355f6e4728e8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:taco-optimizer" data-paper-title="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning 基础模型 University of Central Florida 2026-10-01 每个二维权重列只保留绝对值最大的梯度分量及符号，形成 column-wise one-sparse steepest direction；低精度列状态替代逐参数 dense optimizer state。 未复现 13B/32B 全参微调或论文精度。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  优化器 显存效率 全参微调 基础模型 训练预算：数据配比、目标与优化器 TACO每列只保留一个梯度位置，为什么不是普通的逐元素sign更新？ 它先在每个二维权重列中找绝对值最大的分量，只保留该位置的符号，其余位置更新为零。这样得到列级one-sparse方向，并配合低精度列状态减少优化器存储。逐元素sign则会更新所有非零梯度位置，既不是同一方向，也不具有相同稀疏结构。 教学例子：一列梯度为0.2、负0.9、0.4时，该列只在第二行给负方向；普通sign会同时给出正、负、正三个更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f73d70ba75b1e7db">TACO每列只保留一个梯度位置，为什么不是普通的逐元素sign更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ataco-optimizer">TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Central Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它先在每个二维权重列中找绝对值最大的分量，只保留该位置的符号，其余位置更新为零。这样得到列级one-sparse方向，并配合低精度列状态减少优化器存储。逐元素sign则会更新所有非零梯度位置，既不是同一方向，也不具有相同稀疏结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一列梯度为0.2、负0.9、0.4时，该列只在第二行给负方向；普通sign会同时给出正、负、正三个更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02199">原论文</a> · <a href="../../../../foundation-models/2610.02199-taco-optimizer/">实现解读</a> · <a href="#qa-f73d70ba75b1e7db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:taco-optimizer" data-paper-title="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning 基础模型 University of Central Florida 2026-10-01 每个二维权重列只保留绝对值最大的梯度分量及符号，形成 column-wise one-sparse steepest direction；低精度列状态替代逐参数 dense optimizer state。 未复现 13B/32B 全参微调或论文精度。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  优化器 显存效率 全参微调 基础模型 训练预算：数据配比、目标与优化器 TACO 的一稀疏列方向，与逐元素 signSGD 保留了什么不同信息？ signSGD可在一列的所有非零位置更新；TACO先做列内绝对值最大选择，只在选中行保留符号。两者都可能使用符号，但支持集稀疏结构并不相同。 示意：列梯度为[1,-4,2]，逐元素sign有三项，TACO方向只在第二项为-1。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2cbbc3aaef1647ae">TACO 的一稀疏列方向，与逐元素 signSGD 保留了什么不同信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ataco-optimizer">TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Central Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>signSGD可在一列的所有非零位置更新；TACO先做列内绝对值最大选择，只在选中行保留符号。两者都可能使用符号，但支持集稀疏结构并不相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>列梯度为[1,-4,2]，逐元素sign有三项，TACO方向只在第二项为-1。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02199">原论文</a> · <a href="../../../../foundation-models/2610.02199-taco-optimizer/">实现解读</a> · <a href="#qa-2cbbc3aaef1647ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:taco-optimizer" data-paper-title="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning 基础模型 University of Central Florida 2026-10-01 每个二维权重列只保留绝对值最大的梯度分量及符号，形成 column-wise one-sparse steepest direction；低精度列状态替代逐参数 dense optimizer state。 未复现 13B/32B 全参微调或论文精度。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  优化器 显存效率 全参微调 基础模型 训练预算：数据配比、目标与优化器 TACO 的 argmax 选择若误写成沿列轴，会发生什么？ 定义要求对每一列在行索引中取最大绝对值；轴写反会变成每行保留一项，改变优化几何。还需核对未选位置为0与低精度列momentum，而非只检查更新张量shape。 示意：一个3×5权重应每列最多一个保留位置，不是每行一个。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eec147661cf42971">TACO 的 argmax 选择若误写成沿列轴，会发生什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ataco-optimizer">TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Central Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>定义要求对每一列在行索引中取最大绝对值；轴写反会变成每行保留一项，改变优化几何。还需核对未选位置为0与低精度列momentum，而非只检查更新张量shape。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个3×5权重应每列最多一个保留位置，不是每行一个。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02199">原论文</a> · <a href="../../../../foundation-models/2610.02199-taco-optimizer/">实现解读</a> · <a href="#qa-eec147661cf42971">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tess" data-paper-title="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic) 基础模型 Nanyang Technological University 2026-10-01 先分别训练仅看训练集的模型和加入验证集指导的模型，以两者逐样本损失差构造价值伪标签；再用 pointwise value matching 训练数据 selector。避免直接选择目标的病态优化，并让小规模教师产生的选样规则迁移到更大的未见数据池。 L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；没有声称复现大模型数据选择收益。本地二维合成分类特征代替论文语言模型和指令样本特征；只验证顺序训练、伪标签和 selector 学习。完整 LLM 数据池评分、重训练及质量收益尚未验证，不作为正式 Evolve 数据选择算子。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 生成互不重用的 64 个训练、32 个验证、48 个池样本；两分类器各训练 60 步、selector 120 步，三 seed。  预训练与数据 元网络数据选择 基础模型 训练预算：数据配比、目标与优化器 TESS 为什么把“哪些训练样本有价值”变成一个可学习预测任务？ 它先用训练集模型与验证指导模型的逐样本损失差构造价值伪标签，再训练selector对独立候选池打分。这样把昂贵的价值估计转成可迁移的pointwise预测，而非直接在大池上反复试训。 示意：小规模教师产生一批价值标签，再让selector为未参与教师训练的候选样本估值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-tess-5d7b0b3c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c02202de53c5a68f">TESS 为什么把“哪些训练样本有价值”变成一个可学习预测任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atess">TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它先用训练集模型与验证指导模型的逐样本损失差构造价值伪标签，再训练selector对独立候选池打分。这样把昂贵的价值估计转成可迁移的pointwise预测，而非直接在大池上反复试训。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>小规模教师产生一批价值标签，再让selector为未参与教师训练的候选样本估值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02092">原论文</a> · <a href="../../../../foundation-models/2610.02092-tess/">实现解读</a> · <a href="#qa-c02202de53c5a68f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tess" data-paper-title="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic) 基础模型 Nanyang Technological University 2026-10-01 先分别训练仅看训练集的模型和加入验证集指导的模型，以两者逐样本损失差构造价值伪标签；再用 pointwise value matching 训练数据 selector。避免直接选择目标的病态优化，并让小规模教师产生的选样规则迁移到更大的未见数据池。 L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；没有声称复现大模型数据选择收益。本地二维合成分类特征代替论文语言模型和指令样本特征；只验证顺序训练、伪标签和 selector 学习。完整 LLM 数据池评分、重训练及质量收益尚未验证，不作为正式 Evolve 数据选择算子。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 生成互不重用的 64 个训练、32 个验证、48 个池样本；两分类器各训练 60 步、selector 120 步，三 seed。  预训练与数据 元网络数据选择 基础模型 训练预算：数据配比、目标与优化器 TESS为什么先用两模型损失差作伪标签，再训练selector，而不直接优化选择结果？ 一份模型只看训练数据，另一份得到验证目标指导；同初始化下的逐样本损失差提供价值信号，再用pointwise匹配训练可迁移selector。两阶段设计把价值估计与选择器学习分开，避免某些直接选择目标的病态优化。验证信息用于开发指导，不能把最终test偷偷当作这份指导数据。 教学例子：同一个样本在普通模型与验证指导模型上的损失变化不同，可用来学习哪些样本更贴近目标；上线选择新数据时则由selector预测，而非逐样本读取未来测试成绩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b2d1ae7150fa0a51">TESS为什么先用两模型损失差作伪标签，再训练selector，而不直接优化选择结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atess">TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一份模型只看训练数据，另一份得到验证目标指导；同初始化下的逐样本损失差提供价值信号，再用pointwise匹配训练可迁移selector。两阶段设计把价值估计与选择器学习分开，避免某些直接选择目标的病态优化。验证信息用于开发指导，不能把最终test偷偷当作这份指导数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一个样本在普通模型与验证指导模型上的损失变化不同，可用来学习哪些样本更贴近目标；上线选择新数据时则由selector预测，而非逐样本读取未来测试成绩。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02092">原论文</a> · <a href="../../../../foundation-models/2610.02092-tess/">实现解读</a> · <a href="#qa-b2d1ae7150fa0a51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tess" data-paper-title="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic) 基础模型 Nanyang Technological University 2026-10-01 先分别训练仅看训练集的模型和加入验证集指导的模型，以两者逐样本损失差构造价值伪标签；再用 pointwise value matching 训练数据 selector。避免直接选择目标的病态优化，并让小规模教师产生的选样规则迁移到更大的未见数据池。 L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；没有声称复现大模型数据选择收益。本地二维合成分类特征代替论文语言模型和指令样本特征；只验证顺序训练、伪标签和 selector 学习。完整 LLM 数据池评分、重训练及质量收益尚未验证，不作为正式 Evolve 数据选择算子。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 生成互不重用的 64 个训练、32 个验证、48 个池样本；两分类器各训练 60 步、selector 120 步，三 seed。  预训练与数据 元网络数据选择 基础模型 训练预算：数据配比、目标与优化器 TESS 的损失差伪标签，与只选当前模型 loss 最大的样本有什么区别？ 损失差比较两个同起点模型，尝试捕捉验证指导带来的变化；原始高loss只表示当前难度，未必意味着对目标任务有价值。两者的选择信号不能直接互换。 示意：一条噪声样本可能一直很难，但验证指导并未让它变得更有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e39e791601a4e3e3">TESS 的损失差伪标签，与只选当前模型 loss 最大的样本有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atess">TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>损失差比较两个同起点模型，尝试捕捉验证指导带来的变化；原始高loss只表示当前难度，未必意味着对目标任务有价值。两者的选择信号不能直接互换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条噪声样本可能一直很难，但验证指导并未让它变得更有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02092">原论文</a> · <a href="../../../../foundation-models/2610.02092-tess/">实现解读</a> · <a href="#qa-e39e791601a4e3e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tess" data-paper-title="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic) 基础模型 Nanyang Technological University 2026-10-01 先分别训练仅看训练集的模型和加入验证集指导的模型，以两者逐样本损失差构造价值伪标签；再用 pointwise value matching 训练数据 selector。避免直接选择目标的病态优化，并让小规模教师产生的选样规则迁移到更大的未见数据池。 L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；没有声称复现大模型数据选择收益。本地二维合成分类特征代替论文语言模型和指令样本特征；只验证顺序训练、伪标签和 selector 学习。完整 LLM 数据池评分、重训练及质量收益尚未验证，不作为正式 Evolve 数据选择算子。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 生成互不重用的 64 个训练、32 个验证、48 个池样本；两分类器各训练 60 步、selector 120 步，三 seed。  预训练与数据 元网络数据选择 基础模型 训练预算：数据配比、目标与优化器 TESS 的 Δ_i 可以一边拟合 selector 一边反传回 U/W 吗？ 文档要求stop-gradient伪标签，并从相同初始权重顺序训练U/W；selector只拟合保存的损失差。分数可为负，不能未经转换就当采样概率，也不能把test冒充validation。 示意：一个样本价值差为负时，应先保留该监督含义，而非偷偷clamp成0。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-190651bcfe1a3a18">TESS 的 Δ_i 可以一边拟合 selector 一边反传回 U/W 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atess">TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档要求stop-gradient伪标签，并从相同初始权重顺序训练U/W；selector只拟合保存的损失差。分数可为负，不能未经转换就当采样概率，也不能把test冒充validation。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个样本价值差为负时，应先保留该监督含义，而非偷偷clamp成0。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02092">原论文</a> · <a href="../../../../foundation-models/2610.02092-tess/">实现解读</a> · <a href="#qa-190651bcfe1a3a18">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-1b-audit" data-paper-title="OPEN-1B: A Fully Auditable Training Run" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OPEN-1B: A Fully Auditable Training Run 基础模型 Gensyn 2026-09-15 固定 kernel reduction、数据批次与集体通信顺序，并用逐步状态哈希支持异构硬件单步重放审计。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  可复现训练 训练审计 基础模型 训练预算：数据配比、目标与优化器 OPEN-1B 为什么把逐步状态审计放到训练流程里？ 最终checkpoint不能单独说明每一步怎样得到。固定计算与数据顺序，并记录状态哈希，可支持重放某一步并对照状态，帮助定位训练执行差异。 示意：第100步开始偏离时，可先对照这一点的输入与状态，而不只比较最终模型分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-open-1b-audit-631edf79" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ba2f25947a914bb4">OPEN-1B 为什么把逐步状态审计放到训练流程里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-1b-audit">OPEN-1B: A Fully Auditable Training Run</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Gensyn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终checkpoint不能单独说明每一步怎样得到。固定计算与数据顺序，并记录状态哈希，可支持重放某一步并对照状态，帮助定位训练执行差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第100步开始偏离时，可先对照这一点的输入与状态，而不只比较最终模型分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17380">原论文</a> · <a href="../../../../foundation-models/2609.17380-open-1b-audit/">实现解读</a> · <a href="#qa-ba2f25947a914bb4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-1b-audit" data-paper-title="OPEN-1B: A Fully Auditable Training Run" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OPEN-1B: A Fully Auditable Training Run 基础模型 Gensyn 2026-09-15 固定 kernel reduction、数据批次与集体通信顺序，并用逐步状态哈希支持异构硬件单步重放审计。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  可复现训练 训练审计 基础模型 训练预算：数据配比、目标与优化器 只固定随机种子，为何还不足以审计一次预训练能否逐步重放？ 数据批次、kernel归约与集体通信顺序也会影响浮点计算轨迹。OPEN-1B把这些执行条件与逐步状态哈希一起记录，用单步重放定位差异，而不只比较最终loss。状态哈希能发现不一致，但不能自动解释差异来源，也不等于换硬件后天然逐bit相同。 教学例子：同样梯度项换一种求和顺序就可能产生小数值差；若只保存seed，难以知道差异从哪一步开始，逐步哈希与执行顺序记录可帮助缩小范围。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-eeaeefec1cc1f4e2">只固定随机种子，为何还不足以审计一次预训练能否逐步重放？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-1b-audit">OPEN-1B: A Fully Auditable Training Run</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Gensyn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>数据批次、kernel归约与集体通信顺序也会影响浮点计算轨迹。OPEN-1B把这些执行条件与逐步状态哈希一起记录，用单步重放定位差异，而不只比较最终loss。状态哈希能发现不一致，但不能自动解释差异来源，也不等于换硬件后天然逐bit相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样梯度项换一种求和顺序就可能产生小数值差；若只保存seed，难以知道差异从哪一步开始，逐步哈希与执行顺序记录可帮助缩小范围。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17380">原论文</a> · <a href="../../../../foundation-models/2609.17380-open-1b-audit/">实现解读</a> · <a href="#qa-eeaeefec1cc1f4e2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-1b-audit" data-paper-title="OPEN-1B: A Fully Auditable Training Run" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OPEN-1B: A Fully Auditable Training Run 基础模型 Gensyn 2026-09-15 固定 kernel reduction、数据批次与集体通信顺序，并用逐步状态哈希支持异构硬件单步重放审计。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  可复现训练 训练审计 基础模型 训练预算：数据配比、目标与优化器 只固定随机 seed，与固定 reduction、批次和通信顺序有什么区别？ seed只控制部分随机来源，浮点归约顺序、批次次序和集体通信也可能改变结果。审计需要把这些执行条件显式固定，不能把同seed自动等同于跨硬件逐步可重放。 示意：加法顺序变化也可能积累数值差异，即使最初随机初始化相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-592091d76caabfd0">只固定随机 seed，与固定 reduction、批次和通信顺序有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-1b-audit">OPEN-1B: A Fully Auditable Training Run</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Gensyn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>seed只控制部分随机来源，浮点归约顺序、批次次序和集体通信也可能改变结果。审计需要把这些执行条件显式固定，不能把同seed自动等同于跨硬件逐步可重放。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>加法顺序变化也可能积累数值差异，即使最初随机初始化相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17380">原论文</a> · <a href="../../../../foundation-models/2609.17380-open-1b-audit/">实现解读</a> · <a href="#qa-592091d76caabfd0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-1b-audit" data-paper-title="OPEN-1B: A Fully Auditable Training Run" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OPEN-1B: A Fully Auditable Training Run 基础模型 Gensyn 2026-09-15 固定 kernel reduction、数据批次与集体通信顺序，并用逐步状态哈希支持异构硬件单步重放审计。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  可复现训练 训练审计 基础模型 训练预算：数据配比、目标与优化器 canonical hash 一致，能够独自证明整个400B-token训练已复现吗？ 不能。当前本地只验证固定顺序reduction与canonical hash；完整审计还需对应批次、状态和实际重放链路。哈希是状态对照工具，既不替代训练执行，也不单独证明算法正确。 示意：两个小张量编码后哈希相同，不等于已重放原文全部预训练步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d2ae1e15043babee">canonical hash 一致，能够独自证明整个400B-token训练已复现吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-1b-audit">OPEN-1B: A Fully Auditable Training Run</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Gensyn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前本地只验证固定顺序reduction与canonical hash；完整审计还需对应批次、状态和实际重放链路。哈希是状态对照工具，既不替代训练执行，也不单独证明算法正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个小张量编码后哈希相同，不等于已重放原文全部预训练步骤。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17380">原论文</a> · <a href="../../../../foundation-models/2609.17380-open-1b-audit/">实现解读</a> · <a href="#qa-d2ae1e15043babee">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:musec" data-paper-title="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training 基础模型 National University of Singapore 2026-09-10 对 Muon momentum 的奇异值做平滑谱裁剪，避免硬截断不连续，同时限制不稳定大方向。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  优化器 谱裁剪 基础模型 训练预算：数据配比、目标与优化器 Musec 想限制的是动量矩阵里的哪一类不稳定因素？ 它针对过大的谱方向，对动量奇异值施加平滑裁剪，减少这些方向对Muon-type更新的支配。控制谱幅度是稳定更新的手段，不自动保证最终任务loss更好。 示意：少数异常大的奇异值可被约束，正常方向不必一起按同样倍率缩小。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-musec-4d47b01b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8636213a2e2d2ea8">Musec 想限制的是动量矩阵里的哪一类不稳定因素？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amusec">Musec: MomentUm SpEctral Clipping for Stable Muon-type Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它针对过大的谱方向，对动量奇异值施加平滑裁剪，减少这些方向对Muon-type更新的支配。控制谱幅度是稳定更新的手段，不自动保证最终任务loss更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>少数异常大的奇异值可被约束，正常方向不必一起按同样倍率缩小。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11655">原论文</a> · <a href="../../../../foundation-models/2609.11655-musec/">实现解读</a> · <a href="#qa-8636213a2e2d2ea8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:musec" data-paper-title="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training 基础模型 National University of Singapore 2026-09-10 对 Muon momentum 的奇异值做平滑谱裁剪，避免硬截断不连续，同时限制不稳定大方向。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  优化器 谱裁剪 基础模型 训练预算：数据配比、目标与优化器 Musec的谱裁剪与把所有梯度统一缩小，有什么区别？ 谱裁剪作用于动量矩阵的奇异值，重点限制不稳定的大方向，并用平滑处理避免硬阈值附近的不连续。统一缩放则同时压小所有方向，无法表达这种选择性。它控制的是更新几何；稳定性与最终优化质量仍需分开验证，不能由范数受控直接推出任务效果更好。 教学例子：一个矩阵方向特别大、其他方向正常；谱处理可以主要约束异常方向，而整体乘0.1会连正常方向也一起缩得很小。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-42029f8a35e58893">Musec的谱裁剪与把所有梯度统一缩小，有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amusec">Musec: MomentUm SpEctral Clipping for Stable Muon-type Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>谱裁剪作用于动量矩阵的奇异值，重点限制不稳定的大方向，并用平滑处理避免硬阈值附近的不连续。统一缩放则同时压小所有方向，无法表达这种选择性。它控制的是更新几何；稳定性与最终优化质量仍需分开验证，不能由范数受控直接推出任务效果更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个矩阵方向特别大、其他方向正常；谱处理可以主要约束异常方向，而整体乘0.1会连正常方向也一起缩得很小。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11655">原论文</a> · <a href="../../../../foundation-models/2609.11655-musec/">实现解读</a> · <a href="#qa-42029f8a35e58893">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:musec" data-paper-title="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training 基础模型 National University of Singapore 2026-09-10 对 Muon momentum 的奇异值做平滑谱裁剪，避免硬截断不连续，同时限制不稳定大方向。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  优化器 谱裁剪 基础模型 训练预算：数据配比、目标与优化器 平滑谱裁剪与硬阈值截断，在阈值附近有什么不同？ 硬阈值对跨界方向处理会突变；平滑裁剪让奇异值映射随输入更连续。它改变谱幅度的响应方式，仍需要明确裁剪规则和预算，不能仅用“更稳定”替代定义。 示意：一个奇异值从略低阈值变到略高阈值时，不应突然产生完全不同的更新幅度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2be148601aabca00">平滑谱裁剪与硬阈值截断，在阈值附近有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amusec">Musec: MomentUm SpEctral Clipping for Stable Muon-type Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>硬阈值对跨界方向处理会突变；平滑裁剪让奇异值映射随输入更连续。它改变谱幅度的响应方式，仍需要明确裁剪规则和预算，不能仅用“更稳定”替代定义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个奇异值从略低阈值变到略高阈值时，不应突然产生完全不同的更新幅度。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11655">原论文</a> · <a href="../../../../foundation-models/2609.11655-musec/">实现解读</a> · <a href="#qa-2be148601aabca00">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:musec" data-paper-title="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training 基础模型 National University of Singapore 2026-09-10 对 Muon momentum 的奇异值做平滑谱裁剪，避免硬截断不连续，同时限制不稳定大方向。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  优化器 谱裁剪 基础模型 训练预算：数据配比、目标与优化器 本地完整 SVD soft-clipping reference，能证明大模型训练吞吐吗？ 不能。它用于检查动量的谱分解、平滑映射与重建方向，未复刻大模型训练或优化性能kernel。应把谱处理数值正确性与端到端耗时分开验收。 示意：小矩阵经裁剪重建符合参考，不说明在大模型每步做这件事仍具有同样开销。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0cabe7890ac42e48">本地完整 SVD soft-clipping reference，能证明大模型训练吞吐吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amusec">Musec: MomentUm SpEctral Clipping for Stable Muon-type Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。它用于检查动量的谱分解、平滑映射与重建方向，未复刻大模型训练或优化性能kernel。应把谱处理数值正确性与端到端耗时分开验收。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>小矩阵经裁剪重建符合参考，不说明在大模型每步做这件事仍具有同样开销。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11655">原论文</a> · <a href="../../../../foundation-models/2609.11655-musec/">实现解读</a> · <a href="#qa-0cabe7890ac42e48">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hilp" data-paper-title="Hierarchical Latent Prediction for Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Hierarchical Latent Prediction for Language Models 基础模型 University of Texas at Austin 2026-08-06 主题：分层 latent 预训练。NextLat 的逐步 latent rollout 会累积误差。HiLP 增加更粗粒度的抽象 latent 目标，让局部状态同时受长时间尺度结构约束。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。合成多尺度序列上比较 next-latent 与加入块级 abstract latent 的预测误差；结构也接入 micro-LLM evolve。  pretraining latent-prediction multi-token-prediction speculative-decoding 基础模型 训练预算：数据配比、目标与优化器 HiLP 为什么同时预测下一 latent 和更粗的 abstract latent？ 逐步latent rollout可能累积局部误差，较粗时间尺度的目标为局部状态提供长期结构约束。它让模型既关注下一步细节，也学习更远尺度的变化。 示意：预测接下来一个词的表示时，也受到下一段整体走向的辅助约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-hilp-e751afd4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c953a19c1dd72bb5">HiLP 为什么同时预测下一 latent 和更粗的 abstract latent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahilp">Hierarchical Latent Prediction for Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐步latent rollout可能累积局部误差，较粗时间尺度的目标为局部状态提供长期结构约束。它让模型既关注下一步细节，也学习更远尺度的变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预测接下来一个词的表示时，也受到下一段整体走向的辅助约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05806">原论文</a> · <a href="../../../../reproductions/2608.05806-hilp/">实现解读</a> · <a href="#qa-c953a19c1dd72bb5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hilp" data-paper-title="Hierarchical Latent Prediction for Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Hierarchical Latent Prediction for Language Models 基础模型 University of Texas at Austin 2026-08-06 主题：分层 latent 预训练。NextLat 的逐步 latent rollout 会累积误差。HiLP 增加更粗粒度的抽象 latent 目标，让局部状态同时受长时间尺度结构约束。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。合成多尺度序列上比较 next-latent 与加入块级 abstract latent 的预测误差；结构也接入 micro-LLM evolve。  pretraining latent-prediction multi-token-prediction speculative-decoding 基础模型 训练预算：数据配比、目标与优化器 HiLP为什么在逐步latent预测之外，再加一个更粗时间尺度的目标？ 连续一步预测可能把小误差逐步传下去，局部相似并不保证远处结构仍正确。HiLP用粗粒度抽象latent目标约束更长尺度，同时保留next-token与局部latent训练，使表示兼顾近期细节和远程结构。层级目标提供额外约束，不等于消除了rollout误差或无需检验长程效果。 教学例子：每一步都稍微偏离路线，走很多步后会离终点很远；除了预测下一步，还预测下一个阶段的抽象状态，可以对局部轨迹施加更远的约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-988153cb726324b4">HiLP为什么在逐步latent预测之外，再加一个更粗时间尺度的目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahilp">Hierarchical Latent Prediction for Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续一步预测可能把小误差逐步传下去，局部相似并不保证远处结构仍正确。HiLP用粗粒度抽象latent目标约束更长尺度，同时保留next-token与局部latent训练，使表示兼顾近期细节和远程结构。层级目标提供额外约束，不等于消除了rollout误差或无需检验长程效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>每一步都稍微偏离路线，走很多步后会离终点很远；除了预测下一步，还预测下一个阶段的抽象状态，可以对局部轨迹施加更远的约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05806">原论文</a> · <a href="../../../../reproductions/2608.05806-hilp/">实现解读</a> · <a href="#qa-988153cb726324b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hilp" data-paper-title="Hierarchical Latent Prediction for Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Hierarchical Latent Prediction for Language Models 基础模型 University of Texas at Austin 2026-08-06 主题：分层 latent 预训练。NextLat 的逐步 latent rollout 会累积误差。HiLP 增加更粗粒度的抽象 latent 目标，让局部状态同时受长时间尺度结构约束。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。合成多尺度序列上比较 next-latent 与加入块级 abstract latent 的预测误差；结构也接入 micro-LLM evolve。  pretraining latent-prediction multi-token-prediction speculative-decoding 基础模型 训练预算：数据配比、目标与优化器 增加粗尺度 latent loss，与单纯加大下一步预测 loss 权重有什么不同？ 后者仍监督同一时间尺度；粗尺度目标引入不同跨度的预测对象，能约束局部误差未覆盖的结构。比较时需区分新增目标与仅调整λ1的效果，不能把两者视为同一消融。 示意：把下一秒误差权重翻倍，并不等于要求模型预测下一分钟的整体状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6430efce8e8df83a">增加粗尺度 latent loss，与单纯加大下一步预测 loss 权重有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahilp">Hierarchical Latent Prediction for Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后者仍监督同一时间尺度；粗尺度目标引入不同跨度的预测对象，能约束局部误差未覆盖的结构。比较时需区分新增目标与仅调整λ1的效果，不能把两者视为同一消融。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把下一秒误差权重翻倍，并不等于要求模型预测下一分钟的整体状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05806">原论文</a> · <a href="../../../../reproductions/2608.05806-hilp/">实现解读</a> · <a href="#qa-6430efce8e8df83a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hilp" data-paper-title="Hierarchical Latent Prediction for Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Hierarchical Latent Prediction for Language Models 基础模型 University of Texas at Austin 2026-08-06 主题：分层 latent 预训练。NextLat 的逐步 latent rollout 会累积误差。HiLP 增加更粗粒度的抽象 latent 目标，让局部状态同时受长时间尺度结构约束。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。合成多尺度序列上比较 next-latent 与加入块级 abstract latent 的预测误差；结构也接入 micro-LLM evolve。  pretraining latent-prediction multi-token-prediction speculative-decoding 基础模型 训练预算：数据配比、目标与优化器 HiLP 的实验怎样才能说明粗尺度目标的作用，而不是数据或预算变化？ 应在相同切分、训练预算和主干下比较去掉与加入块级abstract目标的路径，分别记录细尺度与粗尺度误差。当前合成序列机制对照不等于论文规模语言模型效果。 示意：只增加λH对应目标，若同时更换数据和训练步数，就难把变化归因于层级预测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-26cab03f82cf2939">HiLP 的实验怎样才能说明粗尺度目标的作用，而不是数据或预算变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahilp">Hierarchical Latent Prediction for Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应在相同切分、训练预算和主干下比较去掉与加入块级abstract目标的路径，分别记录细尺度与粗尺度误差。当前合成序列机制对照不等于论文规模语言模型效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只增加λH对应目标，若同时更换数据和训练步数，就难把变化归因于层级预测。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05806">原论文</a> · <a href="../../../../reproductions/2608.05806-hilp/">实现解读</a> · <a href="#qa-26cab03f82cf2939">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-orchestra" data-paper-title="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data 基础模型 Fudan University / Shanghai Jiao Tong University / SII-GAIR 2026-07-27 固定 corpus-level 清洗会过度处理本来干净的文本，也会对不同噪声使用同一操作。DataOrchestra 为每个 1024-token chunk 生成计划：先选 Drop、Untouch 或 Clean；Clean 时再按 NP（Noise Pruning）→ SR（Surface Rectification）→ PA（Pedagogical Augmentation）选择阶段，并为 rewrite 生成该 chunk 专属 instruction。 Fidelity: 核心机制复现。实际训练 per-example orchestrator、执行多操作路由并以同预算重新预训练；程序化教师和小模型替代论文大规模 LLM 工具链。本地 8-feature MLP 与程序化规则替代 Qwen3-235B teacher/verifier、Qwen3-1.7B orchestrator、0.6B NP 和 4B SR/PA；四种确定性编辑替代自然语言 chunk-specific rewrite，WikiText-2 替代 20B/30B token 多语料。因此这是 orchestration 决策与下游预训练链路的核心机制复现，不是论文数据质量规模结论的复刻。  llm-pretraining data-curation data-cleaning learned-orchestration 基础模型 训练预算：数据配比、目标与优化器 DataOrchestra 为什么把每个 chunk 当成一个需要单独决策的数据处理单元？ 不同chunk的噪声与质量不同，固定清洗流程可能过度处理干净文本。orchestrator为每块选择Drop、Untouch或Clean，并在需要时组织具体阶段和指令。 示意：一段已干净的说明可原样保留，另一段乱码则可能删除或局部修复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-data-orchestra-f57d3169" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-26d35141723aa774">DataOrchestra 为什么把每个 chunk 当成一个需要单独决策的数据处理单元？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-orchestra">DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University / Shanghai Jiao Tong University / SII-GAIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同chunk的噪声与质量不同，固定清洗流程可能过度处理干净文本。orchestrator为每块选择Drop、Untouch或Clean，并在需要时组织具体阶段和指令。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一段已干净的说明可原样保留，另一段乱码则可能删除或局部修复。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24717">原论文</a> · <a href="../../../../reproductions/2607.24717-data-orchestra/">实现解读</a> · <a href="#qa-26d35141723aa774">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-orchestra" data-paper-title="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data 基础模型 Fudan University / Shanghai Jiao Tong University / SII-GAIR 2026-07-27 固定 corpus-level 清洗会过度处理本来干净的文本，也会对不同噪声使用同一操作。DataOrchestra 为每个 1024-token chunk 生成计划：先选 Drop、Untouch 或 Clean；Clean 时再按 NP（Noise Pruning）→ SR（Surface Rectification）→ PA（Pedagogical Augmentation）选择阶段，并为 rewrite 生成该 chunk 专属 instruction。 Fidelity: 核心机制复现。实际训练 per-example orchestrator、执行多操作路由并以同预算重新预训练；程序化教师和小模型替代论文大规模 LLM 工具链。本地 8-feature MLP 与程序化规则替代 Qwen3-235B teacher/verifier、Qwen3-1.7B orchestrator、0.6B NP 和 4B SR/PA；四种确定性编辑替代自然语言 chunk-specific rewrite，WikiText-2 替代 20B/30B token 多语料。因此这是 orchestration 决策与下游预训练链路的核心机制复现，不是论文数据质量规模结论的复刻。  llm-pretraining data-curation data-cleaning learned-orchestration 基础模型 训练预算：数据配比、目标与优化器 DataOrchestra为何先允许Drop和Untouch，而不是给每个chunk都依次清洗三遍？ 不同样本需要不同处理，干净文本反复改写既浪费算力又可能损伤内容。orchestrator先决定丢弃、原样保留或清洗，只有Clean才组合噪声剪除、表面修正与教学增强，并生成样本专属指令；训练计划还经过真实执行与核验。目标是质量与成本的取舍，不是最大化被清洗比例。 教学例子：一段干净教科书可Untouch，网页噪声段先剪除导航，严重缺内容的段落可Drop；给三者统一套改写指令，可能花钱把原本正确的文本改坏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-221959926fa7c86d">DataOrchestra为何先允许Drop和Untouch，而不是给每个chunk都依次清洗三遍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-orchestra">DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University / Shanghai Jiao Tong University / SII-GAIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同样本需要不同处理，干净文本反复改写既浪费算力又可能损伤内容。orchestrator先决定丢弃、原样保留或清洗，只有Clean才组合噪声剪除、表面修正与教学增强，并生成样本专属指令；训练计划还经过真实执行与核验。目标是质量与成本的取舍，不是最大化被清洗比例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一段干净教科书可Untouch，网页噪声段先剪除导航，严重缺内容的段落可Drop；给三者统一套改写指令，可能花钱把原本正确的文本改坏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24717">原论文</a> · <a href="../../../../reproductions/2607.24717-data-orchestra/">实现解读</a> · <a href="#qa-221959926fa7c86d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-orchestra" data-paper-title="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data 基础模型 Fudan University / Shanghai Jiao Tong University / SII-GAIR 2026-07-27 固定 corpus-level 清洗会过度处理本来干净的文本，也会对不同噪声使用同一操作。DataOrchestra 为每个 1024-token chunk 生成计划：先选 Drop、Untouch 或 Clean；Clean 时再按 NP（Noise Pruning）→ SR（Surface Rectification）→ PA（Pedagogical Augmentation）选择阶段，并为 rewrite 生成该 chunk 专属 instruction。 Fidelity: 核心机制复现。实际训练 per-example orchestrator、执行多操作路由并以同预算重新预训练；程序化教师和小模型替代论文大规模 LLM 工具链。本地 8-feature MLP 与程序化规则替代 Qwen3-235B teacher/verifier、Qwen3-1.7B orchestrator、0.6B NP 和 4B SR/PA；四种确定性编辑替代自然语言 chunk-specific rewrite，WikiText-2 替代 20B/30B token 多语料。因此这是 orchestration 决策与下游预训练链路的核心机制复现，不是论文数据质量规模结论的复刻。  llm-pretraining data-curation data-cleaning learned-orchestration 基础模型 训练预算：数据配比、目标与优化器 逐样本编排相对统一 corpus-level 清洗，为什么还要保留 Untouch？ Untouch明确允许不处理，避免把清洗率误当质量目标。逐样本计划还可选择不同阶段；统一流水线通常让同类操作作用于所有样本，难兼顾过度改写与处理成本。 示意：把本来正确的代码也强行改写，可能既花工具计算又破坏原始信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1ce48109d843ddae">逐样本编排相对统一 corpus-level 清洗，为什么还要保留 Untouch？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-orchestra">DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University / Shanghai Jiao Tong University / SII-GAIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Untouch明确允许不处理，避免把清洗率误当质量目标。逐样本计划还可选择不同阶段；统一流水线通常让同类操作作用于所有样本，难兼顾过度改写与处理成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把本来正确的代码也强行改写，可能既花工具计算又破坏原始信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24717">原论文</a> · <a href="../../../../reproductions/2607.24717-data-orchestra/">实现解读</a> · <a href="#qa-1ce48109d843ddae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-orchestra" data-paper-title="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data 基础模型 Fudan University / Shanghai Jiao Tong University / SII-GAIR 2026-07-27 固定 corpus-level 清洗会过度处理本来干净的文本，也会对不同噪声使用同一操作。DataOrchestra 为每个 1024-token chunk 生成计划：先选 Drop、Untouch 或 Clean；Clean 时再按 NP（Noise Pruning）→ SR（Surface Rectification）→ PA（Pedagogical Augmentation）选择阶段，并为 rewrite 生成该 chunk 专属 instruction。 Fidelity: 核心机制复现。实际训练 per-example orchestrator、执行多操作路由并以同预算重新预训练；程序化教师和小模型替代论文大规模 LLM 工具链。本地 8-feature MLP 与程序化规则替代 Qwen3-235B teacher/verifier、Qwen3-1.7B orchestrator、0.6B NP 和 4B SR/PA；四种确定性编辑替代自然语言 chunk-specific rewrite，WikiText-2 替代 20B/30B token 多语料。因此这是 orchestration 决策与下游预训练链路的核心机制复现，不是论文数据质量规模结论的复刻。  llm-pretraining data-curation data-cleaning learned-orchestration 基础模型 训练预算：数据配比、目标与优化器 DataOrchestra 的 teacher 粗计划，能未经执行验证就直接作为最终 SFT 目标吗？ 文档先实际执行tool model并由verifier检查，失败rewrite有限次纠正，内容损失或改动不足的stage会删除；通过验证的evolved plan才用于训练。只存一份粗计划不能替代这条闭环。 示意：计划写了“修复格式”，但执行后丢了内容，这个stage不应仍被当作成功范例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-aa1ba5f78ac0bb62">DataOrchestra 的 teacher 粗计划，能未经执行验证就直接作为最终 SFT 目标吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-orchestra">DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University / Shanghai Jiao Tong University / SII-GAIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档先实际执行tool model并由verifier检查，失败rewrite有限次纠正，内容损失或改动不足的stage会删除；通过验证的evolved plan才用于训练。只存一份粗计划不能替代这条闭环。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>计划写了“修复格式”，但执行后丢了内容，这个stage不应仍被当作成功范例。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24717">原论文</a> · <a href="../../../../reproductions/2607.24717-data-orchestra/">实现解读</a> · <a href="#qa-aa1ba5f78ac0bb62">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gaugequant" data-paper-title="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries 基础模型 University of Cambridge 2026-07-22 LLM 内部通道存在保持函数不变的 gauge 对称性，但不同等价基的量化误差差异很大。GaugeQuant 在训练中在线学习量化友好正交基，以 LogSumExp 压制 activation outliers，不需要额外 calibration corpus。 未训练 LLaMA-2 7B，也没有 int4 kernel；Fidelity: 核心机制复现。真实学习正交 gauge、优化 outlier，并走 W4A4 STE 路径。未训练 LLaMA-2 7B，也没有 int4 kernel；STE fake quant 用于验证在线 gauge 学习机制，不代表实际吞吐。本地对照口径：基线是浮点 llama_modern；实验组训练 Householder 正交 gauge 并执行 W4A4 STE，LM loss 5.7471→5.7313，相对 -0.27%，PPL 313.27→308.38（-1.56%）。  llm-training quantization w4a4 基础模型 训练预算：数据配比、目标与优化器 量化里的 activation outlier 为什么会让大多数普通数值也受影响？ 有限位宽要覆盖一组数的动态范围，少数大幅度通道会让表示普通值的间隔变粗。GaugeQuant学习内部正交基，用outlier目标寻找更利于量化的表示；浮点等价不代表量化误差相同。 示意：用很少刻度同时表示1、2和1000时，普通小数值之间的差异可能更难保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-gaugequant-8dce1822" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3208d7926b6e1850">量化里的 activation outlier 为什么会让大多数普通数值也受影响？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agaugequant">GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有限位宽要覆盖一组数的动态范围，少数大幅度通道会让表示普通值的间隔变粗。GaugeQuant学习内部正交基，用outlier目标寻找更利于量化的表示；浮点等价不代表量化误差相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用很少刻度同时表示1、2和1000时，普通小数值之间的差异可能更难保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20757">原论文</a> · <a href="../../../../reproductions/2607.20757-gaugequant/">实现解读</a> · <a href="#qa-3208d7926b6e1850">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gaugequant" data-paper-title="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries 基础模型 University of Cambridge 2026-07-22 LLM 内部通道存在保持函数不变的 gauge 对称性，但不同等价基的量化误差差异很大。GaugeQuant 在训练中在线学习量化友好正交基，以 LogSumExp 压制 activation outliers，不需要额外 calibration corpus。 未训练 LLaMA-2 7B，也没有 int4 kernel；Fidelity: 核心机制复现。真实学习正交 gauge、优化 outlier，并走 W4A4 STE 路径。未训练 LLaMA-2 7B，也没有 int4 kernel；STE fake quant 用于验证在线 gauge 学习机制，不代表实际吞吐。本地对照口径：基线是浮点 llama_modern；实验组训练 Householder 正交 gauge 并执行 W4A4 STE，LM loss 5.7471→5.7313，相对 -0.27%，PPL 313.27→308.38（-1.56%）。  llm-training quantization w4a4 基础模型 训练预算：数据配比、目标与优化器 GaugeQuant为什么能先换内部坐标基，再降低量化误差，而不必先改变原始浮点函数？ 某些内部通道变换具有函数等价的对称性：一侧乘正交基，另一侧作逆变换，浮点组合保持一致。量化却依赖坐标轴上的数值分布，因此等价基可能有不同outlier和舍入误差。方法在线学习更友好的基，利用的是函数等价与量化不等价之间的空间，不能随意在不满足对称条件的位置旋转。 教学例子：原来能量集中在一个特别大的通道，经合法旋转可分散到多个通道；逆变换保持浮点输出，而低比特码本可能更容易表示分散后的数值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-be6020bebde4aa23">GaugeQuant为什么能先换内部坐标基，再降低量化误差，而不必先改变原始浮点函数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agaugequant">GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>某些内部通道变换具有函数等价的对称性：一侧乘正交基，另一侧作逆变换，浮点组合保持一致。量化却依赖坐标轴上的数值分布，因此等价基可能有不同outlier和舍入误差。方法在线学习更友好的基，利用的是函数等价与量化不等价之间的空间，不能随意在不满足对称条件的位置旋转。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原来能量集中在一个特别大的通道，经合法旋转可分散到多个通道；逆变换保持浮点输出，而低比特码本可能更容易表示分散后的数值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20757">原论文</a> · <a href="../../../../reproductions/2607.20757-gaugequant/">实现解读</a> · <a href="#qa-be6020bebde4aa23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gaugequant" data-paper-title="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries 基础模型 University of Cambridge 2026-07-22 LLM 内部通道存在保持函数不变的 gauge 对称性，但不同等价基的量化误差差异很大。GaugeQuant 在训练中在线学习量化友好正交基，以 LogSumExp 压制 activation outliers，不需要额外 calibration corpus。 未训练 LLaMA-2 7B，也没有 int4 kernel；Fidelity: 核心机制复现。真实学习正交 gauge、优化 outlier，并走 W4A4 STE 路径。未训练 LLaMA-2 7B，也没有 int4 kernel；STE fake quant 用于验证在线 gauge 学习机制，不代表实际吞吐。本地对照口径：基线是浮点 llama_modern；实验组训练 Householder 正交 gauge 并执行 W4A4 STE，LM loss 5.7471→5.7313，相对 -0.27%，PPL 313.27→308.38（-1.56%）。  llm-training quantization w4a4 基础模型 训练预算：数据配比、目标与优化器 GaugeQuant 与依赖额外 calibration corpus 的离线量化，优化时机有什么不同？ GaugeQuant把正交基及outlier目标放进训练，与LM目标共同优化；离线校准通常在冻结模型后根据样本统计调整量化。训练机制和额外数据需求不同，不能仅比较最终位宽。 示意：两个方案都写W4A4，但一个在训练中改变基，另一个在训练后固定校准参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a0afffd4b54bbb5b">GaugeQuant 与依赖额外 calibration corpus 的离线量化，优化时机有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agaugequant">GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>GaugeQuant把正交基及outlier目标放进训练，与LM目标共同优化；离线校准通常在冻结模型后根据样本统计调整量化。训练机制和额外数据需求不同，不能仅比较最终位宽。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个方案都写W4A4，但一个在训练中改变基，另一个在训练后固定校准参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20757">原论文</a> · <a href="../../../../reproductions/2607.20757-gaugequant/">实现解读</a> · <a href="#qa-a0afffd4b54bbb5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gaugequant" data-paper-title="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries 基础模型 University of Cambridge 2026-07-22 LLM 内部通道存在保持函数不变的 gauge 对称性，但不同等价基的量化误差差异很大。GaugeQuant 在训练中在线学习量化友好正交基，以 LogSumExp 压制 activation outliers，不需要额外 calibration corpus。 未训练 LLaMA-2 7B，也没有 int4 kernel；Fidelity: 核心机制复现。真实学习正交 gauge、优化 outlier，并走 W4A4 STE 路径。未训练 LLaMA-2 7B，也没有 int4 kernel；STE fake quant 用于验证在线 gauge 学习机制，不代表实际吞吐。本地对照口径：基线是浮点 llama_modern；实验组训练 Householder 正交 gauge 并执行 W4A4 STE，LM loss 5.7471→5.7313，相对 -0.27%，PPL 313.27→308.38（-1.56%）。  llm-training quantization w4a4 基础模型 训练预算：数据配比、目标与优化器 验证 GaugeQuant 时，怎样区分函数保持、fake quant 与真正 int4 执行？ 先核对Q正交及对应权重变换，再检查量化与梯度路径；STE fake quant仍可用浮点kernel执行。本地没有int4 kernel，不能用位宽标签推导实测吞吐或内存带宽收益。 示意：张量值被映射到16个级别，不代表它已以4-bit打包并被int4硬件指令读取。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3e9baa60fb6616ad">验证 GaugeQuant 时，怎样区分函数保持、fake quant 与真正 int4 执行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agaugequant">GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先核对Q正交及对应权重变换，再检查量化与梯度路径；STE fake quant仍可用浮点kernel执行。本地没有int4 kernel，不能用位宽标签推导实测吞吐或内存带宽收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>张量值被映射到16个级别，不代表它已以4-bit打包并被int4硬件指令读取。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20757">原论文</a> · <a href="../../../../reproductions/2607.20757-gaugequant/">实现解读</a> · <a href="#qa-3e9baa60fb6616ad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppl-factory" data-paper-title="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning 基础模型 McGill University 2026-07-20 固定的“选最难/最容易”规则会随任务和数据预算失效。PPL-Factory 先用冻结基础模型计算任务相关 NLL：语言建模按 packed block，推理 SFT 只看 reasoning/answer response；再按预算切换策略，高预算偏 easy，较低预算选 middle，极低预算从 middle pool 随机抽样以保覆盖。 未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。Fidelity: 核心机制复现。真实训练冻结 scorer、逐块计算 NLL，并从同一 checkpoint 对 random/easy/middle 子集做同预算微调。只复现 CLM packed-block 分支；未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。负结果保留，不外推为对原论文的否定。本地对照口径：基线是 20% 随机 block；  llm-training data-selection efficient-finetuning 基础模型 训练预算：数据配比、目标与优化器 PPL-Factory 为什么把样本选择策略与任务、数据预算绑定？ 固定选最难或最容易并不适用于所有预算。方法先用冻结模型计算任务相关NLL，再按预算在easy、middle及mid-random之间切换，兼顾训练效用与覆盖。 示意：极少数据时，只取狭窄分数区间可能损失覆盖，随机抽middle pool是另一种取舍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-ppl-factory-5bbf227d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6acc0ef8d7d4889c">PPL-Factory 为什么把样本选择策略与任务、数据预算绑定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appl-factory">PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · McGill University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定选最难或最容易并不适用于所有预算。方法先用冻结模型计算任务相关NLL，再按预算在easy、middle及mid-random之间切换，兼顾训练效用与覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>极少数据时，只取狭窄分数区间可能损失覆盖，随机抽middle pool是另一种取舍。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18199">原论文</a> · <a href="../../../../reproductions/2607.18199-ppl-factory/">实现解读</a> · <a href="#qa-6acc0ef8d7d4889c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppl-factory" data-paper-title="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning 基础模型 McGill University 2026-07-20 固定的“选最难/最容易”规则会随任务和数据预算失效。PPL-Factory 先用冻结基础模型计算任务相关 NLL：语言建模按 packed block，推理 SFT 只看 reasoning/answer response；再按预算切换策略，高预算偏 easy，较低预算选 middle，极低预算从 middle pool 随机抽样以保覆盖。 未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。Fidelity: 核心机制复现。真实训练冻结 scorer、逐块计算 NLL，并从同一 checkpoint 对 random/easy/middle 子集做同预算微调。只复现 CLM packed-block 分支；未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。负结果保留，不外推为对原论文的否定。本地对照口径：基线是 20% 随机 block；  llm-training data-selection efficient-finetuning 基础模型 训练预算：数据配比、目标与优化器 PPL-Factory为什么不总选最难样本，还要随任务和数据预算改变选择区间？ 样本难度与有用性并非固定单调关系；高预算、低预算和极小预算下，学习信号与覆盖的取舍不同。它先用冻结基础模型按任务口径打分，再分别偏向easy、middle或从middle池随机抽样。推理SFT只看response损失，不能让prompt长度主导所谓难度。 教学例子：预算只能留几十条时，机械挑最难可能全是模型尚无学习信号的样本；从中等池随机抽取可保留部分覆盖。预算足够大后，最佳策略又可能改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0f2dc94cbdd47750">PPL-Factory为什么不总选最难样本，还要随任务和数据预算改变选择区间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appl-factory">PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · McGill University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>样本难度与有用性并非固定单调关系；高预算、低预算和极小预算下，学习信号与覆盖的取舍不同。它先用冻结基础模型按任务口径打分，再分别偏向easy、middle或从middle池随机抽样。推理SFT只看response损失，不能让prompt长度主导所谓难度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预算只能留几十条时，机械挑最难可能全是模型尚无学习信号的样本；从中等池随机抽取可保留部分覆盖。预算足够大后，最佳策略又可能改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18199">原论文</a> · <a href="../../../../reproductions/2607.18199-ppl-factory/">实现解读</a> · <a href="#qa-0f2dc94cbdd47750">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppl-factory" data-paper-title="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning 基础模型 McGill University 2026-07-20 固定的“选最难/最容易”规则会随任务和数据预算失效。PPL-Factory 先用冻结基础模型计算任务相关 NLL：语言建模按 packed block，推理 SFT 只看 reasoning/answer response；再按预算切换策略，高预算偏 easy，较低预算选 middle，极低预算从 middle pool 随机抽样以保覆盖。 未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。Fidelity: 核心机制复现。真实训练冻结 scorer、逐块计算 NLL，并从同一 checkpoint 对 random/easy/middle 子集做同预算微调。只复现 CLM packed-block 分支；未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。负结果保留，不外推为对原论文的否定。本地对照口径：基线是 20% 随机 block；  llm-training data-selection efficient-finetuning 基础模型 训练预算：数据配比、目标与优化器 推理 SFT 的 response-only NLL，与整段 prompt+response NLL 排名可能相同吗？ 不一定。整段分数会受到prompt长度和易预测文本影响；response-only把选择依据集中到reasoning/answer部分。语言建模packed-block又是另一口径，不能跨任务直接复用同一排名定义。 示意：一个很长但容易的prompt，可能掩盖其答案部分很难预测的事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bf9edb35a0895570">推理 SFT 的 response-only NLL，与整段 prompt+response NLL 排名可能相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appl-factory">PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · McGill University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不一定。整段分数会受到prompt长度和易预测文本影响；response-only把选择依据集中到reasoning/answer部分。语言建模packed-block又是另一口径，不能跨任务直接复用同一排名定义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个很长但容易的prompt，可能掩盖其答案部分很难预测的事实。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18199">原论文</a> · <a href="../../../../reproductions/2607.18199-ppl-factory/">实现解读</a> · <a href="#qa-bf9edb35a0895570">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppl-factory" data-paper-title="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning 基础模型 McGill University 2026-07-20 固定的“选最难/最容易”规则会随任务和数据预算失效。PPL-Factory 先用冻结基础模型计算任务相关 NLL：语言建模按 packed block，推理 SFT 只看 reasoning/answer response；再按预算切换策略，高预算偏 easy，较低预算选 middle，极低预算从 middle pool 随机抽样以保覆盖。 未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。Fidelity: 核心机制复现。真实训练冻结 scorer、逐块计算 NLL，并从同一 checkpoint 对 random/easy/middle 子集做同预算微调。只复现 CLM packed-block 分支；未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。负结果保留，不外推为对原论文的否定。本地对照口径：基线是 20% 随机 block；  llm-training data-selection efficient-finetuning 基础模型 训练预算：数据配比、目标与优化器 PPL-Factory 的选择实验，为什么要从同一冻结 scorer 和训练起点比较子集？ 否则分数模型或初始checkpoint变化会混入选择效果。文档固定scorer、各组block数量和微调预算，并保留middle规则未迁移成功的负结果；不能事后按test重选区间。 示意：Random、Easy与Middle若分别从不同起点训练，就难把PPL差异归因于数据选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fa724c161c1899c8">PPL-Factory 的选择实验，为什么要从同一冻结 scorer 和训练起点比较子集？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appl-factory">PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · McGill University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>否则分数模型或初始checkpoint变化会混入选择效果。文档固定scorer、各组block数量和微调预算，并保留middle规则未迁移成功的负结果；不能事后按test重选区间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Random、Easy与Middle若分别从不同起点训练，就难把PPL差异归因于数据选择。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18199">原论文</a> · <a href="../../../../reproductions/2607.18199-ppl-factory/">实现解读</a> · <a href="#qa-fa724c161c1899c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-language-model" data-paper-title="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research 基础模型 Indian Institute of Technology Madras 2026-07-18 许多预训练框架把模型结构、训练循环和分布式运行强耦合，难以做透明消融。OLM 让组件保持普通 PyTorch module，用 Block、Residual、Repeat、Parallel 描述布线，同一模型可从 notebook 迁移到 CPU、单 GPU 和单机多 GPU。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未搬运上游整个包和 27 个 preset，也未复刻 348M 四卡实验；本地验证结构语义和统一 evaluator 接口。本地对照口径：基线为同预算 LLaMA-modern，实验组为 olm_composable；相对 PPL -0.000001%。  pretraining-infrastructure composable-architecture small-language-model evolve 基础模型 训练预算：数据配比、目标与优化器 OpenLanguageModel 为什么坚持把组件保留为普通 PyTorch module？ 结构与训练/分布式框架强耦合会增加理解和消融成本。普通module加可组合布线，让模型结构更透明，同一模型也更容易在notebook、CPU和不同GPU环境间迁移。 示意：替换一个block时，可以明确看到改了哪条数据流，而不是同时更换整套训练框架。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-open-language-model-02ba0f0c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7a483d7ce6d15066">OpenLanguageModel 为什么坚持把组件保留为普通 PyTorch module？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-language-model">OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Indian Institute of Technology Madras</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>结构与训练/分布式框架强耦合会增加理解和消融成本。普通module加可组合布线，让模型结构更透明，同一模型也更容易在notebook、CPU和不同GPU环境间迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>替换一个block时，可以明确看到改了哪条数据流，而不是同时更换整套训练框架。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.16669">原论文</a> · <a href="../../../../reproductions/2607.16669-open-language-model/">实现解读</a> · <a href="#qa-7a483d7ce6d15066">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-language-model" data-paper-title="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research 基础模型 Indian Institute of Technology Madras 2026-07-18 许多预训练框架把模型结构、训练循环和分布式运行强耦合，难以做透明消融。OLM 让组件保持普通 PyTorch module，用 Block、Residual、Repeat、Parallel 描述布线，同一模型可从 notebook 迁移到 CPU、单 GPU 和单机多 GPU。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未搬运上游整个包和 27 个 preset，也未复刻 348M 四卡实验；本地验证结构语义和统一 evaluator 接口。本地对照口径：基线为同预算 LLaMA-modern，实验组为 olm_composable；相对 PPL -0.000001%。  pretraining-infrastructure composable-architecture small-language-model evolve 基础模型 训练预算：数据配比、目标与优化器 OpenLanguageModel的可组合Block/Residual/Repeat，怎样帮助判断消融到底改了什么？ 它把普通PyTorch组件与布线结构分开，让重复、残差和并行关系可直接组合，降低模型、训练循环与分布式执行的耦合。这样同一结构更容易跨notebook和不同设备运行，也更容易保持消融的其他条件一致。可读可组合是工程属性，本身不是模型能力提升的实验结论。 教学例子：比较串联两个块与两支并行相加时，可只改布线表达，沿用数据和训练循环；若同时换了整个分布式框架，就更难把结果归因于结构变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ae8ca0c028b6ef9a">OpenLanguageModel的可组合Block/Residual/Repeat，怎样帮助判断消融到底改了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-language-model">OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Indian Institute of Technology Madras</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把普通PyTorch组件与布线结构分开，让重复、残差和并行关系可直接组合，降低模型、训练循环与分布式执行的耦合。这样同一结构更容易跨notebook和不同设备运行，也更容易保持消融的其他条件一致。可读可组合是工程属性，本身不是模型能力提升的实验结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>比较串联两个块与两支并行相加时，可只改布线表达，沿用数据和训练循环；若同时换了整个分布式框架，就更难把结果归因于结构变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.16669">原论文</a> · <a href="../../../../reproductions/2607.16669-open-language-model/">实现解读</a> · <a href="#qa-ae8ca0c028b6ef9a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-language-model" data-paper-title="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research 基础模型 Indian Institute of Technology Madras 2026-07-18 许多预训练框架把模型结构、训练循环和分布式运行强耦合，难以做透明消融。OLM 让组件保持普通 PyTorch module，用 Block、Residual、Repeat、Parallel 描述布线，同一模型可从 notebook 迁移到 CPU、单 GPU 和单机多 GPU。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未搬运上游整个包和 27 个 preset，也未复刻 348M 四卡实验；本地验证结构语义和统一 evaluator 接口。本地对照口径：基线为同预算 LLaMA-modern，实验组为 olm_composable；相对 PPL -0.000001%。  pretraining-infrastructure composable-architecture small-language-model evolve 基础模型 训练预算：数据配比、目标与优化器 组合 DSL 的等价性测试，与比较一种新架构是否更好，目标相同吗？ 等价性测试检查改写布线后是否保持原计算语义；新架构比较则检验结构变化的效果。文档中几乎相同的PPL用于前者，不能把近零数值差异包装成质量提升。 示意：把x+f(x)改写成Residual(f)，首先应得到相同输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6e6cdf128f84a999">组合 DSL 的等价性测试，与比较一种新架构是否更好，目标相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-language-model">OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Indian Institute of Technology Madras</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>等价性测试检查改写布线后是否保持原计算语义；新架构比较则检验结构变化的效果。文档中几乎相同的PPL用于前者，不能把近零数值差异包装成质量提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把x+f(x)改写成Residual(f)，首先应得到相同输出。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.16669">原论文</a> · <a href="../../../../reproductions/2607.16669-open-language-model/">实现解读</a> · <a href="#qa-6e6cdf128f84a999">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-language-model" data-paper-title="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research 基础模型 Indian Institute of Technology Madras 2026-07-18 许多预训练框架把模型结构、训练循环和分布式运行强耦合，难以做透明消融。OLM 让组件保持普通 PyTorch module，用 Block、Residual、Repeat、Parallel 描述布线，同一模型可从 notebook 迁移到 CPU、单 GPU 和单机多 GPU。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未搬运上游整个包和 27 个 preset，也未复刻 348M 四卡实验；本地验证结构语义和统一 evaluator 接口。本地对照口径：基线为同预算 LLaMA-modern，实验组为 olm_composable；相对 PPL -0.000001%。  pretraining-infrastructure composable-architecture small-language-model evolve 基础模型 训练预算：数据配比、目标与优化器 实现 Residual 与 Parallel 时，怎样避免把连接关系写错？ 按文档Residual(f)(x)=x+f(x)，Parallel(f,g)(x)=f(x)+g(x)。还需检查输出维度与重复块的参数关系，不能把分支相加误作顺序串联；本地未搬运上游全部preset。 示意：f(x)+g(x)通常不同于g(f(x))，即使最后shape相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0d6ef84afdcc27b9">实现 Residual 与 Parallel 时，怎样避免把连接关系写错？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-language-model">OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Indian Institute of Technology Madras</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按文档Residual(f)(x)=x+f(x)，Parallel(f,g)(x)=f(x)+g(x)。还需检查输出维度与重复块的参数关系，不能把分支相加误作顺序串联；本地未搬运上游全部preset。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>f(x)+g(x)通常不同于g(f(x))，即使最后shape相同。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.16669">原论文</a> · <a href="../../../../reproductions/2607.16669-open-language-model/">实现解读</a> · <a href="#qa-0d6ef84afdcc27b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gemini-for-google" data-paper-title="Customizing an LLM for Enterprise Software Engineering" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Customizing an LLM for Enterprise Software Engineering 基础模型 Google 2026-05-15 从企业开发历史中提取高价值代码与交互信号，经过去重、质量过滤和污染控制形成中训练数据；用通用数据回放抑制灾难性遗忘，再做面向内部工具的后训练和部署评测。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  企业 LLM 数据治理 中训练与后训练 基础模型 训练预算：数据配比、目标与优化器 企业软件工程适配，为什么不是把内部代码直接全部继续训练？ 文档强调从开发历史提取高价值代码与交互信号，再做去重、质量过滤和污染控制，之后中训练与内部工具后训练。数据选择与评测环境同样是方法链路的一部分。 示意：重复生成文件与高价值修复历史，不应未经筛选就按同样权重混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-gemini-for-google-0c2d88a0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0ae31377ea1cdc2c">企业软件工程适配，为什么不是把内部代码直接全部继续训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agemini-for-google">Customizing an LLM for Enterprise Software Engineering</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档强调从开发历史提取高价值代码与交互信号，再做去重、质量过滤和污染控制，之后中训练与内部工具后训练。数据选择与评测环境同样是方法链路的一部分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>重复生成文件与高价值修复历史，不应未经筛选就按同样权重混在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16517">原论文</a> · <a href="../../../../foundation-models/2605.16517-gemini-for-google/">实现解读</a> · <a href="#qa-0ae31377ea1cdc2c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gemini-for-google" data-paper-title="Customizing an LLM for Enterprise Software Engineering" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Customizing an LLM for Enterprise Software Engineering 基础模型 Google 2026-05-15 从企业开发历史中提取高价值代码与交互信号，经过去重、质量过滤和污染控制形成中训练数据；用通用数据回放抑制灾难性遗忘，再做面向内部工具的后训练和部署评测。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  企业 LLM 数据治理 中训练与后训练 基础模型 训练预算：数据配比、目标与优化器 企业代码适配为什么还混入通用数据回放，而不是只训练内部高价值样本？ 企业样本使模型熟悉内部代码、工具和交互方式，但单独优化这部分可能遗忘通用能力。通用回放给训练提供另一组约束；去重、质量和污染控制则保护数据及评测口径。混合比例表达适配与保留的权衡，不能由内部任务提升直接推出通用能力也保持不变。 教学例子：模型学会内部构建命令后仍要完成一般代码推理；若训练全被内部模式占满，通用任务可能退化，所以应同时验证企业收益与通用回放的保留效果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-88875c261b2a4f2b">企业代码适配为什么还混入通用数据回放，而不是只训练内部高价值样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agemini-for-google">Customizing an LLM for Enterprise Software Engineering</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>企业样本使模型熟悉内部代码、工具和交互方式，但单独优化这部分可能遗忘通用能力。通用回放给训练提供另一组约束；去重、质量和污染控制则保护数据及评测口径。混合比例表达适配与保留的权衡，不能由内部任务提升直接推出通用能力也保持不变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型学会内部构建命令后仍要完成一般代码推理；若训练全被内部模式占满，通用任务可能退化，所以应同时验证企业收益与通用回放的保留效果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16517">原论文</a> · <a href="../../../../foundation-models/2605.16517-gemini-for-google/">实现解读</a> · <a href="#qa-88875c261b2a4f2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gemini-for-google" data-paper-title="Customizing an LLM for Enterprise Software Engineering" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Customizing an LLM for Enterprise Software Engineering 基础模型 Google 2026-05-15 从企业开发历史中提取高价值代码与交互信号，经过去重、质量过滤和污染控制形成中训练数据；用通用数据回放抑制灾难性遗忘，再做面向内部工具的后训练和部署评测。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  企业 LLM 数据治理 中训练与后训练 基础模型 训练预算：数据配比、目标与优化器 企业中训练数据准备，与普通通用语料继续训练有什么额外约束？ 企业任务包含内部代码、交互和工具使用分布，还需要控制重复与评测污染，并兼顾通用能力保留。通用训练loss下降不能自动替代内部开发工作流的部署评测。 示意：背下历史修复补丁可能降低训练loss，却不代表对新的内部问题更有效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dbddc43401d20e73">企业中训练数据准备，与普通通用语料继续训练有什么额外约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agemini-for-google">Customizing an LLM for Enterprise Software Engineering</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>企业任务包含内部代码、交互和工具使用分布，还需要控制重复与评测污染，并兼顾通用能力保留。通用训练loss下降不能自动替代内部开发工作流的部署评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>背下历史修复补丁可能降低训练loss，却不代表对新的内部问题更有效。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16517">原论文</a> · <a href="../../../../foundation-models/2605.16517-gemini-for-google/">实现解读</a> · <a href="#qa-dbddc43401d20e73">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gemini-for-google" data-paper-title="Customizing an LLM for Enterprise Software Engineering" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Customizing an LLM for Enterprise Software Engineering 基础模型 Google 2026-05-15 从企业开发历史中提取高价值代码与交互信号，经过去重、质量过滤和污染控制形成中训练数据；用通用数据回放抑制灾难性遗忘，再做面向内部工具的后训练和部署评测。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  企业 LLM 数据治理 中训练与后训练 基础模型 训练预算：数据配比、目标与优化器 混合 replay 目标里的 λ 两个极端，能帮助检查什么实现错误？ λ=0应只剩企业适配loss，λ=1只剩通用replay loss，可核对混合方向与系数。本地仅执行该目标与不变量，没有Google私有数据、Gemini权重或内部A/B能力。 示意：把λ设为1后仍主要计算企业loss，说明权重方向或数据分支可能写反。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-64bacf05df89aa95">混合 replay 目标里的 λ 两个极端，能帮助检查什么实现错误？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agemini-for-google">Customizing an LLM for Enterprise Software Engineering</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>λ=0应只剩企业适配loss，λ=1只剩通用replay loss，可核对混合方向与系数。本地仅执行该目标与不变量，没有Google私有数据、Gemini权重或内部A/B能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把λ设为1后仍主要计算企业loss，说明权重方向或数据分支可能写反。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16517">原论文</a> · <a href="../../../../foundation-models/2605.16517-gemini-for-google/">实现解读</a> · <a href="#qa-64bacf05df89aa95">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-quality-lsa" data-paper-title="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models 基础模型 University of Southern California / Google Research 2026-03-01 以 in-context 线性回归的权重预测分析预训练与后训练数据协方差。SFT 使用教师中间状态，OS 仅监督最终预测；原文明确 OS 是 outcome-supervised regression，不是包含采样、优势估计和 policy gradient 的完整 RL。§3、§4 给出线性注意力结构及闭式解。 GPT2 多网格、多重复长训练成本过高，不复现（审查 DONE） runner 使用 d=4、6个生成 prompt 的数学诊断，fixture_only: true，没有 benchmark train/test 能力结论。population_initialization、context_embedding、lsa_forward、rollout、sft_loss、outcome_supervision_loss 与 closest_sft_value 可组合执行。自主 rollout 没有真实权重参数，只读取公开任务上下文；训练目标只进入明确命名的训练 loss。  预训练与数据 SFT与outcome supervision理论 基础模型 训练预算：数据配比、目标与优化器 Data Quality LSA 为什么用线性回归来分析预训练与后训练？ 受控线性注意力结构能明确展示数据协方差、初始化和不同监督方式怎样影响权重预测，并给出闭式参考。它是分析模型，不应直接当作完整LLM训练的经验结论。 示意：改变训练任务的协方差，可在小矩阵里单独观察初始化如何影响后续拟合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-data-quality-lsa-d7c7a545" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cde69f54fe549479">Data Quality LSA 为什么用线性回归来分析预训练与后训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-quality-lsa">Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>受控线性注意力结构能明确展示数据协方差、初始化和不同监督方式怎样影响权重预测，并给出闭式参考。它是分析模型，不应直接当作完整LLM训练的经验结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>改变训练任务的协方差，可在小矩阵里单独观察初始化如何影响后续拟合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01293">原论文</a> · <a href="../../../../foundation-models/2603.01293-data-quality-lsa/">实现解读</a> · <a href="#qa-cde69f54fe549479">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-quality-lsa" data-paper-title="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models 基础模型 University of Southern California / Google Research 2026-03-01 以 in-context 线性回归的权重预测分析预训练与后训练数据协方差。SFT 使用教师中间状态，OS 仅监督最终预测；原文明确 OS 是 outcome-supervised regression，不是包含采样、优势估计和 policy gradient 的完整 RL。§3、§4 给出线性注意力结构及闭式解。 GPT2 多网格、多重复长训练成本过高，不复现（审查 DONE） runner 使用 d=4、6个生成 prompt 的数学诊断，fixture_only: true，没有 benchmark train/test 能力结论。population_initialization、context_embedding、lsa_forward、rollout、sft_loss、outcome_supervision_loss 与 closest_sft_value 可组合执行。自主 rollout 没有真实权重参数，只读取公开任务上下文；训练目标只进入明确命名的训练 loss。  预训练与数据 SFT与outcome supervision理论 基础模型 训练预算：数据配比、目标与优化器 这篇数据质量理论里的OS，为什么不能直接称为完整的强化学习后训练？ OS在此指outcome-supervised regression：只监督最终预测，并与使用教师中间状态的SFT对比。线性attention模型与协方差假设让作者能分析闭式关系，但没有完整策略采样、优势估计和policy gradient链路。该理论可帮助理解信息与目标差别，不能被扩成真实LLM RL已得到同样结论。 教学例子：学生只在最后一步的回归权重上计算平方误差，与每一步都对齐教师状态不同；即便前者叫结果监督，也并没有因此出现奖励驱动的策略梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7a5caefc122995f3">这篇数据质量理论里的OS，为什么不能直接称为完整的强化学习后训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-quality-lsa">Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>OS在此指outcome-supervised regression：只监督最终预测，并与使用教师中间状态的SFT对比。线性attention模型与协方差假设让作者能分析闭式关系，但没有完整策略采样、优势估计和policy gradient链路。该理论可帮助理解信息与目标差别，不能被扩成真实LLM RL已得到同样结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生只在最后一步的回归权重上计算平方误差，与每一步都对齐教师状态不同；即便前者叫结果监督，也并没有因此出现奖励驱动的策略梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01293">原论文</a> · <a href="../../../../foundation-models/2603.01293-data-quality-lsa/">实现解读</a> · <a href="#qa-7a5caefc122995f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-quality-lsa" data-paper-title="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models 基础模型 University of Southern California / Google Research 2026-03-01 以 in-context 线性回归的权重预测分析预训练与后训练数据协方差。SFT 使用教师中间状态，OS 仅监督最终预测；原文明确 OS 是 outcome-supervised regression，不是包含采样、优势估计和 policy gradient 的完整 RL。§3、§4 给出线性注意力结构及闭式解。 GPT2 多网格、多重复长训练成本过高，不复现（审查 DONE） runner 使用 d=4、6个生成 prompt 的数学诊断，fixture_only: true，没有 benchmark train/test 能力结论。population_initialization、context_embedding、lsa_forward、rollout、sft_loss、outcome_supervision_loss 与 closest_sft_value 可组合执行。自主 rollout 没有真实权重参数，只读取公开任务上下文；训练目标只进入明确命名的训练 loss。  预训练与数据 SFT与outcome supervision理论 基础模型 训练预算：数据配比、目标与优化器 这项分析中的 SFT 中间状态监督与 OS 最终监督，信息供给有何不同？ SFT使用教师中间权重状态作为训练目标，OS让模型自主rollout后只监督最终预测。两者在训练时可见的轨迹信息不同，OS也不因此自动包含policy gradient等完整RL机制。 示意：一步步给标准中间结果，与只在最后检查预测权重是否接近目标，训练信号不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-127313c1b546145c">这项分析中的 SFT 中间状态监督与 OS 最终监督，信息供给有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-quality-lsa">Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SFT使用教师中间权重状态作为训练目标，OS让模型自主rollout后只监督最终预测。两者在训练时可见的轨迹信息不同，OS也不因此自动包含policy gradient等完整RL机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一步步给标准中间结果，与只在最后检查预测权重是否接近目标，训练信号不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01293">原论文</a> · <a href="../../../../foundation-models/2603.01293-data-quality-lsa/">实现解读</a> · <a href="#qa-127313c1b546145c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-quality-lsa" data-paper-title="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models 基础模型 University of Southern California / Google Research 2026-03-01 以 in-context 线性回归的权重预测分析预训练与后训练数据协方差。SFT 使用教师中间状态，OS 仅监督最终预测；原文明确 OS 是 outcome-supervised regression，不是包含采样、优势估计和 policy gradient 的完整 RL。§3、§4 给出线性注意力结构及闭式解。 GPT2 多网格、多重复长训练成本过高，不复现（审查 DONE） runner 使用 d=4、6个生成 prompt 的数学诊断，fixture_only: true，没有 benchmark train/test 能力结论。population_initialization、context_embedding、lsa_forward、rollout、sft_loss、outcome_supervision_loss 与 closest_sft_value 可组合执行。自主 rollout 没有真实权重参数，只读取公开任务上下文；训练目标只进入明确命名的训练 loss。  预训练与数据 SFT与outcome supervision理论 基础模型 训练预算：数据配比、目标与优化器 为什么自主 rollout 接口不能接收真实任务权重 w*？ 真实权重属于训练loss的监督，传进自主生成会把答案泄漏到被评估路径。文档rollout只读取公开上下文，训练目标进入明确命名的loss；闭式SFT还需保留初始化的零空间分量。 示意：预测下一状态的函数不能先拿到它最终应当恢复的真实权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cb3026ef699d982f">为什么自主 rollout 接口不能接收真实任务权重 w*？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-quality-lsa">Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实权重属于训练loss的监督，传进自主生成会把答案泄漏到被评估路径。文档rollout只读取公开上下文，训练目标进入明确命名的loss；闭式SFT还需保留初始化的零空间分量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预测下一状态的函数不能先拿到它最终应当恢复的真实权重。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01293">原论文</a> · <a href="../../../../foundation-models/2603.01293-data-quality-lsa/">实现解读</a> · <a href="#qa-cb3026ef699d982f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:modular-robust-generative" data-paper-title="A Theoretical Framework for Modular Learning of Robust Generative Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="A Theoretical Framework for Modular Learning of Robust Generative Models 基础模型 Google Research 2026-02-19 以冻结生成专家为基础，优化面对最差数据域的输入相关 gate。核心不是专家均值：逐输入 softmax 不保证整个生成分布积分为一，必须额外约束全局质量。另将非因果教师采样轨迹蒸馏到只读前缀的因果 router。§5.2、§6、§7.3 给出实施过程。 原尺度多专家、多对照、多数据/seed完整 campaign 成本过高，不复现（审查 DONE） runner 为两专家×四结果的生成式数学诊断，显式 fixture_only: true。gated_mass 明确返回未归一化质量；primal_dual_step 执行三方更新；sir_resample 进行实际重要性重采样；cached_router_nll 对冻结缓存训练 router。独立测试覆盖全局约束反例、EG/dual 公式、采样复现、混合概率及梯度隔离。该 API 不自动验证调用方网络的因果性，调用者必须只用前缀产生 router logits。  网络架构 鲁棒模块化生成 基础模型 训练预算：数据配比、目标与优化器 鲁棒生成专家组合为什么要关注最差数据域，而不只优化平均 loss？ 平均分可能掩盖某个域的明显退化。方法用对抗域权重调整输入相关gate，使组合考虑较差域，同时显式处理整个生成分布的质量约束。 示意：三个域中两个很好、一个很差，平均改善不代表最差域已得到保护。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-modular-robust-generative-72932b77" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-141a2b81d1912e50">鲁棒生成专家组合为什么要关注最差数据域，而不只优化平均 loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amodular-robust-generative">A Theoretical Framework for Modular Learning of Robust Generative Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平均分可能掩盖某个域的明显退化。方法用对抗域权重调整输入相关gate，使组合考虑较差域，同时显式处理整个生成分布的质量约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个域中两个很好、一个很差，平均改善不代表最差域已得到保护。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17554">原论文</a> · <a href="../../../../foundation-models/2602.17554-modular-robust-generative/">实现解读</a> · <a href="#qa-141a2b81d1912e50">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:modular-robust-generative" data-paper-title="A Theoretical Framework for Modular Learning of Robust Generative Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="A Theoretical Framework for Modular Learning of Robust Generative Models 基础模型 Google Research 2026-02-19 以冻结生成专家为基础，优化面对最差数据域的输入相关 gate。核心不是专家均值：逐输入 softmax 不保证整个生成分布积分为一，必须额外约束全局质量。另将非因果教师采样轨迹蒸馏到只读前缀的因果 router。§5.2、§6、§7.3 给出实施过程。 原尺度多专家、多对照、多数据/seed完整 campaign 成本过高，不复现（审查 DONE） runner 为两专家×四结果的生成式数学诊断，显式 fixture_only: true。gated_mass 明确返回未归一化质量；primal_dual_step 执行三方更新；sir_resample 进行实际重要性重采样；cached_router_nll 对冻结缓存训练 router。独立测试覆盖全局约束反例、EG/dual 公式、采样复现、混合概率及梯度隔离。该 API 不自动验证调用方网络的因果性，调用者必须只用前缀产生 router logits。  网络架构 鲁棒模块化生成 基础模型 训练预算：数据配比、目标与优化器 生成专家的gate在每个输入上都softmax，为何组合分布仍可能没有归一化？ 若gate随被评价的完整样本变化，它不能像固定混合系数那样移出全局求和；逐输入权重和为1并不保证混合密度对全部样本求和为1。方法因此额外约束总质量，并区分最差域的KL与NLL口径。忽略全局约束，或事后悄悄归一化，都改变了原优化问题。 教学例子：只有A、B两个样本，gate在A处偏向最擅长A的专家，在B处又偏向最擅长B的专家；两处都取到高密度后，总和可能大于1，尽管每处gate都和为1。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8f5d8c105b8e3a12">生成专家的gate在每个输入上都softmax，为何组合分布仍可能没有归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amodular-robust-generative">A Theoretical Framework for Modular Learning of Robust Generative Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若gate随被评价的完整样本变化，它不能像固定混合系数那样移出全局求和；逐输入权重和为1并不保证混合密度对全部样本求和为1。方法因此额外约束总质量，并区分最差域的KL与NLL口径。忽略全局约束，或事后悄悄归一化，都改变了原优化问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只有A、B两个样本，gate在A处偏向最擅长A的专家，在B处又偏向最擅长B的专家；两处都取到高密度后，总和可能大于1，尽管每处gate都和为1。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17554">原论文</a> · <a href="../../../../foundation-models/2602.17554-modular-robust-generative/">实现解读</a> · <a href="#qa-8f5d8c105b8e3a12">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:modular-robust-generative" data-paper-title="A Theoretical Framework for Modular Learning of Robust Generative Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="A Theoretical Framework for Modular Learning of Robust Generative Models 基础模型 Google Research 2026-02-19 以冻结生成专家为基础，优化面对最差数据域的输入相关 gate。核心不是专家均值：逐输入 softmax 不保证整个生成分布积分为一，必须额外约束全局质量。另将非因果教师采样轨迹蒸馏到只读前缀的因果 router。§5.2、§6、§7.3 给出实施过程。 原尺度多专家、多对照、多数据/seed完整 campaign 成本过高，不复现（审查 DONE） runner 为两专家×四结果的生成式数学诊断，显式 fixture_only: true。gated_mass 明确返回未归一化质量；primal_dual_step 执行三方更新；sir_resample 进行实际重要性重采样；cached_router_nll 对冻结缓存训练 router。独立测试覆盖全局约束反例、EG/dual 公式、采样复现、混合概率及梯度隔离。该 API 不自动验证调用方网络的因果性，调用者必须只用前缀产生 router logits。  网络架构 鲁棒模块化生成 基础模型 训练预算：数据配比、目标与优化器 理论域 KL 与实践域 NLL，对 gate 和对抗权重总是等价吗？ 同一域中两者相差与gate无关的域熵，所以gate梯度等价；跨域熵不同时，对抗权重看到的收益排序可能改变。文档默认实践NLL，不能把两种对抗目标静默混用。 示意：两个域预测难度的固有熵不同，减去域熵可能改变哪个域被认为最差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3a09d4a5fe88ce0f">理论域 KL 与实践域 NLL，对 gate 和对抗权重总是等价吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amodular-robust-generative">A Theoretical Framework for Modular Learning of Robust Generative Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一域中两者相差与gate无关的域熵，所以gate梯度等价；跨域熵不同时，对抗权重看到的收益排序可能改变。文档默认实践NLL，不能把两种对抗目标静默混用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个域预测难度的固有熵不同，减去域熵可能改变哪个域被认为最差。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17554">原论文</a> · <a href="../../../../foundation-models/2602.17554-modular-robust-generative/">实现解读</a> · <a href="#qa-3a09d4a5fe88ce0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:modular-robust-generative" data-paper-title="A Theoretical Framework for Modular Learning of Robust Generative Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="A Theoretical Framework for Modular Learning of Robust Generative Models 基础模型 Google Research 2026-02-19 以冻结生成专家为基础，优化面对最差数据域的输入相关 gate。核心不是专家均值：逐输入 softmax 不保证整个生成分布积分为一，必须额外约束全局质量。另将非因果教师采样轨迹蒸馏到只读前缀的因果 router。§5.2、§6、§7.3 给出实施过程。 原尺度多专家、多对照、多数据/seed完整 campaign 成本过高，不复现（审查 DONE） runner 为两专家×四结果的生成式数学诊断，显式 fixture_only: true。gated_mass 明确返回未归一化质量；primal_dual_step 执行三方更新；sir_resample 进行实际重要性重采样；cached_router_nll 对冻结缓存训练 router。独立测试覆盖全局约束反例、EG/dual 公式、采样复现、混合概率及梯度隔离。该 API 不自动验证调用方网络的因果性，调用者必须只用前缀产生 router logits。  网络架构 鲁棒模块化生成 基础模型 训练预算：数据配比、目标与优化器 从非因果教师轨迹蒸馏 router 时，为什么缓存目标不能直接作为 router 输入？ 教师缓存可用于训练目标，但因果router的logits必须只由前缀产生；否则把未来信息泄漏到路由。文档API不自动证明调用方网络因果，调用者还需独立检查这一边界。 示意：训练时知道目标token的专家概率，不代表推理路由器可以提前看到目标token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-844919d92c1ac5cd">从非因果教师轨迹蒸馏 router 时，为什么缓存目标不能直接作为 router 输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amodular-robust-generative">A Theoretical Framework for Modular Learning of Robust Generative Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师缓存可用于训练目标，但因果router的logits必须只由前缀产生；否则把未来信息泄漏到路由。文档API不自动证明调用方网络因果，调用者还需独立检查这一边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时知道目标token的专家概率，不代表推理路由器可以提前看到目标token。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17554">原论文</a> · <a href="../../../../foundation-models/2602.17554-modular-robust-generative/">实现解读</a> · <a href="#qa-844919d92c1ac5cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:eco-optimizer" data-paper-title="ECO: Quantized Training without Full-Precision Master Weights" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="ECO: Quantized Training without Full-Precision Master Weights 基础模型 Google Research / ISTA 2026-01-29 低精度训练通常仍保留高精度 master weights 累积微小更新。ECO 直接在量化权重上更新，将本次重量化误差注入已有动量，避免再保存主权重或持久误差缓冲；Adam 必须使用逐元素有效步长，不能把 SGDM 的标量系数照搬过去。图按原文 Algorithm 1–3 重绘。原文算法及 Figure 1。 成本过高，不复现（审查 DONE）。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.2 按参数量训练个 C4 token，最低 30M 配置也为 3B token；另有 Gemma-3 1B、2.1B MoE 预训练及 DeepSeek-MoE-16B 微调。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。  预训练与数据 优化器与训练稳定性 基础模型 训练预算：数据配比、目标与优化器 ECO 为什么希望同时移除 master weights 和独立误差缓冲？ 低精度训练若仍保存高精度主权重或额外误差状态，存储优势会受限。ECO把重量化误差补入已有动量，尝试在不增加这些持久状态的条件下累积微小更新。 示意：很小的更新本次未改变低精度权重，也不应因此永远丢失其影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-eco-optimizer-dd39c986" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5b12a29e43a1976d">ECO 为什么希望同时移除 master weights 和独立误差缓冲？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aeco-optimizer">ECO: Quantized Training without Full-Precision Master Weights</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / ISTA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>低精度训练若仍保存高精度主权重或额外误差状态，存储优势会受限。ECO把重量化误差补入已有动量，尝试在不增加这些持久状态的条件下累积微小更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>很小的更新本次未改变低精度权重，也不应因此永远丢失其影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.22101v1">原论文</a> · <a href="../../../../foundation-models/2601.22101-eco-optimizer/">实现解读</a> · <a href="#qa-5b12a29e43a1976d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:eco-optimizer" data-paper-title="ECO: Quantized Training without Full-Precision Master Weights" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="ECO: Quantized Training without Full-Precision Master Weights 基础模型 Google Research / ISTA 2026-01-29 低精度训练通常仍保留高精度 master weights 累积微小更新。ECO 直接在量化权重上更新，将本次重量化误差注入已有动量，避免再保存主权重或持久误差缓冲；Adam 必须使用逐元素有效步长，不能把 SGDM 的标量系数照搬过去。图按原文 Algorithm 1–3 重绘。原文算法及 Figure 1。 成本过高，不复现（审查 DONE）。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.2 按参数量训练个 C4 token，最低 30M 配置也为 3B token；另有 Gemma-3 1B、2.1B MoE 预训练及 DeepSeek-MoE-16B 微调。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。  预训练与数据 优化器与训练稳定性 基础模型 训练预算：数据配比、目标与优化器 ECO去掉高精度master weights后，微小更新被量化吃掉的问题怎样处理？ 它直接更新量化权重，并把本次重量化误差反馈到已有动量，避免额外保存主权重或独立误差缓冲。补偿系数与优化器步长相关；Adam的有效步长逐元素变化，不能照搬SGDM标量系数。无额外缓冲规则还有推导近似，不能说每一步都与高精度轨迹精确等价。 教学例子：一次更新小于量化网格，权重暂时没变；误差信息进入动量，影响后续更新，而不是凭空丢掉或另外保存一整份高精度权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-60e5874d502e6a0b">ECO去掉高精度master weights后，微小更新被量化吃掉的问题怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aeco-optimizer">ECO: Quantized Training without Full-Precision Master Weights</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / ISTA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它直接更新量化权重，并把本次重量化误差反馈到已有动量，避免额外保存主权重或独立误差缓冲。补偿系数与优化器步长相关；Adam的有效步长逐元素变化，不能照搬SGDM标量系数。无额外缓冲规则还有推导近似，不能说每一步都与高精度轨迹精确等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次更新小于量化网格，权重暂时没变；误差信息进入动量，影响后续更新，而不是凭空丢掉或另外保存一整份高精度权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.22101v1">原论文</a> · <a href="../../../../foundation-models/2601.22101-eco-optimizer/">实现解读</a> · <a href="#qa-60e5874d502e6a0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:eco-optimizer" data-paper-title="ECO: Quantized Training without Full-Precision Master Weights" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="ECO: Quantized Training without Full-Precision Master Weights 基础模型 Google Research / ISTA 2026-01-29 低精度训练通常仍保留高精度 master weights 累积微小更新。ECO 直接在量化权重上更新，将本次重量化误差注入已有动量，避免再保存主权重或持久误差缓冲；Adam 必须使用逐元素有效步长，不能把 SGDM 的标量系数照搬过去。图按原文 Algorithm 1–3 重绘。原文算法及 Figure 1。 成本过高，不复现（审查 DONE）。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.2 按参数量训练个 C4 token，最低 30M 配置也为 3B token；另有 Gemma-3 1B、2.1B MoE 预训练及 DeepSeek-MoE-16B 微调。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。  预训练与数据 优化器与训练稳定性 基础模型 训练预算：数据配比、目标与优化器 ECO 的无缓冲动量补偿，与保存完整前后量化误差的精确等价规则相同吗？ 不相同。文档说明无额外缓冲形式由相邻误差接近的观察推导，并另有收敛分析；不能把它写成任意量化条件下逐步严格等价于高精度训练。 示意：两步量化误差差异很大时，不能仅凭公式形似就宣称与保存所有误差完全相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3275fe9870f05c43">ECO 的无缓冲动量补偿，与保存完整前后量化误差的精确等价规则相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aeco-optimizer">ECO: Quantized Training without Full-Precision Master Weights</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / ISTA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不相同。文档说明无额外缓冲形式由相邻误差接近的观察推导，并另有收敛分析；不能把它写成任意量化条件下逐步严格等价于高精度训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两步量化误差差异很大时，不能仅凭公式形似就宣称与保存所有误差完全相同。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.22101v1">原论文</a> · <a href="../../../../foundation-models/2601.22101-eco-optimizer/">实现解读</a> · <a href="#qa-3275fe9870f05c43">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:eco-optimizer" data-paper-title="ECO: Quantized Training without Full-Precision Master Weights" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="ECO: Quantized Training without Full-Precision Master Weights 基础模型 Google Research / ISTA 2026-01-29 低精度训练通常仍保留高精度 master weights 累积微小更新。ECO 直接在量化权重上更新，将本次重量化误差注入已有动量，避免再保存主权重或持久误差缓冲；Adam 必须使用逐元素有效步长，不能把 SGDM 的标量系数照搬过去。图按原文 Algorithm 1–3 重绘。原文算法及 Figure 1。 成本过高，不复现（审查 DONE）。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.2 按参数量训练个 C4 token，最低 30M 配置也为 3B token；另有 Gemma-3 1B、2.1B MoE 预训练及 DeepSeek-MoE-16B 微调。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。  预训练与数据 优化器与训练稳定性 基础模型 训练预算：数据配比、目标与优化器 把 ECO 从 SGDM 移到 Adam 时，为什么不能沿用一个标量学习率做补偿？ Adam的偏置修正与第二矩产生逐元素有效步长η_t，误差注入需使用这一尺度。直接照搬SGDM标量系数会对不同坐标补偿失配；量化格式与缩放粒度也必须记录。 示意：两个坐标预条件步长不同，同样的量化误差不能都除以同一个标量来补偿。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-77c5b857c061e0e0">把 ECO 从 SGDM 移到 Adam 时，为什么不能沿用一个标量学习率做补偿？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aeco-optimizer">ECO: Quantized Training without Full-Precision Master Weights</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / ISTA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Adam的偏置修正与第二矩产生逐元素有效步长η_t，误差注入需使用这一尺度。直接照搬SGDM标量系数会对不同坐标补偿失配；量化格式与缩放粒度也必须记录。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个坐标预条件步长不同，同样的量化误差不能都除以同一个标量来补偿。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.22101v1">原论文</a> · <a href="../../../../foundation-models/2601.22101-eco-optimizer/">实现解读</a> · <a href="#qa-77c5b857c061e0e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:me-pois" data-paper-title="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement 基础模型 University of Southern California 2026-01-29 原方法用访问序列编码器连接短期轨迹与长期地点原型，并把高频地点的时段分布跨空间尺度传给稀疏地点；文本语义作为另一条对齐监督。冻结预训练表征后，再训练地图属性探针。主要机制与公式见原文 §3.2–3.6。 阻碍是付费/私有移动数据、SafeGraph 与 Maps 标签及完整多 embedding 组合，因此完整实验不复现，不进入自动重试队列。当前仅为 L0/L1 公式与梯度诊断，无 validation/test 能力结论。实现 transferred_visit_distribution、prototype_contrastive_loss、distribution_kl_sum 和 MobilityPrototypeLoss。接口要求调用方提供真实访问编码及文本特征；没有用随机向量冒充轨迹编码器。  预训练与数据 地理位置表征 基础模型 训练预算：数据配比、目标与优化器 ME-POIs 为什么把访问轨迹、地点原型和文本监督放在一起？ 稀疏地点缺少充足访问记录。方法将短期轨迹与长期地点原型连接，并从高频锚点跨空间尺度传递时段信息，再借文本语义对齐补充监督。 示意：一个少有人到访的地点，可从附近高频地点的时段模式获得辅助信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-me-pois-4510ed6c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-199f83ffcd54bde6">ME-POIs 为什么把访问轨迹、地点原型和文本监督放在一起？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ame-pois">Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>稀疏地点缺少充足访问记录。方法将短期轨迹与长期地点原型连接，并从高频锚点跨空间尺度传递时段信息，再借文本语义对齐补充监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个少有人到访的地点，可从附近高频地点的时段模式获得辅助信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21149">原论文</a> · <a href="../../../../foundation-models/2601.21149-me-pois/">实现解读</a> · <a href="#qa-199f83ffcd54bde6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:me-pois" data-paper-title="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement 基础模型 University of Southern California 2026-01-29 原方法用访问序列编码器连接短期轨迹与长期地点原型，并把高频地点的时段分布跨空间尺度传给稀疏地点；文本语义作为另一条对齐监督。冻结预训练表征后，再训练地图属性探针。主要机制与公式见原文 §3.2–3.6。 阻碍是付费/私有移动数据、SafeGraph 与 Maps 标签及完整多 embedding 组合，因此完整实验不复现，不进入自动重试队列。当前仅为 L0/L1 公式与梯度诊断，无 validation/test 能力结论。实现 transferred_visit_distribution、prototype_contrastive_loss、distribution_kl_sum 和 MobilityPrototypeLoss。接口要求调用方提供真实访问编码及文本特征；没有用随机向量冒充轨迹编码器。  预训练与数据 地理位置表征 基础模型 训练预算：数据配比、目标与优化器 ME-POIs怎样给访问稀少的地点补充时段信息，为什么不能把所有尺度锚点一锅归一化？ 它借助高频地点的时段分布，在每个空间尺度内部先按距离对锚点归一化，再在尺度间平均，避免某个尺度只因锚点多就主导结果。轨迹编码连接短期访问与长期地点原型，文本另作语义对齐。行为时段、地点语义与冻结后的属性探针各有角色，不能混作一个标签。 教学例子：小尺度有2个近邻锚点，大尺度有20个；先各自归一化再平均，可让尺度贡献按设计组合，而不是让大尺度仅凭数量多就压过近邻信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f585319aed43d6d3">ME-POIs怎样给访问稀少的地点补充时段信息，为什么不能把所有尺度锚点一锅归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ame-pois">Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它借助高频地点的时段分布，在每个空间尺度内部先按距离对锚点归一化，再在尺度间平均，避免某个尺度只因锚点多就主导结果。轨迹编码连接短期访问与长期地点原型，文本另作语义对齐。行为时段、地点语义与冻结后的属性探针各有角色，不能混作一个标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>小尺度有2个近邻锚点，大尺度有20个；先各自归一化再平均，可让尺度贡献按设计组合，而不是让大尺度仅凭数量多就压过近邻信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21149">原论文</a> · <a href="../../../../foundation-models/2601.21149-me-pois/">实现解读</a> · <a href="#qa-f585319aed43d6d3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:me-pois" data-paper-title="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement 基础模型 University of Southern California 2026-01-29 原方法用访问序列编码器连接短期轨迹与长期地点原型，并把高频地点的时段分布跨空间尺度传给稀疏地点；文本语义作为另一条对齐监督。冻结预训练表征后，再训练地图属性探针。主要机制与公式见原文 §3.2–3.6。 阻碍是付费/私有移动数据、SafeGraph 与 Maps 标签及完整多 embedding 组合，因此完整实验不复现，不进入自动重试队列。当前仅为 L0/L1 公式与梯度诊断，无 validation/test 能力结论。实现 transferred_visit_distribution、prototype_contrastive_loss、distribution_kl_sum 和 MobilityPrototypeLoss。接口要求调用方提供真实访问编码及文本特征；没有用随机向量冒充轨迹编码器。  预训练与数据 地理位置表征 基础模型 训练预算：数据配比、目标与优化器 按每个空间尺度分别归一化再平均，与所有锚点混成一个 softmax 有何差异？ 分尺度归一化让每个尺度形成自身的锚点分布，再按规定平均；混池会让不同尺度的权重直接竞争，改变每个尺度的贡献，不能视为相同的多尺度传递。 示意：近邻尺度与远邻尺度各给一份预测，而不是因某尺度候选多就占更大总质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6858af52ff4ef838">按每个空间尺度分别归一化再平均，与所有锚点混成一个 softmax 有何差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ame-pois">Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分尺度归一化让每个尺度形成自身的锚点分布，再按规定平均；混池会让不同尺度的权重直接竞争，改变每个尺度的贡献，不能视为相同的多尺度传递。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>近邻尺度与远邻尺度各给一份预测，而不是因某尺度候选多就占更大总质量。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21149">原论文</a> · <a href="../../../../foundation-models/2601.21149-me-pois/">实现解读</a> · <a href="#qa-6858af52ff4ef838">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:me-pois" data-paper-title="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement 基础模型 University of Southern California 2026-01-29 原方法用访问序列编码器连接短期轨迹与长期地点原型，并把高频地点的时段分布跨空间尺度传给稀疏地点；文本语义作为另一条对齐监督。冻结预训练表征后，再训练地图属性探针。主要机制与公式见原文 §3.2–3.6。 阻碍是付费/私有移动数据、SafeGraph 与 Maps 标签及完整多 embedding 组合，因此完整实验不复现，不进入自动重试队列。当前仅为 L0/L1 公式与梯度诊断，无 validation/test 能力结论。实现 transferred_visit_distribution、prototype_contrastive_loss、distribution_kl_sum 和 MobilityPrototypeLoss。接口要求调用方提供真实访问编码及文本特征；没有用随机向量冒充轨迹编码器。  预训练与数据 地理位置表征 基础模型 训练预算：数据配比、目标与优化器 ME-POIs 的对比负例应按访问记录数量重复加入同一地点吗？ 文档Eq.9使用minibatch中不重复的地点原型。重复访问同一地点不应凭数量变成多个独立原型负例；时段KL还需保持r||q方向与对地点求和的口径。 示意：同一POI出现三次访问，原型候选集合中仍只保留一个该POI。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7e4f3a1b6f155b38">ME-POIs 的对比负例应按访问记录数量重复加入同一地点吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ame-pois">Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档Eq.9使用minibatch中不重复的地点原型。重复访问同一地点不应凭数量变成多个独立原型负例；时段KL还需保持r||q方向与对地点求和的口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一POI出现三次访问，原型候选集合中仍只保留一个该POI。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21149">原论文</a> · <a href="../../../../foundation-models/2601.21149-me-pois/">实现解读</a> · <a href="#qa-7e4f3a1b6f155b38">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon" data-paper-title="Muon is Scalable for LLM Training" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Muon is Scalable for LLM Training 基础模型 Moonshot AI / UCLA 2025-02-24 AdamW 把矩阵参数当作独立标量更新，Muon 则把隐藏层梯度视为矩阵，通过 momentum 与 Newton–Schulz 近似极分解得到正交化更新方向。论文为大规模训练补上 weight decay 和按参数形状缩放；非隐藏矩阵参数继续使用 AdamW。 Fidelity: 核心机制复现。隐藏层二维矩阵使用 Muon，embedding、norm、bias 与输出参数保留 AdamW。未复刻分布式 optimizer state、通信优化、3B/16B MoE 和 5.7T-token compute frontier；本地结论只说明算法路径正确运行，不支持 2× 效率在小模型复现。本地对照口径：基线和实验组结构、参数量、数据与 30-step 预算完全相同，只把 AdamW 换为 Muon；WikiText-2 LM loss 5.7471→5.8016，相对 +0.95%（更差），PPL 相对 +5.61%。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 Muon 为什么把隐藏矩阵的更新方向看成一个矩阵几何问题？ 隐藏权重各坐标共同构成线性映射，Muon用动量矩阵的近似polar方向组织更新，而非只逐坐标调尺度。它关注更新方向的谱结构，并配合形状缩放及weight decay。 示意：矩阵中一个相关方向很强时，处理整张矩阵与给每个元素独立调步长不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-muon-e884dc79" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8161dcd10e677583">Muon 为什么把隐藏矩阵的更新方向看成一个矩阵几何问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon">Muon is Scalable for LLM Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI / UCLA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>隐藏权重各坐标共同构成线性映射，Muon用动量矩阵的近似polar方向组织更新，而非只逐坐标调尺度。它关注更新方向的谱结构，并配合形状缩放及weight decay。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>矩阵中一个相关方向很强时，处理整张矩阵与给每个元素独立调步长不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16982">原论文</a> · <a href="../../../../reproductions/2502.16982-muon/">实现解读</a> · <a href="#qa-8161dcd10e677583">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon" data-paper-title="Muon is Scalable for LLM Training" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Muon is Scalable for LLM Training 基础模型 Moonshot AI / UCLA 2025-02-24 AdamW 把矩阵参数当作独立标量更新，Muon 则把隐藏层梯度视为矩阵，通过 momentum 与 Newton–Schulz 近似极分解得到正交化更新方向。论文为大规模训练补上 weight decay 和按参数形状缩放；非隐藏矩阵参数继续使用 AdamW。 Fidelity: 核心机制复现。隐藏层二维矩阵使用 Muon，embedding、norm、bias 与输出参数保留 AdamW。未复刻分布式 optimizer state、通信优化、3B/16B MoE 和 5.7T-token compute frontier；本地结论只说明算法路径正确运行，不支持 2× 效率在小模型复现。本地对照口径：基线和实验组结构、参数量、数据与 30-step 预算完全相同，只把 AdamW 换为 Muon；WikiText-2 LM loss 5.7471→5.8016，相对 +0.95%（更差），PPL 相对 +5.61%。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 Muon为什么把梯度当矩阵处理，而不是像AdamW那样逐坐标调步长？ 它对带动量的隐藏矩阵梯度做近似极分解，调整更新的谱几何，再配合权重衰减与形状缩放。处理对象是矩阵整体的方向关系，不只是每个标量自己的二阶矩。论文大规模方案对非隐藏矩阵参数仍使用AdamW，因此不能把整个训练器简单写成所有张量都调用同一个正交化函数。 教学例子：两列梯度几乎共线，逐坐标缩放与矩阵极分解会给出不同更新方向；词表或一维参数是否适合该规则，也需要按论文参数分工处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-93b41ee941026af3">Muon为什么把梯度当矩阵处理，而不是像AdamW那样逐坐标调步长？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon">Muon is Scalable for LLM Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI / UCLA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它对带动量的隐藏矩阵梯度做近似极分解，调整更新的谱几何，再配合权重衰减与形状缩放。处理对象是矩阵整体的方向关系，不只是每个标量自己的二阶矩。论文大规模方案对非隐藏矩阵参数仍使用AdamW，因此不能把整个训练器简单写成所有张量都调用同一个正交化函数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两列梯度几乎共线，逐坐标缩放与矩阵极分解会给出不同更新方向；词表或一维参数是否适合该规则，也需要按论文参数分工处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16982">原论文</a> · <a href="../../../../reproductions/2502.16982-muon/">实现解读</a> · <a href="#qa-93b41ee941026af3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon" data-paper-title="Muon is Scalable for LLM Training" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Muon is Scalable for LLM Training 基础模型 Moonshot AI / UCLA 2025-02-24 AdamW 把矩阵参数当作独立标量更新，Muon 则把隐藏层梯度视为矩阵，通过 momentum 与 Newton–Schulz 近似极分解得到正交化更新方向。论文为大规模训练补上 weight decay 和按参数形状缩放；非隐藏矩阵参数继续使用 AdamW。 Fidelity: 核心机制复现。隐藏层二维矩阵使用 Muon，embedding、norm、bias 与输出参数保留 AdamW。未复刻分布式 optimizer state、通信优化、3B/16B MoE 和 5.7T-token compute frontier；本地结论只说明算法路径正确运行，不支持 2× 效率在小模型复现。本地对照口径：基线和实验组结构、参数量、数据与 30-step 预算完全相同，只把 AdamW 换为 Muon；WikiText-2 LM loss 5.7471→5.8016，相对 +0.95%（更差），PPL 相对 +5.61%。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 本地 Muon 与“所有参数都使用同一个 Muon 更新”有什么差别？ 文档对hidden矩阵走Muon，对embedding、norm、bias和head等非隐藏参数继续使用AdamW。混合优化器身份是比较的一部分，不能忽略辅助AdamW后声称完全替代。 示意：一维norm参数并不适合直接套用矩阵Newton–Schulz迭代。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d6c646312821684c">本地 Muon 与“所有参数都使用同一个 Muon 更新”有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon">Muon is Scalable for LLM Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI / UCLA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档对hidden矩阵走Muon，对embedding、norm、bias和head等非隐藏参数继续使用AdamW。混合优化器身份是比较的一部分，不能忽略辅助AdamW后声称完全替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一维norm参数并不适合直接套用矩阵Newton–Schulz迭代。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16982">原论文</a> · <a href="../../../../reproductions/2502.16982-muon/">实现解读</a> · <a href="#qa-d6c646312821684c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon" data-paper-title="Muon is Scalable for LLM Training" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Muon is Scalable for LLM Training 基础模型 Moonshot AI / UCLA 2025-02-24 AdamW 把矩阵参数当作独立标量更新，Muon 则把隐藏层梯度视为矩阵，通过 momentum 与 Newton–Schulz 近似极分解得到正交化更新方向。论文为大规模训练补上 weight decay 和按参数形状缩放；非隐藏矩阵参数继续使用 AdamW。 Fidelity: 核心机制复现。隐藏层二维矩阵使用 Muon，embedding、norm、bias 与输出参数保留 AdamW。未复刻分布式 optimizer state、通信优化、3B/16B MoE 和 5.7T-token compute frontier；本地结论只说明算法路径正确运行，不支持 2× 效率在小模型复现。本地对照口径：基线和实验组结构、参数量、数据与 30-step 预算完全相同，只把 AdamW 换为 Muon；WikiText-2 LM loss 5.7471→5.8016，相对 +0.95%（更差），PPL 相对 +5.61%。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 Muon 的 Newton–Schulz 输入为什么先除以 Frobenius 范数？ 归一化控制迭代输入尺度，再按给定多项式系数近似polar方向；还需处理零或极小范数，并保留形状相关缩放。只做归一化或只报正交误差，都不能替代真实优化效果与耗时测量。 示意：把同一梯度整体放大很多倍，不应直接让迭代落到完全不同的数值尺度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8a7420cefbab4d10">Muon 的 Newton–Schulz 输入为什么先除以 Frobenius 范数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon">Muon is Scalable for LLM Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI / UCLA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>归一化控制迭代输入尺度，再按给定多项式系数近似polar方向；还需处理零或极小范数，并保留形状相关缩放。只做归一化或只报正交误差，都不能替代真实优化效果与耗时测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把同一梯度整体放大很多倍，不应直接让迭代落到完全不同的数值尺度。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16982">原论文</a> · <a href="../../../../reproductions/2502.16982-muon/">实现解读</a> · <a href="#qa-8a7420cefbab4d10">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-mixing-laws" data-paper-title="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance 基础模型 University of Cambridge / Shanghai AI Laboratory 2024-03-25 先训练多组小预算 domain mixture，拟合各评测域的混合缩放律，再搜索未训练过的最优配比。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际用公开文本域的十组 pilot mixture 拟合逐域指数 mixing law，并在未训练配比网格上选择最优配比；小型 unigram proxy 不等同于 RedPajama 多模型 scaling curve。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 data-mixing-laws；相对 validation loss -3.48%。  pretraining-data scaling-law data-mixture 基础模型 训练预算：数据配比、目标与优化器 Data Mixing Laws 为什么先花小预算训练多组数据配比？ 这些pilot实验为各评测域的性能预测提供观测，再拟合配比与训练规模的关系。目标是减少每个候选都完整训练的成本，但预测依赖pilot覆盖与模型假设。 示意：先试十组小配比，再用拟合曲线筛选其它候选，而非把未训练点当成实测结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-data-mixing-laws-e8c71fa2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-345a9b000888cf40">Data Mixing Laws 为什么先花小预算训练多组数据配比？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-mixing-laws">Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge / Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这些pilot实验为各评测域的性能预测提供观测，再拟合配比与训练规模的关系。目标是减少每个候选都完整训练的成本，但预测依赖pilot覆盖与模型假设。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先试十组小配比，再用拟合曲线筛选其它候选，而非把未训练点当成实测结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.16952">原论文</a> · <a href="../../../../reproductions/2403.16952-data-mixing-laws/">实现解读</a> · <a href="#qa-345a9b000888cf40">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-mixing-laws" data-paper-title="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance 基础模型 University of Cambridge / Shanghai AI Laboratory 2024-03-25 先训练多组小预算 domain mixture，拟合各评测域的混合缩放律，再搜索未训练过的最优配比。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际用公开文本域的十组 pilot mixture 拟合逐域指数 mixing law，并在未训练配比网格上选择最优配比；小型 unigram proxy 不等同于 RedPajama 多模型 scaling curve。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 data-mixing-laws；相对 validation loss -3.48%。  pretraining-data scaling-law data-mixture 基础模型 训练预算：数据配比、目标与优化器 Data Mixing Laws怎样搜索没真正训练过的数据配比，依据又有什么限制？ 先用多组小预算混合训练观察各评测域损失，再拟合配比、规模与性能关系，最后在拟合模型上搜索目标加权最优配比。省掉的是穷举每个大预算配方的成本，预测可靠性仍取决于试验覆盖和拟合假设；验证选择不能使用最终测试结果反复调配。 教学例子：已经测过代码占比20%、50%、80%的小模型，可预测中间配比的表现，再选择少量候选验证；不能把曲线预测值直接当成该大模型配方的实测成绩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8a72a4e046d49e6c">Data Mixing Laws怎样搜索没真正训练过的数据配比，依据又有什么限制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-mixing-laws">Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge / Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先用多组小预算混合训练观察各评测域损失，再拟合配比、规模与性能关系，最后在拟合模型上搜索目标加权最优配比。省掉的是穷举每个大预算配方的成本，预测可靠性仍取决于试验覆盖和拟合假设；验证选择不能使用最终测试结果反复调配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>已经测过代码占比20%、50%、80%的小模型，可预测中间配比的表现，再选择少量候选验证；不能把曲线预测值直接当成该大模型配方的实测成绩。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.16952">原论文</a> · <a href="../../../../reproductions/2403.16952-data-mixing-laws/">实现解读</a> · <a href="#qa-8a72a4e046d49e6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-mixing-laws" data-paper-title="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance 基础模型 University of Cambridge / Shanghai AI Laboratory 2024-03-25 先训练多组小预算 domain mixture，拟合各评测域的混合缩放律，再搜索未训练过的最优配比。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际用公开文本域的十组 pilot mixture 拟合逐域指数 mixing law，并在未训练配比网格上选择最优配比；小型 unigram proxy 不等同于 RedPajama 多模型 scaling curve。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 data-mixing-laws；相对 validation loss -3.48%。  pretraining-data scaling-law data-mixture 基础模型 训练预算：数据配比、目标与优化器 拟合 mixing law 搜索配比，与对每个配比直接训练评测，有何证据差别？ 前者在未训练点使用模型预测，节省试验但引入拟合与外推误差；后者给出对应配置实测，成本更高。预测最优仍需独立实验复核，不能把曲线最小值直接写成已测收益。 示意：预测某个70/30组合最好，不等于该组合已经完成目标规模训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b7de02f902644429">拟合 mixing law 搜索配比，与对每个配比直接训练评测，有何证据差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-mixing-laws">Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge / Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者在未训练点使用模型预测，节省试验但引入拟合与外推误差；后者给出对应配置实测，成本更高。预测最优仍需独立实验复核，不能把曲线最小值直接写成已测收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预测某个70/30组合最好，不等于该组合已经完成目标规模训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.16952">原论文</a> · <a href="../../../../reproductions/2403.16952-data-mixing-laws/">实现解读</a> · <a href="#qa-b7de02f902644429">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-mixing-laws" data-paper-title="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance 基础模型 University of Cambridge / Shanghai AI Laboratory 2024-03-25 先训练多组小预算 domain mixture，拟合各评测域的混合缩放律，再搜索未训练过的最优配比。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际用公开文本域的十组 pilot mixture 拟合逐域指数 mixing law，并在未训练配比网格上选择最优配比；小型 unigram proxy 不等同于 RedPajama 多模型 scaling curve。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 data-mixing-laws；相对 validation loss -3.48%。  pretraining-data scaling-law data-mixture 基础模型 训练预算：数据配比、目标与优化器 搜索数据混合时，怎样避免把 test 目标写进配比选择？ 拟合、域权重和候选选择需使用预先规定的训练/validation协议，最终才测test；配比还必须满足非负与总和为1。本地unigram proxy不是RedPajama多模型缩放曲线，边界需保留。 示意：不能看完test各域损失后，再调整w_i直到同一test上的加权分数最好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5c41aafffdf87cb9">搜索数据混合时，怎样避免把 test 目标写进配比选择？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-mixing-laws">Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge / Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>拟合、域权重和候选选择需使用预先规定的训练/validation协议，最终才测test；配比还必须满足非负与总和为1。本地unigram proxy不是RedPajama多模型缩放曲线，边界需保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>不能看完test各域损失后，再调整w_i直到同一test上的加权分数最好。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.16952">原论文</a> · <a href="../../../../reproductions/2403.16952-data-mixing-laws/">实现解读</a> · <a href="#qa-5c41aafffdf87cb9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doremi" data-paper-title="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining 基础模型 Stanford University / Google Research 2023-05-17 用小型 proxy model 的 excess loss 做 group DRO，动态提升欠拟合域权重，再按所得配比训练目标模型。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在两个公开文本域上训练 reference unigram proxy，执行 group-DRO excess-loss 指数权重更新，再以所学配比评估；未复刻 The Pile、280M proxy 与 8B target。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 doremi；相对 validation loss -0.15%。  pretraining-data data-mixture group-dro 基础模型 训练预算：数据配比、目标与优化器 DoReMi 为什么用小 proxy 来学习目标模型的数据配比？ 大模型反复试配比成本高。DoReMi先在小proxy上以excess loss做group DRO，动态调整域权重，再把所得配比用于目标训练；proxy到目标的迁移仍需验证。 示意：先用较小试验判断哪些域相对reference欠拟合，再分配昂贵目标训练的数据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-doremi-7bfdfa8e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6091e34a90a5668b">DoReMi 为什么用小 proxy 来学习目标模型的数据配比？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoremi">DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大模型反复试配比成本高。DoReMi先在小proxy上以excess loss做group DRO，动态调整域权重，再把所得配比用于目标训练；proxy到目标的迁移仍需验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先用较小试验判断哪些域相对reference欠拟合，再分配昂贵目标训练的数据。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10429">原论文</a> · <a href="../../../../reproductions/2305.10429-doremi/">实现解读</a> · <a href="#qa-6091e34a90a5668b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doremi" data-paper-title="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining 基础模型 Stanford University / Google Research 2023-05-17 用小型 proxy model 的 excess loss 做 group DRO，动态提升欠拟合域权重，再按所得配比训练目标模型。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在两个公开文本域上训练 reference unigram proxy，执行 group-DRO excess-loss 指数权重更新，再以所学配比评估；未复刻 The Pile、280M proxy 与 8B target。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 doremi；相对 validation loss -0.15%。  pretraining-data data-mixture group-dro 基础模型 训练预算：数据配比、目标与优化器 DoReMi为什么提高excess loss较大的域，而不是直接追最高原始loss的域？ 原始loss同时反映任务固有难度和当前欠拟合；减去参考模型的域损失后，excess loss更关注相对参考仍未学好的部分。小proxy通过group DRO学习域配比，再把配比交给目标模型训练。得到的是特定数据和参考下的资源分配，不能把高熵域天然难预测误当成它总该拿最多预算。 教学例子：A域原始loss为5、参考为4.9，B域为3、参考为2；前者虽绝对更难，B相对参考的缺口却更大，权重更新会区分这两种情况。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-82c48593bd66c5dc">DoReMi为什么提高excess loss较大的域，而不是直接追最高原始loss的域？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoremi">DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始loss同时反映任务固有难度和当前欠拟合；减去参考模型的域损失后，excess loss更关注相对参考仍未学好的部分。小proxy通过group DRO学习域配比，再把配比交给目标模型训练。得到的是特定数据和参考下的资源分配，不能把高熵域天然难预测误当成它总该拿最多预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A域原始loss为5、参考为4.9，B域为3、参考为2；前者虽绝对更难，B相对参考的缺口却更大，权重更新会区分这两种情况。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10429">原论文</a> · <a href="../../../../reproductions/2305.10429-doremi/">实现解读</a> · <a href="#qa-82c48593bd66c5dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doremi" data-paper-title="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining 基础模型 Stanford University / Google Research 2023-05-17 用小型 proxy model 的 excess loss 做 group DRO，动态提升欠拟合域权重，再按所得配比训练目标模型。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在两个公开文本域上训练 reference unigram proxy，执行 group-DRO excess-loss 指数权重更新，再以所学配比评估；未复刻 The Pile、280M proxy 与 8B target。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 doremi；相对 validation loss -0.15%。  pretraining-data data-mixture group-dro 基础模型 训练预算：数据配比、目标与优化器 DoReMi 的动态权重更新，与从头到尾均匀采样有什么不同？ 均匀采样保持域概率不变；DoReMi按各域相对reference的excess loss指数调整并归一化，回应训练中的相对欠拟合。它并不是对原始loss最高的域无条件加权。 示意：两个域原始loss都高，但其中一个reference本来就难，excess loss可区分这两种情形。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-395b5c5a3e6e732d">DoReMi 的动态权重更新，与从头到尾均匀采样有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoremi">DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均匀采样保持域概率不变；DoReMi按各域相对reference的excess loss指数调整并归一化，回应训练中的相对欠拟合。它并不是对原始loss最高的域无条件加权。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个域原始loss都高，但其中一个reference本来就难，excess loss可区分这两种情形。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10429">原论文</a> · <a href="../../../../reproductions/2305.10429-doremi/">实现解读</a> · <a href="#qa-395b5c5a3e6e732d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doremi" data-paper-title="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining 基础模型 Stanford University / Google Research 2023-05-17 用小型 proxy model 的 excess loss 做 group DRO，动态提升欠拟合域权重，再按所得配比训练目标模型。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在两个公开文本域上训练 reference unigram proxy，执行 group-DRO excess-loss 指数权重更新，再以所学配比评估；未复刻 The Pile、280M proxy 与 8B target。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 doremi；相对 validation loss -0.15%。  pretraining-data data-mixture group-dro 基础模型 训练预算：数据配比、目标与优化器 DoReMi 每轮更新 α 后，为什么仍要跨域归一化？ 指数更新先得到相对权重，归一化后才能作为采样分布并保持总和1。需要固定对应reference口径；本地两域unigram proxy不等同于The Pile上的280M proxy到8B target迁移。 示意：两域权重变成2和3时，采样概率应为0.4与0.6，而不是直接把2和3当概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a08f39c27b1ec847">DoReMi 每轮更新 α 后，为什么仍要跨域归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoremi">DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>指数更新先得到相对权重，归一化后才能作为采样分布并保持总和1。需要固定对应reference口径；本地两域unigram proxy不等同于The Pile上的280M proxy到8B target迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两域权重变成2和3时，采样概率应为0.4与0.6，而不是直接把2和3当概率。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10429">原论文</a> · <a href="../../../../reproductions/2305.10429-doremi/">实现解读</a> · <a href="#qa-a08f39c27b1ec847">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

有限训练预算应该先改数据、更新方向，还是模型规模？

## 记住这一点

DoReMi 用小代理模型相对参考模型的域级 excess loss 做 Group DRO，学习数据混合比例，再把配比用于目标模型训练。Muon 对隐藏矩阵的动量作近似正交化，并配合衰减和形状缩放；其余参数不能随意照搬同一种更新。两者分别改变“训练看什么”和“梯度怎样走”，应分轴检验。

## 一个例子

代码、网页、百科各占三分之一只是一个起点。DoReMi 的权重取决于相对参考模型的学习困难，不能简单把最高原始 loss 的域全加满。更换 Muon 后还要比较等 token、等时间或等 FLOPs 的曲线，不能只取相同步数的某一个点宣布节省预算。

## 什么时候要小心

小代理得到的配比不保证任意规模都最优，优化器收益也依赖学习率与预算。低精度状态、压缩激活和数据筛选可能影响不同资源。文档中的机制诊断、短预算负结果及高成本未复现都应保留原边界。

## 先读这几篇

先读 DoReMi，明确域权重为什么由 excess loss 而非原始 loss 决定；再读 Muon 的矩阵更新，理解优化方向与非矩阵参数边界。之后看数据选择、低精度状态和训练系统。

1. [DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining](../../../reproductions/2305.10429-doremi/README.md) · [原论文](https://arxiv.org/abs/2305.10429)
2. [Muon is Scalable for LLM Training](../../../reproductions/2502.16982-muon/README.md) · [原论文](https://arxiv.org/abs/2502.16982)

## 自测一下

优化器 A 每步 loss 降得快、但一步耗时是 B 的两倍，能直接说 A 更省算力吗？

??? note "展开参考答案"

    不能。先确定目标是达到同质量所需时间、FLOPs 还是 token 数，再比较对应成本曲线；训练数据和调参预算也要匹配。单步下降和端到端效率不是同一指标。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
