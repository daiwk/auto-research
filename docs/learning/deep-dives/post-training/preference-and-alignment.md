---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 偏好不是一个分数：先确定反馈格式，再选对齐目标

[LLM 后训练](../index.md) · 更新 2026-10-27 · 25 篇主题资料 / 6 篇重点对照

DPO、KTO、SimPO、ORPO和IPO主要改变“怎样使用反馈”，CleanRM先处理“反馈是否可信”。参考模型、长度归一化、有限间隔和噪声校正是不同设计轴，不能因都在扩大好坏回答差异就当成同一方法。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/post-training/preference-and-alignment.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：监督单位：同题偏好对、单条满意标签、带噪标签 · 参照与尺度：reference log-ratio、长度平均、odds · 目标形状：持续拉开、有限间隔、SFT与偏好联合 · 错误来源：策略目标过强，还是标签本身有噪声

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [DPO](../../../post-training/2305.18290-dpo/README.md) · [原始来源](https://arxiv.org/abs/2305.18290)<br>章节：背景与主要改动、核心公式、复现边界 | 把同题chosen/rejected对转为相对冻结reference的log-ratio二分类，不单独训练RM。 | 流程减少了显式RM与在线RL环节，但仍需要可靠偏好对；本地是候选动作损失验证，未训练原文自回归LLM。 |
| [KTO](../../../post-training/2402.01306-kto/README.md) · [原始来源](https://arxiv.org/abs/2402.01306)<br>章节：背景与主要改动、核心公式、复现边界 | 以单条desirable/undesirable反馈及policy到reference的KL参照点构造效用。 | 不用人为凑同题偏好对，但两类权重、类别不平衡和参照分布仍需明确；本地是六候选线性策略。 |
| [SimPO](../../../post-training/2405.14734-simpo/README.md) · [原始来源](https://arxiv.org/abs/2405.14734)<br>章节：背景与主要改动、核心公式、复现边界 | 以每token平均policy logp作隐式奖励，用固定margin训练偏好，去掉reference前向。 | 长度尺度与偏好压力被明确写入目标；无reference不等于无反馈。已有真实token-loss路径，未复刻原文模型规模与judge。 |
| [ORPO](../../../post-training/2403.07691-orpo/README.md) · [原始来源](https://arxiv.org/abs/2403.07691)<br>章节：背景与主要改动、核心公式、复现边界 | 在同一目标里联合chosen的SFT NLL与chosen/rejected的odds-ratio偏好项。 | 单阶段兼顾绝对似然与相对偏好，但赔率有数值边界；本地完整候选action并非原文语言模型训练。 |
| [IPO](../../../post-training/2310.12036-ipo/README.md) · [原始来源](https://arxiv.org/abs/2310.12036)<br>章节：背景与主要改动、核心公式、复现边界 | 让相对reference的偏好gap拟合有限目标1/(2τ)，而非只要求差距不断增大。 | 超过目标也会被拉回，改变的是目标形状；本地已有缩小的token级自由生成路径，不能据此推断原文大模型效果。 |
| [CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF](../../../post-training/2610.21138-clean-rm/README.md) · [原始来源](https://arxiv.org/abs/2610.21138v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 先用干净校准子集与语义—恢复偏好的joint OT估计双向噪声，再冻结估计器校正RM风险。 | 校正依赖噪声率与校准代表性，signed loss不能擅自截零；完整RM/RLHF因成本过高未复现，当前是L1组件。 |

</div>

## 取舍分析 {#analysis}

### 先问数据里有什么，别从流行loss反推标签

DPO、SimPO、ORPO和IPO都消费同题回答的相对胜负，但KTO允许单条满意反馈。把不同问题的点赞与点踩拼成一对，等于新增了未观测的比较关系。CleanRM又位于另一层：它估计观察标签怎样偏离干净偏好，再校正训练风险；这不能由简单换一种偏好loss自动完成。

对照来源：[dpo](../../../post-training/2305.18290-dpo/README.md) · [kto](../../../post-training/2402.01306-kto/README.md) · [clean-rm](../../../post-training/2610.21138-clean-rm/README.md)

### “无reference”与“少过拟合”不是同一个开关

SimPO移除reference但保留长度平均隐式奖励和固定margin；ORPO用SFT项与赔率偏好共同训练。IPO保留reference，并把最优间隔设为有限值。三者改变不同部件：部署或训练内存、回答长度尺度、优选文本绝对似然和间隔饱和行为都要分开看，不能用一个本地准确率替代这些区别。

对照来源：[simpo](../../../post-training/2405.14734-simpo/README.md) · [orpo](../../../post-training/2403.07691-orpo/README.md) · [ipo](../../../post-training/2310.12036-ipo/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 只有用户对单条回答的点赞/点踩，应把记录凑成DPO对，还是先考虑KTO？ {#cross-binary-feedback-versus-pair}

??? note "展开答案与例子"

    **答案：** 先保留原反馈单位。DPO需要同一提示下哪条回答更好的关系，KTO直接使用单条满意标签及KL参照点。不同问题的点赞和点踩不能自动产生相对偏好；若要使用成对目标，应另外收集或可靠构造同题比较，而不是仅为了适配loss硬配对。

    **教学例子：** 教学例子：甲问题的一条点赞答复与乙问题的一条点踩答复，没有告诉我们甲问题中哪条答复比另一条好。

    对照来源：[dpo](../../../post-training/2305.18290-dpo/README.md) · [kto](../../../post-training/2402.01306-kto/README.md)

### SimPO和ORPO都不用reference，是否只要关掉DPO参考模型就能互换？ {#cross-reference-free-two-objectives}

??? note "展开答案与例子"

    **答案：** 不能。SimPO比较长度平均policy logp并减固定margin；ORPO还提高chosen自身似然，并比较赔率。直接删DPO参考项不会补上这两套定义，也不能保证长度与概率边界处理一致。相同的reference内存节省，不意味着相同训练压力。

    **教学例子：** 教学例子：两条回答相对差距变大时，ORPO的chosen NLL仍单独影响梯度；这不是SimPO固定margin项的别名。

    对照来源：[simpo](../../../post-training/2405.14734-simpo/README.md) · [orpo](../../../post-training/2403.07691-orpo/README.md) · [dpo](../../../post-training/2305.18290-dpo/README.md)

### 把DPO换成有限间隔IPO，就能修复被误标成rejected的正确回答吗？ {#cross-finite-margin-versus-label-cleaning}

??? note "展开答案与例子"

    **答案：** 不能自动修复。IPO限制模型要达到的相对间隔，但仍依赖给定偏好方向；标签反了，有限目标也可能朝错误方向训练。CleanRM针对的是噪声机制估计与风险校正，且其保证依赖估计准确，不能把目标不过度拉开当作标签已经干净。

    **教学例子：** 教学例子：若甲实际更好却被标为输，较温和地让甲输仍未纠正标签；噪声识别是另一项工作。

    对照来源：[dpo](../../../post-training/2305.18290-dpo/README.md) · [ipo](../../../post-training/2310.12036-ipo/README.md) · [clean-rm](../../../post-training/2610.21138-clean-rm/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较DPO/KTO反馈格式、SimPO/ORPO无reference目标、IPO有限间隔与CleanRM噪声校正；已阅25篇摘要，精读6篇。

覆盖 25 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 25 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF](../../../post-training/2610.21138-clean-rm/README.md)
- [GAW-PO: Preference Optimization with Gradient-Aligned Token Weights](../../../post-training/2610.01511-gaw-po/README.md)
- [A Zeroth-Order Paradigm for LLM Preference Alignment](../../../post-training/2609.19144-compo/README.md)
- [Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data](../../../post-training/2609.16532-sd-dpo/README.md)
- [Disentangling Optimization Scale from Preference Scale in DPO](../../../post-training/2608.27032-normalized-dpo/README.md)
- [GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning](../../../post-training/2608.25583-grip/README.md)
- [Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations](../../../post-training/2608.12062-pto/README.md)
- [Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization](../../../post-training/2608.12158-c2-dpo/README.md)
- [What do Reward Models Memorize?](../../../post-training/2607.24484-rm-memorization-protocol/README.md)
- [Mind the Gap: Structure-Aware Consistency in Preference Learning](../../../post-training/2604.27733-sa-dpo/README.md)
- [GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization](../../../post-training/2604.15602-group-dpo/README.md)
- [Judging with Confidence: Calibrating Autoraters to Preference Distributions](../../../post-training/2510.00263-probabilistic-autorater/README.md)
- [When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation](../../../post-training/2509.26600-benchmark-self-bias/README.md)
- [SimPO](../../../post-training/2405.14734-simpo/README.md)
- [ORPO](../../../post-training/2403.07691-orpo/README.md)
- [KTO](../../../post-training/2402.01306-kto/README.md)
- [Self-Rewarding LM](../../../post-training/2401.10020-self-rewarding/README.md)
- [SPIN](../../../post-training/2401.01335-spin/README.md)
- [IPO](../../../post-training/2310.12036-ipo/README.md)
- [SteerLM](../../../post-training/2310.05344-steerlm/README.md)
- [RLAIF](../../../post-training/2309.00267-rlaif/README.md)
- [DPO](../../../post-training/2305.18290-dpo/README.md)
- [SLiC-HF](../../../post-training/2305.10425-slic-hf/README.md)
- [RRHF](../../../post-training/2304.05302-rrhf/README.md)
- [Constitutional AI](../../../post-training/2212.08073-constitutional-ai/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/preference-and-alignment.md) · [返回全部精读卡片](../index.md)
