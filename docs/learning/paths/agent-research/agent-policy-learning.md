---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 交互策略学习：把轨迹反馈变成更新

[Agent](index.md) / 子主题导学 · 约 3 分钟 · 53 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 53 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond Agent Tsinghua University 2026-10-23 同一个环境观测可能经不同历史反复到达，直接按访问次数或 token 数平均会让循环轨迹主导教师介入判断。Frontier-OPD 先在轨迹内、再在轨迹间聚合有符号师生分歧，对不同状态选原历史代表；教师桥与学生续跑须通过同长窗口比较后才接纳，状态共享不能替代真实历史或任务成功评测。排名只寻找值得试验的节点。教师最多接管回合，再让学生继续回合。新窗口必须和原历史从同一位置开始的回合窗口比较；只有成功重放、非终止交接、完整有效续跑且师生 agreement 不下降，桥的教师响应才加入训练。 成本过高，不复现（审查 DONE）。本地排名和接纳诊断不复现上述分数。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  Agentic OPD / rollout budgeting 学习前沿与教师桥 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-frontier-opd-63269744">Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>同一个环境观测可能经不同历史反复到达，直接按访问次数或 token 数平均会让循环轨迹主导教师介入判断。Frontier-OPD 先在轨迹内、再在轨迹间聚合有符号师生分歧，对不同状态选原历史代表；教师桥与学生续跑须通过同长窗口比较后才接纳，状态共享不能替代真实历史或任务成功评测。排名只寻找值得试验的节点。教师最多接管回合，再让学生继续回合。新窗口必须和原历史从同一位置开始的回合窗口比较；只有成功重放、非终止交接、完整有效续跑且师生 agreement 不下降，桥的教师响应才加入训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。本地排名和接纳诊断不复现上述分数。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32802v1">原论文</a> · <a href="../../../../agent-research/2610.32802-frontier-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Asymmetric On-Policy Distillation Learns In-Context Exploration Agent University of Washington 2026-10-21 部分可观测任务中，专家知道隐藏目标，因而总能直接成功；只模仿专家，学生看不到“失败后如何继续搜索”的上下文。ASTEROID 让当前学生先探索，再在同一个隐藏任务下收集专家的完整成功轨迹。学生用自己的观察、动作和奖励历史预测专家动作，迭代扩大可学习的上下文长度。这不是把金标放入 Agent prompt，也不是固定离线行为克隆，更不应简化成只在学生当前状态上打单步标签的普通 DAgger。论文区分两种采样：固定 latent 的 BAMDP 使用跨 episode 上下文； 完整多环境与机器人实验：成本过高，不复现（审查 DONE）；这是生成式机制诊断，没有公开 benchmark split，也没有 validation 选模、test 能力对比或 evolve 晋级。本地状态：L1 核心机制组件，diagnostic only。本地真实训练一个微型因果 Transformer，保留论文 Algorithm 1 的 episode 级在策略上下文与教师轨迹监督；不宣称复现论文的探索能力、样本效率或机器人效果。完整多环境与机器人实验：成本过高，不复现（审查 DONE）；不自动重试、不阻塞审查。  Agent 训练与策略优化 在策略上下文蒸馏与部分可观测探索 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-asteroid-1bdda102">Asymmetric On-Policy Distillation Learns In-Context Exploration</h2>
<p class="ar-learning-card__meta">University of Washington · 论文公开：2026-10-21</p>
<p><strong>方法要点：</strong>部分可观测任务中，专家知道隐藏目标，因而总能直接成功；只模仿专家，学生看不到“失败后如何继续搜索”的上下文。ASTEROID 让当前学生先探索，再在同一个隐藏任务下收集专家的完整成功轨迹。学生用自己的观察、动作和奖励历史预测专家动作，迭代扩大可学习的上下文长度。这不是把金标放入 Agent prompt，也不是固定离线行为克隆，更不应简化成只在学生当前状态上打单步标签的普通 DAgger。论文区分两种采样：固定 latent 的 BAMDP 使用跨 episode 上下文；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整多环境与机器人实验：成本过高，不复现（审查 DONE）；这是生成式机制诊断，没有公开 benchmark split，也没有 validation 选模、test 能力对比或 evolve 晋级。本地状态：L1 核心机制组件，diagnostic only。本地真实训练一个微型因果 Transformer，保留论文 Algorithm 1 的 episode 级在策略上下文与教师轨迹监督；不宣称复现论文的探索能力、样本效率或机器人效果。完整多环境与机器人实验：成本过高，不复现（审查 DONE）；不自动重试、不阻塞审查。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30105v1">原论文</a> · <a href="../../../../agent-research/2610.30105-asteroid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution Agent Chinese University of Hong Kong 2026-10-11 静态或离线训练的技能库难以跟随策略进步，而技能增强教师也可能比学生更差。RSIPO从当前策略轨迹产生技能，以独立控制组与同初态重放测量技能收益，联合优化技能生成、RLVR和按经验贝叶斯可靠性加权的自蒸馏。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Table2：Qwen2.5-3B/7B、Qwen3-1.7B，150训练steps；ALFWorld每step16任务×8rollouts，最长50turns，每任务另4次初态重放与4096token技能生成；搜索每step128任务×8rollouts。之前还要GLM-5.2标注的技能SFT。多轮环境训练与教师评分在单卡预计长时间，未作本地测速；不下载或启动。  agentic-rl on-policy-self-distillation recursive-self-improvement Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-rsipo-71b84017">RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution</h2>
<p class="ar-learning-card__meta">Chinese University of Hong Kong · 论文公开：2026-10-11</p>
<p><strong>方法要点：</strong>静态或离线训练的技能库难以跟随策略进步，而技能增强教师也可能比学生更差。RSIPO从当前策略轨迹产生技能，以独立控制组与同初态重放测量技能收益，联合优化技能生成、RLVR和按经验贝叶斯可靠性加权的自蒸馏。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文Table2：Qwen2.5-3B/7B、Qwen3-1.7B，150训练steps；ALFWorld每step16任务×8rollouts，最长50turns，每任务另4次初态重放与4096token技能生成；搜索每step128任务×8rollouts。之前还要GLM-5.2标注的技能SFT。多轮环境训练与教师评分在单卡预计长时间，未作本地测速；不下载或启动。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15772">原论文</a> · <a href="../../../../reproductions/2610.15772-rsipo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Evo2: Evolving the Evolver through Weight-Harness Co-Evolution Agent University of Illinois Urbana-Champaign / Google DeepMind 2026-10-09 固定任务 executor，共享 Proposer/Reflector 编辑 harness；树搜索与跨分支 crossover 的执行反馈反过来训练 evolver。EvoTIDE 恢复有效编辑轨迹，先 SFT，再交错更新两个角色。事实来源：原文全文。 此处只是有边界的 GSM harness 机制诊断，非原 coding benchmark 复现或隔离 test 能力提升；当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为固定 executor 与初始可执行 harness；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evolution weight-harness-co-evolution dual-role-grpo Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-evo2-2bf44b34">Evo2: Evolving the Evolver through Weight-Harness Co-Evolution</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign / Google DeepMind · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>固定任务 executor，共享 Proposer/Reflector 编辑 harness；树搜索与跨分支 crossover 的执行反馈反过来训练 evolver。EvoTIDE 恢复有效编辑轨迹，先 SFT，再交错更新两个角色。事实来源：原文全文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>此处只是有边界的 GSM harness 机制诊断，非原 coding benchmark 复现或隔离 test 能力提升；当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为固定 executor 与初始可执行 harness；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13025">原论文</a> · <a href="../../../../reproductions/2610.13025-evo2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation Agent Renmin University of China 2026-10-08 LoGiC 从第二轮逐步删除推理，检查本轮及所有后续原动作的平均 token 对数似然变化，已接受删除继续影响后续上下文。成功轨迹压缩后用于 SFT；RL 屏蔽可删推理并监督提前闭合。原文四个 Agent 环境推理 token 分别减少 32.3%、80.2%、46.4%、62.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。动作似然、成功轨迹 SFT 与 cover-aware actor 梯度接口已实现。真实输入必须提供公开环境、修订与 reason/action/observation 训练轨迹；不能把 QA 解题行伪装成工具轨迹。评估 Agent 不读取参考动作。论文四环境完整 on-policy RL 尚未复测；其端到端能力结果仍缺。  Agentic RL 推理效率 跨轮信用分配 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-race-11c5fa7f">When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation</h2>
<p class="ar-learning-card__meta">Renmin University of China · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>LoGiC 从第二轮逐步删除推理，检查本轮及所有后续原动作的平均 token 对数似然变化，已接受删除继续影响后续上下文。成功轨迹压缩后用于 SFT；RL 屏蔽可删推理并监督提前闭合。原文四个 Agent 环境推理 token 分别减少 32.3%、80.2%、46.4%、62.0%，未报告线上 A/B。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。动作似然、成功轨迹 SFT 与 cover-aware actor 梯度接口已实现。真实输入必须提供公开环境、修订与 reason/action/observation 训练轨迹；不能把 QA 解题行伪装成工具轨迹。评估 Agent 不读取参考动作。论文四环境完整 on-policy RL 尚未复测；其端到端能力结果仍缺。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12061">原论文</a> · <a href="../../../../agent-research/2610.12061-race/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning Agent Tsinghua University 2026-10-02 Agent 长轨迹的终局奖励给每一步同样的全局优势，无法指出哪一步有用；GiGPO 等方法用相同锚状态的局部回报补充信用，但同一动作之后的随机路径也会改变回报。AdaStep 不另训 critic，而是看同组中不同动作解释了多少回报方差。动作间差异主导时信任局部信用；同动作内部差异主导时将局部修正压低，保留全局优势。 L1 统计机制诊断。L1 统计机制诊断。实现论文 Eq. (17)–(18) 的同锚状态、按动作分组的方差分解、稀疏组回退和最终优势组合；没有宣称完成 Agent 策略训练或原文任务评测。输入只包含策略 rollout 的任务 ID、状态键、动作、折扣回报和全局优势；分组键为任务 ID 与 anchor state，避免不同任务的同名状态互相污染。不读取金标答案或计划。这里未运行环境交互、Qwen 策略更新、ALFWorld/WebShop/ScienceWorld，也没有同预算的 GiGPO 对照。  Agentic RL 步骤信用分配 方差可靠性 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-adastep-2ac090d9">AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-10-02</p>
<p><strong>方法要点：</strong>Agent 长轨迹的终局奖励给每一步同样的全局优势，无法指出哪一步有用；GiGPO 等方法用相同锚状态的局部回报补充信用，但同一动作之后的随机路径也会改变回报。AdaStep 不另训 critic，而是看同组中不同动作解释了多少回报方差。动作间差异主导时信任局部信用；同动作内部差异主导时将局部修正压低，保留全局优势。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>L1 统计机制诊断。L1 统计机制诊断。实现论文 Eq. (17)–(18) 的同锚状态、按动作分组的方差分解、稀疏组回退和最终优势组合；没有宣称完成 Agent 策略训练或原文任务评测。输入只包含策略 rollout 的任务 ID、状态键、动作、折扣回报和全局优势；分组键为任务 ID 与 anchor state，避免不同任务的同名状态互相污染。不读取金标答案或计划。这里未运行环境交互、Qwen 策略更新、ALFWorld/WebShop/ScienceWorld，也没有同预算的 GiGPO 对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03223">原论文</a> · <a href="../../../../agent-research/2610.03223-adastep/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents Agent Southeast University 2026-10-02 终端 Agent 通常只拿到任务结束后的 verifier 奖励。GRPO 把同一条轨迹的优势分给所有生成 token，无法区分真正生成答案的命令、为其提供数据的读取，以及后来被覆盖或无关的操作。DepGPO 从执行记录构造命令依赖图：文件读取连向该文件尚未覆盖的写入者，可信的 stdout 复用也形成边；再从 verifier 实际检查的文件、端口和进程向后追溯。 L1 机制诊断。L1 机制诊断。这里实现了论文的记录级读写依赖、相关写入与支持性读取信用，以及步级/令牌级优势归一化；尚未接入真实终端 tracer、verifier 执行或 Qwen 策略训练，不能把机制指标当成任务成功率。机制回执只包含四条手工结构化命令：支持读取、间接写入、最终写入、无关写入。测试还覆盖覆盖写不自动建立依赖、写入记录分母、最短路径、回退、负优势与 token 数不等时的均值守恒。这不是 Terminal-Bench、真实 Qwen 训练或多 seed 能力比较。  Agentic RL 终端命令依赖 步骤信用分配 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-depgpo-58f41b1f">Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents</h2>
<p class="ar-learning-card__meta">Southeast University · 论文公开：2026-10-02</p>
<p><strong>方法要点：</strong>终端 Agent 通常只拿到任务结束后的 verifier 奖励。GRPO 把同一条轨迹的优势分给所有生成 token，无法区分真正生成答案的命令、为其提供数据的读取，以及后来被覆盖或无关的操作。DepGPO 从执行记录构造命令依赖图：文件读取连向该文件尚未覆盖的写入者，可信的 stdout 复用也形成边；再从 verifier 实际检查的文件、端口和进程向后追溯。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>L1 机制诊断。L1 机制诊断。这里实现了论文的记录级读写依赖、相关写入与支持性读取信用，以及步级/令牌级优势归一化；尚未接入真实终端 tracer、verifier 执行或 Qwen 策略训练，不能把机制指标当成任务成功率。机制回执只包含四条手工结构化命令：支持读取、间接写入、最终写入、无关写入。测试还覆盖覆盖写不自动建立依赖、写入记录分母、最短路径、回退、负优势与 token 数不等时的均值守恒。这不是 Terminal-Bench、真实 Qwen 训练或多 seed 能力比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03634">原论文</a> · <a href="../../../../agent-research/2610.03634-depgpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents Agent University of Chinese Academy of Sciences 2026-09-28 按 rubric 的历史已接受支持计算本次工具结果带来的新增或部分支持，再与最终结果优势结合，避免重复证据反复得分。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent RL 过程信用分配 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-dr-credit-775af357">Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents</h2>
<p class="ar-learning-card__meta">University of Chinese Academy of Sciences · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>按 rubric 的历史已接受支持计算本次工具结果带来的新增或部分支持，再与最终结果优势结合，避免重复证据反复得分。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34296">原论文</a> · <a href="../../../../agent-research/2609.34296-dr-credit/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents Agent Beihang University 2026-09-28 稀疏终局奖励难以定位长轨迹中的关键动作。GraphHCA 把 rollout 合并为状态转移图，以成功/失败终态为边界解折扣固定点，再把相邻状态的对数势能差分配给每一步，并在同状态动作间标准化。 复现级别：L1 无 gold 核心机制。复现级别：L1 无 gold 核心机制。本地从采样轨迹图、动作和终局结果计算固定点势能与逐步优势；不读取参考答案或计划。当前未训练语言模型，也未把 GraphHCA 注册为 Evolve 算子。只有统一控制器能采样真实轨迹、执行该 estimator 并隔离验证策略更新后才算正式接入。graphhca_credit 只接受 Transition 和 success 布尔值；汇总实验见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Agentic RL 信用分配 轨迹图 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-graphhca-933790a0">GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>稀疏终局奖励难以定位长轨迹中的关键动作。GraphHCA 把 rollout 合并为状态转移图，以成功/失败终态为边界解折扣固定点，再把相邻状态的对数势能差分配给每一步，并在同状态动作间标准化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 无 gold 核心机制。复现级别：L1 无 gold 核心机制。本地从采样轨迹图、动作和终局结果计算固定点势能与逐步优势；不读取参考答案或计划。当前未训练语言模型，也未把 GraphHCA 注册为 Evolve 算子。只有统一控制器能采样真实轨迹、执行该 estimator 并隔离验证策略更新后才算正式接入。graphhca_credit 只接受 Transition 和 success 布尔值；汇总实验见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35084">原论文</a> · <a href="../../../../agent-research/2609.35084-graphhca/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning Agent ShanghaiTech University 2026-09-16 把多轮轨迹表示为轮级依赖 DAG，依次执行叶节点裁剪、严格合并和宽松合并，减少冗余消息同时保留最终答案依赖。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。  轨迹精炼 Agent 微调 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-dependency-refinement-97ad396d">Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning</h2>
<p class="ar-learning-card__meta">ShanghaiTech University · 论文公开：2026-09-16</p>
<p><strong>方法要点：</strong>把多轮轨迹表示为轮级依赖 DAG，依次执行叶节点裁剪、严格合并和宽松合并，减少冗余消息同时保留最终答案依赖。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18417">原论文</a> · <a href="../../../../agent-research/2609.18417-dependency-refinement/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning Agent Harbin Institute of Technology / Alibaba Cloud 2026-09-12 联合 learnability、transferability 与探索 bonus 分配多 harness 训练预算。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行在线 harness 调度；没有进行大模型 RL。本地执行在线 harness 调度；没有进行大模型 RL。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent RL Harness 调度 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-harness-bandit-ffd58529">HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Harbin Institute of Technology / Alibaba Cloud · 论文公开：2026-09-12</p>
<p><strong>方法要点：</strong>联合 learnability、transferability 与探索 bonus 分配多 harness 训练预算。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行在线 harness 调度；没有进行大模型 RL。本地执行在线 harness 调度；没有进行大模型 RL。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13739">原论文</a> · <a href="../../../../agent-research/2609.13739-harness-bandit/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks Agent National University of Singapore / Tencent 2026-09-09 TITO 使用 rollout 实际采样 token id 训练，turn boundary repair 修正漂移，R3 重放 MoE 路由选择。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent RL 长程终端任务 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-t1-terminal-rl-406c9b27">T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks</h2>
<p class="ar-learning-card__meta">National University of Singapore / Tencent · 论文公开：2026-09-09</p>
<p><strong>方法要点：</strong>TITO 使用 rollout 实际采样 token id 训练，turn boundary repair 修正漂移，R3 重放 MoE 路由选择。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11042">原论文</a> · <a href="../../../../agent-research/2609.11042-t1-terminal-rl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents Agent New York University 2026-09-03 多 Harness RL 同时改变了执行环境多样性和 GRPO 的分组边界，难以判断增益来源。论文冻结相同 task-harness 轨迹，只比较组内和跨 harness advantage，并用训练中未见的最小 harness 审计能力是否真正迁移。 复现级别：CPU 分组信用与可微训练算子。复现级别：CPU 分组信用与可微训练算子。在相同 rollout 上计算 task×harness 与 task 两种标准化优势；尚不包含真实编码 Agent 的 held-out harness 迁移实验。真实 coding harness、Qwen3-8B RL 和 sealed oracle 均未在本地复刻；该实现用于防止未来 Evolve 实验把 harness 差异误报为模型能力。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Multi-harness RL audit Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-multi-harness-rl-66c31df3">What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents</h2>
<p class="ar-learning-card__meta">New York University · 论文公开：2026-09-03</p>
<p><strong>方法要点：</strong>多 Harness RL 同时改变了执行环境多样性和 GRPO 的分组边界，难以判断增益来源。论文冻结相同 task-harness 轨迹，只比较组内和跨 harness advantage，并用训练中未见的最小 harness 审计能力是否真正迁移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：CPU 分组信用与可微训练算子。复现级别：CPU 分组信用与可微训练算子。在相同 rollout 上计算 task×harness 与 task 两种标准化优势；尚不包含真实编码 Agent 的 held-out harness 迁移实验。真实 coding harness、Qwen3-8B RL 和 sealed oracle 均未在本地复刻；该实现用于防止未来 Evolve 实验把 harness 差异误报为模型能力。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04518">原论文</a> · <a href="../../../../agent-research/2609.04518-multi-harness-rl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents Agent Huawei Technologies Co., Ltd 2026-08-27 论文把 Agent 数据统一表示为：环境、任务、交互轨迹与可选 verifier。Accuracy 先限定可信支持集，Complexity 相对指定学习者校准难度，Diversity 再控制环境、任务和行为覆盖。 复现级别：框架可执行化 mini-suite。复现级别：框架可执行化 mini-suite。论文是综述/统一框架；本地把三道约束实现为数据准入门。这是框架的可执行准入合同，不声称复刻某个训练模型或公开 benchmark SOTA。planbench-mini、120 episodes：joint success 1.0000、average cost 0.3700，另记录 accuracy gates、complexity calibration 和 diversity accept/reject。指标见 metrics/planbench-mini-seed42.json。  Agent 数据质量 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-ace-data-9a8b6ddd">What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents</h2>
<p class="ar-learning-card__meta">Huawei Technologies Co., Ltd · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>论文把 Agent 数据统一表示为：环境、任务、交互轨迹与可选 verifier。Accuracy 先限定可信支持集，Complexity 相对指定学习者校准难度，Diversity 再控制环境、任务和行为覆盖。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：框架可执行化 mini-suite。复现级别：框架可执行化 mini-suite。论文是综述/统一框架；本地把三道约束实现为数据准入门。这是框架的可执行准入合同，不声称复刻某个训练模型或公开 benchmark SOTA。planbench-mini、120 episodes：joint success 1.0000、average cost 0.3700，另记录 accuracy gates、complexity calibration 和 diversity accept/reject。指标见 metrics/planbench-mini-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27260">原论文</a> · <a href="../../../../agent-research/2608.27260-ace-data/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AHEAD: Agentic Hints for Effective Agent Development Agent AWS AI Labs / Purdue University 2026-08-25 轨迹级 GRPO 给所有步骤同一 advantage；统一 privileged information 又浪费在普通步骤上。AHEAD 先分析失败轨迹定位关键错误：所有步骤的 teacher 都看到环境反馈，只有错误步骤额外看到 LLM corrective hint；teacher/student log-prob gap 被有界地注入 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。普通步骤只用环境反馈，错误步骤再追加 corrective hint，并生成稠密信用。mini-suite 使用确定性错误位置验证 step-aware PI 分流；未运行 LLM analyzer、Qwen、真实 GRPO 或三个原始 benchmark。PlanBench-mini 120 episodes：24 个 error-step hint、360 个 dense-credit 更新，joint success 1.0000，平均成本 0.6160。  环境反馈提示训练 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-ahead-17c82764">AHEAD: Agentic Hints for Effective Agent Development</h2>
<p class="ar-learning-card__meta">AWS AI Labs / Purdue University · 论文公开：2026-08-25</p>
<p><strong>方法要点：</strong>轨迹级 GRPO 给所有步骤同一 advantage；统一 privileged information 又浪费在普通步骤上。AHEAD 先分析失败轨迹定位关键错误：所有步骤的 teacher 都看到环境反馈，只有错误步骤额外看到 LLM corrective hint；teacher/student log-prob gap 被有界地注入 GRPO advantage。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。普通步骤只用环境反馈，错误步骤再追加 corrective hint，并生成稠密信用。mini-suite 使用确定性错误位置验证 step-aware PI 分流；未运行 LLM analyzer、Qwen、真实 GRPO 或三个原始 benchmark。PlanBench-mini 120 episodes：24 个 error-step hint、360 个 dense-credit 更新，joint success 1.0000，平均成本 0.6160。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24114">原论文</a> · <a href="../../../../agent-research/2608.24114-ahead/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction Agent Renmin University of China 2026-08-25 SPO 用单 rollout 和持久 prompt value 避免等待 sibling，但 completion 顺序会污染历史，而且 trajectory whitening 与 token-mean actor loss 的测度不一致。SPO++ 按生成策略事件组织证据、dispatch 时冻结 baseline，并用动作 token 数加权标准化 advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每次 dispatch 冻结 prompt value，并按 action-token measure 消费 advantage。确定性 mini-suite 验证事件时间状态与测度对齐；未运行异步 Qwen3.5、ALFWorld 或 Math-TIR 训练。PlanBench-mini 120 episodes：joint success 1.0000，平均成本 0.6400，执行 120 次冻结 value 与 360 个 action-token measure 更新。  异步单流 Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-spo-plus-plus-c1491ed7">SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction</h2>
<p class="ar-learning-card__meta">Renmin University of China · 论文公开：2026-08-25</p>
<p><strong>方法要点：</strong>SPO 用单 rollout 和持久 prompt value 避免等待 sibling，但 completion 顺序会污染历史，而且 trajectory whitening 与 token-mean actor loss 的测度不一致。SPO++ 按生成策略事件组织证据、dispatch 时冻结 baseline，并用动作 token 数加权标准化 advantage。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每次 dispatch 冻结 prompt value，并按 action-token measure 消费 advantage。确定性 mini-suite 验证事件时间状态与测度对齐；未运行异步 Qwen3.5、ALFWorld 或 Math-TIR 训练。PlanBench-mini 120 episodes：joint success 1.0000，平均成本 0.6400，执行 120 次冻结 value 与 360 个 action-token measure 更新。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24870">原论文</a> · <a href="../../../../agent-research/2608.24870-spo-plus-plus/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning Agent Baidu 2026-08-24 Hint-based Agent RL 保留专家轨迹前缀再让策略探索，但固定深度忽略任务难度，逐样本 probe 又浪费 rollout。Agent-G² 从已有 policy rollout 按难度簇估计 guidance band 的中心和方差，对每个任务采样不同前缀深度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每个任务从在线更新的高斯分布采样专家前缀深度，不额外执行 probe rollout。mini-suite 验证按任务簇在线估计、Gaussian sampling 和专家前缀/策略续写的控制流；没有运行 Qwen2.5、ALFWorld/WebShop 或真实 GRPO。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，在线采样 guidance 120 次，平均成本 0.8253。指标见 metrics/planbench-mini-seed42.json。  高斯 guidance Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-agent-g2-1fe5ec6c">Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Baidu · 论文公开：2026-08-24</p>
<p><strong>方法要点：</strong>Hint-based Agent RL 保留专家轨迹前缀再让策略探索，但固定深度忽略任务难度，逐样本 probe 又浪费 rollout。Agent-G² 从已有 policy rollout 按难度簇估计 guidance band 的中心和方差，对每个任务采样不同前缀深度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。每个任务从在线更新的高斯分布采样专家前缀深度，不额外执行 probe rollout。mini-suite 验证按任务簇在线估计、Gaussian sampling 和专家前缀/策略续写的控制流；没有运行 Qwen2.5、ALFWorld/WebShop 或真实 GRPO。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，在线采样 guidance 120 次，平均成本 0.8253。指标见 metrics/planbench-mini-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23318">原论文</a> · <a href="../../../../agent-research/2608.23318-agent-g2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces Agent Microsoft / POSTECH 2026-08-24 长任务中 prompt、tool configuration 和 middleware 的小错误会累积，而人工调 harness 成本高。AutoSaddler 把 harness 当代码：从 mini-batch 失败 trace 做深度诊断，生成有边界的结构化 patch，在同 batch 检查因果效果，再用 dev set 选更新并写入 EvoDAG，形成可持续版本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际执行深度失败诊断、结构化 patch、局部/held-out 验证和 durable harness 更新。没有运行 GAIA2、SWE-Bench Pro、Terminal-Bench 2.0 或论文的生产 harness；本地只验证优化循环、验证边界和 durable reuse。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，12 次 failure diagnosis 与 durable update、108 次复用，平均成本 0.5440。  Harness 自动优化 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-autosaddler-3e805f29">AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces</h2>
<p class="ar-learning-card__meta">Microsoft / POSTECH · 论文公开：2026-08-24</p>
<p><strong>方法要点：</strong>长任务中 prompt、tool configuration 和 middleware 的小错误会累积，而人工调 harness 成本高。AutoSaddler 把 harness 当代码：从 mini-batch 失败 trace 做深度诊断，生成有边界的结构化 patch，在同 batch 检查因果效果，再用 dev set 选更新并写入 EvoDAG，形成可持续版本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际执行深度失败诊断、结构化 patch、局部/held-out 验证和 durable harness 更新。没有运行 GAIA2、SWE-Bench Pro、Terminal-Bench 2.0 或论文的生产 harness；本地只验证优化循环、验证边界和 durable reuse。PlanBench-mini、120 episodes、seed 42：joint success 1.0000，12 次 failure diagnosis 与 durable update、108 次复用，平均成本 0.5440。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23041">原论文</a> · <a href="../../../../agent-research/2608.23041-autosaddler/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization Agent University of Science and Technology of China 2026-08-21 外部技能检索有上下文开销，完全内化又失去按任务选择能力；按整条轨迹成功率硬切阶段还无法判断某一个动作是否真正受益。AUSO 先用 skill-conditioned teacher 内化通用技能，再进行 outcome-driven exploration，最后对每个动作比较有技能和无技能策略的 JSD，以有界权重调整 GRPO advantage。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行技能内化、无技能/有技能动作分布 JSD、bounded utilization weight 和复用阶段切换。未运行 ALFWorld/WebShop/SearchQA、大模型 token rollout 或完整 GRPO；确定性 mini-suite 验证 progressive lifecycle、JSD 信息增益和 bounded reweighting 的控制流，不把成本代理指标冒充论文成功率。本地对照口径：基线为同一 PlanBench-mini、120 episodes 的 SkillRise；  动作级技能优化 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-auso-a7af1bb4">AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-08-21</p>
<p><strong>方法要点：</strong>外部技能检索有上下文开销，完全内化又失去按任务选择能力；按整条轨迹成功率硬切阶段还无法判断某一个动作是否真正受益。AUSO 先用 skill-conditioned teacher 内化通用技能，再进行 outcome-driven exploration，最后对每个动作比较有技能和无技能策略的 JSD，以有界权重调整 GRPO advantage。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行技能内化、无技能/有技能动作分布 JSD、bounded utilization weight 和复用阶段切换。未运行 ALFWorld/WebShop/SearchQA、大模型 token rollout 或完整 GRPO；确定性 mini-suite 验证 progressive lifecycle、JSD 信息增益和 bounded reweighting 的控制流，不把成本代理指标冒充论文成功率。本地对照口径：基线为同一 PlanBench-mini、120 episodes 的 SkillRise；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21292">原论文</a> · <a href="../../../../agent-research/2608.21292-auso/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning Agent Xiamen University 2026-08-20 同一自回归骨干在不同因果边界输出 policy/value，结合 PPO、on-policy SARSA 和 trajectory GAE。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-sapo-b38c3177">SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Xiamen University · 论文公开：2026-08-20</p>
<p><strong>方法要点：</strong>同一自回归骨干在不同因果边界输出 policy/value，结合 PPO、on-policy SARSA 和 trajectory GAE。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19842">原论文</a> · <a href="../../../../agent-research/2608.19842-sapo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training Agent Adelaide University 2026-08-19 把多轮 rollout 组织成稀疏反向树，按时间逆序更新 turn，令决策与下游 continuation 保持 on-policy。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL credit assignment Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-rtpo-1c108353">RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training</h2>
<p class="ar-learning-card__meta">Adelaide University · 论文公开：2026-08-19</p>
<p><strong>方法要点：</strong>把多轮 rollout 组织成稀疏反向树，按时间逆序更新 turn，令决策与下游 continuation 保持 on-policy。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18682">原论文</a> · <a href="../../../../agent-research/2608.18682-rtpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SPADE: Self-Play in Adaptive Synthetic Executable Environments Agent University of Washington 2026-08-19 同一 LLM 分饰环境设计者和推理 Agent，以有/无 privileged hint 的 regret 学习能力边界上的可执行环境。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 环境生成 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-spade-5fdace60">SPADE: Self-Play in Adaptive Synthetic Executable Environments</h2>
<p class="ar-learning-card__meta">University of Washington · 论文公开：2026-08-19</p>
<p><strong>方法要点：</strong>同一 LLM 分饰环境设计者和推理 Agent，以有/无 privileged hint 的 regret 学习能力边界上的可执行环境。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19197">原论文</a> · <a href="../../../../agent-research/2608.19197-spade/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs Agent Xiamen University 2026-08-18 在成功轨迹内同时比较 trajectory turn 数和单 turn response 长度，形成 coarse-to-fine planning advantages。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 规划 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-planpo-5fac2579">PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs</h2>
<p class="ar-learning-card__meta">Xiamen University · 论文公开：2026-08-18</p>
<p><strong>方法要点：</strong>在成功轨迹内同时比较 trajectory turn 数和单 turn response 长度，形成 coarse-to-fine planning advantages。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17289">原论文</a> · <a href="../../../../agent-research/2608.17289-planpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents Agent Authors did not disclose affiliation 2026-08-17 无需成功 anchor，从每个状态转移的 Evidence、Execution、Invalidity rubric 构造基础和 breakthrough reward。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  Agentic RL 过程奖励 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-trca-ae92667a">TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents</h2>
<p class="ar-learning-card__meta">Authors did not disclose affiliation · 论文公开：2026-08-17</p>
<p><strong>方法要点：</strong>无需成功 anchor，从每个状态转移的 Evidence、Execution、Invalidity rubric 构造基础和 breakthrough reward。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.16156">原论文</a> · <a href="../../../../agent-research/2608.16156-trca/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks Agent Capital One AI Foundations 2026-08-11 长程工具 Agent 的 on-policy rollout 同时受环境状态、长上下文和训练显存限制。SinkFlex-RL 把 Gymnasium 双控制环境、VERL 风格数据流、无 value model 的 GRPO 与 sink-aware FlexAttention 组合，causal / sliding-window mask 下仍保留模型特有 sink scaling。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行 sink 保留、causal sliding window 和无 critic 的 group-relative 更新路径；未声称复刻 CUDA FlexAttention kernel。未复刻论文的 MoE checkpoint、VERL 集群、τ²-Bench 全环境或 GPU kernel 显存曲线；mini-suite 验证状态保留规则与 RL 控制流，GPU 性能数字仅引用原文。ScaleMCP mini-suite 120 episodes：joint success 1.0、average cost 0.67；  Agentic RL / efficient long context Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-sinkflex-rl-6bf5fe2a">Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks</h2>
<p class="ar-learning-card__meta">Capital One AI Foundations · 论文公开：2026-08-11</p>
<p><strong>方法要点：</strong>长程工具 Agent 的 on-policy rollout 同时受环境状态、长上下文和训练显存限制。SinkFlex-RL 把 Gymnasium 双控制环境、VERL 风格数据流、无 value model 的 GRPO 与 sink-aware FlexAttention 组合，causal / sliding-window mask 下仍保留模型特有 sink scaling。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际执行 sink 保留、causal sliding window 和无 critic 的 group-relative 更新路径；未声称复刻 CUDA FlexAttention kernel。未复刻论文的 MoE checkpoint、VERL 集群、τ²-Bench 全环境或 GPU kernel 显存曲线；mini-suite 验证状态保留规则与 RL 控制流，GPU 性能数字仅引用原文。ScaleMCP mini-suite 120 episodes：joint success 1.0、average cost 0.67；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10357">原论文</a> · <a href="../../../../agent-research/2608.10357-sinkflex-rl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="ResidencyRL: Reinforcement Learning in Simulated Clinical Environments Agent Google DeepMind 2026-08-07 静态知识题不能覆盖主动询问、工具调用及长程决策。论文通过场景生成、带信息不对称的模拟环境、按维度隔离的裁判和GRPO组成完整训练链路；隐藏参考信息只属于环境/裁判，不能直接暴露给被评估策略。原文§3 成本过高，不复现（审查 DONE）。原配置依赖内部Gemini策略训练及独立模拟/裁判调用，使用49,870个常规场景、5,000个历史询问场景和2,583个对抗场景；每条轨迹可达60轮对话及8次工具调用。原文§3.4  多轮 Agent RL 多轮模拟与结构奖励 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-residency-rl-21b2b4df">ResidencyRL: Reinforcement Learning in Simulated Clinical Environments</h2>
<p class="ar-learning-card__meta">Google DeepMind · 论文公开：2026-08-07</p>
<p><strong>方法要点：</strong>静态知识题不能覆盖主动询问、工具调用及长程决策。论文通过场景生成、带信息不对称的模拟环境、按维度隔离的裁判和GRPO组成完整训练链路；隐藏参考信息只属于环境/裁判，不能直接暴露给被评估策略。原文§3</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。原配置依赖内部Gemini策略训练及独立模拟/裁判调用，使用49,870个常规场景、5,000个历史询问场景和2,583个对抗场景；每条轨迹可达60轮对话及8次工具调用。原文§3.4</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07418v1">原论文</a> · <a href="../../../../agent-research/2608.07418-residency-rl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="AgentOPSD Agent Tsinghua University 2026-08-06 轨迹奖励难定位少数关键决策。AgentOPSD 把 privileged replay 的 token teacher/student log-prob gap 聚合成 turn evidence，再在 log-odds 空间递归更新成功信念，以相邻信念修订量识别 pivotal turn。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现逐 turn evidence、递归 log-odds belief、pivotal revision 和 critic-free policy update。  递归 turn 信用 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-agent-opsd-6c6325b8">AgentOPSD</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>轨迹奖励难定位少数关键决策。AgentOPSD 把 privileged replay 的 token teacher/student log-prob gap 聚合成 turn evidence，再在 log-odds 空间递归更新成功信念，以相邻信念修订量识别 pivotal turn。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现逐 turn evidence、递归 log-odds belief、pivotal revision 和 critic-free policy update。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05987">原论文</a> · <a href="../../../../agent-research/2608.05987-agent-opsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Contextual Information Policy Optimization for Search Agents Agent Beihang University 2026-08-06 主题：搜索 Agent RL。只奖励最终答案会让检索退化成确认偏见。CIPO 识别受外部证据影响的后续动作，给予 dense turn credit，并与全局 outcome reward 联合优化。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索 Agent RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-cipo-5f899139">Contextual Information Policy Optimization for Search Agents</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>主题：搜索 Agent RL。只奖励最终答案会让检索退化成确认偏见。CIPO 识别受外部证据影响的后续动作，给予 dense turn credit，并与全局 outcome reward 联合优化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索 Agent RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06128">原论文</a> · <a href="../../../../agent-research/2608.06128-cipo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EnvACE Agent Shanghai Jiao Tong 2026-08-06 EnvACE 不另训 world model，而让同一个 agent policy 在真实 act 之间切换到 rehearsal role，自行预测下一 observation；训练时分别为 acting 与 rehearsal 轨迹计算 group-relative advantage，避免两种奖励尺度互相污染，测试时可用少量私有 rehearsal 扩展规划。 Fidelity：核心机制复现。同一策略交替 act/rehearse，rehearsal observation 仅作私有规划状态，并执行 role-wise group advantage。确定性 mini-suite 验证状态路由与计数，不等同于论文浏览器/工具环境和大模型 RL 训练。PlanBench mini-suite 120 episodes：joint success 1.0000，执行 360 次 world rehearsal、720 次 role-wise advantage update；real_tool_responses=0，确保预测 observation 没被伪装成真实环境反馈。  环境 rehearsal / Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-envace-95e34f1b">EnvACE</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>EnvACE 不另训 world model，而让同一个 agent policy 在真实 act 之间切换到 rehearsal role，自行预测下一 observation；训练时分别为 acting 与 rehearsal 轨迹计算 group-relative advantage，避免两种奖励尺度互相污染，测试时可用少量私有 rehearsal 扩展规划。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。同一策略交替 act/rehearse，rehearsal observation 仅作私有规划状态，并执行 role-wise group advantage。确定性 mini-suite 验证状态路由与计数，不等同于论文浏览器/工具环境和大模型 RL 训练。PlanBench mini-suite 120 episodes：joint success 1.0000，执行 360 次 world rehearsal、720 次 role-wise advantage update；real_tool_responses=0，确保预测 observation 没被伪装成真实环境反馈。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06197">原论文</a> · <a href="../../../../agent-research/2608.06197-envace/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents Agent University of Illinois Urbana–Champaign / Meta AI 2026-08-05 主题：Harness policy RL。把 Belief、Progress、Experience 暴露为策略可操作的外部状态；先 SFT 学会 harness action，再以成本感知 GRPO 学习何时读写和合并。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness policy RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness policy RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-evoharness-rl-68a7cfc6">EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana–Champaign / Meta AI · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>主题：Harness policy RL。把 Belief、Progress、Experience 暴露为策略可操作的外部状态；先 SFT 学会 harness action，再以成本感知 GRPO 学习何时读写和合并。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness policy RL 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05446">原论文</a> · <a href="../../../../agent-research/2608.05446-evoharness-rl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="OCSD Agent Nanjing University 2026-08-05 直接重放未来 observation 时，token 分数变化同时来自观测信息和重放脚手架。OCSD 构造结构完全匹配的 Full 与 Observation-Ablated 两个 replay，仅以二者残差调制高不确定 step 的 GRPO 更新。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。执行 full/observation-ablated matched replay、residual calibration 和 turn-level credit。  观测校准蒸馏 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-ocsd-b0061afd">OCSD</h2>
<p class="ar-learning-card__meta">Nanjing University · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>直接重放未来 observation 时，token 分数变化同时来自观测信息和重放脚手架。OCSD 构造结构完全匹配的 Full 与 Observation-Ablated 两个 replay，仅以二者残差调制高不确定 step 的 GRPO 更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。执行 full/observation-ablated matched replay、residual calibration 和 turn-level credit。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04788">原论文</a> · <a href="../../../../agent-research/2608.04788-ocsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="State2State: Environment-Derived Mid-Training for LLM Agents Agent Tsinghua University AIR / Alibaba Group 2026-08-05 主题：环境派生中训练。从环境探索自动采样起点与目标状态，用规则化状态匹配做 verifier，形成无需人工任务与专家轨迹的可扩展 mid-training。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的环境派生中训练算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  环境派生中训练 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-state2state-baaabd4d">State2State: Environment-Derived Mid-Training for LLM Agents</h2>
<p class="ar-learning-card__meta">Tsinghua University AIR / Alibaba Group · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>主题：环境派生中训练。从环境探索自动采样起点与目标状态，用规则化状态匹配做 verifier，形成无需人工任务与专家轨迹的可扩展 mid-training。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的环境派生中训练算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04934">原论文</a> · <a href="../../../../agent-research/2608.04934-state2state/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning Agent Santa Clara University 2026-08-03 主题：搜索轨迹 hindsight。冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索轨迹 hindsight 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  搜索轨迹 hindsight Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-hindsearch-b112afa3">HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Santa Clara University · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>主题：搜索轨迹 hindsight。冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的搜索轨迹 hindsight 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01597">原论文</a> · <a href="../../../../agent-research/2608.01597-hindsearch/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Group-Reflective Self-Distillation Agent Baidu Inc. 2026-07-30 轨迹终局 reward 混合了真正有效行为、重复错误与偶然选择。GRSD 让当前 policy 对同题 on-policy group 中每条已验证轨迹反思，再由参数相同的 stop-gradient 快照对比成功/失败反思，形成只在训练期可见的 DO/AVOID guidance，并调制 turn-level advantage。 保真度：执行成功/失败 rollout group、策略自身反思、stop-gradient group guidance 与 turn-level 更新。反思由可审计结构化轨迹产生，不是 Qwen 自然语言反思；验证的是 group contrast 和更新路由。本地对照口径：PlanBench mini-suite 120 episodes；joint success 1.0000，并执行 120 个反思组、120 次成败对照、360 次 privileged-guidance update。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-grsd-ed16d3df">Group-Reflective Self-Distillation</h2>
<p class="ar-learning-card__meta">Baidu Inc. · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>轨迹终局 reward 混合了真正有效行为、重复错误与偶然选择。GRSD 让当前 policy 对同题 on-policy group 中每条已验证轨迹反思，再由参数相同的 stop-gradient 快照对比成功/失败反思，形成只在训练期可见的 DO/AVOID guidance，并调制 turn-level advantage。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：执行成功/失败 rollout group、策略自身反思、stop-gradient group guidance 与 turn-level 更新。反思由可审计结构化轨迹产生，不是 Qwen 自然语言反思；验证的是 group contrast 和更新路由。本地对照口径：PlanBench mini-suite 120 episodes；joint success 1.0000，并执行 120 个反思组、120 次成败对照、360 次 privileged-guidance update。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28076">原论文</a> · <a href="../../../../agent-research/2607.28076-grsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TAPO Agent Peking University 2026-07-30 稀疏任务 reward 只告诉 Agent 最终成败，没有利用每次动作后的环境反馈。TAPO 复用同一 rollout，在共享 backbone 上交替训练策略目标与的 next-observation 预测，不增加采样、专家数据或推理开销。 保真度：在确定性环境实际交替执行 policy action 与 action-conditioned next-observation supervision。确定性 observation 适合验证数据流与交替目标，不等同于 Qwen2.5 在 WebShop/ALFWorld 的 RL 训练。本地对照口径：PlanBench mini-suite 120 episodes；与只看 outcome 的 Agent 比较，TAPO 保持 joint success 1.0000，并新增 360 个 transition targets、预测准确率 1.0000。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-tapo-abc37e08">TAPO</h2>
<p class="ar-learning-card__meta">Peking University · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>稀疏任务 reward 只告诉 Agent 最终成败，没有利用每次动作后的环境反馈。TAPO 复用同一 rollout，在共享 backbone 上交替训练策略目标与的 next-observation 预测，不增加采样、专家数据或推理开销。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：在确定性环境实际交替执行 policy action 与 action-conditioned next-observation supervision。确定性 observation 适合验证数据流与交替目标，不等同于 Qwen2.5 在 WebShop/ALFWorld 的 RL 训练。本地对照口径：PlanBench mini-suite 120 episodes；与只看 outcome 的 Agent 比较，TAPO 保持 joint success 1.0000，并新增 360 个 transition targets、预测准确率 1.0000。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27973">原论文</a> · <a href="../../../../agent-research/2607.27973-tapo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="CAST Agent University of Science and Technology of China 2026-07-28 把求解器状态价值的相邻差分变成 solver advantage，为稀疏结果奖励补充 turn 级 credit。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。没有复刻论文三类游戏的大规模 LLM RLVR；求解器准确，适合验证 credit assignment 而非模型能力。PlanBench mini-suite 的确定性最短路充当 solver，逐 turn 查询状态值并统计 credit update。  Agentic RL / turn-level credit Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-cast-0c2b025a">CAST</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>把求解器状态价值的相邻差分变成 solver advantage，为稀疏结果奖励补充 turn 级 credit。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。没有复刻论文三类游戏的大规模 LLM RLVR；求解器准确，适合验证 credit assignment 而非模型能力。PlanBench mini-suite 的确定性最短路充当 solver，逐 turn 查询状态值并统计 credit update。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25308">原论文</a> · <a href="../../../../agent-research/2607.25308-cast/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEED Agent Tsinghua University 2026-07-16 从已完成轨迹中反思出可复用 hindsight skill，再用 skill 条件前后的动作概率变化形成稠密 on-policy 蒸馏信号。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。使用确定性任务与结构化 skill，不执行视觉模型或大规模策略梯度训练。在 PlanBench mini-suite 中把成功/失败轨迹压缩为 hindsight skill，并记录 skill 数量、稠密 credit 更新和跨 episode 复用。  Agentic RL / hindsight skill Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-seed-34cb6214">SEED</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-07-16</p>
<p><strong>方法要点：</strong>从已完成轨迹中反思出可复用 hindsight skill，再用 skill 条件前后的动作概率变化形成稠密 on-policy 蒸馏信号。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。使用确定性任务与结构化 skill，不执行视觉模型或大规模策略梯度训练。在 PlanBench mini-suite 中把成功/失败轨迹压缩为 hindsight skill，并记录 skill 数量、稠密 credit 更新和跨 episode 复用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14777">原论文</a> · <a href="../../../../agent-research/2607.14777-seed/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="TurnOPD Agent Academic author team 2026-07-07 用 probe 统计自适应决定 rollout 深度，并逐步把 token KL 预算迁移为 turn-normalized 监督。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。教师行为由确定性任务 oracle 提供；没有运行任务专用大模型教师。ScaleMCP mini-suite 中执行深度 probe、动态截断和 turn 归一化，记录节省的 rollout turns。  Agentic OPD / rollout budgeting Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-turn-opd-4aa539f6">TurnOPD</h2>
<p class="ar-learning-card__meta">Academic author team · 论文公开：2026-07-07</p>
<p><strong>方法要点：</strong>用 probe 统计自适应决定 rollout 深度，并逐步把 token KL 预算迁移为 turn-normalized 监督。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。教师行为由确定性任务 oracle 提供；没有运行任务专用大模型教师。ScaleMCP mini-suite 中执行深度 probe、动态截断和 turn 归一化，记录节省的 rollout turns。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.05804">原论文</a> · <a href="../../../../agent-research/2607.05804-turn-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="StepPO Agent University of Science and Technology of China 2026-04-20 Agent 的自然决策单位是“观察—动作”的 environment step，token-level MDP 会让动作粒度和信用粒度错位。StepPO 将交互重写为 step-level MDP，在 step boundary 估值和做 GAE，并把 step 内 token ratio 聚合后再裁剪。 在 PlanBench mini 的每个环境动作边界执行 step value、step GAE 与 step sequence-ratio clip，并公开对应诊断计数。本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 action 是确定性工具计划，不含真实 LLM token generation；验证的是 step 对齐状态机而非论文规模的 agent 训练。  Step-aligned Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-steppo-4ceaabe2">StepPO</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-04-20</p>
<p><strong>方法要点：</strong>Agent 的自然决策单位是“观察—动作”的 environment step，token-level MDP 会让动作粒度和信用粒度错位。StepPO 将交互重写为 step-level MDP，在 step boundary 估值和做 GAE，并把 step 内 token ratio 聚合后再裁剪。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>在 PlanBench mini 的每个环境动作边界执行 step value、step GAE 与 step sequence-ratio clip，并公开对应诊断计数。本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 action 是确定性工具计划，不含真实 LLM token generation；验证的是 step 对齐状态机而非论文规模的 agent 训练。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18401">原论文</a> · <a href="../../../../agent-research/2604.18401-steppo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="SEARL Agent Shanghai AI Laboratory 2026-04-09 把工具和成功转移维护为图记忆；新 rollout 同时更新 policy 与图边权，形成经验池—检索—改进闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3400；方法特有操作有非零 telemetry。  策略—工具图共进化 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-searl-fe3972b7">SEARL</h2>
<p class="ar-learning-card__meta">Shanghai AI Laboratory · 论文公开：2026-04-09</p>
<p><strong>方法要点：</strong>把工具和成功转移维护为图记忆；新 rollout 同时更新 policy 与图边权，形成经验池—检索—改进闭环。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3400；方法特有操作有非零 telemetry。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07791">原论文</a> · <a href="../../../../agent-research/2604.07791-searl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Reasoning-Driven Synthetic Data Generation and Evaluation Agent EPFL 2026-03-31 单纯扩写种子容易遗漏概念或坍缩到相似样本。Simula 先按因素建立分类树，再控制全局节点组合与局部场景；独立批判过滤样本，并通过批内相对评分校准复杂度。语义生成器与批判模型是决定质量的核心，本地接口不能用启发式替代后宣称复现。§2 与附录 B/C/E 完整实验成本过高，不复现（审查 DONE）。CPU 协议组件，当前验证为 L0 接口与公式检验。没有把固定回调称为 M3 推理，也没有宣称合成数据质量提升。完整实验成本过高，不复现（审查 DONE）。TaxonomyModels 显式提供因素、提案、树 critic 和层计划；GenerationModels 显式提供策略、场景、复杂化、生成、要求批判、修改及正反两个批判回调。它们可接真实提供方，但本轮 runner 使用的都是标明 fixture 的独立调用。  Agent 数据合成 分类树与独立批判 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-simula-9d7ce82b">Reasoning-Driven Synthetic Data Generation and Evaluation</h2>
<p class="ar-learning-card__meta">EPFL · 论文公开：2026-03-31</p>
<p><strong>方法要点：</strong>单纯扩写种子容易遗漏概念或坍缩到相似样本。Simula 先按因素建立分类树，再控制全局节点组合与局部场景；独立批判过滤样本，并通过批内相对评分校准复杂度。语义生成器与批判模型是决定质量的核心，本地接口不能用启发式替代后宣称复现。§2 与附录 B/C/E</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。CPU 协议组件，当前验证为 L0 接口与公式检验。没有把固定回调称为 M3 推理，也没有宣称合成数据质量提升。完整实验成本过高，不复现（审查 DONE）。TaxonomyModels 显式提供因素、提案、树 critic 和层计划；GenerationModels 显式提供策略、场景、复杂化、生成、要求批判、修改及正反两个批判回调。它们可接真实提供方，但本轮 runner 使用的都是标明 fixture 的独立调用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.29791">原论文</a> · <a href="../../../../agent-research/2603.29791-simula/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks Agent University of California, Berkeley 2026-03-04 DMAST 让防守 Agent 与攻击者共享同一 VLM 参数，以不同角色提示交互；先教师模仿，再用不改变目标动作的 oracle reasoning 做 SFT，最后进行共享策略自博弈 RL。改动不只是普通 GRPO：受攻击组中两个角色的原始终局奖励共同决定均值与方差，而成功样本的长度惩罚只进入优势分子。 完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。诊断让同一个微型神经策略处理两种角色，真实执行一次 SGD，并与独立直接公式核对值和梯度。L1 Stage-3 数值组件，diagnostic only，不是浏览器 Agent 能力或完整三阶段复现。完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。只保留 Stage-3 精确组统计与 token 目标；不生成攻击载荷、不访问网页、不加载 VLM、不训练 SFT 或 oracle。length_penalty 是外部提供的；  Agentic RL 共享策略对抗训练 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-dmast-279d6cde">Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks</h2>
<p class="ar-learning-card__meta">University of California, Berkeley · 论文公开：2026-03-04</p>
<p><strong>方法要点：</strong>DMAST 让防守 Agent 与攻击者共享同一 VLM 参数，以不同角色提示交互；先教师模仿，再用不改变目标动作的 oracle reasoning 做 SFT，最后进行共享策略自博弈 RL。改动不只是普通 GRPO：受攻击组中两个角色的原始终局奖励共同决定均值与方差，而成功样本的长度惩罚只进入优势分子。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。诊断让同一个微型神经策略处理两种角色，真实执行一次 SGD，并与独立直接公式核对值和梯度。L1 Stage-3 数值组件，diagnostic only，不是浏览器 Agent 能力或完整三阶段复现。完整实验成本过高，不复现（审查 DONE），不可晋级、未接入 Evolve。只保留 Stage-3 精确组统计与 token 目标；不生成攻击载荷、不访问网页、不加载 VLM、不训练 SFT 或 oracle。length_penalty 是外部提供的；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04364v1">原论文</a> · <a href="../../../../agent-research/2603.04364-dmast/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="PEARL Agent 中国科学院信息工程研究所 2026-01-28 多跳工具调用同时受工具幻觉、参数错误和长程规划薄弱影响。PEARL 的离线阶段用 trial-and-error 建立工具用法与失败条件；在线阶段把 Planner 与 Executor 解耦，用计划正确性、工具链与最终结果组成的密集 reward 进行 GRPO，而不是只依赖稀疏成功信号。 未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。PEARL 先离线探索工具的有效参数与失败条件，再用 planning-centric reward 和 GRPO 训练独立 Planner，把可靠执行与长程规划分开优化。实现离线候选计划探索、planning reward、组内选择更新、Planner/Executor 解耦和跨 episode 复用；未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。  规划强化学习 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-pearl-a555b8b4">PEARL</h2>
<p class="ar-learning-card__meta">中国科学院信息工程研究所 · 论文公开：2026-01-28</p>
<p><strong>方法要点：</strong>多跳工具调用同时受工具幻觉、参数错误和长程规划薄弱影响。PEARL 的离线阶段用 trial-and-error 建立工具用法与失败条件；在线阶段把 Planner 与 Executor 解耦，用计划正确性、工具链与最终结果组成的密集 reward 进行 GRPO，而不是只依赖稀疏成功信号。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。PEARL 先离线探索工具的有效参数与失败条件，再用 planning-centric reward 和 GRPO 训练独立 Planner，把可靠执行与长程规划分开优化。实现离线候选计划探索、planning reward、组内选择更新、Planner/Executor 解耦和跨 episode 复用；未训练 Qwen2.5-7B，也未接入 ToolHop/T-Eval 的真实 API 与 GRPO 集群。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20439">原论文</a> · <a href="../../../../agent-research/2601.20439-pearl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent0 Agent University of North Carolina at Chapel Hill 2025-11-20 任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  零数据多 Agent Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-agent0-bc007c7f">Agent0</h2>
<p class="ar-learning-card__meta">University of North Carolina at Chapel Hill · 论文公开：2025-11-20</p>
<p><strong>方法要点：</strong>任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.16043">原论文</a> · <a href="../../../../agent-research/2511.16043-agent0/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent-R1 Agent University of Science and Technology of China 2025-11-18 把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.9600。  Agentic RL 基础设施 Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-agent-r1-da1f3512">Agent-R1</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2025-11-18</p>
<p><strong>方法要点：</strong>把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.9600。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.14460">原论文</a> · <a href="../../../../agent-research/2511.14460-agent-r1/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="MUA-RL Agent Meituan 2025-08-26 既有 tool-use RL 通常把用户请求视为固定输入，但真实用户会根据 Agent 回答不断修改需求。MUA-RL 将 LLM 模拟用户直接放入 rollout，Agent 在对话中澄清意图并调用真实 MCP/数据库工具；用户消息和工具结果不计入策略 loss，只用最终任务完成奖励鼓励探索。 保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；当前为确定性工具 mini-suite。本地模拟用户按任务上下文确定性揭示约束，工具实际返回 mini-suite 状态，但没有外部 LLM 用户或生产数据库。该实验验证交互与奖励边界，不复刻原模型规模。稳定指标见 omitted-agentic-rl-opd-seed42.json。  多轮用户 Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-mua-rl-ac5031c4">MUA-RL</h2>
<p class="ar-learning-card__meta">Meituan · 论文公开：2025-08-26</p>
<p><strong>方法要点：</strong>既有 tool-use RL 通常把用户请求视为固定输入，但真实用户会根据 Agent 回答不断修改需求。MUA-RL 将 LLM 模拟用户直接放入 rollout，Agent 在对话中澄清意图并调用真实 MCP/数据库工具；用户消息和工具结果不计入策略 loss，只用最终任务完成奖励鼓励探索。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；保真度：实现模拟用户多轮反馈、意图逐步澄清、真实工具观测、环境 token mask 语义和只基于最终完成度的奖励；当前为确定性工具 mini-suite。本地模拟用户按任务上下文确定性揭示约束，工具实际返回 mini-suite 状态，但没有外部 LLM 用户或生产数据库。该实验验证交互与奖励边界，不复刻原模型规模。稳定指标见 omitted-agentic-rl-opd-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.18669">原论文</a> · <a href="../../../../agent-research/2508.18669-mua-rl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Agent Lightning Agent Microsoft Research 2025-08-05 传统 Agent RL 常把所有上下文拼成单序列并与框架强耦合。Agent Lightning 将执行记录成统一 MDP transition，以 credit assignment 拆解轨迹，并采用训练/执行分离架构。 解耦 Agent 执行与 RL 训练，并将长交互轨迹拆成可归因的训练 transition。实现了执行/训练解耦、transition、环境 reward、credit update 与跨 episode 复用；本地更新的是受控 patch policy，不是对 LLM 参数执行 LightningRL。代码 Agent 的命令、编辑与测试形成 transition；测试退出码是真实 reward，失败时把 credit 归给 patch，并把正确修复按 bug family 写入可复用策略记忆。  Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-agent-lightning-78a73390">Agent Lightning</h2>
<p class="ar-learning-card__meta">Microsoft Research · 论文公开：2025-08-05</p>
<p><strong>方法要点：</strong>传统 Agent RL 常把所有上下文拼成单序列并与框架强耦合。Agent Lightning 将执行记录成统一 MDP transition，以 credit assignment 拆解轨迹，并采用训练/执行分离架构。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>解耦 Agent 执行与 RL 训练，并将长交互轨迹拆成可归因的训练 transition。实现了执行/训练解耦、transition、环境 reward、credit update 与跨 episode 复用；本地更新的是受控 patch policy，不是对 LLM 参数执行 LightningRL。代码 Agent 的命令、编辑与测试形成 transition；测试退出码是真实 reward，失败时把 credit 归给 patch，并把正确修复按 bug family 写入可复用策略记忆。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.03680">原论文</a> · <a href="../../../../agent-research/2508.03680-agent-lightning/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="WebAgent-R1 Agent University of Virginia 2025-05-22 网页交互会不断累积 HTML 和历史动作，单轮 GRPO 无法处理状态变化。WebAgent-R1 动态保留近期和任务相关上下文，并行采集完整多轮轨迹，再用 M-GRPO 根据最终成功奖励执行组内相对更新；论文同时强调行为克隆 warm-up 和长 CoT 初始化。 保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；当前使用确定性工具 mini-suite，不冒充 WebArena-Lite。本地环境返回确定性文本工具观测，没有浏览器 DOM、网页副作用或 Qwen/Llama 参数更新。因此只验证多轮 rollout、压缩和组内奖励路径。稳定指标见 omitted-agentic-rl-opd-seed42.json。  网页 Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-webagent-r1-938cd977">WebAgent-R1</h2>
<p class="ar-learning-card__meta">University of Virginia · 论文公开：2025-05-22</p>
<p><strong>方法要点：</strong>网页交互会不断累积 HTML 和历史动作，单轮 GRPO 无法处理状态变化。WebAgent-R1 动态保留近期和任务相关上下文，并行采集完整多轮轨迹，再用 M-GRPO 根据最终成功奖励执行组内相对更新；论文同时强调行为克隆 warm-up 和长 CoT 初始化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；保真度：实现动态上下文压缩、并行完整轨迹、binary outcome reward 和多轮 group-relative update；当前使用确定性工具 mini-suite，不冒充 WebArena-Lite。本地环境返回确定性文本工具观测，没有浏览器 DOM、网页副作用或 Qwen/Llama 参数更新。因此只验证多轮 rollout、压缩和组内奖励路径。稳定指标见 omitted-agentic-rl-opd-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.16421">原论文</a> · <a href="../../../../agent-research/2505.16421-webagent-r1/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="GiGPO Agent Nanyang Technological University 2025-05-16 多轮 Agent 的最终奖励稀疏，整条轨迹的 group relative advantage 无法判断哪个 environment step 做对了。GiGPO 先在完整轨迹组上计算 macro advantage，再按跨轨迹重复到达的 anchor state 建立 step group，计算 micro relative advantage。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。确定性任务没有跨轨迹真实环境 state 合流，使用共享计划步骤作为可审计 anchor-state 代理。在 PlanBench mini 中显式生成完整轨迹组与 step group，分别统计组间和组内优势、trajectory rollout 与 turn credit。  Agent group credit Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-gigpo-7fac2585">GiGPO</h2>
<p class="ar-learning-card__meta">Nanyang Technological University · 论文公开：2025-05-16</p>
<p><strong>方法要点：</strong>多轮 Agent 的最终奖励稀疏，整条轨迹的 group relative advantage 无法判断哪个 environment step 做对了。GiGPO 先在完整轨迹组上计算 macro advantage，再按跨轨迹重复到达的 anchor state 建立 step group，计算 micro relative advantage。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。确定性任务没有跨轨迹真实环境 state 合流，使用共享计划步骤作为可审计 anchor-state 代理。在 PlanBench mini 中显式生成完整轨迹组与 step group，分别统计组间和组内优势、trajectory rollout 与 turn credit。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.10978">原论文</a> · <a href="../../../../agent-research/2505.10978-gigpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="RAGEN Agent Northwestern 2025-04-24 单轮数学 RL 的优化单位是一次回答，而 Agent 要在随机环境中跨多轮决策。RAGEN 提出 StarPO，把 state、thinking、action 和 reward 组织成完整轨迹。论文还观察到 Echo Trap：reward 方差突然塌缩并伴随梯度尖峰。StarPO-S 通过轨迹过滤、critic baseline、梯度稳定和解耦 clipping 抑制这种自我强化的重复模式。 保真度：本地实现 StarPO-S 的 trajectory rollout、退化轨迹过滤、critic baseline、reasoning-aware reward、Echo Trap 探针和解耦 clipping 诊断。本地策略在确定性候选轨迹上选择计划，真实执行但不更新 LLM 参数；Echo Trap 是固定频率的可观测稳定性探针，不冒充论文训练曲线。未运行 WebShop 或原始游戏环境。稳定指标见 classic-agentic-rl-opd-seed42.json。  多轮 Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-ragen-2a3a9785">RAGEN</h2>
<p class="ar-learning-card__meta">Northwestern · 论文公开：2025-04-24</p>
<p><strong>方法要点：</strong>单轮数学 RL 的优化单位是一次回答，而 Agent 要在随机环境中跨多轮决策。RAGEN 提出 StarPO，把 state、thinking、action 和 reward 组织成完整轨迹。论文还观察到 Echo Trap：reward 方差突然塌缩并伴随梯度尖峰。StarPO-S 通过轨迹过滤、critic baseline、梯度稳定和解耦 clipping 抑制这种自我强化的重复模式。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：本地实现 StarPO-S 的 trajectory rollout、退化轨迹过滤、critic baseline、reasoning-aware reward、Echo Trap 探针和解耦 clipping 诊断。本地策略在确定性候选轨迹上选择计划，真实执行但不更新 LLM 参数；Echo Trap 是固定频率的可观测稳定性探针，不冒充论文训练曲线。未运行 WebShop 或原始游戏环境。稳定指标见 classic-agentic-rl-opd-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.20073">原论文</a> · <a href="../../../../agent-research/2504.20073-ragen/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="DeepResearcher Agent HKU 2025-04-04 把 search、browse、证据收集和带引用回答作为一条轨迹，用答案与引用联合奖励训练研究策略。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.5000；方法特有操作有非零 telemetry。  深度研究 RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-deepresearcher-9b53178e">DeepResearcher</h2>
<p class="ar-learning-card__meta">HKU · 论文公开：2025-04-04</p>
<p><strong>方法要点：</strong>把 search、browse、证据收集和带引用回答作为一条轨迹，用答案与引用联合奖励训练研究策略。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.5000；方法特有操作有非零 telemetry。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.03160">原论文</a> · <a href="../../../../agent-research/2504.03160-deepresearcher/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="Search-R1 Agent University of Illinois Urbana-Champaign 2025-03-12 普通 RAG 一次检索后再回答，无法让策略根据中间证据继续调整查询。Search-R1 把搜索引擎视为环境：模型可在 reasoning 中多次输出搜索动作，环境返回文档后继续推理。训练只对模型生成 token 计算 PPO/GRPO loss，检索结果 token 必须 mask，最终答案用简单 outcome reward 评分。 保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；使用确定性 ScaleMCP mini，不调用论文的 E5 索引或训练 Qwen。mini-suite 的检索结果是确定性的当前任务上下文，适合验证交错状态机和 loss mask；没有真实网页索引、Qwen 参数更新或七个 QA benchmark，因此成功率不能与论文 EM 比较。稳定指标见 classic-agentic-rl-opd-seed42.json。  搜索 Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-search-r1-fce4d489">Search-R1</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2025-03-12</p>
<p><strong>方法要点：</strong>普通 RAG 一次检索后再回答，无法让策略根据中间证据继续调整查询。Search-R1 把搜索引擎视为环境：模型可在 reasoning 中多次输出搜索动作，环境返回文档后继续推理。训练只对模型生成 token 计算 PPO/GRPO loss，检索结果 token 必须 mask，最终答案用简单 outcome reward 评分。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；保真度：本地实现多轮推理/搜索状态转换、检索 token loss mask 和 outcome reward；使用确定性 ScaleMCP mini，不调用论文的 E5 索引或训练 Qwen。mini-suite 的检索结果是确定性的当前任务上下文，适合验证交错状态机和 loss mask；没有真实网页索引、Qwen 参数更新或七个 QA benchmark，因此成功率不能与论文 EM 比较。稳定指标见 classic-agentic-rl-opd-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.09516">原论文</a> · <a href="../../../../agent-research/2503.09516-search-r1/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/agent-policy-learning" data-search="LOOP Agent Apple 2025-02-03 长程数字 Agent 的 rollout 昂贵，而传统 PPO 还要维护 value model。LOOP 把 PPO trust region 与 leave-one-out baseline 结合：无需 critic，可对同一批轨迹进行多次更新；逐 token importance ratio 只裁剪漂移 token，不丢弃整条长轨迹。 保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；当前是确定性交互 mini-suite，不是 AppWorld 32B 训练。本地真实执行多轨迹选择和统计更新，但没有 AppWorld、32B LLM 或梯度 checkpoint；mini-suite 满分只说明轨迹控制逻辑正确，不代表论文任务难度。  长时程 Agent RL Agent 交互策略学习：把轨迹反馈变成更新">
<p class="ar-learning-card__domain"><a href="./">Agent / 交互策略学习：把轨迹反馈变成更新</a></p>
<h2 id="paper-agent-research-loop-633efc7d">LOOP</h2>
<p class="ar-learning-card__meta">Apple · 论文公开：2025-02-03</p>
<p><strong>方法要点：</strong>长程数字 Agent 的 rollout 昂贵，而传统 PPO 还要维护 value model。LOOP 把 PPO trust region 与 leave-one-out baseline 结合：无需 critic，可对同一批轨迹进行多次更新；逐 token importance ratio 只裁剪漂移 token，不丢弃整条长轨迹。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；保真度：实现多轨迹采样、leave-one-out advantage、离策略样本复用和逐 token trust-region clipping 诊断；当前是确定性交互 mini-suite，不是 AppWorld 32B 训练。本地真实执行多轨迹选择和统计更新，但没有 AppWorld、32B LLM 或梯度 checkpoint；mini-suite 满分只说明轨迹控制逻辑正确，不代表论文任务难度。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.01600">原论文</a> · <a href="../../../../agent-research/2502.01600-loop/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
