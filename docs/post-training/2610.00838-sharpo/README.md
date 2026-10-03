# SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning

> **复现级别：L1 核心机制诊断。** 执行 segment credit；未读取 gold plan，也未训练 7B Agent。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1](https://arxiv.org/abs/2610.00838) |
| 公司/机构 | Georgia Institute of Technology（按第一作者署名单位） |
| 首次公开日期 | 2026-09-30（arXiv v1） |
| 原文开源代码 | 否：截至 2026-10-03 未找到原作者公开实现 |
| Adapter | `sharpo` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20261003.py`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/post_training/latest_20261003.py) |

## 原始论文总结

### 背景与主要改动

用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。

```mermaid
flowchart LR
  I[输入与当前状态] --> M[sharpo 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2610.00838v1/figure2_numbered.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2610.00838)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$A_{seg}=A\cdot2\sigma(\overline{\log p_T-\log p_S})$。

### 论文离线与线上效果

Qwen2.5-7B-Instruct 在 ALFWorld/WebShop 优于 GRPO、SDAR、RLSD、StepOPSD。

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。

## 复现边界

执行 segment credit；未读取 gold plan，也未训练 7B Agent。
