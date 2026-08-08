# LLM 后训练论文谱系与缺口

本页是系统审计账本：区分已实现的关键谱系、仍值得补的 P1，以及暂不应被“名字占位”
冒充复现的方法。筛选优先级综合经典影响力、机制差异、公开代码/数据和本地可验证性；
最新边界检查至 **2026-08-08**。

## 谱系覆盖

| 谱系 | 代表方法 | 状态 | 本仓库覆盖 |
|---|---|---|---|
| 经典 RLHF | PPO-RLHF、RLOO、ReMax | 已实现 | critic-based、leave-one-out、greedy baseline 三种路线 |
| 成对偏好 | DPO | 已实现 | reference-relative pairwise objective |
| 非成对/单阶段偏好 | KTO、ORPO | 已实现 | 单条二元反馈；SFT + odds ratio |
| Group-relative reasoning RL | GRPO、DAPO、GSPO | 已实现 | group advantage、非对称 token clip、sequence clip |
| 训推失配校正 | TIS、IcePop、Online IcePop、KPop | 已实现 | 单侧截断、固定双侧 mask、纯在线单次更新、binary-KL 自适应 mask |
| On-policy / context distillation | GKD、MiniLLM、OPSD、OPCD、Lightning OPD、Relay-OPD、VAD | 已实现 | 学生轨迹、reverse KL、特权上下文自蒸馏、上下文能力内化、离线教师缓存、有限教师接力、视觉证据归因 target reconstruction |
| 多目标、过程奖励与分布保持 | GPRL、TCR、CoRT、ReCo | 已实现 | 分维 reward、checklist residual、反事实 token credit、响应/方差重权重 |
| 自由生成偏好 | IPO、SimPO | 已实现 | token-level sequence probability、reference-relative / reference-free |
| 长度与能力边界 | LUSPO、CoBA-RL | 已实现 | 长度无偏 sequence RL、动态课程边界与教师触发 |
| AI 反馈安全对齐 | Constitutional AI | 已实现 | 显式原则、自我批评/修订、AI preference |
| Reward-ranked SFT | RRHF、RAFT | 已实现 | 全排序约束；在线采样 top-response filtering |
| 序列校准与可控 SFT | SLiC-HF、SteerLM | 已实现 | preference margin；多属性条件 SFT |
| 自博弈对齐 | SPIN | 已实现 | 上一轮策略负例与迭代对手刷新 |
| AI feedback 与过程监督 | RLAIF、Let's Verify、Math-Shepherd | 已实现 | 顺序去偏 AI 标签、主动步骤标注、MC continuation 自动标签 |
| 自奖励与零数据课程 | Self-Rewarding、Absolute Zero、SPIRAL | 已实现 | 自判偏好、任务 proposer/verifier、自博弈语言游戏 |
| Test-time / intrinsic RL | TTRL、INTUITOR | 已实现 | 多数一致伪标签；self-certainty intrinsic reward |
| Off-policy 与序列稳定 | LUFFY、CISPO、ConSPO | 已实现 | 混合 support、token IS clip、长度归一化对比序列目标 |
| 异步/MoE 与 entropy 稳定 | Stabilizing RL、Missing Old Logits、STARE | 已实现 | Routing Replay、old-logit 语义分解与 EWMA 修复、surprisal 分位数和目标 entropy 闭环 |

## 下一阶段缺口

二级主题复查识别出的 11 个 P0 已全部实现：RLAIF、Let's Verify Step by Step、
Math-Shepherd、Self-Rewarding LM、LUFFY、TTRL、Absolute Zero、INTUITOR、CISPO、
SPIRAL 和 ConSPO。每种目标都进入统一 candidate-policy 训练器和 evolve genome；证据、
固定 seed 指标与去重说明见[全主题系统缺口审计](../full-domain-gap-review-20260808.md)。

同页识别的 3 个 P1 也已闭环：Stabilizing RL with LLMs、Missing Old Logits 与 STARE。

当前 L2 已具备 tokenizer、自由生成、verifier 与多 seed，但仍是小型 GRU。下一阶段是：

- 在 `gsm8k-generate` 上扩大训练并接入可下载的小型 pretrained causal LM；
- 为 CoBA-RL 增加 pass@k 边界缓存和真实教师模型；
- 为偏好方法接入 UltraFeedback 等公开 chosen/rejected 数据；
- GPU 路径增加 batch rollout、mixed precision 与 checkpoint resume。

## 当前结论

当前已覆盖“RLHF → AI 反馈安全对齐 → 直接/全排序偏好与 reward 选优 → 序列校准、
多属性条件 SFT 与自博弈 → 单样本/
单阶段偏好 → group-relative reasoning RL → 蒸馏/多目标/过程奖励 → 自由生成偏好与
能力边界”的主干。L1 candidate 与 L2
free-generation 路径独立保留，报告不能把两类 accuracy 混成同一公平表。

本轮系统复查补齐了 OPSD 和 OPCD：前者代表“学生自身作为带特权解题上下文的
on-policy 教师”，后者代表“把经验或系统提示从 context-conditioned teacher 蒸馏进
context-free student”。二者均已进入统一后训练 genome，不再只是独立复现入口。
