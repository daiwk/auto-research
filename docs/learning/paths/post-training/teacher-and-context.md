---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 教师与纠错：额外信息何时能帮到学生

[LLM 后训练](index.md) / 188 个问题 · 47 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/post-training/teacher-and-context.md)

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
<p class="ar-learning-status" data-learning-status role="status">188 个问题 · 47 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:aopd" data-paper-title="When to Follow the Teacher: Advantage-Based On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="When to Follow the Teacher: Advantage-Based On-Policy Distillation LLM 后训练 University of Pennsylvania 2026-10-22 普通 OPD 在学生实际访问的状态上模仿教师，但教师偏好的动作不一定能被当前学生继续完成。AOPD 用该动作对学生最终奖励的优势加权教师监督，通过学生原有 rollout、终局奖励及教师重要性比率估计，不额外生成反事实续写。 完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。oracle 仅存在测试代码，不进入损失或诊断策略。本地状态：L1 精确损失组件，diagnostic only。实现论文 Eq. 3.6 / 3.8 与 Algorithm 1 的 leave-one-out baseline，不是完整 LLM 训练器或能力复现。完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。leave_one_out_advantages 按 prompt group 独立计算 baseline；  On-policy distillation 优势加权蒸馏与无额外rollout估计 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 AOPD为什么问教师动作对学生是否可完成？ 教师偏好的下一步不一定是当前学生能继续完成的路线，学生相对终局优势用于选择适合其能力的指导。估计复用学生已有rollout，不额外生成反事实续写。 例如教师给很高阶证明起点，学生后面完全接不住，未必是最佳当前监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-aopd-187dc1ba" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0d373390c70e780e">AOPD为什么问教师动作对学生是否可完成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aaopd">When to Follow the Teacher: Advantage-Based On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师偏好的下一步不一定是当前学生能继续完成的路线，学生相对终局优势用于选择适合其能力的指导。估计复用学生已有rollout，不额外生成反事实续写。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师给很高阶证明起点，学生后面完全接不住，未必是最佳当前监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31563v1">原论文</a> · <a href="../../../../post-training/2610.31563-aopd/">实现解读</a> · <a href="#qa-0d373390c70e780e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:aopd" data-paper-title="When to Follow the Teacher: Advantage-Based On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="When to Follow the Teacher: Advantage-Based On-Policy Distillation LLM 后训练 University of Pennsylvania 2026-10-22 普通 OPD 在学生实际访问的状态上模仿教师，但教师偏好的动作不一定能被当前学生继续完成。AOPD 用该动作对学生最终奖励的优势加权教师监督，通过学生原有 rollout、终局奖励及教师重要性比率估计，不额外生成反事实续写。 完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。oracle 仅存在测试代码，不进入损失或诊断策略。本地状态：L1 精确损失组件，diagnostic only。实现论文 Eq. 3.6 / 3.8 与 Algorithm 1 的 leave-one-out baseline，不是完整 LLM 训练器或能力复现。完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。leave_one_out_advantages 按 prompt group 独立计算 baseline；  On-policy distillation 优势加权蒸馏与无额外rollout估计 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 AOPD为什么不只给KL乘一个reward，而需要采样项与全词表教师期望共用截断测度？ 目标关心教师动作对当前学生后续奖励的优势，估计包含两项相消结构。只截断采样项、或把教师测度重新归一化，会破坏对应关系，变成另一目标。leave-one-out基线来自同题其他rollout，教师与行为概率冻结，不额外生成反事实续写来伪造优势。 教学例子：教师偏好一个学生暂时接不下去的开头，不能仅因教师概率高就强化；需结合学生真实续写结果，判断指导是否可利用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7838986bdda19e05">AOPD为什么不只给KL乘一个reward，而需要采样项与全词表教师期望共用截断测度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aaopd">When to Follow the Teacher: Advantage-Based On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标关心教师动作对当前学生后续奖励的优势，估计包含两项相消结构。只截断采样项、或把教师测度重新归一化，会破坏对应关系，变成另一目标。leave-one-out基线来自同题其他rollout，教师与行为概率冻结，不额外生成反事实续写来伪造优势。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师偏好一个学生暂时接不下去的开头，不能仅因教师概率高就强化；需结合学生真实续写结果，判断指导是否可利用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31563v1">原论文</a> · <a href="../../../../post-training/2610.31563-aopd/">实现解读</a> · <a href="#qa-7838986bdda19e05">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:aopd" data-paper-title="When to Follow the Teacher: Advantage-Based On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="When to Follow the Teacher: Advantage-Based On-Policy Distillation LLM 后训练 University of Pennsylvania 2026-10-22 普通 OPD 在学生实际访问的状态上模仿教师，但教师偏好的动作不一定能被当前学生继续完成。AOPD 用该动作对学生最终奖励的优势加权教师监督，通过学生原有 rollout、终局奖励及教师重要性比率估计，不额外生成反事实续写。 完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。oracle 仅存在测试代码，不进入损失或诊断策略。本地状态：L1 精确损失组件，diagnostic only。实现论文 Eq. 3.6 / 3.8 与 Algorithm 1 的 leave-one-out baseline，不是完整 LLM 训练器或能力复现。完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。leave_one_out_advantages 按 prompt group 独立计算 baseline；  On-policy distillation 优势加权蒸馏与无额外rollout估计 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 AOPD与给KL简单乘一个reward有什么不同？ 目标包含同一截断教师测度下的采样项与全分布项，结合独立LOO回报；简单乘奖会丢掉其估计结构。截断测度不重新归一，是关键差异。 例如只对一个采样词乘奖励，不能代表减去全词表教师项的同一目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-11c650f807871930">AOPD与给KL简单乘一个reward有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aaopd">When to Follow the Teacher: Advantage-Based On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标包含同一截断教师测度下的采样项与全分布项，结合独立LOO回报；简单乘奖会丢掉其估计结构。截断测度不重新归一，是关键差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只对一个采样词乘奖励，不能代表减去全词表教师项的同一目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31563v1">原论文</a> · <a href="../../../../post-training/2610.31563-aopd/">实现解读</a> · <a href="#qa-11c650f807871930">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:aopd" data-paper-title="When to Follow the Teacher: Advantage-Based On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="When to Follow the Teacher: Advantage-Based On-Policy Distillation LLM 后训练 University of Pennsylvania 2026-10-22 普通 OPD 在学生实际访问的状态上模仿教师，但教师偏好的动作不一定能被当前学生继续完成。AOPD 用该动作对学生最终奖励的优势加权教师监督，通过学生原有 rollout、终局奖励及教师重要性比率估计，不额外生成反事实续写。 完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。oracle 仅存在测试代码，不进入损失或诊断策略。本地状态：L1 精确损失组件，diagnostic only。实现论文 Eq. 3.6 / 3.8 与 Algorithm 1 的 leave-one-out baseline，不是完整 LLM 训练器或能力复现。完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。leave_one_out_advantages 按 prompt group 独立计算 baseline；  On-policy distillation 优势加权蒸馏与无额外rollout估计 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 AOPD能只裁sampled term或用当前学生替代rollout S吗？ 不能，两项共享同一未归一化截断教师测度，分母来自固定采样学生S。只更新Sθ，组需多于一以形成独立LOO基线，不得跨步偷偷改行为概率。 例如把截断后教师再softmax，会改变总质量及两项对应关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7fc0623d19d76044">AOPD能只裁sampled term或用当前学生替代rollout S吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aaopd">When to Follow the Teacher: Advantage-Based On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，两项共享同一未归一化截断教师测度，分母来自固定采样学生S。只更新Sθ，组需多于一以形成独立LOO基线，不得跨步偷偷改行为概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把截断后教师再softmax，会改变总质量及两项对应关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31563v1">原论文</a> · <a href="../../../../post-training/2610.31563-aopd/">实现解读</a> · <a href="#qa-7fc0623d19d76044">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minimal-edit-opd" data-paper-title="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning LLM 后训练 Meta Superintelligence Labs 2026-10-21 ME-OPD 用训练专属描述与参考解法，让教师为错误的学生回答打分，只纠正教师不支持的 token；正确回答只走任务奖励，避免整段模仿。它针对小型视觉语言模型误读斜边、标签或几何关系的问题，保留原回答中无需修改的推导与措辞。ME-OPD 让教师在训练时看到图形描述、已验证参考解法和学生的完整原回答，要求“用最少编辑修正”。教师不生成新答案，而是 teacher-force 同一学生回答的第二次出现，为原 token 打分。最终答案验证正确的 rollout 只走任务 GRPO； 完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。多个 seed 仍是 L1 机制诊断，不构成能力比较。本地状态：L1 精确路由 / 纠错目标组件，diagnostic only，不是 VLM 能力复现。完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。GRPO 的未公开实现细节不冒充论文原配置。freeze_rollouts 接收外部 verifier 的二元奖励和外部全组优势，复制并冻结旧学生 / 教师概率、mask 与路由。它不判断自然语言答案正确性，不生成图形描述，不校验参考解法是否真的通过验证器。  On-policy distillation 多模态最小编辑纠错 LLM 后训练 教师与纠错：额外信息何时能帮到学生 ME-OPD为什么正确回答不走教师纠错分支？ 正确轨迹保留任务奖励，避免教师改写已成功表达；错误轨迹才筛教师更不支持的原token做局部纠正。教师不生成新答案，而是给原回答评分。 例如答对的另一种解法不必因教师风格不同被整段改掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-minimal-edit-opd-97f1b5ed" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-622a1fc443b1a5c7">ME-OPD为什么正确回答不走教师纠错分支？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminimal-edit-opd">Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确轨迹保留任务奖励，避免教师改写已成功表达；错误轨迹才筛教师更不支持的原token做局部纠正。教师不生成新答案，而是给原回答评分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如答对的另一种解法不必因教师风格不同被整段改掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30231v1">原论文</a> · <a href="../../../../post-training/2610.30231-minimal-edit-opd/">实现解读</a> · <a href="#qa-622a1fc443b1a5c7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minimal-edit-opd" data-paper-title="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning LLM 后训练 Meta Superintelligence Labs 2026-10-21 ME-OPD 用训练专属描述与参考解法，让教师为错误的学生回答打分，只纠正教师不支持的 token；正确回答只走任务奖励，避免整段模仿。它针对小型视觉语言模型误读斜边、标签或几何关系的问题，保留原回答中无需修改的推导与措辞。ME-OPD 让教师在训练时看到图形描述、已验证参考解法和学生的完整原回答，要求“用最少编辑修正”。教师不生成新答案，而是 teacher-force 同一学生回答的第二次出现，为原 token 打分。最终答案验证正确的 rollout 只走任务 GRPO； 完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。多个 seed 仍是 L1 机制诊断，不构成能力比较。本地状态：L1 精确路由 / 纠错目标组件，diagnostic only，不是 VLM 能力复现。完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。GRPO 的未公开实现细节不冒充论文原配置。freeze_rollouts 接收外部 verifier 的二元奖励和外部全组优势，复制并冻结旧学生 / 教师概率、mask 与路由。它不判断自然语言答案正确性，不生成图形描述，不校验参考解法是否真的通过验证器。  On-policy distillation 多模态最小编辑纠错 LLM 后训练 教师与纠错：额外信息何时能帮到学生 ME-OPD为什么正确rollout不走教师纠错分支，错误rollout也只选一部分token？ 正确轨迹只保留任务奖励，避免教师风格压过已成功的学生行为；错误轨迹才比较教师与冻结旧学生，只纠正教师更不支持的位置。先在完整同题组计算任务优势，再拆分支，否则只剩正确组会失去相对信号。参考解和完整回答只进入训练教师视图。 教学例子：学生几何推导仅误读一个标签，教师评分可集中压低相关错误token；不能因表达不同就重训整条已正确回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c91dbc6c4760e464">ME-OPD为什么正确rollout不走教师纠错分支，错误rollout也只选一部分token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminimal-edit-opd">Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确轨迹只保留任务奖励，避免教师风格压过已成功的学生行为；错误轨迹才比较教师与冻结旧学生，只纠正教师更不支持的位置。先在完整同题组计算任务优势，再拆分支，否则只剩正确组会失去相对信号。参考解和完整回答只进入训练教师视图。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生几何推导仅误读一个标签，教师评分可集中压低相关错误token；不能因表达不同就重训整条已正确回答。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30231v1">原论文</a> · <a href="../../../../post-training/2610.30231-minimal-edit-opd/">实现解读</a> · <a href="#qa-c91dbc6c4760e464">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minimal-edit-opd" data-paper-title="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning LLM 后训练 Meta Superintelligence Labs 2026-10-21 ME-OPD 用训练专属描述与参考解法，让教师为错误的学生回答打分，只纠正教师不支持的 token；正确回答只走任务奖励，避免整段模仿。它针对小型视觉语言模型误读斜边、标签或几何关系的问题，保留原回答中无需修改的推导与措辞。ME-OPD 让教师在训练时看到图形描述、已验证参考解法和学生的完整原回答，要求“用最少编辑修正”。教师不生成新答案，而是 teacher-force 同一学生回答的第二次出现，为原 token 打分。最终答案验证正确的 rollout 只走任务 GRPO； 完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。多个 seed 仍是 L1 机制诊断，不构成能力比较。本地状态：L1 精确路由 / 纠错目标组件，diagnostic only，不是 VLM 能力复现。完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。GRPO 的未公开实现细节不冒充论文原配置。freeze_rollouts 接收外部 verifier 的二元奖励和外部全组优势，复制并冻结旧学生 / 教师概率、mask 与路由。它不判断自然语言答案正确性，不生成图形描述，不校验参考解法是否真的通过验证器。  On-policy distillation 多模态最小编辑纠错 LLM 后训练 教师与纠错：额外信息何时能帮到学生 ME-OPD与Projected Distillation的修正产物有何不同？ 前者teacher-force原回答并压低选中错误token，后者外部projector生成已验证修正版并做编辑片段DPO。评分原token与比较新旧文本，数据流不同。 例如一法没有新改写答案，另一法必须把修正版与原版精确对齐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1965d1730d240a81">ME-OPD与Projected Distillation的修正产物有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminimal-edit-opd">Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者teacher-force原回答并压低选中错误token，后者外部projector生成已验证修正版并做编辑片段DPO。评分原token与比较新旧文本，数据流不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一法没有新改写答案，另一法必须把修正版与原版精确对齐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30231v1">原论文</a> · <a href="../../../../post-training/2610.30231-minimal-edit-opd/">实现解读</a> · <a href="#qa-1965d1730d240a81">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minimal-edit-opd" data-paper-title="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning LLM 后训练 Meta Superintelligence Labs 2026-10-21 ME-OPD 用训练专属描述与参考解法，让教师为错误的学生回答打分，只纠正教师不支持的 token；正确回答只走任务奖励，避免整段模仿。它针对小型视觉语言模型误读斜边、标签或几何关系的问题，保留原回答中无需修改的推导与措辞。ME-OPD 让教师在训练时看到图形描述、已验证参考解法和学生的完整原回答，要求“用最少编辑修正”。教师不生成新答案，而是 teacher-force 同一学生回答的第二次出现，为原 token 打分。最终答案验证正确的 rollout 只走任务 GRPO； 完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。多个 seed 仍是 L1 机制诊断，不构成能力比较。本地状态：L1 精确路由 / 纠错目标组件，diagnostic only，不是 VLM 能力复现。完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。GRPO 的未公开实现细节不冒充论文原配置。freeze_rollouts 接收外部 verifier 的二元奖励和外部全组优势，复制并冻结旧学生 / 教师概率、mask 与路由。它不判断自然语言答案正确性，不生成图形描述，不校验参考解法是否真的通过验证器。  On-policy distillation 多模态最小编辑纠错 LLM 后训练 教师与纠错：额外信息何时能帮到学生 ME-OPD应在拆正确/错误集合之前还是之后计算组优势？ 先用全K条奖励算优势，再拆分；只留正确再统计会全为一而丢信号。纠错mask用冻结旧学生，严格大于才选，分母是全minibatch选中纠错token数。 例如teacher与old分数相等的位置不选，不能因当前学生改变又重新挑mask。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-66ee5b0fc573399b">ME-OPD应在拆正确/错误集合之前还是之后计算组优势？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminimal-edit-opd">Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先用全K条奖励算优势，再拆分；只留正确再统计会全为一而丢信号。纠错mask用冻结旧学生，严格大于才选，分母是全minibatch选中纠错token数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如teacher与old分数相等的位置不选，不能因当前学生改变又重新挑mask。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30231v1">原论文</a> · <a href="../../../../post-training/2610.30231-minimal-edit-opd/">实现解读</a> · <a href="#qa-66ee5b0fc573399b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:csd" data-paper-title="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer LLM 后训练 NVIDIA 2026-10-20 师生词表大小、token ID 与分词边界不一致，不能直接逐坐标 KL。CSD 先按原文字符区间对齐 chunk，再通过解码文本等价构造共同事件。1:1 采用共同 token；1:N 或 M:1 固定观察到的 chunk 前缀，只枚举末 token 的等价续写；M:N 默认只保留实际观察序列。未显式匹配的质量进入 REST，而不是被丢弃或重新归一化。 完整实验成本过高，不复现（审查 DONE）。微型诊断使用两套不同大小的词表与不同分词，覆盖四种 chunk 形状。L1 跨 Tokenizer 对齐与损失组件，不是大模型能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。v1 提交在 10 月 20 日截止时间之后，本轮归 2026-10-22 首次公告，不改写其真实提交日期。align_offsets 对原文字符 span 做最小公共边界对齐并核对整体 decode；paired_completions 在固定前缀下按文本建映射，不按相同 ID、概率排名或给定相似分配对；  知识蒸馏 跨Tokenizer共同事件分布 LLM 后训练 教师与纠错：额外信息何时能帮到学生 CSD为什么需要共同文本事件而不直接对齐token ID？ 不同tokenizer的编号、词表和边界不同，同一文字可能拆成不同数量词元。先按字符区间核对解码等价，再比较共同事件概率，才有可比语义对象。 例如一个模型单词一token，另一个拆成两片，编号相同毫无语义保证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-csd-2e95adef" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0b6013f196c2b334">CSD为什么需要共同文本事件而不直接对齐token ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acsd">CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同tokenizer的编号、词表和边界不同，同一文字可能拆成不同数量词元。先按字符区间核对解码等价，再比较共同事件概率，才有可比语义对象。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个模型单词一token，另一个拆成两片，编号相同毫无语义保证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28895v1">原论文</a> · <a href="../../../../post-training/2610.28895-csd/">实现解读</a> · <a href="#qa-0b6013f196c2b334">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:csd" data-paper-title="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer LLM 后训练 NVIDIA 2026-10-20 师生词表大小、token ID 与分词边界不一致，不能直接逐坐标 KL。CSD 先按原文字符区间对齐 chunk，再通过解码文本等价构造共同事件。1:1 采用共同 token；1:N 或 M:1 固定观察到的 chunk 前缀，只枚举末 token 的等价续写；M:N 默认只保留实际观察序列。未显式匹配的质量进入 REST，而不是被丢弃或重新归一化。 完整实验成本过高，不复现（审查 DONE）。微型诊断使用两套不同大小的词表与不同分词，覆盖四种 chunk 形状。L1 跨 Tokenizer 对齐与损失组件，不是大模型能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。v1 提交在 10 月 20 日截止时间之后，本轮归 2026-10-22 首次公告，不改写其真实提交日期。align_offsets 对原文字符 span 做最小公共边界对齐并核对整体 decode；paired_completions 在固定前缀下按文本建映射，不按相同 ID、概率排名或给定相似分配对；  知识蒸馏 跨Tokenizer共同事件分布 LLM 后训练 教师与纠错：额外信息何时能帮到学生 CSD跨tokenizer蒸馏时，为什么保留REST质量而不能对共同候选重新softmax？ 不同分词的token ID没有直接对应，需按解码文本事件和完整链式概率建立共同空间。显式匹配以外的质量进入REST，保留未列出事件的影响；重新归一会把这些质量丢掉并改变散度。共同文本对齐也必须核对字符边界，不能只按位置凑齐两套token。 教学例子：一个模型把词分成两段，另一个用单token；匹配该词事件后，其余续写概率仍存在，不能假装共同事件就是整个词表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1963fb419fddeb23">CSD跨tokenizer蒸馏时，为什么保留REST质量而不能对共同候选重新softmax？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acsd">CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同分词的token ID没有直接对应，需按解码文本事件和完整链式概率建立共同空间。显式匹配以外的质量进入REST，保留未列出事件的影响；重新归一会把这些质量丢掉并改变散度。共同文本对齐也必须核对字符边界，不能只按位置凑齐两套token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个模型把词分成两段，另一个用单token；匹配该词事件后，其余续写概率仍存在，不能假装共同事件就是整个词表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28895v1">原论文</a> · <a href="../../../../post-training/2610.28895-csd/">实现解读</a> · <a href="#qa-1963fb419fddeb23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:csd" data-paper-title="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer LLM 后训练 NVIDIA 2026-10-20 师生词表大小、token ID 与分词边界不一致，不能直接逐坐标 KL。CSD 先按原文字符区间对齐 chunk，再通过解码文本等价构造共同事件。1:1 采用共同 token；1:N 或 M:1 固定观察到的 chunk 前缀，只枚举末 token 的等价续写；M:N 默认只保留实际观察序列。未显式匹配的质量进入 REST，而不是被丢弃或重新归一化。 完整实验成本过高，不复现（审查 DONE）。微型诊断使用两套不同大小的词表与不同分词，覆盖四种 chunk 形状。L1 跨 Tokenizer 对齐与损失组件，不是大模型能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。v1 提交在 10 月 20 日截止时间之后，本轮归 2026-10-22 首次公告，不改写其真实提交日期。align_offsets 对原文字符 span 做最小公共边界对齐并核对整体 decode；paired_completions 在固定前缀下按文本建映射，不按相同 ID、概率排名或给定相似分配对；  知识蒸馏 跨Tokenizer共同事件分布 LLM 后训练 教师与纠错：额外信息何时能帮到学生 REST质量桶与只对共同候选重新归一相比保留什么？ REST保留未显式匹配的概率，避免把少量交集假装成完整分布。重新softmax会隐藏未覆盖质量，且完整链式概率不能随意改成长度平均。 例如共同候选只占很小质量，归一后看似高度一致，遗漏部分却可能很大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-efd7158acfdbd08a">REST质量桶与只对共同候选重新归一相比保留什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acsd">CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>REST保留未显式匹配的概率，避免把少量交集假装成完整分布。重新softmax会隐藏未覆盖质量，且完整链式概率不能随意改成长度平均。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如共同候选只占很小质量，归一后看似高度一致，遗漏部分却可能很大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28895v1">原论文</a> · <a href="../../../../post-training/2610.28895-csd/">实现解读</a> · <a href="#qa-efd7158acfdbd08a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:csd" data-paper-title="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer LLM 后训练 NVIDIA 2026-10-20 师生词表大小、token ID 与分词边界不一致，不能直接逐坐标 KL。CSD 先按原文字符区间对齐 chunk，再通过解码文本等价构造共同事件。1:1 采用共同 token；1:N 或 M:1 固定观察到的 chunk 前缀，只枚举末 token 的等价续写；M:N 默认只保留实际观察序列。未显式匹配的质量进入 REST，而不是被丢弃或重新归一化。 完整实验成本过高，不复现（审查 DONE）。微型诊断使用两套不同大小的词表与不同分词，覆盖四种 chunk 形状。L1 跨 Tokenizer 对齐与损失组件，不是大模型能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。v1 提交在 10 月 20 日截止时间之后，本轮归 2026-10-22 首次公告，不改写其真实提交日期。align_offsets 对原文字符 span 做最小公共边界对齐并核对整体 decode；paired_completions 在固定前缀下按文本建映射，不按相同 ID、概率排名或给定相似分配对；  知识蒸馏 跨Tokenizer共同事件分布 LLM 后训练 教师与纠错：额外信息何时能帮到学生 CSD学生梯度是否只经过chunk末token？ 事件概率含观察前缀链乘因子、末词和REST，学生梯度需经过全部；教师冻结。非1:1权重不进入分母计数，零KD或无共同事件回退CE，比例整体detach。 例如两token对一token时，忽略第一片的概率会错算整段文字事件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-59295ed90b381ba1">CSD学生梯度是否只经过chunk末token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acsd">CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>事件概率含观察前缀链乘因子、末词和REST，学生梯度需经过全部；教师冻结。非1:1权重不进入分母计数，零KD或无共同事件回退CE，比例整体detach。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两token对一token时，忽略第一片的概率会错算整段文字事件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28895v1">原论文</a> · <a href="../../../../post-training/2610.28895-csd/">实现解读</a> · <a href="#qa-59295ed90b381ba1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:apsd" data-paper-title="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization LLM 后训练 Korea University 2026-10-19 反馈条件自教师可能破坏正确rollout里学生已经成功的偏好，却又对错误rollout纠正不足。APSD依据正确性调整蒸馏target：正确时在学生和自教师之间插值，错误时越过自教师外推。关键不只是换一个target数值，还要保留target对学生分布的依赖；整个target一起detach会丢掉定义性的耦合梯度。原文§4及附录B 原图建议：Figure 3方法总览，保留右侧梯度几何与target分支；Figure 1是插值／外推的概念图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，学生实际采样回答。每次更新从同一当前学生复制自教师，教师只在额外的合成训练反馈条件下重放学生回答并停止梯度；不是单独初始化的外部教师。actor的采样条件只有公开prompt，不读取反馈、正确性或gold。反馈ID不代表自然语言执行错误或真实成功解答。  On-policy distillation 自蒸馏与训练稳定性 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 APSD为什么正确时插值、错误时越过自教师外推？ 正确轨迹需要保留学生已有成功偏好，插值减小干扰；错误轨迹希望更强纠正，外推加大教师方向。它依据训练反馈改变目标，不意味着外推必然正确。 例如学生已答对时温和调整，答错时才加强纠正，而不是统一强度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-apsd-7a5d9aba" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b2643095f7c4d5ec">APSD为什么正确时插值、错误时越过自教师外推？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aapsd">Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Korea University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确轨迹需要保留学生已有成功偏好，插值减小干扰；错误轨迹希望更强纠正，外推加大教师方向。它依据训练反馈改变目标，不意味着外推必然正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生已答对时温和调整，答错时才加强纠正，而不是统一强度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25973v1">原论文</a> · <a href="../../../../post-training/2610.25973-apsd/">实现解读</a> · <a href="#qa-b2643095f7c4d5ec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:apsd" data-paper-title="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization LLM 后训练 Korea University 2026-10-19 反馈条件自教师可能破坏正确rollout里学生已经成功的偏好，却又对错误rollout纠正不足。APSD依据正确性调整蒸馏target：正确时在学生和自教师之间插值，错误时越过自教师外推。关键不只是换一个target数值，还要保留target对学生分布的依赖；整个target一起detach会丢掉定义性的耦合梯度。原文§4及附录B 原图建议：Figure 3方法总览，保留右侧梯度几何与target分支；Figure 1是插值／外推的概念图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，学生实际采样回答。每次更新从同一当前学生复制自教师，教师只在额外的合成训练反馈条件下重放学生回答并停止梯度；不是单独初始化的外部教师。actor的采样条件只有公开prompt，不读取反馈、正确性或gold。反馈ID不代表自然语言执行错误或真实成功解答。  On-policy distillation 自蒸馏与训练稳定性 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 APSD只冻结自教师，为什么不能把整个插值或外推target都detach？ target同时依赖冻结教师与当前学生，正确轨迹插值、错误轨迹外推改变的还有学生依赖分支的梯度。把整体detach只留下部分模仿项，会丢掉定义性的耦合修正。数值上目标一样不代表反向一样，反馈只用于训练自教师，不能进入部署学生输入。 教学例子：两个实现算出相同target概率，但一个保留其对学生分布的导数、另一个冻结；即使loss相同，参数更新也会不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-975d7ed4ab0090e0">APSD只冻结自教师，为什么不能把整个插值或外推target都detach？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aapsd">Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Korea University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>target同时依赖冻结教师与当前学生，正确轨迹插值、错误轨迹外推改变的还有学生依赖分支的梯度。把整体detach只留下部分模仿项，会丢掉定义性的耦合修正。数值上目标一样不代表反向一样，反馈只用于训练自教师，不能进入部署学生输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个实现算出相同target概率，但一个保留其对学生分布的导数、另一个冻结；即使loss相同，参数更新也会不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25973v1">原论文</a> · <a href="../../../../post-training/2610.25973-apsd/">实现解读</a> · <a href="#qa-975d7ed4ab0090e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:apsd" data-paper-title="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization LLM 后训练 Korea University 2026-10-19 反馈条件自教师可能破坏正确rollout里学生已经成功的偏好，却又对错误rollout纠正不足。APSD依据正确性调整蒸馏target：正确时在学生和自教师之间插值，错误时越过自教师外推。关键不只是换一个target数值，还要保留target对学生分布的依赖；整个target一起detach会丢掉定义性的耦合梯度。原文§4及附录B 原图建议：Figure 3方法总览，保留右侧梯度几何与target分支；Figure 1是插值／外推的概念图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，学生实际采样回答。每次更新从同一当前学生复制自教师，教师只在额外的合成训练反馈条件下重放学生回答并停止梯度；不是单独初始化的外部教师。actor的采样条件只有公开prompt，不读取反馈、正确性或gold。反馈ID不代表自然语言执行错误或真实成功解答。  On-policy distillation 自蒸馏与训练稳定性 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 APSD冻结自教师与冻结整个target为什么不是一回事？ 自教师q冻结，但PoE目标还依赖可微学生p，完整梯度有额外耦合项。整个target detach会删除定义性项，变成另一种缩放蒸馏，即使前向目标数值相同。 例如目标中一半来自当前学生，切断这支梯度会改变优化而非只节省内存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5fd715ce12c8bbea">APSD冻结自教师与冻结整个target为什么不是一回事？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aapsd">Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Korea University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自教师q冻结，但PoE目标还依赖可微学生p，完整梯度有额外耦合项。整个target detach会删除定义性项，变成另一种缩放蒸馏，即使前向目标数值相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如目标中一半来自当前学生，切断这支梯度会改变优化而非只节省内存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25973v1">原论文</a> · <a href="../../../../post-training/2610.25973-apsd/">实现解读</a> · <a href="#qa-5fd715ce12c8bbea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:apsd" data-paper-title="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization LLM 后训练 Korea University 2026-10-19 反馈条件自教师可能破坏正确rollout里学生已经成功的偏好，却又对错误rollout纠正不足。APSD依据正确性调整蒸馏target：正确时在学生和自教师之间插值，错误时越过自教师外推。关键不只是换一个target数值，还要保留target对学生分布的依赖；整个target一起detach会丢掉定义性的耦合梯度。原文§4及附录B 原图建议：Figure 3方法总览，保留右侧梯度几何与target分支；Figure 1是插值／外推的概念图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，学生实际采样回答。每次更新从同一当前学生复制自教师，教师只在额外的合成训练反馈条件下重放学生回答并停止梯度；不是单独初始化的外部教师。actor的采样条件只有公开prompt，不读取反馈、正确性或gold。反馈ID不代表自然语言执行错误或真实成功解答。  On-policy distillation 自蒸馏与训练稳定性 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 APSD构造PoE时哪些张量保持梯度，默认α如何解释？ 学生分布及其target分支可微，自教师条件分布detach；log-space计算防下溢。正确α在零一间、错误大于一，本地RLRF默认与原RLVR配置不同需明示。 例如正确用0.5、错误用1.5属于本地对应配置，不能写成全部原文设置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e0cdab3eae9b2f49">APSD构造PoE时哪些张量保持梯度，默认α如何解释？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aapsd">Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Korea University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生分布及其target分支可微，自教师条件分布detach；log-space计算防下溢。正确α在零一间、错误大于一，本地RLRF默认与原RLVR配置不同需明示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如正确用0.5、错误用1.5属于本地对应配置，不能写成全部原文设置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25973v1">原论文</a> · <a href="../../../../post-training/2610.25973-apsd/">实现解读</a> · <a href="#qa-e0cdab3eae9b2f49">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:visually-attributable-opd" data-paper-title="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation LLM 后训练 Baidu Inc. 2026-10-19 特权图像裁剪带来的 teacher 修正，可能混有语言先验或风格变化。VAG 让同一 EMA 教师对证据保留裁剪和随机遮挡裁剪重放相同学生前缀，只接纳与视觉对比方向一致的修正，再以有界项调制 verifier 的组归一化 advantage。纯文本教师或固定 logits 门控不能冒充该多模态链路。 仅资料收录，成本过高，不复现（审查 DONE）。仅资料收录，成本过高，不复现（审查 DONE）。没有本地可执行 adapter、评测接口或机制验证；不接入 Evolve，不作为能力证据，不进入自动重试队列。完整实验不复现，审查 DONE。原文 §4.1：Qwen3.5-4B/9B 全参数训练一 epoch，batch 48，每题条响应，最大 1,024 token，8×NVIDIA H800。需要训练数据的目标细节裁剪、EMA 双视图重放和六基准 judge 协议。单 A100/A30 或 Mac 不承担原矩阵，属于配置直接支持的高成本判断，无需下载权重或试跑。  On-policy distillation 多模态RLVR与视觉归因 LLM 后训练 教师与纠错：额外信息何时能帮到学生 VAG为什么比较证据保留与退化裁剪？ 特权裁剪修正可能混入语言风格，匹配两视觉条件的差提供视觉归因方向；只接纳同向修正，再有界调制verifier优势，保留任务锚点。 例如裁剪后教师改口，需判断改动是否与画面证据差异一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-visually-attributable-opd-08abcb9d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6c05fa0a31b262be">VAG为什么比较证据保留与退化裁剪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avisually-attributable-opd">Reinforcement Learning with Visually Attributable On-Policy Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>特权裁剪修正可能混入语言风格，匹配两视觉条件的差提供视觉归因方向；只接纳同向修正，再有界调制verifier优势，保留任务锚点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如裁剪后教师改口，需判断改动是否与画面证据差异一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26856v1">原论文</a> · <a href="../../../../post-training/2610.26856-vag/">实现解读</a> · <a href="#qa-6c05fa0a31b262be">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:visually-attributable-opd" data-paper-title="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation LLM 后训练 Baidu Inc. 2026-10-19 特权图像裁剪带来的 teacher 修正，可能混有语言先验或风格变化。VAG 让同一 EMA 教师对证据保留裁剪和随机遮挡裁剪重放相同学生前缀，只接纳与视觉对比方向一致的修正，再以有界项调制 verifier 的组归一化 advantage。纯文本教师或固定 logits 门控不能冒充该多模态链路。 仅资料收录，成本过高，不复现（审查 DONE）。仅资料收录，成本过高，不复现（审查 DONE）。没有本地可执行 adapter、评测接口或机制验证；不接入 Evolve，不作为能力证据，不进入自动重试队列。完整实验不复现，审查 DONE。原文 §4.1：Qwen3.5-4B/9B 全参数训练一 epoch，batch 48，每题条响应，最大 1,024 token，8×NVIDIA H800。需要训练数据的目标细节裁剪、EMA 双视图重放和六基准 judge 协议。单 A100/A30 或 Mac 不承担原矩阵，属于配置直接支持的高成本判断，无需下载权重或试跑。  On-policy distillation 多模态RLVR与视觉归因 LLM 后训练 教师与纠错：额外信息何时能帮到学生 VAG为什么只接受与证据保留/退化视图对比同号的教师修正？ 特权裁剪带来的修正可能来自语言风格而非视觉证据，同号门控要求它与视觉对比方向相容，再以有界项调制原verifier优势。两分支必须是同一EMA教师，仅改变视觉输入。这个控制不能用两份任意文本logits替代，当前库也未执行完整多模态链路。 教学例子：裁剪后教师更偏爱某个措辞，但遮挡关键图像时偏好不变，说明修正未必由视觉证据驱动，不应一律当作视觉指导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9db3e7df89d58559">VAG为什么只接受与证据保留/退化视图对比同号的教师修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avisually-attributable-opd">Reinforcement Learning with Visually Attributable On-Policy Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>特权裁剪带来的修正可能来自语言风格而非视觉证据，同号门控要求它与视觉对比方向相容，再以有界项调制原verifier优势。两分支必须是同一EMA教师，仅改变视觉输入。这个控制不能用两份任意文本logits替代，当前库也未执行完整多模态链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>裁剪后教师更偏爱某个措辞，但遮挡关键图像时偏好不变，说明修正未必由视觉证据驱动，不应一律当作视觉指导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26856v1">原论文</a> · <a href="../../../../post-training/2610.26856-vag/">实现解读</a> · <a href="#qa-9db3e7df89d58559">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:visually-attributable-opd" data-paper-title="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation LLM 后训练 Baidu Inc. 2026-10-19 特权图像裁剪带来的 teacher 修正，可能混有语言先验或风格变化。VAG 让同一 EMA 教师对证据保留裁剪和随机遮挡裁剪重放相同学生前缀，只接纳与视觉对比方向一致的修正，再以有界项调制 verifier 的组归一化 advantage。纯文本教师或固定 logits 门控不能冒充该多模态链路。 仅资料收录，成本过高，不复现（审查 DONE）。仅资料收录，成本过高，不复现（审查 DONE）。没有本地可执行 adapter、评测接口或机制验证；不接入 Evolve，不作为能力证据，不进入自动重试队列。完整实验不复现，审查 DONE。原文 §4.1：Qwen3.5-4B/9B 全参数训练一 epoch，batch 48，每题条响应，最大 1,024 token，8×NVIDIA H800。需要训练数据的目标细节裁剪、EMA 双视图重放和六基准 judge 协议。单 A100/A30 或 Mac 不承担原矩阵，属于配置直接支持的高成本判断，无需下载权重或试跑。  On-policy distillation 多模态RLVR与视觉归因 LLM 后训练 教师与纠错：额外信息何时能帮到学生 VAG与纯文本教师给固定logits门控有何区别？ 定义链路依赖同一EMA视觉模型在两种真实视图上的条件对照。纯文本或固定分数只能模拟公式，无法证明视觉敏感度和裁剪归因已执行。 例如人工给正负两个分数，并没有让模型实际看过被遮挡图像。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0a9fabe889a4cbd9">VAG与纯文本教师给固定logits门控有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avisually-attributable-opd">Reinforcement Learning with Visually Attributable On-Policy Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>定义链路依赖同一EMA视觉模型在两种真实视图上的条件对照。纯文本或固定分数只能模拟公式，无法证明视觉敏感度和裁剪归因已执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人工给正负两个分数，并没有让模型实际看过被遮挡图像。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26856v1">原论文</a> · <a href="../../../../post-training/2610.26856-vag/">实现解读</a> · <a href="#qa-0a9fabe889a4cbd9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:visually-attributable-opd" data-paper-title="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation LLM 后训练 Baidu Inc. 2026-10-19 特权图像裁剪带来的 teacher 修正，可能混有语言先验或风格变化。VAG 让同一 EMA 教师对证据保留裁剪和随机遮挡裁剪重放相同学生前缀，只接纳与视觉对比方向一致的修正，再以有界项调制 verifier 的组归一化 advantage。纯文本教师或固定 logits 门控不能冒充该多模态链路。 仅资料收录，成本过高，不复现（审查 DONE）。仅资料收录，成本过高，不复现（审查 DONE）。没有本地可执行 adapter、评测接口或机制验证；不接入 Evolve，不作为能力证据，不进入自动重试队列。完整实验不复现，审查 DONE。原文 §4.1：Qwen3.5-4B/9B 全参数训练一 epoch，batch 48，每题条响应，最大 1,024 token，8×NVIDIA H800。需要训练数据的目标细节裁剪、EMA 双视图重放和六基准 judge 协议。单 A100/A30 或 Mac 不承担原矩阵，属于配置直接支持的高成本判断，无需下载权重或试跑。  On-policy distillation 多模态RLVR与视觉归因 LLM 后训练 教师与纠错：额外信息何时能帮到学生 VAG两教师分支可以用不同模型吗，代码已执行了吗？ 不可以当同一设定，两分支应同EMA教师仅改变视觉输入；当前公式是原方法说明，本库未执行该多模态训练。严格同号门控保留，verifier优势不被替换。 例如一个大视觉教师对比一个小文本模型，会混入架构差而非只测视觉对照。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f3aece6b9cdc6db6">VAG两教师分支可以用不同模型吗，代码已执行了吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avisually-attributable-opd">Reinforcement Learning with Visually Attributable On-Policy Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可以当同一设定，两分支应同EMA教师仅改变视觉输入；当前公式是原方法说明，本库未执行该多模态训练。严格同号门控保留，verifier优势不被替换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个大视觉教师对比一个小文本模型，会混入架构差而非只测视觉对照。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26856v1">原论文</a> · <a href="../../../../post-training/2610.26856-vag/">实现解读</a> · <a href="#qa-f3aece6b9cdc6db6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spod" data-paper-title="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation LLM 后训练 University of Southern California 2026-10-18 多轮Agent蒸馏中，学生可能先超过教师，再随着持续模仿而退步。作者区分两个过程：教师修复学生的弱决策，同时也会侵蚀学生已经成功、但与教师偏好不同的行为。SPOD只在成功训练episode内保护教师整action概率更低的decision，取消该处蒸馏压力，并用软概率floor抵消来自其他状态更新的间接侵蚀；其余decision继续正常蒸馏。原文§3–4 原图建议：附录Figure 9的训练流程；Figure 1展示overshoot与修复／侵蚀现象，可作为辅助结果图。原图不是本地运行结果。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是Agent能力复现。L1 定义性组件／梯度诊断，不是Agent能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，实际采样多state episode；教师独立随机初始化后冻结，对同一学生action重放评分。显式合成环境在episode结束后返回训练成功位，actor输入只有公开历史、自己的action及公开观察ID；不读取成功位、gold或评估结果。固定长度预算的合成action不是ALFWorld/WebShop/ScienceWorld语言动作。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 SPOD里的一个decision是一枚词元，还是一次可能含多个词元的action？ 保护对象是某个状态下的完整action，包括多个词元及原生结束符；不是单枚词元，也不是整个episode。成功标签在episode级给出，保护判断却定位到其中具体decision。先分清这三个层级，才能避免把成功轨迹全部当成不再学习。 教学例子：一次工具调用包含工具名、参数和结束符，可组成一个action；同一成功episode中还可能有别的action。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-spod-93843af2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a42d125f58769f2d">SPOD里的一个decision是一枚词元，还是一次可能含多个词元的action？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspod">Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>保护对象是某个状态下的完整action，包括多个词元及原生结束符；不是单枚词元，也不是整个episode。成功标签在episode级给出，保护判断却定位到其中具体decision。先分清这三个层级，才能避免把成功轨迹全部当成不再学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次工具调用包含工具名、参数和结束符，可组成一个action；同一成功episode中还可能有别的action。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25034v1">原论文</a> · <a href="../../../../post-training/2610.25034-spod/">实现解读</a> · <a href="#qa-a42d125f58769f2d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spod" data-paper-title="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation LLM 后训练 University of Southern California 2026-10-18 多轮Agent蒸馏中，学生可能先超过教师，再随着持续模仿而退步。作者区分两个过程：教师修复学生的弱决策，同时也会侵蚀学生已经成功、但与教师偏好不同的行为。SPOD只在成功训练episode内保护教师整action概率更低的decision，取消该处蒸馏压力，并用软概率floor抵消来自其他状态更新的间接侵蚀；其余decision继续正常蒸馏。原文§3–4 原图建议：附录Figure 9的训练流程；Figure 1展示overshoot与修复／侵蚀现象，可作为辅助结果图。原图不是本地运行结果。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是Agent能力复现。L1 定义性组件／梯度诊断，不是Agent能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，实际采样多state episode；教师独立随机初始化后冻结，对同一学生action重放评分。显式合成环境在episode结束后返回训练成功位，actor输入只有公开历史、自己的action及公开观察ID；不读取成功位、gold或评估结果。固定长度预算的合成action不是ALFWorld/WebShop/ScienceWorld语言动作。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 SPOD为什么按完整action原始概率保护成功选择，而不能逐token比较后屏蔽整个成功episode？ 保护条件针对成功episode中教师更不支持的具体decision，完整action概率包含其token共同作用。逐词开关或整段屏蔽会改变保护对象。受保护处取消蒸馏并加软概率floor，其他decision仍学习；软floor不能阻止共享参数从别处间接侵蚀该动作。 教学例子：一个成功工具调用的某些词教师更喜欢、另一些更不喜欢，逐词投票可能与整条调用概率比较给出相反结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4f73294b40790bec">SPOD为什么按完整action原始概率保护成功选择，而不能逐token比较后屏蔽整个成功episode？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspod">Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>保护条件针对成功episode中教师更不支持的具体decision，完整action概率包含其token共同作用。逐词开关或整段屏蔽会改变保护对象。受保护处取消蒸馏并加软概率floor，其他decision仍学习；软floor不能阻止共享参数从别处间接侵蚀该动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个成功工具调用的某些词教师更喜欢、另一些更不喜欢，逐词投票可能与整条调用概率比较给出相反结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25034v1">原论文</a> · <a href="../../../../post-training/2610.25034-spod/">实现解读</a> · <a href="#qa-4f73294b40790bec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spod" data-paper-title="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation LLM 后训练 University of Southern California 2026-10-18 多轮Agent蒸馏中，学生可能先超过教师，再随着持续模仿而退步。作者区分两个过程：教师修复学生的弱决策，同时也会侵蚀学生已经成功、但与教师偏好不同的行为。SPOD只在成功训练episode内保护教师整action概率更低的decision，取消该处蒸馏压力，并用软概率floor抵消来自其他状态更新的间接侵蚀；其余decision继续正常蒸馏。原文§3–4 原图建议：附录Figure 9的训练流程；Figure 1展示overshoot与修复／侵蚀现象，可作为辅助结果图。原图不是本地运行结果。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是Agent能力复现。L1 定义性组件／梯度诊断，不是Agent能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，实际采样多state episode；教师独立随机初始化后冻结，对同一学生action重放评分。显式合成环境在episode结束后返回训练成功位，actor输入只有公开历史、自己的action及公开观察ID；不读取成功位、gold或评估结果。固定长度预算的合成action不是ALFWorld/WebShop/ScienceWorld语言动作。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 SPOD软floor与屏蔽整个成功episode有什么区别？ 保护粒度是完整action，其他decision仍正常蒸馏；floor只是惩罚概率低于门槛，不是硬保证。共享参数上的其他状态更新仍可影响受保护行为。 例如一个成功episode里某步值得保留，不表示其他所有步骤都不能学习教师。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8c4645db472f959d">SPOD软floor与屏蔽整个成功episode有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspod">Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>保护粒度是完整action，其他decision仍正常蒸馏；floor只是惩罚概率低于门槛，不是硬保证。共享参数上的其他状态更新仍可影响受保护行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个成功episode里某步值得保留，不表示其他所有步骤都不能学习教师。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25034v1">原论文</a> · <a href="../../../../post-training/2610.25034-spod/">实现解读</a> · <a href="#qa-8c4645db472f959d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spod" data-paper-title="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation LLM 后训练 University of Southern California 2026-10-18 多轮Agent蒸馏中，学生可能先超过教师，再随着持续模仿而退步。作者区分两个过程：教师修复学生的弱决策，同时也会侵蚀学生已经成功、但与教师偏好不同的行为。SPOD只在成功训练episode内保护教师整action概率更低的decision，取消该处蒸馏压力，并用软概率floor抵消来自其他状态更新的间接侵蚀；其余decision继续正常蒸馏。原文§3–4 原图建议：附录Figure 9的训练流程；Figure 1展示overshoot与修复／侵蚀现象，可作为辅助结果图。原图不是本地运行结果。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是Agent能力复现。L1 定义性组件／梯度诊断，不是Agent能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，实际采样多state episode；教师独立随机初始化后冻结，对同一学生action重放评分。显式合成环境在episode结束后返回训练成功位，actor输入只有公开历史、自己的action及公开观察ID；不读取成功位、gold或评估结果。固定长度预算的合成action不是ALFWorld/WebShop/ScienceWorld语言动作。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 SPOD gate比较的是温度采样概率还是原始整action概率？ 用温度和动作约束前原始概率，含原生结束token，逐token logp求和。gate更新前重算、微分时固定，按action、state、episode分层平均，不把长轨迹自动加权。 例如把每词平均概率当整action概率，会改变长短动作的保护判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-afbfefdafb6ba446">SPOD gate比较的是温度采样概率还是原始整action概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspod">Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用温度和动作约束前原始概率，含原生结束token，逐token logp求和。gate更新前重算、微分时固定，按action、state、episode分层平均，不把长轨迹自动加权。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把每词平均概率当整action概率，会改变长短动作的保护判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25034v1">原论文</a> · <a href="../../../../post-training/2610.25034-spod/">实现解读</a> · <a href="#qa-afbfefdafb6ba446">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:multiagent-opd" data-paper-title="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation LLM 后训练 Alibaba Group 2026-10-16 层级团队的最终答案能监督Leader，却难以判断Searcher的检索、总结是否真正有效。MultiAgent-OPD先在较简单的Searcher–Answerer流程训练教师，再从相同的基础checkpoint重新开始训练共享参数的Leader–Searcher–Answerer团队。冻结教师为学生实际搜索轨迹提供局部OPD反馈；Leader根据团队结果、Answerer根据自己的候选正确性学习。原文 §3 原图建议：Figure 1 层级工作流；如只保留一张，应同时可读出阶段一教师和阶段二角色分工。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。不用固定工作流、随机教师或单个蒸馏算子冒充端到端多Agent系统；未接 Evolve。成本过高，不复现（审查 DONE）。基础模型Qwen3-4B-Instruct-2507，两阶段使用79,168条NQ和90,447条HotpotQA，batch32题×5轨迹、每次多个PPO更新，层级流程包含多波委派、最多12环境步及每请求5个回答候选；还需真实搜索服务。评测是七个数据集合计固定5,000题，每个方法每题四次独立工作流，不是每数据集5,000题。原文当前配置未明确完整GPU数，不臆造显卡数量或训练时长。  Agentic RL On-policy distillation 多Agent协作 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MultiAgent-OPD为什么先训练简单Searcher–Answerer教师？ 团队终局奖难评价搜索细节，任务训练教师先获得相关局部指导，再冻结监督层级团队的Searcher。Leader与Answerer仍用各自结果信号，不把所有角色统一打分。 例如搜索总结是否有用，不能只靠最终答案一位对错粗略判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-multiagent-opd-b3177be0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1250f479e1d32a0f">MultiAgent-OPD为什么先训练简单Searcher–Answerer教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amultiagent-opd">MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>团队终局奖难评价搜索细节，任务训练教师先获得相关局部指导，再冻结监督层级团队的Searcher。Leader与Answerer仍用各自结果信号，不把所有角色统一打分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索总结是否有用，不能只靠最终答案一位对错粗略判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23234v1">原论文</a> · <a href="../../../../post-training/2610.23234-multiagent-opd/">实现解读</a> · <a href="#qa-1250f479e1d32a0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:multiagent-opd" data-paper-title="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation LLM 后训练 Alibaba Group 2026-10-16 层级团队的最终答案能监督Leader，却难以判断Searcher的检索、总结是否真正有效。MultiAgent-OPD先在较简单的Searcher–Answerer流程训练教师，再从相同的基础checkpoint重新开始训练共享参数的Leader–Searcher–Answerer团队。冻结教师为学生实际搜索轨迹提供局部OPD反馈；Leader根据团队结果、Answerer根据自己的候选正确性学习。原文 §3 原图建议：Figure 1 层级工作流；如只保留一张，应同时可读出阶段一教师和阶段二角色分工。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。不用固定工作流、随机教师或单个蒸馏算子冒充端到端多Agent系统；未接 Evolve。成本过高，不复现（审查 DONE）。基础模型Qwen3-4B-Instruct-2507，两阶段使用79,168条NQ和90,447条HotpotQA，batch32题×5轨迹、每次多个PPO更新，层级流程包含多波委派、最多12环境步及每请求5个回答候选；还需真实搜索服务。评测是七个数据集合计固定5,000题，每个方法每题四次独立工作流，不是每数据集5,000题。原文当前配置未明确完整GPU数，不臆造显卡数量或训练时长。  Agentic RL On-policy distillation 多Agent协作 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MultiAgent-OPD为什么用简单团队训练教师，却从原基础checkpoint重新训练层级学生？ 先训练的Searcher–Answerer提供任务相关局部指导，第二阶段重新起步可区分教师知识与层级架构学习。Leader、Searcher和Answerer虽然共享参数，仍接收各自角色信号；Searcher教师读其真实子任务与检索历史，不是把全局gold答案交给所有角色。 教学例子：团队最终答错可能因分工，也可能因检索摘要差；只把最终奖励均匀撒给所有角色，会丢掉局部学习信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f609e498e460cc82">MultiAgent-OPD为什么用简单团队训练教师，却从原基础checkpoint重新训练层级学生？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amultiagent-opd">MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先训练的Searcher–Answerer提供任务相关局部指导，第二阶段重新起步可区分教师知识与层级架构学习。Leader、Searcher和Answerer虽然共享参数，仍接收各自角色信号；Searcher教师读其真实子任务与检索历史，不是把全局gold答案交给所有角色。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>团队最终答错可能因分工，也可能因检索摘要差；只把最终奖励均匀撒给所有角色，会丢掉局部学习信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23234v1">原论文</a> · <a href="../../../../post-training/2610.23234-multiagent-opd/">实现解读</a> · <a href="#qa-f609e498e460cc82">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:multiagent-opd" data-paper-title="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation LLM 后训练 Alibaba Group 2026-10-16 层级团队的最终答案能监督Leader，却难以判断Searcher的检索、总结是否真正有效。MultiAgent-OPD先在较简单的Searcher–Answerer流程训练教师，再从相同的基础checkpoint重新开始训练共享参数的Leader–Searcher–Answerer团队。冻结教师为学生实际搜索轨迹提供局部OPD反馈；Leader根据团队结果、Answerer根据自己的候选正确性学习。原文 §3 原图建议：Figure 1 层级工作流；如只保留一张，应同时可读出阶段一教师和阶段二角色分工。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。不用固定工作流、随机教师或单个蒸馏算子冒充端到端多Agent系统；未接 Evolve。成本过高，不复现（审查 DONE）。基础模型Qwen3-4B-Instruct-2507，两阶段使用79,168条NQ和90,447条HotpotQA，batch32题×5轨迹、每次多个PPO更新，层级流程包含多波委派、最多12环境步及每请求5个回答候选；还需真实搜索服务。评测是七个数据集合计固定5,000题，每个方法每题四次独立工作流，不是每数据集5,000题。原文当前配置未明确完整GPU数，不臆造显卡数量或训练时长。  Agentic RL On-policy distillation 多Agent协作 LLM 后训练 教师与纠错：额外信息何时能帮到学生 阶段二为何从相同base重新开始，而不直接续训阶段一模型？ 重新初始化隔离教师训练产物与层级学生学习，避免把阶段一权重收益混成层级蒸馏收益。共享base不代表教师和学生在阶段二都继续更新。 例如先造一个会教搜索的模型，再从原起点训练团队，而非让现成教师直接变团队。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7a5c7077c1993896">阶段二为何从相同base重新开始，而不直接续训阶段一模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amultiagent-opd">MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重新初始化隔离教师训练产物与层级学生学习，避免把阶段一权重收益混成层级蒸馏收益。共享base不代表教师和学生在阶段二都继续更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先造一个会教搜索的模型，再从原起点训练团队，而非让现成教师直接变团队。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23234v1">原论文</a> · <a href="../../../../post-training/2610.23234-multiagent-opd/">实现解读</a> · <a href="#qa-7a5c7077c1993896">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:multiagent-opd" data-paper-title="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation LLM 后训练 Alibaba Group 2026-10-16 层级团队的最终答案能监督Leader，却难以判断Searcher的检索、总结是否真正有效。MultiAgent-OPD先在较简单的Searcher–Answerer流程训练教师，再从相同的基础checkpoint重新开始训练共享参数的Leader–Searcher–Answerer团队。冻结教师为学生实际搜索轨迹提供局部OPD反馈；Leader根据团队结果、Answerer根据自己的候选正确性学习。原文 §3 原图建议：Figure 1 层级工作流；如只保留一张，应同时可读出阶段一教师和阶段二角色分工。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。不用固定工作流、随机教师或单个蒸馏算子冒充端到端多Agent系统；未接 Evolve。成本过高，不复现（审查 DONE）。基础模型Qwen3-4B-Instruct-2507，两阶段使用79,168条NQ和90,447条HotpotQA，batch32题×5轨迹、每次多个PPO更新，层级流程包含多波委派、最多12环境步及每请求5个回答候选；还需真实搜索服务。评测是七个数据集合计固定5,000题，每个方法每题四次独立工作流，不是每数据集5,000题。原文当前配置未明确完整GPU数，不臆造显卡数量或训练时长。  Agentic RL On-policy distillation 多Agent协作 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MultiAgent角色共享参数时，loss mask仍需分开吗？ 需要，各角色输出对应不同优势和KL设置；Searcher局部log比不等于因果贡献，工具观察mask。搜索活动计的是有检索的环境步，不是原始调用总数。 例如一轮并行多个搜索调用，不应无上限地堆高Leader活动奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1b25f0f6e8f3131c">MultiAgent角色共享参数时，loss mask仍需分开吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amultiagent-opd">MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需要，各角色输出对应不同优势和KL设置；Searcher局部log比不等于因果贡献，工具观察mask。搜索活动计的是有检索的环境步，不是原始调用总数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一轮并行多个搜索调用，不应无上限地堆高Leader活动奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23234v1">原论文</a> · <a href="../../../../post-training/2610.23234-multiagent-opd/">实现解读</a> · <a href="#qa-1b25f0f6e8f3131c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:treeopsd" data-paper-title="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning LLM 后训练 Tsinghua University 2026-10-16 长轨迹仅有终局奖励时，同一轨迹的好坏动作容易一起获奖或受罚；同一批轨迹又会经历多次更新，旧信用不能告诉优化器何时停止。TreeOPSD 将续写分支整理成共享前缀树，把叶奖励按行为策略似然向上回传，再把每个 turn 的信用映射为一个冻结且有界的 Bernoulli 教师。学生相对旧策略的变化达到目标时梯度消失，超过目标则反向，不再只有无限推进的方向。原文 §2–3 原图建议：Figure 2 方法总览，展示树信用、冻结后验教师与多次更新；Figure 1 是概念插图，不宜代替算法图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维 GRU 因果策略，实际采样三 turn 轨迹并从中间前缀继续采样；每个 turn 两个 actor token，非终局附带一个公开观察 ID。显式合成终局奖励由末 turn 的 token 计算，不传入 actor；它不是自然语言搜索 verifier。树合并保留完整历史、观察和终止标记，重复叶仍保留在和奖励统计中。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 TreeOPSD为什么将共享前缀整理成树？ 相同历史下不同续写揭示动作后果，叶奖励可沿行为似然回传成局部信用。共享turn只计一次，避免同一前缀因分枝多被重复放大。 例如两条路线前三步相同，分叉后成败不同，树可保留这一局部比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-treeopsd-8a101275" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ea2a85257cb9f1bd">TreeOPSD为什么将共享前缀整理成树？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atreeopsd">Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同历史下不同续写揭示动作后果，叶奖励可沿行为似然回传成局部信用。共享turn只计一次，避免同一前缀因分枝多被重复放大。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条路线前三步相同，分叉后成败不同，树可保留这一局部比较。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23181v1">原论文</a> · <a href="../../../../post-training/2610.23181-treeopsd/">实现解读</a> · <a href="#qa-ea2a85257cb9f1bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:treeopsd" data-paper-title="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning LLM 后训练 Tsinghua University 2026-10-16 长轨迹仅有终局奖励时，同一轨迹的好坏动作容易一起获奖或受罚；同一批轨迹又会经历多次更新，旧信用不能告诉优化器何时停止。TreeOPSD 将续写分支整理成共享前缀树，把叶奖励按行为策略似然向上回传，再把每个 turn 的信用映射为一个冻结且有界的 Bernoulli 教师。学生相对旧策略的变化达到目标时梯度消失，超过目标则反向，不再只有无限推进的方向。原文 §2–3 原图建议：Figure 2 方法总览，展示树信用、冻结后验教师与多次更新；Figure 1 是概念插图，不宜代替算法图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维 GRU 因果策略，实际采样三 turn 轨迹并从中间前缀继续采样；每个 turn 两个 actor token，非终局附带一个公开观察 ID。显式合成终局奖励由末 turn 的 token 计算，不传入 actor；它不是自然语言搜索 verifier。树合并保留完整历史、观察和终止标记，重复叶仍保留在和奖励统计中。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 TreeOPSD为什么把树回传信用变成有界Bernoulli教师，而不无限重复原奖励梯度？ 终局信用给出改善方向，却不自动告诉多次更新何时停止。冻结有界目标把方向变成有限距离，学生相对旧策略的变化达到目标后梯度消失，超过后会拉回。树中共享turn须去重，分支权重来自完整actor span行为似然，不能任意改为平均token分数。 教学例子：同一批成功轨迹训练很多轮时，有限目标可在“学够了”后停下；单一固定正优势则可能一直推高同一选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-241ac3d1627b0295">TreeOPSD为什么把树回传信用变成有界Bernoulli教师，而不无限重复原奖励梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atreeopsd">Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局信用给出改善方向，却不自动告诉多次更新何时停止。冻结有界目标把方向变成有限距离，学生相对旧策略的变化达到目标后梯度消失，超过后会拉回。树中共享turn须去重，分支权重来自完整actor span行为似然，不能任意改为平均token分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一批成功轨迹训练很多轮时，有限目标可在“学够了”后停下；单一固定正优势则可能一直推高同一选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23181v1">原论文</a> · <a href="../../../../post-training/2610.23181-treeopsd/">实现解读</a> · <a href="#qa-241ac3d1627b0295">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:treeopsd" data-paper-title="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning LLM 后训练 Tsinghua University 2026-10-16 长轨迹仅有终局奖励时，同一轨迹的好坏动作容易一起获奖或受罚；同一批轨迹又会经历多次更新，旧信用不能告诉优化器何时停止。TreeOPSD 将续写分支整理成共享前缀树，把叶奖励按行为策略似然向上回传，再把每个 turn 的信用映射为一个冻结且有界的 Bernoulli 教师。学生相对旧策略的变化达到目标时梯度消失，超过目标则反向，不再只有无限推进的方向。原文 §2–3 原图建议：Figure 2 方法总览，展示树信用、冻结后验教师与多次更新；Figure 1 是概念插图，不宜代替算法图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维 GRU 因果策略，实际采样三 turn 轨迹并从中间前缀继续采样；每个 turn 两个 actor token，非终局附带一个公开观察 ID。显式合成终局奖励由末 turn 的 token 计算，不传入 actor；它不是自然语言搜索 verifier。树合并保留完整历史、观察和终止标记，重复叶仍保留在和奖励统计中。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 有界Bernoulli教师与一直沿同一优势方向更新有什么区别？ 冻结后验给有限目标，当前相对旧策略变化达到目标时梯度为零，超过后反向。普通固定优势重复优化可能持续推进，二者对多次更新的停止含义不同。 例如把某动作推到足够程度后应停，而不是同一批重复训练越推越远。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-091e270e18989e35">有界Bernoulli教师与一直沿同一优势方向更新有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atreeopsd">Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结后验给有限目标，当前相对旧策略变化达到目标时梯度为零，超过后反向。普通固定优势重复优化可能持续推进，二者对多次更新的停止含义不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把某动作推到足够程度后应停，而不是同一批重复训练越推越远。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23181v1">原论文</a> · <a href="../../../../post-training/2610.23181-treeopsd/">实现解读</a> · <a href="#qa-091e270e18989e35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:treeopsd" data-paper-title="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning LLM 后训练 Tsinghua University 2026-10-16 长轨迹仅有终局奖励时，同一轨迹的好坏动作容易一起获奖或受罚；同一批轨迹又会经历多次更新，旧信用不能告诉优化器何时停止。TreeOPSD 将续写分支整理成共享前缀树，把叶奖励按行为策略似然向上回传，再把每个 turn 的信用映射为一个冻结且有界的 Bernoulli 教师。学生相对旧策略的变化达到目标时梯度消失，超过目标则反向，不再只有无限推进的方向。原文 §2–3 原图建议：Figure 2 方法总览，展示树信用、冻结后验教师与多次更新；Figure 1 是概念插图，不宜代替算法图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维 GRU 因果策略，实际采样三 turn 轨迹并从中间前缀继续采样；每个 turn 两个 actor token，非终局附带一个公开观察 ID。显式合成终局奖励由末 turn 的 token 计算，不传入 actor；它不是自然语言搜索 verifier。树合并保留完整历史、观察和终止标记，重复叶仍保留在和奖励统计中。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 TreeOPSD的Bernoulli分布是完整下一词教师吗？ 不是，它描述已采样turn相对旧策略的二点后验。树权重用完整actor span似然，叶奖样本标准差，观察不进分母；不能用任意clip来代替有界目标推导。 例如两个Bernoulli类别不是词表里两个token，而是相对turn变化的抽象表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dcc62aef7e508b26">TreeOPSD的Bernoulli分布是完整下一词教师吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atreeopsd">Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，它描述已采样turn相对旧策略的二点后验。树权重用完整actor span似然，叶奖样本标准差，观察不进分母；不能用任意clip来代替有界目标推导。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个Bernoulli类别不是词表里两个token，而是相对turn变化的抽象表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23181v1">原论文</a> · <a href="../../../../post-training/2610.23181-treeopsd/">实现解读</a> · <a href="#qa-dcc62aef7e508b26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cce-opd" data-paper-title="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models LLM 后训练 The Chinese University of Hong Kong, Shenzhen 2026-10-15 教师可能跟随学生错误 reasoning prefix，而忽略题目条件。CCE 在完全相同的学生 response prefix上，让同一冻结教师分别读取完整题目与遮蔽一个有效前提的题目，以 clipped log-prob contrast 调整辅助 target。学生始终从完整题目生成；未通过 condition eligibility 或 entropy gate 的位置仍保留原 sampled PPO-OPD。 完整实验成本过高，不复现（审查 DONE）。L1 双视图 / union / auxiliary-KL / sampled PPO 组件。只接受已审阅的合法 condition span，不提供伪造的语义抽取器。完整实验成本过高，不复现（审查 DONE）。公开 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784，train/validation/test 原始 byte 区间 80%/10%/10% 分离。微型教师只作公开文本 next-token 训练，并非数学教师。  On-policy distillation 后训练算法组件 CCE-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 CCE为什么用遮蔽有效前提的题面形成教师对照？ 教师可能顺着学生错误前缀而忽略题目条件，匹配题面对照提取条件敏感方向，外推辅助目标。学生始终从完整题面生成，不是训练它解被破坏的问题。 例如删除一个关键数量条件后教师分布变化，可揭示哪些token依赖该前提。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-cce-opd-2c59e40e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c1d96269c32db7e5">CCE为什么用遮蔽有效前提的题面形成教师对照？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acce-opd">Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师可能顺着学生错误前缀而忽略题目条件，匹配题面对照提取条件敏感方向，外推辅助目标。学生始终从完整题面生成，不是训练它解被破坏的问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删除一个关键数量条件后教师分布变化，可揭示哪些token依赖该前提。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21195v1">原论文</a> · <a href="../../../../post-training/2610.21195-cce-opd/">实现解读</a> · <a href="#qa-c1d96269c32db7e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cce-opd" data-paper-title="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models LLM 后训练 The Chinese University of Hong Kong, Shenzhen 2026-10-15 教师可能跟随学生错误 reasoning prefix，而忽略题目条件。CCE 在完全相同的学生 response prefix上，让同一冻结教师分别读取完整题目与遮蔽一个有效前提的题目，以 clipped log-prob contrast 调整辅助 target。学生始终从完整题目生成；未通过 condition eligibility 或 entropy gate 的位置仍保留原 sampled PPO-OPD。 完整实验成本过高，不复现（审查 DONE）。L1 双视图 / union / auxiliary-KL / sampled PPO 组件。只接受已审阅的合法 condition span，不提供伪造的语义抽取器。完整实验成本过高，不复现（审查 DONE）。公开 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784，train/validation/test 原始 byte 区间 80%/10%/10% 分离。微型教师只作公开文本 next-token 训练，并非数学教师。  On-policy distillation 后训练算法组件 CCE-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 CCE-OPD为什么两份教师视图必须保持同一学生response prefix，学生分布又不能在候选上重归一？ 固定前缀使差异主要来自题目条件遮蔽，而非另一条推理轨迹。辅助教师目标在其候选支持上归一，但学生保持完整词表softmax，才能保留支持集之外的概率梯度。合法条件与熵门控只控制附加项，不通过时仍保留原OPD，不是整段跳过。 教学例子：只遮掉一个有效前提再看教师下一词变化；若同时重写了学生前文，就无法把变化归因于这个前提。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c0a63178fb77e7a3">CCE-OPD为什么两份教师视图必须保持同一学生response prefix，学生分布又不能在候选上重归一？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acce-opd">Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定前缀使差异主要来自题目条件遮蔽，而非另一条推理轨迹。辅助教师目标在其候选支持上归一，但学生保持完整词表softmax，才能保留支持集之外的概率梯度。合法条件与熵门控只控制附加项，不通过时仍保留原OPD，不是整段跳过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只遮掉一个有效前提再看教师下一词变化；若同时重写了学生前文，就无法把变化归因于这个前提。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21195v1">原论文</a> · <a href="../../../../post-training/2610.21195-cce-opd/">实现解读</a> · <a href="#qa-c0a63178fb77e7a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cce-opd" data-paper-title="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models LLM 后训练 The Chinese University of Hong Kong, Shenzhen 2026-10-15 教师可能跟随学生错误 reasoning prefix，而忽略题目条件。CCE 在完全相同的学生 response prefix上，让同一冻结教师分别读取完整题目与遮蔽一个有效前提的题目，以 clipped log-prob contrast 调整辅助 target。学生始终从完整题目生成；未通过 condition eligibility 或 entropy gate 的位置仍保留原 sampled PPO-OPD。 完整实验成本过高，不复现（审查 DONE）。L1 双视图 / union / auxiliary-KL / sampled PPO 组件。只接受已审阅的合法 condition span，不提供伪造的语义抽取器。完整实验成本过高，不复现（审查 DONE）。公开 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784，train/validation/test 原始 byte 区间 80%/10%/10% 分离。微型教师只作公开文本 next-token 训练，并非数学教师。  On-policy distillation 后训练算法组件 CCE-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 CCE辅助门控关闭时会把整处OPD也删掉吗？ 不会，原sampled PPO-OPD始终保留，只不加辅助FKL。合法条件和熵门共同限定额外指导，区别于把所有低熵位置彻底停止学习。 例如不够高熵的格式词仍接受基础蒸馏，而非完全从loss消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e02added51ca60cf">CCE辅助门控关闭时会把整处OPD也删掉吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acce-opd">Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不会，原sampled PPO-OPD始终保留，只不加辅助FKL。合法条件和熵门共同限定额外指导，区别于把所有低熵位置彻底停止学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不够高熵的格式词仍接受基础蒸馏，而非完全从loss消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21195v1">原论文</a> · <a href="../../../../post-training/2610.21195-cce-opd/">实现解读</a> · <a href="#qa-e02added51ca60cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cce-opd" data-paper-title="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models LLM 后训练 The Chinese University of Hong Kong, Shenzhen 2026-10-15 教师可能跟随学生错误 reasoning prefix，而忽略题目条件。CCE 在完全相同的学生 response prefix上，让同一冻结教师分别读取完整题目与遮蔽一个有效前提的题目，以 clipped log-prob contrast 调整辅助 target。学生始终从完整题目生成；未通过 condition eligibility 或 entropy gate 的位置仍保留原 sampled PPO-OPD。 完整实验成本过高，不复现（审查 DONE）。L1 双视图 / union / auxiliary-KL / sampled PPO 组件。只接受已审阅的合法 condition span，不提供伪造的语义抽取器。完整实验成本过高，不复现（审查 DONE）。公开 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784，train/validation/test 原始 byte 区间 80%/10%/10% 分离。微型教师只作公开文本 next-token 训练，并非数学教师。  On-policy distillation 后训练算法组件 CCE-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 CCE熵在哪个分布上计算，学生是否在support重归一？ 熵在构建top并集前的完整教师词表上算；辅助目标在support归一，学生仍保留全词表softmax，以保留外部梯度。分母是全部有效响应位置而非通过gate数。 例如只在候选内重算学生，会隐藏候选外质量并改变辅助损失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-102d02cb6b593399">CCE熵在哪个分布上计算，学生是否在support重归一？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acce-opd">Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>熵在构建top并集前的完整教师词表上算；辅助目标在support归一，学生仍保留全词表softmax，以保留外部梯度。分母是全部有效响应位置而非通过gate数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只在候选内重算学生，会隐藏候选外质量并改变辅助损失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21195v1">原论文</a> · <a href="../../../../post-training/2610.21195-cce-opd/">实现解读</a> · <a href="#qa-102d02cb6b593399">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:elite-replay" data-paper-title="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search LLM 后训练 The Ohio State University 2026-10-15 单纯提高正确率的 RL 可能压缩正确解法的覆盖范围。EliteReplay 先用冻结基模和 MAP-Elites 收集不同正确策略，训练时持续回放固定档案。档案按问题、approach 与结构特征分 cell，每格只保留最短已验证解；不是把 IID 样本放进普通 replay buffer。 完整实验成本过高，不复现（审查 DONE）。L1 MAP-Elites / archive / sampler / mixed loss 组件。本地保留真实目标导向搜索，但算术 grammar 不是论文的 SQL LLM，审阅 approach 列表不是 LLM labeler；不以微型结果宣称 BIRD/Spider 能力。完整实验成本过高，不复现（审查 DONE）。runner 提供三个固定整数加法任务，候选为四种可解析表达式。一个小型冻结线性策略在原任务、目标 approach、parent 是否存在的条件下实际采样候选；AST whitelist 计算表达式结果进行验证，不执行任意生成程序。  Reference anchor 后训练算法组件 EliteReplay LLM 后训练 教师与纠错：额外信息何时能帮到学生 EliteReplay为什么给每问题建立质量–多样性档案？ 只提高正确率可能压缩解法覆盖，按approach和结构cell保存最短验证解，维持不同正确策略。档案不是把任意IID样本丢入普通回放池。 例如代数法和几何法分别存格，避免只留下最常见那一路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-elite-replay-bbf50043" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-efb23a3165472dcb">EliteReplay为什么给每问题建立质量–多样性档案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aelite-replay">EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只提高正确率可能压缩解法覆盖，按approach和结构cell保存最短验证解，维持不同正确策略。档案不是把任意IID样本丢入普通回放池。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如代数法和几何法分别存格，避免只留下最常见那一路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22290v1">原论文</a> · <a href="../../../../post-training/2610.22290-elite-replay/">实现解读</a> · <a href="#qa-efb23a3165472dcb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:elite-replay" data-paper-title="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search LLM 后训练 The Ohio State University 2026-10-15 单纯提高正确率的 RL 可能压缩正确解法的覆盖范围。EliteReplay 先用冻结基模和 MAP-Elites 收集不同正确策略，训练时持续回放固定档案。档案按问题、approach 与结构特征分 cell，每格只保留最短已验证解；不是把 IID 样本放进普通 replay buffer。 完整实验成本过高，不复现（审查 DONE）。L1 MAP-Elites / archive / sampler / mixed loss 组件。本地保留真实目标导向搜索，但算术 grammar 不是论文的 SQL LLM，审阅 approach 列表不是 LLM labeler；不以微型结果宣称 BIRD/Spider 能力。完整实验成本过高，不复现（审查 DONE）。runner 提供三个固定整数加法任务，候选为四种可解析表达式。一个小型冻结线性策略在原任务、目标 approach、parent 是否存在的条件下实际采样候选；AST whitelist 计算表达式结果进行验证，不执行任意生成程序。  Reference anchor 后训练算法组件 EliteReplay LLM 后训练 教师与纠错：额外信息何时能帮到学生 EliteReplay为什么按实际实现的approach存cell，并先平衡问题再平衡cell回放？ 请求一种解法不代表模型真按该路线生成，按请求标签存档会伪造多样性。实际descriptor决定cell，每格只保留最短已验证解；回放先平衡问题，避免档案大的题占过多训练权重。质量多样性档案因此不同于普通IID成功样本缓存。 教学例子：要求用几何法，模型却用了代数法，应归入实际代数cell；否则同一种解法会被多个请求标签包装成多样策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b7b4a830107e28f1">EliteReplay为什么按实际实现的approach存cell，并先平衡问题再平衡cell回放？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aelite-replay">EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>请求一种解法不代表模型真按该路线生成，按请求标签存档会伪造多样性。实际descriptor决定cell，每格只保留最短已验证解；回放先平衡问题，避免档案大的题占过多训练权重。质量多样性档案因此不同于普通IID成功样本缓存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>要求用几何法，模型却用了代数法，应归入实际代数cell；否则同一种解法会被多个请求标签包装成多样策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22290v1">原论文</a> · <a href="../../../../post-training/2610.22290-elite-replay/">实现解读</a> · <a href="#qa-b7b4a830107e28f1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:elite-replay" data-paper-title="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search LLM 后训练 The Ohio State University 2026-10-15 单纯提高正确率的 RL 可能压缩正确解法的覆盖范围。EliteReplay 先用冻结基模和 MAP-Elites 收集不同正确策略，训练时持续回放固定档案。档案按问题、approach 与结构特征分 cell，每格只保留最短已验证解；不是把 IID 样本放进普通 replay buffer。 完整实验成本过高，不复现（审查 DONE）。L1 MAP-Elites / archive / sampler / mixed loss 组件。本地保留真实目标导向搜索，但算术 grammar 不是论文的 SQL LLM，审阅 approach 列表不是 LLM labeler；不以微型结果宣称 BIRD/Spider 能力。完整实验成本过高，不复现（审查 DONE）。runner 提供三个固定整数加法任务，候选为四种可解析表达式。一个小型冻结线性策略在原任务、目标 approach、parent 是否存在的条件下实际采样候选；AST whitelist 计算表达式结果进行验证，不执行任意生成程序。  Reference anchor 后训练算法组件 EliteReplay LLM 后训练 教师与纠错：额外信息何时能帮到学生 MAP-Elites最短cell替换与全局只留最短答案有何不同？ 在每个实际描述符格内选短解，保留跨策略多样性；全局最短可能删掉其他方法。请求的approach未必实际实现，必须按实际cell存档。 例如提示要求归纳法却生成枚举法，应按枚举结构记录，而非信任请求标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6b2ee625f7485ad7">MAP-Elites最短cell替换与全局只留最短答案有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aelite-replay">EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>在每个实际描述符格内选短解，保留跨策略多样性；全局最短可能删掉其他方法。请求的approach未必实际实现，必须按实际cell存档。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如提示要求归纳法却生成枚举法，应按枚举结构记录，而非信任请求标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22290v1">原论文</a> · <a href="../../../../post-training/2610.22290-elite-replay/">实现解读</a> · <a href="#qa-6b2ee625f7485ad7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:elite-replay" data-paper-title="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search LLM 后训练 The Ohio State University 2026-10-15 单纯提高正确率的 RL 可能压缩正确解法的覆盖范围。EliteReplay 先用冻结基模和 MAP-Elites 收集不同正确策略，训练时持续回放固定档案。档案按问题、approach 与结构特征分 cell，每格只保留最短已验证解；不是把 IID 样本放进普通 replay buffer。 完整实验成本过高，不复现（审查 DONE）。L1 MAP-Elites / archive / sampler / mixed loss 组件。本地保留真实目标导向搜索，但算术 grammar 不是论文的 SQL LLM，审阅 approach 列表不是 LLM labeler；不以微型结果宣称 BIRD/Spider 能力。完整实验成本过高，不复现（审查 DONE）。runner 提供三个固定整数加法任务，候选为四种可解析表达式。一个小型冻结线性策略在原任务、目标 approach、parent 是否存在的条件下实际采样候选；AST whitelist 计算表达式结果进行验证，不执行任意生成程序。  Reference anchor 后训练算法组件 EliteReplay LLM 后训练 教师与纠错：额外信息何时能帮到学生 EliteReplay为什么先平衡问题再平衡occupied cells？ 否则档案大的题会自动占更多回放。每条响应长度平均，固定档案和GRPO按规定混合，padding在指数运算前清理，不能用测试答案建档或挑解。 例如一道题有很多已占格，不能因此比另一题获得十倍训练抽样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4a6a4358f1278fa3">EliteReplay为什么先平衡问题再平衡occupied cells？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aelite-replay">EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>否则档案大的题会自动占更多回放。每条响应长度平均，固定档案和GRPO按规定混合，padding在指数运算前清理，不能用测试答案建档或挑解。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一道题有很多已占格，不能因此比另一题获得十倍训练抽样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22290v1">原论文</a> · <a href="../../../../post-training/2610.22290-elite-replay/">实现解读</a> · <a href="#qa-4a6a4358f1278fa3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd-reminder" data-paper-title="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents LLM 后训练 Tsinghua University 2026-10-15 编码 Agent 的最终通过/失败不能指出哪一轮忽略了已有约束。OPRD 在学生自己生成的无提醒轨迹上训练：成功轨迹自模仿；失败轨迹由教师读取训练专用提醒，重新评分同一学生前缀，不是教师另生成一条答案。全局提醒持续有效，观测对应的局部提醒只在下一轮有效，之后必须移除。正式推理去掉教师和全部提醒。原文 §3 完整实验成本过高，不复现（审查 DONE）。奇偶校验只用于构造诊断 outcome，不是编码正确性。L1 算法组件，不是 SWE-bench 编码能力复现。已实现作用域、同前缀评分和训练目标；完整实验成本过高，不复现（审查 DONE）。不进入 evolve 晋级。本地使用随机初始化的128词表、12维 causal cumulative-embedding 策略。每步真实采样8条三轮轨迹、每轮2个 token；奇偶校验只用于构造诊断 outcome，不是编码正确性。教师重新读取相同 response 前缀；学生上下文不含提醒。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 提醒OPRD为何让学生先生成无提醒轨迹？ 部署时没有提醒，学生需在该条件下采样；失败后教师读训练提醒重评分相同前缀，把约束内化。成功轨迹另走自模仿，而非教师重写新答案。 例如忘记测试约束的代码动作，由训练教师提醒评分，学生推理仍只读原任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-oprd-reminder-a48a675d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f2796add4208606d">提醒OPRD为何让学生先生成无提醒轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoprd-reminder">OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>部署时没有提醒，学生需在该条件下采样；失败后教师读训练提醒重评分相同前缀，把约束内化。成功轨迹另走自模仿，而非教师重写新答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如忘记测试约束的代码动作，由训练教师提醒评分，学生推理仍只读原任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21496v1">原论文</a> · <a href="../../../../post-training/2610.21496-oprd-reminder/">实现解读</a> · <a href="#qa-f2796add4208606d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd-reminder" data-paper-title="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents LLM 后训练 Tsinghua University 2026-10-15 编码 Agent 的最终通过/失败不能指出哪一轮忽略了已有约束。OPRD 在学生自己生成的无提醒轨迹上训练：成功轨迹自模仿；失败轨迹由教师读取训练专用提醒，重新评分同一学生前缀，不是教师另生成一条答案。全局提醒持续有效，观测对应的局部提醒只在下一轮有效，之后必须移除。正式推理去掉教师和全部提醒。原文 §3 完整实验成本过高，不复现（审查 DONE）。奇偶校验只用于构造诊断 outcome，不是编码正确性。L1 算法组件，不是 SWE-bench 编码能力复现。已实现作用域、同前缀评分和训练目标；完整实验成本过高，不复现（审查 DONE）。不进入 evolve 晋级。本地使用随机初始化的128词表、12维 causal cumulative-embedding 策略。每步真实采样8条三轮轨迹、每轮2个 token；奇偶校验只用于构造诊断 outcome，不是编码正确性。教师重新读取相同 response 前缀；学生上下文不含提醒。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPRD的局部提醒为什么只作用于对应观察的下一轮，不能永久留在教师上下文？ 局部提醒描述某个观察触发的短期约束，过期后继续保留会影响无关后续决策。全局提醒与局部提醒作用域不同，教师重评同一学生前缀而非另生成答案；部署学生不带提醒。成功自模仿与失败蒸馏也须分别归一，不能把两类轨迹混成一种标签。 教学例子：某次编译输出提示先修依赖，提醒针对紧接着的动作；之后依赖已解决，就不应在每轮都继续把它当未完成约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-03709a88439f630e">OPRD的局部提醒为什么只作用于对应观察的下一轮，不能永久留在教师上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoprd-reminder">OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部提醒描述某个观察触发的短期约束，过期后继续保留会影响无关后续决策。全局提醒与局部提醒作用域不同，教师重评同一学生前缀而非另生成答案；部署学生不带提醒。成功自模仿与失败蒸馏也须分别归一，不能把两类轨迹混成一种标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某次编译输出提示先修依赖，提醒针对紧接着的动作；之后依赖已解决，就不应在每轮都继续把它当未完成约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21496v1">原论文</a> · <a href="../../../../post-training/2610.21496-oprd-reminder/">实现解读</a> · <a href="#qa-03709a88439f630e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd-reminder" data-paper-title="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents LLM 后训练 Tsinghua University 2026-10-15 编码 Agent 的最终通过/失败不能指出哪一轮忽略了已有约束。OPRD 在学生自己生成的无提醒轨迹上训练：成功轨迹自模仿；失败轨迹由教师读取训练专用提醒，重新评分同一学生前缀，不是教师另生成一条答案。全局提醒持续有效，观测对应的局部提醒只在下一轮有效，之后必须移除。正式推理去掉教师和全部提醒。原文 §3 完整实验成本过高，不复现（审查 DONE）。奇偶校验只用于构造诊断 outcome，不是编码正确性。L1 算法组件，不是 SWE-bench 编码能力复现。已实现作用域、同前缀评分和训练目标；完整实验成本过高，不复现（审查 DONE）。不进入 evolve 晋级。本地使用随机初始化的128词表、12维 causal cumulative-embedding 策略。每步真实采样8条三轮轨迹、每轮2个 token；奇偶校验只用于构造诊断 outcome，不是编码正确性。教师重新读取相同 response 前缀；学生上下文不含提醒。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 全局提醒与观测后的局部提醒有效范围有何不同？ 全局持续生效，局部只作用该观测后的下一轮，之后移除。永久保留局部信息会改变教师条件，也可能把后续不相关步骤误导成同一约束。 例如一次报错的修复提示只应影响下一次尝试，不应永远挂在所有轮次上。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-48dbec89ac3890dd">全局提醒与观测后的局部提醒有效范围有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoprd-reminder">OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局持续生效，局部只作用该观测后的下一轮，之后移除。永久保留局部信息会改变教师条件，也可能把后续不相关步骤误导成同一约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次报错的修复提示只应影响下一次尝试，不应永远挂在所有轮次上。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21496v1">原论文</a> · <a href="../../../../post-training/2610.21496-oprd-reminder/">实现解读</a> · <a href="#qa-48dbec89ac3890dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd-reminder" data-paper-title="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents LLM 后训练 Tsinghua University 2026-10-15 编码 Agent 的最终通过/失败不能指出哪一轮忽略了已有约束。OPRD 在学生自己生成的无提醒轨迹上训练：成功轨迹自模仿；失败轨迹由教师读取训练专用提醒，重新评分同一学生前缀，不是教师另生成一条答案。全局提醒持续有效，观测对应的局部提醒只在下一轮有效，之后必须移除。正式推理去掉教师和全部提醒。原文 §3 完整实验成本过高，不复现（审查 DONE）。奇偶校验只用于构造诊断 outcome，不是编码正确性。L1 算法组件，不是 SWE-bench 编码能力复现。已实现作用域、同前缀评分和训练目标；完整实验成本过高，不复现（审查 DONE）。不进入 evolve 晋级。本地使用随机初始化的128词表、12维 causal cumulative-embedding 策略。每步真实采样8条三轮轨迹、每轮2个 token；奇偶校验只用于构造诊断 outcome，不是编码正确性。教师重新读取相同 response 前缀；学生上下文不含提醒。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 提醒OPRD Top-100支持如何选，教师何时刷新？ 以双方logp逐项最大值选同一支持并各自归一，不是分别top100。教师在训练规定进度刷新，其余冻结；每轨迹先平均，成功失败分支再分别平均。 例如两边支持集合不同，逐坐标KL就不再比较同一事件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d293ce6549e892f4">提醒OPRD Top-100支持如何选，教师何时刷新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoprd-reminder">OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>以双方logp逐项最大值选同一支持并各自归一，不是分别top100。教师在训练规定进度刷新，其余冻结；每轨迹先平均，成功失败分支再分别平均。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两边支持集合不同，逐坐标KL就不再比较同一事件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21496v1">原论文</a> · <a href="../../../../post-training/2610.21496-oprd-reminder/">实现解读</a> · <a href="#qa-d293ce6549e892f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:shared-residual-distillation" data-paper-title="Learning from Unverified Peers via Shared Residual Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Unverified Peers via Shared Residual Distillation LLM 后训练 Shanghai Jiao Tong University 2026-10-15 没有标准答案或可验证 reward 时，整段错误解答也可能包含有用步骤。SRD 不投票选“正确答案”，而比较同题 peers 相对跨题 control 对 token 分布的改变，只接收多位 peer 共同支持的保守残差。学生仍只读取题目与自己的前缀，训练后的推理不需要 peers。 完整多模型实验成本过高，不复现（审查 DONE）；L1 公式、采样隔离与梯度组件，不是数学能力复现。完整多模型实验成本过高，不复现（审查 DONE）；本地不下载 Qwen、不调用外部教师，不进入 evolve 晋级。使用固定两个整数 prompt、8-token vocabulary、随机初始化的 causal cumulative-embedding 小策略。每个更新重新实际采样每题四条长度四的轨迹；均匀保留两个 peers，余下作为 targets；control 来自另一题。冻结初始策略逐前缀读取各上下文，学生不读 peer/control 或标准答案。  On-policy self-distillation 后训练算法组件 SRD LLM 后训练 教师与纠错：额外信息何时能帮到学生 SRD为何不用peer多数票挑一个正确答案？ 无验证反馈时peer可能全错，仍可包含共同有用局部信息。比较同题peer与跨题control的残差，只接收同向最小幅度，避免把整条未验答案封为正确示范。 例如多条失败推理共享一个合理中间转换，可只吸收保守局部变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-shared-residual-distillation-a834c6f2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2437a16c7225567d">SRD为何不用peer多数票挑一个正确答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ashared-residual-distillation">Learning from Unverified Peers via Shared Residual Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>无验证反馈时peer可能全错，仍可包含共同有用局部信息。比较同题peer与跨题control的残差，只接收同向最小幅度，避免把整条未验答案封为正确示范。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如多条失败推理共享一个合理中间转换，可只吸收保守局部变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22080v1">原论文</a> · <a href="../../../../post-training/2610.22080-shared-residual-distillation/">实现解读</a> · <a href="#qa-2437a16c7225567d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:shared-residual-distillation" data-paper-title="Learning from Unverified Peers via Shared Residual Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Unverified Peers via Shared Residual Distillation LLM 后训练 Shanghai Jiao Tong University 2026-10-15 没有标准答案或可验证 reward 时，整段错误解答也可能包含有用步骤。SRD 不投票选“正确答案”，而比较同题 peers 相对跨题 control 对 token 分布的改变，只接收多位 peer 共同支持的保守残差。学生仍只读取题目与自己的前缀，训练后的推理不需要 peers。 完整多模型实验成本过高，不复现（审查 DONE）；L1 公式、采样隔离与梯度组件，不是数学能力复现。完整多模型实验成本过高，不复现（审查 DONE）；本地不下载 Qwen、不调用外部教师，不进入 evolve 晋级。使用固定两个整数 prompt、8-token vocabulary、随机初始化的 causal cumulative-embedding 小策略。每个更新重新实际采样每题四条长度四的轨迹；均匀保留两个 peers，余下作为 targets；control 来自另一题。冻结初始策略逐前缀读取各上下文，学生不读 peer/control 或标准答案。  On-policy self-distillation 后训练算法组件 SRD LLM 后训练 教师与纠错：额外信息何时能帮到学生 SRD没有验证过的peer答案，为什么只接收多个peer同号的最小残差，而不多数投票选一整份解？ 整份错误答案仍可能含有可复用局部信号，同题peer相对跨题control的变化用于分离题目相关影响。只有同号部分取保守幅度，避免单个peer强推目标；学生仍只看自身前缀。共享残差不是正确性证明，也不能把target自己放回peer上下文制造自我支持。 教学例子：几份未验证推导都弱支持同一中间词，但对结论意见冲突；可以保留保守共同部分，而不宣布票最多的整份解正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fb763df961ba8600">SRD没有验证过的peer答案，为什么只接收多个peer同号的最小残差，而不多数投票选一整份解？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ashared-residual-distillation">Learning from Unverified Peers via Shared Residual Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整份错误答案仍可能含有可复用局部信号，同题peer相对跨题control的变化用于分离题目相关影响。只有同号部分取保守幅度，避免单个peer强推目标；学生仍只看自身前缀。共享残差不是正确性证明，也不能把target自己放回peer上下文制造自我支持。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>几份未验证推导都弱支持同一中间词，但对结论意见冲突；可以保留保守共同部分，而不宣布票最多的整份解正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22080v1">原论文</a> · <a href="../../../../post-training/2610.22080-shared-residual-distillation/">实现解读</a> · <a href="#qa-fb763df961ba8600">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:shared-residual-distillation" data-paper-title="Learning from Unverified Peers via Shared Residual Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Unverified Peers via Shared Residual Distillation LLM 后训练 Shanghai Jiao Tong University 2026-10-15 没有标准答案或可验证 reward 时，整段错误解答也可能包含有用步骤。SRD 不投票选“正确答案”，而比较同题 peers 相对跨题 control 对 token 分布的改变，只接收多位 peer 共同支持的保守残差。学生仍只读取题目与自己的前缀，训练后的推理不需要 peers。 完整多模型实验成本过高，不复现（审查 DONE）；L1 公式、采样隔离与梯度组件，不是数学能力复现。完整多模型实验成本过高，不复现（审查 DONE）；本地不下载 Qwen、不调用外部教师，不进入 evolve 晋级。使用固定两个整数 prompt、8-token vocabulary、随机初始化的 causal cumulative-embedding 小策略。每个更新重新实际采样每题四条长度四的轨迹；均匀保留两个 peers，余下作为 targets；control 来自另一题。冻结初始策略逐前缀读取各上下文，学生不读 peer/control 或标准答案。  On-policy self-distillation 后训练算法组件 SRD LLM 后训练 教师与纠错：额外信息何时能帮到学生 minmod保守残差与平均peer logits有什么差别？ 只有所有peer同号才保留最小幅度，否则归零，平均可让强意见覆盖冲突。它减少冒进但不证明共同信号正确，同源peer仍可能共享偏差。 例如两人正向一人负向时，保守门控不让多数高幅度直接压过异议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fc3074a967131230">minmod保守残差与平均peer logits有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ashared-residual-distillation">Learning from Unverified Peers via Shared Residual Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有所有peer同号才保留最小幅度，否则归零，平均可让强意见覆盖冲突。它减少冒进但不证明共同信号正确，同源peer仍可能共享偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两人正向一人负向时，保守门控不让多数高幅度直接压过异议。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22080v1">原论文</a> · <a href="../../../../post-training/2610.22080-shared-residual-distillation/">实现解读</a> · <a href="#qa-fc3074a967131230">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:shared-residual-distillation" data-paper-title="Learning from Unverified Peers via Shared Residual Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Unverified Peers via Shared Residual Distillation LLM 后训练 Shanghai Jiao Tong University 2026-10-15 没有标准答案或可验证 reward 时，整段错误解答也可能包含有用步骤。SRD 不投票选“正确答案”，而比较同题 peers 相对跨题 control 对 token 分布的改变，只接收多位 peer 共同支持的保守残差。学生仍只读取题目与自己的前缀，训练后的推理不需要 peers。 完整多模型实验成本过高，不复现（审查 DONE）；L1 公式、采样隔离与梯度组件，不是数学能力复现。完整多模型实验成本过高，不复现（审查 DONE）；本地不下载 Qwen、不调用外部教师，不进入 evolve 晋级。使用固定两个整数 prompt、8-token vocabulary、随机初始化的 causal cumulative-embedding 小策略。每个更新重新实际采样每题四条长度四的轨迹；均匀保留两个 peers，余下作为 targets；control 来自另一题。冻结初始策略逐前缀读取各上下文，学生不读 peer/control 或标准答案。  On-policy self-distillation 后训练算法组件 SRD LLM 后训练 教师与纠错：额外信息何时能帮到学生 SRD逐坐标cap为什么允许surrogate为负？ 截的是带符号单词表坐标贡献，不是总KL；负局部项可存在。中心化权重用q0而非control，target自己不可进入peer，全部教师和目标冻结。 例如把负坐标裁成零会改变目标，而不是仅改善数值稳定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1f73fc7a75f99e03">SRD逐坐标cap为什么允许surrogate为负？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ashared-residual-distillation">Learning from Unverified Peers via Shared Residual Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>截的是带符号单词表坐标贡献，不是总KL；负局部项可存在。中心化权重用q0而非control，target自己不可进入peer，全部教师和目标冻结。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把负坐标裁成零会改变目标，而不是仅改善数值稳定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22080v1">原论文</a> · <a href="../../../../post-training/2610.22080-shared-residual-distillation/">实现解读</a> · <a href="#qa-1f73fc7a75f99e03">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tf-opd" data-paper-title="Training-Free On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Training-Free On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-15 共同初始化的专家模型，其线性层融合可以写成匹配各教师输出的最小二乘。关键不是任意协方差，而是每个教师在自己生成的、经过终止和循环筛选的答案上实际遇到的输入二阶矩；统计按 token 数归一，不能让长答案自然压倒其他领域。 完整实验成本过高，不复现（审查 DONE）；L1 公式组件与微型自回归诊断，不是完整论文复现。L1 公式组件与微型自回归诊断，不是完整论文复现。完整实验成本过高，不复现（审查 DONE）；adapter: null、evolve_integrated: false。公开 Hamlet（Gutenberg 1524），固定内容 revision 为 sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784。  多教师能力整合 后训练算法组件 TF-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 TF-OPD无训练融合为何仍需教师自生成数据？ 闭式线性融合依赖各教师实际访问输入的二阶矩，数据提供应匹配哪些输出的统计，而不是对所有权重任意平均。无梯度训练不等于无生成与校准成本。 例如两个专家在不同输入子空间工作，统计能反映各自常用方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-tf-opd-c139b549" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0898ca99dc7454b0">TF-OPD无训练融合为何仍需教师自生成数据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atf-opd">Training-Free On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>闭式线性融合依赖各教师实际访问输入的二阶矩，数据提供应匹配哪些输出的统计，而不是对所有权重任意平均。无梯度训练不等于无生成与校准成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个专家在不同输入子空间工作，统计能反映各自常用方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22236v1">原论文</a> · <a href="../../../../post-training/2610.22236-tf-opd/">实现解读</a> · <a href="#qa-0898ca99dc7454b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tf-opd" data-paper-title="Training-Free On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Training-Free On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-15 共同初始化的专家模型，其线性层融合可以写成匹配各教师输出的最小二乘。关键不是任意协方差，而是每个教师在自己生成的、经过终止和循环筛选的答案上实际遇到的输入二阶矩；统计按 token 数归一，不能让长答案自然压倒其他领域。 完整实验成本过高，不复现（审查 DONE）；L1 公式组件与微型自回归诊断，不是完整论文复现。L1 公式组件与微型自回归诊断，不是完整论文复现。完整实验成本过高，不复现（审查 DONE）；adapter: null、evolve_integrated: false。公开 Hamlet（Gutenberg 1524），固定内容 revision 为 sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784。  多教师能力整合 后训练算法组件 TF-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 TF-OPD为什么收集每个教师自己生成答案时的输入二阶矩，而不随便用一份公共协方差？ 闭式融合要匹配教师在自身实际访问输入上的输出，二阶矩定义了哪些方向的误差重要。换成任意公共统计会改变最小二乘目标；自然终止与循环过滤、token归一也影响支持。无训练指不做梯度蒸馏，并不意味着不需要生成、回读和线性求解成本。 教学例子：两个专家使用不同领域的输入方向，统一协方差可能忽略其中一个领域；各自真实轨迹统计才能反映这种支持差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c2ec17d36f032bf9">TF-OPD为什么收集每个教师自己生成答案时的输入二阶矩，而不随便用一份公共协方差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atf-opd">Training-Free On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>闭式融合要匹配教师在自身实际访问输入上的输出，二阶矩定义了哪些方向的误差重要。换成任意公共统计会改变最小二乘目标；自然终止与循环过滤、token归一也影响支持。无训练指不做梯度蒸馏，并不意味着不需要生成、回读和线性求解成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个专家使用不同领域的输入方向，统一协方差可能忽略其中一个领域；各自真实轨迹统计才能反映这种支持差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22236v1">原论文</a> · <a href="../../../../post-training/2610.22236-tf-opd/">实现解读</a> · <a href="#qa-c2ec17d36f032bf9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tf-opd" data-paper-title="Training-Free On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Training-Free On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-15 共同初始化的专家模型，其线性层融合可以写成匹配各教师输出的最小二乘。关键不是任意协方差，而是每个教师在自己生成的、经过终止和循环筛选的答案上实际遇到的输入二阶矩；统计按 token 数归一，不能让长答案自然压倒其他领域。 完整实验成本过高，不复现（审查 DONE）；L1 公式组件与微型自回归诊断，不是完整论文复现。L1 公式组件与微型自回归诊断，不是完整论文复现。完整实验成本过高，不复现（审查 DONE）；adapter: null、evolve_integrated: false。公开 Hamlet（Gutenberg 1524），固定内容 revision 为 sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784。  多教师能力整合 后训练算法组件 TF-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 相同Gram时闭式融合与task vector求和有何差别？ 相同统计下应退化成加权平均更新，直接求和会放大幅度。正交输入支持时又可恢复各自功能，说明融合依赖统计而非固定一种加法。 例如两个相同专家不应合成两倍任务变化，合理退化要保持平均。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f6678e5697a58a0f">相同Gram时闭式融合与task vector求和有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atf-opd">Training-Free On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同统计下应退化成加权平均更新，直接求和会放大幅度。正交输入支持时又可恢复各自功能，说明融合依赖统计而非固定一种加法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个相同专家不应合成两倍任务变化，合理退化要保持平均。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22236v1">原论文</a> · <a href="../../../../post-training/2610.22236-tf-opd/">实现解读</a> · <a href="#qa-f6678e5697a58a0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tf-opd" data-paper-title="Training-Free On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Training-Free On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-15 共同初始化的专家模型，其线性层融合可以写成匹配各教师输出的最小二乘。关键不是任意协方差，而是每个教师在自己生成的、经过终止和循环筛选的答案上实际遇到的输入二阶矩；统计按 token 数归一，不能让长答案自然压倒其他领域。 完整实验成本过高，不复现（审查 DONE）；L1 公式组件与微型自回归诊断，不是完整论文复现。L1 公式组件与微型自回归诊断，不是完整论文复现。完整实验成本过高，不复现（审查 DONE）；adapter: null、evolve_integrated: false。公开 Hamlet（Gutenberg 1524），固定内容 revision 为 sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784。  多教师能力整合 后训练算法组件 TF-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 TF-OPD的Gram应由谁生成的哪些响应估计？ 各教师回读自己生成且通过终止循环筛选的响应，按token归一。求解用FP64线性方程而非显式逆，hook需清理；任意随机协方差不代表真实教师统计。 例如拿学生生成文本测教师Gram，已经改变原本的访问分布条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-40ed8419c11180ff">TF-OPD的Gram应由谁生成的哪些响应估计？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atf-opd">Training-Free On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各教师回读自己生成且通过终止循环筛选的响应，按token归一。求解用FP64线性方程而非显式逆，hook需清理；任意随机协方差不代表真实教师统计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如拿学生生成文本测教师Gram，已经改变原本的访问分布条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22236v1">原论文</a> · <a href="../../../../post-training/2610.22236-tf-opd/">实现解读</a> · <a href="#qa-40ed8419c11180ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:token-teacher-selection" data-paper-title="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation LLM 后训练 Princeton University 2026-10-15 一个教师未必适合学生整段推理：数学推导和代码生成可能需要不同专家，强教师与学生的分布差距也可能太大。论文把 OPD 的教师选择细化到每个学生实际访问的前缀。路由依据可以是教师置信度、师生分布 Hellinger 距离，或对齐隐藏空间的特征平方距离。软路由混合的是概率，不是 logits 或 log-prob 的平均。原文 §3 原文中理论分解和实验表分别讨论教师能力、师生距离和多样性；不要把原文“存在不劣路由”的可能性结论读成每个路由启发式都保证更优。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。三个随机初始化的32词表、8维 causal 策略分别作为学生和两个冻结教师。学生真实采样4-token响应，所有教师评分相同前缀；默认三次更新依次执行 entropy、Hellinger、features 三个准则。使用随机模型，不能衡量真实教师能力或 kernel 正确率。  On-policy distillation 多教师与路由 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 逐token选教师为什么优于固定整段教师这一假设有吸引力？ 同一回答可能涉及不同专长，且强教师与学生距离也可不同，按学生实际前缀选能更有针对性。吸引力是机制动机，不保证每个路由启发式都更优。 例如代码片段与数学解释可能需要不同专家指导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-token-teacher-selection-efd8fec8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d55cda5621b9a491">逐token选教师为什么优于固定整段教师这一假设有吸引力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atoken-teacher-selection">Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一回答可能涉及不同专长，且强教师与学生距离也可不同，按学生实际前缀选能更有针对性。吸引力是机制动机，不保证每个路由启发式都更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如代码片段与数学解释可能需要不同专家指导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21234v1">原论文</a> · <a href="../../../../post-training/2610.21234-token-teacher-selection/">实现解读</a> · <a href="#qa-d55cda5621b9a491">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:token-teacher-selection" data-paper-title="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation LLM 后训练 Princeton University 2026-10-15 一个教师未必适合学生整段推理：数学推导和代码生成可能需要不同专家，强教师与学生的分布差距也可能太大。论文把 OPD 的教师选择细化到每个学生实际访问的前缀。路由依据可以是教师置信度、师生分布 Hellinger 距离，或对齐隐藏空间的特征平方距离。软路由混合的是概率，不是 logits 或 log-prob 的平均。原文 §3 原文中理论分解和实验表分别讨论教师能力、师生距离和多样性；不要把原文“存在不劣路由”的可能性结论读成每个路由启发式都保证更优。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。三个随机初始化的32词表、8维 causal 策略分别作为学生和两个冻结教师。学生真实采样4-token响应，所有教师评分相同前缀；默认三次更新依次执行 entropy、Hellinger、features 三个准则。使用随机模型，不能衡量真实教师能力或 kernel 正确率。  On-policy distillation 多教师与路由 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 逐token软选教师时，为什么平均教师概率与平均logits不是一回事？ 概率算术混合表示在教师分布之间分配权重，logits或log-prob平均再归一则形成另一种组合，尤其在意见冲突和尾部差异时不同。路由依据还需区分置信、分布距离与对齐表征；强教师并非每个前缀都合适，启发式选择没有普遍更优保证。 教学例子：数学专家和代码专家各自确信不同续写，各取部分概率质量与取两者共同支持的几何组合，会给学生不同目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f07bd4fdf3bcc63d">逐token软选教师时，为什么平均教师概率与平均logits不是一回事？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atoken-teacher-selection">Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>概率算术混合表示在教师分布之间分配权重，logits或log-prob平均再归一则形成另一种组合，尤其在意见冲突和尾部差异时不同。路由依据还需区分置信、分布距离与对齐表征；强教师并非每个前缀都合适，启发式选择没有普遍更优保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>数学专家和代码专家各自确信不同续写，各取部分概率质量与取两者共同支持的几何组合，会给学生不同目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21234v1">原论文</a> · <a href="../../../../post-training/2610.21234-token-teacher-selection/">实现解读</a> · <a href="#qa-f07bd4fdf3bcc63d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:token-teacher-selection" data-paper-title="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation LLM 后训练 Princeton University 2026-10-15 一个教师未必适合学生整段推理：数学推导和代码生成可能需要不同专家，强教师与学生的分布差距也可能太大。论文把 OPD 的教师选择细化到每个学生实际访问的前缀。路由依据可以是教师置信度、师生分布 Hellinger 距离，或对齐隐藏空间的特征平方距离。软路由混合的是概率，不是 logits 或 log-prob 的平均。原文 §3 原文中理论分解和实验表分别讨论教师能力、师生距离和多样性；不要把原文“存在不劣路由”的可能性结论读成每个路由启发式都保证更优。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。三个随机初始化的32词表、8维 causal 策略分别作为学生和两个冻结教师。学生真实采样4-token响应，所有教师评分相同前缀；默认三次更新依次执行 entropy、Hellinger、features 三个准则。使用随机模型，不能衡量真实教师能力或 kernel 正确率。  On-policy distillation 多教师与路由 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 置信、Hellinger距离与隐藏距离路由各假设什么？ 置信偏好教师确定，分布距离偏好与学生兼容，隐藏距离要求特征空间已对齐；三者测量不同。尤其隐藏维数不同不能直接相减，低距离也不等于高正确率。 例如一个很自信但离学生能力太远的教师，可能被不同规则赋不同权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e6832747bbabf135">置信、Hellinger距离与隐藏距离路由各假设什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atoken-teacher-selection">Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>置信偏好教师确定，分布距离偏好与学生兼容，隐藏距离要求特征空间已对齐；三者测量不同。尤其隐藏维数不同不能直接相减，低距离也不等于高正确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个很自信但离学生能力太远的教师，可能被不同规则赋不同权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21234v1">原论文</a> · <a href="../../../../post-training/2610.21234-token-teacher-selection/">实现解读</a> · <a href="#qa-e6832747bbabf135">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:token-teacher-selection" data-paper-title="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation LLM 后训练 Princeton University 2026-10-15 一个教师未必适合学生整段推理：数学推导和代码生成可能需要不同专家，强教师与学生的分布差距也可能太大。论文把 OPD 的教师选择细化到每个学生实际访问的前缀。路由依据可以是教师置信度、师生分布 Hellinger 距离，或对齐隐藏空间的特征平方距离。软路由混合的是概率，不是 logits 或 log-prob 的平均。原文 §3 原文中理论分解和实验表分别讨论教师能力、师生距离和多样性；不要把原文“存在不劣路由”的可能性结论读成每个路由启发式都保证更优。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。三个随机初始化的32词表、8维 causal 策略分别作为学生和两个冻结教师。学生真实采样4-token响应，所有教师评分相同前缀；默认三次更新依次执行 entropy、Hellinger、features 三个准则。使用随机模型，不能衡量真实教师能力或 kernel 正确率。  On-policy distillation 多教师与路由 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 软路由混合概率还是平均logits，τ为零怎样处理？ 按教师概率算术混合，平均logits会变几何式目标；τ零明确硬argmax而不做除零。路由和目标冻结，本地是sampled-token版，未实现Top-K KL版本。 例如两教师各支持不同模式，概率平均与logit平均会给不同质量分配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e36bfbfb2f297f76">软路由混合概率还是平均logits，τ为零怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atoken-teacher-selection">Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按教师概率算术混合，平均logits会变几何式目标；τ零明确硬argmax而不做除零。路由和目标冻结，本地是sampled-token版，未实现Top-K KL版本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两教师各支持不同模式，概率平均与logit平均会给不同质量分配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21234v1">原论文</a> · <a href="../../../../post-training/2610.21234-token-teacher-selection/">实现解读</a> · <a href="#qa-e36bfbfb2f297f76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:waypoint-opd" data-paper-title="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation LLM 后训练 Alibaba Cloud Computing 2026-10-15 仅 initial/final 的 log-probability 位移不能区分“前后两段同向”与“中途反转”。同一 RL run 的 waypoint 只提供一致性证据，不是新的模仿目标。候选由学生 top-k 选择，early/late 位移先按候选学生权重中心化，再以正 cosine 缩放 endpoint credit。 完整实验成本过高，不复现（审查 DONE）；当 gates 全零且 KL 也无梯度时，runner 仍明确失败，并附 seed/step/诊断；L1 gate / dense PPO 组件与真实微型策略更新。完整实验成本过高，不复现（审查 DONE）；不是教师大模型训练重跑，也未集成 evolve。使用固定 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 分为 train/validation/test。  On-policy distillation 后训练算法组件 WAYPOINT-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Waypoint-OPD为什么需要同一教师RL中的中途checkpoint？ 初末变化无法分辨过程是否反转，waypoint提供早晚方向一致性证据，调节endpoint信用；它本身不是另一独立模仿目标。 例如先偏向A后来又转向B，与一路稳定转向B，终点差可以相似。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-waypoint-opd-30b78a3d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-00806496e3e63d41">Waypoint-OPD为什么需要同一教师RL中的中途checkpoint？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Awaypoint-opd">Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Cloud Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>初末变化无法分辨过程是否反转，waypoint提供早晚方向一致性证据，调节endpoint信用；它本身不是另一独立模仿目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先偏向A后来又转向B，与一路稳定转向B，终点差可以相似。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21601v1">原论文</a> · <a href="../../../../post-training/2610.21601-waypoint-opd/">实现解读</a> · <a href="#qa-00806496e3e63d41">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:waypoint-opd" data-paper-title="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation LLM 后训练 Alibaba Cloud Computing 2026-10-15 仅 initial/final 的 log-probability 位移不能区分“前后两段同向”与“中途反转”。同一 RL run 的 waypoint 只提供一致性证据，不是新的模仿目标。候选由学生 top-k 选择，early/late 位移先按候选学生权重中心化，再以正 cosine 缩放 endpoint credit。 完整实验成本过高，不复现（审查 DONE）；当 gates 全零且 KL 也无梯度时，runner 仍明确失败，并附 seed/step/诊断；L1 gate / dense PPO 组件与真实微型策略更新。完整实验成本过高，不复现（审查 DONE）；不是教师大模型训练重跑，也未集成 evolve。使用固定 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 分为 train/validation/test。  On-policy distillation 后训练算法组件 WAYPOINT-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Waypoint-OPD为什么用同次RL中间checkpoint作一致性门，而不把它作为另一个蒸馏目标？ 起点到终点的相同位移可能来自持续同向改进，也可能中途反转，waypoint用来辨认这两种历史。early与late位移在学生候选权重下中心化后比较方向，只缩放endpoint信用。中间模型不是额外要模仿的答案，低范数回退和冻结门控也属于定义。 教学例子：两个教师最终都提高同一词概率，一个一路提高，另一个先降后升；中间检查点能区分路径，但不必要求学生停在中间状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f5a0af895743a394">Waypoint-OPD为什么用同次RL中间checkpoint作一致性门，而不把它作为另一个蒸馏目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Awaypoint-opd">Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Cloud Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>起点到终点的相同位移可能来自持续同向改进，也可能中途反转，waypoint用来辨认这两种历史。early与late位移在学生候选权重下中心化后比较方向，只缩放endpoint信用。中间模型不是额外要模仿的答案，低范数回退和冻结门控也属于定义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个教师最终都提高同一词概率，一个一路提高，另一个先降后升；中间检查点能区分路径，但不必要求学生停在中间状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21601v1">原论文</a> · <a href="../../../../post-training/2610.21601-waypoint-opd/">实现解读</a> · <a href="#qa-f5a0af895743a394">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:waypoint-opd" data-paper-title="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation LLM 后训练 Alibaba Cloud Computing 2026-10-15 仅 initial/final 的 log-probability 位移不能区分“前后两段同向”与“中途反转”。同一 RL run 的 waypoint 只提供一致性证据，不是新的模仿目标。候选由学生 top-k 选择，early/late 位移先按候选学生权重中心化，再以正 cosine 缩放 endpoint credit。 完整实验成本过高，不复现（审查 DONE）；当 gates 全零且 KL 也无梯度时，runner 仍明确失败，并附 seed/step/诊断；L1 gate / dense PPO 组件与真实微型策略更新。完整实验成本过高，不复现（审查 DONE）；不是教师大模型训练重跑，也未集成 evolve。使用固定 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 分为 train/validation/test。  On-policy distillation 后训练算法组件 WAYPOINT-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 正cosine一致性与只看endpoint幅度有何不同？ 幅度大可能来自反复摇摆，一致性关注中心化早晚位移是否同向。它只提供训练路径线索，不保证方向正确，也不能用不同run的任意checkpoint拼成时序证据。 例如两段位移反向会降低gate，即使最终仍离初始很远。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e0952467fc9f0c25">正cosine一致性与只看endpoint幅度有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Awaypoint-opd">Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Cloud Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>幅度大可能来自反复摇摆，一致性关注中心化早晚位移是否同向。它只提供训练路径线索，不保证方向正确，也不能用不同run的任意checkpoint拼成时序证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两段位移反向会降低gate，即使最终仍离初始很远。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21601v1">原论文</a> · <a href="../../../../post-training/2610.21601-waypoint-opd/">实现解读</a> · <a href="#qa-e0952467fc9f0c25">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:waypoint-opd" data-paper-title="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation LLM 后训练 Alibaba Cloud Computing 2026-10-15 仅 initial/final 的 log-probability 位移不能区分“前后两段同向”与“中途反转”。同一 RL run 的 waypoint 只提供一致性证据，不是新的模仿目标。候选由学生 top-k 选择，early/late 位移先按候选学生权重中心化，再以正 cosine 缩放 endpoint credit。 完整实验成本过高，不复现（审查 DONE）；当 gates 全零且 KL 也无梯度时，runner 仍明确失败，并附 seed/step/诊断；L1 gate / dense PPO 组件与真实微型策略更新。完整实验成本过高，不复现（审查 DONE）；不是教师大模型训练重跑，也未集成 evolve。使用固定 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 分为 train/validation/test。  On-policy distillation 后训练算法组件 WAYPOINT-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Waypoint低范数时为什么gate回退为一而非零？ 缺少方向证据不等于存在冲突，规定范数很小时回退一；还需学生top-k权重中心化、有效前缀batch缩放。support、教师和优势冻结，候选不必被采样也可受梯度。 例如早段几乎不变，cosine无法稳定定义，不应因此自动删除全部endpoint信用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-df2d02d36c9b2aa5">Waypoint低范数时为什么gate回退为一而非零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Awaypoint-opd">Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Cloud Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缺少方向证据不等于存在冲突，规定范数很小时回退一；还需学生top-k权重中心化、有效前缀batch缩放。support、教师和优势冻结，候选不必被采样也可受梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如早段几乎不变，cosine无法稳定定义，不应因此自动删除全部endpoint信用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21601v1">原论文</a> · <a href="../../../../post-training/2610.21601-waypoint-opd/">实现解读</a> · <a href="#qa-df2d02d36c9b2aa5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rshd" data-paper-title="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight LLM 后训练 University of California, San Diego 2026-10-14 一组 GRPO rollout 全部失败时，组内 advantage 全为0。RSHD 不把参考答案告诉模型，而让同一策略根据失败响应写纠错 note，再用 note 生成新的 replay。只有 replay 通过率严格超过原组，note 才被接纳；之后蒸馏的也不是旧失败响应，而是 note 实际诱导的新续写。推理时只需无 note 学生。原文算法1–2 原文 Figure 2 展示上述完整数据流；Figure 1 说明难题组出现全失败的比例，不能拿它作为本地数据分布。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表因果模型按每题8条响应真实采样；末 token 余数条件只作人工二值 verifier。note writer 的输入只有原提示、失败响应和“失败”标记，不包含 reference token。诊断用精确 token 子序列筛查答案泄漏，重放每 note 两条、严格比较原组通过率，再均匀选取一条 replay 做真实同前缀双评分与梯度更新。  RLHF / RLVR On-policy distillation 失败重放与探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSHD为何要求note诱导的新replay确实改善通过率？ 反思文字看似合理未必能帮助行为，独立新采样把note质量落到可验证结果。只有严格高于原组才接纳，再蒸馏新续写，不把旧失败轨迹重新当示范。 例如复盘说要检查单位，但带note重试仍全错，就不因措辞好而收录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-rshd-81aa0b1d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d7d54bb36f3dc30d">RSHD为何要求note诱导的新replay确实改善通过率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arshd">Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反思文字看似合理未必能帮助行为，独立新采样把note质量落到可验证结果。只有严格高于原组才接纳，再蒸馏新续写，不把旧失败轨迹重新当示范。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如复盘说要检查单位，但带note重试仍全错，就不因措辞好而收录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21018v1">原论文</a> · <a href="../../../../post-training/2610.21018-rshd/">实现解读</a> · <a href="#qa-d7d54bb36f3dc30d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rshd" data-paper-title="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight LLM 后训练 University of California, San Diego 2026-10-14 一组 GRPO rollout 全部失败时，组内 advantage 全为0。RSHD 不把参考答案告诉模型，而让同一策略根据失败响应写纠错 note，再用 note 生成新的 replay。只有 replay 通过率严格超过原组，note 才被接纳；之后蒸馏的也不是旧失败响应，而是 note 实际诱导的新续写。推理时只需无 note 学生。原文算法1–2 原文 Figure 2 展示上述完整数据流；Figure 1 说明难题组出现全失败的比例，不能拿它作为本地数据分布。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表因果模型按每题8条响应真实采样；末 token 余数条件只作人工二值 verifier。note writer 的输入只有原提示、失败响应和“失败”标记，不包含 reference token。诊断用精确 token 子序列筛查答案泄漏，重放每 note 两条、严格比较原组通过率，再均匀选取一条 replay 做真实同前缀双评分与梯度更新。  RLHF / RLVR On-policy distillation 失败重放与探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSHD为什么必须用note生成新replay并验证通过率提高，而不直接蒸馏旧失败回答？ note是否有用要由它实际诱导的新行为检验，严格高于原组通过率才接纳。随后均匀选择接纳replay，在同前缀比较有无note的正lift，不只挑成功例。旧失败轨迹没有因此变正确，note也不能含gold；没有有效note时附加项为零。 教学例子：复盘建议听起来合理，但新生成仍全错，就不能把它当有效教师；一次事后解释不等于真的修复了行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-40c22840ad00279a">RSHD为什么必须用note生成新replay并验证通过率提高，而不直接蒸馏旧失败回答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arshd">Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>note是否有用要由它实际诱导的新行为检验，严格高于原组通过率才接纳。随后均匀选择接纳replay，在同前缀比较有无note的正lift，不只挑成功例。旧失败轨迹没有因此变正确，note也不能含gold；没有有效note时附加项为零。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>复盘建议听起来合理，但新生成仍全错，就不能把它当有效教师；一次事后解释不等于真的修复了行为。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21018v1">原论文</a> · <a href="../../../../post-training/2610.21018-rshd/">实现解读</a> · <a href="#qa-40c22840ad00279a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rshd" data-paper-title="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight LLM 后训练 University of California, San Diego 2026-10-14 一组 GRPO rollout 全部失败时，组内 advantage 全为0。RSHD 不把参考答案告诉模型，而让同一策略根据失败响应写纠错 note，再用 note 生成新的 replay。只有 replay 通过率严格超过原组，note 才被接纳；之后蒸馏的也不是旧失败响应，而是 note 实际诱导的新续写。推理时只需无 note 学生。原文算法1–2 原文 Figure 2 展示上述完整数据流；Figure 1 说明难题组出现全失败的比例，不能拿它作为本地数据分布。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表因果模型按每题8条响应真实采样；末 token 余数条件只作人工二值 verifier。note writer 的输入只有原提示、失败响应和“失败”标记，不包含 reference token。诊断用精确 token 子序列筛查答案泄漏，重放每 note 两条、严格比较原组通过率，再均匀选取一条 replay 做真实同前缀双评分与梯度更新。  RLHF / RLVR On-policy distillation 失败重放与探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSHD验证后均匀抽replay与只挑成功replay有什么区别？ 均匀抽样保留note诱导分布，挑成功会增加结果条件化选择偏差。note通过率已用于门控，不能再暗中只取最优响应，改变训练来源。 例如一组新重试有对有错，接纳后不等于允许只复制其中正确那条。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5feccb4a3af77e50">RSHD验证后均匀抽replay与只挑成功replay有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arshd">Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均匀抽样保留note诱导分布，挑成功会增加结果条件化选择偏差。note通过率已用于门控，不能再暗中只取最优响应，改变训练来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一组新重试有对有错，接纳后不等于允许只复制其中正确那条。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21018v1">原论文</a> · <a href="../../../../post-training/2610.21018-rshd/">实现解读</a> · <a href="#qa-5feccb4a3af77e50">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rshd" data-paper-title="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight LLM 后训练 University of California, San Diego 2026-10-14 一组 GRPO rollout 全部失败时，组内 advantage 全为0。RSHD 不把参考答案告诉模型，而让同一策略根据失败响应写纠错 note，再用 note 生成新的 replay。只有 replay 通过率严格超过原组，note 才被接纳；之后蒸馏的也不是旧失败响应，而是 note 实际诱导的新续写。推理时只需无 note 学生。原文算法1–2 原文 Figure 2 展示上述完整数据流；Figure 1 说明难题组出现全失败的比例，不能拿它作为本地数据分布。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表因果模型按每题8条响应真实采样；末 token 余数条件只作人工二值 verifier。note writer 的输入只有原提示、失败响应和“失败”标记，不包含 reference token。诊断用精确 token 子序列筛查答案泄漏，重放每 note 两条、严格比较原组通过率，再均匀选取一条 replay 做真实同前缀双评分与梯度更新。  RLHF / RLVR On-policy distillation 失败重放与探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSHD零lift token是否算入辅助项分母？ 算入接纳replay的全部有效词元，零lift也计数。无接纳note时附加项严格零，teacher和lift停止梯度；训练note不能从参考答案构造。 例如只按正lift数平均会放大稀少权重，偏离原归一协议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-27d881c9240abcc4">RSHD零lift token是否算入辅助项分母？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arshd">Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>算入接纳replay的全部有效词元，零lift也计数。无接纳note时附加项严格零，teacher和lift停止梯度；训练note不能从参考答案构造。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只按正lift数平均会放大稀少权重，偏离原归一协议。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21018v1">原论文</a> · <a href="../../../../post-training/2610.21018-rshd/">实现解读</a> · <a href="#qa-27d881c9240abcc4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:loopsd" data-paper-title="LoOPSD: On-Policy Self-Distillation with Looped Teachers" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LoOPSD: On-Policy Self-Distillation with Looped Teachers LLM 后训练 Anhui Province Key Laboratory of Digital Security 2026-10-13 在线自蒸馏需要比学生更有用的教师，但更大外部模型或额外答案上下文并非唯一来源。LoOPSD在不改权重时搜索重复层区间来构造教师，用学生自产前缀进行蒸馏，再从更新后的学生重新搜索下一轮教师。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Appendix A：全部连续层区间先筛128题，24条候选再评872题，前5与标准路径评独立100题；每轮200updates×12题×4responses、每响应上限1024tokens，最多10轮。以Qwen3-1.7B/4B/8B等重复教师计算，完整路线搜索和OPD总预算明显较高；这是上限/配置推断而非实测时长，不做昂贵探针。  on-policy-self-distillation layer-route-search iterative-teacher LLM 后训练 教师与纠错：额外信息何时能帮到学生 LoOPSD为什么通过重复层构造教师而不换更大权重？ 相同参数执行更深的循环路径可能提供更有用预测，搜索连续重复区间形成教师，再在学生自身前缀蒸馏。额外能力来源是计算路径，不是新外部答案。 例如同一组中层再走一遍，参数没增加，但每词执行层数增加。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-loopsd-e562cd53" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2bac65d4d7df1a33">LoOPSD为什么通过重复层构造教师而不换更大权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aloopsd">LoOPSD: On-Policy Self-Distillation with Looped Teachers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Anhui Province Key Laboratory of Digital Security</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同参数执行更深的循环路径可能提供更有用预测，搜索连续重复区间形成教师，再在学生自身前缀蒸馏。额外能力来源是计算路径，不是新外部答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一组中层再走一遍，参数没增加，但每词执行层数增加。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.18162">原论文</a> · <a href="../../../../reproductions/2610.18162-loopsd/">实现解读</a> · <a href="#qa-2bac65d4d7df1a33">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:loopsd" data-paper-title="LoOPSD: On-Policy Self-Distillation with Looped Teachers" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LoOPSD: On-Policy Self-Distillation with Looped Teachers LLM 后训练 Anhui Province Key Laboratory of Digital Security 2026-10-13 在线自蒸馏需要比学生更有用的教师，但更大外部模型或额外答案上下文并非唯一来源。LoOPSD在不改权重时搜索重复层区间来构造教师，用学生自产前缀进行蒸馏，再从更新后的学生重新搜索下一轮教师。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Appendix A：全部连续层区间先筛128题，24条候选再评872题，前5与标准路径评独立100题；每轮200updates×12题×4responses、每响应上限1024tokens，最多10轮。以Qwen3-1.7B/4B/8B等重复教师计算，完整路线搜索和OPD总预算明显较高；这是上限/配置推断而非实测时长，不做昂贵探针。  on-policy-self-distillation layer-route-search iterative-teacher LLM 后训练 教师与纠错：额外信息何时能帮到学生 LoOPSD不新增权重而重复一段网络层，为什么仍有教师成本，也需要独立validation选路由？ 重复层改变计算路径和条件分布，可形成更有用的教师，但每token要额外执行这些层，搜索还会多次评估候选。只按独立validation选择优于标准路径的路由，再在学生自身前缀蒸馏；test不能参与选择，无新参数也不代表免费或保证更强。 教学例子：同一本笔记再读关键章节可能改善理解，但耗时增加；挑哪段重复应在开发题验证，不能看最终考试答案来选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-54a2b1d469f3558f">LoOPSD不新增权重而重复一段网络层，为什么仍有教师成本，也需要独立validation选路由？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aloopsd">LoOPSD: On-Policy Self-Distillation with Looped Teachers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Anhui Province Key Laboratory of Digital Security</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重复层改变计算路径和条件分布，可形成更有用的教师，但每token要额外执行这些层，搜索还会多次评估候选。只按独立validation选择优于标准路径的路由，再在学生自身前缀蒸馏；test不能参与选择，无新参数也不代表免费或保证更强。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一本笔记再读关键章节可能改善理解，但耗时增加；挑哪段重复应在开发题验证，不能看最终考试答案来选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.18162">原论文</a> · <a href="../../../../reproductions/2610.18162-loopsd/">实现解读</a> · <a href="#qa-54a2b1d469f3558f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:loopsd" data-paper-title="LoOPSD: On-Policy Self-Distillation with Looped Teachers" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LoOPSD: On-Policy Self-Distillation with Looped Teachers LLM 后训练 Anhui Province Key Laboratory of Digital Security 2026-10-13 在线自蒸馏需要比学生更有用的教师，但更大外部模型或额外答案上下文并非唯一来源。LoOPSD在不改权重时搜索重复层区间来构造教师，用学生自产前缀进行蒸馏，再从更新后的学生重新搜索下一轮教师。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Appendix A：全部连续层区间先筛128题，24条候选再评872题，前5与标准路径评独立100题；每轮200updates×12题×4responses、每响应上限1024tokens，最多10轮。以Qwen3-1.7B/4B/8B等重复教师计算，完整路线搜索和OPD总预算明显较高；这是上限/配置推断而非实测时长，不做昂贵探针。  on-policy-self-distillation layer-route-search iterative-teacher LLM 后训练 教师与纠错：额外信息何时能帮到学生 每轮重搜loop教师与固定初始loop路径有什么区别？ 学生更新后最优重复区间可能变化，重搜让教师跟随当前模型；固定路径不具这条适应。只有独立验证优于标准路才继续，不能用测试集选路由。 例如原先有效的中层重复在学生学会后可能不再有益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ec091fc879a2e050">每轮重搜loop教师与固定初始loop路径有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aloopsd">LoOPSD: On-Policy Self-Distillation with Looped Teachers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Anhui Province Key Laboratory of Digital Security</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生更新后最优重复区间可能变化，重搜让教师跟随当前模型；固定路径不具这条适应。只有独立验证优于标准路才继续，不能用测试集选路由。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原先有效的中层重复在学生学会后可能不再有益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.18162">原论文</a> · <a href="../../../../reproductions/2610.18162-loopsd/">实现解读</a> · <a href="#qa-ec091fc879a2e050">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:loopsd" data-paper-title="LoOPSD: On-Policy Self-Distillation with Looped Teachers" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LoOPSD: On-Policy Self-Distillation with Looped Teachers LLM 后训练 Anhui Province Key Laboratory of Digital Security 2026-10-13 在线自蒸馏需要比学生更有用的教师，但更大外部模型或额外答案上下文并非唯一来源。LoOPSD在不改权重时搜索重复层区间来构造教师，用学生自产前缀进行蒸馏，再从更新后的学生重新搜索下一轮教师。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Appendix A：全部连续层区间先筛128题，24条候选再评872题，前5与标准路径评独立100题；每轮200updates×12题×4responses、每响应上限1024tokens，最多10轮。以Qwen3-1.7B/4B/8B等重复教师计算，完整路线搜索和OPD总预算明显较高；这是上限/配置推断而非实测时长，不做昂贵探针。  on-policy-self-distillation layer-route-search iterative-teacher LLM 后训练 教师与纠错：额外信息何时能帮到学生 LoOPSD蒸馏时教师路由和权重是否一起求导？ 本轮两者固定，学生标准路径接受RKL更新；训练参考答案可用于允许的路由搜索，不能进入学生蒸馏生成。每词额外执行重复区间长度，成本需计入。 例如重复五层不是零成本教师，即使没有新参数也增加前向计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c26a3bcf42e94a53">LoOPSD蒸馏时教师路由和权重是否一起求导？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aloopsd">LoOPSD: On-Policy Self-Distillation with Looped Teachers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Anhui Province Key Laboratory of Digital Security</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本轮两者固定，学生标准路径接受RKL更新；训练参考答案可用于允许的路由搜索，不能进入学生蒸馏生成。每词额外执行重复区间长度，成本需计入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如重复五层不是零成本教师，即使没有新参数也增加前向计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.18162">原论文</a> · <a href="../../../../reproductions/2610.18162-loopsd/">实现解读</a> · <a href="#qa-c26a3bcf42e94a53">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cast-opd" data-paper-title="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation LLM 后训练 Taobao &amp; Tmall Group of Alibaba 2026-10-09 异构 tokenizer 的同一文本有不同分段，直接比较 token ID 无意义。CAST 先匹配实际解码文本，将教师 span 的总 log probability 均匀投影到学生 span，再按不确定性×局部平滑度分配 credit；未对齐位置通过初始学生 KL 限制漂移。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为未蒸馏的相同student checkpoint，实验组执行异构tokenizer文本span对齐与credit/anchor训练；本地弱teacher短运行不证明有效知识迁移，稳定相对提升不适用。  Cross-tokenizer distillation Token credit assignment Selective KL anchoring LLM 后训练 教师与纠错：额外信息何时能帮到学生 CAST为什么先按解码文本span对齐跨tokenizer监督？ 不同词元编号和切分不可逐位比较，文本等价span提供共同内容。教师span总logp再投影到学生span，才有可用信用对应，而非直接拼两边token表。 例如一个中文词两边分成不同片数，需先确认它们解码成同一文本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-cast-opd-cae7ae27" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-da0704fa87323c6b">CAST为什么先按解码文本span对齐跨tokenizer监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acast-opd">CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同词元编号和切分不可逐位比较，文本等价span提供共同内容。教师span总logp再投影到学生span，才有可用信用对应，而非直接拼两边token表。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个中文词两边分成不同片数，需先确认它们解码成同一文本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13257">原论文</a> · <a href="../../../../reproductions/2610.13257-cast-opd/">实现解读</a> · <a href="#qa-da0704fa87323c6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cast-opd" data-paper-title="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation LLM 后训练 Taobao &amp; Tmall Group of Alibaba 2026-10-09 异构 tokenizer 的同一文本有不同分段，直接比较 token ID 无意义。CAST 先匹配实际解码文本，将教师 span 的总 log probability 均匀投影到学生 span，再按不确定性×局部平滑度分配 credit；未对齐位置通过初始学生 KL 限制漂移。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为未蒸馏的相同student checkpoint，实验组执行异构tokenizer文本span对齐与credit/anchor训练；本地弱teacher短运行不证明有效知识迁移，稳定相对提升不适用。  Cross-tokenizer distillation Token credit assignment Selective KL anchoring LLM 后训练 教师与纠错：额外信息何时能帮到学生 CAST为什么先按解码文本span对齐，再把教师总log概率投到学生位置？ 异构tokenizer的ID和边界不同，逐位置比较没有共同事件含义。文本span提供对应范围，教师总分再投影并按不确定性与平滑度分配，保持chunk总信用；未对齐部分由初始学生锚定。对齐失败应明确保留边界，不能把不相关token硬凑成监督。 教学例子：教师用一个token表示词，学生拆成几段，不能把教师分数只给第一段；需要先确认两边解码的是同一文本范围。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8f5504a33d943aad">CAST为什么先按解码文本span对齐，再把教师总log概率投到学生位置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acast-opd">CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>异构tokenizer的ID和边界不同，逐位置比较没有共同事件含义。文本span提供对应范围，教师总分再投影并按不确定性与平滑度分配，保持chunk总信用；未对齐部分由初始学生锚定。对齐失败应明确保留边界，不能把不相关token硬凑成监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师用一个token表示词，学生拆成几段，不能把教师分数只给第一段；需要先确认两边解码的是同一文本范围。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13257">原论文</a> · <a href="../../../../reproductions/2610.13257-cast-opd/">实现解读</a> · <a href="#qa-8f5504a33d943aad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cast-opd" data-paper-title="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation LLM 后训练 Taobao &amp; Tmall Group of Alibaba 2026-10-09 异构 tokenizer 的同一文本有不同分段，直接比较 token ID 无意义。CAST 先匹配实际解码文本，将教师 span 的总 log probability 均匀投影到学生 span，再按不确定性×局部平滑度分配 credit；未对齐位置通过初始学生 KL 限制漂移。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为未蒸馏的相同student checkpoint，实验组执行异构tokenizer文本span对齐与credit/anchor训练；本地弱teacher短运行不证明有效知识迁移，稳定相对提升不适用。  Cross-tokenizer distillation Token credit assignment Selective KL anchoring LLM 后训练 教师与纠错：额外信息何时能帮到学生 CAST信用分配与CSD共同事件分布有何区别？ CAST把教师span分数投到学生位置再分配总credit，CSD构造包含REST的共同事件概率分布。二者对齐后的监督对象不同，不能因都跨tokenizer就互换公式。 例如保持一段总信用，与保持完整事件概率质量，是不同守恒对象。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b1393548f9b6b374">CAST信用分配与CSD共同事件分布有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acast-opd">CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CAST把教师span分数投到学生位置再分配总credit，CSD构造包含REST的共同事件概率分布。二者对齐后的监督对象不同，不能因都跨tokenizer就互换公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保持一段总信用，与保持完整事件概率质量，是不同守恒对象。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13257">原论文</a> · <a href="../../../../reproductions/2610.13257-cast-opd/">实现解读</a> · <a href="#qa-b1393548f9b6b374">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cast-opd" data-paper-title="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation LLM 后训练 Taobao &amp; Tmall Group of Alibaba 2026-10-09 异构 tokenizer 的同一文本有不同分段，直接比较 token ID 无意义。CAST 先匹配实际解码文本，将教师 span 的总 log probability 均匀投影到学生 span，再按不确定性×局部平滑度分配 credit；未对齐位置通过初始学生 KL 限制漂移。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为未蒸馏的相同student checkpoint，实验组执行异构tokenizer文本span对齐与credit/anchor训练；本地弱teacher短运行不证明有效知识迁移，稳定相对提升不适用。  Cross-tokenizer distillation Token credit assignment Selective KL anchoring LLM 后训练 教师与纠错：额外信息何时能帮到学生 CAST不确定性权重怎样保证chunk信用总量不变？ 先按不确定性与局部平滑度形成归一权重，再乘chunk总优势，使各位置之和等于总credit。未对齐位置用初始学生anchor，不可默默丢弃后宣称覆盖完整文本。 例如某位置权重大只改分配，不应让整段总优势额外增加。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cac37d3cbe163f6b">CAST不确定性权重怎样保证chunk信用总量不变？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acast-opd">CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先按不确定性与局部平滑度形成归一权重，再乘chunk总优势，使各位置之和等于总credit。未对齐位置用初始学生anchor，不可默默丢弃后宣称覆盖完整文本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某位置权重大只改分配，不应让整段总优势额外增加。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13257">原论文</a> · <a href="../../../../reproductions/2610.13257-cast-opd/">实现解读</a> · <a href="#qa-cac37d3cbe163f6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:road-mopd" data-paper-title="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation LLM 后训练 Nanjing University / JD.com 2026-10-09 多域只路由各自教师，不能防止共享参数更新损害其他能力。Road 用未路由教师在当前目标域的同一学生轨迹上给出兼容性证据，调节 token credit，再求真实辅助梯度，投影目标梯度但保留其范数下限。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为不投影的多教师OPD，实验组执行按域teacher路由与逐tensor预防式梯度投影；小型公开算术域运行是机制诊断，稳定相对提升不适用。  Multi-teacher distillation Gradient projection Cross-domain guarding LLM 后训练 教师与纠错：额外信息何时能帮到学生 Road-MOPD为什么查询未路由的其他教师？ 目标域更新共享参数仍可能损害其他域，只用该域教师无法监测。其他教师在同一学生轨迹上提供兼容性信号和真实辅助梯度，用于守护跨域能力。 例如数学批更新也可能影响代码行为，不能因为数据路由分开就假定互不干扰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-road-mopd-dfda03a0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d72be295b3638f74">Road-MOPD为什么查询未路由的其他教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aroad-mopd">Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University / JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标域更新共享参数仍可能损害其他域，只用该域教师无法监测。其他教师在同一学生轨迹上提供兼容性信号和真实辅助梯度，用于守护跨域能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数学批更新也可能影响代码行为，不能因为数据路由分开就假定互不干扰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13521">原论文</a> · <a href="../../../../reproductions/2610.13521-road-mopd/">实现解读</a> · <a href="#qa-d72be295b3638f74">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:road-mopd" data-paper-title="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation LLM 后训练 Nanjing University / JD.com 2026-10-09 多域只路由各自教师，不能防止共享参数更新损害其他能力。Road 用未路由教师在当前目标域的同一学生轨迹上给出兼容性证据，调节 token credit，再求真实辅助梯度，投影目标梯度但保留其范数下限。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为不投影的多教师OPD，实验组执行按域teacher路由与逐tensor预防式梯度投影；小型公开算术域运行是机制诊断，稳定相对提升不适用。  Multi-teacher distillation Gradient projection Cross-domain guarding LLM 后训练 教师与纠错：额外信息何时能帮到学生 Road-MOPD为什么让未路由教师在当前域轨迹上提供证据，还对目标梯度设范数下限？ 只听当前域教师可能通过共享参数损害其他域，辅助教师在同一学生状态上的兼容性提供保护线索。先调token信用再处理真实辅助梯度，冲突投影同时限制目标梯度被削弱程度。范数下限是取舍，不保证所有域同时改善，也不能用随手向量代替真实目标梯度。 教学例子：训练数学专家时，代码教师可检查同批前缀是否受到不利更新；完全删掉冲突方向又可能让数学任务几乎不再学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-71c3912df71c02aa">Road-MOPD为什么让未路由教师在当前域轨迹上提供证据，还对目标梯度设范数下限？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aroad-mopd">Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University / JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只听当前域教师可能通过共享参数损害其他域，辅助教师在同一学生状态上的兼容性提供保护线索。先调token信用再处理真实辅助梯度，冲突投影同时限制目标梯度被削弱程度。范数下限是取舍，不保证所有域同时改善，也不能用随手向量代替真实目标梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练数学专家时，代码教师可检查同批前缀是否受到不利更新；完全删掉冲突方向又可能让数学任务几乎不再学习。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13521">原论文</a> · <a href="../../../../reproductions/2610.13521-road-mopd/">实现解读</a> · <a href="#qa-71c3912df71c02aa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:road-mopd" data-paper-title="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation LLM 后训练 Nanjing University / JD.com 2026-10-09 多域只路由各自教师，不能防止共享参数更新损害其他能力。Road 用未路由教师在当前目标域的同一学生轨迹上给出兼容性证据，调节 token credit，再求真实辅助梯度，投影目标梯度但保留其范数下限。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为不投影的多教师OPD，实验组执行按域teacher路由与逐tensor预防式梯度投影；小型公开算术域运行是机制诊断，稳定相对提升不适用。  Multi-teacher distillation Gradient projection Cross-domain guarding LLM 后训练 教师与纠错：额外信息何时能帮到学生 Road信用门控与冲突梯度投影是否可互相替代？ 前者调节逐token监督强度，后者在参数梯度层处理冲突并保留目标梯度范数下限。两层机制不同，只有一个权重公式不构成完整Road。 例如局部分数看似兼容，共享参数梯度仍可能冲突，需要真实梯度检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ffa58a5632fef07f">Road信用门控与冲突梯度投影是否可互相替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aroad-mopd">Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University / JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者调节逐token监督强度，后者在参数梯度层处理冲突并保留目标梯度范数下限。两层机制不同，只有一个权重公式不构成完整Road。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如局部分数看似兼容，共享参数梯度仍可能冲突，需要真实梯度检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13521">原论文</a> · <a href="../../../../reproductions/2610.13521-road-mopd/">实现解读</a> · <a href="#qa-ffa58a5632fef07f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:road-mopd" data-paper-title="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation LLM 后训练 Nanjing University / JD.com 2026-10-09 多域只路由各自教师，不能防止共享参数更新损害其他能力。Road 用未路由教师在当前目标域的同一学生轨迹上给出兼容性证据，调节 token credit，再求真实辅助梯度，投影目标梯度但保留其范数下限。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为不投影的多教师OPD，实验组执行按域teacher路由与逐tensor预防式梯度投影；小型公开算术域运行是机制诊断，稳定相对提升不适用。  Multi-teacher distillation Gradient projection Cross-domain guarding LLM 后训练 教师与纠错：额外信息何时能帮到学生 Road投影为什么不能简单把冲突分量全部移除？ 规定选择最大可行投影强度，同时保证投影后范数不低于原范数某比例；全投影可能越过下限。辅助梯度必须实际算得，不能由registry标签或静态分数替代。 例如两梯度几乎反平行时，完全去平行分量会使目标更新几乎消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2aa17d83bd77ca58">Road投影为什么不能简单把冲突分量全部移除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aroad-mopd">Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University / JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规定选择最大可行投影强度，同时保证投影后范数不低于原范数某比例；全投影可能越过下限。辅助梯度必须实际算得，不能由registry标签或静态分数替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两梯度几乎反平行时，完全去平行分量会使目标更新几乎消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13521">原论文</a> · <a href="../../../../reproductions/2610.13521-road-mopd/">实现解读</a> · <a href="#qa-2aa17d83bd77ca58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:meta-opd" data-paper-title="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation LLM 后训练 East China Normal University 2026-10-08 轻量权重网络根据师生预测学习 token 监督权重。它通过一次可微虚拟学生更新后的参考解损失获得元梯度，再使用新权重执行真实学生更新。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  On-policy distillation Meta-learning LLM 后训练 教师与纠错：额外信息何时能帮到学生 MetaOPD为什么通过虚拟学生更新学习权重？ 仅看teacher gap不知哪些监督真正有用，虚拟更新后用训练参考解损失评价权重效果，元梯度学习分配规则，再用新权重做真实更新。 例如某词差距大但学它损害参考任务，元目标可降低其权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-meta-opd-c3af9659" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-385bc0a690ca1ca8">MetaOPD为什么通过虚拟学生更新学习权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ameta-opd">MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · East China Normal University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅看teacher gap不知哪些监督真正有用，虚拟更新后用训练参考解损失评价权重效果，元梯度学习分配规则，再用新权重做真实更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某词差距大但学它损害参考任务，元目标可降低其权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11989">原论文</a> · <a href="../../../../post-training/2610.11989-meta-opd/">实现解读</a> · <a href="#qa-385bc0a690ca1ca8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:meta-opd" data-paper-title="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation LLM 后训练 East China Normal University 2026-10-08 轻量权重网络根据师生预测学习 token 监督权重。它通过一次可微虚拟学生更新后的参考解损失获得元梯度，再使用新权重执行真实学生更新。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  On-policy distillation Meta-learning LLM 后训练 教师与纠错：额外信息何时能帮到学生 MetaOPD为什么需要一次可微虚拟学生更新，不能只按当前loss给token调权？ 当前loss大可能来自难噪声，未必对下游有益。虚拟更新让权重网络观察这些权重将怎样影响训练参考解损失，再取元梯度更新权重，随后执行真实学生步。参考解只在训练外层目标，描述特征和所用优化器状态也需按定义隔离，不能偷用测试答案。 教学例子：一个高loss词只是无关文风，另一个决定解题方向；虚拟试走一步后，可比较哪种加权更能帮助训练参考任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c3cd49e2f1d4159d">MetaOPD为什么需要一次可微虚拟学生更新，不能只按当前loss给token调权？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ameta-opd">MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · East China Normal University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前loss大可能来自难噪声，未必对下游有益。虚拟更新让权重网络观察这些权重将怎样影响训练参考解损失，再取元梯度更新权重，随后执行真实学生步。参考解只在训练外层目标，描述特征和所用优化器状态也需按定义隔离，不能偷用测试答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个高loss词只是无关文风，另一个决定解题方向；虚拟试走一步后，可比较哪种加权更能帮助训练参考任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11989">原论文</a> · <a href="../../../../post-training/2610.11989-meta-opd/">实现解读</a> · <a href="#qa-c3cd49e2f1d4159d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:meta-opd" data-paper-title="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation LLM 后训练 East China Normal University 2026-10-08 轻量权重网络根据师生预测学习 token 监督权重。它通过一次可微虚拟学生更新后的参考解损失获得元梯度，再使用新权重执行真实学生更新。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  On-policy distillation Meta-learning LLM 后训练 教师与纠错：额外信息何时能帮到学生 可微虚拟AdamW与先做一次真实更新再事后打分有什么区别？ 虚拟步骤保留到权重网络的计算关系用于元梯度，真实更新会修改学生状态且不自动提供该导数。优化器状态和顺序是算法定义，不是任意一步SGD都等价。 例如需要问这次假想更新受哪些权重影响，而非只比较更新前后一个数字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6660a79840557aed">可微虚拟AdamW与先做一次真实更新再事后打分有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ameta-opd">MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · East China Normal University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>虚拟步骤保留到权重网络的计算关系用于元梯度，真实更新会修改学生状态且不自动提供该导数。优化器状态和顺序是算法定义，不是任意一步SGD都等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如需要问这次假想更新受哪些权重影响，而非只比较更新前后一个数字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11989">原论文</a> · <a href="../../../../post-training/2610.11989-meta-opd/">实现解读</a> · <a href="#qa-6660a79840557aed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:meta-opd" data-paper-title="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation LLM 后训练 East China Normal University 2026-10-08 轻量权重网络根据师生预测学习 token 监督权重。它通过一次可微虚拟学生更新后的参考解损失获得元梯度，再使用新权重执行真实学生更新。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  On-policy distillation Meta-learning LLM 后训练 教师与纠错：额外信息何时能帮到学生 MetaOPD的74维描述与权重变换哪些部分detach？ 输入描述停止梯度，权重网络通过虚拟更新受元梯度；权重先逐响应中心化、tanh限制并单位均值归一。新权重再用于真实更新，参考解只用训练允许数据。 例如测试参考解不能用作外层目标，否则把最终评测变成选权监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-081c80386f8001e6">MetaOPD的74维描述与权重变换哪些部分detach？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ameta-opd">MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · East China Normal University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>输入描述停止梯度，权重网络通过虚拟更新受元梯度；权重先逐响应中心化、tanh限制并单位均值归一。新权重再用于真实更新，参考解只用训练允许数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试参考解不能用作外层目标，否则把最终评测变成选权监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11989">原论文</a> · <a href="../../../../post-training/2610.11989-meta-opd/">实现解读</a> · <a href="#qa-081c80386f8001e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sguid" data-paper-title="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution LLM 后训练 New York University 2026-10-08 语义相关不代表技能真正能够教会模型。SGUID 先从当前模型的已验证训练轨迹生成候选技能，再观察技能在蒸馏早期、晚期是否持续提供与验证器一致的信号。探测训练完成后恢复本轮初始权重，只用通过筛选的紧凑库重新训练；下一轮由更新后的模型重新产技能，不沿用固定手写库。 不复现原 all-linear rank-64、dropout=0.05、原技能生成提示或数学大赛收益。8 次真实梯度更新使 adapter 探测位移为 0.03139，但所有技能的早/晚积极教学次数均为 0，因而无技能入选，精确恢复本轮初始权重，未执行紧凑库训练和第二轮。Qwen3.5-9B 的固定扩展协议已在 A100 完成两轮、464 次真实梯度更新，技能筛选、权重恢复与重新蒸馏均通过机制核验。4 题 validation 的 EM 从 75% 降到 25%，前后均有 2 题截断；保留负结果。GPU 回执只证明 L1 有界机制执行，不证明能力提升。此前失败运行也保持原样归档。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 SGUID为什么看技能持续教学活动而不只语义相似？ 相关技能可能教不会学生，方法检查早晚期是否持续提供与verifier一致的信号，从当前验证轨迹生成并筛选技能。检索频率不是有效教学次数。 例如某技巧常被检索却一直给错方向，就不能因相关而永久保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-sguid-340394af" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9ff07f5766fc4cbf">SGUID为什么看技能持续教学活动而不只语义相似？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asguid">Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相关技能可能教不会学生，方法检查早晚期是否持续提供与verifier一致的信号，从当前验证轨迹生成并筛选技能。检索频率不是有效教学次数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某技巧常被检索却一直给错方向，就不能因相关而永久保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12367">原论文</a> · <a href="../../../../post-training/2610.12367-sguid/">实现解读</a> · <a href="#qa-9ff07f5766fc4cbf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sguid" data-paper-title="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution LLM 后训练 New York University 2026-10-08 语义相关不代表技能真正能够教会模型。SGUID 先从当前模型的已验证训练轨迹生成候选技能，再观察技能在蒸馏早期、晚期是否持续提供与验证器一致的信号。探测训练完成后恢复本轮初始权重，只用通过筛选的紧凑库重新训练；下一轮由更新后的模型重新产技能，不沿用固定手写库。 不复现原 all-linear rank-64、dropout=0.05、原技能生成提示或数学大赛收益。8 次真实梯度更新使 adapter 探测位移为 0.03139，但所有技能的早/晚积极教学次数均为 0，因而无技能入选，精确恢复本轮初始权重，未执行紧凑库训练和第二轮。Qwen3.5-9B 的固定扩展协议已在 A100 完成两轮、464 次真实梯度更新，技能筛选、权重恢复与重新蒸馏均通过机制核验。4 题 validation 的 EM 从 75% 降到 25%，前后均有 2 题截断；保留负结果。GPU 回执只证明 L1 有界机制执行，不证明能力提升。此前失败运行也保持原样归档。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 SGUID探测技能教学效果后，为什么恢复本轮初始权重，只用紧凑库重新训练？ 探测阶段同时尝试大量候选，若直接继承探测后模型，就无法区分筛选库与额外训练的作用。恢复起点后用筛中技能重训，才隔离课程选择效果；下一轮再由更新模型生成新技能。语义检索次数不是有效教学次数，早晚持续信号还要与verifier方向一致。 教学例子：测试十种解题提示已让学生多练许多题，若不恢复起点，就不能说后来提升只来自最终选中的两种提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a83dcc5631e0862a">SGUID探测技能教学效果后，为什么恢复本轮初始权重，只用紧凑库重新训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asguid">Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>探测阶段同时尝试大量候选，若直接继承探测后模型，就无法区分筛选库与额外训练的作用。恢复起点后用筛中技能重训，才隔离课程选择效果；下一轮再由更新模型生成新技能。语义检索次数不是有效教学次数，早晚持续信号还要与verifier方向一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>测试十种解题提示已让学生多练许多题，若不恢复起点，就不能说后来提升只来自最终选中的两种提示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12367">原论文</a> · <a href="../../../../post-training/2610.12367-sguid/">实现解读</a> · <a href="#qa-a83dcc5631e0862a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sguid" data-paper-title="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution LLM 后训练 New York University 2026-10-08 语义相关不代表技能真正能够教会模型。SGUID 先从当前模型的已验证训练轨迹生成候选技能，再观察技能在蒸馏早期、晚期是否持续提供与验证器一致的信号。探测训练完成后恢复本轮初始权重，只用通过筛选的紧凑库重新训练；下一轮由更新后的模型重新产技能，不沿用固定手写库。 不复现原 all-linear rank-64、dropout=0.05、原技能生成提示或数学大赛收益。8 次真实梯度更新使 adapter 探测位移为 0.03139，但所有技能的早/晚积极教学次数均为 0，因而无技能入选，精确恢复本轮初始权重，未执行紧凑库训练和第二轮。Qwen3.5-9B 的固定扩展协议已在 A100 完成两轮、464 次真实梯度更新，技能筛选、权重恢复与重新蒸馏均通过机制核验。4 题 validation 的 EM 从 75% 降到 25%，前后均有 2 题截断；保留负结果。GPU 回执只证明 L1 有界机制执行，不证明能力提升。此前失败运行也保持原样归档。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 SGUID探测后为何恢复本轮初始权重再正式训练？ 筛选过程本身已更新模型，恢复可让紧凑库正式训练不额外继承探测收益，保持轮内对照清楚。下一轮再从新模型产技能，不用固定手工库冒充共同演化。 例如探测看过所有技能后直接续训，会把被淘汰技能的影响也带入正式模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-97c4c173d0fb5f4f">SGUID探测后为何恢复本轮初始权重再正式训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asguid">Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>筛选过程本身已更新模型，恢复可让紧凑库正式训练不额外继承探测收益，保持轮内对照清楚。下一轮再从新模型产技能，不用固定手工库冒充共同演化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如探测看过所有技能后直接续训，会把被淘汰技能的影响也带入正式模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12367">原论文</a> · <a href="../../../../post-training/2610.12367-sguid/">实现解读</a> · <a href="#qa-97c4c173d0fb5f4f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sguid" data-paper-title="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution LLM 后训练 New York University 2026-10-08 语义相关不代表技能真正能够教会模型。SGUID 先从当前模型的已验证训练轨迹生成候选技能，再观察技能在蒸馏早期、晚期是否持续提供与验证器一致的信号。探测训练完成后恢复本轮初始权重，只用通过筛选的紧凑库重新训练；下一轮由更新后的模型重新产技能，不沿用固定手写库。 不复现原 all-linear rank-64、dropout=0.05、原技能生成提示或数学大赛收益。8 次真实梯度更新使 adapter 探测位移为 0.03139，但所有技能的早/晚积极教学次数均为 0，因而无技能入选，精确恢复本轮初始权重，未执行紧凑库训练和第二轮。Qwen3.5-9B 的固定扩展协议已在 A100 完成两轮、464 次真实梯度更新，技能筛选、权重恢复与重新蒸馏均通过机制核验。4 题 validation 的 EM 从 75% 降到 25%，前后均有 2 题截断；保留负结果。GPU 回执只证明 L1 有界机制执行，不证明能力提升。此前失败运行也保持原样归档。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 SGUID负系数可直接删掉吗，既有结果怎样保留？ 定义允许负教学信号，不可只保留正例改目标。筛选需检查早晚活动与质量条件，既有两轮执行后验证下降是负结果，不能因流程跑完称为能力提升。 例如后期信号衰减到不合格，不能只看早期有效就继续留库。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5ca77e8fe6c1a39f">SGUID负系数可直接删掉吗，既有结果怎样保留？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asguid">Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>定义允许负教学信号，不可只保留正例改目标。筛选需检查早晚活动与质量条件，既有两轮执行后验证下降是负结果，不能因流程跑完称为能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如后期信号衰减到不合格，不能只看早期有效就继续留库。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12367">原论文</a> · <a href="../../../../post-training/2610.12367-sguid/">实现解读</a> · <a href="#qa-5ca77e8fe6c1a39f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:where-opd" data-paper-title="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes LLM 后训练 Valeo.ai 2026-10-01 程序化合成场景自动给出对象身份和空间坐标；teacher 接收文本化空间特权信息，student 只看图像与问题，在自己的 on-policy token 上蒸馏 teacher。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  多模态后训练 OPD 空间引导 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Where-OPD为什么用合成场景的空间信息作教师条件？ 程序场景能自动给出对象与坐标，教师获得准确结构线索，学生仍只看图像问题。目的是把空间提示内化到视觉行为，而不是让学生部署时读取答案坐标。 例如教师知道两个物体位置，学生要从画面学会左右关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-where-opd-73f1d45e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c0798f7dbc5e175d">Where-OPD为什么用合成场景的空间信息作教师条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Awhere-opd">Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Valeo.ai</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>程序场景能自动给出对象与坐标，教师获得准确结构线索，学生仍只看图像问题。目的是把空间提示内化到视觉行为，而不是让学生部署时读取答案坐标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师知道两个物体位置，学生要从画面学会左右关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02117">原论文</a> · <a href="../../../../post-training/2610.02117-where-opd/">实现解读</a> · <a href="#qa-c0798f7dbc5e175d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:where-opd" data-paper-title="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes LLM 后训练 Valeo.ai 2026-10-01 程序化合成场景自动给出对象身份和空间坐标；teacher 接收文本化空间特权信息，student 只看图像与问题，在自己的 on-policy token 上蒸馏 teacher。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  多模态后训练 OPD 空间引导 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Where-OPD为什么让教师读文本化空间坐标，而学生只看图像与问题？ 合成场景提供可精确描述的对象身份和位置，作为训练期特权信息帮助教师在学生前缀上给监督。学生部署时不依赖这些坐标，所以不能把它们混入原始学生输入。空间mask与信息边界要保留，随机logits的KL检查不证明模型学会视觉空间推理。 教学例子：教师知道球在盒子左侧的精确坐标，学生只能从图像判断；训练可借教师纠偏，测试不能直接把坐标告诉学生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b4a2e2a2808d8743">Where-OPD为什么让教师读文本化空间坐标，而学生只看图像与问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Awhere-opd">Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Valeo.ai</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>合成场景提供可精确描述的对象身份和位置，作为训练期特权信息帮助教师在学生前缀上给监督。学生部署时不依赖这些坐标，所以不能把它们混入原始学生输入。空间mask与信息边界要保留，随机logits的KL检查不证明模型学会视觉空间推理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师知道球在盒子左侧的精确坐标，学生只能从图像判断；训练可借教师纠偏，测试不能直接把坐标告诉学生。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02117">原论文</a> · <a href="../../../../post-training/2610.02117-where-opd/">实现解读</a> · <a href="#qa-b4a2e2a2808d8743">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:where-opd" data-paper-title="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes LLM 后训练 Valeo.ai 2026-10-01 程序化合成场景自动给出对象身份和空间坐标；teacher 接收文本化空间特权信息，student 只看图像与问题，在自己的 on-policy token 上蒸馏 teacher。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  多模态后训练 OPD 空间引导 LLM 后训练 教师与纠错：额外信息何时能帮到学生 空间特权文本与普通纯文本蒸馏有什么差别？ 定义链路依赖真实场景图像与对应空间标签，单纯随机文本分布不能验证视觉落地。特权信息可帮助教师但不能证明学生真正看图，仍需独立视觉评估。 例如同一空间描述配错图像，公式仍可运行却失去教学意义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a6e6be5151119ef4">空间特权文本与普通纯文本蒸馏有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Awhere-opd">Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Valeo.ai</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>定义链路依赖真实场景图像与对应空间标签，单纯随机文本分布不能验证视觉落地。特权信息可帮助教师但不能证明学生真正看图，仍需独立视觉评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一空间描述配错图像，公式仍可运行却失去教学意义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02117">原论文</a> · <a href="../../../../post-training/2610.02117-where-opd/">实现解读</a> · <a href="#qa-a6e6be5151119ef4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:where-opd" data-paper-title="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes LLM 后训练 Valeo.ai 2026-10-01 程序化合成场景自动给出对象身份和空间坐标；teacher 接收文本化空间特权信息，student 只看图像与问题，在自己的 on-policy token 上蒸馏 teacher。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  多模态后训练 OPD 空间引导 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Where-OPD本地是否已经生成合成场景并加载MLLM？ 没有，只执行spatial mask下的教师KL参考核。mask须对齐学生实际生成位置，教师冻结，随机logits只支持公式诊断，不能报告为视觉空间提升。 例如给定左右两个数字logit不是一场真实看图推理实验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d953d9a8ea49d645">Where-OPD本地是否已经生成合成场景并加载MLLM？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Awhere-opd">Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Valeo.ai</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，只执行spatial mask下的教师KL参考核。mask须对齐学生实际生成位置，教师冻结，随机logits只支持公式诊断，不能报告为视觉空间提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给定左右两个数字logit不是一场真实看图推理实验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02117">原论文</a> · <a href="../../../../post-training/2610.02117-where-opd/">实现解读</a> · <a href="#qa-d953d9a8ea49d645">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:advisd" data-paper-title="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation LLM 后训练 University of Southern California 2026-09-29 冻结 executor，只训练 advisor；反思先提出修正，再对同一已记录 executor 响应分别计算有建议与无建议的平均 log-likelihood，只有影响幅度超过 donor-advice 校准阈值的决定才进入自蒸馏。 不调用 Gemini/Claude executor，未复现 BFCL-v3。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Advisor 自蒸馏 GRPO LLM 后训练 教师与纠错：额外信息何时能帮到学生 AdviSD为什么只训练advisor而冻结executor？ 目标是学会给固定强执行器有用建议，将改进归因到顾问而非同时改变执行器。多轮反思提供候选建议，但只有足够影响执行器决策的部分进入自蒸馏。 例如工具调用模型不改权重，只改善旁边提醒它检查参数的顾问。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-advisd-0fd17b91" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9689d817dbfc3cb9">AdviSD为什么只训练advisor而冻结executor？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadvisd">AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是学会给固定强执行器有用建议，将改进归因到顾问而非同时改变执行器。多轮反思提供候选建议，但只有足够影响执行器决策的部分进入自蒸馏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具调用模型不改权重，只改善旁边提醒它检查参数的顾问。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38142">原论文</a> · <a href="../../../../post-training/2609.38142-advisd/">实现解读</a> · <a href="#qa-9689d817dbfc3cb9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:advisd" data-paper-title="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation LLM 后训练 University of Southern California 2026-09-29 冻结 executor，只训练 advisor；反思先提出修正，再对同一已记录 executor 响应分别计算有建议与无建议的平均 log-likelihood，只有影响幅度超过 donor-advice 校准阈值的决定才进入自蒸馏。 不调用 Gemini/Claude executor，未复现 BFCL-v3。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Advisor 自蒸馏 GRPO LLM 后训练 教师与纠错：额外信息何时能帮到学生 AdviSD为什么固定同一条执行器回答，比较有无建议时的概率？ 固定回答能把差异集中到建议如何改变执行器对这条回答的偏好，避免两次生成的随机差异混入效果估计。顾问只学习超过校准阈值的反思建议，执行器保持冻结。概率提升是筛选信号，不等价于任务成功，阈值也依赖所用建议分布。 例如执行器已给出一次工具调用，分别在有建议和无建议的上下文中给这次调用打分；不另生成两次回答后直接相减。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6de6ac398dbe65f4">AdviSD为什么固定同一条执行器回答，比较有无建议时的概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadvisd">AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定回答能把差异集中到建议如何改变执行器对这条回答的偏好，避免两次生成的随机差异混入效果估计。顾问只学习超过校准阈值的反思建议，执行器保持冻结。概率提升是筛选信号，不等价于任务成功，阈值也依赖所用建议分布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如执行器已给出一次工具调用，分别在有建议和无建议的上下文中给这次调用打分；不另生成两次回答后直接相减。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38142">原论文</a> · <a href="../../../../post-training/2609.38142-advisd/">实现解读</a> · <a href="#qa-6de6ac398dbe65f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:advisd" data-paper-title="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation LLM 后训练 University of Southern California 2026-09-29 冻结 executor，只训练 advisor；反思先提出修正，再对同一已记录 executor 响应分别计算有建议与无建议的平均 log-likelihood，只有影响幅度超过 donor-advice 校准阈值的决定才进入自蒸馏。 不调用 Gemini/Claude executor，未复现 BFCL-v3。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Advisor 自蒸馏 GRPO LLM 后训练 教师与纠错：额外信息何时能帮到学生 建议有影响与建议提高成功率是一回事吗？ 不是，似然对照只测对同一记录响应的偏好改变，影响大小并不独立证明结果更好。donor校准筛掉弱变化，仍需任务评估检查有益性。 例如建议令执行器更喜欢原动作，但原动作本身也可能是错的。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f29a6d7748aa8d87">建议有影响与建议提高成功率是一回事吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadvisd">AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，似然对照只测对同一记录响应的偏好改变，影响大小并不独立证明结果更好。donor校准筛掉弱变化，仍需任务评估检查有益性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如建议令执行器更喜欢原动作，但原动作本身也可能是错的。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38142">原论文</a> · <a href="../../../../post-training/2609.38142-advisd/">实现解读</a> · <a href="#qa-f29a6d7748aa8d87">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:advisd" data-paper-title="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation LLM 后训练 University of Southern California 2026-09-29 冻结 executor，只训练 advisor；反思先提出修正，再对同一已记录 executor 响应分别计算有建议与无建议的平均 log-likelihood，只有影响幅度超过 donor-advice 校准阈值的决定才进入自蒸馏。 不调用 Gemini/Claude executor，未复现 BFCL-v3。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Advisor 自蒸馏 GRPO LLM 后训练 教师与纠错：额外信息何时能帮到学生 AdviSD有无建议对照能分别重新生成两条回答吗？ 不能替代固定记录响应的成对评分，否则随机生成差异混入建议效应。按同一响应有效词元均值计算，阈值来自donor绝对contrast分位，本地未调用真实executor。 例如一边生成长代码另一边生成短代码，分数差不再仅是上下文建议作用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6f3d700f9d4b64e0">AdviSD有无建议对照能分别重新生成两条回答吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadvisd">AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能替代固定记录响应的成对评分，否则随机生成差异混入建议效应。按同一响应有效词元均值计算，阈值来自donor绝对contrast分位，本地未调用真实executor。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一边生成长代码另一边生成短代码，分数差不再仅是上下文建议作用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38142">原论文</a> · <a href="../../../../post-training/2609.38142-advisd/">实现解读</a> · <a href="#qa-6f3d700f9d4b64e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lego-opd" data-paper-title="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation LLM 后训练 KAIST 2026-09-29 把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 factorized teacher composition；未加载 LLM/VLM teacher。执行 factorized teacher composition；未加载 LLM/VLM teacher。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  OPD 多模态后训练 teacher composition LLM 后训练 教师与纠错：额外信息何时能帮到学生 LEGO-OPD里的grounding likelihood可以直接当最终答案概率使用吗？ 它在分解中承担视觉证据因子的角色，最终教师目标还要结合语言先验并归一化。不能因为它也是一个分数，就把它解释成完整语言回答的后验置信度。先分清先验、证据因子与最终分布，才能正确读取两位专家的责任。 教学例子：视觉因子支持“红色”，语言先验约束当前句子可接什么词；只有组合并归一后才是最终词元分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-lego-opd-93f05fa7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d289372d6af6441f">LEGO-OPD里的grounding likelihood可以直接当最终答案概率使用吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alego-opd">LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它在分解中承担视觉证据因子的角色，最终教师目标还要结合语言先验并归一化。不能因为它也是一个分数，就把它解释成完整语言回答的后验置信度。先分清先验、证据因子与最终分布，才能正确读取两位专家的责任。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>视觉因子支持“红色”，语言先验约束当前句子可接什么词；只有组合并归一后才是最终词元分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00333">原论文</a> · <a href="../../../../post-training/2610.00333-lego-opd/">实现解读</a> · <a href="#qa-d289372d6af6441f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lego-opd" data-paper-title="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation LLM 后训练 KAIST 2026-09-29 把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 factorized teacher composition；未加载 LLM/VLM teacher。执行 factorized teacher composition；未加载 LLM/VLM teacher。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  OPD 多模态后训练 teacher composition LLM 后训练 教师与纠错：额外信息何时能帮到学生 LEGO-OPD为什么让语言专家给先验、视觉专家给似然，而不直接平均两个教师？ 语言专家负责一般词语和推理的先验，视觉专家提供与画面有关的证据修正；两者按专家乘积组成蒸馏目标，避免把视觉模型的语言偏差一起照搬。角色分解仍依赖视觉似然是否可靠，本地仅验证组合目标，不能据此认定已获得真实视觉能力。 例如识别杯子颜色时，语言专家让句子通顺，视觉专家提高画面所支持颜色的概率；这个例子解释分工，不代表实际识别成绩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0be0a85b3520122d">LEGO-OPD为什么让语言专家给先验、视觉专家给似然，而不直接平均两个教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alego-opd">LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言专家负责一般词语和推理的先验，视觉专家提供与画面有关的证据修正；两者按专家乘积组成蒸馏目标，避免把视觉模型的语言偏差一起照搬。角色分解仍依赖视觉似然是否可靠，本地仅验证组合目标，不能据此认定已获得真实视觉能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如识别杯子颜色时，语言专家让句子通顺，视觉专家提高画面所支持颜色的概率；这个例子解释分工，不代表实际识别成绩。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00333">原论文</a> · <a href="../../../../post-training/2610.00333-lego-opd/">实现解读</a> · <a href="#qa-0be0a85b3520122d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lego-opd" data-paper-title="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation LLM 后训练 KAIST 2026-09-29 把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 factorized teacher composition；未加载 LLM/VLM teacher。执行 factorized teacher composition；未加载 LLM/VLM teacher。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  OPD 多模态后训练 teacher composition LLM 后训练 教师与纠错：额外信息何时能帮到学生 LEGO-OPD把grounding权重α设为零，与只用视觉专家有什么区别？ 当α为零且概率计算有效时，视觉因子不再影响归一化结果，教师退化为语言先验，而不是视觉独占。只用视觉专家则移除了语言先验，是另一种目标。α控制证据因子的影响强度，不能被读成两个完整教师的投票比例。 教学例子：将视觉项的log贡献乘零后，剩下的是语言专家分数；并不会因为“零语言占比”而变成纯视觉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-16ed41f70e40a9e1">LEGO-OPD把grounding权重α设为零，与只用视觉专家有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alego-opd">LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当α为零且概率计算有效时，视觉因子不再影响归一化结果，教师退化为语言先验，而不是视觉独占。只用视觉专家则移除了语言先验，是另一种目标。α控制证据因子的影响强度，不能被读成两个完整教师的投票比例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>将视觉项的log贡献乘零后，剩下的是语言专家分数；并不会因为“零语言占比”而变成纯视觉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00333">原论文</a> · <a href="../../../../post-training/2610.00333-lego-opd/">实现解读</a> · <a href="#qa-16ed41f70e40a9e1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lego-opd" data-paper-title="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation LLM 后训练 KAIST 2026-09-29 把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 factorized teacher composition；未加载 LLM/VLM teacher。执行 factorized teacher composition；未加载 LLM/VLM teacher。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  OPD 多模态后训练 teacher composition LLM 后训练 教师与纠错：额外信息何时能帮到学生 LEGO本地是否真实加载语言与视觉专家？ 没有，只执行因子化目标组合。实现应对候选维度对齐、在log空间相加后归一，并区分视觉似然因子与完整VLM后验，不能把随机logits称为视觉能力。 例如两向量乘积能验公式，却没有让任何模型实际看图。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0d2bbd06c7f56d04">LEGO本地是否真实加载语言与视觉专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alego-opd">LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，只执行因子化目标组合。实现应对候选维度对齐、在log空间相加后归一，并区分视觉似然因子与完整VLM后验，不能把随机logits称为视觉能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两向量乘积能验公式，却没有让任何模型实际看图。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00333">原论文</a> · <a href="../../../../post-training/2610.00333-lego-opd/">实现解读</a> · <a href="#qa-0d2bbd06c7f56d04">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:maestro-opd" data-paper-title="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation LLM 后训练 Nanyang Technological University 2026-09-29 MAESTRO 用教师 top-k 覆盖度和 Bhattacharyya 相似度构造逐 token Policy Disagreement Score，并对靠近响应起点的位置加权；教师只在高分歧位置介入，减少整段 teacher rollout 的固定开销。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  On-policy distillation 教师介入 策略分歧 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MAESTRO为什么只在高分歧位置让教师介入？ 整段教师rollout昂贵，学生与教师top-k覆盖及相似度可定位更需要帮助的前缀，并偏重早期位置。介入策略是一种预算分配，不是所有分歧都等于学生错误。 例如开头分叉可能影响长后续，比末尾标点差异更值得有限教师计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-maestro-opd-551f210d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3338a9b96bec70e1">MAESTRO为什么只在高分歧位置让教师介入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amaestro-opd">From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整段教师rollout昂贵，学生与教师top-k覆盖及相似度可定位更需要帮助的前缀，并偏重早期位置。介入策略是一种预算分配，不是所有分歧都等于学生错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如开头分叉可能影响长后续，比末尾标点差异更值得有限教师计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37510">原论文</a> · <a href="../../../../post-training/2609.37510-maestro/">实现解读</a> · <a href="#qa-3338a9b96bec70e1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:maestro-opd" data-paper-title="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation LLM 后训练 Nanyang Technological University 2026-09-29 MAESTRO 用教师 top-k 覆盖度和 Bhattacharyya 相似度构造逐 token Policy Disagreement Score，并对靠近响应起点的位置加权；教师只在高分歧位置介入，减少整段 teacher rollout 的固定开销。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  On-policy distillation 教师介入 策略分歧 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MAESTRO为什么把top-k覆盖与Bhattacharyya相似度同时用于教师介入判断？ 覆盖衡量学生候选是否包含教师支持，归一化相似度再看共同支持中的质量分配，两者不能相互替代。分歧分数与靠前位置权重帮助集中有限教师介入预算。分歧高只是需要关注的线索，不保证教师一定正确，本地PDS算子也没有生成完整教师rollout。 教学例子：两模型top-k词完全相同，却给这些词很不一样的概率；只看候选是否重叠，会误判它们没有重要分歧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d66864e0fc2fc51c">MAESTRO为什么把top-k覆盖与Bhattacharyya相似度同时用于教师介入判断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amaestro-opd">From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>覆盖衡量学生候选是否包含教师支持，归一化相似度再看共同支持中的质量分配，两者不能相互替代。分歧分数与靠前位置权重帮助集中有限教师介入预算。分歧高只是需要关注的线索，不保证教师一定正确，本地PDS算子也没有生成完整教师rollout。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两模型top-k词完全相同，却给这些词很不一样的概率；只看候选是否重叠，会误判它们没有重要分歧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37510">原论文</a> · <a href="../../../../post-training/2609.37510-maestro/">实现解读</a> · <a href="#qa-d66864e0fc2fc51c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:maestro-opd" data-paper-title="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation LLM 后训练 Nanyang Technological University 2026-09-29 MAESTRO 用教师 top-k 覆盖度和 Bhattacharyya 相似度构造逐 token Policy Disagreement Score，并对靠近响应起点的位置加权；教师只在高分歧位置介入，减少整段 teacher rollout 的固定开销。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  On-policy distillation 教师介入 策略分歧 LLM 后训练 教师与纠错：额外信息何时能帮到学生 覆盖度与Bhattacharyya相似度为何要一起看？ 覆盖关心教师支持是否落在学生候选中，相似度关心共同支持内的质量分配；单独一个会漏掉另一类差异。高PDS不保证教师路线一定优质。 例如候选身份都相同却权重完全相反，仍应视为有明显分歧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2d65dccc35ab4180">覆盖度与Bhattacharyya相似度为何要一起看？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amaestro-opd">From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>覆盖关心教师支持是否落在学生候选中，相似度关心共同支持内的质量分配；单独一个会漏掉另一类差异。高PDS不保证教师路线一定优质。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选身份都相同却权重完全相反，仍应视为有明显分歧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37510">原论文</a> · <a href="../../../../post-training/2609.37510-maestro/">实现解读</a> · <a href="#qa-2d65dccc35ab4180">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:maestro-opd" data-paper-title="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation LLM 后训练 Nanyang Technological University 2026-09-29 MAESTRO 用教师 top-k 覆盖度和 Bhattacharyya 相似度构造逐 token Policy Disagreement Score，并对靠近响应起点的位置加权；教师只在高分歧位置介入，减少整段 teacher rollout 的固定开销。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  On-policy distillation 教师介入 策略分歧 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MAESTRO本地是否真的生成教师接管rollout？ 没有，只计算top-k覆盖、归一化相似度和PDS。真实介入还需模型生成、状态衔接与成本统计；不能从分数核通过推断已获得论文教师调用节约。 例如人工输入两份概率得到高分，不表示系统已执行一次教师帮助。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0d5b4623fbf3f723">MAESTRO本地是否真的生成教师接管rollout？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amaestro-opd">From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，只计算top-k覆盖、归一化相似度和PDS。真实介入还需模型生成、状态衔接与成本统计；不能从分数核通过推断已获得论文教师调用节约。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人工输入两份概率得到高分，不表示系统已执行一次教师帮助。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37510">原论文</a> · <a href="../../../../post-training/2609.37510-maestro/">实现解读</a> · <a href="#qa-0d5b4623fbf3f723">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pr-opd" data-paper-title="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning LLM 后训练 University of Florida 2026-09-29 GRPO warm start 后，策略为每条已完成轨迹写一条 hindsight skill，并对同一 response 做普通 context 与 skill context 两次 forward。后者是 stop-gradient teacher；PR-OPD 在每层、每个 response token 对齐投影 hidden state，再与 reward objective 组合。推理时 skill 和 teacher 分支都移除。 复现级别：L1 表征对齐目标。复现级别：L1 表征对齐目标。实现多层、多 response-token 的 stop-gradient privileged alignment。测试覆盖相同表征时零损失、不同表征时正损失、mask 与 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 ALFWorld/WebShop 或 GRPO warm start，不能宣称论文最高 +14.0 点结果。  Agentic RL On-policy distillation 表征对齐 LLM 后训练 教师与纠错：额外信息何时能帮到学生 PR-OPD为什么蒸馏表征而非只对最终token分布？ hindsight skill让同一模型形成特权表示，逐层逐响应位置对齐投影hidden state，可传递内部结构信号，再与任务奖励结合。skill只供训练教师，推理去掉。 例如成功后归纳的工具原则帮助教师内部表征，不直接成为部署输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-pr-opd-9c73d4f9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-59a45194479a55f0">PR-OPD为什么蒸馏表征而非只对最终token分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apr-opd">PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>hindsight skill让同一模型形成特权表示，逐层逐响应位置对齐投影hidden state，可传递内部结构信号，再与任务奖励结合。skill只供训练教师，推理去掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如成功后归纳的工具原则帮助教师内部表征，不直接成为部署输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36642">原论文</a> · <a href="../../../../post-training/2609.36642-pr-opd/">实现解读</a> · <a href="#qa-59a45194479a55f0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pr-opd" data-paper-title="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning LLM 后训练 University of Florida 2026-09-29 GRPO warm start 后，策略为每条已完成轨迹写一条 hindsight skill，并对同一 response 做普通 context 与 skill context 两次 forward。后者是 stop-gradient teacher；PR-OPD 在每层、每个 response token 对齐投影 hidden state，再与 reward objective 组合。推理时 skill 和 teacher 分支都移除。 复现级别：L1 表征对齐目标。复现级别：L1 表征对齐目标。实现多层、多 response-token 的 stop-gradient privileged alignment。测试覆盖相同表征时零损失、不同表征时正损失、mask 与 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 ALFWorld/WebShop 或 GRPO warm start，不能宣称论文最高 +14.0 点结果。  Agentic RL On-policy distillation 表征对齐 LLM 后训练 教师与纠错：额外信息何时能帮到学生 PR-OPD为什么对同一response做普通与hindsight skill两次forward，而不是直接模仿技能文本？ skill是完成轨迹后得到的训练专属视图，目标是比较它怎样改变同一响应各层各token表示，再蒸馏到无skill学生。若改成复制技能文本或另一条教师答案，就换了监督对象。教师分支停止梯度，并与任务奖励结合，推理时移除skill和教师。 教学例子：失败复盘总结“先验证工具返回格式”，可以让教师借此重新解释旧决策；学生训练后应在没有这条提示时自己做出判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ceecfd34d31cf4a4">PR-OPD为什么对同一response做普通与hindsight skill两次forward，而不是直接模仿技能文本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apr-opd">PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>skill是完成轨迹后得到的训练专属视图，目标是比较它怎样改变同一响应各层各token表示，再蒸馏到无skill学生。若改成复制技能文本或另一条教师答案，就换了监督对象。教师分支停止梯度，并与任务奖励结合，推理时移除skill和教师。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>失败复盘总结“先验证工具返回格式”，可以让教师借此重新解释旧决策；学生训练后应在没有这条提示时自己做出判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36642">原论文</a> · <a href="../../../../post-training/2609.36642-pr-opd/">实现解读</a> · <a href="#qa-ceecfd34d31cf4a4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pr-opd" data-paper-title="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning LLM 后训练 University of Florida 2026-09-29 GRPO warm start 后，策略为每条已完成轨迹写一条 hindsight skill，并对同一 response 做普通 context 与 skill context 两次 forward。后者是 stop-gradient teacher；PR-OPD 在每层、每个 response token 对齐投影 hidden state，再与 reward objective 组合。推理时 skill 和 teacher 分支都移除。 复现级别：L1 表征对齐目标。复现级别：L1 表征对齐目标。实现多层、多 response-token 的 stop-gradient privileged alignment。测试覆盖相同表征时零损失、不同表征时正损失、mask 与 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 ALFWorld/WebShop 或 GRPO warm start，不能宣称论文最高 +14.0 点结果。  Agentic RL On-policy distillation 表征对齐 LLM 后训练 教师与纠错：额外信息何时能帮到学生 PR-OPD两次forward与把skill直接拼给学生训练有什么区别？ 普通context学生与skill教师分开，教师stop-gradient；若学生也读skill，就改变部署条件并可能只学依赖提示。表征匹配也不等于输出答案监督。 例如评测不再提供skill时，学生应靠参数，而非靠训练期额外文字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e5d6558b0b26dd06">PR-OPD两次forward与把skill直接拼给学生训练有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apr-opd">PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通context学生与skill教师分开，教师stop-gradient；若学生也读skill，就改变部署条件并可能只学依赖提示。表征匹配也不等于输出答案监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如评测不再提供skill时，学生应靠参数，而非靠训练期额外文字。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36642">原论文</a> · <a href="../../../../post-training/2609.36642-pr-opd/">实现解读</a> · <a href="#qa-e5d6558b0b26dd06">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pr-opd" data-paper-title="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning LLM 后训练 University of Florida 2026-09-29 GRPO warm start 后，策略为每条已完成轨迹写一条 hindsight skill，并对同一 response 做普通 context 与 skill context 两次 forward。后者是 stop-gradient teacher；PR-OPD 在每层、每个 response token 对齐投影 hidden state，再与 reward objective 组合。推理时 skill 和 teacher 分支都移除。 复现级别：L1 表征对齐目标。复现级别：L1 表征对齐目标。实现多层、多 response-token 的 stop-gradient privileged alignment。测试覆盖相同表征时零损失、不同表征时正损失、mask 与 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 ALFWorld/WebShop 或 GRPO warm start，不能宣称论文最高 +14.0 点结果。  Agentic RL On-policy distillation 表征对齐 LLM 后训练 教师与纠错：额外信息何时能帮到学生 PR-OPD逐层投影hidden对齐需注意哪些mask？ 只对同一response有效词元和对应层处理，观察或padding不能算学生生成监督。skill来自已完成训练轨迹，不能把gold plan直接当自生成技能；本地核不代表完整Agent训练。 例如教师多出的skill token不与学生response按原位置硬对齐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1ed3d42bb6433d2a">PR-OPD逐层投影hidden对齐需注意哪些mask？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apr-opd">PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只对同一response有效词元和对应层处理，观察或padding不能算学生生成监督。skill来自已完成训练轨迹，不能把gold plan直接当自生成技能；本地核不代表完整Agent训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师多出的skill token不与学生response按原位置硬对齐。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36642">原论文</a> · <a href="../../../../post-training/2609.36642-pr-opd/">实现解读</a> · <a href="#qa-1ed3d42bb6433d2a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weakest-link" data-paper-title="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning LLM 后训练 Huawei Noah’s Ark Lab 2026-09-29 把教师对学生采样 token 的负对数概率当作成本，约束每个生成前缀的平均成本。一旦某个前缀越界，后续进入吸收惩罚状态，防止“先生成坏推理、再靠容易 token 拉低平均成本”；同时把即时奖励的全词表期望精确求导，降低只采样当前动作的方差。 L1 可微目标与优化诊断。L1 可微目标与优化诊断。真实执行全词表即时奖励梯度和未来 Monte Carlo 回报，不等于已蒸馏完整推理模型。API 输入一条无 padding 的 on-policy 轨迹，以及每个访问前缀的全词表教师 log-prob 和任务奖励。调用方负责真实教师/学生 rollout、变长批处理、基准和同预算对照；本次未接入完整 LLM 训练。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 对三动作学生策略训练 80 步 Adam，三个随机初始 seed；教师分布固定公开为 [0.7,0.29,0.01]，预算 2，惩罚 4。  教师前缀约束蒸馏 约束强化学习 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Weakest Link为什么要求每个前缀都满足平均成本约束？ 只看最终平均可先写坏推理，再靠后面容易词稀释。前缀约束首次违约后吸收惩罚，防止这种先破坏后补平均的策略。成本来自教师负logp。 例如前半很不受教师支持，后半加大量常见词也不能洗掉已发生违约。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-weakest-link-b901a370" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c7bd5b0d985d1030">Weakest Link为什么要求每个前缀都满足平均成本约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aweakest-link">The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah’s Ark Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只看最终平均可先写坏推理，再靠后面容易词稀释。前缀约束首次违约后吸收惩罚，防止这种先破坏后补平均的策略。成本来自教师负logp。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前半很不受教师支持，后半加大量常见词也不能洗掉已发生违约。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00332">原论文</a> · <a href="../../../../post-training/2610.00332-weakest-link/">实现解读</a> · <a href="#qa-c7bd5b0d985d1030">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weakest-link" data-paper-title="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning LLM 后训练 Huawei Noah’s Ark Lab 2026-09-29 把教师对学生采样 token 的负对数概率当作成本，约束每个生成前缀的平均成本。一旦某个前缀越界，后续进入吸收惩罚状态，防止“先生成坏推理、再靠容易 token 拉低平均成本”；同时把即时奖励的全词表期望精确求导，降低只采样当前动作的方差。 L1 可微目标与优化诊断。L1 可微目标与优化诊断。真实执行全词表即时奖励梯度和未来 Monte Carlo 回报，不等于已蒸馏完整推理模型。API 输入一条无 padding 的 on-policy 轨迹，以及每个访问前缀的全词表教师 log-prob 和任务奖励。调用方负责真实教师/学生 rollout、变长批处理、基准和同预算对照；本次未接入完整 LLM 训练。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 对三动作学生策略训练 80 步 Adam，三个随机初始 seed；教师分布固定公开为 [0.7,0.29,0.01]，预算 2，惩罚 4。  教师前缀约束蒸馏 约束强化学习 LLM 后训练 教师与纠错：额外信息何时能帮到学生 The Weakest Link为什么前缀一旦违约就持续惩罚，不能靠后面的容易token把平均成本拉回来？ 每个前缀都需满足教师成本约束，最终平均合格可能掩盖早期严重偏离。吸收惩罚阻止事后稀释，让关键链条受局部约束。反事实即时奖励只枚举真实访问前缀的当前动作，不能为每个候选编造不同历史；教师低概率仍不自动等于事实错误。 教学例子：先写一段极不受教师支持的错误推导，再追加很多常见词，可能降低整句平均成本；前缀约束不允许这样补票。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7923acb97ed47a03">The Weakest Link为什么前缀一旦违约就持续惩罚，不能靠后面的容易token把平均成本拉回来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aweakest-link">The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah’s Ark Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个前缀都需满足教师成本约束，最终平均合格可能掩盖早期严重偏离。吸收惩罚阻止事后稀释，让关键链条受局部约束。反事实即时奖励只枚举真实访问前缀的当前动作，不能为每个候选编造不同历史；教师低概率仍不自动等于事实错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先写一段极不受教师支持的错误推导，再追加很多常见词，可能降低整句平均成本；前缀约束不允许这样补票。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00332">原论文</a> · <a href="../../../../post-training/2610.00332-weakest-link/">实现解读</a> · <a href="#qa-7923acb97ed47a03">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weakest-link" data-paper-title="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning LLM 后训练 Huawei Noah’s Ark Lab 2026-09-29 把教师对学生采样 token 的负对数概率当作成本，约束每个生成前缀的平均成本。一旦某个前缀越界，后续进入吸收惩罚状态，防止“先生成坏推理、再靠容易 token 拉低平均成本”；同时把即时奖励的全词表期望精确求导，降低只采样当前动作的方差。 L1 可微目标与优化诊断。L1 可微目标与优化诊断。真实执行全词表即时奖励梯度和未来 Monte Carlo 回报，不等于已蒸馏完整推理模型。API 输入一条无 padding 的 on-policy 轨迹，以及每个访问前缀的全词表教师 log-prob 和任务奖励。调用方负责真实教师/学生 rollout、变长批处理、基准和同预算对照；本次未接入完整 LLM 训练。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 对三动作学生策略训练 80 步 Adam，三个随机初始 seed；教师分布固定公开为 [0.7,0.29,0.01]，预算 2，惩罚 4。  教师前缀约束蒸馏 约束强化学习 LLM 后训练 教师与纠错：额外信息何时能帮到学生 吸收惩罚与普通可恢复滑动平均门控有何不同？ 吸收标记一旦为真持续有效，不因后续平均回落恢复；滑动门控则可能重新放行。它是严格前缀约束选择，不说明教师成本与真实任务价值完全一致。 例如下一步写一个高概率词，不能把上一前缀的违规状态清除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-51efc32637c1fc66">吸收惩罚与普通可恢复滑动平均门控有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aweakest-link">The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah’s Ark Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>吸收标记一旦为真持续有效，不因后续平均回落恢复；滑动门控则可能重新放行。它是严格前缀约束选择，不说明教师成本与真实任务价值完全一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如下一步写一个高概率词，不能把上一前缀的违规状态清除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00332">原论文</a> · <a href="../../../../post-training/2610.00332-weakest-link/">实现解读</a> · <a href="#qa-51efc32637c1fc66">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weakest-link" data-paper-title="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning LLM 后训练 Huawei Noah’s Ark Lab 2026-09-29 把教师对学生采样 token 的负对数概率当作成本，约束每个生成前缀的平均成本。一旦某个前缀越界，后续进入吸收惩罚状态，防止“先生成坏推理、再靠容易 token 拉低平均成本”；同时把即时奖励的全词表期望精确求导，降低只采样当前动作的方差。 L1 可微目标与优化诊断。L1 可微目标与优化诊断。真实执行全词表即时奖励梯度和未来 Monte Carlo 回报，不等于已蒸馏完整推理模型。API 输入一条无 padding 的 on-policy 轨迹，以及每个访问前缀的全词表教师 log-prob 和任务奖励。调用方负责真实教师/学生 rollout、变长批处理、基准和同预算对照；本次未接入完整 LLM 训练。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 对三动作学生策略训练 80 步 Adam，三个随机初始 seed；教师分布固定公开为 [0.7,0.29,0.01]，预算 2，惩罚 4。  教师前缀约束蒸馏 约束强化学习 LLM 后训练 教师与纠错：额外信息何时能帮到学生 枚举反事实当前动作时能为每个动作更换历史成本吗？ 不能，都从真实访问前缀的已发生成本出发，只改变当前候选动作。即时奖励全词表期望可精确求导，未来回报仍采样；当前接口尚无完整语言模型训练。 例如给不喜欢的动作另造一段更坏历史，会人为改变其反事实评价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-18fe7c725ef08fd9">枚举反事实当前动作时能为每个动作更换历史成本吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aweakest-link">The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah’s Ark Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，都从真实访问前缀的已发生成本出发，只改变当前候选动作。即时奖励全词表期望可精确求导，未来回报仍采样；当前接口尚无完整语言模型训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给不喜欢的动作另造一段更坏历史，会人为改变其反事实评价。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00332">原论文</a> · <a href="../../../../post-training/2610.00332-weakest-link/">实现解读</a> · <a href="#qa-18fe7c725ef08fd9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mas-opd" data-paper-title="MAS-OPD: On-Policy Distillation for Multi-Agent Systems" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MAS-OPD: On-Policy Distillation for Multi-Agent Systems LLM 后训练 University of Science and Technology of China 2026-09-28 以目标角色与非目标角色 teacher 信号差构造 role advantage，并把协作冲突归因只提供给 teacher 形成 privileged coordination supervision。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  多 Agent On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 MAS-OPD为什么引入角色相关优势？ 团队结果难区分各成员责任，目标与非目标角色教师信号差提供局部协作监督。最终任务失败不应自动等量惩罚所有角色，角色归因质量仍需核验。 例如检索成功但汇总漏信息，应区分搜索与总结责任。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-mas-opd-e3c3be86" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0ff54511f31821a3">MAS-OPD为什么引入角色相关优势？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amas-opd">MAS-OPD: On-Policy Distillation for Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>团队结果难区分各成员责任，目标与非目标角色教师信号差提供局部协作监督。最终任务失败不应自动等量惩罚所有角色，角色归因质量仍需核验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如检索成功但汇总漏信息，应区分搜索与总结责任。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34234">原论文</a> · <a href="../../../../post-training/2609.34234-mas-opd/">实现解读</a> · <a href="#qa-0ff54511f31821a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mas-opd" data-paper-title="MAS-OPD: On-Policy Distillation for Multi-Agent Systems" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MAS-OPD: On-Policy Distillation for Multi-Agent Systems LLM 后训练 University of Science and Technology of China 2026-09-28 以目标角色与非目标角色 teacher 信号差构造 role advantage，并把协作冲突归因只提供给 teacher 形成 privileged coordination supervision。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  多 Agent On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 MAS-OPD为什么把角色冲突归因放进教师视图，而不是直接改所有角色的奖励？ 多角色协作失败时，整体奖励难以说明哪个角色应改变行为。教师借助额外冲突信息形成角色相关的优势信号，让目标角色与其他角色的贡献有所区分。额外归因属于训练期信息，本地只验证角色优势和掩码，不能当作多模型协作能力复现。 例如规划者路线合理但执行者选错工具，教师可把冲突归到执行动作；不能因为团队失败就同样惩罚规划和执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f1042ce3ff30e42a">MAS-OPD为什么把角色冲突归因放进教师视图，而不是直接改所有角色的奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amas-opd">MAS-OPD: On-Policy Distillation for Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多角色协作失败时，整体奖励难以说明哪个角色应改变行为。教师借助额外冲突信息形成角色相关的优势信号，让目标角色与其他角色的贡献有所区分。额外归因属于训练期信息，本地只验证角色优势和掩码，不能当作多模型协作能力复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规划者路线合理但执行者选错工具，教师可把冲突归到执行动作；不能因为团队失败就同样惩罚规划和执行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34234">原论文</a> · <a href="../../../../post-training/2609.34234-mas-opd/">实现解读</a> · <a href="#qa-f1042ce3ff30e42a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mas-opd" data-paper-title="MAS-OPD: On-Policy Distillation for Multi-Agent Systems" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MAS-OPD: On-Policy Distillation for Multi-Agent Systems LLM 后训练 University of Science and Technology of China 2026-09-28 以目标角色与非目标角色 teacher 信号差构造 role advantage，并把协作冲突归因只提供给 teacher 形成 privileged coordination supervision。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  多 Agent On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 协作冲突特权信息与直接给所有角色看完整归因有什么区别？ 原设计只让教师读取额外冲突说明，学生仍按自身公开角色历史行动。若所有学生先知道归因，会改变实际可用信息，并掩盖是否内化协作。 例如训练教师知道是哪位误解需求，部署成员不能预先拿到事后答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0ff64018a557f657">协作冲突特权信息与直接给所有角色看完整归因有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amas-opd">MAS-OPD: On-Policy Distillation for Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原设计只让教师读取额外冲突说明，学生仍按自身公开角色历史行动。若所有学生先知道归因，会改变实际可用信息，并掩盖是否内化协作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练教师知道是哪位误解需求，部署成员不能预先拿到事后答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34234">原论文</a> · <a href="../../../../post-training/2609.34234-mas-opd/">实现解读</a> · <a href="#qa-0ff64018a557f657">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mas-opd" data-paper-title="MAS-OPD: On-Policy Distillation for Multi-Agent Systems" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MAS-OPD: On-Policy Distillation for Multi-Agent Systems LLM 后训练 University of Science and Technology of China 2026-09-28 以目标角色与非目标角色 teacher 信号差构造 role advantage，并把协作冲突归因只提供给 teacher 形成 privileged coordination supervision。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  多 Agent On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 MAS-OPD本地role advantage是否包含真实多模型联训？ 没有，只验证角色优势与特权冲突mask。需对齐角色、轨迹和有效生成位置，不能把非目标角色分数误加到目标输出，也不能把registry映射叫团队训练完成。 例如数组里两角色交换顺序，计算可运行但信用会分给错误成员。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6a2f647ebe9aace5">MAS-OPD本地role advantage是否包含真实多模型联训？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amas-opd">MAS-OPD: On-Policy Distillation for Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，只验证角色优势与特权冲突mask。需对齐角色、轨迹和有效生成位置，不能把非目标角色分数误加到目标输出，也不能把registry映射叫团队训练完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数组里两角色交换顺序，计算可运行但信用会分给错误成员。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34234">原论文</a> · <a href="../../../../post-training/2609.34234-mas-opd/">实现解读</a> · <a href="#qa-6a2f647ebe9aace5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:olive" data-paper-title="Learning from Teacher Continuations at Student States" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Teacher Continuations at Student States LLM 后训练 University of Illinois Urbana-Champaign 2026-09-28 由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  在线蒸馏 Teacher continuation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OLIVE为什么让教师从学生到达的状态续写？ 学生错误分布与教师理想轨迹不同，在真实学生前缀上续写可提供更贴近部署状态的监督，帮助学习如何继续或修复，而非只背完整标准答案。 例如学生已走到不常见中间式，教师从这里接着完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-olive-4870752f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-be7936ba40a16330">OLIVE为什么让教师从学生到达的状态续写？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aolive">Learning from Teacher Continuations at Student States</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生错误分布与教师理想轨迹不同，在真实学生前缀上续写可提供更贴近部署状态的监督，帮助学习如何继续或修复，而非只背完整标准答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生已走到不常见中间式，教师从这里接着完成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36246">原论文</a> · <a href="../../../../post-training/2609.36246-olive/">实现解读</a> · <a href="#qa-be7936ba40a16330">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:olive" data-paper-title="Learning from Teacher Continuations at Student States" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Teacher Continuations at Student States LLM 后训练 University of Illinois Urbana-Champaign 2026-09-28 由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  在线蒸馏 Teacher continuation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OLIVE的学生前缀参与条件输入，为什么不一起计入监督损失？ 学生先生成前缀，教师从这个真实学生状态继续，监督只落在教师续写的词元上。这样既保留学生容易遇到的偏离状态，又不把学生自己写错的前缀当作正确标签。教师续写质量仍是前提，掩码正确也不能替代完整语言模型实验。 例如学生把计算写到一个可修复的中间步骤，教师接着纠正并完成；训练读取整段上下文，但只学习教师接续的部分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4d5768797235694a">OLIVE的学生前缀参与条件输入，为什么不一起计入监督损失？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aolive">Learning from Teacher Continuations at Student States</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生先生成前缀，教师从这个真实学生状态继续，监督只落在教师续写的词元上。这样既保留学生容易遇到的偏离状态，又不把学生自己写错的前缀当作正确标签。教师续写质量仍是前提，掩码正确也不能替代完整语言模型实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生把计算写到一个可修复的中间步骤，教师接着纠正并完成；训练读取整段上下文，但只学习教师接续的部分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36246">原论文</a> · <a href="../../../../post-training/2609.36246-olive/">实现解读</a> · <a href="#qa-4d5768797235694a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:olive" data-paper-title="Learning from Teacher Continuations at Student States" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Teacher Continuations at Student States LLM 后训练 University of Illinois Urbana-Champaign 2026-09-28 由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  在线蒸馏 Teacher continuation LLM 后训练 教师与纠错：额外信息何时能帮到学生 教师续写CE与教师给学生原token分布评分有何不同？ 前者新增教师生成的后缀作为监督文本，后者仍对学生实际采样token和状态评价。两者数据对象不同，不能把重评分核当成真实教师续写已执行。 例如教师接下来写了新步骤，与只给学生旧步骤打分，不是同一数据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-648e9cd502b8ce7a">教师续写CE与教师给学生原token分布评分有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aolive">Learning from Teacher Continuations at Student States</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者新增教师生成的后缀作为监督文本，后者仍对学生实际采样token和状态评价。两者数据对象不同，不能把重评分核当成真实教师续写已执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师接下来写了新步骤，与只给学生旧步骤打分，不是同一数据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36246">原论文</a> · <a href="../../../../post-training/2609.36246-olive/">实现解读</a> · <a href="#qa-648e9cd502b8ce7a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:olive" data-paper-title="Learning from Teacher Continuations at Student States" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Teacher Continuations at Student States LLM 后训练 University of Illinois Urbana-Champaign 2026-09-28 由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  在线蒸馏 Teacher continuation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OLIVE的prefix虽然不计loss，能从输入里删除吗？ 不能，它仍决定教师续写和学生监督条件；只关闭prefix目标mask。需要明确拼接边界、EOS和padding，当前本地仅验证精确mask，未调用闭源教师。 例如保留三步错误背景但不模仿这三步，才是在该学生状态继续学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-af1bd061756a9659">OLIVE的prefix虽然不计loss，能从输入里删除吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aolive">Learning from Teacher Continuations at Student States</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，它仍决定教师续写和学生监督条件；只关闭prefix目标mask。需要明确拼接边界、EOS和padding，当前本地仅验证精确mask，未调用闭源教师。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保留三步错误背景但不模仿这三步，才是在该学生状态继续学习。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36246">原论文</a> · <a href="../../../../post-training/2609.36246-olive/">实现解读</a> · <a href="#qa-af1bd061756a9659">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opd-aha" data-paper-title="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation LLM 后训练 Arizona State University / University of Virginia / Stevens Institute of Technology 2026-09-15 用真实视觉与空视觉教师分布之差重建视觉偏好目标，抑制错误语言前缀的惯性。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行目标重建公式；未加载多模态 checkpoint。本地执行目标重建公式；未加载多模态 checkpoint。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多模态后训练 On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPD-Aha所说语言惯性是什么？ 学生错误前缀可让教师顺着原说法继续，即使画面支持另一解释。真实与空视觉分布对照尝试找回视觉贡献，减少语言上下文压过证据。 例如前文写狗，图里却是猫，后续不能只跟随前文称呼。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-opd-aha-11a1ffc3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2931ec0c204282a6">OPD-Aha所说语言惯性是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopd-aha">OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University / University of Virginia / Stevens Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生错误前缀可让教师顺着原说法继续，即使画面支持另一解释。真实与空视觉分布对照尝试找回视觉贡献，减少语言上下文压过证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前文写狗，图里却是猫，后续不能只跟随前文称呼。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16459">原论文</a> · <a href="../../../../post-training/2609.16459-opd-aha/">实现解读</a> · <a href="#qa-2931ec0c204282a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opd-aha" data-paper-title="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation LLM 后训练 Arizona State University / University of Virginia / Stevens Institute of Technology 2026-09-15 用真实视觉与空视觉教师分布之差重建视觉偏好目标，抑制错误语言前缀的惯性。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行目标重建公式；未加载多模态 checkpoint。本地执行目标重建公式；未加载多模态 checkpoint。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多模态后训练 On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPD-Aha为何比较真实视觉输入与空视觉输入的教师分布？ 错误前缀可能让教师继续顺着语言惯性推理。把真实画面与空视觉条件下的输出对比，可以提取画面带来的偏好变化，再用它构造蒸馏目标。这个差异帮助区分视觉证据与语言先验，但不保证视觉教师本身正确；本地只是目标构造诊断。 例如前文误说图里是狗，教师在看到猫图与看不到图时的概率变化可突出猫的证据，而不是只复制带错前缀的整段回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4be5a9972445c455">OPD-Aha为何比较真实视觉输入与空视觉输入的教师分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopd-aha">OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University / University of Virginia / Stevens Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>错误前缀可能让教师继续顺着语言惯性推理。把真实画面与空视觉条件下的输出对比，可以提取画面带来的偏好变化，再用它构造蒸馏目标。这个差异帮助区分视觉证据与语言先验，但不保证视觉教师本身正确；本地只是目标构造诊断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前文误说图里是狗，教师在看到猫图与看不到图时的概率变化可突出猫的证据，而不是只复制带错前缀的整段回答。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16459">原论文</a> · <a href="../../../../post-training/2609.16459-opd-aha/">实现解读</a> · <a href="#qa-4be5a9972445c455">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opd-aha" data-paper-title="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation LLM 后训练 Arizona State University / University of Virginia / Stevens Institute of Technology 2026-09-15 用真实视觉与空视觉教师分布之差重建视觉偏好目标，抑制错误语言前缀的惯性。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行目标重建公式；未加载多模态 checkpoint。本地执行目标重建公式；未加载多模态 checkpoint。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多模态后训练 On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 真实/空视觉对照与直接增加教师置信有何区别？ 前者比较同教师在视觉条件变化下的差异，后者可能放大语言先验。对照也受空视觉构造与教师能力影响，不能保证所有改动都源于正确证据。 例如两视图都自信说狗，单纯锐化不会制造看见猫的能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ffb8e96a88323b0c">真实/空视觉对照与直接增加教师置信有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopd-aha">OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University / University of Virginia / Stevens Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者比较同教师在视觉条件变化下的差异，后者可能放大语言先验。对照也受空视觉构造与教师能力影响，不能保证所有改动都源于正确证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两视图都自信说狗，单纯锐化不会制造看见猫的能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16459">原论文</a> · <a href="../../../../post-training/2609.16459-opd-aha/">实现解读</a> · <a href="#qa-ffb8e96a88323b0c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opd-aha" data-paper-title="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation LLM 后训练 Arizona State University / University of Virginia / Stevens Institute of Technology 2026-09-15 用真实视觉与空视觉教师分布之差重建视觉偏好目标，抑制错误语言前缀的惯性。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行目标重建公式；未加载多模态 checkpoint。本地执行目标重建公式；未加载多模态 checkpoint。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多模态后训练 On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPD-Aha本地目标重建通过是否意味着运行了多模态checkpoint？ 不意味着，当前只有目标公式参考核。真实路径还需匹配视觉与空视觉输入、同一学生前缀及模型评分，不能用固定分布差直接报告看图反思效果。 例如人工设置猫概率升高，验证的是重建计算，不是模型自己发现了猫。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7a9393dd8b5eedad">OPD-Aha本地目标重建通过是否意味着运行了多模态checkpoint？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopd-aha">OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University / University of Virginia / Stevens Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不意味着，当前只有目标公式参考核。真实路径还需匹配视觉与空视觉输入、同一学生前缀及模型评分，不能用固定分布差直接报告看图反思效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人工设置猫概率升高，验证的是重建计算，不是模型自己发现了猫。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16459">原论文</a> · <a href="../../../../post-training/2609.16459-opd-aha/">实现解读</a> · <a href="#qa-7a9393dd8b5eedad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:nsd" data-paper-title="Negative Self-Distillation: Learning to Reason by Avoiding Flaws" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Negative Self-Distillation: Learning to Reason by Avoiding Flaws LLM 后训练 University of Virginia 2026-09-10 让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  负向自蒸馏 推理后训练 LLM 后训练 教师与纠错：额外信息何时能帮到学生 NSD为什么把自生成错误作为负向教学材料？ 失败推理可告诉模型应远离什么，而非只有正确示范才有价值。负教师描述错误分布，动态gate把排斥集中到推理关键位置，减少普通语言遗忘。 例如一次错误推导中的关键误用，可作为不要再走的方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-nsd-9169c0f1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-156313e8fb4c0f9c">NSD为什么把自生成错误作为负向教学材料？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ansd">Negative Self-Distillation: Learning to Reason by Avoiding Flaws</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>失败推理可告诉模型应远离什么，而非只有正确示范才有价值。负教师描述错误分布，动态gate把排斥集中到推理关键位置，减少普通语言遗忘。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次错误推导中的关键误用，可作为不要再走的方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11699">原论文</a> · <a href="../../../../post-training/2609.11699-nsd/">实现解读</a> · <a href="#qa-156313e8fb4c0f9c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:nsd" data-paper-title="Negative Self-Distillation: Learning to Reason by Avoiding Flaws" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Negative Self-Distillation: Learning to Reason by Avoiding Flaws LLM 后训练 University of Virginia 2026-09-10 让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  负向自蒸馏 推理后训练 LLM 后训练 教师与纠错：额外信息何时能帮到学生 NSD既然要远离错误推理，为什么不压低整条错误回答的所有词元？ 错误回答仍包含正常语法和可能正确的中间步骤，整段排斥会损伤通用表达。NSD用负向教师提供应远离的分布，并通过动态门控把更新集中到推理关键位置。门控只是定位机制，不能保证每个被选位置确实有错，本地也未训练完整语言模型。 例如算式中只有进位错误，句子里的连接词和正确数字不应全部被压低；教学例子关注选择性纠错，不声称测得收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b7073cf71d4eaf23">NSD既然要远离错误推理，为什么不压低整条错误回答的所有词元？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ansd">Negative Self-Distillation: Learning to Reason by Avoiding Flaws</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>错误回答仍包含正常语法和可能正确的中间步骤，整段排斥会损伤通用表达。NSD用负向教师提供应远离的分布，并通过动态门控把更新集中到推理关键位置。门控只是定位机制，不能保证每个被选位置确实有错，本地也未训练完整语言模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如算式中只有进位错误，句子里的连接词和正确数字不应全部被压低；教学例子关注选择性纠错，不声称测得收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11699">原论文</a> · <a href="../../../../post-training/2609.11699-nsd/">实现解读</a> · <a href="#qa-b7073cf71d4eaf23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:nsd" data-paper-title="Negative Self-Distillation: Learning to Reason by Avoiding Flaws" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Negative Self-Distillation: Learning to Reason by Avoiding Flaws LLM 后训练 University of Virginia 2026-09-10 让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  负向自蒸馏 推理后训练 LLM 后训练 教师与纠错：额外信息何时能帮到学生 负自蒸馏与把错答token全部降概率有什么差别？ 整段错误含正确事实、语法与有效子步，统一惩罚会误伤。选择性gate试图区分错误核心，但其定位也可能不准，不能视为步骤真值。 例如最终算错不代表每个数字和连接词都应被遗忘。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-886ee3b24ca799ed">负自蒸馏与把错答token全部降概率有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ansd">Negative Self-Distillation: Learning to Reason by Avoiding Flaws</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整段错误含正确事实、语法与有效子步，统一惩罚会误伤。选择性gate试图区分错误核心，但其定位也可能不准，不能视为步骤真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最终算错不代表每个数字和连接词都应被遗忘。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11699">原论文</a> · <a href="../../../../post-training/2609.11699-nsd/">实现解读</a> · <a href="#qa-886ee3b24ca799ed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:nsd" data-paper-title="Negative Self-Distillation: Learning to Reason by Avoiding Flaws" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Negative Self-Distillation: Learning to Reason by Avoiding Flaws LLM 后训练 University of Virginia 2026-09-10 让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  负向自蒸馏 推理后训练 LLM 后训练 教师与纠错：额外信息何时能帮到学生 NSD本地负教师与reasoning gate从何种对象构成？ 当前在候选策略上构造并执行控制流，未全参数训练真实LLM。门控需固定并对齐被罚位置，不能用评测gold先标出错误再声称无泄漏自主诊断。 例如预置错误位置可做单测，却不是自动定位推理漏洞的能力证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fdf24dcd2d314d24">NSD本地负教师与reasoning gate从何种对象构成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ansd">Negative Self-Distillation: Learning to Reason by Avoiding Flaws</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前在候选策略上构造并执行控制流，未全参数训练真实LLM。门控需固定并对齐被罚位置，不能用评测gold先标出错误再声称无泄漏自主诊断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预置错误位置可做单测，却不是自动定位推理漏洞的能力证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11699">原论文</a> · <a href="../../../../post-training/2609.11699-nsd/">实现解读</a> · <a href="#qa-fdf24dcd2d314d24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:compass-opd" data-paper-title="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts LLM 后训练 Institute of Information Engineering, Chinese Academy of Sciences 2026-09-09 异构教师与学生的绝对概率刻度不可直接比较。CompassOPD 用教师相对其 reference 的后训练变化作“指南针”，并在模型族内中心化，保留方向而消除不同模型族的整体偏置。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现去除 family offset 的教师方向，不冒充跨 tokenizer 的完整 LLM 训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。当前候选共享同一有限动作空间，未复刻跨 tokenizer 映射和全参数训练，因此属于 L1 机制诊断。  跨模型族 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 CompassOPD为什么需要教师自己的reference？ 不同家族绝对概率尺度不可直接比较，教师相对其参考的变化更能描述后训练方向。家族内中心化削弱整体偏置，再与学生锚点结合，仍非正确性证明。 例如一个家族本来分布尖，不应仅因概率大就被视为学得更多。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-compass-opd-6b3a07da" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-569a9735016a2295">CompassOPD为什么需要教师自己的reference？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acompass-opd">CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同家族绝对概率尺度不可直接比较，教师相对其参考的变化更能描述后训练方向。家族内中心化削弱整体偏置，再与学生锚点结合，仍非正确性证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个家族本来分布尖，不应仅因概率大就被视为学得更多。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10154">原论文</a> · <a href="../../../../post-training/2609.10154-compass-opd/">实现解读</a> · <a href="#qa-569a9735016a2295">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:compass-opd" data-paper-title="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts LLM 后训练 Institute of Information Engineering, Chinese Academy of Sciences 2026-09-09 异构教师与学生的绝对概率刻度不可直接比较。CompassOPD 用教师相对其 reference 的后训练变化作“指南针”，并在模型族内中心化，保留方向而消除不同模型族的整体偏置。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现去除 family offset 的教师方向，不冒充跨 tokenizer 的完整 LLM 训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。当前候选共享同一有限动作空间，未复刻跨 tokenizer 映射和全参数训练，因此属于 L1 机制诊断。  跨模型族 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 CompassOPD为什么比较教师相对自身参考模型的变化，而不直接比较师生概率？ 不同模型家族的概率尖锐程度和校准不同，直接对齐绝对概率会混入尺度差异。方法先看教师后训练相对其参考模型的似然变化，再作家族内中心化，提取方向性信号，并保留学生参考锚点。相对变化仍可能带有教师偏差，不自动等于正确答案。 例如两个教师都更偏好正确步骤，但一个本来输出更尖锐；比较各自训练前后的变化，比把两者概率大小直接排序更合理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f4e800f5f08e0695">CompassOPD为什么比较教师相对自身参考模型的变化，而不直接比较师生概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acompass-opd">CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同模型家族的概率尖锐程度和校准不同，直接对齐绝对概率会混入尺度差异。方法先看教师后训练相对其参考模型的似然变化，再作家族内中心化，提取方向性信号，并保留学生参考锚点。相对变化仍可能带有教师偏差，不自动等于正确答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个教师都更偏好正确步骤，但一个本来输出更尖锐；比较各自训练前后的变化，比把两者概率大小直接排序更合理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10154">原论文</a> · <a href="../../../../post-training/2609.10154-compass-opd/">实现解读</a> · <a href="#qa-f4e800f5f08e0695">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:compass-opd" data-paper-title="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts LLM 后训练 Institute of Information Engineering, Chinese Academy of Sciences 2026-09-09 异构教师与学生的绝对概率刻度不可直接比较。CompassOPD 用教师相对其 reference 的后训练变化作“指南针”，并在模型族内中心化，保留方向而消除不同模型族的整体偏置。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现去除 family offset 的教师方向，不冒充跨 tokenizer 的完整 LLM 训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。当前候选共享同一有限动作空间，未复刻跨 tokenizer 映射和全参数训练，因此属于 L1 机制诊断。  跨模型族 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Compass与直接平均跨家族概率的取舍是什么？ 前者保留相对变化方向，后者混合绝对后验。相对方向减少刻度影响，却也丢掉部分整体信息，不能无同协议实验就宣布一定优于完整教师。 例如同样向正确选项移动，不应被两个模型原始温度差淹没。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-687df570b70d35ac">Compass与直接平均跨家族概率的取舍是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acompass-opd">CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者保留相对变化方向，后者混合绝对后验。相对方向减少刻度影响，却也丢掉部分整体信息，不能无同协议实验就宣布一定优于完整教师。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样向正确选项移动，不应被两个模型原始温度差淹没。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10154">原论文</a> · <a href="../../../../post-training/2609.10154-compass-opd/">实现解读</a> · <a href="#qa-687df570b70d35ac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:compass-opd" data-paper-title="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts LLM 后训练 Institute of Information Engineering, Chinese Academy of Sciences 2026-09-09 异构教师与学生的绝对概率刻度不可直接比较。CompassOPD 用教师相对其 reference 的后训练变化作“指南针”，并在模型族内中心化，保留方向而消除不同模型族的整体偏置。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现去除 family offset 的教师方向，不冒充跨 tokenizer 的完整 LLM 训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。当前候选共享同一有限动作空间，未复刻跨 tokenizer 映射和全参数训练，因此属于 L1 机制诊断。  跨模型族 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Compass中心化应该沿什么可比集合进行？ 对规定家族变化信号使用一致候选和权重，学生reference另作锚点，不能跨不同问题随意减均值。本地审计量只反映修正幅度，不代表真实跨家族训练成功。 例如先后两模型候选顺序不同，直接相减会得到无意义方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f1ec49abd65dc106">Compass中心化应该沿什么可比集合进行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acompass-opd">CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对规定家族变化信号使用一致候选和权重，学生reference另作锚点，不能跨不同问题随意减均值。本地审计量只反映修正幅度，不代表真实跨家族训练成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先后两模型候选顺序不同，直接相减会得到无意义方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10154">原论文</a> · <a href="../../../../post-training/2609.10154-compass-opd/">实现解读</a> · <a href="#qa-f1ec49abd65dc106">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd" data-paper-title="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation LLM 后训练 KAIST AI 2026-09-08 OPRD 不直接模仿弱教师答案，而是先测量弱教师经过后训练后的 logit 变化方向，再沿这个方向增强强模型的可验证奖励梯度；核心假设是“学习方向”比弱模型最终能力更容易迁移。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现论文的反向蒸馏方向提取与验证器梯度投影，不把小型分类策略的结果等同于完整 LLM 后训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。本地仅验证方向提取和的可执行性；候选集合来自带标签的诊断任务，故 diagnostic_only=true、不可晋升为能力证据。  弱到强反向蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 弱到强OPRD迁移的是弱模型哪部分信息？ 弱模型后训练相对base的logit变化方向，被用于增强强模型验证器梯度。它不要求弱答案比强模型正确，假设有用学习方向可能跨能力规模迁移。 例如弱模型学到检查单位的趋势，可辅助强模型，而不用复制其计算结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-oprd-e69b9862" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-349513728ef75b89">弱到强OPRD迁移的是弱模型哪部分信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoprd">Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>弱模型后训练相对base的logit变化方向，被用于增强强模型验证器梯度。它不要求弱答案比强模型正确，假设有用学习方向可能跨能力规模迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如弱模型学到检查单位的趋势，可辅助强模型，而不用复制其计算结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08798">原论文</a> · <a href="../../../../post-training/2609.08798-oprd/">实现解读</a> · <a href="#qa-349513728ef75b89">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd" data-paper-title="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation LLM 后训练 KAIST AI 2026-09-08 OPRD 不直接模仿弱教师答案，而是先测量弱教师经过后训练后的 logit 变化方向，再沿这个方向增强强模型的可验证奖励梯度；核心假设是“学习方向”比弱模型最终能力更容易迁移。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现论文的反向蒸馏方向提取与验证器梯度投影，不把小型分类策略的结果等同于完整 LLM 后训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。本地仅验证方向提取和的可执行性；候选集合来自带标签的诊断任务，故 diagnostic_only=true、不可晋升为能力证据。  弱到强反向蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPRD为什么能借弱模型的变化方向，而不要求强模型模仿弱模型答案？ 方法从弱后训练模型与其基座的差异提取中心化、归一化方向，再增强强模型验证器梯度在该方向上的分量。迁移对象是更新方向，不是弱模型的最终回答。只有方向与强模型当前任务有用地对齐才可能帮助；本地候选方向诊断不证明通用弱到强提升。 例如弱模型训练后更重视检查单位，强模型可增强相关梯度分量，却不必抄它可能算错的最终数值；方向有用仍需验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-960ba50ff9253e9e">OPRD为什么能借弱模型的变化方向，而不要求强模型模仿弱模型答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoprd">Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>方法从弱后训练模型与其基座的差异提取中心化、归一化方向，再增强强模型验证器梯度在该方向上的分量。迁移对象是更新方向，不是弱模型的最终回答。只有方向与强模型当前任务有用地对齐才可能帮助；本地候选方向诊断不证明通用弱到强提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如弱模型训练后更重视检查单位，强模型可增强相关梯度分量，却不必抄它可能算错的最终数值；方向有用仍需验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08798">原论文</a> · <a href="../../../../post-training/2609.08798-oprd/">实现解读</a> · <a href="#qa-960ba50ff9253e9e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd" data-paper-title="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation LLM 后训练 KAIST AI 2026-09-08 OPRD 不直接模仿弱教师答案，而是先测量弱教师经过后训练后的 logit 变化方向，再沿这个方向增强强模型的可验证奖励梯度；核心假设是“学习方向”比弱模型最终能力更容易迁移。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现论文的反向蒸馏方向提取与验证器梯度投影，不把小型分类策略的结果等同于完整 LLM 后训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。本地仅验证方向提取和的可执行性；候选集合来自带标签的诊断任务，故 diagnostic_only=true、不可晋升为能力证据。  弱到强反向蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPRD方向增强与用弱teacher做完整蒸馏有什么差别？ 增强保留强模型原验证梯度，只放大其沿弱学习方向的分量；完整蒸馏直接拟合弱分布。若方向与强任务无关也可能无益，并非弱模型自动教强模型所有技能。 例如强模型仍按自己的任务奖励更新，只受一个方向性调节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-761aac5efd4bbe26">OPRD方向增强与用弱teacher做完整蒸馏有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoprd">Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>增强保留强模型原验证梯度，只放大其沿弱学习方向的分量；完整蒸馏直接拟合弱分布。若方向与强任务无关也可能无益，并非弱模型自动教强模型所有技能。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如强模型仍按自己的任务奖励更新，只受一个方向性调节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08798">原论文</a> · <a href="../../../../post-training/2609.08798-oprd/">实现解读</a> · <a href="#qa-761aac5efd4bbe26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd" data-paper-title="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation LLM 后训练 KAIST AI 2026-09-08 OPRD 不直接模仿弱教师答案，而是先测量弱教师经过后训练后的 logit 变化方向，再沿这个方向增强强模型的可验证奖励梯度；核心假设是“学习方向”比弱模型最终能力更容易迁移。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现论文的反向蒸馏方向提取与验证器梯度投影，不把小型分类策略的结果等同于完整 LLM 后训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。本地仅验证方向提取和的可执行性；候选集合来自带标签的诊断任务，故 diagnostic_only=true、不可晋升为能力证据。  弱到强反向蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPRD的d如何处理零变化与梯度方向？ 变化先去均值再单位化，零范数需明确无有效方向；增强为原梯度加投影项，不能把梯度全替换成d。本地按候选映回参数，不是完整真实模型梯度实验。 例如弱模型训练前后完全相同，不能除零后产生一个随机教学方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e39f4f113b3c46a3">OPRD的d如何处理零变化与梯度方向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoprd">Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>变化先去均值再单位化，零范数需明确无有效方向；增强为原梯度加投影项，不能把梯度全替换成d。本地按候选映回参数，不是完整真实模型梯度实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如弱模型训练前后完全相同，不能除零后产生一个随机教学方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08798">原论文</a> · <a href="../../../../post-training/2609.08798-oprd/">实现解读</a> · <a href="#qa-e39f4f113b3c46a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:uc-mopd" data-paper-title="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD LLM 后训练 Peking University 2026-08-27 普通 MOPD 很少采到强正优势 token，也无法判断更新方向是否可靠。方法扩大温度覆盖，按轨迹正优势密度挑样本，再用熵校准 CLL 概率门控 token 更新。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现双温采样、正优势密度筛选和 centered log-likelihood 门控。未加载通用/垂域教师 checkpoint；本地结果仅证明筛选与随机门控控制流。arithmetic-smoke 本轮 accuracy 0.1953 → 0.1953。零提升被如实保留：机制运行正常，但单教师候选套件不能证明论文多教师收益。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 UC-MOPD为什么先扩大采样温度覆盖？ 普通采样可能很少产生值得强化的正优势位置，双温候选先增加探索，再由轨迹密度和词元可靠性筛选。扩大候选只是找材料，不等于材料都正确。 例如多尝试另一种解法后，还要判断它是否真正提供有效步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-uc-mopd-4afbd03c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9a9ccd364b8ec023">UC-MOPD为什么先扩大采样温度覆盖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Auc-mopd">Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通采样可能很少产生值得强化的正优势位置，双温候选先增加探索，再由轨迹密度和词元可靠性筛选。扩大候选只是找材料，不等于材料都正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如多尝试另一种解法后，还要判断它是否真正提供有效步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26735">原论文</a> · <a href="../../../../post-training/2608.26735-uc-mopd/">实现解读</a> · <a href="#qa-9a9ccd364b8ec023">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:uc-mopd" data-paper-title="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD LLM 后训练 Peking University 2026-08-27 普通 MOPD 很少采到强正优势 token，也无法判断更新方向是否可靠。方法扩大温度覆盖，按轨迹正优势密度挑样本，再用熵校准 CLL 概率门控 token 更新。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现双温采样、正优势密度筛选和 centered log-likelihood 门控。未加载通用/垂域教师 checkpoint；本地结果仅证明筛选与随机门控控制流。arithmetic-smoke 本轮 accuracy 0.1953 → 0.1953。零提升被如实保留：机制运行正常，但单教师候选套件不能证明论文多教师收益。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 UC-MOPD的温度扩展、轨迹筛选和词元门控分别解决什么问题？ 温度扩展先增加候选覆盖，正优势词元密度用于挑选更有学习价值的轨迹，熵校准的概率门控再控制具体词元更新。三个步骤作用在不同层次，不能把候选更多直接等同于监督更准；置信度也不是真值，本地未加载完整的通用与领域教师。 例如先采到几条不同解法，再选有效步骤较密的一条，最后只加强可靠的关键词元；不能把整条高置信回答无条件当标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-269cf7e11d08beba">UC-MOPD的温度扩展、轨迹筛选和词元门控分别解决什么问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Auc-mopd">Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>温度扩展先增加候选覆盖，正优势词元密度用于挑选更有学习价值的轨迹，熵校准的概率门控再控制具体词元更新。三个步骤作用在不同层次，不能把候选更多直接等同于监督更准；置信度也不是真值，本地未加载完整的通用与领域教师。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先采到几条不同解法，再选有效步骤较密的一条，最后只加强可靠的关键词元；不能把整条高置信回答无条件当标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26735">原论文</a> · <a href="../../../../post-training/2608.26735-uc-mopd/">实现解读</a> · <a href="#qa-269cf7e11d08beba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:uc-mopd" data-paper-title="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD LLM 后训练 Peking University 2026-08-27 普通 MOPD 很少采到强正优势 token，也无法判断更新方向是否可靠。方法扩大温度覆盖，按轨迹正优势密度挑样本，再用熵校准 CLL 概率门控 token 更新。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现双温采样、正优势密度筛选和 centered log-likelihood 门控。未加载通用/垂域教师 checkpoint；本地结果仅证明筛选与随机门控控制流。arithmetic-smoke 本轮 accuracy 0.1953 → 0.1953。零提升被如实保留：机制运行正常，但单教师候选套件不能证明论文多教师收益。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 正优势密度筛轨迹与CLL gate筛token怎样配合？ 前者决定哪条轨迹值得进入，后者在入选轨迹中控制局部更新。只实现一个会缺少另一层不确定性控制，不能把高置信直接叫真值。 例如整条路线总体有价值，也可能有些局部位置不适合强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6280056a50d0c34c">正优势密度筛轨迹与CLL gate筛token怎样配合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Auc-mopd">Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者决定哪条轨迹值得进入，后者在入选轨迹中控制局部更新。只实现一个会缺少另一层不确定性控制，不能把高置信直接叫真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如整条路线总体有价值，也可能有些局部位置不适合强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26735">原论文</a> · <a href="../../../../post-training/2608.26735-uc-mopd/">实现解读</a> · <a href="#qa-6280056a50d0c34c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:uc-mopd" data-paper-title="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD LLM 后训练 Peking University 2026-08-27 普通 MOPD 很少采到强正优势 token，也无法判断更新方向是否可靠。方法扩大温度覆盖，按轨迹正优势密度挑样本，再用熵校准 CLL 概率门控 token 更新。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现双温采样、正优势密度筛选和 centered log-likelihood 门控。未加载通用/垂域教师 checkpoint；本地结果仅证明筛选与随机门控控制流。arithmetic-smoke 本轮 accuracy 0.1953 → 0.1953。零提升被如实保留：机制运行正常，但单教师候选套件不能证明论文多教师收益。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 UC-MOPD随机gate需要记录什么，checkpoint已加载吗？ 需记录门控概率、随机种子与有效位置，避免把一次抽样误作确定选择。当前未加载通用或领域教师，公式控制流通过不证明保留真实通用能力。 例如两次不同随机mask应可追溯，而非只选得分最好的一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-24e5a9dad8d49b28">UC-MOPD随机gate需要记录什么，checkpoint已加载吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Auc-mopd">Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需记录门控概率、随机种子与有效位置，避免把一次抽样误作确定选择。当前未加载通用或领域教师，公式控制流通过不证明保留真实通用能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次不同随机mask应可追溯，而非只选得分最好的一次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26735">原论文</a> · <a href="../../../../post-training/2608.26735-uc-mopd/">实现解读</a> · <a href="#qa-24e5a9dad8d49b28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:video-opsd" data-paper-title="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models LLM 后训练 Nanyang Technological University 2026-08-27 学生读取完整视频，训练期自教师只读取人工标注的证据帧；再按 token 对证据的依赖度加权蒸馏。论文称效果接近 GRPO，而训练时间减少约 60%。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现证据视图自教师与 evidence-guided token 权重。公开 smoke 数据没有视频帧，使用独立奖励轴模拟“证据依赖”；未训练 Video-LLM，不把概念验证写成论文指标复刻。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.6562，记录 evidence token weight 与 teacher gap。指标见 metrics/arithmetic-smoke-seed42.json。  证据帧特权自蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Video-OPSD为什么教师只看证据帧而学生看全片？ 训练教师获得更集中证据，学生学习在完整视频干扰中吸收它；推理不假定知道人工定位。若学生也只看标注帧，会改变待解决的证据搜索任务。 例如教师看拿杯子瞬间，学生仍需从整段活动中辨认相关事件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-video-opsd-2da91d84" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f7da4e86ac722d50">Video-OPSD为什么教师只看证据帧而学生看全片？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avideo-opsd">Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练教师获得更集中证据，学生学习在完整视频干扰中吸收它；推理不假定知道人工定位。若学生也只看标注帧，会改变待解决的证据搜索任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师看拿杯子瞬间，学生仍需从整段活动中辨认相关事件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27065">原论文</a> · <a href="../../../../post-training/2608.27065-video-opsd/">实现解读</a> · <a href="#qa-f7da4e86ac722d50">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:video-opsd" data-paper-title="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models LLM 后训练 Nanyang Technological University 2026-08-27 学生读取完整视频，训练期自教师只读取人工标注的证据帧；再按 token 对证据的依赖度加权蒸馏。论文称效果接近 GRPO，而训练时间减少约 60%。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现证据视图自教师与 evidence-guided token 权重。公开 smoke 数据没有视频帧，使用独立奖励轴模拟“证据依赖”；未训练 Video-LLM，不把概念验证写成论文指标复刻。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.6562，记录 evidence token weight 与 teacher gap。指标见 metrics/arithmetic-smoke-seed42.json。  证据帧特权自蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Video-OPSD的证据帧为什么只给训练教师，而学生仍要读取完整视频？ 教师在人工标注的证据帧上形成较聚焦的监督，再按词元对证据的依赖加权蒸馏。学生保留完整视频输入，学习在干扰中利用相关内容；若把证据定位也直接给学生，就改变了推理条件。本地无视频烟雾测试只是奖励轴代理，不能作为视觉能力证据。 例如问题问谁先拿起杯子，教师只看相关片段，学生仍看整段活动视频；教学目标是学会找证据，不是假定已知片段位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-14eccc74c245b0fe">Video-OPSD的证据帧为什么只给训练教师，而学生仍要读取完整视频？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avideo-opsd">Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师在人工标注的证据帧上形成较聚焦的监督，再按词元对证据的依赖加权蒸馏。学生保留完整视频输入，学习在干扰中利用相关内容；若把证据定位也直接给学生，就改变了推理条件。本地无视频烟雾测试只是奖励轴代理，不能作为视觉能力证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问题问谁先拿起杯子，教师只看相关片段，学生仍看整段活动视频；教学目标是学会找证据，不是假定已知片段位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27065">原论文</a> · <a href="../../../../post-training/2608.27065-video-opsd/">实现解读</a> · <a href="#qa-14eccc74c245b0fe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:video-opsd" data-paper-title="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models LLM 后训练 Nanyang Technological University 2026-08-27 学生读取完整视频，训练期自教师只读取人工标注的证据帧；再按 token 对证据的依赖度加权蒸馏。论文称效果接近 GRPO，而训练时间减少约 60%。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现证据视图自教师与 evidence-guided token 权重。公开 smoke 数据没有视频帧，使用独立奖励轴模拟“证据依赖”；未训练 Video-LLM，不把概念验证写成论文指标复刻。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.6562，记录 evidence token weight 与 teacher gap。指标见 metrics/arithmetic-smoke-seed42.json。  证据帧特权自蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 证据依赖权重与所有token等量KL有什么差别？ 前者更强调由视觉证据影响的位置，后者也同等模仿风格等词元。依赖性并不保证事实正确，论文训练时间比较也不能外推到本地无视频smoke。 例如人物动作词可比通用连接词更依赖具体帧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f6c24d377aa71a92">证据依赖权重与所有token等量KL有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avideo-opsd">Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者更强调由视觉证据影响的位置，后者也同等模仿风格等词元。依赖性并不保证事实正确，论文训练时间比较也不能外推到本地无视频smoke。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人物动作词可比通用连接词更依赖具体帧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27065">原论文</a> · <a href="../../../../post-training/2608.27065-video-opsd/">实现解读</a> · <a href="#qa-f6c24d377aa71a92">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:video-opsd" data-paper-title="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models LLM 后训练 Nanyang Technological University 2026-08-27 学生读取完整视频，训练期自教师只读取人工标注的证据帧；再按 token 对证据的依赖度加权蒸馏。论文称效果接近 GRPO，而训练时间减少约 60%。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现证据视图自教师与 evidence-guided token 权重。公开 smoke 数据没有视频帧，使用独立奖励轴模拟“证据依赖”；未训练 Video-LLM，不把概念验证写成论文指标复刻。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.6562，记录 evidence token weight 与 teacher gap。指标见 metrics/arithmetic-smoke-seed42.json。  证据帧特权自蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Video-OPSD本地smoke是否真实含视频帧？ 不含，用独立奖励轴模拟证据依赖。即使存在真实checkpoint路径，也不等于已完成视频模型训练；教师目标与学生前缀需对齐，标注不能进入部署输入。 例如smoke里一个过程分不代表模型实际看过那段视频。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-15746459e8aa6d5e">Video-OPSD本地smoke是否真实含视频帧？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avideo-opsd">Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不含，用独立奖励轴模拟证据依赖。即使存在真实checkpoint路径，也不等于已完成视频模型训练；教师目标与学生前缀需对齐，标注不能进入部署输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如smoke里一个过程分不代表模型实际看过那段视频。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27065">原论文</a> · <a href="../../../../post-training/2608.27065-video-opsd/">实现解读</a> · <a href="#qa-15746459e8aa6d5e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weak-guide-rlvr" data-paper-title="Boosting LLM Exploration via Weak-Model Guidance in RLVR" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Boosting LLM Exploration via Weak-Model Guidance in RLVR LLM 后训练 Peking University 2026-08-27 RLVR 容易熵坍缩。论文用更小弱模型生成部分推理前缀，迫使目标模型进入陌生轨迹，再以 entropy 截断和原生/前缀样本混训保持覆盖率。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现跨模型前缀扰动、混合采样与 entropy 诊断。弱教师由冻结 reference 分布模拟；未声称完成双 checkpoint RLVR。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6797，并记录 guided entropy 与 prefix surprise。  弱模型前缀探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 弱模型前缀为什么可能帮助更强模型探索？ 它把强模型送到自身采样不常访问的起点，增加推理路线覆盖。前缀可能错，最终任务奖励仍需独立verifier，不能把来自弱模型就等同正确示范。 例如弱模型先想到另一种分解，强模型尝试从它继续并接受验算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-weak-guide-rlvr-a37f47f8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-18d555967dc0fe5d">弱模型前缀为什么可能帮助更强模型探索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aweak-guide-rlvr">Boosting LLM Exploration via Weak-Model Guidance in RLVR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把强模型送到自身采样不常访问的起点，增加推理路线覆盖。前缀可能错，最终任务奖励仍需独立verifier，不能把来自弱模型就等同正确示范。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如弱模型先想到另一种分解，强模型尝试从它继续并接受验算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27420">原论文</a> · <a href="../../../../post-training/2608.27420-weak-guide-rlvr/">实现解读</a> · <a href="#qa-18d555967dc0fe5d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weak-guide-rlvr" data-paper-title="Boosting LLM Exploration via Weak-Model Guidance in RLVR" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Boosting LLM Exploration via Weak-Model Guidance in RLVR LLM 后训练 Peking University 2026-08-27 RLVR 容易熵坍缩。论文用更小弱模型生成部分推理前缀，迫使目标模型进入陌生轨迹，再以 entropy 截断和原生/前缀样本混训保持覆盖率。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现跨模型前缀扰动、混合采样与 entropy 诊断。弱教师由冻结 reference 分布模拟；未声称完成双 checkpoint RLVR。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6797，并记录 guided entropy 与 prefix surprise。  弱模型前缀探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 弱模型给出的推理前缀可能错误，Weak-Model Guidance为什么还要混入它？ 弱模型前缀把目标策略带到自身采样不常遇到的状态，提供额外探索起点；熵截断限制不稳定续写，并与原生轨迹混合以保留覆盖。前缀只是引导，不能充当正确标签，最终奖励仍需独立验证器。本地冻结参考代理没有替代真实双模型训练。 例如弱模型提出另一种分解问题的开头，强模型从此继续并接受答案检查；如果检查失败，不能因为有引导就把轨迹判为正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4fb85815b204e8ef">弱模型给出的推理前缀可能错误，Weak-Model Guidance为什么还要混入它？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aweak-guide-rlvr">Boosting LLM Exploration via Weak-Model Guidance in RLVR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>弱模型前缀把目标策略带到自身采样不常遇到的状态，提供额外探索起点；熵截断限制不稳定续写，并与原生轨迹混合以保留覆盖。前缀只是引导，不能充当正确标签，最终奖励仍需独立验证器。本地冻结参考代理没有替代真实双模型训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如弱模型提出另一种分解问题的开头，强模型从此继续并接受答案检查；如果检查失败，不能因为有引导就把轨迹判为正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27420">原论文</a> · <a href="../../../../post-training/2608.27420-weak-guide-rlvr/">实现解读</a> · <a href="#qa-4fb85815b204e8ef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weak-guide-rlvr" data-paper-title="Boosting LLM Exploration via Weak-Model Guidance in RLVR" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Boosting LLM Exploration via Weak-Model Guidance in RLVR LLM 后训练 Peking University 2026-08-27 RLVR 容易熵坍缩。论文用更小弱模型生成部分推理前缀，迫使目标模型进入陌生轨迹，再以 entropy 截断和原生/前缀样本混训保持覆盖率。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现跨模型前缀扰动、混合采样与 entropy 诊断。弱教师由冻结 reference 分布模拟；未声称完成双 checkpoint RLVR。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6797，并记录 guided entropy 与 prefix surprise。  弱模型前缀探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 前缀引导与把弱模型完整答案当SFT目标有什么区别？ 引导只干预起点，后续由目标模型生成并用奖励学习；SFT要求模仿整段文本。原生与引导混合及熵截断控制覆盖，不等于无条件信任弱解。 例如只给思路开头，不要求强模型连同弱模型的最后错误一起抄。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e84a9eb0b18e84db">前缀引导与把弱模型完整答案当SFT目标有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aweak-guide-rlvr">Boosting LLM Exploration via Weak-Model Guidance in RLVR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>引导只干预起点，后续由目标模型生成并用奖励学习；SFT要求模仿整段文本。原生与引导混合及熵截断控制覆盖，不等于无条件信任弱解。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只给思路开头，不要求强模型连同弱模型的最后错误一起抄。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27420">原论文</a> · <a href="../../../../post-training/2608.27420-weak-guide-rlvr/">实现解读</a> · <a href="#qa-e84a9eb0b18e84db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weak-guide-rlvr" data-paper-title="Boosting LLM Exploration via Weak-Model Guidance in RLVR" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Boosting LLM Exploration via Weak-Model Guidance in RLVR LLM 后训练 Peking University 2026-08-27 RLVR 容易熵坍缩。论文用更小弱模型生成部分推理前缀，迫使目标模型进入陌生轨迹，再以 entropy 截断和原生/前缀样本混训保持覆盖率。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现跨模型前缀扰动、混合采样与 entropy 诊断。弱教师由冻结 reference 分布模拟；未声称完成双 checkpoint RLVR。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6797，并记录 guided entropy 与 prefix surprise。  弱模型前缀探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 本地冻结reference代理是否就是双checkpoint RLVR？ 不是，当前弱引导由参考候选分布模拟，未执行真实两套模型前缀生成。混合比例、原生样本和前缀边界需记录，不能把额外提示带到独立测试输入。 例如用数值候选分布换个起点，尚未测真实弱模型语言前缀质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7fc7e666f15f6076">本地冻结reference代理是否就是双checkpoint RLVR？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aweak-guide-rlvr">Boosting LLM Exploration via Weak-Model Guidance in RLVR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，当前弱引导由参考候选分布模拟，未执行真实两套模型前缀生成。混合比例、原生样本和前缀边界需记录，不能把额外提示带到独立测试输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用数值候选分布换个起点，尚未测真实弱模型语言前缀质量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27420">原论文</a> · <a href="../../../../post-training/2608.27420-weak-guide-rlvr/">实现解读</a> · <a href="#qa-7fc7e666f15f6076">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:clue-opsd" data-paper-title="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding LLM 后训练 University of Maryland, College Park 2026-08-26 学生仍看完整长视频，冻结教师在训练时只看问题相关 clue interval；学生自己的 rollout 上做 on-policy self-distillation，推理时不需要 clue、标签或外部教师。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.5938（+375.00%）；clue 用 process-reward proxy 代替。  长视频特权视图 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Clue-OPSD为什么把相关时间区间作为训练特权信息？ 长视频中的关键证据难找，冻结教师看clue可给更聚焦指导，学生仍只依赖完整视频与问题。训练目标是内化定位能力，推理去掉clue与外部教师。 例如问题问首次开门，教师知相关时间段，学生部署时不能直接拿人工时间戳。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-clue-opsd-7ed80773" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-be66d452b82d5b6e">Clue-OPSD为什么把相关时间区间作为训练特权信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aclue-opsd">Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长视频中的关键证据难找，冻结教师看clue可给更聚焦指导，学生仍只依赖完整视频与问题。训练目标是内化定位能力，推理去掉clue与外部教师。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问题问首次开门，教师知相关时间段，学生部署时不能直接拿人工时间戳。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25356">原论文</a> · <a href="../../../../post-training/2608.25356-clue-opsd/">实现解读</a> · <a href="#qa-be66d452b82d5b6e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:clue-opsd" data-paper-title="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding LLM 后训练 University of Maryland, College Park 2026-08-26 学生仍看完整长视频，冻结教师在训练时只看问题相关 clue interval；学生自己的 rollout 上做 on-policy self-distillation，推理时不需要 clue、标签或外部教师。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.5938（+375.00%）；clue 用 process-reward proxy 代替。  长视频特权视图 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Clue-OPSD为什么要在学生自己的前缀上查询只看线索片段的教师？ 学生前缀决定训练时真正遇到的状态，线索片段则让教师聚焦与问题相关的证据；二者结合减少只在教师理想轨迹上学习的偏移。线索是训练期特权信息，推理时学生仍须处理完整视频，不应依赖片段标注、答案或教师。 例如学生已写出一个不完整的事件顺序，教师读取相关时间段后续写纠正；部署时不能把人工圈出的时间段继续作为输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dffc751edf033222">Clue-OPSD为什么要在学生自己的前缀上查询只看线索片段的教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aclue-opsd">Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生前缀决定训练时真正遇到的状态，线索片段则让教师聚焦与问题相关的证据；二者结合减少只在教师理想轨迹上学习的偏移。线索是训练期特权信息，推理时学生仍须处理完整视频，不应依赖片段标注、答案或教师。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生已写出一个不完整的事件顺序，教师读取相关时间段后续写纠正；部署时不能把人工圈出的时间段继续作为输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25356">原论文</a> · <a href="../../../../post-training/2608.25356-clue-opsd/">实现解读</a> · <a href="#qa-dffc751edf033222">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:clue-opsd" data-paper-title="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding LLM 后训练 University of Maryland, College Park 2026-08-26 学生仍看完整长视频，冻结教师在训练时只看问题相关 clue interval；学生自己的 rollout 上做 on-policy self-distillation，推理时不需要 clue、标签或外部教师。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.5938（+375.00%）；clue 用 process-reward proxy 代替。  长视频特权视图 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Clue教师与单纯裁短学生视频有什么不同？ 裁短学生同时降低输入难度，无法检验完整长视频能力；特权教师只改变监督条件。两者成本和任务条件不同，不能拿裁短学生结果替代该方法。 例如学生看到全片与只看答案片段，不是在做相同评测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c8470c0c5f874a93">Clue教师与单纯裁短学生视频有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aclue-opsd">Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>裁短学生同时降低输入难度，无法检验完整长视频能力；特权教师只改变监督条件。两者成本和任务条件不同，不能拿裁短学生结果替代该方法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生看到全片与只看答案片段，不是在做相同评测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25356">原论文</a> · <a href="../../../../post-training/2608.25356-clue-opsd/">实现解读</a> · <a href="#qa-c8470c0c5f874a93">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:clue-opsd" data-paper-title="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding LLM 后训练 University of Maryland, College Park 2026-08-26 学生仍看完整长视频，冻结教师在训练时只看问题相关 clue interval；学生自己的 rollout 上做 on-policy self-distillation，推理时不需要 clue、标签或外部教师。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.5938（+375.00%）；clue 用 process-reward proxy 代替。  长视频特权视图 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Clue-OPSD为什么在学生前缀而非教师自写前缀上计算KL？ 这样指导学生真实访问状态，减少理想轨迹偏移；师生对齐同一词元位置但视觉条件不同。当前mini-suite无完整视频检查点实验，不能报告原文数值。 例如学生已误认角色时，教师仍需评价这个前缀而不是换成自己的正确开头。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8caf90bc522fe861">Clue-OPSD为什么在学生前缀而非教师自写前缀上计算KL？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aclue-opsd">Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这样指导学生真实访问状态，减少理想轨迹偏移；师生对齐同一词元位置但视觉条件不同。当前mini-suite无完整视频检查点实验，不能报告原文数值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生已误认角色时，教师仍需评价这个前缀而不是换成自己的正确开头。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25356">原论文</a> · <a href="../../../../post-training/2608.25356-clue-opsd/">实现解读</a> · <a href="#qa-8caf90bc522fe861">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:smopd" data-paper-title="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation LLM 后训练 Alibaba / Qwen 2026-08-04 先用 reward-priority 分别训练专长教师，再在学生自身轨迹上合并多个教师能力。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 多奖励 RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 SMOPD为什么先specialize再merge？ 不同奖励优先级可训练出不同专长教师，再在学生轨迹上融合稠密监督，避免从一开始把冲突目标挤成同一专家。多样教师仍可能相互干扰。 例如一个教师重严谨，一个重格式，先分开学再决定如何教学生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-smopd-2a4bef05" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7c3d10ce5b7d86dd">SMOPD为什么先specialize再merge？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asmopd">SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Qwen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同奖励优先级可训练出不同专长教师，再在学生轨迹上融合稠密监督，避免从一开始把冲突目标挤成同一专家。多样教师仍可能相互干扰。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个教师重严谨，一个重格式，先分开学再决定如何教学生。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03092">原论文</a> · <a href="../../../../post-training/2608.03092-smopd/">实现解读</a> · <a href="#qa-7c3d10ce5b7d86dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:smopd" data-paper-title="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation LLM 后训练 Alibaba / Qwen 2026-08-04 先用 reward-priority 分别训练专长教师，再在学生自身轨迹上合并多个教师能力。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 多奖励 RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 SMOPD为什么先训练不同奖励侧重的专家，再在学生状态上合并？ 不同奖励优先级可塑造具有不同专长的教师，随后让它们在学生实际到达的状态提供分布监督，以加权蒸馏吸收这些能力。它不等于先把奖励平均成一个教师，也不保证所有能力无损共存；权重与教师分歧仍需验证，本地只是候选模型实验。 例如一个教师擅长检查计算，另一个擅长格式约束，学生在自己的解题步骤上同时获得指导；并非直接把两套参数平均。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-70fa4e434b261d14">SMOPD为什么先训练不同奖励侧重的专家，再在学生状态上合并？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asmopd">SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Qwen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同奖励优先级可塑造具有不同专长的教师，随后让它们在学生实际到达的状态提供分布监督，以加权蒸馏吸收这些能力。它不等于先把奖励平均成一个教师，也不保证所有能力无损共存；权重与教师分歧仍需验证，本地只是候选模型实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个教师擅长检查计算，另一个擅长格式约束，学生在自己的解题步骤上同时获得指导；并非直接把两套参数平均。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03092">原论文</a> · <a href="../../../../post-training/2608.03092-smopd/">实现解读</a> · <a href="#qa-70fa4e434b261d14">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:smopd" data-paper-title="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation LLM 后训练 Alibaba / Qwen 2026-08-04 先用 reward-priority 分别训练专长教师，再在学生自身轨迹上合并多个教师能力。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 多奖励 RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 SMOPD奖励专家与MOPD领域专家的组织依据有何差别？ 前者按奖励优先级塑造专长，后者常按任务领域独立训练教师；二者都可多教师蒸馏，但专家划分与评价维度不同，不能仅按名字混用资源预算。 例如同一领域可有不同奖励专家，不必每专家代表一个数据领域。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-db366732628a378d">SMOPD奖励专家与MOPD领域专家的组织依据有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asmopd">SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Qwen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者按奖励优先级塑造专长，后者常按任务领域独立训练教师；二者都可多教师蒸馏，但专家划分与评价维度不同，不能仅按名字混用资源预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一领域可有不同奖励专家，不必每专家代表一个数据领域。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03092">原论文</a> · <a href="../../../../post-training/2608.03092-smopd/">实现解读</a> · <a href="#qa-db366732628a378d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:smopd" data-paper-title="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation LLM 后训练 Alibaba / Qwen 2026-08-04 先用 reward-priority 分别训练专长教师，再在学生自身轨迹上合并多个教师能力。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 多奖励 RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 SMOPD多教师KL实现需在什么状态对齐？ 都评分学生自身同一前缀，权重和教师目标固定，不能把各教师独立生成的位置直接逐项相加。当前候选核没有完成真实专家训练与合并。 例如一个教师第二步与另一个第四步没有共同状态，就不是相同位置的联合监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-efc24d49c99b3f4d">SMOPD多教师KL实现需在什么状态对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asmopd">SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Qwen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>都评分学生自身同一前缀，权重和教师目标固定，不能把各教师独立生成的位置直接逐项相加。当前候选核没有完成真实专家训练与合并。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个教师第二步与另一个第四步没有共同状态，就不是相同位置的联合监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03092">原论文</a> · <a href="../../../../post-training/2608.03092-smopd/">实现解读</a> · <a href="#qa-efc24d49c99b3f4d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rstg" data-paper-title="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance LLM 后训练 Tianjin University 2026-08-01 只对负向零方差 group 启用教师，并在高熵或大 teacher-student gap token 上蒸馏，同时注入教师正确轨迹 SFT。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD RLVR LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSTG为什么专门恢复全失败组信号？ 全失败时组奖励没有差异，教师可提供纠正和局部指导；全成功虽然也零方差，却不具相同失败需求。触发需同时看方差与奖励值。 例如一组都没解出与一组都解对，不能因方差同为零就同样请教师纠错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-rstg-e8f7dde4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a077cf99039366a7">RSTG为什么专门恢复全失败组信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arstg">Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全失败时组奖励没有差异，教师可提供纠正和局部指导；全成功虽然也零方差，却不具相同失败需求。触发需同时看方差与奖励值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一组都没解出与一组都解对，不能因方差同为零就同样请教师纠错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00782">原论文</a> · <a href="../../../../post-training/2608.00782-rstg/">实现解读</a> · <a href="#qa-a077cf99039366a7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rstg" data-paper-title="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance LLM 后训练 Tianjin University 2026-08-01 只对负向零方差 group 启用教师，并在高熵或大 teacher-student gap token 上蒸馏，同时注入教师正确轨迹 SFT。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD RLVR LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSTG为什么只对全失败的零方差组求助教师，而不把所有同分组一视同仁？ 组内全失败时，奖励归一化缺少可区分信号，教师可提供纠正轨迹，并在高熵或师生差距大的词元上增加监督。全成功组同样可能零方差，却没有相同的纠错需求。触发条件必须区分正负结果，教师纠正也仍需要可靠性检查。 例如四条解法都算错时可请求教师示范；四条都答对时，不能仅因分数相同就当成失败组，再强行覆盖学生的不同解法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a7b069f4ac14b1cf">RSTG为什么只对全失败的零方差组求助教师，而不把所有同分组一视同仁？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arstg">Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组内全失败时，奖励归一化缺少可区分信号，教师可提供纠正轨迹，并在高熵或师生差距大的词元上增加监督。全成功组同样可能零方差，却没有相同的纠错需求。触发条件必须区分正负结果，教师纠正也仍需要可靠性检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四条解法都算错时可请求教师示范；四条都答对时，不能仅因分数相同就当成失败组，再强行覆盖学生的不同解法。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00782">原论文</a> · <a href="../../../../post-training/2608.00782-rstg/">实现解读</a> · <a href="#qa-a7b069f4ac14b1cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rstg" data-paper-title="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance LLM 后训练 Tianjin University 2026-08-01 只对负向零方差 group 启用教师，并在高熵或大 teacher-student gap token 上蒸馏，同时注入教师正确轨迹 SFT。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD RLVR LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSTG token选择与直接全段教师模仿有何区别？ 它将高熵或大gap位置作为更需指导的区域，并加入正确教师轨迹SFT。选择减少无关监督，但置信或gap仍不是错误定位真值。 例如格式已稳定的词可少教，关键不确定转折得到更多指导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b80daeba0810cc0b">RSTG token选择与直接全段教师模仿有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arstg">Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它将高熵或大gap位置作为更需指导的区域，并加入正确教师轨迹SFT。选择减少无关监督，但置信或gap仍不是错误定位真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如格式已稳定的词可少教，关键不确定转折得到更多指导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00782">原论文</a> · <a href="../../../../post-training/2608.00782-rstg/">实现解读</a> · <a href="#qa-b80daeba0810cc0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rstg" data-paper-title="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance LLM 后训练 Tianjin University 2026-08-01 只对负向零方差 group 启用教师，并在高熵或大 teacher-student gap token 上蒸馏，同时注入教师正确轨迹 SFT。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD RLVR LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSTG可以只实现负组gate就称完整方法吗？ 不可以，还要实际执行局部蒸馏与教师正确轨迹监督，并保留来源和mask。当前本地候选目标验证不含大模型教师生成及完整训练预算。 例如布尔值标记need_teacher为真，不等于教师分支真的被运行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-67bfaf2b24863e43">RSTG可以只实现负组gate就称完整方法吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arstg">Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可以，还要实际执行局部蒸馏与教师正确轨迹监督，并保留来源和mask。当前本地候选目标验证不含大模型教师生成及完整训练预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如布尔值标记need_teacher为真，不等于教师分支真的被运行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00782">原论文</a> · <a href="../../../../post-training/2608.00782-rstg/">实现解读</a> · <a href="#qa-67bfaf2b24863e43">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:crpo" data-paper-title="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation LLM 后训练 Authors did not disclose affiliation 2026-07-30 按预测熵区分反思探索正位置和 exposure-bias 负位置，对 privileged self-distillation 做组内对比。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD Agentic RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 CRPO为什么把反思探索与exposure bias区分？ 两者都可能表现高不确定，但前者有益于修正，后者可能因错误前缀越走越偏。组内对比试图区分不同性质的位置，而不是一律奖励熵高。 例如重新检查分支的犹豫，与错误算式后的乱续写，含义不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-crpo-a18535ff" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c06cdac5feb0ffce">CRPO为什么把反思探索与exposure bias区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acrpo">Contrastive Reinforced Policy Optimization via Privileged Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两者都可能表现高不确定，但前者有益于修正，后者可能因错误前缀越走越偏。组内对比试图区分不同性质的位置，而不是一律奖励熵高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如重新检查分支的犹豫，与错误算式后的乱续写，含义不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28026">原论文</a> · <a href="../../../../post-training/2607.28026-crpo/">实现解读</a> · <a href="#qa-c06cdac5feb0ffce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:crpo" data-paper-title="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation LLM 后训练 Authors did not disclose affiliation 2026-07-30 按预测熵区分反思探索正位置和 exposure-bias 负位置，对 privileged self-distillation 做组内对比。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD Agentic RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 CRPO为什么把高不确定位置区分为反思探索与暴露偏差，而不统一奖励高熵？ 高熵可能表示有价值的探索，也可能是错误前缀导致的失控。CRPO结合组内对比和特权自蒸馏来区分这些情形，分别处理有益反思位置与偏差暴露位置。熵只描述不确定程度，不能单独判定对错；本地候选诊断不等于完整推理训练。 例如重新检查一个分支时的不确定与沿错误算式胡乱续写都可能高熵，更新方向应取决于后续可验证结果，而非熵值本身。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fb12ee1ea24d6bed">CRPO为什么把高不确定位置区分为反思探索与暴露偏差，而不统一奖励高熵？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acrpo">Contrastive Reinforced Policy Optimization via Privileged Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高熵可能表示有价值的探索，也可能是错误前缀导致的失控。CRPO结合组内对比和特权自蒸馏来区分这些情形，分别处理有益反思位置与偏差暴露位置。熵只描述不确定程度，不能单独判定对错；本地候选诊断不等于完整推理训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如重新检查一个分支时的不确定与沿错误算式胡乱续写都可能高熵，更新方向应取决于后续可验证结果，而非熵值本身。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28026">原论文</a> · <a href="../../../../post-training/2607.28026-crpo/">实现解读</a> · <a href="#qa-fb12ee1ea24d6bed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:crpo" data-paper-title="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation LLM 后训练 Authors did not disclose affiliation 2026-07-30 按预测熵区分反思探索正位置和 exposure-bias 负位置，对 privileged self-distillation 做组内对比。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD Agentic RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 CRPO对比目标与单独最小化特权教师KL有什么不同？ 对比以正负位置相对分数构造竞争关系，KL直接匹配一个目标分布。正负划分是否可靠是额外假设，不能因有负例就自动消除教师偏差。 例如同样提高正位置分数，分母里有哪些负位置也会影响更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bd450bb59f9c435a">CRPO对比目标与单独最小化特权教师KL有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acrpo">Contrastive Reinforced Policy Optimization via Privileged Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对比以正负位置相对分数构造竞争关系，KL直接匹配一个目标分布。正负划分是否可靠是额外假设，不能因有负例就自动消除教师偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样提高正位置分数，分母里有哪些负位置也会影响更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28026">原论文</a> · <a href="../../../../post-training/2607.28026-crpo/">实现解读</a> · <a href="#qa-bd450bb59f9c435a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:crpo" data-paper-title="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation LLM 后训练 Authors did not disclose affiliation 2026-07-30 按预测熵区分反思探索正位置和 exposure-bias 负位置，对 privileged self-distillation 做组内对比。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD Agentic RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 CRPO本地候选核是否包含真实反思位置识别模型？ 未包含完整大模型链路，当前只验证目标与诊断。正负位置和分组应记录来源，训练特权条件不能进入学生采样，也不能用gold直接填负位置后宣传自主识别。 例如预给mask适合单测，却不能证明真实文本中能找到exposure bias。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e1bf7c072d6c0d5b">CRPO本地候选核是否包含真实反思位置识别模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acrpo">Contrastive Reinforced Policy Optimization via Privileged Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未包含完整大模型链路，当前只验证目标与诊断。正负位置和分组应记录来源，训练特权条件不能进入学生采样，也不能用gold直接填负位置后宣传自主识别。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预给mask适合单测，却不能证明真实文本中能找到exposure bias。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28026">原论文</a> · <a href="../../../../post-training/2607.28026-crpo/">实现解读</a> · <a href="#qa-e1bf7c072d6c0d5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vad" data-paper-title="VAD" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="VAD LLM 后训练 Shanghai Jiao Tong University 2026-07-30 多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。 未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。本页复现论文可隔离的 counterfactual target reconstruction；本地候选策略用过程证据轴模拟 evidence-present / evidence-removed 教师视图，不把它写成 4B/9B 多模态模型复现。候选答案的过程质量轴替代真实图像裁剪，验证的是 counterfactual target reconstruction 的数学路径；未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。  多模态证据归因蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 VAD为什么以学生当前分布重建target？ 只从教师整体复制会混入语言和风格偏差，方法把视觉方向上有用修正加到学生锚点，保留其其他偏好；完整特权教师仅作较弱正则。 例如只吸收图像颜色证据，不强迫学生一起改写所有语言风格。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-vad-1b365cba" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b488d8ea330de209">VAD为什么以学生当前分布重建target？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avad">VAD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只从教师整体复制会混入语言和风格偏差，方法把视觉方向上有用修正加到学生锚点，保留其其他偏好；完整特权教师仅作较弱正则。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只吸收图像颜色证据，不强迫学生一起改写所有语言风格。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28590">原论文</a> · <a href="../../../../post-training/2607.28590-vad/">实现解读</a> · <a href="#qa-b488d8ea330de209">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vad" data-paper-title="VAD" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="VAD LLM 后训练 Shanghai Jiao Tong University 2026-07-30 多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。 未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。本页复现论文可隔离的 counterfactual target reconstruction；本地候选策略用过程证据轴模拟 evidence-present / evidence-removed 教师视图，不把它写成 4B/9B 多模态模型复现。候选答案的过程质量轴替代真实图像裁剪，验证的是 counterfactual target reconstruction 的数学路径；未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。  多模态证据归因蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 VAD为什么把教师修正投影到视觉证据方向，而且只保留同向分量？ 有无视觉证据的教师对比给出视觉方向，原教师修正只保留沿该方向的正向投影，再以当前学生分布为锚构造目标。这样限制与视觉无关或反向的整体模仿；完整教师分布只作较弱约束。本地奖励轴代理并未复现真实视觉裁剪和模型训练。 例如教师既偏好某种措辞又看到红色物体，投影试图保留颜色证据相关的变化，而不把所有语言风格一起灌给学生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-48b96f2481a2a52d">VAD为什么把教师修正投影到视觉证据方向，而且只保留同向分量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avad">VAD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有无视觉证据的教师对比给出视觉方向，原教师修正只保留沿该方向的正向投影，再以当前学生分布为锚构造目标。这样限制与视觉无关或反向的整体模仿；完整教师分布只作较弱约束。本地奖励轴代理并未复现真实视觉裁剪和模型训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师既偏好某种措辞又看到红色物体，投影试图保留颜色证据相关的变化，而不把所有语言风格一起灌给学生。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28590">原论文</a> · <a href="../../../../post-training/2607.28590-vad/">实现解读</a> · <a href="#qa-48b96f2481a2a52d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vad" data-paper-title="VAD" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="VAD LLM 后训练 Shanghai Jiao Tong University 2026-07-30 多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。 未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。本页复现论文可隔离的 counterfactual target reconstruction；本地候选策略用过程证据轴模拟 evidence-present / evidence-removed 教师视图，不把它写成 4B/9B 多模态模型复现。候选答案的过程质量轴替代真实图像裁剪，验证的是 counterfactual target reconstruction 的数学路径；未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。  多模态证据归因蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 单侧投影与直接用视觉方向替换全部修正有什么差别？ 只有教师修正与视觉方向正对齐的部分被保留，反向不硬跟；直接替换忽略原修正是否支持该方向。投影是归因约束，仍不证明教师视觉判断正确。 例如视觉对比有变化，但原修正与它相反时，不应盲目注入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-93258e520a528b62">单侧投影与直接用视觉方向替换全部修正有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avad">VAD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有教师修正与视觉方向正对齐的部分被保留，反向不硬跟；直接替换忽略原修正是否支持该方向。投影是归因约束，仍不证明教师视觉判断正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如视觉对比有变化，但原修正与它相反时，不应盲目注入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28590">原论文</a> · <a href="../../../../post-training/2607.28590-vad/">实现解读</a> · <a href="#qa-93258e520a528b62">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vad" data-paper-title="VAD" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="VAD LLM 后训练 Shanghai Jiao Tong University 2026-07-30 多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。 未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。本页复现论文可隔离的 counterfactual target reconstruction；本地候选策略用过程证据轴模拟 evidence-present / evidence-removed 教师视图，不把它写成 4B/9B 多模态模型复现。候选答案的过程质量轴替代真实图像裁剪，验证的是 counterfactual target reconstruction 的数学路径；未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。  多模态证据归因蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 VAD的证据移除分支应与证据存在分支保持什么一致？ 同一冻结教师、问题和学生前缀，仅改变证据视图；logp需中心化再投影并有稳定分母。当前过程质量轴代理不含真实裁剪、checkpoint和视觉benchmark。 例如用另一个语言模型代替移除视图，会混入架构偏差而非纯证据差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-043731ad0bc86318">VAD的证据移除分支应与证据存在分支保持什么一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avad">VAD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一冻结教师、问题和学生前缀，仅改变证据视图；logp需中心化再投影并有稳定分母。当前过程质量轴代理不含真实裁剪、checkpoint和视觉benchmark。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用另一个语言模型代替移除视图，会混入架构偏差而非纯证据差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28590">原论文</a> · <a href="../../../../post-training/2607.28590-vad/">实现解读</a> · <a href="#qa-043731ad0bc86318">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:distilled-rl" data-paper-title="Distilled RL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distilled RL LLM 后训练 Nankai University 2026-07-19 传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现反向比率裁剪、负样本 reset 与序列几何归一化；教师不是无条件 KL target。  教师奖励重权重 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Distilled RL怎样把教师分布用于RL而非单独模仿？ 教师与旧学生概率比形成词元权重，作用于已有任务优势，只对正优势启用。这样任务反馈决定该强化哪些样本，教师细化其中哪些位置更值得强化。 例如已验证成功解法中，教师更认可关键步骤可获得更多相对权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-distilled-rl-b41ef584" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-be4145dd92521d12">Distilled RL怎样把教师分布用于RL而非单独模仿？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adistilled-rl">Distilled RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nankai University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师与旧学生概率比形成词元权重，作用于已有任务优势，只对正优势启用。这样任务反馈决定该强化哪些样本，教师细化其中哪些位置更值得强化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已验证成功解法中，教师更认可关键步骤可获得更多相对权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17247">原论文</a> · <a href="../../../../post-training/2607.17247-distilled-rl/">实现解读</a> · <a href="#qa-be4145dd92521d12">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:distilled-rl" data-paper-title="Distilled RL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distilled RL LLM 后训练 Nankai University 2026-07-19 传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现反向比率裁剪、负样本 reset 与序列几何归一化；教师不是无条件 KL target。  教师奖励重权重 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Distilled RL为什么只给正优势样本加教师权重，负优势样本保持原权重？ 正优势样本已有任务奖励支持，教师比率可进一步强调其中值得模仿的词元；非正优势样本维持原权重，避免教师重加权干扰其惩罚含义。比率经过裁剪和序列几何均值归一化，限制尺度及长度影响，但教师偏好仍不等于额外正确性证明。 例如一条答对的解法可提高关键步骤权重，一条失败解法仍按原负优势更新；不应因教师喜欢某些用词就削弱失败惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-225945cbff9e4ee0">Distilled RL为什么只给正优势样本加教师权重，负优势样本保持原权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adistilled-rl">Distilled RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nankai University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正优势样本已有任务奖励支持，教师比率可进一步强调其中值得模仿的词元；非正优势样本维持原权重，避免教师重加权干扰其惩罚含义。比率经过裁剪和序列几何均值归一化，限制尺度及长度影响，但教师偏好仍不等于额外正确性证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条答对的解法可提高关键步骤权重，一条失败解法仍按原负优势更新；不应因教师喜欢某些用词就削弱失败惩罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17247">原论文</a> · <a href="../../../../post-training/2607.17247-distilled-rl/">实现解读</a> · <a href="#qa-225945cbff9e4ee0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:distilled-rl" data-paper-title="Distilled RL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distilled RL LLM 后训练 Nankai University 2026-07-19 传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现反向比率裁剪、负样本 reset 与序列几何归一化；教师不是无条件 KL target。  教师奖励重权重 LLM 后训练 教师与纠错：额外信息何时能帮到学生 正优势门控与对正负样本都加教师权重有什么区别？ 负优势维持原权重一，避免教师偏好改变失败惩罚的相对意义；双向重权可能减弱某些负反馈。这个门不是按教师分数重新判断整条对错。 例如失败解法里教师喜欢的措辞，也不能因此获得额外减罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4232f22db291ab10">正优势门控与对正负样本都加教师权重有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adistilled-rl">Distilled RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nankai University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>负优势维持原权重一，避免教师偏好改变失败惩罚的相对意义；双向重权可能减弱某些负反馈。这个门不是按教师分数重新判断整条对错。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如失败解法里教师喜欢的措辞，也不能因此获得额外减罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17247">原论文</a> · <a href="../../../../post-training/2607.17247-distilled-rl/">实现解读</a> · <a href="#qa-4232f22db291ab10">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:distilled-rl" data-paper-title="Distilled RL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distilled RL LLM 后训练 Nankai University 2026-07-19 传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现反向比率裁剪、负样本 reset 与序列几何归一化；教师不是无条件 KL target。  教师奖励重权重 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Distilled RL为何用裁剪比的序列几何均值归一？ 限制比值尺度并让整条权重相对化，求几何均值要用有效响应位置，非正优势分支仍为一。当前确定性mini-suite未完成真实词元生成和完整教师训练。 例如padding混入均值会改变所有词元权重，即使它们本身不计loss。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c5eea841205341bc">Distilled RL为何用裁剪比的序列几何均值归一？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adistilled-rl">Distilled RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nankai University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>限制比值尺度并让整条权重相对化，求几何均值要用有效响应位置，非正优势分支仍为一。当前确定性mini-suite未完成真实词元生成和完整教师训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如padding混入均值会改变所有词元权重，即使它们本身不计loss。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17247">原论文</a> · <a href="../../../../post-training/2607.17247-distilled-rl/">实现解读</a> · <a href="#qa-c5eea841205341bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:armor" data-paper-title="ARMOR" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="ARMOR LLM 后训练 University of Science and Technology of China 2026-07-11 单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。reference 是本地初始化候选策略，不包含论文规模的长程训练或真实轨迹池。每个训练组一半从当前策略采样、一半从冻结 reference 采样，分别记录 anchor 数、权重和最终策略指标。  Reference anchor LLM 后训练 教师与纠错：额外信息何时能帮到学生 ARMOR为什么主动从reference采样？ 惩罚偏离只作用已见样本，不能让当前策略已经不采的好解法重新出现。reference锚点轨迹提供实际数据覆盖，帮助保留原能力路径。 例如学生只剩一种捷径时，旧策略仍可能采出另一条检查路线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-armor-71dc1f8a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8d0793b82963f670">ARMOR为什么主动从reference采样？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aarmor">ARMOR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>惩罚偏离只作用已见样本，不能让当前策略已经不采的好解法重新出现。reference锚点轨迹提供实际数据覆盖，帮助保留原能力路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生只剩一种捷径时，旧策略仍可能采出另一条检查路线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10481">原论文</a> · <a href="../../../../post-training/2607.10481-armor/">实现解读</a> · <a href="#qa-8d0793b82963f670">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:armor" data-paper-title="ARMOR" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="ARMOR LLM 后训练 University of Science and Technology of China 2026-07-11 单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。reference 是本地初始化候选策略，不包含论文规模的长程训练或真实轨迹池。每个训练组一半从当前策略采样、一半从冻结 reference 采样，分别记录 anchor 数、权重和最终策略指标。  Reference anchor LLM 后训练 教师与纠错：额外信息何时能帮到学生 ARMOR主动采样参考策略轨迹，与只在损失里加入KL惩罚有什么区别？ KL惩罚在当前采到的数据上限制策略漂移，却不保证参考策略的好解法仍出现在训练样本中。ARMOR主动混入冻结参考策略的锚点轨迹，恢复这部分数据覆盖。参考轨迹也可能差或已过时，混合比例需要控制；本地参考候选模型不能代表完整语言模型结论。 例如新策略只会用一种捷径，锚点采样能重新提供旧策略的检查路线；仅惩罚分布差异，不一定让这条路线实际进入批次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8a68376cc571efdb">ARMOR主动采样参考策略轨迹，与只在损失里加入KL惩罚有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aarmor">ARMOR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>KL惩罚在当前采到的数据上限制策略漂移，却不保证参考策略的好解法仍出现在训练样本中。ARMOR主动混入冻结参考策略的锚点轨迹，恢复这部分数据覆盖。参考轨迹也可能差或已过时，混合比例需要控制；本地参考候选模型不能代表完整语言模型结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新策略只会用一种捷径，锚点采样能重新提供旧策略的检查路线；仅惩罚分布差异，不一定让这条路线实际进入批次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10481">原论文</a> · <a href="../../../../post-training/2607.10481-armor/">实现解读</a> · <a href="#qa-8a68376cc571efdb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:armor" data-paper-title="ARMOR" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="ARMOR LLM 后训练 University of Science and Technology of China 2026-07-11 单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。reference 是本地初始化候选策略，不包含论文规模的长程训练或真实轨迹池。每个训练组一半从当前策略采样、一半从冻结 reference 采样，分别记录 anchor 数、权重和最终策略指标。  Reference anchor LLM 后训练 教师与纠错：额外信息何时能帮到学生 anchor rollout与额外加reference KL是否等价？ 不等价，前者改变训练数据及访问状态，后者在现有状态约束分布。锚点也可能过时或错误，需要任务评价，不能把保留旧行为当永远有益。 例如没进批次的旧路线，不会仅因一个被动正则就被真正重新练习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-85f7219f929ace1d">anchor rollout与额外加reference KL是否等价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aarmor">ARMOR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等价，前者改变训练数据及访问状态，后者在现有状态约束分布。锚点也可能过时或错误，需要任务评价，不能把保留旧行为当永远有益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如没进批次的旧路线，不会仅因一个被动正则就被真正重新练习。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10481">原论文</a> · <a href="../../../../post-training/2607.10481-armor/">实现解读</a> · <a href="#qa-85f7219f929ace1d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:armor" data-paper-title="ARMOR" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="ARMOR LLM 后训练 University of Science and Technology of China 2026-07-11 单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。reference 是本地初始化候选策略，不包含论文规模的长程训练或真实轨迹池。每个训练组一半从当前策略采样、一半从冻结 reference 采样，分别记录 anchor 数、权重和最终策略指标。  Reference anchor LLM 后训练 教师与纠错：额外信息何时能帮到学生 ARMOR本地reference是什么，样本能标成当前on-policy吗？ reference是初始化候选策略，锚点来源需独立记录，不能称学生当前采样。当前没有论文长程轨迹池，混合项可执行只说明数据路径而非完整稳定能力。 例如旧策略采出的动作，不能拿当前策略生成日志冒充其来源。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6a88eac1ccf377ad">ARMOR本地reference是什么，样本能标成当前on-policy吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aarmor">ARMOR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>reference是初始化候选策略，锚点来源需独立记录，不能称学生当前采样。当前没有论文长程轨迹池，混合项可执行只说明数据路径而非完整稳定能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧策略采出的动作，不能拿当前策略生成日志冒充其来源。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10481">原论文</a> · <a href="../../../../post-training/2607.10481-armor/">实现解读</a> · <a href="#qa-6a88eac1ccf377ad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mopd" data-paper-title="MOPD" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MOPD LLM 后训练 Xiaomi 2026-06-29 多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现四个奖励轴的 domain teacher、按样本域证据混合，并限制在 student rollout support。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MOPD为什么先独立训练领域教师？ 联合RL可能让领域梯度耦合，独立教师允许各域分别优化，再以学生轨迹上的密集信号整合。整合仍是共享参数学习，不保证完全无干扰。 例如数学与代码专家先各自训练，之后共同指导一个学生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-mopd-f0fd48c7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d026bf7949d24011">MOPD为什么先独立训练领域教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amopd">MOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaomi</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>联合RL可能让领域梯度耦合，独立教师允许各域分别优化，再以学生轨迹上的密集信号整合。整合仍是共享参数学习，不保证完全无干扰。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数学与代码专家先各自训练，之后共同指导一个学生。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.30406">原论文</a> · <a href="../../../../post-training/2606.30406-mopd/">实现解读</a> · <a href="#qa-d026bf7949d24011">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mopd" data-paper-title="MOPD" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MOPD LLM 后训练 Xiaomi 2026-06-29 多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现四个奖励轴的 domain teacher、按样本域证据混合，并限制在 student rollout support。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MOPD为什么在学生轨迹上调用多个领域教师，而不直接拼接专家轨迹训练？ 学生自己的前缀暴露真实学习状态，多个领域教师在相同状态提供稠密指导，可减少专家轨迹与学生分布不一致的问题。合并发生在监督信号而非简单参数平均，领域之间仍可能干扰，不能因为有多个教师就推断能力全部保留。本地只是候选级验证。 例如学生在一道混合数学与代码的问题中写到中间步骤，两位教师围绕该状态指导；直接拼接各自完整答案未必覆盖这个状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f2bf256351a9b963">MOPD为什么在学生轨迹上调用多个领域教师，而不直接拼接专家轨迹训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amopd">MOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaomi</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生自己的前缀暴露真实学习状态，多个领域教师在相同状态提供稠密指导，可减少专家轨迹与学生分布不一致的问题。合并发生在监督信号而非简单参数平均，领域之间仍可能干扰，不能因为有多个教师就推断能力全部保留。本地只是候选级验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生在一道混合数学与代码的问题中写到中间步骤，两位教师围绕该状态指导；直接拼接各自完整答案未必覆盖这个状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.30406">原论文</a> · <a href="../../../../post-training/2606.30406-mopd/">实现解读</a> · <a href="#qa-f2bf256351a9b963">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mopd" data-paper-title="MOPD" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MOPD LLM 后训练 Xiaomi 2026-06-29 多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现四个奖励轴的 domain teacher、按样本域证据混合，并限制在 student rollout support。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MOPD概率混合与参数平均分别在哪一层合并？ 概率混合在同一学生状态形成监督，参数平均直接组合权重；前者需教师推理成本，后者需权重可比并可能破坏内部协调。无同协议实验证据不排优劣。 例如两个教师同一前缀给分布，与把两套矩阵逐元素平均，是不同计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-92e43d22fe015b99">MOPD概率混合与参数平均分别在哪一层合并？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amopd">MOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaomi</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>概率混合在同一学生状态形成监督，参数平均直接组合权重；前者需教师推理成本，后者需权重可比并可能破坏内部协调。无同协议实验证据不排优劣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个教师同一前缀给分布，与把两套矩阵逐元素平均，是不同计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.30406">原论文</a> · <a href="../../../../post-training/2606.30406-mopd/">实现解读</a> · <a href="#qa-92e43d22fe015b99">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mopd" data-paper-title="MOPD" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MOPD LLM 后训练 Xiaomi 2026-06-29 多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现四个奖励轴的 domain teacher、按样本域证据混合，并限制在 student rollout support。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MOPD教师权重α与概率维度需要满足什么？ 候选或词表对齐，权重按明确规则归一后构成目标，教师固定且只更新学生。当前mini-suite由确定性分布代理，不能视为各域真实教师训练完成。 例如词表索引不同就不能直接相加概率，归一也无法修复语义错位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-448c87336997f6e1">MOPD教师权重α与概率维度需要满足什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amopd">MOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaomi</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选或词表对齐，权重按明确规则归一后构成目标，教师固定且只更新学生。当前mini-suite由确定性分布代理，不能视为各域真实教师训练完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如词表索引不同就不能直接相加概率，归一也无法修复语义错位。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.30406">原论文</a> · <a href="../../../../post-training/2606.30406-mopd/">实现解读</a> · <a href="#qa-448c87336997f6e1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:polaris-hri" data-paper-title="POLARIS: Guiding Small Models to Write Long Stories" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="POLARIS: Guiding Small Models to Write Long Stories LLM 后训练 University of Maryland 2026-06-02 核固定v2 Section3.2 Eq5和作者fixed verl core：policy-only mean/sample-std，Aref=0.4 min(1,t/15)(rref−μ)/(σ+1e-6)，step0为0；K5+1，clip0.2、KL关闭，token-mean。相同external rubric给policy和ref评分。按adv符号在log-ratio域选精确clipped分支，避免exp溢出的伪有限forward/NaN backward，不改原目标。 成本过高，不复现（审查 DONE）。Qwen3.5-9B、1388 copyrighted prompt-story pairs、4×A10080GB FSDP、batch8、160steps，每run原文约48h并约60美元judge API。完整实验明确超单卡短时预算；人类故事不公开，不能用自造故事冒充原训练数据。hri_advantages仅处理外部真实reward，hri_grpo_loss处理current/old teacher-forced logp与response mask。未实现Story Quality judge、版权故事、thinking trace生成或完整写作RL训练；  RLVR与偏好优化 GRPO与参考轨迹注入 LLM 后训练 教师与纠错：额外信息何时能帮到学生 POLARIS为什么在策略故事外加入teacher-forced参考故事？ 长故事终局评价稀疏，参考提供高质量锚点，与策略样本使用同一外部rubric。它是训练额外监督，不是把版权故事或答案提供给评测生成模型。 例如学生自己写几篇，再学习一篇参考如何展开，但独立测试仍须自主写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-polaris-hri-c07af119" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a8b284fd70c36138">POLARIS为什么在策略故事外加入teacher-forced参考故事？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apolaris-hri">POLARIS: Guiding Small Models to Write Long Stories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长故事终局评价稀疏，参考提供高质量锚点，与策略样本使用同一外部rubric。它是训练额外监督，不是把版权故事或答案提供给评测生成模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生自己写几篇，再学习一篇参考如何展开，但独立测试仍须自主写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.04095v1">原论文</a> · <a href="../../../../post-training/2606.04095-polaris-hri/">实现解读</a> · <a href="#qa-a8b284fd70c36138">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:polaris-hri" data-paper-title="POLARIS: Guiding Small Models to Write Long Stories" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="POLARIS: Guiding Small Models to Write Long Stories LLM 后训练 University of Maryland 2026-06-02 核固定v2 Section3.2 Eq5和作者fixed verl core：policy-only mean/sample-std，Aref=0.4 min(1,t/15)(rref−μ)/(σ+1e-6)，step0为0；K5+1，clip0.2、KL关闭，token-mean。相同external rubric给policy和ref评分。按adv符号在log-ratio域选精确clipped分支，避免exp溢出的伪有限forward/NaN backward，不改原目标。 成本过高，不复现（审查 DONE）。Qwen3.5-9B、1388 copyrighted prompt-story pairs、4×A10080GB FSDP、batch8、160steps，每run原文约48h并约60美元judge API。完整实验明确超单卡短时预算；人类故事不公开，不能用自造故事冒充原训练数据。hri_advantages仅处理外部真实reward，hri_grpo_loss处理current/old teacher-forced logp与response mask。未实现Story Quality judge、版权故事、thinking trace生成或完整写作RL训练；  RLVR与偏好优化 GRPO与参考轨迹注入 LLM 后训练 教师与纠错：额外信息何时能帮到学生 POLARIS HRI为什么用策略样本计算均值方差，并让参考答案优势逐步加入？ 参考故事是额外锚点，若纳入策略组的均值方差，会同时改变所有策略样本的优势尺度。方法只用策略奖励计算统计量，再逐步放大参考样本的相对优势，起始步权重为零。参考与策略使用同一评价准则；本地组件验证不代表完整故事训练已复现。 例如五条策略故事决定组内基线，第六条参考故事只据此计算自己的优势；不能先把参考混入均值，再声称只增加一条监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-502cc3028b75390d">POLARIS HRI为什么用策略样本计算均值方差，并让参考答案优势逐步加入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apolaris-hri">POLARIS: Guiding Small Models to Write Long Stories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参考故事是额外锚点，若纳入策略组的均值方差，会同时改变所有策略样本的优势尺度。方法只用策略奖励计算统计量，再逐步放大参考样本的相对优势，起始步权重为零。参考与策略使用同一评价准则；本地组件验证不代表完整故事训练已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如五条策略故事决定组内基线，第六条参考故事只据此计算自己的优势；不能先把参考混入均值，再声称只增加一条监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.04095v1">原论文</a> · <a href="../../../../post-training/2606.04095-polaris-hri/">实现解读</a> · <a href="#qa-502cc3028b75390d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:polaris-hri" data-paper-title="POLARIS: Guiding Small Models to Write Long Stories" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="POLARIS: Guiding Small Models to Write Long Stories LLM 后训练 University of Maryland 2026-06-02 核固定v2 Section3.2 Eq5和作者fixed verl core：policy-only mean/sample-std，Aref=0.4 min(1,t/15)(rref−μ)/(σ+1e-6)，step0为0；K5+1，clip0.2、KL关闭，token-mean。相同external rubric给policy和ref评分。按adv符号在log-ratio域选精确clipped分支，避免exp溢出的伪有限forward/NaN backward，不改原目标。 成本过高，不复现（审查 DONE）。Qwen3.5-9B、1388 copyrighted prompt-story pairs、4×A10080GB FSDP、batch8、160steps，每run原文约48h并约60美元judge API。完整实验明确超单卡短时预算；人类故事不公开，不能用自造故事冒充原训练数据。hri_advantages仅处理外部真实reward，hri_grpo_loss处理current/old teacher-forced logp与response mask。未实现Story Quality judge、版权故事、thinking trace生成或完整写作RL训练；  RLVR与偏好优化 GRPO与参考轨迹注入 LLM 后训练 教师与纠错：额外信息何时能帮到学生 参考渐进注入与一开始等权混入有什么差别？ 前期参考权重从零升起，避免骤然主导策略；均值方差仍只来自策略故事。等权混入既改变阶段强度，也可能改变全组baseline，两种设定不能互称。 例如第零步参考优势必须为零，而不是已有固定大权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-edb4c07a49fae20e">参考渐进注入与一开始等权混入有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apolaris-hri">POLARIS: Guiding Small Models to Write Long Stories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前期参考权重从零升起，避免骤然主导策略；均值方差仍只来自策略故事。等权混入既改变阶段强度，也可能改变全组baseline，两种设定不能互称。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第零步参考优势必须为零，而不是已有固定大权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.04095v1">原论文</a> · <a href="../../../../post-training/2606.04095-polaris-hri/">实现解读</a> · <a href="#qa-edb4c07a49fae20e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:polaris-hri" data-paper-title="POLARIS: Guiding Small Models to Write Long Stories" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="POLARIS: Guiding Small Models to Write Long Stories LLM 后训练 University of Maryland 2026-06-02 核固定v2 Section3.2 Eq5和作者fixed verl core：policy-only mean/sample-std，Aref=0.4 min(1,t/15)(rref−μ)/(σ+1e-6)，step0为0；K5+1，clip0.2、KL关闭，token-mean。相同external rubric给policy和ref评分。按adv符号在log-ratio域选精确clipped分支，避免exp溢出的伪有限forward/NaN backward，不改原目标。 成本过高，不复现（审查 DONE）。Qwen3.5-9B、1388 copyrighted prompt-story pairs、4×A10080GB FSDP、batch8、160steps，每run原文约48h并约60美元judge API。完整实验明确超单卡短时预算；人类故事不公开，不能用自造故事冒充原训练数据。hri_advantages仅处理外部真实reward，hri_grpo_loss处理current/old teacher-forced logp与response mask。未实现Story Quality judge、版权故事、thinking trace生成或完整写作RL训练；  RLVR与偏好优化 GRPO与参考轨迹注入 LLM 后训练 教师与纠错：额外信息何时能帮到学生 POLARIS如何避免ratio溢出但仍保持原clipped目标？ 先按优势符号在log-ratio域选精确分支，再指数化，padding与零优势先清理；不额外clamp目标。完整实验本地因成本过高未复现，小张量梯度通过不是长故事能力。 例如本该走已封顶分支时，不必先计算一个巨大exp再取min。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-117cbaa22780a1d9">POLARIS如何避免ratio溢出但仍保持原clipped目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apolaris-hri">POLARIS: Guiding Small Models to Write Long Stories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先按优势符号在log-ratio域选精确分支，再指数化，padding与零优势先清理；不额外clamp目标。完整实验本地因成本过高未复现，小张量梯度通过不是长故事能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如本该走已封顶分支时，不必先计算一个巨大exp再取min。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.04095v1">原论文</a> · <a href="../../../../post-training/2606.04095-polaris-hri/">实现解读</a> · <a href="#qa-117cbaa22780a1d9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcd" data-paper-title="OPCD" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPCD LLM 后训练 Microsoft Research 2026-02-12 提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。论文覆盖经验知识蒸馏和系统提示蒸馏，并支持跨模型尺寸教师。 保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；当前为候选策略机制复现，不等同于 Qwen3/VeRL 原始训练。本地“经验上下文”是已验证答案形成的可审计条件分布，不包含真实长 system prompt；未复跑 FrozenLake、Sokoban 或医疗/安全任务，因此不能将本地准确率与论文横向比较。稳定指标见 omitted-agentic-rl-opd-seed42.json。  Context distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPCD想解决的上下文经验流失是什么？ 提示、检索或历史经验只在当前上下文有效，清空后消失。方法让无上下文学生沿自己轨迹吸收带经验教师的行为，目标是把依赖额外上下文的知识内化到参数。 例如学过一次工具使用经验后，下次没有这段提示也希望能遵循。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-opcd-d21234a6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-198f7d6d31dcfc23">OPCD想解决的上下文经验流失是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopcd">OPCD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提示、检索或历史经验只在当前上下文有效，清空后消失。方法让无上下文学生沿自己轨迹吸收带经验教师的行为，目标是把依赖额外上下文的知识内化到参数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学过一次工具使用经验后，下次没有这段提示也希望能遵循。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12275">原论文</a> · <a href="../../../../post-training/2602.12275-opcd/">实现解读</a> · <a href="#qa-198f7d6d31dcfc23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcd" data-paper-title="OPCD" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPCD LLM 后训练 Microsoft Research 2026-02-12 提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。论文覆盖经验知识蒸馏和系统提示蒸馏，并支持跨模型尺寸教师。 保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；当前为候选策略机制复现，不等同于 Qwen3/VeRL 原始训练。本地“经验上下文”是已验证答案形成的可审计条件分布，不包含真实长 system prompt；未复跑 FrozenLake、Sokoban 或医疗/安全任务，因此不能将本地准确率与论文横向比较。稳定指标见 omitted-agentic-rl-opd-seed42.json。  Context distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPCD为什么让无经验上下文的学生生成，再让带上下文的教师评分？ 目标是把外部经验内化到参数，而不是训练学生继续依赖那段经验。学生只读任务并生成轨迹，教师读取经验后在同一学生前缀给出分布，以学生到教师方向的逆KL更新。上下文知识是否可靠仍很关键，本地条件分布诊断没有覆盖真实长系统提示。 例如训练教师可读一条操作经验，学生只能读当前任务；学习后清空上下文再作答，才能检验经验是否进入了参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c0cb6a3f7ec32a4d">OPCD为什么让无经验上下文的学生生成，再让带上下文的教师评分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopcd">OPCD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是把外部经验内化到参数，而不是训练学生继续依赖那段经验。学生只读任务并生成轨迹，教师读取经验后在同一学生前缀给出分布，以学生到教师方向的逆KL更新。上下文知识是否可靠仍很关键，本地条件分布诊断没有覆盖真实长系统提示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练教师可读一条操作经验，学生只能读当前任务；学习后清空上下文再作答，才能检验经验是否进入了参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12275">原论文</a> · <a href="../../../../post-training/2602.12275-opcd/">实现解读</a> · <a href="#qa-c0cb6a3f7ec32a4d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcd" data-paper-title="OPCD" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPCD LLM 后训练 Microsoft Research 2026-02-12 提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。论文覆盖经验知识蒸馏和系统提示蒸馏，并支持跨模型尺寸教师。 保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；当前为候选策略机制复现，不等同于 Qwen3/VeRL 原始训练。本地“经验上下文”是已验证答案形成的可审计条件分布，不包含真实长 system prompt；未复跑 FrozenLake、Sokoban 或医疗/安全任务，因此不能将本地准确率与论文横向比较。稳定指标见 omitted-agentic-rl-opd-seed42.json。  Context distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPCD与推理时一直检索同一经验有什么不同？ 持续检索依赖外部上下文与读取成本，蒸馏希望减少这种依赖，但参数更新可能遗忘或过度泛化。两者也可互补，不能无对照断言内化一定更准。 例如经验更新后检索可立即换文档，已蒸进参数的旧经验则未必自动同步。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ad9048a85aaafb61">OPCD与推理时一直检索同一经验有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopcd">OPCD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>持续检索依赖外部上下文与读取成本，蒸馏希望减少这种依赖，但参数更新可能遗忘或过度泛化。两者也可互补，不能无对照断言内化一定更准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如经验更新后检索可立即换文档，已蒸进参数的旧经验则未必自动同步。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12275">原论文</a> · <a href="../../../../post-training/2602.12275-opcd/">实现解读</a> · <a href="#qa-ad9048a85aaafb61">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcd" data-paper-title="OPCD" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPCD LLM 后训练 Microsoft Research 2026-02-12 提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。论文覆盖经验知识蒸馏和系统提示蒸馏，并支持跨模型尺寸教师。 保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；当前为候选策略机制复现，不等同于 Qwen3/VeRL 原始训练。本地“经验上下文”是已验证答案形成的可审计条件分布，不包含真实长 system prompt；未复跑 FrozenLake、Sokoban 或医疗/安全任务，因此不能将本地准确率与论文横向比较。稳定指标见 omitted-agentic-rl-opd-seed42.json。  Context distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPCD的逆KL方向与学生输入分别是什么？ 方向是无经验学生到带经验教师，教师评分同一学生前缀。经验只进教师，不能给学生生成时也加上；本地验证答案条件分布未覆盖长system prompt及原环境。 例如分子换成教师就变成另一方向，不能只看接口名仍写RKL。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cacfa0f1be011404">OPCD的逆KL方向与学生输入分别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopcd">OPCD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>方向是无经验学生到带经验教师，教师评分同一学生前缀。经验只进教师，不能给学生生成时也加上；本地验证答案条件分布未覆盖长system prompt及原环境。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如分子换成教师就变成另一方向，不能只看接口名仍写RKL。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12275">原论文</a> · <a href="../../../../post-training/2602.12275-opcd/">实现解读</a> · <a href="#qa-cacfa0f1be011404">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opsd" data-paper-title="OPSD" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPSD LLM 后训练 University of California, Los Angeles 2026-01-26 普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。轨迹由学生生成，教师只在学生实际到达的前缀上提供全词表监督；逐 token pointwise divergence clipping 防止风格 token 主导训练。 保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；当前为候选策略机制复现，不是 Qwen3 参数级训练。本地特权教师由当前策略与已验证候选答案共同构造，真实更新候选策略参数；未训练 Qwen3，也未复跑竞赛数学数据。该结果只验证双视图数据流、散度与裁剪机制。稳定指标见 omitted-agentic-rl-opd-seed42.json。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPSD为什么同一个模型会形成更有信息的教师视图？ 教师额外看已验证解题信息，学生只看问题，能力差来自信息条件而非独立大模型。它仍依赖特权解可靠，不意味着模型能自行验证所有问题。 例如同一模型知道结论后点评，与不知道结论独立求解，条件不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-opsd-096ec0f1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b8dc4d92c145bd08">OPSD为什么同一个模型会形成更有信息的教师视图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopsd">OPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师额外看已验证解题信息，学生只看问题，能力差来自信息条件而非独立大模型。它仍依赖特权解可靠，不意味着模型能自行验证所有问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一模型知道结论后点评，与不知道结论独立求解，条件不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18734">原论文</a> · <a href="../../../../post-training/2601.18734-opsd/">实现解读</a> · <a href="#qa-b8dc4d92c145bd08">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opsd" data-paper-title="OPSD" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPSD LLM 后训练 University of California, Los Angeles 2026-01-26 普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。轨迹由学生生成，教师只在学生实际到达的前缀上提供全词表监督；逐 token pointwise divergence clipping 防止风格 token 主导训练。 保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；当前为候选策略机制复现，不是 Qwen3 参数级训练。本地特权教师由当前策略与已验证候选答案共同构造，真实更新候选策略参数；未训练 Qwen3，也未复跑竞赛数学数据。该结果只验证双视图数据流、散度与裁剪机制。稳定指标见 omitted-agentic-rl-opd-seed42.json。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPSD的教师能看验证解，为什么学生生成轨迹时必须看不到它？ 同一模型的两个条件视图承担不同角色：教师借验证解提供更强监督，学生仍按部署条件只看问题。教师沿学生实际前缀评分，逐词元散度裁剪避免少数风格位置主导。若学生生成时也读答案，就绕过了待学习能力；本地仅验证双视图和更新机制。 例如教师知道一道题的标准解，可以评价学生写到一半的步骤；学生采样时不能把标准解放在提示中再声称独立解题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-33c5b265f43889b1">OPSD的教师能看验证解，为什么学生生成轨迹时必须看不到它？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopsd">OPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一模型的两个条件视图承担不同角色：教师借验证解提供更强监督，学生仍按部署条件只看问题。教师沿学生实际前缀评分，逐词元散度裁剪避免少数风格位置主导。若学生生成时也读答案，就绕过了待学习能力；本地仅验证双视图和更新机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师知道一道题的标准解，可以评价学生写到一半的步骤；学生采样时不能把标准解放在提示中再声称独立解题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18734">原论文</a> · <a href="../../../../post-training/2601.18734-opsd/">实现解读</a> · <a href="#qa-33c5b265f43889b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opsd" data-paper-title="OPSD" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPSD LLM 后训练 University of California, Los Angeles 2026-01-26 普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。轨迹由学生生成，教师只在学生实际到达的前缀上提供全词表监督；逐 token pointwise divergence clipping 防止风格 token 主导训练。 保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；当前为候选策略机制复现，不是 Qwen3 参数级训练。本地特权教师由当前策略与已验证候选答案共同构造，真实更新候选策略参数；未训练 Qwen3，也未复跑竞赛数学数据。该结果只验证双视图数据流、散度与裁剪机制。稳定指标见 omitted-agentic-rl-opd-seed42.json。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPSD与给学生做答案条件SFT的隔离区别是什么？ 学生采样时不能见标准解，教师沿学生状态给分布；把解法直接拼给学生会让其依赖部署时不存在的信息。完整分布蒸馏也不同于仅模仿一条答案文本。 例如教师知道中间式可以，学生提示里不能藏同一式作为捷径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7fe169a95f58fd9d">OPSD与给学生做答案条件SFT的隔离区别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopsd">OPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生采样时不能见标准解，教师沿学生状态给分布；把解法直接拼给学生会让其依赖部署时不存在的信息。完整分布蒸馏也不同于仅模仿一条答案文本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师知道中间式可以，学生提示里不能藏同一式作为捷径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18734">原论文</a> · <a href="../../../../post-training/2601.18734-opsd/">实现解读</a> · <a href="#qa-7fe169a95f58fd9d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opsd" data-paper-title="OPSD" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPSD LLM 后训练 University of California, Los Angeles 2026-01-26 普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。轨迹由学生生成，教师只在学生实际到达的前缀上提供全词表监督；逐 token pointwise divergence clipping 防止风格 token 主导训练。 保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；当前为候选策略机制复现，不是 Qwen3 参数级训练。本地特权教师由当前策略与已验证候选答案共同构造，真实更新候选策略参数；未训练 Qwen3，也未复跑竞赛数学数据。该结果只验证双视图数据流、散度与裁剪机制。稳定指标见 omitted-agentic-rl-opd-seed42.json。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPSD的pointwise clipping为何不是把整个响应一个系数截断？ 它控制逐词元散度贡献，避免少数风格位置主导；粒度不同于序列整体裁剪。teacher目标冻结，响应mask一致，本地双视图核不含Qwen竞赛数学训练。 例如一个格式词异常差距不能凭自身放大整条监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0c3aec8cf1f24e30">OPSD的pointwise clipping为何不是把整个响应一个系数截断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopsd">OPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它控制逐词元散度贡献，避免少数风格位置主导；粒度不同于序列整体裁剪。teacher目标冻结，响应mask一致，本地双视图核不含Qwen竞赛数学训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个格式词异常差距不能凭自身放大整条监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18734">原论文</a> · <a href="../../../../post-training/2601.18734-opsd/">实现解读</a> · <a href="#qa-0c3aec8cf1f24e30">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

教师看到了答案、图像证据或专长提示，怎样把帮助传给没有这些信息的学生？

## 记住这一点

教师和学生可以是同一个模型的不同条件视图。OPSD让训练期教师额外读取验证过的答案或解题信息，学生仍只看可部署输入；多教师与token路由进一步决定不同位置向谁学习。关键是额外信息改变了什么监督、教师建议是否适合学生，以及监督是否会侵蚀学生原本成功的行为。

## 一个例子

例如学生在一道图表题上读错刻度，教师训练时能看到证据裁剪或解释。可让教师在相同学生前缀上提供纠错分布，再只用无特权输入更新学生。若数学段与代码段使用不同专家，软路由需要在同一词表上混合有效概率；简单平均两个模型的logits，并不等于混合它们的预测分布。

## 什么时候要小心

特权参考只能处于允许的训练教师或评分边界，不能混入被评估学生输入。教师更自信也可能更错，拼接多个教师不保证互补。此组不少实现只是双视图、路由或梯度组件；完整蒸馏因成本未复现的结论和本地诊断必须同时保留，不能用模块运行替代模型能力。

## 先读这几篇

先读OPSD，分清同参数、不同条件视图；再读Token-Level Teacher Selection，理解按位置选择教师及概率混合；最后读MOPD，思考多教师整合中的能力冲突与保留。

1. [OPSD](../../../post-training/2601.18734-opsd/README.md) · [原论文](https://arxiv.org/abs/2601.18734)
2. [Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation](../../../post-training/2610.21234-token-teacher-selection/README.md) · [原论文](https://arxiv.org/abs/2610.21234v1)
3. [MOPD](../../../post-training/2606.30406-mopd/README.md) · [原论文](https://arxiv.org/abs/2606.30406)

## 自测一下

同一个模型既当教师又当学生，是否必然没有新增学习信号？

??? note "展开参考答案"

    不必然。同一参数在不同上下文、证据或推理路径下会给出不同条件分布，这种差异可形成训练信号。但它是否有益仍须验证；如果师生输入和分布完全相同，或者差异只来自无关文风，不能期待稳定的能力增长。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
