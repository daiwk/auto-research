# LLM 后训练论文与资料索引

本页由统一论文规格生成的 `docs/research-manifest.json` 构建；元数据维护入口是
打包的 `paper.yaml` 和按领域保存的 catalog 规格，不直接编辑生成产物。
背景、架构、公式、原文效果和本地实验请进入独立详情页。

## 论文实现与研究资料

<div class="ar-method-index" markdown>

| 方向 | 方法 | 一作机构与日期 | 原作者代码 | 本地入口 |
|---|---|---|---|---|
| On-policy distillation | [GIFT: Gradient Informed Filtering for Distillation Augmented Reasoning RL](2610.30796-gift/README.md) | Shanghai Jiao Tong University，2026-10-22 | [原作者入口](https://github.com/lilifree/GIFT)；原作者源码可见；固定5e9a9dfdb371b7368949abbdc3a846d23a546557未找到第一方LICENSE/COPYING，GitHub license=null；未确认开放许可，不复制作者源码。本地根据论文独立实现 | `gift`：仅低成本组件，完整实验不复现 |
| 后训练算法组件 | [MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback](2610.30873-moer/README.md) | City University of Hong Kong，2026-10-22 | [原作者入口](https://github.com/CityU-MLO/MOER)；原作者已发布可见源码；固定7dafbe33118e61597a4f0186d538c1630430c0be，无根LICENSE，仅有嵌套上游许可，作者新增代码许可未确认；本地据论文独立重写，不复制上游代码 | `moer`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [UserArena: Benchmarking Interactive User Simulation for Long-Horizon Shopping Agents](2610.30932-userarena-optd/README.md) | Leiden University，2026-10-22 | [原作者入口](https://github.com/RecGPT-Team/UserArena)；原作者发布环境、评测及OPTD源码，固定d37e3c062d30950f2a3744c66a18fda9aa72c1f7；非商业研究且禁止未经授权再分发，本地只据论文独立实现损失，不复制上游代码或数据 | `userarena-optd`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [When to Follow the Teacher: Advantage-Based On-Policy Distillation](2610.31563-aopd/README.md) | University of Pennsylvania，2026-10-22 | [原作者入口](https://github.com/Helloworld10011/AOPD)；原作者代码已发布，固定3f205368f225bfc4ed4ad007ccbae7879d1b38f2，Apache-2.0；本地据论文独立实现Eq3.8，不混入上游sigmoid residual与all-wrong KL附加项 | `aopd`：仅低成本组件，完整实验不复现 |
| Agentic RL | [CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents](2610.29965-cord/README.md) | The Chinese University of Hong Kong，2026-10-21 | [原作者入口](https://github.com/LvAoAo/CORD-release)；原论文首页链接原作者开源仓库；固定快照的cord_utils实现保护第一目标的冲突投影，论文另定义交换保护方向与always门控 | `cord`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation](2610.28194-ap-opd/README.md) | Nanjing University，2026-10-20 | 未发现官方代码 | `ap-opd`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Ask to Distill: Learning to Synthesize Data for On-Policy Distillation](2610.27450-ask-to-distill/README.md) | University of Illinois Urbana-Champaign，2026-10-20 | [原作者入口](https://github.com/GasolSun36/Ask_to_Distill)；原作者公开代码、数据和模型；固定版本核验reward_worker与diversity接口 | `ask-to-distill`：仅低成本组件，完整实验不复现 |
| 知识蒸馏 | [CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer](2610.28895-csd/README.md) | NVIDIA，2026-10-20 | [原作者入口](https://github.com/NVIDIA-NeMo/RL/pull/4680)；正文脚注链接原作者公开PR4680；固定head可读取CSD loss与sub-token工具，核对时PR仍open，不将其标成已合并发布或完整GPU qualification | `csd`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [On-Policy Transition Distillation](2610.28048-optd/README.md) | The Hong Kong Polytechnic University，2026-10-20 | [原作者入口](https://github.com/ModalityDance/optd)；原作者已发布源码；PDF首页链接已核对，仓库包含verl训练代码、配置与测试 | `optd`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Projected Distillation: On Learning to Solve Hard Problems from Close, Correct Targets](2610.27467-projected-distillation/README.md) | University of Massachusetts，2026-10-20 | 未发现官方代码 | `projected-distillation`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization](2610.25973-apsd/README.md) | Korea University，2026-10-19 | 未发现官方代码 | `apsd`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Reinforcement Learning with Visually Attributable On-Policy Self-Distillation](2610.26856-vag/README.md) | Baidu Inc.，2026-10-19 | 未发现官方代码 | 计划键 `visually-attributable-opd`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| On-policy distillation | [Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation](2610.25034-spod/README.md) | University of Southern California，2026-10-18 | [原作者入口](https://github.com/Jike338/SPOD)；作者官方仓库已发布configs、spod训练与sgate方法源码；不是仅占位README | `spod`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [GR-OPD: Group-Relative Sequence Credit for On-Policy Distillation](2610.23042-gr-opd/README.md) | Shanghai Jiao Tong University，2026-10-16 | 未发现官方代码 | `gr-opd`：仅低成本组件，完整实验不复现 |
| RLVR | [MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning](2610.23245-mge-po/README.md) | 论文未列机构（不据邮箱域名推断），2026-10-16 | 未发现官方代码 | 计划键 `mge-po`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| Agentic RL | [MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation](2610.23234-multiagent-opd/README.md) | Alibaba Group，2026-10-16 | 未发现官方代码 | 计划键 `multiagent-opd`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| RLVR | [Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay](2610.24236-tar-adaptive-replay/README.md) | Cornell University，2026-10-16 | [原作者入口](https://github.com/wenzhilics/tar)；作者官方仓库已发布基于verl的recipe/tar训练与memory-bank构建代码 | `tar-adaptive-replay`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [SimOPD: Relational Knowledge Transfer for On-Policy Distillation](2610.23306-simopd/README.md) | Zhejiang University，2026-10-16 | 未发现官方代码 | `simopd`：仅低成本组件，完整实验不复现 |
| Agentic RL | [Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning](2610.23181-treeopsd/README.md) | Tsinghua University，2026-10-16 | 未发现官方代码 | `treeopsd`：仅低成本组件，完整实验不复现 |
| 二元反馈对齐 | [CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF](2610.21138-clean-rm/README.md) | Zhejiang University，2026-10-15 | [原作者入口](https://anonymous.4open.science/r/CAN-RM-46BB)；论文提供匿名代码入口，但本轮访问失败，未核验其内容、许可证或可运行性；本地按公式独立实现 | `clean-rm`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation](2610.21234-token-teacher-selection/README.md) | Princeton University，2026-10-15 | 未发现官方代码 | `token-teacher-selection`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models](2610.21195-cce-opd/README.md) | The Chinese University of Hong Kong, Shenzhen，2026-10-15 | 未发现官方代码 | `cce-opd`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Does On-Policy Distillation Need to Complete Every Rollout?](2610.21337-stopd/README.md) | Cornell University，2026-10-15 | 未发现官方代码 | `stopd`：仅低成本组件，完整实验不复现 |
| RLHF / RLVR | [Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL](2610.21439-mrtpo/README.md) | University of Minnesota，2026-10-15 | [原作者入口](https://github.com/zhaihaotian/MRTPO)；已找到并核对原作者 MRTPO 官方实现，包含三个任务训练及重放可视化 | `mrtpo`：仅低成本组件，完整实验不复现 |
| Reference anchor | [EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search](2610.22290-elite-replay/README.md) | The Ohio State University，2026-10-15 | [原作者入口](https://github.com/skai-research/EliteReplay)；原作者公开代码与实验资料；本地独立实现目标导向 MAP-Elites 与 replay 算法组件 | `elite-replay`：仅低成本组件，完整实验不复现 |
| Agentic RL | [KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents](2610.22331-knowgpo/README.md) | Zhejiang University，2026-10-15 | [原作者入口](https://github.com/ZJU-REAL/KnowGPO)；原作者官方占位仓库；仅 assets、LICENSE 和 README，方法代码待发布，不能标作训练实现已开源 | `knowgpo`：仅低成本组件，完整实验不复现 |
| On-policy self-distillation | [Learning from Unverified Peers via Shared Residual Distillation](2610.22080-shared-residual-distillation/README.md) | Shanghai Jiao Tong University，2026-10-15 | 未发现官方代码 | `shared-residual-distillation`：仅低成本组件，完整实验不复现 |
| 自置信轨迹过滤 | [Learning to Reason with Selective Internal Feedback](2610.21392-sif/README.md) | Institute of Automation, Chinese Academy of Sciences，2026-10-15 | 未发现官方代码 | `sif`：仅低成本组件，完整实验不复现 |
| RLHF / RLVR | [Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense](2610.21404-tag-reward-gating/README.md) | University of British Columbia，2026-10-15 | 未发现官方代码 | `tag-reward-gating`：仅低成本组件，完整实验不复现 |
| Agentic RL | [OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering](2610.21345-opcredit/README.md) | Nanjing University，2026-10-15 | [原作者入口](https://github.com/kaka1215/OpCredit)；原作者已公开 BOC/FTC、训练适配与数据准备代码；配置模板未填，正式评测脚本未随仓库发布 | `opcredit`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents](2610.21496-oprd-reminder/README.md) | Tsinghua University，2026-10-15 | 未发现官方代码 | `oprd-reminder`：仅低成本组件，完整实验不复现 |
| 过程奖励 | [Progress Reward Model for Reinforcement Learning via Large Language Models](2610.22056-progress-reward/README.md) | Beihang University，2026-10-15 | [原作者入口](https://github.com/deng-ai-lab/PRM4RL)；原作者公开 PRM4RL 仓库；本地按公式独立实现，不执行上游生成的任意 Python | `progress-reward`：仅低成本组件，完整实验不复现 |
| RLHF / RLVR | [Training Reasoning Models to Generate Diverse Scientific Ideas](2610.22324-diverge-ideation/README.md) | New York University，2026-10-15 | [原作者入口](https://github.com/ManyaWadhwa/diverge_ideation)；原作者官方占位仓库；当前仅 README，代码、数据和模型待发布，代码许可未确认 | `diverge-ideation`：CPU 评测接口，不执行模型 |
| 多教师能力整合 | [Training-Free On-Policy Distillation](2610.22236-tf-opd/README.md) | University of Illinois Urbana-Champaign，2026-10-15 | 未发现官方代码 | `tf-opd`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation](2610.21601-waypoint-opd/README.md) | Alibaba Cloud Computing，2026-10-15 | [原作者入口](https://github.com/hhhbxloveai/WaypointOPD)；原作者公开仓库；未确认明确许可证，不vendor；从公式独立实现 | `waypoint-opd`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Divergence-Routed On-Policy Distillation for Language Models](2610.19572-divergence-routed-opd/README.md) | Peking University，2026-10-14 | 未发现官方代码 | `divergence-routed-opd`：仅低成本组件，完整实验不复现 |
| RLHF / RLVR | [Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight](2610.21018-rshd/README.md) | University of California, San Diego，2026-10-14 | 未发现官方代码 | `rshd`：仅低成本组件，完整实验不复现 |
| 离策略推理 RL | [Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards](2610.20814-ggpo/README.md) | University of Illinois Urbana-Champaign，2026-10-14 | [原作者入口](https://github.com/thunderous77/GGPO)；原作者公开Apache-2.0仓库；本地按公式独立实现 | `ggpo`：仅低成本组件，完整实验不复现 |
| On-policy distillation | [Information-Gain Calibrated On-Policy Distillation for Deep Search Agents](2610.20664-ig-opd/README.md) | The Chinese University of Hong Kong, Shenzhen，2026-10-14 | 未发现官方代码 | `ig-opd`：仅低成本组件，完整实验不复现 |
| 扩散语言模型后训练 | [On-Policy Residual Learning for Diffusion Language Models](2610.20687-orl-diffusion/README.md) | Together AI / University of Illinois Urbana-Champaign，2026-10-14 | [原作者入口](https://github.com/Introspective-Diffusion/ORL)；已发布作者ORL代码；系统内核和完整实验仍需对应加速器、模型与训练预算 | 计划键 `orl-diffusion`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 偏好图信用分配 | [When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO](2610.20089-rap-walk/README.md) | 未确认（已读 arXiv HTML 未列机构），2026-10-14 | 未发现官方代码 | `rap-walk`：仅低成本组件，完整实验不复现 |
| on-policy-self-distillation | [LoOPSD: On-Policy Self-Distillation with Looped Teachers](../reproductions/2610.18162-loopsd/README.md) | Anhui Province Key Laboratory of Digital Security，2026-10-13 | 未发现官方代码 | 计划键 `loopsd`：成本过高，暂不复现；待验收，未注册可执行入口。 |
| GRPO difficulty curriculum | [A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO](../reproductions/2610.13669-grpo-difficulty-curriculum/README.md) | Dalian Maritime University，2026-10-09 | [已开源](https://github.com/NHLling/GRPO-B) | `grpo-difficulty-curriculum` |
| Multi-teacher distillation | [Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation](../reproductions/2610.13521-road-mopd/README.md) | Nanjing University / JD.com，2026-10-09 | 未发现官方代码 | `road-mopd` |
| Capability boundary | [BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation](../reproductions/2610.13285-boundary-evo/README.md) | Shanghai Artificial Intelligence Laboratory，2026-10-09 | 未发现官方代码 | `boundary-evo` |
| On-policy distillation | [Branching On-Policy Distillation](../reproductions/2610.13481-branch-opd/README.md) | Tsinghua University / SenseTime Research，2026-10-09 | 未发现官方代码 | `branch-opd` |
| Cross-tokenizer distillation | [CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation](../reproductions/2610.13257-cast-opd/README.md) | Taobao & Tmall Group of Alibaba，2026-10-09 | 未发现官方代码 | `cast-opd` |
| Synthetic self-distillation | [Continually Post-training Small Models via Synthetic Self-distillation](../reproductions/2610.13113-synthself/README.md) | KAIST AI / LG AI Research，2026-10-09 | 未发现官方代码 | `synthself` |
| Proximal policy optimization | [Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence](../reproductions/2610.13015-gppo-framework/README.md) | Tsinghua University AIR，2026-10-09 | 未发现官方代码 | `gppo-framework` |
| Self-correction | [Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction](../reproductions/2610.13672-upturn/README.md) | KAIST，2026-10-09 | 未发现官方代码 | `upturn` |
| Monte Carlo reasoning tree | [Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training](../reproductions/2610.12933-progressive-contraction/README.md) | National University of Singapore / Nanjing University，2026-10-09 | 未发现官方代码 | `progressive-contraction` |
| Source-aware RL | [SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents](../reproductions/2610.13157-soar/README.md) | Zhejiang University / Microsoft，2026-10-09 | 未发现官方代码 | `soar` |
| On-policy distillation | [State-OPD: State-Grounded On-Policy Distillation for Multi-Turn Agents](../reproductions/2610.13238-state-opd/README.md) | Alibaba Group，2026-10-09 | 未发现官方代码 | `state-opd` |
| Trajectory-aware policy optimization | [Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL](../reproductions/2610.13020-tapo-trajectory/README.md) | Tsinghua University AIR，2026-10-09 | 未发现官方代码 | `tapo-trajectory` |
| On-policy distillation | [DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation](2610.11659-dial-opd/README.md) | Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University，2026-10-08 | [已开源](https://github.com/EIT-NLP/DIAL-OPD) | `dial-opd` |
| RLVR | [GRPODropout: Less is More for Online Reinforcement Learning Rollouts](2610.11854-grpo-dropout/README.md) | Harbin Institute of Technology (Shenzhen)，2026-10-08 | [已开源](https://github.com/hexuandeng/GRPODropout) | `grpo-dropout` |
| RLVR data synthesis | [MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis](../reproductions/2610.12659-magicbeanstalk/README.md) | University of Washington，2026-10-08 | 未发现官方代码 | 计划键 `magicbeanstalk`：成本过高，暂不复现；待验收，未注册可执行入口。 |
| On-policy distillation | [MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation](2610.11989-meta-opd/README.md) | East China Normal University，2026-10-08 | 未发现官方代码 | `meta-opd` |
| On-policy 蒸馏 | [PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation](2610.11167-pivot/README.md) | Ping An Technology / University of Science and Technology of China，2026-10-08 | 未发现官方代码 | `pivot` |
| On-policy distillation | [ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery](2610.11332-recal/README.md) | Zhongguancun Academy / Tencent / University of Science and Technology of China，2026-10-08 | [已开源](https://github.com/jianghoucheng/ReCal) | `recal` |
| RLVR | [Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards](2610.11519-residual-advantage/README.md) | Harbin Engineering University / Tencent / Harbin Institute of Technology，2026-10-08 | 未发现官方代码 | `residual-advantage` |
| On-policy distillation | [When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better](2610.11291-semi-opd/README.md) | UCLA / NVIDIA（论文注明实习），2026-10-08 | 未发现官方代码 | `semi-opd` |
| 组相对策略优化 | [When KL Regularization Misfires in Group Policy Optimization](2610.12161-zcpo/README.md) | Alibaba Group，2026-10-08 | 未发现官方代码 | `zcpo` |
| On-policy self-distillation | [Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution](2610.12367-sguid/README.md) | New York University，2026-10-08 | 未发现官方代码 | `sguid` |
| On-policy distillation | [Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals](2610.11247-opd-learning-signals/README.md) | University of Pennsylvania，2026-10-08 | [已开源](https://github.com/leizhao7/opd-learning-signals) | `opd-learning-signals` |
| Agentic RL | [Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT](2610.03361-follow-the-winners/README.md) | Trent AI Limited，2026-10-02 | 未发现官方代码 | `follow-the-winners` |
| 后训练数据选择 | [LESSER: Post-Training Data Selection with Output-Layer Gradients](2610.03702-lesser/README.md) | University of Pennsylvania，2026-10-02 | 未发现官方代码 | `lesser` |
| 异步 RL | [Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis](2610.01896-gmc-grpo/README.md) | The Ohio State University，2026-10-01 | 未发现官方代码 | `gmc-grpo` |
| RLVR | [CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning](2610.02039-carm/README.md) | Moore Threads AI，2026-10-01 | 未发现官方代码 | `carm` |
| Agentic RL | [Dependency-Aware Reward Shaping for Agentic Reinforcement Learning](2610.01207-dars/README.md) | University of Illinois Urbana-Champaign，2026-10-01 | 未发现官方代码 | `dars` |
| 偏好优化 | [GAW-PO: Preference Optimization with Gradient-Aligned Token Weights](2610.01511-gaw-po/README.md) | National University of Science and Technology POLITEHNICA Bucharest，2026-10-01 | 未发现官方代码 | `gaw-po` |
| Agentic RL | [My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning](2610.01161-my-fault/README.md) | Alibaba Group，2026-10-01 | 未发现官方代码 | `my-fault` |
| GRPO | [Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals](2610.01548-range-grpo/README.md) | Yonsei University，2026-10-01 | 未发现官方代码 | `range-grpo` |
| 后验集中与长度约束 | [RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration](2610.01458-rlcpr/README.md) | National University of Singapore，2026-10-01 | 未发现官方代码 | `rlcpr` |
| RL 后训练 | [Sharpening Tax in Post-Training](2610.01509-sharpening-tax/README.md) | Meta Superintelligence Labs / University of Wisconsin–Madison，2026-10-01 | [已开源](https://github.com/changdaeoh/sharpening-tax) | `sharpening-tax` |
| 视频生成 | [Token-Level Video Reinforcement Learning](2610.01973-tvrl/README.md) | 原文首页未列第一作者机构，2026-10-01 | 未发现官方代码 | `tvrl` |
| 多模态后训练 | [Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes](2610.02117-where-opd/README.md) | Valeo.ai，2026-10-01 | [已开源](https://github.com/sirkosophia/Where-OPD) | `where-opd` |
| Agentic RL | [SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning](2610.00838-sharpo/README.md) | Georgia Institute of Technology，2026-09-30 | 未发现官方代码 | `sharpo` |
| 轨迹到步骤信用分配 | [T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning](2610.00388-t2spo/README.md) | Nanjing University，2026-09-30 | 未发现官方代码 | `t2spo` |
| Advisor | [AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation](2609.38142-advisd/README.md) | University of Southern California，2026-09-29 | 未发现官方代码 | `advisd` |
| On-policy distillation | [Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models](2609.38025-dr-opd/README.md) | Rutgers University，2026-09-29 | [已开源](https://github.com/zywang0701/Dr-OPD) | `dr-opd` |
| OPD | [DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies](2610.00317-drift-opd/README.md) | KAIST，2026-09-29 | 未发现官方代码 | `drift-opd` |
| On-policy distillation | [FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators](2609.37851-flowmap-opd/README.md) | Georgia Institute of Technology，2026-09-29 | [已开源](https://github.com/ZhiqiLi-CG/Flowmap_OPD_source) | `flowmap-opd` |
| On-policy distillation | [From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation](2609.37510-maestro/README.md) | Nanyang Technological University，2026-09-29 | [已开源](https://github.com/yhao-wang/MAESTRO) | `maestro-opd` |
| Agentic RL | [Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL](2609.37898-gats/README.md) | Dalian University of Technology / Kuaishou，2026-09-29 | [已开源](https://github.com/Ricardo-H/guide-then-let-go) | `gats` |
| 策略蒸馏 | [Interpolated Policy Distillation: A Controllable Continuum Between Off-Policy and On-Policy Distillation](2609.37170-ipd/README.md) | WeChat Vision, Tencent，2026-09-29 | 未发现官方代码 | `ipd` |
| RLVR | [Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR](2609.37868-graft/README.md) | KAIST，2026-09-29 | 未发现官方代码 | `graft` |
| OPD | [LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation](2610.00333-lego-opd/README.md) | KAIST，2026-09-29 | 未发现官方代码 | `lego-opd` |
| On-policy self-distillation | [Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning](2609.37915-oasis/README.md) | North South University，2026-09-29 | 未发现官方代码 | `oasis-opsd` |
| Agentic RL | [PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning](2609.36642-pr-opd/README.md) | University of Florida，2026-09-29 | [已开源](https://github.com/balibata/PR-OPD) | `pr-opd` |
| RLVR | [SIPO: Unifying Reinforcement Learning with On-Policy Self-Distillation](2609.36742-sipo/README.md) | University of Illinois Urbana-Champaign，2026-09-29 | [已开源](https://github.com/Yueeeeeeee/SIPO) | `sipo` |
| On-policy distillation | [The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation](2609.36484-ride/README.md) | 原文未列机构，2026-09-29 | [已开源](https://github.com/xixixixixxxx/RIDE) | `ride-opd` |
| 教师前缀约束蒸馏 | [The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning](2610.00332-weakest-link/README.md) | Huawei Noah’s Ark Lab，2026-09-29 | 未发现官方代码 | `weakest-link` |
| RL | [Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training](2609.37119-rfpo/README.md) | University of Luxembourg，2026-09-29 | 未发现官方代码 | `rfpo` |
| On-policy distillation | [An RL View of OPD: Least Square Policy Distillation for Sample-Efficient LLM Reasoning](2609.35505-lspd/README.md) | University of North Carolina at Chapel Hill，2026-09-28 | [已开源](https://github.com/UNCSciML/LSPD) | `lspd` |
| 在线蒸馏 | [Learning from Teacher Continuations at Student States](2609.36246-olive/README.md) | University of Illinois Urbana-Champaign，2026-09-28 | [已开源](https://dylanzsz.github.io/olive/) | `olive` |
| 多 Agent | [MAS-OPD: On-Policy Distillation for Multi-Agent Systems](2609.34234-mas-opd/README.md) | University of Science and Technology of China，2026-09-28 | 未发现官方代码 | `mas-opd` |
| 离线 SFT | [ROSS: Relearning from Self-Generated Rollouts through Selective Supervision](2609.35954-ross/README.md) | AllSpark Team（原文以团队署名，未列机构），2026-09-28 | 未发现官方代码 | `ross` |
| 自我回顾 | [Shockingly Simple Self-retrospection Improves Agentic Models Without RL](2609.35741-roft/README.md) | Rensselaer Polytechnic Institute，2026-09-28 | 未发现官方代码 | `roft` |
| On-policy self-distillation | [Recursive Self-Improvement via On-Policy Distillation for Reasoning](../reproductions/2609.30652-recursive-opsd/README.md) | Meta AI / University of California, Riverside，2026-09-25 | 未发现官方代码 | `recursive-opsd` |
| 强化学习 | [PACT: From Credit Assignment to Critic Alignment](2609.26355-pact/README.md) | AllSpark Team，2026-09-22 | 未发现官方代码 | `pact` |
| On-policy distillation | [RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning](2609.20784-retire-opd/README.md) | Zhejiang University，2026-09-17 | [已开源](https://github.com/ZJU-REAL/SDAR) | `retire-opd` |
| 偏好优化 | [A Zeroth-Order Paradigm for LLM Preference Alignment](2609.19144-compo/README.md) | University of California, Berkeley，2026-09-16 | 未发现官方代码 | `compo` |
| On-policy distillation | [Trajectory Learnability for Offline On-Policy Distillation](2609.18321-trajectory-learnability/README.md) | National University of Singapore，2026-09-16 | 未发现官方代码 | `trajectory-learnability` |
| On-policy distillation | [Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation](2609.16937-gamma-opd/README.md) | Tsinghua University / DiDi Voyager Labs，2026-09-15 | 未发现官方代码 | `gamma-opd` |
| RL 训练加速 | [GrowMTP: Can RL Grow Its Own Draft Head?](2609.16648-growmtp/README.md) | WeChat AI, Tencent / Peking University，2026-09-15 | 未发现官方代码 | `growmtp` |
| 多模态后训练 | [OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation](2609.16459-opd-aha/README.md) | Arizona State University / University of Virginia / Stevens Institute of Technology，2026-09-15 | [已开源](https://github.com/Echochef/OPD-Aha) | `opd-aha` |
| 偏好优化 | [Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data](2609.16532-sd-dpo/README.md) | Waseda University，2026-09-15 | 未发现官方代码 | `sd-dpo` |
| 强化学习 | [TIAO: Token Importance-Aware Policy Optimization for Text Summarization](2609.16748-tiao/README.md) | National University of Defense Technology，2026-09-15 | [已开源](https://github.com/TechCloud-x/TIAO) | `tiao` |
| 多轮 Agent 对齐 | [Turn-level Multiscale Density Ratio Estimation for LLM Agents](2609.16760-tlm-dre/README.md) | Alibaba Group，2026-09-15 | 未发现官方代码 | `tlm-dre` |
| On-policy distillation | [Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation](2609.14636-stride-opd/README.md) | University of Science and Technology of China / Ant Group，2026-09-13 | 未发现官方代码 | `stride-opd` |
| On-policy distillation | [Data-free On-policy Distillation](2609.14193-df-opd/README.md) | Institute of Automation, Chinese Academy of Sciences / Tencent，2026-09-12 | 未发现官方代码 | `df-opd` |
| 在线强化学习 | [MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning](2609.31644-mad-rl/README.md) | Meta Superintelligence Labs，2026-09-12 | 未发现官方代码 | 计划键 `mad-rl`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| On-policy distillation | [A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients](2609.11768-adaptive-opd-gate/README.md) | Xiaohongshu，2026-09-10 | 未发现官方代码 | `adaptive-opd-gate` |
| 测试时适配 | [Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning](2609.11393-tasco/README.md) | Chongqing University，2026-09-10 | 未发现官方代码 | `tasco` |
| 低秩后训练 | [LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation](2609.11739-locus/README.md) | University of Washington，2026-09-10 | 未发现官方代码 | `locus` |
| 负向自蒸馏 | [Negative Self-Distillation: Learning to Reason by Avoiding Flaws](2609.11699-nsd/README.md) | University of Virginia，2026-09-10 | [已开源](https://github.com/Prongcan/NSD) | `nsd` |
| 跨模型族 OPD | [CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts](2609.10154-compass-opd/README.md) | Institute of Information Engineering, Chinese Academy of Sciences，2026-09-09 | 未发现官方代码 | `compass-opd` |
| 概率传输 OPD | [Distillation as Probability Transport: Routed On-Policy Distillation](2609.08337-route-opd/README.md) | Tencent，2026-09-08 | 未发现官方代码 | `route-opd` |
| 弱到强反向蒸馏 | [Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation](2609.08798-oprd/README.md) | KAIST AI，2026-09-08 | 未发现官方代码 | `oprd` |
| 代码测试时 RL | [Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation](2609.09135-probe-erpo/README.md) | Nanyang Technological University，2026-09-08 | 未发现官方代码 | `probe-erpo` |
| 极稀疏 On-policy distillation | [Extremely Sparse Supervision Incentivizes Reasoning Ability](2609.04565-sparse-opd/README.md) | Amazon / Duke University，2026-09-03 | 未发现官方代码 | `sparse-opd` |
| 弱模型前缀探索 | [Boosting LLM Exploration via Weak-Model Guidance in RLVR](2608.27420-weak-guide-rlvr/README.md) | Peking University，2026-08-27 | 未发现官方代码 | `weak-guide-rlvr` |
| 跨领域 RLVR 能力融合 | [Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms](2608.27409-rlvr-fusion/README.md) | Fudan University，2026-08-27 | [已开源](https://github.com/Di-viner/LLM-Fusion) | `rlvr-fusion` |
| DPO 偏好/优化尺度解耦 | [Disentangling Optimization Scale from Preference Scale in DPO](2608.27032-normalized-dpo/README.md) | Affiliation not listed in the paper，2026-08-27 | [已开源](https://github.com/ivankru/bayesian_dpo) | `normalized-dpo` |
| 多教师能力整合 | [Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD](2608.26735-uc-mopd/README.md) | Peking University，2026-08-27 | 未发现官方代码 | `uc-mopd` |
| 过程奖励 | [SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning](2608.26550-spear/README.md) | University of Pittsburgh，2026-08-27 | [已开源](https://github.com/zhuochunli/SPEAR) | `spear` |
| 测试时强化学习 | [TTPO: Test-Time Policy Optimization](2608.27448-ttpo/README.md) | Zhejiang University，2026-08-27 | [已开源](https://github.com/ZJU-REAL/TTPO) | `ttpo` |
| 证据帧特权自蒸馏 | [Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models](2608.27065-video-opsd/README.md) | Nanyang Technological University，2026-08-27 | 未发现官方代码 | `video-opsd` |
| 混合策略知识注入 RL | [From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection](2608.25243-grin/README.md) | University of California, Merced，2026-08-26 | 未发现官方代码 | `grin` |
| 奖励引导参数插值 | [GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning](2608.25583-grip/README.md) | Peking University，2026-08-26 | 未发现官方代码 | `grip` |
| 多模态 rubric RL | [V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning](2608.25580-v-rubrics/README.md) | S-Lab, Nanyang Technological University，2026-08-26 | [已开源](https://shulin16.github.io/v-rubrics/) | `v-rubrics` |
| 长视频特权视图 OPD | [Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding](2608.25356-clue-opsd/README.md) | University of Maryland, College Park，2026-08-26 | 未发现官方代码 | `clue-opsd` |
| 搜索增强 OPD + RL | [OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning](2608.24310-opd-search-plus/README.md) | University of Chinese Academy of Sciences，2026-08-25 | 未发现官方代码 | `opd-search-plus` |
| 可验证奖励 OPD | [OPDVR: On-Policy Distillation with Verifiable Rewards](2608.24696-opdvr/README.md) | LeapLab, Tsinghua University，2026-08-25 | [已开源](https://github.com/LeapLabTHU/OPDVR) | `opdvr` |
| 输入侧 Query-KL | [Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization](2608.23311-erpo/README.md) | AMAP, Alibaba Group，2026-08-24 | [已开源](https://github.com/alibaba/ERPO) | `erpo` |
| 反思式 token 信用 | [SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning](2608.23493-srpo/README.md) | Wuhan University，2026-08-24 | [已开源](https://github.com/Galleons2029/SRPO) | `srpo` |
| OPD | [Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress](2608.19408-r2-opd/README.md) | Authors did not disclose affiliation，2026-08-19 | 未发现官方代码 | `r2-opd` |
| 多奖励 RL | [Learn What's Left, Not What's Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization](2608.16072-sa-mrpo/README.md) | University of Florida，2026-08-17 | 未发现官方代码 | `sa-mrpo` |
| 多模态上下文偏好校准 | [Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization](2608.12158-c2-dpo/README.md) | Korea University，2026-08-12 | [已开源](https://github.com/mlvlab/C2-DPO) | `c2-dpo` |
| 几何约束 RL | [GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs](2608.11674-gcpo/README.md) | Shanghai AI Laboratory，2026-08-12 | [已开源](https://github.com/Icarus1411/GCPO) | `gcpo` |
| 前瞻偏好树 | [Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations](2608.12062-pto/README.md) | Reichman University，2026-08-12 | 未发现官方代码 | `pto` |
| Rubric RL | [Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL](2608.11669-rubric-dropout/README.md) | Scale AI，2026-08-12 | 未发现官方代码 | `rubric-dropout` |
| OPD | [SR-OPSD: Self-Referenced On-Policy Self-Distillation](2608.09745-sr-opsd/README.md) | Independent Researcher，2026-08-10 | 未发现官方代码 | `sr-opsd` |
| 自适应自蒸馏 | [DASH](2608.06243-dash/README.md) | Nanjing University，2026-08-06 | [已开源](https://github.com/DBtxy/DASH-OPSD) | `dash` |
| OPD | [On-Policy Delta Distillation for Multilingual Math Reasoning](2608.05802-opd2/README.md) | NAVER AI Lab，2026-08-06 | [已开源](https://github.com/naver-ai/opd2) | `opd2` |
| 推理枢纽蒸馏 | [RP-OPSD](2608.06347-rp-opsd/README.md) | Nanjing University，2026-08-06 | [已开源](https://github.com/NJUNLP/RP-OPSD) | `rp-opsd` |
| 生成式奖励模型 | [RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction](2608.06310-rrc/README.md) | Northeastern University，2026-08-06 | [已开源](https://github.com/wangclnlp/RRC) | `rrc` |
| 无监督自蒸馏 | [U-OPSD](2608.06296-u-opsd/README.md) | University of California, San Diego，2026-08-06 | 未发现官方代码 | `u-opsd` |
| rollout 预算分配 | [Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning](2608.05080-rail/README.md) | University of Notre Dame / Amazon，2026-08-05 | 未发现官方代码 | `rail` |
| RL rollout 加速 | [SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts](2608.04962-specroll/README.md) | VNU University of Engineering and Technology / Viettel AI，2026-08-05 | [已开源](https://anonymous.4open.science/r/SpecRoll-26062006) | `specroll` |
| 回报相关奖励塑形 | [ADRS](2608.03223-adrs/README.md) | University of Science and Technology of China，2026-08-04 | [已开源](https://github.com/gitrxh/ADRS-arxiv) | `adrs` |
| OPD | [CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning](2608.03673-causal-opd/README.md) | Authors did not disclose affiliation，2026-08-04 | 未发现官方代码 | `causal-opd` |
| OPD | [SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation](2608.03092-smopd/README.md) | Alibaba / Qwen，2026-08-04 | 未发现官方代码 | `smopd` |
| 外部 rollout | [Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models](2608.01717-erils/README.md) | Seoul National University，2026-08-03 | 未发现官方代码 | `erils` |
| 持续一致性蒸馏 | [PCSD](2608.01837-pcsd/README.md) | 论文未列机构，2026-08-03 | 未发现官方代码 | `pcsd` |
| OPD | [Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance](2608.00782-rstg/README.md) | Tianjin University，2026-08-01 | 未发现官方代码 | `rstg` |
| OPD | [Contrastive Reinforced Policy Optimization via Privileged Self-Distillation](2607.28026-crpo/README.md) | Authors did not disclose affiliation，2026-07-30 | 未发现官方代码 | `crpo` |
| Context distillation | [Flux-OPD](2607.28022-flux-opd/README.md) | Peking University，2026-07-30 | 未发现官方代码 | `flux-opd` |
| 多模态证据归因蒸馏 | [VAD](2607.28590-vad/README.md) | Shanghai Jiao Tong University，2026-07-30 | [已开源](https://github.com/DeepExperience/VAD_Multimodal_OPD) | `vad` |
| On-policy self-distillation | [β-OPSD](2607.28582-beta-opsd/README.md) | University of Maryland, College Park，2026-07-30 | 未发现官方代码 | `beta-opsd` |
| 分布保持 RL | [ReCo](2607.26862-reco/README.md) | Seoul National University，2026-07-29 | 未发现官方代码 | `reco-grpo` |
| Rubric RL | [SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning](2607.26873-serpo/README.md) | Authors did not disclose affiliation，2026-07-29 | 未发现官方代码 | `serpo` |
| Token-level credit assignment | [CoRT](2607.25659-cort/README.md) | ByteDance internship，2026-07-28 | 未发现官方代码 | `cort` |
| 在线强化学习 | [Reinforcement Learning for Code Optimization](2607.25970-code-optimization-rl/README.md) | FAIR at Meta / Inria，2026-07-28 | 未发现官方代码 | 计划键 `code-optimization-rl`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| On-policy distillation | [Relay-OPD](2607.26057-relay-opd/README.md) | Zhejiang University，2026-07-28 | [已开源](https://github.com/ZJU-REAL/Relay-OPD) | `relay-opd` |
| post-training | [Co-Evolving LLM Evaluators and Policies via DynamicRubric](../reproductions/2607.20083-dynamic-rubric/README.md) | WeChat / Tencent，2026-07-22 | 未发现官方代码 | `dynamic-rubric` |
| 过程奖励 | [TCR](2607.19824-tcr/README.md) | 论文未列机构，2026-07-22 | 未发现官方代码 | `tcr` |
| RLVR | [ISO: An RLVR-Native Optimization Stack](2607.19331-iso-rlvr/README.md) | The University of Texas at Austin，2026-07-21 | [已开源](https://github.com/zhuhanqing/ISO) | `iso-rlvr` |
| rlvr | [Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information](../reproductions/2607.19313-off-context-grpo/README.md) | Meta AI，2026-07-21 | [已开源](https://github.com/AgPriyank/OC-GRPO) | `off-context-grpo` |
| 教师奖励重权重 | [Distilled RL](2607.17247-distilled-rl/README.md) | Nankai University，2026-07-19 | [已开源](https://github.com/597358816/Distilled-RL) | `distilled-rl` |
| Reference anchor | [ARMOR](2607.10481-armor/README.md) | University of Science and Technology of China，2026-07-11 | 未发现官方代码 | `armor` |
| 几何信任域 | [RIPO](2607.10169-ripo/README.md) | Tsinghua University，2026-07-11 | 未发现官方代码 | `ripo` |
| Token 信用校准 | [TACO](2607.07976-taco/README.md) | Johns Hopkins University，2026-07-08 | [已开源](https://github.com/xiuyilou/TACO) | `taco` |
| post-training | [Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment](../reproductions/2607.04728-sis/README.md) | Renmin University of China，2026-07-06 | 未发现官方代码 | `sis` |
| 多教师能力整合 | [MOPD](2606.30406-mopd/README.md) | Xiaomi，2026-06-29 | 未发现官方代码 | `mopd` |
| 能力边界课程 | [CoBA-RL](2606.22317-coba-rl/README.md) | Zhejiang University，2026-06-21 | 未发现官方代码 | `coba-rl` |
| Entropy 稳定 | [STARE](2606.19236-stare/README.md) | Tsinghua University，2026-06-17 | [已开源](https://github.com/hp-luo/STARE) | `stare` |
| 异步训推失配 | [KPop](2606.15079-kpop/README.md) | Ling / Ring Team，2026-06-13 | 未发现官方代码 | `kpop` |
| AR-to-Diffusion 蒸馏 | [OPDLM](2606.06712-opd-lm/README.md) | Texas A&M University，2026-06-04 | 未发现官方代码 | `opd-lm` |
| 多目标 RL | [GPRL](2605.18721-gprl/README.md) | Stanford University，2026-05-18 | 未发现官方代码 | `gprl` |
| 对比序列 RL | [ConSPO](2605.12969-conspo/README.md) | Beijing Institute of Technology，2026-05-13 | 未发现官方代码 | `conspo` |
| 异步 off-policy | [Missing Old Logits](2605.12070-missing-old-logits/README.md) | Tianjin University，2026-05-12 | 未发现官方代码 | `missing-old-logits` |
| 直接偏好优化 | [Mind the Gap: Structure-Aware Consistency in Preference Learning](2604.27733-sa-dpo/README.md) | Google Research / Courant Institute of Mathematical Sciences，2026-04-30 | 未发现官方代码 | 计划键 `sa-dpo`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| On-policy distillation | [Lightning OPD](2604.13010-lightning-opd/README.md) | MIT HAN Lab，2026-04-14 | [已开源](https://github.com/jet-ai-projects/Lightning-OPD) | `lightning-opd` |
| Context distillation | [Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning](2602.21103-prompt-level-distillation/README.md) | Google，2026-02-24 | 未发现官方代码 | 计划键 `prompt-level-distillation`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| Context distillation | [OPCD](2602.12275-opcd/README.md) | Microsoft Research，2026-02-12 | [已开源](https://github.com/microsoft/LMOps/tree/main/opcd) | `opcd` |
| 长度无偏 RL | [LUSPO](2602.05261-luspo/README.md) | Meituan，2026-02-05 | 未发现官方代码 | `luspo` |
| On-policy self-distillation | [OPSD](2601.18734-opsd/README.md) | University of California, Los Angeles，2026-01-26 | [已开源](https://github.com/siyan-zhao/OPSD) | `opsd` |
| 校准强化学习 | [Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning](2601.13284-calibration-aware-rl/README.md) | University of Southern California，2026-01-19 | 未发现官方代码 | `calibration-aware-rl` |
| 纯在线训推校正 | [Online IcePop](web-2025-online-icepop/README.md) | Ant Group，2025-12-16 | 未发现官方代码 | `online-icepop` |
| 稳定 MoE RL | [Stabilizing RL with LLMs](2512.01374-minirl/README.md) | Alibaba Qwen Team，2025-12-01 | 未发现官方代码 | `minirl` |
| MoE 训推失配 | [IcePop](2510.18855-icepop/README.md) | Ant Group，2025-10-21 | 未发现官方代码 | `icepop` |
| SFT-RL 动态混合 | [CHORD](2508.11408-chord/README.md) | Alibaba Group，2025-08-15 | [已开源](https://github.com/modelscope/Trinity-RFT/tree/main/examples/mix_chord) | `chord` |
| 梯度保留 clip | [GPPO](2508.07629-gppo/README.md) | Alibaba Group，2025-08-11 | 未发现官方代码 | `gppo` |
| 训推失配校正 | [TIS](web-2025-tis/README.md) | University of California, San Diego，2025-08-05 | 未发现官方代码 | `tis` |
| 稳定序列 RL | [GSPO](2507.18071-gspo/README.md) | Alibaba Qwen Team，2025-07-24 | [已开源](https://alibaba.github.io/ROLL/docs/User%20Guides/Algorithms/GSPO/) | `gspo` |
| 校准奖励 | [Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty](2507.16806-rlcr/README.md) | Massachusetts Institute of Technology，2025-07-22 | [已开源](https://github.com/damanimehul/RLCR) | `rlcr` |
| 自博弈课程 | [SPIRAL](2506.24119-spiral/README.md) | Apple，2025-06-30 | [已开源](https://github.com/spiral-rl/spiral) | `spiral` |
| 长上下文 RL | [CISPO / MiniMax-M1](2506.13585-cispo/README.md) | MiniMax，2025-06-16 | [已开源](https://github.com/MiniMax-AI/MiniMax-M1) | `cispo` |
| 自置信奖励 | [INTUITOR](2505.19590-intuitor/README.md) | University of California, Berkeley，2025-05-26 | [已开源](https://github.com/sunblaze-ucb/Intuitor) | `intuitor` |
| 零数据自博弈 | [Absolute Zero](2505.03335-absolute-zero/README.md) | Tsinghua University，2025-05-06 | [已开源](https://github.com/LeapLabTHU/Absolute-Zero-Reasoner) | `absolute-zero` |
| 测试时强化学习 | [TTRL](2504.16084-ttrl/README.md) | PRIME-RL author team，2025-04-22 | [已开源](https://github.com/PRIME-RL/TTRL) | `ttrl` |
| 离策略推理 RL | [LUFFY](2504.14945-luffy/README.md) | University of Washington，2025-04-21 | [已开源](https://github.com/Simplified-Reasoning/LUFFY) | `luffy` |
| Critic PPO | [VAPO](2504.05118-vapo/README.md) | ByteDance Seed，2025-04-07 | 未发现官方代码 | `vapo` |
| GRPO 聚合偏置 | [Dr. GRPO](2503.20783-dr-grpo/README.md) | SAIL 研究团队，2025-03-26 | [已开源](https://github.com/sail-sg/understand-r1-zero) | `dr-grpo` |
| 长推理 RL | [DAPO](2503.14476-dapo/README.md) | ByteDance Seed，2025-03-18 | [已开源](https://github.com/BytedTsinghua-SIA/DAPO) | `dapo` |
| 全局优势估计 | [REINFORCE++](2501.03262-reinforce-plus/README.md) | Independent researchers，2025-01-04 | 未发现官方代码 | `reinforce-plus` |
| Reference-free 偏好 | [SimPO](2405.14734-simpo/README.md) | Princeton University，2024-05-23 | [已开源](https://github.com/princeton-nlp/SimPO) | `simpo` |
| 单阶段偏好 | [ORPO](2403.07691-orpo/README.md) | KAIST，2024-03-12 | [已开源](https://github.com/xfactlab/orpo) | `orpo` |
| 经典 RLHF | [RLOO](2402.14740-rloo/README.md) | Cohere For AI，2024-02-22 | 未发现官方代码 | `rloo` |
| 在线推理 RL | [DeepSeekMath / GRPO](2402.03300-grpo/README.md) | DeepSeek-AI，2024-02-05 | [已开源](https://github.com/deepseek-ai/DeepSeek-Math) | `grpo` |
| 二元反馈对齐 | [KTO](2402.01306-kto/README.md) | Contextual AI，2024-02-02 | [已开源](https://github.com/ContextualAI/HALOs) | `kto` |
| 自奖励 | [Self-Rewarding LM](2401.10020-self-rewarding/README.md) | Meta AI，2024-01-18 | 未发现官方代码 | `self-rewarding` |
| 自博弈微调 | [SPIN](2401.01335-spin/README.md) | University of California, Los Angeles，2024-01-02 | [已开源](https://github.com/uclaml/SPIN) | `spin` |
| 自动过程奖励 | [Math-Shepherd](2312.08935-math-shepherd/README.md) | Peking University，2023-12-14 | 未发现官方代码 | `math-shepherd` |
| 偏好正则 | [IPO](2310.12036-ipo/README.md) | Google DeepMind，2023-10-18 | 未发现官方代码 | `ipo` |
| 经典 RLHF | [ReMax](2310.10505-remax/README.md) | 香港中文大学（深圳）/ 深圳市大数据研究院，2023-10-16 | [已开源](https://github.com/liziniu/ReMax) | `remax` |
| 多属性可控 SFT | [SteerLM](2310.05344-steerlm/README.md) | NVIDIA，2023-10-09 | [已开源](https://github.com/NVIDIA/NeMo-Aligner) | `steerlm` |
| AI 反馈 | [RLAIF](2309.00267-rlaif/README.md) | Google Research，2023-09-01 | 未发现官方代码 | `rlaif` |
| 经典 On-policy distillation | [GKD](2306.13649-gkd/README.md) | Google DeepMind，2023-06-23 | [已开源](https://github.com/huggingface/trl/blob/main/docs/source/distillation_trainer.md) | `gkd` |
| Reverse-KL distillation | [MiniLLM](2306.08543-minillm/README.md) | Tsinghua University，2023-06-14 | [已开源](https://github.com/microsoft/LMOps/tree/main/minillm) | `minillm` |
| 过程监督 | [Let's Verify Step by Step](2305.20050-process-supervision/README.md) | OpenAI，2023-05-31 | [已开源](https://github.com/openai/prm800k) | `process-supervision` |
| 直接偏好优化 | [DPO](2305.18290-dpo/README.md) | Stanford University，2023-05-29 | [已开源](https://github.com/eric-mitchell/direct-preference-optimization) | `dpo` |
| 序列概率校准 | [SLiC-HF](2305.10425-slic-hf/README.md) | Google DeepMind，2023-05-17 | 未发现官方代码 | `slic-hf` |
| Reward 选优微调 | [RAFT](2304.06767-raft/README.md) | HKUST，2023-04-13 | [已开源](https://github.com/OptimalScale/LMFlow) | `raft` |
| 全排序偏好 | [RRHF](2304.05302-rrhf/README.md) | Alibaba DAMO Academy，2023-04-11 | [已开源](https://github.com/GanjinZero/RRHF) | `rrhf` |
| AI 反馈安全对齐 | [Constitutional AI](2212.08073-constitutional-ai/README.md) | Anthropic，2022-12-15 | [已开源](https://github.com/anthropics/ConstitutionalHarmlessnessPaper) | `constitutional-ai` |
| 经典 RLHF | [InstructGPT / PPO-RLHF](2203.02155-ppo-rlhf/README.md) | OpenAI，2022-03-04 | [已开源](https://github.com/openai/following-instructions-human-feedback) | `ppo-rlhf` |

</div>

分类浏览：

- [按机构/公司/学校](catalog/by-organization.md)
- [按主题](catalog/by-topic.md)
- [按年份](catalog/by-year.md)
