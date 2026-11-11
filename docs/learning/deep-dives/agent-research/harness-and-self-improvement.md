---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 自改进先标对象：答案、经验、接口与系统版本

[Agent](../index.md) · 更新 2026-11-11 · 54 篇主题资料 / 17 篇重点对照

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

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

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

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 54 篇资料</summary>

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

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/harness-and-self-improvement.md) · [返回全部精读卡片](../index.md)
