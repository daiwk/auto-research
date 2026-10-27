---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 省掉哪一份算力：选问题、少生成、分枝与有条件重放

[LLM 后训练](../index.md) · 更新 2026-10-27 · 38 篇主题资料 / 6 篇重点对照

数据与预算方法改变的是训练链路的不同位置。课程重估当前难度，LESSER降低筛选特征成本，STOPD随机少生成并校正，BranchOPD增加关键分枝，Lightning缓存教师，TAR召回被压制的正确模式；少调用一次教师不等于整个训练更便宜。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/post-training/data-and-budget.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：选择对象：问题、token位置、后缀、历史轨迹 · 额外代价：估难、前向特征、教师评分、bank构建 · 统计合同：逆概率权重、固定策略独立分枝、缓存一致性 · 学生变化：难度重估、当前logp刷新、被压制模式门控

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO](../../../reproductions/2610.13669-grpo-difficulty-curriculum/README.md) · [原始来源](https://arxiv.org/abs/2610.13669)<br>章节：背景与主要改动、核心公式、边界与未完成项 | 以当前policy真实rollout成功率重估难度，按课程阶段保留样本。 | 难度并非题长或永久标签；本地缩放课程与B5控制不等同原文完整阶段进展复现。 |
| [LESSER: Post-Training Data Selection with Output-Layer Gradients](../../../post-training/2610.03702-lesser/README.md) · [原始来源](https://arxiv.org/abs/2610.03702)<br>章节：背景与主要改动、核心公式、复现边界 | 以一次前向解析得到输出层梯度特征，替换昂贵的全参数逐样本梯度，原选择规则不变。 | 只保证独立readout下的特征公式，不是全模型梯度等价；当前固定随机张量诊断，未做下游LLM训练。 |
| [Does On-Policy Distillation Need to Complete Every Rollout?](../../../post-training/2610.21337-stopd/README.md) · [原始来源](https://arxiv.org/abs/2610.21337v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 生成前独立采anchor并确定block cutoff，保留token以精确inclusion probability加权。 | 无偏论证针对gradient sum，不保证每次归一化Adam更新相同；完整长rollout未复现，已有真实短策略L1组件。 |
| [Branching On-Policy Distillation](../../../reproductions/2610.13481-branch-opd/README.md) · [原始来源](https://arxiv.org/abs/2610.13481)<br>章节：背景与主要改动、核心公式、代码映射与复现边界 | 按学生不确定性与师生分歧选fork，从同一冻结学生策略独立采多个suffix，公共前缀只计一次。 | 在关键处分配更多生成预算，并非裁短或教师强制；本地短checkpoint未实跑同预算单轨基线。 |
| [Lightning OPD](../../../post-training/2604.13010-lightning-opd/README.md) · [原始来源](https://arxiv.org/abs/2604.13010)<br>章节：背景与主要改动、核心公式、复现边界 | 先采学生轨迹并由一致教师一次评分缓存，训练阶段只读取教师缓存。 | 将教师成本移到预填充，不等于无教师成本或轨迹持续刷新；本地候选缓存未复刻Qwen token分布训练。 |
| [Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay](../../../post-training/2610.24236-tar-adaptive-replay/README.md) · [原始来源](https://arxiv.org/abs/2610.24236v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 从base正确轨迹建分散原型bank，只重放当前策略相对base已压制的轨迹与token。 | 需计入bank生成和验证成本，且bank有限；完整实验未复现，当前随机模型L1诊断不证明语义多样性。 |

</div>

## 取舍分析 {#analysis}

### 题目难，不代表对当前学生最有训练价值

课程以当前成功率定位难度带，学生更新后同题可以移入或移出。LESSER则近似获取任务相关梯度特征，选择依据不是题目长短或答错率本身。前者需要花rollout估难，后者需要候选与目标query前向；预算比较应包含筛选成本，目标query也不能从最终test取得。

对照来源：[grpo-difficulty-curriculum](../../../reproductions/2610.13669-grpo-difficulty-curriculum/README.md) · [lesser](../../../post-training/2610.03702-lesser/README.md)

### 生成、评分、重放是三本不同的账

STOPD在生成前随机截断，依赖保留概率校正；BranchOPD在已选fork扩充学生后缀，公共前缀不能重复计信用；Lightning缓存教师评分，TAR缓存已验证base轨迹并按当前压制程度激活。它们省略或增加的计算不同，既不能仅数训练步，也不能只数训练期教师调用。

对照来源：[stopd](../../../post-training/2610.21337-stopd/README.md) · [branch-opd](../../../reproductions/2610.13481-branch-opd/README.md) · [lightning-opd](../../../post-training/2604.13010-lightning-opd/README.md) · [tar-adaptive-replay](../../../post-training/2610.24236-tar-adaptive-replay/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 课程认为一道题太难，LESSER就一定也该把它删掉吗？ {#cross-hardness-versus-selection-value}

??? note "展开答案与例子"

    **答案：** 不一定。课程依据当前策略成功率挑难度带，LESSER按候选与目标query的输出层梯度特征执行既定选择规则，衡量的是另一种相关性。难题可能含所需知识，也可能完全超出可学范围，不能只凭难度推出梯度选择结论。两种筛选还各有成本。

    **教学例子：** 教学例子：学生暂时做不出的领域题，仍可能与目标任务共享梯度方向；这不保证训练它有效，却也不是自动零价值。

    对照来源：[grpo-difficulty-curriculum](../../../reproductions/2610.13669-grpo-difficulty-curriculum/README.md) · [lesser](../../../post-training/2610.03702-lesser/README.md)

### STOPD与BranchOPD都改变后缀长度，为什么不能实现成同一种早停？ {#cross-cutoff-versus-branch}

??? note "展开答案与例子"

    **答案：** STOPD生成前随机选cutoff，以每个token的保留概率校正估计；BranchOPD先定位fork，再从同一冻结策略独立采多个后缀，公共前缀只计一次。一个减少观测并补权，一个在关键状态增加探索。事后随意截短既没有STOPD概率合同，也没有Branch的独立分枝。

    **教学例子：** 教学例子：预先抽到第64词截止，与在第64词分出三条续写，是相反的预算分配操作，不该只用“64词预算”概括。

    对照来源：[stopd](../../../post-training/2610.21337-stopd/README.md) · [branch-opd](../../../reproductions/2610.13481-branch-opd/README.md)

### Lightning缓存与TAR回放都复用旧数据，为什么TAR还要看当前学生概率？ {#cross-teacher-cache-versus-behavior-bank}

??? note "展开答案与例子"

    **答案：** Lightning缓存的是一致教师对初始学生轨迹的评分，以减少训练期教师调用；TAR保存的是base已验证正确行为，只有相对base被当前策略压制时才激活重放，并聚焦被压制token。固定bank不等于固定权重，更不能把训练期零教师调用理解为前期建库无成本。

    **教学例子：** 教学例子：某base解法当前仍常出现，TAR可给零重放；教师评分缓存仍可存在，两种“缓存命中”没有同一含义。

    对照来源：[lightning-opd](../../../post-training/2604.13010-lightning-opd/README.md) · [tar-adaptive-replay](../../../post-training/2610.24236-tar-adaptive-replay/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较课程/LESSER选样、STOPD少生成、BranchOPD分枝、Lightning教师缓存与TAR条件回放；已阅38篇摘要，精读6篇。

覆盖 38 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 38 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Ask to Distill: Learning to Synthesize Data for On-Policy Distillation](../../../post-training/2610.27450-ask-to-distill/README.md)
- [Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay](../../../post-training/2610.24236-tar-adaptive-replay/README.md)
- [Does On-Policy Distillation Need to Complete Every Rollout?](../../../post-training/2610.21337-stopd/README.md)
- [Continually Post-training Small Models via Synthetic Self-distillation](../../../reproductions/2610.13113-synthself/README.md)
- [Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training](../../../reproductions/2610.12933-progressive-contraction/README.md)
- [A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO](../../../reproductions/2610.13669-grpo-difficulty-curriculum/README.md)
- [Branching On-Policy Distillation](../../../reproductions/2610.13481-branch-opd/README.md)
- [BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation](../../../reproductions/2610.13285-boundary-evo/README.md)
- [ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery](../../../post-training/2610.11332-recal/README.md)
- [PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation](../../../post-training/2610.11167-pivot/README.md)
- [MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis](../../../reproductions/2610.12659-magicbeanstalk/README.md)
- [GRPODropout: Less is More for Online Reinforcement Learning Rollouts](../../../post-training/2610.11854-grpo-dropout/README.md)
- [DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation](../../../post-training/2610.11659-dial-opd/README.md)
- [LESSER: Post-Training Data Selection with Output-Layer Gradients](../../../post-training/2610.03702-lesser/README.md)
- [Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT](../../../post-training/2610.03361-follow-the-winners/README.md)
- [Dependency-Aware Reward Shaping for Agentic Reinforcement Learning](../../../post-training/2610.01207-dars/README.md)
- [Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL](../../../post-training/2609.37898-gats/README.md)
- [ROSS: Relearning from Self-Generated Rollouts through Selective Supervision](../../../post-training/2609.35954-ross/README.md)
- [Shockingly Simple Self-retrospection Improves Agentic Models Without RL](../../../post-training/2609.35741-roft/README.md)
- [RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning](../../../post-training/2609.20784-retire-opd/README.md)
- [Trajectory Learnability for Offline On-Policy Distillation](../../../post-training/2609.18321-trajectory-learnability/README.md)
- [GrowMTP: Can RL Grow Its Own Draft Head?](../../../post-training/2609.16648-growmtp/README.md)
- [Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation](../../../post-training/2609.14636-stride-opd/README.md)
- [Data-free On-policy Distillation](../../../post-training/2609.14193-df-opd/README.md)
- [LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation](../../../post-training/2609.11739-locus/README.md)
- [A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients](../../../post-training/2609.11768-adaptive-opd-gate/README.md)
- [Extremely Sparse Supervision Incentivizes Reasoning Ability](../../../post-training/2609.04565-sparse-opd/README.md)
- [SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts](../../../post-training/2608.04962-specroll/README.md)
- [Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning](../../../post-training/2608.05080-rail/README.md)
- [CoBA-RL](../../../post-training/2606.22317-coba-rl/README.md)
- [Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training](../../../post-training/2605.12483-sparse-to-dense-reward-principle/README.md)
- [Lightning OPD](../../../post-training/2604.13010-lightning-opd/README.md)
- [Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts](../../../post-training/2603.17070-cross-script-knowledge-transfer/README.md)
- [Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning](../../../post-training/2602.21103-prompt-level-distillation/README.md)
- [CHORD](../../../post-training/2508.11408-chord/README.md)
- [SPIRAL](../../../post-training/2506.24119-spiral/README.md)
- [Absolute Zero](../../../post-training/2505.03335-absolute-zero/README.md)
- [RAFT](../../../post-training/2304.06767-raft/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/data-and-budget.md) · [返回全部精读卡片](../index.md)
