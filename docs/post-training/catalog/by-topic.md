# LLM 后训练：按主题

按论文解决的核心问题分组；每篇论文独占一行，简介直接概括主要机制，实验结果与复现边界请进入详情页查看。

## AI 反馈安全对齐

- [Constitutional AI](../2212.08073-constitutional-ai/README.md)（`constitutional-ai`）：人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。

## Context distillation

- [OPCD](../2602.12275-opcd/README.md)（`opcd`）：提示词、检索文档和历史经验在上下文清空后会消失。OPCD 让无上下文学生生成轨迹，再由带经验或系统提示的教师沿同一轨迹打分，以 reverse KL 把高概率行为内化到学生参数中。

## On-policy distillation

- [Lightning OPD](../2604.13010-lightning-opd/README.md)（`lightning-opd`）：传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。
- [Relay-OPD](../2607.26057-relay-opd/README.md)（`relay-opd`）：检测学生前缀失效后让教师短暂接管，再把轨迹交还学生；有限接力预算把监督集中到关键早期位置。

## On-policy self-distillation

- [OPSD](../2601.18734-opsd/README.md)（`opsd`）：普通 OPD 仍需独立教师。OPSD 让同一个模型形成两个条件分布：学生只看问题，教师额外看到验证过的解题过程或答案。

## Reference-free 偏好

- [SimPO](../2405.14734-simpo/README.md)（`simpo`）：DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。

## Reverse-KL distillation

- [MiniLLM](../2306.08543-minillm/README.md)（`minillm`）：标准 forward KL 倾向覆盖教师所有概率质量，小学生可能因此高估教师的低概率区域。MiniLLM 改用 mode-seeking 的 reverse KL，在学生自身生成分布上优化，并通过 teacher-mixed sampling、单步分解、长度归一化和 reward baseline 稳定策略梯度。

## Reward 选优微调

- [RAFT](../2304.06767-raft/README.md)（`raft`）：PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。

## Token-level credit assignment

- [CoRT](../2607.25659-cort/README.md)（`cort`）：对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。

## 二元反馈对齐

- [KTO](../2402.01306-kto/README.md)（`kto`）：DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。

## 偏好正则

- [IPO](../2310.12036-ipo/README.md)（`ipo`）：论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 $\Psi$PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。

## 全排序偏好

- [RRHF](../2304.05302-rrhf/README.md)（`rrhf`）：PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。

## 分布保持 RL

- [ReCo](../2607.26862-reco/README.md)（`reco-grpo`）：GRPO 容易重复采到高概率回答，并继续放大已经占优的 token，导致大 $k$ 下推理路径覆盖率下降。ReCo 同时修正 response 和 token：按 rollout 组中的期望出现次数抑制高频回答，再用 Bernoulli 方差比把更新集中到尚未饱和的决策点。

## 单阶段偏好

- [ORPO](../2403.07691-orpo/README.md)（`orpo`）：常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。

## 在线推理 RL

- [DeepSeekMath / GRPO](../2402.03300-grpo/README.md)（`grpo`）：PPO 的 value model 与 policy 同规模，数学推理 RL 训练显存昂贵。GRPO 对同一问题采样一组 response，以组内 reward 均值和标准差构造 advantage，删除 critic；策略部分仍使用 old policy ratio、clipping 与 reference KL。

## 多属性可控 SFT

- [SteerLM](../2310.05344-steerlm/README.md)（`steerlm`）：传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。

## 多目标 RL

- [GPRL](../2605.18721-gprl/README.md)（`gprl`）：单一标量 reward 容易掩盖 helpfulness、格式、推理和简洁度之间的冲突。GPRL 先在每个偏好维度内部计算 group-relative advantage，再根据上下文聚合；漂移控制器检测某个维度是否主导训练并调整权重。

## 序列概率校准

- [SLiC-HF](../2305.10425-slic-hf/README.md)（`slic-hf`）：PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。

## 直接偏好优化

- [DPO](../2305.18290-dpo/README.md)（`dpo`）：传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。

## 稳定序列 RL

- [GSPO](../2507.18071-gspo/README.md)（`gspo`）：GRPO/PPO 常逐 token 裁剪 ratio，但 reward 在完整序列级给出；长序列中单个异常 token 会造成大量裁剪，MoE routing 变化还会放大不稳定。GSPO 对每条 response 取平均 log-ratio，再指数化为单一 sequence ratio，整条序列共享 clip 权重。

## 经典 On-policy distillation

- [GKD](../2306.13649-gkd/README.md)（`gkd`）：固定教师轨迹会让学生训练时看到的前缀与推理时自身生成的前缀不一致。GKD 让学生生成当前策略轨迹，再让教师在这些学生实际访问的状态给出完整分布；同时用 `student data fraction` 在固定数据和 on-policy 数据之间插值，并允许 forward KL、reverse KL 或广义 JSD。

## 经典 RLHF

- [InstructGPT / PPO-RLHF](../2203.02155-ppo-rlhf/README.md)（`ppo-rlhf`）：只扩大语言模型不能保证更符合用户意图。InstructGPT 建立了经典三阶段流程：先用标注员示范做 SFT，再用成对排序训练 reward model，最后用 PPO 优化策略，同时以 KL 惩罚限制策略偏离 SFT/reference model。
- [ReMax](../2310.10505-remax/README.md)（`remax`）：ReMax 利用 LLM RLHF 的三项特征：模拟快、token 转移确定、reward 通常只在轨迹末端给出。它删除 PPO 的 value model，以当前策略 greedy decoding 的 reward 作 prompt-dependent baseline，降低 REINFORCE 方差。
- [RLOO](../2402.14740-rloo/README.md)（`rloo`）：PPO 为一般长时域 RL 设计，价值网络、GAE 和多轮 clipping 给 LLM RLHF 带来较大显存与调参开销。RLOO 把一整段 response 视作一个 action；同一 prompt 采样多个 response，用其余样本的平均 reward 作为当前样本 baseline。

## 能力边界课程

- [CoBA-RL](../2606.22317-coba-rl/README.md)（`coba-rl`）：普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。

## 自博弈微调

- [SPIN](../2401.01335-spin/README.md)（`spin`）：额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。

## 过程奖励

- [TCR](../2607.19824-tcr/README.md)（`tcr`）：只奖励最终答案会遗漏推理质量，直接叠加过程奖励又可能重复计算 outcome。TCR 为每个样本构造 thinking checklist，并从过程得分中减去 outcome 的指数滑动基线，把更新集中到“结果奖励尚未解释的思考增益”。

## 长度无偏 RL

- [LUSPO](../2602.05261-luspo/README.md)（`luspo`）：论文从目标函数分解解释不同 RLVR 算法为何产生不同的响应长度轨迹，并指出 GSPO 的 sequence ratio 仍含长度偏置。LUSPO 对 sequence log-probability 作长度无偏归一化，避免训练中的长度坍塌。

## 长推理 RL

- [DAPO](../2503.14476-dapo/README.md)（`dapo`）：长 CoT 的在线 RL 容易被标准对称 clip 限制探索，且全对/全错的组没有学习信号。DAPO 用 Clip-Higher 放宽概率上升、Dynamic Sampling 丢弃零方差组、token-level loss 公平处理不同长度，并对过长回答分段惩罚。
