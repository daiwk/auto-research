# 近期论文扫描与实现（2026-09-07）

## 扫描范围与口径

- 请求窗口为 2026-09-05 至 2026-09-07；为覆盖周末、跨源延迟和晚公告，实际查询窗口向前重叠两天至 2026-09-03。
- 四条高召回轨道共返回推荐 211、基础模型 258、后训练 95、Agent 211 个去重候选；与仓库和历史审计去重后，真正待复核的新候选分别为 11、54、23、72。
- 工业候选继续检查正文而非只读摘要；Google / Google DeepMind / Meta 优先查询本轮没有产生新的待实现命中。
- 所有新候选均已写入 [`paper-discovery-ledger.json`](paper-discovery-ledger.json) 的 implemented/rejected 终态；跨轨道论文只实现一次，但保留每条发现来源。

## 本轮实现

| 轨道 | 论文 | 级别 | 进入原因与本地入口 |
|---|---|---|---|
| 工业推荐 | [AlleCompanion](reproductions/2609.05063-allecompanion/README.md) | P0 | 两周 100% 平台流量和量化 GMV；类别约束双塔、ComCat 与 Category Adapter |
| 工业研究自动化 | [AutoLR](reproductions/2609.04871-autolr/README.md) | P0 | 1,586 次离线评估、9 次上线评审与线上提升；多专家、证据预算和确定性晋级门 |
| 基础模型 / 推理 | [BeaconKV](reproductions/2609.04971-beaconkv/README.md) | P1 | 固定预算下用 query beacon 保留远程 KV；需要真实 checkpoint GPU gate |
| 基础模型 / Agent 系统 | [KVMEM](reproductions/2609.04852-kvmem/README.md) | P1 | 开源代码、百万 token 公共评测；query-conditioned 分页 KV 工作视图 |
| LLM 后训练 | [Sparse OPD](post-training/2609.04565-sparse-opd/README.md) | P0 | 九种教师—学生组合；每轨迹仅监督 1–2 个关键 token 的独立目标函数 |
| Agent 推荐 | [AtomRec](agent-research/2609.04882-atomrec/README.md) | P1 | 四个公开基准；原子协同记忆和多跳证据路径 |
| Agentic RL | [CoSkill](agent-research/2609.04865-coskill/README.md) | P0 | 原作者代码、ALFWorld/WebShop；推理与元技能策略联合进化 |
| Agent verifier | [SiLR](agent-research/2609.04629-silr/README.md) | P1 | shadow execution、乘积序安全准入与同源过程奖励 |
| Agentic RL 审计 | [Multi-Harness RL](agent-research/2609.04518-multi-harness-rl/README.md) | P1 | 24,000 次 sealed 评估揭示 harness 混杂；加入 held-out harness 审计协议 |

九篇均已补齐论文信息块、中文机制说明、原论文关键图、公式、三随机种子指标、复现边界和 Evolve 映射。AlleCompanion 与 AutoLR 使用公开 MovieLens 对照；后训练和 Agent 使用统一机制 mini-suite；BeaconKV 与 KVMEM 另受 A100/A30 真实 checkpoint gate 约束。

## 下一轮水位

下一轮从 **2026-09-07** 继续增量扫描，并保留公告日重叠；本轮终态候选不会重复进入待实现队列。
