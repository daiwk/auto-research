---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 教师更强仍可能教错：信息、兼容性与成功行为保护

[LLM 后训练](../index.md) · 更新 2026-10-27 · 47 篇主题资料 / 6 篇重点对照

教师的价值不只取决于总分。OPSD改变训练期可见信息，MOPD与逐token路由组织多教师，CSD先统一概率事件，SPOD保护学生已成功选择，VAD筛出可归于视觉证据的修正；这些约束要在模仿之前分别成立。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/post-training/teacher-and-context.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：教师来源：同参数特权视图或独立领域专家 · 组合粒度：按域、逐token路由、成功action保护 · 可比接口：同词表坐标或共同文本事件 · 信息归因：额外证据、语言先验与学生已会行为

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [OPSD](../../../post-training/2601.18734-opsd/README.md) · [原始来源](https://arxiv.org/abs/2601.18734)<br>章节：背景与主要改动、核心公式、复现边界 | 同一模型以两种条件分布充当师生，教师额外看已验证答案，学生自行生成无答案前缀。 | 额外信息仅限训练教师；本地候选双视图未复刻Qwen参数级训练。 |
| [MOPD](../../../post-training/2606.30406-mopd/README.md) · [原始来源](https://arxiv.org/abs/2606.30406)<br>章节：背景与主要改动、核心公式、复现边界 | 各域先独立训练RL教师，再在同一学生rollout上混合领域分布信号。 | 复用专家但共享学生仍可能出现域间干扰；本地确定性mini-suite不代表大模型能力融合。 |
| [Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation](../../../post-training/2610.21234-token-teacher-selection/README.md) · [原始来源](https://arxiv.org/abs/2610.21234v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 每个学生前缀按置信、Hellinger距离或对齐特征距离选教师，软路由算术混合概率。 | 合适程度不等于教师更自信；异维特征不可直接相减。完整训练未复现，当前随机策略L1组件。 |
| [Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation](../../../post-training/2610.25034-spod/README.md) · [原始来源](https://arxiv.org/abs/2610.25034v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 仅保护成功episode中教师原始完整action概率更低的decision，取消该处蒸馏并加软floor。 | 其余decision继续学，soft floor不保证共享参数下永不退化；完整Agent实验因成本未复现。 |
| [CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer](../../../post-training/2610.28895-csd/README.md) · [原始来源](https://arxiv.org/abs/2610.28895v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 先按字符区间与解码文本构造共同chunk事件，用链式概率及REST保留未匹配质量。 | 跨tokenizer不再假装同ID同含义，但事件覆盖受限；本地是不同小词表的对齐与梯度诊断。 |
| [VAD](../../../post-training/2607.28590-vad/README.md) · [原始来源](https://arxiv.org/abs/2607.28590)<br>章节：背景与主要改动、核心公式、复现边界 | 对比同一教师证据存在/移除视图，将原修正单侧投影到视觉方向后重建学生锚定目标。 | 操作性对比不证明所有修正皆真视觉因果；本地过程证据轴替代真实crop，未运行原视觉模型。 |

</div>

## 取舍分析 {#analysis}

### 先确认教师信号说的是同一件事

MOPD和token路由都可能混合多个教师，但域级组合与逐位置选择并不相同。若师生tokenizer不同，CSD还要求先构建解码文本等价事件，不能直接混合同坐标概率。OPSD则未必换更大模型，它利用额外条件提高教师信息量；这与增加独立专家是另一轴。

对照来源：[mopd](../../../post-training/2606.30406-mopd/README.md) · [token-teacher-selection](../../../post-training/2610.21234-token-teacher-selection/README.md) · [csd](../../../post-training/2610.28895-csd/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### 教师修正应被审查，而不是自动全部接纳

SPOD指出学生成功动作也可能不符合教师偏好，保护粒度是具体action而不是整段成功episode。VAD进一步区分特权教师的修正来自视觉证据还是共享语言偏差。这两种约束分别审查“学生已有成功”与“教师证据来源”，不能只看teacher总分更高就跳过。

对照来源：[spod](../../../post-training/2610.25034-spod/README.md) · [vad](../../../post-training/2607.28590-vad/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### OPSD师生权重相同，为什么不是让学生直接抄标准答案？ {#cross-same-weights-privileged-view}

??? note "展开答案与例子"

    **答案：** 两者条件不同：学生只读问题并生成自己的前缀，教师在训练时额外读已验证答案，再评分同一前缀。监督的是无特权条件下的学生分布。MOPD主要换独立领域教师，而非必须给学生额外上下文；无论哪种路径，都不能将训练参考答案接入正式学生预测输入。

    **教学例子：** 教学例子：教师知道解法来判断学生下一步，但学生生成时不能看到解法；给学生也加答案会变成另一种任务。

    对照来源：[opsd](../../../post-training/2601.18734-opsd/README.md) · [mopd](../../../post-training/2606.30406-mopd/README.md)

### 逐token教师路由能否直接平均不同tokenizer的同编号logits？ {#cross-mixture-events-before-probabilities}

??? note "展开答案与例子"

    **答案：** 不能。路由软混合的是相同事件上的概率，平均logits或logp通常是另一种组合；不同tokenizer还可能让同ID对应不同文本。CSD先做文本事件对齐，并保留REST质量，再比较分布。教师选择发生得再细，也不能代替概率事件具有共同含义。

    **教学例子：** 教学例子：编号17在一位教师是完整词，在学生是词片段，二者不能因编号相同就被相加当作一个候选。

    对照来源：[token-teacher-selection](../../../post-training/2610.21234-token-teacher-selection/README.md) · [csd](../../../post-training/2610.28895-csd/README.md) · [mopd](../../../post-training/2606.30406-mopd/README.md)

### 学生episode成功但教师不喜欢其中一个action，SPOD会停掉整段学习吗？ {#cross-success-not-whole-episode-freeze}

??? note "展开答案与例子"

    **答案：** 不会。SPOD依据成功位和完整action原始概率比较，只在符合条件的decision取消蒸馏并施加软floor，其他decision继续正常学。普通MOPD或OPSD并不自动拥有这一保护；教师偏好与已验证成功不一致时，需要明确决定如何保留已有行为。

    **教学例子：** 教学例子：三步任务里第二步虽不常见却有效，只保护第二步不代表第一、三步的教师修正也要全部丢弃。

    对照来源：[spod](../../../post-training/2610.25034-spod/README.md) · [mopd](../../../post-training/2606.30406-mopd/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### 给OPSD教师更多视觉证据，就能确定它的全部修正都来自看图吗？ {#cross-privilege-not-visual-attribution}

??? note "展开答案与例子"

    **答案：** 不能。教师还可能改变语言先验、风格或继承错误前缀。VAD用同教师、同学生前缀的证据存在/移除对比构造视觉方向，并投影原修正；这是额外的归因设计，不是增加特权输入自动带来的性质，本地代理也不能冒充真实视觉归因能力。

    **教学例子：** 教学例子：换成证据crop后教师更爱简短措辞，简短偏好不必来自图像；需要对照视图区分共享变化。

    对照来源：[opsd](../../../post-training/2601.18734-opsd/README.md) · [vad](../../../post-training/2607.28590-vad/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较特权自教师、多领域与逐token路由、CSD文本事件对齐、SPOD成功保护和VAD视觉归因；已阅47篇摘要，精读6篇。

覆盖 47 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 47 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [When to Follow the Teacher: Advantage-Based On-Policy Distillation](../../../post-training/2610.31563-aopd/README.md)
- [Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning](../../../post-training/2610.30231-minimal-edit-opd/README.md)
- [CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer](../../../post-training/2610.28895-csd/README.md)
- [Reinforcement Learning with Visually Attributable On-Policy Self-Distillation](../../../post-training/2610.26856-vag/README.md)
- [Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization](../../../post-training/2610.25973-apsd/README.md)
- [Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation](../../../post-training/2610.25034-spod/README.md)
- [Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning](../../../post-training/2610.23181-treeopsd/README.md)
- [MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation](../../../post-training/2610.23234-multiagent-opd/README.md)
- [Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation](../../../post-training/2610.21601-waypoint-opd/README.md)
- [Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation](../../../post-training/2610.21234-token-teacher-selection/README.md)
- [Training-Free On-Policy Distillation](../../../post-training/2610.22236-tf-opd/README.md)
- [Learning from Unverified Peers via Shared Residual Distillation](../../../post-training/2610.22080-shared-residual-distillation/README.md)
- [OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents](../../../post-training/2610.21496-oprd-reminder/README.md)
- [EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search](../../../post-training/2610.22290-elite-replay/README.md)
- [Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models](../../../post-training/2610.21195-cce-opd/README.md)
- [Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight](../../../post-training/2610.21018-rshd/README.md)
- [LoOPSD: On-Policy Self-Distillation with Looped Teachers](../../../reproductions/2610.18162-loopsd/README.md)
- [Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation](../../../reproductions/2610.13521-road-mopd/README.md)
- [CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation](../../../reproductions/2610.13257-cast-opd/README.md)
- [Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution](../../../post-training/2610.12367-sguid/README.md)
- [MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation](../../../post-training/2610.11989-meta-opd/README.md)
- [Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes](../../../post-training/2610.02117-where-opd/README.md)
- [The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning](../../../post-training/2610.00332-weakest-link/README.md)
- [PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning](../../../post-training/2609.36642-pr-opd/README.md)
- [From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation](../../../post-training/2609.37510-maestro/README.md)
- [LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation](../../../post-training/2610.00333-lego-opd/README.md)
- [AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation](../../../post-training/2609.38142-advisd/README.md)
- [Learning from Teacher Continuations at Student States](../../../post-training/2609.36246-olive/README.md)
- [MAS-OPD: On-Policy Distillation for Multi-Agent Systems](../../../post-training/2609.34234-mas-opd/README.md)
- [OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation](../../../post-training/2609.16459-opd-aha/README.md)
- [Negative Self-Distillation: Learning to Reason by Avoiding Flaws](../../../post-training/2609.11699-nsd/README.md)
- [CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts](../../../post-training/2609.10154-compass-opd/README.md)
- [Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation](../../../post-training/2609.08798-oprd/README.md)
- [Boosting LLM Exploration via Weak-Model Guidance in RLVR](../../../post-training/2608.27420-weak-guide-rlvr/README.md)
- [Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models](../../../post-training/2608.27065-video-opsd/README.md)
- [Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD](../../../post-training/2608.26735-uc-mopd/README.md)
- [Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding](../../../post-training/2608.25356-clue-opsd/README.md)
- [SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation](../../../post-training/2608.03092-smopd/README.md)
- [Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance](../../../post-training/2608.00782-rstg/README.md)
- [VAD](../../../post-training/2607.28590-vad/README.md)
- [Contrastive Reinforced Policy Optimization via Privileged Self-Distillation](../../../post-training/2607.28026-crpo/README.md)
- [Distilled RL](../../../post-training/2607.17247-distilled-rl/README.md)
- [ARMOR](../../../post-training/2607.10481-armor/README.md)
- [MOPD](../../../post-training/2606.30406-mopd/README.md)
- [POLARIS: Guiding Small Models to Write Long Stories](../../../post-training/2606.04095-polaris-hri/README.md)
- [OPCD](../../../post-training/2602.12275-opcd/README.md)
- [OPSD](../../../post-training/2601.18734-opsd/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/teacher-and-context.md) · [返回全部精读卡片](../index.md)
