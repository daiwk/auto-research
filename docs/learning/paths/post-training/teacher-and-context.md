---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 教师与纠错：额外信息何时能帮到学生

[LLM 后训练](index.md) / 47 个问题 · 47 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">47 个问题 · 47 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:aopd" data-paper-title="When to Follow the Teacher: Advantage-Based On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="When to Follow the Teacher: Advantage-Based On-Policy Distillation LLM 后训练 University of Pennsylvania 2026-10-22 普通 OPD 在学生实际访问的状态上模仿教师，但教师偏好的动作不一定能被当前学生继续完成。AOPD 用该动作对学生最终奖励的优势加权教师监督，通过学生原有 rollout、终局奖励及教师重要性比率估计，不额外生成反事实续写。 完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。oracle 仅存在测试代码，不进入损失或诊断策略。本地状态：L1 精确损失组件，diagnostic only。实现论文 Eq. 3.6 / 3.8 与 Algorithm 1 的 leave-one-out baseline，不是完整 LLM 训练器或能力复现。完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。leave_one_out_advantages 按 prompt group 独立计算 baseline；  On-policy distillation 优势加权蒸馏与无额外rollout估计 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 AOPD为什么不只给KL乘一个reward，而需要采样项与全词表教师期望共用截断测度？ 目标关心教师动作对当前学生后续奖励的优势，估计包含两项相消结构。只截断采样项、或把教师测度重新归一化，会破坏对应关系，变成另一目标。leave-one-out基线来自同题其他rollout，教师与行为概率冻结，不额外生成反事实续写来伪造优势。 教学例子：教师偏好一个学生暂时接不下去的开头，不能仅因教师概率高就强化；需结合学生真实续写结果，判断指导是否可利用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-aopd-187dc1ba" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minimal-edit-opd" data-paper-title="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning LLM 后训练 Meta Superintelligence Labs 2026-10-21 ME-OPD 用训练专属描述与参考解法，让教师为错误的学生回答打分，只纠正教师不支持的 token；正确回答只走任务奖励，避免整段模仿。它针对小型视觉语言模型误读斜边、标签或几何关系的问题，保留原回答中无需修改的推导与措辞。ME-OPD 让教师在训练时看到图形描述、已验证参考解法和学生的完整原回答，要求“用最少编辑修正”。教师不生成新答案，而是 teacher-force 同一学生回答的第二次出现，为原 token 打分。最终答案验证正确的 rollout 只走任务 GRPO； 完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。多个 seed 仍是 L1 机制诊断，不构成能力比较。本地状态：L1 精确路由 / 纠错目标组件，diagnostic only，不是 VLM 能力复现。完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。GRPO 的未公开实现细节不冒充论文原配置。freeze_rollouts 接收外部 verifier 的二元奖励和外部全组优势，复制并冻结旧学生 / 教师概率、mask 与路由。它不判断自然语言答案正确性，不生成图形描述，不校验参考解法是否真的通过验证器。  On-policy distillation 多模态最小编辑纠错 LLM 后训练 教师与纠错：额外信息何时能帮到学生 ME-OPD为什么正确rollout不走教师纠错分支，错误rollout也只选一部分token？ 正确轨迹只保留任务奖励，避免教师风格压过已成功的学生行为；错误轨迹才比较教师与冻结旧学生，只纠正教师更不支持的位置。先在完整同题组计算任务优势，再拆分支，否则只剩正确组会失去相对信号。参考解和完整回答只进入训练教师视图。 教学例子：学生几何推导仅误读一个标签，教师评分可集中压低相关错误token；不能因表达不同就重训整条已正确回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-minimal-edit-opd-97f1b5ed" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:csd" data-paper-title="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer LLM 后训练 NVIDIA 2026-10-20 师生词表大小、token ID 与分词边界不一致，不能直接逐坐标 KL。CSD 先按原文字符区间对齐 chunk，再通过解码文本等价构造共同事件。1:1 采用共同 token；1:N 或 M:1 固定观察到的 chunk 前缀，只枚举末 token 的等价续写；M:N 默认只保留实际观察序列。未显式匹配的质量进入 REST，而不是被丢弃或重新归一化。 完整实验成本过高，不复现（审查 DONE）。微型诊断使用两套不同大小的词表与不同分词，覆盖四种 chunk 形状。L1 跨 Tokenizer 对齐与损失组件，不是大模型能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。v1 提交在 10 月 20 日截止时间之后，本轮归 2026-10-22 首次公告，不改写其真实提交日期。align_offsets 对原文字符 span 做最小公共边界对齐并核对整体 decode；paired_completions 在固定前缀下按文本建映射，不按相同 ID、概率排名或给定相似分配对；  知识蒸馏 跨Tokenizer共同事件分布 LLM 后训练 教师与纠错：额外信息何时能帮到学生 CSD跨tokenizer蒸馏时，为什么保留REST质量而不能对共同候选重新softmax？ 不同分词的token ID没有直接对应，需按解码文本事件和完整链式概率建立共同空间。显式匹配以外的质量进入REST，保留未列出事件的影响；重新归一会把这些质量丢掉并改变散度。共同文本对齐也必须核对字符边界，不能只按位置凑齐两套token。 教学例子：一个模型把词分成两段，另一个用单token；匹配该词事件后，其余续写概率仍存在，不能假装共同事件就是整个词表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-csd-2e95adef" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:apsd" data-paper-title="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization LLM 后训练 Korea University 2026-10-19 反馈条件自教师可能破坏正确rollout里学生已经成功的偏好，却又对错误rollout纠正不足。APSD依据正确性调整蒸馏target：正确时在学生和自教师之间插值，错误时越过自教师外推。关键不只是换一个target数值，还要保留target对学生分布的依赖；整个target一起detach会丢掉定义性的耦合梯度。原文§4及附录B 原图建议：Figure 3方法总览，保留右侧梯度几何与target分支；Figure 1是插值／外推的概念图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，学生实际采样回答。每次更新从同一当前学生复制自教师，教师只在额外的合成训练反馈条件下重放学生回答并停止梯度；不是单独初始化的外部教师。actor的采样条件只有公开prompt，不读取反馈、正确性或gold。反馈ID不代表自然语言执行错误或真实成功解答。  On-policy distillation 自蒸馏与训练稳定性 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 APSD只冻结自教师，为什么不能把整个插值或外推target都detach？ target同时依赖冻结教师与当前学生，正确轨迹插值、错误轨迹外推改变的还有学生依赖分支的梯度。把整体detach只留下部分模仿项，会丢掉定义性的耦合修正。数值上目标一样不代表反向一样，反馈只用于训练自教师，不能进入部署学生输入。 教学例子：两个实现算出相同target概率，但一个保留其对学生分布的导数、另一个冻结；即使loss相同，参数更新也会不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-apsd-7a5d9aba" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:visually-attributable-opd" data-paper-title="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation LLM 后训练 Baidu Inc. 2026-10-19 特权图像裁剪带来的 teacher 修正，可能混有语言先验或风格变化。VAG 让同一 EMA 教师对证据保留裁剪和随机遮挡裁剪重放相同学生前缀，只接纳与视觉对比方向一致的修正，再以有界项调制 verifier 的组归一化 advantage。纯文本教师或固定 logits 门控不能冒充该多模态链路。 仅资料收录，成本过高，不复现（审查 DONE）。仅资料收录，成本过高，不复现（审查 DONE）。没有本地可执行 adapter、评测接口或机制验证；不接入 Evolve，不作为能力证据，不进入自动重试队列。完整实验不复现，审查 DONE。原文 §4.1：Qwen3.5-4B/9B 全参数训练一 epoch，batch 48，每题条响应，最大 1,024 token，8×NVIDIA H800。需要训练数据的目标细节裁剪、EMA 双视图重放和六基准 judge 协议。单 A100/A30 或 Mac 不承担原矩阵，属于配置直接支持的高成本判断，无需下载权重或试跑。  On-policy distillation 多模态RLVR与视觉归因 LLM 后训练 教师与纠错：额外信息何时能帮到学生 VAG为什么只接受与证据保留/退化视图对比同号的教师修正？ 特权裁剪带来的修正可能来自语言风格而非视觉证据，同号门控要求它与视觉对比方向相容，再以有界项调制原verifier优势。两分支必须是同一EMA教师，仅改变视觉输入。这个控制不能用两份任意文本logits替代，当前库也未执行完整多模态链路。 教学例子：裁剪后教师更偏爱某个措辞，但遮挡关键图像时偏好不变，说明修正未必由视觉证据驱动，不应一律当作视觉指导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-visually-attributable-opd-08abcb9d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spod" data-paper-title="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation LLM 后训练 University of Southern California 2026-10-18 多轮Agent蒸馏中，学生可能先超过教师，再随着持续模仿而退步。作者区分两个过程：教师修复学生的弱决策，同时也会侵蚀学生已经成功、但与教师偏好不同的行为。SPOD只在成功训练episode内保护教师整action概率更低的decision，取消该处蒸馏压力，并用软概率floor抵消来自其他状态更新的间接侵蚀；其余decision继续正常蒸馏。原文§3–4 原图建议：附录Figure 9的训练流程；Figure 1展示overshoot与修复／侵蚀现象，可作为辅助结果图。原图不是本地运行结果。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是Agent能力复现。L1 定义性组件／梯度诊断，不是Agent能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，实际采样多state episode；教师独立随机初始化后冻结，对同一学生action重放评分。显式合成环境在episode结束后返回训练成功位，actor输入只有公开历史、自己的action及公开观察ID；不读取成功位、gold或评估结果。固定长度预算的合成action不是ALFWorld/WebShop/ScienceWorld语言动作。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 SPOD为什么按完整action原始概率保护成功选择，而不能逐token比较后屏蔽整个成功episode？ 保护条件针对成功episode中教师更不支持的具体decision，完整action概率包含其token共同作用。逐词开关或整段屏蔽会改变保护对象。受保护处取消蒸馏并加软概率floor，其他decision仍学习；软floor不能阻止共享参数从别处间接侵蚀该动作。 教学例子：一个成功工具调用的某些词教师更喜欢、另一些更不喜欢，逐词投票可能与整条调用概率比较给出相反结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-spod-93843af2" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:multiagent-opd" data-paper-title="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation LLM 后训练 Alibaba Group 2026-10-16 层级团队的最终答案能监督Leader，却难以判断Searcher的检索、总结是否真正有效。MultiAgent-OPD先在较简单的Searcher–Answerer流程训练教师，再从相同的基础checkpoint重新开始训练共享参数的Leader–Searcher–Answerer团队。冻结教师为学生实际搜索轨迹提供局部OPD反馈；Leader根据团队结果、Answerer根据自己的候选正确性学习。原文 §3 原图建议：Figure 1 层级工作流；如只保留一张，应同时可读出阶段一教师和阶段二角色分工。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。不用固定工作流、随机教师或单个蒸馏算子冒充端到端多Agent系统；未接 Evolve。成本过高，不复现（审查 DONE）。基础模型Qwen3-4B-Instruct-2507，两阶段使用79,168条NQ和90,447条HotpotQA，batch32题×5轨迹、每次多个PPO更新，层级流程包含多波委派、最多12环境步及每请求5个回答候选；还需真实搜索服务。评测是七个数据集合计固定5,000题，每个方法每题四次独立工作流，不是每数据集5,000题。原文当前配置未明确完整GPU数，不臆造显卡数量或训练时长。  Agentic RL On-policy distillation 多Agent协作 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MultiAgent-OPD为什么用简单团队训练教师，却从原基础checkpoint重新训练层级学生？ 先训练的Searcher–Answerer提供任务相关局部指导，第二阶段重新起步可区分教师知识与层级架构学习。Leader、Searcher和Answerer虽然共享参数，仍接收各自角色信号；Searcher教师读其真实子任务与检索历史，不是把全局gold答案交给所有角色。 教学例子：团队最终答错可能因分工，也可能因检索摘要差；只把最终奖励均匀撒给所有角色，会丢掉局部学习信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-multiagent-opd-b3177be0" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:treeopsd" data-paper-title="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning LLM 后训练 Tsinghua University 2026-10-16 长轨迹仅有终局奖励时，同一轨迹的好坏动作容易一起获奖或受罚；同一批轨迹又会经历多次更新，旧信用不能告诉优化器何时停止。TreeOPSD 将续写分支整理成共享前缀树，把叶奖励按行为策略似然向上回传，再把每个 turn 的信用映射为一个冻结且有界的 Bernoulli 教师。学生相对旧策略的变化达到目标时梯度消失，超过目标则反向，不再只有无限推进的方向。原文 §2–3 原图建议：Figure 2 方法总览，展示树信用、冻结后验教师与多次更新；Figure 1 是概念插图，不宜代替算法图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维 GRU 因果策略，实际采样三 turn 轨迹并从中间前缀继续采样；每个 turn 两个 actor token，非终局附带一个公开观察 ID。显式合成终局奖励由末 turn 的 token 计算，不传入 actor；它不是自然语言搜索 verifier。树合并保留完整历史、观察和终止标记，重复叶仍保留在和奖励统计中。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 TreeOPSD为什么把树回传信用变成有界Bernoulli教师，而不无限重复原奖励梯度？ 终局信用给出改善方向，却不自动告诉多次更新何时停止。冻结有界目标把方向变成有限距离，学生相对旧策略的变化达到目标后梯度消失，超过后会拉回。树中共享turn须去重，分支权重来自完整actor span行为似然，不能任意改为平均token分数。 教学例子：同一批成功轨迹训练很多轮时，有限目标可在“学够了”后停下；单一固定正优势则可能一直推高同一选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-treeopsd-8a101275" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cce-opd" data-paper-title="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models LLM 后训练 The Chinese University of Hong Kong, Shenzhen 2026-10-15 教师可能跟随学生错误 reasoning prefix，而忽略题目条件。CCE 在完全相同的学生 response prefix上，让同一冻结教师分别读取完整题目与遮蔽一个有效前提的题目，以 clipped log-prob contrast 调整辅助 target。学生始终从完整题目生成；未通过 condition eligibility 或 entropy gate 的位置仍保留原 sampled PPO-OPD。 完整实验成本过高，不复现（审查 DONE）。L1 双视图 / union / auxiliary-KL / sampled PPO 组件。只接受已审阅的合法 condition span，不提供伪造的语义抽取器。完整实验成本过高，不复现（审查 DONE）。公开 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784，train/validation/test 原始 byte 区间 80%/10%/10% 分离。微型教师只作公开文本 next-token 训练，并非数学教师。  On-policy distillation 后训练算法组件 CCE-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 CCE-OPD为什么两份教师视图必须保持同一学生response prefix，学生分布又不能在候选上重归一？ 固定前缀使差异主要来自题目条件遮蔽，而非另一条推理轨迹。辅助教师目标在其候选支持上归一，但学生保持完整词表softmax，才能保留支持集之外的概率梯度。合法条件与熵门控只控制附加项，不通过时仍保留原OPD，不是整段跳过。 教学例子：只遮掉一个有效前提再看教师下一词变化；若同时重写了学生前文，就无法把变化归因于这个前提。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-cce-opd-2c59e40e" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:elite-replay" data-paper-title="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search LLM 后训练 The Ohio State University 2026-10-15 单纯提高正确率的 RL 可能压缩正确解法的覆盖范围。EliteReplay 先用冻结基模和 MAP-Elites 收集不同正确策略，训练时持续回放固定档案。档案按问题、approach 与结构特征分 cell，每格只保留最短已验证解；不是把 IID 样本放进普通 replay buffer。 完整实验成本过高，不复现（审查 DONE）。L1 MAP-Elites / archive / sampler / mixed loss 组件。本地保留真实目标导向搜索，但算术 grammar 不是论文的 SQL LLM，审阅 approach 列表不是 LLM labeler；不以微型结果宣称 BIRD/Spider 能力。完整实验成本过高，不复现（审查 DONE）。runner 提供三个固定整数加法任务，候选为四种可解析表达式。一个小型冻结线性策略在原任务、目标 approach、parent 是否存在的条件下实际采样候选；AST whitelist 计算表达式结果进行验证，不执行任意生成程序。  Reference anchor 后训练算法组件 EliteReplay LLM 后训练 教师与纠错：额外信息何时能帮到学生 EliteReplay为什么按实际实现的approach存cell，并先平衡问题再平衡cell回放？ 请求一种解法不代表模型真按该路线生成，按请求标签存档会伪造多样性。实际descriptor决定cell，每格只保留最短已验证解；回放先平衡问题，避免档案大的题占过多训练权重。质量多样性档案因此不同于普通IID成功样本缓存。 教学例子：要求用几何法，模型却用了代数法，应归入实际代数cell；否则同一种解法会被多个请求标签包装成多样策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-elite-replay-bbf50043" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd-reminder" data-paper-title="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents LLM 后训练 Tsinghua University 2026-10-15 编码 Agent 的最终通过/失败不能指出哪一轮忽略了已有约束。OPRD 在学生自己生成的无提醒轨迹上训练：成功轨迹自模仿；失败轨迹由教师读取训练专用提醒，重新评分同一学生前缀，不是教师另生成一条答案。全局提醒持续有效，观测对应的局部提醒只在下一轮有效，之后必须移除。正式推理去掉教师和全部提醒。原文 §3 完整实验成本过高，不复现（审查 DONE）。奇偶校验只用于构造诊断 outcome，不是编码正确性。L1 算法组件，不是 SWE-bench 编码能力复现。已实现作用域、同前缀评分和训练目标；完整实验成本过高，不复现（审查 DONE）。不进入 evolve 晋级。本地使用随机初始化的128词表、12维 causal cumulative-embedding 策略。每步真实采样8条三轮轨迹、每轮2个 token；奇偶校验只用于构造诊断 outcome，不是编码正确性。教师重新读取相同 response 前缀；学生上下文不含提醒。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPRD的局部提醒为什么只作用于对应观察的下一轮，不能永久留在教师上下文？ 局部提醒描述某个观察触发的短期约束，过期后继续保留会影响无关后续决策。全局提醒与局部提醒作用域不同，教师重评同一学生前缀而非另生成答案；部署学生不带提醒。成功自模仿与失败蒸馏也须分别归一，不能把两类轨迹混成一种标签。 教学例子：某次编译输出提示先修依赖，提醒针对紧接着的动作；之后依赖已解决，就不应在每轮都继续把它当未完成约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-oprd-reminder-a48a675d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:shared-residual-distillation" data-paper-title="Learning from Unverified Peers via Shared Residual Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Unverified Peers via Shared Residual Distillation LLM 后训练 Shanghai Jiao Tong University 2026-10-15 没有标准答案或可验证 reward 时，整段错误解答也可能包含有用步骤。SRD 不投票选“正确答案”，而比较同题 peers 相对跨题 control 对 token 分布的改变，只接收多位 peer 共同支持的保守残差。学生仍只读取题目与自己的前缀，训练后的推理不需要 peers。 完整多模型实验成本过高，不复现（审查 DONE）；L1 公式、采样隔离与梯度组件，不是数学能力复现。完整多模型实验成本过高，不复现（审查 DONE）；本地不下载 Qwen、不调用外部教师，不进入 evolve 晋级。使用固定两个整数 prompt、8-token vocabulary、随机初始化的 causal cumulative-embedding 小策略。每个更新重新实际采样每题四条长度四的轨迹；均匀保留两个 peers，余下作为 targets；control 来自另一题。冻结初始策略逐前缀读取各上下文，学生不读 peer/control 或标准答案。  On-policy self-distillation 后训练算法组件 SRD LLM 后训练 教师与纠错：额外信息何时能帮到学生 SRD没有验证过的peer答案，为什么只接收多个peer同号的最小残差，而不多数投票选一整份解？ 整份错误答案仍可能含有可复用局部信号，同题peer相对跨题control的变化用于分离题目相关影响。只有同号部分取保守幅度，避免单个peer强推目标；学生仍只看自身前缀。共享残差不是正确性证明，也不能把target自己放回peer上下文制造自我支持。 教学例子：几份未验证推导都弱支持同一中间词，但对结论意见冲突；可以保留保守共同部分，而不宣布票最多的整份解正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-shared-residual-distillation-a834c6f2" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tf-opd" data-paper-title="Training-Free On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Training-Free On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-15 共同初始化的专家模型，其线性层融合可以写成匹配各教师输出的最小二乘。关键不是任意协方差，而是每个教师在自己生成的、经过终止和循环筛选的答案上实际遇到的输入二阶矩；统计按 token 数归一，不能让长答案自然压倒其他领域。 完整实验成本过高，不复现（审查 DONE）；L1 公式组件与微型自回归诊断，不是完整论文复现。L1 公式组件与微型自回归诊断，不是完整论文复现。完整实验成本过高，不复现（审查 DONE）；adapter: null、evolve_integrated: false。公开 Hamlet（Gutenberg 1524），固定内容 revision 为 sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784。  多教师能力整合 后训练算法组件 TF-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 TF-OPD为什么收集每个教师自己生成答案时的输入二阶矩，而不随便用一份公共协方差？ 闭式融合要匹配教师在自身实际访问输入上的输出，二阶矩定义了哪些方向的误差重要。换成任意公共统计会改变最小二乘目标；自然终止与循环过滤、token归一也影响支持。无训练指不做梯度蒸馏，并不意味着不需要生成、回读和线性求解成本。 教学例子：两个专家使用不同领域的输入方向，统一协方差可能忽略其中一个领域；各自真实轨迹统计才能反映这种支持差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-tf-opd-c139b549" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:token-teacher-selection" data-paper-title="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation LLM 后训练 Princeton University 2026-10-15 一个教师未必适合学生整段推理：数学推导和代码生成可能需要不同专家，强教师与学生的分布差距也可能太大。论文把 OPD 的教师选择细化到每个学生实际访问的前缀。路由依据可以是教师置信度、师生分布 Hellinger 距离，或对齐隐藏空间的特征平方距离。软路由混合的是概率，不是 logits 或 log-prob 的平均。原文 §3 原文中理论分解和实验表分别讨论教师能力、师生距离和多样性；不要把原文“存在不劣路由”的可能性结论读成每个路由启发式都保证更优。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。三个随机初始化的32词表、8维 causal 策略分别作为学生和两个冻结教师。学生真实采样4-token响应，所有教师评分相同前缀；默认三次更新依次执行 entropy、Hellinger、features 三个准则。使用随机模型，不能衡量真实教师能力或 kernel 正确率。  On-policy distillation 多教师与路由 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生 逐token软选教师时，为什么平均教师概率与平均logits不是一回事？ 概率算术混合表示在教师分布之间分配权重，logits或log-prob平均再归一则形成另一种组合，尤其在意见冲突和尾部差异时不同。路由依据还需区分置信、分布距离与对齐表征；强教师并非每个前缀都合适，启发式选择没有普遍更优保证。 教学例子：数学专家和代码专家各自确信不同续写，各取部分概率质量与取两者共同支持的几何组合，会给学生不同目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-token-teacher-selection-efd8fec8" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:waypoint-opd" data-paper-title="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation LLM 后训练 Alibaba Cloud Computing 2026-10-15 仅 initial/final 的 log-probability 位移不能区分“前后两段同向”与“中途反转”。同一 RL run 的 waypoint 只提供一致性证据，不是新的模仿目标。候选由学生 top-k 选择，early/late 位移先按候选学生权重中心化，再以正 cosine 缩放 endpoint credit。 完整实验成本过高，不复现（审查 DONE）；当 gates 全零且 KL 也无梯度时，runner 仍明确失败，并附 seed/step/诊断；L1 gate / dense PPO 组件与真实微型策略更新。完整实验成本过高，不复现（审查 DONE）；不是教师大模型训练重跑，也未集成 evolve。使用固定 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 分为 train/validation/test。  On-policy distillation 后训练算法组件 WAYPOINT-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Waypoint-OPD为什么用同次RL中间checkpoint作一致性门，而不把它作为另一个蒸馏目标？ 起点到终点的相同位移可能来自持续同向改进，也可能中途反转，waypoint用来辨认这两种历史。early与late位移在学生候选权重下中心化后比较方向，只缩放endpoint信用。中间模型不是额外要模仿的答案，低范数回退和冻结门控也属于定义。 教学例子：两个教师最终都提高同一词概率，一个一路提高，另一个先降后升；中间检查点能区分路径，但不必要求学生停在中间状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-waypoint-opd-30b78a3d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rshd" data-paper-title="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight LLM 后训练 University of California, San Diego 2026-10-14 一组 GRPO rollout 全部失败时，组内 advantage 全为0。RSHD 不把参考答案告诉模型，而让同一策略根据失败响应写纠错 note，再用 note 生成新的 replay。只有 replay 通过率严格超过原组，note 才被接纳；之后蒸馏的也不是旧失败响应，而是 note 实际诱导的新续写。推理时只需无 note 学生。原文算法1–2 原文 Figure 2 展示上述完整数据流；Figure 1 说明难题组出现全失败的比例，不能拿它作为本地数据分布。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表因果模型按每题8条响应真实采样；末 token 余数条件只作人工二值 verifier。note writer 的输入只有原提示、失败响应和“失败”标记，不包含 reference token。诊断用精确 token 子序列筛查答案泄漏，重放每 note 两条、严格比较原组通过率，再均匀选取一条 replay 做真实同前缀双评分与梯度更新。  RLHF / RLVR On-policy distillation 失败重放与探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSHD为什么必须用note生成新replay并验证通过率提高，而不直接蒸馏旧失败回答？ note是否有用要由它实际诱导的新行为检验，严格高于原组通过率才接纳。随后均匀选择接纳replay，在同前缀比较有无note的正lift，不只挑成功例。旧失败轨迹没有因此变正确，note也不能含gold；没有有效note时附加项为零。 教学例子：复盘建议听起来合理，但新生成仍全错，就不能把它当有效教师；一次事后解释不等于真的修复了行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-rshd-81aa0b1d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:loopsd" data-paper-title="LoOPSD: On-Policy Self-Distillation with Looped Teachers" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LoOPSD: On-Policy Self-Distillation with Looped Teachers LLM 后训练 Anhui Province Key Laboratory of Digital Security 2026-10-13 在线自蒸馏需要比学生更有用的教师，但更大外部模型或额外答案上下文并非唯一来源。LoOPSD在不改权重时搜索重复层区间来构造教师，用学生自产前缀进行蒸馏，再从更新后的学生重新搜索下一轮教师。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Appendix A：全部连续层区间先筛128题，24条候选再评872题，前5与标准路径评独立100题；每轮200updates×12题×4responses、每响应上限1024tokens，最多10轮。以Qwen3-1.7B/4B/8B等重复教师计算，完整路线搜索和OPD总预算明显较高；这是上限/配置推断而非实测时长，不做昂贵探针。  on-policy-self-distillation layer-route-search iterative-teacher LLM 后训练 教师与纠错：额外信息何时能帮到学生 LoOPSD不新增权重而重复一段网络层，为什么仍有教师成本，也需要独立validation选路由？ 重复层改变计算路径和条件分布，可形成更有用的教师，但每token要额外执行这些层，搜索还会多次评估候选。只按独立validation选择优于标准路径的路由，再在学生自身前缀蒸馏；test不能参与选择，无新参数也不代表免费或保证更强。 教学例子：同一本笔记再读关键章节可能改善理解，但耗时增加；挑哪段重复应在开发题验证，不能看最终考试答案来选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-loopsd-e562cd53" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cast-opd" data-paper-title="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation LLM 后训练 Taobao &amp; Tmall Group of Alibaba 2026-10-09 异构 tokenizer 的同一文本有不同分段，直接比较 token ID 无意义。CAST 先匹配实际解码文本，将教师 span 的总 log probability 均匀投影到学生 span，再按不确定性×局部平滑度分配 credit；未对齐位置通过初始学生 KL 限制漂移。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为未蒸馏的相同student checkpoint，实验组执行异构tokenizer文本span对齐与credit/anchor训练；本地弱teacher短运行不证明有效知识迁移，稳定相对提升不适用。  Cross-tokenizer distillation Token credit assignment Selective KL anchoring LLM 后训练 教师与纠错：额外信息何时能帮到学生 CAST为什么先按解码文本span对齐，再把教师总log概率投到学生位置？ 异构tokenizer的ID和边界不同，逐位置比较没有共同事件含义。文本span提供对应范围，教师总分再投影并按不确定性与平滑度分配，保持chunk总信用；未对齐部分由初始学生锚定。对齐失败应明确保留边界，不能把不相关token硬凑成监督。 教学例子：教师用一个token表示词，学生拆成几段，不能把教师分数只给第一段；需要先确认两边解码的是同一文本范围。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-cast-opd-cae7ae27" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:road-mopd" data-paper-title="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation LLM 后训练 Nanjing University / JD.com 2026-10-09 多域只路由各自教师，不能防止共享参数更新损害其他能力。Road 用未路由教师在当前目标域的同一学生轨迹上给出兼容性证据，调节 token credit，再求真实辅助梯度，投影目标梯度但保留其范数下限。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为不投影的多教师OPD，实验组执行按域teacher路由与逐tensor预防式梯度投影；小型公开算术域运行是机制诊断，稳定相对提升不适用。  Multi-teacher distillation Gradient projection Cross-domain guarding LLM 后训练 教师与纠错：额外信息何时能帮到学生 Road-MOPD为什么让未路由教师在当前域轨迹上提供证据，还对目标梯度设范数下限？ 只听当前域教师可能通过共享参数损害其他域，辅助教师在同一学生状态上的兼容性提供保护线索。先调token信用再处理真实辅助梯度，冲突投影同时限制目标梯度被削弱程度。范数下限是取舍，不保证所有域同时改善，也不能用随手向量代替真实目标梯度。 教学例子：训练数学专家时，代码教师可检查同批前缀是否受到不利更新；完全删掉冲突方向又可能让数学任务几乎不再学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-road-mopd-dfda03a0" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:meta-opd" data-paper-title="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation LLM 后训练 East China Normal University 2026-10-08 轻量权重网络根据师生预测学习 token 监督权重。它通过一次可微虚拟学生更新后的参考解损失获得元梯度，再使用新权重执行真实学生更新。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  On-policy distillation Meta-learning LLM 后训练 教师与纠错：额外信息何时能帮到学生 MetaOPD为什么需要一次可微虚拟学生更新，不能只按当前loss给token调权？ 当前loss大可能来自难噪声，未必对下游有益。虚拟更新让权重网络观察这些权重将怎样影响训练参考解损失，再取元梯度更新权重，随后执行真实学生步。参考解只在训练外层目标，描述特征和所用优化器状态也需按定义隔离，不能偷用测试答案。 教学例子：一个高loss词只是无关文风，另一个决定解题方向；虚拟试走一步后，可比较哪种加权更能帮助训练参考任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-meta-opd-c3af9659" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sguid" data-paper-title="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution LLM 后训练 New York University 2026-10-08 语义相关不代表技能真正能够教会模型。SGUID 先从当前模型的已验证训练轨迹生成候选技能，再观察技能在蒸馏早期、晚期是否持续提供与验证器一致的信号。探测训练完成后恢复本轮初始权重，只用通过筛选的紧凑库重新训练；下一轮由更新后的模型重新产技能，不沿用固定手写库。 不复现原 all-linear rank-64、dropout=0.05、原技能生成提示或数学大赛收益。8 次真实梯度更新使 adapter 探测位移为 0.03139，但所有技能的早/晚积极教学次数均为 0，因而无技能入选，精确恢复本轮初始权重，未执行紧凑库训练和第二轮。Qwen3.5-9B 的固定扩展协议已在 A100 完成两轮、464 次真实梯度更新，技能筛选、权重恢复与重新蒸馏均通过机制核验。4 题 validation 的 EM 从 75% 降到 25%，前后均有 2 题截断；保留负结果。GPU 回执只证明 L1 有界机制执行，不证明能力提升。此前失败运行也保持原样归档。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 SGUID探测技能教学效果后，为什么恢复本轮初始权重，只用紧凑库重新训练？ 探测阶段同时尝试大量候选，若直接继承探测后模型，就无法区分筛选库与额外训练的作用。恢复起点后用筛中技能重训，才隔离课程选择效果；下一轮再由更新模型生成新技能。语义检索次数不是有效教学次数，早晚持续信号还要与verifier方向一致。 教学例子：测试十种解题提示已让学生多练许多题，若不恢复起点，就不能说后来提升只来自最终选中的两种提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-sguid-340394af" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:where-opd" data-paper-title="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes LLM 后训练 Valeo.ai 2026-10-01 程序化合成场景自动给出对象身份和空间坐标；teacher 接收文本化空间特权信息，student 只看图像与问题，在自己的 on-policy token 上蒸馏 teacher。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  多模态后训练 OPD 空间引导 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Where-OPD为什么让教师读文本化空间坐标，而学生只看图像与问题？ 合成场景提供可精确描述的对象身份和位置，作为训练期特权信息帮助教师在学生前缀上给监督。学生部署时不依赖这些坐标，所以不能把它们混入原始学生输入。空间mask与信息边界要保留，随机logits的KL检查不证明模型学会视觉空间推理。 教学例子：教师知道球在盒子左侧的精确坐标，学生只能从图像判断；训练可借教师纠偏，测试不能直接把坐标告诉学生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-where-opd-73f1d45e" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:advisd" data-paper-title="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation LLM 后训练 University of Southern California 2026-09-29 冻结 executor，只训练 advisor；反思先提出修正，再对同一已记录 executor 响应分别计算有建议与无建议的平均 log-likelihood，只有影响幅度超过 donor-advice 校准阈值的决定才进入自蒸馏。 不调用 Gemini/Claude executor，未复现 BFCL-v3。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Advisor 自蒸馏 GRPO LLM 后训练 教师与纠错：额外信息何时能帮到学生 AdviSD为什么固定同一条执行器回答，比较有无建议时的概率？ 固定回答能把差异集中到建议如何改变执行器对这条回答的偏好，避免两次生成的随机差异混入效果估计。顾问只学习超过校准阈值的反思建议，执行器保持冻结。概率提升是筛选信号，不等价于任务成功，阈值也依赖所用建议分布。 例如执行器已给出一次工具调用，分别在有建议和无建议的上下文中给这次调用打分；不另生成两次回答后直接相减。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-advisd-0fd17b91" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lego-opd" data-paper-title="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation LLM 后训练 KAIST 2026-09-29 把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 factorized teacher composition；未加载 LLM/VLM teacher。执行 factorized teacher composition；未加载 LLM/VLM teacher。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  OPD 多模态后训练 teacher composition LLM 后训练 教师与纠错：额外信息何时能帮到学生 LEGO-OPD为什么让语言专家给先验、视觉专家给似然，而不直接平均两个教师？ 语言专家负责一般词语和推理的先验，视觉专家提供与画面有关的证据修正；两者按专家乘积组成蒸馏目标，避免把视觉模型的语言偏差一起照搬。角色分解仍依赖视觉似然是否可靠，本地仅验证组合目标，不能据此认定已获得真实视觉能力。 例如识别杯子颜色时，语言专家让句子通顺，视觉专家提高画面所支持颜色的概率；这个例子解释分工，不代表实际识别成绩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-lego-opd-93f05fa7" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:maestro-opd" data-paper-title="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation LLM 后训练 Nanyang Technological University 2026-09-29 MAESTRO 用教师 top-k 覆盖度和 Bhattacharyya 相似度构造逐 token Policy Disagreement Score，并对靠近响应起点的位置加权；教师只在高分歧位置介入，减少整段 teacher rollout 的固定开销。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  On-policy distillation 教师介入 策略分歧 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MAESTRO为什么把top-k覆盖与Bhattacharyya相似度同时用于教师介入判断？ 覆盖衡量学生候选是否包含教师支持，归一化相似度再看共同支持中的质量分配，两者不能相互替代。分歧分数与靠前位置权重帮助集中有限教师介入预算。分歧高只是需要关注的线索，不保证教师一定正确，本地PDS算子也没有生成完整教师rollout。 教学例子：两模型top-k词完全相同，却给这些词很不一样的概率；只看候选是否重叠，会误判它们没有重要分歧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-maestro-opd-551f210d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pr-opd" data-paper-title="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning LLM 后训练 University of Florida 2026-09-29 GRPO warm start 后，策略为每条已完成轨迹写一条 hindsight skill，并对同一 response 做普通 context 与 skill context 两次 forward。后者是 stop-gradient teacher；PR-OPD 在每层、每个 response token 对齐投影 hidden state，再与 reward objective 组合。推理时 skill 和 teacher 分支都移除。 复现级别：L1 表征对齐目标。复现级别：L1 表征对齐目标。实现多层、多 response-token 的 stop-gradient privileged alignment。测试覆盖相同表征时零损失、不同表征时正损失、mask 与 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 ALFWorld/WebShop 或 GRPO warm start，不能宣称论文最高 +14.0 点结果。  Agentic RL On-policy distillation 表征对齐 LLM 后训练 教师与纠错：额外信息何时能帮到学生 PR-OPD为什么对同一response做普通与hindsight skill两次forward，而不是直接模仿技能文本？ skill是完成轨迹后得到的训练专属视图，目标是比较它怎样改变同一响应各层各token表示，再蒸馏到无skill学生。若改成复制技能文本或另一条教师答案，就换了监督对象。教师分支停止梯度，并与任务奖励结合，推理时移除skill和教师。 教学例子：失败复盘总结“先验证工具返回格式”，可以让教师借此重新解释旧决策；学生训练后应在没有这条提示时自己做出判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-pr-opd-9c73d4f9" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weakest-link" data-paper-title="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning LLM 后训练 Huawei Noah’s Ark Lab 2026-09-29 把教师对学生采样 token 的负对数概率当作成本，约束每个生成前缀的平均成本。一旦某个前缀越界，后续进入吸收惩罚状态，防止“先生成坏推理、再靠容易 token 拉低平均成本”；同时把即时奖励的全词表期望精确求导，降低只采样当前动作的方差。 L1 可微目标与优化诊断。L1 可微目标与优化诊断。真实执行全词表即时奖励梯度和未来 Monte Carlo 回报，不等于已蒸馏完整推理模型。API 输入一条无 padding 的 on-policy 轨迹，以及每个访问前缀的全词表教师 log-prob 和任务奖励。调用方负责真实教师/学生 rollout、变长批处理、基准和同预算对照；本次未接入完整 LLM 训练。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 对三动作学生策略训练 80 步 Adam，三个随机初始 seed；教师分布固定公开为 [0.7,0.29,0.01]，预算 2，惩罚 4。  教师前缀约束蒸馏 约束强化学习 LLM 后训练 教师与纠错：额外信息何时能帮到学生 The Weakest Link为什么前缀一旦违约就持续惩罚，不能靠后面的容易token把平均成本拉回来？ 每个前缀都需满足教师成本约束，最终平均合格可能掩盖早期严重偏离。吸收惩罚阻止事后稀释，让关键链条受局部约束。反事实即时奖励只枚举真实访问前缀的当前动作，不能为每个候选编造不同历史；教师低概率仍不自动等于事实错误。 教学例子：先写一段极不受教师支持的错误推导，再追加很多常见词，可能降低整句平均成本；前缀约束不允许这样补票。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-weakest-link-b901a370" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mas-opd" data-paper-title="MAS-OPD: On-Policy Distillation for Multi-Agent Systems" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MAS-OPD: On-Policy Distillation for Multi-Agent Systems LLM 后训练 University of Science and Technology of China 2026-09-28 以目标角色与非目标角色 teacher 信号差构造 role advantage，并把协作冲突归因只提供给 teacher 形成 privileged coordination supervision。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  多 Agent On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 MAS-OPD为什么把角色冲突归因放进教师视图，而不是直接改所有角色的奖励？ 多角色协作失败时，整体奖励难以说明哪个角色应改变行为。教师借助额外冲突信息形成角色相关的优势信号，让目标角色与其他角色的贡献有所区分。额外归因属于训练期信息，本地只验证角色优势和掩码，不能当作多模型协作能力复现。 例如规划者路线合理但执行者选错工具，教师可把冲突归到执行动作；不能因为团队失败就同样惩罚规划和执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-mas-opd-e3c3be86" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:olive" data-paper-title="Learning from Teacher Continuations at Student States" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Teacher Continuations at Student States LLM 后训练 University of Illinois Urbana-Champaign 2026-09-28 由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  在线蒸馏 Teacher continuation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OLIVE的学生前缀参与条件输入，为什么不一起计入监督损失？ 学生先生成前缀，教师从这个真实学生状态继续，监督只落在教师续写的词元上。这样既保留学生容易遇到的偏离状态，又不把学生自己写错的前缀当作正确标签。教师续写质量仍是前提，掩码正确也不能替代完整语言模型实验。 例如学生把计算写到一个可修复的中间步骤，教师接着纠正并完成；训练读取整段上下文，但只学习教师接续的部分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-olive-4870752f" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opd-aha" data-paper-title="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation LLM 后训练 Arizona State University / University of Virginia / Stevens Institute of Technology 2026-09-15 用真实视觉与空视觉教师分布之差重建视觉偏好目标，抑制错误语言前缀的惯性。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行目标重建公式；未加载多模态 checkpoint。本地执行目标重建公式；未加载多模态 checkpoint。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多模态后训练 On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPD-Aha为何比较真实视觉输入与空视觉输入的教师分布？ 错误前缀可能让教师继续顺着语言惯性推理。把真实画面与空视觉条件下的输出对比，可以提取画面带来的偏好变化，再用它构造蒸馏目标。这个差异帮助区分视觉证据与语言先验，但不保证视觉教师本身正确；本地只是目标构造诊断。 例如前文误说图里是狗，教师在看到猫图与看不到图时的概率变化可突出猫的证据，而不是只复制带错前缀的整段回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-opd-aha-11a1ffc3" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:nsd" data-paper-title="Negative Self-Distillation: Learning to Reason by Avoiding Flaws" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Negative Self-Distillation: Learning to Reason by Avoiding Flaws LLM 后训练 University of Virginia 2026-09-10 让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  负向自蒸馏 推理后训练 LLM 后训练 教师与纠错：额外信息何时能帮到学生 NSD既然要远离错误推理，为什么不压低整条错误回答的所有词元？ 错误回答仍包含正常语法和可能正确的中间步骤，整段排斥会损伤通用表达。NSD用负向教师提供应远离的分布，并通过动态门控把更新集中到推理关键位置。门控只是定位机制，不能保证每个被选位置确实有错，本地也未训练完整语言模型。 例如算式中只有进位错误，句子里的连接词和正确数字不应全部被压低；教学例子关注选择性纠错，不声称测得收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-nsd-9169c0f1" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:compass-opd" data-paper-title="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts LLM 后训练 Institute of Information Engineering, Chinese Academy of Sciences 2026-09-09 异构教师与学生的绝对概率刻度不可直接比较。CompassOPD 用教师相对其 reference 的后训练变化作“指南针”，并在模型族内中心化，保留方向而消除不同模型族的整体偏置。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现去除 family offset 的教师方向，不冒充跨 tokenizer 的完整 LLM 训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。当前候选共享同一有限动作空间，未复刻跨 tokenizer 映射和全参数训练，因此属于 L1 机制诊断。  跨模型族 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 CompassOPD为什么比较教师相对自身参考模型的变化，而不直接比较师生概率？ 不同模型家族的概率尖锐程度和校准不同，直接对齐绝对概率会混入尺度差异。方法先看教师后训练相对其参考模型的似然变化，再作家族内中心化，提取方向性信号，并保留学生参考锚点。相对变化仍可能带有教师偏差，不自动等于正确答案。 例如两个教师都更偏好正确步骤，但一个本来输出更尖锐；比较各自训练前后的变化，比把两者概率大小直接排序更合理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-compass-opd-6b3a07da" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oprd" data-paper-title="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation LLM 后训练 KAIST AI 2026-09-08 OPRD 不直接模仿弱教师答案，而是先测量弱教师经过后训练后的 logit 变化方向，再沿这个方向增强强模型的可验证奖励梯度；核心假设是“学习方向”比弱模型最终能力更容易迁移。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现论文的反向蒸馏方向提取与验证器梯度投影，不把小型分类策略的结果等同于完整 LLM 后训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。本地仅验证方向提取和的可执行性；候选集合来自带标签的诊断任务，故 diagnostic_only=true、不可晋升为能力证据。  弱到强反向蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPRD为什么能借弱模型的变化方向，而不要求强模型模仿弱模型答案？ 方法从弱后训练模型与其基座的差异提取中心化、归一化方向，再增强强模型验证器梯度在该方向上的分量。迁移对象是更新方向，不是弱模型的最终回答。只有方向与强模型当前任务有用地对齐才可能帮助；本地候选方向诊断不证明通用弱到强提升。 例如弱模型训练后更重视检查单位，强模型可增强相关梯度分量，却不必抄它可能算错的最终数值；方向有用仍需验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-oprd-e69b9862" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:uc-mopd" data-paper-title="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD LLM 后训练 Peking University 2026-08-27 普通 MOPD 很少采到强正优势 token，也无法判断更新方向是否可靠。方法扩大温度覆盖，按轨迹正优势密度挑样本，再用熵校准 CLL 概率门控 token 更新。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现双温采样、正优势密度筛选和 centered log-likelihood 门控。未加载通用/垂域教师 checkpoint；本地结果仅证明筛选与随机门控控制流。arithmetic-smoke 本轮 accuracy 0.1953 → 0.1953。零提升被如实保留：机制运行正常，但单教师候选套件不能证明论文多教师收益。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 UC-MOPD的温度扩展、轨迹筛选和词元门控分别解决什么问题？ 温度扩展先增加候选覆盖，正优势词元密度用于挑选更有学习价值的轨迹，熵校准的概率门控再控制具体词元更新。三个步骤作用在不同层次，不能把候选更多直接等同于监督更准；置信度也不是真值，本地未加载完整的通用与领域教师。 例如先采到几条不同解法，再选有效步骤较密的一条，最后只加强可靠的关键词元；不能把整条高置信回答无条件当标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-uc-mopd-4afbd03c" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:video-opsd" data-paper-title="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models LLM 后训练 Nanyang Technological University 2026-08-27 学生读取完整视频，训练期自教师只读取人工标注的证据帧；再按 token 对证据的依赖度加权蒸馏。论文称效果接近 GRPO，而训练时间减少约 60%。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现证据视图自教师与 evidence-guided token 权重。公开 smoke 数据没有视频帧，使用独立奖励轴模拟“证据依赖”；未训练 Video-LLM，不把概念验证写成论文指标复刻。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.6562，记录 evidence token weight 与 teacher gap。指标见 metrics/arithmetic-smoke-seed42.json。  证据帧特权自蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Video-OPSD的证据帧为什么只给训练教师，而学生仍要读取完整视频？ 教师在人工标注的证据帧上形成较聚焦的监督，再按词元对证据的依赖加权蒸馏。学生保留完整视频输入，学习在干扰中利用相关内容；若把证据定位也直接给学生，就改变了推理条件。本地无视频烟雾测试只是奖励轴代理，不能作为视觉能力证据。 例如问题问谁先拿起杯子，教师只看相关片段，学生仍看整段活动视频；教学目标是学会找证据，不是假定已知片段位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-video-opsd-2da91d84" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:weak-guide-rlvr" data-paper-title="Boosting LLM Exploration via Weak-Model Guidance in RLVR" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Boosting LLM Exploration via Weak-Model Guidance in RLVR LLM 后训练 Peking University 2026-08-27 RLVR 容易熵坍缩。论文用更小弱模型生成部分推理前缀，迫使目标模型进入陌生轨迹，再以 entropy 截断和原生/前缀样本混训保持覆盖率。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现跨模型前缀扰动、混合采样与 entropy 诊断。弱教师由冻结 reference 分布模拟；未声称完成双 checkpoint RLVR。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6797，并记录 guided entropy 与 prefix surprise。  弱模型前缀探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生 弱模型给出的推理前缀可能错误，Weak-Model Guidance为什么还要混入它？ 弱模型前缀把目标策略带到自身采样不常遇到的状态，提供额外探索起点；熵截断限制不稳定续写，并与原生轨迹混合以保留覆盖。前缀只是引导，不能充当正确标签，最终奖励仍需独立验证器。本地冻结参考代理没有替代真实双模型训练。 例如弱模型提出另一种分解问题的开头，强模型从此继续并接受答案检查；如果检查失败，不能因为有引导就把轨迹判为正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-weak-guide-rlvr-a37f47f8" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:clue-opsd" data-paper-title="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding LLM 后训练 University of Maryland, College Park 2026-08-26 学生仍看完整长视频，冻结教师在训练时只看问题相关 clue interval；学生自己的 rollout 上做 on-policy self-distillation，推理时不需要 clue、标签或外部教师。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.5938（+375.00%）；clue 用 process-reward proxy 代替。  长视频特权视图 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生 Clue-OPSD为什么要在学生自己的前缀上查询只看线索片段的教师？ 学生前缀决定训练时真正遇到的状态，线索片段则让教师聚焦与问题相关的证据；二者结合减少只在教师理想轨迹上学习的偏移。线索是训练期特权信息，推理时学生仍须处理完整视频，不应依赖片段标注、答案或教师。 例如学生已写出一个不完整的事件顺序，教师读取相关时间段后续写纠正；部署时不能把人工圈出的时间段继续作为输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-clue-opsd-7ed80773" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:smopd" data-paper-title="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation LLM 后训练 Alibaba / Qwen 2026-08-04 先用 reward-priority 分别训练专长教师，再在学生自身轨迹上合并多个教师能力。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 多奖励 RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 SMOPD为什么先训练不同奖励侧重的专家，再在学生状态上合并？ 不同奖励优先级可塑造具有不同专长的教师，随后让它们在学生实际到达的状态提供分布监督，以加权蒸馏吸收这些能力。它不等于先把奖励平均成一个教师，也不保证所有能力无损共存；权重与教师分歧仍需验证，本地只是候选模型实验。 例如一个教师擅长检查计算，另一个擅长格式约束，学生在自己的解题步骤上同时获得指导；并非直接把两套参数平均。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-smopd-2a4bef05" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rstg" data-paper-title="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance LLM 后训练 Tianjin University 2026-08-01 只对负向零方差 group 启用教师，并在高熵或大 teacher-student gap token 上蒸馏，同时注入教师正确轨迹 SFT。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD RLVR LLM 后训练 教师与纠错：额外信息何时能帮到学生 RSTG为什么只对全失败的零方差组求助教师，而不把所有同分组一视同仁？ 组内全失败时，奖励归一化缺少可区分信号，教师可提供纠正轨迹，并在高熵或师生差距大的词元上增加监督。全成功组同样可能零方差，却没有相同的纠错需求。触发条件必须区分正负结果，教师纠正也仍需要可靠性检查。 例如四条解法都算错时可请求教师示范；四条都答对时，不能仅因分数相同就当成失败组，再强行覆盖学生的不同解法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-rstg-e8f7dde4" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:crpo" data-paper-title="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation LLM 后训练 Authors did not disclose affiliation 2026-07-30 按预测熵区分反思探索正位置和 exposure-bias 负位置，对 privileged self-distillation 做组内对比。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD Agentic RL LLM 后训练 教师与纠错：额外信息何时能帮到学生 CRPO为什么把高不确定位置区分为反思探索与暴露偏差，而不统一奖励高熵？ 高熵可能表示有价值的探索，也可能是错误前缀导致的失控。CRPO结合组内对比和特权自蒸馏来区分这些情形，分别处理有益反思位置与偏差暴露位置。熵只描述不确定程度，不能单独判定对错；本地候选诊断不等于完整推理训练。 例如重新检查一个分支时的不确定与沿错误算式胡乱续写都可能高熵，更新方向应取决于后续可验证结果，而非熵值本身。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-crpo-a18535ff" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vad" data-paper-title="VAD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="VAD LLM 后训练 Shanghai Jiao Tong University 2026-07-30 多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。 未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。本页复现论文可隔离的 counterfactual target reconstruction；本地候选策略用过程证据轴模拟 evidence-present / evidence-removed 教师视图，不把它写成 4B/9B 多模态模型复现。候选答案的过程质量轴替代真实图像裁剪，验证的是 counterfactual target reconstruction 的数学路径；未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。  多模态证据归因蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生 VAD为什么把教师修正投影到视觉证据方向，而且只保留同向分量？ 有无视觉证据的教师对比给出视觉方向，原教师修正只保留沿该方向的正向投影，再以当前学生分布为锚构造目标。这样限制与视觉无关或反向的整体模仿；完整教师分布只作较弱约束。本地奖励轴代理并未复现真实视觉裁剪和模型训练。 例如教师既偏好某种措辞又看到红色物体，投影试图保留颜色证据相关的变化，而不把所有语言风格一起灌给学生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-vad-1b365cba" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:distilled-rl" data-paper-title="Distilled RL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distilled RL LLM 后训练 Nankai University 2026-07-19 传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现反向比率裁剪、负样本 reset 与序列几何归一化；教师不是无条件 KL target。  教师奖励重权重 LLM 后训练 教师与纠错：额外信息何时能帮到学生 Distilled RL为什么只给正优势样本加教师权重，负优势样本保持原权重？ 正优势样本已有任务奖励支持，教师比率可进一步强调其中值得模仿的词元；非正优势样本维持原权重，避免教师重加权干扰其惩罚含义。比率经过裁剪和序列几何均值归一化，限制尺度及长度影响，但教师偏好仍不等于额外正确性证明。 例如一条答对的解法可提高关键步骤权重，一条失败解法仍按原负优势更新；不应因教师喜欢某些用词就削弱失败惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-distilled-rl-b41ef584" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:armor" data-paper-title="ARMOR" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="ARMOR LLM 后训练 University of Science and Technology of China 2026-07-11 单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。reference 是本地初始化候选策略，不包含论文规模的长程训练或真实轨迹池。每个训练组一半从当前策略采样、一半从冻结 reference 采样，分别记录 anchor 数、权重和最终策略指标。  Reference anchor LLM 后训练 教师与纠错：额外信息何时能帮到学生 ARMOR主动采样参考策略轨迹，与只在损失里加入KL惩罚有什么区别？ KL惩罚在当前采到的数据上限制策略漂移，却不保证参考策略的好解法仍出现在训练样本中。ARMOR主动混入冻结参考策略的锚点轨迹，恢复这部分数据覆盖。参考轨迹也可能差或已过时，混合比例需要控制；本地参考候选模型不能代表完整语言模型结论。 例如新策略只会用一种捷径，锚点采样能重新提供旧策略的检查路线；仅惩罚分布差异，不一定让这条路线实际进入批次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-armor-71dc1f8a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mopd" data-paper-title="MOPD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MOPD LLM 后训练 Xiaomi 2026-06-29 多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现四个奖励轴的 domain teacher、按样本域证据混合，并限制在 student rollout support。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生 MOPD为什么在学生轨迹上调用多个领域教师，而不直接拼接专家轨迹训练？ 学生自己的前缀暴露真实学习状态，多个领域教师在相同状态提供稠密指导，可减少专家轨迹与学生分布不一致的问题。合并发生在监督信号而非简单参数平均，领域之间仍可能干扰，不能因为有多个教师就推断能力全部保留。本地只是候选级验证。 例如学生在一道混合数学与代码的问题中写到中间步骤，两位教师围绕该状态指导；直接拼接各自完整答案未必覆盖这个状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-mopd-f0fd48c7" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:polaris-hri" data-paper-title="POLARIS: Guiding Small Models to Write Long Stories" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="POLARIS: Guiding Small Models to Write Long Stories LLM 后训练 University of Maryland 2026-06-02 核固定v2 Section3.2 Eq5和作者fixed verl core：policy-only mean/sample-std，Aref=0.4 min(1,t/15)(rref−μ)/(σ+1e-6)，step0为0；K5+1，clip0.2、KL关闭，token-mean。相同external rubric给policy和ref评分。按adv符号在log-ratio域选精确clipped分支，避免exp溢出的伪有限forward/NaN backward，不改原目标。 成本过高，不复现（审查 DONE）。Qwen3.5-9B、1388 copyrighted prompt-story pairs、4×A10080GB FSDP、batch8、160steps，每run原文约48h并约60美元judge API。完整实验明确超单卡短时预算；人类故事不公开，不能用自造故事冒充原训练数据。hri_advantages仅处理外部真实reward，hri_grpo_loss处理current/old teacher-forced logp与response mask。未实现Story Quality judge、版权故事、thinking trace生成或完整写作RL训练；  RLVR与偏好优化 GRPO与参考轨迹注入 LLM 后训练 教师与纠错：额外信息何时能帮到学生 POLARIS HRI为什么用策略样本计算均值方差，并让参考答案优势逐步加入？ 参考故事是额外锚点，若纳入策略组的均值方差，会同时改变所有策略样本的优势尺度。方法只用策略奖励计算统计量，再逐步放大参考样本的相对优势，起始步权重为零。参考与策略使用同一评价准则；本地组件验证不代表完整故事训练已复现。 例如五条策略故事决定组内基线，第六条参考故事只据此计算自己的优势；不能先把参考混入均值，再声称只增加一条监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-polaris-hri-c07af119" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcd" data-paper-title="OPCD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPCD LLM 后训练 Microsoft Research 2026-02-12 提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。论文覆盖经验知识蒸馏和系统提示蒸馏，并支持跨模型尺寸教师。 保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；当前为候选策略机制复现，不等同于 Qwen3/VeRL 原始训练。本地“经验上下文”是已验证答案形成的可审计条件分布，不包含真实长 system prompt；未复跑 FrozenLake、Sokoban 或医疗/安全任务，因此不能将本地准确率与论文横向比较。稳定指标见 omitted-agentic-rl-opd-seed42.json。  Context distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPCD为什么让无经验上下文的学生生成，再让带上下文的教师评分？ 目标是把外部经验内化到参数，而不是训练学生继续依赖那段经验。学生只读任务并生成轨迹，教师读取经验后在同一学生前缀给出分布，以学生到教师方向的逆KL更新。上下文知识是否可靠仍很关键，本地条件分布诊断没有覆盖真实长系统提示。 例如训练教师可读一条操作经验，学生只能读当前任务；学习后清空上下文再作答，才能检验经验是否进入了参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-opcd-d21234a6" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opsd" data-paper-title="OPSD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPSD LLM 后训练 University of California, Los Angeles 2026-01-26 普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。轨迹由学生生成，教师只在学生实际到达的前缀上提供全词表监督；逐 token pointwise divergence clipping 防止风格 token 主导训练。 保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；当前为候选策略机制复现，不是 Qwen3 参数级训练。本地特权教师由当前策略与已验证候选答案共同构造，真实更新候选策略参数；未训练 Qwen3，也未复跑竞赛数学数据。该结果只验证双视图数据流、散度与裁剪机制。稳定指标见 omitted-agentic-rl-opd-seed42.json。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生 OPSD的教师能看验证解，为什么学生生成轨迹时必须看不到它？ 同一模型的两个条件视图承担不同角色：教师借验证解提供更强监督，学生仍按部署条件只看问题。教师沿学生实际前缀评分，逐词元散度裁剪避免少数风格位置主导。若学生生成时也读答案，就绕过了待学习能力；本地仅验证双视图和更新机制。 例如教师知道一道题的标准解，可以评价学生写到一半的步骤；学生采样时不能把标准解放在提示中再声称独立解题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<span id="paper-post-training-opsd-096ec0f1" class="ar-learning-paper-anchor"></span>
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
