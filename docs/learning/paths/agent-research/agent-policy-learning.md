---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 交互策略学习：把轨迹反馈变成更新

[Agent](index.md) / 53 个问题 · 53 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">53 个问题 · 53 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frontier-opd" data-paper-title="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond Agent Tsinghua University 2026-10-23 同一个环境观测可能经不同历史反复到达，直接按访问次数或 token 数平均会让循环轨迹主导教师介入判断。Frontier-OPD 先在轨迹内、再在轨迹间聚合有符号师生分歧，对不同状态选原历史代表；教师桥与学生续跑须通过同长窗口比较后才接纳，状态共享不能替代真实历史或任务成功评测。排名只寻找值得试验的节点。教师最多接管回合，再让学生继续回合。新窗口必须和原历史从同一位置开始的回合窗口比较；只有成功重放、非终止交接、完整有效续跑且师生 agreement 不下降，桥的教师响应才加入训练。 成本过高，不复现（审查 DONE）。本地排名和接纳诊断不复现上述分数。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  Agentic OPD / rollout budgeting 学习前沿与教师桥 Agent 交互策略学习：把轨迹反馈变成更新 为什么先轨迹内再轨迹间平均师生分歧，不能按节点访问次数直接平均？ 循环轨迹会多次访问同一状态，若每次都算独立证据，频繁绕圈的一条路径就压过其他轨迹。两级平均先平衡轨迹权重，代表历史再用于真实教师桥试验；排名的有符号分歧与验证 agreement 也不同，节点高分不等于接管一定有益。 例如一条轨迹三次分歧十分，另一条一次零分，节点应是五分；直接按四次访问平均成七点五会放大循环影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-frontier-opd-63269744" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:asteroid" data-paper-title="Asymmetric On-Policy Distillation Learns In-Context Exploration" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Asymmetric On-Policy Distillation Learns In-Context Exploration Agent University of Washington 2026-10-21 部分可观测任务中，专家知道隐藏目标，因而总能直接成功；只模仿专家，学生看不到“失败后如何继续搜索”的上下文。ASTEROID 让当前学生先探索，再在同一个隐藏任务下收集专家的完整成功轨迹。学生用自己的观察、动作和奖励历史预测专家动作，迭代扩大可学习的上下文长度。这不是把金标放入 Agent prompt，也不是固定离线行为克隆，更不应简化成只在学生当前状态上打单步标签的普通 DAgger。论文区分两种采样：固定 latent 的 BAMDP 使用跨 episode 上下文； 完整多环境与机器人实验：成本过高，不复现（审查 DONE）；这是生成式机制诊断，没有公开 benchmark split，也没有 validation 选模、test 能力对比或 evolve 晋级。本地状态：L1 核心机制组件，diagnostic only。本地真实训练一个微型因果 Transformer，保留论文 Algorithm 1 的 episode 级在策略上下文与教师轨迹监督；不宣称复现论文的探索能力、样本效率或机器人效果。完整多环境与机器人实验：成本过高，不复现（审查 DONE）；不自动重试、不阻塞审查。  Agent 训练与策略优化 在策略上下文蒸馏与部分可观测探索 Agent 交互策略学习：把轨迹反馈变成更新 为什么学生先探索，再学习同隐藏任务的专家完整成功轨迹，而不是只模仿开局专家？ 专家知道隐藏目标，直接成功的轨迹缺少失败后继续搜索的上下文。先收学生实际经历，再把这些历史作为专家动作预测的条件，训练其从观察与奖励中更新任务认识；部署时仍没有隐藏目标，学生探索动作也不能被自动当成正确监督标签。 例如学生先找错两个房间，再看到同任务专家如何找到目标，能学习从失败历史缩小范围，而非只记住专家开局直达路线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-asteroid-1bdda102" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsipo" data-paper-title="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution Agent Chinese University of Hong Kong 2026-10-11 静态或离线训练的技能库难以跟随策略进步，而技能增强教师也可能比学生更差。RSIPO从当前策略轨迹产生技能，以独立控制组与同初态重放测量技能收益，联合优化技能生成、RLVR和按经验贝叶斯可靠性加权的自蒸馏。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Table2：Qwen2.5-3B/7B、Qwen3-1.7B，150训练steps；ALFWorld每step16任务×8rollouts，最长50turns，每任务另4次初态重放与4096token技能生成；搜索每step128任务×8rollouts。之前还要GLM-5.2标注的技能SFT。多轮环境训练与教师评分在单卡预计长时间，未作本地测速；不下载或启动。  agentic-rl on-policy-self-distillation recursive-self-improvement Agent 交互策略学习：把轨迹反馈变成更新 为什么技能增强教师的蒸馏权重，要依据收益可靠性收缩后再确定？ 技能可能无效甚至比学生更差，直接等权信任会把退化传回策略。独立控制与同初态重放估计效用差，再按观测噪声向组均值收缩，用较可靠收益调节蒸馏信任；技能奖励与收缩信任用途不同，失效重放也不能作为有效配对证据。 例如某技能只试一次碰巧成功，其收益不确定应被收缩；多次同初态对照都有效的技能，才更值得提高蒸馏权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-rsipo-71b84017" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evo2" data-paper-title="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution Agent University of Illinois Urbana-Champaign / Google DeepMind 2026-10-09 固定任务 executor，共享 Proposer/Reflector 编辑 harness；树搜索与跨分支 crossover 的执行反馈反过来训练 evolver。EvoTIDE 恢复有效编辑轨迹，先 SFT，再交错更新两个角色。事实来源：原文全文。 此处只是有边界的 GSM harness 机制诊断，非原 coding benchmark 复现或隔离 test 能力提升；当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为固定 executor 与初始可执行 harness；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evolution weight-harness-co-evolution dual-role-grpo Agent 交互策略学习：把轨迹反馈变成更新 为什么固定 executor，却训练 Proposer 与 Reflector，仍可称为演化器本身在进步？ 执行任务的模型保持不变，变化的是提出和修复 harness 的策略参数；搜索产生的有效编辑轨迹为这两个角色提供训练信号。这样改进对象从候选框架扩展到如何改框架，keep 收益仍为零，不能把没改动的提议也奖励成成功创新。 例如同一个执行器处理任务，训练后的提议者更会选择日志压缩方案，反思者更会修复错误 hook，收益来自改进过程变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-evo2-2bf44b34" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:race" data-paper-title="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation Agent Renmin University of China 2026-10-08 LoGiC 从第二轮逐步删除推理，检查本轮及所有后续原动作的平均 token 对数似然变化，已接受删除继续影响后续上下文。成功轨迹压缩后用于 SFT；RL 屏蔽可删推理并监督提前闭合。原文四个 Agent 环境推理 token 分别减少 32.3%、80.2%、46.4%、62.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。动作似然、成功轨迹 SFT 与 cover-aware actor 梯度接口已实现。真实输入必须提供公开环境、修订与 reason/action/observation 训练轨迹；不能把 QA 解题行伪装成工具轨迹。评估 Agent 不读取参考动作。论文四环境完整 on-policy RL 尚未复测；其端到端能力结果仍缺。  Agentic RL 推理效率 跨轮信用分配 Agent 交互策略学习：把轨迹反馈变成更新 删除某轮 reasoning 时，为什么还要检查所有后续原动作的似然变化？ 当前动作看似不受影响，不代表早期推理对后面规划无用。逐步删除后用受影响的新上下文评估后续动作，只有变化都在容差内才继续，已接受删除也保留在之后压缩状态；仅检查本轮会漏掉长程依赖，删 token 数也不等于任务成功。 例如一段推理提前记住安全限制，本轮只是读取文件，后面删除动作才依赖该限制；只验本轮就可能误删关键思考。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-race-11c5fa7f" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adastep" data-paper-title="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning Agent Tsinghua University 2026-10-02 Agent 长轨迹的终局奖励给每一步同样的全局优势，无法指出哪一步有用；GiGPO 等方法用相同锚状态的局部回报补充信用，但同一动作之后的随机路径也会改变回报。AdaStep 不另训 critic，而是看同组中不同动作解释了多少回报方差。动作间差异主导时信任局部信用；同动作内部差异主导时将局部修正压低，保留全局优势。 L1 统计机制诊断。L1 统计机制诊断。实现论文 Eq. (17)–(18) 的同锚状态、按动作分组的方差分解、稀疏组回退和最终优势组合；没有宣称完成 Agent 策略训练或原文任务评测。输入只包含策略 rollout 的任务 ID、状态键、动作、折扣回报和全局优势；分组键为任务 ID 与 anchor state，避免不同任务的同名状态互相污染。不读取金标答案或计划。这里未运行环境交互、Qwen 策略更新、ALFWorld/WebShop/ScienceWorld，也没有同预算的 GiGPO 对照。  Agentic RL 步骤信用分配 方差可靠性 Agent 交互策略学习：把轨迹反馈变成更新 同锚状态下动作内回报方差很大时，为什么应降低局部信用修正？ 同一动作后续随机路线就能导致很大成败差，说明局部动作未解释大部分回报变化。方差分解让动作间差异主导时更信任局部优势，否则保留全局优势而压低修正；权重从原始回报统计估计，不能先随意归一化后改变方差关系。 例如动作甲的几条 rollout 既有满分也有零分，乙也类似，差异主要来自后续随机性，就不应把单次结果强归因给甲乙。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-adastep-2ac090d9" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:depgpo" data-paper-title="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents Agent Southeast University 2026-10-02 终端 Agent 通常只拿到任务结束后的 verifier 奖励。GRPO 把同一条轨迹的优势分给所有生成 token，无法区分真正生成答案的命令、为其提供数据的读取，以及后来被覆盖或无关的操作。DepGPO 从执行记录构造命令依赖图：文件读取连向该文件尚未覆盖的写入者，可信的 stdout 复用也形成边；再从 verifier 实际检查的文件、端口和进程向后追溯。 L1 机制诊断。L1 机制诊断。这里实现了论文的记录级读写依赖、相关写入与支持性读取信用，以及步级/令牌级优势归一化；尚未接入真实终端 tracer、verifier 执行或 Qwen 策略训练，不能把机制指标当成任务成功率。机制回执只包含四条手工结构化命令：支持读取、间接写入、最终写入、无关写入。测试还覆盖覆盖写不自动建立依赖、写入记录分母、最短路径、回退、负优势与 token 数不等时的均值守恒。这不是 Terminal-Bench、真实 Qwen 训练或多 seed 能力比较。  Agentic RL 终端命令依赖 步骤信用分配 Agent 交互策略学习：把轨迹反馈变成更新 命令依赖图为什么要连接文件读取与尚未被覆盖的写入者？ 读取实际消费的是当时有效版本，已被后续覆盖的旧写入不一定影响最终产物。依赖图从 verifier 检查对象向后追踪，把贡献数据的操作与真正结果路径连接，减少无关步骤共享终局优势；图构建还需可信执行记录，不能凭命令文字猜因果。 例如先写旧配置、再覆盖新配置，测试只读取新版本；信用不应同样奖励已被覆盖且未被使用的旧写入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-depgpo-58f41b1f" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dr-credit" data-paper-title="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents Agent University of Chinese Academy of Sciences 2026-09-28 按 rubric 的历史已接受支持计算本次工具结果带来的新增或部分支持，再与最终结果优势结合，避免重复证据反复得分。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent RL 过程信用分配 Agent 交互策略学习：把轨迹反馈变成更新 为什么检索到重复证据不应该反复获得同样的过程奖励？ 过程信用应反映相对已接受证据的新支持，而不是工具调用次数。按 rubric 维护历史覆盖，再评本次新增或部分支持，能减少重复搜索刷分；最终结果优势仍保留，避免局部新颖证据与真正研究目标脱节，支持关系也须有可核验依据。 例如两次返回同一发布日期，第二次没有补新约束就不应再拿完整奖励；找到此前缺失的机构证据才有新增贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-dr-credit-775af357" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:graphhca" data-paper-title="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents Agent Beihang University 2026-09-28 稀疏终局奖励难以定位长轨迹中的关键动作。GraphHCA 把 rollout 合并为状态转移图，以成功/失败终态为边界解折扣固定点，再把相邻状态的对数势能差分配给每一步，并在同状态动作间标准化。 复现级别：L1 无 gold 核心机制。复现级别：L1 无 gold 核心机制。本地从采样轨迹图、动作和终局结果计算固定点势能与逐步优势；不读取参考答案或计划。当前未训练语言模型，也未把 GraphHCA 注册为 Evolve 算子。只有统一控制器能采样真实轨迹、执行该 estimator 并隔离验证策略更新后才算正式接入。graphhca_credit 只接受 Transition 和 success 布尔值；汇总实验见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Agentic RL 信用分配 轨迹图 Agent 交互策略学习：把轨迹反馈变成更新 为什么先解状态图折扣固定点，再用对数势能差给动作信用？ 终局成功失败作为边界，经经验转移传播到共享状态，得到通往成功的折扣潜势；相邻状态的对数变化把远期信息转成局部推进信号，再在同起点动作间标准化。它利用完整 rollout 作训练归因，不能把这些事后成功边界交给评测 Agent 当观察。 例如两条路径都经过同一中间状态，状态图可共享其后成功证据，再比较离开该状态的动作是靠近成功还是走入死路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-graphhca-933790a0" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dependency-refinement" data-paper-title="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning Agent ShanghaiTech University 2026-09-16 把多轮轨迹表示为轮级依赖 DAG，依次执行叶节点裁剪、严格合并和宽松合并，减少冗余消息同时保留最终答案依赖。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。  轨迹精炼 Agent 微调 Agent 交互策略学习：把轨迹反馈变成更新 为什么压缩多轮轨迹先裁叶节点，而不能按消息长度直接删最长一段？ 依赖 DAG 标记哪些轮次支撑最终答案，叶节点更可能是无下游依赖的冗余分支。后续严格和宽松合并再逐步减少重复，同时维持必要信息流；最长消息可能恰是关键工具证据，纯长度裁剪会把学习样本变成缺因果条件的残缺轨迹。 例如长日志里包含唯一错误码，短闲聊反而无依赖；依赖裁剪应删闲聊叶节点，而不是因为日志长就优先扔掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-dependency-refinement-97ad396d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-bandit" data-paper-title="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning Agent Harbin Institute of Technology / Alibaba Cloud 2026-09-12 联合 learnability、transferability 与探索 bonus 分配多 harness 训练预算。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行在线 harness 调度；没有进行大模型 RL。本地执行在线 harness 调度；没有进行大模型 RL。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent RL Harness 调度 Agent 交互策略学习：把轨迹反馈变成更新 learnability 与 transferability 为什么需要同时进入多 harness 的训练调度？ 容易学的框架可能只让策略适应其特殊接口，迁移性强但当前难学的框架又需要更多探索。联合两类信号及 bonus 分配有限训练预算，避免只在一套容易刷分的环境过拟合；调度权重只是训练决策，参考函数或多种子诊断不是跨框架能力证据。 例如框架甲提供很多提示、乙较接近部署接口，不能因为甲短期涨分快就把全部预算都给它，还需考虑学到的技能能否转移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-harness-bandit-ffd58529" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t1-terminal-rl" data-paper-title="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks Agent National University of Singapore / Tencent 2026-09-09 TITO 使用 rollout 实际采样 token id 训练，turn boundary repair 修正漂移，R3 重放 MoE 路由选择。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent RL 长程终端任务 Agent 交互策略学习：把轨迹反馈变成更新 为什么训练要使用 rollout 真正采样的 token ID，而不是把完整交互文本重新分词？ 拼接工具观察与多轮消息后重新分词，边界和 token 可能与实际采样不一致，导致策略概率对应错误动作。TITO 保留真实 ID，边界修复处理漂移，MoE 路由重放再控制专家路径差异；数据对齐正确仍只是训练合同，不等于终端任务已学会。 例如一段命令与下一条观察拼接后形成不同子词，重新分词会把非动作内容也混进训练；保留采样 ID 才能对准原动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-t1-terminal-rl-406c9b27" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:multi-harness-rl" data-paper-title="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents Agent New York University 2026-09-03 多 Harness RL 同时改变了执行环境多样性和 GRPO 的分组边界，难以判断增益来源。论文冻结相同 task-harness 轨迹，只比较组内和跨 harness advantage，并用训练中未见的最小 harness 审计能力是否真正迁移。 复现级别：CPU 分组信用与可微训练算子。复现级别：CPU 分组信用与可微训练算子。在相同 rollout 上计算 task×harness 与 task 两种标准化优势；尚不包含真实编码 Agent 的 held-out harness 迁移实验。真实 coding harness、Qwen3-8B RL 和 sealed oracle 均未在本地复刻；该实现用于防止未来 Evolve 实验把 harness 差异误报为模型能力。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Multi-harness RL audit Agent 交互策略学习：把轨迹反馈变成更新 冻结同一批 task-harness 轨迹，只改 advantage 分组，能隔离哪种混淆？ 多框架训练同时带来数据多样性和信用比较范围变化，直接对比两个完整系统无法区分来源。固定轨迹后，在同 task 内比较跨框架与各自框架标准化，才更集中检验分组影响；迁移还要在训练未见的最小 harness 上报告差异与不确定性。 例如同一道修复题在两种接口产生相同已存轨迹，重新计算分组优势而不重新采样，可减少把采样变化误归因给信用规则。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-multi-harness-rl-66c31df3" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ace-data" data-paper-title="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents Agent Huawei Technologies Co., Ltd 2026-08-27 论文把 Agent 数据统一表示为：环境、任务、交互轨迹与可选 verifier。Accuracy 先限定可信支持集，Complexity 相对指定学习者校准难度，Diversity 再控制环境、任务和行为覆盖。 复现级别：框架可执行化 mini-suite。复现级别：框架可执行化 mini-suite。论文是综述/统一框架；本地把三道约束实现为数据准入门。这是框架的可执行准入合同，不声称复刻某个训练模型或公开 benchmark SOTA。planbench-mini、120 episodes：joint success 1.0000、average cost 0.3700，另记录 accuracy gates、complexity calibration 和 diversity accept/reject。指标见 metrics/planbench-mini-seed42.json。  Agent 数据质量 Agent 交互策略学习：把轨迹反馈变成更新 为什么 Complexity 必须相对指定学习者校准，而不能只给任务一个固定难度标签？ 同题对不同模型的可学性不同，过易提供少量新信号、过难可能只产生失败。Accuracy 先保证样本可信，学习者相对的复杂度再选有效区间，Diversity 补环境与行为覆盖；三者缺一不可，轨迹长或工具多本身不能证明数据更优。 例如初级模型解三步工具题尚可学习，二十步全失败未必更好；强模型可能正需要后者，课程区间应随学习者变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-ace-data-9a8b6ddd" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ahead" data-paper-title="AHEAD: Agentic Hints for Effective Agent Development" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AHEAD: Agentic Hints for Effective Agent Development Agent AWS AI Labs / Purdue University 2026-08-25 轨迹级 GRPO 给所有步骤同一 advantage；统一 privileged information 又浪费在普通步骤上。AHEAD 先分析失败轨迹定位关键错误：所有步骤的 teacher 都看到环境反馈，只有错误步骤额外看到 LLM corrective hint；teacher/student log-prob gap 被有界地注入 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。普通步骤只用环境反馈，错误步骤再追加 corrective hint，并生成稠密信用。mini-suite 使用确定性错误位置验证 step-aware PI 分流；未运行 LLM analyzer、Qwen、真实 GRPO 或三个原始 benchmark。PlanBench-mini 120 episodes：24 个 error-step hint、360 个 dense-credit 更新，joint success 1.0000，平均成本 0.6160。  环境反馈提示训练 Agent 交互策略学习：把轨迹反馈变成更新 纠错 hint 为什么只额外给关键错误步骤的 teacher，而不是所有步骤都给完整答案提示？ 普通步骤已有环境反馈，统一特权提示会浪费信号并掩盖真正需要纠正的位置。定位错误后，在相同生成动作上比较有无 hint 的对数概率差，再有界调节终局优势；提示只在训练教师侧使用，不能把答案或纠错信息直接放进部署学生上下文。 例如轨迹只有第三步选错工具，额外 hint 应聚焦该决策，而非让每一步都看到最终解决方案再假称学生自主完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-ahead-17c82764" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spo-plus-plus" data-paper-title="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction Agent Renmin University of China 2026-08-25 SPO 用单 rollout 和持久 prompt value 避免等待 sibling，但 completion 顺序会污染历史，而且 trajectory whitening 与 token-mean actor loss 的测度不一致。SPO++ 按生成策略事件组织证据、dispatch 时冻结 baseline，并用动作 token 数加权标准化 advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每次 dispatch 冻结 prompt value，并按 action-token measure 消费 advantage。确定性 mini-suite 验证事件时间状态与测度对齐；未运行异步 Qwen3.5、ALFWorld 或 Math-TIR 训练。PlanBench-mini 120 episodes：joint success 1.0000，平均成本 0.6400，执行 120 次冻结 value 与 360 个 action-token measure 更新。  异步单流 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么 token-mean actor loss 要用动作 token 数加权 advantage 标准化？ 若每条轨迹只投一票做白化，而损失按 token 平均，长短轨迹在两处的测度不一致，会改变实际更新权重。token 加权让标准化与优化对象一致，dispatch 冻结 baseline 又防止异步完成顺序污染历史；它不是简单把奖励按文本长度重新定义。 例如一条十 token、一条一百 token，损失中后者占更多位置，标准化若各算一票，就与真实梯度平均的权重不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-spo-plus-plus-c1491ed7" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-g2" data-paper-title="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning Agent Baidu 2026-08-24 Hint-based Agent RL 保留专家轨迹前缀再让策略探索，但固定深度忽略任务难度，逐样本 probe 又浪费 rollout。Agent-G² 从已有 policy rollout 按难度簇估计 guidance band 的中心和方差，对每个任务采样不同前缀深度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每个任务从在线更新的高斯分布采样专家前缀深度，不额外执行 probe rollout。mini-suite 验证按任务簇在线估计、Gaussian sampling 和专家前缀/策略续写的控制流；没有运行 Qwen2.5、ALFWorld/WebShop 或真实 GRPO。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，在线采样 guidance 120 次，平均成本 0.8253。指标见 metrics/planbench-mini-seed42.json。  高斯 guidance Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么 guidance 深度要按难度簇采样，而不是所有任务都保留相同长度的专家前缀？ 简单题给过多前缀会减少自主探索，难题给太少又可能只产生失败。已有 rollout 的簇级成功率与波动用于调整引导带中心和方差，再为任务采样深度，减少逐题额外 probe；训练前缀是脚手架，评测不能继续提供参考专家轨迹来冒充独立解题。 例如简单开门题只给很短提示，复杂多房间任务可给较长起步；固定一半前缀会让前者过度依赖、后者仍难学。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent-g2-1fe5ec6c" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autosaddler" data-paper-title="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces Agent Microsoft / POSTECH 2026-08-24 长任务中 prompt、tool configuration 和 middleware 的小错误会累积，而人工调 harness 成本高。AutoSaddler 把 harness 当代码：从 mini-batch 失败 trace 做深度诊断，生成有边界的结构化 patch，在同 batch 检查因果效果，再用 dev set 选更新并写入 EvoDAG，形成可持续版本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际执行深度失败诊断、结构化 patch、局部/held-out 验证和 durable harness 更新。没有运行 GAIA2、SWE-Bench Pro、Terminal-Bench 2.0 或论文的生产 harness；本地只验证优化循环、验证边界和 durable reuse。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，12 次 failure diagnosis 与 durable update、108 次复用，平均成本 0.5440。  Harness 自动优化 Agent 交互策略学习：把轨迹反馈变成更新 同 batch 检查 patch 效果后，为什么还要在 dev set 选择并写 EvoDAG？ 原失败 batch 适合诊断因果方向，却可能被针对性补丁过拟合。开发集再比较更新，版本图记录从哪个父框架与证据产生，支持后续迭代和回溯；结构化 patch 有边界不等于语义安全，测试报告集也不能加入循环选更新。 例如补丁恰好修好三条相同报错，需要再看其他开发任务是否退化，并保存父子关系，而不是立刻覆盖唯一框架文件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-autosaddler-3e805f29" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auso" data-paper-title="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization Agent University of Science and Technology of China 2026-08-21 外部技能检索有上下文开销，完全内化又失去按任务选择能力；按整条轨迹成功率硬切阶段还无法判断某一个动作是否真正受益。AUSO 先用 skill-conditioned teacher 内化通用技能，再进行 outcome-driven exploration，最后对每个动作比较有技能和无技能策略的 JSD，以有界权重调整 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行技能内化、无技能/有技能动作分布 JSD、bounded utilization weight 和复用阶段切换。未运行 ALFWorld/WebShop/SearchQA、大模型 token rollout 或完整 GRPO；确定性 mini-suite 验证 progressive lifecycle、JSD 信息增益和 bounded reweighting 的控制流，不把成本代理指标冒充论文成功率。本地对照口径：基线为同一 PlanBench-mini、120 episodes 的 SkillRise；  动作级技能优化 Agent 交互策略学习：把轨迹反馈变成更新 动作级 JSD 调权为什么要有界且不翻转原轨迹 advantage 的符号？ 有无技能的分布差说明该动作受技能影响多大，却不直接证明它有益。保留结果优势符号，让局部权重只调节信用强弱，避免把失败轨迹某步因分歧大就变成正奖励；内化、探索和利用分阶段处理，也减少外部技能上下文的持续开销。 例如一次失败中某动作很依赖技能，可以加强对其错误的学习力度，但不能仅因依赖强就把这一步改奖为成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-auso-a7af1bb4" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sapo" data-paper-title="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning Agent Xiamen University 2026-08-20 同一自回归骨干在不同因果边界输出 policy/value，结合 PPO、on-policy SARSA 和 trajectory GAE。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 同一自回归骨干输出 policy 和 value 时，为什么必须指定不同因果边界？ 动作概率应只条件化于决策前可见历史，价值估计也要对应正确时点，混入动作后观察会使优势携带未来信息。共享骨干节省模型结构，但 PPO、SARSA 与 GAE 的状态动作对齐仍要严格维护，单 rollout 不表示可以忽略 bootstrap 与终止语义。 例如决定运行命令前的 value 不能先读到该命令测试通过的输出，否则策略看似获得精确信用，实则泄漏了未来结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-sapo-b38c3177" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rtpo" data-paper-title="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training Agent Adelaide University 2026-08-19 把多轮 rollout 组织成稀疏反向树，按时间逆序更新 turn，令决策与下游 continuation 保持 on-policy。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新 为什么按 turn 逆序更新有助于保持决策与下游 continuation 的 on-policy 对应？ 早期动作价值依赖后续策略，若下游已大幅改变却仍用旧 continuation 信用，会产生不一致。反向树先处理靠近结果的回合，再向前传播相应训练依据，让前段决策面对更新后的续跑关系；顺序稳定训练不等于无需重要性或执行对齐检查。 例如最后两步已学会恢复，开局动作的好坏应按新的恢复能力重新理解，而不持续沿用末段还是旧失败策略时的估值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-rtpo-1c108353" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spade" data-paper-title="SPADE: Self-Play in Adaptive Synthetic Executable Environments" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPADE: Self-Play in Adaptive Synthetic Executable Environments Agent University of Washington 2026-08-19 同一 LLM 分饰环境设计者和推理 Agent，以有/无 privileged hint 的 regret 学习能力边界上的可执行环境。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 环境生成 Agent 交互策略学习：把轨迹反馈变成更新 环境设计者为什么用有 hint 与无 hint 的 regret，而不是只追求让 Agent 失败？ 纯失败奖励可能生成根本无解或过难的环境，无法提供有效课程。hint 能显著提高表现而无 hint 仍困难的差距，更接近可学习能力边界；环境还必须可执行，特权信息只属于训练比较，不能在无提示评测时暗中交给推理 Agent。 例如迷宫无提示难走、给方向后可完成，适合作为训练挑战；完全封死出口让双方都失败，不应只因困难就获高设计分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-spade-5fdace60" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:planpo" data-paper-title="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs Agent Xiamen University 2026-08-18 在成功轨迹内同时比较 trajectory turn 数和单 turn response 长度，形成 coarse-to-fine planning advantages。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 规划 Agent 交互策略学习：把轨迹反馈变成更新 为什么只在成功轨迹中比较回合数和响应长度，而不能直接奖励所有短轨迹？ 短可能来自高效规划，也可能只是提前放弃。先以结果区分成功，再在可比成功路径内看少回合和短响应，才更接近规划效率。粗到细优势补充 outcome，不能压倒正确性，也不能用少 token 掩盖必要工具取证被跳过。 例如两条都修好同一 bug，一条少三次无效搜索可获效率优势；另一条直接说完成却没改文件，不能因更短而受奖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-planpo-5fac2579" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:trca" data-paper-title="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents Agent Authors did not disclose affiliation 2026-08-17 无需成功 anchor，从每个状态转移的 Evidence、Execution、Invalidity rubric 构造基础和 breakthrough reward。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 过程奖励 Agent 交互策略学习：把轨迹反馈变成更新 把 Evidence、Execution、Invalidity 分开评估，为什么比单一过程分数更可定位？ 转移可能增加证据却执行失败，或动作格式合法但没有任务价值，分项 rubric 能区分这些情况并限制无效行为。breakthrough 信号强调关键推进，不必等待成功锚轨迹；但 rubric 仍需基于真实状态转移，不能由固定模板分数代替环境过程。 例如搜索返回新错误原因属于证据进展，随后命令语法错属于执行问题；合成一个总分会模糊究竟应该修检索还是修调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-trca-ae92667a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sinkflex-rl" data-paper-title="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks Agent Capital One AI Foundations 2026-08-11 长程工具 Agent 的 on-policy rollout 同时受环境状态、长上下文和训练显存限制。SinkFlex-RL 把 Gymnasium 双控制环境、VERL 风格数据流、无 value model 的 GRPO 与 sink-aware FlexAttention 组合，causal / sliding-window mask 下仍保留模型特有 sink scaling。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行 sink 保留、causal sliding window 和无 critic 的 group-relative 更新路径；未声称复刻 CUDA FlexAttention kernel。未复刻论文的 MoE checkpoint、VERL 集群、τ²-Bench 全环境或 GPU kernel 显存曲线；mini-suite 验证状态保留规则与 RL 控制流，GPU 性能数字仅引用原文。ScaleMCP mini-suite 120 episodes：joint success 1.0、average cost 0.67；  Agentic RL / efficient long context Agent 交互策略学习：把轨迹反馈变成更新 滑窗或 causal mask 为什么仍要保留模型特有的 sink scaling？ 稀疏可见性与 sink 数值机制影响注意力的不同部分，改 mask 并不授权删除模型原有缩放。训练系统还需连接真实环境状态、长上下文与 GRPO 数据流；公式 kernel 通过只能说明局部算子，不能替代完整 on-policy rollout 和工具任务验证。 例如窗口只保留最近文本和 sink，若同时把 sink 的特殊缩放去掉，输出变化就混入两项改动，无法归因于滑窗本身。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-sinkflex-rl-6bf5fe2a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:residency-rl" data-paper-title="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments Agent Google DeepMind 2026-08-07 静态知识题不能覆盖主动询问、工具调用及长程决策。论文通过场景生成、带信息不对称的模拟环境、按维度隔离的裁判和GRPO组成完整训练链路；隐藏参考信息只属于环境/裁判，不能直接暴露给被评估策略。原文§3 成本过高，不复现（审查 DONE）。原配置依赖内部Gemini策略训练及独立模拟/裁判调用，使用49,870个常规场景、5,000个历史询问场景和2,583个对抗场景；每条轨迹可达60轮对话及8次工具调用。原文§3.4  多轮 Agent RL 多轮模拟与结构奖励 Agent 交互策略学习：把轨迹反馈变成更新 带信息不对称的模拟训练，为什么必须把隐藏参考留在环境和裁判侧？ 策略需要通过询问、工具和观察逐步取证，若直接看到参考信息就绕过了长程决策难点。各维裁判隔离再聚合奖励，减少互相污染，但奖励公式本身不是完整环境或专业能力；本地诊断也不能当真实临床效果或决策可靠性的证据。 例如模拟任务中某项状态应通过查询后才出现，不能把完整参考摘要先放进策略提示，再把最终判断记成自主取证成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-residency-rl-21b2b4df" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-opsd" data-paper-title="AgentOPSD" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AgentOPSD Agent Tsinghua University 2026-08-06 轨迹奖励难定位少数关键决策。AgentOPSD 把 privileged replay 的 token teacher/student log-prob gap 聚合成 turn evidence，再在 log-odds 空间递归更新成功信念，以相邻信念修订量识别 pivotal turn。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现逐 turn evidence、递归 log-odds belief、pivotal revision 和 critic-free policy update。  递归 turn 信用 Agent 交互策略学习：把轨迹反馈变成更新 为什么用相邻成功信念的修订量，而非最终信念值识别 pivotal turn？ 最终值混合了此前全部证据，不能定位哪一步导致关键改变。把 token 师生概率差累积到 log-odds，再观察每回合 sigmoid 信念的增量，能提取局部转折；这是训练侧事后归因，特权 replay 和参考信息不能交给独立评测策略。 例如前几步信息平淡，某次工具返回让成功信念陡升，该回合增量更能提示关键作用，而非把高终值平均分给所有动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent-opsd-6c6325b8" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cipo" data-paper-title="Contextual Information Policy Optimization for Search Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Contextual Information Policy Optimization for Search Agents Agent Beihang University 2026-08-06 主题：搜索 Agent RL。只奖励最终答案会让检索退化成确认偏见。CIPO 识别受外部证据影响的后续动作，给予 dense turn credit，并与全局 outcome reward 联合优化。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索 Agent RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么只奖最终答案可能让搜索变成确认偏见，而 dense evidence credit 有帮助？ 模型可能先猜答案再只找支持它的内容，终局碰巧正确掩盖了无效搜索。识别外部证据真正改变后续动作的回合并给局部信用，鼓励信息被实际使用，而非机械调用次数；仍需结合全局 outcome，避免只追新证据却偏离问题。 例如搜索发现原猜测日期错误，Agent 据此改查另一来源，这种证据驱动转向应区别于反复查询同一句猜测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-cipo-5f899139" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:envace" data-paper-title="EnvACE" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EnvACE Agent Shanghai Jiao Tong 2026-08-06 EnvACE 不另训 world model，而让同一个 agent policy 在真实 act 之间切换到 rehearsal role，自行预测下一 observation；训练时分别为 acting 与 rehearsal 轨迹计算 group-relative advantage，避免两种奖励尺度互相污染，测试时可用少量私有 rehearsal 扩展规划。 Fidelity：核心机制复现。同一策略交替 act/rehearse，rehearsal observation 仅作私有规划状态，并执行 role-wise group advantage。确定性 mini-suite 验证状态路由与计数，不等同于论文浏览器/工具环境和大模型 RL 训练。PlanBench mini-suite 120 episodes：joint success 1.0000，执行 360 次 world rehearsal、720 次 role-wise advantage update；real_tool_responses=0，确保预测 observation 没被伪装成真实环境反馈。  环境 rehearsal / Agent RL Agent 交互策略学习：把轨迹反馈变成更新 acting 与 rehearsal 为什么要分别计算 group-relative advantage？ 真实行动成败与观察预测的奖励尺度和目标不同，放在同一组中心化会让一种角色的高分压制另一种学习。分组后共享策略仍能练习预测环境，再把私有 rehearsal 用于规划；想象的下一观察不能当作真实工具反馈写入执行证据。 例如演练预测“门打开”得高分，不应让实际行动失败也因同组分布被误奖励；演练结果还须与真实开门返回区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-envace-95e34f1b" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoharness-rl" data-paper-title="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents Agent University of Illinois Urbana–Champaign / Meta AI 2026-08-05 主题：Harness policy RL。把 Belief、Progress、Experience 暴露为策略可操作的外部状态；先 SFT 学会 harness action，再以成本感知 GRPO 学习何时读写和合并。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness policy RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness policy RL Agent 交互策略学习：把轨迹反馈变成更新 为什么 Belief、Progress、Experience 要成为策略可读写的外部状态？ 固定框架替模型决定保存和合并什么，可能不适合当前任务。显式 harness action 让策略学习维护信念、进度与经验，先 SFT 学接口，再以任务收益减管理成本优化使用时机；写得越多不等于越好，状态内容也须由实际观察支持。 例如遇到新约束时写入 Belief，重复信息则合并进 Experience；若每轮无差别追加所有日志，管理费用会抵消任务收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-evoharness-rl-68a7cfc6" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ocsd" data-paper-title="OCSD" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="OCSD Agent Nanjing University 2026-08-05 直接重放未来 observation 时，token 分数变化同时来自观测信息和重放脚手架。OCSD 构造结构完全匹配的 Full 与 Observation-Ablated 两个 replay，仅以二者残差调制高不确定 step 的 GRPO 更新。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。执行 full/observation-ablated matched replay、residual calibration 和 turn-level credit。  观测校准蒸馏 Agent 交互策略学习：把轨迹反馈变成更新 为什么 Full replay 要减去结构匹配的 Observation-Ablated replay？ 直接比较带未来观察的重放与学生，变化同时含观察内容和额外脚手架格式的影响。保持结构一致只消融观察，再取差值更集中识别信息贡献，之后只调高不确定步骤的更新；未来信息属于训练归因，不能成为测试时可见输入。 例如重放模板本身多了“请检查”提示，两种 replay 都保留它，只有真实观察有无不同，才能少把提示效应算给观察。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-ocsd-b0061afd" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:state2state" data-paper-title="State2State: Environment-Derived Mid-Training for LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="State2State: Environment-Derived Mid-Training for LLM Agents Agent Tsinghua University AIR / Alibaba Group 2026-08-05 主题：环境派生中训练。从环境探索自动采样起点与目标状态，用规则化状态匹配做 verifier，形成无需人工任务与专家轨迹的可扩展 mid-training。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的环境派生中训练算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  环境派生中训练 Agent 交互策略学习：把轨迹反馈变成更新 从环境起点与目标状态构造任务，为什么不需要同时提供专家动作轨迹？ 目标描述规定希望到达哪里，策略可通过探索尝试如何到达，规则化状态匹配仅负责最后验证。这样把任务生成与专家示范分开，扩大中训练来源；验证器内部目标或规则不能作为逐步正确动作提示，匹配定义也必须保留任务相关状态。 例如给出初始物体布局和目标布局，Agent 自己移动物体，环境最后比对；无需先给一条“先左后右”的标准操作序列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-state2state-baaabd4d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hindsearch" data-paper-title="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning Agent Santa Clara University 2026-08-03 主题：搜索轨迹 hindsight。冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索轨迹 hindsight 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索轨迹 hindsight Agent 交互策略学习：把轨迹反馈变成更新 judge 可看 gold 生成 critique 时，为什么不能把这段 critique 直接用于评测搜索？ gold 用于训练侧解释失败，把稀疏成败转成更具体的蒸馏信号，帮助策略学习纠错方向。评测若继续提供同题参考派生 critique，策略已间接得到答案信息，就不再衡量独立搜索；冻结 judge 只固定参数，并不消除其输入中的特权来源。 例如训练时根据正确日期指出查错来源，测试时仍必须只给日期问题；不能先送“正确应为周三”的批评再统计自主答对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-hindsearch-b112afa3" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grsd" data-paper-title="Group-Reflective Self-Distillation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Group-Reflective Self-Distillation Agent Baidu Inc. 2026-07-30 轨迹终局 reward 混合了真正有效行为、重复错误与偶然选择。GRSD 让当前 policy 对同题 on-policy group 中每条已验证轨迹反思，再由参数相同的 stop-gradient 快照对比成功/失败反思，形成只在训练期可见的 DO/AVOID guidance，并调制 turn-level advantage。 保真度：执行成功/失败 rollout group、策略自身反思、stop-gradient group guidance 与 turn-level 更新。反思由可审计结构化轨迹产生，不是 Qwen 自然语言反思；验证的是 group contrast 和更新路由。本地对照口径：PlanBench mini-suite 120 episodes；joint success 1.0000，并执行 120 个反思组、120 次成败对照、360 次 privileged-guidance update。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 DO/AVOID guidance 为什么由 stop-gradient 快照生成，并只在训练时可见？ 指导从同题已验证的成功失败反思形成，固定快照防止指导路径随当前梯度共同漂移。它调节 turn-level 信用而不让评测策略偷看整组事后成败；正乘数还保留结果优势方向，避免把某段反思本身当作答案或独立奖励 oracle。 例如组内成功者都先检查依赖，失败者直接改代码，训练可提炼这一对照；新测试题不能预先看到它自己的成功失败组反思。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-grsd-ed16d3df" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tapo" data-paper-title="TAPO" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TAPO Agent Peking University 2026-07-30 稀疏任务 reward 只告诉 Agent 最终成败，没有利用每次动作后的环境反馈。TAPO 复用同一 rollout，在共享 backbone 上交替训练策略目标与的 next-observation 预测，不增加采样、专家数据或推理开销。 保真度：在确定性环境实际交替执行 policy action 与 action-conditioned next-observation supervision。确定性 observation 适合验证数据流与交替目标，不等同于 Qwen2.5 在 WebShop/ALFWorld 的 RL 训练。本地对照口径：PlanBench mini-suite 120 episodes；与只看 outcome 的 Agent 比较，TAPO 保持 joint success 1.0000，并新增 360 个 transition targets、预测准确率 1.0000。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 复用 rollout 学下一观察，为什么能增加训练信号却不必增加部署推理步骤？ 每次环境转移已含状态、动作和下一观察，训练侧在共享骨干上加入预测目标即可利用它，无需再采专家或新 rollout。部署仍执行原策略，不要求显式调用预测器；辅助目标改善是否转成任务收益仍需对照，能预测反馈不等于会选好动作。 例如执行 ls 已得到目录列表，可把它用于训练状态转移预测；上线时仍直接选命令，不必每步先生成一份想象目录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-tapo-abc37e08" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cast" data-paper-title="CAST" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="CAST Agent University of Science and Technology of China 2026-07-28 把求解器状态价值的相邻差分变成 solver advantage，为稀疏结果奖励补充 turn 级 credit。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。没有复刻论文三类游戏的大规模 LLM RLVR；求解器准确，适合验证 credit assignment 而非模型能力。PlanBench mini-suite 的确定性最短路充当 solver，逐 turn 查询状态值并统计 credit update。  Agentic RL / turn-level credit Agent 交互策略学习：把轨迹反馈变成更新 solver 相邻状态价值差为什么能补充终局 outcome，而不是替代它？ 差值把状态向可解方向的变化转为局部信用，帮助识别长链中的关键一步；但 solver 估值可能不完美，局部改善也可能最终失败，所以保留任务结果优势作整体约束。训练侧价值接口若接触隐藏答案，必须与评测行动者的信息边界隔离。 例如一步约束化简让剩余问题更易解，可得到正局部信用；若后面写出无效结果，仍不能把整条轨迹当最终成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-cast-0c2b025a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seed" data-paper-title="SEED" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEED Agent Tsinghua University 2026-07-16 从已完成轨迹中反思出可复用 hindsight skill，再用 skill 条件前后的动作概率变化形成稠密 on-policy 蒸馏信号。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。使用确定性任务与结构化 skill，不执行视觉模型或大规模策略梯度训练。在 PlanBench mini-suite 中把成功/失败轨迹压缩为 hindsight skill，并记录 skill 数量、稠密 credit 更新和跨 episode 复用。  Agentic RL / hindsight skill Agent 交互策略学习：把轨迹反馈变成更新 用 hindsight skill 前后动作概率差，为什么是在原动作上蒸馏而不是复制新专家轨迹？ 技能由已完成轨迹反思得到，再对学生实际访问状态和动作比较条件概率，形成更稠密的局部学习信号。它利用事后知识解释原行为，不要求教师另走一条不同路线；部署不能携带同题未来答案，技能本身的错误也可能污染信号，需保留验证边界。 例如学生已执行一次目录检查，反思技能指出该检查有用，就评估有无技能时这条原动作的概率，而非换成教师另写的命令。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-seed-34cb6214" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:turn-opd" data-paper-title="TurnOPD" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TurnOPD Agent Academic author team 2026-07-07 用 probe 统计自适应决定 rollout 深度，并逐步把 token KL 预算迁移为 turn-normalized 监督。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。教师行为由确定性任务 oracle 提供；没有运行任务专用大模型教师。ScaleMCP mini-suite 中执行深度 probe、动态截断和 turn 归一化，记录节省的 rollout turns。  Agentic OPD / rollout budgeting Agent 交互策略学习：把轨迹反馈变成更新 为什么把 KL 监督按 turn 长度归一化，能改变长短回合的训练权重？ 纯 token 求和让冗长回合天然贡献更多损失，可能压过短但关键的决策。turn-normalized 监督先在回合内平均，再依据 probe 分配 rollout 深度，把有限教师预算聚焦到有信息的交互；这改变的是权重与采样合同，不代表更深或更多监督必然更好。 例如一句关键工具选择只有十 token，另一轮长解释有两百 token；按回合平均可减少仅由长度造成的二十倍权重差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-turn-opd-4aa539f6" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:steppo" data-paper-title="StepPO" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="StepPO Agent University of Science and Technology of China 2026-04-20 Agent 的自然决策单位是“观察—动作”的 environment step，token-level MDP 会让动作粒度和信用粒度错位。StepPO 将交互重写为 step-level MDP，在 step boundary 估值和做 GAE，并把 step 内 token ratio 聚合后再裁剪。 在 PlanBench mini 的每个环境动作边界执行 step value、step GAE 与 step sequence-ratio clip，并公开对应诊断计数。本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 action 是确定性工具计划，不含真实 LLM token generation；验证的是 step 对齐状态机而非论文规模的 agent 训练。  Step-aligned Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么 StepPO 先聚合一步内的 token ratio，再对 step ratio 裁剪？ 环境执行的是一整个动作，逐 token 独立裁剪与动作级概率变化并不相同。先把一步中 log ratio 平均并指数化，再在 step 边界估值与 GAE，使信用单位更接近环境转移；这不允许把工具观察算成动作 token，长度归一化也须保持一致。 例如一条 shell 命令拆成多个 token，环境只在命令完成后执行一次；应以这一步整体变化评价，而非让每个子词各自承担状态奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-steppo-4ceaabe2" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searl" data-paper-title="SEARL" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEARL Agent Shanghai AI Laboratory 2026-04-09 把工具和成功转移维护为图记忆；新 rollout 同时更新 policy 与图边权，形成经验池—检索—改进闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3400；方法特有操作有非零 telemetry。  策略—工具图共进化 Agent 交互策略学习：把轨迹反馈变成更新 图记忆与 policy 为什么都要随新 rollout 更新，而不能只固定一张工具关系图？ 新执行会揭示哪些工具转移可用、哪些失败，图边权应反映这些证据；策略同时学习怎样利用更新后的关系。固定图只能复用旧经验，可能限制后续探索，单更新图又不保证策略会读；两侧闭环仍需真实奖励，不能用预设成功边制造进步。 例如新任务发现某工具返回可直接喂给另一工具，图中新增转移后，策略也要学会选这条路线，而不是永远沿旧流程行动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-searl-fe3972b7" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:simula" data-paper-title="Reasoning-Driven Synthetic Data Generation and Evaluation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Reasoning-Driven Synthetic Data Generation and Evaluation Agent EPFL 2026-03-31 单纯扩写种子容易遗漏概念或坍缩到相似样本。Simula 先按因素建立分类树，再控制全局节点组合与局部场景；独立批判过滤样本，并通过批内相对评分校准复杂度。语义生成器与批判模型是决定质量的核心，本地接口不能用启发式替代后宣称复现。§2 与附录 B/C/E 完整实验成本过高，不复现（审查 DONE）。CPU 协议组件，当前验证为 L0 接口与公式检验。没有把固定回调称为 M3 推理，也没有宣称合成数据质量提升。完整实验成本过高，不复现（审查 DONE）。TaxonomyModels 显式提供因素、提案、树 critic 和层计划；GenerationModels 显式提供策略、场景、复杂化、生成、要求批判、修改及正反两个批判回调。它们可接真实提供方，但本轮 runner 使用的都是标明 fixture 的独立调用。  Agent 数据合成 分类树与独立批判 Agent 交互策略学习：把轨迹反馈变成更新 正确性批判和错误性批判为什么不是同一判断的简单重复？ 生成样本可能让单个审查器迎合表面合理性，分别问支持正确与识别错误提供互补筛选；接纳同时要求需求满足、正批判肯定及负批判否定。因素树控制覆盖，批内相对难度再校准复杂度，不能用规则替代语义批判后声称数据质量已验证。 例如题目看似完整却暗含互斥条件，正向审查可能略过，专门寻找错误的批判应暴露矛盾，而非仅重复一句“看起来不错”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-simula-9d7ce82b" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dmast" data-paper-title="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks Agent University of California, Berkeley 2026-03-04 DMAST 让防守 Agent 与攻击者共享同一 VLM 参数，以不同角色提示交互；先教师模仿，再用不改变目标动作的 oracle reasoning 做 SFT，最后进行共享策略自博弈 RL。改动不只是普通 GRPO：受攻击组中两个角色的原始终局奖励共同决定均值与方差，而成功样本的长度惩罚只进入优势分子。 完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。诊断让同一个微型神经策略处理两种角色，真实执行一次 SGD，并与独立直接公式核对值和梯度。L1 Stage-3 数值组件，diagnostic only，不是浏览器 Agent 能力或完整三阶段复现。完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。只保留 Stage-3 精确组统计与 token 目标；不生成攻击载荷、不访问网页、不加载 VLM、不训练 SFT 或 oracle。length_penalty 是外部提供的；  Agentic RL 共享策略对抗训练 Agent 交互策略学习：把轨迹反馈变成更新 为什么组均值方差用 raw reward，而成功长度罚只进入优势分子？ 长度罚旨在调节某条成功响应的信用，不应同时重定义全组基线尺度。受攻击组还联合攻击与防守角色的原始回报统计，若先减罚再白化，就改变双方比较与原算法；零方差组需排除，不能靠任意 epsilon 制造学习信号。 例如两条同样成功的响应一长一短，长度罚降低长者优势，但共同基线仍按原始任务回报计算，不能被长文本额外拖动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-dmast-279d6cde" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pearl" data-paper-title="PEARL" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PEARL Agent 中国科学院信息工程研究所 2026-01-28 多跳工具调用同时受工具幻觉、参数错误和长程规划薄弱影响。PEARL 的离线阶段用 trial-and-error 建立工具用法与失败条件；在线阶段把 Planner 与 Executor 解耦，用计划正确性、工具链与最终结果组成的密集 reward 进行 GRPO，而不是只依赖稀疏成功信号。 未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。PEARL 先离线探索工具的有效参数与失败条件，再用 planning-centric reward 和 GRPO 训练独立 Planner，把可靠执行与长程规划分开优化。实现离线候选计划探索、planning reward、组内选择更新、Planner/Executor 解耦和跨 episode 复用；未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。  规划强化学习 Agent 交互策略学习：把轨迹反馈变成更新 为什么 Planner 与 Executor 分开后，仍需要工具链与最终结果共同奖励？ 计划格式正确不保证工具存在、顺序可执行或答案成立，执行器也可能在合理计划下填错参数。离线试错先积累用法与失败条件，在线密集信号分别约束工具、顺序和结果，使规划能学到可执行结构；单个过程分高不能替代任务实际成功。 例如计划先查询订单再退款顺序正确，但订单 ID 错了仍会失败；奖励应同时反映工具链合理性与最终操作结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-pearl-a555b8b4" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent0" data-paper-title="Agent0" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent0 Agent University of North Carolina at Chapel Hill 2025-11-20 任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  零数据多 Agent Agent 交互策略学习：把轨迹反馈变成更新 多数投票为什么还必须接受任务 verifier 检查，而不能把一致答案直接当真？ 多个执行者可能共享同一错误先验，投票提高一致性却不提供独立事实保证。可验证任务用外部规则判断候选答案，课程再按当前能力边界升级；若生成器或投票器读取参考答案，训练闭环就变成泄漏，不能作为自主工具能力证据。 例如五名执行者都把单位换算错成同一数值，票数很高仍是错误；verifier 应按任务合同检查，而非按赞同人数决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent0-bc007c7f" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-r1" data-paper-title="Agent-R1" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-R1 Agent University of Science and Technology of China 2025-11-18 把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.9600。  Agentic RL 基础设施 Agent 交互策略学习：把轨迹反馈变成更新 把每次交互记录成独立 transition，为什么有助于切换 token 或 step 级信用？ 状态、动作和下一观察的边界被显式保存，优化器可选择在生成细节或环境步层面归因，而不把所有文本混成一段。可插拔上下文管理处理可见历史，但不能悄悄改变转移语义；工具结果属于环境，不能因统一记录就自动进入策略动作损失。 例如一次查询返回长表格，transition 仍只有一项实际查询动作；训练可按步给信用，或只对查询的生成 token 细分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent-r1-da1f3512" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mua-rl" data-paper-title="MUA-RL" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="MUA-RL Agent Meituan 2025-08-26 既有 tool-use RL 通常把用户请求视为固定输入，但真实用户会根据 Agent 回答不断修改需求。MUA-RL 将 LLM 模拟用户直接放入 rollout，Agent 在对话中澄清意图并调用真实 MCP/数据库工具；用户消息和工具结果不计入策略 loss，只用最终任务完成奖励鼓励探索。 保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；当前为确定性工具 mini-suite。本地模拟用户按任务上下文确定性揭示约束，工具实际返回 mini-suite 状态，但没有外部 LLM 用户或生产数据库。该实验验证交互与奖励边界，不复刻原模型规模。稳定指标见 omitted-agentic-rl-opd-seed42.json。  多轮用户 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 模拟用户消息为什么和工具结果一样，不应计算为 Agent 的策略 token loss？ 这些文本由环境侧用户策略或工具产生，Agent 无法直接选择它们，拿来监督会混淆动作与条件。把用户放进 rollout 能训练澄清与需求变化下的决策，但最终奖励应评价任务完成，而非奖励模型复述模拟用户；模拟分布也不等于真实用户全部行为。 例如用户中途把日期改到周五，Agent 应据此重排，而不被训练成自己生成“改到周五”这句用户话。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-mua-rl-ac5031c4" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-lightning" data-paper-title="Agent Lightning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent Lightning Agent Microsoft Research 2025-08-05 传统 Agent RL 常把所有上下文拼成单序列并与框架强耦合。Agent Lightning 将执行记录成统一 MDP transition，以 credit assignment 拆解轨迹，并采用训练/执行分离架构。 解耦 Agent 执行与 RL 训练，并将长交互轨迹拆成可归因的训练 transition。实现了执行/训练解耦、transition、环境 reward、credit update 与跨 episode 复用；本地更新的是受控 patch policy，不是对 LLM 参数执行 LightningRL。代码 Agent 的命令、编辑与测试形成 transition；测试退出码是真实 reward，失败时把 credit 归给 patch，并把正确修复按 bug family 写入可复用策略记忆。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新 训练与执行分离为什么不仅是把日志写到另一台机器？ 统一 transition 合同把框架行为转成可归因的 MDP 数据，训练侧据此计算回报与优势，执行侧可继续使用原有工具编排。若日志缺状态动作边界或混入环境 token，物理分离也无法得到正确策略更新；架构解耦不自动证明任何具体 Agent 已提升。 例如同一工具框架输出查询动作和结果，训练器只读取规范转移即可更新；不能把未经切分的整份聊天日志直接当动作序列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-agent-lightning-78a73390" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webagent-r1" data-paper-title="WebAgent-R1" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="WebAgent-R1 Agent University of Virginia 2025-05-22 网页交互会不断累积 HTML 和历史动作，单轮 GRPO 无法处理状态变化。WebAgent-R1 动态保留近期和任务相关上下文，并行采集完整多轮轨迹，再用 M-GRPO 根据最终成功奖励执行组内相对更新；论文同时强调行为克隆 warm-up 和长 CoT 初始化。 保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；当前使用确定性工具 mini-suite，不冒充 WebArena-Lite。本地环境返回确定性文本工具观测，没有浏览器 DOM、网页副作用或 Qwen/Llama 参数更新。因此只验证多轮 rollout、压缩和组内奖励路径。稳定指标见 omitted-agentic-rl-opd-seed42.json。  网页 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么多轮网页 GRPO 需要动态上下文，而不只是把单轮回答重复训练几次？ 网页状态会随点击、输入和跳转改变，后续动作必须看到真实最新页面及必要历史。完整多轮 rollout 才能把终局成功回报连到这些生成动作，动态保留控制 HTML 膨胀；行为克隆与初始化也影响探索，不能把一个组内优势公式当成完整网页交互训练。 例如点击登录后页面结构变化，下一步必须读取新表单；只反复训练最初截图上的答案，无法学会真实状态转换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-webagent-r1-938cd977" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gigpo" data-paper-title="GiGPO" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GiGPO Agent Nanyang Technological University 2025-05-16 多轮 Agent 的最终奖励稀疏，整条轨迹的 group relative advantage 无法判断哪个 environment step 做对了。GiGPO 先在完整轨迹组上计算 macro advantage，再按跨轨迹重复到达的 anchor state 建立 step group，计算 micro relative advantage。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。确定性任务没有跨轨迹真实环境 state 合流，使用共享计划步骤作为可审计 anchor-state 代理。在 PlanBench mini 中显式生成完整轨迹组与 step group，分别统计组间和组内优势、trajectory rollout 与 turn credit。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新 为什么 micro advantage 要在重复到达同一 anchor state 的动作间比较？ 不同状态的可选动作与剩余难度不同，直接比较回报会混入起点差异。共享锚状态提供更相近的局部条件，micro 信号补充整条轨迹 macro 优势；同状态后仍有随机续跑，局部差异不是无噪声因果值，也不能取代最终成功约束。 例如两条轨迹都站在锁门前，一条找钥匙、一条重复推门，才适合比较该处动作；不能拿已到终点的状态当同组对照。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-gigpo-7fac2585" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ragen" data-paper-title="RAGEN" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RAGEN Agent Northwestern 2025-04-24 单轮数学 RL 的优化单位是一次回答，而 Agent 要在随机环境中跨多轮决策。RAGEN 提出 StarPO，把 state、thinking、action 和 reward 组织成完整轨迹。论文还观察到 Echo Trap：reward 方差突然塌缩并伴随梯度尖峰。StarPO-S 通过轨迹过滤、critic baseline、梯度稳定和解耦 clipping 抑制这种自我强化的重复模式。 保真度：本地实现 StarPO-S 的 trajectory rollout、退化轨迹过滤、critic baseline、reasoning-aware reward、Echo Trap 探针和解耦 clipping 诊断。本地策略在确定性候选轨迹上选择计划，真实执行但不更新 LLM 参数；Echo Trap 是固定频率的可观测稳定性探针，不冒充论文训练曲线。未运行 WebShop 或原始游戏环境。稳定指标见 classic-agentic-rl-opd-seed42.json。  多轮 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 reward 方差塌缩为什么不一定说明策略已经稳定学会任务？ 策略可能陷入反复输出同类失败或僵化行为，回报缺变化伴随梯度尖峰就是 Echo Trap 的危险征兆。轨迹过滤、critic 基线和解耦 clipping 分别控制数据、估值与更新稳定性；稳定训练还需看真实任务表现，不能把低方差自动写成收敛成功。 例如所有 rollout 都重复同一无效命令，奖励全零且方差为零，数值看似一致，实际是探索崩溃而非能力已成熟。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-ragen-2a3a9785" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deepresearcher" data-paper-title="DeepResearcher" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="DeepResearcher Agent HKU 2025-04-04 把 search、browse、证据收集和带引用回答作为一条轨迹，用答案与引用联合奖励训练研究策略。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.5000；方法特有操作有非零 telemetry。  深度研究 RL Agent 交互策略学习：把轨迹反馈变成更新 答案奖励之外加 citation reward，为什么仍不能只按引用数量给分？ 引用的作用是把结论连到真实证据，数量多可能只是重复或无关链接。搜索、浏览与回答组成整条策略轨迹，联合目标应约束证据支持与正确答案，并惩罚无用查询；最终主张与来源的对应关系必须核对，调用一次浏览也不等于认真使用了证据。 例如回答含十个无关来源不应胜过两条直接支持结论的引用，否则策略会学习堆链接而不是完成研究取证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-deepresearcher-9b53178e" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:search-r1" data-paper-title="Search-R1" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Search-R1 Agent University of Illinois Urbana-Champaign 2025-03-12 普通 RAG 一次检索后再回答，无法让策略根据中间证据继续调整查询。Search-R1 把搜索引擎视为环境：模型可在 reasoning 中多次输出搜索动作，环境返回文档后继续推理。训练只对模型生成 token 计算 PPO/GRPO loss，检索结果 token 必须 mask，最终答案用简单 outcome reward 评分。 保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；使用确定性 ScaleMCP mini，不调用论文的 E5 索引或训练 Qwen。mini-suite 的检索结果是确定性的当前任务上下文，适合验证交错状态机和 loss mask；没有真实网页索引、Qwen 参数更新或七个 QA benchmark，因此成功率不能与论文 EM 比较。稳定指标见 classic-agentic-rl-opd-seed42.json。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 为什么检索结果 token 必须 mask，哪怕它们也在模型输入序列中？ 文档由搜索环境返回，不是策略采样的动作，给这些位置算 policy loss 会错误地训练模型生成外部证据。模型只对查询与推理回答等自身 token 负责，检索结果作为后续条件影响决策；多轮检索收益来自闭环调整，不能用静态一次 RAG 代替。 例如搜索返回“发布日期为周二”，训练不应把这句环境文本记作 Agent 的行为，而应更新它怎样查询和据证回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-search-r1-fce4d489" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loop" data-paper-title="LOOP" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="LOOP Agent Apple 2025-02-03 长程数字 Agent 的 rollout 昂贵，而传统 PPO 还要维护 value model。LOOP 把 PPO trust region 与 leave-one-out baseline 结合：无需 critic，可对同一批轨迹进行多次更新；逐 token importance ratio 只裁剪漂移 token，不丢弃整条长轨迹。 保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；当前是确定性交互 mini-suite，不是 AppWorld 32B 训练。本地真实执行多轨迹选择和统计更新，但没有 AppWorld、32B LLM 或梯度 checkpoint；mini-suite 满分只说明轨迹控制逻辑正确，不代表论文任务难度。  长时程 Agent RL Agent 交互策略学习：把轨迹反馈变成更新 leave-one-out baseline 为什么把当前轨迹自己排除？ 用其他同组结果作基线，减少把本条回报直接混进自身参照的影响，在无 critic 条件下形成相对优势。长 rollout 成本高，因此逐 token ratio 裁剪和复用同批更新有价值；但多次更新仍受策略漂移约束，不能无限重复把旧轨迹当新 on-policy 数据。 例如三条回报为一、一、零，第一条与另外两条平均比较，而不是用包含自身的整体均值；局部漂移 token 再单独裁剪。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<span id="paper-agent-research-loop-633efc7d" class="ar-learning-paper-anchor"></span>
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
