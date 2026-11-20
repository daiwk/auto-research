---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 自改进先标对象：答案、经验、接口与系统版本

[Agent](../index.md) · 更新 2026-11-20 · 78 篇主题资料 / 41 篇重点对照

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
| [Strategist: Evolving Reasoning with Agents](../../../agent-research/2611.03618-strategist/README.md) · [原始来源](https://arxiv.org/abs/2611.03618)<br>章节：背景与主要改动、核心公式、数据协议与实现边界、高成本完整实验 | 冻结执行模型，把可执行推理blueprint组成跨任务无环库，检索相关与邻域素材，按开发集实际准确率与分层token成本选策略。 | 库保留未获胜结构供后续任务复用，但最终候选仍须validation和hidden双过门槛；本地只实现AST/DAG、外部检索分数核和配对选择，不是meta-agent搜索。 |
| [Discovering formally verified quantum programs with AI](../../../agent-research/2611.09822-verified-quantum-wiki/README.md) · [原始来源](https://arxiv.org/abs/2611.09822v1)<br>章节：核心公式、数据协议与代码映射、结果、负控与边界 | 由独立验证器核对冻结规范，再按成本改善或代码缩短门槛将候选写入共享知识库。 | 形式证明依赖所写规格，并不是留出任务的能力比较。本地只消费外部核验结果执行合入门槛，不验证 Lean。 |
| [Meta²: Precomputing Reusable Knowledge for Online Harness Evolution in Long-Horizon Agents](../../../agent-research/2611.05139-meta-square/README.md) · [原始来源](https://arxiv.org/abs/2611.05139)<br>章节：核心公式、数据协议与实现边界、高成本完整实验 | 冻结离线Meta-Skill，在同环境、同轨迹checkpoint上有界KEEP/EVOLVE；具体编辑任务结束即弃。 | 可复用的是演化指导，不是所有任务共享的最终Harness；本地没有LLM演化器或知识学习。 |
| [From AutoResearch to Continual AutoResearch: Do Agents Learn Across Tasks?](../../../agent-research/2611.05108-continual-autoresearch/README.md) · [原始来源](https://arxiv.org/abs/2611.05108)<br>章节：核心公式、数据协议与实现边界、高成本完整实验 | 相同任务流与预算配对持续、重置运行，运行后分别计算首解、最优曲线和实际最终选择。 | 效率优势可与最终效果下降并存；本地仅离线评分合同，无自主研究或记忆收益验证。 |
| [Training LLM Agents to Automate LLM Post-Training with RSI-Dojo](../../../agent-research/2611.03698-rsi-dojo/README.md) · [原始来源](https://arxiv.org/abs/2611.03698)<br>章节：核心公式、数据协议与实现边界、高成本完整实验 | 构建可执行训练环境，筛选过程与结果均合格的轨迹，微调自动后训练Agent。 | 9B/35B-A3B与每任务5至10小时全矩阵高成本不复现；只收录，不声明运行时或权重能力。 |
| [EnvOpt: Automated Optimization for Agent Environments](../../../agent-research/2611.07372-envopt/README.md) · [原始来源](https://arxiv.org/abs/2611.07372)<br>章节：背景与主要改动、核心公式、数据协议与实现边界 | 固定模型与 Harness，把可复用的信息表示作为跨任务资产；无训练 verifier 的成本/代理筛选之后，用独立验证决定是否保留。 | 更便宜的代理轨迹可错判，验证回归即回滚；本地仅回放选择规则，不生成环境或运行 Agent。 |
| [When Should Agents Remember? Falsification-Gated Self-Evolution for LLM Agents](../../../agent-research/2611.14326-fgse/README.md) · [原始来源](https://arxiv.org/abs/2611.14326)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 临时更新在迁移、定向证伪与归档回归三个探针集分别计分，收益、风险和旧任务损伤同时达标才准入。 | 经验门依赖真实成对verifier和适当探针；本地仅Eq7–9，不含自动细化、Actor或论文置信保证，完整API实验不复现。 |
| [Program-Aided Patchable Skill Evolution](../../../agent-research/2611.14019-pase/README.md) · [原始来源](https://arxiv.org/abs/2611.14019)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 分离描述性技能与关联程序，局部patch后只在held-out validation严格改善时保留配对更新。 | 程序语法不证明正确或安全，外部分数也不能验证陈旧patch目标；本地只做preimage事务和接受/回滚，不执行模型或生成代码。 |
| [Agent Gym: A Framework for Continuous Evaluation and Evolution of LLM Agents Through Human-in-the-Loop Feedback](../../../agent-research/2608.15591-agent-gym/README.md) · [原始来源](https://arxiv.org/abs/2608.15591)<br>章节：核心公式、数据协议与代码映射、结果、负控与边界 | 以独立ALF规则层修正原Agent的JSON输出；AND检测、scope互斥、三层动作合并和显式SME批准保持纠错可审计。 | 目标匹配和collateral只描述适应案例覆盖，类型合同不证明语义正确。原Agent/模型不重训；LLM发现与自动晋升没有本地实现。 |
| [ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI](../../../agent-research/2609.19644-scientist-two/README.md) · [原始来源](https://arxiv.org/abs/2609.19644)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、复现边界 | 把科研工作拆成可拒绝、可修改、有预算的阶段；子集筛选后独立全量验证，并用成功及失败历史继续探索。 | 控制层安排实验与评审，不证明外部语义判断或实验产物真实。ScientistOne的证据完整性审计与ScientistTwo的研究扩展控制互补；本地两者都不等于完整自主科学家。 |
| [EnvHarness: Awakening Static Worlds for Agent Learning](../../../agent-research/2608.19880-envharness/README.md) · [原始来源](https://arxiv.org/abs/2608.19880)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、复现边界 | 在固定环境的标准接口外组合初态重放、动作/转换/观察hook和串行任务，保留各基础环境的成功判据。 | 它改环境而非模型外工具/记忆；可reset、可信verifier和新rollout验收是前提。本地只有CPU包装器，无EnvRigger、模型学习、真实bridge或安全sandbox。 |
| [MLE-STAR: Machine Learning Engineering Agent via Search and Targeted Refinement](../../../agent-research/2506.15692-mle-star/README.md) · [原始来源](https://arxiv.org/abs/2506.15692v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 检索模型并实际验证合并，再以消融定位高影响代码块，内层改写/验证、外层重新定位，集成另行搜索。 | 搜索材料与块级训练反馈必须真实执行；不同于MARS按成本奖励调度仓库候选。八V100及小时级完整矩阵不复现，本地无控制器或能力指标。 |
| [AlphaEvolve: A coding agent for scientific and algorithmic discovery](../../../agent-research/2506.13131-alphaevolve/README.md) · [原始来源](https://arxiv.org/abs/2506.13131v1)<br>章节：背景与主要改动、核心公式、论文离线与线上效果、高成本完整实验 | 固定人类评价合同，混合LLM提案、级联执行评价与多维进化档案，异步探索程序空间。 | 指标优化仍受评价器充分性约束，不等于ScientistOne的主张/引用/方法完整性审计。官方只开放构造验证资料，完整搜索/生产矩阵高成本不复现，本地没有算子。 |
| [Co-Director: Agentic Generative Video Storytelling](../../../agent-research/2604.24842-co-director/README.md) · [原始来源](https://arxiv.org/abs/2604.24842)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、复现边界 | 分别更新策略/叙事/美学轴的战略reward，用推荐冷启动和UCB选方向，独立质量分选择已有视频。 | CoDirector用UCB乐观探索尚不确定的创意方向；RuHarness按联合后验效用的低分位保守选择rubric frontier，再让独立validation决定harness是否晋级。探索奖励和准入证据不能互换，也都不把judge关联分当因果效应。 |
| [MULTILOOP: Evolving Multi-Agent Harnesses for Complex Information-Seeking Tasks](../../../agent-research/2611.15754-multiloop/README.md) · [原始来源](https://arxiv.org/abs/2611.15754v1)<br>章节：背景与主要改动、核心公式 | 把既有自动harness优化用于真实多Agent检索，记录完整历史并分析优化后仍未消除的编排失败；不提出新优化器。 | HarnessLens强调受影响行为的配对验证与归因门；MULTILOOP的整体提升多来自提示和工具。总分提高不能单独证明结构协调改善，10训练样例也不代表低API成本。 |
| [Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science](../../../agent-research/2609.15983-stellar-colosseum/README.md) · [原始来源](https://arxiv.org/abs/2609.15983v1)<br>章节：背景与主要改动、核心公式 | 策略readiness门后分解证明依赖，带反驳的重叠树综合与全局验证指导局部修订／重新探索，结果grader与候选选择隔离。 | ScientistTwo控制子集到全量实验和review闭环；Colosseum核查数学假设与跨节论证。共同的多阶段形态不使语义judge或证据充分性可互换。 |
| [AskALCF: A Self-Improving Agentic System for Intelligent HPC User Support](../../../agent-research/2611.15700-askalcf-protocol/README.md) · [原始来源](https://arxiv.org/abs/2611.15700v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 回答盲的生产／全库充分性pivot、独立质量信号、revision缓存与受人审动作控制的修复协议。 | Harness²不依赖答案rubric，按开放执行对照选择并积累经验；AskALCF有冻结专家归因和target/control，不能用文本偏好选择替代充分性探针。局部七路不是原文28规则。 |
| [ProdPilot: A Layered Model Context Protocol System for Automated Production Readiness and Deployment of Vibe-Coded Projects](../../../agent-research/2611.17381-prodpilot-protocol/README.md) · [原始来源](https://arxiv.org/abs/2611.17381v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 按修复类型分层，真实checker接受修改、全量审计回滚回归，再按规则和概率顺序门控；本地仅文件映射回调。 | ProdPilot依特定生产规则，Harness²比较开放任务行为且无gold rubric。规则通过不等于通用安全；handle返回不是smoke成功，外部调用异常还需记未知副作用。 |
| [DetourBench: Trajectory-Level Evaluation of Interactive Agents with Exact Minimum-Action Bounds](../../../agent-research/2611.20844-detourbench/README.md) · [原始来源](https://arxiv.org/abs/2611.20844v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 只看最终成功会把最短路线、绕路成功和接近完成的失败混成同一结果。DetourBench把环境限制为有限、确定、部分可观察的资源／凭证状态机，资源标识发现后全局可寻址，没有当前位置或回退路费。离线评测器知道全图，用BFS给出最少收费访问数和可回放见证；这不是部分可观察条件下的最优策略。 | 负控覆盖重复／无效都收费、batch终态截断、部分进展、不可逆失败的null指标与状态上限。三seed是同一确定性边界测试的重复，不是三次独立能力实验。与Harness²相比，这里有全信息exact evaluator；Harness²是无rubric的执行对照改进，不能把其选择器当最短路oracle。 |
| [SciResearch-Eval: Evaluating Scientific Judgment in Autonomous Experimental Agents](../../../agent-research/2611.21541-sciresearch-eval/README.md) · [原始来源](https://arxiv.org/abs/2611.21541v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | Agent需要给未知材料设计加热实验，用可能粗糙或缺物理项的热传导模拟器估计物性，再报告95%区间与隐藏实验的预测。拟合残差小不代表模型正确：错误物理可给出看似精确但偏置的参数。环境让“真实样品”由更丰富模拟器生成，评测器有精确truth，Agent只得到工具、初始测量和预算。 | 负控验证过窄错误区间代价、区间加宽不免费、单位倍数变换不改log区间评分，以及非正值／NaN／漏参数拒绝。AskALCF用回答盲的两范围证据定位检索责任；本篇用独立物理truth评分置信区间。二者都要求评测参考不能进入被评Agent，但不能互换judgment。 |
| [Invariant-Aware Harness Enforcement to Protect LLM Agents from Silent API Failures](../../../agent-research/2611.20595-silentguard/README.md) · [原始来源](https://arxiv.org/abs/2611.20595v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | API返回HTTP200并不保证按请求过滤，静默忽略字段、把AND变OR或截断total都可能让Agent相信错误数据。SilentGuard把检查从提示中的建议移到执行harness：结果过确定性不变量才放行，失败真实重试一次，仍失败时按检查可信度隐藏值或警告，不自动生成“修复值”。 | 负控包含一致谎言确实放行、97/98个clean样本的阈值边界、documented参数拒绝、原API error透传、宽松count不能背书严格请求，以及两次拒绝后弃答。与Harness²改进执行策略不同，这里只限制结果能否被使用；判定“可验证”不等于开放任务能力。 |
| [MetaAct: Self-Evolving Executable Action Constraints for Embodied Language Agents](../../../agent-research/2611.20655-metaact/README.md) · [原始来源](https://arxiv.org/abs/2611.20655v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 自然语言教训改变偏好，却不能保证不可逆动作不执行。MetaAct让LLM输出类型化GEAR规格，由固定编译器转成确定性guard；运行时拒绝违反约束的动作并返触发消息，模型需要重新规划。保证只覆盖规格表达的局部规则，不是全任务安全证明。 | 合成日志验证观察变化后动作恢复可用、已生效选项被拦、有效动作误拦和成功轨迹误拦会拒绝、缺正负参考时不打虚假零率。成功和score标签只供离线evaluator，guard只能见动作前View。与Harness²基于开放执行对照组合不同，这里选择有明确作用域的可执行约束，回放通过并不证明真实环境收益。 |
| [Evaluation-Free Recursive Self-Improvement for Coding Agents](../../../agent-research/2611.21056-elite-eval-free/README.md) · [原始来源](https://arxiv.org/abs/2611.21056v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | ELITE质疑反复在固定下游任务上evaluate-and-select的成本与适应偏差。冻结模型，演化可执行scaffold代码：同一parent先给出多个聚焦改进假设，每条假设独立实现，经过确定性有效性检查后交给LLM integrator。它不是从得分最高子代里挑一个。 | 负控验证两次explorer确实看到相同parent、integrator收到独立子代、严格范围拒绝、acceptance失败回滚和无效gate不被truthiness放行。与Harness²相比，两者都不依赖任务rubric，但Harness²按任务执行对照改框架，ELITE刻意不看下游执行结局，不能把普通validation elitism写成ELITE。 |
| [The Resolution Hypothesis: Agent Evolution&#x27;s Key Is Identifying Improvements](../../../agent-research/2611.23068-resolution-hypothesis/README.md) · [原始来源](https://arxiv.org/abs/2611.23068v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 自进化停滞不一定是提案不够好，可能是一次嘈杂评分分不清候选改进。本文把“同一artifact反复测”的评测噪声与“不同演化run产出不同artifact”的真实质量波动分开。固定artifact的对照只受前者限制，方法排名同时受两者限制。 | 负控用相同行的嘈杂数据得到负tau²、无行内噪声但均值不同得到正tau²，并检验整体平移不改变方差、ragged/NaN/bool拒绝。Harness²的执行对照也会有随机性；本估计器只是诊断测量分辨率，不把其输出直接变成自动晋级门。 |
| [SkillBuffBench: Measuring What Agent Skills Contribute across Harnesses, Models, Skill Access Modes and Memory](../../../agent-research/2611.22017-skillbuffbench/README.md) · [原始来源](https://arxiv.org/abs/2611.22017v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 手工给Agent正确skill测的是精选上界，不等于部署时能从库里找到它。SkillBuffBench在同一任务／模型／harness下交叉三种skill访问（无、精选、自动）与两种memory模式，单独测内容收益、发现损失和记忆交互。模型池和harness版本应固定到每次结果，不能把更新后版本混进同一格。 | Harness²会产生与改进执行框架；SkillBuffBench评估框架、模型、skill access和memory条件的配对差异。让改进过程看测试任务的verifier会同时改变二者的信息边界。精选skill不应被写成自动发现能力。 |
| [Verifying Agents in Rubric-Graded Environments](../../../agent-research/2611.22841-gandalf-bvb/README.md) · [原始来源](https://arxiv.org/abs/2611.22841v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 复杂任务产物可能是Excel、PowerPoint或应用状态，单纯把文件转成文本会丢公式、布局与跨文件关系。本文不是新做任务的Agent，而是研究判断Agent产物的verifier：BVB包含24投资银行任务、2464个人工判定criteria，用来评测验证器的判断。 | AskALCF把回答质量与检索充分性分开归因，Gandalf检查已完成工作是否满足rubric；二者都依赖独立证据但不能互换。judge拥有的固定workspace和文件权限不能泄漏给actor作为gold，judge也不能有写权限。完整API／多任务评测成本过高，不复现（审查DONE）。 |
| [Do LLM Agents Still Need to Be Told How to Self-Improve?](../../../agent-research/2611.23219-self-organized-learning/README.md) · [原始来源](https://arxiv.org/abs/2611.23219v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 本文不先指定GEPA式优化循环，而是给冻结teacher通用自改进目标、文件读写／Bash／gameplay原语与资源预算。teacher可自己造游戏、观察短生命周期player、编辑文本产物，自行决定何时探索、比较和更新。真实游戏与外部benchmark不在teacher训练访问范围。 | ELITE预设explore-then-integrate程序且不读下游任务结果，本篇刻意不给外部优化loop、让teacher自行选择学习动作；Harness²又有预定义Propose–Probe–Compose。固定脚手架协议可支持研究，但不等于复现自发学习能力。完整多模型多benchmark长rollout成本过高，不复现（审查DONE）。 |
| [Agentic Harness Engineering Beta: Requirement-Centered Evolution of Agent Harnesses](../../../agent-research/2611.24924-ahe-beta/README.md) · [原始来源](https://arxiv.org/abs/2611.24924v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | AHE-Beta把演进的依据从测试分数移到经过核实的用户需求。模拟用户进行多轮交互并提交问题；Triage把问题核实成可泛化需求，Architect按共同根因合并至少两个需求，PM从跨会话记录找隐含产品需求。开发者只接收被准入的需求及其证据包。 | Harness²按执行对照提出、组合并积累经验，且不使用rubric；AHE-Beta把跨会话需求、证据准入和head绑定审查作为演进主干。两者都不能由本地固定角色替身的通过数证明泛化能力。 |
| [Safe Personal RSI: Evaluating and Repairing Personal-Agent Updates](../../../agent-research/2611.23651-safe-personal-rsi/README.md) · [原始来源](https://arxiv.org/abs/2611.23651v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 个人Agent的prompt更新可能提升主动性，却同时改变隐私披露、承诺和执行报告。论文固定模型和runtime，只改指令；先比较候选与父版本寻找反例，再重复确认、回滚定位和修复。修复局部验证后仍须完整admission；没有通过版本就继续用父版本。 | Harness²用执行差异优化harness，不要求rubric；Safe Personal RSI对prompt候选显式比较安全/效用并保留父版本。后者有领域风险标签但仍不是安全证明；不能把前者匿名产物选择当后者admission。 |
| [RSIBench-Infra: Can Agents Optimize Their Own Training and Inference Infrastructure at Production Scale?](../../../agent-research/2611.24395-rsibench-infra/README.md) · [原始来源](https://arxiv.org/abs/2611.24395v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 单算子快不代表端到端训练或服务变快。RSIBench-Infra让Agent从官方可运行baseline出发，跨engine、kernel、instruction修改，但只提交一个OCI filesystem layer。独立Serve/Train Job把同一digest应用到每个rank；Benchmark Job绝不加载候选层，单独做质量门和端到端计时。 | Harness²改模型外执行框架并以任务执行对照积累经验；RSIBench-Infra评价跨栈训练/推理优化，以独立质量门约束端到端加速。优化harness通过数和已验证吞吐收益不是同一个结果，前者不能代替后者硬件链路。 |
| [SearchInject: Retrieval Exposure Control for Indirect Prompt Injection in Language-Model Search](../../../agent-research/2611.02643-searchinject/README.md) · [原始来源](https://arxiv.org/abs/2611.02643v1)<br>章节：背景与主要改动、核心公式、同主题对照 | 间接注入先要进入上下文才有机会影响LLM。SearchInject在原top100候选中，用相关性、abuse、instruction概率及两项相关性交互做logistic风险评分；超过冻结阈值才隔离，按原顺序从同一候选池补足top10。它控制暴露，而不是验证下游攻击成功。Google官方目录今天新增，但论文首发11月2日，按历史发现补录，不算今天新论文。 | SilentGuard核对工具返回值是否满足请求不变量；SearchInject在第三方文本进入上下文之前做风险准入。前者检查语义执行合同，后者检查检索暴露，HTTP200或低暴露率都不能证明最终回答安全。 |
| [BuggyMLE: Scaling Machine Learning Engineering Difficulty with Bug Injection](../../../agent-research/2611.25088-buggymle-cci/README.md) · [原始来源](https://arxiv.org/abs/2611.25088v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | BuggyMLE先审核可运行、指标稳定且对代码变化敏感的ML仓库，再让Injector注入不同规模的错误。Oracle通过逐个恢复变动找最小恢复集合，再把每个改动单独应用到干净仓库，筛出确有独立指标影响的错误。Solver必须在多文件仓库里真实修复；评价同时检查执行、指标恢复和逐错误语义修复，不能把补偿性调参当修好了全部bug。 | MLE-STAR用检索、真实消融与validation结果定位并改进模型代码；BuggyMLE用有Oracle归因的注入错误构建难度阶梯，CCI是评测/课程设计尺度。前者选改进方案，后者塑造训练与评测任务；不能把后者的结构分数当成前者的真实验证收益。 |

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

### 策略能入库，不代表它能成为当前冠军

Strategist把可执行推理结构、测量卡与训练轨迹经验组成跨任务资产，和Reflexion只留下可读教训不同；它可保留测过但未获胜的结构，给未来任务组合机会。当前交付选择则另设validation和hidden双门槛，且test不参与。EvalAlloc治理花在哪些评测cell上的成本，而不代替提出策略。三者都依赖真实执行反馈，但经验积累、结构复用与预算分配是不同机制；合成分数通过任何选择规则，都不提供LLM能力证据。

对照来源：[strategist](../../../agent-research/2611.03618-strategist/README.md) · [reflexion](../../../agent-research/2303.11366-reflexion/README.md) · [evalalloc](../../../agent-research/2610.37276-evalalloc/README.md)

### 编辑生命周期、经验持久性和模型内化不是同一条演化轴

Strategist将可执行推理程序与测量经验放入跨任务库；Meta²则把跨任务保留对象限制为冻结的演化知识，避免把某个任务修复永久带到另一任务。Continual AutoResearch进一步要求把首解、搜索曲线与最终选择分别评估：更快找到0.8候选但最终选择0.5，不能写成最终提升。RSI-Dojo改变的又是模型权重学习阶段，不能把阈值过滤器或未执行环境注册视为训练完成。比较前应先固定跨任务可见状态、编辑的生效范围以及验证反馈何时可见。

对照来源：[strategist](../../../agent-research/2611.03618-strategist/README.md) · [meta-square](../../../agent-research/2611.05139-meta-square/README.md) · [continual-autoresearch](../../../agent-research/2611.05108-continual-autoresearch/README.md) · [rsi-dojo](../../../agent-research/2611.03698-rsi-dojo/README.md)

### 跨任务保留环境、演化指导与会话经验是三种干预

EnvOpt 保留能服务不同查询的环境表示，内层成本下降且代理保真才接受，验证回归即停止并回滚；Meta² 保留冻结 Meta-Skill，具体 Harness 编辑只作用于当前 run；Continual AutoResearch 固定任务流比较会话/工作区状态，独立测量搜索速度与最终选择。应分别记录变更产物的生效范围、外层验证可见性和跨任务继承对象，不能因搜索轨迹更省就推断模型能力提高。

对照来源：[envopt](../../../agent-research/2611.07372-envopt/README.md) · [meta-square](../../../agent-research/2611.05139-meta-square/README.md) · [continual-autoresearch](../../../agent-research/2611.05108-continual-autoresearch/README.md)

### 平均验证增益、边界风险与形式规范是不同准入依据

PASE将技能程序patch交给独立validation，以严格改善决定保留；FGSE另外要求证伪失败与旧任务损伤不超阈值，避免平均收益掩盖危险子范围。Verified Quantum Wiki先依冻结规范独立证明，再比较成本/大小。三者都在准入，但可获得的保证不同：AST语法、经验探针和形式定理不能互换。当前CPU组件都不生成候选或外部核验，测试分数和synthetic receipt只用于合同负控。

对照来源：[pase](../../../agent-research/2611.14019-pase/README.md) · [fgse](../../../agent-research/2611.14326-fgse/README.md) · [verified-quantum-wiki](../../../agent-research/2611.09822-verified-quantum-wiki/README.md)

### 改输出的例外规则与改程序的技能补丁，准入证据不同

PASE在skill/program配对上提出程序补丁，依held-out validation严格改善接受；Agent Gym在原Agent外层保存可逆业务例外，target/collateral检查之后仍需要专家明确批准。程序语法、规则匹配、人工授权和任务效果是四种不同判断，不应互相冒充。本地两者都是准入/事务L1核，不是自动发明规则、模型变聪明或完整RSI。

对照来源：[agent-gym](../../../agent-research/2608.15591-agent-gym/README.md) · [pase](../../../agent-research/2611.14019-pase/README.md)

### 有界研究扩展与证据完整性必须分开验收

ScientistTwo用子集到全量的升阶门、成功/失败历史、未试种子探索、严格改善接纳和review预算组织研究。ScientistOne的CoE则针对分数复算、引文、规则及方法代码一致性，现有局部核也明确把语义判断外置。即使阶段全部accept、评审评分很高，外部日志仍可能错误或不真实；反过来，证据可复算也不能证明科研想法新颖或优越。局部状态测试只证明预算和数据流，不是107任务能力复现。

对照来源：[scientist-two](../../../agent-research/2609.19644-scientist-two/README.md) · [scientist-one](../../../agent-research/2605.26340-scientist-one/README.md)

### 改Agent的执行层与改环境的练习层不能混为一个消融

Harness²在同模型同环境下比较工具、提示、记忆和脚本变更，再积累如何改进的证据；EnvHarness则让环境对特定弱点提供更好的练习，但保留基础目标判据。若两边同时改变，很难把能力收益归因到任一层。串行Chain的A∧B只是原判据组合，不证明任务语义兼容；Contract阻止捷径也不证明策略学到可迁移技能。完整EnvRigger要用freshrollout验收并回到未包装任务评测，本地未完成这条能力链。

对照来源：[envharness](../../../agent-research/2608.19880-envharness/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 寻找值得改的部件，与决定把预算花在哪个分支，是不同控制问题

MLE-STAR用执行消融选择代码块，在相对固定的局部空间内反复提出计划；MARS则通过预算感知MCTS安排模块化候选，并把新旧代码与运行差异变成跨分支经验。局部影响与性能/时间折中可以互补，却不是同一个分数；高耗时竞赛上的原文结果也不能拿来给本地空控制器背书。两者收录都应明确生成脚本、完整编排器与已运行能力三种不同资产。

对照来源：[mle-star](../../../agent-research/2506.15692-mle-star/README.md) · [mars-research](../../../agent-research/2602.02660-mars-research/README.md)

### 发现更好的对象，与证明对它的研究主张有证据，是不同验收层

AlphaEvolve需要一个能实际评价候选程序的目标，靠程序库和模型提案产生改进；ScientistOne继续追问论文数字是否复算、引文是否存在并支持主张、方法文字是否对应代码。构造通过指定检查只支持那项性质，不能把生成的论文全部自动判真；证据链可靠也不能保证搜索有创新。官方结果notebook可验证已给出的对象，但不恢复原发现过程，本库因此只收录有据成本审查。

对照来源：[alphaevolve](../../../agent-research/2506.13131-alphaevolve/README.md) · [scientist-one](../../../agent-research/2605.26340-scientist-one/README.md)

### 乐观探索不等于保守准入：两种不确定性用途

CoDirector在3/3/4个创意轴上用战略reward均值加UCB探索项分配下一次尝试，官方warmstart只推荐先试未观察arm，不虚构计数。RuHarness从六格联合Dirichlet后验抽2000次，取效用0.2分位保守选择active rubric，候选harness仍须独立validation严格增益超过0.05才晋级。前者的不确定性鼓励探索，后者抑制小样本虚高；不能用UCB高分替代验证改善。CoDirector最终成片还按独立质量分而非战略分之和选取。本地只核两类数值机制，没有视频生成、语义judge或完整自进化能力证据。

对照来源：[co-director](../../../agent-research/2604.24842-co-director/README.md) · [ruharness](../../../agent-research/2610.36826-ruharness/README.md)

### 优化有收益不等于编排改动获得了因果证明

MULTILOOP让编码优化器读轨迹改harness，但实证指出关键编排故障继续存在。HarnessLens将验收收窄到相关行为任务并要求配对可归因证据。两者提醒我们分清搜索发现、候选验收和机制解释；若完整模型／工具缺席，简单循环只能说明控制流，不能重建原文收益。

对照来源：[multiloop](../../../agent-research/2611.15754-multiloop/README.md) · [harnesslens](../../../agent-research/2608.27311-harnesslens/README.md)

### 科学研究控制器的成功取决于领域证据，而非统一success标签

ScientistTwo的升阶、消融与严格比较针对可执行实验；Colosseum的readiness、局部复核和全局反驳针对长证明。未发现反例不等于证明正确，模拟评审高分也不等于会议录用。二者完整系统依赖高成本外部语义研究；本地通用tree或callback不会自动继承这种能力。

对照来源：[stellar-colosseum](../../../agent-research/2609.15983-stellar-colosseum/README.md) · [scientist-two](../../../agent-research/2609.19644-scientist-two/README.md)

### 执行差异是证据，但不自动告诉你该修哪一层

Harness²先提出并真实执行不同harness，再组合和反思；AskALCF先区分生产检索与全库知识是否充分，才把错误交给对应组件。两者都不能用成功计数代替真实动作。AskALCF的after必须与冷缓存null比较，并记录逐题翻转；人审ship/revert/decline不由judge自信度授权。

对照来源：[askalcf-protocol](../../../agent-research/2611.15700-askalcf-protocol/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 从可执行修改到可信交付，需要独立验收和失败语义

Harness²保留真实候选执行与采用依据，不把“提案”当“执行”。ProdPilot在结构化修复域进一步把每个fix的接受交给原checker，回归即回滚，关键P0不能被高模型概率覆盖。局部回调能验证这些控制流，但没有50条规则、概率模型或实际云环境，因此不能宣称应用已生产就绪。

对照来源：[prodpilot-protocol](../../../agent-research/2611.17381-prodpilot-protocol/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### DetourBench：把成功、绕路和不可逆失败分开

每次真正送达dispatcher的访问都收费，包括无效、禁用和重复动作；不产生访问的模型回复不收费，另有turn上限。batch按顺序执行，达到终态或固定预算便停止。活跃状态下资源与凭证只增不减，错误承诺是吸收终态，不给它编造一个有限剩余距离。成功率必须与条件attainment一起报告，不能用只在成功子集上定义的效率排整个模型名次。 负控覆盖重复／无效都收费、batch终态截断、部分进展、不可逆失败的null指标与状态上限。三seed是同一确定性边界测试的重复，不是三次独立能力实验。与Harness²相比，这里有全信息exact evaluator；Harness²是无rubric的执行对照改进，不能把其选择器当最短路oracle。

对照来源：[detourbench](../../../agent-research/2611.20844-detourbench/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### SciResearch-Eval：用正确区间评分检验科学判断

物性区间在log10尺度上使用proper interval score：区间越宽承担宽度代价，错过truth另以40倍距离处罚。隐藏温度预测另按传感噪声sigma及真实温升归一化，不能和物性log评分混成一个accuracy。无提交单独保存，论文覆盖率把它算miss；不能只统计按时提交的成功子集。 负控验证过窄错误区间代价、区间加宽不免费、单位倍数变换不改log区间评分，以及非正值／NaN／漏参数拒绝。AskALCF用回答盲的两范围证据定位检索责任；本篇用独立物理truth评分置信区间。二者都要求评测参考不能进入被评Agent，但不能互换judgment。

对照来源：[sciresearch-eval](../../../agent-research/2611.21541-sciresearch-eval/README.md) · [askalcf-protocol](../../../agent-research/2611.15700-askalcf-protocol/README.md)

### SilentGuard：把API一致性检查变成强制执行门

计数查询对每个条件i执行N(F)+N(F不含i且非Ci)=N(F不含i)，每次最多2k额外API查询。文档外参数可在执行前拒绝。精确检查误报估计0；learned contract从n条clean样本估1/(n+2)，不大于1%才强制隐藏。最终count必须来自足够严格且已通过检查的查询，否则拒绝最多两次再弃答。 负控包含一致谎言确实放行、97/98个clean样本的阈值边界、documented参数拒绝、原API error透传、宽松count不能背书严格请求，以及两次拒绝后弃答。与Harness²改进执行策略不同，这里只限制结果能否被使用；判定“可验证”不等于开放任务能力。

对照来源：[silentguard](../../../agent-research/2611.20595-silentguard/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### MetaAct：类型化动作约束与离线回放验证

v1提出ordered_once、no_op_repeat、idempotence_block、revisit_block、generic_deref、relevance_filter六类primitive及固定extractor菜单。候选用训练日志反事实回放，要求失败轨迹覆盖至少0.3、有效动作误拦不高于0.15、成功轨迹被拦不高于0.10。有效动作分母来自成功及高分失败的安全参考，不把本来无效的重复动作充成误拦。 合成日志验证观察变化后动作恢复可用、已生效选项被拦、有效动作误拦和成功轨迹误拦会拒绝、缺正负参考时不打虚假零率。成功和score标签只供离线evaluator，guard只能见动作前View。与Harness²基于开放执行对照组合不同，这里选择有明确作用域的可执行约束，回放通过并不证明真实环境收益。

对照来源：[metaact](../../../agent-research/2611.20655-metaact/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### ELITE：同父探索后按实现证据整合，不做任务分数选择

integrator查看实现、hypothesis与gate结果，推理互补、冗余、冲突、复杂度或缺失，再对原parent重新实现一个组合patch。不能简单拼接所有patch，也不能把已串联修改的子代当共同起点。compile/import/tool-load/scope等exploration gate与更严格call-return/message-order/main-flow acceptance gate只验证操作有效性；下游解题轨迹和benchmark结果都不进入演化。 负控验证两次explorer确实看到相同parent、integrator收到独立子代、严格范围拒绝、acceptance失败回滚和无效gate不被truthiness放行。与Harness²相比，两者都不依赖任务rubric，但Harness²按任务执行对照改框架，ELITE刻意不看下游执行结局，不能把普通validation elitism写成ELITE。

对照来源：[elite-eval-free](../../../agent-research/2611.21056-elite-eval-free/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### Resolution Hypothesis：区分评测噪声与演化run方差

在R个独立artifact、每个M次重复评测的平衡矩阵中，sigma²用每行sample variance再平均，tau²用行均值sample variance减sigma²/M。tau²的无偏矩估计可以为负；不能删掉负结果，论文只在显示标准差时截成0。把所有RM项拉平会破坏层级，不能用更多同artifact重复代替更多独立演化run。 负控用相同行的嘈杂数据得到负tau²、无行内噪声但均值不同得到正tau²，并检验整体平移不改变方差、ragged/NaN/bool拒绝。Harness²的执行对照也会有随机性；本估计器只是诊断测量分辨率，不把其输出直接变成自动晋级门。

对照来源：[resolution-hypothesis](../../../agent-research/2611.23068-resolution-hypothesis/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### SkillBuffBench：把精选技能、自动发现与记忆分开评测

M0每轮新workspace、session和memory namespace，缓存／历史不跨轮；只有API凭据可复用。任务prompt不点名skill，golden值、reference solution和verifier不给Agent。网络默认只开模型API，必要外部工具逐任务allowlist；私有技能正文不能靠摘要重写成声称同等的benchmark。 Harness²会产生与改进执行框架；SkillBuffBench评估框架、模型、skill access和memory条件的配对差异。让改进过程看测试任务的verifier会同时改变二者的信息边界。精选skill不应被写成自动发现能力。

对照来源：[skillbuffbench](../../../agent-research/2611.22017-skillbuffbench/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### Gandalf / BVB：检验rubric验证器本身是否可靠

Gandalf把rubric转成reactive检查任务，自行决定读什么原生文件／工具，直到得出布尔verdict；环境对齐让judge使用只读固定快照工具，domain guidance给全语料通用银行惯例，不含任务答案。mutation权限不交给judge，不能让评测器修好产物后再判它通过。 AskALCF把回答质量与检索充分性分开归因，Gandalf检查已完成工作是否满足rubric；二者都依赖独立证据但不能互换。judge拥有的固定workspace和文件权限不能泄漏给actor作为gold，judge也不能有写权限。完整API／多任务评测成本过高，不复现（审查DONE）。

对照来源：[gandalf-bvb](../../../agent-research/2611.22841-gandalf-bvb/README.md) · [askalcf-protocol](../../../agent-research/2611.15700-askalcf-protocol/README.md)

### Self-Organized Learning：只给原语，观察Agent如何设计自学过程

teacher在持久session内组织算法，player每次新session只读取当前文本产物；权重不变。论文分析自发课程、难度选择和A/B测试行为，并在不同游戏horizon／机制／3D导航上检验迁移。teacher看到自己生成任务的结果不等于能看最终外部测试标签。 ELITE预设explore-then-integrate程序且不读下游任务结果，本篇刻意不给外部优化loop、让teacher自行选择学习动作；Harness²又有预定义Propose–Probe–Compose。固定脚手架协议可支持研究，但不等于复现自发学习能力。完整多模型多benchmark长rollout成本过高，不复现（审查DONE）。

对照来源：[self-organized-learning](../../../agent-research/2611.23219-self-organized-learning/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### AHE-Beta：让需求证据而非基准分数决定Harness演进

证据包只有被引用会话的运行日志、公开任务和执行条件，用户对话、隐藏测试和grader不能传给开发者。RFC先做设计审查，代码再按验收标准审查；合并时批准必须绑定当前PR head，且RFC仍与已审设计一致。这里的“verified”是上游角色判断，不是形式正确性证明。测试确认未核实的合并需求不能吞掉原需求；原始issue不能作为交付类型；证据为空、head过期、RFC变动或全套测试未完成均不能通过。无benchmark score、gold或隐藏test参数，但不提供恶意回调沙箱。

对照来源：[ahe-beta](../../../agent-research/2611.24924-ahe-beta/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### Safe Personal RSI：修复通过不等于更新可准入

Appendix I以所有开发重放（含control）为分母，取五个primary风险类别的最大率。确认过的未授权披露case产生持久严重性veto，即使后来修复也拒该attempt；否则父/工作版本各至少5条且全部执行完成，最大风险不超过0.10且不高于父版本。效用不降，或成功率最多绝对下降0.02且成本proxy绝对减少至少0.10，才可准入。RQ1模板确认可接受非空截断多数；RQ2要求三次候选确认完整，差分还要三次父重放。测试保留论文限制：最大风险不变时次大类别风险仍可升高；不偷偷把规则增强为总风险比较。缺5条、未完成、严重veto、风险上升或效用/成本均不达标分别拒绝。阈值是点估计与工程常数，不提供置信界或总体安全概率。

对照来源：[safe-personal-rsi](../../../agent-research/2611.23651-safe-personal-rsi/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### RSIBench-Infra：把生产级基础设施优化与独立质量验证分开

任务定义含模型、环境、资源和独立verifier。16推理+4训练任务覆盖1–32个加速器、最多4节点；推理模型1.7B–2.8T。训练固定输入，比较逐步loss和全局梯度范数；VLM GRPO还检查policy/KL loss、forward及隔离KL梯度。性能得分只有通过任务质量门才有效，microbenchmark不能替代端到端计时。审查明确隔离Agent环境、Serve/Train环境和Benchmark环境，比较部署digest与质量门，而不是伪造本地通过指标。没有运行正式任务、提交OCI、训练或测试模型；所以没有CPU/GPU能力分数，也不要求GPU回执。

对照来源：[rsibench-infra](../../../agent-research/2611.24395-rsibench-infra/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### SearchInject：检索风险与干净误隔离预算：机制和证据边界

§III-C/D：joint模型为class-balanced logistic regression，不能把输出当校准概率。阈值只在calibration集选并冻结；文档重复出现在不同query时按placement计数。原稿未发布abuse/字符与词n-gram词表、IDF、scaler或拟合系数，因此本地明确接收外部特征/系数，只实现score、约束选阈与有序refill，不用关键词规则假装原检测器。 SilentGuard核对工具返回值是否满足请求不变量；SearchInject在第三方文本进入上下文之前做风险准入。前者检查语义执行合同，后者检查检索暴露，HTTP200或低暴露率都不能证明最终回答安全。

对照来源：[searchinject](../../../agent-research/2611.02643-searchinject/README.md) · [silentguard](../../../agent-research/2611.20595-silentguard/README.md)

### BuggyMLE：用代码复杂度分层，而不是把指标恢复当完整修复

CCI在八个参考benchmark上，先取十项结构特征的任务中位数，做log1p和特征z-score，再对repo、dependency、patch三组求均值，并把组分数按参考方差缩放。固定logistic系数的负加权和构成raw CCI，再用参考最小/最大值定标。新任务不能重新拟合或裁剪回[0,1]。Figure10的repo系数为+0.64，dependency为-0.34，patch为-0.99；repo项是给定其他项的条件调整，不支持“仓库越大必然越难”。负控保留正repo系数、组方差缩放和参考区间外结果；验证median不是mean，未给截距时不捏造预测成功率。拒绝NaN、零尺度和退化边界。Table4把total_lines_delta写成净变化，若值≤-1会使log1p无定义，接口明确拒绝，既不取绝对值，也不补造作者未说明的变换。

对照来源：[buggymle-cci](../../../agent-research/2611.25088-buggymle-cci/README.md) · [mle-star](../../../agent-research/2506.15692-mle-star/README.md)

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

### Strategist把失败策略也入库，与Reflexion记录教训、EvalAlloc确认冠军，有哪些不同？ {#cross-blueprint-archive-versus-current-pick}

??? note "展开答案与例子"

    **答案：** 入库保存可执行结构与实测卡，不自动采用为当前答案流程；最终仍要两split都胜出。Reflexion主要保存下次可读的文字经验，EvalAlloc决定观测预算与最终确认，不替系统生成结构。结构档案、经验内容和获准采用的策略必须分别记录。

    **教学例子：** 教学例：某次投票策略不划算仍可作为未来分解程序的组件，但不能因已入库就覆盖当前更便宜的基线。

    对照来源：[strategist](../../../agent-research/2611.03618-strategist/README.md) · [reflexion](../../../agent-research/2303.11366-reflexion/README.md) · [evalalloc](../../../agent-research/2610.37276-evalalloc/README.md)

### 预建跨任务文件索引和某次任务失败时追加一个工具提醒，能用同一张训练收益表吗？ {#cross-environment-index-versus-in-run-edit}

??? note "展开答案与例子"

    **答案：** 不能直接合并。EnvOpt 的索引改变任务共享的环境表示，要在未用于该轮提出改动的验证任务上看成本和效果；Meta² 的提醒是当前 run 的有界 Harness 编辑，跨任务保留的是指导如何演进的知识，不是同一个提醒。

    **教学例子：** 教学例：搜索任务都可复用同一目录索引；只针对一次缺失权限发出的恢复提醒不应永久植入其他任务。

    对照来源：[envopt](../../../agent-research/2611.07372-envopt/README.md) · [meta-square](../../../agent-research/2611.05139-meta-square/README.md) · [continual-autoresearch](../../../agent-research/2611.05108-continual-autoresearch/README.md)

### 一个patch提高验证均分，同时破坏旧案例，它能同时通过PASE、FGSE和Verified Quantum Wiki吗？ {#cross-risk-gates-versus-validation}

??? note "展开答案与例子"

    **答案：** 不能据这两个数字统一判断。PASE的明确规则看held-out validation严格改善；FGSE还看单独归档损伤和证伪风险，可能拒绝。Verified Quantum Wiki另需规范绑定的独立证明及资源改进，不接受均分代替定理。选择哪种门必须匹配可观测证据和更新范围。

    **教学例子：** 教学例：九题改进掩盖一次重复付款，均分门可能通过而风险门拒绝；量子wiki则根本不以这类任务均分为准入条件。

    对照来源：[pase](../../../agent-research/2611.14019-pase/README.md) · [fgse](../../../agent-research/2611.14326-fgse/README.md) · [verified-quantum-wiki](../../../agent-research/2611.09822-verified-quantum-wiki/README.md)

### 一条业务纠错规则经SME批准，与一个程序补丁validation提高，能相互替代吗？ {#cross-cross-rule-governance-versus-program-validation}

??? note "展开答案与例子"

    **答案：** 不能。前者是在目标与collateral范围内授权下游例外；后者是配对程序在隔离validation上的测得效果。二者作用位置和接受依据不同，均不能靠语法/类型检查证明语义成功。

    **教学例子：** 教学例：紧急采购例外可获人工授权；表格公式修补则要validation严格提高。把专家批准标成benchmark提升，或用一次分数提高授权采购政策，都混淆证据。

    对照来源：[agent-gym](../../../agent-research/2608.15591-agent-gym/README.md) · [pase](../../../agent-research/2611.14019-pase/README.md)

### ScientistTwo完成严格改善比较与两轮review后，能否跳过ScientistOne式证据审计？ {#cross-cross-scientist-control-versus-evidence-integrity}

??? note "展开答案与例子"

    **答案：** 不能。严格比较与review本身由外部模型或人作出，控制核只保证何时调用、何时更新和何时停止。独立分数复算、数据隔离、日志来源与方法代码一致性仍需核查；高分不是来源真实性证明。

    **教学例子：** 教学例：外部比较器根据复制来的高分返回true，控制核会忠实更新best，但只有执行与来源审计才能发现这个高分不属于当前代码。

    对照来源：[scientist-two](../../../agent-research/2609.19644-scientist-two/README.md) · [scientist-one](../../../agent-research/2605.26340-scientist-one/README.md)

### 同时替换Agent harness和环境Contract，再见到成功率上涨，能归因到EnvHarness吗？ {#cross-cross-environment-and-agent-harness-attribution}

??? note "展开答案与例子"

    **答案：** 不能。需固定策略、任务划分和Agent执行层，再比较原环境与包装环境产生的训练/技能，并在未包装评测环境验收。固定toy包装器检查不覆盖学习与迁移，更不是两套系统已集成。

    **教学例子：** 教学例：同时增加测试工具并禁止直接提交，失败减少可能来自任一改动；没有分开对照就无法识别机制贡献。

    对照来源：[envharness](../../../agent-research/2608.19880-envharness/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 一处修改影响很大但训练昂贵，MLE-STAR的消融定位与MARS的预算奖励会作同一个决定吗？ {#cross-cross-block-targeting-versus-budget-allocation}

??? note "展开答案与例子"

    **答案：** 不一定。消融回答哪个部件值得深入，预算奖励还按性能与执行时间取舍候选。前者不自动包含MARS的时间惩罚，后者也不自动实现MLE-STAR的块内计划搜索；应分别固定真实validation和运行成本再组合。

    **教学例子：** 教学例：缺失值处理每次提高0.01却需一小时，另一路提高0.008只要一分钟。影响排序与预算内的探索价值可以不同，不能只看一列精度。

    对照来源：[mle-star](../../../agent-research/2506.15692-mle-star/README.md) · [mars-research](../../../agent-research/2602.02660-mars-research/README.md)

### 一个已发表矩阵构造通过验证，为何仍不能说本地AlphaEvolve和科研完整性都已验证？ {#cross-cross-discovery-score-versus-claim-grounding}

??? note "展开答案与例子"

    **答案：** 构造检查没有执行提案、进化档案和分布式搜索，所以不验证发现能力；它也不检查论文所有数值、引用或方法描述，所以不替代CoE审计。每项证据只支持它实际检查的对象。

    **教学例子：** 教学例：rank-48复数构造通过验证，却不能支持“任意域rank-48”或“本地重新发现”两个更强主张；后两者需要各自额外证据。

    对照来源：[alphaevolve](../../../agent-research/2506.13131-alphaevolve/README.md) · [scientist-one](../../../agent-research/2605.26340-scientist-one/README.md)

### CoDirector的UCB高分与RuHarness的后验低分位，为什么不能作为同一种晋级证据？ {#cross-cross-colm-co-director}

??? note "展开答案与例子"

    **答案：** UCB故意给未充分探索的方向加乐观奖励，服务于下一次尝试；RuHarness用联合后验效用低分位抑制不确定的rubric点估计，并另外要求独立validation严格提升。两者调度对象和风险偏好不同，分轴judge评分也不能识别因果贡献。

    **教学例子：** 教学例：只试一次的新创意可因探索项很高而被再次选择，但一个只解释单次失败的rubric不应据此直接晋级；harness候选还必须跨过validation门槛。这不是实测效果。

    对照来源：[co-director](../../../agent-research/2604.24842-co-director/README.md) · [ruharness](../../../agent-research/2610.36826-ruharness/README.md)

### MULTILOOP总准确率提高，能说明子Agent委派结构已被优化好吗？ {#cross-cross-nov15-multiloop}

??? note "展开答案与例子"

    **答案：** 不能。prompt-only和工具变化可贡献多数收益，编排故障仍持续。要把提升归因到委派结构，需保持其他条件并对相关行为做有据对照。

    **教学例子：** 教学例：新增PDF读取能力提高得分，不等于解决了重复派工。

    对照来源：[multiloop](../../../agent-research/2611.15754-multiloop/README.md) · [harnesslens](../../../agent-research/2608.27311-harnesslens/README.md)

### 用最终参考证明挑选Colosseum候选，可以作为更强的ScientistTwo式评审吗？ {#cross-cross-nov15-stellar-colosseum}

??? note "展开答案与例子"

    **答案：** 不能。参考proof仅供最终benchmark grader；给选择器会把oracle best-of-two上界当真实推理能力。研究评审同样必须守住held-out信息边界。

    **教学例子：** 教学例：先看标准解再挑对的论文，不能称无泄漏自主研究。

    对照来源：[stellar-colosseum](../../../agent-research/2609.15983-stellar-colosseum/README.md) · [scientist-two](../../../agent-research/2609.19644-scientist-two/README.md)

### Harness²的某候选回答更好，足以认定AskALCF需要补知识吗？ {#cross-cross-nov18-askalcf-protocol}

??? note "展开答案与例子"

    **答案：** 不足。更好文本不证明全库缺少权威文档；应看回答盲的R／C。R假C真优先修retrieval，二者假才是knowledge。再以冻结参考和null对照验证候选。

    **教学例子：** 教学例：同一文档已在全库但top-k错过，补一份重复文档可能掩盖检索问题。

    对照来源：[askalcf-protocol](../../../agent-research/2611.15700-askalcf-protocol/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 修复后的规则分数很高，Harness²或ProdPilot就能自动部署吗？ {#cross-cross-nov18-prodpilot-protocol}

??? note "展开答案与例子"

    **答案：** 不能。ProdPilot还需无失败P0、概率门、确定构建和显式批准；Harness²没有同一生产门控保证。部署回调已发出但异常时状态未知，不能直接重试制造重复副作用。

    **教学例子：** 教学例：全局分数93但唯一P0失败仍须闭门；服务创建后超时需查外部状态。

    对照来源：[prodpilot-protocol](../../../agent-research/2611.17381-prodpilot-protocol/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 它与Harness²的执行比较有什么不同？ {#cross-cross-nov18-latest-detourbench}

??? note "展开答案与例子"

    **答案：** DetourBench评价固定轨迹与可证明离线最短路；Harness²通过真实执行对照改harness，选择不依赖gold或rubric。两者评价对象和信息权限不同。

    **教学例子：** 教学例：匿名选产物不能证明该产物花的访问数最少。

    对照来源：[detourbench](../../../agent-research/2611.20844-detourbench/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 它与AskALCF回答盲探针的参考信息一样吗？ {#cross-cross-nov18-latest-sciresearch-eval}

??? note "展开答案与例子"

    **答案：** 不一样。本篇evaluator有精确物理truth，AskALCF充分性探针只看问题和文档，不能看生成答案。参考对象和权限必须分别隔离。

    **教学例子：** 教学例：热物性真值可以供评分器用，但不能传给实验设计Agent。

    对照来源：[sciresearch-eval](../../../agent-research/2611.21541-sciresearch-eval/README.md) · [askalcf-protocol](../../../agent-research/2611.15700-askalcf-protocol/README.md)

### 为什么不把这个当Harness²式自改进？ {#cross-cross-nov18-latest-silentguard}

??? note "展开答案与例子"

    **答案：** SilentGuard按固定不变量执行放行／隐藏，不提出或整合harness改动；Harness²需要执行对照和经验积累。两者可组合但不互相替代。

    **教学例子：** 教学例：重发一次API不是生成一个新的工具策略候选。

    对照来源：[silentguard](../../../agent-research/2611.20595-silentguard/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 与Harness²组合候选相比，GEAR union能直接采用吗？ {#cross-cross-nov18-latest-metaact}

??? note "展开答案与例子"

    **答案：** 不能。GEAR union是guard合取，拦截更多动作也可能误伤成功轨迹，必须重新回放；Harness²也要求实际执行组合结果，证据类型不同。

    **教学例子：** 教学例：两个各自安全的约束合并后仍需算eff和ok。

    对照来源：[metaact](../../../agent-research/2611.20655-metaact/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### ELITE与Harness²都无rubric，差别在哪里？ {#cross-cross-nov18-latest-elite-eval-free}

??? note "展开答案与例子"

    **答案：** Harness²会运行任务并比较行为来组合；ELITE用实现级证据且排除下游任务结果。二者“无rubric”不意味着相同信息边界。

    **教学例子：** 教学例：给ELITE integrator一张候选成功率表已经改变算法。

    对照来源：[elite-eval-free](../../../agent-research/2611.21056-elite-eval-free/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 它能取代Harness²的selector吗？ {#cross-cross-nov18-latest-resolution-hypothesis}

??? note "展开答案与例子"

    **答案：** 不能。它估测量波动，不判断哪条机制互补或哪个产物更符合任务。候选质量、选择能力与分辨率是不同对象。

    **教学例子：** 教学例：低方差的错误答案也不会因为稳定就变正确。

    对照来源：[resolution-hypothesis](../../../agent-research/2611.23068-resolution-hypothesis/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 为什么它不能直接等同Harness²实验？ {#cross-cross-nov18-latest-skillbuffbench}

??? note "展开答案与例子"

    **答案：** 这里固定配置比较skill access与memory条件，Harness²主动修改harness并积累经验。演化产物与评测条件必须分开。

    **教学例子：** 教学例：自动安装新skill会改变一个原定固定的benchmark格子。

    对照来源：[skillbuffbench](../../../agent-research/2611.22017-skillbuffbench/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 它与AskALCF的独立探针能共用标签吗？ {#cross-cross-nov18-latest-gandalf-bvb}

??? note "展开答案与例子"

    **答案：** 不能直接共用。前者判断交付物criteria，后者先问文档是否足够回答并隔离生成答案。问题、参照和权限不相同。

    **教学例子：** 教学例：引用页存在不证明PowerPoint里实际画了正确图。

    对照来源：[gandalf-bvb](../../../agent-research/2611.22841-gandalf-bvb/README.md) · [askalcf-protocol](../../../agent-research/2611.15700-askalcf-protocol/README.md)

### 它与ELITE的无评测演化是一回事吗？ {#cross-cross-nov18-latest-self-organized-learning}

??? note "展开答案与例子"

    **答案：** 不是。ELITE规定同父探索和代码整合，排除下游结果；本篇让teacher在自造游戏反馈下自主设计学习循环。干预和反馈权限不同。

    **教学例子：** 教学例：强行按7子代整合运行就不再是自由自组织设定。

    对照来源：[self-organized-learning](../../../agent-research/2611.23219-self-organized-learning/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 它和Harness²都不看rubric，为何不是同一算法？ {#cross-cross-nov19-ahe-beta}

??? note "展开答案与例子"

    **答案：** Harness²用当前任务执行对照组合候选，再积累如何改的经验；AHE-Beta以会话需求、角色分工和审查准入选择跨任务结构改动。

    **教学例子：** 教学例：比较两个产物和核实中断控制需求，是两种不同证据。

    对照来源：[ahe-beta](../../../agent-research/2611.24924-ahe-beta/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 相比Harness²，它的安全门是否证明风险不会增加？ {#cross-cross-nov19-safe-personal-rsi}

??? note "展开答案与例子"

    **答案：** 不证明。它比较最大primary类别点估计，次大类别甚至总primary风险可增加；Harness²的执行对照又不是这个领域风险门。

    **教学例子：** 教学例：最大类别维持2/20，另一类别0→1/20仍可能准入。

    对照来源：[safe-personal-rsi](../../../agent-research/2611.23651-safe-personal-rsi/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### 相比Harness²或kernel评测，它的目标有什么不同？ {#cross-cross-nov19-rsibench-infra}

??? note "展开答案与例子"

    **答案：** 这里检查整个模型服务/训练链路在质量门下是否更快；harness任务通过或单kernel提速不证明端到端吞吐提高。

    **教学例子：** 教学例：kernel快2倍但数据传输占90%，整条链路提升仍可能很小。

    对照来源：[rsibench-infra](../../../agent-research/2611.24395-rsibench-infra/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

### SearchInject和SilentGuard的门槛是否相同？ {#cross-cross-nov19-searchinject}

??? note "展开答案与例子"

    **答案：** 不是。前者筛选检索上下文，后者验证工具结果不变量；一种通过不证明另一种安全。

    **教学例子：** 教学例：低风险页面仍可能给出不满足过滤条件的API值。

    对照来源：[searchinject](../../../agent-research/2611.02643-searchinject/README.md) · [silentguard](../../../agent-research/2611.20595-silentguard/README.md)

### CCI和MLE-STAR的消融分数能互换吗？ {#cross-cross-nov20-buggymle-cci}

??? note "展开答案与例子"

    **答案：** 不能。CCI预测结构困难度，MLE-STAR用执行和validation消融选择值得改的代码块；结构困难不等于模型效果差。

    **教学例子：** 教学例：跨文件修复很难，并不说明该模型validation AUC低。

    对照来源：[buggymle-cci](../../../agent-research/2611.25088-buggymle-cci/README.md) · [mle-star](../../../agent-research/2506.15692-mle-star/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-20** · 本地仅实现给定十项特征的benchmark中位数、固定校准投影和可选的稳定logistic读数。没有AST/依赖图抽取、Injector、Oracle、LLM solver、校准拟合或模型训练。完整μ/σ、组尺度、截距与参考边界未在原文公开成可直接加载文件，因此API强制调用方显式提供Calibration；诊断用合成校准，不能称为复算了作者八benchmark CCI。Patch特征属于构建/评测端，不能把隐藏修复补丁或其困难标签传给被测Agent。 完整实验高成本不复现。

涉及：[buggymle-cci](../../../agent-research/2611.25088-buggymle-cci/README.md) · [mle-star](../../../agent-research/2506.15692-mle-star/README.md)

**2026-11-19** · 显式数值夹具只检查feature顺序、严格>阈值、干净经验约束与refill。无真实payload、SciFact检索、拟合分类器、生成模型或安全认证；更低阈值移除更多候选，也可能补入原rank10外的攻击页。 完整高成本实验不复现，审查DONE。

涉及：[searchinject](../../../agent-research/2611.02643-searchinject/README.md) · [silentguard](../../../agent-research/2611.20595-silentguard/README.md)

**2026-11-19** · 仅做原文审查、成本评估、中英文说明和学习材料。没有把OCI字段stub、任意microbenchmark或单卡小模型标成RSIBench-Infra已接入；local_operator=null，不提供可执行Evolve算子。项目页https://rsibench-infra.github.io已核对，未验证论文专用源码仓库公开。 完整实验高成本不复现，不作能力证据。

涉及：[rsibench-infra](../../../agent-research/2611.24395-rsibench-infra/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-19** · 实现Replay评测记录、最大类别风险准入、持久veto、最少重放/完成检查、严格多数确认两种协议与回滚gain-retention的零gain约定。未实现Willow/Kicker、邮件工具、攻击搜索、LLM修复、语义judge、verification回放或OAuth修复。Replay不是给Actor的输入，只有离线evaluator调用。 完整实验高成本不复现，不作能力证据。

涉及：[safe-personal-rsi](../../../agent-research/2611.23651-safe-personal-rsi/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-19** · 只实现类型化Evidence/Requirement交付集、已核实合并需求的covers消解，以及绑定head与RFC的纯merge_eligible判定。没有模拟用户、Triage/Architect/PM语言判断、开发Agent或真正git合并。结构字段不保证字符串内部绝无隐藏答案，所以保持L0，不把类型检查称为语义安全。 完整实验高成本不复现，不作能力证据。

涉及：[ahe-beta](../../../agent-research/2611.24924-ahe-beta/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-18** · 本轮review-only，不用预写课程／固定答案脚本替代自组织行为，不启动Bash工具Agent或付费gameplay。保留官方project入口和固定v1方法、预算及允许权限，未验证作者源仓库时明确记未核实。 完整实验高成本不复现，不作能力证据。

涉及：[self-organized-learning](../../../agent-research/2611.23219-self-organized-learning/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-18** · 本轮review-only，不提供一个空JSON接口冒充reactive verifier，不调用付费模型，也不重建native banking环境。官方Gandalf与BVBv1.0仓库可供后续显式预算实验，但本轮没有运行或审计其全部运行权限。 完整实验高成本不复现，不作能力证据。

涉及：[gandalf-bvb](../../../agent-research/2611.22841-gandalf-bvb/README.md) · [askalcf-protocol](../../../agent-research/2611.15700-askalcf-protocol/README.md)

**2026-11-18** · 本轮review-only，无模型矩阵／task复刻／metrics。完整3168轮API执行及部分未公开collaborator技能不适合低成本忠实复现；保留协议与资产可用边界为审查DONE，不把私有skill目的描述冒充技能实现。 完整实验高成本不复现，不作能力证据。

涉及：[skillbuffbench](../../../agent-research/2611.22017-skillbuffbench/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-18** · variance_components执行附录B.2的两个估计，返回负的run_variance_unbiased与仅截断的run_sd，要求至少2×2平衡有限数值矩阵。输入必须是已经测量且来源明确的结果；模块不生成agent轨迹、不选择候选，也不伪造方差置信区间或powered superiority。 完整实验高成本不复现，不作能力证据。

涉及：[resolution-hypothesis](../../../agent-research/2611.23068-resolution-hypothesis/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-18** · 本地L0 generation真实调用独立explore、exploration_gate、integrate、acceptance_gate；共同parent映射不可变，越界／空patch和非bool门结果拒绝。IntegrationRequest只有parent与有效children，不接收任务成绩／轨迹。失败acceptance或无有效子代保留原parent，不选择“次优分数”。回调可编译示例源码但没有LLM、SWE容器或安全沙箱。 完整实验高成本不复现，不作能力证据。

涉及：[elite-eval-free](../../../agent-research/2611.21056-elite-eval-free/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-18** · 本地独立实现已核的no_op_repeat和idempotence_block两种guard，以及Eq2–5回放评分／union选择；明确不含其余四primitive、goal extractor、LLM综合和在线retirement。安全参考score阈值必须显式提供，不把教学0.5当论文统一常数。未知primitive严格拒绝，不静默跳过；上游当前repo比v1多primitive，不能据此改写原论文事实。 完整实验高成本不复现，不作能力证据。

涉及：[metaact](../../../agent-research/2611.20655-metaact/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-18** · 本地guarded_count实际调用API回调及辅助查询，失败真实重发原调用一次；无效count删去而不是返回0。action_for_checks实现learned/exact阈值；AnswerGate跟踪查询条件数，防止用宽松查询的verified count替代更严格请求。只支持计数切片，未实现列表验证、contract miner、值交换检查、模型或训练。 完整实验高成本不复现，不作能力证据。

涉及：[silentguard](../../../agent-research/2611.20595-silentguard/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-18** · 本地只执行interval_score与parameter_score：正值物性先取log10，检查端点有序、有限与key完全一致。evaluator_truth没有Actor回调入口；它是评分器专用参数，不是给被评策略的信息。未实现热求解器、实验选择、拟合、科学家LLM或无提交聚合，不据此宣称科学任务复现。 完整实验高成本不复现，不作能力证据。

涉及：[sciresearch-eval](../../../agent-research/2611.21541-sciresearch-eval/README.md) · [askalcf-protocol](../../../agent-research/2611.15700-askalcf-protocol/README.md)

**2026-11-18** · FiniteTask执行资源／凭证前置条件、收费batch和BFS精确见证；metrics分别保留成功、错误终态、剩余距离和效率。合成图只验证算子，不运行LLM，也不把BFS答案喂给策略。100,000状态上限触发时明确报错，绝不退成近似下界冒充exact。未实现官方任务源语料、远程端点或哈希冻结全链。 完整实验高成本不复现，不作能力证据。

涉及：[detourbench](../../../agent-research/2611.20844-detourbench/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-18** · 按修复类型分层，真实checker接受修改、全量审计回滚回归，再按规则和概率顺序门控；本地仅文件映射回调。 完整实验高成本不复现，局部协议不作能力或Evolve证据。

涉及：[prodpilot-protocol](../../../agent-research/2611.17381-prodpilot-protocol/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-18** · 回答盲的生产／全库充分性pivot、独立质量信号、revision缓存与受人审动作控制的修复协议。 完整实验高成本不复现，局部协议不作能力或Evolve证据。

涉及：[askalcf-protocol](../../../agent-research/2611.15700-askalcf-protocol/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-15** · 策略readiness门后分解证明依赖，带反驳的重叠树综合与全局验证指导局部修订／重新探索，结果grader与候选选择隔离。 ScientistTwo控制子集到全量实验和review闭环；Colosseum核查数学假设与跨节论证。共同的多阶段形态不使语义judge或证据充分性可互换。

涉及：[stellar-colosseum](../../../agent-research/2609.15983-stellar-colosseum/README.md) · [scientist-two](../../../agent-research/2609.19644-scientist-two/README.md)

**2026-11-15** · 把既有自动harness优化用于真实多Agent检索，记录完整历史并分析优化后仍未消除的编排失败；不提出新优化器。 HarnessLens强调受影响行为的配对验证与归因门；MULTILOOP的整体提升多来自提示和工具。总分提高不能单独证明结构协调改善，10训练样例也不代表低API成本。

涉及：[multiloop](../../../agent-research/2611.15754-multiloop/README.md) · [harnesslens](../../../agent-research/2608.27311-harnesslens/README.md)

**2026-11-13** · 补入CoDirector分轴UCB和独立质量选优，与RuHarness联合后验低分位及validation准入比较：明确乐观探索和保守接受的不同不确定性用途；两者本地机制检查均不是完整生成或自进化能力。

涉及：[co-director](../../../agent-research/2604.24842-co-director/README.md) · [ruharness](../../../agent-research/2610.36826-ruharness/README.md)

**2026-11-13** · 补入经典程序进化与评价级联，区分搜索结果、构造验证与研究主张完整性；记录官方未发布运行系统、完整实验高成本不复现和零本地执行能力。

涉及：[alphaevolve](../../../agent-research/2506.13131-alphaevolve/README.md) · [scientist-one](../../../agent-research/2605.26340-scientist-one/README.md)

**2026-11-13** · 补入检索初始化与消融定向细化，区分块级搜索与成本感知树调度；核对2025精确v1日期、生成产物与控制器源码边界，完整实验高成本不复现。

涉及：[mle-star](../../../agent-research/2506.15692-mle-star/README.md) · [mars-research](../../../agent-research/2602.02660-mars-research/README.md)

**2026-11-13** · 补入EnvHarness环境侧可组合控制，区分Agent执行层和环境练习层；CPU三seed仅验Stage/Contract/serialChain合同，完整商业rollout和8H100训练不复现。

涉及：[envharness](../../../agent-research/2608.19880-envharness/README.md) · [harness2](../../../agent-research/2610.14224-harness2/README.md)

**2026-11-13** · 补入Google ScientistTwo历史漏项，区分科研扩展控制与证据完整性；局部CPU合同不生成科学结果，完整多日商业Agent实验高成本不复现。

涉及：[scientist-two](../../../agent-research/2609.19644-scientist-two/README.md) · [scientist-one](../../../agent-research/2605.26340-scientist-one/README.md)

**2026-11-12** · 加入下游规则治理这一演化位置：明确scope互斥、3→2→1真实状态更新与SME信任边界，并与PASE程序validation准入区分；完整API/人工系统不复现。

涉及：[agent-gym](../../../agent-research/2608.15591-agent-gym/README.md)

**2026-11-11** · 加入FGSE和PASE，分别拆开风险约束准入与validation-only程序补丁接受，并与Verified Quantum Wiki的规范绑定独立证明比较；不将CPU经验门、语法解析或模拟凭据包装成完整自进化/证明能力。

涉及：[fgse](../../../agent-research/2611.14326-fgse/README.md) · [pase](../../../agent-research/2611.14019-pase/README.md) · [verified-quantum-wiki](../../../agent-research/2611.09822-verified-quantum-wiki/README.md)

**2026-11-09** · 加入 Verified Quantum Wiki，区分 Strategist 的开发集选择与冻结规范下的独立证明后合入。证明保证的是规范所声明的性质；本地只检查外部结果的绑定及合入阈值。

涉及：[verified-quantum-wiki](../../../agent-research/2611.09822-verified-quantum-wiki/README.md)

**2026-11-06** · 补入 EnvOpt，明确模型/Harness 固定时可演进的第三层环境表示；与 Meta² 的单次运行编辑和 Continual AutoResearch 的会话经验测量分开。留出验证回滚不等于暴露训练金标；本地 CPU 离线核不是完整自主环境优化。

涉及：[envopt](../../../agent-research/2611.07372-envopt/README.md) · [meta-square](../../../agent-research/2611.05139-meta-square/README.md) · [continual-autoresearch](../../../agent-research/2611.05108-continual-autoresearch/README.md)

**2026-11-05** · 把三种常被混叫RSI的对象拆开：Meta²冻结跨任务指导，只修改当前run；Continual AutoResearch度量会话、工作区经验是否更早产生好候选，而不保证最终选得更好；RSI-Dojo用训练环境和筛选轨迹把后训练过程内化进模型，完整实验高成本不复现。Meta²与Continual AutoResearch仅实现CPU合同组件，RSI-Dojo只收录；三者均不是模型能力提升证据，完整实验高成本不复现、审查DONE。

涉及：[meta-square](../../../agent-research/2611.05139-meta-square/README.md) · [continual-autoresearch](../../../agent-research/2611.05108-continual-autoresearch/README.md) · [rsi-dojo](../../../agent-research/2611.03698-rsi-dojo/README.md)

**2026-11-04** · 精读Strategist，并与Reflexion、EvalAlloc区分跨任务可执行结构库、可读教训和评测预算。新增AST去重的显式prompt边界、validation/hidden双门槛与2个百分点/2%成本带解释；未把CPU合成选择核宣传为真实搜索，原文8×H200完整矩阵高成本不复现、审查DONE。

涉及：[strategist](../../../agent-research/2611.03618-strategist/README.md) · [reflexion](../../../agent-research/2303.11366-reflexion/README.md) · [evalalloc](../../../agent-research/2610.37276-evalalloc/README.md)

**2026-10-30** · 精读CROP与EvalAlloc：以Self-Refine/RuHarness为对照，分开系统提示修改、rubric价值和SEARCH观测预算；补validation/CoT成本、观测优先补全、公共prefix确认及未实现MIRT/controller边界。

涉及：[crop](../../../agent-research/2604.14214-crop/README.md) · [evalalloc](../../../agent-research/2610.37276-evalalloc/README.md) · [self-refine](../../../agent-research/2303.17651-self-refine/README.md) · [ruharness](../../../agent-research/2610.36826-ruharness/README.md)

**2026-10-29** · RuHarness的criterion frontier不是按一次正确率排序：2×3行为/结果联合表用Jeffreys-Dirichlet后验估计保守utility分位，集合新颖性和冗余仍固定来自已测轨迹。它把有限样本不确定性和候选准入分开，只有active准则能进入frontier，最终harness修改还要独立validation严格增益。本地没有LLM评审或harness生成。

涉及：[ruharness](../../../agent-research/2610.36826-ruharness/README.md)

**2026-10-27** · 首版：比较当前修订、跨trial反思、局部验证、非贪心接口种群、分层干预与有护栏生产闭环。

覆盖 43 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 78 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Discovering formally verified quantum programs with AI](../../../agent-research/2611.09822-verified-quantum-wiki/README.md)
- [Meta²: Precomputing Reusable Knowledge for Online Harness Evolution in Long-Horizon Agents](../../../agent-research/2611.05139-meta-square/README.md)
- [From AutoResearch to Continual AutoResearch: Do Agents Learn Across Tasks?](../../../agent-research/2611.05108-continual-autoresearch/README.md)
- [Training LLM Agents to Automate LLM Post-Training with RSI-Dojo](../../../agent-research/2611.03698-rsi-dojo/README.md)
- [Strategist: Evolving Reasoning with Agents](../../../agent-research/2611.03618-strategist/README.md)
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
- [EnvOpt: Automated Optimization for Agent Environments](../../../agent-research/2611.07372-envopt/README.md)
- [When Should Agents Remember? Falsification-Gated Self-Evolution for LLM Agents](../../../agent-research/2611.14326-fgse/README.md)
- [Program-Aided Patchable Skill Evolution](../../../agent-research/2611.14019-pase/README.md)
- [Agent Gym: A Framework for Continuous Evaluation and Evolution of LLM Agents Through Human-in-the-Loop Feedback](../../../agent-research/2608.15591-agent-gym/README.md)
- [ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI](../../../agent-research/2609.19644-scientist-two/README.md)
- [EnvHarness: Awakening Static Worlds for Agent Learning](../../../agent-research/2608.19880-envharness/README.md)
- [MLE-STAR: Machine Learning Engineering Agent via Search and Targeted Refinement](../../../agent-research/2506.15692-mle-star/README.md)
- [AlphaEvolve: A coding agent for scientific and algorithmic discovery](../../../agent-research/2506.13131-alphaevolve/README.md)
- [Co-Director: Agentic Generative Video Storytelling](../../../agent-research/2604.24842-co-director/README.md)
- [MULTILOOP: Evolving Multi-Agent Harnesses for Complex Information-Seeking Tasks](../../../agent-research/2611.15754-multiloop/README.md)
- [Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science](../../../agent-research/2609.15983-stellar-colosseum/README.md)
- [AskALCF: A Self-Improving Agentic System for Intelligent HPC User Support](../../../agent-research/2611.15700-askalcf-protocol/README.md)
- [ProdPilot: A Layered Model Context Protocol System for Automated Production Readiness and Deployment of Vibe-Coded Projects](../../../agent-research/2611.17381-prodpilot-protocol/README.md)
- [DetourBench: Trajectory-Level Evaluation of Interactive Agents with Exact Minimum-Action Bounds](../../../agent-research/2611.20844-detourbench/README.md)
- [SciResearch-Eval: Evaluating Scientific Judgment in Autonomous Experimental Agents](../../../agent-research/2611.21541-sciresearch-eval/README.md)
- [Invariant-Aware Harness Enforcement to Protect LLM Agents from Silent API Failures](../../../agent-research/2611.20595-silentguard/README.md)
- [MetaAct: Self-Evolving Executable Action Constraints for Embodied Language Agents](../../../agent-research/2611.20655-metaact/README.md)
- [Evaluation-Free Recursive Self-Improvement for Coding Agents](../../../agent-research/2611.21056-elite-eval-free/README.md)
- [The Resolution Hypothesis: Agent Evolution&#x27;s Key Is Identifying Improvements](../../../agent-research/2611.23068-resolution-hypothesis/README.md)
- [SkillBuffBench: Measuring What Agent Skills Contribute across Harnesses, Models, Skill Access Modes and Memory](../../../agent-research/2611.22017-skillbuffbench/README.md)
- [Verifying Agents in Rubric-Graded Environments](../../../agent-research/2611.22841-gandalf-bvb/README.md)
- [Do LLM Agents Still Need to Be Told How to Self-Improve?](../../../agent-research/2611.23219-self-organized-learning/README.md)
- [Agentic Harness Engineering Beta: Requirement-Centered Evolution of Agent Harnesses](../../../agent-research/2611.24924-ahe-beta/README.md)
- [Safe Personal RSI: Evaluating and Repairing Personal-Agent Updates](../../../agent-research/2611.23651-safe-personal-rsi/README.md)
- [RSIBench-Infra: Can Agents Optimize Their Own Training and Inference Infrastructure at Production Scale?](../../../agent-research/2611.24395-rsibench-infra/README.md)
- [SearchInject: Retrieval Exposure Control for Indirect Prompt Injection in Language-Model Search](../../../agent-research/2611.02643-searchinject/README.md)
- [BuggyMLE: Scaling Machine Learning Engineering Difficulty with Bug Injection](../../../agent-research/2611.25088-buggymle-cci/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/harness-and-self-improvement.md) · [返回全部精读卡片](../index.md)
