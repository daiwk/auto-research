# 2026-09-30 官方来源重试与 P0/P1 合并批次

## 扫描结论

本轮继续使用 **2026-09-27～2026-09-30** 重叠窗口。推荐、基础模型、后训练与 Agent 四条 arXiv 查询全部完成，cache fallback 为 0。Google Research、Google DeepMind、Meta 与会议官方列表已恢复访问；但列表仍含无日期或尚未匹配 arXiv identity 的标题，所以跨来源状态是 `partial`，发现 watermark **不推进**。

同时修复了官方待审队列的两个噪声来源：已知日期但落在请求窗口之外的历史论文不再混入“本轮待审”；纯数字分页链接不再当论文标题。无日期标题仍保留待审，避免为了界面好看丢召回。

## 本轮实现

| 论文 | 领域 / 优先级 | 忠实实现与边界 |
|---|---|---|
| [GRP v0.1](reproductions/2609.36688-grp/README.md) | 工业推荐 P0 | Snap 多组线上 A/B；实现 block-wise SID decoding、detached MHP 与 mGRPO 召回保护，不复刻私有数据/服务 |
| [LIFT](foundation-models/2609.38149-lift-feedback/README.md) | 基础模型 P1 | top-k latent state、融合层与 CE + state KL；未做 1B 预训练 |
| [Triadic Linear Attention](foundation-models/2609.36529-triadic-linear-attention/README.md) | 基础模型 P1 | 三阶状态写入/双 query 收缩/衰减；未实现专用 GPU kernel |
| [OASIS](post-training/2609.37915-oasis/README.md) | 后训练 P1 | shortest verified scaffold、独立 context 与 clipped OPSD loss |
| [GRAFT](post-training/2609.37868-graft/README.md) | 后训练 P1 | all-fail peer group、compatibility gate 与 token clipping |
| [RIDE](post-training/2609.36484-ride/README.md) | 后训练 P1 | RL hidden residual 外推与 masked regression |
| [PR-OPD](post-training/2609.36642-pr-opd/README.md) | 后训练 / Agentic RL P1 | 多层特权表征对齐、teacher stop-gradient |
| [UserProxyBench](agent-research/2609.38043-userproxybench/README.md) | Agent 评测 P1 | 严格 UFS 与 premature disclosure 审计，和 agent reward 隔离 |
| [UpliftMem](agent-research/2609.36805-upliftmem/README.md) | Agent 记忆 P1 | paired set uplift 与 Gaussian EVSI probe |

九篇均有原文截图、元数据、三种子 L1 指标和单元测试；它们是公开核心机制，不是论文规模效果复现。没有新增或升级宣称 CUDA 的路径，因此本批不伪造 GPU gate；Triadic 的论文专用 GPU kernel 被明确列为未实现。

## 终态 deferred

S3、FOCUS、Traverse、LatCom、SkillGym、AnyAct、BRIDGE 与 RLTL;DR 依赖真实 checkpoint、大模型训练、浏览器/MCP/代码执行环境或大规模环境生成。它们已写入 ledger 的 terminal deferred，不用名称占位或随机张量冒充定义性算法。

## 下一扫描点

下一轮仍从 2026-09-28 左右保留至少三天 overlap；先重试 official unresolved queue，再看 2026-09-30 之后的新 arXiv。只有所有官方入口达到可审计终态，才推进跨来源 watermark。
