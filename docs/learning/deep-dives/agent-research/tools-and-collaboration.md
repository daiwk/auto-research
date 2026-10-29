---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 从会调用到能交付：工具接口、可靠性与协作合同

[Agent](../index.md) · 更新 2026-10-29 · 49 篇主题资料 / 6 篇重点对照

Toolformer 学何时调用，SWE-agent 设计动作接口，RATED 处理相关工具的运行可靠性；AutoGen 定义消息程序，MetaGPT 约束角色交付物，World of SWEcraft 再用隐藏下游检验群体产出。每层都可能失败，调用格式正确不是端到端完成的替身。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/agent-research/tools-and-collaboration.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：改进对象是调用策略、交互接口、工具选择还是团队协议 · 反馈来自语言loss、实际执行、结构交付物还是隐藏下游 · 协作状态是一段对话、显式中间物还是跨会话仓库资产 · 失败和资源如何进入最终交付口径

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [原始来源](https://arxiv.org/abs/2302.04761)<br>章节：背景与主要改动、核心公式、复现边界 | 采样API候选，通过真实返回对后续token loss的帮助筛选，再继续语言模型训练。 | 训练效用不等于所有部署工具可靠；本地确定性utility替代GPT-J loss，未执行完整continued training。 |
| [SWE-agent](../../../agent-research/2405.15793-swe-agent/README.md) · [原始来源](https://arxiv.org/abs/2405.15793)<br>章节：背景与主要改动、核心公式、复现边界 | 以专门ACI控制搜索、查看、精确编辑与测试，把软件任务变成可反复执行的动作循环。 | 接口降低操作负担，不替代理解和验证；本地真实临时仓库属于micro benchmark，不是官方SWE-bench resolved rate。 |
| [AutoGen](../../../agent-research/2308.08155-autogen/README.md) · [原始来源](https://arxiv.org/abs/2308.08155)<br>章节：背景与主要改动、核心公式、复现边界 | 以ConversableAgent、回复策略和停止条件编程消息交互，支持群聊与嵌套会话。 | 抽象灵活但协议仍需设计，角色数量不等于协作质量；本地只执行消息与交接协议，未接完整运行时。 |
| [MetaGPT](../../../agent-research/2308.00352-metagpt/README.md) · [原始来源](https://arxiv.org/abs/2308.00352)<br>章节：背景与主要改动、核心公式、复现边界 | 把软件SOP写入角色流程，每步生产结构化中间物供下游消费和验证。 | 结构化交付限制自由聊天，但上游错误仍可能被后续继承；本地有真实编辑测试，仍不代表完整LLM团队。 |
| [RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics](../../../reproductions/2610.13889-rated/README.md) · [原始来源](https://arxiv.org/abs/2610.13889)<br>章节：背景与主要改动、核心公式、结果、验证与边界 | 冻结语义双encoder取Top-K，再由metadata与逐工具discounted LinUCB利用真实执行反馈重排。 | 只知道选中工具的反馈，不能给未调用项虚构回报；本地encoder短训实际执行，但授权binding失败，未证明原生态能力。 |
| [World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds](../../../agent-research/2610.24061-world-of-swecraft/README.md) · [原始来源](https://arxiv.org/abs/2610.24061v1)<br>章节：背景与主要改动、核心公式、本地复现与成本判断 | 持久会话、issue/PR和包依赖组成软件世界，隐藏下游安装冻结版本检验集体产物。 | 本地微基准通过不足以证明下游收益，指令计数也不是墙钟；完整55K会话环境高成本，本地未运行。 |

</div>

## 取舍分析 {#analysis}

### 会选工具，还不等于工具能用

Toolformer 的调用样本依据后续预测是否受益筛选，它主要提供策略训练信号；SWE-agent 把可执行接口及返回形态整理给模型；RATED 再将语义相关与近期可靠性拆开。于是“模型愿意调用”“调用格式合法”“接口实际成功”和“答案完成任务”应是分开的记录。相关但失效的工具不能靠更高语义分弥补，接口成功也不能给未调用候选制造反事实奖励。

对照来源：[toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [swe-agent](../../../agent-research/2405.15793-swe-agent/README.md) · [rated](../../../reproductions/2610.13889-rated/README.md)

### 消息协议、中间物与生态后果

AutoGen 让谁回复、何时继续和停止成为可编程协议；MetaGPT 进一步把角色输入输出收束成SOP交付物。World of SWEcraft 将观察范围扩到跨仓库长期维护：一个包自己的测试可能通过，下游却被破坏。它们分别约束沟通控制、信息交接与最终外部影响，不能仅用消息数、角色数或产物数量替代后者。长期协作还需要持久资产与会话预算，而非无限加长单条群聊。

对照来源：[autogen](../../../agent-research/2308.08155-autogen/README.md) · [metagpt](../../../agent-research/2308.00352-metagpt/README.md) · [world-of-swecraft](../../../agent-research/2610.24061-world-of-swecraft/README.md)

### 10月29日：新方法与来源变化

Meta官方retrieval-programs现已可核验，更新RPL旧条目的开源状态；主体CC-BY-NC4，vendored检索/训练组件保留各自许可。代码公开不等于本地typed grammar突然覆盖任意Python、跨轮状态、神经检索或RL；本轮未复制源码或改变原L1证据。

对照来源：[toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [rpl](../../../agent-research/2610.24854-rpl/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### Toolformer 筛出一个有用API调用后，RATED 为什么仍可能在部署时降低这个工具的优先级？ {#cross-usefulness-versus-reliability}

??? note "展开答案与例子"

    **答案：** 训练筛选说明返回值曾帮助后续预测，不能保证服务一直可用或参数行为不漂移。RATED 先限定语义相关候选，再从实际选中工具的成功、错误和超时更新可靠性统计，用折扣适应变化。训练有用与当前可执行是两个条件，也不能因本次失败给所有未尝试工具打负分。

    **教学例子：** 教学例：汇率API在训练样本很有用，部署后连续超时；语义依旧匹配，但实际可靠性证据应影响下一次选择。

    对照来源：[toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [rated](../../../reproductions/2610.13889-rated/README.md)

### AutoGen 里已有程序员和测试员，为什么 MetaGPT 还强调结构化交付物，SWE-agent 又强调ACI？ {#cross-message-protocol-versus-artifact}

??? note "展开答案与例子"

    **答案：** 角色名只说明职责，AutoGen 的回复与终止协议组织交互；MetaGPT 规定需求、设计、实现等角色具体交付什么，减少信息在自由聊天中漂移；SWE-agent 则约束单次查看、编辑和测试怎样落地。三者分别处理控制、信息合同和动作接口，可组合但不能互相冒充。

    **教学例子：** 教学例：测试员知道何时回复，不代表拿到了明确接口规格；即便规格完整，编辑命令若不能精确定位，代码仍会改错。

    对照来源：[autogen](../../../agent-research/2308.08155-autogen/README.md) · [metagpt](../../../agent-research/2308.00352-metagpt/README.md) · [swe-agent](../../../agent-research/2405.15793-swe-agent/README.md)

### MetaGPT/SWE-agent 的仓库测试通过后，World of SWEcraft 为什么还用隐藏下游包检查？ {#cross-local-tests-versus-downstream}

??? note "展开答案与例子"

    **答案：** 本仓库测试只能覆盖维护者可见合同，跨包接口变化可能破坏真实依赖者，也可能只优化自己可见的微基准。隐藏下游在冻结发布版本上安装并检查，评价不同层面的集体交付。失败包不能从速度平均里静默移除，strict/carry也需明确；这仍不是用一个本地micro通过推导生态能力。

    **教学例子：** 教学例：库作者把函数参数改名并更新自身测试，下游仍按旧参数调用而崩溃；只有依赖者检查能暴露这种回归。

    对照来源：[metagpt](../../../agent-research/2308.00352-metagpt/README.md) · [swe-agent](../../../agent-research/2405.15793-swe-agent/README.md) · [world-of-swecraft](../../../agent-research/2610.24061-world-of-swecraft/README.md)

### 官方仓库补上后，为何仍需保留RPL本地组件边界？ {#cross-oct29-method-boundary}

??? note "展开答案与例子"

    **答案：** 来源完整性与执行保真度是两条轴。拿到完整训练代码并未使已有受限SDK执行完整策略、神经检索或蒸馏；若以后接入，需要另定成本、真实运行与许可边界。

    **教学例子：** 教学例：原来能检查检索程序语法，现在知道官方训练入口，也不能把语法测试改叫多跳QA评测。

    对照来源：[toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [rpl](../../../agent-research/2610.24854-rpl/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-29** · Meta官方retrieval-programs现已可核验，更新RPL旧条目的开源状态；主体CC-BY-NC4，vendored检索/训练组件保留各自许可。代码公开不等于本地typed grammar突然覆盖任意Python、跨轮状态、神经检索或RL；本轮未复制源码或改变原L1证据。

涉及：[rpl](../../../agent-research/2610.24854-rpl/README.md)

**2026-10-27** · 首版：比较调用学习、ACI、消息编排、SOP交付、可靠性重排与隐藏下游协作评价。

覆盖 49 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 49 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning](../../../agent-research/2610.24854-rpl/README.md)
- [World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds](../../../agent-research/2610.24061-world-of-swecraft/README.md)
- [TRACER: Trajectory-Aware Tool Retrieval for LLM Agents](../../../agent-research/2610.21267-tracer/README.md)
- [SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems](../../../agent-research/2610.21113-structural-signal-retriever/README.md)
- [LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents](../../../agent-research/2610.22280-leash/README.md)
- [JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs](../../../agent-research/2610.21412-jev-agent-harness/README.md)
- [A team of Gemini 4 Argon agents beats Minecraft](../../../agent-research/2610.22319-gemini-minecraft/README.md)
- [Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure](../../../agent-research/2610.21281-diviner/README.md)
- [ARIA: Runtime Inspection and Amendment for Multi-Agent Systems](../../../agent-research/2610.20780-aria/README.md)
- [RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics](../../../reproductions/2610.13889-rated/README.md)
- [When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows](../../../reproductions/2610.13092-jev-workflow/README.md)
- [Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks](../../../agent-research/2610.02001-mingbird/README.md)
- [CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents](../../../agent-research/2609.18779-cera-moa/README.md)
- [RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views](../../../agent-research/2609.16936-repoatlas/README.md)
- [Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration](../../../agent-research/2609.12464-hcrg/README.md)
- [Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks](../../../agent-research/2609.08404-feedback-scaffold/README.md)
- [SWE-Prime: Fewer Trajectories, Better Performance](../../../agent-research/2608.27449-swe-prime/README.md)
- [TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development](../../../agent-research/2608.26086-traceml/README.md)
- [TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving](../../../agent-research/2608.25523-topas/README.md)
- [ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs](../../../agent-research/2608.25992-progrouter/README.md)
- [AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research](../../../agent-research/2608.25559-adavdr/README.md)
- [SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification](../../../agent-research/2608.24571-smith/README.md)
- [Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution](../../../agent-research/2608.06811-pmcoder/README.md)
- [CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents](../../../agent-research/2608.05886-codegrep/README.md)
- [MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems](../../../agent-research/2607.28527-manta/README.md)
- [CAM-DF](../../../agent-research/2607.27083-cam-df/README.md)
- [Formalizing Mathematics at Scale](../../../agent-research/2605.29955-autoformbot/README.md)
- [PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving](../../../agent-research/mlsys2026-prompts/README.md)
- [PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing](../../../agent-research/2604.05018-paperorchestra/README.md)
- [AIRA2: Overcoming Bottlenecks in AI Research Agents](../../../agent-research/2603.26499-aira2/README.md)
- [Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair](../../../agent-research/2601.19066-dynamic-brt/README.md)
- [Watch and Learn: Learning to Use Computers from Online Videos](../../../agent-research/2510.04673-watch-and-learn/README.md)
- [ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients](../../../agent-research/2508.04086-toolgrad/README.md)
- [ToolRL](../../../agent-research/2504.13958-toolrl/README.md)
- [ReTool](../../../agent-research/2504.11536-retool/README.md)
- [OpenHands](../../../agent-research/2407.16741-openhands/README.md)
- [SWE-agent](../../../agent-research/2405.15793-swe-agent/README.md)
- [AutoGen](../../../agent-research/2308.08155-autogen/README.md)
- [MetaGPT](../../../agent-research/2308.00352-metagpt/README.md)
- [ToolBench](../../../agent-research/2305.16504-toolbench/README.md)
- [CRITIC](../../../agent-research/2305.11738-critic/README.md)
- [CAMEL](../../../agent-research/2303.17760-camel/README.md)
- [HuggingGPT](../../../agent-research/2303.17580-hugginggpt/README.md)
- [ART](../../../agent-research/2303.09014-art/README.md)
- [Toolformer](../../../agent-research/2302.04761-toolformer/README.md)
- [PAL](../../../agent-research/2211.10435-pal/README.md)
- [MRKL](../../../agent-research/2205.00445-mrkl/README.md)
- [SayCan](../../../agent-research/2204.01691-saycan/README.md)
- [WebGPT](../../../agent-research/2112.09332-webgpt/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/tools-and-collaboration.md) · [返回全部精读卡片](../index.md)
