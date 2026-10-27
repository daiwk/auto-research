---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 评测追问四件事：完成了、稳健吗、靠什么、花多少

[Agent](../index.md) · 更新 2026-10-27 · 43 篇主题资料 / 6 篇重点对照

GAIA测最终任务回答，AgentPerturb检查单目标输入扰动，User Proxy Bench检查用户模拟是否偷省信息获取；AlphaDiana完整记录失败与重试，HDA拆解harness涨分来源，选择性评测则约束自动裁判的错误区域。高分只有在这些协议讲清后才有可解释性。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/agent-research/evaluation-and-reliability.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：测最终产物、输入稳健性、用户合同还是自动裁判风险 · 配对干预改变输入、算力或已检测捷径中的哪一项 · 缺失评分、重试和共享记忆是否留在分母与成本里 · 置信区间和证书以独立任务还是相关轨迹为单位

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [GAIA](../../../agent-research/2311.12983-gaia/README.md) · [原始来源](https://arxiv.org/abs/2311.12983)<br>章节：背景与主要改动、核心公式、复现边界 | 真实工具与多模态问题以规范化短答案精确匹配、三级难度组织最终得分。 | 最终正确不解释过程或依赖何种帮助；本地gaia-mini仅验证协议，不代表原466问题能力。 |
| [AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations](../../../agent-research/2610.21624-agent-perturb/README.md) · [原始来源](https://arxiv.org/abs/2610.21624)<br>章节：背景与主要改动、核心公式、真实性、gold 隔离与成本 | 四类输入面交叉三类扰动，只改一个目标并独立验证仍可解，再做双侧任务配对。 | 语法有效不等于语义保真，未评分任务必须保留覆盖率和未知区间；本地算术fixture不是官方真实环境矩阵。 |
| [UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training](../../../agent-research/2609.38043-userproxybench/README.md) · [原始来源](https://arxiv.org/abs/2609.38043)<br>章节：背景与主要改动、本地复现 | 把用户合同所有适用项的乘积作为UFS，单独审计用户是否在被问前泄露私有字段。 | 任务reward不替代proxy保真，提前泄露可让任务成功但测不到主动询问；本地只验rubric与事件时序。 |
| [AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks](../../../agent-research/2610.20675-alpha-diana/README.md) · [原始来源](https://arxiv.org/abs/2610.20675)<br>章节：背景与主要改动、核心公式、无 gold 边界与限制 | 以稳定逻辑样本区分attempt，保留未评分状态并累计所有重试成本，在统一政策下比较模型—Harness系统。 | 已确认正确比例不是未知评分补齐后的真实成功率；缺成本时不报完整每成功token。本地只有合成会计协议。 |
| [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](../../../agent-research/2610.22466-harness-decomposition/README.md) · [原始来源](https://arxiv.org/abs/2610.22466)<br>章节：背景与主要改动、核心公式、本地复现与边界 | 先检验配对增益，再构造人审算力匹配与捷径中和四臂，分解额外算力、已检测捷径和剩余项。 | 中和只能覆盖已发现机制，剩余项仍可能含捷径，不能直接当迁移证据；本地只执行已测四臂统计。 |
| [Certified Selective Automation of LLM Agent Evaluation](../../../agent-research/2609.34320-certified-selective-eval/README.md) · [原始来源](https://arxiv.org/abs/2609.34320)<br>章节：背景与主要改动、复现边界 | 以任务簇bootstrap估计自动判断区域的错误率上界，证书低于预算才自动接管。 | 依赖校准任务簇与目标自动区域，不能把轨迹数当独立样本；本地mini证书不代表论文语料覆盖或通用裁判可靠。 |

</div>

## 取舍分析 {#analysis}

### 任务成功可以掩盖测量对象已经改变

GAIA式终局精确答案说明交付是否匹配参考，但若模拟用户提前透露本应由Agent询问的信息，任务仍成功却少测了信息获取。User Proxy Bench因此把UFS与任务reward分开。AgentPerturb从另一方向要求输入修改仍保持目标和可求解性：故意破坏到无解再责怪Agent，也没有测到原本想测的稳健性。好评测应控制任务与可见信息，而不只让分数发生变化。

对照来源：[gaia](../../../agent-research/2311.12983-gaia/README.md) · [user-proxy-bench](../../../agent-research/2609.38043-userproxybench/README.md) · [agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md)

### 配对设计之后，还要保留失败和归因条件

AlphaDiana强调逻辑样本不随重试扩张，所有attempt成本都要累计，运行成功与已评分分开。HDA的四臂要求逐样本对齐、预算控制与人审中和，且先确认涨分再归因。选择性评测的簇级证书则处理另一种相关性：同任务多条轨迹不能伪装成许多独立校准样本。它们共同约束怎样解释数字，却没有把未知评分、未检测捷径或未覆盖任务自动变成已验证。

对照来源：[alpha-diana](../../../agent-research/2610.20675-alpha-diana/README.md) · [harness-decomposition](../../../agent-research/2610.22466-harness-decomposition/README.md) · [certified-selective-eval](../../../agent-research/2609.34320-certified-selective-eval/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 一个工具任务最终答对，为什么 User Proxy Bench 仍可能判该评测不合格，AgentPerturb又要求扰动后仍可解？ {#cross-success-versus-proxy-fidelity}

??? note "展开答案与例子"

    **答案：** 前者检查用户模拟是否遵守信息披露合同：没被问就给私有字段，会让Agent绕过本应展示的澄清能力。后者检查被改输入仍对应相同目标且可执行可求解，避免把无解任务冒充稳健性下降。终局准确率只看交付，两种协议分别约束帮助是否过量与破坏是否过量。

    **教学例子：** 教学例：订单号应先询问，模拟用户开场直接给出会偷省步骤；反过来删掉订单号却禁止澄清，也不能公平要求Agent完成。

    对照来源：[gaia](../../../agent-research/2311.12983-gaia/README.md) · [user-proxy-bench](../../../agent-research/2609.38043-userproxybench/README.md) · [agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md)

### 扰动侧grader失败、干净侧正确，还有两次重试时，AgentPerturb与AlphaDiana会怎样防止“越失败分越好看”？ {#cross-missing-pairs-and-retries}

??? note "展开答案与例子"

    **答案：** AgentPerturb只在双侧已评分的相同任务对计算配对差，同时保留全部请求的覆盖率和未知上下界，不静默删掉未测对。AlphaDiana让重试仍属同一逻辑样本，采用最新记录而非最好记录，所有已知attempt成本累计；评分或token缺失时不伪造完整成功成本。

    **教学例子：** 教学例：三次尝试花了很多token，最终grader中断；不能只保留先前一次成功，也不能把中断样本从请求分母里删掉。

    对照来源：[agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md) · [alpha-diana](../../../agent-research/2610.20675-alpha-diana/README.md)

### HDA中和已检测捷径后仍涨分，与选择性评测的错误率证书通过，为什么是两种不同结论？ {#cross-gain-attribution-versus-risk-certificate}

??? note "展开答案与例子"

    **答案：** HDA比较四臂结果，剩余项是扣除已检测捷径和算力解释后的部分，仍可能含未知捷径，不能直接证明迁移。选择性证书则在校准任务簇上约束某个自动判断区域的错误上界，不解释某个harness为什么涨分。前者是收益来源分析，后者是判断接管条件，都需保留任务范围和统计单位。

    **教学例子：** 教学例：裁判在某区域的误判上界达标，不说明Agent提升来自推理；移除一种捷径后仍有效，也不保证裁判在新域同样可靠。

    对照来源：[harness-decomposition](../../../agent-research/2610.22466-harness-decomposition/README.md) · [certified-selective-eval](../../../agent-research/2609.34320-certified-selective-eval/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较终局能力、单目标扰动、用户合同、失败重试会计、四臂归因与簇级选择性证书。

覆盖 43 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 43 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [PLE: Physical-Engineering&#x27;s Last Exam](../../../agent-research/2610.30537-physical-engineering-exam/README.md)
- [SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning](../../../agent-research/2610.23128-scope-replay/README.md)
- [ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets](../../../agent-research/2610.21098-tool-bottleneck-bench/README.md)
- [Shortcut Sensitivity in Agent-Safety Evaluations](../../../agent-research/2610.22243-shortcut-sensitivity/README.md)
- [SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents](../../../agent-research/2610.21082-scipivot/README.md)
- [PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents](../../../agent-research/2610.22124-probe/README.md)
- [Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries](../../../agent-research/2610.22273-librarian-agents/README.md)
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](../../../agent-research/2610.22466-harness-decomposition/README.md)
- [GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models](../../../agent-research/2610.21893-gacc-bench/README.md)
- [Disagreement-Guided Weak-to-Strong Routing](../../../agent-research/2610.22245-disagreement-routing/README.md)
- [AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations](../../../agent-research/2610.21624-agent-perturb/README.md)
- [What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports](../../../agent-research/2610.20003-ctxgap/README.md)
- [Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents](../../../agent-research/2610.20845-coda/README.md)
- [AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks](../../../agent-research/2610.20675-alpha-diana/README.md)
- [CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline](../../../agent-research/2610.19128-clasharness/README.md)
- [One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails](../../../agent-research/2610.12292-option-channel-attack/README.md)
- [OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport](../../../agent-research/2610.12375-ontrack/README.md)
- [SpecGuard: Proving a Task Is Broken Before the Agent Cheats](../../../agent-research/2610.09159-specguard/README.md)
- [VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks](../../../agent-research/2610.00972-veriharness/README.md)
- [Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover](../../../agent-research/2610.01073-safe-self-improvement/README.md)
- [PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents](../../../agent-research/2610.01349-pace-capability/README.md)
- [DeFA: Dependency-Guided Failure Attribution for LLM Agents](../../../agent-research/2610.01256-defa/README.md)
- [UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training](../../../agent-research/2609.38043-userproxybench/README.md)
- [Certified Selective Automation of LLM Agent Evaluation](../../../agent-research/2609.34320-certified-selective-eval/README.md)
- [An Empirical Study of Harness Design for Coding Agents](../../../agent-research/2609.20804-harness-design-study/README.md)
- [Verifiable Social Reasoning for LLM Assistants](../../../agent-research/2609.17496-fuse-evaluator/README.md)
- [SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents](../../../agent-research/2609.04629-silr/README.md)
- [RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution](../../../agent-research/2608.27439-redevoagent/README.md)
- [Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation](../../../agent-research/2608.17177-spec-driven-tests/README.md)
- [HarnessOpt-Bench: Evaluating LLMs at Harness Optimization](../../../agent-research/2608.06301-harnessopt-bench/README.md)
- [OSReward / OS-Shepherd](../../../agent-research/2607.28609-osreward/README.md)
- [FinanceHarness: Autonomous Financial Deep Research Framework](../../../agent-research/2607.27853-finance-harness-protocol/README.md)
- [AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents](../../../agent-research/2607.18754-agentdebugx/README.md)
- [LogAct: Enabling Agentic Reliability via Shared Logs](../../../agent-research/2604.07988-logact/README.md)
- [TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems](../../../agent-research/2604.05364-tfrbench/README.md)
- [ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders](../../../agent-research/2602.16938-convapparel/README.md)
- [CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution](../../../agent-research/2602.07918-causal-armor/README.md)
- [AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents](../../../agent-research/2602.06855-airs-bench/README.md)
- [LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning](../../../agent-research/2601.13880-lifeagentbench/README.md)
- [CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation](../../../agent-research/2601.12208-coreflect/README.md)
- [SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints](../../../agent-research/2503.08669-sopbench-protocol/README.md)
- [GAIA](../../../agent-research/2311.12983-gaia/README.md)
- [AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics](../../../agent-research/autoformbench/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/evaluation-and-reliability.md) · [返回全部精读卡片](../index.md)
