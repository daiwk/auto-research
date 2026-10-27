---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 奖励与信用：正确结果该奖励哪些步骤

[LLM 后训练](index.md) / 144 个问题 · 36 篇论文

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
<p class="ar-learning-status" data-learning-status role="status">144 个问题 · 36 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mart-grpo" data-paper-title="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning LLM 后训练 The University of Hong Kong 2026-10-23 一次机器人最终失败，不等于每个动作都导致失败；全轨迹负优势还会惩罚有价值的重抓和恢复尝试。MART-GRPO 用冻结事件 VLM 回看完整失败轨迹，定位最后一次未恢复错误，只保留截止该边界的失败反馈；成功轨迹、原组优势和原始 token 分母不变。论文先分析理想 stopping-time 条件下，何时删除零条件期望的后续梯度可以保持估计器期望；实际回溯 VLM 不自动满足这些理论条件。VLM 用三路同步摄像头、机器人状态、任务与帧/动作 chunk 对齐信息，报告最后一次可见且未恢复的错误起始区间； 这超过单张 A100/A30 或 Mac 的合理迭代预算，完整 actor/VLM 训练和机器人多任务评测为成本过高，不复现（审查 DONE）；诊断真实反传合成 logits，用独立概率空间 Eq.15 参考检查值与梯度、原分母、失败后缀零梯度和成功项保留；本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  策略优化 时序信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MART-GRPO为什么在失败轨迹后半段屏蔽反馈？ 最终失败不代表后续每个动作都造成失败，恢复尝试也可能有价值。回溯定位最后未恢复错误，把其后的负向信用屏蔽，保留此前相关信号；不是提前停止机器人。 例如物体掉落后尝试重抓，不应仅因终局失败就把所有恢复动作同罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-mart-grpo-1903b786" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d10e4667ff1e98b4">MART-GRPO为什么在失败轨迹后半段屏蔽反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amart-grpo">When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终失败不代表后续每个动作都造成失败，恢复尝试也可能有价值。回溯定位最后未恢复错误，把其后的负向信用屏蔽，保留此前相关信号；不是提前停止机器人。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如物体掉落后尝试重抓，不应仅因终局失败就把所有恢复动作同罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32431v1">原论文</a> · <a href="../../../../post-training/2610.32431-mart-grpo/">实现解读</a> · <a href="#qa-d10e4667ff1e98b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mart-grpo" data-paper-title="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning LLM 后训练 The University of Hong Kong 2026-10-23 一次机器人最终失败，不等于每个动作都导致失败；全轨迹负优势还会惩罚有价值的重抓和恢复尝试。MART-GRPO 用冻结事件 VLM 回看完整失败轨迹，定位最后一次未恢复错误，只保留截止该边界的失败反馈；成功轨迹、原组优势和原始 token 分母不变。论文先分析理想 stopping-time 条件下，何时删除零条件期望的后续梯度可以保持估计器期望；实际回溯 VLM 不自动满足这些理论条件。VLM 用三路同步摄像头、机器人状态、任务与帧/动作 chunk 对齐信息，报告最后一次可见且未恢复的错误起始区间； 这超过单张 A100/A30 或 Mac 的合理迭代预算，完整 actor/VLM 训练和机器人多任务评测为成本过高，不复现（审查 DONE）；诊断真实反传合成 logits，用独立概率空间 Eq.15 参考检查值与梯度、原分母、失败后缀零梯度和成功项保留；本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  策略优化 时序信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MART-GRPO屏蔽最后未恢复错误之后的惩罚，为什么不重新算组优势或有效token分母？ 它过滤的是失败反馈作用的位置，保持原始组奖励、优势和归一化才能隔离这一机制；改分母会额外放大保留前缀。轨迹先完整执行，事件模型再回溯边界，并非提前终止环境。回溯VLM也不自动满足理想停止时刻理论，必须区分经验启发与保证。 教学例子：机器人失手后做了无关停留，可屏蔽停留的负信用；但不能把剩余动作数量缩小后再把同一失败惩罚额外放大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e7694d8cca75156c">MART-GRPO屏蔽最后未恢复错误之后的惩罚，为什么不重新算组优势或有效token分母？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amart-grpo">When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它过滤的是失败反馈作用的位置，保持原始组奖励、优势和归一化才能隔离这一机制；改分母会额外放大保留前缀。轨迹先完整执行，事件模型再回溯边界，并非提前终止环境。回溯VLM也不自动满足理想停止时刻理论，必须区分经验启发与保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>机器人失手后做了无关停留，可屏蔽停留的负信用；但不能把剩余动作数量缩小后再把同一失败惩罚额外放大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32431v1">原论文</a> · <a href="../../../../post-training/2610.32431-mart-grpo/">实现解读</a> · <a href="#qa-e7694d8cca75156c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mart-grpo" data-paper-title="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning LLM 后训练 The University of Hong Kong 2026-10-23 一次机器人最终失败，不等于每个动作都导致失败；全轨迹负优势还会惩罚有价值的重抓和恢复尝试。MART-GRPO 用冻结事件 VLM 回看完整失败轨迹，定位最后一次未恢复错误，只保留截止该边界的失败反馈；成功轨迹、原组优势和原始 token 分母不变。论文先分析理想 stopping-time 条件下，何时删除零条件期望的后续梯度可以保持估计器期望；实际回溯 VLM 不自动满足这些理论条件。VLM 用三路同步摄像头、机器人状态、任务与帧/动作 chunk 对齐信息，报告最后一次可见且未恢复的错误起始区间； 这超过单张 A100/A30 或 Mac 的合理迭代预算，完整 actor/VLM 训练和机器人多任务评测为成本过高，不复现（审查 DONE）；诊断真实反传合成 logits，用独立概率空间 Eq.15 参考检查值与梯度、原分母、失败后缀零梯度和成功项保留；本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  策略优化 时序信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 回溯VLM边界与理论stopping-time条件为什么不能等同？ VLM看过未来完整轨迹，其选择通常不是只依过去的停止时间。理论无偏条件不能自动套用，因此任意事件mask不保证无偏或必然降低方差。 例如看完结局才决定哪一步重要，与执行到该步就能决定停止，是不同信息条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8ac75269276a736b">回溯VLM边界与理论stopping-time条件为什么不能等同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amart-grpo">When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>VLM看过未来完整轨迹，其选择通常不是只依过去的停止时间。理论无偏条件不能自动套用，因此任意事件mask不保证无偏或必然降低方差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如看完结局才决定哪一步重要，与执行到该步就能决定停止，是不同信息条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32431v1">原论文</a> · <a href="../../../../post-training/2610.32431-mart-grpo/">实现解读</a> · <a href="#qa-8ac75269276a736b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mart-grpo" data-paper-title="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning LLM 后训练 The University of Hong Kong 2026-10-23 一次机器人最终失败，不等于每个动作都导致失败；全轨迹负优势还会惩罚有价值的重抓和恢复尝试。MART-GRPO 用冻结事件 VLM 回看完整失败轨迹，定位最后一次未恢复错误，只保留截止该边界的失败反馈；成功轨迹、原组优势和原始 token 分母不变。论文先分析理想 stopping-time 条件下，何时删除零条件期望的后续梯度可以保持估计器期望；实际回溯 VLM 不自动满足这些理论条件。VLM 用三路同步摄像头、机器人状态、任务与帧/动作 chunk 对齐信息，报告最后一次可见且未恢复的错误起始区间； 这超过单张 A100/A30 或 Mac 的合理迭代预算，完整 actor/VLM 训练和机器人多任务评测为成本过高，不复现（审查 DONE）；诊断真实反传合成 logits，用独立概率空间 Eq.15 参考检查值与梯度、原分母、失败后缀零梯度和成功项保留；本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  策略优化 时序信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MART屏蔽后可以重算优势或按剩余token数归一吗？ 不可以。原全组优势和原始有效动作词元分母保持，mask仅作用反馈；合法区间含上端点。格式错、身份错或越界要报错，不能当语义不确定fallback。 例如删掉后半loss后再缩小分母，会额外放大剩余梯度，改变原方法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9bd0021c9f561f87">MART屏蔽后可以重算优势或按剩余token数归一吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amart-grpo">When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可以。原全组优势和原始有效动作词元分母保持，mask仅作用反馈；合法区间含上端点。格式错、身份错或越界要报错，不能当语义不确定fallback。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删掉后半loss后再缩小分母，会额外放大剩余梯度，改变原方法。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32431v1">原论文</a> · <a href="../../../../post-training/2610.32431-mart-grpo/">实现解读</a> · <a href="#qa-9bd0021c9f561f87">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mge-po" data-paper-title="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning LLM 后训练 论文未列机构（不据邮箱域名推断） 2026-10-16 GRPO会给同题、同正确性的回答相同 advantage，忽略生成的不确定性。MGE-PO 用生成时缓存的 token 熵区分回答，在成功／失败与高熵／低熵四象限上调整信用；再用在线题目熵统计安排课程，并以熵加权参考KL约束优化。原文 §4及附录B 原图建议：Figure 1 方法总览，不能把熵阈值示意图当成本地实验结果。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。无本地实现、指标或能力比较，不进入 Evolve；该终态不阻塞审查水位。成本过高，不复现（审查 DONE）。原实验硬件为2×H200 141GB，完整单次MGE-PO记录约22.6小时，另有Math-7B-Instruct约22.8小时；该计时表的base setting没有单独checkpoint标识，不能强指为8B配置。8B训练另报告624次更新、8epochs、每题8条最长20,480 token回答；Qwen2.5系列使用17,398题和约12k生成上限。附录C与D.8  RLVR 熵与训练稳定性 过程奖励与信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MGE-PO为什么在同正确性的回答间仍区分生成熵？ 终局正确性相同不代表生成过程同样确定，缓存熵为信用分配补充轨迹信息。它还用题目熵安排课程、熵权KL约束更新，不能只看单个奖励修正公式。 例如两条都失败，一条犹豫探索，另一条确信错误，训练可区别对待。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-mge-po-5743f3b7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-53cb1c4c12782d8b">MGE-PO为什么在同正确性的回答间仍区分生成熵？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amge-po">MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构（不据邮箱域名推断）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局正确性相同不代表生成过程同样确定，缓存熵为信用分配补充轨迹信息。它还用题目熵安排课程、熵权KL约束更新，不能只看单个奖励修正公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条都失败，一条犹豫探索，另一条确信错误，训练可区别对待。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23245v1">原论文</a> · <a href="../../../../post-training/2610.23245-mge-po/">实现解读</a> · <a href="#qa-53cb1c4c12782d8b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mge-po" data-paper-title="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning LLM 后训练 论文未列机构（不据邮箱域名推断） 2026-10-16 GRPO会给同题、同正确性的回答相同 advantage，忽略生成的不确定性。MGE-PO 用生成时缓存的 token 熵区分回答，在成功／失败与高熵／低熵四象限上调整信用；再用在线题目熵统计安排课程，并以熵加权参考KL约束优化。原文 §4及附录B 原图建议：Figure 1 方法总览，不能把熵阈值示意图当成本地实验结果。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。无本地实现、指标或能力比较，不进入 Evolve；该终态不阻塞审查水位。成本过高，不复现（审查 DONE）。原实验硬件为2×H200 141GB，完整单次MGE-PO记录约22.6小时，另有Math-7B-Instruct约22.8小时；该计时表的base setting没有单独checkpoint标识，不能强指为8B配置。8B训练另报告624次更新、8epochs、每题8条最长20,480 token回答；Qwen2.5系列使用17,398题和约12k生成上限。附录C与D.8  RLVR 熵与训练稳定性 过程奖励与信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MGE-PO为什么使用生成时缓存的token熵，而不在更新后重算当前策略熵来分配信用？ 信用要描述采样该回答时的不确定性，更新后重算会把策略变化混入原轨迹评价。方法结合正确性与高低熵四象限修正优势，并另有课程和KL权重。截断响应直接修正为零，也不意味着批内重新中心化后最终优势必为零，几个步骤不能混为一项。 教学例子：同一回答更新后变得更确定，不能倒过来说它采样时就毫不犹豫；信用依据应固定在原生成分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bdfc8a5d4d1b5197">MGE-PO为什么使用生成时缓存的token熵，而不在更新后重算当前策略熵来分配信用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amge-po">MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构（不据邮箱域名推断）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>信用要描述采样该回答时的不确定性，更新后重算会把策略变化混入原轨迹评价。方法结合正确性与高低熵四象限修正优势，并另有课程和KL权重。截断响应直接修正为零，也不意味着批内重新中心化后最终优势必为零，几个步骤不能混为一项。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一回答更新后变得更确定，不能倒过来说它采样时就毫不犹豫；信用依据应固定在原生成分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23245v1">原论文</a> · <a href="../../../../post-training/2610.23245-mge-po/">实现解读</a> · <a href="#qa-bdfc8a5d4d1b5197">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mge-po" data-paper-title="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning LLM 后训练 论文未列机构（不据邮箱域名推断） 2026-10-16 GRPO会给同题、同正确性的回答相同 advantage，忽略生成的不确定性。MGE-PO 用生成时缓存的 token 熵区分回答，在成功／失败与高熵／低熵四象限上调整信用；再用在线题目熵统计安排课程，并以熵加权参考KL约束优化。原文 §4及附录B 原图建议：Figure 1 方法总览，不能把熵阈值示意图当成本地实验结果。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。无本地实现、指标或能力比较，不进入 Evolve；该终态不阻塞审查水位。成本过高，不复现（审查 DONE）。原实验硬件为2×H200 141GB，完整单次MGE-PO记录约22.6小时，另有Math-7B-Instruct约22.8小时；该计时表的base setting没有单独checkpoint标识，不能强指为8B配置。8B训练另报告624次更新、8epochs、每题8条最长20,480 token回答；Qwen2.5系列使用17,398题和约12k生成上限。附录C与D.8  RLVR 熵与训练稳定性 过程奖励与信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MGE-PO四象限与只奖励低熵回答有何区别？ 修正同时结合成功或失败与高低熵，避免把自信直接当正确。简单低熵奖励会鼓励自信错误；四象限仍依赖可验证正确性，不适用于偷看评测答案。 例如低熵错误与低熵正确虽然都确定，奖励方向不应相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-63a80fb16094e7b5">MGE-PO四象限与只奖励低熵回答有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amge-po">MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构（不据邮箱域名推断）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>修正同时结合成功或失败与高低熵，避免把自信直接当正确。简单低熵奖励会鼓励自信错误；四象限仍依赖可验证正确性，不适用于偷看评测答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如低熵错误与低熵正确虽然都确定，奖励方向不应相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23245v1">原论文</a> · <a href="../../../../post-training/2610.23245-mge-po/">实现解读</a> · <a href="#qa-63a80fb16094e7b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mge-po" data-paper-title="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning LLM 后训练 论文未列机构（不据邮箱域名推断） 2026-10-16 GRPO会给同题、同正确性的回答相同 advantage，忽略生成的不确定性。MGE-PO 用生成时缓存的 token 熵区分回答，在成功／失败与高熵／低熵四象限上调整信用；再用在线题目熵统计安排课程，并以熵加权参考KL约束优化。原文 §4及附录B 原图建议：Figure 1 方法总览，不能把熵阈值示意图当成本地实验结果。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。无本地实现、指标或能力比较，不进入 Evolve；该终态不阻塞审查水位。成本过高，不复现（审查 DONE）。原实验硬件为2×H200 141GB，完整单次MGE-PO记录约22.6小时，另有Math-7B-Instruct约22.8小时；该计时表的base setting没有单独checkpoint标识，不能强指为8B配置。8B训练另报告624次更新、8epochs、每题8条最长20,480 token回答；Qwen2.5系列使用17,398题和约12k生成上限。附录C与D.8  RLVR 熵与训练稳定性 过程奖励与信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 截断响应直接修正为零，为什么最终advantage仍可能不为零？ 门控只令其直接增量为零，随后批内重新中心化会统一移动所有优势。课程还使用滞后题目EMA，不能依据未来生成选择当前题；生成熵需从采样策略缓存。 例如其他回答获得正修正，批均值变化后，未修正那条也会相对均值移动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-65e6ce7ff69955ff">截断响应直接修正为零，为什么最终advantage仍可能不为零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amge-po">MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构（不据邮箱域名推断）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>门控只令其直接增量为零，随后批内重新中心化会统一移动所有优势。课程还使用滞后题目EMA，不能依据未来生成选择当前题；生成熵需从采样策略缓存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如其他回答获得正修正，批均值变化后，未修正那条也会相对均值移动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23245v1">原论文</a> · <a href="../../../../post-training/2610.23245-mge-po/">实现解读</a> · <a href="#qa-65e6ce7ff69955ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:diverge-ideation" data-paper-title="Training Reasoning Models to Generate Diverse Scientific Ideas" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Training Reasoning Models to Generate Diverse Scientific Ideas LLM 后训练 New York University 2026-10-15 独立采样多个高分想法可能反复得到同一个方向。论文让模型在一次生成中写出整组想法，每个新想法都能看到前面写过的内容，再按整组质量和相互差异训练。每张卡包含 problem gap、core claim、method、inspiration；质量由与 gold idea 的影响力比较提供，语义距离由三个被评字段的 judge 结果等权平均。不是用字符串不同就代表科研创新。原文 §2–3 原图建议 Figure 1：训练流程； 完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。固定诊断、不可晋级、未接 Evolve。L1 CPU reward/evaluation protocol 接口，不是科学创意模型复现。不伪造 SciJudge 或语义距离；完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。CPU runner每 seed构造12组明确标为 synthetic 的 judge 观测：双顺序Boolean赢票，以及三个字段的归一化距离。它们用于检验协议，不来自 SciJudge、LLM或真实科研评价。回调接口可替换为用户明确配置的 judge；  RLHF / RLVR 多样性与科学发现 奖励与评测协议 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 DIVERGE为什么一次生成整组想法而不是独立抽样后去重？ 后续想法可看已生成内容，模型学习主动寻找不同方向，组奖励结合质量与相互差异。字符串不重复不足以说明研究创新，语义判断仍依赖评价器。 例如第二个方案针对第一个的覆盖空缺，而非换几个同义词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-diverge-ideation-5eb53208" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-eb97cf6a3bc21812">DIVERGE为什么一次生成整组想法而不是独立抽样后去重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adiverge-ideation">Training Reasoning Models to Generate Diverse Scientific Ideas</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后续想法可看已生成内容，模型学习主动寻找不同方向，组奖励结合质量与相互差异。字符串不重复不足以说明研究创新，语义判断仍依赖评价器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第二个方案针对第一个的覆盖空缺，而非换几个同义词。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22324v1">原论文</a> · <a href="../../../../post-training/2610.22324-diverge-ideation/">实现解读</a> · <a href="#qa-eb97cf6a3bc21812">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:diverge-ideation" data-paper-title="Training Reasoning Models to Generate Diverse Scientific Ideas" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Training Reasoning Models to Generate Diverse Scientific Ideas LLM 后训练 New York University 2026-10-15 独立采样多个高分想法可能反复得到同一个方向。论文让模型在一次生成中写出整组想法，每个新想法都能看到前面写过的内容，再按整组质量和相互差异训练。每张卡包含 problem gap、core claim、method、inspiration；质量由与 gold idea 的影响力比较提供，语义距离由三个被评字段的 judge 结果等权平均。不是用字符串不同就代表科研创新。原文 §2–3 原图建议 Figure 1：训练流程； 完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。固定诊断、不可晋级、未接 Evolve。L1 CPU reward/evaluation protocol 接口，不是科学创意模型复现。不伪造 SciJudge 或语义距离；完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。CPU runner每 seed构造12组明确标为 synthetic 的 judge 观测：双顺序Boolean赢票，以及三个字段的归一化距离。它们用于检验协议，不来自 SciJudge、LLM或真实科研评价。回调接口可替换为用户明确配置的 judge；  RLHF / RLVR 多样性与科学发现 奖励与评测协议 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 DIVERGE训练为何按想法生成顺序计差异，不能照评测那样重排后再算？ 训练中每个新想法看到已有前驱，最近前驱距离对应实际生成过程；事后重排会改变哪个想法先出现及其信用。评测的折扣重排指标与训练奖励是不同定义，不能互换。质量比较与语义距离还依赖独立judge，字符串不同并不证明科学创新。 教学例子：先提出方法甲，再提出甲的改写，后者应因重复少得差异信用；不能重排成一个看起来更丰富的顺序来改写训练奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-06a668f3c7600605">DIVERGE训练为何按想法生成顺序计差异，不能照评测那样重排后再算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adiverge-ideation">Training Reasoning Models to Generate Diverse Scientific Ideas</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练中每个新想法看到已有前驱，最近前驱距离对应实际生成过程；事后重排会改变哪个想法先出现及其信用。评测的折扣重排指标与训练奖励是不同定义，不能互换。质量比较与语义距离还依赖独立judge，字符串不同并不证明科学创新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先提出方法甲，再提出甲的改写，后者应因重复少得差异信用；不能重排成一个看起来更丰富的顺序来改写训练奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22324v1">原论文</a> · <a href="../../../../post-training/2610.22324-diverge-ideation/">实现解读</a> · <a href="#qa-06a668f3c7600605">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:diverge-ideation" data-paper-title="Training Reasoning Models to Generate Diverse Scientific Ideas" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Training Reasoning Models to Generate Diverse Scientific Ideas LLM 后训练 New York University 2026-10-15 独立采样多个高分想法可能反复得到同一个方向。论文让模型在一次生成中写出整组想法，每个新想法都能看到前面写过的内容，再按整组质量和相互差异训练。每张卡包含 problem gap、core claim、method、inspiration；质量由与 gold idea 的影响力比较提供，语义距离由三个被评字段的 judge 结果等权平均。不是用字符串不同就代表科研创新。原文 §2–3 原图建议 Figure 1：训练流程； 完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。固定诊断、不可晋级、未接 Evolve。L1 CPU reward/evaluation protocol 接口，不是科学创意模型复现。不伪造 SciJudge 或语义距离；完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。CPU runner每 seed构造12组明确标为 synthetic 的 judge 观测：双顺序Boolean赢票，以及三个字段的归一化距离。它们用于检验协议，不来自 SciJudge、LLM或真实科研评价。回调接口可替换为用户明确配置的 judge；  RLHF / RLVR 多样性与科学发现 奖励与评测协议 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 训练集合奖励与评测Creative Utility能直接互用吗？ 训练按生成顺序计算最近前驱距离，不重排；评测允许重排并带折扣及归一化。贪心评测只是最大CU的下界，不能把它写成严格最优或训练目标。 例如将最强想法挪到第一可改变评测值，却不是原生成顺序下的奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a1be5157fe404d78">训练集合奖励与评测Creative Utility能直接互用吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adiverge-ideation">Training Reasoning Models to Generate Diverse Scientific Ideas</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练按生成顺序计算最近前驱距离，不重排；评测允许重排并带折扣及归一化。贪心评测只是最大CU的下界，不能把它写成严格最优或训练目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如将最强想法挪到第一可改变评测值，却不是原生成顺序下的奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22324v1">原论文</a> · <a href="../../../../post-training/2610.22324-diverge-ideation/">实现解读</a> · <a href="#qa-a1be5157fe404d78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:diverge-ideation" data-paper-title="Training Reasoning Models to Generate Diverse Scientific Ideas" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Training Reasoning Models to Generate Diverse Scientific Ideas LLM 后训练 New York University 2026-10-15 独立采样多个高分想法可能反复得到同一个方向。论文让模型在一次生成中写出整组想法，每个新想法都能看到前面写过的内容，再按整组质量和相互差异训练。每张卡包含 problem gap、core claim、method、inspiration；质量由与 gold idea 的影响力比较提供，语义距离由三个被评字段的 judge 结果等权平均。不是用字符串不同就代表科研创新。原文 §2–3 原图建议 Figure 1：训练流程； 完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。固定诊断、不可晋级、未接 Evolve。L1 CPU reward/evaluation protocol 接口，不是科学创意模型复现。不伪造 SciJudge 或语义距离；完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。CPU runner每 seed构造12组明确标为 synthetic 的 judge 观测：双顺序Boolean赢票，以及三个字段的归一化距离。它们用于检验协议，不来自 SciJudge、LLM或真实科研评价。回调接口可替换为用户明确配置的 judge；  RLHF / RLVR 多样性与科学发现 奖励与评测协议 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 DIVERGE长度惩罚应统计哪些字段？ 只统计problem_gap、core_claim与method的token，不含inspiration或think，且需相应tokenizer。schema失败奖励为零且不调用judge，不能用字符数静默代替词元数。 例如引用灵感写很长，不应被算入规定三字段的长度项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-01e29eab2dc9e08a">DIVERGE长度惩罚应统计哪些字段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adiverge-ideation">Training Reasoning Models to Generate Diverse Scientific Ideas</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只统计problem_gap、core_claim与method的token，不含inspiration或think，且需相应tokenizer。schema失败奖励为零且不调用judge，不能用字符数静默代替词元数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如引用灵感写很长，不应被算入规定三字段的长度项。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22324v1">原论文</a> · <a href="../../../../post-training/2610.22324-diverge-ideation/">实现解读</a> · <a href="#qa-01e29eab2dc9e08a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:knowgpo" data-paper-title="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents LLM 后训练 Zhejiang University 2026-10-15 不同搜索轨迹即使读到了相同事实，也可能使用完全不同的 query、网页和表述，按表面观察匹配会把可比较的步骤拆散。KnowGPO 将问题所需事实拆为原子条件，训练 verifier 检查每步获得了哪些条件。状态是已验证条件的单调集合；从相同知识前态出发的动作互相比较新增知识，再与最终回答的奖励共同更新策略。原文 §3与附录A 原图建议：Figure 2 方法总览，左侧为训练知识条件构建，右侧为分组与信用；这不表示本地实现了左侧 LLM 标注流程。 完整实验成本过高，不复现（审查 DONE）；L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 Evolve 晋级。随机初始化16词表、8维因果策略，每个问题采样6条三步轨迹，前两步为搜索、最后一步为 answer。公开输入只有题目 token、自己生成的动作和外部文档 ID；私有条件表与训练 outcome 只在 actor 调用外使用。精确小环境 verifier 不是自然语言 LLM verifier，不提供真实搜索能力。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 KnowGPO为什么按已知事实集合分组？ 不同网页和query可能获得相同知识，按表面观察会拆散可比步骤。验证原子条件后用单调集合表示知识状态，让同知识起点动作比较新增事实。 例如两条搜索路径措辞不同，但已掌握同一人物与年份，可进入同类前态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-knowgpo-346974ee" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-791c6625a80c5167">KnowGPO为什么按已知事实集合分组？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aknowgpo">KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同网页和query可能获得相同知识，按表面观察会拆散可比步骤。验证原子条件后用单调集合表示知识状态，让同知识起点动作比较新增事实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条搜索路径措辞不同，但已掌握同一人物与年份，可进入同类前态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22331v1">原论文</a> · <a href="../../../../post-training/2610.22331-knowgpo/">实现解读</a> · <a href="#qa-791c6625a80c5167">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:knowgpo" data-paper-title="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents LLM 后训练 Zhejiang University 2026-10-15 不同搜索轨迹即使读到了相同事实，也可能使用完全不同的 query、网页和表述，按表面观察匹配会把可比较的步骤拆散。KnowGPO 将问题所需事实拆为原子条件，训练 verifier 检查每步获得了哪些条件。状态是已验证条件的单调集合；从相同知识前态出发的动作互相比较新增知识，再与最终回答的奖励共同更新策略。原文 §3与附录A 原图建议：Figure 2 方法总览，左侧为训练知识条件构建，右侧为分组与信用；这不表示本地实现了左侧 LLM 标注流程。 完整实验成本过高，不复现（审查 DONE）；L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 Evolve 晋级。随机初始化16词表、8维因果策略，每个问题采样6条三步轨迹，前两步为搜索、最后一步为 answer。公开输入只有题目 token、自己生成的动作和外部文档 ID；私有条件表与训练 outcome 只在 actor 调用外使用。精确小环境 verifier 不是自然语言 LLM verifier，不提供真实搜索能力。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 KnowGPO为什么按动作前的知识集合分组，不能按动作后状态分组？ 要比较从相同已知条件出发的不同动作，前态才提供共同起点；用后态分组会把动作带来的信息增益提前作为分组条件。训练verifier将事实条件单调累积，再把过程与终局优势结合，只广播到生成token，不能把隐藏条件清单交给actor。 教学例子：两次搜索从相同证据出发，一次补到关键事实、一次没有；按结果知识分组会先把它们拆开，反而无法比较动作收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-99b78cf2f318ca24">KnowGPO为什么按动作前的知识集合分组，不能按动作后状态分组？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aknowgpo">KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>要比较从相同已知条件出发的不同动作，前态才提供共同起点；用后态分组会把动作带来的信息增益提前作为分组条件。训练verifier将事实条件单调累积，再把过程与终局优势结合，只广播到生成token，不能把隐藏条件清单交给actor。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两次搜索从相同证据出发，一次补到关键事实、一次没有；按结果知识分组会先把它们拆开，反而无法比较动作收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22331v1">原论文</a> · <a href="../../../../post-training/2610.22331-knowgpo/">实现解读</a> · <a href="#qa-99b78cf2f318ca24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:knowgpo" data-paper-title="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents LLM 后训练 Zhejiang University 2026-10-15 不同搜索轨迹即使读到了相同事实，也可能使用完全不同的 query、网页和表述，按表面观察匹配会把可比较的步骤拆散。KnowGPO 将问题所需事实拆为原子条件，训练 verifier 检查每步获得了哪些条件。状态是已验证条件的单调集合；从相同知识前态出发的动作互相比较新增知识，再与最终回答的奖励共同更新策略。原文 §3与附录A 原图建议：Figure 2 方法总览，左侧为训练知识条件构建，右侧为分组与信用；这不表示本地实现了左侧 LLM 标注流程。 完整实验成本过高，不复现（审查 DONE）；L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 Evolve 晋级。随机初始化16词表、8维因果策略，每个问题采样6条三步轨迹，前两步为搜索、最后一步为 answer。公开输入只有题目 token、自己生成的动作和外部文档 ID；私有条件表与训练 outcome 只在 actor 调用外使用。精确小环境 verifier 不是自然语言 LLM verifier，不提供真实搜索能力。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 知识状态分组与按动作后结果分组为何不同？ 过程信用要比较从同起点做不同动作的收益，按后状态分组会把获得不同新知识的动作拆开。原文歧义以算法前态为准，不可用后态图省事。 例如一个动作找到新事实、另一个没找到，恰应在相同前态下比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6a9ae4caad7bf46a">知识状态分组与按动作后结果分组为何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aknowgpo">KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>过程信用要比较从同起点做不同动作的收益，按后状态分组会把获得不同新知识的动作拆开。原文歧义以算法前态为准，不可用后态图省事。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个动作找到新事实、另一个没找到，恰应在相同前态下比较。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22331v1">原论文</a> · <a href="../../../../post-training/2610.22331-knowgpo/">实现解读</a> · <a href="#qa-6a9ae4caad7bf46a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:knowgpo" data-paper-title="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents LLM 后训练 Zhejiang University 2026-10-15 不同搜索轨迹即使读到了相同事实，也可能使用完全不同的 query、网页和表述，按表面观察匹配会把可比较的步骤拆散。KnowGPO 将问题所需事实拆为原子条件，训练 verifier 检查每步获得了哪些条件。状态是已验证条件的单调集合；从相同知识前态出发的动作互相比较新增知识，再与最终回答的奖励共同更新策略。原文 §3与附录A 原图建议：Figure 2 方法总览，左侧为训练知识条件构建，右侧为分组与信用；这不表示本地实现了左侧 LLM 标注流程。 完整实验成本过高，不复现（审查 DONE）；L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 Evolve 晋级。随机初始化16词表、8维因果策略，每个问题采样6条三步轨迹，前两步为搜索、最后一步为 answer。公开输入只有题目 token、自己生成的动作和外部文档 ID；私有条件表与训练 outcome 只在 actor 调用外使用。精确小环境 verifier 不是自然语言 LLM verifier，不提供真实搜索能力。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 KnowGPO的answer步骤和工具观察怎样处理loss？ answer不进过程分组，但仍接收混合中的终局项；优势只广播到生成推理与动作token。训练verifier信息和工具观察不可作为actor标签，singleton过程优势为零。 例如搜索返回正文是环境给的，不应被当模型生成文本计算策略梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6360eec115845831">KnowGPO的answer步骤和工具观察怎样处理loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aknowgpo">KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>answer不进过程分组，但仍接收混合中的终局项；优势只广播到生成推理与动作token。训练verifier信息和工具观察不可作为actor标签，singleton过程优势为零。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索返回正文是环境给的，不应被当模型生成文本计算策略梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22331v1">原论文</a> · <a href="../../../../post-training/2610.22331-knowgpo/">实现解读</a> · <a href="#qa-6360eec115845831">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mrtpo" data-paper-title="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL LLM 后训练 University of Minnesota 2026-10-15 GDPO 虽然分别归一化多种奖励，但仍把每种奖励均摊到整条响应。SQL 可执行性、格式、执行结果可能只分别依赖少数 token。MRTPO 用采样时的冻结策略重放响应：先提供所有 verifier 信息，再逐个删除奖励信息块。某个块被移除后，哪些位置的预测变化更大，就把该奖励更多地分配给哪些位置；正负 advantage 都使用相同的相关性权重。原文 §4 原文关键图：Figure 1/3 展示格式、可执行性和执行错误分别影响的 SQL token；见方法与图注。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机初始化32词表策略真实生成响应，两种人工 verifier 只产生 token 条件奖励。冻结快照在完整信息和两个留一上下文下重新评分相同响应前缀；学生原始采样、更新评分均不接收 verifier 块。每个 seed 默认3次真实梯度更新，不使用 SQL、BFCL 或预训练 LLM。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MRTPO为什么不把每维奖励均匀广播整条响应？ 格式、可执行性和结果可能依赖不同位置，均摊会把信用分给无关词元。删去一块奖励信息后分布变化，可作为该奖励与各位置关联的线索。 例如SQL语法错误和数值结果错误，可能指向不同关键token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-mrtpo-6e178dc9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-82c09b1f0f2ccc05">MRTPO为什么不把每维奖励均匀广播整条响应？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amrtpo">Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Minnesota</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>格式、可执行性和结果可能依赖不同位置，均摊会把信用分给无关词元。删去一块奖励信息后分布变化，可作为该奖励与各位置关联的线索。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如SQL语法错误和数值结果错误，可能指向不同关键token。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21439v1">原论文</a> · <a href="../../../../post-training/2610.21439-mrtpo/">实现解读</a> · <a href="#qa-82c09b1f0f2ccc05">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mrtpo" data-paper-title="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL LLM 后训练 University of Minnesota 2026-10-15 GDPO 虽然分别归一化多种奖励，但仍把每种奖励均摊到整条响应。SQL 可执行性、格式、执行结果可能只分别依赖少数 token。MRTPO 用采样时的冻结策略重放响应：先提供所有 verifier 信息，再逐个删除奖励信息块。某个块被移除后，哪些位置的预测变化更大，就把该奖励更多地分配给哪些位置；正负 advantage 都使用相同的相关性权重。原文 §4 原文关键图：Figure 1/3 展示格式、可执行性和执行错误分别影响的 SQL token；见方法与图注。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机初始化32词表策略真实生成响应，两种人工 verifier 只产生 token 条件奖励。冻结快照在完整信息和两个留一上下文下重新评分相同响应前缀；学生原始采样、更新评分均不接收 verifier 块。每个 seed 默认3次真实梯度更新，不使用 SQL、BFCL 或预训练 LLM。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MRTPO逐个删除奖励信息块重放响应，为什么比较的是全词表JS而非采样token概率差？ 单个已采样词的变化可能漏掉其他候选之间的重分配，全词表差异更完整地表示某类奖励信息影响哪些位置。相关性权重在响应内保均值，正负信用都按相同规则分配，并限制重分配幅度。verifier信息只供训练重放，不能泄漏到学生原始采样。 教学例子：删除SQL格式反馈后，模型可能把概率从逗号转到括号，采样出的词概率恰好不变；只看该词会漏掉真实分布变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ff72edc10ba95a02">MRTPO逐个删除奖励信息块重放响应，为什么比较的是全词表JS而非采样token概率差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amrtpo">Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Minnesota</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个已采样词的变化可能漏掉其他候选之间的重分配，全词表差异更完整地表示某类奖励信息影响哪些位置。相关性权重在响应内保均值，正负信用都按相同规则分配，并限制重分配幅度。verifier信息只供训练重放，不能泄漏到学生原始采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>删除SQL格式反馈后，模型可能把概率从逗号转到括号，采样出的词概率恰好不变；只看该词会漏掉真实分布变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21439v1">原论文</a> · <a href="../../../../post-training/2610.21439-mrtpo/">实现解读</a> · <a href="#qa-ff72edc10ba95a02">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mrtpo" data-paper-title="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL LLM 后训练 University of Minnesota 2026-10-15 GDPO 虽然分别归一化多种奖励，但仍把每种奖励均摊到整条响应。SQL 可执行性、格式、执行结果可能只分别依赖少数 token。MRTPO 用采样时的冻结策略重放响应：先提供所有 verifier 信息，再逐个删除奖励信息块。某个块被移除后，哪些位置的预测变化更大，就把该奖励更多地分配给哪些位置；正负 advantage 都使用相同的相关性权重。原文 §4 原文关键图：Figure 1/3 展示格式、可执行性和执行错误分别影响的 SQL token；见方法与图注。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机初始化32词表策略真实生成响应，两种人工 verifier 只产生 token 条件奖励。冻结快照在完整信息和两个留一上下文下重新评分相同响应前缀；学生原始采样、更新评分均不接收 verifier 块。每个 seed 默认3次真实梯度更新，不使用 SQL、BFCL 或预训练 LLM。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MRTPO信息留一与直接看采样token概率差有何区别？ 规定使用同一冻结策略的全词表JS距离，捕捉整份条件分布变化；单个采样词只是局部值。相关性仍非因果正确性证明，奖励信息不能进入学生原始采样。 例如被采到的词概率不变，其他候选大幅重排仍可能使JS非零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4141e1fd3e3b3403">MRTPO信息留一与直接看采样token概率差有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amrtpo">Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Minnesota</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规定使用同一冻结策略的全词表JS距离，捕捉整份条件分布变化；单个采样词只是局部值。相关性仍非因果正确性证明，奖励信息不能进入学生原始采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如被采到的词概率不变，其他候选大幅重排仍可能使JS非零。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21439v1">原论文</a> · <a href="../../../../post-training/2610.21439-mrtpo/">实现解读</a> · <a href="#qa-4141e1fd3e3b3403">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mrtpo" data-paper-title="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL LLM 后训练 University of Minnesota 2026-10-15 GDPO 虽然分别归一化多种奖励，但仍把每种奖励均摊到整条响应。SQL 可执行性、格式、执行结果可能只分别依赖少数 token。MRTPO 用采样时的冻结策略重放响应：先提供所有 verifier 信息，再逐个删除奖励信息块。某个块被移除后，哪些位置的预测变化更大，就把该奖励更多地分配给哪些位置；正负 advantage 都使用相同的相关性权重。原文 §4 原文关键图：Figure 1/3 展示格式、可执行性和执行错误分别影响的 SQL token；见方法与图注。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机初始化32词表策略真实生成响应，两种人工 verifier 只产生 token 条件奖励。冻结快照在完整信息和两个留一上下文下重新评分相同响应前缀；学生原始采样、更新评分均不接收 verifier 块。每个 seed 默认3次真实梯度更新，不使用 SQL、BFCL 或预训练 LLM。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MRTPO相关性全零时为什么回退权重一而非全零？ 无信息或全零差异时无法定位，均匀权重保留原奖励总信用；每响应均值为一，再做二阶矩限制和batch归一。直接置零会删除该奖励，而非重分配。 例如格式块空白时，不应因不能定位就让整项格式优势消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7288bd2955058951">MRTPO相关性全零时为什么回退权重一而非全零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amrtpo">Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Minnesota</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>无信息或全零差异时无法定位，均匀权重保留原奖励总信用；每响应均值为一，再做二阶矩限制和batch归一。直接置零会删除该奖励，而非重分配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如格式块空白时，不应因不能定位就让整项格式优势消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21439v1">原论文</a> · <a href="../../../../post-training/2610.21439-mrtpo/">实现解读</a> · <a href="#qa-7288bd2955058951">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcredit" data-paper-title="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering LLM 后训练 Nanjing University 2026-10-15 整条轨迹失败不代表每一步都无用，成功轨迹也可能绕路。OpCredit 的 BOC 从普通 rollout 中复用分支结果：同题、同活动实体，再匹配访问集合、剩余预算和决策阶段；FTC 则衡量该操作局部前沿相对答案邻域的进退。两种信用对齐同一段推理及可执行操作 token，不给工具观察记策略损失。原文 §3、附录D 原文完整实验成本过高，不复现（审查 DONE）；这些是公式及梯度诊断，不是 KGQA 能力比较。L1 信用分配与梯度组件，不是 CWQ/WebQSP/GrailQA 能力复现。原文完整实验成本过高，不复现（审查 DONE）；本地 gold 只供训练后信用计算，不进入 Actor 输入或 evolve 晋级。随机初始化4输入、3输出的小策略在两个固定微型图上，每题真实采样6条关系选择＋答案动作轨迹。gold 仅在 rollout 结束后计算终止奖励与邻域信用；公开状态白名单只有题目、活动实体、访问集合、预算、阶段和可见实体，不能传 gold 字段。  Agentic RL 操作级信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 OpCredit为什么把知识图谱搜索信用分到具体操作？ 轨迹成功可能绕路，失败也可能包含有用探索。分支结果信用与局部前沿进退分别评价操作，再对齐推理和执行token，而不是把工具观察当策略输出训练。 例如一次扩展发现关键实体，即使最终答错，也可能有正向过程价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-opcredit-fae57ef0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-467f3a76765e0009">OpCredit为什么把知识图谱搜索信用分到具体操作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopcredit">OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轨迹成功可能绕路，失败也可能包含有用探索。分支结果信用与局部前沿进退分别评价操作，再对齐推理和执行token，而不是把工具观察当策略输出训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次扩展发现关键实体，即使最终答错，也可能有正向过程价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21345v1">原论文</a> · <a href="../../../../post-training/2610.21345-opcredit/">实现解读</a> · <a href="#qa-467f3a76765e0009">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcredit" data-paper-title="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering LLM 后训练 Nanjing University 2026-10-15 整条轨迹失败不代表每一步都无用，成功轨迹也可能绕路。OpCredit 的 BOC 从普通 rollout 中复用分支结果：同题、同活动实体，再匹配访问集合、剩余预算和决策阶段；FTC 则衡量该操作局部前沿相对答案邻域的进退。两种信用对齐同一段推理及可执行操作 token，不给工具观察记策略损失。原文 §3、附录D 原文完整实验成本过高，不复现（审查 DONE）；这些是公式及梯度诊断，不是 KGQA 能力比较。L1 信用分配与梯度组件，不是 CWQ/WebQSP/GrailQA 能力复现。原文完整实验成本过高，不复现（审查 DONE）；本地 gold 只供训练后信用计算，不进入 Actor 输入或 evolve 晋级。随机初始化4输入、3输出的小策略在两个固定微型图上，每题真实采样6条关系选择＋答案动作轨迹。gold 仅在 rollout 结束后计算终止奖励与邻域信用；公开状态白名单只有题目、活动实体、访问集合、预算、阶段和可见实体，不能传 gold 字段。  Agentic RL 操作级信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 OpCredit比较同一操作时，为什么还要匹配访问集合、剩余预算和决策阶段？ 同一活动实体不等于同一可决策状态，过去访问和剩余资源会改变操作价值。BOC复用匹配上下文的分支结果并按轨迹去重，FTC另用训练专属答案邻域衡量局部前沿改善。答案信息只参与训练信用，不能进入actor输入，工具观察也不承担策略损失。 教学例子：都站在同一知识节点，一个轨迹已查过邻居、另一个还没查；再次扩展的价值不同，不能只按节点名混组比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b7d3d7888c5e21b5">OpCredit比较同一操作时，为什么还要匹配访问集合、剩余预算和决策阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopcredit">OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一活动实体不等于同一可决策状态，过去访问和剩余资源会改变操作价值。BOC复用匹配上下文的分支结果并按轨迹去重，FTC另用训练专属答案邻域衡量局部前沿改善。答案信息只参与训练信用，不能进入actor输入，工具观察也不承担策略损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>都站在同一知识节点，一个轨迹已查过邻居、另一个还没查；再次扩展的价值不同，不能只按节点名混组比较。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21345v1">原论文</a> · <a href="../../../../post-training/2610.21345-opcredit/">实现解读</a> · <a href="#qa-b7d3d7888c5e21b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcredit" data-paper-title="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering LLM 后训练 Nanjing University 2026-10-15 整条轨迹失败不代表每一步都无用，成功轨迹也可能绕路。OpCredit 的 BOC 从普通 rollout 中复用分支结果：同题、同活动实体，再匹配访问集合、剩余预算和决策阶段；FTC 则衡量该操作局部前沿相对答案邻域的进退。两种信用对齐同一段推理及可执行操作 token，不给工具观察记策略损失。原文 §3、附录D 原文完整实验成本过高，不复现（审查 DONE）；这些是公式及梯度诊断，不是 KGQA 能力比较。L1 信用分配与梯度组件，不是 CWQ/WebQSP/GrailQA 能力复现。原文完整实验成本过高，不复现（审查 DONE）；本地 gold 只供训练后信用计算，不进入 Actor 输入或 evolve 晋级。随机初始化4输入、3输出的小策略在两个固定微型图上，每题真实采样6条关系选择＋答案动作轨迹。gold 仅在 rollout 结束后计算终止奖励与邻域信用；公开状态白名单只有题目、活动实体、访问集合、预算、阶段和可见实体，不能传 gold 字段。  Agentic RL 操作级信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 BOC分支比较与FTC答案邻域进度各依赖什么？ BOC复用匹配状态下其他轨迹结果，FTC用训练专属答案邻域评价局部前沿。后者可使用训练标签计算信用，但actor采样时不可见，两者也不能当同一奖励。 例如知道哪个邻居更接近训练答案，只用于事后信用，不放进搜索请求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9c6efe2251e4b589">BOC分支比较与FTC答案邻域进度各依赖什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopcredit">OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>BOC复用匹配状态下其他轨迹结果，FTC用训练专属答案邻域评价局部前沿。后者可使用训练标签计算信用，但actor采样时不可见，两者也不能当同一奖励。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如知道哪个邻居更接近训练答案，只用于事后信用，不放进搜索请求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21345v1">原论文</a> · <a href="../../../../post-training/2610.21345-opcredit/">实现解读</a> · <a href="#qa-9c6efe2251e4b589">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcredit" data-paper-title="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering LLM 后训练 Nanjing University 2026-10-15 整条轨迹失败不代表每一步都无用，成功轨迹也可能绕路。OpCredit 的 BOC 从普通 rollout 中复用分支结果：同题、同活动实体，再匹配访问集合、剩余预算和决策阶段；FTC 则衡量该操作局部前沿相对答案邻域的进退。两种信用对齐同一段推理及可执行操作 token，不给工具观察记策略损失。原文 §3、附录D 原文完整实验成本过高，不复现（审查 DONE）；这些是公式及梯度诊断，不是 KGQA 能力比较。L1 信用分配与梯度组件，不是 CWQ/WebQSP/GrailQA 能力复现。原文完整实验成本过高，不复现（审查 DONE）；本地 gold 只供训练后信用计算，不进入 Actor 输入或 evolve 晋级。随机初始化4输入、3输出的小策略在两个固定微型图上，每题真实采样6条关系选择＋答案动作轨迹。gold 仅在 rollout 结束后计算终止奖励与邻域信用；公开状态白名单只有题目、活动实体、访问集合、预算、阶段和可见实体，不能传 gold 字段。  Agentic RL 操作级信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 OpCredit匹配分支为什么不能只看活动实体？ 还需同题、访问集合、剩余预算和阶段，才能让分支机会相近；支持集每轨迹只计一次。FTC取局部前沿最好机会，不是全图平均距离，信用及参考均停止梯度。 例如到同一节点但已经耗尽预算，与刚到节点的后续成功机会不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ddad88751e9efaa5">OpCredit匹配分支为什么不能只看活动实体？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopcredit">OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>还需同题、访问集合、剩余预算和阶段，才能让分支机会相近；支持集每轨迹只计一次。FTC取局部前沿最好机会，不是全图平均距离，信用及参考均停止梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如到同一节点但已经耗尽预算，与刚到节点的后续成功机会不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21345v1">原论文</a> · <a href="../../../../post-training/2610.21345-opcredit/">实现解读</a> · <a href="#qa-ddad88751e9efaa5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progress-reward" data-paper-title="Progress Reward Model for Reinforcement Learning via Large Language Models" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Progress Reward Model for Reinforcement Learning via Large Language Models LLM 后训练 Beihang University 2026-10-15 稀疏成功信号难以指导长程机器人控制。PRM4RL 让 LLM 给出子任务、当前子任务判定函数与进度势函数；将子任务语义作为状态先验，将相邻状态进度差作为低层 RL 的密集 reward。规划只需预先生成，而不是每个环境步重新调用 LLM。 完整机器人实验成本过高，不复现（审查 DONE）。L1 状态机、embedding 接口及 reward 机制诊断。L1 状态机、embedding 接口及 reward 机制诊断。这是 NeurIPS 2025 已发表成果于 2026-10-15 上传 arXiv，不能称为新提出的 2026 算法。完整机器人实验成本过高，不复现（审查 DONE）。本地 ProgressPlan 只接收调用者审阅过的 completion predicates、potential 与子任务名称，不执行上游或 LLM 返回的任意 Python。stage 从当前状态重新计算，可因抓取丢失等情况回退，不使用仅随时间递增的计数器。  过程奖励 后训练算法组件 PRM4RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 PRM4RL为什么同时提供子任务语义和进度势函数？ 子任务语义增强状态，告诉低层策略当前阶段；势函数差提供稠密进度奖励，缓解只有成功终局的稀疏反馈。二者分别改变输入与奖励，规划可预先生成。 例如机器人知道正在抓取，同时从离目标更近的状态变化获得进度信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-progress-reward-e17dc6a6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-43d964b36c94f1d8">PRM4RL为什么同时提供子任务语义和进度势函数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprogress-reward">Progress Reward Model for Reinforcement Learning via Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>子任务语义增强状态，告诉低层策略当前阶段；势函数差提供稠密进度奖励，缓解只有成功终局的稀疏反馈。二者分别改变输入与奖励，规划可预先生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如机器人知道正在抓取，同时从离目标更近的状态变化获得进度信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22056v1">原论文</a> · <a href="../../../../post-training/2610.22056-progress-reward/">实现解读</a> · <a href="#qa-43d964b36c94f1d8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progress-reward" data-paper-title="Progress Reward Model for Reinforcement Learning via Large Language Models" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Progress Reward Model for Reinforcement Learning via Large Language Models LLM 后训练 Beihang University 2026-10-15 稀疏成功信号难以指导长程机器人控制。PRM4RL 让 LLM 给出子任务、当前子任务判定函数与进度势函数；将子任务语义作为状态先验，将相邻状态进度差作为低层 RL 的密集 reward。规划只需预先生成，而不是每个环境步重新调用 LLM。 完整机器人实验成本过高，不复现（审查 DONE）。L1 状态机、embedding 接口及 reward 机制诊断。L1 状态机、embedding 接口及 reward 机制诊断。这是 NeurIPS 2025 已发表成果于 2026-10-15 上传 arXiv，不能称为新提出的 2026 算法。完整机器人实验成本过高，不复现（审查 DONE）。本地 ProgressPlan 只接收调用者审阅过的 completion predicates、potential 与子任务名称，不执行上游或 LLM 返回的任意 Python。stage 从当前状态重新计算，可因抓取丢失等情况回退，不使用仅随时间递增的计数器。  过程奖励 后训练算法组件 PRM4RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 PRM4RL为什么把进度奖励写成折扣势函数差，时间截断又为何不能当真实终止？ 势函数差让相邻状态的进度贡献沿轨迹望远镜相消，剩下起点和终点项。真实终止需要正确吸收边界处理，才能避免终点势值额外改变目标；时间预算截断后任务可能仍继续，不能自动将势函数置零。子任务编码与奖励塑形也是两个独立接口。 教学例子：机器人接近目标时因计时结束，不能假装任务已经真正终止；若把此处势值清零，可能凭空给出错误的进度惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8d43537bb6eddd8b">PRM4RL为什么把进度奖励写成折扣势函数差，时间截断又为何不能当真实终止？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprogress-reward">Progress Reward Model for Reinforcement Learning via Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>势函数差让相邻状态的进度贡献沿轨迹望远镜相消，剩下起点和终点项。真实终止需要正确吸收边界处理，才能避免终点势值额外改变目标；时间预算截断后任务可能仍继续，不能自动将势函数置零。子任务编码与奖励塑形也是两个独立接口。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>机器人接近目标时因计时结束，不能假装任务已经真正终止；若把此处势值清零，可能凭空给出错误的进度惩罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22056v1">原论文</a> · <a href="../../../../post-training/2610.22056-progress-reward/">实现解读</a> · <a href="#qa-8d43537bb6eddd8b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progress-reward" data-paper-title="Progress Reward Model for Reinforcement Learning via Large Language Models" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Progress Reward Model for Reinforcement Learning via Large Language Models LLM 后训练 Beihang University 2026-10-15 稀疏成功信号难以指导长程机器人控制。PRM4RL 让 LLM 给出子任务、当前子任务判定函数与进度势函数；将子任务语义作为状态先验，将相邻状态进度差作为低层 RL 的密集 reward。规划只需预先生成，而不是每个环境步重新调用 LLM。 完整机器人实验成本过高，不复现（审查 DONE）。L1 状态机、embedding 接口及 reward 机制诊断。L1 状态机、embedding 接口及 reward 机制诊断。这是 NeurIPS 2025 已发表成果于 2026-10-15 上传 arXiv，不能称为新提出的 2026 算法。完整机器人实验成本过高，不复现（审查 DONE）。本地 ProgressPlan 只接收调用者审阅过的 completion predicates、potential 与子任务名称，不执行上游或 LLM 返回的任意 Python。stage 从当前状态重新计算，可因抓取丢失等情况回退，不使用仅随时间递增的计数器。  过程奖励 后训练算法组件 PRM4RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 势函数塑形与直接奖励当前进度数值有什么差别？ 差分奖励看相邻状态变化，折扣和可望远镜相消；直接每步给高势值会鼓励停留。有限回合的边界条件仍关键，不能只因写了差分就自动保证策略不变。 例如停在高进度状态不继续完成任务，直接累计分可能奖励拖延。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4057a09262779abf">势函数塑形与直接奖励当前进度数值有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprogress-reward">Progress Reward Model for Reinforcement Learning via Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>差分奖励看相邻状态变化，折扣和可望远镜相消；直接每步给高势值会鼓励停留。有限回合的边界条件仍关键，不能只因写了差分就自动保证策略不变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如停在高进度状态不继续完成任务，直接累计分可能奖励拖延。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22056v1">原论文</a> · <a href="../../../../post-training/2610.22056-progress-reward/">实现解读</a> · <a href="#qa-4057a09262779abf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progress-reward" data-paper-title="Progress Reward Model for Reinforcement Learning via Large Language Models" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Progress Reward Model for Reinforcement Learning via Large Language Models LLM 后训练 Beihang University 2026-10-15 稀疏成功信号难以指导长程机器人控制。PRM4RL 让 LLM 给出子任务、当前子任务判定函数与进度势函数；将子任务语义作为状态先验，将相邻状态进度差作为低层 RL 的密集 reward。规划只需预先生成，而不是每个环境步重新调用 LLM。 完整机器人实验成本过高，不复现（审查 DONE）。L1 状态机、embedding 接口及 reward 机制诊断。L1 状态机、embedding 接口及 reward 机制诊断。这是 NeurIPS 2025 已发表成果于 2026-10-15 上传 arXiv，不能称为新提出的 2026 算法。完整机器人实验成本过高，不复现（审查 DONE）。本地 ProgressPlan 只接收调用者审阅过的 completion predicates、potential 与子任务名称，不执行上游或 LLM 返回的任意 Python。stage 从当前状态重新计算，可因抓取丢失等情况回退，不使用仅随时间递增的计数器。  过程奖励 后训练算法组件 PRM4RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 PRM4RL为什么区分terminated与时间截断？ 真实终止可按吸收边界置终点势为零，时间截断仍可能有后继价值，不能一律归零。未传明确终止时应按公式计算，不暗改边界；生成函数还需审阅合法性。 例如时间预算到但任务可继续，与物理任务完成或失败，是不同终止语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-94810a2cf81ad696">PRM4RL为什么区分terminated与时间截断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprogress-reward">Progress Reward Model for Reinforcement Learning via Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实终止可按吸收边界置终点势为零，时间截断仍可能有后继价值，不能一律归零。未传明确终止时应按公式计算，不暗改边界；生成函数还需审阅合法性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如时间预算到但任务可继续，与物理任务完成或失败，是不同终止语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22056v1">原论文</a> · <a href="../../../../post-training/2610.22056-progress-reward/">实现解读</a> · <a href="#qa-94810a2cf81ad696">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sif" data-paper-title="Learning to Reason with Selective Internal Feedback" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learning to Reason with Selective Internal Feedback LLM 后训练 Institute of Automation, Chinese Academy of Sciences 2026-10-15 平均 self-certainty 可以随错误置信一起增长。SIF 不把它当正确性标签，而是比较同一 prompt 内响应的排序 certainty profile：先按窗口比较投票，再按击败 peer 的比例给二元 reward，过滤不具资格的响应和同 reward 组。policy 与 KL 必须同时施加选择 mask。 完整实验成本过高，不复现（审查 DONE）。短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。L1 完整资格 / 投票 / 双 mask 公式组件。默认资格仍为 550 tokens；短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。完整实验成本过高，不复现（审查 DONE）。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；train/validation/test byte 区间 80%/10%/10% 不相交，不按 heldout NLL 选超参。  自置信轨迹过滤 Self-certainty 选择性策略更新 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SIF为什么不把平均self-certainty直接当正确标签？ 错误信心也能升高，方法比较同题多回答的排序确定性窗口，再以两级投票形成相对奖励。它利用分布形状与相对关系，仍不获得独立正确性真值。 例如整段都很自信的错误答案，不应只因平均值高就被宣布正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-sif-620fc6b5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f888a406df8ca361">SIF为什么不把平均self-certainty直接当正确标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asif">Learning to Reason with Selective Internal Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>错误信心也能升高，方法比较同题多回答的排序确定性窗口，再以两级投票形成相对奖励。它利用分布形状与相对关系，仍不获得独立正确性真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如整段都很自信的错误答案，不应只因平均值高就被宣布正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21392v1">原论文</a> · <a href="../../../../post-training/2610.21392-sif/">实现解读</a> · <a href="#qa-f888a406df8ca361">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sif" data-paper-title="Learning to Reason with Selective Internal Feedback" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learning to Reason with Selective Internal Feedback LLM 后训练 Institute of Automation, Chinese Academy of Sciences 2026-10-15 平均 self-certainty 可以随错误置信一起增长。SIF 不把它当正确性标签，而是比较同一 prompt 内响应的排序 certainty profile：先按窗口比较投票，再按击败 peer 的比例给二元 reward，过滤不具资格的响应和同 reward 组。policy 与 KL 必须同时施加选择 mask。 完整实验成本过高，不复现（审查 DONE）。短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。L1 完整资格 / 投票 / 双 mask 公式组件。默认资格仍为 550 tokens；短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。完整实验成本过高，不复现（审查 DONE）。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；train/validation/test byte 区间 80%/10%/10% 不相交，不按 heldout NLL 选超参。  自置信轨迹过滤 Self-certainty 选择性策略更新 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SIF为什么比较排序后的certainty窗口，而不把平均熵或高概率token当正确标签？ 平均确定性可能随错误自信一起上升，SIF使用均匀分布到策略的KL构成certainty profile，在合格同题回答间做窗口和peer两级比较。它不是token熵或采样词概率；不合格响应和同奖励组被过滤，policy与KL还必须使用同一选择mask。 教学例子：一条回答平均很自信，但只有少数位置贡献极端值；比较多个排序窗口，可与另一条分布较均匀的回答区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-560ca2565f6d2582">SIF为什么比较排序后的certainty窗口，而不把平均熵或高概率token当正确标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asif">Learning to Reason with Selective Internal Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平均确定性可能随错误自信一起上升，SIF使用均匀分布到策略的KL构成certainty profile，在合格同题回答间做窗口和peer两级比较。它不是token熵或采样词概率；不合格响应和同奖励组被过滤，policy与KL还必须使用同一选择mask。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条回答平均很自信，但只有少数位置贡献极端值；比较多个排序窗口，可与另一条分布较均匀的回答区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21392v1">原论文</a> · <a href="../../../../post-training/2610.21392-sif/">实现解读</a> · <a href="#qa-560ca2565f6d2582">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sif" data-paper-title="Learning to Reason with Selective Internal Feedback" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learning to Reason with Selective Internal Feedback LLM 后训练 Institute of Automation, Chinese Academy of Sciences 2026-10-15 平均 self-certainty 可以随错误置信一起增长。SIF 不把它当正确性标签，而是比较同一 prompt 内响应的排序 certainty profile：先按窗口比较投票，再按击败 peer 的比例给二元 reward，过滤不具资格的响应和同 reward 组。policy 与 KL 必须同时施加选择 mask。 完整实验成本过高，不复现（审查 DONE）。短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。L1 完整资格 / 投票 / 双 mask 公式组件。默认资格仍为 550 tokens；短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。完整实验成本过高，不复现（审查 DONE）。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；train/validation/test byte 区间 80%/10%/10% 不相交，不按 heldout NLL 选超参。  自置信轨迹过滤 Self-certainty 选择性策略更新 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SIF的KL(U||π)与负熵为何不是同一个确定性量？ 前者平均全词表对数概率，负熵按策略概率加权，方向不同，对低概率区域敏感性也不同。用采样词概率替代同样改变指标，不能仅说都是自信分数。 例如罕见词的概率趋零，对均匀到策略KL与策略加权熵的影响不一样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7db75046cdac1089">SIF的KL(U||π)与负熵为何不是同一个确定性量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asif">Learning to Reason with Selective Internal Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者平均全词表对数概率，负熵按策略概率加权，方向不同，对低概率区域敏感性也不同。用采样词概率替代同样改变指标，不能仅说都是自信分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如罕见词的概率趋零，对均匀到策略KL与策略加权熵的影响不一样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21392v1">原论文</a> · <a href="../../../../post-training/2610.21392-sif/">实现解读</a> · <a href="#qa-7db75046cdac1089">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sif" data-paper-title="Learning to Reason with Selective Internal Feedback" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learning to Reason with Selective Internal Feedback LLM 后训练 Institute of Automation, Chinese Academy of Sciences 2026-10-15 平均 self-certainty 可以随错误置信一起增长。SIF 不把它当正确性标签，而是比较同一 prompt 内响应的排序 certainty profile：先按窗口比较投票，再按击败 peer 的比例给二元 reward，过滤不具资格的响应和同 reward 组。policy 与 KL 必须同时施加选择 mask。 完整实验成本过高，不复现（审查 DONE）。短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。L1 完整资格 / 投票 / 双 mask 公式组件。默认资格仍为 550 tokens；短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。完整实验成本过高，不复现（审查 DONE）。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；train/validation/test byte 区间 80%/10%/10% 不相交，不按 heldout NLL 选超参。  自置信轨迹过滤 Self-certainty 选择性策略更新 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SIF不合资格响应是否也要关闭KL项？ 需要，policy与KL共用选择mask；组归一仍保留原响应因子，不偷偷改成仅合格响应数。窗口资格、严格比较与样本标准差也需按协议实现，不能把tie算获胜。 例如关闭策略损失却保留参考KL，仍会更新本应过滤的响应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-743b1654ab9a1908">SIF不合资格响应是否也要关闭KL项？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asif">Learning to Reason with Selective Internal Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需要，policy与KL共用选择mask；组归一仍保留原响应因子，不偷偷改成仅合格响应数。窗口资格、严格比较与样本标准差也需按协议实现，不能把tie算获胜。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如关闭策略损失却保留参考KL，仍会更新本应过滤的响应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21392v1">原论文</a> · <a href="../../../../post-training/2610.21392-sif/">实现解读</a> · <a href="#qa-743b1654ab9a1908">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tag-reward-gating" data-paper-title="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense LLM 后训练 University of British Columbia 2026-10-15 正确性和简短、低时延等奖励相加时，容易获取的辅助奖励可能主导 GRPO：总奖励上涨，主要任务却变差。TAG 不是简单降低辅助权重，而是先从同一基线分别优化每个奖励，观察哪个探针对基线的分布漂移最小，再将该奖励选为 anchor。随后丢弃探针、从原基线重新联合训练，辅助信用只有在 anchor 满足时才生效。原文 §5 原文关键图：Figure 1：短而错误的奖励投机；Figure 4 展示 reverse KL 对新造模式的敏感性。它们不是本地训练结果。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是数学或代码能力复现。L1 算法组件／梯度诊断，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不参与 evolve 晋级。使用随机初始化的32词表、8维 causal cumulative-embedding 策略，不下载任何 checkpoint。两个奖励是人工 token 奇偶条件，不表示数学正确性。每个奖励从同一基线独立做3次更新，在另一组提示上由该探针真实采样并计算选举统计，然后从未变化的基线做3次门控更新。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TAG为什么先选可信anchor再联合多奖励训练？ 辅助目标可能容易投机，让总分上涨却破坏主任务。anchor为联合奖励设前提，只有锚点满足时辅助信用才生效；它不是单纯把辅助系数调小。 例如短而错误不能仅凭简洁拿到正向辅助信用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-tag-reward-gating-d0312c36" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7568ec547fc88e46">TAG为什么先选可信anchor再联合多奖励训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atag-reward-gating">Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of British Columbia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>辅助目标可能容易投机，让总分上涨却破坏主任务。anchor为联合奖励设前提，只有锚点满足时辅助信用才生效；它不是单纯把辅助系数调小。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如短而错误不能仅凭简洁拿到正向辅助信用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21404v1">原论文</a> · <a href="../../../../post-training/2610.21404-tag-reward-gating/">实现解读</a> · <a href="#qa-7568ec547fc88e46">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tag-reward-gating" data-paper-title="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense LLM 后训练 University of British Columbia 2026-10-15 正确性和简短、低时延等奖励相加时，容易获取的辅助奖励可能主导 GRPO：总奖励上涨，主要任务却变差。TAG 不是简单降低辅助权重，而是先从同一基线分别优化每个奖励，观察哪个探针对基线的分布漂移最小，再将该奖励选为 anchor。随后丢弃探针、从原基线重新联合训练，辅助信用只有在 anchor 满足时才生效。原文 §5 原文关键图：Figure 1：短而错误的奖励投机；Figure 4 展示 reverse KL 对新造模式的敏感性。它们不是本地训练结果。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是数学或代码能力复现。L1 算法组件／梯度诊断，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不参与 evolve 晋级。使用随机初始化的32词表、8维 causal cumulative-embedding 策略，不下载任何 checkpoint。两个奖励是人工 token 奇偶条件，不表示数学正确性。每个奖励从同一基线独立做3次更新，在另一组提示上由该探针真实采样并计算选举统计，然后从未变化的基线做3次门控更新。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TAG选出anchor后为什么丢弃探针并从原基线重训，辅助奖励又何时生效？ 独立探针用于比较各奖励引起的分布漂移，选出最稳定的锚点，并非继续拿探针权重联合训练。重新从共同基线出发才能隔离选择机制；anchor不满足时辅助奖励不能单独给信用。探针轨迹须由探针自身采样，不能把KL方向悄悄换掉。 教学例子：简短回答很容易拿到辅助分，但答错时应被锚点门控挡住；不能靠越来越短，让总奖励上升却失去正确性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7a30ff0ff404f806">TAG选出anchor后为什么丢弃探针并从原基线重训，辅助奖励又何时生效？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atag-reward-gating">Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of British Columbia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立探针用于比较各奖励引起的分布漂移，选出最稳定的锚点，并非继续拿探针权重联合训练。重新从共同基线出发才能隔离选择机制；anchor不满足时辅助奖励不能单独给信用。探针轨迹须由探针自身采样，不能把KL方向悄悄换掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>简短回答很容易拿到辅助分，但答错时应被锚点门控挡住；不能靠越来越短，让总奖励上升却失去正确性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21404v1">原论文</a> · <a href="../../../../post-training/2610.21404-tag-reward-gating/">实现解读</a> · <a href="#qa-7a30ff0ff404f806">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tag-reward-gating" data-paper-title="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense LLM 后训练 University of British Columbia 2026-10-15 正确性和简短、低时延等奖励相加时，容易获取的辅助奖励可能主导 GRPO：总奖励上涨，主要任务却变差。TAG 不是简单降低辅助权重，而是先从同一基线分别优化每个奖励，观察哪个探针对基线的分布漂移最小，再将该奖励选为 anchor。随后丢弃探针、从原基线重新联合训练，辅助信用只有在 anchor 满足时才生效。原文 §5 原文关键图：Figure 1：短而错误的奖励投机；Figure 4 展示 reverse KL 对新造模式的敏感性。它们不是本地训练结果。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是数学或代码能力复现。L1 算法组件／梯度诊断，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不参与 evolve 晋级。使用随机初始化的32词表、8维 causal cumulative-embedding 策略，不下载任何 checkpoint。两个奖励是人工 token 奇偶条件，不表示数学正确性。每个奖励从同一基线独立做3次更新，在另一组提示上由该探针真实采样并计算选举统计，然后从未变化的基线做3次门控更新。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TAG选漂移最小探针与人工指定正确性anchor有什么区别？ 方法从同一基线分别探测各奖励，以探针到基线的逆KL漂移选择anchor，再丢弃探针重新训练。人工指定省去此选择过程，是不同配置，不能假称执行了探针选举。 例如最容易刷高的奖励可能导致大漂移，选择依据不是它得分升得最快。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f580247c5dd0e8fc">TAG选漂移最小探针与人工指定正确性anchor有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atag-reward-gating">Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of British Columbia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>方法从同一基线分别探测各奖励，以探针到基线的逆KL漂移选择anchor，再丢弃探针重新训练。人工指定省去此选择过程，是不同配置，不能假称执行了探针选举。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最容易刷高的奖励可能导致大漂移，选择依据不是它得分升得最快。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21404v1">原论文</a> · <a href="../../../../post-training/2610.21404-tag-reward-gating/">实现解读</a> · <a href="#qa-f580247c5dd0e8fc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tag-reward-gating" data-paper-title="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense LLM 后训练 University of British Columbia 2026-10-15 正确性和简短、低时延等奖励相加时，容易获取的辅助奖励可能主导 GRPO：总奖励上涨，主要任务却变差。TAG 不是简单降低辅助权重，而是先从同一基线分别优化每个奖励，观察哪个探针对基线的分布漂移最小，再将该奖励选为 anchor。随后丢弃探针、从原基线重新联合训练，辅助信用只有在 anchor 满足时才生效。原文 §5 原文关键图：Figure 1：短而错误的奖励投机；Figure 4 展示 reverse KL 对新造模式的敏感性。它们不是本地训练结果。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是数学或代码能力复现。L1 算法组件／梯度诊断，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不参与 evolve 晋级。使用随机初始化的32词表、8维 causal cumulative-embedding 策略，不下载任何 checkpoint。两个奖励是人工 token 奇偶条件，不表示数学正确性。每个奖励从同一基线独立做3次更新，在另一组提示上由该探针真实采样并计算选举统计，然后从未变化的基线做3次门控更新。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TAG漂移为什么必须在探针自己的采样轨迹上估？ 逆KL的期望分布是探针，改用基线采样会改变方向；按全部生成词元池化，不是先各响应平均。有限样本估计可负，不能为选举方便截成零。 例如长短探针响应的词元应按规定共同计数，而非每条强行同权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-97ee3549d16b5442">TAG漂移为什么必须在探针自己的采样轨迹上估？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atag-reward-gating">Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of British Columbia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逆KL的期望分布是探针，改用基线采样会改变方向；按全部生成词元池化，不是先各响应平均。有限样本估计可负，不能为选举方便截成零。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长短探针响应的词元应按规定共同计数，而非每条强行同权。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21404v1">原论文</a> · <a href="../../../../post-training/2610.21404-tag-reward-gating/">实现解读</a> · <a href="#qa-97ee3549d16b5442">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rap-walk" data-paper-title="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO LLM 后训练 未确认（已读 arXiv HTML 未列机构） 2026-10-14 RAP-Walk 不把成对视频偏好压成相互独立的胜率，而保留对手身份、循环关系和边清晰度。它在从输者到赢家的可靠随机游走中计算平稳偏好信用，经最低熵校准后修正原始胜率优势，最后仍交给同一 GRPO 更新。偏好循环并不自动表示视频质量差；可能是不同视频各擅长提示遵循、画面或运动。该方法把局部不一致当作传播可靠性线索，而不是删除循环或把循环直接写成负奖励。 完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。L1 图算子与策略更新接口。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。不提供输入时，产物明确标为 explicit_mechanism_fixtures，只验证图方向、循环、校准和可微 GRPO 更新接口。可通过 --input-path observed-graphs.json 提供已有真实评审概率：  偏好图信用分配 GRPO 视频后训练 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 RAP-Walk为什么保留偏好对手身份与循环结构？ 独立胜率会丢失赢了谁及偏好不一致信息，图传播利用边清晰度和循环可靠性修正信用。循环可能来自多维取舍，不能直接判视频差或删除节点。 例如A运动好、B画质好、C遵循好，三者循环不必是无用样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-rap-walk-742b8b38" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a29913380a281c97">RAP-Walk为什么保留偏好对手身份与循环结构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arap-walk">When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 未确认（已读 arXiv HTML 未列机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立胜率会丢失赢了谁及偏好不一致信息，图传播利用边清晰度和循环可靠性修正信用。循环可能来自多维取舍，不能直接判视频差或删除节点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如A运动好、B画质好、C遵循好，三者循环不必是无用样本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20089v1">原论文</a> · <a href="../../../../post-training/2610.20089-rap-walk/">实现解读</a> · <a href="#qa-a29913380a281c97">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rap-walk" data-paper-title="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO LLM 后训练 未确认（已读 arXiv HTML 未列机构） 2026-10-14 RAP-Walk 不把成对视频偏好压成相互独立的胜率，而保留对手身份、循环关系和边清晰度。它在从输者到赢家的可靠随机游走中计算平稳偏好信用，经最低熵校准后修正原始胜率优势，最后仍交给同一 GRPO 更新。偏好循环并不自动表示视频质量差；可能是不同视频各擅长提示遵循、画面或运动。该方法把局部不一致当作传播可靠性线索，而不是删除循环或把循环直接写成负奖励。 完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。L1 图算子与策略更新接口。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。不提供输入时，产物明确标为 explicit_mechanism_fixtures，只验证图方向、循环、校准和可微 GRPO 更新接口。可通过 --input-path observed-graphs.json 提供已有真实评审概率：  偏好图信用分配 GRPO 视频后训练 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 偏好出现循环时，RAP-Walk为什么不直接删除循环或把循环节点判成坏样本？ 循环可能来自不同视频各擅长不同维度，并不自动说明质量差。方法保留对手身份、边清晰度和循环不一致，构造从输者到赢家的可靠传播，再用平稳信用修正胜率优势。方向、收敛与熵校准都属于机制，不能随意换成普通PageRank。 教学例子：甲胜乙、乙胜丙、丙又胜甲，可能分别在画面、运动和遵循提示上占优；简单删掉三者会丢失有用比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6be900bea95718dd">偏好出现循环时，RAP-Walk为什么不直接删除循环或把循环节点判成坏样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arap-walk">When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 未确认（已读 arXiv HTML 未列机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>循环可能来自不同视频各擅长不同维度，并不自动说明质量差。方法保留对手身份、边清晰度和循环不一致，构造从输者到赢家的可靠传播，再用平稳信用修正胜率优势。方向、收敛与熵校准都属于机制，不能随意换成普通PageRank。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲胜乙、乙胜丙、丙又胜甲，可能分别在画面、运动和遵循提示上占优；简单删掉三者会丢失有用比较。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20089v1">原论文</a> · <a href="../../../../post-training/2610.20089-rap-walk/">实现解读</a> · <a href="#qa-6be900bea95718dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rap-walk" data-paper-title="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO LLM 后训练 未确认（已读 arXiv HTML 未列机构） 2026-10-14 RAP-Walk 不把成对视频偏好压成相互独立的胜率，而保留对手身份、循环关系和边清晰度。它在从输者到赢家的可靠随机游走中计算平稳偏好信用，经最低熵校准后修正原始胜率优势，最后仍交给同一 GRPO 更新。偏好循环并不自动表示视频质量差；可能是不同视频各擅长提示遵循、画面或运动。该方法把局部不一致当作传播可靠性线索，而不是删除循环或把循环直接写成负奖励。 完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。L1 图算子与策略更新接口。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。不提供输入时，产物明确标为 explicit_mechanism_fixtures，只验证图方向、循环、校准和可微 GRPO 更新接口。可通过 --input-path observed-graphs.json 提供已有真实评审概率：  偏好图信用分配 GRPO 视频后训练 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 可靠随机游走与普通平均胜率有什么差别？ 从输者流向赢家并结合可靠性得到平稳信用，再与胜率锚点混合；平均胜率没有这条传播结构。方法还限制最低熵，避免信用过度集中。 例如击败不同可靠对手在图中传播不同，不只是每次胜利都加同一票。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b676c0beb2f42f73">可靠随机游走与普通平均胜率有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arap-walk">When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 未确认（已读 arXiv HTML 未列机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>从输者流向赢家并结合可靠性得到平稳信用，再与胜率锚点混合；平均胜率没有这条传播结构。方法还限制最低熵，避免信用过度集中。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如击败不同可靠对手在图中传播不同，不只是每次胜利都加同一票。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20089v1">原论文</a> · <a href="../../../../post-training/2610.20089-rap-walk/">实现解读</a> · <a href="#qa-b676c0beb2f42f73">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rap-walk" data-paper-title="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO LLM 后训练 未确认（已读 arXiv HTML 未列机构） 2026-10-14 RAP-Walk 不把成对视频偏好压成相互独立的胜率，而保留对手身份、循环关系和边清晰度。它在从输者到赢家的可靠随机游走中计算平稳偏好信用，经最低熵校准后修正原始胜率优势，最后仍交给同一 GRPO 更新。偏好循环并不自动表示视频质量差；可能是不同视频各擅长提示遵循、画面或运动。该方法把局部不一致当作传播可靠性线索，而不是删除循环或把循环直接写成负奖励。 完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。L1 图算子与策略更新接口。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。不提供输入时，产物明确标为 explicit_mechanism_fixtures，只验证图方向、循环、校准和可微 GRPO 更新接口。可通过 --input-path observed-graphs.json 提供已有真实评审概率：  偏好图信用分配 GRPO 视频后训练 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 RAP-Walk不收敛时能自动加入PageRank teleportation吗？ 不能未声明替换。应按协议报错，转移方向用W_ji，混合后重新组标准化，偏好图与优势停止梯度。偷偷加传送会改变平稳分布及原算法。 例如把输到赢方向写反，游走会奖励相反节点，即使矩阵仍能归一化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-99e71ff2f73a8479">RAP-Walk不收敛时能自动加入PageRank teleportation吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arap-walk">When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 未确认（已读 arXiv HTML 未列机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能未声明替换。应按协议报错，转移方向用W_ji，混合后重新组标准化，偏好图与优势停止梯度。偷偷加传送会改变平稳分布及原算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把输到赢方向写反，游走会奖励相反节点，即使矩阵仍能归一化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20089v1">原论文</a> · <a href="../../../../post-training/2610.20089-rap-walk/">实现解读</a> · <a href="#qa-99e71ff2f73a8479">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:soar" data-paper-title="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents LLM 后训练 Zhejiang University / Microsoft 2026-10-09 只按答案奖训练的search agent可能答对却伪造证据依赖。SOAR独立记录atomic query的internal recall和external retrieval，再要求显式声明source。internal recall不接收旧reasoning或external evidence；来源一致性、正确性与格式reward训练真实策略。 本轮SOAR队列使用明确派生的工具文档属性QA训练诊断，不在不匹配的WikiText+GSM上宣称知识QA效果。本地对照口径：基线为相同source-aware工作流的without-source-reward消融；另有冻结初始策略；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Source-aware RL Search agents Source-consistency reward LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SOAR为什么要求答案显式声明知识来源？ 只答对无法判断证据依赖是否真实。内部回忆与外部检索分别记录，再核验所声明流能否支持答案，训练来源一致性而非事后随意编引文。 例如答案宣称来自检索，就应能由对应检索记录支持，而不是内存碰巧知道。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-soar-c6475aad" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a387e5ecd2d98831">SOAR为什么要求答案显式声明知识来源？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asoar">SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University / Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只答对无法判断证据依赖是否真实。内部回忆与外部检索分别记录，再核验所声明流能否支持答案，训练来源一致性而非事后随意编引文。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如答案宣称来自检索，就应能由对应检索记录支持，而不是内存碰巧知道。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13157">原论文</a> · <a href="../../../../reproductions/2610.13157-soar/">实现解读</a> · <a href="#qa-a387e5ecd2d98831">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:soar" data-paper-title="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents LLM 后训练 Zhejiang University / Microsoft 2026-10-09 只按答案奖训练的search agent可能答对却伪造证据依赖。SOAR独立记录atomic query的internal recall和external retrieval，再要求显式声明source。internal recall不接收旧reasoning或external evidence；来源一致性、正确性与格式reward训练真实策略。 本轮SOAR队列使用明确派生的工具文档属性QA训练诊断，不在不匹配的WikiText+GSM上宣称知识QA效果。本地对照口径：基线为相同source-aware工作流的without-source-reward消融；另有冻结初始策略；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Source-aware RL Search agents Source-consistency reward LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SOAR为什么只用回答声明的证据stream判来源一致性，另一stream碰巧含答案也不能给奖？ 来源声明应与真正支持答案的证据对应，否则模型可答对却编造依赖。独立内部回忆与外部检索后，校验只查看声明的stream，避免另一侧泄漏替它兜底。内部回忆不能先读外部证据或旧推理，工具观察也不作为可训练的生成动作token。 教学例子：答案声称来自检索网页，但事实其实只在模型内部回忆中出现；不能因另一stream有正确事实就判引用一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-12ee59ebf4740899">SOAR为什么只用回答声明的证据stream判来源一致性，另一stream碰巧含答案也不能给奖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asoar">SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University / Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源声明应与真正支持答案的证据对应，否则模型可答对却编造依赖。独立内部回忆与外部检索后，校验只查看声明的stream，避免另一侧泄漏替它兜底。内部回忆不能先读外部证据或旧推理，工具观察也不作为可训练的生成动作token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>答案声称来自检索网页，但事实其实只在模型内部回忆中出现；不能因另一stream有正确事实就判引用一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13157">原论文</a> · <a href="../../../../reproductions/2610.13157-soar/">实现解读</a> · <a href="#qa-12ee59ebf4740899">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:soar" data-paper-title="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents LLM 后训练 Zhejiang University / Microsoft 2026-10-09 只按答案奖训练的search agent可能答对却伪造证据依赖。SOAR独立记录atomic query的internal recall和external retrieval，再要求显式声明source。internal recall不接收旧reasoning或external evidence；来源一致性、正确性与格式reward训练真实策略。 本轮SOAR队列使用明确派生的工具文档属性QA训练诊断，不在不匹配的WikiText+GSM上宣称知识QA效果。本地对照口径：基线为相同source-aware工作流的without-source-reward消融；另有冻结初始策略；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Source-aware RL Search agents Source-consistency reward LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SOAR的internal recall为什么不能读旧推理和检索证据？ 要区分内部已有知识与外部获得信息，就必须先隔离诱导回忆输入。若把检索结果传进去，内部流已被污染，后续来源匹配失去意义。 例如先看网页再回忆同一事实，不能算模型原本独立记得。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-96979c3c6b6830da">SOAR的internal recall为什么不能读旧推理和检索证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asoar">SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University / Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>要区分内部已有知识与外部获得信息，就必须先隔离诱导回忆输入。若把检索结果传进去，内部流已被污染，后续来源匹配失去意义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先看网页再回忆同一事实，不能算模型原本独立记得。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13157">原论文</a> · <a href="../../../../reproductions/2610.13157-soar/">实现解读</a> · <a href="#qa-96979c3c6b6830da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:soar" data-paper-title="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents LLM 后训练 Zhejiang University / Microsoft 2026-10-09 只按答案奖训练的search agent可能答对却伪造证据依赖。SOAR独立记录atomic query的internal recall和external retrieval，再要求显式声明source。internal recall不接收旧reasoning或external evidence；来源一致性、正确性与格式reward训练真实策略。 本轮SOAR队列使用明确派生的工具文档属性QA训练诊断，不在不匹配的WikiText+GSM上宣称知识QA效果。本地对照口径：基线为相同source-aware工作流的without-source-reward消融；另有冻结初始策略；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Source-aware RL Search agents Source-consistency reward LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SOAR匹配奖励能借另一条stream中正确证据补分吗？ 不能，只核验声明stream。工具观察和internal recall文本也不接受actor策略loss，奖励按明示归一后再组优势；完整机制执行与外部 benchmark能力结论仍要区分。 例如宣称内部知识却只有外部网页支持，不能因答案对就授予来源匹配奖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b7b5b84db8f01af1">SOAR匹配奖励能借另一条stream中正确证据补分吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asoar">SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University / Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，只核验声明stream。工具观察和internal recall文本也不接受actor策略loss，奖励按明示归一后再组优势；完整机制执行与外部 benchmark能力结论仍要区分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如宣称内部知识却只有外部网页支持，不能因答案对就授予来源匹配奖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13157">原论文</a> · <a href="../../../../reproductions/2610.13157-soar/">实现解读</a> · <a href="#qa-b7b5b84db8f01af1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:upturn" data-paper-title="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction LLM 后训练 KAIST 2026-10-09 冻结reasoner和小causal encoder，只学习paragraph boundary处的MLP cut policy。真实失败rollout在不同cut被冻结reasoner重新生成，给rescue奖励。推理时独立learned gate决定纠错；保留prefix、结束assistant turn、插固定新user turn，按剩余response预算生成suffix。 本页不声明未执行实验已经完成。本地对照口径：基线为Base@2N完整rollout，对照UPTURN@N及至多N次替换；预算匹配为最大允许生成数，不等于实际耗时一致；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Self-correction Frozen causal encoder Learned cut policy LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 UpTurn学习的是如何改写每个词，还是在哪里重开纠错？ 主要学习段落边界的cut policy与是否纠错的gate，reasoner和编码器冻结。选中位置后保留前缀，插入固定新user turn，由冻结reasoner继续生成。 例如在一段错误推导后发起新轮纠正，而非给每个旧token直接改概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-upturn-1713cc09" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d3ef4642ef0f2fa1">UpTurn学习的是如何改写每个词，还是在哪里重开纠错？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aupturn">Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主要学习段落边界的cut policy与是否纠错的gate，reasoner和编码器冻结。选中位置后保留前缀，插入固定新user turn，由冻结reasoner继续生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如在一段错误推导后发起新轮纠正，而非给每个旧token直接改概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13672">原论文</a> · <a href="../../../../reproductions/2610.13672-upturn/">实现解读</a> · <a href="#qa-d3ef4642ef0f2fa1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:upturn" data-paper-title="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction LLM 后训练 KAIST 2026-10-09 冻结reasoner和小causal encoder，只学习paragraph boundary处的MLP cut policy。真实失败rollout在不同cut被冻结reasoner重新生成，给rescue奖励。推理时独立learned gate决定纠错；保留prefix、结束assistant turn、插固定新user turn，按剩余response预算生成suffix。 本页不声明未执行实验已经完成。本地对照口径：基线为Base@2N完整rollout，对照UPTURN@N及至多N次替换；预算匹配为最大允许生成数，不等于实际耗时一致；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Self-correction Frozen causal encoder Learned cut policy LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 UPTURN为什么学习段落边界上的cut，而不是直接微调整个reasoner？ 冻结reasoner后，学习对象集中到何时插入纠错轮次，救援回报来自不同cut后的真实重新生成。保留前缀、结束当前轮并插固定新用户轮，再按剩余预算生成后缀，与整段重写或参数级推理训练不同。推理gate必须独立决定，不能由gold答案触发。 教学例子：推导在某段开始偏离，可在该段边界发起一次重新考虑；前文保留，后续预算减少，不能把这次救援当成无限免费重试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-725c5fb5bbb1c264">UPTURN为什么学习段落边界上的cut，而不是直接微调整个reasoner？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aupturn">Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结reasoner后，学习对象集中到何时插入纠错轮次，救援回报来自不同cut后的真实重新生成。保留前缀、结束当前轮并插固定新用户轮，再按剩余预算生成后缀，与整段重写或参数级推理训练不同。推理gate必须独立决定，不能由gold答案触发。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>推导在某段开始偏离，可在该段边界发起一次重新考虑；前文保留，后续预算减少，不能把这次救援当成无限免费重试。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13672">原论文</a> · <a href="../../../../reproductions/2610.13672-upturn/">实现解读</a> · <a href="#qa-725c5fb5bbb1c264">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:upturn" data-paper-title="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction LLM 后训练 KAIST 2026-10-09 冻结reasoner和小causal encoder，只学习paragraph boundary处的MLP cut policy。真实失败rollout在不同cut被冻结reasoner重新生成，给rescue奖励。推理时独立learned gate决定纠错；保留prefix、结束assistant turn、插固定新user turn，按剩余response预算生成suffix。 本页不声明未执行实验已经完成。本地对照口径：基线为Base@2N完整rollout，对照UPTURN@N及至多N次替换；预算匹配为最大允许生成数，不等于实际耗时一致；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Self-correction Frozen causal encoder Learned cut policy LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 插入新turn与在同一assistant消息中补一句反思有何差别？ 消息角色与条件边界改变，方法明确结束旧assistant并加入新user指令，再按剩余预算续写。简单字符串追加可能没有相同对话语义，不能当同一实现。 例如新用户说重新检查，会与assistant自己继续碎碎念形成不同提示结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-75e2b20d8166f842">插入新turn与在同一assistant消息中补一句反思有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aupturn">Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>消息角色与条件边界改变，方法明确结束旧assistant并加入新user指令，再按剩余预算续写。简单字符串追加可能没有相同对话语义，不能当同一实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新用户说重新检查，会与assistant自己继续碎碎念形成不同提示结构。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13672">原论文</a> · <a href="../../../../reproductions/2610.13672-upturn/">实现解读</a> · <a href="#qa-75e2b20d8166f842">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:upturn" data-paper-title="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction LLM 后训练 KAIST 2026-10-09 冻结reasoner和小causal encoder，只学习paragraph boundary处的MLP cut policy。真实失败rollout在不同cut被冻结reasoner重新生成，给rescue奖励。推理时独立learned gate决定纠错；保留prefix、结束assistant turn、插固定新user turn，按剩余response预算生成suffix。 本页不声明未执行实验已经完成。本地对照口径：基线为Base@2N完整rollout，对照UPTURN@N及至多N次替换；预算匹配为最大允许生成数，不等于实际耗时一致；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Self-correction Frozen causal encoder Learned cut policy LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 UpTurn的suffix预算为什么不能重新给满L_max？ 前缀已消耗响应预算，后缀只剩L_max减cut位置。无可解析答案gate为零，阈值按协议固定；既有三seed中仍有机制不通过，不能把执行完成等同稳定通过。 例如切在很后面时仍给满预算，会让方法比对照多用大量生成成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-335c54c30d946d1b">UpTurn的suffix预算为什么不能重新给满L_max？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aupturn">Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前缀已消耗响应预算，后缀只剩L_max减cut位置。无可解析答案gate为零，阈值按协议固定；既有三seed中仍有机制不通过，不能把执行完成等同稳定通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如切在很后面时仍给满预算，会让方法比对照多用大量生成成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13672">原论文</a> · <a href="../../../../reproductions/2610.13672-upturn/">实现解读</a> · <a href="#qa-335c54c30d946d1b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:residual-advantage" data-paper-title="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards LLM 后训练 Harbin Engineering University / Tencent / Harbin Institute of Technology 2026-10-08 把全词表师生概率残差变成相对学生的有界局部优势，再逐响应中心化，与验证器优势相加。Co-RA 在同一已评分学生批次上更新教师 LoRA，下一轮才使用新教师。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Teacher guidance LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Residual Advantage为什么把师生概率残差变成局部优势？ 教师分布差提供稠密指导，扣除学生分布期望基线后得到相对当前学生的信号，再与验证器优势结合。它不是仅增加一个终局教师评分。 例如同一前缀里教师更支持另一个词，可为当前词提供局部改进方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-residual-advantage-393aad16" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-95133b8bdb919c25">Residual Advantage为什么把师生概率残差变成局部优势？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aresidual-advantage">Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Engineering University / Tencent / Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师分布差提供稠密指导，扣除学生分布期望基线后得到相对当前学生的信号，再与验证器优势结合。它不是仅增加一个终局教师评分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一前缀里教师更支持另一个词，可为当前词提供局部改进方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11519">原论文</a> · <a href="../../../../post-training/2610.11519-residual-advantage/">实现解读</a> · <a href="#qa-95133b8bdb919c25">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:residual-advantage" data-paper-title="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards LLM 后训练 Harbin Engineering University / Tencent / Harbin Institute of Technology 2026-10-08 把全词表师生概率残差变成相对学生的有界局部优势，再逐响应中心化，与验证器优势相加。Co-RA 在同一已评分学生批次上更新教师 LoRA，下一轮才使用新教师。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Teacher guidance LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Residual Advantage为什么减去学生分布下的残差期望，再做响应内中心化？ 师生概率差的原始值依赖学生当前覆盖，减去学生期望后才得到相对学生的局部优势，响应中心化再分离位置差异。它与验证器优势相加而非取代真值信号。共同更新教师时先固定同一已评分批次，新教师只在下一轮使用，不能中途重标标签。 教学例子：教师对某词比学生更支持，但学生对许多替代词也有相近残差；需相对整体基线判断，而非看到差值为正就强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1982982d6084b49f">Residual Advantage为什么减去学生分布下的残差期望，再做响应内中心化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aresidual-advantage">Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Engineering University / Tencent / Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>师生概率差的原始值依赖学生当前覆盖，减去学生期望后才得到相对学生的局部优势，响应中心化再分离位置差异。它与验证器优势相加而非取代真值信号。共同更新教师时先固定同一已评分批次，新教师只在下一轮使用，不能中途重标标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师对某词比学生更支持，但学生对许多替代词也有相近残差；需相对整体基线判断，而非看到差值为正就强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11519">原论文</a> · <a href="../../../../post-training/2610.11519-residual-advantage/">实现解读</a> · <a href="#qa-1982982d6084b49f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:residual-advantage" data-paper-title="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards LLM 后训练 Harbin Engineering University / Tencent / Harbin Institute of Technology 2026-10-08 把全词表师生概率残差变成相对学生的有界局部优势，再逐响应中心化，与验证器优势相加。Co-RA 在同一已评分学生批次上更新教师 LoRA，下一轮才使用新教师。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Teacher guidance LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 残差优势与直接全分布KL蒸馏的监督形式有何不同？ 残差构造成有界局部优势并逐响应中心化，进入策略更新；KL直接约束分布差。二者梯度形式与任务奖励组合不同，不能只因都用教师概率就等同。 例如局部修正先减学生期望与响应均值，不是原封不动复制教师logits。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-784c243a2fc82976">残差优势与直接全分布KL蒸馏的监督形式有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aresidual-advantage">Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Engineering University / Tencent / Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>残差构造成有界局部优势并逐响应中心化，进入策略更新；KL直接约束分布差。二者梯度形式与任务奖励组合不同，不能只因都用教师概率就等同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如局部修正先减学生期望与响应均值，不是原封不动复制教师logits。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11519">原论文</a> · <a href="../../../../post-training/2610.11519-residual-advantage/">实现解读</a> · <a href="#qa-784c243a2fc82976">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:residual-advantage" data-paper-title="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards LLM 后训练 Harbin Engineering University / Tencent / Harbin Institute of Technology 2026-10-08 把全词表师生概率残差变成相对学生的有界局部优势，再逐响应中心化，与验证器优势相加。Co-RA 在同一已评分学生批次上更新教师 LoRA，下一轮才使用新教师。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Teacher guidance LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Co-RA为什么本批评分后不允许中途换教师重打标签？ 学生与教师更新基于同一已评分批次，教师LoRA只用固定验证器优势更新，新教师下一轮才使用。中途重算会让同批目标随参数变化，破坏可追溯顺序。 例如学生前半批读旧教师、后半批读已更新教师，不再是同一固定监督批。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2fa1b9bb8cbdadff">Co-RA为什么本批评分后不允许中途换教师重打标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aresidual-advantage">Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Engineering University / Tencent / Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生与教师更新基于同一已评分批次，教师LoRA只用固定验证器优势更新，新教师下一轮才使用。中途重算会让同批目标随参数变化，破坏可追溯顺序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生前半批读旧教师、后半批读已更新教师，不再是同一固定监督批。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11519">原论文</a> · <a href="../../../../post-training/2610.11519-residual-advantage/">实现解读</a> · <a href="#qa-2fa1b9bb8cbdadff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:carm" data-paper-title="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning LLM 后训练 Moore Threads AI 2026-10-01 对每个 token 的 current/rollout log-ratio 先取绝对值再平均，避免正负漂移在序列级几何均值中抵消。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 detached response gate；未训练 Qwen3.5。执行 detached response gate；未训练 Qwen3.5。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RLVR off-policy 响应掩码 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CARM为什么先对token log-ratio取绝对值？ 序列平均可让正负漂移抵消，看似接近旧策略却各位置已严重改变。先绝对再平均测总体偏离幅度，用响应门控识别这种相消风险。 例如一个位置概率大升、另一个大降，平均log比可能恰好为零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-carm-c2bacd93" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4d62623fa8b57200">CARM为什么先对token log-ratio取绝对值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acarm">CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moore Threads AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>序列平均可让正负漂移抵消，看似接近旧策略却各位置已严重改变。先绝对再平均测总体偏离幅度，用响应门控识别这种相消风险。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个位置概率大升、另一个大降，平均log比可能恰好为零。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02039">原论文</a> · <a href="../../../../post-training/2610.02039-carm/">实现解读</a> · <a href="#qa-4d62623fa8b57200">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:carm" data-paper-title="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning LLM 后训练 Moore Threads AI 2026-10-01 对每个 token 的 current/rollout log-ratio 先取绝对值再平均，避免正负漂移在序列级几何均值中抵消。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 detached response gate；未训练 Qwen3.5。执行 detached response gate；未训练 Qwen3.5。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RLVR off-policy 响应掩码 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CARM为什么先对每个token的log-ratio取绝对值，再求响应平均？ 一处概率上升与另一处下降可能在普通序列平均中抵消，让整条响应看似没有漂移。先取绝对值保留偏移幅度，再用响应gate筛出累积失配大的样本。它衡量的是策略变化而非回答质量；gate应冻结，不能借选择过程反向改变筛选依据。 教学例子：前半句概率显著上升，后半句等幅下降，总log-ratio接近零；绝对偏移平均仍会发现这条响应变化很大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8bd0cdb80dceafcc">CARM为什么先对每个token的log-ratio取绝对值，再求响应平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acarm">CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moore Threads AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一处概率上升与另一处下降可能在普通序列平均中抵消，让整条响应看似没有漂移。先取绝对值保留偏移幅度，再用响应gate筛出累积失配大的样本。它衡量的是策略变化而非回答质量；gate应冻结，不能借选择过程反向改变筛选依据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>前半句概率显著上升，后半句等幅下降，总log-ratio接近零；绝对偏移平均仍会发现这条响应变化很大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02039">原论文</a> · <a href="../../../../post-training/2610.02039-carm/">实现解读</a> · <a href="#qa-8bd0cdb80dceafcc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:carm" data-paper-title="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning LLM 后训练 Moore Threads AI 2026-10-01 对每个 token 的 current/rollout log-ratio 先取绝对值再平均，避免正负漂移在序列级几何均值中抵消。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 detached response gate；未训练 Qwen3.5。执行 detached response gate；未训练 Qwen3.5。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RLVR off-policy 响应掩码 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CARM与按序列几何比接近一筛样本有何差别？ 几何比保留方向相消，CARM关注不带符号的幅度；因此可拒绝总比值近一却内部变化大的响应。它不是任务质量评分，也不保证被保留回答正确。 例如总账收支为零不表示没有大额流动，两个指标测的是不同性质。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5c46d61ebc67a055">CARM与按序列几何比接近一筛样本有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acarm">CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moore Threads AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>几何比保留方向相消，CARM关注不带符号的幅度；因此可拒绝总比值近一却内部变化大的响应。它不是任务质量评分，也不保证被保留回答正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如总账收支为零不表示没有大额流动，两个指标测的是不同性质。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02039">原论文</a> · <a href="../../../../post-training/2610.02039-carm/">实现解读</a> · <a href="#qa-5c46d61ebc67a055">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:carm" data-paper-title="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning LLM 后训练 Moore Threads AI 2026-10-01 对每个 token 的 current/rollout log-ratio 先取绝对值再平均，避免正负漂移在序列级几何均值中抵消。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 detached response gate；未训练 Qwen3.5。执行 detached response gate；未训练 Qwen3.5。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RLVR off-policy 响应掩码 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CARM的response gate应该进入梯度计算吗？ 作为冻结选择门控使用，不通过阈值判定求导。统计只覆盖有效响应词元，并按规定阈值保留；本地未训练Qwen3.5，不能把mask核通过当实际稳定收益。 例如更新后概率变化不应在同一步通过gate支路额外推导一份梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5e16cfa5082016de">CARM的response gate应该进入梯度计算吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acarm">CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moore Threads AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>作为冻结选择门控使用，不通过阈值判定求导。统计只覆盖有效响应词元，并按规定阈值保留；本地未训练Qwen3.5，不能把mask核通过当实际稳定收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如更新后概率变化不应在同一步通过gate支路额外推导一份梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02039">原论文</a> · <a href="../../../../post-training/2610.02039-carm/">实现解读</a> · <a href="#qa-5e16cfa5082016de">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:my-fault" data-paper-title="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning LLM 后训练 Alibaba Group 2026-10-01 自诊断器提出错误类别与位置，只有经证据验证的 claim 才进入在线 error pricing；学得的相对成本把终局 credit 守恒地重分配到步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 信用分配 自诊断 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 My FAULT为什么先验证自诊断claim再定错误成本？ 模型自我解释可能编造原因，只有有证据支持的类别与位置才进入在线定价。终局信用按相对错误成本分配，防止未经验证的自责直接改变训练。 例如模型说是工具错了，需要执行记录支持，不能仅因它这么说就惩罚工具步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-my-fault-cefa1f11" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3e739d97e21fc937">My FAULT为什么先验证自诊断claim再定错误成本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amy-fault">My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型自我解释可能编造原因，只有有证据支持的类别与位置才进入在线定价。终局信用按相对错误成本分配，防止未经验证的自责直接改变训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型说是工具错了，需要执行记录支持，不能仅因它这么说就惩罚工具步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01161">原论文</a> · <a href="../../../../post-training/2610.01161-my-fault/">实现解读</a> · <a href="#qa-3e739d97e21fc937">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:my-fault" data-paper-title="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning LLM 后训练 Alibaba Group 2026-10-01 自诊断器提出错误类别与位置，只有经证据验证的 claim 才进入在线 error pricing；学得的相对成本把终局 credit 守恒地重分配到步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 信用分配 自诊断 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 My FAULT为什么要求自诊断claim先经证据验证，再进入error pricing？ 自诊断文本可能只是事后合理化，未经核对就估计错误成本会把偏见写进训练。验证后的类别与位置用于在线相对定价，再在步骤间重新分配终局信用，并保持总量守恒。它改变信用位置，不凭空创造成功奖励；本地没有联合训练完整诊断模型。 教学例子：失败后模型说“搜索错了”，但日志显示工具调用正确、最终汇总丢了事实；未经验证的归因不应指导搜索步骤受罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8a0aa95a3d7af3e5">My FAULT为什么要求自诊断claim先经证据验证，再进入error pricing？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amy-fault">My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自诊断文本可能只是事后合理化，未经核对就估计错误成本会把偏见写进训练。验证后的类别与位置用于在线相对定价，再在步骤间重新分配终局信用，并保持总量守恒。它改变信用位置，不凭空创造成功奖励；本地没有联合训练完整诊断模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>失败后模型说“搜索错了”，但日志显示工具调用正确、最终汇总丢了事实；未经验证的归因不应指导搜索步骤受罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01161">原论文</a> · <a href="../../../../post-training/2610.01161-my-fault/">实现解读</a> · <a href="#qa-8a0aa95a3d7af3e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:my-fault" data-paper-title="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning LLM 后训练 Alibaba Group 2026-10-01 自诊断器提出错误类别与位置，只有经证据验证的 claim 才进入在线 error pricing；学得的相对成本把终局 credit 守恒地重分配到步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 信用分配 自诊断 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 守恒重分配与额外加一份错误惩罚有何区别？ 守恒方式保持步骤信用总和等于原终局回报，只改变分布；额外惩罚会改变总目标。两者学习激励不同，不能把任意扣分称为同一error pricing。 例如某一步多扣的信用需在其他步骤相对补回，而不是整条总分又少一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ad19140e9b0328c6">守恒重分配与额外加一份错误惩罚有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amy-fault">My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>守恒方式保持步骤信用总和等于原终局回报，只改变分布；额外惩罚会改变总目标。两者学习激励不同，不能把任意扣分称为同一error pricing。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某一步多扣的信用需在其他步骤相对补回，而不是整条总分又少一次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01161">原论文</a> · <a href="../../../../post-training/2610.01161-my-fault/">实现解读</a> · <a href="#qa-ad19140e9b0328c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:my-fault" data-paper-title="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning LLM 后训练 Alibaba Group 2026-10-01 自诊断器提出错误类别与位置，只有经证据验证的 claim 才进入在线 error pricing；学得的相对成本把终局 credit 守恒地重分配到步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 信用分配 自诊断 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 My FAULT实现应检验哪条守恒不变量？ 逐步重分配之和应等于原回报，成本均值与步数需使用相同有效步骤集合。当前本地仅验证诊断筛选、成本及守恒核，没有共同训练策略和诊断模型。 例如把padding也算进平均成本，会破坏有效步骤上的总信用关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-22cc52b5d633b695">My FAULT实现应检验哪条守恒不变量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amy-fault">My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐步重分配之和应等于原回报，成本均值与步数需使用相同有效步骤集合。当前本地仅验证诊断筛选、成本及守恒核，没有共同训练策略和诊断模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把padding也算进平均成本，会破坏有效步骤上的总信用关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01161">原论文</a> · <a href="../../../../post-training/2610.01161-my-fault/">实现解读</a> · <a href="#qa-22cc52b5d633b695">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tvrl" data-paper-title="Token-Level Video Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Token-Level Video Reinforcement Learning LLM 后训练 原文首页未列第一作者机构 2026-10-01 冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度 credit 归一化；未训练视频扩散模型。执行梯度 credit 归一化；未训练视频扩散模型。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  视频生成 token credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TVRL为什么用梯度敏感性分配token信用？ 视频终局奖励粗糙，冻结评价路径对生成位置的敏感度提供局部线索，再重分配组优势。敏感不等于该词必然正确，只表示奖励对相应变化更敏感。 例如描述动作的词比连接词更影响视频奖励，可获得不同局部权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-tvrl-0c541634" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-017b1a45c76fbcfd">TVRL为什么用梯度敏感性分配token信用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atvrl">Token-Level Video Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视频终局奖励粗糙，冻结评价路径对生成位置的敏感度提供局部线索，再重分配组优势。敏感不等于该词必然正确，只表示奖励对相应变化更敏感。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如描述动作的词比连接词更影响视频奖励，可获得不同局部权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01973">原论文</a> · <a href="../../../../post-training/2610.01973-tvrl/">实现解读</a> · <a href="#qa-017b1a45c76fbcfd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tvrl" data-paper-title="Token-Level Video Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Token-Level Video Reinforcement Learning LLM 后训练 原文首页未列第一作者机构 2026-10-01 冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度 credit 归一化；未训练视频扩散模型。执行梯度 credit 归一化；未训练视频扩散模型。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  视频生成 token credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 视频token对冻结VLM奖励的梯度较大，为什么只能理解为敏感度而非必然正确的信用？ 梯度描述当前奖励模型对局部变化的敏感程度，可用于把同组优势稠密分配给生成token；按均值归一化控制总尺度。但评分模型也可能依赖捷径，敏感位置不一定是真正因果要素。本地只检验信用归一化，没有训练视频模型或证明感知质量提升。 教学例子：奖励模型可能对画面角落标记特别敏感；即使其梯度很大，也不能直接断定修改该区域就是提高视频质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-52574986269291c8">视频token对冻结VLM奖励的梯度较大，为什么只能理解为敏感度而非必然正确的信用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atvrl">Token-Level Video Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>梯度描述当前奖励模型对局部变化的敏感程度，可用于把同组优势稠密分配给生成token；按均值归一化控制总尺度。但评分模型也可能依赖捷径，敏感位置不一定是真正因果要素。本地只检验信用归一化，没有训练视频模型或证明感知质量提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>奖励模型可能对画面角落标记特别敏感；即使其梯度很大，也不能直接断定修改该区域就是提高视频质量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01973">原论文</a> · <a href="../../../../post-training/2610.01973-tvrl/">实现解读</a> · <a href="#qa-52574986269291c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tvrl" data-paper-title="Token-Level Video Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Token-Level Video Reinforcement Learning LLM 后训练 原文首页未列第一作者机构 2026-10-01 冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度 credit 归一化；未训练视频扩散模型。执行梯度 credit 归一化；未训练视频扩散模型。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  视频生成 token credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TVRL梯度信用与把相同优势均匀发给所有token有什么差别？ 均匀广播忽略位置贡献差异，归一化梯度范数使敏感位置权重大、其他小。它仍依赖冻结VLM评价的质量，不能由梯度大直接断言真正因果贡献大。 例如评价器特别在意某词，也可能是其偏差，而非任务必需证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-344d709eb000f913">TVRL梯度信用与把相同优势均匀发给所有token有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atvrl">Token-Level Video Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均匀广播忽略位置贡献差异，归一化梯度范数使敏感位置权重大、其他小。它仍依赖冻结VLM评价的质量，不能由梯度大直接断言真正因果贡献大。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如评价器特别在意某词，也可能是其偏差，而非任务必需证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01973">原论文</a> · <a href="../../../../post-training/2610.01973-tvrl/">实现解读</a> · <a href="#qa-344d709eb000f913">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tvrl" data-paper-title="Token-Level Video Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Token-Level Video Reinforcement Learning LLM 后训练 原文首页未列第一作者机构 2026-10-01 冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度 credit 归一化；未训练视频扩散模型。执行梯度 credit 归一化；未训练视频扩散模型。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  视频生成 token credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TVRL本地信用核是否已经训练视频扩散模型？ 没有，只计算梯度信用及均值归一。实际还需真实视频输入、冻结VLM梯度与策略训练路径；输入范数全零等边界须明确，不能靠随机数替代后宣传视频能力。 例如人工给几个梯度大小，可验权重，却没有执行任何视频生成训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7e0532299250133a">TVRL本地信用核是否已经训练视频扩散模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atvrl">Token-Level Video Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，只计算梯度信用及均值归一。实际还需真实视频输入、冻结VLM梯度与策略训练路径；输入范数全零等边界须明确，不能靠随机数替代后宣传视频能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人工给几个梯度大小，可验权重，却没有执行任何视频生成训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01973">原论文</a> · <a href="../../../../post-training/2610.01973-tvrl/">实现解读</a> · <a href="#qa-7e0532299250133a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpo" data-paper-title="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning LLM 后训练 Georgia Institute of Technology 2026-09-30 用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 segment credit；未读取 gold plan，也未训练 7B Agent。执行 segment credit；未读取 gold plan，也未训练 7B Agent。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agentic RL segment credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SHARPO为什么以成功同组轨迹作为教师上下文？ 组内成功示范提供当前任务可用指导，在环境交互段内比较师生logp，调节该段原GRPO优势。教师信息用于训练信用，不是评测时读取标准计划。 例如同题一条成功路线可提示学生某段行为值得加强，但不直接塞进部署提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-sharpo-de267e69" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f14e021dde614f5f">SHARPO为什么以成功同组轨迹作为教师上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asharpo">SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组内成功示范提供当前任务可用指导，在环境交互段内比较师生logp，调节该段原GRPO优势。教师信息用于训练信用，不是评测时读取标准计划。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同题一条成功路线可提示学生某段行为值得加强，但不直接塞进部署提示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00838">原论文</a> · <a href="../../../../post-training/2610.00838-sharpo/">实现解读</a> · <a href="#qa-f14e021dde614f5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpo" data-paper-title="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning LLM 后训练 Georgia Institute of Technology 2026-09-30 用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 segment credit；未读取 gold plan，也未训练 7B Agent。执行 segment credit；未读取 gold plan，也未训练 7B Agent。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agentic RL segment credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SHARPO借同组成功轨迹重评segment，为什么仍用有界因子缩放原GRPO优势？ 成功轨迹为同一学生前缀提供额外教师上下文，segment内师生log-prob差反映局部支持差异。有界缩放限制这种自蒸馏信号对原优势的放大，不把教师评分直接变成无限新奖励。成功上下文仅用于训练评分，不是给推理Agent展示gold计划。 教学例子：同一失败轨迹中的检索段可能接近成功策略，而汇总段偏差较大；按segment调信用，比整条回答统一放大更细。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-eb132069cbbc6f92">SHARPO借同组成功轨迹重评segment，为什么仍用有界因子缩放原GRPO优势？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asharpo">SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成功轨迹为同一学生前缀提供额外教师上下文，segment内师生log-prob差反映局部支持差异。有界缩放限制这种自蒸馏信号对原优势的放大，不把教师评分直接变成无限新奖励。成功上下文仅用于训练评分，不是给推理Agent展示gold计划。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一失败轨迹中的检索段可能接近成功策略，而汇总段偏差较大；按segment调信用，比整条回答统一放大更细。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00838">原论文</a> · <a href="../../../../post-training/2610.00838-sharpo/">实现解读</a> · <a href="#qa-eb132069cbbc6f92">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpo" data-paper-title="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning LLM 后训练 Georgia Institute of Technology 2026-09-30 用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 segment credit；未读取 gold plan，也未训练 7B Agent。执行 segment credit；未读取 gold plan，也未训练 7B Agent。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agentic RL segment credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SHARPO有界乘法与直接相加教师优势有何差别？ 二倍sigmoid位于零到二之间，缩放保留原优势符号；相加项可能翻转正负。它调整强度而非重新决定终局好坏，零优势也不会凭缩放变非零。 例如原失败段仍为负，只是惩罚程度变化，不会因教师偏好变成正奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a8453c1cebfd958d">SHARPO有界乘法与直接相加教师优势有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asharpo">SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>二倍sigmoid位于零到二之间，缩放保留原优势符号；相加项可能翻转正负。它调整强度而非重新决定终局好坏，零优势也不会凭缩放变非零。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原失败段仍为负，只是惩罚程度变化，不会因教师偏好变成正奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00838">原论文</a> · <a href="../../../../post-training/2610.00838-sharpo/">实现解读</a> · <a href="#qa-a8453c1cebfd958d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpo" data-paper-title="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning LLM 后训练 Georgia Institute of Technology 2026-09-30 用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 segment credit；未读取 gold plan，也未训练 7B Agent。执行 segment credit；未读取 gold plan，也未训练 7B Agent。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agentic RL segment credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SHARPO的segment边界与gold plan访问有什么要求？ 师生差按同一交互段平均后广播，不能混入工具观察或错接分段。当前本地执行段信用，未读取gold plan也未训练7B智能体，不能把固定片段核当完整能力。 例如一轮工具调用和下一轮答复若被拼错，平均差就不再对应原段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c8a64e5d92aa765a">SHARPO的segment边界与gold plan访问有什么要求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asharpo">SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>师生差按同一交互段平均后广播，不能混入工具观察或错接分段。当前本地执行段信用，未读取gold plan也未训练7B智能体，不能把固定片段核当完整能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一轮工具调用和下一轮答复若被拼错，平均差就不再对应原段。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00838">原论文</a> · <a href="../../../../post-training/2610.00838-sharpo/">实现解读</a> · <a href="#qa-c8a64e5d92aa765a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:t2spo" data-paper-title="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning LLM 后训练 Nanjing University 2026-09-30 用历史成功轨迹中的剩余步数训练上下文内距离估计器，预测每个状态距离成功还多远；把相邻状态的距离改善转为步骤优势，与轨迹级奖励共同优化。冻结 TabPFN 避免额外训练 critic，失败轨迹不被误标成接近成功的正样本。 尚未复现完整 LLM＋ALFWorld 训练。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。没有用启发式回归器冒充 TabPFN；尚未复现完整 LLM＋ALFWorld 训练。本地预动作输入是公开合成数值状态，不是冻结文本 encoder；完整 ALFWorld/WebShop rollout、文本编码器和 LLM 参数更新未完成。TabPFN MAE 不是任务成功率；没有 CUDA 完整训练或正式 Evolve 接入。  轨迹到步骤信用分配 强化学习 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 T2SPO为什么用成功轨迹剩余步数估计距离？ 距离提供比终局成败更密集的进度信号，成功历史中的状态与剩余步数可作为支持集，让冻结上下文内预测器评估新状态离成功多远。失败不能伪标为接近成功。 例如一个成功路线中还剩三步的状态，为后续距离预测提供监督例子。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-t2spo-3a6c006a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-140748fa5efbfd50">T2SPO为什么用成功轨迹剩余步数估计距离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3At2spo">T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>距离提供比终局成败更密集的进度信号，成功历史中的状态与剩余步数可作为支持集，让冻结上下文内预测器评估新状态离成功多远。失败不能伪标为接近成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个成功路线中还剩三步的状态，为后续距离预测提供监督例子。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00388">原论文</a> · <a href="../../../../post-training/2610.00388-t2spo/">实现解读</a> · <a href="#qa-140748fa5efbfd50">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:t2spo" data-paper-title="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning LLM 后训练 Nanjing University 2026-09-30 用历史成功轨迹中的剩余步数训练上下文内距离估计器，预测每个状态距离成功还多远；把相邻状态的距离改善转为步骤优势，与轨迹级奖励共同优化。冻结 TabPFN 避免额外训练 critic，失败轨迹不被误标成接近成功的正样本。 尚未复现完整 LLM＋ALFWorld 训练。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。没有用启发式回归器冒充 TabPFN；尚未复现完整 LLM＋ALFWorld 训练。本地预动作输入是公开合成数值状态，不是冻结文本 encoder；完整 ALFWorld/WebShop rollout、文本编码器和 LLM 参数更新未完成。TabPFN MAE 不是任务成功率；没有 CUDA 完整训练或正式 Evolve 接入。  轨迹到步骤信用分配 强化学习 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 T2SPO成功终止把后继距离置零，为什么失败终止却把步骤进展直接置零？ 成功终止确实到达目标，距离归零表示完成；失败结束只是无法继续，若同样当作到达成功，会制造虚假正进展。距离估计来自历史成功支持集，本轮先完成评分再更新历史，避免自我泄漏。时间截断还需按所用GRPO或PPO语义分别处理。 教学例子：代理因工具耗尽而退出，并不意味着离成功只差零步；若把退出统一当作成功终点，最后一个失败动作可能被错误奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-32febe1027d78f23">T2SPO成功终止把后继距离置零，为什么失败终止却把步骤进展直接置零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3At2spo">T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成功终止确实到达目标，距离归零表示完成；失败结束只是无法继续，若同样当作到达成功，会制造虚假正进展。距离估计来自历史成功支持集，本轮先完成评分再更新历史，避免自我泄漏。时间截断还需按所用GRPO或PPO语义分别处理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>代理因工具耗尽而退出，并不意味着离成功只差零步；若把退出统一当作成功终点，最后一个失败动作可能被错误奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00388">原论文</a> · <a href="../../../../post-training/2610.00388-t2spo/">实现解读</a> · <a href="#qa-32febe1027d78f23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:t2spo" data-paper-title="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning LLM 后训练 Nanjing University 2026-09-30 用历史成功轨迹中的剩余步数训练上下文内距离估计器，预测每个状态距离成功还多远；把相邻状态的距离改善转为步骤优势，与轨迹级奖励共同优化。冻结 TabPFN 避免额外训练 critic，失败轨迹不被误标成接近成功的正样本。 尚未复现完整 LLM＋ALFWorld 训练。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。没有用启发式回归器冒充 TabPFN；尚未复现完整 LLM＋ALFWorld 训练。本地预动作输入是公开合成数值状态，不是冻结文本 encoder；完整 ALFWorld/WebShop rollout、文本编码器和 LLM 参数更新未完成。TabPFN MAE 不是任务成功率；没有 CUDA 完整训练或正式 Evolve 接入。  轨迹到步骤信用分配 强化学习 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 距离改善信用与只奖励最终成功有何互补？ 相邻距离变化可指导中间步骤，轨迹奖励仍评价最终结果；预测距离有误时需mask和缩放限制。TabPFN预测误差不是任务成功率，也不能代替真实环境评测。 例如某动作明显接近目标却未终局完成，可得过程线索，但仍需最终验收。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dfa8733b74c8bb46">距离改善信用与只奖励最终成功有何互补？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3At2spo">T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相邻距离变化可指导中间步骤，轨迹奖励仍评价最终结果；预测距离有误时需mask和缩放限制。TabPFN预测误差不是任务成功率，也不能代替真实环境评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某动作明显接近目标却未终局完成，可得过程线索，但仍需最终验收。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00388">原论文</a> · <a href="../../../../post-training/2610.00388-t2spo/">实现解读</a> · <a href="#qa-dfa8733b74c8bb46">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:t2spo" data-paper-title="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning LLM 后训练 Nanjing University 2026-09-30 用历史成功轨迹中的剩余步数训练上下文内距离估计器，预测每个状态距离成功还多远；把相邻状态的距离改善转为步骤优势，与轨迹级奖励共同优化。冻结 TabPFN 避免额外训练 critic，失败轨迹不被误标成接近成功的正样本。 尚未复现完整 LLM＋ALFWorld 训练。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。没有用启发式回归器冒充 TabPFN；尚未复现完整 LLM＋ALFWorld 训练。本地预动作输入是公开合成数值状态，不是冻结文本 encoder；完整 ALFWorld/WebShop rollout、文本编码器和 LLM 参数更新未完成。TabPFN MAE 不是任务成功率；没有 CUDA 完整训练或正式 Evolve 接入。  轨迹到步骤信用分配 强化学习 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 T2SPO本地optimizer=ppo是否已包含完整PPO训练器？ 没有，该开关只改变信用的截断语义，未实现critic与GAE。GRPO对截断信用置零，PPO语义用真实后继预测；支持标准化和SVD仅在历史支持集拟合。 例如切换字符串参数不会自动产生value模型，不能报告PPO能力已接入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1808ae2cbc70dbb5">T2SPO本地optimizer=ppo是否已包含完整PPO训练器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3At2spo">T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，该开关只改变信用的截断语义，未实现critic与GAE。GRPO对截断信用置零，PPO语义用真实后继预测；支持标准化和SVD仅在历史支持集拟合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如切换字符串参数不会自动产生value模型，不能报告PPO能力已接入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00388">原论文</a> · <a href="../../../../post-training/2610.00388-t2spo/">实现解读</a> · <a href="#qa-1808ae2cbc70dbb5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pact" data-paper-title="PACT: From Credit Assignment to Critic Alignment" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="PACT: From Credit Assignment to Critic Alignment LLM 后训练 AllSpark Team 2026-09-22 终局奖励只有一个标量，但 actor 要更新每个生成 token。论文在完整性、前缀一致性和中性三个条件下，刻画 token 的理论信用为相邻前缀的条件期望之差。实际训练无法精确知道这些期望，因此用概率 critic 估计前缀价值，令 token advantage 近似为 R − V(prefix)。论文的关键是顺序：critic 应逼近 actor 更新后的策略，而不是只拟合刚采样时的旧策略。实用版本用当前 token 的概率比 ρ_t，而非整个未来序列的比率乘积； 以真实自由生成轨迹验证 Actor-then-Critic、更新后策略的重要性校正与概率 critic；本地结果不是原论文大模型成绩。这验证了 PACT 的更新次序与损失路径，但没有复现 4B/35B checkpoint、agentic 工具环境、原文训练规模或原文基准成绩；应作为小模型机制证据，不据此宣称 LLM 能力提升。短预算训练中格式命中率仍为零；上述非零 exact accuracy 只有极少数样本，不能解释为稳定的能力改善。本地使用小型 GRU 因果语言模型、独立前缀 critic、无约束 token 自由生成与 exact-answer verifier。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 PACT为什么把token信用联系到前缀价值？ 终局奖励只有一个数，前缀条件期望帮助判断各位置尚有多少可改善空间，实际用R减V近似优势。精确信用有理论条件，学习critic只是可执行近似。 例如同样失败，已很有把握的前缀与本来就困难的前缀可有不同优势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-pact-439c5053" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2bcf3e2654649c91">PACT为什么把token信用联系到前缀价值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apact">PACT: From Credit Assignment to Critic Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AllSpark Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局奖励只有一个数，前缀条件期望帮助判断各位置尚有多少可改善空间，实际用R减V近似优势。精确信用有理论条件，学习critic只是可执行近似。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样失败，已很有把握的前缀与本来就困难的前缀可有不同优势。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.26355">原论文</a> · <a href="../../../../post-training/2609.26355-pact/">实现解读</a> · <a href="#qa-2bcf3e2654649c91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pact" data-paper-title="PACT: From Credit Assignment to Critic Alignment" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="PACT: From Credit Assignment to Critic Alignment LLM 后训练 AllSpark Team 2026-09-22 终局奖励只有一个标量，但 actor 要更新每个生成 token。论文在完整性、前缀一致性和中性三个条件下，刻画 token 的理论信用为相邻前缀的条件期望之差。实际训练无法精确知道这些期望，因此用概率 critic 估计前缀价值，令 token advantage 近似为 R − V(prefix)。论文的关键是顺序：critic 应逼近 actor 更新后的策略，而不是只拟合刚采样时的旧策略。实用版本用当前 token 的概率比 ρ_t，而非整个未来序列的比率乘积； 以真实自由生成轨迹验证 Actor-then-Critic、更新后策略的重要性校正与概率 critic；本地结果不是原论文大模型成绩。这验证了 PACT 的更新次序与损失路径，但没有复现 4B/35B checkpoint、agentic 工具环境、原文训练规模或原文基准成绩；应作为小模型机制证据，不据此宣称 LLM 能力提升。短预算训练中格式命中率仍为零；上述非零 exact accuracy 只有极少数样本，不能解释为稳定的能力改善。本地使用小型 GRU 因果语言模型、独立前缀 critic、无约束 token 自由生成与 exact-answer verifier。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 PACT为什么先更新actor再重算比率训练critic，soft target超过一时能直接clamp吗？ critic应逼近更新后的策略，因此用新旧actor的token概率比校正旧轨迹回报，再拟合对应目标。逐样本的比率乘奖励可能超过一，直接截断会改变目标，不能套用只接收标准概率标签的BCE接口。更新顺序和稳定softplus表达都属于机制。 教学例子：actor已更偏向某个成功动作，critic仍只拟合旧采样分布会滞后；概率比校正用于让旧结果服务新策略价值估计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4512977cc96eb85e">PACT为什么先更新actor再重算比率训练critic，soft target超过一时能直接clamp吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apact">PACT: From Credit Assignment to Critic Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AllSpark Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>critic应逼近更新后的策略，因此用新旧actor的token概率比校正旧轨迹回报，再拟合对应目标。逐样本的比率乘奖励可能超过一，直接截断会改变目标，不能套用只接收标准概率标签的BCE接口。更新顺序和稳定softplus表达都属于机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>actor已更偏向某个成功动作，critic仍只拟合旧采样分布会滞后；概率比校正用于让旧结果服务新策略价值估计。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.26355">原论文</a> · <a href="../../../../post-training/2609.26355-pact/">实现解读</a> · <a href="#qa-4512977cc96eb85e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pact" data-paper-title="PACT: From Credit Assignment to Critic Alignment" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="PACT: From Credit Assignment to Critic Alignment LLM 后训练 AllSpark Team 2026-09-22 终局奖励只有一个标量，但 actor 要更新每个生成 token。论文在完整性、前缀一致性和中性三个条件下，刻画 token 的理论信用为相邻前缀的条件期望之差。实际训练无法精确知道这些期望，因此用概率 critic 估计前缀价值，令 token advantage 近似为 R − V(prefix)。论文的关键是顺序：critic 应逼近 actor 更新后的策略，而不是只拟合刚采样时的旧策略。实用版本用当前 token 的概率比 ρ_t，而非整个未来序列的比率乘积； 以真实自由生成轨迹验证 Actor-then-Critic、更新后策略的重要性校正与概率 critic；本地结果不是原论文大模型成绩。这验证了 PACT 的更新次序与损失路径，但没有复现 4B/35B checkpoint、agentic 工具环境、原文训练规模或原文基准成绩；应作为小模型机制证据，不据此宣称 LLM 能力提升。短预算训练中格式命中率仍为零；上述非零 exact accuracy 只有极少数样本，不能解释为稳定的能力改善。本地使用小型 GRU 因果语言模型、独立前缀 critic、无约束 token 自由生成与 exact-answer verifier。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 PACT先更新actor再训练critic，与只拟合旧策略有什么差别？ critic应跟随更新后策略，因此用新旧actor当前词元比修正目标。该单词元近似不是未来完整续写的重要性乘积，不能据此称精确continuation校正。 例如actor已改变接下来动作，critic仍只背旧回报会落后于当前策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5734fd63ef0bee5c">PACT先更新actor再训练critic，与只拟合旧策略有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apact">PACT: From Credit Assignment to Critic Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AllSpark Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>critic应跟随更新后策略，因此用新旧actor当前词元比修正目标。该单词元近似不是未来完整续写的重要性乘积，不能据此称精确continuation校正。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如actor已改变接下来动作，critic仍只背旧回报会落后于当前策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.26355">原论文</a> · <a href="../../../../post-training/2609.26355-pact/">实现解读</a> · <a href="#qa-5734fd63ef0bee5c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pact" data-paper-title="PACT: From Credit Assignment to Critic Alignment" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="PACT: From Credit Assignment to Critic Alignment LLM 后训练 AllSpark Team 2026-09-22 终局奖励只有一个标量，但 actor 要更新每个生成 token。论文在完整性、前缀一致性和中性三个条件下，刻画 token 的理论信用为相邻前缀的条件期望之差。实际训练无法精确知道这些期望，因此用概率 critic 估计前缀价值，令 token advantage 近似为 R − V(prefix)。论文的关键是顺序：critic 应逼近 actor 更新后的策略，而不是只拟合刚采样时的旧策略。实用版本用当前 token 的概率比 ρ_t，而非整个未来序列的比率乘积； 以真实自由生成轨迹验证 Actor-then-Critic、更新后策略的重要性校正与概率 critic；本地结果不是原论文大模型成绩。这验证了 PACT 的更新次序与损失路径，但没有复现 4B/35B checkpoint、agentic 工具环境、原文训练规模或原文基准成绩；应作为小模型机制证据，不据此宣称 LLM 能力提升。短预算训练中格式命中率仍为零；上述非零 exact accuracy 只有极少数样本，不能解释为稳定的能力改善。本地使用小型 GRU 因果语言模型、独立前缀 critic、无约束 token 自由生成与 exact-answer verifier。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 PACT的ρR大于一时为什么不能塞进普通概率BCE接口？ 软目标可能超一，需按softplus(z)减Yz的规定形式计算，并过滤超界比率。标准API若假定目标在零一可能拒绝或隐改语义；本地少量非零结果不证明稳定能力提升。 例如奖励一乘略大于一的比值，目标自然超过一，并不应偷偷裁回一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9144cf1db5f3c27f">PACT的ρR大于一时为什么不能塞进普通概率BCE接口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apact">PACT: From Credit Assignment to Critic Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AllSpark Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>软目标可能超一，需按softplus(z)减Yz的规定形式计算，并过滤超界比率。标准API若假定目标在零一可能拒绝或隐改语义；本地少量非零结果不证明稳定能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如奖励一乘略大于一的比值，目标自然超过一，并不应偷偷裁回一。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.26355">原论文</a> · <a href="../../../../post-training/2609.26355-pact/">实现解读</a> · <a href="#qa-9144cf1db5f3c27f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tiao" data-paper-title="TIAO: Token Importance-Aware Policy Optimization for Text Summarization" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TIAO: Token Importance-Aware Policy Optimization for Text Summarization LLM 后训练 National University of Defense Technology 2026-09-15 通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TIAO为什么遮蔽源文档来测token依赖？ 摘要应依赖原文，比较遮蔽前后概率可定位更受源证据影响的位置，再调整轨迹与词元信用。依赖性是关联线索，不保证该词事实正确。 例如人名概率在删去相关句后明显变化，比固定连接词更可能依赖原文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-tiao-f57cc707" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1daed1b1b2c11bfc">TIAO为什么遮蔽源文档来测token依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atiao">TIAO: Token Importance-Aware Policy Optimization for Text Summarization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Defense Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>摘要应依赖原文，比较遮蔽前后概率可定位更受源证据影响的位置，再调整轨迹与词元信用。依赖性是关联线索，不保证该词事实正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人名概率在删去相关句后明显变化，比固定连接词更可能依赖原文。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16748">原论文</a> · <a href="../../../../post-training/2609.16748-tiao/">实现解读</a> · <a href="#qa-1daed1b1b2c11bfc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tiao" data-paper-title="TIAO: Token Importance-Aware Policy Optimization for Text Summarization" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TIAO: Token Importance-Aware Policy Optimization for Text Summarization LLM 后训练 National University of Defense Technology 2026-09-15 通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TIAO遮蔽源文档后看token概率变化，为什么这比仅按回答长度分配信用更有针对性？ 摘要中不同token对原文证据的依赖不同，遮蔽前后的概率差提供这种依赖线索，再用于轨迹与token两层信用塑形。长度只能描述多少字，不能说明哪些内容依赖来源。但遮蔽也可能引入分布变化，因此依赖估计不能直接等同事实归因正确性。 教学例子：摘要里的日期依赖原文细节，而连接词可能不依赖；同样长度下，二者不应仅因位置相近就获得完全相同的证据信用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0d4589e1aa50f7cf">TIAO遮蔽源文档后看token概率变化，为什么这比仅按回答长度分配信用更有针对性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atiao">TIAO: Token Importance-Aware Policy Optimization for Text Summarization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Defense Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>摘要中不同token对原文证据的依赖不同，遮蔽前后的概率差提供这种依赖线索，再用于轨迹与token两层信用塑形。长度只能描述多少字，不能说明哪些内容依赖来源。但遮蔽也可能引入分布变化，因此依赖估计不能直接等同事实归因正确性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>摘要里的日期依赖原文细节，而连接词可能不依赖；同样长度下，二者不应仅因位置相近就获得完全相同的证据信用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16748">原论文</a> · <a href="../../../../post-training/2609.16748-tiao/">实现解读</a> · <a href="#qa-0d4589e1aa50f7cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tiao" data-paper-title="TIAO: Token Importance-Aware Policy Optimization for Text Summarization" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TIAO: Token Importance-Aware Policy Optimization for Text Summarization LLM 后训练 National University of Defense Technology 2026-09-15 通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TIAO双尺度信用与只在整篇摘要打分有什么不同？ 整篇分数评价总体质量，词元依赖再分配局部更新，方法同时处理轨迹层与词元层。单有高摘要分不说明每个词都得到适当监督。 例如整篇不错但一个日期幻觉，可需要更局部的调整而非全篇同等强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dc23fe1a47d3797e">TIAO双尺度信用与只在整篇摘要打分有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atiao">TIAO: Token Importance-Aware Policy Optimization for Text Summarization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Defense Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整篇分数评价总体质量，词元依赖再分配局部更新，方法同时处理轨迹层与词元层。单有高摘要分不说明每个词都得到适当监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如整篇不错但一个日期幻觉，可需要更局部的调整而非全篇同等强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16748">原论文</a> · <a href="../../../../post-training/2609.16748-tiao/">实现解读</a> · <a href="#qa-dc23fe1a47d3797e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tiao" data-paper-title="TIAO: Token Importance-Aware Policy Optimization for Text Summarization" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TIAO: Token Importance-Aware Policy Optimization for Text Summarization LLM 后训练 National University of Defense Technology 2026-09-15 通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TIAO的有源和遮蔽评分应使用哪条响应？ 应围绕同一待评分响应及对应前缀比较，否则生成变化会混入遮蔽效应。mask与奖励计算作为训练信号处理，本地依赖核没有训练原文7B模型。 例如有源评摘要A、遮蔽后另生成摘要B，差异不再只来自源信息移除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-57c47c920b15a51d">TIAO的有源和遮蔽评分应使用哪条响应？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atiao">TIAO: Token Importance-Aware Policy Optimization for Text Summarization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Defense Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应围绕同一待评分响应及对应前缀比较，否则生成变化会混入遮蔽效应。mask与奖励计算作为训练信号处理，本地依赖核没有训练原文7B模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如有源评摘要A、遮蔽后另生成摘要B，差异不再只来自源信息移除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16748">原论文</a> · <a href="../../../../post-training/2609.16748-tiao/">实现解读</a> · <a href="#qa-57c47c920b15a51d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spear" data-paper-title="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning LLM 后训练 University of Pittsburgh 2026-08-27 结果奖励过稀，神经 PRM 又昂贵。SPEAR 把教师推理投影为领域符号 milestone，用 LCS-F1 给学生轨迹提供顺序敏感的稠密奖励。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现领域 milestone、顺序对齐与无神经 PRM 的稠密奖励。本地 milestone 使用候选过程/格式轴，不等同论文的自然语言符号抽取器。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.2812，神经 PRM 调用数为 0。  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SPEAR为什么把教师推理转为符号milestone？ 结果奖稀疏，完整神经过程裁判又昂贵；领域符号骨架让学生过程可被顺序对齐，提供稠密进度线索。它依赖抽取规则能保留真正重要推理结构。 例如把证明中的关键等式作为里程碑，而非逐字匹配教师全部措辞。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-spear-64318b6a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4ce49a0d006854c3">SPEAR为什么把教师推理转为符号milestone？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspear">SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pittsburgh</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>结果奖稀疏，完整神经过程裁判又昂贵；领域符号骨架让学生过程可被顺序对齐，提供稠密进度线索。它依赖抽取规则能保留真正重要推理结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把证明中的关键等式作为里程碑，而非逐字匹配教师全部措辞。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26550">原论文</a> · <a href="../../../../post-training/2608.26550-spear/">实现解读</a> · <a href="#qa-4ce49a0d006854c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spear" data-paper-title="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning LLM 后训练 University of Pittsburgh 2026-08-27 结果奖励过稀，神经 PRM 又昂贵。SPEAR 把教师推理投影为领域符号 milestone，用 LCS-F1 给学生轨迹提供顺序敏感的稠密奖励。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现领域 milestone、顺序对齐与无神经 PRM 的稠密奖励。本地 milestone 使用候选过程/格式轴，不等同论文的自然语言符号抽取器。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.2812，神经 PRM 调用数为 0。  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SPEAR为什么用LCS-F1对齐符号milestone，而不只检查两条推理包含相同符号？ 相同步骤集合可能顺序不同，导致推理依赖被破坏。最长公共子序列保留相对顺序，配合精确率和召回率衡量遗漏与冗余，形成比单个终局分数更密集的信号。符号抽取本身仍可能出错，本地候选轴不能冒充原文自然语言抽取器。 教学例子：先代入条件再求解与先写结论再拼条件，可能含相同标记却有不同依赖；顺序敏感对齐可以区分这种结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6186a5ebb210c071">SPEAR为什么用LCS-F1对齐符号milestone，而不只检查两条推理包含相同符号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspear">SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pittsburgh</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同步骤集合可能顺序不同，导致推理依赖被破坏。最长公共子序列保留相对顺序，配合精确率和召回率衡量遗漏与冗余，形成比单个终局分数更密集的信号。符号抽取本身仍可能出错，本地候选轴不能冒充原文自然语言抽取器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先代入条件再求解与先写结论再拼条件，可能含相同标记却有不同依赖；顺序敏感对齐可以区分这种结构。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26550">原论文</a> · <a href="../../../../post-training/2608.26550-spear/">实现解读</a> · <a href="#qa-6186a5ebb210c071">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spear" data-paper-title="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning LLM 后训练 University of Pittsburgh 2026-08-27 结果奖励过稀，神经 PRM 又昂贵。SPEAR 把教师推理投影为领域符号 milestone，用 LCS-F1 给学生轨迹提供顺序敏感的稠密奖励。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现领域 milestone、顺序对齐与无神经 PRM 的稠密奖励。本地 milestone 使用候选过程/格式轴，不等同论文的自然语言符号抽取器。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.2812，神经 PRM 调用数为 0。  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 LCS-F1与无序符号集合重合率有什么差别？ LCS保留顺序，集合重合不管先后；F1同时考虑覆盖和冗余。若学生把关键步骤倒置，无序匹配可能高估过程正确，顺序对齐会给出不同信号。 例如先得到结论再补前提，与按依赖推导，符号相同但顺序价值不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-19016356004de9ab">LCS-F1与无序符号集合重合率有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspear">SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pittsburgh</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>LCS保留顺序，集合重合不管先后；F1同时考虑覆盖和冗余。若学生把关键步骤倒置，无序匹配可能高估过程正确，顺序对齐会给出不同信号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先得到结论再补前提，与按依赖推导，符号相同但顺序价值不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26550">原论文</a> · <a href="../../../../post-training/2608.26550-spear/">实现解读</a> · <a href="#qa-19016356004de9ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spear" data-paper-title="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning LLM 后训练 University of Pittsburgh 2026-08-27 结果奖励过稀，神经 PRM 又昂贵。SPEAR 把教师推理投影为领域符号 milestone，用 LCS-F1 给学生轨迹提供顺序敏感的稠密奖励。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现领域 milestone、顺序对齐与无神经 PRM 的稠密奖励。本地 milestone 使用候选过程/格式轴，不等同论文的自然语言符号抽取器。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.2812，神经 PRM 调用数为 0。  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 本地SPEAR milestone是否实现自然语言符号抽取器？ 没有，本地用候选过程和格式轴模拟里程碑，验证LCS-F1路径。真实教师文本到领域符号仍是独立模块，不能把手工标签的通过当自动抽取能力。 例如直接输入一串已知步骤符号，测试不了模型是否能从长证明抽出它们。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b3521e591526d2b8">本地SPEAR milestone是否实现自然语言符号抽取器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspear">SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pittsburgh</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，本地用候选过程和格式轴模拟里程碑，验证LCS-F1路径。真实教师文本到领域符号仍是独立模块，不能把手工标签的通过当自动抽取能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如直接输入一串已知步骤符号，测试不了模型是否能从长证明抽出它们。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26550">原论文</a> · <a href="../../../../post-training/2608.26550-spear/">实现解读</a> · <a href="#qa-b3521e591526d2b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:v-rubrics" data-paper-title="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning LLM 后训练 S-Lab, Nanyang Technological University 2026-08-26 把参考回答拆成视觉忠实度（VF）、推理一致性（RC）和指令遵循（IF）原子 rubric，并把可定位证据的信用分配到前缀，避免终局标量奖励掩盖局部幻觉。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2188（+75.00%）；只验证多维、prefix-localized candidate credit。  多模态 rubric RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 V-Rubrics为什么把视觉回答质量拆成VF、RC、IF？ 视觉忠实、推理一致与指令遵循可能分别出错，单个总分会掩盖局部问题。原子rubric让可定位证据对应前缀信用，维度分解仍需可靠标注或评价器。 例如图片对象说对但推理跳步，与完全看错图，是不同错误来源。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-v-rubrics-b3920a4a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a0415fcdbddcdc16">V-Rubrics为什么把视觉回答质量拆成VF、RC、IF？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Av-rubrics">V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · S-Lab, Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视觉忠实、推理一致与指令遵循可能分别出错，单个总分会掩盖局部问题。原子rubric让可定位证据对应前缀信用，维度分解仍需可靠标注或评价器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图片对象说对但推理跳步，与完全看错图，是不同错误来源。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25580">原论文</a> · <a href="../../../../post-training/2608.25580-v-rubrics/">实现解读</a> · <a href="#qa-a0415fcdbddcdc16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:v-rubrics" data-paper-title="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning LLM 后训练 S-Lab, Nanyang Technological University 2026-08-26 把参考回答拆成视觉忠实度（VF）、推理一致性（RC）和指令遵循（IF）原子 rubric，并把可定位证据的信用分配到前缀，避免终局标量奖励掩盖局部幻觉。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2188（+75.00%）；只验证多维、prefix-localized candidate credit。  多模态 rubric RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 V-Rubrics为什么把视觉忠实、推理一致和指令遵循分开，而不只给整条回答一个总分？ 回答可能看图正确却推理跳步，也可能推理连贯却编造视觉细节。原子rubric区分这些来源，再把可定位的证据信用关联到前缀，减少终局标量掩盖局部幻觉。维度加权只是目标取舍，不能证明judge标签无误；本地候选轴并非真实视觉证据模型。 教学例子：回答遵守了输出格式，但把图中不存在的物体当作前提；格式分高不能替代视觉忠实度的单独检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f0e27b68376395a6">V-Rubrics为什么把视觉忠实、推理一致和指令遵循分开，而不只给整条回答一个总分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Av-rubrics">V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · S-Lab, Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>回答可能看图正确却推理跳步，也可能推理连贯却编造视觉细节。原子rubric区分这些来源，再把可定位的证据信用关联到前缀，减少终局标量掩盖局部幻觉。维度加权只是目标取舍，不能证明judge标签无误；本地候选轴并非真实视觉证据模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>回答遵守了输出格式，但把图中不存在的物体当作前提；格式分高不能替代视觉忠实度的单独检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25580">原论文</a> · <a href="../../../../post-training/2608.25580-v-rubrics/">实现解读</a> · <a href="#qa-f0e27b68376395a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:v-rubrics" data-paper-title="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning LLM 后训练 S-Lab, Nanyang Technological University 2026-08-26 把参考回答拆成视觉忠实度（VF）、推理一致性（RC）和指令遵循（IF）原子 rubric，并把可定位证据的信用分配到前缀，避免终局标量奖励掩盖局部幻觉。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2188（+75.00%）；只验证多维、prefix-localized candidate credit。  多模态 rubric RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 多维rubric与只看最终答案准确率有什么差别？ 前者允许区分证据、推理与格式，后者可能在答案碰巧正确时漏掉幻觉过程。多维不自动表示更公正，权重和rubric覆盖仍影响结果。 例如最终选项对了，但解释里凭空多出一个物体，结果奖可能看不出来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ccf69661c52bf587">多维rubric与只看最终答案准确率有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Av-rubrics">V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · S-Lab, Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者允许区分证据、推理与格式，后者可能在答案碰巧正确时漏掉幻觉过程。多维不自动表示更公正，权重和rubric覆盖仍影响结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最终选项对了，但解释里凭空多出一个物体，结果奖可能看不出来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25580">原论文</a> · <a href="../../../../post-training/2608.25580-v-rubrics/">实现解读</a> · <a href="#qa-ccf69661c52bf587">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:v-rubrics" data-paper-title="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning LLM 后训练 S-Lab, Nanyang Technological University 2026-08-26 把参考回答拆成视觉忠实度（VF）、推理一致性（RC）和指令遵循（IF）原子 rubric，并把可定位证据的信用分配到前缀，避免终局标量奖励掩盖局部幻觉。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2188（+75.00%）；只验证多维、prefix-localized candidate credit。  多模态 rubric RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 V-Rubrics本地固定维度分数能证明真实视觉判据已运行吗？ 不能。当前公开确定性候选或计划任务只隔离奖励组合和信用路径，没有论文视觉检查点、私有数据及完整评测，不能把固定分数代理当视觉忠实度能力。 例如人为给VF分，再计算总奖，测试的是组合而非自动看图评分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6165dbc62536173d">V-Rubrics本地固定维度分数能证明真实视觉判据已运行吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Av-rubrics">V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · S-Lab, Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前公开确定性候选或计划任务只隔离奖励组合和信用路径，没有论文视觉检查点、私有数据及完整评测，不能把固定分数代理当视觉忠实度能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人为给VF分，再计算总奖，测试的是组合而非自动看图评分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25580">原论文</a> · <a href="../../../../post-training/2608.25580-v-rubrics/">实现解读</a> · <a href="#qa-6165dbc62536173d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:srpo" data-paper-title="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning LLM 后训练 Wuhan University 2026-08-24 长轨迹只给终局 reward 时，很难知道具体哪个 token/动作导致失败。SRPO 让当前模型先根据完整轨迹和环境结果写出简短 reflection patch，再把 patch 拼回原问题；同一个模型在这个特权上下文中充当教师，对学生的 on-policy rollout 给出逐 token 分数。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行反思 patch、reflection-conditioned teacher score 和稠密 advantage；没有把小型策略代理结果写成 Qwen3-8B 训练结果。本地策略代理用 outcome/process reward 构造同方向的反思稠密信用，没有运行 Qwen3-8B、WebShop、ALFWorld、SWE-Bench 或真实 token rollout。  反思式 token 信用 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SRPO为什么在失败后生成reflection patch？ 终局反馈粗，patch把可修正线索转成特权上下文，使同一模型在学生实际前缀上提供稠密指导。它不是直接把整个旧错误轨迹都当作监督。 例如工具报错后归纳应检查参数，教师据此重新评价学生当时的词元。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-srpo-6cb8099c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bc9bdc2d6fcf7dc4">SRPO为什么在失败后生成reflection patch？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asrpo">SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局反馈粗，patch把可修正线索转成特权上下文，使同一模型在学生实际前缀上提供稠密指导。它不是直接把整个旧错误轨迹都当作监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具报错后归纳应检查参数，教师据此重新评价学生当时的词元。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23493">原论文</a> · <a href="../../../../post-training/2608.23493-srpo/">实现解读</a> · <a href="#qa-bc9bdc2d6fcf7dc4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:srpo" data-paper-title="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning LLM 后训练 Wuhan University 2026-08-24 长轨迹只给终局 reward 时，很难知道具体哪个 token/动作导致失败。SRPO 让当前模型先根据完整轨迹和环境结果写出简短 reflection patch，再把 patch 拼回原问题；同一个模型在这个特权上下文中充当教师，对学生的 on-policy rollout 给出逐 token 分数。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行反思 patch、reflection-conditioned teacher score 和稠密 advantage；没有把小型策略代理结果写成 Qwen3-8B 训练结果。本地策略代理用 outcome/process reward 构造同方向的反思稠密信用，没有运行 Qwen3-8B、WebShop、ALFWorld、SWE-Bench 或真实 token rollout。  反思式 token 信用 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SRPO把失败后的reflection patch给同参数教师，为什么学生原始rollout前缀仍要保持不变？ patch是训练时事后得到的特权反馈，用来让教师重新评价学生实际走过的位置。若改写学生前缀或直接把patch给部署学生，就变成另一种采样或推理任务。逐token教师与旧学生log-ratio形成稠密信用，反思文本本身也不是经过独立证明的正确答案。 教学例子：学生先做错一个检索决策，任务结束后才知道遗漏约束；教师可借提醒评分这个旧决策，但不能假装学生当时已经知道。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ceb50c358f897166">SRPO把失败后的reflection patch给同参数教师，为什么学生原始rollout前缀仍要保持不变？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asrpo">SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>patch是训练时事后得到的特权反馈，用来让教师重新评价学生实际走过的位置。若改写学生前缀或直接把patch给部署学生，就变成另一种采样或推理任务。逐token教师与旧学生log-ratio形成稠密信用，反思文本本身也不是经过独立证明的正确答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生先做错一个检索决策，任务结束后才知道遗漏约束；教师可借提醒评分这个旧决策，但不能假装学生当时已经知道。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23493">原论文</a> · <a href="../../../../post-training/2608.23493-srpo/">实现解读</a> · <a href="#qa-ceb50c358f897166">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:srpo" data-paper-title="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning LLM 后训练 Wuhan University 2026-08-24 长轨迹只给终局 reward 时，很难知道具体哪个 token/动作导致失败。SRPO 让当前模型先根据完整轨迹和环境结果写出简短 reflection patch，再把 patch 拼回原问题；同一个模型在这个特权上下文中充当教师，对学生的 on-policy rollout 给出逐 token 分数。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行反思 patch、reflection-conditioned teacher score 和稠密 advantage；没有把小型策略代理结果写成 Qwen3-8B 训练结果。本地策略代理用 outcome/process reward 构造同方向的反思稠密信用，没有运行 Qwen3-8B、WebShop、ALFWorld、SWE-Bench 或真实 token rollout。  反思式 token 信用 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SRPO自反思教师与独立外部教师的区别是什么？ 师生共享模型但条件输入不同，能力差来自额外反馈和patch，而非更大的外部参数。若反思本身错误，同源模型也可能相互强化偏差，不能视为独立验证。 例如同一个人看过结果再点评，信息更多，但不是另一位独立专家。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8963981c3086ad72">SRPO自反思教师与独立外部教师的区别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asrpo">SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>师生共享模型但条件输入不同，能力差来自额外反馈和patch，而非更大的外部参数。若反思本身错误，同源模型也可能相互强化偏差，不能视为独立验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一个人看过结果再点评，信息更多，但不是另一位独立专家。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23493">原论文</a> · <a href="../../../../post-training/2608.23493-srpo/">实现解读</a> · <a href="#qa-8963981c3086ad72">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:srpo" data-paper-title="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning LLM 后训练 Wuhan University 2026-08-24 长轨迹只给终局 reward 时，很难知道具体哪个 token/动作导致失败。SRPO 让当前模型先根据完整轨迹和环境结果写出简短 reflection patch，再把 patch 拼回原问题；同一个模型在这个特权上下文中充当教师，对学生的 on-policy rollout 给出逐 token 分数。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行反思 patch、reflection-conditioned teacher score 和稠密 advantage；没有把小型策略代理结果写成 Qwen3-8B 训练结果。本地策略代理用 outcome/process reward 构造同方向的反思稠密信用，没有运行 Qwen3-8B、WebShop、ALFWorld、SWE-Bench 或真实 token rollout。  反思式 token 信用 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SRPO教师评分是否应沿教师重新生成的理想前缀？ 应沿学生on-policy前缀评分，patch只改变教师条件；奖励差及优势停止梯度。本地用结果过程轴构造同向信用，未真实生成patch或运行大模型工具环境。 例如学生第三步已经偏离，教师仍需评价这个状态，而非悄悄换成正确第三步。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1fbf4e7408760400">SRPO教师评分是否应沿教师重新生成的理想前缀？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asrpo">SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应沿学生on-policy前缀评分，patch只改变教师条件；奖励差及优势停止梯度。本地用结果过程轴构造同向信用，未真实生成patch或运行大模型工具环境。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生第三步已经偏离，教师仍需评价这个状态，而非悄悄换成正确第三步。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23493">原论文</a> · <a href="../../../../post-training/2608.23493-srpo/">实现解读</a> · <a href="#qa-1fbf4e7408760400">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sa-mrpo" data-paper-title="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization LLM 后训练 University of Florida 2026-08-17 逐 reward 维度标准化优势，并依据 batch 饱和度动态把梯度预算转移到尚未掌握的目标。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  多奖励 RL 稳定性 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SA-MRPO为什么关注各奖励的饱和度？ 已经掌握的目标继续占据梯度预算，可能妨碍尚未学会的维度。逐维标准化后按一减饱和度加权，把注意转向剩余学习空间，但依赖饱和指标合理。 例如格式已几乎总满足，训练可多关注仍经常失败的事实检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-sa-mrpo-184fd311" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a0af90db8872ed3b">SA-MRPO为什么关注各奖励的饱和度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asa-mrpo">Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>已经掌握的目标继续占据梯度预算，可能妨碍尚未学会的维度。逐维标准化后按一减饱和度加权，把注意转向剩余学习空间，但依赖饱和指标合理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如格式已几乎总满足，训练可多关注仍经常失败的事实检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16072">原论文</a> · <a href="../../../../post-training/2608.16072-sa-mrpo/">实现解读</a> · <a href="#qa-a0af90db8872ed3b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sa-mrpo" data-paper-title="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization LLM 后训练 University of Florida 2026-08-17 逐 reward 维度标准化优势，并依据 batch 饱和度动态把梯度预算转移到尚未掌握的目标。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  多奖励 RL 稳定性 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SA-MRPO为什么根据奖励饱和度调权，而不一直给所有目标相同权重？ 某些维度已被模型掌握后，继续分配同样更新预算可能挤占尚未掌握的目标。方法逐维标准化优势，再按饱和程度降低已学会目标的权重。饱和必须按明确统计口径估计，不等于高分维度从此永远无用，也不能混淆奖励量纲与真实掌握程度。 教学例子：格式目标几乎总通过，推理正确性仍不稳定；可减少格式维度的相对压力，但仍需监测它是否因训练其他目标而退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-70571048b7377895">SA-MRPO为什么根据奖励饱和度调权，而不一直给所有目标相同权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asa-mrpo">Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>某些维度已被模型掌握后，继续分配同样更新预算可能挤占尚未掌握的目标。方法逐维标准化优势，再按饱和程度降低已学会目标的权重。饱和必须按明确统计口径估计，不等于高分维度从此永远无用，也不能混淆奖励量纲与真实掌握程度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>格式目标几乎总通过，推理正确性仍不稳定；可减少格式维度的相对压力，但仍需监测它是否因训练其他目标而退化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16072">原论文</a> · <a href="../../../../post-training/2608.16072-sa-mrpo/">实现解读</a> · <a href="#qa-70571048b7377895">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sa-mrpo" data-paper-title="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization LLM 后训练 University of Florida 2026-08-17 逐 reward 维度标准化优势，并依据 batch 饱和度动态把梯度预算转移到尚未掌握的目标。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  多奖励 RL 稳定性 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 饱和度重权与固定多奖励权重有何不同？ 固定权重不随学习状态变化，饱和感知根据当前批目标掌握程度调整。它不改变各维度最终重要性定义，也不保证被降权维度永远不会遗忘。 例如某维度暂时学会后少更新，仍需后续监控，不能永久宣布完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-72131cb19fdb4037">饱和度重权与固定多奖励权重有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asa-mrpo">Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定权重不随学习状态变化，饱和感知根据当前批目标掌握程度调整。它不改变各维度最终重要性定义，也不保证被降权维度永远不会遗忘。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某维度暂时学会后少更新，仍需后续监控，不能永久宣布完成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16072">原论文</a> · <a href="../../../../post-training/2608.16072-sa-mrpo/">实现解读</a> · <a href="#qa-72131cb19fdb4037">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sa-mrpo" data-paper-title="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization LLM 后训练 University of Florida 2026-08-17 逐 reward 维度标准化优势，并依据 batch 饱和度动态把梯度预算转移到尚未掌握的目标。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  多奖励 RL 稳定性 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SA-MRPO实现可把所有reward合并后只算一个饱和度吗？ 那会丢掉逐维转移预算的定义。需分别维护每维均值、方差与饱和度，再汇总；本地候选策略只验证公式，未复刻论文检查点训练。 例如正确性低而格式高，合成一个平均饱和度无法指出该加强哪一维。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1d3549ed36ff2513">SA-MRPO实现可把所有reward合并后只算一个饱和度吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asa-mrpo">Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>那会丢掉逐维转移预算的定义。需分别维护每维均值、方差与饱和度，再汇总；本地候选策略只验证公式，未复刻论文检查点训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如正确性低而格式高，合成一个平均饱和度无法指出该加强哪一维。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16072">原论文</a> · <a href="../../../../post-training/2608.16072-sa-mrpo/">实现解读</a> · <a href="#qa-1d3549ed36ff2513">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rubric-dropout" data-paper-title="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL LLM 后训练 Scale AI 2026-08-12 每个 rollout group 共享随机丢弃的 rubric 子集，使策略无法持续利用固定 judge proxy。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL reward hacking LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Rubric Dropout为什么随机隐藏部分评价条款？ 固定条款可能被策略持续利用形成奖励投机，随机子集让它难以只依赖某个固定代理。被隐藏并不表示条款不重要，而是在训练中改变可见奖励组合。 例如某条容易靠套话拿分，不能保证每组都靠它获得总奖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-rubric-dropout-0c8d1da7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5a48a08bd29cde14">Rubric Dropout为什么随机隐藏部分评价条款？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arubric-dropout">Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Scale AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定条款可能被策略持续利用形成奖励投机，随机子集让它难以只依赖某个固定代理。被隐藏并不表示条款不重要，而是在训练中改变可见奖励组合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某条容易靠套话拿分，不能保证每组都靠它获得总奖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11669">原论文</a> · <a href="../../../../post-training/2608.11669-rubric-dropout/">实现解读</a> · <a href="#qa-5a48a08bd29cde14">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rubric-dropout" data-paper-title="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL LLM 后训练 Scale AI 2026-08-12 每个 rollout group 共享随机丢弃的 rubric 子集，使策略无法持续利用固定 judge proxy。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL reward hacking LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Rubric Dropout为什么让同一个rollout组共享丢弃的rubric子集？ 同组响应需要在可比标准下形成相对奖励，共享子集能避免每个回答因随机评价规则不同而被误排序。跨组变化的rubric又使策略难以持续利用固定评分捷径。随机丢弃只是缓和特定reward hacking机制，不能保证余下标准可靠或主任务不会受损。 教学例子：比较两份答案时都暂时去掉“简短”标准，比一份按简短评分、另一份不按它评分，更能保持相对奖励可比。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ea048f226344f026">Rubric Dropout为什么让同一个rollout组共享丢弃的rubric子集？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arubric-dropout">Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Scale AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同组响应需要在可比标准下形成相对奖励，共享子集能避免每个回答因随机评价规则不同而被误排序。跨组变化的rubric又使策略难以持续利用固定评分捷径。随机丢弃只是缓和特定reward hacking机制，不能保证余下标准可靠或主任务不会受损。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>比较两份答案时都暂时去掉“简短”标准，比一份按简短评分、另一份不按它评分，更能保持相对奖励可比。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11669">原论文</a> · <a href="../../../../post-training/2608.11669-rubric-dropout/">实现解读</a> · <a href="#qa-ea048f226344f026">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rubric-dropout" data-paper-title="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL LLM 后训练 Scale AI 2026-08-12 每个 rollout group 共享随机丢弃的 rubric 子集，使策略无法持续利用固定 judge proxy。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL reward hacking LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 组内共享dropout与每条回答独立丢条款有什么差别？ 共享子集让同题组的回答在相同标准下比较，独立子集会把评分标准差异混进相对优势。随机化需在组级处理，而非每响应各自随机。 例如A只评格式、B只评正确性，它们分数差就难解释为回答质量差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c21118c94c319de5">组内共享dropout与每条回答独立丢条款有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arubric-dropout">Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Scale AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享子集让同题组的回答在相同标准下比较，独立子集会把评分标准差异混进相对优势。随机化需在组级处理，而非每响应各自随机。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如A只评格式、B只评正确性，它们分数差就难解释为回答质量差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11669">原论文</a> · <a href="../../../../post-training/2608.11669-rubric-dropout/">实现解读</a> · <a href="#qa-c21118c94c319de5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rubric-dropout" data-paper-title="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL LLM 后训练 Scale AI 2026-08-12 每个 rollout group 共享随机丢弃的 rubric 子集，使策略无法持续利用固定 judge proxy。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL reward hacking LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Rubric Dropout的mask应该何时采样并怎样留存？ 每个rollout group采一份条款mask并固定用于组内奖励，记录随机种子便于复核。不能按哪条回答得分更好再选mask；本地未运行真实rubric judge。 例如先看结果再隐藏难达标条款，会把随机机制变成事后刷分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b2ac7c4da469d607">Rubric Dropout的mask应该何时采样并怎样留存？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arubric-dropout">Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Scale AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个rollout group采一份条款mask并固定用于组内奖励，记录随机种子便于复核。不能按哪条回答得分更好再选mask；本地未运行真实rubric judge。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先看结果再隐藏难达标条款，会把随机机制变成事后刷分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11669">原论文</a> · <a href="../../../../post-training/2608.11669-rubric-dropout/">实现解读</a> · <a href="#qa-b2ac7c4da469d607">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rrc" data-paper-title="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction LLM 后训练 Northeastern University 2026-08-06 主题：生成式奖励模型。生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。RRC 用组内自竞争排序和少量 anchor 排序构造中心化 reward。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的生成式奖励模型算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  生成式奖励模型 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 RRC为什么更愿意从相对排序构造生成式RM奖励？ 生成式评价器擅长解释和比较，独立标量未必校准。组内排序与少量anchor提供相对位置，再构成中心化奖励供策略学习，保留其比较优势。 例如裁判能稳定说两篇哪篇好，却不一定给所有题一致的十分制分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-rrc-3d32cfb6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-aab7c26674050fe8">RRC为什么更愿意从相对排序构造生成式RM奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arrc">RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成式评价器擅长解释和比较，独立标量未必校准。组内排序与少量anchor提供相对位置，再构成中心化奖励供策略学习，保留其比较优势。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如裁判能稳定说两篇哪篇好，却不一定给所有题一致的十分制分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06310">原论文</a> · <a href="../../../../post-training/2608.06310-rrc/">实现解读</a> · <a href="#qa-aab7c26674050fe8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rrc" data-paper-title="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction LLM 后训练 Northeastern University 2026-08-06 主题：生成式奖励模型。生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。RRC 用组内自竞争排序和少量 anchor 排序构造中心化 reward。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的生成式奖励模型算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  生成式奖励模型 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 RRC为什么把生成式奖励模型的组内排名与anchor排名结合，而不要求它逐条报绝对分数？ 生成式judge可能更擅长比较哪条更好，而绝对数值尺度不稳定。组内自竞争给相对位置，少量anchor提供跨组参照，再构造中心化奖励。排名仍依赖候选集合和judge质量，不能把相对第一解释为绝对正确，也不等于已经运行原文昂贵评审系统。 教学例子：两组答案各自都有第一名，但整体质量可能不同；加入固定参照可帮助判断两组的“第一”是否处在相近水平。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-efbd610af1123aeb">RRC为什么把生成式奖励模型的组内排名与anchor排名结合，而不要求它逐条报绝对分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arrc">RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成式judge可能更擅长比较哪条更好，而绝对数值尺度不稳定。组内自竞争给相对位置，少量anchor提供跨组参照，再构造中心化奖励。排名仍依赖候选集合和judge质量，不能把相对第一解释为绝对正确，也不等于已经运行原文昂贵评审系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组答案各自都有第一名，但整体质量可能不同；加入固定参照可帮助判断两组的“第一”是否处在相近水平。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06310">原论文</a> · <a href="../../../../post-training/2608.06310-rrc/">实现解读</a> · <a href="#qa-efbd610af1123aeb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rrc" data-paper-title="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction LLM 后训练 Northeastern University 2026-08-06 主题：生成式奖励模型。生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。RRC 用组内自竞争排序和少量 anchor 排序构造中心化 reward。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的生成式奖励模型算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  生成式奖励模型 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 组内self-competition与anchor排序分别提供什么信息？ 组内比较区分当前候选，anchor提供跨组参照，缓解只有局部名次无法解释绝对水平的问题。两部分需明确权重，不能把名次当真实等距质量。 例如一组全差也总有第一，anchor能提醒它虽第一仍不理想。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a6fd8d121f808e69">组内self-competition与anchor排序分别提供什么信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arrc">RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组内比较区分当前候选，anchor提供跨组参照，缓解只有局部名次无法解释绝对水平的问题。两部分需明确权重，不能把名次当真实等距质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一组全差也总有第一，anchor能提醒它虽第一仍不理想。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06310">原论文</a> · <a href="../../../../post-training/2608.06310-rrc/">实现解读</a> · <a href="#qa-a6fd8d121f808e69">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rrc" data-paper-title="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction LLM 后训练 Northeastern University 2026-08-06 主题：生成式奖励模型。生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。RRC 用组内自竞争排序和少量 anchor 排序构造中心化 reward。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的生成式奖励模型算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  生成式奖励模型 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 RRC名次转奖时为什么要检查组大小和排名方向？ 公式含K减一，单样本组无法按同一尺度计算；高名次究竟代表好还是差必须统一。实际judge尚未本地运行，注册候选发现不等于完整能力集成。 例如把名次一当最优却使用相反公式，会把最好回答给予最低奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-404cabbf88bd9a1e">RRC名次转奖时为什么要检查组大小和排名方向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arrc">RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式含K减一，单样本组无法按同一尺度计算；高名次究竟代表好还是差必须统一。实际judge尚未本地运行，注册候选发现不等于完整能力集成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把名次一当最优却使用相反公式，会把最好回答给予最低奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06310">原论文</a> · <a href="../../../../post-training/2608.06310-rrc/">实现解读</a> · <a href="#qa-404cabbf88bd9a1e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adrs" data-paper-title="ADRS" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="ADRS LLM 后训练 University of Science and Technology of China 2026-08-04 privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 step 内中心化、return association、TVA gate 与原生 REINFORCE advantage 注入。  回报相关奖励塑形 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 ADRS为什么不直接相信特权教师的高置信？ 额外技能或信息可让教师更确定，却未必提高真实回报。方法观察同一步教师分数与已实现回报的相关，再门控稠密信号，避免无效自信主导训练。 例如教师很喜欢某工具用法，但实际任务常失败，就不应无条件强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-adrs-2cc77780" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-60e05ad660e88f18">ADRS为什么不直接相信特权教师的高置信？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadrs">ADRS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>额外技能或信息可让教师更确定，却未必提高真实回报。方法观察同一步教师分数与已实现回报的相关，再门控稠密信号，避免无效自信主导训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师很喜欢某工具用法，但实际任务常失败，就不应无条件强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03223">原论文</a> · <a href="../../../../post-training/2608.03223-adrs/">实现解读</a> · <a href="#qa-60e05ad660e88f18">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adrs" data-paper-title="ADRS" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="ADRS LLM 后训练 University of Science and Technology of China 2026-08-04 privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 step 内中心化、return association、TVA gate 与原生 REINFORCE advantage 注入。  回报相关奖励塑形 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 ADRS为什么先检查教师置信与实际回报的相关性，再使用教师token信号？ 特权教师越自信不必然意味着任务越成功，直接灌入可能放大错误。ADRS在交互步内标准化教师分数，用与实际回报的正相关形成门控，再进入原奖励到优势路径。负相关不应被当正向帮助，推理时也不依赖训练专属技能或结果信息。 教学例子：某一步教师总偏爱流畅但无效的工具调用，而真实回报更低；相关性门控应限制这种自信信号进入策略更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e51841f6db85c131">ADRS为什么先检查教师置信与实际回报的相关性，再使用教师token信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadrs">ADRS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>特权教师越自信不必然意味着任务越成功，直接灌入可能放大错误。ADRS在交互步内标准化教师分数，用与实际回报的正相关形成门控，再进入原奖励到优势路径。负相关不应被当正向帮助，推理时也不依赖训练专属技能或结果信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某一步教师总偏爱流畅但无效的工具调用，而真实回报更低；相关性门控应限制这种自信信号进入策略更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03223">原论文</a> · <a href="../../../../post-training/2608.03223-adrs/">实现解读</a> · <a href="#qa-e51841f6db85c131">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adrs" data-paper-title="ADRS" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="ADRS LLM 后训练 University of Science and Technology of China 2026-08-04 privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 step 内中心化、return association、TVA gate 与原生 REINFORCE advantage 注入。  回报相关奖励塑形 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TVA相关门控与固定蒸馏系数有何不同？ 固定系数始终信任教师，门控只保留与回报正相关的部分。相关性是批次统计而非因果保证，也不能在测试时借标准答案估一份最有利gate。 例如教师分数与成功无关时，正部相关可使额外指导减弱。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a89350278459cda5">TVA相关门控与固定蒸馏系数有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadrs">ADRS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定系数始终信任教师，门控只保留与回报正相关的部分。相关性是批次统计而非因果保证，也不能在测试时借标准答案估一份最有利gate。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师分数与成功无关时，正部相关可使额外指导减弱。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03223">原论文</a> · <a href="../../../../post-training/2608.03223-adrs/">实现解读</a> · <a href="#qa-a89350278459cda5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adrs" data-paper-title="ADRS" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="ADRS LLM 后训练 University of Science and Technology of China 2026-08-04 privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 step 内中心化、return association、TVA gate 与原生 REINFORCE advantage 注入。  回报相关奖励塑形 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 ADRS标准化是在整条轨迹还是同一交互step内？ 按交互step对教师分数标准化，再与跨轨迹回报计算相应相关，写入宿主reward-to-advantage路径。不能把局部z分直接视作独立终局正确标签。 例如第二轮工具调用的教师信号，应与同轮其他轨迹比较，而非混入所有轮次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-29657d9aa8a6b890">ADRS标准化是在整条轨迹还是同一交互step内？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadrs">ADRS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按交互step对教师分数标准化，再与跨轨迹回报计算相应相关，写入宿主reward-to-advantage路径。不能把局部z分直接视作独立终局正确标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第二轮工具调用的教师信号，应与同轮其他轨迹比较，而非混入所有轮次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03223">原论文</a> · <a href="../../../../post-training/2608.03223-adrs/">实现解读</a> · <a href="#qa-29657d9aa8a6b890">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:serpo" data-paper-title="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning LLM 后训练 Authors did not disclose affiliation 2026-07-29 让 Good–Normal–Bad 响应档案、query-specific rubrics 和 actor 策略形成三方闭环自进化。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL 测试时自进化 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SERPO为什么维护Good–Normal–Bad响应档案？ 档案为当前问题的rubric和策略更新提供多质量参照，评估标准与actor共同演化，而非只永久保留最高分文本。分类仍取决于评价机制可靠性。 例如中等回答可暴露差距，坏回答帮助标准指出需要避免的模式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-serpo-1bbe9fff" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c2866c0ae1401306">SERPO为什么维护Good–Normal–Bad响应档案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aserpo">SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>档案为当前问题的rubric和策略更新提供多质量参照，评估标准与actor共同演化，而非只永久保留最高分文本。分类仍取决于评价机制可靠性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如中等回答可暴露差距，坏回答帮助标准指出需要避免的模式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26873">原论文</a> · <a href="../../../../post-training/2607.26873-serpo/">实现解读</a> · <a href="#qa-c2866c0ae1401306">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:serpo" data-paper-title="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning LLM 后训练 Authors did not disclose affiliation 2026-07-29 让 Good–Normal–Bad 响应档案、query-specific rubrics 和 actor 策略形成三方闭环自进化。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL 测试时自进化 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SERPO同时更新响应档案、rubric和actor，为什么必须区分这三者的作用？ Good–Normal–Bad档案提供经验比较，题目特定rubric决定当轮评价标准，actor才负责生成行为。三方闭环允许标准随策略改变，但也可能互相强化偏差。更新档案不等于训练模型，生成新rubric也不证明质量提高；需要独立留出评估避免自评自证。 教学例子：旧档案只收录短答案，rubric逐渐偏爱简短，actor随之缩短；三者彼此一致仍可能同时忽略任务事实正确性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-40eccd1b65b34ba5">SERPO同时更新响应档案、rubric和actor，为什么必须区分这三者的作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aserpo">SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Good–Normal–Bad档案提供经验比较，题目特定rubric决定当轮评价标准，actor才负责生成行为。三方闭环允许标准随策略改变，但也可能互相强化偏差。更新档案不等于训练模型，生成新rubric也不证明质量提高；需要独立留出评估避免自评自证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旧档案只收录短答案，rubric逐渐偏爱简短，actor随之缩短；三者彼此一致仍可能同时忽略任务事实正确性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26873">原论文</a> · <a href="../../../../post-training/2607.26873-serpo/">实现解读</a> · <a href="#qa-40eccd1b65b34ba5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:serpo" data-paper-title="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning LLM 后训练 Authors did not disclose affiliation 2026-07-29 让 Good–Normal–Bad 响应档案、query-specific rubrics 和 actor 策略形成三方闭环自进化。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL 测试时自进化 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SERPO与固定rubric下反复RL有什么不同？ 固定标准可能随着策略进步失去区分力，SERPO同时更新查询相关rubric和档案。更多可变环节也带来漂移与自强化风险，不能仅看自评分上升证明能力。 例如策略学会旧条款后，新标准应区分新的难负例，而非永远重复基础检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-54db0361417a9679">SERPO与固定rubric下反复RL有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aserpo">SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定标准可能随着策略进步失去区分力，SERPO同时更新查询相关rubric和档案。更多可变环节也带来漂移与自强化风险，不能仅看自评分上升证明能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如策略学会旧条款后，新标准应区分新的难负例，而非永远重复基础检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26873">原论文</a> · <a href="../../../../post-training/2607.26873-serpo/">实现解读</a> · <a href="#qa-54db0361417a9679">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:serpo" data-paper-title="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning LLM 后训练 Authors did not disclose affiliation 2026-07-29 让 Good–Normal–Bad 响应档案、query-specific rubrics 和 actor 策略形成三方闭环自进化。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL 测试时自进化 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SERPO的三方状态需要怎样按轮次追踪？ 应记录生成响应、形成档案、更新rubric和actor的先后及版本，防止用后来标准倒填旧奖励。本地候选闭环未包含真实开放生成和模型judge的完整流程。 例如本轮评分用哪个rubric版本必须可复核，否则无法解释策略更新来源。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eb6638f64a00a344">SERPO的三方状态需要怎样按轮次追踪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aserpo">SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应记录生成响应、形成档案、更新rubric和actor的先后及版本，防止用后来标准倒填旧奖励。本地候选闭环未包含真实开放生成和模型judge的完整流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如本轮评分用哪个rubric版本必须可复核，否则无法解释策略更新来源。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26873">原论文</a> · <a href="../../../../post-training/2607.26873-serpo/">实现解读</a> · <a href="#qa-eb6638f64a00a344">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cort" data-paper-title="CoRT" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CoRT LLM 后训练 ByteDance internship 2026-07-28 对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。候选动作特征代理真实 token 序列；没有开放式生成、rubric judge 或大模型参数更新。在 GSM8K candidate-policy 上执行 rubric/criteria-free 两次反事实重放、归一化 token 权重和带符号 advantage 更新。  Token-level credit assignment LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CoRT为什么对同一回答做有无criteria的重放？ 保持响应不变，条件差使词元似然变化反映rubric信息与位置关联，再重分配响应级优势。它尝试回答奖励应作用在哪，而不只是再给整篇加分。 例如格式条款影响括号位置的预测，可让该位置获得不同信用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-cort-3a4a9a75" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-930c953e3f0bce85">CoRT为什么对同一回答做有无criteria的重放？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acort">CoRT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance internship</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>保持响应不变，条件差使词元似然变化反映rubric信息与位置关联，再重分配响应级优势。它尝试回答奖励应作用在哪，而不只是再给整篇加分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如格式条款影响括号位置的预测，可让该位置获得不同信用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25659">原论文</a> · <a href="../../../../post-training/2607.25659-cort/">实现解读</a> · <a href="#qa-930c953e3f0bce85">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cort" data-paper-title="CoRT" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CoRT LLM 后训练 ByteDance internship 2026-07-28 对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。候选动作特征代理真实 token 序列；没有开放式生成、rubric judge 或大模型参数更新。在 GSM8K candidate-policy 上执行 rubric/criteria-free 两次反事实重放、归一化 token 权重和带符号 advantage 更新。  Token-level credit assignment LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CoRT为什么在有无rubric的上下文中重放同一响应，而不是各自重新生成后比较？ 重放同一前缀和token能把似然差更多归于rubric条件变化；重新生成会同时改变轨迹，难以定位哪些位置受标准影响。差异用于重分配原响应级优势，而非把评分文本直接输入部署学生。反事实上下文也可能产生偏差，不能把权重等同真实因果贡献。 教学例子：同一句答案在加入“需引用来源”后，引用位置概率变化较大；若另一边重新生成整段，差异就不只来自评价条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-771f392e93e7712c">CoRT为什么在有无rubric的上下文中重放同一响应，而不是各自重新生成后比较？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acort">CoRT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance internship</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重放同一前缀和token能把似然差更多归于rubric条件变化；重新生成会同时改变轨迹，难以定位哪些位置受标准影响。差异用于重分配原响应级优势，而非把评分文本直接输入部署学生。反事实上下文也可能产生偏差，不能把权重等同真实因果贡献。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一句答案在加入“需引用来源”后，引用位置概率变化较大；若另一边重新生成整段，差异就不只来自评价条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25659">原论文</a> · <a href="../../../../post-training/2607.25659-cort/">实现解读</a> · <a href="#qa-771f392e93e7712c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cort" data-paper-title="CoRT" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CoRT LLM 后训练 ByteDance internship 2026-07-28 对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。候选动作特征代理真实 token 序列；没有开放式生成、rubric judge 或大模型参数更新。在 GSM8K candidate-policy 上执行 rubric/criteria-free 两次反事实重放、归一化 token 权重和带符号 advantage 更新。  Token-level credit assignment LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CoRT反事实重放与直接按attention大小分配有什么差别？ 重放比较评价条件改变后的概率，attention只是一次前向的信息权重；二者不等价，也都不直接证明因果正确性。不能用随意注意力图替代规定的似然对照。 例如某词注意力大，却在移除criteria后概率不变，两种信号会不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-10c4f02fc797746e">CoRT反事实重放与直接按attention大小分配有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acort">CoRT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance internship</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重放比较评价条件改变后的概率，attention只是一次前向的信息权重；二者不等价，也都不直接证明因果正确性。不能用随意注意力图替代规定的似然对照。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某词注意力大，却在移除criteria后概率不变，两种信号会不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25659">原论文</a> · <a href="../../../../post-training/2607.25659-cort/">实现解读</a> · <a href="#qa-10c4f02fc797746e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cort" data-paper-title="CoRT" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CoRT LLM 后训练 ByteDance internship 2026-07-28 对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。候选动作特征代理真实 token 序列；没有开放式生成、rubric judge 或大模型参数更新。在 GSM8K candidate-policy 上执行 rubric/criteria-free 两次反事实重放、归一化 token 权重和带符号 advantage 更新。  Token-level credit assignment LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CoRT两次评分为什么必须对齐同一token与前缀？ 否则差异会混入生成内容变化，无法归因于criteria移除。归一后的权重用于固定优势，原学生采样不应见特权rubric；本地候选特征不等于真实逐词元重放。 例如带条款评A句、不带条款评B句，差值已经不是局部条件对照。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9bee9b91adbf24e5">CoRT两次评分为什么必须对齐同一token与前缀？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acort">CoRT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance internship</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>否则差异会混入生成内容变化，无法归因于criteria移除。归一后的权重用于固定优势，原学生采样不应见特权rubric；本地候选特征不等于真实逐词元重放。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如带条款评A句、不带条款评B句，差值已经不是局部条件对照。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25659">原论文</a> · <a href="../../../../post-training/2607.25659-cort/">实现解读</a> · <a href="#qa-9bee9b91adbf24e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dynamic-rubric" data-paper-title="Co-Evolving LLM Evaluators and Policies via DynamicRubric" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Co-Evolving LLM Evaluators and Policies via DynamicRubric LLM 后训练 WeChat / Tencent 2026-07-22 固定 judge 或固定 rubric 会在策略模型进步后失去区分力。DynamicRubric 根据当前 prompt 和一组候选回答动态生成评估维度与权重，用 discriminability 目标寻找能区分当代 hard negatives 的标准，用 anchor 目标限制评估器漂移，再让 evaluator 和 policy 多轮协同进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行动态 rubric 和多轮共进化；Qwen3 与生产 judge 规模未复刻。公开 Alpaca 回答与确定性截断/重排候选构成可审计偏好集；代码实际执行 response-set conditioned 权重生成、四项 binary rubric、discriminability/anchor 双目标和 policy-induced hard-negative 共进化。  post-training reward-model evaluator co-evolution LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 DynamicRubric为什么看当前候选集合生成标准？ 策略进步后旧标准可能全满足，新的hard negatives需要更细区分。动态维度与权重利用当前差异，anchor限制评价器漂移，不意味着评价标准可以任意事后改变。 例如旧格式条款人人通过后，应寻找仍能分开好坏回答的证据维度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-dynamic-rubric-5fe56c96" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0ec541e2997598ca">DynamicRubric为什么看当前候选集合生成标准？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adynamic-rubric">Co-Evolving LLM Evaluators and Policies via DynamicRubric</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略进步后旧标准可能全满足，新的hard negatives需要更细区分。动态维度与权重利用当前差异，anchor限制评价器漂移，不意味着评价标准可以任意事后改变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧格式条款人人通过后，应寻找仍能分开好坏回答的证据维度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20083">原论文</a> · <a href="../../../../reproductions/2607.20083-dynamic-rubric/">实现解读</a> · <a href="#qa-0ec541e2997598ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dynamic-rubric" data-paper-title="Co-Evolving LLM Evaluators and Policies via DynamicRubric" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Co-Evolving LLM Evaluators and Policies via DynamicRubric LLM 后训练 WeChat / Tencent 2026-07-22 固定 judge 或固定 rubric 会在策略模型进步后失去区分力。DynamicRubric 根据当前 prompt 和一组候选回答动态生成评估维度与权重，用 discriminability 目标寻找能区分当代 hard negatives 的标准，用 anchor 目标限制评估器漂移，再让 evaluator 和 policy 多轮协同进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行动态 rubric 和多轮共进化；Qwen3 与生产 judge 规模未复刻。公开 Alpaca 回答与确定性截断/重排候选构成可审计偏好集；代码实际执行 response-set conditioned 权重生成、四项 binary rubric、discriminability/anchor 双目标和 policy-induced hard-negative 共进化。  post-training reward-model evaluator co-evolution LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 DynamicRubric为什么既要求区分当前hard negatives，又用anchor限制评估器漂移？ 固定标准可能随着策略进步失去区分力，动态维度和权重帮助识别新难例；若只追求可区分，评估器也可能学到任意风格捷径。anchor提供相对稳定的参照，约束评价标准改变。共同进化不等于客观真值同步改善，仍需独立任务验证。 教学例子：所有回答都已格式正确，旧格式rubric难再区分；新增标准若只偏爱更长措辞，也需被锚点评价约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-59f9cc11b48a7651">DynamicRubric为什么既要求区分当前hard negatives，又用anchor限制评估器漂移？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adynamic-rubric">Co-Evolving LLM Evaluators and Policies via DynamicRubric</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定标准可能随着策略进步失去区分力，动态维度和权重帮助识别新难例；若只追求可区分，评估器也可能学到任意风格捷径。anchor提供相对稳定的参照，约束评价标准改变。共同进化不等于客观真值同步改善，仍需独立任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>所有回答都已格式正确，旧格式rubric难再区分；新增标准若只偏爱更长措辞，也需被锚点评价约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20083">原论文</a> · <a href="../../../../reproductions/2607.20083-dynamic-rubric/">实现解读</a> · <a href="#qa-59f9cc11b48a7651">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dynamic-rubric" data-paper-title="Co-Evolving LLM Evaluators and Policies via DynamicRubric" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Co-Evolving LLM Evaluators and Policies via DynamicRubric LLM 后训练 WeChat / Tencent 2026-07-22 固定 judge 或固定 rubric 会在策略模型进步后失去区分力。DynamicRubric 根据当前 prompt 和一组候选回答动态生成评估维度与权重，用 discriminability 目标寻找能区分当代 hard negatives 的标准，用 anchor 目标限制评估器漂移，再让 evaluator 和 policy 多轮协同进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行动态 rubric 和多轮共进化；Qwen3 与生产 judge 规模未复刻。公开 Alpaca 回答与确定性截断/重排候选构成可审计偏好集；代码实际执行 response-set conditioned 权重生成、四项 binary rubric、discriminability/anchor 双目标和 policy-induced hard-negative 共进化。  post-training reward-model evaluator co-evolution LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 discriminability目标与anchor目标会怎样拉扯？ 区分目标推动评价器对当前难样本敏感，anchor保留原参考标准避免随策略共谋。只追区分可能奖励无关差异，只追anchor又可能停留旧尺度，需要明确权衡。 例如区分回答长短很容易，但若偏离真实质量，anchor应起限制作用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-78a5fcd1bb4f3dc8">discriminability目标与anchor目标会怎样拉扯？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adynamic-rubric">Co-Evolving LLM Evaluators and Policies via DynamicRubric</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>区分目标推动评价器对当前难样本敏感，anchor保留原参考标准避免随策略共谋。只追区分可能奖励无关差异，只追anchor又可能停留旧尺度，需要明确权衡。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如区分回答长短很容易，但若偏离真实质量，anchor应起限制作用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20083">原论文</a> · <a href="../../../../reproductions/2607.20083-dynamic-rubric/">实现解读</a> · <a href="#qa-78a5fcd1bb4f3dc8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dynamic-rubric" data-paper-title="Co-Evolving LLM Evaluators and Policies via DynamicRubric" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Co-Evolving LLM Evaluators and Policies via DynamicRubric LLM 后训练 WeChat / Tencent 2026-07-22 固定 judge 或固定 rubric 会在策略模型进步后失去区分力。DynamicRubric 根据当前 prompt 和一组候选回答动态生成评估维度与权重，用 discriminability 目标寻找能区分当代 hard negatives 的标准，用 anchor 目标限制评估器漂移，再让 evaluator 和 policy 多轮协同进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行动态 rubric 和多轮共进化；Qwen3 与生产 judge 规模未复刻。公开 Alpaca 回答与确定性截断/重排候选构成可审计偏好集；代码实际执行 response-set conditioned 权重生成、四项 binary rubric、discriminability/anchor 双目标和 policy-induced hard-negative 共进化。  post-training reward-model evaluator co-evolution LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 DynamicRubric权重为什么要绑定prompt和候选版本？ 评分函数依赖两者，换候选可能产生新标准。训练记录需保存所用rubric及anchor版本，不能给不同组套用未声明的新权重后继续比较原奖励。 例如同题两轮候选难点不同，得分变化可能来自标准变化而非策略本身。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7573cde7b2242058">DynamicRubric权重为什么要绑定prompt和候选版本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adynamic-rubric">Co-Evolving LLM Evaluators and Policies via DynamicRubric</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>评分函数依赖两者，换候选可能产生新标准。训练记录需保存所用rubric及anchor版本，不能给不同组套用未声明的新权重后继续比较原奖励。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同题两轮候选难点不同，得分变化可能来自标准变化而非策略本身。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20083">原论文</a> · <a href="../../../../reproductions/2607.20083-dynamic-rubric/">实现解读</a> · <a href="#qa-7573cde7b2242058">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tcr" data-paper-title="TCR" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TCR LLM 后训练 论文未列机构 2026-07-22 只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。 保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；过程 verifier 是可控信号，不等同于论文的真实模型推理评审器。当前不包含真实自由生成、模型生成 checklist 或论文规模训练。结果只支持残差过程奖励机制在候选策略上的有效性，不能作为对论文五模型实验的数值复刻。本地 checklist verifier 为候选推理生成可控噪声过程得分；  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TCR为什么把过程分数减去outcome的EMA？ 过程与结果评分可能重复奖励同一成功，残差试图突出尚未由结果解释的思考增益，再与原结果合并。EMA反映训练状态，不是逐题真值。 例如答对本来已得分，不能把同一个成功又包装成许多过程分重复强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-tcr-a5ef9cee" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ba053d62fb8e7cba">TCR为什么把过程分数减去outcome的EMA？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atcr">TCR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>过程与结果评分可能重复奖励同一成功，残差试图突出尚未由结果解释的思考增益，再与原结果合并。EMA反映训练状态，不是逐题真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如答对本来已得分，不能把同一个成功又包装成许多过程分重复强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19824">原论文</a> · <a href="../../../../post-training/2607.19824-tcr/">实现解读</a> · <a href="#qa-ba053d62fb8e7cba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tcr" data-paper-title="TCR" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TCR LLM 后训练 论文未列机构 2026-07-22 只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。 保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；过程 verifier 是可控信号，不等同于论文的真实模型推理评审器。当前不包含真实自由生成、模型生成 checklist 或论文规模训练。结果只支持残差过程奖励机制在候选策略上的有效性，不能作为对论文五模型实验的数值复刻。本地 checklist verifier 为候选推理生成可控噪声过程得分；  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TCR为什么从过程奖励里减去outcome的滑动基线，而不直接把两项相加？ 过程分与最终正确性常高度相关，直接相加可能把同一个成功信号重复奖励。残差项试图保留结果尚未解释的思考增益，并随训练状态更新参照。它依赖checklist质量和基线口径，不意味着过程残差必是真实推理质量，本地候选验证也不能外推完整模型。 教学例子：答对的回答几乎总获得高过程分，简单求和会重复计分；关注超出通常结果水平的过程改善，才有额外信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-28193c59a175f590">TCR为什么从过程奖励里减去outcome的滑动基线，而不直接把两项相加？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atcr">TCR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>过程分与最终正确性常高度相关，直接相加可能把同一个成功信号重复奖励。残差项试图保留结果尚未解释的思考增益，并随训练状态更新参照。它依赖checklist质量和基线口径，不意味着过程残差必是真实推理质量，本地候选验证也不能外推完整模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>答对的回答几乎总获得高过程分，简单求和会重复计分；关注超出通常结果水平的过程改善，才有额外信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19824">原论文</a> · <a href="../../../../post-training/2607.19824-tcr/">实现解读</a> · <a href="#qa-28193c59a175f590">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tcr" data-paper-title="TCR" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TCR LLM 后训练 论文未列机构 2026-07-22 只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。 保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；过程 verifier 是可控信号，不等同于论文的真实模型推理评审器。当前不包含真实自由生成、模型生成 checklist 或论文规模训练。结果只支持残差过程奖励机制在候选策略上的有效性，不能作为对论文五模型实验的数值复刻。本地 checklist verifier 为候选推理生成可控噪声过程得分；  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TCR残差与简单把过程奖加到结果奖有什么不同？ 直接相加持续累积两个来源，残差扣去动态结果基线，降低重复贡献。它不是精确统计去相关证明，也不保证过程裁判没有独立偏差。 例如结果整体已提升，基线升高会减少同等过程分的额外信用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-871611a87be6887c">TCR残差与简单把过程奖加到结果奖有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atcr">TCR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接相加持续累积两个来源，残差扣去动态结果基线，降低重复贡献。它不是精确统计去相关证明，也不保证过程裁判没有独立偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如结果整体已提升，基线升高会减少同等过程分的额外信用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19824">原论文</a> · <a href="../../../../post-training/2607.19824-tcr/">实现解读</a> · <a href="#qa-871611a87be6887c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tcr" data-paper-title="TCR" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TCR LLM 后训练 论文未列机构 2026-07-22 只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。 保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；过程 verifier 是可控信号，不等同于论文的真实模型推理评审器。当前不包含真实自由生成、模型生成 checklist 或论文规模训练。结果只支持残差过程奖励机制在候选策略上的有效性，不能作为对论文五模型实验的数值复刻。本地 checklist verifier 为候选推理生成可控噪声过程得分；  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TCR本地是否会调用模型生成样本级checklist？ 不会，当前候选策略只验证残差过程奖励计算，未包含真实checklist生成与自由文本训练。EMA需按训练顺序更新，不能由测试整体成绩反向设置。 例如给定一张手工清单并算奖，不能说明自动清单质量已验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-742d03a7a9c6d3b5">TCR本地是否会调用模型生成样本级checklist？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atcr">TCR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不会，当前候选策略只验证残差过程奖励计算，未包含真实checklist生成与自由文本训练。EMA需按训练顺序更新，不能由测试整体成绩反向设置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给定一张手工清单并算奖，不能说明自动清单质量已验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19824">原论文</a> · <a href="../../../../post-training/2607.19824-tcr/">实现解读</a> · <a href="#qa-742d03a7a9c6d3b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:taco" data-paper-title="TACO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TACO LLM 后训练 Johns Hopkins University 2026-07-08 整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作而非逐 token CoT，无法复刻论文的上下文 tail-risk predictor，只验证信用校准方向。以 rollout 概率的 surprisal 代理 tail risk，正 advantage 的 tail 样本会被连续降权，负 advantage 不会被 mask。  Token 信用校准 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TACO为什么认为正确回答也可能含不该强化的token？ 终局正确只验证结论，过程里仍可有偶然或不合理词元。统一正优势会一起提升它们，tail risk用于平滑减弱这些位置的正信用，避免正向污染。 例如最终算对但中间夹了错误理由，不应把整段都无差别当范文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-taco-d0adf0d1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c59506c22db1e018">TACO为什么认为正确回答也可能含不该强化的token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ataco">TACO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johns Hopkins University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局正确只验证结论，过程里仍可有偶然或不合理词元。统一正优势会一起提升它们，tail risk用于平滑减弱这些位置的正信用，避免正向污染。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最终算对但中间夹了错误理由，不应把整段都无差别当范文。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.07976">原论文</a> · <a href="../../../../post-training/2607.07976-taco/">实现解读</a> · <a href="#qa-c59506c22db1e018">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:taco" data-paper-title="TACO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TACO LLM 后训练 Johns Hopkins University 2026-07-08 整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作而非逐 token CoT，无法复刻论文的上下文 tail-risk predictor，只验证信用校准方向。以 rollout 概率的 surprisal 代理 tail risk，正 advantage 的 tail 样本会被连续降权，负 advantage 不会被 mask。  Token 信用校准 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TACO为什么只降低高tail-risk token的正信用，而不把负信用一起减弱？ 正确整句可能夹有不合理的低概率步骤，统一正优势会把它们也强化。TACO平滑削弱这类位置的正信用，同时保留负信用，避免对坏轨迹的抑制也被一并取消。tail risk依赖局部上下文，不是凡低概率就错误，本地也未复现真实token风险预测器。 教学例子：答案碰巧正确，但中间有一次无根据猜测；可减少对猜测的奖励，而当整体失败时，不应顺便免除它的负向反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0598c1bb5aa61a76">TACO为什么只降低高tail-risk token的正信用，而不把负信用一起减弱？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ataco">TACO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johns Hopkins University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确整句可能夹有不合理的低概率步骤，统一正优势会把它们也强化。TACO平滑削弱这类位置的正信用，同时保留负信用，避免对坏轨迹的抑制也被一并取消。tail risk依赖局部上下文，不是凡低概率就错误，本地也未复现真实token风险预测器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>答案碰巧正确，但中间有一次无根据猜测；可减少对猜测的奖励，而当整体失败时，不应顺便免除它的负向反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.07976">原论文</a> · <a href="../../../../post-training/2607.07976-taco/">实现解读</a> · <a href="#qa-0598c1bb5aa61a76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:taco" data-paper-title="TACO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TACO LLM 后训练 Johns Hopkins University 2026-07-08 整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作而非逐 token CoT，无法复刻论文的上下文 tail-risk predictor，只验证信用校准方向。以 rollout 概率的 surprisal 代理 tail risk，正 advantage 的 tail 样本会被连续降权，负 advantage 不会被 mask。  Token 信用校准 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TACO对正负优势采取相同缩放吗？ 不相同。只降低高风险词元的正信用，非正优势保持，让失败学习信号不因tail风险被削弱。与双向都乘权重的方法有不同目标语义。 例如错误回答中的稀有词仍保留原惩罚，不能因风险高反而替它减罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3393248b5a7d48c9">TACO对正负优势采取相同缩放吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ataco">TACO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johns Hopkins University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不相同。只降低高风险词元的正信用，非正优势保持，让失败学习信号不因tail风险被削弱。与双向都乘权重的方法有不同目标语义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如错误回答中的稀有词仍保留原惩罚，不能因风险高反而替它减罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.07976">原论文</a> · <a href="../../../../post-training/2607.07976-taco/">实现解读</a> · <a href="#qa-3393248b5a7d48c9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:taco" data-paper-title="TACO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TACO LLM 后训练 Johns Hopkins University 2026-07-08 整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作而非逐 token CoT，无法复刻论文的上下文 tail-risk predictor，只验证信用校准方向。以 rollout 概率的 surprisal 代理 tail risk，正 advantage 的 tail 样本会被连续降权，负 advantage 不会被 mask。  Token 信用校准 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 本地TACO是否复现了真实上下文tail-risk predictor？ 没有，候选动作只验证信用校准方向；逐词元长CoT预测器不在当前实现。权重应在零与一之间且平滑，不可直接把所有低概率位置一刀切删除。 例如人工给风险标签能验证分支，但没有证明模型自动识别不合理token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5ae3e76c30e78f7d">本地TACO是否复现了真实上下文tail-risk predictor？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ataco">TACO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johns Hopkins University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，候选动作只验证信用校准方向；逐词元长CoT预测器不在当前实现。权重应在零与一之间且平滑，不可直接把所有低概率位置一刀切删除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人工给风险标签能验证分支，但没有证明模型自动识别不合理token。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.07976">原论文</a> · <a href="../../../../post-training/2607.07976-taco/">实现解读</a> · <a href="#qa-5ae3e76c30e78f7d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:intuitor" data-paper-title="INTUITOR" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="INTUITOR LLM 后训练 University of California, Berkeley 2025-05-26 以每个生成前缀下的全词表 next-token 分布计算，再沿回答长度平均，作为 intrinsic self-certainty reward。方向是均匀分布到策略分布，并非策略的负熵；高置信度也不等于答案一定正确。 它既没有原文的逐 token 全词表计算，也使用了相反方向的 KL，因此仅为候选奖励更新诊断，尚未复现 Intuitor 的定义性 self-certainty。本地为候选分布机制诊断。本地为候选分布机制诊断。当前算子没有实现原文逐 token、全词表的 self-certainty；现有 mini-suite 不能作为该定义性奖励或原论文推理能力的验证。当前 p0_20260808.py 的 intuitor 分支以采样候选的 log p + log N 作为奖励，诊断量 intrinsic_kl_to_uniform 则是。  自置信奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 INTUITOR不使用外部verifier时，奖励从哪里来？ 从每个生成前缀的完整下一词分布计算自确定性，再沿回答平均。它是内部学习信号而非正确标签，高置信仍可能稳定地错，需要独立任务评估。 例如模型分布很尖但算术结论错，内部奖高不代表验算通过。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-intuitor-7b64d1c3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-74312e0a24ed0414">INTUITOR不使用外部verifier时，奖励从哪里来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aintuitor">INTUITOR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>从每个生成前缀的完整下一词分布计算自确定性，再沿回答平均。它是内部学习信号而非正确标签，高置信仍可能稳定地错，需要独立任务评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型分布很尖但算术结论错，内部奖高不代表验算通过。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.19590">原论文</a> · <a href="../../../../post-training/2505.19590-intuitor/">实现解读</a> · <a href="#qa-74312e0a24ed0414">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:intuitor" data-paper-title="INTUITOR" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="INTUITOR LLM 后训练 University of California, Berkeley 2025-05-26 以每个生成前缀下的全词表 next-token 分布计算，再沿回答长度平均，作为 intrinsic self-certainty reward。方向是均匀分布到策略分布，并非策略的负熵；高置信度也不等于答案一定正确。 它既没有原文的逐 token 全词表计算，也使用了相反方向的 KL，因此仅为候选奖励更新诊断，尚未复现 Intuitor 的定义性 self-certainty。本地为候选分布机制诊断。本地为候选分布机制诊断。当前算子没有实现原文逐 token、全词表的 self-certainty；现有 mini-suite 不能作为该定义性奖励或原论文推理能力的验证。当前 p0_20260808.py 的 intuitor 分支以采样候选的 log p + log N 作为奖励，诊断量 intrinsic_kl_to_uniform 则是。  自置信奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 INTUITOR的self-certainty能直接换成负熵吗，KL方向为什么重要？ 原文self-certainty使用均匀分布到下一词分布的KL，即KL(U||p)，与KL(p||U)或负熵不同，对全词表低概率区域的敏感性也不同。本地采样候选log-ratio是另一种诊断，不能当成原文token级实现。内部置信提供学习线索，不意味着答案已经正确。 教学例子：两个分布最高概率相近，但一个给其他词极小概率；不同KL方向会以不同方式放大这种尾部差异，不能随意互换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-601f1127c7c740bf">INTUITOR的self-certainty能直接换成负熵吗，KL方向为什么重要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aintuitor">INTUITOR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文self-certainty使用均匀分布到下一词分布的KL，即KL(U||p)，与KL(p||U)或负熵不同，对全词表低概率区域的敏感性也不同。本地采样候选log-ratio是另一种诊断，不能当成原文token级实现。内部置信提供学习线索，不意味着答案已经正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个分布最高概率相近，但一个给其他词极小概率；不同KL方向会以不同方式放大这种尾部差异，不能随意互换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.19590">原论文</a> · <a href="../../../../post-training/2505.19590-intuitor/">实现解读</a> · <a href="#qa-601f1127c7c740bf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:intuitor" data-paper-title="INTUITOR" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="INTUITOR LLM 后训练 University of California, Berkeley 2025-05-26 以每个生成前缀下的全词表 next-token 分布计算，再沿回答长度平均，作为 intrinsic self-certainty reward。方向是均匀分布到策略分布，并非策略的负熵；高置信度也不等于答案一定正确。 它既没有原文的逐 token 全词表计算，也使用了相反方向的 KL，因此仅为候选奖励更新诊断，尚未复现 Intuitor 的定义性 self-certainty。本地为候选分布机制诊断。本地为候选分布机制诊断。当前算子没有实现原文逐 token、全词表的 self-certainty；现有 mini-suite 不能作为该定义性奖励或原论文推理能力的验证。当前 p0_20260808.py 的 intuitor 分支以采样候选的 log p + log N 作为奖励，诊断量 intrinsic_kl_to_uniform 则是。  自置信奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 INTUITOR的内在KL与训练reference KL能合并成一项吗？ 不能。内在KL从均匀分布到当前下一词分布衡量确定性，reference KL约束策略漂移，参照和作用都不同。把内在奖直接当正则会改变训练目标。 例如一项鼓励形成明确分布，另一项限制偏离旧模型，可能方向并不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-353bedaefa0b55ce">INTUITOR的内在KL与训练reference KL能合并成一项吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aintuitor">INTUITOR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。内在KL从均匀分布到当前下一词分布衡量确定性，reference KL约束策略漂移，参照和作用都不同。把内在奖直接当正则会改变训练目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一项鼓励形成明确分布，另一项限制偏离旧模型，可能方向并不一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.19590">原论文</a> · <a href="../../../../post-training/2505.19590-intuitor/">实现解读</a> · <a href="#qa-353bedaefa0b55ce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:intuitor" data-paper-title="INTUITOR" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="INTUITOR LLM 后训练 University of California, Berkeley 2025-05-26 以每个生成前缀下的全词表 next-token 分布计算，再沿回答长度平均，作为 intrinsic self-certainty reward。方向是均匀分布到策略分布，并非策略的负熵；高置信度也不等于答案一定正确。 它既没有原文的逐 token 全词表计算，也使用了相反方向的 KL，因此仅为候选奖励更新诊断，尚未复现 Intuitor 的定义性 self-certainty。本地为候选分布机制诊断。本地为候选分布机制诊断。当前算子没有实现原文逐 token、全词表的 self-certainty；现有 mini-suite 不能作为该定义性奖励或原论文推理能力的验证。当前 p0_20260808.py 的 intuitor 分支以采样候选的 log p + log N 作为奖励，诊断量 intrinsic_kl_to_uniform 则是。  自置信奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 当前intuitor源码是否实现了原文全词表self-certainty？ 没有。采样候选logp加logN作为奖励，诊断还是相反方向KL(p||U)，缺少逐词元全词表KL(U||p)。历史指标应保留诊断身份，不能因README公式已修就宣称源码升级。 例如改正文档方向不会自动改变训练分支，测试候选奖励仍是另一对象。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-48559647056aa759">当前intuitor源码是否实现了原文全词表self-certainty？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aintuitor">INTUITOR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。采样候选logp加logN作为奖励，诊断还是相反方向KL(p||U)，缺少逐词元全词表KL(U||p)。历史指标应保留诊断身份，不能因README公式已修就宣称源码升级。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如改正文档方向不会自动改变训练分支，测试候选奖励仍是另一对象。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.19590">原论文</a> · <a href="../../../../post-training/2505.19590-intuitor/">实现解读</a> · <a href="#qa-48559647056aa759">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:scar-shapley-credit" data-paper-title="SCAR: Shapley Credit Assignment for More Efficient RLHF" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SCAR: Shapley Credit Assignment for More Efficient RLHF LLM 后训练 McGill University 2025-05-26 原文Sec.3.2–3.4 Eq.3–6：外部冻结RM对原顺序、未入选位置填空格的文本coalition评分，v(empty)=0；Shapley必须保留负贡献，span credit只给该span末token。完整论文用自适应分段和SHAP/Owen近似。这里只保真实现N&lt;=10的完整coalition精确式及gamma=1的奖励散布；不把未指定解析器、Owen层次结构或合成RM冒充原系统。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 exact_shapley 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与信用分配 Shapley token/span credit LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SCAR为什么考虑文本span组合的边际贡献？ 一个片段的价值依赖其他片段是否存在，Shapley对不同组合的增益加权，尝试分配终局奖励。贡献可以为负，不能把所有出现过的片段都视为有益。 例如一段解释只有与前提一起出现才有价值，单独评分可能误判其作用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-scar-shapley-credit-01c57925" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4ac7a70be0008147">SCAR为什么考虑文本span组合的边际贡献？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ascar-shapley-credit">SCAR: Shapley Credit Assignment for More Efficient RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · McGill University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个片段的价值依赖其他片段是否存在，Shapley对不同组合的增益加权，尝试分配终局奖励。贡献可以为负，不能把所有出现过的片段都视为有益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一段解释只有与前提一起出现才有价值，单独评分可能误判其作用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.20417v1">原论文</a> · <a href="../../../../post-training/2505.20417-scar-shapley-credit/">实现解读</a> · <a href="#qa-4ac7a70be0008147">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:scar-shapley-credit" data-paper-title="SCAR: Shapley Credit Assignment for More Efficient RLHF" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SCAR: Shapley Credit Assignment for More Efficient RLHF LLM 后训练 McGill University 2025-05-26 原文Sec.3.2–3.4 Eq.3–6：外部冻结RM对原顺序、未入选位置填空格的文本coalition评分，v(empty)=0；Shapley必须保留负贡献，span credit只给该span末token。完整论文用自适应分段和SHAP/Owen近似。这里只保真实现N&lt;=10的完整coalition精确式及gamma=1的奖励散布；不把未指定解析器、Owen层次结构或合成RM冒充原系统。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 exact_shapley 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与信用分配 Shapley token/span credit LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SCAR为什么保留负Shapley贡献，并只把span信用放在该段末token？ 某段文字可能降低冻结奖励模型对整体的评分，负贡献是合作价值分解的一部分，截零会破坏总量关系。span末token是其信用落点，与原顺序coalition构造共同定义奖励散布。总奖励等价还有折扣条件，局部精确枚举不能冒充大规模Owen近似或完整RLHF。 教学例子：一个多余段落引入矛盾，加入它使整体价值下降；若把这段负贡献清零，其他段落的信用总和就不再对应原奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-933b9e934b9cdf0b">SCAR为什么保留负Shapley贡献，并只把span信用放在该段末token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ascar-shapley-credit">SCAR: Shapley Credit Assignment for More Efficient RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · McGill University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>某段文字可能降低冻结奖励模型对整体的评分，负贡献是合作价值分解的一部分，截零会破坏总量关系。span末token是其信用落点，与原顺序coalition构造共同定义奖励散布。总奖励等价还有折扣条件，局部精确枚举不能冒充大规模Owen近似或完整RLHF。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个多余段落引入矛盾，加入它使整体价值下降；若把这段负贡献清零，其他段落的信用总和就不再对应原奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.20417v1">原论文</a> · <a href="../../../../post-training/2505.20417-scar-shapley-credit/">实现解读</a> · <a href="#qa-933b9e934b9cdf0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:scar-shapley-credit" data-paper-title="SCAR: Shapley Credit Assignment for More Efficient RLHF" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SCAR: Shapley Credit Assignment for More Efficient RLHF LLM 后训练 McGill University 2025-05-26 原文Sec.3.2–3.4 Eq.3–6：外部冻结RM对原顺序、未入选位置填空格的文本coalition评分，v(empty)=0；Shapley必须保留负贡献，span credit只给该span末token。完整论文用自适应分段和SHAP/Owen近似。这里只保真实现N&lt;=10的完整coalition精确式及gamma=1的奖励散布；不把未指定解析器、Owen层次结构或合成RM冒充原系统。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 exact_shapley 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与信用分配 Shapley token/span credit LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 精确Shapley组件与论文SHAP/Owen大流程有什么边界？ 完整枚举成本指数增长，本地只接受小规模完整值表；原方法还有自适应分段和近似层次结构，不能把小枚举通过当成这些模块已实现。 例如三个span可枚举全部组合，长回答几十段就不是同一计算规模。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-616c8387b8bbd255">精确Shapley组件与论文SHAP/Owen大流程有什么边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ascar-shapley-credit">SCAR: Shapley Credit Assignment for More Efficient RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · McGill University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整枚举成本指数增长，本地只接受小规模完整值表；原方法还有自适应分段和近似层次结构，不能把小枚举通过当成这些模块已实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三个span可枚举全部组合，长回答几十段就不是同一计算规模。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.20417v1">原论文</a> · <a href="../../../../post-training/2505.20417-scar-shapley-credit/">实现解读</a> · <a href="#qa-616c8387b8bbd255">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:scar-shapley-credit" data-paper-title="SCAR: Shapley Credit Assignment for More Efficient RLHF" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SCAR: Shapley Credit Assignment for More Efficient RLHF LLM 后训练 McGill University 2025-05-26 原文Sec.3.2–3.4 Eq.3–6：外部冻结RM对原顺序、未入选位置填空格的文本coalition评分，v(empty)=0；Shapley必须保留负贡献，span credit只给该span末token。完整论文用自适应分段和SHAP/Owen近似。这里只保真实现N&lt;=10的完整coalition精确式及gamma=1的奖励散布；不把未指定解析器、Owen层次结构或合成RM冒充原系统。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 exact_shapley 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与信用分配 Shapley token/span credit LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SCAR为什么把span credit放在末token，且保留空位顺序？ 外部RM按原顺序评分，未入选位置填空格；信用按规定落到span末位置。负值不截断，空集合价值为零，总奖守恒只承诺相应γ为一的条件，不能随意推广。 例如删掉中间段后把两端拼成新句，会改变原先定义的coalition文本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a9863037678e5668">SCAR为什么把span credit放在末token，且保留空位顺序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ascar-shapley-credit">SCAR: Shapley Credit Assignment for More Efficient RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · McGill University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>外部RM按原顺序评分，未入选位置填空格；信用按规定落到span末位置。负值不截断，空集合价值为零，总奖守恒只承诺相应γ为一的条件，不能随意推广。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删掉中间段后把两端拼成新句，会改变原先定义的coalition文本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.20417v1">原论文</a> · <a href="../../../../post-training/2505.20417-scar-shapley-credit/">实现解读</a> · <a href="#qa-a9863037678e5668">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:math-shepherd" data-paper-title="Math-Shepherd" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Math-Shepherd LLM 后训练 Peking University 2023-12-14 从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自动过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Math-Shepherd怎样无需人工逐步标注得到step信号？ 从某中间步骤多次续写，用最终答案正确的比例估计该状态的可达成功率，再训练过程验证器。标签来自采样和终局校验，不等同人工判断每句话逻辑是否正确。 例如一个步骤之后多数续写能解对，可为该前缀提供较高成功估计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-math-shepherd-cc3174ec" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4aa9a43e201b22c1">Math-Shepherd怎样无需人工逐步标注得到step信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amath-shepherd">Math-Shepherd</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>从某中间步骤多次续写，用最终答案正确的比例估计该状态的可达成功率，再训练过程验证器。标签来自采样和终局校验，不等同人工判断每句话逻辑是否正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个步骤之后多数续写能解对，可为该前缀提供较高成功估计。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.08935">原论文</a> · <a href="../../../../post-training/2312.08935-math-shepherd/">实现解读</a> · <a href="#qa-4aa9a43e201b22c1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:math-shepherd" data-paper-title="Math-Shepherd" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Math-Shepherd LLM 后训练 Peking University 2023-12-14 从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自动过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Math-Shepherd从中间步骤续写成功率造标签，为什么它不是对该步骤正确性的直接人工判定？ 续写衡量在给定策略和预算下从该前缀继续成功的可能性，受到后续求解能力影响。正确前缀也可能因续写差而得低分，错误前缀还可能被后续纠正。因此自动步骤标签是一种可达性信号，需要与人工正确性区分；金标只属于训练标注或独立评分侧。 教学例子：前两步都正确，模型却总在最后算错；从第二步续写的成功率低，并不能单凭这一点判第二步本身错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-162d99ef25d3753e">Math-Shepherd从中间步骤续写成功率造标签，为什么它不是对该步骤正确性的直接人工判定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amath-shepherd">Math-Shepherd</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>续写衡量在给定策略和预算下从该前缀继续成功的可能性，受到后续求解能力影响。正确前缀也可能因续写差而得低分，错误前缀还可能被后续纠正。因此自动步骤标签是一种可达性信号，需要与人工正确性区分；金标只属于训练标注或独立评分侧。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>前两步都正确，模型却总在最后算错；从第二步续写的成功率低，并不能单凭这一点判第二步本身错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.08935">原论文</a> · <a href="../../../../post-training/2312.08935-math-shepherd/">实现解读</a> · <a href="#qa-162d99ef25d3753e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:math-shepherd" data-paper-title="Math-Shepherd" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Math-Shepherd LLM 后训练 Peking University 2023-12-14 从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自动过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 续写成功率与步骤本身的绝对正确性有什么差别？ 后续模型可能修复错误，也可能从正确步骤继续犯错，因此估计混合了当前状态与续写策略能力。它是过程监督线索，不能直接作逻辑证明。 例如某步写错但后续常能纠正，较高续写成功不说明该错步应被原样模仿。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a1b3f74d41607794">续写成功率与步骤本身的绝对正确性有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amath-shepherd">Math-Shepherd</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后续模型可能修复错误，也可能从正确步骤继续犯错，因此估计混合了当前状态与续写策略能力。它是过程监督线索，不能直接作逻辑证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某步写错但后续常能纠正，较高续写成功不说明该错步应被原样模仿。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.08935">原论文</a> · <a href="../../../../post-training/2312.08935-math-shepherd/">实现解读</a> · <a href="#qa-a1b3f74d41607794">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:math-shepherd" data-paper-title="Math-Shepherd" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Math-Shepherd LLM 后训练 Peking University 2023-12-14 从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自动过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 构造Math-Shepherd训练标签时gold能给生成模型看吗？ 标准答案只供终局校验，不进入续写策略输入；续写从对应前缀真实采样，不能用已知答案直接构造路径。当前本地机制没有完整大模型数据生成与PRM训练规模。 例如评分器知道结果为某数，不代表续写提示也能附上这个数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-92344e3f0c9b1409">构造Math-Shepherd训练标签时gold能给生成模型看吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amath-shepherd">Math-Shepherd</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>标准答案只供终局校验，不进入续写策略输入；续写从对应前缀真实采样，不能用已知答案直接构造路径。当前本地机制没有完整大模型数据生成与PRM训练规模。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如评分器知道结果为某数，不代表续写提示也能附上这个数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.08935">原论文</a> · <a href="../../../../post-training/2312.08935-math-shepherd/">实现解读</a> · <a href="#qa-92344e3f0c9b1409">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:process-supervision" data-paper-title="Let&#x27;s Verify Step by Step" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Let&#x27;s Verify Step by Step LLM 后训练 OpenAI 2023-05-31 逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5781（+146.67%）；奖励、KL、长度和候选预算一致。  过程监督 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 过程监督为什么需要逐步标签而非仅最终结果？ 终局失败不能定位哪个推理步骤出错，过程标签提供更局部的学习与筛选信号。它需要额外标注或可靠过程评价，不能由最终对错机械复制到所有步骤。 例如前两步正确、第三步错，整题失败不应把前两步都标错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-process-supervision-e0dd1357" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-db9edb2d592cf144">过程监督为什么需要逐步标签而非仅最终结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprocess-supervision">Let&#x27;s Verify Step by Step</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局失败不能定位哪个推理步骤出错，过程标签提供更局部的学习与筛选信号。它需要额外标注或可靠过程评价，不能由最终对错机械复制到所有步骤。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前两步正确、第三步错，整题失败不应把前两步都标错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.20050">原论文</a> · <a href="../../../../post-training/2305.20050-process-supervision/">实现解读</a> · <a href="#qa-db9edb2d592cf144">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:process-supervision" data-paper-title="Let&#x27;s Verify Step by Step" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Let&#x27;s Verify Step by Step LLM 后训练 OpenAI 2023-05-31 逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5781（+146.67%）；奖励、KL、长度和候选预算一致。  过程监督 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Process Supervision为什么优先标注不确定步骤，而不只标最终答案是否正确？ 终局对错无法定位最先出现的错误，逐步标签能给奖励模型更细的监督。主动选择高不确定步骤把标注预算用在当前难分的位置，但不确定性并非错误概率的万能替身。还需控制候选与评测预算，本地机制夹具不代表已重建完整过程标注数据集。 教学例子：一份推导末尾错了，复核重点可放在模型最犹豫的关键变换，而不是重复标注已经非常明确的格式步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7c928a3ae66cbf1b">Process Supervision为什么优先标注不确定步骤，而不只标最终答案是否正确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprocess-supervision">Let&#x27;s Verify Step by Step</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局对错无法定位最先出现的错误，逐步标签能给奖励模型更细的监督。主动选择高不确定步骤把标注预算用在当前难分的位置，但不确定性并非错误概率的万能替身。还需控制候选与评测预算，本地机制夹具不代表已重建完整过程标注数据集。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一份推导末尾错了，复核重点可放在模型最犹豫的关键变换，而不是重复标注已经非常明确的格式步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.20050">原论文</a> · <a href="../../../../post-training/2305.20050-process-supervision/">实现解读</a> · <a href="#qa-7c928a3ae66cbf1b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:process-supervision" data-paper-title="Let&#x27;s Verify Step by Step" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Let&#x27;s Verify Step by Step LLM 后训练 OpenAI 2023-05-31 逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5781（+146.67%）；奖励、KL、长度和候选预算一致。  过程监督 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 主动选择高不确定步骤与随机标注有什么取舍？ 主动方式希望把预算放到模型最难判断的位置，随机抽样更接近原分布。高不确定不必代表最重要，采样偏差及标签质量仍需考虑，不能单凭熵保证效率。 例如一个含糊格式步骤熵高，也未必比关键数学转折更值得人工审查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-14599bd243e344eb">主动选择高不确定步骤与随机标注有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprocess-supervision">Let&#x27;s Verify Step by Step</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主动方式希望把预算放到模型最难判断的位置，随机抽样更接近原分布。高不确定不必代表最重要，采样偏差及标签质量仍需考虑，不能单凭熵保证效率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个含糊格式步骤熵高，也未必比关键数学转折更值得人工审查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.20050">原论文</a> · <a href="../../../../post-training/2305.20050-process-supervision/">实现解读</a> · <a href="#qa-14599bd243e344eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:process-supervision" data-paper-title="Let&#x27;s Verify Step by Step" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Let&#x27;s Verify Step by Step LLM 后训练 OpenAI 2023-05-31 逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5781（+146.67%）；奖励、KL、长度和候选预算一致。  过程监督 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 本地PRM目标里的标签与模型预测概率应怎样隔离？ 步骤真标签作为固定监督，PRM概率可微，熵用于允许的选样阶段；不能用测试步骤金标选择训练样本。本地统一候选预算仅验证机制，未复刻完整原数据。 例如先看测试哪里标错再重点训练，会把评测答案用于学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fc42fa618967fd6a">本地PRM目标里的标签与模型预测概率应怎样隔离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprocess-supervision">Let&#x27;s Verify Step by Step</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>步骤真标签作为固定监督，PRM概率可微，熵用于允许的选样阶段；不能用测试步骤金标选择训练样本。本地统一候选预算仅验证机制，未复刻完整原数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先看测试哪里标错再重点训练，会把评测答案用于学习。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.20050">原论文</a> · <a href="../../../../post-training/2305.20050-process-supervision/">实现解读</a> · <a href="#qa-fc42fa618967fd6a">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

一个最终分数，怎样转成不会奖励错误步骤的训练信号？

## 记住这一点

奖励定义什么算好，信用分配决定哪段行为收到这个信号。过程监督直接评价中间步骤；Math-Shepherd从某一步继续采样，用最终可解性构造步骤标签。多目标与rubric方法还要决定不同标准对应哪些token，以及如何防止一项奖励掩盖另一项。结果奖励、步骤证据和训练优势相关，但不能直接当同一个量。

## 一个例子

假设一道数学题前两步合理、第三步算错，却碰巧给出正确最终答案。只按终局奖励更新整段回答，会强化错误步骤。可以对关键前缀做独立后续求解或步骤审查，形成更细证据；但某个前缀后续采样失败，也可能来自采样预算不足，不能立刻等同于该步骤必错。

## 什么时候要小心

多个裁判的一致意见不保证真值，rubric分数也可能被风格和捷径操纵。应分开验证标签质量、信用公式与策略能力，并保持评价器不泄漏隐藏答案。此组包括奖励/梯度组件和成本审查资料，本地合成信用检查不构成推理、机器人或视频生成能力证据。

## 先读这几篇

先读Process Supervision，区分逐步标签与终局标签；再读Math-Shepherd，看如何用续写构造步骤信号；最后读TACO，理解为什么正确回答内部也可能存在不该被强化的token。

1. [Let&#x27;s Verify Step by Step](../../../post-training/2305.20050-process-supervision/README.md) · [原论文](https://arxiv.org/abs/2305.20050)
2. [Math-Shepherd](../../../post-training/2312.08935-math-shepherd/README.md) · [原论文](https://arxiv.org/abs/2312.08935)
3. [TACO](../../../post-training/2607.07976-taco/README.md) · [原论文](https://arxiv.org/abs/2607.07976)

## 自测一下

一条长回答最终正确，能否把所有token都赋予相同正信用，并据此声称每一步正确？

??? note "展开参考答案"

    不能。终局奖励只说明输出满足验收条件，无法证明中间过程无误。统一信用是一种估计选择，应检查错误步骤被强化的风险；细粒度信用也必须有可靠来源和独立对照，不能把评审分数本身当作过程真值。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
