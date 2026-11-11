---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 评测追问四件事：完成了、稳健吗、靠什么、花多少

[Agent](../index.md) · 更新 2026-11-11 · 48 篇主题资料 / 11 篇重点对照

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
| [AgentHeal: Evaluating Goal-Preserving Resource Recovery of Web Agents under Access Barriers](../../../agent-research/2610.39234-agentheal/README.md) · [原始来源](https://arxiv.org/abs/2610.39234)<br>章节：背景与主要改动、核心公式、数据协议与实现边界、本地结果与负控 | 显式构造无障碍、可恢复和不可恢复资源三联，按副本/版本关系、障碍诊断和访问政策联合评价目标保真。 | 不可恢复时正确行为是诚实弃答而非强行回答；需要独立来源与政策标注，本地真值表不具备浏览器或语义judge能力。 |
| [XStack: A Benchmark for ML Repo Migration](../../../agent-research/2611.08472-xstack/README.md) · [原始来源](https://arxiv.org/abs/2611.08472)<br>章节：评估协议、论文离线与线上效果、复现与验证边界 | 以干净 TPU 全规模重训、独立判分、反作弊与原框架权重回载共同定义通过；二阶段只公开配方并冻结入口外代码。 | 补配方与训练复现是不同诊断阶段；GPU 初步实验不可替代主 TPU 矩阵。本地只收录。 |
| [ARE-bench: Benchmarking Agents&#x27; Research Ability in Real-World Researcher Sessions and Workspaces](../../../agent-research/2611.14364-are-bench/README.md) · [原始来源](https://arxiv.org/abs/2611.14364)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 在真实会话切点保留仍有效要求与未清理workspace，actor/evaluator分离，以全条目ISR和逐任务macro CSR判断交付。 | 评分依赖可验证rubric与完整任务分母；本地只实现输入隔离和scorer，无官方75任务包、Actor或judge，不将手工例子算benchmark成绩。 |
| [ReproBridge: Building Reproducibility into ML Research Artifacts](../../../agent-research/2611.08452-reprobridge/README.md) · [原始来源](https://arxiv.org/abs/2611.08452)<br>章节：核心公式、数据协议与代码映射、高成本完整实验 | 将复现的执行知识保存为代码、环境、launcher和指南；评价侧把五次参考的双侧数值兼容与独立执行完整性审计分开。 | 公开任务不含私有参考/成功阈值；本地只有数学与文件证据合同，没有LLM Reproducer或语义Auditor，完整8×H100/多模型任务矩阵高成本不复现。 |
| [AlphaProof Code: Verifying Signal&#x27;s Security at the Machine-Code Level](../../../agent-research/alphaproof-code/README.md) · [原始来源](https://deepmind.google/documents/36/Formal_Verification_of_Signal_4.pdf)<br>章节：核心验证条件、来源核验、高成本完整实验 | 由人类批准规格，再用Lean内核、隔离规格副本及comparator检查顶层定理、所有传递定义和标准公理；证明生成Agent不自行宣布完成。 | 内核证明以可信规格、机器语义和密码学假设为前提，不等于真实意图充分；650万行证明及数小时工具链构建高成本，仅收录不复现。 |

</div>

## 取舍分析 {#analysis}

### 任务成功可以掩盖测量对象已经改变

GAIA式终局精确答案说明交付是否匹配参考，但若模拟用户提前透露本应由Agent询问的信息，任务仍成功却少测了信息获取。User Proxy Bench因此把UFS与任务reward分开。AgentPerturb从另一方向要求输入修改仍保持目标和可求解性：故意破坏到无解再责怪Agent，也没有测到原本想测的稳健性。好评测应控制任务与可见信息，而不只让分数发生变化。

对照来源：[gaia](../../../agent-research/2311.12983-gaia/README.md) · [user-proxy-bench](../../../agent-research/2609.38043-userproxybench/README.md) · [agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md)

### 配对设计之后，还要保留失败和归因条件

AlphaDiana强调逻辑样本不随重试扩张，所有attempt成本都要累计，运行成功与已评分分开。HDA的四臂要求逐样本对齐、预算控制与人审中和，且先确认涨分再归因。选择性评测的簇级证书则处理另一种相关性：同任务多条轨迹不能伪装成许多独立校准样本。它们共同约束怎样解释数字，却没有把未知评分、未检测捷径或未覆盖任务自动变成已验证。

对照来源：[alpha-diana](../../../agent-research/2610.20675-alpha-diana/README.md) · [harness-decomposition](../../../agent-research/2610.22466-harness-decomposition/README.md) · [certified-selective-eval](../../../agent-research/2609.34320-certified-selective-eval/README.md)

### 无解任务何时是合理评测，而不是破坏后的假稳健性

AgentPerturb要求扰动后仍保留原目标与可解性，避免凭空制造失败。AgentHeal则把真正不可恢复作为明确标注的独立regime，评价诚实弃答、障碍诊断和合规，而不强求不存在的答案；可恢复时又要求优先精确副本或披露版本差异。GAIA式最终答案正确性不能替代这类来源与过程条件。只有明确每组期待行为并分组保留分母，回答率、恢复率和可靠性才不会混淆。

对照来源：[agentheal](../../../agent-research/2610.39234-agentheal/README.md) · [agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md) · [gaia](../../../agent-research/2311.12983-gaia/README.md)

### 明确配方与改坏任务不是同一种协议变化

AgentPerturb 只改一个输入面，并独立验证目标保持和可解性，配对差值才可归因于该扰动。XStack 的第二阶段却是在同一迁移产物上补主实验配方，锁住入口脚本外代码且不公开目标；它是在区分实验选择错误与迁移错误，不是输入扰动稳健性测量。两者都需要评分者独立于执行 Agent，不能让执行者看到用于判定的隐含目标。

对照来源：[xstack](../../../agent-research/2611.08472-xstack/README.md) · [agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md)

### 历史语义保真与跨栈重训是两种研究交付证据

ARE-bench检验任务接手时是否保留历史决定和工作区材料，严格ISR防止高条目均分掩盖缺一项交付；CSR仍按任务macro。XStack检验跨框架代码在干净全规模重跑、来源判定和权重回载中是否达标。二者都不能把私有判据交给Actor，但任务分母、资源和成功标准不同。ARE的本地scorer接口不是官方任务集接入，XStack资料审查也不是训练迁移已完成。

对照来源：[are-bench](../../../agent-research/2611.14364-are-bench/README.md) · [xstack](../../../agent-research/2611.08472-xstack/README.md)

### 结果相符、过程有效与目标保留是不同的审计问题

AgentHeal关心失败恢复后是否仍引用合法同版本来源并遵守政策；ReproBridge关心一个接近论文的分数是否来自指定实验与统计单位。前者不能凭答案相似替代来源归因，后者不能凭数值兼容替代独立执行审计。它们都要求评价侧标注/参考与actor隔离，也都不能把机械真值表当真实Agent成功率。

对照来源：[reprobridge](../../../agent-research/2611.08452-reprobridge/README.md) · [agentheal](../../../agent-research/2610.39234-agentheal/README.md)

### 可机器检查的证据仍需要先固定要证明什么

AlphaProof Code把获批规格及依赖隔离，阻止模型把secure偷改成恒真再交付合法Lean证明。ReproBridge则预先固定实验与报告统计，阻止得到目标分数后再替换测量。两者都保留人类规格/评价设计责任，但形式证明的逻辑正确性不能替代实验执行完整性，反过来数值复现也不证明程序安全。

对照来源：[alphaproof-code](../../../agent-research/alphaproof-code/README.md) · [reprobridge](../../../agent-research/2611.08452-reprobridge/README.md)

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

### 为什么AgentHeal可以奖励不可恢复任务中的弃答，而AgentPerturb却不能随意把任务扰坏到无解？ {#cross-unrecoverable-is-a-different-contract}

??? note "展开答案与例子"

    **答案：** 两者预先定义的目标不同：AgentPerturb测同目标配对稳健性，要求仍可解；AgentHeal测资源恢复，明确区分可恢复与不可恢复，后者要求准确诊断并诚实停止或请求用户协助。不能将该弃答算成终局答题准确率，也不能用总分掩盖不同regime的行为。

    **教学例子：** 教学例：唯一文件消失且无合法备份时，说明障碍而不编造内容是可靠性成功；同一情况若作为仍应答出数值的扰动题，就是改坏了题。

    对照来源：[agentheal](../../../agent-research/2610.39234-agentheal/README.md) · [agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md) · [gaia](../../../agent-research/2311.12983-gaia/README.md)

### 同一个迁移在 XStack 第一阶段失败、第二阶段通过，为什么不能当作 AgentPerturb 式的稳健性配对分数？ {#cross-aligned-recipe-not-robustness-pair}

??? note "展开答案与例子"

    **答案：** XStack 只对失败单元追加配方并约束修改范围，判的是同一迁移在正确配方下能否重训达标；AgentPerturb 对共同任务的干净和扰动输入分别执行且保持目标与可解性。分母、干预和通过条件不同。

    **教学例子：** 教学例：原来误跑较小数据集，澄清后换入口并全规模达标，说明该迁移路径可运行，不说明 Agent 能应对不同工具说明扰动。

    对照来源：[xstack](../../../agent-research/2611.08472-xstack/README.md) · [agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md)

### 脚本能恢复训练、checklist大部分通过，为何仍可能同时没通过ARE式交接和XStack式迁移？ {#cross-history-checklist-versus-clean-retraining}

??? note "展开答案与例子"

    **答案：** ARE的严格ISR要求所有有效历史和材料条目通过，恢复运行不能抵消改错原loss的失败；XStack还要求独立完整重训、反作弊核验及原框架权重加载。部分条目通过或一次执行成功都不覆盖另一套证据。

    **教学例子：** 教学例：为了让训练跑起来删掉匹配loss，可能仍生成日志和checkpoint，却违反历史方法要求，也不能证明跨栈复现达标。

    对照来源：[are-bench](../../../agent-research/2611.14364-are-bench/README.md) · [xstack](../../../agent-research/2611.08472-xstack/README.md)

### AgentHeal的任务成功与ReproBridge的数值兼容，为什么都不能只看最终输出是否漂亮？ {#cross-cross-reproduction-compatibility-versus-goal-preservation}

??? note "展开答案与例子"

    **答案：** AgentHeal还要求合法来源版本与逐动作合规；ReproBridge还要求指定测量程序、统计单位与可反驳的执行审计。输出好看可能分别掩盖旧版本替换或复制旧分数，评价者也不能把这些答案/参考交给actor。

    **教学例子：** 教学例：拿旧版论文答对一句话不等于恢复指定新版本；把已发表MSE抄进新JSON也不等于训练了模型。

    对照来源：[reprobridge](../../../agent-research/2611.08452-reprobridge/README.md) · [agentheal](../../../agent-research/2610.39234-agentheal/README.md)

### Lean能检查证明，为什么AlphaProof仍需要人类审规格；ReproBridge又为何不能只检查分数？ {#cross-cross-proof-checking-versus-execution-audit}

??? note "展开答案与例子"

    **答案：** 内核只证明给定命题，弱化规格依然可能得到有效证明；数值兼容只说明数值落在区间，复制或错误统计也可能相符。前者固定规格及传递定义，后者固定实验程序与证据链，均不能以漂亮最终产物跳过输入合同。

    **教学例子：** 教学例：把secure定义为True后证明成功，与把旧结果复制成新JSON后分数兼容，都可能表面通过一个窄检查，却没有完成原要求。

    对照来源：[alphaproof-code](../../../agent-research/alphaproof-code/README.md) · [reprobridge](../../../agent-research/2611.08452-reprobridge/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-11** · 增加形式规格保真与传递依赖门控维度；明确高成本reference无本地证明能力，不用regex或玩具定理替代官方验证。

涉及：[alphaproof-code](../../../agent-research/alphaproof-code/README.md)

**2026-11-11** · 补充独立科研复现的统计兼容与证据完整性维度，明确相近分数不是执行证明；未改变现有来源/政策审计边界。

涉及：[reprobridge](../../../agent-research/2611.08452-reprobridge/README.md)

**2026-11-11** · 加入ARE-bench，强调真实会话/workspace与私有rubric隔离、严格ISR及task-macro CSR；与XStack独立重训证据分开。仅交CPU评分接口，官方任务包和多frontier长任务评测均未运行。

涉及：[are-bench](../../../agent-research/2611.14364-are-bench/README.md) · [xstack](../../../agent-research/2611.08472-xstack/README.md)

**2026-11-06** · 补入 XStack，将真实跨框架执行、隔离来源判定和权重回载与输入稳健性分开。主实验 TPU 成本高，仅资料审查，不把 Appendix G 或静态合同当成本地能力结果。

涉及：[xstack](../../../agent-research/2611.08472-xstack/README.md) · [agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md)

**2026-11-04** · 补AgentHeal，并对照AgentPerturb与GAIA解释不可恢复regime、目标版本、来源归因与政策乘积。区分精确副本的交集条件与其他版本的子集条件，独立gold标注仅给评价者；本地TS=0.5是四条合成真值表，不是Agent准确率。855任务×13模型完整矩阵高成本不复现、审查DONE。

涉及：[agentheal](../../../agent-research/2610.39234-agentheal/README.md) · [agent-perturb](../../../agent-research/2610.21624-agent-perturb/README.md) · [gaia](../../../agent-research/2311.12983-gaia/README.md)

**2026-10-27** · 首版：比较终局能力、单目标扰动、用户合同、失败重试会计、四臂归因与簇级选择性证书。

覆盖 43 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 48 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [AgentHeal: Evaluating Goal-Preserving Resource Recovery of Web Agents under Access Barriers](../../../agent-research/2610.39234-agentheal/README.md)
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
- [XStack: A Benchmark for ML Repo Migration](../../../agent-research/2611.08472-xstack/README.md)
- [ReproBridge: Building Reproducibility into ML Research Artifacts](../../../agent-research/2611.08452-reprobridge/README.md)
- [ARE-bench: Benchmarking Agents&#x27; Research Ability in Real-World Researcher Sessions and Workspaces](../../../agent-research/2611.14364-are-bench/README.md)
- [AlphaProof Code: Verifying Signal&#x27;s Security at the Machine-Code Level](../../../agent-research/alphaproof-code/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/evaluation-and-reliability.md) · [返回全部精读卡片](../index.md)
