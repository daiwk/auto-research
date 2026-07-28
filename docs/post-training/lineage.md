# LLM 后训练论文谱系与缺口

本页是系统审计账本：区分已实现的关键谱系、仍值得补的 P1，以及暂不应被“名字占位”
冒充复现的方法。筛选优先级综合经典影响力、机制差异、公开代码/数据和本地可验证性；
最新边界检查至 **2026-07-28**。

## 谱系覆盖

| 谱系 | 代表方法 | 状态 | 本仓库覆盖 |
|---|---|---|---|
| 经典 RLHF | PPO-RLHF、RLOO、ReMax | 已实现 | critic-based、leave-one-out、greedy baseline 三种路线 |
| 成对偏好 | DPO | 已实现 | reference-relative pairwise objective |
| 非成对/单阶段偏好 | KTO、ORPO | 已实现 | 单条二元反馈；SFT + odds ratio |
| Group-relative reasoning RL | GRPO、DAPO、GSPO | 已实现 | group advantage、非对称 token clip、sequence clip |
| On-policy distillation | Lightning OPD | 已实现 | 离线教师缓存 |
| 多目标与过程奖励 | GPRL、TCR | 已实现 | 分维 reward 与 checklist residual |

## 仍缺失但值得补的 P1

| 方法 | 为什么仍有价值 | 未在本批实现的原因 |
|---|---|---|
| IPO | 修正 DPO 在确定性偏好下的过拟合，是偏好目标理论谱系的重要节点 | 与当前 DPO/KTO/ORPO 的本地候选目标重叠较高，下一批需增加噪声偏好协议 |
| SimPO | reference-free、length-normalized preference objective，工程使用广 | 需要先把 response length 从伪长度升级为真实 tokenizer trajectory |
| LUPO（2026） | 处理 RLVR 中长度偏置，适合长推理 evolve | 最新方法，需增加自由生成与真实长度 judge 后再实现 |
| CoBA-RL（2026） | 课程/边界自适应类 reasoning RL | 需要公开生成 benchmark，L1 候选空间不足以支撑结论 |

## 当前结论

当前已覆盖“RLHF → 直接偏好 → 单样本/单阶段偏好 → group-relative reasoning RL →
蒸馏/多目标/过程奖励”的主干。下一步不应继续堆相似 loss 名称，而应先把 L1 六候选
评测升级到真实 tokenizer、自由生成、verifier 和多 seed，再接 IPO/SimPO/LUPO。
