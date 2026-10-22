# LLM 后训练：按主题

采用“研究方向 → 方法簇 → 论文”的两级结构。一级用于快速定位研究范式，二级保留可比较的方法族；每篇论文独占一行，实验结果与复现边界请进入详情页查看。

## 奖励、信用与课程

### 课程与能力边界

- [Learning to Reason with Selective Internal Feedback](../2610.21392-sif/README.md)（`sif`）：平均 self-certainty 可以随错误置信一起增长。SIF 不把它当正确性标签，而是比较同一 prompt 内响应的排序 certainty profile：先按窗口比较投票，再按击败 peer 的比例给二元 reward，过滤不具资格的响应和同 reward 组。
- [A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO](../../reproductions/2610.13669-grpo-difficulty-curriculum/README.md)（`grpo-difficulty-curriculum`）：difficulty随当前policy变化，样本可能反复进出难度带。论文比较静态easy-to-hard、在线fixed-medium和B1→B5课程，进一步升到B5会退化。
- [BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation](../../reproductions/2610.13285-boundary-evo/README.md)（`boundary-evo`）：长推理监督的价值随学生能力变化。BoundaryEvo 先不按 correctness 过滤地蒸馏少量教师行为做 capability priming，然后每轮用当前学生、固定 expert 和 analyzer 重估边界，保留仍未掌握的 replay 并补充新问题；选好问题后再生成并验证 fresh teacher trajectories。
- [MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis](../../reproductions/2610.12659-magicbeanstalk/README.md)（`magicbeanstalk`）：RLVR有效性取决于problem、当前policy、rollout预算。MBS从verified hard seed提炼reasoning蓝图，自顶向下分解并实测child worked examples是否提高parent正确率，再合成更难新leaf、自底向上按原依赖组合。 **成本过高，暂不复现；待验收，未注册可执行入口。**
- [CoBA-RL](../2606.22317-coba-rl/README.md)（`coba-rl`）：普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。
- [SPIRAL](../2506.24119-spiral/README.md)（`spiral`）：同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。
- [INTUITOR](../2505.19590-intuitor/README.md)（`intuitor`）：把答案分布相对均匀分布的 KL 作为 intrinsic self-certainty reward，在没有答案和 verifier 时优化。
- [Absolute Zero](../2505.03335-absolute-zero/README.md)（`absolute-zero`）：proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。

### 过程 / token 信用分配

- [Progress Reward Model for Reinforcement Learning via Large Language Models](../2610.22056-progress-reward/README.md)（`progress-reward`）：稀疏成功信号难以指导长程机器人控制。PRM4RL 让 LLM 给出子任务、当前子任务判定函数 $\Psi$ 与进度势函数 $\Phi$；将子任务语义作为状态先验，将相邻状态进度差作为低层 RL 的密集 reward。
- [Inject a Turn, Not a Token: Learning Where to Redirect LLM Reasoning for Self-Correction](../../reproductions/2610.13672-upturn/README.md)（`upturn`）：冻结reasoner和小causal encoder，只学习paragraph boundary处的MLP cut policy。真实失败rollout在不同cut被冻结reasoner重新生成，给rescue奖励。
- [SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning](../2608.26550-spear/README.md)（`spear`）：结果奖励过稀，神经 PRM 又昂贵。SPEAR 把教师推理投影为领域符号 milestone，用 LCS-F1 给学生轨迹提供顺序敏感的稠密奖励。
- [SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning](../2608.23493-srpo/README.md)（`srpo`）：长轨迹只给终局 reward 时，很难知道具体哪个 token/动作导致失败。SRPO 让当前模型先根据完整轨迹和环境结果写出简短 reflection patch，再把 patch 拼回原问题；同一个模型在这个特权上下文中充当教师，对学生的 on-policy rollout 给出逐 token 分数。
- [ADRS](../2608.03223-adrs/README.md)（`adrs`）：privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。
- [CoRT](../2607.25659-cort/README.md)（`cort`）：对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。
- [TCR](../2607.19824-tcr/README.md)（`tcr`）：只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。
- [TACO](../2607.07976-taco/README.md)（`taco`）：整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。
- [Math-Shepherd](../2312.08935-math-shepherd/README.md)（`math-shepherd`）：从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。
- [Let's Verify Step by Step](../2305.20050-process-supervision/README.md)（`process-supervision`）：逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。

### 奖励构造与排序信号

- [When Pairwise Preferences Cycle: A Reliability-Anchored Preference Walk for Video GRPO](../2610.20089-rap-walk/README.md)（`rap-walk`）：RAP-Walk 不把成对视频偏好压成相互独立的胜率，而保留对手身份、循环关系和边清晰度。它在从输者到赢家的可靠随机游走中计算平稳偏好信用，经最低熵校准后修正原始胜率优势，最后仍交给同一 GRPO 更新。
- [RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction](../2608.06310-rrc/README.md)（`rrc`）：**主题：生成式奖励模型。** 生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。

### 多模态与结构化 reward

- [V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning](../2608.25580-v-rubrics/README.md)（`v-rubrics`）：把参考回答拆成视觉忠实度（VF）、推理一致性（RC）和指令遵循（IF）原子 rubric，并把可定位证据的信用分配到前缀，避免终局标量奖励掩盖局部幻觉。

## 蒸馏与训练闭环

### on-policy / context 蒸馏

- [Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation](../2610.28194-ap-opd/README.md)（`ap-opd`）：同样高的 OPD 惩罚可能是持续稳定的，也可能刚刚突增。AP-OPD 用相邻 token 块定位后一种情况，再把突增后整块监督按一个比率回拉；不增加教师 forward，不改变 token 系数的正负。
- [Ask to Distill: Learning to Synthesize Data for On-Policy Distillation](../2610.27450-ask-to-distill/README.md)（`ask-to-distill`）：问题决定学生会走到哪些前缀，因而决定教师能提供什么监督。A2D 冻结评分用的师生，训练独立的问题合成器；奖励同时要求“有差异”和“教师偏好的候选仍落在学生可达支持集”，然后筛选问题库，再从原始学生初始化执行 OPD。
- [On-Policy Transition Distillation](../2610.28048-optd/README.md)（`optd`）：最终层分布接近教师，不一定代表模型沿深度修正预测的方式接近教师。OPTD 保留最终层 OPD，再对选定浅到深 readout 的 log 概率增量施加监督。
- [Projected Distillation: On Learning to Solve Hard Problems from Close, Correct Targets](../2610.27467-projected-distillation/README.md)（`projected-distillation`）：困难问题的学生 rollout 可能全错，RL 得不到成功奖励；直接拟合外部完整答案又过于 off-policy。论文用 projector 最小改写学生的错误响应，经 verifier 接受后，只在变化片段做 DPO；学生自己答对的响应单独做 SFT，每轮重新采样和纠错。
- [Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization](../2610.25973-apsd/README.md)（`apsd`）：反馈条件自教师可能破坏正确rollout里学生已经成功的偏好，却又对错误rollout纠正不足。APSD依据正确性调整蒸馏target：正确时在学生和自教师之间插值，错误时越过自教师外推。
- [Reinforcement Learning with Visually Attributable On-Policy Self-Distillation](../2610.26856-vag/README.md)（`visually-attributable-opd`）：特权图像裁剪带来的 teacher 修正，可能混有语言先验或风格变化。VAG 让同一 EMA 教师对证据保留裁剪和随机遮挡裁剪重放相同学生前缀，只接纳与视觉对比方向一致的修正，再以有界项调制 verifier 的组归一化 advantage。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**
- [Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation](../2610.25034-spod/README.md)（`spod`）：多轮Agent蒸馏中，学生可能先超过教师，再随着持续模仿而退步。作者区分两个过程：教师修复学生的弱决策，同时也会侵蚀学生已经成功、但与教师偏好不同的行为。
- [GR-OPD: Group-Relative Sequence Credit for On-Policy Distillation](../2610.23042-gr-opd/README.md)（`gr-opd`）：教师在每个 token 上更自信，不一定意味着整段推理更值得复制；教师与学生的推理模式不同还可能造成训练崩溃。GR-OPD 在学生轨迹上重放教师，把 log-prob 差聚合为序列分数，在同题回答之间分配相对信用；保留一部分组均值压力，以免纯中心化抹掉教师总体偏好，然后使用 clipped PPO 更新。
- [SimOPD: Relational Knowledge Transfer for On-Policy Distillation](../2610.23306-simopd/README.md)（`simopd`）：概率蒸馏只利用输出分布，直接匹配隐状态又要求学生迁就教师的坐标和维数。SimOPD 改为比较回答之间的关系：两模型分别编码同一批学生回答，在自己的空间里计算“当前回答与历史回答有多像”，再匹配这两个相似度分布。
- [Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation](../2610.21234-token-teacher-selection/README.md)（`token-teacher-selection`）：一个教师未必适合学生整段推理：数学推导和代码生成可能需要不同专家，强教师与学生的分布差距也可能太大。论文把 OPD 的教师选择细化到每个学生实际访问的前缀。
- [Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models](../2610.21195-cce-opd/README.md)（`cce-opd`）：教师可能跟随学生错误 reasoning prefix，而忽略题目条件。CCE 在**完全相同的学生 response prefix**上，让同一冻结教师分别读取完整题目与遮蔽一个有效前提的题目，以 clipped log-prob contrast 调整辅助 target。
- [Does On-Policy Distillation Need to Complete Every Rollout?](../2610.21337-stopd/README.md)（`stopd`）：每条响应在生成**之前**独立采样 anchor，向上取整到 block 末尾，学生只生成到该 cutoff 或自然 EOS。保留的每个 token 都接收教师监督，并按其精确 inclusion probability 加权；自然 EOS 也是普通有效 token。
- [Learning from Unverified Peers via Shared Residual Distillation](../2610.22080-shared-residual-distillation/README.md)（`shared-residual-distillation`）：没有标准答案或可验证 reward 时，整段错误解答也可能包含有用步骤。SRD 不投票选“正确答案”，而比较同题 peers 相对跨题 control 对 token 分布的改变，只接收多位 peer 共同支持的保守残差。
- [OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents](../2610.21496-oprd-reminder/README.md)（`oprd-reminder`）：编码 Agent 的最终通过/失败不能指出哪一轮忽略了已有约束。OPRD 在学生自己生成的无提醒轨迹上训练：成功轨迹自模仿；失败轨迹由教师读取训练专用提醒，重新评分**同一学生前缀**，不是教师另生成一条答案。
- [Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation](../2610.21601-waypoint-opd/README.md)（`waypoint-opd`）：仅 initial/final 的 log-probability 位移不能区分“前后两段同向”与“中途反转”。同一 RL run 的 waypoint 只提供一致性证据，不是新的模仿目标。
- [Divergence-Routed On-Policy Distillation for Language Models](../2610.19572-divergence-routed-opd/README.md)（`divergence-routed-opd`）：DrOPD 在学生自己生成的轨迹上比较师生分布，以 JS 散度识别教师支持而学生严重欠覆盖的位置。它在所有位置保留 reverse-KL，并仅向高分歧位置增加 forward-KL 的纠正信号，通过候选级优势执行 PPO clipped 更新。
- [Information-Gain Calibrated On-Policy Distillation for Deep Search Agents](../2610.20664-ig-opd/README.md)（`ig-opd`）：普通 OPD 在检索前按教师偏好评分 query，却不知道检索结果是否有用；又按 token 数量分配预算，容易让很长的最终回答压过短而关键的搜索调用。IG-OPD 用检索后的答案置信变化校正两点：ITC 重新分配回合预算，IQC 用有符号增益修正动作关键 token 的方向。
- [LoOPSD: On-Policy Self-Distillation with Looped Teachers](../../reproductions/2610.18162-loopsd/README.md)（`loopsd`）：在线自蒸馏需要比学生更有用的教师，但更大外部模型或额外答案上下文并非唯一来源。LoOPSD在不改权重时搜索重复层区间来构造教师，用学生自产前缀进行蒸馏，再从更新后的学生重新搜索下一轮教师。 **成本过高，暂不复现；待验收，未注册可执行入口。**
- [Branching On-Policy Distillation](../../reproductions/2610.13481-branch-opd/README.md)（`branch-opd`）：普通 OPD 每个前缀只看到一次后续。BranchOPD 用学生不确定性和师生分歧定位 fork，从同一冻结学生策略独立采样 suffix，前缀只计入一次；并用协议事件监督结束行为。
- [State-OPD: State-Grounded On-Policy Distillation for Multi-Turn Agents](../../reproductions/2610.13238-state-opd/README.md)（`state-opd`）：多轮OPD把旧reasoning和实际环境记录混在教师上下文中，可能继承错误推理。State-OPD只给教师已执行action/observation状态，学生仍保留完整history；在高完整词表熵状态扩采整段reasoning+action，额外action不执行。
- [DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation](../2610.11659-dial-opd/README.md)（`dial-opd`）：用概率的对数均值调节教师—学生对数差异，降低两者都不认可的低概率 token 的监督优先级。按每条响应选取高分位置，未选位置仍保留为上下文。
- [MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation](../2610.11989-meta-opd/README.md)（`meta-opd`）：轻量权重网络根据师生预测学习 token 监督权重。它通过一次可微虚拟学生更新后的参考解损失获得元梯度，再使用新权重执行真实学生更新。
- [ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery](../2610.11332-recal/README.md)（`recal`）：先剪枝再蒸馏并不保证可恢复：损坏的学生轨迹会限制 OPD 教师信号。ReCal 先用剪枝 probe 测量教师轨迹上损伤，再用损伤重加权原始未剪枝模型的校准统计，重新选择通道；目标宽度和恢复流程保持一致。
- [When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better](../2610.11291-semi-opd/README.md)（`semi-opd`）：初始学生先一次性生成响应，教师评分缓存后固定复用。每次优化仍重新计算当前学生概率和 token 优势，不能把旧优势也一起缓存。
- [Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution](../2610.12367-sguid/README.md)（`sguid`）：语义相关不代表技能真正能够教会模型。SGUID 先从当前模型的已验证训练轨迹生成候选技能，再观察技能在蒸馏早期、晚期是否持续提供与验证器一致的信号。
- [Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals](../2610.11247-opd-learning-signals/README.md)（`opd-learning-signals`）：OPD 的残余差异可能仍大，但梯度提供的学习信号已变弱。论文同时记录损失、截断前梯度、两折 occupancy 估计、参数位移和逐层表征 CKA；这些是相关性诊断，不是因果证明。
- [Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models](../2609.38025-dr-opd/README.md)（`dr-opd`）：普通 OPD 对每个 teacher token 信号等权，但改正关键推理错误与替换同义措辞的下游价值不同。Dr. OPD 用双层优化定义“更新学生后预期 reward 最大”的 token 权重，并在每轮先闭式更新权重，再执行一次加权 OPD。
- [FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators](../2609.37851-flowmap-opd/README.md)（`flowmap-opd`）：把生成状态的 rollout 分布与 teacher/student 比较 kernel 解耦：rollout 只负责提供具有正确边缘分布的状态，优化 kernel 在这些冻结状态上比较 flow map、诱导速度或瞬时速度。
- [From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation](../2609.37510-maestro/README.md)（`maestro-opd`）：MAESTRO 用教师 top-k 覆盖度和 Bhattacharyya 相似度构造逐 token Policy Disagreement Score，并对靠近响应起点的位置加权；教师只在高分歧位置介入，减少整段 teacher rollout 的固定开销。
- [Interpolated Policy Distillation: A Controllable Continuum Between Off-Policy and On-Policy Distillation](../2609.37170-ipd/README.md)（`ipd`）：在每个 token 状态把 student 与 teacher 分布按 $m_\gamma=(1-\gamma)\pi_S+\gamma\pi_T$ 插值，从纯 on-policy 连续过渡到 off-policy teacher；论文再用验证感知的 speculative sampler 精确采样该目标策略。
- [Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning](../2609.37915-oasis/README.md)（`oasis-opsd`）：OASIS 把“在哪里监督”和“teacher 看什么 context”解耦：从同一题的 on-policy rollouts 中选最短的已验证轨迹作为 scaffold；teacher context 优先使用另一条未验证尝试；没有 verified rollout 的题不产生训练信号。这样只需要最终答案 verifier，而不需要 gold solution。
- [The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation](../2609.36484-ride/README.md)（`ride-opd`）：RIDE 不在输出概率空间放大 teacher/student ratio，而是在每层每个 token 计算 RL teacher 相对其 pre-RL checkpoint 的 hidden residual：$r=h_T-h_B$；学生回归到 $h_B+\alpha r$，其中 $\alpha>1$ 把方向延伸到 teacher 之外。teacher/base 均 stop-gradient，避免目标分支被学生更新。
- [The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning](../2610.00332-weakest-link/README.md)（`weakest-link`）：把教师对学生采样 token 的负对数概率当作成本，约束每个生成前缀的平均成本。一旦某个前缀越界，后续进入吸收惩罚状态，防止“先生成坏推理、再靠容易 token 拉低平均成本”；同时把即时奖励的全词表期望精确求导，降低只采样当前动作的方差。
- [An RL View of OPD: Least Square Policy Distillation for Sample-Efficient LLM Reasoning](../2609.35505-lspd/README.md)（`lspd`）：LSPD 把教师与学生的 token log-prob 差视作可优化残差，以 least-square 形式直接收缩分布差距，并用 Huber 式尾部限制异常差值的梯度；同时允许复用历史 query-response 轨迹，提高样本效率。
- [Recursive Self-Improvement via On-Policy Distillation for Reasoning](../../reproductions/2609.30652-recursive-opsd/README.md)（`recursive-opsd`）：传统 OPSD 让学生只看题目、冻结的特权教师额外看标准解，在学生自己的输出前缀上做逐 token 蒸馏。教师停留在初始权重时，后续学生学到的回看和纠错行为无法反哺教师。
- [RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning](../2609.20784-retire-opd/README.md)（`retire-opd`）：给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。
- [Trajectory Learnability for Offline On-Policy Distillation](../2609.18321-trajectory-learnability/README.md)（`trajectory-learnability`）：用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。
- [Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation](../2609.16937-gamma-opd/README.md)（`gamma-opd`）：以折扣时间信用逼近序列级 reverse-KL，再用有界奖励优势补入可验证结果。
- [Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation](../2609.14636-stride-opd/README.md)（`stride-opd`）：teacher 累积置信度越界时早停，并从最弱正确 turn 的缓存前缀重新开始。
- [Data-free On-policy Distillation](../2609.14193-df-opd/README.md)（`df-opd`）：由教师在自身策略空间生成问题，减少对外部后训练语料的依赖。本地实现保留决定性状态转换，并输出统一预算下可审计的中间量。
- [A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients](../2609.11768-adaptive-opd-gate/README.md)（`adaptive-opd-gate`）：把熵、不确定性、reference 偏移和教师—学生差距组合成逐 token gate，在 FKL/RKL 蒸馏方向间自适应分配。
- [Distillation as Probability Transport: Routed On-Policy Distillation](../2609.08337-route-opd/README.md)（`route-opd`）：普通 OPD 对整个教师分布做密集匹配。RouteOPD 先识别学生高估的 source token 和低估的 destination token，再只搬运需要修正的概率质量，使监督更聚焦且可解释。
- [Extremely Sparse Supervision Incentivizes Reasoning Ability](../2609.04565-sparse-opd/README.md)（`sparse-opd`）：常规 on-policy distillation 对生成轨迹的每个 token 使用教师分布。论文发现只挑一到两个关键位置、约占全部 token 的 0.05%，也能达到或超过全 token 训练。
- [Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding](../2608.25356-clue-opsd/README.md)（`clue-opsd`）：学生仍看完整长视频，冻结教师在训练时只看问题相关 clue interval；学生自己的 rollout 上做 on-policy self-distillation，推理时不需要 clue、标签或外部教师。
- [OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning](../2608.24310-opd-search-plus/README.md)（`opd-search-plus`）：搜索 Agent 的多轮 SFT 数据昂贵，任务专用教师又需先训练。OPDSearch+ 直接冻结通用 instruct teacher，在学生自己的在线搜索轨迹上用 forward-KL 蒸馏 query、推理和答案 token；随后 RL 从更好的行为分布继续优化，突破教师与纯 RL 的局部最优。
- [OPDVR: On-Policy Distillation with Verifiable Rewards](../2608.24696-opdvr/README.md)（`opdvr`）：Sampled-token OPD 的隐式奖励由教师/学生概率比决定，可能给正确轨迹负奖励、给错误轨迹正奖励。OPDVR 不再额外混合一个 RL loss，而是直接用 verifier correctness 对该隐式奖励做单侧 ReLU：正确轨迹只保留非负教师信号，错误轨迹只保留非正信号。
- [DASH](../2608.06243-dash/README.md)（`dash`）：普通 OPSD 对每个 token 独立匹配 privileged teacher，难把后续可靠推理对前面决策的信用传回去。DASH 由局部 teacher/student divergence 产生停止梯度 gate，再从后向前递推聚合权重；不增加 teacher forward pass，却获得自适应 distillation horizon。
- [RP-OPSD](../2608.06347-rp-opsd/README.md)（`rp-opsd`）：跨语言迁移中，表面措辞与真正改变推理状态的 pivot 不应同权。RP-OPSD 比较带英文参考解与去掉参考解的匹配教师视图，用分布位移定位 pivot，再在这些位置强化 privileged distillation 并保留 reference anchor。
- [U-OPSD](../2608.06296-u-opsd/README.md)（`u-opsd`）：U-OPSD 不使用答案、环境奖励或更大教师。模型多次采样后做多数投票，以最短一致解作为 privileged view，定点修复最长且高置信错误轨迹，是真正依赖内部一致性的自蒸馏。
- [PCSD](../2608.01837-pcsd/README.md)（`pcsd`）：单 token teacher gap 容易受噪声影响，整步共享权重又会抹掉位置差异。PCSD 在自适应窗口内指数累积 teacher-favoring signal，并对下降趋势衰减，最后用连续 sigmoid gate 与 GRPO 联合训练。
- [Flux-OPD](../2607.28022-flux-opd/README.md)（`flux-opd`）：固定上下文很快被学生吸收，直接更换上下文 teacher 又会让目标跳变。Flux-OPD 固定 context-free teacher 为锚，只注入多个演化上下文 teacher 相对锚点的 log-probability 差，并用几何均值归一化常数表示冲突、冲突越大修正越弱。
- [VAD](../2607.28590-vad/README.md)（`vad`）：多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。
- [β-OPSD](../2607.28582-beta-opsd/README.md)（`beta-opsd`）：论文指出 vanilla OPSD 是 β=1 的 KL 正则策略优化特例。先推导 reference policy 与 privileged teacher 之间的最优几何插值，再把昂贵高方差的 RL 解转成 token-logit 蒸馏目标，并以 return-to-go 做长推理信用分配。
- [Relay-OPD](../2607.26057-relay-opd/README.md)（`relay-opd`）：检测学生前缀失效后让教师短暂接管，再把轨迹交还学生；有限接力预算把监督集中到关键早期位置。
- [OPDLM](../2606.06712-opd-lm/README.md)（`opd-lm`）：ARLM 改成双向注意力后既会遗忘原知识，也有随机 mask 训练与 confidence decoding 推理之间的偏移。OPDLM 让双向学生在自身推理轨迹上生成，冻结 AR 教师在同一轨迹给 target logits。
- [Lightning OPD](../2604.13010-lightning-opd/README.md)（`lightning-opd`）：传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。
- [Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning](../2602.21103-prompt-level-distillation/README.md)（`prompt-level-distillation`）：PLD 不微调学生参数，而把教师推理抽象为可审查的系统指令：先用带标签训练样本提取微规则，经语义向量 DBSCAN 去掉噪声、合成规则，再根据训练错误修订冲突。学生最终使用整理后的规则，不读取每个测试样本的答案。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**
- [OPCD](../2602.12275-opcd/README.md)（`opcd`）：提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。
- [OPSD](../2601.18734-opsd/README.md)（`opsd`）：普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。
- [GKD](../2306.13649-gkd/README.md)（`gkd`）：固定教师轨迹会让学生训练时看到的前缀与推理时自身生成的前缀不一致。GKD 让学生生成当前策略轨迹，再让教师在这些学生实际访问的状态给出完整分布；同时用 `student data fraction` 在固定数据和 on-policy 数据之间插值，并允许 forward KL、reverse KL 或广义 JSD。
- [MiniLLM](../2306.08543-minillm/README.md)（`minillm`）：标准 forward KL 倾向覆盖教师所有概率质量，小学生可能因此高估教师的低概率区域。MiniLLM 改用 mode-seeking 的 reverse KL，在学生自身生成分布上优化，并通过 teacher-mixed sampling、单步分解、长度归一化和 reward baseline 稳定策略梯度。

### Advisor 与 targeted self-distillation

- [AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation](../2609.38142-advisd/README.md)（`advisd`）：冻结 executor，只训练 advisor；反思先提出修正，再对同一已记录 executor 响应分别计算有建议与无建议的平均 log-likelihood，只有影响幅度超过 donor-advice 校准阈值的决定才进入自蒸馏。

### 教师锚点与 SFT-RL 混合

- [CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer](../2610.28895-csd/README.md)（`csd`）：师生词表大小、token ID 与分词边界不一致，不能直接逐坐标 KL。CSD 先按原文字符区间对齐 chunk，再通过 **解码文本等价** 构造共同事件。
- [EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search](../2610.22290-elite-replay/README.md)（`elite-replay`）：单纯提高正确率的 RL 可能压缩正确解法的覆盖范围。EliteReplay 先用冻结基模和 MAP-Elites 收集不同正确策略，训练时持续回放固定档案。
- [Training-Free On-Policy Distillation](../2610.22236-tf-opd/README.md)（`tf-opd`）：共同初始化的专家模型，其线性层融合可以写成匹配各教师输出的最小二乘。关键不是任意协方差，而是每个教师在**自己生成的、经过终止和循环筛选的答案**上实际遇到的输入二阶矩；统计按 token 数归一，不能让长答案自然压倒其他领域。
- [Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation](../../reproductions/2610.13521-road-mopd/README.md)（`road-mopd`）：多域只路由各自教师，不能防止共享参数更新损害其他能力。Road 用未路由教师在当前目标域的同一学生轨迹上给出兼容性证据，调节 token credit，再求真实辅助梯度，投影目标梯度但保留其范数下限。
- [CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation](../../reproductions/2610.13257-cast-opd/README.md)（`cast-opd`）：异构 tokenizer 的同一文本有不同分段，直接比较 token ID 无意义。CAST 先匹配实际解码文本，将教师 span 的总 log probability 均匀投影到学生 span，再按不确定性×局部平滑度分配 credit；未对齐位置通过初始学生 KL 限制漂移。
- [Continually Post-training Small Models via Synthetic Self-distillation](../../reproductions/2610.13113-synthself/README.md)（`synthself`）：小模型self-rewrite可能失真，直接SFT又可能偏离base分布。SynthSelf用更大的同家族aligner把train demonstration贪心离线改写，通过答案拒绝采样后SFT。
- [Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training](../../reproductions/2610.12933-progressive-contraction/README.md)（`progressive-contraction`）：正确teacher CoT也可能经过多种正确/错误后续的reasoning fork。论文对真实prefix做Monte Carlo continuation，按branch不确定性先收缩teacher pool，再经真实student probing epoch按当前NLL选top-M并重路由。
- [CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts](../2609.10154-compass-opd/README.md)（`compass-opd`）：异构教师与学生的绝对概率刻度不可直接比较。CompassOPD 用教师相对其 reference 的后训练变化作“指南针”，并在模型族内中心化，保留方向而消除不同模型族的整体偏置。
- [Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation](../2609.08798-oprd/README.md)（`oprd`）：OPRD 不直接模仿弱教师答案，而是先测量弱教师经过后训练后的 logit 变化方向，再沿这个方向增强强模型的可验证奖励梯度；核心假设是“学习方向”比弱模型最终能力更容易迁移。
- [Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD](../2608.26735-uc-mopd/README.md)（`uc-mopd`）：普通 MOPD 很少采到强正优势 token，也无法判断更新方向是否可靠。方法扩大温度覆盖，按轨迹正优势密度挑样本，再用熵校准 CLL 概率门控 token 更新。
- [From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection](../2608.25243-grin/README.md)（`grin`）：纯 on-policy RL 在新知识尚未掌握时几乎采不到正确答案。GRIN 在失败组注入 golden response，再以 mixed-policy importance correction 训练；能力提高后自动回到 on-policy 探索。
- [Distilled RL](../2607.17247-distilled-rl/README.md)（`distilled-rl`）：传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。
- [ARMOR](../2607.10481-armor/README.md)（`armor`）：单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。
- [MOPD](../2606.30406-mopd/README.md)（`mopd`）：多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。
- [CHORD](../2508.11408-chord/README.md)（`chord`）：将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。

## 其他

### 多模态上下文偏好校准

- [Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization](../2608.12158-c2-dpo/README.md)（`c2-dpo`）：普通 DPO 即使输入相关图像上下文，也可能主要依赖语言先验。论文先定义 CPG，度量加入上下文后 chosen/rejected preference margin 增加多少；C²-DPO 直接扩大该增益，同时保留原偏好顺序。

### 校准强化学习

- [Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning](../2601.13284-calibration-aware-rl/README.md)（`calibration-aware-rl`）：论文指出 RLVR 虽能提高决策正确率，却可能让 decision token 极度过度自信；其方法直接调整决策 token 的概率，在保留准确率的同时降低 ECE。本仓库对应地把 accuracy 与 Brier/ECE 同时纳入报告，并只用 validation 拟合温度，禁止用 test 调参。

### RLVR

- [MGE-PO: Entropy-Aware Credit Assignment for Mathematical Reasoning](../2610.23245-mge-po/README.md)（`mge-po`）：GRPO会给同题、同正确性的回答相同 advantage，忽略生成的不确定性。MGE-PO 用生成时缓存的 token 熵区分回答，在成功／失败与高熵／低熵四象限上调整信用；再用在线题目熵统计安排课程，并以熵加权参考KL约束优化。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**
- [Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay](../2610.24236-tar-adaptive-replay/README.md)（`tar-adaptive-replay`）：有限on-policy采样可能逐步压低同样正确但较少出现的推理模式；仅在当前rollout上重加权，难以恢复已经采不到的模式。TAR先从基础策略大量生成，过滤正确回答，再保留分散的原型轨迹。
- [GRPODropout: Less is More for Online Reinforcement Learning Rollouts](../2610.11854-grpo-dropout/README.md)（`grpo-dropout`）：从同一 prompt 的 GRPO 响应组中筛除部分高概率、正优势响应，并用旧策略概率重新中心化保留响应的优势。不是随机 dropout，也不改变生成预算。
- [Residual Advantage: Student-Relative Teacher Guidance for RL with Verifiable Rewards](../2610.11519-residual-advantage/README.md)（`residual-advantage`）：把全词表师生概率残差变成相对学生的有界局部优势，再逐响应中心化，与验证器优势相加。Co-RA 在同一已评分学生批次上更新教师 LoRA，下一轮才使用新教师。
- [CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning](../2610.02039-carm/README.md)（`carm`）：对每个 token 的 current/rollout log-ratio 先取绝对值再平均，避免正负漂移在序列级几何均值中抵消。
- [Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR](../2609.37868-graft/README.md)（`graft`）：当 receiver 的 rollout group 全错、peer 在同题同时有成功和失败轨迹时，GRAFT 用完整 peer group 替换无信号组并保留 peer 内部 advantage。跨 tokenizer 的策略错配通过序列平均 log-likelihood compatibility 加权，再用 token importance ratio clipping 限制更新。
- [SIPO: Unifying Reinforcement Learning with On-Policy Self-Distillation](../2609.36742-sipo/README.md)（`sipo`）：RLVR 的轨迹 reward 稀疏，普通 OPSD 又会受自教师过度自信和长序列惩罚影响。SIPO 对同一 rollout 构造正/负两份特权上下文：两者 teacher log-prob 的差值抵消共享偏差，形成逐 token 信用；环境 reward 决定主方向，dense evidence 负责在 token 间重新分配。
- [ISO: An RLVR-Native Optimization Stack](../2607.19331-iso-rlvr/README.md)（`iso-rlvr`）：固定预训练权重奇异值，仅优化输入/输出 singular frames；同时提供无数据 specialist merger。

### OPD

- [DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies](../2610.00317-drift-opd/README.md)（`drift-opd`）：把序列级 reverse-KL 拆成当前 chunk 的一步 reverse-KL 与刻画长期动作后果的 future potential；critic 从离线 demonstrations 学习。
- [LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation](../2610.00333-lego-opd/README.md)（`lego-opd`）：把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。
- [Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress](../2608.19408-r2-opd/README.md)（`r2-opd`）：分别按教师奖励和独立进展奖励排序 reasoning spans，冲突时屏蔽蒸馏信号。
- [SR-OPSD: Self-Referenced On-Policy Self-Distillation](../2608.09745-sr-opsd/README.md)（`sr-opsd`）：把自教师与 reference 做几何插值得到有效目标，再用 Rényi divergence 控制投影几何和密度比敏感度。
- [On-Policy Delta Distillation for Multilingual Math Reasoning](../2608.05802-opd2/README.md)（`opd2`）：以 post-trained teacher 相对其 base model 的概率增量作为蒸馏信号，减少复制教师原有偏差。
- [CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning](../2608.03673-causal-opd/README.md)（`causal-opd`）：教师定位 on-policy 因果链第一个错误步骤，以短 horizon RL 修复，并按证据→机制→结论推进课程。
- [SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation](../2608.03092-smopd/README.md)（`smopd`）：先用 reward-priority 分别训练专长教师，再在学生自身轨迹上合并多个教师能力。
- [Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance](../2608.00782-rstg/README.md)（`rstg`）：只对负向零方差 group 启用教师，并在高熵或大 teacher-student gap token 上蒸馏，同时注入教师正确轨迹 SFT。
- [Contrastive Reinforced Policy Optimization via Privileged Self-Distillation](../2607.28026-crpo/README.md)（`crpo`）：按预测熵区分反思探索正位置和 exposure-bias 负位置，对 privileged self-distillation 做组内对比。

### 在线强化学习

- [MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning](../2609.31644-mad-rl/README.md)（`mad-rl`）：逐条最大化正确性奖励可能令输出类别坍缩；MaD-RL为输出的类别频率拟合指定分布，而非仅提高token熵。它将组内频率与目标类别分布构造的L2、forward-KL、reverse-KL或JSD奖励，与任务正确性结合后用于GRPO。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**
- [Reinforcement Learning for Code Optimization](../2607.25970-code-optimization-rl/README.md)（`code-optimization-rl`）：代码正确不等于运行快；直接加入耗时奖励会被小测试、共享worker负载和稀疏优势淹没。作者构造DMC-Optim，用独立服务校准时长，再组合正确性、优化测试和人类参考百分位。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**

### 偏好优化

- [GAW-PO: Preference Optimization with Gradient-Aligned Token Weights](../2610.01511-gaw-po/README.md)（`gaw-po`）：用拒绝 token 梯度与 preferred update direction 的对齐度调节负权重；越支持优选行为的 token 越少受罚。
- [A Zeroth-Order Paradigm for LLM Preference Alignment](../2609.19144-compo/README.md)（`compo`）：不求偏好目标梯度，只比较正负参数扰动的结果得到一比特方向，再以逐坐标阈值抑制噪声。
- [Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data](../2609.16532-sd-dpo/README.md)（`sd-dpo`）：识别事实正确但风格不同的 rejected response，反转其偏好方向并按组比例加权以抵消风格梯度。

### RLHF / RLVR

- [Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL](../2610.21439-mrtpo/README.md)（`mrtpo`）：GDPO 虽然分别归一化多种奖励，但仍把每种奖励均摊到整条响应。SQL 可执行性、格式、执行结果可能只分别依赖少数 token。
- [Multi-Reward Hacking: From Aggregation-Induced Drift to Trust-Anchored Defense](../2610.21404-tag-reward-gating/README.md)（`tag-reward-gating`）：正确性和简短、低时延等奖励相加时，容易获取的辅助奖励可能主导 GRPO：总奖励上涨，主要任务却变差。TAG 不是简单降低辅助权重，而是先从同一基线分别优化每个奖励，观察哪个探针对基线的分布漂移最小，再将该奖励选为 anchor。
- [Training Reasoning Models to Generate Diverse Scientific Ideas](../2610.22324-diverge-ideation/README.md)（`diverge-ideation`）：独立采样多个高分想法可能反复得到同一个方向。论文让模型在一次生成中写出整组想法，每个新想法都能看到前面写过的内容，再按整组质量和相互差异训练。
- [Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight](../2610.21018-rshd/README.md)（`rshd`）：一组 GRPO rollout 全部失败时，组内 advantage 全为0。RSHD 不把参考答案告诉模型，而让同一策略根据失败响应写纠错 note，再用 note 生成**新的** replay。

### post-training

- [Co-Evolving LLM Evaluators and Policies via DynamicRubric](../../reproductions/2607.20083-dynamic-rubric/README.md)（`dynamic-rubric`）：固定 judge 或固定 rubric 会在策略模型进步后失去区分力。DynamicRubric 根据当前 prompt 和一组候选回答动态生成评估维度与权重，用 discriminability 目标寻找能区分当代 hard negatives 的标准，用 anchor 目标限制评估器漂移，再让 evaluator 和 policy 多轮协同进化。
- [Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment](../../reproductions/2607.04728-sis/README.md)（`sis`）：异步 rollout、样本复用和 stale policy 会让 LLM 强化学习变成 off-policy 更新。标准 importance sampling（IS）在长序列上连乘后方差很大，直接 clipping 又会丢失有效梯度。

### 外部 rollout

- [Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models](../2608.01717-erils/README.md)（`erils`）：约束外部策略 rollout 长度，并对 on-policy/external 来源分别处理奖励以防联合归一化崩溃。

### 异步 RL

- [Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis](../2610.01896-gmc-grpo/README.md)（`gmc-grpo`）：异步 rollout 的重要性比在 group 级统一缩放，使总质量受帽约束；在共同二阶矩保证下减少 trajectory-wise clipping 的持续偏差。

### RL 训练加速

- [GrowMTP: Can RL Grow Its Own Draft Head?](../2609.16648-growmtp/README.md)（`growmtp`）：在 RL rollout 内按被接受的草稿深度训练 MTP head，并与主干梯度解耦。

### 后训练数据选择

- [LESSER: Post-Training Data Selection with Output-Layer Gradients](../2610.03702-lesser/README.md)（`lesser`）：现有面向目标任务的数据选择常计算每个候选样本和少量目标任务 query 的全参数梯度，再按相似性选取训练子集；对大模型逐样本反传代价很高。LESSER 只替换**特征**：从一次前向得到的最后隐藏状态和词表概率解析地计算输出层梯度。

### 低秩后训练

- [LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation](../2609.11739-locus/README.md)（`locus`）：学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。

### 多 Agent

- [MAS-OPD: On-Policy Distillation for Multi-Agent Systems](../2609.34234-mas-opd/README.md)（`mas-opd`）：以目标角色与非目标角色 teacher 信号差构造 role advantage，并把协作冲突归因只提供给 teacher 形成 privileged coordination supervision。

### DPO 偏好/优化尺度解耦

- [Disentangling Optimization Scale from Preference Scale in DPO](../2608.27032-normalized-dpo/README.md)（`normalized-dpo`）：标准 DPO 的 $\beta$ 同时改变偏好噪声尺度与梯度幅度，导致有效学习率被隐式重缩放。论文用除以 $\beta$ 的 centered-softplus 保持相同 argmin，同时让梯度尺度在 $\beta\to0$ 时不消失。

### 负向自蒸馏

- [Negative Self-Distillation: Learning to Reason by Avoiding Flaws](../2609.11699-nsd/README.md)（`nsd`）：让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。

### rlvr

- [Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information](../../reproductions/2607.19313-off-context-grpo/README.md)（`off-context-grpo`）：困难题上 vanilla GRPO 常因整组 rollout 都失败而没有有效优势信号。Off-Context GRPO 只在采样时向 behavior policy 提供解题草稿或提示等 privileged information，提高成功轨迹出现率；优化目标仍是原始无提示 policy，并用 importance ratio 校正两种采样分布的偏差，因此推理时不需要特权上下文。

### 在线蒸馏

- [Learning from Teacher Continuations at Student States](../2609.36246-olive/README.md)（`olive`）：由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。

### 多模态后训练

- [Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes](../2610.02117-where-opd/README.md)（`where-opd`）：程序化合成场景自动给出对象身份和空间坐标；teacher 接收文本化空间特权信息，student 只看图像与问题，在自己的 on-policy token 上蒸馏 teacher。
- [OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation](../2609.16459-opd-aha/README.md)（`opd-aha`）：用真实视觉与空视觉教师分布之差重建视觉偏好目标，抑制错误语言前缀的惯性。

### 扩散语言模型后训练

- [On-Policy Residual Learning for Diffusion Language Models](../2610.20687-orl-diffusion/README.md)（`orl-diffusion`）：将上一步预测分布作为残差上下文不是简单后处理：训练时必须看到模型自己诱导的残差轨迹。ORL联合在线采集、状态传输、精确重放及熵收缩，减少训练与推理残差状态分布差异。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**

### 强化学习

- [PACT: From Credit Assignment to Critic Alignment](../2609.26355-pact/README.md)（`pact`）：终局奖励只有一个标量，但 actor 要更新每个生成 token。论文在完整性、前缀一致性和中性三个条件下，刻画 token 的理论信用为相邻前缀的条件期望之差。
- [TIAO: Token Importance-Aware Policy Optimization for Text Summarization](../2609.16748-tiao/README.md)（`tiao`）：通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。

### On-policy 蒸馏

- [PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation](../2610.11167-pivot/README.md)（`pivot`）：垂直领域的小模型既需要教师传授知识，也需要任务奖励改善最终判断；所有样本同时从蒸馏切换到 RL，可能使困难样本过早失去教师监督。PIVOT 在学生自己的响应上计算教师困惑度，先把低困惑度问题切换到 GRPO，高困惑度问题继续 OPD。

### 前瞻偏好树

- [Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations](../2608.12062-pto/README.md)（`pto`）：逐轮偏好只判断当前回答，难以优化目标导向对话的长期结果。PTO 让 agent 和虚拟用户展开候选对话树，oracle 评价当前回答及未来延续，以偏好对迭代执行 DPO；更深 look-ahead 带来更稳定的长期策略。

### GRPO

- [Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals](../2610.01548-range-grpo/README.md)（`range-grpo`）：用 conformal reward interval 代替单点 judge 分数；组内只对可确定排序的区间产生方向信号，区间重叠时不制造虚假偏好。

### RL

- [Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training](../2609.37119-rfpo/README.md)（`rfpo`）：冻结已校准 critic，把前缀成功概率同时作为 rollout reward、GAE baseline 和未完成轨迹预报，并在去长度偏置后二值化，降低策略利用 critic 偏差的风险。

### 校准奖励

- [Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty](../2507.16806-rlcr/README.md)（`rlcr`）：普通 binary reward 只奖励答对，容易鼓励模型无差别地自信。RLCR 让模型同时输出预测与置信度，并把 bounded proper scoring rule 加入奖励，使诚实概率具有最优激励。

### 跨领域 RLVR 能力融合

- [Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms](../2608.27409-rlvr-fusion/README.md)（`rlvr-fusion`）：论文统一比较三种复用产物不同的跨域能力融合：Merge 合并专家 task vector，Mix RL 合并训练数据，MOPD 同时复用专家和数据。平均差距不超过 1.4 points，但单项可达 8.6 points，因此选择取决于专家、数据和成本条件。

### 自我回顾

- [Shockingly Simple Self-retrospection Improves Agentic Models Without RL](../2609.35741-roft/README.md)（`roft`）：ROFT 不直接用环境奖励更新动作策略，而是让模型在完整轨迹与反馈之后生成一段自我回顾，再只监督回顾 token。回顾成为后续行为可复用的训练信号，同时避免把环境文本或历史动作误当监督标签。

### 离线 SFT

- [ROSS: Relearning from Self-Generated Rollouts through Selective Supervision](../2609.35954-ross/README.md)（`ross`）：保留历史 self-rollout 的完整上下文，但只对筛选出的模型 continuation 计算损失，避免模仿其中错误或冗余步骤。

### Rubric RL

- [Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL](../2608.11669-rubric-dropout/README.md)（`rubric-dropout`）：每个 rollout group 共享随机丢弃的 rubric 子集，使策略无法持续利用固定 judge proxy。
- [SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning](../2607.26873-serpo/README.md)（`serpo`）：让 Good–Normal–Bad 响应档案、query-specific rubrics 和 actor 策略形成三方闭环自进化。

### 多奖励 RL

- [Learn What's Left, Not What's Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization](../2608.16072-sa-mrpo/README.md)（`sa-mrpo`）：逐 reward 维度标准化优势，并依据 batch 饱和度动态把梯度预算转移到尚未掌握的目标。

### RL 后训练

- [Sharpening Tax in Post-Training](../2610.01509-sharpening-tax/README.md)（`sharpening-tax`）：比较 base 与后训练策略在固定采样预算下的任务覆盖；再用 posterior-tempered group sampling 按估计难度调温，兼顾 pass@1 与覆盖率。

### 测试时适配

- [Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning](../2609.11393-tasco/README.md)（`tasco`）：冻结主模型，优化轻量 prefix；除置信度外还惩罚邻域扰动下的不稳定，从而避免自信但错误的轨迹。

### 多轮 Agent 对齐

- [Turn-level Multiscale Density Ratio Estimation for LLM Agents](../2609.16760-tlm-dre/README.md)（`tlm-dre`）：按 turn 分配多尺度权重，并对正负 token 密度比采用非对称更新。

### 视频生成

- [Token-Level Video Reinforcement Learning](../2610.01973-tvrl/README.md)（`tvrl`）：冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。

### 证据帧特权自蒸馏

- [Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models](../2608.27065-video-opsd/README.md)（`video-opsd`）：学生读取完整视频，训练期自教师只读取人工标注的证据帧；再按 token 对证据的依赖度加权蒸馏。论文称效果接近 GRPO，而训练时间减少约 60%。

## 在线强化学习与稳定性

### 信任域、clip 与梯度稳定

- [Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence](../../reproductions/2610.13015-gppo-framework/README.md)（`gppo-framework`）：GPPO把近端优化拆成f-divergence几何和估计拓扑。MC、atomic、binary对采样动作概率/补集的处理不同，诱导实际不同信任域。
- [Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization](../2608.23311-erpo/README.md)（`erpo`）：传统 Policy-KL 直接压回答分布，稳定训练的同时消耗探索预算。ERPO 观察到 RL 过程中模型诱导的问题分布也会漂移，于是把正则放到输入侧：用冻结 reference 的问题似然给 query 静态加权，再以 Query-KL 控制环境分布漂移，不直接对 response score function 施压。
- [GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs](../2608.11674-gcpo/README.md)（`gcpo`）：GRPO 等 on-policy rollout RL 会偶发进入预训练权重的主奇异子空间，论文观察到这些 spike 常先于验证性能下降。GCPO 固定预训练矩阵两侧的 top-k 奇异空间，只允许低秩更新存在于输入、输出两侧的正交补中；这是硬可行域，不是依赖系数的软 penalty。
- [RIPO](../2607.10169-ripo/README.md)（`ripo`）：固定 PPO ratio 区间在低概率区域过于保守、在高概率区域又可能过大。RIPO 以 Fisher–Rao 几何定义策略距离，并按旧策略概率设置等距 clip 半径，使不同概率区域获得更均衡的局部 KL 预算。
- [STARE](../2606.19236-stare/README.md)（`stare`）：按 batch surprisal 分位数识别 entropy-critical token，重加权其 advantage，并以目标 entropy 闭环 gate 调节方向。
- [GPPO](../2508.07629-gppo/README.md)（`gppo`）：普通 PPO 在正优势高 ratio、负优势低 ratio 的越界象限直接令梯度为零，可能同时压制探索和从负样本学习。GPPO 保持 PPO 的前向 clipped objective，但通过 stop-gradient 边界权重恢复这些越界位置的反向信号。
- [CISPO / MiniMax-M1](../2506.13585-cispo/README.md)（`cispo`）：固定 rollout policy 采样，token 级计算 importance ratio，只裁剪比率以保留优势方向和有效梯度。
- [VAPO](../2504.05118-vapo/README.md)（`vapo`）：长 CoT 的 value-based PPO 易受 critic bias、异质 response 长度和稀疏奖励影响。VAPO 预训练 value model，并依 response 长度调节 actor 的 GAE/更新策略，以更稳定地进行 value-based 推理 RL。

### 序列目标、长度与聚合偏置

- [Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL](../../reproductions/2610.13020-tapo-trajectory/README.md)（`tapo-trajectory`）：autoregressive轨迹的前序policy变化累积state distribution gap。TAPO对token前缀likelihood ratio取几何均值、按长度收紧clipping，并stop-gradient避免前序token反传进当前动作。
- [RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration](../2610.01458-rlcpr/README.md)（`rlcpr`）：概率奖励在同组推理后验接近时难以区分冗长推理；RLCPR 只对“全组都长、答案后验又集中”的组施加相对长度惩罚。另用直接作答时的 token 平均熵把数据分层，让保留分布偏向低不确定样本。
- [ReCo](../2607.26862-reco/README.md)（`reco-grpo`）：GRPO 容易重复采到高概率回答，并继续放大已经占优的 token，导致大 $k$ 下推理路径覆盖率下降。ReCo 同时修正 response 和 token：按 rollout 组中的期望出现次数抑制高频回答，再用 Bernoulli 方差比把更新集中到尚未饱和的决策点。
- [ConSPO](../2605.12969-conspo/README.md)（`conspo`）：将同组序列的优劣关系写成长度归一化 InfoNCE，避免 token 求和造成长度和组内尺度偏差。
- [LUSPO](../2602.05261-luspo/README.md)（`luspo`）：论文从目标函数分解解释不同 RLVR 算法为何产生不同的响应长度轨迹，并指出 GSPO 的 sequence ratio 仍含长度偏置。LUSPO 对 sequence log-probability 作长度无偏归一化，避免训练中的长度坍塌。
- [GSPO](../2507.18071-gspo/README.md)（`gspo`）：GRPO/PPO 常逐 token 裁剪 ratio，但 reward 在完整序列级给出；长序列中单个异常 token 会造成大量裁剪，MoE routing 变化还会放大不稳定。GSPO 对每条 response 取平均 log-ratio，再指数化为单一 sequence ratio，整条序列共享 clip 权重。
- [Dr. GRPO](../2503.20783-dr-grpo/README.md)（`dr-grpo`）：原始 GRPO 的 response 内长度平均和组内标准差会引入长度与题目难度偏置。Dr. GRPO 移除这两个归一化项，保留中心化的组相对奖励，让每条轨迹以原始尺度参与更新。

### Agentic RL 与教师调度

- [CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents](../2610.29965-cord/README.md)（`cord`）：任务奖励和教师指导提供不同信号，直接相加会让相反的梯度互相抵消。CORD 不替换 GRPO 或 OPD 的目标，而是明确选择一个 **protected objective**，最小修改另一个梯度。
- [MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation](../2610.23234-multiagent-opd/README.md)（`multiagent-opd`）：层级团队的最终答案能监督Leader，却难以判断Searcher的检索、总结是否真正有效。MultiAgent-OPD先在较简单的Searcher–Answerer流程训练教师，再从**相同的基础checkpoint重新开始**训练共享参数的Leader–Searcher–Answerer团队。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**
- [Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning](../2610.23181-treeopsd/README.md)（`treeopsd`）：长轨迹仅有终局奖励时，同一轨迹的好坏动作容易一起获奖或受罚；同一批轨迹又会经历多次更新，旧信用不能告诉优化器何时停止。TreeOPSD 将续写分支整理成共享前缀树，把叶奖励按行为策略似然向上回传，再把每个 turn 的信用映射为一个冻结且有界的 Bernoulli 教师。
- [KnowGPO: Knowledge-Grouped Policy Optimization for Search Agents](../2610.22331-knowgpo/README.md)（`knowgpo`）：不同搜索轨迹即使读到了相同事实，也可能使用完全不同的 query、网页和表述，按表面观察匹配会把可比较的步骤拆散。KnowGPO 将问题所需事实拆为原子条件，训练 verifier 检查每步获得了哪些条件。
- [OpCredit: Operation-Aware Policy Learning for Agentic Knowledge Graph Question Answering](../2610.21345-opcredit/README.md)（`opcredit`）：整条轨迹失败不代表每一步都无用，成功轨迹也可能绕路。OpCredit 的 BOC 从普通 rollout 中复用分支结果：同题、同活动实体，再匹配访问集合、剩余预算和决策阶段；FTC 则衡量**该操作局部前沿**相对答案邻域的进退。
- [SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents](../../reproductions/2610.13157-soar/README.md)（`soar`）：只按答案奖训练的search agent可能答对却伪造证据依赖。SOAR独立记录atomic query的internal recall和external retrieval，再要求显式声明source。
- [Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT](../2610.03361-follow-the-winners/README.md)（`follow-the-winners`）：在有状态工具环境里，为同一提示重复生成一组等价 rollout 往往很贵；而 PPO 的 critic 又占用额外模型资源。FTW 不计算 value，也不要求 GRPO 式同题多轨迹。
- [Dependency-Aware Reward Shaping for Agentic Reinforcement Learning](../2610.01207-dars/README.md)（`dars`）：把任务进度表示为带先决条件的 predicate 图；验证、失效和修复事件更新图状态，最近破损依赖按图距离衰减已完成工作的 credit，独立分支不受牵连。
- [My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning](../2610.01161-my-fault/README.md)（`my-fault`）：自诊断器提出错误类别与位置，只有经证据验证的 claim 才进入在线 error pricing；学得的相对成本把终局 credit 守恒地重分配到步骤。
- [SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning](../2610.00838-sharpo/README.md)（`sharpo`）：用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。
- [Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL](../2609.37898-gats/README.md)（`gats`）：用教师训练尾部成功率作为固定参考，以学生滞后一拍的移动平均估计能力差距；OPD 权重随差距线性下降，学生达到教师参考后永久关闭教师分支，继续只做 GRPO。
- [PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning](../2609.36642-pr-opd/README.md)（`pr-opd`）：GRPO warm start 后，策略为每条已完成轨迹写一条 hindsight skill，并对同一 response 做普通 context 与 skill context 两次 forward。后者是 stop-gradient teacher；PR-OPD 在每层、每个 response token 对齐投影 hidden state，再与 reward objective 组合。

### PPO、REINFORCE 与 group RL

- [Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards](../2610.20814-ggpo/README.md)（`ggpo`）：behavior policy 负责产生样本，reference policy 负责 KL anchor，两者不是同一角色。组内 adjusted reward 全相同时，策略满足该 reference 的 Gibbs 目标。
- [When KL Regularization Misfires in Group Policy Optimization](../2610.12161-zcpo/README.md)（`zcpo`）：独立 KL 惩罚可能在奖励相同或奖励梯度取消时继续更新策略。ZCPO 用响应平均的条件 KL 相对漂移，校准组内奖励系数；再将该系数放进原策略 surrogate，不另加独立 KL loss。
- [LUFFY](../2504.14945-luffy/README.md)（`luffy`）：把离线高质量推理与在线 rollout 放进同一 support，通过正则化 importance ratio 保留 on-policy 行为。
- [DAPO](../2503.14476-dapo/README.md)（`dapo`）：长 CoT 的在线 RL 容易被标准对称 clip 限制探索，且全对/全错的组没有学习信号。DAPO 用 Clip-Higher 放宽概率上升、Dynamic Sampling 丢弃零方差组、token-level loss 公平处理不同长度，并对过长回答分段惩罚。
- [RLOO](../2402.14740-rloo/README.md)（`rloo`）：PPO 为一般长时域 RL 设计，价值网络、GAE 和多轮 clipping 给 LLM RLHF 带来较大显存与调参开销。RLOO 把一整段 response 视作一个 action；同一 prompt 采样多个 response，用其余样本的平均 reward 作为当前样本 baseline。
- [DeepSeekMath / GRPO](../2402.03300-grpo/README.md)（`grpo`）：PPO 的 value model 与 policy 同规模，数学推理 RL 训练显存昂贵。GRPO 对同一问题采样一组 response，以组内 reward 均值和标准差构造 advantage，删除 critic；策略部分仍使用 old policy ratio、clipping 与 reference KL。
- [ReMax](../2310.10505-remax/README.md)（`remax`）：ReMax 利用 LLM RLHF 的三项特征：模拟快、token 转移确定、reward 通常只在轨迹末端给出。它删除 PPO 的 value model，以当前策略 greedy decoding 的 reward 作 prompt-dependent baseline，降低 REINFORCE 方差。
- [InstructGPT / PPO-RLHF](../2203.02155-ppo-rlhf/README.md)（`ppo-rlhf`）：只扩大语言模型不能保证更符合用户意图。InstructGPT 建立了经典三阶段流程：先用标注员示范做 SFT，再用成对排序训练 reward model，最后用 PPO 优化策略，同时以 KL 惩罚限制策略偏离 SFT/reference model。

### 优势估计与多目标优化

- [Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation](../2609.09135-probe-erpo/README.md)（`probe-erpo`）：论文用不依赖最终答案的 probe consistency ratio（PCR）估计当前题目的可信度：高一致样本可强化，低一致样本对排名靠后的候选施加负向约束，同时用熵项控制探索。
- [Boosting LLM Exploration via Weak-Model Guidance in RLVR](../2608.27420-weak-guide-rlvr/README.md)（`weak-guide-rlvr`）：RLVR 容易熵坍缩。论文用更小弱模型生成部分推理前缀，迫使目标模型进入陌生轨迹，再以 entropy 截断和原生/前缀样本混训保持覆盖率。
- [TTPO: Test-Time Policy Optimization](../2608.27448-ttpo/README.md)（`ttpo`）：多数票伪标签可能错误，但与多数票分歧的 rollout 通常仍是错的。TTPO 因而对同意分支做 OPSD，对分歧分支做 grouped RL，并分别过滤已收敛 token 与高置信错误。
- [GPRL](../2605.18721-gprl/README.md)（`gprl`）：单一标量 reward 容易掩盖 helpfulness、格式、推理和简洁度之间的冲突。GPRL 先在每个偏好维度内部计算 group-relative advantage，再根据上下文聚合；漂移控制器检测某个维度是否主导训练并调整权重。
- [TTRL](../2504.16084-ttrl/README.md)（`ttrl`）：同一测试题多次采样，以多数一致答案作为伪标签并即时更新模型，不访问 gold label。
- [REINFORCE++](../2501.03262-reinforce-plus/README.md)（`reinforce-plus`）：GRPO/RLOO 的 prompt-local 标准差会让不同难度组被随机方差重新加权。REINFORCE++ 保留组内中心化，但使用跨 batch 的全局优势尺度归一化，从而在不引入 critic 的前提下降低方差与局部偏置。

### 步骤奖励与信用分配

- [T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning](../2610.00388-t2spo/README.md)（`t2spo`）：用历史成功轨迹中的剩余步数训练上下文内距离估计器，预测每个状态距离成功还多远；把相邻状态的距离改善转为步骤优势，与轨迹级奖励共同优化。冻结 TabPFN 避免额外训练 critic，失败轨迹不被误标成接近成功的正样本。

## 偏好建模与监督

### 成对、单样本与排序偏好

- [CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF](../2610.21138-clean-rm/README.md)（`clean-rm`）：不同偏好样本的标注噪声不一定相同。CleanRM 用少量干净反馈校准两个方向的样本级噪声率；以语义与恢复偏好的**联合分布**作最优传输，而不是只匹配偏好直方图。
- [Mind the Gap: Structure-Aware Consistency in Preference Learning](../2604.27733-sa-dpo/README.md)（`sa-dpo`）：对语义几乎相同的回答强求固定偏好间隔，会制造难以满足的约束。SA-DPO 将间隔改为回答距离的函数，保留相对参考策略的隐式奖励差；同时研究 margin、模型容量与 surrogate 尾部的一致性关系，而非单纯调整 DPO 的学习率。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**
- [SimPO](../2405.14734-simpo/README.md)（`simpo`）：DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。
- [ORPO](../2403.07691-orpo/README.md)（`orpo`）：常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。
- [KTO](../2402.01306-kto/README.md)（`kto`）：DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。
- [IPO](../2310.12036-ipo/README.md)（`ipo`）：论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 $\Psi$PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。
- [DPO](../2305.18290-dpo/README.md)（`dpo`）：传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。
- [SLiC-HF](../2305.10425-slic-hf/README.md)（`slic-hf`）：PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。
- [RRHF](../2304.05302-rrhf/README.md)（`rrhf`）：PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。

### 安全对齐与可控监督

- [SteerLM](../2310.05344-steerlm/README.md)（`steerlm`）：传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。
- [RLAIF](../2309.00267-rlaif/README.md)（`rlaif`）：AI labeler 对候选做顺序交换评判，去除位置偏差后训练 preference policy；本地落实双顺序标签与成对更新。
- [Constitutional AI](../2212.08073-constitutional-ai/README.md)（`constitutional-ai`）：人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。

### 模型融合与推理效率

- [GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning](../2608.25583-grip/README.md)（`grip`）：在 thinking 与 instruct 权重间，不使用单一全局系数，而由细粒度 reward 学习分层/参数插值，使模型保留推理准确率同时缩短输出。

### 选优微调与自博弈

- [Self-Rewarding LM](../2401.10020-self-rewarding/README.md)（`self-rewarding`）：每轮由当前模型生成候选并以 LLM-as-a-Judge 打分，形成新的偏好对继续 DPO，构成自举闭环。
- [SPIN](../2401.01335-spin/README.md)（`spin`）：额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。
- [RAFT](../2304.06767-raft/README.md)（`raft`）：PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。

## 训推一致性与高效 rollout

### 重要性采样与引擎失配

- [KPop](../2606.15079-kpop/README.md)（`kpop`）：异步 rollout 中的 serving 概率与训练侧概率失配，固定 ratio mask 会误删正常探索或保留错误梯度。KPop 将当前 token 与“其余词表”压缩为二元分布，只有正反两个方向的 binary KL 都低于阈值时才保留该 token 的更新。
- [Missing Old Logits](../2605.12070-missing-old-logits/README.md)（`missing-old-logits`）：指出异步 RL 丢失历史训练侧 logits 后，训推校正与策略陈旧校正发生语义混叠；给出快照、old-logit model、中断同步和 PPO-EWMA 修复。
- [Online IcePop](../web-2025-online-icepop/README.md)（`online-icepop`）：普通 IcePop 同时面对训练/rollout 引擎差异和一次 rollout 被多次更新造成的策略陈旧。Online IcePop 强制每个 rollout batch 只更新一次，使 stale-policy ratio 恒为 1，从目标中移除 PPO ratio 与 clip；训练侧仍用 IcePop 双侧 mask 和区间内原始 ratio 校正引擎失配。
- [Stabilizing RL with LLMs](../2512.01374-minirl/README.md)（`minirl`）：分解训推差异与 policy staleness，on-policy 使用 importance correction，off-policy 结合 clipping 与 MoE Routing Replay。
- [IcePop](../2510.18855-icepop/README.md)（`icepop`）：MoE router 会放大训练引擎与 rollout 引擎的微小数值差异，单侧 TIS 仍可能保留严重偏小的失配 ratio。IcePop 对训练侧与 rollout 引擎的 token 概率比设置固定双侧区间；区间内保留原始校正权重，区间外 token 的本次策略梯度直接归零。
- [TIS](../web-2025-tis/README.md)（`tis`）：混合训练框架由 rollout 引擎采样、训练引擎重算 log-prob；即使权重相同，数值精度和 kernel 差异也会让行为分布与训练分布偏离。TIS 将训练侧与 rollout 引擎概率比乘入策略梯度，并只对过大的校正权重做单侧上截断，保留小权重样本而控制重尾方差。

### 预算分配与 speculative rollout

- [Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning](../2608.05080-rail/README.md)（`rail`）：**主题：rollout 预算分配。** 均匀 rollout 浪费预算，静态启发式又跟不上策略变化。
- [SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts](../2608.04962-specroll/README.md)（`specroll`）：**主题：RL rollout 加速。** RL 中 target policy 持续变化，静态 drafter 很快过时。
