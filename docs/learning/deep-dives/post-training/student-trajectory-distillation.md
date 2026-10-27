---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 沿学生前缀蒸馏：采样分布与散度方向要分开看

[LLM 后训练](../index.md) · 更新 2026-10-27 · 40 篇主题资料 / 6 篇重点对照

“on-policy”描述监督发生在哪些状态，FKL/RKL/JSD描述在这些状态怎样比较分布。GKD和MiniLLM建立这两个轴，DrOPD、AP-OPD再调整纠错位置或强度，Semi-OPD与学习信号诊断则提醒：离线复用和残余损失各有不同含义。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/post-training/student-trajectory-distillation.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：状态来源：教师示范、当前学生、初始学生固定轨迹 · 比较几何：FKL覆盖、RKL寻模态、JSD路由 · 局部处理：增加纠正方向或缩放原监督 · 证据类型：训练目标、缓存合同、学习信号诊断

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [GKD](../../../post-training/2306.13649-gkd/README.md) · [原始来源](https://arxiv.org/abs/2306.13649)<br>章节：背景与主要改动、核心公式、复现边界 | 让教师在学生实际生成的前缀上给分布监督，用student data fraction混合固定数据与on-policy状态。 | 改善状态覆盖并不指定唯一散度；本地候选支撑集未训练原文T5序列模型。 |
| [MiniLLM](../../../post-training/2306.08543-minillm/README.md) · [原始来源](https://arxiv.org/abs/2306.08543)<br>章节：背景与主要改动、核心公式、复现边界 | 在学生生成分布上优化RKL，并用teacher-mixed sampling、baseline和长度处理稳定估计。 | 偏向学生可承载的教师模态，可能弱化欠覆盖方向；本地为候选采样与梯度方向验证。 |
| [Divergence-Routed On-Policy Distillation for Language Models](../../../post-training/2610.19572-divergence-routed-opd/README.md) · [原始来源](https://arxiv.org/abs/2610.19572v1)<br>章节：背景与主要改动、核心公式、结果与验收 | 所有位置保留RKL，仅在高JS分歧位置增加FKL，以候选并集的PPO surrogate实施纠正。 | 路由支持教师高概率但学生少采到的候选，不等于全局改用FKL；完整训练未复现，微型在线更新为L1诊断。 |
| [Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation](../../../post-training/2610.28194-ap-opd/README.md) · [原始来源](https://arxiv.org/abs/2610.28194v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 比较相邻块的原始惩罚统计，对突增后整块有符号监督统一回拉。 | 不增加教师前向，也不换符号；阈值并非校准显著性检验。完整实验成本过高未复现。 |
| [When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better](../../../post-training/2610.11291-semi-opd/README.md) · [原始来源](https://arxiv.org/abs/2610.11291)<br>章节：背景与主要改动、核心公式、代码映射与复现边界 | 固定初始学生轨迹与教师评分，但每步重算当前学生logp及优势。 | 省去重复采集，却不会自动覆盖新学生访问的全部状态；短预算checkpoint只验训练链路。 |
| [Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals](../../../post-training/2610.11247-opd-learning-signals/README.md) · [原始来源](https://arxiv.org/abs/2610.11247)<br>章节：背景与主要改动、核心公式、代码映射与复现边界 | 同时观察残余loss、截断前梯度、两折occupancy、参数位移与CKA，区分损失和可用学习信号。 | 这是相关性诊断设施，不是新优化算法；本地三步运行不复现长平台期，也不能证明失败原因。 |

</div>

## 取舍分析 {#analysis}

### 同在学生轨迹上，也可能学到不同方向

GKD说明监督应覆盖学生会走到的前缀，但允许多种散度。MiniLLM选择学生到教师的RKL；当学生几乎不支持某教师候选时，该方向的纠正可能较弱。DrOPD保留RKL底座，只在高分歧处加入FKL，并从师生候选并集实施更新。采样状态、散度方向与被更新候选因此是三个可分别检查的部件。

对照来源：[gkd](../../../post-training/2306.13649-gkd/README.md) · [minillm](../../../post-training/2306.08543-minillm/README.md) · [divergence-routed-opd](../../../post-training/2610.19572-divergence-routed-opd/README.md)

### loss大、梯度弱、局部尖峰，不是同一个故障

OPD Learning Signals要求同时记录损失与梯度，避免把残余差异当作仍有强学习动力。AP-OPD处理的是相邻块惩罚突然上升，缩放整块而保留方向；它不构成对平台期原因的通用解释。Semi-OPD则改变状态复用方式，教师标签固定也不允许把学生相关优势固定下来。

对照来源：[opd-learning-signals](../../../post-training/2610.11247-opd-learning-signals/README.md) · [ap-opd](../../../post-training/2610.28194-ap-opd/README.md) · [semi-opd](../../../post-training/2610.11291-semi-opd/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### GKD与MiniLLM都沿学生轨迹学习，为什么DrOPD还会额外加入FKL？ {#cross-on-policy-not-one-kl}

??? note "展开答案与例子"

    **答案：** 沿学生轨迹只确定前缀分布。MiniLLM的RKL倾向学生已支持的教师模态；学生给某教师候选极低概率时，纠正可能弱。DrOPD用高JS位置路由额外FKL，并保留教师候选支持。它没有更换采样者，也不是说所有位置都应无限增加FKL。

    **教学例子：** 教学例子：学生在同一错误前缀上总只考虑甲，教师偏好乙；访问该前缀并不自动保证乙获得足够纠正梯度。

    对照来源：[gkd](../../../post-training/2306.13649-gkd/README.md) · [minillm](../../../post-training/2306.08543-minillm/README.md) · [divergence-routed-opd](../../../post-training/2610.19572-divergence-routed-opd/README.md)

### Semi-OPD把教师评分缓存后，为什么不能连教师减学生的优势也永久缓存？ {#cross-frozen-teacher-versus-student-score}

??? note "展开答案与例子"

    **答案：** 教师配置固定时，其评分可复用；学生参数每步改变，学生logp及二者差值必须重算。否则更新仍响应旧学生的错误程度。与GKD持续采新前缀相比，Semi-OPD另外固定了初始轨迹，这两个“固定”不能混成训练中所有概率都不再变化。

    **教学例子：** 教学例子：某token已被学生学会，旧缓存还保留很大教师优势，会继续施加过时的监督压力。

    对照来源：[semi-opd](../../../post-training/2610.11291-semi-opd/README.md) · [gkd](../../../post-training/2306.13649-gkd/README.md) · [minillm](../../../post-training/2306.08543-minillm/README.md)

### AP-OPD回拉惩罚尖峰，与DrOPD在高分歧处加FKL，是相反的处理吗？ {#cross-spike-versus-direction-repair}

??? note "展开答案与例子"

    **答案：** 它们检测的对象不同。AP-OPD看相邻块原始惩罚是否突增，再缩放该块全部有符号系数；DrOPD看师生分布的JS与欠覆盖，增加指定纠正方向。一个改变局部强度，一个改变监督组成。不能只因都用“分歧”一词，就认定应对相同token作同样或相反操作。

    **教学例子：** 教学例子：持续高分歧却无块间跳升，可触发DrOPD路由而不触发AP回拉；两种门控不是同一阈值的反面。

    对照来源：[ap-opd](../../../post-training/2610.28194-ap-opd/README.md) · [divergence-routed-opd](../../../post-training/2610.19572-divergence-routed-opd/README.md) · [opd-learning-signals](../../../post-training/2610.11247-opd-learning-signals/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：分开学生状态分布与散度方向，比较GKD/MiniLLM、DrOPD/AP-OPD、Semi-OPD和学习信号诊断；已阅40篇摘要，精读6篇。

覆盖 40 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 40 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [On-Policy Self-Training: Data-Free Self-Improvement in Large Language Models](../../../post-training/2610.32770-opst/README.md)
- [UserArena: Benchmarking Interactive User Simulation for Long-Horizon Shopping Agents](../../../post-training/2610.30932-userarena-optd/README.md)
- [GIFT: Gradient Informed Filtering for Distillation Augmented Reasoning RL](../../../post-training/2610.30796-gift/README.md)
- [Projected Distillation: On Learning to Solve Hard Problems from Close, Correct Targets](../../../post-training/2610.27467-projected-distillation/README.md)
- [On-Policy Transition Distillation](../../../post-training/2610.28048-optd/README.md)
- [Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation](../../../post-training/2610.28194-ap-opd/README.md)
- [SimOPD: Relational Knowledge Transfer for On-Policy Distillation](../../../post-training/2610.23306-simopd/README.md)
- [GR-OPD: Group-Relative Sequence Credit for On-Policy Distillation](../../../post-training/2610.23042-gr-opd/README.md)
- [Information-Gain Calibrated On-Policy Distillation for Deep Search Agents](../../../post-training/2610.20664-ig-opd/README.md)
- [Divergence-Routed On-Policy Distillation for Language Models](../../../post-training/2610.19572-divergence-routed-opd/README.md)
- [State-OPD: State-Grounded On-Policy Distillation for Multi-Turn Agents](../../../reproductions/2610.13238-state-opd/README.md)
- [When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better](../../../post-training/2610.11291-semi-opd/README.md)
- [Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals](../../../post-training/2610.11247-opd-learning-signals/README.md)
- [SIPO: Unifying Reinforcement Learning with On-Policy Self-Distillation](../../../post-training/2609.36742-sipo/README.md)
- [The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation](../../../post-training/2609.36484-ride/README.md)
- [Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning](../../../post-training/2609.37915-oasis/README.md)
- [Interpolated Policy Distillation: A Controllable Continuum Between Off-Policy and On-Policy Distillation](../../../post-training/2609.37170-ipd/README.md)
- [FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators](../../../post-training/2609.37851-flowmap-opd/README.md)
- [DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies](../../../post-training/2610.00317-drift-opd/README.md)
- [Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models](../../../post-training/2609.38025-dr-opd/README.md)
- [An RL View of OPD: Least Square Policy Distillation for Sample-Efficient LLM Reasoning](../../../post-training/2609.35505-lspd/README.md)
- [Recursive Self-Improvement via On-Policy Distillation for Reasoning](../../../reproductions/2609.30652-recursive-opsd/README.md)
- [Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation](../../../post-training/2609.16937-gamma-opd/README.md)
- [Distillation as Probability Transport: Routed On-Policy Distillation](../../../post-training/2609.08337-route-opd/README.md)
- [OPDVR: On-Policy Distillation with Verifiable Rewards](../../../post-training/2608.24696-opdvr/README.md)
- [OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning](../../../post-training/2608.24310-opd-search-plus/README.md)
- [Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress](../../../post-training/2608.19408-r2-opd/README.md)
- [SR-OPSD: Self-Referenced On-Policy Self-Distillation](../../../post-training/2608.09745-sr-opsd/README.md)
- [U-OPSD](../../../post-training/2608.06296-u-opsd/README.md)
- [RP-OPSD](../../../post-training/2608.06347-rp-opsd/README.md)
- [On-Policy Delta Distillation for Multilingual Math Reasoning](../../../post-training/2608.05802-opd2/README.md)
- [DASH](../../../post-training/2608.06243-dash/README.md)
- [CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning](../../../post-training/2608.03673-causal-opd/README.md)
- [PCSD](../../../post-training/2608.01837-pcsd/README.md)
- [Flux-OPD](../../../post-training/2607.28022-flux-opd/README.md)
- [β-OPSD](../../../post-training/2607.28582-beta-opsd/README.md)
- [Relay-OPD](../../../post-training/2607.26057-relay-opd/README.md)
- [OPDLM](../../../post-training/2606.06712-opd-lm/README.md)
- [GKD](../../../post-training/2306.13649-gkd/README.md)
- [MiniLLM](../../../post-training/2306.08543-minillm/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/student-trajectory-distillation.md) · [返回全部精读卡片](../index.md)
