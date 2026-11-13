---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 规划先问何时见反馈，再问要不要展开搜索

[Agent](../index.md) · 更新 2026-11-13 · 19 篇主题资料 / 9 篇重点对照

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
| [Budget-Aware Tool Use Enables Effective Agent Scaling](../../../agent-research/2511.17006-bats/README.md) · [原始来源](https://arxiv.org/abs/2511.17006)<br>章节：核心公式、数据协议与代码映射、结果、负控与边界 | 持续注入逐工具预算，并由外部SUCCESS/CONTINUE/PIVOT信号调节尝试；摘要清理历史但不补额度，任一工具耗尽结束。 | 统一token/工具账本是实际消耗而非预算上限；本地只有状态与费用核，没有语义规划、自验证、网页工具、答案judge或准确率结论。 |
| [DS-STAR: Data Science Agent via Iterative Planning and Verification](../../../agent-research/2509.21825-ds-star/README.md) · [原始来源](https://arxiv.org/abs/2509.21825)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、复现边界 | 以计划、代码和实际输出为条件显式检查语义充分性；不足时在追加与删除错误后缀之间路由，再生成一步。 | 比只追加步骤更能撤销错误依赖，但核心verifier/router依赖外部语义模型。本地仅验证回溯、数据流和预算，末轮未经验证的新稿不得计成功；商业完整评测未运行。 |
| [An AI system to help scientists write expert-level empirical software (ERA)](../../../agent-research/2509.06503-era-flat-puct/README.md) · [原始来源](https://arxiv.org/abs/2509.06503)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、高成本完整实验与边界 | 将所有已执行程序平铺竞争，用任务分数的归一化排名、整树均匀先验和祖先访问计数决定下一次代码变异。 | 不回传后代 rollout 均值，也不按根到叶递归选择；与 LATS 的行动轨迹、环境反馈及价值回传不是同一价值语义。外部执行、评分和数据隔离未在 CPU 算术核中实现，不能把节点数或夹具满分当成科研能力。 |

</div>

## 取舍分析 {#analysis}

### 先规划完整依赖，还是等观察再决定

ReWOO 的变量引用说明它不是不看工具证据，而是不让 Planner 在每轮观察后重新生成整段思考；后续参数仍可由前序证据填入。ReAct 则让真实返回直接参与下一次选择，适合路径会随结果变化的任务。若工具步骤结构稳定，预规划可能减少重复输入；若异常会改变目标或可用操作，必须考虑重新决策路径。两者要按完整交付成本比较，不能只数 Planner 调用。

对照来源：[react](../../../agent-research/2210.03629-react/README.md) · [rewoo](../../../agent-research/2305.18323-rewoo/README.md)

### 搜索给机会，验证决定证据的含义

ToT 与 LATS 都扩展多个方向，但前者突出中间状态评价和前沿组织，后者还通过执行与访问统计回传反馈。Jev Lookahead 进一步要求代码模拟提供可观察后继，DRAGO 用符号探针检查规格。外部计算也不是万能 oracle：模拟器可能不隔离，求解器可能解了错误规格。比较搜索器时应先固定它能看到的证据及失败含义，再讨论树宽、深度和预算。

对照来源：[tree-of-thoughts](../../../agent-research/2305.10601-tree-of-thoughts/README.md) · [lats](../../../agent-research/2310.04406-lats/README.md) · [jev-lookahead](../../../agent-research/2610.01834-jev-lookahead/README.md) · [drago](../../../agent-research/2610.22568-drago/README.md)

### 减少重复规划与有预算的自适应换路不是同一个轴

ReWOO把完整依赖计划交给Worker后再由Solver汇总，减少中间观察对Planner的反复打断；BATS让剩余额度持续参与模型决策，并通过语义自验证决定保留方向还是换路。因而开环分解与预算条件化是不同控制假设，可比较其成本记账和重启语义，但不能拿合成状态转换断言哪种真实任务更强。外部SUCCESS只表示该模块接受，不能读取gold把自检变成oracle。

对照来源：[bats](../../../agent-research/2511.17006-bats/README.md) · [rewoo](../../../agent-research/2305.18323-rewoo/README.md)

### 观察反馈不等于充分性证明，回溯也不等于状态重算

ReAct交替推理、工具动作与观察，适应新信息。DS-STAR额外把query、累计计划、代码与输出交给verifier判断是否足够，再决定追加还是删除错误后缀。删除计划后，原方法仍把上一输出给planner、上一代码给coder，它们是纠错上下文，不是已重算的前缀状态。完整执行和语义验证必须外置补齐；本地L1不得与ReAct已有隔离能力结果混排。

对照来源：[ds-star](../../../agent-research/2509.21825-ds-star/README.md) · [react](../../../agent-research/2210.03629-react/README.md)

### 程序质量排名与轨迹回报均值不能混为一种树价值

ERA 的节点是已执行程序，整树任意节点都可直接扩张；任务分数只转成相对排名供 PUCT 选择，访问更新不把子孙分数平均回传给祖先，最终仍按原始任务分数选优。LATS 以 MCTS 组织行动与 rollout，环境回报、价值统计及失败反思共同影响后续搜索。两者都需要外部反馈，却在搜索单元、单次成本和可见证据上不同。仓库 ERA 仅验证有限候选的选择算术，LATS 以完整计划为叶且未运行原文 LM value 或 WebShop；不应从这些局部结果宣布同预算科研能力胜负。公平比较必须先固定执行器、validation/test 隔离、失败费用和总预算。

对照来源：[era-flat-puct](../../../agent-research/2509.06503-era-flat-puct/README.md) · [lats](../../../agent-research/2310.04406-lats/README.md)

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

### ReWOO省去多次Planner与BATS在矛盾后PIVOT，分别付出什么代价？ {#cross-cross-open-loop-versus-budget-conditioned-pivot}

??? note "展开答案与例子"

    **答案：** ReWOO的预先分解减少重复规划但要承担计划对后来证据不适配；BATS保留动态决策但要支付规划/验证开销，并在换路时保留真实已用预算。准确率与实际费用仍须完整隔离评测，不能用本地控制核决定胜者。

    **教学例子：** 教学例：ReWOO执行预排三步工具依赖；BATS用掉一次搜索后换路仍只剩两次额度，不能为了展示更好答案重置为三次。

    对照来源：[bats](../../../agent-research/2511.17006-bats/README.md) · [rewoo](../../../agent-research/2305.18323-rewoo/README.md)

### DS-STAR删掉错误步骤后，能否把上一输出当成正确前缀的执行结果？ {#cross-cross-plan-truncation-versus-execution-replay}

??? note "展开答案与例子"

    **答案：** 不能。上一输出是整份旧代码的结果，可能依赖错误后缀。原方法把它作为纠错信息继续条件化；控制核不声称已经回滚文件状态或重算数据。必须由真实coder/executor和独立verifier处理。

    **教学例子：** 教学例：错误join后的聚合值不会因删除计划文字自动消失，外部代码必须重新生成并执行。

    对照来源：[ds-star](../../../agent-research/2509.21825-ds-star/README.md) · [react](../../../agent-research/2210.03629-react/README.md)

### 给 ERA 和 LATS 都限制一百次扩张，就能公平比较哪一个更会探索吗？ {#cross-cross-flat-program-rank-versus-rollout-value}

??? note "展开答案与例子"

    **答案：** 不能。一项 ERA 扩张需要生成并执行新程序以获得任务分数；一项 LATS rollout 可能执行多步交互并更新价值及反思。计数单位不等于成本单位，整树排名也不等于轨迹回报均值。应先统一任务和可见证据，记录模型调用、执行费用及失败成本，再隔离验证选择与测试；本地机制核尚不能提供这类能力比较。

    **教学例子：** 教学例：一个程序评估训练模型两小时，另一个轨迹只执行四次廉价工具；都算一次扩张会掩盖预算差异。探索项选中的低访问候选，也不能未经独立评测就取代最高原始 validation 分数的候选。

    对照来源：[era-flat-puct](../../../agent-research/2509.06503-era-flat-puct/README.md) · [lats](../../../agent-research/2310.04406-lats/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-13** · 补入 Google ERA 历史锚点，区分全树程序排名 PUCT 与 LATS 轨迹 rollout/价值回传；保留 v1 访问初始化及最终原始分数选优。CPU 组件仅为机制证据，完整多任务科研搜索高成本不复现。

涉及：[era-flat-puct](../../../agent-research/2509.06503-era-flat-puct/README.md) · [lats](../../../agent-research/2310.04406-lats/README.md)

**2026-11-13** · 补入Google/KAIST DS-STAR历史漏项，区分语义充分性、计划回溯与真实执行状态；CPU三seed只验控制，完整商业Agent评测未复现，不能夸大为大训练。

涉及：[ds-star](../../../agent-research/2509.21825-ds-star/README.md) · [react](../../../agent-research/2210.03629-react/README.md)

**2026-11-12** · 补充预算条件化搜索与实际费用轴，区分BATS动态换路和ReWOO开环解耦；强调任一工具耗尽、换路保留用量和外部verifier非gold能力证据。

涉及：[bats](../../../agent-research/2511.17006-bats/README.md)

**2026-10-27** · 首版：比较反馈时机、thought与MCTS搜索、代码后继模拟和形式规格诊断，区分规划效率与验证证据。

覆盖 16 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 19 篇资料</summary>

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
- [Budget-Aware Tool Use Enables Effective Agent Scaling](../../../agent-research/2511.17006-bats/README.md)
- [DS-STAR: Data Science Agent via Iterative Planning and Verification](../../../agent-research/2509.21825-ds-star/README.md)
- [An AI system to help scientists write expert-level empirical software (ERA)](../../../agent-research/2509.06503-era-flat-puct/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/planning-and-search.md) · [返回全部精读卡片](../index.md)
