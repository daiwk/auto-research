# Agent 研究：按年份

按首次公开年份浏览；同年论文按日期倒序排列，每篇独占一行并附主要方法简介。

## 2026

- 2026-08 · [Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning](../2608.23318-agent-g2/README.md)（`agent-g2`）：Hint-based Agent RL 保留专家轨迹前缀再让策略探索，但固定深度忽略任务难度，逐样本 probe 又浪费 rollout。Agent-G² 从已有 policy rollout 按难度簇估计 guidance band 的中心和方差，对每个任务采样不同前缀深度。
- 2026-08 · [AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces](../2608.23041-autosaddler/README.md)（`autosaddler`）：长任务中 prompt、tool configuration 和 middleware 的小错误会累积，而人工调 harness 成本高。AutoSaddler 把 harness 当代码：从 mini-batch 失败 trace 做深度诊断，生成有边界的结构化 patch，在同 batch 检查因果效果，再用 dev set 选更新并写入 EvoDAG，形成可持续版本。
- 2026-08 · [AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization](../2608.21292-auso/README.md)（`auso`）：外部技能检索有上下文开销，完全内化又失去按任务选择能力；按整条轨迹成功率硬切阶段还无法判断某一个动作是否真正受益。AUSO 先用 skill-conditioned teacher 内化通用技能，再进行 outcome-driven exploration，最后对每个动作比较有技能和无技能策略的 JSD，以有界权重调整 GRPO advantage。
- 2026-08 · [SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning](../2608.19842-sapo/README.md)（`sapo`）：同一自回归骨干在不同因果边界输出 policy/value，结合 PPO、on-policy SARSA 和 trajectory GAE。
- 2026-08 · [RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training](../2608.18682-rtpo/README.md)（`rtpo`）：把多轮 rollout 组织成稀疏反向树，按时间逆序更新 turn，令决策与下游 continuation 保持 on-policy。
- 2026-08 · [SPADE: Self-Play in Adaptive Synthetic Executable Environments](../2608.19197-spade/README.md)（`spade`）：同一 LLM 分饰环境设计者和推理 Agent，以有/无 privileged hint 的 regret 学习能力边界上的可执行环境。
- 2026-08 · [PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs](../2608.17289-planpo/README.md)（`planpo`）：在成功轨迹内同时比较 trajectory turn 数和单 turn response 长度，形成 coarse-to-fine planning advantages。
- 2026-08 · [TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents](../2608.16156-trca/README.md)（`trca`）：无需成功 anchor，从每个状态转移的 Evidence、Execution、Invalidity rubric 构造基础和 breakthrough reward。
- 2026-08 · [HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation](../2608.15703-hymem/README.md)（`hymem`）：把 planning、execution 和 isolated reasoning 分层，结构化摘要在 context refresh 间保存任务进展。
- 2026-08 · [LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation](../2608.11967-loongreflect/README.md)（`loongreflect`）：把 reflect/backtrack 视为可逆轨迹树的 memory-control actions，以 privileged teacher 快通道和 outcome GRPO 慢通道协调训练。
- 2026-08 · [Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks](../2608.10357-sinkflex-rl/README.md)（`sinkflex-rl`）：长程工具 Agent 的 on-policy rollout 同时受环境状态、长上下文和训练显存限制。SinkFlex-RL 把 Gymnasium 双控制环境、VERL 风格数据流、无 value model 的 GRPO 与 sink-aware FlexAttention 组合，causal / sliding-window mask 下仍保留模型特有 sink scaling。
- 2026-08 · [OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks](../2608.09380-openloopevolve/README.md)（`openloopevolve`）：把 observation/planning/memory/action/verification/recovery 等 Loop Policy 资产版本化，以 Champion–Challenger、发布监控和回滚治理进化。
- 2026-08 · [Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution](../2608.06811-pmcoder/README.md)（`pmcoder`）：用层级 phase planner 条件化 episodic retrieval，再用记忆轨迹统计检测 stuck 并重规划，以真实执行 verdict 验证。
- 2026-08 · [AgentOPSD](../2608.05987-agent-opsd/README.md)（`agent-opsd`）：轨迹奖励难定位少数关键决策。AgentOPSD 把 privileged replay 的 token teacher/student log-prob gap 聚合成 turn evidence，再在 log-odds 空间递归更新成功信念，以相邻信念修订量识别 pivotal turn。
- 2026-08 · [CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents](../2608.05886-codegrep/README.md)（`codegrep`）：**主题：代码检索 Agent。** 以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。
- 2026-08 · [Contextual Information Policy Optimization for Search Agents](../2608.06128-cipo/README.md)（`cipo`）：**主题：搜索 Agent RL。** 只奖励最终答案会让检索退化成确认偏见。
- 2026-08 · [EnvACE](../2608.06197-envace/README.md)（`envace`）：EnvACE 不另训 world model，而让同一个 agent policy 在真实 act 之间切换到 rehearsal role，自行预测下一 observation；训练时分别为 acting 与 rehearsal 轨迹计算 group-relative advantage，避免两种奖励尺度互相污染，测试时可用少量私有 rehearsal 扩展规划。
- 2026-08 · [HarnessOpt-Bench: Evaluating LLMs at Harness Optimization](../2608.06301-harnessopt-bench/README.md)（`harnessopt-bench`）：**主题：Harness 优化评测。** 在固定 target-evaluation 预算下，让优化器修改 prompt、工具、控制流和记忆；隐藏测试集与可信执行环境隔离搜索反馈，保留候选版本以供审计。
- 2026-08 · [Learning Globally Reusable Skills for Coding Agents](../2608.06153-gse/README.md)（`gse`）：**主题：全局技能进化。** GSE 用 Skill Relation Graph 显式维护技能关系，以聚类合并局部经验，并通过 replay verification 防止过拟合与行为回退。
- 2026-08 · [When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents](../2608.05810-vag/README.md)（`vag`）：**主题：技能进化安全。** 技能一旦进入上下文会污染后代，事后删除无法彻底回滚。
- 2026-08 · [EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents](../2608.05446-evoharness-rl/README.md)（`evoharness-rl`）：**主题：Harness policy RL。** 把 Belief、Progress、Experience 暴露为策略可操作的外部状态；先 SFT 学会 harness action，再以成本感知 GRPO 学习何时读写和合并。
- 2026-08 · [MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off](../2608.04843-memorycpt/README.md)（`memorycpt`）：**主题：端到端 Agent 记忆。** QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。
- 2026-08 · [OCSD](../2608.04788-ocsd/README.md)（`ocsd`）：直接重放未来 observation 时，token 分数变化同时来自观测信息和重放脚手架。OCSD 构造结构完全匹配的 Full 与 Observation-Ablated 两个 replay，仅以二者残差调制高不确定 step 的 GRPO 更新。
- 2026-08 · [State2State: Environment-Derived Mid-Training for LLM Agents](../2608.04934-state2state/README.md)（`state2state`）：**主题：环境派生中训练。** 从环境探索自动采样起点与目标状态，用规则化状态匹配做 verifier，形成无需人工任务与专家轨迹的可扩展 mid-training。
- 2026-08 · [ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning](../2608.03468-toollift/README.md)（`toollift`）：把工具级历史轨迹提升为可跨工具集迁移的 function workflow graph，再解耦 workflow planning 与 tool selection。
- 2026-08 · [VerMem](../2608.03137-vermem/README.md)（`vermem`）：长期记忆、活动上下文与 episodic history 往往分开优化，轨迹奖励无法判断单次记忆操作是否正确。VerMem 用一个策略管理三类状态和七种原子操作，以 local verifier 审核状态转移、global verifier 审核证据一致性。
- 2026-08 · [CoEvo-Mem](../2608.01739-coevo-mem/README.md)（`coevo-mem`）：只优化 query routing 或只更新 memory bank 会忽略二者反馈环。CoEvo-Mem 让冻结 LLM 生成 route-specific rewrite 和 prior，轻量 residual router 在线修正；任务结果更新路由，轨迹反馈更新 memory value 与 graph relation，并交替冻结一侧控制非平稳性。
- 2026-08 · [HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning](../2608.01597-hindsearch/README.md)（`hindsearch`）：**主题：搜索轨迹 hindsight。** 冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。
- 2026-07 · [HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents](../2608.02650-hyperagent/README.md)（`hyperagent`）：把工具建模为 input-schema→output-schema 超边，先构造 Task DAG，再按状态缺口扩展 producer tool support graph。
- 2026-07 · [Group-Reflective Self-Distillation](../2607.28076-grsd/README.md)（`grsd`）：轨迹终局 reward 混合了真正有效行为、重复错误与偶然选择。GRSD 让当前 policy 对同题 on-policy group 中每条已验证轨迹反思，再由参数相同的 stop-gradient 快照对比成功/失败反思，形成只在训练期可见的 DO/AVOID guidance，并调制 turn-level advantage。
- 2026-07 · [MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems](../2607.28527-manta/README.md)（`manta`）：根据任务先验初始化通信拓扑，运行中监控协作 trace，并有界调整角色、边、顺序、可见性和验证路径。
- 2026-07 · [OSReward / OS-Shepherd](../2607.28609-osreward/README.md)（`os-shepherd`）：电脑操作 Agent 需要 reward model 判断完整轨迹是否真的完成任务，但普通 accuracy 会掩盖“几乎全判成功”的宽松偏差。OSReward 汇集 Windows、macOS、Ubuntu、Android 的人工验证任务与轨迹，同时发布 Hard 和 Multi 子集；统一报告 success recall、fail recall 与两者均值 balanced accuracy，并用 OS-Shepherd-100K 训练开放 9B/35B judge。
- 2026-07 · [TAPO](../2607.27973-tapo/README.md)（`tapo`）：稀疏任务 reward 只告诉 Agent 最终成败，没有利用每次动作后的环境反馈。TAPO 复用同一 rollout，在共享 backbone 上交替训练策略目标与 $(s_t,a_t)\to s_{t+1}$ 的 next-observation 预测，不增加采样、专家数据或推理开销。
- 2026-07 · [CAM-DF](../2607.27083-cam-df/README.md)（`cam-df`）：工具 router 只能给出相关性排序，不能回答“应该开放前几个工具”。CAM-DF 在任何工具执行前虚拟遍历排序前缀，以任务充分性减异构工具成本作为 payoff；停止当前前缀与最佳后续前缀的 payoff gap 决定标签，gap 绝对值决定错误的 regret 权重。
- 2026-07 · [SkillRise](../2607.26784-skillrise/README.md)（`skillrise`）：标准 Agent RL 把任务视为独立 episode，外部 skill bank 又把抽取、检索和执行缠在一起。SkillRise 把相关但不同的任务排成由易到难的序列，让同一 policy 交替求解当前任务与整理一个直接传给下一任务的 skill document；求解阶段由当前结果监督，整理阶段由折扣后的下游任务结果监督。
- 2026-07 · [CAST](../2607.25308-cast/README.md)（`cast`）：把求解器状态价值的相邻差分变成 solver advantage，为稀疏结果奖励补充 turn 级 credit。
- 2026-07 · [HiSkill](../2607.25853-hiskill/README.md)（`hiskill`）：用高层 skill、可执行 AtomicOp 和多类有向边组织经验，推理时只检索任务相关子图来落地动作。
- 2026-07 · [UniMem](../2607.26017-unimem/README.md)（`unimem`）：新颖任务先进入 episodic buffer；反复出现且可靠的执行模式再被自路由控制器固化到可扩展 parametric memory。
- 2026-07 · [SEED](../2607.14777-seed/README.md)（`seed`）：从已完成轨迹中反思出可复用 hindsight skill，再用 skill 条件前后的动作概率变化形成稠密 on-policy 蒸馏信号。
- 2026-07 · [TurnOPD](../2607.05804-turn-opd/README.md)（`turn-opd`）：用 probe 统计自适应决定 rollout 深度，并逐步把 token KL 预算迁移为 turn-normalized 监督。
- 2026-06 · [AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems](../2606.26859-agentx/README.md)（`agentx`）：传统推荐迭代需要工程师串联假设、生产代码、上线 A/B 和归因，经验也难以跨实验积累。AgentX 将流程改造成四阶段闭环：Brainstorm Agent 从实验库、系统知识、数据分析和外部论文生成有证据的候选；Developing Agent 在仓库约束下实现并验证；Evaluation Agent 用护栏否决的线上 A/B 判断；最后以 SGPO 从成功与失败轨迹更新 Agent harness。
- 2026-04 · [StepPO](../2604.18401-steppo/README.md)（`steppo`）：Agent 的自然决策单位是“观察—动作”的 environment step，token-level MDP 会让动作粒度和信用粒度错位。StepPO 将交互重写为 step-level MDP，在 step boundary 估值和做 GAE，并把 step 内 token ratio 聚合后再裁剪。
- 2026-04 · [SEARL](../2604.07791-searl/README.md)（`searl`）：把工具和成功转移维护为图记忆；新 rollout 同时更新 policy 与图边权，形成经验池—检索—改进闭环。
- 2026-03 · [Memento-Skills](../2603.18743-memento-skills/README.md)（`memento-skills`）：从执行日志反思出结构化技能说明，按任务检索并写回版本化技能，而不是原样堆叠轨迹。
- 2026-02 · [U-Mem](../2602.22406-u-mem/README.md)（`u-mem`）：传统 Agent 记忆通常被动写入和检索，缺少“当前知识不够时主动去哪里找”的决策。U-Mem 将获取过程建模为成本递增的级联：先尝试 self/teacher，再做工具研究，最后请求 expert；检索结合语义相似度与 Thompson sampling，并在写回前验证和整理记忆。
- 2026-02 · [MemSkill](../2602.02474-memskill/README.md)（`memskill`）：controller 从历史 episode 选择记忆，designer 将重复成功模式编译为技能，并随新反馈升级技能版本。
- 2026-01 · [PEARL](../2601.20439-pearl/README.md)（`pearl`）：多跳工具调用同时受工具幻觉、参数错误和长程规划薄弱影响。PEARL 的离线阶段用 trial-and-error 建立工具用法与失败条件；在线阶段把 Planner 与 Executor 解耦，用计划正确性、工具链与最终结果组成的密集 reward 进行 GRPO，而不是只依赖稀疏成功信号。

## 2025

- 2025-12 · [SAGE](../2512.17102-sage/README.md)（`sage`）：从成功轨迹抽象技能，失败时修订或淘汰，并以任务回报学习技能检索与复用。
- 2025-11 · [Agent0](../2511.16043-agent0/README.md)（`agent0`）：任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。
- 2025-11 · [Agent-R1](../2511.14460-agent-r1/README.md)（`agent-r1`）：把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。
- 2025-10 · [LEGOMem](../2510.04851-legomem/README.md)（`legomem`）：整段成功轨迹难以迁移到新任务，单一全局记忆又混合了任务分解和工具执行。LEGOMem 把经验拆成像积木一样的 procedural units：orchestrator memory 保存任务分解与委派，agent memory 保存具体动作模板，运行时按新任务重新组合。
- 2025-08 · [MUA-RL](../2508.18669-mua-rl/README.md)（`mua-rl`）：既有 tool-use RL 通常把用户请求视为固定输入，但真实用户会根据 Agent 回答不断修改需求。MUA-RL 将 LLM 模拟用户直接放入 rollout，Agent 在对话中澄清意图并调用真实 MCP/数据库工具；用户消息和工具结果不计入策略 loss，只用最终任务完成奖励鼓励探索。
- 2025-08 · [Agent Lightning](../2508.03680-agent-lightning/README.md)（`agent-lightning`）：传统 Agent RL 常把所有上下文拼成单序列并与框架强耦合。Agent Lightning 将执行记录成统一 MDP transition，以 credit assignment 拆解轨迹，并采用训练/执行分离架构。
- 2025-07 · [MemTool](../2507.21428-memtool/README.md)（`memtool`）：大量 MCP 工具描述会迅速占满上下文，静态截断又可能删掉当前工作流需要的工具。MemTool 比较 autonomous、workflow 和 hybrid 管理方式；hybrid 策略保护当前工作流的必需工具，其余工具依据近期性和历史成功率动态淘汰。
- 2025-05 · [WebAgent-R1](../2505.16421-webagent-r1/README.md)（`webagent-r1`）：网页交互会不断累积 HTML 和历史动作，单轮 GRPO 无法处理状态变化。WebAgent-R1 动态保留近期和任务相关上下文，并行采集完整多轮轨迹，再用 M-GRPO 根据最终成功奖励执行组内相对更新；论文同时强调行为克隆 warm-up 和长 CoT 初始化。
- 2025-05 · [GiGPO](../2505.10978-gigpo/README.md)（`gigpo`）：多轮 Agent 的最终奖励稀疏，整条轨迹的 group relative advantage 无法判断哪个 environment step 做对了。GiGPO 先在完整轨迹组上计算 macro advantage，再按跨轨迹重复到达的 anchor state 建立 step group，计算 micro relative advantage。
- 2025-04 · [RAGEN](../2504.20073-ragen/README.md)（`ragen`）：单轮数学 RL 的优化单位是一次回答，而 Agent 要在随机环境中跨多轮决策。RAGEN 提出 StarPO，把 state、thinking、action 和 reward 组织成完整轨迹。
- 2025-04 · [ToolRL](../2504.13958-toolrl/README.md)（`toolrl`）：联合优化工具选择、参数生成和执行结果；动态 reward scaling 让不同工具难度进入同一 RL batch。
- 2025-04 · [ReTool](../2504.11536-retool/README.md)（`retool`）：策略在自然语言 reasoning 与工具执行之间交替，并由可执行反馈学习调用、纠错和停止。
- 2025-04 · [DeepResearcher](../2504.03160-deepresearcher/README.md)（`deepresearcher`）：把 search、browse、证据收集和带引用回答作为一条轨迹，用答案与引用联合奖励训练研究策略。
- 2025-03 · [Search-R1](../2503.09516-search-r1/README.md)（`search-r1`）：普通 RAG 一次检索后再回答，无法让策略根据中间证据继续调整查询。Search-R1 把搜索引擎视为环境：模型可在 reasoning 中多次输出搜索动作，环境返回文档后继续推理。
- 2025-02 · [LOOP](../2502.01600-loop/README.md)（`loop`）：长程数字 Agent 的 rollout 昂贵，而传统 PPO 还要维护 value model。LOOP 把 PPO trust region 与 leave-one-out baseline 结合：无需 critic，可对同一批轨迹进行多次更新；逐 token importance ratio 只裁剪漂移 token，不丢弃整条长轨迹。

## 2024

- 2024-07 · [OpenHands](../2407.16741-openhands/README.md)（`openhands`）：OpenHands 提供开放的软件 Agent 平台，把终端、编辑器、浏览器等动作统一到 event stream，并以 sandbox 隔离执行，覆盖修 bug、写代码和仓库维护。
- 2024-05 · [SWE-agent](../2405.15793-swe-agent/README.md)（`swe-agent`）：通用 shell 对 LLM 而言动作空间过宽、输出冗长。SWE-agent 用专门 ACI 约束仓库搜索、文件查看、精确编辑和测试，让模型能围绕 issue 定位故障并验证 patch。

## 2023

- 2023-11 · [GAIA](../2311.12983-gaia/README.md)（`gaia`）：以 466 个真实问题联合考查推理、多模态、网页浏览与工具使用，采用精确短答案和三级难度。
- 2023-10 · [MemGPT](../2310.08560-memgpt/README.md)（`memgpt`）：有限 context window 使长文档和多轮会话不断遗忘。MemGPT 借鉴操作系统虚拟内存，把常驻核心信息、当前工作上下文和外部归档分层管理；模型通过函数调用移动数据，并以 interrupt/heartbeat 控制继续推理和与用户交互。
- 2023-10 · [LATS](../2310.04406-lats/README.md)（`lats`）：ReAct 等方法通常沿单条轨迹行动，失败后缺少系统搜索。LATS 把 LM 同时作为 agent、value function 和 optimizer，嵌入 Monte Carlo Tree Search；环境执行提供外部 reward，失败轨迹生成 reflection，帮助后续搜索避开错误。
- 2023-08 · [AutoGen](../2308.08155-autogen/README.md)（`autogen`）：复杂应用常需要多个模型、工具和人类协作，手写控制流难复用。AutoGen 提供 ConversableAgent 与 conversation programming：每个角色声明能力、回复策略和终止条件，通过群聊或嵌套会话组合成工作流。
- 2023-08 · [MetaGPT](../2308.00352-metagpt/README.md)（`metagpt`）：简单串联多个聊天 Agent 容易让幻觉级联。MetaGPT 把人类软件团队的 SOP 编码成角色化消息流程，每个角色生产结构化中间物，由下游角色消费和验证。
- 2023-05 · [ReWOO](../2305.18323-rewoo/README.md)（`rewoo`）：ReAct 在每次工具返回后重新调用 LLM，token 和推理成本随轨迹增长。ReWOO 的 Planner 用变量引用写出完整多步计划，Worker 只负责填入工具证据，Solver 最后读取计划与证据生成答案，因此 Planner 不被中间观察反复打断。
- 2023-05 · [ToolBench](../2305.16504-toolbench/README.md)（`toolbench`）：分析开源 LLM 工具失败后，组合程序化使用样例、system prompt、in-context demonstration retriever 与生成格式约束。
- 2023-05 · [Voyager](../2305.16291-voyager/README.md)（`voyager`）：开放世界 Agent 需要持续选择有新颖性的任务、把成功行为积累为技能，并根据环境报错修复程序。Voyager 用 GPT-4 自动生成 curriculum，以代码作为动作空间；成功程序按描述索引进 skill library，新任务检索并组合已有技能。
- 2023-05 · [CRITIC](../2305.11738-critic/README.md)（`critic`）：仅让 LLM 反思自己的文本可能重复同一错误。CRITIC 调用搜索、代码解释器等外部工具，把可观测反馈带回修订循环，使 critique 有环境证据。
- 2023-05 · [Tree of Thoughts](../2305.10601-tree-of-thoughts/README.md)（`tree-of-thoughts`）：自回归生成和单条 CoT 很难撤销早期错误。ToT 将中间推理视为可独立评价的 thought，在树上生成多个候选，使用语言模型 value 函数选择 BFS/DFS frontier，并允许 lookahead 和 backtracking。
- 2023-04 · [Generative Agents](../2304.03442-generative-agents/README.md)（`generative-agents`）：只把完整历史塞给 LLM 无法支撑长期一致行为。论文把每次观察写入 memory stream，按 recency、importance、relevance 检索；累计重要事件达到阈值后生成更高层 reflection，再结合记忆与当前状态制定日程和行动计划。
- 2023-03 · [CAMEL](../2303.17760-camel/README.md)（`camel`）：用 inception prompting 固定 user/assistant 的角色、目标和边界，通过轮流消息完成任务并生成可研究的多 Agent 社会轨迹。
- 2023-03 · [HuggingGPT](../2303.17580-hugginggpt/README.md)（`hugginggpt`）：单个 LLM 难以覆盖视觉、语音和其他专业任务，而模型社区已有大量专家。HuggingGPT 让 ChatGPT 充当控制器：先把请求拆成带依赖的子任务，再按 Hugging Face 模型描述匹配专家，按拓扑顺序执行，最后把多模型输出组织为用户答案。
- 2023-03 · [Self-Refine](../2303.17651-self-refine/README.md)（`self-refine`）：一次生成很难同时满足所有约束。Self-Refine 让同一个 LLM 先生成初稿，再针对任务维度给出可执行反馈，最后据此改写；若反馈判断已满足要求则停止，不需要额外训练数据、人工反馈或外部 reward model。
- 2023-03 · [Reflexion](../2303.11366-reflexion/README.md)（`reflexion`）：传统 RL 要大量采样与参数更新。Reflexion 把稀疏标量/二值反馈“放大”为可执行的自然语言经验，写入长期 episodic memory；Actor 在下一 trial 读取反思，Evaluator 继续判定成功与否。
- 2023-03 · [ART](../2303.09014-art/README.md)（`art`）：既有 tool-use prompting 常需为每个任务手写示例和调用顺序。ART 根据新任务自动检索相近的推理/工具示例，让冻结 LLM 生成程序；运行器遇到工具标记就暂停生成，执行工具并注入结果后继续。
- 2023-02 · [Toolformer](../2302.04761-toolformer/README.md)（`toolformer`）：手工标注工具调用昂贵，纯 prompting 又难以让较小模型稳定决定何时调用。Toolformer 先用少量 demonstration 采样 API call，再比较插入真实返回值、隐藏返回值和完全不调用时的后续 token loss，只保留确实有用的调用并继续语言模型训练。

## 2022

- 2022-11 · [PAL](../2211.10435-pal/README.md)（`pal`）：LLM 擅长把问题分解成步骤，却会在算术和符号执行阶段出错。PAL 让 LLM 输出带变量和控制流的程序，最终计算完全交给 Python 等确定性 runtime；模型只承担自然语言理解和程序合成。
- 2022-10 · [ReAct](../2210.03629-react/README.md)（`react`）：纯 CoT 容易在封闭知识上幻觉，纯 action agent 又缺少计划与状态跟踪。ReAct 让模型交替生成自然语言推理和环境 action，再把 observation 放回下一步上下文，使推理可以纠错、行动可以获取外部事实。
- 2022-05 · [MRKL](../2205.00445-mrkl/README.md)（`mrkl`）：单个 LLM 容易在精确计算、时效知识和可验证推理上失败。MRKL 把 LLM 放入系统架构，由 router 根据输入选择语言模型、知识库、计算器等专家；离散模块保证确定性能力，语言模型负责理解和自然语言接口。
- 2022-04 · [SayCan](../2204.01691-saycan/README.md)（`saycan`）：LLM 知道“应该做什么”，却不知道当前机器人“能不能做”。SayCan 为每个预训练技能同时计算语言相关性和 value-function affordance，选择乘积最高的技能并执行，再把动作追加到上下文继续规划。

## 2021

- 2021-12 · [WebGPT](../2112.09332-webgpt/README.md)（`webgpt`）：长文本问答容易幻觉，且很难核查依据。WebGPT 让模型在文本浏览器里搜索、点击和滚动，回答必须收集引用；训练先做行为克隆，再用人类偏好 reward model 从多条浏览/回答轨迹中做拒绝采样。
