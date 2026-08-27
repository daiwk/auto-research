# 2026-08-27 最新论文增量扫描

本轮按 arXiv 公告日扫描，并把 API 时间窗向前重叠一天：页面在 8 月 27 日展示的论文，API
`published` 可能仍是 8 月 26 日。推荐、基础模型、后训练和 Agent 四路去重后分别召回
6 / 50 / 14 / 38 个候选；逐项全文复核后实现 14 篇。Google / Meta 继续最高优先，
但机构优先不豁免工业论文的量化线上证据门槛。

## 本轮实现

| 领域 | 论文 | 第一作者机构 | 本地结论 |
|---|---|---|---|
| 工业推荐 | [DCEO](reproductions/2608.25635-dceo/README.md) | Alibaba | 41 天 A/B GMV +0.36%；公开 proxy 上 Hit 提升、NDCG 略降 |
| 工业推荐 | [TransRetrieval](reproductions/2608.25528-transretrieval/README.md) | RUC / Alibaba | 一个月 5% 流量收入 +2.53%；本地 Hit@10 +11.76% |
| 基础/多模态 | [VBVR-Pro](reproductions/2608.26105-vbvr-pro/README.md) | NTU | 可执行 verifier 明显优于带噪 scalar judge analogue |
| 基础/多模态 | [MLLMCLIP](reproductions/2608.25575-mllmclip/README.md) | KAIST / Sony | attention selection + CKA 路径可运行；proxy 指标仅诊断 |
| 后训练 | [V-Rubrics](post-training/2608.25580-v-rubrics/README.md) | NTU | 多维、prefix-localized rubric credit |
| 后训练 | [Clue-OPSD](post-training/2608.25356-clue-opsd/README.md) | UMD | 训练期 clue teacher、推理期完整视频 student |
| 后训练 | [GRIN](post-training/2608.25243-grin/README.md) | UC Merced | 失败 rollout 注入 golden response 与 mixed-policy 校正 |
| 后训练 | [GRIP](post-training/2608.25583-grip/README.md) | Peking University | reward-guided policy interpolation |
| Agent | [JIT-Agent](agent-research/2608.25593-jit-agent/README.md) | LV-NUS Lab | harness 生成、修复、archive 蒸馏；本地 joint success 仅 0.15 |
| Agent | [TraceML](agent-research/2608.26086-traceml/README.md) | CMU | 四阶段开发轨迹与旧方案重开 |
| Agent | [AdaVDR](agent-research/2608.25559-adavdr/README.md) | Alibaba | tool necessity filtering 与可靠性反思 |
| Agent | [TOPAS](agent-research/2608.25523-topas/README.md) | USTC | critical-path 与 prefix reuse 联合调度 |
| Agent | [CaSKG](agent-research/2608.25500-caskg/README.md) | Jilin / Ant | 反事实探针和 Bayesian 技能图校准 |
| Agent | [ProgRouter](agent-research/2608.25992-progrouter/README.md) | Aston | 进展/成本在线逐步路由 |

## 工业证据终态

- **AMBER（Meta，2608.25546）拒绝进入工业实现队列**：已全文检索实验章节，未发现
  量化生产 A/B 或明确全流量发布。它仍被记录为 Meta 优先候选；拒绝原因不是“摘要没写”。
- **HSR、MOTIF 等学术推荐候选拒绝**：公开离线数据有价值，但不满足本项目工业搜广推
  新论文的线上证据硬门槛。
- DCEO 与 TransRetrieval 均通过正文证据门槛；线上结果和本地公开数据结果分栏记录，
  不进行跨口径换算。

## 扫描器修正

`discover_papers.py` 默认增加一天 announcement overlap，并同时保存用户请求窗口和实际
查询窗口。这样下次从 8 月 27 日之后增量扫描时，不会因 arXiv 公告日与 API UTC 日期错位
漏掉论文；重复项由 ledger identity 去重。

