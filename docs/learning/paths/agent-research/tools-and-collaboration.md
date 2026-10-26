---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 工具与协作执行：把计划变成可检查的动作

[Agent](index.md) / 49 个问题 · 49 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">49 个问题 · 49 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rpl" data-paper-title="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning Agent KAIST AI / Meta Superintelligence Labs 2026-10-17 固定检索pipeline把召回数量、融合和返回上下文绑在一起。RPL让策略生成短程序组合稀疏/稠密召回、RRF、去重和重排，只将显式打印的证据交回模型。为解决稀疏奖励难探索的问题，保留策略已有query，对最后一次检索程序做受语法约束的结构变异；执行核验通过后生成续写轨迹，再穿插蒸馏与RL。§3及附录B 成本过高，不复现（审查 DONE）；RetrievalProgram最多4个不同query，宽度取论文阶梯，最多20篇显式输出；execute只解释数据类并调用注入的SDK，不解析或执行Python源码。多路检索实际执行RRF，单路、列表内部或跨路遇到相同ID不同内容时统一拒绝，只有内容完全一致的重复才去重；重排不得注入召回外文档。RRF常数60是明确的本地惯例；输出是文档数上限，不是假装实现了论文2048-token观测限制。  检索与工具 可编程检索与结构变异 Agent 工具与协作执行：把计划变成可检查的动作 为什么答案错误时仍可能保留检索程序监督，却屏蔽答案 span？ 程序可通过语法与执行核验，说明检索组合本身值得学习，最终答案错误不必把全部结构监督一并丢掉。反之，保留错误答案会教坏生成行为；程序或续写 actor 也不能看到 verifier 的 gold，环境观察不应被当成策略自己生成的训练 token。 例如程序正确融合两路召回并去重，回答器却抄错日期，可保留检索步骤训练而遮掉错误日期的答案监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-rpl-95ce1341" class="ar-learning-paper-anchor"></span>
<h2 id="qa-387614f0d3ed6061">为什么答案错误时仍可能保留检索程序监督，却屏蔽答案 span？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arpl">Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>程序可通过语法与执行核验，说明检索组合本身值得学习，最终答案错误不必把全部结构监督一并丢掉。反之，保留错误答案会教坏生成行为；程序或续写 actor 也不能看到 verifier 的 gold，环境观察不应被当成策略自己生成的训练 token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如程序正确融合两路召回并去重，回答器却抄错日期，可保留检索步骤训练而遮掉错误日期的答案监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24854">原论文</a> · <a href="../../../../agent-research/2610.24854-rpl/">实现解读</a> · <a href="#qa-387614f0d3ed6061">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:world-of-swecraft" data-paper-title="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds Agent Massachusetts Institute of Technology 2026-10-16 传统代码Agent评测通常分配一个预定义issue，难以衡量多个维护者如何自主找任务、分工和跨仓库改进。Software World由真实依赖库构成，让Agent用持久记忆、issue、PR和发布进行长期协作，以不可见的下游包检查群体产出是否真正有用。SW-Env用Harbor会话和Forgejo模拟软件维护环境，通信权限、仓库所有权与会话预算可独立控制；SW-Eval在隐藏依赖包上安装冻结版本，测正确性与指令计数，避免只优化自己看到的微基准。多会话持久状态不是无限增长的单条对话。 仅研究资料，成本过高，不复现（审查 DONE）。仅研究资料，成本过高，不复现（审查 DONE）。没有本地软件世界、Agent实验或能力指标。完整复现需要多仓库构建、隔离部署、代码执行沙箱、真实模型会话及大量隐藏下游评测；原论文规模已明显超过单卡A100/A30与Mac低成本预算。成本过高，不复现（审查 DONE）。不克隆和执行未知项目脚本、不伪造本地Agent成绩、不保留自动运行队列，也不宣称Evolve已接入。  多Agent协作 软件生态与自进化评测 Agent 工具与协作执行：把计划变成可检查的动作 为什么用隐藏下游包验证群体改进，而不只运行 Agent 自己维护的微基准？ 群体可能优化已见基准的特例，却破坏真实依赖者。冻结版本在不可见下游安装与检查，能检验公共产物的兼容性和收益；失败任务必须按既定 strict 或 carry 规则处理，不能删掉后再平均，指令计数收益也不能冒充墙钟加速。 例如库把某函数针对自测输入特化，微基准很快却令下游解析器失败；隐藏依赖检查会暴露这种局部优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-world-of-swecraft-5a1942f1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ac28edabd2d0ac9a">为什么用隐藏下游包验证群体改进，而不只运行 Agent 自己维护的微基准？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aworld-of-swecraft">World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>群体可能优化已见基准的特例，却破坏真实依赖者。冻结版本在不可见下游安装与检查，能检验公共产物的兼容性和收益；失败任务必须按既定 strict 或 carry 规则处理，不能删掉后再平均，指令计数收益也不能冒充墙钟加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如库把某函数针对自测输入特化，微基准很快却令下游解析器失败；隐藏依赖检查会暴露这种局部优化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24061v1">原论文</a> · <a href="../../../../agent-research/2610.24061-world-of-swecraft/">实现解读</a> · <a href="#qa-ac28edabd2d0ac9a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:diviner" data-paper-title="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure Agent Meta 2026-10-15 生产事故的症状可能跨推荐、排序、数据、配置和算力服务传播。LLM 能调用工具并不代表它能可靠诊断：超时不等于无异常，历史相似事故不证明本次根因，事后总结也不能作为事故发生时的证据。原文 §4–5用 Encode／Execute／Evaluate／Adapt 四阶段闭环组织领域知识、Lead–worker 调查、事后审查和 owner 批准的知识更新。运行中只调整本次调查计划，不能自行发布新的共享工作流或执行缓解操作。 成本过高，不复现（审查 DONE），亦不伪造公开事故替代结论。这些是合同诊断，不是 RCA 成功率。component_only / L1 CPU 协议组件。实现证据接纳、假设状态与人工批准合同，不运行生产 RCA Agent，不进入 Evolve 晋级。每 seed 产生 24 个有来源的人工事件，随机化工具状态、可获得时间和数值。独立参考条件重算可接纳数；负对照把任何非空工具响应都当证据，从而保留错误接纳计数。另测未批准发布被拒和 owner 批准后版本前进。接口不接真实事故，也不生成根因答案。  工具使用与可靠性 生产事故诊断与证据治理 Agent 工具与协作执行：把计划变成可检查的动作 工具超时为什么既不能支持、也不能反驳根因假设？ 超时说明未取得有效观察，不代表被测服务正常或异常。证据还需匹配事故、目标、时间窗口及当时可获得性，历史相似案例也只是线索；调查计划可在本轮调整，持久工作流发布和缓解执行则是不同权限，不能由一次自动诊断直接越过。 例如查询排序服务日志超时，不能据此写“没有排序异常”；应标记未知并换取证方式，也不能用事故后总结倒灌当前证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-diviner-0cc63af7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a9cacdbf91e3b740">工具超时为什么既不能支持、也不能反驳根因假设？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adiviner">Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>超时说明未取得有效观察，不代表被测服务正常或异常。证据还需匹配事故、目标、时间窗口及当时可获得性，历史相似案例也只是线索；调查计划可在本轮调整，持久工作流发布和缓解执行则是不同权限，不能由一次自动诊断直接越过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如查询排序服务日志超时，不能据此写“没有排序异常”；应标记未知并换取证方式，也不能用事故后总结倒灌当前证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21281">原论文</a> · <a href="../../../../agent-research/2610.21281-diviner/">实现解读</a> · <a href="#qa-a9cacdbf91e3b740">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gemini-minecraft" data-paper-title="A team of Gemini 4 Argon agents beats Minecraft" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="A team of Gemini 4 Argon agents beats Minecraft Agent Google DeepMind 2026-10-15 四个执行 Agent 通过编写 JavaScript 程序操纵 Mineflayer 角色；Observer 汇总世界状态，聊天和笔记传递进度。研究重点是长期协作、程序化工具与持久状态，而不是新训练目标。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地执行 Agent、游戏成功率或 GPU 验证，不接入 Evolve。无本地 capability 指标、训练结果或 Evolve 算子；不创建虚构成功回执。范围见本批验收合同。只完成资料、原图和成本审查，不调用商业模型或运行游戏。原文长时交互超过本轮单卡/本地预算，完整实验标注成本过高，不复现（审查 DONE）。  多 Agent 协作 长期规划与工具使用 Agent 工具与协作执行：把计划变成可检查的动作 Observer 与共享笔记为什么不能替代每个执行 Agent 的真实环境反馈？ 汇总状态适合协调分工，但可能延迟或遗漏局部变化；执行程序仍需以世界实际返回判断成败。程序化动作、持久记录和多会话协作共同支持长程任务，不能仅因聊天中说已完成就推进依赖步骤，也不能把协作案例描述当作本地运行结果。 例如一名角色记下“桥已修好”，另一名过桥前仍可能看到桥被破坏；应依据当前观察修正计划，而非盲信旧笔记。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-gemini-minecraft-c1e2611e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bec7e1165a81dee5">Observer 与共享笔记为什么不能替代每个执行 Agent 的真实环境反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agemini-minecraft">A team of Gemini 4 Argon agents beats Minecraft</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>汇总状态适合协调分工，但可能延迟或遗漏局部变化；执行程序仍需以世界实际返回判断成败。程序化动作、持久记录和多会话协作共同支持长程任务，不能仅因聊天中说已完成就推进依赖步骤，也不能把协作案例描述当作本地运行结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一名角色记下“桥已修好”，另一名过桥前仍可能看到桥被破坏；应依据当前观察修正计划，而非盲信旧笔记。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22319">原论文</a> · <a href="../../../../agent-research/2610.22319-gemini-minecraft/">实现解读</a> · <a href="#qa-bec7e1165a81dee5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-agent-harness" data-paper-title="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs Agent University of Illinois Urbana-Champaign 2026-10-15 Agent 不需要每一步都让昂贵 LLM 生成长文本，但离线多选题高准确率也不保证闭环不出错。JevAgentHarness 在 agent 自己访问的 shadow trajectories 上，分别校准工具、参数等决策的委派阈值，低置信交回 LLM，并报告成功／费用／关键路径延迟。AgentDecision-4B 另用到达过的错误后状态训练，避免只模仿成功轨迹。原文 §2–4、附录 A/D 对单 A100/A30 或 Mac 的本轮预算，完整训练、真实工具任务和多臂评测成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现按决策类别拟合阈值、低置信回退及声明成本会计；没有 Jev／LLM 调用、AgentDecision-4B 训练或统一 Evolve 接入。每 seed 的低／高置信值随机化，40 行 shadow 数值 fixture 拟合不同阈值，在 12 个独立公共请求上实际调用概率 callback 或强模型 callback。负对照把阈值压低到 0.5，保留错误委派；NaN 输出触发回退；  工具使用与可靠性 System One/JEV置信委派与回退 Agent 工具与协作执行：把计划变成可检查的动作 为什么委派阈值要在 Agent 自己访问的 shadow trajectories 上按决策类型校准？ 真实闭环会到达错误后状态，离线干净多选题不覆盖这些输入；工具选择与参数选择的风险和收益也不同。配对比较决策模型与强模型，按任务价值和成本找可靠阈值，不确定或未见类别回退，才能把准确率、费用和延迟放进同一控制问题。 例如小模型选对工具却常把参数填错，两类决策应有不同委派条件；不能用一条整体准确率给全部调用统一放行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-jev-agent-harness-91c2ebf3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e9b8fa18e0639f8f">为什么委派阈值要在 Agent 自己访问的 shadow trajectories 上按决策类型校准？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-agent-harness">JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实闭环会到达错误后状态，离线干净多选题不覆盖这些输入；工具选择与参数选择的风险和收益也不同。配对比较决策模型与强模型，按任务价值和成本找可靠阈值，不确定或未见类别回退，才能把准确率、费用和延迟放进同一控制问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小模型选对工具却常把参数填错，两类决策应有不同委派条件；不能用一条整体准确率给全部调用统一放行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21412">原论文</a> · <a href="../../../../agent-research/2610.21412-jev-agent-harness/">实现解读</a> · <a href="#qa-e9b8fa18e0639f8f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:leash" data-paper-title="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents Agent Simular 2026-10-15 小模型先执行、必要时交给强模型可降低成本，但“何时接管”和“强模型接管后是否走偏”是两个问题。LEASH 利用弱模型表示与历史成功/失败参考的距离，不额外训练一个监控网络；初始和运行时 gate 决定 handoff，之后定期用弱模型的未执行 Shadow 动作表示监督强模型，并在需要时要求其重新审视策略。 完整多模型多配置实验成本高且需要 GUI/远程接口，成本过高，不复现（审查 DONE）。Shadow 高分回调在两次改变强动作后停止，未执行探针动作。component_only / L1 CPU 机制诊断。输入是明确生成的合成向量，不是模型 hidden states；统计校准和 Shadow callback 不等于完成 OSWorld 或真实 GUI Agent。每 seed 使用 30 个合成 reference task、90 action 向量及 12 个隔离 evaluation task；  专家模型编排 公共评测与协议 Agent 工具与协作执行：把计划变成可检查的动作 强模型接管后，为什么还要用未执行的 Shadow 动作继续监督？ 升级解决弱模型可能失败的问题，却不保证强模型之后不偏离。弱模型的影子表示提供低成本参照，定期判断是否需要强模型重新审视策略，但不实际执行影子动作；距离分数只是与失败参考更近的指标，不是已校准失败概率或测试固定接管配额。 例如强模型接管后准备点击删除，弱模型影子建议先检查权限，系统可触发复核，却不能把两套动作都同时执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-leash-edca97db" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cc752aad38fc797e">强模型接管后，为什么还要用未执行的 Shadow 动作继续监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aleash">LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Simular</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>升级解决弱模型可能失败的问题，却不保证强模型之后不偏离。弱模型的影子表示提供低成本参照，定期判断是否需要强模型重新审视策略，但不实际执行影子动作；距离分数只是与失败参考更近的指标，不是已校准失败概率或测试固定接管配额。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如强模型接管后准备点击删除，弱模型影子建议先检查权限，系统可触发复核，却不能把两套动作都同时执行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22280">原论文</a> · <a href="../../../../agent-research/2610.22280-leash/">实现解读</a> · <a href="#qa-cc752aad38fc797e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:structural-signal-retriever" data-paper-title="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems Agent State University of Campinas 2026-10-15 多 Agent 注册表扩大后，把全部 Agent Card 塞给 LLM 会增加输入和选择成本。SSR §III 不训练额外模型，而是从明确的能力字段提取可解释词法信号，以倒排表预先缩小候选池。这里 structural 指来源于 name、description、skills、tags、examples、tools 的字段，不是句法图或隐向量。核心词法机制是已有IDF检索的特定集成，不应包装为新语义模型。 完整实验成本过高，不复现（审查 DONE）。本地CPU诊断记录保存可审计逐seed数据。无数据下载、LLM调用或GPU需求。固定 revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1；seeds42/43/44各生成64张合成能力card及12个查询，检索器只接收能力文本，接口没有gold answer或目标card参数。  工具使用与路由 Agent发现与词法检索 Agent 工具与协作执行：把计划变成可检查的动作 SSR 为什么在无词法命中时返回空池，而不声称找到了语义相近 Agent？ 它的 structural 信号来自明确字段中的词与相邻词组，IDF 得分不包含未匹配语义。倒排索引只省去零分候选的枚举，保持同一词法正分排序；无命中就应暴露信息不足，不能把任意回退结果包装成这套机制提供的语义理解。 例如注册卡只写“invoice”，查询用一个没有共享词的表达可能返回空池；系统应知道是词法覆盖不足，而非假装已理解同义关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-structural-signal-retriever-c1b3c953" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2848f9d257695af3">SSR 为什么在无词法命中时返回空池，而不声称找到了语义相近 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Astructural-signal-retriever">SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · State University of Campinas</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它的 structural 信号来自明确字段中的词与相邻词组，IDF 得分不包含未匹配语义。倒排索引只省去零分候选的枚举，保持同一词法正分排序；无命中就应暴露信息不足，不能把任意回退结果包装成这套机制提供的语义理解。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如注册卡只写“invoice”，查询用一个没有共享词的表达可能返回空池；系统应知道是词法覆盖不足，而非假装已理解同义关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21113">原论文</a> · <a href="../../../../agent-research/2610.21113-structural-signal-retriever/">实现解读</a> · <a href="#qa-2848f9d257695af3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tracer" data-paper-title="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents Agent Microsoft 2026-10-15 把完整工具目录塞进 prompt 会占用大量上下文，纯工具描述相似度又忽略历史执行路径。TRACER 用 turn 内完整调用前缀索引执行 trie，候选是该前缀在训练中实际出现过的下一工具；边上记录频率和发生该转移时的完整 conversation context 均值。训练两个五维线性 head，逐状态决定经验频率/上下文先验的权重和温度；未知前缀或低置信时回到全目录向量检索。原图出处：原文 Figure 6：完整 TRACER 架构。 以单 A100/A30/Mac 的预算，成本过高，不复现（审查 DONE）；本地仅 component_only / CPU 算子诊断。本地仅 component_only / CPU 算子诊断。真正优化的是可学习混合与温度；使用合成三维表示而非原始语义 encoder，也没有 LLM 选择或执行工具。高 fixture recall 不是 Agent 能力，promotion_eligible: false。每 seed 使用 40 train trajectories / 20 held-out trajectories，每条三步，120 个训练步和 60 个测试步。  tool-retrieval Agent 工具与协作执行：把计划变成可检查的动作 为什么工具 trie 用 turn 内完整调用前缀，而不是只看上一把工具？ 同一个上一工具可能出现在不同工作流，完整前缀保留路径身份，下一工具候选才对应真实训练转移。上下文相似度补充当前意图，学习的权重与温度决定如何融合；未知前缀要回退目录检索，不能强行把未见路径套到最相似的旧分支。 例如“搜索→下载”与“认证→下载”后续可能分别需要解析与权限检查，只看最后一个下载工具会混淆两种路线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-tracer-f2f8d03e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a03d84108db990af">为什么工具 trie 用 turn 内完整调用前缀，而不是只看上一把工具？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atracer">TRACER: Trajectory-Aware Tool Retrieval for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一个上一工具可能出现在不同工作流，完整前缀保留路径身份，下一工具候选才对应真实训练转移。上下文相似度补充当前意图，学习的权重与温度决定如何融合；未知前缀要回退目录检索，不能强行把未见路径套到最相似的旧分支。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“搜索→下载”与“认证→下载”后续可能分别需要解析与权限检查，只看最后一个下载工具会混淆两种路线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21267">原论文</a> · <a href="../../../../agent-research/2610.21267-tracer/">实现解读</a> · <a href="#qa-a03d84108db990af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aria" data-paper-title="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems Agent Florida State University 2026-10-14 多 Agent 的早期错误会沿消息和工具结果传播。ARIA 不只在结束后解释失败，而是把执行验证过的修复转成训练数据，让模型在部分轨迹上决定何时干预、在哪里切断及如何续写。原文 §2、附录 B的训练链包括结构 SFT、repair DPO、diagnosis transfer、repair GRPO 和 gate GRPO。本地没有以人工 heuristic 冒充这些学习阶段，只抽出可独立检验的补丁合同。 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现 cut-and-continuation 数据合同，不训练 inspection gate 或修复策略。随机事件序列实际执行合法 cut 与新 tool request 替换；负对照注入未知 cut、保留前缀 ID 冲突和伪造工具观察。另以随机成对执行 verdict 检查“只看 patched pass”会产生的错误样本接纳。verdict 是调用方 scorer 的人工 fixture，不是 Agent 推出的答案；模块不把 gold 传给模型。详见 CPU 产物。  多Agent协作 运行时诊断与续写修复 Agent 工具与协作执行：把计划变成可检查的动作 修复轨迹为什么只能提出待执行 tool call，不能直接写入一个成功 tool result？ 工具结果必须来自真实执行，否则补丁只是伪造证据。切断点保留已观察前缀，模型续写可提出新行动，再与 fresh control 比较是否真的恢复；结构合法只证明补丁格式可接纳，不能单独证明归因正确或错误已被修好。 例如模型提出重新运行测试是合法修复候选，但不能在续写里直接捏造“全部通过”；必须执行测试并读取实际结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-aria-04eaa6e6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-72d8e93a8b1ee2a9">修复轨迹为什么只能提出待执行 tool call，不能直接写入一个成功 tool result？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaria">ARIA: Runtime Inspection and Amendment for Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Florida State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具结果必须来自真实执行，否则补丁只是伪造证据。切断点保留已观察前缀，模型续写可提出新行动，再与 fresh control 比较是否真的恢复；结构合法只证明补丁格式可接纳，不能单独证明归因正确或错误已被修好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型提出重新运行测试是合法修复候选，但不能在续写里直接捏造“全部通过”；必须执行测试并读取实际结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20780">原论文</a> · <a href="../../../../agent-research/2610.20780-aria/">实现解读</a> · <a href="#qa-72d8e93a8b1ee2a9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-workflow" data-paper-title="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows Agent Nanjing University 2026-10-09 这是一篇评测研究，不是新的 self-improvement 算法。比较决策延迟/费用与端到端成功交付；failed recovery、premature completion 和失败开销计入资源每成功，而非只报告单步省时。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为同task/run的原配置与替换decision配置；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evaluation delivered-outcome latency-cost-recovery Agent 工具与协作执行：把计划变成可检查的动作 单步决策更快，为什么每次成功交付的总资源反而可能更高？ 错误决策会引入重试、恢复失败或过早完成，省下的单次延迟可能被失败轨迹抵消。资源每成功把所有尝试的费用和时间计入，再除成功数；只看双方都成功的配对可比较顺利路径，但不能替代全尝试交付口径或隐藏失败成本。 例如快速方案每次便宜一半却经常失败，十次才完成两次；完整统计可能比稍慢但十次成功八次的方案更贵。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-jev-workflow-32efeb08" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f67a6f111ad8004f">单步决策更快，为什么每次成功交付的总资源反而可能更高？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-workflow">When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>错误决策会引入重试、恢复失败或过早完成，省下的单次延迟可能被失败轨迹抵消。资源每成功把所有尝试的费用和时间计入，再除成功数；只看双方都成功的配对可比较顺利路径，但不能替代全尝试交付口径或隐藏失败成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如快速方案每次便宜一半却经常失败，十次才完成两次；完整统计可能比稍慢但十次成功八次的方案更贵。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13092">原论文</a> · <a href="../../../../reproductions/2610.13092-jev-workflow/">实现解读</a> · <a href="#qa-f67a6f111ad8004f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rated" data-paper-title="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics Agent Texas Tech University 2026-10-09 独立 query/tool encoder 做 CLS 归一化与 contrastive InfoNCE 训练。部署时 encoder 冻结，先语义 top-K，再融合 metadata prior 与逐工具 discounted LinUCB；只从实际选中工具的执行成功、错误或超时更新对应 arm。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为冻结语义dual encoder；线上反馈重排实验组；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  tool-retrieval execution-reliability contextual-bandit Agent 工具与协作执行：把计划变成可检查的动作 为什么执行反馈只更新实际选中工具的 LinUCB arm？ 只有被执行工具产生可观察的成功、错误或超时，未选择工具的反事实结果并不知道。逐工具更新避免把一次失败归罪整个候选集，折扣又让旧可靠性随时间衰减；语义 top-K 提供相关候选，可靠性探索项并不意味着模型已证明未调用工具更好。 例如工具甲本次超时，应更新甲的记录；同题没调用的乙不能直接记成功，只能保持不确定并等待以后探索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-rated-710146a7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f3a60a5875bf4cde">为什么执行反馈只更新实际选中工具的 LinUCB arm？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arated">RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Texas Tech University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有被执行工具产生可观察的成功、错误或超时，未选择工具的反事实结果并不知道。逐工具更新避免把一次失败归罪整个候选集，折扣又让旧可靠性随时间衰减；语义 top-K 提供相关候选，可靠性探索项并不意味着模型已证明未调用工具更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具甲本次超时，应更新甲的记录；同题没调用的乙不能直接记成功，只能保持不确定并等待以后探索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13889">原论文</a> · <a href="../../../../reproductions/2610.13889-rated/">实现解读</a> · <a href="#qa-f3a60a5875bf4cde">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mingbird" data-paper-title="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks Agent University of Science and Technology Beijing 2026-10-01 通过 domain 路由和扁平 schema 降低小模型工具调用负担；当模型宣称完成时重新注入原任务与计划并检查产物，发现重复调用或无输出循环时提醒修正，同时为常见 JSON 格式错误提供有限救援。改进的是推理运行框架，不需要把它解释为新的基础模型结构。 L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；使用显式脚本策略，不冒充真实小模型任务成功率。未实现整个 Windows GUI/语音产品、未跑 LRAB/τ²、未接入真实本地 LLM。注册工具仍继承调用方权限，此模块不是隔离沙箱，不应直接注册任意 shell。外部验收不能读取策略未获授权的私密信息并反馈给策略。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 在临时目录中真实写入文件：第一次 finish 因文件不存在被拒绝，随后执行写入，最后重新检查通过。  本地 Agent 运行框架 工具使用 Agent 工具与协作执行：把计划变成可检查的动作 模型宣称完成后，为什么还要重新注入原任务与计划并检查产物？ 长轨迹中模型可能遗忘目标或把动作执行当成最终交付，重新对照原始要求能发现缺文件、缺验证和提前结束。循环检测与有限格式救援解决运行故障，不是直接提升基础模型知识；字节预算也必须按实际 UTF-8 计算，不能用字符数替代。 例如模型成功创建文件后说完成，但原任务还要求生成测试报告；回看原任务才能发现产物清单尚未满足。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-mingbird-bbd1f960" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d9bfd00f5a7bc2d8">模型宣称完成后，为什么还要重新注入原任务与计划并检查产物？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amingbird">Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology Beijing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长轨迹中模型可能遗忘目标或把动作执行当成最终交付，重新对照原始要求能发现缺文件、缺验证和提前结束。循环检测与有限格式救援解决运行故障，不是直接提升基础模型知识；字节预算也必须按实际 UTF-8 计算，不能用字符数替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型成功创建文件后说完成，但原任务还要求生成测试报告；回看原任务才能发现产物清单尚未满足。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02001">原论文</a> · <a href="../../../../agent-research/2610.02001-mingbird/">实现解读</a> · <a href="#qa-d9bfd00f5a7bc2d8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cera-moa" data-paper-title="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents Agent IIIS, Tsinghua University 2026-09-16 用中层隐藏状态估计 Agent 对样本的熟悉度，以累计阈值自适应选专家，并把训练样本定向分配给相应专家。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。  多 Agent 路由与协同进化 Agent 工具与协作执行：把计划变成可检查的动作 根据样本熟悉度自适应选专家，为什么还要把训练样本定向分配回专家？ 路由不只在推理时挑人，训练分配会改变各专家之后擅长什么，两侧存在反馈。中层表示估计熟悉度，累计阈值控制本题需要多少专家，再定向训练强化分工；若只改路由却让所有专家始终同样训练，专长结构可能难以持续形成。 例如代码题多分给更熟悉程序的专家，语言题给另一专家；边界不明确的题可激活更多成员，而不是永远固定同一队伍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-cera-moa-0d23f31e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7a271c323eae1f5d">根据样本熟悉度自适应选专家，为什么还要把训练样本定向分配回专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acera-moa">CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · IIIS, Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路由不只在推理时挑人，训练分配会改变各专家之后擅长什么，两侧存在反馈。中层表示估计熟悉度，累计阈值控制本题需要多少专家，再定向训练强化分工；若只改路由却让所有专家始终同样训练，专长结构可能难以持续形成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如代码题多分给更熟悉程序的专家，语言题给另一专家；边界不明确的题可激活更多成员，而不是永远固定同一队伍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18779">原论文</a> · <a href="../../../../agent-research/2609.18779-cera-moa/">实现解读</a> · <a href="#qa-7a271c323eae1f5d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:repoatlas" data-paper-title="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views Agent Beihang University 2026-09-15 在固定预算下执行 select–project–refresh，把任务相关代码子图同步投影为视觉拓扑与精确文本索引。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  编程 Agent 多模态仓库视图 Agent 工具与协作执行：把计划变成可检查的动作 视觉拓扑与精确文本索引为什么要同步 refresh？ 拓扑展示模块依赖，文本索引负责定位可编辑的真实符号，两者一旦不同步，Agent 可能沿正确图找到过期文件。select–project–refresh 在预算内选择任务相关子图并维护双视图，提供的是共同来源的导航接口，不是用一张漂亮架构图替代源码证据。 例如函数被移动到新模块，图中调用边和文本路径都应更新；只刷新其中一侧会让后续检索指向已经不存在的位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-repoatlas-e75f59d2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5335c0c305107d48">视觉拓扑与精确文本索引为什么要同步 refresh？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arepoatlas">RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>拓扑展示模块依赖，文本索引负责定位可编辑的真实符号，两者一旦不同步，Agent 可能沿正确图找到过期文件。select–project–refresh 在预算内选择任务相关子图并维护双视图，提供的是共同来源的导航接口，不是用一张漂亮架构图替代源码证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如函数被移动到新模块，图中调用边和文本路径都应更新；只刷新其中一侧会让后续检索指向已经不存在的位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16936">原论文</a> · <a href="../../../../agent-research/2609.16936-repoatlas/">实现解读</a> · <a href="#qa-5335c0c305107d48">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hcrg" data-paper-title="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration Agent Google Cloud 2026-09-11 HCRG 用 AST 提取 INHERITS/CALLS/IMPORTS，缓存全局架构骨架，按父依赖先后迁移，三跳取回结构上下文。原文对照是 800 字符/150 overlap/top-5 向量 RAG。§3–4 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0，仅 Python AST 支持的 graph 子系统。不是 Java tree-sitter 管线或真实 LLM 跨语言迁移复现。完整实验：成本过高，不复现（审查 DONE）。8 项 Python 自建源码机制测试通过：跨模块继承、三跳边界、签名骨架、父依赖顺序、显式循环组、缓存与部分静态指标，以及未导入跨模块同名、参数/局部变量shadow、歧义和外部依赖保留。诊断记录  代码 Agent 图检索 代码迁移 Agent 工具与协作执行：把计划变成可检查的动作 依赖图出现环时，为什么不能假称仍有逐节点的父优先拓扑顺序？ 有向环中的节点互相依赖，不存在满足所有边的线性先后。应识别强连通分组，把组间依赖排序与组内迁移问题分开；AST 结构上下文能够揭示这种限制，却不会自动给出论文未定义的破环算法，不能用任意顺序冒充精确依赖处理。 例如 A 调 B、B 又导入 A，应作为循环组一起分析；先迁移 A 再说所有父依赖已完成，会与图的实际关系矛盾。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-hcrg-d21831b9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-62471e72ac894fa6">依赖图出现环时，为什么不能假称仍有逐节点的父优先拓扑顺序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahcrg">Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有向环中的节点互相依赖，不存在满足所有边的线性先后。应识别强连通分组，把组间依赖排序与组内迁移问题分开；AST 结构上下文能够揭示这种限制，却不会自动给出论文未定义的破环算法，不能用任意顺序冒充精确依赖处理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 A 调 B、B 又导入 A，应作为循环组一起分析；先迁移 A 再说所有父依赖已完成，会与图的实际关系矛盾。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12464">原论文</a> · <a href="../../../../agent-research/2609.12464-hcrg/">实现解读</a> · <a href="#qa-62471e72ac894fa6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:feedback-scaffold" data-paper-title="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks Agent Fudan University 2026-09-08 论文指出统一反馈不适合整个探索过程：早期能力不足时使用 action guidance 降低搜索难度，后期则改为 observation enrichment，让 Agent 自己选择动作，避免长期依赖示范。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现早期公开动作引导、后期观察增强的阶段切换；不读取 gold plan。三种子结果见 metrics/mini-suite-seeds42-44.json。第一步只可采用公开 observation 中明确给出的 workflow；后续仅加入状态摘要，隐藏 AgentTask.plan 从不进入策略。当前未训练 LLM，也没有真实环境 rollout。  环境反馈脚手架 Agent 工具与协作执行：把计划变成可检查的动作 为什么早期用 action guidance，后期要转向 observation enrichment？ 能力不足时直接引导动作能降低探索难度，帮助获得可学习轨迹；长期持续示范却可能让策略依赖外部答案。后期改为丰富观察，把取证支持留下、动作选择交还 Agent，逐步降低脚手架依赖；两阶段反馈角色不同，不能用统一强提示覆盖所有训练过程。 例如初学开柜时先提示“找钥匙”，熟练后只补充锁的状态，让 Agent 自己决定下一步，而非永远告诉它完整动作序列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-feedback-scaffold-b914bba8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-32e4e27887fc3581">为什么早期用 action guidance，后期要转向 observation enrichment？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afeedback-scaffold">Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>能力不足时直接引导动作能降低探索难度，帮助获得可学习轨迹；长期持续示范却可能让策略依赖外部答案。后期改为丰富观察，把取证支持留下、动作选择交还 Agent，逐步降低脚手架依赖；两阶段反馈角色不同，不能用统一强提示覆盖所有训练过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如初学开柜时先提示“找钥匙”，熟练后只补充锁的状态，让 Agent 自己决定下一步，而非永远告诉它完整动作序列。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08404">原论文</a> · <a href="../../../../agent-research/2609.08404-feedback-scaffold/">实现解读</a> · <a href="#qa-32e4e27887fc3581">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-prime" data-paper-title="SWE-Prime: Fewer Trajectories, Better Performance" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-Prime: Fewer Trajectories, Better Performance Agent Sun Yat-sen University 2026-08-27 成功轨迹仍可能冗余、危险或不可学习。SWE-Prime 先按过程、结果和代表性选轨迹，再按贡献、可学习性和风险选语义段；上下文完整保留，但只对选中段计算 SFT loss。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现轨迹筛选、语义段筛选和 loss mask。未训练代码 LLM，也未运行官方 SWE-Bench；本地只比较相同 observation/tool 接口下的筛选策略。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5497。  软件轨迹筛选 Agent 工具与协作执行：把计划变成可检查的动作 为什么上下文完整保留，却只对选中语义段计算 SFT loss？ 未选段仍可能是理解后续行为所需的因果背景，删除会造成不完整前缀；但其生成行为可能冗余、危险或不值得模仿。mask 把“提供上下文”与“作为学习目标”分开，让模型读到真实过程而只学习有贡献且可学的部分，成功轨迹也不必全量监督。 例如前面一次错误命令解释了后续修复原因，可保留给模型看，却不奖励重新生成那条危险命令。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-swe-prime-e014601a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-09148f0475ab00b9">为什么上下文完整保留，却只对选中语义段计算 SFT loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-prime">SWE-Prime: Fewer Trajectories, Better Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未选段仍可能是理解后续行为所需的因果背景，删除会造成不完整前缀；但其生成行为可能冗余、危险或不值得模仿。mask 把“提供上下文”与“作为学习目标”分开，让模型读到真实过程而只学习有贡献且可学的部分，成功轨迹也不必全量监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前面一次错误命令解释了后续修复原因，可保留给模型看，却不奖励重新生成那条危险命令。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27449">原论文</a> · <a href="../../../../agent-research/2608.27449-swe-prime/">实现解读</a> · <a href="#qa-09148f0475ab00b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adavdr" data-paper-title="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research Agent Accio Team, Alibaba Group 2026-08-26 先以目标模型能力过滤不必要工具调用，只在中间证据不可靠时回退反思；SFT 后用 redundancy-aware reward 做 RL，兼顾视频理解、外部检索和调用成本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。AdaVDR 在无 oracle 的状态化工具环境中执行候选验证、失败反思与回退。ToolRoute-L2.1 三 seed 的 joint success 为 0.8167，plan step F1 为 0.8366，平均成本 5.0577；  视频研究自适应工具与反思 Agent 工具与协作执行：把计划变成可检查的动作 为什么工具必要性判断与证据不可靠时的回退反思要分开？ 前者决定是否需要外部取证，后者在已取得信息后判断是否值得重新检查，两者面对不同失败点。按能力过滤无必要调用可节省成本，冗余惩罚再约束训练；若为了少调用而无视不可靠证据，也会牺牲视频研究结果，不能把调用数最低直接当最优。 例如模型能直接判断视频有人跑步就不搜索网页，但人物身份线索矛盾时应回退核查，不能机械坚持首次结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-adavdr-576e1cf8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-88d371dfdcbc173d">为什么工具必要性判断与证据不可靠时的回退反思要分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aadavdr">AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Accio Team, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者决定是否需要外部取证，后者在已取得信息后判断是否值得重新检查，两者面对不同失败点。按能力过滤无必要调用可节省成本，冗余惩罚再约束训练；若为了少调用而无视不可靠证据，也会牺牲视频研究结果，不能把调用数最低直接当最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型能直接判断视频有人跑步就不搜索网页，但人物身份线索矛盾时应回退核查，不能机械坚持首次结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25559">原论文</a> · <a href="../../../../agent-research/2608.25559-adavdr/">实现解读</a> · <a href="#qa-88d371dfdcbc173d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:progrouter" data-paper-title="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs Agent Aston University 2026-08-26 用多视角 scorer 衡量子任务完成度、进展趋势和状态质量，再由双路径 predictor 估计候选模型的边际进展，以 meta-gate 在质量、时间和长期成本预算间逐步决策。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。ProgRouter 把验证后的工具选择压缩为可复用程序路由，validation/test 冻结路由后再执行。ToolRoute-L2.1 三 seed的 joint success 为 0.7778，plan step F1 为 0.8037，平均成本 4.6324。  在线进展成本路由 Agent 工具与协作执行：把计划变成可检查的动作 为什么模型路由要预测边际进展，而不只比较各模型的平均准确率？ 不同子任务状态下，强模型可能只比弱模型多推进一点，也可能解决关键阻塞。边际进展结合当前完成度、趋势和质量，才能评价下一次调用的价值，再与时间和长期预算权衡；平均准确率忽略阶段差异，预测分数也仍须由后续执行检验。 例如格式修复时小模型已足够，困难证明阶段强模型才可能带来显著推进；固定每一步都用平均最强者会浪费预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-progrouter-c8bea01c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1a4bcdd40231ca7a">为什么模型路由要预测边际进展，而不只比较各模型的平均准确率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprogrouter">ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Aston University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同子任务状态下，强模型可能只比弱模型多推进一点，也可能解决关键阻塞。边际进展结合当前完成度、趋势和质量，才能评价下一次调用的价值，再与时间和长期预算权衡；平均准确率忽略阶段差异，预测分数也仍须由后续执行检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如格式修复时小模型已足够，困难证明阶段强模型才可能带来显著推进；固定每一步都用平均最强者会浪费预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25992">原论文</a> · <a href="../../../../agent-research/2608.25992-progrouter/">实现解读</a> · <a href="#qa-1a4bcdd40231ca7a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:topas" data-paper-title="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving Agent University of Science and Technology of China 2026-08-26 在共享 KV-cache 预算下，同时估算工作流最长剩余路径与下游 prefix reuse 收益，并纳入 prefix 移动、抢占和 aging，避免只优化局部命中率或单请求进度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TOPAS 在状态化工具环境里先做安全排序与候选压缩，再根据调用反馈恢复。ToolRoute-L2.1 三 seed 的 joint success 为 0.7556，plan step F1 为 0.7887，平均成本 4.5571。  工作流 Prefix-State 调度 Agent 工具与协作执行：把计划变成可检查的动作 为什么共享缓存调度不能只追求最高 prefix hit rate？ 缓存命中提高局部复用，却可能让关键路径上的工作流等待，或产生昂贵搬运和抢占。TOPAS 同时估计最长剩余路径、下游复用收益及移动成本，并用 aging 避免长期饥饿；命中率是一项中间指标，不能单独代表多 Agent 任务的总完成时间。 例如反复服务一批高命中小请求，却堵住即将完成的主流程；牺牲一点命中率优先关键路径，可能更早交付整个任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-topas-ae42000c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-844b8a90e779e693">为什么共享缓存调度不能只追求最高 prefix hit rate？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atopas">TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缓存命中提高局部复用，却可能让关键路径上的工作流等待，或产生昂贵搬运和抢占。TOPAS 同时估计最长剩余路径、下游复用收益及移动成本，并用 aging 避免长期饥饿；命中率是一项中间指标，不能单独代表多 Agent 任务的总完成时间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如反复服务一批高命中小请求，却堵住即将完成的主流程；牺牲一点命中率优先关键路径，可能更早交付整个任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25523">原论文</a> · <a href="../../../../agent-research/2608.25523-topas/">实现解读</a> · <a href="#qa-844b8a90e779e693">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:traceml" data-paper-title="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development Agent Carnegie Mellon University 2026-08-26 统一记录每个代码版本、得分、动作意图、编辑规模和效果，比较 4465 条人类轨迹与 Agent 轨迹；把人类会交替阶段、回开旧方案的规律蒸馏成 planning prior。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TraceML 策略从训练 split 的失败轨迹写入反思先验，validation/test 只读取先验并通过真实工具反馈推进，不读取隐藏 route 或答案。  ML 开发轨迹规划 Agent 工具与协作执行：把计划变成可检查的动作 记录版本、动作意图和编辑规模，为什么比只保存分数曲线更能学习规划规律？ 分数只表示结果，无法区分模型在试新架构、调参还是回退旧方案。把每次修改与意图及效果对应起来，才能观察阶段切换和重开旧路线的策略，再形成规划先验；人类轨迹中的相关规律仍需在 Agent 环境检验，不能直接解释成最优策略。 例如两次分数下降，一次是探索新特征、一次是意外删配置，只有版本和动作记录才能判断该继续尝试还是立即回滚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-traceml-cea4f922" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8d61cb02f607c749">记录版本、动作意图和编辑规模，为什么比只保存分数曲线更能学习规划规律？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atraceml">TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分数只表示结果，无法区分模型在试新架构、调参还是回退旧方案。把每次修改与意图及效果对应起来，才能观察阶段切换和重开旧路线的策略，再形成规划先验；人类轨迹中的相关规律仍需在 Agent 环境检验，不能直接解释成最优策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次分数下降，一次是探索新特征、一次是意外删配置，只有版本和动作记录才能判断该继续尝试还是立即回滚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26086">原论文</a> · <a href="../../../../agent-research/2608.26086-traceml/">实现解读</a> · <a href="#qa-8d61cb02f607c749">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:smith" data-paper-title="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification Agent Appier AI Research / National Taiwan University 2026-08-25 现有工具创建通常在推理时让冻结模型写代码，创建者与使用者没有联合信号。SMITH 在同一 policy 中混合 build task（从样例写 schema/backend）和 use task（在 held-out 问题调用池中工具），分别给 schema 合法性、代码执行和最终答案奖励，并用更难问题鼓励可复用抽象。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。同一 Agent 交替 build/use，并独立执行 schema、代码和 outcome 三类 verifier。本地工具为结构化 plan，并真实分开 build/use 状态和三轴 verifier；未运行 Qwen3-4B、可执行 Python sandbox、Reasoning-Gym、TabMWP 或 GQA。PlanBench-mini 120 episodes：生成 12 个工具、复用 108 次，执行 360 个分轴 verifier，joint success 1.0000、平均成本 0.4550。  多维验证工具自进化 Agent 工具与协作执行：把计划变成可检查的动作 为什么创建工具与使用工具要在同一策略中联合训练？ 只奖励生成可运行代码，可能得到难调用或不解决新题的工具；只训练使用者又无法改进工具设计。build 与 held-out use 混合任务把 schema、执行和最终结果信号连起来，鼓励可复用抽象；样例通过不是独立问题解决，使用评测仍需隔离。 例如工具能算训练样例却把常量写死，代码执行奖励可能通过，但 held-out 调用会失败，从而暴露它没有真正可复用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-smith-3e4d7833" class="ar-learning-paper-anchor"></span>
<h2 id="qa-26ea08414f79720d">为什么创建工具与使用工具要在同一策略中联合训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asmith">SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Appier AI Research / National Taiwan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只奖励生成可运行代码，可能得到难调用或不解决新题的工具；只训练使用者又无法改进工具设计。build 与 held-out use 混合任务把 schema、执行和最终结果信号连起来，鼓励可复用抽象；样例通过不是独立问题解决，使用评测仍需隔离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具能算训练样例却把常量写死，代码执行奖励可能通过，但 held-out 调用会失败，从而暴露它没有真正可复用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24571">原论文</a> · <a href="../../../../agent-research/2608.24571-smith/">实现解读</a> · <a href="#qa-26ea08414f79720d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pmcoder" data-paper-title="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution Agent Vanderbilt University 2026-08-07 用层级 phase planner 条件化 episodic retrieval，再用记忆轨迹统计检测 stuck 并重规划，以真实执行 verdict 验证。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  代码 Agent 记忆与规划 Agent 工具与协作执行：把计划变成可检查的动作 为什么 episodic retrieval 要由当前 phase 条件化，而非每步都对原 issue 做相同检索？ 定位、修改和验证阶段需要不同证据，固定检索容易重复返回主题相似但不适合当前动作的轨迹。层级规划用 phase 约束经验选择，再根据历史行为检测卡住并重规划；最终仍由真实执行 verdict 判断，不应把“计划切换了”当成问题已经解决。 例如定位阶段需要找相关文件，验证阶段需要已知回归测试；只按 issue 文本反复检索，可能一直返回定位经验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-pmcoder-088b3672" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d5a49a3fee65a642">为什么 episodic retrieval 要由当前 phase 条件化，而非每步都对原 issue 做相同检索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apmcoder">Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Vanderbilt University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>定位、修改和验证阶段需要不同证据，固定检索容易重复返回主题相似但不适合当前动作的轨迹。层级规划用 phase 约束经验选择，再根据历史行为检测卡住并重规划；最终仍由真实执行 verdict 判断，不应把“计划切换了”当成问题已经解决。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如定位阶段需要找相关文件，验证阶段需要已知回归测试；只按 issue 文本反复检索，可能一直返回定位经验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06811">原论文</a> · <a href="../../../../agent-research/2608.06811-pmcoder/">实现解读</a> · <a href="#qa-d5a49a3fee65a642">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:codegrep" data-paper-title="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents Agent NetEase Guangzhou AI Lab 2026-08-06 主题：代码检索 Agent。以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的代码检索 Agent 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  代码检索 Agent Agent 工具与协作执行：把计划变成可检查的动作 为什么代码检索 Agent 的奖励来自下游修复收益，而不只看找对文件？ 正确文件可能仍缺少调用链和约束，检索也可能耗费过多 token 与轮次。把结果交给冻结 coding agent，观察实际修复并计入成本，能评价证据是否可用；冻结执行器减少两侧同时变化的混淆，但单次下游失败也不自动证明某条证据无价值。 例如找到报错函数却没读其调用约束，修复器仍会改错；检索相关文件和测试上下文才可能真正提高可修复性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-codegrep-29277303" class="ar-learning-paper-anchor"></span>
<h2 id="qa-be1af93d2bb20565">为什么代码检索 Agent 的奖励来自下游修复收益，而不只看找对文件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acodegrep">CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Guangzhou AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确文件可能仍缺少调用链和约束，检索也可能耗费过多 token 与轮次。把结果交给冻结 coding agent，观察实际修复并计入成本，能评价证据是否可用；冻结执行器减少两侧同时变化的混淆，但单次下游失败也不自动证明某条证据无价值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如找到报错函数却没读其调用约束，修复器仍会改错；检索相关文件和测试上下文才可能真正提高可修复性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05886">原论文</a> · <a href="../../../../agent-research/2608.05886-codegrep/">实现解读</a> · <a href="#qa-be1af93d2bb20565">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:manta" data-paper-title="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems Agent Cornell University 2026-07-30 根据任务先验初始化通信拓扑，运行中监控协作 trace，并有界调整角色、边、顺序、可见性和验证路径。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  多 Agent 自进化 Agent 工具与协作执行：把计划变成可检查的动作 为什么通信拓扑调整要同时约束边、顺序与可见性，而非只增加更多 Agent？ 协作失败可能来自信息没传到、角色重复或验证路径缺失，人数增加不一定解决。运行轨迹驱动有界拓扑修改，把角色关系与信息流作为优化对象；预算投影限制额外通信和执行成本，改图的收益也须由实际任务反馈确认，不能仅以边数增加判断改进。 例如审查者一直看不到最新代码，应改消息可见性而非再加三名审查者；否则只是重复评估同一份旧材料。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-manta-a024f561" class="ar-learning-paper-anchor"></span>
<h2 id="qa-12a63e7249c622c4">为什么通信拓扑调整要同时约束边、顺序与可见性，而非只增加更多 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amanta">MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>协作失败可能来自信息没传到、角色重复或验证路径缺失，人数增加不一定解决。运行轨迹驱动有界拓扑修改，把角色关系与信息流作为优化对象；预算投影限制额外通信和执行成本，改图的收益也须由实际任务反馈确认，不能仅以边数增加判断改进。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如审查者一直看不到最新代码，应改消息可见性而非再加三名审查者；否则只是重复评估同一份旧材料。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28527">原论文</a> · <a href="../../../../agent-research/2607.28527-manta/">实现解读</a> · <a href="#qa-12a63e7249c622c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cam-df" data-paper-title="CAM-DF" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAM-DF Agent Peking University 2026-07-29 工具 router 只能给出相关性排序，不能回答“应该开放前几个工具”。CAM-DF 在任何工具执行前虚拟遍历排序前缀，以任务充分性减异构工具成本作为 payoff；停止当前前缀与最佳后续前缀的 payoff gap 决定标签，gap 绝对值决定错误的 regret 权重。 本地是确定性工具 mini-suite，不是 τ-bench Retail live execution；充分性来自 benchmark 可审计 required-tools，而不是另训的 scorer。ScaleMCP mini 为每个任务构造冻结排序和异构成本，枚举所有前缀的下游 payoff，执行 regret-weighted 停止并只挂载所选工具。  成本感知工具停止 Agent 工具与协作执行：把计划变成可检查的动作 停止标签为什么由当前前缀与最佳后续前缀的 payoff gap 决定？ 相关性排名不回答开放多少工具才足够，停止过早可能缺能力，继续过久又付出额外成本。虚拟前缀的充分性减成本形成 payoff，差值决定停或续，绝对差衡量选错的遗憾；这些评估发生在执行前，不能把虚拟收益写成真实工具成功率。 例如前两把工具已能完成任务，第三把虽相关却很贵，继续前缀收益更低；停止标签应考虑这部分成本而非只看排名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-cam-df-2b7f3d23" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0570cdc0a7c4faa1">停止标签为什么由当前前缀与最佳后续前缀的 payoff gap 决定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acam-df">CAM-DF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相关性排名不回答开放多少工具才足够，停止过早可能缺能力，继续过久又付出额外成本。虚拟前缀的充分性减成本形成 payoff，差值决定停或续，绝对差衡量选错的遗憾；这些评估发生在执行前，不能把虚拟收益写成真实工具成功率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前两把工具已能完成任务，第三把虽相关却很贵，继续前缀收益更低；停止标签应考虑这部分成本而非只看排名。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27083">原论文</a> · <a href="../../../../agent-research/2607.27083-cam-df/">实现解读</a> · <a href="#qa-0570cdc0a7c4faa1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbot" data-paper-title="Formalizing Mathematics at Scale" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Formalizing Mathematics at Scale Agent FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris 2026-05-28 先构建教材声明的依赖DAG，工作者在独立worktree写Lean，经并发审查和合并队列进入主库；失败轨迹生成技能，监督者在合并后核查目标并反馈重规划。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；开源框架不等于本地已运行。每书约一周；39目标的小书消融仍使用600M至1200M tokens，持续数小时。成本过高，不复现（审查 DONE），不调用付费模型、不启动Lean多Agent任务。保留源码和协议，无本地分数、GPU回执或evolve可执行映射，不重新排入自动队列。  多Agent协作 形式化验证与依赖调度 Agent 工具与协作执行：把计划变成可检查的动作 为什么数学形式化工作者要独立 worktree，并经合并队列后再核对全局目标？ 独立工作区减少并发文件冲突，依赖 DAG 指定可先形式化哪些声明，合并审查维护共享库一致性。局部 Lean 通过不保证所有教材目标都已覆盖，监督者还要对照全局进度重规划；失败经验可沉淀技能，但不能因分支存在就认定证明已合入。 例如两个工作者各证明一个引理，分别通过后仍需检查名称冲突及主定理依赖；不能把两个孤立文件当成完整教材已形式化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-autoformbot-6fe44000" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f57c0f41ebcd567f">为什么数学形式化工作者要独立 worktree，并经合并队列后再核对全局目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbot">Formalizing Mathematics at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立工作区减少并发文件冲突，依赖 DAG 指定可先形式化哪些声明，合并审查维护共享库一致性。局部 Lean 通过不保证所有教材目标都已覆盖，监督者还要对照全局进度重规划；失败经验可沉淀技能，但不能因分支存在就认定证明已合入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个工作者各证明一个引理，分别通过后仍需检查名称冲突及主定理依赖；不能把两个孤立文件当成完整教材已形式化。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29955">原论文</a> · <a href="../../../../agent-research/2605.29955-autoformbot/">实现解读</a> · <a href="#qa-f57c0f41ebcd567f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:prompts" data-paper-title="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving Agent University of Maryland / Google 2026-05-18 Coordinator、Analyzer 和 Proposal Agent 联合读取 profiler 与知识库，诊断瓶颈并输出可解释的 sharding 候选。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  训练服务优化 多 Agent 性能诊断 Agent 工具与协作执行：把计划变成可检查的动作 为什么 sharding 提案必须结合 profiler，而不能只检索一套常见最佳配置？ 最优并行方式取决于计算、通信和内存的实际瓶颈，知识库只提供候选经验。Analyzer 读测量定位约束，Proposal Agent 再提出可解释分片方案，Coordinator 组织验证；生成配置或公式自检不等于运行了训练系统，也不能把预计加速冒充实测。 例如模型卡说某配置快，但当前设备是通信受限；profiler 若显示 all-reduce 占主导，就需要针对通信重新比较方案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-prompts-61564db7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a638de4eb75357c6">为什么 sharding 提案必须结合 profiler，而不能只检索一套常见最佳配置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprompts">PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最优并行方式取决于计算、通信和内存的实际瓶颈，知识库只提供候选经验。Analyzer 读测量定位约束，Proposal Agent 再提出可解释分片方案，Coordinator 组织验证；生成配置或公式自检不等于运行了训练系统，也不能把预计加速冒充实测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型卡说某配置快，但当前设备是通信受限；profiler 若显示 all-reduce 占主导，就需要针对通信重新比较方案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/prompts-performance-optimization-via-multi-agent-planning-for-llm-training-and-serving/">原论文</a> · <a href="../../../../agent-research/mlsys2026-prompts/">实现解读</a> · <a href="#qa-a638de4eb75357c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:paperorchestra" data-paper-title="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing Agent Google Cloud AI Research 2026-04-06 PaperOrchestra 用 Outline、Plotting、Literature Review、Section Writing、Content Refinement 五个 Agent，把零散想法和实验日志转成含文献与图表的 LaTeX 稿件。大纲之后图示与文献检索并行，引用经过实体和时间截止核验，最终根据多维评价接受或回退修订；系统不负责替作者发明或执行新实验。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。无可执行 adapter、生成能力指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。原文附录 B 在 10 篇计时子集报告每文约 60–70 次 LLM 调用、39.6 分钟裁尾均值；完整 200 篇、多基线、多 judge 和人工评测成本远不止单次运行。写作需 Gemini3.1Pro，检索为 Gemini3Flash＋联网搜索，另有图像生成和多轮审稿。以上为作者报告和配置判断，不是本地测量，也不假设外部 API 免费或无限。  多Agent协作 研究与论文写作 Agent 工具与协作执行：把计划变成可检查的动作 为什么引用核验与修订接纳不能替代真实实验和论文论证？ 引用实体、摘要和截止时间检查只保证来源身份及时间资格，修订分数只约束既有内容的改写方向。五类写作 Agent 应基于真实想法与日志组织稿件，不负责凭空创造结果；机械 BibTeX 校验或判定器也不能被包装为完整文献综合与研究能力。 例如图表 Agent 可根据已有实验日志画曲线，却不能为让稿件完整而填一组想象指标；引用真实也不会使虚构结果变真。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-paperorchestra-986964dd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8dc7aca4108c4bbc">为什么引用核验与修订接纳不能替代真实实验和论文论证？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apaperorchestra">PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>引用实体、摘要和截止时间检查只保证来源身份及时间资格，修订分数只约束既有内容的改写方向。五类写作 Agent 应基于真实想法与日志组织稿件，不负责凭空创造结果；机械 BibTeX 校验或判定器也不能被包装为完整文献综合与研究能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图表 Agent 可根据已有实验日志画曲线，却不能为让稿件完整而填一组想象指标；引用真实也不会使虚构结果变真。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05018v1">原论文</a> · <a href="../../../../agent-research/2604.05018-paperorchestra/">实现解读</a> · <a href="#qa-8dc7aca4108c4bbc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aira2" data-paper-title="AIRA2: Overcoming Bottlenecks in AI Research Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AIRA2: Overcoming Bottlenecks in AI Research Agents Agent FAIR at Meta / University College London 2026-03-27 以无同步屏障的 steady-state worker pool 提高实验吞吐；训练、搜索、最终选择使用固定的 80/10/10 隐藏切分，搜索只看 search score，结束后才用未参与爬山的 validation 选冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。三种子诊断：metrics/mechanism-seeds42-44.json  AI 研究 Agent 异步进化 隐藏一致评测 Agent 工具与协作执行：把计划变成可检查的动作 为什么 steady-state worker pool 比每代等待全部实验结束更能利用计算资源？ 不同实验耗时不一，同步屏障会让快任务完成后闲等最慢者；持续池让空闲 worker 立即接下一候选。吞吐提升不应改变评测隔离：搜索仅用固定 search 分数，结束后再由未参与爬山的 validation 选冠军，不能边跑边偷看最终选择集。 例如三个实验十分钟完成、一个要一小时，同步代会浪费前三个槽位；持续池可继续试验，但仍共享预先冻结的数据切分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-aira2-3f4a88e8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6b1a28c04e252ad2">为什么 steady-state worker pool 比每代等待全部实验结束更能利用计算资源？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaira2">AIRA2: Overcoming Bottlenecks in AI Research Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University College London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同实验耗时不一，同步屏障会让快任务完成后闲等最慢者；持续池让空闲 worker 立即接下一候选。吞吐提升不应改变评测隔离：搜索仅用固定 search 分数，结束后再由未参与爬山的 validation 选冠军，不能边跑边偷看最终选择集。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三个实验十分钟完成、一个要一小时，同步代会浪费前三个槽位；持续池可继续试验，但仍共享预先冻结的数据切分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26499">原论文</a> · <a href="../../../../agent-research/2603.26499-aira2/">实现解读</a> · <a href="#qa-6b1a28c04e252ad2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dynamic-brt" data-paper-title="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair Agent Google 2026-01-27 论文让修复和 BRT 留在同一条轨迹；TDD、TLD、Freeform 改变生成顺序。BRT 必须在原 bug 上失败、生成修复上通过。选择器按非测试修复归组，避免不同测试拆散同一修复的票数；ranked 在多数修复组内优先保留测试。原文 §3 完整实验：成本过高，不复现（审查 DONE）。component_only / L1 机制诊断。component_only / L1 机制诊断。实现测试验证及选择器，没有实现或宣称 Passerine 生成 Agent 的能力。完整实验：成本过高，不复现（审查 DONE）。11 项单元测试已通过。自建 increment 算术实例真实启动独立 Python 子进程，观察 assertion_failed → passed；恒真测试、异常而非断言失败、未通过回归的修复均不接纳。ranked 与 dual 的不同选项已通过多数分组实例验证。诊断指标  代码 Agent 程序修复 测试与验证 Agent 工具与协作执行：把计划变成可检查的动作 测试在原 bug 上失败、在生成修复上通过，为什么还不能证明修复正确？ 自生成测试可能只覆盖修复碰巧满足的局部行为，二者相互吻合不等于原题完整语义。这个条件只定义候选 BRT；更强的可信判断还需隔离参考修复等验证。按非测试 patch 分组投票，也避免同一修复因配了不同测试而被拆散票数。 例如修复把返回值写成常量，自测也只检查这一个输入，两项条件都可能通过，但其他输入仍错，不能宣称真正修好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-dynamic-brt-f3fe2d3c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bc8c2cd9cd8b383e">测试在原 bug 上失败、在生成修复上通过，为什么还不能证明修复正确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adynamic-brt">Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自生成测试可能只覆盖修复碰巧满足的局部行为，二者相互吻合不等于原题完整语义。这个条件只定义候选 BRT；更强的可信判断还需隔离参考修复等验证。按非测试 patch 分组投票，也避免同一修复因配了不同测试而被拆散票数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如修复把返回值写成常量，自测也只检查这一个输入，两项条件都可能通过，但其他输入仍错，不能宣称真正修好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.19066">原论文</a> · <a href="../../../../agent-research/2601.19066-dynamic-brt/">实现解读</a> · <a href="#qa-bc8c2cd9cd8b383e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:watch-and-learn" data-paper-title="Watch and Learn: Learning to Use Computers from Online Videos" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Watch and Learn: Learning to Use Computers from Online Videos Agent The Ohio State University 2025-10-06 W&amp;L 把“视频里发生了什么操作”建模为逆动力学：输入前后两张屏幕图像，预测导致状态变化的动作。训练好的 IDM 再标注网络教程视频，结合任务检索形成轨迹，分别用于 CUA 的上下文示范和监督训练，而非直接让通用大模型猜动作或用规则恢复轨迹。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。本页没有可执行 adapter、组件指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。固定 v1 §3.1/附录 D.3 使用超过 630k 状态转移，IDM 训练为 8×A100 80GB、15 epochs；另有 53,125 个视频轨迹、7B CUA SFT、联网检索/API 和真实 OSWorld 桌面评测。该配置明显超过单张 A100/A30 或本地 Mac 的短时预算；这是作者配置形成的成本判断，不是本地计时。  工具与环境交互 计算机使用与视频示范 Agent 工具与协作执行：把计划变成可检查的动作 为什么看教程视频需要学习逆动力学，而不是把前后截图差异直接当成鼠标动作？ 视觉变化可能来自滚动、键盘输入或程序响应，仅像素差无法唯一确定操作。逆动力学模型在前后屏幕上预测动作类型、坐标与文本，再把推断串成轨迹供检索和训练；这些标签仍是模型估计，不能把规则恢复或随意猜动作冒充已训练的 IDM。 例如页面向下移动可能由滚轮也可能由按键触发，动作模型需结合画面与监督区分，而非看到内容下移就硬填一次点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-watch-and-learn-e9cf239b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6d5dc634ef7c4b6c">为什么看教程视频需要学习逆动力学，而不是把前后截图差异直接当成鼠标动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awatch-and-learn">Watch and Learn: Learning to Use Computers from Online Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视觉变化可能来自滚动、键盘输入或程序响应，仅像素差无法唯一确定操作。逆动力学模型在前后屏幕上预测动作类型、坐标与文本，再把推断串成轨迹供检索和训练；这些标签仍是模型估计，不能把规则恢复或随意猜动作冒充已训练的 IDM。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如页面向下移动可能由滚轮也可能由按键触发，动作模型需结合画面与监督区分，而非看到内容下移就硬填一次点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04673v1">原论文</a> · <a href="../../../../agent-research/2510.04673-watch-and-learn/">实现解读</a> · <a href="#qa-6d5dc634ef7c4b6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolgrad" data-paper-title="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients Agent Google 2025-08-06 先从目标答案反推工具轨迹，再使用 textual gradient 定位并修订失败调用，降低人工轨迹标注成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  工具学习 数据生成 Agent 工具与协作执行：把计划变成可检查的动作 从目标答案反推轨迹为什么只适合数据生成侧，而不能作为评测 Agent 的输入？ 反推利用已知答案构造候选工具链，textual gradient 再定位失败调用并修订，目的是减少训练轨迹标注。评测若把目标答案传给行动者，就已经泄漏任务目标值，不能衡量独立取证；训练数据的构造信息与部署时可见信息必须明确分开。 例如训练侧已知某城市人口，可反查需要哪些 API；测试时 Agent 应只接到人口问题，不能同时拿到参考数字再安排搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-toolgrad-568745ef" class="ar-learning-paper-anchor"></span>
<h2 id="qa-48defda29bfde8a3">从目标答案反推轨迹为什么只适合数据生成侧，而不能作为评测 Agent 的输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolgrad">ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反推利用已知答案构造候选工具链，textual gradient 再定位失败调用并修订，目的是减少训练轨迹标注。评测若把目标答案传给行动者，就已经泄漏任务目标值，不能衡量独立取证；训练数据的构造信息与部署时可见信息必须明确分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练侧已知某城市人口，可反查需要哪些 API；测试时 Agent 应只接到人口问题，不能同时拿到参考数字再安排搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.04086">原论文</a> · <a href="../../../../agent-research/2508.04086-toolgrad/">实现解读</a> · <a href="#qa-48defda29bfde8a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolrl" data-paper-title="ToolRL" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolRL Agent University of Illinois Urbana-Champaign 2025-04-16 联合优化工具选择、参数生成和执行结果；动态 reward scaling 让不同工具难度进入同一 RL batch。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.1250；方法特有操作有非零 telemetry。  工具强化学习 Agent 工具与协作执行：把计划变成可检查的动作 不同工具奖励难度不同时，为什么要做工具条件下的动态 scaling？ 容易工具的高原始奖励可能主导同一批更新，困难工具虽有进步却被淹没。按工具分布中心化和缩放，让相对表现更可比较，同时保留选择、参数、执行与答案多种信号；归一化不自动修正错误奖励定义，也不意味着所有工具实际难度相同。 例如计算器多数能成功，数据库复杂查询常失败；分别按各自奖励分布评价进步，避免训练只偏向更容易拿分的计算器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-toolrl-7e3d5cc8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-39b3cc929256b458">不同工具奖励难度不同时，为什么要做工具条件下的动态 scaling？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolrl">ToolRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>容易工具的高原始奖励可能主导同一批更新，困难工具虽有进步却被淹没。按工具分布中心化和缩放，让相对表现更可比较，同时保留选择、参数、执行与答案多种信号；归一化不自动修正错误奖励定义，也不意味着所有工具实际难度相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如计算器多数能成功，数据库复杂查询常失败；分别按各自奖励分布评价进步，避免训练只偏向更容易拿分的计算器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.13958">原论文</a> · <a href="../../../../agent-research/2504.13958-toolrl/">实现解读</a> · <a href="#qa-39b3cc929256b458">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:retool" data-paper-title="ReTool" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ReTool Agent ByteDance Seed 2025-04-15 策略在自然语言 reasoning 与工具执行之间交替，并由可执行反馈学习调用、纠错和停止。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.0500；方法特有操作有非零 telemetry。  推理中工具调用 Agent 工具与协作执行：把计划变成可检查的动作 工具调用带成本惩罚时，为什么不能简单训练成“尽量不调用工具”？ 策略目标同时包含答案收益，少调用只有在不显著损害结果时才有价值。交替推理与真实执行反馈让模型学习哪些步骤值得外包、失败后如何纠正以及何时停止；若只优化调用数，模型可能用流畅猜测替代必要计算，反而失去工具使用能力。 例如心算两位数可以省调用，但复杂统计应执行代码；一次可靠计算的收益可能远大于为省调用而给出错误答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-retool-db452677" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f341f5ec4e371354">工具调用带成本惩罚时，为什么不能简单训练成“尽量不调用工具”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aretool">ReTool</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略目标同时包含答案收益，少调用只有在不显著损害结果时才有价值。交替推理与真实执行反馈让模型学习哪些步骤值得外包、失败后如何纠正以及何时停止；若只优化调用数，模型可能用流畅猜测替代必要计算，反而失去工具使用能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如心算两位数可以省调用，但复杂统计应执行代码；一次可靠计算的收益可能远大于为省调用而给出错误答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.11536">原论文</a> · <a href="../../../../agent-research/2504.11536-retool/">实现解读</a> · <a href="#qa-f341f5ec4e371354">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openhands" data-paper-title="OpenHands" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="OpenHands Agent All-Hands-AI 2024-07-23 OpenHands 提供开放的软件 Agent 平台，把终端、编辑器、浏览器等动作统一到 event stream，并以 sandbox 隔离执行，覆盖修 bug、写代码和仓库维护。 浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。用编辑器、终端和可观测事件流驱动通用软件开发 Agent。已实现编辑器/终端事件和真实代码 sandbox；浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。本地将 file-editor 与 terminal 动作写入 event stream；terminal 在独立临时目录执行固定回归测试，最终报告动作、编辑 hash、命令输出和 success。  通用软件 Agent Agent 工具与协作执行：把计划变成可检查的动作 统一 event stream 为什么有助于把终端、编辑器和浏览器串成可检查的软件工作流？ 每个动作与 sandbox 返回都进入同一时序记录，后续策略可依据真实反馈继续，审阅者也能追踪修改和验证的来源。统一事件不意味着各种工具语义相同，更不等于代码已安全或正确；执行隔离、权限和实际测试仍承担各自职责。 例如编辑事件修改文件，终端事件跑测试，浏览器事件核对页面；统一记录能判断测试究竟发生在修改前还是修改后。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-openhands-e21fcd2c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7201d318abb3e27c">统一 event stream 为什么有助于把终端、编辑器和浏览器串成可检查的软件工作流？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aopenhands">OpenHands</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · All-Hands-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个动作与 sandbox 返回都进入同一时序记录，后续策略可依据真实反馈继续，审阅者也能追踪修改和验证的来源。统一事件不意味着各种工具语义相同，更不等于代码已安全或正确；执行隔离、权限和实际测试仍承担各自职责。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如编辑事件修改文件，终端事件跑测试，浏览器事件核对页面；统一记录能判断测试究竟发生在修改前还是修改后。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16741">原论文</a> · <a href="../../../../agent-research/2407.16741-openhands/">实现解读</a> · <a href="#qa-7201d318abb3e27c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-agent" data-paper-title="SWE-agent" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-agent Agent Princeton University 2024-05-06 通用 shell 对 LLM 而言动作空间过宽、输出冗长。SWE-agent 用专门 ACI 约束仓库搜索、文件查看、精确编辑和测试，让模型能围绕 issue 定位故障并验证 patch。 为软件工程 Agent 设计面向仓库浏览、编辑和测试的 Agent-Computer Interface。这是可执行的 SWE-style micro benchmark，不是官方 SWE-bench Lite 数据与 Docker 镜像。名称 swebench-local 明确保留该区别，不能将本地 success 当作论文 resolved rate。本地 ACI 只暴露读文件、写 solution.py 和固定 unittest 命令；每题初始仓库必须先真实失败，Agent 定位、编辑并以退出码验证。  软件工程 ACI Agent 工具与协作执行：把计划变成可检查的动作 专门 ACI 为什么可能比给模型无限制 shell 更有效？ 动作空间过宽和冗长输出会增加选择与定位负担，专门界面把搜索、查看、精确编辑和测试变成更易理解的操作反馈。改进的是 Agent 与仓库的交互合同，不是给模型偷偷提供正确 patch；界面约束也不能替代真正执行测试与检查任务完成。 例如只展示目标函数附近行并提供精确替换，比把整个文件打印进提示更易定位，但仍要运行回归测试确认修改有效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-swe-agent-79904a33" class="ar-learning-paper-anchor"></span>
<h2 id="qa-dafefde79785114c">专门 ACI 为什么可能比给模型无限制 shell 更有效？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-agent">SWE-agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动作空间过宽和冗长输出会增加选择与定位负担，专门界面把搜索、查看、精确编辑和测试变成更易理解的操作反馈。改进的是 Agent 与仓库的交互合同，不是给模型偷偷提供正确 patch；界面约束也不能替代真正执行测试与检查任务完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只展示目标函数附近行并提供精确替换，比把整个文件打印进提示更易定位，但仍要运行回归测试确认修改有效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.15793">原论文</a> · <a href="../../../../agent-research/2405.15793-swe-agent/">实现解读</a> · <a href="#qa-dafefde79785114c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autogen" data-paper-title="AutoGen" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AutoGen Agent Microsoft Research 2023-08-16 复杂应用常需要多个模型、工具和人类协作，手写控制流难复用。AutoGen 提供 ConversableAgent 与 conversation programming：每个角色声明能力、回复策略和终止条件，通过群聊或嵌套会话组合成工作流。 AutoGen 把 Agent 抽象为可对话、可配置的角色，用消息路由和终止条件编排 planner、executor、critic、人类或工具。实现 planner/executor/critic 的消息协议、角色交接与显式终止；未嵌入完整 AutoGen 运行时、容器代码执行或真实 LLM 群聊，1.0 是确定性控制流测试而非论文应用得分。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.0000，记录 120 份 plan、360 条跨角色消息和 120 次 critic round。  多 Agent Agent 工具与协作执行：把计划变成可检查的动作 对话编程为什么需要显式终止条件，而不能让多个角色一直互相回复？ 消息本身可以不断触发新回复，若没有角色职责、工具边界和停止规则，协作容易重复或形成循环。conversation programming 把这些规则变成可组合控制流，适合群聊与嵌套会话；角色数量增加并不保证分工正确，最终仍需可验证产物判断完成。 例如写作者与审查者每轮都说“再优化一下”会无限往返；约定验证通过或预算耗尽时结束，才能形成可控工作流。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-autogen-60994f2d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-47f466dc66f53411">对话编程为什么需要显式终止条件，而不能让多个角色一直互相回复？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautogen">AutoGen</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>消息本身可以不断触发新回复，若没有角色职责、工具边界和停止规则，协作容易重复或形成循环。conversation programming 把这些规则变成可组合控制流，适合群聊与嵌套会话；角色数量增加并不保证分工正确，最终仍需可验证产物判断完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如写作者与审查者每轮都说“再优化一下”会无限往返；约定验证通过或预算耗尽时结束，才能形成可控工作流。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.08155">原论文</a> · <a href="../../../../agent-research/2308.08155-autogen/">实现解读</a> · <a href="#qa-47f466dc66f53411">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:metagpt" data-paper-title="MetaGPT" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MetaGPT Agent DeepWisdom 2023-08-01 简单串联多个聊天 Agent 容易让幻觉级联。MetaGPT 把人类软件团队的 SOP 编码成角色化消息流程，每个角色生产结构化中间物，由下游角色消费和验证。 用标准作业流程（SOP）把软件需求依次交给产品、架构、工程和测试角色。保留 SOP、角色交付物、真实编辑与测试；本地不是完整 MetaGPT LLM 对话，也不是官方 SWE-bench Lite，fixture 仅验证执行链路和可审计 trace。每个 episode 创建真实临时 Python 仓库；四个角色留下结构化 artifact，工程角色修改文件，QA 角色通过固定 python -m unittest -q 执行回归测试。  多 Agent 软件工程 Agent 工具与协作执行：把计划变成可检查的动作 结构化中间物为什么比角色间自由聊天更能抑制软件工作流的幻觉级联？ 下游依赖清晰的需求、设计和测试合同，能检查上游是否提供必要字段与约束，而不只接收自然语言承诺。SOP 规定角色顺序和消费关系，使错误更易定位；结构化不等于内容正确，仍需要下游验证与真实执行，不能把格式齐全当成可用软件。 例如架构师输出明确接口，工程师才能核对实现签名；若只收到“系统设计好了”，后续各角色可能各自想象不同约定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-metagpt-ffaa73e8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-03055a1e793d577f">结构化中间物为什么比角色间自由聊天更能抑制软件工作流的幻觉级联？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ametagpt">MetaGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepWisdom</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>下游依赖清晰的需求、设计和测试合同，能检查上游是否提供必要字段与约束，而不只接收自然语言承诺。SOP 规定角色顺序和消费关系，使错误更易定位；结构化不等于内容正确，仍需要下游验证与真实执行，不能把格式齐全当成可用软件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如架构师输出明确接口，工程师才能核对实现签名；若只收到“系统设计好了”，后续各角色可能各自想象不同约定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.00352">原论文</a> · <a href="../../../../agent-research/2308.00352-metagpt/">实现解读</a> · <a href="#qa-03055a1e793d577f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolbench" data-paper-title="ToolBench" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolBench Agent Tsinghua University 2023-05-25 分析开源 LLM 工具失败后，组合程序化使用样例、system prompt、in-context demonstration retriever 与生成格式约束。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.8400。  工具指令与评测 Agent 工具与协作执行：把计划变成可检查的动作 为什么检索调用示例之外，还需要格式约束和真实执行检查？ 示例帮助模型理解何时以及怎样用工具，却不保证新调用满足 schema 或参数语义。格式约束控制可解析性，执行结果再检查调用是否实现目标；三者分别补充经验、合同与环境反馈，不能用一个看起来像 JSON 的字符串替代真实工具能力。 例如模型检索到天气 API 示例后生成字段齐全的调用，城市参数却写错；JSON 合法仍不代表查到了用户所需城市的天气。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-toolbench-89c52f4b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-effa1825464a63ea">为什么检索调用示例之外，还需要格式约束和真实执行检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolbench">ToolBench</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>示例帮助模型理解何时以及怎样用工具，却不保证新调用满足 schema 或参数语义。格式约束控制可解析性，执行结果再检查调用是否实现目标；三者分别补充经验、合同与环境反馈，不能用一个看起来像 JSON 的字符串替代真实工具能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型检索到天气 API 示例后生成字段齐全的调用，城市参数却写错；JSON 合法仍不代表查到了用户所需城市的天气。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16504">原论文</a> · <a href="../../../../agent-research/2305.16504-toolbench/">实现解读</a> · <a href="#qa-effa1825464a63ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:critic" data-paper-title="CRITIC" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CRITIC Agent Microsoft 2023-05-19 仅让 LLM 反思自己的文本可能重复同一错误。CRITIC 调用搜索、代码解释器等外部工具，把可观测反馈带回修订循环，使 critique 有环境证据。 让 Agent 用外部工具验证初稿，再依据真实反馈自我修正。外部反馈和迭代改码是真实执行的；反馈源仅为受控代码测试，没有搜索引擎、toxicity classifier 或通用 LLM critic。Agent 先写入一个有缺陷 patch，真实运行 unittest 获取 traceback，再根据反馈写入正确 patch 并复测；报告记录每轮编辑、命令、退出码和输出。  工具反馈 Agent 工具与协作执行：把计划变成可检查的动作 为什么外部工具反馈比模型只重读自己的答案更可能发现重复性错误？ 同一模型的自我批评可能沿用原先错误假设，工具提供独立可观察约束，例如搜索事实或代码执行结果。修订围绕这些证据改变答案，形成闭环；工具也可能失败或无结果，不能把没有反馈当成已验证正确，更不能伪造成功检查。 例如答案算错乘积，模型重读仍觉得合理，实际运行计算器会给出不同数值，修订才能针对明确矛盾而非泛泛反思。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-critic-11dab3d3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1766e55c41f638fd">为什么外部工具反馈比模型只重读自己的答案更可能发现重复性错误？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acritic">CRITIC</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一模型的自我批评可能沿用原先错误假设，工具提供独立可观察约束，例如搜索事实或代码执行结果。修订围绕这些证据改变答案，形成闭环；工具也可能失败或无结果，不能把没有反馈当成已验证正确，更不能伪造成功检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如答案算错乘积，模型重读仍觉得合理，实际运行计算器会给出不同数值，修订才能针对明确矛盾而非泛泛反思。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.11738">原论文</a> · <a href="../../../../agent-research/2305.11738-critic/">实现解读</a> · <a href="#qa-1766e55c41f638fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:camel" data-paper-title="CAMEL" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAMEL Agent King Abdullah University of Science and Technology 2023-03-31 用 inception prompting 固定 user/assistant 的角色、目标和边界，通过轮流消息完成任务并生成可研究的多 Agent 社会轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.3500。  多 Agent 协作 Agent 工具与协作执行：把计划变成可检查的动作 inception prompting 固定角色、目标和边界，为什么不仅是给两个模型起名字？ 角色提示影响双方职责、可提出的请求及如何配合，轮流消息在这些约束下推进共同任务。若只换名称却没有能力与边界差异，可能得到两段重复回答而非协作；社会轨迹的存在也不是目标已达成的证据，需要另行检查任务产物。 例如一方提出实现需求、另一方负责写方案，并约定不能更改总目标；若两者都只夸赞对方，聊天很长也没有工作推进。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-camel-640cbec7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-03d873922f3e2ffc">inception prompting 固定角色、目标和边界，为什么不仅是给两个模型起名字？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acamel">CAMEL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · King Abdullah University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>角色提示影响双方职责、可提出的请求及如何配合，轮流消息在这些约束下推进共同任务。若只换名称却没有能力与边界差异，可能得到两段重复回答而非协作；社会轨迹的存在也不是目标已达成的证据，需要另行检查任务产物。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一方提出实现需求、另一方负责写方案，并约定不能更改总目标；若两者都只夸赞对方，聊天很长也没有工作推进。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17760">原论文</a> · <a href="../../../../agent-research/2303.17760-camel/">实现解读</a> · <a href="#qa-03d873922f3e2ffc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hugginggpt" data-paper-title="HuggingGPT" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="HuggingGPT Agent Zhejiang University 2023-03-30 单个 LLM 难以覆盖视觉、语音和其他专业任务，而模型社区已有大量专家。HuggingGPT 让 ChatGPT 充当控制器：先把请求拆成带依赖的子任务，再按 Hugging Face 模型描述匹配专家，按拓扑顺序执行，最后把多模型输出组织为用户答案。 本页实现 task planning、按能力描述选择模型、依赖图执行和最终汇总四阶段。复现控制流、能力匹配和依赖执行；没有下载数百个 Hugging Face 模型，也未调用 ChatGPT。mini-suite 的 1.0 表示编排一致，不代表论文跨模态能力。PlanBench mini 120 episodes、seed 42；工具描述充当本地模型 capability registry，每个子任务保留 dependency edge 后执行。  专家模型编排 Agent 工具与协作执行：把计划变成可检查的动作 为什么多模态专家执行要遵守子任务依赖，而不是把所有模型同时调用？ 后续专家的输入可能是前面检测、识别或转写的输出，没有这些结果就无法正确调用。控制器先建依赖图，再按模型描述选择能力并拓扑执行，最后汇总；模型名称相似不证明接口兼容，独立任务才适合并行，依赖链不能被忽略。 例如先语音转写再翻译，需要把真实转写送入翻译器；两者同时启动并让翻译器猜转写内容，会破坏证据链。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-hugginggpt-c07a7bb7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a9a80e3694f3511f">为什么多模态专家执行要遵守子任务依赖，而不是把所有模型同时调用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahugginggpt">HuggingGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后续专家的输入可能是前面检测、识别或转写的输出，没有这些结果就无法正确调用。控制器先建依赖图，再按模型描述选择能力并拓扑执行，最后汇总；模型名称相似不证明接口兼容，独立任务才适合并行，依赖链不能被忽略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先语音转写再翻译，需要把真实转写送入翻译器；两者同时启动并让翻译器猜转写内容，会破坏证据链。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17580">原论文</a> · <a href="../../../../agent-research/2303.17580-hugginggpt/">实现解读</a> · <a href="#qa-a9a80e3694f3511f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:art" data-paper-title="ART" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ART Agent University of Washington 2023-03-16 既有 tool-use prompting 常需为每个任务手写示例和调用顺序。ART 根据新任务自动检索相近的推理/工具示例，让冻结 LLM 生成程序；运行器遇到工具标记就暂停生成，执行工具并注入结果后继续。人可以用少量修订扩展任务库。 本页复现任务库检索、程序式多步推理、工具调用处暂停/恢复和成功示例写回，不把 mini-suite 写成完整 BIG-Bench/MMLU。保留自动示例检索、程序生成控制流、工具暂停和库更新；本地任务库很小，不调用冻结大模型，也未复刻 BIG-Bench/MMLU 原始分数。PlanBench mini 120 episodes、seed 42；按工具签名组织任务库，并逐工具暂停/恢复。  自动工具推理 Agent 工具与协作执行：把计划变成可检查的动作 为什么遇到工具标记时暂停生成、执行后再续写，比一次性写完含结果的程序更可靠？ 暂停让后续文本条件化于真实工具返回，避免模型预先想象执行结果。自动检索推理与工具示例减少手工提示负担，但运行器仍要识别标记并注入观察；冻结模型只是参数不更新，工具反馈仍会改变当前上下文和后续生成。 例如生成到数据库查询标记便执行，得到三条记录再汇总；不能先写出“查到十条”再补一段未执行查询装饰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-art-62b00229" class="ar-learning-paper-anchor"></span>
<h2 id="qa-16afeb1e858f4dd5">为什么遇到工具标记时暂停生成、执行后再续写，比一次性写完含结果的程序更可靠？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aart">ART</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>暂停让后续文本条件化于真实工具返回，避免模型预先想象执行结果。自动检索推理与工具示例减少手工提示负担，但运行器仍要识别标记并注入观察；冻结模型只是参数不更新，工具反馈仍会改变当前上下文和后续生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如生成到数据库查询标记便执行，得到三条记录再汇总；不能先写出“查到十条”再补一段未执行查询装饰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.09014">原论文</a> · <a href="../../../../agent-research/2303.09014-art/">实现解读</a> · <a href="#qa-16afeb1e858f4dd5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolformer" data-paper-title="Toolformer" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Toolformer Agent Meta AI Research 2023-02-09 手工标注工具调用昂贵，纯 prompting 又难以让较小模型稳定决定何时调用。Toolformer 先用少量 demonstration 采样 API call，再比较插入真实返回值、隐藏返回值和完全不调用时的后续 token loss，只保留确实有用的调用并继续语言模型训练。 本页实现候选 API call 生成、no-call/masked-call loss 对照和自监督过滤，只保留能降低预测 loss 的工具调用。实现自监督候选过滤的核心判据，但 loss 来自确定性 tool utility，不是 GPT-J token loss；未进行 6.7B continued training，也未复刻论文五类真实 API。ScaleMCP mini 对 required 和 distractor tools 都生成候选，只有相对 no-call 降低 loss 的调用被接受。  工具学习 Agent 工具与协作执行：把计划变成可检查的动作 为什么筛选 API 调用要比较有返回、隐藏返回与不调用时的后续 loss？ 只看调用字符串可能把有用提示格式误认为真实工具价值。对照不同返回条件，检查实际结果是否降低后续预测损失，再保留超过门槛的调用训练模型，才能更接近学习调用效用；这个自监督代理也不等于所有任务正确率或真实业务收益。 例如计算器调用形式本身不告诉乘积，只有注入正确返回才改善后续预测，筛选才有理由保留这次计算调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-toolformer-dc9c6efa" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bf11c35f247b81e0">为什么筛选 API 调用要比较有返回、隐藏返回与不调用时的后续 loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolformer">Toolformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只看调用字符串可能把有用提示格式误认为真实工具价值。对照不同返回条件，检查实际结果是否降低后续预测损失，再保留超过门槛的调用训练模型，才能更接近学习调用效用；这个自监督代理也不等于所有任务正确率或真实业务收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如计算器调用形式本身不告诉乘积，只有注入正确返回才改善后续预测，筛选才有理由保留这次计算调用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2302.04761">原论文</a> · <a href="../../../../agent-research/2302.04761-toolformer/">实现解读</a> · <a href="#qa-bf11c35f247b81e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pal" data-paper-title="PAL" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PAL Agent Carnegie Mellon University 2022-11-18 LLM 擅长把问题分解成步骤，却会在算术和符号执行阶段出错。PAL 让 LLM 输出带变量和控制流的程序，最终计算完全交给 Python 等确定性 runtime；模型只承担自然语言理解和程序合成。 本页复现“语言模型生成程序、符号 runtime 执行、返回解释器答案”的系统边界，不把结构化 task program 写成 Codex 生成代码。保留神经程序生成与符号执行的职责分离；本地使用受控中间表示而非任意 Python，不调用 Codex，也未复刻原论文 GSM8K。ScaleMCP mini 120 episodes、seed 42；每题实际构建 CALL/RETURN 程序并由本地解释器执行。  程序推理 Agent 工具与协作执行：把计划变成可检查的动作 把算术交给 Python 后，模型为什么仍可能给出错误答案？ 确定性 runtime 保证执行给定程序，不保证程序正确表达题意。模型还要理解变量、关系和控制流，若把折扣顺序或单位写错，Python 会精确执行错误逻辑；PAL 分离程序合成与计算执行，降低算术出错但并不消除建模错误。 例如题意先打折再加运费，程序却给总额一起打折，计算器执行无误，最终价格仍与用户要求不符。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-pal-f0f14e4c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c9d3e89879637bdf">把算术交给 Python 后，模型为什么仍可能给出错误答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apal">PAL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>确定性 runtime 保证执行给定程序，不保证程序正确表达题意。模型还要理解变量、关系和控制流，若把折扣顺序或单位写错，Python 会精确执行错误逻辑；PAL 分离程序合成与计算执行，降低算术出错但并不消除建模错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如题意先打折再加运费，程序却给总额一起打折，计算器执行无误，最终价格仍与用户要求不符。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.10435">原论文</a> · <a href="../../../../agent-research/2211.10435-pal/">实现解读</a> · <a href="#qa-c9d3e89879637bdf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mrkl" data-paper-title="MRKL" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MRKL Agent AI21 Labs 2022-05-01 单个 LLM 容易在精确计算、时效知识和可验证推理上失败。MRKL 把 LLM 放入系统架构，由 router 根据输入选择语言模型、知识库、计算器等专家；离散模块保证确定性能力，语言模型负责理解和自然语言接口。 本页实现显式 router、神经/离散专家注册表和结果汇总；不是让一个通用 prompt 直接返回正确工具链。保留 router 和可区分的专家执行计数；本地专家是确定性 mini-suite 工具，不调用 Jurassic-X、真实搜索服务或私有知识库，成本是统一代理成本而非线上延迟。ScaleMCP mini 120 episodes、seed 42；每个工具动作都先经 router，计算器、日历、地图、天气、数据库和表格进入离散专家。  神经符号路由 Agent 工具与协作执行：把计划变成可检查的动作 路由到确定性模块，为什么不能据此保证整个系统答案确定正确？ 计算器或数据库只在各自合同内可靠，路由器仍可能选错模块或传错输入，语言层也可能误解和错误组织结果。MRKL 的价值在于把精确能力从语言生成中拆出，明确各模块边界；局部确定性与端到端任务正确性是两层不同保证。 例如用户问含税价格，路由器虽调用计算器，却传入错误税率；结果可重复且精确，仍不是正确业务答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-mrkl-816ab670" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3b8ae0b3087063fb">路由到确定性模块，为什么不能据此保证整个系统答案确定正确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amrkl">MRKL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AI21 Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>计算器或数据库只在各自合同内可靠，路由器仍可能选错模块或传错输入，语言层也可能误解和错误组织结果。MRKL 的价值在于把精确能力从语言生成中拆出，明确各模块边界；局部确定性与端到端任务正确性是两层不同保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户问含税价格，路由器虽调用计算器，却传入错误税率；结果可重复且精确，仍不是正确业务答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.00445">原论文</a> · <a href="../../../../agent-research/2205.00445-mrkl/">实现解读</a> · <a href="#qa-3b8ae0b3087063fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:saycan" data-paper-title="SayCan" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SayCan Agent Robotics at Google 2022-04-04 LLM 知道“应该做什么”，却不知道当前机器人“能不能做”。SayCan 为每个预训练技能同时计算语言相关性和 value-function affordance，选择乘积最高的技能并执行，再把动作追加到上下文继续规划。 本页复现逐步技能枚举及“语言分数 × affordance”决策，不把确定性工具 mini-suite 冒充真实移动机械臂。保留双分数逐步规划与不可行技能过滤；affordance 是确定性本地可执行性，不含视觉、机器人控制策略或真实 value-function 训练。PlanBench mini 120 episodes、seed 42；每一步同时打分必要技能和干扰技能。  具身规划 Agent 工具与协作执行：把计划变成可检查的动作 语言相关性与 affordance 相乘，为什么能过滤“合理但做不到”的动作？ 语言模型衡量技能与指令、历史是否匹配，价值函数衡量当前环境下执行成功的可能，两者乘积要求语义合适且物理可行。单靠语言可能建议拿取够不到的物体，单靠可行性又可能执行无关动作；评分仍依赖技能库与价值估计的覆盖。 例如指令要拿杯子，但杯子在锁柜里，直接抓取语言上相关却可行性低；先开柜可能更适合作为下一技能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-saycan-7674e520" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ff44151b17aba420">语言相关性与 affordance 相乘，为什么能过滤“合理但做不到”的动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asaycan">SayCan</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Robotics at Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言模型衡量技能与指令、历史是否匹配，价值函数衡量当前环境下执行成功的可能，两者乘积要求语义合适且物理可行。单靠语言可能建议拿取够不到的物体，单靠可行性又可能执行无关动作；评分仍依赖技能库与价值估计的覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如指令要拿杯子，但杯子在锁柜里，直接抓取语言上相关却可行性低；先开柜可能更适合作为下一技能。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2204.01691">原论文</a> · <a href="../../../../agent-research/2204.01691-saycan/">实现解读</a> · <a href="#qa-ff44151b17aba420">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webgpt" data-paper-title="WebGPT" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="WebGPT Agent OpenAI 2021-12-17 长文本问答容易幻觉，且很难核查依据。WebGPT 让模型在文本浏览器里搜索、点击和滚动，回答必须收集引用；训练先做行为克隆，再用人类偏好 reward model 从多条浏览/回答轨迹中做拒绝采样。 本页复现文本浏览轨迹、证据引用和 reward-model 拒绝采样；本地确定性工具环境不是实时互联网浏览。保留 browser-action、citation constraint 和 trajectory rejection sampling；不访问实时网页、不训练 GPT-3/reward model，也不复刻 ELI5 人评。ScaleMCP mini 120 episodes、seed 42；每题生成两条工具轨迹，按证据覆盖选择。  浏览问答 Agent 工具与协作执行：把计划变成可检查的动作 带引用的浏览轨迹为什么还要经过人类偏好排序，而不只要求附上网址？ 网址存在不保证证据支持结论或回答满足问题，浏览过程与最终组织都需要质量判断。行为克隆先学习操作，再由偏好奖励选择较好轨迹；引用提供可核查入口，却不能让断章取义或未访问来源自动变可靠，仍需对应具体主张。 例如两段回答都贴了同一新闻链接，一段准确区分事件时间，另一段夸大结论；仅检查链接数量无法选出更好的答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-webgpt-13267288" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cb490f6e472d9e28">带引用的浏览轨迹为什么还要经过人类偏好排序，而不只要求附上网址？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awebgpt">WebGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>网址存在不保证证据支持结论或回答满足问题，浏览过程与最终组织都需要质量判断。行为克隆先学习操作，再由偏好奖励选择较好轨迹；引用提供可核查入口，却不能让断章取义或未访问来源自动变可靠，仍需对应具体主张。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两段回答都贴了同一新闻链接，一段准确区分事件时间，另一段夸大结论；仅检查链接数量无法选出更好的答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2112.09332">原论文</a> · <a href="../../../../agent-research/2112.09332-webgpt/">实现解读</a> · <a href="#qa-cb490f6e472d9e28">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

模型已经有计划，怎样选择工具、解释返回值，并让多个角色共享可靠的执行状态？

## 记住这一点

工具调用需要完整契约：何时调用、参数是什么、返回值如何改变下一步、失败如何记录。Toolformer 用后续预测损失过滤有用的 API 调用；CRITIC 用外部工具反馈修订回答。协作系统在此基础上再分工、交接状态与核对产物。角色数量只是组织方式，真正起作用的是信息和责任怎样流动，以及工具是否实际执行。

## 一个例子

以修复一个仓库问题为例：检索角色定位代码，执行角色修改文件并运行测试，复核角色读取真实 diff 与测试输出。若执行超时，记录为超时，不把“已发出命令”写成成功。若测试报错来自环境，先区分环境故障与修复失败；让三个角色分别说“看起来正确”，并没有替代可执行检查。

## 什么时候要小心

工具返回是待验证的输入，可能过期、被注入或不完整。需要限制权限、保留失败与未知结果，避免重复执行有副作用的动作。当前库中的接口、候选调用过滤和小环境循环有各自复现边界；它们不自动构成完整浏览器、生产服务或软件工程 benchmark 能力。

## 先读这几篇

先读 Toolformer，理解调用何时有用；再读 CRITIC，观察工具证据怎样进入修订；最后读 SWE-agent，把单次调用扩展为有状态的仓库操作与测试循环。

1. [Toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [原论文](https://arxiv.org/abs/2302.04761)
2. [CRITIC](../../../agent-research/2305.11738-critic/README.md) · [原论文](https://arxiv.org/abs/2305.11738)
3. [SWE-agent](../../../agent-research/2405.15793-swe-agent/README.md) · [原论文](https://arxiv.org/abs/2405.15793)

## 自测一下

一个角色生成补丁，另一个角色赞同，第三个角色宣告通过；没有任何测试执行记录，能算验证完成吗？

??? note "展开参考答案"

    不能。多角色共识仍可能共享同一个错误。应说明验收条件，实际执行相关检查并读取结果；未执行或中断的检查单独保留。若工具不允许执行，就把结论限制为静态审查，不能把角色对话计为测试通过。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
