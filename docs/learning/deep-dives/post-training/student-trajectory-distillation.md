---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 轨迹蒸馏：采样者、提案与散度方向分开看

[LLM 后训练](../index.md) · 更新 2026-11-05 · 43 篇主题资料 / 9 篇重点对照

“on-policy”描述监督发生在哪些状态，FKL/RKL/JSD描述在这些状态怎样比较分布。GKD和MiniLLM建立这两个轴，DrOPD、AP-OPD再调整纠错位置或强度，Semi-OPD与学习信号诊断则提醒：离线复用和残余损失各有不同含义。 MPOPD再把采样者变成可学习proposal：几何混合是提案target，学生仍向教师做RKL，二者不能混成同一个蒸馏分布。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/post-training/student-trajectory-distillation.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：状态来源：教师示范、当前学生、初始学生固定轨迹 · 比较几何：FKL覆盖、RKL寻模态、JSD路由 · 局部处理：增加纠正方向或缩放原监督 · 证据类型：训练目标、缓存合同、学习信号诊断

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [SpecOPD: Branch-Parallel On-Policy Distillation for Speculative Decoding](../../../post-training/2611.02846-specopd/README.md) · [原始来源](https://arxiv.org/abs/2611.02846v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 在固定reference anchors重新采当前draft私有历史，以共享trunk并行收集teacher分布，按overlap的prefix乘积优化接受长度surrogate。 | 改的是监督采集依赖与draft目标，不是普通学生RKL的同义写法；teacher全词表质量与predecessor readout必须保留。完整混合target训练/serving未复现，局部张量不证明加速。 |
| [GKD](../../../post-training/2306.13649-gkd/README.md) · [原始来源](https://arxiv.org/abs/2306.13649)<br>章节：背景与主要改动、核心公式、复现边界 | 让教师在学生实际生成的前缀上给分布监督，用student data fraction混合固定数据与on-policy状态。 | 改善状态覆盖并不指定唯一散度；本地候选支撑集未训练原文T5序列模型。 |
| [MiniLLM](../../../post-training/2306.08543-minillm/README.md) · [原始来源](https://arxiv.org/abs/2306.08543)<br>章节：背景与主要改动、核心公式、复现边界 | 在学生生成分布上优化RKL，并用teacher-mixed sampling、baseline和长度处理稳定估计。 | 偏向学生可承载的教师模态，可能弱化欠覆盖方向；本地为候选采样与梯度方向验证。 |
| [Divergence-Routed On-Policy Distillation for Language Models](../../../post-training/2610.19572-divergence-routed-opd/README.md) · [原始来源](https://arxiv.org/abs/2610.19572v1)<br>章节：背景与主要改动、核心公式、结果与验收 | 所有位置保留RKL，仅在高JS分歧位置增加FKL，以候选并集的PPO surrogate实施纠正。 | 路由支持教师高概率但学生少采到的候选，不等于全局改用FKL；完整训练未复现，微型在线更新为L1诊断。 |
| [Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation](../../../post-training/2610.28194-ap-opd/README.md) · [原始来源](https://arxiv.org/abs/2610.28194v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 比较相邻块的原始惩罚统计，对突增后整块有符号监督统一回拉。 | 不增加教师前向，也不换符号；阈值并非校准显著性检验。完整实验成本过高未复现。 |
| [When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better](../../../post-training/2610.11291-semi-opd/README.md) · [原始来源](https://arxiv.org/abs/2610.11291)<br>章节：背景与主要改动、核心公式、代码映射与复现边界 | 固定初始学生轨迹与教师评分，但每步重算当前学生logp及优势。 | 省去重复采集，却不会自动覆盖新学生访问的全部状态；短预算checkpoint只验训练链路。 |
| [Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals](../../../post-training/2610.11247-opd-learning-signals/README.md) · [原始来源](https://arxiv.org/abs/2610.11247)<br>章节：背景与主要改动、核心公式、代码映射与复现边界 | 同时观察残余loss、截断前梯度、两折occupancy、参数位移与CKA，区分损失和可用学习信号。 | 这是相关性诊断设施，不是新优化算法；本地三步运行不复现长平台期，也不能证明失败原因。 |
| [Proposing Better Rollouts for On-Policy Distillation](../../../post-training/2610.36477-mpopd/README.md) · [原始来源](https://arxiv.org/abs/2610.36477v2)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 用独立proposal拟合更新后师生的归一化几何混合，学生沿proposal轨迹以滞后一token的冻结单步ratio加权RKL。 | ratio不是累积乘积；每轮proposal从更新后学生重置。完整采样、LM复制和优化器编排未实现，小张量loss不能证明真实on-policy。 |
| [Shuffled OPSD: When Semantic Consistency Hurts On-Policy Self-Distillation?](../../../post-training/2611.04958-shuffled-opsd/README.md) · [原始来源](https://arxiv.org/abs/2611.04958v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 同时改变学生采样和教师评分的共享问题词序，保留固定111偏移的完整其他题示例为教师私有上下文，使用逐词表有符号上截断监督。 | 变的是共享输入与访问状态，不是重排已采轨迹；词multiset不保证token预算不变。负项与response等权归约不能被普通KL替代，完整数学评测仍用原始题。 |

</div>

## 取舍分析 {#analysis}

### 同在学生轨迹上，也可能学到不同方向

GKD说明监督应覆盖学生会走到的前缀，但允许多种散度。MiniLLM选择学生到教师的RKL；当学生几乎不支持某教师候选时，该方向的纠正可能较弱。DrOPD保留RKL底座，只在高分歧处加入FKL，并从师生候选并集实施更新。采样状态、散度方向与被更新候选因此是三个可分别检查的部件。

对照来源：[gkd](../../../post-training/2306.13649-gkd/README.md) · [minillm](../../../post-training/2306.08543-minillm/README.md) · [divergence-routed-opd](../../../post-training/2610.19572-divergence-routed-opd/README.md)

### loss大、梯度弱、局部尖峰，不是同一个故障

OPD Learning Signals要求同时记录损失与梯度，避免把残余差异当作仍有强学习动力。AP-OPD处理的是相邻块惩罚突然上升，缩放整块而保留方向；它不构成对平台期原因的通用解释。Semi-OPD则改变状态复用方式，教师标签固定也不允许把学生相关优势固定下来。

对照来源：[opd-learning-signals](../../../post-training/2610.11247-opd-learning-signals/README.md) · [ap-opd](../../../post-training/2610.28194-ap-opd/README.md) · [semi-opd](../../../post-training/2610.11291-semi-opd/README.md)

### 改采样者，不等于把学生target改成几何混合

GKD让教师在学生访问的前缀上监督，MiniLLM进一步选定学生到教师的RKL并稳定估计。MPOPD保留学生向教师学习，却训练另一个proposal来改善轨迹可达性；师生几何混合供proposal拟合，不直接替代教师成为学生的target。采样差距以冻结old-student/old-proposal的前一token单步ratio处理，不是把整条路径ratio累乘。真实实现还须保证proposal每轮从更新后学生重置；只有外部logits接口不能证明这些轨迹来源。

对照来源：[mpopd](../../../post-training/2610.36477-mpopd/README.md) · [gkd](../../../post-training/2306.13649-gkd/README.md) · [minillm](../../../post-training/2306.08543-minillm/README.md)

### 固定外层reference仍可有当前策略内层分支

GKD/MiniLLM让teacher在学生访问状态上监督，MPOPD再训练独立proposal改变可达性；SpecOPD则针对推测draft，把固定reference作为外层锚点，每步重采内层draft分支以打破整响应验证依赖。reference固定不等于分支off-policy；但这也不是完全自由的学生轨迹。其E2E-TV优化前缀存活，需要完整teacher质量，且teacher query必须读私有前驱历史；loss通过不能证明混合注意力target已经正确共享状态或真实serving更快。

对照来源：[specopd](../../../post-training/2611.02846-specopd/README.md) · [gkd](../../../post-training/2306.13649-gkd/README.md) · [mpopd](../../../post-training/2610.36477-mpopd/README.md)

### 同为学生轨迹，题目条件本身也会改变访问状态

GKD强调教师应在学生实际访问的前缀上监督，但不固定唯一散度。Shuffled OPSD把共享题目也作为设计变量：相同T(x)同时决定学生采样与教师评分，固定其他题参考只在teacher中出现。只打乱教师输入或生成完再打乱续写，都不是该条件结构。其signed pointwise cap保留负项，与普通KL不同；负总损失可以来自定义而非错误。状态来源、共享输入、教师私有信息和数值目标仍需分别检查，局部loss通过不能证明数学能力提升。

对照来源：[shuffled-opsd](../../../post-training/2611.04958-shuffled-opsd/README.md) · [gkd](../../../post-training/2306.13649-gkd/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### SpecOPD的reference anchor后分支已偏离原文，教师仍应按原reference后缀来打分吗？ {#cross-branch-prefix-is-not-reference-label}

??? note "展开答案与例子"

    **答案：** 不应。当前分支token的教师条件由reference前缀和该分支已采样token组成，不能用reference后缀替换，也不能看到未来或兄弟。第一token读anchor，后续读前驱行。否则改变监督历史，甚至从自身行泄漏答案；不再是原方法的分支监督。

    **教学例子：** 教学例：reference是a quiet，draft采short evening；预测evening必须以a short为条件，而不能回到a quiet，也不能把evening先喂入再打自己的分。

    对照来源：[specopd](../../../post-training/2611.02846-specopd/README.md) · [gkd](../../../post-training/2306.13649-gkd/README.md)

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

### MPOPD把提案拟合到师生几何混合后，学生也应直接蒸馏这个混合target吗？ {#cross-mpopd-proposal-target-versus-student-target}

??? note "展开答案与例子"

    **答案：** 不应这样替换。几何混合决定proposal应从哪里采样，学生目标仍是向教师的RKL；加权学生loss还用冻结旧学生与旧proposal的单步ratio，并滞后一token。GKD/MiniLLM提示的“采样状态”和“散度方向”在这里又增加了独立提案轴。

    **教学例子：** 教学示意：proposal更容易提出教师支持的新前缀，不表示学生应只学一个折中教师；把采样分布直接当监督target，会同时改掉原方法的两个目标。

    对照来源：[mpopd](../../../post-training/2610.36477-mpopd/README.md) · [gkd](../../../post-training/2306.13649-gkd/README.md) · [minillm](../../../post-training/2306.08543-minillm/README.md)

### GKD要求沿学生轨迹监督，Shuffled OPSD把题目打乱后是不是就变成了off-policy？ {#cross-shared-input-shuffle-not-offpolicy}

??? note "展开答案与例子"

    **答案：** 不因此变成off-policy。若学生确实在变换后的共享问题上采样，教师评分同一问题和同一已采前缀，监督仍来自学生实际访问状态。需要另外区分训练输入发生变化、teacher私有示例和截断损失；把原题轨迹缓存后仅改教师题目才改变了条件对齐。

    **教学例子：** 教学例：学生在“coins red five contains box”上生成y，教师也评分T(x),y的同一前缀；若学生实际读的是原题，教师却读打乱题，已不是同一条件实验。

    对照来源：[shuffled-opsd](../../../post-training/2611.04958-shuffled-opsd/README.md) · [gkd](../../../post-training/2306.13649-gkd/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-05** · 补入Shuffled OPSD的共享题目变换，对照GKD的学生访问前缀原则；明确固定参考配对、有符号上截断及原题评测，未把输入扰动或L1梯度检查当作能力复现。

涉及：[shuffled-opsd](../../../post-training/2611.04958-shuffled-opsd/README.md) · [gkd](../../../post-training/2306.13649-gkd/README.md)

**2026-11-04** · 精读SpecOPD，分开固定reference外层、当前draft内层分支及E2E-TV目标；相对GKD/MPOPD补充采集依赖这一轴，保留teacher完整质量、祖先隔离与predecessor读出，不把L1张量通过写成serving加速。

涉及：[specopd](../../../post-training/2611.02846-specopd/README.md)

**2026-10-30** · 精读MPOPD v2，把独立proposal、学生RKL、教师top-k支持与滞后一token的冻结单步ratio分开；相对GKD/MiniLLM补充采样者可学习这一轴，保留proposal重置等外部前提。

涉及：[mpopd](../../../post-training/2610.36477-mpopd/README.md) · [gkd](../../../post-training/2306.13649-gkd/README.md) · [minillm](../../../post-training/2306.08543-minillm/README.md)

**2026-10-27** · 首版：分开学生状态分布与散度方向，比较GKD/MiniLLM、DrOPD/AP-OPD、Semi-OPD和学习信号诊断；已阅40篇摘要，精读6篇。

覆盖 40 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 43 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Shuffled OPSD: When Semantic Consistency Hurts On-Policy Self-Distillation?](../../../post-training/2611.04958-shuffled-opsd/README.md)
- [SpecOPD: Branch-Parallel On-Policy Distillation for Speculative Decoding](../../../post-training/2611.02846-specopd/README.md)
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
- [Proposing Better Rollouts for On-Policy Distillation](../../../post-training/2610.36477-mpopd/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/student-trajectory-distillation.md) · [返回全部精读卡片](../index.md)
