# LLM 后训练：按主题

采用“研究方向 → 方法簇 → 论文”的两级结构。一级用于快速定位研究范式，二级保留可比较的方法族；每篇论文独占一行，实验结果与复现边界请进入详情页查看。

## 蒸馏与训练闭环

### on-policy / context 蒸馏

- [DASH](../2608.06243-dash/README.md)（`dash`）：普通 OPSD 对每个 token 独立匹配 privileged teacher，难把后续可靠推理对前面决策的信用传回去。DASH 由局部 teacher/student divergence 产生停止梯度 gate，再从后向前递推聚合权重；不增加 teacher forward pass，却获得自适应 distillation horizon。
- [Flux-OPD](../2607.28022-flux-opd/README.md)（`flux-opd`）：固定上下文很快被学生吸收，直接更换上下文 teacher 又会让目标跳变。Flux-OPD 固定 context-free teacher 为锚，只注入多个演化上下文 teacher 相对锚点的 log-probability 差，并用几何均值归一化常数表示冲突、冲突越大修正越弱。
- [VAD](../2607.28590-vad/README.md)（`vad`）：多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。
- [β-OPSD](../2607.28582-beta-opsd/README.md)（`beta-opsd`）：论文指出 vanilla OPSD 是 β=1 的 KL 正则策略优化特例。先推导 reference policy 与 privileged teacher 之间的最优几何插值，再把昂贵高方差的 RL 解转成 token-logit 蒸馏目标，并以 return-to-go 做长推理信用分配。
- [Relay-OPD](../2607.26057-relay-opd/README.md)（`relay-opd`）：检测学生前缀失效后让教师短暂接管，再把轨迹交还学生；有限接力预算把监督集中到关键早期位置。
- [Lightning OPD](../2604.13010-lightning-opd/README.md)（`lightning-opd`）：传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。
- [OPCD](../2602.12275-opcd/README.md)（`opcd`）：提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。
- [OPSD](../2601.18734-opsd/README.md)（`opsd`）：普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。
- [GKD](../2306.13649-gkd/README.md)（`gkd`）：固定教师轨迹会让学生训练时看到的前缀与推理时自身生成的前缀不一致。GKD 让学生生成当前策略轨迹，再让教师在这些学生实际访问的状态给出完整分布；同时用 `student data fraction` 在固定数据和 on-policy 数据之间插值，并允许 forward KL、reverse KL 或广义 JSD。
- [MiniLLM](../2306.08543-minillm/README.md)（`minillm`）：标准 forward KL 倾向覆盖教师所有概率质量，小学生可能因此高估教师的低概率区域。MiniLLM 改用 mode-seeking 的 reverse KL，在学生自身生成分布上优化，并通过 teacher-mixed sampling、单步分解、长度归一化和 reward baseline 稳定策略梯度。

### 教师锚点与 SFT-RL 混合

- [ARMOR](../2607.10481-armor/README.md)（`armor`）：单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。
- [CHORD](../2508.11408-chord/README.md)（`chord`）：将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。

## 偏好建模与监督

### 成对、单样本与排序偏好

- [SimPO](../2405.14734-simpo/README.md)（`simpo`）：DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。
- [ORPO](../2403.07691-orpo/README.md)（`orpo`）：常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。
- [KTO](../2402.01306-kto/README.md)（`kto`）：DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。
- [IPO](../2310.12036-ipo/README.md)（`ipo`）：论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 $\Psi$PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。
- [DPO](../2305.18290-dpo/README.md)（`dpo`）：传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。
- [SLiC-HF](../2305.10425-slic-hf/README.md)（`slic-hf`）：PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。
- [RRHF](../2304.05302-rrhf/README.md)（`rrhf`）：PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。

### 安全对齐与可控监督

- [SteerLM](../2310.05344-steerlm/README.md)（`steerlm`）：传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。
- [Constitutional AI](../2212.08073-constitutional-ai/README.md)（`constitutional-ai`）：人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。

### 选优微调与自博弈

- [SPIN](../2401.01335-spin/README.md)（`spin`）：额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。
- [RAFT](../2304.06767-raft/README.md)（`raft`）：PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。

## 在线强化学习与稳定性

### PPO、REINFORCE 与 group RL

- [DAPO](../2503.14476-dapo/README.md)（`dapo`）：长 CoT 的在线 RL 容易被标准对称 clip 限制探索，且全对/全错的组没有学习信号。DAPO 用 Clip-Higher 放宽概率上升、Dynamic Sampling 丢弃零方差组、token-level loss 公平处理不同长度，并对过长回答分段惩罚。
- [RLOO](../2402.14740-rloo/README.md)（`rloo`）：PPO 为一般长时域 RL 设计，价值网络、GAE 和多轮 clipping 给 LLM RLHF 带来较大显存与调参开销。RLOO 把一整段 response 视作一个 action；同一 prompt 采样多个 response，用其余样本的平均 reward 作为当前样本 baseline。
- [DeepSeekMath / GRPO](../2402.03300-grpo/README.md)（`grpo`）：PPO 的 value model 与 policy 同规模，数学推理 RL 训练显存昂贵。GRPO 对同一问题采样一组 response，以组内 reward 均值和标准差构造 advantage，删除 critic；策略部分仍使用 old policy ratio、clipping 与 reference KL。
- [ReMax](../2310.10505-remax/README.md)（`remax`）：ReMax 利用 LLM RLHF 的三项特征：模拟快、token 转移确定、reward 通常只在轨迹末端给出。它删除 PPO 的 value model，以当前策略 greedy decoding 的 reward 作 prompt-dependent baseline，降低 REINFORCE 方差。
- [InstructGPT / PPO-RLHF](../2203.02155-ppo-rlhf/README.md)（`ppo-rlhf`）：只扩大语言模型不能保证更符合用户意图。InstructGPT 建立了经典三阶段流程：先用标注员示范做 SFT，再用成对排序训练 reward model，最后用 PPO 优化策略，同时以 KL 惩罚限制策略偏离 SFT/reference model。

### 信任域、clip 与梯度稳定

- [RIPO](../2607.10169-ripo/README.md)（`ripo`）：固定 PPO ratio 区间在低概率区域过于保守、在高概率区域又可能过大。RIPO 以 Fisher–Rao 几何定义策略距离，并按旧策略概率设置等距 clip 半径，使不同概率区域获得更均衡的局部 KL 预算。
- [GPPO](../2508.07629-gppo/README.md)（`gppo`）：普通 PPO 在正优势高 ratio、负优势低 ratio 的越界象限直接令梯度为零，可能同时压制探索和从负样本学习。GPPO 保持 PPO 的前向 clipped objective，但通过 stop-gradient 边界权重恢复这些越界位置的反向信号。
- [VAPO](../2504.05118-vapo/README.md)（`vapo`）：长 CoT 的 value-based PPO 易受 critic bias、异质 response 长度和稀疏奖励影响。VAPO 预训练 value model，并依 response 长度调节 actor 的 GAE/更新策略，以更稳定地进行 value-based 推理 RL。

### 序列目标、长度与聚合偏置

- [ReCo](../2607.26862-reco/README.md)（`reco-grpo`）：GRPO 容易重复采到高概率回答，并继续放大已经占优的 token，导致大 $k$ 下推理路径覆盖率下降。ReCo 同时修正 response 和 token：按 rollout 组中的期望出现次数抑制高频回答，再用 Bernoulli 方差比把更新集中到尚未饱和的决策点。
- [LUSPO](../2602.05261-luspo/README.md)（`luspo`）：论文从目标函数分解解释不同 RLVR 算法为何产生不同的响应长度轨迹，并指出 GSPO 的 sequence ratio 仍含长度偏置。LUSPO 对 sequence log-probability 作长度无偏归一化，避免训练中的长度坍塌。
- [GSPO](../2507.18071-gspo/README.md)（`gspo`）：GRPO/PPO 常逐 token 裁剪 ratio，但 reward 在完整序列级给出；长序列中单个异常 token 会造成大量裁剪，MoE routing 变化还会放大不稳定。GSPO 对每条 response 取平均 log-ratio，再指数化为单一 sequence ratio，整条序列共享 clip 权重。
- [Dr. GRPO](../2503.20783-dr-grpo/README.md)（`dr-grpo`）：原始 GRPO 的 response 内长度平均和组内标准差会引入长度与题目难度偏置。Dr. GRPO 移除这两个归一化项，保留中心化的组相对奖励，让每条轨迹以原始尺度参与更新。

### 优势估计与多目标优化

- [GPRL](../2605.18721-gprl/README.md)（`gprl`）：单一标量 reward 容易掩盖 helpfulness、格式、推理和简洁度之间的冲突。GPRL 先在每个偏好维度内部计算 group-relative advantage，再根据上下文聚合；漂移控制器检测某个维度是否主导训练并调整权重。
- [REINFORCE++](../2501.03262-reinforce-plus/README.md)（`reinforce-plus`）：GRPO/RLOO 的 prompt-local 标准差会让不同难度组被随机方差重新加权。REINFORCE++ 保留组内中心化，但使用跨 batch 的全局优势尺度归一化，从而在不引入 critic 的前提下降低方差与局部偏置。

## 训推一致性与高效 rollout

### 重要性采样与引擎失配

- [KPop](../2606.15079-kpop/README.md)（`kpop`）：异步 rollout 中的 serving 概率与训练侧概率失配，固定 ratio mask 会误删正常探索或保留错误梯度。KPop 将当前 token 与“其余词表”压缩为二元分布，只有正反两个方向的 binary KL 都低于阈值时才保留该 token 的更新。
- [Online IcePop](../web-2025-online-icepop/README.md)（`online-icepop`）：普通 IcePop 同时面对训练/rollout 引擎差异和一次 rollout 被多次更新造成的策略陈旧。Online IcePop 强制每个 rollout batch 只更新一次，使 stale-policy ratio 恒为 1，从目标中移除 PPO ratio 与 clip；训练侧仍用 IcePop 双侧 mask 和区间内原始 ratio 校正引擎失配。
- [IcePop](../2510.18855-icepop/README.md)（`icepop`）：MoE router 会放大训练引擎与 rollout 引擎的微小数值差异，单侧 TIS 仍可能保留严重偏小的失配 ratio。IcePop 对训练侧与 rollout 引擎的 token 概率比设置固定双侧区间；区间内保留原始校正权重，区间外 token 的本次策略梯度直接归零。
- [TIS](../web-2025-tis/README.md)（`tis`）：混合训练框架由 rollout 引擎采样、训练引擎重算 log-prob；即使权重相同，数值精度和 kernel 差异也会让行为分布与训练分布偏离。TIS 将训练侧与 rollout 引擎概率比乘入策略梯度，并只对过大的校正权重做单侧上截断，保留小权重样本而控制重尾方差。

## 奖励、信用与课程

### 过程 / token 信用分配

- [CoRT](../2607.25659-cort/README.md)（`cort`）：对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。
- [TCR](../2607.19824-tcr/README.md)（`tcr`）：只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。
- [TACO](../2607.07976-taco/README.md)（`taco`）：整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。

### 课程与能力边界

- [CoBA-RL](../2606.22317-coba-rl/README.md)（`coba-rl`）：普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。
