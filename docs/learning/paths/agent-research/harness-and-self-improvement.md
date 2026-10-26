---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 运行流程与自进化：改的是哪一层

[Agent](index.md) / 43 个问题 · 43 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">43 个问题 · 43 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessmm" data-paper-title="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency Agent Tsinghua University 2026-10-23 Agent 在得到工具反馈后经常再调用模型，即使上一轮推理已确定下一步命令。HarnessMM 的 EDG 只保存先前确实完成语义解析的动作及完整字面参数；GDR 检查前置任务完成、public guard 真和参数闭合，再选一个合格节点或 abstain。不支持的观察、缺少依赖、需要新语义判断时回到原慢 actor。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。无 adapter、operator、运行命令、metrics 或 GPU receipt。本地不实现原生 harness 替代器，不制造 fake callback/receipt，不执行 LLM 生成动作或 shell，不用确定性 fixture 证明节省 token。仅保留规范文献及成本终态；promotion_eligible=false、evolve_integrated=false。既有 Agent tracing 框架不等于本论文已集成。  Agent评测与自进化 原生harness回调替代与成本审计 Agent 运行流程与自进化：改的是哪一层 参数闭合和 guard 为真，为什么还不足以证明省掉一次模型调用既正确又真实？ 这些条件只支持某条动作可被复用，语义是否完成任务仍需原评测器判断。执行证书还要绑定精确参数、前驱回执与工具结果，并审计原注册边界的慢调用确实未发生；理论上可跳过与物理调用实际减少是两件事，失败和恢复成本也不能漏算。 例如图里已有可执行测试命令，系统可直接调用，但必须留下真实测试回执并确认未另发一次慢模型请求，才能计入节省。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harnessmm-efa1b75e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f0cd3e3e41dc248b">参数闭合和 guard 为真，为什么还不足以证明省掉一次模型调用既正确又真实？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnessmm">HarnessMM: Recursive Self-Improvement for Harness Token Efficiency</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这些条件只支持某条动作可被复用，语义是否完成任务仍需原评测器判断。执行证书还要绑定精确参数、前驱回执与工具结果，并审计原注册边界的慢调用确实未发生；理论上可跳过与物理调用实际减少是两件事，失败和恢复成本也不能漏算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图里已有可执行测试命令，系统可直接调用，但必须留下真实测试回执并确认未另发一次慢模型请求，才能计入节省。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32813v1">原论文</a> · <a href="../../../../agent-research/2610.32813-harnessmm/">实现解读</a> · <a href="#qa-f0cd3e3e41dc248b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:image-rsi" data-paper-title="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation Agent University of Science and Technology of China 2026-10-23 图像生成器即使输出好看，也可能遗漏数量、空间关系、特定文字或身份约束。ImageRSI 固定原始 requirements，以真实生成器产图、五维评审器提供缺陷证据并指导修复，再经独立配对与 holdout 接纳跨任务经验、离线升级 judge，不能靠删掉要求提高分数。经验抽取和经验复用分开：轨迹提议一个包含 Trigger、Negative Trigger、Action、Effect、Side Effects 的策略，不能直接激活。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞审查水位。无可执行 adapter、operator、训练命令、metrics 或 GPU receipt。只保存规范资料条目和原图，不提供可运行模型、打分代理、训练命令或伪单测。真实 generator、语义 judge、repair、paired admission 与 judge post-training 均未实现；promotion_eligible=false、evolve_integrated=false。  Agent评测与自进化 验证驱动图像生成与经验复用 Agent 运行流程与自进化：改的是哪一层 为什么循环内图像评分高，仍不能直接激活抽取出的经验策略？ 同一评审器引导修复又评价收益，可能强化自身偏差。经验需先在相同请求、配置和 seed 下做有无配对，由独立盲评校准，再经独立 holdout 接纳；硬约束也不能被平均高分掩盖，fallback 返回最好图不等于经验或图像已达接纳标准。 例如修复策略让评审偏爱的构图更漂亮，却漏掉指定人数；只有固定要求的独立配对与硬否决检查，才能暴露这种投机。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-image-rsi-f8d5a27f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f8c753569fbafcbc">为什么循环内图像评分高，仍不能直接激活抽取出的经验策略？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aimage-rsi">ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一评审器引导修复又评价收益，可能强化自身偏差。经验需先在相同请求、配置和 seed 下做有无配对，由独立盲评校准，再经独立 holdout 接纳；硬约束也不能被平均高分掩盖，fallback 返回最好图不等于经验或图像已达接纳标准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如修复策略让评审偏爱的构图更漂亮，却漏掉指定人数；只有固定要求的独立配对与硬否决检查，才能暴露这种投机。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32120v1">原论文</a> · <a href="../../../../agent-research/2610.32120-image-rsi/">实现解读</a> · <a href="#qa-f8c753569fbafcbc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-opt" data-paper-title="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training Agent Purdue University 2026-10-23 单次优化器 Agent 能根据当前训练调整程序，却不会自动把经验带到下一次训练。RSI-Opt 让代码 Agent 根据真实训练证据改写 updater，再将 prompt、自然语言 playbook、代码 library 与 cadence 作为可继承策略，通过外层训练评估递归演化。内层训练保持模型、数据顺序、loss、batch size 和更新步数固定，Agent 在 20 个预定机会读取训练损失/诊断；异常更新器经过短试验后回滚。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。没有可执行 adapter、operator、命令、metrics 或 GPU receipt。仅规范收录方法、风险、原图和成本；没有本地优化器 Agent 或跨run控制器，没有用父策略采样公式冒充整篇论文。promotion_eligible=false、evolve_integrated=false。不会把已有通用进化控制器的名字登记为“已集成”。  Agent评测与自进化 优化器程序与跨运行策略演化 Agent 运行流程与自进化：改的是哪一层 为什么内层 Agent 看不到最终任务指标，而外层仍能用它评价策略？ 内层依据训练损失与诊断改 updater，若读取最终指标就会直接对评测反馈调参；外层评估固定策略的整体研究表现，承担不同选择职责。跨轮继承提示、库和节奏才是递归部分，归一化聚合也只是排名工具，不能把搜索套件成绩当未见任务泛化。 例如内层只看到训练 loss 决定改更新规则，运行结束后外层比较策略；不能让内层每次试改都先查看最终测试分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-rsi-opt-94e59e6e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d4432df8e608d4f4">为什么内层 Agent 看不到最终任务指标，而外层仍能用它评价策略？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsi-opt">RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Purdue University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内层依据训练损失与诊断改 updater，若读取最终指标就会直接对评测反馈调参；外层评估固定策略的整体研究表现，承担不同选择职责。跨轮继承提示、库和节奏才是递归部分，归一化聚合也只是排名工具，不能把搜索套件成绩当未见任务泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如内层只看到训练 loss 决定改更新规则，运行结束后外层比较策略；不能让内层每次试改都先查看最终测试分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32026v1">原论文</a> · <a href="../../../../agent-research/2610.32026-rsi-opt/">实现解读</a> · <a href="#qa-d4432df8e608d4f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-s4" data-paper-title="Evolving Agent Interfaces" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Evolving Agent Interfaces Agent University of California, Santa Barbara 2026-10-20 固定GUI、shell或浏览器接口决定Agent能观察和执行什么。重复点击、逐格编辑、冗长输出等低效行为，既可能来自模型，也可能来自接口设计。Agent S4把接口代码与使用经验一起保存为仓库，固定任务Agent的模型和Harness，由Meta-Agent依据训练轨迹修改仓库。不同于只积累由现有工具组成的技能，它允许改变操作和观察本身。搜索过程中，训练轨迹没有成功标签；验证任务、轨迹、诊断和分数不交给Meta-Agent。验证分数只决定下一步选哪个父仓库。变异修改一个父本，交叉整合两个不同父本； 成本过高，不复现（审查 DONE）。CPU诊断指标与上游工程的差异：本地依据论文保留被淘汰候选及其谱系作为审计记录，未复制上游多岛迁移、SQLite恢复、AWS启动或Landlock沙箱。Repository保存代码文本和使用知识；本模块不exec任意源代码。调用方提供可信的任务Agent、Builder和私有验证grader。这是API数据隔离，不是Python进程沙箱；闭包、回调或字符串本身若已经夹带gold，本模块无法自动识别。真正接入模型时仍须用进程/权限边界保护验证器。  自我进化 接口与Harness进化 Agent 运行流程与自进化：改的是哪一层 为什么子接口仓库即使暂时低分也留在种群，而非只保留严格优于父本的修改？ 进化搜索可能需要经过局部低谷或组合不同改动，保留后代让未来变异和交叉仍能利用其结构。验证分数用于选父本，但验证轨迹和标签不交给 Meta-Agent；改变的是动作与观察接口本身，不能把训练策略误写为逐轮贪心接纳最佳 patch。 例如一次接口改动单独效果一般，却可与另一路观察压缩组合；若立即删除所有低分后代，就失去这类后续组合机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-agent-s4-640f2b45" class="ar-learning-paper-anchor"></span>
<h2 id="qa-290fc521db43089d">为什么子接口仓库即使暂时低分也留在种群，而非只保留严格优于父本的修改？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-s4">Evolving Agent Interfaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>进化搜索可能需要经过局部低谷或组合不同改动，保留后代让未来变异和交叉仍能利用其结构。验证分数用于选父本，但验证轨迹和标签不交给 Meta-Agent；改变的是动作与观察接口本身，不能把训练策略误写为逐轮贪心接纳最佳 patch。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次接口改动单独效果一般，却可与另一路观察压缩组合；若立即删除所有低分后代，就失去这类后续组合机会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28601">原论文</a> · <a href="../../../../agent-research/2610.28601-agent-s4/">实现解读</a> · <a href="#qa-290fc521db43089d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:oo-harness" data-paper-title="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design Agent University of Illinois Urbana-Champaign 2026-10-20 全任务共用一个harness可能互相干扰；为每类任务复制完整实现又难以复用。作者将专用harness写成父类的子类，只覆盖需要改变的prompt、工具或执行hook。发现阶段围绕任务簇改进，部署阶段冻结代码和经验，再用任务及可观察base轨迹选择完整类；父类方法在一个实例里执行，不是额外运行多个祖先Agent。§3 成本过高，不复现（审查 DONE），不下载模型、不试跑完整实验、不自动重试。HarnessDiscovery只接受可信的Python类，不从字符串exec候选。它保存发现阶段的接受和拒绝记录；freeze只复制当前可路由类描述、必要祖先类和路由经验，不传发现分数。发现/held-out ID必须不相交，任务簇只允许发现集ID，部署只接受预声明held-out任务。Actor和路由入口只接受exact PublicTask并按白名单重建对象，拒绝附带gold字段的子类；工具观察也拒绝子类并重建，不能借嵌套对象携带隐藏grader元数据。  自我进化 Harness搜索与继承 Agent 运行流程与自进化：改的是哪一层 子类复用父 harness 方法，为什么不等于同时执行多个祖先 Agent？ 继承是代码复用：一个实例调用未覆盖的父方法，不会自动启动祖先的独立轨迹。专用子类只改必要 hook，部署时从冻结候选选完整类；目标簇得分提升也不保证所有任务改善，自报置信度消融更不能被误作校准成功概率。 例如子类只覆盖搜索 prompt，终端执行仍调用父实现；这是一名 Agent 的一套方法，不应把它计成两名 Agent 并行协作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-oo-harness-cd6587e9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5d4d6c07f614cbe3">子类复用父 harness 方法，为什么不等于同时执行多个祖先 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aoo-harness">Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>继承是代码复用：一个实例调用未覆盖的父方法，不会自动启动祖先的独立轨迹。专用子类只改必要 hook，部署时从冻结候选选完整类；目标簇得分提升也不保证所有任务改善，自报置信度消融更不能被误作校准成功概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如子类只覆盖搜索 prompt，终端执行仍调用父实现；这是一名 Agent 的一套方法，不应把它计成两名 Agent 并行协作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28380">原论文</a> · <a href="../../../../agent-research/2610.28380-oo-harness/">实现解读</a> · <a href="#qa-5d4d6c07f614cbe3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aptamer-lab-loop" data-paper-title="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery Agent Google Research 2026-10-17 该研究把计算设计与真实实验测量放进多轮反馈闭环，让Agent利用成功和失败证据调整下一轮策略。关键不是把Agent多跑几轮，而是实物测量可以否定计算评分；论文显示一些预测代理与实际测量不一致。这里仅讨论研究编排与证据边界，不提供生物实验操作流程。 完整实验成本过高，不复现（审查 DONE）。Google优先资料收录；完整实验成本过高，不复现（审查 DONE）。没有低成本代理被标成实现，不进入自动训练队列。完整研究需要专业实验室、物理测量与多轮7–10天反馈周期，无法在单A100/A30或本地Mac低成本完成。依据Results R.1/Figure1直接标记成本过高，不复现（审查 DONE），未启动模型下载、实验运行或无意义代理测试。  科学研究与实验闭环 物理实验反馈 Agent 运行流程与自进化：改的是哪一层 真实实验反馈为什么不能由计算代理高分替代，也不能跨轮直接算成固定测试提升？ 计算评分可能与现实测量不一致，闭环的价值就在于新测量能够否定预测并保留失败证据。不同轮次改变候选和策略，命中比例还受所选分布影响，不是同一测试集上的可比机器学习分数；这里评价研究编排，不据此推出具体实验操作建议。 例如一轮专挑代理认为最优的候选、下一轮转向探索，二者命中比例差异可能来自选择范围，不能直接称模型泛化提高。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-aptamer-lab-loop-d80e05ef" class="ar-learning-paper-anchor"></span>
<h2 id="qa-356a38d089051a53">真实实验反馈为什么不能由计算代理高分替代，也不能跨轮直接算成固定测试提升？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaptamer-lab-loop">Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>计算评分可能与现实测量不一致，闭环的价值就在于新测量能够否定预测并保留失败证据。不同轮次改变候选和策略，命中比例还受所选分布影响，不是同一测试集上的可比机器学习分数；这里评价研究编排，不据此推出具体实验操作建议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一轮专挑代理认为最优的候选、下一轮转向探索，二者命中比例差异可能来自选择范围，不能直接称模型泛化提高。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与评测；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24806v1">原论文</a> · <a href="../../../../agent-research/2610.24806-aptamer-lab-loop/">实现解读</a> · <a href="#qa-356a38d089051a53">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:athanor" data-paper-title="Athanor: An Agent-Native System for Autonomous Post-Training Research" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Athanor: An Agent-Native System for Autonomous Post-Training Research Agent ByteDance / Duke University 2026-10-15 研究 Agent 选择数据、训练算法和阶段组合；独立服务执行异步任务、去污染、冻结评测并保存 checkpoint 谱系。团队共享实验记录与模型，组合 SFT、RL、模型合并及自蒸馏；外部教师调用被禁止。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。不运行完整研究 campaign，不将现有 Evolve 改名冒充 Athanor。无研究自动化实现、benchmark分数或 GPU回执；不把资料链接宣称为 Evolve 集成。范围见本批验收合同。只做论文解读和原图收录。原配置为四个商业研究 Agent 各占八卡节点，合计约12000美元；超过本轮单 A100/A30资源，不启动探跑。成本过高，不复现（审查 DONE）。  递归自改进 自主研究 多 Agent 协作 Agent 运行流程与自进化：改的是哪一层 独立训练服务为什么还需要冻结评测与 checkpoint 谱系？ 异步实验会产生多个数据、算法和阶段组合，仅看文件名无法确定结果来自哪条训练链。谱系保存可追溯父子关系，冻结评测减少标准随搜索漂移，最终 held-out 则隔离研究者选择；一次开发最高分可能只是噪声，不能立刻称为稳健能力提升。 例如某模型经过 SFT、合并再自蒸馏，若不记录父 checkpoint，就难解释哪次改动导致分数变化或复现同一候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-athanor-3414bb2a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2fa991bc91763fd2">独立训练服务为什么还需要冻结评测与 checkpoint 谱系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aathanor">Athanor: An Agent-Native System for Autonomous Post-Training Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>异步实验会产生多个数据、算法和阶段组合，仅看文件名无法确定结果来自哪条训练链。谱系保存可追溯父子关系，冻结评测减少标准随搜索漂移，最终 held-out 则隔离研究者选择；一次开发最高分可能只是噪声，不能立刻称为稳健能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某模型经过 SFT、合并再自蒸馏，若不记录父 checkpoint，就难解释哪次改动导致分数变化或复现同一候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21055">原论文</a> · <a href="../../../../agent-research/2610.21055-athanor/">实现解读</a> · <a href="#qa-2fa991bc91763fd2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auto-sft" data-paper-title="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning Agent Tsinghua University 2026-10-15 自动后训练研究若让一个 Agent 同时读训练日志、分析失败、改数据、提交任务，可能在上下文中积累大量执行输出，最终只反复调整混合比例。AutoSFT 将 Meta Agent、执行子代理、四种分析视角与数据合成分开：执行侧只返回可追溯产物，分析侧从数据、失败、训练信号、研究历史提出不同方案，Meta Agent 决定下一轮的数据干预。原文 §2–4 干预不局限于筛行或生成：可以调类别比例、删除、修复、替换回答、定向合成和调整顺序。这六类是作者对实际动作的事后归类，不是给分析Agent预设的固定菜单。 完整实验成本过高，不复现（审查 DONE）；高成本资料收录。完整实验成本过高，不复现（审查 DONE）；没有本地模型实现、控制器fixture、假 Adapter 或 evolve 接入。原文配置 Qwen3-1.7B-Base、Megatron-LM、8×H800。一次20轮运行约 130 GPU小时；Agent与数据合成约 95美元/轮、1900美元/次。执行子代理、独立语义审查和每轮从基座训练都是定义机制的重要部分，不能删成几条规则后称为AutoSFT复现。原文 Appendix D  递归自改进 自动后训练与数据研究 Agent 运行流程与自进化：改的是哪一层 每轮都从同一基座重新训练，为什么对数据研究归因很重要？ 这样跨轮变化主要来自数据池、配比与顺序，而非上一轮权重继续学习产生的累积效应。固定训练器和预算后登记干预假设，才能比较预期机制是否出现；不同分析视角提出方案不等于已经执行实验，也不能事后按分数改写原始预测。 例如第二轮修复了错误回答数据，应从同一基座重训；若续训第一轮模型，提升还混入更多训练步数的影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-auto-sft-e69c4a3b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f387b0e8c600a749">每轮都从同一基座重新训练，为什么对数据研究归因很重要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aauto-sft">AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这样跨轮变化主要来自数据池、配比与顺序，而非上一轮权重继续学习产生的累积效应。固定训练器和预算后登记干预假设，才能比较预期机制是否出现；不同分析视角提出方案不等于已经执行实验，也不能事后按分数改写原始预测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第二轮修复了错误回答数据，应从同一基座重训；若续训第一轮模型，提升还混入更多训练步数的影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式：固定训练合同的形式化；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22194">原论文</a> · <a href="../../../../agent-research/2610.22194-auto-sft/">实现解读</a> · <a href="#qa-f387b0e8c600a749">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsiflow" data-paper-title="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent Agent Beihang University 2026-10-15 性能瓶颈可能来自模型参数、执行 Harness，也可能只是当前交付物。固定只改其中一项，或固定交替更新，未必对应当前失败。RSIFlow 的 Meta-Agent 用任务执行证据选择 Model / Harness / Artifacts 干预，比较同父代、同任务批的候选，并从成功和失败中维护技能。Meta 模型参数保持固定；本地遵循已发布的技能记忆变体，不把它扩写成任意自改代码系统。 原文五轮、每轮最多两个候选、4B/8B、SFT/GRPO、16K/32K 与 8 ranks，加上 Meta API 和真实工具执行，完整多臂评测对单 A100/A30 或 Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。实现固定 callback 控制器与技能经验记录，不训练语言模型，不执行任意元程序自改，不进入统一 Evolve 晋级。每 seed 初始化三批、每批四个数值 fixture 和五个独立报告任务；私有目标值仅由 evaluator 闭包持有。M/H/A proposer 只拿公共任务、父代标量分数及已有训练技能。  RSI 自我改进与工作流 Agent 运行流程与自进化：改的是哪一层 比较候选时为什么必须都从同一个冻结父代出发？ 若第一个候选的修改混入第二个，无法把收益归因到所选 Model、Harness 或 Artifacts 干预。统一父代和任务批提供配对基线，仅有效且严格提升者接受，失败后仍从原父代再试；技能可来自训练经验，报告集分数不能反向泄漏给维护过程。 例如先改 prompt 后又换模型，应分别对同一父配置评估，不能把第二次累计收益全算给模型替换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-rsiflow-bf0996bb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8c0705993316eab7">比较候选时为什么必须都从同一个冻结父代出发？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsiflow">RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若第一个候选的修改混入第二个，无法把收益归因到所选 Model、Harness 或 Artifacts 干预。统一父代和任务批提供配对基线，仅有效且严格提升者接受，失败后仍从原父代再试；技能可来自训练经验，报告集分数不能反向泄漏给维护过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先改 prompt 后又换模型，应分别对同一父配置评估，不能把第二次累计收益全算给模型替换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21791">原论文</a> · <a href="../../../../agent-research/2610.21791-rsiflow/">实现解读</a> · <a href="#qa-8c0705993316eab7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:terminal-rsi" data-paper-title="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine Agent Tencent Hy Frontier / National University of Singapore 2026-10-15 终端 Agent 既要从验证成功的轨迹里学会可重现行为，也要把稀疏完成反馈传给很早的动作。Terminal-RSI 交替 RSR 轨迹改写和保留 critic 权重的 RPR，阶段开始时先校准 critic；提出 TB-GAE 用交互 turn 时钟而非 observation 文本长度衰减，并用 family 校准的 FDR 过渡到严格完成优先的 SPR。 原文 Qwen3.8-27B、256K、多阶段分布式训练、3,000 任务及长终端环境，对单 A100/A30/Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 数值诊断。只执行 TB-GAE、精确 chunk 续接和 FDR/SPR，不执行 shell、终端 Agent 或 PPO 训练。原文 TB-GAE 的 checkpoint 实际使用情况有明确未核实边界。每 seed 初始化 20 个 generated-token value，五个 turn、一个终端奖励；再插入 40 个 observation，核对结果不变。  RSI Agent RL 长程终端任务 Agent 运行流程与自进化：改的是哪一层 TB-GAE 为什么按交互 turn 衰减，而不是按 observation 文本长度衰减？ 工具输出长度并不对应额外决策时间，若把长 observation 当很多递推节点，早期动作的信用会被无意义地过度衰减。方法仅在生成 token 上递推，同 turn 不衰减、跨 turn 才用折扣；分块续接还需 value 和 advantage，计算切块不是环境终止。 例如两次执行结果相同，一份日志十行、一份千行，不应仅因冗长日志就把之前动作的奖励信用压低更多。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-terminal-rsi-d5ceabe6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b604c93ca728c134">TB-GAE 为什么按交互 turn 衰减，而不是按 observation 文本长度衰减？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aterminal-rsi">Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Hy Frontier / National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具输出长度并不对应额外决策时间，若把长 observation 当很多递推节点，早期动作的信用会被无意义地过度衰减。方法仅在生成 token 上递推，同 turn 不衰减、跨 turn 才用折扣；分块续接还需 value 和 advantage，计算切块不是环境终止。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次执行结果相同，一份日志十行、一份千行，不应仅因冗长日志就把之前动作的奖励信用压低更多。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22192">原论文</a> · <a href="../../../../agent-research/2610.22192-terminal-rsi/">实现解读</a> · <a href="#qa-b604c93ca728c134">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:torsi" data-paper-title="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock Agent Peking University / Samsung Research 2026-10-14 游戏在模型推理时继续前进，观测时正确的动作在执行时可能已失效。原文 §3–4提出 RealtimeBench 的 paused／live／accelerated 时钟比较，及 Two-Timescale Offline Recursive Self-Improvement：快学生在实况中独立行动，慢教师只在两次尝试之间读失败轨迹、在 feedback 保存状态上离线练习，并改写可复用指导。指导冻结后只由独立 validation 决定是否替换；test 不参与修订或选择。 成本过高，不复现（审查 DONE）。本地未运行 Mario/Snake 等引擎、Jev、教师或异步控制，不把数值 fixture 当实时能力评测；evaluation_protocol_interface / L1 CPU。只有时钟、反馈隔离与指导接受协议，没有实时游戏或模型能力复现。每 seed 随机生成 16 个计时事件和 12 个数值 validation 行；独立检查 action age 比只统计响应延迟多出的调度时间、严格增益、平局与下降拒绝。teacher 仅收到人工 feedback 轨迹。逐 seed 实测和来源 hash 见 CPU 产物，不代表游戏进展或 Jev 改善。  RSI 实时决策与离线指导进化 Agent 运行流程与自进化：改的是哪一层 response latency 与 action age 为什么不能混成一个指标？ 前者到模型返回为止，后者还包含排队和应用动作的时间；实况环境持续变化，返回快也可能因应用晚而失效。慢教师只能在尝试之间用反馈练习和改指导，再由独立 validation 决定是否替换，不能在 live test 中偷看未来状态修正动作。 例如模型一秒内决定跳跃，命令又排队两秒才执行，此时障碍已移走；动作年龄三秒，比单纯响应一秒更能解释失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-torsi-cd7ddf6f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1cb9b40763fb601f">response latency 与 action age 为什么不能混成一个指标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atorsi">The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University / Samsung Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者到模型返回为止，后者还包含排队和应用动作的时间；实况环境持续变化，返回快也可能因应用晚而失效。慢教师只能在尝试之间用反馈练习和改指导，再由独立 validation 决定是否替换，不能在 live test 中偷看未来状态修正动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型一秒内决定跳跃，命令又排队两秒才执行，此时障碍已移走；动作年龄三秒，比单纯响应一秒更能解释失败。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20665">原论文</a> · <a href="../../../../agent-research/2610.20665-torsi/">实现解读</a> · <a href="#qa-1cb9b40763fb601f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harmony-harness" data-paper-title="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses Agent Google Cloud AI Research / Carnegie Mellon University 2026-10-10 单目标演化可能通过放松检查提高功能分数，同时损害安全。Harmony Harness 将功能与安全保持为两个独立目标：每个偏好向量维护一个框架，候选只替换邻域中更差的框架。工具、技能、逻辑分别记录在通用或环境专属范围，再由组合器为当前任务选择执行 DAG。图为依据原文 Figure 1 重绘的机制说明，不是本地执行记录。原图与正文。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。Gemini 3.6 Flash 承担 proposer 与 solver；三次独立运行、多代多子问题，真实 Docker 构建和 exploit 评估主导耗时（§5、附录 C/G/I）。完整实验成本过高，不复现（审查 DONE）；成本判断源于论文规模，不是本地测量。  自进化与经验复用 多目标Harness演化 Agent 运行流程与自进化：改的是哪一层 为什么 min(功能成功率,安全成功率) 不能当成联合成功率？ 两项边际率可能来自不同轨迹，只有同一次执行同时满足两条件才算联合成功。多目标搜索用偏好与邻域替换维护取舍，不能靠放松安全提高功能总分；最终选择集和 held-out 也要分开，否则框架会把报告环境当搜索反馈使用。 例如十次里八次功能成功、八次安全通过，但失败恰好错开，联合可能只有六次；取两项最小值八次会高估。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harmony-harness-9020f112" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4036ffbcca6c9c03">为什么 min(功能成功率,安全成功率) 不能当成联合成功率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharmony-harness">Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两项边际率可能来自不同轨迹，只有同一次执行同时满足两条件才算联合成功。多目标搜索用偏好与邻域替换维护取舍，不能靠放松安全提高功能总分；最终选择集和 held-out 也要分开，否则框架会把报告环境当搜索反馈使用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十次里八次功能成功、八次安全通过，但失败恰好错开，联合可能只有六次；取两项最小值八次会高估。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15150v1">原论文</a> · <a href="../../../../agent-research/2610.15150-harmony-harness/">实现解读</a> · <a href="#qa-4036ffbcca6c9c03">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness2" data-paper-title="Harness²: Recursive Agent Harnessing for an Open World" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness²: Recursive Agent Harnessing for an Open World Agent Northwestern University 2026-10-09 Harness 是模型外的提示、工具、记忆、技能、脚本、子代理和中间件。论文在不改模型权重的前提下，把“改进当前任务执行方式”和“积累以后如何改进的经验”连接起来。它不要求任务答案、评分细则或验证器：先观察执行，再提出通用候选与领域候选，执行二者，最后按行为差异组合，而不是把某个评分函数冒充正确性判定。论文 §2 高成本完整实验：成本过高，不复现（审查 DONE）。编辑器诊断脚本中的正数过滤，通用分支更新约束，领域分支删除不符合公开任务的过滤，组合分支合并实际执行过的修改。component_only / L1 CPU 控制器与接口。真实执行 Python 探针，但 editor、selector 是确定性机制测试替身；不是模型支持的 Agent 能力评测，也不是已接入 Evolve。只使用 Python 标准库，无模型下载、API 凭证或 GPU。产物存在时拒绝覆盖，重复执行请换输出路径。实际探针在临时目录运行可信 Python 脚本，单次 subprocess 超时 5 秒；  规划、搜索与反思 Harness 与自我改进 Agent 运行流程与自进化：改的是哪一层 没有答案或评分细则时，Propose–Probe–Compose 怎样避免把自评分当作正确性 oracle？ 候选先真实执行，再依据公开任务与行为差异组合，证据来自轨迹和产物而非隐藏答案。多产物选择时匿名化，减少按 harness 身份偏好；这种开放改进不提供绝对正确保证，选择、反思和 probe 调用也必须计成本，不能只统计最终执行次数。 例如通用候选强化验证、领域候选改善检索，实际跑后可组合有用部分；不能因为其中一个自称最好就当作已经正确完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harness2-5c8a24eb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cde1fd9a6db3a6fc">没有答案或评分细则时，Propose–Probe–Compose 怎样避免把自评分当作正确性 oracle？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness2">Harness²: Recursive Agent Harnessing for an Open World</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选先真实执行，再依据公开任务与行为差异组合，证据来自轨迹和产物而非隐藏答案。多产物选择时匿名化，减少按 harness 身份偏好；这种开放改进不提供绝对正确保证，选择、反思和 probe 调用也必须计成本，不能只统计最终执行次数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如通用候选强化验证、领域候选改善检索，实际跑后可组合有用部分；不能因为其中一个自称最好就当作已经正确完成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14224">原论文</a> · <a href="../../../../agent-research/2610.14224-harness2/">实现解读</a> · <a href="#qa-cde1fd9a6db3a6fc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-anything" data-paper-title="RSI-Anything: Unlocking Recursive Self-Improvement with World Models" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Anything: Unlocking Recursive Self-Improvement with World Models Agent PhAI Labs / The Chinese University of Hong Kong 2026-10-09 候选先经世界模型预测，再向外部验证申请反馈；反馈更新持久 policy/workflow，可靠性不足且数据/预算足够时适配 predictor。只有组件检查和配对兼容性检查均通过的版本进入下一轮。事实来源：原文全文。 保持 concept_demo / L1、diagnostic_only=true、capability_comparison=false、evolve_promotion_eligible=false，不进入 Evolve 晋级。当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始 policy workflow 与初始 predictor 配对；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  recursive-self-improvement world-model compatibility-retention Agent 运行流程与自进化：改的是哪一层 组件分别通过检查后，为什么还需要 policy 与 predictor 的配对兼容性检查？ 策略可能依赖旧预测器的状态或假设，新预测器单独准确也可能与它不兼容。配对检查验证一起运行的行为，失败就整体回退到已知配对；预测器适配还需可靠性不足、数据和预算充足，不能把每轮自动重训或单模块通过当成系统已进步。 例如预测器更新了动作编码顺序，策略仍按旧顺序读取，二者单测可过却联调失败，应回退整个组合而非只记各自通过。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-rsi-anything-7f27ef73" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7477ecc5f73f2292">组件分别通过检查后，为什么还需要 policy 与 predictor 的配对兼容性检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsi-anything">RSI-Anything: Unlocking Recursive Self-Improvement with World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PhAI Labs / The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略可能依赖旧预测器的状态或假设，新预测器单独准确也可能与它不兼容。配对检查验证一起运行的行为，失败就整体回退到已知配对；预测器适配还需可靠性不足、数据和预算充足，不能把每轮自动重训或单模块通过当成系统已进步。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预测器更新了动作编码顺序，策略仍按旧顺序读取，二者单测可过却联调失败，应回退整个组合而非只记各自通过。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13912">原论文</a> · <a href="../../../../reproductions/2610.13912-rsi-anything/">实现解读</a> · <a href="#qa-7477ecc5f73f2292">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoalloc" data-paper-title="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution Agent King Abdullah University of Science and Technology 2026-10-08 模型选择 Full、Partial 或 Discard，得到 Partial 证据后再选择继续/停止。已观察案例更新固定语句经验并反思策略；影子策略共享同一证据，以漏掉新最佳的次数优先、再比较评测成本。拒绝候选以概率做反事实评测，避免选择性反馈。原文达到基线时 Full 数减少 59–82%，同预算成绩提高 8.7–12.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。复用真实 Linux bubblewrap/prlimit Circle26 程序环境，可信几何检查器评分而非模型自报，沙箱失败即拒绝运行。Circle26 无 Partial，因此此运行只允许 Full/Discard。经验 ADD/UPDATE/DELETE 不允许 UPDATE 重写语句，未观察案例不可当证据，最多四条活跃/暂定和四条陈旧经验。  程序进化 评测预算 策略自进化 Agent 运行流程与自进化：改的是哪一层 为什么被 Discard 的候选还要以概率做反事实评测？ 若只评估被选中的程序，分配策略看不到错过优良候选的情况，容易把自身偏好越学越确定。随机反事实检查揭示漏掉新最佳的风险，影子策略还需共享同一证据；这些 Full 调用同样消耗预算，不能为显示节省而排除探索与 warmup。 例如筛选器把一个陌生写法丢弃，偶尔完整评测却发现它更好；这类证据才能纠正“陌生即低质”的选择性反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-evoalloc-9a5390ec" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ea25419573e292b0">为什么被 Discard 的候选还要以概率做反事实评测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoalloc">EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · King Abdullah University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若只评估被选中的程序，分配策略看不到错过优良候选的情况，容易把自身偏好越学越确定。随机反事实检查揭示漏掉新最佳的风险，影子策略还需共享同一证据；这些 Full 调用同样消耗预算，不能为显示节省而排除探索与 warmup。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如筛选器把一个陌生写法丢弃，偶尔完整评测却发现它更好；这类证据才能纠正“陌生即低质”的选择性反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12086">原论文</a> · <a href="../../../../agent-research/2610.12086-evoalloc/">实现解读</a> · <a href="#qa-ea25419573e292b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mass" data-paper-title="Recursive Self-Improvement through Multi-Agent Self-Supervision" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Recursive Self-Improvement through Multi-Agent Self-Supervision Agent UC Berkeley 2026-10-08 同一模型执行、提出工作流并成对评价。固定权重下搜索后，独立采集轨迹，以 Bradley–Terry 排名选择前 K−1 条训练、第 K 条验证；仅移除编排者初始工作流提示，保留工作者分工。助手 token 的 SFT 更新权重后再重复。原文 Qwen3.6-27B 两轮在研究任务中提高单位输出 token 表现约 1.2–1.6 倍，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。真实共享 checkpoint 完成两轮搜索、裁判、轨迹采集与 LoRA SFT。本地为固定两工作者和一编排者的有界文本工作流族，可改变角色指令和传递内容；未接入任意工作流图、qwen-code 文件/终端工具，因此不是完整科研 coding-agent 复现。  递归自改进 工作流搜索 多智能体自监督 Agent 运行流程与自进化：改的是哪一层 为什么训练前要移除编排者初始工作流提示，却保留工作者分工？ 初始提示承载搜索得到的工作流，直接保留可能让训练只学依赖这段外部说明，而非吸收有用协作行为。保留角色分工仍维持实际执行结构，再对助手 token 做监督；Bradley–Terry 排名用于筛轨迹，也不能把自评排序直接当独立任务能力证明。 例如搜索提示详细规定先检索再核对，训练移除该起始说明，让模型从成功执行学习流程，但保留实际检索者和核对者的对话。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-mass-a7f2d6e4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f2ba8ed1f9334346">为什么训练前要移除编排者初始工作流提示，却保留工作者分工？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amass">Recursive Self-Improvement through Multi-Agent Self-Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>初始提示承载搜索得到的工作流，直接保留可能让训练只学依赖这段外部说明，而非吸收有用协作行为。保留角色分工仍维持实际执行结构，再对助手 token 做监督；Bradley–Terry 排名用于筛轨迹，也不能把自评排序直接当独立任务能力证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索提示详细规定先检索再核对，训练移除该起始说明，让模型从成功执行学习流程，但保留实际检索者和核对者的对话。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12176">原论文</a> · <a href="../../../../agent-research/2610.12176-mass/">实现解读</a> · <a href="#qa-f2ba8ed1f9334346">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento3" data-paper-title="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks Agent University College London 2026-10-08 冻结 LLM 将黑盒交互证据写成可修改规则册，再编译为世界模型。新代码必须同时通过语义忠实性判断和全部历史逐格回放；规划失配会触发修复。多个模型共享历史，按不同完整计划的等价类均匀抽样，而非按重复模型投票。论文第 2 节 当前实现为 L1 核心机制实验，不是原论文完整基准。已在 NVIDIA A100-SXM4-80GB 上实际运行冻结 Qwen2.5-7B；生成模型在第一次真实动作后被证伪，修复未成功，最终没有可用世界模型，任务也未完成。这是一条保留失败的机制执行记录，不是能力提升结果。  世界模型 反思与记忆 Agent 运行流程与自进化：改的是哪一层 历史回放为什么不能每一步都用下一张真实观察重置模拟状态？ 逐步重置会掩盖世界模型误差的累积，使错误模型看似每步都符合历史。连续回放从初始观察仅初始化一次，后续状态全由模型转移产生，才检验规则册能否真正解释轨迹；语义忠实性也需另查，单纯拟合有限历史不等于通用正确。 例如模型第一步把门位置算错，若第二步直接塞回真实截图，错误就被擦掉；连续回放则会让偏差在后续观察中暴露。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-memento3-dd7ada6c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-81dc7395c90b6e8d">历史回放为什么不能每一步都用下一张真实观察重置模拟状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemento3">Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University College London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐步重置会掩盖世界模型误差的累积，使错误模型看似每步都符合历史。连续回放从初始观察仅初始化一次，后续状态全由模型转移产生，才检验规则册能否真正解释轨迹；语义忠实性也需另查，单纯拟合有限历史不等于通用正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型第一步把门位置算错，若第二步直接塞回真实截图，错误就被擦掉；连续回放则会让偏差在后续观察中暴露。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11794">原论文</a> · <a href="../../../../agent-research/2610.11794-memento3/">实现解读</a> · <a href="#qa-81dc7395c90b6e8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frugalevo" data-paper-title="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution Agent National University of Singapore 2026-10-02 FrugalEvo 把程序优化拆成高成本模型提出策略、低成本模型执行和改进代码，按预算内整条最佳成绩曲线评价搜索效率。先试跑多种策略再排序，失败时保留父程序追加反馈，取得改进后重新锚定，并用岛屿档案保存不同程序。 本地独立实现与公开任务小预算验证。不是原论文 API 模型、美元成本或完整 20 任务结果的复现；尚未接入统一 Evolve 控制器。共享前缀字节顺序已实现；当前 Transformers 后端没有跨请求 KV 前缀缓存，cached_input_tokens=0，不声称复现论文缓存加速。需要 Linux、可用的 bubblewrap/prlimit、CUDA 和预先下载的公开 checkpoint。生成程序在无网络、无工作区/凭据/模型缓存挂载的沙箱中运行；沙箱不能启动时拒绝执行，没有裸 exec 回退。  程序进化 成本约束 强弱模型协作 Agent 运行流程与自进化：改的是哪一层 为什么高成本模型提出策略后，还要由低成本模型反复执行，并评价整条最佳曲线？ 策略构思与局部代码迭代所需能力和费用不同，分层让昂贵调用集中在方向选择。失败时保留父程序追加反馈，改进后再锚定，岛屿档案保护多样性；整条预算内最佳曲线反映多快找到有用方案，而非只在最后挑一次幸运高分。 例如强模型提出向量化方向，小模型负责多个等价实现试验；同预算下更早得到可用加速，比最后一次偶然最好更稳定有意义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-frugalevo-468f3ba3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-08a5a44572618256">为什么高成本模型提出策略后，还要由低成本模型反复执行，并评价整条最佳曲线？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afrugalevo">FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略构思与局部代码迭代所需能力和费用不同，分层让昂贵调用集中在方向选择。失败时保留父程序追加反馈，改进后再锚定，岛屿档案保护多样性；整条预算内最佳曲线反映多快找到有用方案，而非只在最后挑一次幸运高分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如强模型提出向量化方向，小模型负责多个等价实现试验；同预算下更早得到可用加速，比最后一次偶然最好更稳定有意义。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03675">原论文</a> · <a href="../../../../agent-research/2610.03675-frugalevo/">实现解读</a> · <a href="#qa-08a5a44572618256">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seer-forecasting" data-paper-title="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting Agent Google Cloud AI Research / University of Virginia 2026-10-02 数值历史可能缺少外部事件信息，普通 RAG 又不会从预测错误中修订检索方法。SEER 保持预测模型权重不变，把上下文拆成检索记忆、筛选记忆和因果知识。只有过去结果真正可见后，才从预测轨迹中分别更新两类记忆与知识；容量不足时压缩，而不是无限追加。图按原文 Figure 2 与 §3 重绘。原图及方法。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。完整协议涉及 Gemini 3.1 Pro/Flash、Claude 4.6 Sonnet/4.8 Opus，多轮搜索、LEAF 事实核验与顺序回测（§4.1）。闭源调用与六领域完整成本无法用廉价只读检查可靠固定；成本过高，不复现（审查 DONE）。  自进化与经验复用 时间约束事件检索与预测 Agent 运行流程与自进化：改的是哪一层 为什么预测结果成熟后才能反思，测试窗口还必须冻结记忆与因果知识？ 未来真值在预测时不可见，提前用它更新检索或筛选会泄漏结果；测试期间继续按测试误差改记忆，也会把报告集变成训练反馈。分开检索记忆、筛选记忆和知识有助定位错误来源，但事件时间与实际可获得时间仍须独立核对。 例如预测下周销量时，周末才公布的新闻不能回填周一输入；测试结束后知道的销量也不能用于重写同一测试的检索策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-seer-forecasting-fb9c59fb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6d160d05f468f8ca">为什么预测结果成熟后才能反思，测试窗口还必须冻结记忆与因果知识？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aseer-forecasting">SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未来真值在预测时不可见，提前用它更新检索或筛选会泄漏结果；测试期间继续按测试误差改记忆，也会把报告集变成训练反馈。分开检索记忆、筛选记忆和知识有助定位错误来源，但事件时间与实际可获得时间仍须独立核对。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预测下周销量时，周末才公布的新闻不能回填周一输入；测试结束后知道的销量也不能用于重写同一测试的检索策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.04109v1">原论文</a> · <a href="../../../../agent-research/2610.04109-seer-forecasting/">实现解读</a> · <a href="#qa-6d160d05f468f8ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sentry" data-paper-title="Sentry: Learning to Recover from LLM Agent Failures at Test Time" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Sentry: Learning to Recover from LLM Agent Failures at Test Time Agent Stanford University 2026-10-02 Sentry 不把所有失败经验长期塞进 Agent 上下文，而是先识别当前行为失败，再按类别和标签检索相关恢复建议。外部验证器只看后续可观察进展、不看任务奖励，确认恢复后才把经验写入 playbook；动作格式错误走单独的硬修复路径。 未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。独立控制器与真实 checkpoint 的小预算工具任务验证；未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。数据使用 HotpotQA 官方 Hugging Face 镜像的 validation parquet。脚本校验固定 SHA-256，并按题目 ID 哈希排序；前 4 题建立记忆，之后 16 题保留给接口开发，再后 8 题作隔离对照。它们均来自官方 dev，不是官方 test。  失败恢复 条件记忆 测试时学习 Agent 运行流程与自进化：改的是哪一层 恢复建议为什么只有经后续可观察进展验证后才写入 playbook？ 失败后提出建议只是猜测，若直接永久保存，错误补救会成为新污染。外部验证器看后续行为是否真正恢复，不读取任务奖励来给行动者答案，再按失败类别检索适用经验；格式错误另走硬修复路径，避免把机械纠错与语义恢复混成一类能力。 例如建议“刷新登录”后若仍循环报错就不应入库；只有观察到继续完成后续步骤，才形成可供相似失败复用的证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-sentry-acd21bdd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2ae4b0a62a5f04d6">恢复建议为什么只有经后续可观察进展验证后才写入 playbook？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asentry">Sentry: Learning to Recover from LLM Agent Failures at Test Time</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>失败后提出建议只是猜测，若直接永久保存，错误补救会成为新污染。外部验证器看后续行为是否真正恢复，不读取任务奖励来给行动者答案，再按失败类别检索适用经验；格式错误另走硬修复路径，避免把机械纠错与语义恢复混成一类能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如建议“刷新登录”后若仍循环报错就不应入库；只有观察到继续完成后续步骤，才形成可供相似失败复用的证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02994">原论文</a> · <a href="../../../../agent-research/2610.02994-sentry/">实现解读</a> · <a href="#qa-2ae4b0a62a5f04d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:active-saddler" data-paper-title="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization Agent POSTECH 2026-10-01 把反复出现的失败模式动态实例化为非平稳 bandit arm；课程控制器在发现新场景和重访已知弱点之间选择，并随 harness 修复结果更新优先级。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Harness 优化 主动课程 RSI Agent 运行流程与自进化：改的是哪一层 失败模式作为非平稳 bandit arm，为什么必须允许发现新场景并重访旧弱点？ harness 修复后旧失败的收益会变化，固定课程可能不断测试已经解决的问题，又漏掉新暴露的缺陷。控制器用价值与探索项安排预算，周期性引入未见场景，保持发现和验证两种需求；次数或优先级只是课程信号，不能当模型能力指标。 例如超时问题已修好后应降低重复练习，但仍偶尔复测防回退，同时探索此前没有覆盖的权限错误场景。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-active-saddler-9c3dd285" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bd6e14f5e934fc23">失败模式作为非平稳 bandit arm，为什么必须允许发现新场景并重访旧弱点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aactive-saddler">ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · POSTECH</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>harness 修复后旧失败的收益会变化，固定课程可能不断测试已经解决的问题，又漏掉新暴露的缺陷。控制器用价值与探索项安排预算，周期性引入未见场景，保持发现和验证两种需求；次数或优先级只是课程信号，不能当模型能力指标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如超时问题已修好后应降低重复练习，但仍偶尔复测防回退，同时探索此前没有覆盖的权限错误场景。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00906">原论文</a> · <a href="../../../../agent-research/2610.00906-active-saddler/">实现解读</a> · <a href="#qa-bd6e14f5e934fc23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:flowright" data-paper-title="It Takes Workflows to Evolve Better Workflows" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="It Takes Workflows to Evolve Better Workflows Agent William &amp; Mary 2026-10-01 利用 workflow 拓扑把稀疏结果拆为层级、结构感知的 role credit，使单角色自进化、上下游协同或多 Agent co-evolution 可共用一个 harness。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  工作流进化 多 Agent 层级奖励 Agent 运行流程与自进化：改的是哪一层 为什么结构感知 role credit 要看 workflow 拓扑，而不是把终局回报平均给所有角色？ 不同角色的位置与下游影响不同，平均分配掩盖了某个无效节点或关键上游。拓扑权重把有效性和后继关系纳入分配，使单角色改进与上下游协同共享控制框架；这种分摊仍是信用规则，不等于已识别各角色的真实因果贡献，须用执行对照检验。 例如检索者的错误传给三个下游，修复它可能比润色末段更重要；拓扑能提示这种传播范围，而非按人数平分奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-flowright-b0c3085e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bff8ef395659ef30">为什么结构感知 role credit 要看 workflow 拓扑，而不是把终局回报平均给所有角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aflowright">It Takes Workflows to Evolve Better Workflows</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · William &amp; Mary</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同角色的位置与下游影响不同，平均分配掩盖了某个无效节点或关键上游。拓扑权重把有效性和后继关系纳入分配，使单角色改进与上下游协同共享控制框架；这种分摊仍是信用规则，不等于已识别各角色的真实因果贡献，须用执行对照检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如检索者的错误传给三个下游，修复它可能比润色末段更重要；拓扑能提示这种传播范围，而非按人数平分奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01026">原论文</a> · <a href="../../../../agent-research/2610.01026-flowright/">实现解读</a> · <a href="#qa-bff8ef395659ef30">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rule-evolve" data-paper-title="Self-Evolving Coding Rules for AI Coding Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Evolving Coding Rules for AI Coding Agents Agent 原文首页未列第一作者机构 2026-09-30 维护 coding rule 候选池，由 mutator 生成变体，再只用隔离 validation evaluator 选择并回写更优规则。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选变异后的 validation 选择；不调用 LLM mutator。执行候选变异后的 validation 选择；不调用 LLM mutator。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RSI Coding Agent 规则进化 Agent 运行流程与自进化：改的是哪一层 为什么 mutator 生成的 coding rule 不能依据生成者自评直接回写？ 规则看似合理可能只适合少数样例，甚至损害旧行为。隔离 validation evaluator 对候选池和变体统一测量，再选择回写，把提议与接纳的依据分开；用于选择的数据也已属于开发反馈，最终测试不能继续交给 mutator 反复调整。 例如新规则要求所有函数都重试，文字上强调鲁棒性，却可能让非幂等调用重复执行；独立验证才能发现这种退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-rule-evolve-f1ced1e2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e4060e8043015f09">为什么 mutator 生成的 coding rule 不能依据生成者自评直接回写？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arule-evolve">Self-Evolving Coding Rules for AI Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规则看似合理可能只适合少数样例，甚至损害旧行为。隔离 validation evaluator 对候选池和变体统一测量，再选择回写，把提议与接纳的依据分开；用于选择的数据也已属于开发反馈，最终测试不能继续交给 mutator 反复调整。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新规则要求所有函数都重试，文字上强调鲁棒性，却可能让非幂等调用重复执行；独立验证才能发现这种退化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00650">原论文</a> · <a href="../../../../agent-research/2610.00650-rule-evolve/">实现解读</a> · <a href="#qa-e4060e8043015f09">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:branch-mixture" data-paper-title="Mixture of Self-Improving Branches for Agent Harness Optimization" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Mixture of Self-Improving Branches for Agent Harness Optimization Agent 原文首页未列机构 2026-09-29 将 harness 搜索拆成多条分支，每条分支维护不同的开发子集和 proposal policy；全分支都解决的样本被移除，具有分支区分度的样本被保留，部署时由只看输入特征的 router 选择开发集冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 优化 分支搜索 RSI Agent 运行流程与自进化：改的是哪一层 为什么全分支都解决的开发样本可移除，仍要保留有分支区分度的样本？ 共同已会样本对判断分支差异的信息量较小，持续占预算会稀释真正弱点。各分支保留有辨别力的子集与提议策略，部署 router 再按输入选择开发冠军；这种适应性开发集不能被当独立最终测试，路由也不能读取测试标签来挑赢家。 例如所有分支都能做简单排序，只有图搜索任务能区分两套策略，课程可把更多预算留给后者而不重复刷共同强项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-branch-mixture-203f2124" class="ar-learning-paper-anchor"></span>
<h2 id="qa-aabf9fb0b40ae634">为什么全分支都解决的开发样本可移除，仍要保留有分支区分度的样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abranch-mixture">Mixture of Self-Improving Branches for Agent Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共同已会样本对判断分支差异的信息量较小，持续占预算会稀释真正弱点。各分支保留有辨别力的子集与提议策略，部署 router 再按输入选择开发冠军；这种适应性开发集不能被当独立最终测试，路由也不能读取测试标签来挑赢家。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如所有分支都能做简单排序，只有图搜索任务能区分两套策略，课程可把更多预算留给后者而不重复刷共同强项。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37834">原论文</a> · <a href="../../../../agent-research/2609.37834-branch-mixture/">实现解读</a> · <a href="#qa-aabf9fb0b40ae634">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-skills" data-paper-title="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI Agent Apodex / University of Illinois Urbana-Champaign 2026-09-29 从开发任务的 harness 执行反馈中提炼包含 when、provide、use 的 meta-skill，再冻结技能库；测试任务只检索相关 meta-skill 来构建新 harness，不用测试结果反向修改技能库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 设计 Meta-skill RSI Agent 运行流程与自进化：改的是哪一层 为什么 meta-skill 要显式写 when、provide、use，而不只留一句“以后多验证”？ when 指出触发条件，provide 说明该补什么资源，use 规定如何把它接进流程，三者把宽泛建议转成可检索的设计知识。技能库在开发后冻结，测试只检索构建 harness；若再用测试成败改库，就不再是对未见任务的固定技能迁移。 例如“当工具输出不完整时，提供原始日志入口，并先核对再重试”比一句“更谨慎”更容易形成具体运行组件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-meta-skills-2db3e168" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6a366ef3d536dcd6">为什么 meta-skill 要显式写 when、provide、use，而不只留一句“以后多验证”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ameta-skills">Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apodex / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>when 指出触发条件，provide 说明该补什么资源，use 规定如何把它接进流程，三者把宽泛建议转成可检索的设计知识。技能库在开发后冻结，测试只检索构建 harness；若再用测试成败改库，就不再是对未见任务的固定技能迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“当工具输出不完整时，提供原始日志入口，并先核对再重试”比一句“更谨慎”更容易形成具体运行组件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38143">原论文</a> · <a href="../../../../agent-research/2609.38143-meta-skills/">实现解读</a> · <a href="#qa-6a366ef3d536dcd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:video-rsi" data-paper-title="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution Agent Tsinghua University 2026-09-29 视频 Agent 的执行 trace 只包含当前 harness 选择观察的证据，因此失败解释可能无法区分。Video-RSI 让模型回访原训练视频、主动收集额外观察，形成可检验诊断并改写 harness；候选只有在准确率提高且成本不恶化，或成本下降且准确率不恶化时才保留。 复现级别：L1 接纳规则。复现级别：L1 接纳规则。实现准确率—视觉成本双目标的 Pareto 接纳；未在视频 benchmark 上自动改写并执行完整 harness。未把训练视频私有答案或 example-level score 暴露给候选 harness；当前不含真实视频解码、代码改写 sandbox 和跨代停止条件，因而暂不登记为 Evolve 可执行 operator。  RSI Harness 演化 视频理解 Agent Agent 运行流程与自进化：改的是哪一层 为什么只读失败 trace 可能不足以确定视频 Agent 的取证问题？ trace 只记录旧 harness 选择看到的部分，没看到的关键帧无法从日志中重新推断。回访训练视频补观察，可检验是漏证据还是推理错，再改接口；接纳保持准确率与成本双门槛，不能用加权总分掩盖明显质量或费用退化。 例如旧策略只取视频开头，关键动作在末尾，失败日志没有该动作；回看原训练视频才能验证应修改采样而非答案措辞。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-video-rsi-6a868dfd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8a4bdd987fbb14e7">为什么只读失败 trace 可能不足以确定视频 Agent 的取证问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avideo-rsi">Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>trace 只记录旧 harness 选择看到的部分，没看到的关键帧无法从日志中重新推断。回访训练视频补观察，可检验是漏证据还是推理错，再改接口；接纳保持准确率与成本双门槛，不能用加权总分掩盖明显质量或费用退化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧策略只取视频开头，关键动作在末尾，失败日志没有该动作；回看原训练视频才能验证应修改采样而非答案措辞。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37950">原论文</a> · <a href="../../../../agent-research/2609.37950-video-rsi/">实现解读</a> · <a href="#qa-8a4bdd987fbb14e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-learning" data-paper-title="Harness Learning Enables Generalizable Test-Time Adaptation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness Learning Enables Generalizable Test-Time Adaptation Agent Johns Hopkins University 2026-09-28 论文把测试时适配的对象从模型参数转为可执行 harness：proposer 根据真实执行反馈修改验证、解释器、检索或重试组件；底层任务模型保持冻结，多轮执行后保留更有效的脚手架。 复现级别：L1 无 gold 机制诊断。复现级别：L1 无 gold 机制诊断。实现由执行反馈驱动的 harness revision policy 与多轮适配；冻结任务策略，不读取答案或计划。当前没有接入通用 Agent runner 或 Evolve，因为二者尚不能安全执行任意 harness 并完成隔离验证；本页不把规则化 mini-suite 的成功率宣称为 Agent 能力提升。HarnessProposer 与 adapt_harness 可接入外部真实执行 callback；汇总诊断见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Harness 学习 测试时适配 元学习 Agent 运行流程与自进化：改的是哪一层 冻结任务模型权重，为什么仍然可以发生测试时适配？ 可适配对象是模型外可执行组件，如验证、解释器、检索或重试协议；执行反馈改变这些脚手架，进而影响同一模型之后的行为。它不同于微调，也不允许借接口把隐藏答案送给 proposer；本地分类策略更新更不能冒充整篇真实 LLM 适配链。 例如模型不变，但失败后为 shell 输出加入截断与错误定位器，下一次更易处理；改的是交互运行方式而非神经权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harness-learning-a67122de" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a6385fbc64265b44">冻结任务模型权重，为什么仍然可以发生测试时适配？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-learning">Harness Learning Enables Generalizable Test-Time Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johns Hopkins University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可适配对象是模型外可执行组件，如验证、解释器、检索或重试协议；执行反馈改变这些脚手架，进而影响同一模型之后的行为。它不同于微调，也不允许借接口把隐藏答案送给 proposer；本地分类策略更新更不能冒充整篇真实 LLM 适配链。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型不变，但失败后为 shell 输出加入截断与错误定位器，下一次更易处理；改的是交互运行方式而非神经权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35738">原论文</a> · <a href="../../../../agent-research/2609.35738-harness-learning/">实现解读</a> · <a href="#qa-a6385fbc64265b44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx-model-replay" data-paper-title="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems Agent Kuaishou 2026-09-24 早期 AgentX 关注从研究构想到实现、评估的单次闭环；AgentX-Model 追问一次实验之后如何决定下一次做什么。Research Agent 负责跨论文和实验路径提出、独立审查研究问题；Model Agent 接收获批提案，在固定业务输入与预测任务下多轮改代码、训练、测量，并返回中间最佳实现、负结果和未解问题。两者通过提案而非共享完整工作日志衔接。 本地保真度：公开数据机制验证（concept demo）。本地保真度：公开数据机制验证（concept demo）。执行了双角色提案/审查/调查接口、四类动作和带依赖的结果盲回放；角色由确定性规则驱动，实验图由 MovieLens-1M 上实际训练的六个轻量模型节点组成。它不是论文的私有 473 节点历史图、LLM Agent 系统或线上 A/B 复现。本地两个“Agent”是有隔离接口的确定性执行角色，而非论文使用的 Pi/Claude Code/GLM、独立 LLM 审查或自动编程；模型变种也是预设可执行候选，非系统自主发明。六节点依赖图来自本仓库真实公开数据实验，不是作者 473 节点生产日志；  研究自动化 依赖约束历史回放 Agent 运行流程与自进化：改的是哪一层 Research Agent 与 Model Agent 为什么通过提案衔接，而不是共享完整实验日志？ 提案明确研究问题、约束和获批方向，模型实现侧再在固定业务输入与预测任务下多轮试验，减少两侧上下文相互淹没。返回中间最佳、负结果与未解问题支持下一研究决策；衔接的是证据化研究接口，不是只报最后一个漂亮分数。 例如研究侧提出检验长历史压缩假设，模型侧反馈最佳版本及失效条件，研究者据此决定下一假设，无需读每次编译输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-agentx-model-replay-82b929d4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-900b22adccd50c90">Research Agent 与 Model Agent 为什么通过提案衔接，而不是共享完整实验日志？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentx-model-replay">Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提案明确研究问题、约束和获批方向，模型实现侧再在固定业务输入与预测任务下多轮试验，减少两侧上下文相互淹没。返回中间最佳、负结果与未解问题支持下一研究决策；衔接的是证据化研究接口，不是只报最后一个漂亮分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如研究侧提出检验长历史压缩假设，模型侧反馈最佳版本及失效条件，研究者据此决定下一假设，无需读每次编译输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30001">原论文</a> · <a href="../../../../agent-research/2609.30001-agentx-model/">实现解读</a> · <a href="#qa-900b22adccd50c90">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sciencebuddy" data-paper-title="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents Agent Gen-Verse research collaboration 2026-09-15 内层递归演化交互 harness，外层用成功轨迹更新科学 Agent 策略。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双层状态更新；没有连接真实实验室环境。本地执行双层状态更新；没有连接真实实验室环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  科学 Agent 递归自进化 Agent 运行流程与自进化：改的是哪一层 内层演化 harness、外层更新策略，为什么不能简化成同一轮反复改 prompt？ 两层修改对象不同：内层优化交互方式，外层利用成功执行轨迹改变科学 Agent 的参数策略，后者又影响下一轮内层搜索。只有真实执行、筛选和训练组成闭环，才体现递归中的递归；参考门控函数或合成统计不能替代这些模型与环境过程。 例如先找到更好的实验检查流程，再用其成功轨迹训练 Agent，使之后更会使用该流程；仅把提示重写三遍没有第二层更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-sciencebuddy-cd9b47fe" class="ar-learning-paper-anchor"></span>
<h2 id="qa-83f78a9174f9ee29">内层演化 harness、外层更新策略，为什么不能简化成同一轮反复改 prompt？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asciencebuddy">ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Gen-Verse research collaboration</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两层修改对象不同：内层优化交互方式，外层利用成功执行轨迹改变科学 Agent 的参数策略，后者又影响下一轮内层搜索。只有真实执行、筛选和训练组成闭环，才体现递归中的递归；参考门控函数或合成统计不能替代这些模型与环境过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先找到更好的实验检查流程，再用其成功轨迹训练 Agent，使之后更会使用该流程；仅把提示重写三遍没有第二层更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17523">原论文</a> · <a href="../../../../agent-research/2609.17523-sciencebuddy/">实现解读</a> · <a href="#qa-83f78a9174f9ee29">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cobra-skills" data-paper-title="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization Agent The Chinese University of Hong Kong, Shenzhen 2026-09-10 把技能优化视为动态候选空间中的预算化 contextual bandit，优先评估高收益或高信息量技能，再依据执行反馈演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能进化 Contextual bandit Agent 运行流程与自进化：改的是哪一层 动态技能候选为什么适合预算化 contextual bandit，而不是只按历史最高分排序？ 技能收益依赖当前任务，新增或修订候选又缺乏历史数据。上下文 bandit 在利用已知高收益与探索高信息量候选之间分配评测预算，再用真实反馈演化；仅看历史最高值会偏向早期幸运技能，忽略新任务条件和未评候选的不确定性。 例如旧技能擅长文件操作，新任务转向网页，多给新候选少量试验可能比持续验证旧冠军更有信息价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-cobra-skills-f91c343f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0f97cc70d3ab4160">动态技能候选为什么适合预算化 contextual bandit，而不是只按历史最高分排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acobra-skills">COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>技能收益依赖当前任务，新增或修订候选又缺乏历史数据。上下文 bandit 在利用已知高收益与探索高信息量候选之间分配评测预算，再用真实反馈演化；仅看历史最高值会偏向早期幸运技能，忽略新任务条件和未评候选的不确定性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧技能擅长文件操作，新任务转向网页，多给新候选少量试验可能比持续验证旧冠军更有信息价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11682">原论文</a> · <a href="../../../../agent-research/2609.11682-cobra-skills/">实现解读</a> · <a href="#qa-0f97cc70d3ab4160">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ecdysis" data-paper-title="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents Agent Chengdu Institute of Computer Applications, Chinese Academy of Sciences 2026-09-10 聚合跨任务重复失败以区分模型偶发错误和 harness 系统缺陷，再由 FDCR 多角色诊断形成修复规格。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Harness 自进化 失败诊断 Agent 运行流程与自进化：改的是哪一层 为什么同一种失败要跨任务聚合，才能判断是 harness 系统缺陷？ 单次出错可能来自模型随机性或特殊题意，重复出现的模式才更提示共同运行接口存在问题。多角色诊断把这些证据转成可验证修复规格，避免每遇一次失败就改全局框架；聚合相关性仍不是充分因果证明，修复后必须做受影响行为对照。 例如许多任务都因日志被截断而漏掉错误码，比单题猜错更支持检查输出接口；应针对截断机制修复而非泛泛换模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-ecdysis-3d533dc6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bdf6583baffee7b9">为什么同一种失败要跨任务聚合，才能判断是 harness 系统缺陷？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aecdysis">Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chengdu Institute of Computer Applications, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次出错可能来自模型随机性或特殊题意，重复出现的模式才更提示共同运行接口存在问题。多角色诊断把这些证据转成可验证修复规格，避免每遇一次失败就改全局框架；聚合相关性仍不是充分因果证明，修复后必须做受影响行为对照。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如许多任务都因日志被截断而漏掉错误码，比单题猜错更支持检查输出接口；应针对截断机制修复而非泛泛换模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11677">原论文</a> · <a href="../../../../agent-research/2609.11677-ecdysis/">实现解读</a> · <a href="#qa-bdf6583baffee7b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:maple" data-paper-title="MAPLE: Memory-Augmented Planning with Language and Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MAPLE: Memory-Augmented Planning with Language and Evolution Agent Harbin Institute of Technology, Shenzhen 2026-09-10 MAPLE 把自然语言优化知识变成可持续修改的程序状态：生成候选、检查可执行性、接纳更好的方案，并把已接受程序带到后续问题中继续进化，而不是每次从零提示。 复现级别：持久状态机制诊断。复现级别：持久状态机制诊断。实现候选方案接纳、跨任务复用和版本化状态，不执行论文的数学优化器或 LLM 代码生成。三种子结果见 metrics/mini-suite-seeds42-44.json。本地只接纳由非空命名操作构成的公开计划并验证后续复用；没有运行作者求解器、训练模型或外部工具，因此不把 mini-suite 成功率作为论文能力复现。  持久化优化规划 Agent 运行流程与自进化：改的是哪一层 被接受程序作为后续问题的起点，为什么比每次重新提示更能积累优化知识？ 程序状态保留已经验证可执行的结构和取舍，下一题在其上修改，而不是靠自然语言重新回忆所有细节。接纳规则阻止未执行的想法直接覆盖可靠父本；跨问题继续进化也要检查任务差异，不能把某一实例的特化程序当成普适最佳。 例如上一题已实现可靠的数据解析，下一题可以在此基础改目标函数，而不每次从空脚本重新生成并重犯格式错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-maple-2e42a8d7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fedfb0ce31b03cfb">被接受程序作为后续问题的起点，为什么比每次重新提示更能积累优化知识？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amaple">MAPLE: Memory-Augmented Planning with Language and Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>程序状态保留已经验证可执行的结构和取舍，下一题在其上修改，而不是靠自然语言重新回忆所有细节。接纳规则阻止未执行的想法直接覆盖可靠父本；跨问题继续进化也要检查任务差异，不能把某一实例的特化程序当成普适最佳。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如上一题已实现可靠的数据解析，下一题可以在此基础改目标函数，而不每次从空脚本重新生成并重犯格式错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11636">原论文</a> · <a href="../../../../agent-research/2609.11636-maple/">实现解读</a> · <a href="#qa-fedfb0ce31b03cfb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:procedural-graphs" data-paper-title="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents Agent Google 2026-09-08 方法把成功经验从自然语言片段提升为 procedure–relation–procedure 图。新经验先局部化为候选图编辑，再经过 held-out 验证门才写入长期结构，减少错误经验污染。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现 procedure–relation–procedure 图和保守编辑门，不包含 LLM 生成或真实环境执行。三种子 evomem-mini 结果见 metrics/mini-suite-seeds42-44.json。本地编辑门以“已建立路线必须保留首尾节点”为确定性代理；策略看不到隐藏答案/计划，也未调用真实工具，因此仅验证图更新与拒绝路径。  自进化程序图 Agent 运行流程与自进化：改的是哪一层 为什么经验写入要先局部化为图编辑，再经过 held-out 门？ 图中的过程关系会影响多条执行路径，整段新经验直接覆盖可能污染无关技能。局部编辑明确改哪条节点或关系，held-out 再检验是否超越原轨迹的偶然成功；验证通过只支持该评测范围，不能把训练轨迹上的自洽当作全局结构已可靠。 例如只新增“认证失败后刷新令牌”的恢复边，不重写整个上传图，再用未参与提议的任务检查是否引入重复认证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-procedural-graphs-6aeeaceb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-495c2876d5383645">为什么经验写入要先局部化为图编辑，再经过 held-out 门？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprocedural-graphs">Procedural Graphs: Self-Evolving Execution Structures for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图中的过程关系会影响多条执行路径，整段新经验直接覆盖可能污染无关技能。局部编辑明确改哪条节点或关系，held-out 再检验是否超越原轨迹的偶然成功；验证通过只支持该评测范围，不能把训练轨迹上的自洽当作全局结构已可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只新增“认证失败后刷新令牌”的恢复边，不重写整个上传图，再用未参与提议的任务检查是否引入重复认证。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09153">原论文</a> · <a href="../../../../agent-research/2609.09153-procedural-graphs/">实现解读</a> · <a href="#qa-495c2876d5383645">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnesslens" data-paper-title="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification Agent Fudan University 2026-08-27 固定验证集浪费 rollout 且会用平均分掩盖局部回退。HarnessLens 从执行轨迹提出修改，只在受影响行为对应的任务上成对验证，并要求证据能归因到候选修改。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现行为任务选择、配对验证与可归因证据门。未运行论文四个完整 benchmark；本地执行冻结测试集和无 answer/guide 接口的真实工具反馈协议。ToolRoute-L2.1 三 seed：joint success 0.8194，plan F1 0.8372，平均成本 5.0419。  行为相关 Harness 验证 Agent 运行流程与自进化：改的是哪一层 行为感知的成对验证为什么比固定验证集平均分更能发现局部回退？ 修改只影响部分行为，混入大量无关题会稀释差异并浪费 rollout。针对受影响任务比较父子框架，要求变化可归因于该修改，才能辨别真正修复与偶然波动；局部通过仍需明确适用范围，不能从一个行为提升推导全部任务均变好。 例如只改重试组件，应配对检查超时和恢复任务；大量简单成功题可能把某个重试死循环的退化淹没在平均分里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harnesslens-7d46fb0d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5970447fb917ddcb">行为感知的成对验证为什么比固定验证集平均分更能发现局部回退？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnesslens">Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>修改只影响部分行为，混入大量无关题会稀释差异并浪费 rollout。针对受影响任务比较父子框架，要求变化可归因于该修改，才能辨别真正修复与偶然波动；局部通过仍需明确适用范围，不能从一个行为提升推导全部任务均变好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只改重试组件，应配对检查超时和恢复任务；大量简单成功题可能把某个重试死循环的退化淹没在平均分里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27311">原论文</a> · <a href="../../../../agent-research/2608.27311-harnesslens/">实现解读</a> · <a href="#qa-5970447fb917ddcb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jit-agent" data-paper-title="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution Agent LV-NUS Lab 2026-08-26 把 harness 形式化为 memory、planning、action protocol、tools/skills 四个可生成模块；模型按任务生成、失败后修复，并从历史配置 archive 蒸馏可迁移模式。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。JIT harness 在训练任务上即时写入/修复可复用路由，在 validation/test 冻结后仅通过公开 observation、工具元数据和真实调用反馈执行；不存在 answer、guide 或 reference-plan 接口。  Harness 即时生成与进化 Agent 运行流程与自进化：改的是哪一层 为什么按任务生成 harness 时，要把 memory、planning、action protocol、tools 分成模块？ 不同任务瓶颈可能位于不同层，模块化让生成与失败修复定位具体对象，也便于从配置档案提炼可迁移模式。即用即生成不等于无需验证，每个模块仍要满足运行合同；仅改提示内容却未生成相应工具或状态接口，不能算四模块都已实现。 例如长任务需要换记忆策略、短计算题只需配置计算工具，不必每次重建全部组件，也不能让两者混用不兼容协议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-jit-agent-92c11b63" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6f7f1b4cdc3ad572">为什么按任务生成 harness 时，要把 memory、planning、action protocol、tools 分成模块？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajit-agent">JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LV-NUS Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同任务瓶颈可能位于不同层，模块化让生成与失败修复定位具体对象，也便于从配置档案提炼可迁移模式。即用即生成不等于无需验证，每个模块仍要满足运行合同；仅改提示内容却未生成相应工具或状态接口，不能算四模块都已实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长任务需要换记忆策略、短计算题只需配置计算工具，不必每次重建全部组件，也不能让两者混用不兼容协议。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25593">原论文</a> · <a href="../../../../agent-research/2608.25593-jit-agent/">实现解读</a> · <a href="#qa-6f7f1b4cdc3ad572">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openloopevolve" data-paper-title="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks Agent Tsinghua University 2026-08-10 把 observation/planning/memory/action/verification/recovery 等 Loop Policy 资产版本化，以 Champion–Challenger、发布监控和回滚治理进化。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  自进化 策略治理 Agent 运行流程与自进化：改的是哪一层 Champion–Challenger 之外，为什么还需要发布监控与回滚？ 离线候选优于冠军不保证上线分布和长期交互同样稳定，监控发现新退化后需要可追溯地恢复旧版本。版本化涵盖观察、规划、记忆、验证和恢复等资产，避免只记录模型名；发布治理是进化闭环的一部分，不能以候选评测一次通过替代。 例如挑战者在开发任务更省调用，上线却在权限错误时循环，监控应定位版本并回滚到旧策略，而不是继续无界试错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-openloopevolve-709aab65" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0f68c8d27ea47fea">Champion–Challenger 之外，为什么还需要发布监控与回滚？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aopenloopevolve">OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线候选优于冠军不保证上线分布和长期交互同样稳定，监控发现新退化后需要可追溯地恢复旧版本。版本化涵盖观察、规划、记忆、验证和恢复等资产，避免只记录模型名；发布治理是进化闭环的一部分，不能以候选评测一次通过替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如挑战者在开发任务更省调用，上线却在权限错误时循环，监控应定位版本并回滚到旧策略，而不是继续无界试错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09380">原论文</a> · <a href="../../../../agent-research/2608.09380-openloopevolve/">实现解读</a> · <a href="#qa-0f68c8d27ea47fea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx" data-paper-title="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems Agent Kuaishou 2026-06-26 传统推荐迭代需要工程师串联假设、生产代码、上线 A/B 和归因，经验也难以跨实验积累。AgentX 将流程改造成四阶段闭环：Brainstorm Agent 从实验库、系统知识、数据分析和外部论文生成有证据的候选；Developing Agent 在仓库约束下实现并验证；Evaluation Agent 用护栏否决的线上 A/B 判断；最后以 SGPO 从成功与失败轨迹更新 Agent harness。 复现级别：核心闭环 mini-suite。复现级别：核心闭环 mini-suite。本地实现 Brainstorm、Developing、Evaluation 与 Harness Evolution 四阶段控制流，并验证实验知识复用带来的执行成本下降。本地没有 Kuaishou 内部仓库、流量平台、线上用户或 SGPO 大模型训练，因此不能复现论文的业务增益。mini-suite 验证的是四阶段闭环、正负结果资产化、验证门槛与跨 episode 复用；average proxy cost 仅是控制流成本，不冒充人效、收入或线上时长。  研究自动化 工业推荐 Agent Agent 运行流程与自进化：改的是哪一层 主指标显著改善后，为什么护栏越界仍能否决候选发布？ 推荐系统需要在目标收益与关键约束之间满足共同条件，单指标上涨可能以稳定性或其他重要体验为代价。Evaluation Agent 用线上证据和护栏否决，成功失败都写回实验知识；harness 学习依据完整轨迹，而不是只筛赢家形成乐观偏差。 例如点击率提高却导致关键时延明显越界，不能只拿上涨指标宣称可上线；失败原因也应进入下一轮提案证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-agentx-26ba162a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5c6f98a0c4e7b3e7">主指标显著改善后，为什么护栏越界仍能否决候选发布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentx">AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>推荐系统需要在目标收益与关键约束之间满足共同条件，单指标上涨可能以稳定性或其他重要体验为代价。Evaluation Agent 用线上证据和护栏否决，成功失败都写回实验知识；harness 学习依据完整轨迹，而不是只筛赢家形成乐观偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如点击率提高却导致关键时延明显越界，不能只拿上涨指标宣称可上线；失败原因也应进入下一轮提案证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.26859">原论文</a> · <a href="../../../../agent-research/2606.26859-agentx/">实现解读</a> · <a href="#qa-5c6f98a0c4e7b3e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scientist-one" data-paper-title="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence Agent Google Cloud AI Research 2026-05-25 研究产物看起来完整，仍可能引用虚构、分数无法复算或方法描述与代码不同。CoE 将主张连到可核验来源；独立 I1–I4 检查分数、规则、引用和方法/代码一致性。来源存在不等于主张被支持。原文 §3 与 §5 完整实验成本过高，不复现（审查 DONE）。本地实现低成本 CoE 机械核验内核与语义审计接口，不是完整自主科学家。固定刺激为 L0；完整实验成本过高，不复现（审查 DONE）。canonical evaluator 的可信性、日志是否由实际实验产生、语义判断是否正确仍由上层证据保障；哈希只能证明“相同字节”，不能证明“字节描述了真实实验”。本地不将任意 Python callback 当安全沙箱。  科学研究 Agent 证据链与完整性审计 Agent 运行流程与自进化：改的是哪一层 来源和日志都存在，为什么还要核对 metric、stage、unit 与 direction？ 同一日志可能同时含训练、消融和正式评测，多种数值不能互相替代。主张需连到身份和口径一致的证据，再检查可复算性与方法代码一致性；没有定量主张时溯源率应为空而非满分，来源存在本身也不证明它支持文本结论。 例如日志记录的是训练 loss 下降，报告却写测试准确率提高，即使数字可追溯也不算主张获得对应证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-scientist-one-ba34af9f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0979e17fc2ce7849">来源和日志都存在，为什么还要核对 metric、stage、unit 与 direction？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascientist-one">ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一日志可能同时含训练、消融和正式评测，多种数值不能互相替代。主张需连到身份和口径一致的证据，再检查可复算性与方法代码一致性；没有定量主张时溯源率应为空而非满分，来源存在本身也不证明它支持文本结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如日志记录的是训练 loss 下降，报告却写测试准确率提高，即使数字可追溯也不算主张获得对应证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26340">原论文</a> · <a href="../../../../agent-research/2605.26340-scientist-one/">实现解读</a> · <a href="#qa-0979e17fc2ce7849">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagents" data-paper-title="HyperAgents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HyperAgents Agent University of British Columbia 2026-03-19 把任务 Agent 与修改它的 meta Agent 放入同一可编辑程序，并在开放档案中积累变体；父代概率同时奖励当前性能与较少后代的探索价值，使改进机制本身也可继续被改进。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。三种子诊断：metrics/mechanism-seeds42-44.json  RSI 开放式进化 元认知自修改 Agent 运行流程与自进化：改的是哪一层 父代抽样为什么同时考虑性能和已有后代数？ 只追最高分容易反复扩展同一分支，降低探索多样性；后代数惩罚给较少探索的可行父本机会。任务 Agent 与修改机制都在可编辑程序里，让改进方式本身也能演化；抽样概率只是预算分配，不代表每个后代被接受或性能必然递增。 例如冠军已有二十个子版本，稍弱但只试过一次的父本可获得更多机会，可能发现不同的改进路径而非一直局部打磨。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-hyperagents-ae71283f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1955136546ec1e42">父代抽样为什么同时考虑性能和已有后代数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahyperagents">HyperAgents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of British Columbia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只追最高分容易反复扩展同一分支，降低探索多样性；后代数惩罚给较少探索的可行父本机会。任务 Agent 与修改机制都在可编辑程序里，让改进方式本身也能演化；抽样概率只是预算分配，不代表每个后代被接受或性能必然递增。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如冠军已有二十个子版本，稍弱但只试过一次的父本可获得更多机会，可能发现不同的改进路径而非一直局部打磨。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19461">原论文</a> · <a href="../../../../agent-research/2603.19461-hyperagents/">实现解读</a> · <a href="#qa-1955136546ec1e42">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:polca" data-paper-title="POLCA: Stochastic Generative Optimization with LLM" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="POLCA: Stochastic Generative Optimization with LLM Agent University of Wisconsin-Madison 2026-03-16 随机 minibatch、程序与评估器都会产生噪声。POLCA 不仅保留一次最高分，而是持续更新候选评价历史；Summarizer 形成全局经验，Proposer 利用当前反馈提出参数，语义 epsilon-net 限制冗余候选。原文 §3 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0；优先队列和真实回调接口已实现，没有声称已运行 LLM 优化器或 benchmark 能力。完整实验：成本过高，不复现（审查 DONE）。6 项测试通过，覆盖严格 epsilon 边界、新候选互相过滤、同一有放回 minibatch、跨轮噪声均值/方差、完整输入/输出历史送入 Summarizer/Proposer、预算耗尽及拒绝 test split。诊断记录  Agent 自进化 随机优化 程序搜索 Agent 运行流程与自进化：改的是哪一层 为什么候选评价要维护历史均值，并用语义 epsilon-net 限制冗余？ 随机数据和评估器会带来噪声，一次高分可能是偶然，持续记录提供更稳的候选比较。语义距离约束减少把预算浪费在近似重复提案上，加入新候选后还要重算距离；经验均值规则与理论 UCB 不能混作同一实现，也不能把均值排名当显著性结论。 例如十个候选只是同一提示换标点，语义过滤可少测这些重复项；某方案首轮幸运高分，也应结合后续评价而非永久封王。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-polca-3e1ab10b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d412acefc26869b2">为什么候选评价要维护历史均值，并用语义 epsilon-net 限制冗余？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apolca">POLCA: Stochastic Generative Optimization with LLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin-Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>随机数据和评估器会带来噪声，一次高分可能是偶然，持续记录提供更稳的候选比较。语义距离约束减少把预算浪费在近似重复提案上，加入新候选后还要重算距离；经验均值规则与理论 UCB 不能混作同一实现，也不能把均值排名当显著性结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十个候选只是同一提示换标点，语义过滤可少测这些重复项；某方案首轮幸运高分，也应结合后续评价而非永久封王。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.14769">原论文</a> · <a href="../../../../agent-research/2603.14769-polca/">实现解读</a> · <a href="#qa-d412acefc26869b2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mars-research" data-paper-title="MARS: Modular Agent with Reflective Search for Automated AI Research" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MARS: Modular Agent with Reflective Search for Automated AI Research Agent Google Cloud AI Research 2026-02-02 自动研究不仅要生成正确代码，还需在有限训练时间内分辨改动价值。MARS 使用“设计—拆分—实现”生成模块化仓库，以预算感知 MCTS 选择新方案、改进或调试；比较新旧执行结果和代码差异，提炼解决方案经验与调试经验，供其他搜索分支复用。图按原文 Figure 2 重绘。原文流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。MLE-Bench 包含 75 个竞赛，每竞赛预算 24 小时单张 A100-40GB，另有大内存、存储和闭源 LLM 调用；完整多方法三次评测显然超出短时单卡预算（§5.1）。成本过高，不复现（审查 DONE），不启动下载与竞赛训练来验证成本。  自进化与经验复用 预算感知自动研究 Agent 运行流程与自进化：改的是哪一层 为什么研究搜索的节点价值要同时考虑指标和运行时间？ 有限训练预算下，同等质量但更慢的方案会挤占后续探索，单看分数可能选中不划算的路线。MARS 归一化执行指标并加入时间惩罚，再有界地安排改进或调试；反思经验来自代码差与真实结果，不能用模型预期性能替代节点测量。 例如两种方案都到相近验证分数，一种耗时十倍，预算感知搜索可优先较快者，留下资源检验更多结构假设。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-mars-research-5e806f85" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c36b6b4056dd27e5">为什么研究搜索的节点价值要同时考虑指标和运行时间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amars-research">MARS: Modular Agent with Reflective Search for Automated AI Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有限训练预算下，同等质量但更慢的方案会挤占后续探索，单看分数可能选中不划算的路线。MARS 归一化执行指标并加入时间惩罚，再有界地安排改进或调试；反思经验来自代码差与真实结果，不能用模型预期性能替代节点测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两种方案都到相近验证分数，一种耗时十倍，预算感知搜索可优先较快者，留下资源检验更多结构假设。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02660v1">原论文</a> · <a href="../../../../agent-research/2602.02660-mars-research/">实现解读</a> · <a href="#qa-c36b6b4056dd27e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:self-refine" data-paper-title="Self-Refine" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Refine Agent Carnegie Mellon University 2023-03-30 一次生成很难同时满足所有约束。Self-Refine 让同一个 LLM 先生成初稿，再针对任务维度给出可执行反馈，最后据此改写；若反馈判断已满足要求则停止，不需要额外训练数据、人工反馈或外部 reward model。 Self-Refine 在不更新参数的情况下循环执行“生成—自反馈—改写”，把推理时计算用于发现并修正当前答案的问题。实现显式初稿、约束反馈、修订和停止链路；mini-suite 用确定性 critic 验证状态迁移，没有调用论文中的通用 LLM，也不能用 1.0 成功率替代七项原始 benchmark 结果。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 2.0000，执行 120 次反馈和 120 次 refinement，共记录 240 个 reasoning steps。  自我迭代 Agent 运行流程与自进化：改的是哪一层 同一模型同时写初稿和反馈，为什么还要把反馈作为单独步骤显式生成？ 显式反馈把不满足的约束转成可执行修改方向，使改写不只是随机再采样一遍答案。生成、反馈和精炼承担不同角色，停止仍依赖模型自身判断；无需外部训练并不意味着反馈一定正确，也不能把反复润色当作已经有独立事实验证。 例如初稿遗漏单位，反馈明确指出需补每个数值单位，改写才有具体目标；仅说“再写好一点”很难定位同一缺陷。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-self-refine-16be87c4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-439d518e3a48ecee">同一模型同时写初稿和反馈，为什么还要把反馈作为单独步骤显式生成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aself-refine">Self-Refine</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>显式反馈把不满足的约束转成可执行修改方向，使改写不只是随机再采样一遍答案。生成、反馈和精炼承担不同角色，停止仍依赖模型自身判断；无需外部训练并不意味着反馈一定正确，也不能把反复润色当作已经有独立事实验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如初稿遗漏单位，反馈明确指出需补每个数值单位，改写才有具体目标；仅说“再写好一点”很难定位同一缺陷。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17651">原论文</a> · <a href="../../../../agent-research/2303.17651-self-refine/">实现解读</a> · <a href="#qa-439d518e3a48ecee">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:reflexion" data-paper-title="Reflexion" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Reflexion Agent Northeastern University 2023-03-20 传统 RL 要大量采样与参数更新。Reflexion 把稀疏标量/二值反馈“放大”为可执行的自然语言经验，写入长期 episodic memory；Actor 在下一 trial 读取反思，Evaluator 继续判定成功与否。 本页实现失败反馈 → 语言反思 → 有界 episodic memory → 下一 trial 改进，全程不更新模型权重。实现跨 trial 的失败、语言经验与复用闭环，但反思模板和 evaluator 是确定性的；没有调用 GPT-4、ALFWorld、HotpotQA 或代码执行器。0.9 来自“每个新族首次失败”的可审计协议，不等同 HumanEval pass@1。PlanBench mini 有 12 个重复任务族。每族首次暴露计划错误，Evaluator 失败后生成一条可复用反思；后续 episode 读取当前上下文并执行完整计划。  自我反思 Agent 运行流程与自进化：改的是哪一层 verbal reinforcement 为什么不等于对模型参数做强化学习更新？ 反馈被转换成自然语言经验写入有界 episodic memory，下一次尝试改变的是模型所见上下文，而非通过梯度修改权重。反思能传递比二元成败更具体的经验，但记忆内容仍可能错误，Evaluator 必须继续判定实际执行，不能由反思自称学会。 例如失败后记下“先确认文件路径再编辑”，下一轮读取这句话会改变行为；即使权重完全相同也可表现不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-reflexion-b837a66e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bb3bffbeb91462b9">verbal reinforcement 为什么不等于对模型参数做强化学习更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Areflexion">Reflexion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反馈被转换成自然语言经验写入有界 episodic memory，下一次尝试改变的是模型所见上下文，而非通过梯度修改权重。反思能传递比二元成败更具体的经验，但记忆内容仍可能错误，Evaluator 必须继续判定实际执行，不能由反思自称学会。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如失败后记下“先确认文件路径再编辑”，下一轮读取这句话会改变行为；即使权重完全相同也可表现不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.11366">原论文</a> · <a href="../../../../agent-research/2303.11366-reflexion/">实现解读</a> · <a href="#qa-bb3bffbeb91462b9">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
