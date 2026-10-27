---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 排序不变、概率校准与完整集合恢复，是三种不同承诺

[结构化决策](../index.md) · 更新 2026-10-27 · 3 篇主题资料 / 3 篇重点对照

Prism-1约束分数的计算依赖，JEV请求审计设计配对干预，多正确选项审计检查分布能否恢复正确集合。三者分别回答“架构保证什么”“实验改变了什么”“评价目标是什么”，不能用合法输出或一次top-1准确率代替。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/system-one/candidate-invariance.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：独立选项打分的架构条件 · 问题、证据与候选资格的干预范围 · 相对赔率、绝对概率与集合恢复指标

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Prism-1: Position- and Rival-Independent Scoring for System One Models](../../../foundation-models/2610.22066-prism-1/README.md) · [原始来源](https://arxiv.org/abs/2610.22066)<br>章节：背景与主要改动、核心公式、代码映射与边界 | 每个选项只看共享状态、当前问题和自身block，各block重置相同起始位置；独立yes/no对数赔率再做选项softmax。 | 保护固定证据下旧选项的相对赔率，允许新候选成为赢家；不保证准确率或抗共享上下文注入，不适合“以上皆非”等跨选项语义。 |
| [The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval](../../../system-one/2610.14631-request-audit/README.md) · [原始来源](https://arxiv.org/abs/2610.14631)<br>章节：背景与主要改动、核心公式、已验证结果与边界 | 将新增问题、新增显示证据、新增候选资格分成三类配对干预，分别测翻转、ties、条件概率与允许标签质量。 | 测量依赖固定公共输入和隔离评分标签；证据真的改变时不能要求答案保持不变。本地审计接口与原文付费模型能力结论分开。 |
| [When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models](../../../system-one/2610.29217-jev-multicorrect/README.md) · [原始来源](https://arxiv.org/abs/2610.29217v1)<br>章节：背景与主要改动、方法与本地协议、原文结论与复现边界 | 同时观察正确项概率差、排序、阈值后exact-set恢复和独立二元校准，区分一份类别分布与逐项正确概率。 | 全部正确项排在前面仍可能无法用阈值完整恢复集合；阈值要在validation选定。原文模型响应未公开，本地只验证评分/隔离合同。 |

</div>

## 取舍分析 {#analysis}

### 先冻结证据，再讨论独立性

Prism-1的不变性以共享状态和问题不变为前提。请求审计中，只增加候选资格必须保留全部显示证据；若同时添加了一段能解释问题的新材料，分数变化可能是合理的信息更新。审计应比较A/B条件概率或赔率，不能把softmax分母扩大导致的绝对概率下降算成偏好翻转。

对照来源：[prism-1](../../../foundation-models/2610.22066-prism-1/README.md) · [jev-request-audit](../../../system-one/2610.14631-request-audit/README.md)

### 独立分数也不会自动变成多标签概率

即使Prism-1让每个候选的分数不受其他选项干扰，选项softmax仍把总质量分配为一。多正确选项审计关心的是恢复整个正确集合，正确项之间依然会竞争质量；因此排序稳定不能推出每个正确项都过同一阈值，更不能推出候选份额已经校准为逐项正确率。

对照来源：[prism-1](../../../foundation-models/2610.22066-prism-1/README.md) · [jev-multicorrect](../../../system-one/2610.29217-jev-multicorrect/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 加入无关C后，A的概率下降，是否已经违反Prism-1想保护的性质？ {#cross-denominator-not-reversal}

??? note "展开答案与例子"

    **答案：** 未必。先固定证据，比较A相对B的赔率或A/(A+B)。加入C会增加总分母，A的绝对份额可正常下降；只有旧二者相对偏好发生变化，才需要排查跨选项信息或位置依赖。请求审计正是将这类归一化效应与新增证据分开。

    **教学例子：** 示意：A、B指数分数为2和1时A占2/3；加入分数5的C后A占2/8，但A/B始终为2，没有发生旧候选偏好翻转。

    对照来源：[prism-1](../../../foundation-models/2610.22066-prism-1/README.md) · [jev-request-audit](../../../system-one/2610.14631-request-audit/README.md)

### 所有正确项都排在错误项之前，为什么仍不能证明多选题已经解决？ {#cross-ranking-versus-set-recovery}

??? note "展开答案与例子"

    **答案：** 排序只要求相对次序，多选还要确定取多少项。候选softmax把一个单位质量分给全部选项，第二个正确项可能分到很低份额；固定阈值可能漏选，降低阈值又可能纳入错误项。必须另测exact-set恢复，并用独立验证集选择阈值。

    **教学例子：** 示意：A、B正确，分数份额为0.60、0.25、0.15。排序完全正确，但阈值0.4只返回A；top-1正确也没有揭示B被漏掉。

    对照来源：[jev-multicorrect](../../../system-one/2610.29217-jev-multicorrect/README.md) · [prism-1](../../../foundation-models/2610.22066-prism-1/README.md)

### 为什么“把C加入候选”和“把描述C的证据加入上下文”不能放在同一组独立性测试里？ {#cross-evidence-versus-eligibility}

??? note "展开答案与例子"

    **答案：** 前者改变可选动作集合，后者改变模型知道的事实。Prism-1只约束固定共享证据下的选项独立分数；请求审计将两种干预分开，才能判断变化来自竞争关系还是合理取证。多正确项的评分也必须在固定正确集合和输入条件下解释。

    **教学例子：** 示意：工具C原本已完整显示，只把它从不可选变可选是资格变化；补上一句“C支持离线运算”则提供了新信息，A/B偏好可随任务证据改变。

    对照来源：[jev-request-audit](../../../system-one/2610.14631-request-audit/README.md) · [prism-1](../../../foundation-models/2610.22066-prism-1/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较prism-1、jev-request-audit、jev-multicorrect，梳理独立选项打分的架构条件与问题、证据与候选资格的干预范围，并补充跨论文问答。

涉及：[jev-multicorrect](../../../system-one/2610.29217-jev-multicorrect/README.md) · [jev-request-audit](../../../system-one/2610.14631-request-audit/README.md) · [prism-1](../../../foundation-models/2610.22066-prism-1/README.md)

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 3 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models](../../../system-one/2610.29217-jev-multicorrect/README.md)
- [The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval](../../../system-one/2610.14631-request-audit/README.md)
- [Prism-1: Position- and Rival-Independent Scoring for System One Models](../../../foundation-models/2610.22066-prism-1/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/system-one/candidate-invariance.md) · [返回全部精读卡片](../index.md)
