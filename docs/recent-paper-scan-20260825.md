# 2026-08-25 最新论文增量扫描

## 扫描范围与口径

- 时间边界：接续已关闭的 2026-01-01～2026-08-24 历史扫描；本次读取 2026-08-25 可见的 arXiv 新日批次（条目标注 2026-08-24 UTC）。
- 来源：arXiv API `submittedDate` 全量分页、DeepXiv 语义检索、论文 HTML/PDF 正文和官方代码仓库。
- 领域：工业搜广推与 LLM 应用、基础模型、多模态、LLM 后训练、Agent。
- 工业门槛：搜广推仍要求量化线上 A/B 或可核验全流量证据；摘要不是证据门槛，需审正文。

## 本轮结论

329 篇 `cs.IR/cs.LG/cs.CL/cs.AI/cs.CV` 新条目完成元数据扫描。未发现满足线上证据硬门槛的新工业搜广推论文；因此没有把 ANR-DiffRec、SST 等公开数据集推荐论文写成工业落地。

本轮实现四篇具备明确新机制和公开实验的论文：

| 领域 | 论文 | 选择理由 | 状态 |
|---|---|---|---|
| 后训练 | [SRPO](post-training/2608.23493-srpo/README.md) | 反思 patch 与同模型特权教师形成 token 级信用 | 已实现 |
| 后训练 | [ERPO](post-training/2608.23311-erpo/README.md) | 阿里/高德；把稳定正则移到 Query-KL，不直接压回答探索 | 已实现 |
| Agent | [Agent-G²](agent-research/2608.23318-agent-g2/README.md) | 百度；无需 probe rollout 的任务级高斯 guidance | 已实现 |
| Agent | [AutoSaddler](agent-research/2608.23041-autosaddler/README.md) | Microsoft 合作；失败 trace 驱动 durable harness 更新 | 已实现 |

## 已筛但本轮未进入实现

- ProxyFormer、Sigmoid Attention KV eviction：基础模型结构候选，待更高保真训练预算；
- E2S-Pruner、FOVEA、WnW：多模态/语音推理效率候选，需真实 checkpoint 协议；
- ANR-DiffRec、SST：学术推荐候选，无工业线上 A/B，不进入工业搜广推队列；
- Prime Agent、SkillAlchemy、TRACE、GSAR：机制有价值，但与本轮两个 Agent P0 相比优先级较低，保留在后续增量候选中。

下一次扫描严格从本批次之后的新提交开始，同时继续执行 Google/Meta 工业正文优先反查。
