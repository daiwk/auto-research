# 2026-09-30 重叠窗口扫描与收口

## 结论

本轮以 **2026-09-27～2026-09-30** 为请求窗口，分别运行推荐、基础模型、后训练、Agent 四条官方 arXiv 高召回查询。四条 arXiv 传输均完整、缓存回退为 0；候选总数 197 / 1081 / 569 / 976，是多查询、分页和跨主题重复产生的**高召回池**，不是一天内出现的合格新论文数。按 arXiv v1 日期切到 2026-09-29 后，分别为 8 / 127 / 62 / 78 条，仍须正文门槛、查重和可复现性终审。

机构官方论文页的跨来源抓取在 TLS 读取阶段超时，因此本轮只确认 arXiv 来源完整，**跨来源覆盖不完整、watermark 不推进**。没有使用 DeepXiv，也不以第三方摘要替代原文。

## 本轮实现

| 论文 | 领域 / 优先级 | 终态与依据 |
|---|---|---|
| [HELIX](reproductions/2609.37183-helix/README.md) | 工业推荐 P0 | TikTok 电商完整流量 A/B，正文 Section 3.5 / Tables 4–5；实现三流 token、单向可复用缓存与 MPTF 机制 |
| [STEPQuant](foundation-models/2609.38169-stepquant/README.md) | 基础模型 P1 | 官方代码可用；实现时间寿命 × 空间影响 bit 分配与双轴 scale |
| [LeapQuant](foundation-models/2609.38166-leapquant/README.md) | 基础模型 P1 | 实现窗口量化、补偿 token 与 residual smoothing |
| [Chinese-Jev](foundation-models/2609.36965-chinese-jev/README.md) | System One P1 | 实现中文候选 marker 决策头及 CE/RLCD 目标 |
| [Dr. OPD](post-training/2609.38025-dr-opd/README.md) | 后训练 P1 | 官方代码可用；实现双层问题导出的 token credit 与加权 OPD |
| [SIPO](post-training/2609.36742-sipo/README.md) | 后训练 P1 | 官方代码可用；实现双上下文 contrastive self-teacher 与逐 token advantage |
| [ReMem](agent-research/2609.37311-remem/README.md) | Agent P1 | 官方代码可用；实现时间演化记忆和 Multi-Memory GRPO 机制 |
| [Video-RSI](agent-research/2609.37950-video-rsi/README.md) | Agent / RSI P1 | 官方代码可用；实现准确率—视觉成本 Pareto 接纳门槛 |

上一批已在 [PR #180](https://github.com/daiwk/auto-research/pull/180) 实现 ROFT、LSPD、Harness Learning、MS-GLA 与 GraphHCA；本轮只补齐其发现台账和路线图，不重做实现。

## 已审但未实现

| 候选 | 终态 | 原因 |
|---|---|---|
| RECAP / arXiv:2609.37905 | rejected（工业实现门槛） | Google Research 候选已阅读全文，但没有量化线上 A/B 或用户认可的全流量部署证据；Google 优先意味着优先审，不意味着绕过硬门槛 |
| SelfSearch / arXiv:2609.37968 | deferred | 定义性贡献依赖真实可执行搜索环境、reward-free 轨迹筛选与同预算 Agent 对照；当前小张量替代会丢失算法本体 |
| VACE / arXiv:2609.37105 | deferred | 需要可编辑多工具 Agent、真实执行反馈和跨代公平成本；不创建名称占位实现 |

## 后续扫描基线

下一轮继续保留至少三天重叠窗口，并首先重试 Google / Meta / DeepMind 官方来源。只有当 arXiv 与机构官方来源均得到可审计终态，才能推进发现 watermark；历史高召回池不会反复解释为“新论文”。
