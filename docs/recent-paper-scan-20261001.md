# 2026-10-01 P0/P1 全量实现批次

## 扫描结论

本轮复核 arXiv 官方 2026-09-30 announcement 及论文完整 HTML/PDF；截至
2026-10-01，官方 daily 页面尚无 `2610.*` 新编号。去除仓库已实现的 Video-RSI
后，共识别 16 篇可在当前证据和算力边界内保真实现的 P0/P1 条目，并全部进入
可执行代码、三种子 L1 机制指标、中文详情页、关键原论文图和统一目录。

Google / Meta 相关候选优先阅读全文。RECAP CTR 的正文没有量化线上 A/B，因此不
作为工业推荐证据；本轮根据用户明确批准，仅作为学术诊断和可执行 Evolve 算子
收录。CohortMix-TS 的 25 天随机部署显著结果来自 post-assignment 完整窗口子组，
文档保留该限制，不把 6.23 个百分点外推为全体用户收益。

## 本轮 P0

| 论文 | 领域 | 本地实现 |
|---|---|---|
| Thinking Before Thinking | Agent | 元推理 dispatch、预算与审计状态 |
| Context Language Models | Agent | context file、suffix cache 与分支状态 |
| Learning Meta-Skills for Agent Harness Design | Agent / RSI | 可版本化 meta-skill bank |
| Mixture of Self-Improving Branches | Agent / RSI | 分支子集更新与路由 |
| AdviSD | 后训练 | targeted contrast、advisor gate |
| Guide, Then Let Go | 后训练 / Agentic RL | gap-adaptive teacher schedule |
| CohortMix-TS | 推荐 | cohort prior、Thompson slate、posterior update |

Video-RSI（arXiv:2609.37950）已在上一批实现，本轮只复核并保留去重终态。

## 本轮 P1

| 论文 | 领域 | 本地实现 |
|---|---|---|
| RECAP CTR | 推荐 / Evolve | 共享递归 route、trajectory EMA、`rankmixer_recap` |
| MAESTRO | 后训练 | teacher/student dissonance 与 intervention |
| Interpolated Policy Distillation | 后训练 | off/on-policy 可控插值 |
| FlowMap-OPD | 后训练 | rollout/kernel 分离损失 |
| V-JEPA Policy | 基础模型 / 多模态 | predictive visual latent action loss |
| CE-guided MoE | 基础模型 | token-error 路由辅助目标 |
| TADM | 基础模型 | time-anchored latent cache fusion |
| PUMBA | 基础模型 | trajectory-aware masked diffusion window |
| SPLASH | 基础模型 / serving | 并行布局选择与无缝 handoff 状态 |

## 证据与运行边界

- 全部新增指标均为 `diagnostic_only=true` 的 schema-v2 机制诊断，不进入正式能力排行。
- 本批新增路径均可在 CPU 执行，没有新增或升级对外宣称依赖 CUDA 的训练路径，因此
  不触发 A100/A30 GPU 验证门槛；SPLASH 只实现可审计布局规划，不冒充 CUDA 通信栈。
- 论文关键图来自 arXiv 官方 HTML 或官方 PDF 图注裁剪，并记录在统一 figure manifest。
- 下一轮从 2026-10-01 起扫描，并保留至少两天重叠窗口；不把历史高召回候选重复计为新论文。
