# Role-aware Heuristic Episodic Attention for Conversational LLMs

> **复现级别：L1 核心机制诊断。** 执行角色分离与 episodic top-k；不调用压缩 LLM。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1](https://arxiv.org/abs/2610.00958) |
| 公司/机构 | 原文首页未列第一作者机构（按第一作者署名单位） |
| 首次公开日期 | 2026-10-01（arXiv v1） |
| 原文开源代码 | 否：截至 2026-10-03 未找到原作者公开实现 |
| Adapter | `rea` |
| 本地复现代码 | [`src/auto_research/foundation_latest_20261003.py`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/foundation_latest_20261003.py) |

## 原始论文总结

### 背景与主要改动

把全局指令放入持久前缀，把多轮交互放入 episodic memory；检索时按角色决定保留原文、压缩表示或省略。

```mermaid
flowchart LR
  I[输入与当前状态] --> M[rea 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Role-aware Heuristic Episodic Attention for Conversational LLMs 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2610.00958v1/framework_time_1.png)

> **原论文 Figure 2（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2610.00958)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$C=I_{persistent}\oplus TopK(E, relevance)$。

### 论文离线与线上效果

Long-MT-Bench+ judge 6.32→7.36，平均延迟降低 2.91×。

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。

## 复现边界

执行角色分离与 episodic top-k；不调用压缩 LLM。
