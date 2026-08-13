# LLM 后训练：按机构/公司/学校

按论文一作的第一署名单位聚合；单位内按首次公开日期倒序排列。每篇论文同时显示一作姓名，并附一至两句中文方法简介。联合工作不会重复归入所有合作单位。

## Alibaba DAMO Academy

- 2023-04-11 · 一作：Zheng Yuan · [RRHF](../2304.05302-rrhf/README.md)（`rrhf`）：PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。

## Alibaba Group

- 2025-08-15 · 一作：Wenhao Zhang · [CHORD](../2508.11408-chord/README.md)（`chord`）：将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。
- 2025-08-11 · 一作：Zhenpeng Su · [GPPO](../2508.07629-gppo/README.md)（`gppo`）：普通 PPO 在正优势高 ratio、负优势低 ratio 的越界象限直接令梯度为零，可能同时压制探索和从负样本学习。GPPO 保持 PPO 的前向 clipped objective，但通过 stop-gradient 边界权重恢复这些越界位置的反向信号。

## Alibaba Qwen Team

- 2025-12-01 · 一作：Chujie Zheng · [Stabilizing RL with LLMs](../2512.01374-minirl/README.md)（`minirl`）：分解训推差异与 policy staleness，on-policy 使用 importance correction，off-policy 结合 clipping 与 MoE Routing Replay。
- 2025-07-24 · 一作：Chujie Zheng · [GSPO](../2507.18071-gspo/README.md)（`gspo`）：GRPO/PPO 常逐 token 裁剪 ratio，但 reward 在完整序列级给出；长序列中单个异常 token 会造成大量裁剪，MoE routing 变化还会放大不稳定。GSPO 对每条 response 取平均 log-ratio，再指数化为单一 sequence ratio，整条序列共享 clip 权重。

## Ant Group

- 2025-12-16 · 一作：Jian Hu · [Online IcePop](../web-2025-online-icepop/README.md)（`online-icepop`）：普通 IcePop 同时面对训练/rollout 引擎差异和一次 rollout 被多次更新造成的策略陈旧。Online IcePop 强制每个 rollout batch 只更新一次，使 stale-policy ratio 恒为 1，从目标中移除 PPO ratio 与 clip；训练侧仍用 IcePop 双侧 mask 和区间内原始 ratio 校正引擎失配。
- 2025-10-21 · 一作：Ling Team · [IcePop](../2510.18855-icepop/README.md)（`icepop`）：MoE router 会放大训练引擎与 rollout 引擎的微小数值差异，单侧 TIS 仍可能保留严重偏小的失配 ratio。IcePop 对训练侧与 rollout 引擎的 token 概率比设置固定双侧区间；区间内保留原始校正权重，区间外 token 的本次策略梯度直接归零。

## Anthropic

- 2022-12-15 · 一作：Yuntao Bai · [Constitutional AI](../2212.08073-constitutional-ai/README.md)（`constitutional-ai`）：人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。

## Apple

- 2025-06-30 · 一作：Bo Liu · [SPIRAL](../2506.24119-spiral/README.md)（`spiral`）：同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。

## Beijing Institute of Technology

- 2026-05-13 · 一作：Feng Zhang · [ConSPO](../2605.12969-conspo/README.md)（`conspo`）：将同组序列的优劣关系写成长度归一化 InfoNCE，避免 token 求和造成长度和组内尺度偏差。

## ByteDance Seed

- 2025-04-07 · 一作：Yu Yue · [VAPO](../2504.05118-vapo/README.md)（`vapo`）：长 CoT 的 value-based PPO 易受 critic bias、异质 response 长度和稀疏奖励影响。VAPO 预训练 value model，并依 response 长度调节 actor 的 GAE/更新策略，以更稳定地进行 value-based 推理 RL。
- 2025-03-18 · 一作：Qiying Yu · [DAPO](../2503.14476-dapo/README.md)（`dapo`）：长 CoT 的在线 RL 容易被标准对称 clip 限制探索，且全对/全错的组没有学习信号。DAPO 用 Clip-Higher 放宽概率上升、Dynamic Sampling 丢弃零方差组、token-level loss 公平处理不同长度，并对过长回答分段惩罚。

## ByteDance internship

- 2026-07-28 · 一作：Bo-Wen Zhang · [CoRT](../2607.25659-cort/README.md)（`cort`）：对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。

## Cohere For AI

- 2024-02-22 · 一作：Arash Ahmadian · [RLOO](../2402.14740-rloo/README.md)（`rloo`）：PPO 为一般长时域 RL 设计，价值网络、GAE 和多轮 clipping 给 LLM RLHF 带来较大显存与调参开销。RLOO 把一整段 response 视作一个 action；同一 prompt 采样多个 response，用其余样本的平均 reward 作为当前样本 baseline。

## Contextual AI

- 2024-02-02 · 一作：Kawin Ethayarajh · [KTO](../2402.01306-kto/README.md)（`kto`）：DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。

## DeepSeek-AI

- 2024-02-05 · 一作：Zhihong Shao · [DeepSeekMath / GRPO](../2402.03300-grpo/README.md)（`grpo`）：PPO 的 value model 与 policy 同规模，数学推理 RL 训练显存昂贵。GRPO 对同一问题采样一组 response，以组内 reward 均值和标准差构造 advantage，删除 critic；策略部分仍使用 old policy ratio、clipping 与 reference KL。

## Google DeepMind

- 2023-10-18 · 一作：Mohammad Gheshlaghi Azar · [IPO](../2310.12036-ipo/README.md)（`ipo`）：论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 $\Psi$PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。
- 2023-06-23 · 一作：Rishabh Agarwal · [GKD](../2306.13649-gkd/README.md)（`gkd`）：固定教师轨迹会让学生训练时看到的前缀与推理时自身生成的前缀不一致。GKD 让学生生成当前策略轨迹，再让教师在这些学生实际访问的状态给出完整分布；同时用 `student data fraction` 在固定数据和 on-policy 数据之间插值，并允许 forward KL、reverse KL 或广义 JSD。
- 2023-05-17 · 一作：Yao Zhao · [SLiC-HF](../2305.10425-slic-hf/README.md)（`slic-hf`）：PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。

## Google Research

- 2023-09-01 · 一作：Harrison Lee · [RLAIF](../2309.00267-rlaif/README.md)（`rlaif`）：AI labeler 对候选做顺序交换评判，去除位置偏差后训练 preference policy；本地落实双顺序标签与成对更新。

## HKUST

- 2023-04-13 · 一作：Hanze Dong · [RAFT](../2304.06767-raft/README.md)（`raft`）：PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。

## Independent researchers

- 2025-01-04 · 一作：Jian Hu · [REINFORCE++](../2501.03262-reinforce-plus/README.md)（`reinforce-plus`）：GRPO/RLOO 的 prompt-local 标准差会让不同难度组被随机方差重新加权。REINFORCE++ 保留组内中心化，但使用跨 batch 的全局优势尺度归一化，从而在不引入 critic 的前提下降低方差与局部偏置。

## Johns Hopkins University

- 2026-07-08 · 一作：Xiuyi Lou · [TACO](../2607.07976-taco/README.md)（`taco`）：整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。

## KAIST

- 2024-03-12 · 一作：Jiwoo Hong · [ORPO](../2403.07691-orpo/README.md)（`orpo`）：常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。

## Korea University

- 2026-08-12 · 一作：Byungoh Ko · [Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization](../2608.12158-c2-dpo/README.md)（`c2-dpo`）：普通 DPO 即使输入相关图像上下文，也可能主要依赖语言先验。论文先定义 CPG，度量加入上下文后 chosen/rejected preference margin 增加多少；C²-DPO 直接扩大该增益，同时保留原偏好顺序。

## Ling / Ring Team

- 2026-06-13 · 一作：Ang Li · [KPop](../2606.15079-kpop/README.md)（`kpop`）：异步 rollout 中的 serving 概率与训练侧概率失配，固定 ratio mask 会误删正常探索或保留错误梯度。KPop 将当前 token 与“其余词表”压缩为二元分布，只有正反两个方向的 binary KL 都低于阈值时才保留该 token 的更新。

## MIT HAN Lab

- 2026-04-14 · 一作：Yecheng Wu · [Lightning OPD](../2604.13010-lightning-opd/README.md)（`lightning-opd`）：传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。

## Meituan

- 2026-02-05 · 一作：Fanfan Liu · [LUSPO](../2602.05261-luspo/README.md)（`luspo`）：论文从目标函数分解解释不同 RLVR 算法为何产生不同的响应长度轨迹，并指出 GSPO 的 sequence ratio 仍含长度偏置。LUSPO 对 sequence log-probability 作长度无偏归一化，避免训练中的长度坍塌。

## Meta AI

- 2026-07-21 · 一作：Priyank Agrawal · [Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information](../../reproductions/2607.19313-off-context-grpo/README.md)（`off-context-grpo`）：困难题上 vanilla GRPO 常因整组 rollout 都失败而没有有效优势信号。Off-Context GRPO 只在采样时向 behavior policy 提供解题草稿或提示等 privileged information，提高成功轨迹出现率；优化目标仍是原始无提示 policy，并用 importance ratio 校正两种采样分布的偏差，因此推理时不需要特权上下文。
- 2024-01-18 · 一作：Weizhe Yuan · [Self-Rewarding LM](../2401.10020-self-rewarding/README.md)（`self-rewarding`）：每轮由当前模型生成候选并以 LLM-as-a-Judge 打分，形成新的偏好对继续 DPO，构成自举闭环。

## Microsoft Research

- 2026-02-12 · 一作：Tianzhu Ye · [OPCD](../2602.12275-opcd/README.md)（`opcd`）：提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。

## MiniMax

- 2025-06-16 · 一作：MiniMax · [CISPO / MiniMax-M1](../2506.13585-cispo/README.md)（`cispo`）：固定 rollout policy 采样，token 级计算 importance ratio，只裁剪比率以保留优势方向和有效梯度。

## NVIDIA

- 2023-10-09 · 一作：Yi Dong · [SteerLM](../2310.05344-steerlm/README.md)（`steerlm`）：传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。

## Nanjing University

- 2026-08-06 · 一作：Zhiyan Hou · [DASH](../2608.06243-dash/README.md)（`dash`）：普通 OPSD 对每个 token 独立匹配 privileged teacher，难把后续可靠推理对前面决策的信用传回去。DASH 由局部 teacher/student divergence 产生停止梯度 gate，再从后向前递推聚合权重；不增加 teacher forward pass，却获得自适应 distillation horizon。
- 2026-08-06 · 一作：Xinye Wang · [RP-OPSD](../2608.06347-rp-opsd/README.md)（`rp-opsd`）：跨语言迁移中，表面措辞与真正改变推理状态的 pivot 不应同权。RP-OPSD 比较带英文参考解与去掉参考解的匹配教师视图，用分布位移定位 pivot，再在这些位置强化 privileged distillation 并保留 reference anchor。

## Nankai University

- 2026-07-19 · 一作：Chen Wang · [Distilled RL](../2607.17247-distilled-rl/README.md)（`distilled-rl`）：传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。

## Northeastern University

- 2026-08-06 · 一作：Chenglong Wang · [RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction](../2608.06310-rrc/README.md)（`rrc`）：**主题：生成式奖励模型。** 生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。

## OpenAI

- 2023-05-31 · 一作：Hunter Lightman · [Let's Verify Step by Step](../2305.20050-process-supervision/README.md)（`process-supervision`）：逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。
- 2022-03-04 · 一作：Long Ouyang · [InstructGPT / PPO-RLHF](../2203.02155-ppo-rlhf/README.md)（`ppo-rlhf`）：只扩大语言模型不能保证更符合用户意图。InstructGPT 建立了经典三阶段流程：先用标注员示范做 SFT，再用成对排序训练 reward model，最后用 PPO 优化策略，同时以 KL 惩罚限制策略偏离 SFT/reference model。

## PRIME-RL author team

- 2025-04-22 · 一作：Yuxin Zuo · [TTRL](../2504.16084-ttrl/README.md)（`ttrl`）：同一测试题多次采样，以多数一致答案作为伪标签并即时更新模型，不访问 gold label。

## Peking University

- 2026-07-30 · 一作：Yuran Wang · [Flux-OPD](../2607.28022-flux-opd/README.md)（`flux-opd`）：固定上下文很快被学生吸收，直接更换上下文 teacher 又会让目标跳变。Flux-OPD 固定 context-free teacher 为锚，只注入多个演化上下文 teacher 相对锚点的 log-probability 差，并用几何均值归一化常数表示冲突、冲突越大修正越弱。
- 2023-12-14 · 一作：Peiyi Wang · [Math-Shepherd](../2312.08935-math-shepherd/README.md)（`math-shepherd`）：从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。

## Princeton University

- 2024-05-23 · 一作：Yu Meng · [SimPO](../2405.14734-simpo/README.md)（`simpo`）：DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。

## Reichman University

- 2026-08-12 · 一作：Lior Baruch · [Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations](../2608.12062-pto/README.md)（`pto`）：逐轮偏好只判断当前回答，难以优化目标导向对话的长期结果。PTO 让 agent 和虚拟用户展开候选对话树，oracle 评价当前回答及未来延续，以偏好对迭代执行 DPO；更深 look-ahead 带来更稳定的长期策略。

## Renmin University of China

- 2026-07-06 · 一作：Yu Li · [Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment](../../reproductions/2607.04728-sis/README.md)（`sis`）：异步 rollout、样本复用和 stale policy 会让 LLM 强化学习变成 off-policy 更新。标准 importance sampling（IS）在长序列上连乘后方差很大，直接 clipping 又会丢失有效梯度。

## SAIL 研究团队

- 2025-03-26 · 一作：Zichen Liu · [Dr. GRPO](../2503.20783-dr-grpo/README.md)（`dr-grpo`）：原始 GRPO 的 response 内长度平均和组内标准差会引入长度与题目难度偏置。Dr. GRPO 移除这两个归一化项，保留中心化的组相对奖励，让每条轨迹以原始尺度参与更新。

## Seoul National University

- 2026-07-29 · 一作：Junoh Park · [ReCo](../2607.26862-reco/README.md)（`reco-grpo`）：GRPO 容易重复采到高概率回答，并继续放大已经占优的 token，导致大 $k$ 下推理路径覆盖率下降。ReCo 同时修正 response 和 token：按 rollout 组中的期望出现次数抑制高频回答，再用 Bernoulli 方差比把更新集中到尚未饱和的决策点。

## Shanghai Jiao Tong University

- 2026-07-30 · 一作：Kangning Zhang · [VAD](../2607.28590-vad/README.md)（`vad`）：多模态 OPD 直接匹配 privileged-view teacher 时，教师修正同时混入视觉证据、语言先验和教师自身偏差。VAD 对同一冻结教师分别输入“相关视觉证据存在/移除”两种视图，以 centered log-probability 差构造带符号的视觉方向，再把原教师修正单侧投影到该方向，重建以学生当前分布为锚的 target；完整 privileged teacher 只保留为弱正则。

## Stanford University

- 2026-05-18 · 一作：Muhammad Umer · [GPRL](../2605.18721-gprl/README.md)（`gprl`）：单一标量 reward 容易掩盖 helpfulness、格式、推理和简洁度之间的冲突。GPRL 先在每个偏好维度内部计算 group-relative advantage，再根据上下文聚合；漂移控制器检测某个维度是否主导训练并调整权重。
- 2023-05-29 · 一作：Rafael Rafailov · [DPO](../2305.18290-dpo/README.md)（`dpo`）：传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。

## Texas A&M University

- 2026-06-04 · 一作：Xingyu Su · [OPDLM](../2606.06712-opd-lm/README.md)（`opd-lm`）：ARLM 改成双向注意力后既会遗忘原知识，也有随机 mask 训练与 confidence decoding 推理之间的偏移。OPDLM 让双向学生在自身推理轨迹上生成，冻结 AR 教师在同一轨迹给 target logits。

## Tianjin University

- 2026-05-12 · 一作：Zhong Guan · [Missing Old Logits](../2605.12070-missing-old-logits/README.md)（`missing-old-logits`）：指出异步 RL 丢失历史训练侧 logits 后，训推校正与策略陈旧校正发生语义混叠；给出快照、old-logit model、中断同步和 PPO-EWMA 修复。

## Tsinghua University

- 2026-07-11 · 一作：Zhicheng Cai · [RIPO](../2607.10169-ripo/README.md)（`ripo`）：固定 PPO ratio 区间在低概率区域过于保守、在高概率区域又可能过大。RIPO 以 Fisher–Rao 几何定义策略距离，并按旧策略概率设置等距 clip 半径，使不同概率区域获得更均衡的局部 KL 预算。
- 2026-06-17 · 一作：Haipeng Luo · [STARE](../2606.19236-stare/README.md)（`stare`）：按 batch surprisal 分位数识别 entropy-critical token，重加权其 advantage，并以目标 entropy 闭环 gate 调节方向。
- 2025-05-06 · 一作：Andrew Zhao · [Absolute Zero](../2505.03335-absolute-zero/README.md)（`absolute-zero`）：proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。
- 2023-06-14 · 一作：Yuxian Gu · [MiniLLM](../2306.08543-minillm/README.md)（`minillm`）：标准 forward KL 倾向覆盖教师所有概率质量，小学生可能因此高估教师的低概率区域。MiniLLM 改用 mode-seeking 的 reverse KL，在学生自身生成分布上优化，并通过 teacher-mixed sampling、单步分解、长度归一化和 reward baseline 稳定策略梯度。

## University of California, Berkeley

- 2025-05-26 · 一作：Xuandong Zhao · [INTUITOR](../2505.19590-intuitor/README.md)（`intuitor`）：把答案分布相对均匀分布的 KL 作为 intrinsic self-certainty reward，在没有答案和 verifier 时优化。

## University of California, Los Angeles

- 2026-01-26 · 一作：Siyan Zhao · [OPSD](../2601.18734-opsd/README.md)（`opsd`）：普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。
- 2024-01-02 · 一作：Zixiang Chen · [SPIN](../2401.01335-spin/README.md)（`spin`）：额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。

## University of California, San Diego

- 2026-08-06 · 一作：Yijiang Li · [U-OPSD](../2608.06296-u-opsd/README.md)（`u-opsd`）：U-OPSD 不使用答案、环境奖励或更大教师。模型多次采样后做多数投票，以最短一致解作为 privileged view，定点修复最长且高置信错误轨迹，是真正依赖内部一致性的自蒸馏。
- 2025-08-05 · 一作：Feng Yao · [TIS](../web-2025-tis/README.md)（`tis`）：混合训练框架由 rollout 引擎采样、训练引擎重算 log-prob；即使权重相同，数值精度和 kernel 差异也会让行为分布与训练分布偏离。TIS 将训练侧与 rollout 引擎概率比乘入策略梯度，并只对过大的校正权重做单侧上截断，保留小权重样本而控制重尾方差。

## University of Maryland, College Park

- 2026-07-30 · 一作：Jiawei Xu · [β-OPSD](../2607.28582-beta-opsd/README.md)（`beta-opsd`）：论文指出 vanilla OPSD 是 β=1 的 KL 正则策略优化特例。先推导 reference policy 与 privileged teacher 之间的最优几何插值，再把昂贵高方差的 RL 解转成 token-logit 蒸馏目标，并以 return-to-go 做长推理信用分配。

## University of Notre Dame / Amazon

- 2026-08-05 · 一作：Zheyuan Zhang · [Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning](../2608.05080-rail/README.md)（`rail`）：**主题：rollout 预算分配。** 均匀 rollout 浪费预算，静态启发式又跟不上策略变化。

## University of Science and Technology of China

- 2026-08-04 · 一作：Ranxu Zhang · [ADRS](../2608.03223-adrs/README.md)（`adrs`）：privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。
- 2026-07-11 · 一作：Kexin Huang · [ARMOR](../2607.10481-armor/README.md)（`armor`）：单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。

## University of Washington

- 2025-04-21 · 一作：Jianhao Yan · [LUFFY](../2504.14945-luffy/README.md)（`luffy`）：把离线高质量推理与在线 rollout 放进同一 support，通过正则化 importance ratio 保留 on-policy 行为。

## VNU University of Engineering and Technology / Viettel AI

- 2026-08-05 · 一作：Nhat Minh Pham · [SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts](../2608.04962-specroll/README.md)（`specroll`）：**主题：RL rollout 加速。** RL 中 target policy 持续变化，静态 drafter 很快过时。

## WeChat / Tencent

- 2026-07-22 · 一作：Beining Wang · [Co-Evolving LLM Evaluators and Policies via DynamicRubric](../../reproductions/2607.20083-dynamic-rubric/README.md)（`dynamic-rubric`）：固定 judge 或固定 rubric 会在策略模型进步后失去区分力。DynamicRubric 根据当前 prompt 和一组候选回答动态生成评估维度与权重，用 discriminability 目标寻找能区分当代 hard negatives 的标准，用 anchor 目标限制评估器漂移，再让 evaluator 和 policy 多轮协同进化。

## Xiaomi

- 2026-06-29 · 一作：Wenhan Ma · [MOPD](../2606.30406-mopd/README.md)（`mopd`）：多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。

## Zhejiang University

- 2026-07-28 · 一作：Haolei Xu · [Relay-OPD](../2607.26057-relay-opd/README.md)（`relay-opd`）：检测学生前缀失效后让教师短暂接管，再把轨迹交还学生；有限接力预算把监督集中到关键早期位置。
- 2026-06-21 · 一作：Pengxiang Cai · [CoBA-RL](../2606.22317-coba-rl/README.md)（`coba-rl`）：普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。

## 论文未列机构

- 2026-08-03 · 一作：Chunji Lv · [PCSD](../2608.01837-pcsd/README.md)（`pcsd`）：单 token teacher gap 容易受噪声影响，整步共享权重又会抹掉位置差异。PCSD 在自适应窗口内指数累积 teacher-favoring signal，并对下降趋势衰减，最后用连续 sigmoid gate 与 GRPO 联合训练。
- 2026-07-22 · 一作：Xubo Liu · [TCR](../2607.19824-tcr/README.md)（`tcr`）：只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。

## 香港中文大学（深圳）/ 深圳市大数据研究院

- 2023-10-16 · 一作：Ziniu Li · [ReMax](../2310.10505-remax/README.md)（`remax`）：ReMax 利用 LLM RLHF 的三项特征：模拟快、token 转移确定、reward 通常只在轨迹末端给出。它删除 PPO 的 value model，以当前策略 greedy decoding 的 reward 作 prompt-dependent baseline，降低 REINFORCE 方差。
