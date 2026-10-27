---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 交互学习：统一轨迹之后，信用和教师信息怎样分配

[Agent](../index.md) · 更新 2026-10-27 · 53 篇主题资料 / 6 篇重点对照

Agent Lightning先把执行整理成可训练transition；GiGPO、AdaStep和DepGPO分别利用重复状态、回报方差与命令依赖分配信用；Frontier-OPD和ASTEROID则改变教师数据怎样进入学生学习。记录成轨迹只是入口，训练目标和可见信息才定义算法。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/agent-research/agent-policy-learning.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：监督单位是token、environment step、命令依赖还是专家轨迹 · 局部信用依赖状态重复、随机回报还是可信tracer · 教师只提供分布/短桥，还是完整成功episode · 特权信息处在训练侧还是部署输入中

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Agent Lightning](../../../agent-research/2508.03680-agent-lightning/README.md) · [原始来源](https://arxiv.org/abs/2508.03680)<br>章节：背景与主要改动、核心公式、复现边界 | 将执行记录为统一MDP transition，解耦训练与执行，再接入credit assignment。 | 统一接口不指定所有信用算法；本地只更新受控patch policy，没有对LLM运行LightningRL。 |
| [GiGPO](../../../agent-research/2505.10978-gigpo/README.md) · [原始来源](https://arxiv.org/abs/2505.10978)<br>章节：背景与主要改动、核心公式、复现边界 | 完整轨迹组产生macro优势，相同anchor state的跨轨迹step组提供micro相对优势。 | 依赖可信状态对齐和足够重复；本地以共享计划步骤代理anchor，不是实际环境状态合流。 |
| [AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning](../../../agent-research/2610.03223-adastep/README.md) · [原始来源](https://arxiv.org/abs/2610.03223)<br>章节：背景与主要改动、核心公式、复现边界 | 用动作间解释的回报方差比例调节局部优势，动作内后续波动大时降低局部修正。 | 不另训critic，但需要同锚多动作与重复样本；本地合成回报只检验估计方向，没有策略更新。 |
| [Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents](../../../agent-research/2610.03634-depgpo/README.md) · [原始来源](https://arxiv.org/abs/2610.03634)<br>章节：背景与主要改动、公式与关键区别、复现边界与下一步 | 从verifier资源向命令读写依赖反追，给直接/间接写入和支持读取分信用，并保持token加权优势均值。 | 依赖真实tracer和verifier资源清理，不从shell文本猜依赖；本地手工命令诊断非Terminal-Bench训练。 |
| [Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond](../../../agent-research/2610.32802-frontier-opd/README.md) · [原始来源](https://arxiv.org/abs/2610.32802v1)<br>章节：背景与主要改动、核心公式、本地复现 | 轨迹平衡聚合有符号师生分歧来挑介入状态，短教师桥加学生续跑经等长agreement门后仅桥响应入训练。 | 排名不是接纳、agreement不是成功率，验证续跑不进入训练池；本地A100只验L1数值协议，完整训练高成本。 |
| [Asymmetric On-Policy Distillation Learns In-Context Exploration](../../../agent-research/2610.30105-asteroid/README.md) · [原始来源](https://arxiv.org/abs/2610.30105v1)<br>章节：背景与主要改动、核心公式、保留的定义机制与缩小边界 | 学生先收探索历史，再在同隐藏任务收专家完整成功轨迹，训练学生据自身历史预测专家动作。 | BAMDP跨episode与一般POMDP takeover不可混用；本地是单步三门、真实小模型训练诊断，非多步机器人能力。 |

</div>

## 取舍分析 {#analysis}

### 局部信用的来源决定何时能相信它

GiGPO通过同锚状态中的动作回报比较补充全局优势；AdaStep进一步问差异有多少来自动作，有多少来自同动作后的随机路径。DepGPO不依赖同状态重复，而以文件、stdout和verifier资源的实际依赖提供另一种结构线索。三者不是可互换的“每步reward”：没有可信状态或tracer时，细粒度数字再多也不增加证据。Agent Lightning的统一transition有助接入，但不能自动补全这些条件。

对照来源：[gigpo](../../../agent-research/2505.10978-gigpo/README.md) · [adastep](../../../agent-research/2610.03223-adastep/README.md) · [depgpo](../../../agent-research/2610.03634-depgpo/README.md) · [agent-lightning](../../../agent-research/2508.03680-agent-lightning/README.md)

### 教师改变数据来源，不应改变部署可见世界

Frontier-OPD在学生访问状态中选择短介入，接纳需比较实际桥长加续跑的同长窗口，且只把教师桥响应加入训练。ASTEROID在学生探索历史之后提供同隐藏任务的完整成功episode，使训练覆盖专家顺利开局之外的上下文。两者都利用教师，却采不同单位和目标；部署侧仍只能用公开观察与自身历史，不能为了方便重放把隐藏任务、gold或未来结果加进actor。

对照来源：[frontier-opd](../../../agent-research/2610.32802-frontier-opd/README.md) · [asteroid](../../../agent-research/2610.30105-asteroid/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 同一动作之后的成败差很大时，GiGPO、AdaStep与DepGPO为什么需要不同的判断材料？ {#cross-local-credit-evidence}

??? note "展开答案与例子"

    **答案：** GiGPO先在相同anchor中比较动作的局部回报；AdaStep再用动作内与总方差衡量局部差异是否可信，后续随机性高就压低修正。DepGPO则看命令产生的文件和数据是否沿依赖到达verifier，不直接用同动作方差。应按环境是否有可信重复状态或tracer选择证据，不能用合成anchor代替真实状态后宣称公平胜负。

    **教学例子：** 教学例：相同查询后有的轨迹答错，可能是后续写作波动；终端任务则可检查某个写文件命令是否真的供最终测试读取。

    对照来源：[gigpo](../../../agent-research/2505.10978-gigpo/README.md) · [adastep](../../../agent-research/2610.03223-adastep/README.md) · [depgpo](../../../agent-research/2610.03634-depgpo/README.md)

### Frontier-OPD的教师桥与ASTEROID的成功专家轨迹，为什么不能统一成“当前状态打一个专家标签”？ {#cross-bridge-versus-successful-episode}

??? note "展开答案与例子"

    **答案：** Frontier-OPD用短桥改变后续可达轨迹，再以桥加学生续跑的等长agreement比较决定是否收教师响应；ASTEROID让学生探索历史成为条件，再学习同任务完整专家episode，BAMDP还跨episode保持隐藏任务。二者的上下文、收集单位和接纳条件不同，单步标签会抹去各自定义性机制。

    **教学例子：** 教学例：教师帮学生越过一步阻塞后交还控制，与学生试错两次后读一整段成功专家示范，不是同一种训练样本。

    对照来源：[frontier-opd](../../../agent-research/2610.32802-frontier-opd/README.md) · [asteroid](../../../agent-research/2610.30105-asteroid/README.md)

### 把Agent Lightning的transition记录接上GiGPO或Frontier-OPD，什么时候才算真正完成训练集成？ {#cross-transition-log-versus-actual-update}

??? note "展开答案与例子"

    **答案：** 记录必须能提供算法实际需要的状态、采样策略和合法监督，训练器还要按对应优势或蒸馏目标执行参数更新并评价。GiGPO需形成有效anchor组，Frontier-OPD需保留原历史、有效桥与训练池边界。只有方法名、计数或callback存在不够；本地受控patch更新与L1协议检查也不能冒充LLM策略训练。

    **教学例子：** 教学例：日志有一千条动作，但没有同状态关联或冻结师生概率，既无法直接算micro优势，也无法真实接纳教师桥。

    对照来源：[agent-lightning](../../../agent-research/2508.03680-agent-lightning/README.md) · [gigpo](../../../agent-research/2505.10978-gigpo/README.md) · [frontier-opd](../../../agent-research/2610.32802-frontier-opd/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较transition接入、状态组信用、方差可靠性、命令依赖与两种教师数据机制，明确训练和部署信息边界。

覆盖 53 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 53 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Frontier-OPD: Discovering the Edge of Agent Capability and Teaching Agents to Go Beyond](../../../agent-research/2610.32802-frontier-opd/README.md)
- [Asymmetric On-Policy Distillation Learns In-Context Exploration](../../../agent-research/2610.30105-asteroid/README.md)
- [RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution](../../../reproductions/2610.15772-rsipo/README.md)
- [Evo2: Evolving the Evolver through Weight-Harness Co-Evolution](../../../reproductions/2610.13025-evo2/README.md)
- [When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation](../../../agent-research/2610.12061-race/README.md)
- [Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents](../../../agent-research/2610.03634-depgpo/README.md)
- [AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning](../../../agent-research/2610.03223-adastep/README.md)
- [GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents](../../../agent-research/2609.35084-graphhca/README.md)
- [Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents](../../../agent-research/2609.34296-dr-credit/README.md)
- [Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning](../../../agent-research/2609.18417-dependency-refinement/README.md)
- [HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning](../../../agent-research/2609.13739-harness-bandit/README.md)
- [T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks](../../../agent-research/2609.11042-t1-terminal-rl/README.md)
- [What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents](../../../agent-research/2609.04518-multi-harness-rl/README.md)
- [What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents](../../../agent-research/2608.27260-ace-data/README.md)
- [SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction](../../../agent-research/2608.24870-spo-plus-plus/README.md)
- [AHEAD: Agentic Hints for Effective Agent Development](../../../agent-research/2608.24114-ahead/README.md)
- [AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces](../../../agent-research/2608.23041-autosaddler/README.md)
- [Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning](../../../agent-research/2608.23318-agent-g2/README.md)
- [AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization](../../../agent-research/2608.21292-auso/README.md)
- [SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning](../../../agent-research/2608.19842-sapo/README.md)
- [SPADE: Self-Play in Adaptive Synthetic Executable Environments](../../../agent-research/2608.19197-spade/README.md)
- [RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training](../../../agent-research/2608.18682-rtpo/README.md)
- [PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs](../../../agent-research/2608.17289-planpo/README.md)
- [TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents](../../../agent-research/2608.16156-trca/README.md)
- [Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks](../../../agent-research/2608.10357-sinkflex-rl/README.md)
- [ResidencyRL: Reinforcement Learning in Simulated Clinical Environments](../../../agent-research/2608.07418-residency-rl/README.md)
- [EnvACE](../../../agent-research/2608.06197-envace/README.md)
- [Contextual Information Policy Optimization for Search Agents](../../../agent-research/2608.06128-cipo/README.md)
- [AgentOPSD](../../../agent-research/2608.05987-agent-opsd/README.md)
- [State2State: Environment-Derived Mid-Training for LLM Agents](../../../agent-research/2608.04934-state2state/README.md)
- [OCSD](../../../agent-research/2608.04788-ocsd/README.md)
- [EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents](../../../agent-research/2608.05446-evoharness-rl/README.md)
- [HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning](../../../agent-research/2608.01597-hindsearch/README.md)
- [TAPO](../../../agent-research/2607.27973-tapo/README.md)
- [Group-Reflective Self-Distillation](../../../agent-research/2607.28076-grsd/README.md)
- [CAST](../../../agent-research/2607.25308-cast/README.md)
- [SEED](../../../agent-research/2607.14777-seed/README.md)
- [TurnOPD](../../../agent-research/2607.05804-turn-opd/README.md)
- [StepPO](../../../agent-research/2604.18401-steppo/README.md)
- [SEARL](../../../agent-research/2604.07791-searl/README.md)
- [Reasoning-Driven Synthetic Data Generation and Evaluation](../../../agent-research/2603.29791-simula/README.md)
- [Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks](../../../agent-research/2603.04364-dmast/README.md)
- [PEARL](../../../agent-research/2601.20439-pearl/README.md)
- [Agent0](../../../agent-research/2511.16043-agent0/README.md)
- [Agent-R1](../../../agent-research/2511.14460-agent-r1/README.md)
- [MUA-RL](../../../agent-research/2508.18669-mua-rl/README.md)
- [Agent Lightning](../../../agent-research/2508.03680-agent-lightning/README.md)
- [WebAgent-R1](../../../agent-research/2505.16421-webagent-r1/README.md)
- [GiGPO](../../../agent-research/2505.10978-gigpo/README.md)
- [RAGEN](../../../agent-research/2504.20073-ragen/README.md)
- [DeepResearcher](../../../agent-research/2504.03160-deepresearcher/README.md)
- [Search-R1](../../../agent-research/2503.09516-search-r1/README.md)
- [LOOP](../../../agent-research/2502.01600-loop/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/agent-policy-learning.md) · [返回全部精读卡片](../index.md)
