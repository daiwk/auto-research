---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 运行流程与自进化：改的是哪一层

[Agent](index.md) / 172 个问题 · 43 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/agent-research/harness-and-self-improvement.md)

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
<p class="ar-learning-status" data-learning-status role="status">172 个问题 · 43 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessmm" data-paper-title="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency Agent Tsinghua University 2026-10-23 Agent 在得到工具反馈后经常再调用模型，即使上一轮推理已确定下一步命令。HarnessMM 的 EDG 只保存先前确实完成语义解析的动作及完整字面参数；GDR 检查前置任务完成、public guard 真和参数闭合，再选一个合格节点或 abstain。不支持的观察、缺少依赖、需要新语义判断时回到原慢 actor。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。无 adapter、operator、运行命令、metrics 或 GPU receipt。本地不实现原生 harness 替代器，不制造 fake callback/receipt，不执行 LLM 生成动作或 shell，不用确定性 fixture 证明节省 token。仅保留规范文献及成本终态；promotion_eligible=false、evolve_integrated=false。既有 Agent tracing 框架不等于本论文已集成。  Agent评测与自进化 原生harness回调替代与成本审计 Agent 运行流程与自进化：改的是哪一层 HarnessMM 为什么认为工具反馈后再调用一次模型，有时是在重复已经完成的判断？ Agent 可能已在上一轮确定某个后续命令，只是等待前置工具返回；条件满足后再让模型重新推理，未必增加新信息。HarnessMM 研究复用这种已确定决策来减少慢调用。需要新的语义理解时仍应交回模型，复用范围不能扩展成任意预测未来动作。 教学例：已明确“文件创建成功后运行指定测试”，成功回执到来时可检查条件并执行；若出现未知错误，则需要重新判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harnessmm-efa1b75e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1f97e11482fc1d08">HarnessMM 为什么认为工具反馈后再调用一次模型，有时是在重复已经完成的判断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnessmm">HarnessMM: Recursive Self-Improvement for Harness Token Efficiency</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Agent 可能已在上一轮确定某个后续命令，只是等待前置工具返回；条件满足后再让模型重新推理，未必增加新信息。HarnessMM 研究复用这种已确定决策来减少慢调用。需要新的语义理解时仍应交回模型，复用范围不能扩展成任意预测未来动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：已明确“文件创建成功后运行指定测试”，成功回执到来时可检查条件并执行；若出现未知错误，则需要重新判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32813v1">原论文</a> · <a href="../../../../agent-research/2610.32813-harnessmm/">实现解读</a> · <a href="#qa-1f97e11482fc1d08">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessmm" data-paper-title="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency Agent Tsinghua University 2026-10-23 Agent 在得到工具反馈后经常再调用模型，即使上一轮推理已确定下一步命令。HarnessMM 的 EDG 只保存先前确实完成语义解析的动作及完整字面参数；GDR 检查前置任务完成、public guard 真和参数闭合，再选一个合格节点或 abstain。不支持的观察、缺少依赖、需要新语义判断时回到原慢 actor。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。无 adapter、operator、运行命令、metrics 或 GPU receipt。本地不实现原生 harness 替代器，不制造 fake callback/receipt，不执行 LLM 生成动作或 shell，不用确定性 fixture 证明节省 token。仅保留规范文献及成本终态；promotion_eligible=false、evolve_integrated=false。既有 Agent tracing 框架不等于本论文已集成。  Agent评测与自进化 原生harness回调替代与成本审计 Agent 运行流程与自进化：改的是哪一层 参数闭合和 guard 为真，为什么还不足以证明省掉一次模型调用既正确又真实？ 这些条件只支持某条动作可被复用，语义是否完成任务仍需原评测器判断。执行证书还要绑定精确参数、前驱回执与工具结果，并审计原注册边界的慢调用确实未发生；理论上可跳过与物理调用实际减少是两件事，失败和恢复成本也不能漏算。 例如图里已有可执行测试命令，系统可直接调用，但必须留下真实测试回执并确认未另发一次慢模型请求，才能计入节省。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessmm" data-paper-title="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency Agent Tsinghua University 2026-10-23 Agent 在得到工具反馈后经常再调用模型，即使上一轮推理已确定下一步命令。HarnessMM 的 EDG 只保存先前确实完成语义解析的动作及完整字面参数；GDR 检查前置任务完成、public guard 真和参数闭合，再选一个合格节点或 abstain。不支持的观察、缺少依赖、需要新语义判断时回到原慢 actor。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。无 adapter、operator、运行命令、metrics 或 GPU receipt。本地不实现原生 harness 替代器，不制造 fake callback/receipt，不执行 LLM 生成动作或 shell，不用确定性 fixture 证明节省 token。仅保留规范文献及成本终态；promotion_eligible=false、evolve_integrated=false。既有 Agent tracing 框架不等于本论文已集成。  Agent评测与自进化 原生harness回调替代与成本审计 Agent 运行流程与自进化：改的是哪一层 复用已确定动作与让模型规划新动作，在线决策自由度有什么区别？ 复用只在先前完成语义解析、参数完整且条件满足的动作中选择，不能凭当前观察自由补参数或发明新步骤；规划则需要解释新信息并构造行动。前者可跳过重复推理，但受覆盖范围限制，不支持或需新判断时应 abstain，不能把结构条件通过当成语义正确。 教学例：已保存的精确测试命令可按成功回执触发；临时发现新的依赖冲突时，不能由复用器猜一个修复命令。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8a00533c8b214ed6">复用已确定动作与让模型规划新动作，在线决策自由度有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnessmm">HarnessMM: Recursive Self-Improvement for Harness Token Efficiency</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>复用只在先前完成语义解析、参数完整且条件满足的动作中选择，不能凭当前观察自由补参数或发明新步骤；规划则需要解释新信息并构造行动。前者可跳过重复推理，但受覆盖范围限制，不支持或需新判断时应 abstain，不能把结构条件通过当成语义正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：已保存的精确测试命令可按成功回执触发；临时发现新的依赖冲突时，不能由复用器猜一个修复命令。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32813v1">原论文</a> · <a href="../../../../agent-research/2610.32813-harnessmm/">实现解读</a> · <a href="#qa-8a00533c8b214ed6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessmm" data-paper-title="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HarnessMM: Recursive Self-Improvement for Harness Token Efficiency Agent Tsinghua University 2026-10-23 Agent 在得到工具反馈后经常再调用模型，即使上一轮推理已确定下一步命令。HarnessMM 的 EDG 只保存先前确实完成语义解析的动作及完整字面参数；GDR 检查前置任务完成、public guard 真和参数闭合，再选一个合格节点或 abstain。不支持的观察、缺少依赖、需要新语义判断时回到原慢 actor。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。无 adapter、operator、运行命令、metrics 或 GPU receipt。本地不实现原生 harness 替代器，不制造 fake callback/receipt，不执行 LLM 生成动作或 shell，不用确定性 fixture 证明节省 token。仅保留规范文献及成本终态；promotion_eligible=false、evolve_integrated=false。既有 Agent tracing 框架不等于本论文已集成。  Agent评测与自进化 原生harness回调替代与成本审计 Agent 运行流程与自进化：改的是哪一层 核算 HarnessMM 成本时，为什么连失败、fallback 和开发阶段都不能漏记？ 完整 episode 要累计所有实际调用的输入输出 token，包括生成复用结构、选择、额外上下文、失败恢复和最终整理，cached input 也属于账目。开发成本另记并按部署次数摊销。少一次慢调用只是局部证据，不能直接推出总 token、延迟或能耗都降低。 教学例：省去一次主模型调用，却新增两次选择与恢复调用，应全部计入；一次性建图成本还需按实际复用任务数摊销。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-403e05ae2ac0edb4">核算 HarnessMM 成本时，为什么连失败、fallback 和开发阶段都不能漏记？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnessmm">HarnessMM: Recursive Self-Improvement for Harness Token Efficiency</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整 episode 要累计所有实际调用的输入输出 token，包括生成复用结构、选择、额外上下文、失败恢复和最终整理，cached input 也属于账目。开发成本另记并按部署次数摊销。少一次慢调用只是局部证据，不能直接推出总 token、延迟或能耗都降低。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：省去一次主模型调用，却新增两次选择与恢复调用，应全部计入；一次性建图成本还需按实际复用任务数摊销。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32813v1">原论文</a> · <a href="../../../../agent-research/2610.32813-harnessmm/">实现解读</a> · <a href="#qa-403e05ae2ac0edb4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:image-rsi" data-paper-title="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation Agent University of Science and Technology of China 2026-10-23 图像生成器即使输出好看，也可能遗漏数量、空间关系、特定文字或身份约束。ImageRSI 固定原始 requirements，以真实生成器产图、五维评审器提供缺陷证据并指导修复，再经独立配对与 holdout 接纳跨任务经验、离线升级 judge，不能靠删掉要求提高分数。经验抽取和经验复用分开：轨迹提议一个包含 Trigger、Negative Trigger、Action、Effect、Side Effects 的策略，不能直接激活。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞审查水位。无可执行 adapter、operator、训练命令、metrics 或 GPU receipt。只保存规范资料条目和原图，不提供可运行模型、打分代理、训练命令或伪单测。真实 generator、语义 judge、repair、paired admission 与 judge post-training 均未实现；promotion_eligible=false、evolve_integrated=false。  Agent评测与自进化 验证驱动图像生成与经验复用 Agent 运行流程与自进化：改的是哪一层 固定原始 requirements 为什么比只提高五维平均分更重要？ 图像修复应满足用户最初的数量、关系、文字与身份约束，不能通过删除难要求或平均抵消缺陷提高分数。五维评分用于定位问题，接纳还受硬 veto；漂亮但遗漏关键条件的图仍应失败，评审得分也不是生成结果本身的事实保证。 例如要求三只杯子且文字准确，画面美感再高也不能抵消只有两只杯子，修复不能把要求改成“两只或三只”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-image-rsi-f8d5a27f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-33b4f94f521f4a4c">固定原始 requirements 为什么比只提高五维平均分更重要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aimage-rsi">ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图像修复应满足用户最初的数量、关系、文字与身份约束，不能通过删除难要求或平均抵消缺陷提高分数。五维评分用于定位问题，接纳还受硬 veto；漂亮但遗漏关键条件的图仍应失败，评审得分也不是生成结果本身的事实保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如要求三只杯子且文字准确，画面美感再高也不能抵消只有两只杯子，修复不能把要求改成“两只或三只”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32120v1">原论文</a> · <a href="../../../../agent-research/2610.32120-image-rsi/">实现解读</a> · <a href="#qa-33b4f94f521f4a4c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:image-rsi" data-paper-title="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation Agent University of Science and Technology of China 2026-10-23 图像生成器即使输出好看，也可能遗漏数量、空间关系、特定文字或身份约束。ImageRSI 固定原始 requirements，以真实生成器产图、五维评审器提供缺陷证据并指导修复，再经独立配对与 holdout 接纳跨任务经验、离线升级 judge，不能靠删掉要求提高分数。经验抽取和经验复用分开：轨迹提议一个包含 Trigger、Negative Trigger、Action、Effect、Side Effects 的策略，不能直接激活。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞审查水位。无可执行 adapter、operator、训练命令、metrics 或 GPU receipt。只保存规范资料条目和原图，不提供可运行模型、打分代理、训练命令或伪单测。真实 generator、语义 judge、repair、paired admission 与 judge post-training 均未实现；promotion_eligible=false、evolve_integrated=false。  Agent评测与自进化 验证驱动图像生成与经验复用 Agent 运行流程与自进化：改的是哪一层 为什么循环内图像评分高，仍不能直接激活抽取出的经验策略？ 同一评审器引导修复又评价收益，可能强化自身偏差。经验需先在相同请求、配置和 seed 下做有无配对，由独立盲评校准，再经独立 holdout 接纳；硬约束也不能被平均高分掩盖，fallback 返回最好图不等于经验或图像已达接纳标准。 例如修复策略让评审偏爱的构图更漂亮，却漏掉指定人数；只有固定要求的独立配对与硬否决检查，才能暴露这种投机。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:image-rsi" data-paper-title="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation Agent University of Science and Technology of China 2026-10-23 图像生成器即使输出好看，也可能遗漏数量、空间关系、特定文字或身份约束。ImageRSI 固定原始 requirements，以真实生成器产图、五维评审器提供缺陷证据并指导修复，再经独立配对与 holdout 接纳跨任务经验、离线升级 judge，不能靠删掉要求提高分数。经验抽取和经验复用分开：轨迹提议一个包含 Trigger、Negative Trigger、Action、Effect、Side Effects 的策略，不能直接激活。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞审查水位。无可执行 adapter、operator、训练命令、metrics 或 GPU receipt。只保存规范资料条目和原图，不提供可运行模型、打分代理、训练命令或伪单测。真实 generator、语义 judge、repair、paired admission 与 judge post-training 均未实现；promotion_eligible=false、evolve_integrated=false。  Agent评测与自进化 验证驱动图像生成与经验复用 Agent 运行流程与自进化：改的是哪一层 经验抽取与独立 paired admission 为什么要分开？ 轨迹提出可复用策略只是候选，有无经验需在相同请求、输入、配置和 seed 下配对，再盲评校准并用独立 holdout。循环内 judge 可能偏爱自己指导的修改，不能直接用它的分数激活经验或让外部 test verdict 指导生成。 例如“加强空间描述”在当前一图有效，只能作为提案；还需新请求配对检查是否也会损害其他关系或风格。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ae7e526e94592742">经验抽取与独立 paired admission 为什么要分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aimage-rsi">ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轨迹提出可复用策略只是候选，有无经验需在相同请求、输入、配置和 seed 下配对，再盲评校准并用独立 holdout。循环内 judge 可能偏爱自己指导的修改，不能直接用它的分数激活经验或让外部 test verdict 指导生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“加强空间描述”在当前一图有效，只能作为提案；还需新请求配对检查是否也会损害其他关系或风格。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32120v1">原论文</a> · <a href="../../../../agent-research/2610.32120-image-rsi/">实现解读</a> · <a href="#qa-ae7e526e94592742">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:image-rsi" data-paper-title="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation Agent University of Science and Technology of China 2026-10-23 图像生成器即使输出好看，也可能遗漏数量、空间关系、特定文字或身份约束。ImageRSI 固定原始 requirements，以真实生成器产图、五维评审器提供缺陷证据并指导修复，再经独立配对与 holdout 接纳跨任务经验、离线升级 judge，不能靠删掉要求提高分数。经验抽取和经验复用分开：轨迹提议一个包含 Trigger、Negative Trigger、Action、Effect、Side Effects 的策略，不能直接激活。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞审查水位。无可执行 adapter、operator、训练命令、metrics 或 GPU receipt。只保存规范资料条目和原图，不提供可运行模型、打分代理、训练命令或伪单测。真实 generator、语义 judge、repair、paired admission 与 judge post-training 均未实现；promotion_eligible=false、evolve_integrated=false。  Agent评测与自进化 验证驱动图像生成与经验复用 Agent 运行流程与自进化：改的是哪一层 最多两次修复后返回最高分 fallback，是否表示 accepted？ 不表示。初始加两次修复的最好候选可作为 fallback，但若未过硬条件仍未接纳。judge 离线 SFT/GRPO 在采集轮之间更新，不在同一评测请求自改；本地真实生成、语义 judge 与训练链都未实现，不应把评分公式写成已验证系统。 例如三张图都拼错指定文字，返回其中最好看的一张仍是未通过，不能因有返回文件就统计 checklist 成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-132ef279c0c873ba">最多两次修复后返回最高分 fallback，是否表示 accepted？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aimage-rsi">ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不表示。初始加两次修复的最好候选可作为 fallback，但若未过硬条件仍未接纳。judge 离线 SFT/GRPO 在采集轮之间更新，不在同一评测请求自改；本地真实生成、语义 judge 与训练链都未实现，不应把评分公式写成已验证系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三张图都拼错指定文字，返回其中最好看的一张仍是未通过，不能因有返回文件就统计 checklist 成功。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32120v1">原论文</a> · <a href="../../../../agent-research/2610.32120-image-rsi/">实现解读</a> · <a href="#qa-132ef279c0c873ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-opt" data-paper-title="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training Agent Purdue University 2026-10-23 单次优化器 Agent 能根据当前训练调整程序，却不会自动把经验带到下一次训练。RSI-Opt 让代码 Agent 根据真实训练证据改写 updater，再将 prompt、自然语言 playbook、代码 library 与 cadence 作为可继承策略，通过外层训练评估递归演化。内层训练保持模型、数据顺序、loss、batch size 和更新步数固定，Agent 在 20 个预定机会读取训练损失/诊断；异常更新器经过短试验后回滚。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。没有可执行 adapter、operator、命令、metrics 或 GPU receipt。仅规范收录方法、风险、原图和成本；没有本地优化器 Agent 或跨run控制器，没有用父策略采样公式冒充整篇论文。promotion_eligible=false、evolve_integrated=false。不会把已有通用进化控制器的名字登记为“已集成”。  Agent评测与自进化 优化器程序与跨运行策略演化 Agent 运行流程与自进化：改的是哪一层 RSI-Opt 为什么研究“怎样改进优化方法”，而不只优化一个固定模型？ 某种优化更新在当前任务有效，不表示它适用于其他模型或训练阶段。RSI-Opt 把更新策略本身作为可改进对象，在受控任务执行后评价其作用，再决定保留哪些变化。它需要区分内层实际优化与外层方法选择，不能由候选描述或单次高分推导普遍收益。 教学例：先让一种更新规则训练小模型，再据同预算结果比较规则；研究目标是更新方法，而不是只记住某次训练的最好参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-rsi-opt-94e59e6e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-066ae36575676705">RSI-Opt 为什么研究“怎样改进优化方法”，而不只优化一个固定模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsi-opt">RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Purdue University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>某种优化更新在当前任务有效，不表示它适用于其他模型或训练阶段。RSI-Opt 把更新策略本身作为可改进对象，在受控任务执行后评价其作用，再决定保留哪些变化。它需要区分内层实际优化与外层方法选择，不能由候选描述或单次高分推导普遍收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：先让一种更新规则训练小模型，再据同预算结果比较规则；研究目标是更新方法，而不是只记住某次训练的最好参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32026v1">原论文</a> · <a href="../../../../agent-research/2610.32026-rsi-opt/">实现解读</a> · <a href="#qa-066ae36575676705">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-opt" data-paper-title="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training Agent Purdue University 2026-10-23 单次优化器 Agent 能根据当前训练调整程序，却不会自动把经验带到下一次训练。RSI-Opt 让代码 Agent 根据真实训练证据改写 updater，再将 prompt、自然语言 playbook、代码 library 与 cadence 作为可继承策略，通过外层训练评估递归演化。内层训练保持模型、数据顺序、loss、batch size 和更新步数固定，Agent 在 20 个预定机会读取训练损失/诊断；异常更新器经过短试验后回滚。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。没有可执行 adapter、operator、命令、metrics 或 GPU receipt。仅规范收录方法、风险、原图和成本；没有本地优化器 Agent 或跨run控制器，没有用父策略采样公式冒充整篇论文。promotion_eligible=false、evolve_integrated=false。不会把已有通用进化控制器的名字登记为“已集成”。  Agent评测与自进化 优化器程序与跨运行策略演化 Agent 运行流程与自进化：改的是哪一层 为什么内层 Agent 看不到最终任务指标，而外层仍能用它评价策略？ 内层依据训练损失与诊断改 updater，若读取最终指标就会直接对评测反馈调参；外层评估固定策略的整体研究表现，承担不同选择职责。跨轮继承提示、库和节奏才是递归部分，归一化聚合也只是排名工具，不能把搜索套件成绩当未见任务泛化。 例如内层只看到训练 loss 决定改更新规则，运行结束后外层比较策略；不能让内层每次试改都先查看最终测试分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-opt" data-paper-title="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training Agent Purdue University 2026-10-23 单次优化器 Agent 能根据当前训练调整程序，却不会自动把经验带到下一次训练。RSI-Opt 让代码 Agent 根据真实训练证据改写 updater，再将 prompt、自然语言 playbook、代码 library 与 cadence 作为可继承策略，通过外层训练评估递归演化。内层训练保持模型、数据顺序、loss、batch size 和更新步数固定，Agent 在 20 个预定机会读取训练损失/诊断；异常更新器经过短试验后回滚。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。没有可执行 adapter、operator、命令、metrics 或 GPU receipt。仅规范收录方法、风险、原图和成本；没有本地优化器 Agent 或跨run控制器，没有用父策略采样公式冒充整篇论文。promotion_eligible=false、evolve_integrated=false。不会把已有通用进化控制器的名字登记为“已集成”。  Agent评测与自进化 优化器程序与跨运行策略演化 Agent 运行流程与自进化：改的是哪一层 为什么跨候选固定模型、数据顺序和更新预算比仅固定 seed 更重要？ 若候选能改模型、loss 或训练时长，分数差就不再只反映 updater 策略。固定合同控制优化对象，异常 updater 短试验后回滚；多个 seed 也不能补救系统性协议差异，或把训练套件指标自动变成未见任务泛化。 例如甲多训练一万步、乙只训练一千步，即使用同 seed 也无法把差值归给优化器策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-24437c49b12176e9">为什么跨候选固定模型、数据顺序和更新预算比仅固定 seed 更重要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsi-opt">RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Purdue University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若候选能改模型、loss 或训练时长，分数差就不再只反映 updater 策略。固定合同控制优化对象，异常 updater 短试验后回滚；多个 seed 也不能补救系统性协议差异，或把训练套件指标自动变成未见任务泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如甲多训练一万步、乙只训练一千步，即使用同 seed 也无法把差值归给优化器策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32026v1">原论文</a> · <a href="../../../../agent-research/2610.32026-rsi-opt/">实现解读</a> · <a href="#qa-24437c49b12176e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-opt" data-paper-title="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training Agent Purdue University 2026-10-23 单次优化器 Agent 能根据当前训练调整程序，却不会自动把经验带到下一次训练。RSI-Opt 让代码 Agent 根据真实训练证据改写 updater，再将 prompt、自然语言 playbook、代码 library 与 cadence 作为可继承策略，通过外层训练评估递归演化。内层训练保持模型、数据顺序、loss、batch size 和更新步数固定，Agent 在 20 个预定机会读取训练损失/诊断；异常更新器经过短试验后回滚。 完整实验：成本过高，不复现（审查 DONE）；仅文献与成本收录。完整实验：成本过高，不复现（审查 DONE）；不自动重试，不阻塞水位。没有可执行 adapter、operator、命令、metrics 或 GPU receipt。仅规范收录方法、风险、原图和成本；没有本地优化器 Agent 或跨run控制器，没有用父策略采样公式冒充整篇论文。promotion_eligible=false、evolve_integrated=false。不会把已有通用进化控制器的名字登记为“已集成”。  Agent评测与自进化 优化器程序与跨运行策略演化 Agent 运行流程与自进化：改的是哪一层 archive 保留低分后代与排除暴露分支各有什么证据边界？ 低分已评估策略仍入 archive，可保存探索与失败经验，不能只存赢家伪造单调改进。曾暴露 held-out 描述的分支即使排除，其总结可能经其他 archive 传播，原文未解决该 provenance 风险；z-score 聚合也不是显著性检验。 例如删除一条污染策略却保留别人读过它后写的总结，信息仍可能间接流入后代，不能据删除动作宣称隔离已证明。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-74594fbd5fa19d33">archive 保留低分后代与排除暴露分支各有什么证据边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsi-opt">RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Purdue University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>低分已评估策略仍入 archive，可保存探索与失败经验，不能只存赢家伪造单调改进。曾暴露 held-out 描述的分支即使排除，其总结可能经其他 archive 传播，原文未解决该 provenance 风险；z-score 聚合也不是显著性检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删除一条污染策略却保留别人读过它后写的总结，信息仍可能间接流入后代，不能据删除动作宣称隔离已证明。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32026v1">原论文</a> · <a href="../../../../agent-research/2610.32026-rsi-opt/">实现解读</a> · <a href="#qa-74594fbd5fa19d33">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-s4" data-paper-title="Evolving Agent Interfaces" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Evolving Agent Interfaces Agent University of California, Santa Barbara 2026-10-20 固定GUI、shell或浏览器接口决定Agent能观察和执行什么。重复点击、逐格编辑、冗长输出等低效行为，既可能来自模型，也可能来自接口设计。Agent S4把接口代码与使用经验一起保存为仓库，固定任务Agent的模型和Harness，由Meta-Agent依据训练轨迹修改仓库。不同于只积累由现有工具组成的技能，它允许改变操作和观察本身。搜索过程中，训练轨迹没有成功标签；验证任务、轨迹、诊断和分数不交给Meta-Agent。验证分数只决定下一步选哪个父仓库。变异修改一个父本，交叉整合两个不同父本； 成本过高，不复现（审查 DONE）。CPU诊断指标与上游工程的差异：本地依据论文保留被淘汰候选及其谱系作为审计记录，未复制上游多岛迁移、SQLite恢复、AWS启动或Landlock沙箱。Repository保存代码文本和使用知识；本模块不exec任意源代码。调用方提供可信的任务Agent、Builder和私有验证grader。这是API数据隔离，不是Python进程沙箱；闭包、回调或字符串本身若已经夹带gold，本模块无法自动识别。真正接入模型时仍须用进程/权限边界保护验证器。  自我进化 接口与Harness进化 Agent 运行流程与自进化：改的是哪一层 进化 interface 与只积累现有工具组成的 skill 有何区别？ skill 通常在固定动作观察接口上组合方法，S4 允许 Meta-Agent 修改接口代码与使用知识，改变任务 Agent 能观察和执行什么。底层任务模型与 harness 固定以隔离接口作用，但新接口仍需真实任务验证，不能只给仓库换版本名。 例如将逐格编辑工具改为批量区域操作属于接口变化，记录“逐格编辑时先排序”只是使用现有工具的经验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-agent-s4-640f2b45" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d5b57cb78fed3749">进化 interface 与只积累现有工具组成的 skill 有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-s4">Evolving Agent Interfaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>skill 通常在固定动作观察接口上组合方法，S4 允许 Meta-Agent 修改接口代码与使用知识，改变任务 Agent 能观察和执行什么。底层任务模型与 harness 固定以隔离接口作用，但新接口仍需真实任务验证，不能只给仓库换版本名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如将逐格编辑工具改为批量区域操作属于接口变化，记录“逐格编辑时先排序”只是使用现有工具的经验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28601">原论文</a> · <a href="../../../../agent-research/2610.28601-agent-s4/">实现解读</a> · <a href="#qa-d5b57cb78fed3749">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-s4" data-paper-title="Evolving Agent Interfaces" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Evolving Agent Interfaces Agent University of California, Santa Barbara 2026-10-20 固定GUI、shell或浏览器接口决定Agent能观察和执行什么。重复点击、逐格编辑、冗长输出等低效行为，既可能来自模型，也可能来自接口设计。Agent S4把接口代码与使用经验一起保存为仓库，固定任务Agent的模型和Harness，由Meta-Agent依据训练轨迹修改仓库。不同于只积累由现有工具组成的技能，它允许改变操作和观察本身。搜索过程中，训练轨迹没有成功标签；验证任务、轨迹、诊断和分数不交给Meta-Agent。验证分数只决定下一步选哪个父仓库。变异修改一个父本，交叉整合两个不同父本； 成本过高，不复现（审查 DONE）。CPU诊断指标与上游工程的差异：本地依据论文保留被淘汰候选及其谱系作为审计记录，未复制上游多岛迁移、SQLite恢复、AWS启动或Landlock沙箱。Repository保存代码文本和使用知识；本模块不exec任意源代码。调用方提供可信的任务Agent、Builder和私有验证grader。这是API数据隔离，不是Python进程沙箱；闭包、回调或字符串本身若已经夹带gold，本模块无法自动识别。真正接入模型时仍须用进程/权限边界保护验证器。  自我进化 接口与Harness进化 Agent 运行流程与自进化：改的是哪一层 为什么子接口仓库即使暂时低分也留在种群，而非只保留严格优于父本的修改？ 进化搜索可能需要经过局部低谷或组合不同改动，保留后代让未来变异和交叉仍能利用其结构。验证分数用于选父本，但验证轨迹和标签不交给 Meta-Agent；改变的是动作与观察接口本身，不能把训练策略误写为逐轮贪心接纳最佳 patch。 例如一次接口改动单独效果一般，却可与另一路观察压缩组合；若立即删除所有低分后代，就失去这类后续组合机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-s4" data-paper-title="Evolving Agent Interfaces" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Evolving Agent Interfaces Agent University of California, Santa Barbara 2026-10-20 固定GUI、shell或浏览器接口决定Agent能观察和执行什么。重复点击、逐格编辑、冗长输出等低效行为，既可能来自模型，也可能来自接口设计。Agent S4把接口代码与使用经验一起保存为仓库，固定任务Agent的模型和Harness，由Meta-Agent依据训练轨迹修改仓库。不同于只积累由现有工具组成的技能，它允许改变操作和观察本身。搜索过程中，训练轨迹没有成功标签；验证任务、轨迹、诊断和分数不交给Meta-Agent。验证分数只决定下一步选哪个父仓库。变异修改一个父本，交叉整合两个不同父本； 成本过高，不复现（审查 DONE）。CPU诊断指标与上游工程的差异：本地依据论文保留被淘汰候选及其谱系作为审计记录，未复制上游多岛迁移、SQLite恢复、AWS启动或Landlock沙箱。Repository保存代码文本和使用知识；本模块不exec任意源代码。调用方提供可信的任务Agent、Builder和私有验证grader。这是API数据隔离，不是Python进程沙箱；闭包、回调或字符串本身若已经夹带gold，本模块无法自动识别。真正接入模型时仍须用进程/权限边界保护验证器。  自我进化 接口与Harness进化 Agent 运行流程与自进化：改的是哪一层 变异一个接口父仓库与交叉两个父仓库，探索的改动来源有什么不同？ 变异从单个父仓库出发修改接口及使用知识，交叉则综合两个不同父本的结构或经验。两者都由无标签训练轨迹支持构建，私有验证结果只用于种群选择，不能传给 Meta-Agent 当答案。交叉增加组合来源，也可能带来不兼容，仍要冻结后代再独立执行评价。 教学例：一个父本改善截图观察，另一个改善批量编辑；交叉可尝试结合二者，而单父变异只依据当前仓库继续修改。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f4a95f794a9b3ec9">变异一个接口父仓库与交叉两个父仓库，探索的改动来源有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-s4">Evolving Agent Interfaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>变异从单个父仓库出发修改接口及使用知识，交叉则综合两个不同父本的结构或经验。两者都由无标签训练轨迹支持构建，私有验证结果只用于种群选择，不能传给 Meta-Agent 当答案。交叉增加组合来源，也可能带来不兼容，仍要冻结后代再独立执行评价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一个父本改善截图观察，另一个改善批量编辑；交叉可尝试结合二者，而单父变异只依据当前仓库继续修改。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28601">原论文</a> · <a href="../../../../agent-research/2610.28601-agent-s4/">实现解读</a> · <a href="#qa-f4a95f794a9b3ec9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-s4" data-paper-title="Evolving Agent Interfaces" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Evolving Agent Interfaces Agent University of California, Santa Barbara 2026-10-20 固定GUI、shell或浏览器接口决定Agent能观察和执行什么。重复点击、逐格编辑、冗长输出等低效行为，既可能来自模型，也可能来自接口设计。Agent S4把接口代码与使用经验一起保存为仓库，固定任务Agent的模型和Harness，由Meta-Agent依据训练轨迹修改仓库。不同于只积累由现有工具组成的技能，它允许改变操作和观察本身。搜索过程中，训练轨迹没有成功标签；验证任务、轨迹、诊断和分数不交给Meta-Agent。验证分数只决定下一步选哪个父仓库。变异修改一个父本，交叉整合两个不同父本； 成本过高，不复现（审查 DONE）。CPU诊断指标与上游工程的差异：本地依据论文保留被淘汰候选及其谱系作为审计记录，未复制上游多岛迁移、SQLite恢复、AWS启动或Landlock沙箱。Repository保存代码文本和使用知识；本模块不exec任意源代码。调用方提供可信的任务Agent、Builder和私有验证grader。这是API数据隔离，不是Python进程沙箱；闭包、回调或字符串本身若已经夹带gold，本模块无法自动识别。真正接入模型时仍须用进程/权限边界保护验证器。  自我进化 接口与Harness进化 Agent 运行流程与自进化：改的是哪一层 BuilderContext 为何不传验证诊断，低分淘汰又为何保留谱系？ 验证只用于父本选择，传诊断会把受保护选择集变成开发反馈。淘汰撤销父本资格但保留审计与最终候选，不能抹去失败历史；本地控制器仅运行可信 callback 与合成任务，不执行任意接口源码或证明真实 GUI 提升。 例如 Meta-Agent 看到验证失败文件名后定向修复，就不再是规定的训练轨迹开发；删除低分记录还会隐藏搜索代价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e85d3ecb46446354">BuilderContext 为何不传验证诊断，低分淘汰又为何保留谱系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-s4">Evolving Agent Interfaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>验证只用于父本选择，传诊断会把受保护选择集变成开发反馈。淘汰撤销父本资格但保留审计与最终候选，不能抹去失败历史；本地控制器仅运行可信 callback 与合成任务，不执行任意接口源码或证明真实 GUI 提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 Meta-Agent 看到验证失败文件名后定向修复，就不再是规定的训练轨迹开发；删除低分记录还会隐藏搜索代价。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28601">原论文</a> · <a href="../../../../agent-research/2610.28601-agent-s4/">实现解读</a> · <a href="#qa-e85d3ecb46446354">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:oo-harness" data-paper-title="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design Agent University of Illinois Urbana-Champaign 2026-10-20 全任务共用一个harness可能互相干扰；为每类任务复制完整实现又难以复用。作者将专用harness写成父类的子类，只覆盖需要改变的prompt、工具或执行hook。发现阶段围绕任务簇改进，部署阶段冻结代码和经验，再用任务及可观察base轨迹选择完整类；父类方法在一个实例里执行，不是额外运行多个祖先Agent。§3 成本过高，不复现（审查 DONE），不下载模型、不试跑完整实验、不自动重试。HarnessDiscovery只接受可信的Python类，不从字符串exec候选。它保存发现阶段的接受和拒绝记录；freeze只复制当前可路由类描述、必要祖先类和路由经验，不传发现分数。发现/held-out ID必须不相交，任务簇只允许发现集ID，部署只接受预声明held-out任务。Actor和路由入口只接受exact PublicTask并按白名单重建对象，拒绝附带gold字段的子类；工具观察也拒绝子类并重建，不能借嵌套对象携带隐藏grader元数据。  自我进化 Harness搜索与继承 Agent 运行流程与自进化：改的是哪一层 OO-Harness 为什么用可继承的 harness 类组织面向不同任务的专门化？ 单一通用流程未必适合所有任务，但为每类任务完全复制代码又难共享已验证逻辑。OO-Harness 用类和继承表达可复用部分与专门改动，再按任务选择适合的版本。继承关系是代码组织，不代表运行更多 Agent，也不保证专用版本在所有任务上优于基类。 教学例：浏览任务子类沿用基础恢复逻辑，只改搜索步骤；选择该子类后执行的是一套流程，并非父类与子类各跑一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-oo-harness-cd6587e9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-001a95d0b85c9840">OO-Harness 为什么用可继承的 harness 类组织面向不同任务的专门化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aoo-harness">Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单一通用流程未必适合所有任务，但为每类任务完全复制代码又难共享已验证逻辑。OO-Harness 用类和继承表达可复用部分与专门改动，再按任务选择适合的版本。继承关系是代码组织，不代表运行更多 Agent，也不保证专用版本在所有任务上优于基类。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：浏览任务子类沿用基础恢复逻辑，只改搜索步骤；选择该子类后执行的是一套流程，并非父类与子类各跑一次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28380">原论文</a> · <a href="../../../../agent-research/2610.28380-oo-harness/">实现解读</a> · <a href="#qa-001a95d0b85c9840">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:oo-harness" data-paper-title="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design Agent University of Illinois Urbana-Champaign 2026-10-20 全任务共用一个harness可能互相干扰；为每类任务复制完整实现又难以复用。作者将专用harness写成父类的子类，只覆盖需要改变的prompt、工具或执行hook。发现阶段围绕任务簇改进，部署阶段冻结代码和经验，再用任务及可观察base轨迹选择完整类；父类方法在一个实例里执行，不是额外运行多个祖先Agent。§3 成本过高，不复现（审查 DONE），不下载模型、不试跑完整实验、不自动重试。HarnessDiscovery只接受可信的Python类，不从字符串exec候选。它保存发现阶段的接受和拒绝记录；freeze只复制当前可路由类描述、必要祖先类和路由经验，不传发现分数。发现/held-out ID必须不相交，任务簇只允许发现集ID，部署只接受预声明held-out任务。Actor和路由入口只接受exact PublicTask并按白名单重建对象，拒绝附带gold字段的子类；工具观察也拒绝子类并重建，不能借嵌套对象携带隐藏grader元数据。  自我进化 Harness搜索与继承 Agent 运行流程与自进化：改的是哪一层 子类复用父 harness 方法，为什么不等于同时执行多个祖先 Agent？ 继承是代码复用：一个实例调用未覆盖的父方法，不会自动启动祖先的独立轨迹。专用子类只改必要 hook，部署时从冻结候选选完整类；目标簇得分提升也不保证所有任务改善，自报置信度消融更不能被误作校准成功概率。 例如子类只覆盖搜索 prompt，终端执行仍调用父实现；这是一名 Agent 的一套方法，不应把它计成两名 Agent 并行协作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:oo-harness" data-paper-title="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design Agent University of Illinois Urbana-Champaign 2026-10-20 全任务共用一个harness可能互相干扰；为每类任务复制完整实现又难以复用。作者将专用harness写成父类的子类，只覆盖需要改变的prompt、工具或执行hook。发现阶段围绕任务簇改进，部署阶段冻结代码和经验，再用任务及可观察base轨迹选择完整类；父类方法在一个实例里执行，不是额外运行多个祖先Agent。§3 成本过高，不复现（审查 DONE），不下载模型、不试跑完整实验、不自动重试。HarnessDiscovery只接受可信的Python类，不从字符串exec候选。它保存发现阶段的接受和拒绝记录；freeze只复制当前可路由类描述、必要祖先类和路由经验，不传发现分数。发现/held-out ID必须不相交，任务簇只允许发现集ID，部署只接受预声明held-out任务。Actor和路由入口只接受exact PublicTask并按白名单重建对象，拒绝附带gold字段的子类；工具观察也拒绝子类并重建，不能借嵌套对象携带隐藏grader元数据。  自我进化 Harness搜索与继承 Agent 运行流程与自进化：改的是哪一层 按任务簇严格接纳与全任务只看平均分有什么取舍？ 目标簇需严格高于当前专用类且额外检查通过，避免全局平均掩盖相关簇退化；但不保证所有任务都改善。路由部署只看公共任务与可观察 base 轨迹，不能读取测试 grader 分数选类，自报 0.7 也不是校准成功概率。 例如修改只帮助表格任务，应在该簇验证，不能靠另一个容易簇的分数上涨掩盖它没有提升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-67c269161e84e1cc">按任务簇严格接纳与全任务只看平均分有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aoo-harness">Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标簇需严格高于当前专用类且额外检查通过，避免全局平均掩盖相关簇退化；但不保证所有任务都改善。路由部署只看公共任务与可观察 base 轨迹，不能读取测试 grader 分数选类，自报 0.7 也不是校准成功概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如修改只帮助表格任务，应在该簇验证，不能靠另一个容易簇的分数上涨掩盖它没有提升。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28380">原论文</a> · <a href="../../../../agent-research/2610.28380-oo-harness/">实现解读</a> · <a href="#qa-67c269161e84e1cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:oo-harness" data-paper-title="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design Agent University of Illinois Urbana-Champaign 2026-10-20 全任务共用一个harness可能互相干扰；为每类任务复制完整实现又难以复用。作者将专用harness写成父类的子类，只覆盖需要改变的prompt、工具或执行hook。发现阶段围绕任务簇改进，部署阶段冻结代码和经验，再用任务及可观察base轨迹选择完整类；父类方法在一个实例里执行，不是额外运行多个祖先Agent。§3 成本过高，不复现（审查 DONE），不下载模型、不试跑完整实验、不自动重试。HarnessDiscovery只接受可信的Python类，不从字符串exec候选。它保存发现阶段的接受和拒绝记录；freeze只复制当前可路由类描述、必要祖先类和路由经验，不传发现分数。发现/held-out ID必须不相交，任务簇只允许发现集ID，部署只接受预声明held-out任务。Actor和路由入口只接受exact PublicTask并按白名单重建对象，拒绝附带gold字段的子类；工具观察也拒绝子类并重建，不能借嵌套对象携带隐藏grader元数据。  自我进化 Harness搜索与继承 Agent 运行流程与自进化：改的是哪一层 选专用类时为何必须重建同初始环境，而选 Base 可复用结果？ 路由前 Base 已执行，若最终仍选 Base 可直接用；选专用类需 tool_factory 重置，避免继承 Base 已造成的进展。真实外部副作用不保证可回滚，本地可信 Python 类与白名单数据隔离也不是安全沙箱，脚本 actor 不代表 LLM 能力。 例如 Base 已创建一半文件后再让专用类接着做，会让后者看似更成功；公平比较应从相同初始文件状态开始。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c54046ce9413a3c7">选专用类时为何必须重建同初始环境，而选 Base 可复用结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aoo-harness">Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路由前 Base 已执行，若最终仍选 Base 可直接用；选专用类需 tool_factory 重置，避免继承 Base 已造成的进展。真实外部副作用不保证可回滚，本地可信 Python 类与白名单数据隔离也不是安全沙箱，脚本 actor 不代表 LLM 能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 Base 已创建一半文件后再让专用类接着做，会让后者看似更成功；公平比较应从相同初始文件状态开始。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28380">原论文</a> · <a href="../../../../agent-research/2610.28380-oo-harness/">实现解读</a> · <a href="#qa-c54046ce9413a3c7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aptamer-lab-loop" data-paper-title="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery Agent Google Research 2026-10-17 该研究把计算设计与真实实验测量放进多轮反馈闭环，让Agent利用成功和失败证据调整下一轮策略。关键不是把Agent多跑几轮，而是实物测量可以否定计算评分；论文显示一些预测代理与实际测量不一致。这里仅讨论研究编排与证据边界，不提供生物实验操作流程。 完整实验成本过高，不复现（审查 DONE）。Google优先资料收录；完整实验成本过高，不复现（审查 DONE）。没有低成本代理被标成实现，不进入自动训练队列。完整研究需要专业实验室、物理测量与多轮7–10天反馈周期，无法在单A100/A30或本地Mac低成本完成。依据Results R.1/Figure1直接标记成本过高，不复现（审查 DONE），未启动模型下载、实验运行或无意义代理测试。  科学研究与实验闭环 物理实验反馈 Agent 运行流程与自进化：改的是哪一层 适配体设计为什么需要反复连接计算提案与真实实验反馈？ 计算模型只能按已有数据估计候选性质，实际分子表现仍可能受未建模因素影响。该工作研究用真实测量检验提案并支持下一轮设计，使实验而非预测分数成为关键反馈。不同轮候选和筛选条件会变化，不能将闭环进展自动解读为固定测试集能力提升。 教学例：模型偏好的候选在实际测量中表现一般，下一轮应利用这个反例；重新调高预测分数并不会改变真实测量结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-aptamer-lab-loop-d80e05ef" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f037abf7dbe5b196">适配体设计为什么需要反复连接计算提案与真实实验反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaptamer-lab-loop">Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>计算模型只能按已有数据估计候选性质，实际分子表现仍可能受未建模因素影响。该工作研究用真实测量检验提案并支持下一轮设计，使实验而非预测分数成为关键反馈。不同轮候选和筛选条件会变化，不能将闭环进展自动解读为固定测试集能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：模型偏好的候选在实际测量中表现一般，下一轮应利用这个反例；重新调高预测分数并不会改变真实测量结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24806v1">原论文</a> · <a href="../../../../agent-research/2610.24806-aptamer-lab-loop/">实现解读</a> · <a href="#qa-f037abf7dbe5b196">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aptamer-lab-loop" data-paper-title="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery Agent Google Research 2026-10-17 该研究把计算设计与真实实验测量放进多轮反馈闭环，让Agent利用成功和失败证据调整下一轮策略。关键不是把Agent多跑几轮，而是实物测量可以否定计算评分；论文显示一些预测代理与实际测量不一致。这里仅讨论研究编排与证据边界，不提供生物实验操作流程。 完整实验成本过高，不复现（审查 DONE）。Google优先资料收录；完整实验成本过高，不复现（审查 DONE）。没有低成本代理被标成实现，不进入自动训练队列。完整研究需要专业实验室、物理测量与多轮7–10天反馈周期，无法在单A100/A30或本地Mac低成本完成。依据Results R.1/Figure1直接标记成本过高，不复现（审查 DONE），未启动模型下载、实验运行或无意义代理测试。  科学研究与实验闭环 物理实验反馈 Agent 运行流程与自进化：改的是哪一层 真实实验反馈为什么不能由计算代理高分替代，也不能跨轮直接算成固定测试提升？ 计算评分可能与现实测量不一致，闭环的价值就在于新测量能够否定预测并保留失败证据。不同轮次改变候选和策略，命中比例还受所选分布影响，不是同一测试集上的可比机器学习分数；这里评价研究编排，不据此推出具体实验操作建议。 例如一轮专挑代理认为最优的候选、下一轮转向探索，二者命中比例差异可能来自选择范围，不能直接称模型泛化提高。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aptamer-lab-loop" data-paper-title="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery Agent Google Research 2026-10-17 该研究把计算设计与真实实验测量放进多轮反馈闭环，让Agent利用成功和失败证据调整下一轮策略。关键不是把Agent多跑几轮，而是实物测量可以否定计算评分；论文显示一些预测代理与实际测量不一致。这里仅讨论研究编排与证据边界，不提供生物实验操作流程。 完整实验成本过高，不复现（审查 DONE）。Google优先资料收录；完整实验成本过高，不复现（审查 DONE）。没有低成本代理被标成实现，不进入自动训练队列。完整研究需要专业实验室、物理测量与多轮7–10天反馈周期，无法在单A100/A30或本地Mac低成本完成。依据Results R.1/Figure1直接标记成本过高，不复现（审查 DONE），未启动模型下载、实验运行或无意义代理测试。  科学研究与实验闭环 物理实验反馈 Agent 运行流程与自进化：改的是哪一层 新增真实测量与反复重新评价已有实验记录，分别增加什么信息？ 重新评价已有记录可改进解释或候选选择，却没有产生新的物理观察；新增测量能检验尚未验证的候选，可能揭示模型遗漏。二者都可参与研究，但不能把再计算说成独立实验，也不能用模拟代理替代实验终点。跨轮比较还需保留候选和测量条件变化。 教学例：对十个旧结果重新排序，仍只有十次已发生测量；真正测试第十一个候选，才增加一个新的外部反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c4f29aea97ea8cba">新增真实测量与反复重新评价已有实验记录，分别增加什么信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaptamer-lab-loop">Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重新评价已有记录可改进解释或候选选择，却没有产生新的物理观察；新增测量能检验尚未验证的候选，可能揭示模型遗漏。二者都可参与研究，但不能把再计算说成独立实验，也不能用模拟代理替代实验终点。跨轮比较还需保留候选和测量条件变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：对十个旧结果重新排序，仍只有十次已发生测量；真正测试第十一个候选，才增加一个新的外部反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24806v1">原论文</a> · <a href="../../../../agent-research/2610.24806-aptamer-lab-loop/">实现解读</a> · <a href="#qa-c4f29aea97ea8cba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aptamer-lab-loop" data-paper-title="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery Agent Google Research 2026-10-17 该研究把计算设计与真实实验测量放进多轮反馈闭环，让Agent利用成功和失败证据调整下一轮策略。关键不是把Agent多跑几轮，而是实物测量可以否定计算评分；论文显示一些预测代理与实际测量不一致。这里仅讨论研究编排与证据边界，不提供生物实验操作流程。 完整实验成本过高，不复现（审查 DONE）。Google优先资料收录；完整实验成本过高，不复现（审查 DONE）。没有低成本代理被标成实现，不进入自动训练队列。完整研究需要专业实验室、物理测量与多轮7–10天反馈周期，无法在单A100/A30或本地Mac低成本完成。依据Results R.1/Figure1直接标记成本过高，不复现（审查 DONE），未启动模型下载、实验运行或无意义代理测试。  科学研究与实验闭环 物理实验反馈 Agent 运行流程与自进化：改的是哪一层 本地为何不以模拟测量或预测分数替代物理终点？ 真实实验是否定计算代理的定义性环节，替换后会消除论文核心难点。本地只收录研究编排与成本，没有模型、GPU receipt、能力指标或 Evolve 集成；专业实验室与多天反馈不由一个数值 fixture 代表，也不提供实验操作流程。 例如随机生成一个“测量通过”标签可测消息接口，却不能证明候选在真实物理实验有效，更不能算完成实验闭环。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-05aefca653b2f5bd">本地为何不以模拟测量或预测分数替代物理终点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaptamer-lab-loop">Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实实验是否定计算代理的定义性环节，替换后会消除论文核心难点。本地只收录研究编排与成本，没有模型、GPU receipt、能力指标或 Evolve 集成；专业实验室与多天反馈不由一个数值 fixture 代表，也不提供实验操作流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如随机生成一个“测量通过”标签可测消息接口，却不能证明候选在真实物理实验有效，更不能算完成实验闭环。</p>
<p class="ar-learning-sources">依据：核心机制与评测、本地复现与成本决策；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24806v1">原论文</a> · <a href="../../../../agent-research/2610.24806-aptamer-lab-loop/">实现解读</a> · <a href="#qa-05aefca653b2f5bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:athanor" data-paper-title="Athanor: An Agent-Native System for Autonomous Post-Training Research" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Athanor: An Agent-Native System for Autonomous Post-Training Research Agent ByteDance / Duke University 2026-10-15 研究 Agent 选择数据、训练算法和阶段组合；独立服务执行异步任务、去污染、冻结评测并保存 checkpoint 谱系。团队共享实验记录与模型，组合 SFT、RL、模型合并及自蒸馏；外部教师调用被禁止。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。不运行完整研究 campaign，不将现有 Evolve 改名冒充 Athanor。无研究自动化实现、benchmark分数或 GPU回执；不把资料链接宣称为 Evolve 集成。范围见本批验收合同。只做论文解读和原图收录。原配置为四个商业研究 Agent 各占八卡节点，合计约12000美元；超过本轮单 A100/A30资源，不启动探跑。成本过高，不复现（审查 DONE）。  递归自改进 自主研究 多 Agent 协作 Agent 运行流程与自进化：改的是哪一层 研究 Agent 与异步训练评测服务分开有什么作用？ Agent 选择数据、算法和阶段，服务执行训练、去污染、冻结评测并保存 checkpoint 谱系，让提案与真实产物相连。分开也有助限制最终 held-out 可见性；服务返回的开发分仍有噪声，不是研究 Agent 每次猜测的真实性能。 例如 Agent 提议自蒸馏后，必须等服务完成并记录新 checkpoint 与评测，不能用提案文字中的“预计更好”替代结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-athanor-3414bb2a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7110f2236cddb02d">研究 Agent 与异步训练评测服务分开有什么作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aathanor">Athanor: An Agent-Native System for Autonomous Post-Training Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Agent 选择数据、算法和阶段，服务执行训练、去污染、冻结评测并保存 checkpoint 谱系，让提案与真实产物相连。分开也有助限制最终 held-out 可见性；服务返回的开发分仍有噪声，不是研究 Agent 每次猜测的真实性能。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 Agent 提议自蒸馏后，必须等服务完成并记录新 checkpoint 与评测，不能用提案文字中的“预计更好”替代结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21055">原论文</a> · <a href="../../../../agent-research/2610.21055-athanor/">实现解读</a> · <a href="#qa-7110f2236cddb02d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:athanor" data-paper-title="Athanor: An Agent-Native System for Autonomous Post-Training Research" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Athanor: An Agent-Native System for Autonomous Post-Training Research Agent ByteDance / Duke University 2026-10-15 研究 Agent 选择数据、训练算法和阶段组合；独立服务执行异步任务、去污染、冻结评测并保存 checkpoint 谱系。团队共享实验记录与模型，组合 SFT、RL、模型合并及自蒸馏；外部教师调用被禁止。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。不运行完整研究 campaign，不将现有 Evolve 改名冒充 Athanor。无研究自动化实现、benchmark分数或 GPU回执；不把资料链接宣称为 Evolve 集成。范围见本批验收合同。只做论文解读和原图收录。原配置为四个商业研究 Agent 各占八卡节点，合计约12000美元；超过本轮单 A100/A30资源，不启动探跑。成本过高，不复现（审查 DONE）。  递归自改进 自主研究 多 Agent 协作 Agent 运行流程与自进化：改的是哪一层 独立训练服务为什么还需要冻结评测与 checkpoint 谱系？ 异步实验会产生多个数据、算法和阶段组合，仅看文件名无法确定结果来自哪条训练链。谱系保存可追溯父子关系，冻结评测减少标准随搜索漂移，最终 held-out 则隔离研究者选择；一次开发最高分可能只是噪声，不能立刻称为稳健能力提升。 例如某模型经过 SFT、合并再自蒸馏，若不记录父 checkpoint，就难解释哪次改动导致分数变化或复现同一候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:athanor" data-paper-title="Athanor: An Agent-Native System for Autonomous Post-Training Research" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Athanor: An Agent-Native System for Autonomous Post-Training Research Agent ByteDance / Duke University 2026-10-15 研究 Agent 选择数据、训练算法和阶段组合；独立服务执行异步任务、去污染、冻结评测并保存 checkpoint 谱系。团队共享实验记录与模型，组合 SFT、RL、模型合并及自蒸馏；外部教师调用被禁止。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。不运行完整研究 campaign，不将现有 Evolve 改名冒充 Athanor。无研究自动化实现、benchmark分数或 GPU回执；不把资料链接宣称为 Evolve 集成。范围见本批验收合同。只做论文解读和原图收录。原配置为四个商业研究 Agent 各占八卡节点，合计约12000美元；超过本轮单 A100/A30资源，不启动探跑。成本过高，不复现（审查 DONE）。  递归自改进 自主研究 多 Agent 协作 Agent 运行流程与自进化：改的是哪一层 禁止外部教师时，自蒸馏与调用更强商业教师有什么区别？ 自蒸馏使用系统内允许的模型和已有数据，外部教师会引入额外能力、费用与数据来源，违反本研究合同。不能因为研究 Agent 本身由商业模型驱动，就把它的答案偷偷当训练标签；研究控制与受训模型监督来源需要分开。 例如商业 Agent 可规划下一轮训练，但若直接把其高质量解答加入数据，就不再是规定的无外部教师设置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2f6eb0573de3da89">禁止外部教师时，自蒸馏与调用更强商业教师有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aathanor">Athanor: An Agent-Native System for Autonomous Post-Training Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自蒸馏使用系统内允许的模型和已有数据，外部教师会引入额外能力、费用与数据来源，违反本研究合同。不能因为研究 Agent 本身由商业模型驱动，就把它的答案偷偷当训练标签；研究控制与受训模型监督来源需要分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如商业 Agent 可规划下一轮训练，但若直接把其高质量解答加入数据，就不再是规定的无外部教师设置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21055">原论文</a> · <a href="../../../../agent-research/2610.21055-athanor/">实现解读</a> · <a href="#qa-2f6eb0573de3da89">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:athanor" data-paper-title="Athanor: An Agent-Native System for Autonomous Post-Training Research" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Athanor: An Agent-Native System for Autonomous Post-Training Research Agent ByteDance / Duke University 2026-10-15 研究 Agent 选择数据、训练算法和阶段组合；独立服务执行异步任务、去污染、冻结评测并保存 checkpoint 谱系。团队共享实验记录与模型，组合 SFT、RL、模型合并及自蒸馏；外部教师调用被禁止。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。不运行完整研究 campaign，不将现有 Evolve 改名冒充 Athanor。无研究自动化实现、benchmark分数或 GPU回执；不把资料链接宣称为 Evolve 集成。范围见本批验收合同。只做论文解读和原图收录。原配置为四个商业研究 Agent 各占八卡节点，合计约12000美元；超过本轮单 A100/A30资源，不启动探跑。成本过高，不复现（审查 DONE）。  递归自改进 自主研究 多 Agent 协作 Agent 运行流程与自进化：改的是哪一层 为何搜索中最高开发分不能作为最终正式结果？ 多次提案在噪声开发集上选最大值会产生选择偏差，正式比较需区分 campaign、提交多 seed 均值和统一解码重测，最终 held-out 不向研究者暴露。本地仅资料与成本审查，无研究自动化、模型运行或 GPU receipt。 例如一百次评测中偶然一次最高，不代表该 checkpoint 的期望能力；需冻结选择后在独立协议重新评价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d66143f49b76710f">为何搜索中最高开发分不能作为最终正式结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aathanor">Athanor: An Agent-Native System for Autonomous Post-Training Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多次提案在噪声开发集上选最大值会产生选择偏差，正式比较需区分 campaign、提交多 seed 均值和统一解码重测，最终 held-out 不向研究者暴露。本地仅资料与成本审查，无研究自动化、模型运行或 GPU receipt。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一百次评测中偶然一次最高，不代表该 checkpoint 的期望能力；需冻结选择后在独立协议重新评价。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21055">原论文</a> · <a href="../../../../agent-research/2610.21055-athanor/">实现解读</a> · <a href="#qa-d66143f49b76710f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auto-sft" data-paper-title="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning Agent Tsinghua University 2026-10-15 自动后训练研究若让一个 Agent 同时读训练日志、分析失败、改数据、提交任务，可能在上下文中积累大量执行输出，最终只反复调整混合比例。AutoSFT 将 Meta Agent、执行子代理、四种分析视角与数据合成分开：执行侧只返回可追溯产物，分析侧从数据、失败、训练信号、研究历史提出不同方案，Meta Agent 决定下一轮的数据干预。原文 §2–4 干预不局限于筛行或生成：可以调类别比例、删除、修复、替换回答、定向合成和调整顺序。这六类是作者对实际动作的事后归类，不是给分析Agent预设的固定菜单。 完整实验成本过高，不复现（审查 DONE）；高成本资料收录。完整实验成本过高，不复现（审查 DONE）；没有本地模型实现、控制器fixture、假 Adapter 或 evolve 接入。原文配置 Qwen3-1.7B-Base、Megatron-LM、8×H800。一次20轮运行约 130 GPU小时；Agent与数据合成约 95美元/轮、1900美元/次。执行子代理、独立语义审查和每轮从基座训练都是定义机制的重要部分，不能删成几条规则后称为AutoSFT复现。原文 Appendix D  递归自改进 自动后训练与数据研究 Agent 运行流程与自进化：改的是哪一层 AutoSFT 为什么把训练数据的选择与组织作为自动研究对象？ 同一基座采用不同数据内容、质量与组合，可能学出不同能力，人工反复试配方成本很高。AutoSFT 让研究过程提出并检验数据假设，而不只调整一次训练参数。为了理解数据改动的作用，需要控制训练条件并隔离评测，不能从开发分持续上涨推导最终泛化。 教学例：怀疑某类格式错误来自示例不足，可增加对应数据再从相同基座比较；沿用上一轮权重会混入额外训练历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-auto-sft-e69c4a3b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4d12282618b9c1d0">AutoSFT 为什么把训练数据的选择与组织作为自动研究对象？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aauto-sft">AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一基座采用不同数据内容、质量与组合，可能学出不同能力，人工反复试配方成本很高。AutoSFT 让研究过程提出并检验数据假设，而不只调整一次训练参数。为了理解数据改动的作用，需要控制训练条件并隔离评测，不能从开发分持续上涨推导最终泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：怀疑某类格式错误来自示例不足，可增加对应数据再从相同基座比较；沿用上一轮权重会混入额外训练历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式：固定训练合同的形式化；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22194">原论文</a> · <a href="../../../../agent-research/2610.22194-auto-sft/">实现解读</a> · <a href="#qa-4d12282618b9c1d0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auto-sft" data-paper-title="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning Agent Tsinghua University 2026-10-15 自动后训练研究若让一个 Agent 同时读训练日志、分析失败、改数据、提交任务，可能在上下文中积累大量执行输出，最终只反复调整混合比例。AutoSFT 将 Meta Agent、执行子代理、四种分析视角与数据合成分开：执行侧只返回可追溯产物，分析侧从数据、失败、训练信号、研究历史提出不同方案，Meta Agent 决定下一轮的数据干预。原文 §2–4 干预不局限于筛行或生成：可以调类别比例、删除、修复、替换回答、定向合成和调整顺序。这六类是作者对实际动作的事后归类，不是给分析Agent预设的固定菜单。 完整实验成本过高，不复现（审查 DONE）；高成本资料收录。完整实验成本过高，不复现（审查 DONE）；没有本地模型实现、控制器fixture、假 Adapter 或 evolve 接入。原文配置 Qwen3-1.7B-Base、Megatron-LM、8×H800。一次20轮运行约 130 GPU小时；Agent与数据合成约 95美元/轮、1900美元/次。执行子代理、独立语义审查和每轮从基座训练都是定义机制的重要部分，不能删成几条规则后称为AutoSFT复现。原文 Appendix D  递归自改进 自动后训练与数据研究 Agent 运行流程与自进化：改的是哪一层 每轮都从同一基座重新训练，为什么对数据研究归因很重要？ 这样跨轮变化主要来自数据池、配比与顺序，而非上一轮权重继续学习产生的累积效应。固定训练器和预算后登记干预假设，才能比较预期机制是否出现；不同分析视角提出方案不等于已经执行实验，也不能事后按分数改写原始预测。 例如第二轮修复了错误回答数据，应从同一基座重训；若续训第一轮模型，提升还混入更多训练步数的影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auto-sft" data-paper-title="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning Agent Tsinghua University 2026-10-15 自动后训练研究若让一个 Agent 同时读训练日志、分析失败、改数据、提交任务，可能在上下文中积累大量执行输出，最终只反复调整混合比例。AutoSFT 将 Meta Agent、执行子代理、四种分析视角与数据合成分开：执行侧只返回可追溯产物，分析侧从数据、失败、训练信号、研究历史提出不同方案，Meta Agent 决定下一轮的数据干预。原文 §2–4 干预不局限于筛行或生成：可以调类别比例、删除、修复、替换回答、定向合成和调整顺序。这六类是作者对实际动作的事后归类，不是给分析Agent预设的固定菜单。 完整实验成本过高，不复现（审查 DONE）；高成本资料收录。完整实验成本过高，不复现（审查 DONE）；没有本地模型实现、控制器fixture、假 Adapter 或 evolve 接入。原文配置 Qwen3-1.7B-Base、Megatron-LM、8×H800。一次20轮运行约 130 GPU小时；Agent与数据合成约 95美元/轮、1900美元/次。执行子代理、独立语义审查和每轮从基座训练都是定义机制的重要部分，不能删成几条规则后称为AutoSFT复现。原文 Appendix D  递归自改进 自动后训练与数据研究 Agent 运行流程与自进化：改的是哪一层 四分析视角与单 Agent 只调数据比例有什么不同？ 数据、失败、训练信号和历史研究提供不同证据，执行子代理回传可追溯工件，Meta Agent 决定干预，不必局限于混合比例。作者六类动作是事后归类而非固定菜单，不能把一个规则选项表冒充开放数据研究。 例如失败分析建议修答案、训练信号提示顺序问题，两种提案需按证据比较，而不是每轮只把某类别占比增加百分之五。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d4811813cf908dd5">四分析视角与单 Agent 只调数据比例有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aauto-sft">AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>数据、失败、训练信号和历史研究提供不同证据，执行子代理回传可追溯工件，Meta Agent 决定干预，不必局限于混合比例。作者六类动作是事后归类而非固定菜单，不能把一个规则选项表冒充开放数据研究。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如失败分析建议修答案、训练信号提示顺序问题，两种提案需按证据比较，而不是每轮只把某类别占比增加百分之五。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式：固定训练合同的形式化；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22194">原论文</a> · <a href="../../../../agent-research/2610.22194-auto-sft/">实现解读</a> · <a href="#qa-d4811813cf908dd5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:auto-sft" data-paper-title="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning Agent Tsinghua University 2026-10-15 自动后训练研究若让一个 Agent 同时读训练日志、分析失败、改数据、提交任务，可能在上下文中积累大量执行输出，最终只反复调整混合比例。AutoSFT 将 Meta Agent、执行子代理、四种分析视角与数据合成分开：执行侧只返回可追溯产物，分析侧从数据、失败、训练信号、研究历史提出不同方案，Meta Agent 决定下一轮的数据干预。原文 §2–4 干预不局限于筛行或生成：可以调类别比例、删除、修复、替换回答、定向合成和调整顺序。这六类是作者对实际动作的事后归类，不是给分析Agent预设的固定菜单。 完整实验成本过高，不复现（审查 DONE）；高成本资料收录。完整实验成本过高，不复现（审查 DONE）；没有本地模型实现、控制器fixture、假 Adapter 或 evolve 接入。原文配置 Qwen3-1.7B-Base、Megatron-LM、8×H800。一次20轮运行约 130 GPU小时；Agent与数据合成约 95美元/轮、1900美元/次。执行子代理、独立语义审查和每轮从基座训练都是定义机制的重要部分，不能删成几条规则后称为AutoSFT复现。原文 Appendix D  递归自改进 自动后训练与数据研究 Agent 运行流程与自进化：改的是哪一层 为什么训练前登记假设，去污染后仍需独立外部 holdout？ 预先记录改什么、对照、方向和证据防事后改写预测；多轮使用同一评测失败与最优选择仍可能适配评测，即使 n-gram 未直接复制。独立冻结 holdout 才能另检泛化，本地未运行八 H800 和付费研究 campaign，不提供伪训练指标。 例如分数涨了但预期机制证据未出现，应承认假设未证实；不能回头把原本预计的方向改成实际结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a3c27f91439eca03">为什么训练前登记假设，去污染后仍需独立外部 holdout？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aauto-sft">AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预先记录改什么、对照、方向和证据防事后改写预测；多轮使用同一评测失败与最优选择仍可能适配评测，即使 n-gram 未直接复制。独立冻结 holdout 才能另检泛化，本地未运行八 H800 和付费研究 campaign，不提供伪训练指标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如分数涨了但预期机制证据未出现，应承认假设未证实；不能回头把原本预计的方向改成实际结果。</p>
<p class="ar-learning-sources">依据：核心公式：固定训练合同的形式化、成本决策与本地状态；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22194">原论文</a> · <a href="../../../../agent-research/2610.22194-auto-sft/">实现解读</a> · <a href="#qa-a3c27f91439eca03">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsiflow" data-paper-title="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent Agent Beihang University 2026-10-15 性能瓶颈可能来自模型参数、执行 Harness，也可能只是当前交付物。固定只改其中一项，或固定交替更新，未必对应当前失败。RSIFlow 的 Meta-Agent 用任务执行证据选择 Model / Harness / Artifacts 干预，比较同父代、同任务批的候选，并从成功和失败中维护技能。Meta 模型参数保持固定；本地遵循已发布的技能记忆变体，不把它扩写成任意自改代码系统。 原文五轮、每轮最多两个候选、4B/8B、SFT/GRPO、16K/32K 与 8 ranks，加上 Meta API 和真实工具执行，完整多臂评测对单 A100/A30 或 Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。实现固定 callback 控制器与技能经验记录，不训练语言模型，不执行任意元程序自改，不进入统一 Evolve 晋级。每 seed 初始化三批、每批四个数值 fixture 和五个独立报告任务；私有目标值仅由 evaluator 闭包持有。M/H/A proposer 只拿公共任务、父代标量分数及已有训练技能。  RSI 自我改进与工作流 Agent 运行流程与自进化：改的是哪一层 自动研究失败时，RSIFlow 为什么先判断瓶颈来自哪一类对象？ 效果不足可能来自模型本身、执行流程，也可能只是当前产物存在缺陷，固定只改提示或一律重训会错配资源。RSIFlow 用执行证据选择干预对象，让改进与失败原因相联系。诊断和候选都需要实际验证，不能把选择了某个分支当成该类瓶颈已被解决。 教学例：结果文件格式错可修产物，工具流程总是漏验证可改 harness；二者并不都需要重新训练模型权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-rsiflow-bf0996bb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e83fc8ef79fc5a35">自动研究失败时，RSIFlow 为什么先判断瓶颈来自哪一类对象？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsiflow">RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>效果不足可能来自模型本身、执行流程，也可能只是当前产物存在缺陷，固定只改提示或一律重训会错配资源。RSIFlow 用执行证据选择干预对象，让改进与失败原因相联系。诊断和候选都需要实际验证，不能把选择了某个分支当成该类瓶颈已被解决。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：结果文件格式错可修产物，工具流程总是漏验证可改 harness；二者并不都需要重新训练模型权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21791">原论文</a> · <a href="../../../../agent-research/2610.21791-rsiflow/">实现解读</a> · <a href="#qa-e83fc8ef79fc5a35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsiflow" data-paper-title="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent Agent Beihang University 2026-10-15 性能瓶颈可能来自模型参数、执行 Harness，也可能只是当前交付物。固定只改其中一项，或固定交替更新，未必对应当前失败。RSIFlow 的 Meta-Agent 用任务执行证据选择 Model / Harness / Artifacts 干预，比较同父代、同任务批的候选，并从成功和失败中维护技能。Meta 模型参数保持固定；本地遵循已发布的技能记忆变体，不把它扩写成任意自改代码系统。 原文五轮、每轮最多两个候选、4B/8B、SFT/GRPO、16K/32K 与 8 ranks，加上 Meta API 和真实工具执行，完整多臂评测对单 A100/A30 或 Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。实现固定 callback 控制器与技能经验记录，不训练语言模型，不执行任意元程序自改，不进入统一 Evolve 晋级。每 seed 初始化三批、每批四个数值 fixture 和五个独立报告任务；私有目标值仅由 evaluator 闭包持有。M/H/A proposer 只拿公共任务、父代标量分数及已有训练技能。  RSI 自我改进与工作流 Agent 运行流程与自进化：改的是哪一层 比较候选时为什么必须都从同一个冻结父代出发？ 若第一个候选的修改混入第二个，无法把收益归因到所选 Model、Harness 或 Artifacts 干预。统一父代和任务批提供配对基线，仅有效且严格提升者接受，失败后仍从原父代再试；技能可来自训练经验，报告集分数不能反向泄漏给维护过程。 例如先改 prompt 后又换模型，应分别对同一父配置评估，不能把第二次累计收益全算给模型替换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsiflow" data-paper-title="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent Agent Beihang University 2026-10-15 性能瓶颈可能来自模型参数、执行 Harness，也可能只是当前交付物。固定只改其中一项，或固定交替更新，未必对应当前失败。RSIFlow 的 Meta-Agent 用任务执行证据选择 Model / Harness / Artifacts 干预，比较同父代、同任务批的候选，并从成功和失败中维护技能。Meta 模型参数保持固定；本地遵循已发布的技能记忆变体，不把它扩写成任意自改代码系统。 原文五轮、每轮最多两个候选、4B/8B、SFT/GRPO、16K/32K 与 8 ranks，加上 Meta API 和真实工具执行，完整多臂评测对单 A100/A30 或 Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。实现固定 callback 控制器与技能经验记录，不训练语言模型，不执行任意元程序自改，不进入统一 Evolve 晋级。每 seed 初始化三批、每批四个数值 fixture 和五个独立报告任务；私有目标值仅由 evaluator 闭包持有。M/H/A proposer 只拿公共任务、父代标量分数及已有训练技能。  RSI 自我改进与工作流 Agent 运行流程与自进化：改的是哪一层 Model、Harness 与 Artifacts 干预，各改变后续执行的哪一层？ Model 干预针对模型，Harness 改变执行组织，Artifacts 作用于交付物；它们的作用域和可继承状态不同。比较时要明确候选到底改了什么，不能把一次文件修正宣传为策略普遍学会，也不能让越界改动混入既定分支。当前本地是可信 callback 与技能记忆变体。 教学例：修一份输出报告只改变该产物；修改每次都执行的检查流程，才可能影响下一任务，但仍须验证其迁移效果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3635aa173e7ccab2">Model、Harness 与 Artifacts 干预，各改变后续执行的哪一层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsiflow">RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Model 干预针对模型，Harness 改变执行组织，Artifacts 作用于交付物；它们的作用域和可继承状态不同。比较时要明确候选到底改了什么，不能把一次文件修正宣传为策略普遍学会，也不能让越界改动混入既定分支。当前本地是可信 callback 与技能记忆变体。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：修一份输出报告只改变该产物；修改每次都执行的检查流程，才可能影响下一任务，但仍须验证其迁移效果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21791">原论文</a> · <a href="../../../../agent-research/2610.21791-rsiflow/">实现解读</a> · <a href="#qa-3635aa173e7ccab2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsiflow" data-paper-title="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent Agent Beihang University 2026-10-15 性能瓶颈可能来自模型参数、执行 Harness，也可能只是当前交付物。固定只改其中一项，或固定交替更新，未必对应当前失败。RSIFlow 的 Meta-Agent 用任务执行证据选择 Model / Harness / Artifacts 干预，比较同父代、同任务批的候选，并从成功和失败中维护技能。Meta 模型参数保持固定；本地遵循已发布的技能记忆变体，不把它扩写成任意自改代码系统。 原文五轮、每轮最多两个候选、4B/8B、SFT/GRPO、16K/32K 与 8 ranks，加上 Meta API 和真实工具执行，完整多臂评测对单 A100/A30 或 Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。实现固定 callback 控制器与技能经验记录，不训练语言模型，不执行任意元程序自改，不进入统一 Evolve 晋级。每 seed 初始化三批、每批四个数值 fixture 和五个独立报告任务；私有目标值仅由 evaluator 闭包持有。M/H/A proposer 只拿公共任务、父代标量分数及已有训练技能。  RSI 自我改进与工作流 Agent 运行流程与自进化：改的是哪一层 可信 callback 的 CPU 控制器是否能说明完整 RSIFlow 已集成 Evolve？ 不能。当前 callback 与结构证据验证父代保护、paired 接纳、失败保存和训练报告隔离，没有内置 LLM、任意程序执行或六 benchmark 训练。声明修改作用域与数值 fixture 高分不能替代真实候选执行及晋级评估，进程内接口也不是恶意代码沙箱。 例如 scalar proposer 改一个数值并涨分，只证明控制器分支可达，不代表真实模型参数或 harness 已按论文更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7df2699c3716bd8a">可信 callback 的 CPU 控制器是否能说明完整 RSIFlow 已集成 Evolve？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsiflow">RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前 callback 与结构证据验证父代保护、paired 接纳、失败保存和训练报告隔离，没有内置 LLM、任意程序执行或六 benchmark 训练。声明修改作用域与数值 fixture 高分不能替代真实候选执行及晋级评估，进程内接口也不是恶意代码沙箱。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 scalar proposer 改一个数值并涨分，只证明控制器分支可达，不代表真实模型参数或 harness 已按论文更新。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射、成本与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21791">原论文</a> · <a href="../../../../agent-research/2610.21791-rsiflow/">实现解读</a> · <a href="#qa-7df2699c3716bd8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:terminal-rsi" data-paper-title="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine Agent Tencent Hy Frontier / National University of Singapore 2026-10-15 终端 Agent 既要从验证成功的轨迹里学会可重现行为，也要把稀疏完成反馈传给很早的动作。Terminal-RSI 交替 RSR 轨迹改写和保留 critic 权重的 RPR，阶段开始时先校准 critic；提出 TB-GAE 用交互 turn 时钟而非 observation 文本长度衰减，并用 family 校准的 FDR 过渡到严格完成优先的 SPR。 原文 Qwen3.8-27B、256K、多阶段分布式训练、3,000 任务及长终端环境，对单 A100/A30/Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 数值诊断。只执行 TB-GAE、精确 chunk 续接和 FDR/SPR，不执行 shell、终端 Agent 或 PPO 训练。原文 TB-GAE 的 checkpoint 实际使用情况有明确未核实边界。每 seed 初始化 20 个 generated-token value，五个 turn、一个终端奖励；再插入 40 个 observation，核对结果不变。  RSI Agent RL 长程终端任务 Agent 运行流程与自进化：改的是哪一层 终端 Agent 的长任务为什么给强化学习带来比单轮回答更难的反馈问题？ 终端任务包含命令、长观察和多轮状态变化，成功往往到最后才确定，早期动作贡献难分配；失败也可能离完成只差一步。Terminal RSI 研究在这种交互结构中组织奖励和优势，支持持续训练。部分进展不等于完成，观察文本长度也不能直接代表真实交互时间。 教学例：Agent 已修好代码却未运行最后测试，终局只有失败会掩盖此前有效动作；训练需要利用进度，同时保持完成标准。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-terminal-rsi-d5ceabe6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ee2baf6e22e38c51">终端 Agent 的长任务为什么给强化学习带来比单轮回答更难的反馈问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aterminal-rsi">Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Hy Frontier / National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终端任务包含命令、长观察和多轮状态变化，成功往往到最后才确定，早期动作贡献难分配；失败也可能离完成只差一步。Terminal RSI 研究在这种交互结构中组织奖励和优势，支持持续训练。部分进展不等于完成，观察文本长度也不能直接代表真实交互时间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：Agent 已修好代码却未运行最后测试，终局只有失败会掩盖此前有效动作；训练需要利用进度，同时保持完成标准。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22192">原论文</a> · <a href="../../../../agent-research/2610.22192-terminal-rsi/">实现解读</a> · <a href="#qa-ee2baf6e22e38c51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:terminal-rsi" data-paper-title="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine Agent Tencent Hy Frontier / National University of Singapore 2026-10-15 终端 Agent 既要从验证成功的轨迹里学会可重现行为，也要把稀疏完成反馈传给很早的动作。Terminal-RSI 交替 RSR 轨迹改写和保留 critic 权重的 RPR，阶段开始时先校准 critic；提出 TB-GAE 用交互 turn 时钟而非 observation 文本长度衰减，并用 family 校准的 FDR 过渡到严格完成优先的 SPR。 原文 Qwen3.8-27B、256K、多阶段分布式训练、3,000 任务及长终端环境，对单 A100/A30/Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 数值诊断。只执行 TB-GAE、精确 chunk 续接和 FDR/SPR，不执行 shell、终端 Agent 或 PPO 训练。原文 TB-GAE 的 checkpoint 实际使用情况有明确未核实边界。每 seed 初始化 20 个 generated-token value，五个 turn、一个终端奖励；再插入 40 个 observation，核对结果不变。  RSI Agent RL 长程终端任务 Agent 运行流程与自进化：改的是哪一层 TB-GAE 为什么按交互 turn 衰减，而不是按 observation 文本长度衰减？ 工具输出长度并不对应额外决策时间，若把长 observation 当很多递推节点，早期动作的信用会被无意义地过度衰减。方法仅在生成 token 上递推，同 turn 不衰减、跨 turn 才用折扣；分块续接还需 value 和 advantage，计算切块不是环境终止。 例如两次执行结果相同，一份日志十行、一份千行，不应仅因冗长日志就把之前动作的奖励信用压低更多。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:terminal-rsi" data-paper-title="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine Agent Tencent Hy Frontier / National University of Singapore 2026-10-15 终端 Agent 既要从验证成功的轨迹里学会可重现行为，也要把稀疏完成反馈传给很早的动作。Terminal-RSI 交替 RSR 轨迹改写和保留 critic 权重的 RPR，阶段开始时先校准 critic；提出 TB-GAE 用交互 turn 时钟而非 observation 文本长度衰减，并用 family 校准的 FDR 过渡到严格完成优先的 SPR。 原文 Qwen3.8-27B、256K、多阶段分布式训练、3,000 任务及长终端环境，对单 A100/A30/Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 数值诊断。只执行 TB-GAE、精确 chunk 续接和 FDR/SPR，不执行 shell、终端 Agent 或 PPO 训练。原文 TB-GAE 的 checkpoint 实际使用情况有明确未核实边界。每 seed 初始化 20 个 generated-token value，五个 turn、一个终端奖励；再插入 40 个 observation，核对结果不变。  RSI Agent RL 长程终端任务 Agent 运行流程与自进化：改的是哪一层 SPR 与单纯部分得分 FDR 为什么有不同排序边界？ FDR 按 family divisor 缩放部分分且无固定上界，失败高部分分可超成功；SPR 加严格成功并将部分分压到一以内，确保失败低于严格成功。这个排序性质不是策略梯度方差或势函数不变证明，也不能将原文整套训练收益归给此公式。 例如未完成任务部分分很高，FDR 可能超过一；SPR 仍把它放在任何严格成功的最低分之下。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-21c071abd587613f">SPR 与单纯部分得分 FDR 为什么有不同排序边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aterminal-rsi">Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Hy Frontier / National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>FDR 按 family divisor 缩放部分分且无固定上界，失败高部分分可超成功；SPR 加严格成功并将部分分压到一以内，确保失败低于严格成功。这个排序性质不是策略梯度方差或势函数不变证明，也不能将原文整套训练收益归给此公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如未完成任务部分分很高，FDR 可能超过一；SPR 仍把它放在任何严格成功的最低分之下。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22192">原论文</a> · <a href="../../../../agent-research/2610.22192-terminal-rsi/">实现解读</a> · <a href="#qa-21c071abd587613f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:terminal-rsi" data-paper-title="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine Agent Tencent Hy Frontier / National University of Singapore 2026-10-15 终端 Agent 既要从验证成功的轨迹里学会可重现行为，也要把稀疏完成反馈传给很早的动作。Terminal-RSI 交替 RSR 轨迹改写和保留 critic 权重的 RPR，阶段开始时先校准 critic；提出 TB-GAE 用交互 turn 时钟而非 observation 文本长度衰减，并用 family 校准的 FDR 过渡到严格完成优先的 SPR。 原文 Qwen3.8-27B、256K、多阶段分布式训练、3,000 任务及长终端环境，对单 A100/A30/Mac 成本过高，成本过高，不复现（审查 DONE）。component_only / L1 CPU 数值诊断。只执行 TB-GAE、精确 chunk 续接和 FDR/SPR，不执行 shell、终端 Agent 或 PPO 训练。原文 TB-GAE 的 checkpoint 实际使用情况有明确未核实边界。每 seed 初始化 20 个 generated-token value，五个 turn、一个终端奖励；再插入 40 个 observation，核对结果不变。  RSI Agent RL 长程终端任务 Agent 运行流程与自进化：改的是哪一层 分 chunk 计算 GAE 时，为什么只传 value bootstrap 不够？ 计算分块不是环境终止，需同时传下一 value 与下一 advantage 才保留尾部 trace，终末奖励只发一次。observation 不作为递推节点；本地只有数值算子，无 actor/critic、RSR 或真实终端训练，unit-clock 等价也不证明 TB-GAE 已在线部署。 例如在第十一个生成 token 切块后把尾部 advantage 清零，会丢失后续奖励向前传播，即使 value 接对也不等价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-888eaed3118a74ba">分 chunk 计算 GAE 时，为什么只传 value bootstrap 不够？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aterminal-rsi">Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Hy Frontier / National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>计算分块不是环境终止，需同时传下一 value 与下一 advantage 才保留尾部 trace，终末奖励只发一次。observation 不作为递推节点；本地只有数值算子，无 actor/critic、RSR 或真实终端训练，unit-clock 等价也不证明 TB-GAE 已在线部署。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如在第十一个生成 token 切块后把尾部 advantage 清零，会丢失后续奖励向前传播，即使 value 接对也不等价。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射、成本与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22192">原论文</a> · <a href="../../../../agent-research/2610.22192-terminal-rsi/">实现解读</a> · <a href="#qa-888eaed3118a74ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:torsi" data-paper-title="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock Agent Peking University / Samsung Research 2026-10-14 游戏在模型推理时继续前进，观测时正确的动作在执行时可能已失效。原文 §3–4提出 RealtimeBench 的 paused／live／accelerated 时钟比较，及 Two-Timescale Offline Recursive Self-Improvement：快学生在实况中独立行动，慢教师只在两次尝试之间读失败轨迹、在 feedback 保存状态上离线练习，并改写可复用指导。指导冻结后只由独立 validation 决定是否替换；test 不参与修订或选择。 成本过高，不复现（审查 DONE）。本地未运行 Mario/Snake 等引擎、Jev、教师或异步控制，不把数值 fixture 当实时能力评测；evaluation_protocol_interface / L1 CPU。只有时钟、反馈隔离与指导接受协议，没有实时游戏或模型能力复现。每 seed 随机生成 16 个计时事件和 12 个数值 validation 行；独立检查 action age 比只统计响应延迟多出的调度时间、严格增益、平局与下降拒绝。teacher 仅收到人工 feedback 轨迹。逐 seed 实测和来源 hash 见 CPU 产物，不代表游戏进展或 Jev 改善。  RSI 实时决策与离线指导进化 Agent 运行流程与自进化：改的是哪一层 实时 Agent 为什么可能“想得更好”，却因为响应太慢而做错事？ 任务环境会在推理期间继续变化，基于旧观察生成的动作到执行时可能已经过期。TORSI 研究在实时约束下改进小型执行策略，让高质量指导不必都发生在在线关键路径。离线学习和在线响应要分别核算，静态任务准确率不能代替真实时间环境中的有效行动。 教学例：目标在移动，模型花很久算出对旧位置的正确动作，执行时仍会落空；需要同时关注响应速度和信息新鲜度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-torsi-cd7ddf6f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-814a0e85a5594988">实时 Agent 为什么可能“想得更好”，却因为响应太慢而做错事？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atorsi">The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University / Samsung Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务环境会在推理期间继续变化，基于旧观察生成的动作到执行时可能已经过期。TORSI 研究在实时约束下改进小型执行策略，让高质量指导不必都发生在在线关键路径。离线学习和在线响应要分别核算，静态任务准确率不能代替真实时间环境中的有效行动。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：目标在移动，模型花很久算出对旧位置的正确动作，执行时仍会落空；需要同时关注响应速度和信息新鲜度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20665">原论文</a> · <a href="../../../../agent-research/2610.20665-torsi/">实现解读</a> · <a href="#qa-814a0e85a5594988">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:torsi" data-paper-title="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock Agent Peking University / Samsung Research 2026-10-14 游戏在模型推理时继续前进，观测时正确的动作在执行时可能已失效。原文 §3–4提出 RealtimeBench 的 paused／live／accelerated 时钟比较，及 Two-Timescale Offline Recursive Self-Improvement：快学生在实况中独立行动，慢教师只在两次尝试之间读失败轨迹、在 feedback 保存状态上离线练习，并改写可复用指导。指导冻结后只由独立 validation 决定是否替换；test 不参与修订或选择。 成本过高，不复现（审查 DONE）。本地未运行 Mario/Snake 等引擎、Jev、教师或异步控制，不把数值 fixture 当实时能力评测；evaluation_protocol_interface / L1 CPU。只有时钟、反馈隔离与指导接受协议，没有实时游戏或模型能力复现。每 seed 随机生成 16 个计时事件和 12 个数值 validation 行；独立检查 action age 比只统计响应延迟多出的调度时间、严格增益、平局与下降拒绝。teacher 仅收到人工 feedback 轨迹。逐 seed 实测和来源 hash 见 CPU 产物，不代表游戏进展或 Jev 改善。  RSI 实时决策与离线指导进化 Agent 运行流程与自进化：改的是哪一层 response latency 与 action age 为什么不能混成一个指标？ 前者到模型返回为止，后者还包含排队和应用动作的时间；实况环境持续变化，返回快也可能因应用晚而失效。慢教师只能在尝试之间用反馈练习和改指导，再由独立 validation 决定是否替换，不能在 live test 中偷看未来状态修正动作。 例如模型一秒内决定跳跃，命令又排队两秒才执行，此时障碍已移走；动作年龄三秒，比单纯响应一秒更能解释失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:torsi" data-paper-title="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock Agent Peking University / Samsung Research 2026-10-14 游戏在模型推理时继续前进，观测时正确的动作在执行时可能已失效。原文 §3–4提出 RealtimeBench 的 paused／live／accelerated 时钟比较，及 Two-Timescale Offline Recursive Self-Improvement：快学生在实况中独立行动，慢教师只在两次尝试之间读失败轨迹、在 feedback 保存状态上离线练习，并改写可复用指导。指导冻结后只由独立 validation 决定是否替换；test 不参与修订或选择。 成本过高，不复现（审查 DONE）。本地未运行 Mario/Snake 等引擎、Jev、教师或异步控制，不把数值 fixture 当实时能力评测；evaluation_protocol_interface / L1 CPU。只有时钟、反馈隔离与指导接受协议，没有实时游戏或模型能力复现。每 seed 随机生成 16 个计时事件和 12 个数值 validation 行；独立检查 action age 比只统计响应延迟多出的调度时间、严格增益、平局与下降拒绝。teacher 仅收到人工 feedback 轨迹。逐 seed 实测和来源 hash 见 CPU 产物，不代表游戏进展或 Jev 改善。  RSI 实时决策与离线指导进化 Agent 运行流程与自进化：改的是哪一层 慢教师在线接管与 TORSI 两次尝试间离线指导有什么区别？ 在线接管会让慢模型直接参与实时控制，可能因延迟失效；TORSI 让慢教师在尝试间分析 feedback 并练习，冻结指导后快学生独立执行。教师不能读 test 来修订，指导只由独立 validation 的严格增益接纳，不应把回放练习当实况执行。 例如教师可离线解释某次追踪失败，但下一场 live 仍由学生自己快速选动作，不能暂停世界等教师逐步告诉答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-02ca6afaa67ea658">慢教师在线接管与 TORSI 两次尝试间离线指导有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atorsi">The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University / Samsung Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>在线接管会让慢模型直接参与实时控制，可能因延迟失效；TORSI 让慢教师在尝试间分析 feedback 并练习，冻结指导后快学生独立执行。教师不能读 test 来修订，指导只由独立 validation 的严格增益接纳，不应把回放练习当实况执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师可离线解释某次追踪失败，但下一场 live 仍由学生自己快速选动作，不能暂停世界等教师逐步告诉答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20665">原论文</a> · <a href="../../../../agent-research/2610.20665-torsi/">实现解读</a> · <a href="#qa-02ca6afaa67ea658">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:torsi" data-paper-title="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock Agent Peking University / Samsung Research 2026-10-14 游戏在模型推理时继续前进，观测时正确的动作在执行时可能已失效。原文 §3–4提出 RealtimeBench 的 paused／live／accelerated 时钟比较，及 Two-Timescale Offline Recursive Self-Improvement：快学生在实况中独立行动，慢教师只在两次尝试之间读失败轨迹、在 feedback 保存状态上离线练习，并改写可复用指导。指导冻结后只由独立 validation 决定是否替换；test 不参与修订或选择。 成本过高，不复现（审查 DONE）。本地未运行 Mario/Snake 等引擎、Jev、教师或异步控制，不把数值 fixture 当实时能力评测；evaluation_protocol_interface / L1 CPU。只有时钟、反馈隔离与指导接受协议，没有实时游戏或模型能力复现。每 seed 随机生成 16 个计时事件和 12 个数值 validation 行；独立检查 action age 比只统计响应延迟多出的调度时间、严格增益、平局与下降拒绝。teacher 仅收到人工 feedback 轨迹。逐 seed 实测和来源 hash 见 CPU 产物，不代表游戏进展或 Jev 改善。  RSI 实时决策与离线指导进化 Agent 运行流程与自进化：改的是哪一层 validation 打平时是否接纳新指导，本地测到什么？ 不接纳，完整相同 task ID 配对的平均增益须严格大于零，且 feedback、validation、test 分离。时间戳需有限有序；本地只验证计时和数值选择合同，未运行游戏引擎、Jev 或教师，不能把 fixture 的动作年龄差写成游戏进展提升。 例如新旧指导各得到同样验证分，不能因新说明更长就替换；也不能看 test 略好后再反向选它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2759040921440d2b">validation 打平时是否接纳新指导，本地测到什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atorsi">The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University / Samsung Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不接纳，完整相同 task ID 配对的平均增益须严格大于零，且 feedback、validation、test 分离。时间戳需有限有序；本地只验证计时和数值选择合同，未运行游戏引擎、Jev 或教师，不能把 fixture 的动作年龄差写成游戏进展提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新旧指导各得到同样验证分，不能因新说明更长就替换；也不能看 test 略好后再反向选它。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20665">原论文</a> · <a href="../../../../agent-research/2610.20665-torsi/">实现解读</a> · <a href="#qa-2759040921440d2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harmony-harness" data-paper-title="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses Agent Google Cloud AI Research / Carnegie Mellon University 2026-10-10 单目标演化可能通过放松检查提高功能分数，同时损害安全。Harmony Harness 将功能与安全保持为两个独立目标：每个偏好向量维护一个框架，候选只替换邻域中更差的框架。工具、技能、逻辑分别记录在通用或环境专属范围，再由组合器为当前任务选择执行 DAG。图为依据原文 Figure 1 重绘的机制说明，不是本地执行记录。原图与正文。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。Gemini 3.6 Flash 承担 proposer 与 solver；三次独立运行、多代多子问题，真实 Docker 构建和 exploit 评估主导耗时（§5、附录 C/G/I）。完整实验成本过高，不复现（审查 DONE）；成本判断源于论文规模，不是本地测量。  自进化与经验复用 多目标Harness演化 Agent 运行流程与自进化：改的是哪一层 功能与安全为什么不能先合成一个未经约束的平均分？ 功能提升可能来自放松检查，而平均分允许高功能抵消严重安全退化。Harmony 保留两个目标，以偏好子问题和邻域替换组织搜索，要求部署同时考虑二者；它不等于证明所有攻击都安全，也不能把独立边际率当同轨迹联合成功。 例如一条轨迹完成任务却泄露受保护数据，应记功能成功、安全失败，而不是靠功能高分平均成合格。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harmony-harness-9020f112" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e5785ba0eb74fff6">功能与安全为什么不能先合成一个未经约束的平均分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharmony-harness">Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>功能提升可能来自放松检查，而平均分允许高功能抵消严重安全退化。Harmony 保留两个目标，以偏好子问题和邻域替换组织搜索，要求部署同时考虑二者；它不等于证明所有攻击都安全，也不能把独立边际率当同轨迹联合成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条轨迹完成任务却泄露受保护数据，应记功能成功、安全失败，而不是靠功能高分平均成合格。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15150v1">原论文</a> · <a href="../../../../agent-research/2610.15150-harmony-harness/">实现解读</a> · <a href="#qa-e5785ba0eb74fff6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harmony-harness" data-paper-title="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses Agent Google Cloud AI Research / Carnegie Mellon University 2026-10-10 单目标演化可能通过放松检查提高功能分数，同时损害安全。Harmony Harness 将功能与安全保持为两个独立目标：每个偏好向量维护一个框架，候选只替换邻域中更差的框架。工具、技能、逻辑分别记录在通用或环境专属范围，再由组合器为当前任务选择执行 DAG。图为依据原文 Figure 1 重绘的机制说明，不是本地执行记录。原图与正文。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。Gemini 3.6 Flash 承担 proposer 与 solver；三次独立运行、多代多子问题，真实 Docker 构建和 exploit 评估主导耗时（§5、附录 C/G/I）。完整实验成本过高，不复现（审查 DONE）；成本判断源于论文规模，不是本地测量。  自进化与经验复用 多目标Harness演化 Agent 运行流程与自进化：改的是哪一层 为什么 min(功能成功率,安全成功率) 不能当成联合成功率？ 两项边际率可能来自不同轨迹，只有同一次执行同时满足两条件才算联合成功。多目标搜索用偏好与邻域替换维护取舍，不能靠放松安全提高功能总分；最终选择集和 held-out 也要分开，否则框架会把报告环境当搜索反馈使用。 例如十次里八次功能成功、八次安全通过，但失败恰好错开，联合可能只有六次；取两项最小值八次会高估。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harmony-harness" data-paper-title="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses Agent Google Cloud AI Research / Carnegie Mellon University 2026-10-10 单目标演化可能通过放松检查提高功能分数，同时损害安全。Harmony Harness 将功能与安全保持为两个独立目标：每个偏好向量维护一个框架，候选只替换邻域中更差的框架。工具、技能、逻辑分别记录在通用或环境专属范围，再由组合器为当前任务选择执行 DAG。图为依据原文 Figure 1 重绘的机制说明，不是本地执行记录。原图与正文。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。Gemini 3.6 Flash 承担 proposer 与 solver；三次独立运行、多代多子问题，真实 Docker 构建和 exploit 评估主导耗时（§5、附录 C/G/I）。完整实验成本过高，不复现（审查 DONE）；成本判断源于论文规模，不是本地测量。  自进化与经验复用 多目标Harness演化 Agent 运行流程与自进化：改的是哪一层 weighted Chebyshev 与固定线性加权在保留候选上有什么差别？ Chebyshev 看相对理想点的最大加权偏差，强调短板；不同偏好向量各维护框架，只在邻域严格改善时替换且一次最多两个。固定线性和可让一个目标大幅提升抵消另一目标损失，两种选择几何不同，但都依赖评估可靠。 例如候选功能九成安全三成，最大偏差会突出安全短板，而简单平均可能仍胜过均衡方案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-80c7d1bd28aa88ae">weighted Chebyshev 与固定线性加权在保留候选上有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharmony-harness">Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Chebyshev 看相对理想点的最大加权偏差，强调短板；不同偏好向量各维护框架，只在邻域严格改善时替换且一次最多两个。固定线性和可让一个目标大幅提升抵消另一目标损失，两种选择几何不同，但都依赖评估可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选功能九成安全三成，最大偏差会突出安全短板，而简单平均可能仍胜过均衡方案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15150v1">原论文</a> · <a href="../../../../agent-research/2610.15150-harmony-harness/">实现解读</a> · <a href="#qa-80c7d1bd28aa88ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harmony-harness" data-paper-title="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses Agent Google Cloud AI Research / Carnegie Mellon University 2026-10-10 单目标演化可能通过放松检查提高功能分数，同时损害安全。Harmony Harness 将功能与安全保持为两个独立目标：每个偏好向量维护一个框架，候选只替换邻域中更差的框架。工具、技能、逻辑分别记录在通用或环境专属范围，再由组合器为当前任务选择执行 DAG。图为依据原文 Figure 1 重绘的机制说明，不是本地执行记录。原图与正文。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。Gemini 3.6 Flash 承担 proposer 与 solver；三次独立运行、多代多子问题，真实 Docker 构建和 exploit 评估主导耗时（§5、附录 C/G/I）。完整实验成本过高，不复现（审查 DONE）；成本判断源于论文规模，不是本地测量。  自进化与经验复用 多目标Harness演化 Agent 运行流程与自进化：改的是哪一层 最终 max-min 选择可以在 held-out OOD 上挑最优框架吗？ 不能。最终框架由搜索集功能安全估计的 max-min 选出，held-out ID/OOD 留作评价。联合率需同一轨迹两条件都满足；本地没有 MOEA/D、真实 Docker 或 exploit 评测，实现标量化公式也不能宣称完整自进化已验证。 例如功能八成、安全七成的边际率不能直接写联合七成，失败可能落在不同任务上，必须逐轨迹求交集。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f4f53be87255685f">最终 max-min 选择可以在 held-out OOD 上挑最优框架吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharmony-harness">Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。最终框架由搜索集功能安全估计的 max-min 选出，held-out ID/OOD 留作评价。联合率需同一轨迹两条件都满足；本地没有 MOEA/D、真实 Docker 或 exploit 评测，实现标量化公式也不能宣称完整自进化已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如功能八成、安全七成的边际率不能直接写联合七成，失败可能落在不同任务上，必须逐轨迹求交集。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与成本判断；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.15150v1">原论文</a> · <a href="../../../../agent-research/2610.15150-harmony-harness/">实现解读</a> · <a href="#qa-f4f53be87255685f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness2" data-paper-title="Harness²: Recursive Agent Harnessing for an Open World" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness²: Recursive Agent Harnessing for an Open World Agent Northwestern University 2026-10-09 Harness 是模型外的提示、工具、记忆、技能、脚本、子代理和中间件。论文在不改模型权重的前提下，把“改进当前任务执行方式”和“积累以后如何改进的经验”连接起来。它不要求任务答案、评分细则或验证器：先观察执行，再提出通用候选与领域候选，执行二者，最后按行为差异组合，而不是把某个评分函数冒充正确性判定。论文 §2 高成本完整实验：成本过高，不复现（审查 DONE）。编辑器诊断脚本中的正数过滤，通用分支更新约束，领域分支删除不符合公开任务的过滤，组合分支合并实际执行过的修改。component_only / L1 CPU 控制器与接口。真实执行 Python 探针，但 editor、selector 是确定性机制测试替身；不是模型支持的 Agent 能力评测，也不是已接入 Evolve。只使用 Python 标准库，无模型下载、API 凭证或 GPU。产物存在时拒绝覆盖，重复执行请换输出路径。实际探针在临时目录运行可信 Python 脚本，单次 subprocess 超时 5 秒；  规划、搜索与反思 Harness 与自我改进 Agent 运行流程与自进化：改的是哪一层 Harness² 为什么研究在没有标准答案和评分细则时改进 Agent 的工作流程？ 很多真实任务只有交付要求，没有随时可调用的正确性 oracle，仍可能通过执行探测发现流程不足。Harness² 研究从提案、探测和组合中构造更合适的 harness。观察到改动或获得高自评分不代表答案正确，最终产物需要与生成流程分开的选择和检查。 教学例：整理一份开放研究报告，没有唯一标准答案；可先探测来源获取和组织流程，再检查匿名产物，而不是直接相信作者自评。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harness2-5c8a24eb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-56f8f0526251b9f6">Harness² 为什么研究在没有标准答案和评分细则时改进 Agent 的工作流程？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness2">Harness²: Recursive Agent Harnessing for an Open World</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>很多真实任务只有交付要求，没有随时可调用的正确性 oracle，仍可能通过执行探测发现流程不足。Harness² 研究从提案、探测和组合中构造更合适的 harness。观察到改动或获得高自评分不代表答案正确，最终产物需要与生成流程分开的选择和检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：整理一份开放研究报告，没有唯一标准答案；可先探测来源获取和组织流程，再检查匿名产物，而不是直接相信作者自评。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14224">原论文</a> · <a href="../../../../agent-research/2610.14224-harness2/">实现解读</a> · <a href="#qa-56f8f0526251b9f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness2" data-paper-title="Harness²: Recursive Agent Harnessing for an Open World" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness²: Recursive Agent Harnessing for an Open World Agent Northwestern University 2026-10-09 Harness 是模型外的提示、工具、记忆、技能、脚本、子代理和中间件。论文在不改模型权重的前提下，把“改进当前任务执行方式”和“积累以后如何改进的经验”连接起来。它不要求任务答案、评分细则或验证器：先观察执行，再提出通用候选与领域候选，执行二者，最后按行为差异组合，而不是把某个评分函数冒充正确性判定。论文 §2 高成本完整实验：成本过高，不复现（审查 DONE）。编辑器诊断脚本中的正数过滤，通用分支更新约束，领域分支删除不符合公开任务的过滤，组合分支合并实际执行过的修改。component_only / L1 CPU 控制器与接口。真实执行 Python 探针，但 editor、selector 是确定性机制测试替身；不是模型支持的 Agent 能力评测，也不是已接入 Evolve。只使用 Python 标准库，无模型下载、API 凭证或 GPU。产物存在时拒绝覆盖，重复执行请换输出路径。实际探针在临时目录运行可信 Python 脚本，单次 subprocess 超时 5 秒；  规划、搜索与反思 Harness 与自我改进 Agent 运行流程与自进化：改的是哪一层 没有答案或评分细则时，Propose–Probe–Compose 怎样避免把自评分当作正确性 oracle？ 候选先真实执行，再依据公开任务与行为差异组合，证据来自轨迹和产物而非隐藏答案。多产物选择时匿名化，减少按 harness 身份偏好；这种开放改进不提供绝对正确保证，选择、反思和 probe 调用也必须计成本，不能只统计最终执行次数。 例如通用候选强化验证、领域候选改善检索，实际跑后可组合有用部分；不能因为其中一个自称最好就当作已经正确完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness2" data-paper-title="Harness²: Recursive Agent Harnessing for an Open World" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness²: Recursive Agent Harnessing for an Open World Agent Northwestern University 2026-10-09 Harness 是模型外的提示、工具、记忆、技能、脚本、子代理和中间件。论文在不改模型权重的前提下，把“改进当前任务执行方式”和“积累以后如何改进的经验”连接起来。它不要求任务答案、评分细则或验证器：先观察执行，再提出通用候选与领域候选，执行二者，最后按行为差异组合，而不是把某个评分函数冒充正确性判定。论文 §2 高成本完整实验：成本过高，不复现（审查 DONE）。编辑器诊断脚本中的正数过滤，通用分支更新约束，领域分支删除不符合公开任务的过滤，组合分支合并实际执行过的修改。component_only / L1 CPU 控制器与接口。真实执行 Python 探针，但 editor、selector 是确定性机制测试替身；不是模型支持的 Agent 能力评测，也不是已接入 Evolve。只使用 Python 标准库，无模型下载、API 凭证或 GPU。产物存在时拒绝覆盖，重复执行请换输出路径。实际探针在临时目录运行可信 Python 脚本，单次 subprocess 超时 5 秒；  规划、搜索与反思 Harness 与自我改进 Agent 运行流程与自进化：改的是哪一层 并行独立组合与顺序递归改进为什么不是相同候选依赖？ 并行模式分别提出通用和领域候选，再形成独立组合；顺序模式每步读此前 harness 与任务内历史，后步依赖前步结果。二者同为 4k 次执行、3k 次提案，选择器和反思另计，不能把并行等待减少当调用成本减少。 例如 k=2 时并行有两个独立最终组合，顺序则第二次在第一次结果上继续，候选之间依赖完全不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5b95ea9904b497c3">并行独立组合与顺序递归改进为什么不是相同候选依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness2">Harness²: Recursive Agent Harnessing for an Open World</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>并行模式分别提出通用和领域候选，再形成独立组合；顺序模式每步读此前 harness 与任务内历史，后步依赖前步结果。二者同为 4k 次执行、3k 次提案，选择器和反思另计，不能把并行等待减少当调用成本减少。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 k=2 时并行有两个独立最终组合，顺序则第二次在第一次结果上继续，候选之间依赖完全不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14224">原论文</a> · <a href="../../../../agent-research/2610.14224-harness2/">实现解读</a> · <a href="#qa-5b95ea9904b497c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness2" data-paper-title="Harness²: Recursive Agent Harnessing for an Open World" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness²: Recursive Agent Harnessing for an Open World Agent Northwestern University 2026-10-09 Harness 是模型外的提示、工具、记忆、技能、脚本、子代理和中间件。论文在不改模型权重的前提下，把“改进当前任务执行方式”和“积累以后如何改进的经验”连接起来。它不要求任务答案、评分细则或验证器：先观察执行，再提出通用候选与领域候选，执行二者，最后按行为差异组合，而不是把某个评分函数冒充正确性判定。论文 §2 高成本完整实验：成本过高，不复现（审查 DONE）。编辑器诊断脚本中的正数过滤，通用分支更新约束，领域分支删除不符合公开任务的过滤，组合分支合并实际执行过的修改。component_only / L1 CPU 控制器与接口。真实执行 Python 探针，但 editor、selector 是确定性机制测试替身；不是模型支持的 Agent 能力评测，也不是已接入 Evolve。只使用 Python 标准库，无模型下载、API 凭证或 GPU。产物存在时拒绝覆盖，重复执行请换输出路径。实际探针在临时目录运行可信 Python 脚本，单次 subprocess 超时 5 秒；  规划、搜索与反思 Harness 与自我改进 Agent 运行流程与自进化：改的是哪一层 最终 selector 为什么只看匿名产物，不能看 harness 身份或重新写答案？ 匿名选择减少按提案来源偏好，只能从实际最终产物中选，不能混入参考、提案中间物或生成新答案。k=1 直接采用；本地可信脚本探针核对执行账但非 LLM 开放任务，外层算术检查结果不能回灌 editor 或 reflector。 例如 selector 若知道哪份来自“高级方案”可能偏选身份；若自己再改答案，就不再是对已有执行产物的选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8f178bdac3b099db">最终 selector 为什么只看匿名产物，不能看 harness 身份或重新写答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness2">Harness²: Recursive Agent Harnessing for an Open World</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>匿名选择减少按提案来源偏好，只能从实际最终产物中选，不能混入参考、提案中间物或生成新答案。k=1 直接采用；本地可信脚本探针核对执行账但非 LLM 开放任务，外层算术检查结果不能回灌 editor 或 reflector。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 selector 若知道哪份来自“高级方案”可能偏选身份；若自己再改答案，就不再是对已有执行产物的选择。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14224">原论文</a> · <a href="../../../../agent-research/2610.14224-harness2/">实现解读</a> · <a href="#qa-8f178bdac3b099db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-anything" data-paper-title="RSI-Anything: Unlocking Recursive Self-Improvement with World Models" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Anything: Unlocking Recursive Self-Improvement with World Models Agent PhAI Labs / The Chinese University of Hong Kong 2026-10-09 候选先经世界模型预测，再向外部验证申请反馈；反馈更新持久 policy/workflow，可靠性不足且数据/预算足够时适配 predictor。只有组件检查和配对兼容性检查均通过的版本进入下一轮。事实来源：原文全文。 保持 concept_demo / L1、diagnostic_only=true、capability_comparison=false、evolve_promotion_eligible=false，不进入 Evolve 晋级。当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始 policy workflow 与初始 predictor 配对；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  recursive-self-improvement world-model compatibility-retention Agent 运行流程与自进化：改的是哪一层 世界模型预测为什么仍需要外部验证反馈？ 预测可提前筛选候选后果，但可能不准确，外部工具或环境才提供实际证据。RSI-Anything 据反馈更新持久 policy/workflow，只有可靠性不足且适配数据、预算都足够才更新 predictor；预测高分不是已验证任务成功。 例如预测某程序布局合法仍要跑可信几何检查器，若真实结果冲突，应记录预测失准而不是用预测代替验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-rsi-anything-7f27ef73" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-530166fda0dc63e5">世界模型预测为什么仍需要外部验证反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsi-anything">RSI-Anything: Unlocking Recursive Self-Improvement with World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PhAI Labs / The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预测可提前筛选候选后果，但可能不准确，外部工具或环境才提供实际证据。RSI-Anything 据反馈更新持久 policy/workflow，只有可靠性不足且适配数据、预算都足够才更新 predictor；预测高分不是已验证任务成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预测某程序布局合法仍要跑可信几何检查器，若真实结果冲突，应记录预测失准而不是用预测代替验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13912">原论文</a> · <a href="../../../../reproductions/2610.13912-rsi-anything/">实现解读</a> · <a href="#qa-530166fda0dc63e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-anything" data-paper-title="RSI-Anything: Unlocking Recursive Self-Improvement with World Models" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Anything: Unlocking Recursive Self-Improvement with World Models Agent PhAI Labs / The Chinese University of Hong Kong 2026-10-09 候选先经世界模型预测，再向外部验证申请反馈；反馈更新持久 policy/workflow，可靠性不足且数据/预算足够时适配 predictor。只有组件检查和配对兼容性检查均通过的版本进入下一轮。事实来源：原文全文。 保持 concept_demo / L1、diagnostic_only=true、capability_comparison=false、evolve_promotion_eligible=false，不进入 Evolve 晋级。当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始 policy workflow 与初始 predictor 配对；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  recursive-self-improvement world-model compatibility-retention Agent 运行流程与自进化：改的是哪一层 组件分别通过检查后，为什么还需要 policy 与 predictor 的配对兼容性检查？ 策略可能依赖旧预测器的状态或假设，新预测器单独准确也可能与它不兼容。配对检查验证一起运行的行为，失败就整体回退到已知配对；预测器适配还需可靠性不足、数据和预算充足，不能把每轮自动重训或单模块通过当成系统已进步。 例如预测器更新了动作编码顺序，策略仍按旧顺序读取，二者单测可过却联调失败，应回退整个组合而非只记各自通过。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-anything" data-paper-title="RSI-Anything: Unlocking Recursive Self-Improvement with World Models" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Anything: Unlocking Recursive Self-Improvement with World Models Agent PhAI Labs / The Chinese University of Hong Kong 2026-10-09 候选先经世界模型预测，再向外部验证申请反馈；反馈更新持久 policy/workflow，可靠性不足且数据/预算足够时适配 predictor。只有组件检查和配对兼容性检查均通过的版本进入下一轮。事实来源：原文全文。 保持 concept_demo / L1、diagnostic_only=true、capability_comparison=false、evolve_promotion_eligible=false，不进入 Evolve 晋级。当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始 policy workflow 与初始 predictor 配对；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  recursive-self-improvement world-model compatibility-retention Agent 运行流程与自进化：改的是哪一层 只更新 policy 与同时适配世界模型有什么取舍？ 固定 predictor 提供稳定评价却可能长期误导，适配可纠正分布偏移但增加成本并改变 policy 所依赖的接口。框架用可靠性、数据和预算门控，并做组件与配对检查，不能把任何一次 predictor loss 下降都当整体策略改进。 例如预测器学会新反馈格式后旧 workflow 可能读错字段，需要配对兼容验证，而不只单测两个组件各自能运行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-38c1c449ff5f70c3">只更新 policy 与同时适配世界模型有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsi-anything">RSI-Anything: Unlocking Recursive Self-Improvement with World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PhAI Labs / The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定 predictor 提供稳定评价却可能长期误导，适配可纠正分布偏移但增加成本并改变 policy 所依赖的接口。框架用可靠性、数据和预算门控，并做组件与配对检查，不能把任何一次 predictor loss 下降都当整体策略改进。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预测器学会新反馈格式后旧 workflow 可能读错字段，需要配对兼容验证，而不只单测两个组件各自能运行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13912">原论文</a> · <a href="../../../../reproductions/2610.13912-rsi-anything/">实现解读</a> · <a href="#qa-38c1c449ff5f70c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rsi-anything" data-paper-title="RSI-Anything: Unlocking Recursive Self-Improvement with World Models" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="RSI-Anything: Unlocking Recursive Self-Improvement with World Models Agent PhAI Labs / The Chinese University of Hong Kong 2026-10-09 候选先经世界模型预测，再向外部验证申请反馈；反馈更新持久 policy/workflow，可靠性不足且数据/预算足够时适配 predictor。只有组件检查和配对兼容性检查均通过的版本进入下一轮。事实来源：原文全文。 保持 concept_demo / L1、diagnostic_only=true、capability_comparison=false、evolve_promotion_eligible=false，不进入 Evolve 晋级。当前是 concept_demo / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始 policy workflow 与初始 predictor 配对；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  recursive-self-improvement world-model compatibility-retention Agent 运行流程与自进化：改的是哪一层 predictor 什么时候才允许适配，为什么不能每收到一次失败就更新？ 适配要求世界模型可靠性不足、有足够适配数据，并且更新预算能承担估计成本，三个条件共同成立才触发。失败未必来自预测器，样本不足时更新也可能追逐噪声。候选经外部验证后仍需版本归因和配对检查，本地短执行不证明长期自改进收益。 教学例：一次错误预测只满足不可靠线索，若适配数据不够或预算已耗尽，就不应强行训练，再把噪声更新当作学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a9314caa9163bb27">predictor 什么时候才允许适配，为什么不能每收到一次失败就更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arsi-anything">RSI-Anything: Unlocking Recursive Self-Improvement with World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PhAI Labs / The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>适配要求世界模型可靠性不足、有足够适配数据，并且更新预算能承担估计成本，三个条件共同成立才触发。失败未必来自预测器，样本不足时更新也可能追逐噪声。候选经外部验证后仍需版本归因和配对检查，本地短执行不证明长期自改进收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一次错误预测只满足不可靠线索，若适配数据不够或预算已耗尽，就不应强行训练，再把噪声更新当作学习。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、结果、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13912">原论文</a> · <a href="../../../../reproductions/2610.13912-rsi-anything/">实现解读</a> · <a href="#qa-a9314caa9163bb27">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoalloc" data-paper-title="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution Agent King Abdullah University of Science and Technology 2026-10-08 模型选择 Full、Partial 或 Discard，得到 Partial 证据后再选择继续/停止。已观察案例更新固定语句经验并反思策略；影子策略共享同一证据，以漏掉新最佳的次数优先、再比较评测成本。拒绝候选以概率做反事实评测，避免选择性反馈。原文达到基线时 Full 数减少 59–82%，同预算成绩提高 8.7–12.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。复用真实 Linux bubblewrap/prlimit Circle26 程序环境，可信几何检查器评分而非模型自报，沙箱失败即拒绝运行。Circle26 无 Partial，因此此运行只允许 Full/Discard。经验 ADD/UPDATE/DELETE 不允许 UPDATE 重写语句，未观察案例不可当证据，最多四条活跃/暂定和四条陈旧经验。  程序进化 评测预算 策略自进化 Agent 运行流程与自进化：改的是哪一层 Partial 后继续或停止为什么比一次性 Full/Discard 更灵活？ 部分评测可提供较便宜的初始证据，再决定是否支付完整成本，避免对明显差候选全测，也避免一开始就丢弃潜在赢家。它要求任务确有可信 Partial 信号，不能给不支持该模式的环境硬造部分分数。 例如程序先通过快速约束检查后再跑长性能评测可有意义，但 Circle26 当前接口没有 Partial，本地只能 Full 或 Discard。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-evoalloc-9a5390ec" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6fe37e2f64ef258e">Partial 后继续或停止为什么比一次性 Full/Discard 更灵活？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoalloc">EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · King Abdullah University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>部分评测可提供较便宜的初始证据，再决定是否支付完整成本，避免对明显差候选全测，也避免一开始就丢弃潜在赢家。它要求任务确有可信 Partial 信号，不能给不支持该模式的环境硬造部分分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如程序先通过快速约束检查后再跑长性能评测可有意义，但 Circle26 当前接口没有 Partial，本地只能 Full 或 Discard。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12086">原论文</a> · <a href="../../../../agent-research/2610.12086-evoalloc/">实现解读</a> · <a href="#qa-6fe37e2f64ef258e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoalloc" data-paper-title="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution Agent King Abdullah University of Science and Technology 2026-10-08 模型选择 Full、Partial 或 Discard，得到 Partial 证据后再选择继续/停止。已观察案例更新固定语句经验并反思策略；影子策略共享同一证据，以漏掉新最佳的次数优先、再比较评测成本。拒绝候选以概率做反事实评测，避免选择性反馈。原文达到基线时 Full 数减少 59–82%，同预算成绩提高 8.7–12.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。复用真实 Linux bubblewrap/prlimit Circle26 程序环境，可信几何检查器评分而非模型自报，沙箱失败即拒绝运行。Circle26 无 Partial，因此此运行只允许 Full/Discard。经验 ADD/UPDATE/DELETE 不允许 UPDATE 重写语句，未观察案例不可当证据，最多四条活跃/暂定和四条陈旧经验。  程序进化 评测预算 策略自进化 Agent 运行流程与自进化：改的是哪一层 为什么被 Discard 的候选还要以概率做反事实评测？ 若只评估被选中的程序，分配策略看不到错过优良候选的情况，容易把自身偏好越学越确定。随机反事实检查揭示漏掉新最佳的风险，影子策略还需共享同一证据；这些 Full 调用同样消耗预算，不能为显示节省而排除探索与 warmup。 例如筛选器把一个陌生写法丢弃，偶尔完整评测却发现它更好；这类证据才能纠正“陌生即低质”的选择性反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoalloc" data-paper-title="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution Agent King Abdullah University of Science and Technology 2026-10-08 模型选择 Full、Partial 或 Discard，得到 Partial 证据后再选择继续/停止。已观察案例更新固定语句经验并反思策略；影子策略共享同一证据，以漏掉新最佳的次数优先、再比较评测成本。拒绝候选以概率做反事实评测，避免选择性反馈。原文达到基线时 Full 数减少 59–82%，同预算成绩提高 8.7–12.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。复用真实 Linux bubblewrap/prlimit Circle26 程序环境，可信几何检查器评分而非模型自报，沙箱失败即拒绝运行。Circle26 无 Partial，因此此运行只允许 Full/Discard。经验 ADD/UPDATE/DELETE 不允许 UPDATE 重写语句，未观察案例不可当证据，最多四条活跃/暂定和四条陈旧经验。  程序进化 评测预算 策略自进化 Agent 运行流程与自进化：改的是哪一层 优先比较 missed newbest 而后比较成本，与单纯最少 Full 有何不同？ 只省评测可能丢掉真正最优候选，字典序先保护搜索质量，再在漏掉新最佳相同的情况下节省 Full 和 Partial。随机反事实评估被丢候选缓解选择性反馈，影子策略共享证据，不能只挑实际接受项评价 allocator。 例如甲少测十次却错过新冠军，乙多测两次保住冠军，按该目标不应仅因甲更便宜就晋级。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-89728affaf2b375a">优先比较 missed newbest 而后比较成本，与单纯最少 Full 有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoalloc">EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · King Abdullah University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只省评测可能丢掉真正最优候选，字典序先保护搜索质量，再在漏掉新最佳相同的情况下节省 Full 和 Partial。随机反事实评估被丢候选缓解选择性反馈，影子策略共享证据，不能只挑实际接受项评价 allocator。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如甲少测十次却错过新冠军，乙多测两次保住冠军，按该目标不应仅因甲更便宜就晋级。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12086">原论文</a> · <a href="../../../../agent-research/2610.12086-evoalloc/">实现解读</a> · <a href="#qa-89728affaf2b375a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoalloc" data-paper-title="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution Agent King Abdullah University of Science and Technology 2026-10-08 模型选择 Full、Partial 或 Discard，得到 Partial 证据后再选择继续/停止。已观察案例更新固定语句经验并反思策略；影子策略共享同一证据，以漏掉新最佳的次数优先、再比较评测成本。拒绝候选以概率做反事实评测，避免选择性反馈。原文达到基线时 Full 数减少 59–82%，同预算成绩提高 8.7–12.0%，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。复用真实 Linux bubblewrap/prlimit Circle26 程序环境，可信几何检查器评分而非模型自报，沙箱失败即拒绝运行。Circle26 无 Partial，因此此运行只允许 Full/Discard。经验 ADD/UPDATE/DELETE 不允许 UPDATE 重写语句，未观察案例不可当证据，最多四条活跃/暂定和四条陈旧经验。  程序进化 评测预算 策略自进化 Agent 运行流程与自进化：改的是哪一层 warmup、影子并集和反事实 Full 为何都计预算，短 GPU 运行何处未触发？ 这些评测实际发生且消耗资源，不能当管理开销免费；影子晋级还需观察两次分歧。本地四次真实 Full 最佳未超过初始程序，warmup 不足、无晋级，Partial 与双分歧仅由合同测试覆盖，不能把它们写成真实运行已全部触发。 例如影子要求额外测一个被主策略丢弃的程序，这次 Full 必须进成本，即使最终没有改变主冠军。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ad4d7c9071244a6f">warmup、影子并集和反事实 Full 为何都计预算，短 GPU 运行何处未触发？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoalloc">EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · King Abdullah University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这些评测实际发生且消耗资源，不能当管理开销免费；影子晋级还需观察两次分歧。本地四次真实 Full 最佳未超过初始程序，warmup 不足、无晋级，Partial 与双分歧仅由合同测试覆盖，不能把它们写成真实运行已全部触发。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如影子要求额外测一个被主策略丢弃的程序，这次 Full 必须进成本，即使最终没有改变主冠军。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12086">原论文</a> · <a href="../../../../agent-research/2610.12086-evoalloc/">实现解读</a> · <a href="#qa-ad4d7c9071244a6f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mass" data-paper-title="Recursive Self-Improvement through Multi-Agent Self-Supervision" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Recursive Self-Improvement through Multi-Agent Self-Supervision Agent UC Berkeley 2026-10-08 同一模型执行、提出工作流并成对评价。固定权重下搜索后，独立采集轨迹，以 Bradley–Terry 排名选择前 K−1 条训练、第 K 条验证；仅移除编排者初始工作流提示，保留工作者分工。助手 token 的 SFT 更新权重后再重复。原文 Qwen3.6-27B 两轮在研究任务中提高单位输出 token 表现约 1.2–1.6 倍，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。真实共享 checkpoint 完成两轮搜索、裁判、轨迹采集与 LoRA SFT。本地为固定两工作者和一编排者的有界文本工作流族，可改变角色指令和传递内容；未接入任意工作流图、qwen-code 文件/终端工具，因此不是完整科研 coding-agent 复现。  递归自改进 工作流搜索 多智能体自监督 Agent 运行流程与自进化：改的是哪一层 固定权重搜索与之后 SFT 为什么要分开采集轨迹？ 先搜索工作流避免在探索中混入参数变化，再独立生成轨迹排名，选较优样本训练、留一条验证，之后才更新共享模型。执行、提案和评价由同模型承担，不代表自评分无偏；自生成验证 loss 不等于独立任务正确率。 例如某工作流在搜索时表现好，还要另采实际执行轨迹用于训练，不能把搜索中同一条偶然高分直接当独立验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-mass-a7f2d6e4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a53cbfd37dcfcacc">固定权重搜索与之后 SFT 为什么要分开采集轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amass">Recursive Self-Improvement through Multi-Agent Self-Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先搜索工作流避免在探索中混入参数变化，再独立生成轨迹排名，选较优样本训练、留一条验证，之后才更新共享模型。执行、提案和评价由同模型承担，不代表自评分无偏；自生成验证 loss 不等于独立任务正确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某工作流在搜索时表现好，还要另采实际执行轨迹用于训练，不能把搜索中同一条偶然高分直接当独立验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12176">原论文</a> · <a href="../../../../agent-research/2610.12176-mass/">实现解读</a> · <a href="#qa-a53cbfd37dcfcacc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mass" data-paper-title="Recursive Self-Improvement through Multi-Agent Self-Supervision" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Recursive Self-Improvement through Multi-Agent Self-Supervision Agent UC Berkeley 2026-10-08 同一模型执行、提出工作流并成对评价。固定权重下搜索后，独立采集轨迹，以 Bradley–Terry 排名选择前 K−1 条训练、第 K 条验证；仅移除编排者初始工作流提示，保留工作者分工。助手 token 的 SFT 更新权重后再重复。原文 Qwen3.6-27B 两轮在研究任务中提高单位输出 token 表现约 1.2–1.6 倍，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。真实共享 checkpoint 完成两轮搜索、裁判、轨迹采集与 LoRA SFT。本地为固定两工作者和一编排者的有界文本工作流族，可改变角色指令和传递内容；未接入任意工作流图、qwen-code 文件/终端工具，因此不是完整科研 coding-agent 复现。  递归自改进 工作流搜索 多智能体自监督 Agent 运行流程与自进化：改的是哪一层 为什么训练前要移除编排者初始工作流提示，却保留工作者分工？ 初始提示承载搜索得到的工作流，直接保留可能让训练只学依赖这段外部说明，而非吸收有用协作行为。保留角色分工仍维持实际执行结构，再对助手 token 做监督；Bradley–Terry 排名用于筛轨迹，也不能把自评排序直接当独立任务能力证明。 例如搜索提示详细规定先检索再核对，训练移除该起始说明，让模型从成功执行学习流程，但保留实际检索者和核对者的对话。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mass" data-paper-title="Recursive Self-Improvement through Multi-Agent Self-Supervision" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Recursive Self-Improvement through Multi-Agent Self-Supervision Agent UC Berkeley 2026-10-08 同一模型执行、提出工作流并成对评价。固定权重下搜索后，独立采集轨迹，以 Bradley–Terry 排名选择前 K−1 条训练、第 K 条验证；仅移除编排者初始工作流提示，保留工作者分工。助手 token 的 SFT 更新权重后再重复。原文 Qwen3.6-27B 两轮在研究任务中提高单位输出 token 表现约 1.2–1.6 倍，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。真实共享 checkpoint 完成两轮搜索、裁判、轨迹采集与 LoRA SFT。本地为固定两工作者和一编排者的有界文本工作流族，可改变角色指令和传递内容；未接入任意工作流图、qwen-code 文件/终端工具，因此不是完整科研 coding-agent 复现。  递归自改进 工作流搜索 多智能体自监督 Agent 运行流程与自进化：改的是哪一层 BT 排名中留出第 K 条轨迹验证，与把全部高分轨迹都用于 SFT，有何区别？ MASS 在固定权重搜索后独立采集轨迹，用成对比较形成 BT 排名，前 K−1 条训练，第 K 条用于验证。留出使训练与检查不完全使用同一批目标，但验证信号仍来自既定评价过程，不等于独立真实任务成功。不能将搜索时见过的全部好轨迹同时当训练和泛化证据。 教学例：排名前三条中取前两条训练、第三条验证；若第三条也参与梯度更新，验证损失就失去了原本的留出意义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c73c85ee811935d7">BT 排名中留出第 K 条轨迹验证，与把全部高分轨迹都用于 SFT，有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amass">Recursive Self-Improvement through Multi-Agent Self-Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MASS 在固定权重搜索后独立采集轨迹，用成对比较形成 BT 排名，前 K−1 条训练，第 K 条用于验证。留出使训练与检查不完全使用同一批目标，但验证信号仍来自既定评价过程，不等于独立真实任务成功。不能将搜索时见过的全部好轨迹同时当训练和泛化证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：排名前三条中取前两条训练、第三条验证；若第三条也参与梯度更新，验证损失就失去了原本的留出意义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12176">原论文</a> · <a href="../../../../agent-research/2610.12176-mass/">实现解读</a> · <a href="#qa-c73c85ee811935d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mass" data-paper-title="Recursive Self-Improvement through Multi-Agent Self-Supervision" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Recursive Self-Improvement through Multi-Agent Self-Supervision Agent UC Berkeley 2026-10-08 同一模型执行、提出工作流并成对评价。固定权重下搜索后，独立采集轨迹，以 Bradley–Terry 排名选择前 K−1 条训练、第 K 条验证；仅移除编排者初始工作流提示，保留工作者分工。助手 token 的 SFT 更新权重后再重复。原文 Qwen3.6-27B 两轮在研究任务中提高单位输出 token 表现约 1.2–1.6 倍，未报告线上 A/B。 本地指标：L1 GPU 诊断。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。真实共享 checkpoint 完成两轮搜索、裁判、轨迹采集与 LoRA SFT。本地为固定两工作者和一编排者的有界文本工作流族，可改变角色指令和传递内容；未接入任意工作流图、qwen-code 文件/终端工具，因此不是完整科研 coding-agent 复现。  递归自改进 工作流搜索 多智能体自监督 Agent 运行流程与自进化：改的是哪一层 本地两轮真实 LoRA 与验证损失下降可以证明什么？ 它证明共享 checkpoint 的执行、提案、排名和更新链实际运行，受限两 worker 文本工作流出现真实参数训练。数据是自生成轨迹且单 seed、短步数，没有任意工作流图或科研文件工具，不能据 loss 降低宣称独立科研能力提升。 例如第二轮更容易模仿自己生成的验证文本会让 loss 降低，却未测试未知研究任务最终结论是否正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3b165fac154d365c">本地两轮真实 LoRA 与验证损失下降可以证明什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amass">Recursive Self-Improvement through Multi-Agent Self-Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它证明共享 checkpoint 的执行、提案、排名和更新链实际运行，受限两 worker 文本工作流出现真实参数训练。数据是自生成轨迹且单 seed、短步数，没有任意工作流图或科研文件工具，不能据 loss 降低宣称独立科研能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第二轮更容易模仿自己生成的验证文本会让 loss 降低，却未测试未知研究任务最终结论是否正确。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12176">原论文</a> · <a href="../../../../agent-research/2610.12176-mass/">实现解读</a> · <a href="#qa-3b165fac154d365c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento3" data-paper-title="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks Agent University College London 2026-10-08 冻结 LLM 将黑盒交互证据写成可修改规则册，再编译为世界模型。新代码必须同时通过语义忠实性判断和全部历史逐格回放；规划失配会触发修复。多个模型共享历史，按不同完整计划的等价类均匀抽样，而非按重复模型投票。论文第 2 节 当前实现为 L1 核心机制实验，不是原论文完整基准。已在 NVIDIA A100-SXM4-80GB 上实际运行冻结 Qwen2.5-7B；生成模型在第一次真实动作后被证伪，修复未成功，最终没有可用世界模型，任务也未完成。这是一条保留失败的机制执行记录，不是能力提升结果。  世界模型 反思与记忆 Agent 运行流程与自进化：改的是哪一层 Memento 3 为什么要从黑盒交互中学习可供规划的环境规则？ 新环境不一定公开转移规律，Agent 只看到动作及其后果，直接凭语言猜计划容易反复犯错。Memento 3 将观察整理成规则册并编译成可执行模型，用历史和新行动检验，以便先在模型中规划。学到的是可修订假设，历史一致不保证未见状态也正确。 教学例：按下按钮后物体方向改变，Agent 先提出旋转规则，再用其他已见转移检查；新观察不符时应修规则，而非忽略反例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-memento3-dd7ada6c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ad1d7f6482680c52">Memento 3 为什么要从黑盒交互中学习可供规划的环境规则？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemento3">Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University College London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新环境不一定公开转移规律，Agent 只看到动作及其后果，直接凭语言猜计划容易反复犯错。Memento 3 将观察整理成规则册并编译成可执行模型，用历史和新行动检验，以便先在模型中规划。学到的是可修订假设，历史一致不保证未见状态也正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：按下按钮后物体方向改变，Agent 先提出旋转规则，再用其他已见转移检查；新观察不符时应修规则，而非忽略反例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11794">原论文</a> · <a href="../../../../agent-research/2610.11794-memento3/">实现解读</a> · <a href="#qa-ad1d7f6482680c52">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento3" data-paper-title="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks Agent University College London 2026-10-08 冻结 LLM 将黑盒交互证据写成可修改规则册，再编译为世界模型。新代码必须同时通过语义忠实性判断和全部历史逐格回放；规划失配会触发修复。多个模型共享历史，按不同完整计划的等价类均匀抽样，而非按重复模型投票。论文第 2 节 当前实现为 L1 核心机制实验，不是原论文完整基准。已在 NVIDIA A100-SXM4-80GB 上实际运行冻结 Qwen2.5-7B；生成模型在第一次真实动作后被证伪，修复未成功，最终没有可用世界模型，任务也未完成。这是一条保留失败的机制执行记录，不是能力提升结果。  世界模型 反思与记忆 Agent 运行流程与自进化：改的是哪一层 历史回放为什么不能每一步都用下一张真实观察重置模拟状态？ 逐步重置会掩盖世界模型误差的累积，使错误模型看似每步都符合历史。连续回放从初始观察仅初始化一次，后续状态全由模型转移产生，才检验规则册能否真正解释轨迹；语义忠实性也需另查，单纯拟合有限历史不等于通用正确。 例如模型第一步把门位置算错，若第二步直接塞回真实截图，错误就被擦掉；连续回放则会让偏差在后续观察中暴露。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento3" data-paper-title="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks Agent University College London 2026-10-08 冻结 LLM 将黑盒交互证据写成可修改规则册，再编译为世界模型。新代码必须同时通过语义忠实性判断和全部历史逐格回放；规划失配会触发修复。多个模型共享历史，按不同完整计划的等价类均匀抽样，而非按重复模型投票。论文第 2 节 当前实现为 L1 核心机制实验，不是原论文完整基准。已在 NVIDIA A100-SXM4-80GB 上实际运行冻结 Qwen2.5-7B；生成模型在第一次真实动作后被证伪，修复未成功，最终没有可用世界模型，任务也未完成。这是一条保留失败的机制执行记录，不是能力提升结果。  世界模型 反思与记忆 Agent 运行流程与自进化：改的是哪一层 按完整计划等价类均匀抽样，与按模型成员投票有什么不同？ 多个模型可能提出完全相同动作序列，按成员抽样会让重复计划获得额外概率；按非空完整序列分组后均匀抽类，强调行为多样性而非模型数量。选定计划保持到完成、失配或重规划，也不是每步重新随机切换路线。 例如三模型都提左左、一个提右上，按成员是三比一，按两种计划类则各一半，重复成员不会放大同一路线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c135d3f3afc9d094">按完整计划等价类均匀抽样，与按模型成员投票有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemento3">Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University College London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个模型可能提出完全相同动作序列，按成员抽样会让重复计划获得额外概率；按非空完整序列分组后均匀抽类，强调行为多样性而非模型数量。选定计划保持到完成、失配或重规划，也不是每步重新随机切换路线。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三模型都提左左、一个提右上，按成员是三比一，按两种计划类则各一半，重复成员不会放大同一路线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11794">原论文</a> · <a href="../../../../agent-research/2610.11794-memento3/">实现解读</a> · <a href="#qa-c135d3f3afc9d094">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento3" data-paper-title="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks Agent University College London 2026-10-08 冻结 LLM 将黑盒交互证据写成可修改规则册，再编译为世界模型。新代码必须同时通过语义忠实性判断和全部历史逐格回放；规划失配会触发修复。多个模型共享历史，按不同完整计划的等价类均匀抽样，而非按重复模型投票。论文第 2 节 当前实现为 L1 核心机制实验，不是原论文完整基准。已在 NVIDIA A100-SXM4-80GB 上实际运行冻结 Qwen2.5-7B；生成模型在第一次真实动作后被证伪，修复未成功，最终没有可用世界模型，任务也未完成。这是一条保留失败的机制执行记录，不是能力提升结果。  世界模型 反思与记忆 Agent 运行流程与自进化：改的是哪一层 新世界模型代码为什么要同时过语义忠实性检查和历史执行检查？ 代码可能能拟合部分观察，却没有表达当前规则册，也可能忠实实现了一份本就错误的规则。语义检查约束编译结果与规则一致，历史回放检查它能否重现已见转移，两者分别约束表达和行为。新真实动作失配仍会触发修复，GPU 执行记录不等于规则已经普遍正确。 教学例：规则册写顺时针旋转，代码却硬编码一张结果图；即使碰巧通过一个样例，也不能认为忠实实现了这条规则。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-66d5b7038bccdd48">新世界模型代码为什么要同时过语义忠实性检查和历史执行检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemento3">Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University College London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>代码可能能拟合部分观察，却没有表达当前规则册，也可能忠实实现了一份本就错误的规则。语义检查约束编译结果与规则一致，历史回放检查它能否重现已见转移，两者分别约束表达和行为。新真实动作失配仍会触发修复，GPU 执行记录不等于规则已经普遍正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：规则册写顺时针旋转，代码却硬编码一张结果图；即使碰巧通过一个样例，也不能认为忠实实现了这条规则。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11794">原论文</a> · <a href="../../../../agent-research/2610.11794-memento3/">实现解读</a> · <a href="#qa-66d5b7038bccdd48">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frugalevo" data-paper-title="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution Agent National University of Singapore 2026-10-02 FrugalEvo 把程序优化拆成高成本模型提出策略、低成本模型执行和改进代码，按预算内整条最佳成绩曲线评价搜索效率。先试跑多种策略再排序，失败时保留父程序追加反馈，取得改进后重新锚定，并用岛屿档案保存不同程序。 本地独立实现与公开任务小预算验证。不是原论文 API 模型、美元成本或完整 20 任务结果的复现；尚未接入统一 Evolve 控制器。共享前缀字节顺序已实现；当前 Transformers 后端没有跨请求 KV 前缀缓存，cached_input_tokens=0，不声称复现论文缓存加速。需要 Linux、可用的 bubblewrap/prlimit、CUDA 和预先下载的公开 checkpoint。生成程序在无网络、无工作区/凭据/模型缓存挂载的沙箱中运行；沙箱不能启动时拒绝执行，没有裸 exec 回退。  程序进化 成本约束 强弱模型协作 Agent 运行流程与自进化：改的是哪一层 FrugalEvo 为什么希望强模型的研究想法能由便宜模型反复落实？ 持续用强模型生成并执行所有搜索步骤成本高，而弱模型可能缺少有效策略。FrugalEvo 将较强的策略提案与较便宜的反复实现连接起来，在有限预算下寻找有效程序。需要评估整段搜索的实际成本和质量变化，不能只看最后最好分数或某次便宜调用。 教学例：强模型提出一种改进方向，弱模型围绕它尝试多次代码变体；若反复失败仍消耗大量预算，分工就未必划算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-frugalevo-468f3ba3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-68885a6d3cab967b">FrugalEvo 为什么希望强模型的研究想法能由便宜模型反复落实？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afrugalevo">FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>持续用强模型生成并执行所有搜索步骤成本高，而弱模型可能缺少有效策略。FrugalEvo 将较强的策略提案与较便宜的反复实现连接起来，在有限预算下寻找有效程序。需要评估整段搜索的实际成本和质量变化，不能只看最后最好分数或某次便宜调用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：强模型提出一种改进方向，弱模型围绕它尝试多次代码变体；若反复失败仍消耗大量预算，分工就未必划算。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03675">原论文</a> · <a href="../../../../agent-research/2610.03675-frugalevo/">实现解读</a> · <a href="#qa-68885a6d3cab967b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frugalevo" data-paper-title="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution Agent National University of Singapore 2026-10-02 FrugalEvo 把程序优化拆成高成本模型提出策略、低成本模型执行和改进代码，按预算内整条最佳成绩曲线评价搜索效率。先试跑多种策略再排序，失败时保留父程序追加反馈，取得改进后重新锚定，并用岛屿档案保存不同程序。 本地独立实现与公开任务小预算验证。不是原论文 API 模型、美元成本或完整 20 任务结果的复现；尚未接入统一 Evolve 控制器。共享前缀字节顺序已实现；当前 Transformers 后端没有跨请求 KV 前缀缓存，cached_input_tokens=0，不声称复现论文缓存加速。需要 Linux、可用的 bubblewrap/prlimit、CUDA 和预先下载的公开 checkpoint。生成程序在无网络、无工作区/凭据/模型缓存挂载的沙箱中运行；沙箱不能启动时拒绝执行，没有裸 exec 回退。  程序进化 成本约束 强弱模型协作 Agent 运行流程与自进化：改的是哪一层 为什么高成本模型提出策略后，还要由低成本模型反复执行，并评价整条最佳曲线？ 策略构思与局部代码迭代所需能力和费用不同，分层让昂贵调用集中在方向选择。失败时保留父程序追加反馈，改进后再锚定，岛屿档案保护多样性；整条预算内最佳曲线反映多快找到有用方案，而非只在最后挑一次幸运高分。 例如强模型提出向量化方向，小模型负责多个等价实现试验；同预算下更早得到可用加速，比最后一次偶然最好更稳定有意义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frugalevo" data-paper-title="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution Agent National University of Singapore 2026-10-02 FrugalEvo 把程序优化拆成高成本模型提出策略、低成本模型执行和改进代码，按预算内整条最佳成绩曲线评价搜索效率。先试跑多种策略再排序，失败时保留父程序追加反馈，取得改进后重新锚定，并用岛屿档案保存不同程序。 本地独立实现与公开任务小预算验证。不是原论文 API 模型、美元成本或完整 20 任务结果的复现；尚未接入统一 Evolve 控制器。共享前缀字节顺序已实现；当前 Transformers 后端没有跨请求 KV 前缀缓存，cached_input_tokens=0，不声称复现论文缓存加速。需要 Linux、可用的 bubblewrap/prlimit、CUDA 和预先下载的公开 checkpoint。生成程序在无网络、无工作区/凭据/模型缓存挂载的沙箱中运行；沙箱不能启动时拒绝执行，没有裸 exec 回退。  程序进化 成本约束 强弱模型协作 Agent 运行流程与自进化：改的是哪一层 高成本策略模型加低成本实现模型与纯弱模型搜索应怎样公平解释？ 二者从同一初始程序、相同预算与调用上限出发，仍可能因不同上限先触发而实际花费不等。较大模型也未必更强，需报告真实 token、策略试跑和细化；不能从分工名称推断协作必优，当前本地整体结果未支持该结论。 例如弱模型先达到三十次调用但预算未用完，协作花更多 token，必须写“相同上限”而非“相同实际成本”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b570190e7adc039e">高成本策略模型加低成本实现模型与纯弱模型搜索应怎样公平解释？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afrugalevo">FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>二者从同一初始程序、相同预算与调用上限出发，仍可能因不同上限先触发而实际花费不等。较大模型也未必更强，需报告真实 token、策略试跑和细化；不能从分工名称推断协作必优，当前本地整体结果未支持该结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如弱模型先达到三十次调用但预算未用完，协作花更多 token，必须写“相同上限”而非“相同实际成本”。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03675">原论文</a> · <a href="../../../../agent-research/2610.03675-frugalevo/">实现解读</a> · <a href="#qa-b570190e7adc039e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:frugalevo" data-paper-title="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution Agent National University of Singapore 2026-10-02 FrugalEvo 把程序优化拆成高成本模型提出策略、低成本模型执行和改进代码，按预算内整条最佳成绩曲线评价搜索效率。先试跑多种策略再排序，失败时保留父程序追加反馈，取得改进后重新锚定，并用岛屿档案保存不同程序。 本地独立实现与公开任务小预算验证。不是原论文 API 模型、美元成本或完整 20 任务结果的复现；尚未接入统一 Evolve 控制器。共享前缀字节顺序已实现；当前 Transformers 后端没有跨请求 KV 前缀缓存，cached_input_tokens=0，不声称复现论文缓存加速。需要 Linux、可用的 bubblewrap/prlimit、CUDA 和预先下载的公开 checkpoint。生成程序在无网络、无工作区/凭据/模型缓存挂载的沙箱中运行；沙箱不能启动时拒绝执行，没有裸 exec 回退。  程序进化 成本约束 强弱模型协作 Agent 运行流程与自进化：改的是哪一层 生成程序失败时为何保留父程序且必须拒绝裸 exec 回退？ 失败反馈用于下一次修订，已验证父本不应被无效代码替换；实际生成代码需 Linux 隔离和资源限制，沙箱启动失败就拒绝。模型自报分不采信，可信检查器验证边界与不重叠；本地负结果也不能靠删失败调用或改安全边界修饰。 例如程序输出非法半径应计失败和调用成本，不能用父本答案回填成候选成功，也不能因 sandbox 不可用直接在宿主执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e1f4b7fda8831b85">生成程序失败时为何保留父程序且必须拒绝裸 exec 回退？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afrugalevo">FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>失败反馈用于下一次修订，已验证父本不应被无效代码替换；实际生成代码需 Linux 隔离和资源限制，沙箱启动失败就拒绝。模型自报分不采信，可信检查器验证边界与不重叠；本地负结果也不能靠删失败调用或改安全边界修饰。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如程序输出非法半径应计失败和调用成本，不能用父本答案回填成候选成功，也不能因 sandbox 不可用直接在宿主执行。</p>
<p class="ar-learning-sources">依据：公式与原文结果、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03675">原论文</a> · <a href="../../../../agent-research/2610.03675-frugalevo/">实现解读</a> · <a href="#qa-e1f4b7fda8831b85">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seer-forecasting" data-paper-title="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting Agent Google Cloud AI Research / University of Virginia 2026-10-02 数值历史可能缺少外部事件信息，普通 RAG 又不会从预测错误中修订检索方法。SEER 保持预测模型权重不变，把上下文拆成检索记忆、筛选记忆和因果知识。只有过去结果真正可见后，才从预测轨迹中分别更新两类记忆与知识；容量不足时压缩，而不是无限追加。图按原文 Figure 2 与 §3 重绘。原图及方法。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。完整协议涉及 Gemini 3.1 Pro/Flash、Claude 4.6 Sonnet/4.8 Opus，多轮搜索、LEAF 事实核验与顺序回测（§4.1）。闭源调用与六领域完整成本无法用廉价只读检查可靠固定；成本过高，不复现（审查 DONE）。  自进化与经验复用 时间约束事件检索与预测 Agent 运行流程与自进化：改的是哪一层 SEER 为什么在数值时间序列之外，还要关注可获取的外部事件？ 价格、需求等序列可能受新闻或政策影响，仅看历史数值难解释这些外部变化。SEER 研究检索相关事件并从过去预测经验中改进筛选与知识，而保持预测模型权重固定。额外文本也会带来噪声和前视风险，必须核对预测时真正可获得的信息。 教学例：需求突变可能与已公布的节假日安排有关；事后才发布的销售总结不能回填给更早的预测，哪怕它解释得很清楚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-seer-forecasting-fb9c59fb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9e21ec395e7e0fe8">SEER 为什么在数值时间序列之外，还要关注可获取的外部事件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aseer-forecasting">SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>价格、需求等序列可能受新闻或政策影响，仅看历史数值难解释这些外部变化。SEER 研究检索相关事件并从过去预测经验中改进筛选与知识，而保持预测模型权重固定。额外文本也会带来噪声和前视风险，必须核对预测时真正可获得的信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：需求突变可能与已公布的节假日安排有关；事后才发布的销售总结不能回填给更早的预测，哪怕它解释得很清楚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.04109v1">原论文</a> · <a href="../../../../agent-research/2610.04109-seer-forecasting/">实现解读</a> · <a href="#qa-9e21ec395e7e0fe8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seer-forecasting" data-paper-title="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting Agent Google Cloud AI Research / University of Virginia 2026-10-02 数值历史可能缺少外部事件信息，普通 RAG 又不会从预测错误中修订检索方法。SEER 保持预测模型权重不变，把上下文拆成检索记忆、筛选记忆和因果知识。只有过去结果真正可见后，才从预测轨迹中分别更新两类记忆与知识；容量不足时压缩，而不是无限追加。图按原文 Figure 2 与 §3 重绘。原图及方法。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。完整协议涉及 Gemini 3.1 Pro/Flash、Claude 4.6 Sonnet/4.8 Opus，多轮搜索、LEAF 事实核验与顺序回测（§4.1）。闭源调用与六领域完整成本无法用廉价只读检查可靠固定；成本过高，不复现（审查 DONE）。  自进化与经验复用 时间约束事件检索与预测 Agent 运行流程与自进化：改的是哪一层 为什么预测结果成熟后才能反思，测试窗口还必须冻结记忆与因果知识？ 未来真值在预测时不可见，提前用它更新检索或筛选会泄漏结果；测试期间继续按测试误差改记忆，也会把报告集变成训练反馈。分开检索记忆、筛选记忆和知识有助定位错误来源，但事件时间与实际可获得时间仍须独立核对。 例如预测下周销量时，周末才公布的新闻不能回填周一输入；测试结束后知道的销量也不能用于重写同一测试的检索策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seer-forecasting" data-paper-title="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting Agent Google Cloud AI Research / University of Virginia 2026-10-02 数值历史可能缺少外部事件信息，普通 RAG 又不会从预测错误中修订检索方法。SEER 保持预测模型权重不变，把上下文拆成检索记忆、筛选记忆和因果知识。只有过去结果真正可见后，才从预测轨迹中分别更新两类记忆与知识；容量不足时压缩，而不是无限追加。图按原文 Figure 2 与 §3 重绘。原图及方法。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。完整协议涉及 Gemini 3.1 Pro/Flash、Claude 4.6 Sonnet/4.8 Opus，多轮搜索、LEAF 事实核验与顺序回测（§4.1）。闭源调用与六领域完整成本无法用廉价只读检查可靠固定；成本过高，不复现（审查 DONE）。  自进化与经验复用 时间约束事件检索与预测 Agent 运行流程与自进化：改的是哪一层 固定预测模型而更新检索与筛选经验，和直接 finetune 权重有什么不同？ 前者改变外部证据如何扩展、过滤及组织，预测器权重保持相同，便于研究上下文演化；finetune 改变模型内部映射。两条记忆和知识各有作用，不能把手写因果规则或更新查询模板自动解释成模型学会新的数值动力学。 例如检索记忆提醒查节假日事件，筛选记忆排除无关新闻，但时间序列模型本身参数仍未变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4d45948e73d7437d">固定预测模型而更新检索与筛选经验，和直接 finetune 权重有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aseer-forecasting">SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者改变外部证据如何扩展、过滤及组织，预测器权重保持相同，便于研究上下文演化；finetune 改变模型内部映射。两条记忆和知识各有作用，不能把手写因果规则或更新查询模板自动解释成模型学会新的数值动力学。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如检索记忆提醒查节假日事件，筛选记忆排除无关新闻，但时间序列模型本身参数仍未变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.04109v1">原论文</a> · <a href="../../../../agent-research/2610.04109-seer-forecasting/">实现解读</a> · <a href="#qa-4d45948e73d7437d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:seer-forecasting" data-paper-title="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting Agent Google Cloud AI Research / University of Virginia 2026-10-02 数值历史可能缺少外部事件信息，普通 RAG 又不会从预测错误中修订检索方法。SEER 保持预测模型权重不变，把上下文拆成检索记忆、筛选记忆和因果知识。只有过去结果真正可见后，才从预测轨迹中分别更新两类记忆与知识；容量不足时压缩，而不是无限追加。图按原文 Figure 2 与 §3 重绘。原图及方法。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。完整协议涉及 Gemini 3.1 Pro/Flash、Claude 4.6 Sonnet/4.8 Opus，多轮搜索、LEAF 事实核验与顺序回测（§4.1）。闭源调用与六领域完整成本无法用廉价只读检查可靠固定；成本过高，不复现（审查 DONE）。  自进化与经验复用 时间约束事件检索与预测 Agent 运行流程与自进化：改的是哪一层 事件发生时间与可获得时间，怎样共同限制预测侧可读的文本？ 一条事件可能早已发生，但相关报道或数据库记录到更晚才公开；预测输入必须同时符合目标时间与信息可获得边界。仅看新闻标注日期不够，还要核查当时能否取得其内容。记忆容量不足时可压缩，但压缩不能把未来结论混进过去上下文，测试阶段也不得继续反思。 教学例：周一发生的事件周三才披露，周二预测不应使用周三报道；把报道标题改成周一日期仍不能改变可获得时间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-96a96332cee84000">事件发生时间与可获得时间，怎样共同限制预测侧可读的文本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aseer-forecasting">SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一条事件可能早已发生，但相关报道或数据库记录到更晚才公开；预测输入必须同时符合目标时间与信息可获得边界。仅看新闻标注日期不够，还要核查当时能否取得其内容。记忆容量不足时可压缩，但压缩不能把未来结论混进过去上下文，测试阶段也不得继续反思。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：周一发生的事件周三才披露，周二预测不应使用周三报道；把报道标题改成周一日期仍不能改变可获得时间。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与成本判断；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.04109v1">原论文</a> · <a href="../../../../agent-research/2610.04109-seer-forecasting/">实现解读</a> · <a href="#qa-96a96332cee84000">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sentry" data-paper-title="Sentry: Learning to Recover from LLM Agent Failures at Test Time" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Sentry: Learning to Recover from LLM Agent Failures at Test Time Agent Stanford University 2026-10-02 Sentry 不把所有失败经验长期塞进 Agent 上下文，而是先识别当前行为失败，再按类别和标签检索相关恢复建议。外部验证器只看后续可观察进展、不看任务奖励，确认恢复后才把经验写入 playbook；动作格式错误走单独的硬修复路径。 未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。独立控制器与真实 checkpoint 的小预算工具任务验证；未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。数据使用 HotpotQA 官方 Hugging Face 镜像的 validation parquet。脚本校验固定 SHA-256，并按题目 ID 哈希排序；前 4 题建立记忆，之后 16 题保留给接口开发，再后 8 题作隔离对照。它们均来自官方 dev，不是官方 test。  失败恢复 条件记忆 测试时学习 Agent 运行流程与自进化：改的是哪一层 Sentry 为什么专门处理 Agent 运行中的卡住、重复与格式错误？ 长程 Agent 不一定因缺知识失败，也可能陷入循环、重复无效动作或发出不合法调用。Sentry 研究在运行时识别这些故障并给恢复支持，使已有经验服务当前阻塞。恢复只是局部继续行动，不能直接等同于最终答对；真实本地对照还出现了负结果。 教学例：Agent 连续重复同一无效搜索，检测后可尝试相关恢复建议；即使之后开始读新页面，也仍要检查最终答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-sentry-acd21bdd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-495464cea2ff924e">Sentry 为什么专门处理 Agent 运行中的卡住、重复与格式错误？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asentry">Sentry: Learning to Recover from LLM Agent Failures at Test Time</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长程 Agent 不一定因缺知识失败，也可能陷入循环、重复无效动作或发出不合法调用。Sentry 研究在运行时识别这些故障并给恢复支持，使已有经验服务当前阻塞。恢复只是局部继续行动，不能直接等同于最终答对；真实本地对照还出现了负结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：Agent 连续重复同一无效搜索，检测后可尝试相关恢复建议；即使之后开始读新页面，也仍要检查最终答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02994">原论文</a> · <a href="../../../../agent-research/2610.02994-sentry/">实现解读</a> · <a href="#qa-495464cea2ff924e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sentry" data-paper-title="Sentry: Learning to Recover from LLM Agent Failures at Test Time" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Sentry: Learning to Recover from LLM Agent Failures at Test Time Agent Stanford University 2026-10-02 Sentry 不把所有失败经验长期塞进 Agent 上下文，而是先识别当前行为失败，再按类别和标签检索相关恢复建议。外部验证器只看后续可观察进展、不看任务奖励，确认恢复后才把经验写入 playbook；动作格式错误走单独的硬修复路径。 未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。独立控制器与真实 checkpoint 的小预算工具任务验证；未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。数据使用 HotpotQA 官方 Hugging Face 镜像的 validation parquet。脚本校验固定 SHA-256，并按题目 ID 哈希排序；前 4 题建立记忆，之后 16 题保留给接口开发，再后 8 题作隔离对照。它们均来自官方 dev，不是官方 test。  失败恢复 条件记忆 测试时学习 Agent 运行流程与自进化：改的是哪一层 恢复建议为什么只有经后续可观察进展验证后才写入 playbook？ 失败后提出建议只是猜测，若直接永久保存，错误补救会成为新污染。外部验证器看后续行为是否真正恢复，不读取任务奖励来给行动者答案，再按失败类别检索适用经验；格式错误另走硬修复路径，避免把机械纠错与语义恢复混成一类能力。 例如建议“刷新登录”后若仍循环报错就不应入库；只有观察到继续完成后续步骤，才形成可供相似失败复用的证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sentry" data-paper-title="Sentry: Learning to Recover from LLM Agent Failures at Test Time" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Sentry: Learning to Recover from LLM Agent Failures at Test Time Agent Stanford University 2026-10-02 Sentry 不把所有失败经验长期塞进 Agent 上下文，而是先识别当前行为失败，再按类别和标签检索相关恢复建议。外部验证器只看后续可观察进展、不看任务奖励，确认恢复后才把经验写入 playbook；动作格式错误走单独的硬修复路径。 未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。独立控制器与真实 checkpoint 的小预算工具任务验证；未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。数据使用 HotpotQA 官方 Hugging Face 镜像的 validation parquet。脚本校验固定 SHA-256，并按题目 ID 哈希排序；前 4 题建立记忆，之后 16 题保留给接口开发，再后 8 题作隔离对照。它们均来自官方 dev，不是官方 test。  失败恢复 条件记忆 测试时学习 Agent 运行流程与自进化：改的是哪一层 按失败类别检索恢复建议，与把全部经验常驻上下文，有何信息取舍？ 条件检索只在检测到相应失败时提供相关类别和标签的经验，减少正常执行时的额外输入；常驻全部经验无需等待触发，却更容易加入无关建议。条件方式依赖检测和匹配是否可靠，漏检会错过帮助，误检也可能打断正常策略，不能由上下文减少直接推出成功提升。 教学例：网络超时后检索连接恢复经验，比每一步都携带所有格式与循环修复指南更聚焦；若把正常等待误判超时，干预仍会有害。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f2eab53b675d142d">按失败类别检索恢复建议，与把全部经验常驻上下文，有何信息取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asentry">Sentry: Learning to Recover from LLM Agent Failures at Test Time</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>条件检索只在检测到相应失败时提供相关类别和标签的经验，减少正常执行时的额外输入；常驻全部经验无需等待触发，却更容易加入无关建议。条件方式依赖检测和匹配是否可靠，漏检会错过帮助，误检也可能打断正常策略，不能由上下文减少直接推出成功提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：网络超时后检索连接恢复经验，比每一步都携带所有格式与循环修复指南更聚焦；若把正常等待误判超时，干预仍会有害。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02994">原论文</a> · <a href="../../../../agent-research/2610.02994-sentry/">实现解读</a> · <a href="#qa-f2eab53b675d142d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sentry" data-paper-title="Sentry: Learning to Recover from LLM Agent Failures at Test Time" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Sentry: Learning to Recover from LLM Agent Failures at Test Time Agent Stanford University 2026-10-02 Sentry 不把所有失败经验长期塞进 Agent 上下文，而是先识别当前行为失败，再按类别和标签检索相关恢复建议。外部验证器只看后续可观察进展、不看任务奖励，确认恢复后才把经验写入 playbook；动作格式错误走单独的硬修复路径。 未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。独立控制器与真实 checkpoint 的小预算工具任务验证；未复现原文四套环境，不宣称 WebShop、AppWorld、SWE-bench 或 Mind2Web 成绩。数据使用 HotpotQA 官方 Hugging Face 镜像的 validation parquet。脚本校验固定 SHA-256，并按题目 ID 哈希排序；前 4 题建立记忆，之后 16 题保留给接口开发，再后 8 题作隔离对照。它们均来自官方 dev，不是官方 test。  失败恢复 条件记忆 测试时学习 Agent 运行流程与自进化：改的是哪一层 本地三 seed HotpotQA 结果为什么不能改成提升或二十四个独立任务？ 三个生成 seed 重复同八题，均值低于基线，额外管理器和验证调用还增加成本；这是负结果。记忆建立后冻结，隔离题不用于重调 detector，官方 validation 派生留出也非官方 test，不能以挑一个 seed 的正差覆盖整体下降。 例如 seed43 多答对一题，但其他两个更差，报告全部配对结果才能看到不稳定，不能只宣传最好一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fc327101cfc3f1ce">本地三 seed HotpotQA 结果为什么不能改成提升或二十四个独立任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asentry">Sentry: Learning to Recover from LLM Agent Failures at Test Time</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>三个生成 seed 重复同八题，均值低于基线，额外管理器和验证调用还增加成本；这是负结果。记忆建立后冻结，隔离题不用于重调 detector，官方 validation 派生留出也非官方 test，不能以挑一个 seed 的正差覆盖整体下降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 seed43 多答对一题，但其他两个更差，报告全部配对结果才能看到不稳定，不能只宣传最好一次。</p>
<p class="ar-learning-sources">依据：核心规则与原文结果、本地复现、复现边界与失败记录；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02994">原论文</a> · <a href="../../../../agent-research/2610.02994-sentry/">实现解读</a> · <a href="#qa-fc327101cfc3f1ce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:active-saddler" data-paper-title="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization Agent POSTECH 2026-10-01 把反复出现的失败模式动态实例化为非平稳 bandit arm；课程控制器在发现新场景和重访已知弱点之间选择，并随 harness 修复结果更新优先级。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Harness 优化 主动课程 RSI Agent 运行流程与自进化：改的是哪一层 有限修复预算下，ActiveSaddler 为什么需要选择下一批该暴露哪类失败？ harness 不可能对所有场景同时做同等深入修复，反复只测熟悉问题又会漏掉新弱点。ActiveSaddler 把训练课程当作动态决策，利用已有失败和修复反馈安排后续任务。选中困难场景只提供学习机会，不表示修复已实现，也不能把调度计数当成真实能力增长。 教学例：文件编辑故障已多次修好，浏览恢复问题刚出现；课程需要决定继续验证旧问题还是拿预算探索这个新故障。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-active-saddler-9c3dd285" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-eb7aff962dad76a3">有限修复预算下，ActiveSaddler 为什么需要选择下一批该暴露哪类失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aactive-saddler">ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · POSTECH</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>harness 不可能对所有场景同时做同等深入修复，反复只测熟悉问题又会漏掉新弱点。ActiveSaddler 把训练课程当作动态决策，利用已有失败和修复反馈安排后续任务。选中困难场景只提供学习机会，不表示修复已实现，也不能把调度计数当成真实能力增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：文件编辑故障已多次修好，浏览恢复问题刚出现；课程需要决定继续验证旧问题还是拿预算探索这个新故障。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00906">原论文</a> · <a href="../../../../agent-research/2610.00906-active-saddler/">实现解读</a> · <a href="#qa-eb7aff962dad76a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:active-saddler" data-paper-title="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization Agent POSTECH 2026-10-01 把反复出现的失败模式动态实例化为非平稳 bandit arm；课程控制器在发现新场景和重访已知弱点之间选择，并随 harness 修复结果更新优先级。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Harness 优化 主动课程 RSI Agent 运行流程与自进化：改的是哪一层 失败模式作为非平稳 bandit arm，为什么必须允许发现新场景并重访旧弱点？ harness 修复后旧失败的收益会变化，固定课程可能不断测试已经解决的问题，又漏掉新暴露的缺陷。控制器用价值与探索项安排预算，周期性引入未见场景，保持发现和验证两种需求；次数或优先级只是课程信号，不能当模型能力指标。 例如超时问题已修好后应降低重复练习，但仍偶尔复测防回退，同时探索此前没有覆盖的权限错误场景。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:active-saddler" data-paper-title="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization Agent POSTECH 2026-10-01 把反复出现的失败模式动态实例化为非平稳 bandit arm；课程控制器在发现新场景和重访已知弱点之间选择，并随 harness 修复结果更新优先级。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Harness 优化 主动课程 RSI Agent 运行流程与自进化：改的是哪一层 固定难题采样与修复后动态调整失败优先级，面对的回报是否平稳？ 固定采样通常沿用预先设定的难度或频率，而修复会改变旧失败模式的价值：曾经常错的场景可能不再值得反复投入，新缺陷又可能出现。动态调度要跟随这种非平稳反馈更新，不能把历史失败率永久当作当前收益，也不保证每次再访都有新信息。 教学例：解析器问题修好后，原难例已连续通过，继续占满课程会浪费预算；新发现的认证问题可能更值得安排。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a4c5ad7e44c1c3e3">固定难题采样与修复后动态调整失败优先级，面对的回报是否平稳？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aactive-saddler">ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · POSTECH</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定采样通常沿用预先设定的难度或频率，而修复会改变旧失败模式的价值：曾经常错的场景可能不再值得反复投入，新缺陷又可能出现。动态调度要跟随这种非平稳反馈更新，不能把历史失败率永久当作当前收益，也不保证每次再访都有新信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：解析器问题修好后，原难例已连续通过，继续占满课程会浪费预算；新发现的认证问题可能更值得安排。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00906">原论文</a> · <a href="../../../../agent-research/2610.00906-active-saddler/">实现解读</a> · <a href="#qa-a4c5ad7e44c1c3e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:active-saddler" data-paper-title="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization Agent POSTECH 2026-10-01 把反复出现的失败模式动态实例化为非平稳 bandit arm；课程控制器在发现新场景和重访已知弱点之间选择，并随 harness 修复结果更新优先级。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Harness 优化 主动课程 RSI Agent 运行流程与自进化：改的是哪一层 本地动态 arm 调度是否包括 AutoSaddler 的真实修复链？ 不包括。本地只执行失败 arm 创建、探索利用和优先级更新，没有调用 AutoSaddler 或真实 GAIA2、Terminal-Bench。观察次数和选择权重验证调度规则，不能用合成反馈声称 harness 已被修好，真实 rollout 成本也仍须另计。 例如人为降低某 arm 收益后选择次数减少，说明控制器响应变化；它没有证明任何实际工具失败被解决。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-49be3a394da7a5ca">本地动态 arm 调度是否包括 AutoSaddler 的真实修复链？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aactive-saddler">ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · POSTECH</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不包括。本地只执行失败 arm 创建、探索利用和优先级更新，没有调用 AutoSaddler 或真实 GAIA2、Terminal-Bench。观察次数和选择权重验证调度规则，不能用合成反馈声称 harness 已被修好，真实 rollout 成本也仍须另计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人为降低某 arm 收益后选择次数减少，说明控制器响应变化；它没有证明任何实际工具失败被解决。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00906">原论文</a> · <a href="../../../../agent-research/2610.00906-active-saddler/">实现解读</a> · <a href="#qa-49be3a394da7a5ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:flowright" data-paper-title="It Takes Workflows to Evolve Better Workflows" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="It Takes Workflows to Evolve Better Workflows Agent William &amp; Mary 2026-10-01 利用 workflow 拓扑把稀疏结果拆为层级、结构感知的 role credit，使单角色自进化、上下游协同或多 Agent co-evolution 可共用一个 harness。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  工作流进化 多 Agent 层级奖励 Agent 运行流程与自进化：改的是哪一层 多 Agent 工作流只在末尾得到结果时，为什么很难知道该改进哪个角色？ 终局成败由多个角色及其依赖共同形成，把同一奖励发给所有人会掩盖谁真正推动或阻碍了流程。FlowRight 研究利用工作流结构组织角色信用，支持不同范围的协同改进。结构权重是一种归因规则，不是每个角色真实因果贡献的直接测量。 教学例：检索者找到证据，写作者却误读结论；若只给所有角色同一失败分数，后续更新可能连有效检索习惯也一起改坏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-flowright-b0c3085e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-769d988dd4262bbd">多 Agent 工作流只在末尾得到结果时，为什么很难知道该改进哪个角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aflowright">It Takes Workflows to Evolve Better Workflows</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · William &amp; Mary</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局成败由多个角色及其依赖共同形成，把同一奖励发给所有人会掩盖谁真正推动或阻碍了流程。FlowRight 研究利用工作流结构组织角色信用，支持不同范围的协同改进。结构权重是一种归因规则，不是每个角色真实因果贡献的直接测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：检索者找到证据，写作者却误读结论；若只给所有角色同一失败分数，后续更新可能连有效检索习惯也一起改坏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01026">原论文</a> · <a href="../../../../agent-research/2610.01026-flowright/">实现解读</a> · <a href="#qa-769d988dd4262bbd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:flowright" data-paper-title="It Takes Workflows to Evolve Better Workflows" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="It Takes Workflows to Evolve Better Workflows Agent William &amp; Mary 2026-10-01 利用 workflow 拓扑把稀疏结果拆为层级、结构感知的 role credit，使单角色自进化、上下游协同或多 Agent co-evolution 可共用一个 harness。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  工作流进化 多 Agent 层级奖励 Agent 运行流程与自进化：改的是哪一层 为什么结构感知 role credit 要看 workflow 拓扑，而不是把终局回报平均给所有角色？ 不同角色的位置与下游影响不同，平均分配掩盖了某个无效节点或关键上游。拓扑权重把有效性和后继关系纳入分配，使单角色改进与上下游协同共享控制框架；这种分摊仍是信用规则，不等于已识别各角色的真实因果贡献，须用执行对照检验。 例如检索者的错误传给三个下游，修复它可能比润色末段更重要；拓扑能提示这种传播范围，而非按人数平分奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:flowright" data-paper-title="It Takes Workflows to Evolve Better Workflows" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="It Takes Workflows to Evolve Better Workflows Agent William &amp; Mary 2026-10-01 利用 workflow 拓扑把稀疏结果拆为层级、结构感知的 role credit，使单角色自进化、上下游协同或多 Agent co-evolution 可共用一个 harness。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  工作流进化 多 Agent 层级奖励 Agent 运行流程与自进化：改的是哪一层 单角色自进化、上下游协同与多角色共同进化，各改变哪些参与者？ 单角色更新把其他参与者固定，便于观察局部变化；上下游协同关注依赖接口，多个角色共同变化则可调整整体配合，但更难区分收益来源。FlowRight 用统一工作流和信用表达支持这些范围，不能把某一范围有效直接推为所有联合更新都有效。 教学例：只改写作者与同时改检索者和写作者，可能需要不同验证；后者也许适配了新证据格式，不能只归功于写作能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1e685b943960b7cf">单角色自进化、上下游协同与多角色共同进化，各改变哪些参与者？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aflowright">It Takes Workflows to Evolve Better Workflows</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · William &amp; Mary</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单角色更新把其他参与者固定，便于观察局部变化；上下游协同关注依赖接口，多个角色共同变化则可调整整体配合，但更难区分收益来源。FlowRight 用统一工作流和信用表达支持这些范围，不能把某一范围有效直接推为所有联合更新都有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：只改写作者与同时改检索者和写作者，可能需要不同验证；后者也许适配了新证据格式，不能只归功于写作能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01026">原论文</a> · <a href="../../../../agent-research/2610.01026-flowright/">实现解读</a> · <a href="#qa-1e685b943960b7cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:flowright" data-paper-title="It Takes Workflows to Evolve Better Workflows" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="It Takes Workflows to Evolve Better Workflows Agent William &amp; Mary 2026-10-01 利用 workflow 拓扑把稀疏结果拆为层级、结构感知的 role credit，使单角色自进化、上下游协同或多 Agent co-evolution 可共用一个 harness。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  工作流进化 多 Agent 层级奖励 Agent 运行流程与自进化：改的是哪一层 valid_i(1+children_i) 的实现需要核对什么，本地没有完成什么？ 应让无效角色权重为零，并按全部有效权重归一化，检查信用守恒及无有效项边界。当前本地只执行这个分配算子，不生成 workflow、不训练 Qwen3.5 或运行 DataWright；结构统计通过不能当多 Agent 共同进化能力提升。 例如一个无效节点有十个孩子也不应因拓扑大获得信用；若所有节点无效，要显式处理而不是除以零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d5eae1a0fd5db0e8">valid_i(1+children_i) 的实现需要核对什么，本地没有完成什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aflowright">It Takes Workflows to Evolve Better Workflows</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · William &amp; Mary</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应让无效角色权重为零，并按全部有效权重归一化，检查信用守恒及无有效项边界。当前本地只执行这个分配算子，不生成 workflow、不训练 Qwen3.5 或运行 DataWright；结构统计通过不能当多 Agent 共同进化能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个无效节点有十个孩子也不应因拓扑大获得信用；若所有节点无效，要显式处理而不是除以零。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01026">原论文</a> · <a href="../../../../agent-research/2610.01026-flowright/">实现解读</a> · <a href="#qa-d5eae1a0fd5db0e8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rule-evolve" data-paper-title="Self-Evolving Coding Rules for AI Coding Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Evolving Coding Rules for AI Coding Agents Agent 原文首页未列第一作者机构 2026-09-30 维护 coding rule 候选池，由 mutator 生成变体，再只用隔离 validation evaluator 选择并回写更优规则。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选变异后的 validation 选择；不调用 LLM mutator。执行候选变异后的 validation 选择；不调用 LLM mutator。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RSI Coding Agent 规则进化 Agent 运行流程与自进化：改的是哪一层 RuleEvolve 为什么把 coding rule 当作可以检验和迭代的开发经验？ 编码 Agent 的工作规则会影响反复发生的定位、编辑和测试行为，手写一句建议未必适合当前任务分布。RuleEvolve 研究从规则变体中选择有实际证据的版本，使经验能持续修订。规则文字更详细不代表执行更好，选择还需隔离验证，不能依生成者自信直接回写。 教学例：新增“修改前先查调用点”的规则后，要看是否在相同开发任务上帮助修复，而不只评判这句话听起来是否合理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-rule-evolve-f1ced1e2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-846804b9a08fcd6a">RuleEvolve 为什么把 coding rule 当作可以检验和迭代的开发经验？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arule-evolve">Self-Evolving Coding Rules for AI Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>编码 Agent 的工作规则会影响反复发生的定位、编辑和测试行为，手写一句建议未必适合当前任务分布。RuleEvolve 研究从规则变体中选择有实际证据的版本，使经验能持续修订。规则文字更详细不代表执行更好，选择还需隔离验证，不能依生成者自信直接回写。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：新增“修改前先查调用点”的规则后，要看是否在相同开发任务上帮助修复，而不只评判这句话听起来是否合理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00650">原论文</a> · <a href="../../../../agent-research/2610.00650-rule-evolve/">实现解读</a> · <a href="#qa-846804b9a08fcd6a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rule-evolve" data-paper-title="Self-Evolving Coding Rules for AI Coding Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Evolving Coding Rules for AI Coding Agents Agent 原文首页未列第一作者机构 2026-09-30 维护 coding rule 候选池，由 mutator 生成变体，再只用隔离 validation evaluator 选择并回写更优规则。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选变异后的 validation 选择；不调用 LLM mutator。执行候选变异后的 validation 选择；不调用 LLM mutator。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RSI Coding Agent 规则进化 Agent 运行流程与自进化：改的是哪一层 为什么 mutator 生成的 coding rule 不能依据生成者自评直接回写？ 规则看似合理可能只适合少数样例，甚至损害旧行为。隔离 validation evaluator 对候选池和变体统一测量，再选择回写，把提议与接纳的依据分开；用于选择的数据也已属于开发反馈，最终测试不能继续交给 mutator 反复调整。 例如新规则要求所有函数都重试，文字上强调鲁棒性，却可能让非幂等调用重复执行；独立验证才能发现这种退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rule-evolve" data-paper-title="Self-Evolving Coding Rules for AI Coding Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Evolving Coding Rules for AI Coding Agents Agent 原文首页未列第一作者机构 2026-09-30 维护 coding rule 候选池，由 mutator 生成变体，再只用隔离 validation evaluator 选择并回写更优规则。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选变异后的 validation 选择；不调用 LLM mutator。执行候选变异后的 validation 选择；不调用 LLM mutator。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RSI Coding Agent 规则进化 Agent 运行流程与自进化：改的是哪一层 维护规则候选池与每次立刻覆盖唯一规则，在搜索和回退上有何区别？ 候选池让多个版本在相同评价口径下竞争，旧规则可作为比较和保留对象；立即覆盖把提案直接变成运行状态，失败后可能丢掉可用基线。候选池并不自动提供正确裁判，仍需隔离 evaluator，且不能用候选数量替代真实工具任务效果。 教学例：一条新规则更重视搜索、另一条更重视测试，可先保留两者比较；若每次生成即覆盖，就难区分是哪次修改造成退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5c0648898c9a12dc">维护规则候选池与每次立刻覆盖唯一规则，在搜索和回退上有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arule-evolve">Self-Evolving Coding Rules for AI Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选池让多个版本在相同评价口径下竞争，旧规则可作为比较和保留对象；立即覆盖把提案直接变成运行状态，失败后可能丢掉可用基线。候选池并不自动提供正确裁判，仍需隔离 evaluator，且不能用候选数量替代真实工具任务效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一条新规则更重视搜索、另一条更重视测试，可先保留两者比较；若每次生成即覆盖，就难区分是哪次修改造成退化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00650">原论文</a> · <a href="../../../../agent-research/2610.00650-rule-evolve/">实现解读</a> · <a href="#qa-5c0648898c9a12dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rule-evolve" data-paper-title="Self-Evolving Coding Rules for AI Coding Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Evolving Coding Rules for AI Coding Agents Agent 原文首页未列第一作者机构 2026-09-30 维护 coding rule 候选池，由 mutator 生成变体，再只用隔离 validation evaluator 选择并回写更优规则。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选变异后的 validation 选择；不调用 LLM mutator。执行候选变异后的 validation 选择；不调用 LLM mutator。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RSI Coding Agent 规则进化 Agent 运行流程与自进化：改的是哪一层 本地 mutation 后选择能否称为 LLM 规则进化已运行？ 不能。本地仅验证候选变异后的 validation 选择，不调用 LLM mutator 或完整 Coding Agent。argmax 在给定真实分数上正确是控制流证据，若分数来自 fixture 就不能解释为代码质量；旧规则和失败候选也应保留审计。 例如三个预设候选分数中选最大，只证明选择器；没有模型提出规则、实际修代码，就未验证整条自进化路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0dd59670d06cd928">本地 mutation 后选择能否称为 LLM 规则进化已运行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arule-evolve">Self-Evolving Coding Rules for AI Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地仅验证候选变异后的 validation 选择，不调用 LLM mutator 或完整 Coding Agent。argmax 在给定真实分数上正确是控制流证据，若分数来自 fixture 就不能解释为代码质量；旧规则和失败候选也应保留审计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三个预设候选分数中选最大，只证明选择器；没有模型提出规则、实际修代码，就未验证整条自进化路径。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00650">原论文</a> · <a href="../../../../agent-research/2610.00650-rule-evolve/">实现解读</a> · <a href="#qa-0dd59670d06cd928">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:branch-mixture" data-paper-title="Mixture of Self-Improving Branches for Agent Harness Optimization" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Mixture of Self-Improving Branches for Agent Harness Optimization Agent 原文首页未列机构 2026-09-29 将 harness 搜索拆成多条分支，每条分支维护不同的开发子集和 proposal policy；全分支都解决的样本被移除，具有分支区分度的样本被保留，部署时由只看输入特征的 router 选择开发集冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 优化 分支搜索 RSI Agent 运行流程与自进化：改的是哪一层 为什么多分支要维护不同开发子集和 proposal policy？ 如果所有分支看同样样本并采用相同提案，很容易收敛成重复 harness；差异化子集与策略保留专长，后续由输入路由选择。分支数增加也消耗开发成本，不能把多次搜索的总预算隐去再与单分支比较。 例如一支专攻工具格式，另一支专攻长程验证，输入路由才有不同能力可选，而不是多个同名副本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-branch-mixture-203f2124" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d71231e390a01996">为什么多分支要维护不同开发子集和 proposal policy？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abranch-mixture">Mixture of Self-Improving Branches for Agent Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>如果所有分支看同样样本并采用相同提案，很容易收敛成重复 harness；差异化子集与策略保留专长，后续由输入路由选择。分支数增加也消耗开发成本，不能把多次搜索的总预算隐去再与单分支比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一支专攻工具格式，另一支专攻长程验证，输入路由才有不同能力可选，而不是多个同名副本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37834">原论文</a> · <a href="../../../../agent-research/2609.37834-branch-mixture/">实现解读</a> · <a href="#qa-d71231e390a01996">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:branch-mixture" data-paper-title="Mixture of Self-Improving Branches for Agent Harness Optimization" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Mixture of Self-Improving Branches for Agent Harness Optimization Agent 原文首页未列机构 2026-09-29 将 harness 搜索拆成多条分支，每条分支维护不同的开发子集和 proposal policy；全分支都解决的样本被移除，具有分支区分度的样本被保留，部署时由只看输入特征的 router 选择开发集冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 优化 分支搜索 RSI Agent 运行流程与自进化：改的是哪一层 为什么全分支都解决的开发样本可移除，仍要保留有分支区分度的样本？ 共同已会样本对判断分支差异的信息量较小，持续占预算会稀释真正弱点。各分支保留有辨别力的子集与提议策略，部署 router 再按输入选择开发冠军；这种适应性开发集不能被当独立最终测试，路由也不能读取测试标签来挑赢家。 例如所有分支都能做简单排序，只有图搜索任务能区分两套策略，课程可把更多预算留给后者而不重复刷共同强项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:branch-mixture" data-paper-title="Mixture of Self-Improving Branches for Agent Harness Optimization" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Mixture of Self-Improving Branches for Agent Harness Optimization Agent 原文首页未列机构 2026-09-29 将 harness 搜索拆成多条分支，每条分支维护不同的开发子集和 proposal policy；全分支都解决的样本被移除，具有分支区分度的样本被保留，部署时由只看输入特征的 router 选择开发集冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 优化 分支搜索 RSI Agent 运行流程与自进化：改的是哪一层 输入路由多个专门分支，与始终运行一个全局冠军，有何假设差异？ 全局冠军假设同一 harness 能覆盖各类输入，分支混合则允许不同流程各擅长一部分任务，再由公开输入特征选择。专门化可能改善匹配，也引入路由错误与维护成本；路由只能用部署时可见信息，不能读当前测试真实分数再挑赢家。 教学例：代码题和浏览题分别有开发集冠军，router 可据任务特征选择；若先看两者在本题的金标得分才选择，就不是可部署路由。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9a69ceef4c84d93f">输入路由多个专门分支，与始终运行一个全局冠军，有何假设差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abranch-mixture">Mixture of Self-Improving Branches for Agent Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局冠军假设同一 harness 能覆盖各类输入，分支混合则允许不同流程各擅长一部分任务，再由公开输入特征选择。专门化可能改善匹配，也引入路由错误与维护成本；路由只能用部署时可见信息，不能读当前测试真实分数再挑赢家。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：代码题和浏览题分别有开发集冠军，router 可据任务特征选择；若先看两者在本题的金标得分才选择，就不是可部署路由。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37834">原论文</a> · <a href="../../../../agent-research/2609.37834-branch-mixture/">实现解读</a> · <a href="#qa-9a69ceef4c84d93f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:branch-mixture" data-paper-title="Mixture of Self-Improving Branches for Agent Harness Optimization" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Mixture of Self-Improving Branches for Agent Harness Optimization Agent 原文首页未列机构 2026-09-29 将 harness 搜索拆成多条分支，每条分支维护不同的开发子集和 proposal policy；全分支都解决的样本被移除，具有分支区分度的样本被保留，部署时由只看输入特征的 router 选择开发集冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 优化 分支搜索 RSI Agent 运行流程与自进化：改的是哪一层 部署 router 可以读取各分支在当前 test 的真实得分来挑冠军吗？ 不能。router 只看输入特征并选择开发期冠军，test 标签和未来执行分数不得进入。当前本地仅实现子集分化与线性输入路由，没有 LLM 生成 harness 或 SWE-bench，分支选择正确的 fixture 不代表真实混合模型收益。 例如先跑所有分支再看隐藏 judge 选最好，是 oracle ensemble，不是只依据请求输入的部署路由。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6112ff8a7f4f4deb">部署 router 可以读取各分支在当前 test 的真实得分来挑冠军吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abranch-mixture">Mixture of Self-Improving Branches for Agent Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。router 只看输入特征并选择开发期冠军，test 标签和未来执行分数不得进入。当前本地仅实现子集分化与线性输入路由，没有 LLM 生成 harness 或 SWE-bench，分支选择正确的 fixture 不代表真实混合模型收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先跑所有分支再看隐藏 judge 选最好，是 oracle ensemble，不是只依据请求输入的部署路由。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37834">原论文</a> · <a href="../../../../agent-research/2609.37834-branch-mixture/">实现解读</a> · <a href="#qa-6112ff8a7f4f4deb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-skills" data-paper-title="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI Agent Apodex / University of Illinois Urbana-Champaign 2026-09-29 从开发任务的 harness 执行反馈中提炼包含 when、provide、use 的 meta-skill，再冻结技能库；测试任务只检索相关 meta-skill 来构建新 harness，不用测试结果反向修改技能库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 设计 Meta-skill RSI Agent 运行流程与自进化：改的是哪一层 Meta-Skills 为什么关注“怎样配置 Agent 工作方式”的可迁移经验？ 相似任务可能共享规划、取证或验证习惯，若每次只保留具体答案，下一任务仍需重新设计流程。Meta-Skills 把这种如何工作的经验作为可复用对象，让检索结果指导 harness 使用。经验必须有适用条件，不能将某题有效的提示无条件施加到所有任务。 教学例：处理多源数字比较时先建证据表是流程经验；具体表中的数字只属于原任务，不应一起作为新任务答案复用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-meta-skills-2db3e168" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e92a721ec01e3781">Meta-Skills 为什么关注“怎样配置 Agent 工作方式”的可迁移经验？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ameta-skills">Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apodex / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似任务可能共享规划、取证或验证习惯，若每次只保留具体答案，下一任务仍需重新设计流程。Meta-Skills 把这种如何工作的经验作为可复用对象，让检索结果指导 harness 使用。经验必须有适用条件，不能将某题有效的提示无条件施加到所有任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：处理多源数字比较时先建证据表是流程经验；具体表中的数字只属于原任务，不应一起作为新任务答案复用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38143">原论文</a> · <a href="../../../../agent-research/2609.38143-meta-skills/">实现解读</a> · <a href="#qa-e92a721ec01e3781">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-skills" data-paper-title="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI Agent Apodex / University of Illinois Urbana-Champaign 2026-09-29 从开发任务的 harness 执行反馈中提炼包含 when、provide、use 的 meta-skill，再冻结技能库；测试任务只检索相关 meta-skill 来构建新 harness，不用测试结果反向修改技能库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 设计 Meta-skill RSI Agent 运行流程与自进化：改的是哪一层 为什么 meta-skill 要显式写 when、provide、use，而不只留一句“以后多验证”？ when 指出触发条件，provide 说明该补什么资源，use 规定如何把它接进流程，三者把宽泛建议转成可检索的设计知识。技能库在开发后冻结，测试只检索构建 harness；若再用测试成败改库，就不再是对未见任务的固定技能迁移。 例如“当工具输出不完整时，提供原始日志入口，并先核对再重试”比一句“更谨慎”更容易形成具体运行组件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-skills" data-paper-title="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI Agent Apodex / University of Illinois Urbana-Champaign 2026-09-29 从开发任务的 harness 执行反馈中提炼包含 when、provide、use 的 meta-skill，再冻结技能库；测试任务只检索相关 meta-skill 来构建新 harness，不用测试结果反向修改技能库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 设计 Meta-skill RSI Agent 运行流程与自进化：改的是哪一层 冻结开发技能库后测试只检索，与测试边做边写回有什么区别？ 冻结用于检查开发经验能否迁移，测试反馈写回会让后续任务利用评测结果，改变测试时信息合同。可以在当前任务利用允许的执行观察构建 harness，但不能把私有 test 得分用于长期修订或重选已报告结果。 例如 test1 错了后新增精确对应规则再跑 test1，就不再是固定库泛化，应另列为新的学习协议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-07f0a4ee787f4c47">冻结开发技能库后测试只检索，与测试边做边写回有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ameta-skills">Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apodex / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结用于检查开发经验能否迁移，测试反馈写回会让后续任务利用评测结果，改变测试时信息合同。可以在当前任务利用允许的执行观察构建 harness，但不能把私有 test 得分用于长期修订或重选已报告结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 test1 错了后新增精确对应规则再跑 test1，就不再是固定库泛化，应另列为新的学习协议。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38143">原论文</a> · <a href="../../../../agent-research/2609.38143-meta-skills/">实现解读</a> · <a href="#qa-07f0a4ee787f4c47">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-skills" data-paper-title="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI Agent Apodex / University of Illinois Urbana-Champaign 2026-09-29 从开发任务的 harness 执行反馈中提炼包含 when、provide、use 的 meta-skill，再冻结技能库；测试任务只检索相关 meta-skill 来构建新 harness，不用测试结果反向修改技能库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Harness 设计 Meta-skill RSI Agent 运行流程与自进化：改的是哪一层 本地开发 refine 与冻结检索如何限定证据结论？ 本地仅验证技能库接受开发反馈、冻结后检索不写回及相关状态不变量，fixture reward 不是 AI4AI benchmark。没有真实 harness proposer 和任务模型时，when 字段匹配成功不能算已学会可泛化设计策略，更不能复制原文提升数值。 例如检索器找到带“长文本”标签的 meta-skill，可检查路由，但未验证它在真实长上下文任务里改善结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e690a5adb56993a1">本地开发 refine 与冻结检索如何限定证据结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ameta-skills">Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apodex / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地仅验证技能库接受开发反馈、冻结后检索不写回及相关状态不变量，fixture reward 不是 AI4AI benchmark。没有真实 harness proposer 和任务模型时，when 字段匹配成功不能算已学会可泛化设计策略，更不能复制原文提升数值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如检索器找到带“长文本”标签的 meta-skill，可检查路由，但未验证它在真实长上下文任务里改善结果。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38143">原论文</a> · <a href="../../../../agent-research/2609.38143-meta-skills/">实现解读</a> · <a href="#qa-e690a5adb56993a1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:video-rsi" data-paper-title="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution Agent Tsinghua University 2026-09-29 视频 Agent 的执行 trace 只包含当前 harness 选择观察的证据，因此失败解释可能无法区分。Video-RSI 让模型回访原训练视频、主动收集额外观察，形成可检验诊断并改写 harness；候选只有在准确率提高且成本不恶化，或成本下降且准确率不恶化时才保留。 复现级别：L1 接纳规则。复现级别：L1 接纳规则。实现准确率—视觉成本双目标的 Pareto 接纳；未在视频 benchmark 上自动改写并执行完整 harness。未把训练视频私有答案或 example-level score 暴露给候选 harness；当前不含真实视频解码、代码改写 sandbox 和跨代停止条件，因而暂不登记为 Evolve 可执行 operator。  RSI Harness 演化 视频理解 Agent Agent 运行流程与自进化：改的是哪一层 视频 Agent 为什么可能需要改取证流程，而不只是换一个更强回答提示？ 长视频包含大量时刻和细节，错误可能发生在选帧、定位、读取或证据组织，而非最后一句回答。Video RSI 研究依据执行过程改进视频任务的 harness，让有限成本用在真正需要的证据上。观察到流程变化不等于理解能力已提高，需要同时检查准确性和真实成本。 教学例：问题问某人离开前做了什么，Agent 若只取开头和结尾，改写最终提示也看不到中间关键动作，需要先改取证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-video-rsi-6a868dfd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-852af1294a326d1e">视频 Agent 为什么可能需要改取证流程，而不只是换一个更强回答提示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avideo-rsi">Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长视频包含大量时刻和细节，错误可能发生在选帧、定位、读取或证据组织，而非最后一句回答。Video RSI 研究依据执行过程改进视频任务的 harness，让有限成本用在真正需要的证据上。观察到流程变化不等于理解能力已提高，需要同时检查准确性和真实成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：问题问某人离开前做了什么，Agent 若只取开头和结尾，改写最终提示也看不到中间关键动作，需要先改取证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37950">原论文</a> · <a href="../../../../agent-research/2609.37950-video-rsi/">实现解读</a> · <a href="#qa-852af1294a326d1e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:video-rsi" data-paper-title="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution Agent Tsinghua University 2026-09-29 视频 Agent 的执行 trace 只包含当前 harness 选择观察的证据，因此失败解释可能无法区分。Video-RSI 让模型回访原训练视频、主动收集额外观察，形成可检验诊断并改写 harness；候选只有在准确率提高且成本不恶化，或成本下降且准确率不恶化时才保留。 复现级别：L1 接纳规则。复现级别：L1 接纳规则。实现准确率—视觉成本双目标的 Pareto 接纳；未在视频 benchmark 上自动改写并执行完整 harness。未把训练视频私有答案或 example-level score 暴露给候选 harness；当前不含真实视频解码、代码改写 sandbox 和跨代停止条件，因而暂不登记为 Evolve 可执行 operator。  RSI Harness 演化 视频理解 Agent Agent 运行流程与自进化：改的是哪一层 为什么只读失败 trace 可能不足以确定视频 Agent 的取证问题？ trace 只记录旧 harness 选择看到的部分，没看到的关键帧无法从日志中重新推断。回访训练视频补观察，可检验是漏证据还是推理错，再改接口；接纳保持准确率与成本双门槛，不能用加权总分掩盖明显质量或费用退化。 例如旧策略只取视频开头，关键动作在末尾，失败日志没有该动作；回看原训练视频才能验证应修改采样而非答案措辞。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:video-rsi" data-paper-title="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution Agent Tsinghua University 2026-09-29 视频 Agent 的执行 trace 只包含当前 harness 选择观察的证据，因此失败解释可能无法区分。Video-RSI 让模型回访原训练视频、主动收集额外观察，形成可检验诊断并改写 harness；候选只有在准确率提高且成本不恶化，或成本下降且准确率不恶化时才保留。 复现级别：L1 接纳规则。复现级别：L1 接纳规则。实现准确率—视觉成本双目标的 Pareto 接纳；未在视频 benchmark 上自动改写并执行完整 harness。未把训练视频私有答案或 example-level score 暴露给候选 harness；当前不含真实视频解码、代码改写 sandbox 和跨代停止条件，因而暂不登记为 Evolve 可执行 operator。  RSI Harness 演化 视频理解 Agent Agent 运行流程与自进化：改的是哪一层 accuracy/cost 双门槛与单一加权分数相比保护了什么？ 候选须准确率不降且成本不升，并至少一项严格改善，防止一个目标的大幅好转掩盖另一个明显退化。允许误差阈值要预先声明，不能事后为接纳调松；双门槛也依赖同协议测量，不自动保证泛化。 例如准确率下降十点但帧数减半，可能在加权和中胜出，却不符合此处不恶化要求，应拒绝。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b4df352f6dc0c05f">accuracy/cost 双门槛与单一加权分数相比保护了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avideo-rsi">Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选须准确率不降且成本不升，并至少一项严格改善，防止一个目标的大幅好转掩盖另一个明显退化。允许误差阈值要预先声明，不能事后为接纳调松；双门槛也依赖同协议测量，不自动保证泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如准确率下降十点但帧数减半，可能在加权和中胜出，却不符合此处不恶化要求，应拒绝。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37950">原论文</a> · <a href="../../../../agent-research/2609.37950-video-rsi/">实现解读</a> · <a href="#qa-b4df352f6dc0c05f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:video-rsi" data-paper-title="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution Agent Tsinghua University 2026-09-29 视频 Agent 的执行 trace 只包含当前 harness 选择观察的证据，因此失败解释可能无法区分。Video-RSI 让模型回访原训练视频、主动收集额外观察，形成可检验诊断并改写 harness；候选只有在准确率提高且成本不恶化，或成本下降且准确率不恶化时才保留。 复现级别：L1 接纳规则。复现级别：L1 接纳规则。实现准确率—视觉成本双目标的 Pareto 接纳；未在视频 benchmark 上自动改写并执行完整 harness。未把训练视频私有答案或 example-level score 暴露给候选 harness；当前不含真实视频解码、代码改写 sandbox 和跨代停止条件，因而暂不登记为 Evolve 可执行 operator。  RSI Harness 演化 视频理解 Agent Agent 运行流程与自进化：改的是哪一层 本地 Pareto gate 已通过，为什么仍不登记可执行 Evolve operator？ 当前缺真实视频解码、代码改写沙箱与跨代停止条件，控制器不能完整执行和评估候选。gate 仅检查给定指标的接纳关系，不能用 fixture 分数证明视频 Agent 提升，也不能把注册名或三 seed 规则检查称为端到端进化。 例如输入两组数字可以算支配关系，但没有从候选 harness 真跑视频获得数字，就没有可晋级能力证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4c1480a393a3ca8e">本地 Pareto gate 已通过，为什么仍不登记可执行 Evolve operator？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avideo-rsi">Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前缺真实视频解码、代码改写沙箱与跨代停止条件，控制器不能完整执行和评估候选。gate 仅检查给定指标的接纳关系，不能用 fixture 分数证明视频 Agent 提升，也不能把注册名或三 seed 规则检查称为端到端进化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如输入两组数字可以算支配关系，但没有从候选 harness 真跑视频获得数字，就没有可晋级能力证据。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37950">原论文</a> · <a href="../../../../agent-research/2609.37950-video-rsi/">实现解读</a> · <a href="#qa-4c1480a393a3ca8e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-learning" data-paper-title="Harness Learning Enables Generalizable Test-Time Adaptation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness Learning Enables Generalizable Test-Time Adaptation Agent Johns Hopkins University 2026-09-28 论文把测试时适配的对象从模型参数转为可执行 harness：proposer 根据真实执行反馈修改验证、解释器、检索或重试组件；底层任务模型保持冻结，多轮执行后保留更有效的脚手架。 复现级别：L1 无 gold 机制诊断。复现级别：L1 无 gold 机制诊断。实现由执行反馈驱动的 harness revision policy 与多轮适配；冻结任务策略，不读取答案或计划。当前没有接入通用 Agent runner 或 Evolve，因为二者尚不能安全执行任意 harness 并完成隔离验证；本页不把规则化 mini-suite 的成功率宣称为 Agent 能力提升。HarnessProposer 与 adapt_harness 可接入外部真实执行 callback；汇总诊断见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Harness 学习 测试时适配 元学习 Agent 运行流程与自进化：改的是哪一层 Harness Learning 为什么把工具协议、记忆和规划流程也视为可学习对象？ 模型权重相同，外部工作流程仍会影响它能看到什么、何时调用工具和怎样恢复错误。Harness Learning 研究根据任务反馈修订这些可执行组织方式，减少把所有缺陷都归因于底座。流程适配有独立作用域，不能将它描述成模型参数已学到新能力。 教学例：底座不变，只加入每次提交前的测试流程，也可能改变结果；这种变化来自执行组织，不能当成模型权重训练收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harness-learning-a67122de" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ad3546d8176fcc6f">Harness Learning 为什么把工具协议、记忆和规划流程也视为可学习对象？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-learning">Harness Learning Enables Generalizable Test-Time Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johns Hopkins University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型权重相同，外部工作流程仍会影响它能看到什么、何时调用工具和怎样恢复错误。Harness Learning 研究根据任务反馈修订这些可执行组织方式，减少把所有缺陷都归因于底座。流程适配有独立作用域，不能将它描述成模型参数已学到新能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：底座不变，只加入每次提交前的测试流程，也可能改变结果；这种变化来自执行组织，不能当成模型权重训练收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35738">原论文</a> · <a href="../../../../agent-research/2609.35738-harness-learning/">实现解读</a> · <a href="#qa-ad3546d8176fcc6f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-learning" data-paper-title="Harness Learning Enables Generalizable Test-Time Adaptation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness Learning Enables Generalizable Test-Time Adaptation Agent Johns Hopkins University 2026-09-28 论文把测试时适配的对象从模型参数转为可执行 harness：proposer 根据真实执行反馈修改验证、解释器、检索或重试组件；底层任务模型保持冻结，多轮执行后保留更有效的脚手架。 复现级别：L1 无 gold 机制诊断。复现级别：L1 无 gold 机制诊断。实现由执行反馈驱动的 harness revision policy 与多轮适配；冻结任务策略，不读取答案或计划。当前没有接入通用 Agent runner 或 Evolve，因为二者尚不能安全执行任意 harness 并完成隔离验证；本页不把规则化 mini-suite 的成功率宣称为 Agent 能力提升。HarnessProposer 与 adapt_harness 可接入外部真实执行 callback；汇总诊断见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Harness 学习 测试时适配 元学习 Agent 运行流程与自进化：改的是哪一层 冻结任务模型权重，为什么仍然可以发生测试时适配？ 可适配对象是模型外可执行组件，如验证、解释器、检索或重试协议；执行反馈改变这些脚手架，进而影响同一模型之后的行为。它不同于微调，也不允许借接口把隐藏答案送给 proposer；本地分类策略更新更不能冒充整篇真实 LLM 适配链。 例如模型不变，但失败后为 shell 输出加入截断与错误定位器，下一次更易处理；改的是交互运行方式而非神经权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-learning" data-paper-title="Harness Learning Enables Generalizable Test-Time Adaptation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness Learning Enables Generalizable Test-Time Adaptation Agent Johns Hopkins University 2026-09-28 论文把测试时适配的对象从模型参数转为可执行 harness：proposer 根据真实执行反馈修改验证、解释器、检索或重试组件；底层任务模型保持冻结，多轮执行后保留更有效的脚手架。 复现级别：L1 无 gold 机制诊断。复现级别：L1 无 gold 机制诊断。实现由执行反馈驱动的 harness revision policy 与多轮适配；冻结任务策略，不读取答案或计划。当前没有接入通用 Agent runner 或 Evolve，因为二者尚不能安全执行任意 harness 并完成隔离验证；本页不把规则化 mini-suite 的成功率宣称为 Agent 能力提升。HarnessProposer 与 adapt_harness 可接入外部真实执行 callback；汇总诊断见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Harness 学习 测试时适配 元学习 Agent 运行流程与自进化：改的是哪一层 组内相对奖励更新 revision policy 与手写固定修订规则有何不同？ 本地按候选执行分减组均值形成优势，对 revision logit 做 REINFORCE，允许反馈影响提案偏好；固定规则没有这种参数学习。该小型分类 proposer 仍不是论文完整通用 harness 学习，不能从一个公式推断所有组件都能安全自由修改。 例如同组某修订实际更有效，它得到正优势增加选择倾向；不是因为规则作者预先指定它永远最好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fdbd2dc11b469064">组内相对奖励更新 revision policy 与手写固定修订规则有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-learning">Harness Learning Enables Generalizable Test-Time Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johns Hopkins University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地按候选执行分减组均值形成优势，对 revision logit 做 REINFORCE，允许反馈影响提案偏好；固定规则没有这种参数学习。该小型分类 proposer 仍不是论文完整通用 harness 学习，不能从一个公式推断所有组件都能安全自由修改。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同组某修订实际更有效，它得到正优势增加选择倾向；不是因为规则作者预先指定它永远最好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35738">原论文</a> · <a href="../../../../agent-research/2609.35738-harness-learning/">实现解读</a> · <a href="#qa-fdbd2dc11b469064">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-learning" data-paper-title="Harness Learning Enables Generalizable Test-Time Adaptation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Harness Learning Enables Generalizable Test-Time Adaptation Agent Johns Hopkins University 2026-09-28 论文把测试时适配的对象从模型参数转为可执行 harness：proposer 根据真实执行反馈修改验证、解释器、检索或重试组件；底层任务模型保持冻结，多轮执行后保留更有效的脚手架。 复现级别：L1 无 gold 机制诊断。复现级别：L1 无 gold 机制诊断。实现由执行反馈驱动的 harness revision policy 与多轮适配；冻结任务策略，不读取答案或计划。当前没有接入通用 Agent runner 或 Evolve，因为二者尚不能安全执行任意 harness 并完成隔离验证；本页不把规则化 mini-suite 的成功率宣称为 Agent 能力提升。HarnessProposer 与 adapt_harness 可接入外部真实执行 callback；汇总诊断见 ../../experiments/sep30-p0-p1-mechanisms-seeds42-44.json。  Harness 学习 测试时适配 元学习 Agent 运行流程与自进化：改的是哪一层 为何支持外部 callback 仍不能称已接入通用 Agent runner 或 Evolve？ 可信 callback 只是执行接口，通用系统还要安全运行任意 harness 并隔离验证。当前缺这条完整链，适配输入也只允许 score 与 failure 类型，不含 gold 或隐藏 verifier 字段；mini-suite 成功率不能当开放 Agent 能力。 例如 callback 直接返回预设高分能测闭环控制，但没有实际候选执行，就不能用该回调作为晋级证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6af322ce5a688d5e">为何支持外部 callback 仍不能称已接入通用 Agent runner 或 Evolve？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-learning">Harness Learning Enables Generalizable Test-Time Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johns Hopkins University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可信 callback 只是执行接口，通用系统还要安全运行任意 harness 并隔离验证。当前缺这条完整链，适配输入也只允许 score 与 failure 类型，不含 gold 或隐藏 verifier 字段；mini-suite 成功率不能当开放 Agent 能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 callback 直接返回预设高分能测闭环控制，但没有实际候选执行，就不能用该回调作为晋级证据。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35738">原论文</a> · <a href="../../../../agent-research/2609.35738-harness-learning/">实现解读</a> · <a href="#qa-6af322ce5a688d5e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx-model-replay" data-paper-title="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems Agent Kuaishou 2026-09-24 早期 AgentX 关注从研究构想到实现、评估的单次闭环；AgentX-Model 追问一次实验之后如何决定下一次做什么。Research Agent 负责跨论文和实验路径提出、独立审查研究问题；Model Agent 接收获批提案，在固定业务输入与预测任务下多轮改代码、训练、测量，并返回中间最佳实现、负结果和未解问题。两者通过提案而非共享完整工作日志衔接。 本地保真度：公开数据机制验证（concept demo）。本地保真度：公开数据机制验证（concept demo）。执行了双角色提案/审查/调查接口、四类动作和带依赖的结果盲回放；角色由确定性规则驱动，实验图由 MovieLens-1M 上实际训练的六个轻量模型节点组成。它不是论文的私有 473 节点历史图、LLM Agent 系统或线上 A/B 复现。本地两个“Agent”是有隔离接口的确定性执行角色，而非论文使用的 Pi/Claude Code/GLM、独立 LLM 审查或自动编程；模型变种也是预设可执行候选，非系统自主发明。六节点依赖图来自本仓库真实公开数据实验，不是作者 473 节点生产日志；  研究自动化 依赖约束历史回放 Agent 运行流程与自进化：改的是哪一层 AgentX-Model 为什么需要把一次研究选择与后续真实实验串起来？ 自动研究要决定下一步试什么，再由实现和评测获得新证据，不能只持续生成方案文本。该工作通过研究与模型执行角色衔接提案，使搜索历史反映实际试过的候选。历史 replay 只能重放已有结果的揭示与选择，不能证明这些训练实验在本地重新发生。 教学例：研究者提出换损失函数，执行者训练后才返回结果；重放旧日志时也应等选中该候选后揭示分数，不能提前偷看未来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-agentx-model-replay-82b929d4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-026d2b5abf0f0211">AgentX-Model 为什么需要把一次研究选择与后续真实实验串起来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentx-model-replay">Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自动研究要决定下一步试什么，再由实现和评测获得新证据，不能只持续生成方案文本。该工作通过研究与模型执行角色衔接提案，使搜索历史反映实际试过的候选。历史 replay 只能重放已有结果的揭示与选择，不能证明这些训练实验在本地重新发生。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：研究者提出换损失函数，执行者训练后才返回结果；重放旧日志时也应等选中该候选后揭示分数，不能提前偷看未来。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30001">原论文</a> · <a href="../../../../agent-research/2609.30001-agentx-model/">实现解读</a> · <a href="#qa-026d2b5abf0f0211">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx-model-replay" data-paper-title="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems Agent Kuaishou 2026-09-24 早期 AgentX 关注从研究构想到实现、评估的单次闭环；AgentX-Model 追问一次实验之后如何决定下一次做什么。Research Agent 负责跨论文和实验路径提出、独立审查研究问题；Model Agent 接收获批提案，在固定业务输入与预测任务下多轮改代码、训练、测量，并返回中间最佳实现、负结果和未解问题。两者通过提案而非共享完整工作日志衔接。 本地保真度：公开数据机制验证（concept demo）。本地保真度：公开数据机制验证（concept demo）。执行了双角色提案/审查/调查接口、四类动作和带依赖的结果盲回放；角色由确定性规则驱动，实验图由 MovieLens-1M 上实际训练的六个轻量模型节点组成。它不是论文的私有 473 节点历史图、LLM Agent 系统或线上 A/B 复现。本地两个“Agent”是有隔离接口的确定性执行角色，而非论文使用的 Pi/Claude Code/GLM、独立 LLM 审查或自动编程；模型变种也是预设可执行候选，非系统自主发明。六节点依赖图来自本仓库真实公开数据实验，不是作者 473 节点生产日志；  研究自动化 依赖约束历史回放 Agent 运行流程与自进化：改的是哪一层 Research Agent 与 Model Agent 为什么通过提案衔接，而不是共享完整实验日志？ 提案明确研究问题、约束和获批方向，模型实现侧再在固定业务输入与预测任务下多轮试验，减少两侧上下文相互淹没。返回中间最佳、负结果与未解问题支持下一研究决策；衔接的是证据化研究接口，不是只报最后一个漂亮分数。 例如研究侧提出检验长历史压缩假设，模型侧反馈最佳版本及失效条件，研究者据此决定下一假设，无需读每次编译输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx-model-replay" data-paper-title="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems Agent Kuaishou 2026-09-24 早期 AgentX 关注从研究构想到实现、评估的单次闭环；AgentX-Model 追问一次实验之后如何决定下一次做什么。Research Agent 负责跨论文和实验路径提出、独立审查研究问题；Model Agent 接收获批提案，在固定业务输入与预测任务下多轮改代码、训练、测量，并返回中间最佳实现、负结果和未解问题。两者通过提案而非共享完整工作日志衔接。 本地保真度：公开数据机制验证（concept demo）。本地保真度：公开数据机制验证（concept demo）。执行了双角色提案/审查/调查接口、四类动作和带依赖的结果盲回放；角色由确定性规则驱动，实验图由 MovieLens-1M 上实际训练的六个轻量模型节点组成。它不是论文的私有 473 节点历史图、LLM Agent 系统或线上 A/B 复现。本地两个“Agent”是有隔离接口的确定性执行角色，而非论文使用的 Pi/Claude Code/GLM、独立 LLM 审查或自动编程；模型变种也是预设可执行候选，非系统自主发明。六节点依赖图来自本仓库真实公开数据实验，不是作者 473 节点生产日志；  研究自动化 依赖约束历史回放 Agent 运行流程与自进化：改的是哪一层 相对父节点提升与刷新整条祖先路径最佳为什么不同？ 若父节点曾退化，子实验恢复一部分即可得到正增量，却未超过更早冠军。同时计算父差与可比祖先差避免把恢复宣传为新突破；Diagnose 主要降低不确定性，也不应与涨 AUC 的行动按同一即时目标排序。 例如祖先 AUC .80、父本 .75、子本 .78，子比父涨 .03，但仍比路径最佳低 .02，两个事实应同时保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-24e0589e2f1f44db">相对父节点提升与刷新整条祖先路径最佳为什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentx-model-replay">Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若父节点曾退化，子实验恢复一部分即可得到正增量，却未超过更早冠军。同时计算父差与可比祖先差避免把恢复宣传为新突破；Diagnose 主要降低不确定性，也不应与涨 AUC 的行动按同一即时目标排序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如祖先 AUC .80、父本 .75、子本 .78，子比父涨 .03，但仍比路径最佳低 .02，两个事实应同时保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30001">原论文</a> · <a href="../../../../agent-research/2609.30001-agentx-model/">实现解读</a> · <a href="#qa-24e0589e2f1f44db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx-model-replay" data-paper-title="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems Agent Kuaishou 2026-09-24 早期 AgentX 关注从研究构想到实现、评估的单次闭环；AgentX-Model 追问一次实验之后如何决定下一次做什么。Research Agent 负责跨论文和实验路径提出、独立审查研究问题；Model Agent 接收获批提案，在固定业务输入与预测任务下多轮改代码、训练、测量，并返回中间最佳实现、负结果和未解问题。两者通过提案而非共享完整工作日志衔接。 本地保真度：公开数据机制验证（concept demo）。本地保真度：公开数据机制验证（concept demo）。执行了双角色提案/审查/调查接口、四类动作和带依赖的结果盲回放；角色由确定性规则驱动，实验图由 MovieLens-1M 上实际训练的六个轻量模型节点组成。它不是论文的私有 473 节点历史图、LLM Agent 系统或线上 A/B 复现。本地两个“Agent”是有隔离接口的确定性执行角色，而非论文使用的 Pi/Claude Code/GLM、独立 LLM 审查或自动编程；模型变种也是预设可执行候选，非系统自主发明。六节点依赖图来自本仓库真实公开数据实验，不是作者 473 节点生产日志；  研究自动化 依赖约束历史回放 Agent 运行流程与自进化：改的是哪一层 历史 replay 的候选结果何时揭示，本地数据如何避免未来泄露？ 只有父实验已选才能选子节点，候选结果选中后才揭示；MovieLens 按时间留后两交互验证测试，训练统计不读未来，champion 只看 validation。规则选择器与逻辑回归 replay 不冒充论文 LLM 研究 Agent，更不复刻线上 A/B。 例如未选择的另一个分支即使记录里成绩很高，也不能让 selector 提前读取来决定下一步，否则变成未来指标 oracle。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9e537d66be10432b">历史 replay 的候选结果何时揭示，本地数据如何避免未来泄露？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentx-model-replay">Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有父实验已选才能选子节点，候选结果选中后才揭示；MovieLens 按时间留后两交互验证测试，训练统计不读未来，champion 只看 validation。规则选择器与逻辑回归 replay 不冒充论文 LLM 研究 Agent，更不复刻线上 A/B。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如未选择的另一个分支即使记录里成绩很高，也不能让 selector 提前读取来决定下一步，否则变成未来指标 oracle。</p>
<p class="ar-learning-sources">依据：本地复现、可执行路径与防泄漏边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30001">原论文</a> · <a href="../../../../agent-research/2609.30001-agentx-model/">实现解读</a> · <a href="#qa-9e537d66be10432b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sciencebuddy" data-paper-title="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents Agent Gen-Verse research collaboration 2026-09-15 内层递归演化交互 harness，外层用成功轨迹更新科学 Agent 策略。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双层状态更新；没有连接真实实验室环境。本地执行双层状态更新；没有连接真实实验室环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  科学 Agent 递归自进化 Agent 运行流程与自进化：改的是哪一层 ScienceBuddy 为什么把科学任务中的工具交互和策略学习放在同一持续过程里？ 科学任务常需要提出动作、使用工具、解释观察并调整后续方案，固定一次提示难以覆盖不断出现的反馈。ScienceBuddy 研究工作流程与策略如何在这种交互中共同改进。两个层面的变化要分别追踪，模拟状态更新不能替代真实科学环境或模型训练证据。 教学例：检索发现原假设缺少证据后，流程可改为先核查来源；策略是否真正学会这种判断，还需要后续实际任务验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-sciencebuddy-cd9b47fe" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c3463aea1843b4ca">ScienceBuddy 为什么把科学任务中的工具交互和策略学习放在同一持续过程里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asciencebuddy">ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Gen-Verse research collaboration</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>科学任务常需要提出动作、使用工具、解释观察并调整后续方案，固定一次提示难以覆盖不断出现的反馈。ScienceBuddy 研究工作流程与策略如何在这种交互中共同改进。两个层面的变化要分别追踪，模拟状态更新不能替代真实科学环境或模型训练证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：检索发现原假设缺少证据后，流程可改为先核查来源；策略是否真正学会这种判断，还需要后续实际任务验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17523">原论文</a> · <a href="../../../../agent-research/2609.17523-sciencebuddy/">实现解读</a> · <a href="#qa-c3463aea1843b4ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sciencebuddy" data-paper-title="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents Agent Gen-Verse research collaboration 2026-09-15 内层递归演化交互 harness，外层用成功轨迹更新科学 Agent 策略。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双层状态更新；没有连接真实实验室环境。本地执行双层状态更新；没有连接真实实验室环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  科学 Agent 递归自进化 Agent 运行流程与自进化：改的是哪一层 内层演化 harness、外层更新策略，为什么不能简化成同一轮反复改 prompt？ 两层修改对象不同：内层优化交互方式，外层利用成功执行轨迹改变科学 Agent 的参数策略，后者又影响下一轮内层搜索。只有真实执行、筛选和训练组成闭环，才体现递归中的递归；参考门控函数或合成统计不能替代这些模型与环境过程。 例如先找到更好的实验检查流程，再用其成功轨迹训练 Agent，使之后更会使用该流程；仅把提示重写三遍没有第二层更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sciencebuddy" data-paper-title="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents Agent Gen-Verse research collaboration 2026-09-15 内层递归演化交互 harness，外层用成功轨迹更新科学 Agent 策略。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双层状态更新；没有连接真实实验室环境。本地执行双层状态更新；没有连接真实实验室环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  科学 Agent 递归自进化 Agent 运行流程与自进化：改的是哪一层 双层反馈相比固定 harness 的单层训练可能带来什么取舍？ 双层可同时改善数据产生方式与策略，但两侧都变会增加归因与非平稳性，需分别记录版本、轨迹来源和更新。固定 harness 较易控制却可能限制探索；机制比较不能代替科学任务能力与真实实验结果。 例如外层成绩上升可能来自更强工具反馈，也可能来自新参数，若版本不记录，就难判断哪一层贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ec29bbe804bbe212">双层反馈相比固定 harness 的单层训练可能带来什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asciencebuddy">ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Gen-Verse research collaboration</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>双层可同时改善数据产生方式与策略，但两侧都变会增加归因与非平稳性，需分别记录版本、轨迹来源和更新。固定 harness 较易控制却可能限制探索；机制比较不能代替科学任务能力与真实实验结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如外层成绩上升可能来自更强工具反馈，也可能来自新参数，若版本不记录，就难判断哪一层贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17523">原论文</a> · <a href="../../../../agent-research/2609.17523-sciencebuddy/">实现解读</a> · <a href="#qa-ec29bbe804bbe212">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sciencebuddy" data-paper-title="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents Agent Gen-Verse research collaboration 2026-09-15 内层递归演化交互 harness，外层用成功轨迹更新科学 Agent 策略。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双层状态更新；没有连接真实实验室环境。本地执行双层状态更新；没有连接真实实验室环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  科学 Agent 递归自进化 Agent 运行流程与自进化：改的是哪一层 本地 double-state reference 是否包含实验室和真实科学策略学习？ 不包含。本地只执行双层状态更新与门控 reference，没有真实实验室环境、完整科学任务或论文规模训练。三 seed 中间量能验证分支和信息流，不是可复制的科学发现成功率，也不能按状态更新次数声称递归学习已完整验证。 例如计数显示内层改两次、外层更新一次，只说明控制状态发生变化，没有真实轨迹和梯度就不足以证明策略学会任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-04bf786ad243175c">本地 double-state reference 是否包含实验室和真实科学策略学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asciencebuddy">ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Gen-Verse research collaboration</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不包含。本地只执行双层状态更新与门控 reference，没有真实实验室环境、完整科学任务或论文规模训练。三 seed 中间量能验证分支和信息流，不是可复制的科学发现成功率，也不能按状态更新次数声称递归学习已完整验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如计数显示内层改两次、外层更新一次，只说明控制状态发生变化，没有真实轨迹和梯度就不足以证明策略学会任务。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17523">原论文</a> · <a href="../../../../agent-research/2609.17523-sciencebuddy/">实现解读</a> · <a href="#qa-04bf786ad243175c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cobra-skills" data-paper-title="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization Agent The Chinese University of Hong Kong, Shenzhen 2026-09-10 把技能优化视为动态候选空间中的预算化 contextual bandit，优先评估高收益或高信息量技能，再依据执行反馈演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能进化 Contextual bandit Agent 运行流程与自进化：改的是哪一层 技能候选持续增长时，COBRA-Skills 为什么不能给每个候选同样多的试验机会？ 评估技能会消耗任务执行预算，候选数量与质量又会随演化变化，平均分配可能浪费在明显无用或重复的条目上。COBRA-Skills 研究结合当前上下文和已见反馈安排试验，使有限预算更有针对性。选择器只能利用已获得证据，不能把未执行候选的效果当成已知。 教学例：十份相似技能已有多次失败记录，新生成的一份可能仍值得少量探索；预算不够时，全部各跑百次并不可行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-cobra-skills-f91c343f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1c56fd2f44841929">技能候选持续增长时，COBRA-Skills 为什么不能给每个候选同样多的试验机会？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acobra-skills">COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>评估技能会消耗任务执行预算，候选数量与质量又会随演化变化，平均分配可能浪费在明显无用或重复的条目上。COBRA-Skills 研究结合当前上下文和已见反馈安排试验，使有限预算更有针对性。选择器只能利用已获得证据，不能把未执行候选的效果当成已知。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：十份相似技能已有多次失败记录，新生成的一份可能仍值得少量探索；预算不够时，全部各跑百次并不可行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11682">原论文</a> · <a href="../../../../agent-research/2609.11682-cobra-skills/">实现解读</a> · <a href="#qa-1c56fd2f44841929">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cobra-skills" data-paper-title="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization Agent The Chinese University of Hong Kong, Shenzhen 2026-09-10 把技能优化视为动态候选空间中的预算化 contextual bandit，优先评估高收益或高信息量技能，再依据执行反馈演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能进化 Contextual bandit Agent 运行流程与自进化：改的是哪一层 动态技能候选为什么适合预算化 contextual bandit，而不是只按历史最高分排序？ 技能收益依赖当前任务，新增或修订候选又缺乏历史数据。上下文 bandit 在利用已知高收益与探索高信息量候选之间分配评测预算，再用真实反馈演化；仅看历史最高值会偏向早期幸运技能，忽略新任务条件和未评候选的不确定性。 例如旧技能擅长文件操作，新任务转向网页，多给新候选少量试验可能比持续验证旧冠军更有信息价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cobra-skills" data-paper-title="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization Agent The Chinese University of Hong Kong, Shenzhen 2026-09-10 把技能优化视为动态候选空间中的预算化 contextual bandit，优先评估高收益或高信息量技能，再依据执行反馈演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能进化 Contextual bandit Agent 运行流程与自进化：改的是哪一层 提出一个技能变体与获得它的执行收益，为什么应分成两个证据阶段？ 提案根据已有经验生成可能更好的行为描述，尚未说明它在当前任务有效；执行评估才产生可用于预算分配和后续演化的反馈。候选空间可动态扩展，但加入集合不等于获得正奖励。COBRA-Skills 的 bandit 选择需要区分已测收益和未测不确定性，不能用提案自评补齐结果。 教学例：新技能写得更详细，可先安排试验；只有任务真实执行后才知道它是否帮助，而不能直接把“预计改进”当作成功样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dd3c458ed7ccbf9b">提出一个技能变体与获得它的执行收益，为什么应分成两个证据阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acobra-skills">COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提案根据已有经验生成可能更好的行为描述，尚未说明它在当前任务有效；执行评估才产生可用于预算分配和后续演化的反馈。候选空间可动态扩展，但加入集合不等于获得正奖励。COBRA-Skills 的 bandit 选择需要区分已测收益和未测不确定性，不能用提案自评补齐结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：新技能写得更详细，可先安排试验；只有任务真实执行后才知道它是否帮助，而不能直接把“预计改进”当作成功样本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11682">原论文</a> · <a href="../../../../agent-research/2609.11682-cobra-skills/">实现解读</a> · <a href="#qa-dd3c458ed7ccbf9b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cobra-skills" data-paper-title="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization Agent The Chinese University of Hong Kong, Shenzhen 2026-09-10 把技能优化视为动态候选空间中的预算化 contextual bandit，优先评估高收益或高信息量技能，再依据执行反馈演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能进化 Contextual bandit Agent 运行流程与自进化：改的是哪一层 本地 contextual-UCB 分配是否覆盖真实 LLM 技能演化？ 不覆盖。本地执行分配和反馈准入 reference，没有外部 LLM 或六套环境。候选 index、置信项和预算可独立检查，实际技能文本生成与任务执行尚未发生；不能把 fixture 反馈写成真实成本降低或 Agent 能力提升。 例如一个数值 arm 的 UCB 变大而被选中，仅验证 bandit 公式，没有证明对应自然语言技能在网页任务可执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e657576f6a249149">本地 contextual-UCB 分配是否覆盖真实 LLM 技能演化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acobra-skills">COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不覆盖。本地执行分配和反馈准入 reference，没有外部 LLM 或六套环境。候选 index、置信项和预算可独立检查，实际技能文本生成与任务执行尚未发生；不能把 fixture 反馈写成真实成本降低或 Agent 能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个数值 arm 的 UCB 变大而被选中，仅验证 bandit 公式，没有证明对应自然语言技能在网页任务可执行。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11682">原论文</a> · <a href="../../../../agent-research/2609.11682-cobra-skills/">实现解读</a> · <a href="#qa-e657576f6a249149">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ecdysis" data-paper-title="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents Agent Chengdu Institute of Computer Applications, Chinese Academy of Sciences 2026-09-10 聚合跨任务重复失败以区分模型偶发错误和 harness 系统缺陷，再由 FDCR 多角色诊断形成修复规格。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Harness 自进化 失败诊断 Agent 运行流程与自进化：改的是哪一层 Ecdysis 为什么先问失败来自模型偶发行为，还是来自运行流程的共同缺陷？ 相同 Agent 在不同任务出错，既可能是具体理解错误，也可能是工具包装、上下文或恢复流程反复制造问题。Ecdysis 研究从多次执行中找到可系统修复的 harness 缺陷，使改进针对共享原因。重复现象只是诊断线索，不能未经修复执行和验证就宣称问题已解决。 教学例：多题都因工具结果被截断而漏证据，可能是共享接口问题；只有一道题误读内容，则不应马上改所有任务的流程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-ecdysis-3d533dc6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a195b04da4575d0d">Ecdysis 为什么先问失败来自模型偶发行为，还是来自运行流程的共同缺陷？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aecdysis">Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chengdu Institute of Computer Applications, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同 Agent 在不同任务出错，既可能是具体理解错误，也可能是工具包装、上下文或恢复流程反复制造问题。Ecdysis 研究从多次执行中找到可系统修复的 harness 缺陷，使改进针对共享原因。重复现象只是诊断线索，不能未经修复执行和验证就宣称问题已解决。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：多题都因工具结果被截断而漏证据，可能是共享接口问题；只有一道题误读内容，则不应马上改所有任务的流程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11677">原论文</a> · <a href="../../../../agent-research/2609.11677-ecdysis/">实现解读</a> · <a href="#qa-a195b04da4575d0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ecdysis" data-paper-title="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents Agent Chengdu Institute of Computer Applications, Chinese Academy of Sciences 2026-09-10 聚合跨任务重复失败以区分模型偶发错误和 harness 系统缺陷，再由 FDCR 多角色诊断形成修复规格。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Harness 自进化 失败诊断 Agent 运行流程与自进化：改的是哪一层 为什么同一种失败要跨任务聚合，才能判断是 harness 系统缺陷？ 单次出错可能来自模型随机性或特殊题意，重复出现的模式才更提示共同运行接口存在问题。多角色诊断把这些证据转成可验证修复规格，避免每遇一次失败就改全局框架；聚合相关性仍不是充分因果证明，修复后必须做受影响行为对照。 例如许多任务都因日志被截断而漏掉错误码，比单题猜错更支持检查输出接口；应针对截断机制修复而非泛泛换模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ecdysis" data-paper-title="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents Agent Chengdu Institute of Computer Applications, Chinese Academy of Sciences 2026-09-10 聚合跨任务重复失败以区分模型偶发错误和 harness 系统缺陷，再由 FDCR 多角色诊断形成修复规格。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Harness 自进化 失败诊断 Agent 运行流程与自进化：改的是哪一层 形成修复规格与直接执行 harness 补丁，分别处在改进链的哪一步？ FDCR 的多角色诊断把失败证据组织成可讨论的修复规格，说明应该改哪里和为何改；真正执行还需生成具体补丁、接入运行并验证后果。诊断输出不能冒充已修改系统，触发门或修复建议数量也不说明任务成功提升，本地 reference 尤其要保持这个证据边界。 教学例：规格指出“保留工具返回的错误字段”，代码是否真的修改并在后续任务生效，需要另行检查补丁和运行记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-cd6fec7b3d5c110c">形成修复规格与直接执行 harness 补丁，分别处在改进链的哪一步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aecdysis">Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chengdu Institute of Computer Applications, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>FDCR 的多角色诊断把失败证据组织成可讨论的修复规格，说明应该改哪里和为何改；真正执行还需生成具体补丁、接入运行并验证后果。诊断输出不能冒充已修改系统，触发门或修复建议数量也不说明任务成功提升，本地 reference 尤其要保持这个证据边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：规格指出“保留工具返回的错误字段”，代码是否真的修改并在后续任务生效，需要另行检查补丁和运行记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11677">原论文</a> · <a href="../../../../agent-research/2609.11677-ecdysis/">实现解读</a> · <a href="#qa-cd6fec7b3d5c110c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ecdysis" data-paper-title="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents Agent Chengdu Institute of Computer Applications, Chinese Academy of Sciences 2026-09-10 聚合跨任务重复失败以区分模型偶发错误和 harness 系统缺陷，再由 FDCR 多角色诊断形成修复规格。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Harness 自进化 失败诊断 Agent 运行流程与自进化：改的是哪一层 本地触发 FDCR 修复门是否已生成或执行 harness 补丁？ 没有。本地只聚合公开 observation 的失败签名并触发受限修复门，不生成或执行代码，也没有论文规模训练。门触发说明统计满足条件，不证明诊断正确或真实缺陷已修，三 seed 计数不能换算原文速度和准确率。 例如三次同类失败后状态变为“待修复”，只是调度信号；没有实际补丁和重跑就不能标为已解决。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fb9a1324918e6565">本地触发 FDCR 修复门是否已生成或执行 harness 补丁？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aecdysis">Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chengdu Institute of Computer Applications, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地只聚合公开 observation 的失败签名并触发受限修复门，不生成或执行代码，也没有论文规模训练。门触发说明统计满足条件，不证明诊断正确或真实缺陷已修，三 seed 计数不能换算原文速度和准确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三次同类失败后状态变为“待修复”，只是调度信号；没有实际补丁和重跑就不能标为已解决。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11677">原论文</a> · <a href="../../../../agent-research/2609.11677-ecdysis/">实现解读</a> · <a href="#qa-fb9a1324918e6565">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:maple" data-paper-title="MAPLE: Memory-Augmented Planning with Language and Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MAPLE: Memory-Augmented Planning with Language and Evolution Agent Harbin Institute of Technology, Shenzhen 2026-09-10 MAPLE 把自然语言优化知识变成可持续修改的程序状态：生成候选、检查可执行性、接纳更好的方案，并把已接受程序带到后续问题中继续进化，而不是每次从零提示。 复现级别：持久状态机制诊断。复现级别：持久状态机制诊断。实现候选方案接纳、跨任务复用和版本化状态，不执行论文的数学优化器或 LLM 代码生成。三种子结果见 metrics/mini-suite-seeds42-44.json。本地只接纳由非空命名操作构成的公开计划并验证后续复用；没有运行作者求解器、训练模型或外部工具，因此不把 mini-suite 成功率作为论文能力复现。  持久化优化规划 Agent 运行流程与自进化：改的是哪一层 MAPLE 为什么希望优化知识能随着连续求解保留下来？ 连续问题常有共享结构，若每题从零提案，已验证的程序改进很难积累。MAPLE 把可执行解法作为持续研究状态，让下一问题从已接受程序继续探索。继承也可能带来旧假设偏差，必须重新验证新问题条件，不能把可执行或历史成功当成当前最优证明。 教学例：上一次排程程序已处理资源冲突，新问题可从该程序起步；但新增加的时间窗口约束仍需实现与测试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-maple-2e42a8d7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bf5ce6d0765f08ca">MAPLE 为什么希望优化知识能随着连续求解保留下来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amaple">MAPLE: Memory-Augmented Planning with Language and Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续问题常有共享结构，若每题从零提案，已验证的程序改进很难积累。MAPLE 把可执行解法作为持续研究状态，让下一问题从已接受程序继续探索。继承也可能带来旧假设偏差，必须重新验证新问题条件，不能把可执行或历史成功当成当前最优证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：上一次排程程序已处理资源冲突，新问题可从该程序起步；但新增加的时间窗口约束仍需实现与测试。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11636">原论文</a> · <a href="../../../../agent-research/2609.11636-maple/">实现解读</a> · <a href="#qa-bf5ce6d0765f08ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:maple" data-paper-title="MAPLE: Memory-Augmented Planning with Language and Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MAPLE: Memory-Augmented Planning with Language and Evolution Agent Harbin Institute of Technology, Shenzhen 2026-09-10 MAPLE 把自然语言优化知识变成可持续修改的程序状态：生成候选、检查可执行性、接纳更好的方案，并把已接受程序带到后续问题中继续进化，而不是每次从零提示。 复现级别：持久状态机制诊断。复现级别：持久状态机制诊断。实现候选方案接纳、跨任务复用和版本化状态，不执行论文的数学优化器或 LLM 代码生成。三种子结果见 metrics/mini-suite-seeds42-44.json。本地只接纳由非空命名操作构成的公开计划并验证后续复用；没有运行作者求解器、训练模型或外部工具，因此不把 mini-suite 成功率作为论文能力复现。  持久化优化规划 Agent 运行流程与自进化：改的是哪一层 被接受程序作为后续问题的起点，为什么比每次重新提示更能积累优化知识？ 程序状态保留已经验证可执行的结构和取舍，下一题在其上修改，而不是靠自然语言重新回忆所有细节。接纳规则阻止未执行的想法直接覆盖可靠父本；跨问题继续进化也要检查任务差异，不能把某一实例的特化程序当成普适最佳。 例如上一题已实现可靠的数据解析，下一题可以在此基础改目标函数，而不每次从空脚本重新生成并重犯格式错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:maple" data-paper-title="MAPLE: Memory-Augmented Planning with Language and Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MAPLE: Memory-Augmented Planning with Language and Evolution Agent Harbin Institute of Technology, Shenzhen 2026-09-10 MAPLE 把自然语言优化知识变成可持续修改的程序状态：生成候选、检查可执行性、接纳更好的方案，并把已接受程序带到后续问题中继续进化，而不是每次从零提示。 复现级别：持久状态机制诊断。复现级别：持久状态机制诊断。实现候选方案接纳、跨任务复用和版本化状态，不执行论文的数学优化器或 LLM 代码生成。三种子结果见 metrics/mini-suite-seeds42-44.json。本地只接纳由非空命名操作构成的公开计划并验证后续复用；没有运行作者求解器、训练模型或外部工具，因此不把 mini-suite 成功率作为论文能力复现。  持久化优化规划 Agent 运行流程与自进化：改的是哪一层 接受可执行程序与接受“看起来更好的”优化描述有什么不同？ 描述只表达意图，程序必须能运行并通过相应比较，才形成可继续演化的状态。可执行仍不代表更有效，合法性和收益是不同门槛；一次改进也不能证明对所有后续问题泛化，不应无条件继承失败提案。 例如“减少重复搜索”是建议，真正候选需要改变调用逻辑并验证没有漏掉必需证据，才能称接纳了优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8144cd5a6a2e654d">接受可执行程序与接受“看起来更好的”优化描述有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amaple">MAPLE: Memory-Augmented Planning with Language and Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>描述只表达意图，程序必须能运行并通过相应比较，才形成可继续演化的状态。可执行仍不代表更有效，合法性和收益是不同门槛；一次改进也不能证明对所有后续问题泛化，不应无条件继承失败提案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“减少重复搜索”是建议，真正候选需要改变调用逻辑并验证没有漏掉必需证据，才能称接纳了优化。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11636">原论文</a> · <a href="../../../../agent-research/2609.11636-maple/">实现解读</a> · <a href="#qa-8144cd5a6a2e654d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:maple" data-paper-title="MAPLE: Memory-Augmented Planning with Language and Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MAPLE: Memory-Augmented Planning with Language and Evolution Agent Harbin Institute of Technology, Shenzhen 2026-09-10 MAPLE 把自然语言优化知识变成可持续修改的程序状态：生成候选、检查可执行性、接纳更好的方案，并把已接受程序带到后续问题中继续进化，而不是每次从零提示。 复现级别：持久状态机制诊断。复现级别：持久状态机制诊断。实现候选方案接纳、跨任务复用和版本化状态，不执行论文的数学优化器或 LLM 代码生成。三种子结果见 metrics/mini-suite-seeds42-44.json。本地只接纳由非空命名操作构成的公开计划并验证后续复用；没有运行作者求解器、训练模型或外部工具，因此不把 mini-suite 成功率作为论文能力复现。  持久化优化规划 Agent 运行流程与自进化：改的是哪一层 本地非空命名操作计划验证与作者求解器之间有什么差别？ 本地只接纳由非空命名操作组成的公开计划，并检查后续复用，没有作者求解器、训练模型或外部工具。计划表示的执行合同可验，但 mini-suite 满分不能作为原文优化能力或通用程序进化；不得把未实现的 solver 用名称注册补齐。 例如“搜索、验证”两个节点不是空字符串，可通过结构检查，却尚未证明真实搜索算法性能比上一版更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-97e540f60a62b382">本地非空命名操作计划验证与作者求解器之间有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amaple">MAPLE: Memory-Augmented Planning with Language and Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地只接纳由非空命名操作组成的公开计划，并检查后续复用，没有作者求解器、训练模型或外部工具。计划表示的执行合同可验，但 mini-suite 满分不能作为原文优化能力或通用程序进化；不得把未实现的 solver 用名称注册补齐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“搜索、验证”两个节点不是空字符串，可通过结构检查，却尚未证明真实搜索算法性能比上一版更好。</p>
<p class="ar-learning-sources">依据：本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11636">原论文</a> · <a href="../../../../agent-research/2609.11636-maple/">实现解读</a> · <a href="#qa-97e540f60a62b382">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:procedural-graphs" data-paper-title="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents Agent Google 2026-09-08 方法把成功经验从自然语言片段提升为 procedure–relation–procedure 图。新经验先局部化为候选图编辑，再经过 held-out 验证门才写入长期结构，减少错误经验污染。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现 procedure–relation–procedure 图和保守编辑门，不包含 LLM 生成或真实环境执行。三种子 evomem-mini 结果见 metrics/mini-suite-seeds42-44.json。本地编辑门以“已建立路线必须保留首尾节点”为确定性代理；策略看不到隐藏答案/计划，也未调用真实工具，因此仅验证图更新与拒绝路径。  自进化程序图 Agent 运行流程与自进化：改的是哪一层 procedure—relation—procedure 图比单纯保存技能片段多了什么？ 图显式表达程序之间的依赖或组合关系，让新经验可以修改局部执行结构，而不只是增加一段相似文字。关系正确性会影响后续路径，因此新编辑要经过独立 held-out 验证，不能因为来自一次成功轨迹就直接永久写入。 例如“认证后查询”表达先后约束，“查询后若失败刷新凭据”表达恢复关系，单独两个文本片段未必包含这些连接。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-procedural-graphs-6aeeaceb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0813fc391c0f0f1c">procedure—relation—procedure 图比单纯保存技能片段多了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprocedural-graphs">Procedural Graphs: Self-Evolving Execution Structures for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图显式表达程序之间的依赖或组合关系，让新经验可以修改局部执行结构，而不只是增加一段相似文字。关系正确性会影响后续路径，因此新编辑要经过独立 held-out 验证，不能因为来自一次成功轨迹就直接永久写入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“认证后查询”表达先后约束，“查询后若失败刷新凭据”表达恢复关系，单独两个文本片段未必包含这些连接。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09153">原论文</a> · <a href="../../../../agent-research/2609.09153-procedural-graphs/">实现解读</a> · <a href="#qa-0813fc391c0f0f1c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:procedural-graphs" data-paper-title="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents Agent Google 2026-09-08 方法把成功经验从自然语言片段提升为 procedure–relation–procedure 图。新经验先局部化为候选图编辑，再经过 held-out 验证门才写入长期结构，减少错误经验污染。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现 procedure–relation–procedure 图和保守编辑门，不包含 LLM 生成或真实环境执行。三种子 evomem-mini 结果见 metrics/mini-suite-seeds42-44.json。本地编辑门以“已建立路线必须保留首尾节点”为确定性代理；策略看不到隐藏答案/计划，也未调用真实工具，因此仅验证图更新与拒绝路径。  自进化程序图 Agent 运行流程与自进化：改的是哪一层 为什么经验写入要先局部化为图编辑，再经过 held-out 门？ 图中的过程关系会影响多条执行路径，整段新经验直接覆盖可能污染无关技能。局部编辑明确改哪条节点或关系，held-out 再检验是否超越原轨迹的偶然成功；验证通过只支持该评测范围，不能把训练轨迹上的自洽当作全局结构已可靠。 例如只新增“认证失败后刷新令牌”的恢复边，不重写整个上传图，再用未参与提议的任务检查是否引入重复认证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:procedural-graphs" data-paper-title="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents Agent Google 2026-09-08 方法把成功经验从自然语言片段提升为 procedure–relation–procedure 图。新经验先局部化为候选图编辑，再经过 held-out 验证门才写入长期结构，减少错误经验污染。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现 procedure–relation–procedure 图和保守编辑门，不包含 LLM 生成或真实环境执行。三种子 evomem-mini 结果见 metrics/mini-suite-seeds42-44.json。本地编辑门以“已建立路线必须保留首尾节点”为确定性代理；策略看不到隐藏答案/计划，也未调用真实工具，因此仅验证图更新与拒绝路径。  自进化程序图 Agent 运行流程与自进化：改的是哪一层 局部候选图编辑与重写整张程序图有什么取舍？ 局部编辑减少对已有路线的无关影响，便于归因与回退；整图重写更自由但容易破坏旧接口和有效路径。局部也不保证安全，修改一个关键节点可影响许多后续过程，仍需独立验证而非只查图格式。 例如替换查询节点可能改变所有下游输入，虽然只动一个节点，也应验证依赖它的路线是否保持可用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-36893bcf703a5f2a">局部候选图编辑与重写整张程序图有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprocedural-graphs">Procedural Graphs: Self-Evolving Execution Structures for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部编辑减少对已有路线的无关影响，便于归因与回退；整图重写更自由但容易破坏旧接口和有效路径。局部也不保证安全，修改一个关键节点可影响许多后续过程，仍需独立验证而非只查图格式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如替换查询节点可能改变所有下游输入，虽然只动一个节点，也应验证依赖它的路线是否保持可用。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09153">原论文</a> · <a href="../../../../agent-research/2609.09153-procedural-graphs/">实现解读</a> · <a href="#qa-36893bcf703a5f2a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:procedural-graphs" data-paper-title="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Procedural Graphs: Self-Evolving Execution Structures for LLM Agents Agent Google 2026-09-08 方法把成功经验从自然语言片段提升为 procedure–relation–procedure 图。新经验先局部化为候选图编辑，再经过 held-out 验证门才写入长期结构，减少错误经验污染。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现 procedure–relation–procedure 图和保守编辑门，不包含 LLM 生成或真实环境执行。三种子 evomem-mini 结果见 metrics/mini-suite-seeds42-44.json。本地编辑门以“已建立路线必须保留首尾节点”为确定性代理；策略看不到隐藏答案/计划，也未调用真实工具，因此仅验证图更新与拒绝路径。  自进化程序图 Agent 运行流程与自进化：改的是哪一层 本地首尾节点保护能否当作完整 held-out 能力验证？ 不能。本地以既有路线首尾必须保留作为确定性编辑门，验证图更新与拒绝路径，不调用真实工具。该代理只保留结构条件，无法证明中间步骤语义正确或新图泛化，策略仍不得看到隐藏计划和答案。 例如保住起点终点却删除必需认证步骤仍可能结构过门，说明该合同不能替代实际任务成功判定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f6396bb67c386274">本地首尾节点保护能否当作完整 held-out 能力验证？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprocedural-graphs">Procedural Graphs: Self-Evolving Execution Structures for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地以既有路线首尾必须保留作为确定性编辑门，验证图更新与拒绝路径，不调用真实工具。该代理只保留结构条件，无法证明中间步骤语义正确或新图泛化，策略仍不得看到隐藏计划和答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保住起点终点却删除必需认证步骤仍可能结构过门，说明该合同不能替代实际任务成功判定。</p>
<p class="ar-learning-sources">依据：本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09153">原论文</a> · <a href="../../../../agent-research/2609.09153-procedural-graphs/">实现解读</a> · <a href="#qa-f6396bb67c386274">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnesslens" data-paper-title="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification Agent Fudan University 2026-08-27 固定验证集浪费 rollout 且会用平均分掩盖局部回退。HarnessLens 从执行轨迹提出修改，只在受影响行为对应的任务上成对验证，并要求证据能归因到候选修改。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现行为任务选择、配对验证与可归因证据门。未运行论文四个完整 benchmark；本地执行冻结测试集和无 answer/guide 接口的真实工具反馈协议。ToolRoute-L2.1 三 seed：joint success 0.8194，plan F1 0.8372，平均成本 5.0419。  行为相关 Harness 验证 Agent 运行流程与自进化：改的是哪一层 HarnessLens 为什么把验证成本本身当作 harness 搜索的瓶颈？ 每个候选都完整运行固定验证集会消耗大量 rollout，而整体平均值又可能掩盖少数受影响行为的退化。HarnessLens 研究让验证关注修改实际触及的行为，以有限预算获得更有针对性的证据。局部检查需说明覆盖边界，不能因节省评测就跳过归因或扩大质量结论。 教学例：只改浏览恢复逻辑，却把全部无关计算题重跑一遍可能浪费；应找到对应行为任务，但仍需承认其他行为未被新证据覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-harnesslens-7d46fb0d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1bd6146aa60c6f88">HarnessLens 为什么把验证成本本身当作 harness 搜索的瓶颈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnesslens">Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个候选都完整运行固定验证集会消耗大量 rollout，而整体平均值又可能掩盖少数受影响行为的退化。HarnessLens 研究让验证关注修改实际触及的行为，以有限预算获得更有针对性的证据。局部检查需说明覆盖边界，不能因节省评测就跳过归因或扩大质量结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：只改浏览恢复逻辑，却把全部无关计算题重跑一遍可能浪费；应找到对应行为任务，但仍需承认其他行为未被新证据覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27311">原论文</a> · <a href="../../../../agent-research/2608.27311-harnesslens/">实现解读</a> · <a href="#qa-1bd6146aa60c6f88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnesslens" data-paper-title="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification Agent Fudan University 2026-08-27 固定验证集浪费 rollout 且会用平均分掩盖局部回退。HarnessLens 从执行轨迹提出修改，只在受影响行为对应的任务上成对验证，并要求证据能归因到候选修改。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现行为任务选择、配对验证与可归因证据门。未运行论文四个完整 benchmark；本地执行冻结测试集和无 answer/guide 接口的真实工具反馈协议。ToolRoute-L2.1 三 seed：joint success 0.8194，plan F1 0.8372，平均成本 5.0419。  行为相关 Harness 验证 Agent 运行流程与自进化：改的是哪一层 行为感知的成对验证为什么比固定验证集平均分更能发现局部回退？ 修改只影响部分行为，混入大量无关题会稀释差异并浪费 rollout。针对受影响任务比较父子框架，要求变化可归因于该修改，才能辨别真正修复与偶然波动；局部通过仍需明确适用范围，不能从一个行为提升推导全部任务均变好。 例如只改重试组件，应配对检查超时和恢复任务；大量简单成功题可能把某个重试死循环的退化淹没在平均分里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnesslens" data-paper-title="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification Agent Fudan University 2026-08-27 固定验证集浪费 rollout 且会用平均分掩盖局部回退。HarnessLens 从执行轨迹提出修改，只在受影响行为对应的任务上成对验证，并要求证据能归因到候选修改。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现行为任务选择、配对验证与可归因证据门。未运行论文四个完整 benchmark；本地执行冻结测试集和无 answer/guide 接口的真实工具反馈协议。ToolRoute-L2.1 三 seed：joint success 0.8194，plan F1 0.8372，平均成本 5.0419。  行为相关 Harness 验证 Agent 运行流程与自进化：改的是哪一层 通过局部行为接纳门，与证明整个 Agent 能力提升，证据范围有何差别？ 局部门要求目标行为的配对增益为正且可归因，回答这次改动在所选行为上是否值得接纳；整体能力还涉及未覆盖任务、其他行为及资源影响。Δ_b 与 A_b 不能自动外推到所有任务。应同时保留验证集合和修改作用域，而非把局部通过改名为全面能力验证。 教学例：恢复任务五个样例改善，能支持这类改动的有限接纳；不能直接声称代码生成、数学和所有浏览任务都变好了。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1fec5db47abd72cf">通过局部行为接纳门，与证明整个 Agent 能力提升，证据范围有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnesslens">Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部门要求目标行为的配对增益为正且可归因，回答这次改动在所选行为上是否值得接纳；整体能力还涉及未覆盖任务、其他行为及资源影响。Δ_b 与 A_b 不能自动外推到所有任务。应同时保留验证集合和修改作用域，而非把局部通过改名为全面能力验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：恢复任务五个样例改善，能支持这类改动的有限接纳；不能直接声称代码生成、数学和所有浏览任务都变好了。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27311">原论文</a> · <a href="../../../../agent-research/2608.27311-harnesslens/">实现解读</a> · <a href="#qa-1fec5db47abd72cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnesslens" data-paper-title="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification Agent Fudan University 2026-08-27 固定验证集浪费 rollout 且会用平均分掩盖局部回退。HarnessLens 从执行轨迹提出修改，只在受影响行为对应的任务上成对验证，并要求证据能归因到候选修改。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现行为任务选择、配对验证与可归因证据门。未运行论文四个完整 benchmark；本地执行冻结测试集和无 answer/guide 接口的真实工具反馈协议。ToolRoute-L2.1 三 seed：joint success 0.8194，plan F1 0.8372，平均成本 5.0419。  行为相关 Harness 验证 Agent 运行流程与自进化：改的是哪一层 Δ_b&gt;0 之外的 A_b 条件为什么不能省略？ 正差可能来自随机重试或环境变化，A_b 要求改善证据可归因到候选。当前本地有无 answer/guide 的真实工具反馈协议，但未运行论文四个完整 benchmark；本地成功率不能替代原文 held-out 提升，结构标签也不自动证明因果。 例如两次运行随机结果不同，若未检查候选行为是否实际触发，就不能把这次正差全归给补丁。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-aad409452ebef205">Δ_b&gt;0 之外的 A_b 条件为什么不能省略？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnesslens">Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正差可能来自随机重试或环境变化，A_b 要求改善证据可归因到候选。当前本地有无 answer/guide 的真实工具反馈协议，但未运行论文四个完整 benchmark；本地成功率不能替代原文 held-out 提升，结构标签也不自动证明因果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次运行随机结果不同，若未检查候选行为是否实际触发，就不能把这次正差全归给补丁。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27311">原论文</a> · <a href="../../../../agent-research/2608.27311-harnesslens/">实现解读</a> · <a href="#qa-aad409452ebef205">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jit-agent" data-paper-title="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution Agent LV-NUS Lab 2026-08-26 把 harness 形式化为 memory、planning、action protocol、tools/skills 四个可生成模块；模型按任务生成、失败后修复，并从历史配置 archive 蒸馏可迁移模式。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。JIT harness 在训练任务上即时写入/修复可复用路由，在 validation/test 冻结后仅通过公开 observation、工具元数据和真实调用反馈执行；不存在 answer、guide 或 reference-plan 接口。  Harness 即时生成与进化 Agent 运行流程与自进化：改的是哪一层 Jit-Agent 为什么希望根据当前任务生成工作流程，而不只选择固定提示？ 任务对记忆、规划、动作协议和工具的需求不同，一套通用 harness 可能过重或缺少关键支持。Jit-Agent 研究在任务到来时组合相应工作方式，让外部组织更贴近需求。即时生成仍需要质量约束和冻结评测，不能因为模块齐全就认为所得 Agent 一定胜过固定流程。 教学例：单步计算不一定需要长期记忆，而多页资料整理可能需要取证与进度管理；任务特征应影响使用哪些模块。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-jit-agent-92c11b63" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-22c8f75c233ddfc6">Jit-Agent 为什么希望根据当前任务生成工作流程，而不只选择固定提示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajit-agent">JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LV-NUS Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务对记忆、规划、动作协议和工具的需求不同，一套通用 harness 可能过重或缺少关键支持。Jit-Agent 研究在任务到来时组合相应工作方式，让外部组织更贴近需求。即时生成仍需要质量约束和冻结评测，不能因为模块齐全就认为所得 Agent 一定胜过固定流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：单步计算不一定需要长期记忆，而多页资料整理可能需要取证与进度管理；任务特征应影响使用哪些模块。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25593">原论文</a> · <a href="../../../../agent-research/2608.25593-jit-agent/">实现解读</a> · <a href="#qa-22c8f75c233ddfc6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jit-agent" data-paper-title="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution Agent LV-NUS Lab 2026-08-26 把 harness 形式化为 memory、planning、action protocol、tools/skills 四个可生成模块；模型按任务生成、失败后修复，并从历史配置 archive 蒸馏可迁移模式。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。JIT harness 在训练任务上即时写入/修复可复用路由，在 validation/test 冻结后仅通过公开 observation、工具元数据和真实调用反馈执行；不存在 answer、guide 或 reference-plan 接口。  Harness 即时生成与进化 Agent 运行流程与自进化：改的是哪一层 为什么按任务生成 harness 时，要把 memory、planning、action protocol、tools 分成模块？ 不同任务瓶颈可能位于不同层，模块化让生成与失败修复定位具体对象，也便于从配置档案提炼可迁移模式。即用即生成不等于无需验证，每个模块仍要满足运行合同；仅改提示内容却未生成相应工具或状态接口，不能算四模块都已实现。 例如长任务需要换记忆策略、短计算题只需配置计算工具，不必每次重建全部组件，也不能让两者混用不兼容协议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jit-agent" data-paper-title="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution Agent LV-NUS Lab 2026-08-26 把 harness 形式化为 memory、planning、action protocol、tools/skills 四个可生成模块；模型按任务生成、失败后修复，并从历史配置 archive 蒸馏可迁移模式。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。JIT harness 在训练任务上即时写入/修复可复用路由，在 validation/test 冻结后仅通过公开 observation、工具元数据和真实调用反馈执行；不存在 answer、guide 或 reference-plan 接口。  Harness 即时生成与进化 Agent 运行流程与自进化：改的是哪一层 按任务即时生成与复用固定单一 harness 有何取舍？ 即时配置可适应不同任务需求，archive 还能帮助迁移，但生成与修复增加开发成本并可能引入不稳定。固定框架更容易维护却可能过于通用；比较需计入候选生成和实际失败，不能只挑最终成功配置忽略探索费用。 例如长检索任务需要引用核查，简单计算未必需要，按任务生成可区分；但无用核查器也可能拖慢简单任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e2cd81f241f4787f">按任务即时生成与复用固定单一 harness 有何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajit-agent">JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LV-NUS Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>即时配置可适应不同任务需求，archive 还能帮助迁移，但生成与修复增加开发成本并可能引入不稳定。固定框架更容易维护却可能过于通用；比较需计入候选生成和实际失败，不能只挑最终成功配置忽略探索费用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长检索任务需要引用核查，简单计算未必需要，按任务生成可区分；但无用核查器也可能拖慢简单任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25593">原论文</a> · <a href="../../../../agent-research/2608.25593-jit-agent/">实现解读</a> · <a href="#qa-e2cd81f241f4787f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jit-agent" data-paper-title="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution Agent LV-NUS Lab 2026-08-26 把 harness 形式化为 memory、planning、action protocol、tools/skills 四个可生成模块；模型按任务生成、失败后修复，并从历史配置 archive 蒸馏可迁移模式。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。JIT harness 在训练任务上即时写入/修复可复用路由，在 validation/test 冻结后仅通过公开 observation、工具元数据和真实调用反馈执行；不存在 answer、guide 或 reference-plan 接口。  Harness 即时生成与进化 Agent 运行流程与自进化：改的是哪一层 本地训练期修路由与 test 冻结执行为什么要分开？ 训练任务可写入修复经验，validation/test 冻结后只凭公开观察、工具元数据和真实反馈行动，不能读取答案或 reference-plan。受控低成功率及真实 ToolRoute 结果应各按协议报告，没有原模型与完整 DeepSearchQA 就不能移用作者分数。 例如 test 看到报错可按已冻结规则恢复，但不能把隐藏正确路线写入 archive 后再说即时适配成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7b9656fc577d1bd9">本地训练期修路由与 test 冻结执行为什么要分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajit-agent">JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LV-NUS Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练任务可写入修复经验，validation/test 冻结后只凭公开观察、工具元数据和真实反馈行动，不能读取答案或 reference-plan。受控低成功率及真实 ToolRoute 结果应各按协议报告，没有原模型与完整 DeepSearchQA 就不能移用作者分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 test 看到报错可按已冻结规则恢复，但不能把隐藏正确路线写入 archive 后再说即时适配成功。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25593">原论文</a> · <a href="../../../../agent-research/2608.25593-jit-agent/">实现解读</a> · <a href="#qa-7b9656fc577d1bd9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openloopevolve" data-paper-title="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks Agent Tsinghua University 2026-08-10 把 observation/planning/memory/action/verification/recovery 等 Loop Policy 资产版本化，以 Champion–Challenger、发布监控和回滚治理进化。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  自进化 策略治理 Agent 运行流程与自进化：改的是哪一层 Loop Policy 为什么不仅是一段 system prompt？ 观察、规划、记忆、行动、验证与恢复等资产共同决定长程行为，版本化需覆盖这些组件及其组合。只改提示可能漏掉真正瓶颈，只有保存可执行版本、比较并监控，才可追踪进化；资产文件齐全也不等于其行为有效。 例如提示要求“失败后重试”，若工具恢复中间件仍不能辨认超时，实际循环未必具备有效恢复能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-openloopevolve-709aab65" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4968c00f9e6ec87b">Loop Policy 为什么不仅是一段 system prompt？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aopenloopevolve">OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>观察、规划、记忆、行动、验证与恢复等资产共同决定长程行为，版本化需覆盖这些组件及其组合。只改提示可能漏掉真正瓶颈，只有保存可执行版本、比较并监控，才可追踪进化；资产文件齐全也不等于其行为有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如提示要求“失败后重试”，若工具恢复中间件仍不能辨认超时，实际循环未必具备有效恢复能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09380">原论文</a> · <a href="../../../../agent-research/2608.09380-openloopevolve/">实现解读</a> · <a href="#qa-4968c00f9e6ec87b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openloopevolve" data-paper-title="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks Agent Tsinghua University 2026-08-10 把 observation/planning/memory/action/verification/recovery 等 Loop Policy 资产版本化，以 Champion–Challenger、发布监控和回滚治理进化。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  自进化 策略治理 Agent 运行流程与自进化：改的是哪一层 Champion–Challenger 之外，为什么还需要发布监控与回滚？ 离线候选优于冠军不保证上线分布和长期交互同样稳定，监控发现新退化后需要可追溯地恢复旧版本。版本化涵盖观察、规划、记忆、验证和恢复等资产，避免只记录模型名；发布治理是进化闭环的一部分，不能以候选评测一次通过替代。 例如挑战者在开发任务更省调用，上线却在权限错误时循环，监控应定位版本并回滚到旧策略，而不是继续无界试错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openloopevolve" data-paper-title="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks Agent Tsinghua University 2026-08-10 把 observation/planning/memory/action/verification/recovery 等 Loop Policy 资产版本化，以 Champion–Challenger、发布监控和回滚治理进化。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  自进化 策略治理 Agent 运行流程与自进化：改的是哪一层 Champion–Challenger 与每轮直接覆盖当前策略有什么区别？ 保留 champion 作为已验基线，challenger 经过比较再发布，并在运行监控中必要时回滚，减少未经验证改动长期污染。发布门需要实际评价与版本证据，不能把候选自评更好当接纳，线上监控也不等于自动允许任何外部部署。 例如新恢复策略在验证好但上线后出现新退化，应能恢复具体旧版本，而不是只剩一份被覆盖的配置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8f8d343b5c61d073">Champion–Challenger 与每轮直接覆盖当前策略有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aopenloopevolve">OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>保留 champion 作为已验基线，challenger 经过比较再发布，并在运行监控中必要时回滚，减少未经验证改动长期污染。发布门需要实际评价与版本证据，不能把候选自评更好当接纳，线上监控也不等于自动允许任何外部部署。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新恢复策略在验证好但上线后出现新退化，应能恢复具体旧版本，而不是只剩一份被覆盖的配置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09380">原论文</a> · <a href="../../../../agent-research/2608.09380-openloopevolve/">实现解读</a> · <a href="#qa-8f8d343b5c61d073">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openloopevolve" data-paper-title="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks Agent Tsinghua University 2026-08-10 把 observation/planning/memory/action/verification/recovery 等 Loop Policy 资产版本化，以 Champion–Challenger、发布监控和回滚治理进化。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  自进化 策略治理 Agent 运行流程与自进化：改的是哪一层 本地版本和回滚状态是否已证明真实长期在线自演化？ 没有。本地确定性 PlanBench 只验证机制分支、版本状态与报告，没有真实浏览器、服务或 YC-Bench。代理成本、发布标志和回滚次数是控制证据，不是线上风险或成功率，原文 online/offline 结果不能直接搬成当前实测。 例如状态从 challenger 变 champion 可由规则触发，若未实际跑模型和工具，不能宣称已发布更强 Agent。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a5becae453b70928">本地版本和回滚状态是否已证明真实长期在线自演化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aopenloopevolve">OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地确定性 PlanBench 只验证机制分支、版本状态与报告，没有真实浏览器、服务或 YC-Bench。代理成本、发布标志和回滚次数是控制证据，不是线上风险或成功率，原文 online/offline 结果不能直接搬成当前实测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如状态从 challenger 变 champion 可由规则触发，若未实际跑模型和工具，不能宣称已发布更强 Agent。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09380">原论文</a> · <a href="../../../../agent-research/2608.09380-openloopevolve/">实现解读</a> · <a href="#qa-a5becae453b70928">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx" data-paper-title="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems Agent Kuaishou 2026-06-26 传统推荐迭代需要工程师串联假设、生产代码、上线 A/B 和归因，经验也难以跨实验积累。AgentX 将流程改造成四阶段闭环：Brainstorm Agent 从实验库、系统知识、数据分析和外部论文生成有证据的候选；Developing Agent 在仓库约束下实现并验证；Evaluation Agent 用护栏否决的线上 A/B 判断；最后以 SGPO 从成功与失败轨迹更新 Agent harness。 复现级别：核心闭环 mini-suite。复现级别：核心闭环 mini-suite。本地实现 Brainstorm、Developing、Evaluation 与 Harness Evolution 四阶段控制流，并验证实验知识复用带来的执行成本下降。本地没有 Kuaishou 内部仓库、流量平台、线上用户或 SGPO 大模型训练，因此不能复现论文的业务增益。mini-suite 验证的是四阶段闭环、正负结果资产化、验证门槛与跨 episode 复用；average proxy cost 仅是控制流成本，不冒充人效、收入或线上时长。  研究自动化 工业推荐 Agent Agent 运行流程与自进化：改的是哪一层 四阶段闭环为什么让失败轨迹也进入实验知识库？ 失败可说明实现限制、护栏风险和不成立假设，帮助后续提案避免重复；只收成功会产生幸存者偏差。Brainstorm、Developing、Evaluation 与 SGPO 分工串联证据、代码、线上验证及经验更新，仍需区分作者生产系统与本地控制流。 例如某特征离线涨分却线上伤害延迟，记录失败及条件可防下一轮再次提出同样高风险方案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-agentx-26ba162a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2476b944234ef8ff">四阶段闭环为什么让失败轨迹也进入实验知识库？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentx">AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>失败可说明实现限制、护栏风险和不成立假设，帮助后续提案避免重复；只收成功会产生幸存者偏差。Brainstorm、Developing、Evaluation 与 SGPO 分工串联证据、代码、线上验证及经验更新，仍需区分作者生产系统与本地控制流。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某特征离线涨分却线上伤害延迟，记录失败及条件可防下一轮再次提出同样高风险方案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.26859">原论文</a> · <a href="../../../../agent-research/2606.26859-agentx/">实现解读</a> · <a href="#qa-2476b944234ef8ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx" data-paper-title="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems Agent Kuaishou 2026-06-26 传统推荐迭代需要工程师串联假设、生产代码、上线 A/B 和归因，经验也难以跨实验积累。AgentX 将流程改造成四阶段闭环：Brainstorm Agent 从实验库、系统知识、数据分析和外部论文生成有证据的候选；Developing Agent 在仓库约束下实现并验证；Evaluation Agent 用护栏否决的线上 A/B 判断；最后以 SGPO 从成功与失败轨迹更新 Agent harness。 复现级别：核心闭环 mini-suite。复现级别：核心闭环 mini-suite。本地实现 Brainstorm、Developing、Evaluation 与 Harness Evolution 四阶段控制流，并验证实验知识复用带来的执行成本下降。本地没有 Kuaishou 内部仓库、流量平台、线上用户或 SGPO 大模型训练，因此不能复现论文的业务增益。mini-suite 验证的是四阶段闭环、正负结果资产化、验证门槛与跨 episode 复用；average proxy cost 仅是控制流成本，不冒充人效、收入或线上时长。  研究自动化 工业推荐 Agent Agent 运行流程与自进化：改的是哪一层 主指标显著改善后，为什么护栏越界仍能否决候选发布？ 推荐系统需要在目标收益与关键约束之间满足共同条件，单指标上涨可能以稳定性或其他重要体验为代价。Evaluation Agent 用线上证据和护栏否决，成功失败都写回实验知识；harness 学习依据完整轨迹，而不是只筛赢家形成乐观偏差。 例如点击率提高却导致关键时延明显越界，不能只拿上涨指标宣称可上线；失败原因也应进入下一轮提案证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx" data-paper-title="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems Agent Kuaishou 2026-06-26 传统推荐迭代需要工程师串联假设、生产代码、上线 A/B 和归因，经验也难以跨实验积累。AgentX 将流程改造成四阶段闭环：Brainstorm Agent 从实验库、系统知识、数据分析和外部论文生成有证据的候选；Developing Agent 在仓库约束下实现并验证；Evaluation Agent 用护栏否决的线上 A/B 判断；最后以 SGPO 从成功与失败轨迹更新 Agent harness。 复现级别：核心闭环 mini-suite。复现级别：核心闭环 mini-suite。本地实现 Brainstorm、Developing、Evaluation 与 Harness Evolution 四阶段控制流，并验证实验知识复用带来的执行成本下降。本地没有 Kuaishou 内部仓库、流量平台、线上用户或 SGPO 大模型训练，因此不能复现论文的业务增益。mini-suite 验证的是四阶段闭环、正负结果资产化、验证门槛与跨 episode 复用；average proxy cost 仅是控制流成本，不冒充人效、收入或线上时长。  研究自动化 工业推荐 Agent Agent 运行流程与自进化：改的是哪一层 离线实现验证与生产线上 A/B，在 AgentX 中分别支持什么结论？ 离线检查能发现代码、数据和运行合同问题，为进入安全流量提供准备；线上 A/B 才观察业务环境中主指标及护栏的变化。二者任务和风险口径不同，离线通过不能替代线上发布判定。作者生产证据也不能由本地小型 episode 或更新计数冒充。 教学例：推荐代码通过单元测试，仅说明实现可进入后续实验；是否改善用户行为且不损害延迟，还需对应流量下的对照。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-594ae560d1f3665d">离线实现验证与生产线上 A/B，在 AgentX 中分别支持什么结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentx">AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线检查能发现代码、数据和运行合同问题，为进入安全流量提供准备；线上 A/B 才观察业务环境中主指标及护栏的变化。二者任务和风险口径不同，离线通过不能替代线上发布判定。作者生产证据也不能由本地小型 episode 或更新计数冒充。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：推荐代码通过单元测试，仅说明实现可进入后续实验；是否改善用户行为且不损害延迟，还需对应流量下的对照。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.26859">原论文</a> · <a href="../../../../agent-research/2606.26859-agentx/">实现解读</a> · <a href="#qa-594ae560d1f3665d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentx" data-paper-title="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems Agent Kuaishou 2026-06-26 传统推荐迭代需要工程师串联假设、生产代码、上线 A/B 和归因，经验也难以跨实验积累。AgentX 将流程改造成四阶段闭环：Brainstorm Agent 从实验库、系统知识、数据分析和外部论文生成有证据的候选；Developing Agent 在仓库约束下实现并验证；Evaluation Agent 用护栏否决的线上 A/B 判断；最后以 SGPO 从成功与失败轨迹更新 Agent harness。 复现级别：核心闭环 mini-suite。复现级别：核心闭环 mini-suite。本地实现 Brainstorm、Developing、Evaluation 与 Harness Evolution 四阶段控制流，并验证实验知识复用带来的执行成本下降。本地没有 Kuaishou 内部仓库、流量平台、线上用户或 SGPO 大模型训练，因此不能复现论文的业务增益。mini-suite 验证的是四阶段闭环、正负结果资产化、验证门槛与跨 episode 复用；average proxy cost 仅是控制流成本，不冒充人效、收入或线上时长。  研究自动化 工业推荐 Agent Agent 运行流程与自进化：改的是哪一层 本地 120 个 episode 的 policy update 计数能说明 SGPO 大模型训练吗？ 不能。本地验证四阶段、资产化和复用状态，没有快手仓库、用户流量或 SGPO 训练。average proxy cost 不是人效、收入或用户时长；原文上线收益属作者证据，不能用确定性满分声称复刻工业推荐系统迭代。 例如实验知识复用一百零八次是本地流程计数，没有真实 A/B 就不能将它换算成年化收入或生产业务价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-296e78851537b605">本地 120 个 episode 的 policy update 计数能说明 SGPO 大模型训练吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentx">AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地验证四阶段、资产化和复用状态，没有快手仓库、用户流量或 SGPO 训练。average proxy cost 不是人效、收入或用户时长；原文上线收益属作者证据，不能用确定性满分声称复刻工业推荐系统迭代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如实验知识复用一百零八次是本地流程计数，没有真实 A/B 就不能将它换算成年化收入或生产业务价值。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.26859">原论文</a> · <a href="../../../../agent-research/2606.26859-agentx/">实现解读</a> · <a href="#qa-296e78851537b605">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scientist-one" data-paper-title="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence Agent Google Cloud AI Research 2026-05-25 研究产物看起来完整，仍可能引用虚构、分数无法复算或方法描述与代码不同。CoE 将主张连到可核验来源；独立 I1–I4 检查分数、规则、引用和方法/代码一致性。来源存在不等于主张被支持。原文 §3 与 §5 完整实验成本过高，不复现（审查 DONE）。本地实现低成本 CoE 机械核验内核与语义审计接口，不是完整自主科学家。固定刺激为 L0；完整实验成本过高，不复现（审查 DONE）。canonical evaluator 的可信性、日志是否由实际实验产生、语义判断是否正确仍由上层证据保障；哈希只能证明“相同字节”，不能证明“字节描述了真实实验”。本地不将任意 Python callback 当安全沙箱。  科学研究 Agent 证据链与完整性审计 Agent 运行流程与自进化：改的是哪一层 Scientist-One 为什么要让研究主张能被独立追溯和重新核查？ 自动研究可生成许多代码、图表和结论，但报告中的数字可能缺少真实执行或与来源口径不一致。Scientist-One 研究把主张、证据与执行记录连接起来，使读者能检查结论从何而来。证据链存在只是审计入口，仍需核对内容、单位和实验阶段，不能用哈希代替真实性。 教学例：报告写准确率提升，应能追到对应数据划分与运行结果；找到一个有哈希的文件，并不能证明里面记录的是准确率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-scientist-one-ba34af9f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0de4476b19cd6939">Scientist-One 为什么要让研究主张能被独立追溯和重新核查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascientist-one">ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自动研究可生成许多代码、图表和结论，但报告中的数字可能缺少真实执行或与来源口径不一致。Scientist-One 研究把主张、证据与执行记录连接起来，使读者能检查结论从何而来。证据链存在只是审计入口，仍需核对内容、单位和实验阶段，不能用哈希代替真实性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：报告写准确率提升，应能追到对应数据划分与运行结果；找到一个有哈希的文件，并不能证明里面记录的是准确率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26340">原论文</a> · <a href="../../../../agent-research/2605.26340-scientist-one/">实现解读</a> · <a href="#qa-0de4476b19cd6939">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scientist-one" data-paper-title="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence Agent Google Cloud AI Research 2026-05-25 研究产物看起来完整，仍可能引用虚构、分数无法复算或方法描述与代码不同。CoE 将主张连到可核验来源；独立 I1–I4 检查分数、规则、引用和方法/代码一致性。来源存在不等于主张被支持。原文 §3 与 §5 完整实验成本过高，不复现（审查 DONE）。本地实现低成本 CoE 机械核验内核与语义审计接口，不是完整自主科学家。固定刺激为 L0；完整实验成本过高，不复现（审查 DONE）。canonical evaluator 的可信性、日志是否由实际实验产生、语义判断是否正确仍由上层证据保障；哈希只能证明“相同字节”，不能证明“字节描述了真实实验”。本地不将任意 Python callback 当安全沙箱。  科学研究 Agent 证据链与完整性审计 Agent 运行流程与自进化：改的是哪一层 来源和日志都存在，为什么还要核对 metric、stage、unit 与 direction？ 同一日志可能同时含训练、消融和正式评测，多种数值不能互相替代。主张需连到身份和口径一致的证据，再检查可复算性与方法代码一致性；没有定量主张时溯源率应为空而非满分，来源存在本身也不证明它支持文本结论。 例如日志记录的是训练 loss 下降，报告却写测试准确率提高，即使数字可追溯也不算主张获得对应证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scientist-one" data-paper-title="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence Agent Google Cloud AI Research 2026-05-25 研究产物看起来完整，仍可能引用虚构、分数无法复算或方法描述与代码不同。CoE 将主张连到可核验来源；独立 I1–I4 检查分数、规则、引用和方法/代码一致性。来源存在不等于主张被支持。原文 §3 与 §5 完整实验成本过高，不复现（审查 DONE）。本地实现低成本 CoE 机械核验内核与语义审计接口，不是完整自主科学家。固定刺激为 L0；完整实验成本过高，不复现（审查 DONE）。canonical evaluator 的可信性、日志是否由实际实验产生、语义判断是否正确仍由上层证据保障；哈希只能证明“相同字节”，不能证明“字节描述了真实实验”。本地不将任意 Python callback 当安全沙箱。  科学研究 Agent 证据链与完整性审计 Agent 运行流程与自进化：改的是哪一层 数值 CPR 与学术引用真实性为什么是不同问题？ CPR 检查定量主张能否追溯到数值匹配的执行日志，还要求 metric、stage、unit 和方向一致；引用核验另需检索与语义消歧。数值对应可能正确但引用虚构，真实论文也可能不支持当前断言，两个检查不能互相代替。 例如日志中的训练 loss 不能拿来支持 test accuracy，即使数值恰好相同；存在一篇同名论文也不证明它说过该结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4d5ea75c7583ba81">数值 CPR 与学术引用真实性为什么是不同问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascientist-one">ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CPR 检查定量主张能否追溯到数值匹配的执行日志，还要求 metric、stage、unit 和方向一致；引用核验另需检索与语义消歧。数值对应可能正确但引用虚构，真实论文也可能不支持当前断言，两个检查不能互相代替。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如日志中的训练 loss 不能拿来支持 test accuracy，即使数值恰好相同；存在一篇同名论文也不证明它说过该结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26340">原论文</a> · <a href="../../../../agent-research/2605.26340-scientist-one/">实现解读</a> · <a href="#qa-4d5ea75c7583ba81">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scientist-one" data-paper-title="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence Agent Google Cloud AI Research 2026-05-25 研究产物看起来完整，仍可能引用虚构、分数无法复算或方法描述与代码不同。CoE 将主张连到可核验来源；独立 I1–I4 检查分数、规则、引用和方法/代码一致性。来源存在不等于主张被支持。原文 §3 与 §5 完整实验成本过高，不复现（审查 DONE）。本地实现低成本 CoE 机械核验内核与语义审计接口，不是完整自主科学家。固定刺激为 L0；完整实验成本过高，不复现（审查 DONE）。canonical evaluator 的可信性、日志是否由实际实验产生、语义判断是否正确仍由上层证据保障；哈希只能证明“相同字节”，不能证明“字节描述了真实实验”。本地不将任意 Python callback 当安全沙箱。  科学研究 Agent 证据链与完整性审计 Agent 运行流程与自进化：改的是哪一层 五次复算零均值、无定量主张和投票平局该怎样处理？ 零均值且确定时要求报告精确零，不加宽松 ε；没有定量主张 CPR 为 null，不是满分；无多数或弃权保留 unverified。I1 用总体标准差容差，可信 evaluator 和日志来源仍由上层保障，本地 fixture 未验证整篇研究。 例如一篇没有任何数字的稿件不能因分母为零得到 CPR=1，两个审查者意见相反也不能默认多数通过。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-79ed0d4a52806e10">五次复算零均值、无定量主张和投票平局该怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascientist-one">ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>零均值且确定时要求报告精确零，不加宽松 ε；没有定量主张 CPR 为 null，不是满分；无多数或弃权保留 unverified。I1 用总体标准差容差，可信 evaluator 和日志来源仍由上层保障，本地 fixture 未验证整篇研究。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一篇没有任何数字的稿件不能因分母为零得到 CPR=1，两个审查者意见相反也不能默认多数通过。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26340">原论文</a> · <a href="../../../../agent-research/2605.26340-scientist-one/">实现解读</a> · <a href="#qa-79ed0d4a52806e10">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagents" data-paper-title="HyperAgents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HyperAgents Agent University of British Columbia 2026-03-19 把任务 Agent 与修改它的 meta Agent 放入同一可编辑程序，并在开放档案中积累变体；父代概率同时奖励当前性能与较少后代的探索价值，使改进机制本身也可继续被改进。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。三种子诊断：metrics/mechanism-seeds42-44.json  RSI 开放式进化 元认知自修改 Agent 运行流程与自进化：改的是哪一层 HyperAgents 为什么不仅改任务解法，还允许改“生成下一版解法”的程序？ 固定改进器会持续沿同一套提案和反思方式搜索，它自身的限制可能阻碍后续进步。HyperAgents 把任务程序与 meta 程序一起纳入可编辑对象，研究改进方法能否随经验演化。自改代码增加了验证难度，档案里出现新版本不等于真实性能或长期进步已得到证明。 教学例：某版本总提出相似改动，可以尝试修改提案器本身；之后仍要验证新提案器是否真的带来更有效候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-hyperagents-ae71283f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-42342c52c5c76f30">HyperAgents 为什么不仅改任务解法，还允许改“生成下一版解法”的程序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahyperagents">HyperAgents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of British Columbia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定改进器会持续沿同一套提案和反思方式搜索，它自身的限制可能阻碍后续进步。HyperAgents 把任务程序与 meta 程序一起纳入可编辑对象，研究改进方法能否随经验演化。自改代码增加了验证难度，档案里出现新版本不等于真实性能或长期进步已得到证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：某版本总提出相似改动，可以尝试修改提案器本身；之后仍要验证新提案器是否真的带来更有效候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19461">原论文</a> · <a href="../../../../agent-research/2603.19461-hyperagents/">实现解读</a> · <a href="#qa-42342c52c5c76f30">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagents" data-paper-title="HyperAgents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HyperAgents Agent University of British Columbia 2026-03-19 把任务 Agent 与修改它的 meta Agent 放入同一可编辑程序，并在开放档案中积累变体；父代概率同时奖励当前性能与较少后代的探索价值，使改进机制本身也可继续被改进。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。三种子诊断：metrics/mechanism-seeds42-44.json  RSI 开放式进化 元认知自修改 Agent 运行流程与自进化：改的是哪一层 父代抽样为什么同时考虑性能和已有后代数？ 只追最高分容易反复扩展同一分支，降低探索多样性；后代数惩罚给较少探索的可行父本机会。任务 Agent 与修改机制都在可编辑程序里，让改进方式本身也能演化；抽样概率只是预算分配，不代表每个后代被接受或性能必然递增。 例如冠军已有二十个子版本，稍弱但只试过一次的父本可获得更多机会，可能发现不同的改进路径而非一直局部打磨。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagents" data-paper-title="HyperAgents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HyperAgents Agent University of British Columbia 2026-03-19 把任务 Agent 与修改它的 meta Agent 放入同一可编辑程序，并在开放档案中积累变体；父代概率同时奖励当前性能与较少后代的探索价值，使改进机制本身也可继续被改进。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。三种子诊断：metrics/mechanism-seeds42-44.json  RSI 开放式进化 元认知自修改 Agent 运行流程与自进化：改的是哪一层 固定 meta Agent 的程序搜索，与允许 meta Agent 一起被编辑，有何搜索范围差异？ 固定改进器只在任务解法空间内生成变体，允许编辑 meta Agent 则还可改变候选生成和改进流程，扩大搜索对象。更大空间也带来失效与归因困难，需要分别执行和评价新程序。当前本地 archive 操作不生成或运行任意源码，不能用档案谱系冒充完整程序自修改。 教学例：只改排序函数属于任务层；把“如何选择待试函数”的策略也改写，才涉及 meta 层，但新增自由度未必自动有效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a6ebd187b8938135">固定 meta Agent 的程序搜索，与允许 meta Agent 一起被编辑，有何搜索范围差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahyperagents">HyperAgents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of British Columbia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定改进器只在任务解法空间内生成变体，允许编辑 meta Agent 则还可改变候选生成和改进流程，扩大搜索对象。更大空间也带来失效与归因困难，需要分别执行和评价新程序。当前本地 archive 操作不生成或运行任意源码，不能用档案谱系冒充完整程序自修改。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：只改排序函数属于任务层；把“如何选择待试函数”的策略也改写，才涉及 meta 层，但新增自由度未必自动有效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19461">原论文</a> · <a href="../../../../agent-research/2603.19461-hyperagents/">实现解读</a> · <a href="#qa-a6ebd187b8938135">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagents" data-paper-title="HyperAgents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="HyperAgents Agent University of British Columbia 2026-03-19 把任务 Agent 与修改它的 meta Agent 放入同一可编辑程序，并在开放档案中积累变体；父代概率同时奖励当前性能与较少后代的探索价值，使改进机制本身也可继续被改进。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，因此只验证搜索控制机制，不声称复现自指代码修改能力。三种子诊断：metrics/mechanism-seeds42-44.json  RSI 开放式进化 元认知自修改 Agent 运行流程与自进化：改的是哪一层 本地 archive step 是否执行模型生成源码或 shell？ 没有。本地只计算父代分布和有界结构化档案，禁止执行生成代码或 shell，因此不能宣称验证自指程序修改能力。概率和为一、谱系更新正常是搜索控制证据，不能替代真实任务 Agent 与 meta Agent 的行为评测。 例如修改记录中的一个字段可测 archive，但若未运行修改后的程序，就不知道它会不会破坏任务执行或改进策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ccc25faa1e3c6fce">本地 archive step 是否执行模型生成源码或 shell？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahyperagents">HyperAgents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of British Columbia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地只计算父代分布和有界结构化档案，禁止执行生成代码或 shell，因此不能宣称验证自指程序修改能力。概率和为一、谱系更新正常是搜索控制证据，不能替代真实任务 Agent 与 meta Agent 的行为评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如修改记录中的一个字段可测 archive，但若未运行修改后的程序，就不知道它会不会破坏任务执行或改进策略。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19461">原论文</a> · <a href="../../../../agent-research/2603.19461-hyperagents/">实现解读</a> · <a href="#qa-ccc25faa1e3c6fce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:polca" data-paper-title="POLCA: Stochastic Generative Optimization with LLM" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="POLCA: Stochastic Generative Optimization with LLM Agent University of Wisconsin-Madison 2026-03-16 随机 minibatch、程序与评估器都会产生噪声。POLCA 不仅保留一次最高分，而是持续更新候选评价历史；Summarizer 形成全局经验，Proposer 利用当前反馈提出参数，语义 epsilon-net 限制冗余候选。原文 §3 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0；优先队列和真实回调接口已实现，没有声称已运行 LLM 优化器或 benchmark 能力。完整实验：成本过高，不复现（审查 DONE）。6 项测试通过，覆盖严格 epsilon 边界、新候选互相过滤、同一有放回 minibatch、跨轮噪声均值/方差、完整输入/输出历史送入 Summarizer/Proposer、预算耗尽及拒绝 test split。诊断记录  Agent 自进化 随机优化 程序搜索 Agent 运行流程与自进化：改的是哪一层 带噪声的优化任务为什么容易把一次偶然高分误当成好方案？ 随机批次、程序执行和评价器都会让同一候选的分数波动，只记最高观察会偏向运气好的候选。POLCA 研究让搜索利用评价历史和全局经验，并限制提案冗余。历史更多并不消除偏差，仍需相同评测条件与预算控制，不能用未测提案的预期替代真实观察。 教学例：配置甲偶然遇到容易批次得高分，配置乙在多批次较稳定；只看各自最高值可能选错，保留完整历史才能检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-polca-3e1ab10b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0893e96060cf1920">带噪声的优化任务为什么容易把一次偶然高分误当成好方案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apolca">POLCA: Stochastic Generative Optimization with LLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin-Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>随机批次、程序执行和评价器都会让同一候选的分数波动，只记最高观察会偏向运气好的候选。POLCA 研究让搜索利用评价历史和全局经验，并限制提案冗余。历史更多并不消除偏差，仍需相同评测条件与预算控制，不能用未测提案的预期替代真实观察。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：配置甲偶然遇到容易批次得高分，配置乙在多批次较稳定；只看各自最高值可能选错，保留完整历史才能检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.14769">原论文</a> · <a href="../../../../agent-research/2603.14769-polca/">实现解读</a> · <a href="#qa-0893e96060cf1920">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:polca" data-paper-title="POLCA: Stochastic Generative Optimization with LLM" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="POLCA: Stochastic Generative Optimization with LLM Agent University of Wisconsin-Madison 2026-03-16 随机 minibatch、程序与评估器都会产生噪声。POLCA 不仅保留一次最高分，而是持续更新候选评价历史；Summarizer 形成全局经验，Proposer 利用当前反馈提出参数，语义 epsilon-net 限制冗余候选。原文 §3 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0；优先队列和真实回调接口已实现，没有声称已运行 LLM 优化器或 benchmark 能力。完整实验：成本过高，不复现（审查 DONE）。6 项测试通过，覆盖严格 epsilon 边界、新候选互相过滤、同一有放回 minibatch、跨轮噪声均值/方差、完整输入/输出历史送入 Summarizer/Proposer、预算耗尽及拒绝 test split。诊断记录  Agent 自进化 随机优化 程序搜索 Agent 运行流程与自进化：改的是哪一层 为什么候选评价要维护历史均值，并用语义 epsilon-net 限制冗余？ 随机数据和评估器会带来噪声，一次高分可能是偶然，持续记录提供更稳的候选比较。语义距离约束减少把预算浪费在近似重复提案上，加入新候选后还要重算距离；经验均值规则与理论 UCB 不能混作同一实现，也不能把均值排名当显著性结论。 例如十个候选只是同一提示换标点，语义过滤可少测这些重复项；某方案首轮幸运高分，也应结合后续评价而非永久封王。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:polca" data-paper-title="POLCA: Stochastic Generative Optimization with LLM" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="POLCA: Stochastic Generative Optimization with LLM Agent University of Wisconsin-Madison 2026-03-16 随机 minibatch、程序与评估器都会产生噪声。POLCA 不仅保留一次最高分，而是持续更新候选评价历史；Summarizer 形成全局经验，Proposer 利用当前反馈提出参数，语义 epsilon-net 限制冗余候选。原文 §3 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0；优先队列和真实回调接口已实现，没有声称已运行 LLM 优化器或 benchmark 能力。完整实验：成本过高，不复现（审查 DONE）。6 项测试通过，覆盖严格 epsilon 边界、新候选互相过滤、同一有放回 minibatch、跨轮噪声均值/方差、完整输入/输出历史送入 Summarizer/Proposer、预算耗尽及拒绝 test split。诊断记录  Agent 自进化 随机优化 程序搜索 Agent 运行流程与自进化：改的是哪一层 POLCA 正文的经验均值优先级与理论 UCB 版本，为什么不应混成同一更新规则？ 经验均值使用候选实际已有的平均回报排序，UCB 还会显式加入对不确定性的探索奖励。两者会给少评候选不同优先级，预算与选择轨迹也可能随之改变。正文实现和理论分析的规则需要分别说明，本地不能未经实现就把某一种规则的性质归给另一种。 教学例：新候选只评过一次，均值排序未必选它；UCB 可能因不确定度较大再给机会，这会形成不同的下一轮。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-72aa3981c593eb47">POLCA 正文的经验均值优先级与理论 UCB 版本，为什么不应混成同一更新规则？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apolca">POLCA: Stochastic Generative Optimization with LLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin-Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>经验均值使用候选实际已有的平均回报排序，UCB 还会显式加入对不确定性的探索奖励。两者会给少评候选不同优先级，预算与选择轨迹也可能随之改变。正文实现和理论分析的规则需要分别说明，本地不能未经实现就把某一种规则的性质归给另一种。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：新候选只评过一次，均值排序未必选它；UCB 可能因不确定度较大再给机会，这会形成不同的下一轮。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.14769">原论文</a> · <a href="../../../../agent-research/2603.14769-polca/">实现解读</a> · <a href="#qa-72aa3981c593eb47">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:polca" data-paper-title="POLCA: Stochastic Generative Optimization with LLM" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="POLCA: Stochastic Generative Optimization with LLM Agent University of Wisconsin-Madison 2026-03-16 随机 minibatch、程序与评估器都会产生噪声。POLCA 不仅保留一次最高分，而是持续更新候选评价历史；Summarizer 形成全局经验，Proposer 利用当前反馈提出参数，语义 epsilon-net 限制冗余候选。原文 §3 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0；优先队列和真实回调接口已实现，没有声称已运行 LLM 优化器或 benchmark 能力。完整实验：成本过高，不复现（审查 DONE）。6 项测试通过，覆盖严格 epsilon 边界、新候选互相过滤、同一有放回 minibatch、跨轮噪声均值/方差、完整输入/输出历史送入 Summarizer/Proposer、预算耗尽及拒绝 test split。诊断记录  Agent 自进化 随机优化 程序搜索 Agent 运行流程与自进化：改的是哪一层 metric 预算耗尽后未测提案和失败前观察如何保存？ 实际调用前计数，失败前已完成的观察保留；未评价提案标 deferred_budget，不加入有回报统计，旧新候选用同一有放回 batch。callback 无默认伪 LLM 兜底，输入输出深拷贝保护历史；本地测试不证明真实生成优化能力。 例如最后预算只够评一个新提案，另三个不能记成零分或默认成功，它们没有观测，应与已测候选区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b232414eebadc9b4">metric 预算耗尽后未测提案和失败前观察如何保存？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apolca">POLCA: Stochastic Generative Optimization with LLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin-Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实际调用前计数，失败前已完成的观察保留；未评价提案标 deferred_budget，不加入有回报统计，旧新候选用同一有放回 batch。callback 无默认伪 LLM 兜底，输入输出深拷贝保护历史；本地测试不证明真实生成优化能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最后预算只够评一个新提案，另三个不能记成零分或默认成功，它们没有观测，应与已测候选区分。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.14769">原论文</a> · <a href="../../../../agent-research/2603.14769-polca/">实现解读</a> · <a href="#qa-b232414eebadc9b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mars-research" data-paper-title="MARS: Modular Agent with Reflective Search for Automated AI Research" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MARS: Modular Agent with Reflective Search for Automated AI Research Agent Google Cloud AI Research 2026-02-02 自动研究不仅要生成正确代码，还需在有限训练时间内分辨改动价值。MARS 使用“设计—拆分—实现”生成模块化仓库，以预算感知 MCTS 选择新方案、改进或调试；比较新旧执行结果和代码差异，提炼解决方案经验与调试经验，供其他搜索分支复用。图按原文 Figure 2 重绘。原文流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。MLE-Bench 包含 75 个竞赛，每竞赛预算 24 小时单张 A100-40GB，另有大内存、存储和闭源 LLM 调用；完整多方法三次评测显然超出短时单卡预算（§5.1）。成本过高，不复现（审查 DONE），不启动下载与竞赛训练来验证成本。  自进化与经验复用 预算感知自动研究 Agent 运行流程与自进化：改的是哪一层 Design—Split—Implement 为什么要先生成模块化仓库？ 研究改动涉及多个组件，先明确设计与模块边界再实现，可让搜索分支局部改进并复用调试经验，而不每次重写整体代码。模块化也可能界面不完整，真正效果仍来自训练执行，不能把仓库结构漂亮或代码差异小当算法已正确实现。 例如数据加载、模型与评测分开后，可只替换模型分支并保持同一评测入口，便于比较而不混入数据改动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-mars-research-5e806f85" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dc84c4925aa29228">Design—Split—Implement 为什么要先生成模块化仓库？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amars-research">MARS: Modular Agent with Reflective Search for Automated AI Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究改动涉及多个组件，先明确设计与模块边界再实现，可让搜索分支局部改进并复用调试经验，而不每次重写整体代码。模块化也可能界面不完整，真正效果仍来自训练执行，不能把仓库结构漂亮或代码差异小当算法已正确实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数据加载、模型与评测分开后，可只替换模型分支并保持同一评测入口，便于比较而不混入数据改动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02660v1">原论文</a> · <a href="../../../../agent-research/2602.02660-mars-research/">实现解读</a> · <a href="#qa-dc84c4925aa29228">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mars-research" data-paper-title="MARS: Modular Agent with Reflective Search for Automated AI Research" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MARS: Modular Agent with Reflective Search for Automated AI Research Agent Google Cloud AI Research 2026-02-02 自动研究不仅要生成正确代码，还需在有限训练时间内分辨改动价值。MARS 使用“设计—拆分—实现”生成模块化仓库，以预算感知 MCTS 选择新方案、改进或调试；比较新旧执行结果和代码差异，提炼解决方案经验与调试经验，供其他搜索分支复用。图按原文 Figure 2 重绘。原文流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。MLE-Bench 包含 75 个竞赛，每竞赛预算 24 小时单张 A100-40GB，另有大内存、存储和闭源 LLM 调用；完整多方法三次评测显然超出短时单卡预算（§5.1）。成本过高，不复现（审查 DONE），不启动下载与竞赛训练来验证成本。  自进化与经验复用 预算感知自动研究 Agent 运行流程与自进化：改的是哪一层 为什么研究搜索的节点价值要同时考虑指标和运行时间？ 有限训练预算下，同等质量但更慢的方案会挤占后续探索，单看分数可能选中不划算的路线。MARS 归一化执行指标并加入时间惩罚，再有界地安排改进或调试；反思经验来自代码差与真实结果，不能用模型预期性能替代节点测量。 例如两种方案都到相近验证分数，一种耗时十倍，预算感知搜索可优先较快者，留下资源检验更多结构假设。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mars-research" data-paper-title="MARS: Modular Agent with Reflective Search for Automated AI Research" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MARS: Modular Agent with Reflective Search for Automated AI Research Agent Google Cloud AI Research 2026-02-02 自动研究不仅要生成正确代码，还需在有限训练时间内分辨改动价值。MARS 使用“设计—拆分—实现”生成模块化仓库，以预算感知 MCTS 选择新方案、改进或调试；比较新旧执行结果和代码差异，提炼解决方案经验与调试经验，供其他搜索分支复用。图按原文 Figure 2 重绘。原文流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。MLE-Bench 包含 75 个竞赛，每竞赛预算 24 小时单张 A100-40GB，另有大内存、存储和闭源 LLM 调用；完整多方法三次评测显然超出短时单卡预算（§5.1）。成本过高，不复现（审查 DONE），不启动下载与竞赛训练来验证成本。  自进化与经验复用 预算感知自动研究 Agent 运行流程与自进化：改的是哪一层 新建、改进与调试三类搜索动作，各试图改变什么？ 新建探索不同研究方案，改进沿已有效节点提高性能，调试则修复尚不能有效执行的候选。三者产出的证据不同：报错减少不等于指标更好，已运行也不等于值得继续搜索。MARS 按执行状态和预算选择分支，并限制调试及子代数量，不能把失败候选的估计指标当实测。 教学例：导入错误先走调试，修好后才能测指标；指标有效但还有空间可做改进，完全换路线才属于新建。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-239f41d9330029f8">新建、改进与调试三类搜索动作，各试图改变什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amars-research">MARS: Modular Agent with Reflective Search for Automated AI Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新建探索不同研究方案，改进沿已有效节点提高性能，调试则修复尚不能有效执行的候选。三者产出的证据不同：报错减少不等于指标更好，已运行也不等于值得继续搜索。MARS 按执行状态和预算选择分支，并限制调试及子代数量，不能把失败候选的估计指标当实测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：导入错误先走调试，修好后才能测指标；指标有效但还有空间可做改进，完全换路线才属于新建。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02660v1">原论文</a> · <a href="../../../../agent-research/2602.02660-mars-research/">实现解读</a> · <a href="#qa-239f41d9330029f8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mars-research" data-paper-title="MARS: Modular Agent with Reflective Search for Automated AI Research" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="MARS: Modular Agent with Reflective Search for Automated AI Research Agent Google Cloud AI Research 2026-02-02 自动研究不仅要生成正确代码，还需在有限训练时间内分辨改动价值。MARS 使用“设计—拆分—实现”生成模块化仓库，以预算感知 MCTS 选择新方案、改进或调试；比较新旧执行结果和代码差异，提炼解决方案经验与调试经验，供其他搜索分支复用。图按原文 Figure 2 重绘。原文流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。MLE-Bench 包含 75 个竞赛，每竞赛预算 24 小时单张 A100-40GB，另有大内存、存储和闭源 LLM 调用；完整多方法三次评测显然超出短时单卡预算（§5.1）。成本过高，不复现（审查 DONE），不启动下载与竞赛训练来验证成本。  自进化与经验复用 预算感知自动研究 Agent 运行流程与自进化：改的是哪一层 全节点指标相同、失败调试与经验容量有哪些明确边界？ 指标范围为零时归一化取 0.5，避免除零；论文至多十次调试、两个改进子代、三十条近期经验，限制搜索扩张。当前本地无实现或训练，作者代码与轨迹发布也不等于完整控制器可复现，不能仅抄奖励公式宣称研究能力。 例如所有候选 AUC 都相同，不应产生 NaN 或任选一个极高分；统一中值只让时间等其他条件继续起作用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6074a7a5727628e7">全节点指标相同、失败调试与经验容量有哪些明确边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amars-research">MARS: Modular Agent with Reflective Search for Automated AI Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>指标范围为零时归一化取 0.5，避免除零；论文至多十次调试、两个改进子代、三十条近期经验，限制搜索扩张。当前本地无实现或训练，作者代码与轨迹发布也不等于完整控制器可复现，不能仅抄奖励公式宣称研究能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如所有候选 AUC 都相同，不应产生 NaN 或任选一个极高分；统一中值只让时间等其他条件继续起作用。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与成本判断；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02660v1">原论文</a> · <a href="../../../../agent-research/2602.02660-mars-research/">实现解读</a> · <a href="#qa-6074a7a5727628e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:self-refine" data-paper-title="Self-Refine" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Refine Agent Carnegie Mellon University 2023-03-30 一次生成很难同时满足所有约束。Self-Refine 让同一个 LLM 先生成初稿，再针对任务维度给出可执行反馈，最后据此改写；若反馈判断已满足要求则停止，不需要额外训练数据、人工反馈或外部 reward model。 Self-Refine 在不更新参数的情况下循环执行“生成—自反馈—改写”，把推理时计算用于发现并修正当前答案的问题。实现显式初稿、约束反馈、修订和停止链路；mini-suite 用确定性 critic 验证状态迁移，没有调用论文中的通用 LLM，也不能用 1.0 成功率替代七项原始 benchmark 结果。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 2.0000，执行 120 次反馈和 120 次 refinement，共记录 240 个 reasoning steps。  自我迭代 Agent 运行流程与自进化：改的是哪一层 Self-Refine 为什么把一次输出看成还能按具体要求改进的草稿？ 开放生成常同时要求正确、完整、清晰或符合风格，一次回答可能只满足其中部分。Self-Refine 让模型先生成，再明确检查不足并修订，不依赖额外参数训练。循环需要有可执行反馈，模型也可能误判或越改越差，因此改了多轮不等于质量已经提高。 教学例：初稿解释正确却缺少例子，反馈指出这一缺口后再补写；若反馈只有“再好一点”，下一轮未必知道该改哪里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-self-refine-16be87c4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f58bee1c1db1b73e">Self-Refine 为什么把一次输出看成还能按具体要求改进的草稿？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aself-refine">Self-Refine</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>开放生成常同时要求正确、完整、清晰或符合风格，一次回答可能只满足其中部分。Self-Refine 让模型先生成，再明确检查不足并修订，不依赖额外参数训练。循环需要有可执行反馈，模型也可能误判或越改越差，因此改了多轮不等于质量已经提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：初稿解释正确却缺少例子，反馈指出这一缺口后再补写；若反馈只有“再好一点”，下一轮未必知道该改哪里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17651">原论文</a> · <a href="../../../../agent-research/2303.17651-self-refine/">实现解读</a> · <a href="#qa-f58bee1c1db1b73e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:self-refine" data-paper-title="Self-Refine" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Refine Agent Carnegie Mellon University 2023-03-30 一次生成很难同时满足所有约束。Self-Refine 让同一个 LLM 先生成初稿，再针对任务维度给出可执行反馈，最后据此改写；若反馈判断已满足要求则停止，不需要额外训练数据、人工反馈或外部 reward model。 Self-Refine 在不更新参数的情况下循环执行“生成—自反馈—改写”，把推理时计算用于发现并修正当前答案的问题。实现显式初稿、约束反馈、修订和停止链路；mini-suite 用确定性 critic 验证状态迁移，没有调用论文中的通用 LLM，也不能用 1.0 成功率替代七项原始 benchmark 结果。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 2.0000，执行 120 次反馈和 120 次 refinement，共记录 240 个 reasoning steps。  自我迭代 Agent 运行流程与自进化：改的是哪一层 同一模型同时写初稿和反馈，为什么还要把反馈作为单独步骤显式生成？ 显式反馈把不满足的约束转成可执行修改方向，使改写不只是随机再采样一遍答案。生成、反馈和精炼承担不同角色，停止仍依赖模型自身判断；无需外部训练并不意味着反馈一定正确，也不能把反复润色当作已经有独立事实验证。 例如初稿遗漏单位，反馈明确指出需补每个数值单位，改写才有具体目标；仅说“再写好一点”很难定位同一缺陷。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:self-refine" data-paper-title="Self-Refine" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Refine Agent Carnegie Mellon University 2023-03-30 一次生成很难同时满足所有约束。Self-Refine 让同一个 LLM 先生成初稿，再针对任务维度给出可执行反馈，最后据此改写；若反馈判断已满足要求则停止，不需要额外训练数据、人工反馈或外部 reward model。 Self-Refine 在不更新参数的情况下循环执行“生成—自反馈—改写”，把推理时计算用于发现并修正当前答案的问题。实现显式初稿、约束反馈、修订和停止链路；mini-suite 用确定性 critic 验证状态迁移，没有调用论文中的通用 LLM，也不能用 1.0 成功率替代七项原始 benchmark 结果。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 2.0000，执行 120 次反馈和 120 次 refinement，共记录 240 个 reasoning steps。  自我迭代 Agent 运行流程与自进化：改的是哪一层 与 Reflexion 的跨 trial episodic memory 相比，Self-Refine 更关注哪种循环？ Self-Refine 围绕当前初稿做反馈和修订，Reflexion 将失败经验写入有界记忆供下一 trial 使用。两者可组合却不是同一状态机制，前者不自动形成长期经验库，也不能因为多次改写就称参数 RL。 例如一封邮件在当前轮改三次是 Self-Refine；把“先核对收件人”经验用于明天的新邮件则涉及跨 trial 记忆。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-aafa2deef3b0dbdb">与 Reflexion 的跨 trial episodic memory 相比，Self-Refine 更关注哪种循环？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aself-refine">Self-Refine</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Self-Refine 围绕当前初稿做反馈和修订，Reflexion 将失败经验写入有界记忆供下一 trial 使用。两者可组合却不是同一状态机制，前者不自动形成长期经验库，也不能因为多次改写就称参数 RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一封邮件在当前轮改三次是 Self-Refine；把“先核对收件人”经验用于明天的新邮件则涉及跨 trial 记忆。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17651">原论文</a> · <a href="../../../../agent-research/2303.17651-self-refine/">实现解读</a> · <a href="#qa-aafa2deef3b0dbdb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:self-refine" data-paper-title="Self-Refine" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Self-Refine Agent Carnegie Mellon University 2023-03-30 一次生成很难同时满足所有约束。Self-Refine 让同一个 LLM 先生成初稿，再针对任务维度给出可执行反馈，最后据此改写；若反馈判断已满足要求则停止，不需要额外训练数据、人工反馈或外部 reward model。 Self-Refine 在不更新参数的情况下循环执行“生成—自反馈—改写”，把推理时计算用于发现并修正当前答案的问题。实现显式初稿、约束反馈、修订和停止链路；mini-suite 用确定性 critic 验证状态迁移，没有调用论文中的通用 LLM，也不能用 1.0 成功率替代七项原始 benchmark 结果。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 2.0000，执行 120 次反馈和 120 次 refinement，共记录 240 个 reasoning steps。  自我迭代 Agent 运行流程与自进化：改的是哪一层 本地确定性 critic 的停止能代表真实 LLM 自评可靠性吗？ 不能。本地显式生成、反馈、修订和停止的状态链由受控 critic 验证，没有通用 LLM 或七项原 benchmark。停止只证明该判定合同，不能推断模型在开放事实题也能识别自己已正确，更不能用本地满分替代人类偏好。 例如规则检查文本长度合格就停止，无法证明其中事实无误；真实自评可能过早满意，需独立证据评估。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d41641b7b845502f">本地确定性 critic 的停止能代表真实 LLM 自评可靠性吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aself-refine">Self-Refine</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地显式生成、反馈、修订和停止的状态链由受控 critic 验证，没有通用 LLM 或七项原 benchmark。停止只证明该判定合同，不能推断模型在开放事实题也能识别自己已正确，更不能用本地满分替代人类偏好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规则检查文本长度合格就停止，无法证明其中事实无误；真实自评可能过早满意，需独立证据评估。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17651">原论文</a> · <a href="../../../../agent-research/2303.17651-self-refine/">实现解读</a> · <a href="#qa-d41641b7b845502f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:reflexion" data-paper-title="Reflexion" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Reflexion Agent Northeastern University 2023-03-20 传统 RL 要大量采样与参数更新。Reflexion 把稀疏标量/二值反馈“放大”为可执行的自然语言经验，写入长期 episodic memory；Actor 在下一 trial 读取反思，Evaluator 继续判定成功与否。 本页实现失败反馈 → 语言反思 → 有界 episodic memory → 下一 trial 改进，全程不更新模型权重。实现跨 trial 的失败、语言经验与复用闭环，但反思模板和 evaluator 是确定性的；没有调用 GPT-4、ALFWorld、HotpotQA 或代码执行器。0.9 来自“每个新族首次失败”的可审计协议，不等同 HumanEval pass@1。PlanBench mini 有 12 个重复任务族。每族首次暴露计划错误，Evaluator 失败后生成一条可复用反思；后续 episode 读取当前上下文并执行完整计划。  自我反思 Agent 运行流程与自进化：改的是哪一层 Reflexion 为什么在多次尝试之间保存失败教训，而不只重新随机作答？ 同一任务反复尝试时，单纯重采样容易重复原来的错误。Reflexion 将执行评价转成可读经验，供后续尝试调整行为，使反馈跨 trial 保留。记下教训不等于它正确或可迁移，外部奖励与文字反思的作用应分开，模型参数也不会因此自动完成 RL 更新。 教学例：第一次搜索停在无效页面，反思可提醒下一次检查来源和扩大查询；只重新开始而不保留教训，可能再次走同一路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<span id="paper-agent-research-reflexion-b837a66e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2a78cc6a61444ea4">Reflexion 为什么在多次尝试之间保存失败教训，而不只重新随机作答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Areflexion">Reflexion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一任务反复尝试时，单纯重采样容易重复原来的错误。Reflexion 将执行评价转成可读经验，供后续尝试调整行为，使反馈跨 trial 保留。记下教训不等于它正确或可迁移，外部奖励与文字反思的作用应分开，模型参数也不会因此自动完成 RL 更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：第一次搜索停在无效页面，反思可提醒下一次检查来源和扩大查询；只重新开始而不保留教训，可能再次走同一路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.11366">原论文</a> · <a href="../../../../agent-research/2303.11366-reflexion/">实现解读</a> · <a href="#qa-2a78cc6a61444ea4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:reflexion" data-paper-title="Reflexion" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Reflexion Agent Northeastern University 2023-03-20 传统 RL 要大量采样与参数更新。Reflexion 把稀疏标量/二值反馈“放大”为可执行的自然语言经验，写入长期 episodic memory；Actor 在下一 trial 读取反思，Evaluator 继续判定成功与否。 本页实现失败反馈 → 语言反思 → 有界 episodic memory → 下一 trial 改进，全程不更新模型权重。实现跨 trial 的失败、语言经验与复用闭环，但反思模板和 evaluator 是确定性的；没有调用 GPT-4、ALFWorld、HotpotQA 或代码执行器。0.9 来自“每个新族首次失败”的可审计协议，不等同 HumanEval pass@1。PlanBench mini 有 12 个重复任务族。每族首次暴露计划错误，Evaluator 失败后生成一条可复用反思；后续 episode 读取当前上下文并执行完整计划。  自我反思 Agent 运行流程与自进化：改的是哪一层 verbal reinforcement 为什么不等于对模型参数做强化学习更新？ 反馈被转换成自然语言经验写入有界 episodic memory，下一次尝试改变的是模型所见上下文，而非通过梯度修改权重。反思能传递比二元成败更具体的经验，但记忆内容仍可能错误，Evaluator 必须继续判定实际执行，不能由反思自称学会。 例如失败后记下“先确认文件路径再编辑”，下一轮读取这句话会改变行为；即使权重完全相同也可表现不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:reflexion" data-paper-title="Reflexion" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Reflexion Agent Northeastern University 2023-03-20 传统 RL 要大量采样与参数更新。Reflexion 把稀疏标量/二值反馈“放大”为可执行的自然语言经验，写入长期 episodic memory；Actor 在下一 trial 读取反思，Evaluator 继续判定成功与否。 本页实现失败反馈 → 语言反思 → 有界 episodic memory → 下一 trial 改进，全程不更新模型权重。实现跨 trial 的失败、语言经验与复用闭环，但反思模板和 evaluator 是确定性的；没有调用 GPT-4、ALFWorld、HotpotQA 或代码执行器。0.9 来自“每个新族首次失败”的可审计协议，不等同 HumanEval pass@1。PlanBench mini 有 12 个重复任务族。每族首次暴露计划错误，Evaluator 失败后生成一条可复用反思；后续 episode 读取当前上下文并执行完整计划。  自我反思 Agent 运行流程与自进化：改的是哪一层 二值失败到可执行反思相比直接保存奖励多了什么？ 二值奖励只说未成功，反思尝试提炼原因和下一次应避免或尝试的行为，提供可操作上下文。推断仍可能错误，需要真实下一 trial 反馈检验；不能把隐藏标准计划直接写成反思，再把成功归因自主学习。 例如“失败”不足以说明要改哪里，“日期参数需 ISO 格式”更可执行，但必须来自可见报错而不是 gold route。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e6913428acdd0141">二值失败到可执行反思相比直接保存奖励多了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Areflexion">Reflexion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>二值奖励只说未成功，反思尝试提炼原因和下一次应避免或尝试的行为，提供可操作上下文。推断仍可能错误，需要真实下一 trial 反馈检验；不能把隐藏标准计划直接写成反思，再把成功归因自主学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“失败”不足以说明要改哪里，“日期参数需 ISO 格式”更可执行，但必须来自可见报错而不是 gold route。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.11366">原论文</a> · <a href="../../../../agent-research/2303.11366-reflexion/">实现解读</a> · <a href="#qa-e6913428acdd0141">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:reflexion" data-paper-title="Reflexion" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/harness-and-self-improvement" data-search="Reflexion Agent Northeastern University 2023-03-20 传统 RL 要大量采样与参数更新。Reflexion 把稀疏标量/二值反馈“放大”为可执行的自然语言经验，写入长期 episodic memory；Actor 在下一 trial 读取反思，Evaluator 继续判定成功与否。 本页实现失败反馈 → 语言反思 → 有界 episodic memory → 下一 trial 改进，全程不更新模型权重。实现跨 trial 的失败、语言经验与复用闭环，但反思模板和 evaluator 是确定性的；没有调用 GPT-4、ALFWorld、HotpotQA 或代码执行器。0.9 来自“每个新族首次失败”的可审计协议，不等同 HumanEval pass@1。PlanBench mini 有 12 个重复任务族。每族首次暴露计划错误，Evaluator 失败后生成一条可复用反思；后续 episode 读取当前上下文并执行完整计划。  自我反思 Agent 运行流程与自进化：改的是哪一层 mini-suite 0.9 与 ToolRoute 的隔离结果为什么要分别解读？ 前者按每个新族首次失败、后续复用的确定性协议构造，反思模板与 evaluator 也固定；后者是另一个无 reference policy 接口的工具环境。两者都非 HumanEval pass@1，记忆有界追加和失败保留可验证，数值不能跨协议排名或替代原论文。 例如十二个任务族各故意失败一次会决定总体比例，这与模型在一百二十个独立编程题上的自然错误分布不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 运行流程与自进化：改的是哪一层</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cba650900339d0a3">mini-suite 0.9 与 ToolRoute 的隔离结果为什么要分别解读？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Areflexion">Reflexion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者按每个新族首次失败、后续复用的确定性协议构造，反思模板与 evaluator 也固定；后者是另一个无 reference policy 接口的工具环境。两者都非 HumanEval pass@1，记忆有界追加和失败保留可验证，数值不能跨协议排名或替代原论文。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十二个任务族各故意失败一次会决定总体比例，这与模型在一百二十个独立编程题上的自然错误分布不同。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.11366">原论文</a> · <a href="../../../../agent-research/2303.11366-reflexion/">实现解读</a> · <a href="#qa-cba650900339d0a3">问题链接</a></p>
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
