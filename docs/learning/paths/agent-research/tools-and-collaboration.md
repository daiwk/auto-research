---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 工具与协作执行：把计划变成可检查的动作

[Agent](index.md) / 子主题导学 · 约 3 分钟 · 49 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 49 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning Agent KAIST AI / Meta Superintelligence Labs 2026-10-17 固定检索pipeline把召回数量、融合和返回上下文绑在一起。RPL让策略生成短程序组合稀疏/稠密召回、RRF、去重和重排，只将显式打印的证据交回模型。为解决稀疏奖励难探索的问题，保留策略已有query，对最后一次检索程序做受语法约束的结构变异；执行核验通过后生成续写轨迹，再穿插蒸馏与RL。§3及附录B 成本过高，不复现（审查 DONE）；RetrievalProgram最多4个不同query，宽度取论文阶梯，最多20篇显式输出；execute只解释数据类并调用注入的SDK，不解析或执行Python源码。多路检索实际执行RRF，单路、列表内部或跨路遇到相同ID不同内容时统一拒绝，只有内容完全一致的重复才去重；重排不得注入召回外文档。RRF常数60是明确的本地惯例；输出是文档数上限，不是假装实现了论文2048-token观测限制。  检索与工具 可编程检索与结构变异 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-rpl-95ce1341">Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning</h2>
<p class="ar-learning-card__meta">KAIST AI / Meta Superintelligence Labs · 论文公开：2026-10-17</p>
<p><strong>方法要点：</strong>固定检索pipeline把召回数量、融合和返回上下文绑在一起。RPL让策略生成短程序组合稀疏/稠密召回、RRF、去重和重排，只将显式打印的证据交回模型。为解决稀疏奖励难探索的问题，保留策略已有query，对最后一次检索程序做受语法约束的结构变异；执行核验通过后生成续写轨迹，再穿插蒸馏与RL。§3及附录B</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）；RetrievalProgram最多4个不同query，宽度取论文阶梯，最多20篇显式输出；execute只解释数据类并调用注入的SDK，不解析或执行Python源码。多路检索实际执行RRF，单路、列表内部或跨路遇到相同ID不同内容时统一拒绝，只有内容完全一致的重复才去重；重排不得注入召回外文档。RRF常数60是明确的本地惯例；输出是文档数上限，不是假装实现了论文2048-token观测限制。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24854">原论文</a> · <a href="../../../../agent-research/2610.24854-rpl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds Agent Massachusetts Institute of Technology 2026-10-16 传统代码Agent评测通常分配一个预定义issue，难以衡量多个维护者如何自主找任务、分工和跨仓库改进。Software World由真实依赖库构成，让Agent用持久记忆、issue、PR和发布进行长期协作，以不可见的下游包检查群体产出是否真正有用。SW-Env用Harbor会话和Forgejo模拟软件维护环境，通信权限、仓库所有权与会话预算可独立控制；SW-Eval在隐藏依赖包上安装冻结版本，测正确性与指令计数，避免只优化自己看到的微基准。多会话持久状态不是无限增长的单条对话。 仅研究资料，成本过高，不复现（审查 DONE）。仅研究资料，成本过高，不复现（审查 DONE）。没有本地软件世界、Agent实验或能力指标。完整复现需要多仓库构建、隔离部署、代码执行沙箱、真实模型会话及大量隐藏下游评测；原论文规模已明显超过单卡A100/A30与Mac低成本预算。成本过高，不复现（审查 DONE）。不克隆和执行未知项目脚本、不伪造本地Agent成绩、不保留自动运行队列，也不宣称Evolve已接入。  多Agent协作 软件生态与自进化评测 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-world-of-swecraft-5a1942f1">World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds</h2>
<p class="ar-learning-card__meta">Massachusetts Institute of Technology · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>传统代码Agent评测通常分配一个预定义issue，难以衡量多个维护者如何自主找任务、分工和跨仓库改进。Software World由真实依赖库构成，让Agent用持久记忆、issue、PR和发布进行长期协作，以不可见的下游包检查群体产出是否真正有用。SW-Env用Harbor会话和Forgejo模拟软件维护环境，通信权限、仓库所有权与会话预算可独立控制；SW-Eval在隐藏依赖包上安装冻结版本，测正确性与指令计数，避免只优化自己看到的微基准。多会话持久状态不是无限增长的单条对话。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>仅研究资料，成本过高，不复现（审查 DONE）。仅研究资料，成本过高，不复现（审查 DONE）。没有本地软件世界、Agent实验或能力指标。完整复现需要多仓库构建、隔离部署、代码执行沙箱、真实模型会话及大量隐藏下游评测；原论文规模已明显超过单卡A100/A30与Mac低成本预算。成本过高，不复现（审查 DONE）。不克隆和执行未知项目脚本、不伪造本地Agent成绩、不保留自动运行队列，也不宣称Evolve已接入。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24061v1">原论文</a> · <a href="../../../../agent-research/2610.24061-world-of-swecraft/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure Agent Meta 2026-10-15 生产事故的症状可能跨推荐、排序、数据、配置和算力服务传播。LLM 能调用工具并不代表它能可靠诊断：超时不等于无异常，历史相似事故不证明本次根因，事后总结也不能作为事故发生时的证据。原文 §4–5用 Encode／Execute／Evaluate／Adapt 四阶段闭环组织领域知识、Lead–worker 调查、事后审查和 owner 批准的知识更新。运行中只调整本次调查计划，不能自行发布新的共享工作流或执行缓解操作。 成本过高，不复现（审查 DONE），亦不伪造公开事故替代结论。这些是合同诊断，不是 RCA 成功率。component_only / L1 CPU 协议组件。实现证据接纳、假设状态与人工批准合同，不运行生产 RCA Agent，不进入 Evolve 晋级。每 seed 产生 24 个有来源的人工事件，随机化工具状态、可获得时间和数值。独立参考条件重算可接纳数；负对照把任何非空工具响应都当证据，从而保留错误接纳计数。另测未批准发布被拒和 owner 批准后版本前进。接口不接真实事故，也不生成根因答案。  工具使用与可靠性 生产事故诊断与证据治理 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-diviner-0cc63af7">Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>生产事故的症状可能跨推荐、排序、数据、配置和算力服务传播。LLM 能调用工具并不代表它能可靠诊断：超时不等于无异常，历史相似事故不证明本次根因，事后总结也不能作为事故发生时的证据。原文 §4–5用 Encode／Execute／Evaluate／Adapt 四阶段闭环组织领域知识、Lead–worker 调查、事后审查和 owner 批准的知识更新。运行中只调整本次调查计划，不能自行发布新的共享工作流或执行缓解操作。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE），亦不伪造公开事故替代结论。这些是合同诊断，不是 RCA 成功率。component_only / L1 CPU 协议组件。实现证据接纳、假设状态与人工批准合同，不运行生产 RCA Agent，不进入 Evolve 晋级。每 seed 产生 24 个有来源的人工事件，随机化工具状态、可获得时间和数值。独立参考条件重算可接纳数；负对照把任何非空工具响应都当证据，从而保留错误接纳计数。另测未批准发布被拒和 owner 批准后版本前进。接口不接真实事故，也不生成根因答案。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21281">原论文</a> · <a href="../../../../agent-research/2610.21281-diviner/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="A team of Gemini 4 Argon agents beats Minecraft Agent Google DeepMind 2026-10-15 四个执行 Agent 通过编写 JavaScript 程序操纵 Mineflayer 角色；Observer 汇总世界状态，聊天和笔记传递进度。研究重点是长期协作、程序化工具与持久状态，而不是新训练目标。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地执行 Agent、游戏成功率或 GPU 验证，不接入 Evolve。无本地 capability 指标、训练结果或 Evolve 算子；不创建虚构成功回执。范围见本批验收合同。只完成资料、原图和成本审查，不调用商业模型或运行游戏。原文长时交互超过本轮单卡/本地预算，完整实验标注成本过高，不复现（审查 DONE）。  多 Agent 协作 长期规划与工具使用 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-gemini-minecraft-c1e2611e">A team of Gemini 4 Argon agents beats Minecraft</h2>
<p class="ar-learning-card__meta">Google DeepMind · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>四个执行 Agent 通过编写 JavaScript 程序操纵 Mineflayer 角色；Observer 汇总世界状态，聊天和笔记传递进度。研究重点是长期协作、程序化工具与持久状态，而不是新训练目标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地执行 Agent、游戏成功率或 GPU 验证，不接入 Evolve。无本地 capability 指标、训练结果或 Evolve 算子；不创建虚构成功回执。范围见本批验收合同。只完成资料、原图和成本审查，不调用商业模型或运行游戏。原文长时交互超过本轮单卡/本地预算，完整实验标注成本过高，不复现（审查 DONE）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22319">原论文</a> · <a href="../../../../agent-research/2610.22319-gemini-minecraft/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs Agent University of Illinois Urbana-Champaign 2026-10-15 Agent 不需要每一步都让昂贵 LLM 生成长文本，但离线多选题高准确率也不保证闭环不出错。JevAgentHarness 在 agent 自己访问的 shadow trajectories 上，分别校准工具、参数等决策的委派阈值，低置信交回 LLM，并报告成功／费用／关键路径延迟。AgentDecision-4B 另用到达过的错误后状态训练，避免只模仿成功轨迹。原文 §2–4、附录 A/D 对单 A100/A30 或 Mac 的本轮预算，完整训练、真实工具任务和多臂评测成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现按决策类别拟合阈值、低置信回退及声明成本会计；没有 Jev／LLM 调用、AgentDecision-4B 训练或统一 Evolve 接入。每 seed 的低／高置信值随机化，40 行 shadow 数值 fixture 拟合不同阈值，在 12 个独立公共请求上实际调用概率 callback 或强模型 callback。负对照把阈值压低到 0.5，保留错误委派；NaN 输出触发回退；  工具使用与可靠性 System One/JEV置信委派与回退 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-jev-agent-harness-91c2ebf3">JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>Agent 不需要每一步都让昂贵 LLM 生成长文本，但离线多选题高准确率也不保证闭环不出错。JevAgentHarness 在 agent 自己访问的 shadow trajectories 上，分别校准工具、参数等决策的委派阈值，低置信交回 LLM，并报告成功／费用／关键路径延迟。AgentDecision-4B 另用到达过的错误后状态训练，避免只模仿成功轨迹。原文 §2–4、附录 A/D</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>对单 A100/A30 或 Mac 的本轮预算，完整训练、真实工具任务和多臂评测成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现按决策类别拟合阈值、低置信回退及声明成本会计；没有 Jev／LLM 调用、AgentDecision-4B 训练或统一 Evolve 接入。每 seed 的低／高置信值随机化，40 行 shadow 数值 fixture 拟合不同阈值，在 12 个独立公共请求上实际调用概率 callback 或强模型 callback。负对照把阈值压低到 0.5，保留错误委派；NaN 输出触发回退；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21412">原论文</a> · <a href="../../../../agent-research/2610.21412-jev-agent-harness/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents Agent Simular 2026-10-15 小模型先执行、必要时交给强模型可降低成本，但“何时接管”和“强模型接管后是否走偏”是两个问题。LEASH 利用弱模型表示与历史成功/失败参考的距离，不额外训练一个监控网络；初始和运行时 gate 决定 handoff，之后定期用弱模型的未执行 Shadow 动作表示监督强模型，并在需要时要求其重新审视策略。 完整多模型多配置实验成本高且需要 GUI/远程接口，成本过高，不复现（审查 DONE）。Shadow 高分回调在两次改变强动作后停止，未执行探针动作。component_only / L1 CPU 机制诊断。输入是明确生成的合成向量，不是模型 hidden states；统计校准和 Shadow callback 不等于完成 OSWorld 或真实 GUI Agent。每 seed 使用 30 个合成 reference task、90 action 向量及 12 个隔离 evaluation task；  专家模型编排 公共评测与协议 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-leash-edca97db">LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents</h2>
<p class="ar-learning-card__meta">Simular · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>小模型先执行、必要时交给强模型可降低成本，但“何时接管”和“强模型接管后是否走偏”是两个问题。LEASH 利用弱模型表示与历史成功/失败参考的距离，不额外训练一个监控网络；初始和运行时 gate 决定 handoff，之后定期用弱模型的未执行 Shadow 动作表示监督强模型，并在需要时要求其重新审视策略。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整多模型多配置实验成本高且需要 GUI/远程接口，成本过高，不复现（审查 DONE）。Shadow 高分回调在两次改变强动作后停止，未执行探针动作。component_only / L1 CPU 机制诊断。输入是明确生成的合成向量，不是模型 hidden states；统计校准和 Shadow callback 不等于完成 OSWorld 或真实 GUI Agent。每 seed 使用 30 个合成 reference task、90 action 向量及 12 个隔离 evaluation task；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22280">原论文</a> · <a href="../../../../agent-research/2610.22280-leash/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems Agent State University of Campinas 2026-10-15 多 Agent 注册表扩大后，把全部 Agent Card 塞给 LLM 会增加输入和选择成本。SSR §III 不训练额外模型，而是从明确的能力字段提取可解释词法信号，以倒排表预先缩小候选池。这里 structural 指来源于 name、description、skills、tags、examples、tools 的字段，不是句法图或隐向量。核心词法机制是已有IDF检索的特定集成，不应包装为新语义模型。 完整实验成本过高，不复现（审查 DONE）。本地CPU诊断记录保存可审计逐seed数据。无数据下载、LLM调用或GPU需求。固定 revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1；seeds42/43/44各生成64张合成能力card及12个查询，检索器只接收能力文本，接口没有gold answer或目标card参数。  工具使用与路由 Agent发现与词法检索 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-structural-signal-retriever-c1b3c953">SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems</h2>
<p class="ar-learning-card__meta">State University of Campinas · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>多 Agent 注册表扩大后，把全部 Agent Card 塞给 LLM 会增加输入和选择成本。SSR §III 不训练额外模型，而是从明确的能力字段提取可解释词法信号，以倒排表预先缩小候选池。这里 structural 指来源于 name、description、skills、tags、examples、tools 的字段，不是句法图或隐向量。核心词法机制是已有IDF检索的特定集成，不应包装为新语义模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。本地CPU诊断记录保存可审计逐seed数据。无数据下载、LLM调用或GPU需求。固定 revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1；seeds42/43/44各生成64张合成能力card及12个查询，检索器只接收能力文本，接口没有gold answer或目标card参数。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21113">原论文</a> · <a href="../../../../agent-research/2610.21113-structural-signal-retriever/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents Agent Microsoft 2026-10-15 把完整工具目录塞进 prompt 会占用大量上下文，纯工具描述相似度又忽略历史执行路径。TRACER 用 turn 内完整调用前缀索引执行 trie，候选是该前缀在训练中实际出现过的下一工具；边上记录频率和发生该转移时的完整 conversation context 均值。训练两个五维线性 head，逐状态决定经验频率/上下文先验的权重和温度；未知前缀或低置信时回到全目录向量检索。原图出处：原文 Figure 6：完整 TRACER 架构。 以单 A100/A30/Mac 的预算，成本过高，不复现（审查 DONE）；本地仅 component_only / CPU 算子诊断。本地仅 component_only / CPU 算子诊断。真正优化的是可学习混合与温度；使用合成三维表示而非原始语义 encoder，也没有 LLM 选择或执行工具。高 fixture recall 不是 Agent 能力，promotion_eligible: false。每 seed 使用 40 train trajectories / 20 held-out trajectories，每条三步，120 个训练步和 60 个测试步。  tool-retrieval Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-tracer-f2f8d03e">TRACER: Trajectory-Aware Tool Retrieval for LLM Agents</h2>
<p class="ar-learning-card__meta">Microsoft · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>把完整工具目录塞进 prompt 会占用大量上下文，纯工具描述相似度又忽略历史执行路径。TRACER 用 turn 内完整调用前缀索引执行 trie，候选是该前缀在训练中实际出现过的下一工具；边上记录频率和发生该转移时的完整 conversation context 均值。训练两个五维线性 head，逐状态决定经验频率/上下文先验的权重和温度；未知前缀或低置信时回到全目录向量检索。原图出处：原文 Figure 6：完整 TRACER 架构。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>以单 A100/A30/Mac 的预算，成本过高，不复现（审查 DONE）；本地仅 component_only / CPU 算子诊断。本地仅 component_only / CPU 算子诊断。真正优化的是可学习混合与温度；使用合成三维表示而非原始语义 encoder，也没有 LLM 选择或执行工具。高 fixture recall 不是 Agent 能力，promotion_eligible: false。每 seed 使用 40 train trajectories / 20 held-out trajectories，每条三步，120 个训练步和 60 个测试步。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21267">原论文</a> · <a href="../../../../agent-research/2610.21267-tracer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems Agent Florida State University 2026-10-14 多 Agent 的早期错误会沿消息和工具结果传播。ARIA 不只在结束后解释失败，而是把执行验证过的修复转成训练数据，让模型在部分轨迹上决定何时干预、在哪里切断及如何续写。原文 §2、附录 B的训练链包括结构 SFT、repair DPO、diagnosis transfer、repair GRPO 和 gate GRPO。本地没有以人工 heuristic 冒充这些学习阶段，只抽出可独立检验的补丁合同。 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现 cut-and-continuation 数据合同，不训练 inspection gate 或修复策略。随机事件序列实际执行合法 cut 与新 tool request 替换；负对照注入未知 cut、保留前缀 ID 冲突和伪造工具观察。另以随机成对执行 verdict 检查“只看 patched pass”会产生的错误样本接纳。verdict 是调用方 scorer 的人工 fixture，不是 Agent 推出的答案；模块不把 gold 传给模型。详见 CPU 产物。  多Agent协作 运行时诊断与续写修复 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-aria-04eaa6e6">ARIA: Runtime Inspection and Amendment for Multi-Agent Systems</h2>
<p class="ar-learning-card__meta">Florida State University · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>多 Agent 的早期错误会沿消息和工具结果传播。ARIA 不只在结束后解释失败，而是把执行验证过的修复转成训练数据，让模型在部分轨迹上决定何时干预、在哪里切断及如何续写。原文 §2、附录 B的训练链包括结构 SFT、repair DPO、diagnosis transfer、repair GRPO 和 gate GRPO。本地没有以人工 heuristic 冒充这些学习阶段，只抽出可独立检验的补丁合同。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现 cut-and-continuation 数据合同，不训练 inspection gate 或修复策略。随机事件序列实际执行合法 cut 与新 tool request 替换；负对照注入未知 cut、保留前缀 ID 冲突和伪造工具观察。另以随机成对执行 verdict 检查“只看 patched pass”会产生的错误样本接纳。verdict 是调用方 scorer 的人工 fixture，不是 Agent 推出的答案；模块不把 gold 传给模型。详见 CPU 产物。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20780">原论文</a> · <a href="../../../../agent-research/2610.20780-aria/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows Agent Nanjing University 2026-10-09 这是一篇评测研究，不是新的 self-improvement 算法。比较决策延迟/费用与端到端成功交付；failed recovery、premature completion 和失败开销计入资源每成功，而非只报告单步省时。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为同task/run的原配置与替换decision配置；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evaluation delivered-outcome latency-cost-recovery Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-jev-workflow-32efeb08">When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows</h2>
<p class="ar-learning-card__meta">Nanjing University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>这是一篇评测研究，不是新的 self-improvement 算法。比较决策延迟/费用与端到端成功交付；failed recovery、premature completion 和失败开销计入资源每成功，而非只报告单步省时。事实来源：原文全文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为同task/run的原配置与替换decision配置；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13092">原论文</a> · <a href="../../../../reproductions/2610.13092-jev-workflow/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics Agent Texas Tech University 2026-10-09 独立 query/tool encoder 做 CLS 归一化与 contrastive InfoNCE 训练。部署时 encoder 冻结，先语义 top-K，再融合 metadata prior 与逐工具 discounted LinUCB；只从实际选中工具的执行成功、错误或超时更新对应 arm。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为冻结语义dual encoder；线上反馈重排实验组；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  tool-retrieval execution-reliability contextual-bandit Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-rated-710146a7">RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics</h2>
<p class="ar-learning-card__meta">Texas Tech University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>独立 query/tool encoder 做 CLS 归一化与 contrastive InfoNCE 训练。部署时 encoder 冻结，先语义 top-K，再融合 metadata prior 与逐工具 discounted LinUCB；只从实际选中工具的执行成功、错误或超时更新对应 arm。事实来源：原文全文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为冻结语义dual encoder；线上反馈重排实验组；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13889">原论文</a> · <a href="../../../../reproductions/2610.13889-rated/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks Agent University of Science and Technology Beijing 2026-10-01 通过 domain 路由和扁平 schema 降低小模型工具调用负担；当模型宣称完成时重新注入原任务与计划并检查产物，发现重复调用或无输出循环时提醒修正，同时为常见 JSON 格式错误提供有限救援。改进的是推理运行框架，不需要把它解释为新的基础模型结构。 L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；使用显式脚本策略，不冒充真实小模型任务成功率。未实现整个 Windows GUI/语音产品、未跑 LRAB/τ²、未接入真实本地 LLM。注册工具仍继承调用方权限，此模块不是隔离沙箱，不应直接注册任意 shell。外部验收不能读取策略未获授权的私密信息并反馈给策略。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 在临时目录中真实写入文件：第一次 finish 因文件不存在被拒绝，随后执行写入，最后重新检查通过。  本地 Agent 运行框架 工具使用 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-mingbird-bbd1f960">Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks</h2>
<p class="ar-learning-card__meta">University of Science and Technology Beijing · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>通过 domain 路由和扁平 schema 降低小模型工具调用负担；当模型宣称完成时重新注入原任务与计划并检查产物，发现重复调用或无输出循环时提醒修正，同时为常见 JSON 格式错误提供有限救援。改进的是推理运行框架，不需要把它解释为新的基础模型结构。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；使用显式脚本策略，不冒充真实小模型任务成功率。未实现整个 Windows GUI/语音产品、未跑 LRAB/τ²、未接入真实本地 LLM。注册工具仍继承调用方权限，此模块不是隔离沙箱，不应直接注册任意 shell。外部验收不能读取策略未获授权的私密信息并反馈给策略。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 在临时目录中真实写入文件：第一次 finish 因文件不存在被拒绝，随后执行写入，最后重新检查通过。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02001">原论文</a> · <a href="../../../../agent-research/2610.02001-mingbird/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents Agent IIIS, Tsinghua University 2026-09-16 用中层隐藏状态估计 Agent 对样本的熟悉度，以累计阈值自适应选专家，并把训练样本定向分配给相应专家。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。  多 Agent 路由与协同进化 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-cera-moa-0d23f31e">CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents</h2>
<p class="ar-learning-card__meta">IIIS, Tsinghua University · 论文公开：2026-09-16</p>
<p><strong>方法要点：</strong>用中层隐藏状态估计 Agent 对样本的熟悉度，以累计阈值自适应选专家，并把训练样本定向分配给相应专家。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18779">原论文</a> · <a href="../../../../agent-research/2609.18779-cera-moa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views Agent Beihang University 2026-09-15 在固定预算下执行 select–project–refresh，把任务相关代码子图同步投影为视觉拓扑与精确文本索引。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  编程 Agent 多模态仓库视图 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-repoatlas-e75f59d2">RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>在固定预算下执行 select–project–refresh，把任务相关代码子图同步投影为视觉拓扑与精确文本索引。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16936">原论文</a> · <a href="../../../../agent-research/2609.16936-repoatlas/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration Agent Google Cloud 2026-09-11 HCRG 用 AST 提取 INHERITS/CALLS/IMPORTS，缓存全局架构骨架，按父依赖先后迁移，三跳取回结构上下文。原文对照是 800 字符/150 overlap/top-5 向量 RAG。§3–4 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0，仅 Python AST 支持的 graph 子系统。不是 Java tree-sitter 管线或真实 LLM 跨语言迁移复现。完整实验：成本过高，不复现（审查 DONE）。8 项 Python 自建源码机制测试通过：跨模块继承、三跳边界、签名骨架、父依赖顺序、显式循环组、缓存与部分静态指标，以及未导入跨模块同名、参数/局部变量shadow、歧义和外部依赖保留。诊断记录  代码 Agent 图检索 代码迁移 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-hcrg-d21831b9">Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration</h2>
<p class="ar-learning-card__meta">Google Cloud · 论文公开：2026-09-11</p>
<p><strong>方法要点：</strong>HCRG 用 AST 提取 INHERITS/CALLS/IMPORTS，缓存全局架构骨架，按父依赖先后迁移，三跳取回结构上下文。原文对照是 800 字符/150 overlap/top-5 向量 RAG。§3–4</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0，仅 Python AST 支持的 graph 子系统。不是 Java tree-sitter 管线或真实 LLM 跨语言迁移复现。完整实验：成本过高，不复现（审查 DONE）。8 项 Python 自建源码机制测试通过：跨模块继承、三跳边界、签名骨架、父依赖顺序、显式循环组、缓存与部分静态指标，以及未导入跨模块同名、参数/局部变量shadow、歧义和外部依赖保留。诊断记录</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12464">原论文</a> · <a href="../../../../agent-research/2609.12464-hcrg/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks Agent Fudan University 2026-09-08 论文指出统一反馈不适合整个探索过程：早期能力不足时使用 action guidance 降低搜索难度，后期则改为 observation enrichment，让 Agent 自己选择动作，避免长期依赖示范。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现早期公开动作引导、后期观察增强的阶段切换；不读取 gold plan。三种子结果见 metrics/mini-suite-seeds42-44.json。第一步只可采用公开 observation 中明确给出的 workflow；后续仅加入状态摘要，隐藏 AgentTask.plan 从不进入策略。当前未训练 LLM，也没有真实环境 rollout。  环境反馈脚手架 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-feedback-scaffold-b914bba8">Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks</h2>
<p class="ar-learning-card__meta">Fudan University · 论文公开：2026-09-08</p>
<p><strong>方法要点：</strong>论文指出统一反馈不适合整个探索过程：早期能力不足时使用 action guidance 降低搜索难度，后期则改为 observation enrichment，让 Agent 自己选择动作，避免长期依赖示范。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现早期公开动作引导、后期观察增强的阶段切换；不读取 gold plan。三种子结果见 metrics/mini-suite-seeds42-44.json。第一步只可采用公开 observation 中明确给出的 workflow；后续仅加入状态摘要，隐藏 AgentTask.plan 从不进入策略。当前未训练 LLM，也没有真实环境 rollout。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08404">原论文</a> · <a href="../../../../agent-research/2609.08404-feedback-scaffold/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-Prime: Fewer Trajectories, Better Performance Agent Sun Yat-sen University 2026-08-27 成功轨迹仍可能冗余、危险或不可学习。SWE-Prime 先按过程、结果和代表性选轨迹，再按贡献、可学习性和风险选语义段；上下文完整保留，但只对选中段计算 SFT loss。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现轨迹筛选、语义段筛选和 loss mask。未训练代码 LLM，也未运行官方 SWE-Bench；本地只比较相同 observation/tool 接口下的筛选策略。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5497。  软件轨迹筛选 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-swe-prime-e014601a">SWE-Prime: Fewer Trajectories, Better Performance</h2>
<p class="ar-learning-card__meta">Sun Yat-sen University · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>成功轨迹仍可能冗余、危险或不可学习。SWE-Prime 先按过程、结果和代表性选轨迹，再按贡献、可学习性和风险选语义段；上下文完整保留，但只对选中段计算 SFT loss。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现轨迹筛选、语义段筛选和 loss mask。未训练代码 LLM，也未运行官方 SWE-Bench；本地只比较相同 observation/tool 接口下的筛选策略。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5497。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27449">原论文</a> · <a href="../../../../agent-research/2608.27449-swe-prime/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research Agent Accio Team, Alibaba Group 2026-08-26 先以目标模型能力过滤不必要工具调用，只在中间证据不可靠时回退反思；SFT 后用 redundancy-aware reward 做 RL，兼顾视频理解、外部检索和调用成本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。AdaVDR 在无 oracle 的状态化工具环境中执行候选验证、失败反思与回退。ToolRoute-L2.1 三 seed 的 joint success 为 0.8167，plan step F1 为 0.8366，平均成本 5.0577；  视频研究自适应工具与反思 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-adavdr-576e1cf8">AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research</h2>
<p class="ar-learning-card__meta">Accio Team, Alibaba Group · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>先以目标模型能力过滤不必要工具调用，只在中间证据不可靠时回退反思；SFT 后用 redundancy-aware reward 做 RL，兼顾视频理解、外部检索和调用成本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。AdaVDR 在无 oracle 的状态化工具环境中执行候选验证、失败反思与回退。ToolRoute-L2.1 三 seed 的 joint success 为 0.8167，plan step F1 为 0.8366，平均成本 5.0577；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25559">原论文</a> · <a href="../../../../agent-research/2608.25559-adavdr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs Agent Aston University 2026-08-26 用多视角 scorer 衡量子任务完成度、进展趋势和状态质量，再由双路径 predictor 估计候选模型的边际进展，以 meta-gate 在质量、时间和长期成本预算间逐步决策。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。ProgRouter 把验证后的工具选择压缩为可复用程序路由，validation/test 冻结路由后再执行。ToolRoute-L2.1 三 seed的 joint success 为 0.7778，plan step F1 为 0.8037，平均成本 4.6324。  在线进展成本路由 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-progrouter-c8bea01c">ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs</h2>
<p class="ar-learning-card__meta">Aston University · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>用多视角 scorer 衡量子任务完成度、进展趋势和状态质量，再由双路径 predictor 估计候选模型的边际进展，以 meta-gate 在质量、时间和长期成本预算间逐步决策。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。ProgRouter 把验证后的工具选择压缩为可复用程序路由，validation/test 冻结路由后再执行。ToolRoute-L2.1 三 seed的 joint success 为 0.7778，plan step F1 为 0.8037，平均成本 4.6324。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25992">原论文</a> · <a href="../../../../agent-research/2608.25992-progrouter/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving Agent University of Science and Technology of China 2026-08-26 在共享 KV-cache 预算下，同时估算工作流最长剩余路径与下游 prefix reuse 收益，并纳入 prefix 移动、抢占和 aging，避免只优化局部命中率或单请求进度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TOPAS 在状态化工具环境里先做安全排序与候选压缩，再根据调用反馈恢复。ToolRoute-L2.1 三 seed 的 joint success 为 0.7556，plan step F1 为 0.7887，平均成本 4.5571。  工作流 Prefix-State 调度 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-topas-ae42000c">TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>在共享 KV-cache 预算下，同时估算工作流最长剩余路径与下游 prefix reuse 收益，并纳入 prefix 移动、抢占和 aging，避免只优化局部命中率或单请求进度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TOPAS 在状态化工具环境里先做安全排序与候选压缩，再根据调用反馈恢复。ToolRoute-L2.1 三 seed 的 joint success 为 0.7556，plan step F1 为 0.7887，平均成本 4.5571。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25523">原论文</a> · <a href="../../../../agent-research/2608.25523-topas/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development Agent Carnegie Mellon University 2026-08-26 统一记录每个代码版本、得分、动作意图、编辑规模和效果，比较 4465 条人类轨迹与 Agent 轨迹；把人类会交替阶段、回开旧方案的规律蒸馏成 planning prior。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TraceML 策略从训练 split 的失败轨迹写入反思先验，validation/test 只读取先验并通过真实工具反馈推进，不读取隐藏 route 或答案。  ML 开发轨迹规划 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-traceml-cea4f922">TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development</h2>
<p class="ar-learning-card__meta">Carnegie Mellon University · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>统一记录每个代码版本、得分、动作意图、编辑规模和效果，比较 4465 条人类轨迹与 Agent 轨迹；把人类会交替阶段、回开旧方案的规律蒸馏成 planning prior。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TraceML 策略从训练 split 的失败轨迹写入反思先验，validation/test 只读取先验并通过真实工具反馈推进，不读取隐藏 route 或答案。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26086">原论文</a> · <a href="../../../../agent-research/2608.26086-traceml/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification Agent Appier AI Research / National Taiwan University 2026-08-25 现有工具创建通常在推理时让冻结模型写代码，创建者与使用者没有联合信号。SMITH 在同一 policy 中混合 build task（从样例写 schema/backend）和 use task（在 held-out 问题调用池中工具），分别给 schema 合法性、代码执行和最终答案奖励，并用更难问题鼓励可复用抽象。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。同一 Agent 交替 build/use，并独立执行 schema、代码和 outcome 三类 verifier。本地工具为结构化 plan，并真实分开 build/use 状态和三轴 verifier；未运行 Qwen3-4B、可执行 Python sandbox、Reasoning-Gym、TabMWP 或 GQA。PlanBench-mini 120 episodes：生成 12 个工具、复用 108 次，执行 360 个分轴 verifier，joint success 1.0000、平均成本 0.4550。  多维验证工具自进化 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-smith-3e4d7833">SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification</h2>
<p class="ar-learning-card__meta">Appier AI Research / National Taiwan University · 论文公开：2026-08-25</p>
<p><strong>方法要点：</strong>现有工具创建通常在推理时让冻结模型写代码，创建者与使用者没有联合信号。SMITH 在同一 policy 中混合 build task（从样例写 schema/backend）和 use task（在 held-out 问题调用池中工具），分别给 schema 合法性、代码执行和最终答案奖励，并用更难问题鼓励可复用抽象。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。同一 Agent 交替 build/use，并独立执行 schema、代码和 outcome 三类 verifier。本地工具为结构化 plan，并真实分开 build/use 状态和三轴 verifier；未运行 Qwen3-4B、可执行 Python sandbox、Reasoning-Gym、TabMWP 或 GQA。PlanBench-mini 120 episodes：生成 12 个工具、复用 108 次，执行 360 个分轴 verifier，joint success 1.0000、平均成本 0.4550。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24571">原论文</a> · <a href="../../../../agent-research/2608.24571-smith/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution Agent Vanderbilt University 2026-08-07 用层级 phase planner 条件化 episodic retrieval，再用记忆轨迹统计检测 stuck 并重规划，以真实执行 verdict 验证。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  代码 Agent 记忆与规划 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-pmcoder-088b3672">Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution</h2>
<p class="ar-learning-card__meta">Vanderbilt University · 论文公开：2026-08-07</p>
<p><strong>方法要点：</strong>用层级 phase planner 条件化 episodic retrieval，再用记忆轨迹统计检测 stuck 并重规划，以真实执行 verdict 验证。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06811">原论文</a> · <a href="../../../../agent-research/2608.06811-pmcoder/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents Agent NetEase Guangzhou AI Lab 2026-08-06 主题：代码检索 Agent。以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的代码检索 Agent 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  代码检索 Agent Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-codegrep-29277303">CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents</h2>
<p class="ar-learning-card__meta">NetEase Guangzhou AI Lab · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>主题：代码检索 Agent。以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的代码检索 Agent 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05886">原论文</a> · <a href="../../../../agent-research/2608.05886-codegrep/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems Agent Cornell University 2026-07-30 根据任务先验初始化通信拓扑，运行中监控协作 trace，并有界调整角色、边、顺序、可见性和验证路径。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  多 Agent 自进化 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-manta-a024f561">MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems</h2>
<p class="ar-learning-card__meta">Cornell University · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>根据任务先验初始化通信拓扑，运行中监控协作 trace，并有界调整角色、边、顺序、可见性和验证路径。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28527">原论文</a> · <a href="../../../../agent-research/2607.28527-manta/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAM-DF Agent Peking University 2026-07-29 工具 router 只能给出相关性排序，不能回答“应该开放前几个工具”。CAM-DF 在任何工具执行前虚拟遍历排序前缀，以任务充分性减异构工具成本作为 payoff；停止当前前缀与最佳后续前缀的 payoff gap 决定标签，gap 绝对值决定错误的 regret 权重。 本地是确定性工具 mini-suite，不是 τ-bench Retail live execution；充分性来自 benchmark 可审计 required-tools，而不是另训的 scorer。ScaleMCP mini 为每个任务构造冻结排序和异构成本，枚举所有前缀的下游 payoff，执行 regret-weighted 停止并只挂载所选工具。  成本感知工具停止 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-cam-df-2b7f3d23">CAM-DF</h2>
<p class="ar-learning-card__meta">Peking University · 论文公开：2026-07-29</p>
<p><strong>方法要点：</strong>工具 router 只能给出相关性排序，不能回答“应该开放前几个工具”。CAM-DF 在任何工具执行前虚拟遍历排序前缀，以任务充分性减异构工具成本作为 payoff；停止当前前缀与最佳后续前缀的 payoff gap 决定标签，gap 绝对值决定错误的 regret 权重。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地是确定性工具 mini-suite，不是 τ-bench Retail live execution；充分性来自 benchmark 可审计 required-tools，而不是另训的 scorer。ScaleMCP mini 为每个任务构造冻结排序和异构成本，枚举所有前缀的下游 payoff，执行 regret-weighted 停止并只挂载所选工具。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27083">原论文</a> · <a href="../../../../agent-research/2607.27083-cam-df/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Formalizing Mathematics at Scale Agent FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris 2026-05-28 先构建教材声明的依赖DAG，工作者在独立worktree写Lean，经并发审查和合并队列进入主库；失败轨迹生成技能，监督者在合并后核查目标并反馈重规划。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；开源框架不等于本地已运行。每书约一周；39目标的小书消融仍使用600M至1200M tokens，持续数小时。成本过高，不复现（审查 DONE），不调用付费模型、不启动Lean多Agent任务。保留源码和协议，无本地分数、GPU回执或evolve可执行映射，不重新排入自动队列。  多Agent协作 形式化验证与依赖调度 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-autoformbot-6fe44000">Formalizing Mathematics at Scale</h2>
<p class="ar-learning-card__meta">FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris · 论文公开：2026-05-28</p>
<p><strong>方法要点：</strong>先构建教材声明的依赖DAG，工作者在独立worktree写Lean，经并发审查和合并队列进入主库；失败轨迹生成技能，监督者在合并后核查目标并反馈重规划。原文§3–4</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；开源框架不等于本地已运行。每书约一周；39目标的小书消融仍使用600M至1200M tokens，持续数小时。成本过高，不复现（审查 DONE），不调用付费模型、不启动Lean多Agent任务。保留源码和协议，无本地分数、GPU回执或evolve可执行映射，不重新排入自动队列。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29955">原论文</a> · <a href="../../../../agent-research/2605.29955-autoformbot/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving Agent University of Maryland / Google 2026-05-18 Coordinator、Analyzer 和 Proposal Agent 联合读取 profiler 与知识库，诊断瓶颈并输出可解释的 sharding 候选。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  训练服务优化 多 Agent 性能诊断 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-prompts-61564db7">PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving</h2>
<p class="ar-learning-card__meta">University of Maryland / Google · 论文公开：2026-05-18</p>
<p><strong>方法要点：</strong>Coordinator、Analyzer 和 Proposal Agent 联合读取 profiler 与知识库，诊断瓶颈并输出可解释的 sharding 候选。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/prompts-performance-optimization-via-multi-agent-planning-for-llm-training-and-serving/">原论文</a> · <a href="../../../../agent-research/mlsys2026-prompts/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing Agent Google Cloud AI Research 2026-04-06 PaperOrchestra 用 Outline、Plotting、Literature Review、Section Writing、Content Refinement 五个 Agent，把零散想法和实验日志转成含文献与图表的 LaTeX 稿件。大纲之后图示与文献检索并行，引用经过实体和时间截止核验，最终根据多维评价接受或回退修订；系统不负责替作者发明或执行新实验。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。无可执行 adapter、生成能力指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。原文附录 B 在 10 篇计时子集报告每文约 60–70 次 LLM 调用、39.6 分钟裁尾均值；完整 200 篇、多基线、多 judge 和人工评测成本远不止单次运行。写作需 Gemini3.1Pro，检索为 Gemini3Flash＋联网搜索，另有图像生成和多轮审稿。以上为作者报告和配置判断，不是本地测量，也不假设外部 API 免费或无限。  多Agent协作 研究与论文写作 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-paperorchestra-986964dd">PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing</h2>
<p class="ar-learning-card__meta">Google Cloud AI Research · 论文公开：2026-04-06</p>
<p><strong>方法要点：</strong>PaperOrchestra 用 Outline、Plotting、Literature Review、Section Writing、Content Refinement 五个 Agent，把零散想法和实验日志转成含文献与图表的 LaTeX 稿件。大纲之后图示与文献检索并行，引用经过实体和时间截止核验，最终根据多维评价接受或回退修订；系统不负责替作者发明或执行新实验。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。无可执行 adapter、生成能力指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。原文附录 B 在 10 篇计时子集报告每文约 60–70 次 LLM 调用、39.6 分钟裁尾均值；完整 200 篇、多基线、多 judge 和人工评测成本远不止单次运行。写作需 Gemini3.1Pro，检索为 Gemini3Flash＋联网搜索，另有图像生成和多轮审稿。以上为作者报告和配置判断，不是本地测量，也不假设外部 API 免费或无限。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05018v1">原论文</a> · <a href="../../../../agent-research/2604.05018-paperorchestra/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AIRA2: Overcoming Bottlenecks in AI Research Agents Agent FAIR at Meta / University College London 2026-03-27 以无同步屏障的 steady-state worker pool 提高实验吞吐；训练、搜索、最终选择使用固定的 80/10/10 隐藏切分，搜索只看 search score，结束后才用未参与爬山的 validation 选冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。三种子诊断：metrics/mechanism-seeds42-44.json  AI 研究 Agent 异步进化 隐藏一致评测 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-aira2-3f4a88e8">AIRA2: Overcoming Bottlenecks in AI Research Agents</h2>
<p class="ar-learning-card__meta">FAIR at Meta / University College London · 论文公开：2026-03-27</p>
<p><strong>方法要点：</strong>以无同步屏障的 steady-state worker pool 提高实验吞吐；训练、搜索、最终选择使用固定的 80/10/10 隐藏切分，搜索只看 search score，结束后才用未参与爬山的 validation 选冠军。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。三种子诊断：metrics/mechanism-seeds42-44.json</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26499">原论文</a> · <a href="../../../../agent-research/2603.26499-aira2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair Agent Google 2026-01-27 论文让修复和 BRT 留在同一条轨迹；TDD、TLD、Freeform 改变生成顺序。BRT 必须在原 bug 上失败、生成修复上通过。选择器按非测试修复归组，避免不同测试拆散同一修复的票数；ranked 在多数修复组内优先保留测试。原文 §3 完整实验：成本过高，不复现（审查 DONE）。component_only / L1 机制诊断。component_only / L1 机制诊断。实现测试验证及选择器，没有实现或宣称 Passerine 生成 Agent 的能力。完整实验：成本过高，不复现（审查 DONE）。11 项单元测试已通过。自建 increment 算术实例真实启动独立 Python 子进程，观察 assertion_failed → passed；恒真测试、异常而非断言失败、未通过回归的修复均不接纳。ranked 与 dual 的不同选项已通过多数分组实例验证。诊断指标  代码 Agent 程序修复 测试与验证 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-dynamic-brt-f3fe2d3c">Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-01-27</p>
<p><strong>方法要点：</strong>论文让修复和 BRT 留在同一条轨迹；TDD、TLD、Freeform 改变生成顺序。BRT 必须在原 bug 上失败、生成修复上通过。选择器按非测试修复归组，避免不同测试拆散同一修复的票数；ranked 在多数修复组内优先保留测试。原文 §3</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE）。component_only / L1 机制诊断。component_only / L1 机制诊断。实现测试验证及选择器，没有实现或宣称 Passerine 生成 Agent 的能力。完整实验：成本过高，不复现（审查 DONE）。11 项单元测试已通过。自建 increment 算术实例真实启动独立 Python 子进程，观察 assertion_failed → passed；恒真测试、异常而非断言失败、未通过回归的修复均不接纳。ranked 与 dual 的不同选项已通过多数分组实例验证。诊断指标</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.19066">原论文</a> · <a href="../../../../agent-research/2601.19066-dynamic-brt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Watch and Learn: Learning to Use Computers from Online Videos Agent The Ohio State University 2025-10-06 W&amp;L 把“视频里发生了什么操作”建模为逆动力学：输入前后两张屏幕图像，预测导致状态变化的动作。训练好的 IDM 再标注网络教程视频，结合任务检索形成轨迹，分别用于 CUA 的上下文示范和监督训练，而非直接让通用大模型猜动作或用规则恢复轨迹。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。本页没有可执行 adapter、组件指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。固定 v1 §3.1/附录 D.3 使用超过 630k 状态转移，IDM 训练为 8×A100 80GB、15 epochs；另有 53,125 个视频轨迹、7B CUA SFT、联网检索/API 和真实 OSWorld 桌面评测。该配置明显超过单张 A100/A30 或本地 Mac 的短时预算；这是作者配置形成的成本判断，不是本地计时。  工具与环境交互 计算机使用与视频示范 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-watch-and-learn-e9cf239b">Watch and Learn: Learning to Use Computers from Online Videos</h2>
<p class="ar-learning-card__meta">The Ohio State University · 论文公开：2025-10-06</p>
<p><strong>方法要点：</strong>W&amp;L 把“视频里发生了什么操作”建模为逆动力学：输入前后两张屏幕图像，预测导致状态变化的动作。训练好的 IDM 再标注网络教程视频，结合任务检索形成轨迹，分别用于 CUA 的上下文示范和监督训练，而非直接让通用大模型猜动作或用规则恢复轨迹。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。本页没有可执行 adapter、组件指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。固定 v1 §3.1/附录 D.3 使用超过 630k 状态转移，IDM 训练为 8×A100 80GB、15 epochs；另有 53,125 个视频轨迹、7B CUA SFT、联网检索/API 和真实 OSWorld 桌面评测。该配置明显超过单张 A100/A30 或本地 Mac 的短时预算；这是作者配置形成的成本判断，不是本地计时。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04673v1">原论文</a> · <a href="../../../../agent-research/2510.04673-watch-and-learn/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients Agent Google 2025-08-06 先从目标答案反推工具轨迹，再使用 textual gradient 定位并修订失败调用，降低人工轨迹标注成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  工具学习 数据生成 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-toolgrad-568745ef">ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2025-08-06</p>
<p><strong>方法要点：</strong>先从目标答案反推工具轨迹，再使用 textual gradient 定位并修订失败调用，降低人工轨迹标注成本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.04086">原论文</a> · <a href="../../../../agent-research/2508.04086-toolgrad/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolRL Agent University of Illinois Urbana-Champaign 2025-04-16 联合优化工具选择、参数生成和执行结果；动态 reward scaling 让不同工具难度进入同一 RL batch。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.1250；方法特有操作有非零 telemetry。  工具强化学习 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-toolrl-7e3d5cc8">ToolRL</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2025-04-16</p>
<p><strong>方法要点：</strong>联合优化工具选择、参数生成和执行结果；动态 reward scaling 让不同工具难度进入同一 RL batch。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.1250；方法特有操作有非零 telemetry。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.13958">原论文</a> · <a href="../../../../agent-research/2504.13958-toolrl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ReTool Agent ByteDance Seed 2025-04-15 策略在自然语言 reasoning 与工具执行之间交替，并由可执行反馈学习调用、纠错和停止。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.0500；方法特有操作有非零 telemetry。  推理中工具调用 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-retool-db452677">ReTool</h2>
<p class="ar-learning-card__meta">ByteDance Seed · 论文公开：2025-04-15</p>
<p><strong>方法要点：</strong>策略在自然语言 reasoning 与工具执行之间交替，并由可执行反馈学习调用、纠错和停止。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.0500；方法特有操作有非零 telemetry。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.11536">原论文</a> · <a href="../../../../agent-research/2504.11536-retool/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="OpenHands Agent All-Hands-AI 2024-07-23 OpenHands 提供开放的软件 Agent 平台，把终端、编辑器、浏览器等动作统一到 event stream，并以 sandbox 隔离执行，覆盖修 bug、写代码和仓库维护。 浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。用编辑器、终端和可观测事件流驱动通用软件开发 Agent。已实现编辑器/终端事件和真实代码 sandbox；浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。本地将 file-editor 与 terminal 动作写入 event stream；terminal 在独立临时目录执行固定回归测试，最终报告动作、编辑 hash、命令输出和 success。  通用软件 Agent Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-openhands-e21fcd2c">OpenHands</h2>
<p class="ar-learning-card__meta">All-Hands-AI · 论文公开：2024-07-23</p>
<p><strong>方法要点：</strong>OpenHands 提供开放的软件 Agent 平台，把终端、编辑器、浏览器等动作统一到 event stream，并以 sandbox 隔离执行，覆盖修 bug、写代码和仓库维护。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。用编辑器、终端和可观测事件流驱动通用软件开发 Agent。已实现编辑器/终端事件和真实代码 sandbox；浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。本地将 file-editor 与 terminal 动作写入 event stream；terminal 在独立临时目录执行固定回归测试，最终报告动作、编辑 hash、命令输出和 success。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16741">原论文</a> · <a href="../../../../agent-research/2407.16741-openhands/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-agent Agent Princeton University 2024-05-06 通用 shell 对 LLM 而言动作空间过宽、输出冗长。SWE-agent 用专门 ACI 约束仓库搜索、文件查看、精确编辑和测试，让模型能围绕 issue 定位故障并验证 patch。 为软件工程 Agent 设计面向仓库浏览、编辑和测试的 Agent-Computer Interface。这是可执行的 SWE-style micro benchmark，不是官方 SWE-bench Lite 数据与 Docker 镜像。名称 swebench-local 明确保留该区别，不能将本地 success 当作论文 resolved rate。本地 ACI 只暴露读文件、写 solution.py 和固定 unittest 命令；每题初始仓库必须先真实失败，Agent 定位、编辑并以退出码验证。  软件工程 ACI Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-swe-agent-79904a33">SWE-agent</h2>
<p class="ar-learning-card__meta">Princeton University · 论文公开：2024-05-06</p>
<p><strong>方法要点：</strong>通用 shell 对 LLM 而言动作空间过宽、输出冗长。SWE-agent 用专门 ACI 约束仓库搜索、文件查看、精确编辑和测试，让模型能围绕 issue 定位故障并验证 patch。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>为软件工程 Agent 设计面向仓库浏览、编辑和测试的 Agent-Computer Interface。这是可执行的 SWE-style micro benchmark，不是官方 SWE-bench Lite 数据与 Docker 镜像。名称 swebench-local 明确保留该区别，不能将本地 success 当作论文 resolved rate。本地 ACI 只暴露读文件、写 solution.py 和固定 unittest 命令；每题初始仓库必须先真实失败，Agent 定位、编辑并以退出码验证。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.15793">原论文</a> · <a href="../../../../agent-research/2405.15793-swe-agent/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AutoGen Agent Microsoft Research 2023-08-16 复杂应用常需要多个模型、工具和人类协作，手写控制流难复用。AutoGen 提供 ConversableAgent 与 conversation programming：每个角色声明能力、回复策略和终止条件，通过群聊或嵌套会话组合成工作流。 AutoGen 把 Agent 抽象为可对话、可配置的角色，用消息路由和终止条件编排 planner、executor、critic、人类或工具。实现 planner/executor/critic 的消息协议、角色交接与显式终止；未嵌入完整 AutoGen 运行时、容器代码执行或真实 LLM 群聊，1.0 是确定性控制流测试而非论文应用得分。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.0000，记录 120 份 plan、360 条跨角色消息和 120 次 critic round。  多 Agent Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-autogen-60994f2d">AutoGen</h2>
<p class="ar-learning-card__meta">Microsoft Research · 论文公开：2023-08-16</p>
<p><strong>方法要点：</strong>复杂应用常需要多个模型、工具和人类协作，手写控制流难复用。AutoGen 提供 ConversableAgent 与 conversation programming：每个角色声明能力、回复策略和终止条件，通过群聊或嵌套会话组合成工作流。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>AutoGen 把 Agent 抽象为可对话、可配置的角色，用消息路由和终止条件编排 planner、executor、critic、人类或工具。实现 planner/executor/critic 的消息协议、角色交接与显式终止；未嵌入完整 AutoGen 运行时、容器代码执行或真实 LLM 群聊，1.0 是确定性控制流测试而非论文应用得分。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.0000，记录 120 份 plan、360 条跨角色消息和 120 次 critic round。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.08155">原论文</a> · <a href="../../../../agent-research/2308.08155-autogen/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MetaGPT Agent DeepWisdom 2023-08-01 简单串联多个聊天 Agent 容易让幻觉级联。MetaGPT 把人类软件团队的 SOP 编码成角色化消息流程，每个角色生产结构化中间物，由下游角色消费和验证。 用标准作业流程（SOP）把软件需求依次交给产品、架构、工程和测试角色。保留 SOP、角色交付物、真实编辑与测试；本地不是完整 MetaGPT LLM 对话，也不是官方 SWE-bench Lite，fixture 仅验证执行链路和可审计 trace。每个 episode 创建真实临时 Python 仓库；四个角色留下结构化 artifact，工程角色修改文件，QA 角色通过固定 python -m unittest -q 执行回归测试。  多 Agent 软件工程 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-metagpt-ffaa73e8">MetaGPT</h2>
<p class="ar-learning-card__meta">DeepWisdom · 论文公开：2023-08-01</p>
<p><strong>方法要点：</strong>简单串联多个聊天 Agent 容易让幻觉级联。MetaGPT 把人类软件团队的 SOP 编码成角色化消息流程，每个角色生产结构化中间物，由下游角色消费和验证。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>用标准作业流程（SOP）把软件需求依次交给产品、架构、工程和测试角色。保留 SOP、角色交付物、真实编辑与测试；本地不是完整 MetaGPT LLM 对话，也不是官方 SWE-bench Lite，fixture 仅验证执行链路和可审计 trace。每个 episode 创建真实临时 Python 仓库；四个角色留下结构化 artifact，工程角色修改文件，QA 角色通过固定 python -m unittest -q 执行回归测试。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.00352">原论文</a> · <a href="../../../../agent-research/2308.00352-metagpt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolBench Agent Tsinghua University 2023-05-25 分析开源 LLM 工具失败后，组合程序化使用样例、system prompt、in-context demonstration retriever 与生成格式约束。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.8400。  工具指令与评测 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-toolbench-89c52f4b">ToolBench</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2023-05-25</p>
<p><strong>方法要点：</strong>分析开源 LLM 工具失败后，组合程序化使用样例、system prompt、in-context demonstration retriever 与生成格式约束。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.8400。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16504">原论文</a> · <a href="../../../../agent-research/2305.16504-toolbench/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CRITIC Agent Microsoft 2023-05-19 仅让 LLM 反思自己的文本可能重复同一错误。CRITIC 调用搜索、代码解释器等外部工具，把可观测反馈带回修订循环，使 critique 有环境证据。 让 Agent 用外部工具验证初稿，再依据真实反馈自我修正。外部反馈和迭代改码是真实执行的；反馈源仅为受控代码测试，没有搜索引擎、toxicity classifier 或通用 LLM critic。Agent 先写入一个有缺陷 patch，真实运行 unittest 获取 traceback，再根据反馈写入正确 patch 并复测；报告记录每轮编辑、命令、退出码和输出。  工具反馈 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-critic-11dab3d3">CRITIC</h2>
<p class="ar-learning-card__meta">Microsoft · 论文公开：2023-05-19</p>
<p><strong>方法要点：</strong>仅让 LLM 反思自己的文本可能重复同一错误。CRITIC 调用搜索、代码解释器等外部工具，把可观测反馈带回修订循环，使 critique 有环境证据。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>让 Agent 用外部工具验证初稿，再依据真实反馈自我修正。外部反馈和迭代改码是真实执行的；反馈源仅为受控代码测试，没有搜索引擎、toxicity classifier 或通用 LLM critic。Agent 先写入一个有缺陷 patch，真实运行 unittest 获取 traceback，再根据反馈写入正确 patch 并复测；报告记录每轮编辑、命令、退出码和输出。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.11738">原论文</a> · <a href="../../../../agent-research/2305.11738-critic/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAMEL Agent King Abdullah University of Science and Technology 2023-03-31 用 inception prompting 固定 user/assistant 的角色、目标和边界，通过轮流消息完成任务并生成可研究的多 Agent 社会轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.3500。  多 Agent 协作 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-camel-640cbec7">CAMEL</h2>
<p class="ar-learning-card__meta">King Abdullah University of Science and Technology · 论文公开：2023-03-31</p>
<p><strong>方法要点：</strong>用 inception prompting 固定 user/assistant 的角色、目标和边界，通过轮流消息完成任务并生成可研究的多 Agent 社会轨迹。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.3500。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17760">原论文</a> · <a href="../../../../agent-research/2303.17760-camel/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="HuggingGPT Agent Zhejiang University 2023-03-30 单个 LLM 难以覆盖视觉、语音和其他专业任务，而模型社区已有大量专家。HuggingGPT 让 ChatGPT 充当控制器：先把请求拆成带依赖的子任务，再按 Hugging Face 模型描述匹配专家，按拓扑顺序执行，最后把多模型输出组织为用户答案。 本页实现 task planning、按能力描述选择模型、依赖图执行和最终汇总四阶段。复现控制流、能力匹配和依赖执行；没有下载数百个 Hugging Face 模型，也未调用 ChatGPT。mini-suite 的 1.0 表示编排一致，不代表论文跨模态能力。PlanBench mini 120 episodes、seed 42；工具描述充当本地模型 capability registry，每个子任务保留 dependency edge 后执行。  专家模型编排 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-hugginggpt-c07a7bb7">HuggingGPT</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2023-03-30</p>
<p><strong>方法要点：</strong>单个 LLM 难以覆盖视觉、语音和其他专业任务，而模型社区已有大量专家。HuggingGPT 让 ChatGPT 充当控制器：先把请求拆成带依赖的子任务，再按 Hugging Face 模型描述匹配专家，按拓扑顺序执行，最后把多模型输出组织为用户答案。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现 task planning、按能力描述选择模型、依赖图执行和最终汇总四阶段。复现控制流、能力匹配和依赖执行；没有下载数百个 Hugging Face 模型，也未调用 ChatGPT。mini-suite 的 1.0 表示编排一致，不代表论文跨模态能力。PlanBench mini 120 episodes、seed 42；工具描述充当本地模型 capability registry，每个子任务保留 dependency edge 后执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17580">原论文</a> · <a href="../../../../agent-research/2303.17580-hugginggpt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ART Agent University of Washington 2023-03-16 既有 tool-use prompting 常需为每个任务手写示例和调用顺序。ART 根据新任务自动检索相近的推理/工具示例，让冻结 LLM 生成程序；运行器遇到工具标记就暂停生成，执行工具并注入结果后继续。人可以用少量修订扩展任务库。 本页复现任务库检索、程序式多步推理、工具调用处暂停/恢复和成功示例写回，不把 mini-suite 写成完整 BIG-Bench/MMLU。保留自动示例检索、程序生成控制流、工具暂停和库更新；本地任务库很小，不调用冻结大模型，也未复刻 BIG-Bench/MMLU 原始分数。PlanBench mini 120 episodes、seed 42；按工具签名组织任务库，并逐工具暂停/恢复。  自动工具推理 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-art-62b00229">ART</h2>
<p class="ar-learning-card__meta">University of Washington · 论文公开：2023-03-16</p>
<p><strong>方法要点：</strong>既有 tool-use prompting 常需为每个任务手写示例和调用顺序。ART 根据新任务自动检索相近的推理/工具示例，让冻结 LLM 生成程序；运行器遇到工具标记就暂停生成，执行工具并注入结果后继续。人可以用少量修订扩展任务库。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页复现任务库检索、程序式多步推理、工具调用处暂停/恢复和成功示例写回，不把 mini-suite 写成完整 BIG-Bench/MMLU。保留自动示例检索、程序生成控制流、工具暂停和库更新；本地任务库很小，不调用冻结大模型，也未复刻 BIG-Bench/MMLU 原始分数。PlanBench mini 120 episodes、seed 42；按工具签名组织任务库，并逐工具暂停/恢复。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.09014">原论文</a> · <a href="../../../../agent-research/2303.09014-art/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Toolformer Agent Meta AI Research 2023-02-09 手工标注工具调用昂贵，纯 prompting 又难以让较小模型稳定决定何时调用。Toolformer 先用少量 demonstration 采样 API call，再比较插入真实返回值、隐藏返回值和完全不调用时的后续 token loss，只保留确实有用的调用并继续语言模型训练。 本页实现候选 API call 生成、no-call/masked-call loss 对照和自监督过滤，只保留能降低预测 loss 的工具调用。实现自监督候选过滤的核心判据，但 loss 来自确定性 tool utility，不是 GPT-J token loss；未进行 6.7B continued training，也未复刻论文五类真实 API。ScaleMCP mini 对 required 和 distractor tools 都生成候选，只有相对 no-call 降低 loss 的调用被接受。  工具学习 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-toolformer-dc9c6efa">Toolformer</h2>
<p class="ar-learning-card__meta">Meta AI Research · 论文公开：2023-02-09</p>
<p><strong>方法要点：</strong>手工标注工具调用昂贵，纯 prompting 又难以让较小模型稳定决定何时调用。Toolformer 先用少量 demonstration 采样 API call，再比较插入真实返回值、隐藏返回值和完全不调用时的后续 token loss，只保留确实有用的调用并继续语言模型训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现候选 API call 生成、no-call/masked-call loss 对照和自监督过滤，只保留能降低预测 loss 的工具调用。实现自监督候选过滤的核心判据，但 loss 来自确定性 tool utility，不是 GPT-J token loss；未进行 6.7B continued training，也未复刻论文五类真实 API。ScaleMCP mini 对 required 和 distractor tools 都生成候选，只有相对 no-call 降低 loss 的调用被接受。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2302.04761">原论文</a> · <a href="../../../../agent-research/2302.04761-toolformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PAL Agent Carnegie Mellon University 2022-11-18 LLM 擅长把问题分解成步骤，却会在算术和符号执行阶段出错。PAL 让 LLM 输出带变量和控制流的程序，最终计算完全交给 Python 等确定性 runtime；模型只承担自然语言理解和程序合成。 本页复现“语言模型生成程序、符号 runtime 执行、返回解释器答案”的系统边界，不把结构化 task program 写成 Codex 生成代码。保留神经程序生成与符号执行的职责分离；本地使用受控中间表示而非任意 Python，不调用 Codex，也未复刻原论文 GSM8K。ScaleMCP mini 120 episodes、seed 42；每题实际构建 CALL/RETURN 程序并由本地解释器执行。  程序推理 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-pal-f0f14e4c">PAL</h2>
<p class="ar-learning-card__meta">Carnegie Mellon University · 论文公开：2022-11-18</p>
<p><strong>方法要点：</strong>LLM 擅长把问题分解成步骤，却会在算术和符号执行阶段出错。PAL 让 LLM 输出带变量和控制流的程序，最终计算完全交给 Python 等确定性 runtime；模型只承担自然语言理解和程序合成。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页复现“语言模型生成程序、符号 runtime 执行、返回解释器答案”的系统边界，不把结构化 task program 写成 Codex 生成代码。保留神经程序生成与符号执行的职责分离；本地使用受控中间表示而非任意 Python，不调用 Codex，也未复刻原论文 GSM8K。ScaleMCP mini 120 episodes、seed 42；每题实际构建 CALL/RETURN 程序并由本地解释器执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.10435">原论文</a> · <a href="../../../../agent-research/2211.10435-pal/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MRKL Agent AI21 Labs 2022-05-01 单个 LLM 容易在精确计算、时效知识和可验证推理上失败。MRKL 把 LLM 放入系统架构，由 router 根据输入选择语言模型、知识库、计算器等专家；离散模块保证确定性能力，语言模型负责理解和自然语言接口。 本页实现显式 router、神经/离散专家注册表和结果汇总；不是让一个通用 prompt 直接返回正确工具链。保留 router 和可区分的专家执行计数；本地专家是确定性 mini-suite 工具，不调用 Jurassic-X、真实搜索服务或私有知识库，成本是统一代理成本而非线上延迟。ScaleMCP mini 120 episodes、seed 42；每个工具动作都先经 router，计算器、日历、地图、天气、数据库和表格进入离散专家。  神经符号路由 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-mrkl-816ab670">MRKL</h2>
<p class="ar-learning-card__meta">AI21 Labs · 论文公开：2022-05-01</p>
<p><strong>方法要点：</strong>单个 LLM 容易在精确计算、时效知识和可验证推理上失败。MRKL 把 LLM 放入系统架构，由 router 根据输入选择语言模型、知识库、计算器等专家；离散模块保证确定性能力，语言模型负责理解和自然语言接口。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现显式 router、神经/离散专家注册表和结果汇总；不是让一个通用 prompt 直接返回正确工具链。保留 router 和可区分的专家执行计数；本地专家是确定性 mini-suite 工具，不调用 Jurassic-X、真实搜索服务或私有知识库，成本是统一代理成本而非线上延迟。ScaleMCP mini 120 episodes、seed 42；每个工具动作都先经 router，计算器、日历、地图、天气、数据库和表格进入离散专家。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.00445">原论文</a> · <a href="../../../../agent-research/2205.00445-mrkl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SayCan Agent Robotics at Google 2022-04-04 LLM 知道“应该做什么”，却不知道当前机器人“能不能做”。SayCan 为每个预训练技能同时计算语言相关性和 value-function affordance，选择乘积最高的技能并执行，再把动作追加到上下文继续规划。 本页复现逐步技能枚举及“语言分数 × affordance”决策，不把确定性工具 mini-suite 冒充真实移动机械臂。保留双分数逐步规划与不可行技能过滤；affordance 是确定性本地可执行性，不含视觉、机器人控制策略或真实 value-function 训练。PlanBench mini 120 episodes、seed 42；每一步同时打分必要技能和干扰技能。  具身规划 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-saycan-7674e520">SayCan</h2>
<p class="ar-learning-card__meta">Robotics at Google · 论文公开：2022-04-04</p>
<p><strong>方法要点：</strong>LLM 知道“应该做什么”，却不知道当前机器人“能不能做”。SayCan 为每个预训练技能同时计算语言相关性和 value-function affordance，选择乘积最高的技能并执行，再把动作追加到上下文继续规划。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页复现逐步技能枚举及“语言分数 × affordance”决策，不把确定性工具 mini-suite 冒充真实移动机械臂。保留双分数逐步规划与不可行技能过滤；affordance 是确定性本地可执行性，不含视觉、机器人控制策略或真实 value-function 训练。PlanBench mini 120 episodes、seed 42；每一步同时打分必要技能和干扰技能。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2204.01691">原论文</a> · <a href="../../../../agent-research/2204.01691-saycan/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="WebGPT Agent OpenAI 2021-12-17 长文本问答容易幻觉，且很难核查依据。WebGPT 让模型在文本浏览器里搜索、点击和滚动，回答必须收集引用；训练先做行为克隆，再用人类偏好 reward model 从多条浏览/回答轨迹中做拒绝采样。 本页复现文本浏览轨迹、证据引用和 reward-model 拒绝采样；本地确定性工具环境不是实时互联网浏览。保留 browser-action、citation constraint 和 trajectory rejection sampling；不访问实时网页、不训练 GPT-3/reward model，也不复刻 ELI5 人评。ScaleMCP mini 120 episodes、seed 42；每题生成两条工具轨迹，按证据覆盖选择。  浏览问答 Agent 工具与协作执行：把计划变成可检查的动作">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<h2 id="paper-agent-research-webgpt-13267288">WebGPT</h2>
<p class="ar-learning-card__meta">OpenAI · 论文公开：2021-12-17</p>
<p><strong>方法要点：</strong>长文本问答容易幻觉，且很难核查依据。WebGPT 让模型在文本浏览器里搜索、点击和滚动，回答必须收集引用；训练先做行为克隆，再用人类偏好 reward model 从多条浏览/回答轨迹中做拒绝采样。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页复现文本浏览轨迹、证据引用和 reward-model 拒绝采样；本地确定性工具环境不是实时互联网浏览。保留 browser-action、citation constraint 和 trajectory rejection sampling；不访问实时网页、不训练 GPT-3/reward model，也不复刻 ELI5 人评。ScaleMCP mini 120 episodes、seed 42；每题生成两条工具轨迹，按证据覆盖选择。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2112.09332">原论文</a> · <a href="../../../../agent-research/2112.09332-webgpt/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
