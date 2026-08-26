# 2026-08-26 最新论文增量扫描

本轮扫描覆盖 arXiv 在 2026-08-26 展示的新提交。对 `cs.AI`、`cs.LG`、`cs.CL`、
`cs.IR` 和 `cs.CV` 去重后共有 **363 篇**。流程先对全部元数据做关键词与语义召回，
再对高优先候选读取 HTML/PDF 全文；Google / Meta 另做机构反查，摘要没有写 A/B
不会成为拒绝理由。

## 本轮实现

| 领域 | 论文 | 机构 | 选择理由 |
| --- | --- | --- | --- |
| 工业推荐 | [TAGR](reproductions/2608.24034-tagr/README.md) | Kuaishou | 正文报告 LRE +8.5%、SCC +7.4%、Revenue +16.1% 的生产 A/B |
| 多模态基础模型 | [WeMM-Embedding](reproductions/2608.24053-wemm-embedding/README.md) | WeChat / Tencent | 两阶段多模态 embedding，14 项线上 A/B 后全量发布，并公开权重与代码 |
| LLM 后训练 | [OPDSearch+](post-training/2608.24310-opd-search-plus/README.md) | UCAS | 把搜索证据注入 on-policy distillation，再用 RL 闭环修正 |
| LLM 后训练 | [OPDVR](post-training/2608.24696-opdvr/README.md) | Tsinghua LeapLab | 用可验证奖励门控 token 级 on-policy distillation |
| Agent | [SPO++](agent-research/2608.24870-spo-plus-plus/README.md) | Renmin University | 异步 Agent RL 的事件时刻 value 冻结与 token measure 校正 |
| Agent | [SkillForge](agent-research/2608.24747-skillforge/README.md) | AMAP / Alibaba | 自动创建、验证、复用并修订显式技能 |
| Agent | [AHEAD](agent-research/2608.24114-ahead/README.md) | AWS AI Labs / Purdue | 用环境反馈和纠错提示形成稠密训练轨迹 |
| Agent | [SMITH](agent-research/2608.24571-smith/README.md) | Appier / NTU | 通过 schema、代码和执行结果三轴验证自改进工具 |

八篇均提供论文特有实现、固定指标、原文关键图、中文详情页和 evolve mutation。
本地实验为公开数据或确定性 mini-suite 的机制验证，不冒充论文规模复现。

## 工业线上证据审查

- **TAGR 通过**：正文 §4.3 / Table 1 给出同一生产下游栈上的多周 A/B，且三项
  线上指标均量化。
- **WeMM-Embedding 进入基础模型线**：论文说明 14 项线上 A/B 的收益已全量发布；
  报告没有公开具体幅度，因此不把它写成量化工业推荐 A/B。
- **RecGPT-Mobile-V2（2608.24295）拒绝进入工业实现队列**：全文讨论部署管线和
  检索分析，但没有找到量化生产 A/B 或明确全流量上线证据。
- **Intuit production recommender migration（2608.24132）拒绝**：属于生产迁移
  case study，但结果是固定人群离线评估，没有生产线上实验。
- **Native Multimodal Representation Learning for CTR（2608.24091）拒绝**、
  **RetrievalFormer（2608.24079）拒绝**、**Tlow（2608.24176）拒绝**：均未通过
  工业线上证据门槛。

本轮 Google / Meta 机构反查没有发现新的、同时满足主题范围与正文线上证据门槛的论文；
这表示“本日新批次没有通过项”，不表示后续无需继续反查。

## 本地结果边界

- TAGR 在 MovieLens-1M 的 NDCG@10 从 `0.11227` 降到 `0.08212`（`-26.86%`），
  但 head share@10 从 `0.7275` 降到 `0.1303`。这说明语义 ID 机制显著增加长尾覆盖，
  在该小型公开数据与当前超参数下没有换来排序收益。
- WeMM 两阶段对齐把 Recall@10 从 `0.56111` 提升到 `0.83889`，MRR 从
  `0.28627` 提升到 `0.50894`；它是 MovieLens 内容/协同双视图代理实验。
- OPDSearch+、OPDVR 在 arithmetic-smoke 上最终 accuracy 均为 `0.66406`；这是
  candidate-policy 算法冒烟验证，不是大模型 benchmark 结论。
- 四个 Agent 方法在 planbench-mini 上 joint success 都为 `1.0`，主要用于核验各自
  telemetry 和控制流，不用于宣称超过原论文基线。

下一次日批扫描从本批次之后继续；未通过项及理由已写入机器可审计 ledger，不会在下一轮消失。
