# 近期论文扫描记录（2026-09-15）

## 覆盖声明

- 重叠窗口：2026-09-10 至 2026-09-15；覆盖工业搜广推、基础模型、后训练与 Agent；
- 来源：arXiv 官方 recent/摘要/HTML/PDF、论文中的生产实验段落及作者官方仓库；
- arXiv API 在本轮持续连接重置，因此用官方 recent 页面逐页复核，但不把该降级路径写成全源穷尽；
- Google / Meta 仍按机构与主题反向检索并最高优先；摘要未写 A/B 不作为拒绝理由；
- 上一轮 watermark 保持在 2026-09-11；下一轮继续从 2026-09-10 重叠扫描。

## 本轮已实现

| 优先级 | 领域 | 论文 | Adapter | 实现与证据边界 |
|---|---|---|---|---|
| P0 | 广告 | PinDCO（2609.11943） | `pindco` | 组件增量融合与 PAM；原文 Pinterest Ads CTR +3.09% 并已上线 |
| P0 | 召回 | MIMA（2609.12842） | `mima` | 多正例排他分配与 activation routing；原文七天 A/B 交易数 +5.60% |
| P0 | 长序列排序 | ChronicleRec（2609.12375） | `chronicle-rec` | 近密远疏、时间锚点与多 horizon；原文七天 A/B GMV +1.61% |
| P1 | 基础模型 | SAS（2609.13141） | `sas-attention` | WikiText-2 上端到端训练连续 log-gate selector；CPU reference 不声称 Triton 加速 |

四篇均提供独立中文页、完整论文信息、原文关键图、真实执行代码、三 seed 指标和明确的本地边界。

## 已登记但未冒充完成

| 优先级 | 论文 | 状态 | 原因 / 恢复条件 |
|---|---|---|---|
| P1 | OneLA（2609.12399） | DEFERRED | 定义性贡献是大 beam recurrent state sharing 与 fused GPU kernel；需在 A100/A30 完成真实 kernel、显存和 decode latency 验证 |
| P1 | CanvasAnneal（2609.13060） | DEFERRED | 需可下载 diffusion LM、teacher canvas curriculum 与公开 RL/tool-use 训练预算，不能以普通 AR-LM heuristic 代替 |
| P1 | GAUGE（2609.12191） | DEFERRED | 值得进入 Agent 统一评测，但需取得公开 transcript/盲评标注并实现 grounded reward 排名一致性协议 |
| P1 | AMDKernelVault（2609.12471） | DEFERRED | 目标平台为 AMD ROCm/HIP；当前 A100/A30 不能验证定义性执行环境，等待 ROCm 机器 |

这些条目已进入 ledger 的终态队列；条件未满足前不创建占位 adapter，也不会推进扫描 watermark。
