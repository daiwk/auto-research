---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 同一个GRPO名字之外：优势尺度、裁剪单位与训推失配

[LLM 后训练](../index.md) · 更新 2026-10-27 · 54 篇主题资料 / 6 篇重点对照

GRPO家族的差别可拆成三问：奖励怎样变成优势、哪种概率比被裁剪、样本到底由哪个分布生成。Dr. GRPO、DAPO、GSPO与TIS/IcePop分别改动这些环节，不能把所有ratio都叫同一种off-policy校正。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/post-training/policy-optimization.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：优势尺度：组均值、组标准差、长度归一化 · 更新单位：token surrogate或sequence ratio · 采样有效性：零方差组与动态补采 · 分布角色：当前训练、旧训练、rollout引擎

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [DeepSeekMath / GRPO](../../../post-training/2402.03300-grpo/README.md) · [原始来源](https://arxiv.org/abs/2402.03300)<br>章节：背景与主要改动、核心公式、复现边界 | 用同题组的奖励均值和标准差替代critic，保留old-policy ratio、clip和reference KL。 | 省去价值模型，却需要同题多响应；全组同奖励没有相对方向。本地是完整候选action，不是DeepSeekMath训练。 |
| [Dr. GRPO](../../../post-training/2503.20783-dr-grpo/README.md) · [原始来源](https://arxiv.org/abs/2503.20783)<br>章节：背景与主要改动、核心公式、复现边界 | 去掉response内长度平均和组标准差，保留组内中心化，审查隐含难度与长度权重。 | 去归一化改变不同组与轨迹的梯度相对尺度，不会创造全错组信号；本地伪长度仅用于诊断。 |
| [DAPO](../../../post-training/2503.14476-dapo/README.md) · [原始来源](https://arxiv.org/abs/2503.14476)<br>章节：背景与主要改动、核心公式、复现边界 | 组合Clip-Higher、零方差组过滤、token-level loss和过长奖励处理。 | 有效更新样本与实际生成预算要分别计数；本地长度来自伪token，未复刻长CoT分布式训练。 |
| [GSPO](../../../post-training/2507.18071-gspo/README.md) · [原始来源](https://arxiv.org/abs/2507.18071)<br>章节：背景与主要改动、核心公式、复现边界 | 先对响应内log-ratio取平均再指数化，整条response共享sequence clip。 | 改变异常token如何影响整条轨迹，不等于重新定义奖励；本地没有真实token轨迹或MoE路由。 |
| [TIS](../../../post-training/web-2025-tis/README.md) · [原始来源](https://fengyao.notion.site/off-policy-rl)<br>章节：背景与主要改动、核心公式、复现边界 | 用训练侧与rollout引擎概率比校正训推差异，只对过大权重单侧截断。 | 小ratio仍保留，重尾被限制；它不替代old-policy陈旧校正。本地用确定性引擎扰动验证梯度路径。 |
| [IcePop](../../../post-training/2510.18855-icepop/README.md) · [原始来源](https://arxiv.org/abs/2510.18855)<br>章节：背景与主要改动、核心公式、复现边界 | 对训推ratio使用双侧有效区间，区间内保留原ratio，区间外策略梯度为零。 | 会丢弃严重失配token，而不是把所有ratio夹回边界；本地未运行真实MoE集群。 |

</div>

## 取舍分析 {#analysis}

### 先画概率比的分子分母，再讨论稳定性

GSPO聚合的是当前策略相对旧策略的响应内log-ratio；TIS与IcePop关注相同权重在训练引擎和rollout引擎中的概率差。前者管理策略更新幅度，后者处理采样实现失配。同一训练流程可以同时需要两类因子，不能删掉一种后声称另一种已经覆盖全部偏差。

对照来源：[gspo](../../../post-training/2507.18071-gspo/README.md) · [tis](../../../post-training/web-2025-tis/README.md) · [icepop](../../../post-training/2510.18855-icepop/README.md)

### 归一化改变权重，不等于补上缺失信号

GRPO组标准差、Dr. GRPO移除该尺度、DAPO按有效token汇总，都会改变样本之间的相对贡献。然而同题全对或全错时，中心化后仍可能没有方向。DAPO动态采样处理的是这类组进入更新的问题，代价应把被过滤前的生成也计入，不能仅按optimizer步数对齐成本。

对照来源：[grpo](../../../post-training/2402.03300-grpo/README.md) · [dr-grpo](../../../post-training/2503.20783-dr-grpo/README.md) · [dapo](../../../post-training/2503.14476-dapo/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 同题四条回答全错，把GRPO改成Dr. GRPO就能得到学习方向吗？ {#cross-all-failed-group}

??? note "展开答案与例子"

    **答案：** 若奖励仍完全相同，去掉组标准差也不会改变减均值后全零的事实。Dr. GRPO主要改变尺度偏置，DAPO则会过滤零方差组并继续采样。若预算内始终没有可区分结果，仍需另外解决探索或监督，不能靠重命名归一化获得新信息。

    **教学例子：** 教学例子：奖励全为0时，0减组均值仍为0；把分母从标准差改成常量不会令某条轨迹突然更好。

    对照来源：[grpo](../../../post-training/2402.03300-grpo/README.md) · [dr-grpo](../../../post-training/2503.20783-dr-grpo/README.md) · [dapo](../../../post-training/2503.14476-dapo/README.md)

### GSPO是否等于先逐token做PPO裁剪，再把结果求平均？ {#cross-sequence-ratio-not-token-average}

??? note "展开答案与例子"

    **答案：** 不等于。GSPO先平均log-ratio形成一个响应级ratio，再用它裁剪整条响应；逐token裁剪是先分别作非线性选择。平均与裁剪不能任意交换，某个异常词元在两种流程里的影响不同。序列级奖励也不在数学上强制唯一一种surrogate。

    **教学例子：** 教学例子：一枚token的ratio很高，其余接近一；逐token方案可只裁它，GSPO则依据聚合后的单一ratio决定整条响应的权重。

    对照来源：[grpo](../../../post-training/2402.03300-grpo/README.md) · [gspo](../../../post-training/2507.18071-gspo/README.md) · [dapo](../../../post-training/2503.14476-dapo/README.md)

### 某token的训推ratio非常小，TIS与IcePop会怎样处理，和策略变旧是一回事吗？ {#cross-tis-versus-icepop}

??? note "展开答案与例子"

    **答案：** TIS单侧上截断仍保留这个小权重，IcePop若低于下界会把本次策略梯度置零。它们审查的是训练引擎与rollout引擎的差异；当前权重相对旧采样权重的变化还需另算。不能把区间外mask称作普通PPO clip，也不能用它自动消除策略陈旧。

    **教学例子：** 教学例子：同一份权重因两套kernel给出不同概率，是训推问题；拿几步更新前的权重采样，则另有策略陈旧问题。

    对照来源：[tis](../../../post-training/web-2025-tis/README.md) · [icepop](../../../post-training/2510.18855-icepop/README.md) · [gspo](../../../post-training/2507.18071-gspo/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较GRPO/Dr. GRPO/DAPO的优势与归一化、GSPO序列ratio、TIS/IcePop训推校正；已阅54篇摘要，精读6篇。

覆盖 54 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 54 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback](../../../post-training/2610.30873-moer/README.md)
- [CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents](../../../post-training/2610.29965-cord/README.md)
- [On-Policy Residual Learning for Diffusion Language Models](../../../post-training/2610.20687-orl-diffusion/README.md)
- [Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards](../../../post-training/2610.20814-ggpo/README.md)
- [Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL](../../../reproductions/2610.13020-tapo-trajectory/README.md)
- [Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence](../../../reproductions/2610.13015-gppo-framework/README.md)
- [When KL Regularization Misfires in Group Policy Optimization](../../../post-training/2610.12161-zcpo/README.md)
- [Sharpening Tax in Post-Training](../../../post-training/2610.01509-sharpening-tax/README.md)
- [RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration](../../../post-training/2610.01458-rlcpr/README.md)
- [Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals](../../../post-training/2610.01548-range-grpo/README.md)
- [Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis](../../../post-training/2610.01896-gmc-grpo/README.md)
- [Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training](../../../post-training/2609.37119-rfpo/README.md)
- [Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR](../../../post-training/2609.37868-graft/README.md)
- [Turn-level Multiscale Density Ratio Estimation for LLM Agents](../../../post-training/2609.16760-tlm-dre/README.md)
- [MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning](../../../post-training/2609.31644-mad-rl/README.md)
- [Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning](../../../post-training/2609.11393-tasco/README.md)
- [Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation](../../../post-training/2609.09135-probe-erpo/README.md)
- [TTPO: Test-Time Policy Optimization](../../../post-training/2608.27448-ttpo/README.md)
- [Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms](../../../post-training/2608.27409-rlvr-fusion/README.md)
- [From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection](../../../post-training/2608.25243-grin/README.md)
- [Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization](../../../post-training/2608.23311-erpo/README.md)
- [GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs](../../../post-training/2608.11674-gcpo/README.md)
- [Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models](../../../post-training/2608.01717-erils/README.md)
- [ReCo](../../../post-training/2607.26862-reco/README.md)
- [Reinforcement Learning for Code Optimization](../../../post-training/2607.25970-code-optimization-rl/README.md)
- [Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information](../../../reproductions/2607.19313-off-context-grpo/README.md)
- [ISO: An RLVR-Native Optimization Stack](../../../post-training/2607.19331-iso-rlvr/README.md)
- [RIPO](../../../post-training/2607.10169-ripo/README.md)
- [Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment](../../../reproductions/2607.04728-sis/README.md)
- [STARE](../../../post-training/2606.19236-stare/README.md)
- [KPop](../../../post-training/2606.15079-kpop/README.md)
- [GPRL](../../../post-training/2605.18721-gprl/README.md)
- [ConSPO](../../../post-training/2605.12969-conspo/README.md)
- [Missing Old Logits](../../../post-training/2605.12070-missing-old-logits/README.md)
- [LUSPO](../../../post-training/2602.05261-luspo/README.md)
- [Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning](../../../post-training/2601.13284-calibration-aware-rl/README.md)
- [Online IcePop](../../../post-training/web-2025-online-icepop/README.md)
- [Stabilizing RL with LLMs](../../../post-training/2512.01374-minirl/README.md)
- [IcePop](../../../post-training/2510.18855-icepop/README.md)
- [GPPO](../../../post-training/2508.07629-gppo/README.md)
- [TIS](../../../post-training/web-2025-tis/README.md)
- [GSPO](../../../post-training/2507.18071-gspo/README.md)
- [Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty](../../../post-training/2507.16806-rlcr/README.md)
- [CISPO / MiniMax-M1](../../../post-training/2506.13585-cispo/README.md)
- [TTRL](../../../post-training/2504.16084-ttrl/README.md)
- [LUFFY](../../../post-training/2504.14945-luffy/README.md)
- [VAPO](../../../post-training/2504.05118-vapo/README.md)
- [Dr. GRPO](../../../post-training/2503.20783-dr-grpo/README.md)
- [DAPO](../../../post-training/2503.14476-dapo/README.md)
- [REINFORCE++](../../../post-training/2501.03262-reinforce-plus/README.md)
- [RLOO](../../../post-training/2402.14740-rloo/README.md)
- [DeepSeekMath / GRPO](../../../post-training/2402.03300-grpo/README.md)
- [ReMax](../../../post-training/2310.10505-remax/README.md)
- [InstructGPT / PPO-RLHF](../../../post-training/2203.02155-ppo-rlhf/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/policy-optimization.md) · [返回全部精读卡片](../index.md)
