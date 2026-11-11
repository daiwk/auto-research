---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 奖励从哪里来，信用才该分到哪里

[LLM 后训练](../index.md) · 更新 2026-11-11 · 41 篇主题资料 / 11 篇重点对照

过程标签、最终结果、模型自置信与回溯归因是不同证据。逐步PRM、MRTPO、TACO和MART-GRPO分别做标签获取、奖励定位、正信用降权和失败后缀过滤；INTUITOR则改用内在分布信号，不能把它当外部正确性验证器。 CONCUR另处理奖励维度之间的优先级，把门控辅助优势投影到主奖励保序锥；这不是沿时间轴分配token信用。

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
| [CONCUR: Concordant Auxiliary Rewards for Multi-Task, Multi-Reward Reinforcement Learning](../../../post-training/2610.36437-concur/README.md) · [原始来源](https://arxiv.org/abs/2610.36437v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 组内先标准化，再把门控辅助分数作最近保序投影；到顶约束按T/A策略处理，最后整batch白化。 | 主奖励以下的并列不强行相等，投影后不重新标准化；未门控分量仍可能反转排序。完整32GPU训练不复现，本地仅优势估计器。 |
| [Density-Aware Reward Scaling: A Reinforcement Learning Framework for Reward-Proportional Sampling](../../../post-training/2611.04792-dars/README.md) · [原始来源](https://arxiv.org/abs/2611.04792)<br>章节：背景与主要改动、核心公式、检查与负控 | 同prompt组内对结果表示计算含self的Gaussian KDE，以非负reward除以density后再标准化，原GRPO目标不变。 | 终局结果拥挤度不是token置信或奖励优先级；重复点在窄带宽仍计多次，原reward常数不代表缩放后常数。std约定和零方差策略显式，L1不证明已学到奖励比例分布。 |
| [EmoReward: Self-Evolving Reward Calibration for Emotional Video Generation RL](../../../post-training/2611.06518-emoreward/README.md) · [原始来源](https://arxiv.org/abs/2611.06518)<br>章节：背景与主要改动、核心公式、诊断与边界 | 先用当前视频的有效证据门控决定哪些评分能进入融合，再用完成轮的原始分数与结果相关性倾斜各通道权重。训练轮之间拟合一次，下一轮只读。 | 需要已完成的参考轮，相关性依赖 VideoAlign 代理结果，不等同于独立情绪偏好。CPU 只验收分配，未运行视觉评分器或完整生成训练。 |
| [MaxIM: Maximally Informative Incremental Summarization via Reinforcement Learning](../../../post-training/2611.12825-maxim/README.md) · [原始来源](https://arxiv.org/abs/2611.12825v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 以冻结critic的conditional/null teacher-forced log-ratio分别测摘要的目标信息与前向历史支持，再经中心化sigmoid、1-gamma尺度与退火构成跨turn return。 | 生成奖励信号而非重分配已有token信用；特权目标只能用于奖励端，不得给被评估摘要器读。近似critic与非线性shaping不是事实或最优策略保证；本地不训练Gemini。 |
| [Margin-Guided Token Credit for Reinforcement Learning with Verifiable Rewards](../../../post-training/2611.14015-mcpo/README.md) · [原始来源](https://arxiv.org/abs/2611.14015v1)<br>章节：核心公式、原文结果与限制、结果、负控与边界 | 用温度后old-policy top1-top2 margin构造截断线性不确定度，按优势符号指数加权，再按响应内有效token均值归一，保持平均序列优势。 | 负优势时不确定token少受罚，非band-pass、非额外verifier。原文更长生成与缺length-matched对照限制因果解释；Qwen三数据种子的p=.083不应写成显著胜出。 |

</div>

## 取舍分析 {#analysis}

### 自动过程标签不是无条件的步骤真理

人工过程监督直接询问某一步是否合理；Math-Shepherd估计的是从这一步继续采样后答对的比例。后者还混入当前续写器能否恢复、能否完成后续推理的信息。INTUITOR更进一步只读模型分布，连最终答案正确性都不是其原生证据；三者的标签含义应先分清，再比较成本。

对照来源：[process-supervision](../../../post-training/2305.20050-process-supervision/README.md) · [math-shepherd](../../../post-training/2312.08935-math-shepherd/README.md) · [intuitor](../../../post-training/2505.19590-intuitor/README.md)

### 同叫信用过滤，作用对象和守恒量却不同

TACO只衰减正优势，避免正确整句污染局部低质量token；MART-GRPO在失败episode中遮去事后错误边界后的信用，原分母不变；MRTPO依据不同奖励信息块重分配正负信用，并控制总量与重分配幅度。它们不能都实现成“删掉可疑token后对剩余token求均值”。

对照来源：[taco](../../../post-training/2607.07976-taco/README.md) · [mart-grpo](../../../post-training/2610.32431-mart-grpo/README.md) · [mrtpo](../../../post-training/2610.21439-mrtpo/README.md)

### 奖励维度优先级与token信用是两种坐标系

TACO在同一响应的正优势内部，按token风险降低局部信用，负优势不变。CONCUR则比较同一prompt组中不同响应的主奖励与辅助奖励，修正辅助标准化分数的排序和到顶差异；它不定位哪一个token造成错误。把两者都写成“奖励乘一个小系数”会丢掉CONCUR的最近投影与TACO的正负分流。辅助到顶并列也不是终止梯度训练，而是让该辅助在此组不再单独排序。

对照来源：[concur](../../../post-training/2610.36437-concur/README.md) · [taco](../../../post-training/2607.07976-taco/README.md)

### 结果密度是组内新坐标，不是token风险或主奖励优先级

TACO按局部tail risk降低正token信用，负信用保留；CONCUR按主奖励顺序投影组内辅助优势。DARS改的是另一层：相同prompt下结果表示的拥挤度，先用含self的Gaussian密度缩放非负终局reward，再计算组优势。原reward都相同也可能因density不同产生不同缩放值；只有缩放后reward为常数时才出现零方差。重复点在窄带宽仍有重复计数，不能一律当density趋1。embedding、bandwidth、std约定决定该坐标，合成KDE检查不是策略分布覆盖或图像质量证据。

对照来源：[dars-density](../../../post-training/2611.04792-dars/README.md) · [taco](../../../post-training/2607.07976-taco/README.md) · [concur](../../../post-training/2610.36437-concur/README.md)

### 先合成视频奖励，还是把奖励分给生成 token？

EmoReward 在评分通道维度校准一个视频标量，靠本次有效性与前一完成轮的代理相关性；TVRL 则沿生成 token 维度，使用冻结 VLM 的输入梯度把现有组优势重新分配。前者只改标量并不定位哪些 token 导致效果，后者的梯度归因也不会估计面部或运动评分器跨轮是否可靠。比较时分别冻结评分器集合与信用分配方式。

对照来源：[emoreward](../../../post-training/2611.06518-emoreward/README.md) · [tvrl](../../../post-training/2610.01973-tvrl/README.md)

### 奖励有用不等于token该怎么分，信用守恒也不等于奖励正确

MaxIM先定义任务信息与事实一致性怎样成为可用奖励；MCPO接受已有序列优势，只改变局部token的相对权重。MCPO的响应均值守恒不能修复一个错误critic，MaxIM的critic也不会自动给出正确token归因。比较时应分别检查奖励端有没有特权泄漏、token端是old policy还是current policy，以及生成长度是否改变实际预算。

对照来源：[maxim](../../../post-training/2611.12825-maxim/README.md) · [mcpo](../../../post-training/2611.14015-mcpo/README.md)

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

### CONCUR为何不能直接复用TACO的风险权重，或只把长度奖励权重调小？ {#cross-concur-reward-axis-not-token-filter}

??? note "展开答案与例子"

    **答案：** TACO按token风险衰减正信用，解决整条成功回答对局部错误的强化；CONCUR要求主奖励更高的响应不能得到更低的门控辅助分数，并在需要时合并到顶分数。统一缩放辅助仍保留原来可能反转的次序，也不等于最小距离保序投影。

    **教学例子：** 教学示意：两条响应正确性为0.6与0.9，长度标准化分数却为1与-1；都乘0.1不会修复辅助本身的反序，逐token风险又回答不了这两个响应的主次关系。

    对照来源：[concur](../../../post-training/2610.36437-concur/README.md) · [taco](../../../post-training/2607.07976-taco/README.md)

### 原reward全为1时，DARS一定和不改reward的组标准化一样给零优势吗？ {#cross-outcome-density-not-token-or-priority}

??? note "展开答案与例子"

    **答案：** 不一定。密度不同会把相同reward缩放成不同值，再标准化就可能有非零相对信号；零方差判断必须看缩放后reward。TACO根据token风险调正信用，CONCUR依据主奖励约束辅助排序，都没有仅由原reward相等就等价于DARS的理由。三种方法读取的证据和作用坐标不同。

    **教学例子：** 教学例：同组结果y=(0,0,100)、极窄带宽、r=(1,1,1)，含self密度约(2,2,1)，缩放后为(0.5,0.5,1)并非常数；若三个结果全重合才得到共同密度和常数缩放值。

    对照来源：[dars-density](../../../post-training/2611.04792-dars/README.md) · [taco](../../../post-training/2607.07976-taco/README.md) · [concur](../../../post-training/2610.36437-concur/README.md)

### 两段视频最终情绪标量相同，EmoReward 和 TVRL 是否一定给生成 token 相同信用？ {#cross-emoreward-vs-tvrl-credit-axis}

??? note "展开答案与例子"

    **答案：** 不一定。EmoReward 的输出是视频级标量，不能单独决定 token 信用；TVRL 会把既有组优势按冻结 VLM 的输入梯度分配。相同标量的两段视频仍可能有不同的 token 敏感度。如果同组优势本身为零，归因不能凭空产生非零信用。

    **教学例子：** 教学例：假设两段视频在一个非零优势的组内都为正优势，一段更依赖前景人物动作 token，另一段依赖后半段转场；TVRL 的敏感度可不同，EmoReward 不输出这样的分配。

    对照来源：[emoreward](../../../post-training/2611.06518-emoreward/README.md) · [tvrl](../../../post-training/2610.01973-tvrl/README.md)

### 把MCPO套在MaxIM奖励上，就能保证更真实的记忆吗？ {#cross-reward-versus-token-redistribution}

??? note "展开答案与例子"

    **答案：** 不能。两者可以作用在不同环节，但信息奖励近似、token信用启发式和推理输入隔离要分别验证。响应内平均优势守恒只是一条算术合同，不证明critic正确、摘要无幻觉或任务提升。

    **教学例子：** 教学例：如果critic错误奖励了虚构预算，MCPO仍可把这个正优势按margin分给token；均值完全守恒，却依然强化错误方向。

    对照来源：[maxim](../../../post-training/2611.12825-maxim/README.md) · [mcpo](../../../post-training/2611.14015-mcpo/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-11** · 加入 Google MaxIM 与 PayPal MCPO，区分奖励产生、前向grounding和token信用重分配；保留MCPO负优势方向、均值守恒及长度/显著性限制。仅L1 CPU核，完整Gemini/长rollout实验按成本不复现。

涉及：[maxim](../../../post-training/2611.12825-maxim/README.md) · [mcpo](../../../post-training/2611.14015-mcpo/README.md)

**2026-11-07** · 补入 11 月 5 日公告窗口的 EmoReward，对照 TVRL 的 token 信用，区分通道相关、当前有效性与组内 token 敏感度；仅 CPU L1，未运行生成器或完整训练。

涉及：[emoreward](../../../post-training/2611.06518-emoreward/README.md) · [tvrl](../../../post-training/2610.01973-tvrl/README.md)

**2026-11-05** · 补入DARS，按终局结果密度、token正信用和主奖励保序三轴对照TACO/CONCUR；明确含self与重复点、缩放后零方差、非负reward和L1机制证据边界。

涉及：[dars-density](../../../post-training/2611.04792-dars/README.md) · [taco](../../../post-training/2607.07976-taco/README.md) · [concur](../../../post-training/2610.36437-concur/README.md)

**2026-10-30** · 精读CONCUR的辅助优势保序投影、到顶并列和整batch信任更新，与TACO的token正信用校准分轴比较；记录L1估计器而非32GPU训练能力。

涉及：[concur](../../../post-training/2610.36437-concur/README.md) · [taco](../../../post-training/2607.07976-taco/README.md)

**2026-10-27** · 首版：比较人工/自动过程标签、MRTPO奖励定位、TACO正信用、MART失败后缀过滤与INTUITOR内在奖励；已阅36篇摘要，精读6篇。

覆盖 36 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 41 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [EmoReward: Self-Evolving Reward Calibration for Emotional Video Generation RL](../../../post-training/2611.06518-emoreward/README.md)
- [Density-Aware Reward Scaling: A Reinforcement Learning Framework for Reward-Proportional Sampling](../../../post-training/2611.04792-dars/README.md)
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
- [CONCUR: Concordant Auxiliary Rewards for Multi-Task, Multi-Reward Reinforcement Learning](../../../post-training/2610.36437-concur/README.md)
- [MaxIM: Maximally Informative Incremental Summarization via Reinforcement Learning](../../../post-training/2611.12825-maxim/README.md)
- [Margin-Guided Token Credit for Reinforcement Learning with Verifiable Rewards](../../../post-training/2611.14015-mcpo/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/reward-and-credit.md) · [返回全部精读卡片](../index.md)
