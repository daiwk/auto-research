# SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs

> **复现级别：L1 核心机制诊断。** 本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs](https://arxiv.org/abs/2609.10901) |
| 公司/机构 | Duke University（按第一作者署名单位） |
| 首次公开日期 | 2026-09-09 |
| 原文开源代码 | 是：[https://github.com/DukeNLP/SearchAtlas](https://github.com/DukeNLP/SearchAtlas) |
| Adapter / 方法 | `searchatlas` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260914.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260914.py) |

## 原始论文总结

### 背景与主要改动

把搜索轨迹转为 query—evidence—answer 有向图，审计证据是否真正覆盖问题约束和最终回答。

```mermaid
flowchart LR
  I[输入与公开状态] --> M[searchatlas 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.10901v1/Figure1.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.10901)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式或操作

本地代码把论文决定性操作实现为确定性的 reference kernel，并显式输出门控、选择、投影、图边或状态更新统计；测试覆盖公式不变量和边界条件。

### 论文离线与线上效果

自动图解析相对人工标注平均 edge F1 为 86.0%。 这些数字来自原论文，不与本地缩小实验直接比较；论文未报告线上 A/B 时不推断线上收益。

## 本地复现

三种子指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。

### 复现边界

本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。
