---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 规划先问何时见反馈，再问要不要展开搜索

[Agent](../index.md) · 更新 2026-10-27 · 16 篇主题资料 / 6 篇重点对照

ReAct 与 ReWOO 改变计划接收观察的时机，ToT 与 LATS 改变候选搜索组织，Jev Lookahead 把后继模拟交给代码，DRAGO 则检查形式计划是否忠实。它们处理不同的不确定性：步骤未知、路线选择、环境可达性与规格错误，不应以搜索次数或本地满分统一排名。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/agent-research/planning-and-search.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：计划在中间工具观察到来前还是之后生成 · 搜索单元是thought、环境动作还是完整计划 · 价值信号来自模型判断、真实执行还是符号探针 · 可恢复的分支与模拟状态是否有可靠隔离

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [ReAct](../../../agent-research/2210.03629-react/README.md) · [原始来源](https://arxiv.org/abs/2210.03629)<br>章节：背景与主要改动、核心公式、复现边界 | 推理、动作和真实观察交替，每轮据最新结果决定下一步。 | 适应中间变化，但历史和重复推理成本增长；本地经典mini使用确定性观察，不能当论文真实环境结果。 |
| [ReWOO](../../../agent-research/2305.18323-rewoo/README.md) · [原始来源](https://arxiv.org/abs/2305.18323)<br>章节：背景与主要改动、核心公式、复现边界 | Planner 先生成含证据变量的多步依赖，Worker 填工具结果，Solver 最后合成。 | 减少 Planner 重读观察，但异常可能使原计划不再适用；依赖变量仍限制并行，本地只验证解耦控制流。 |
| [Tree of Thoughts](../../../agent-research/2305.10601-tree-of-thoughts/README.md) · [原始来源](https://arxiv.org/abs/2305.10601)<br>章节：背景与主要改动、核心公式、复现边界 | 将可评价中间状态组成 thought tree，以 BFS/DFS 维护前沿并可回溯。 | 能撤销早期方向，却依赖中间评价；本地 workflow coherence 替代 LM value，不说明开放推理能力。 |
| [LATS](../../../agent-research/2310.04406-lats/README.md) · [原始来源](https://arxiv.org/abs/2310.04406)<br>章节：背景与主要改动、核心公式、复现边界 | 用 MCTS 组织行动、rollout 与价值回传，UCT 平衡已有回报和访问不足，失败生成反思。 | 真实 rollout 增加外部约束也消耗预算；本地以完整计划为叶，未运行原文 LM value 或 WebShop。 |
| [Code Owns the Simulation, Jev Owns the Evaluation](../../../agent-research/2610.01834-jev-lookahead/README.md) · [原始来源](https://arxiv.org/abs/2610.01834)<br>章节：背景与主要改动、核心公式、本地复现 | 逐动作克隆模拟后继，把新观察和新可用动作交给决策器比较进展。 | 依赖可信且隔离的 simulator；独立对象不保证 RNG/外部资源隔离。本地词法 provider 只是替身。 |
| [Repairing LLM-Generated Specifications with Deterministic Diagnosis](../../../agent-research/2610.22568-drago/README.md) · [原始来源](https://arxiv.org/abs/2610.22568)<br>章节：背景与主要改动、核心公式、本地复现与边界 | 以类型、契约、可达性和题意诊断定向修复形式规格，严格降低阻塞并防止删目标退化。 | 求解器只验证给定形式化，仍可能形式上可解却题意错误；本地是正前提 STRIPS 子集，完整多模型实验高成本未复现。 |

</div>

## 取舍分析 {#analysis}

### 先规划完整依赖，还是等观察再决定

ReWOO 的变量引用说明它不是不看工具证据，而是不让 Planner 在每轮观察后重新生成整段思考；后续参数仍可由前序证据填入。ReAct 则让真实返回直接参与下一次选择，适合路径会随结果变化的任务。若工具步骤结构稳定，预规划可能减少重复输入；若异常会改变目标或可用操作，必须考虑重新决策路径。两者要按完整交付成本比较，不能只数 Planner 调用。

对照来源：[react](../../../agent-research/2210.03629-react/README.md) · [rewoo](../../../agent-research/2305.18323-rewoo/README.md)

### 搜索给机会，验证决定证据的含义

ToT 与 LATS 都扩展多个方向，但前者突出中间状态评价和前沿组织，后者还通过执行与访问统计回传反馈。Jev Lookahead 进一步要求代码模拟提供可观察后继，DRAGO 用符号探针检查规格。外部计算也不是万能 oracle：模拟器可能不隔离，求解器可能解了错误规格。比较搜索器时应先固定它能看到的证据及失败含义，再讨论树宽、深度和预算。

对照来源：[tree-of-thoughts](../../../agent-research/2305.10601-tree-of-thoughts/README.md) · [lats](../../../agent-research/2310.04406-lats/README.md) · [jev-lookahead](../../../agent-research/2610.01834-jev-lookahead/README.md) · [drago](../../../agent-research/2610.22568-drago/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 第一步查到用户身份后才能查订单，ReWOO 还能预规划吗？与 ReAct 的真正差别在哪里？ {#cross-dependency-versus-adaptation}

??? note "展开答案与例子"

    **答案：** 能，ReWOO 可先写出第二步引用第一步证据变量，Worker 等真实值返回后填入参数；预规划不等于预知工具结果。差别在于 Planner 不被每次观察反复打断，而 ReAct 会据返回重新决定行动。若身份查询异常使后续流程必须换路线，预先依赖图不一定足够，仍需处理失败和重规划。

    **教学例子：** 教学例：先查 customer_id 再查订单可预写；如果返回“用户合并，需要人工确认”，就不是简单替换变量值能继续的情况。

    对照来源：[rewoo](../../../agent-research/2305.18323-rewoo/README.md) · [react](../../../agent-research/2210.03629-react/README.md)

### ToT 当前评价低的一条 thought，LATS 为什么可能仍给它一次 rollout？ {#cross-frontier-versus-rollout}

??? note "展开答案与例子"

    **答案：** 按层前沿选择可根据当前 value 剪枝，MCTS 的 UCT 则同时考虑已有 Q 和访问次数，少访问分支仍可能值得探索。外部 rollout 可能提供新回报，但不是免费纠正所有价值误判。比较应控制预算及评价器，不能把本地确定性 coherence 的搜索结果直接当成 LM value 或真实环境能力对照。

    **教学例子：** 教学例：一条路线看起来绕远，却可能打开关键资源；UCT 可因尚未尝试保留机会，固定前沿也可能已把它剪掉。

    对照来源：[tree-of-thoughts](../../../agent-research/2305.10601-tree-of-thoughts/README.md) · [lats](../../../agent-research/2310.04406-lats/README.md)

### Jev 模拟显示动作能到达目标，DRAGO 求解器也说可解，为什么仍要核对用户原意？ {#cross-simulation-versus-specification}

??? note "展开答案与例子"

    **答案：** 两者验证的是已编码环境或规格中的后果。Jev Lookahead 需要模拟与真实状态一致且不泄露 reward/gold；DRAGO 需要形式规格忠实，不能通过删除目标获得可解。代码或求解器能排除某类错误，却无法自动保证自然语言需求已完整转成状态、约束和目标。

    **教学例子：** 教学例：用户要“送到A且保持低温”，规格只写“送到A”。模拟和求解都成功，仍没验证低温要求，因为它从未被编码。

    对照来源：[jev-lookahead](../../../agent-research/2610.01834-jev-lookahead/README.md) · [drago](../../../agent-research/2610.22568-drago/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较反馈时机、thought与MCTS搜索、代码后继模拟和形式规格诊断，区分规划效率与验证证据。

覆盖 16 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 16 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Repairing LLM-Generated Specifications with Deterministic Diagnosis](../../../agent-research/2610.22568-drago/README.md)
- [Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models](../../../reproductions/2610.13194-janus/README.md)
- [Code Owns the Simulation, Jev Owns the Evaluation](../../../agent-research/2610.01834-jev-lookahead/README.md)
- [JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces](../../../agent-research/2610.00437-jev-spawn/README.md)
- [Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning](../../../agent-research/2609.38147-meta-reasoning/README.md)
- [SAGE: Symbolic Action-Gating and Editing for LLM Task Planners](../../../agent-research/2609.34268-sage/README.md)
- [SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs](../../../agent-research/2609.10901-searchatlas/README.md)
- [DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories](../../../agent-research/2608.26557-deeprepro/README.md)
- [LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation](../../../agent-research/2608.11967-loongreflect/README.md)
- [ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning](../../../agent-research/2608.03468-toollift/README.md)
- [HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents](../../../agent-research/2608.02650-hyperagent/README.md)
- [Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval](../../../agent-research/2605.06647-sira/README.md)
- [LATS](../../../agent-research/2310.04406-lats/README.md)
- [ReWOO](../../../agent-research/2305.18323-rewoo/README.md)
- [Tree of Thoughts](../../../agent-research/2305.10601-tree-of-thoughts/README.md)
- [ReAct](../../../agent-research/2210.03629-react/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/planning-and-search.md) · [返回全部精读卡片](../index.md)
