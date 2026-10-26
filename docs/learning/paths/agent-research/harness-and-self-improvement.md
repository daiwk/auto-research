---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 运行流程与自进化：改的是哪一层

[Agent](index.md) / 子主题导学 · 约 3 分钟 · 43 张论文卡

## 先想一个问题

失败之后，是改一次提示、积累经验，还是改变整个任务执行流程？

## 记住这一点

先区分三种变化：当前回合重新作答、跨回合保存语言经验，以及修改工具组织、工作流或运行框架。Reflexion 把失败反馈转为下一次尝试可读的经验，不更新模型权重；更完整的研究系统还会提出候选、实现、评估并保留谱系。每一层变化都要有独立验收：流程被改写不等于任务能力已经提升。

## 一个例子

假设一次研究任务忘记核对数据版本。可先把失误写入下次计划；进一步可把“校验版本与样本切分”加入工作流入口。评估时用未参与修改的任务，记录成功率和总调用成本，再与旧流程比较。只在刚失败的同一个例子上重跑成功，说明修复了这个例子，尚未证明流程能泛化。

## 什么时候要小心

用来提出修改的开发反馈和最终留出评测必须分开，不能让被评估系统读取隐藏答案或评分计划。AgentX 等论文涉及真实研究或工业闭环，本地 mini-suite、固定回调或资料收录不能冒充这些完整能力。完整实验因成本终止的条目仍为未复现，不应因归入“自进化”而重新排入训练队列。

## 先读这几篇

先读 Reflexion，看语言经验如何跨尝试保存；再读 Self-Refine，对比单次反馈修订；最后读 AgentX，理解候选开发、评估与运行流程更新的完整边界，并对照本地仅实现的部分。

1. [Reflexion](../../../agent-research/2303.11366-reflexion/README.md) · [原论文](https://arxiv.org/abs/2303.11366)
2. [Self-Refine](../../../agent-research/2303.17651-self-refine/README.md) · [原论文](https://arxiv.org/abs/2303.17651)
3. [AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems](../../../agent-research/2606.26859-agentx/README.md) · [原论文](https://arxiv.org/abs/2606.26859)

## 自测一下

把一次失败后的提醒写进提示模板，模型权重没有变化，可以称为模型通过 RL 学会了吗？

??? note "展开参考答案"

    不可以。发生的是提示、记忆或运行流程的更新。它可能改善后续行为，但需要按对应层级报告，并用留出任务验证。只有真正收集训练信号并更新策略参数，才能进一步讨论训练算法与模型学习。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 43 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency Agent Tsinghua University 2026-10-23 Agent 在得到工具反馈后经常再调用模型，即使上一轮推理已确定下一步命令。HarnessMM 的 EDG 只保存先前确实完成语义解析的动作及完整字面参数；GDR 检查前置任务完成、public guard 真和参数闭合，再选一个合格节点或 abstain。不支持的观察、缺少依赖、需要新语义判断时回到原慢 actor。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。无 adapter、operator、运行命令、metrics 或 GPU receipt。本地不实现原生 harness 替代器，不制造 fake callback/receipt，不执行 LLM 生成动作或 shell，不用确定性 fixture 证明节省 token。仅保留规范文献及成本终态；promotion_eligible=false、evolve_integrated=false。既有 Agent tracing 框架不等于本论文已集成。  Agent评测与自进化 原生harness回调替代与成本审计 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-harnessmm-efa1b75e">HarnessMM: Recursive Self-Improvement for Harness Token Efficiency</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>Agent 在得到工具反馈后经常再调用模型，即使上一轮推理已确定下一步命令。HarnessMM 的 EDG 只保存先前确实完成语义解析的动作及完整字面参数；GDR 检查前置任务完成、public guard 真和参数闭合，再选一个合格节点或 abstain。不支持的观察、缺少依赖、需要新语义判断时回到原慢 actor。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。无 adapter、operator、运行命令、metrics 或 GPU receipt。本地不实现原生 harness 替代器，不制造 fake callback/receipt，不执行 LLM 生成动作或 shell，不用确定性 fixture 证明节省 token。仅保留规范文献及成本终态；promotion_eligible=false、evolve_integrated=false。既有 Agent tracing 框架不等于本论文已集成。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32813v1">原论文</a> · <a href="../../../../agent-research/2610.32813-harnessmm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation Agent University of Science and Technology of China 2026-10-23 图像生成器即使输出好看，也可能遗漏数量、空间关系、特定文字或身份约束。ImageRSI 固定原始 requirements，以真实生成器产图、五维评审器提供缺陷证据并指导修复，再经独立配对与 holdout 接纳跨任务经验、离线升级 judge，不能靠删掉要求提高分数。经验抽取和经验复用分开：轨迹提议一个包含 Trigger、Negative Trigger、Action、Effect、Side Effects 的策略，不能直接激活。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞审查水位。无可执行 adapter、operator、训练命令、metrics 或 GPU receipt。只保存规范资料条目和原图，不提供可运行模型、打分代理、训练命令或伪单测。真实 generator、语义 judge、repair、paired admission 与 judge post-training 均未实现；promotion_eligible=false、evolve_integrated=false。  Agent评测与自进化 验证驱动图像生成与经验复用 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-image-rsi-f8d5a27f">ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>图像生成器即使输出好看，也可能遗漏数量、空间关系、特定文字或身份约束。ImageRSI 固定原始 requirements，以真实生成器产图、五维评审器提供缺陷证据并指导修复，再经独立配对与 holdout 接纳跨任务经验、离线升级 judge，不能靠删掉要求提高分数。经验抽取和经验复用分开：轨迹提议一个包含 Trigger、Negative Trigger、Action、Effect、Side Effects 的策略，不能直接激活。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞审查水位。无可执行 adapter、operator、训练命令、metrics 或 GPU receipt。只保存规范资料条目和原图，不提供可运行模型、打分代理、训练命令或伪单测。真实 generator、语义 judge、repair、paired admission 与 judge post-training 均未实现；promotion_eligible=false、evolve_integrated=false。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32120v1">原论文</a> · <a href="../../../../agent-research/2610.32120-image-rsi/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training Agent Purdue University 2026-10-23 单次优化器 Agent 能根据当前训练调整程序，却不会自动把经验带到下一次训练。RSI-Opt 让代码 Agent 根据真实训练证据改写 updater，再将 prompt、自然语言 playbook、代码 library 与 cadence 作为可继承策略，通过外层训练评估递归演化。内层训练保持模型、数据顺序、loss、batch size 和更新步数固定，Agent 在 20 个预定机会读取训练损失/诊断；异常更新器经过短试验后回滚。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。没有可执行 adapter、operator、命令、metrics 或 GPU receipt。仅规范收录方法、风险、原图和成本；没有本地优化器 Agent 或跨run控制器，没有用父策略采样公式冒充整篇论文。promotion_eligible=false、evolve_integrated=false。不会把已有通用进化控制器的名字登记为“已集成”。  Agent评测与自进化 优化器程序与跨运行策略演化 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-rsi-opt-94e59e6e">RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training</h2>
<p class="ar-learning-card__meta">Purdue University · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>单次优化器 Agent 能根据当前训练调整程序，却不会自动把经验带到下一次训练。RSI-Opt 让代码 Agent 根据真实训练证据改写 updater，再将 prompt、自然语言 playbook、代码 library 与 cadence 作为可继承策略，通过外层训练评估递归演化。内层训练保持模型、数据顺序、loss、batch size 和更新步数固定，Agent 在 20 个预定机会读取训练损失/诊断；异常更新器经过短试验后回滚。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。没有可执行 adapter、operator、命令、metrics 或 GPU receipt。仅规范收录方法、风险、原图和成本；没有本地优化器 Agent 或跨run控制器，没有用父策略采样公式冒充整篇论文。promotion_eligible=false、evolve_integrated=false。不会把已有通用进化控制器的名字登记为“已集成”。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32026v1">原论文</a> · <a href="../../../../agent-research/2610.32026-rsi-opt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Evolving Agent Interfaces Agent University of California, Santa Barbara 2026-10-20 固定GUI、shell或浏览器接口决定Agent能观察和执行什么。重复点击、逐格编辑、冗长输出等低效行为，既可能来自模型，也可能来自接口设计。Agent S4把接口代码与使用经验一起保存为仓库，固定任务Agent的模型和Harness，由Meta-Agent依据训练轨迹修改仓库。不同于只积累由现有工具组成的技能，它允许改变操作和观察本身。搜索过程中，训练轨迹没有成功标签；验证任务、轨迹、诊断和分数不交给Meta-Agent。验证分数只决定下一步选哪个父仓库。变异修改一个父本，交叉整合两个不同父本； 成本过高，不复现（审查 DONE）。CPU诊断指标与上游工程的差异：本地依据论文保留被淘汰候选及其谱系作为审计记录，未复制上游多岛迁移、SQLite恢复、AWS启动或Landlock沙箱。Repository保存代码文本和使用知识；本模块不exec任意源代码。调用方提供可信的任务Agent、Builder和私有验证grader。这是API数据隔离，不是Python进程沙箱；闭包、回调或字符串本身若已经夹带gold，本模块无法自动识别。真正接入模型时仍须用进程/权限边界保护验证器。  自我进化 接口与Harness进化 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-agent-s4-640f2b45">Evolving Agent Interfaces</h2>
<p class="ar-learning-card__meta">University of California, Santa Barbara · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>固定GUI、shell或浏览器接口决定Agent能观察和执行什么。重复点击、逐格编辑、冗长输出等低效行为，既可能来自模型，也可能来自接口设计。Agent S4把接口代码与使用经验一起保存为仓库，固定任务Agent的模型和Harness，由Meta-Agent依据训练轨迹修改仓库。不同于只积累由现有工具组成的技能，它允许改变操作和观察本身。搜索过程中，训练轨迹没有成功标签；验证任务、轨迹、诊断和分数不交给Meta-Agent。验证分数只决定下一步选哪个父仓库。变异修改一个父本，交叉整合两个不同父本；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。CPU诊断指标与上游工程的差异：本地依据论文保留被淘汰候选及其谱系作为审计记录，未复制上游多岛迁移、SQLite恢复、AWS启动或Landlock沙箱。Repository保存代码文本和使用知识；本模块不exec任意源代码。调用方提供可信的任务Agent、Builder和私有验证grader。这是API数据隔离，不是Python进程沙箱；闭包、回调或字符串本身若已经夹带gold，本模块无法自动识别。真正接入模型时仍须用进程/权限边界保护验证器。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28601">原论文</a> · <a href="../../../../agent-research/2610.28601-agent-s4/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design Agent University of Illinois Urbana-Champaign 2026-10-20 全任务共用一个harness可能互相干扰；为每类任务复制完整实现又难以复用。作者将专用harness写成父类的子类，只覆盖需要改变的prompt、工具或执行hook。发现阶段围绕任务簇改进，部署阶段冻结代码和经验，再用任务及可观察base轨迹选择完整类；父类方法在一个实例里执行，不是额外运行多个祖先Agent。§3 成本过高，不复现（审查 DONE），不下载模型、不试跑完整实验、不自动重试。HarnessDiscovery只接受可信的Python类，不从字符串exec候选。它保存发现阶段的接受和拒绝记录；freeze只复制当前可路由类描述、必要祖先类和路由经验，不传发现分数。发现/held-out ID必须不相交，任务簇只允许发现集ID，部署只接受预声明held-out任务。Actor和路由入口只接受exact PublicTask并按白名单重建对象，拒绝附带gold字段的子类；工具观察也拒绝子类并重建，不能借嵌套对象携带隐藏grader元数据。  自我进化 Harness搜索与继承 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-oo-harness-cd6587e9">Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>全任务共用一个harness可能互相干扰；为每类任务复制完整实现又难以复用。作者将专用harness写成父类的子类，只覆盖需要改变的prompt、工具或执行hook。发现阶段围绕任务簇改进，部署阶段冻结代码和经验，再用任务及可观察base轨迹选择完整类；父类方法在一个实例里执行，不是额外运行多个祖先Agent。§3</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE），不下载模型、不试跑完整实验、不自动重试。HarnessDiscovery只接受可信的Python类，不从字符串exec候选。它保存发现阶段的接受和拒绝记录；freeze只复制当前可路由类描述、必要祖先类和路由经验，不传发现分数。发现/held-out ID必须不相交，任务簇只允许发现集ID，部署只接受预声明held-out任务。Actor和路由入口只接受exact PublicTask并按白名单重建对象，拒绝附带gold字段的子类；工具观察也拒绝子类并重建，不能借嵌套对象携带隐藏grader元数据。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28380">原论文</a> · <a href="../../../../agent-research/2610.28380-oo-harness/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery Agent Google Research 2026-10-17 该研究把计算设计与真实实验测量放进多轮反馈闭环，让Agent利用成功和失败证据调整下一轮策略。关键不是把Agent多跑几轮，而是实物测量可以否定计算评分；论文显示一些预测代理与实际测量不一致。这里仅讨论研究编排与证据边界，不提供生物实验操作流程。 完整实验成本过高，不复现（审查 DONE）。Google优先资料收录；完整实验成本过高，不复现（审查 DONE）。没有低成本代理被标成实现，不进入自动训练队列。完整研究需要专业实验室、物理测量与多轮7–10天反馈周期，无法在单A100/A30或本地Mac低成本完成。依据Results R.1/Figure1直接标记成本过高，不复现（审查 DONE），未启动模型下载、实验运行或无意义代理测试。  科学研究与实验闭环 物理实验反馈 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-aptamer-lab-loop-d80e05ef">Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery</h2>
<p class="ar-learning-card__meta">Google Research · 论文公开：2026-10-17</p>
<p><strong>方法要点：</strong>该研究把计算设计与真实实验测量放进多轮反馈闭环，让Agent利用成功和失败证据调整下一轮策略。关键不是把Agent多跑几轮，而是实物测量可以否定计算评分；论文显示一些预测代理与实际测量不一致。这里仅讨论研究编排与证据边界，不提供生物实验操作流程。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。Google优先资料收录；完整实验成本过高，不复现（审查 DONE）。没有低成本代理被标成实现，不进入自动训练队列。完整研究需要专业实验室、物理测量与多轮7–10天反馈周期，无法在单A100/A30或本地Mac低成本完成。依据Results R.1/Figure1直接标记成本过高，不复现（审查 DONE），未启动模型下载、实验运行或无意义代理测试。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24806v1">原论文</a> · <a href="../../../../agent-research/2610.24806-aptamer-lab-loop/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Athanor: An Agent-Native System for Autonomous Post-Training Research Agent ByteDance / Duke University 2026-10-15 研究 Agent 选择数据、训练算法和阶段组合；独立服务执行异步任务、去污染、冻结评测并保存 checkpoint 谱系。团队共享实验记录与模型，组合 SFT、RL、模型合并及自蒸馏；外部教师调用被禁止。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。不运行完整研究 campaign，不将现有 Evolve 改名冒充 Athanor。无研究自动化实现、benchmark分数或 GPU回执；不把资料链接宣称为 Evolve 集成。范围见本批验收合同。只做论文解读和原图收录。原配置为四个商业研究 Agent 各占八卡节点，合计约12000美元；超过本轮单 A100/A30资源，不启动探跑。成本过高，不复现（审查 DONE）。  递归自改进 自主研究 多 Agent 协作 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-athanor-3414bb2a">Athanor: An Agent-Native System for Autonomous Post-Training Research</h2>
<p class="ar-learning-card__meta">ByteDance / Duke University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>研究 Agent 选择数据、训练算法和阶段组合；独立服务执行异步任务、去污染、冻结评测并保存 checkpoint 谱系。团队共享实验记录与模型，组合 SFT、RL、模型合并及自蒸馏；外部教师调用被禁止。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。不运行完整研究 campaign，不将现有 Evolve 改名冒充 Athanor。无研究自动化实现、benchmark分数或 GPU回执；不把资料链接宣称为 Evolve 集成。范围见本批验收合同。只做论文解读和原图收录。原配置为四个商业研究 Agent 各占八卡节点，合计约12000美元；超过本轮单 A100/A30资源，不启动探跑。成本过高，不复现（审查 DONE）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21055">原论文</a> · <a href="../../../../agent-research/2610.21055-athanor/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning Agent Tsinghua University 2026-10-15 自动后训练研究若让一个 Agent 同时读训练日志、分析失败、改数据、提交任务，可能在上下文中积累大量执行输出，最终只反复调整混合比例。AutoSFT 将 Meta Agent、执行子代理、四种分析视角与数据合成分开：执行侧只返回可追溯产物，分析侧从数据、失败、训练信号、研究历史提出不同方案，Meta Agent 决定下一轮的数据干预。原文 §2–4 干预不局限于筛行或生成：可以调类别比例、删除、修复、替换回答、定向合成和调整顺序。这六类是作者对实际动作的事后归类，不是给分析Agent预设的固定菜单。 完整实验成本过高，不复现（审查 DONE）；高成本资料收录。完整实验成本过高，不复现（审查 DONE）；没有本地模型实现、控制器fixture、假 Adapter 或 evolve 接入。原文配置 Qwen3-1.7B-Base、Megatron-LM、8×H800。一次20轮运行约 130 GPU小时；Agent与数据合成约 95美元/轮、1900美元/次。执行子代理、独立语义审查和每轮从基座训练都是定义机制的重要部分，不能删成几条规则后称为AutoSFT复现。原文 Appendix D  递归自改进 自动后训练与数据研究 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-auto-sft-e69c4a3b">AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>自动后训练研究若让一个 Agent 同时读训练日志、分析失败、改数据、提交任务，可能在上下文中积累大量执行输出，最终只反复调整混合比例。AutoSFT 将 Meta Agent、执行子代理、四种分析视角与数据合成分开：执行侧只返回可追溯产物，分析侧从数据、失败、训练信号、研究历史提出不同方案，Meta Agent 决定下一轮的数据干预。原文 §2–4 干预不局限于筛行或生成：可以调类别比例、删除、修复、替换回答、定向合成和调整顺序。这六类是作者对实际动作的事后归类，不是给分析Agent预设的固定菜单。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；高成本资料收录。完整实验成本过高，不复现（审查 DONE）；没有本地模型实现、控制器fixture、假 Adapter 或 evolve 接入。原文配置 Qwen3-1.7B-Base、Megatron-LM、8×H800。一次20轮运行约 130 GPU小时；Agent与数据合成约 95美元/轮、1900美元/次。执行子代理、独立语义审查和每轮从基座训练都是定义机制的重要部分，不能删成几条规则后称为AutoSFT复现。原文 Appendix D</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22194">原论文</a> · <a href="../../../../agent-research/2610.22194-auto-sft/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent Agent Beihang University 2026-10-15 性能瓶颈可能来自模型参数、执行 Harness，也可能只是当前交付物。固定只改其中一项，或固定交替更新，未必对应当前失败。RSIFlow 的 Meta-Agent 用任务执行证据选择 Model / Harness / Artifacts 干预，比较同父代、同任务批的候选，并从成功和失败中维护技能。Meta 模型参数保持固定；本地遵循已发布的技能记忆变体，不把它扩写成任意自改代码系统。 原文五轮、每轮最多两个候选、4B/8B、SFT/GRPO、16K/32K 与 8 ranks，加上 Meta API 和真实工具执行，完整多臂评测对单 A100/A30 或 Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。实现固定 callback 控制器与技能经验记录，不训练语言模型，不执行任意元程序自改，不进入统一 Evolve 晋级。每 seed 初始化三批、每批四个数值 fixture 和五个独立报告任务；私有目标值仅由 evaluator 闭包持有。M/H/A proposer 只拿公共任务、父代标量分数及已有训练技能。  RSI 自我改进与工作流 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-rsiflow-bf0996bb">RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>性能瓶颈可能来自模型参数、执行 Harness，也可能只是当前交付物。固定只改其中一项，或固定交替更新，未必对应当前失败。RSIFlow 的 Meta-Agent 用任务执行证据选择 Model / Harness / Artifacts 干预，比较同父代、同任务批的候选，并从成功和失败中维护技能。Meta 模型参数保持固定；本地遵循已发布的技能记忆变体，不把它扩写成任意自改代码系统。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原文五轮、每轮最多两个候选、4B/8B、SFT/GRPO、16K/32K 与 8 ranks，加上 Meta API 和真实工具执行，完整多臂评测对单 A100/A30 或 Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。实现固定 callback 控制器与技能经验记录，不训练语言模型，不执行任意元程序自改，不进入统一 Evolve 晋级。每 seed 初始化三批、每批四个数值 fixture 和五个独立报告任务；私有目标值仅由 evaluator 闭包持有。M/H/A proposer 只拿公共任务、父代标量分数及已有训练技能。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21791">原论文</a> · <a href="../../../../agent-research/2610.21791-rsiflow/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine Agent Tencent Hy Frontier / National University of Singapore 2026-10-15 终端 Agent 既要从验证成功的轨迹里学会可重现行为，也要把稀疏完成反馈传给很早的动作。Terminal-RSI 交替 RSR 轨迹改写和保留 critic 权重的 RPR，阶段开始时先校准 critic；提出 TB-GAE 用交互 turn 时钟而非 observation 文本长度衰减，并用 family 校准的 FDR 过渡到严格完成优先的 SPR。 原文 Qwen3.8-27B、256K、多阶段分布式训练、3,000 任务及长终端环境，对单 A100/A30/Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 数值诊断。只执行 TB-GAE、精确 chunk 续接和 FDR/SPR，不执行 shell、终端 Agent 或 PPO 训练。原文 TB-GAE 的 checkpoint 实际使用情况有明确未核实边界。每 seed 初始化 20 个 generated-token value，五个 turn、一个终端奖励；再插入 40 个 observation，核对结果不变。  RSI Agent RL 长程终端任务 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-terminal-rsi-d5ceabe6">Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine</h2>
<p class="ar-learning-card__meta">Tencent Hy Frontier / National University of Singapore · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>终端 Agent 既要从验证成功的轨迹里学会可重现行为，也要把稀疏完成反馈传给很早的动作。Terminal-RSI 交替 RSR 轨迹改写和保留 critic 权重的 RPR，阶段开始时先校准 critic；提出 TB-GAE 用交互 turn 时钟而非 observation 文本长度衰减，并用 family 校准的 FDR 过渡到严格完成优先的 SPR。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原文 Qwen3.8-27B、256K、多阶段分布式训练、3,000 任务及长终端环境，对单 A100/A30/Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 数值诊断。只执行 TB-GAE、精确 chunk 续接和 FDR/SPR，不执行 shell、终端 Agent 或 PPO 训练。原文 TB-GAE 的 checkpoint 实际使用情况有明确未核实边界。每 seed 初始化 20 个 generated-token value，五个 turn、一个终端奖励；再插入 40 个 observation，核对结果不变。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22192">原论文</a> · <a href="../../../../agent-research/2610.22192-terminal-rsi/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock Agent Peking University / Samsung Research 2026-10-14 游戏在模型推理时继续前进，观测时正确的动作在执行时可能已失效。原文 §3–4提出 RealtimeBench 的 paused／live／accelerated 时钟比较，及 Two-Timescale Offline Recursive Self-Improvement：快学生在实况中独立行动，慢教师只在两次尝试之间读失败轨迹、在 feedback 保存状态上离线练习，并改写可复用指导。指导冻结后只由独立 validation 决定是否替换；test 不参与修订或选择。 成本过高，不复现（审查 DONE）。本地未运行 Mario/Snake 等引擎、Jev、教师或异步控制，不把数值 fixture 当实时能力评测；evaluation_protocol_interface / L1 CPU。只有时钟、反馈隔离与指导接受协议，没有实时游戏或模型能力复现。每 seed 随机生成 16 个计时事件和 12 个数值 validation 行；独立检查 action age 比只统计响应延迟多出的调度时间、严格增益、平局与下降拒绝。teacher 仅收到人工 feedback 轨迹。逐 seed 实测和来源 hash 见 CPU 产物，不代表游戏进展或 Jev 改善。  RSI 实时决策与离线指导进化 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-torsi-cd7ddf6f">The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock</h2>
<p class="ar-learning-card__meta">Peking University / Samsung Research · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>游戏在模型推理时继续前进，观测时正确的动作在执行时可能已失效。原文 §3–4提出 RealtimeBench 的 paused／live／accelerated 时钟比较，及 Two-Timescale Offline Recursive Self-Improvement：快学生在实况中独立行动，慢教师只在两次尝试之间读失败轨迹、在 feedback 保存状态上离线练习，并改写可复用指导。指导冻结后只由独立 validation 决定是否替换；test 不参与修订或选择。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。本地未运行 Mario/Snake 等引擎、Jev、教师或异步控制，不把数值 fixture 当实时能力评测；evaluation_protocol_interface / L1 CPU。只有时钟、反馈隔离与指导接受协议，没有实时游戏或模型能力复现。每 seed 随机生成 16 个计时事件和 12 个数值 validation 行；独立检查 action age 比只统计响应延迟多出的调度时间、严格增益、平局与下降拒绝。teacher 仅收到人工 feedback 轨迹。逐 seed 实测和来源 hash 见 CPU 产物，不代表游戏进展或 Jev 改善。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20665">原论文</a> · <a href="../../../../agent-research/2610.20665-torsi/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses Agent Google Cloud AI Research / Carnegie Mellon University 2026-10-10 单目标演化可能通过放松检查提高功能分数，同时损害安全。Harmony Harness 将功能与安全保持为两个独立目标：每个偏好向量维护一个框架，候选只替换邻域中更差的框架。工具、技能、逻辑分别记录在通用或环境专属范围，再由组合器为当前任务选择执行 DAG。图为依据原文 Figure 1 重绘的机制说明，不是本地执行记录。原图与正文。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。Gemini 3.6 Flash 承担 proposer 与 solver；三次独立运行、多代多子问题，真实 Docker 构建和 exploit 评估主导耗时（§5、附录 C/G/I）。完整实验成本过高，不复现（审查 DONE）；成本判断源于论文规模，不是本地测量。  自进化与经验复用 多目标Harness演化 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-harmony-harness-9020f112">Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses</h2>
<p class="ar-learning-card__meta">Google Cloud AI Research / Carnegie Mellon University · 论文公开：2026-10-10</p>
<p><strong>方法要点：</strong>单目标演化可能通过放松检查提高功能分数，同时损害安全。Harmony Harness 将功能与安全保持为两个独立目标：每个偏好向量维护一个框架，候选只替换邻域中更差的框架。工具、技能、逻辑分别记录在通用或环境专属范围，再由组合器为当前任务选择执行 DAG。图为依据原文 Figure 1 重绘的机制说明，不是本地执行记录。原图与正文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。Gemini 3.6 Flash 承担 proposer 与 solver；三次独立运行、多代多子问题，真实 Docker 构建和 exploit 评估主导耗时（§5、附录 C/G/I）。完整实验成本过高，不复现（审查 DONE）；成本判断源于论文规模，不是本地测量。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15150v1">原论文</a> · <a href="../../../../agent-research/2610.15150-harmony-harness/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness²: Recursive Agent Harnessing for an Open World Agent Northwestern University 2026-10-09 Harness 是模型外的提示、工具、记忆、技能、脚本、子代理和中间件。论文在不改模型权重的前提下，把“改进当前任务执行方式”和“积累以后如何改进的经验”连接起来。它不要求任务答案、评分细则或验证器：先观察执行，再提出通用候选与领域候选，执行二者，最后按行为差异组合，而不是把某个评分函数冒充正确性判定。论文 §2 高成本完整实验：成本过高，不复现（审查 DONE）。编辑器诊断脚本中的正数过滤，通用分支更新约束，领域分支删除不符合公开任务的过滤，组合分支合并实际执行过的修改。component_only / L1 CPU 控制器与接口。真实执行 Python 探针，但 editor、selector 是确定性机制测试替身；不是模型支持的 Agent 能力评测，也不是已接入 Evolve。只使用 Python 标准库，无模型下载、API 凭证或 GPU。产物存在时拒绝覆盖，重复执行请换输出路径。实际探针在临时目录运行可信 Python 脚本，单次 subprocess 超时 5 秒；  规划、搜索与反思 Harness 与自我改进 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-harness2-5c8a24eb">Harness²: Recursive Agent Harnessing for an Open World</h2>
<p class="ar-learning-card__meta">Northwestern University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>Harness 是模型外的提示、工具、记忆、技能、脚本、子代理和中间件。论文在不改模型权重的前提下，把“改进当前任务执行方式”和“积累以后如何改进的经验”连接起来。它不要求任务答案、评分细则或验证器：先观察执行，再提出通用候选与领域候选，执行二者，最后按行为差异组合，而不是把某个评分函数冒充正确性判定。论文 §2</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>高成本完整实验：成本过高，不复现（审查 DONE）。编辑器诊断脚本中的正数过滤，通用分支更新约束，领域分支删除不符合公开任务的过滤，组合分支合并实际执行过的修改。component_only / L1 CPU 控制器与接口。真实执行 Python 探针，但 editor、selector 是确定性机制测试替身；不是模型支持的 Agent 能力评测，也不是已接入 Evolve。只使用 Python 标准库，无模型下载、API 凭证或 GPU。产物存在时拒绝覆盖，重复执行请换输出路径。实际探针在临时目录运行可信 Python 脚本，单次 subprocess 超时 5 秒；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14224">原论文</a> · <a href="../../../../agent-research/2610.14224-harness2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Anything: Unlocking Recursive Self-Improvement with World Models Agent PhAI Labs / The Chinese University of Hong Kong 2026-10-09 候选先经世界模型预测，再向外部验证申请反馈；反馈更新持久 policy/workflow，可靠性不足且数据/预算足够时适配 predictor。只有组件检查和配对兼容性检查均通过的版本进入下一轮。事实来源：原文全文。 保持 concept_demo / L1、diagnostic_only=true、capability_comparison=false、evolve_promotion_eligible=false，不进入 Evolve 晋级。当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始 policy workflow 与初始 predictor 配对；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  recursive-self-improvement world-model compatibility-retention Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-rsi-anything-7f27ef73">RSI-Anything: Unlocking Recursive Self-Improvement with World Models</h2>
<p class="ar-learning-card__meta">PhAI Labs / The Chinese University of Hong Kong · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>候选先经世界模型预测，再向外部验证申请反馈；反馈更新持久 policy/workflow，可靠性不足且数据/预算足够时适配 predictor。只有组件检查和配对兼容性检查均通过的版本进入下一轮。事实来源：原文全文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>保持 concept_demo / L1、diagnostic_only=true、capability_comparison=false、evolve_promotion_eligible=false，不进入 Evolve 晋级。当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始 policy workflow 与初始 predictor 配对；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13912">原论文</a> · <a href="../../../../reproductions/2610.13912-rsi-anything/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution Agent King Abdullah University of Science and Technology 2026-10-08 模型选择 Full、Partial 或 Discard，得到 Partial 证据后再选择继续/停止。已观察案例更新固定语句经验并反思策略；影子策略共享同一证据，以漏掉新最佳的次数优先、再比较评测成本。拒绝候选以概率做反事实评测，避免选择性反馈。原文达到基线时 Full 数减少 59–82%，同预算成绩提高 8.7–12.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。复用真实 Linux bubblewrap/prlimit Circle26 程序环境，可信几何检查器评分而非模型自报，沙箱失败即拒绝运行。Circle26 无 Partial，因此此运行只允许 Full/Discard。经验 ADD/UPDATE/DELETE 不允许 UPDATE 重写语句，未观察案例不可当证据，最多四条活跃/暂定和四条陈旧经验。  程序进化 评测预算 策略自进化 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-evoalloc-9a5390ec">EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution</h2>
<p class="ar-learning-card__meta">King Abdullah University of Science and Technology · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>模型选择 Full、Partial 或 Discard，得到 Partial 证据后再选择继续/停止。已观察案例更新固定语句经验并反思策略；影子策略共享同一证据，以漏掉新最佳的次数优先、再比较评测成本。拒绝候选以概率做反事实评测，避免选择性反馈。原文达到基线时 Full 数减少 59–82%，同预算成绩提高 8.7–12.0%，未报告线上 A/B。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。复用真实 Linux bubblewrap/prlimit Circle26 程序环境，可信几何检查器评分而非模型自报，沙箱失败即拒绝运行。Circle26 无 Partial，因此此运行只允许 Full/Discard。经验 ADD/UPDATE/DELETE 不允许 UPDATE 重写语句，未观察案例不可当证据，最多四条活跃/暂定和四条陈旧经验。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12086">原论文</a> · <a href="../../../../agent-research/2610.12086-evoalloc/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Recursive Self-Improvement through Multi-Agent Self-Supervision Agent UC Berkeley 2026-10-08 同一模型执行、提出工作流并成对评价。固定权重下搜索后，独立采集轨迹，以 Bradley–Terry 排名选择前 K−1 条训练、第 K 条验证；仅移除编排者初始工作流提示，保留工作者分工。助手 token 的 SFT 更新权重后再重复。原文 Qwen3.6-27B 两轮在研究任务中提高单位输出 token 表现约 1.2–1.6 倍，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。真实共享 checkpoint 完成两轮搜索、裁判、轨迹采集与 LoRA SFT。本地为固定两工作者和一编排者的有界文本工作流族，可改变角色指令和传递内容；未接入任意工作流图、qwen-code 文件/终端工具，因此不是完整科研 coding-agent 复现。  递归自改进 工作流搜索 多智能体自监督 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-mass-a7f2d6e4">Recursive Self-Improvement through Multi-Agent Self-Supervision</h2>
<p class="ar-learning-card__meta">UC Berkeley · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>同一模型执行、提出工作流并成对评价。固定权重下搜索后，独立采集轨迹，以 Bradley–Terry 排名选择前 K−1 条训练、第 K 条验证；仅移除编排者初始工作流提示，保留工作者分工。助手 token 的 SFT 更新权重后再重复。原文 Qwen3.6-27B 两轮在研究任务中提高单位输出 token 表现约 1.2–1.6 倍，未报告线上 A/B。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。真实共享 checkpoint 完成两轮搜索、裁判、轨迹采集与 LoRA SFT。本地为固定两工作者和一编排者的有界文本工作流族，可改变角色指令和传递内容；未接入任意工作流图、qwen-code 文件/终端工具，因此不是完整科研 coding-agent 复现。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12176">原论文</a> · <a href="../../../../agent-research/2610.12176-mass/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks Agent University College London 2026-10-08 冻结 LLM 将黑盒交互证据写成可修改规则册，再编译为世界模型。新代码必须同时通过语义忠实性判断和全部历史逐格回放；规划失配会触发修复。多个模型共享历史，按不同完整计划的等价类均匀抽样，而非按重复模型投票。论文第 2 节 当前实现为 L1 核心机制实验，不是原论文完整基准。已在 NVIDIA A100-SXM4-80GB 上实际运行冻结 Qwen2.5-7B；生成模型在第一次真实动作后被证伪，修复未成功，最终没有可用世界模型，任务也未完成。这是一条保留失败的机制执行记录，不是能力提升结果。  世界模型 反思与记忆 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-memento3-dd7ada6c">Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks</h2>
<p class="ar-learning-card__meta">University College London · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>冻结 LLM 将黑盒交互证据写成可修改规则册，再编译为世界模型。新代码必须同时通过语义忠实性判断和全部历史逐格回放；规划失配会触发修复。多个模型共享历史，按不同完整计划的等价类均匀抽样，而非按重复模型投票。论文第 2 节</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>当前实现为 L1 核心机制实验，不是原论文完整基准。已在 NVIDIA A100-SXM4-80GB 上实际运行冻结 Qwen2.5-7B；生成模型在第一次真实动作后被证伪，修复未成功，最终没有可用世界模型，任务也未完成。这是一条保留失败的机制执行记录，不是能力提升结果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11794">原论文</a> · <a href="../../../../agent-research/2610.11794-memento3/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution Agent National University of Singapore 2026-10-02 FrugalEvo 把程序优化拆成高成本模型提出策略、低成本模型执行和改进代码，按预算内整条最佳成绩曲线评价搜索效率。先试跑多种策略再排序，失败时保留父程序追加反馈，取得改进后重新锚定，并用岛屿档案保存不同程序。 本地独立实现与公开任务小预算验证。不是原论文 API 模型、美元成本或完整 20 任务结果的复现；尚未接入统一 Evolve 控制器。共享前缀字节顺序已实现；当前 Transformers 后端没有跨请求 KV 前缀缓存，cached_input_tokens=0，不声称复现论文缓存加速。需要 Linux、可用的 bubblewrap/prlimit、CUDA 和预先下载的公开 checkpoint。生成程序在无网络、无工作区/凭据/模型缓存挂载的沙箱中运行；沙箱不能启动时拒绝执行，没有裸 exec 回退。  程序进化 成本约束 强弱模型协作 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-frugalevo-468f3ba3">FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution</h2>
<p class="ar-learning-card__meta">National University of Singapore · 论文公开：2026-10-02</p>
<p><strong>方法要点：</strong>FrugalEvo 把程序优化拆成高成本模型提出策略、低成本模型执行和改进代码，按预算内整条最佳成绩曲线评价搜索效率。先试跑多种策略再排序，失败时保留父程序追加反馈，取得改进后重新锚定，并用岛屿档案保存不同程序。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地独立实现与公开任务小预算验证。不是原论文 API 模型、美元成本或完整 20 任务结果的复现；尚未接入统一 Evolve 控制器。共享前缀字节顺序已实现；当前 Transformers 后端没有跨请求 KV 前缀缓存，cached_input_tokens=0，不声称复现论文缓存加速。需要 Linux、可用的 bubblewrap/prlimit、CUDA 和预先下载的公开 checkpoint。生成程序在无网络、无工作区/凭据/模型缓存挂载的沙箱中运行；沙箱不能启动时拒绝执行，没有裸 exec 回退。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03675">原论文</a> · <a href="../../../../agent-research/2610.03675-frugalevo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting Agent Google Cloud AI Research / University of Virginia 2026-10-02 数值历史可能缺少外部事件信息，普通 RAG 又不会从预测错误中修订检索方法。SEER 保持预测模型权重不变，把上下文拆成检索记忆、筛选记忆和因果知识。只有过去结果真正可见后，才从预测轨迹中分别更新两类记忆与知识；容量不足时压缩，而不是无限追加。图按原文 Figure 2 与 §3 重绘。原图及方法。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。完整协议涉及 Gemini 3.1 Pro/Flash、Claude 4.6 Sonnet/4.8 Opus，多轮搜索、LEAF 事实核验与顺序回测（§4.1）。闭源调用与六领域完整成本无法用廉价只读检查可靠固定；成本过高，不复现（审查 DONE）。  自进化与经验复用 时间约束事件检索与预测 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-seer-forecasting-fb9c59fb">SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting</h2>
<p class="ar-learning-card__meta">Google Cloud AI Research / University of Virginia · 论文公开：2026-10-02</p>
<p><strong>方法要点：</strong>数值历史可能缺少外部事件信息，普通 RAG 又不会从预测错误中修订检索方法。SEER 保持预测模型权重不变，把上下文拆成检索记忆、筛选记忆和因果知识。只有过去结果真正可见后，才从预测轨迹中分别更新两类记忆与知识；容量不足时压缩，而不是无限追加。图按原文 Figure 2 与 §3 重绘。原图及方法。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。完整协议涉及 Gemini 3.1 Pro/Flash、Claude 4.6 Sonnet/4.8 Opus，多轮搜索、LEAF 事实核验与顺序回测（§4.1）。闭源调用与六领域完整成本无法用廉价只读检查可靠固定；成本过高，不复现（审查 DONE）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.04109v1">原论文</a> · <a href="../../../../agent-research/2610.04109-seer-forecasting/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Sentry: Learning to Recover from LLM Agent Failures at Test Time Agent Stanford University 2026-10-02 Sentry 不把所有失败经验长期塞进 Agent 上下文，而是先识别当前行为失败，再按类别和标签检索相关恢复建议。外部验证器只看后续可观察进展、不看任务奖励，确认恢复后才把经验写入 playbook；动作格式错误走单独的硬修复路径。 未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。独立控制器与真实 checkpoint 的小预算工具任务验证；未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。数据使用 HotpotQA 官方 Hugging Face 镜像的 validation parquet。脚本校验固定 SHA-256，并按题目 ID 哈希排序；前 4 题建立记忆，之后 16 题保留给接口开发，再后 8 题作隔离对照。它们均来自官方 dev，不是官方 test。  失败恢复 条件记忆 测试时学习 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-sentry-acd21bdd">Sentry: Learning to Recover from LLM Agent Failures at Test Time</h2>
<p class="ar-learning-card__meta">Stanford University · 论文公开：2026-10-02</p>
<p><strong>方法要点：</strong>Sentry 不把所有失败经验长期塞进 Agent 上下文，而是先识别当前行为失败，再按类别和标签检索相关恢复建议。外部验证器只看后续可观察进展、不看任务奖励，确认恢复后才把经验写入 playbook；动作格式错误走单独的硬修复路径。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。独立控制器与真实 checkpoint 的小预算工具任务验证；未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。数据使用 HotpotQA 官方 Hugging Face 镜像的 validation parquet。脚本校验固定 SHA-256，并按题目 ID 哈希排序；前 4 题建立记忆，之后 16 题保留给接口开发，再后 8 题作隔离对照。它们均来自官方 dev，不是官方 test。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02994">原论文</a> · <a href="../../../../agent-research/2610.02994-sentry/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization Agent POSTECH 2026-10-01 把反复出现的失败模式动态实例化为非平稳 bandit arm；课程控制器在发现新场景和重访已知弱点之间选择，并随 harness 修复结果更新优先级。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Harness 优化 主动课程 RSI Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-active-saddler-9c3dd285">ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization</h2>
<p class="ar-learning-card__meta">POSTECH · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>把反复出现的失败模式动态实例化为非平稳 bandit arm；课程控制器在发现新场景和重访已知弱点之间选择，并随 harness 修复结果更新优先级。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00906">原论文</a> · <a href="../../../../agent-research/2610.00906-active-saddler/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="It Takes Workflows to Evolve Better Workflows Agent William &amp; Mary 2026-10-01 利用 workflow 拓扑把稀疏结果拆为层级、结构感知的 role credit，使单角色自进化、上下游协同或多 Agent co-evolution 可共用一个 harness。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  工作流进化 多 Agent 层级奖励 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-flowright-b0c3085e">It Takes Workflows to Evolve Better Workflows</h2>
<p class="ar-learning-card__meta">William &amp; Mary · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>利用 workflow 拓扑把稀疏结果拆为层级、结构感知的 role credit，使单角色自进化、上下游协同或多 Agent co-evolution 可共用一个 harness。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01026">原论文</a> · <a href="../../../../agent-research/2610.01026-flowright/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Evolving Coding Rules for AI Coding Agents Agent 原文首页未列第一作者机构 2026-09-30 维护 coding rule 候选池，由 mutator 生成变体，再只用隔离 validation evaluator 选择并回写更优规则。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选变异后的 validation 选择；不调用 LLM mutator。执行候选变异后的 validation 选择；不调用 LLM mutator。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RSI Coding Agent 规则进化 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-rule-evolve-f1ced1e2">Self-Evolving Coding Rules for AI Coding Agents</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-09-30</p>
<p><strong>方法要点：</strong>维护 coding rule 候选池，由 mutator 生成变体，再只用隔离 validation evaluator 选择并回写更优规则。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选变异后的 validation 选择；不调用 LLM mutator。执行候选变异后的 validation 选择；不调用 LLM mutator。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00650">原论文</a> · <a href="../../../../agent-research/2610.00650-rule-evolve/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Mixture of Self-Improving Branches for Agent Harness Optimization Agent 原文首页未列机构 2026-09-29 将 harness 搜索拆成多条分支，每条分支维护不同的开发子集和 proposal policy；全分支都解决的样本被移除，具有分支区分度的样本被保留，部署时由只看输入特征的 router 选择开发集冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 优化 分支搜索 RSI Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-branch-mixture-203f2124">Mixture of Self-Improving Branches for Agent Harness Optimization</h2>
<p class="ar-learning-card__meta">原文首页未列机构 · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>将 harness 搜索拆成多条分支，每条分支维护不同的开发子集和 proposal policy；全分支都解决的样本被移除，具有分支区分度的样本被保留，部署时由只看输入特征的 router 选择开发集冠军。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37834">原论文</a> · <a href="../../../../agent-research/2609.37834-branch-mixture/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI Agent Apodex / University of Illinois Urbana-Champaign 2026-09-29 从开发任务的 harness 执行反馈中提炼包含 when、provide、use 的 meta-skill，再冻结技能库；测试任务只检索相关 meta-skill 来构建新 harness，不用测试结果反向修改技能库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 设计 Meta-skill RSI Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-meta-skills-2db3e168">Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI</h2>
<p class="ar-learning-card__meta">Apodex / University of Illinois Urbana-Champaign · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>从开发任务的 harness 执行反馈中提炼包含 when、provide、use 的 meta-skill，再冻结技能库；测试任务只检索相关 meta-skill 来构建新 harness，不用测试结果反向修改技能库。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38143">原论文</a> · <a href="../../../../agent-research/2609.38143-meta-skills/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution Agent Tsinghua University 2026-09-29 视频 Agent 的执行 trace 只包含当前 harness 选择观察的证据，因此失败解释可能无法区分。Video-RSI 让模型回访原训练视频、主动收集额外观察，形成可检验诊断并改写 harness；候选只有在准确率提高且成本不恶化，或成本下降且准确率不恶化时才保留。 复现级别：L1 接纳规则。复现级别：L1 接纳规则。实现准确率—视觉成本双目标的 Pareto 接纳；未在视频 benchmark 上自动改写并执行完整 harness。未把训练视频私有答案或 example-level score 暴露给候选 harness；当前不含真实视频解码、代码改写 sandbox 和跨代停止条件，因而暂不登记为 Evolve 可执行 operator。  RSI Harness 演化 视频理解 Agent Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-video-rsi-6a868dfd">Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>视频 Agent 的执行 trace 只包含当前 harness 选择观察的证据，因此失败解释可能无法区分。Video-RSI 让模型回访原训练视频、主动收集额外观察，形成可检验诊断并改写 harness；候选只有在准确率提高且成本不恶化，或成本下降且准确率不恶化时才保留。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 接纳规则。复现级别：L1 接纳规则。实现准确率—视觉成本双目标的 Pareto 接纳；未在视频 benchmark 上自动改写并执行完整 harness。未把训练视频私有答案或 example-level score 暴露给候选 harness；当前不含真实视频解码、代码改写 sandbox 和跨代停止条件，因而暂不登记为 Evolve 可执行 operator。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37950">原论文</a> · <a href="../../../../agent-research/2609.37950-video-rsi/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness Learning Enables Generalizable Test-Time Adaptation Agent Johns Hopkins University 2026-09-28 论文把测试时适配的对象从模型参数转为可执行 harness：proposer 根据真实执行反馈修改验证、解释器、检索或重试组件；底层任务模型保持冻结，多轮执行后保留更有效的脚手架。 复现级别：L1 无 gold 机制诊断。复现级别：L1 无 gold 机制诊断。实现由执行反馈驱动的 harness revision policy 与多轮适配；冻结任务策略，不读取答案或计划。当前没有接入通用 Agent runner 或 Evolve，因为二者尚不能安全执行任意 harness 并完成隔离验证；本页不把规则化 mini-suite 的成功率宣称为 Agent 能力提升。HarnessProposer 与 adapt_harness 可接入外部真实执行 callback；汇总诊断见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Harness 学习 测试时适配 元学习 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-harness-learning-a67122de">Harness Learning Enables Generalizable Test-Time Adaptation</h2>
<p class="ar-learning-card__meta">Johns Hopkins University · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>论文把测试时适配的对象从模型参数转为可执行 harness：proposer 根据真实执行反馈修改验证、解释器、检索或重试组件；底层任务模型保持冻结，多轮执行后保留更有效的脚手架。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 无 gold 机制诊断。复现级别：L1 无 gold 机制诊断。实现由执行反馈驱动的 harness revision policy 与多轮适配；冻结任务策略，不读取答案或计划。当前没有接入通用 Agent runner 或 Evolve，因为二者尚不能安全执行任意 harness 并完成隔离验证；本页不把规则化 mini-suite 的成功率宣称为 Agent 能力提升。HarnessProposer 与 adapt_harness 可接入外部真实执行 callback；汇总诊断见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35738">原论文</a> · <a href="../../../../agent-research/2609.35738-harness-learning/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems Agent Kuaishou 2026-09-24 早期 AgentX 关注从研究构想到实现、评估的单次闭环；AgentX-Model 追问一次实验之后如何决定下一次做什么。Research Agent 负责跨论文和实验路径提出、独立审查研究问题；Model Agent 接收获批提案，在固定业务输入与预测任务下多轮改代码、训练、测量，并返回中间最佳实现、负结果和未解问题。两者通过提案而非共享完整工作日志衔接。 本地保真度：公开数据机制验证（concept demo）。本地保真度：公开数据机制验证（concept demo）。执行了双角色提案/审查/调查接口、四类动作和带依赖的结果盲回放；角色由确定性规则驱动，实验图由 MovieLens-1M 上实际训练的六个轻量模型节点组成。它不是论文的私有 473 节点历史图、LLM Agent 系统或线上 A/B 复现。本地两个“Agent”是有隔离接口的确定性执行角色，而非论文使用的 Pi/Claude Code/GLM、独立 LLM 审查或自动编程；模型变种也是预设可执行候选，非系统自主发明。六节点依赖图来自本仓库真实公开数据实验，不是作者 473 节点生产日志；  研究自动化 依赖约束历史回放 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-agentx-model-replay-82b929d4">Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2026-09-24</p>
<p><strong>方法要点：</strong>早期 AgentX 关注从研究构想到实现、评估的单次闭环；AgentX-Model 追问一次实验之后如何决定下一次做什么。Research Agent 负责跨论文和实验路径提出、独立审查研究问题；Model Agent 接收获批提案，在固定业务输入与预测任务下多轮改代码、训练、测量，并返回中间最佳实现、负结果和未解问题。两者通过提案而非共享完整工作日志衔接。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地保真度：公开数据机制验证（concept demo）。本地保真度：公开数据机制验证（concept demo）。执行了双角色提案/审查/调查接口、四类动作和带依赖的结果盲回放；角色由确定性规则驱动，实验图由 MovieLens-1M 上实际训练的六个轻量模型节点组成。它不是论文的私有 473 节点历史图、LLM Agent 系统或线上 A/B 复现。本地两个“Agent”是有隔离接口的确定性执行角色，而非论文使用的 Pi/Claude Code/GLM、独立 LLM 审查或自动编程；模型变种也是预设可执行候选，非系统自主发明。六节点依赖图来自本仓库真实公开数据实验，不是作者 473 节点生产日志；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30001">原论文</a> · <a href="../../../../agent-research/2609.30001-agentx-model/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents Agent Gen-Verse research collaboration 2026-09-15 内层递归演化交互 harness，外层用成功轨迹更新科学 Agent 策略。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双层状态更新；没有连接真实实验室环境。本地执行双层状态更新；没有连接真实实验室环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  科学 Agent 递归自进化 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-sciencebuddy-cd9b47fe">ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents</h2>
<p class="ar-learning-card__meta">Gen-Verse research collaboration · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>内层递归演化交互 harness，外层用成功轨迹更新科学 Agent 策略。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双层状态更新；没有连接真实实验室环境。本地执行双层状态更新；没有连接真实实验室环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17523">原论文</a> · <a href="../../../../agent-research/2609.17523-sciencebuddy/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization Agent The Chinese University of Hong Kong, Shenzhen 2026-09-10 把技能优化视为动态候选空间中的预算化 contextual bandit，优先评估高收益或高信息量技能，再依据执行反馈演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能进化 Contextual bandit Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-cobra-skills-f91c343f">COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization</h2>
<p class="ar-learning-card__meta">The Chinese University of Hong Kong, Shenzhen · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>把技能优化视为动态候选空间中的预算化 contextual bandit，优先评估高收益或高信息量技能，再依据执行反馈演化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11682">原论文</a> · <a href="../../../../agent-research/2609.11682-cobra-skills/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents Agent Chengdu Institute of Computer Applications, Chinese Academy of Sciences 2026-09-10 聚合跨任务重复失败以区分模型偶发错误和 harness 系统缺陷，再由 FDCR 多角色诊断形成修复规格。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Harness 自进化 失败诊断 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-ecdysis-3d533dc6">Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents</h2>
<p class="ar-learning-card__meta">Chengdu Institute of Computer Applications, Chinese Academy of Sciences · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>聚合跨任务重复失败以区分模型偶发错误和 harness 系统缺陷，再由 FDCR 多角色诊断形成修复规格。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11677">原论文</a> · <a href="../../../../agent-research/2609.11677-ecdysis/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MAPLE: Memory-Augmented Planning with Language and Evolution Agent Harbin Institute of Technology, Shenzhen 2026-09-10 MAPLE 把自然语言优化知识变成可持续修改的程序状态：生成候选、检查可执行性、接纳更好的方案，并把已接受程序带到后续问题中继续进化，而不是每次从零提示。 复现级别：持久状态机制诊断。复现级别：持久状态机制诊断。实现候选方案接纳、跨任务复用和版本化状态，不执行论文的数学优化器或 LLM 代码生成。三种子结果见 metrics/mini-suite-seeds42-44.json。本地只接纳由非空命名操作构成的公开计划并验证后续复用；没有运行作者求解器、训练模型或外部工具，因此不把 mini-suite 成功率作为论文能力复现。  持久化优化规划 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-maple-2e42a8d7">MAPLE: Memory-Augmented Planning with Language and Evolution</h2>
<p class="ar-learning-card__meta">Harbin Institute of Technology, Shenzhen · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>MAPLE 把自然语言优化知识变成可持续修改的程序状态：生成候选、检查可执行性、接纳更好的方案，并把已接受程序带到后续问题中继续进化，而不是每次从零提示。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：持久状态机制诊断。复现级别：持久状态机制诊断。实现候选方案接纳、跨任务复用和版本化状态，不执行论文的数学优化器或 LLM 代码生成。三种子结果见 metrics/mini-suite-seeds42-44.json。本地只接纳由非空命名操作构成的公开计划并验证后续复用；没有运行作者求解器、训练模型或外部工具，因此不把 mini-suite 成功率作为论文能力复现。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11636">原论文</a> · <a href="../../../../agent-research/2609.11636-maple/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents Agent Google 2026-09-08 方法把成功经验从自然语言片段提升为 procedure–relation–procedure 图。新经验先局部化为候选图编辑，再经过 held-out 验证门才写入长期结构，减少错误经验污染。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现 procedure–relation–procedure 图和保守编辑门，不包含 LLM 生成或真实环境执行。三种子 evomem-mini 结果见 metrics/mini-suite-seeds42-44.json。本地编辑门以“已建立路线必须保留首尾节点”为确定性代理；策略看不到隐藏答案/计划，也未调用真实工具，因此仅验证图更新与拒绝路径。  自进化程序图 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-procedural-graphs-6aeeaceb">Procedural Graphs: Self-Evolving Execution Structures for LLM Agents</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-09-08</p>
<p><strong>方法要点：</strong>方法把成功经验从自然语言片段提升为 procedure–relation–procedure 图。新经验先局部化为候选图编辑，再经过 held-out 验证门才写入长期结构，减少错误经验污染。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现 procedure–relation–procedure 图和保守编辑门，不包含 LLM 生成或真实环境执行。三种子 evomem-mini 结果见 metrics/mini-suite-seeds42-44.json。本地编辑门以“已建立路线必须保留首尾节点”为确定性代理；策略看不到隐藏答案/计划，也未调用真实工具，因此仅验证图更新与拒绝路径。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09153">原论文</a> · <a href="../../../../agent-research/2609.09153-procedural-graphs/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification Agent Fudan University 2026-08-27 固定验证集浪费 rollout 且会用平均分掩盖局部回退。HarnessLens 从执行轨迹提出修改，只在受影响行为对应的任务上成对验证，并要求证据能归因到候选修改。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现行为任务选择、配对验证与可归因证据门。未运行论文四个完整 benchmark；本地执行冻结测试集和无 answer/guide 接口的真实工具反馈协议。ToolRoute-L2.1 三 seed：joint success 0.8194，plan F1 0.8372，平均成本 5.0419。  行为相关 Harness 验证 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-harnesslens-7d46fb0d">Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification</h2>
<p class="ar-learning-card__meta">Fudan University · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>固定验证集浪费 rollout 且会用平均分掩盖局部回退。HarnessLens 从执行轨迹提出修改，只在受影响行为对应的任务上成对验证，并要求证据能归因到候选修改。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现行为任务选择、配对验证与可归因证据门。未运行论文四个完整 benchmark；本地执行冻结测试集和无 answer/guide 接口的真实工具反馈协议。ToolRoute-L2.1 三 seed：joint success 0.8194，plan F1 0.8372，平均成本 5.0419。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27311">原论文</a> · <a href="../../../../agent-research/2608.27311-harnesslens/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution Agent LV-NUS Lab 2026-08-26 把 harness 形式化为 memory、planning、action protocol、tools/skills 四个可生成模块；模型按任务生成、失败后修复，并从历史配置 archive 蒸馏可迁移模式。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。JIT harness 在训练任务上即时写入/修复可复用路由，在 validation/test 冻结后仅通过公开 observation、工具元数据和真实调用反馈执行；不存在 answer、guide 或 reference-plan 接口。  Harness 即时生成与进化 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-jit-agent-92c11b63">JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution</h2>
<p class="ar-learning-card__meta">LV-NUS Lab · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>把 harness 形式化为 memory、planning、action protocol、tools/skills 四个可生成模块；模型按任务生成、失败后修复，并从历史配置 archive 蒸馏可迁移模式。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。JIT harness 在训练任务上即时写入/修复可复用路由，在 validation/test 冻结后仅通过公开 observation、工具元数据和真实调用反馈执行；不存在 answer、guide 或 reference-plan 接口。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25593">原论文</a> · <a href="../../../../agent-research/2608.25593-jit-agent/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks Agent Tsinghua University 2026-08-10 把 observation/planning/memory/action/verification/recovery 等 Loop Policy 资产版本化，以 Champion–Challenger、发布监控和回滚治理进化。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  自进化 策略治理 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-openloopevolve-709aab65">OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-08-10</p>
<p><strong>方法要点：</strong>把 observation/planning/memory/action/verification/recovery 等 Loop Policy 资产版本化，以 Champion–Challenger、发布监控和回滚治理进化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09380">原论文</a> · <a href="../../../../agent-research/2608.09380-openloopevolve/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems Agent Kuaishou 2026-06-26 传统推荐迭代需要工程师串联假设、生产代码、上线 A/B 和归因，经验也难以跨实验积累。AgentX 将流程改造成四阶段闭环：Brainstorm Agent 从实验库、系统知识、数据分析和外部论文生成有证据的候选；Developing Agent 在仓库约束下实现并验证；Evaluation Agent 用护栏否决的线上 A/B 判断；最后以 SGPO 从成功与失败轨迹更新 Agent harness。 复现级别：核心闭环 mini-suite。复现级别：核心闭环 mini-suite。本地实现 Brainstorm、Developing、Evaluation 与 Harness Evolution 四阶段控制流，并验证实验知识复用带来的执行成本下降。本地没有 Kuaishou 内部仓库、流量平台、线上用户或 SGPO 大模型训练，因此不能复现论文的业务增益。mini-suite 验证的是四阶段闭环、正负结果资产化、验证门槛与跨 episode 复用；average proxy cost 仅是控制流成本，不冒充人效、收入或线上时长。  研究自动化 工业推荐 Agent Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-agentx-26ba162a">AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2026-06-26</p>
<p><strong>方法要点：</strong>传统推荐迭代需要工程师串联假设、生产代码、上线 A/B 和归因，经验也难以跨实验积累。AgentX 将流程改造成四阶段闭环：Brainstorm Agent 从实验库、系统知识、数据分析和外部论文生成有证据的候选；Developing Agent 在仓库约束下实现并验证；Evaluation Agent 用护栏否决的线上 A/B 判断；最后以 SGPO 从成功与失败轨迹更新 Agent harness。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心闭环 mini-suite。复现级别：核心闭环 mini-suite。本地实现 Brainstorm、Developing、Evaluation 与 Harness Evolution 四阶段控制流，并验证实验知识复用带来的执行成本下降。本地没有 Kuaishou 内部仓库、流量平台、线上用户或 SGPO 大模型训练，因此不能复现论文的业务增益。mini-suite 验证的是四阶段闭环、正负结果资产化、验证门槛与跨 episode 复用；average proxy cost 仅是控制流成本，不冒充人效、收入或线上时长。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.26859">原论文</a> · <a href="../../../../agent-research/2606.26859-agentx/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence Agent Google Cloud AI Research 2026-05-25 研究产物看起来完整，仍可能引用虚构、分数无法复算或方法描述与代码不同。CoE 将主张连到可核验来源；独立 I1–I4 检查分数、规则、引用和方法/代码一致性。来源存在不等于主张被支持。原文 §3 与 §5 完整实验成本过高，不复现（审查 DONE）。本地实现低成本 CoE 机械核验内核与语义审计接口，不是完整自主科学家。固定刺激为 L0；完整实验成本过高，不复现（审查 DONE）。canonical evaluator 的可信性、日志是否由实际实验产生、语义判断是否正确仍由上层证据保障；哈希只能证明“相同字节”，不能证明“字节描述了真实实验”。本地不将任意 Python callback 当安全沙箱。  科学研究 Agent 证据链与完整性审计 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-scientist-one-ba34af9f">ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence</h2>
<p class="ar-learning-card__meta">Google Cloud AI Research · 论文公开：2026-05-25</p>
<p><strong>方法要点：</strong>研究产物看起来完整，仍可能引用虚构、分数无法复算或方法描述与代码不同。CoE 将主张连到可核验来源；独立 I1–I4 检查分数、规则、引用和方法/代码一致性。来源存在不等于主张被支持。原文 §3 与 §5</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。本地实现低成本 CoE 机械核验内核与语义审计接口，不是完整自主科学家。固定刺激为 L0；完整实验成本过高，不复现（审查 DONE）。canonical evaluator 的可信性、日志是否由实际实验产生、语义判断是否正确仍由上层证据保障；哈希只能证明“相同字节”，不能证明“字节描述了真实实验”。本地不将任意 Python callback 当安全沙箱。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26340">原论文</a> · <a href="../../../../agent-research/2605.26340-scientist-one/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HyperAgents Agent University of British Columbia 2026-03-19 把任务 Agent 与修改它的 meta Agent 放入同一可编辑程序，并在开放档案中积累变体；父代概率同时奖励当前性能与较少后代的探索价值，使改进机制本身也可继续被改进。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。三种子诊断：metrics/mechanism-seeds42-44.json  RSI 开放式进化 元认知自修改 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-hyperagents-ae71283f">HyperAgents</h2>
<p class="ar-learning-card__meta">University of British Columbia · 论文公开：2026-03-19</p>
<p><strong>方法要点：</strong>把任务 Agent 与修改它的 meta Agent 放入同一可编辑程序，并在开放档案中积累变体；父代概率同时奖励当前性能与较少后代的探索价值，使改进机制本身也可继续被改进。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。三种子诊断：metrics/mechanism-seeds42-44.json</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19461">原论文</a> · <a href="../../../../agent-research/2603.19461-hyperagents/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="POLCA: Stochastic Generative Optimization with LLM Agent University of Wisconsin-Madison 2026-03-16 随机 minibatch、程序与评估器都会产生噪声。POLCA 不仅保留一次最高分，而是持续更新候选评价历史；Summarizer 形成全局经验，Proposer 利用当前反馈提出参数，语义 epsilon-net 限制冗余候选。原文 §3 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0；优先队列和真实回调接口已实现，没有声称已运行 LLM 优化器或 benchmark 能力。完整实验：成本过高，不复现（审查 DONE）。6 项测试通过，覆盖严格 epsilon 边界、新候选互相过滤、同一有放回 minibatch、跨轮噪声均值/方差、完整输入/输出历史送入 Summarizer/Proposer、预算耗尽及拒绝 test split。诊断记录  Agent 自进化 随机优化 程序搜索 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-polca-3e1ab10b">POLCA: Stochastic Generative Optimization with LLM</h2>
<p class="ar-learning-card__meta">University of Wisconsin-Madison · 论文公开：2026-03-16</p>
<p><strong>方法要点：</strong>随机 minibatch、程序与评估器都会产生噪声。POLCA 不仅保留一次最高分，而是持续更新候选评价历史；Summarizer 形成全局经验，Proposer 利用当前反馈提出参数，语义 epsilon-net 限制冗余候选。原文 §3</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0；优先队列和真实回调接口已实现，没有声称已运行 LLM 优化器或 benchmark 能力。完整实验：成本过高，不复现（审查 DONE）。6 项测试通过，覆盖严格 epsilon 边界、新候选互相过滤、同一有放回 minibatch、跨轮噪声均值/方差、完整输入/输出历史送入 Summarizer/Proposer、预算耗尽及拒绝 test split。诊断记录</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.14769">原论文</a> · <a href="../../../../agent-research/2603.14769-polca/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MARS: Modular Agent with Reflective Search for Automated AI Research Agent Google Cloud AI Research 2026-02-02 自动研究不仅要生成正确代码，还需在有限训练时间内分辨改动价值。MARS 使用“设计—拆分—实现”生成模块化仓库，以预算感知 MCTS 选择新方案、改进或调试；比较新旧执行结果和代码差异，提炼解决方案经验与调试经验，供其他搜索分支复用。图按原文 Figure 2 重绘。原文流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。MLE-Bench 包含 75 个竞赛，每竞赛预算 24 小时单张 A100-40GB，另有大内存、存储和闭源 LLM 调用；完整多方法三次评测显然超出短时单卡预算（§5.1）。成本过高，不复现（审查 DONE），不启动下载与竞赛训练来验证成本。  自进化与经验复用 预算感知自动研究 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-mars-research-5e806f85">MARS: Modular Agent with Reflective Search for Automated AI Research</h2>
<p class="ar-learning-card__meta">Google Cloud AI Research · 论文公开：2026-02-02</p>
<p><strong>方法要点：</strong>自动研究不仅要生成正确代码，还需在有限训练时间内分辨改动价值。MARS 使用“设计—拆分—实现”生成模块化仓库，以预算感知 MCTS 选择新方案、改进或调试；比较新旧执行结果和代码差异，提炼解决方案经验与调试经验，供其他搜索分支复用。图按原文 Figure 2 重绘。原文流程图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。MLE-Bench 包含 75 个竞赛，每竞赛预算 24 小时单张 A100-40GB，另有大内存、存储和闭源 LLM 调用；完整多方法三次评测显然超出短时单卡预算（§5.1）。成本过高，不复现（审查 DONE），不启动下载与竞赛训练来验证成本。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02660v1">原论文</a> · <a href="../../../../agent-research/2602.02660-mars-research/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Refine Agent Carnegie Mellon University 2023-03-30 一次生成很难同时满足所有约束。Self-Refine 让同一个 LLM 先生成初稿，再针对任务维度给出可执行反馈，最后据此改写；若反馈判断已满足要求则停止，不需要额外训练数据、人工反馈或外部 reward model。 Self-Refine 在不更新参数的情况下循环执行“生成—自反馈—改写”，把推理时计算用于发现并修正当前答案的问题。实现显式初稿、约束反馈、修订和停止链路；mini-suite 用确定性 critic 验证状态迁移，没有调用论文中的通用 LLM，也不能用 1.0 成功率替代七项原始 benchmark 结果。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 2.0000，执行 120 次反馈和 120 次 refinement，共记录 240 个 reasoning steps。  自我迭代 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-self-refine-16be87c4">Self-Refine</h2>
<p class="ar-learning-card__meta">Carnegie Mellon University · 论文公开：2023-03-30</p>
<p><strong>方法要点：</strong>一次生成很难同时满足所有约束。Self-Refine 让同一个 LLM 先生成初稿，再针对任务维度给出可执行反馈，最后据此改写；若反馈判断已满足要求则停止，不需要额外训练数据、人工反馈或外部 reward model。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Self-Refine 在不更新参数的情况下循环执行“生成—自反馈—改写”，把推理时计算用于发现并修正当前答案的问题。实现显式初稿、约束反馈、修订和停止链路；mini-suite 用确定性 critic 验证状态迁移，没有调用论文中的通用 LLM，也不能用 1.0 成功率替代七项原始 benchmark 结果。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 2.0000，执行 120 次反馈和 120 次 refinement，共记录 240 个 reasoning steps。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17651">原论文</a> · <a href="../../../../agent-research/2303.17651-self-refine/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Reflexion Agent Northeastern University 2023-03-20 传统 RL 要大量采样与参数更新。Reflexion 把稀疏标量/二值反馈“放大”为可执行的自然语言经验，写入长期 episodic memory；Actor 在下一 trial 读取反思，Evaluator 继续判定成功与否。 本页实现失败反馈 → 语言反思 → 有界 episodic memory → 下一 trial 改进，全程不更新模型权重。实现跨 trial 的失败、语言经验与复用闭环，但反思模板和 evaluator 是确定性的；没有调用 GPT-4、ALFWorld、HotpotQA 或代码执行器。0.9 来自“每个新族首次失败”的可审计协议，不等同 HumanEval pass@1。PlanBench mini 有 12 个重复任务族。每族首次暴露计划错误，Evaluator 失败后生成一条可复用反思；后续 episode 读取当前上下文并执行完整计划。  自我反思 Agent 运行流程与自进化：改的是哪一层">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<h2 id="paper-agent-research-reflexion-b837a66e">Reflexion</h2>
<p class="ar-learning-card__meta">Northeastern University · 论文公开：2023-03-20</p>
<p><strong>方法要点：</strong>传统 RL 要大量采样与参数更新。Reflexion 把稀疏标量/二值反馈“放大”为可执行的自然语言经验，写入长期 episodic memory；Actor 在下一 trial 读取反思，Evaluator 继续判定成功与否。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现失败反馈 → 语言反思 → 有界 episodic memory → 下一 trial 改进，全程不更新模型权重。实现跨 trial 的失败、语言经验与复用闭环，但反思模板和 evaluator 是确定性的；没有调用 GPT-4、ALFWorld、HotpotQA 或代码执行器。0.9 来自“每个新族首次失败”的可审计协议，不等同 HumanEval pass@1。PlanBench mini 有 12 个重复任务族。每族首次暴露计划错误，Evaluator 失败后生成一条可复用反思；后续 episode 读取当前上下文并执行完整计划。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.11366">原论文</a> · <a href="../../../../agent-research/2303.11366-reflexion/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
