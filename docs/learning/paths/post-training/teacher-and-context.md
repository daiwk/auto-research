---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 教师与纠错：额外信息何时能帮到学生

[LLM 后训练](index.md) / 子主题导学 · 约 3 分钟 · 47 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 47 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="When to Follow the Teacher: Advantage-Based On-Policy Distillation LLM 后训练 University of Pennsylvania 2026-10-22 普通 OPD 在学生实际访问的状态上模仿教师，但教师偏好的动作不一定能被当前学生继续完成。AOPD 用该动作对学生最终奖励的优势加权教师监督，通过学生原有 rollout、终局奖励及教师重要性比率估计，不额外生成反事实续写。 完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。oracle 仅存在测试代码，不进入损失或诊断策略。本地状态：L1 精确损失组件，diagnostic only。实现论文 Eq. 3.6 / 3.8 与 Algorithm 1 的 leave-one-out baseline，不是完整 LLM 训练器或能力复现。完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。leave_one_out_advantages 按 prompt group 独立计算 baseline；  On-policy distillation 优势加权蒸馏与无额外rollout估计 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-aopd-187dc1ba">When to Follow the Teacher: Advantage-Based On-Policy Distillation</h2>
<p class="ar-learning-card__meta">University of Pennsylvania · 论文公开：2026-10-22</p>
<p><strong>方法要点：</strong>普通 OPD 在学生实际访问的状态上模仿教师，但教师偏好的动作不一定能被当前学生继续完成。AOPD 用该动作对学生最终奖励的优势加权教师监督，通过学生原有 rollout、终局奖励及教师重要性比率估计，不额外生成反事实续写。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。oracle 仅存在测试代码，不进入损失或诊断策略。本地状态：L1 精确损失组件，diagnostic only。实现论文 Eq. 3.6 / 3.8 与 Algorithm 1 的 leave-one-out baseline，不是完整 LLM 训练器或能力复现。完整实验：成本过高，不复现（审查 DONE），不进入自动重试队列。leave_one_out_advantages 按 prompt group 独立计算 baseline；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31563v1">原论文</a> · <a href="../../../../post-training/2610.31563-aopd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning LLM 后训练 Meta Superintelligence Labs 2026-10-21 ME-OPD 用训练专属描述与参考解法，让教师为错误的学生回答打分，只纠正教师不支持的 token；正确回答只走任务奖励，避免整段模仿。它针对小型视觉语言模型误读斜边、标签或几何关系的问题，保留原回答中无需修改的推导与措辞。ME-OPD 让教师在训练时看到图形描述、已验证参考解法和学生的完整原回答，要求“用最少编辑修正”。教师不生成新答案，而是 teacher-force 同一学生回答的第二次出现，为原 token 打分。最终答案验证正确的 rollout 只走任务 GRPO； 完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。多个 seed 仍是 L1 机制诊断，不构成能力比较。本地状态：L1 精确路由 / 纠错目标组件，diagnostic only，不是 VLM 能力复现。完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。GRPO 的未公开实现细节不冒充论文原配置。freeze_rollouts 接收外部 verifier 的二元奖励和外部全组优势，复制并冻结旧学生 / 教师概率、mask 与路由。它不判断自然语言答案正确性，不生成图形描述，不校验参考解法是否真的通过验证器。  On-policy distillation 多模态最小编辑纠错 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-minimal-edit-opd-97f1b5ed">Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning</h2>
<p class="ar-learning-card__meta">Meta Superintelligence Labs · 论文公开：2026-10-21</p>
<p><strong>方法要点：</strong>ME-OPD 用训练专属描述与参考解法，让教师为错误的学生回答打分，只纠正教师不支持的 token；正确回答只走任务奖励，避免整段模仿。它针对小型视觉语言模型误读斜边、标签或几何关系的问题，保留原回答中无需修改的推导与措辞。ME-OPD 让教师在训练时看到图形描述、已验证参考解法和学生的完整原回答，要求“用最少编辑修正”。教师不生成新答案，而是 teacher-force 同一学生回答的第二次出现，为原 token 打分。最终答案验证正确的 rollout 只走任务 GRPO；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。多个 seed 仍是 L1 机制诊断，不构成能力比较。本地状态：L1 精确路由 / 纠错目标组件，diagnostic only，不是 VLM 能力复现。完整多模态训练：成本过高，不复现（审查 DONE），不自动重试。GRPO 的未公开实现细节不冒充论文原配置。freeze_rollouts 接收外部 verifier 的二元奖励和外部全组优势，复制并冻结旧学生 / 教师概率、mask 与路由。它不判断自然语言答案正确性，不生成图形描述，不校验参考解法是否真的通过验证器。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30231v1">原论文</a> · <a href="../../../../post-training/2610.30231-minimal-edit-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer LLM 后训练 NVIDIA 2026-10-20 师生词表大小、token ID 与分词边界不一致，不能直接逐坐标 KL。CSD 先按原文字符区间对齐 chunk，再通过解码文本等价构造共同事件。1:1 采用共同 token；1:N 或 M:1 固定观察到的 chunk 前缀，只枚举末 token 的等价续写；M:N 默认只保留实际观察序列。未显式匹配的质量进入 REST，而不是被丢弃或重新归一化。 完整实验成本过高，不复现（审查 DONE）。微型诊断使用两套不同大小的词表与不同分词，覆盖四种 chunk 形状。L1 跨 Tokenizer 对齐与损失组件，不是大模型能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。v1 提交在 10 月 20 日截止时间之后，本轮归 2026-10-22 首次公告，不改写其真实提交日期。align_offsets 对原文字符 span 做最小公共边界对齐并核对整体 decode；paired_completions 在固定前缀下按文本建映射，不按相同 ID、概率排名或给定相似分配对；  知识蒸馏 跨Tokenizer共同事件分布 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-csd-2e95adef">CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer</h2>
<p class="ar-learning-card__meta">NVIDIA · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>师生词表大小、token ID 与分词边界不一致，不能直接逐坐标 KL。CSD 先按原文字符区间对齐 chunk，再通过解码文本等价构造共同事件。1:1 采用共同 token；1:N 或 M:1 固定观察到的 chunk 前缀，只枚举末 token 的等价续写；M:N 默认只保留实际观察序列。未显式匹配的质量进入 REST，而不是被丢弃或重新归一化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。微型诊断使用两套不同大小的词表与不同分词，覆盖四种 chunk 形状。L1 跨 Tokenizer 对齐与损失组件，不是大模型能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。v1 提交在 10 月 20 日截止时间之后，本轮归 2026-10-22 首次公告，不改写其真实提交日期。align_offsets 对原文字符 span 做最小公共边界对齐并核对整体 decode；paired_completions 在固定前缀下按文本建映射，不按相同 ID、概率排名或给定相似分配对；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28895v1">原论文</a> · <a href="../../../../post-training/2610.28895-csd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization LLM 后训练 Korea University 2026-10-19 反馈条件自教师可能破坏正确rollout里学生已经成功的偏好，却又对错误rollout纠正不足。APSD依据正确性调整蒸馏target：正确时在学生和自教师之间插值，错误时越过自教师外推。关键不只是换一个target数值，还要保留target对学生分布的依赖；整个target一起detach会丢掉定义性的耦合梯度。原文§4及附录B 原图建议：Figure 3方法总览，保留右侧梯度几何与target分支；Figure 1是插值／外推的概念图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，学生实际采样回答。每次更新从同一当前学生复制自教师，教师只在额外的合成训练反馈条件下重放学生回答并停止梯度；不是单独初始化的外部教师。actor的采样条件只有公开prompt，不读取反馈、正确性或gold。反馈ID不代表自然语言执行错误或真实成功解答。  On-policy distillation 自蒸馏与训练稳定性 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-apsd-7a5d9aba">Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization</h2>
<p class="ar-learning-card__meta">Korea University · 论文公开：2026-10-19</p>
<p><strong>方法要点：</strong>反馈条件自教师可能破坏正确rollout里学生已经成功的偏好，却又对错误rollout纠正不足。APSD依据正确性调整蒸馏target：正确时在学生和自教师之间插值，错误时越过自教师外推。关键不只是换一个target数值，还要保留target对学生分布的依赖；整个target一起detach会丢掉定义性的耦合梯度。原文§4及附录B 原图建议：Figure 3方法总览，保留右侧梯度几何与target分支；Figure 1是插值／外推的概念图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。L1 定义性组件／梯度诊断，不是科学推理、工具或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，学生实际采样回答。每次更新从同一当前学生复制自教师，教师只在额外的合成训练反馈条件下重放学生回答并停止梯度；不是单独初始化的外部教师。actor的采样条件只有公开prompt，不读取反馈、正确性或gold。反馈ID不代表自然语言执行错误或真实成功解答。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25973v1">原论文</a> · <a href="../../../../post-training/2610.25973-apsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Reinforcement Learning with Visually Attributable On-Policy Self-Distillation LLM 后训练 Baidu Inc. 2026-10-19 特权图像裁剪带来的 teacher 修正，可能混有语言先验或风格变化。VAG 让同一 EMA 教师对证据保留裁剪和随机遮挡裁剪重放相同学生前缀，只接纳与视觉对比方向一致的修正，再以有界项调制 verifier 的组归一化 advantage。纯文本教师或固定 logits 门控不能冒充该多模态链路。 仅资料收录，成本过高，不复现（审查 DONE）。仅资料收录，成本过高，不复现（审查 DONE）。没有本地可执行 adapter、评测接口或机制验证；不接入 Evolve，不作为能力证据，不进入自动重试队列。完整实验不复现，审查 DONE。原文 §4.1：Qwen3.5-4B/9B 全参数训练一 epoch，batch 48，每题条响应，最大 1,024 token，8×NVIDIA H800。需要训练数据的目标细节裁剪、EMA 双视图重放和六基准 judge 协议。单 A100/A30 或 Mac 不承担原矩阵，属于配置直接支持的高成本判断，无需下载权重或试跑。  On-policy distillation 多模态RLVR与视觉归因 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-visually-attributable-opd-08abcb9d">Reinforcement Learning with Visually Attributable On-Policy Self-Distillation</h2>
<p class="ar-learning-card__meta">Baidu Inc. · 论文公开：2026-10-19</p>
<p><strong>方法要点：</strong>特权图像裁剪带来的 teacher 修正，可能混有语言先验或风格变化。VAG 让同一 EMA 教师对证据保留裁剪和随机遮挡裁剪重放相同学生前缀，只接纳与视觉对比方向一致的修正，再以有界项调制 verifier 的组归一化 advantage。纯文本教师或固定 logits 门控不能冒充该多模态链路。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>仅资料收录，成本过高，不复现（审查 DONE）。仅资料收录，成本过高，不复现（审查 DONE）。没有本地可执行 adapter、评测接口或机制验证；不接入 Evolve，不作为能力证据，不进入自动重试队列。完整实验不复现，审查 DONE。原文 §4.1：Qwen3.5-4B/9B 全参数训练一 epoch，batch 48，每题条响应，最大 1,024 token，8×NVIDIA H800。需要训练数据的目标细节裁剪、EMA 双视图重放和六基准 judge 协议。单 A100/A30 或 Mac 不承担原矩阵，属于配置直接支持的高成本判断，无需下载权重或试跑。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26856v1">原论文</a> · <a href="../../../../post-training/2610.26856-vag/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation LLM 后训练 University of Southern California 2026-10-18 多轮Agent蒸馏中，学生可能先超过教师，再随着持续模仿而退步。作者区分两个过程：教师修复学生的弱决策，同时也会侵蚀学生已经成功、但与教师偏好不同的行为。SPOD只在成功训练episode内保护教师整action概率更低的decision，取消该处蒸馏压力，并用软概率floor抵消来自其他状态更新的间接侵蚀；其余decision继续正常蒸馏。原文§3–4 原图建议：附录Figure 9的训练流程；Figure 1展示overshoot与修复／侵蚀现象，可作为辅助结果图。原图不是本地运行结果。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是Agent能力复现。L1 定义性组件／梯度诊断，不是Agent能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，实际采样多state episode；教师独立随机初始化后冻结，对同一学生action重放评分。显式合成环境在episode结束后返回训练成功位，actor输入只有公开历史、自己的action及公开观察ID；不读取成功位、gold或评估结果。固定长度预算的合成action不是ALFWorld/WebShop/ScienceWorld语言动作。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-spod-93843af2">Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation</h2>
<p class="ar-learning-card__meta">University of Southern California · 论文公开：2026-10-18</p>
<p><strong>方法要点：</strong>多轮Agent蒸馏中，学生可能先超过教师，再随着持续模仿而退步。作者区分两个过程：教师修复学生的弱决策，同时也会侵蚀学生已经成功、但与教师偏好不同的行为。SPOD只在成功训练episode内保护教师整action概率更低的decision，取消该处蒸馏压力，并用软概率floor抵消来自其他状态更新的间接侵蚀；其余decision继续正常蒸馏。原文§3–4 原图建议：附录Figure 9的训练流程；Figure 1展示overshoot与修复／侵蚀现象，可作为辅助结果图。原图不是本地运行结果。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是Agent能力复现。L1 定义性组件／梯度诊断，不是Agent能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维因果GRU，实际采样多state episode；教师独立随机初始化后冻结，对同一学生action重放评分。显式合成环境在episode结束后返回训练成功位，actor输入只有公开历史、自己的action及公开观察ID；不读取成功位、gold或评估结果。固定长度预算的合成action不是ALFWorld/WebShop/ScienceWorld语言动作。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25034v1">原论文</a> · <a href="../../../../post-training/2610.25034-spod/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation LLM 后训练 Alibaba Group 2026-10-16 层级团队的最终答案能监督Leader，却难以判断Searcher的检索、总结是否真正有效。MultiAgent-OPD先在较简单的Searcher–Answerer流程训练教师，再从相同的基础checkpoint重新开始训练共享参数的Leader–Searcher–Answerer团队。冻结教师为学生实际搜索轨迹提供局部OPD反馈；Leader根据团队结果、Answerer根据自己的候选正确性学习。原文 §3 原图建议：Figure 1 层级工作流；如只保留一张，应同时可读出阶段一教师和阶段二角色分工。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。不用固定工作流、随机教师或单个蒸馏算子冒充端到端多Agent系统；未接 Evolve。成本过高，不复现（审查 DONE）。基础模型Qwen3-4B-Instruct-2507，两阶段使用79,168条NQ和90,447条HotpotQA，batch32题×5轨迹、每次多个PPO更新，层级流程包含多波委派、最多12环境步及每请求5个回答候选；还需真实搜索服务。评测是七个数据集合计固定5,000题，每个方法每题四次独立工作流，不是每数据集5,000题。原文当前配置未明确完整GPU数，不臆造显卡数量或训练时长。  Agentic RL On-policy distillation 多Agent协作 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-multiagent-opd-b3177be0">MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Alibaba Group · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>层级团队的最终答案能监督Leader，却难以判断Searcher的检索、总结是否真正有效。MultiAgent-OPD先在较简单的Searcher–Answerer流程训练教师，再从相同的基础checkpoint重新开始训练共享参数的Leader–Searcher–Answerer团队。冻结教师为学生实际搜索轨迹提供局部OPD反馈；Leader根据团队结果、Answerer根据自己的候选正确性学习。原文 §3 原图建议：Figure 1 层级工作流；如只保留一张，应同时可读出阶段一教师和阶段二角色分工。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。不用固定工作流、随机教师或单个蒸馏算子冒充端到端多Agent系统；未接 Evolve。成本过高，不复现（审查 DONE）。基础模型Qwen3-4B-Instruct-2507，两阶段使用79,168条NQ和90,447条HotpotQA，batch32题×5轨迹、每次多个PPO更新，层级流程包含多波委派、最多12环境步及每请求5个回答候选；还需真实搜索服务。评测是七个数据集合计固定5,000题，每个方法每题四次独立工作流，不是每数据集5,000题。原文当前配置未明确完整GPU数，不臆造显卡数量或训练时长。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23234v1">原论文</a> · <a href="../../../../post-training/2610.23234-multiagent-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning LLM 后训练 Tsinghua University 2026-10-16 长轨迹仅有终局奖励时，同一轨迹的好坏动作容易一起获奖或受罚；同一批轨迹又会经历多次更新，旧信用不能告诉优化器何时停止。TreeOPSD 将续写分支整理成共享前缀树，把叶奖励按行为策略似然向上回传，再把每个 turn 的信用映射为一个冻结且有界的 Bernoulli 教师。学生相对旧策略的变化达到目标时梯度消失，超过目标则反向，不再只有无限推进的方向。原文 §2–3 原图建议：Figure 2 方法总览，展示树信用、冻结后验教师与多次更新；Figure 1 是概念插图，不宜代替算法图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维 GRU 因果策略，实际采样三 turn 轨迹并从中间前缀继续采样；每个 turn 两个 actor token，非终局附带一个公开观察 ID。显式合成终局奖励由末 turn 的 token 计算，不传入 actor；它不是自然语言搜索 verifier。树合并保留完整历史、观察和终止标记，重复叶仍保留在和奖励统计中。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-treeopsd-8a101275">Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>长轨迹仅有终局奖励时，同一轨迹的好坏动作容易一起获奖或受罚；同一批轨迹又会经历多次更新，旧信用不能告诉优化器何时停止。TreeOPSD 将续写分支整理成共享前缀树，把叶奖励按行为策略似然向上回传，再把每个 turn 的信用映射为一个冻结且有界的 Bernoulli 教师。学生相对旧策略的变化达到目标时梯度消失，超过目标则反向，不再只有无限推进的方向。原文 §2–3 原图建议：Figure 2 方法总览，展示树信用、冻结后验教师与多次更新；Figure 1 是概念插图，不宜代替算法图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维 GRU 因果策略，实际采样三 turn 轨迹并从中间前缀继续采样；每个 turn 两个 actor token，非终局附带一个公开观察 ID。显式合成终局奖励由末 turn 的 token 计算，不传入 actor；它不是自然语言搜索 verifier。树合并保留完整历史、观察和终止标记，重复叶仍保留在和奖励统计中。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23181v1">原论文</a> · <a href="../../../../post-training/2610.23181-treeopsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models LLM 后训练 The Chinese University of Hong Kong, Shenzhen 2026-10-15 教师可能跟随学生错误 reasoning prefix，而忽略题目条件。CCE 在完全相同的学生 response prefix上，让同一冻结教师分别读取完整题目与遮蔽一个有效前提的题目，以 clipped log-prob contrast 调整辅助 target。学生始终从完整题目生成；未通过 condition eligibility 或 entropy gate 的位置仍保留原 sampled PPO-OPD。 完整实验成本过高，不复现（审查 DONE）。L1 双视图 / union / auxiliary-KL / sampled PPO 组件。只接受已审阅的合法 condition span，不提供伪造的语义抽取器。完整实验成本过高，不复现（审查 DONE）。公开 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784，train/validation/test 原始 byte 区间 80%/10%/10% 分离。微型教师只作公开文本 next-token 训练，并非数学教师。  On-policy distillation 后训练算法组件 CCE-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-cce-opd-2c59e40e">Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models</h2>
<p class="ar-learning-card__meta">The Chinese University of Hong Kong, Shenzhen · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>教师可能跟随学生错误 reasoning prefix，而忽略题目条件。CCE 在完全相同的学生 response prefix上，让同一冻结教师分别读取完整题目与遮蔽一个有效前提的题目，以 clipped log-prob contrast 调整辅助 target。学生始终从完整题目生成；未通过 condition eligibility 或 entropy gate 的位置仍保留原 sampled PPO-OPD。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。L1 双视图 / union / auxiliary-KL / sampled PPO 组件。只接受已审阅的合法 condition span，不提供伪造的语义抽取器。完整实验成本过高，不复现（审查 DONE）。公开 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784，train/validation/test 原始 byte 区间 80%/10%/10% 分离。微型教师只作公开文本 next-token 训练，并非数学教师。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21195v1">原论文</a> · <a href="../../../../post-training/2610.21195-cce-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search LLM 后训练 The Ohio State University 2026-10-15 单纯提高正确率的 RL 可能压缩正确解法的覆盖范围。EliteReplay 先用冻结基模和 MAP-Elites 收集不同正确策略，训练时持续回放固定档案。档案按问题、approach 与结构特征分 cell，每格只保留最短已验证解；不是把 IID 样本放进普通 replay buffer。 完整实验成本过高，不复现（审查 DONE）。L1 MAP-Elites / archive / sampler / mixed loss 组件。本地保留真实目标导向搜索，但算术 grammar 不是论文的 SQL LLM，审阅 approach 列表不是 LLM labeler；不以微型结果宣称 BIRD/Spider 能力。完整实验成本过高，不复现（审查 DONE）。runner 提供三个固定整数加法任务，候选为四种可解析表达式。一个小型冻结线性策略在原任务、目标 approach、parent 是否存在的条件下实际采样候选；AST whitelist 计算表达式结果进行验证，不执行任意生成程序。  Reference anchor 后训练算法组件 EliteReplay LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-elite-replay-bbf50043">EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search</h2>
<p class="ar-learning-card__meta">The Ohio State University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>单纯提高正确率的 RL 可能压缩正确解法的覆盖范围。EliteReplay 先用冻结基模和 MAP-Elites 收集不同正确策略，训练时持续回放固定档案。档案按问题、approach 与结构特征分 cell，每格只保留最短已验证解；不是把 IID 样本放进普通 replay buffer。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。L1 MAP-Elites / archive / sampler / mixed loss 组件。本地保留真实目标导向搜索，但算术 grammar 不是论文的 SQL LLM，审阅 approach 列表不是 LLM labeler；不以微型结果宣称 BIRD/Spider 能力。完整实验成本过高，不复现（审查 DONE）。runner 提供三个固定整数加法任务，候选为四种可解析表达式。一个小型冻结线性策略在原任务、目标 approach、parent 是否存在的条件下实际采样候选；AST whitelist 计算表达式结果进行验证，不执行任意生成程序。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22290v1">原论文</a> · <a href="../../../../post-training/2610.22290-elite-replay/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents LLM 后训练 Tsinghua University 2026-10-15 编码 Agent 的最终通过/失败不能指出哪一轮忽略了已有约束。OPRD 在学生自己生成的无提醒轨迹上训练：成功轨迹自模仿；失败轨迹由教师读取训练专用提醒，重新评分同一学生前缀，不是教师另生成一条答案。全局提醒持续有效，观测对应的局部提醒只在下一轮有效，之后必须移除。正式推理去掉教师和全部提醒。原文 §3 完整实验成本过高，不复现（审查 DONE）。奇偶校验只用于构造诊断 outcome，不是编码正确性。L1 算法组件，不是 SWE-bench 编码能力复现。已实现作用域、同前缀评分和训练目标；完整实验成本过高，不复现（审查 DONE）。不进入 evolve 晋级。本地使用随机初始化的128词表、12维 causal cumulative-embedding 策略。每步真实采样8条三轮轨迹、每轮2个 token；奇偶校验只用于构造诊断 outcome，不是编码正确性。教师重新读取相同 response 前缀；学生上下文不含提醒。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-oprd-reminder-a48a675d">OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>编码 Agent 的最终通过/失败不能指出哪一轮忽略了已有约束。OPRD 在学生自己生成的无提醒轨迹上训练：成功轨迹自模仿；失败轨迹由教师读取训练专用提醒，重新评分同一学生前缀，不是教师另生成一条答案。全局提醒持续有效，观测对应的局部提醒只在下一轮有效，之后必须移除。正式推理去掉教师和全部提醒。原文 §3</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。奇偶校验只用于构造诊断 outcome，不是编码正确性。L1 算法组件，不是 SWE-bench 编码能力复现。已实现作用域、同前缀评分和训练目标；完整实验成本过高，不复现（审查 DONE）。不进入 evolve 晋级。本地使用随机初始化的128词表、12维 causal cumulative-embedding 策略。每步真实采样8条三轮轨迹、每轮2个 token；奇偶校验只用于构造诊断 outcome，不是编码正确性。教师重新读取相同 response 前缀；学生上下文不含提醒。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21496v1">原论文</a> · <a href="../../../../post-training/2610.21496-oprd-reminder/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Unverified Peers via Shared Residual Distillation LLM 后训练 Shanghai Jiao Tong University 2026-10-15 没有标准答案或可验证 reward 时，整段错误解答也可能包含有用步骤。SRD 不投票选“正确答案”，而比较同题 peers 相对跨题 control 对 token 分布的改变，只接收多位 peer 共同支持的保守残差。学生仍只读取题目与自己的前缀，训练后的推理不需要 peers。 完整多模型实验成本过高，不复现（审查 DONE）；L1 公式、采样隔离与梯度组件，不是数学能力复现。完整多模型实验成本过高，不复现（审查 DONE）；本地不下载 Qwen、不调用外部教师，不进入 evolve 晋级。使用固定两个整数 prompt、8-token vocabulary、随机初始化的 causal cumulative-embedding 小策略。每个更新重新实际采样每题四条长度四的轨迹；均匀保留两个 peers，余下作为 targets；control 来自另一题。冻结初始策略逐前缀读取各上下文，学生不读 peer/control 或标准答案。  On-policy self-distillation 后训练算法组件 SRD LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-shared-residual-distillation-a834c6f2">Learning from Unverified Peers via Shared Residual Distillation</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>没有标准答案或可验证 reward 时，整段错误解答也可能包含有用步骤。SRD 不投票选“正确答案”，而比较同题 peers 相对跨题 control 对 token 分布的改变，只接收多位 peer 共同支持的保守残差。学生仍只读取题目与自己的前缀，训练后的推理不需要 peers。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整多模型实验成本过高，不复现（审查 DONE）；L1 公式、采样隔离与梯度组件，不是数学能力复现。完整多模型实验成本过高，不复现（审查 DONE）；本地不下载 Qwen、不调用外部教师，不进入 evolve 晋级。使用固定两个整数 prompt、8-token vocabulary、随机初始化的 causal cumulative-embedding 小策略。每个更新重新实际采样每题四条长度四的轨迹；均匀保留两个 peers，余下作为 targets；control 来自另一题。冻结初始策略逐前缀读取各上下文，学生不读 peer/control 或标准答案。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22080v1">原论文</a> · <a href="../../../../post-training/2610.22080-shared-residual-distillation/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Training-Free On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-15 共同初始化的专家模型，其线性层融合可以写成匹配各教师输出的最小二乘。关键不是任意协方差，而是每个教师在自己生成的、经过终止和循环筛选的答案上实际遇到的输入二阶矩；统计按 token 数归一，不能让长答案自然压倒其他领域。 完整实验成本过高，不复现（审查 DONE）；L1 公式组件与微型自回归诊断，不是完整论文复现。L1 公式组件与微型自回归诊断，不是完整论文复现。完整实验成本过高，不复现（审查 DONE）；adapter: null、evolve_integrated: false。公开 Hamlet（Gutenberg 1524），固定内容 revision 为 sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784。  多教师能力整合 后训练算法组件 TF-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-tf-opd-c139b549">Training-Free On-Policy Distillation</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>共同初始化的专家模型，其线性层融合可以写成匹配各教师输出的最小二乘。关键不是任意协方差，而是每个教师在自己生成的、经过终止和循环筛选的答案上实际遇到的输入二阶矩；统计按 token 数归一，不能让长答案自然压倒其他领域。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 公式组件与微型自回归诊断，不是完整论文复现。L1 公式组件与微型自回归诊断，不是完整论文复现。完整实验成本过高，不复现（审查 DONE）；adapter: null、evolve_integrated: false。公开 Hamlet（Gutenberg 1524），固定内容 revision 为 sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22236v1">原论文</a> · <a href="../../../../post-training/2610.22236-tf-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation LLM 后训练 Princeton University 2026-10-15 一个教师未必适合学生整段推理：数学推导和代码生成可能需要不同专家，强教师与学生的分布差距也可能太大。论文把 OPD 的教师选择细化到每个学生实际访问的前缀。路由依据可以是教师置信度、师生分布 Hellinger 距离，或对齐隐藏空间的特征平方距离。软路由混合的是概率，不是 logits 或 log-prob 的平均。原文 §3 原文中理论分解和实验表分别讨论教师能力、师生距离和多样性；不要把原文“存在不劣路由”的可能性结论读成每个路由启发式都保证更优。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。三个随机初始化的32词表、8维 causal 策略分别作为学生和两个冻结教师。学生真实采样4-token响应，所有教师评分相同前缀；默认三次更新依次执行 entropy、Hellinger、features 三个准则。使用随机模型，不能衡量真实教师能力或 kernel 正确率。  On-policy distillation 多教师与路由 后训练算法组件 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-token-teacher-selection-efd8fec8">Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Princeton University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>一个教师未必适合学生整段推理：数学推导和代码生成可能需要不同专家，强教师与学生的分布差距也可能太大。论文把 OPD 的教师选择细化到每个学生实际访问的前缀。路由依据可以是教师置信度、师生分布 Hellinger 距离，或对齐隐藏空间的特征平方距离。软路由混合的是概率，不是 logits 或 log-prob 的平均。原文 §3 原文中理论分解和实验表分别讨论教师能力、师生距离和多样性；不要把原文“存在不劣路由”的可能性结论读成每个路由启发式都保证更优。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。L1 算法组件／梯度诊断，不是代码、数学或多模态推理复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。三个随机初始化的32词表、8维 causal 策略分别作为学生和两个冻结教师。学生真实采样4-token响应，所有教师评分相同前缀；默认三次更新依次执行 entropy、Hellinger、features 三个准则。使用随机模型，不能衡量真实教师能力或 kernel 正确率。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21234v1">原论文</a> · <a href="../../../../post-training/2610.21234-token-teacher-selection/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation LLM 后训练 Alibaba Cloud Computing 2026-10-15 仅 initial/final 的 log-probability 位移不能区分“前后两段同向”与“中途反转”。同一 RL run 的 waypoint 只提供一致性证据，不是新的模仿目标。候选由学生 top-k 选择，early/late 位移先按候选学生权重中心化，再以正 cosine 缩放 endpoint credit。 完整实验成本过高，不复现（审查 DONE）；当 gates 全零且 KL 也无梯度时，runner 仍明确失败，并附 seed/step/诊断；L1 gate / dense PPO 组件与真实微型策略更新。完整实验成本过高，不复现（审查 DONE）；不是教师大模型训练重跑，也未集成 evolve。使用固定 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 分为 train/validation/test。  On-policy distillation 后训练算法组件 WAYPOINT-OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-waypoint-opd-30b78a3d">Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Alibaba Cloud Computing · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>仅 initial/final 的 log-probability 位移不能区分“前后两段同向”与“中途反转”。同一 RL run 的 waypoint 只提供一致性证据，不是新的模仿目标。候选由学生 top-k 选择，early/late 位移先按候选学生权重中心化，再以正 cosine 缩放 endpoint credit。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；当 gates 全零且 KL 也无梯度时，runner 仍明确失败，并附 seed/step/诊断；L1 gate / dense PPO 组件与真实微型策略更新。完整实验成本过高，不复现（审查 DONE）；不是教师大模型训练重跑，也未集成 evolve。使用固定 Hamlet 1524 内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 分为 train/validation/test。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21601v1">原论文</a> · <a href="../../../../post-training/2610.21601-waypoint-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight LLM 后训练 University of California, San Diego 2026-10-14 一组 GRPO rollout 全部失败时，组内 advantage 全为0。RSHD 不把参考答案告诉模型，而让同一策略根据失败响应写纠错 note，再用 note 生成新的 replay。只有 replay 通过率严格超过原组，note 才被接纳；之后蒸馏的也不是旧失败响应，而是 note 实际诱导的新续写。推理时只需无 note 学生。原文算法1–2 原文 Figure 2 展示上述完整数据流；Figure 1 说明难题组出现全失败的比例，不能拿它作为本地数据分布。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表因果模型按每题8条响应真实采样；末 token 余数条件只作人工二值 verifier。note writer 的输入只有原提示、失败响应和“失败”标记，不包含 reference token。诊断用精确 token 子序列筛查答案泄漏，重放每 note 两条、严格比较原组通过率，再均匀选取一条 replay 做真实同前缀双评分与梯度更新。  RLHF / RLVR On-policy distillation 失败重放与探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-rshd-81aa0b1d">Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight</h2>
<p class="ar-learning-card__meta">University of California, San Diego · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>一组 GRPO rollout 全部失败时，组内 advantage 全为0。RSHD 不把参考答案告诉模型，而让同一策略根据失败响应写纠错 note，再用 note 生成新的 replay。只有 replay 通过率严格超过原组，note 才被接纳；之后蒸馏的也不是旧失败响应，而是 note 实际诱导的新续写。推理时只需无 note 学生。原文算法1–2 原文 Figure 2 展示上述完整数据流；Figure 1 说明难题组出现全失败的比例，不能拿它作为本地数据分布。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。L1 算法组件／token 梯度诊断，不是自然语言反思或推理能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表因果模型按每题8条响应真实采样；末 token 余数条件只作人工二值 verifier。note writer 的输入只有原提示、失败响应和“失败”标记，不包含 reference token。诊断用精确 token 子序列筛查答案泄漏，重放每 note 两条、严格比较原组通过率，再均匀选取一条 replay 做真实同前缀双评分与梯度更新。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21018v1">原论文</a> · <a href="../../../../post-training/2610.21018-rshd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LoOPSD: On-Policy Self-Distillation with Looped Teachers LLM 后训练 Anhui Province Key Laboratory of Digital Security 2026-10-13 在线自蒸馏需要比学生更有用的教师，但更大外部模型或额外答案上下文并非唯一来源。LoOPSD在不改权重时搜索重复层区间来构造教师，用学生自产前缀进行蒸馏，再从更新后的学生重新搜索下一轮教师。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Appendix A：全部连续层区间先筛128题，24条候选再评872题，前5与标准路径评独立100题；每轮200updates×12题×4responses、每响应上限1024tokens，最多10轮。以Qwen3-1.7B/4B/8B等重复教师计算，完整路线搜索和OPD总预算明显较高；这是上限/配置推断而非实测时长，不做昂贵探针。  on-policy-self-distillation layer-route-search iterative-teacher LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-loopsd-e562cd53">LoOPSD: On-Policy Self-Distillation with Looped Teachers</h2>
<p class="ar-learning-card__meta">Anhui Province Key Laboratory of Digital Security · 论文公开：2026-10-13</p>
<p><strong>方法要点：</strong>在线自蒸馏需要比学生更有用的教师，但更大外部模型或额外答案上下文并非唯一来源。LoOPSD在不改权重时搜索重复层区间来构造教师，用学生自产前缀进行蒸馏，再从更新后的学生重新搜索下一轮教师。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Appendix A：全部连续层区间先筛128题，24条候选再评872题，前5与标准路径评独立100题；每轮200updates×12题×4responses、每响应上限1024tokens，最多10轮。以Qwen3-1.7B/4B/8B等重复教师计算，完整路线搜索和OPD总预算明显较高；这是上限/配置推断而非实测时长，不做昂贵探针。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.18162">原论文</a> · <a href="../../../../reproductions/2610.18162-loopsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation LLM 后训练 Taobao &amp; Tmall Group of Alibaba 2026-10-09 异构 tokenizer 的同一文本有不同分段，直接比较 token ID 无意义。CAST 先匹配实际解码文本，将教师 span 的总 log probability 均匀投影到学生 span，再按不确定性×局部平滑度分配 credit；未对齐位置通过初始学生 KL 限制漂移。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为未蒸馏的相同student checkpoint，实验组执行异构tokenizer文本span对齐与credit/anchor训练；本地弱teacher短运行不证明有效知识迁移，稳定相对提升不适用。  Cross-tokenizer distillation Token credit assignment Selective KL anchoring LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-cast-opd-cae7ae27">CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Taobao &amp; Tmall Group of Alibaba · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>异构 tokenizer 的同一文本有不同分段，直接比较 token ID 无意义。CAST 先匹配实际解码文本，将教师 span 的总 log probability 均匀投影到学生 span，再按不确定性×局部平滑度分配 credit；未对齐位置通过初始学生 KL 限制漂移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为未蒸馏的相同student checkpoint，实验组执行异构tokenizer文本span对齐与credit/anchor训练；本地弱teacher短运行不证明有效知识迁移，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13257">原论文</a> · <a href="../../../../reproductions/2610.13257-cast-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation LLM 后训练 Nanjing University / JD.com 2026-10-09 多域只路由各自教师，不能防止共享参数更新损害其他能力。Road 用未路由教师在当前目标域的同一学生轨迹上给出兼容性证据，调节 token credit，再求真实辅助梯度，投影目标梯度但保留其范数下限。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为不投影的多教师OPD，实验组执行按域teacher路由与逐tensor预防式梯度投影；小型公开算术域运行是机制诊断，稳定相对提升不适用。  Multi-teacher distillation Gradient projection Cross-domain guarding LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-road-mopd-dfda03a0">Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Nanjing University / JD.com · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>多域只路由各自教师，不能防止共享参数更新损害其他能力。Road 用未路由教师在当前目标域的同一学生轨迹上给出兼容性证据，调节 token credit，再求真实辅助梯度，投影目标梯度但保留其范数下限。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：基线为不投影的多教师OPD，实验组执行按域teacher路由与逐tensor预防式梯度投影；小型公开算术域运行是机制诊断，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13521">原论文</a> · <a href="../../../../reproductions/2610.13521-road-mopd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation LLM 后训练 East China Normal University 2026-10-08 轻量权重网络根据师生预测学习 token 监督权重。它通过一次可微虚拟学生更新后的参考解损失获得元梯度，再使用新权重执行真实学生更新。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  On-policy distillation Meta-learning LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-meta-opd-c3af9659">MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation</h2>
<p class="ar-learning-card__meta">East China Normal University · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>轻量权重网络根据师生预测学习 token 监督权重。它通过一次可微虚拟学生更新后的参考解损失获得元梯度，再使用新权重执行真实学生更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11989">原论文</a> · <a href="../../../../post-training/2610.11989-meta-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution LLM 后训练 New York University 2026-10-08 语义相关不代表技能真正能够教会模型。SGUID 先从当前模型的已验证训练轨迹生成候选技能，再观察技能在蒸馏早期、晚期是否持续提供与验证器一致的信号。探测训练完成后恢复本轮初始权重，只用通过筛选的紧凑库重新训练；下一轮由更新后的模型重新产技能，不沿用固定手写库。 不复现原 all-linear rank-64、dropout=0.05、原技能生成提示或数学大赛收益。8 次真实梯度更新使 adapter 探测位移为 0.03139，但所有技能的早/晚积极教学次数均为 0，因而无技能入选，精确恢复本轮初始权重，未执行紧凑库训练和第二轮。Qwen3.5-9B 的固定扩展协议已在 A100 完成两轮、464 次真实梯度更新，技能筛选、权重恢复与重新蒸馏均通过机制核验。4 题 validation 的 EM 从 75% 降到 25%，前后均有 2 题截断；保留负结果。GPU 回执只证明 L1 有界机制执行，不证明能力提升。此前失败运行也保持原样归档。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-sguid-340394af">Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution</h2>
<p class="ar-learning-card__meta">New York University · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>语义相关不代表技能真正能够教会模型。SGUID 先从当前模型的已验证训练轨迹生成候选技能，再观察技能在蒸馏早期、晚期是否持续提供与验证器一致的信号。探测训练完成后恢复本轮初始权重，只用通过筛选的紧凑库重新训练；下一轮由更新后的模型重新产技能，不沿用固定手写库。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原 all-linear rank-64、dropout=0.05、原技能生成提示或数学大赛收益。8 次真实梯度更新使 adapter 探测位移为 0.03139，但所有技能的早/晚积极教学次数均为 0，因而无技能入选，精确恢复本轮初始权重，未执行紧凑库训练和第二轮。Qwen3.5-9B 的固定扩展协议已在 A100 完成两轮、464 次真实梯度更新，技能筛选、权重恢复与重新蒸馏均通过机制核验。4 题 validation 的 EM 从 75% 降到 25%，前后均有 2 题截断；保留负结果。GPU 回执只证明 L1 有界机制执行，不证明能力提升。此前失败运行也保持原样归档。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12367">原论文</a> · <a href="../../../../post-training/2610.12367-sguid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes LLM 后训练 Valeo.ai 2026-10-01 程序化合成场景自动给出对象身份和空间坐标；teacher 接收文本化空间特权信息，student 只看图像与问题，在自己的 on-policy token 上蒸馏 teacher。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  多模态后训练 OPD 空间引导 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-where-opd-73f1d45e">Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes</h2>
<p class="ar-learning-card__meta">Valeo.ai · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>程序化合成场景自动给出对象身份和空间坐标；teacher 接收文本化空间特权信息，student 只看图像与问题，在自己的 on-policy token 上蒸馏 teacher。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02117">原论文</a> · <a href="../../../../post-training/2610.02117-where-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation LLM 后训练 University of Southern California 2026-09-29 冻结 executor，只训练 advisor；反思先提出修正，再对同一已记录 executor 响应分别计算有建议与无建议的平均 log-likelihood，只有影响幅度超过 donor-advice 校准阈值的决定才进入自蒸馏。 不调用 Gemini/Claude executor，未复现 BFCL-v3。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Advisor 自蒸馏 GRPO LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-advisd-0fd17b91">AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation</h2>
<p class="ar-learning-card__meta">University of Southern California · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>冻结 executor，只训练 advisor；反思先提出修正，再对同一已记录 executor 响应分别计算有建议与无建议的平均 log-likelihood，只有影响幅度超过 donor-advice 校准阈值的决定才进入自蒸馏。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>不调用 Gemini/Claude executor，未复现 BFCL-v3。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38142">原论文</a> · <a href="../../../../post-training/2609.38142-advisd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation LLM 后训练 KAIST 2026-09-29 把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 factorized teacher composition；未加载 LLM/VLM teacher。执行 factorized teacher composition；未加载 LLM/VLM teacher。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  OPD 多模态后训练 teacher composition LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-lego-opd-93f05fa7">LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation</h2>
<p class="ar-learning-card__meta">KAIST · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 factorized teacher composition；未加载 LLM/VLM teacher。执行 factorized teacher composition；未加载 LLM/VLM teacher。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00333">原论文</a> · <a href="../../../../post-training/2610.00333-lego-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation LLM 后训练 Nanyang Technological University 2026-09-29 MAESTRO 用教师 top-k 覆盖度和 Bhattacharyya 相似度构造逐 token Policy Disagreement Score，并对靠近响应起点的位置加权；教师只在高分歧位置介入，减少整段 teacher rollout 的固定开销。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  On-policy distillation 教师介入 策略分歧 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-maestro-opd-551f210d">From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Nanyang Technological University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>MAESTRO 用教师 top-k 覆盖度和 Bhattacharyya 相似度构造逐 token Policy Disagreement Score，并对靠近响应起点的位置加权；教师只在高分歧位置介入，减少整段 teacher rollout 的固定开销。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37510">原论文</a> · <a href="../../../../post-training/2609.37510-maestro/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning LLM 后训练 University of Florida 2026-09-29 GRPO warm start 后，策略为每条已完成轨迹写一条 hindsight skill，并对同一 response 做普通 context 与 skill context 两次 forward。后者是 stop-gradient teacher；PR-OPD 在每层、每个 response token 对齐投影 hidden state，再与 reward objective 组合。推理时 skill 和 teacher 分支都移除。 复现级别：L1 表征对齐目标。复现级别：L1 表征对齐目标。实现多层、多 response-token 的 stop-gradient privileged alignment。测试覆盖相同表征时零损失、不同表征时正损失、mask 与 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 ALFWorld/WebShop 或 GRPO warm start，不能宣称论文最高 +14.0 点结果。  Agentic RL On-policy distillation 表征对齐 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-pr-opd-9c73d4f9">PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">University of Florida · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>GRPO warm start 后，策略为每条已完成轨迹写一条 hindsight skill，并对同一 response 做普通 context 与 skill context 两次 forward。后者是 stop-gradient teacher；PR-OPD 在每层、每个 response token 对齐投影 hidden state，再与 reward objective 组合。推理时 skill 和 teacher 分支都移除。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 表征对齐目标。复现级别：L1 表征对齐目标。实现多层、多 response-token 的 stop-gradient privileged alignment。测试覆盖相同表征时零损失、不同表征时正损失、mask 与 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 ALFWorld/WebShop 或 GRPO warm start，不能宣称论文最高 +14.0 点结果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36642">原论文</a> · <a href="../../../../post-training/2609.36642-pr-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning LLM 后训练 Huawei Noah’s Ark Lab 2026-09-29 把教师对学生采样 token 的负对数概率当作成本，约束每个生成前缀的平均成本。一旦某个前缀越界，后续进入吸收惩罚状态，防止“先生成坏推理、再靠容易 token 拉低平均成本”；同时把即时奖励的全词表期望精确求导，降低只采样当前动作的方差。 L1 可微目标与优化诊断。L1 可微目标与优化诊断。真实执行全词表即时奖励梯度和未来 Monte Carlo 回报，不等于已蒸馏完整推理模型。API 输入一条无 padding 的 on-policy 轨迹，以及每个访问前缀的全词表教师 log-prob 和任务奖励。调用方负责真实教师/学生 rollout、变长批处理、基准和同预算对照；本次未接入完整 LLM 训练。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 对三动作学生策略训练 80 步 Adam，三个随机初始 seed；教师分布固定公开为 [0.7,0.29,0.01]，预算 2，惩罚 4。  教师前缀约束蒸馏 约束强化学习 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-weakest-link-b901a370">The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Huawei Noah’s Ark Lab · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>把教师对学生采样 token 的负对数概率当作成本，约束每个生成前缀的平均成本。一旦某个前缀越界，后续进入吸收惩罚状态，防止“先生成坏推理、再靠容易 token 拉低平均成本”；同时把即时奖励的全词表期望精确求导，降低只采样当前动作的方差。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>L1 可微目标与优化诊断。L1 可微目标与优化诊断。真实执行全词表即时奖励梯度和未来 Monte Carlo 回报，不等于已蒸馏完整推理模型。API 输入一条无 padding 的 on-policy 轨迹，以及每个访问前缀的全词表教师 log-prob 和任务奖励。调用方负责真实教师/学生 rollout、变长批处理、基准和同预算对照；本次未接入完整 LLM 训练。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 对三动作学生策略训练 80 步 Adam，三个随机初始 seed；教师分布固定公开为 [0.7,0.29,0.01]，预算 2，惩罚 4。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00332">原论文</a> · <a href="../../../../post-training/2610.00332-weakest-link/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MAS-OPD: On-Policy Distillation for Multi-Agent Systems LLM 后训练 University of Science and Technology of China 2026-09-28 以目标角色与非目标角色 teacher 信号差构造 role advantage，并把协作冲突归因只提供给 teacher 形成 privileged coordination supervision。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  多 Agent On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-mas-opd-e3c3be86">MAS-OPD: On-Policy Distillation for Multi-Agent Systems</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>以目标角色与非目标角色 teacher 信号差构造 role advantage，并把协作冲突归因只提供给 teacher 形成 privileged coordination supervision。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34234">原论文</a> · <a href="../../../../post-training/2609.34234-mas-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Learning from Teacher Continuations at Student States LLM 后训练 University of Illinois Urbana-Champaign 2026-09-28 由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  在线蒸馏 Teacher continuation LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-olive-4870752f">Learning from Teacher Continuations at Student States</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36246">原论文</a> · <a href="../../../../post-training/2609.36246-olive/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation LLM 后训练 Arizona State University / University of Virginia / Stevens Institute of Technology 2026-09-15 用真实视觉与空视觉教师分布之差重建视觉偏好目标，抑制错误语言前缀的惯性。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行目标重建公式；未加载多模态 checkpoint。本地执行目标重建公式；未加载多模态 checkpoint。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多模态后训练 On-policy distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-opd-aha-11a1ffc3">OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Arizona State University / University of Virginia / Stevens Institute of Technology · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>用真实视觉与空视觉教师分布之差重建视觉偏好目标，抑制错误语言前缀的惯性。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行目标重建公式；未加载多模态 checkpoint。本地执行目标重建公式；未加载多模态 checkpoint。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16459">原论文</a> · <a href="../../../../post-training/2609.16459-opd-aha/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Negative Self-Distillation: Learning to Reason by Avoiding Flaws LLM 后训练 University of Virginia 2026-09-10 让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  负向自蒸馏 推理后训练 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-nsd-9169c0f1">Negative Self-Distillation: Learning to Reason by Avoiding Flaws</h2>
<p class="ar-learning-card__meta">University of Virginia · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11699">原论文</a> · <a href="../../../../post-training/2609.11699-nsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts LLM 后训练 Institute of Information Engineering, Chinese Academy of Sciences 2026-09-09 异构教师与学生的绝对概率刻度不可直接比较。CompassOPD 用教师相对其 reference 的后训练变化作“指南针”，并在模型族内中心化，保留方向而消除不同模型族的整体偏置。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现去除 family offset 的教师方向，不冒充跨 tokenizer 的完整 LLM 训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。当前候选共享同一有限动作空间，未复刻跨 tokenizer 映射和全参数训练，因此属于 L1 机制诊断。  跨模型族 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-compass-opd-6b3a07da">CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts</h2>
<p class="ar-learning-card__meta">Institute of Information Engineering, Chinese Academy of Sciences · 论文公开：2026-09-09</p>
<p><strong>方法要点：</strong>异构教师与学生的绝对概率刻度不可直接比较。CompassOPD 用教师相对其 reference 的后训练变化作“指南针”，并在模型族内中心化，保留方向而消除不同模型族的整体偏置。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现去除 family offset 的教师方向，不冒充跨 tokenizer 的完整 LLM 训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。当前候选共享同一有限动作空间，未复刻跨 tokenizer 映射和全参数训练，因此属于 L1 机制诊断。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10154">原论文</a> · <a href="../../../../post-training/2609.10154-compass-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation LLM 后训练 KAIST AI 2026-09-08 OPRD 不直接模仿弱教师答案，而是先测量弱教师经过后训练后的 logit 变化方向，再沿这个方向增强强模型的可验证奖励梯度；核心假设是“学习方向”比弱模型最终能力更容易迁移。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现论文的反向蒸馏方向提取与验证器梯度投影，不把小型分类策略的结果等同于完整 LLM 后训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。本地仅验证方向提取和的可执行性；候选集合来自带标签的诊断任务，故 diagnostic_only=true、不可晋升为能力证据。  弱到强反向蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-oprd-e69b9862">Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation</h2>
<p class="ar-learning-card__meta">KAIST AI · 论文公开：2026-09-08</p>
<p><strong>方法要点：</strong>OPRD 不直接模仿弱教师答案，而是先测量弱教师经过后训练后的 logit 变化方向，再沿这个方向增强强模型的可验证奖励梯度；核心假设是“学习方向”比弱模型最终能力更容易迁移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。实现论文的反向蒸馏方向提取与验证器梯度投影，不把小型分类策略的结果等同于完整 LLM 后训练。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。本地仅验证方向提取和的可执行性；候选集合来自带标签的诊断任务，故 diagnostic_only=true、不可晋升为能力证据。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08798">原论文</a> · <a href="../../../../post-training/2609.08798-oprd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD LLM 后训练 Peking University 2026-08-27 普通 MOPD 很少采到强正优势 token，也无法判断更新方向是否可靠。方法扩大温度覆盖，按轨迹正优势密度挑样本，再用熵校准 CLL 概率门控 token 更新。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现双温采样、正优势密度筛选和 centered log-likelihood 门控。未加载通用/垂域教师 checkpoint；本地结果仅证明筛选与随机门控控制流。arithmetic-smoke 本轮 accuracy 0.1953 → 0.1953。零提升被如实保留：机制运行正常，但单教师候选套件不能证明论文多教师收益。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-uc-mopd-4afbd03c">Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD</h2>
<p class="ar-learning-card__meta">Peking University · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>普通 MOPD 很少采到强正优势 token，也无法判断更新方向是否可靠。方法扩大温度覆盖，按轨迹正优势密度挑样本，再用熵校准 CLL 概率门控 token 更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现双温采样、正优势密度筛选和 centered log-likelihood 门控。未加载通用/垂域教师 checkpoint；本地结果仅证明筛选与随机门控控制流。arithmetic-smoke 本轮 accuracy 0.1953 → 0.1953。零提升被如实保留：机制运行正常，但单教师候选套件不能证明论文多教师收益。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26735">原论文</a> · <a href="../../../../post-training/2608.26735-uc-mopd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models LLM 后训练 Nanyang Technological University 2026-08-27 学生读取完整视频，训练期自教师只读取人工标注的证据帧；再按 token 对证据的依赖度加权蒸馏。论文称效果接近 GRPO，而训练时间减少约 60%。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现证据视图自教师与 evidence-guided token 权重。公开 smoke 数据没有视频帧，使用独立奖励轴模拟“证据依赖”；未训练 Video-LLM，不把概念验证写成论文指标复刻。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.6562，记录 evidence token weight 与 teacher gap。指标见 metrics/arithmetic-smoke-seed42.json。  证据帧特权自蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-video-opsd-2da91d84">Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models</h2>
<p class="ar-learning-card__meta">Nanyang Technological University · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>学生读取完整视频，训练期自教师只读取人工标注的证据帧；再按 token 对证据的依赖度加权蒸馏。论文称效果接近 GRPO，而训练时间减少约 60%。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现证据视图自教师与 evidence-guided token 权重。公开 smoke 数据没有视频帧，使用独立奖励轴模拟“证据依赖”；未训练 Video-LLM，不把概念验证写成论文指标复刻。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.6562，记录 evidence token weight 与 teacher gap。指标见 metrics/arithmetic-smoke-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27065">原论文</a> · <a href="../../../../post-training/2608.27065-video-opsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Boosting LLM Exploration via Weak-Model Guidance in RLVR LLM 后训练 Peking University 2026-08-27 RLVR 容易熵坍缩。论文用更小弱模型生成部分推理前缀，迫使目标模型进入陌生轨迹，再以 entropy 截断和原生/前缀样本混训保持覆盖率。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现跨模型前缀扰动、混合采样与 entropy 诊断。弱教师由冻结 reference 分布模拟；未声称完成双 checkpoint RLVR。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6797，并记录 guided entropy 与 prefix surprise。  弱模型前缀探索 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-weak-guide-rlvr-a37f47f8">Boosting LLM Exploration via Weak-Model Guidance in RLVR</h2>
<p class="ar-learning-card__meta">Peking University · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>RLVR 容易熵坍缩。论文用更小弱模型生成部分推理前缀，迫使目标模型进入陌生轨迹，再以 entropy 截断和原生/前缀样本混训保持覆盖率。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现跨模型前缀扰动、混合采样与 entropy 诊断。弱教师由冻结 reference 分布模拟；未声称完成双 checkpoint RLVR。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6797，并记录 guided entropy 与 prefix surprise。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27420">原论文</a> · <a href="../../../../post-training/2608.27420-weak-guide-rlvr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding LLM 后训练 University of Maryland, College Park 2026-08-26 学生仍看完整长视频，冻结教师在训练时只看问题相关 clue interval；学生自己的 rollout 上做 on-policy self-distillation，推理时不需要 clue、标签或外部教师。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.5938（+375.00%）；clue 用 process-reward proxy 代替。  长视频特权视图 OPD LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-clue-opsd-7ed80773">Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding</h2>
<p class="ar-learning-card__meta">University of Maryland, College Park · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>学生仍看完整长视频，冻结教师在训练时只看问题相关 clue interval；学生自己的 rollout 上做 on-policy self-distillation，推理时不需要 clue、标签或外部教师。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.5938（+375.00%）；clue 用 process-reward proxy 代替。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25356">原论文</a> · <a href="../../../../post-training/2608.25356-clue-opsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation LLM 后训练 Alibaba / Qwen 2026-08-04 先用 reward-priority 分别训练专长教师，再在学生自身轨迹上合并多个教师能力。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 多奖励 RL LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-smopd-2a4bef05">SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation</h2>
<p class="ar-learning-card__meta">Alibaba / Qwen · 论文公开：2026-08-04</p>
<p><strong>方法要点：</strong>先用 reward-priority 分别训练专长教师，再在学生自身轨迹上合并多个教师能力。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03092">原论文</a> · <a href="../../../../post-training/2608.03092-smopd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance LLM 后训练 Tianjin University 2026-08-01 只对负向零方差 group 启用教师，并在高熵或大 teacher-student gap token 上蒸馏，同时注入教师正确轨迹 SFT。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD RLVR LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-rstg-e8f7dde4">Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance</h2>
<p class="ar-learning-card__meta">Tianjin University · 论文公开：2026-08-01</p>
<p><strong>方法要点：</strong>只对负向零方差 group 启用教师，并在高熵或大 teacher-student gap token 上蒸馏，同时注入教师正确轨迹 SFT。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00782">原论文</a> · <a href="../../../../post-training/2608.00782-rstg/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Contrastive Reinforced Policy Optimization via Privileged Self-Distillation LLM 后训练 Authors did not disclose affiliation 2026-07-30 按预测熵区分反思探索正位置和 exposure-bias 负位置，对 privileged self-distillation 做组内对比。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD Agentic RL LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-crpo-a18535ff">Contrastive Reinforced Policy Optimization via Privileged Self-Distillation</h2>
<p class="ar-learning-card__meta">Authors did not disclose affiliation · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>按预测熵区分反思探索正位置和 exposure-bias 负位置，对 privileged self-distillation 做组内对比。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28026">原论文</a> · <a href="../../../../post-training/2607.28026-crpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="VAD LLM 后训练 Shanghai Jiao Tong University 2026-07-30 多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。 未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。本页复现论文可隔离的 counterfactual target reconstruction；本地候选策略用过程证据轴模拟 evidence-present / evidence-removed 教师视图，不把它写成 4B/9B 多模态模型复现。候选答案的过程质量轴替代真实图像裁剪，验证的是 counterfactual target reconstruction 的数学路径；未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。  多模态证据归因蒸馏 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-vad-1b365cba">VAD</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong University · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。本页复现论文可隔离的 counterfactual target reconstruction；本地候选策略用过程证据轴模拟 evidence-present / evidence-removed 教师视图，不把它写成 4B/9B 多模态模型复现。候选答案的过程质量轴替代真实图像裁剪，验证的是 counterfactual target reconstruction 的数学路径；未运行 Qwen3.5、视觉 top-100 token support 和六个官方视觉 benchmark。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28590">原论文</a> · <a href="../../../../post-training/2607.28590-vad/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="Distilled RL LLM 后训练 Nankai University 2026-07-19 传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现反向比率裁剪、负样本 reset 与序列几何归一化；教师不是无条件 KL target。  教师奖励重权重 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-distilled-rl-b41ef584">Distilled RL</h2>
<p class="ar-learning-card__meta">Nankai University · 论文公开：2026-07-19</p>
<p><strong>方法要点：</strong>传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现反向比率裁剪、负样本 reset 与序列几何归一化；教师不是无条件 KL target。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17247">原论文</a> · <a href="../../../../post-training/2607.17247-distilled-rl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="ARMOR LLM 后训练 University of Science and Technology of China 2026-07-11 单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。reference 是本地初始化候选策略，不包含论文规模的长程训练或真实轨迹池。每个训练组一半从当前策略采样、一半从冻结 reference 采样，分别记录 anchor 数、权重和最终策略指标。  Reference anchor LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-armor-71dc1f8a">ARMOR</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-07-11</p>
<p><strong>方法要点：</strong>单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。reference 是本地初始化候选策略，不包含论文规模的长程训练或真实轨迹池。每个训练组一半从当前策略采样、一半从冻结 reference 采样，分别记录 anchor 数、权重和最终策略指标。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10481">原论文</a> · <a href="../../../../post-training/2607.10481-armor/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="MOPD LLM 后训练 Xiaomi 2026-06-29 多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现四个奖励轴的 domain teacher、按样本域证据混合，并限制在 student rollout support。  多教师能力整合 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-mopd-f0fd48c7">MOPD</h2>
<p class="ar-learning-card__meta">Xiaomi · 论文公开：2026-06-29</p>
<p><strong>方法要点：</strong>多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现四个奖励轴的 domain teacher、按样本域证据混合，并限制在 student rollout support。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.30406">原论文</a> · <a href="../../../../post-training/2606.30406-mopd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="POLARIS: Guiding Small Models to Write Long Stories LLM 后训练 University of Maryland 2026-06-02 核固定v2 Section3.2 Eq5和作者fixed verl core：policy-only mean/sample-std，Aref=0.4 min(1,t/15)(rref−μ)/(σ+1e-6)，step0为0；K5+1，clip0.2、KL关闭，token-mean。相同external rubric给policy和ref评分。按adv符号在log-ratio域选精确clipped分支，避免exp溢出的伪有限forward/NaN backward，不改原目标。 成本过高，不复现（审查 DONE）。Qwen3.5-9B、1388 copyrighted prompt-story pairs、4×A10080GB FSDP、batch8、160steps，每run原文约48h并约60美元judge API。完整实验明确超单卡短时预算；人类故事不公开，不能用自造故事冒充原训练数据。hri_advantages仅处理外部真实reward，hri_grpo_loss处理current/old teacher-forced logp与response mask。未实现Story Quality judge、版权故事、thinking trace生成或完整写作RL训练；  RLVR与偏好优化 GRPO与参考轨迹注入 LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-polaris-hri-c07af119">POLARIS: Guiding Small Models to Write Long Stories</h2>
<p class="ar-learning-card__meta">University of Maryland · 论文公开：2026-06-02</p>
<p><strong>方法要点：</strong>核固定v2 Section3.2 Eq5和作者fixed verl core：policy-only mean/sample-std，Aref=0.4 min(1,t/15)(rref−μ)/(σ+1e-6)，step0为0；K5+1，clip0.2、KL关闭，token-mean。相同external rubric给policy和ref评分。按adv符号在log-ratio域选精确clipped分支，避免exp溢出的伪有限forward/NaN backward，不改原目标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。Qwen3.5-9B、1388 copyrighted prompt-story pairs、4×A10080GB FSDP、batch8、160steps，每run原文约48h并约60美元judge API。完整实验明确超单卡短时预算；人类故事不公开，不能用自造故事冒充原训练数据。hri_advantages仅处理外部真实reward，hri_grpo_loss处理current/old teacher-forced logp与response mask。未实现Story Quality judge、版权故事、thinking trace生成或完整写作RL训练；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.04095v1">原论文</a> · <a href="../../../../post-training/2606.04095-polaris-hri/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPCD LLM 后训练 Microsoft Research 2026-02-12 提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。论文覆盖经验知识蒸馏和系统提示蒸馏，并支持跨模型尺寸教师。 保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；当前为候选策略机制复现，不等同于 Qwen3/VeRL 原始训练。本地“经验上下文”是已验证答案形成的可审计条件分布，不包含真实长 system prompt；未复跑 FrozenLake、Sokoban 或医疗/安全任务，因此不能将本地准确率与论文横向比较。稳定指标见 omitted-agentic-rl-opd-seed42.json。  Context distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-opcd-d21234a6">OPCD</h2>
<p class="ar-learning-card__meta">Microsoft Research · 论文公开：2026-02-12</p>
<p><strong>方法要点：</strong>提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。论文覆盖经验知识蒸馏和系统提示蒸馏，并支持跨模型尺寸教师。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；保真度：实现无上下文学生 rollout、带经验上下文教师、reverse KL 与经验内化更新；当前为候选策略机制复现，不等同于 Qwen3/VeRL 原始训练。本地“经验上下文”是已验证答案形成的可审计条件分布，不包含真实长 system prompt；未复跑 FrozenLake、Sokoban 或医疗/安全任务，因此不能将本地准确率与论文横向比较。稳定指标见 omitted-agentic-rl-opd-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12275">原论文</a> · <a href="../../../../post-training/2602.12275-opcd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/teacher-and-context" data-search="OPSD LLM 后训练 University of California, Los Angeles 2026-01-26 普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。轨迹由学生生成，教师只在学生实际到达的前缀上提供全词表监督；逐 token pointwise divergence clipping 防止风格 token 主导训练。 保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；当前为候选策略机制复现，不是 Qwen3 参数级训练。本地特权教师由当前策略与已验证候选答案共同构造，真实更新候选策略参数；未训练 Qwen3，也未复跑竞赛数学数据。该结果只验证双视图数据流、散度与裁剪机制。稳定指标见 omitted-agentic-rl-opd-seed42.json。  On-policy self-distillation LLM 后训练 教师与纠错：额外信息何时能帮到学生">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 教师与纠错：额外信息何时能帮到学生</a></p>
<h2 id="paper-post-training-opsd-096ec0f1">OPSD</h2>
<p class="ar-learning-card__meta">University of California, Los Angeles · 论文公开：2026-01-26</p>
<p><strong>方法要点：</strong>普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。轨迹由学生生成，教师只在学生实际到达的前缀上提供全词表监督；逐 token pointwise divergence clipping 防止风格 token 主导训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；保真度：实现同参数教师/学生双视图、学生 on-policy rollout、特权答案条件、稠密分布监督与逐项散度裁剪；当前为候选策略机制复现，不是 Qwen3 参数级训练。本地特权教师由当前策略与已验证候选答案共同构造，真实更新候选策略参数；未训练 Qwen3，也未复跑竞赛数学数据。该结果只验证双视图数据流、散度与裁剪机制。稳定指标见 omitted-agentic-rl-opd-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18734">原论文</a> · <a href="../../../../post-training/2601.18734-opsd/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
