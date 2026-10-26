---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 奖励与信用：正确结果该奖励哪些步骤

[LLM 后训练](index.md) / 36 个问题 · 36 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">36 个问题 · 36 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mart-grpo" data-paper-title="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning LLM 后训练 The University of Hong Kong 2026-10-23 一次机器人最终失败，不等于每个动作都导致失败；全轨迹负优势还会惩罚有价值的重抓和恢复尝试。MART-GRPO 用冻结事件 VLM 回看完整失败轨迹，定位最后一次未恢复错误，只保留截止该边界的失败反馈；成功轨迹、原组优势和原始 token 分母不变。论文先分析理想 stopping-time 条件下，何时删除零条件期望的后续梯度可以保持估计器期望；实际回溯 VLM 不自动满足这些理论条件。VLM 用三路同步摄像头、机器人状态、任务与帧/动作 chunk 对齐信息，报告最后一次可见且未恢复的错误起始区间； 这超过单张 A100/A30 或 Mac 的合理迭代预算，完整 actor/VLM 训练和机器人多任务评测为成本过高，不复现（审查 DONE）；诊断真实反传合成 logits，用独立概率空间 Eq.15 参考检查值与梯度、原分母、失败后缀零梯度和成功项保留；本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  策略优化 时序信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MART-GRPO屏蔽最后未恢复错误之后的惩罚，为什么不重新算组优势或有效token分母？ 它过滤的是失败反馈作用的位置，保持原始组奖励、优势和归一化才能隔离这一机制；改分母会额外放大保留前缀。轨迹先完整执行，事件模型再回溯边界，并非提前终止环境。回溯VLM也不自动满足理想停止时刻理论，必须区分经验启发与保证。 教学例子：机器人失手后做了无关停留，可屏蔽停留的负信用；但不能把剩余动作数量缩小后再把同一失败惩罚额外放大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-mart-grpo-1903b786" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mge-po" data-paper-title="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning LLM 后训练 论文未列机构（不据邮箱域名推断） 2026-10-16 GRPO会给同题、同正确性的回答相同 advantage，忽略生成的不确定性。MGE-PO 用生成时缓存的 token 熵区分回答，在成功／失败与高熵／低熵四象限上调整信用；再用在线题目熵统计安排课程，并以熵加权参考KL约束优化。原文 §4及附录B 原图建议：Figure 1 方法总览，不能把熵阈值示意图当成本地实验结果。 仅收录，成本过高，不复现（审查 DONE）。仅收录，成本过高，不复现（审查 DONE）。无本地实现、指标或能力比较，不进入 Evolve；该终态不阻塞审查水位。成本过高，不复现（审查 DONE）。原实验硬件为2×H200 141GB，完整单次MGE-PO记录约22.6小时，另有Math-7B-Instruct约22.8小时；该计时表的base setting没有单独checkpoint标识，不能强指为8B配置。8B训练另报告624次更新、8epochs、每题8条最长20,480 token回答；Qwen2.5系列使用17,398题和约12k生成上限。附录C与D.8  RLVR 熵与训练稳定性 过程奖励与信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MGE-PO为什么使用生成时缓存的token熵，而不在更新后重算当前策略熵来分配信用？ 信用要描述采样该回答时的不确定性，更新后重算会把策略变化混入原轨迹评价。方法结合正确性与高低熵四象限修正优势，并另有课程和KL权重。截断响应直接修正为零，也不意味着批内重新中心化后最终优势必为零，几个步骤不能混为一项。 教学例子：同一回答更新后变得更确定，不能倒过来说它采样时就毫不犹豫；信用依据应固定在原生成分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-mge-po-5743f3b7" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:diverge-ideation" data-paper-title="Training Reasoning Models to Generate Diverse Scientific Ideas" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Training Reasoning Models to Generate Diverse Scientific Ideas LLM 后训练 New York University 2026-10-15 独立采样多个高分想法可能反复得到同一个方向。论文让模型在一次生成中写出整组想法，每个新想法都能看到前面写过的内容，再按整组质量和相互差异训练。每张卡包含 problem gap、core claim、method、inspiration；质量由与 gold idea 的影响力比较提供，语义距离由三个被评字段的 judge 结果等权平均。不是用字符串不同就代表科研创新。原文 §2–3 原图建议 Figure 1：训练流程； 完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。固定诊断、不可晋级、未接 Evolve。L1 CPU reward/evaluation protocol 接口，不是科学创意模型复现。不伪造 SciJudge 或语义距离；完整实验成本过高，不复现（审查 DONE），不进入 Evolve 晋级。CPU runner每 seed构造12组明确标为 synthetic 的 judge 观测：双顺序Boolean赢票，以及三个字段的归一化距离。它们用于检验协议，不来自 SciJudge、LLM或真实科研评价。回调接口可替换为用户明确配置的 judge；  RLHF / RLVR 多样性与科学发现 奖励与评测协议 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 DIVERGE训练为何按想法生成顺序计差异，不能照评测那样重排后再算？ 训练中每个新想法看到已有前驱，最近前驱距离对应实际生成过程；事后重排会改变哪个想法先出现及其信用。评测的折扣重排指标与训练奖励是不同定义，不能互换。质量比较与语义距离还依赖独立judge，字符串不同并不证明科学创新。 教学例子：先提出方法甲，再提出甲的改写，后者应因重复少得差异信用；不能重排成一个看起来更丰富的顺序来改写训练奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-diverge-ideation-5eb53208" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:knowgpo" data-paper-title="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents LLM 后训练 Zhejiang University 2026-10-15 不同搜索轨迹即使读到了相同事实，也可能使用完全不同的 query、网页和表述，按表面观察匹配会把可比较的步骤拆散。KnowGPO 将问题所需事实拆为原子条件，训练 verifier 检查每步获得了哪些条件。状态是已验证条件的单调集合；从相同知识前态出发的动作互相比较新增知识，再与最终回答的奖励共同更新策略。原文 §3与附录A 原图建议：Figure 2 方法总览，左侧为训练知识条件构建，右侧为分组与信用；这不表示本地实现了左侧 LLM 标注流程。 完整实验成本过高，不复现（审查 DONE）；L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。L1 定义性算法组件／梯度诊断，不是搜索 Agent 能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 Evolve 晋级。随机初始化16词表、8维因果策略，每个问题采样6条三步轨迹，前两步为搜索、最后一步为 answer。公开输入只有题目 token、自己生成的动作和外部文档 ID；私有条件表与训练 outcome 只在 actor 调用外使用。精确小环境 verifier 不是自然语言 LLM verifier，不提供真实搜索能力。  Agentic RL 过程奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 KnowGPO为什么按动作前的知识集合分组，不能按动作后状态分组？ 要比较从相同已知条件出发的不同动作，前态才提供共同起点；用后态分组会把动作带来的信息增益提前作为分组条件。训练verifier将事实条件单调累积，再把过程与终局优势结合，只广播到生成token，不能把隐藏条件清单交给actor。 教学例子：两次搜索从相同证据出发，一次补到关键事实、一次没有；按结果知识分组会先把它们拆开，反而无法比较动作收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-knowgpo-346974ee" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mrtpo" data-paper-title="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL LLM 后训练 University of Minnesota 2026-10-15 GDPO 虽然分别归一化多种奖励，但仍把每种奖励均摊到整条响应。SQL 可执行性、格式、执行结果可能只分别依赖少数 token。MRTPO 用采样时的冻结策略重放响应：先提供所有 verifier 信息，再逐个删除奖励信息块。某个块被移除后，哪些位置的预测变化更大，就把该奖励更多地分配给哪些位置；正负 advantage 都使用相同的相关性权重。原文 §4 原文关键图：Figure 1/3 展示格式、可执行性和执行错误分别影响的 SQL token；见方法与图注。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。L1 算法组件／梯度诊断，不是 SQL、指令遵循或工具能力复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机初始化32词表策略真实生成响应，两种人工 verifier 只产生 token 条件奖励。冻结快照在完整信息和两个留一上下文下重新评分相同响应前缀；学生原始采样、更新评分均不接收 verifier 块。每个 seed 默认3次真实梯度更新，不使用 SQL、BFCL 或预训练 LLM。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 MRTPO逐个删除奖励信息块重放响应，为什么比较的是全词表JS而非采样token概率差？ 单个已采样词的变化可能漏掉其他候选之间的重分配，全词表差异更完整地表示某类奖励信息影响哪些位置。相关性权重在响应内保均值，正负信用都按相同规则分配，并限制重分配幅度。verifier信息只供训练重放，不能泄漏到学生原始采样。 教学例子：删除SQL格式反馈后，模型可能把概率从逗号转到括号，采样出的词概率恰好不变；只看该词会漏掉真实分布变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-mrtpo-6e178dc9" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opcredit" data-paper-title="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering LLM 后训练 Nanjing University 2026-10-15 整条轨迹失败不代表每一步都无用，成功轨迹也可能绕路。OpCredit 的 BOC 从普通 rollout 中复用分支结果：同题、同活动实体，再匹配访问集合、剩余预算和决策阶段；FTC 则衡量该操作局部前沿相对答案邻域的进退。两种信用对齐同一段推理及可执行操作 token，不给工具观察记策略损失。原文 §3、附录D 原文完整实验成本过高，不复现（审查 DONE）；这些是公式及梯度诊断，不是 KGQA 能力比较。L1 信用分配与梯度组件，不是 CWQ/WebQSP/GrailQA 能力复现。原文完整实验成本过高，不复现（审查 DONE）；本地 gold 只供训练后信用计算，不进入 Actor 输入或 evolve 晋级。随机初始化4输入、3输出的小策略在两个固定微型图上，每题真实采样6条关系选择＋答案动作轨迹。gold 仅在 rollout 结束后计算终止奖励与邻域信用；公开状态白名单只有题目、活动实体、访问集合、预算、阶段和可见实体，不能传 gold 字段。  Agentic RL 操作级信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 OpCredit比较同一操作时，为什么还要匹配访问集合、剩余预算和决策阶段？ 同一活动实体不等于同一可决策状态，过去访问和剩余资源会改变操作价值。BOC复用匹配上下文的分支结果并按轨迹去重，FTC另用训练专属答案邻域衡量局部前沿改善。答案信息只参与训练信用，不能进入actor输入，工具观察也不承担策略损失。 教学例子：都站在同一知识节点，一个轨迹已查过邻居、另一个还没查；再次扩展的价值不同，不能只按节点名混组比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-opcredit-fae57ef0" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progress-reward" data-paper-title="Progress Reward Model for Reinforcement Learning via Large Language Models" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Progress Reward Model for Reinforcement Learning via Large Language Models LLM 后训练 Beihang University 2026-10-15 稀疏成功信号难以指导长程机器人控制。PRM4RL 让 LLM 给出子任务、当前子任务判定函数与进度势函数；将子任务语义作为状态先验，将相邻状态进度差作为低层 RL 的密集 reward。规划只需预先生成，而不是每个环境步重新调用 LLM。 完整机器人实验成本过高，不复现（审查 DONE）。L1 状态机、embedding 接口及 reward 机制诊断。L1 状态机、embedding 接口及 reward 机制诊断。这是 NeurIPS 2025 已发表成果于 2026-10-15 上传 arXiv，不能称为新提出的 2026 算法。完整机器人实验成本过高，不复现（审查 DONE）。本地 ProgressPlan 只接收调用者审阅过的 completion predicates、potential 与子任务名称，不执行上游或 LLM 返回的任意 Python。stage 从当前状态重新计算，可因抓取丢失等情况回退，不使用仅随时间递增的计数器。  过程奖励 后训练算法组件 PRM4RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 PRM4RL为什么把进度奖励写成折扣势函数差，时间截断又为何不能当真实终止？ 势函数差让相邻状态的进度贡献沿轨迹望远镜相消，剩下起点和终点项。真实终止需要正确吸收边界处理，才能避免终点势值额外改变目标；时间预算截断后任务可能仍继续，不能自动将势函数置零。子任务编码与奖励塑形也是两个独立接口。 教学例子：机器人接近目标时因计时结束，不能假装任务已经真正终止；若把此处势值清零，可能凭空给出错误的进度惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-progress-reward-e17dc6a6" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sif" data-paper-title="Learning to Reason with Selective Internal Feedback" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learning to Reason with Selective Internal Feedback LLM 后训练 Institute of Automation, Chinese Academy of Sciences 2026-10-15 平均 self-certainty 可以随错误置信一起增长。SIF 不把它当正确性标签，而是比较同一 prompt 内响应的排序 certainty profile：先按窗口比较投票，再按击败 peer 的比例给二元 reward，过滤不具资格的响应和同 reward 组。policy 与 KL 必须同时施加选择 mask。 完整实验成本过高，不复现（审查 DONE）。短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。L1 完整资格 / 投票 / 双 mask 公式组件。默认资格仍为 550 tokens；短在线更新单独标为缩窗诊断，不能当原文默认 SIF 训练。完整实验成本过高，不复现（审查 DONE）。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；train/validation/test byte 区间 80%/10%/10% 不相交，不按 heldout NLL 选超参。  自置信轨迹过滤 Self-certainty 选择性策略更新 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SIF为什么比较排序后的certainty窗口，而不把平均熵或高概率token当正确标签？ 平均确定性可能随错误自信一起上升，SIF使用均匀分布到策略的KL构成certainty profile，在合格同题回答间做窗口和peer两级比较。它不是token熵或采样词概率；不合格响应和同奖励组被过滤，policy与KL还必须使用同一选择mask。 教学例子：一条回答平均很自信，但只有少数位置贡献极端值；比较多个排序窗口，可与另一条分布较均匀的回答区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-sif-620fc6b5" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tag-reward-gating" data-paper-title="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense LLM 后训练 University of British Columbia 2026-10-15 正确性和简短、低时延等奖励相加时，容易获取的辅助奖励可能主导 GRPO：总奖励上涨，主要任务却变差。TAG 不是简单降低辅助权重，而是先从同一基线分别优化每个奖励，观察哪个探针对基线的分布漂移最小，再将该奖励选为 anchor。随后丢弃探针、从原基线重新联合训练，辅助信用只有在 anchor 满足时才生效。原文 §5 原文关键图：Figure 1：短而错误的奖励投机；Figure 4 展示 reverse KL 对新造模式的敏感性。它们不是本地训练结果。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是数学或代码能力复现。L1 算法组件／梯度诊断，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不参与 evolve 晋级。使用随机初始化的32词表、8维 causal cumulative-embedding 策略，不下载任何 checkpoint。两个奖励是人工 token 奇偶条件，不表示数学正确性。每个奖励从同一基线独立做3次更新，在另一组提示上由该探针真实采样并计算选举统计，然后从未变化的基线做3次门控更新。  RLHF / RLVR 多奖励与信用分配 后训练算法组件 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TAG选出anchor后为什么丢弃探针并从原基线重训，辅助奖励又何时生效？ 独立探针用于比较各奖励引起的分布漂移，选出最稳定的锚点，并非继续拿探针权重联合训练。重新从共同基线出发才能隔离选择机制；anchor不满足时辅助奖励不能单独给信用。探针轨迹须由探针自身采样，不能把KL方向悄悄换掉。 教学例子：简短回答很容易拿到辅助分，但答错时应被锚点门控挡住；不能靠越来越短，让总奖励上升却失去正确性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-tag-reward-gating-d0312c36" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rap-walk" data-paper-title="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO LLM 后训练 未确认（已读 arXiv HTML 未列机构） 2026-10-14 RAP-Walk 不把成对视频偏好压成相互独立的胜率，而保留对手身份、循环关系和边清晰度。它在从输者到赢家的可靠随机游走中计算平稳偏好信用，经最低熵校准后修正原始胜率优势，最后仍交给同一 GRPO 更新。偏好循环并不自动表示视频质量差；可能是不同视频各擅长提示遵循、画面或运动。该方法把局部不一致当作传播可靠性线索，而不是删除循环或把循环直接写成负奖励。 完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。L1 图算子与策略更新接口。默认小图是显式机制诊断，未生成视频、未调用视频评审模型。完整 Wan 训练与大型 VLM 评估成本过高，不复现（审查 DONE）。不提供输入时，产物明确标为 explicit_mechanism_fixtures，只验证图方向、循环、校准和可微 GRPO 更新接口。可通过 --input-path observed-graphs.json 提供已有真实评审概率：  偏好图信用分配 GRPO 视频后训练 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 偏好出现循环时，RAP-Walk为什么不直接删除循环或把循环节点判成坏样本？ 循环可能来自不同视频各擅长不同维度，并不自动说明质量差。方法保留对手身份、边清晰度和循环不一致，构造从输者到赢家的可靠传播，再用平稳信用修正胜率优势。方向、收敛与熵校准都属于机制，不能随意换成普通PageRank。 教学例子：甲胜乙、乙胜丙、丙又胜甲，可能分别在画面、运动和遵循提示上占优；简单删掉三者会丢失有用比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-rap-walk-742b8b38" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:soar" data-paper-title="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents LLM 后训练 Zhejiang University / Microsoft 2026-10-09 只按答案奖训练的search agent可能答对却伪造证据依赖。SOAR独立记录atomic query的internal recall和external retrieval，再要求显式声明source。internal recall不接收旧reasoning或external evidence；来源一致性、正确性与格式reward训练真实策略。 本轮SOAR队列使用明确派生的工具文档属性QA训练诊断，不在不匹配的WikiText+GSM上宣称知识QA效果。本地对照口径：基线为相同source-aware工作流的without-source-reward消融；另有冻结初始策略；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Source-aware RL Search agents Source-consistency reward LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SOAR为什么只用回答声明的证据stream判来源一致性，另一stream碰巧含答案也不能给奖？ 来源声明应与真正支持答案的证据对应，否则模型可答对却编造依赖。独立内部回忆与外部检索后，校验只查看声明的stream，避免另一侧泄漏替它兜底。内部回忆不能先读外部证据或旧推理，工具观察也不作为可训练的生成动作token。 教学例子：答案声称来自检索网页，但事实其实只在模型内部回忆中出现；不能因另一stream有正确事实就判引用一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-soar-c6475aad" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:upturn" data-paper-title="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction LLM 后训练 KAIST 2026-10-09 冻结reasoner和小causal encoder，只学习paragraph boundary处的MLP cut policy。真实失败rollout在不同cut被冻结reasoner重新生成，给rescue奖励。推理时独立learned gate决定纠错；保留prefix、结束assistant turn、插固定新user turn，按剩余response预算生成suffix。 本页不声明未执行实验已经完成。本地对照口径：基线为Base@2N完整rollout，对照UPTURN@N及至多N次替换；预算匹配为最大允许生成数，不等于实际耗时一致；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Self-correction Frozen causal encoder Learned cut policy LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 UPTURN为什么学习段落边界上的cut，而不是直接微调整个reasoner？ 冻结reasoner后，学习对象集中到何时插入纠错轮次，救援回报来自不同cut后的真实重新生成。保留前缀、结束当前轮并插固定新用户轮，再按剩余预算生成后缀，与整段重写或参数级推理训练不同。推理gate必须独立决定，不能由gold答案触发。 教学例子：推导在某段开始偏离，可在该段边界发起一次重新考虑；前文保留，后续预算减少，不能把这次救援当成无限免费重试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-upturn-1713cc09" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:residual-advantage" data-paper-title="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards LLM 后训练 Harbin Engineering University / Tencent / Harbin Institute of Technology 2026-10-08 把全词表师生概率残差变成相对学生的有界局部优势，再逐响应中心化，与验证器优势相加。Co-RA 在同一已评分学生批次上更新教师 LoRA，下一轮才使用新教师。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Teacher guidance LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Residual Advantage为什么减去学生分布下的残差期望，再做响应内中心化？ 师生概率差的原始值依赖学生当前覆盖，减去学生期望后才得到相对学生的局部优势，响应中心化再分离位置差异。它与验证器优势相加而非取代真值信号。共同更新教师时先固定同一已评分批次，新教师只在下一轮使用，不能中途重标标签。 教学例子：教师对某词比学生更支持，但学生对许多替代词也有相近残差；需相对整体基线判断，而非看到差值为正就强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-residual-advantage-393aad16" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:carm" data-paper-title="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning LLM 后训练 Moore Threads AI 2026-10-01 对每个 token 的 current/rollout log-ratio 先取绝对值再平均，避免正负漂移在序列级几何均值中抵消。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 detached response gate；未训练 Qwen3.5。执行 detached response gate；未训练 Qwen3.5。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RLVR off-policy 响应掩码 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CARM为什么先对每个token的log-ratio取绝对值，再求响应平均？ 一处概率上升与另一处下降可能在普通序列平均中抵消，让整条响应看似没有漂移。先取绝对值保留偏移幅度，再用响应gate筛出累积失配大的样本。它衡量的是策略变化而非回答质量；gate应冻结，不能借选择过程反向改变筛选依据。 教学例子：前半句概率显著上升，后半句等幅下降，总log-ratio接近零；绝对偏移平均仍会发现这条响应变化很大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-carm-c2bacd93" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:my-fault" data-paper-title="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning LLM 后训练 Alibaba Group 2026-10-01 自诊断器提出错误类别与位置，只有经证据验证的 claim 才进入在线 error pricing；学得的相对成本把终局 credit 守恒地重分配到步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 信用分配 自诊断 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 My FAULT为什么要求自诊断claim先经证据验证，再进入error pricing？ 自诊断文本可能只是事后合理化，未经核对就估计错误成本会把偏见写进训练。验证后的类别与位置用于在线相对定价，再在步骤间重新分配终局信用，并保持总量守恒。它改变信用位置，不凭空创造成功奖励；本地没有联合训练完整诊断模型。 教学例子：失败后模型说“搜索错了”，但日志显示工具调用正确、最终汇总丢了事实；未经验证的归因不应指导搜索步骤受罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-my-fault-cefa1f11" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tvrl" data-paper-title="Token-Level Video Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Token-Level Video Reinforcement Learning LLM 后训练 原文首页未列第一作者机构 2026-10-01 冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度 credit 归一化；未训练视频扩散模型。执行梯度 credit 归一化；未训练视频扩散模型。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  视频生成 token credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 视频token对冻结VLM奖励的梯度较大，为什么只能理解为敏感度而非必然正确的信用？ 梯度描述当前奖励模型对局部变化的敏感程度，可用于把同组优势稠密分配给生成token；按均值归一化控制总尺度。但评分模型也可能依赖捷径，敏感位置不一定是真正因果要素。本地只检验信用归一化，没有训练视频模型或证明感知质量提升。 教学例子：奖励模型可能对画面角落标记特别敏感；即使其梯度很大，也不能直接断定修改该区域就是提高视频质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-tvrl-0c541634" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpo" data-paper-title="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning LLM 后训练 Georgia Institute of Technology 2026-09-30 用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 segment credit；未读取 gold plan，也未训练 7B Agent。执行 segment credit；未读取 gold plan，也未训练 7B Agent。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agentic RL segment credit GRPO LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SHARPO借同组成功轨迹重评segment，为什么仍用有界因子缩放原GRPO优势？ 成功轨迹为同一学生前缀提供额外教师上下文，segment内师生log-prob差反映局部支持差异。有界缩放限制这种自蒸馏信号对原优势的放大，不把教师评分直接变成无限新奖励。成功上下文仅用于训练评分，不是给推理Agent展示gold计划。 教学例子：同一失败轨迹中的检索段可能接近成功策略，而汇总段偏差较大；按segment调信用，比整条回答统一放大更细。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-sharpo-de267e69" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:t2spo" data-paper-title="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning LLM 后训练 Nanjing University 2026-09-30 用历史成功轨迹中的剩余步数训练上下文内距离估计器，预测每个状态距离成功还多远；把相邻状态的距离改善转为步骤优势，与轨迹级奖励共同优化。冻结 TabPFN 避免额外训练 critic，失败轨迹不被误标成接近成功的正样本。 尚未复现完整 LLM＋ALFWorld 训练。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。L1 核心机制诊断：实现真实冻结 TabPFN 距离预测、历史支持集、步骤信用和 token 裁剪目标。没有用启发式回归器冒充 TabPFN；尚未复现完整 LLM＋ALFWorld 训练。本地预动作输入是公开合成数值状态，不是冻结文本 encoder；完整 ALFWorld/WebShop rollout、文本编码器和 LLM 参数更新未完成。TabPFN MAE 不是任务成功率；没有 CUDA 完整训练或正式 Evolve 接入。  轨迹到步骤信用分配 强化学习 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 T2SPO成功终止把后继距离置零，为什么失败终止却把步骤进展直接置零？ 成功终止确实到达目标，距离归零表示完成；失败结束只是无法继续，若同样当作到达成功，会制造虚假正进展。距离估计来自历史成功支持集，本轮先完成评分再更新历史，避免自我泄漏。时间截断还需按所用GRPO或PPO语义分别处理。 教学例子：代理因工具耗尽而退出，并不意味着离成功只差零步；若把退出统一当作成功终点，最后一个失败动作可能被错误奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-t2spo-3a6c006a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pact" data-paper-title="PACT: From Credit Assignment to Critic Alignment" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="PACT: From Credit Assignment to Critic Alignment LLM 后训练 AllSpark Team 2026-09-22 终局奖励只有一个标量，但 actor 要更新每个生成 token。论文在完整性、前缀一致性和中性三个条件下，刻画 token 的理论信用为相邻前缀的条件期望之差。实际训练无法精确知道这些期望，因此用概率 critic 估计前缀价值，令 token advantage 近似为 R − V(prefix)。论文的关键是顺序：critic 应逼近 actor 更新后的策略，而不是只拟合刚采样时的旧策略。实用版本用当前 token 的概率比 ρ_t，而非整个未来序列的比率乘积； 以真实自由生成轨迹验证 Actor-then-Critic、更新后策略的重要性校正与概率 critic；本地结果不是原论文大模型成绩。这验证了 PACT 的更新次序与损失路径，但没有复现 4B/35B checkpoint、agentic 工具环境、原文训练规模或原文基准成绩；应作为小模型机制证据，不据此宣称 LLM 能力提升。短预算训练中格式命中率仍为零；上述非零 exact accuracy 只有极少数样本，不能解释为稳定的能力改善。本地使用小型 GRU 因果语言模型、独立前缀 critic、无约束 token 自由生成与 exact-answer verifier。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 PACT为什么先更新actor再重算比率训练critic，soft target超过一时能直接clamp吗？ critic应逼近更新后的策略，因此用新旧actor的token概率比校正旧轨迹回报，再拟合对应目标。逐样本的比率乘奖励可能超过一，直接截断会改变目标，不能套用只接收标准概率标签的BCE接口。更新顺序和稳定softplus表达都属于机制。 教学例子：actor已更偏向某个成功动作，critic仍只拟合旧采样分布会滞后；概率比校正用于让旧结果服务新策略价值估计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-pact-439c5053" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tiao" data-paper-title="TIAO: Token Importance-Aware Policy Optimization for Text Summarization" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TIAO: Token Importance-Aware Policy Optimization for Text Summarization LLM 后训练 National University of Defense Technology 2026-09-15 通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。本地执行 token dependency 与双尺度 credit；未训练 7B 模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  强化学习 Token 信用分配 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TIAO遮蔽源文档后看token概率变化，为什么这比仅按回答长度分配信用更有针对性？ 摘要中不同token对原文证据的依赖不同，遮蔽前后的概率差提供这种依赖线索，再用于轨迹与token两层信用塑形。长度只能描述多少字，不能说明哪些内容依赖来源。但遮蔽也可能引入分布变化，因此依赖估计不能直接等同事实归因正确性。 教学例子：摘要里的日期依赖原文细节，而连接词可能不依赖；同样长度下，二者不应仅因位置相近就获得完全相同的证据信用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-tiao-f57cc707" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spear" data-paper-title="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning LLM 后训练 University of Pittsburgh 2026-08-27 结果奖励过稀，神经 PRM 又昂贵。SPEAR 把教师推理投影为领域符号 milestone，用 LCS-F1 给学生轨迹提供顺序敏感的稠密奖励。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现领域 milestone、顺序对齐与无神经 PRM 的稠密奖励。本地 milestone 使用候选过程/格式轴，不等同论文的自然语言符号抽取器。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.2812，神经 PRM 调用数为 0。  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SPEAR为什么用LCS-F1对齐符号milestone，而不只检查两条推理包含相同符号？ 相同步骤集合可能顺序不同，导致推理依赖被破坏。最长公共子序列保留相对顺序，配合精确率和召回率衡量遗漏与冗余，形成比单个终局分数更密集的信号。符号抽取本身仍可能出错，本地候选轴不能冒充原文自然语言抽取器。 教学例子：先代入条件再求解与先写结论再拼条件，可能含相同标记却有不同依赖；顺序敏感对齐可以区分这种结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-spear-64318b6a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:v-rubrics" data-paper-title="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning LLM 后训练 S-Lab, Nanyang Technological University 2026-08-26 把参考回答拆成视觉忠实度（VF）、推理一致性（RC）和指令遵循（IF）原子 rubric，并把可定位证据的信用分配到前缀，避免终局标量奖励掩盖局部幻觉。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2188（+75.00%）；只验证多维、prefix-localized candidate credit。  多模态 rubric RL LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 V-Rubrics为什么把视觉忠实、推理一致和指令遵循分开，而不只给整条回答一个总分？ 回答可能看图正确却推理跳步，也可能推理连贯却编造视觉细节。原子rubric区分这些来源，再把可定位的证据信用关联到前缀，减少终局标量掩盖局部幻觉。维度加权只是目标取舍，不能证明judge标签无误；本地候选轴并非真实视觉证据模型。 教学例子：回答遵守了输出格式，但把图中不存在的物体当作前提；格式分高不能替代视觉忠实度的单独检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-v-rubrics-b3920a4a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:srpo" data-paper-title="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning LLM 后训练 Wuhan University 2026-08-24 长轨迹只给终局 reward 时，很难知道具体哪个 token/动作导致失败。SRPO 让当前模型先根据完整轨迹和环境结果写出简短 reflection patch，再把 patch 拼回原问题；同一个模型在这个特权上下文中充当教师，对学生的 on-policy rollout 给出逐 token 分数。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行反思 patch、reflection-conditioned teacher score 和稠密 advantage；没有把小型策略代理结果写成 Qwen3-8B 训练结果。本地策略代理用 outcome/process reward 构造同方向的反思稠密信用，没有运行 Qwen3-8B、WebShop、ALFWorld、SWE-Bench 或真实 token rollout。  反思式 token 信用 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SRPO把失败后的reflection patch给同参数教师，为什么学生原始rollout前缀仍要保持不变？ patch是训练时事后得到的特权反馈，用来让教师重新评价学生实际走过的位置。若改写学生前缀或直接把patch给部署学生，就变成另一种采样或推理任务。逐token教师与旧学生log-ratio形成稠密信用，反思文本本身也不是经过独立证明的正确答案。 教学例子：学生先做错一个检索决策，任务结束后才知道遗漏约束；教师可借提醒评分这个旧决策，但不能假装学生当时已经知道。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-srpo-6cb8099c" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sa-mrpo" data-paper-title="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization LLM 后训练 University of Florida 2026-08-17 逐 reward 维度标准化优势，并依据 batch 饱和度动态把梯度预算转移到尚未掌握的目标。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  多奖励 RL 稳定性 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SA-MRPO为什么根据奖励饱和度调权，而不一直给所有目标相同权重？ 某些维度已被模型掌握后，继续分配同样更新预算可能挤占尚未掌握的目标。方法逐维标准化优势，再按饱和程度降低已学会目标的权重。饱和必须按明确统计口径估计，不等于高分维度从此永远无用，也不能混淆奖励量纲与真实掌握程度。 教学例子：格式目标几乎总通过，推理正确性仍不稳定；可减少格式维度的相对压力，但仍需监测它是否因训练其他目标而退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-sa-mrpo-184fd311" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rubric-dropout" data-paper-title="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL LLM 后训练 Scale AI 2026-08-12 每个 rollout group 共享随机丢弃的 rubric 子集，使策略无法持续利用固定 judge proxy。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL reward hacking LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Rubric Dropout为什么让同一个rollout组共享丢弃的rubric子集？ 同组响应需要在可比标准下形成相对奖励，共享子集能避免每个回答因随机评价规则不同而被误排序。跨组变化的rubric又使策略难以持续利用固定评分捷径。随机丢弃只是缓和特定reward hacking机制，不能保证余下标准可靠或主任务不会受损。 教学例子：比较两份答案时都暂时去掉“简短”标准，比一份按简短评分、另一份不按它评分，更能保持相对奖励可比。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-rubric-dropout-0c8d1da7" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rrc" data-paper-title="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction LLM 后训练 Northeastern University 2026-08-06 主题：生成式奖励模型。生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。RRC 用组内自竞争排序和少量 anchor 排序构造中心化 reward。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的生成式奖励模型算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  生成式奖励模型 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 RRC为什么把生成式奖励模型的组内排名与anchor排名结合，而不要求它逐条报绝对分数？ 生成式judge可能更擅长比较哪条更好，而绝对数值尺度不稳定。组内自竞争给相对位置，少量anchor提供跨组参照，再构造中心化奖励。排名仍依赖候选集合和judge质量，不能把相对第一解释为绝对正确，也不等于已经运行原文昂贵评审系统。 教学例子：两组答案各自都有第一名，但整体质量可能不同；加入固定参照可帮助判断两组的“第一”是否处在相近水平。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-rrc-3d32cfb6" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adrs" data-paper-title="ADRS" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="ADRS LLM 后训练 University of Science and Technology of China 2026-08-04 privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 step 内中心化、return association、TVA gate 与原生 REINFORCE advantage 注入。  回报相关奖励塑形 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 ADRS为什么先检查教师置信与实际回报的相关性，再使用教师token信号？ 特权教师越自信不必然意味着任务越成功，直接灌入可能放大错误。ADRS在交互步内标准化教师分数，用与实际回报的正相关形成门控，再进入原奖励到优势路径。负相关不应被当正向帮助，推理时也不依赖训练专属技能或结果信息。 教学例子：某一步教师总偏爱流畅但无效的工具调用，而真实回报更低；相关性门控应限制这种自信信号进入策略更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-adrs-2cc77780" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:serpo" data-paper-title="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning LLM 后训练 Authors did not disclose affiliation 2026-07-29 让 Good–Normal–Bad 响应档案、query-specific rubrics 和 actor 策略形成三方闭环自进化。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  Rubric RL 测试时自进化 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SERPO同时更新响应档案、rubric和actor，为什么必须区分这三者的作用？ Good–Normal–Bad档案提供经验比较，题目特定rubric决定当轮评价标准，actor才负责生成行为。三方闭环允许标准随策略改变，但也可能互相强化偏差。更新档案不等于训练模型，生成新rubric也不证明质量提高；需要独立留出评估避免自评自证。 教学例子：旧档案只收录短答案，rubric逐渐偏爱简短，actor随之缩短；三者彼此一致仍可能同时忽略任务事实正确性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-serpo-1bbe9fff" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cort" data-paper-title="CoRT" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="CoRT LLM 后训练 ByteDance internship 2026-07-28 对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。候选动作特征代理真实 token 序列；没有开放式生成、rubric judge 或大模型参数更新。在 GSM8K candidate-policy 上执行 rubric/criteria-free 两次反事实重放、归一化 token 权重和带符号 advantage 更新。  Token-level credit assignment LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 CoRT为什么在有无rubric的上下文中重放同一响应，而不是各自重新生成后比较？ 重放同一前缀和token能把似然差更多归于rubric条件变化；重新生成会同时改变轨迹，难以定位哪些位置受标准影响。差异用于重分配原响应级优势，而非把评分文本直接输入部署学生。反事实上下文也可能产生偏差，不能把权重等同真实因果贡献。 教学例子：同一句答案在加入“需引用来源”后，引用位置概率变化较大；若另一边重新生成整段，差异就不只来自评价条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-cort-3a4a9a75" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dynamic-rubric" data-paper-title="Co-Evolving LLM Evaluators and Policies via DynamicRubric" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Co-Evolving LLM Evaluators and Policies via DynamicRubric LLM 后训练 WeChat / Tencent 2026-07-22 固定 judge 或固定 rubric 会在策略模型进步后失去区分力。DynamicRubric 根据当前 prompt 和一组候选回答动态生成评估维度与权重，用 discriminability 目标寻找能区分当代 hard negatives 的标准，用 anchor 目标限制评估器漂移，再让 evaluator 和 policy 多轮协同进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行动态 rubric 和多轮共进化；Qwen3 与生产 judge 规模未复刻。公开 Alpaca 回答与确定性截断/重排候选构成可审计偏好集；代码实际执行 response-set conditioned 权重生成、四项 binary rubric、discriminability/anchor 双目标和 policy-induced hard-negative 共进化。  post-training reward-model evaluator co-evolution LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 DynamicRubric为什么既要求区分当前hard negatives，又用anchor限制评估器漂移？ 固定标准可能随着策略进步失去区分力，动态维度和权重帮助识别新难例；若只追求可区分，评估器也可能学到任意风格捷径。anchor提供相对稳定的参照，约束评价标准改变。共同进化不等于客观真值同步改善，仍需独立任务验证。 教学例子：所有回答都已格式正确，旧格式rubric难再区分；新增标准若只偏爱更长措辞，也需被锚点评价约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-dynamic-rubric-5fe56c96" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tcr" data-paper-title="TCR" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TCR LLM 后训练 论文未列机构 2026-07-22 只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。 保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；保真度：本地实现样本级 checklist、outcome EMA 和 thinking surplus；过程 verifier 是可控信号，不等同于论文的真实模型推理评审器。当前不包含真实自由生成、模型生成 checklist 或论文规模训练。结果只支持残差过程奖励机制在候选策略上的有效性，不能作为对论文五模型实验的数值复刻。本地 checklist verifier 为候选推理生成可控噪声过程得分；  过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TCR为什么从过程奖励里减去outcome的滑动基线，而不直接把两项相加？ 过程分与最终正确性常高度相关，直接相加可能把同一个成功信号重复奖励。残差项试图保留结果尚未解释的思考增益，并随训练状态更新参照。它依赖checklist质量和基线口径，不意味着过程残差必是真实推理质量，本地候选验证也不能外推完整模型。 教学例子：答对的回答几乎总获得高过程分，简单求和会重复计分；关注超出通常结果水平的过程改善，才有额外信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-tcr-a5ef9cee" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:taco" data-paper-title="TACO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="TACO LLM 后训练 Johns Hopkins University 2026-07-08 整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作而非逐 token CoT，无法复刻论文的上下文 tail-risk predictor，只验证信用校准方向。以 rollout 概率的 surprisal 代理 tail risk，正 advantage 的 tail 样本会被连续降权，负 advantage 不会被 mask。  Token 信用校准 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 TACO为什么只降低高tail-risk token的正信用，而不把负信用一起减弱？ 正确整句可能夹有不合理的低概率步骤，统一正优势会把它们也强化。TACO平滑削弱这类位置的正信用，同时保留负信用，避免对坏轨迹的抑制也被一并取消。tail risk依赖局部上下文，不是凡低概率就错误，本地也未复现真实token风险预测器。 教学例子：答案碰巧正确，但中间有一次无根据猜测；可减少对猜测的奖励，而当整体失败时，不应顺便免除它的负向反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-taco-d0adf0d1" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:intuitor" data-paper-title="INTUITOR" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="INTUITOR LLM 后训练 University of California, Berkeley 2025-05-26 以每个生成前缀下的全词表 next-token 分布计算，再沿回答长度平均，作为 intrinsic self-certainty reward。方向是均匀分布到策略分布，并非策略的负熵；高置信度也不等于答案一定正确。 它既没有原文的逐 token 全词表计算，也使用了相反方向的 KL，因此仅为候选奖励更新诊断，尚未复现 Intuitor 的定义性 self-certainty。本地为候选分布机制诊断。本地为候选分布机制诊断。当前算子没有实现原文逐 token、全词表的 self-certainty；现有 mini-suite 不能作为该定义性奖励或原论文推理能力的验证。当前 p0_20260808.py 的 intuitor 分支以采样候选的 log p + log N 作为奖励，诊断量 intrinsic_kl_to_uniform 则是。  自置信奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 INTUITOR的self-certainty能直接换成负熵吗，KL方向为什么重要？ 原文self-certainty使用均匀分布到下一词分布的KL，即KL(U||p)，与KL(p||U)或负熵不同，对全词表低概率区域的敏感性也不同。本地采样候选log-ratio是另一种诊断，不能当成原文token级实现。内部置信提供学习线索，不意味着答案已经正确。 教学例子：两个分布最高概率相近，但一个给其他词极小概率；不同KL方向会以不同方式放大这种尾部差异，不能随意互换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-intuitor-7b64d1c3" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:scar-shapley-credit" data-paper-title="SCAR: Shapley Credit Assignment for More Efficient RLHF" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="SCAR: Shapley Credit Assignment for More Efficient RLHF LLM 后训练 McGill University 2025-05-26 原文Sec.3.2–3.4 Eq.3–6：外部冻结RM对原顺序、未入选位置填空格的文本coalition评分，v(empty)=0；Shapley必须保留负贡献，span credit只给该span末token。完整论文用自适应分段和SHAP/Owen近似。这里只保真实现N&lt;=10的完整coalition精确式及gamma=1的奖励散布；不把未指定解析器、Owen层次结构或合成RM冒充原系统。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 exact_shapley 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与信用分配 Shapley token/span credit LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 SCAR为什么保留负Shapley贡献，并只把span信用放在该段末token？ 某段文字可能降低冻结奖励模型对整体的评分，负贡献是合作价值分解的一部分，截零会破坏总量关系。span末token是其信用落点，与原顺序coalition构造共同定义奖励散布。总奖励等价还有折扣条件，局部精确枚举不能冒充大规模Owen近似或完整RLHF。 教学例子：一个多余段落引入矛盾，加入它使整体价值下降；若把这段负贡献清零，其他段落的信用总和就不再对应原奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-scar-shapley-credit-01c57925" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:math-shepherd" data-paper-title="Math-Shepherd" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Math-Shepherd LLM 后训练 Peking University 2023-12-14 从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自动过程奖励 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Math-Shepherd从中间步骤续写成功率造标签，为什么它不是对该步骤正确性的直接人工判定？ 续写衡量在给定策略和预算下从该前缀继续成功的可能性，受到后续求解能力影响。正确前缀也可能因续写差而得低分，错误前缀还可能被后续纠正。因此自动步骤标签是一种可达性信号，需要与人工正确性区分；金标只属于训练标注或独立评分侧。 教学例子：前两步都正确，模型却总在最后算错；从第二步续写的成功率低，并不能单凭这一点判第二步本身错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-math-shepherd-cc3174ec" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:process-supervision" data-paper-title="Let&#x27;s Verify Step by Step" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/reward-and-credit" data-search="Let&#x27;s Verify Step by Step LLM 后训练 OpenAI 2023-05-31 逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5781（+146.67%）；奖励、KL、长度和候选预算一致。  过程监督 LLM 后训练 奖励与信用：正确结果该奖励哪些步骤 Process Supervision为什么优先标注不确定步骤，而不只标最终答案是否正确？ 终局对错无法定位最先出现的错误，逐步标签能给奖励模型更细的监督。主动选择高不确定步骤把标注预算用在当前难分的位置，但不确定性并非错误概率的万能替身。还需控制候选与评测预算，本地机制夹具不代表已重建完整过程标注数据集。 教学例子：一份推导末尾错了，复核重点可放在模型最犹豫的关键变换，而不是重复标注已经非常明确的格式步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 奖励与信用：正确结果该奖励哪些步骤</a></p>
<span id="paper-post-training-process-supervision-e0dd1357" class="ar-learning-paper-anchor"></span>
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
