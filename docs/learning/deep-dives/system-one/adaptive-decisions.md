---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 追加推理、跨语言路由与持续反馈，各在哪个时刻改变决策？

[结构化决策](../index.md) · 更新 2026-11-20 · 6 篇主题资料 / 6 篇重点对照

按需决策有三条时间轴：Selective Reasoning在单题内分配推理和读取预算，跨语言级联在不同后端间分配请求，Jev-DLC用已发生反馈影响后续请求。能力评测提供基线边界，却不自动证明任何控制策略有效。所有选择都要在当前测试目标揭晓之前冻结或作出。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/system-one/adaptive-decisions.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：单请求内控制与请求之间的状态更新 · 熵、校准、错误排序与任务准确率 · 验证集选阈值及测试时间的信息隔离 · 原文能力、统计复算与本地真实模型测量

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop](../../../system-one/2610.19644-selective-reasoning/README.md) · [原始来源](https://arxiv.org/abs/2610.19644)<br>章节：背景与主要改动、核心公式、复现边界与成本结论 | 共享reader读空前缀和推理中途分布；benefit gate、读取trigger、接受/停止阈值分工控制推理。 | 低熵只代表集中，预算耗尽须另记budget-forced；完整在线实验未复现，本地控制器和作者统计复算不等于重新生成答案。 |
| [Jev-DLC: Decision-Level Continual Learning from Typed Feedback](../../../system-one/2610.31521-jev-dlc/README.md) · [原始来源](https://arxiv.org/abs/2610.31521v1)<br>章节：背景与主要改动、双通道、PA-I与可靠性、本地复现与边界 | 冻结scorer之上维护保守/响应双通道，PA-I更新修正方向，以反馈前预测误差调整可靠性。 | 不保留完整交互文本，但仍依赖外部表示与固定词表；只能在提交本次选择后接收反馈，更新不得回填当前成功。本地为随机外部logits的状态组件。 |
| [Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages](../../../system-one/2610.14112-regional-transfer/README.md) · [原始来源](https://arxiv.org/abs/2610.14112)<br>章节：背景与主要改动、核心公式、已验证结果与边界 | 分别测跨语言准确率、概率校准与错误排序；按validation宏F1选低置信度路由比例，再冻结用于test。 | 温度校准不保证把错题排到最前，翻译也非无条件有效；同句不同语言须聚类统计，不能当独立样本扩大证据。 |
| [Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks](../../../system-one/2610.11978-jev-capability/README.md) · [原始来源](https://arxiv.org/abs/2610.11978)<br>章节：背景与主要改动、数据与评测契约、本地验证与边界 | 规范化知识、推理和多语言有限候选任务，以隔离标签评估一次选择，并分开供应商引用与实际测量。 | 它是评测协议而非自适应算法；本地NanoJev的ARC结果不代表闭源Jev，13类接口支持也不表示13任务全量已测。 |
| [Measure Before You Train: Typed Decision Models vs. a Classical Baseline vs. a Generative LLM for Routing a Personal Multilingual Inbox](../../../system-one/2610.32955-typed-inbox-protocol/README.md) · [原始来源](https://arxiv.org/abs/2610.32955v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | 先冻结可见输入与线程切分，再按动作成本选择validation阈值；本地只含L0二元接口。 | Jev能力入口运行独立问题／候选并按gold计分；Typed Inbox关注多开关组合后的行动损失与私有邮箱分布。线程隔离不能被三seed替代，简单阈值也不是原文完整模型。 |
| [Stop Going in Circles:Loop-Triggered Routing for System 1 Decision Agents](../../../system-one/2611.25363-looproute/README.md) · [原始来源](https://arxiv.org/abs/2611.25363v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | System One决策模型能快速选动作，但局部选择正确不保证长任务完成。LoopRoute默认把控制权交给冻结Jev；只有同一公开状态下的同一动作已经执行两次，才拦截第三次提案，让LLM按实际环境反馈接管最多两步，然后无额外恢复测试地交回Jev。后续再次卡住可再次接管。 | Selective Reasoning依据共享读出、benefit gate和答案分布确定性，决定何时生成/读取/停止推理；LoopRoute依据真实环境状态-动作复现，决定是否把控制权短暂交给另一policy。前者的高certainty不代表环境已进展，后者的未重复也不保证动作正确。 |

</div>

## 取舍分析 {#analysis}

### 算力反馈与用户反馈不能混作一种循环

Selective Reasoning在答案未知时观察自己的中间分布，决定是否再生成或读取；Jev-DLC在一个请求结束后接收accept/revoke，改变下一请求状态。前者不需要当前gold来决定停止，后者虽需要反馈也不得回头改本题成绩。二者可以组合，但必须分别记录单题预算和跨题适配后的泛化。

对照来源：[selective-reasoning](../../../system-one/2610.19644-selective-reasoning/README.md) · [jev-dlc](../../../system-one/2610.31521-jev-dlc/README.md)

### 概率好看与会挑难题不同

跨语言迁移用ECE/Brier衡量概率校准，用风险覆盖等指标衡量错误排序，Selective Reasoning的归一化熵则只读当前分布集中程度。一个温度能改善校准，却不一定改善错题排序；能力评测中知识强、数学弱也不能直接变成逐题启动规则。应在验证集确定路由和预算，再独立测量不同任务与语言。

对照来源：[jev-regional-transfer](../../../system-one/2610.14112-regional-transfer/README.md) · [selective-reasoning](../../../system-one/2610.19644-selective-reasoning/README.md) · [jev-capability](../../../system-one/2610.11978-jev-capability/README.md)

### 从“选对标签”到“少漏重要邮件”还隔着行动策略

Jev能力评测要求请求不带标准答案，并记录真实后端和数据覆盖。Typed Inbox进一步指出预测字段会组合为真实动作，错误的成本不对称；相同accuracy不代表同样漏信风险。先冻结邮箱可见快照，整线程切分，再在训练／validation内选阈值。原文的类别分层CV和完整三开关成本没有被局部二元接口替代。

对照来源：[typed-inbox-protocol](../../../system-one/2610.32955-typed-inbox-protocol/README.md) · [jev-capability](../../../system-one/2610.11978-jev-capability/README.md)

### LoopRoute：在重复执行前拦截，让LLM只接管两步

状态key不含不断增长的history或step。ALFWorld用已确认事实和排序后的可行动作；MapReader用当前动作回应、房间描述和inventory；TextWorld用房间、inventory和候选ID到命令映射。ALFWorld只累计决策模型执行，新事实或接管结束会清空；另外两者累计两种policy的执行并保持到episode结束。被拦截提案既不占环境步，也不更新计数。负控区分相同动作但不同状态、未执行提案和真实执行；拒绝未提交transition就再次route，防止重试被当执行。测试ALFWorld不计LLM动作、接管结束清空，以及MapReader/TextWorld计两种动作且不清空。终止立即结束接管；共享key拒绝history/step/gold附加字段。

对照来源：[looproute](../../../system-one/2611.25363-looproute/README.md) · [selective-reasoning](../../../system-one/2610.19644-selective-reasoning/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### Selective Reasoning的中途读取与Jev-DLC的revoke更新，为什么需要不同的评价时钟？ {#cross-within-versus-between-requests}

??? note "展开答案与例子"

    **答案：** 中途读取发生在当前目标未揭晓时，衡量追加算力是否改变当前选择；revoke已经揭示旧选择应改为什么，只能更新后续请求。若把反馈后的重答算成本题成功，就把已知标签混进预测，无法证明持续适配能力。

    **教学例子：** 示意：第10题先选A，再收到“改B”。DLC可据此帮助第11题；第10题仍按最初A计分。第10题推理到一半读取分布则尚未收到该反馈。

    对照来源：[selective-reasoning](../../../system-one/2610.19644-selective-reasoning/README.md) · [jev-dlc](../../../system-one/2610.31521-jev-dlc/README.md)

### 概率校准改善后，为什么仍要单独测试低置信度路由和熵停止？ {#cross-calibration-does-not-route-errors}

??? note "展开答案与例子"

    **答案：** 校准检查概率与总体正确频率是否对应，路由还要求错题在低置信度端聚集；熵停止只说明某次分布集中。跨语言迁移分别测这些性质，Selective Reasoning再用验证时确定的控制规则分配预算，不能把更低ECE直接当作更好的早停或fallback策略。

    **教学例子：** 示意：两个模型在各自0.8置信度分桶中都答对80%，但整个置信度排序中，一个把更多错误集中在最低分段，另一个把错误分散到各段；单看这个分桶不能判断级联能节省多少成本。

    对照来源：[jev-regional-transfer](../../../system-one/2610.14112-regional-transfer/README.md) · [selective-reasoning](../../../system-one/2610.19644-selective-reasoning/README.md)

### 发现某语言或数学任务较弱后，能否在test上试许多路由比例再报告最好的策略？ {#cross-validation-budget-versus-test}

??? note "展开答案与例子"

    **答案：** 不能。能力评测提示要分任务查看覆盖与误差，但不能把test变成策略选择集。跨语言级联先在validation宏F1下选最小达标路由比例，再固定评测；同样，是否启动推理和熵阈值也应预先冻结，保留预算被迫结束的情况。

    **教学例子：** 示意：验证集选择把20%最低置信度请求交给强模型；测试即使30%看起来更好，也不能把30%冒充原定策略，除非另开独立确认评测。

    对照来源：[jev-regional-transfer](../../../system-one/2610.14112-regional-transfer/README.md) · [jev-capability](../../../system-one/2610.11978-jev-capability/README.md) · [selective-reasoning](../../../system-one/2610.19644-selective-reasoning/README.md)

### 把邮箱noise阈值在held-out邮件上调到最低成本，能当Jev能力评测的公平对比吗？ {#cross-cross-nov18-typed-inbox-protocol}

??? note "展开答案与例子"

    **答案：** 不能。它把测试标签用于选择策略，且动作成本不同于独立选择accuracy。必须提前固定切分、成本和阈值选择规则，冻结后只评分；本地也没有调用Jev。

    **教学例子：** 教学例：看到漏掉一封重要信后回调阈值，会改变刚评过样本的决策，不能再当未见测试。

    对照来源：[typed-inbox-protocol](../../../system-one/2610.32955-typed-inbox-protocol/README.md) · [jev-capability](../../../system-one/2610.11978-jev-capability/README.md)

### LoopRoute和Selective Reasoning都省推理，证据一样吗？ {#cross-cross-nov20-looproute}

??? note "展开答案与例子"

    **答案：** 不一样。一个看环境中的重复执行，另一个看冻结读出与推理收益/确定性；重复不是低置信度，高置信度也不等于任务有进展。

    **教学例子：** 教学例：模型非常确信地反复开一个锁住的门，仍应触发循环路由。

    对照来源：[looproute](../../../system-one/2611.25363-looproute/README.md) · [selective-reasoning](../../../system-one/2610.19644-selective-reasoning/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-20** · 本地执行公开状态key、pending decision/实际执行分离、第三次提案拦截、准确两步接管及各benchmark计数规则。只接受显式公开字段，不接收gold、奖励或成功标签；new_information由可信外部ALFWorld适配器提供，本地不假装语义核实事实。没有Jev/LLM backend、benchmark环境或实际API请求；控制轨迹只证明路由规则，不证明任务成功率。 完整实验高成本不复现。

涉及：[looproute](../../../system-one/2611.25363-looproute/README.md) · [selective-reasoning](../../../system-one/2610.19644-selective-reasoning/README.md)

**2026-11-18** · 先冻结可见输入与线程切分，再按动作成本选择validation阈值；本地只含L0二元接口。 完整实验高成本不复现，局部协议不作能力或Evolve证据。

涉及：[typed-inbox-protocol](../../../system-one/2610.32955-typed-inbox-protocol/README.md) · [jev-capability](../../../system-one/2610.11978-jev-capability/README.md)

**2026-10-27** · 首版：比较selective-reasoning、jev-dlc、jev-regional-transfer、jev-capability，梳理单请求内控制与请求之间的状态更新与熵、校准、错误排序与任务准确率，并补充跨论文问答。

涉及：[jev-capability](../../../system-one/2610.11978-jev-capability/README.md) · [jev-dlc](../../../system-one/2610.31521-jev-dlc/README.md) · [jev-regional-transfer](../../../system-one/2610.14112-regional-transfer/README.md) · [selective-reasoning](../../../system-one/2610.19644-selective-reasoning/README.md)

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 6 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks](../../../system-one/2610.11978-jev-capability/README.md)
- [Jev-DLC: Decision-Level Continual Learning from Typed Feedback](../../../system-one/2610.31521-jev-dlc/README.md)
- [Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages](../../../system-one/2610.14112-regional-transfer/README.md)
- [Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop](../../../system-one/2610.19644-selective-reasoning/README.md)
- [Measure Before You Train: Typed Decision Models vs. a Classical Baseline vs. a Generative LLM for Routing a Personal Multilingual Inbox](../../../system-one/2610.32955-typed-inbox-protocol/README.md)
- [Stop Going in Circles:Loop-Triggered Routing for System 1 Decision Agents](../../../system-one/2611.25363-looproute/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/system-one/adaptive-decisions.md) · [返回全部精读卡片](../index.md)
