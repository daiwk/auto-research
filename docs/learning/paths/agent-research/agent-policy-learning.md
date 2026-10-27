---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 交互策略学习：把轨迹反馈变成更新

[Agent](index.md) / 212 个问题 · 53 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/agent-research/agent-policy-learning.md)

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
<p class="ar-learning-status" data-learning-status role="status">212 个问题 · 53 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frontier-opd" data-paper-title="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond Agent Tsinghua University 2026-10-23 同一个环境观测可能经不同历史反复到达，直接按访问次数或 token 数平均会让循环轨迹主导教师介入判断。Frontier-OPD 先在轨迹内、再在轨迹间聚合有符号师生分歧，对不同状态选原历史代表；教师桥与学生续跑须通过同长窗口比较后才接纳，状态共享不能替代真实历史或任务成功评测。排名只寻找值得试验的节点。教师最多接管回合，再让学生继续回合。新窗口必须和原历史从同一位置开始的回合窗口比较；只有成功重放、非终止交接、完整有效续跑且师生 agreement 不下降，桥的教师响应才加入训练。 成本过高，不复现（审查 DONE）。本地排名和接纳诊断不复现上述分数。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  Agentic OPD / rollout budgeting 学习前沿与教师桥 Agent 交互策略学习：把轨迹反馈变成更新 Frontier-OPD 为什么只在部分状态请教师接管，而不让教师生成所有训练轨迹？ 强教师的完整交互昂贵，而且直接模仿其顺利轨迹未必覆盖学生会卡住的位置。Frontier-OPD 从学生自己到达的状态寻找值得尝试教学的前沿，让教师短暂搭桥后交回学生；节省预算的同时还需验证这段教学是否真的适合学生续跑。 例如学生反复卡在找钥匙后的开门步骤，可针对该位置试一小段教师帮助，而不是每道题都由教师从头完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-frontier-opd-63269744" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4da2b7b9e7379237">Frontier-OPD 为什么只在部分状态请教师接管，而不让教师生成所有训练轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afrontier-opd">Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>强教师的完整交互昂贵，而且直接模仿其顺利轨迹未必覆盖学生会卡住的位置。Frontier-OPD 从学生自己到达的状态寻找值得尝试教学的前沿，让教师短暂搭桥后交回学生；节省预算的同时还需验证这段教学是否真的适合学生续跑。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生反复卡在找钥匙后的开门步骤，可针对该位置试一小段教师帮助，而不是每道题都由教师从头完成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32802v1">原论文</a> · <a href="../../../../agent-research/2610.32802-frontier-opd/">实现解读</a> · <a href="#qa-4da2b7b9e7379237">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frontier-opd" data-paper-title="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond Agent Tsinghua University 2026-10-23 同一个环境观测可能经不同历史反复到达，直接按访问次数或 token 数平均会让循环轨迹主导教师介入判断。Frontier-OPD 先在轨迹内、再在轨迹间聚合有符号师生分歧，对不同状态选原历史代表；教师桥与学生续跑须通过同长窗口比较后才接纳，状态共享不能替代真实历史或任务成功评测。排名只寻找值得试验的节点。教师最多接管回合，再让学生继续回合。新窗口必须和原历史从同一位置开始的回合窗口比较；只有成功重放、非终止交接、完整有效续跑且师生 agreement 不下降，桥的教师响应才加入训练。 成本过高，不复现（审查 DONE）。本地排名和接纳诊断不复现上述分数。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  Agentic OPD / rollout budgeting 学习前沿与教师桥 Agent 交互策略学习：把轨迹反馈变成更新 为什么先轨迹内再轨迹间平均师生分歧，不能按节点访问次数直接平均？ 循环轨迹会多次访问同一状态，若每次都算独立证据，频繁绕圈的一条路径就压过其他轨迹。两级平均先平衡轨迹权重，代表历史再用于真实教师桥试验；排名的有符号分歧与验证 agreement 也不同，节点高分不等于接管一定有益。 例如一条轨迹三次分歧十分，另一条一次零分，节点应是五分；直接按四次访问平均成七点五会放大循环影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-98ef87ac80ac6218">为什么先轨迹内再轨迹间平均师生分歧，不能按节点访问次数直接平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afrontier-opd">Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>循环轨迹会多次访问同一状态，若每次都算独立证据，频繁绕圈的一条路径就压过其他轨迹。两级平均先平衡轨迹权重，代表历史再用于真实教师桥试验；排名的有符号分歧与验证 agreement 也不同，节点高分不等于接管一定有益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条轨迹三次分歧十分，另一条一次零分，节点应是五分；直接按四次访问平均成七点五会放大循环影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32802v1">原论文</a> · <a href="../../../../agent-research/2610.32802-frontier-opd/">实现解读</a> · <a href="#qa-98ef87ac80ac6218">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frontier-opd" data-paper-title="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond Agent Tsinghua University 2026-10-23 同一个环境观测可能经不同历史反复到达，直接按访问次数或 token 数平均会让循环轨迹主导教师介入判断。Frontier-OPD 先在轨迹内、再在轨迹间聚合有符号师生分歧，对不同状态选原历史代表；教师桥与学生续跑须通过同长窗口比较后才接纳，状态共享不能替代真实历史或任务成功评测。排名只寻找值得试验的节点。教师最多接管回合，再让学生继续回合。新窗口必须和原历史从同一位置开始的回合窗口比较；只有成功重放、非终止交接、完整有效续跑且师生 agreement 不下降，桥的教师响应才加入训练。 成本过高，不复现（审查 DONE）。本地排名和接纳诊断不复现上述分数。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  Agentic OPD / rollout budgeting 学习前沿与教师桥 Agent 交互策略学习：把轨迹反馈变成更新 高分前沿节点与有效教师桥为什么不能用同一个判据确认？ 节点排名决定先把有限教师预算花在哪里，依据有符号师生分歧；桥验证则比较真实接管加学生续跑与原历史的同长窗口，要求有效重放和 agreement 不下降。前者是试验优先级，后者是训练数据准入，排名靠前本身不证明教学有效。 例如某状态分歧很大，但教师接管后学生仍无法继续，该位置可被优先试验，却不能因此直接把失败桥加入训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-538f695379155fc1">高分前沿节点与有效教师桥为什么不能用同一个判据确认？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afrontier-opd">Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>节点排名决定先把有限教师预算花在哪里，依据有符号师生分歧；桥验证则比较真实接管加学生续跑与原历史的同长窗口，要求有效重放和 agreement 不下降。前者是试验优先级，后者是训练数据准入，排名靠前本身不证明教学有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某状态分歧很大，但教师接管后学生仍无法继续，该位置可被优先试验，却不能因此直接把失败桥加入训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32802v1">原论文</a> · <a href="../../../../agent-research/2610.32802-frontier-opd/">实现解读</a> · <a href="#qa-538f695379155fc1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frontier-opd" data-paper-title="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond Agent Tsinghua University 2026-10-23 同一个环境观测可能经不同历史反复到达，直接按访问次数或 token 数平均会让循环轨迹主导教师介入判断。Frontier-OPD 先在轨迹内、再在轨迹间聚合有符号师生分歧，对不同状态选原历史代表；教师桥与学生续跑须通过同长窗口比较后才接纳，状态共享不能替代真实历史或任务成功评测。排名只寻找值得试验的节点。教师最多接管回合，再让学生继续回合。新窗口必须和原历史从同一位置开始的回合窗口比较；只有成功重放、非终止交接、完整有效续跑且师生 agreement 不下降，桥的教师响应才加入训练。 成本过高，不复现（审查 DONE）。本地排名和接纳诊断不复现上述分数。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  Agentic OPD / rollout budgeting 学习前沿与教师桥 Agent 交互策略学习：把轨迹反馈变成更新 桥实际少于 K 回合时怎样比较窗口，续跑能进训练池吗？ 比较实际桥长加 H 的新旧同长窗口，需有效重放、非终止交接和完整续跑，agreement 不下降才接纳桥响应。验证用的学生续跑不能进训练池，重复响应另需保留；当前只做 L1 数值协议，未实现训练器和完整经验池。 例如 K 上限二但教师只走一轮，就用一加 H 比较，不能拿更长旧窗口或把验证续跑也当教师示范训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c6a4f6a4fdc8378a">桥实际少于 K 回合时怎样比较窗口，续跑能进训练池吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afrontier-opd">Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>比较实际桥长加 H 的新旧同长窗口，需有效重放、非终止交接和完整续跑，agreement 不下降才接纳桥响应。验证用的学生续跑不能进训练池，重复响应另需保留；当前只做 L1 数值协议，未实现训练器和完整经验池。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 K 上限二但教师只走一轮，就用一加 H 比较，不能拿更长旧窗口或把验证续跑也当教师示范训练。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32802v1">原论文</a> · <a href="../../../../agent-research/2610.32802-frontier-opd/">实现解读</a> · <a href="#qa-c6a4f6a4fdc8378a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:asteroid" data-paper-title="Asymmetric On-Policy Distillation Learns In-Context Exploration" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Asymmetric On-Policy Distillation Learns In-Context Exploration Agent University of Washington 2026-10-21 部分可观测任务中，专家知道隐藏目标，因而总能直接成功；只模仿专家，学生看不到“失败后如何继续搜索”的上下文。ASTEROID 让当前学生先探索，再在同一个隐藏任务下收集专家的完整成功轨迹。学生用自己的观察、动作和奖励历史预测专家动作，迭代扩大可学习的上下文长度。这不是把金标放入 Agent prompt，也不是固定离线行为克隆，更不应简化成只在学生当前状态上打单步标签的普通 DAgger。论文区分两种采样：固定 latent 的 BAMDP 使用跨 episode 上下文； 完整多环境与机器人实验：成本过高，不复现（审查 DONE）；这是生成式机制诊断，没有公开 benchmark split，也没有 validation 选模、test 能力对比或 evolve 晋级。本地状态：L1 核心机制组件，diagnostic only。本地真实训练一个微型因果 Transformer，保留论文 Algorithm 1 的 episode 级在策略上下文与教师轨迹监督；不宣称复现论文的探索能力、样本效率或机器人效果。完整多环境与机器人实验：成本过高，不复现（审查 DONE）；不自动重试、不阻塞审查。  Agent 训练与策略优化 在策略上下文蒸馏与部分可观测探索 Agent 交互策略学习：把轨迹反馈变成更新 隐藏任务环境中，为什么只模仿专家成功路线可能不够应对学生真正遇到的状态？ 学生会尝试不成熟动作，看到的信息和进入的状态未必出现在专家的顺利路线中。ASTEROID 研究让学生探索与专家成功经验结合，使学习覆盖实际遭遇的不确定情况。探索必须来自可见交互，专家信息用于训练的范围也需隔离，不能在评测时直接透露隐藏任务或解法。 教学例：专家一开始就走对路，学生却先探索错门；只学成功开局并未告诉学生如何利用自己已观察到的失败信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-asteroid-1bdda102" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-98484c774b0b30a3">隐藏任务环境中，为什么只模仿专家成功路线可能不够应对学生真正遇到的状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aasteroid">Asymmetric On-Policy Distillation Learns In-Context Exploration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生会尝试不成熟动作，看到的信息和进入的状态未必出现在专家的顺利路线中。ASTEROID 研究让学生探索与专家成功经验结合，使学习覆盖实际遭遇的不确定情况。探索必须来自可见交互，专家信息用于训练的范围也需隔离，不能在评测时直接透露隐藏任务或解法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：专家一开始就走对路，学生却先探索错门；只学成功开局并未告诉学生如何利用自己已观察到的失败信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30105v1">原论文</a> · <a href="../../../../agent-research/2610.30105-asteroid/">实现解读</a> · <a href="#qa-98484c774b0b30a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:asteroid" data-paper-title="Asymmetric On-Policy Distillation Learns In-Context Exploration" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Asymmetric On-Policy Distillation Learns In-Context Exploration Agent University of Washington 2026-10-21 部分可观测任务中，专家知道隐藏目标，因而总能直接成功；只模仿专家，学生看不到“失败后如何继续搜索”的上下文。ASTEROID 让当前学生先探索，再在同一个隐藏任务下收集专家的完整成功轨迹。学生用自己的观察、动作和奖励历史预测专家动作，迭代扩大可学习的上下文长度。这不是把金标放入 Agent prompt，也不是固定离线行为克隆，更不应简化成只在学生当前状态上打单步标签的普通 DAgger。论文区分两种采样：固定 latent 的 BAMDP 使用跨 episode 上下文； 完整多环境与机器人实验：成本过高，不复现（审查 DONE）；这是生成式机制诊断，没有公开 benchmark split，也没有 validation 选模、test 能力对比或 evolve 晋级。本地状态：L1 核心机制组件，diagnostic only。本地真实训练一个微型因果 Transformer，保留论文 Algorithm 1 的 episode 级在策略上下文与教师轨迹监督；不宣称复现论文的探索能力、样本效率或机器人效果。完整多环境与机器人实验：成本过高，不复现（审查 DONE）；不自动重试、不阻塞审查。  Agent 训练与策略优化 在策略上下文蒸馏与部分可观测探索 Agent 交互策略学习：把轨迹反馈变成更新 为什么学生先探索，再学习同隐藏任务的专家完整成功轨迹，而不是只模仿开局专家？ 专家知道隐藏目标，直接成功的轨迹缺少失败后继续搜索的上下文。先收学生实际经历，再把这些历史作为专家动作预测的条件，训练其从观察与奖励中更新任务认识；部署时仍没有隐藏目标，学生探索动作也不能被自动当成正确监督标签。 例如学生先找错两个房间，再看到同任务专家如何找到目标，能学习从失败历史缩小范围，而非只记住专家开局直达路线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bf60456848f6e9e7">为什么学生先探索，再学习同隐藏任务的专家完整成功轨迹，而不是只模仿开局专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aasteroid">Asymmetric On-Policy Distillation Learns In-Context Exploration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>专家知道隐藏目标，直接成功的轨迹缺少失败后继续搜索的上下文。先收学生实际经历，再把这些历史作为专家动作预测的条件，训练其从观察与奖励中更新任务认识；部署时仍没有隐藏目标，学生探索动作也不能被自动当成正确监督标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生先找错两个房间，再看到同任务专家如何找到目标，能学习从失败历史缩小范围，而非只记住专家开局直达路线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30105v1">原论文</a> · <a href="../../../../agent-research/2610.30105-asteroid/">实现解读</a> · <a href="#qa-bf60456848f6e9e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:asteroid" data-paper-title="Asymmetric On-Policy Distillation Learns In-Context Exploration" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Asymmetric On-Policy Distillation Learns In-Context Exploration Agent University of Washington 2026-10-21 部分可观测任务中，专家知道隐藏目标，因而总能直接成功；只模仿专家，学生看不到“失败后如何继续搜索”的上下文。ASTEROID 让当前学生先探索，再在同一个隐藏任务下收集专家的完整成功轨迹。学生用自己的观察、动作和奖励历史预测专家动作，迭代扩大可学习的上下文长度。这不是把金标放入 Agent prompt，也不是固定离线行为克隆，更不应简化成只在学生当前状态上打单步标签的普通 DAgger。论文区分两种采样：固定 latent 的 BAMDP 使用跨 episode 上下文； 完整多环境与机器人实验：成本过高，不复现（审查 DONE）；这是生成式机制诊断，没有公开 benchmark split，也没有 validation 选模、test 能力对比或 evolve 晋级。本地状态：L1 核心机制组件，diagnostic only。本地真实训练一个微型因果 Transformer，保留论文 Algorithm 1 的 episode 级在策略上下文与教师轨迹监督；不宣称复现论文的探索能力、样本效率或机器人效果。完整多环境与机器人实验：成本过高，不复现（审查 DONE）；不自动重试、不阻塞审查。  Agent 训练与策略优化 在策略上下文蒸馏与部分可观测探索 Agent 交互策略学习：把轨迹反馈变成更新 BAMDP 跨 episode 条件与一般 POMDP takeover 为什么不能混为单步 DAgger？ 固定 latent 的 BAMDP 在多个 episode 积累任务知识，再配同任务专家 episode；一般 POMDP 从学生到达的中间状态接管。完整专家轨迹和上下文都重要，单步给当前动作标签会丢掉方法定义；部署也不能继续调用知道 latent 的专家。 例如隐藏门跨三次尝试不变时，第一轮失败可帮助下一轮；若每轮都换门，这种跨 episode 历史就不再提供同样知识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8ee47c30c993734e">BAMDP 跨 episode 条件与一般 POMDP takeover 为什么不能混为单步 DAgger？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aasteroid">Asymmetric On-Policy Distillation Learns In-Context Exploration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定 latent 的 BAMDP 在多个 episode 积累任务知识，再配同任务专家 episode；一般 POMDP 从学生到达的中间状态接管。完整专家轨迹和上下文都重要，单步给当前动作标签会丢掉方法定义；部署也不能继续调用知道 latent 的专家。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如隐藏门跨三次尝试不变时，第一轮失败可帮助下一轮；若每轮都换门，这种跨 episode 历史就不再提供同样知识。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30105v1">原论文</a> · <a href="../../../../agent-research/2610.30105-asteroid/">实现解读</a> · <a href="#qa-8ee47c30c993734e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:asteroid" data-paper-title="Asymmetric On-Policy Distillation Learns In-Context Exploration" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Asymmetric On-Policy Distillation Learns In-Context Exploration Agent University of Washington 2026-10-21 部分可观测任务中，专家知道隐藏目标，因而总能直接成功；只模仿专家，学生看不到“失败后如何继续搜索”的上下文。ASTEROID 让当前学生先探索，再在同一个隐藏任务下收集专家的完整成功轨迹。学生用自己的观察、动作和奖励历史预测专家动作，迭代扩大可学习的上下文长度。这不是把金标放入 Agent prompt，也不是固定离线行为克隆，更不应简化成只在学生当前状态上打单步标签的普通 DAgger。论文区分两种采样：固定 latent 的 BAMDP 使用跨 episode 上下文； 完整多环境与机器人实验：成本过高，不复现（审查 DONE）；这是生成式机制诊断，没有公开 benchmark split，也没有 validation 选模、test 能力对比或 evolve 晋级。本地状态：L1 核心机制组件，diagnostic only。本地真实训练一个微型因果 Transformer，保留论文 Algorithm 1 的 episode 级在策略上下文与教师轨迹监督；不宣称复现论文的探索能力、样本效率或机器人效果。完整多环境与机器人实验：成本过高，不复现（审查 DONE）；不自动重试、不阻塞审查。  Agent 训练与策略优化 在策略上下文蒸馏与部分可观测探索 Agent 交互策略学习：把轨迹反馈变成更新 本地单步三门诊断如何保留完整专家轨迹，又有哪些限制？ 每次选门本身是完整单步 episode，所以专家轨迹长度一是该环境边界，而非将多步方法普遍简化。真实小 Transformer 仅末端专家 query 监督，学生历史动作不当正确标签，部署从空历史不调专家；无一般 POMDP 或机器人能力比较。 例如学生错误尝试留在上下文供理解，但 loss 不要求重复这个错动作；正确专家动作仅作为训练目标分离保存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d1830851d2191bbd">本地单步三门诊断如何保留完整专家轨迹，又有哪些限制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aasteroid">Asymmetric On-Policy Distillation Learns In-Context Exploration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每次选门本身是完整单步 episode，所以专家轨迹长度一是该环境边界，而非将多步方法普遍简化。真实小 Transformer 仅末端专家 query 监督，学生历史动作不当正确标签，部署从空历史不调专家；无一般 POMDP 或机器人能力比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生错误尝试留在上下文供理解，但 loss 不要求重复这个错动作；正确专家动作仅作为训练目标分离保存。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、保留的定义机制与缩小边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30105v1">原论文</a> · <a href="../../../../agent-research/2610.30105-asteroid/">实现解读</a> · <a href="#qa-d1830851d2191bbd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsipo" data-paper-title="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution Agent Chinese University of Hong Kong 2026-10-11 静态或离线训练的技能库难以跟随策略进步，而技能增强教师也可能比学生更差。RSIPO从当前策略轨迹产生技能，以独立控制组与同初态重放测量技能收益，联合优化技能生成、RLVR和按经验贝叶斯可靠性加权的自蒸馏。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Table2：Qwen2.5-3B/7B、Qwen3-1.7B，150训练steps；ALFWorld每step16任务×8rollouts，最长50turns，每任务另4次初态重放与4096token技能生成；搜索每step128任务×8rollouts。之前还要GLM-5.2标注的技能SFT。多轮环境训练与教师评分在单卡预计长时间，未作本地测速；不下载或启动。  agentic-rl on-policy-self-distillation recursive-self-improvement Agent 交互策略学习：把轨迹反馈变成更新 策略不断变强时，RSIPO 为什么认为原有技能库也需要跟着更新？ 旧技能来自过去策略，可能已冗余、失效，甚至弱于当前学生的直接求解。RSIPO 研究让当前轨迹形成技能，再检验技能是否真的改善同初态执行，使技能与策略协同变化。技能辅助并非天然正收益，必须保留独立对照，也不能把原任务答案写进评测输入。 教学例：早期技能要求繁琐搜索，当前策略已能直接找到证据；继续强制使用旧技能可能更慢，需要重新测量而非盲目信任。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-rsipo-71b84017" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-28a01f8794a0c2d3">策略不断变强时，RSIPO 为什么认为原有技能库也需要跟着更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsipo">RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>旧技能来自过去策略，可能已冗余、失效，甚至弱于当前学生的直接求解。RSIPO 研究让当前轨迹形成技能，再检验技能是否真的改善同初态执行，使技能与策略协同变化。技能辅助并非天然正收益，必须保留独立对照，也不能把原任务答案写进评测输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：早期技能要求繁琐搜索，当前策略已能直接找到证据；继续强制使用旧技能可能更慢，需要重新测量而非盲目信任。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15772">原论文</a> · <a href="../../../../reproductions/2610.15772-rsipo/">实现解读</a> · <a href="#qa-28a01f8794a0c2d3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsipo" data-paper-title="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution Agent Chinese University of Hong Kong 2026-10-11 静态或离线训练的技能库难以跟随策略进步，而技能增强教师也可能比学生更差。RSIPO从当前策略轨迹产生技能，以独立控制组与同初态重放测量技能收益，联合优化技能生成、RLVR和按经验贝叶斯可靠性加权的自蒸馏。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Table2：Qwen2.5-3B/7B、Qwen3-1.7B，150训练steps；ALFWorld每step16任务×8rollouts，最长50turns，每任务另4次初态重放与4096token技能生成；搜索每step128任务×8rollouts。之前还要GLM-5.2标注的技能SFT。多轮环境训练与教师评分在单卡预计长时间，未作本地测速；不下载或启动。  agentic-rl on-policy-self-distillation recursive-self-improvement Agent 交互策略学习：把轨迹反馈变成更新 为什么技能增强教师的蒸馏权重，要依据收益可靠性收缩后再确定？ 技能可能无效甚至比学生更差，直接等权信任会把退化传回策略。独立控制与同初态重放估计效用差，再按观测噪声向组均值收缩，用较可靠收益调节蒸馏信任；技能奖励与收缩信任用途不同，失效重放也不能作为有效配对证据。 例如某技能只试一次碰巧成功，其收益不确定应被收缩；多次同初态对照都有效的技能，才更值得提高蒸馏权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9728e8966646598d">为什么技能增强教师的蒸馏权重，要依据收益可靠性收缩后再确定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsipo">RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>技能可能无效甚至比学生更差，直接等权信任会把退化传回策略。独立控制与同初态重放估计效用差，再按观测噪声向组均值收缩，用较可靠收益调节蒸馏信任；技能奖励与收缩信任用途不同，失效重放也不能作为有效配对证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某技能只试一次碰巧成功，其收益不确定应被收缩；多次同初态对照都有效的技能，才更值得提高蒸馏权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15772">原论文</a> · <a href="../../../../reproductions/2610.15772-rsipo/">实现解读</a> · <a href="#qa-9728e8966646598d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsipo" data-paper-title="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution Agent Chinese University of Hong Kong 2026-10-11 静态或离线训练的技能库难以跟随策略进步，而技能增强教师也可能比学生更差。RSIPO从当前策略轨迹产生技能，以独立控制组与同初态重放测量技能收益，联合优化技能生成、RLVR和按经验贝叶斯可靠性加权的自蒸馏。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Table2：Qwen2.5-3B/7B、Qwen3-1.7B，150训练steps；ALFWorld每step16任务×8rollouts，最长50turns，每任务另4次初态重放与4096token技能生成；搜索每step128任务×8rollouts。之前还要GLM-5.2标注的技能SFT。多轮环境训练与教师评分在单卡预计长时间，未作本地测速；不下载或启动。  agentic-rl on-policy-self-distillation recursive-self-improvement Agent 交互策略学习：把轨迹反馈变成更新 动态技能—策略协同更新，与固定离线技能库，在经验时效上有什么不同？ 固定库让检索条件较稳定，但技能来源停留在旧策略和旧任务；协同更新从当前策略轨迹构建技能，再用独立控制与同初态重放检查收益，可跟随能力变化。它也增加非平稳性和评估开销，不能把技能条目更新数量当成有效收益或可靠教师的证据。 教学例：策略学会更短的证据路径后，新技能可反映这条路径；固定旧库仍可能反复推荐已经过时的长流程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f6ffb006746e4a09">动态技能—策略协同更新，与固定离线技能库，在经验时效上有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsipo">RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定库让检索条件较稳定，但技能来源停留在旧策略和旧任务；协同更新从当前策略轨迹构建技能，再用独立控制与同初态重放检查收益，可跟随能力变化。它也增加非平稳性和评估开销，不能把技能条目更新数量当成有效收益或可靠教师的证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：策略学会更短的证据路径后，新技能可反映这条路径；固定旧库仍可能反复推荐已经过时的长流程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15772">原论文</a> · <a href="../../../../reproductions/2610.15772-rsipo/">实现解读</a> · <a href="#qa-f6ffb006746e4a09">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsipo" data-paper-title="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution Agent Chinese University of Hong Kong 2026-10-11 静态或离线训练的技能库难以跟随策略进步，而技能增强教师也可能比学生更差。RSIPO从当前策略轨迹产生技能，以独立控制组与同初态重放测量技能收益，联合优化技能生成、RLVR和按经验贝叶斯可靠性加权的自蒸馏。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Table2：Qwen2.5-3B/7B、Qwen3-1.7B，150训练steps；ALFWorld每step16任务×8rollouts，最长50turns，每任务另4次初态重放与4096token技能生成；搜索每step128任务×8rollouts。之前还要GLM-5.2标注的技能SFT。多轮环境训练与教师评分在单卡预计长时间，未作本地测速；不下载或启动。  agentic-rl on-policy-self-distillation recursive-self-improvement Agent 交互策略学习：把轨迹反馈变成更新 本地是否已有 RSIPO adapter、真实技能 replay 和策略训练？ 没有。当前仅保留规格与成本决定，无 paper adapter、指标或 GPU 通过。未来若实现需保留当前策略技能、有效初态重放、独立控制及训练测试隔离，不能拿其他技能算子或固定规则替代后登记完整 RSIPO/Evolve。 例如一个现成 GRPO 训练器能运行，不说明它已测技能净收益或按可靠性做 OPSD，缺这些就未实现该算法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-21d3144e7a542768">本地是否已有 RSIPO adapter、真实技能 replay 和策略训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsipo">RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。当前仅保留规格与成本决定，无 paper adapter、指标或 GPU 通过。未来若实现需保留当前策略技能、有效初态重放、独立控制及训练测试隔离，不能拿其他技能算子或固定规则替代后登记完整 RSIPO/Evolve。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个现成 GRPO 训练器能运行，不说明它已测技能净收益或按可靠性做 OPSD，缺这些就未实现该算法。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、边界与后续触发条件；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15772">原论文</a> · <a href="../../../../reproductions/2610.15772-rsipo/">实现解读</a> · <a href="#qa-21d3144e7a542768">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evo2" data-paper-title="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution Agent University of Illinois Urbana-Champaign / Google DeepMind 2026-10-09 固定任务 executor，共享 Proposer/Reflector 编辑 harness；树搜索与跨分支 crossover 的执行反馈反过来训练 evolver。EvoTIDE 恢复有效编辑轨迹，先 SFT，再交错更新两个角色。事实来源：原文全文。 此处只是有边界的 GSM harness 机制诊断，非原 coding benchmark 复现或隔离 test 能力提升；当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为固定 executor 与初始可执行 harness；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evolution weight-harness-co-evolution dual-role-grpo Agent 交互策略学习：把轨迹反馈变成更新 Evo2 为什么希望自动搜索的提案与反思能力能从经验中学习？ 固定 evolver 每次使用相同提案习惯，可能持续给出低价值或难执行的修改。Evo2 把生成与反思策略作为训练对象，让搜索经验影响后续改进方式，同时固定任务执行器以明确更新来源。搜索获得新版本不等于任务底座也训练了，收益仍需独立执行评价。 教学例：若提案器反复建议不可运行的结构，可训练它利用失败经验改变提案；负责执行任务的模型权重并不必同时变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-evo2-2bf44b34" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e0e1fab4556cc465">Evo2 为什么希望自动搜索的提案与反思能力能从经验中学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevo2">Evo2: Evolving the Evolver through Weight-Harness Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定 evolver 每次使用相同提案习惯，可能持续给出低价值或难执行的修改。Evo2 把生成与反思策略作为训练对象，让搜索经验影响后续改进方式，同时固定任务执行器以明确更新来源。搜索获得新版本不等于任务底座也训练了，收益仍需独立执行评价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：若提案器反复建议不可运行的结构，可训练它利用失败经验改变提案；负责执行任务的模型权重并不必同时变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13025">原论文</a> · <a href="../../../../reproductions/2610.13025-evo2/">实现解读</a> · <a href="#qa-e0e1fab4556cc465">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evo2" data-paper-title="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution Agent University of Illinois Urbana-Champaign / Google DeepMind 2026-10-09 固定任务 executor，共享 Proposer/Reflector 编辑 harness；树搜索与跨分支 crossover 的执行反馈反过来训练 evolver。EvoTIDE 恢复有效编辑轨迹，先 SFT，再交错更新两个角色。事实来源：原文全文。 此处只是有边界的 GSM harness 机制诊断，非原 coding benchmark 复现或隔离 test 能力提升；当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为固定 executor 与初始可执行 harness；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evolution weight-harness-co-evolution dual-role-grpo Agent 交互策略学习：把轨迹反馈变成更新 为什么固定 executor，却训练 Proposer 与 Reflector，仍可称为演化器本身在进步？ 执行任务的模型保持不变，变化的是提出和修复 harness 的策略参数；搜索产生的有效编辑轨迹为这两个角色提供训练信号。这样改进对象从候选框架扩展到如何改框架，keep 收益仍为零，不能把没改动的提议也奖励成成功创新。 例如同一个执行器处理任务，训练后的提议者更会选择日志压缩方案，反思者更会修复错误 hook，收益来自改进过程变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4e5c6f6a3a4054b6">为什么固定 executor，却训练 Proposer 与 Reflector，仍可称为演化器本身在进步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevo2">Evo2: Evolving the Evolver through Weight-Harness Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>执行任务的模型保持不变，变化的是提出和修复 harness 的策略参数；搜索产生的有效编辑轨迹为这两个角色提供训练信号。这样改进对象从候选框架扩展到如何改框架，keep 收益仍为零，不能把没改动的提议也奖励成成功创新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一个执行器处理任务，训练后的提议者更会选择日志压缩方案，反思者更会修复错误 hook，收益来自改进过程变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13025">原论文</a> · <a href="../../../../reproductions/2610.13025-evo2/">实现解读</a> · <a href="#qa-4e5c6f6a3a4054b6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evo2" data-paper-title="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution Agent University of Illinois Urbana-Champaign / Google DeepMind 2026-10-09 固定任务 executor，共享 Proposer/Reflector 编辑 harness；树搜索与跨分支 crossover 的执行反馈反过来训练 evolver。EvoTIDE 恢复有效编辑轨迹，先 SFT，再交错更新两个角色。事实来源：原文全文。 此处只是有边界的 GSM harness 机制诊断，非原 coding benchmark 复现或隔离 test 能力提升；当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为固定 executor 与初始可执行 harness；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evolution weight-harness-co-evolution dual-role-grpo Agent 交互策略学习：把轨迹反馈变成更新 树父权重 ε+|V-1/2| 与只偏爱高成功率节点有什么不同？ 该权重偏离中间表现的节点，并保留 root 固定采样份额，用于搜索分配，不是单纯“分数越高越常选”。跨分支 crossover 与 reflector 也参与产生新 harness，不能用普通冠军贪心替代而保留同名。 例如 V 为零和一都比二分之一离中心更远，这个抽样规则不会只按成功率从高到低选父节点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dae08c347acff56e">树父权重 ε+|V-1/2| 与只偏爱高成功率节点有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevo2">Evo2: Evolving the Evolver through Weight-Harness Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>该权重偏离中间表现的节点，并保留 root 固定采样份额，用于搜索分配，不是单纯“分数越高越常选”。跨分支 crossover 与 reflector 也参与产生新 harness，不能用普通冠军贪心替代而保留同名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 V 为零和一都比二分之一离中心更远，这个抽样规则不会只按成功率从高到低选父节点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13025">原论文</a> · <a href="../../../../reproductions/2610.13025-evo2/">实现解读</a> · <a href="#qa-dae08c347acff56e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evo2" data-paper-title="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution Agent University of Illinois Urbana-Champaign / Google DeepMind 2026-10-09 固定任务 executor，共享 Proposer/Reflector 编辑 harness；树搜索与跨分支 crossover 的执行反馈反过来训练 evolver。EvoTIDE 恢复有效编辑轨迹，先 SFT，再交错更新两个角色。事实来源：原文全文。 此处只是有边界的 GSM harness 机制诊断，非原 coding benchmark 复现或隔离 test 能力提升；当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为固定 executor 与初始可执行 harness；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evolution weight-harness-co-evolution dual-role-grpo Agent 交互策略学习：把轨迹反馈变成更新 keep 收益、角色优势和截断 token 在 loss 中怎么处理？ keep 收益为零，各角色组内用奖励减均值；token loss 按固定 Lmax 归一，截断输出屏蔽，防长度改变训练尺度。本地真实路径仍有特定环境和资源范围，7B policy/executor 加冻结副本不能推定 A30 可容纳，也不等于论文完整代码 benchmark。 例如长输出被截断不应把其不完整尾部当正确编辑监督，若按实际短长度重新平均，还会改变原训练权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-589b7fe7e2d4b7ca">keep 收益、角色优势和截断 token 在 loss 中怎么处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevo2">Evo2: Evolving the Evolver through Weight-Harness Co-Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>keep 收益为零，各角色组内用奖励减均值；token loss 按固定 Lmax 归一，截断输出屏蔽，防长度改变训练尺度。本地真实路径仍有特定环境和资源范围，7B policy/executor 加冻结副本不能推定 A30 可容纳，也不等于论文完整代码 benchmark。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长输出被截断不应把其不完整尾部当正确编辑监督，若按实际短长度重新平均，还会改变原训练权重。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、结果、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13025">原论文</a> · <a href="../../../../reproductions/2610.13025-evo2/">实现解读</a> · <a href="#qa-589b7fe7e2d4b7ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:race" data-paper-title="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation Agent Renmin University of China 2026-10-08 LoGiC 从第二轮逐步删除推理，检查本轮及所有后续原动作的平均 token 对数似然变化，已接受删除继续影响后续上下文。成功轨迹压缩后用于 SFT；RL 屏蔽可删推理并监督提前闭合。原文四个 Agent 环境推理 token 分别减少 32.3%、80.2%、46.4%、62.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。动作似然、成功轨迹 SFT 与 cover-aware actor 梯度接口已实现。真实输入必须提供公开环境、修订与 reason/action/observation 训练轨迹；不能把 QA 解题行伪装成工具轨迹。评估 Agent 不读取参考动作。论文四环境完整 on-policy RL 尚未复测；其端到端能力结果仍缺。  Agentic RL 推理效率 跨轮信用分配 Agent 交互策略学习：把轨迹反馈变成更新 RACE 为什么研究删掉 Agent 轨迹里没有实际帮助的推理？ 长程 Agent 会生成大量思考文本，其中部分只是重复或不影响后续行动，却增加训练与推理负担。RACE 研究在保留行为依据的条件下减少冗余推理。短并非天然更好，删除可能让后续行动失去必要信息，因此压缩需要检查影响，不能只按字数决定哪些内容无用。 教学例：某轮反复复述目标却没有改变任何后续决定，可能是冗余；另一句记录了关键路径，虽短却不能随意删除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-race-11c5fa7f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-126077c5cb720dd9">RACE 为什么研究删掉 Agent 轨迹里没有实际帮助的推理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arace">When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长程 Agent 会生成大量思考文本，其中部分只是重复或不影响后续行动，却增加训练与推理负担。RACE 研究在保留行为依据的条件下减少冗余推理。短并非天然更好，删除可能让后续行动失去必要信息，因此压缩需要检查影响，不能只按字数决定哪些内容无用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：某轮反复复述目标却没有改变任何后续决定，可能是冗余；另一句记录了关键路径，虽短却不能随意删除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12061">原论文</a> · <a href="../../../../agent-research/2610.12061-race/">实现解读</a> · <a href="#qa-126077c5cb720dd9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:race" data-paper-title="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation Agent Renmin University of China 2026-10-08 LoGiC 从第二轮逐步删除推理，检查本轮及所有后续原动作的平均 token 对数似然变化，已接受删除继续影响后续上下文。成功轨迹压缩后用于 SFT；RL 屏蔽可删推理并监督提前闭合。原文四个 Agent 环境推理 token 分别减少 32.3%、80.2%、46.4%、62.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。动作似然、成功轨迹 SFT 与 cover-aware actor 梯度接口已实现。真实输入必须提供公开环境、修订与 reason/action/observation 训练轨迹；不能把 QA 解题行伪装成工具轨迹。评估 Agent 不读取参考动作。论文四环境完整 on-policy RL 尚未复测；其端到端能力结果仍缺。  Agentic RL 推理效率 跨轮信用分配 Agent 交互策略学习：把轨迹反馈变成更新 删除某轮 reasoning 时，为什么还要检查所有后续原动作的似然变化？ 当前动作看似不受影响，不代表早期推理对后面规划无用。逐步删除后用受影响的新上下文评估后续动作，只有变化都在容差内才继续，已接受删除也保留在之后压缩状态；仅检查本轮会漏掉长程依赖，删 token 数也不等于任务成功。 例如一段推理提前记住安全限制，本轮只是读取文件，后面删除动作才依赖该限制；只验本轮就可能误删关键思考。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-98ccf35fdf26f763">删除某轮 reasoning 时，为什么还要检查所有后续原动作的似然变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arace">When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前动作看似不受影响，不代表早期推理对后面规划无用。逐步删除后用受影响的新上下文评估后续动作，只有变化都在容差内才继续，已接受删除也保留在之后压缩状态；仅检查本轮会漏掉长程依赖，删 token 数也不等于任务成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一段推理提前记住安全限制，本轮只是读取文件，后面删除动作才依赖该限制；只验本轮就可能误删关键思考。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12061">原论文</a> · <a href="../../../../agent-research/2610.12061-race/">实现解读</a> · <a href="#qa-98ccf35fdf26f763">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:race" data-paper-title="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation Agent Renmin University of China 2026-10-08 LoGiC 从第二轮逐步删除推理，检查本轮及所有后续原动作的平均 token 对数似然变化，已接受删除继续影响后续上下文。成功轨迹压缩后用于 SFT；RL 屏蔽可删推理并监督提前闭合。原文四个 Agent 环境推理 token 分别减少 32.3%、80.2%、46.4%、62.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。动作似然、成功轨迹 SFT 与 cover-aware actor 梯度接口已实现。真实输入必须提供公开环境、修订与 reason/action/observation 训练轨迹；不能把 QA 解题行伪装成工具轨迹。评估 Agent 不读取参考动作。论文四环境完整 on-policy RL 尚未复测；其端到端能力结果仍缺。  Agentic RL 推理效率 跨轮信用分配 Agent 交互策略学习：把轨迹反馈变成更新 推理 loss mask 与实际删掉训练上下文有什么区别？ mask 只取消被判可删 token 的监督，其他动作仍在规定条件下训练；直接删除上下文会改变后续预测分布。RACE 还监督提前闭合，保持原全部策略 token 和全部回合分母，不能随删减量重缩放而默默改变目标。 例如删去一半 reasoning 的监督后仍用原 token 数归一，避免剩余动作权重因长度变短意外翻倍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4be62e7f3db5d3ea">推理 loss mask 与实际删掉训练上下文有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arace">When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>mask 只取消被判可删 token 的监督，其他动作仍在规定条件下训练；直接删除上下文会改变后续预测分布。RACE 还监督提前闭合，保持原全部策略 token 和全部回合分母，不能随删减量重缩放而默默改变目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删去一半 reasoning 的监督后仍用原 token 数归一，避免剩余动作权重因长度变短意外翻倍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12061">原论文</a> · <a href="../../../../agent-research/2610.12061-race/">实现解读</a> · <a href="#qa-4be62e7f3db5d3ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:race" data-paper-title="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation Agent Renmin University of China 2026-10-08 LoGiC 从第二轮逐步删除推理，检查本轮及所有后续原动作的平均 token 对数似然变化，已接受删除继续影响后续上下文。成功轨迹压缩后用于 SFT；RL 屏蔽可删推理并监督提前闭合。原文四个 Agent 环境推理 token 分别减少 32.3%、80.2%、46.4%、62.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。动作似然、成功轨迹 SFT 与 cover-aware actor 梯度接口已实现。真实输入必须提供公开环境、修订与 reason/action/observation 训练轨迹；不能把 QA 解题行伪装成工具轨迹。评估 Agent 不读取参考动作。论文四环境完整 on-policy RL 尚未复测；其端到端能力结果仍缺。  Agentic RL 推理效率 跨轮信用分配 Agent 交互策略学习：把轨迹反馈变成更新 真实轨迹输入与本地 bounded calculator 结果如何限定结论？ 真实训练数据要有环境、修订、split 和 reasoning/action/observation，不能把 QA 行伪装工具轨迹。本地 calculator 确有动作采样和 SFT/on-policy 更新，但只是 L1 机制，单 seed 少量成功不代表 ScienceWorld 或四环境完整 RL 复现。 例如模型真正调用两种计算工具可证明交互训练发生，不能把这些短轨迹改名为长期网页或具身任务能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-202711996a37bca1">真实轨迹输入与本地 bounded calculator 结果如何限定结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arace">When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实训练数据要有环境、修订、split 和 reasoning/action/observation，不能把 QA 行伪装工具轨迹。本地 calculator 确有动作采样和 SFT/on-policy 更新，但只是 L1 机制，单 seed 少量成功不代表 ScienceWorld 或四环境完整 RL 复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型真正调用两种计算工具可证明交互训练发生，不能把这些短轨迹改名为长期网页或具身任务能力。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12061">原论文</a> · <a href="../../../../agent-research/2610.12061-race/">实现解读</a> · <a href="#qa-202711996a37bca1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adastep" data-paper-title="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning Agent Tsinghua University 2026-10-02 Agent 长轨迹的终局奖励给每一步同样的全局优势，无法指出哪一步有用；GiGPO 等方法用相同锚状态的局部回报补充信用，但同一动作之后的随机路径也会改变回报。AdaStep 不另训 critic，而是看同组中不同动作解释了多少回报方差。动作间差异主导时信任局部信用；同动作内部差异主导时将局部修正压低，保留全局优势。 L1 统计机制诊断。L1 统计机制诊断。实现论文 Eq. (17)–(18) 的同锚状态、按动作分组的方差分解、稀疏组回退和最终优势组合；没有宣称完成 Agent 策略训练或原文任务评测。输入只包含策略 rollout 的任务 ID、状态键、动作、折扣回报和全局优势；分组键为任务 ID 与 anchor state，避免不同任务的同名状态互相污染。不读取金标答案或计划。这里未运行环境交互、Qwen 策略更新、ALFWorld/WebShop/ScienceWorld，也没有同预算的 GiGPO 对照。  Agentic RL 步骤信用分配 方差可靠性 Agent 交互策略学习：把轨迹反馈变成更新 AdaStep 为什么要区分一个动作的作用与后续随机路径带来的运气？ 长任务相同中间状态下，一次动作后最终成败还受很多后续选择影响，直接把终局差异归给该动作会产生噪声。AdaStep 研究利用多条已观察轨迹判断局部信用有多可信，保留全局结果同时谨慎调整步骤信号。它不需要另训 critic，也不能凭少数样本证明动作真实因果效应。 教学例：相同查找动作后，有人后续答对、有人误写答案，这种差异不能全怪查找；需要看动作间差异是否超出各自后续波动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-adastep-2ac090d9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-926133c26eb20165">AdaStep 为什么要区分一个动作的作用与后续随机路径带来的运气？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aadastep">AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长任务相同中间状态下，一次动作后最终成败还受很多后续选择影响，直接把终局差异归给该动作会产生噪声。AdaStep 研究利用多条已观察轨迹判断局部信用有多可信，保留全局结果同时谨慎调整步骤信号。它不需要另训 critic，也不能凭少数样本证明动作真实因果效应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：相同查找动作后，有人后续答对、有人误写答案，这种差异不能全怪查找；需要看动作间差异是否超出各自后续波动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03223">原论文</a> · <a href="../../../../agent-research/2610.03223-adastep/">实现解读</a> · <a href="#qa-926133c26eb20165">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adastep" data-paper-title="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning Agent Tsinghua University 2026-10-02 Agent 长轨迹的终局奖励给每一步同样的全局优势，无法指出哪一步有用；GiGPO 等方法用相同锚状态的局部回报补充信用，但同一动作之后的随机路径也会改变回报。AdaStep 不另训 critic，而是看同组中不同动作解释了多少回报方差。动作间差异主导时信任局部信用；同动作内部差异主导时将局部修正压低，保留全局优势。 L1 统计机制诊断。L1 统计机制诊断。实现论文 Eq. (17)–(18) 的同锚状态、按动作分组的方差分解、稀疏组回退和最终优势组合；没有宣称完成 Agent 策略训练或原文任务评测。输入只包含策略 rollout 的任务 ID、状态键、动作、折扣回报和全局优势；分组键为任务 ID 与 anchor state，避免不同任务的同名状态互相污染。不读取金标答案或计划。这里未运行环境交互、Qwen 策略更新、ALFWorld/WebShop/ScienceWorld，也没有同预算的 GiGPO 对照。  Agentic RL 步骤信用分配 方差可靠性 Agent 交互策略学习：把轨迹反馈变成更新 同锚状态下动作内回报方差很大时，为什么应降低局部信用修正？ 同一动作后续随机路线就能导致很大成败差，说明局部动作未解释大部分回报变化。方差分解让动作间差异主导时更信任局部优势，否则保留全局优势而压低修正；权重从原始回报统计估计，不能先随意归一化后改变方差关系。 例如动作甲的几条 rollout 既有满分也有零分，乙也类似，差异主要来自后续随机性，就不应把单次结果强归因给甲乙。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-01ccc5b94842adc5">同锚状态下动作内回报方差很大时，为什么应降低局部信用修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aadastep">AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一动作后续随机路线就能导致很大成败差，说明局部动作未解释大部分回报变化。方差分解让动作间差异主导时更信任局部优势，否则保留全局优势而压低修正；权重从原始回报统计估计，不能先随意归一化后改变方差关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如动作甲的几条 rollout 既有满分也有零分，乙也类似，差异主要来自后续随机性，就不应把单次结果强归因给甲乙。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03223">原论文</a> · <a href="../../../../agent-research/2610.03223-adastep/">实现解读</a> · <a href="#qa-01ccc5b94842adc5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adastep" data-paper-title="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning Agent Tsinghua University 2026-10-02 Agent 长轨迹的终局奖励给每一步同样的全局优势，无法指出哪一步有用；GiGPO 等方法用相同锚状态的局部回报补充信用，但同一动作之后的随机路径也会改变回报。AdaStep 不另训 critic，而是看同组中不同动作解释了多少回报方差。动作间差异主导时信任局部信用；同动作内部差异主导时将局部修正压低，保留全局优势。 L1 统计机制诊断。L1 统计机制诊断。实现论文 Eq. (17)–(18) 的同锚状态、按动作分组的方差分解、稀疏组回退和最终优势组合；没有宣称完成 Agent 策略训练或原文任务评测。输入只包含策略 rollout 的任务 ID、状态键、动作、折扣回报和全局优势；分组键为任务 ID 与 anchor state，避免不同任务的同名状态互相污染。不读取金标答案或计划。这里未运行环境交互、Qwen 策略更新、ALFWorld/WebShop/ScienceWorld，也没有同预算的 GiGPO 对照。  Agentic RL 步骤信用分配 方差可靠性 Agent 交互策略学习：把轨迹反馈变成更新 AdaStep 的回报统计路线与另训 critic 的步骤评价，在额外学习对象上有什么不同？ critic 路线要训练一个状态或动作价值估计器，再用其预测组织信用；AdaStep 直接从同锚状态多动作的经验回报统计估计局部修正可信度，不另训练 critic。它减少一个预测器，也受重复状态和样本覆盖限制，不能由无 critic 推出无噪声或普遍更准确。 教学例：同一网页状态有多次不同动作及后续结果，可直接统计波动；若只出现一次，就没有足够样本凭空获得可靠局部估计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-064d790622e98c72">AdaStep 的回报统计路线与另训 critic 的步骤评价，在额外学习对象上有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aadastep">AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>critic 路线要训练一个状态或动作价值估计器，再用其预测组织信用；AdaStep 直接从同锚状态多动作的经验回报统计估计局部修正可信度，不另训练 critic。它减少一个预测器，也受重复状态和样本覆盖限制，不能由无 critic 推出无噪声或普遍更准确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：同一网页状态有多次不同动作及后续结果，可直接统计波动；若只出现一次，就没有足够样本凭空获得可靠局部估计。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03223">原论文</a> · <a href="../../../../agent-research/2610.03223-adastep/">实现解读</a> · <a href="#qa-064d790622e98c72">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adastep" data-paper-title="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning Agent Tsinghua University 2026-10-02 Agent 长轨迹的终局奖励给每一步同样的全局优势，无法指出哪一步有用；GiGPO 等方法用相同锚状态的局部回报补充信用，但同一动作之后的随机路径也会改变回报。AdaStep 不另训 critic，而是看同组中不同动作解释了多少回报方差。动作间差异主导时信任局部信用；同动作内部差异主导时将局部修正压低，保留全局优势。 L1 统计机制诊断。L1 统计机制诊断。实现论文 Eq. (17)–(18) 的同锚状态、按动作分组的方差分解、稀疏组回退和最终优势组合；没有宣称完成 Agent 策略训练或原文任务评测。输入只包含策略 rollout 的任务 ID、状态键、动作、折扣回报和全局优势；分组键为任务 ID 与 anchor state，避免不同任务的同名状态互相污染。不读取金标答案或计划。这里未运行环境交互、Qwen 策略更新、ALFWorld/WebShop/ScienceWorld，也没有同预算的 GiGPO 对照。  Agentic RL 步骤信用分配 方差可靠性 Agent 交互策略学习：把轨迹反馈变成更新 少动作、少样本、零方差与归一化回报如何处理？ 至少两动作、每动作两样本且总方差正才估比率，否则按论文回退 w=1；全回报相同时局部优势为零。权重始终用未归一化回报统计，分组含 task ID 防同名状态跨任务混合；本地未运行真实环境或策略训练。 例如只有一个动作虽看不见动作间差异，也不能自造 w=0 替代约定；所有奖励一样则不应凭空产生局部修正。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f78bea596aecce94">少动作、少样本、零方差与归一化回报如何处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aadastep">AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>至少两动作、每动作两样本且总方差正才估比率，否则按论文回退 w=1；全回报相同时局部优势为零。权重始终用未归一化回报统计，分组含 task ID 防同名状态跨任务混合；本地未运行真实环境或策略训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只有一个动作虽看不见动作间差异，也不能自造 w=0 替代约定；所有奖励一样则不应凭空产生局部修正。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03223">原论文</a> · <a href="../../../../agent-research/2610.03223-adastep/">实现解读</a> · <a href="#qa-f78bea596aecce94">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:depgpo" data-paper-title="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents Agent Southeast University 2026-10-02 终端 Agent 通常只拿到任务结束后的 verifier 奖励。GRPO 把同一条轨迹的优势分给所有生成 token，无法区分真正生成答案的命令、为其提供数据的读取，以及后来被覆盖或无关的操作。DepGPO 从执行记录构造命令依赖图：文件读取连向该文件尚未覆盖的写入者，可信的 stdout 复用也形成边；再从 verifier 实际检查的文件、端口和进程向后追溯。 L1 机制诊断。L1 机制诊断。这里实现了论文的记录级读写依赖、相关写入与支持性读取信用，以及步级/令牌级优势归一化；尚未接入真实终端 tracer、verifier 执行或 Qwen 策略训练，不能把机制指标当成任务成功率。机制回执只包含四条手工结构化命令：支持读取、间接写入、最终写入、无关写入。测试还覆盖覆盖写不自动建立依赖、写入记录分母、最短路径、回退、负优势与 token 数不等时的均值守恒。这不是 Terminal-Bench、真实 Qwen 训练或多 seed 能力比较。  Agentic RL 终端命令依赖 步骤信用分配 Agent 交互策略学习：把轨迹反馈变成更新 终端任务只有最后成功或失败时，DEPGPO 为什么要追踪命令之间的依赖？ 一条长轨迹含许多读写文件的动作，终局奖励无法直接指出哪些命令产生了最终结果。DEPGPO 用实际依赖把后续验证与前面有效工作联系起来，为信用分配提供结构。依赖只说明数据流关系，不是所有命令的真实因果贡献，缺失记录或验证器副作用都需明确边界。 教学例：最后测试读取某个源文件，可沿写入关系找到生成它的命令；无关目录浏览不应只因出现在同一轨迹就得到相同信用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-depgpo-58f41b1f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5869340756f1992c">终端任务只有最后成功或失败时，DEPGPO 为什么要追踪命令之间的依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adepgpo">Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一条长轨迹含许多读写文件的动作，终局奖励无法直接指出哪些命令产生了最终结果。DEPGPO 用实际依赖把后续验证与前面有效工作联系起来，为信用分配提供结构。依赖只说明数据流关系，不是所有命令的真实因果贡献，缺失记录或验证器副作用都需明确边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：最后测试读取某个源文件，可沿写入关系找到生成它的命令；无关目录浏览不应只因出现在同一轨迹就得到相同信用。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03634">原论文</a> · <a href="../../../../agent-research/2610.03634-depgpo/">实现解读</a> · <a href="#qa-5869340756f1992c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:depgpo" data-paper-title="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents Agent Southeast University 2026-10-02 终端 Agent 通常只拿到任务结束后的 verifier 奖励。GRPO 把同一条轨迹的优势分给所有生成 token，无法区分真正生成答案的命令、为其提供数据的读取，以及后来被覆盖或无关的操作。DepGPO 从执行记录构造命令依赖图：文件读取连向该文件尚未覆盖的写入者，可信的 stdout 复用也形成边；再从 verifier 实际检查的文件、端口和进程向后追溯。 L1 机制诊断。L1 机制诊断。这里实现了论文的记录级读写依赖、相关写入与支持性读取信用，以及步级/令牌级优势归一化；尚未接入真实终端 tracer、verifier 执行或 Qwen 策略训练，不能把机制指标当成任务成功率。机制回执只包含四条手工结构化命令：支持读取、间接写入、最终写入、无关写入。测试还覆盖覆盖写不自动建立依赖、写入记录分母、最短路径、回退、负优势与 token 数不等时的均值守恒。这不是 Terminal-Bench、真实 Qwen 训练或多 seed 能力比较。  Agentic RL 终端命令依赖 步骤信用分配 Agent 交互策略学习：把轨迹反馈变成更新 命令依赖图为什么要连接文件读取与尚未被覆盖的写入者？ 读取实际消费的是当时有效版本，已被后续覆盖的旧写入不一定影响最终产物。依赖图从 verifier 检查对象向后追踪，把贡献数据的操作与真正结果路径连接，减少无关步骤共享终局优势；图构建还需可信执行记录，不能凭命令文字猜因果。 例如先写旧配置、再覆盖新配置，测试只读取新版本；信用不应同样奖励已被覆盖且未被使用的旧写入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6b464bc6f959c9dc">命令依赖图为什么要连接文件读取与尚未被覆盖的写入者？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adepgpo">Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>读取实际消费的是当时有效版本，已被后续覆盖的旧写入不一定影响最终产物。依赖图从 verifier 检查对象向后追踪，把贡献数据的操作与真正结果路径连接，减少无关步骤共享终局优势；图构建还需可信执行记录，不能凭命令文字猜因果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先写旧配置、再覆盖新配置，测试只读取新版本；信用不应同样奖励已被覆盖且未被使用的旧写入。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03634">原论文</a> · <a href="../../../../agent-research/2610.03634-depgpo/">实现解读</a> · <a href="#qa-6b464bc6f959c9dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:depgpo" data-paper-title="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents Agent Southeast University 2026-10-02 终端 Agent 通常只拿到任务结束后的 verifier 奖励。GRPO 把同一条轨迹的优势分给所有生成 token，无法区分真正生成答案的命令、为其提供数据的读取，以及后来被覆盖或无关的操作。DepGPO 从执行记录构造命令依赖图：文件读取连向该文件尚未覆盖的写入者，可信的 stdout 复用也形成边；再从 verifier 实际检查的文件、端口和进程向后追溯。 L1 机制诊断。L1 机制诊断。这里实现了论文的记录级读写依赖、相关写入与支持性读取信用，以及步级/令牌级优势归一化；尚未接入真实终端 tracer、verifier 执行或 Qwen 策略训练，不能把机制指标当成任务成功率。机制回执只包含四条手工结构化命令：支持读取、间接写入、最终写入、无关写入。测试还覆盖覆盖写不自动建立依赖、写入记录分母、最短路径、回退、负优势与 token 数不等时的均值守恒。这不是 Terminal-Bench、真实 Qwen 训练或多 seed 能力比较。  Agentic RL 终端命令依赖 步骤信用分配 Agent 交互策略学习：把轨迹反馈变成更新 依赖信用与 GRPO 全轨迹单位权重有什么不同？ 单位权重不区分支持动作、最终写和无关命令，DepGPO 按可追溯写入及距离分配步信用，再归一保持 token 加权平均优势和符号。它依赖 tracer 正确性，不是完整因果证明，也不能把高信用自动解释为该命令单独必要。 例如读输入再写答案的链可获得间接信用，清理无关临时文件权重较低，但负轨迹优势仍保持负号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-10cd0d548bedc46a">依赖信用与 GRPO 全轨迹单位权重有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adepgpo">Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单位权重不区分支持动作、最终写和无关命令，DepGPO 按可追溯写入及距离分配步信用，再归一保持 token 加权平均优势和符号。它依赖 tracer 正确性，不是完整因果证明，也不能把高信用自动解释为该命令单独必要。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如读输入再写答案的链可获得间接信用，清理无关临时文件权重较低，但负轨迹优势仍保持负号。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03634">原论文</a> · <a href="../../../../agent-research/2610.03634-depgpo/">实现解读</a> · <a href="#qa-10cd0d548bedc46a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:depgpo" data-paper-title="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents Agent Southeast University 2026-10-02 终端 Agent 通常只拿到任务结束后的 verifier 奖励。GRPO 把同一条轨迹的优势分给所有生成 token，无法区分真正生成答案的命令、为其提供数据的读取，以及后来被覆盖或无关的操作。DepGPO 从执行记录构造命令依赖图：文件读取连向该文件尚未覆盖的写入者，可信的 stdout 复用也形成边；再从 verifier 实际检查的文件、端口和进程向后追溯。 L1 机制诊断。L1 机制诊断。这里实现了论文的记录级读写依赖、相关写入与支持性读取信用，以及步级/令牌级优势归一化；尚未接入真实终端 tracer、verifier 执行或 Qwen 策略训练，不能把机制指标当成任务成功率。机制回执只包含四条手工结构化命令：支持读取、间接写入、最终写入、无关写入。测试还覆盖覆盖写不自动建立依赖、写入记录分母、最短路径、回退、负优势与 token 数不等时的均值守恒。这不是 Terminal-Bench、真实 Qwen 训练或多 seed 能力比较。  Agentic RL 终端命令依赖 步骤信用分配 Agent 交互策略学习：把轨迹反馈变成更新 同一步多命令、缺记录与 verifier 自写文件有哪些边界？ 同一步命令信用求和而非平均；无记录或全并列回退单位权重。verifier 自写资源须剔除，stdout 来源排除任务提示已有值，路径和行号由可信 tracer 提供；本地不解析 shell、不运行真实 Qwen RL，四条手工链只属机制验证。 例如评分脚本自行生成结果文件，若把它当 Agent 写入会奖励不存在的贡献；输入 tracer 应先清除这类噪声。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5469b9418d6e2fa5">同一步多命令、缺记录与 verifier 自写文件有哪些边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adepgpo">Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一步命令信用求和而非平均；无记录或全并列回退单位权重。verifier 自写资源须剔除，stdout 来源排除任务提示已有值，路径和行号由可信 tracer 提供；本地不解析 shell、不运行真实 Qwen RL，四条手工链只属机制验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如评分脚本自行生成结果文件，若把它当 Agent 写入会奖励不存在的贡献；输入 tracer 应先清除这类噪声。</p>
<p class="ar-learning-sources">依据：公式与关键区别、本地复现（机制验证）、复现边界与下一步；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03634">原论文</a> · <a href="../../../../agent-research/2610.03634-depgpo/">实现解读</a> · <a href="#qa-5469b9418d6e2fa5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dr-credit" data-paper-title="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents Agent University of Chinese Academy of Sciences 2026-09-28 按 rubric 的历史已接受支持计算本次工具结果带来的新增或部分支持，再与最终结果优势结合，避免重复证据反复得分。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent RL 过程信用分配 Agent 交互策略学习：把轨迹反馈变成更新 Dr.Credit 为什么关注深度研究中每次检索有没有带来新的答案依据？ 研究 Agent 可以不断搜索并收集很多相似材料，却未必补齐问题所需事实。Dr.Credit 研究把过程反馈与评价标准的证据支持联系起来，鼓励真正推进回答的检索。奖励来自训练侧的支持判断，不是文档数量，判断器和 rubric 的可靠性仍会限制信用质量。 教学例：已有价格证据后再找三份同价转载，并未补上保修条件；下一次找到保修原文才可能填补新的回答要求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-dr-credit-775af357" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-525c97d9167576c7">Dr.Credit 为什么关注深度研究中每次检索有没有带来新的答案依据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adr-credit">Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究 Agent 可以不断搜索并收集很多相似材料，却未必补齐问题所需事实。Dr.Credit 研究把过程反馈与评价标准的证据支持联系起来，鼓励真正推进回答的检索。奖励来自训练侧的支持判断，不是文档数量，判断器和 rubric 的可靠性仍会限制信用质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：已有价格证据后再找三份同价转载，并未补上保修条件；下一次找到保修原文才可能填补新的回答要求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34296">原论文</a> · <a href="../../../../agent-research/2609.34296-dr-credit/">实现解读</a> · <a href="#qa-525c97d9167576c7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dr-credit" data-paper-title="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents Agent University of Chinese Academy of Sciences 2026-09-28 按 rubric 的历史已接受支持计算本次工具结果带来的新增或部分支持，再与最终结果优势结合，避免重复证据反复得分。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent RL 过程信用分配 Agent 交互策略学习：把轨迹反馈变成更新 为什么检索到重复证据不应该反复获得同样的过程奖励？ 过程信用应反映相对已接受证据的新支持，而不是工具调用次数。按 rubric 维护历史覆盖，再评本次新增或部分支持，能减少重复搜索刷分；最终结果优势仍保留，避免局部新颖证据与真正研究目标脱节，支持关系也须有可核验依据。 例如两次返回同一发布日期，第二次没有补新约束就不应再拿完整奖励；找到此前缺失的机构证据才有新增贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2a21b47c32a7be2a">为什么检索到重复证据不应该反复获得同样的过程奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adr-credit">Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>过程信用应反映相对已接受证据的新支持，而不是工具调用次数。按 rubric 维护历史覆盖，再评本次新增或部分支持，能减少重复搜索刷分；最终结果优势仍保留，避免局部新颖证据与真正研究目标脱节，支持关系也须有可核验依据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次返回同一发布日期，第二次没有补新约束就不应再拿完整奖励；找到此前缺失的机构证据才有新增贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34296">原论文</a> · <a href="../../../../agent-research/2609.34296-dr-credit/">实现解读</a> · <a href="#qa-2a21b47c32a7be2a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dr-credit" data-paper-title="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents Agent University of Chinese Academy of Sciences 2026-09-28 按 rubric 的历史已接受支持计算本次工具结果带来的新增或部分支持，再与最终结果优势结合，避免重复证据反复得分。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent RL 过程信用分配 Agent 交互策略学习：把轨迹反馈变成更新 按 rubric 给增量过程反馈，与只在最终答案打分，对监督时机有何不同？ 终局打分评价最终产物，却难区分此前哪些检索有效；增量支持沿过程检查各项要求何时获得新依据，把反馈连接到具体取证动作。过程支持不保证最后写对，最终答案也可能误用已找到材料，因此两种信号不能互相替代，更不能将训练 rubric 暴露给受评 actor。 教学例：检索已找到正确日期，过程可确认一项证据补齐；最终回答却抄错年份，终局评分仍应指出答案错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-db3655f96d65603f">按 rubric 给增量过程反馈，与只在最终答案打分，对监督时机有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adr-credit">Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局打分评价最终产物，却难区分此前哪些检索有效；增量支持沿过程检查各项要求何时获得新依据，把反馈连接到具体取证动作。过程支持不保证最后写对，最终答案也可能误用已找到材料，因此两种信号不能互相替代，更不能将训练 rubric 暴露给受评 actor。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：检索已找到正确日期，过程可确认一项证据补齐；最终回答却抄错年份，终局评分仍应指出答案错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34296">原论文</a> · <a href="../../../../agent-research/2609.34296-dr-credit/">实现解读</a> · <a href="#qa-db3655f96d65603f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dr-credit" data-paper-title="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents Agent University of Chinese Academy of Sciences 2026-09-28 按 rubric 的历史已接受支持计算本次工具结果带来的新增或部分支持，再与最终结果优势结合，避免重复证据反复得分。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent RL 过程信用分配 Agent 交互策略学习：把轨迹反馈变成更新 本地 rubric 与支持分由 fixture 提供时能验证什么？ 能验证历史更新、重复证据不重复得分和增量信用方向，不能验证语义 judge 是否真实识别支持。策略不读 gold answer，三 seed mini-suite 也不是 Deep Research 能力；只有来源真实、匹配可信并有实际训练才能升级结论。 例如预设证据甲支持规则一后可测第二次增量为零，但未测试模型能否从网页自行判断甲确实支持规则一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-15d7ab33e8441f51">本地 rubric 与支持分由 fixture 提供时能验证什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adr-credit">Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>能验证历史更新、重复证据不重复得分和增量信用方向，不能验证语义 judge 是否真实识别支持。策略不读 gold answer，三 seed mini-suite 也不是 Deep Research 能力；只有来源真实、匹配可信并有实际训练才能升级结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预设证据甲支持规则一后可测第二次增量为零，但未测试模型能否从网页自行判断甲确实支持规则一。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34296">原论文</a> · <a href="../../../../agent-research/2609.34296-dr-credit/">实现解读</a> · <a href="#qa-15d7ab33e8441f51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:graphhca" data-paper-title="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents Agent Beihang University 2026-09-28 稀疏终局奖励难以定位长轨迹中的关键动作。GraphHCA 把 rollout 合并为状态转移图，以成功/失败终态为边界解折扣固定点，再把相邻状态的对数势能差分配给每一步，并在同状态动作间标准化。 复现级别：L1 无 gold 核心机制。复现级别：L1 无 gold 核心机制。本地从采样轨迹图、动作和终局结果计算固定点势能与逐步优势；不读取参考答案或计划。当前未训练语言模型，也未把 GraphHCA 注册为 Evolve 算子。只有统一控制器能采样真实轨迹、执行该 estimator 并隔离验证策略更新后才算正式接入。graphhca_credit 只接受 Transition 和 success 布尔值；汇总实验见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Agentic RL 信用分配 轨迹图 Agent 交互策略学习：把轨迹反馈变成更新 GraphHCA 为什么希望长程动作在最终成功之前也能获得有结构的训练信号？ 终局反馈稀疏时，早期探索和关键转移常被同一个轨迹奖励淹没。GraphHCA 把已观察状态转移组织成图，再将成功信息传播到相连状态，用于估计动作进展。图只覆盖已有数据，图上的势能不是环境真值，也不能把训练侧成功标签提前给部署 actor。 教学例：多条路线都经某个关键开门状态才到终点，状态图可连接这些经验；未见过的门后状态仍不能凭图假定成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-graphhca-933790a0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-78177d1580783057">GraphHCA 为什么希望长程动作在最终成功之前也能获得有结构的训练信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agraphhca">GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局反馈稀疏时，早期探索和关键转移常被同一个轨迹奖励淹没。GraphHCA 把已观察状态转移组织成图，再将成功信息传播到相连状态，用于估计动作进展。图只覆盖已有数据，图上的势能不是环境真值，也不能把训练侧成功标签提前给部署 actor。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：多条路线都经某个关键开门状态才到终点，状态图可连接这些经验；未见过的门后状态仍不能凭图假定成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35084">原论文</a> · <a href="../../../../agent-research/2609.35084-graphhca/">实现解读</a> · <a href="#qa-78177d1580783057">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:graphhca" data-paper-title="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents Agent Beihang University 2026-09-28 稀疏终局奖励难以定位长轨迹中的关键动作。GraphHCA 把 rollout 合并为状态转移图，以成功/失败终态为边界解折扣固定点，再把相邻状态的对数势能差分配给每一步，并在同状态动作间标准化。 复现级别：L1 无 gold 核心机制。复现级别：L1 无 gold 核心机制。本地从采样轨迹图、动作和终局结果计算固定点势能与逐步优势；不读取参考答案或计划。当前未训练语言模型，也未把 GraphHCA 注册为 Evolve 算子。只有统一控制器能采样真实轨迹、执行该 estimator 并隔离验证策略更新后才算正式接入。graphhca_credit 只接受 Transition 和 success 布尔值；汇总实验见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Agentic RL 信用分配 轨迹图 Agent 交互策略学习：把轨迹反馈变成更新 为什么先解状态图折扣固定点，再用对数势能差给动作信用？ 终局成功失败作为边界，经经验转移传播到共享状态，得到通往成功的折扣潜势；相邻状态的对数变化把远期信息转成局部推进信号，再在同起点动作间标准化。它利用完整 rollout 作训练归因，不能把这些事后成功边界交给评测 Agent 当观察。 例如两条路径都经过同一中间状态，状态图可共享其后成功证据，再比较离开该状态的动作是靠近成功还是走入死路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-626bb9e86b51c09f">为什么先解状态图折扣固定点，再用对数势能差给动作信用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agraphhca">GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局成功失败作为边界，经经验转移传播到共享状态，得到通往成功的折扣潜势；相邻状态的对数变化把远期信息转成局部推进信号，再在同起点动作间标准化。它利用完整 rollout 作训练归因，不能把这些事后成功边界交给评测 Agent 当观察。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条路径都经过同一中间状态，状态图可共享其后成功证据，再比较离开该状态的动作是靠近成功还是走入死路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35084">原论文</a> · <a href="../../../../agent-research/2609.35084-graphhca/">实现解读</a> · <a href="#qa-626bb9e86b51c09f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:graphhca" data-paper-title="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents Agent Beihang University 2026-09-28 稀疏终局奖励难以定位长轨迹中的关键动作。GraphHCA 把 rollout 合并为状态转移图，以成功/失败终态为边界解折扣固定点，再把相邻状态的对数势能差分配给每一步，并在同状态动作间标准化。 复现级别：L1 无 gold 核心机制。复现级别：L1 无 gold 核心机制。本地从采样轨迹图、动作和终局结果计算固定点势能与逐步优势；不读取参考答案或计划。当前未训练语言模型，也未把 GraphHCA 注册为 Evolve 算子。只有统一控制器能采样真实轨迹、执行该 estimator 并隔离验证策略更新后才算正式接入。graphhca_credit 只接受 Transition 和 success 布尔值；汇总实验见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Agentic RL 信用分配 轨迹图 Agent 交互策略学习：把轨迹反馈变成更新 图势能差与整条轨迹同一个 advantage 有何区别？ 轨迹优势不区分哪步走近可成功区域，势能差尝试突出状态价值的改善或恶化，并在共享起点动作间标准化。它依赖经验转移概率和 ε，不能把差值当独立因果贡献，也不意味着所有循环都被可靠惩罚。 例如终局相同的轨迹里，一步推进到高势能状态、另一步返回低势能状态可得到不同局部信用，而非统一广播。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7232cac30f7687cb">图势能差与整条轨迹同一个 advantage 有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agraphhca">GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轨迹优势不区分哪步走近可成功区域，势能差尝试突出状态价值的改善或恶化，并在共享起点动作间标准化。它依赖经验转移概率和 ε，不能把差值当独立因果贡献，也不意味着所有循环都被可靠惩罚。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如终局相同的轨迹里，一步推进到高势能状态、另一步返回低势能状态可得到不同局部信用，而非统一广播。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35084">原论文</a> · <a href="../../../../agent-research/2609.35084-graphhca/">实现解读</a> · <a href="#qa-7232cac30f7687cb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:graphhca" data-paper-title="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents Agent Beihang University 2026-09-28 稀疏终局奖励难以定位长轨迹中的关键动作。GraphHCA 把 rollout 合并为状态转移图，以成功/失败终态为边界解折扣固定点，再把相邻状态的对数势能差分配给每一步，并在同状态动作间标准化。 复现级别：L1 无 gold 核心机制。复现级别：L1 无 gold 核心机制。本地从采样轨迹图、动作和终局结果计算固定点势能与逐步优势；不读取参考答案或计划。当前未训练语言模型，也未把 GraphHCA 注册为 Evolve 算子。只有统一控制器能采样真实轨迹、执行该 estimator 并隔离验证策略更新后才算正式接入。graphhca_credit 只接受 Transition 和 success 布尔值；汇总实验见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Agentic RL 信用分配 轨迹图 Agent 交互策略学习：把轨迹反馈变成更新 本地 Transition 与 success 输入为什么只留在 estimator，不进入 actor？ 终态标签用于训练侧势能估计，actor 只能读当时公开状态，不能提前获得图中最终成功边界。当前未训练语言模型或接入 Evolve，固定点收敛和信用排序只是机制证据，需真实 rollout、策略更新和隔离评价才算完整集成。 例如训练后标注某终态成功可用来算信用，测试决策时若直接告诉 Agent 哪条后继通向成功，就泄露了结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b3bf6752fef4363f">本地 Transition 与 success 输入为什么只留在 estimator，不进入 actor？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agraphhca">GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终态标签用于训练侧势能估计，actor 只能读当时公开状态，不能提前获得图中最终成功边界。当前未训练语言模型或接入 Evolve，固定点收敛和信用排序只是机制证据，需真实 rollout、策略更新和隔离评价才算完整集成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练后标注某终态成功可用来算信用，测试决策时若直接告诉 Agent 哪条后继通向成功，就泄露了结果。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35084">原论文</a> · <a href="../../../../agent-research/2609.35084-graphhca/">实现解读</a> · <a href="#qa-b3bf6752fef4363f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dependency-refinement" data-paper-title="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning Agent ShanghaiTech University 2026-09-16 把多轮轨迹表示为轮级依赖 DAG，依次执行叶节点裁剪、严格合并和宽松合并，减少冗余消息同时保留最终答案依赖。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。  轨迹精炼 Agent 微调 Agent 交互策略学习：把轨迹反馈变成更新 长多轮训练轨迹为什么不能只按长度截断来减少开销？ 工具轨迹包含观察、推理与动作的依赖，某段很早或很长的内容可能正是最终结论的依据，机械截断会让后文变得不可解释。Dependency Refinement 研究在减少轨迹负担时保留必要语义连接。依赖标注本身可能出错，压短不等于策略学会更多，也不证明被删内容永远无用。 教学例：最早一轮取得授权范围，最后动作依赖它；若只留最近消息，训练样本会像是在没有前提时突然执行操作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-dependency-refinement-97ad396d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4a0523d8d2933e96">长多轮训练轨迹为什么不能只按长度截断来减少开销？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adependency-refinement">Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ShanghaiTech University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具轨迹包含观察、推理与动作的依赖，某段很早或很长的内容可能正是最终结论的依据，机械截断会让后文变得不可解释。Dependency Refinement 研究在减少轨迹负担时保留必要语义连接。依赖标注本身可能出错，压短不等于策略学会更多，也不证明被删内容永远无用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：最早一轮取得授权范围，最后动作依赖它；若只留最近消息，训练样本会像是在没有前提时突然执行操作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18417">原论文</a> · <a href="../../../../agent-research/2609.18417-dependency-refinement/">实现解读</a> · <a href="#qa-4a0523d8d2933e96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dependency-refinement" data-paper-title="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning Agent ShanghaiTech University 2026-09-16 把多轮轨迹表示为轮级依赖 DAG，依次执行叶节点裁剪、严格合并和宽松合并，减少冗余消息同时保留最终答案依赖。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。  轨迹精炼 Agent 微调 Agent 交互策略学习：把轨迹反馈变成更新 为什么压缩多轮轨迹先裁叶节点，而不能按消息长度直接删最长一段？ 依赖 DAG 标记哪些轮次支撑最终答案，叶节点更可能是无下游依赖的冗余分支。后续严格和宽松合并再逐步减少重复，同时维持必要信息流；最长消息可能恰是关键工具证据，纯长度裁剪会把学习样本变成缺因果条件的残缺轨迹。 例如长日志里包含唯一错误码，短闲聊反而无依赖；依赖裁剪应删闲聊叶节点，而不是因为日志长就优先扔掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f59aedad5aa4c32a">为什么压缩多轮轨迹先裁叶节点，而不能按消息长度直接删最长一段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adependency-refinement">Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ShanghaiTech University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>依赖 DAG 标记哪些轮次支撑最终答案，叶节点更可能是无下游依赖的冗余分支。后续严格和宽松合并再逐步减少重复，同时维持必要信息流；最长消息可能恰是关键工具证据，纯长度裁剪会把学习样本变成缺因果条件的残缺轨迹。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长日志里包含唯一错误码，短闲聊反而无依赖；依赖裁剪应删闲聊叶节点，而不是因为日志长就优先扔掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18417">原论文</a> · <a href="../../../../agent-research/2609.18417-dependency-refinement/">实现解读</a> · <a href="#qa-f59aedad5aa4c32a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dependency-refinement" data-paper-title="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning Agent ShanghaiTech University 2026-09-16 把多轮轨迹表示为轮级依赖 DAG，依次执行叶节点裁剪、严格合并和宽松合并，减少冗余消息同时保留最终答案依赖。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。  轨迹精炼 Agent 微调 Agent 交互策略学习：把轨迹反馈变成更新 叶节点裁剪与轮次合并在保留语义上有什么不同？ 裁剪移除不再服务目标的分支，合并把可共同表达的相邻或相关步骤压成更紧凑表示。严格合并约束更强，宽松合并追求进一步压缩但风险更高；处理顺序和依赖不变量需要保留，不能用任意摘要替代。 例如两次重复读取同一状态可考虑合并，但验证与修改之间的因果顺序仍应明确，不能合成一句模糊“已处理”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-79061bfab7fe97d2">叶节点裁剪与轮次合并在保留语义上有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adependency-refinement">Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ShanghaiTech University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>裁剪移除不再服务目标的分支，合并把可共同表达的相邻或相关步骤压成更紧凑表示。严格合并约束更强，宽松合并追求进一步压缩但风险更高；处理顺序和依赖不变量需要保留，不能用任意摘要替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次重复读取同一状态可考虑合并，但验证与修改之间的因果顺序仍应明确，不能合成一句模糊“已处理”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18417">原论文</a> · <a href="../../../../agent-research/2609.18417-dependency-refinement/">实现解读</a> · <a href="#qa-79061bfab7fe97d2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dependency-refinement" data-paper-title="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning Agent ShanghaiTech University 2026-09-16 把多轮轨迹表示为轮级依赖 DAG，依次执行叶节点裁剪、严格合并和宽松合并，减少冗余消息同时保留最终答案依赖。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。  轨迹精炼 Agent 微调 Agent 交互策略学习：把轨迹反馈变成更新 本地可审计 DAG 是否包含真实 LLM 依赖标注器？ 没有。本地只执行给定 fixture DAG 的裁剪合并，验证结构和拒绝路径，不冒充自动语义标注。若输入依赖漏掉关键边，算法可能合法删掉必要轮次；因此压缩率与机制通过不能当实际 Agent fine-tuning 质量或原文效果。 例如 fixture 没标“答案依赖第二轮”，裁剪器无法凭空知道这条语义，测试图正确不能证明开放轨迹依赖抽取正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-453bfd86cb2878fc">本地可审计 DAG 是否包含真实 LLM 依赖标注器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adependency-refinement">Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ShanghaiTech University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地只执行给定 fixture DAG 的裁剪合并，验证结构和拒绝路径，不冒充自动语义标注。若输入依赖漏掉关键边，算法可能合法删掉必要轮次；因此压缩率与机制通过不能当实际 Agent fine-tuning 质量或原文效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 fixture 没标“答案依赖第二轮”，裁剪器无法凭空知道这条语义，测试图正确不能证明开放轨迹依赖抽取正确。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18417">原论文</a> · <a href="../../../../agent-research/2609.18417-dependency-refinement/">实现解读</a> · <a href="#qa-453bfd86cb2878fc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-bandit" data-paper-title="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning Agent Harbin Institute of Technology / Alibaba Cloud 2026-09-12 联合 learnability、transferability 与探索 bonus 分配多 harness 训练预算。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行在线 harness 调度；没有进行大模型 RL。本地执行在线 harness 调度；没有进行大模型 RL。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent RL Harness 调度 Agent 交互策略学习：把轨迹反馈变成更新 在一种 harness 里练得更好，为什么未必能在其他接口下同样进步？ 工具协议、提示和执行流程会改变模型训练时遇到的状态与行为，有些经验只适配特定组织方式。Harness Bandit 研究如何在多个训练 harness 间分配预算，兼顾能否学到和能否迁移。训练内分数上升不等于跨接口泛化，必须把不同评测条件的结果分开。 教学例：模型习惯一种文件编辑命令，在另一框架参数格式不同；继续只练熟悉接口，可能提高本框架分数却不改善迁移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-harness-bandit-ffd58529" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b961ccb8ddc0f357">在一种 harness 里练得更好，为什么未必能在其他接口下同样进步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-bandit">HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology / Alibaba Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具协议、提示和执行流程会改变模型训练时遇到的状态与行为，有些经验只适配特定组织方式。Harness Bandit 研究如何在多个训练 harness 间分配预算，兼顾能否学到和能否迁移。训练内分数上升不等于跨接口泛化，必须把不同评测条件的结果分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：模型习惯一种文件编辑命令，在另一框架参数格式不同；继续只练熟悉接口，可能提高本框架分数却不改善迁移。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13739">原论文</a> · <a href="../../../../agent-research/2609.13739-harness-bandit/">实现解读</a> · <a href="#qa-b961ccb8ddc0f357">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-bandit" data-paper-title="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning Agent Harbin Institute of Technology / Alibaba Cloud 2026-09-12 联合 learnability、transferability 与探索 bonus 分配多 harness 训练预算。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行在线 harness 调度；没有进行大模型 RL。本地执行在线 harness 调度；没有进行大模型 RL。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent RL Harness 调度 Agent 交互策略学习：把轨迹反馈变成更新 learnability 与 transferability 为什么需要同时进入多 harness 的训练调度？ 容易学的框架可能只让策略适应其特殊接口，迁移性强但当前难学的框架又需要更多探索。联合两类信号及 bonus 分配有限训练预算，避免只在一套容易刷分的环境过拟合；调度权重只是训练决策，参考函数或多种子诊断不是跨框架能力证据。 例如框架甲提供很多提示、乙较接近部署接口，不能因为甲短期涨分快就把全部预算都给它，还需考虑学到的技能能否转移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ab71656976360ab1">learnability 与 transferability 为什么需要同时进入多 harness 的训练调度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-bandit">HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology / Alibaba Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>容易学的框架可能只让策略适应其特殊接口，迁移性强但当前难学的框架又需要更多探索。联合两类信号及 bonus 分配有限训练预算，避免只在一套容易刷分的环境过拟合；调度权重只是训练决策，参考函数或多种子诊断不是跨框架能力证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如框架甲提供很多提示、乙较接近部署接口，不能因为甲短期涨分快就把全部预算都给它，还需考虑学到的技能能否转移。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13739">原论文</a> · <a href="../../../../agent-research/2609.13739-harness-bandit/">实现解读</a> · <a href="#qa-ab71656976360ab1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-bandit" data-paper-title="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning Agent Harbin Institute of Technology / Alibaba Cloud 2026-09-12 联合 learnability、transferability 与探索 bonus 分配多 harness 训练预算。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行在线 harness 调度；没有进行大模型 RL。本地执行在线 harness 调度；没有进行大模型 RL。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent RL Harness 调度 Agent 交互策略学习：把轨迹反馈变成更新 固定平均分配多 harness 与 bandit 预算调度有什么取舍？ 平均分配不适应各阶段收益变化，bandit 可把更多样本给当前更值得学习或不确定的环境。它也可能偏向短期代理信号，探索消耗总预算，不能只比较单 harness 训练效率而忽略整个调度成本和迁移评测。 例如某 harness 已饱和后减少其采样，把预算转给尚有可迁移进展的路径，但仍需偶尔重访防估计失真。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0750ff4e3195da29">固定平均分配多 harness 与 bandit 预算调度有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-bandit">HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology / Alibaba Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平均分配不适应各阶段收益变化，bandit 可把更多样本给当前更值得学习或不确定的环境。它也可能偏向短期代理信号，探索消耗总预算，不能只比较单 harness 训练效率而忽略整个调度成本和迁移评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某 harness 已饱和后减少其采样，把预算转给尚有可迁移进展的路径，但仍需偶尔重访防估计失真。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13739">原论文</a> · <a href="../../../../agent-research/2609.13739-harness-bandit/">实现解读</a> · <a href="#qa-0750ff4e3195da29">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-bandit" data-paper-title="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning Agent Harbin Institute of Technology / Alibaba Cloud 2026-09-12 联合 learnability、transferability 与探索 bonus 分配多 harness 训练预算。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行在线 harness 调度；没有进行大模型 RL。本地执行在线 harness 调度；没有进行大模型 RL。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent RL Harness 调度 Agent 交互策略学习：把轨迹反馈变成更新 本地在线 harness 选择计数是否意味着完成多框架大模型 RL？ 没有。本地仅执行门控、分配与状态更新 reference，没有真实大模型 RL、完整 rollout 或迁移 benchmark。合成 learnability/transferability 输入可检查权重响应，不能证明系统已学到可移植能力，也不能从三 seed 调度统计推算效果。 例如给某 arm 较高迁移分后多分配几次，验证的是调度器；若分数由人工给定，还未测模型真实迁移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2437ebba3b51eb5c">本地在线 harness 选择计数是否意味着完成多框架大模型 RL？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-bandit">HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology / Alibaba Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地仅执行门控、分配与状态更新 reference，没有真实大模型 RL、完整 rollout 或迁移 benchmark。合成 learnability/transferability 输入可检查权重响应，不能证明系统已学到可移植能力，也不能从三 seed 调度统计推算效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给某 arm 较高迁移分后多分配几次，验证的是调度器；若分数由人工给定，还未测模型真实迁移。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13739">原论文</a> · <a href="../../../../agent-research/2609.13739-harness-bandit/">实现解读</a> · <a href="#qa-2437ebba3b51eb5c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t1-terminal-rl" data-paper-title="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks Agent National University of Singapore / Tencent 2026-09-09 TITO 使用 rollout 实际采样 token id 训练，turn boundary repair 修正漂移，R3 重放 MoE 路由选择。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent RL 长程终端任务 Agent 交互策略学习：把轨迹反馈变成更新 训练大规模终端 Agent 时，为什么推理轨迹与优化器看到的样本必须一致？ 终端交互包含模型生成、工具观察和可能变化的模型执行路径，训练若重建出不同样本，就会优化并非真正采样的行为。T1 关注让长程 rollout 与后续更新保持可追踪一致，同时支撑大规模训练。记录一致只是训练正确性的条件，不代表任务能力或最终收益已经得到证明。 教学例：工具输出夹在模型回答之间，训练端若重新拼接后改变 token 边界，计算的概率就可能不再对应当时实际动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-t1-terminal-rl-406c9b27" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b5ce8bc476b1bbed">训练大规模终端 Agent 时，为什么推理轨迹与优化器看到的样本必须一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3At1-terminal-rl">T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终端交互包含模型生成、工具观察和可能变化的模型执行路径，训练若重建出不同样本，就会优化并非真正采样的行为。T1 关注让长程 rollout 与后续更新保持可追踪一致，同时支撑大规模训练。记录一致只是训练正确性的条件，不代表任务能力或最终收益已经得到证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：工具输出夹在模型回答之间，训练端若重新拼接后改变 token 边界，计算的概率就可能不再对应当时实际动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11042">原论文</a> · <a href="../../../../agent-research/2609.11042-t1-terminal-rl/">实现解读</a> · <a href="#qa-b5ce8bc476b1bbed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t1-terminal-rl" data-paper-title="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks Agent National University of Singapore / Tencent 2026-09-09 TITO 使用 rollout 实际采样 token id 训练，turn boundary repair 修正漂移，R3 重放 MoE 路由选择。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent RL 长程终端任务 Agent 交互策略学习：把轨迹反馈变成更新 为什么训练要使用 rollout 真正采样的 token ID，而不是把完整交互文本重新分词？ 拼接工具观察与多轮消息后重新分词，边界和 token 可能与实际采样不一致，导致策略概率对应错误动作。TITO 保留真实 ID，边界修复处理漂移，MoE 路由重放再控制专家路径差异；数据对齐正确仍只是训练合同，不等于终端任务已学会。 例如一段命令与下一条观察拼接后形成不同子词，重新分词会把非动作内容也混进训练；保留采样 ID 才能对准原动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1063f6614633db4d">为什么训练要使用 rollout 真正采样的 token ID，而不是把完整交互文本重新分词？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3At1-terminal-rl">T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>拼接工具观察与多轮消息后重新分词，边界和 token 可能与实际采样不一致，导致策略概率对应错误动作。TITO 保留真实 ID，边界修复处理漂移，MoE 路由重放再控制专家路径差异；数据对齐正确仍只是训练合同，不等于终端任务已学会。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一段命令与下一条观察拼接后形成不同子词，重新分词会把非动作内容也混进训练；保留采样 ID 才能对准原动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11042">原论文</a> · <a href="../../../../agent-research/2609.11042-t1-terminal-rl/">实现解读</a> · <a href="#qa-1063f6614633db4d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t1-terminal-rl" data-paper-title="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks Agent National University of Singapore / Tencent 2026-09-09 TITO 使用 rollout 实际采样 token id 训练，turn boundary repair 修正漂移，R3 重放 MoE 路由选择。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent RL 长程终端任务 Agent 交互策略学习：把轨迹反馈变成更新 MoE route replay 与只重放生成 token 有何不同？ 同样输入 token 下专家路由也可能随实现或状态变化，R3 保存并重放路由选择，试图缩小训练推理路径差。token 一致是必要但不充分条件，路由一致也不保证最终任务提升，需真实模型和日志概率对照。 例如某 token 原走专家甲乙，训练重算改走甲丙，会改变输出和梯度，即使 token ID 完全一样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1dad37cdd9124676">MoE route replay 与只重放生成 token 有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3At1-terminal-rl">T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同样输入 token 下专家路由也可能随实现或状态变化，R3 保存并重放路由选择，试图缩小训练推理路径差。token 一致是必要但不充分条件，路由一致也不保证最终任务提升，需真实模型和日志概率对照。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某 token 原走专家甲乙，训练重算改走甲丙，会改变输出和梯度，即使 token ID 完全一样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11042">原论文</a> · <a href="../../../../agent-research/2609.11042-t1-terminal-rl/">实现解读</a> · <a href="#qa-1dad37cdd9124676">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t1-terminal-rl" data-paper-title="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks Agent National University of Singapore / Tencent 2026-09-09 TITO 使用 rollout 实际采样 token id 训练，turn boundary repair 修正漂移，R3 重放 MoE 路由选择。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent RL 长程终端任务 Agent 交互策略学习：把轨迹反馈变成更新 本地 exact-token/route 状态审计能覆盖 122B MoE 训练吗？ 不能。本地只检查采样序列与路由重放状态合同，没有 122B 模型、三百多 turn 云沙箱或完整 terminal RL。日志一致性不等于训练—推理 gap 已实测缩小，原文分数和 gap 属于作者真实系统，不能据字段存在搬用。 例如 fixture route 数组能逐项重放，说明索引协议正常；它未运行真实 MoE dispatch 或反向计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-802e5687f7b00d55">本地 exact-token/route 状态审计能覆盖 122B MoE 训练吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3At1-terminal-rl">T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地只检查采样序列与路由重放状态合同，没有 122B 模型、三百多 turn 云沙箱或完整 terminal RL。日志一致性不等于训练—推理 gap 已实测缩小，原文分数和 gap 属于作者真实系统，不能据字段存在搬用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 fixture route 数组能逐项重放，说明索引协议正常；它未运行真实 MoE dispatch 或反向计算。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11042">原论文</a> · <a href="../../../../agent-research/2609.11042-t1-terminal-rl/">实现解读</a> · <a href="#qa-802e5687f7b00d55">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:multi-harness-rl" data-paper-title="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents Agent New York University 2026-09-03 多 Harness RL 同时改变了执行环境多样性和 GRPO 的分组边界，难以判断增益来源。论文冻结相同 task-harness 轨迹，只比较组内和跨 harness advantage，并用训练中未见的最小 harness 审计能力是否真正迁移。 复现级别：CPU 分组信用与可微训练算子。复现级别：CPU 分组信用与可微训练算子。在相同 rollout 上计算 task×harness 与 task 两种标准化优势；尚不包含真实编码 Agent 的 held-out harness 迁移实验。真实 coding harness、Qwen3-8B RL 和 sealed oracle 均未在本地复刻；该实现用于防止未来 Evolve 实验把 harness 差异误报为模型能力。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Multi-harness RL audit Agent 交互策略学习：把轨迹反馈变成更新 多 harness 强化学习为什么需要区分底座能力与执行接口带来的差异？ 同一任务在不同提示、工具协议和流程下可能呈现不同成功率，训练奖励还会因分组方式改变含义。Multi-Harness RL 研究这种条件变化如何影响学习和迁移。若底座、任务或采样同时变化，就难判断收益来源，因此要控制轨迹与评价口径，而非把跨框架涨分都归为能力增长。 教学例：一种 harness 自动补全参数，另一种要求模型自己填写；成功率差异可能反映接口帮助，不能直接当成底座推理差距。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-multi-harness-rl-66c31df3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c9a85584b1ebed7b">多 harness 强化学习为什么需要区分底座能力与执行接口带来的差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amulti-harness-rl">What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一任务在不同提示、工具协议和流程下可能呈现不同成功率，训练奖励还会因分组方式改变含义。Multi-Harness RL 研究这种条件变化如何影响学习和迁移。若底座、任务或采样同时变化，就难判断收益来源，因此要控制轨迹与评价口径，而非把跨框架涨分都归为能力增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一种 harness 自动补全参数，另一种要求模型自己填写；成功率差异可能反映接口帮助，不能直接当成底座推理差距。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04518">原论文</a> · <a href="../../../../agent-research/2609.04518-multi-harness-rl/">实现解读</a> · <a href="#qa-c9a85584b1ebed7b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:multi-harness-rl" data-paper-title="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents Agent New York University 2026-09-03 多 Harness RL 同时改变了执行环境多样性和 GRPO 的分组边界，难以判断增益来源。论文冻结相同 task-harness 轨迹，只比较组内和跨 harness advantage，并用训练中未见的最小 harness 审计能力是否真正迁移。 复现级别：CPU 分组信用与可微训练算子。复现级别：CPU 分组信用与可微训练算子。在相同 rollout 上计算 task×harness 与 task 两种标准化优势；尚不包含真实编码 Agent 的 held-out harness 迁移实验。真实 coding harness、Qwen3-8B RL 和 sealed oracle 均未在本地复刻；该实现用于防止未来 Evolve 实验把 harness 差异误报为模型能力。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Multi-harness RL audit Agent 交互策略学习：把轨迹反馈变成更新 冻结同一批 task-harness 轨迹，只改 advantage 分组，能隔离哪种混淆？ 多框架训练同时带来数据多样性和信用比较范围变化，直接对比两个完整系统无法区分来源。固定轨迹后，在同 task 内比较跨框架与各自框架标准化，才更集中检验分组影响；迁移还要在训练未见的最小 harness 上报告差异与不确定性。 例如同一道修复题在两种接口产生相同已存轨迹，重新计算分组优势而不重新采样，可减少把采样变化误归因给信用规则。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2cb0d51874f501b1">冻结同一批 task-harness 轨迹，只改 advantage 分组，能隔离哪种混淆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amulti-harness-rl">What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多框架训练同时带来数据多样性和信用比较范围变化，直接对比两个完整系统无法区分来源。固定轨迹后，在同 task 内比较跨框架与各自框架标准化，才更集中检验分组影响；迁移还要在训练未见的最小 harness 上报告差异与不确定性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一道修复题在两种接口产生相同已存轨迹，重新计算分组优势而不重新采样，可减少把采样变化误归因给信用规则。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04518">原论文</a> · <a href="../../../../agent-research/2609.04518-multi-harness-rl/">实现解读</a> · <a href="#qa-2cb0d51874f501b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:multi-harness-rl" data-paper-title="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents Agent New York University 2026-09-03 多 Harness RL 同时改变了执行环境多样性和 GRPO 的分组边界，难以判断增益来源。论文冻结相同 task-harness 轨迹，只比较组内和跨 harness advantage，并用训练中未见的最小 harness 审计能力是否真正迁移。 复现级别：CPU 分组信用与可微训练算子。复现级别：CPU 分组信用与可微训练算子。在相同 rollout 上计算 task×harness 与 task 两种标准化优势；尚不包含真实编码 Agent 的 held-out harness 迁移实验。真实 coding harness、Qwen3-8B RL 和 sealed oracle 均未在本地复刻；该实现用于防止未来 Evolve 实验把 harness 差异误报为模型能力。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Multi-harness RL audit Agent 交互策略学习：把轨迹反馈变成更新 Within 与 Cross 怎样改变同一 reward 的相对意义？ Within 在各 task-harness 内标准化，评价同环境兄弟轨迹；Cross 跨同任务不同 harness 标准化，会把环境间奖励差也带入优势。后者可能学到环境偏好，是否可移植需未见最小 harness 配对验证，不能只看训练均值。 例如工具更强的 harness 整体奖励高，Cross 可能普遍给其正优势；这未必是模型在简约接口也更会修代码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ed1a599911375548">Within 与 Cross 怎样改变同一 reward 的相对意义？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amulti-harness-rl">What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Within 在各 task-harness 内标准化，评价同环境兄弟轨迹；Cross 跨同任务不同 harness 标准化，会把环境间奖励差也带入优势。后者可能学到环境偏好，是否可移植需未见最小 harness 配对验证，不能只看训练均值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具更强的 harness 整体奖励高，Cross 可能普遍给其正优势；这未必是模型在简约接口也更会修代码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04518">原论文</a> · <a href="../../../../agent-research/2609.04518-multi-harness-rl/">实现解读</a> · <a href="#qa-ed1a599911375548">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:multi-harness-rl" data-paper-title="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents Agent New York University 2026-09-03 多 Harness RL 同时改变了执行环境多样性和 GRPO 的分组边界，难以判断增益来源。论文冻结相同 task-harness 轨迹，只比较组内和跨 harness advantage，并用训练中未见的最小 harness 审计能力是否真正迁移。 复现级别：CPU 分组信用与可微训练算子。复现级别：CPU 分组信用与可微训练算子。在相同 rollout 上计算 task×harness 与 task 两种标准化优势；尚不包含真实编码 Agent 的 held-out harness 迁移实验。真实 coding harness、Qwen3-8B RL 和 sealed oracle 均未在本地复刻；该实现用于防止未来 Evolve 实验把 harness 差异误报为模型能力。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Multi-harness RL audit Agent 交互策略学习：把轨迹反馈变成更新 为何 held-out Cross-Within 区间跨零时不能宣称已证实迁移？ 点估计微小正差仍与无变化相容，原文应连同配对置信区间解释。旧 gold-reading 本地分数作废，当前只验证分组、梯度和协议，未复刻 Qwen RL、真实 coding harness 或 sealed oracle，不把计数器包装为 SWE-bench 能力。 例如提升零点二五百分点而区间含负值，证据不足以说稳定优于 Within，更不能省略区间只报正数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f053cdb0bfd492e6">为何 held-out Cross-Within 区间跨零时不能宣称已证实迁移？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amulti-harness-rl">What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点估计微小正差仍与无变化相容，原文应连同配对置信区间解释。旧 gold-reading 本地分数作废，当前只验证分组、梯度和协议，未复刻 Qwen RL、真实 coding harness 或 sealed oracle，不把计数器包装为 SWE-bench 能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如提升零点二五百分点而区间含负值，证据不足以说稳定优于 Within，更不能省略区间只报正数。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04518">原论文</a> · <a href="../../../../agent-research/2609.04518-multi-harness-rl/">实现解读</a> · <a href="#qa-f053cdb0bfd492e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ace-data" data-paper-title="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents Agent Huawei Technologies Co., Ltd 2026-08-27 论文把 Agent 数据统一表示为：环境、任务、交互轨迹与可选 verifier。Accuracy 先限定可信支持集，Complexity 相对指定学习者校准难度，Diversity 再控制环境、任务和行为覆盖。 复现级别：框架可执行化 mini-suite。复现级别：框架可执行化 mini-suite。论文是综述/统一框架；本地把三道约束实现为数据准入门。这是框架的可执行准入合同，不声称复刻某个训练模型或公开 benchmark SOTA。planbench-mini、120 episodes：joint success 1.0000、average cost 0.3700，另记录 accuracy gates、complexity calibration 和 diversity accept/reject。指标见 metrics/planbench-mini-seed42.json。  Agent 数据质量 Agent 交互策略学习：把轨迹反馈变成更新 ACE 为什么认为更多 Agent 轨迹不一定意味着更好的训练数据？ 数据可能答案不准、对当前学习者过难或过于重复，数量增加会同时放大这些问题。ACE 从 Accuracy、Complexity、Diversity 三个角度检查 Agent 数据，让质量与学习适配性进入选择。三者需要真实定义和评测，不能仅凭步骤多、主题多就认定训练一定受益。 教学例：重复一千条错误调用并不会变成好数据；全是模型已熟练完成的简单题，也可能提供很有限的新学习信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-ace-data-9a8b6ddd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5a5ac4e33413cea3">ACE 为什么认为更多 Agent 轨迹不一定意味着更好的训练数据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aace-data">What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies Co., Ltd</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>数据可能答案不准、对当前学习者过难或过于重复，数量增加会同时放大这些问题。ACE 从 Accuracy、Complexity、Diversity 三个角度检查 Agent 数据，让质量与学习适配性进入选择。三者需要真实定义和评测，不能仅凭步骤多、主题多就认定训练一定受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：重复一千条错误调用并不会变成好数据；全是模型已熟练完成的简单题，也可能提供很有限的新学习信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27260">原论文</a> · <a href="../../../../agent-research/2608.27260-ace-data/">实现解读</a> · <a href="#qa-5a5ac4e33413cea3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ace-data" data-paper-title="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents Agent Huawei Technologies Co., Ltd 2026-08-27 论文把 Agent 数据统一表示为：环境、任务、交互轨迹与可选 verifier。Accuracy 先限定可信支持集，Complexity 相对指定学习者校准难度，Diversity 再控制环境、任务和行为覆盖。 复现级别：框架可执行化 mini-suite。复现级别：框架可执行化 mini-suite。论文是综述/统一框架；本地把三道约束实现为数据准入门。这是框架的可执行准入合同，不声称复刻某个训练模型或公开 benchmark SOTA。planbench-mini、120 episodes：joint success 1.0000、average cost 0.3700，另记录 accuracy gates、complexity calibration 和 diversity accept/reject。指标见 metrics/planbench-mini-seed42.json。  Agent 数据质量 Agent 交互策略学习：把轨迹反馈变成更新 为什么 Complexity 必须相对指定学习者校准，而不能只给任务一个固定难度标签？ 同题对不同模型的可学性不同，过易提供少量新信号、过难可能只产生失败。Accuracy 先保证样本可信，学习者相对的复杂度再选有效区间，Diversity 补环境与行为覆盖；三者缺一不可，轨迹长或工具多本身不能证明数据更优。 例如初级模型解三步工具题尚可学习，二十步全失败未必更好；强模型可能正需要后者，课程区间应随学习者变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c709cf44b82a6aa7">为什么 Complexity 必须相对指定学习者校准，而不能只给任务一个固定难度标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aace-data">What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies Co., Ltd</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同题对不同模型的可学性不同，过易提供少量新信号、过难可能只产生失败。Accuracy 先保证样本可信，学习者相对的复杂度再选有效区间，Diversity 补环境与行为覆盖；三者缺一不可，轨迹长或工具多本身不能证明数据更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如初级模型解三步工具题尚可学习，二十步全失败未必更好；强模型可能正需要后者，课程区间应随学习者变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27260">原论文</a> · <a href="../../../../agent-research/2608.27260-ace-data/">实现解读</a> · <a href="#qa-c709cf44b82a6aa7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ace-data" data-paper-title="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents Agent Huawei Technologies Co., Ltd 2026-08-27 论文把 Agent 数据统一表示为：环境、任务、交互轨迹与可选 verifier。Accuracy 先限定可信支持集，Complexity 相对指定学习者校准难度，Diversity 再控制环境、任务和行为覆盖。 复现级别：框架可执行化 mini-suite。复现级别：框架可执行化 mini-suite。论文是综述/统一框架；本地把三道约束实现为数据准入门。这是框架的可执行准入合同，不声称复刻某个训练模型或公开 benchmark SOTA。planbench-mini、120 episodes：joint success 1.0000、average cost 0.3700，另记录 accuracy gates、complexity calibration 和 diversity accept/reject。指标见 metrics/planbench-mini-seed42.json。  Agent 数据质量 Agent 交互策略学习：把轨迹反馈变成更新 Complexity 与 Diversity 分别描述学习挑战还是数据覆盖，为什么不能合并？ Complexity 关注样本对指定学习者的挑战程度，Diversity 关注样本之间和任务空间的覆盖差异。多样数据可以都很简单，困难数据也可以只是同一模式重复。二者还受 Accuracy 前提约束，错误但新奇的轨迹不能因此成为好监督，也不能从静态标签推导实际训练收益。 教学例：十种不同工具的单步调用可能很广但很易；十条同类高难故障题可能很难却覆盖窄，两种数据补足的缺口不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4ec1c6af15d90cb9">Complexity 与 Diversity 分别描述学习挑战还是数据覆盖，为什么不能合并？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aace-data">What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies Co., Ltd</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Complexity 关注样本对指定学习者的挑战程度，Diversity 关注样本之间和任务空间的覆盖差异。多样数据可以都很简单，困难数据也可以只是同一模式重复。二者还受 Accuracy 前提约束，错误但新奇的轨迹不能因此成为好监督，也不能从静态标签推导实际训练收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：十种不同工具的单步调用可能很广但很易；十条同类高难故障题可能很难却覆盖窄，两种数据补足的缺口不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27260">原论文</a> · <a href="../../../../agent-research/2608.27260-ace-data/">实现解读</a> · <a href="#qa-4ec1c6af15d90cb9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ace-data" data-paper-title="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents Agent Huawei Technologies Co., Ltd 2026-08-27 论文把 Agent 数据统一表示为：环境、任务、交互轨迹与可选 verifier。Accuracy 先限定可信支持集，Complexity 相对指定学习者校准难度，Diversity 再控制环境、任务和行为覆盖。 复现级别：框架可执行化 mini-suite。复现级别：框架可执行化 mini-suite。论文是综述/统一框架；本地把三道约束实现为数据准入门。这是框架的可执行准入合同，不声称复刻某个训练模型或公开 benchmark SOTA。planbench-mini、120 episodes：joint success 1.0000、average cost 0.3700，另记录 accuracy gates、complexity calibration 和 diversity accept/reject。指标见 metrics/planbench-mini-seed42.json。  Agent 数据质量 Agent 交互策略学习：把轨迹反馈变成更新 公开 artifact 评测怎样避免把三段准入变成虚构训练结果？ 需固定真实数据 revision，记录环境、问题、轨迹、verifier 和 learner loss，在同预算比较随机与三段选择；本地只有准入合同及产物回放，不声称训练 checkpoint 或 SOTA。来源和失败记录缺失时不能用合成高分补齐。 例如导出 JSONL 通过字段检查只说明可审计输入，若未训练并独立评测模型，就不能报告 ACE 带来任务成功率提升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4855db385496d579">公开 artifact 评测怎样避免把三段准入变成虚构训练结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aace-data">What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies Co., Ltd</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需固定真实数据 revision，记录环境、问题、轨迹、verifier 和 learner loss，在同预算比较随机与三段选择；本地只有准入合同及产物回放，不声称训练 checkpoint 或 SOTA。来源和失败记录缺失时不能用合成高分补齐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如导出 JSONL 通过字段检查只说明可审计输入，若未训练并独立评测模型，就不能报告 ACE 带来任务成功率提升。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27260">原论文</a> · <a href="../../../../agent-research/2608.27260-ace-data/">实现解读</a> · <a href="#qa-4855db385496d579">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ahead" data-paper-title="AHEAD: Agentic Hints for Effective Agent Development" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AHEAD: Agentic Hints for Effective Agent Development Agent AWS AI Labs / Purdue University 2026-08-25 轨迹级 GRPO 给所有步骤同一 advantage；统一 privileged information 又浪费在普通步骤上。AHEAD 先分析失败轨迹定位关键错误：所有步骤的 teacher 都看到环境反馈，只有错误步骤额外看到 LLM corrective hint；teacher/student log-prob gap 被有界地注入 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。普通步骤只用环境反馈，错误步骤再追加 corrective hint，并生成稠密信用。mini-suite 使用确定性错误位置验证 step-aware PI 分流；未运行 LLM analyzer、Qwen、真实 GRPO 或三个原始 benchmark。PlanBench-mini 120 episodes：24 个 error-step hint、360 个 dense-credit 更新，joint success 1.0000，平均成本 0.6160。  环境反馈提示训练 Agent 交互策略学习：把轨迹反馈变成更新 AHEAD 为什么不满足于给长程 Agent 整条轨迹同一个成功或失败反馈？ 轨迹中可能只有少数关键错误决定终局，其他步骤则合理或只是受错误连累，统一信用难以说明应改哪里。AHEAD 研究用针对性的教师信号调整这些步骤的学习重点。更细信号也依赖错误定位可靠性，训练教师的额外信息不能被当成部署 Agent 已知答案。 教学例：多步检索只有第三次查询偏离目标，后续失败不应让所有正确取证步骤承担相同责任；需要识别真正关键的偏差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-ahead-17c82764" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d7aa07df3793e0b8">AHEAD 为什么不满足于给长程 Agent 整条轨迹同一个成功或失败反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aahead">AHEAD: Agentic Hints for Effective Agent Development</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AWS AI Labs / Purdue University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轨迹中可能只有少数关键错误决定终局，其他步骤则合理或只是受错误连累，统一信用难以说明应改哪里。AHEAD 研究用针对性的教师信号调整这些步骤的学习重点。更细信号也依赖错误定位可靠性，训练教师的额外信息不能被当成部署 Agent 已知答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：多步检索只有第三次查询偏离目标，后续失败不应让所有正确取证步骤承担相同责任；需要识别真正关键的偏差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24114">原论文</a> · <a href="../../../../agent-research/2608.24114-ahead/">实现解读</a> · <a href="#qa-d7aa07df3793e0b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ahead" data-paper-title="AHEAD: Agentic Hints for Effective Agent Development" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AHEAD: Agentic Hints for Effective Agent Development Agent AWS AI Labs / Purdue University 2026-08-25 轨迹级 GRPO 给所有步骤同一 advantage；统一 privileged information 又浪费在普通步骤上。AHEAD 先分析失败轨迹定位关键错误：所有步骤的 teacher 都看到环境反馈，只有错误步骤额外看到 LLM corrective hint；teacher/student log-prob gap 被有界地注入 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。普通步骤只用环境反馈，错误步骤再追加 corrective hint，并生成稠密信用。mini-suite 使用确定性错误位置验证 step-aware PI 分流；未运行 LLM analyzer、Qwen、真实 GRPO 或三个原始 benchmark。PlanBench-mini 120 episodes：24 个 error-step hint、360 个 dense-credit 更新，joint success 1.0000，平均成本 0.6160。  环境反馈提示训练 Agent 交互策略学习：把轨迹反馈变成更新 纠错 hint 为什么只额外给关键错误步骤的 teacher，而不是所有步骤都给完整答案提示？ 普通步骤已有环境反馈，统一特权提示会浪费信号并掩盖真正需要纠正的位置。定位错误后，在相同生成动作上比较有无 hint 的对数概率差，再有界调节终局优势；提示只在训练教师侧使用，不能把答案或纠错信息直接放进部署学生上下文。 例如轨迹只有第三步选错工具，额外 hint 应聚焦该决策，而非让每一步都看到最终解决方案再假称学生自主完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b9c59b738ccefc35">纠错 hint 为什么只额外给关键错误步骤的 teacher，而不是所有步骤都给完整答案提示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aahead">AHEAD: Agentic Hints for Effective Agent Development</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AWS AI Labs / Purdue University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通步骤已有环境反馈，统一特权提示会浪费信号并掩盖真正需要纠正的位置。定位错误后，在相同生成动作上比较有无 hint 的对数概率差，再有界调节终局优势；提示只在训练教师侧使用，不能把答案或纠错信息直接放进部署学生上下文。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如轨迹只有第三步选错工具，额外 hint 应聚焦该决策，而非让每一步都看到最终解决方案再假称学生自主完成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24114">原论文</a> · <a href="../../../../agent-research/2608.24114-ahead/">实现解读</a> · <a href="#qa-b9c59b738ccefc35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ahead" data-paper-title="AHEAD: Agentic Hints for Effective Agent Development" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AHEAD: Agentic Hints for Effective Agent Development Agent AWS AI Labs / Purdue University 2026-08-25 轨迹级 GRPO 给所有步骤同一 advantage；统一 privileged information 又浪费在普通步骤上。AHEAD 先分析失败轨迹定位关键错误：所有步骤的 teacher 都看到环境反馈，只有错误步骤额外看到 LLM corrective hint；teacher/student log-prob gap 被有界地注入 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。普通步骤只用环境反馈，错误步骤再追加 corrective hint，并生成稠密信用。mini-suite 使用确定性错误位置验证 step-aware PI 分流；未运行 LLM analyzer、Qwen、真实 GRPO 或三个原始 benchmark。PlanBench-mini 120 episodes：24 个 error-step hint、360 个 dense-credit 更新，joint success 1.0000，平均成本 0.6160。  环境反馈提示训练 Agent 交互策略学习：把轨迹反馈变成更新 乘法调节原 episode advantage 与直接用 teacher gap 当新奖励有什么区别？ 乘法在原优势基础上调节力度，受 clip 和 λ 限制，保留终局信号的角色；直接替换会把教师偏好变成独立目标。gap 反映相同 token 在不同上下文的似然，不是最终成功概率或真实因果贡献。 例如失败轨迹某 token 受 hint 更支持，不应因此无条件当成功动作正奖；它仍受原轨迹 advantage 和有界因子影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e93dbc6554977b2b">乘法调节原 episode advantage 与直接用 teacher gap 当新奖励有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aahead">AHEAD: Agentic Hints for Effective Agent Development</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AWS AI Labs / Purdue University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>乘法在原优势基础上调节力度，受 clip 和 λ 限制，保留终局信号的角色；直接替换会把教师偏好变成独立目标。gap 反映相同 token 在不同上下文的似然，不是最终成功概率或真实因果贡献。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如失败轨迹某 token 受 hint 更支持，不应因此无条件当成功动作正奖；它仍受原轨迹 advantage 和有界因子影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24114">原论文</a> · <a href="../../../../agent-research/2608.24114-ahead/">实现解读</a> · <a href="#qa-e93dbc6554977b2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ahead" data-paper-title="AHEAD: Agentic Hints for Effective Agent Development" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AHEAD: Agentic Hints for Effective Agent Development Agent AWS AI Labs / Purdue University 2026-08-25 轨迹级 GRPO 给所有步骤同一 advantage；统一 privileged information 又浪费在普通步骤上。AHEAD 先分析失败轨迹定位关键错误：所有步骤的 teacher 都看到环境反馈，只有错误步骤额外看到 LLM corrective hint；teacher/student log-prob gap 被有界地注入 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。普通步骤只用环境反馈，错误步骤再追加 corrective hint，并生成稠密信用。mini-suite 使用确定性错误位置验证 step-aware PI 分流；未运行 LLM analyzer、Qwen、真实 GRPO 或三个原始 benchmark。PlanBench-mini 120 episodes：24 个 error-step hint、360 个 dense-credit 更新，joint success 1.0000，平均成本 0.6160。  环境反馈提示训练 Agent 交互策略学习：把轨迹反馈变成更新 本地确定错误位置、真实 ToolRoute 与论文 LLM analyzer 如何区分？ mini-suite 用确定性错误位置验证提示分流，不含 LLM analyzer、Qwen GRPO 或原三 benchmark；ToolRoute 是另一隔离反馈协议，也不能补成原算法完整训练。hint、gold 和参考动作必须只在允许训练侧，test 策略不得读取。 例如 fixture 告诉第六步错误可测试门控，但没有证明模型能从真实失败长轨迹自主找出第六步。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8331787f806cc0e1">本地确定错误位置、真实 ToolRoute 与论文 LLM analyzer 如何区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aahead">AHEAD: Agentic Hints for Effective Agent Development</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AWS AI Labs / Purdue University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>mini-suite 用确定性错误位置验证提示分流，不含 LLM analyzer、Qwen GRPO 或原三 benchmark；ToolRoute 是另一隔离反馈协议，也不能补成原算法完整训练。hint、gold 和参考动作必须只在允许训练侧，test 策略不得读取。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 fixture 告诉第六步错误可测试门控，但没有证明模型能从真实失败长轨迹自主找出第六步。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24114">原论文</a> · <a href="../../../../agent-research/2608.24114-ahead/">实现解读</a> · <a href="#qa-8331787f806cc0e1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spo-plus-plus" data-paper-title="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction Agent Renmin University of China 2026-08-25 SPO 用单 rollout 和持久 prompt value 避免等待 sibling，但 completion 顺序会污染历史，而且 trajectory whitening 与 token-mean actor loss 的测度不一致。SPO++ 按生成策略事件组织证据、dispatch 时冻结 baseline，并用动作 token 数加权标准化 advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每次 dispatch 冻结 prompt value，并按 action-token measure 消费 advantage。确定性 mini-suite 验证事件时间状态与测度对齐；未运行异步 Qwen3.5、ALFWorld 或 Math-TIR 训练。PlanBench-mini 120 episodes：joint success 1.0000，平均成本 0.6400，执行 120 次冻结 value 与 360 个 action-token measure 更新。  异步单流 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 异步 Agent RL 为什么容易受到“哪个任务先完成”的影响？ 长任务耗时不同，异步训练希望先用已返回结果而不等全部同伴，但完成顺序与任务难度、策略版本相关。SPO++ 研究在保持吞吐的同时让优势基线和证据统计对应正确生成事件。快完成不表示更有代表性，训练记录必须追踪采样时的条件，而不是事后随结果回填。 教学例：简单任务先返回并改变历史值，较早发出的难任务晚到时不应被当成在新基线下采样，否则会混入时间顺序偏差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-spo-plus-plus-c1491ed7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-67629927643b2cac">异步 Agent RL 为什么容易受到“哪个任务先完成”的影响？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspo-plus-plus">SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长任务耗时不同，异步训练希望先用已返回结果而不等全部同伴，但完成顺序与任务难度、策略版本相关。SPO++ 研究在保持吞吐的同时让优势基线和证据统计对应正确生成事件。快完成不表示更有代表性，训练记录必须追踪采样时的条件，而不是事后随结果回填。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：简单任务先返回并改变历史值，较早发出的难任务晚到时不应被当成在新基线下采样，否则会混入时间顺序偏差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24870">原论文</a> · <a href="../../../../agent-research/2608.24870-spo-plus-plus/">实现解读</a> · <a href="#qa-67629927643b2cac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spo-plus-plus" data-paper-title="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction Agent Renmin University of China 2026-08-25 SPO 用单 rollout 和持久 prompt value 避免等待 sibling，但 completion 顺序会污染历史，而且 trajectory whitening 与 token-mean actor loss 的测度不一致。SPO++ 按生成策略事件组织证据、dispatch 时冻结 baseline，并用动作 token 数加权标准化 advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每次 dispatch 冻结 prompt value，并按 action-token measure 消费 advantage。确定性 mini-suite 验证事件时间状态与测度对齐；未运行异步 Qwen3.5、ALFWorld 或 Math-TIR 训练。PlanBench-mini 120 episodes：joint success 1.0000，平均成本 0.6400，执行 120 次冻结 value 与 360 个 action-token measure 更新。  异步单流 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么 token-mean actor loss 要用动作 token 数加权 advantage 标准化？ 若每条轨迹只投一票做白化，而损失按 token 平均，长短轨迹在两处的测度不一致，会改变实际更新权重。token 加权让标准化与优化对象一致，dispatch 冻结 baseline 又防止异步完成顺序污染历史；它不是简单把奖励按文本长度重新定义。 例如一条十 token、一条一百 token，损失中后者占更多位置，标准化若各算一票，就与真实梯度平均的权重不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-12fbffeabf99f50b">为什么 token-mean actor loss 要用动作 token 数加权 advantage 标准化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspo-plus-plus">SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若每条轨迹只投一票做白化，而损失按 token 平均，长短轨迹在两处的测度不一致，会改变实际更新权重。token 加权让标准化与优化对象一致，dispatch 冻结 baseline 又防止异步完成顺序污染历史；它不是简单把奖励按文本长度重新定义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条十 token、一条一百 token，损失中后者占更多位置，标准化若各算一票，就与真实梯度平均的权重不一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24870">原论文</a> · <a href="../../../../agent-research/2608.24870-spo-plus-plus/">实现解读</a> · <a href="#qa-12fbffeabf99f50b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spo-plus-plus" data-paper-title="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction Agent Renmin University of China 2026-08-25 SPO 用单 rollout 和持久 prompt value 避免等待 sibling，但 completion 顺序会污染历史，而且 trajectory whitening 与 token-mean actor loss 的测度不一致。SPO++ 按生成策略事件组织证据、dispatch 时冻结 baseline，并用动作 token 数加权标准化 advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每次 dispatch 冻结 prompt value，并按 action-token measure 消费 advantage。确定性 mini-suite 验证事件时间状态与测度对齐；未运行异步 Qwen3.5、ALFWorld 或 Math-TIR 训练。PlanBench-mini 120 episodes：joint success 1.0000，平均成本 0.6400，执行 120 次冻结 value 与 360 个 action-token measure 更新。  异步单流 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 按 dispatch 事件冻结 baseline，与按完成顺序取最新 baseline，会改变什么条件？ dispatch 冻结让每条 rollout 的优势对应其发出时可见的 prompt value；完成时取最新值会掺入后来才到达的其他结果，且耗时不同的轨迹受影响程度不同。SPO++ 将证据按生成策略事件组织，不能用事后历史覆盖已冻结条件；这与 token 加权标准化是另一项独立修正。 教学例：轨迹甲先发后到，乙后发先到；乙的结果可更新未来基线，但不能倒写进甲发出时本不存在的历史信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3c83d8cdc2ba5e67">按 dispatch 事件冻结 baseline，与按完成顺序取最新 baseline，会改变什么条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspo-plus-plus">SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>dispatch 冻结让每条 rollout 的优势对应其发出时可见的 prompt value；完成时取最新值会掺入后来才到达的其他结果，且耗时不同的轨迹受影响程度不同。SPO++ 将证据按生成策略事件组织，不能用事后历史覆盖已冻结条件；这与 token 加权标准化是另一项独立修正。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：轨迹甲先发后到，乙后发先到；乙的结果可更新未来基线，但不能倒写进甲发出时本不存在的历史信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24870">原论文</a> · <a href="../../../../agent-research/2608.24870-spo-plus-plus/">实现解读</a> · <a href="#qa-3c83d8cdc2ba5e67">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spo-plus-plus" data-paper-title="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction Agent Renmin University of China 2026-08-25 SPO 用单 rollout 和持久 prompt value 避免等待 sibling，但 completion 顺序会污染历史，而且 trajectory whitening 与 token-mean actor loss 的测度不一致。SPO++ 按生成策略事件组织证据、dispatch 时冻结 baseline，并用动作 token 数加权标准化 advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每次 dispatch 冻结 prompt value，并按 action-token measure 消费 advantage。确定性 mini-suite 验证事件时间状态与测度对齐；未运行异步 Qwen3.5、ALFWorld 或 Math-TIR 训练。PlanBench-mini 120 episodes：joint success 1.0000，平均成本 0.6400，执行 120 次冻结 value 与 360 个 action-token measure 更新。  异步单流 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 本地事件时间和 token measure 验证包含异步 Qwen 训练吗？ 没有。本地在确定性 mini-suite 检查冻结 value、历史时序和动作 token 加权公式，未运行真实异步模型、ALFWorld 或 Math-TIR。事件计数可以验证分支实际发生，但不等于论文 reward-curve area 或吞吐收益。 例如人为乱序完成十条 fixture 后统计仍正确，能测时序合同，尚未测真实 worker 延迟、模型陈旧度和参数更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-de233a30a2539d90">本地事件时间和 token measure 验证包含异步 Qwen 训练吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspo-plus-plus">SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地在确定性 mini-suite 检查冻结 value、历史时序和动作 token 加权公式，未运行真实异步模型、ALFWorld 或 Math-TIR。事件计数可以验证分支实际发生，但不等于论文 reward-curve area 或吞吐收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人为乱序完成十条 fixture 后统计仍正确，能测时序合同，尚未测真实 worker 延迟、模型陈旧度和参数更新。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24870">原论文</a> · <a href="../../../../agent-research/2608.24870-spo-plus-plus/">实现解读</a> · <a href="#qa-de233a30a2539d90">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-g2" data-paper-title="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning Agent Baidu 2026-08-24 Hint-based Agent RL 保留专家轨迹前缀再让策略探索，但固定深度忽略任务难度，逐样本 probe 又浪费 rollout。Agent-G² 从已有 policy rollout 按难度簇估计 guidance band 的中心和方差，对每个任务采样不同前缀深度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每个任务从在线更新的高斯分布采样专家前缀深度，不额外执行 probe rollout。mini-suite 验证按任务簇在线估计、Gaussian sampling 和专家前缀/策略续写的控制流；没有运行 Qwen2.5、ALFWorld/WebShop 或真实 GRPO。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，在线采样 guidance 120 次，平均成本 0.8253。指标见 metrics/planbench-mini-seed42.json。  高斯 guidance Agent RL Agent 交互策略学习：把轨迹反馈变成更新 Agent-G² 为什么在探索前提供部分专家轨迹，而非始终全靠随机试错？ 专家前缀能把策略带到较有学习价值的位置，再由当前策略续写探索。方法按已有rollout估计不同难度簇所需guidance比例，希望兼顾帮助与自主学习，避免逐样本昂贵probe。 示意：难任务可给更长起步提示，容易任务则让策略更早接手。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent-g2-1fe5ec6c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9bb87fa93054b0b0">Agent-G² 为什么在探索前提供部分专家轨迹，而非始终全靠随机试错？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-g2">Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>专家前缀能把策略带到较有学习价值的位置，再由当前策略续写探索。方法按已有rollout估计不同难度簇所需guidance比例，希望兼顾帮助与自主学习，避免逐样本昂贵probe。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>难任务可给更长起步提示，容易任务则让策略更早接手。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23318">原论文</a> · <a href="../../../../agent-research/2608.23318-agent-g2/">实现解读</a> · <a href="#qa-9bb87fa93054b0b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-g2" data-paper-title="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning Agent Baidu 2026-08-24 Hint-based Agent RL 保留专家轨迹前缀再让策略探索，但固定深度忽略任务难度，逐样本 probe 又浪费 rollout。Agent-G² 从已有 policy rollout 按难度簇估计 guidance band 的中心和方差，对每个任务采样不同前缀深度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每个任务从在线更新的高斯分布采样专家前缀深度，不额外执行 probe rollout。mini-suite 验证按任务簇在线估计、Gaussian sampling 和专家前缀/策略续写的控制流；没有运行 Qwen2.5、ALFWorld/WebShop 或真实 GRPO。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，在线采样 guidance 120 次，平均成本 0.8253。指标见 metrics/planbench-mini-seed42.json。  高斯 guidance Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么 guidance 深度要按难度簇采样，而不是所有任务都保留相同长度的专家前缀？ 简单题给过多前缀会减少自主探索，难题给太少又可能只产生失败。已有 rollout 的簇级成功率与波动用于调整引导带中心和方差，再为任务采样深度，减少逐题额外 probe；训练前缀是脚手架，评测不能继续提供参考专家轨迹来冒充独立解题。 例如简单开门题只给很短提示，复杂多房间任务可给较长起步；固定一半前缀会让前者过度依赖、后者仍难学。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6889355ac6f32e8c">为什么 guidance 深度要按难度簇采样，而不是所有任务都保留相同长度的专家前缀？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-g2">Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>简单题给过多前缀会减少自主探索，难题给太少又可能只产生失败。已有 rollout 的簇级成功率与波动用于调整引导带中心和方差，再为任务采样深度，减少逐题额外 probe；训练前缀是脚手架，评测不能继续提供参考专家轨迹来冒充独立解题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如简单开门题只给很短提示，复杂多房间任务可给较长起步；固定一半前缀会让前者过度依赖、后者仍难学。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23318">原论文</a> · <a href="../../../../agent-research/2608.23318-agent-g2/">实现解读</a> · <a href="#qa-6889355ac6f32e8c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-g2" data-paper-title="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning Agent Baidu 2026-08-24 Hint-based Agent RL 保留专家轨迹前缀再让策略探索，但固定深度忽略任务难度，逐样本 probe 又浪费 rollout。Agent-G² 从已有 policy rollout 按难度簇估计 guidance band 的中心和方差，对每个任务采样不同前缀深度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每个任务从在线更新的高斯分布采样专家前缀深度，不额外执行 probe rollout。mini-suite 验证按任务簇在线估计、Gaussian sampling 和专家前缀/策略续写的控制流；没有运行 Qwen2.5、ALFWorld/WebShop 或真实 GRPO。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，在线采样 guidance 120 次，平均成本 0.8253。指标见 metrics/planbench-mini-seed42.json。  高斯 guidance Agent RL Agent 交互策略学习：把轨迹反馈变成更新 按簇估计 guidance band，与每题单独反复 probe 有什么成本差异？ 簇统计复用已有policy rollout的成功率与变化信息，减少额外逐题探测；逐题probe可能更细，但要额外付rollout成本。固定或按簇帮助也不能视为已知道每题最优深度。 示意：同类任务可共享一个深度分布，而不为每题先跑很多次找起点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-70610fe508fd57ba">按簇估计 guidance band，与每题单独反复 probe 有什么成本差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-g2">Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>簇统计复用已有policy rollout的成功率与变化信息，减少额外逐题探测；逐题probe可能更细，但要额外付rollout成本。固定或按簇帮助也不能视为已知道每题最优深度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同类任务可共享一个深度分布，而不为每题先跑很多次找起点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23318">原论文</a> · <a href="../../../../agent-research/2608.23318-agent-g2/">实现解读</a> · <a href="#qa-70610fe508fd57ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-g2" data-paper-title="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning Agent Baidu 2026-08-24 Hint-based Agent RL 保留专家轨迹前缀再让策略探索，但固定深度忽略任务难度，逐样本 probe 又浪费 rollout。Agent-G² 从已有 policy rollout 按难度簇估计 guidance band 的中心和方差，对每个任务采样不同前缀深度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每个任务从在线更新的高斯分布采样专家前缀深度，不额外执行 probe rollout。mini-suite 验证按任务簇在线估计、Gaussian sampling 和专家前缀/策略续写的控制流；没有运行 Qwen2.5、ALFWorld/WebShop 或真实 GRPO。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，在线采样 guidance 120 次，平均成本 0.8253。指标见 metrics/planbench-mini-seed42.json。  高斯 guidance Agent RL Agent 交互策略学习：把轨迹反馈变成更新 Agent-G² 采样到负深度或超过整条专家轨迹的比例时怎么办？ 文档先为均值设边界，再将高斯样本clip到[0,1]；方差也有下限。专家前缀是训练guidance，不应把隐藏专家计划直接交给独立能力评测中的策略。 示意：一次采样r=1.2需裁到1，不能索引到轨迹之外或把越界当成额外oracle信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e4661243a36cc425">Agent-G² 采样到负深度或超过整条专家轨迹的比例时怎么办？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-g2">Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档先为均值设边界，再将高斯样本clip到[0,1]；方差也有下限。专家前缀是训练guidance，不应把隐藏专家计划直接交给独立能力评测中的策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次采样r=1.2需裁到1，不能索引到轨迹之外或把越界当成额外oracle信息。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23318">原论文</a> · <a href="../../../../agent-research/2608.23318-agent-g2/">实现解读</a> · <a href="#qa-e4661243a36cc425">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autosaddler" data-paper-title="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces Agent Microsoft / POSTECH 2026-08-24 长任务中 prompt、tool configuration 和 middleware 的小错误会累积，而人工调 harness 成本高。AutoSaddler 把 harness 当代码：从 mini-batch 失败 trace 做深度诊断，生成有边界的结构化 patch，在同 batch 检查因果效果，再用 dev set 选更新并写入 EvoDAG，形成可持续版本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际执行深度失败诊断、结构化 patch、局部/held-out 验证和 durable harness 更新。没有运行 GAIA2、SWE-Bench Pro、Terminal-Bench 2.0 或论文的生产 harness；本地只验证优化循环、验证边界和 durable reuse。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，12 次 failure diagnosis 与 durable update、108 次复用，平均成本 0.5440。  Harness 自动优化 Agent 交互策略学习：把轨迹反馈变成更新 AutoSaddler 为什么希望一次任务的失败能转化为以后任务也可利用的流程改进？ 长任务中的提示、工具配置和中间件缺陷会反复造成相似失败，只修当前回答难以消除共享原因。AutoSaddler 从执行证据提出有边界的 harness 改动，并维护持续版本。候选补丁只是提案，只有实际验证和后续复用才能说明其作用，版本数不能代替能力证据。 教学例：多次漏掉提交前测试，可尝试修共享执行流程；手动补跑当前任务的测试只修了一次交付，并未保证以后不再遗漏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-autosaddler-3e805f29" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-311080cb265d3c16">AutoSaddler 为什么希望一次任务的失败能转化为以后任务也可利用的流程改进？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautosaddler">AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft / POSTECH</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长任务中的提示、工具配置和中间件缺陷会反复造成相似失败，只修当前回答难以消除共享原因。AutoSaddler 从执行证据提出有边界的 harness 改动，并维护持续版本。候选补丁只是提案，只有实际验证和后续复用才能说明其作用，版本数不能代替能力证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：多次漏掉提交前测试，可尝试修共享执行流程；手动补跑当前任务的测试只修了一次交付，并未保证以后不再遗漏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23041">原论文</a> · <a href="../../../../agent-research/2608.23041-autosaddler/">实现解读</a> · <a href="#qa-311080cb265d3c16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autosaddler" data-paper-title="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces Agent Microsoft / POSTECH 2026-08-24 长任务中 prompt、tool configuration 和 middleware 的小错误会累积，而人工调 harness 成本高。AutoSaddler 把 harness 当代码：从 mini-batch 失败 trace 做深度诊断，生成有边界的结构化 patch，在同 batch 检查因果效果，再用 dev set 选更新并写入 EvoDAG，形成可持续版本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际执行深度失败诊断、结构化 patch、局部/held-out 验证和 durable harness 更新。没有运行 GAIA2、SWE-Bench Pro、Terminal-Bench 2.0 或论文的生产 harness；本地只验证优化循环、验证边界和 durable reuse。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，12 次 failure diagnosis 与 durable update、108 次复用，平均成本 0.5440。  Harness 自动优化 Agent 交互策略学习：把轨迹反馈变成更新 同 batch 检查 patch 效果后，为什么还要在 dev set 选择并写 EvoDAG？ 原失败 batch 适合诊断因果方向，却可能被针对性补丁过拟合。开发集再比较更新，版本图记录从哪个父框架与证据产生，支持后续迭代和回溯；结构化 patch 有边界不等于语义安全，测试报告集也不能加入循环选更新。 例如补丁恰好修好三条相同报错，需要再看其他开发任务是否退化，并保存父子关系，而不是立刻覆盖唯一框架文件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-829d316001b1c096">同 batch 检查 patch 效果后，为什么还要在 dev set 选择并写 EvoDAG？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautosaddler">AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft / POSTECH</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原失败 batch 适合诊断因果方向，却可能被针对性补丁过拟合。开发集再比较更新，版本图记录从哪个父框架与证据产生，支持后续迭代和回溯；结构化 patch 有边界不等于语义安全，测试报告集也不能加入循环选更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如补丁恰好修好三条相同报错，需要再看其他开发任务是否退化，并保存父子关系，而不是立刻覆盖唯一框架文件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23041">原论文</a> · <a href="../../../../agent-research/2608.23041-autosaddler/">实现解读</a> · <a href="#qa-829d316001b1c096">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autosaddler" data-paper-title="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces Agent Microsoft / POSTECH 2026-08-24 长任务中 prompt、tool configuration 和 middleware 的小错误会累积，而人工调 harness 成本高。AutoSaddler 把 harness 当代码：从 mini-batch 失败 trace 做深度诊断，生成有边界的结构化 patch，在同 batch 检查因果效果，再用 dev set 选更新并写入 EvoDAG，形成可持续版本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际执行深度失败诊断、结构化 patch、局部/held-out 验证和 durable harness 更新。没有运行 GAIA2、SWE-Bench Pro、Terminal-Bench 2.0 或论文的生产 harness；本地只验证优化循环、验证边界和 durable reuse。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，12 次 failure diagnosis 与 durable update、108 次复用，平均成本 0.5440。  Harness 自动优化 Agent 交互策略学习：把轨迹反馈变成更新 修改 harness 代码与更新底座模型权重，改变的是哪一种长期状态？ harness 修改影响提示、工具配置或中间件如何组织后续执行，底座权重更新则改变模型本身的行为分布。AutoSaddler 将前者作为可持续代码资产迭代，不需要把一次流程修复称为模型已经训练。两类改进可互补，但证据、版本与回退对象都应分别记录。 教学例：加入测试失败时的恢复分支是流程代码变化；若模型仍用原 checkpoint，就不能据此说它的参数学会了错误恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1064a26346ac437f">修改 harness 代码与更新底座模型权重，改变的是哪一种长期状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautosaddler">AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft / POSTECH</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>harness 修改影响提示、工具配置或中间件如何组织后续执行，底座权重更新则改变模型本身的行为分布。AutoSaddler 将前者作为可持续代码资产迭代，不需要把一次流程修复称为模型已经训练。两类改进可互补，但证据、版本与回退对象都应分别记录。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：加入测试失败时的恢复分支是流程代码变化；若模型仍用原 checkpoint，就不能据此说它的参数学会了错误恢复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23041">原论文</a> · <a href="../../../../agent-research/2608.23041-autosaddler/">实现解读</a> · <a href="#qa-1064a26346ac437f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autosaddler" data-paper-title="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces Agent Microsoft / POSTECH 2026-08-24 长任务中 prompt、tool configuration 和 middleware 的小错误会累积，而人工调 harness 成本高。AutoSaddler 把 harness 当代码：从 mini-batch 失败 trace 做深度诊断，生成有边界的结构化 patch，在同 batch 检查因果效果，再用 dev set 选更新并写入 EvoDAG，形成可持续版本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际执行深度失败诊断、结构化 patch、局部/held-out 验证和 durable harness 更新。没有运行 GAIA2、SWE-Bench Pro、Terminal-Bench 2.0 或论文的生产 harness；本地只验证优化循环、验证边界和 durable reuse。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，12 次 failure diagnosis 与 durable update、108 次复用，平均成本 0.5440。  Harness 自动优化 Agent 交互策略学习：把轨迹反馈变成更新 本地 durable update 和 reuse 计数能够代表什么？ 它们证明公共 mini-suite 中优化循环、验证门与持久复用状态运行，没有原 GAIA2、SWE-Bench Pro、Terminal-Bench 或生产 harness。失败诊断和写入次数不是实际 LLM 深诊断能力，代理成本也不等于真实 API、人效或线上收益。 例如十二次规则更新后复用一百零八次可核对版本路径，但未执行真实模型和工具，不能移用作者九到十点提升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5f24efb3681d1296">本地 durable update 和 reuse 计数能够代表什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautosaddler">AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft / POSTECH</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它们证明公共 mini-suite 中优化循环、验证门与持久复用状态运行，没有原 GAIA2、SWE-Bench Pro、Terminal-Bench 或生产 harness。失败诊断和写入次数不是实际 LLM 深诊断能力，代理成本也不等于真实 API、人效或线上收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十二次规则更新后复用一百零八次可核对版本路径，但未执行真实模型和工具，不能移用作者九到十点提升。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23041">原论文</a> · <a href="../../../../agent-research/2608.23041-autosaddler/">实现解读</a> · <a href="#qa-5f24efb3681d1296">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auso" data-paper-title="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization Agent University of Science and Technology of China 2026-08-21 外部技能检索有上下文开销，完全内化又失去按任务选择能力；按整条轨迹成功率硬切阶段还无法判断某一个动作是否真正受益。AUSO 先用 skill-conditioned teacher 内化通用技能，再进行 outcome-driven exploration，最后对每个动作比较有技能和无技能策略的 JSD，以有界权重调整 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行技能内化、无技能/有技能动作分布 JSD、bounded utilization weight 和复用阶段切换。未运行 ALFWorld/WebShop/SearchQA、大模型 token rollout 或完整 GRPO；确定性 mini-suite 验证 progressive lifecycle、JSD 信息增益和 bounded reweighting 的控制流，不把成本代理指标冒充论文成功率。本地对照口径：基线为同一 PlanBench-mini、120 episodes 的 SkillRise；  动作级技能优化 Agent 交互策略学习：把轨迹反馈变成更新 AUSO 为什么既要内化技能，又保留按动作利用技能的阶段？ 外部技能每次检索有上下文成本，完全内化又不易按任务选择。AUSO先让技能teacher帮助通用内化，再探索，并逐动作比较有无技能的分布差异，调整学习重点。 示意：常用步骤可以学进策略，但某个复杂动作仍可能从特定技能提示获益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-auso-a7af1bb4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4d23c8a96e53e3ca">AUSO 为什么既要内化技能，又保留按动作利用技能的阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aauso">AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>外部技能每次检索有上下文成本，完全内化又不易按任务选择。AUSO先让技能teacher帮助通用内化，再探索，并逐动作比较有无技能的分布差异，调整学习重点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>常用步骤可以学进策略，但某个复杂动作仍可能从特定技能提示获益。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21292">原论文</a> · <a href="../../../../agent-research/2608.21292-auso/">实现解读</a> · <a href="#qa-4d23c8a96e53e3ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auso" data-paper-title="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization Agent University of Science and Technology of China 2026-08-21 外部技能检索有上下文开销，完全内化又失去按任务选择能力；按整条轨迹成功率硬切阶段还无法判断某一个动作是否真正受益。AUSO 先用 skill-conditioned teacher 内化通用技能，再进行 outcome-driven exploration，最后对每个动作比较有技能和无技能策略的 JSD，以有界权重调整 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行技能内化、无技能/有技能动作分布 JSD、bounded utilization weight 和复用阶段切换。未运行 ALFWorld/WebShop/SearchQA、大模型 token rollout 或完整 GRPO；确定性 mini-suite 验证 progressive lifecycle、JSD 信息增益和 bounded reweighting 的控制流，不把成本代理指标冒充论文成功率。本地对照口径：基线为同一 PlanBench-mini、120 episodes 的 SkillRise；  动作级技能优化 Agent 交互策略学习：把轨迹反馈变成更新 动作级 JSD 调权为什么要有界且不翻转原轨迹 advantage 的符号？ 有无技能的分布差说明该动作受技能影响多大，却不直接证明它有益。保留结果优势符号，让局部权重只调节信用强弱，避免把失败轨迹某步因分歧大就变成正奖励；内化、探索和利用分阶段处理，也减少外部技能上下文的持续开销。 例如一次失败中某动作很依赖技能，可以加强对其错误的学习力度，但不能仅因依赖强就把这一步改奖为成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-229676a9ebe02981">动作级 JSD 调权为什么要有界且不翻转原轨迹 advantage 的符号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aauso">AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有无技能的分布差说明该动作受技能影响多大，却不直接证明它有益。保留结果优势符号，让局部权重只调节信用强弱，避免把失败轨迹某步因分歧大就变成正奖励；内化、探索和利用分阶段处理，也减少外部技能上下文的持续开销。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次失败中某动作很依赖技能，可以加强对其错误的学习力度，但不能仅因依赖强就把这一步改奖为成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21292">原论文</a> · <a href="../../../../agent-research/2608.21292-auso/">实现解读</a> · <a href="#qa-229676a9ebe02981">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auso" data-paper-title="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization Agent University of Science and Technology of China 2026-08-21 外部技能检索有上下文开销，完全内化又失去按任务选择能力；按整条轨迹成功率硬切阶段还无法判断某一个动作是否真正受益。AUSO 先用 skill-conditioned teacher 内化通用技能，再进行 outcome-driven exploration，最后对每个动作比较有技能和无技能策略的 JSD，以有界权重调整 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行技能内化、无技能/有技能动作分布 JSD、bounded utilization weight 和复用阶段切换。未运行 ALFWorld/WebShop/SearchQA、大模型 token rollout 或完整 GRPO；确定性 mini-suite 验证 progressive lifecycle、JSD 信息增益和 bounded reweighting 的控制流，不把成本代理指标冒充论文成功率。本地对照口径：基线为同一 PlanBench-mini、120 episodes 的 SkillRise；  动作级技能优化 Agent 交互策略学习：把轨迹反馈变成更新 AUSO 的动作级 JSD，与整条轨迹是否成功提供的信息相同吗？ 最终成功只能说明整条过程的结果；动作级分布差异显示某一步对技能条件的敏感性。差异不自动等于技能带来的因果收益，仍需结合结果和有界调权，而非只因JSD大就认定更优。 示意：同一成功轨迹中，只有一次工具选择可能真正受到技能信息影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0132b36c11bbbdf1">AUSO 的动作级 JSD，与整条轨迹是否成功提供的信息相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aauso">AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终成功只能说明整条过程的结果；动作级分布差异显示某一步对技能条件的敏感性。差异不自动等于技能带来的因果收益，仍需结合结果和有界调权，而非只因JSD大就认定更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一成功轨迹中，只有一次工具选择可能真正受到技能信息影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21292">原论文</a> · <a href="../../../../agent-research/2608.21292-auso/">实现解读</a> · <a href="#qa-0132b36c11bbbdf1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auso" data-paper-title="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization Agent University of Science and Technology of China 2026-08-21 外部技能检索有上下文开销，完全内化又失去按任务选择能力；按整条轨迹成功率硬切阶段还无法判断某一个动作是否真正受益。AUSO 先用 skill-conditioned teacher 内化通用技能，再进行 outcome-driven exploration，最后对每个动作比较有技能和无技能策略的 JSD，以有界权重调整 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行技能内化、无技能/有技能动作分布 JSD、bounded utilization weight 和复用阶段切换。未运行 ALFWorld/WebShop/SearchQA、大模型 token rollout 或完整 GRPO；确定性 mini-suite 验证 progressive lifecycle、JSD 信息增益和 bounded reweighting 的控制流，不把成本代理指标冒充论文成功率。本地对照口径：基线为同一 PlanBench-mini、120 episodes 的 SkillRise；  动作级技能优化 Agent 交互策略学习：把轨迹反馈变成更新 比较有技能和无技能策略时，为什么要使用相同 h_t 和动作分布口径？ 上下文若同时变化，JSD就混入其它条件差异；应在同一动作边界比较两份分布。调权还需核对实际w非负及有界，不能只写出1±β就忽略保advantage符号的条件。 示意：一边多看了工具结果、另一边没看时，分布差异不能只归因于技能S。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d5de36efbae3b19f">比较有技能和无技能策略时，为什么要使用相同 h_t 和动作分布口径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aauso">AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>上下文若同时变化，JSD就混入其它条件差异；应在同一动作边界比较两份分布。调权还需核对实际w非负及有界，不能只写出1±β就忽略保advantage符号的条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一边多看了工具结果、另一边没看时，分布差异不能只归因于技能S。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21292">原论文</a> · <a href="../../../../agent-research/2608.21292-auso/">实现解读</a> · <a href="#qa-d5de36efbae3b19f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sapo" data-paper-title="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning Agent Xiamen University 2026-08-20 同一自回归骨干在不同因果边界输出 policy/value，结合 PPO、on-policy SARSA 和 trajectory GAE。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 SAPO 为什么希望一个自回归骨干同时提供 policy 与 value？ 共享骨干可在不同因果位置读出动作决策和价值信号，再结合PPO、on-policy SARSA及轨迹GAE。共享参数不表示两种读出可以无视各自输入边界。 示意：动作生成前的策略信息，与后续可用于价值估计的信息应按协议区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-sapo-b38c3177" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-87217be71f41ec4d">SAPO 为什么希望一个自回归骨干同时提供 policy 与 value？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asapo">SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享骨干可在不同因果位置读出动作决策和价值信号，再结合PPO、on-policy SARSA及轨迹GAE。共享参数不表示两种读出可以无视各自输入边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>动作生成前的策略信息，与后续可用于价值估计的信息应按协议区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19842">原论文</a> · <a href="../../../../agent-research/2608.19842-sapo/">实现解读</a> · <a href="#qa-87217be71f41ec4d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sapo" data-paper-title="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning Agent Xiamen University 2026-08-20 同一自回归骨干在不同因果边界输出 policy/value，结合 PPO、on-policy SARSA 和 trajectory GAE。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 同一自回归骨干输出 policy 和 value 时，为什么必须指定不同因果边界？ 动作概率应只条件化于决策前可见历史，价值估计也要对应正确时点，混入动作后观察会使优势携带未来信息。共享骨干节省模型结构，但 PPO、SARSA 与 GAE 的状态动作对齐仍要严格维护，单 rollout 不表示可以忽略 bootstrap 与终止语义。 例如决定运行命令前的 value 不能先读到该命令测试通过的输出，否则策略看似获得精确信用，实则泄漏了未来结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-de81b8c4f559f15f">同一自回归骨干输出 policy 和 value 时，为什么必须指定不同因果边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asapo">SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动作概率应只条件化于决策前可见历史，价值估计也要对应正确时点，混入动作后观察会使优势携带未来信息。共享骨干节省模型结构，但 PPO、SARSA 与 GAE 的状态动作对齐仍要严格维护，单 rollout 不表示可以忽略 bootstrap 与终止语义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如决定运行命令前的 value 不能先读到该命令测试通过的输出，否则策略看似获得精确信用，实则泄漏了未来结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19842">原论文</a> · <a href="../../../../agent-research/2608.19842-sapo/">实现解读</a> · <a href="#qa-de81b8c4f559f15f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sapo" data-paper-title="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning Agent Xiamen University 2026-08-20 同一自回归骨干在不同因果边界输出 policy/value，结合 PPO、on-policy SARSA 和 trajectory GAE。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 单 rollout 的轨迹优化，与同一状态先采很多分支再做组比较有何区别？ SAPO强调从单条on-policy过程组织policy/value和时序优势，分支组比较则依赖多个候选rollout。数据需求、价值估计和信用分配口径不同，不能只看最终成功率就当成同一训练方式。 示意：只有一条已执行轨迹时，不能假定还拥有同状态其它候选的真实回报。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-31317deb3033a79a">单 rollout 的轨迹优化，与同一状态先采很多分支再做组比较有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asapo">SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SAPO强调从单条on-policy过程组织policy/value和时序优势，分支组比较则依赖多个候选rollout。数据需求、价值估计和信用分配口径不同，不能只看最终成功率就当成同一训练方式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只有一条已执行轨迹时，不能假定还拥有同状态其它候选的真实回报。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19842">原论文</a> · <a href="../../../../agent-research/2608.19842-sapo/">实现解读</a> · <a href="#qa-31317deb3033a79a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sapo" data-paper-title="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning Agent Xiamen University 2026-08-20 同一自回归骨干在不同因果边界输出 policy/value，结合 PPO、on-policy SARSA 和 trajectory GAE。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 GAE 计算为什么要保留 trajectory 边界，而不能把多个 episode 直接串接？ 优势沿后续TD残差累积，跨episode串接会把另一个任务的回报传进当前任务。需按终止边界处理bootstrap与累积；当前确定性mini-suite不等于真实浏览器或完整RL训练。 示意：任务A结束后的下一条记录属于任务B，不能继续作为A的未来奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-218946eb5ef436a0">GAE 计算为什么要保留 trajectory 边界，而不能把多个 episode 直接串接？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asapo">SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>优势沿后续TD残差累积，跨episode串接会把另一个任务的回报传进当前任务。需按终止边界处理bootstrap与累积；当前确定性mini-suite不等于真实浏览器或完整RL训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>任务A结束后的下一条记录属于任务B，不能继续作为A的未来奖励。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19842">原论文</a> · <a href="../../../../agent-research/2608.19842-sapo/">实现解读</a> · <a href="#qa-218946eb5ef436a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rtpo" data-paper-title="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training Agent Adelaide University 2026-08-19 把多轮 rollout 组织成稀疏反向树，按时间逆序更新 turn，令决策与下游 continuation 保持 on-policy。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 RTPO 为什么把多轮决策组织成反向更新过程？ 一个早期动作的价值取决于后续continuation。RTPO把rollout组织成稀疏反向树，按turn逆序更新，让决策与用于评价它的下游策略尽量保持对应。 示意：先处理最后几次动作的后果，再回到更早决策，而非把整条轨迹当无结构文本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-rtpo-1c108353" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-52f37824bda763dd">RTPO 为什么把多轮决策组织成反向更新过程？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Artpo">RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个早期动作的价值取决于后续continuation。RTPO把rollout组织成稀疏反向树，按turn逆序更新，让决策与用于评价它的下游策略尽量保持对应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先处理最后几次动作的后果，再回到更早决策，而非把整条轨迹当无结构文本。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18682">原论文</a> · <a href="../../../../agent-research/2608.18682-rtpo/">实现解读</a> · <a href="#qa-52f37824bda763dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rtpo" data-paper-title="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training Agent Adelaide University 2026-08-19 把多轮 rollout 组织成稀疏反向树，按时间逆序更新 turn，令决策与下游 continuation 保持 on-policy。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 为什么按 turn 逆序更新有助于保持决策与下游 continuation 的 on-policy 对应？ 早期动作价值依赖后续策略，若下游已大幅改变却仍用旧 continuation 信用，会产生不一致。反向树先处理靠近结果的回合，再向前传播相应训练依据，让前段决策面对更新后的续跑关系；顺序稳定训练不等于无需重要性或执行对齐检查。 例如最后两步已学会恢复，开局动作的好坏应按新的恢复能力重新理解，而不持续沿用末段还是旧失败策略时的估值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9c34e4b512e67b3c">为什么按 turn 逆序更新有助于保持决策与下游 continuation 的 on-policy 对应？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Artpo">RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早期动作价值依赖后续策略，若下游已大幅改变却仍用旧 continuation 信用，会产生不一致。反向树先处理靠近结果的回合，再向前传播相应训练依据，让前段决策面对更新后的续跑关系；顺序稳定训练不等于无需重要性或执行对齐检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最后两步已学会恢复，开局动作的好坏应按新的恢复能力重新理解，而不持续沿用末段还是旧失败策略时的估值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18682">原论文</a> · <a href="../../../../agent-research/2608.18682-rtpo/">实现解读</a> · <a href="#qa-9c34e4b512e67b3c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rtpo" data-paper-title="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training Agent Adelaide University 2026-08-19 把多轮 rollout 组织成稀疏反向树，按时间逆序更新 turn，令决策与下游 continuation 保持 on-policy。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 逆 turn 更新与把整段 token 文本倒序训练，是同一操作吗？ 不是。逆序指决策更新顺序及下游continuation关系，语言模型的因果输入仍按合法轨迹构造。倒置文本会改变任务与可见性，不能用它代替反向策略优化。 示意：先更新第3轮再更新第2轮，不代表让模型先读第3轮观测去预测第1轮动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d0b1be0b8eafd96b">逆 turn 更新与把整段 token 文本倒序训练，是同一操作吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Artpo">RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。逆序指决策更新顺序及下游continuation关系，语言模型的因果输入仍按合法轨迹构造。倒置文本会改变任务与可见性，不能用它代替反向策略优化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先更新第3轮再更新第2轮，不代表让模型先读第3轮观测去预测第1轮动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18682">原论文</a> · <a href="../../../../agent-research/2608.18682-rtpo/">实现解读</a> · <a href="#qa-d0b1be0b8eafd96b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rtpo" data-paper-title="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training Agent Adelaide University 2026-08-19 把多轮 rollout 组织成稀疏反向树，按时间逆序更新 turn，令决策与下游 continuation 保持 on-policy。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 RTPO 为什么要同时记录每个 turn 的行为策略与下游 continuation 版本？ 早期决策的优势若来自不匹配的后续策略，可能失去on-policy对应。仅把更新索引改成倒序并不足够，还需核对树节点、状态与续写归属；本地控制流不是完整外部环境RL。 示意：某节点已按新版后续策略重评，不能仍把旧续写奖励当成同一状态的当前回报。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dd588ecabba448b1">RTPO 为什么要同时记录每个 turn 的行为策略与下游 continuation 版本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Artpo">RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早期决策的优势若来自不匹配的后续策略，可能失去on-policy对应。仅把更新索引改成倒序并不足够，还需核对树节点、状态与续写归属；本地控制流不是完整外部环境RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某节点已按新版后续策略重评，不能仍把旧续写奖励当成同一状态的当前回报。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18682">原论文</a> · <a href="../../../../agent-research/2608.18682-rtpo/">实现解读</a> · <a href="#qa-dd588ecabba448b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spade" data-paper-title="SPADE: Self-Play in Adaptive Synthetic Executable Environments" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPADE: Self-Play in Adaptive Synthetic Executable Environments Agent University of Washington 2026-08-19 同一 LLM 分饰环境设计者和推理 Agent，以有/无 privileged hint 的 regret 学习能力边界上的可执行环境。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 环境生成 Agent 交互策略学习：把轨迹反馈变成更新 SPADE 为什么让同一 LLM 同时扮演环境设计者与推理 Agent？ 设计者生成可执行的合成环境，Agent尝试解决，再用有无privileged hint的回报差寻找能力边界上的任务。目标是产生有学习价值的挑战，而非堆积任何无法解决的问题。 示意：无hint失败、有hint成功的环境，可能比两者都失败的坏题更有区分价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-spade-5fdace60" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8d3ed730866d322d">SPADE 为什么让同一 LLM 同时扮演环境设计者与推理 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspade">SPADE: Self-Play in Adaptive Synthetic Executable Environments</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>设计者生成可执行的合成环境，Agent尝试解决，再用有无privileged hint的回报差寻找能力边界上的任务。目标是产生有学习价值的挑战，而非堆积任何无法解决的问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>无hint失败、有hint成功的环境，可能比两者都失败的坏题更有区分价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19197">原论文</a> · <a href="../../../../agent-research/2608.19197-spade/">实现解读</a> · <a href="#qa-8d3ed730866d322d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spade" data-paper-title="SPADE: Self-Play in Adaptive Synthetic Executable Environments" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPADE: Self-Play in Adaptive Synthetic Executable Environments Agent University of Washington 2026-08-19 同一 LLM 分饰环境设计者和推理 Agent，以有/无 privileged hint 的 regret 学习能力边界上的可执行环境。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 环境生成 Agent 交互策略学习：把轨迹反馈变成更新 环境设计者为什么用有 hint 与无 hint 的 regret，而不是只追求让 Agent 失败？ 纯失败奖励可能生成根本无解或过难的环境，无法提供有效课程。hint 能显著提高表现而无 hint 仍困难的差距，更接近可学习能力边界；环境还必须可执行，特权信息只属于训练比较，不能在无提示评测时暗中交给推理 Agent。 例如迷宫无提示难走、给方向后可完成，适合作为训练挑战；完全封死出口让双方都失败，不应只因困难就获高设计分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c7c3a5bda0319f3a">环境设计者为什么用有 hint 与无 hint 的 regret，而不是只追求让 Agent 失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspade">SPADE: Self-Play in Adaptive Synthetic Executable Environments</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>纯失败奖励可能生成根本无解或过难的环境，无法提供有效课程。hint 能显著提高表现而无 hint 仍困难的差距，更接近可学习能力边界；环境还必须可执行，特权信息只属于训练比较，不能在无提示评测时暗中交给推理 Agent。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如迷宫无提示难走、给方向后可完成，适合作为训练挑战；完全封死出口让双方都失败，不应只因困难就获高设计分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19197">原论文</a> · <a href="../../../../agent-research/2608.19197-spade/">实现解读</a> · <a href="#qa-c7c3a5bda0319f3a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spade" data-paper-title="SPADE: Self-Play in Adaptive Synthetic Executable Environments" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPADE: Self-Play in Adaptive Synthetic Executable Environments Agent University of Washington 2026-08-19 同一 LLM 分饰环境设计者和推理 Agent，以有/无 privileged hint 的 regret 学习能力边界上的可执行环境。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 环境生成 Agent 交互策略学习：把轨迹反馈变成更新 最大化失败率，与最大化 hint/no-hint regret，会偏好相同环境吗？ 不会。只追失败可鼓励无解或无意义环境；regret还要求特权帮助能提高回报，从而区分可解但当前困难的任务。它仍需真正的可执行环境与反馈，不是固定难度标签。 示意：两种Agent都得0分的环境，失败率高但regret为0。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a01da2b026001f3b">最大化失败率，与最大化 hint/no-hint regret，会偏好相同环境吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspade">SPADE: Self-Play in Adaptive Synthetic Executable Environments</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不会。只追失败可鼓励无解或无意义环境；regret还要求特权帮助能提高回报，从而区分可解但当前困难的任务。它仍需真正的可执行环境与反馈，不是固定难度标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两种Agent都得0分的环境，失败率高但regret为0。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19197">原论文</a> · <a href="../../../../agent-research/2608.19197-spade/">实现解读</a> · <a href="#qa-a01da2b026001f3b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spade" data-paper-title="SPADE: Self-Play in Adaptive Synthetic Executable Environments" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPADE: Self-Play in Adaptive Synthetic Executable Environments Agent University of Washington 2026-08-19 同一 LLM 分饰环境设计者和推理 Agent，以有/无 privileged hint 的 regret 学习能力边界上的可执行环境。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 环境生成 Agent 交互策略学习：把轨迹反馈变成更新 SPADE 的 hint 条件能在无 hint 评测中保留给被评估 Agent 吗？ 不能。两种条件的输入必须分开，privileged hint只用于对应训练/对照路径，不能偷偷流入无hint策略。还需实际执行环境验证；本地mini-suite没有运行原文外部环境和大模型训练。 示意：无hint回调若仍拿到设计者保存的解题计划，就无法解释两条件回报差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fe52868b4be336c7">SPADE 的 hint 条件能在无 hint 评测中保留给被评估 Agent 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspade">SPADE: Self-Play in Adaptive Synthetic Executable Environments</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。两种条件的输入必须分开，privileged hint只用于对应训练/对照路径，不能偷偷流入无hint策略。还需实际执行环境验证；本地mini-suite没有运行原文外部环境和大模型训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>无hint回调若仍拿到设计者保存的解题计划，就无法解释两条件回报差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19197">原论文</a> · <a href="../../../../agent-research/2608.19197-spade/">实现解读</a> · <a href="#qa-fe52868b4be336c7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:planpo" data-paper-title="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs Agent Xiamen University 2026-08-18 在成功轨迹内同时比较 trajectory turn 数和单 turn response 长度，形成 coarse-to-fine planning advantages。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 规划 Agent 交互策略学习：把轨迹反馈变成更新 PlanPO 为什么把规划效率分成回合数与单回合响应长度？ 少走环境turn与少写内部响应是两种成本。方法在成功轨迹内做coarse-to-fine比较，再与outcome优势结合，既保留任务完成目标，又鼓励更有效的过程。 示意：两条都成功的轨迹，一条工具调用少，另一条每次解释短，可分开评价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-planpo-5fac2579" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-224fcadb29af723f">PlanPO 为什么把规划效率分成回合数与单回合响应长度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aplanpo">PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>少走环境turn与少写内部响应是两种成本。方法在成功轨迹内做coarse-to-fine比较，再与outcome优势结合，既保留任务完成目标，又鼓励更有效的过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条都成功的轨迹，一条工具调用少，另一条每次解释短，可分开评价。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17289">原论文</a> · <a href="../../../../agent-research/2608.17289-planpo/">实现解读</a> · <a href="#qa-224fcadb29af723f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:planpo" data-paper-title="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs Agent Xiamen University 2026-08-18 在成功轨迹内同时比较 trajectory turn 数和单 turn response 长度，形成 coarse-to-fine planning advantages。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 规划 Agent 交互策略学习：把轨迹反馈变成更新 为什么只在成功轨迹中比较回合数和响应长度，而不能直接奖励所有短轨迹？ 短可能来自高效规划，也可能只是提前放弃。先以结果区分成功，再在可比成功路径内看少回合和短响应，才更接近规划效率。粗到细优势补充 outcome，不能压倒正确性，也不能用少 token 掩盖必要工具取证被跳过。 例如两条都修好同一 bug，一条少三次无效搜索可获效率优势；另一条直接说完成却没改文件，不能因更短而受奖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2c01413b29f93499">为什么只在成功轨迹中比较回合数和响应长度，而不能直接奖励所有短轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aplanpo">PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>短可能来自高效规划，也可能只是提前放弃。先以结果区分成功，再在可比成功路径内看少回合和短响应，才更接近规划效率。粗到细优势补充 outcome，不能压倒正确性，也不能用少 token 掩盖必要工具取证被跳过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条都修好同一 bug，一条少三次无效搜索可获效率优势；另一条直接说完成却没改文件，不能因更短而受奖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17289">原论文</a> · <a href="../../../../agent-research/2608.17289-planpo/">实现解读</a> · <a href="#qa-2c01413b29f93499">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:planpo" data-paper-title="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs Agent Xiamen University 2026-08-18 在成功轨迹内同时比较 trajectory turn 数和单 turn response 长度，形成 coarse-to-fine planning advantages。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 规划 Agent 交互策略学习：把轨迹反馈变成更新 PlanPO 的成功条件内效率比较，与直接奖励最短答案有什么差别？ 直接短奖励可能偏好失败或过早停止；成功轨迹内部比较先保证完成任务，再优化turn与长度。长度优势也不等于全局outcome优势，二者不能混成同一个奖励。 示意：一句“完成了”但没做任务，不应因最短而胜过真正成功的多轮过程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-724afe0ef4b5ce66">PlanPO 的成功条件内效率比较，与直接奖励最短答案有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aplanpo">PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接短奖励可能偏好失败或过早停止；成功轨迹内部比较先保证完成任务，再优化turn与长度。长度优势也不等于全局outcome优势，二者不能混成同一个奖励。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一句“完成了”但没做任务，不应因最短而胜过真正成功的多轮过程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17289">原论文</a> · <a href="../../../../agent-research/2608.17289-planpo/">实现解读</a> · <a href="#qa-724afe0ef4b5ce66">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:planpo" data-paper-title="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs Agent Xiamen University 2026-08-18 在成功轨迹内同时比较 trajectory turn 数和单 turn response 长度，形成 coarse-to-fine planning advantages。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 规划 Agent 交互策略学习：把轨迹反馈变成更新 统计 turn-count 与 response-length 时，为什么要区分 Agent 响应和环境 observation？ 两种效率轴分别描述交互轮次与单turn响应，若把工具返回的大段文本也当Agent写作长度，会改变信用口径。应记录成功筛选、计数边界和各优势系数，而非只报平均总token。 示意：一个工具返回长网页，不一定表示该轮Agent自己生成了同样多的响应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ce24322d0dd67bb6">统计 turn-count 与 response-length 时，为什么要区分 Agent 响应和环境 observation？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aplanpo">PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两种效率轴分别描述交互轮次与单turn响应，若把工具返回的大段文本也当Agent写作长度，会改变信用口径。应记录成功筛选、计数边界和各优势系数，而非只报平均总token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个工具返回长网页，不一定表示该轮Agent自己生成了同样多的响应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17289">原论文</a> · <a href="../../../../agent-research/2608.17289-planpo/">实现解读</a> · <a href="#qa-ce24322d0dd67bb6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:trca" data-paper-title="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents Agent Authors did not disclose affiliation 2026-08-17 无需成功 anchor，从每个状态转移的 Evidence、Execution、Invalidity rubric 构造基础和 breakthrough reward。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 过程奖励 Agent 交互策略学习：把轨迹反馈变成更新 TRCA 为什么为每次状态转移定义 rubric，而不只给最后一次总分？ 长程结果难定位关键动作，逐转移rubric可分开检查证据、执行和无效行为，并加入突破奖励。它不依赖先找一条成功anchor，提供更细的信用来源。 示意：某一步获取了关键证据但执行失败，可在两个维度上分别记录，而非全归零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-trca-ae92667a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-873192fd9718233f">TRCA 为什么为每次状态转移定义 rubric，而不只给最后一次总分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atrca">TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长程结果难定位关键动作，逐转移rubric可分开检查证据、执行和无效行为，并加入突破奖励。它不依赖先找一条成功anchor，提供更细的信用来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某一步获取了关键证据但执行失败，可在两个维度上分别记录，而非全归零。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16156">原论文</a> · <a href="../../../../agent-research/2608.16156-trca/">实现解读</a> · <a href="#qa-873192fd9718233f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:trca" data-paper-title="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents Agent Authors did not disclose affiliation 2026-08-17 无需成功 anchor，从每个状态转移的 Evidence、Execution、Invalidity rubric 构造基础和 breakthrough reward。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 过程奖励 Agent 交互策略学习：把轨迹反馈变成更新 把 Evidence、Execution、Invalidity 分开评估，为什么比单一过程分数更可定位？ 转移可能增加证据却执行失败，或动作格式合法但没有任务价值，分项 rubric 能区分这些情况并限制无效行为。breakthrough 信号强调关键推进，不必等待成功锚轨迹；但 rubric 仍需基于真实状态转移，不能由固定模板分数代替环境过程。 例如搜索返回新错误原因属于证据进展，随后命令语法错属于执行问题；合成一个总分会模糊究竟应该修检索还是修调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-92f4d424dd06d08a">把 Evidence、Execution、Invalidity 分开评估，为什么比单一过程分数更可定位？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atrca">TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>转移可能增加证据却执行失败，或动作格式合法但没有任务价值，分项 rubric 能区分这些情况并限制无效行为。breakthrough 信号强调关键推进，不必等待成功锚轨迹；但 rubric 仍需基于真实状态转移，不能由固定模板分数代替环境过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索返回新错误原因属于证据进展，随后命令语法错属于执行问题；合成一个总分会模糊究竟应该修检索还是修调用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16156">原论文</a> · <a href="../../../../agent-research/2608.16156-trca/">实现解读</a> · <a href="#qa-92f4d424dd06d08a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:trca" data-paper-title="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents Agent Authors did not disclose affiliation 2026-08-17 无需成功 anchor，从每个状态转移的 Evidence、Execution、Invalidity rubric 构造基础和 breakthrough reward。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 过程奖励 Agent 交互策略学习：把轨迹反馈变成更新 TRCA 无需成功 anchor，与依赖成功参照轨迹的反馈相比，前提有何不同？ 依赖成功参照的方案首先需要取得可比较的成功执行，TRCA则从实际状态转移的rubric构造基础和突破奖励，不要求先有成功anchor。这是反馈来源的前提差异，不能仅凭它宣称实际任务成功率更高。 示意：两条完整轨迹都失败时，其中一次转移仍可能收集有效证据，逐转移rubric仍可提供反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0b6075a31659322e">TRCA 无需成功 anchor，与依赖成功参照轨迹的反馈相比，前提有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atrca">TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>依赖成功参照的方案首先需要取得可比较的成功执行，TRCA则从实际状态转移的rubric构造基础和突破奖励，不要求先有成功anchor。这是反馈来源的前提差异，不能仅凭它宣称实际任务成功率更高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条完整轨迹都失败时，其中一次转移仍可能收集有效证据，逐转移rubric仍可提供反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16156">原论文</a> · <a href="../../../../agent-research/2608.16156-trca/">实现解读</a> · <a href="#qa-0b6075a31659322e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:trca" data-paper-title="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents Agent Authors did not disclose affiliation 2026-08-17 无需成功 anchor，从每个状态转移的 Evidence、Execution、Invalidity rubric 构造基础和 breakthrough reward。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 过程奖励 Agent 交互策略学习：把轨迹反馈变成更新 TRCA 聚合 invalidity 时，为什么要核对符号与分项日志？ 公式减去r_invalid，其余基础与breakthrough按定义相加。漏负号会奖励无效行为；只记录总和又会掩盖错误，应保留逐分项及对应转移，不能以固定分数替代实际评估。 示意：保持其它分项不变、增加invalidity时，总奖励应下降。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f234aa5e56240844">TRCA 聚合 invalidity 时，为什么要核对符号与分项日志？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atrca">TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式减去r_invalid，其余基础与breakthrough按定义相加。漏负号会奖励无效行为；只记录总和又会掩盖错误，应保留逐分项及对应转移，不能以固定分数替代实际评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>保持其它分项不变、增加invalidity时，总奖励应下降。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16156">原论文</a> · <a href="../../../../agent-research/2608.16156-trca/">实现解读</a> · <a href="#qa-f234aa5e56240844">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sinkflex-rl" data-paper-title="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks Agent Capital One AI Foundations 2026-08-11 长程工具 Agent 的 on-policy rollout 同时受环境状态、长上下文和训练显存限制。SinkFlex-RL 把 Gymnasium 双控制环境、VERL 风格数据流、无 value model 的 GRPO 与 sink-aware FlexAttention 组合，causal / sliding-window mask 下仍保留模型特有 sink scaling。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行 sink 保留、causal sliding window 和无 critic 的 group-relative 更新路径；未声称复刻 CUDA FlexAttention kernel。未复刻论文的 MoE checkpoint、VERL 集群、τ²-Bench 全环境或 GPU kernel 显存曲线；mini-suite 验证状态保留规则与 RL 控制流，GPU 性能数字仅引用原文。ScaleMCP mini-suite 120 episodes：joint success 1.0、average cost 0.67；  Agentic RL / efficient long context Agent 交互策略学习：把轨迹反馈变成更新 SinkFlex-RL 为什么同时关注 rollout 环境与 attention 显存？ 长工具轨迹既有多轮状态管理，也有上下文与训练显存瓶颈。方法把环境、fresh轨迹组、无value-model GRPO与sink-aware FlexAttention结合，不能只把它理解成一个压缩mask。 示意：省下attention显存仍需正确保留环境状态，才能进行真正多轮策略更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-sinkflex-rl-6bf5fe2a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1aa103458d0f49d2">SinkFlex-RL 为什么同时关注 rollout 环境与 attention 显存？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asinkflex-rl">Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Capital One AI Foundations</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长工具轨迹既有多轮状态管理，也有上下文与训练显存瓶颈。方法把环境、fresh轨迹组、无value-model GRPO与sink-aware FlexAttention结合，不能只把它理解成一个压缩mask。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>省下attention显存仍需正确保留环境状态，才能进行真正多轮策略更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10357">原论文</a> · <a href="../../../../agent-research/2608.10357-sinkflex-rl/">实现解读</a> · <a href="#qa-1aa103458d0f49d2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sinkflex-rl" data-paper-title="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks Agent Capital One AI Foundations 2026-08-11 长程工具 Agent 的 on-policy rollout 同时受环境状态、长上下文和训练显存限制。SinkFlex-RL 把 Gymnasium 双控制环境、VERL 风格数据流、无 value model 的 GRPO 与 sink-aware FlexAttention 组合，causal / sliding-window mask 下仍保留模型特有 sink scaling。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行 sink 保留、causal sliding window 和无 critic 的 group-relative 更新路径；未声称复刻 CUDA FlexAttention kernel。未复刻论文的 MoE checkpoint、VERL 集群、τ²-Bench 全环境或 GPU kernel 显存曲线；mini-suite 验证状态保留规则与 RL 控制流，GPU 性能数字仅引用原文。ScaleMCP mini-suite 120 episodes：joint success 1.0、average cost 0.67；  Agentic RL / efficient long context Agent 交互策略学习：把轨迹反馈变成更新 滑窗或 causal mask 为什么仍要保留模型特有的 sink scaling？ 稀疏可见性与 sink 数值机制影响注意力的不同部分，改 mask 并不授权删除模型原有缩放。训练系统还需连接真实环境状态、长上下文与 GRPO 数据流；公式 kernel 通过只能说明局部算子，不能替代完整 on-policy rollout 和工具任务验证。 例如窗口只保留最近文本和 sink，若同时把 sink 的特殊缩放去掉，输出变化就混入两项改动，无法归因于滑窗本身。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-10d9b7593d872e71">滑窗或 causal mask 为什么仍要保留模型特有的 sink scaling？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asinkflex-rl">Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Capital One AI Foundations</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>稀疏可见性与 sink 数值机制影响注意力的不同部分，改 mask 并不授权删除模型原有缩放。训练系统还需连接真实环境状态、长上下文与 GRPO 数据流；公式 kernel 通过只能说明局部算子，不能替代完整 on-policy rollout 和工具任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如窗口只保留最近文本和 sink，若同时把 sink 的特殊缩放去掉，输出变化就混入两项改动，无法归因于滑窗本身。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10357">原论文</a> · <a href="../../../../agent-research/2608.10357-sinkflex-rl/">实现解读</a> · <a href="#qa-10d9b7593d872e71">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sinkflex-rl" data-paper-title="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks Agent Capital One AI Foundations 2026-08-11 长程工具 Agent 的 on-policy rollout 同时受环境状态、长上下文和训练显存限制。SinkFlex-RL 把 Gymnasium 双控制环境、VERL 风格数据流、无 value model 的 GRPO 与 sink-aware FlexAttention 组合，causal / sliding-window mask 下仍保留模型特有 sink scaling。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行 sink 保留、causal sliding window 和无 critic 的 group-relative 更新路径；未声称复刻 CUDA FlexAttention kernel。未复刻论文的 MoE checkpoint、VERL 集群、τ²-Bench 全环境或 GPU kernel 显存曲线；mini-suite 验证状态保留规则与 RL 控制流，GPU 性能数字仅引用原文。ScaleMCP mini-suite 120 episodes：joint success 1.0、average cost 0.67；  Agentic RL / efficient long context Agent 交互策略学习：把轨迹反馈变成更新 GRPO 的组相对优势与 PPO 的独立 value model 路径，训练依赖有什么不同？ 文档方案不使用独立value model，而从轨迹组构造相对优势，再做裁剪策略目标及KL正则。替换估计路径影响rollout需求和显存，不能只把优化器名字换成GRPO。 示意：一组轨迹回报提供相对基线，不代表已训练了一个逐状态critic。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-eb11358bd9590099">GRPO 的组相对优势与 PPO 的独立 value model 路径，训练依赖有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asinkflex-rl">Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Capital One AI Foundations</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档方案不使用独立value model，而从轨迹组构造相对优势，再做裁剪策略目标及KL正则。替换估计路径影响rollout需求和显存，不能只把优化器名字换成GRPO。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组轨迹回报提供相对基线，不代表已训练了一个逐状态critic。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10357">原论文</a> · <a href="../../../../agent-research/2608.10357-sinkflex-rl/">实现解读</a> · <a href="#qa-eb11358bd9590099">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sinkflex-rl" data-paper-title="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks Agent Capital One AI Foundations 2026-08-11 长程工具 Agent 的 on-policy rollout 同时受环境状态、长上下文和训练显存限制。SinkFlex-RL 把 Gymnasium 双控制环境、VERL 风格数据流、无 value model 的 GRPO 与 sink-aware FlexAttention 组合，causal / sliding-window mask 下仍保留模型特有 sink scaling。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行 sink 保留、causal sliding window 和无 critic 的 group-relative 更新路径；未声称复刻 CUDA FlexAttention kernel。未复刻论文的 MoE checkpoint、VERL 集群、τ²-Bench 全环境或 GPU kernel 显存曲线；mini-suite 验证状态保留规则与 RL 控制流，GPU 性能数字仅引用原文。ScaleMCP mini-suite 120 episodes：joint success 1.0、average cost 0.67；  Agentic RL / efficient long context Agent 交互策略学习：把轨迹反馈变成更新 SinkFlex-RL 公式里的 token 平均，为什么不能擅自改成每轨迹先平均再等权？ 文档分母为总有效长度ΣT_i，长短轨迹的计数口径与先各自平均不同。还需保留模型sink scaling并核对实际mask；本地mini-suite未复刻FlexAttention GPU显存曲线。 示意：长度10与100的两条轨迹，逐token均值与各占一半权重不是同一loss。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-065d32c7060b868a">SinkFlex-RL 公式里的 token 平均，为什么不能擅自改成每轨迹先平均再等权？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asinkflex-rl">Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Capital One AI Foundations</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档分母为总有效长度ΣT_i，长短轨迹的计数口径与先各自平均不同。还需保留模型sink scaling并核对实际mask；本地mini-suite未复刻FlexAttention GPU显存曲线。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长度10与100的两条轨迹，逐token均值与各占一半权重不是同一loss。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10357">原论文</a> · <a href="../../../../agent-research/2608.10357-sinkflex-rl/">实现解读</a> · <a href="#qa-065d32c7060b868a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:residency-rl" data-paper-title="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments Agent Google DeepMind 2026-08-07 静态知识题不能覆盖主动询问、工具调用及长程决策。论文通过场景生成、带信息不对称的模拟环境、按维度隔离的裁判和GRPO组成完整训练链路；隐藏参考信息只属于环境/裁判，不能直接暴露给被评估策略。原文§3 成本过高，不复现（审查 DONE）。原配置依赖内部Gemini策略训练及独立模拟/裁判调用，使用49,870个常规场景、5,000个历史询问场景和2,583个对抗场景；每条轨迹可达60轮对话及8次工具调用。原文§3.4  多轮 Agent RL 多轮模拟与结构奖励 Agent 交互策略学习：把轨迹反馈变成更新 ResidencyRL 为什么使用多轮模拟，而不只训练静态知识问答？ 主动询问、工具调用和长程决策需要观察交互后果。方法将场景生成、信息不对称环境、隔离多维裁判与GRPO连接起来，训练对象是交互策略而非只背静态答案。 示意：Agent需根据新观察决定下一次询问，不能一开始就拿到场景全部隐藏信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-residency-rl-21b2b4df" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e23450ebdaeb526a">ResidencyRL 为什么使用多轮模拟，而不只训练静态知识问答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aresidency-rl">ResidencyRL: Reinforcement Learning in Simulated Clinical Environments</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主动询问、工具调用和长程决策需要观察交互后果。方法将场景生成、信息不对称环境、隔离多维裁判与GRPO连接起来，训练对象是交互策略而非只背静态答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Agent需根据新观察决定下一次询问，不能一开始就拿到场景全部隐藏信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07418v1">原论文</a> · <a href="../../../../agent-research/2608.07418-residency-rl/">实现解读</a> · <a href="#qa-e23450ebdaeb526a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:residency-rl" data-paper-title="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments Agent Google DeepMind 2026-08-07 静态知识题不能覆盖主动询问、工具调用及长程决策。论文通过场景生成、带信息不对称的模拟环境、按维度隔离的裁判和GRPO组成完整训练链路；隐藏参考信息只属于环境/裁判，不能直接暴露给被评估策略。原文§3 成本过高，不复现（审查 DONE）。原配置依赖内部Gemini策略训练及独立模拟/裁判调用，使用49,870个常规场景、5,000个历史询问场景和2,583个对抗场景；每条轨迹可达60轮对话及8次工具调用。原文§3.4  多轮 Agent RL 多轮模拟与结构奖励 Agent 交互策略学习：把轨迹反馈变成更新 带信息不对称的模拟训练，为什么必须把隐藏参考留在环境和裁判侧？ 策略需要通过询问、工具和观察逐步取证，若直接看到参考信息就绕过了长程决策难点。各维裁判隔离再聚合奖励，减少互相污染，但奖励公式本身不是完整环境或专业能力；本地诊断也不能当真实临床效果或决策可靠性的证据。 例如模拟任务中某项状态应通过查询后才出现，不能把完整参考摘要先放进策略提示，再把最终判断记成自主取证成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2ea7561e68c91b4a">带信息不对称的模拟训练，为什么必须把隐藏参考留在环境和裁判侧？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aresidency-rl">ResidencyRL: Reinforcement Learning in Simulated Clinical Environments</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略需要通过询问、工具和观察逐步取证，若直接看到参考信息就绕过了长程决策难点。各维裁判隔离再聚合奖励，减少互相污染，但奖励公式本身不是完整环境或专业能力；本地诊断也不能当真实临床效果或决策可靠性的证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模拟任务中某项状态应通过查询后才出现，不能把完整参考摘要先放进策略提示，再把最终判断记成自主取证成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07418v1">原论文</a> · <a href="../../../../agent-research/2608.07418-residency-rl/">实现解读</a> · <a href="#qa-2ea7561e68c91b4a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:residency-rl" data-paper-title="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments Agent Google DeepMind 2026-08-07 静态知识题不能覆盖主动询问、工具调用及长程决策。论文通过场景生成、带信息不对称的模拟环境、按维度隔离的裁判和GRPO组成完整训练链路；隐藏参考信息只属于环境/裁判，不能直接暴露给被评估策略。原文§3 成本过高，不复现（审查 DONE）。原配置依赖内部Gemini策略训练及独立模拟/裁判调用，使用49,870个常规场景、5,000个历史询问场景和2,583个对抗场景；每条轨迹可达60轮对话及8次工具调用。原文§3.4  多轮 Agent RL 多轮模拟与结构奖励 Agent 交互策略学习：把轨迹反馈变成更新 六个维度的奖励聚合，与完整模拟训练算法，有什么层级差别？ 聚合公式只把已获得的归一化评分与惩罚汇总；完整方法还需要场景、真实交互、各维裁判和策略更新。固定分数或一个loss包装不能替代这一链路。 示意：能把六个数字加权成R，不代表已经让模型在模拟环境里完成并学习了一次交互。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e206b051f6ef2513">六个维度的奖励聚合，与完整模拟训练算法，有什么层级差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aresidency-rl">ResidencyRL: Reinforcement Learning in Simulated Clinical Environments</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>聚合公式只把已获得的归一化评分与惩罚汇总；完整方法还需要场景、真实交互、各维裁判和策略更新。固定分数或一个loss包装不能替代这一链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>能把六个数字加权成R，不代表已经让模型在模拟环境里完成并学习了一次交互。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07418v1">原论文</a> · <a href="../../../../agent-research/2608.07418-residency-rl/">实现解读</a> · <a href="#qa-e206b051f6ef2513">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:residency-rl" data-paper-title="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments Agent Google DeepMind 2026-08-07 静态知识题不能覆盖主动询问、工具调用及长程决策。论文通过场景生成、带信息不对称的模拟环境、按维度隔离的裁判和GRPO组成完整训练链路；隐藏参考信息只属于环境/裁判，不能直接暴露给被评估策略。原文§3 成本过高，不复现（审查 DONE）。原配置依赖内部Gemini策略训练及独立模拟/裁判调用，使用49,870个常规场景、5,000个历史询问场景和2,583个对抗场景；每条轨迹可达60轮对话及8次工具调用。原文§3.4  多轮 Agent RL 多轮模拟与结构奖励 Agent 交互策略学习：把轨迹反馈变成更新 ResidencyRL 的惩罚为何先 min(3,P)，而不是在总奖励上任意截断？ 文档先算3倍加权归一化维度分，再减最多3的惩罚，顺序与分别作用对象要保留。隐藏场景仅给环境/裁判，各维隔离调用不能把参考直接传给策略。 示意：P从4增到10时，该项扣分仍为3，但不能顺带改写其它维度的分值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d22abfba171c8915">ResidencyRL 的惩罚为何先 min(3,P)，而不是在总奖励上任意截断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aresidency-rl">ResidencyRL: Reinforcement Learning in Simulated Clinical Environments</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档先算3倍加权归一化维度分，再减最多3的惩罚，顺序与分别作用对象要保留。隐藏场景仅给环境/裁判，各维隔离调用不能把参考直接传给策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>P从4增到10时，该项扣分仍为3，但不能顺带改写其它维度的分值。</p>
<p class="ar-learning-sources">依据：核心公式、背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07418v1">原论文</a> · <a href="../../../../agent-research/2608.07418-residency-rl/">实现解读</a> · <a href="#qa-d22abfba171c8915">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-opsd" data-paper-title="AgentOPSD" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AgentOPSD Agent Tsinghua University 2026-08-06 轨迹奖励难定位少数关键决策。AgentOPSD 把 privileged replay 的 token teacher/student log-prob gap 聚合成 turn evidence，再在 log-odds 空间递归更新成功信念，以相邻信念修订量识别 pivotal turn。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现逐 turn evidence、递归 log-odds belief、pivotal revision 和 critic-free policy update。  递归 turn 信用 Agent 交互策略学习：把轨迹反馈变成更新 AgentOPSD 为什么用 turn evidence 来递归更新成功信念？ 整条轨迹奖励难指出关键决策。方法将privileged replay中teacher/student的token log-prob gap聚合到turn，再累积到log-odds，用相邻信念变化分配更局部的信用。 示意：一个关键工具选择使成功信念明显上升，可比此前已经很高的信念值更能定位贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent-opsd-6c6325b8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-edd89b34aa8c5592">AgentOPSD 为什么用 turn evidence 来递归更新成功信念？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-opsd">AgentOPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整条轨迹奖励难指出关键决策。方法将privileged replay中teacher/student的token log-prob gap聚合到turn，再累积到log-odds，用相邻信念变化分配更局部的信用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个关键工具选择使成功信念明显上升，可比此前已经很高的信念值更能定位贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05987">原论文</a> · <a href="../../../../agent-research/2608.05987-agent-opsd/">实现解读</a> · <a href="#qa-edd89b34aa8c5592">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-opsd" data-paper-title="AgentOPSD" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AgentOPSD Agent Tsinghua University 2026-08-06 轨迹奖励难定位少数关键决策。AgentOPSD 把 privileged replay 的 token teacher/student log-prob gap 聚合成 turn evidence，再在 log-odds 空间递归更新成功信念，以相邻信念修订量识别 pivotal turn。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现逐 turn evidence、递归 log-odds belief、pivotal revision 和 critic-free policy update。  递归 turn 信用 Agent 交互策略学习：把轨迹反馈变成更新 为什么用相邻成功信念的修订量，而非最终信念值识别 pivotal turn？ 最终值混合了此前全部证据，不能定位哪一步导致关键改变。把 token 师生概率差累积到 log-odds，再观察每回合 sigmoid 信念的增量，能提取局部转折；这是训练侧事后归因，特权 replay 和参考信息不能交给独立评测策略。 例如前几步信息平淡，某次工具返回让成功信念陡升，该回合增量更能提示关键作用，而非把高终值平均分给所有动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-79e8ecd371a73695">为什么用相邻成功信念的修订量，而非最终信念值识别 pivotal turn？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-opsd">AgentOPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终值混合了此前全部证据，不能定位哪一步导致关键改变。把 token 师生概率差累积到 log-odds，再观察每回合 sigmoid 信念的增量，能提取局部转折；这是训练侧事后归因，特权 replay 和参考信息不能交给独立评测策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前几步信息平淡，某次工具返回让成功信念陡升，该回合增量更能提示关键作用，而非把高终值平均分给所有动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05987">原论文</a> · <a href="../../../../agent-research/2608.05987-agent-opsd/">实现解读</a> · <a href="#qa-79e8ecd371a73695">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-opsd" data-paper-title="AgentOPSD" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AgentOPSD Agent Tsinghua University 2026-08-06 轨迹奖励难定位少数关键决策。AgentOPSD 把 privileged replay 的 token teacher/student log-prob gap 聚合成 turn evidence，再在 log-odds 空间递归更新成功信念，以相邻信念修订量识别 pivotal turn。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现逐 turn evidence、递归 log-odds belief、pivotal revision 和 critic-free policy update。  递归 turn 信用 Agent 交互策略学习：把轨迹反馈变成更新 AgentOPSD 的 critic-free，是否表示不再需要任何教师信息？ 不是。它不依赖独立value critic，但turn evidence仍来自privileged replay的teacher/student差异。mini-suite的状态更新也不能自动证明真实大模型teacher rollout与策略训练已经执行。 示意：没有critic网络，不等于训练时可以省掉定义e_t所需的教师分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ae5b7f23496958c6">AgentOPSD 的 critic-free，是否表示不再需要任何教师信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-opsd">AgentOPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它不依赖独立value critic，但turn evidence仍来自privileged replay的teacher/student差异。mini-suite的状态更新也不能自动证明真实大模型teacher rollout与策略训练已经执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>没有critic网络，不等于训练时可以省掉定义e_t所需的教师分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05987">原论文</a> · <a href="../../../../agent-research/2608.05987-agent-opsd/">实现解读</a> · <a href="#qa-ae5b7f23496958c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-opsd" data-paper-title="AgentOPSD" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AgentOPSD Agent Tsinghua University 2026-08-06 轨迹奖励难定位少数关键决策。AgentOPSD 把 privileged replay 的 token teacher/student log-prob gap 聚合成 turn evidence，再在 log-odds 空间递归更新成功信念，以相邻信念修订量识别 pivotal turn。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现逐 turn evidence、递归 log-odds belief、pivotal revision 和 critic-free policy update。  递归 turn 信用 Agent 交互策略学习：把轨迹反馈变成更新 AgentOPSD 的 evidence 为什么在 log-odds 上累加，再取 sigmoid 差？ log-odds状态ℓ_t=ℓ_{t-1}+e_t，信用是两个相邻sigmoid信念之差；直接把e_t加到概率会越界，也会改写累积方式。较大log-odds还需稳定数值计算，privileged replay不能进入评测策略输入。 示意：同样e_t在不同既有信念下产生不同概率修订，不应一律当成同样大小的概率加法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3a8ec969cbfd98ea">AgentOPSD 的 evidence 为什么在 log-odds 上累加，再取 sigmoid 差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-opsd">AgentOPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>log-odds状态ℓ_t=ℓ_{t-1}+e_t，信用是两个相邻sigmoid信念之差；直接把e_t加到概率会越界，也会改写累积方式。较大log-odds还需稳定数值计算，privileged replay不能进入评测策略输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样e_t在不同既有信念下产生不同概率修订，不应一律当成同样大小的概率加法。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05987">原论文</a> · <a href="../../../../agent-research/2608.05987-agent-opsd/">实现解读</a> · <a href="#qa-3a8ec969cbfd98ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cipo" data-paper-title="Contextual Information Policy Optimization for Search Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Contextual Information Policy Optimization for Search Agents Agent Beihang University 2026-08-06 主题：搜索 Agent RL。只奖励最终答案会让检索退化成确认偏见。CIPO 识别受外部证据影响的后续动作，给予 dense turn credit，并与全局 outcome reward 联合优化。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索 Agent RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 CIPO 为什么给搜索中间步骤增加 evidence credit？ 最终答案奖励难说明检索是否真正影响决策，容易鼓励确认已有结论。CIPO关注外部证据带来的后续动作变化，把dense证据信用与全局结果结合，鼓励实质使用新信息。 示意：搜到反证后修改计划，比只在答案里附上一个无关引用更有信息价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-cipo-5f899139" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0323829fb5f31cf8">CIPO 为什么给搜索中间步骤增加 evidence credit？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acipo">Contextual Information Policy Optimization for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终答案奖励难说明检索是否真正影响决策，容易鼓励确认已有结论。CIPO关注外部证据带来的后续动作变化，把dense证据信用与全局结果结合，鼓励实质使用新信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>搜到反证后修改计划，比只在答案里附上一个无关引用更有信息价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06128">原论文</a> · <a href="../../../../agent-research/2608.06128-cipo/">实现解读</a> · <a href="#qa-0323829fb5f31cf8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cipo" data-paper-title="Contextual Information Policy Optimization for Search Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Contextual Information Policy Optimization for Search Agents Agent Beihang University 2026-08-06 主题：搜索 Agent RL。只奖励最终答案会让检索退化成确认偏见。CIPO 识别受外部证据影响的后续动作，给予 dense turn credit，并与全局 outcome reward 联合优化。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索 Agent RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么只奖最终答案可能让搜索变成确认偏见，而 dense evidence credit 有帮助？ 模型可能先猜答案再只找支持它的内容，终局碰巧正确掩盖了无效搜索。识别外部证据真正改变后续动作的回合并给局部信用，鼓励信息被实际使用，而非机械调用次数；仍需结合全局 outcome，避免只追新证据却偏离问题。 例如搜索发现原猜测日期错误，Agent 据此改查另一来源，这种证据驱动转向应区别于反复查询同一句猜测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fca80e0fca779969">为什么只奖最终答案可能让搜索变成确认偏见，而 dense evidence credit 有帮助？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acipo">Contextual Information Policy Optimization for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型可能先猜答案再只找支持它的内容，终局碰巧正确掩盖了无效搜索。识别外部证据真正改变后续动作的回合并给局部信用，鼓励信息被实际使用，而非机械调用次数；仍需结合全局 outcome，避免只追新证据却偏离问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索发现原猜测日期错误，Agent 据此改查另一来源，这种证据驱动转向应区别于反复查询同一句猜测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06128">原论文</a> · <a href="../../../../agent-research/2608.06128-cipo/">实现解读</a> · <a href="#qa-fca80e0fca779969">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cipo" data-paper-title="Contextual Information Policy Optimization for Search Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Contextual Information Policy Optimization for Search Agents Agent Beihang University 2026-08-06 主题：搜索 Agent RL。只奖励最终答案会让检索退化成确认偏见。CIPO 识别受外部证据影响的后续动作，给予 dense turn credit，并与全局 outcome reward 联合优化。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索 Agent RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 CIPO 的证据影响信用，与奖励引用数量有什么不同？ 引用数量只反映表面形式；证据信用关注外部信息是否作用于后续动作。两者不等价，也不能只见一段搜索文本就认定它对决策有因果贡献，需按方法定义验证。 示意：回答贴了十个链接，但动作完全不变，未必比一个真正改变判断的证据更有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bd6a60f81287a8df">CIPO 的证据影响信用，与奖励引用数量有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acipo">Contextual Information Policy Optimization for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>引用数量只反映表面形式；证据信用关注外部信息是否作用于后续动作。两者不等价，也不能只见一段搜索文本就认定它对决策有因果贡献，需按方法定义验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>回答贴了十个链接，但动作完全不变，未必比一个真正改变判断的证据更有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06128">原论文</a> · <a href="../../../../agent-research/2608.06128-cipo/">实现解读</a> · <a href="#qa-bd6a60f81287a8df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cipo" data-paper-title="Contextual Information Policy Optimization for Search Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Contextual Information Policy Optimization for Search Agents Agent Beihang University 2026-08-06 主题：搜索 Agent RL。只奖励最终答案会让检索退化成确认偏见。CIPO 识别受外部证据影响的后续动作，给予 dense turn credit，并与全局 outcome reward 联合优化。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索 Agent RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 CIPO 的 λ=0 与 λ=1 两个边界，应分别保留哪种优势？ 公式λ=0只用outcome，λ=1只用evidence，能帮助检查混合方向；中间值才是两者联合。还应把每turn信用绑定真实轨迹位置，不能以原文大模型成绩替代本地mini-suite。 示意：λ归零后若仍有证据信用影响更新，就需检查系数或残留分支。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ef7fbb791d5bdef3">CIPO 的 λ=0 与 λ=1 两个边界，应分别保留哪种优势？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acipo">Contextual Information Policy Optimization for Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式λ=0只用outcome，λ=1只用evidence，能帮助检查混合方向；中间值才是两者联合。还应把每turn信用绑定真实轨迹位置，不能以原文大模型成绩替代本地mini-suite。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>λ归零后若仍有证据信用影响更新，就需检查系数或残留分支。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06128">原论文</a> · <a href="../../../../agent-research/2608.06128-cipo/">实现解读</a> · <a href="#qa-ef7fbb791d5bdef3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:envace" data-paper-title="EnvACE" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EnvACE Agent Shanghai Jiao Tong 2026-08-06 EnvACE 不另训 world model，而让同一个 agent policy 在真实 act 之间切换到 rehearsal role，自行预测下一 observation；训练时分别为 acting 与 rehearsal 轨迹计算 group-relative advantage，避免两种奖励尺度互相污染，测试时可用少量私有 rehearsal 扩展规划。 Fidelity：核心机制复现。同一策略交替 act/rehearse，rehearsal observation 仅作私有规划状态，并执行 role-wise group advantage。确定性 mini-suite 验证状态路由与计数，不等同于论文浏览器/工具环境和大模型 RL 训练。PlanBench mini-suite 120 episodes：joint success 1.0000，执行 360 次 world rehearsal、720 次 role-wise advantage update；real_tool_responses=0，确保预测 observation 没被伪装成真实环境反馈。  环境 rehearsal / Agent RL Agent 交互策略学习：把轨迹反馈变成更新 EnvACE 为什么让同一策略切换成 rehearsal role？ 它在真实act之间预测下一observation，用自身策略做少量私有前瞻，而不另训独立world model。训练同时约束acting与rehearsal两种角色，规划预测不等于已经执行工具。 示意：Agent先设想某动作可能返回什么，再决定是否真正采取它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-envace-95e34f1b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a38fc9fc88352019">EnvACE 为什么让同一策略切换成 rehearsal role？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aenvace">EnvACE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它在真实act之间预测下一observation，用自身策略做少量私有前瞻，而不另训独立world model。训练同时约束acting与rehearsal两种角色，规划预测不等于已经执行工具。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Agent先设想某动作可能返回什么，再决定是否真正采取它。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06197">原论文</a> · <a href="../../../../agent-research/2608.06197-envace/">实现解读</a> · <a href="#qa-a38fc9fc88352019">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:envace" data-paper-title="EnvACE" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EnvACE Agent Shanghai Jiao Tong 2026-08-06 EnvACE 不另训 world model，而让同一个 agent policy 在真实 act 之间切换到 rehearsal role，自行预测下一 observation；训练时分别为 acting 与 rehearsal 轨迹计算 group-relative advantage，避免两种奖励尺度互相污染，测试时可用少量私有 rehearsal 扩展规划。 Fidelity：核心机制复现。同一策略交替 act/rehearse，rehearsal observation 仅作私有规划状态，并执行 role-wise group advantage。确定性 mini-suite 验证状态路由与计数，不等同于论文浏览器/工具环境和大模型 RL 训练。PlanBench mini-suite 120 episodes：joint success 1.0000，执行 360 次 world rehearsal、720 次 role-wise advantage update；real_tool_responses=0，确保预测 observation 没被伪装成真实环境反馈。  环境 rehearsal / Agent RL Agent 交互策略学习：把轨迹反馈变成更新 acting 与 rehearsal 为什么要分别计算 group-relative advantage？ 真实行动成败与观察预测的奖励尺度和目标不同，放在同一组中心化会让一种角色的高分压制另一种学习。分组后共享策略仍能练习预测环境，再把私有 rehearsal 用于规划；想象的下一观察不能当作真实工具反馈写入执行证据。 例如演练预测“门打开”得高分，不应让实际行动失败也因同组分布被误奖励；演练结果还须与真实开门返回区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-50472467ca29dd53">acting 与 rehearsal 为什么要分别计算 group-relative advantage？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aenvace">EnvACE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实行动成败与观察预测的奖励尺度和目标不同，放在同一组中心化会让一种角色的高分压制另一种学习。分组后共享策略仍能练习预测环境，再把私有 rehearsal 用于规划；想象的下一观察不能当作真实工具反馈写入执行证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如演练预测“门打开”得高分，不应让实际行动失败也因同组分布被误奖励；演练结果还须与真实开门返回区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06197">原论文</a> · <a href="../../../../agent-research/2608.06197-envace/">实现解读</a> · <a href="#qa-50472467ca29dd53">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:envace" data-paper-title="EnvACE" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EnvACE Agent Shanghai Jiao Tong 2026-08-06 EnvACE 不另训 world model，而让同一个 agent policy 在真实 act 之间切换到 rehearsal role，自行预测下一 observation；训练时分别为 acting 与 rehearsal 轨迹计算 group-relative advantage，避免两种奖励尺度互相污染，测试时可用少量私有 rehearsal 扩展规划。 Fidelity：核心机制复现。同一策略交替 act/rehearse，rehearsal observation 仅作私有规划状态，并执行 role-wise group advantage。确定性 mini-suite 验证状态路由与计数，不等同于论文浏览器/工具环境和大模型 RL 训练。PlanBench mini-suite 120 episodes：joint success 1.0000，执行 360 次 world rehearsal、720 次 role-wise advantage update；real_tool_responses=0，确保预测 observation 没被伪装成真实环境反馈。  环境 rehearsal / Agent RL Agent 交互策略学习：把轨迹反馈变成更新 同策略 rehearsal 与另训练一个 world model，有什么模块差异？ 前者复用agent policy的角色条件，后者有独立环境预测模型及训练维护成本。复用不表示预测一定准确，仍要把预测observation与真实环境反馈分开，并分别计算角色优势。 示意：rehearsal说“工具可能返回成功”，不能把它记成真实工具已经成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2e2c2fb84e75f438">同策略 rehearsal 与另训练一个 world model，有什么模块差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aenvace">EnvACE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者复用agent policy的角色条件，后者有独立环境预测模型及训练维护成本。复用不表示预测一定准确，仍要把预测observation与真实环境反馈分开，并分别计算角色优势。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>rehearsal说“工具可能返回成功”，不能把它记成真实工具已经成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06197">原论文</a> · <a href="../../../../agent-research/2608.06197-envace/">实现解读</a> · <a href="#qa-2e2c2fb84e75f438">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:envace" data-paper-title="EnvACE" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EnvACE Agent Shanghai Jiao Tong 2026-08-06 EnvACE 不另训 world model，而让同一个 agent policy 在真实 act 之间切换到 rehearsal role，自行预测下一 observation；训练时分别为 acting 与 rehearsal 轨迹计算 group-relative advantage，避免两种奖励尺度互相污染，测试时可用少量私有 rehearsal 扩展规划。 Fidelity：核心机制复现。同一策略交替 act/rehearse，rehearsal observation 仅作私有规划状态，并执行 role-wise group advantage。确定性 mini-suite 验证状态路由与计数，不等同于论文浏览器/工具环境和大模型 RL 训练。PlanBench mini-suite 120 episodes：joint success 1.0000，执行 360 次 world rehearsal、720 次 role-wise advantage update；real_tool_responses=0，确保预测 observation 没被伪装成真实环境反馈。  环境 rehearsal / Agent RL Agent 交互策略学习：把轨迹反馈变成更新 EnvACE 的真实工具响应计数，为什么不能把 rehearsal 预测也算进去？ 这会把内部想象伪装成环境执行证据。文档mini-suite明确real_tool_responses=0，rehearsal和role-wise更新计数只证明对应路径发生，不证明浏览器或真实工具成功。 示意：三次预测observation只能记三次rehearsal，而不是三次真实API调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5bc4bf2059fbd6c1">EnvACE 的真实工具响应计数，为什么不能把 rehearsal 预测也算进去？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aenvace">EnvACE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这会把内部想象伪装成环境执行证据。文档mini-suite明确real_tool_responses=0，rehearsal和role-wise更新计数只证明对应路径发生，不证明浏览器或真实工具成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三次预测observation只能记三次rehearsal，而不是三次真实API调用。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06197">原论文</a> · <a href="../../../../agent-research/2608.06197-envace/">实现解读</a> · <a href="#qa-5bc4bf2059fbd6c1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoharness-rl" data-paper-title="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents Agent University of Illinois Urbana–Champaign / Meta AI 2026-08-05 主题：Harness policy RL。把 Belief、Progress、Experience 暴露为策略可操作的外部状态；先 SFT 学会 harness action，再以成本感知 GRPO 学习何时读写和合并。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness policy RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness policy RL Agent 交互策略学习：把轨迹反馈变成更新 EvoHarness-RL 为什么让读写运行状态也成为可训练动作？ Belief、Progress、Experience若只由固定脚本维护，策略无法学习何时值得更新或合并。方法先SFT学会harness action，再以任务回报与运行成本训练使用这些状态的时机。 示意：一个简单任务不必频繁改写经验库，长任务则可能需要保存阶段进度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-evoharness-rl-68a7cfc6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-071696521e65d6fd">EvoHarness-RL 为什么让读写运行状态也成为可训练动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoharness-rl">EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana–Champaign / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Belief、Progress、Experience若只由固定脚本维护，策略无法学习何时值得更新或合并。方法先SFT学会harness action，再以任务回报与运行成本训练使用这些状态的时机。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个简单任务不必频繁改写经验库，长任务则可能需要保存阶段进度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05446">原论文</a> · <a href="../../../../agent-research/2608.05446-evoharness-rl/">实现解读</a> · <a href="#qa-071696521e65d6fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoharness-rl" data-paper-title="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents Agent University of Illinois Urbana–Champaign / Meta AI 2026-08-05 主题：Harness policy RL。把 Belief、Progress、Experience 暴露为策略可操作的外部状态；先 SFT 学会 harness action，再以成本感知 GRPO 学习何时读写和合并。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness policy RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness policy RL Agent 交互策略学习：把轨迹反馈变成更新 为什么 Belief、Progress、Experience 要成为策略可读写的外部状态？ 固定框架替模型决定保存和合并什么，可能不适合当前任务。显式 harness action 让策略学习维护信念、进度与经验，先 SFT 学接口，再以任务收益减管理成本优化使用时机；写得越多不等于越好，状态内容也须由实际观察支持。 例如遇到新约束时写入 Belief，重复信息则合并进 Experience；若每轮无差别追加所有日志，管理费用会抵消任务收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f87d53ba6777d290">为什么 Belief、Progress、Experience 要成为策略可读写的外部状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoharness-rl">EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana–Champaign / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定框架替模型决定保存和合并什么，可能不适合当前任务。显式 harness action 让策略学习维护信念、进度与经验，先 SFT 学接口，再以任务收益减管理成本优化使用时机；写得越多不等于越好，状态内容也须由实际观察支持。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如遇到新约束时写入 Belief，重复信息则合并进 Experience；若每轮无差别追加所有日志，管理费用会抵消任务收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05446">原论文</a> · <a href="../../../../agent-research/2608.05446-evoharness-rl/">实现解读</a> · <a href="#qa-f87d53ba6777d290">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoharness-rl" data-paper-title="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents Agent University of Illinois Urbana–Champaign / Meta AI 2026-08-05 主题：Harness policy RL。把 Belief、Progress、Experience 暴露为策略可操作的外部状态；先 SFT 学会 harness action，再以成本感知 GRPO 学习何时读写和合并。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness policy RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness policy RL Agent 交互策略学习：把轨迹反馈变成更新 学习 harness policy 与固定配置记忆模块，优化对象有什么区别？ 固定模块规定存取流程；harness policy选择何时读写和合并，并为这些操作付成本。不能仅给固定流程登记一个“可进化”名字就认为策略已学会管理外部状态。 示意：每轮固定保存全部历史，与根据当前进度决定是否保存，是不同控制方式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-da44087982608915">学习 harness policy 与固定配置记忆模块，优化对象有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoharness-rl">EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana–Champaign / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定模块规定存取流程；harness policy选择何时读写和合并，并为这些操作付成本。不能仅给固定流程登记一个“可进化”名字就认为策略已学会管理外部状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>每轮固定保存全部历史，与根据当前进度决定是否保存，是不同控制方式。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05446">原论文</a> · <a href="../../../../agent-research/2608.05446-evoharness-rl/">实现解读</a> · <a href="#qa-da44087982608915">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoharness-rl" data-paper-title="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents Agent University of Illinois Urbana–Champaign / Meta AI 2026-08-05 主题：Harness policy RL。把 Belief、Progress、Experience 暴露为策略可操作的外部状态；先 SFT 学会 harness action，再以成本感知 GRPO 学习何时读写和合并。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness policy RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness policy RL Agent 交互策略学习：把轨迹反馈变成更新 EvoHarness-RL 的 harness 成本项，为什么要与真实执行日志绑定？ R=R_task−λC_harness中的成本应反映实际读写/合并，而不是只统计被提议的操作。还需核对状态更新是否被后续策略读到；本地mini-suite不等于原文完整大模型RL。 示意：生成了“合并经验”的文本但没有更新状态，不能记为一次成功harness操作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ac7fc64654335ad8">EvoHarness-RL 的 harness 成本项，为什么要与真实执行日志绑定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoharness-rl">EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana–Champaign / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>R=R_task−λC_harness中的成本应反映实际读写/合并，而不是只统计被提议的操作。还需核对状态更新是否被后续策略读到；本地mini-suite不等于原文完整大模型RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成了“合并经验”的文本但没有更新状态，不能记为一次成功harness操作。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05446">原论文</a> · <a href="../../../../agent-research/2608.05446-evoharness-rl/">实现解读</a> · <a href="#qa-ac7fc64654335ad8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ocsd" data-paper-title="OCSD" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="OCSD Agent Nanjing University 2026-08-05 直接重放未来 observation 时，token 分数变化同时来自观测信息和重放脚手架。OCSD 构造结构完全匹配的 Full 与 Observation-Ablated 两个 replay，仅以二者残差调制高不确定 step 的 GRPO 更新。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。执行 full/observation-ablated matched replay、residual calibration 和 turn-level credit。  观测校准蒸馏 Agent 交互策略学习：把轨迹反馈变成更新 OCSD 为什么担心 replay scaffold 本身改变 token 分数？ 重放未来observation时，额外结构和提示格式也会影响预测，不一定全来自观测信息。方法用结构匹配的Full与Observation-Ablated对照，提取更专注于观测的残差信号。 示意：加入一大段重放模板就改变了模型概率，不能把变化全记作环境证据贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-ocsd-b0061afd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f363eb1521afa2c4">OCSD 为什么担心 replay scaffold 本身改变 token 分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aocsd">OCSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重放未来observation时，额外结构和提示格式也会影响预测，不一定全来自观测信息。方法用结构匹配的Full与Observation-Ablated对照，提取更专注于观测的残差信号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>加入一大段重放模板就改变了模型概率，不能把变化全记作环境证据贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04788">原论文</a> · <a href="../../../../agent-research/2608.04788-ocsd/">实现解读</a> · <a href="#qa-f363eb1521afa2c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ocsd" data-paper-title="OCSD" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="OCSD Agent Nanjing University 2026-08-05 直接重放未来 observation 时，token 分数变化同时来自观测信息和重放脚手架。OCSD 构造结构完全匹配的 Full 与 Observation-Ablated 两个 replay，仅以二者残差调制高不确定 step 的 GRPO 更新。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。执行 full/observation-ablated matched replay、residual calibration 和 turn-level credit。  观测校准蒸馏 Agent 交互策略学习：把轨迹反馈变成更新 为什么 Full replay 要减去结构匹配的 Observation-Ablated replay？ 直接比较带未来观察的重放与学生，变化同时含观察内容和额外脚手架格式的影响。保持结构一致只消融观察，再取差值更集中识别信息贡献，之后只调高不确定步骤的更新；未来信息属于训练归因，不能成为测试时可见输入。 例如重放模板本身多了“请检查”提示，两种 replay 都保留它，只有真实观察有无不同，才能少把提示效应算给观察。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7cac41cdba0e5c86">为什么 Full replay 要减去结构匹配的 Observation-Ablated replay？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aocsd">OCSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接比较带未来观察的重放与学生，变化同时含观察内容和额外脚手架格式的影响。保持结构一致只消融观察，再取差值更集中识别信息贡献，之后只调高不确定步骤的更新；未来信息属于训练归因，不能成为测试时可见输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如重放模板本身多了“请检查”提示，两种 replay 都保留它，只有真实观察有无不同，才能少把提示效应算给观察。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04788">原论文</a> · <a href="../../../../agent-research/2608.04788-ocsd/">实现解读</a> · <a href="#qa-7cac41cdba0e5c86">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ocsd" data-paper-title="OCSD" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="OCSD Agent Nanjing University 2026-08-05 直接重放未来 observation 时，token 分数变化同时来自观测信息和重放脚手架。OCSD 构造结构完全匹配的 Full 与 Observation-Ablated 两个 replay，仅以二者残差调制高不确定 step 的 GRPO 更新。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。执行 full/observation-ablated matched replay、residual calibration 和 turn-level credit。  观测校准蒸馏 Agent 交互策略学习：把轨迹反馈变成更新 Full–Student gap 与 Full–Ablated 残差，校准掉的因素有什么不同？ 单gap同时包含观测内容和重放脚手架影响；匹配ablated对照在相同结构下移除观测，使两项差值进一步扣除共享影响。若两份模板不匹配，仍会残留新的混杂。 示意：只有Full里多了一句额外指令，Full−Ablated也会把那句指令效应误算进去。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a3015dc1b5914cab">Full–Student gap 与 Full–Ablated 残差，校准掉的因素有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aocsd">OCSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单gap同时包含观测内容和重放脚手架影响；匹配ablated对照在相同结构下移除观测，使两项差值进一步扣除共享影响。若两份模板不匹配，仍会残留新的混杂。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只有Full里多了一句额外指令，Full−Ablated也会把那句指令效应误算进去。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04788">原论文</a> · <a href="../../../../agent-research/2608.04788-ocsd/">实现解读</a> · <a href="#qa-a3015dc1b5914cab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ocsd" data-paper-title="OCSD" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="OCSD Agent Nanjing University 2026-08-05 直接重放未来 observation 时，token 分数变化同时来自观测信息和重放脚手架。OCSD 构造结构完全匹配的 Full 与 Observation-Ablated 两个 replay，仅以二者残差调制高不确定 step 的 GRPO 更新。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。执行 full/observation-ablated matched replay、residual calibration 和 turn-level credit。  观测校准蒸馏 Agent 交互策略学习：把轨迹反馈变成更新 OCSD 残差里的两个 student log-prob，在代数上应怎样抵消？ 同一token和student条件下，r=(logπ_full−logπ_S)−(logπ_abl−logπ_S)=logπ_full−logπ_abl。若两份student值来自不同前缀或token对齐，则不能这样抵消，需先修复匹配。 示意：用相同输入验证简化式与原式相同，可发现差值符号和位置错配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f927523ea57cddbb">OCSD 残差里的两个 student log-prob，在代数上应怎样抵消？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aocsd">OCSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一token和student条件下，r=(logπ_full−logπ_S)−(logπ_abl−logπ_S)=logπ_full−logπ_abl。若两份student值来自不同前缀或token对齐，则不能这样抵消，需先修复匹配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用相同输入验证简化式与原式相同，可发现差值符号和位置错配。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04788">原论文</a> · <a href="../../../../agent-research/2608.04788-ocsd/">实现解读</a> · <a href="#qa-f927523ea57cddbb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:state2state" data-paper-title="State2State: Environment-Derived Mid-Training for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="State2State: Environment-Derived Mid-Training for LLM Agents Agent Tsinghua University AIR / Alibaba Group 2026-08-05 主题：环境派生中训练。从环境探索自动采样起点与目标状态，用规则化状态匹配做 verifier，形成无需人工任务与专家轨迹的可扩展 mid-training。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的环境派生中训练算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  环境派生中训练 Agent 交互策略学习：把轨迹反馈变成更新 State2State 为什么能从环境探索中自动构造训练任务？ 探索产生可达起点与目标状态，用明确状态投影T匹配终点作为verifier，就可形成任务，不必每题人工写描述和专家动作轨迹。策略仍需自己寻找从起点到目标的过程。 示意：知道房间起点与目标布置，不代表同时知道应该依次执行哪些动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-state2state-baaabd4d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7d9b8c2719a98f32">State2State 为什么能从环境探索中自动构造训练任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Astate2state">State2State: Environment-Derived Mid-Training for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR / Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>探索产生可达起点与目标状态，用明确状态投影T匹配终点作为verifier，就可形成任务，不必每题人工写描述和专家动作轨迹。策略仍需自己寻找从起点到目标的过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>知道房间起点与目标布置，不代表同时知道应该依次执行哪些动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04934">原论文</a> · <a href="../../../../agent-research/2608.04934-state2state/">实现解读</a> · <a href="#qa-7d9b8c2719a98f32">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:state2state" data-paper-title="State2State: Environment-Derived Mid-Training for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="State2State: Environment-Derived Mid-Training for LLM Agents Agent Tsinghua University AIR / Alibaba Group 2026-08-05 主题：环境派生中训练。从环境探索自动采样起点与目标状态，用规则化状态匹配做 verifier，形成无需人工任务与专家轨迹的可扩展 mid-training。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的环境派生中训练算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  环境派生中训练 Agent 交互策略学习：把轨迹反馈变成更新 从环境起点与目标状态构造任务，为什么不需要同时提供专家动作轨迹？ 目标描述规定希望到达哪里，策略可通过探索尝试如何到达，规则化状态匹配仅负责最后验证。这样把任务生成与专家示范分开，扩大中训练来源；验证器内部目标或规则不能作为逐步正确动作提示，匹配定义也必须保留任务相关状态。 例如给出初始物体布局和目标布局，Agent 自己移动物体，环境最后比对；无需先给一条“先左后右”的标准操作序列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-af6d87b1df83394d">从环境起点与目标状态构造任务，为什么不需要同时提供专家动作轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Astate2state">State2State: Environment-Derived Mid-Training for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR / Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标描述规定希望到达哪里，策略可通过探索尝试如何到达，规则化状态匹配仅负责最后验证。这样把任务生成与专家示范分开，扩大中训练来源；验证器内部目标或规则不能作为逐步正确动作提示，匹配定义也必须保留任务相关状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给出初始物体布局和目标布局，Agent 自己移动物体，环境最后比对；无需先给一条“先左后右”的标准操作序列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04934">原论文</a> · <a href="../../../../agent-research/2608.04934-state2state/">实现解读</a> · <a href="#qa-af6d87b1df83394d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:state2state" data-paper-title="State2State: Environment-Derived Mid-Training for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="State2State: Environment-Derived Mid-Training for LLM Agents Agent Tsinghua University AIR / Alibaba Group 2026-08-05 主题：环境派生中训练。从环境探索自动采样起点与目标状态，用规则化状态匹配做 verifier，形成无需人工任务与专家轨迹的可扩展 mid-training。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的环境派生中训练算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  环境派生中训练 Agent 交互策略学习：把轨迹反馈变成更新 目标状态监督与行为克隆专家轨迹，给策略的信息相同吗？ 目标状态定义成功条件，行为克隆还给出动作序列。前者允许不同有效路径，不能把verifier里计算的专家路径偷偷传给策略后仍称无需专家轨迹。 示意：两条不同路线都到达目标，可以同样成功，而不必复制某条标准动作序列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-763bfc28ba021ee8">目标状态监督与行为克隆专家轨迹，给策略的信息相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Astate2state">State2State: Environment-Derived Mid-Training for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR / Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标状态定义成功条件，行为克隆还给出动作序列。前者允许不同有效路径，不能把verifier里计算的专家路径偷偷传给策略后仍称无需专家轨迹。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条不同路线都到达目标，可以同样成功，而不必复制某条标准动作序列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04934">原论文</a> · <a href="../../../../agent-research/2608.04934-state2state/">实现解读</a> · <a href="#qa-763bfc28ba021ee8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:state2state" data-paper-title="State2State: Environment-Derived Mid-Training for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="State2State: Environment-Derived Mid-Training for LLM Agents Agent Tsinghua University AIR / Alibaba Group 2026-08-05 主题：环境派生中训练。从环境探索自动采样起点与目标状态，用规则化状态匹配做 verifier，形成无需人工任务与专家轨迹的可扩展 mid-training。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的环境派生中训练算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  环境派生中训练 Agent 交互策略学习：把轨迹反馈变成更新 State2State 的 T(s_T)=T(s*)，为什么必须事先固定状态投影？ 投影决定哪些差异影响成功，临时为每次结果改T会改变任务。需核对起终状态、合法环境转移与匹配字段；本地状态算子不能替代原文真实环境的大模型中训练。 示意：若目标要求物品位置，不能在失败后把“位置”从匹配字段里删除以制造成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a7a8506d6f99e52e">State2State 的 T(s_T)=T(s*)，为什么必须事先固定状态投影？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Astate2state">State2State: Environment-Derived Mid-Training for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR / Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投影决定哪些差异影响成功，临时为每次结果改T会改变任务。需核对起终状态、合法环境转移与匹配字段；本地状态算子不能替代原文真实环境的大模型中训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若目标要求物品位置，不能在失败后把“位置”从匹配字段里删除以制造成功。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04934">原论文</a> · <a href="../../../../agent-research/2608.04934-state2state/">实现解读</a> · <a href="#qa-a7a8506d6f99e52e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hindsearch" data-paper-title="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning Agent Santa Clara University 2026-08-03 主题：搜索轨迹 hindsight。冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索轨迹 hindsight 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索轨迹 hindsight Agent 交互策略学习：把轨迹反馈变成更新 HindSearch 为什么在失败搜索轨迹完成后再生成 hindsight critique？ 终局成败信号很稀疏，冻结judge结合gold可指出整条失败搜索中的问题，再作为辅助on-policy蒸馏信号帮助训练。它利用事后信息解释失败，不是评测时给Agent提供未来答案。 示意：训练后指出“搜索忽略了关键证据”，用于改进下一轮策略而非替当前测试题作答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-hindsearch-b112afa3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-859ae4093ffa2212">HindSearch 为什么在失败搜索轨迹完成后再生成 hindsight critique？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahindsearch">HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Santa Clara University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局成败信号很稀疏，冻结judge结合gold可指出整条失败搜索中的问题，再作为辅助on-policy蒸馏信号帮助训练。它利用事后信息解释失败，不是评测时给Agent提供未来答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练后指出“搜索忽略了关键证据”，用于改进下一轮策略而非替当前测试题作答。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01597">原论文</a> · <a href="../../../../agent-research/2608.01597-hindsearch/">实现解读</a> · <a href="#qa-859ae4093ffa2212">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hindsearch" data-paper-title="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning Agent Santa Clara University 2026-08-03 主题：搜索轨迹 hindsight。冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索轨迹 hindsight 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索轨迹 hindsight Agent 交互策略学习：把轨迹反馈变成更新 judge 可看 gold 生成 critique 时，为什么不能把这段 critique 直接用于评测搜索？ gold 用于训练侧解释失败，把稀疏成败转成更具体的蒸馏信号，帮助策略学习纠错方向。评测若继续提供同题参考派生 critique，策略已间接得到答案信息，就不再衡量独立搜索；冻结 judge 只固定参数，并不消除其输入中的特权来源。 例如训练时根据正确日期指出查错来源，测试时仍必须只给日期问题；不能先送“正确应为周三”的批评再统计自主答对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-412d450bc5952de0">judge 可看 gold 生成 critique 时，为什么不能把这段 critique 直接用于评测搜索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahindsearch">HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Santa Clara University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>gold 用于训练侧解释失败，把稀疏成败转成更具体的蒸馏信号，帮助策略学习纠错方向。评测若继续提供同题参考派生 critique，策略已间接得到答案信息，就不再衡量独立搜索；冻结 judge 只固定参数，并不消除其输入中的特权来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练时根据正确日期指出查错来源，测试时仍必须只给日期问题；不能先送“正确应为周三”的批评再统计自主答对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01597">原论文</a> · <a href="../../../../agent-research/2608.01597-hindsearch/">实现解读</a> · <a href="#qa-412d450bc5952de0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hindsearch" data-paper-title="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning Agent Santa Clara University 2026-08-03 主题：搜索轨迹 hindsight。冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索轨迹 hindsight 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索轨迹 hindsight Agent 交互策略学习：把轨迹反馈变成更新 轨迹级 hindsight critique 与每步只给一个成功/失败数值，多提供了什么？ critique可定位搜索过程的具体不足及关联，而二值结果只说明最终是否成功。它仍由teacher/judge产生并有成本，也可能有误，不能把“解释更长”自动视为更准确监督。 示意：两个失败轨迹可能分别是检索不足和读错证据，单一0分无法区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0822ca2bca11cec5">轨迹级 hindsight critique 与每步只给一个成功/失败数值，多提供了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahindsearch">HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Santa Clara University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>critique可定位搜索过程的具体不足及关联，而二值结果只说明最终是否成功。它仍由teacher/judge产生并有成本，也可能有误，不能把“解释更长”自动视为更准确监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个失败轨迹可能分别是检索不足和读错证据，单一0分无法区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01597">原论文</a> · <a href="../../../../agent-research/2608.01597-hindsearch/">实现解读</a> · <a href="#qa-0822ca2bca11cec5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hindsearch" data-paper-title="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning Agent Santa Clara University 2026-08-03 主题：搜索轨迹 hindsight。冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索轨迹 hindsight 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索轨迹 hindsight Agent 交互策略学习：把轨迹反馈变成更新 HindSearch 中谁可以读取 gold，哪些输入绝不能进入独立评测搜索策略？ gold只属于训练期冻结judge和独立评分侧；由它生成的critique也是特权训练信号。评测策略不能接收这一题的gold、judge对象或gold衍生提示，否则搜索成功率会被污染。 示意：把judge刚根据标准答案写出的改正建议直接塞进测试搜索prompt，不是无泄漏推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0989636a7474d473">HindSearch 中谁可以读取 gold，哪些输入绝不能进入独立评测搜索策略？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahindsearch">HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Santa Clara University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>gold只属于训练期冻结judge和独立评分侧；由它生成的critique也是特权训练信号。评测策略不能接收这一题的gold、judge对象或gold衍生提示，否则搜索成功率会被污染。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把judge刚根据标准答案写出的改正建议直接塞进测试搜索prompt，不是无泄漏推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01597">原论文</a> · <a href="../../../../agent-research/2608.01597-hindsearch/">实现解读</a> · <a href="#qa-0989636a7474d473">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grsd" data-paper-title="Group-Reflective Self-Distillation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Group-Reflective Self-Distillation Agent Baidu Inc. 2026-07-30 轨迹终局 reward 混合了真正有效行为、重复错误与偶然选择。GRSD 让当前 policy 对同题 on-policy group 中每条已验证轨迹反思，再由参数相同的 stop-gradient 快照对比成功/失败反思，形成只在训练期可见的 DO/AVOID guidance，并调制 turn-level advantage。 保真度：执行成功/失败 rollout group、策略自身反思、stop-gradient group guidance 与 turn-level 更新。反思由可审计结构化轨迹产生，不是 Qwen 自然语言反思；验证的是 group contrast 和更新路由。本地对照口径：PlanBench mini-suite 120 episodes；joint success 1.0000，并执行 120 个反思组、120 次成败对照、360 次 privileged-guidance update。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 GRSD 为什么先反思同题的一组已验证成功和失败轨迹？ 终局reward把有效行为、重复错误和偶然选择混在一起。对同题成败反思做对照，可形成更具体的DO/AVOID指导，再用于调制turn级信用。 示意：同题两条轨迹都查了资料，但只有一条核对关键条件，对照有助于分辨有效行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-grsd-ed16d3df" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e89fb2bb2adfb023">GRSD 为什么先反思同题的一组已验证成功和失败轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agrsd">Group-Reflective Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局reward把有效行为、重复错误和偶然选择混在一起。对同题成败反思做对照，可形成更具体的DO/AVOID指导，再用于调制turn级信用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题两条轨迹都查了资料，但只有一条核对关键条件，对照有助于分辨有效行为。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28076">原论文</a> · <a href="../../../../agent-research/2607.28076-grsd/">实现解读</a> · <a href="#qa-e89fb2bb2adfb023">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grsd" data-paper-title="Group-Reflective Self-Distillation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Group-Reflective Self-Distillation Agent Baidu Inc. 2026-07-30 轨迹终局 reward 混合了真正有效行为、重复错误与偶然选择。GRSD 让当前 policy 对同题 on-policy group 中每条已验证轨迹反思，再由参数相同的 stop-gradient 快照对比成功/失败反思，形成只在训练期可见的 DO/AVOID guidance，并调制 turn-level advantage。 保真度：执行成功/失败 rollout group、策略自身反思、stop-gradient group guidance 与 turn-level 更新。反思由可审计结构化轨迹产生，不是 Qwen 自然语言反思；验证的是 group contrast 和更新路由。本地对照口径：PlanBench mini-suite 120 episodes；joint success 1.0000，并执行 120 个反思组、120 次成败对照、360 次 privileged-guidance update。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 DO/AVOID guidance 为什么由 stop-gradient 快照生成，并只在训练时可见？ 指导从同题已验证的成功失败反思形成，固定快照防止指导路径随当前梯度共同漂移。它调节 turn-level 信用而不让评测策略偷看整组事后成败；正乘数还保留结果优势方向，避免把某段反思本身当作答案或独立奖励 oracle。 例如组内成功者都先检查依赖，失败者直接改代码，训练可提炼这一对照；新测试题不能预先看到它自己的成功失败组反思。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-97caf32fa0217ef6">DO/AVOID guidance 为什么由 stop-gradient 快照生成，并只在训练时可见？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agrsd">Group-Reflective Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>指导从同题已验证的成功失败反思形成，固定快照防止指导路径随当前梯度共同漂移。它调节 turn-level 信用而不让评测策略偷看整组事后成败；正乘数还保留结果优势方向，避免把某段反思本身当作答案或独立奖励 oracle。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如组内成功者都先检查依赖，失败者直接改代码，训练可提炼这一对照；新测试题不能预先看到它自己的成功失败组反思。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28076">原论文</a> · <a href="../../../../agent-research/2607.28076-grsd/">实现解读</a> · <a href="#qa-97caf32fa0217ef6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grsd" data-paper-title="Group-Reflective Self-Distillation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Group-Reflective Self-Distillation Agent Baidu Inc. 2026-07-30 轨迹终局 reward 混合了真正有效行为、重复错误与偶然选择。GRSD 让当前 policy 对同题 on-policy group 中每条已验证轨迹反思，再由参数相同的 stop-gradient 快照对比成功/失败反思，形成只在训练期可见的 DO/AVOID guidance，并调制 turn-level advantage。 保真度：执行成功/失败 rollout group、策略自身反思、stop-gradient group guidance 与 turn-level 更新。反思由可审计结构化轨迹产生，不是 Qwen 自然语言反思；验证的是 group contrast 和更新路由。本地对照口径：PlanBench mini-suite 120 episodes；joint success 1.0000，并执行 120 个反思组、120 次成败对照、360 次 privileged-guidance update。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 GRSD 的成败组对照，与复制单条成功轨迹有什么不同？ 单条成功可能包含偶然或多余步骤；组对照利用失败反思识别哪些行为值得做或避免。它仍是训练指导，不应被误当成独立测试时可读取的解题oracle。 示意：成功轨迹里出现过的无关工具调用，不一定因“成功”二字就该全部学会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d2cc0c2d48d654f2">GRSD 的成败组对照，与复制单条成功轨迹有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agrsd">Group-Reflective Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单条成功可能包含偶然或多余步骤；组对照利用失败反思识别哪些行为值得做或避免。它仍是训练指导，不应被误当成独立测试时可读取的解题oracle。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>成功轨迹里出现过的无关工具调用，不一定因“成功”二字就该全部学会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28076">原论文</a> · <a href="../../../../agent-research/2607.28076-grsd/">实现解读</a> · <a href="#qa-d2cc0c2d48d654f2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grsd" data-paper-title="Group-Reflective Self-Distillation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Group-Reflective Self-Distillation Agent Baidu Inc. 2026-07-30 轨迹终局 reward 混合了真正有效行为、重复错误与偶然选择。GRSD 让当前 policy 对同题 on-policy group 中每条已验证轨迹反思，再由参数相同的 stop-gradient 快照对比成功/失败反思，形成只在训练期可见的 DO/AVOID guidance，并调制 turn-level advantage。 保真度：执行成功/失败 rollout group、策略自身反思、stop-gradient group guidance 与 turn-level 更新。反思由可审计结构化轨迹产生，不是 Qwen 自然语言反思；验证的是 group contrast 和更新路由。本地对照口径：PlanBench mini-suite 120 episodes；joint success 1.0000，并执行 120 个反思组、120 次成败对照、360 次 privileged-guidance update。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 GRSD 的正调制 m_t 为什么要与 outcome advantage 分开核对？ 文档m_t&gt;0只调整强度，保留原outcome advantage的符号；负值会反转原学习方向。guidance由stop-gradient快照生成且训练期可见，不能把特权指导继续留在评测输入中。 示意：原本应降低概率的动作，乘一个正m仍应降低，而不是被错误调制成奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0cf8f23b8cf80af1">GRSD 的正调制 m_t 为什么要与 outcome advantage 分开核对？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agrsd">Group-Reflective Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档m_t&gt;0只调整强度，保留原outcome advantage的符号；负值会反转原学习方向。guidance由stop-gradient快照生成且训练期可见，不能把特权指导继续留在评测输入中。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原本应降低概率的动作，乘一个正m仍应降低，而不是被错误调制成奖励。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28076">原论文</a> · <a href="../../../../agent-research/2607.28076-grsd/">实现解读</a> · <a href="#qa-0cf8f23b8cf80af1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tapo" data-paper-title="TAPO" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TAPO Agent Peking University 2026-07-30 稀疏任务 reward 只告诉 Agent 最终成败，没有利用每次动作后的环境反馈。TAPO 复用同一 rollout，在共享 backbone 上交替训练策略目标与的 next-observation 预测，不增加采样、专家数据或推理开销。 保真度：在确定性环境实际交替执行 policy action 与 action-conditioned next-observation supervision。确定性 observation 适合验证数据流与交替目标，不等同于 Qwen2.5 在 WebShop/ALFWorld 的 RL 训练。本地对照口径：PlanBench mini-suite 120 episodes；与只看 outcome 的 Agent 比较，TAPO 保持 joint success 1.0000，并新增 360 个 transition targets、预测准确率 1.0000。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 TAPO 为什么用已经发生的环境转移增加训练信号？ 同一rollout包含每步动作后的observation，不只是最终reward。把(s_t,a_t)预测s_{t+1}作为辅助目标，可让共享backbone学习动作后果，不必为这份监督另采专家轨迹。 示意：调用工具后实际返回的内容，可训练模型理解该动作会带来什么反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-tapo-abc37e08" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bff3209c0d122b62">TAPO 为什么用已经发生的环境转移增加训练信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atapo">TAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一rollout包含每步动作后的observation，不只是最终reward。把(s_t,a_t)预测s_{t+1}作为辅助目标，可让共享backbone学习动作后果，不必为这份监督另采专家轨迹。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>调用工具后实际返回的内容，可训练模型理解该动作会带来什么反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27973">原论文</a> · <a href="../../../../agent-research/2607.27973-tapo/">实现解读</a> · <a href="#qa-bff3209c0d122b62">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tapo" data-paper-title="TAPO" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TAPO Agent Peking University 2026-07-30 稀疏任务 reward 只告诉 Agent 最终成败，没有利用每次动作后的环境反馈。TAPO 复用同一 rollout，在共享 backbone 上交替训练策略目标与的 next-observation 预测，不增加采样、专家数据或推理开销。 保真度：在确定性环境实际交替执行 policy action 与 action-conditioned next-observation supervision。确定性 observation 适合验证数据流与交替目标，不等同于 Qwen2.5 在 WebShop/ALFWorld 的 RL 训练。本地对照口径：PlanBench mini-suite 120 episodes；与只看 outcome 的 Agent 比较，TAPO 保持 joint success 1.0000，并新增 360 个 transition targets、预测准确率 1.0000。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 复用 rollout 学下一观察，为什么能增加训练信号却不必增加部署推理步骤？ 每次环境转移已含状态、动作和下一观察，训练侧在共享骨干上加入预测目标即可利用它，无需再采专家或新 rollout。部署仍执行原策略，不要求显式调用预测器；辅助目标改善是否转成任务收益仍需对照，能预测反馈不等于会选好动作。 例如执行 ls 已得到目录列表，可把它用于训练状态转移预测；上线时仍直接选命令，不必每步先生成一份想象目录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e6111f746314c1da">复用 rollout 学下一观察，为什么能增加训练信号却不必增加部署推理步骤？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atapo">TAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每次环境转移已含状态、动作和下一观察，训练侧在共享骨干上加入预测目标即可利用它，无需再采专家或新 rollout。部署仍执行原策略，不要求显式调用预测器；辅助目标改善是否转成任务收益仍需对照，能预测反馈不等于会选好动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如执行 ls 已得到目录列表，可把它用于训练状态转移预测；上线时仍直接选命令，不必每步先生成一份想象目录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27973">原论文</a> · <a href="../../../../agent-research/2607.27973-tapo/">实现解读</a> · <a href="#qa-e6111f746314c1da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tapo" data-paper-title="TAPO" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TAPO Agent Peking University 2026-07-30 稀疏任务 reward 只告诉 Agent 最终成败，没有利用每次动作后的环境反馈。TAPO 复用同一 rollout，在共享 backbone 上交替训练策略目标与的 next-observation 预测，不增加采样、专家数据或推理开销。 保真度：在确定性环境实际交替执行 policy action 与 action-conditioned next-observation supervision。确定性 observation 适合验证数据流与交替目标，不等同于 Qwen2.5 在 WebShop/ALFWorld 的 RL 训练。本地对照口径：PlanBench mini-suite 120 episodes；与只看 outcome 的 Agent 比较，TAPO 保持 joint success 1.0000，并新增 360 个 transition targets、预测准确率 1.0000。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 TAPO 的训练期转移预测，与部署时必须额外调用 world model 一样吗？ 不一样。文档辅助目标用于共享backbone训练，部署不强制增加预测步骤；显式world-model planning则会增加在线调用。训练信号增多不自动意味着推理开销增加。 示意：模型学过下一observation预测，实际工具执行前仍可只生成原本的动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-70ad992f4cddf423">TAPO 的训练期转移预测，与部署时必须额外调用 world model 一样吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atapo">TAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不一样。文档辅助目标用于共享backbone训练，部署不强制增加预测步骤；显式world-model planning则会增加在线调用。训练信号增多不自动意味着推理开销增加。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型学过下一observation预测，实际工具执行前仍可只生成原本的动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27973">原论文</a> · <a href="../../../../agent-research/2607.27973-tapo/">实现解读</a> · <a href="#qa-70ad992f4cddf423">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tapo" data-paper-title="TAPO" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TAPO Agent Peking University 2026-07-30 稀疏任务 reward 只告诉 Agent 最终成败，没有利用每次动作后的环境反馈。TAPO 复用同一 rollout，在共享 backbone 上交替训练策略目标与的 next-observation 预测，不增加采样、专家数据或推理开销。 保真度：在确定性环境实际交替执行 policy action 与 action-conditioned next-observation supervision。确定性 observation 适合验证数据流与交替目标，不等同于 Qwen2.5 在 WebShop/ALFWorld 的 RL 训练。本地对照口径：PlanBench mini-suite 120 episodes；与只看 outcome 的 Agent 比较，TAPO 保持 joint success 1.0000，并新增 360 个 transition targets、预测准确率 1.0000。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 构造 TAPO transition target 时，为什么要核对 s_t、a_t 与下一条 observation 的归属？ 错位或跨episode拼接会把另一次动作的结果当监督。目标应来自同一rollout已发生的合法反馈，不能把s_{t+1}提前放进预测输入；mini-suite高准确率也不代表真实工具建模能力。 示意：第2步的动作应预测它引发的第3次观察，而不是下一任务的第一条观察。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-967576bf775d342b">构造 TAPO transition target 时，为什么要核对 s_t、a_t 与下一条 observation 的归属？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atapo">TAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>错位或跨episode拼接会把另一次动作的结果当监督。目标应来自同一rollout已发生的合法反馈，不能把s_{t+1}提前放进预测输入；mini-suite高准确率也不代表真实工具建模能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第2步的动作应预测它引发的第3次观察，而不是下一任务的第一条观察。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27973">原论文</a> · <a href="../../../../agent-research/2607.27973-tapo/">实现解读</a> · <a href="#qa-967576bf775d342b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cast" data-paper-title="CAST" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="CAST Agent University of Science and Technology of China 2026-07-28 把求解器状态价值的相邻差分变成 solver advantage，为稀疏结果奖励补充 turn 级 credit。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。没有复刻论文三类游戏的大规模 LLM RLVR；求解器准确，适合验证 credit assignment 而非模型能力。PlanBench mini-suite 的确定性最短路充当 solver，逐 turn 查询状态值并统计 credit update。  Agentic RL / turn-level credit Agent 交互策略学习：把轨迹反馈变成更新 CAST 为什么向求解器查询相邻状态价值，而不只看终局输赢？ 长程游戏的终局信号难定位单步贡献，solver对动作前后状态的价值变化可提供turn级credit，补充最终outcome，使训练更清楚某步如何改变局势。 示意：尚未结束的一步已明显改善可达结果，价值差可在终局前提供信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-cast-0c2b025a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1dd56ca2824b7355">CAST 为什么向求解器查询相邻状态价值，而不只看终局输赢？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acast">CAST</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长程游戏的终局信号难定位单步贡献，solver对动作前后状态的价值变化可提供turn级credit，补充最终outcome，使训练更清楚某步如何改变局势。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>尚未结束的一步已明显改善可达结果，价值差可在终局前提供信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25308">原论文</a> · <a href="../../../../agent-research/2607.25308-cast/">实现解读</a> · <a href="#qa-1dd56ca2824b7355">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cast" data-paper-title="CAST" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="CAST Agent University of Science and Technology of China 2026-07-28 把求解器状态价值的相邻差分变成 solver advantage，为稀疏结果奖励补充 turn 级 credit。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。没有复刻论文三类游戏的大规模 LLM RLVR；求解器准确，适合验证 credit assignment 而非模型能力。PlanBench mini-suite 的确定性最短路充当 solver，逐 turn 查询状态值并统计 credit update。  Agentic RL / turn-level credit Agent 交互策略学习：把轨迹反馈变成更新 solver 相邻状态价值差为什么能补充终局 outcome，而不是替代它？ 差值把状态向可解方向的变化转为局部信用，帮助识别长链中的关键一步；但 solver 估值可能不完美，局部改善也可能最终失败，所以保留任务结果优势作整体约束。训练侧价值接口若接触隐藏答案，必须与评测行动者的信息边界隔离。 例如一步约束化简让剩余问题更易解，可得到正局部信用；若后面写出无效结果，仍不能把整条轨迹当最终成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0544eb1cba34b953">solver 相邻状态价值差为什么能补充终局 outcome，而不是替代它？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acast">CAST</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>差值把状态向可解方向的变化转为局部信用，帮助识别长链中的关键一步；但 solver 估值可能不完美，局部改善也可能最终失败，所以保留任务结果优势作整体约束。训练侧价值接口若接触隐藏答案，必须与评测行动者的信息边界隔离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一步约束化简让剩余问题更易解，可得到正局部信用；若后面写出无效结果，仍不能把整条轨迹当最终成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25308">原论文</a> · <a href="../../../../agent-research/2607.25308-cast/">实现解读</a> · <a href="#qa-0544eb1cba34b953">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cast" data-paper-title="CAST" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="CAST Agent University of Science and Technology of China 2026-07-28 把求解器状态价值的相邻差分变成 solver advantage，为稀疏结果奖励补充 turn 级 credit。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。没有复刻论文三类游戏的大规模 LLM RLVR；求解器准确，适合验证 credit assignment 而非模型能力。PlanBench mini-suite 的确定性最短路充当 solver，逐 turn 查询状态值并统计 credit update。  Agentic RL / turn-level credit Agent 交互策略学习：把轨迹反馈变成更新 solver 状态价值与策略自己学的 value critic，监督来源一样吗？ solver来自可求解环境的外部计算，critic则通常从经验学习估计。前者依赖环境可求解性并有查询成本，不能把小型最短路oracle的准确度外推到任意真实Agent任务。 示意：确定性小图可精确求解，并不意味着真实网页任务也存在同样便宜的完美solver。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1351945562a08193">solver 状态价值与策略自己学的 value critic，监督来源一样吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acast">CAST</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>solver来自可求解环境的外部计算，critic则通常从经验学习估计。前者依赖环境可求解性并有查询成本，不能把小型最短路oracle的准确度外推到任意真实Agent任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>确定性小图可精确求解，并不意味着真实网页任务也存在同样便宜的完美solver。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25308">原论文</a> · <a href="../../../../agent-research/2607.25308-cast/">实现解读</a> · <a href="#qa-1351945562a08193">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cast" data-paper-title="CAST" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="CAST Agent University of Science and Technology of China 2026-07-28 把求解器状态价值的相邻差分变成 solver advantage，为稀疏结果奖励补充 turn 级 credit。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。没有复刻论文三类游戏的大规模 LLM RLVR；求解器准确，适合验证 credit assignment 而非模型能力。PlanBench mini-suite 的确定性最短路充当 solver，逐 turn 查询状态值并统计 credit update。  Agentic RL / turn-level credit Agent 交互策略学习：把轨迹反馈变成更新 CAST 计算 V(s_{t+1})−V(s_t) 时，怎样避免把状态顺序写反？ 同一动作前后状态必须成对绑定，并使用一致价值方向；顺序写反会把进步记成负credit。还要统计solver实际调用成本，训练teacher价值也不应作为评测策略的隐藏答案接口。 示意：价值从0.2升到0.5应得到+0.3，而不是−0.3。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-44cde34b2c4454d2">CAST 计算 V(s_{t+1})−V(s_t) 时，怎样避免把状态顺序写反？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acast">CAST</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一动作前后状态必须成对绑定，并使用一致价值方向；顺序写反会把进步记成负credit。还要统计solver实际调用成本，训练teacher价值也不应作为评测策略的隐藏答案接口。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>价值从0.2升到0.5应得到+0.3，而不是−0.3。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25308">原论文</a> · <a href="../../../../agent-research/2607.25308-cast/">实现解读</a> · <a href="#qa-44cde34b2c4454d2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seed" data-paper-title="SEED" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEED Agent Tsinghua University 2026-07-16 从已完成轨迹中反思出可复用 hindsight skill，再用 skill 条件前后的动作概率变化形成稠密 on-policy 蒸馏信号。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。使用确定性任务与结构化 skill，不执行视觉模型或大规模策略梯度训练。在 PlanBench mini-suite 中把成功/失败轨迹压缩为 hindsight skill，并记录 skill 数量、稠密 credit 更新和跨 episode 复用。  Agentic RL / hindsight skill Agent 交互策略学习：把轨迹反馈变成更新 SEED 为什么把已完成轨迹的反思整理为可复用 hindsight skill？ 反思若只停留在当前答案，难积累成稳定训练信号。SEED提取skill后，在相同原动作上比较有无skill的概率，形成稠密蒸馏并与outcome RL联合，促进经验复用。 示意：一次失败暴露的“先检查工具前置条件”可成为之后任务的训练指导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-seed-34cb6214" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5ff13b56066ad7da">SEED 为什么把已完成轨迹的反思整理为可复用 hindsight skill？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aseed">SEED</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反思若只停留在当前答案，难积累成稳定训练信号。SEED提取skill后，在相同原动作上比较有无skill的概率，形成稠密蒸馏并与outcome RL联合，促进经验复用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次失败暴露的“先检查工具前置条件”可成为之后任务的训练指导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14777">原论文</a> · <a href="../../../../agent-research/2607.14777-seed/">实现解读</a> · <a href="#qa-5ff13b56066ad7da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seed" data-paper-title="SEED" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEED Agent Tsinghua University 2026-07-16 从已完成轨迹中反思出可复用 hindsight skill，再用 skill 条件前后的动作概率变化形成稠密 on-policy 蒸馏信号。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。使用确定性任务与结构化 skill，不执行视觉模型或大规模策略梯度训练。在 PlanBench mini-suite 中把成功/失败轨迹压缩为 hindsight skill，并记录 skill 数量、稠密 credit 更新和跨 episode 复用。  Agentic RL / hindsight skill Agent 交互策略学习：把轨迹反馈变成更新 用 hindsight skill 前后动作概率差，为什么是在原动作上蒸馏而不是复制新专家轨迹？ 技能由已完成轨迹反思得到，再对学生实际访问状态和动作比较条件概率，形成更稠密的局部学习信号。它利用事后知识解释原行为，不要求教师另走一条不同路线；部署不能携带同题未来答案，技能本身的错误也可能污染信号，需保留验证边界。 例如学生已执行一次目录检查，反思技能指出该检查有用，就评估有无技能时这条原动作的概率，而非换成教师另写的命令。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-28ff13e83ba14c21">用 hindsight skill 前后动作概率差，为什么是在原动作上蒸馏而不是复制新专家轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aseed">SEED</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>技能由已完成轨迹反思得到，再对学生实际访问状态和动作比较条件概率，形成更稠密的局部学习信号。它利用事后知识解释原行为，不要求教师另走一条不同路线；部署不能携带同题未来答案，技能本身的错误也可能污染信号，需保留验证边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生已执行一次目录检查，反思技能指出该检查有用，就评估有无技能时这条原动作的概率，而非换成教师另写的命令。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14777">原论文</a> · <a href="../../../../agent-research/2607.14777-seed/">实现解读</a> · <a href="#qa-28ff13e83ba14c21">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seed" data-paper-title="SEED" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEED Agent Tsinghua University 2026-07-16 从已完成轨迹中反思出可复用 hindsight skill，再用 skill 条件前后的动作概率变化形成稠密 on-policy 蒸馏信号。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。使用确定性任务与结构化 skill，不执行视觉模型或大规模策略梯度训练。在 PlanBench mini-suite 中把成功/失败轨迹压缩为 hindsight skill，并记录 skill 数量、稠密 credit 更新和跨 episode 复用。  Agentic RL / hindsight skill Agent 交互策略学习：把轨迹反馈变成更新 SEED 在原动作上重打分，与让teacher另写完整成功轨迹有什么差别？ 前者保持学生实际访问的状态与动作，衡量skill条件对这些动作的改变；新专家轨迹可能走到另一批状态。它是on-policy重评分，不应偷换成只模仿另外的理想过程。 示意：学生确实执行过动作A，就比较A在两条件下的概率，而非拿从未执行的B替代记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1b8702074452165b">SEED 在原动作上重打分，与让teacher另写完整成功轨迹有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aseed">SEED</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者保持学生实际访问的状态与动作，衡量skill条件对这些动作的改变；新专家轨迹可能走到另一批状态。它是on-policy重评分，不应偷换成只模仿另外的理想过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生确实执行过动作A，就比较A在两条件下的概率，而非拿从未执行的B替代记录。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14777">原论文</a> · <a href="../../../../agent-research/2607.14777-seed/">实现解读</a> · <a href="#qa-1b8702074452165b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seed" data-paper-title="SEED" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEED Agent Tsinghua University 2026-07-16 从已完成轨迹中反思出可复用 hindsight skill，再用 skill 条件前后的动作概率变化形成稠密 on-policy 蒸馏信号。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。使用确定性任务与结构化 skill，不执行视觉模型或大规模策略梯度训练。在 PlanBench mini-suite 中把成功/失败轨迹压缩为 hindsight skill，并记录 skill 数量、稠密 credit 更新和跨 episode 复用。  Agentic RL / hindsight skill Agent 交互策略学习：把轨迹反馈变成更新 计算 SEED skill log-prob 差时，需要冻结哪些对齐条件？ 两项应对应同一s_t、同一a_t与同一策略评估口径，仅改变skill条件z；否则差值混入状态或动作变化。hindsight信息属于训练反馈，不能将当前评测题答案衍生skill泄漏给策略。 示意：有skill时评分A、无skill时评分B，两数之差不能解释为A获得的skill指导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-83fb8cee4148afc3">计算 SEED skill log-prob 差时，需要冻结哪些对齐条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aseed">SEED</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两项应对应同一s_t、同一a_t与同一策略评估口径，仅改变skill条件z；否则差值混入状态或动作变化。hindsight信息属于训练反馈，不能将当前评测题答案衍生skill泄漏给策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>有skill时评分A、无skill时评分B，两数之差不能解释为A获得的skill指导。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14777">原论文</a> · <a href="../../../../agent-research/2607.14777-seed/">实现解读</a> · <a href="#qa-83fb8cee4148afc3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:turn-opd" data-paper-title="TurnOPD" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TurnOPD Agent Academic author team 2026-07-07 用 probe 统计自适应决定 rollout 深度，并逐步把 token KL 预算迁移为 turn-normalized 监督。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。教师行为由确定性任务 oracle 提供；没有运行任务专用大模型教师。ScaleMCP mini-suite 中执行深度 probe、动态截断和 turn 归一化，记录节省的 rollout turns。  Agentic OPD / rollout budgeting Agent 交互策略学习：把轨迹反馈变成更新 TurnOPD 为什么同时研究 rollout 深度与 turn 内监督归一化？ 长程Agent的后续turn有不同训练价值和成本。probe用于决定采多深，turn-normalized KL改变长短回合的监督份额，分别控制采样预算和更新权重。 示意：少采几轮与减少一个长回合的相对权重，是两种独立节省方式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-turn-opd-4aa539f6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d1e3ea105a700501">TurnOPD 为什么同时研究 rollout 深度与 turn 内监督归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aturn-opd">TurnOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Academic author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长程Agent的后续turn有不同训练价值和成本。probe用于决定采多深，turn-normalized KL改变长短回合的监督份额，分别控制采样预算和更新权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>少采几轮与减少一个长回合的相对权重，是两种独立节省方式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.05804">原论文</a> · <a href="../../../../agent-research/2607.05804-turn-opd/">实现解读</a> · <a href="#qa-d1e3ea105a700501">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:turn-opd" data-paper-title="TurnOPD" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TurnOPD Agent Academic author team 2026-07-07 用 probe 统计自适应决定 rollout 深度，并逐步把 token KL 预算迁移为 turn-normalized 监督。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。教师行为由确定性任务 oracle 提供；没有运行任务专用大模型教师。ScaleMCP mini-suite 中执行深度 probe、动态截断和 turn 归一化，记录节省的 rollout turns。  Agentic OPD / rollout budgeting Agent 交互策略学习：把轨迹反馈变成更新 为什么把 KL 监督按 turn 长度归一化，能改变长短回合的训练权重？ 纯 token 求和让冗长回合天然贡献更多损失，可能压过短但关键的决策。turn-normalized 监督先在回合内平均，再依据 probe 分配 rollout 深度，把有限教师预算聚焦到有信息的交互；这改变的是权重与采样合同，不代表更深或更多监督必然更好。 例如一句关键工具选择只有十 token，另一轮长解释有两百 token；按回合平均可减少仅由长度造成的二十倍权重差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a39bbdba25423153">为什么把 KL 监督按 turn 长度归一化，能改变长短回合的训练权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aturn-opd">TurnOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Academic author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>纯 token 求和让冗长回合天然贡献更多损失，可能压过短但关键的决策。turn-normalized 监督先在回合内平均，再依据 probe 分配 rollout 深度，把有限教师预算聚焦到有信息的交互；这改变的是权重与采样合同，不代表更深或更多监督必然更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一句关键工具选择只有十 token，另一轮长解释有两百 token；按回合平均可减少仅由长度造成的二十倍权重差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.05804">原论文</a> · <a href="../../../../agent-research/2607.05804-turn-opd/">实现解读</a> · <a href="#qa-a39bbdba25423153">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:turn-opd" data-paper-title="TurnOPD" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TurnOPD Agent Academic author team 2026-07-07 用 probe 统计自适应决定 rollout 深度，并逐步把 token KL 预算迁移为 turn-normalized 监督。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。教师行为由确定性任务 oracle 提供；没有运行任务专用大模型教师。ScaleMCP mini-suite 中执行深度 probe、动态截断和 turn 归一化，记录节省的 rollout turns。  Agentic OPD / rollout budgeting Agent 交互策略学习：把轨迹反馈变成更新 每 token 平均 KL 与每 turn 除长度后求和，有何权重差异？ 逐token口径使长turn贡献更多项；每turn除以自身长度后，各回合更接近按回合单位计权。两种损失即使使用同一批token，也不是相同学习目标。 示意：一个10-token turn和一个100-token turn，先各自归一化不会让后者天然占十倍权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dd0b137eb5166900">每 token 平均 KL 与每 turn 除长度后求和，有何权重差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aturn-opd">TurnOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Academic author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐token口径使长turn贡献更多项；每turn除以自身长度后，各回合更接近按回合单位计权。两种损失即使使用同一批token，也不是相同学习目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个10-token turn和一个100-token turn，先各自归一化不会让后者天然占十倍权重。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.05804">原论文</a> · <a href="../../../../agent-research/2607.05804-turn-opd/">实现解读</a> · <a href="#qa-dd0b137eb5166900">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:turn-opd" data-paper-title="TurnOPD" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TurnOPD Agent Academic author team 2026-07-07 用 probe 统计自适应决定 rollout 深度，并逐步把 token KL 预算迁移为 turn-normalized 监督。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。教师行为由确定性任务 oracle 提供；没有运行任务专用大模型教师。ScaleMCP mini-suite 中执行深度 probe、动态截断和 turn 归一化，记录节省的 rollout turns。  Agentic OPD / rollout budgeting Agent 交互策略学习：把轨迹反馈变成更新 TurnOPD 动态截断后，loss 中是否还能保留被省略 turn 的 teacher 分数？ 监督应与实际rollout截断L*一致，避免对未采样回合使用虚构目标。还需处理有效响应长度；当前教师由确定性任务oracle提供，未运行任务专用大模型teacher。 示意：本次只采到第3轮，就不能仍把第4到6轮的预填答案计入同次训练证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-76ebf6fc34171b93">TurnOPD 动态截断后，loss 中是否还能保留被省略 turn 的 teacher 分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aturn-opd">TurnOPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Academic author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>监督应与实际rollout截断L*一致，避免对未采样回合使用虚构目标。还需处理有效响应长度；当前教师由确定性任务oracle提供，未运行任务专用大模型teacher。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>本次只采到第3轮，就不能仍把第4到6轮的预填答案计入同次训练证据。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.05804">原论文</a> · <a href="../../../../agent-research/2607.05804-turn-opd/">实现解读</a> · <a href="#qa-76ebf6fc34171b93">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:steppo" data-paper-title="StepPO" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="StepPO Agent University of Science and Technology of China 2026-04-20 Agent 的自然决策单位是“观察—动作”的 environment step，token-level MDP 会让动作粒度和信用粒度错位。StepPO 将交互重写为 step-level MDP，在 step boundary 估值和做 GAE，并把 step 内 token ratio 聚合后再裁剪。 在 PlanBench mini 的每个环境动作边界执行 step value、step GAE 与 step sequence-ratio clip，并公开对应诊断计数。本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 action 是确定性工具计划，不含真实 LLM token generation；验证的是 step 对齐状态机而非论文规模的 agent 训练。  Step-aligned Agent RL Agent 交互策略学习：把轨迹反馈变成更新 StepPO 为什么把观察—动作作为自然决策单位？ 一次工具动作往往由多个token共同表达，逐token估值可能与环境反馈边界错位。StepPO在step边界估值、计算GAE，并把动作内token ratio聚合为step ratio再裁剪。 示意：一个完整工具调用包含名称和参数，但环境只在调用完成后返回反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-steppo-4ceaabe2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ee8199c6224d4965">StepPO 为什么把观察—动作作为自然决策单位？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asteppo">StepPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一次工具动作往往由多个token共同表达，逐token估值可能与环境反馈边界错位。StepPO在step边界估值、计算GAE，并把动作内token ratio聚合为step ratio再裁剪。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个完整工具调用包含名称和参数，但环境只在调用完成后返回反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18401">原论文</a> · <a href="../../../../agent-research/2604.18401-steppo/">实现解读</a> · <a href="#qa-ee8199c6224d4965">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:steppo" data-paper-title="StepPO" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="StepPO Agent University of Science and Technology of China 2026-04-20 Agent 的自然决策单位是“观察—动作”的 environment step，token-level MDP 会让动作粒度和信用粒度错位。StepPO 将交互重写为 step-level MDP，在 step boundary 估值和做 GAE，并把 step 内 token ratio 聚合后再裁剪。 在 PlanBench mini 的每个环境动作边界执行 step value、step GAE 与 step sequence-ratio clip，并公开对应诊断计数。本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 action 是确定性工具计划，不含真实 LLM token generation；验证的是 step 对齐状态机而非论文规模的 agent 训练。  Step-aligned Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么 StepPO 先聚合一步内的 token ratio，再对 step ratio 裁剪？ 环境执行的是一整个动作，逐 token 独立裁剪与动作级概率变化并不相同。先把一步中 log ratio 平均并指数化，再在 step 边界估值与 GAE，使信用单位更接近环境转移；这不允许把工具观察算成动作 token，长度归一化也须保持一致。 例如一条 shell 命令拆成多个 token，环境只在命令完成后执行一次；应以这一步整体变化评价，而非让每个子词各自承担状态奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-77600865a38c44dc">为什么 StepPO 先聚合一步内的 token ratio，再对 step ratio 裁剪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asteppo">StepPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>环境执行的是一整个动作，逐 token 独立裁剪与动作级概率变化并不相同。先把一步中 log ratio 平均并指数化，再在 step 边界估值与 GAE，使信用单位更接近环境转移；这不允许把工具观察算成动作 token，长度归一化也须保持一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条 shell 命令拆成多个 token，环境只在命令完成后执行一次；应以这一步整体变化评价，而非让每个子词各自承担状态奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18401">原论文</a> · <a href="../../../../agent-research/2604.18401-steppo/">实现解读</a> · <a href="#qa-77600865a38c44dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:steppo" data-paper-title="StepPO" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="StepPO Agent University of Science and Technology of China 2026-04-20 Agent 的自然决策单位是“观察—动作”的 environment step，token-level MDP 会让动作粒度和信用粒度错位。StepPO 将交互重写为 step-level MDP，在 step boundary 估值和做 GAE，并把 step 内 token ratio 聚合后再裁剪。 在 PlanBench mini 的每个环境动作边界执行 step value、step GAE 与 step sequence-ratio clip，并公开对应诊断计数。本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 action 是确定性工具计划，不含真实 LLM token generation；验证的是 step 对齐状态机而非论文规模的 agent 训练。  Step-aligned Agent RL Agent 交互策略学习：把轨迹反馈变成更新 先裁剪各 token ratio 再平均，与先聚合 step ratio 再裁剪等价吗？ 不等价。clip是非线性操作，顺序会改变哪些整体动作受约束；文档先对log ratio取平均再exp得到几何平均step ratio，不是ratio的算术均值。 示意：动作里一项ratio很大、另一项很小，几何聚合与逐项clip可能给出不同更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bb09405ae546c81a">先裁剪各 token ratio 再平均，与先聚合 step ratio 再裁剪等价吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asteppo">StepPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等价。clip是非线性操作，顺序会改变哪些整体动作受约束；文档先对log ratio取平均再exp得到几何平均step ratio，不是ratio的算术均值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>动作里一项ratio很大、另一项很小，几何聚合与逐项clip可能给出不同更新。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18401">原论文</a> · <a href="../../../../agent-research/2604.18401-steppo/">实现解读</a> · <a href="#qa-bb09405ae546c81a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:steppo" data-paper-title="StepPO" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="StepPO Agent University of Science and Technology of China 2026-04-20 Agent 的自然决策单位是“观察—动作”的 environment step，token-level MDP 会让动作粒度和信用粒度错位。StepPO 将交互重写为 step-level MDP，在 step boundary 估值和做 GAE，并把 step 内 token ratio 聚合后再裁剪。 在 PlanBench mini 的每个环境动作边界执行 step value、step GAE 与 step sequence-ratio clip，并公开对应诊断计数。本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 action 是确定性工具计划，不含真实 LLM token generation；验证的是 step 对齐状态机而非论文规模的 agent 训练。  Step-aligned Agent RL Agent 交互策略学习：把轨迹反馈变成更新 StepPO 如何避免把 observation token 也混进动作 ratio 聚合？ 需要显式step和响应token边界，只聚合该动作的策略ratio，环境observation属于条件而非Agent生成动作。文档本地确定性工具计划只验证step状态机，不含真实LLM token rollout。 示意：工具返回一千字网页，不应被当成该次动作一千个策略token参与ratio均值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4af94536ae2c6cbc">StepPO 如何避免把 observation token 也混进动作 ratio 聚合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asteppo">StepPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需要显式step和响应token边界，只聚合该动作的策略ratio，环境observation属于条件而非Agent生成动作。文档本地确定性工具计划只验证step状态机，不含真实LLM token rollout。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工具返回一千字网页，不应被当成该次动作一千个策略token参与ratio均值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18401">原论文</a> · <a href="../../../../agent-research/2604.18401-steppo/">实现解读</a> · <a href="#qa-4af94536ae2c6cbc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searl" data-paper-title="SEARL" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEARL Agent Shanghai AI Laboratory 2026-04-09 把工具和成功转移维护为图记忆；新 rollout 同时更新 policy 与图边权，形成经验池—检索—改进闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3400；方法特有操作有非零 telemetry。  策略—工具图共进化 Agent 交互策略学习：把轨迹反馈变成更新 SEARL 为什么把工具经验存成带成功转移的图？ 图能表达工具与有效转移的关系，供后续检索和策略决策；新rollout再更新边权与policy，使经验不是静态说明书，而能随实际结果改变。 示意：某工具调用顺序多次成功后，其关联可在新任务里被更容易取回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-searl-fe3972b7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-56cf2479bbb6356c">SEARL 为什么把工具经验存成带成功转移的图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearl">SEARL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图能表达工具与有效转移的关系，供后续检索和策略决策；新rollout再更新边权与policy，使经验不是静态说明书，而能随实际结果改变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某工具调用顺序多次成功后，其关联可在新任务里被更容易取回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07791">原论文</a> · <a href="../../../../agent-research/2604.07791-searl/">实现解读</a> · <a href="#qa-56cf2479bbb6356c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searl" data-paper-title="SEARL" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEARL Agent Shanghai AI Laboratory 2026-04-09 把工具和成功转移维护为图记忆；新 rollout 同时更新 policy 与图边权，形成经验池—检索—改进闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3400；方法特有操作有非零 telemetry。  策略—工具图共进化 Agent 交互策略学习：把轨迹反馈变成更新 图记忆与 policy 为什么都要随新 rollout 更新，而不能只固定一张工具关系图？ 新执行会揭示哪些工具转移可用、哪些失败，图边权应反映这些证据；策略同时学习怎样利用更新后的关系。固定图只能复用旧经验，可能限制后续探索，单更新图又不保证策略会读；两侧闭环仍需真实奖励，不能用预设成功边制造进步。 例如新任务发现某工具返回可直接喂给另一工具，图中新增转移后，策略也要学会选这条路线，而不是永远沿旧流程行动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4211ad26baa9dca9">图记忆与 policy 为什么都要随新 rollout 更新，而不能只固定一张工具关系图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearl">SEARL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新执行会揭示哪些工具转移可用、哪些失败，图边权应反映这些证据；策略同时学习怎样利用更新后的关系。固定图只能复用旧经验，可能限制后续探索，单更新图又不保证策略会读；两侧闭环仍需真实奖励，不能用预设成功边制造进步。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新任务发现某工具返回可直接喂给另一工具，图中新增转移后，策略也要学会选这条路线，而不是永远沿旧流程行动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07791">原论文</a> · <a href="../../../../agent-research/2604.07791-searl/">实现解读</a> · <a href="#qa-4211ad26baa9dca9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searl" data-paper-title="SEARL" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEARL Agent Shanghai AI Laboratory 2026-04-09 把工具和成功转移维护为图记忆；新 rollout 同时更新 policy 与图边权，形成经验池—检索—改进闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3400；方法特有操作有非零 telemetry。  策略—工具图共进化 Agent 交互策略学习：把轨迹反馈变成更新 SEARL 的联合图/策略更新，与只改记忆库不改 policy 有什么差别？ 只改图主要改变外部检索信息，联合更新还改变策略如何使用这些信息并行动。反过来只训policy但固定图，也遗漏经验结构演化；两条状态轨迹需分别记录。 示意：图里新增一条成功边，不代表策略参数已学会在相关状态使用它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-158bda47b868b306">SEARL 的联合图/策略更新，与只改记忆库不改 policy 有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearl">SEARL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只改图主要改变外部检索信息，联合更新还改变策略如何使用这些信息并行动。反过来只训policy但固定图，也遗漏经验结构演化；两条状态轨迹需分别记录。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>图里新增一条成功边，不代表策略参数已学会在相关状态使用它。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07791">原论文</a> · <a href="../../../../agent-research/2604.07791-searl/">实现解读</a> · <a href="#qa-158bda47b868b306">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searl" data-paper-title="SEARL" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEARL Agent Shanghai AI Laboratory 2026-04-09 把工具和成功转移维护为图记忆；新 rollout 同时更新 policy 与图边权，形成经验池—检索—改进闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3400；方法特有操作有非零 telemetry。  策略—工具图共进化 Agent 交互策略学习：把轨迹反馈变成更新 SEARL 怎样证明图更新被后续决策实际消费，而非只写了日志？ 应对照rollout前后边权、后续检索命中与policy输入，验证更新确实改变可用经验。非零telemetry只说明操作发生，当前mini-suite不能因此升级为真实网页或多卡RL能力。 示意：边权文件改了，但后续策略始终读旧缓存，就没有形成所声明的经验闭环。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-50efd1f955befd96">SEARL 怎样证明图更新被后续决策实际消费，而非只写了日志？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearl">SEARL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应对照rollout前后边权、后续检索命中与policy输入，验证更新确实改变可用经验。非零telemetry只说明操作发生，当前mini-suite不能因此升级为真实网页或多卡RL能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>边权文件改了，但后续策略始终读旧缓存，就没有形成所声明的经验闭环。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07791">原论文</a> · <a href="../../../../agent-research/2604.07791-searl/">实现解读</a> · <a href="#qa-50efd1f955befd96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:simula" data-paper-title="Reasoning-Driven Synthetic Data Generation and Evaluation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Reasoning-Driven Synthetic Data Generation and Evaluation Agent EPFL 2026-03-31 单纯扩写种子容易遗漏概念或坍缩到相似样本。Simula 先按因素建立分类树，再控制全局节点组合与局部场景；独立批判过滤样本，并通过批内相对评分校准复杂度。语义生成器与批判模型是决定质量的核心，本地接口不能用启发式替代后宣称复现。§2 与附录 B/C/E 完整实验成本过高，不复现（审查 DONE）。CPU 协议组件，当前验证为 L0 接口与公式检验。没有把固定回调称为 M3 推理，也没有宣称合成数据质量提升。完整实验成本过高，不复现（审查 DONE）。TaxonomyModels 显式提供因素、提案、树 critic 和层计划；GenerationModels 显式提供策略、场景、复杂化、生成、要求批判、修改及正反两个批判回调。它们可接真实提供方，但本轮 runner 使用的都是标明 fixture 的独立调用。  Agent 数据合成 分类树与独立批判 Agent 交互策略学习：把轨迹反馈变成更新 Simula 为什么先建因素分类树，再生成具体样本？ 直接扩写种子容易覆盖不足或样本相似。分类树组织因素和组合空间，生成时再控制全局节点组合与局部场景，之后经独立批判和相对复杂度校准。 示意：先区分任务类型、条件与难度因素，再组合出不同案例，而非反复改写同一题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-simula-9d7ce82b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-43e969fdccf0f6d8">Simula 为什么先建因素分类树，再生成具体样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asimula">Reasoning-Driven Synthetic Data Generation and Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · EPFL</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接扩写种子容易覆盖不足或样本相似。分类树组织因素和组合空间，生成时再控制全局节点组合与局部场景，之后经独立批判和相对复杂度校准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先区分任务类型、条件与难度因素，再组合出不同案例，而非反复改写同一题。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.29791">原论文</a> · <a href="../../../../agent-research/2603.29791-simula/">实现解读</a> · <a href="#qa-43e969fdccf0f6d8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:simula" data-paper-title="Reasoning-Driven Synthetic Data Generation and Evaluation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Reasoning-Driven Synthetic Data Generation and Evaluation Agent EPFL 2026-03-31 单纯扩写种子容易遗漏概念或坍缩到相似样本。Simula 先按因素建立分类树，再控制全局节点组合与局部场景；独立批判过滤样本，并通过批内相对评分校准复杂度。语义生成器与批判模型是决定质量的核心，本地接口不能用启发式替代后宣称复现。§2 与附录 B/C/E 完整实验成本过高，不复现（审查 DONE）。CPU 协议组件，当前验证为 L0 接口与公式检验。没有把固定回调称为 M3 推理，也没有宣称合成数据质量提升。完整实验成本过高，不复现（审查 DONE）。TaxonomyModels 显式提供因素、提案、树 critic 和层计划；GenerationModels 显式提供策略、场景、复杂化、生成、要求批判、修改及正反两个批判回调。它们可接真实提供方，但本轮 runner 使用的都是标明 fixture 的独立调用。  Agent 数据合成 分类树与独立批判 Agent 交互策略学习：把轨迹反馈变成更新 正确性批判和错误性批判为什么不是同一判断的简单重复？ 生成样本可能让单个审查器迎合表面合理性，分别问支持正确与识别错误提供互补筛选；接纳同时要求需求满足、正批判肯定及负批判否定。因素树控制覆盖，批内相对难度再校准复杂度，不能用规则替代语义批判后声称数据质量已验证。 例如题目看似完整却暗含互斥条件，正向审查可能略过，专门寻找错误的批判应暴露矛盾，而非仅重复一句“看起来不错”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6dd6ff06e3e13093">正确性批判和错误性批判为什么不是同一判断的简单重复？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asimula">Reasoning-Driven Synthetic Data Generation and Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · EPFL</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成样本可能让单个审查器迎合表面合理性，分别问支持正确与识别错误提供互补筛选；接纳同时要求需求满足、正批判肯定及负批判否定。因素树控制覆盖，批内相对难度再校准复杂度，不能用规则替代语义批判后声称数据质量已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如题目看似完整却暗含互斥条件，正向审查可能略过，专门寻找错误的批判应暴露矛盾，而非仅重复一句“看起来不错”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.29791">原论文</a> · <a href="../../../../agent-research/2603.29791-simula/">实现解读</a> · <a href="#qa-6dd6ff06e3e13093">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:simula" data-paper-title="Reasoning-Driven Synthetic Data Generation and Evaluation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Reasoning-Driven Synthetic Data Generation and Evaluation Agent EPFL 2026-03-31 单纯扩写种子容易遗漏概念或坍缩到相似样本。Simula 先按因素建立分类树，再控制全局节点组合与局部场景；独立批判过滤样本，并通过批内相对评分校准复杂度。语义生成器与批判模型是决定质量的核心，本地接口不能用启发式替代后宣称复现。§2 与附录 B/C/E 完整实验成本过高，不复现（审查 DONE）。CPU 协议组件，当前验证为 L0 接口与公式检验。没有把固定回调称为 M3 推理，也没有宣称合成数据质量提升。完整实验成本过高，不复现（审查 DONE）。TaxonomyModels 显式提供因素、提案、树 critic 和层计划；GenerationModels 显式提供策略、场景、复杂化、生成、要求批判、修改及正反两个批判回调。它们可接真实提供方，但本轮 runner 使用的都是标明 fixture 的独立调用。  Agent 数据合成 分类树与独立批判 Agent 交互策略学习：把轨迹反馈变成更新 Simula 的 Elo 相对复杂度，与一个模型直接给绝对难度分有何不同？ Elo用批内成对比较的胜负更新相对排名，结果与对局和超参有关；绝对分数是另一种尺度。文档明确本地初始1000、尺度400、k32是显式配置，不冒称作者唯一设定。 示意：某题相对同批其它题更难，不等于已拥有跨所有任务通用的绝对难度单位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-172bf44316db2ae0">Simula 的 Elo 相对复杂度，与一个模型直接给绝对难度分有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asimula">Reasoning-Driven Synthetic Data Generation and Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · EPFL</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Elo用批内成对比较的胜负更新相对排名，结果与对局和超参有关；绝对分数是另一种尺度。文档明确本地初始1000、尺度400、k32是显式配置，不冒称作者唯一设定。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某题相对同批其它题更难，不等于已拥有跨所有任务通用的绝对难度单位。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.29791">原论文</a> · <a href="../../../../agent-research/2603.29791-simula/">实现解读</a> · <a href="#qa-172bf44316db2ae0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:simula" data-paper-title="Reasoning-Driven Synthetic Data Generation and Evaluation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Reasoning-Driven Synthetic Data Generation and Evaluation Agent EPFL 2026-03-31 单纯扩写种子容易遗漏概念或坍缩到相似样本。Simula 先按因素建立分类树，再控制全局节点组合与局部场景；独立批判过滤样本，并通过批内相对评分校准复杂度。语义生成器与批判模型是决定质量的核心，本地接口不能用启发式替代后宣称复现。§2 与附录 B/C/E 完整实验成本过高，不复现（审查 DONE）。CPU 协议组件，当前验证为 L0 接口与公式检验。没有把固定回调称为 M3 推理，也没有宣称合成数据质量提升。完整实验成本过高，不复现（审查 DONE）。TaxonomyModels 显式提供因素、提案、树 critic 和层计划；GenerationModels 显式提供策略、场景、复杂化、生成、要求批判、修改及正反两个批判回调。它们可接真实提供方，但本轮 runner 使用的都是标明 fixture 的独立调用。  Agent 数据合成 分类树与独立批判 Agent 交互策略学习：把轨迹反馈变成更新 Simula 正反 critic 共用同一底模时，能把第一次 verdict 塞给第二次吗？ 不能。二者应独立调用、各自只收到样本；接纳需要求critic通过、correct肯定且incorrect否定。语义生成与批判是核心，fixture回调或短文本零13-gram重叠不能证明完整质量或无污染。 示意：先告诉错误性critic“另一个已判正确”，会破坏两份独立判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-42fd38ef1def93cd">Simula 正反 critic 共用同一底模时，能把第一次 verdict 塞给第二次吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asimula">Reasoning-Driven Synthetic Data Generation and Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · EPFL</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。二者应独立调用、各自只收到样本；接纳需要求critic通过、correct肯定且incorrect否定。语义生成与批判是核心，fixture回调或短文本零13-gram重叠不能证明完整质量或无污染。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先告诉错误性critic“另一个已判正确”，会破坏两份独立判断。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与调用边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.29791">原论文</a> · <a href="../../../../agent-research/2603.29791-simula/">实现解读</a> · <a href="#qa-42fd38ef1def93cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dmast" data-paper-title="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks Agent University of California, Berkeley 2026-03-04 DMAST 让防守 Agent 与攻击者共享同一 VLM 参数，以不同角色提示交互；先教师模仿，再用不改变目标动作的 oracle reasoning 做 SFT，最后进行共享策略自博弈 RL。改动不只是普通 GRPO：受攻击组中两个角色的原始终局奖励共同决定均值与方差，而成功样本的长度惩罚只进入优势分子。 完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。诊断让同一个微型神经策略处理两种角色，真实执行一次 SGD，并与独立直接公式核对值和梯度。L1 Stage-3 数值组件，diagnostic only，不是浏览器 Agent 能力或完整三阶段复现。完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。只保留 Stage-3 精确组统计与 token 目标；不生成攻击载荷、不访问网页、不加载 VLM、不训练 SFT 或 oracle。length_penalty 是外部提供的；  Agentic RL 共享策略对抗训练 Agent 交互策略学习：把轨迹反馈变成更新 DMAST 为什么用同一 VLM 参数承担 Agent 与攻击者两种角色？ 共享参数以角色条件进行交互和自博弈，使鲁棒性训练同时涉及防守决策与攻击过程。完整方法还有教师模仿和oracle reasoning SFT，Stage3奖励公式只是其中一段。 示意：同一底模在不同角色提示下生成各自轨迹，并非两套毫无共享的策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-dmast-279d6cde" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b729efde757ea518">DMAST 为什么用同一 VLM 参数承担 Agent 与攻击者两种角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Admast">Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享参数以角色条件进行交互和自博弈，使鲁棒性训练同时涉及防守决策与攻击过程。完整方法还有教师模仿和oracle reasoning SFT，Stage3奖励公式只是其中一段。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一底模在不同角色提示下生成各自轨迹，并非两套毫无共享的策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04364v1">原论文</a> · <a href="../../../../agent-research/2603.04364-dmast/">实现解读</a> · <a href="#qa-b729efde757ea518">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dmast" data-paper-title="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks Agent University of California, Berkeley 2026-03-04 DMAST 让防守 Agent 与攻击者共享同一 VLM 参数，以不同角色提示交互；先教师模仿，再用不改变目标动作的 oracle reasoning 做 SFT，最后进行共享策略自博弈 RL。改动不只是普通 GRPO：受攻击组中两个角色的原始终局奖励共同决定均值与方差，而成功样本的长度惩罚只进入优势分子。 完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。诊断让同一个微型神经策略处理两种角色，真实执行一次 SGD，并与独立直接公式核对值和梯度。L1 Stage-3 数值组件，diagnostic only，不是浏览器 Agent 能力或完整三阶段复现。完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。只保留 Stage-3 精确组统计与 token 目标；不生成攻击载荷、不访问网页、不加载 VLM、不训练 SFT 或 oracle。length_penalty 是外部提供的；  Agentic RL 共享策略对抗训练 Agent 交互策略学习：把轨迹反馈变成更新 为什么组均值方差用 raw reward，而成功长度罚只进入优势分子？ 长度罚旨在调节某条成功响应的信用，不应同时重定义全组基线尺度。受攻击组还联合攻击与防守角色的原始回报统计，若先减罚再白化，就改变双方比较与原算法；零方差组需排除，不能靠任意 epsilon 制造学习信号。 例如两条同样成功的响应一长一短，长度罚降低长者优势，但共同基线仍按原始任务回报计算，不能被长文本额外拖动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8e05154677691641">为什么组均值方差用 raw reward，而成功长度罚只进入优势分子？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Admast">Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长度罚旨在调节某条成功响应的信用，不应同时重定义全组基线尺度。受攻击组还联合攻击与防守角色的原始回报统计，若先减罚再白化，就改变双方比较与原算法；零方差组需排除，不能靠任意 epsilon 制造学习信号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条同样成功的响应一长一短，长度罚降低长者优势，但共同基线仍按原始任务回报计算，不能被长文本额外拖动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04364v1">原论文</a> · <a href="../../../../agent-research/2603.04364-dmast/">实现解读</a> · <a href="#qa-8e05154677691641">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dmast" data-paper-title="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks Agent University of California, Berkeley 2026-03-04 DMAST 让防守 Agent 与攻击者共享同一 VLM 参数，以不同角色提示交互；先教师模仿，再用不改变目标动作的 oracle reasoning 做 SFT，最后进行共享策略自博弈 RL。改动不只是普通 GRPO：受攻击组中两个角色的原始终局奖励共同决定均值与方差，而成功样本的长度惩罚只进入优势分子。 完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。诊断让同一个微型神经策略处理两种角色，真实执行一次 SGD，并与独立直接公式核对值和梯度。L1 Stage-3 数值组件，diagnostic only，不是浏览器 Agent 能力或完整三阶段复现。完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。只保留 Stage-3 精确组统计与 token 目标；不生成攻击载荷、不访问网页、不加载 VLM、不训练 SFT 或 oracle。length_penalty 是外部提供的；  Agentic RL 共享策略对抗训练 Agent 交互策略学习：把轨迹反馈变成更新 只实现 DMAST 组统计目标，与复现视觉 Agent 对抗训练有什么差距？ 组统计可验证loss与梯度，但完整方法还需真实VLM、环境交互、教师模仿、oracle SFT和自博弈。数学诊断不生成攻击载荷，也不证明浏览器成功率或对抗鲁棒性。 示意：微型策略一次SGD与大模型在环境里经历完整多阶段训练，不能共用能力结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-389529b5addb5ba5">只实现 DMAST 组统计目标，与复现视觉 Agent 对抗训练有什么差距？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Admast">Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组统计可验证loss与梯度，但完整方法还需真实VLM、环境交互、教师模仿、oracle SFT和自博弈。数学诊断不生成攻击载荷，也不证明浏览器成功率或对抗鲁棒性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>微型策略一次SGD与大模型在环境里经历完整多阶段训练，不能共用能力结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04364v1">原论文</a> · <a href="../../../../agent-research/2603.04364-dmast/">实现解读</a> · <a href="#qa-389529b5addb5ba5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dmast" data-paper-title="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks Agent University of California, Berkeley 2026-03-04 DMAST 让防守 Agent 与攻击者共享同一 VLM 参数，以不同角色提示交互；先教师模仿，再用不改变目标动作的 oracle reasoning 做 SFT，最后进行共享策略自博弈 RL。改动不只是普通 GRPO：受攻击组中两个角色的原始终局奖励共同决定均值与方差，而成功样本的长度惩罚只进入优势分子。 完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。诊断让同一个微型神经策略处理两种角色，真实执行一次 SGD，并与独立直接公式核对值和梯度。L1 Stage-3 数值组件，diagnostic only，不是浏览器 Agent 能力或完整三阶段复现。完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。只保留 Stage-3 精确组统计与 token 目标；不生成攻击载荷、不访问网页、不加载 VLM、不训练 SFT 或 oracle。length_penalty 是外部提供的；  Agentic RL 共享策略对抗训练 Agent 交互策略学习：把轨迹反馈变成更新 DMAST 的训推概率比应乘到 PG 与 KL 两项上吗？ 文档仅对PG乘min(π_old/π_sampling,1)，小于0.1时PG权重归零，KL项不因此一并缩放。组方差为零直接排除，分母仍为全批有效响应token，而非角色局部平均。 示意：某token的PG因低采样比被关闭，不代表reference KL也可顺手删掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-70306168e069480f">DMAST 的训推概率比应乘到 PG 与 KL 两项上吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Admast">Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档仅对PG乘min(π_old/π_sampling,1)，小于0.1时PG权重归零，KL项不因此一并缩放。组方差为零直接排除，分母仍为全批有效响应token，而非角色局部平均。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某token的PG因低采样比被关闭，不代表reference KL也可顺手删掉。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04364v1">原论文</a> · <a href="../../../../agent-research/2603.04364-dmast/">实现解读</a> · <a href="#qa-70306168e069480f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pearl" data-paper-title="PEARL" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PEARL Agent 中国科学院信息工程研究所 2026-01-28 多跳工具调用同时受工具幻觉、参数错误和长程规划薄弱影响。PEARL 的离线阶段用 trial-and-error 建立工具用法与失败条件；在线阶段把 Planner 与 Executor 解耦，用计划正确性、工具链与最终结果组成的密集 reward 进行 GRPO，而不是只依赖稀疏成功信号。 未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。PEARL 先离线探索工具的有效参数与失败条件，再用 planning-centric reward 和 GRPO 训练独立 Planner，把可靠执行与长程规划分开优化。实现离线候选计划探索、planning reward、组内选择更新、Planner/Executor 解耦和跨 episode 复用；未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。  规划强化学习 Agent 交互策略学习：把轨迹反馈变成更新 PEARL 为什么在在线规划前先做离线工具 trial-and-error？ 工具幻觉和参数错误会破坏多跳计划。离线探索整理工具用法与失败条件，在线再分离Planner与Executor，使计划生成可以利用更可靠的工具经验。 示意：先知道工具需要哪类参数以及何时失败，再让Planner决定调用顺序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-pearl-a555b8b4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-929aae8a41b36595">PEARL 为什么在在线规划前先做离线工具 trial-and-error？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apearl">PEARL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 中国科学院信息工程研究所</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具幻觉和参数错误会破坏多跳计划。离线探索整理工具用法与失败条件，在线再分离Planner与Executor，使计划生成可以利用更可靠的工具经验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先知道工具需要哪类参数以及何时失败，再让Planner决定调用顺序。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20439">原论文</a> · <a href="../../../../agent-research/2601.20439-pearl/">实现解读</a> · <a href="#qa-929aae8a41b36595">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pearl" data-paper-title="PEARL" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PEARL Agent 中国科学院信息工程研究所 2026-01-28 多跳工具调用同时受工具幻觉、参数错误和长程规划薄弱影响。PEARL 的离线阶段用 trial-and-error 建立工具用法与失败条件；在线阶段把 Planner 与 Executor 解耦，用计划正确性、工具链与最终结果组成的密集 reward 进行 GRPO，而不是只依赖稀疏成功信号。 未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。PEARL 先离线探索工具的有效参数与失败条件，再用 planning-centric reward 和 GRPO 训练独立 Planner，把可靠执行与长程规划分开优化。实现离线候选计划探索、planning reward、组内选择更新、Planner/Executor 解耦和跨 episode 复用；未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。  规划强化学习 Agent 交互策略学习：把轨迹反馈变成更新 为什么 Planner 与 Executor 分开后，仍需要工具链与最终结果共同奖励？ 计划格式正确不保证工具存在、顺序可执行或答案成立，执行器也可能在合理计划下填错参数。离线试错先积累用法与失败条件，在线密集信号分别约束工具、顺序和结果，使规划能学到可执行结构；单个过程分高不能替代任务实际成功。 例如计划先查询订单再退款顺序正确，但订单 ID 错了仍会失败；奖励应同时反映工具链合理性与最终操作结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c63eec069a33caa8">为什么 Planner 与 Executor 分开后，仍需要工具链与最终结果共同奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apearl">PEARL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 中国科学院信息工程研究所</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>计划格式正确不保证工具存在、顺序可执行或答案成立，执行器也可能在合理计划下填错参数。离线试错先积累用法与失败条件，在线密集信号分别约束工具、顺序和结果，使规划能学到可执行结构；单个过程分高不能替代任务实际成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如计划先查询订单再退款顺序正确，但订单 ID 错了仍会失败；奖励应同时反映工具链合理性与最终操作结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20439">原论文</a> · <a href="../../../../agent-research/2601.20439-pearl/">实现解读</a> · <a href="#qa-c63eec069a33caa8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pearl" data-paper-title="PEARL" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PEARL Agent 中国科学院信息工程研究所 2026-01-28 多跳工具调用同时受工具幻觉、参数错误和长程规划薄弱影响。PEARL 的离线阶段用 trial-and-error 建立工具用法与失败条件；在线阶段把 Planner 与 Executor 解耦，用计划正确性、工具链与最终结果组成的密集 reward 进行 GRPO，而不是只依赖稀疏成功信号。 未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。PEARL 先离线探索工具的有效参数与失败条件，再用 planning-centric reward 和 GRPO 训练独立 Planner，把可靠执行与长程规划分开优化。实现离线候选计划探索、planning reward、组内选择更新、Planner/Executor 解耦和跨 episode 复用；未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。  规划强化学习 Agent 交互策略学习：把轨迹反馈变成更新 Planner/Executor 解耦与一个模型一边想一边调用工具，训练反馈如何不同？ 解耦可把计划组的工具选择、顺序与最终成功作为规划奖励，同时让Executor负责实际执行反馈。它不保证仅靠好计划就成功，工具参数与运行后果仍需核验。 示意：计划选对了三种工具，但Executor参数错了，最终结果仍可能失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-76d0171ea8615e7d">Planner/Executor 解耦与一个模型一边想一边调用工具，训练反馈如何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apearl">PEARL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 中国科学院信息工程研究所</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>解耦可把计划组的工具选择、顺序与最终成功作为规划奖励，同时让Executor负责实际执行反馈。它不保证仅靠好计划就成功，工具参数与运行后果仍需核验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>计划选对了三种工具，但Executor参数错了，最终结果仍可能失败。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20439">原论文</a> · <a href="../../../../agent-research/2601.20439-pearl/">实现解读</a> · <a href="#qa-76d0171ea8615e7d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pearl" data-paper-title="PEARL" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PEARL Agent 中国科学院信息工程研究所 2026-01-28 多跳工具调用同时受工具幻觉、参数错误和长程规划薄弱影响。PEARL 的离线阶段用 trial-and-error 建立工具用法与失败条件；在线阶段把 Planner 与 Executor 解耦，用计划正确性、工具链与最终结果组成的密集 reward 进行 GRPO，而不是只依赖稀疏成功信号。 未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。PEARL 先离线探索工具的有效参数与失败条件，再用 planning-centric reward 和 GRPO 训练独立 Planner，把可靠执行与长程规划分开优化。实现离线候选计划探索、planning reward、组内选择更新、Planner/Executor 解耦和跨 episode 复用；未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。  规划强化学习 Agent 交互策略学习：把轨迹反馈变成更新 PEARL 的 tool/order/success 分项为什么要保留，而不只存总 reward？ 不同分项对应工具身份、顺序和完成情况，可定位规划更新信号并核对加权方向。只存总分会掩盖错误组件；本地计划探索与复用不等于已跑ToolHop真实API或完整GRPO。 示意：工具都选对但顺序错，总reward低的原因应在order项中可见。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b9c18c460dc7c583">PEARL 的 tool/order/success 分项为什么要保留，而不只存总 reward？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apearl">PEARL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 中国科学院信息工程研究所</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同分项对应工具身份、顺序和完成情况，可定位规划更新信号并核对加权方向。只存总分会掩盖错误组件；本地计划探索与复用不等于已跑ToolHop真实API或完整GRPO。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工具都选对但顺序错，总reward低的原因应在order项中可见。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20439">原论文</a> · <a href="../../../../agent-research/2601.20439-pearl/">实现解读</a> · <a href="#qa-b9c18c460dc7c583">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent0" data-paper-title="Agent0" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent0 Agent University of North Carolina at Chapel Hill 2025-11-20 任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  零数据多 Agent Agent 交互策略学习：把轨迹反馈变成更新 Agent0 为什么让任务生成 Agent 与多个执行 Agent 组成课程？ 可验证任务可自动产生训练机会，多个执行候选提供群体反馈，再按当前能力边界提高任务难度。零人工数据不代表没有成功标准，verifier仍是课程质量的重要约束。 示意：执行者普遍掌握一类任务后，生成者再提出稍难但可验证的新任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent0-bc007c7f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8d1f4c7bee308515">Agent0 为什么让任务生成 Agent 与多个执行 Agent 组成课程？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent0">Agent0</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of North Carolina at Chapel Hill</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可验证任务可自动产生训练机会，多个执行候选提供群体反馈，再按当前能力边界提高任务难度。零人工数据不代表没有成功标准，verifier仍是课程质量的重要约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>执行者普遍掌握一类任务后，生成者再提出稍难但可验证的新任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.16043">原论文</a> · <a href="../../../../agent-research/2511.16043-agent0/">实现解读</a> · <a href="#qa-8d1f4c7bee308515">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent0" data-paper-title="Agent0" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent0 Agent University of North Carolina at Chapel Hill 2025-11-20 任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  零数据多 Agent Agent 交互策略学习：把轨迹反馈变成更新 多数投票为什么还必须接受任务 verifier 检查，而不能把一致答案直接当真？ 多个执行者可能共享同一错误先验，投票提高一致性却不提供独立事实保证。可验证任务用外部规则判断候选答案，课程再按当前能力边界升级；若生成器或投票器读取参考答案，训练闭环就变成泄漏，不能作为自主工具能力证据。 例如五名执行者都把单位换算错成同一数值，票数很高仍是错误；verifier 应按任务合同检查，而非按赞同人数决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-67c36df868cd6ab4">多数投票为什么还必须接受任务 verifier 检查，而不能把一致答案直接当真？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent0">Agent0</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of North Carolina at Chapel Hill</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个执行者可能共享同一错误先验，投票提高一致性却不提供独立事实保证。可验证任务用外部规则判断候选答案，课程再按当前能力边界升级；若生成器或投票器读取参考答案，训练闭环就变成泄漏，不能作为自主工具能力证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如五名执行者都把单位换算错成同一数值，票数很高仍是错误；verifier 应按任务合同检查，而非按赞同人数决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.16043">原论文</a> · <a href="../../../../agent-research/2511.16043-agent0/">实现解读</a> · <a href="#qa-67c36df868cd6ab4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent0" data-paper-title="Agent0" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent0 Agent University of North Carolina at Chapel Hill 2025-11-20 任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  零数据多 Agent Agent 交互策略学习：把轨迹反馈变成更新 多 Agent 多数一致，与独立 verifier 通过提供的是同一种证据吗？ 一致性衡量候选是否相同，verifier检查它是否满足任务；共同错误也可形成多数。群体候选不能自我证明正确，课程升级也不能只以投票一致作为能力已提高。 示意：五个Agent都输出同一个错误结果，投票仍一致，但verifier应判失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1054f5b756fea842">多 Agent 多数一致，与独立 verifier 通过提供的是同一种证据吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent0">Agent0</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of North Carolina at Chapel Hill</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一致性衡量候选是否相同，verifier检查它是否满足任务；共同错误也可形成多数。群体候选不能自我证明正确，课程升级也不能只以投票一致作为能力已提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>五个Agent都输出同一个错误结果，投票仍一致，但verifier应判失败。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.16043">原论文</a> · <a href="../../../../agent-research/2511.16043-agent0/">实现解读</a> · <a href="#qa-1054f5b756fea842">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent0" data-paper-title="Agent0" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent0 Agent University of North Carolina at Chapel Hill 2025-11-20 任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  零数据多 Agent Agent 交互策略学习：把轨迹反馈变成更新 Agent0 的任务 verifier 能把内部解法或 Gold 直接返回给执行者吗？ 评测和执行输入应只含公开任务条件，隐藏参考留给验证侧；否则课程成绩混入答案泄漏。还需核对生成任务可执行与反馈来源，不能用mini-suite饱和成功率冒充大模型自进化。 示意：任务生成器若把标准动作序列夹在执行prompt里，成功不再证明自主求解。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ae86237122a8fe2d">Agent0 的任务 verifier 能把内部解法或 Gold 直接返回给执行者吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent0">Agent0</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of North Carolina at Chapel Hill</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>评测和执行输入应只含公开任务条件，隐藏参考留给验证侧；否则课程成绩混入答案泄漏。还需核对生成任务可执行与反馈来源，不能用mini-suite饱和成功率冒充大模型自进化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>任务生成器若把标准动作序列夹在执行prompt里，成功不再证明自主求解。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.16043">原论文</a> · <a href="../../../../agent-research/2511.16043-agent0/">实现解读</a> · <a href="#qa-ae86237122a8fe2d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-r1" data-paper-title="Agent-R1" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-R1 Agent University of Science and Technology of China 2025-11-18 把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.9600。  Agentic RL 基础设施 Agent 交互策略学习：把轨迹反馈变成更新 Agent-R1 为什么把 Agent 与环境的每次交互单独记录？ 独立transition把状态、动作及下一observation显式绑定，便于插拔上下文管理和环境接口，并选择token或step级训练信用，而非把整段聊天只当一条文本样本。 示意：一次工具调用及其返回可成为清楚的一条训练记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent-r1-da1f3512" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-62f2c79ffa3c825e">Agent-R1 为什么把 Agent 与环境的每次交互单独记录？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-r1">Agent-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立transition把状态、动作及下一observation显式绑定，便于插拔上下文管理和环境接口，并选择token或step级训练信用，而非把整段聊天只当一条文本样本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次工具调用及其返回可成为清楚的一条训练记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.14460">原论文</a> · <a href="../../../../agent-research/2511.14460-agent-r1/">实现解读</a> · <a href="#qa-62f2c79ffa3c825e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-r1" data-paper-title="Agent-R1" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-R1 Agent University of Science and Technology of China 2025-11-18 把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.9600。  Agentic RL 基础设施 Agent 交互策略学习：把轨迹反馈变成更新 把每次交互记录成独立 transition，为什么有助于切换 token 或 step 级信用？ 状态、动作和下一观察的边界被显式保存，优化器可选择在生成细节或环境步层面归因，而不把所有文本混成一段。可插拔上下文管理处理可见历史，但不能悄悄改变转移语义；工具结果属于环境，不能因统一记录就自动进入策略动作损失。 例如一次查询返回长表格，transition 仍只有一项实际查询动作；训练可按步给信用，或只对查询的生成 token 细分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8a55f93cba02dd89">把每次交互记录成独立 transition，为什么有助于切换 token 或 step 级信用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-r1">Agent-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>状态、动作和下一观察的边界被显式保存，优化器可选择在生成细节或环境步层面归因，而不把所有文本混成一段。可插拔上下文管理处理可见历史，但不能悄悄改变转移语义；工具结果属于环境，不能因统一记录就自动进入策略动作损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次查询返回长表格，transition 仍只有一项实际查询动作；训练可按步给信用，或只对查询的生成 token 细分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.14460">原论文</a> · <a href="../../../../agent-research/2511.14460-agent-r1/">实现解读</a> · <a href="#qa-8a55f93cba02dd89">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-r1" data-paper-title="Agent-R1" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-R1 Agent University of Science and Technology of China 2025-11-18 把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.9600。  Agentic RL 基础设施 Agent 交互策略学习：把轨迹反馈变成更新 token-level 与 step-level 信用只是改一个 loss 名字吗？ 不是。它们对齐的决策单位、价值边界和动作长度处理不同；显式transition使这些选择可审计。若仍混淆工具observation与策略响应，换优化器名字不会修复数据边界。 示意：一个由20个token组成的工具动作，可以对应一个环境step而非20次环境反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-24b67c242f79eb7d">token-level 与 step-level 信用只是改一个 loss 名字吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-r1">Agent-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它们对齐的决策单位、价值边界和动作长度处理不同；显式transition使这些选择可审计。若仍混淆工具observation与策略响应，换优化器名字不会修复数据边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个由20个token组成的工具动作，可以对应一个环境step而非20次环境反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.14460">原论文</a> · <a href="../../../../agent-research/2511.14460-agent-r1/">实现解读</a> · <a href="#qa-24b67c242f79eb7d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-r1" data-paper-title="Agent-R1" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-R1 Agent University of Science and Technology of China 2025-11-18 把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.9600。  Agentic RL 基础设施 Agent 交互策略学习：把轨迹反馈变成更新 Agent-R1 的 transition 日志怎样避免把下一观察误当当前动作可见信息？ 需保留s_t、a_t、o_{t+1}的时间边界，policy生成a_t时不能提前读取o_{t+1}。优势递推也需按episode终止截断；本地机制状态更新不等于真实多卡Agent训练。 示意：工具尚未调用时，策略输入中不能已含它稍后才返回的结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9d3ce2876478b905">Agent-R1 的 transition 日志怎样避免把下一观察误当当前动作可见信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-r1">Agent-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需保留s_t、a_t、o_{t+1}的时间边界，policy生成a_t时不能提前读取o_{t+1}。优势递推也需按episode终止截断；本地机制状态更新不等于真实多卡Agent训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工具尚未调用时，策略输入中不能已含它稍后才返回的结果。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.14460">原论文</a> · <a href="../../../../agent-research/2511.14460-agent-r1/">实现解读</a> · <a href="#qa-9d3ce2876478b905">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mua-rl" data-paper-title="MUA-RL" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="MUA-RL Agent Meituan 2025-08-26 既有 tool-use RL 通常把用户请求视为固定输入，但真实用户会根据 Agent 回答不断修改需求。MUA-RL 将 LLM 模拟用户直接放入 rollout，Agent 在对话中澄清意图并调用真实 MCP/数据库工具；用户消息和工具结果不计入策略 loss，只用最终任务完成奖励鼓励探索。 保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；当前为确定性工具 mini-suite。本地模拟用户按任务上下文确定性揭示约束，工具实际返回 mini-suite 状态，但没有外部 LLM 用户或生产数据库。该实验验证交互与奖励边界，不复刻原模型规模。稳定指标见 omitted-agentic-rl-opd-seed42.json。  多轮用户 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 MUA-RL 为什么把用户也放进动态 rollout，而不只使用开头一条请求？ 真实用户可能澄清或修改意图，策略需根据新需求调整工具行动。方法让模拟用户与Agent交互，再用最终任务完成奖励学习整个过程，而不是把用户输入视作固定不变。 示意：用户在第二轮增加限制，Agent需要据此改变后续工具参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-mua-rl-ac5031c4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6064a2872b370dfe">MUA-RL 为什么把用户也放进动态 rollout，而不只使用开头一条请求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amua-rl">MUA-RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实用户可能澄清或修改意图，策略需根据新需求调整工具行动。方法让模拟用户与Agent交互，再用最终任务完成奖励学习整个过程，而不是把用户输入视作固定不变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户在第二轮增加限制，Agent需要据此改变后续工具参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.18669">原论文</a> · <a href="../../../../agent-research/2508.18669-mua-rl/">实现解读</a> · <a href="#qa-6064a2872b370dfe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mua-rl" data-paper-title="MUA-RL" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="MUA-RL Agent Meituan 2025-08-26 既有 tool-use RL 通常把用户请求视为固定输入，但真实用户会根据 Agent 回答不断修改需求。MUA-RL 将 LLM 模拟用户直接放入 rollout，Agent 在对话中澄清意图并调用真实 MCP/数据库工具；用户消息和工具结果不计入策略 loss，只用最终任务完成奖励鼓励探索。 保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；当前为确定性工具 mini-suite。本地模拟用户按任务上下文确定性揭示约束，工具实际返回 mini-suite 状态，但没有外部 LLM 用户或生产数据库。该实验验证交互与奖励边界，不复刻原模型规模。稳定指标见 omitted-agentic-rl-opd-seed42.json。  多轮用户 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 模拟用户消息为什么和工具结果一样，不应计算为 Agent 的策略 token loss？ 这些文本由环境侧用户策略或工具产生，Agent 无法直接选择它们，拿来监督会混淆动作与条件。把用户放进 rollout 能训练澄清与需求变化下的决策，但最终奖励应评价任务完成，而非奖励模型复述模拟用户；模拟分布也不等于真实用户全部行为。 例如用户中途把日期改到周五，Agent 应据此重排，而不被训练成自己生成“改到周五”这句用户话。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-09abb6a40a03acf3">模拟用户消息为什么和工具结果一样，不应计算为 Agent 的策略 token loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amua-rl">MUA-RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这些文本由环境侧用户策略或工具产生，Agent 无法直接选择它们，拿来监督会混淆动作与条件。把用户放进 rollout 能训练澄清与需求变化下的决策，但最终奖励应评价任务完成，而非奖励模型复述模拟用户；模拟分布也不等于真实用户全部行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户中途把日期改到周五，Agent 应据此重排，而不被训练成自己生成“改到周五”这句用户话。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.18669">原论文</a> · <a href="../../../../agent-research/2508.18669-mua-rl/">实现解读</a> · <a href="#qa-09abb6a40a03acf3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mua-rl" data-paper-title="MUA-RL" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="MUA-RL Agent Meituan 2025-08-26 既有 tool-use RL 通常把用户请求视为固定输入，但真实用户会根据 Agent 回答不断修改需求。MUA-RL 将 LLM 模拟用户直接放入 rollout，Agent 在对话中澄清意图并调用真实 MCP/数据库工具；用户消息和工具结果不计入策略 loss，只用最终任务完成奖励鼓励探索。 保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；当前为确定性工具 mini-suite。本地模拟用户按任务上下文确定性揭示约束，工具实际返回 mini-suite 状态，但没有外部 LLM 用户或生产数据库。该实验验证交互与奖励边界，不复刻原模型规模。稳定指标见 omitted-agentic-rl-opd-seed42.json。  多轮用户 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 动态用户模拟与把工具结果当唯一环境反馈，有什么任务差异？ 用户消息会改变或澄清目标，工具结果主要反映执行后状态。两者都是环境输入，但作用不同；只重复静态工具轨迹无法覆盖需求持续变化的交互策略。 示意：工具说操作成功，用户却进一步说明想要另一种结果，Agent仍需继续理解需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b0003b8f82cef21c">动态用户模拟与把工具结果当唯一环境反馈，有什么任务差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amua-rl">MUA-RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户消息会改变或澄清目标，工具结果主要反映执行后状态。两者都是环境输入，但作用不同；只重复静态工具轨迹无法覆盖需求持续变化的交互策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工具说操作成功，用户却进一步说明想要另一种结果，Agent仍需继续理解需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.18669">原论文</a> · <a href="../../../../agent-research/2508.18669-mua-rl/">实现解读</a> · <a href="#qa-b0003b8f82cef21c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mua-rl" data-paper-title="MUA-RL" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="MUA-RL Agent Meituan 2025-08-26 既有 tool-use RL 通常把用户请求视为固定输入，但真实用户会根据 Agent 回答不断修改需求。MUA-RL 将 LLM 模拟用户直接放入 rollout，Agent 在对话中澄清意图并调用真实 MCP/数据库工具；用户消息和工具结果不计入策略 loss，只用最终任务完成奖励鼓励探索。 保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；当前为确定性工具 mini-suite。本地模拟用户按任务上下文确定性揭示约束，工具实际返回 mini-suite 状态，但没有外部 LLM 用户或生产数据库。该实验验证交互与奖励边界，不复刻原模型规模。稳定指标见 omitted-agentic-rl-opd-seed42.json。  多轮用户 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 MUA-RL 的模拟用户能直接暴露场景内部的完整隐藏目标给 Agent 吗？ 应按交互协议只逐步提供用户可说出的信息，不能把模拟器私有参考或完整解法直接交给策略。loss还只覆盖Agent响应；本地确定性用户和mini工具不是外部LLM或生产数据库。 示意：模拟用户只在被澄清后补充限制，而不是开头附上全部标准工具调用序列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bef8d360a271edc5">MUA-RL 的模拟用户能直接暴露场景内部的完整隐藏目标给 Agent 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amua-rl">MUA-RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应按交互协议只逐步提供用户可说出的信息，不能把模拟器私有参考或完整解法直接交给策略。loss还只覆盖Agent响应；本地确定性用户和mini工具不是外部LLM或生产数据库。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模拟用户只在被澄清后补充限制，而不是开头附上全部标准工具调用序列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.18669">原论文</a> · <a href="../../../../agent-research/2508.18669-mua-rl/">实现解读</a> · <a href="#qa-bef8d360a271edc5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-lightning" data-paper-title="Agent Lightning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent Lightning Agent Microsoft Research 2025-08-05 传统 Agent RL 常把所有上下文拼成单序列并与框架强耦合。Agent Lightning 将执行记录成统一 MDP transition，以 credit assignment 拆解轨迹，并采用训练/执行分离架构。 解耦 Agent 执行与 RL 训练，并将长交互轨迹拆成可归因的训练 transition。实现了执行/训练解耦、transition、环境 reward、credit update 与跨 episode 复用；本地更新的是受控 patch policy，不是对 LLM 参数执行 LightningRL。代码 Agent 的命令、编辑与测试形成 transition；测试退出码是真实 reward，失败时把 credit 归给 patch，并把正确修复按 bug family 写入可复用策略记忆。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 Agent Lightning 为什么先把执行事件转换成统一 transition？ 不同Agent runtime的日志形式不同，统一MDP transition与credit拆解可让训练侧理解状态、动作和回报，从而把执行框架与策略训练解耦，而不只是换日志存储位置。 示意：一次代码编辑后测试失败，应能绑定到该次patch动作及其状态，而非只留下孤立文本日志。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent-lightning-78a73390" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dc5ea5ae4caba782">Agent Lightning 为什么先把执行事件转换成统一 transition？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-lightning">Agent Lightning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同Agent runtime的日志形式不同，统一MDP transition与credit拆解可让训练侧理解状态、动作和回报，从而把执行框架与策略训练解耦，而不只是换日志存储位置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次代码编辑后测试失败，应能绑定到该次patch动作及其状态，而非只留下孤立文本日志。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.03680">原论文</a> · <a href="../../../../agent-research/2508.03680-agent-lightning/">实现解读</a> · <a href="#qa-dc5ea5ae4caba782">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-lightning" data-paper-title="Agent Lightning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent Lightning Agent Microsoft Research 2025-08-05 传统 Agent RL 常把所有上下文拼成单序列并与框架强耦合。Agent Lightning 将执行记录成统一 MDP transition，以 credit assignment 拆解轨迹，并采用训练/执行分离架构。 解耦 Agent 执行与 RL 训练，并将长交互轨迹拆成可归因的训练 transition。实现了执行/训练解耦、transition、环境 reward、credit update 与跨 episode 复用；本地更新的是受控 patch policy，不是对 LLM 参数执行 LightningRL。代码 Agent 的命令、编辑与测试形成 transition；测试退出码是真实 reward，失败时把 credit 归给 patch，并把正确修复按 bug family 写入可复用策略记忆。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 训练与执行分离为什么不仅是把日志写到另一台机器？ 统一 transition 合同把框架行为转成可归因的 MDP 数据，训练侧据此计算回报与优势，执行侧可继续使用原有工具编排。若日志缺状态动作边界或混入环境 token，物理分离也无法得到正确策略更新；架构解耦不自动证明任何具体 Agent 已提升。 例如同一工具框架输出查询动作和结果，训练器只读取规范转移即可更新；不能把未经切分的整份聊天日志直接当动作序列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9eae2b8c915b5c27">训练与执行分离为什么不仅是把日志写到另一台机器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-lightning">Agent Lightning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一 transition 合同把框架行为转成可归因的 MDP 数据，训练侧据此计算回报与优势，执行侧可继续使用原有工具编排。若日志缺状态动作边界或混入环境 token，物理分离也无法得到正确策略更新；架构解耦不自动证明任何具体 Agent 已提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一工具框架输出查询动作和结果，训练器只读取规范转移即可更新；不能把未经切分的整份聊天日志直接当动作序列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.03680">原论文</a> · <a href="../../../../agent-research/2508.03680-agent-lightning/">实现解读</a> · <a href="#qa-9eae2b8c915b5c27">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-lightning" data-paper-title="Agent Lightning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent Lightning Agent Microsoft Research 2025-08-05 传统 Agent RL 常把所有上下文拼成单序列并与框架强耦合。Agent Lightning 将执行记录成统一 MDP transition，以 credit assignment 拆解轨迹，并采用训练/执行分离架构。 解耦 Agent 执行与 RL 训练，并将长交互轨迹拆成可归因的训练 transition。实现了执行/训练解耦、transition、环境 reward、credit update 与跨 episode 复用；本地更新的是受控 patch policy，不是对 LLM 参数执行 LightningRL。代码 Agent 的命令、编辑与测试形成 transition；测试退出码是真实 reward，失败时把 credit 归给 patch，并把正确修复按 bug family 写入可复用策略记忆。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 执行/训练解耦与仅异步收集日志，有何能力差别？ 解耦还需把轨迹映射成可训练transition、分配credit并把更新后的策略交回执行；异步日志只解决记录与传输。没有真实消费更新的执行路径，就不能宣称闭环已接通。 示意：日志不断增加，但下一轮始终使用旧策略，不构成训练影响执行的循环。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d90a4c4e3c50b51e">执行/训练解耦与仅异步收集日志，有何能力差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-lightning">Agent Lightning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>解耦还需把轨迹映射成可训练transition、分配credit并把更新后的策略交回执行；异步日志只解决记录与传输。没有真实消费更新的执行路径，就不能宣称闭环已接通。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>日志不断增加，但下一轮始终使用旧策略，不构成训练影响执行的循环。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.03680">原论文</a> · <a href="../../../../agent-research/2508.03680-agent-lightning/">实现解读</a> · <a href="#qa-d90a4c4e3c50b51e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-lightning" data-paper-title="Agent Lightning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent Lightning Agent Microsoft Research 2025-08-05 传统 Agent RL 常把所有上下文拼成单序列并与框架强耦合。Agent Lightning 将执行记录成统一 MDP transition，以 credit assignment 拆解轨迹，并采用训练/执行分离架构。 解耦 Agent 执行与 RL 训练，并将长交互轨迹拆成可归因的训练 transition。实现了执行/训练解耦、transition、环境 reward、credit update 与跨 episode 复用；本地更新的是受控 patch policy，不是对 LLM 参数执行 LightningRL。代码 Agent 的命令、编辑与测试形成 transition；测试退出码是真实 reward，失败时把 credit 归给 patch，并把正确修复按 bug family 写入可复用策略记忆。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 本地 Agent Lightning 的真实测试 reward，更新的是哪种 policy？ 文档代码sandbox用测试退出码给patch分配credit，更新受控patch policy并按bug family复用；不是对LLM参数执行LightningRL。应分别检查命令/编辑/测试事件、实际reward及记忆消费。 示意：测试失败能改变后续patch选择，却不能据此声称大语言模型权重已完成RL训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-677f718873b61e65">本地 Agent Lightning 的真实测试 reward，更新的是哪种 policy？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-lightning">Agent Lightning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档代码sandbox用测试退出码给patch分配credit，更新受控patch policy并按bug family复用；不是对LLM参数执行LightningRL。应分别检查命令/编辑/测试事件、实际reward及记忆消费。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>测试失败能改变后续patch选择，却不能据此声称大语言模型权重已完成RL训练。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.03680">原论文</a> · <a href="../../../../agent-research/2508.03680-agent-lightning/">实现解读</a> · <a href="#qa-677f718873b61e65">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webagent-r1" data-paper-title="WebAgent-R1" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="WebAgent-R1 Agent University of Virginia 2025-05-22 网页交互会不断累积 HTML 和历史动作，单轮 GRPO 无法处理状态变化。WebAgent-R1 动态保留近期和任务相关上下文，并行采集完整多轮轨迹，再用 M-GRPO 根据最终成功奖励执行组内相对更新；论文同时强调行为克隆 warm-up 和长 CoT 初始化。 保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；当前使用确定性工具 mini-suite，不冒充 WebArena-Lite。本地环境返回确定性文本工具观测，没有浏览器 DOM、网页副作用或 Qwen/Llama 参数更新。因此只验证多轮 rollout、压缩和组内奖励路径。稳定指标见 omitted-agentic-rl-opd-seed42.json。  网页 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 WebAgent-R1 为什么把完整多轮网页过程作为训练轨迹？ 网页状态、HTML和历史动作随交互变化，最终成功依赖多次决策。方法动态管理近期与任务相关上下文，采集完整轨迹并以组相对结果更新，而非重复优化单轮答案。 示意：点击后页面换了，下一动作需依据新状态，不能继续假设初始页面不变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-webagent-r1-938cd977" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e697ddfc76e544bd">WebAgent-R1 为什么把完整多轮网页过程作为训练轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awebagent-r1">WebAgent-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>网页状态、HTML和历史动作随交互变化，最终成功依赖多次决策。方法动态管理近期与任务相关上下文，采集完整轨迹并以组相对结果更新，而非重复优化单轮答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击后页面换了，下一动作需依据新状态，不能继续假设初始页面不变。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.16421">原论文</a> · <a href="../../../../agent-research/2505.16421-webagent-r1/">实现解读</a> · <a href="#qa-e697ddfc76e544bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webagent-r1" data-paper-title="WebAgent-R1" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="WebAgent-R1 Agent University of Virginia 2025-05-22 网页交互会不断累积 HTML 和历史动作，单轮 GRPO 无法处理状态变化。WebAgent-R1 动态保留近期和任务相关上下文，并行采集完整多轮轨迹，再用 M-GRPO 根据最终成功奖励执行组内相对更新；论文同时强调行为克隆 warm-up 和长 CoT 初始化。 保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；当前使用确定性工具 mini-suite，不冒充 WebArena-Lite。本地环境返回确定性文本工具观测，没有浏览器 DOM、网页副作用或 Qwen/Llama 参数更新。因此只验证多轮 rollout、压缩和组内奖励路径。稳定指标见 omitted-agentic-rl-opd-seed42.json。  网页 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么多轮网页 GRPO 需要动态上下文，而不只是把单轮回答重复训练几次？ 网页状态会随点击、输入和跳转改变，后续动作必须看到真实最新页面及必要历史。完整多轮 rollout 才能把终局成功回报连到这些生成动作，动态保留控制 HTML 膨胀；行为克隆与初始化也影响探索，不能把一个组内优势公式当成完整网页交互训练。 例如点击登录后页面结构变化，下一步必须读取新表单；只反复训练最初截图上的答案，无法学会真实状态转换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-be6d569f718d3a13">为什么多轮网页 GRPO 需要动态上下文，而不只是把单轮回答重复训练几次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awebagent-r1">WebAgent-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>网页状态会随点击、输入和跳转改变，后续动作必须看到真实最新页面及必要历史。完整多轮 rollout 才能把终局成功回报连到这些生成动作，动态保留控制 HTML 膨胀；行为克隆与初始化也影响探索，不能把一个组内优势公式当成完整网页交互训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如点击登录后页面结构变化，下一步必须读取新表单；只反复训练最初截图上的答案，无法学会真实状态转换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.16421">原论文</a> · <a href="../../../../agent-research/2505.16421-webagent-r1/">实现解读</a> · <a href="#qa-be6d569f718d3a13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webagent-r1" data-paper-title="WebAgent-R1" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="WebAgent-R1 Agent University of Virginia 2025-05-22 网页交互会不断累积 HTML 和历史动作，单轮 GRPO 无法处理状态变化。WebAgent-R1 动态保留近期和任务相关上下文，并行采集完整多轮轨迹，再用 M-GRPO 根据最终成功奖励执行组内相对更新；论文同时强调行为克隆 warm-up 和长 CoT 初始化。 保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；当前使用确定性工具 mini-suite，不冒充 WebArena-Lite。本地环境返回确定性文本工具观测，没有浏览器 DOM、网页副作用或 Qwen/Llama 参数更新。因此只验证多轮 rollout、压缩和组内奖励路径。稳定指标见 omitted-agentic-rl-opd-seed42.json。  网页 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 行为克隆 warm-up 与随后 M-GRPO，分别解决什么训练问题？ warm-up提供基础交互行为与初始化，M-GRPO再根据完整任务成功的组内相对反馈优化策略。两阶段监督不同，不能仅注册一个GRPO名字就省略论文强调的行为与长CoT起点。 示意：先学会合法点击和输入，再利用任务结果改进长程选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6a3db74d6fed501a">行为克隆 warm-up 与随后 M-GRPO，分别解决什么训练问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awebagent-r1">WebAgent-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>warm-up提供基础交互行为与初始化，M-GRPO再根据完整任务成功的组内相对反馈优化策略。两阶段监督不同，不能仅注册一个GRPO名字就省略论文强调的行为与长CoT起点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先学会合法点击和输入，再利用任务结果改进长程选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.16421">原论文</a> · <a href="../../../../agent-research/2505.16421-webagent-r1/">实现解读</a> · <a href="#qa-6a3db74d6fed501a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webagent-r1" data-paper-title="WebAgent-R1" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="WebAgent-R1 Agent University of Virginia 2025-05-22 网页交互会不断累积 HTML 和历史动作，单轮 GRPO 无法处理状态变化。WebAgent-R1 动态保留近期和任务相关上下文，并行采集完整多轮轨迹，再用 M-GRPO 根据最终成功奖励执行组内相对更新；论文同时强调行为克隆 warm-up 和长 CoT 初始化。 保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；当前使用确定性工具 mini-suite，不冒充 WebArena-Lite。本地环境返回确定性文本工具观测，没有浏览器 DOM、网页副作用或 Qwen/Llama 参数更新。因此只验证多轮 rollout、压缩和组内奖励路径。稳定指标见 omitted-agentic-rl-opd-seed42.json。  网页 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 网页状态压缩之后，怎样避免仍把旧页面 DOM 当成当前可操作状态？ 应将每步动作与当时observation及压缩上下文绑定，动态状态不可由固定初始页替代。当前mini-suite只有确定性文本工具观测，没有真实DOM副作用或Qwen/Llama参数更新。 示意：上一页按钮的标识在跳转后可能失效，不能只因历史中出现过就继续点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-856a46c9abd64eb7">网页状态压缩之后，怎样避免仍把旧页面 DOM 当成当前可操作状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awebagent-r1">WebAgent-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应将每步动作与当时observation及压缩上下文绑定，动态状态不可由固定初始页替代。当前mini-suite只有确定性文本工具观测，没有真实DOM副作用或Qwen/Llama参数更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>上一页按钮的标识在跳转后可能失效，不能只因历史中出现过就继续点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.16421">原论文</a> · <a href="../../../../agent-research/2505.16421-webagent-r1/">实现解读</a> · <a href="#qa-856a46c9abd64eb7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gigpo" data-paper-title="GiGPO" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GiGPO Agent Nanyang Technological University 2025-05-16 多轮 Agent 的最终奖励稀疏，整条轨迹的 group relative advantage 无法判断哪个 environment step 做对了。GiGPO 先在完整轨迹组上计算 macro advantage，再按跨轨迹重复到达的 anchor state 建立 step group，计算 micro relative advantage。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。确定性任务没有跨轨迹真实环境 state 合流，使用共享计划步骤作为可审计 anchor-state 代理。在 PlanBench mini 中显式生成完整轨迹组与 step group，分别统计组间和组内优势、trajectory rollout 与 turn credit。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 GiGPO 为什么既要 macro trajectory advantage，又要 micro step advantage？ 终局结果反映整条轨迹，却不容易定位哪个环境step贡献更大。方法先比较轨迹组，再在重复到达的anchor state动作组内比较，把整体与局部信用相加。 示意：两条轨迹最终都失败，但在同一中间状态的一次动作仍可能明显更有帮助。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-gigpo-7fac2585" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-de70025cd20df8d7">GiGPO 为什么既要 macro trajectory advantage，又要 micro step advantage？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agigpo">GiGPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局结果反映整条轨迹，却不容易定位哪个环境step贡献更大。方法先比较轨迹组，再在重复到达的anchor state动作组内比较，把整体与局部信用相加。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条轨迹最终都失败，但在同一中间状态的一次动作仍可能明显更有帮助。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.10978">原论文</a> · <a href="../../../../agent-research/2505.10978-gigpo/">实现解读</a> · <a href="#qa-de70025cd20df8d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gigpo" data-paper-title="GiGPO" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GiGPO Agent Nanyang Technological University 2025-05-16 多轮 Agent 的最终奖励稀疏，整条轨迹的 group relative advantage 无法判断哪个 environment step 做对了。GiGPO 先在完整轨迹组上计算 macro advantage，再按跨轨迹重复到达的 anchor state 建立 step group，计算 micro relative advantage。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。确定性任务没有跨轨迹真实环境 state 合流，使用共享计划步骤作为可审计 anchor-state 代理。在 PlanBench mini 中显式生成完整轨迹组与 step group，分别统计组间和组内优势、trajectory rollout 与 turn credit。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 为什么 micro advantage 要在重复到达同一 anchor state 的动作间比较？ 不同状态的可选动作与剩余难度不同，直接比较回报会混入起点差异。共享锚状态提供更相近的局部条件，micro 信号补充整条轨迹 macro 优势；同状态后仍有随机续跑，局部差异不是无噪声因果值，也不能取代最终成功约束。 例如两条轨迹都站在锁门前，一条找钥匙、一条重复推门，才适合比较该处动作；不能拿已到终点的状态当同组对照。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e6181f3487b83939">为什么 micro advantage 要在重复到达同一 anchor state 的动作间比较？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agigpo">GiGPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同状态的可选动作与剩余难度不同，直接比较回报会混入起点差异。共享锚状态提供更相近的局部条件，micro 信号补充整条轨迹 macro 优势；同状态后仍有随机续跑，局部差异不是无噪声因果值，也不能取代最终成功约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条轨迹都站在锁门前，一条找钥匙、一条重复推门，才适合比较该处动作；不能拿已到终点的状态当同组对照。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.10978">原论文</a> · <a href="../../../../agent-research/2505.10978-gigpo/">实现解读</a> · <a href="#qa-e6181f3487b83939">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gigpo" data-paper-title="GiGPO" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GiGPO Agent Nanyang Technological University 2025-05-16 多轮 Agent 的最终奖励稀疏，整条轨迹的 group relative advantage 无法判断哪个 environment step 做对了。GiGPO 先在完整轨迹组上计算 macro advantage，再按跨轨迹重复到达的 anchor state 建立 step group，计算 micro relative advantage。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。确定性任务没有跨轨迹真实环境 state 合流，使用共享计划步骤作为可审计 anchor-state 代理。在 PlanBench mini 中显式生成完整轨迹组与 step group，分别统计组间和组内优势、trajectory rollout 与 turn credit。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 按相同 anchor state 建 micro group，与把所有 step 混在一起排名有什么不同？ 同状态比较更有可比性，混合不同状态会把任务难度和行动后果混在一起。共享计划步骤只能作为本地代理，不能自动等价于真实环境中状态完全合流。 示意：一个容易状态的高回报动作，不应直接拿来当困难状态动作的相同基线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-951a8f0b5718b90f">按相同 anchor state 建 micro group，与把所有 step 混在一起排名有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agigpo">GiGPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同状态比较更有可比性，混合不同状态会把任务难度和行动后果混在一起。共享计划步骤只能作为本地代理，不能自动等价于真实环境中状态完全合流。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个容易状态的高回报动作，不应直接拿来当困难状态动作的相同基线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.10978">原论文</a> · <a href="../../../../agent-research/2505.10978-gigpo/">实现解读</a> · <a href="#qa-951a8f0b5718b90f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gigpo" data-paper-title="GiGPO" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GiGPO Agent Nanyang Technological University 2025-05-16 多轮 Agent 的最终奖励稀疏，整条轨迹的 group relative advantage 无法判断哪个 environment step 做对了。GiGPO 先在完整轨迹组上计算 macro advantage，再按跨轨迹重复到达的 anchor state 建立 step group，计算 micro relative advantage。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。确定性任务没有跨轨迹真实环境 state 合流，使用共享计划步骤作为可审计 anchor-state 代理。在 PlanBench mini 中显式生成完整轨迹组与 step group，分别统计组间和组内优势、trajectory rollout 与 turn credit。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 GiGPO 记录 micro advantage 时，为什么要保存 anchor 身份与对应动作？ 公式均值取同一G(s_t)，若anchor键错误或混入其它状态，局部基线就变了。应同时保留macro与micro日志、实际组成员和状态代理边界，而非只报最终合成优势。 示意：两个界面标题相同但底层任务状态不同，不能仅凭标题把它们合成一个anchor。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-57d3ee83ffa537e5">GiGPO 记录 micro advantage 时，为什么要保存 anchor 身份与对应动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agigpo">GiGPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式均值取同一G(s_t)，若anchor键错误或混入其它状态，局部基线就变了。应同时保留macro与micro日志、实际组成员和状态代理边界，而非只报最终合成优势。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个界面标题相同但底层任务状态不同，不能仅凭标题把它们合成一个anchor。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.10978">原论文</a> · <a href="../../../../agent-research/2505.10978-gigpo/">实现解读</a> · <a href="#qa-57d3ee83ffa537e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ragen" data-paper-title="RAGEN" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RAGEN Agent Northwestern 2025-04-24 单轮数学 RL 的优化单位是一次回答，而 Agent 要在随机环境中跨多轮决策。RAGEN 提出 StarPO，把 state、thinking、action 和 reward 组织成完整轨迹。论文还观察到 Echo Trap：reward 方差突然塌缩并伴随梯度尖峰。StarPO-S 通过轨迹过滤、critic baseline、梯度稳定和解耦 clipping 抑制这种自我强化的重复模式。 保真度：本地实现 StarPO-S 的 trajectory rollout、退化轨迹过滤、critic baseline、reasoning-aware reward、Echo Trap 探针和解耦 clipping 诊断。本地策略在确定性候选轨迹上选择计划，真实执行但不更新 LLM 参数；Echo Trap 是固定频率的可观测稳定性探针，不冒充论文训练曲线。未运行 WebShop 或原始游戏环境。稳定指标见 classic-agentic-rl-opd-seed42.json。  多轮 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 RAGEN 的 Echo Trap 为什么值得单独监测？ 多轮随机环境训练可能进入自我强化的重复模式，表现为reward方差塌缩与梯度尖峰。StarPO-S通过轨迹过滤、critic baseline及梯度/clipping稳定控制，而不是把低方差都当成已学会。 示意：策略总走同一条失败轨迹，奖励非常一致也不代表能力稳定提升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-ragen-2a3a9785" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ef11042a5e1ad9ea">RAGEN 的 Echo Trap 为什么值得单独监测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aragen">RAGEN</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多轮随机环境训练可能进入自我强化的重复模式，表现为reward方差塌缩与梯度尖峰。StarPO-S通过轨迹过滤、critic baseline及梯度/clipping稳定控制，而不是把低方差都当成已学会。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>策略总走同一条失败轨迹，奖励非常一致也不代表能力稳定提升。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.20073">原论文</a> · <a href="../../../../agent-research/2504.20073-ragen/">实现解读</a> · <a href="#qa-ef11042a5e1ad9ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ragen" data-paper-title="RAGEN" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RAGEN Agent Northwestern 2025-04-24 单轮数学 RL 的优化单位是一次回答，而 Agent 要在随机环境中跨多轮决策。RAGEN 提出 StarPO，把 state、thinking、action 和 reward 组织成完整轨迹。论文还观察到 Echo Trap：reward 方差突然塌缩并伴随梯度尖峰。StarPO-S 通过轨迹过滤、critic baseline、梯度稳定和解耦 clipping 抑制这种自我强化的重复模式。 保真度：本地实现 StarPO-S 的 trajectory rollout、退化轨迹过滤、critic baseline、reasoning-aware reward、Echo Trap 探针和解耦 clipping 诊断。本地策略在确定性候选轨迹上选择计划，真实执行但不更新 LLM 参数；Echo Trap 是固定频率的可观测稳定性探针，不冒充论文训练曲线。未运行 WebShop 或原始游戏环境。稳定指标见 classic-agentic-rl-opd-seed42.json。  多轮 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 reward 方差塌缩为什么不一定说明策略已经稳定学会任务？ 策略可能陷入反复输出同类失败或僵化行为，回报缺变化伴随梯度尖峰就是 Echo Trap 的危险征兆。轨迹过滤、critic 基线和解耦 clipping 分别控制数据、估值与更新稳定性；稳定训练还需看真实任务表现，不能把低方差自动写成收敛成功。 例如所有 rollout 都重复同一无效命令，奖励全零且方差为零，数值看似一致，实际是探索崩溃而非能力已成熟。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-50b92779eb94d4cb">reward 方差塌缩为什么不一定说明策略已经稳定学会任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aragen">RAGEN</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略可能陷入反复输出同类失败或僵化行为，回报缺变化伴随梯度尖峰就是 Echo Trap 的危险征兆。轨迹过滤、critic 基线和解耦 clipping 分别控制数据、估值与更新稳定性；稳定训练还需看真实任务表现，不能把低方差自动写成收敛成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如所有 rollout 都重复同一无效命令，奖励全零且方差为零，数值看似一致，实际是探索崩溃而非能力已成熟。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.20073">原论文</a> · <a href="../../../../agent-research/2504.20073-ragen/">实现解读</a> · <a href="#qa-50b92779eb94d4cb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ragen" data-paper-title="RAGEN" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RAGEN Agent Northwestern 2025-04-24 单轮数学 RL 的优化单位是一次回答，而 Agent 要在随机环境中跨多轮决策。RAGEN 提出 StarPO，把 state、thinking、action 和 reward 组织成完整轨迹。论文还观察到 Echo Trap：reward 方差突然塌缩并伴随梯度尖峰。StarPO-S 通过轨迹过滤、critic baseline、梯度稳定和解耦 clipping 抑制这种自我强化的重复模式。 保真度：本地实现 StarPO-S 的 trajectory rollout、退化轨迹过滤、critic baseline、reasoning-aware reward、Echo Trap 探针和解耦 clipping 诊断。本地策略在确定性候选轨迹上选择计划，真实执行但不更新 LLM 参数；Echo Trap 是固定频率的可观测稳定性探针，不冒充论文训练曲线。未运行 WebShop 或原始游戏环境。稳定指标见 classic-agentic-rl-opd-seed42.json。  多轮 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 StarPO-S 的轨迹质量过滤，与只在 PPO loss 内裁剪 ratio 有何区别？ 过滤决定哪些轨迹进入目标，ratio clipping约束已入选样本的策略漂移；critic与梯度稳定又是其它环节。只保留一个clip操作不能替代完整稳定化链路。 示意：重复低信息轨迹即使ratio被裁剪，仍可能持续占据大量训练样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3a4fb5b58a42b90f">StarPO-S 的轨迹质量过滤，与只在 PPO loss 内裁剪 ratio 有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aragen">RAGEN</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>过滤决定哪些轨迹进入目标，ratio clipping约束已入选样本的策略漂移；critic与梯度稳定又是其它环节。只保留一个clip操作不能替代完整稳定化链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>重复低信息轨迹即使ratio被裁剪，仍可能持续占据大量训练样本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.20073">原论文</a> · <a href="../../../../agent-research/2504.20073-ragen/">实现解读</a> · <a href="#qa-3a4fb5b58a42b90f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ragen" data-paper-title="RAGEN" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RAGEN Agent Northwestern 2025-04-24 单轮数学 RL 的优化单位是一次回答，而 Agent 要在随机环境中跨多轮决策。RAGEN 提出 StarPO，把 state、thinking、action 和 reward 组织成完整轨迹。论文还观察到 Echo Trap：reward 方差突然塌缩并伴随梯度尖峰。StarPO-S 通过轨迹过滤、critic baseline、梯度稳定和解耦 clipping 抑制这种自我强化的重复模式。 保真度：本地实现 StarPO-S 的 trajectory rollout、退化轨迹过滤、critic baseline、reasoning-aware reward、Echo Trap 探针和解耦 clipping 诊断。本地策略在确定性候选轨迹上选择计划，真实执行但不更新 LLM 参数；Echo Trap 是固定频率的可观测稳定性探针，不冒充论文训练曲线。未运行 WebShop 或原始游戏环境。稳定指标见 classic-agentic-rl-opd-seed42.json。  多轮 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 本地固定频率 Echo Trap probe，能当作测得论文训练坍缩曲线吗？ 不能。文档probe是可观测稳定性路径，策略只在确定性候选中选择且未更新LLM参数。应把probe触发、真实梯度行为和大规模训练曲线分开，不用计数代替模型坍缩证据。 示意：每隔若干轮主动检查一次，不代表这些轮次实际发生了论文中的Echo Trap。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b358c5305dd0b789">本地固定频率 Echo Trap probe，能当作测得论文训练坍缩曲线吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aragen">RAGEN</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。文档probe是可观测稳定性路径，策略只在确定性候选中选择且未更新LLM参数。应把probe触发、真实梯度行为和大规模训练曲线分开，不用计数代替模型坍缩证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>每隔若干轮主动检查一次，不代表这些轮次实际发生了论文中的Echo Trap。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.20073">原论文</a> · <a href="../../../../agent-research/2504.20073-ragen/">实现解读</a> · <a href="#qa-b358c5305dd0b789">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deepresearcher" data-paper-title="DeepResearcher" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="DeepResearcher Agent HKU 2025-04-04 把 search、browse、证据收集和带引用回答作为一条轨迹，用答案与引用联合奖励训练研究策略。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.5000；方法特有操作有非零 telemetry。  深度研究 RL Agent 交互策略学习：把轨迹反馈变成更新 DeepResearcher 为什么把搜索、浏览、证据与回答视作同一条研究轨迹？ 研究答案依赖前面如何找证据与使用证据，分开只看最终文字难分配信用。联合答案/引用奖励和查询成本，使策略在完整搜索过程里权衡质量与开销。 示意：有用的一次浏览可让后续回答更可核验，而不是只评价最后一句是否流畅。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-deepresearcher-9b53178e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-88cf40121cb186e1">DeepResearcher 为什么把搜索、浏览、证据与回答视作同一条研究轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adeepresearcher">DeepResearcher</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · HKU</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究答案依赖前面如何找证据与使用证据，分开只看最终文字难分配信用。联合答案/引用奖励和查询成本，使策略在完整搜索过程里权衡质量与开销。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>有用的一次浏览可让后续回答更可核验，而不是只评价最后一句是否流畅。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.03160">原论文</a> · <a href="../../../../agent-research/2504.03160-deepresearcher/">实现解读</a> · <a href="#qa-88cf40121cb186e1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deepresearcher" data-paper-title="DeepResearcher" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="DeepResearcher Agent HKU 2025-04-04 把 search、browse、证据收集和带引用回答作为一条轨迹，用答案与引用联合奖励训练研究策略。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.5000；方法特有操作有非零 telemetry。  深度研究 RL Agent 交互策略学习：把轨迹反馈变成更新 答案奖励之外加 citation reward，为什么仍不能只按引用数量给分？ 引用的作用是把结论连到真实证据，数量多可能只是重复或无关链接。搜索、浏览与回答组成整条策略轨迹，联合目标应约束证据支持与正确答案，并惩罚无用查询；最终主张与来源的对应关系必须核对，调用一次浏览也不等于认真使用了证据。 例如回答含十个无关来源不应胜过两条直接支持结论的引用，否则策略会学习堆链接而不是完成研究取证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-aff7e18e331cc491">答案奖励之外加 citation reward，为什么仍不能只按引用数量给分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adeepresearcher">DeepResearcher</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · HKU</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>引用的作用是把结论连到真实证据，数量多可能只是重复或无关链接。搜索、浏览与回答组成整条策略轨迹，联合目标应约束证据支持与正确答案，并惩罚无用查询；最终主张与来源的对应关系必须核对，调用一次浏览也不等于认真使用了证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如回答含十个无关来源不应胜过两条直接支持结论的引用，否则策略会学习堆链接而不是完成研究取证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.03160">原论文</a> · <a href="../../../../agent-research/2504.03160-deepresearcher/">实现解读</a> · <a href="#qa-aff7e18e331cc491">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deepresearcher" data-paper-title="DeepResearcher" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="DeepResearcher Agent HKU 2025-04-04 把 search、browse、证据收集和带引用回答作为一条轨迹，用答案与引用联合奖励训练研究策略。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.5000；方法特有操作有非零 telemetry。  深度研究 RL Agent 交互策略学习：把轨迹反馈变成更新 引用质量奖励与查询次数惩罚，为什么不是同一个效率目标？ 引用奖励关注证据支撑，查询惩罚控制调用成本；少查不保证证据可靠，多引用也不保证查询有效。三项权重决定取舍，不能用更短轨迹单独证明研究质量更好。 示意：一次错误搜索后迅速作答可能很省调用，却没有可靠证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4a779c50af1afc7e">引用质量奖励与查询次数惩罚，为什么不是同一个效率目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adeepresearcher">DeepResearcher</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · HKU</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>引用奖励关注证据支撑，查询惩罚控制调用成本；少查不保证证据可靠，多引用也不保证查询有效。三项权重决定取舍，不能用更短轨迹单独证明研究质量更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次错误搜索后迅速作答可能很省调用，却没有可靠证据。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.03160">原论文</a> · <a href="../../../../agent-research/2504.03160-deepresearcher/">实现解读</a> · <a href="#qa-4a779c50af1afc7e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deepresearcher" data-paper-title="DeepResearcher" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="DeepResearcher Agent HKU 2025-04-04 把 search、browse、证据收集和带引用回答作为一条轨迹，用答案与引用联合奖励训练研究策略。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.5000；方法特有操作有非零 telemetry。  深度研究 RL Agent 交互策略学习：把轨迹反馈变成更新 DeepResearcher 的 citation reward 应怎样与实际检索证据对齐？ 需核对引用指向真实可获得材料并支持对应陈述，而不是只数链接；N_query也应统计实际搜索调用。当前mini-suite没有真实网页与完整大模型RL，不能把fixture引用当外部证据。 示意：答案里列出一个从未检索过且不支持结论的标题，不应仅因格式像引用就得分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fc41b0278af88bb1">DeepResearcher 的 citation reward 应怎样与实际检索证据对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adeepresearcher">DeepResearcher</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · HKU</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需核对引用指向真实可获得材料并支持对应陈述，而不是只数链接；N_query也应统计实际搜索调用。当前mini-suite没有真实网页与完整大模型RL，不能把fixture引用当外部证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>答案里列出一个从未检索过且不支持结论的标题，不应仅因格式像引用就得分。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.03160">原论文</a> · <a href="../../../../agent-research/2504.03160-deepresearcher/">实现解读</a> · <a href="#qa-fc41b0278af88bb1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:search-r1" data-paper-title="Search-R1" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Search-R1 Agent University of Illinois Urbana-Champaign 2025-03-12 普通 RAG 一次检索后再回答，无法让策略根据中间证据继续调整查询。Search-R1 把搜索引擎视为环境：模型可在 reasoning 中多次输出搜索动作，环境返回文档后继续推理。训练只对模型生成 token 计算 PPO/GRPO loss，检索结果 token 必须 mask，最终答案用简单 outcome reward 评分。 保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；使用确定性 ScaleMCP mini，不调用论文的 E5 索引或训练 Qwen。mini-suite 的检索结果是确定性的当前任务上下文，适合验证交错状态机和 loss mask；没有真实网页索引、Qwen 参数更新或七个 QA benchmark，因此成功率不能与论文 EM 比较。稳定指标见 classic-agentic-rl-opd-seed42.json。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 Search-R1 相对一次性 RAG，为什么需要在推理中反复决定是否搜索？ 中间证据可能暴露新问题或修正当前判断，策略需要根据反馈调整下一次query。方法将搜索引擎当环境，让reasoning与search交替，最终用答案outcome训练。 示意：第一次检索发现实体有歧义，Agent可再查限定条件，而不是立即固定回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-search-r1-fce4d489" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-79676ef5125d404d">Search-R1 相对一次性 RAG，为什么需要在推理中反复决定是否搜索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearch-r1">Search-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>中间证据可能暴露新问题或修正当前判断，策略需要根据反馈调整下一次query。方法将搜索引擎当环境，让reasoning与search交替，最终用答案outcome训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一次检索发现实体有歧义，Agent可再查限定条件，而不是立即固定回答。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.09516">原论文</a> · <a href="../../../../agent-research/2503.09516-search-r1/">实现解读</a> · <a href="#qa-79676ef5125d404d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:search-r1" data-paper-title="Search-R1" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Search-R1 Agent University of Illinois Urbana-Champaign 2025-03-12 普通 RAG 一次检索后再回答，无法让策略根据中间证据继续调整查询。Search-R1 把搜索引擎视为环境：模型可在 reasoning 中多次输出搜索动作，环境返回文档后继续推理。训练只对模型生成 token 计算 PPO/GRPO loss，检索结果 token 必须 mask，最终答案用简单 outcome reward 评分。 保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；使用确定性 ScaleMCP mini，不调用论文的 E5 索引或训练 Qwen。mini-suite 的检索结果是确定性的当前任务上下文，适合验证交错状态机和 loss mask；没有真实网页索引、Qwen 参数更新或七个 QA benchmark，因此成功率不能与论文 EM 比较。稳定指标见 classic-agentic-rl-opd-seed42.json。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么检索结果 token 必须 mask，哪怕它们也在模型输入序列中？ 文档由搜索环境返回，不是策略采样的动作，给这些位置算 policy loss 会错误地训练模型生成外部证据。模型只对查询与推理回答等自身 token 负责，检索结果作为后续条件影响决策；多轮检索收益来自闭环调整，不能用静态一次 RAG 代替。 例如搜索返回“发布日期为周二”，训练不应把这句环境文本记作 Agent 的行为，而应更新它怎样查询和据证回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c61b1b171492b766">为什么检索结果 token 必须 mask，哪怕它们也在模型输入序列中？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearch-r1">Search-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档由搜索环境返回，不是策略采样的动作，给这些位置算 policy loss 会错误地训练模型生成外部证据。模型只对查询与推理回答等自身 token 负责，检索结果作为后续条件影响决策；多轮检索收益来自闭环调整，不能用静态一次 RAG 代替。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索返回“发布日期为周二”，训练不应把这句环境文本记作 Agent 的行为，而应更新它怎样查询和据证回答。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.09516">原论文</a> · <a href="../../../../agent-research/2503.09516-search-r1/">实现解读</a> · <a href="#qa-c61b1b171492b766">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:search-r1" data-paper-title="Search-R1" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Search-R1 Agent University of Illinois Urbana-Champaign 2025-03-12 普通 RAG 一次检索后再回答，无法让策略根据中间证据继续调整查询。Search-R1 把搜索引擎视为环境：模型可在 reasoning 中多次输出搜索动作，环境返回文档后继续推理。训练只对模型生成 token 计算 PPO/GRPO loss，检索结果 token 必须 mask，最终答案用简单 outcome reward 评分。 保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；使用确定性 ScaleMCP mini，不调用论文的 E5 索引或训练 Qwen。mini-suite 的检索结果是确定性的当前任务上下文，适合验证交错状态机和 loss mask；没有真实网页索引、Qwen 参数更新或七个 QA benchmark，因此成功率不能与论文 EM 比较。稳定指标见 classic-agentic-rl-opd-seed42.json。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 搜索结果作为上下文可见，与把它们当策略生成 token 学习，有何不同？ 模型可读取文档继续决策，但这些token由环境提供，并非策略动作。训练应mask其loss；否则把环境文本当成学生生成内容，会污染策略优化的行为概率口径。 示意：网页返回一千字，不能视作Agent一次生成一千字动作并获得相应策略梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-38e311ec6e4bf35a">搜索结果作为上下文可见，与把它们当策略生成 token 学习，有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearch-r1">Search-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型可读取文档继续决策，但这些token由环境提供，并非策略动作。训练应mask其loss；否则把环境文本当成学生生成内容，会污染策略优化的行为概率口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>网页返回一千字，不能视作Agent一次生成一千字动作并获得相应策略梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.09516">原论文</a> · <a href="../../../../agent-research/2503.09516-search-r1/">实现解读</a> · <a href="#qa-38e311ec6e4bf35a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:search-r1" data-paper-title="Search-R1" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Search-R1 Agent University of Illinois Urbana-Champaign 2025-03-12 普通 RAG 一次检索后再回答，无法让策略根据中间证据继续调整查询。Search-R1 把搜索引擎视为环境：模型可在 reasoning 中多次输出搜索动作，环境返回文档后继续推理。训练只对模型生成 token 计算 PPO/GRPO loss，检索结果 token 必须 mask，最终答案用简单 outcome reward 评分。 保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；使用确定性 ScaleMCP mini，不调用论文的 E5 索引或训练 Qwen。mini-suite 的检索结果是确定性的当前任务上下文，适合验证交错状态机和 loss mask；没有真实网页索引、Qwen 参数更新或七个 QA benchmark，因此成功率不能与论文 EM 比较。稳定指标见 classic-agentic-rl-opd-seed42.json。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 Search-R1 的 loss mask 怎样避免连搜索动作 query 也一起屏蔽？ 应区分模型生成的reasoning/search指令与环境返回information，前者仍是策略token，后者mask为0。需按来源构建边界，不能仅按某段文本含“搜索”二字一概屏蔽。 示意：&lt;search&gt;里的query是Agent动作，后续&lt;information&gt;正文是环境观测，两段训练身份不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7ba876b05ccaf382">Search-R1 的 loss mask 怎样避免连搜索动作 query 也一起屏蔽？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearch-r1">Search-R1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应区分模型生成的reasoning/search指令与环境返回information，前者仍是策略token，后者mask为0。需按来源构建边界，不能仅按某段文本含“搜索”二字一概屏蔽。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>&lt;search&gt;里的query是Agent动作，后续&lt;information&gt;正文是环境观测，两段训练身份不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.09516">原论文</a> · <a href="../../../../agent-research/2503.09516-search-r1/">实现解读</a> · <a href="#qa-7ba876b05ccaf382">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loop" data-paper-title="LOOP" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="LOOP Agent Apple 2025-02-03 长程数字 Agent 的 rollout 昂贵，而传统 PPO 还要维护 value model。LOOP 把 PPO trust region 与 leave-one-out baseline 结合：无需 critic，可对同一批轨迹进行多次更新；逐 token importance ratio 只裁剪漂移 token，不丢弃整条长轨迹。 保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；当前是确定性交互 mini-suite，不是 AppWorld 32B 训练。本地真实执行多轨迹选择和统计更新，但没有 AppWorld、32B LLM 或梯度 checkpoint；mini-suite 满分只说明轨迹控制逻辑正确，不代表论文任务难度。  长时程 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 LOOP 为什么用同任务多条轨迹代替独立 value network？ 多条轨迹的回报可构造leave-one-out基线，减少critic训练维护，并与PPO trust region结合复用昂贵rollout。无value network不表示无需重要性比或漂移控制。 示意：一条轨迹用其它同题轨迹的平均回报作比较基线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-loop-633efc7d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-65aace0802d88c38">LOOP 为什么用同任务多条轨迹代替独立 value network？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aloop">LOOP</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多条轨迹的回报可构造leave-one-out基线，减少critic训练维护，并与PPO trust region结合复用昂贵rollout。无value network不表示无需重要性比或漂移控制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条轨迹用其它同题轨迹的平均回报作比较基线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.01600">原论文</a> · <a href="../../../../agent-research/2502.01600-loop/">实现解读</a> · <a href="#qa-65aace0802d88c38">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loop" data-paper-title="LOOP" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="LOOP Agent Apple 2025-02-03 长程数字 Agent 的 rollout 昂贵，而传统 PPO 还要维护 value model。LOOP 把 PPO trust region 与 leave-one-out baseline 结合：无需 critic，可对同一批轨迹进行多次更新；逐 token importance ratio 只裁剪漂移 token，不丢弃整条长轨迹。 保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；当前是确定性交互 mini-suite，不是 AppWorld 32B 训练。本地真实执行多轨迹选择和统计更新，但没有 AppWorld、32B LLM 或梯度 checkpoint；mini-suite 满分只说明轨迹控制逻辑正确，不代表论文任务难度。  长时程 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 leave-one-out baseline 为什么把当前轨迹自己排除？ 用其他同组结果作基线，减少把本条回报直接混进自身参照的影响，在无 critic 条件下形成相对优势。长 rollout 成本高，因此逐 token ratio 裁剪和复用同批更新有价值；但多次更新仍受策略漂移约束，不能无限重复把旧轨迹当新 on-policy 数据。 例如三条回报为一、一、零，第一条与另外两条平均比较，而不是用包含自身的整体均值；局部漂移 token 再单独裁剪。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-67c19d40e81f457a">leave-one-out baseline 为什么把当前轨迹自己排除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aloop">LOOP</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用其他同组结果作基线，减少把本条回报直接混进自身参照的影响，在无 critic 条件下形成相对优势。长 rollout 成本高，因此逐 token ratio 裁剪和复用同批更新有价值；但多次更新仍受策略漂移约束，不能无限重复把旧轨迹当新 on-policy 数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三条回报为一、一、零，第一条与另外两条平均比较，而不是用包含自身的整体均值；局部漂移 token 再单独裁剪。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.01600">原论文</a> · <a href="../../../../agent-research/2502.01600-loop/">实现解读</a> · <a href="#qa-67c19d40e81f457a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loop" data-paper-title="LOOP" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="LOOP Agent Apple 2025-02-03 长程数字 Agent 的 rollout 昂贵，而传统 PPO 还要维护 value model。LOOP 把 PPO trust region 与 leave-one-out baseline 结合：无需 critic，可对同一批轨迹进行多次更新；逐 token importance ratio 只裁剪漂移 token，不丢弃整条长轨迹。 保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；当前是确定性交互 mini-suite，不是 AppWorld 32B 训练。本地真实执行多轨迹选择和统计更新，但没有 AppWorld、32B LLM 或梯度 checkpoint；mini-suite 满分只说明轨迹控制逻辑正确，不代表论文任务难度。  长时程 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 LOOP 的逐 token clipping，与发现一个漂移 token 就丢整条轨迹有什么差别？ 逐token约束局部策略漂移，让长轨迹其它有效部分仍能被利用；整条丢弃会损失更多昂贵交互数据。多次复用仍需保留旧行为概率，不是把off-policy样本当全新on-policy。 示意：一百步轨迹只有一个token ratio异常，不应无条件删除其它所有已采反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1fab1e9ed3f8bc5a">LOOP 的逐 token clipping，与发现一个漂移 token 就丢整条轨迹有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aloop">LOOP</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐token约束局部策略漂移，让长轨迹其它有效部分仍能被利用；整条丢弃会损失更多昂贵交互数据。多次复用仍需保留旧行为概率，不是把off-policy样本当全新on-policy。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一百步轨迹只有一个token ratio异常，不应无条件删除其它所有已采反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.01600">原论文</a> · <a href="../../../../agent-research/2502.01600-loop/">实现解读</a> · <a href="#qa-1fab1e9ed3f8bc5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loop" data-paper-title="LOOP" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="LOOP Agent Apple 2025-02-03 长程数字 Agent 的 rollout 昂贵，而传统 PPO 还要维护 value model。LOOP 把 PPO trust region 与 leave-one-out baseline 结合：无需 critic，可对同一批轨迹进行多次更新；逐 token importance ratio 只裁剪漂移 token，不丢弃整条长轨迹。 保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；当前是确定性交互 mini-suite，不是 AppWorld 32B 训练。本地真实执行多轨迹选择和统计更新，但没有 AppWorld、32B LLM 或梯度 checkpoint；mini-suite 满分只说明轨迹控制逻辑正确，不代表论文任务难度。  长时程 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 LOOP 的 leave-one-out baseline 在 K=1 时还能直接计算吗？ 公式分母K−1为0，单条轨迹不满足该组基线定义，需显式处理或拒绝。复用多epoch时还需固定对应旧策略概率和episode身份，不能临时把当前回报又放回其自己的基线。 示意：只有一条样本时，“其它样本平均值”并不存在。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-725085d718d823b9">LOOP 的 leave-one-out baseline 在 K=1 时还能直接计算吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aloop">LOOP</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式分母K−1为0，单条轨迹不满足该组基线定义，需显式处理或拒绝。复用多epoch时还需固定对应旧策略概率和episode身份，不能临时把当前回报又放回其自己的基线。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只有一条样本时，“其它样本平均值”并不存在。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.01600">原论文</a> · <a href="../../../../agent-research/2502.01600-loop/">实现解读</a> · <a href="#qa-725085d718d823b9">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

一次长任务只有最终成功或失败，如何知道应该强化哪轮动作？

## 记住这一点

交互策略学习需要把环境轨迹与参数更新连接起来。Agent Lightning 强调执行与训练解耦，让不同框架产生可用于学习的 transition；GiGPO 在整条轨迹之外，利用重复到达的状态分组提供更细信用。世界模型、技能监督和交互式蒸馏也属于这一问题：需要标明训练状态来自学生执行、专家演示还是环境模型，不能把理想或模拟轨迹当成已经执行的事实。

## 一个例子

设一个搜索任务有“构造查询—阅读结果—提交答案”三轮。最终答错，原因可能是第一轮检索偏题，也可能是最后忽略正确证据。若多条轨迹在相同中间状态采取不同动作，可以在可比条件下比较后续结果。若环境状态不同，仅按轮数对齐再分奖励，会把任务难度或工具差异误计为动作价值。

## 什么时候要小心

步骤信用、策略更新与真实能力是三层证据。合成状态上的有限梯度、重复三 seed 的数值检查，都不能证明浏览、编程或探索能力。特权教师和评分器可用隐藏参考，但 actor 不得看到；高成本完整训练被标成未复现时，本地组件诊断仍只能按原范围解释。

## 先读这几篇

先读 Agent Lightning，画清执行、transition和训练的分离；再读 GiGPO，理解轨迹级与步骤级信用；最后读 ASTEROID，观察部分可见环境中跨 episode 的学生上下文与教师监督如何区分。

1. [Agent Lightning](../../../agent-research/2508.03680-agent-lightning/README.md) · [原论文](https://arxiv.org/abs/2508.03680)
2. [GiGPO](../../../agent-research/2505.10978-gigpo/README.md) · [原论文](https://arxiv.org/abs/2505.10978)
3. [Asymmetric On-Policy Distillation Learns In-Context Exploration](../../../agent-research/2610.30105-asteroid/README.md) · [原论文](https://arxiv.org/abs/2610.30105v1)

## 自测一下

两个第3轮动作看起来相同，但一个环境已取得正确文档，另一个没有；能直接合成同一状态组计算相对优势吗？

??? note "展开参考答案"

    不能只按轮数或动作文本分组。必须先定义并核对影响后续回报的可观察状态与分组条件；否则相对优势会混入环境差异。还要保留执行失败和评分中断，避免只选择成功轨迹来构造学习信号。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
