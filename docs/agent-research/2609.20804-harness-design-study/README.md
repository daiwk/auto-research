# An Empirical Study of Harness Design for Coding Agents

> **复现级别：L1 核心机制诊断。** 本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [An Empirical Study of Harness Design for Coding Agents](https://arxiv.org/abs/2609.20804) |
| 公司/机构 | University of Massachusetts Amherst（按第一作者署名单位） |
| 首次公开日期 | 2026-09-17（arXiv v1） |
| 原文开源代码 | 否：截至 2026-09-19 未找到原作者公开实现仓库 |
| Adapter / 方法 | `harness-design-study` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260919.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260919.py) |

## 原始论文总结

### 背景与主要改动

固定底层执行循环，分别控制 planning、action space 与 context management，隔离 coding-agent harness 中真正影响效果和成本的因素。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[harness-design-study 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![An Empirical Study of Harness Design for Coding Agents 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2609.20804v1/fig_harness_overview_v2.png)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.20804)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、权重、状态转换或调度规则，并把中间量写入指标产物；具体公式与变量对应见实现函数及测试中的不变量断言。

### 论文离线与线上效果

论文报告的线上、benchmark、训练效率或推理速度只作为原文结果。本地三种子 artifact 只验证核心机制、形状和状态不变量，不与论文数字直接横比。指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。

## 复现边界

本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。
