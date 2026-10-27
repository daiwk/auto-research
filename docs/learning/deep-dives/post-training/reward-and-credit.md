---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 奖励从哪里来，信用才该分到哪里

[LLM 后训练](../index.md) · 更新 2026-10-27 · 36 篇主题资料 / 6 篇重点对照

过程标签、最终结果、模型自置信与回溯归因是不同证据。逐步PRM、MRTPO、TACO和MART-GRPO分别做标签获取、奖励定位、正信用降权和失败后缀过滤；INTUITOR则改用内在分布信号，不能把它当外部正确性验证器。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/post-training/reward-and-credit.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：证据来源：人工步骤、正确续写比例、verifier、内在分布 · 信用粒度：步骤、token、奖励维度、动作chunk · 修改方式：增加监督、重分配、降权、屏蔽 · 可见时间：生成时信息与事后回看

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Let&#x27;s Verify Step by Step](../../../post-training/2305.20050-process-supervision/README.md) · [原始来源](https://arxiv.org/abs/2305.20050)<br>章节：背景与主要改动、核心公式、复现边界 | 训练逐步PRM并优先标注不确定步骤，直接获得过程质量监督。 | 依赖步骤标注与覆盖；本地候选机制实验不代表原文大规模过程评测。 |
| [Math-Shepherd](../../../post-training/2312.08935-math-shepherd/README.md) · [原始来源](https://arxiv.org/abs/2312.08935)<br>章节：背景与主要改动、核心公式、复现边界 | 从中间步骤采样续写，以最终答案正确比例构造自动step label。 | 减少人工逐步标签，但标签依赖续写策略与采样预算；本地未复刻原文训练规模。 |
| [Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL](../../../post-training/2610.21439-mrtpo/README.md) · [原始来源](https://arxiv.org/abs/2610.21439v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 固定采样策略，在全verifier上下文与留一信息块下重放，用全词表JSD定位各奖励相关token。 | 守住奖励总信用但依赖信息块构造；完整SQL/工具实验成本过高未复现，当前为L1梯度诊断。 |
| [TACO](../../../post-training/2607.07976-taco/README.md) · [原始来源](https://arxiv.org/abs/2607.07976)<br>章节：背景与主要改动、核心公式、复现边界 | 按局部tail risk只降低高风险token的正优势，负优势完整保留。 | 防止答对轨迹把局部错误一并强化；本地surprisal代理未复刻原文上下文风险预测器。 |
| [When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning](../../../post-training/2610.32431-mart-grpo/README.md) · [原始来源](https://arxiv.org/abs/2610.32431v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 事后事件VLM定位最后未恢复错误，过滤失败边界之后的信用，保留原组优势和原分母。 | 回溯边界不自动满足理想stopping-time条件；完整机器人/VLM训练成本过高未复现，A100证据仅验收L1组件。 |
| [INTUITOR](../../../post-training/2505.19590-intuitor/README.md) · [原始来源](https://arxiv.org/abs/2505.19590)<br>章节：背景与主要改动、核心公式、复现边界 | 以逐token全词表KL(U∥policy)的长度平均作为self-certainty内在奖励。 | 不需外部verifier但置信不保证正确；本地仍是相反KL方向的候选诊断，尚未实现定义性奖励。 |

</div>

## 取舍分析 {#analysis}

### 自动过程标签不是无条件的步骤真理

人工过程监督直接询问某一步是否合理；Math-Shepherd估计的是从这一步继续采样后答对的比例。后者还混入当前续写器能否恢复、能否完成后续推理的信息。INTUITOR更进一步只读模型分布，连最终答案正确性都不是其原生证据；三者的标签含义应先分清，再比较成本。

对照来源：[process-supervision](../../../post-training/2305.20050-process-supervision/README.md) · [math-shepherd](../../../post-training/2312.08935-math-shepherd/README.md) · [intuitor](../../../post-training/2505.19590-intuitor/README.md)

### 同叫信用过滤，作用对象和守恒量却不同

TACO只衰减正优势，避免正确整句污染局部低质量token；MART-GRPO在失败episode中遮去事后错误边界后的信用，原分母不变；MRTPO依据不同奖励信息块重分配正负信用，并控制总量与重分配幅度。它们不能都实现成“删掉可疑token后对剩余token求均值”。

对照来源：[taco](../../../post-training/2607.07976-taco/README.md) · [mart-grpo](../../../post-training/2610.32431-mart-grpo/README.md) · [mrtpo](../../../post-training/2610.21439-mrtpo/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### Math-Shepherd某一步续写成功率低，等同于人工PRM判定这一步逻辑错误吗？ {#cross-step-truth-versus-continuation}

??? note "展开答案与例子"

    **答案：** 不等同。续写成功率还受后续采样能力和预算影响，正确中间步骤也可能因后续难而低分；人工过程标签则直接评价该步。两种证据可以互补，却不能把自动标签无条件称为逻辑真值，评估时也要隔离训练用标准答案与受测模型输入。

    **教学例子：** 教学例子：前面列式正确，但模型不擅长后面的计算，多次续写都失败；这不能单独证明列式本身错。

    对照来源：[process-supervision](../../../post-training/2305.20050-process-supervision/README.md) · [math-shepherd](../../../post-training/2312.08935-math-shepherd/README.md)

### TACO与MART-GRPO都想少罚无辜步骤，为什么不能统一成删token后重新平均？ {#cross-filter-denominator}

??? note "展开答案与例子"

    **答案：** TACO保留负信用，只降低高风险正信用；MART-GRPO才针对失败后缀置零，并明确保留原有效action-token分母。删后重新平均会放大剩余项，改变目标。MRTPO又要求按奖励相关性保留信用总量，因此统一的“先删再均分”会抹掉三者定义。

    **教学例子：** 教学例子：原轨迹十个token中遮掉后四个，按六而非十归一，会使剩余负项更强；这不是MART原公式。

    对照来源：[taco](../../../post-training/2607.07976-taco/README.md) · [mart-grpo](../../../post-training/2610.32431-mart-grpo/README.md) · [mrtpo](../../../post-training/2610.21439-mrtpo/README.md)

### INTUITOR分布越尖锐，与Math-Shepherd更常续写答对，能视作同一种奖励增加吗？ {#cross-confidence-is-not-verification}

??? note "展开答案与例子"

    **答案：** 不能。INTUITOR读取KL(U∥policy)，反映全词表分布形状；Math-Shepherd读取最终正确性频率。模型可以自信地错，且把KL方向反过来会得到另一种量。本地INTUITOR尚未实现原方向和逐词全词表计算，不能用其候选指标给两方法排能力名次。

    **教学例子：** 教学例子：模型每次都坚定输出同一个错误数值，分布可很尖锐，但对照标准答案的续写成功率仍为零。

    对照来源：[intuitor](../../../post-training/2505.19590-intuitor/README.md) · [math-shepherd](../../../post-training/2312.08935-math-shepherd/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较人工/自动过程标签、MRTPO奖励定位、TACO正信用、MART失败后缀过滤与INTUITOR内在奖励；已阅36篇摘要，精读6篇。

覆盖 36 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 36 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning](../../../post-training/2610.32431-mart-grpo/README.md)
- [MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning](../../../post-training/2610.23245-mge-po/README.md)
- [Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense](../../../post-training/2610.21404-tag-reward-gating/README.md)
- [Learning to Reason with Selective Internal Feedback](../../../post-training/2610.21392-sif/README.md)
- [Progress Reward Model for Reinforcement Learning via Large Language Models](../../../post-training/2610.22056-progress-reward/README.md)
- [OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering](../../../post-training/2610.21345-opcredit/README.md)
- [Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL](../../../post-training/2610.21439-mrtpo/README.md)
- [KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents](../../../post-training/2610.22331-knowgpo/README.md)
- [Training Reasoning Models to Generate Diverse Scientific Ideas](../../../post-training/2610.22324-diverge-ideation/README.md)
- [When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO](../../../post-training/2610.20089-rap-walk/README.md)
- [Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction](../../../reproductions/2610.13672-upturn/README.md)
- [SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents](../../../reproductions/2610.13157-soar/README.md)
- [Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards](../../../post-training/2610.11519-residual-advantage/README.md)
- [Token-Level Video Reinforcement Learning](../../../post-training/2610.01973-tvrl/README.md)
- [My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning](../../../post-training/2610.01161-my-fault/README.md)
- [CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning](../../../post-training/2610.02039-carm/README.md)
- [T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning](../../../post-training/2610.00388-t2spo/README.md)
- [SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning](../../../post-training/2610.00838-sharpo/README.md)
- [PACT: From Credit Assignment to Critic Alignment](../../../post-training/2609.26355-pact/README.md)
- [TIAO: Token Importance-Aware Policy Optimization for Text Summarization](../../../post-training/2609.16748-tiao/README.md)
- [SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning](../../../post-training/2608.26550-spear/README.md)
- [V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning](../../../post-training/2608.25580-v-rubrics/README.md)
- [SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning](../../../post-training/2608.23493-srpo/README.md)
- [Learn What&#x27;s Left, Not What&#x27;s Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization](../../../post-training/2608.16072-sa-mrpo/README.md)
- [Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL](../../../post-training/2608.11669-rubric-dropout/README.md)
- [RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction](../../../post-training/2608.06310-rrc/README.md)
- [ADRS](../../../post-training/2608.03223-adrs/README.md)
- [SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning](../../../post-training/2607.26873-serpo/README.md)
- [CoRT](../../../post-training/2607.25659-cort/README.md)
- [TCR](../../../post-training/2607.19824-tcr/README.md)
- [Co-Evolving LLM Evaluators and Policies via DynamicRubric](../../../reproductions/2607.20083-dynamic-rubric/README.md)
- [TACO](../../../post-training/2607.07976-taco/README.md)
- [SCAR: Shapley Credit Assignment for More Efficient RLHF](../../../post-training/2505.20417-scar-shapley-credit/README.md)
- [INTUITOR](../../../post-training/2505.19590-intuitor/README.md)
- [Math-Shepherd](../../../post-training/2312.08935-math-shepherd/README.md)
- [Let&#x27;s Verify Step by Step](../../../post-training/2305.20050-process-supervision/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/reward-and-credit.md) · [返回全部精读卡片](../index.md)
