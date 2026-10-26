---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 奖励与信用：正确结果该奖励哪些步骤

[LLM 后训练](index.md) / 子主题导学 · 约 3 分钟 · 36 张论文卡

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

1. [Let's Verify Step by Step](../../../post-training/2305.20050-process-supervision/README.md) · [原论文](https://arxiv.org/abs/2305.20050)
2. [Math-Shepherd](../../../post-training/2312.08935-math-shepherd/README.md) · [原论文](https://arxiv.org/abs/2312.08935)
3. [TACO](../../../post-training/2607.07976-taco/README.md) · [原论文](https://arxiv.org/abs/2607.07976)

## 自测一下

一条长回答最终正确，能否把所有token都赋予相同正信用，并据此声称每一步正确？

??? note "展开参考答案"

    不能。终局奖励只说明输出满足验收条件，无法证明中间过程无误。统一信用是一种估计选择，应检查错误步骤被强化的风险；细粒度信用也必须有可靠来源和独立对照，不能把评审分数本身当作过程真值。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 36 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning LLM 后训练 The University of Hong Kong 2026-10-23 一次机器人最终失败，不等于每个动作都导致失败；全轨迹负优势还会惩罚有价值的重抓和恢复尝试。MART-GRPO 用冻结事件 VLM 回看完整失败轨迹，定位最后一次未恢复错误，只保留截止该边界的失败反馈；成功轨迹、原组优势和原始 token 分母不变。论文先分析理想 stopping-time 条件下，何时删除零条件期望的后续梯度可以保持估计器期望；实际回溯 VLM 不自动满足这些理论条件。VLM 用三路同步摄像头、机器人状态、任务与帧/动作 chunk 对齐信息，报告最后一次可见且未恢复的错误起始区间； 这超过单张 A100/A30 或 Mac 的合理迭代预算，完整 actor/VLM 训练和机器人多任务评测为成本过高，不复现（审查 DONE）；诊断真实反传合成 logits，用独立概率空间 Eq.15 参考检查值与梯度、原分母、失败后缀零梯度和成功项保留；本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  策略优化 时序信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-mart-grpo-1903b786">When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning</h2>
<p class="ar-learning-card__meta">The University of Hong Kong · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>一次机器人最终失败，不等于每个动作都导致失败；全轨迹负优势还会惩罚有价值的重抓和恢复尝试。MART-GRPO 用冻结事件 VLM 回看完整失败轨迹，定位最后一次未恢复错误，只保留截止该边界的失败反馈；成功轨迹、原组优势和原始 token 分母不变。论文先分析理想 stopping-time 条件下，何时删除零条件期望的后续梯度可以保持估计器期望；实际回溯 VLM 不自动满足这些理论条件。VLM 用三路同步摄像头、机器人状态、任务与帧/动作 chunk 对齐信息，报告最后一次可见且未恢复的错误起始区间；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>这超过单张 A100/A30 或 Mac 的合理迭代预算，完整 actor/VLM 训练和机器人多任务评测为成本过高，不复现（审查 DONE）；诊断真实反传合成 logits，用独立概率空间 Eq.15 参考检查值与梯度、原分母、失败后缀零梯度和成功项保留；本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32431v1">原论文</a> · <a href="../../../../post-training/2610.32431-mart-grpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning LLM 后训练 论文未列机构（不据邮箱域名推断） 2026-10-16 GRPO会给同题、同正确性的回答相同 advantage，忽略生成的不确定性。MGE-PO 用生成时缓存的 token 熵区分回答，在成功／失败与高熵／低熵四象限上调整信用；再用在线题目熵统计安排课程，并以熵加权参考KL约束优化。原文 §4及附录B 原图建议：Figure 1 方法总览，不能把熵阈值示意图当成本地实验结果。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。无本地实现、指标或能力比较，不进入 Evolve；该终态不阻塞审查水位。成本过高，不复现（审查 DONE）。原实验硬件为2×H200 141GB，完整单次MGE-PO记录约22.6小时，另有Math-7B-Instruct约22.8小时；该计时表的base setting没有单独checkpoint标识，不能强指为8B配置。8B训练另报告624次更新、8epochs、每题8条最长20,480 token回答；Qwen2.5系列使用17,398题和约12k生成上限。附录C与D.8  RLVR 熵与训练稳定性 过程奖励与信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-mge-po-5743f3b7">MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning</h2>
<p class="ar-learning-card__meta">论文未列机构（不据邮箱域名推断） · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>GRPO会给同题、同正确性的回答相同 advantage，忽略生成的不确定性。MGE-PO 用生成时缓存的 token 熵区分回答，在成功／失败与高熵／低熵四象限上调整信用；再用在线题目熵统计安排课程，并以熵加权参考KL约束优化。原文 §4及附录B 原图建议：Figure 1 方法总览，不能把熵阈值示意图当成本地实验结果。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。无本地实现、指标或能力比较，不进入 Evolve；该终态不阻塞审查水位。成本过高，不复现（审查 DONE）。原实验硬件为2×H200 141GB，完整单次MGE-PO记录约22.6小时，另有Math-7B-Instruct约22.8小时；该计时表的base setting没有单独checkpoint标识，不能强指为8B配置。8B训练另报告624次更新、8epochs、每题8条最长20,480 token回答；Qwen2.5系列使用17,398题和约12k生成上限。附录C与D.8</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23245v1">原论文</a> · <a href="../../../../post-training/2610.23245-mge-po/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Training Reasoning Models to Generate Diverse Scientific Ideas LLM 后训练 New York University 2026-10-15 独立采样多个高分想法可能反复得到同一个方向。论文让模型在一次生成中写出整组想法，每个新想法都能看到前面写过的内容，再按整组质量和相互差异训练。每张卡包含 problem gap、core claim、method、inspiration；质量由与 gold idea 的影响力比较提供，语义距离由三个被评字段的 judge 结果等权平均。不是用字符串不同就代表科研创新。原文 §2–3 原图建议 Figure 1：训练流程； 完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。固定诊断、不可晋级、未接 Evolve。L1 CPU reward/evaluation protocol 接口，不是科学创意模型复现。不伪造 SciJudge 或语义距离；完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。CPU runner每 seed构造12组明确标为 synthetic 的 judge 观测：双顺序Boolean赢票，以及三个字段的归一化距离。它们用于检验协议，不来自 SciJudge、LLM或真实科研评价。回调接口可替换为用户明确配置的 judge；  RLHF / RLVR 多样性与科学发现 奖励与评测协议 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-diverge-ideation-5eb53208">Training Reasoning Models to Generate Diverse Scientific Ideas</h2>
<p class="ar-learning-card__meta">New York University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>独立采样多个高分想法可能反复得到同一个方向。论文让模型在一次生成中写出整组想法，每个新想法都能看到前面写过的内容，再按整组质量和相互差异训练。每张卡包含 problem gap、core claim、method、inspiration；质量由与 gold idea 的影响力比较提供，语义距离由三个被评字段的 judge 结果等权平均。不是用字符串不同就代表科研创新。原文 §2–3 原图建议 Figure 1：训练流程；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。固定诊断、不可晋级、未接 Evolve。L1 CPU reward/evaluation protocol 接口，不是科学创意模型复现。不伪造 SciJudge 或语义距离；完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。CPU runner每 seed构造12组明确标为 synthetic 的 judge 观测：双顺序Boolean赢票，以及三个字段的归一化距离。它们用于检验协议，不来自 SciJudge、LLM或真实科研评价。回调接口可替换为用户明确配置的 judge；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22324v1">原论文</a> · <a href="../../../../post-training/2610.22324-diverge-ideation/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents LLM 后训练 Zhejiang University 2026-10-15 不同搜索轨迹即使读到了相同事实，也可能使用完全不同的 query、网页和表述，按表面观察匹配会把可比较的步骤拆散。KnowGPO 将问题所需事实拆为原子条件，训练 verifier 检查每步获得了哪些条件。状态是已验证条件的单调集合；从相同知识前态出发的动作互相比较新增知识，再与最终回答的奖励共同更新策略。原文 §3与附录A 原图建议：Figure 2 方法总览，左侧为训练知识条件构建，右侧为分组与信用；这不表示本地实现了左侧 LLM 标注流程。 完整实验成本过高，不复现（审查 DONE）；L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 Evolve 晋级。随机初始化16词表、8维因果策略，每个问题采样6条三步轨迹，前两步为搜索、最后一步为 answer。公开输入只有题目 token、自己生成的动作和外部文档 ID；私有条件表与训练 outcome 只在 actor 调用外使用。精确小环境 verifier 不是自然语言 LLM verifier，不提供真实搜索能力。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-knowgpo-346974ee">KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>不同搜索轨迹即使读到了相同事实，也可能使用完全不同的 query、网页和表述，按表面观察匹配会把可比较的步骤拆散。KnowGPO 将问题所需事实拆为原子条件，训练 verifier 检查每步获得了哪些条件。状态是已验证条件的单调集合；从相同知识前态出发的动作互相比较新增知识，再与最终回答的奖励共同更新策略。原文 §3与附录A 原图建议：Figure 2 方法总览，左侧为训练知识条件构建，右侧为分组与信用；这不表示本地实现了左侧 LLM 标注流程。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 Evolve 晋级。随机初始化16词表、8维因果策略，每个问题采样6条三步轨迹，前两步为搜索、最后一步为 answer。公开输入只有题目 token、自己生成的动作和外部文档 ID；私有条件表与训练 outcome 只在 actor 调用外使用。精确小环境 verifier 不是自然语言 LLM verifier，不提供真实搜索能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22331v1">原论文</a> · <a href="../../../../post-training/2610.22331-knowgpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL LLM 后训练 University of Minnesota 2026-10-15 GDPO 虽然分别归一化多种奖励，但仍把每种奖励均摊到整条响应。SQL 可执行性、格式、执行结果可能只分别依赖少数 token。MRTPO 用采样时的冻结策略重放响应：先提供所有 verifier 信息，再逐个删除奖励信息块。某个块被移除后，哪些位置的预测变化更大，就把该奖励更多地分配给哪些位置；正负 advantage 都使用相同的相关性权重。原文 §4 原文关键图：Figure 1/3 展示格式、可执行性和执行错误分别影响的 SQL token；见方法与图注。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机初始化32词表策略真实生成响应，两种人工 verifier 只产生 token 条件奖励。冻结快照在完整信息和两个留一上下文下重新评分相同响应前缀；学生原始采样、更新评分均不接收 verifier 块。每个 seed 默认3次真实梯度更新，不使用 SQL、BFCL 或预训练 LLM。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-mrtpo-6e178dc9">Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL</h2>
<p class="ar-learning-card__meta">University of Minnesota · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>GDPO 虽然分别归一化多种奖励，但仍把每种奖励均摊到整条响应。SQL 可执行性、格式、执行结果可能只分别依赖少数 token。MRTPO 用采样时的冻结策略重放响应：先提供所有 verifier 信息，再逐个删除奖励信息块。某个块被移除后，哪些位置的预测变化更大，就把该奖励更多地分配给哪些位置；正负 advantage 都使用相同的相关性权重。原文 §4 原文关键图：Figure 1/3 展示格式、可执行性和执行错误分别影响的 SQL token；见方法与图注。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机初始化32词表策略真实生成响应，两种人工 verifier 只产生 token 条件奖励。冻结快照在完整信息和两个留一上下文下重新评分相同响应前缀；学生原始采样、更新评分均不接收 verifier 块。每个 seed 默认3次真实梯度更新，不使用 SQL、BFCL 或预训练 LLM。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21439v1">原论文</a> · <a href="../../../../post-training/2610.21439-mrtpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering LLM 后训练 Nanjing University 2026-10-15 整条轨迹失败不代表每一步都无用，成功轨迹也可能绕路。OpCredit 的 BOC 从普通 rollout 中复用分支结果：同题、同活动实体，再匹配访问集合、剩余预算和决策阶段；FTC 则衡量该操作局部前沿相对答案邻域的进退。两种信用对齐同一段推理及可执行操作 token，不给工具观察记策略损失。原文 §3、附录D 原文完整实验成本过高，不复现（审查 DONE）；这些是公式及梯度诊断，不是 KGQA 能力比较。L1 信用分配与梯度组件，不是 CWQ/WebQSP/GrailQA 能力复现。原文完整实验成本过高，不复现（审查 DONE）；本地 gold 只供训练后信用计算，不进入 Actor 输入或 evolve 晋级。随机初始化4输入、3输出的小策略在两个固定微型图上，每题真实采样6条关系选择＋答案动作轨迹。gold 仅在 rollout 结束后计算终止奖励与邻域信用；公开状态白名单只有题目、活动实体、访问集合、预算、阶段和可见实体，不能传 gold 字段。  Agentic RL 操作级信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-opcredit-fae57ef0">OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering</h2>
<p class="ar-learning-card__meta">Nanjing University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>整条轨迹失败不代表每一步都无用，成功轨迹也可能绕路。OpCredit 的 BOC 从普通 rollout 中复用分支结果：同题、同活动实体，再匹配访问集合、剩余预算和决策阶段；FTC 则衡量该操作局部前沿相对答案邻域的进退。两种信用对齐同一段推理及可执行操作 token，不给工具观察记策略损失。原文 §3、附录D</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原文完整实验成本过高，不复现（审查 DONE）；这些是公式及梯度诊断，不是 KGQA 能力比较。L1 信用分配与梯度组件，不是 CWQ/WebQSP/GrailQA 能力复现。原文完整实验成本过高，不复现（审查 DONE）；本地 gold 只供训练后信用计算，不进入 Actor 输入或 evolve 晋级。随机初始化4输入、3输出的小策略在两个固定微型图上，每题真实采样6条关系选择＋答案动作轨迹。gold 仅在 rollout 结束后计算终止奖励与邻域信用；公开状态白名单只有题目、活动实体、访问集合、预算、阶段和可见实体，不能传 gold 字段。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21345v1">原论文</a> · <a href="../../../../post-training/2610.21345-opcredit/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Progress Reward Model for Reinforcement Learning via Large Language Models LLM 后训练 Beihang University 2026-10-15 稀疏成功信号难以指导长程机器人控制。PRM4RL 让 LLM 给出子任务、当前子任务判定函数与进度势函数；将子任务语义作为状态先验，将相邻状态进度差作为低层 RL 的密集 reward。规划只需预先生成，而不是每个环境步重新调用 LLM。 完整机器人实验成本过高，不复现（审查 DONE）。L1 状态机、embedding 接口及 reward 机制诊断。L1 状态机、embedding 接口及 reward 机制诊断。这是 NeurIPS 2025 已发表成果于 2026-10-15 上传 arXiv，不能称为新提出的 2026 算法。完整机器人实验成本过高，不复现（审查 DONE）。本地 ProgressPlan 只接收调用者审阅过的 completion predicates、potential 与子任务名称，不执行上游或 LLM 返回的任意 Python。stage 从当前状态重新计算，可因抓取丢失等情况回退，不使用仅随时间递增的计数器。  过程奖励 后训练算法组件 PRM4RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-progress-reward-e17dc6a6">Progress Reward Model for Reinforcement Learning via Large Language Models</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>稀疏成功信号难以指导长程机器人控制。PRM4RL 让 LLM 给出子任务、当前子任务判定函数与进度势函数；将子任务语义作为状态先验，将相邻状态进度差作为低层 RL 的密集 reward。规划只需预先生成，而不是每个环境步重新调用 LLM。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整机器人实验成本过高，不复现（审查 DONE）。L1 状态机、embedding 接口及 reward 机制诊断。L1 状态机、embedding 接口及 reward 机制诊断。这是 NeurIPS 2025 已发表成果于 2026-10-15 上传 arXiv，不能称为新提出的 2026 算法。完整机器人实验成本过高，不复现（审查 DONE）。本地 ProgressPlan 只接收调用者审阅过的 completion predicates、potential 与子任务名称，不执行上游或 LLM 返回的任意 Python。stage 从当前状态重新计算，可因抓取丢失等情况回退，不使用仅随时间递增的计数器。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22056v1">原论文</a> · <a href="../../../../post-training/2610.22056-progress-reward/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learning to Reason with Selective Internal Feedback LLM 后训练 Institute of Automation, Chinese Academy of Sciences 2026-10-15 平均 self-certainty 可以随错误置信一起增长。SIF 不把它当正确性标签，而是比较同一 prompt 内响应的排序 certainty profile：先按窗口比较投票，再按击败 peer 的比例给二元 reward，过滤不具资格的响应和同 reward 组。policy 与 KL 必须同时施加选择 mask。 完整实验成本过高，不复现（审查 DONE）。短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。L1 完整资格 / 投票 / 双 mask 公式组件。默认资格仍为 550 tokens；短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。完整实验成本过高，不复现（审查 DONE）。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；train/validation/test byte 区间 80%/10%/10% 不相交，不按 heldout NLL 选超参。  自置信轨迹过滤 Self-certainty 选择性策略更新 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-sif-620fc6b5">Learning to Reason with Selective Internal Feedback</h2>
<p class="ar-learning-card__meta">Institute of Automation, Chinese Academy of Sciences · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>平均 self-certainty 可以随错误置信一起增长。SIF 不把它当正确性标签，而是比较同一 prompt 内响应的排序 certainty profile：先按窗口比较投票，再按击败 peer 的比例给二元 reward，过滤不具资格的响应和同 reward 组。policy 与 KL 必须同时施加选择 mask。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。L1 完整资格 / 投票 / 双 mask 公式组件。默认资格仍为 550 tokens；短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。完整实验成本过高，不复现（审查 DONE）。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；train/validation/test byte 区间 80%/10%/10% 不相交，不按 heldout NLL 选超参。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21392v1">原论文</a> · <a href="../../../../post-training/2610.21392-sif/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense LLM 后训练 University of British Columbia 2026-10-15 正确性和简短、低时延等奖励相加时，容易获取的辅助奖励可能主导 GRPO：总奖励上涨，主要任务却变差。TAG 不是简单降低辅助权重，而是先从同一基线分别优化每个奖励，观察哪个探针对基线的分布漂移最小，再将该奖励选为 anchor。随后丢弃探针、从原基线重新联合训练，辅助信用只有在 anchor 满足时才生效。原文 §5 原文关键图：Figure 1：短而错误的奖励投机；Figure 4 展示 reverse KL 对新造模式的敏感性。它们不是本地训练结果。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是数学或代码能力复现。L1 算法组件／梯度诊断，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不参与 evolve 晋级。使用随机初始化的32词表、8维 causal cumulative-embedding 策略，不下载任何 checkpoint。两个奖励是人工 token 奇偶条件，不表示数学正确性。每个奖励从同一基线独立做3次更新，在另一组提示上由该探针真实采样并计算选举统计，然后从未变化的基线做3次门控更新。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-tag-reward-gating-d0312c36">Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense</h2>
<p class="ar-learning-card__meta">University of British Columbia · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>正确性和简短、低时延等奖励相加时，容易获取的辅助奖励可能主导 GRPO：总奖励上涨，主要任务却变差。TAG 不是简单降低辅助权重，而是先从同一基线分别优化每个奖励，观察哪个探针对基线的分布漂移最小，再将该奖励选为 anchor。随后丢弃探针、从原基线重新联合训练，辅助信用只有在 anchor 满足时才生效。原文 §5 原文关键图：Figure 1：短而错误的奖励投机；Figure 4 展示 reverse KL 对新造模式的敏感性。它们不是本地训练结果。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是数学或代码能力复现。L1 算法组件／梯度诊断，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不参与 evolve 晋级。使用随机初始化的32词表、8维 causal cumulative-embedding 策略，不下载任何 checkpoint。两个奖励是人工 token 奇偶条件，不表示数学正确性。每个奖励从同一基线独立做3次更新，在另一组提示上由该探针真实采样并计算选举统计，然后从未变化的基线做3次门控更新。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21404v1">原论文</a> · <a href="../../../../post-training/2610.21404-tag-reward-gating/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO LLM 后训练 未确认（已读 arXiv HTML 未列机构） 2026-10-14 RAP-Walk 不把成对视频偏好压成相互独立的胜率，而保留对手身份、循环关系和边清晰度。它在从输者到赢家的可靠随机游走中计算平稳偏好信用，经最低熵校准后修正原始胜率优势，最后仍交给同一 GRPO 更新。偏好循环并不自动表示视频质量差；可能是不同视频各擅长提示遵循、画面或运动。该方法把局部不一致当作传播可靠性线索，而不是删除循环或把循环直接写成负奖励。 完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。L1 图算子与策略更新接口。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。不提供输入时，产物明确标为 explicit_mechanism_fixtures，只验证图方向、循环、校准和可微 GRPO 更新接口。可通过 --input-path observed-graphs.json 提供已有真实评审概率：  偏好图信用分配 GRPO 视频后训练 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-rap-walk-742b8b38">When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO</h2>
<p class="ar-learning-card__meta">未确认（已读 arXiv HTML 未列机构） · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>RAP-Walk 不把成对视频偏好压成相互独立的胜率，而保留对手身份、循环关系和边清晰度。它在从输者到赢家的可靠随机游走中计算平稳偏好信用，经最低熵校准后修正原始胜率优势，最后仍交给同一 GRPO 更新。偏好循环并不自动表示视频质量差；可能是不同视频各擅长提示遵循、画面或运动。该方法把局部不一致当作传播可靠性线索，而不是删除循环或把循环直接写成负奖励。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。L1 图算子与策略更新接口。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。不提供输入时，产物明确标为 explicit_mechanism_fixtures，只验证图方向、循环、校准和可微 GRPO 更新接口。可通过 --input-path observed-graphs.json 提供已有真实评审概率：</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20089v1">原论文</a> · <a href="../../../../post-training/2610.20089-rap-walk/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents LLM 后训练 Zhejiang University / Microsoft 2026-10-09 只按答案奖训练的search agent可能答对却伪造证据依赖。SOAR独立记录atomic query的internal recall和external retrieval，再要求显式声明source。internal recall不接收旧reasoning或external evidence；来源一致性、正确性与格式reward训练真实策略。 本轮SOAR队列使用明确派生的工具文档属性QA训练诊断，不在不匹配的WikiText+GSM上宣称知识QA效果。本地对照口径：基线为相同source-aware工作流的without-source-reward消融；另有冻结初始策略；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Source-aware RL Search agents Source-consistency reward LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-soar-c6475aad">SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents</h2>
<p class="ar-learning-card__meta">Zhejiang University / Microsoft · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>只按答案奖训练的search agent可能答对却伪造证据依赖。SOAR独立记录atomic query的internal recall和external retrieval，再要求显式声明source。internal recall不接收旧reasoning或external evidence；来源一致性、正确性与格式reward训练真实策略。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本轮SOAR队列使用明确派生的工具文档属性QA训练诊断，不在不匹配的WikiText+GSM上宣称知识QA效果。本地对照口径：基线为相同source-aware工作流的without-source-reward消融；另有冻结初始策略；实验组仅支持本页L0/L1机制，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13157">原论文</a> · <a href="../../../../reproductions/2610.13157-soar/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction LLM 后训练 KAIST 2026-10-09 冻结reasoner和小causal encoder，只学习paragraph boundary处的MLP cut policy。真实失败rollout在不同cut被冻结reasoner重新生成，给rescue奖励。推理时独立learned gate决定纠错；保留prefix、结束assistant turn、插固定新user turn，按剩余response预算生成suffix。 本页不声明未执行实验已经完成。本地对照口径：基线为Base@2N完整rollout，对照UPTURN@N及至多N次替换；预算匹配为最大允许生成数，不等于实际耗时一致；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Self-correction Frozen causal encoder Learned cut policy LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-upturn-1713cc09">Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction</h2>
<p class="ar-learning-card__meta">KAIST · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>冻结reasoner和小causal encoder，只学习paragraph boundary处的MLP cut policy。真实失败rollout在不同cut被冻结reasoner重新生成，给rescue奖励。推理时独立learned gate决定纠错；保留prefix、结束assistant turn、插固定新user turn，按剩余response预算生成suffix。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页不声明未执行实验已经完成。本地对照口径：基线为Base@2N完整rollout，对照UPTURN@N及至多N次替换；预算匹配为最大允许生成数，不等于实际耗时一致；实验组仅支持本页L0/L1机制，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13672">原论文</a> · <a href="../../../../reproductions/2610.13672-upturn/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards LLM 后训练 Harbin Engineering University / Tencent / Harbin Institute of Technology 2026-10-08 把全词表师生概率残差变成相对学生的有界局部优势，再逐响应中心化，与验证器优势相加。Co-RA 在同一已评分学生批次上更新教师 LoRA，下一轮才使用新教师。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Teacher guidance LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-residual-advantage-393aad16">Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards</h2>
<p class="ar-learning-card__meta">Harbin Engineering University / Tencent / Harbin Institute of Technology · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>把全词表师生概率残差变成相对学生的有界局部优势，再逐响应中心化，与验证器优势相加。Co-RA 在同一已评分学生批次上更新教师 LoRA，下一轮才使用新教师。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11519">原论文</a> · <a href="../../../../post-training/2610.11519-residual-advantage/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning LLM 后训练 Moore Threads AI 2026-10-01 对每个 token 的 current/rollout log-ratio 先取绝对值再平均，避免正负漂移在序列级几何均值中抵消。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 detached response gate；未训练 Qwen3.5。执行 detached response gate；未训练 Qwen3.5。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RLVR off-policy 响应掩码 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-carm-c2bacd93">CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Moore Threads AI · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>对每个 token 的 current/rollout log-ratio 先取绝对值再平均，避免正负漂移在序列级几何均值中抵消。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 detached response gate；未训练 Qwen3.5。执行 detached response gate；未训练 Qwen3.5。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02039">原论文</a> · <a href="../../../../post-training/2610.02039-carm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning LLM 后训练 Alibaba Group 2026-10-01 自诊断器提出错误类别与位置，只有经证据验证的 claim 才进入在线 error pricing；学得的相对成本把终局 credit 守恒地重分配到步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 信用分配 自诊断 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-my-fault-cefa1f11">My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Alibaba Group · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>自诊断器提出错误类别与位置，只有经证据验证的 claim 才进入在线 error pricing；学得的相对成本把终局 credit 守恒地重分配到步骤。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01161">原论文</a> · <a href="../../../../post-training/2610.01161-my-fault/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Token-Level Video Reinforcement Learning LLM 后训练 原文首页未列第一作者机构 2026-10-01 冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度 credit 归一化；未训练视频扩散模型。执行梯度 credit 归一化；未训练视频扩散模型。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  视频生成 token credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-tvrl-0c541634">Token-Level Video Reinforcement Learning</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度 credit 归一化；未训练视频扩散模型。执行梯度 credit 归一化；未训练视频扩散模型。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01973">原论文</a> · <a href="../../../../post-training/2610.01973-tvrl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning LLM 后训练 Georgia Institute of Technology 2026-09-30 用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 segment credit；未读取 gold plan，也未训练 7B Agent。执行 segment credit；未读取 gold plan，也未训练 7B Agent。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agentic RL segment credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-sharpo-de267e69">SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Georgia Institute of Technology · 论文公开：2026-09-30</p>
<p><strong>方法要点：</strong>用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 segment credit；未读取 gold plan，也未训练 7B Agent。执行 segment credit；未读取 gold plan，也未训练 7B Agent。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00838">原论文</a> · <a href="../../../../post-training/2610.00838-sharpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning LLM 后训练 Nanjing University 2026-09-30 用历史成功轨迹中的剩余步数训练上下文内距离估计器，预测每个状态距离成功还多远；把相邻状态的距离改善转为步骤优势，与轨迹级奖励共同优化。冻结 TabPFN 避免额外训练 critic，失败轨迹不被误标成接近成功的正样本。 尚未复现完整 LLM＋ALFWorld 训练。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。没有用启发式回归器冒充 TabPFN；尚未复现完整 LLM＋ALFWorld 训练。本地预动作输入是公开合成数值状态，不是冻结文本 encoder；完整 ALFWorld/WebShop rollout、文本编码器和 LLM 参数更新未完成。TabPFN MAE 不是任务成功率；没有 CUDA 完整训练或正式 Evolve 接入。  轨迹到步骤信用分配 强化学习 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-t2spo-3a6c006a">T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Nanjing University · 论文公开：2026-09-30</p>
<p><strong>方法要点：</strong>用历史成功轨迹中的剩余步数训练上下文内距离估计器，预测每个状态距离成功还多远；把相邻状态的距离改善转为步骤优势，与轨迹级奖励共同优化。冻结 TabPFN 避免额外训练 critic，失败轨迹不被误标成接近成功的正样本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>尚未复现完整 LLM＋ALFWorld 训练。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。没有用启发式回归器冒充 TabPFN；尚未复现完整 LLM＋ALFWorld 训练。本地预动作输入是公开合成数值状态，不是冻结文本 encoder；完整 ALFWorld/WebShop rollout、文本编码器和 LLM 参数更新未完成。TabPFN MAE 不是任务成功率；没有 CUDA 完整训练或正式 Evolve 接入。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00388">原论文</a> · <a href="../../../../post-training/2610.00388-t2spo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="PACT: From Credit Assignment to Critic Alignment LLM 后训练 AllSpark Team 2026-09-22 终局奖励只有一个标量，但 actor 要更新每个生成 token。论文在完整性、前缀一致性和中性三个条件下，刻画 token 的理论信用为相邻前缀的条件期望之差。实际训练无法精确知道这些期望，因此用概率 critic 估计前缀价值，令 token advantage 近似为 R − V(prefix)。论文的关键是顺序：critic 应逼近 actor 更新后的策略，而不是只拟合刚采样时的旧策略。实用版本用当前 token 的概率比 ρ_t，而非整个未来序列的比率乘积； 以真实自由生成轨迹验证 Actor-then-Critic、更新后策略的重要性校正与概率 critic；本地结果不是原论文大模型成绩。这验证了 PACT 的更新次序与损失路径，但没有复现 4B/35B checkpoint、agentic 工具环境、原文训练规模或原文基准成绩；应作为小模型机制证据，不据此宣称 LLM 能力提升。短预算训练中格式命中率仍为零；上述非零 exact accuracy 只有极少数样本，不能解释为稳定的能力改善。本地使用小型 GRU 因果语言模型、独立前缀 critic、无约束 token 自由生成与 exact-answer verifier。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-pact-439c5053">PACT: From Credit Assignment to Critic Alignment</h2>
<p class="ar-learning-card__meta">AllSpark Team · 论文公开：2026-09-22</p>
<p><strong>方法要点：</strong>终局奖励只有一个标量，但 actor 要更新每个生成 token。论文在完整性、前缀一致性和中性三个条件下，刻画 token 的理论信用为相邻前缀的条件期望之差。实际训练无法精确知道这些期望，因此用概率 critic 估计前缀价值，令 token advantage 近似为 R − V(prefix)。论文的关键是顺序：critic 应逼近 actor 更新后的策略，而不是只拟合刚采样时的旧策略。实用版本用当前 token 的概率比 ρ_t，而非整个未来序列的比率乘积；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>以真实自由生成轨迹验证 Actor-then-Critic、更新后策略的重要性校正与概率 critic；本地结果不是原论文大模型成绩。这验证了 PACT 的更新次序与损失路径，但没有复现 4B/35B checkpoint、agentic 工具环境、原文训练规模或原文基准成绩；应作为小模型机制证据，不据此宣称 LLM 能力提升。短预算训练中格式命中率仍为零；上述非零 exact accuracy 只有极少数样本，不能解释为稳定的能力改善。本地使用小型 GRU 因果语言模型、独立前缀 critic、无约束 token 自由生成与 exact-answer verifier。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.26355">原论文</a> · <a href="../../../../post-training/2609.26355-pact/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TIAO: Token Importance-Aware Policy Optimization for Text Summarization LLM 后训练 National University of Defense Technology 2026-09-15 通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-tiao-f57cc707">TIAO: Token Importance-Aware Policy Optimization for Text Summarization</h2>
<p class="ar-learning-card__meta">National University of Defense Technology · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16748">原论文</a> · <a href="../../../../post-training/2609.16748-tiao/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning LLM 后训练 University of Pittsburgh 2026-08-27 结果奖励过稀，神经 PRM 又昂贵。SPEAR 把教师推理投影为领域符号 milestone，用 LCS-F1 给学生轨迹提供顺序敏感的稠密奖励。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现领域 milestone、顺序对齐与无神经 PRM 的稠密奖励。本地 milestone 使用候选过程/格式轴，不等同论文的自然语言符号抽取器。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.2812，神经 PRM 调用数为 0。  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-spear-64318b6a">SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning</h2>
<p class="ar-learning-card__meta">University of Pittsburgh · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>结果奖励过稀，神经 PRM 又昂贵。SPEAR 把教师推理投影为领域符号 milestone，用 LCS-F1 给学生轨迹提供顺序敏感的稠密奖励。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现领域 milestone、顺序对齐与无神经 PRM 的稠密奖励。本地 milestone 使用候选过程/格式轴，不等同论文的自然语言符号抽取器。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.2812，神经 PRM 调用数为 0。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26550">原论文</a> · <a href="../../../../post-training/2608.26550-spear/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning LLM 后训练 S-Lab, Nanyang Technological University 2026-08-26 把参考回答拆成视觉忠实度（VF）、推理一致性（RC）和指令遵循（IF）原子 rubric，并把可定位证据的信用分配到前缀，避免终局标量奖励掩盖局部幻觉。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2188（+75.00%）；只验证多维、prefix-localized candidate credit。  多模态 rubric RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-v-rubrics-b3920a4a">V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning</h2>
<p class="ar-learning-card__meta">S-Lab, Nanyang Technological University · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>把参考回答拆成视觉忠实度（VF）、推理一致性（RC）和指令遵循（IF）原子 rubric，并把可定位证据的信用分配到前缀，避免终局标量奖励掩盖局部幻觉。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2188（+75.00%）；只验证多维、prefix-localized candidate credit。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25580">原论文</a> · <a href="../../../../post-training/2608.25580-v-rubrics/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning LLM 后训练 Wuhan University 2026-08-24 长轨迹只给终局 reward 时，很难知道具体哪个 token/动作导致失败。SRPO 让当前模型先根据完整轨迹和环境结果写出简短 reflection patch，再把 patch 拼回原问题；同一个模型在这个特权上下文中充当教师，对学生的 on-policy rollout 给出逐 token 分数。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行反思 patch、reflection-conditioned teacher score 和稠密 advantage；没有把小型策略代理结果写成 Qwen3-8B 训练结果。本地策略代理用 outcome/process reward 构造同方向的反思稠密信用，没有运行 Qwen3-8B、WebShop、ALFWorld、SWE-Bench 或真实 token rollout。  反思式 token 信用 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-srpo-6cb8099c">SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning</h2>
<p class="ar-learning-card__meta">Wuhan University · 论文公开：2026-08-24</p>
<p><strong>方法要点：</strong>长轨迹只给终局 reward 时，很难知道具体哪个 token/动作导致失败。SRPO 让当前模型先根据完整轨迹和环境结果写出简短 reflection patch，再把 patch 拼回原问题；同一个模型在这个特权上下文中充当教师，对学生的 on-policy rollout 给出逐 token 分数。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行反思 patch、reflection-conditioned teacher score 和稠密 advantage；没有把小型策略代理结果写成 Qwen3-8B 训练结果。本地策略代理用 outcome/process reward 构造同方向的反思稠密信用，没有运行 Qwen3-8B、WebShop、ALFWorld、SWE-Bench 或真实 token rollout。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23493">原论文</a> · <a href="../../../../post-training/2608.23493-srpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization LLM 后训练 University of Florida 2026-08-17 逐 reward 维度标准化优势，并依据 batch 饱和度动态把梯度预算转移到尚未掌握的目标。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  多奖励 RL 稳定性 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-sa-mrpo-184fd311">Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization</h2>
<p class="ar-learning-card__meta">University of Florida · 论文公开：2026-08-17</p>
<p><strong>方法要点：</strong>逐 reward 维度标准化优势，并依据 batch 饱和度动态把梯度预算转移到尚未掌握的目标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16072">原论文</a> · <a href="../../../../post-training/2608.16072-sa-mrpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL LLM 后训练 Scale AI 2026-08-12 每个 rollout group 共享随机丢弃的 rubric 子集，使策略无法持续利用固定 judge proxy。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL reward hacking LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-rubric-dropout-0c8d1da7">Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL</h2>
<p class="ar-learning-card__meta">Scale AI · 论文公开：2026-08-12</p>
<p><strong>方法要点：</strong>每个 rollout group 共享随机丢弃的 rubric 子集，使策略无法持续利用固定 judge proxy。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11669">原论文</a> · <a href="../../../../post-training/2608.11669-rubric-dropout/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction LLM 后训练 Northeastern University 2026-08-06 主题：生成式奖励模型。生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。RRC 用组内自竞争排序和少量 anchor 排序构造中心化 reward。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的生成式奖励模型算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  生成式奖励模型 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-rrc-3d32cfb6">RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction</h2>
<p class="ar-learning-card__meta">Northeastern University · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>主题：生成式奖励模型。生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。RRC 用组内自竞争排序和少量 anchor 排序构造中心化 reward。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的生成式奖励模型算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06310">原论文</a> · <a href="../../../../post-training/2608.06310-rrc/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="ADRS LLM 后训练 University of Science and Technology of China 2026-08-04 privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 step 内中心化、return association、TVA gate 与原生 REINFORCE advantage 注入。  回报相关奖励塑形 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-adrs-2cc77780">ADRS</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-08-04</p>
<p><strong>方法要点：</strong>privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 step 内中心化、return association、TVA gate 与原生 REINFORCE advantage 注入。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03223">原论文</a> · <a href="../../../../post-training/2608.03223-adrs/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning LLM 后训练 Authors did not disclose affiliation 2026-07-29 让 Good–Normal–Bad 响应档案、query-specific rubrics 和 actor 策略形成三方闭环自进化。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL 测试时自进化 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-serpo-1bbe9fff">SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Authors did not disclose affiliation · 论文公开：2026-07-29</p>
<p><strong>方法要点：</strong>让 Good–Normal–Bad 响应档案、query-specific rubrics 和 actor 策略形成三方闭环自进化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26873">原论文</a> · <a href="../../../../post-training/2607.26873-serpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CoRT LLM 后训练 ByteDance internship 2026-07-28 对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。候选动作特征代理真实 token 序列；没有开放式生成、rubric judge 或大模型参数更新。在 GSM8K candidate-policy 上执行 rubric/criteria-free 两次反事实重放、归一化 token 权重和带符号 advantage 更新。  Token-level credit assignment LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-cort-3a4a9a75">CoRT</h2>
<p class="ar-learning-card__meta">ByteDance internship · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。候选动作特征代理真实 token 序列；没有开放式生成、rubric judge 或大模型参数更新。在 GSM8K candidate-policy 上执行 rubric/criteria-free 两次反事实重放、归一化 token 权重和带符号 advantage 更新。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25659">原论文</a> · <a href="../../../../post-training/2607.25659-cort/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Co-Evolving LLM Evaluators and Policies via DynamicRubric LLM 后训练 WeChat / Tencent 2026-07-22 固定 judge 或固定 rubric 会在策略模型进步后失去区分力。DynamicRubric 根据当前 prompt 和一组候选回答动态生成评估维度与权重，用 discriminability 目标寻找能区分当代 hard negatives 的标准，用 anchor 目标限制评估器漂移，再让 evaluator 和 policy 多轮协同进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行动态 rubric 和多轮共进化；Qwen3 与生产 judge 规模未复刻。公开 Alpaca 回答与确定性截断/重排候选构成可审计偏好集；代码实际执行 response-set conditioned 权重生成、四项 binary rubric、discriminability/anchor 双目标和 policy-induced hard-negative 共进化。  post-training reward-model evaluator co-evolution LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-dynamic-rubric-5fe56c96">Co-Evolving LLM Evaluators and Policies via DynamicRubric</h2>
<p class="ar-learning-card__meta">WeChat / Tencent · 论文公开：2026-07-22</p>
<p><strong>方法要点：</strong>固定 judge 或固定 rubric 会在策略模型进步后失去区分力。DynamicRubric 根据当前 prompt 和一组候选回答动态生成评估维度与权重，用 discriminability 目标寻找能区分当代 hard negatives 的标准，用 anchor 目标限制评估器漂移，再让 evaluator 和 policy 多轮协同进化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行动态 rubric 和多轮共进化；Qwen3 与生产 judge 规模未复刻。公开 Alpaca 回答与确定性截断/重排候选构成可审计偏好集；代码实际执行 response-set conditioned 权重生成、四项 binary rubric、discriminability/anchor 双目标和 policy-induced hard-negative 共进化。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20083">原论文</a> · <a href="../../../../reproductions/2607.20083-dynamic-rubric/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TCR LLM 后训练 论文未列机构 2026-07-22 只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。 保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；过程 verifier 是可控信号，不等同于论文的真实模型推理评审器。当前不包含真实自由生成、模型生成 checklist 或论文规模训练。结果只支持残差过程奖励机制在候选策略上的有效性，不能作为对论文五模型实验的数值复刻。本地 checklist verifier 为候选推理生成可控噪声过程得分；  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-tcr-a5ef9cee">TCR</h2>
<p class="ar-learning-card__meta">论文未列机构 · 论文公开：2026-07-22</p>
<p><strong>方法要点：</strong>只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；过程 verifier 是可控信号，不等同于论文的真实模型推理评审器。当前不包含真实自由生成、模型生成 checklist 或论文规模训练。结果只支持残差过程奖励机制在候选策略上的有效性，不能作为对论文五模型实验的数值复刻。本地 checklist verifier 为候选推理生成可控噪声过程得分；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19824">原论文</a> · <a href="../../../../post-training/2607.19824-tcr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TACO LLM 后训练 Johns Hopkins University 2026-07-08 整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作而非逐 token CoT，无法复刻论文的上下文 tail-risk predictor，只验证信用校准方向。以 rollout 概率的 surprisal 代理 tail risk，正 advantage 的 tail 样本会被连续降权，负 advantage 不会被 mask。  Token 信用校准 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-taco-d0adf0d1">TACO</h2>
<p class="ar-learning-card__meta">Johns Hopkins University · 论文公开：2026-07-08</p>
<p><strong>方法要点：</strong>整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作而非逐 token CoT，无法复刻论文的上下文 tail-risk predictor，只验证信用校准方向。以 rollout 概率的 surprisal 代理 tail risk，正 advantage 的 tail 样本会被连续降权，负 advantage 不会被 mask。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.07976">原论文</a> · <a href="../../../../post-training/2607.07976-taco/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="INTUITOR LLM 后训练 University of California, Berkeley 2025-05-26 把答案分布相对均匀分布的 KL 作为 intrinsic self-certainty reward，在没有答案和 verifier 时优化。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.2344（+0.00%）；奖励、KL、长度和候选预算一致。  自置信奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-intuitor-7b64d1c3">INTUITOR</h2>
<p class="ar-learning-card__meta">University of California, Berkeley · 论文公开：2025-05-26</p>
<p><strong>方法要点：</strong>把答案分布相对均匀分布的 KL 作为 intrinsic self-certainty reward，在没有答案和 verifier 时优化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.2344（+0.00%）；奖励、KL、长度和候选预算一致。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.19590">原论文</a> · <a href="../../../../post-training/2505.19590-intuitor/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SCAR: Shapley Credit Assignment for More Efficient RLHF LLM 后训练 McGill University 2025-05-26 原文Sec.3.2–3.4 Eq.3–6：外部冻结RM对原顺序、未入选位置填空格的文本coalition评分，v(empty)=0；Shapley必须保留负贡献，span credit只给该span末token。完整论文用自适应分段和SHAP/Owen近似。这里只保真实现N&lt;=10的完整coalition精确式及gamma=1的奖励散布；不把未指定解析器、Owen层次结构或合成RM冒充原系统。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 exact_shapley 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与信用分配 Shapley token/span credit LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-scar-shapley-credit-01c57925">SCAR: Shapley Credit Assignment for More Efficient RLHF</h2>
<p class="ar-learning-card__meta">McGill University · 论文公开：2025-05-26</p>
<p><strong>方法要点：</strong>原文Sec.3.2–3.4 Eq.3–6：外部冻结RM对原顺序、未入选位置填空格的文本coalition评分，v(empty)=0；Shapley必须保留负贡献，span credit只给该span末token。完整论文用自适应分段和SHAP/Owen近似。这里只保真实现N&lt;=10的完整coalition精确式及gamma=1的奖励散布；不把未指定解析器、Owen层次结构或合成RM冒充原系统。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 exact_shapley 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.20417v1">原论文</a> · <a href="../../../../post-training/2505.20417-scar-shapley-credit/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Math-Shepherd LLM 后训练 Peking University 2023-12-14 从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自动过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-math-shepherd-cc3174ec">Math-Shepherd</h2>
<p class="ar-learning-card__meta">Peking University · 论文公开：2023-12-14</p>
<p><strong>方法要点：</strong>从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.08935">原论文</a> · <a href="../../../../post-training/2312.08935-math-shepherd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Let&#x27;s Verify Step by Step LLM 后训练 OpenAI 2023-05-31 逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5781（+146.67%）；奖励、KL、长度和候选预算一致。  过程监督 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<h2 id="paper-post-training-process-supervision-e0dd1357">Let&#x27;s Verify Step by Step</h2>
<p class="ar-learning-card__meta">OpenAI · 论文公开：2023-05-31</p>
<p><strong>方法要点：</strong>逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5781（+146.67%）；奖励、KL、长度和候选预算一致。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.20050">原论文</a> · <a href="../../../../post-training/2305.20050-process-supervision/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
