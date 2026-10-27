---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 策略优化：谁在采样，谁在被更新

[LLM 后训练](index.md) / 216 个问题 · 54 篇论文

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
<p class="ar-learning-status" data-learning-status role="status">216 个问题 · 54 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:moer" data-paper-title="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback LLM 后训练 City University of Hong Kong 2026-10-22 既有混合策略训练直接加入完整专家解法，可能削弱探索；专家前缀引导虽允许学生续写，却可能把错误续写继续作为监督。MOER 逐步缩短专家 CoT 前缀：成功则保留前缀加续写，失败则回滚到已有的完整、已验证专家轨迹。它把整个引导轨迹都视为 off-policy，包括学生续写部分，并为两类轨迹采用不同目标。 完整实验：成本过高，不复现（审查 DONE），不自动重试。不得用三 seed 将诊断升级为能力复现。本地状态：L1 精确数值组件，diagnostic only。保留 Eq. 1、3–6 与单候选回滚，不是 LLM 训练器、验证器或能力复现。完整实验：成本过高，不复现（审查 DONE），不自动重试。moer.py 独立实现论文公式与单候选回滚。每个 prompt 限定一个已验证 off-policy 行、至少一个 on-policy 行，对应作者主配置 n_prefix=1；调用方提供完整响应 token mask。guided 行的前缀与续写必须都有效，prompt/padding 不参与损失。  后训练算法组件 Mix-policy RL CoT prefix guidance and selective rollback LLM 后训练 策略优化：谁在采样，谁在被更新 MOER为什么用逐渐缩短的专家前缀引导学生？ 完整专家解法减少探索空间，完全无指导又可能难以成功。逐步减少前缀让学生承担更多续写；失败时回滚到已验证完整专家轨迹，避免把错误续写继续当示范。 例如先提示前两步，再只提示第一步，学生逐渐自己完成剩余推导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-moer-39449a72" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5603dfb9948cf6c0">MOER为什么用逐渐缩短的专家前缀引导学生？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amoer">MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整专家解法减少探索空间，完全无指导又可能难以成功。逐步减少前缀让学生承担更多续写；失败时回滚到已验证完整专家轨迹，避免把错误续写继续当示范。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先提示前两步，再只提示第一步，学生逐渐自己完成剩余推导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30873v1">原论文</a> · <a href="../../../../post-training/2610.30873-moer/">实现解读</a> · <a href="#qa-5603dfb9948cf6c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:moer" data-paper-title="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback LLM 后训练 City University of Hong Kong 2026-10-22 既有混合策略训练直接加入完整专家解法，可能削弱探索；专家前缀引导虽允许学生续写，却可能把错误续写继续作为监督。MOER 逐步缩短专家 CoT 前缀：成功则保留前缀加续写，失败则回滚到已有的完整、已验证专家轨迹。它把整个引导轨迹都视为 off-policy，包括学生续写部分，并为两类轨迹采用不同目标。 完整实验：成本过高，不复现（审查 DONE），不自动重试。不得用三 seed 将诊断升级为能力复现。本地状态：L1 精确数值组件，diagnostic only。保留 Eq. 1、3–6 与单候选回滚，不是 LLM 训练器、验证器或能力复现。完整实验：成本过高，不复现（审查 DONE），不自动重试。moer.py 独立实现论文公式与单候选回滚。每个 prompt 限定一个已验证 off-policy 行、至少一个 on-policy 行，对应作者主配置 n_prefix=1；调用方提供完整响应 token mask。guided 行的前缀与续写必须都有效，prompt/padding 不参与损失。  后训练算法组件 Mix-policy RL CoT prefix guidance and selective rollback LLM 后训练 策略优化：谁在采样，谁在被更新 MOER里续写由学生生成，为什么整条专家前缀引导轨迹仍按off-policy处理？ 学生是在外部专家前缀条件下续写，整条轨迹并非从无引导学生策略完整采样，因此不能仅按作者身份把后半段归为普通on-policy。MOER成功时保留引导轨迹，失败时回滚到已验证专家轨迹，并使用两类目标；专家信息仅能处于训练边界。 教学例子：老师先写出关键推导，学生接着完成；即使后半段亲自写出，也不能假装学生从空白独立走到了同一状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8338e49fb024a4f2">MOER里续写由学生生成，为什么整条专家前缀引导轨迹仍按off-policy处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amoer">MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生是在外部专家前缀条件下续写，整条轨迹并非从无引导学生策略完整采样，因此不能仅按作者身份把后半段归为普通on-policy。MOER成功时保留引导轨迹，失败时回滚到已验证专家轨迹，并使用两类目标；专家信息仅能处于训练边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>老师先写出关键推导，学生接着完成；即使后半段亲自写出，也不能假装学生从空白独立走到了同一状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30873v1">原论文</a> · <a href="../../../../post-training/2610.30873-moer/">实现解读</a> · <a href="#qa-8338e49fb024a4f2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:moer" data-paper-title="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback LLM 后训练 City University of Hong Kong 2026-10-22 既有混合策略训练直接加入完整专家解法，可能削弱探索；专家前缀引导虽允许学生续写，却可能把错误续写继续作为监督。MOER 逐步缩短专家 CoT 前缀：成功则保留前缀加续写，失败则回滚到已有的完整、已验证专家轨迹。它把整个引导轨迹都视为 off-policy，包括学生续写部分，并为两类轨迹采用不同目标。 完整实验：成本过高，不复现（审查 DONE），不自动重试。不得用三 seed 将诊断升级为能力复现。本地状态：L1 精确数值组件，diagnostic only。保留 Eq. 1、3–6 与单候选回滚，不是 LLM 训练器、验证器或能力复现。完整实验：成本过高，不复现（审查 DONE），不自动重试。moer.py 独立实现论文公式与单候选回滚。每个 prompt 限定一个已验证 off-policy 行、至少一个 on-policy 行，对应作者主配置 n_prefix=1；调用方提供完整响应 token mask。guided 行的前缀与续写必须都有效，prompt/padding 不参与损失。  后训练算法组件 Mix-policy RL CoT prefix guidance and selective rollback LLM 后训练 策略优化：谁在采样，谁在被更新 MOER怎样区分原生on-policy与专家前缀引导轨迹？ 整个引导轨迹均视为off-policy，即使后半由学生生成，因为其起始状态受专家干预。两类使用不同目标，不能按词元作者把后缀直接归入原生策略样本。 例如学生接着专家写第三步，第三步仍属于受引导轨迹的数据流。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ab9fbec477f9eb53">MOER怎样区分原生on-policy与专家前缀引导轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amoer">MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整个引导轨迹均视为off-policy，即使后半由学生生成，因为其起始状态受专家干预。两类使用不同目标，不能按词元作者把后缀直接归入原生策略样本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生接着专家写第三步，第三步仍属于受引导轨迹的数据流。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30873v1">原论文</a> · <a href="../../../../post-training/2610.30873-moer/">实现解读</a> · <a href="#qa-ab9fbec477f9eb53">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:moer" data-paper-title="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback LLM 后训练 City University of Hong Kong 2026-10-22 既有混合策略训练直接加入完整专家解法，可能削弱探索；专家前缀引导虽允许学生续写，却可能把错误续写继续作为监督。MOER 逐步缩短专家 CoT 前缀：成功则保留前缀加续写，失败则回滚到已有的完整、已验证专家轨迹。它把整个引导轨迹都视为 off-policy，包括学生续写部分，并为两类轨迹采用不同目标。 完整实验：成本过高，不复现（审查 DONE），不自动重试。不得用三 seed 将诊断升级为能力复现。本地状态：L1 精确数值组件，diagnostic only。保留 Eq. 1、3–6 与单候选回滚，不是 LLM 训练器、验证器或能力复现。完整实验：成本过高，不复现（审查 DONE），不自动重试。moer.py 独立实现论文公式与单候选回滚。每个 prompt 限定一个已验证 off-policy 行、至少一个 on-policy 行，对应作者主配置 n_prefix=1；调用方提供完整响应 token mask。guided 行的前缀与续写必须都有效，prompt/padding 不参与损失。  后训练算法组件 Mix-policy RL CoT prefix guidance and selective rollback LLM 后训练 策略优化：谁在采样，谁在被更新 MOER的off-policy比值前向为一时为什么仍有梯度？ 分母中的策略概率停止梯度，分子保持可微，所以数值相消不等于导数相消。联合组优势不除标准差，最终按全部有效响应词元归一，不能额外按混合权重改分母。 例如分子等于detach后的分母时结果是一，但改变分子仍会改变损失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6db180f129af89fe">MOER的off-policy比值前向为一时为什么仍有梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amoer">MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分母中的策略概率停止梯度，分子保持可微，所以数值相消不等于导数相消。联合组优势不除标准差，最终按全部有效响应词元归一，不能额外按混合权重改分母。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如分子等于detach后的分母时结果是一，但改变分子仍会改变损失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30873v1">原论文</a> · <a href="../../../../post-training/2610.30873-moer/">实现解读</a> · <a href="#qa-6db180f129af89fe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cord" data-paper-title="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents LLM 后训练 The Chinese University of Hong Kong 2026-10-21 任务奖励和教师指导提供不同信号，直接相加会让相反的梯度互相抵消。CORD 不替换 GRPO 或 OPD 的目标，而是明确选择一个 protected objective，最小修改另一个梯度。是否修改由独立的投影 gate 决定：只在冲突时投影，或始终去掉平行分量。两种保护方向、两种 gate 不能混为同一个算法配置。 完整实验成本过高，不复现（审查 DONE）。诊断用两个冲突的交叉熵目标对一个极小 MLP 做三次真实 SGD 更新，验证一般双目标组合公式。L1 梯度组合组件，不是 Agent 能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本篇属于 2026-10-22 新公告，不是将旧候选重记为新论文。combine_gradients 对已汇总向量执行公式；accumulate_gradients 先应用调用方固定的损失聚合权重，再执行一次投影；objective_gradients 从真实 scalar loss 提取参数梯度。  Agentic RL 联合RL与蒸馏梯度优化 LLM 后训练 策略优化：谁在采样，谁在被更新 CORD为什么先选要保护的目标？ 任务奖励与教师指导梯度冲突时，直接相加会抵消。保护方向明确哪一目标的一阶方向不能被另一目标损害，再最小修改未保护梯度；这是一种明确取舍。 例如保护任务奖励与保护教师行为，是两种不同配置，不能只写用了投影。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-cord-0b4a5d25" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a09f25b1ef523765">CORD为什么先选要保护的目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acord">CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务奖励与教师指导梯度冲突时，直接相加会抵消。保护方向明确哪一目标的一阶方向不能被另一目标损害，再最小修改未保护梯度；这是一种明确取舍。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保护任务奖励与保护教师行为，是两种不同配置，不能只写用了投影。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29965v1">原论文</a> · <a href="../../../../post-training/2610.29965-cord/">实现解读</a> · <a href="#qa-a09f25b1ef523765">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cord" data-paper-title="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents LLM 后训练 The Chinese University of Hong Kong 2026-10-21 任务奖励和教师指导提供不同信号，直接相加会让相反的梯度互相抵消。CORD 不替换 GRPO 或 OPD 的目标，而是明确选择一个 protected objective，最小修改另一个梯度。是否修改由独立的投影 gate 决定：只在冲突时投影，或始终去掉平行分量。两种保护方向、两种 gate 不能混为同一个算法配置。 完整实验成本过高，不复现（审查 DONE）。诊断用两个冲突的交叉熵目标对一个极小 MLP 做三次真实 SGD 更新，验证一般双目标组合公式。L1 梯度组合组件，不是 Agent 能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本篇属于 2026-10-22 新公告，不是将旧候选重记为新论文。combine_gradients 对已汇总向量执行公式；accumulate_gradients 先应用调用方固定的损失聚合权重，再执行一次投影；objective_gradients 从真实 scalar loss 提取参数梯度。  Agentic RL 联合RL与蒸馏梯度优化 LLM 后训练 策略优化：谁在采样，谁在被更新 CORD为什么要先选protected梯度，再对另一个梯度投影？ 投影的含义是尽量保留被保护目标的方向，只最小修改冲突的另一方向；交换保护对象会得到不同更新。还要区分只在冲突时投影与始终投影，并在完整优化批次汇总后操作。得到的是优化器转换前的一阶性质，不保证有限AdamW步后目标必降。 教学例子：任务奖励与教师模仿希望把同一参数往相反方向推。保护任务目标与保护模仿目标，保留下来的方向不会相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1ebcba12aeca3711">CORD为什么要先选protected梯度，再对另一个梯度投影？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acord">CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投影的含义是尽量保留被保护目标的方向，只最小修改冲突的另一方向；交换保护对象会得到不同更新。还要区分只在冲突时投影与始终投影，并在完整优化批次汇总后操作。得到的是优化器转换前的一阶性质，不保证有限AdamW步后目标必降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>任务奖励与教师模仿希望把同一参数往相反方向推。保护任务目标与保护模仿目标，保留下来的方向不会相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29965v1">原论文</a> · <a href="../../../../post-training/2610.29965-cord/">实现解读</a> · <a href="#qa-1ebcba12aeca3711">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cord" data-paper-title="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents LLM 后训练 The Chinese University of Hong Kong 2026-10-21 任务奖励和教师指导提供不同信号，直接相加会让相反的梯度互相抵消。CORD 不替换 GRPO 或 OPD 的目标，而是明确选择一个 protected objective，最小修改另一个梯度。是否修改由独立的投影 gate 决定：只在冲突时投影，或始终去掉平行分量。两种保护方向、两种 gate 不能混为同一个算法配置。 完整实验成本过高，不复现（审查 DONE）。诊断用两个冲突的交叉熵目标对一个极小 MLP 做三次真实 SGD 更新，验证一般双目标组合公式。L1 梯度组合组件，不是 Agent 能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本篇属于 2026-10-22 新公告，不是将旧候选重记为新论文。combine_gradients 对已汇总向量执行公式；accumulate_gradients 先应用调用方固定的损失聚合权重，再执行一次投影；objective_gradients 从真实 scalar loss 提取参数梯度。  Agentic RL 联合RL与蒸馏梯度优化 LLM 后训练 策略优化：谁在采样，谁在被更新 CORD只在冲突时投影与always投影有什么差别？ 冲突门控保留同向分量，只有内积为负才移除冲突；always连有益平行分量也去掉。两者合成方向不同，且投影前性质不保证自适应优化器有限步更新必然下降。 例如两个梯度同向时，冲突版直接相加，always版仍削掉另一方向的平行部分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-05b2cde4b0ffd64b">CORD只在冲突时投影与always投影有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acord">CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冲突门控保留同向分量，只有内积为负才移除冲突；always连有益平行分量也去掉。两者合成方向不同，且投影前性质不保证自适应优化器有限步更新必然下降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个梯度同向时，冲突版直接相加，always版仍削掉另一方向的平行部分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29965v1">原论文</a> · <a href="../../../../post-training/2610.29965-cord/">实现解读</a> · <a href="#qa-05b2cde4b0ffd64b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cord" data-paper-title="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents LLM 后训练 The Chinese University of Hong Kong 2026-10-21 任务奖励和教师指导提供不同信号，直接相加会让相反的梯度互相抵消。CORD 不替换 GRPO 或 OPD 的目标，而是明确选择一个 protected objective，最小修改另一个梯度。是否修改由独立的投影 gate 决定：只在冲突时投影，或始终去掉平行分量。两种保护方向、两种 gate 不能混为同一个算法配置。 完整实验成本过高，不复现（审查 DONE）。诊断用两个冲突的交叉熵目标对一个极小 MLP 做三次真实 SGD 更新，验证一般双目标组合公式。L1 梯度组合组件，不是 Agent 能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本篇属于 2026-10-22 新公告，不是将旧候选重记为新论文。combine_gradients 对已汇总向量执行公式；accumulate_gradients 先应用调用方固定的损失聚合权重，再执行一次投影；objective_gradients 从真实 scalar loss 提取参数梯度。  Agentic RL 联合RL与蒸馏梯度优化 LLM 后训练 策略优化：谁在采样，谁在被更新 CORD为什么先累加完整optimizer批梯度，再投影一次？ 投影是非线性操作，逐微批投影再相加通常不等于全批投影。固定权重汇总后还需先应用目标权重λ；保护梯度为零时不投影，λ为零直接返回第一目标方向。 例如两微批冲突方向抵消后可能不冲突，提前分别投影会改变最终结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-096a6edd2e82c442">CORD为什么先累加完整optimizer批梯度，再投影一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acord">CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投影是非线性操作，逐微批投影再相加通常不等于全批投影。固定权重汇总后还需先应用目标权重λ；保护梯度为零时不投影，λ为零直接返回第一目标方向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两微批冲突方向抵消后可能不冲突，提前分别投影会改变最终结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29965v1">原论文</a> · <a href="../../../../post-training/2610.29965-cord/">实现解读</a> · <a href="#qa-096a6edd2e82c442">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ggpo" data-paper-title="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards LLM 后训练 University of Illinois Urbana-Champaign 2026-10-14 behavior policy 负责产生样本，reference policy 负责 KL anchor，两者不是同一角色。组内 adjusted reward 全相同时，策略满足该 reference 的 Gibbs 目标。GGPO 用 log-mean-exp 与算术平均的差量度偏离，不给更新乘 learner/behavior importance weight，并周期刷新 reference 以改变后续目标。 完整多 GPU 训练成本过高，不复现（审查 DONE）；L1 objective / refresh 组件及微型策略更新诊断。L1 objective / refresh 组件及微型策略更新诊断。完整多 GPU 训练成本过高，不复现（审查 DONE）；不把规则 verifier 当数学能力证据。公开 Hamlet 1524 固定内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；  离策略推理 RL 后训练算法组件 GGPO LLM 后训练 策略优化：谁在采样，谁在被更新 GGPO为什么分开behavior与reference两种策略角色？ behavior决定采样数据来自哪里，reference定义KL锚点。二者可不同，混为一个会误解目标和刷新行为；周期改变reference是在改变后续优化目标，而非自动重采同一批数据。 例如一套冻结策略收集回答，另一套参考决定偏移惩罚，各自有独立职责。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ggpo-409d30ac" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7a1894bc05c764de">GGPO为什么分开behavior与reference两种策略角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aggpo">Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>behavior决定采样数据来自哪里，reference定义KL锚点。二者可不同，混为一个会误解目标和刷新行为；周期改变reference是在改变后续优化目标，而非自动重采同一批数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一套冻结策略收集回答，另一套参考决定偏移惩罚，各自有独立职责。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20814v1">原论文</a> · <a href="../../../../post-training/2610.20814-ggpo/">实现解读</a> · <a href="#qa-7a1894bc05c764de">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ggpo" data-paper-title="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards LLM 后训练 University of Illinois Urbana-Champaign 2026-10-14 behavior policy 负责产生样本，reference policy 负责 KL anchor，两者不是同一角色。组内 adjusted reward 全相同时，策略满足该 reference 的 Gibbs 目标。GGPO 用 log-mean-exp 与算术平均的差量度偏离，不给更新乘 learner/behavior importance weight，并周期刷新 reference 以改变后续目标。 完整多 GPU 训练成本过高，不复现（审查 DONE）；L1 objective / refresh 组件及微型策略更新诊断。L1 objective / refresh 组件及微型策略更新诊断。完整多 GPU 训练成本过高，不复现（审查 DONE）；不把规则 verifier 当数学能力证据。公开 Hamlet 1524 固定内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；  离策略推理 RL 后训练算法组件 GGPO LLM 后训练 策略优化：谁在采样，谁在被更新 GGPO的behavior policy与reference policy为什么不能混为同一个角色？ behavior决定固定样本从哪里来，reference决定KL锚定后的Gibbs目标。GGPO根据调整奖励的log-mean-exp与均值差直接优化，不额外套learner/behavior重要性权重。刷新reference改变后续目标，而不是改写过去采样来源；过滤和归一化后的日志也不能直接套原始理论界。 教学例子：旧模型提供一组回答，新模型相对另一个锚点更新；更换锚点并不会让这批旧回答变成由新模型采样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1f2cbda8035e076d">GGPO的behavior policy与reference policy为什么不能混为同一个角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aggpo">Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>behavior决定固定样本从哪里来，reference决定KL锚定后的Gibbs目标。GGPO根据调整奖励的log-mean-exp与均值差直接优化，不额外套learner/behavior重要性权重。刷新reference改变后续目标，而不是改写过去采样来源；过滤和归一化后的日志也不能直接套原始理论界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旧模型提供一组回答，新模型相对另一个锚点更新；更换锚点并不会让这批旧回答变成由新模型采样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20814v1">原论文</a> · <a href="../../../../post-training/2610.20814-ggpo/">实现解读</a> · <a href="#qa-1f2cbda8035e076d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ggpo" data-paper-title="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards LLM 后训练 University of Illinois Urbana-Champaign 2026-10-14 behavior policy 负责产生样本，reference policy 负责 KL anchor，两者不是同一角色。组内 adjusted reward 全相同时，策略满足该 reference 的 Gibbs 目标。GGPO 用 log-mean-exp 与算术平均的差量度偏离，不给更新乘 learner/behavior importance weight，并周期刷新 reference 以改变后续目标。 完整多 GPU 训练成本过高，不复现（审查 DONE）；L1 objective / refresh 组件及微型策略更新诊断。L1 objective / refresh 组件及微型策略更新诊断。完整多 GPU 训练成本过高，不复现（审查 DONE）；不把规则 verifier 当数学能力证据。公开 Hamlet 1524 固定内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；  离策略推理 RL 后训练算法组件 GGPO LLM 后训练 策略优化：谁在采样，谁在被更新 GGPO的Gibbs gap与普通learner/behavior重要性加权有什么不同？ 它用调整奖励的log-mean-exp减均值度量组内偏离，直接求导，不把learner/behavior比再乘进更新。额外重要性权重会改变目标，不应因看见off-policy样本就自行添加。 例如数据来自旧策略，并不意味着所有方法的损失都必须再乘同一套比值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-63db0ed06b4206f6">GGPO的Gibbs gap与普通learner/behavior重要性加权有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aggpo">Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用调整奖励的log-mean-exp减均值度量组内偏离，直接求导，不把learner/behavior比再乘进更新。额外重要性权重会改变目标，不应因看见off-policy样本就自行添加。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数据来自旧策略，并不意味着所有方法的损失都必须再乘同一套比值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20814v1">原论文</a> · <a href="../../../../post-training/2610.20814-ggpo/">实现解读</a> · <a href="#qa-63db0ed06b4206f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ggpo" data-paper-title="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards LLM 后训练 University of Illinois Urbana-Champaign 2026-10-14 behavior policy 负责产生样本，reference policy 负责 KL anchor，两者不是同一角色。组内 adjusted reward 全相同时，策略满足该 reference 的 Gibbs 目标。GGPO 用 log-mean-exp 与算术平均的差量度偏离，不给更新乘 learner/behavior importance weight，并周期刷新 reference 以改变后续目标。 完整多 GPU 训练成本过高，不复现（审查 DONE）；L1 objective / refresh 组件及微型策略更新诊断。L1 objective / refresh 组件及微型策略更新诊断。完整多 GPU 训练成本过高，不复现（审查 DONE）；不把规则 verifier 当数学能力证据。公开 Hamlet 1524 固定内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；  离策略推理 RL 后训练算法组件 GGPO LLM 后训练 策略优化：谁在采样，谁在被更新 GGPO可选clipping为何不能直接对clamp后的LME反传？ 该接口先用裁剪的learner/reference比计算冻结系数，再用原序列logp更新。直接穿过clamp会把饱和词元梯度清零，改变规定的替身梯度；全批归一与过滤边界也须保留。 例如裁剪只限制用于构造权重的数值，不代表饱和位置从学习图中永久消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8ef00609abac4e8a">GGPO可选clipping为何不能直接对clamp后的LME反传？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aggpo">Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>该接口先用裁剪的learner/reference比计算冻结系数，再用原序列logp更新。直接穿过clamp会把饱和词元梯度清零，改变规定的替身梯度；全批归一与过滤边界也须保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如裁剪只限制用于构造权重的数值，不代表饱和位置从学习图中永久消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20814v1">原论文</a> · <a href="../../../../post-training/2610.20814-ggpo/">实现解读</a> · <a href="#qa-8ef00609abac4e8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:orl-diffusion" data-paper-title="On-Policy Residual Learning for Diffusion Language Models" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="On-Policy Residual Learning for Diffusion Language Models LLM 后训练 Together AI / University of Illinois Urbana-Champaign 2026-10-14 将上一步预测分布作为残差上下文不是简单后处理：训练时必须看到模型自己诱导的残差轨迹。ORL联合在线采集、状态传输、精确重放及熵收缩，减少训练与推理残差状态分布差异。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  扩散语言模型后训练 On-policy学习与蒸馏 LLM 后训练 策略优化：谁在采样，谁在被更新 ORL为何要让扩散训练看到自身诱导的残差上下文？ 残差来自前一步模型预测，推理时包含模型自身误差。只训练理想残差会形成状态分布差，在线采集和重放让模型学习实际会遇到的残差状态。 例如前一步把某词预测错，下一步需要见过这种带错概率上下文才能学会修复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-orl-diffusion-21689257" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7afac6883271e078">ORL为何要让扩散训练看到自身诱导的残差上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aorl-diffusion">On-Policy Residual Learning for Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>残差来自前一步模型预测，推理时包含模型自身误差。只训练理想残差会形成状态分布差，在线采集和重放让模型学习实际会遇到的残差状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前一步把某词预测错，下一步需要见过这种带错概率上下文才能学会修复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20687">原论文</a> · <a href="../../../../post-training/2610.20687-orl-diffusion/">实现解读</a> · <a href="#qa-7afac6883271e078">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:orl-diffusion" data-paper-title="On-Policy Residual Learning for Diffusion Language Models" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="On-Policy Residual Learning for Diffusion Language Models LLM 后训练 Together AI / University of Illinois Urbana-Champaign 2026-10-14 将上一步预测分布作为残差上下文不是简单后处理：训练时必须看到模型自己诱导的残差轨迹。ORL联合在线采集、状态传输、精确重放及熵收缩，减少训练与推理残差状态分布差异。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  扩散语言模型后训练 On-policy学习与蒸馏 LLM 后训练 策略优化：谁在采样，谁在被更新 ORL为什么要求重放模型自己产生的残差状态，而不只训练固定残差输入？ 扩散模型上一步预测会成为下一步残差上下文，误差也沿这条状态路径传播。固定或理想残差训练可能避开推理时真实遇到的状态；在线采集与精确重放让训练面对自身诱导的分布，再结合熵收缩。该机制不是输出后的简单修补，本地尚无完整训练证据。 教学例子：第一轮预测已偏向错误词，第二轮会在这个偏差上继续更新；只用完美残差做训练，可能从未见过这种纠偏情形。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fd0685fda98823c0">ORL为什么要求重放模型自己产生的残差状态，而不只训练固定残差输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aorl-diffusion">On-Policy Residual Learning for Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>扩散模型上一步预测会成为下一步残差上下文，误差也沿这条状态路径传播。固定或理想残差训练可能避开推理时真实遇到的状态；在线采集与精确重放让训练面对自身诱导的分布，再结合熵收缩。该机制不是输出后的简单修补，本地尚无完整训练证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一轮预测已偏向错误词，第二轮会在这个偏差上继续更新；只用完美残差做训练，可能从未见过这种纠偏情形。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20687">原论文</a> · <a href="../../../../post-training/2610.20687-orl-diffusion/">实现解读</a> · <a href="#qa-fd0685fda98823c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:orl-diffusion" data-paper-title="On-Policy Residual Learning for Diffusion Language Models" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="On-Policy Residual Learning for Diffusion Language Models LLM 后训练 Together AI / University of Illinois Urbana-Champaign 2026-10-14 将上一步预测分布作为残差上下文不是简单后处理：训练时必须看到模型自己诱导的残差轨迹。ORL联合在线采集、状态传输、精确重放及熵收缩，减少训练与推理残差状态分布差异。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  扩散语言模型后训练 On-policy学习与蒸馏 LLM 后训练 策略优化：谁在采样，谁在被更新 ORL残差学习与推理后额外平滑输出有何不同？ 后处理只改最后结果，ORL把前一步分布传入后续模型并参与训练，改变状态和学习目标。它还包含精确重放与熵收缩，不能用简单概率平均冒充整个方法。 例如把两次结果平均，没有教模型在上次错配状态下继续去噪。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8a6e93004eb1c371">ORL残差学习与推理后额外平滑输出有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aorl-diffusion">On-Policy Residual Learning for Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后处理只改最后结果，ORL把前一步分布传入后续模型并参与训练，改变状态和学习目标。它还包含精确重放与熵收缩，不能用简单概率平均冒充整个方法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把两次结果平均，没有教模型在上次错配状态下继续去噪。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20687">原论文</a> · <a href="../../../../post-training/2610.20687-orl-diffusion/">实现解读</a> · <a href="#qa-8a6e93004eb1c371">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:orl-diffusion" data-paper-title="On-Policy Residual Learning for Diffusion Language Models" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="On-Policy Residual Learning for Diffusion Language Models LLM 后训练 Together AI / University of Illinois Urbana-Champaign 2026-10-14 将上一步预测分布作为残差上下文不是简单后处理：训练时必须看到模型自己诱导的残差轨迹。ORL联合在线采集、状态传输、精确重放及熵收缩，减少训练与推理残差状态分布差异。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  扩散语言模型后训练 On-policy学习与蒸馏 LLM 后训练 策略优化：谁在采样，谁在被更新 本地能否调用ORL adapter复现残差轨迹？ 当前只有文献收录，没有本地adapter、指标或GPU回执。README公式是阅读记号，不能因看见递推式就登记可执行算子，也不能把通用扩散模块称为该训练已实现。 例如演化注册表里加一个名字，不会自动产生在线采集和精确重放流程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-59fae2e103ec2ef6">本地能否调用ORL adapter复现残差轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aorl-diffusion">On-Policy Residual Learning for Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前只有文献收录，没有本地adapter、指标或GPU回执。README公式是阅读记号，不能因看见递推式就登记可执行算子，也不能把通用扩散模块称为该训练已实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如演化注册表里加一个名字，不会自动产生在线采集和精确重放流程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20687">原论文</a> · <a href="../../../../post-training/2610.20687-orl-diffusion/">实现解读</a> · <a href="#qa-59fae2e103ec2ef6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo-framework" data-paper-title="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence LLM 后训练 Tsinghua University AIR 2026-10-09 GPPO把近端优化拆成f-divergence几何和估计拓扑。MC、atomic、binary对采样动作概率/补集的处理不同，诱导实际不同信任域。所有组合参与真实rollout token优化，不是给GRPO换registry名；新key不覆盖已有2508.07629的gppo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint与配置的GRPO-control；零优势重采样成本显式记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Proximal policy optimization f-divergence geometry Probability-aware estimator LLM 后训练 策略优化：谁在采样，谁在被更新 GPPO框架把近端更新拆成哪两个独立选择？ 一是f-divergence几何，二是如何估计该散度的拓扑。不同组合定义不同可接受概率比范围，因此统一框架并不表示所有实例训练行为相同。 例如相同散度函数配不同概率补集处理，也可能得到不同信任域。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gppo-framework-a99015aa" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7e47d9d0de4b56de">GPPO框架把近端更新拆成哪两个独立选择？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo-framework">Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一是f-divergence几何，二是如何估计该散度的拓扑。不同组合定义不同可接受概率比范围，因此统一框架并不表示所有实例训练行为相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如相同散度函数配不同概率补集处理，也可能得到不同信任域。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13015">原论文</a> · <a href="../../../../reproductions/2610.13015-gppo-framework/">实现解读</a> · <a href="#qa-7e47d9d0de4b56de">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo-framework" data-paper-title="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence LLM 后训练 Tsinghua University AIR 2026-10-09 GPPO把近端优化拆成f-divergence几何和估计拓扑。MC、atomic、binary对采样动作概率/补集的处理不同，诱导实际不同信任域。所有组合参与真实rollout token优化，不是给GRPO换registry名；新key不覆盖已有2508.07629的gppo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint与配置的GRPO-control；零优势重采样成本显式记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Proximal policy optimization f-divergence geometry Probability-aware estimator LLM 后训练 策略优化：谁在采样，谁在被更新 同一个f-divergence换成MC、atomic或binary估计，为何可能得到不同信任域？ 估计方式决定采样动作概率及其补集怎样进入散度，因而相同函数和半径也不必给出相同可行比率区间。GPPO把几何与估计拓扑分开描述，再由实际区间约束策略更新。不能只给GRPO换名称；某些KL写法间的差异也应显式保留而非暗改。 教学例子：一个动作本来极罕见，只约束它自己的比率与同时考虑“其余动作”概率，可能允许不同幅度的概率变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9f37ce2c9a7ea94c">同一个f-divergence换成MC、atomic或binary估计，为何可能得到不同信任域？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo-framework">Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>估计方式决定采样动作概率及其补集怎样进入散度，因而相同函数和半径也不必给出相同可行比率区间。GPPO把几何与估计拓扑分开描述，再由实际区间约束策略更新。不能只给GRPO换名称；某些KL写法间的差异也应显式保留而非暗改。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个动作本来极罕见，只约束它自己的比率与同时考虑“其余动作”概率，可能允许不同幅度的概率变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13015">原论文</a> · <a href="../../../../reproductions/2610.13015-gppo-framework/">实现解读</a> · <a href="#qa-9f37ce2c9a7ea94c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo-framework" data-paper-title="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence LLM 后训练 Tsinghua University AIR 2026-10-09 GPPO把近端优化拆成f-divergence几何和估计拓扑。MC、atomic、binary对采样动作概率/补集的处理不同，诱导实际不同信任域。所有组合参与真实rollout token优化，不是给GRPO换registry名；新key不覆盖已有2508.07629的gppo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint与配置的GRPO-control；零优势重采样成本显式记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Proximal policy optimization f-divergence geometry Probability-aware estimator LLM 后训练 策略优化：谁在采样，谁在被更新 MC、atomic与binary拓扑为何不能只看成实现细节？ 它们分别如何计入采样动作概率及未采样补集不同，会改变估计散度和允许比值边界。只有在相应定义成立时才能谈算法对应，不能把名字映射当数学等价。 例如binary还考虑一减动作概率的部分，不是给atomic结果简单换标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-418da2f4d66475da">MC、atomic与binary拓扑为何不能只看成实现细节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo-framework">Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它们分别如何计入采样动作概率及未采样补集不同，会改变估计散度和允许比值边界。只有在相应定义成立时才能谈算法对应，不能把名字映射当数学等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如binary还考虑一减动作概率的部分，不是给atomic结果简单换标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13015">原论文</a> · <a href="../../../../reproductions/2610.13015-gppo-framework/">实现解读</a> · <a href="#qa-418da2f4d66475da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo-framework" data-paper-title="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence LLM 后训练 Tsinghua University AIR 2026-10-09 GPPO把近端优化拆成f-divergence几何和估计拓扑。MC、atomic、binary对采样动作概率/补集的处理不同，诱导实际不同信任域。所有组合参与真实rollout token优化，不是给GRPO换registry名；新key不覆盖已有2508.07629的gppo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint与配置的GRPO-control；零优势重采样成本显式记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Proximal policy optimization f-divergence geometry Probability-aware estimator LLM 后训练 策略优化：谁在采样，谁在被更新 GPPO中的literal KL与two-sided-log为什么分开暴露？ 原式与部分算法映射存在不一致，本地显式区分两个目标，避免悄悄改公式。实现还需保证比值正、binary补集合法，并按选定拓扑求信任域而非固定复制PPO边界。 例如配置写KL却执行双侧log，会使实验无法知道究竟验证了哪个目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-21dcbebdc78ec1a6">GPPO中的literal KL与two-sided-log为什么分开暴露？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo-framework">Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原式与部分算法映射存在不一致，本地显式区分两个目标，避免悄悄改公式。实现还需保证比值正、binary补集合法，并按选定拓扑求信任域而非固定复制PPO边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如配置写KL却执行双侧log，会使实验无法知道究竟验证了哪个目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13015">原论文</a> · <a href="../../../../reproductions/2610.13015-gppo-framework/">实现解读</a> · <a href="#qa-21dcbebdc78ec1a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tapo-trajectory" data-paper-title="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL LLM 后训练 Tsinghua University AIR 2026-10-09 autoregressive轨迹的前序policy变化累积state distribution gap。TAPO对token前缀likelihood ratio取几何均值、按长度收紧clipping，并stop-gradient避免前序token反传进当前动作。新key不覆盖已有2607.27973的tapo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint、采样与优化上限的GRPO-control；不是原Qwen3-8B Avg@8结果；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Trajectory-aware policy optimization Geometric prefix correction Length-aware clipping LLM 后训练 策略优化：谁在采样，谁在被更新 TAPO轨迹版为何关注前缀状态分布而不只关注当前动作比值？ 前面策略的细小变化可累积成后续状态偏移，当前动作比值不足以描述整段访问差异。前缀对数比的几何平均把轨迹信息带进当前更新，并按位置收紧边界。 例如前几步分支已经改变，最后一步动作看似接近，也不能说明其状态仍来自旧分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-tapo-trajectory-36082418" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d2a704ecd94eafec">TAPO轨迹版为何关注前缀状态分布而不只关注当前动作比值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atapo-trajectory">Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前面策略的细小变化可累积成后续状态偏移，当前动作比值不足以描述整段访问差异。前缀对数比的几何平均把轨迹信息带进当前更新，并按位置收紧边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前几步分支已经改变，最后一步动作看似接近，也不能说明其状态仍来自旧分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13020">原论文</a> · <a href="../../../../reproductions/2610.13020-tapo-trajectory/">实现解读</a> · <a href="#qa-d2a704ecd94eafec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tapo-trajectory" data-paper-title="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL LLM 后训练 Tsinghua University AIR 2026-10-09 autoregressive轨迹的前序policy变化累积state distribution gap。TAPO对token前缀likelihood ratio取几何均值、按长度收紧clipping，并stop-gradient避免前序token反传进当前动作。新key不覆盖已有2607.27973的tapo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint、采样与优化上限的GRPO-control；不是原Qwen3-8B Avg@8结果；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Trajectory-aware policy optimization Geometric prefix correction Length-aware clipping LLM 后训练 策略优化：谁在采样，谁在被更新 TAPO用前缀几何平均比率后，为什么还要stop-gradient避免跨token反传？ 前缀比率用于衡量累计状态偏移，但当前动作的信用不应经这一权重再回传到所有早期token。TAPO冻结几何平均权重，并让当前动作保留自己的log-prob梯度，避免额外的跨位置梯度和按前缀长度稀释。权重与梯度路径是两个需要分别实现的部分。 教学例子：第十步的前缀已偏离旧策略，需要调整这一动作的权重；不等于这一次损失应该同时重写前九步的信用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dbfc5a17598c40cf">TAPO用前缀几何平均比率后，为什么还要stop-gradient避免跨token反传？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atapo-trajectory">Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前缀比率用于衡量累计状态偏移，但当前动作的信用不应经这一权重再回传到所有早期token。TAPO冻结几何平均权重，并让当前动作保留自己的log-prob梯度，避免额外的跨位置梯度和按前缀长度稀释。权重与梯度路径是两个需要分别实现的部分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第十步的前缀已偏离旧策略，需要调整这一动作的权重；不等于这一次损失应该同时重写前九步的信用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13020">原论文</a> · <a href="../../../../reproductions/2610.13020-tapo-trajectory/">实现解读</a> · <a href="#qa-dbfc5a17598c40cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tapo-trajectory" data-paper-title="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL LLM 后训练 Tsinghua University AIR 2026-10-09 autoregressive轨迹的前序policy变化累积state distribution gap。TAPO对token前缀likelihood ratio取几何均值、按长度收紧clipping，并stop-gradient避免前序token反传进当前动作。新key不覆盖已有2607.27973的tapo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint、采样与优化上限的GRPO-control；不是原Qwen3-8B Avg@8结果；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Trajectory-aware policy optimization Geometric prefix correction Length-aware clipping LLM 后训练 策略优化：谁在采样，谁在被更新 前缀几何平均与前缀概率比直接相乘有什么差别？ 几何平均取平均log-ratio后指数化，减轻比值随前缀长度极端放大的尺度问题。它是另一估计设计，不是完整轨迹重要性乘积的数值技巧替代。 例如同样轻微偏移重复多步，连乘可能很极端，几何平均保留的是平均偏移尺度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-db3847d99823a9c8">前缀几何平均与前缀概率比直接相乘有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atapo-trajectory">Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>几何平均取平均log-ratio后指数化，减轻比值随前缀长度极端放大的尺度问题。它是另一估计设计，不是完整轨迹重要性乘积的数值技巧替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样轻微偏移重复多步，连乘可能很极端，几何平均保留的是平均偏移尺度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13020">原论文</a> · <a href="../../../../reproductions/2610.13020-tapo-trajectory/">实现解读</a> · <a href="#qa-db3847d99823a9c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tapo-trajectory" data-paper-title="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL LLM 后训练 Tsinghua University AIR 2026-10-09 autoregressive轨迹的前序policy变化累积state distribution gap。TAPO对token前缀likelihood ratio取几何均值、按长度收紧clipping，并stop-gradient避免前序token反传进当前动作。新key不覆盖已有2607.27973的tapo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint、采样与优化上限的GRPO-control；不是原Qwen3-8B Avg@8结果；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Trajectory-aware policy optimization Geometric prefix correction Length-aware clipping LLM 后训练 策略优化：谁在采样，谁在被更新 TAPO怎样避免前缀比值让当前词元梯度被除以位置长度？ 前缀几何比停止梯度，再乘当前概率除以其停止梯度副本。这样前向保持所需比值，反向只作用当前动作，不引入前序梯度或一除位置长度的稀释。 例如第十步权重参考前十步，但它的梯度不应因此自动缩成原来的十分之一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b8acbe2f1744cbf8">TAPO怎样避免前缀比值让当前词元梯度被除以位置长度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atapo-trajectory">Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前缀几何比停止梯度，再乘当前概率除以其停止梯度副本。这样前向保持所需比值，反向只作用当前动作，不引入前序梯度或一除位置长度的稀释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第十步权重参考前十步，但它的梯度不应因此自动缩成原来的十分之一。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13020">原论文</a> · <a href="../../../../reproductions/2610.13020-tapo-trajectory/">实现解读</a> · <a href="#qa-b8acbe2f1744cbf8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:zcpo" data-paper-title="When KL Regularization Misfires in Group Policy Optimization" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="When KL Regularization Misfires in Group Policy Optimization LLM 后训练 Alibaba Group 2026-10-08 独立 KL 惩罚可能在奖励相同或奖励梯度取消时继续更新策略。ZCPO 用响应平均的条件 KL 相对漂移，校准组内奖励系数；再将该系数放进原策略 surrogate，不另加独立 KL loss。 实际训练链路和边界检查已实现；24 步单 seed 诊断不是 AIME 收益复现。固定 Qwen3-4B 基础参考，训练 q/v LoRA；group=4、24 步、每响应最多 256 token，8 个独立验证问题。完整词表条件 KL、有效响应 mask、长度平均和 stop-gradient 均实际执行。见运行说明。  组相对策略优化 KL 校准 LLM 后训练 策略优化：谁在采样，谁在被更新 ZCPO为什么把KL漂移放进组内系数而不另加独立损失？ 独立KL在奖励无区分时仍可能推动更新，ZCPO把奖励和相对KL共同中心化后形成零和系数，再交给原策略surrogate，强调组内相对信用。 例如所有回答奖励一样时，不希望仅因额外KL项仍自动发生一次策略训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-zcpo-1bf32735" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bbc74cf447b9f8d5">ZCPO为什么把KL漂移放进组内系数而不另加独立损失？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Azcpo">When KL Regularization Misfires in Group Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立KL在奖励无区分时仍可能推动更新，ZCPO把奖励和相对KL共同中心化后形成零和系数，再交给原策略surrogate，强调组内相对信用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如所有回答奖励一样时，不希望仅因额外KL项仍自动发生一次策略训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12161">原论文</a> · <a href="../../../../post-training/2610.12161-zcpo/">实现解读</a> · <a href="#qa-bbc74cf447b9f8d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:zcpo" data-paper-title="When KL Regularization Misfires in Group Policy Optimization" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="When KL Regularization Misfires in Group Policy Optimization LLM 后训练 Alibaba Group 2026-10-08 独立 KL 惩罚可能在奖励相同或奖励梯度取消时继续更新策略。ZCPO 用响应平均的条件 KL 相对漂移，校准组内奖励系数；再将该系数放进原策略 surrogate，不另加独立 KL loss。 实际训练链路和边界检查已实现；24 步单 seed 诊断不是 AIME 收益复现。固定 Qwen3-4B 基础参考，训练 q/v LoRA；group=4、24 步、每响应最多 256 token，8 个独立验证问题。完整词表条件 KL、有效响应 mask、长度平均和 stop-gradient 均实际执行。见运行说明。  组相对策略优化 KL 校准 LLM 后训练 策略优化：谁在采样，谁在被更新 ZCPO为什么把KL放进组内零和系数，而不另外加一项KL loss？ 独立KL项在奖励没有区分或奖励梯度抵消时仍可能推动策略。ZCPO把响应平均条件KL的相对漂移与组内奖励一起中心化，再放入原策略surrogate。奖励尺度为零或组不合格时跳过整组，还需避免优化器权重衰减造成无信号更新，不能只返回零损失。 教学例子：一组回答全得相同奖励，本来没有相对学习方向；额外KL仍可能改模型，所以要明确整组是否真正跳过优化步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-16d59c38f113dc65">ZCPO为什么把KL放进组内零和系数，而不另外加一项KL loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Azcpo">When KL Regularization Misfires in Group Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立KL项在奖励没有区分或奖励梯度抵消时仍可能推动策略。ZCPO把响应平均条件KL的相对漂移与组内奖励一起中心化，再放入原策略surrogate。奖励尺度为零或组不合格时跳过整组，还需避免优化器权重衰减造成无信号更新，不能只返回零损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组回答全得相同奖励，本来没有相对学习方向；额外KL仍可能改模型，所以要明确整组是否真正跳过优化步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12161">原论文</a> · <a href="../../../../post-training/2610.12161-zcpo/">实现解读</a> · <a href="#qa-16d59c38f113dc65">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:zcpo" data-paper-title="When KL Regularization Misfires in Group Policy Optimization" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="When KL Regularization Misfires in Group Policy Optimization LLM 后训练 Alibaba Group 2026-10-08 独立 KL 惩罚可能在奖励相同或奖励梯度取消时继续更新策略。ZCPO 用响应平均的条件 KL 相对漂移，校准组内奖励系数；再将该系数放进原策略 surrogate，不另加独立 KL loss。 实际训练链路和边界检查已实现；24 步单 seed 诊断不是 AIME 收益复现。固定 Qwen3-4B 基础参考，训练 q/v LoRA；group=4、24 步、每响应最多 256 token，8 个独立验证问题。完整词表条件 KL、有效响应 mask、长度平均和 stop-gradient 均实际执行。见运行说明。  组相对策略优化 KL 校准 LLM 后训练 策略优化：谁在采样，谁在被更新 ZCPO条件KL与采样token的单点log-ratio可以互换吗？ 不能。规定信号是完整词表条件KL，先沿响应长度平均，再组内中心化。单点比值是不同估计，可能有很大采样波动，不能仅因都涉及log概率就替换。 例如某次采到的罕见词偏移，不代表整份条件分布的KL就是该数值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-65b69d8e4f98bf16">ZCPO条件KL与采样token的单点log-ratio可以互换吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Azcpo">When KL Regularization Misfires in Group Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。规定信号是完整词表条件KL，先沿响应长度平均，再组内中心化。单点比值是不同估计，可能有很大采样波动，不能仅因都涉及log概率就替换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某次采到的罕见词偏移，不代表整份条件分布的KL就是该数值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12161">原论文</a> · <a href="../../../../post-training/2610.12161-zcpo/">实现解读</a> · <a href="#qa-65b69d8e4f98bf16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:zcpo" data-paper-title="When KL Regularization Misfires in Group Policy Optimization" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="When KL Regularization Misfires in Group Policy Optimization LLM 后训练 Alibaba Group 2026-10-08 独立 KL 惩罚可能在奖励相同或奖励梯度取消时继续更新策略。ZCPO 用响应平均的条件 KL 相对漂移，校准组内奖励系数；再将该系数放进原策略 surrogate，不另加独立 KL loss。 实际训练链路和边界检查已实现；24 步单 seed 诊断不是 AIME 收益复现。固定 Qwen3-4B 基础参考，训练 q/v LoRA；group=4、24 步、每响应最多 256 token，8 个独立验证问题。完整词表条件 KL、有效响应 mask、长度平均和 stop-gradient 均实际执行。见运行说明。  组相对策略优化 KL 校准 LLM 后训练 策略优化：谁在采样，谁在被更新 ZCPO奖励全相同的组为什么必须跳过optimizer更新？ 奖励尺度为零会产生除零，且空损失仍执行AdamW可能通过权重衰减改参数。整组应跳过；组大小不足也不进入该相对系数计算，不能只把系数填零后照常step。 例如日志显示梯度零，但权重衰减仍能改模型，因此跳过与零梯度不是同一件事。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3d89399c52763499">ZCPO奖励全相同的组为什么必须跳过optimizer更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Azcpo">When KL Regularization Misfires in Group Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>奖励尺度为零会产生除零，且空损失仍执行AdamW可能通过权重衰减改参数。整组应跳过；组大小不足也不进入该相对系数计算，不能只把系数填零后照常step。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如日志显示梯度零，但权重衰减仍能改模型，因此跳过与零梯度不是同一件事。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12161">原论文</a> · <a href="../../../../post-training/2610.12161-zcpo/">实现解读</a> · <a href="#qa-3d89399c52763499">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gmc-grpo" data-paper-title="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis LLM 后训练 The Ohio State University 2026-10-01 异步 rollout 的重要性比在 group 级统一缩放，使总质量受帽约束；在共同二阶矩保证下减少 trajectory-wise clipping 的持续偏差。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 group mass capping；未搭建异步 RL 集群。执行 group mass capping；未搭建异步 RL 集群。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  异步 RL GRPO 重要性采样 LLM 后训练 策略优化：谁在采样，谁在被更新 GMC-GRPO为什么按组限制重要性总质量？ 异步样本来自较旧策略，某些比值可能很大。按整个组同系数缩放，可约束总质量，同时保持组内原比值比例，减少逐轨迹各自截断带来的结构改变。 例如一组所有比值一起放大时，统一缩小而非只切掉其中最大一条。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gmc-grpo-1030f809" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4530e4fc6872ebb5">GMC-GRPO为什么按组限制重要性总质量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agmc-grpo">Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>异步样本来自较旧策略，某些比值可能很大。按整个组同系数缩放，可约束总质量，同时保持组内原比值比例，减少逐轨迹各自截断带来的结构改变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一组所有比值一起放大时，统一缩小而非只切掉其中最大一条。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01896">原论文</a> · <a href="../../../../post-training/2610.01896-gmc-grpo/">实现解读</a> · <a href="#qa-4530e4fc6872ebb5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gmc-grpo" data-paper-title="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis LLM 后训练 The Ohio State University 2026-10-01 异步 rollout 的重要性比在 group 级统一缩放，使总质量受帽约束；在共同二阶矩保证下减少 trajectory-wise clipping 的持续偏差。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 group mass capping；未搭建异步 RL 集群。执行 group mass capping；未搭建异步 RL 集群。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  异步 RL GRPO 重要性采样 LLM 后训练 策略优化：谁在采样，谁在被更新 GMC-GRPO为什么统一缩放整组重要性比，而不把每条轨迹各自截断？ 逐条截断会不均匀改变组内样本之间的比例。组质量封顶在总比率过大时用同一个因子缩放，保持相对比例而限制总权重。它控制的是组层面质量，仍依赖采样和矩条件；在公式上计算这一步，不代表已经搭建并验证异步训练系统。 教学例子：一组旧轨迹的比率总量过大，统一缩小可保留彼此相对贡献；分别裁平可能让原本不同的重要性看起来一样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c6f729f6a888dc53">GMC-GRPO为什么统一缩放整组重要性比，而不把每条轨迹各自截断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agmc-grpo">Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐条截断会不均匀改变组内样本之间的比例。组质量封顶在总比率过大时用同一个因子缩放，保持相对比例而限制总权重。它控制的是组层面质量，仍依赖采样和矩条件；在公式上计算这一步，不代表已经搭建并验证异步训练系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组旧轨迹的比率总量过大，统一缩小可保留彼此相对贡献；分别裁平可能让原本不同的重要性看起来一样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01896">原论文</a> · <a href="../../../../post-training/2610.01896-gmc-grpo/">实现解读</a> · <a href="#qa-c6f729f6a888dc53">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gmc-grpo" data-paper-title="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis LLM 后训练 The Ohio State University 2026-10-01 异步 rollout 的重要性比在 group 级统一缩放，使总质量受帽约束；在共同二阶矩保证下减少 trajectory-wise clipping 的持续偏差。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 group mass capping；未搭建异步 RL 集群。执行 group mass capping；未搭建异步 RL 集群。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  异步 RL GRPO 重要性采样 LLM 后训练 策略优化：谁在采样，谁在被更新 组质量帽与逐轨迹clipping保留的关系有什么不同？ 组帽让所有比值乘相同因子，组内相对比例不变；独立裁剪会改变彼此比例。其理论结论还依赖共同二阶矩等条件，不表示任何异步陈旧程度都能修复。 例如大比值与中比值在独立截断后可能接近，而统一缩放仍保留它们比率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4eea76d90300a7b0">组质量帽与逐轨迹clipping保留的关系有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agmc-grpo">Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组帽让所有比值乘相同因子，组内相对比例不变；独立裁剪会改变彼此比例。其理论结论还依赖共同二阶矩等条件，不表示任何异步陈旧程度都能修复。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如大比值与中比值在独立截断后可能接近，而统一缩放仍保留它们比率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01896">原论文</a> · <a href="../../../../post-training/2610.01896-gmc-grpo/">实现解读</a> · <a href="#qa-4eea76d90300a7b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gmc-grpo" data-paper-title="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis LLM 后训练 The Ohio State University 2026-10-01 异步 rollout 的重要性比在 group 级统一缩放，使总质量受帽约束；在共同二阶矩保证下减少 trajectory-wise clipping 的持续偏差。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 group mass capping；未搭建异步 RL 集群。执行 group mass capping；未搭建异步 RL 集群。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  异步 RL GRPO 重要性采样 LLM 后训练 策略优化：谁在采样，谁在被更新 GMC权重在总质量低于帽时应怎样变化？ 缩放系数为一，原比值不变；超过帽才乘帽除总和。需核对比值非负及分组边界，本地只验证质量帽核，未构建异步训练集群或测吞吐。 例如两个不同提示组不能合并总和，否则一组极大比值会影响另一组。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1610e7e0c7bb3600">GMC权重在总质量低于帽时应怎样变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agmc-grpo">Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缩放系数为一，原比值不变；超过帽才乘帽除总和。需核对比值非负及分组边界，本地只验证质量帽核，未构建异步训练集群或测吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个不同提示组不能合并总和，否则一组极大比值会影响另一组。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01896">原论文</a> · <a href="../../../../post-training/2610.01896-gmc-grpo/">实现解读</a> · <a href="#qa-1610e7e0c7bb3600">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:range-grpo" data-paper-title="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals LLM 后训练 Yonsei University 2026-10-01 用 conformal reward interval 代替单点 judge 分数；组内只对可确定排序的区间产生方向信号，区间重叠时不制造虚假偏好。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  GRPO 奖励区间 半监督后训练 LLM 后训练 策略优化：谁在采样，谁在被更新 Range-GRPO为什么给奖励区间而非只信一个裁判分数？ 单点评分掩盖估计不确定性，区间让组内关系承认哪些顺序尚不能确定。只有可判定的区间关系提供方向，避免将微小噪声差硬转成偏好。 例如两个评分的可能范围大量重叠，就不强行说其中一个明显更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-range-grpo-b66c385f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a15f72e3b4bd2e6e">Range-GRPO为什么给奖励区间而非只信一个裁判分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arange-grpo">Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yonsei University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单点评分掩盖估计不确定性，区间让组内关系承认哪些顺序尚不能确定。只有可判定的区间关系提供方向，避免将微小噪声差硬转成偏好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个评分的可能范围大量重叠，就不强行说其中一个明显更好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01548">原论文</a> · <a href="../../../../post-training/2610.01548-range-grpo/">实现解读</a> · <a href="#qa-a15f72e3b4bd2e6e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:range-grpo" data-paper-title="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals LLM 后训练 Yonsei University 2026-10-01 用 conformal reward interval 代替单点 judge 分数；组内只对可确定排序的区间产生方向信号，区间重叠时不制造虚假偏好。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  GRPO 奖励区间 半监督后训练 LLM 后训练 策略优化：谁在采样，谁在被更新 奖励区间重叠时，Range-GRPO为什么不强行给两条回答排出先后？ 点估计的微小差别可能只是裁判不确定性。Range-GRPO比较校准区间的可确定关系，重叠时不制造方向信号，再在组内聚合相对优势；区间退化为点时回到对应点奖励情形。区间可信性依赖校准协议，只有区间关系算子并不等于已训练可靠judge。 教学例子：两个回答的质量估计范围大幅重叠，不能因一个中心值略高就当作明确优例；先保留无法确定的关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-58d186d40a148b8d">奖励区间重叠时，Range-GRPO为什么不强行给两条回答排出先后？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arange-grpo">Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yonsei University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点估计的微小差别可能只是裁判不确定性。Range-GRPO比较校准区间的可确定关系，重叠时不制造方向信号，再在组内聚合相对优势；区间退化为点时回到对应点奖励情形。区间可信性依赖校准协议，只有区间关系算子并不等于已训练可靠judge。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个回答的质量估计范围大幅重叠，不能因一个中心值略高就当作明确优例；先保留无法确定的关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01548">原论文</a> · <a href="../../../../post-training/2610.01548-range-grpo/">实现解读</a> · <a href="#qa-58d186d40a148b8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:range-grpo" data-paper-title="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals LLM 后训练 Yonsei University 2026-10-01 用 conformal reward interval 代替单点 judge 分数；组内只对可确定排序的区间产生方向信号，区间重叠时不制造虚假偏好。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  GRPO 奖励区间 半监督后训练 LLM 后训练 策略优化：谁在采样，谁在被更新 区间重叠置为不确定，与把区间中点排序有何不同？ 中点排序总能给出方向，即使差异远小于不确定范围；区间关系选择保守地不给这类伪信号。代价是监督可能更稀疏，不能无对照就断言训练更快或更好。 例如两区间中点一高一低但范围重叠，保守方法不把这个小差当确定胜负。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e90be0ef0d21656e">区间重叠置为不确定，与把区间中点排序有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arange-grpo">Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yonsei University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>中点排序总能给出方向，即使差异远小于不确定范围；区间关系选择保守地不给这类伪信号。代价是监督可能更稀疏，不能无对照就断言训练更快或更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两区间中点一高一低但范围重叠，保守方法不把这个小差当确定胜负。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01548">原论文</a> · <a href="../../../../post-training/2610.01548-range-grpo/">实现解读</a> · <a href="#qa-e90be0ef0d21656e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:range-grpo" data-paper-title="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals LLM 后训练 Yonsei University 2026-10-01 用 conformal reward interval 代替单点 judge 分数；组内只对可确定排序的区间产生方向信号，区间重叠时不制造虚假偏好。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  GRPO 奖励区间 半监督后训练 LLM 后训练 策略优化：谁在采样，谁在被更新 Range-GRPO本地实现是否已经校准conformal裁判？ 没有。它接收给定区间并计算成对关系与点极限；区间覆盖保证还需真实校准数据和裁判流程。区间退化为点时应检查相应DR-GRPO极限，而非随意平滑。 例如输入一个很宽区间通过测试，只说明关系核能处理，不证明其覆盖率正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-50dbc843fd89d3de">Range-GRPO本地实现是否已经校准conformal裁判？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arange-grpo">Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yonsei University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。它接收给定区间并计算成对关系与点极限；区间覆盖保证还需真实校准数据和裁判流程。区间退化为点时应检查相应DR-GRPO极限，而非随意平滑。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如输入一个很宽区间通过测试，只说明关系核能处理，不证明其覆盖率正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01548">原论文</a> · <a href="../../../../post-training/2610.01548-range-grpo/">实现解读</a> · <a href="#qa-50dbc843fd89d3de">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcpr" data-paper-title="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration LLM 后训练 National University of Singapore 2026-10-01 概率奖励在同组推理后验接近时难以区分冗长推理；RLCPR 只对“全组都长、答案后验又集中”的组施加相对长度惩罚。另用直接作答时的 token 平均熵把数据分层，让保留分布偏向低不确定样本。 L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；未运行完整语言模型 RL。调用方必须提供真实模型 token 熵、答案后验、长度及策略更新；本地手工输入是公式诊断，不是推理正确率或模型 RL 收益。没有 GPU/Evolve 正式能力集成。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：短且后验分散的组不受惩罚；长且集中的组最长 rollout 惩罚为 -1，最短不罚。低熵样本保留概率约 0.333，高熵约 0.100。见产物。  后验集中与长度约束 强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 RLCPR为什么不对所有长回答统一扣长度分？ 长推理有时必要。只有全组都偏长且答案后验已集中时，额外长度更可能没有区分价值，才启用组内相对惩罚；因此它保留针对困难不确定推理的空间。 例如一组都已很确定却反复解释，可与仍在探索关键分叉的长回答区别处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rlcpr-dde5901c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f17b3c74251f3a07">RLCPR为什么不对所有长回答统一扣长度分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcpr">RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长推理有时必要。只有全组都偏长且答案后验已集中时，额外长度更可能没有区分价值，才启用组内相对惩罚；因此它保留针对困难不确定推理的空间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一组都已很确定却反复解释，可与仍在探索关键分叉的长回答区别处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01458">原论文</a> · <a href="../../../../post-training/2610.01458-rlcpr/">实现解读</a> · <a href="#qa-f17b3c74251f3a07">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcpr" data-paper-title="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration LLM 后训练 National University of Singapore 2026-10-01 概率奖励在同组推理后验接近时难以区分冗长推理；RLCPR 只对“全组都长、答案后验又集中”的组施加相对长度惩罚。另用直接作答时的 token 平均熵把数据分层，让保留分布偏向低不确定样本。 L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；未运行完整语言模型 RL。调用方必须提供真实模型 token 熵、答案后验、长度及策略更新；本地手工输入是公式诊断，不是推理正确率或模型 RL 收益。没有 GPU/Evolve 正式能力集成。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：短且后验分散的组不受惩罚；长且集中的组最长 rollout 惩罚为 -1，最短不罚。低熵样本保留概率约 0.333，高熵约 0.100。见产物。  后验集中与长度约束 强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 RLCPR为什么只有全组都长且答案后验集中时才加相对长度惩罚？ 后验接近说明这些推理给答案提供的区分有限，全组都长时才有理由压缩相对冗余。门控同时满足后，惩罚依据组内相对长度而非统一固定阈值；等号边界和分位数口径都重要。输入后验与熵须来自真实模型，手工数值只验证公式。 教学例子：同题几条回答都很长且答案概率近似，可尝试偏向较短者；若长回答明显提高答案支持，就不应照样惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-524181a96eb45723">RLCPR为什么只有全组都长且答案后验集中时才加相对长度惩罚？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcpr">RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后验接近说明这些推理给答案提供的区分有限，全组都长时才有理由压缩相对冗余。门控同时满足后，惩罚依据组内相对长度而非统一固定阈值；等号边界和分位数口径都重要。输入后验与熵须来自真实模型，手工数值只验证公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题几条回答都很长且答案概率近似，可尝试偏向较短者；若长回答明显提高答案支持，就不应照样惩罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01458">原论文</a> · <a href="../../../../post-training/2610.01458-rlcpr/">实现解读</a> · <a href="#qa-524181a96eb45723">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcpr" data-paper-title="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration LLM 后训练 National University of Singapore 2026-10-01 概率奖励在同组推理后验接近时难以区分冗长推理；RLCPR 只对“全组都长、答案后验又集中”的组施加相对长度惩罚。另用直接作答时的 token 平均熵把数据分层，让保留分布偏向低不确定样本。 L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；未运行完整语言模型 RL。调用方必须提供真实模型 token 熵、答案后验、长度及策略更新；本地手工输入是公式诊断，不是推理正确率或模型 RL 收益。没有 GPU/Evolve 正式能力集成。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：短且后验分散的组不受惩罚；长且集中的组最长 rollout 惩罚为 -1，最短不罚。低熵样本保留概率约 0.333，高熵约 0.100。见产物。  后验集中与长度约束 强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 RLCPR的熵分层与长度门控是同一选择吗？ 熵分层在采样数据前调节保留分布，长度与后验门控在生成组内决定奖励修正。二者时点和变量不同，不能用一个全局长度阈值替代整条流程。 例如先决定更常抽哪类题，再判断该题本轮回答是否普遍冗长，是两步。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-89ed669827603c39">RLCPR的熵分层与长度门控是同一选择吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcpr">RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>熵分层在采样数据前调节保留分布，长度与后验门控在生成组内决定奖励修正。二者时点和变量不同，不能用一个全局长度阈值替代整条流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先决定更常抽哪类题，再判断该题本轮回答是否普遍冗长，是两步。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01458">原论文</a> · <a href="../../../../post-training/2610.01458-rlcpr/">实现解读</a> · <a href="#qa-89ed669827603c39">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcpr" data-paper-title="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration LLM 后训练 National University of Singapore 2026-10-01 概率奖励在同组推理后验接近时难以区分冗长推理；RLCPR 只对“全组都长、答案后验又集中”的组施加相对长度惩罚。另用直接作答时的 token 平均熵把数据分层，让保留分布偏向低不确定样本。 L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；未运行完整语言模型 RL。调用方必须提供真实模型 token 熵、答案后验、长度及策略更新；本地手工输入是公式诊断，不是推理正确率或模型 RL 收益。没有 GPU/Evolve 正式能力集成。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：短且后验分散的组不受惩罚；长且集中的组最长 rollout 惩罚为 -1，最短不罚。低熵样本保留概率约 0.333，高熵约 0.100。见产物。  后验集中与长度约束 强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 RLCPR门控遇到等于长度或后验阈值时是否激活？ 原条件使用严格大于最短长度阈值和严格小于后验极差阈值，等号不激活。熵CDF也用严格小于处理并列值；本地手工量只验证公式，不是实际RL收益。 例如组最短长度正好落在阈值上，不能改成大于等于以多惩罚一些样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2deca80ebb108f1b">RLCPR门控遇到等于长度或后验阈值时是否激活？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcpr">RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原条件使用严格大于最短长度阈值和严格小于后验极差阈值，等号不激活。熵CDF也用严格小于处理并列值；本地手工量只验证公式，不是实际RL收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如组最短长度正好落在阈值上，不能改成大于等于以多惩罚一些样本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01458">原论文</a> · <a href="../../../../post-training/2610.01458-rlcpr/">实现解读</a> · <a href="#qa-2deca80ebb108f1b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpening-tax" data-paper-title="Sharpening Tax in Post-Training" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Sharpening Tax in Post-Training LLM 后训练 Meta Superintelligence Labs / University of Wisconsin–Madison 2026-10-01 比较 base 与后训练策略在固定采样预算下的任务覆盖；再用 posterior-tempered group sampling 按估计难度调温，兼顾 pass@1 与覆盖率。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RL 后训练 覆盖率 Agentic RL LLM 后训练 策略优化：谁在采样，谁在被更新 Sharpening Tax为何同时观察单次成功与固定预算覆盖？ 后训练可能提高常见正确路径概率，却减少其他任务或解法的可达性。固定采样预算下的覆盖差揭示这种代价，避免只凭单次成功率判断能力边界扩大。 例如某题从偶尔对变常对，但另一类题再也采不到正确解，覆盖可能下降。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-sharpening-tax-09653801" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b1670c70f32180f7">Sharpening Tax为何同时观察单次成功与固定预算覆盖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asharpening-tax">Sharpening Tax in Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后训练可能提高常见正确路径概率，却减少其他任务或解法的可达性。固定采样预算下的覆盖差揭示这种代价，避免只凭单次成功率判断能力边界扩大。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某题从偶尔对变常对，但另一类题再也采不到正确解，覆盖可能下降。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01509">原论文</a> · <a href="../../../../post-training/2610.01509-sharpening-tax/">实现解读</a> · <a href="#qa-b1670c70f32180f7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpening-tax" data-paper-title="Sharpening Tax in Post-Training" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Sharpening Tax in Post-Training LLM 后训练 Meta Superintelligence Labs / University of Wisconsin–Madison 2026-10-01 比较 base 与后训练策略在固定采样预算下的任务覆盖；再用 posterior-tempered group sampling 按估计难度调温，兼顾 pass@1 与覆盖率。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RL 后训练 覆盖率 Agentic RL LLM 后训练 策略优化：谁在采样，谁在被更新 pass@1提高时，Sharpening Tax为什么仍要比较固定预算下的任务覆盖？ 后训练可能把概率集中到熟悉解法，让一次命中更高，却失去某些只有多次采样才能找到的解。覆盖差比较基座与后训练策略在同一预算能解决哪些任务，再据难度调温。单次准确率、token熵和任务覆盖不是同一指标，不能用一个替代另一个。 教学例子：模型对常见题更确定，但再也采不到一类罕见正确解；只看首个答案的表现，可能完全看不见这部分覆盖损失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7fe59e1e2e6de973">pass@1提高时，Sharpening Tax为什么仍要比较固定预算下的任务覆盖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asharpening-tax">Sharpening Tax in Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后训练可能把概率集中到熟悉解法，让一次命中更高，却失去某些只有多次采样才能找到的解。覆盖差比较基座与后训练策略在同一预算能解决哪些任务，再据难度调温。单次准确率、token熵和任务覆盖不是同一指标，不能用一个替代另一个。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型对常见题更确定，但再也采不到一类罕见正确解；只看首个答案的表现，可能完全看不见这部分覆盖损失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01509">原论文</a> · <a href="../../../../post-training/2610.01509-sharpening-tax/">实现解读</a> · <a href="#qa-7fe59e1e2e6de973">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpening-tax" data-paper-title="Sharpening Tax in Post-Training" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Sharpening Tax in Post-Training LLM 后训练 Meta Superintelligence Labs / University of Wisconsin–Madison 2026-10-01 比较 base 与后训练策略在固定采样预算下的任务覆盖；再用 posterior-tempered group sampling 按估计难度调温，兼顾 pass@1 与覆盖率。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RL 后训练 覆盖率 Agentic RL LLM 后训练 策略优化：谁在采样，谁在被更新 后验调温与简单所有题都提高温度有什么差别？ 按估计难度分配组采样温度，试图在利用与覆盖间做条件化取舍；全局升温对已掌握和困难题一视同仁。估计错误也会影响分配，不能视作保证恢复全部覆盖。 例如熟练题无需同样强探索，困难题可能需要更多分支，而不是统一变随机。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4b1a6a6ef598e60f">后验调温与简单所有题都提高温度有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asharpening-tax">Sharpening Tax in Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按估计难度分配组采样温度，试图在利用与覆盖间做条件化取舍；全局升温对已掌握和困难题一视同仁。估计错误也会影响分配，不能视作保证恢复全部覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如熟练题无需同样强探索，困难题可能需要更多分支，而不是统一变随机。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01509">原论文</a> · <a href="../../../../post-training/2610.01509-sharpening-tax/">实现解读</a> · <a href="#qa-4b1a6a6ef598e60f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpening-tax" data-paper-title="Sharpening Tax in Post-Training" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Sharpening Tax in Post-Training LLM 后训练 Meta Superintelligence Labs / University of Wisconsin–Madison 2026-10-01 比较 base 与后训练策略在固定采样预算下的任务覆盖；再用 posterior-tempered group sampling 按估计难度调温，兼顾 pass@1 与覆盖率。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RL 后训练 覆盖率 Agentic RL LLM 后训练 策略优化：谁在采样，谁在被更新 Tax_K计算时为什么必须固定K及两策略输入集合？ 覆盖随采样次数和题目集合变化，两边预算或样本不同会混入比较偏差。定义为base覆盖减post覆盖，正负号应保留；本地仅执行指标核，不含原模型实验。 例如base采很多次而post只采一次，得到的差不能解释为后训练本身的税。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cdbe2496774f9c56">Tax_K计算时为什么必须固定K及两策略输入集合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asharpening-tax">Sharpening Tax in Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>覆盖随采样次数和题目集合变化，两边预算或样本不同会混入比较偏差。定义为base覆盖减post覆盖，正负号应保留；本地仅执行指标核，不含原模型实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如base采很多次而post只采一次，得到的差不能解释为后训练本身的税。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01509">原论文</a> · <a href="../../../../post-training/2610.01509-sharpening-tax/">实现解读</a> · <a href="#qa-cdbe2496774f9c56">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:graft" data-paper-title="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR LLM 后训练 KAIST 2026-09-29 当 receiver 的 rollout group 全错、peer 在同题同时有成功和失败轨迹时，GRAFT 用完整 peer group 替换无信号组并保留 peer 内部 advantage。跨 tokenizer 的策略错配通过序列平均 log-likelihood compatibility 加权，再用 token importance ratio clipping 限制更新。 复现级别：L1 目标机制。复现级别：L1 目标机制。实现 peer compatibility gate、source advantage 保留与 token ratio clipping。本地目标检查低兼容 peer 被降权、ratio 越界被截断且 advantage 不回传；三种子机制结果见 metrics/mechanism-seeds42-44.json。未进行双模型 GRPO 联训或五个数学 benchmark，故不宣称论文平均 +2.1 分收益。  RLVR 跨模型轨迹交换 离策略校正 LLM 后训练 策略优化：谁在采样，谁在被更新 GRAFT什么时候才借用peer轨迹组？ receiver全失败而peer同题组内既有成功又有失败时，才有可迁移的相对优势信号。不是每次都借最强模型答案，也不是只复制peer的一条正确轨迹。 例如receiver四条都错，peer组内有对有错，后者才提供组内可区分反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-graft-20b4d98a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bfafd4bf9c31e789">GRAFT什么时候才借用peer轨迹组？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agraft">Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>receiver全失败而peer同题组内既有成功又有失败时，才有可迁移的相对优势信号。不是每次都借最强模型答案，也不是只复制peer的一条正确轨迹。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如receiver四条都错，peer组内有对有错，后者才提供组内可区分反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37868">原论文</a> · <a href="../../../../post-training/2609.37868-graft/">实现解读</a> · <a href="#qa-bfafd4bf9c31e789">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:graft" data-paper-title="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR LLM 后训练 KAIST 2026-09-29 当 receiver 的 rollout group 全错、peer 在同题同时有成功和失败轨迹时，GRAFT 用完整 peer group 替换无信号组并保留 peer 内部 advantage。跨 tokenizer 的策略错配通过序列平均 log-likelihood compatibility 加权，再用 token importance ratio clipping 限制更新。 复现级别：L1 目标机制。复现级别：L1 目标机制。实现 peer compatibility gate、source advantage 保留与 token ratio clipping。本地目标检查低兼容 peer 被降权、ratio 越界被截断且 advantage 不回传；三种子机制结果见 metrics/mechanism-seeds42-44.json。未进行双模型 GRPO 联训或五个数学 benchmark，故不宣称论文平均 +2.1 分收益。  RLVR 跨模型轨迹交换 离策略校正 LLM 后训练 策略优化：谁在采样，谁在被更新 GRAFT为什么交换同题完整peer组，而不只挑peer的一条成功回答？ receiver全错组缺少区分信号，完整peer组同时保留成功与失败及其内部相对优势。只取成功例会改变组结构和信用。跨模型尤其跨tokenizer时，还需序列兼容性与token比率裁剪处理错配；交换来的数据不能被标成receiver自己的在策略采样。 教学例子：模型甲同题全错，模型乙有对有错。把乙的整组连同组内信用交给甲学习，与单独塞入一份标准答案不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4a8a72e7c33e77d4">GRAFT为什么交换同题完整peer组，而不只挑peer的一条成功回答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agraft">Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>receiver全错组缺少区分信号，完整peer组同时保留成功与失败及其内部相对优势。只取成功例会改变组结构和信用。跨模型尤其跨tokenizer时，还需序列兼容性与token比率裁剪处理错配；交换来的数据不能被标成receiver自己的在策略采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型甲同题全错，模型乙有对有错。把乙的整组连同组内信用交给甲学习，与单独塞入一份标准答案不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37868">原论文</a> · <a href="../../../../post-training/2609.37868-graft/">实现解读</a> · <a href="#qa-4a8a72e7c33e77d4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:graft" data-paper-title="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR LLM 后训练 KAIST 2026-09-29 当 receiver 的 rollout group 全错、peer 在同题同时有成功和失败轨迹时，GRAFT 用完整 peer group 替换无信号组并保留 peer 内部 advantage。跨 tokenizer 的策略错配通过序列平均 log-likelihood compatibility 加权，再用 token importance ratio clipping 限制更新。 复现级别：L1 目标机制。复现级别：L1 目标机制。实现 peer compatibility gate、source advantage 保留与 token ratio clipping。本地目标检查低兼容 peer 被降权、ratio 越界被截断且 advantage 不回传；三种子机制结果见 metrics/mechanism-seeds42-44.json。未进行双模型 GRPO 联训或五个数学 benchmark，故不宣称论文平均 +2.1 分收益。  RLVR 跨模型轨迹交换 离策略校正 LLM 后训练 策略优化：谁在采样，谁在被更新 借完整peer组与只塞一条成功答案有何差别？ 完整替换保留peer原组内部优势关系；只加正例会改变组分布及信用基准。借用仍是跨策略数据，不能标成receiver自身的on-policy生成。 例如peer失败轨迹也保留，才能解释为什么组内成功轨迹获得相对正优势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-18fb1d6cc0e5ef2d">借完整peer组与只塞一条成功答案有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agraft">Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整替换保留peer原组内部优势关系；只加正例会改变组分布及信用基准。借用仍是跨策略数据，不能标成receiver自身的on-policy生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如peer失败轨迹也保留，才能解释为什么组内成功轨迹获得相对正优势。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37868">原论文</a> · <a href="../../../../post-training/2609.37868-graft/">实现解读</a> · <a href="#qa-18fb1d6cc0e5ef2d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:graft" data-paper-title="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR LLM 后训练 KAIST 2026-09-29 当 receiver 的 rollout group 全错、peer 在同题同时有成功和失败轨迹时，GRAFT 用完整 peer group 替换无信号组并保留 peer 内部 advantage。跨 tokenizer 的策略错配通过序列平均 log-likelihood compatibility 加权，再用 token importance ratio clipping 限制更新。 复现级别：L1 目标机制。复现级别：L1 目标机制。实现 peer compatibility gate、source advantage 保留与 token ratio clipping。本地目标检查低兼容 peer 被降权、ratio 越界被截断且 advantage 不回传；三种子机制结果见 metrics/mechanism-seeds42-44.json。未进行双模型 GRPO 联训或五个数学 benchmark，故不宣称论文平均 +2.1 分收益。  RLVR 跨模型轨迹交换 离策略校正 LLM 后训练 策略优化：谁在采样，谁在被更新 跨tokenizer的GRAFT为什么先用序列平均似然衡量兼容性？ 不同分词造成词元级一一对应困难，序列平均似然提供整体兼容信号，再用重要性比裁剪限制更新。它不使两模型策略自动相同，来源、组内优势和文本重评分需可追踪。 例如同一句话被拆成不同数量词元，不能按位置直接相减两个模型词元概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a391696ae8153767">跨tokenizer的GRAFT为什么先用序列平均似然衡量兼容性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agraft">Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同分词造成词元级一一对应困难，序列平均似然提供整体兼容信号，再用重要性比裁剪限制更新。它不使两模型策略自动相同，来源、组内优势和文本重评分需可追踪。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一句话被拆成不同数量词元，不能按位置直接相减两个模型词元概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37868">原论文</a> · <a href="../../../../post-training/2609.37868-graft/">实现解读</a> · <a href="#qa-a391696ae8153767">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rfpo" data-paper-title="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training LLM 后训练 University of Luxembourg 2026-09-29 冻结已校准 critic，把前缀成功概率同时作为 rollout reward、GAE baseline 和未完成轨迹预报，并在去长度偏置后二值化，降低策略利用 critic 偏差的风险。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  RL 冻结 Critic 无标签奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 RFPO的reward-free是不是不需要任何质量信号？ 它用已校准且冻结的critic预测前缀成功概率，替代训练时昂贵的外部终局奖励。监督被转移到critic而非消失，critic可靠性仍决定信号质量。 例如未完成解答可获得成功预估，但这来自已有评价能力，不是凭空知道答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rfpo-964b9a42" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-679b738a1f593837">RFPO的reward-free是不是不需要任何质量信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arfpo">Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Luxembourg</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用已校准且冻结的critic预测前缀成功概率，替代训练时昂贵的外部终局奖励。监督被转移到critic而非消失，critic可靠性仍决定信号质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如未完成解答可获得成功预估，但这来自已有评价能力，不是凭空知道答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37119">原论文</a> · <a href="../../../../post-training/2609.37119-rfpo/">实现解读</a> · <a href="#qa-679b738a1f593837">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rfpo" data-paper-title="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training LLM 后训练 University of Luxembourg 2026-09-29 冻结已校准 critic，把前缀成功概率同时作为 rollout reward、GAE baseline 和未完成轨迹预报，并在去长度偏置后二值化，降低策略利用 critic 偏差的风险。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  RL 冻结 Critic 无标签奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 RFPO冻结critic后，为什么还需要去长度偏置和二值化，不能直接最大化它的连续分数？ 冻结只阻止critic参数继续变化，不能消除其评分偏差。策略仍可能通过冗长或其他捷径提高分数，因此方法对前缀成功估计去偏并二值化，同时把critic用于基线和未完成轨迹预报。reward-free不等于无监督来源，而是复用已校准critic提供信号。 教学例子：critic偏爱长推理，学生即使不更正确也可靠加长拿高分；固定critic之后，这个可利用的偏差仍然存在。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-cfcc645e9e1f5910">RFPO冻结critic后，为什么还需要去长度偏置和二值化，不能直接最大化它的连续分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arfpo">Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Luxembourg</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结只阻止critic参数继续变化，不能消除其评分偏差。策略仍可能通过冗长或其他捷径提高分数，因此方法对前缀成功估计去偏并二值化，同时把critic用于基线和未完成轨迹预报。reward-free不等于无监督来源，而是复用已校准critic提供信号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>critic偏爱长推理，学生即使不更正确也可靠加长拿高分；固定critic之后，这个可利用的偏差仍然存在。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37119">原论文</a> · <a href="../../../../post-training/2609.37119-rfpo/">实现解读</a> · <a href="#qa-cfcc645e9e1f5910">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rfpo" data-paper-title="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training LLM 后训练 University of Luxembourg 2026-09-29 冻结已校准 critic，把前缀成功概率同时作为 rollout reward、GAE baseline 和未完成轨迹预报，并在去长度偏置后二值化，降低策略利用 critic 偏差的风险。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  RL 冻结 Critic 无标签奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 critic同时作奖励与baseline会带来什么额外风险？ 两种角色共享偏差时，策略可能利用critic盲点。去长度偏置和二值化用于限制这种利用，但不能保证评价器不受攻击，也不能用critic自身得分证明真实能力提升。 例如把冗长文字误判成更可能成功，策略就可能只学会拖长输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-17d352b39cff66da">critic同时作奖励与baseline会带来什么额外风险？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arfpo">Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Luxembourg</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两种角色共享偏差时，策略可能利用critic盲点。去长度偏置和二值化用于限制这种利用，但不能保证评价器不受攻击，也不能用critic自身得分证明真实能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把冗长文字误判成更可能成功，策略就可能只学会拖长输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37119">原论文</a> · <a href="../../../../post-training/2609.37119-rfpo/">实现解读</a> · <a href="#qa-17d352b39cff66da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rfpo" data-paper-title="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training LLM 后训练 University of Luxembourg 2026-09-29 冻结已校准 critic，把前缀成功概率同时作为 rollout reward、GAE baseline 和未完成轨迹预报，并在去长度偏置后二值化，降低策略利用 critic 偏差的风险。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  RL 冻结 Critic 无标签奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 RFPO为什么冻结critic，并区分未完成轨迹的预报？ 冻结保证策略训练期间评价基准明确，未完成预报用于处理尚无终局结果的轨迹，不能冒充已验证成功。当前本地只执行去偏、二值奖励和GAE核，未训练长推理模型。 例如截断轨迹的高成功预报要保留估计身份，不能直接标成真实答案正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ee0051c78752baa7">RFPO为什么冻结critic，并区分未完成轨迹的预报？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arfpo">Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Luxembourg</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结保证策略训练期间评价基准明确，未完成预报用于处理尚无终局结果的轨迹，不能冒充已验证成功。当前本地只执行去偏、二值奖励和GAE核，未训练长推理模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如截断轨迹的高成功预报要保留估计身份，不能直接标成真实答案正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37119">原论文</a> · <a href="../../../../post-training/2609.37119-rfpo/">实现解读</a> · <a href="#qa-ee0051c78752baa7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tlm-dre" data-paper-title="Turn-level Multiscale Density Ratio Estimation for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turn-level Multiscale Density Ratio Estimation for LLM Agents LLM 后训练 Alibaba Group 2026-09-15 按 turn 分配多尺度权重，并对正负 token 密度比采用非对称更新。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多轮 Agent 对齐 密度比估计 LLM 后训练 策略优化：谁在采样，谁在被更新 TLM-DRE为什么在turn层面建模而不只平均全部词元？ 多轮任务各轮贡献和长度不同，多尺度轮次权重能表达对话过程结构；把所有词元等权平均可能让长轮次支配信号。具体信用仍依赖输入密度比与反馈。 例如简短工具选择可能关键，不能因只有几个词就被冗长描述的梯度淹没。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-tlm-dre-7ebc851d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6dd63a8240c91c1f">TLM-DRE为什么在turn层面建模而不只平均全部词元？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atlm-dre">Turn-level Multiscale Density Ratio Estimation for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多轮任务各轮贡献和长度不同，多尺度轮次权重能表达对话过程结构；把所有词元等权平均可能让长轮次支配信号。具体信用仍依赖输入密度比与反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如简短工具选择可能关键，不能因只有几个词就被冗长描述的梯度淹没。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16760">原论文</a> · <a href="../../../../post-training/2609.16760-tlm-dre/">实现解读</a> · <a href="#qa-6dd63a8240c91c1f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tlm-dre" data-paper-title="Turn-level Multiscale Density Ratio Estimation for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turn-level Multiscale Density Ratio Estimation for LLM Agents LLM 后训练 Alibaba Group 2026-09-15 按 turn 分配多尺度权重，并对正负 token 密度比采用非对称更新。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多轮 Agent 对齐 密度比估计 LLM 后训练 策略优化：谁在采样，谁在被更新 tlm-DRE为什么提高低置信轮次的权重，而不是给每轮相同惩罚？ 参考策略的长度平均对数概率被用作训练充分程度的估计，低置信轮次获得更高尺度，改变多轮密度比及正负轨迹的不对称训练压力。它依赖置信与学习需求的关系，不声称低概率动作必错；本地仅执行权重与更新诊断，未验证真实Agent泛化。 教学例子：工具选择轮次犹豫、最后复述轮次很确定，可把更多校正压力放在前者；但低置信可能也来自合法的罕见动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8bf40a276febca62">tlm-DRE为什么提高低置信轮次的权重，而不是给每轮相同惩罚？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atlm-dre">Turn-level Multiscale Density Ratio Estimation for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参考策略的长度平均对数概率被用作训练充分程度的估计，低置信轮次获得更高尺度，改变多轮密度比及正负轨迹的不对称训练压力。它依赖置信与学习需求的关系，不声称低概率动作必错；本地仅执行权重与更新诊断，未验证真实Agent泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工具选择轮次犹豫、最后复述轮次很确定，可把更多校正压力放在前者；但低置信可能也来自合法的罕见动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16760">原论文</a> · <a href="../../../../post-training/2609.16760-tlm-dre/">实现解读</a> · <a href="#qa-8bf40a276febca62">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tlm-dre" data-paper-title="Turn-level Multiscale Density Ratio Estimation for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turn-level Multiscale Density Ratio Estimation for LLM Agents LLM 后训练 Alibaba Group 2026-09-15 按 turn 分配多尺度权重，并对正负 token 密度比采用非对称更新。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多轮 Agent 对齐 密度比估计 LLM 后训练 策略优化：谁在采样，谁在被更新 正负token密度比非对称更新与统一加权有什么差别？ 正负证据承担强化与抑制不同作用，非对称规则允许不同处理。统一规则会抹平这个设计，但非对称本身不证明对所有数据更好，需要真实多轮任务验证。 例如鼓励关键正确动作和压低错误续写，不必被假定具有同样的权重曲线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2313a70c65e97e9f">正负token密度比非对称更新与统一加权有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atlm-dre">Turn-level Multiscale Density Ratio Estimation for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正负证据承担强化与抑制不同作用，非对称规则允许不同处理。统一规则会抹平这个设计，但非对称本身不证明对所有数据更好，需要真实多轮任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如鼓励关键正确动作和压低错误续写，不必被假定具有同样的权重曲线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16760">原论文</a> · <a href="../../../../post-training/2609.16760-tlm-dre/">实现解读</a> · <a href="#qa-2313a70c65e97e9f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tlm-dre" data-paper-title="Turn-level Multiscale Density Ratio Estimation for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turn-level Multiscale Density Ratio Estimation for LLM Agents LLM 后训练 Alibaba Group 2026-09-15 按 turn 分配多尺度权重，并对正负 token 密度比采用非对称更新。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多轮 Agent 对齐 密度比估计 LLM 后训练 策略优化：谁在采样，谁在被更新 TLM-DRE本地轮权重核能代表真实多轮Agent训练吗？ 不能。当前只执行轮次权重与非对称词元更新的参考计算，未运行完整智能体环境。输入应保留词元所属轮次，不能把拼接文本直接当作一轮并沿用原方法名称。 例如三个工具轮次拼成长字符串后失去边界，就无法验证原本的turn分配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4f874be5c36b0fbe">TLM-DRE本地轮权重核能代表真实多轮Agent训练吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atlm-dre">Turn-level Multiscale Density Ratio Estimation for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前只执行轮次权重与非对称词元更新的参考计算，未运行完整智能体环境。输入应保留词元所属轮次，不能把拼接文本直接当作一轮并沿用原方法名称。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三个工具轮次拼成长字符串后失去边界，就无法验证原本的turn分配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16760">原论文</a> · <a href="../../../../post-training/2609.16760-tlm-dre/">实现解读</a> · <a href="#qa-4f874be5c36b0fbe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mad-rl" data-paper-title="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning LLM 后训练 Meta Superintelligence Labs 2026-09-12 逐条最大化正确性奖励可能令输出类别坍缩；MaD-RL为输出的类别频率拟合指定分布，而非仅提高token熵。它将组内频率与目标类别分布构造的L2、forward-KL、reverse-KL或JSD奖励，与任务正确性结合后用于GRPO。完整分布约束与正确性须分别测量。原文§2 完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。Google/Meta优先资料与实验关联。完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。既有实验、三种子结果与负结果仍是事实来源。字符GRU与Qwen3-4B五选项诊断不是原文自由数学/代码任务；Qwen三臂验证完全打平，未观察到分布奖励差异。已有A100回执绑定mad-rl-qwen-choice，不改键、不重新绑定到本资料条目；本轮没有新增CUDA路径或GPU交付。  在线强化学习 类别分布匹配奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 MaD-RL为什么约束输出类别分布，而不是仅增加词元熵？ 类别多样性描述语义结果频率，词元熵描述表面生成不确定性。模型可以措辞多样却总选同一类别，因此用经验类别分布与指定目标构造奖励，再与正确性结合。 例如写出许多不同句子却全推荐同一类物品，词元多样不等于类别覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-mad-rl-6dafc52d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9537d417371ba926">MaD-RL为什么约束输出类别分布，而不是仅增加词元熵？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amad-rl">MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>类别多样性描述语义结果频率，词元熵描述表面生成不确定性。模型可以措辞多样却总选同一类别，因此用经验类别分布与指定目标构造奖励，再与正确性结合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如写出许多不同句子却全推荐同一类物品，词元多样不等于类别覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31644">原论文</a> · <a href="../../../../post-training/2609.31644-mad-rl/">实现解读</a> · <a href="#qa-9537d417371ba926">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mad-rl" data-paper-title="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning LLM 后训练 Meta Superintelligence Labs 2026-09-12 逐条最大化正确性奖励可能令输出类别坍缩；MaD-RL为输出的类别频率拟合指定分布，而非仅提高token熵。它将组内频率与目标类别分布构造的L2、forward-KL、reverse-KL或JSD奖励，与任务正确性结合后用于GRPO。完整分布约束与正确性须分别测量。原文§2 完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。Google/Meta优先资料与实验关联。完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。既有实验、三种子结果与负结果仍是事实来源。字符GRU与Qwen3-4B五选项诊断不是原文自由数学/代码任务；Qwen三臂验证完全打平，未观察到分布奖励差异。已有A100回执绑定mad-rl-qwen-choice，不改键、不重新绑定到本资料条目；本轮没有新增CUDA路径或GPU交付。  在线强化学习 类别分布匹配奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 MaD-RL为什么约束输出类别频率，而不是只提高每个token的熵？ token更随机不保证最终类别更均衡。MaD-RL先把输出映射为类别，用经验频率与指定目标分布的差异构造奖励，再与任务正确性结合。频率在该次更新中视为固定，未采到的类别也不会凭空获得on-policy样本；类别判定与无效输出分母必须明确。 教学例子：模型可以用很多不同措辞反复给出同一类别，token多样但决策仍坍缩；应直接检查最终类别分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-83efe3e396c5af87">MaD-RL为什么约束输出类别频率，而不是只提高每个token的熵？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amad-rl">MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>token更随机不保证最终类别更均衡。MaD-RL先把输出映射为类别，用经验频率与指定目标分布的差异构造奖励，再与任务正确性结合。频率在该次更新中视为固定，未采到的类别也不会凭空获得on-policy样本；类别判定与无效输出分母必须明确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型可以用很多不同措辞反复给出同一类别，token多样但决策仍坍缩；应直接检查最终类别分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31644">原论文</a> · <a href="../../../../post-training/2609.31644-mad-rl/">实现解读</a> · <a href="#qa-83efe3e396c5af87">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mad-rl" data-paper-title="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning LLM 后训练 Meta Superintelligence Labs 2026-09-12 逐条最大化正确性奖励可能令输出类别坍缩；MaD-RL为输出的类别频率拟合指定分布，而非仅提高token熵。它将组内频率与目标类别分布构造的L2、forward-KL、reverse-KL或JSD奖励，与任务正确性结合后用于GRPO。完整分布约束与正确性须分别测量。原文§2 完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。Google/Meta优先资料与实验关联。完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。既有实验、三种子结果与负结果仍是事实来源。字符GRU与Qwen3-4B五选项诊断不是原文自由数学/代码任务；Qwen三臂验证完全打平，未观察到分布奖励差异。已有A100回执绑定mad-rl-qwen-choice，不改键、不重新绑定到本资料条目；本轮没有新增CUDA路径或GPU交付。  在线强化学习 类别分布匹配奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 类别分布匹配与单独最大化正确率会出现什么取舍？ 正确性奖励可能集中到最容易的类别，分布奖励则把质量分配拉向目标；二者需分别测量。匹配分布不保证每条正确，正确率高也不保证达到目标类别比例。 例如各类别数量均衡了，但某类回答仍错误，不能只报分布距离就算成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-293edb5053eb4a47">类别分布匹配与单独最大化正确率会出现什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amad-rl">MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确性奖励可能集中到最容易的类别，分布奖励则把质量分配拉向目标；二者需分别测量。匹配分布不保证每条正确，正确率高也不保证达到目标类别比例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如各类别数量均衡了，但某类回答仍错误，不能只报分布距离就算成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31644">原论文</a> · <a href="../../../../post-training/2609.31644-mad-rl/">实现解读</a> · <a href="#qa-293edb5053eb4a47">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mad-rl" data-paper-title="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning LLM 后训练 Meta Superintelligence Labs 2026-09-12 逐条最大化正确性奖励可能令输出类别坍缩；MaD-RL为输出的类别频率拟合指定分布，而非仅提高token熵。它将组内频率与目标类别分布构造的L2、forward-KL、reverse-KL或JSD奖励，与任务正确性结合后用于GRPO。完整分布约束与正确性须分别测量。原文§2 完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。Google/Meta优先资料与实验关联。完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。既有实验、三种子结果与负结果仍是事实来源。字符GRU与Qwen3-4B五选项诊断不是原文自由数学/代码任务；Qwen三臂验证完全打平，未观察到分布奖励差异。已有A100回执绑定mad-rl-qwen-choice，不改键、不重新绑定到本资料条目；本轮没有新增CUDA路径或GPU交付。  在线强化学习 类别分布匹配奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 MaD-RL统计类别频率时无效样本可以从分母删除吗？ 不能随意删去，否则改变经验分布和每类奖励。更新时频率视为固定，零目标概率需显式平滑，未采到类别也不会凭空收到on-policy梯度；本地诊断不等于完整模型训练。 例如把无法分类输出全部排除，会让剩余类别比例看似更符合目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-aabb50423710ae5d">MaD-RL统计类别频率时无效样本可以从分母删除吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amad-rl">MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能随意删去，否则改变经验分布和每类奖励。更新时频率视为固定，零目标概率需显式平滑，未采到类别也不会凭空收到on-policy梯度；本地诊断不等于完整模型训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把无法分类输出全部排除，会让剩余类别比例看似更符合目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31644">原论文</a> · <a href="../../../../post-training/2609.31644-mad-rl/">实现解读</a> · <a href="#qa-aabb50423710ae5d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tasco" data-paper-title="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning LLM 后训练 Chongqing University 2026-09-10 冻结主模型，优化轻量 prefix；除置信度外还惩罚邻域扰动下的不稳定，从而避免自信但错误的轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  测试时适配 稳定性优化 LLM 后训练 策略优化：谁在采样，谁在被更新 TASCO在测试时适配的是主模型权重，还是额外的轻量prefix？ 主模型冻结，适配对象是附加的轻量prefix。测试时优化因此仍会改变模型的条件输入表示，但不是重新训练全部骨干，也不是仅靠多采样选答案。它使用当前任务的无标签信号，不能把测试金标当成prefix优化目标。 教学例子：保持语言模型各层权重不动，只更新前缀向量，再重新读取该题分布；题目答案不参与更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-tasco-a3638c7c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6ae37dc4a87906c6">TASCO在测试时适配的是主模型权重，还是额外的轻量prefix？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atasco">Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chongqing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主模型冻结，适配对象是附加的轻量prefix。测试时优化因此仍会改变模型的条件输入表示，但不是重新训练全部骨干，也不是仅靠多采样选答案。它使用当前任务的无标签信号，不能把测试金标当成prefix优化目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>保持语言模型各层权重不动，只更新前缀向量，再重新读取该题分布；题目答案不参与更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11393">原论文</a> · <a href="../../../../post-training/2609.11393-tasco/">实现解读</a> · <a href="#qa-6ae37dc4a87906c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tasco" data-paper-title="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning LLM 后训练 Chongqing University 2026-09-10 冻结主模型，优化轻量 prefix；除置信度外还惩罚邻域扰动下的不稳定，从而避免自信但错误的轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  测试时适配 稳定性优化 LLM 后训练 策略优化：谁在采样，谁在被更新 TASCO只提高测试题置信度为什么不够，还要检查邻域扰动的稳定性？ 错误答案也可能被模型反复自信确认，仅优化置信会强化这种错误。TASCO冻结主模型，只调轻量前缀，并把邻域扰动下预测不稳定作为额外惩罚。它利用的是无标签稳定性线索，不是正确性oracle；本地扰动诊断没有加载真实LLM前缀。 教学例子：题目换一种等价说法，模型就从一个答案跳到另一个；即使原答案概率很高，这种不稳定也提示不能只按置信强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3bf3e360a7863e6c">TASCO只提高测试题置信度为什么不够，还要检查邻域扰动的稳定性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atasco">Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chongqing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>错误答案也可能被模型反复自信确认，仅优化置信会强化这种错误。TASCO冻结主模型，只调轻量前缀，并把邻域扰动下预测不稳定作为额外惩罚。它利用的是无标签稳定性线索，不是正确性oracle；本地扰动诊断没有加载真实LLM前缀。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>题目换一种等价说法，模型就从一个答案跳到另一个；即使原答案概率很高，这种不稳定也提示不能只按置信强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11393">原论文</a> · <a href="../../../../post-training/2609.11393-tasco/">实现解读</a> · <a href="#qa-3bf3e360a7863e6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tasco" data-paper-title="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning LLM 后训练 Chongqing University 2026-09-10 冻结主模型，优化轻量 prefix；除置信度外还惩罚邻域扰动下的不稳定，从而避免自信但错误的轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  测试时适配 稳定性优化 LLM 后训练 策略优化：谁在采样，谁在被更新 TASCO更新prefix与增加best-of-N采样，额外计算主要花在哪里？ prefix适配把计算用于优化可训练条件，再让冻结模型据此预测；best-of-N主要生成更多候选并依赖选择规则。二者的可训练状态和预算构成都不同，比较时需要计入优化前向、反向及候选生成，不能把相同候选数当相同成本。 教学例子：一种做几次prefix梯度更新后答题，另一种直接生成多份答案再筛选；次数相同也不是同一种工作量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7138500cadc224d7">TASCO更新prefix与增加best-of-N采样，额外计算主要花在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atasco">Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chongqing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>prefix适配把计算用于优化可训练条件，再让冻结模型据此预测；best-of-N主要生成更多候选并依赖选择规则。二者的可训练状态和预算构成都不同，比较时需要计入优化前向、反向及候选生成，不能把相同候选数当相同成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一种做几次prefix梯度更新后答题，另一种直接生成多份答案再筛选；次数相同也不是同一种工作量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11393">原论文</a> · <a href="../../../../post-training/2609.11393-tasco/">实现解读</a> · <a href="#qa-7138500cadc224d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tasco" data-paper-title="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning LLM 后训练 Chongqing University 2026-09-10 冻结主模型，优化轻量 prefix；除置信度外还惩罚邻域扰动下的不稳定，从而避免自信但错误的轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  测试时适配 稳定性优化 LLM 后训练 策略优化：谁在采样，谁在被更新 TASCO本地扰动惩罚是否包含真实LLM prefix训练？ 没有。本地只执行随机邻域扰动与稳定性惩罚参考核，未加载冻结语言模型的prefix路径。不能把小向量目标通过解释成真实测试时推理收益。 例如在数值特征上测稳定，不等于已在真实题目上优化语言模型前缀。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9e74343bb7ff5725">TASCO本地扰动惩罚是否包含真实LLM prefix训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atasco">Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chongqing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地只执行随机邻域扰动与稳定性惩罚参考核，未加载冻结语言模型的prefix路径。不能把小向量目标通过解释成真实测试时推理收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如在数值特征上测稳定，不等于已在真实题目上优化语言模型前缀。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11393">原论文</a> · <a href="../../../../post-training/2609.11393-tasco/">实现解读</a> · <a href="#qa-9e74343bb7ff5725">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:probe-erpo" data-paper-title="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation LLM 后训练 Nanyang Technological University 2026-09-08 论文用不依赖最终答案的 probe consistency ratio（PCR）估计当前题目的可信度：高一致样本可强化，低一致样本对排名靠后的候选施加负向约束，同时用熵项控制探索。 复现级别：PCR 已知条件下的策略更新诊断。复现级别：PCR 已知条件下的策略更新诊断。本地不执行论文的代码探针，只验证 PCR 分组后的负排名掩码与熵方向。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。诊断 fixture 提供 PCR 轴，本地实现低共识候选的负排名 mask 和 entropy direction；没有运行代码执行探针，所以不可把该结果称为完整 TTRL/ERPO。  代码测试时 RL LLM 后训练 策略优化：谁在采样，谁在被更新 Probe-ERPO为什么用不依赖最终答案的探针？ 测试时没有标准答案，若探针先读取最终正确解，就失去无标签适配意义。PCR用探针一致性提供可信度线索，再决定强化还是施加负向约束。 例如从中间状态检查一致性，而不是拿金标逐条比对后决定该学谁。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-probe-erpo-6a0c336f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e457206d88014d8c">Probe-ERPO为什么用不依赖最终答案的探针？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprobe-erpo">Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>测试时没有标准答案，若探针先读取最终正确解，就失去无标签适配意义。PCR用探针一致性提供可信度线索，再决定强化还是施加负向约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从中间状态检查一致性，而不是拿金标逐条比对后决定该学谁。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09135">原论文</a> · <a href="../../../../post-training/2609.09135-probe-erpo/">实现解读</a> · <a href="#qa-e457206d88014d8c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:probe-erpo" data-paper-title="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation LLM 后训练 Nanyang Technological University 2026-09-08 论文用不依赖最终答案的 probe consistency ratio（PCR）估计当前题目的可信度：高一致样本可强化，低一致样本对排名靠后的候选施加负向约束，同时用熵项控制探索。 复现级别：PCR 已知条件下的策略更新诊断。复现级别：PCR 已知条件下的策略更新诊断。本地不执行论文的代码探针，只验证 PCR 分组后的负排名掩码与熵方向。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。诊断 fixture 提供 PCR 轴，本地实现低共识候选的负排名 mask 和 entropy direction；没有运行代码执行探针，所以不可把该结果称为完整 TTRL/ERPO。  代码测试时 RL LLM 后训练 策略优化：谁在采样，谁在被更新 Probe-ERPO为什么用不依赖最终答案的探针一致性，低一致时又不直接强化多数答案？ 直接用模型自己的输出当标签可能循环确认错误。输出自由探针提供另一种一致性估计，高一致与低一致分支采用不同更新；低一致时限制排名靠后的候选，并配合熵控制探索。一致性仍不是答案真值，所以不能把探针分数当作有监督正确率。 教学例子：多个相关探针互相矛盾，主答案即使票数最多也不宜盲目强化；可先抑制明显落后的候选，保留进一步探索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-974ed0304580b614">Probe-ERPO为什么用不依赖最终答案的探针一致性，低一致时又不直接强化多数答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprobe-erpo">Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接用模型自己的输出当标签可能循环确认错误。输出自由探针提供另一种一致性估计，高一致与低一致分支采用不同更新；低一致时限制排名靠后的候选，并配合熵控制探索。一致性仍不是答案真值，所以不能把探针分数当作有监督正确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多个相关探针互相矛盾，主答案即使票数最多也不宜盲目强化；可先抑制明显落后的候选，保留进一步探索。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09135">原论文</a> · <a href="../../../../post-training/2609.09135-probe-erpo/">实现解读</a> · <a href="#qa-974ed0304580b614">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:probe-erpo" data-paper-title="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation LLM 后训练 Nanyang Technological University 2026-09-08 论文用不依赖最终答案的 probe consistency ratio（PCR）估计当前题目的可信度：高一致样本可强化，低一致样本对排名靠后的候选施加负向约束，同时用熵项控制探索。 复现级别：PCR 已知条件下的策略更新诊断。复现级别：PCR 已知条件下的策略更新诊断。本地不执行论文的代码探针，只验证 PCR 分组后的负排名掩码与熵方向。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。诊断 fixture 提供 PCR 轴，本地实现低共识候选的负排名 mask 和 entropy direction；没有运行代码执行探针，所以不可把该结果称为完整 TTRL/ERPO。  代码测试时 RL LLM 后训练 策略优化：谁在采样，谁在被更新 高PCR强化与低PCR负向排名为何不是简单同一伪标签训练？ 低一致组缺少可靠正例，方法转而约束较差候选，不把某个多数项无条件当真。高一致也只是可用线索，仍需熵控制与独立评估防止错误共识。 例如候选彼此矛盾时，可以先远离明显弱项，不必强行选一条作为正确示范。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7354527fcaae28bd">高PCR强化与低PCR负向排名为何不是简单同一伪标签训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprobe-erpo">Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>低一致组缺少可靠正例，方法转而约束较差候选，不把某个多数项无条件当真。高一致也只是可用线索，仍需熵控制与独立评估防止错误共识。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选彼此矛盾时，可以先远离明显弱项，不必强行选一条作为正确示范。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09135">原论文</a> · <a href="../../../../post-training/2609.09135-probe-erpo/">实现解读</a> · <a href="#qa-7354527fcaae28bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:probe-erpo" data-paper-title="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation LLM 后训练 Nanyang Technological University 2026-09-08 论文用不依赖最终答案的 probe consistency ratio（PCR）估计当前题目的可信度：高一致样本可强化，低一致样本对排名靠后的候选施加负向约束，同时用熵项控制探索。 复现级别：PCR 已知条件下的策略更新诊断。复现级别：PCR 已知条件下的策略更新诊断。本地不执行论文的代码探针，只验证 PCR 分组后的负排名掩码与熵方向。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。诊断 fixture 提供 PCR 轴，本地实现低共识候选的负排名 mask 和 entropy direction；没有运行代码执行探针，所以不可把该结果称为完整 TTRL/ERPO。  代码测试时 RL LLM 后训练 策略优化：谁在采样，谁在被更新 Probe-ERPO的负排名mask能否访问标准答案？ 不能。mask应由允许的探针与候选排名形成，答案只能在独立评分时出现。本地机制组件不能因预设mask工作正常，就宣称真实探针已具备可靠识别能力。 例如测试固定哪些位置被压低，只验证更新路径，不代表自动知道了哪些推理错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0c98f34ea7d7c7dc">Probe-ERPO的负排名mask能否访问标准答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprobe-erpo">Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。mask应由允许的探针与候选排名形成，答案只能在独立评分时出现。本地机制组件不能因预设mask工作正常，就宣称真实探针已具备可靠识别能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试固定哪些位置被压低，只验证更新路径，不代表自动知道了哪些推理错。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09135">原论文</a> · <a href="../../../../post-training/2609.09135-probe-erpo/">实现解读</a> · <a href="#qa-0c98f34ea7d7c7dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlvr-fusion" data-paper-title="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms LLM 后训练 Fudan University 2026-08-27 论文统一比较三种复用产物不同的跨域能力融合：Merge 合并专家 task vector，Mix RL 合并训练数据，MOPD 同时复用专家和数据。平均差距不超过 1.4 points，但单项可达 8.6 points，因此选择取决于专家、数据和成本条件。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。公平实现论文三种范式的可审计诊断；本地已有领域专家时执行论文建议的 task-vector Merge，不把三者混成论文没有提出的新目标。本地候选策略不是大模型 checkpoint；只执行“已有 experts”条件下的 Merge，Mix RL/MOPD 作为等预算可审计诊断，不声称复刻论文多模型规模结果。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.2812；同时记录 task-vector cosine、Mix RL advantage 和 MOPD teacher-gap 诊断。  跨领域 RLVR 能力融合 LLM 后训练 策略优化：谁在采样，谁在被更新 RLVR Fusion中的Merge、Mix RL、MOPD各复用什么？ Merge复用专家权重差，Mix RL复用训练数据，MOPD同时使用专家与数据提供蒸馏。这些资源前提不同，选择不能只依据一个平均效果数字。 例如只有已训练专家没有原训练集时，能做的融合路径与数据齐全时不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rlvr-fusion-9745b358" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1279a9ea40e51b64">RLVR Fusion中的Merge、Mix RL、MOPD各复用什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlvr-fusion">Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Merge复用专家权重差，Mix RL复用训练数据，MOPD同时使用专家与数据提供蒸馏。这些资源前提不同，选择不能只依据一个平均效果数字。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只有已训练专家没有原训练集时，能做的融合路径与数据齐全时不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27409">原论文</a> · <a href="../../../../post-training/2608.27409-rlvr-fusion/">实现解读</a> · <a href="#qa-1279a9ea40e51b64">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlvr-fusion" data-paper-title="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms LLM 后训练 Fudan University 2026-08-27 论文统一比较三种复用产物不同的跨域能力融合：Merge 合并专家 task vector，Mix RL 合并训练数据，MOPD 同时复用专家和数据。平均差距不超过 1.4 points，但单项可达 8.6 points，因此选择取决于专家、数据和成本条件。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。公平实现论文三种范式的可审计诊断；本地已有领域专家时执行论文建议的 task-vector Merge，不把三者混成论文没有提出的新目标。本地候选策略不是大模型 checkpoint；只执行“已有 experts”条件下的 Merge，Mix RL/MOPD 作为等预算可审计诊断，不声称复刻论文多模型规模结果。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.2812；同时记录 task-vector cosine、Mix RL advantage 和 MOPD teacher-gap 诊断。  跨领域 RLVR 能力融合 LLM 后训练 策略优化：谁在采样，谁在被更新 RLVR Fusion里的Merge、Mix RL和MOPD为什么不能当作同一种融合操作？ 三者复用的产物不同：Merge组合已有专家的参数增量，Mix RL混合领域数据再训练，MOPD同时利用专家指导与数据。可用专家、数据和预算因此决定可选路线。平均接近不代表各领域相同，也不能用概率向量合并的小实验证明真实checkpoint融合无损。 教学例子：只有两个领域专家权重、没有训练数据时，可讨论参数合并；若只有数据而无专家，则不能假装可以运行同样的蒸馏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7a1eadf46dc7ae5e">RLVR Fusion里的Merge、Mix RL和MOPD为什么不能当作同一种融合操作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlvr-fusion">Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>三者复用的产物不同：Merge组合已有专家的参数增量，Mix RL混合领域数据再训练，MOPD同时利用专家指导与数据。可用专家、数据和预算因此决定可选路线。平均接近不代表各领域相同，也不能用概率向量合并的小实验证明真实checkpoint融合无损。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只有两个领域专家权重、没有训练数据时，可讨论参数合并；若只有数据而无专家，则不能假装可以运行同样的蒸馏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27409">原论文</a> · <a href="../../../../post-training/2608.27409-rlvr-fusion/">实现解读</a> · <a href="#qa-7a1eadf46dc7ae5e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlvr-fusion" data-paper-title="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms LLM 后训练 Fudan University 2026-08-27 论文统一比较三种复用产物不同的跨域能力融合：Merge 合并专家 task vector，Mix RL 合并训练数据，MOPD 同时复用专家和数据。平均差距不超过 1.4 points，但单项可达 8.6 points，因此选择取决于专家、数据和成本条件。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。公平实现论文三种范式的可审计诊断；本地已有领域专家时执行论文建议的 task-vector Merge，不把三者混成论文没有提出的新目标。本地候选策略不是大模型 checkpoint；只执行“已有 experts”条件下的 Merge，Mix RL/MOPD 作为等预算可审计诊断，不声称复刻论文多模型规模结果。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.2812；同时记录 task-vector cosine、Mix RL advantage 和 MOPD teacher-gap 诊断。  跨领域 RLVR 能力融合 LLM 后训练 策略优化：谁在采样，谁在被更新 平均接近为何不能证明三种融合在每个领域等价？ 平均会抵消单领域差异，论文也记录单项差距更大。比较需看目标领域、专家和数据可得性及成本；机制近似或总体相近不代表逐任务可互换。 例如数学略好、代码略差的两个模型，平均相同也不满足相同部署需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ceb497193b26b2dc">平均接近为何不能证明三种融合在每个领域等价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlvr-fusion">Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平均会抵消单领域差异，论文也记录单项差距更大。比较需看目标领域、专家和数据可得性及成本；机制近似或总体相近不代表逐任务可互换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数学略好、代码略差的两个模型，平均相同也不满足相同部署需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27409">原论文</a> · <a href="../../../../post-training/2608.27409-rlvr-fusion/">实现解读</a> · <a href="#qa-ceb497193b26b2dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlvr-fusion" data-paper-title="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms LLM 后训练 Fudan University 2026-08-27 论文统一比较三种复用产物不同的跨域能力融合：Merge 合并专家 task vector，Mix RL 合并训练数据，MOPD 同时复用专家和数据。平均差距不超过 1.4 points，但单项可达 8.6 points，因此选择取决于专家、数据和成本条件。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。公平实现论文三种范式的可审计诊断；本地已有领域专家时执行论文建议的 task-vector Merge，不把三者混成论文没有提出的新目标。本地候选策略不是大模型 checkpoint；只执行“已有 experts”条件下的 Merge，Mix RL/MOPD 作为等预算可审计诊断，不声称复刻论文多模型规模结果。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.2812；同时记录 task-vector cosine、Mix RL advantage 和 MOPD teacher-gap 诊断。  跨领域 RLVR 能力融合 LLM 后训练 策略优化：谁在采样，谁在被更新 Merge的task vector为什么必须相对同一基座定义？ 专家参数减基座构成任务向量，再按规定合并。若基座或参数坐标不同，差向量不再表达同一参照变化；本地候选Merge也不能冒充大检查点完整融合实验。 例如两专家来自不同词表或权重布局，不能直接逐元素平均差值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3f2cc44b2ba85f0a">Merge的task vector为什么必须相对同一基座定义？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlvr-fusion">Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>专家参数减基座构成任务向量，再按规定合并。若基座或参数坐标不同，差向量不再表达同一参照变化；本地候选Merge也不能冒充大检查点完整融合实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两专家来自不同词表或权重布局，不能直接逐元素平均差值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27409">原论文</a> · <a href="../../../../post-training/2608.27409-rlvr-fusion/">实现解读</a> · <a href="#qa-3f2cc44b2ba85f0a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttpo" data-paper-title="TTPO: Test-Time Policy Optimization" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTPO: Test-Time Policy Optimization LLM 后训练 Zhejiang University 2026-08-27 多数票伪标签可能错误，但与多数票分歧的 rollout 通常仍是错的。TTPO 因而对同意分支做 OPSD，对分歧分支做 grouped RL，并分别过滤已收敛 token 与高置信错误。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现多数票路由、同意样本 OPSD、分歧样本 grouped RL 与置信错误筛选。未加载 Qwen checkpoint、未执行真实 test-time rollout；只验证非对称目标和 token 选择路径。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6328。这是候选策略上的机制隔离，不等同论文数学 benchmark。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTPO为什么把同意与反对多数票的轨迹分开训练？ 多数票可能错，但分歧轨迹通常仍提供不同性质的信号。同意分支用自蒸馏，分歧分支用组强化学习，避免给所有轨迹同一无标签伪监督。 例如支持主流结论与另走一条路的回答，不直接按相同模仿目标处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ttpo-67dfbe79" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9b00787b0189ac51">TTPO为什么把同意与反对多数票的轨迹分开训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attpo">TTPO: Test-Time Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多数票可能错，但分歧轨迹通常仍提供不同性质的信号。同意分支用自蒸馏，分歧分支用组强化学习，避免给所有轨迹同一无标签伪监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如支持主流结论与另走一条路的回答，不直接按相同模仿目标处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27448">原论文</a> · <a href="../../../../post-training/2608.27448-ttpo/">实现解读</a> · <a href="#qa-9b00787b0189ac51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttpo" data-paper-title="TTPO: Test-Time Policy Optimization" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTPO: Test-Time Policy Optimization LLM 后训练 Zhejiang University 2026-08-27 多数票伪标签可能错误，但与多数票分歧的 rollout 通常仍是错的。TTPO 因而对同意分支做 OPSD，对分歧分支做 grouped RL，并分别过滤已收敛 token 与高置信错误。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现多数票路由、同意样本 OPSD、分歧样本 grouped RL 与置信错误筛选。未加载 Qwen checkpoint、未执行真实 test-time rollout；只验证非对称目标和 token 选择路径。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6328。这是候选策略上的机制隔离，不等同论文数学 benchmark。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTPO为什么对同意多数票与反对多数票的回答采用不同目标？ 多数票可能正确也可能错，完全照抄会把误差扩散。TTPO对同意分支使用自蒸馏，对分歧分支采用组式RL，并通过token选择过滤已收敛位置和高置信错误。两条路径利用不同信号，并不把多数票升级为真值，也不允许读取测试金标。 教学例子：几条回答都选同一答案，其中一条反对；不能简单把反对者整段删掉，而要按各分支的目标与可靠性过滤处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-69b2a4247c96ba4a">TTPO为什么对同意多数票与反对多数票的回答采用不同目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attpo">TTPO: Test-Time Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多数票可能正确也可能错，完全照抄会把误差扩散。TTPO对同意分支使用自蒸馏，对分歧分支采用组式RL，并通过token选择过滤已收敛位置和高置信错误。两条路径利用不同信号，并不把多数票升级为真值，也不允许读取测试金标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>几条回答都选同一答案，其中一条反对；不能简单把反对者整段删掉，而要按各分支的目标与可靠性过滤处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27448">原论文</a> · <a href="../../../../post-training/2608.27448-ttpo/">实现解读</a> · <a href="#qa-69b2a4247c96ba4a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttpo" data-paper-title="TTPO: Test-Time Policy Optimization" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTPO: Test-Time Policy Optimization LLM 后训练 Zhejiang University 2026-08-27 多数票伪标签可能错误，但与多数票分歧的 rollout 通常仍是错的。TTPO 因而对同意分支做 OPSD，对分歧分支做 grouped RL，并分别过滤已收敛 token 与高置信错误。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现多数票路由、同意样本 OPSD、分歧样本 grouped RL 与置信错误筛选。未加载 Qwen checkpoint、未执行真实 test-time rollout；只验证非对称目标和 token 选择路径。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6328。这是候选策略上的机制隔离，不等同论文数学 benchmark。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTPO与直接把多数答案当金标相比多了哪些限制？ 它采用非对称目标，并过滤已收敛词元及高置信错误，承认多数票并非真值。过滤可靠性仍影响结果，不能用无标签共识宣称得到了独立验证解。 例如一组一致猜错时，多数项也可能不值得继续强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-eaac62071a684a01">TTPO与直接把多数答案当金标相比多了哪些限制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attpo">TTPO: Test-Time Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它采用非对称目标，并过滤已收敛词元及高置信错误，承认多数票并非真值。过滤可靠性仍影响结果，不能用无标签共识宣称得到了独立验证解。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一组一致猜错时，多数项也可能不值得继续强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27448">原论文</a> · <a href="../../../../post-training/2608.27448-ttpo/">实现解读</a> · <a href="#qa-eaac62071a684a01">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttpo" data-paper-title="TTPO: Test-Time Policy Optimization" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTPO: Test-Time Policy Optimization LLM 后训练 Zhejiang University 2026-08-27 多数票伪标签可能错误，但与多数票分歧的 rollout 通常仍是错的。TTPO 因而对同意分支做 OPSD，对分歧分支做 grouped RL，并分别过滤已收敛 token 与高置信错误。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现多数票路由、同意样本 OPSD、分歧样本 grouped RL 与置信错误筛选。未加载 Qwen checkpoint、未执行真实 test-time rollout；只验证非对称目标和 token 选择路径。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6328。这是候选策略上的机制隔离，不等同论文数学 benchmark。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTPO本地是否执行真实测试时采样与Qwen更新？ 未执行。当前只验证分支目标与词元选择路径，不能将手工候选上的更新视为真实无标签题目适配。实现需在分支判定前保持答案不可见。 例如预给候选答案用于公式测试，不等于模型在评测题上真实生成这些轨迹。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-04141004d61046ff">TTPO本地是否执行真实测试时采样与Qwen更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attpo">TTPO: Test-Time Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未执行。当前只验证分支目标与词元选择路径，不能将手工候选上的更新视为真实无标签题目适配。实现需在分支判定前保持答案不可见。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预给候选答案用于公式测试，不等于模型在评测题上真实生成这些轨迹。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27448">原论文</a> · <a href="../../../../post-training/2608.27448-ttpo/">实现解读</a> · <a href="#qa-04141004d61046ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grin" data-paper-title="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection LLM 后训练 University of California, Merced 2026-08-26 纯 on-policy RL 在新知识尚未掌握时几乎采不到正确答案。GRIN 在失败组注入 golden response，再以 mixed-policy importance correction 训练；能力提高后自动回到 on-policy 探索。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.3438（+175.00%）；golden answer 是本地候选 oracle。  混合策略知识注入 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRIN为什么只在失败组注入golden response？ 全失败组缺少相对正信号，正确轨迹可提供可学方向；学生已有成功样本时则更多保留原生探索。注入是训练期帮助，不是让评测模型读取答案。 例如学生所有尝试都失败时才补一条验证解，而非每题始终给出标准答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-grin-1eaeb543" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-873baedb77750dde">GRIN为什么只在失败组注入golden response？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrin">From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Merced</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全失败组缺少相对正信号，正确轨迹可提供可学方向；学生已有成功样本时则更多保留原生探索。注入是训练期帮助，不是让评测模型读取答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生所有尝试都失败时才补一条验证解，而非每题始终给出标准答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25243">原论文</a> · <a href="../../../../post-training/2608.25243-grin/">实现解读</a> · <a href="#qa-873baedb77750dde">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grin" data-paper-title="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection LLM 后训练 University of California, Merced 2026-08-26 纯 on-policy RL 在新知识尚未掌握时几乎采不到正确答案。GRIN 在失败组注入 golden response，再以 mixed-policy importance correction 训练；能力提高后自动回到 on-policy 探索。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.3438（+175.00%）；golden answer 是本地候选 oracle。  混合策略知识注入 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRIN给失败组注入golden response时，为什么必须按混合采样分布校正？ 注入的专家回答并非由无提示当前策略采到，组内数据来自策略与外部来源的混合。以混合分布作分母的校正用于处理这种变化，能力提高后再减少注入、回到探索。gold只属于训练监督，不能让被评估Agent在部署输入中直接读取。 教学例子：学生整组都答错，训练时加入一份已验证解法；可以利用它学习，但不能把这份外部解法记成学生自己探索成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3f5bf75743d70577">GRIN给失败组注入golden response时，为什么必须按混合采样分布校正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrin">From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Merced</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>注入的专家回答并非由无提示当前策略采到，组内数据来自策略与外部来源的混合。以混合分布作分母的校正用于处理这种变化，能力提高后再减少注入、回到探索。gold只属于训练监督，不能让被评估Agent在部署输入中直接读取。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生整组都答错，训练时加入一份已验证解法；可以利用它学习，但不能把这份外部解法记成学生自己探索成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25243">原论文</a> · <a href="../../../../post-training/2608.25243-grin/">实现解读</a> · <a href="#qa-3f5bf75743d70577">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grin" data-paper-title="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection LLM 后训练 University of California, Merced 2026-08-26 纯 on-policy RL 在新知识尚未掌握时几乎采不到正确答案。GRIN 在失败组注入 golden response，再以 mixed-policy importance correction 训练；能力提高后自动回到 on-policy 探索。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.3438（+175.00%）；golden answer 是本地候选 oracle。  混合策略知识注入 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRIN混合策略校正与把专家答案当作学生采样有什么差别？ 混合数据的采样分布包含注入来源，校正分母应反映这个分布。把专家样本标成纯on-policy会给错误权重，并掩盖外部知识来源。 例如人工加入的解法没有由学生随机采到，不能拿学生生成概率当它唯一来源。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e5936dbb1a152686">GRIN混合策略校正与把专家答案当作学生采样有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrin">From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Merced</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>混合数据的采样分布包含注入来源，校正分母应反映这个分布。把专家样本标成纯on-policy会给错误权重，并掩盖外部知识来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人工加入的解法没有由学生随机采到，不能拿学生生成概率当它唯一来源。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25243">原论文</a> · <a href="../../../../post-training/2608.25243-grin/">实现解读</a> · <a href="#qa-e5936dbb1a152686">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grin" data-paper-title="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection LLM 后训练 University of California, Merced 2026-08-26 纯 on-policy RL 在新知识尚未掌握时几乎采不到正确答案。GRIN 在失败组注入 golden response，再以 mixed-policy importance correction 训练；能力提高后自动回到 on-policy 探索。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.3438（+175.00%）；golden answer 是本地候选 oracle。  混合策略知识注入 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRIN的重要性比为什么用q_mix而非冻结reference？ q_mix描述样本实际怎样产生，reference通常描述正则锚点，两者职责不同。实现需追踪混合来源及概率；本地确定性候选诊断未复刻论文知识吸收数据。 例如参考模型很旧但样本来自另一专家，二者概率不能随意替换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e8650e7c6e350f94">GRIN的重要性比为什么用q_mix而非冻结reference？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrin">From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Merced</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>q_mix描述样本实际怎样产生，reference通常描述正则锚点，两者职责不同。实现需追踪混合来源及概率；本地确定性候选诊断未复刻论文知识吸收数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如参考模型很旧但样本来自另一专家，二者概率不能随意替换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25243">原论文</a> · <a href="../../../../post-training/2608.25243-grin/">实现解读</a> · <a href="#qa-e8650e7c6e350f94">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erpo" data-paper-title="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization LLM 后训练 AMAP, Alibaba Group 2026-08-24 传统 Policy-KL 直接压回答分布，稳定训练的同时消耗探索预算。ERPO 观察到 RL 过程中模型诱导的问题分布也会漂移，于是把正则放到输入侧：用冻结 reference 的问题似然给 query 静态加权，再以 Query-KL 控制环境分布漂移，不直接对 response score function 施压。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 reference typicality weight 与 Query-KL，且响应侧 Policy-KL 系数固定为零。本地将 candidate typicality 作为 query-likelihood 代理，验证梯度边界和稳定性控制流；没有训练真实 LLM 或复跑六个论文 benchmark。同一初始 candidate policy、arithmetic-smoke、100 steps、seed 42。基线 accuracy 0.1953，ERPO 0.6094（+212.0%）；  输入侧 Query-KL LLM 后训练 策略优化：谁在采样，谁在被更新 ERPO为何把策略漂移问题放到输入侧观察？ 回答正则会直接限制响应探索；ERPO关注模型诱导的问题分布漂移，用问题似然加权及Query-KL控制输入环境的偏移，改变正则作用位置。 例如保持学习问题的分布不至于失衡，而非要求每个回答都贴近旧措辞。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-erpo-0cf15e52" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dcb7785d8df7472f">ERPO为何把策略漂移问题放到输入侧观察？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerpo">Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AMAP, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>回答正则会直接限制响应探索；ERPO关注模型诱导的问题分布漂移，用问题似然加权及Query-KL控制输入环境的偏移，改变正则作用位置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保持学习问题的分布不至于失衡，而非要求每个回答都贴近旧措辞。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23311">原论文</a> · <a href="../../../../post-training/2608.23311-erpo/">实现解读</a> · <a href="#qa-dcb7785d8df7472f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erpo" data-paper-title="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization LLM 后训练 AMAP, Alibaba Group 2026-08-24 传统 Policy-KL 直接压回答分布，稳定训练的同时消耗探索预算。ERPO 观察到 RL 过程中模型诱导的问题分布也会漂移，于是把正则放到输入侧：用冻结 reference 的问题似然给 query 静态加权，再以 Query-KL 控制环境分布漂移，不直接对 response score function 施压。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 reference typicality weight 与 Query-KL，且响应侧 Policy-KL 系数固定为零。本地将 candidate typicality 作为 query-likelihood 代理，验证梯度边界和稳定性控制流；没有训练真实 LLM 或复跑六个论文 benchmark。同一初始 candidate policy、arithmetic-smoke、100 steps、seed 42。基线 accuracy 0.1953，ERPO 0.6094（+212.0%）；  输入侧 Query-KL LLM 后训练 策略优化：谁在采样，谁在被更新 ERPO把正则移到问题分布一侧，和直接限制回答分布有什么区别？ 回答侧KL会直接压制输出变化，稳定训练的同时也限制探索。ERPO用reference的问题似然对query加权，并约束模型诱导的问题分布漂移，改变的是哪些输入获得多少更新压力。它不是把回答KL换个变量名；本地typicality代理也没有验证真实query分布建模。 教学例子：训练持续偏向某类熟题时，可调整问题侧权重；这与要求每个回答都紧贴原模型，是两种不同的约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-474029342d1961bb">ERPO把正则移到问题分布一侧，和直接限制回答分布有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerpo">Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AMAP, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>回答侧KL会直接压制输出变化，稳定训练的同时也限制探索。ERPO用reference的问题似然对query加权，并约束模型诱导的问题分布漂移，改变的是哪些输入获得多少更新压力。它不是把回答KL换个变量名；本地typicality代理也没有验证真实query分布建模。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练持续偏向某类熟题时，可调整问题侧权重；这与要求每个回答都紧贴原模型，是两种不同的约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23311">原论文</a> · <a href="../../../../post-training/2608.23311-erpo/">实现解读</a> · <a href="#qa-474029342d1961bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erpo" data-paper-title="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization LLM 后训练 AMAP, Alibaba Group 2026-08-24 传统 Policy-KL 直接压回答分布，稳定训练的同时消耗探索预算。ERPO 观察到 RL 过程中模型诱导的问题分布也会漂移，于是把正则放到输入侧：用冻结 reference 的问题似然给 query 静态加权，再以 Query-KL 控制环境分布漂移，不直接对 response score function 施压。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 reference typicality weight 与 Query-KL，且响应侧 Policy-KL 系数固定为零。本地将 candidate typicality 作为 query-likelihood 代理，验证梯度边界和稳定性控制流；没有训练真实 LLM 或复跑六个论文 benchmark。同一初始 candidate policy、arithmetic-smoke、100 steps、seed 42。基线 accuracy 0.1953，ERPO 0.6094（+212.0%）；  输入侧 Query-KL LLM 后训练 策略优化：谁在采样，谁在被更新 Query-KL与Policy-KL能否在实现里直接互换？ 不能。一个约束问题分布，一个约束给定问题下回答分布，梯度边界不同。两者都写KL不代表同一正则，也不能在回答score function上施压后仍称仅输入侧控制。 例如常抽哪些题与一道题怎样作答，是两个不同条件分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f6c1dd6350ae3b8d">Query-KL与Policy-KL能否在实现里直接互换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerpo">Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AMAP, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。一个约束问题分布，一个约束给定问题下回答分布，梯度边界不同。两者都写KL不代表同一正则，也不能在回答score function上施压后仍称仅输入侧控制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如常抽哪些题与一道题怎样作答，是两个不同条件分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23311">原论文</a> · <a href="../../../../post-training/2608.23311-erpo/">实现解读</a> · <a href="#qa-f6c1dd6350ae3b8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erpo" data-paper-title="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization LLM 后训练 AMAP, Alibaba Group 2026-08-24 传统 Policy-KL 直接压回答分布，稳定训练的同时消耗探索预算。ERPO 观察到 RL 过程中模型诱导的问题分布也会漂移，于是把正则放到输入侧：用冻结 reference 的问题似然给 query 静态加权，再以 Query-KL 控制环境分布漂移，不直接对 response score function 施压。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 reference typicality weight 与 Query-KL，且响应侧 Policy-KL 系数固定为零。本地将 candidate typicality 作为 query-likelihood 代理，验证梯度边界和稳定性控制流；没有训练真实 LLM 或复跑六个论文 benchmark。同一初始 candidate policy、arithmetic-smoke、100 steps、seed 42。基线 accuracy 0.1953，ERPO 0.6094（+212.0%）；  输入侧 Query-KL LLM 后训练 策略优化：谁在采样，谁在被更新 ERPO本地candidate typicality为何只能叫query-likelihood代理？ 它在有限候选上模拟输入典型性，用来验证控制流与梯度边界，并非真实语言模型对自然问题的似然。静态权重来自冻结参考，不能用测试正确率倒推权重。 例如候选特征常见程度不等于完整中文问题在真实模型下的生成概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-25993f182c79b72b">ERPO本地candidate typicality为何只能叫query-likelihood代理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerpo">Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AMAP, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它在有限候选上模拟输入典型性，用来验证控制流与梯度边界，并非真实语言模型对自然问题的似然。静态权重来自冻结参考，不能用测试正确率倒推权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选特征常见程度不等于完整中文问题在真实模型下的生成概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23311">原论文</a> · <a href="../../../../post-training/2608.23311-erpo/">实现解读</a> · <a href="#qa-25993f182c79b72b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gcpo" data-paper-title="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs LLM 后训练 Shanghai AI Laboratory 2026-08-12 GRPO 等 on-policy rollout RL 会偶发进入预训练权重的主奇异子空间，论文观察到这些 spike 常先于验证性能下降。GCPO 固定预训练矩阵两侧的 top-k 奇异空间，只允许低秩更新存在于输入、输出两侧的正交补中；这是硬可行域，不是依赖系数的软 penalty。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际计算 rollout update 的主子空间重合，并把 policy update 投影到互补子空间；线性策略不是论文矩阵层的完整双侧 LoRA。本地 policy 参数是向量，因此以 empirical update covariance 的主右奇异空间实现等价正交限制；未声称复刻 Qwen3-8B/GLM4-9B 的逐层矩阵双侧 LoRA、三 seed 或论文 benchmark。本地对照口径：基线为同一随机初始化 candidate policy 训练前；  几何约束 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GCPO为什么保护预训练权重的主奇异空间？ 论文观察到rollout更新进入这些主空间的尖峰可能先于验证退化，于是把更新限制在两侧正交补，避免覆盖已有主要映射。观察关联并不表示所有主方向都不能学习。 例如保持已有重要输入输出映射，优先在剩余子空间添加任务变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gcpo-c679efe1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d7473bf332d552ad">GCPO为什么保护预训练权重的主奇异空间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agcpo">GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>论文观察到rollout更新进入这些主空间的尖峰可能先于验证退化，于是把更新限制在两侧正交补，避免覆盖已有主要映射。观察关联并不表示所有主方向都不能学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保持已有重要输入输出映射，优先在剩余子空间添加任务变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11674">原论文</a> · <a href="../../../../post-training/2608.11674-gcpo/">实现解读</a> · <a href="#qa-d7473bf332d552ad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gcpo" data-paper-title="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs LLM 后训练 Shanghai AI Laboratory 2026-08-12 GRPO 等 on-policy rollout RL 会偶发进入预训练权重的主奇异子空间，论文观察到这些 spike 常先于验证性能下降。GCPO 固定预训练矩阵两侧的 top-k 奇异空间，只允许低秩更新存在于输入、输出两侧的正交补中；这是硬可行域，不是依赖系数的软 penalty。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际计算 rollout update 的主子空间重合，并把 policy update 投影到互补子空间；线性策略不是论文矩阵层的完整双侧 LoRA。本地 policy 参数是向量，因此以 empirical update covariance 的主右奇异空间实现等价正交限制；未声称复刻 Qwen3-8B/GLM4-9B 的逐层矩阵双侧 LoRA、三 seed 或论文 benchmark。本地对照口径：基线为同一随机初始化 candidate policy 训练前；  几何约束 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GCPO为什么把低秩更新投影到左右奇异空间的正交补，而不只惩罚投影大小？ 软惩罚允许优化用足够大收益换取主子空间漂移，双侧投影则把这类更新从可行域中直接排除。固定预训练主奇异空间后，输入和输出两侧都受约束，目标是减少覆盖已有主映射。向量级诊断并不等同真实逐层矩阵LoRA训练。 教学例子：若某个权重矩阵的主要输入输出方向需要保护，只在损失里罚它仍可被突破；双侧投影要求每次有效更新都避开这些方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b228873198b3173b">GCPO为什么把低秩更新投影到左右奇异空间的正交补，而不只惩罚投影大小？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agcpo">GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>软惩罚允许优化用足够大收益换取主子空间漂移，双侧投影则把这类更新从可行域中直接排除。固定预训练主奇异空间后，输入和输出两侧都受约束，目标是减少覆盖已有主映射。向量级诊断并不等同真实逐层矩阵LoRA训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若某个权重矩阵的主要输入输出方向需要保护，只在损失里罚它仍可被突破；双侧投影要求每次有效更新都避开这些方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11674">原论文</a> · <a href="../../../../post-training/2608.11674-gcpo/">实现解读</a> · <a href="#qa-b228873198b3173b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gcpo" data-paper-title="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs LLM 后训练 Shanghai AI Laboratory 2026-08-12 GRPO 等 on-policy rollout RL 会偶发进入预训练权重的主奇异子空间，论文观察到这些 spike 常先于验证性能下降。GCPO 固定预训练矩阵两侧的 top-k 奇异空间，只允许低秩更新存在于输入、输出两侧的正交补中；这是硬可行域，不是依赖系数的软 penalty。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际计算 rollout update 的主子空间重合，并把 policy update 投影到互补子空间；线性策略不是论文矩阵层的完整双侧 LoRA。本地 policy 参数是向量，因此以 empirical update covariance 的主右奇异空间实现等价正交限制；未声称复刻 Qwen3-8B/GLM4-9B 的逐层矩阵双侧 LoRA、三 seed 或论文 benchmark。本地对照口径：基线为同一随机初始化 candidate policy 训练前；  几何约束 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GCPO硬正交约束与加一个小投影惩罚有何区别？ 硬约束把不合条件的更新从可行域排除，软惩罚仍允许优化器用目标收益交换违规。二者约束强度与训练行为不同，不能只调惩罚系数就声称严格双侧正交。 例如软目标允许暂时进入主方向，硬投影则每次都移除相应分量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-14dc24b93afc8e6b">GCPO硬正交约束与加一个小投影惩罚有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agcpo">GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>硬约束把不合条件的更新从可行域排除，软惩罚仍允许优化器用目标收益交换违规。二者约束强度与训练行为不同，不能只调惩罚系数就声称严格双侧正交。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如软目标允许暂时进入主方向，硬投影则每次都移除相应分量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11674">原论文</a> · <a href="../../../../post-training/2608.11674-gcpo/">实现解读</a> · <a href="#qa-14dc24b93afc8e6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gcpo" data-paper-title="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs LLM 后训练 Shanghai AI Laboratory 2026-08-12 GRPO 等 on-policy rollout RL 会偶发进入预训练权重的主奇异子空间，论文观察到这些 spike 常先于验证性能下降。GCPO 固定预训练矩阵两侧的 top-k 奇异空间，只允许低秩更新存在于输入、输出两侧的正交补中；这是硬可行域，不是依赖系数的软 penalty。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际计算 rollout update 的主子空间重合，并把 policy update 投影到互补子空间；线性策略不是论文矩阵层的完整双侧 LoRA。本地 policy 参数是向量，因此以 empirical update covariance 的主右奇异空间实现等价正交限制；未声称复刻 Qwen3-8B/GLM4-9B 的逐层矩阵双侧 LoRA、三 seed 或论文 benchmark。本地对照口径：基线为同一随机初始化 candidate policy 训练前；  几何约束 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GCPO本地向量策略验证了原文逐层双侧LoRA吗？ 没有。向量参数用经验更新协方差的主右空间做正交限制，是参考机制代理；原文矩阵还需输入与输出两侧固定投影。不能把单侧向量核的结果当逐层双侧模型证据。 例如一维参数数组没有独立左右作用轴，无法直接测试完整矩阵两侧约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5dff608003ae7cdb">GCPO本地向量策略验证了原文逐层双侧LoRA吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agcpo">GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。向量参数用经验更新协方差的主右空间做正交限制，是参考机制代理；原文矩阵还需输入与输出两侧固定投影。不能把单侧向量核的结果当逐层双侧模型证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一维参数数组没有独立左右作用轴，无法直接测试完整矩阵两侧约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11674">原论文</a> · <a href="../../../../post-training/2608.11674-gcpo/">实现解读</a> · <a href="#qa-5dff608003ae7cdb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erils" data-paper-title="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models LLM 后训练 Seoul National University 2026-08-03 约束外部策略 rollout 长度，并对 on-policy/external 来源分别处理奖励以防联合归一化崩溃。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  外部 rollout Diffusion LM RL LLM 后训练 策略优化：谁在采样，谁在被更新 ERILS为什么在扩散RL中引入外部rollout？ 学生自身探索可能覆盖不足，外部策略提供不同轨迹。引入后必须处理来源与长度差异，不能把外部高分直接解释为学生原生可达能力。 例如外部模型提供另一种去噪轨迹，学生学习来源仍要在记录中明确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-erils-07f1d788" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d48d992843b46b3e">ERILS为什么在扩散RL中引入外部rollout？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerils">Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生自身探索可能覆盖不足，外部策略提供不同轨迹。引入后必须处理来源与长度差异，不能把外部高分直接解释为学生原生可达能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如外部模型提供另一种去噪轨迹，学生学习来源仍要在记录中明确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01717">原论文</a> · <a href="../../../../post-training/2608.01717-erils/">实现解读</a> · <a href="#qa-d48d992843b46b3e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erils" data-paper-title="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models LLM 后训练 Seoul National University 2026-08-03 约束外部策略 rollout 长度，并对 on-policy/external 来源分别处理奖励以防联合归一化崩溃。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  外部 rollout Diffusion LM RL LLM 后训练 策略优化：谁在采样，谁在被更新 ERILS为什么分别处理自身与外部rollout的奖励，而不把它们直接拼组归一化？ 不同来源的长度与奖励分布可能不同，联合归一化会把来源差异混成优势，使一类样本支配或失去信号。ERILS限制外部轨迹长度并分来源处理奖励，保留外部探索价值。来源分组不自动消除所有离策略误差，仍需按实际目标解释采样口径。 教学例子：外部策略总写更长、更高分的回答，直接与学生短回答混组，可能让所有学生样本都变负；应先识别来源差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-671320bb53b7dd5a">ERILS为什么分别处理自身与外部rollout的奖励，而不把它们直接拼组归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerils">Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同来源的长度与奖励分布可能不同，联合归一化会把来源差异混成优势，使一类样本支配或失去信号。ERILS限制外部轨迹长度并分来源处理奖励，保留外部探索价值。来源分组不自动消除所有离策略误差，仍需按实际目标解释采样口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>外部策略总写更长、更高分的回答，直接与学生短回答混组，可能让所有学生样本都变负；应先识别来源差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01717">原论文</a> · <a href="../../../../post-training/2608.01717-erils/">实现解读</a> · <a href="#qa-671320bb53b7dd5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erils" data-paper-title="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models LLM 后训练 Seoul National University 2026-08-03 约束外部策略 rollout 长度，并对 on-policy/external 来源分别处理奖励以防联合归一化崩溃。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  外部 rollout Diffusion LM RL LLM 后训练 策略优化：谁在采样，谁在被更新 来源分别归一与on/off混合一起归一有什么区别？ 两个来源的奖励尺度和分布可能不同，联合基线会让一种来源系统压制另一种。分别处理能保留各自组内信号，但不自动解决所有跨策略偏差。 例如专家奖励整体较高，联合均值可能把学生有价值改进也变成负优势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8597a1ba52af3551">来源分别归一与on/off混合一起归一有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerils">Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两个来源的奖励尺度和分布可能不同，联合基线会让一种来源系统压制另一种。分别处理能保留各自组内信号，但不自动解决所有跨策略偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如专家奖励整体较高，联合均值可能把学生有价值改进也变成负优势。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01717">原论文</a> · <a href="../../../../post-training/2608.01717-erils/">实现解读</a> · <a href="#qa-8597a1ba52af3551">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erils" data-paper-title="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models LLM 后训练 Seoul National University 2026-08-03 约束外部策略 rollout 长度，并对 on-policy/external 来源分别处理奖励以防联合归一化崩溃。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  外部 rollout Diffusion LM RL LLM 后训练 策略优化：谁在采样，谁在被更新 ERILS实现为什么还需显式检查外部响应长度？ 长轨迹会影响有效词元预算与损失尺度，方法要求长度约束。来源标签也要一直传到奖励归一化，不能拼接后丢失；本地candidate-policy未跑完整扩散检查点训练。 例如超长专家轨迹若直接混入，可能占满批次预算，改变原来的混合设定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6f3e41502de5e0cd">ERILS实现为什么还需显式检查外部响应长度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerils">Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长轨迹会影响有效词元预算与损失尺度，方法要求长度约束。来源标签也要一直传到奖励归一化，不能拼接后丢失；本地candidate-policy未跑完整扩散检查点训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如超长专家轨迹若直接混入，可能占满批次预算，改变原来的混合设定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01717">原论文</a> · <a href="../../../../post-training/2608.01717-erils/">实现解读</a> · <a href="#qa-6f3e41502de5e0cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reco-grpo" data-paper-title="ReCo" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReCo LLM 后训练 Seoul National University 2026-07-29 GRPO 容易重复采到高概率回答，并继续放大已经占优的 token，导致大下推理路径覆盖率下降。ReCo 同时修正 response 和 token：按 rollout 组中的期望出现次数抑制高频回答，再用 Bernoulli 方差比把更新集中到尚未饱和的决策点。 这是 objective-level 机制复现，不是 Qwen/Llama 全参数 RLVR；本地候选动作代理完整 response，无法等价报告 Pass@64 或自然语言 Self-BLEU。candidate-policy mini-suite 中同时执行期望出现次数权重、方差比、PPO clip、KL 和每 16 步 rollout-policy refresh。  分布保持 RL LLM 后训练 策略优化：谁在采样，谁在被更新 ReCo为何同时处理重复响应与饱和词元？ 高概率回答反复出现会占据更多训练权重，已确定词元也可能继续被强化。响应级期望次数修正与词元方差比针对两种不同冗余，意在保留更多可探索路径。 例如同一解法出现多次，里面的常见格式词又很确定，两层重复都可能主导梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-reco-grpo-97f782ad" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c34e2c8ac9baa559">ReCo为何同时处理重复响应与饱和词元？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areco-grpo">ReCo</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高概率回答反复出现会占据更多训练权重，已确定词元也可能继续被强化。响应级期望次数修正与词元方差比针对两种不同冗余，意在保留更多可探索路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一解法出现多次，里面的常见格式词又很确定，两层重复都可能主导梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26862">原论文</a> · <a href="../../../../post-training/2607.26862-reco/">实现解读</a> · <a href="#qa-c34e2c8ac9baa559">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reco-grpo" data-paper-title="ReCo" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReCo LLM 后训练 Seoul National University 2026-07-29 GRPO 容易重复采到高概率回答，并继续放大已经占优的 token，导致大下推理路径覆盖率下降。ReCo 同时修正 response 和 token：按 rollout 组中的期望出现次数抑制高频回答，再用 Bernoulli 方差比把更新集中到尚未饱和的决策点。 这是 objective-level 机制复现，不是 Qwen/Llama 全参数 RLVR；本地候选动作代理完整 response，无法等价报告 Pass@64 或自然语言 Self-BLEU。candidate-policy mini-suite 中同时执行期望出现次数权重、方差比、PPO clip、KL 和每 16 步 rollout-policy refresh。  分布保持 RL LLM 后训练 策略优化：谁在采样，谁在被更新 ReCo为什么既抑制高频回答，又按token的Bernoulli方差调整更新？ 响应级重复会让热门解法反复占据样本，token级饱和又会继续放大已占优决策。两项分别校正组内期望出现次数和局部决策的可塑性，不能相互替代。保持覆盖的目标也不等于追求任意随机性，本地候选概率不能代表真实长文本路径覆盖。 教学例子：多次采样都得到同一句模板，末尾选择也几乎确定；只减少重复回答权重，未必能避免饱和token继续主导更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-24eff40b49e92f55">ReCo为什么既抑制高频回答，又按token的Bernoulli方差调整更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areco-grpo">ReCo</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>响应级重复会让热门解法反复占据样本，token级饱和又会继续放大已占优决策。两项分别校正组内期望出现次数和局部决策的可塑性，不能相互替代。保持覆盖的目标也不等于追求任意随机性，本地候选概率不能代表真实长文本路径覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多次采样都得到同一句模板，末尾选择也几乎确定；只减少重复回答权重，未必能避免饱和token继续主导更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26862">原论文</a> · <a href="../../../../post-training/2607.26862-reco/">实现解读</a> · <a href="#qa-24eff40b49e92f55">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reco-grpo" data-paper-title="ReCo" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReCo LLM 后训练 Seoul National University 2026-07-29 GRPO 容易重复采到高概率回答，并继续放大已经占优的 token，导致大下推理路径覆盖率下降。ReCo 同时修正 response 和 token：按 rollout 组中的期望出现次数抑制高频回答，再用 Bernoulli 方差比把更新集中到尚未饱和的决策点。 这是 objective-level 机制复现，不是 Qwen/Llama 全参数 RLVR；本地候选动作代理完整 response，无法等价报告 Pass@64 或自然语言 Self-BLEU。candidate-policy mini-suite 中同时执行期望出现次数权重、方差比、PPO clip、KL 和每 16 步 rollout-policy refresh。  分布保持 RL LLM 后训练 策略优化：谁在采样，谁在被更新 响应去重与ReCo期望出现次数加权能等同吗？ 硬去重直接丢重复样本，期望次数权重依据策略概率连续调整贡献；词元方差比还另作局部修正。二者改变的目标不同，不能用简单去重冒充整个方法。 例如两回答碰巧未重复，但一种本来极常见，概率权重仍可能不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-44a200aee7cb27b3">响应去重与ReCo期望出现次数加权能等同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areco-grpo">ReCo</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>硬去重直接丢重复样本，期望次数权重依据策略概率连续调整贡献；词元方差比还另作局部修正。二者改变的目标不同，不能用简单去重冒充整个方法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两回答碰巧未重复，但一种本来极常见，概率权重仍可能不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26862">原论文</a> · <a href="../../../../post-training/2607.26862-reco/">实现解读</a> · <a href="#qa-44a200aee7cb27b3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reco-grpo" data-paper-title="ReCo" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReCo LLM 后训练 Seoul National University 2026-07-29 GRPO 容易重复采到高概率回答，并继续放大已经占优的 token，导致大下推理路径覆盖率下降。ReCo 同时修正 response 和 token：按 rollout 组中的期望出现次数抑制高频回答，再用 Bernoulli 方差比把更新集中到尚未饱和的决策点。 这是 objective-level 机制复现，不是 Qwen/Llama 全参数 RLVR；本地候选动作代理完整 response，无法等价报告 Pass@64 或自然语言 Self-BLEU。candidate-policy mini-suite 中同时执行期望出现次数权重、方差比、PPO clip、KL 和每 16 步 rollout-policy refresh。  分布保持 RL LLM 后训练 策略优化：谁在采样，谁在被更新 ReCo的Bernoulli方差比为什么要保留old与current区分？ 它比较当前概率乘一减概率与旧策略相应量，衡量决策饱和变化。分母边界需数值保护，不能把两边都用当前概率后得到一；本地候选动作不等价自然语言pass@64。 例如旧概率极接近边界时要审查稳定性，不能把数值异常当巨大有效信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b7324658a6699d93">ReCo的Bernoulli方差比为什么要保留old与current区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areco-grpo">ReCo</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它比较当前概率乘一减概率与旧策略相应量，衡量决策饱和变化。分母边界需数值保护，不能把两边都用当前概率后得到一；本地候选动作不等价自然语言pass@64。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧概率极接近边界时要审查稳定性，不能把数值异常当巨大有效信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26862">原论文</a> · <a href="../../../../post-training/2607.26862-reco/">实现解读</a> · <a href="#qa-b7324658a6699d93">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:code-optimization-rl" data-paper-title="Reinforcement Learning for Code Optimization" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Reinforcement Learning for Code Optimization LLM 后训练 FAIR at Meta / Inria 2026-07-28 代码正确不等于运行快；直接加入耗时奖励会被小测试、共享worker负载和稀疏优势淹没。作者构造DMC-Optim，用独立服务校准时长，再组合正确性、优化测试和人类参考百分位。先离线回放筛选奖励与环境，在线GRPO另处理稀疏奖励与过旧批次。原文§3–5、附录C–F 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；没有新增训练、CUDA路径或evolve接入。原文每次在线RL运行使用8至32个GPU节点、数小时至数天，且依赖独立代码执行服务，显著超出单A100/A30或Mac预算。成本过高，不复现（审查 DONE）；不下载checkpoint、不训练，不用CPU计时fixture替代完整算法。  在线强化学习 代码效率奖励与执行校准 LLM 后训练 策略优化：谁在采样，谁在被更新 代码优化RL为什么不能只奖励程序答案正确？ 正确性是前提，目标还包括运行速度；但计时受输入规模与机器负载影响，需要专门测试和校准，才能把有效优化与环境噪声区分。 例如两个算法输出一样，较大输入下运行差异才可能体现真正复杂度改进。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-code-optimization-rl-602974e9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2c4471ecbedbb6a3">代码优化RL为什么不能只奖励程序答案正确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acode-optimization-rl">Reinforcement Learning for Code Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确性是前提，目标还包括运行速度；但计时受输入规模与机器负载影响，需要专门测试和校准，才能把有效优化与环境噪声区分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个算法输出一样，较大输入下运行差异才可能体现真正复杂度改进。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25970">原论文</a> · <a href="../../../../post-training/2607.25970-code-optimization-rl/">实现解读</a> · <a href="#qa-2c4471ecbedbb6a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:code-optimization-rl" data-paper-title="Reinforcement Learning for Code Optimization" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Reinforcement Learning for Code Optimization LLM 后训练 FAIR at Meta / Inria 2026-07-28 代码正确不等于运行快；直接加入耗时奖励会被小测试、共享worker负载和稀疏优势淹没。作者构造DMC-Optim，用独立服务校准时长，再组合正确性、优化测试和人类参考百分位。先离线回放筛选奖励与环境，在线GRPO另处理稀疏奖励与过旧批次。原文§3–5、附录C–F 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；没有新增训练、CUDA路径或evolve接入。原文每次在线RL运行使用8至32个GPU节点、数小时至数天，且依赖独立代码执行服务，显著超出单A100/A30或Mac预算。成本过高，不复现（审查 DONE）；不下载checkpoint、不训练，不用CPU计时fixture替代完整算法。  在线强化学习 代码效率奖励与执行校准 LLM 后训练 策略优化：谁在采样，谁在被更新 代码优化RL为什么先校准计时环境，再把耗时加入奖励？ 共享worker负载和小测试波动会让同一程序测得不同速度，策略可能学会利用计时噪声而非优化程序。独立沙箱计时、正确性门控与优化测试共同界定速度奖励，再处理稀疏优势和旧批次。通过语法或小夹具不能证明生产代码更快。 教学例子：一份程序恰好在空闲机器上跑得快，不应因此压过真正更高效的版本；先做同条件重复计时，再比较合法程序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2d56a2f3fb13d993">代码优化RL为什么先校准计时环境，再把耗时加入奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acode-optimization-rl">Reinforcement Learning for Code Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享worker负载和小测试波动会让同一程序测得不同速度，策略可能学会利用计时噪声而非优化程序。独立沙箱计时、正确性门控与优化测试共同界定速度奖励，再处理稀疏优势和旧批次。通过语法或小夹具不能证明生产代码更快。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一份程序恰好在空闲机器上跑得快，不应因此压过真正更高效的版本；先做同条件重复计时，再比较合法程序。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25970">原论文</a> · <a href="../../../../post-training/2607.25970-code-optimization-rl/">实现解读</a> · <a href="#qa-2d56a2f3fb13d993">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:code-optimization-rl" data-paper-title="Reinforcement Learning for Code Optimization" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Reinforcement Learning for Code Optimization LLM 后训练 FAIR at Meta / Inria 2026-07-28 代码正确不等于运行快；直接加入耗时奖励会被小测试、共享worker负载和稀疏优势淹没。作者构造DMC-Optim，用独立服务校准时长，再组合正确性、优化测试和人类参考百分位。先离线回放筛选奖励与环境，在线GRPO另处理稀疏奖励与过旧批次。原文§3–5、附录C–F 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；没有新增训练、CUDA路径或evolve接入。原文每次在线RL运行使用8至32个GPU节点、数小时至数天，且依赖独立代码执行服务，显著超出单A100/A30或Mac预算。成本过高，不复现（审查 DONE）；不下载checkpoint、不训练，不用CPU计时fixture替代完整算法。  在线强化学习 代码效率奖励与执行校准 LLM 后训练 策略优化：谁在采样，谁在被更新 代码耗时奖励与普通数学verifier奖励有何不同？ 数学正确性常可相对确定地判定，耗时则依赖测试、沙箱和负载，容易被小测试或测量噪声误导。需要门控与参考百分位，而非直接用一次墙钟时间作可靠优劣。 例如共享worker短暂拥塞会让同一程序变慢，不应误判为代码退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4891bbeecea8b14a">代码耗时奖励与普通数学verifier奖励有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acode-optimization-rl">Reinforcement Learning for Code Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>数学正确性常可相对确定地判定，耗时则依赖测试、沙箱和负载，容易被小测试或测量噪声误导。需要门控与参考百分位，而非直接用一次墙钟时间作可靠优劣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如共享worker短暂拥塞会让同一程序变慢，不应误判为代码退化。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25970">原论文</a> · <a href="../../../../post-training/2607.25970-code-optimization-rl/">实现解读</a> · <a href="#qa-4891bbeecea8b14a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:code-optimization-rl" data-paper-title="Reinforcement Learning for Code Optimization" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Reinforcement Learning for Code Optimization LLM 后训练 FAIR at Meta / Inria 2026-07-28 代码正确不等于运行快；直接加入耗时奖励会被小测试、共享worker负载和稀疏优势淹没。作者构造DMC-Optim，用独立服务校准时长，再组合正确性、优化测试和人类参考百分位。先离线回放筛选奖励与环境，在线GRPO另处理稀疏奖励与过旧批次。原文§3–5、附录C–F 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；没有新增训练、CUDA路径或evolve接入。原文每次在线RL运行使用8至32个GPU节点、数小时至数天，且依赖独立代码执行服务，显著超出单A100/A30或Mac预算。成本过高，不复现（审查 DONE）；不下载checkpoint、不训练，不用CPU计时fixture替代完整算法。  在线强化学习 代码效率奖励与执行校准 LLM 后训练 策略优化：谁在采样，谁在被更新 代码优化方法的本地组件能替代独立计时服务吗？ 不能。真实奖励需通过正确性及优化测试、独立沙箱校准，再处理稀疏优势和陈旧批次；只计算奖励公式不包含这套执行环境，也不能编造真实加速测量。 例如模拟给出快慢分数，未实际运行代码，就只能验证更新接口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d0b6f1cfd3a1e5ab">代码优化方法的本地组件能替代独立计时服务吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acode-optimization-rl">Reinforcement Learning for Code Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。真实奖励需通过正确性及优化测试、独立沙箱校准，再处理稀疏优势和陈旧批次；只计算奖励公式不包含这套执行环境，也不能编造真实加速测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模拟给出快慢分数，未实际运行代码，就只能验证更新接口。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25970">原论文</a> · <a href="../../../../post-training/2607.25970-code-optimization-rl/">实现解读</a> · <a href="#qa-d0b6f1cfd3a1e5ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:iso-rlvr" data-paper-title="ISO: An RLVR-Native Optimization Stack" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ISO: An RLVR-Native Optimization Stack LLM 后训练 The University of Texas at Austin 2026-07-21 固定预训练权重奇异值，仅优化输入/输出 singular frames；同时提供无数据 specialist merger。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  RLVR 优化器 LLM 后训练 策略优化：谁在采样，谁在被更新 ISO为什么固定奇异值而只调整singular frames？ 固定谱强度、改变输入输出方向，提供一种受结构限制的适配空间，减少任意重塑权重。它不是冻结整层，也不意味着权重功能完全不变。 例如同样各方向伸缩强度，旋转输入和输出基仍能改变处理哪些特征。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-iso-rlvr-42a6dc22" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f42c411f56be25bc">ISO为什么固定奇异值而只调整singular frames？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aiso-rlvr">ISO: An RLVR-Native Optimization Stack</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定谱强度、改变输入输出方向，提供一种受结构限制的适配空间，减少任意重塑权重。它不是冻结整层，也不意味着权重功能完全不变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样各方向伸缩强度，旋转输入和输出基仍能改变处理哪些特征。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19331">原论文</a> · <a href="../../../../post-training/2607.19331-iso-rlvr/">实现解读</a> · <a href="#qa-f42c411f56be25bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:iso-rlvr" data-paper-title="ISO: An RLVR-Native Optimization Stack" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ISO: An RLVR-Native Optimization Stack LLM 后训练 The University of Texas at Austin 2026-07-21 固定预训练权重奇异值，仅优化输入/输出 singular frames；同时提供无数据 specialist merger。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  RLVR 优化器 LLM 后训练 策略优化：谁在采样，谁在被更新 ISO固定奇异值只优化singular frames，和普通低秩增量训练有什么不同？ 固定谱把参数变化限制为输入与输出奇异方向的调整，而非自由改变所有幅度或任意加一个低秩矩阵。这个约束影响可达权重集合，也为专家合并提供结构。只验证小矩阵或候选策略上的保持性质，不能据此声称完整模型优化栈已被复现。 教学例子：同一组奇异值对应的矩阵仍可因方向旋转而改变映射；因此“谱不变”不意味着模型行为不变，也不等于参数被冻结。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d6e53e6e465caeee">ISO固定奇异值只优化singular frames，和普通低秩增量训练有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aiso-rlvr">ISO: An RLVR-Native Optimization Stack</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定谱把参数变化限制为输入与输出奇异方向的调整，而非自由改变所有幅度或任意加一个低秩矩阵。这个约束影响可达权重集合，也为专家合并提供结构。只验证小矩阵或候选策略上的保持性质，不能据此声称完整模型优化栈已被复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一组奇异值对应的矩阵仍可因方向旋转而改变映射；因此“谱不变”不意味着模型行为不变，也不等于参数被冻结。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19331">原论文</a> · <a href="../../../../post-training/2607.19331-iso-rlvr/">实现解读</a> · <a href="#qa-d6e53e6e465caeee">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:iso-rlvr" data-paper-title="ISO: An RLVR-Native Optimization Stack" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ISO: An RLVR-Native Optimization Stack LLM 后训练 The University of Texas at Austin 2026-07-21 固定预训练权重奇异值，仅优化输入/输出 singular frames；同时提供无数据 specialist merger。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  RLVR 优化器 LLM 后训练 策略优化：谁在采样，谁在被更新 ISO固定谱与GCPO保护主子空间是不是同一种约束？ 不是。ISO固定奇异值而可改变奇异框架，GCPO限制更新不得进入选定主空间；固定量与允许变化的方向不同，只能按机制比较，不能由名字相近推断等价。 例如保持尺度但转动方向，与保持主方向不动再在补空间更新，并非一回事。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a6056b798db106b9">ISO固定谱与GCPO保护主子空间是不是同一种约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aiso-rlvr">ISO: An RLVR-Native Optimization Stack</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。ISO固定奇异值而可改变奇异框架，GCPO限制更新不得进入选定主空间；固定量与允许变化的方向不同，只能按机制比较，不能由名字相近推断等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保持尺度但转动方向，与保持主方向不动再在补空间更新，并非一回事。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19331">原论文</a> · <a href="../../../../post-training/2607.19331-iso-rlvr/">实现解读</a> · <a href="#qa-a6056b798db106b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:iso-rlvr" data-paper-title="ISO: An RLVR-Native Optimization Stack" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ISO: An RLVR-Native Optimization Stack LLM 后训练 The University of Texas at Austin 2026-07-21 固定预训练权重奇异值，仅优化输入/输出 singular frames；同时提供无数据 specialist merger。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  RLVR 优化器 LLM 后训练 策略优化：谁在采样，谁在被更新 ISO实现中怎样避免把Σ也作为可训练参数？ 参数化需明确固定Σ0，只把允许的输入输出框架交给优化器，并检查相应结构约束。普通无约束矩阵更新会改变谱；本地候选核未覆盖原文完整大模型栈。 例如把重建矩阵整体设requires_grad后任意更新，会绕过固定奇异值的设计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8f88d7e0f9daefca">ISO实现中怎样避免把Σ也作为可训练参数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aiso-rlvr">ISO: An RLVR-Native Optimization Stack</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参数化需明确固定Σ0，只把允许的输入输出框架交给优化器，并检查相应结构约束。普通无约束矩阵更新会改变谱；本地候选核未覆盖原文完整大模型栈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把重建矩阵整体设requires_grad后任意更新，会绕过固定奇异值的设计。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19331">原论文</a> · <a href="../../../../post-training/2607.19331-iso-rlvr/">实现解读</a> · <a href="#qa-8f88d7e0f9daefca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:off-context-grpo" data-paper-title="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information LLM 后训练 Meta AI 2026-07-21 困难题上 vanilla GRPO 常因整组 rollout 都失败而没有有效优势信号。Off-Context GRPO 只在采样时向 behavior policy 提供解题草稿或提示等 privileged information，提高成功轨迹出现率；优化目标仍是原始无提示 policy，并用 importance ratio 校正两种采样分布的偏差，因此推理时不需要特权上下文。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 privileged rollout 和 importance correction；Qwen2.5 大模型规模未复刻。脚本下载并使用官方 GSM8K。vanilla GRPO 从原问题采样；OC-GRPO 从包含官方解题过程的 behavior distribution 采样，计算 exact-answer reward、group-relative advantage 和 target/behavior importance correction。  rlvr grpo reasoning privileged-information LLM 后训练 策略优化：谁在采样，谁在被更新 Off-Context GRPO为什么只让behavior看特权提示？ 提示帮助采到成功轨迹，目标策略仍按部署条件只看原题。这样训练学习无提示行为；若目标也看到解题信息，就不再检验推理时无需特权上下文。 例如采样器可拿到一段草稿，目标评分时必须去掉这段草稿。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-off-context-grpo-ccd1608e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-71690cceadeeaf26">Off-Context GRPO为什么只让behavior看特权提示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoff-context-grpo">Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提示帮助采到成功轨迹，目标策略仍按部署条件只看原题。这样训练学习无提示行为；若目标也看到解题信息，就不再检验推理时无需特权上下文。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如采样器可拿到一段草稿，目标评分时必须去掉这段草稿。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19313">原论文</a> · <a href="../../../../reproductions/2607.19313-off-context-grpo/">实现解读</a> · <a href="#qa-71690cceadeeaf26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:off-context-grpo" data-paper-title="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information LLM 后训练 Meta AI 2026-07-21 困难题上 vanilla GRPO 常因整组 rollout 都失败而没有有效优势信号。Off-Context GRPO 只在采样时向 behavior policy 提供解题草稿或提示等 privileged information，提高成功轨迹出现率；优化目标仍是原始无提示 policy，并用 importance ratio 校正两种采样分布的偏差，因此推理时不需要特权上下文。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 privileged rollout 和 importance correction；Qwen2.5 大模型规模未复刻。脚本下载并使用官方 GSM8K。vanilla GRPO 从原问题采样；OC-GRPO 从包含官方解题过程的 behavior distribution 采样，计算 exact-answer reward、group-relative advantage 和 target/behavior importance correction。  rlvr grpo reasoning privileged-information LLM 后训练 策略优化：谁在采样，谁在被更新 Off-Context GRPO采样时给提示，为什么优化与推理却仍使用无提示策略？ 提示用于提高困难题成功轨迹的出现率，采样行为分布因此不同于目标策略。训练用无提示策略概率与带特权行为概率的比值校正，而不是训练一个依赖提示才能运行的模型。忽略分母或把提示留在评测输入中，都会改变方法所声称的任务。 教学例子：训练教师给出一段草稿帮助采到正确续写；更新时学生仍只条件于原题，测试时也不能把那段草稿偷偷保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5a3ebe3e47f8ed51">Off-Context GRPO采样时给提示，为什么优化与推理却仍使用无提示策略？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoff-context-grpo">Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提示用于提高困难题成功轨迹的出现率，采样行为分布因此不同于目标策略。训练用无提示策略概率与带特权行为概率的比值校正，而不是训练一个依赖提示才能运行的模型。忽略分母或把提示留在评测输入中，都会改变方法所声称的任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练教师给出一段草稿帮助采到正确续写；更新时学生仍只条件于原题，测试时也不能把那段草稿偷偷保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19313">原论文</a> · <a href="../../../../reproductions/2607.19313-off-context-grpo/">实现解读</a> · <a href="#qa-5a3ebe3e47f8ed51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:off-context-grpo" data-paper-title="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information LLM 后训练 Meta AI 2026-07-21 困难题上 vanilla GRPO 常因整组 rollout 都失败而没有有效优势信号。Off-Context GRPO 只在采样时向 behavior policy 提供解题草稿或提示等 privileged information，提高成功轨迹出现率；优化目标仍是原始无提示 policy，并用 importance ratio 校正两种采样分布的偏差，因此推理时不需要特权上下文。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 privileged rollout 和 importance correction；Qwen2.5 大模型规模未复刻。脚本下载并使用官方 GSM8K。vanilla GRPO 从原问题采样；OC-GRPO 从包含官方解题过程的 behavior distribution 采样，计算 exact-answer reward、group-relative advantage 和 target/behavior importance correction。  rlvr grpo reasoning privileged-information LLM 后训练 策略优化：谁在采样，谁在被更新 它与直接对提示后回答做普通SFT有何区别？ 它保留可验证奖励和组内相对信号，并校正有提示采样与无提示目标分布；普通模仿不自动处理这种采样差。两者都需严格隔离评测答案。 例如有提示更易生成某解法，不代表无提示策略原来以同样频率生成它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1b49e62f44a966b7">它与直接对提示后回答做普通SFT有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoff-context-grpo">Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它保留可验证奖励和组内相对信号，并校正有提示采样与无提示目标分布；普通模仿不自动处理这种采样差。两者都需严格隔离评测答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如有提示更易生成某解法，不代表无提示策略原来以同样频率生成它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19313">原论文</a> · <a href="../../../../reproductions/2607.19313-off-context-grpo/">实现解读</a> · <a href="#qa-1b49e62f44a966b7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:off-context-grpo" data-paper-title="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information LLM 后训练 Meta AI 2026-07-21 困难题上 vanilla GRPO 常因整组 rollout 都失败而没有有效优势信号。Off-Context GRPO 只在采样时向 behavior policy 提供解题草稿或提示等 privileged information，提高成功轨迹出现率；优化目标仍是原始无提示 policy，并用 importance ratio 校正两种采样分布的偏差，因此推理时不需要特权上下文。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 privileged rollout 和 importance correction；Qwen2.5 大模型规模未复刻。脚本下载并使用官方 GSM8K。vanilla GRPO 从原问题采样；OC-GRPO 从包含官方解题过程的 behavior distribution 采样，计算 exact-answer reward、group-relative advantage 和 target/behavior importance correction。  rlvr grpo reasoning privileged-information LLM 后训练 策略优化：谁在采样，谁在被更新 Off-Context重要性比分子分母分别条件于什么？ 分子是原问题下目标策略概率，分母是问题加特权信息下behavior采样概率。回答前缀相同，条件上下文不同；不能把两边都用带提示概率让比值退化。 例如删除提示只发生在目标视图，分母仍须保留真实采样时的提示条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a4a13b9d97f85b98">Off-Context重要性比分子分母分别条件于什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoff-context-grpo">Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分子是原问题下目标策略概率，分母是问题加特权信息下behavior采样概率。回答前缀相同，条件上下文不同；不能把两边都用带提示概率让比值退化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删除提示只发生在目标视图，分母仍须保留真实采样时的提示条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19313">原论文</a> · <a href="../../../../reproductions/2607.19313-off-context-grpo/">实现解读</a> · <a href="#qa-a4a13b9d97f85b98">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ripo" data-paper-title="RIPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RIPO LLM 后训练 Tsinghua University 2026-07-11 固定 PPO ratio 区间在低概率区域过于保守、在高概率区域又可能过大。RIPO 以 Fisher–Rao 几何定义策略距离，并按旧策略概率设置等距 clip 半径，使不同概率区域获得更均衡的局部 KL 预算。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作概率替代 token 分布，验证动态 clip 与梯度路径，不复刻论文的全参数长 CoT 训练。在 GSM8K candidate-policy 上实际执行依旧概率相关的 Fisher–Rao clip、组内优势和旧 rollout policy 刷新，并记录各样本动态半径。  几何信任域 LLM 后训练 策略优化：谁在采样，谁在被更新 RIPO为什么认为固定概率比clip没有给各区域相同距离预算？ 同样比值变化在高低概率区域对应的分布距离不同。用Fisher–Rao几何按旧概率调整边界，试图让局部更新预算更均衡，而非固定百分比一刀切。 例如罕见动作与常见动作都提高相同比例，对分布几何的影响并不相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ripo-458e77e0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6c4c25eef9c2cb71">RIPO为什么认为固定概率比clip没有给各区域相同距离预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aripo">RIPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同样比值变化在高低概率区域对应的分布距离不同。用Fisher–Rao几何按旧概率调整边界，试图让局部更新预算更均衡，而非固定百分比一刀切。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如罕见动作与常见动作都提高相同比例，对分布几何的影响并不相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10169">原论文</a> · <a href="../../../../post-training/2607.10169-ripo/">实现解读</a> · <a href="#qa-6c4c25eef9c2cb71">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ripo" data-paper-title="RIPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RIPO LLM 后训练 Tsinghua University 2026-07-11 固定 PPO ratio 区间在低概率区域过于保守、在高概率区域又可能过大。RIPO 以 Fisher–Rao 几何定义策略距离，并按旧策略概率设置等距 clip 半径，使不同概率区域获得更均衡的局部 KL 预算。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作概率替代 token 分布，验证动态 clip 与梯度路径，不复刻论文的全参数长 CoT 训练。在 GSM8K candidate-policy 上实际执行依旧概率相关的 Fisher–Rao clip、组内优势和旧 rollout policy 刷新，并记录各样本动态半径。  几何信任域 LLM 后训练 策略优化：谁在采样，谁在被更新 相同PPO ratio区间在不同旧概率处，为什么不代表相同的策略距离？ 概率空间的几何随旧概率位置改变，罕见动作与高概率动作的相同比率变化会消耗不同局部KL预算。RIPO依据Fisher–Rao距离设置概率相关半径，试图让约束更可比。它改变裁剪边界而非优势标签，仍需用实际更新验证稳定性。 教学例子：把一个极少见动作的概率翻倍与把常见动作概率翻倍，对其余分布的影响不同；统一比率上限并不几何等距。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-925d5b7d5f114e23">相同PPO ratio区间在不同旧概率处，为什么不代表相同的策略距离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aripo">RIPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>概率空间的几何随旧概率位置改变，罕见动作与高概率动作的相同比率变化会消耗不同局部KL预算。RIPO依据Fisher–Rao距离设置概率相关半径，试图让约束更可比。它改变裁剪边界而非优势标签，仍需用实际更新验证稳定性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把一个极少见动作的概率翻倍与把常见动作概率翻倍，对其余分布的影响不同；统一比率上限并不几何等距。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10169">原论文</a> · <a href="../../../../post-training/2607.10169-ripo/">实现解读</a> · <a href="#qa-925d5b7d5f114e23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ripo" data-paper-title="RIPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RIPO LLM 后训练 Tsinghua University 2026-07-11 固定 PPO ratio 区间在低概率区域过于保守、在高概率区域又可能过大。RIPO 以 Fisher–Rao 几何定义策略距离，并按旧策略概率设置等距 clip 半径，使不同概率区域获得更均衡的局部 KL 预算。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作概率替代 token 分布，验证动态 clip 与梯度路径，不复刻论文的全参数长 CoT 训练。在 GSM8K candidate-policy 上实际执行依旧概率相关的 Fisher–Rao clip、组内优势和旧 rollout policy 刷新，并记录各样本动态半径。  几何信任域 LLM 后训练 策略优化：谁在采样，谁在被更新 RIPO自适应边界与直接提高PPO全局ε有何差别？ 全局ε同时放宽所有动作，RIPO依据旧概率区分位置。它是概率条件化的距离设计，不只是把训练调得更激进，也不保证任何数据都更稳。 例如只希望低概率区域有合适探索空间，不必让高概率区域也同样放大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-733379e1b83a5724">RIPO自适应边界与直接提高PPO全局ε有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aripo">RIPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局ε同时放宽所有动作，RIPO依据旧概率区分位置。它是概率条件化的距离设计，不只是把训练调得更激进，也不保证任何数据都更稳。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只希望低概率区域有合适探索空间，不必让高概率区域也同样放大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10169">原论文</a> · <a href="../../../../post-training/2607.10169-ripo/">实现解读</a> · <a href="#qa-733379e1b83a5724">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ripo" data-paper-title="RIPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RIPO LLM 后训练 Tsinghua University 2026-07-11 固定 PPO ratio 区间在低概率区域过于保守、在高概率区域又可能过大。RIPO 以 Fisher–Rao 几何定义策略距离，并按旧策略概率设置等距 clip 半径，使不同概率区域获得更均衡的局部 KL 预算。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作概率替代 token 分布，验证动态 clip 与梯度路径，不复刻论文的全参数长 CoT 训练。在 GSM8K candidate-policy 上实际执行依旧概率相关的 Fisher–Rao clip、组内优势和旧 rollout policy 刷新，并记录各样本动态半径。  几何信任域 LLM 后训练 策略优化：谁在采样，谁在被更新 RIPO动态clip应该读取更新前还是更新后的概率？ 边界按旧策略动作概率定义，训练中固定这份参照，再评价当前比值。若用不断变化的当前概率重算，会让信任域随更新移动；本地候选核不等于长CoT训练。 例如一个动作本轮被提高概率，不应据此立即重写这轮的原始允许边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-68231f74e75567f7">RIPO动态clip应该读取更新前还是更新后的概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aripo">RIPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>边界按旧策略动作概率定义，训练中固定这份参照，再评价当前比值。若用不断变化的当前概率重算，会让信任域随更新移动；本地候选核不等于长CoT训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个动作本轮被提高概率，不应据此立即重写这轮的原始允许边界。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10169">原论文</a> · <a href="../../../../post-training/2607.10169-ripo/">实现解读</a> · <a href="#qa-68231f74e75567f7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sis" data-paper-title="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment LLM 后训练 Renmin University of China 2026-07-06 异步 rollout、样本复用和 stale policy 会让 LLM 强化学习变成 off-policy 更新。标准 importance sampling（IS）在长序列上连乘后方差很大，直接 clipping 又会丢失有效梯度。SIS 将 token 级 rejection sampling 插入 GRPO、DAPO、GSPO：被接受的旧策略 token 可视为来自当前策略，其 IS ratio 直接置 1；未接受 token 仍交给原算法处理。 Fidelity: 核心机制复现。SIS 的 off-policy token 变换按论文公式实际执行；Qwen3 上的完整 RL 后训练不在本地实验中。本地对照口径：基线是标准 token-level Importance Sampling；实验组是 SIS ratio transformation；importance-weight variance 平均 -6.62%。这是 off-policy estimator 比较，DIN 与推荐排序指标均不适用。  post-training off-policy-correction importance-sampling LLM 后训练 策略优化：谁在采样，谁在被更新 SIS为什么尝试把部分旧策略token变成当前策略可用样本？ 异步和样本复用造成陈旧分布，长序列重要性连乘方差大。拒绝采样选择的接受部分可减少这种校正负担，未接受部分仍由宿主算法处理，而非整条数据一律丢弃。 例如旧批次里一些词元仍与当前分布兼容，可保留它们的训练价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-sis-7add6071" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-032fce07199c0994">SIS为什么尝试把部分旧策略token变成当前策略可用样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asis">Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>异步和样本复用造成陈旧分布，长序列重要性连乘方差大。拒绝采样选择的接受部分可减少这种校正负担，未接受部分仍由宿主算法处理，而非整条数据一律丢弃。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧批次里一些词元仍与当前分布兼容，可保留它们的训练价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.04728">原论文</a> · <a href="../../../../reproductions/2607.04728-sis/">实现解读</a> · <a href="#qa-032fce07199c0994">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sis" data-paper-title="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment LLM 后训练 Renmin University of China 2026-07-06 异步 rollout、样本复用和 stale policy 会让 LLM 强化学习变成 off-policy 更新。标准 importance sampling（IS）在长序列上连乘后方差很大，直接 clipping 又会丢失有效梯度。SIS 将 token 级 rejection sampling 插入 GRPO、DAPO、GSPO：被接受的旧策略 token 可视为来自当前策略，其 IS ratio 直接置 1；未接受 token 仍交给原算法处理。 Fidelity: 核心机制复现。SIS 的 off-policy token 变换按论文公式实际执行；Qwen3 上的完整 RL 后训练不在本地实验中。本地对照口径：基线是标准 token-level Importance Sampling；实验组是 SIS ratio transformation；importance-weight variance 平均 -6.62%。这是 off-policy estimator 比较，DIN 与推荐排序指标均不适用。  post-training off-policy-correction importance-sampling LLM 后训练 策略优化：谁在采样，谁在被更新 SIS接受旧token后为什么把ratio置1，这是否意味着整条旧轨迹都变成on-policy？ 拒绝采样在给定前缀下校正被接受动作的条件分布，理想条件下这部分无需再乘原重要性比；未接受token仍由宿主算法处理。它不把整条旧轨迹自动改成当前策略轨迹，且top-K envelope是工程近似，必须与精确采样保证区分。 教学例子：一条旧回答只有部分位置通过接受检验，不能因为其中一个token被接受，就把整段历史的全部比率都改成一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1196d9cfe453f499">SIS接受旧token后为什么把ratio置1，这是否意味着整条旧轨迹都变成on-policy？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asis">Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>拒绝采样在给定前缀下校正被接受动作的条件分布，理想条件下这部分无需再乘原重要性比；未接受token仍由宿主算法处理。它不把整条旧轨迹自动改成当前策略轨迹，且top-K envelope是工程近似，必须与精确采样保证区分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条旧回答只有部分位置通过接受检验，不能因为其中一个token被接受，就把整段历史的全部比率都改成一。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.04728">原论文</a> · <a href="../../../../reproductions/2607.04728-sis/">实现解读</a> · <a href="#qa-1196d9cfe453f499">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sis" data-paper-title="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment LLM 后训练 Renmin University of China 2026-07-06 异步 rollout、样本复用和 stale policy 会让 LLM 强化学习变成 off-policy 更新。标准 importance sampling（IS）在长序列上连乘后方差很大，直接 clipping 又会丢失有效梯度。SIS 将 token 级 rejection sampling 插入 GRPO、DAPO、GSPO：被接受的旧策略 token 可视为来自当前策略，其 IS ratio 直接置 1；未接受 token 仍交给原算法处理。 Fidelity: 核心机制复现。SIS 的 off-policy token 变换按论文公式实际执行；Qwen3 上的完整 RL 后训练不在本地实验中。本地对照口径：基线是标准 token-level Importance Sampling；实验组是 SIS ratio transformation；importance-weight variance 平均 -6.62%。这是 off-policy estimator 比较，DIN 与推荐排序指标均不适用。  post-training off-policy-correction importance-sampling LLM 后训练 策略优化：谁在采样，谁在被更新 SIS接受token后把ratio设一，与普通clip到一相同吗？ 不同。接受事件由拒绝采样分布机制决定，不是看到任意比值就数值截成一。精确包络与工程top-K近似也有区别，不能把近似选择包装成无条件精确采样保证。 例如随手把所有大比值改成一，没有提供接受样本来自目标分布的依据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-81cc7a58bc1c0e36">SIS接受token后把ratio设一，与普通clip到一相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asis">Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同。接受事件由拒绝采样分布机制决定，不是看到任意比值就数值截成一。精确包络与工程top-K近似也有区别，不能把近似选择包装成无条件精确采样保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如随手把所有大比值改成一，没有提供接受样本来自目标分布的依据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.04728">原论文</a> · <a href="../../../../reproductions/2607.04728-sis/">实现解读</a> · <a href="#qa-81cc7a58bc1c0e36">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sis" data-paper-title="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment LLM 后训练 Renmin University of China 2026-07-06 异步 rollout、样本复用和 stale policy 会让 LLM 强化学习变成 off-policy 更新。标准 importance sampling（IS）在长序列上连乘后方差很大，直接 clipping 又会丢失有效梯度。SIS 将 token 级 rejection sampling 插入 GRPO、DAPO、GSPO：被接受的旧策略 token 可视为来自当前策略，其 IS ratio 直接置 1；未接受 token 仍交给原算法处理。 Fidelity: 核心机制复现。SIS 的 off-policy token 变换按论文公式实际执行；Qwen3 上的完整 RL 后训练不在本地实验中。本地对照口径：基线是标准 token-level Importance Sampling；实验组是 SIS ratio transformation；importance-weight variance 平均 -6.62%。这是 off-policy estimator 比较，DIN 与推荐排序指标均不适用。  post-training off-policy-correction importance-sampling LLM 后训练 策略优化：谁在采样，谁在被更新 SIS的top-K envelope来自哪个策略，拒绝项怎样处理？ 工程近似用behavior的top-K候选估包络；接受项按规则置一，未接受项继续使用GRPO、DAPO或GSPO等宿主校正，不能自动也改成一或删掉。 例如一处拒绝并不表示整条响应都必须丢弃，处理仍遵循所选宿主目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1eeece4be8b6c955">SIS的top-K envelope来自哪个策略，拒绝项怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asis">Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工程近似用behavior的top-K候选估包络；接受项按规则置一，未接受项继续使用GRPO、DAPO或GSPO等宿主校正，不能自动也改成一或删掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一处拒绝并不表示整条响应都必须丢弃，处理仍遵循所选宿主目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.04728">原论文</a> · <a href="../../../../reproductions/2607.04728-sis/">实现解读</a> · <a href="#qa-1eeece4be8b6c955">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stare" data-paper-title="STARE" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="STARE LLM 后训练 Tsinghua University 2026-06-17 按 batch surprisal 分位数识别 entropy-critical token，重加权其 advantage，并以目标 entropy 闭环 gate 调节方向。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5312（+126.67%）。  Entropy 稳定 LLM 后训练 策略优化：谁在采样，谁在被更新 STARE为什么关注surprisal关键词元而非平均强化整条轨迹？ 轨迹优势相同地作用所有位置，可能在熵变化上产生不同效果。按惊讶度分位数找关键位置，再结合目标熵闭环调整权重，让更新关注分布状态而非只看终局结果。 例如一处不确定分叉与常见标点即使共享优势，也不必承担相同探索作用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-stare-ca64b168" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cf2187d20e32967c">STARE为什么关注surprisal关键词元而非平均强化整条轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astare">STARE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轨迹优势相同地作用所有位置，可能在熵变化上产生不同效果。按惊讶度分位数找关键位置，再结合目标熵闭环调整权重，让更新关注分布状态而非只看终局结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一处不确定分叉与常见标点即使共享优势，也不必承担相同探索作用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19236">原论文</a> · <a href="../../../../post-training/2606.19236-stare/">实现解读</a> · <a href="#qa-cf2187d20e32967c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stare" data-paper-title="STARE" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="STARE LLM 后训练 Tsinghua University 2026-06-17 按 batch surprisal 分位数识别 entropy-critical token，重加权其 advantage，并以目标 entropy 闭环 gate 调节方向。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5312（+126.67%）。  Entropy 稳定 LLM 后训练 策略优化：谁在采样，谁在被更新 STARE为什么同时看token surprisal和整体熵目标，而不一律强化意外token？ 高surprisal位置可能对熵变化更敏感，但持续放大它们也可能让策略过度发散。STARE先按batch分位识别关键位置，再依据当前熵与目标熵的差异调节优势权重。意外程度不是正确性，门控旨在控制训练动态，不是把罕见词都标成好动作。 教学例子：同样一个低概率token，在策略过度确定时与已经过度随机时，可能需要不同调节方向；不能永远给它额外正权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-faaef258a6b76c26">STARE为什么同时看token surprisal和整体熵目标，而不一律强化意外token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astare">STARE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高surprisal位置可能对熵变化更敏感，但持续放大它们也可能让策略过度发散。STARE先按batch分位识别关键位置，再依据当前熵与目标熵的差异调节优势权重。意外程度不是正确性，门控旨在控制训练动态，不是把罕见词都标成好动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样一个低概率token，在策略过度确定时与已经过度随机时，可能需要不同调节方向；不能永远给它额外正权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19236">原论文</a> · <a href="../../../../post-training/2606.19236-stare/">实现解读</a> · <a href="#qa-faaef258a6b76c26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stare" data-paper-title="STARE" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="STARE LLM 后训练 Tsinghua University 2026-06-17 按 batch surprisal 分位数识别 entropy-critical token，重加权其 advantage，并以目标 entropy 闭环 gate 调节方向。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5312（+126.67%）。  Entropy 稳定 LLM 后训练 策略优化：谁在采样，谁在被更新 STARE目标熵闭环与固定熵奖励有何机制区别？ 固定奖励持续朝同一熵方向推动，闭环依据当前熵与目标差距调节。它仍依赖目标设定与测量，不意味着熵越大越好，也不能由高惊讶度判定词元正确。 例如熵已高于目标时，控制方向应与熵不足时不同，而非始终鼓励随机性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dc56eb8e87c7dbc1">STARE目标熵闭环与固定熵奖励有何机制区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astare">STARE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定奖励持续朝同一熵方向推动，闭环依据当前熵与目标差距调节。它仍依赖目标设定与测量，不意味着熵越大越好，也不能由高惊讶度判定词元正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如熵已高于目标时，控制方向应与熵不足时不同，而非始终鼓励随机性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19236">原论文</a> · <a href="../../../../post-training/2606.19236-stare/">实现解读</a> · <a href="#qa-dc56eb8e87c7dbc1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stare" data-paper-title="STARE" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="STARE LLM 后训练 Tsinghua University 2026-06-17 按 batch surprisal 分位数识别 entropy-critical token，重加权其 advantage，并以目标 entropy 闭环 gate 调节方向。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5312（+126.67%）。  Entropy 稳定 LLM 后训练 策略优化：谁在采样，谁在被更新 STARE关键位置为什么按batch分位数识别？ 分位数按当前批分布定义相对关键性，与固定绝对惊讶度阈值不同。实现需固定有效词元mask和所用策略概率，排除padding；本地只验证重权与闭环核。 例如padding的伪低概率若混进统计，会把关键分位数整个移位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-144b8b66263c2dbb">STARE关键位置为什么按batch分位数识别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astare">STARE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分位数按当前批分布定义相对关键性，与固定绝对惊讶度阈值不同。实现需固定有效词元mask和所用策略概率，排除padding；本地只验证重权与闭环核。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如padding的伪低概率若混进统计，会把关键分位数整个移位。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19236">原论文</a> · <a href="../../../../post-training/2606.19236-stare/">实现解读</a> · <a href="#qa-144b8b66263c2dbb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:kpop" data-paper-title="KPop" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="KPop LLM 后训练 Ling / Ring Team 2026-06-13 异步 rollout 中的 serving 概率与训练侧概率失配，固定 ratio mask 会误删正常探索或保留错误梯度。KPop 将当前 token 与“其余词表”压缩为二元分布，只有正反两个方向的 binary KL 都低于阈值时才保留该 token 的更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实训推引擎、MoE routing 或万亿参数异步集群；本地只验证 binary-KL mask 的可审计更新语义。在候选策略的 rollout/训练双分布上计算双向 binary KL，并让 mask 真正决定每个采样动作是否产生 policy gradient。  异步训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 KPop为什么把一个token与其余词表看成二元分布？ 仅比较采样词概率比可能忽视它在整体质量中的地位。二元表示同时约束该词与补集的概率变化，用正反KL衡量训练与服务失配，再决定是否保留更新。 例如同样倍数的变化发生在罕见词或高概率词上，补集变化并不相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-kpop-03b1bc3e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4c555e547d25d78c">KPop为什么把一个token与其余词表看成二元分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Akpop">KPop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ling / Ring Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅比较采样词概率比可能忽视它在整体质量中的地位。二元表示同时约束该词与补集的概率变化，用正反KL衡量训练与服务失配，再决定是否保留更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样倍数的变化发生在罕见词或高概率词上，补集变化并不相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.15079">原论文</a> · <a href="../../../../post-training/2606.15079-kpop/">实现解读</a> · <a href="#qa-4c555e547d25d78c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:kpop" data-paper-title="KPop" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="KPop LLM 后训练 Ling / Ring Team 2026-06-13 异步 rollout 中的 serving 概率与训练侧概率失配，固定 ratio mask 会误删正常探索或保留错误梯度。KPop 将当前 token 与“其余词表”压缩为二元分布，只有正反两个方向的 binary KL 都低于阈值时才保留该 token 的更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实训推引擎、MoE routing 或万亿参数异步集群；本地只验证 binary-KL mask 的可审计更新语义。在候选策略的 rollout/训练双分布上计算双向 binary KL，并让 mask 真正决定每个采样动作是否产生 policy gradient。  异步训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 KPop为什么比较token与其余词表的双向binary KL，而不只判断ratio是否过大？ 相同比率在不同基础概率下含义不同，二元分布同时考虑当前token及其补集，更能反映局部概率变化。正反KL还具有不对称性，因此两边都过关才保留更新。这个掩码检验训推概率一致性，不证明留下的动作正确或整个异步系统无偏。 教学例子：一个罕见词与一个常见词都出现相同比率偏移，仅看ratio会同等处理；加入其余词表概率后，几何差异才显现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d03b1e6d172879e3">KPop为什么比较token与其余词表的双向binary KL，而不只判断ratio是否过大？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Akpop">KPop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ling / Ring Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同比率在不同基础概率下含义不同，二元分布同时考虑当前token及其补集，更能反映局部概率变化。正反KL还具有不对称性，因此两边都过关才保留更新。这个掩码检验训推概率一致性，不证明留下的动作正确或整个异步系统无偏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个罕见词与一个常见词都出现相同比率偏移，仅看ratio会同等处理；加入其余词表概率后，几何差异才显现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.15079">原论文</a> · <a href="../../../../post-training/2606.15079-kpop/">实现解读</a> · <a href="#qa-d03b1e6d172879e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:kpop" data-paper-title="KPop" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="KPop LLM 后训练 Ling / Ring Team 2026-06-13 异步 rollout 中的 serving 概率与训练侧概率失配，固定 ratio mask 会误删正常探索或保留错误梯度。KPop 将当前 token 与“其余词表”压缩为二元分布，只有正反两个方向的 binary KL 都低于阈值时才保留该 token 的更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实训推引擎、MoE routing 或万亿参数异步集群；本地只验证 binary-KL mask 的可审计更新语义。在候选策略的 rollout/训练双分布上计算双向 binary KL，并让 mask 真正决定每个采样动作是否产生 policy gradient。  异步训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 双向binary KL门控与固定ratio mask有何差别？ 双向KL根据概率水平自适应评估失配，固定ratio只看相对倍率。两个方向都需达标，因为KL不对称；这仍只是mask规则，不证明真实异步服务已同步。 例如一个方向KL较小不代表反向也小，只检一边会放过另一类失配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2bbe37f3bfe81534">双向binary KL门控与固定ratio mask有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Akpop">KPop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ling / Ring Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>双向KL根据概率水平自适应评估失配，固定ratio只看相对倍率。两个方向都需达标，因为KL不对称；这仍只是mask规则，不证明真实异步服务已同步。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个方向KL较小不代表反向也小，只检一边会放过另一类失配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.15079">原论文</a> · <a href="../../../../post-training/2606.15079-kpop/">实现解读</a> · <a href="#qa-2bbe37f3bfe81534">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:kpop" data-paper-title="KPop" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="KPop LLM 后训练 Ling / Ring Team 2026-06-13 异步 rollout 中的 serving 概率与训练侧概率失配，固定 ratio mask 会误删正常探索或保留错误梯度。KPop 将当前 token 与“其余词表”压缩为二元分布，只有正反两个方向的 binary KL 都低于阈值时才保留该 token 的更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实训推引擎、MoE routing 或万亿参数异步集群；本地只验证 binary-KL mask 的可审计更新语义。在候选策略的 rollout/训练双分布上计算双向 binary KL，并让 mask 真正决定每个采样动作是否产生 policy gradient。  异步训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 KPop的保留条件是两个KL同时小还是任一小？ 必须正反两个binary KL均不超过阈值；用或条件会放宽算法。边界概率需稳定处理且不能混淆serving与training来源，本地没有真实训推引擎或MoE集群。 例如只有训练到服务方向达标时仍应mask，不能因另一边通过就保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b948a36fbc87ae40">KPop的保留条件是两个KL同时小还是任一小？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Akpop">KPop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ling / Ring Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>必须正反两个binary KL均不超过阈值；用或条件会放宽算法。边界概率需稳定处理且不能混淆serving与training来源，本地没有真实训推引擎或MoE集群。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只有训练到服务方向达标时仍应mask，不能因另一边通过就保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.15079">原论文</a> · <a href="../../../../post-training/2606.15079-kpop/">实现解读</a> · <a href="#qa-b948a36fbc87ae40">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gprl" data-paper-title="GPRL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPRL LLM 后训练 Stanford University 2026-05-18 单一标量 reward 容易掩盖 helpfulness、格式、推理和简洁度之间的冲突。GPRL 先在每个偏好维度内部计算 group-relative advantage，再根据上下文聚合；漂移控制器检测某个维度是否主导训练并调整权重。 保真度：本地实现逐维 group normalization、动态聚合和漂移监控；保真度：本地实现逐维 group normalization、动态聚合和漂移监控；候选式 GSM8K 主要验证算法状态，不覆盖论文的开放式多维 judge。当前没有接入 AlpacaEval judge、开放式生成或真实人类多维偏好。GPRL 低于 DPO/OPD 的 exact-answer accuracy 是已记录的负结果，不代表论文的多维开放式结论已被否定。本地 reward 轴为 outcome、format、reasoning、brevity；每轴独立标准化并记录漂移事件。  多目标 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GPRL为什么先逐偏好维度算组内优势？ 不同维度量纲与波动不同，先在每个维度标准化，避免大数值维度自动主导；再按任务上下文聚合，表达不同质量取舍。标准化不表示各维度同样重要。 例如格式分以百分制、正确性以零一制，直接相加会让格式数值压倒正确性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gprl-3009fd16" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-fcd8ef0ba525dcfd">GPRL为什么先逐偏好维度算组内优势？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agprl">GPRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同维度量纲与波动不同，先在每个维度标准化，避免大数值维度自动主导；再按任务上下文聚合，表达不同质量取舍。标准化不表示各维度同样重要。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如格式分以百分制、正确性以零一制，直接相加会让格式数值压倒正确性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18721">原论文</a> · <a href="../../../../post-training/2605.18721-gprl/">实现解读</a> · <a href="#qa-fcd8ef0ba525dcfd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gprl" data-paper-title="GPRL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPRL LLM 后训练 Stanford University 2026-05-18 单一标量 reward 容易掩盖 helpfulness、格式、推理和简洁度之间的冲突。GPRL 先在每个偏好维度内部计算 group-relative advantage，再根据上下文聚合；漂移控制器检测某个维度是否主导训练并调整权重。 保真度：本地实现逐维 group normalization、动态聚合和漂移监控；保真度：本地实现逐维 group normalization、动态聚合和漂移监控；候选式 GSM8K 主要验证算法状态，不覆盖论文的开放式多维 judge。当前没有接入 AlpacaEval judge、开放式生成或真实人类多维偏好。GPRL 低于 DPO/OPD 的 exact-answer accuracy 是已记录的负结果，不代表论文的多维开放式结论已被否定。本地 reward 轴为 outcome、format、reasoning、brevity；每轴独立标准化并记录漂移事件。  多目标 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GPRL为什么逐偏好维度算组内优势，再按上下文聚合？ 直接相加原始奖励会让量纲大或方差大的维度支配训练，掩盖帮助性、格式与简洁性的冲突。逐维标准化先获得可比信号，再用上下文权重表达任务取舍，并监测漂移。标准化不决定价值优先级，也不能把单一答案准确率当作多维偏好的完整评估。 教学例子：一个评分维度取百分制，另一个只取少数档位，直接求和容易由前者主导；需先区分尺度与用户真正想要的权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d36e96fff938a5a3">GPRL为什么逐偏好维度算组内优势，再按上下文聚合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agprl">GPRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接相加原始奖励会让量纲大或方差大的维度支配训练，掩盖帮助性、格式与简洁性的冲突。逐维标准化先获得可比信号，再用上下文权重表达任务取舍，并监测漂移。标准化不决定价值优先级，也不能把单一答案准确率当作多维偏好的完整评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个评分维度取百分制，另一个只取少数档位，直接求和容易由前者主导；需先区分尺度与用户真正想要的权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18721">原论文</a> · <a href="../../../../post-training/2605.18721-gprl/">实现解读</a> · <a href="#qa-d36e96fff938a5a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gprl" data-paper-title="GPRL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPRL LLM 后训练 Stanford University 2026-05-18 单一标量 reward 容易掩盖 helpfulness、格式、推理和简洁度之间的冲突。GPRL 先在每个偏好维度内部计算 group-relative advantage，再根据上下文聚合；漂移控制器检测某个维度是否主导训练并调整权重。 保真度：本地实现逐维 group normalization、动态聚合和漂移监控；保真度：本地实现逐维 group normalization、动态聚合和漂移监控；候选式 GSM8K 主要验证算法状态，不覆盖论文的开放式多维 judge。当前没有接入 AlpacaEval judge、开放式生成或真实人类多维偏好。GPRL 低于 DPO/OPD 的 exact-answer accuracy 是已记录的负结果，不代表论文的多维开放式结论已被否定。本地 reward 轴为 outcome、format、reasoning、brevity；每轴独立标准化并记录漂移事件。  多目标 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GPRL与先把多维reward加总再做GRPO有什么区别？ 先加总会在归一化前混合尺度与冲突，逐维标准化再聚合保留每维相对关系。两者通常不交换；上下文权重及漂移控制还需独立验证，不能只报单一准确率。 例如一维波动很大时，先总分标准化仍可能让其他维度几乎失去作用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4acbb9a1f4e30016">GPRL与先把多维reward加总再做GRPO有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agprl">GPRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先加总会在归一化前混合尺度与冲突，逐维标准化再聚合保留每维相对关系。两者通常不交换；上下文权重及漂移控制还需独立验证，不能只报单一准确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一维波动很大时，先总分标准化仍可能让其他维度几乎失去作用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18721">原论文</a> · <a href="../../../../post-training/2605.18721-gprl/">实现解读</a> · <a href="#qa-4acbb9a1f4e30016">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gprl" data-paper-title="GPRL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPRL LLM 后训练 Stanford University 2026-05-18 单一标量 reward 容易掩盖 helpfulness、格式、推理和简洁度之间的冲突。GPRL 先在每个偏好维度内部计算 group-relative advantage，再根据上下文聚合；漂移控制器检测某个维度是否主导训练并调整权重。 保真度：本地实现逐维 group normalization、动态聚合和漂移监控；保真度：本地实现逐维 group normalization、动态聚合和漂移监控；候选式 GSM8K 主要验证算法状态，不覆盖论文的开放式多维 judge。当前没有接入 AlpacaEval judge、开放式生成或真实人类多维偏好。GPRL 低于 DPO/OPD 的 exact-answer accuracy 是已记录的负结果，不代表论文的多维开放式结论已被否定。本地 reward 轴为 outcome、format、reasoning、brevity；每轴独立标准化并记录漂移事件。  多目标 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GPRL本地exact-answer负结果能否否定论文开放式多维结论？ 不能。当前未接入真实人类多维偏好或开放生成judge，本地准确率更低是应保留的负结果，但评测目标与原文不同。实现需逐维维护均值方差和有效权重。 例如简洁性改善与最终答案命中可能冲突，单看答案分数不能概括全部维度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f517255fce38ba7b">GPRL本地exact-answer负结果能否否定论文开放式多维结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agprl">GPRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前未接入真实人类多维偏好或开放生成judge，本地准确率更低是应保留的负结果，但评测目标与原文不同。实现需逐维维护均值方差和有效权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如简洁性改善与最终答案命中可能冲突，单看答案分数不能概括全部维度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18721">原论文</a> · <a href="../../../../post-training/2605.18721-gprl/">实现解读</a> · <a href="#qa-f517255fce38ba7b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:conspo" data-paper-title="ConSPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ConSPO LLM 后训练 Beijing Institute of Technology 2026-05-13 将同组序列的优劣关系写成长度归一化 InfoNCE，避免 token 求和造成长度和组内尺度偏差。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  对比序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 ConSPO为什么用组内InfoNCE表达序列优劣？ 同提示多个序列作为相互竞争的候选，以优选序列对整组的相对分数形成目标。长度平均的logp减少序列长度尺度干扰，组内温度控制分离强度。 例如一个好解法需相对多条其他解法提高，而不仅评价它自身概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-conspo-ff3e363d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e9fd63f5b835a51b">ConSPO为什么用组内InfoNCE表达序列优劣？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aconspo">ConSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同提示多个序列作为相互竞争的候选，以优选序列对整组的相对分数形成目标。长度平均的logp减少序列长度尺度干扰，组内温度控制分离强度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个好解法需相对多条其他解法提高，而不仅评价它自身概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12969">原论文</a> · <a href="../../../../post-training/2605.12969-conspo/">实现解读</a> · <a href="#qa-e9fd63f5b835a51b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:conspo" data-paper-title="ConSPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ConSPO LLM 后训练 Beijing Institute of Technology 2026-05-13 将同组序列的优劣关系写成长度归一化 InfoNCE，避免 token 求和造成长度和组内尺度偏差。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  对比序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 ConSPO为什么用长度归一化序列分数做组内InfoNCE，而不直接累计token奖励？ 累积对数概率会随长度改变分数尺度，可能把长短差异误当优劣。ConSPO先用平均token分数表示整条响应，再在同题组内做对比，使优选响应相对其他候选得到更高概率。归一化与温度仍影响梯度，组内相对好不保证答案绝对正确。 教学例子：同题一份短回答和一份长解释都正确，直接求和可能惩罚后者；先归一化，再比较组内相对质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dcba0d92e323eff2">ConSPO为什么用长度归一化序列分数做组内InfoNCE，而不直接累计token奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aconspo">ConSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>累积对数概率会随长度改变分数尺度，可能把长短差异误当优劣。ConSPO先用平均token分数表示整条响应，再在同题组内做对比，使优选响应相对其他候选得到更高概率。归一化与温度仍影响梯度，组内相对好不保证答案绝对正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题一份短回答和一份长解释都正确，直接求和可能惩罚后者；先归一化，再比较组内相对质量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12969">原论文</a> · <a href="../../../../post-training/2605.12969-conspo/">实现解读</a> · <a href="#qa-dcba0d92e323eff2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:conspo" data-paper-title="ConSPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ConSPO LLM 后训练 Beijing Institute of Technology 2026-05-13 将同组序列的优劣关系写成长度归一化 InfoNCE，避免 token 求和造成长度和组内尺度偏差。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  对比序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 ConSPO组对比与逐个独立正负二分类有何区别？ InfoNCE的分母把全组耦合，一个候选变化会影响共同归一；独立成对损失分别计算关系。组大小和负例组成也会改变目标，不能把两者简单视为完全等价。 例如新增一条竞争回答会进入共同分母，原来的每对损失则没有同样耦合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c52cad0e9bc58eaf">ConSPO组对比与逐个独立正负二分类有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aconspo">ConSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>InfoNCE的分母把全组耦合，一个候选变化会影响共同归一；独立成对损失分别计算关系。组大小和负例组成也会改变目标，不能把两者简单视为完全等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新增一条竞争回答会进入共同分母，原来的每对损失则没有同样耦合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12969">原论文</a> · <a href="../../../../post-training/2605.12969-conspo/">实现解读</a> · <a href="#qa-c52cad0e9bc58eaf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:conspo" data-paper-title="ConSPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ConSPO LLM 后训练 Beijing Institute of Technology 2026-05-13 将同组序列的优劣关系写成长度归一化 InfoNCE，避免 token 求和造成长度和组内尺度偏差。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  对比序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 ConSPO实现中温度与长度归一化分别作用在哪里？ 先对有效响应logp按长度平均，再除温度送入组softmax，计算稳定log-sum-exp。padding与提示不得计入响应长度；本地核没有复刻论文规模训练。 例如先对每个词元任意温度处理后再改长度分母，会偏离规定序列分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6584c823e36000c0">ConSPO实现中温度与长度归一化分别作用在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aconspo">ConSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先对有效响应logp按长度平均，再除温度送入组softmax，计算稳定log-sum-exp。padding与提示不得计入响应长度；本地核没有复刻论文规模训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先对每个词元任意温度处理后再改长度分母，会偏离规定序列分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12969">原论文</a> · <a href="../../../../post-training/2605.12969-conspo/">实现解读</a> · <a href="#qa-6584c823e36000c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:missing-old-logits" data-paper-title="Missing Old Logits" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Missing Old Logits LLM 后训练 Tianjin University 2026-05-12 指出异步 RL 丢失历史训练侧 logits 后，训推校正与策略陈旧校正发生语义混叠；给出快照、old-logit model、中断同步和 PPO-EWMA 修复。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  异步 off-policy LLM 后训练 策略优化：谁在采样，谁在被更新 Missing Old Logits为什么不只是缺少一份日志？ 历史训练侧概率是区分训推失配与策略陈旧所需的参照。只留下服务概率后，两种变化混在一个比率里，难以确定优化器到底在校正什么。 例如同一词概率变化可能来自推理引擎差异，也可能来自策略已训练多步。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-missing-old-logits-37bc553d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-09973dbae7619570">Missing Old Logits为什么不只是缺少一份日志？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amissing-old-logits">Missing Old Logits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史训练侧概率是区分训推失配与策略陈旧所需的参照。只留下服务概率后，两种变化混在一个比率里，难以确定优化器到底在校正什么。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一词概率变化可能来自推理引擎差异，也可能来自策略已训练多步。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12070">原论文</a> · <a href="../../../../post-training/2605.12070-missing-old-logits/">实现解读</a> · <a href="#qa-09973dbae7619570">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:missing-old-logits" data-paper-title="Missing Old Logits" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Missing Old Logits LLM 后训练 Tianjin University 2026-05-12 指出异步 RL 丢失历史训练侧 logits 后，训推校正与策略陈旧校正发生语义混叠；给出快照、old-logit model、中断同步和 PPO-EWMA 修复。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  异步 off-policy LLM 后训练 策略优化：谁在采样，谁在被更新 丢掉历史训练侧logits后，为什么无法分清训推失配与策略陈旧？ 当前训练概率到旧推理概率的总比率可拆成历史训推差异和后续策略变化，两者需要历史训练侧概率作中间量。缺失它时，只看总比率无法判断偏移来自引擎还是权重更新。快照或old-logit模型是在恢复这个参照，不是给缺失值随便补零。 教学例子：同一旧样本现在概率变了，可能是推理引擎当时就有差，也可能训练后模型改变；没有旧训练快照，两种原因会混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-460fc794c3daf6c8">丢掉历史训练侧logits后，为什么无法分清训推失配与策略陈旧？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amissing-old-logits">Missing Old Logits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前训练概率到旧推理概率的总比率可拆成历史训推差异和后续策略变化，两者需要历史训练侧概率作中间量。缺失它时，只看总比率无法判断偏移来自引擎还是权重更新。快照或old-logit模型是在恢复这个参照，不是给缺失值随便补零。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一旧样本现在概率变了，可能是推理引擎当时就有差，也可能训练后模型改变；没有旧训练快照，两种原因会混在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12070">原论文</a> · <a href="../../../../post-training/2605.12070-missing-old-logits/">实现解读</a> · <a href="#qa-460fc794c3daf6c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:missing-old-logits" data-paper-title="Missing Old Logits" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Missing Old Logits LLM 后训练 Tianjin University 2026-05-12 指出异步 RL 丢失历史训练侧 logits 后，训推校正与策略陈旧校正发生语义混叠；给出快照、old-logit model、中断同步和 PPO-EWMA 修复。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  异步 off-policy LLM 后训练 策略优化：谁在采样，谁在被更新 训推校正与staleness校正为何需要不同分母？ 前者比较同一旧策略的训练和推理实现，后者比较当前与旧训练策略。连乘可得到整体比率，但两者不能互相替代，否则会把系统差异当作学习漂移。 例如更换推理实现但权重未变，仍可能有第一种差异，却没有同样的训练陈旧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-da5bb471e20b2a8f">训推校正与staleness校正为何需要不同分母？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amissing-old-logits">Missing Old Logits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者比较同一旧策略的训练和推理实现，后者比较当前与旧训练策略。连乘可得到整体比率，但两者不能互相替代，否则会把系统差异当作学习漂移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如更换推理实现但权重未变，仍可能有第一种差异，却没有同样的训练陈旧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12070">原论文</a> · <a href="../../../../post-training/2605.12070-missing-old-logits/">实现解读</a> · <a href="#qa-da5bb471e20b2a8f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:missing-old-logits" data-paper-title="Missing Old Logits" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Missing Old Logits LLM 后训练 Tianjin University 2026-05-12 指出异步 RL 丢失历史训练侧 logits 后，训推校正与策略陈旧校正发生语义混叠；给出快照、old-logit model、中断同步和 PPO-EWMA 修复。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  异步 off-policy LLM 后训练 策略优化：谁在采样，谁在被更新 缺失旧训练logits时能直接用当前logits回填吗？ 不能假装它仍是历史值。快照、old-logit模型、中断同步或EWMA等是明确修复方案，各有假设与成本；本地只验证分解及状态路径，未部署真实异步训练集群。 例如当前模型已更新，拿它重算旧样本会改写历史参照而非恢复原记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-19100a5769e4bc47">缺失旧训练logits时能直接用当前logits回填吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amissing-old-logits">Missing Old Logits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能假装它仍是历史值。快照、old-logit模型、中断同步或EWMA等是明确修复方案，各有假设与成本；本地只验证分解及状态路径，未部署真实异步训练集群。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如当前模型已更新，拿它重算旧样本会改写历史参照而非恢复原记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12070">原论文</a> · <a href="../../../../post-training/2605.12070-missing-old-logits/">实现解读</a> · <a href="#qa-19100a5769e4bc47">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luspo" data-paper-title="LUSPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUSPO LLM 后训练 Meituan 2026-02-05 论文从目标函数分解解释不同 RLVR 算法为何产生不同的响应长度轨迹，并指出 GSPO 的 sequence ratio 仍含长度偏置。LUSPO 对 sequence log-probability 作长度无偏归一化，避免训练中的长度坍塌。 Length-Unbiased Sequence Policy Optimization：校正 sequence policy objective 的响应长度偏差。已实现真实自由生成、sequence-level ratio 和长度无偏归一化；本地短算术响应无法覆盖论文长 CoT 的长度动力学，结论仅用于代码路径与指标口径验证。本地从 policy 自由采样完整响应，用 exact-answer verifier 评分，以长度归一化的 sequence ratio 和 group advantage 更新；同时记录 response length 与 reward 相关性。  长度无偏 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUSPO为什么把响应长度轨迹当成优化目标的一部分审查？ 不同RLVR目标对序列长度的隐含加权不同，可能导致响应逐渐坍塌或偏移。对序列logp作规定归一化，试图区分奖励学习与长度尺度效应。 例如准确率暂时不变但回答越来越短，仍需检查是否丢掉长推理覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-luspo-8b4b98a1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6e5434f9738f469e">LUSPO为什么把响应长度轨迹当成优化目标的一部分审查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluspo">LUSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同RLVR目标对序列长度的隐含加权不同，可能导致响应逐渐坍塌或偏移。对序列logp作规定归一化，试图区分奖励学习与长度尺度效应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如准确率暂时不变但回答越来越短，仍需检查是否丢掉长推理覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.05261">原论文</a> · <a href="../../../../post-training/2602.05261-luspo/">实现解读</a> · <a href="#qa-6e5434f9738f469e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luspo" data-paper-title="LUSPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUSPO LLM 后训练 Meituan 2026-02-05 论文从目标函数分解解释不同 RLVR 算法为何产生不同的响应长度轨迹，并指出 GSPO 的 sequence ratio 仍含长度偏置。LUSPO 对 sequence log-probability 作长度无偏归一化，避免训练中的长度坍塌。 Length-Unbiased Sequence Policy Optimization：校正 sequence policy objective 的响应长度偏差。已实现真实自由生成、sequence-level ratio 和长度无偏归一化；本地短算术响应无法覆盖论文长 CoT 的长度动力学，结论仅用于代码路径与指标口径验证。本地从 policy 自由采样完整响应，用 exact-answer verifier 评分，以长度归一化的 sequence ratio 和 group advantage 更新；同时记录 response length 与 reward 相关性。  长度无偏 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUSPO为什么认为sequence ratio仍需检查长度偏置，序列级更新不就已经公平了吗？ 把更新聚合到序列级并不会自动消除累积log-prob与长度的耦合。LUSPO从目标分解关注这种差异，用长度无偏口径组织序列分数，避免更新系统性推着响应变长或变短。短算术任务上跑通归一化，并不能验证长CoT训练的长度动力学。 教学例子：两条回答每步变化相近，但一条长很多，累积比率仍可能不同；称为“序列级目标”本身不能消除这种长度效应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-335bdae0fb18cc4d">LUSPO为什么认为sequence ratio仍需检查长度偏置，序列级更新不就已经公平了吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluspo">LUSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把更新聚合到序列级并不会自动消除累积log-prob与长度的耦合。LUSPO从目标分解关注这种差异，用长度无偏口径组织序列分数，避免更新系统性推着响应变长或变短。短算术任务上跑通归一化，并不能验证长CoT训练的长度动力学。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条回答每步变化相近，但一条长很多，累积比率仍可能不同；称为“序列级目标”本身不能消除这种长度效应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.05261">原论文</a> · <a href="../../../../post-training/2602.05261-luspo/">实现解读</a> · <a href="#qa-335bdae0fb18cc4d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luspo" data-paper-title="LUSPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUSPO LLM 后训练 Meituan 2026-02-05 论文从目标函数分解解释不同 RLVR 算法为何产生不同的响应长度轨迹，并指出 GSPO 的 sequence ratio 仍含长度偏置。LUSPO 对 sequence log-probability 作长度无偏归一化，避免训练中的长度坍塌。 Length-Unbiased Sequence Policy Optimization：校正 sequence policy objective 的响应长度偏差。已实现真实自由生成、sequence-level ratio 和长度无偏归一化；本地短算术响应无法覆盖论文长 CoT 的长度动力学，结论仅用于代码路径与指标口径验证。本地从 policy 自由采样完整响应，用 exact-answer verifier 评分，以长度归一化的 sequence ratio 和 group advantage 更新；同时记录 response length 与 reward 相关性。  长度无偏 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUSPO序列比与把每个token ratio独立clip有何区别？ 它先形成长度归一化的序列log-ratio再指数化，整条响应共享相应信号；逐词元裁剪处理局部比值，目标不相同。序列方法也不能自动保证任何长回答动力学。 例如一处变大另一处变小，序列平均与分别裁剪可能得到不同更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-76dd1146a3249f22">LUSPO序列比与把每个token ratio独立clip有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluspo">LUSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它先形成长度归一化的序列log-ratio再指数化，整条响应共享相应信号；逐词元裁剪处理局部比值，目标不相同。序列方法也不能自动保证任何长回答动力学。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一处变大另一处变小，序列平均与分别裁剪可能得到不同更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.05261">原论文</a> · <a href="../../../../post-training/2602.05261-luspo/">实现解读</a> · <a href="#qa-76dd1146a3249f22">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luspo" data-paper-title="LUSPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUSPO LLM 后训练 Meituan 2026-02-05 论文从目标函数分解解释不同 RLVR 算法为何产生不同的响应长度轨迹，并指出 GSPO 的 sequence ratio 仍含长度偏置。LUSPO 对 sequence log-probability 作长度无偏归一化，避免训练中的长度坍塌。 Length-Unbiased Sequence Policy Optimization：校正 sequence policy objective 的响应长度偏差。已实现真实自由生成、sequence-level ratio 和长度无偏归一化；本地短算术响应无法覆盖论文长 CoT 的长度动力学，结论仅用于代码路径与指标口径验证。本地从 policy 自由采样完整响应，用 exact-answer verifier 评分，以长度归一化的 sequence ratio 和 group advantage 更新；同时记录 response length 与 reward 相关性。  长度无偏 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUSPO本地短算术测试为什么不能证明长CoT长度稳定？ 代码虽有自由生成、序列比和长度归一化，但短响应缺少原文长链的长度演化范围。实现需按真实有效响应长度计算，不可把padding或prompt带入分母。 例如十余词的算术回答跑通，未覆盖数千词推理中逐步累积的长度变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6d27849877ca4fb1">LUSPO本地短算术测试为什么不能证明长CoT长度稳定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluspo">LUSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>代码虽有自由生成、序列比和长度归一化，但短响应缺少原文长链的长度演化范围。实现需按真实有效响应长度计算，不可把padding或prompt带入分母。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十余词的算术回答跑通，未覆盖数千词推理中逐步累积的长度变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.05261">原论文</a> · <a href="../../../../post-training/2602.05261-luspo/">实现解读</a> · <a href="#qa-6d27849877ca4fb1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:calibration-aware-rl" data-paper-title="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning LLM 后训练 University of Southern California 2026-01-19 论文指出 RLVR 虽能提高决策正确率，却可能让 decision token 极度过度自信；其方法直接调整决策 token 的概率，在保留准确率的同时降低 ECE。本仓库对应地把 accuracy 与 Brier/ECE 同时纳入报告，并只用 validation 拟合温度，禁止用 test 调参。本地实现不复刻论文的完整 RLVR 流程，属于决策概率校准机制与评测协议实现。 未复现完整 RLVR 训练，只实现决策概率校准轴、数据隔离与统一报告。  校准强化学习 决策 token LLM 后训练 策略优化：谁在采样，谁在被更新 校准感知RL中的decision token，是整段解释都正确的评分吗？ 不是。它关注承载最终决策的词元概率及其校准，不能用该概率直接评价整段推理的事实忠实性。候选决策正确与概率可信也要分别测；一个答案词元获得高概率，并不证明前面每一步解释都可靠。 教学例子：最终选项A的概率很高，只描述这次选择的信心，不能据此给此前一段可能含错误的解释全判正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-calibration-aware-rl-6e3cb1f1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b4f067719b7ff0b1">校准感知RL中的decision token，是整段解释都正确的评分吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acalibration-aware-rl">Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它关注承载最终决策的词元概率及其校准，不能用该概率直接评价整段推理的事实忠实性。候选决策正确与概率可信也要分别测；一个答案词元获得高概率，并不证明前面每一步解释都可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>最终选项A的概率很高，只描述这次选择的信心，不能据此给此前一段可能含错误的解释全判正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13284">原论文</a> · <a href="../../../../post-training/2601.13284-calibration-aware-rl/">实现解读</a> · <a href="#qa-b4f067719b7ff0b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:calibration-aware-rl" data-paper-title="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning LLM 后训练 University of Southern California 2026-01-19 论文指出 RLVR 虽能提高决策正确率，却可能让 decision token 极度过度自信；其方法直接调整决策 token 的概率，在保留准确率的同时降低 ECE。本仓库对应地把 accuracy 与 Brier/ECE 同时纳入报告，并只用 validation 拟合温度，禁止用 test 调参。本地实现不复刻论文的完整 RLVR 流程，属于决策概率校准机制与评测协议实现。 未复现完整 RLVR 训练，只实现决策概率校准轴、数据隔离与统一报告。  校准强化学习 决策 token LLM 后训练 策略优化：谁在采样，谁在被更新 准确率提高而ECE变差，为什么Calibration-Aware RL还要单独约束决策概率？ 正确决策只要求最大概率类别对，校准还要求置信与真实命中频率相符。RLVR可能把已正确的选择推得过度自信，因此两项应分开测量。本地温度只由validation选择，test用于最终报告；事后校准机制并不等于原论文完整RL训练被复现。 教学例子：两模型总选同一类别，但一个每次声称几乎必对，另一个承认不确定；准确率相同不代表概率质量相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4c73529324e3dd75">准确率提高而ECE变差，为什么Calibration-Aware RL还要单独约束决策概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acalibration-aware-rl">Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确决策只要求最大概率类别对，校准还要求置信与真实命中频率相符。RLVR可能把已正确的选择推得过度自信，因此两项应分开测量。本地温度只由validation选择，test用于最终报告；事后校准机制并不等于原论文完整RL训练被复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两模型总选同一类别，但一个每次声称几乎必对，另一个承认不确定；准确率相同不代表概率质量相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13284">原论文</a> · <a href="../../../../post-training/2601.13284-calibration-aware-rl/">实现解读</a> · <a href="#qa-4c73529324e3dd75">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:calibration-aware-rl" data-paper-title="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning LLM 后训练 University of Southern California 2026-01-19 论文指出 RLVR 虽能提高决策正确率，却可能让 decision token 极度过度自信；其方法直接调整决策 token 的概率，在保留准确率的同时降低 ECE。本仓库对应地把 accuracy 与 Brier/ECE 同时纳入报告，并只用 validation 拟合温度，禁止用 test 调参。本地实现不复刻论文的完整 RLVR 流程，属于决策概率校准机制与评测协议实现。 未复现完整 RLVR 训练，只实现决策概率校准轴、数据隔离与统一报告。  校准强化学习 决策 token LLM 后训练 策略优化：谁在采样，谁在被更新 本地温度校准与原论文完整RLVR训练有什么差别？ 温度在已有logits上调整概率尺度，原论文训练会改变决策模型本身。两者都关注校准，但执行环节不同，不能把后处理结果称为完整训练复现。 例如冻结模型调T，不涉及重新采样轨迹和策略梯度更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4e7311780075723f">本地温度校准与原论文完整RLVR训练有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acalibration-aware-rl">Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>温度在已有logits上调整概率尺度，原论文训练会改变决策模型本身。两者都关注校准，但执行环节不同，不能把后处理结果称为完整训练复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如冻结模型调T，不涉及重新采样轨迹和策略梯度更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13284">原论文</a> · <a href="../../../../post-training/2601.13284-calibration-aware-rl/">实现解读</a> · <a href="#qa-4e7311780075723f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:calibration-aware-rl" data-paper-title="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning LLM 后训练 University of Southern California 2026-01-19 论文指出 RLVR 虽能提高决策正确率，却可能让 decision token 极度过度自信；其方法直接调整决策 token 的概率，在保留准确率的同时降低 ECE。本仓库对应地把 accuracy 与 Brier/ECE 同时纳入报告，并只用 validation 拟合温度，禁止用 test 调参。本地实现不复刻论文的完整 RLVR 流程，属于决策概率校准机制与评测协议实现。 未复现完整 RLVR 训练，只实现决策概率校准轴、数据隔离与统一报告。  校准强化学习 决策 token LLM 后训练 策略优化：谁在采样，谁在被更新 校准温度T允许在测试NLL上选择吗？ 不允许。只在验证NLL上拟合，冻结后报告测试准确率与校准指标；测试调T会把最终评估用于选择。本地实现只覆盖校准轴和隔离协议。 例如试遍温度看测试哪点最好，再报告该点，会高估未见数据表现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-586428ee262c0ee4">校准温度T允许在测试NLL上选择吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acalibration-aware-rl">Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不允许。只在验证NLL上拟合，冻结后报告测试准确率与校准指标；测试调T会把最终评估用于选择。本地实现只覆盖校准轴和隔离协议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如试遍温度看测试哪点最好，再报告该点，会高估未见数据表现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13284">原论文</a> · <a href="../../../../post-training/2601.13284-calibration-aware-rl/">实现解读</a> · <a href="#qa-586428ee262c0ee4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:online-icepop" data-paper-title="Online IcePop" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Online IcePop LLM 后训练 Ant Group 2025-12-16 普通 IcePop 同时面对训练/rollout 引擎差异和一次 rollout 被多次更新造成的策略陈旧。Online IcePop 强制每个 rollout batch 只更新一次，使 stale-policy ratio 恒为 1，从目标中移除 PPO ratio 与 clip；训练侧仍用 IcePop 双侧 mask 和区间内原始 ratio 校正引擎失配。 每个训练 step 后立即把当前权重刷新为下一批 rollout 权重，诊断中强制 policy_staleness_ratio_mean=1、关闭 PPO clip，同时沿用 IcePop [0.5, 5.0] 双侧 mask。本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。本地一个 candidate group 对应一个 rollout batch，不包含真实并行采样和通信；验证的是单次更新调度、stale ratio 消除和训推 mask 的组合语义。  纯在线训推校正 LLM 后训练 策略优化：谁在采样，谁在被更新 Online IcePop为什么要求一批rollout只更新一次？ 单次更新避免同一批被反复利用产生额外策略陈旧，使更新起点的policy ratio为一；它仍保留训练与推理引擎数值失配校正，并非所有比率都消失。 例如新批次用完就丢，不再拿已更新策略对旧批次做第二轮。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-online-icepop-2e9d86d8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-491d6e763ccc16dc">Online IcePop为什么要求一批rollout只更新一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aonline-icepop">Online IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次更新避免同一批被反复利用产生额外策略陈旧，使更新起点的policy ratio为一；它仍保留训练与推理引擎数值失配校正，并非所有比率都消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新批次用完就丢，不再拿已更新策略对旧批次做第二轮。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://zhuanlan.zhihu.com/p/1984379979035850499">原始资料</a> · <a href="../../../../post-training/web-2025-online-icepop/">实现解读</a> · <a href="#qa-491d6e763ccc16dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:online-icepop" data-paper-title="Online IcePop" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Online IcePop LLM 后训练 Ant Group 2025-12-16 普通 IcePop 同时面对训练/rollout 引擎差异和一次 rollout 被多次更新造成的策略陈旧。Online IcePop 强制每个 rollout batch 只更新一次，使 stale-policy ratio 恒为 1，从目标中移除 PPO ratio 与 clip；训练侧仍用 IcePop 双侧 mask 和区间内原始 ratio 校正引擎失配。 每个训练 step 后立即把当前权重刷新为下一批 rollout 权重，诊断中强制 policy_staleness_ratio_mean=1、关闭 PPO clip，同时沿用 IcePop [0.5, 5.0] 双侧 mask。本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。本地一个 candidate group 对应一个 rollout batch，不包含真实并行采样和通信；验证的是单次更新调度、stale ratio 消除和训推 mask 的组合语义。  纯在线训推校正 LLM 后训练 策略优化：谁在采样，谁在被更新 Online IcePop每批只更新一次后，为什么仍不能删掉训推引擎校正？ 单次使用新鲜rollout消除了跨更新复用造成的策略陈旧，所以对应policy ratio在采样点为一，不再需要那条PPO裁剪路径。但同一权重在推理和训练引擎中仍可能给出不同概率，双侧IcePop掩码及区间内原始比率仍负责这一差异。 教学例子：刚采样的回答虽然没有过期，推理端与训练端精度仍不同；“新鲜数据”不意味着两个引擎算出的概率完全一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7d8fc111dd88f837">Online IcePop每批只更新一次后，为什么仍不能删掉训推引擎校正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aonline-icepop">Online IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次使用新鲜rollout消除了跨更新复用造成的策略陈旧，所以对应policy ratio在采样点为一，不再需要那条PPO裁剪路径。但同一权重在推理和训练引擎中仍可能给出不同概率，双侧IcePop掩码及区间内原始比率仍负责这一差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>刚采样的回答虽然没有过期，推理端与训练端精度仍不同；“新鲜数据”不意味着两个引擎算出的概率完全一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://zhuanlan.zhihu.com/p/1984379979035850499">原始资料</a> · <a href="../../../../post-training/web-2025-online-icepop/">实现解读</a> · <a href="#qa-7d8fc111dd88f837">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:online-icepop" data-paper-title="Online IcePop" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Online IcePop LLM 后训练 Ant Group 2025-12-16 普通 IcePop 同时面对训练/rollout 引擎差异和一次 rollout 被多次更新造成的策略陈旧。Online IcePop 强制每个 rollout batch 只更新一次，使 stale-policy ratio 恒为 1，从目标中移除 PPO ratio 与 clip；训练侧仍用 IcePop 双侧 mask 和区间内原始 ratio 校正引擎失配。 每个训练 step 后立即把当前权重刷新为下一批 rollout 权重，诊断中强制 policy_staleness_ratio_mean=1、关闭 PPO clip，同时沿用 IcePop [0.5, 5.0] 双侧 mask。本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。本地一个 candidate group 对应一个 rollout batch，不包含真实并行采样和通信；验证的是单次更新调度、stale ratio 消除和训推 mask 的组合语义。  纯在线训推校正 LLM 后训练 策略优化：谁在采样，谁在被更新 Online IcePop与普通IcePop少掉的是哪种校正？ 少掉重复更新引入的stale-policy ratio与PPO clip，保留训推双侧mask和区间内原比值。若仍多轮优化同一批，就不能沿用纯在线设定的简化。 例如省略PPO比值的前提是调度改变，而不是单删一行公式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-16114b522aa61dbb">Online IcePop与普通IcePop少掉的是哪种校正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aonline-icepop">Online IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>少掉重复更新引入的stale-policy ratio与PPO clip，保留训推双侧mask和区间内原比值。若仍多轮优化同一批，就不能沿用纯在线设定的简化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如省略PPO比值的前提是调度改变，而不是单删一行公式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://zhuanlan.zhihu.com/p/1984379979035850499">原始资料</a> · <a href="../../../../post-training/web-2025-online-icepop/">实现解读</a> · <a href="#qa-16114b522aa61dbb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:online-icepop" data-paper-title="Online IcePop" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Online IcePop LLM 后训练 Ant Group 2025-12-16 普通 IcePop 同时面对训练/rollout 引擎差异和一次 rollout 被多次更新造成的策略陈旧。Online IcePop 强制每个 rollout batch 只更新一次，使 stale-policy ratio 恒为 1，从目标中移除 PPO ratio 与 clip；训练侧仍用 IcePop 双侧 mask 和区间内原始 ratio 校正引擎失配。 每个训练 step 后立即把当前权重刷新为下一批 rollout 权重，诊断中强制 policy_staleness_ratio_mean=1、关闭 PPO clip，同时沿用 IcePop [0.5, 5.0] 双侧 mask。本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。本地一个 candidate group 对应一个 rollout batch，不包含真实并行采样和通信；验证的是单次更新调度、stale ratio 消除和训推 mask 的组合语义。  纯在线训推校正 LLM 后训练 策略优化：谁在采样，谁在被更新 怎样验证Online IcePop没有暗中复用同一批次？ 批次需要唯一身份和消费状态，第二次更新应被拒绝；一个candidate group对应一批只是本地调度代理，不包含真实并行通信或采样集群。 例如重试回调再次送来同批数据，也不能被当作一批新鲜轨迹。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c2fc001681f837ad">怎样验证Online IcePop没有暗中复用同一批次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aonline-icepop">Online IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>批次需要唯一身份和消费状态，第二次更新应被拒绝；一个candidate group对应一批只是本地调度代理，不包含真实并行通信或采样集群。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如重试回调再次送来同批数据，也不能被当作一批新鲜轨迹。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://zhuanlan.zhihu.com/p/1984379979035850499">原始资料</a> · <a href="../../../../post-training/web-2025-online-icepop/">实现解读</a> · <a href="#qa-c2fc001681f837ad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minirl" data-paper-title="Stabilizing RL with LLMs" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Stabilizing RL with LLMs LLM 后训练 Alibaba Qwen Team 2025-12-01 分解训推差异与 policy staleness，on-policy 使用 importance correction，off-policy 结合 clipping 与 MoE Routing Replay。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  稳定 MoE RL LLM 后训练 策略优化：谁在采样，谁在被更新 miniRL为什么同时考虑训推差异和策略陈旧？ 相同权重在不同引擎下也可能给不同概率，旧权重与新权重之间还存在学习漂移。两者来源不同，分解后才能为on-policy与off-policy设置合适校正。 例如更换内核造成偏差，与模型训练后概率改变，不能都归因于同一个旧模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-minirl-5767c2fc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-fe81c4815abf4b1f">miniRL为什么同时考虑训推差异和策略陈旧？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminirl">Stabilizing RL with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同权重在不同引擎下也可能给不同概率，旧权重与新权重之间还存在学习漂移。两者来源不同，分解后才能为on-policy与off-policy设置合适校正。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如更换内核造成偏差，与模型训练后概率改变，不能都归因于同一个旧模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.01374">原论文</a> · <a href="../../../../post-training/2512.01374-minirl/">实现解读</a> · <a href="#qa-fe81c4815abf4b1f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minirl" data-paper-title="Stabilizing RL with LLMs" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Stabilizing RL with LLMs LLM 后训练 Alibaba Qwen Team 2025-12-01 分解训推差异与 policy staleness，on-policy 使用 importance correction，off-policy 结合 clipping 与 MoE Routing Replay。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  稳定 MoE RL LLM 后训练 策略优化：谁在采样，谁在被更新 MiniRL为什么把训推差异与policy staleness拆开，MoE Routing Replay又处理哪层不一致？ 引擎数值差异与参数更新造成的陈旧是不同来源，不能用同一个未说明的比率混过去。方法对在策略部分做概率校正，对离策略更新结合裁剪，并重放rollout时的MoE路由以减少执行路径变化。概率权重和专家路径都需核对，小核诊断不代表集群验证。 教学例子：相同token在采样时走专家甲，训练重算时走专家乙，即使权重刚同步也会产生差异；仅调陈旧比率未必解决。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a451194042251330">MiniRL为什么把训推差异与policy staleness拆开，MoE Routing Replay又处理哪层不一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminirl">Stabilizing RL with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>引擎数值差异与参数更新造成的陈旧是不同来源，不能用同一个未说明的比率混过去。方法对在策略部分做概率校正，对离策略更新结合裁剪，并重放rollout时的MoE路由以减少执行路径变化。概率权重和专家路径都需核对，小核诊断不代表集群验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相同token在采样时走专家甲，训练重算时走专家乙，即使权重刚同步也会产生差异；仅调陈旧比率未必解决。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.01374">原论文</a> · <a href="../../../../post-training/2512.01374-minirl/">实现解读</a> · <a href="#qa-a451194042251330">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minirl" data-paper-title="Stabilizing RL with LLMs" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Stabilizing RL with LLMs LLM 后训练 Alibaba Qwen Team 2025-12-01 分解训推差异与 policy staleness，on-policy 使用 importance correction，off-policy 结合 clipping 与 MoE Routing Replay。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  稳定 MoE RL LLM 后训练 策略优化：谁在采样，谁在被更新 MoE Routing Replay与普通ratio clipping各解决什么？ 路由重放约束专家执行路径的一致性，裁剪限制概率比带来的更新幅度。它们作用层次不同，裁剪并不会自动恢复曾经使用的专家分支。 例如保留旧专家选择信息，与只把一个过大概率比压小，不是同一干预。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e1ec329e91d3f23e">MoE Routing Replay与普通ratio clipping各解决什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminirl">Stabilizing RL with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路由重放约束专家执行路径的一致性，裁剪限制概率比带来的更新幅度。它们作用层次不同，裁剪并不会自动恢复曾经使用的专家分支。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保留旧专家选择信息，与只把一个过大概率比压小，不是同一干预。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.01374">原论文</a> · <a href="../../../../post-training/2512.01374-minirl/">实现解读</a> · <a href="#qa-e1ec329e91d3f23e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minirl" data-paper-title="Stabilizing RL with LLMs" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Stabilizing RL with LLMs LLM 后训练 Alibaba Qwen Team 2025-12-01 分解训推差异与 policy staleness，on-policy 使用 importance correction，off-policy 结合 clipping 与 MoE Routing Replay。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  稳定 MoE RL LLM 后训练 策略优化：谁在采样，谁在被更新 miniRL本地状态核能证明真实MoE集群稳定吗？ 不能。当前验证校正、裁剪和路由状态的机制语义，未复刻大模型分布式训练。实际重放还需记录并对齐每词元路由，不能用标签字段替代真正执行。 例如日志写着replay，不表示前向计算已经按记录的专家路径运行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6b23a91234d3e2e2">miniRL本地状态核能证明真实MoE集群稳定吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminirl">Stabilizing RL with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前验证校正、裁剪和路由状态的机制语义，未复刻大模型分布式训练。实际重放还需记录并对齐每词元路由，不能用标签字段替代真正执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如日志写着replay，不表示前向计算已经按记录的专家路径运行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.01374">原论文</a> · <a href="../../../../post-training/2512.01374-minirl/">实现解读</a> · <a href="#qa-6b23a91234d3e2e2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:icepop" data-paper-title="IcePop" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="IcePop LLM 后训练 Ant Group 2025-10-21 MoE router 会放大训练引擎与 rollout 引擎的微小数值差异，单侧 TIS 仍可能保留严重偏小的失配 ratio。IcePop 对训练侧与 rollout 引擎的 token 概率比设置固定双侧区间；区间内保留原始校正权重，区间外 token 的本次策略梯度直接归零。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实 MoE expert routing、万亿参数模型或异步集群；本地只隔离复现固定双侧 mask 与原始区间内校正权重。在与 TIS 相同的候选策略和引擎失配模拟中采用公开实现常用的 [0.5, 5.0] 区间，区间外动作真正不产生梯度，同时保留旧 rollout policy 的 PPO ratio/clip。  MoE 训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 IcePop为什么也要屏蔽非常小的训推比？ 单侧上截断只控制巨大权重，严重偏小也可能反映引擎失配，继续保留会给不可靠梯度。双侧区间选择保留可信范围，并不把区间外比值拉回边界。 例如训练概率远低于服务概率，也不能因权重小就认定没有问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-icepop-96432a79" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-72e55a56d06c1046">IcePop为什么也要屏蔽非常小的训推比？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aicepop">IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单侧上截断只控制巨大权重，严重偏小也可能反映引擎失配，继续保留会给不可靠梯度。双侧区间选择保留可信范围，并不把区间外比值拉回边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练概率远低于服务概率，也不能因权重小就认定没有问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.18855">原论文</a> · <a href="../../../../post-training/2510.18855-icepop/">实现解读</a> · <a href="#qa-72e55a56d06c1046">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:icepop" data-paper-title="IcePop" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="IcePop LLM 后训练 Ant Group 2025-10-21 MoE router 会放大训练引擎与 rollout 引擎的微小数值差异，单侧 TIS 仍可能保留严重偏小的失配 ratio。IcePop 对训练侧与 rollout 引擎的 token 概率比设置固定双侧区间；区间内保留原始校正权重，区间外 token 的本次策略梯度直接归零。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实 MoE expert routing、万亿参数模型或异步集群；本地只隔离复现固定双侧 mask 与原始区间内校正权重。在与 TIS 相同的候选策略和引擎失配模拟中采用公开实现常用的 [0.5, 5.0] 区间，区间外动作真正不产生梯度，同时保留旧 rollout policy 的 PPO ratio/clip。  MoE 训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 IcePop区间外token的更新归零，和把ratio裁到最近边界有什么不同？ 裁剪会保留边界权重下的贡献，掩码则直接放弃该token本次策略梯度。IcePop用固定双侧区间排除过大和过小的训推比，区间内仍使用原始校正权重，避免把它们全部改成一。它过滤的是失配程度，不是在判断token内容好坏。 教学例子：某token的训推比极小，单侧上截断几乎不处理它；双侧掩码会排除，而非给它补上一个最小边界权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6dd13d3913684d0d">IcePop区间外token的更新归零，和把ratio裁到最近边界有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aicepop">IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>裁剪会保留边界权重下的贡献，掩码则直接放弃该token本次策略梯度。IcePop用固定双侧区间排除过大和过小的训推比，区间内仍使用原始校正权重，避免把它们全部改成一。它过滤的是失配程度，不是在判断token内容好坏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某token的训推比极小，单侧上截断几乎不处理它；双侧掩码会排除，而非给它补上一个最小边界权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.18855">原论文</a> · <a href="../../../../post-training/2510.18855-icepop/">实现解读</a> · <a href="#qa-6dd13d3913684d0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:icepop" data-paper-title="IcePop" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="IcePop LLM 后训练 Ant Group 2025-10-21 MoE router 会放大训练引擎与 rollout 引擎的微小数值差异，单侧 TIS 仍可能保留严重偏小的失配 ratio。IcePop 对训练侧与 rollout 引擎的 token 概率比设置固定双侧区间；区间内保留原始校正权重，区间外 token 的本次策略梯度直接归零。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实 MoE expert routing、万亿参数模型或异步集群；本地只隔离复现固定双侧 mask 与原始区间内校正权重。在与 TIS 相同的候选策略和引擎失配模拟中采用公开实现常用的 [0.5, 5.0] 区间，区间外动作真正不产生梯度，同时保留旧 rollout policy 的 PPO ratio/clip。  MoE 训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 IcePop的mask与TIS截断在越界样本上有何不同？ IcePop越界项本次梯度归零，TIS对大比值截到上限后仍保留贡献；区间内IcePop使用原比值，不统一改成一。二者偏差与保留策略不同。 例如过大比值在一种方法仍有封顶权重，在另一种方法直接不参与此次更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8939bfededdaa33b">IcePop的mask与TIS截断在越界样本上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aicepop">IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>IcePop越界项本次梯度归零，TIS对大比值截到上限后仍保留贡献；区间内IcePop使用原比值，不统一改成一。二者偏差与保留策略不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如过大比值在一种方法仍有封顶权重，在另一种方法直接不参与此次更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.18855">原论文</a> · <a href="../../../../post-training/2510.18855-icepop/">实现解读</a> · <a href="#qa-8939bfededdaa33b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:icepop" data-paper-title="IcePop" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="IcePop LLM 后训练 Ant Group 2025-10-21 MoE router 会放大训练引擎与 rollout 引擎的微小数值差异，单侧 TIS 仍可能保留严重偏小的失配 ratio。IcePop 对训练侧与 rollout 引擎的 token 概率比设置固定双侧区间；区间内保留原始校正权重，区间外 token 的本次策略梯度直接归零。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实 MoE expert routing、万亿参数模型或异步集群；本地只隔离复现固定双侧 mask 与原始区间内校正权重。在与 TIS 相同的候选策略和引擎失配模拟中采用公开实现常用的 [0.5, 5.0] 区间，区间外动作真正不产生梯度，同时保留旧 rollout policy 的 PPO ratio/clip。  MoE 训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 IcePop要避免把训推比与policy比写成同一个量吗？ 需要。前者描述引擎差异，后者描述当前与采样策略差异，mask只针对规定的训推比。当前候选核未实现真实MoE路由或异步集群。 例如把新旧策略变化拿来做引擎mask，会误删正常学习导致的概率改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2ebbae817f487cec">IcePop要避免把训推比与policy比写成同一个量吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aicepop">IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需要。前者描述引擎差异，后者描述当前与采样策略差异，mask只针对规定的训推比。当前候选核未实现真实MoE路由或异步集群。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把新旧策略变化拿来做引擎mask，会误删正常学习导致的概率改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.18855">原论文</a> · <a href="../../../../post-training/2510.18855-icepop/">实现解读</a> · <a href="#qa-2ebbae817f487cec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo" data-paper-title="GPPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPPO LLM 后训练 Alibaba Group 2025-08-11 普通 PPO 在正优势高 ratio、负优势低 ratio 的越界象限直接令梯度为零，可能同时压制探索和从负样本学习。GPPO 保持 PPO 的前向 clipped objective，但通过 stop-gradient 边界权重恢复这些越界位置的反向信号。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 Klear-Reasoner 或长 CoT SFT，只复现 GPPO 的前向/反向分离机制。在 GSM8K candidate-policy 中区分 PPO 正常和越界样本，前向仍计算 clipped surrogate，反向以 clip 边界权重保留越界梯度。  梯度保留 clip LLM 后训练 策略优化：谁在采样，谁在被更新 GPPO保留的是PPO哪类原本被清零的信号？ 普通clip在正优势高比值和负优势低比值区域可能切断梯度，GPPO尝试保持相同前向数值却恢复这些反向信号，避免直接停止相关学习。 例如失败样本概率已降低很多时，仍可能需要继续学到如何远离它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gppo-ce7f50e5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f7a918e89b2d7d6b">GPPO保留的是PPO哪类原本被清零的信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo">GPPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通clip在正优势高比值和负优势低比值区域可能切断梯度，GPPO尝试保持相同前向数值却恢复这些反向信号，避免直接停止相关学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如失败样本概率已降低很多时，仍可能需要继续学到如何远离它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.07629">原论文</a> · <a href="../../../../post-training/2508.07629-gppo/">实现解读</a> · <a href="#qa-f7a918e89b2d7d6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo" data-paper-title="GPPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPPO LLM 后训练 Alibaba Group 2025-08-11 普通 PPO 在正优势高 ratio、负优势低 ratio 的越界象限直接令梯度为零，可能同时压制探索和从负样本学习。GPPO 保持 PPO 的前向 clipped objective，但通过 stop-gradient 边界权重恢复这些越界位置的反向信号。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 Klear-Reasoner 或长 CoT SFT，只复现 GPPO 的前向/反向分离机制。在 GSM8K candidate-policy 中区分 PPO 正常和越界样本，前向仍计算 clipped surrogate，反向以 clip 边界权重保留越界梯度。  梯度保留 clip LLM 后训练 策略优化：谁在采样，谁在被更新 GPPO前向仍像PPO，为什么越界token却能保留反向信号？ 前向裁剪值和反向导数可以通过stop-gradient构造分别指定。GPPO保留PPO形式的数值目标，同时用边界权重恢复原本被截平象限的更新，避免正样本探索和负样本学习同时中断。仅比较loss数值看不出差异，必须检查梯度路径。 教学例子：两个算子打印同一个裁剪后分数，但一个越界时梯度为零，另一个仍有边界加权梯度；训练行为会不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7ded4f2a343eef5f">GPPO前向仍像PPO，为什么越界token却能保留反向信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo">GPPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前向裁剪值和反向导数可以通过stop-gradient构造分别指定。GPPO保留PPO形式的数值目标，同时用边界权重恢复原本被截平象限的更新，避免正样本探索和负样本学习同时中断。仅比较loss数值看不出差异，必须检查梯度路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个算子打印同一个裁剪后分数，但一个越界时梯度为零，另一个仍有边界加权梯度；训练行为会不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.07629">原论文</a> · <a href="../../../../post-training/2508.07629-gppo/">实现解读</a> · <a href="#qa-7ded4f2a343eef5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo" data-paper-title="GPPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPPO LLM 后训练 Alibaba Group 2025-08-11 普通 PPO 在正优势高 ratio、负优势低 ratio 的越界象限直接令梯度为零，可能同时压制探索和从负样本学习。GPPO 保持 PPO 的前向 clipped objective，但通过 stop-gradient 边界权重恢复这些越界位置的反向信号。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 Klear-Reasoner 或长 CoT SFT，只复现 GPPO 的前向/反向分离机制。在 GSM8K candidate-policy 中区分 PPO 正常和越界样本，前向仍计算 clipped surrogate，反向以 clip 边界权重保留越界梯度。  梯度保留 clip LLM 后训练 策略优化：谁在采样，谁在被更新 前向损失相同为什么训练更新仍可能不同？ 自动微分图可通过stop-gradient改变导数而不改当前数值。GPPO的关键就是前反向分离，因此只比较loss日志无法判断是否实现其机制。 例如两函数当前都输出同一数，detach分支会让它们对参数的导数不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0106d720dd6e5fbf">前向损失相同为什么训练更新仍可能不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo">GPPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自动微分图可通过stop-gradient改变导数而不改当前数值。GPPO的关键就是前反向分离，因此只比较loss日志无法判断是否实现其机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两函数当前都输出同一数，detach分支会让它们对参数的导数不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.07629">原论文</a> · <a href="../../../../post-training/2508.07629-gppo/">实现解读</a> · <a href="#qa-0106d720dd6e5fbf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo" data-paper-title="GPPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPPO LLM 后训练 Alibaba Group 2025-08-11 普通 PPO 在正优势高 ratio、负优势低 ratio 的越界象限直接令梯度为零，可能同时压制探索和从负样本学习。GPPO 保持 PPO 的前向 clipped objective，但通过 stop-gradient 边界权重恢复这些越界位置的反向信号。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 Klear-Reasoner 或长 CoT SFT，只复现 GPPO 的前向/反向分离机制。在 GSM8K candidate-policy 中区分 PPO 正常和越界样本，前向仍计算 clipped surrogate，反向以 clip 边界权重保留越界梯度。  梯度保留 clip LLM 后训练 策略优化：谁在采样，谁在被更新 GPPO测试应该只断言clipped loss数值相等吗？ 不够。还需在越界优势象限检查梯度是否保留，并与普通PPO的零梯度区分；stop-gradient边界要明确。本地未训练原文长CoT模型。 例如正优势且ratio越上界的输入，是检验恢复反向路径的针对性负控。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e05efa68db424685">GPPO测试应该只断言clipped loss数值相等吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo">GPPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不够。还需在越界优势象限检查梯度是否保留，并与普通PPO的零梯度区分；stop-gradient边界要明确。本地未训练原文长CoT模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如正优势且ratio越上界的输入，是检验恢复反向路径的针对性负控。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.07629">原论文</a> · <a href="../../../../post-training/2508.07629-gppo/">实现解读</a> · <a href="#qa-e05efa68db424685">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tis" data-paper-title="TIS" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TIS LLM 后训练 University of California, San Diego 2025-08-05 混合训练框架由 rollout 引擎采样、训练引擎重算 log-prob；即使权重相同，数值精度和 kernel 差异也会让行为分布与训练分布偏离。TIS 将训练侧与 rollout 引擎概率比乘入策略梯度，并只对过大的校正权重做单侧上截断，保留小权重样本而控制重尾方差。 本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。候选动作分布替代逐 token LLM 概率，确定性引擎扰动替代真实 vLLM/FSDP 数值差异；这里只验证 TIS 权重与梯度路径，不复刻网页中的大模型训练。本地显式维护旧训练策略和带确定性数值/router 扰动的 rollout 引擎分布，以 c=2 单侧截断训推 ratio；TIS 不丢弃区间外样本，并继续保留 PPO stale-policy ratio。  训推失配校正 LLM 后训练 策略优化：谁在采样，谁在被更新 TIS为什么在权重相同的训推引擎之间仍有用？ 精度、kernel等数值差异可让采样分布与训练侧重算分布不一致。TIS用两者概率比修正策略梯度，处理的是执行实现差异而非额外任务奖励。 例如同一参数在两套计算路径下给出略不同的词概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-tis-834fa80d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-af8f5cde5a29c025">TIS为什么在权重相同的训推引擎之间仍有用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atis">TIS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>精度、kernel等数值差异可让采样分布与训练侧重算分布不一致。TIS用两者概率比修正策略梯度，处理的是执行实现差异而非额外任务奖励。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一参数在两套计算路径下给出略不同的词概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://fengyao.notion.site/off-policy-rl">原始资料</a> · <a href="../../../../post-training/web-2025-tis/">实现解读</a> · <a href="#qa-af8f5cde5a29c025">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tis" data-paper-title="TIS" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TIS LLM 后训练 University of California, San Diego 2025-08-05 混合训练框架由 rollout 引擎采样、训练引擎重算 log-prob；即使权重相同，数值精度和 kernel 差异也会让行为分布与训练分布偏离。TIS 将训练侧与 rollout 引擎概率比乘入策略梯度，并只对过大的校正权重做单侧上截断，保留小权重样本而控制重尾方差。 本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。候选动作分布替代逐 token LLM 概率，确定性引擎扰动替代真实 vLLM/FSDP 数值差异；这里只验证 TIS 权重与梯度路径，不复刻网页中的大模型训练。本地显式维护旧训练策略和带确定性数值/router 扰动的 rollout 引擎分布，以 c=2 单侧截断训推 ratio；TIS 不丢弃区间外样本，并继续保留 PPO stale-policy ratio。  训推失配校正 LLM 后训练 策略优化：谁在采样，谁在被更新 TIS为什么只上截断训练与推理概率比，而保留小权重样本？ 比率用于把rollout引擎采样校正到训练侧分布，特别大的权重会带来重尾方差，上截断限制其支配程度。小比率表示该样本在目标侧贡献较小，仍可保留相应权重。它不是PPO的新旧策略比，也不等于双侧丢弃失配token。 教学例子：一个旧引擎常采到、训练侧罕见的词应少贡献，而不是自动删除；极大的反向失配则需限制其单个样本影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-741f3036cd257055">TIS为什么只上截断训练与推理概率比，而保留小权重样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atis">TIS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>比率用于把rollout引擎采样校正到训练侧分布，特别大的权重会带来重尾方差，上截断限制其支配程度。小比率表示该样本在目标侧贡献较小，仍可保留相应权重。它不是PPO的新旧策略比，也不等于双侧丢弃失配token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个旧引擎常采到、训练侧罕见的词应少贡献，而不是自动删除；极大的反向失配则需限制其单个样本影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://fengyao.notion.site/off-policy-rl">原始资料</a> · <a href="../../../../post-training/web-2025-tis/">实现解读</a> · <a href="#qa-741f3036cd257055">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tis" data-paper-title="TIS" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TIS LLM 后训练 University of California, San Diego 2025-08-05 混合训练框架由 rollout 引擎采样、训练引擎重算 log-prob；即使权重相同，数值精度和 kernel 差异也会让行为分布与训练分布偏离。TIS 将训练侧与 rollout 引擎概率比乘入策略梯度，并只对过大的校正权重做单侧上截断，保留小权重样本而控制重尾方差。 本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。候选动作分布替代逐 token LLM 概率，确定性引擎扰动替代真实 vLLM/FSDP 数值差异；这里只验证 TIS 权重与梯度路径，不复刻网页中的大模型训练。本地显式维护旧训练策略和带确定性数值/router 扰动的 rollout 引擎分布，以 c=2 单侧截断训推 ratio；TIS 不丢弃区间外样本，并继续保留 PPO stale-policy ratio。  训推失配校正 LLM 后训练 策略优化：谁在采样，谁在被更新 TIS为什么只上截断而不像IcePop两侧丢弃？ 上截断控制重尾大权重，同时保留小权重贡献；双侧mask则会删除两种方向严重失配。两者保留策略不同，不能把TIS低权重也置零后仍称原公式。 例如很小ratio在TIS里仍有小贡献，而不是自动被判无效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-444934d9fbc8e69e">TIS为什么只上截断而不像IcePop两侧丢弃？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atis">TIS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>上截断控制重尾大权重，同时保留小权重贡献；双侧mask则会删除两种方向严重失配。两者保留策略不同，不能把TIS低权重也置零后仍称原公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如很小ratio在TIS里仍有小贡献，而不是自动被判无效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://fengyao.notion.site/off-policy-rl">原始资料</a> · <a href="../../../../post-training/web-2025-tis/">实现解读</a> · <a href="#qa-444934d9fbc8e69e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tis" data-paper-title="TIS" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TIS LLM 后训练 University of California, San Diego 2025-08-05 混合训练框架由 rollout 引擎采样、训练引擎重算 log-prob；即使权重相同，数值精度和 kernel 差异也会让行为分布与训练分布偏离。TIS 将训练侧与 rollout 引擎概率比乘入策略梯度，并只对过大的校正权重做单侧上截断，保留小权重样本而控制重尾方差。 本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。候选动作分布替代逐 token LLM 概率，确定性引擎扰动替代真实 vLLM/FSDP 数值差异；这里只验证 TIS 权重与梯度路径，不复刻网页中的大模型训练。本地显式维护旧训练策略和带确定性数值/router 扰动的 rollout 引擎分布，以 c=2 单侧截断训推 ratio；TIS 不丢弃区间外样本，并继续保留 PPO stale-policy ratio。  训推失配校正 LLM 后训练 策略优化：谁在采样，谁在被更新 TIS权重应使用哪个引擎概率作分母？ 分母是实际生成轨迹的rollout引擎概率，分子是对应训练侧概率；随后还可有独立policy ratio。当前本地用确定性扰动模拟数值差异，未测真实vLLM/FSDP。 例如把分子分母倒过来，会把应降低的样本权重反而提高。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6194fab57efb0811">TIS权重应使用哪个引擎概率作分母？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atis">TIS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分母是实际生成轨迹的rollout引擎概率，分子是对应训练侧概率；随后还可有独立policy ratio。当前本地用确定性扰动模拟数值差异，未测真实vLLM/FSDP。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把分子分母倒过来，会把应降低的样本权重反而提高。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://fengyao.notion.site/off-policy-rl">原始资料</a> · <a href="../../../../post-training/web-2025-tis/">实现解读</a> · <a href="#qa-6194fab57efb0811">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gspo" data-paper-title="GSPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GSPO LLM 后训练 Alibaba Qwen Team 2025-07-24 GRPO/PPO 常逐 token 裁剪 ratio，但 reward 在完整序列级给出；长序列中单个异常 token 会造成大量裁剪，MoE routing 变化还会放大不稳定。GSPO 对每条 response 取平均 log-ratio，再指数化为单一 sequence ratio，整条序列共享 clip 权重。 GSPO 把 token-level importance ratio 改为 response 的序列级 ratio，使优化单元与序列 reward 对齐，并降低长回答和 MoE 训练中的方差。实现了长度归一化 sequence ratio、group advantage、序列级 clip 与 reference KL；本地候选没有真实 token trajectory，也未复刻 Qwen3 MoE 的 expert routing 与集群规模。300 steps 刷新 old policy 18 次；最后一组 sequence ratio 均值/标准差为 1.0131/0.0117。  稳定序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GSPO为什么让完整响应共享一个重要性比？ 终局奖励在序列级给出，词元局部异常可能导致零散裁剪。平均词元log-ratio后形成序列比，把更新决策提升到完整响应层，减少局部比值主导。 例如一个罕见词偏移很大，不必直接决定整条长回答所有位置分别怎样被clip。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gspo-8ccc0734" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5b426bfd8e95bfd5">GSPO为什么让完整响应共享一个重要性比？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agspo">GSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局奖励在序列级给出，词元局部异常可能导致零散裁剪。平均词元log-ratio后形成序列比，把更新决策提升到完整响应层，减少局部比值主导。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个罕见词偏移很大，不必直接决定整条长回答所有位置分别怎样被clip。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.18071">原论文</a> · <a href="../../../../post-training/2507.18071-gspo/">实现解读</a> · <a href="#qa-5b426bfd8e95bfd5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gspo" data-paper-title="GSPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GSPO LLM 后训练 Alibaba Qwen Team 2025-07-24 GRPO/PPO 常逐 token 裁剪 ratio，但 reward 在完整序列级给出；长序列中单个异常 token 会造成大量裁剪，MoE routing 变化还会放大不稳定。GSPO 对每条 response 取平均 log-ratio，再指数化为单一 sequence ratio，整条序列共享 clip 权重。 GSPO 把 token-level importance ratio 改为 response 的序列级 ratio，使优化单元与序列 reward 对齐，并降低长回答和 MoE 训练中的方差。实现了长度归一化 sequence ratio、group advantage、序列级 clip 与 reference KL；本地候选没有真实 token trajectory，也未复刻 Qwen3 MoE 的 expert routing 与集群规模。300 steps 刷新 old policy 18 次；最后一组 sequence ratio 均值/标准差为 1.0131/0.0117。  稳定序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GSPO为何先平均token log-ratio再指数化，而不逐token各裁一次？ 完整回答接收一个结果奖励，逐token异常可能引发不一致裁剪。GSPO把平均log-ratio变成单个序列权重，让整条回答共享相对优势与裁剪决定。它缓和局部噪声，但改变了信用聚合粒度，也不能因此推断所有长度偏置或MoE路径差异已经消失。 教学例子：一段正确回答只有一个词的ratio异常，逐词裁剪与整段共享一个几何平均权重，会给出不同的更新分配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b968145af51dfe73">GSPO为何先平均token log-ratio再指数化，而不逐token各裁一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agspo">GSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整回答接收一个结果奖励，逐token异常可能引发不一致裁剪。GSPO把平均log-ratio变成单个序列权重，让整条回答共享相对优势与裁剪决定。它缓和局部噪声，但改变了信用聚合粒度，也不能因此推断所有长度偏置或MoE路径差异已经消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一段正确回答只有一个词的ratio异常，逐词裁剪与整段共享一个几何平均权重，会给出不同的更新分配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.18071">原论文</a> · <a href="../../../../post-training/2507.18071-gspo/">实现解读</a> · <a href="#qa-b968145af51dfe73">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gspo" data-paper-title="GSPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GSPO LLM 后训练 Alibaba Qwen Team 2025-07-24 GRPO/PPO 常逐 token 裁剪 ratio，但 reward 在完整序列级给出；长序列中单个异常 token 会造成大量裁剪，MoE routing 变化还会放大不稳定。GSPO 对每条 response 取平均 log-ratio，再指数化为单一 sequence ratio，整条序列共享 clip 权重。 GSPO 把 token-level importance ratio 改为 response 的序列级 ratio，使优化单元与序列 reward 对齐，并降低长回答和 MoE 训练中的方差。实现了长度归一化 sequence ratio、group advantage、序列级 clip 与 reference KL；本地候选没有真实 token trajectory，也未复刻 Qwen3 MoE 的 expert routing 与集群规模。300 steps 刷新 old policy 18 次；最后一组 sequence ratio 均值/标准差为 1.0131/0.0117。  稳定序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GSPO几何平均序列比与真正序列概率比相同吗？ 不相同。前者对log-ratio取长度平均，后者是求和后指数，即词元比连乘。平均改变长度尺度与目标定义，不能把它描述成只为避免溢出的同值计算。 例如重复同一个小偏移很多步，连乘会累积放大，几何平均保持平均程度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d23ce2ac81343580">GSPO几何平均序列比与真正序列概率比相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agspo">GSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不相同。前者对log-ratio取长度平均，后者是求和后指数，即词元比连乘。平均改变长度尺度与目标定义，不能把它描述成只为避免溢出的同值计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如重复同一个小偏移很多步，连乘会累积放大，几何平均保持平均程度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.18071">原论文</a> · <a href="../../../../post-training/2507.18071-gspo/">实现解读</a> · <a href="#qa-d23ce2ac81343580">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gspo" data-paper-title="GSPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GSPO LLM 后训练 Alibaba Qwen Team 2025-07-24 GRPO/PPO 常逐 token 裁剪 ratio，但 reward 在完整序列级给出；长序列中单个异常 token 会造成大量裁剪，MoE routing 变化还会放大不稳定。GSPO 对每条 response 取平均 log-ratio，再指数化为单一 sequence ratio，整条序列共享 clip 权重。 GSPO 把 token-level importance ratio 改为 response 的序列级 ratio，使优化单元与序列 reward 对齐，并降低长回答和 MoE 训练中的方差。实现了长度归一化 sequence ratio、group advantage、序列级 clip 与 reference KL；本地候选没有真实 token trajectory，也未复刻 Qwen3 MoE 的 expert routing 与集群规模。300 steps 刷新 old policy 18 次；最后一组 sequence ratio 均值/标准差为 1.0131/0.0117。  稳定序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GSPO的clip应逐token执行还是按响应执行？ 规定对每条响应的单一序列比clip，整条共享权重。有效响应mask决定长度，不能计入padding；本地候选没有真实词元轨迹，也未复刻MoE路由与集群。 例如先把各词元裁剪再取平均，通常不会得到先平均再裁剪的同一结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e9419f1e0394ebb6">GSPO的clip应逐token执行还是按响应执行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agspo">GSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规定对每条响应的单一序列比clip，整条共享权重。有效响应mask决定长度，不能计入padding；本地候选没有真实词元轨迹，也未复刻MoE路由与集群。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先把各词元裁剪再取平均，通常不会得到先平均再裁剪的同一结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.18071">原论文</a> · <a href="../../../../post-training/2507.18071-gspo/">实现解读</a> · <a href="#qa-e9419f1e0394ebb6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcr" data-paper-title="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty LLM 后训练 Massachusetts Institute of Technology 2025-07-22 普通 binary reward 只奖励答对，容易鼓励模型无差别地自信。RLCR 让模型同时输出预测与置信度，并把 bounded proper scoring rule 加入奖励，使诚实概率具有最优激励。本地基线对完整候选分布最小化多类 Brier：这里复现的是 scoring-rule 机制，不是论文的 LLM rollout、RL 训练栈或 confidence-weighted scaling；因此以机制实验而非论文结果复刻报告。 未运行论文的 LLM checkpoint 与 RL rollout，当前为 proper-scoring 机制实现。  校准奖励 Proper scoring rule LLM 后训练 策略优化：谁在采样，谁在被更新 RLCR为什么让模型同时输出预测和置信度？ 只奖励答对不能约束报出的概率是否诚实，proper scoring rule把概率与结果一起评价，让真实概率在相应假设下获得最优期望激励。 例如知道自己常错时报告中等信心，比一律宣称确定更符合校准目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rlcr-9a05e032" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0ac0af70774f8783">RLCR为什么让模型同时输出预测和置信度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcr">Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只奖励答对不能约束报出的概率是否诚实，proper scoring rule把概率与结果一起评价，让真实概率在相应假设下获得最优期望激励。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如知道自己常错时报告中等信心，比一律宣称确定更符合校准目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.16806">原论文</a> · <a href="../../../../post-training/2507.16806-rlcr/">实现解读</a> · <a href="#qa-0ac0af70774f8783">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcr" data-paper-title="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty LLM 后训练 Massachusetts Institute of Technology 2025-07-22 普通 binary reward 只奖励答对，容易鼓励模型无差别地自信。RLCR 让模型同时输出预测与置信度，并把 bounded proper scoring rule 加入奖励，使诚实概率具有最优激励。本地基线对完整候选分布最小化多类 Brier：这里复现的是 scoring-rule 机制，不是论文的 LLM rollout、RL 训练栈或 confidence-weighted scaling；因此以机制实验而非论文结果复刻报告。 未运行论文的 LLM checkpoint 与 RL rollout，当前为 proper-scoring 机制实现。  校准奖励 Proper scoring rule LLM 后训练 策略优化：谁在采样，谁在被更新 RLCR输出答案再报置信，为什么需要proper scoring rule而不是只奖励答对？ 二元正确奖励不区分恰当谨慎与盲目自信，模型即使经常出错也可能报高置信。proper评分规则把预测概率与结果共同计分，在其假设下激励诚实概率。训练与报告应分开准确性和校准；本地Brier梯度实验不是论文完整rollout强化学习。 教学例子：一个答题器对不熟悉的问题总说“完全确定”，仅按对错奖励未必纠正这句话；概率评分会让无根据自信付出代价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e491a49ab4ec08e3">RLCR输出答案再报置信，为什么需要proper scoring rule而不是只奖励答对？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcr">Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>二元正确奖励不区分恰当谨慎与盲目自信，模型即使经常出错也可能报高置信。proper评分规则把预测概率与结果共同计分，在其假设下激励诚实概率。训练与报告应分开准确性和校准；本地Brier梯度实验不是论文完整rollout强化学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个答题器对不熟悉的问题总说“完全确定”，仅按对错奖励未必纠正这句话；概率评分会让无根据自信付出代价。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.16806">原论文</a> · <a href="../../../../post-training/2507.16806-rlcr/">实现解读</a> · <a href="#qa-e491a49ab4ec08e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcr" data-paper-title="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty LLM 后训练 Massachusetts Institute of Technology 2025-07-22 普通 binary reward 只奖励答对，容易鼓励模型无差别地自信。RLCR 让模型同时输出预测与置信度，并把 bounded proper scoring rule 加入奖励，使诚实概率具有最优激励。本地基线对完整候选分布最小化多类 Brier：这里复现的是 scoring-rule 机制，不是论文的 LLM rollout、RL 训练栈或 confidence-weighted scaling；因此以机制实验而非论文结果复刻报告。 未运行论文的 LLM checkpoint 与 RL rollout，当前为 proper-scoring 机制实现。  校准奖励 Proper scoring rule LLM 后训练 策略优化：谁在采样，谁在被更新 RLCR与训练后仅显示一个confidence字段有何区别？ 字段若不进入目标就没有校准学习压力，RLCR把合适评分规则加入奖励。本地Brier与hybrid是机制实现，不能据此声称原文rollout栈已执行。 例如界面写出九成信心，不代表模型曾因信心不准受到训练惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bf73ac1980f7fa4e">RLCR与训练后仅显示一个confidence字段有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcr">Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>字段若不进入目标就没有校准学习压力，RLCR把合适评分规则加入奖励。本地Brier与hybrid是机制实现，不能据此声称原文rollout栈已执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如界面写出九成信心，不代表模型曾因信心不准受到训练惩罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.16806">原论文</a> · <a href="../../../../post-training/2507.16806-rlcr/">实现解读</a> · <a href="#qa-bf73ac1980f7fa4e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcr" data-paper-title="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty LLM 后训练 Massachusetts Institute of Technology 2025-07-22 普通 binary reward 只奖励答对，容易鼓励模型无差别地自信。RLCR 让模型同时输出预测与置信度，并把 bounded proper scoring rule 加入奖励，使诚实概率具有最优激励。本地基线对完整候选分布最小化多类 Brier：这里复现的是 scoring-rule 机制，不是论文的 LLM rollout、RL 训练栈或 confidence-weighted scaling；因此以机制实验而非论文结果复刻报告。 未运行论文的 LLM checkpoint 与 RL rollout，当前为 proper-scoring 机制实现。  校准奖励 Proper scoring rule LLM 后训练 策略优化：谁在采样，谁在被更新 本地RLCR的Brier梯度应覆盖哪些类别？ 对完整softmax候选分布与one-hot目标计算多类平方差并反传，不只针对选中类别或展示置信值。hybrid还组合CE；未运行论文检查点RL。 例如未被选中的类别仍分走概率质量，也应参与分布评分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7e79bc66d4f44aa7">本地RLCR的Brier梯度应覆盖哪些类别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcr">Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对完整softmax候选分布与one-hot目标计算多类平方差并反传，不只针对选中类别或展示置信值。hybrid还组合CE；未运行论文检查点RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如未被选中的类别仍分走概率质量，也应参与分布评分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.16806">原论文</a> · <a href="../../../../post-training/2507.16806-rlcr/">实现解读</a> · <a href="#qa-7e79bc66d4f44aa7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cispo" data-paper-title="CISPO / MiniMax-M1" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CISPO / MiniMax-M1 LLM 后训练 MiniMax 2025-06-16 固定 rollout policy 采样，token 级计算 importance ratio，只裁剪比率以保留优势方向和有效梯度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5000（+113.33%）；奖励、KL、长度和候选预算一致。  长上下文 RL LLM 后训练 策略优化：谁在采样，谁在被更新 CISPO为什么把裁剪对象放在importance weight上？ 它希望限制权重幅度却保留优势方向与有效学习信号，区别于PPO在部分越界区域通过min分支直接清零梯度。关键在冻结权重与可微logp路径的分工。 例如一个正样本权重封顶后，仍可通过logp项继续产生强化信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-cispo-73dd09ad" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ba75db1b56d9b580">CISPO为什么把裁剪对象放在importance weight上？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acispo">CISPO / MiniMax-M1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它希望限制权重幅度却保留优势方向与有效学习信号，区别于PPO在部分越界区域通过min分支直接清零梯度。关键在冻结权重与可微logp路径的分工。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个正样本权重封顶后，仍可通过logp项继续产生强化信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.13585">原论文</a> · <a href="../../../../post-training/2506.13585-cispo/">实现解读</a> · <a href="#qa-ba75db1b56d9b580">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cispo" data-paper-title="CISPO / MiniMax-M1" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CISPO / MiniMax-M1 LLM 后训练 MiniMax 2025-06-16 固定 rollout policy 采样，token 级计算 importance ratio，只裁剪比率以保留优势方向和有效梯度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5000（+113.33%）；奖励、KL、长度和候选预算一致。  长上下文 RL LLM 后训练 策略优化：谁在采样，谁在被更新 CISPO裁剪的是importance weight，为什么不像PPO那样让部分越界token直接没有梯度？ 它把裁剪后的比率当作策略梯度的权重，优势方向和log-prob更新仍被保留；PPO的min-surrogate则会在某些越界象限形成平坦区。两者即使采用相似裁剪区间，反向路径也不同。测试需要检查梯度，不能只比前向目标或把优势本身截断。 教学例子：一个负优势token已经很少出现，PPO可能不再继续压低；权重式裁剪仍可给它受限的负向学习信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ce326a3ad19568a3">CISPO裁剪的是importance weight，为什么不像PPO那样让部分越界token直接没有梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acispo">CISPO / MiniMax-M1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把裁剪后的比率当作策略梯度的权重，优势方向和log-prob更新仍被保留；PPO的min-surrogate则会在某些越界象限形成平坦区。两者即使采用相似裁剪区间，反向路径也不同。测试需要检查梯度，不能只比前向目标或把优势本身截断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个负优势token已经很少出现，PPO可能不再继续压低；权重式裁剪仍可给它受限的负向学习信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.13585">原论文</a> · <a href="../../../../post-training/2506.13585-cispo/">实现解读</a> · <a href="#qa-ce326a3ad19568a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cispo" data-paper-title="CISPO / MiniMax-M1" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CISPO / MiniMax-M1 LLM 后训练 MiniMax 2025-06-16 固定 rollout policy 采样，token 级计算 importance ratio，只裁剪比率以保留优势方向和有效梯度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5000（+113.33%）；奖励、KL、长度和候选预算一致。  长上下文 RL LLM 后训练 策略优化：谁在采样，谁在被更新 CISPO与普通PPO都出现clip，为什么不能当成同一目标？ PPO比较未裁剪和裁剪surrogate的较小值，CISPO用裁剪权重乘优势与logp。反向路径与越界行为不同，不能只检查clip上下界一致就判断等价。 例如两者前向都含一个边界值，但一个切断学习、另一个仍能更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-45e7baa94a6c0de4">CISPO与普通PPO都出现clip，为什么不能当成同一目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acispo">CISPO / MiniMax-M1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>PPO比较未裁剪和裁剪surrogate的较小值，CISPO用裁剪权重乘优势与logp。反向路径与越界行为不同，不能只检查clip上下界一致就判断等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两者前向都含一个边界值，但一个切断学习、另一个仍能更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.13585">原论文</a> · <a href="../../../../post-training/2506.13585-cispo/">实现解读</a> · <a href="#qa-45e7baa94a6c0de4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cispo" data-paper-title="CISPO / MiniMax-M1" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CISPO / MiniMax-M1 LLM 后训练 MiniMax 2025-06-16 固定 rollout policy 采样，token 级计算 importance ratio，只裁剪比率以保留优势方向和有效梯度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5000（+113.33%）；奖励、KL、长度和候选预算一致。  长上下文 RL LLM 后训练 策略优化：谁在采样，谁在被更新 CISPO的裁剪比值若直接参与反传会有什么风险？ 会引入额外权重导数，改变把校正权重用于策略梯度的目标。实现应核对固定rollout、权重及logp路径，不把本地机制通过写成MiniMax规模训练完成。 例如应由当前动作logp承担策略梯度，而非同时沿用于构造权重的支路重复求导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0a45c23f226dd11a">CISPO的裁剪比值若直接参与反传会有什么风险？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acispo">CISPO / MiniMax-M1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>会引入额外权重导数，改变把校正权重用于策略梯度的目标。实现应核对固定rollout、权重及logp路径，不把本地机制通过写成MiniMax规模训练完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如应由当前动作logp承担策略梯度，而非同时沿用于构造权重的支路重复求导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.13585">原论文</a> · <a href="../../../../post-training/2506.13585-cispo/">实现解读</a> · <a href="#qa-0a45c23f226dd11a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttrl" data-paper-title="TTRL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTRL LLM 后训练 PRIME-RL author team 2025-04-22 同一测试题多次采样，以多数一致答案作为伪标签并即时更新模型，不访问 gold label。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.2344（+0.00%）；奖励、KL、长度和候选预算一致。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTRL在无标签测试题上从哪里得到奖励？ 对同题多次采样，以多数一致答案作伪标签，再按是否一致生成奖励并在线更新。它不读取gold，但多数本身可能错，因此仍需独立评测。 例如模型几次都猜同一个错误结果，共识只能提供自监督线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ttrl-f1272098" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e13260c6de1f2d65">TTRL在无标签测试题上从哪里得到奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attrl">TTRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PRIME-RL author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对同题多次采样，以多数一致答案作伪标签，再按是否一致生成奖励并在线更新。它不读取gold，但多数本身可能错，因此仍需独立评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型几次都猜同一个错误结果，共识只能提供自监督线索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.16084">原论文</a> · <a href="../../../../post-training/2504.16084-ttrl/">实现解读</a> · <a href="#qa-e13260c6de1f2d65">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttrl" data-paper-title="TTRL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTRL LLM 后训练 PRIME-RL author team 2025-04-22 同一测试题多次采样，以多数一致答案作为伪标签并即时更新模型，不访问 gold label。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.2344（+0.00%）；奖励、KL、长度和候选预算一致。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTRL用测试题多数票作奖励，为什么必须明确它是无标签适配而非普通固定模型评测？ 测试输入被用于采样并即时更新参数，评测对象因此随过程变化。多数票提供伪标签而非gold，可能自我强化错误，所以必须报告采样与适配预算，并把隐藏答案留在独立评分侧。无标签不等于没有测试时学习，更不能与零适配结果混写。 教学例子：模型对一道新题采样多次，再按共识更新后作答；这与直接调用原模型一次不同，即使全过程没有读取标准答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c6d9c41a8ac4de24">TTRL用测试题多数票作奖励，为什么必须明确它是无标签适配而非普通固定模型评测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attrl">TTRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PRIME-RL author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>测试输入被用于采样并即时更新参数，评测对象因此随过程变化。多数票提供伪标签而非gold，可能自我强化错误，所以必须报告采样与适配预算，并把隐藏答案留在独立评分侧。无标签不等于没有测试时学习，更不能与零适配结果混写。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型对一道新题采样多次，再按共识更新后作答；这与直接调用原模型一次不同，即使全过程没有读取标准答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.16084">原论文</a> · <a href="../../../../post-training/2504.16084-ttrl/">实现解读</a> · <a href="#qa-c6d9c41a8ac4de24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttrl" data-paper-title="TTRL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTRL LLM 后训练 PRIME-RL author team 2025-04-22 同一测试题多次采样，以多数一致答案作为伪标签并即时更新模型，不访问 gold label。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.2344（+0.00%）；奖励、KL、长度和候选预算一致。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTRL与单纯多数投票推理的差别是什么？ 多数投票只汇总输出，TTRL还用该伪奖励改变模型参数，后续行为会受更新影响。计算预算和状态传递因此不同，比较时不能忽略训练成本。 例如同样抽几条回答，投票返回后结束，TTRL则还执行一次优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-de29d2e53a75bceb">TTRL与单纯多数投票推理的差别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attrl">TTRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PRIME-RL author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多数投票只汇总输出，TTRL还用该伪奖励改变模型参数，后续行为会受更新影响。计算预算和状态传递因此不同，比较时不能忽略训练成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样抽几条回答，投票返回后结束，TTRL则还执行一次优化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.16084">原论文</a> · <a href="../../../../post-training/2504.16084-ttrl/">实现解读</a> · <a href="#qa-de29d2e53a75bceb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttrl" data-paper-title="TTRL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTRL LLM 后训练 PRIME-RL author team 2025-04-22 同一测试题多次采样，以多数一致答案作为伪标签并即时更新模型，不访问 gold label。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.2344（+0.00%）；奖励、KL、长度和候选预算一致。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTRL的答案规范化能查看测试标准解吗？ 不能。等价判断与多数统计只能用允许的预测文本规则，金标用于事后评分。当前本地只验证闭环机制，未执行论文规模真实无标签rollout。 例如不能先拿正确数值过滤候选，再说多数票自主找到了伪标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-764787173229e3b9">TTRL的答案规范化能查看测试标准解吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attrl">TTRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PRIME-RL author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。等价判断与多数统计只能用允许的预测文本规则，金标用于事后评分。当前本地只验证闭环机制，未执行论文规模真实无标签rollout。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不能先拿正确数值过滤候选，再说多数票自主找到了伪标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.16084">原论文</a> · <a href="../../../../post-training/2504.16084-ttrl/">实现解读</a> · <a href="#qa-764787173229e3b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luffy" data-paper-title="LUFFY" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUFFY LLM 后训练 University of Washington 2025-04-21 把离线高质量推理与在线 rollout 放进同一 support，通过正则化 importance ratio 保留 on-policy 行为。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5312（+126.67%）；奖励、KL、长度和候选预算一致。  离策略推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUFFY为什么要同时保留离线示范与在线探索？ 高质量示范能提供学生尚难采到的路线，在线轨迹保留当前策略的探索状态；统一支持集并处理来源概率，避免只会模仿专家或只在已有行为中打转。 例如专家展示新证明思路，学生仍生成自己的尝试并接受任务反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-luffy-8fd3aff1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c299f856a9e50d38">LUFFY为什么要同时保留离线示范与在线探索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluffy">LUFFY</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高质量示范能提供学生尚难采到的路线，在线轨迹保留当前策略的探索状态；统一支持集并处理来源概率，避免只会模仿专家或只在已有行为中打转。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如专家展示新证明思路，学生仍生成自己的尝试并接受任务反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.14945">原论文</a> · <a href="../../../../post-training/2504.14945-luffy/">实现解读</a> · <a href="#qa-c299f856a9e50d38">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luffy" data-paper-title="LUFFY" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUFFY LLM 后训练 University of Washington 2025-04-21 把离线高质量推理与在线 rollout 放进同一 support，通过正则化 importance ratio 保留 on-policy 行为。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5312（+126.67%）；奖励、KL、长度和候选预算一致。  离策略推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUFFY把离线示范和在线rollout放在一起时，为什么还要关心行为分布mu？ 示范与当前策略样本来自不同分布，不能仅因共用一个batch就当成同一种on-policy数据。重要性比及正则化用于控制这种来源错配，同时保留在线探索。示范覆盖不到的状态仍需学生自己访问，且训练示范不能泄漏到最终被评估策略的输入。 教学例子：专家有一条成功推导，学生自己采到几条失败推导；混合使用时要记录每条来源，而非把专家成功记作学生采样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3e37406dcb0a268f">LUFFY把离线示范和在线rollout放在一起时，为什么还要关心行为分布mu？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluffy">LUFFY</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>示范与当前策略样本来自不同分布，不能仅因共用一个batch就当成同一种on-policy数据。重要性比及正则化用于控制这种来源错配，同时保留在线探索。示范覆盖不到的状态仍需学生自己访问，且训练示范不能泄漏到最终被评估策略的输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>专家有一条成功推导，学生自己采到几条失败推导；混合使用时要记录每条来源，而非把专家成功记作学生采样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.14945">原论文</a> · <a href="../../../../post-training/2504.14945-luffy/">实现解读</a> · <a href="#qa-3e37406dcb0a268f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luffy" data-paper-title="LUFFY" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUFFY LLM 后训练 University of Washington 2025-04-21 把离线高质量推理与在线 rollout 放进同一 support，通过正则化 importance ratio 保留 on-policy 行为。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5312（+126.67%）；奖励、KL、长度和候选预算一致。  离策略推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUFFY混合更新与把示范追加到普通GRPO组有何区别？ 外部示范来自不同采样来源，需要相应校正与正则；直接当学生采样会错设分母。方法强调统一目标中的来源关系，而非仅增加几条高分文本。 例如人工插入成功解法不能伪装成学生当前策略恰好采出的结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e45f299abee943ba">LUFFY混合更新与把示范追加到普通GRPO组有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluffy">LUFFY</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>外部示范来自不同采样来源，需要相应校正与正则；直接当学生采样会错设分母。方法强调统一目标中的来源关系，而非仅增加几条高分文本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人工插入成功解法不能伪装成学生当前策略恰好采出的结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.14945">原论文</a> · <a href="../../../../post-training/2504.14945-luffy/">实现解读</a> · <a href="#qa-e45f299abee943ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luffy" data-paper-title="LUFFY" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUFFY LLM 后训练 University of Washington 2025-04-21 把离线高质量推理与在线 rollout 放进同一 support，通过正则化 importance ratio 保留 on-policy 行为。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5312（+126.67%）；奖励、KL、长度和候选预算一致。  离策略推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUFFY里采样策略μ与参考策略ref各有什么作用？ μ描述混合样本怎样生成，ref定义KL锚点，不能混用。实现需追踪示范与在线来源，本地候选诊断不包含原论文真实文本与分布式训练。 例如数据从专家来，reference却是初始学生，二者概率没有理由相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8d4452a51f7d0b3b">LUFFY里采样策略μ与参考策略ref各有什么作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluffy">LUFFY</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>μ描述混合样本怎样生成，ref定义KL锚点，不能混用。实现需追踪示范与在线来源，本地候选诊断不包含原论文真实文本与分布式训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数据从专家来，reference却是初始学生，二者概率没有理由相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.14945">原论文</a> · <a href="../../../../post-training/2504.14945-luffy/">实现解读</a> · <a href="#qa-8d4452a51f7d0b3b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vapo" data-paper-title="VAPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="VAPO LLM 后训练 ByteDance Seed 2025-04-07 长 CoT 的 value-based PPO 易受 critic bias、异质 response 长度和稀疏奖励影响。VAPO 预训练 value model，并依 response 长度调节 actor 的 GAE/更新策略，以更稳定地进行 value-based 推理 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 critic 不是预训练 value model，候选动作与伪长度替代自由生成长 CoT。复用可训练线性 critic，按候选伪长度调节 GAE 系数，并真实更新 actor、old policy 和 critic。  Critic PPO LLM 后训练 策略优化：谁在采样，谁在被更新 VAPO为什么为长推理重新重视value critic？ 长轨迹终局奖励稀疏，critic可为各前缀提供基准，但偏差也会随长度影响优势。预训练value与长度自适应设计希望使这条价值路径更可靠。 例如解题中间步骤尚无终局反馈，价值估计可为其后续收益提供参考。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-vapo-b94393ac" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8e6b5956ce7b7a3c">VAPO为什么为长推理重新重视value critic？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avapo">VAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长轨迹终局奖励稀疏，critic可为各前缀提供基准，但偏差也会随长度影响优势。预训练value与长度自适应设计希望使这条价值路径更可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如解题中间步骤尚无终局反馈，价值估计可为其后续收益提供参考。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05118">原论文</a> · <a href="../../../../post-training/2504.05118-vapo/">实现解读</a> · <a href="#qa-8e6b5956ce7b7a3c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vapo" data-paper-title="VAPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="VAPO LLM 后训练 ByteDance Seed 2025-04-07 长 CoT 的 value-based PPO 易受 critic bias、异质 response 长度和稀疏奖励影响。VAPO 预训练 value model，并依 response 长度调节 actor 的 GAE/更新策略，以更稳定地进行 value-based 推理 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 critic 不是预训练 value model，候选动作与伪长度替代自由生成长 CoT。复用可训练线性 critic，按候选伪长度调节 GAE 系数，并真实更新 actor、old policy 和 critic。  Critic PPO LLM 后训练 策略优化：谁在采样，谁在被更新 VAPO为什么先改善critic，并让GAE与响应长度相关，而不是直接换成无critic算法？ 长推理中稀疏奖励和长度差异会放大价值估计偏差，VAPO选择修复value-based路径：预训练critic，再让优势估计与actor策略适配长度。它没有声称critic可以省略；本地小价值估计和伪长度也不能代替真实长CoT的训练与稳定性证据。 教学例子：短回答很快看到结果，长回答要延迟很久才获奖；同一优势估计参数可能给它们不同的偏差与方差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0e539b78de945446">VAPO为什么先改善critic，并让GAE与响应长度相关，而不是直接换成无critic算法？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avapo">VAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长推理中稀疏奖励和长度差异会放大价值估计偏差，VAPO选择修复value-based路径：预训练critic，再让优势估计与actor策略适配长度。它没有声称critic可以省略；本地小价值估计和伪长度也不能代替真实长CoT的训练与稳定性证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>短回答很快看到结果，长回答要延迟很久才获奖；同一优势估计参数可能给它们不同的偏差与方差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05118">原论文</a> · <a href="../../../../post-training/2504.05118-vapo/">实现解读</a> · <a href="#qa-0e539b78de945446">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vapo" data-paper-title="VAPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="VAPO LLM 后训练 ByteDance Seed 2025-04-07 长 CoT 的 value-based PPO 易受 critic bias、异质 response 长度和稀疏奖励影响。VAPO 预训练 value model，并依 response 长度调节 actor 的 GAE/更新策略，以更稳定地进行 value-based 推理 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 critic 不是预训练 value model，候选动作与伪长度替代自由生成长 CoT。复用可训练线性 critic，按候选伪长度调节 GAE 系数，并真实更新 actor、old policy 和 critic。  Critic PPO LLM 后训练 策略优化：谁在采样，谁在被更新 VAPO与critic-free GRPO主要交换了什么成本和信号？ GRPO用同题响应组相对奖励省掉value模型，VAPO承担critic训练成本获得前缀价值估计。二者误差来源不同，不能因少一个模型就判定能力更好。 例如组内全错时GRPO缺少差异，critic可能仍给估计，但也可能估错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d806ff9fba95bf37">VAPO与critic-free GRPO主要交换了什么成本和信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avapo">VAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>GRPO用同题响应组相对奖励省掉value模型，VAPO承担critic训练成本获得前缀价值估计。二者误差来源不同，不能因少一个模型就判定能力更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如组内全错时GRPO缺少差异，critic可能仍给估计，但也可能估错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05118">原论文</a> · <a href="../../../../post-training/2504.05118-vapo/">实现解读</a> · <a href="#qa-d806ff9fba95bf37">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vapo" data-paper-title="VAPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="VAPO LLM 后训练 ByteDance Seed 2025-04-07 长 CoT 的 value-based PPO 易受 critic bias、异质 response 长度和稀疏奖励影响。VAPO 预训练 value model，并依 response 长度调节 actor 的 GAE/更新策略，以更稳定地进行 value-based 推理 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 critic 不是预训练 value model，候选动作与伪长度替代自由生成长 CoT。复用可训练线性 critic，按候选伪长度调节 GAE 系数，并真实更新 actor、old policy 和 critic。  Critic PPO LLM 后训练 策略优化：谁在采样，谁在被更新 VAPO的本地critic为何不能叫预训练value model复现？ 本地候选动作和伪长度只模拟价值与长度自适应关系，并非真实长CoT前缀。GAE的λ依响应长度设定需保留，不能用固定λ替代后声称完整方法。 例如几类候选的价值表，不等于读入数千词推理前缀的神经critic。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0f259ddc6b3c4d6b">VAPO的本地critic为何不能叫预训练value model复现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avapo">VAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地候选动作和伪长度只模拟价值与长度自适应关系，并非真实长CoT前缀。GAE的λ依响应长度设定需保留，不能用固定λ替代后声称完整方法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如几类候选的价值表，不等于读入数千词推理前缀的神经critic。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05118">原论文</a> · <a href="../../../../post-training/2504.05118-vapo/">实现解读</a> · <a href="#qa-0f259ddc6b3c4d6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dr-grpo" data-paper-title="Dr. GRPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Dr. GRPO LLM 后训练 SAIL 研究团队 2025-03-26 原始 GRPO 的 response 内长度平均和组内标准差会引入长度与题目难度偏置。Dr. GRPO 移除这两个归一化项，保留中心化的组相对奖励，让每条轨迹以原始尺度参与更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选策略没有自由生成 response 长度，伪长度只用于暴露归一化差异，不等同于论文的 token-level 长 CoT 训练。在相同 GSM8K candidate-policy、步数和 seed 下真实移除组 std 与伪长度归一化，并与 GRPO 的更新统计对比。  GRPO 聚合偏置 LLM 后训练 策略优化：谁在采样，谁在被更新 Dr. GRPO为什么审查长度平均和组标准差两种归一？ 这些操作不只是数值稳定，也会改变不同长度响应和不同难度题的训练权重。移除后保留组均值中心化，让奖励差在原尺度上参与更新。 例如奖励差相同但组方差不同，标准化会让两组产生不同强度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-dr-grpo-c17c40d0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-aad7fc2a0748abfc">Dr. GRPO为什么审查长度平均和组标准差两种归一？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adr-grpo">Dr. GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · SAIL 研究团队</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这些操作不只是数值稳定，也会改变不同长度响应和不同难度题的训练权重。移除后保留组均值中心化，让奖励差在原尺度上参与更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如奖励差相同但组方差不同，标准化会让两组产生不同强度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.20783">原论文</a> · <a href="../../../../post-training/2503.20783-dr-grpo/">实现解读</a> · <a href="#qa-aad7fc2a0748abfc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dr-grpo" data-paper-title="Dr. GRPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Dr. GRPO LLM 后训练 SAIL 研究团队 2025-03-26 原始 GRPO 的 response 内长度平均和组内标准差会引入长度与题目难度偏置。Dr. GRPO 移除这两个归一化项，保留中心化的组相对奖励，让每条轨迹以原始尺度参与更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选策略没有自由生成 response 长度，伪长度只用于暴露归一化差异，不等同于论文的 token-level 长 CoT 训练。在相同 GSM8K candidate-policy、步数和 seed 下真实移除组 std 与伪长度归一化，并与 GRPO 的更新统计对比。  GRPO 聚合偏置 LLM 后训练 策略优化：谁在采样，谁在被更新 Dr. GRPO为什么同时移除组标准差和响应内长度平均？ 按组标准差会让不同难度问题因局部方差被重新加权，响应内长度平均又改变长短轨迹的相对贡献。移除两项后，保留中心化奖励并按固定口径汇总，从目标层面减少这些偏置。它不是删除所有归一化，也不保证任何任务都自动更好。 教学例子：两个问题的平均奖励差相近，但其中一个组方差极小，标准化后可能被放大；再除响应长度会叠加另一层权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-72916d57d18ee4c3">Dr. GRPO为什么同时移除组标准差和响应内长度平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adr-grpo">Dr. GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · SAIL 研究团队</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按组标准差会让不同难度问题因局部方差被重新加权，响应内长度平均又改变长短轨迹的相对贡献。移除两项后，保留中心化奖励并按固定口径汇总，从目标层面减少这些偏置。它不是删除所有归一化，也不保证任何任务都自动更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个问题的平均奖励差相近，但其中一个组方差极小，标准化后可能被放大；再除响应长度会叠加另一层权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.20783">原论文</a> · <a href="../../../../post-training/2503.20783-dr-grpo/">实现解读</a> · <a href="#qa-72916d57d18ee4c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dr-grpo" data-paper-title="Dr. GRPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Dr. GRPO LLM 后训练 SAIL 研究团队 2025-03-26 原始 GRPO 的 response 内长度平均和组内标准差会引入长度与题目难度偏置。Dr. GRPO 移除这两个归一化项，保留中心化的组相对奖励，让每条轨迹以原始尺度参与更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选策略没有自由生成 response 长度，伪长度只用于暴露归一化差异，不等同于论文的 token-level 长 CoT 训练。在相同 GSM8K candidate-policy、步数和 seed 下真实移除组 std 与伪长度归一化，并与 GRPO 的更新统计对比。  GRPO 聚合偏置 LLM 后训练 策略优化：谁在采样，谁在被更新 Dr. GRPO与GRPO在全组奖励中心化上还相同吗？ 仍减同题组均值，区别是移除规定的长度与标准差归一。不能把去标准差误写成不需要baseline，也不能擅自再用全局标准差而称目标完全相同。 例如每条仍相对组平均判断好坏，只是不再除该组波动大小。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b75da045562bf37a">Dr. GRPO与GRPO在全组奖励中心化上还相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adr-grpo">Dr. GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · SAIL 研究团队</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仍减同题组均值，区别是移除规定的长度与标准差归一。不能把去标准差误写成不需要baseline，也不能擅自再用全局标准差而称目标完全相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如每条仍相对组平均判断好坏，只是不再除该组波动大小。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.20783">原论文</a> · <a href="../../../../post-training/2503.20783-dr-grpo/">实现解读</a> · <a href="#qa-b75da045562bf37a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dr-grpo" data-paper-title="Dr. GRPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Dr. GRPO LLM 后训练 SAIL 研究团队 2025-03-26 原始 GRPO 的 response 内长度平均和组内标准差会引入长度与题目难度偏置。Dr. GRPO 移除这两个归一化项，保留中心化的组相对奖励，让每条轨迹以原始尺度参与更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选策略没有自由生成 response 长度，伪长度只用于暴露归一化差异，不等同于论文的 token-level 长 CoT 训练。在相同 GSM8K candidate-policy、步数和 seed 下真实移除组 std 与伪长度归一化，并与 GRPO 的更新统计对比。  GRPO 聚合偏置 LLM 后训练 策略优化：谁在采样，谁在被更新 本地伪长度能证明Dr. GRPO消除真实长CoT长度偏置吗？ 不能。候选策略无自由生成长度，伪长度只能暴露不同归一计算的差别。真实验证还需词元损失与长响应分布，不能把公式测试当成论文训练结果。 例如改变一个候选的模拟长度，不会产生真实生成中提前结束的行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5ba362a618993555">本地伪长度能证明Dr. GRPO消除真实长CoT长度偏置吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adr-grpo">Dr. GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · SAIL 研究团队</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。候选策略无自由生成长度，伪长度只能暴露不同归一计算的差别。真实验证还需词元损失与长响应分布，不能把公式测试当成论文训练结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如改变一个候选的模拟长度，不会产生真实生成中提前结束的行为。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.20783">原论文</a> · <a href="../../../../post-training/2503.20783-dr-grpo/">实现解读</a> · <a href="#qa-5ba362a618993555">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dapo" data-paper-title="DAPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DAPO LLM 后训练 ByteDance Seed 2025-03-18 长 CoT 的在线 RL 容易被标准对称 clip 限制探索，且全对/全错的组没有学习信号。DAPO 用 Clip-Higher 放宽概率上升、Dynamic Sampling 丢弃零方差组、token-level loss 公平处理不同长度，并对过长回答分段惩罚。 DAPO 在 GRPO 类在线训练上加入非对称裁剪、动态采样、token-level loss 与 overlong reward shaping，解决熵坍缩和无效 batch。实现四个核心训练机制和 old-policy rollout；候选长度由确定性伪 token 长度模拟，没有复刻 32B 长 CoT、分布式训练、真实 token mask 或 AIME verifier。300 steps 刷新 old policy 18 次；最后一步 low/high clip 为 0.20/0.28，clip fraction 0.25，平均伪 token 数 2.25，overlong penalty 0.0125。  长推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 DAPO为什么动态跳过全对或全错的响应组？ 二元奖励组内无方差时缺少相对优势信号，继续占用训练批会浪费有效样本位置。动态采样选择有差异组，但并没有自动解决所有失败题的探索不足。 例如四条全错难区分谁更好，需要重新采样而非把同一零信号重复优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-dapo-b7495c1f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-22a113575bc73943">DAPO为什么动态跳过全对或全错的响应组？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adapo">DAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>二元奖励组内无方差时缺少相对优势信号，继续占用训练批会浪费有效样本位置。动态采样选择有差异组，但并没有自动解决所有失败题的探索不足。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四条全错难区分谁更好，需要重新采样而非把同一零信号重复优化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.14476">原论文</a> · <a href="../../../../post-training/2503.14476-dapo/">实现解读</a> · <a href="#qa-22a113575bc73943">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dapo" data-paper-title="DAPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DAPO LLM 后训练 ByteDance Seed 2025-03-18 长 CoT 的在线 RL 容易被标准对称 clip 限制探索，且全对/全错的组没有学习信号。DAPO 用 Clip-Higher 放宽概率上升、Dynamic Sampling 丢弃零方差组、token-level loss 公平处理不同长度，并对过长回答分段惩罚。 DAPO 在 GRPO 类在线训练上加入非对称裁剪、动态采样、token-level loss 与 overlong reward shaping，解决熵坍缩和无效 batch。实现四个核心训练机制和 old-policy rollout；候选长度由确定性伪 token 长度模拟，没有复刻 32B 长 CoT、分布式训练、真实 token mask 或 AIME verifier。300 steps 刷新 old policy 18 次；最后一步 low/high clip 为 0.20/0.28，clip fraction 0.25，平均伪 token 数 2.25，overlong penalty 0.0125。  长推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 DAPO的Dynamic Sampling为什么丢弃全对组，难道正确回答不值得继续学习？ 同组全对或全错时，中心化奖励没有相对差异，继续消耗该组预算难以提供所需优势。动态采样挑选仍有区分的组；Clip-Higher、token级汇总与过长惩罚分别处理探索和长度问题。丢弃无方差组不等于判定这些回答无价值，也不允许用test挑题。 教学例子：同题所有回答奖励完全相同，再算组内相对优势仍无方向；换一组尚有成败差异的训练样本，可能更有学习信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ebd8d3555febbac3">DAPO的Dynamic Sampling为什么丢弃全对组，难道正确回答不值得继续学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adapo">DAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同组全对或全错时，中心化奖励没有相对差异，继续消耗该组预算难以提供所需优势。动态采样挑选仍有区分的组；Clip-Higher、token级汇总与过长惩罚分别处理探索和长度问题。丢弃无方差组不等于判定这些回答无价值，也不允许用test挑题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题所有回答奖励完全相同，再算组内相对优势仍无方向；换一组尚有成败差异的训练样本，可能更有学习信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.14476">原论文</a> · <a href="../../../../post-training/2503.14476-dapo/">实现解读</a> · <a href="#qa-ebd8d3555febbac3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dapo" data-paper-title="DAPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DAPO LLM 后训练 ByteDance Seed 2025-03-18 长 CoT 的在线 RL 容易被标准对称 clip 限制探索，且全对/全错的组没有学习信号。DAPO 用 Clip-Higher 放宽概率上升、Dynamic Sampling 丢弃零方差组、token-level loss 公平处理不同长度，并对过长回答分段惩罚。 DAPO 在 GRPO 类在线训练上加入非对称裁剪、动态采样、token-level loss 与 overlong reward shaping，解决熵坍缩和无效 batch。实现四个核心训练机制和 old-policy rollout；候选长度由确定性伪 token 长度模拟，没有复刻 32B 长 CoT、分布式训练、真实 token mask 或 AIME verifier。300 steps 刷新 old policy 18 次；最后一步 low/high clip 为 0.20/0.28，clip fraction 0.25，平均伪 token 数 2.25，overlong penalty 0.0125。  长推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 Clip-Higher与普通对称clip主要放宽哪侧？ 上界更宽，允许正向概率提升保留更多探索空间，下界仍单独控制。它还需与动态采样、词元损失和超长塑形共同理解，单改上界不是完整DAPO。 例如让一个有用新动作更易提高概率，并不意味着下降方向也同样放宽。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e1eb83514170cabf">Clip-Higher与普通对称clip主要放宽哪侧？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adapo">DAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>上界更宽，允许正向概率提升保留更多探索空间，下界仍单独控制。它还需与动态采样、词元损失和超长塑形共同理解，单改上界不是完整DAPO。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如让一个有用新动作更易提高概率，并不意味着下降方向也同样放宽。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.14476">原论文</a> · <a href="../../../../post-training/2503.14476-dapo/">实现解读</a> · <a href="#qa-e1eb83514170cabf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dapo" data-paper-title="DAPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DAPO LLM 后训练 ByteDance Seed 2025-03-18 长 CoT 的在线 RL 容易被标准对称 clip 限制探索，且全对/全错的组没有学习信号。DAPO 用 Clip-Higher 放宽概率上升、Dynamic Sampling 丢弃零方差组、token-level loss 公平处理不同长度，并对过长回答分段惩罚。 DAPO 在 GRPO 类在线训练上加入非对称裁剪、动态采样、token-level loss 与 overlong reward shaping，解决熵坍缩和无效 batch。实现四个核心训练机制和 old-policy rollout；候选长度由确定性伪 token 长度模拟，没有复刻 32B 长 CoT、分布式训练、真实 token mask 或 AIME verifier。300 steps 刷新 old policy 18 次；最后一步 low/high clip 为 0.20/0.28，clip fraction 0.25，平均伪 token 数 2.25，overlong penalty 0.0125。  长推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 DAPO词元级分母与逐响应均值有什么差别？ 先汇总有效响应词元再统一归一，避免每条先平均造成另一种长度权重。动态过滤与超长惩罚也需明确；本地伪长度未覆盖真实mask与32B训练。 例如长短两条先各自平均，和把全部词元放一起平均，贡献权重一般不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f25cd80adbf410cf">DAPO词元级分母与逐响应均值有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adapo">DAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先汇总有效响应词元再统一归一，避免每条先平均造成另一种长度权重。动态过滤与超长惩罚也需明确；本地伪长度未覆盖真实mask与32B训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长短两条先各自平均，和把全部词元放一起平均，贡献权重一般不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.14476">原论文</a> · <a href="../../../../post-training/2503.14476-dapo/">实现解读</a> · <a href="#qa-f25cd80adbf410cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reinforce-plus" data-paper-title="REINFORCE++" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="REINFORCE++ LLM 后训练 Independent researchers 2025-01-04 GRPO/RLOO 的 prompt-local 标准差会让不同难度组被随机方差重新加权。REINFORCE++ 保留组内中心化，但使用跨 batch 的全局优势尺度归一化，从而在不引入 critic 的前提下降低方差与局部偏置。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 EMA 是小批候选轨迹统计，不代表论文的大 batch 分布或人类偏好奖励。维护跨训练步的 reward 二阶矩，真实以它而非当前组 std 缩放 group-centered advantage。  全局优势估计 LLM 后训练 策略优化：谁在采样，谁在被更新 REINFORCE++为什么不用每个prompt自己的标准差？ 局部方差由少量采样决定，可能随机放大某些难度组。保留组内中心化、使用全局优势尺度，试图减少这种跨题重新加权，而不增加critic。 例如某题偶然只有一点奖励波动，不应因此被局部归一放得特别大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-reinforce-plus-c6bb06c9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2c36afea4bd44747">REINFORCE++为什么不用每个prompt自己的标准差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areinforce-plus">REINFORCE++</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部方差由少量采样决定，可能随机放大某些难度组。保留组内中心化、使用全局优势尺度，试图减少这种跨题重新加权，而不增加critic。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某题偶然只有一点奖励波动，不应因此被局部归一放得特别大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.03262">原论文</a> · <a href="../../../../post-training/2501.03262-reinforce-plus/">实现解读</a> · <a href="#qa-2c36afea4bd44747">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reinforce-plus" data-paper-title="REINFORCE++" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="REINFORCE++ LLM 后训练 Independent researchers 2025-01-04 GRPO/RLOO 的 prompt-local 标准差会让不同难度组被随机方差重新加权。REINFORCE++ 保留组内中心化，但使用跨 batch 的全局优势尺度归一化，从而在不引入 critic 的前提下降低方差与局部偏置。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 EMA 是小批候选轨迹统计，不代表论文的大 batch 分布或人类偏好奖励。维护跨训练步的 reward 二阶矩，真实以它而非当前组 std 缩放 group-centered advantage。  全局优势估计 LLM 后训练 策略优化：谁在采样，谁在被更新 REINFORCE++为什么保留组内中心化，却把尺度归一化放到全局？ 组内中心化消除同题共同难度，但局部标准差可能把偶然小方差组放大。跨batch的全局尺度提供更一致的更新量纲，在不增加critic的情况下减少局部重新加权。全局统计的窗口与分布也有影响，小batch EMA诊断不能当作大规模稳定性证明。 教学例子：两道题都出现一点奖励差，只有一道题的组方差特别小；统一全局尺度可避免它因偶然方差而获得异常大权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-939c465a1c7db3eb">REINFORCE++为什么保留组内中心化，却把尺度归一化放到全局？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areinforce-plus">REINFORCE++</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组内中心化消除同题共同难度，但局部标准差可能把偶然小方差组放大。跨batch的全局尺度提供更一致的更新量纲，在不增加critic的情况下减少局部重新加权。全局统计的窗口与分布也有影响，小batch EMA诊断不能当作大规模稳定性证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两道题都出现一点奖励差，只有一道题的组方差特别小；统一全局尺度可避免它因偶然方差而获得异常大权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.03262">原论文</a> · <a href="../../../../post-training/2501.03262-reinforce-plus/">实现解读</a> · <a href="#qa-939c465a1c7db3eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reinforce-plus" data-paper-title="REINFORCE++" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="REINFORCE++ LLM 后训练 Independent researchers 2025-01-04 GRPO/RLOO 的 prompt-local 标准差会让不同难度组被随机方差重新加权。REINFORCE++ 保留组内中心化，但使用跨 batch 的全局优势尺度归一化，从而在不引入 critic 的前提下降低方差与局部偏置。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 EMA 是小批候选轨迹统计，不代表论文的大 batch 分布或人类偏好奖励。维护跨训练步的 reward 二阶矩，真实以它而非当前组 std 缩放 group-centered advantage。  全局优势估计 LLM 后训练 策略优化：谁在采样，谁在被更新 全局EMA归一与组内GRPO归一为什么不是交换顺序而已？ 分母统计范围不同，组内均值仍描述同题相对表现，全局二阶量提供共享尺度。改统计范围会改变题间权重，不能仅称为相同优势的更快计算。 例如两组奖励差一样、方差不同，共享尺度与各除本组方差会产生不同结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ecef13818d1e0f7e">全局EMA归一与组内GRPO归一为什么不是交换顺序而已？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areinforce-plus">REINFORCE++</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分母统计范围不同，组内均值仍描述同题相对表现，全局二阶量提供共享尺度。改统计范围会改变题间权重，不能仅称为相同优势的更快计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两组奖励差一样、方差不同，共享尺度与各除本组方差会产生不同结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.03262">原论文</a> · <a href="../../../../post-training/2501.03262-reinforce-plus/">实现解读</a> · <a href="#qa-ecef13818d1e0f7e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reinforce-plus" data-paper-title="REINFORCE++" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="REINFORCE++ LLM 后训练 Independent researchers 2025-01-04 GRPO/RLOO 的 prompt-local 标准差会让不同难度组被随机方差重新加权。REINFORCE++ 保留组内中心化，但使用跨 batch 的全局优势尺度归一化，从而在不引入 critic 的前提下降低方差与局部偏置。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 EMA 是小批候选轨迹统计，不代表论文的大 batch 分布或人类偏好奖励。维护跨训练步的 reward 二阶矩，真实以它而非当前组 std 缩放 group-centered advantage。  全局优势估计 LLM 后训练 策略优化：谁在采样，谁在被更新 REINFORCE++的EMA状态在评估中能用金标重估吗？ 训练统计应按规定批次顺序更新并保留状态，不能用测试答案调尺度。当前小候选批EMA只验证统计与更新语义，不代表原文大batch分布。 例如把全测试集奖励先扫一遍定分母，会把评测信息带回训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9a8daf8a6d85b0f7">REINFORCE++的EMA状态在评估中能用金标重估吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areinforce-plus">REINFORCE++</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练统计应按规定批次顺序更新并保留状态，不能用测试答案调尺度。当前小候选批EMA只验证统计与更新语义，不代表原文大batch分布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把全测试集奖励先扫一遍定分母，会把评测信息带回训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.03262">原论文</a> · <a href="../../../../post-training/2501.03262-reinforce-plus/">实现解读</a> · <a href="#qa-9a8daf8a6d85b0f7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rloo" data-paper-title="RLOO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLOO LLM 后训练 Cohere For AI 2024-02-22 PPO 为一般长时域 RL 设计，价值网络、GAE 和多轮 clipping 给 LLM RLHF 带来较大显存与调参开销。RLOO 把一整段 response 视作一个 action；同一 prompt 采样多个 response，用其余样本的平均 reward 作为当前样本 baseline。 本页实现完整响应级 REINFORCE、leave-one-out baseline 与 KL-shaped reward，不引入 PPO critic。实现了 K=4 的 leave-one-out advantage、完整候选 action 和 KL shaping，且明确不创建 value model；未复刻 6.9B/7B 模型、学习到的 reward model 与论文数据规模。与 PPO-RLHF 使用完全相同的 GSM8K candidate 数据、特征、reward、steps 与 seed。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 RLOO为什么把完整response看作一个动作？ RLHF奖励常在整段回答后给出，完整动作的REINFORCE可避免学习逐前缀value网络。同题其他回答的平均回报作为baseline降低方差，但仍需要多次采样。 例如一篇摘要获得终局分数，直接用其相对回报加权整段logp。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rloo-064c4d91" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4b9c6d8a40ab7e4f">RLOO为什么把完整response看作一个动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arloo">RLOO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cohere For AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>RLHF奖励常在整段回答后给出，完整动作的REINFORCE可避免学习逐前缀value网络。同题其他回答的平均回报作为baseline降低方差，但仍需要多次采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一篇摘要获得终局分数，直接用其相对回报加权整段logp。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.14740">原论文</a> · <a href="../../../../post-training/2402.14740-rloo/">实现解读</a> · <a href="#qa-4b9c6d8a40ab7e4f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rloo" data-paper-title="RLOO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLOO LLM 后训练 Cohere For AI 2024-02-22 PPO 为一般长时域 RL 设计，价值网络、GAE 和多轮 clipping 给 LLM RLHF 带来较大显存与调参开销。RLOO 把一整段 response 视作一个 action；同一 prompt 采样多个 response，用其余样本的平均 reward 作为当前样本 baseline。 本页实现完整响应级 REINFORCE、leave-one-out baseline 与 KL-shaped reward，不引入 PPO critic。实现了 K=4 的 leave-one-out advantage、完整候选 action 和 KL shaping，且明确不创建 value model；未复刻 6.9B/7B 模型、学习到的 reward model 与论文数据规模。与 PPO-RLHF 使用完全相同的 GSM8K candidate 数据、特征、reward、steps 与 seed。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 RLOO为什么用同题其余样本的平均奖励作baseline，而把当前样本排除？ baseline用来降低方差，应避免把当前动作自己的随机奖励混入其参照。leave-one-out使用同prompt其他独立样本，整段回答当一个动作，省去value网络。仍需足够组大小与一致奖励口径；无需critic不意味着无需采样、reference约束或外部评价。 教学例子：四份独立回答中评价第一份时，用另外三份的平均表现作参照；若把自己也算入，参照会随自身奖励一起移动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8f08c5af1cc0c720">RLOO为什么用同题其余样本的平均奖励作baseline，而把当前样本排除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arloo">RLOO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cohere For AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>baseline用来降低方差，应避免把当前动作自己的随机奖励混入其参照。leave-one-out使用同prompt其他独立样本，整段回答当一个动作，省去value网络。仍需足够组大小与一致奖励口径；无需critic不意味着无需采样、reference约束或外部评价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四份独立回答中评价第一份时，用另外三份的平均表现作参照；若把自己也算入，参照会随自身奖励一起移动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.14740">原论文</a> · <a href="../../../../post-training/2402.14740-rloo/">实现解读</a> · <a href="#qa-8f08c5af1cc0c720">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rloo" data-paper-title="RLOO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLOO LLM 后训练 Cohere For AI 2024-02-22 PPO 为一般长时域 RL 设计，价值网络、GAE 和多轮 clipping 给 LLM RLHF 带来较大显存与调参开销。RLOO 把一整段 response 视作一个 action；同一 prompt 采样多个 response，用其余样本的平均 reward 作为当前样本 baseline。 本页实现完整响应级 REINFORCE、leave-one-out baseline 与 KL-shaped reward，不引入 PPO critic。实现了 K=4 的 leave-one-out advantage、完整候选 action 和 KL shaping，且明确不创建 value model；未复刻 6.9B/7B 模型、学习到的 reward model 与论文数据规模。与 PPO-RLHF 使用完全相同的 GSM8K candidate 数据、特征、reward、steps 与 seed。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 leave-one-out基线与包含自身的组均值有何差别？ LOO为当前样本排除自己，避免其奖励直接进入自身baseline；包含自身则有不同缩放和依赖结构。两者都critic-free，但不能忽略组大小后当作完全相同。 例如两条回答时，第一条的LOO基线就是第二条，不是两条平均。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7349629a82265af6">leave-one-out基线与包含自身的组均值有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arloo">RLOO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cohere For AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>LOO为当前样本排除自己，避免其奖励直接进入自身baseline；包含自身则有不同缩放和依赖结构。两者都critic-free，但不能忽略组大小后当作完全相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条回答时，第一条的LOO基线就是第二条，不是两条平均。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.14740">原论文</a> · <a href="../../../../post-training/2402.14740-rloo/">实现解读</a> · <a href="#qa-7349629a82265af6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rloo" data-paper-title="RLOO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLOO LLM 后训练 Cohere For AI 2024-02-22 PPO 为一般长时域 RL 设计，价值网络、GAE 和多轮 clipping 给 LLM RLHF 带来较大显存与调参开销。RLOO 把一整段 response 视作一个 action；同一 prompt 采样多个 response，用其余样本的平均 reward 作为当前样本 baseline。 本页实现完整响应级 REINFORCE、leave-one-out baseline 与 KL-shaped reward，不引入 PPO critic。实现了 K=4 的 leave-one-out advantage、完整候选 action 和 KL shaping，且明确不创建 value model；未复刻 6.9B/7B 模型、学习到的 reward model 与论文数据规模。与 PPO-RLHF 使用完全相同的 GSM8K candidate 数据、特征、reward、steps 与 seed。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 RLOO在K等于一时能直接执行同一公式吗？ 不能，分母K减一且没有其他样本形成基线。实现需要求足够组大小并区分KL塑形后的回报，本地K为四的完整候选不是7B生成与真实奖励模型。 例如仅生成一篇摘要时，不能把空集合平均偷偷置零后声称仍是同一LOO估计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-593dd7b298e4697f">RLOO在K等于一时能直接执行同一公式吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arloo">RLOO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cohere For AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，分母K减一且没有其他样本形成基线。实现需要求足够组大小并区分KL塑形后的回报，本地K为四的完整候选不是7B生成与真实奖励模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如仅生成一篇摘要时，不能把空集合平均偷偷置零后声称仍是同一LOO估计。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.14740">原论文</a> · <a href="../../../../post-training/2402.14740-rloo/">实现解读</a> · <a href="#qa-593dd7b298e4697f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo" data-paper-title="DeepSeekMath / GRPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DeepSeekMath / GRPO LLM 后训练 DeepSeek-AI 2024-02-05 PPO 的 value model 与 policy 同规模，数学推理 RL 训练显存昂贵。GRPO 对同一问题采样一组 response，以组内 reward 均值和标准差构造 advantage，删除 critic；策略部分仍使用 old policy ratio、clipping 与 reference KL。 最后一步诊断包含 4 个 group samples、importance ratio、clip fraction；本页实现 group-relative advantage、old-policy ratio、clipped surrogate 与 reference KL，并验证无需 critic 的在线策略更新。保留 GRPO 的在线 group sampling、critic-free advantage、ratio clipping 和 KL；本地 response 是六候选完整 action，未训练 DeepSeekMath 7B，也未复刻 120B token 预训练和自由生成数学 verifier。  在线推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRPO为什么可以去掉与policy同规模的value model？ 它用同题响应组奖励的均值与标准差估计相对优势，不学习前缀value函数。节省的是critic资源，代价是组采样和组内有区分反馈的需求。 例如同题多次尝试中好的相对其他尝试获得正优势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-grpo-679757d4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a1014e27ef04ab41">GRPO为什么可以去掉与policy同规模的value model？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo">DeepSeekMath / GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用同题响应组奖励的均值与标准差估计相对优势，不学习前缀value函数。节省的是critic资源，代价是组采样和组内有区分反馈的需求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同题多次尝试中好的相对其他尝试获得正优势。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.03300">原论文</a> · <a href="../../../../post-training/2402.03300-grpo/">实现解读</a> · <a href="#qa-a1014e27ef04ab41">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo" data-paper-title="DeepSeekMath / GRPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DeepSeekMath / GRPO LLM 后训练 DeepSeek-AI 2024-02-05 PPO 的 value model 与 policy 同规模，数学推理 RL 训练显存昂贵。GRPO 对同一问题采样一组 response，以组内 reward 均值和标准差构造 advantage，删除 critic；策略部分仍使用 old policy ratio、clipping 与 reference KL。 最后一步诊断包含 4 个 group samples、importance ratio、clip fraction；本页实现 group-relative advantage、old-policy ratio、clipped surrogate 与 reference KL，并验证无需 critic 的在线策略更新。保留 GRPO 的在线 group sampling、critic-free advantage、ratio clipping 和 KL；本地 response 是六候选完整 action，未训练 DeepSeekMath 7B，也未复刻 120B token 预训练和自由生成数学 verifier。  在线推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRPO省掉critic后，同一问题的回答组怎样提供优势，old policy与reference还各做什么？ 组内奖励的中心化与尺度化提供相对优势，代替单独训练的价值估计；old policy记录采样时分布，用于比率和裁剪，reference则提供KL锚点。三者角色不能互换，全同奖励组也不会凭空产生区分信号。本地候选动作更新不等于完整数学模型训练。 教学例子：同题几份回答有对有错，可比较彼此奖励；更换reference只改变锚定目标，不能改写这些回答当时由谁采样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-62e639b015b8e33e">GRPO省掉critic后，同一问题的回答组怎样提供优势，old policy与reference还各做什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo">DeepSeekMath / GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组内奖励的中心化与尺度化提供相对优势，代替单独训练的价值估计；old policy记录采样时分布，用于比率和裁剪，reference则提供KL锚点。三者角色不能互换，全同奖励组也不会凭空产生区分信号。本地候选动作更新不等于完整数学模型训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题几份回答有对有错，可比较彼此奖励；更换reference只改变锚定目标，不能改写这些回答当时由谁采样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.03300">原论文</a> · <a href="../../../../post-training/2402.03300-grpo/">实现解读</a> · <a href="#qa-62e639b015b8e33e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo" data-paper-title="DeepSeekMath / GRPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DeepSeekMath / GRPO LLM 后训练 DeepSeek-AI 2024-02-05 PPO 的 value model 与 policy 同规模，数学推理 RL 训练显存昂贵。GRPO 对同一问题采样一组 response，以组内 reward 均值和标准差构造 advantage，删除 critic；策略部分仍使用 old policy ratio、clipping 与 reference KL。 最后一步诊断包含 4 个 group samples、importance ratio、clip fraction；本页实现 group-relative advantage、old-policy ratio、clipped surrogate 与 reference KL，并验证无需 critic 的在线策略更新。保留 GRPO 的在线 group sampling、critic-free advantage、ratio clipping 和 KL；本地 response 是六候选完整 action，未训练 DeepSeekMath 7B，也未复刻 120B token 预训练和自由生成数学 verifier。  在线推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRPO的old policy与reference policy为什么不是同一角色？ old用于采样与近端比值，reference用于长期KL锚定；old可随训练批刷新，reference通常按独立协议固定。混用会把更新限制与偏移正则耦合。 例如一轮新采样要更新old，不意味着初始参考模型也必须随之改写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5af499f3d629e3b1">GRPO的old policy与reference policy为什么不是同一角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo">DeepSeekMath / GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>old用于采样与近端比值，reference用于长期KL锚定；old可随训练批刷新，reference通常按独立协议固定。混用会把更新限制与偏移正则耦合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一轮新采样要更新old，不意味着初始参考模型也必须随之改写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.03300">原论文</a> · <a href="../../../../post-training/2402.03300-grpo/">实现解读</a> · <a href="#qa-5af499f3d629e3b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo" data-paper-title="DeepSeekMath / GRPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DeepSeekMath / GRPO LLM 后训练 DeepSeek-AI 2024-02-05 PPO 的 value model 与 policy 同规模，数学推理 RL 训练显存昂贵。GRPO 对同一问题采样一组 response，以组内 reward 均值和标准差构造 advantage，删除 critic；策略部分仍使用 old policy ratio、clipping 与 reference KL。 最后一步诊断包含 4 个 group samples、importance ratio、clip fraction；本页实现 group-relative advantage、old-policy ratio、clipped surrogate 与 reference KL，并验证无需 critic 的在线策略更新。保留 GRPO 的在线 group sampling、critic-free advantage、ratio clipping 和 KL；本地 response 是六候选完整 action，未训练 DeepSeekMath 7B，也未复刻 120B token 预训练和自由生成数学 verifier。  在线推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRPO全组同分时优势应怎样处理？ 中心化后为零，标准差也为零，需数值保护且不得用评分器金标硬造组内差异。本地六候选完整动作验证目标，不包含DeepSeekMath自由生成训练。 例如四条都错不能按接近标准答案的程度偷偷排序，除非协议本来允许该奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ad9a955723733b8a">GRPO全组同分时优势应怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo">DeepSeekMath / GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>中心化后为零，标准差也为零，需数值保护且不得用评分器金标硬造组内差异。本地六候选完整动作验证目标，不包含DeepSeekMath自由生成训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四条都错不能按接近标准答案的程度偷偷排序，除非协议本来允许该奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.03300">原论文</a> · <a href="../../../../post-training/2402.03300-grpo/">实现解读</a> · <a href="#qa-ad9a955723733b8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:remax" data-paper-title="ReMax" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReMax LLM 后训练 香港中文大学（深圳）/ 深圳市大数据研究院 2023-10-16 ReMax 利用 LLM RLHF 的三项特征：模拟快、token 转移确定、reward 通常只在轨迹末端给出。它删除 PPO 的 value model，以当前策略 greedy decoding 的 reward 作 prompt-dependent baseline，降低 REINFORCE 方差。 本页实现 ReMax 的 sampled rollout 减 greedy rollout baseline，验证无需价值网络的低状态 RLHF 更新。实现 sampled/greedy 双 rollout 与 value-free 更新；候选策略中的 greedy baseline 与自回归 greedy decoding 同构，但没有复刻 Mistral-7B、分布式训练或显存基准，本地结果不能与 AlpacaEval 横向比较。稳定指标：classic-post-training-gsm8k-seed42.json。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 ReMax为什么使用同题greedy回答的奖励作baseline？ 它提供随问题变化的参照，无需另训练value模型。采样回答比当前贪心更好则强化、更差则抑制；贪心答案本身不一定正确。 例如抽样找到比常规首选更好的解释，差值提供正向学习信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-remax-79f8bb09" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-87b16e785b3b5268">ReMax为什么使用同题greedy回答的奖励作baseline？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aremax">ReMax</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 香港中文大学（深圳）/ 深圳市大数据研究院</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它提供随问题变化的参照，无需另训练value模型。采样回答比当前贪心更好则强化、更差则抑制；贪心答案本身不一定正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如抽样找到比常规首选更好的解释，差值提供正向学习信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.10505">原论文</a> · <a href="../../../../post-training/2310.10505-remax/">实现解读</a> · <a href="#qa-87b16e785b3b5268">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:remax" data-paper-title="ReMax" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReMax LLM 后训练 香港中文大学（深圳）/ 深圳市大数据研究院 2023-10-16 ReMax 利用 LLM RLHF 的三项特征：模拟快、token 转移确定、reward 通常只在轨迹末端给出。它删除 PPO 的 value model，以当前策略 greedy decoding 的 reward 作 prompt-dependent baseline，降低 REINFORCE 方差。 本页实现 ReMax 的 sampled rollout 减 greedy rollout baseline，验证无需价值网络的低状态 RLHF 更新。实现 sampled/greedy 双 rollout 与 value-free 更新；候选策略中的 greedy baseline 与自回归 greedy decoding 同构，但没有复刻 Mistral-7B、分布式训练或显存基准，本地结果不能与 AlpacaEval 横向比较。稳定指标：classic-post-training-gsm8k-seed42.json。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 ReMax用greedy回答奖励作baseline，会不会要求greedy答案一定正确？ 不需要。baseline只是同prompt的参照，用来降低采样更新的方差；随机回答比greedy好或差，决定相对信号。greedy也可能错，且baseline不作为独立真值标签。方法省去value模型，但仍要实际生成并评价greedy与采样两条路径的成本。 教学例子：贪心解法答错，随机解法答对时仍有正信号；如果两者都错，不能因为贪心是baseline就把它称作标准答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4c70be2bb992c727">ReMax用greedy回答奖励作baseline，会不会要求greedy答案一定正确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aremax">ReMax</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 香港中文大学（深圳）/ 深圳市大数据研究院</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不需要。baseline只是同prompt的参照，用来降低采样更新的方差；随机回答比greedy好或差，决定相对信号。greedy也可能错，且baseline不作为独立真值标签。方法省去value模型，但仍要实际生成并评价greedy与采样两条路径的成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>贪心解法答错，随机解法答对时仍有正信号；如果两者都错，不能因为贪心是baseline就把它称作标准答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.10505">原论文</a> · <a href="../../../../post-training/2310.10505-remax/">实现解读</a> · <a href="#qa-4c70be2bb992c727">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:remax" data-paper-title="ReMax" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReMax LLM 后训练 香港中文大学（深圳）/ 深圳市大数据研究院 2023-10-16 ReMax 利用 LLM RLHF 的三项特征：模拟快、token 转移确定、reward 通常只在轨迹末端给出。它删除 PPO 的 value model，以当前策略 greedy decoding 的 reward 作 prompt-dependent baseline，降低 REINFORCE 方差。 本页实现 ReMax 的 sampled rollout 减 greedy rollout baseline，验证无需价值网络的低状态 RLHF 更新。实现 sampled/greedy 双 rollout 与 value-free 更新；候选策略中的 greedy baseline 与自回归 greedy decoding 同构，但没有复刻 Mistral-7B、分布式训练或显存基准，本地结果不能与 AlpacaEval 横向比较。稳定指标：classic-post-training-gsm8k-seed42.json。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 ReMax与RLOO的baseline来源有什么不同？ ReMax另外生成贪心轨迹，RLOO用同组其他随机响应。前者依赖贪心质量与额外执行，后者依赖组采样统计，不能只比较是否critic-free。 例如两个方法都省value网络，却为基线花在不同类型的生成上。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-411e4e350882bf7e">ReMax与RLOO的baseline来源有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aremax">ReMax</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 香港中文大学（深圳）/ 深圳市大数据研究院</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ReMax另外生成贪心轨迹，RLOO用同组其他随机响应。前者依赖贪心质量与额外执行，后者依赖组采样统计，不能只比较是否critic-free。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个方法都省value网络，却为基线花在不同类型的生成上。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.10505">原论文</a> · <a href="../../../../post-training/2310.10505-remax/">实现解读</a> · <a href="#qa-411e4e350882bf7e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:remax" data-paper-title="ReMax" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReMax LLM 后训练 香港中文大学（深圳）/ 深圳市大数据研究院 2023-10-16 ReMax 利用 LLM RLHF 的三项特征：模拟快、token 转移确定、reward 通常只在轨迹末端给出。它删除 PPO 的 value model，以当前策略 greedy decoding 的 reward 作 prompt-dependent baseline，降低 REINFORCE 方差。 本页实现 ReMax 的 sampled rollout 减 greedy rollout baseline，验证无需价值网络的低状态 RLHF 更新。实现 sampled/greedy 双 rollout 与 value-free 更新；候选策略中的 greedy baseline 与自回归 greedy decoding 同构，但没有复刻 Mistral-7B、分布式训练或显存基准，本地结果不能与 AlpacaEval 横向比较。稳定指标：classic-post-training-gsm8k-seed42.json。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 ReMax训练时能把greedy baseline的奖励当可微路径吗？ 策略梯度把baseline作为固定回报参照，不应沿解码决策或奖励重新反传。贪心与随机轨迹需同题同评价协议；本地候选greedy不代表真实模型显存或延迟结果。 例如本轮改变策略时，不能同时通过离散argmax奖励支路求一个虚构梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6fba78bf3d20b0b6">ReMax训练时能把greedy baseline的奖励当可微路径吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aremax">ReMax</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 香港中文大学（深圳）/ 深圳市大数据研究院</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略梯度把baseline作为固定回报参照，不应沿解码决策或奖励重新反传。贪心与随机轨迹需同题同评价协议；本地候选greedy不代表真实模型显存或延迟结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如本轮改变策略时，不能同时通过离散argmax奖励支路求一个虚构梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.10505">原论文</a> · <a href="../../../../post-training/2310.10505-remax/">实现解读</a> · <a href="#qa-6fba78bf3d20b0b6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ppo-rlhf" data-paper-title="InstructGPT / PPO-RLHF" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="InstructGPT / PPO-RLHF LLM 后训练 OpenAI 2022-03-04 只扩大语言模型不能保证更符合用户意图。InstructGPT 建立了经典三阶段流程：先用标注员示范做 SFT，再用成对排序训练 reward model，最后用 PPO 优化策略，同时以 KL 惩罚限制策略偏离 SFT/reference model。 未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。本页实现 PPO-RLHF 的旧策略采样、clipped surrogate、独立 critic 与 KL 约束；不把候选策略实验写成 175B InstructGPT 复刻。保留 PPO 的 actor/old-policy/critic/clip/KL 更新结构，但策略是可解释的候选线性 policy，reward 来自确定性结果与过程轴；未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 InstructGPT三阶段分别引入什么监督？ 人工示范训练SFT，人工排序训练奖励模型，再用PPO优化奖励并以参考KL控制偏移。每阶段的模型和数据作用不同，单跑PPO损失不构成整条流程。 例如有示范但没有排序数据，尚不足以声称奖励模型已被训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ppo-rlhf-a0e573a8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c05e10242ad8a177">InstructGPT三阶段分别引入什么监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Appo-rlhf">InstructGPT / PPO-RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>人工示范训练SFT，人工排序训练奖励模型，再用PPO优化奖励并以参考KL控制偏移。每阶段的模型和数据作用不同，单跑PPO损失不构成整条流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如有示范但没有排序数据，尚不足以声称奖励模型已被训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2203.02155">原论文</a> · <a href="../../../../post-training/2203.02155-ppo-rlhf/">实现解读</a> · <a href="#qa-c05e10242ad8a177">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ppo-rlhf" data-paper-title="InstructGPT / PPO-RLHF" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="InstructGPT / PPO-RLHF LLM 后训练 OpenAI 2022-03-04 只扩大语言模型不能保证更符合用户意图。InstructGPT 建立了经典三阶段流程：先用标注员示范做 SFT，再用成对排序训练 reward model，最后用 PPO 优化策略，同时以 KL 惩罚限制策略偏离 SFT/reference model。 未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。本页实现 PPO-RLHF 的旧策略采样、clipped surrogate、独立 critic 与 KL 约束；不把候选策略实验写成 175B InstructGPT 复刻。保留 PPO 的 actor/old-policy/critic/clip/KL 更新结构，但策略是可解释的候选线性 policy，reward 来自确定性结果与过程轴；未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 InstructGPT流程中的reward model、critic、old policy与reference为什么不能合成一个概念？ reward model把偏好转成评分，critic估计回报以构造优势，old policy标识采样分布，reference约束相对SFT策略的漂移。它们可能有共享初始化，但训练目的与使用时点不同。只跑候选策略的actor/critic更新，并未复现人工排序、奖励模型训练或大模型RLHF。 教学例子：一份回答可被奖励模型评高分，但critic只是预测它未来能获多少回报；reference又只负责比较策略偏离程度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5003585127af1af3">InstructGPT流程中的reward model、critic、old policy与reference为什么不能合成一个概念？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Appo-rlhf">InstructGPT / PPO-RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>reward model把偏好转成评分，critic估计回报以构造优势，old policy标识采样分布，reference约束相对SFT策略的漂移。它们可能有共享初始化，但训练目的与使用时点不同。只跑候选策略的actor/critic更新，并未复现人工排序、奖励模型训练或大模型RLHF。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一份回答可被奖励模型评高分，但critic只是预测它未来能获多少回报；reference又只负责比较策略偏离程度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2203.02155">原论文</a> · <a href="../../../../post-training/2203.02155-ppo-rlhf/">实现解读</a> · <a href="#qa-5003585127af1af3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ppo-rlhf" data-paper-title="InstructGPT / PPO-RLHF" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="InstructGPT / PPO-RLHF LLM 后训练 OpenAI 2022-03-04 只扩大语言模型不能保证更符合用户意图。InstructGPT 建立了经典三阶段流程：先用标注员示范做 SFT，再用成对排序训练 reward model，最后用 PPO 优化策略，同时以 KL 惩罚限制策略偏离 SFT/reference model。 未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。本页实现 PPO-RLHF 的旧策略采样、clipped surrogate、独立 critic 与 KL 约束；不把候选策略实验写成 175B InstructGPT 复刻。保留 PPO 的 actor/old-policy/critic/clip/KL 更新结构，但策略是可解释的候选线性 policy，reward 来自确定性结果与过程轴；未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 PPO clip与reference KL都限制变化，为什么仍需区分？ clip限制相对old policy的近端更新，KL限制相对参考策略的偏移；作用基准与时间尺度不同。二者不能互相替代，也不保证奖励模型没有被利用。 例如每步都小改仍可长期离初始策略很远，近端限制不等于固定锚点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-eaf08fcf780ae999">PPO clip与reference KL都限制变化，为什么仍需区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Appo-rlhf">InstructGPT / PPO-RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>clip限制相对old policy的近端更新，KL限制相对参考策略的偏移；作用基准与时间尺度不同。二者不能互相替代，也不保证奖励模型没有被利用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如每步都小改仍可长期离初始策略很远，近端限制不等于固定锚点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2203.02155">原论文</a> · <a href="../../../../post-training/2203.02155-ppo-rlhf/">实现解读</a> · <a href="#qa-eaf08fcf780ae999">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ppo-rlhf" data-paper-title="InstructGPT / PPO-RLHF" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="InstructGPT / PPO-RLHF LLM 后训练 OpenAI 2022-03-04 只扩大语言模型不能保证更符合用户意图。InstructGPT 建立了经典三阶段流程：先用标注员示范做 SFT，再用成对排序训练 reward model，最后用 PPO 优化策略，同时以 KL 惩罚限制策略偏离 SFT/reference model。 未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。本页实现 PPO-RLHF 的旧策略采样、clipped surrogate、独立 critic 与 KL 约束；不把候选策略实验写成 175B InstructGPT 复刻。保留 PPO 的 actor/old-policy/critic/clip/KL 更新结构，但策略是可解释的候选线性 policy，reward 来自确定性结果与过程轴；未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 本地PPO-RLHF是否包含真实学习的reward model？ 没有，奖励来自确定性结果和过程轴，策略也是候选线性模型。虽有actor、old、critic、clip与KL结构，仍不能宣称训练了GPT-3或使用原文人工数据。 例如一个数值critic可验证baseline更新，不代表完整人类偏好训练栈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6f6c88f5229999b2">本地PPO-RLHF是否包含真实学习的reward model？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Appo-rlhf">InstructGPT / PPO-RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，奖励来自确定性结果和过程轴，策略也是候选线性模型。虽有actor、old、critic、clip与KL结构，仍不能宣称训练了GPT-3或使用原文人工数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个数值critic可验证baseline更新，不代表完整人类偏好训练栈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2203.02155">原论文</a> · <a href="../../../../post-training/2203.02155-ppo-rlhf/">实现解读</a> · <a href="#qa-6f6c88f5229999b2">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

在线采样、旧策略概率与当前策略更新之间，哪些量必须分开？

## 记住这一点

RL后训练先产生轨迹和奖励，再计算优势与更新目标。GRPO用同题一组回答的相对奖励替代独立critic；DAPO进一步处理裁剪、无效组和长度等训练问题。异步执行、离策略回放与训推引擎差异会改变采样分布，旧策略、当前策略和参考策略各有角色，不能把它们的概率混用。

## 一个例子

同一道题采样四个回答，奖励为0、0、1、1，组内相对优势能提供方向；若四个都错且奖励相同，仅靠标准组中心化得不到区分信号。把旧轨迹缓存下来继续训练时，当前概率仍在变化，不能连旧优势与密度比一起盲目复用。先核对目标是否需要重要性权重，以及权重对应哪个采样策略。

## 什么时候要小心

训练更稳定与任务能力更强需要不同证据。有限梯度、clip分支和概率比测试不能证明推理提升；离线样本上的低损失也不能替代真实rollout对照。涉及真实checkpoint和长轨迹的完整实验，继续服从成本与GPU证据边界，不因公式能执行而视为训练完成。

## 先读这几篇

先读GRPO，区分采样、优势、ratio和参考KL；再读DAPO，观察零方差组与训练稳定性的处理；最后读TIS，把实际采样引擎和训练引擎的概率口径纳入检查。

1. [DeepSeekMath / GRPO](../../../post-training/2402.03300-grpo/README.md) · [原论文](https://arxiv.org/abs/2402.03300)
2. [DAPO](../../../post-training/2503.14476-dapo/README.md) · [原论文](https://arxiv.org/abs/2503.14476)
3. [TIS](../../../post-training/web-2025-tis/README.md) · [原始资料](https://fengyao.notion.site/off-policy-rl)

## 自测一下

同一组回答奖励全相同，增大batch或多算几次相同的组内优势能产生新的学习方向吗？

??? note "展开参考答案"

    标准组中心化下不会自动产生区分。需要检查奖励是否过粗、问题难度是否合适、是否该重新采样或引入合规的额外信号；不能通过读取测试答案制造非零优势。任何改法都要重新核对目标和预算。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
