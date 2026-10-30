---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 自改进先标对象：答案、经验、接口与系统版本

[Agent](../index.md) · 更新 2026-10-30 · 46 篇主题资料 / 9 篇重点对照

Self-Refine 改当前产物，Reflexion 改下一次可读经验，HarnessLens 检查局部流程改动，Agent S4 演化接口仓库，RSIFlow 选择干预层，AgentX 把候选送到有护栏的生产闭环。多跑几轮不是共同算法，持久状态与接纳规则才决定在改什么。 CROP离线改系统提示并显式惩罚输出成本；EvalAlloc不替候选修代码，而是分配SEARCH评测预算、固定参照估计fitness并组织最终配对确认。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/agent-research/harness-and-self-improvement.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：可变对象是答案、文字经验、接口、模型还是交付物 · 变化仅服务当前任务还是成为持久版本 · 反馈用于提案、选择父本、接纳候选还是发布 · 失败候选是回滚、留在种群还是进入知识资产

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Self-Refine](../../../agent-research/2303.17651-self-refine/README.md) · [原始来源](https://arxiv.org/abs/2303.17651)<br>章节：背景与主要改动、核心公式、复现边界 | 同一模型显式生成草稿、任务维度反馈和修订，满足要求后停止。 | 主要是当前输出循环，自评可能重复错误；本地确定性critic只验证状态迁移。 |
| [Reflexion](../../../agent-research/2303.11366-reflexion/README.md) · [原始来源](https://arxiv.org/abs/2303.11366)<br>章节：背景与主要改动、核心公式、复现边界 | 将执行反馈变成自然语言反思，下一trial读取有界episodic memory。 | 改变上下文而非梯度权重，教训可能错误或过时；本地模板反思与隔离ToolRoute结果需分开解释。 |
| [Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification](../../../agent-research/2608.27311-harnesslens/README.md) · [原始来源](https://arxiv.org/abs/2608.27311)<br>章节：背景与主要改动、核心公式、复现边界 | 根据受影响行为选择成对验证任务，正增益之外还要求能归因到候选修改。 | 局部接纳节省验证，但覆盖不等于全能力；本地ToolRoute协议不是论文全部benchmark。 |
| [Evolving Agent Interfaces](../../../agent-research/2610.28601-agent-s4/README.md) · [原始来源](https://arxiv.org/abs/2610.28601)<br>章节：背景与主要改动、核心公式、成本与复现边界 | 固定任务Agent与Harness，编辑接口代码和使用知识，变异/交叉后代无论暂时分数高低都入种群。 | 验证只用于父本选择且不暴露给构建者；本地仅可信callback控制器，无真实桌面接口演化，完整实验高成本。 |
| [RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent](../../../agent-research/2610.21791-rsiflow/README.md) · [原始来源](https://arxiv.org/abs/2610.21791)<br>章节：背景与主要改动、核心公式、代码映射、成本与边界 | 依据证据在Model/Harness/Artifacts选择干预，同父代同批比较，仅有效且正增益时接受。 | 失败仍从冻结父代重试，不等于任意代码自改；本地只执行作用域、配对与技能记录，没有模型训练。 |
| [AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems](../../../agent-research/2606.26859-agentx/README.md) · [原始来源](https://arxiv.org/abs/2606.26859)<br>章节：背景与主要改动、核心公式、复现边界 | 证据提案、仓库实现、护栏线上A/B和正负资产化组成推荐迭代闭环。 | 主指标改善仍可被护栏否决；作者生产证据与本地确定性mini闭环不同，本地没有用户流量或SGPO大模型训练。 |
| [When the Critic Falls Behind: Co-Evolving Rubrics and Harnesses for Continual Agent Self-Improvement](../../../agent-research/2610.36826-ruharness/README.md) · [原始来源](https://arxiv.org/abs/2610.36826v1)<br>章节：背景与主要改动、核心公式 | 六格联合后验、2000次抽样0.2分位、active frontier与validation准入。 | 行为标签、执行结果和验证分数外置；统计排序不是完整自进化运行。 |
| [CROP: Token-Efficient Reasoning in Large Language Models via Regularized Prompt Optimization](../../../agent-research/2604.14214-crop/README.md) · [原始来源](https://arxiv.org/abs/2604.14214v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 固定目标权重，拼接任务与超阈值长度文本批评，外部元优化器重写系统提示；按准确率减CoT归一化token成本选已测提示。 | 不同于Self-Refine修当前答案；本地validation选优是明确防泄漏加强。确定性callback诊断不代表真实LLM无损缩短或完整evolve。 |
| [Where Should the Evaluation Budget Go in LLM-Driven Agent Scaffold Evolution?](../../../agent-research/2610.37276-evalalloc/README.md) · [原始来源](https://arxiv.org/abs/2610.37276v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 用SEARCH观测的信息度选共享core与无放回item，固定外部item参照仅推断新候选参数；最终公共prefix补缓存并作配对校正。 | 预测不能覆盖已测cell，评测cell减少不等于token费用等比下降；warmup MIRT、cross-fit refit和完整successive halving未实现。 |

</div>

## 取舍分析 {#analysis}

### 把“记住改法”与“系统真的改变”分开

Self-Refine 的修订对象是当前输出，Reflexion 的持久项是下次可见的文字经验；Agent S4 则把接口代码及知识作为仓库版本，使操作与观察本身可以变化。RSIFlow 再显式区分模型、流程和产物。它们都可能改善后续结果，却不能统称模型学会了：应该记录变了哪个对象、如何执行，以及下一任务继承什么，而不是只记一项policy update计数。

对照来源：[self-refine](../../../agent-research/2303.17651-self-refine/README.md) · [reflexion](../../../agent-research/2303.11366-reflexion/README.md) · [agent-s4](../../../agent-research/2610.28601-agent-s4/README.md) · [rsiflow](../../../agent-research/2610.21791-rsiflow/README.md)

### 入种群、接纳和发布是三类决定

Agent S4 保留暂时低分后代，验证分用于后续选择父本，这是非贪心搜索；RSIFlow 要有效且相对同父代提高才改变当前状态。HarnessLens 将接纳限制在行为相关的可归因证据，AgentX 的生产发布还要通过关键护栏。因此一个候选存在于档案、在局部验证通过与允许影响线上流量，不能由同一个“已接入”状态概括。这里比较的是规则和作用范围，不将不同论文的成绩排列成优劣。

对照来源：[agent-s4](../../../agent-research/2610.28601-agent-s4/README.md) · [rsiflow](../../../agent-research/2610.21791-rsiflow/README.md) · [harnesslens](../../../agent-research/2608.27311-harnesslens/README.md) · [agentx](../../../agent-research/2606.26859-agentx/README.md)

### 10月29日：新方法与来源变化

RuHarness的criterion frontier不是按一次正确率排序：2×3行为/结果联合表用Jeffreys-Dirichlet后验估计保守utility分位，集合新颖性和冗余仍固定来自已测轨迹。它把有限样本不确定性和候选准入分开，只有active准则能进入frontier，最终harness修改还要独立validation严格增益。本地没有LLM评审或harness生成。

对照来源：[self-refine](../../../agent-research/2303.17651-self-refine/README.md) · [ruharness](../../../agent-research/2610.36826-ruharness/README.md)

### 修改对象、评判标准与评测预算要分三本账

Self-Refine修当前输出，CROP则在训练样本反馈下改下一次通用系统提示，并明确计算输出token成本；它不把权重训练称为已完成。RuHarness维护能区分当前失败的rubric frontier，EvalAlloc另问应把真实评测cell花在哪些SEARCH items上：固定item参照做稀疏补全，只用预测填未观测项，最终以公共prefix与缓存确认。高rubric效用、较高预测fitness和留出任务真成功是三种证据，尤其不能把少一半cell直接宣传为少一半LLM费用。

对照来源：[crop](../../../agent-research/2604.14214-crop/README.md) · [evalalloc](../../../agent-research/2610.37276-evalalloc/README.md) · [self-refine](../../../agent-research/2303.17651-self-refine/README.md) · [ruharness](../../../agent-research/2610.36826-ruharness/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 同一回答修改三轮，与失败后留下经验再做下一次任务，Self-Refine和Reflexion在什么地方分开？ {#cross-revision-versus-episodic-learning}

??? note "展开答案与例子"

    **答案：** Self-Refine 围绕当前草稿产生反馈再修订，循环主要改变当前产物；Reflexion 将一次执行评价整理成经验，供下一trial的actor读取。二者都可使用同一冻结模型，不代表梯度训练。应检查反馈有没有进入后续上下文、是否适用新状态，以及结果有没有真实验证，不能仅用循环次数判断“学会”。

    **教学例子：** 教学例：把报告中的错数改对属于当前修订；留下“引用数字前核对原表”的经验供下次使用，才是跨trial可读状态。

    对照来源：[self-refine](../../../agent-research/2303.17651-self-refine/README.md) · [reflexion](../../../agent-research/2303.11366-reflexion/README.md)

### Agent S4保留低分后代，而RSIFlow拒绝不改善候选，两者为什么不构成矛盾？ {#cross-population-versus-current-parent}

??? note "展开答案与例子"

    **答案：** 它们维护的搜索状态不同。Agent S4 的种群保留探索来源，低分后代也可能参与后续搜索，私有验证决定父本选择；RSIFlow 每轮围绕冻结父代检验候选，失败后不改变下一次出发点。一个规则关注种群多样性，一个约束当前版本更新，不能把入档等同发布，也不能给两者套同一逐轮单调标准。

    **教学例子：** 教学例：接口变体甲暂时差但提供新操作，可留种群；某次流程修补乙无改善，RSIFlow仍从原流程再提下一候选。

    对照来源：[agent-s4](../../../agent-research/2610.28601-agent-s4/README.md) · [rsiflow](../../../agent-research/2610.21791-rsiflow/README.md)

### HarnessLens 的局部行为配对涨分，为什么不能直接替代 AgentX 的线上发布判断？ {#cross-local-admission-versus-production}

??? note "展开答案与例子"

    **答案：** 局部验证回答修改在所选行为上是否有正且可归因的收益；生产部署还涉及业务分布、关键护栏和真实资源。AgentX 主指标改善后仍允许护栏否决，并把正负实验保留供后续研究。两个阶段可衔接，但本地小协议通过没有提供用户流量因果证据，也不能自动授权发布。

    **教学例子：** 教学例：离线恢复流程成功更多，却增加线上请求延迟；局部功能证据成立，护栏仍可能要求拒绝上线。

    对照来源：[harnesslens](../../../agent-research/2608.27311-harnesslens/README.md) · [agentx](../../../agent-research/2606.26859-agentx/README.md)

### RuHarness为什么不把新颖性和冗余也随每个Dirichlet样本重抽？ {#cross-oct29-method-boundary}

??? note "展开答案与例子"

    **答案：** 这两项来自固定轨迹集合的重叠关系，不是六格结果概率。把它们一同随机化会改变原文不确定性模型；后验保守分位也不等于已证明真实Agent更强。

    **教学例子：** 教学例：两条准则标记了完全相同的失败轨迹，抽一次成功/失败概率不应让这两集合忽然不再相同。

    对照来源：[self-refine](../../../agent-research/2303.17651-self-refine/README.md) · [ruharness](../../../agent-research/2610.36826-ruharness/README.md)

### CROP和Self-Refine都让模型读反馈改文本，为什么不能用同一个“修正成功”指标概括？ {#cross-crop-prompt-versus-current-answer}

??? note "展开答案与例子"

    **答案：** Self-Refine的主要修订对象是当前答案；CROP离线改系统提示，再以准确率和CoT归一化输出token成本选已测候选。当前样本答案变好不证明提示可迁移，提示更短也不保证答案更短或正确。真实LLM回调及独立validation仍是组件之外的证据。

    **教学例子：** 教学示意：把一个算术答案改对，与得到适用于一批未见算术题的简洁系统提示，是两种验收；最后新写出的提示未评测时不能直接当最佳。

    对照来源：[crop](../../../agent-research/2604.14214-crop/README.md) · [self-refine](../../../agent-research/2303.17651-self-refine/README.md)

### EvalAlloc的高预测fitness与RuHarness的高准则效用，为什么都不能直接当真实Agent成功率？ {#cross-evalalloc-fitness-versus-rubric-frontier}

??? note "展开答案与例子"

    **答案：** EvalAlloc用固定参照估计未观测SEARCH结果，必须保留已测cell并最终确认；RuHarness衡量准则是否有保守的失败诊断价值，候选harness还需独立validation。两者分别治理观测预算和评判标准，不是已执行任务的替代答案。

    **教学例子：** 教学示意：某候选只测20/300个item，补全均值0.8并不意味着已真实完成240项；一条准则能覆盖失败，也不等于使用它后任务已经成功。

    对照来源：[evalalloc](../../../agent-research/2610.37276-evalalloc/README.md) · [ruharness](../../../agent-research/2610.36826-ruharness/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-30** · 精读CROP与EvalAlloc：以Self-Refine/RuHarness为对照，分开系统提示修改、rubric价值和SEARCH观测预算；补validation/CoT成本、观测优先补全、公共prefix确认及未实现MIRT/controller边界。

涉及：[crop](../../../agent-research/2604.14214-crop/README.md) · [evalalloc](../../../agent-research/2610.37276-evalalloc/README.md) · [self-refine](../../../agent-research/2303.17651-self-refine/README.md) · [ruharness](../../../agent-research/2610.36826-ruharness/README.md)

**2026-10-29** · RuHarness的criterion frontier不是按一次正确率排序：2×3行为/结果联合表用Jeffreys-Dirichlet后验估计保守utility分位，集合新颖性和冗余仍固定来自已测轨迹。它把有限样本不确定性和候选准入分开，只有active准则能进入frontier，最终harness修改还要独立validation严格增益。本地没有LLM评审或harness生成。

涉及：[ruharness](../../../agent-research/2610.36826-ruharness/README.md)

**2026-10-27** · 首版：比较当前修订、跨trial反思、局部验证、非贪心接口种群、分层干预与有护栏生产闭环。

覆盖 43 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 46 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training](../../../agent-research/2610.32026-rsi-opt/README.md)
- [ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation](../../../agent-research/2610.32120-image-rsi/README.md)
- [HarnessMM: Recursive Self-Improvement for Harness Token Efficiency](../../../agent-research/2610.32813-harnessmm/README.md)
- [Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design](../../../agent-research/2610.28380-oo-harness/README.md)
- [Evolving Agent Interfaces](../../../agent-research/2610.28601-agent-s4/README.md)
- [Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery](../../../agent-research/2610.24806-aptamer-lab-loop/README.md)
- [Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine](../../../agent-research/2610.22192-terminal-rsi/README.md)
- [RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent](../../../agent-research/2610.21791-rsiflow/README.md)
- [AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning](../../../agent-research/2610.22194-auto-sft/README.md)
- [Athanor: An Agent-Native System for Autonomous Post-Training Research](../../../agent-research/2610.21055-athanor/README.md)
- [The World Won&#x27;t Wait: Evaluating and Teaching Agents Under a Live Clock](../../../agent-research/2610.20665-torsi/README.md)
- [Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses](../../../agent-research/2610.15150-harmony-harness/README.md)
- [RSI-Anything: Unlocking Recursive Self-Improvement with World Models](../../../reproductions/2610.13912-rsi-anything/README.md)
- [Harness²: Recursive Agent Harnessing for an Open World](../../../agent-research/2610.14224-harness2/README.md)
- [Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks](../../../agent-research/2610.11794-memento3/README.md)
- [Recursive Self-Improvement through Multi-Agent Self-Supervision](../../../agent-research/2610.12176-mass/README.md)
- [EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution](../../../agent-research/2610.12086-evoalloc/README.md)
- [Sentry: Learning to Recover from LLM Agent Failures at Test Time](../../../agent-research/2610.02994-sentry/README.md)
- [SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting](../../../agent-research/2610.04109-seer-forecasting/README.md)
- [FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution](../../../agent-research/2610.03675-frugalevo/README.md)
- [It Takes Workflows to Evolve Better Workflows](../../../agent-research/2610.01026-flowright/README.md)
- [ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization](../../../agent-research/2610.00906-active-saddler/README.md)
- [Self-Evolving Coding Rules for AI Coding Agents](../../../agent-research/2610.00650-rule-evolve/README.md)
- [Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution](../../../agent-research/2609.37950-video-rsi/README.md)
- [Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI](../../../agent-research/2609.38143-meta-skills/README.md)
- [Mixture of Self-Improving Branches for Agent Harness Optimization](../../../agent-research/2609.37834-branch-mixture/README.md)
- [Harness Learning Enables Generalizable Test-Time Adaptation](../../../agent-research/2609.35738-harness-learning/README.md)
- [Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems](../../../agent-research/2609.30001-agentx-model/README.md)
- [ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents](../../../agent-research/2609.17523-sciencebuddy/README.md)
- [MAPLE: Memory-Augmented Planning with Language and Evolution](../../../agent-research/2609.11636-maple/README.md)
- [Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents](../../../agent-research/2609.11677-ecdysis/README.md)
- [COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization](../../../agent-research/2609.11682-cobra-skills/README.md)
- [Procedural Graphs: Self-Evolving Execution Structures for LLM Agents](../../../agent-research/2609.09153-procedural-graphs/README.md)
- [Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification](../../../agent-research/2608.27311-harnesslens/README.md)
- [JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution](../../../agent-research/2608.25593-jit-agent/README.md)
- [OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks](../../../agent-research/2608.09380-openloopevolve/README.md)
- [AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems](../../../agent-research/2606.26859-agentx/README.md)
- [ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence](../../../agent-research/2605.26340-scientist-one/README.md)
- [HyperAgents](../../../agent-research/2603.19461-hyperagents/README.md)
- [POLCA: Stochastic Generative Optimization with LLM](../../../agent-research/2603.14769-polca/README.md)
- [MARS: Modular Agent with Reflective Search for Automated AI Research](../../../agent-research/2602.02660-mars-research/README.md)
- [Self-Refine](../../../agent-research/2303.17651-self-refine/README.md)
- [Reflexion](../../../agent-research/2303.11366-reflexion/README.md)
- [When the Critic Falls Behind: Co-Evolving Rubrics and Harnesses for Continual Agent Self-Improvement](../../../agent-research/2610.36826-ruharness/README.md)
- [CROP: Token-Efficient Reasoning in Large Language Models via Regularized Prompt Optimization](../../../agent-research/2604.14214-crop/README.md)
- [Where Should the Evaluation Budget Go in LLM-Driven Agent Scaffold Evolution?](../../../agent-research/2610.37276-evalalloc/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/harness-and-self-improvement.md) · [返回全部精读卡片](../index.md)
