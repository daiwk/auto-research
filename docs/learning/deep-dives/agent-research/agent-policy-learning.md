---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 交互学习：统一轨迹之后，信用和教师信息怎样分配

[Agent](../index.md) · 更新 2026-11-27 · 59 篇主题资料 / 12 篇重点对照

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
| [Decoupling Planning and Control for Instructable Agents](../../../agent-research/2608.26788-instruct-to-act/README.md) · [原始来源](https://arxiv.org/abs/2608.26788)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、复现边界 | 用自身rollout后标指令区间，BC监督已标动作、stop监督完成端点；保留Dreamer其他目标。 | AgentLightning解耦执行与RL训练transition，Instruct-to-Act解耦规划与高频控制。两种解耦不是同一接口，标签正确也不能补缺失RSSM和环境学习。 |
| [Experience-Handoff Reinforcement Learning for Recursive Self-Improvement](../../../agent-research/2611.16409-ace-rl/README.md) · [原始来源](https://arxiv.org/abs/2611.16409v1)<br>章节：背景与主要改动、核心公式 | 按任务、种子、反思来源建立三角色比较组，交接物信用取自全新actor的下游表现，联合生成token-mean更新共享模型。 | GiGPO在轨迹与共享anchor-state层分macro/micro信用；ACE-RL比较的是生成交接物的角色来源，不是state合流。没有真实actor环境时只能验证公式和控制合同。 |
| [From Acting to Learning: Experience Selection toward Continually Learning Agents](../../../agent-research/2611.27159-acting-to-learning/README.md) · [原始来源](https://arxiv.org/abs/2611.27159v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验 | 论文把成功交互后的经验选择单独隔离：历史池先固定，选择规则决定训练哪些action记录，所有学生使用同一训练预算与部署executor。它不是一个新通用梯度影响公式；打分沿用LESS式优化器感知梯度，贡献是Agent学习中的严格对照，尤其把排序规则和可选择的覆盖空间交叉。完整研究只有一次选择—训练阶段，没有验证多轮持续学习、遗忘或自主修改harness。 | ACE Lens把Accuracy、学习者相对Complexity和Diversity作为数据准入维度；本篇进一步问同样成功的action在当前学生/optimizer状态下，对公开任务family有多大梯度相关性，并把coverage自由度作为对照的一部分。两者都不能把“成功”自动等同于“最值得学”；较低NLL只表示容易预测，不是更高训练收益。ACE旧页的mini-suite也不是本篇ALFWorld训练对照，不能横向比较其满分与本文提升。 |
| [$R^2$: Recognizing and Reducing Redundant Visual Tool Use](../../../agent-research/2611.27070-r2-tool-redundancy/README.md) · [原始来源](https://arxiv.org/abs/2611.27070v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验 | R²把三个问题分开：CAT描述题目是否可能从工具获益；VFD描述一次返回观察对后续同一段推理文本提供多少额外似然支持；RA-GRPO在答对的轨迹之间比较工具效率，而不是奖励所有少调用的轨迹。CAT标签来自训练侧tool/no-tool rollouts的多次正确性和实际调用，不是根据问题长度或关键词猜测；VFD也不是gold-answer概率或“这次工具有用”的因果证明。 | AdaStep看同锚状态下动作间回报方差相对动作内噪声，调节局部信用可靠性；R²看当前视觉反馈对同一后续推理的依赖，并把成本只在correct集合内相对化。它们都补充终局奖励，但方差解释率不是观察必要性，VFD也不衡量动作内随机回报噪声。不能把AdaStep的权重直接当VFD，或把R²效率项施加给失败轨迹。本地两者都是统计/数值组件，不能比较其Agent能力。 |
| [Optimistic Online Learning for Coding Agents with Aggregate Feedback](../../../agent-research/2611.30405-ooas/README.md) · [原始来源](https://arxiv.org/abs/2611.30405v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、完整实验与成本决定 | OOAS把activation steering候选选择建模为逐turn多臂bandit。每轮先见所有候选的reward hint，选一个策略；任务结束只见已选序列的加和reward，不见逐轮贡献。它不是猜哪条编辑会通过隐藏测试，而是在聚合反馈粒度下修正累计hint误差。论文理论要求reward向量、hint和任务划分预先固定、独立于学习者随机数；真实编码Agent的状态依赖轨迹不自动满足该假设。 | From Acting to Learning在固定历史池里选SFT action记录，选择后冷启动学生；OOAS在任务执行中选steering臂，并在任务结束后修正hint。前者的梯度相关性不是后者的reward预测，后者的共享noise也不是经验重放的shuffle。两者都必须分开选择信息与最终评测；本地均没有真实Agent能力比较。 |
| [Compute-Aware Submodular Online Learning in Open Multi-Agent Systems](../../../agent-research/2611.34211-budgeted-submapl/README.md) · [原始来源](https://arxiv.org/abs/2611.34211v1)<br>章节：背景与主要改动、核心公式、论文离线与线上效果、数据协议与代码映射、结果、负控与边界、同主题比较与边界、完整实验与成本决定 | 固定域多agent分类策略在收益未知前分配rho，依赖舍入精确Q后只问所选边际，IPW与KL更新保留实际预算化策略学习。 | OOAS只见aggregate任务回报与逐turn hint，使用共享Exp噪声和整任务同臂概率；本篇可查询反事实坐标。重要性分母、反馈粒度与FTRL/KL更新不可替换。 |

</div>

## 取舍分析 {#analysis}

### 局部信用的来源决定何时能相信它

GiGPO通过同锚状态中的动作回报比较补充全局优势；AdaStep进一步问差异有多少来自动作，有多少来自同动作后的随机路径。DepGPO不依赖同状态重复，而以文件、stdout和verifier资源的实际依赖提供另一种结构线索。三者不是可互换的“每步reward”：没有可信状态或tracer时，细粒度数字再多也不增加证据。Agent Lightning的统一transition有助接入，但不能自动补全这些条件。

对照来源：[gigpo](../../../agent-research/2505.10978-gigpo/README.md) · [adastep](../../../agent-research/2610.03223-adastep/README.md) · [depgpo](../../../agent-research/2610.03634-depgpo/README.md) · [agent-lightning](../../../agent-research/2508.03680-agent-lightning/README.md)

### 教师改变数据来源，不应改变部署可见世界

Frontier-OPD在学生访问状态中选择短介入，接纳需比较实际桥长加续跑的同长窗口，且只把教师桥响应加入训练。ASTEROID在学生探索历史之后提供同隐藏任务的完整成功episode，使训练覆盖专家顺利开局之外的上下文。两者都利用教师，却采不同单位和目标；部署侧仍只能用公开观察与自身历史，不能为了方便重放把隐藏任务、gold或未来结果加进actor。

对照来源：[frontier-opd](../../../agent-research/2610.32802-frontier-opd/README.md) · [asteroid](../../../agent-research/2610.30105-asteroid/README.md)

### 轨迹变成训练数据时，目标边界比统一接口更重要

AgentLightning把异构执行记录变成可归因transition；Instruct-to-Act用同一episode内非重叠区间绑定语言，在末步标指令完成。未标注有效步不贡献BC却仍是stop负例，padding两者排除。完整controller还需RSSM、actor/value与真实rollout，单独两项loss不得宣传为通用指令执行器。

对照来源：[instruct-to-act](../../../agent-research/2608.26788-instruct-to-act/README.md) · [agent-lightning](../../../agent-research/2508.03680-agent-lightning/README.md)

### 组相对信用首先要明确组里比较的对象

GiGPO把轨迹整体reward和同一anchor-state动作差异分开；ACE-RL让actor任务、reflector种子和curator反思各自成组，编辑价值来自新的执行而非文字评分。即使两者都中心化reward，来源、counterfactual和信息边界也不同。singleton过滤与token归约还会改变哪些角色被训练，不能用一个通用group-normalize替代。

对照来源：[ace-rl](../../../agent-research/2611.16409-ace-rl/README.md) · [gigpo](../../../agent-research/2505.10978-gigpo/README.md)

### From Acting to Learning：成功经验该选哪些，而不只是收集多少

候选LoRA梯度在warmup第8/16/24/32个checkpoint上，与冻结Adam一、二阶矩构成ranking feature；省略bias correction，不能称作完整AdamW更新。每个公共support梯度先单独归一化，再按任务family取均值；候选feature归一化后与之做点积，先平均checkpoint，再在family间取最大。40条公开support action不含评测query答案。全局选择先按完整messages内容精确去重，保留首代表索引，选256种内容，再三次shuffle共768次展示；matched版本保持reference每个task/action位置与不同内容配额。最终学生从原始base重新开始，不能继承打分warmup权重。负控核对checkpoint/family运算顺序、support均值不再归一化、重复行不增加random抽样概率、得分并列按首代表索引、每个shuffle pass访问全部选中内容、matched仍可选择reference以外的同stratum内容、跨stratum重复内容拒绝、NaN/负二阶矩/中间溢出拒绝。seed只改变合成输入与调度，不是独立训练。

对照来源：[acting-to-learning](../../../agent-research/2611.27159-acting-to-learning/README.md) · [ace-data](../../../agent-research/2608.27260-ace-data/README.md)

### R²：把视觉反馈依赖变成正确轨迹内的效率优势

VFD仅替换当前调用的视觉反馈，保留原图、其他历史与待评分推理tokens；实际反馈的平均log概率减去3个同尺寸不重叠随机crop的平均。前10%训练步按来源、只用reasoning windows估计30%分位阈值，之后冻结；直接答案window可在监督时用，但不参与初始化。每轨迹均匀抽一个eligible call，以M×冗余指示量估计全部eligible冗余数，完整记录但score缺失时指示量设1，空eligible集为0。Tool-Independent另加0.5×全部调用数。效率优势只在同题答对轨迹内居中、除固定调用预算4，再以0.2加到outcome优势；不能把失败少调用当高效率成功。负控包括actual与alternative相同时VFD为0、阈值不吸收答案window、来源缺warmup拒绝、d恰好等于阈值不判冗余、None与空eligible区分、抽一个调用而非逐个累加、失败轨迹效率项严格为0、correct集合内效率项和为0、全错/单个correct/相同cost时效率为0、负优势裁剪方向、padding无贡献与中间溢出拒绝。三seed的数值控制不支持工具效率或准确率提升结论。

对照来源：[r2-tool-redundancy](../../../agent-research/2611.27070-r2-tool-redundancy/README.md) · [adastep](../../../agent-research/2610.03223-adastep/README.md)

### OOAS：只看到任务总回报，也能用逐轮hint学习策略

分布不是softmax：FTRL同时使用Tsallis项和log barrier。turn t把已完成任务score、当前任务此前hint和本轮hint乘已过turn数相加，再求内点最优分布。每任务只抽一次K个Exp(1)噪声，所有turn共享，以argmin ξ/p选臂。整任务都选同一臂k的概率ρ由各turn概率比的最大值计算，不能用边缘概率相乘；只有该事件发生时才以Z/ρ修正此臂，发生切臂则残差修正全0，但所有臂仍加hint之和。Alg2用可观察potential gap的有符号累积触发严格大于阈值的doubling，重启score与gap，不把负gap裁为0。负控覆盖KKT残差、分布平移不变、共享noise的整任务事件概率不等于独立概率乘积、切臂时无残差归因、每turn的hint倍率、任务长度上限、重复begin/finish拒绝、aggregate越界不丢pending状态、保留负potential gap及重启后score归零。使用分析事件分区核对importance权重，不用少量Monte Carlo冒充无偏证明。

对照来源：[ooas](../../../agent-research/2611.30405-ooas/README.md) · [acting-to-learning](../../../agent-research/2611.27159-acting-to-learning/README.md)

### 预算反馈的无偏性取决于采样事件，不是统一的1/p技巧

SubMAPL的rho是边缘包含概率，固定基数依赖舍入须保E[Z]=rho，query选择不能偷看当前gain或联合action。IPW后在每agent simplex做KL mirror-ascent，sqrt分配最小化二阶矩上界而非保证胜率。OOAS全任务共享noise使同臂事件概率不等于边缘概率乘积，切臂时不归因残差。两者本地都是有限数学核，非LLM Agent。SubMAPL迁移/环境尚未承接且无证据高成本，完整状态保留scope-limited/false full-review，不能制造高成本DONE。

对照来源：[budgeted-submapl](../../../agent-research/2611.34211-budgeted-submapl/README.md) · [ooas](../../../agent-research/2611.30405-ooas/README.md)

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

### 算出BC和stoploss是否已复现语言worldmodelcontroller？ {#cross-cross-colm-instruct-to-act}

??? note "展开答案与例子"

    **答案：** 没有。原目标还包括RSSM模型、actor、value训练及真实rollout，指令embedding和标注器也不可缺。本地仅真实执行两项辅助目标，不替代缺失网络。

    **教学例子：** 教学例：一组logits梯度正确，不等于模型在Minecraft能挖出钻石。

    对照来源：[instruct-to-act](../../../agent-research/2608.26788-instruct-to-act/README.md) · [agent-lightning](../../../agent-research/2508.03680-agent-lightning/README.md)

### 把所有actor、reflector和curator按同一task合成一个GRPO组是否保留ACE-RL？ {#cross-cross-nov15-ace-rl}

??? note "展开答案与例子"

    **答案：** 不保留。它们reward含义和比较来源不同，会把角色基线混合。原文必须保留seed／reflection provenance，最后才合并token执行一次共享策略更新。

    **教学例子：** 教学例：同一反思的三条编辑要互比，不能与另一个actor的任务分数直接抢基线。

    对照来源：[ace-rl](../../../agent-research/2611.16409-ace-rl/README.md) · [gigpo](../../../agent-research/2505.10978-gigpo/README.md)

### 与ACE Lens相比，本篇额外控制了什么？ {#cross-cross-nov23-acting-to-learning}

??? note "展开答案与例子"

    **答案：** ACE组织数据可信度、复杂度和覆盖；本篇把排序规则与选择空间分开，global random和global high-NLL也可自由改变coverage，避免把自由度差异误算成gradient优势。

    **教学例子：** 教学例：如果gradient可跨任务挑256条，random也应能跨任务挑256条；不能只给random固定旧任务配额。

    对照来源：[acting-to-learning](../../../agent-research/2611.27159-acting-to-learning/README.md) · [ace-data](../../../agent-research/2608.27260-ace-data/README.md)

### R²与AdaStep都是credit方法，能交换统计量吗？ {#cross-cross-nov23-r2-tool-redundancy}

??? note "展开答案与例子"

    **答案：** 不能。AdaStep从同状态动作组的回报方差估计局部信用可靠性；R²用当前视觉反馈的同文本似然差估计冗余成本，再只在correct集合内比较。它们条件信息与归一化对象不同。

    **教学例子：** 教学例：重复crop可能VFD接近0，但动作后环境回报很稳定；稳定不等于观察不冗余。

    对照来源：[r2-tool-redundancy](../../../agent-research/2611.27070-r2-tool-redundancy/README.md) · [adastep](../../../agent-research/2610.03223-adastep/README.md)

### 与From Acting to Learning都做选择，选择的对象和时点相同吗？ {#cross-cross-nov24-ooas}

??? note "展开答案与例子"

    **答案：** 不同。旧文选历史action用于后续SFT；OOAS在当前执行turn选steering策略，结束后用aggregate更新。不能用离线gradient score直接替代hint并宣称有同样regret保证。

    **教学例子：** 教学例：挑256条清洁经验是训练数据选择；本轮选Cap=1.5还是2.0是在线干预选择。

    对照来源：[ooas](../../../agent-research/2611.30405-ooas/README.md) · [acting-to-learning](../../../agent-research/2611.27159-acting-to-learning/README.md)

### SubMAPL与OOAS的重要性权重可互换吗？ {#cross-cross-nov27-budgeted-submapl}

??? note "展开答案与例子"

    **答案：** 不可。前者观察被查询的反事实边际，按坐标包含概率校正；OOAS只观察任务总反馈，按共享noise产生的整任务同臂事件概率校正hint残差。两者反馈可见性和更新器都不同。

    **教学例子：** 教学例：一任务中切过臂时OOAS残差归因全0；SubMAPL同轮选中的两坐标仍各按自己的rho更新。

    对照来源：[budgeted-submapl](../../../agent-research/2611.34211-budgeted-submapl/README.md) · [ooas](../../../agent-research/2611.30405-ooas/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-27** · 固定active-domain的clipped sqrt包含分配、精确Q依赖舍入、独立joint-action采样、仅所选坐标oracle查询、IPW与log-space KL更新；真归一化子模coverage小函数与评估侧期望控制。无LLM Agent、动态迁移M、完整环境/观察策略表，未伪造高成本终态。 组件范围完成；完整便宜模拟/迁移未承接，not_run_scope_limited，非高成本延期。

涉及：[budgeted-submapl](../../../agent-research/2611.34211-budgeted-submapl/README.md) · [ooas](../../../agent-research/2611.30405-ooas/README.md)

**2026-11-24** · 独立标准库CPU核实际解FTRL的KKT方程：Gk+α/√pk+β/pk为共同乘子，通过平移score与二分求解，而非softmax替身；实现共享Exp采样、ρ、聚合残差、potential和Alg2重启。begin→choose→finish只接受当前hint和最终aggregate，不接受turn reward向量或gold答案/计划。噪声注入只供数学控制。没有LLM、activation probe、TACT干预、代码执行器、真实任务分数或Evolve映射。数值求根是有公差的float64近似，不声称无限精度理论实现。 完整campaign终态不复现，审查DONE。

涉及：[ooas](../../../agent-research/2611.30405-ooas/README.md) · [acting-to-learning](../../../agent-research/2611.27159-acting-to-learning/README.md)

**2026-11-23** · CPU NumPy组件只执行同文本token log概率的VFD差、reasoning-only分来源冻结阈值、单eligible-call无偏冗余估计和类别base cost、sample-SD outcome advantage、仅正确轨迹效率项及clipped GRPO标量目标。分位数采用线性插值、目标按每轨迹有效token均值再组平均，是公开的数值约定；不宣称与未公开trainer逐位相等。调用方必须已保证同一推理window、有效crop与完整记录；数组不能证明这些语义。没有VLM、crop构造/评分、CAT rollout标注、图像数据、policy反传/更新或视觉Agent评测；数值差分只检验标量目标导数，不是训练。没有gold答案/计划接口，reward为外部trainer/evaluator给定的0/1标量。 完整实验高成本不复现，审查DONE。

涉及：[r2-tool-redundancy](../../../agent-research/2611.27070-r2-tool-redundancy/README.md) · [adastep](../../../agent-research/2610.03223-adastep/README.md)

**2026-11-23** · 本地独立实现NumPy float64公式核：显式梯度/冻结moments转feature、逐support向量归一化、checkpoint平均后family最大值、按完整字符串精确去重、全局top/random和三轮调度、按reference逐位置匹配stratum并保持不同内容配额的选择。零范数方向原文未定义，明确拒绝而不补造0分；feature中间溢出也拒绝。测试用显式合成梯度与历史action字符串，不把梯度相似度换成词项相似度。没有自动抽LoRA梯度、warmup训练、ALFWorld、Qwen checkpoint、部署executor、学生SFT或能力比较；调用方必须保证support来自公开训练侧而非query答案。 完整实验高成本不复现，审查DONE。

涉及：[acting-to-learning](../../../agent-research/2611.27159-acting-to-learning/README.md) · [ace-data](../../../agent-research/2608.27260-ace-data/README.md)

**2026-11-15** · 按任务、种子、反思来源建立三角色比较组，交接物信用取自全新actor的下游表现，联合生成token-mean更新共享模型。 GiGPO在轨迹与共享anchor-state层分macro/micro信用；ACE-RL比较的是生成交接物的角色来源，不是state合流。没有真实actor环境时只能验证公式和控制合同。

涉及：[ace-rl](../../../agent-research/2611.16409-ace-rl/README.md) · [gigpo](../../../agent-research/2505.10978-gigpo/README.md)

**2026-11-13** · 补入instruct-to-act历史遗漏，用自身rollout后标指令区间，BC监督已标动作、stop监督完成端点；保留Dreamer其他目标。 AgentLightning解耦执行与RL训练transition，Instruct-to-Act解耦规划与高频控制。两种解耦不是同一接口，标签正确也不能补缺失RSSM和环境学习。

涉及：[instruct-to-act](../../../agent-research/2608.26788-instruct-to-act/README.md) · [agent-lightning](../../../agent-research/2508.03680-agent-lightning/README.md)

**2026-10-27** · 首版：比较transition接入、状态组信用、方差可靠性、命令依赖与两种教师数据机制，明确训练和部署信息边界。

覆盖 53 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 59 篇资料</summary>

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
- [Decoupling Planning and Control for Instructable Agents](../../../agent-research/2608.26788-instruct-to-act/README.md)
- [Experience-Handoff Reinforcement Learning for Recursive Self-Improvement](../../../agent-research/2611.16409-ace-rl/README.md)
- [From Acting to Learning: Experience Selection toward Continually Learning Agents](../../../agent-research/2611.27159-acting-to-learning/README.md)
- [$R^2$: Recognizing and Reducing Redundant Visual Tool Use](../../../agent-research/2611.27070-r2-tool-redundancy/README.md)
- [Optimistic Online Learning for Coding Agents with Aggregate Feedback](../../../agent-research/2611.30405-ooas/README.md)
- [Compute-Aware Submodular Online Learning in Open Multi-Agent Systems](../../../agent-research/2611.34211-budgeted-submapl/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/agent-policy-learning.md) · [返回全部精读卡片](../index.md)
