# 近期论文扫描与实现（2026-09-05）

## 扫描范围与口径

- 时间窗：2026-08-31 至 2026-09-05；四条自动查询轨道分别覆盖搜广推、基础模型/多模态、LLM 后训练和 Agent。
- 原始高召回候选：推荐 37、基础模型 297、后训练 96、Agent 208。候选数不是待实现数；标题误命中、综述、纯应用和不能形成独立公开实验者均写入终态账本。
- 工业论文逐篇检查全文中的 online A/B、full rollout 与 production evidence，不能因为摘要没写 A/B 而漏掉。
- Google Research / DeepMind 和 Meta AI 官方发布页单独复核。Google/DeepMind 在窗口内没有新的符合本库四领域门槛的论文；Meta publications 源本轮返回 HTTP 500，已使用官方站点检索补查，并把源失败保留为审计信息而非当作“无候选”。

## 本轮实现

| 轨道 | 论文 | 级别 | 进入原因与本地入口 |
|---|---|---|---|
| 工业推荐 | [ReST](reproductions/2609.01240-rest/README.md) | P0 | 一周线上 A/B、核心收入 +11.93%、全量部署；双门控时序与共享前缀核心路径 |
| 工业推荐 | [TGR](reproductions/2609.00986-tgr/README.md) | P0 | 多场景 A/B/full launch；CCFormer、分层生成和 reason-token 组合 |
| 工业推荐 | [CAMIE](reproductions/2608.30255-camie/README.md) | P0 | Snap DPA 总体流量 CTR/CVR 增益并部署；共同互动多模态 embedding |
| 工业推荐 | [SetMIR](reproductions/2608.30251-setmir/README.md) | P0 | 生产召回源总体 CVR +3.1%；兴趣集合、presence 与 query NMS |
| LLM 后训练 | [GAPO](post-training/2609.00444-gapo/README.md) | P1 | 官方代码与公开数学/代码 benchmark；逐组自适应 clip 可独立测试 |
| Agent | [DRACO](agent-research/2609.04094-draco/README.md) | P1 | 官方代码、AppWorld/Tau-Bench；动态 rubric 与闭式步骤信用 |

六篇均具备论文信息块、中文方法说明、原论文关键图、核心公式、本地代码、指标产物、边界和 Evolve 映射。四篇推荐执行 MovieLens 100K 三 seed；GAPO 与 DRACO 执行统一 deterministic mini-suite。

## 后续资源门槛状态（2026-09-06 更新）

- [Random Attention](reproductions/2609.03430-random-attention/README.md)：已完成核心机制、真实 Qwen checkpoint KV 等预算 A100 验证和 Evolve 映射。
- [Lngram v2](reproductions/2609.03426-lngram-v2/README.md)：已完成离散路由、memory readout、反事实梯度、真实 VLM hidden state A100 验证和 Evolve 映射。
- [CORAL](reproductions/2609.02730-coral/README.md)：纠正摘要级误拒；全文的多处 A/B/部署证据已登记并实现。
- [RecEvolve](reproductions/2609.01622-recevolve/README.md)：通过 arXiv ID 月份 late-arrival 召回，已实现多轮研究控制器。

其余高召回项已经在 [`paper-discovery-ledger.json`](paper-discovery-ledger.json) 获得终态，不会在下次窗口重复出现。下一轮增量水位从 **2026-09-05** 继续；扫描同时使用 API 公开日期、公告重叠日和 arXiv ID 月份，覆盖修订、跨源延迟和晚索引记录。
