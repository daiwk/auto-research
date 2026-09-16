# Verifiable Social Reasoning for LLM Assistants

> **复现级别：L1 核心机制诊断。** 本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Verifiable Social Reasoning for LLM Assistants](https://arxiv.org/abs/2609.17496) |
| 公司/机构 | Google Research / Hebrew University of Jerusalem / University of Cambridge（按第一作者署名单位） |
| 首次公开日期 | 2026-09-15（arXiv v1） |
| 原文开源代码 | 否：截至 2026-09-16 未找到原作者公开仓库 |
| Adapter / 方法 | `fuse-evaluator` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260916.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260916.py) |

## 原始论文总结

### 背景与主要改动

用隐藏动机可验证的多 Agent 模拟评测用户转述、 framing bias 与社会推理。

本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。

```mermaid
flowchart LR
  I[公开输入与状态] --> M[fuse-evaluator 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或策略更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Verifiable Social Reasoning for LLM Assistants 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.17496v1/assets/viz1.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.17496)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

实现保留论文的决定性状态转换，并输出权重、门控、深度、阶段或缓存统计；固定预算和三种子只用于检查机制不变量，不等同于论文规模训练。

### 论文离线与线上效果

论文报告的能力、速度或成本结论只作为原文事实记录；本地指标不与其直接横比，也不外推线上收益。

## 本地复现

三种子结果见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。统一 receipt 标记 `diagnostic_only=true`，不会被公开看板当成完整能力提升。

### 复现边界

本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。
