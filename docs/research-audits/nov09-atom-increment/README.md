# 11 月 9 日：官方 Atom 增量与优先机构核查

arXiv 列表仍返回 11 月 6 日快照。改从官方 Atom 的 `cs.AI`、`cs.LG`、`cs.CL` 首屏读取，得到 **217 个高于上批编号上界的去重候选**。这是初筛集合，不等于 217 篇都通过全文审查，也不等于这些论文在 11 月 9 日首次提交。逐篇记录原始 v1 时间；没有把 Atom 发现日填成公告日期。机构优先查 Google Research、DeepMind 与 Meta FAIR。

| 论文 | 本地 CPU 组件 | 完整实验不复现的原因 |
| --- | --- | --- |
| [Google DeepMind：Discovering formally verified quantum programs with AI](../../agent-research/2611.09822-verified-quantum-wiki/README.md) | 在外部验证结果之上执行 wiki 合入门槛 | Lean 题库与验证材料未公开；不尝试重跑多代理量子程序搜索 |
| [Meta FAIR / École des Ponts：e-means](../../foundation-models/2611.09501-e-means/README.md) | 流式质心更新、低使用率中心复活、闭合轮精确均值 | 原文大规模向量集、Faiss 检索性能矩阵超出预算 |
| [UNSW：ENGRAM](../../agent-research/2611.09472-engram-consolidation/README.md) | 成功示范准入、无记忆候选验证、分离归档和在线检索 | 完整多任务 8B LoRA、独立验证和推理矩阵超出预算 |
| [西南大学：RCEA](../../post-training/2611.09448-rcea/README.md) | 有限支持的熵分解及同前缀协方差 | 两个模型尺度、六个 RLVR 目标及固定探针矩阵超出预算 |

每篇完整实验标记为 **成本过高，不复现（审查 DONE）**；不自动重试。四项本地组件都只跑 CPU 的 L1 机制检查，三种子，不把合成样本当能力基准，不接入 Evolve。不声明 CUDA 路径，因此没有把 A100/A30 测试写成通过。

工业证据单独核对正文：Dual-Stream Fraud 的生产模型是离线对照；Reversible Rule Overlay 明确没有做线上 A/B；SteerGR 没有核实到生产受控实验或全量证据。未把这些计入工业复现。其它类别或未通过验证的线索没有宣称完成审查。

[覆盖范围与原文证据](source-coverage.json) · [固定预算](preflight.json) · [执行源与回执](frozen-sources.json) · [中英学习问答入口](../../learning/recent.md)

这次是**部分来源的增量交付**，不是整日公告闭环。全局审查水位仍是 **2026-10-15**。
