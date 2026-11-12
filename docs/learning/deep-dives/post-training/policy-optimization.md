---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 同一个GRPO名字之外：优势尺度、裁剪单位与训推失配

[LLM 后训练](../index.md) · 更新 2026-11-12 · 58 篇主题资料 / 10 篇重点对照

GRPO家族的差别可拆成三问：奖励怎样变成优势、哪种概率比被裁剪、样本到底由哪个分布生成。Dr. GRPO、DAPO、GSPO与TIS/IcePop分别改动这些环节，不能把所有ratio都叫同一种off-policy校正。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/post-training/policy-optimization.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：优势尺度：组均值、组标准差、长度归一化 · 更新单位：token surrogate或sequence ratio · 采样有效性：零方差组与动态补采 · 分布角色：当前训练、旧训练、rollout引擎

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [RLiD: Reinforcement Learning in the Decision Plane for Language Agents and LLMs](../../../post-training/2611.02455-rlid/README.md) · [原始来源](https://arxiv.org/abs/2611.02455v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 将优化单位从自由文本改为合法菜单动作概率，单前向label readout后做决策级PPO；同策略内边缘化措辞可去掉对应方差。 | 菜单、记忆和afterstate改变接口；方差恒等式不比较不同模型，也不消除时序信用噪声。本地仅概率/PPO/枚举审计，完整多环境训练成本过高不复现。 |
| [DeepSeekMath / GRPO](../../../post-training/2402.03300-grpo/README.md) · [原始来源](https://arxiv.org/abs/2402.03300)<br>章节：背景与主要改动、核心公式、复现边界 | 用同题组的奖励均值和标准差替代critic，保留old-policy ratio、clip和reference KL。 | 省去价值模型，却需要同题多响应；全组同奖励没有相对方向。本地是完整候选action，不是DeepSeekMath训练。 |
| [Dr. GRPO](../../../post-training/2503.20783-dr-grpo/README.md) · [原始来源](https://arxiv.org/abs/2503.20783)<br>章节：背景与主要改动、核心公式、复现边界 | 去掉response内长度平均和组标准差，保留组内中心化，审查隐含难度与长度权重。 | 去归一化改变不同组与轨迹的梯度相对尺度，不会创造全错组信号；本地伪长度仅用于诊断。 |
| [DAPO](../../../post-training/2503.14476-dapo/README.md) · [原始来源](https://arxiv.org/abs/2503.14476)<br>章节：背景与主要改动、核心公式、复现边界 | 组合Clip-Higher、零方差组过滤、token-level loss和过长奖励处理。 | 有效更新样本与实际生成预算要分别计数；本地长度来自伪token，未复刻长CoT分布式训练。 |
| [GSPO](../../../post-training/2507.18071-gspo/README.md) · [原始来源](https://arxiv.org/abs/2507.18071)<br>章节：背景与主要改动、核心公式、复现边界 | 先对响应内log-ratio取平均再指数化，整条response共享sequence clip。 | 改变异常token如何影响整条轨迹，不等于重新定义奖励；本地没有真实token轨迹或MoE路由。 |
| [TIS](../../../post-training/web-2025-tis/README.md) · [原始来源](https://fengyao.notion.site/off-policy-rl)<br>章节：背景与主要改动、核心公式、复现边界 | 用训练侧与rollout引擎概率比校正训推差异，只对过大权重单侧截断。 | 小ratio仍保留，重尾被限制；它不替代old-policy陈旧校正。本地用确定性引擎扰动验证梯度路径。 |
| [IcePop](../../../post-training/2510.18855-icepop/README.md) · [原始来源](https://arxiv.org/abs/2510.18855)<br>章节：背景与主要改动、核心公式、复现边界 | 对训推ratio使用双侧有效区间，区间内保留原ratio，区间外策略梯度为零。 | 会丢弃严重失配token，而不是把所有ratio夹回边界；本地未运行真实MoE集群。 |
| [Not All Entropy Is Equal: Reward-Conditioned Entropy Allocation in Reinforcement Learning with Verifiable Rewards](../../../post-training/2611.09448-rcea/README.md) · [原始来源](https://arxiv.org/abs/2611.09448)<br>章节：核心公式、原文结果与限制、诊断与边界 | 不改更新目标，先按验证结果、过程有效性和解法模式拆开轨迹熵，再用同前缀协方差解释局部变化方向。 | 精确分解需要确定性分区；局部协方差不是策略模式或因果归因。CPU 只覆盖数值核，未跑多目标 RLVR 矩阵。 |
| [Off-policy Learning with Excursion Policies](../../../post-training/2611.13275-excursion-td/README.md) · [原始来源](https://arxiv.org/abs/2611.13275v1)<br>章节：核心公式、数据协议与代码映射、结果、负控与边界 | 对目标策略持续若干步后永久回到行为策略的 excursion 时长作混合，以递归权重构造 Ex-TD/Ex-Retrace；本地计算5状态3动作精确算子和实际轨迹target。 | beta在目标偏差、方差与收缩间取舍，不是TIS的训推引擎ratio截断；中间beta不保证目标固定点无偏。完整七任务MPO每run约12小时不复现。 |
| [A Theory of Policy Optimization in Post-Training: Coverage Collapse and Reference Resets](../../../post-training/2611.14467-apmd-reference-reset/README.md) · [原始来源](https://arxiv.org/abs/2611.14467v1)<br>章节：核心公式、结果、负控与边界、理论与实验范围 | 每轮把KL reference更新为最新策略，再近似求解reference×exp(eta×reward)的镜像目标；有限核检查精确重置路径、Kimi均值baseline的平方KL偏差与Rebel=2×centered-MSE。 | 参考重置不等于刷新PPO/GRPO old policy，也不等于把学生退回base；保证依赖策略/reward可实现性及内层精度。纯理论无大型实证方案，不编高成本或把数值检查当完整证明。 |

</div>

## 取舍分析 {#analysis}

### 先画概率比的分子分母，再讨论稳定性

GSPO聚合的是当前策略相对旧策略的响应内log-ratio；TIS与IcePop关注相同权重在训练引擎和rollout引擎中的概率差。前者管理策略更新幅度，后者处理采样实现失配。同一训练流程可以同时需要两类因子，不能删掉一种后声称另一种已经覆盖全部偏差。

对照来源：[gspo](../../../post-training/2507.18071-gspo/README.md) · [tis](../../../post-training/web-2025-tis/README.md) · [icepop](../../../post-training/2510.18855-icepop/README.md)

### 归一化改变权重，不等于补上缺失信号

GRPO组标准差、Dr. GRPO移除该尺度、DAPO按有效token汇总，都会改变样本之间的相对贡献。然而同题全对或全错时，中心化后仍可能没有方向。DAPO动态采样处理的是这类组进入更新的问题，代价应把被过滤前的生成也计入，不能仅按optimizer步数对齐成本。

对照来源：[grpo](../../../post-training/2402.03300-grpo/README.md) · [dr-grpo](../../../post-training/2503.20783-dr-grpo/README.md) · [dapo](../../../post-training/2503.14476-dapo/README.md)

### 更新单位先于裁剪公式：文本和决策不是同一变量

GRPO/GSPO主要调整既有文本策略的优势或ratio单位，RLiD先把被优化的概率事件改成编译菜单中的动作。其Rao-Blackwell解释只在同一文本策略里对同动作措辞求条件期望；不能凭这个恒等式断言另训LDM更强。菜单是否包含afterstate、记忆来自何处、标签校准及接口对齐，都需在比较前写清；PPO公式相同并不能抹去这些差别。

对照来源：[rlid](../../../post-training/2611.02455-rlid/README.md) · [grpo](../../../post-training/2402.03300-grpo/README.md) · [gspo](../../../post-training/2507.18071-gspo/README.md)

### 先确认离策略发生在哪一层，再选择校正

TIS比较同一权重在training与rollout引擎产生的概率，处理数值实现失配；Ex-Retrace比较目标策略与行为策略，按整段excursion持续时间构造多步值target。两者都出现重要性比，不表示可交换：逐token训推ratio不能直接替代状态动作价值target里的持续时长前缀，后者也不消除LM训练引擎的数值差异。

对照来源：[excursion-td](../../../post-training/2611.13275-excursion-td/README.md) · [tis](../../../post-training/web-2025-tis/README.md)

### old policy负责采样比，KL reference决定优化锚点，二者不能混称旧模型

GRPO用old-policy ratio和组优势形成更新，同时另有reference KL；APMD讨论的是KL锚点随外层迭代重置，允许在强局部约束下累积前进。刷新采样行为的old policy不自动满足APMD的reference条件，组内去均值也不消除Kimi均值baseline相对镜像目标的平方KL偏差。这里的有限响应恒等式不能替代真实LLM的假设核验或采样误差分析。

对照来源：[apmd-reference-reset](../../../post-training/2611.14467-apmd-reference-reset/README.md) · [grpo](../../../post-training/2402.03300-grpo/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 把文本映射到动作后方差下降，为什么不意味着RLiD在每个任务都胜过带推理token的策略？ {#cross-same-policy-marginalization-not-new-model-win}

??? note "展开答案与例子"

    **答案：** 该结论固定同一个文本策略和只依赖动作的优势，边缘化措辞后保持期望更新并删去措辞方差。真正LDM有不同参数化和训练路径，文本推理还提供额外计算；时序信用和菜单接口也未被恒等式解决。论文ARC的Qwen3.5-2B上token策略仍更高，必须保留这个反例。

    **教学例子：** 教学例：一个策略用两种句子表达open可被边缘化；把它换成另一个只看label的网络，已超出同策略恒等式的比较范围。

    对照来源：[rlid](../../../post-training/2611.02455-rlid/README.md) · [grpo](../../../post-training/2402.03300-grpo/README.md)

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

### TIS的单侧ratio截断能否直接替代Ex-Retrace？ {#cross-engine-ratio-versus-excursion}

??? note "展开答案与例子"

    **答案：** 不能。TIS校正training/rollout引擎概率失配；Ex-Retrace定义目标/行为策略之间多步价值target，并对先目标后行为的时长混合。必须先对齐分子、分母、条件变量和更新对象。

    **教学例子：** 教学例：两个引擎给同一token .2与.1时TIS比为2；Ex-Retrace里的比则比较给定状态下目标与行为动作概率，还需要gamma、lambda、beta和后续Q值。

    对照来源：[excursion-td](../../../post-training/2611.13275-excursion-td/README.md) · [tis](../../../post-training/web-2025-tis/README.md)

### GRPO已经周期更新old policy，为什么还不能说实现了APMD reference reset？ {#cross-cross-old-policy-versus-kl-anchor-reset}

??? note "展开答案与例子"

    **答案：** old policy在概率比分母中记录行为分布；KL reference是正则化锚点。两者可不同步，且APMD还要求近似解满足内层误差条件，不能因名字都叫旧模型就认为等价。

    **教学例子：** 教学例：每批采样前刷新old policy，但KL始终惩罚偏离最初base，仍是固定reference；APMD下一轮锚定最新pi_t。

    对照来源：[apmd-reference-reset](../../../post-training/2611.14467-apmd-reference-reset/README.md) · [grpo](../../../post-training/2402.03300-grpo/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-12** · 补审coverage/reference-reset理论，分清行为old policy、KL reference和student初始化；增加Kimi偏差与Rebel中心化恒等式。仅CPU精确有限核，纯理论大型实证不适用，不宣称普适GRPO收敛。

涉及：[apmd-reference-reset](../../../post-training/2611.14467-apmd-reference-reset/README.md)

**2026-11-11** · 加入 Google DeepMind 相关 Excursion TD，区分持续时长混合与逐动作混合，也区分目标/行为校正与 TIS 训推引擎校正；实现可负担的表格型核心，完整约12小时/run的控制实验不复现。

涉及：[excursion-td](../../../post-training/2611.13275-excursion-td/README.md)

**2026-11-09** · 加入 RCEA，把策略优化目标与熵诊断分开。全局熵变小不能证明正确策略模式变少，本地只验证轨迹链式分解与局部一阶近似。

涉及：[rcea](../../../post-training/2611.09448-rcea/README.md)

**2026-11-04** · 精读RLiD，增加文本概率事件与可执行动作事件这一比较轴，明确同策略方差边缘化不等于不同LDM优越性，并补充标签边际KL与逐行entropy的区别；仅L1组件，完整训练成本过高不复现。

涉及：[rlid](../../../post-training/2611.02455-rlid/README.md)

**2026-10-27** · 首版：比较GRPO/Dr. GRPO/DAPO的优势与归一化、GSPO序列ratio、TIS/IcePop训推校正；已阅54篇摘要，精读6篇。

覆盖 54 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 58 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Not All Entropy Is Equal: Reward-Conditioned Entropy Allocation in Reinforcement Learning with Verifiable Rewards](../../../post-training/2611.09448-rcea/README.md)
- [RLiD: Reinforcement Learning in the Decision Plane for Language Agents and LLMs](../../../post-training/2611.02455-rlid/README.md)
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
- [Off-policy Learning with Excursion Policies](../../../post-training/2611.13275-excursion-td/README.md)
- [A Theory of Policy Optimization in Post-Training: Coverage Collapse and Reference Resets](../../../post-training/2611.14467-apmd-reference-reset/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/policy-optimization.md) · [返回全部精读卡片](../index.md)
