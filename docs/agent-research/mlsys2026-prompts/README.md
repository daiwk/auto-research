# PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving

> **复现级别：L1 核心机制诊断。** 本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving](https://research.google/pubs/prompts-performance-optimization-via-multi-agent-planning-for-llm-training-and-serving/) |
| 论文标识 | MLSys 2026 Industry Track（仓库 ID：`mlsys2026-prompts`） |
| 公司/机构 | University of Maryland / Google（按第一作者署名单位） |
| 首次公开日期 | 2026-05-18 |
| 原文开源代码 | 否：未找到作者公开仓库（核查日期：2026-09-14） |
| Adapter / 方法 | `prompts` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260914.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260914.py) |

## 原始论文总结

### 背景与主要改动

Coordinator、Analyzer 和 Proposal Agent 联合读取 profiler 与知识库，诊断瓶颈并输出可解释的 sharding 候选。

```mermaid
flowchart LR
  I[输入与公开状态] --> M[prompts 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving 原论文 Figure 2](assets/paper-figure-01.png)](https://storage.googleapis.com/gweb-research2023-media/pubtools/1038279.pdf#page=3)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://research.google/pubs/prompts-performance-optimization-via-multi-agent-planning-for-llm-training-and-serving/)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式或操作

本地代码把论文决定性操作实现为确定性的 reference kernel，并显式输出门控、选择、投影、图边或状态更新统计；测试覆盖公式不变量和边界条件。

### 论文离线与线上效果

8 个生产工作负载最高提升 434%；工程师最终采用方案始终在 top-3，top-1 命中 87.5%。 这些数字来自原论文，不与本地缩小实验直接比较；论文未报告线上 A/B 时不推断线上收益。

## 本地复现

三种子指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。

### 复现边界

本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。
