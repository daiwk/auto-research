# 2026-10-13 标签访问与状态计数角色核验

这是人工检查后的源码角色记录，不是能力验收证书。对 AST inventory 新增/变化的 14 个文件，
检查参考答案流向、生成消息、训练目标和状态计数；GPU 状态单独由 [TODO](oct13-gpu-todo.md) 维护。

| 源码/角色 | 标签边界 | 计数与限制 |
| --- | --- | --- |
| `oct13_common.evaluate`、State `evaluate` | 模型消息仅 question；answer 只进入外部 scorer | accuracy=0 仍保留，不能以真实更新替代能力提升 |
| 难度课程 `run` | 当前策略 question-only rollout；verifier correctness 控制 difficulty band | validation 只用于 staged 选择；零有效更新不推进 stage，长度奖励不冒充 correctness |
| MagicBeanStalk 构建/验证 | 离线训练数据构建 teacher 可看 train problem/trace；独立重解只看 question；student scaffold 不含 parent answer/完整 plan | teacher effectivity/novelty 判断不是形式证明；所有拒绝与重新校准计入成本 |
| Progressive contraction | question-only teacher backbone 和续写，answer 仅验证；已验证 teacher token 是 train SFT target | teacher profiling 成本与 exposure reduction 分开，不冒充总计算节省 |
| SynthSelf | train-only aligner/self-builder 明确以训练答案作改写条件；被评估 student 只看 question | target NLL 不是 generation hint；Eq.6 不满足须保持 failed，不晋级 |
| UPTURN | answer 只产生训练标签、救援奖励与外部评估；inference gate/cut head 不读答案 | encoder/token 成本对应真实调用；新轮直接拼接保留原 token，不以重编码代替 |
| SOAR | policy/internal recall/retriever 不收 gold；`final.answer` 是模型自己的提交；row.answer 只用于奖励/scorer | 外部 corpus 必须是独立公开知识库，不得以答案库替代；实际轨迹成本计入 ledger |
| SkillDreamer | 输入 question 与 generic skills；reference 独立保存在外部 scorer，PSG/HSR/CSI 无 reference 参数 | calls/token 计数来自实际 model.generate；skill load count 不等于成功 |
| Beyond / ReplaySSM | search/refresh 计数只描述已执行计算路径 | 不据此单独宣称 retrieval success、kernel 带宽或任务能力 |

相关行为测试覆盖 question-only 生成、scaffold 泄漏拒绝、exact-prefix、零优势拒绝与代价核算。
AST 辅助清单仍不覆盖动态键或全程序污点传播，因此不能把 inventory 更新说成完整语义证明。

本轮新增/修改 CUDA 门禁不因网络暂停而放宽；缺失或旧 source receipt 继续作为待完成项。
