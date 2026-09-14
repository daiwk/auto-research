# SenseNova-U1.5: Towards Native Unified Visual Intelligence

> **复现级别：L1 核心机制诊断。** 本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [SenseNova-U1.5: Towards Native Unified Visual Intelligence](https://arxiv.org/abs/2609.11929) |
| 公司/机构 | SenseTime Research（按第一作者署名单位） |
| 首次公开日期 | 2026-09-10 |
| 原文开源代码 | 是：[https://github.com/OpenSenseNova/SenseNova-U1](https://github.com/OpenSenseNova/SenseNova-U1) |
| Adapter / 方法 | `sensenova-u1-5` |
| 本地复现代码 | [`src/auto_research/foundation_latest_20260914.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/foundation_latest_20260914.py) |

## 原始论文总结

### 背景与主要改动

用空间 patch reconstruction 摆脱 tokenizer/VAE，并以多专家 OPD 统一视觉理解与生成后训练。

```mermaid
flowchart LR
  I[输入与公开状态] --> M[sensenova-u1-5 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![SenseNova-U1.5: Towards Native Unified Visual Intelligence 原论文 Figure 3](assets/paper-figure-01.png)](https://arxiv.org/html/2609.11929v1/assets/u1.5_arch.png)

> **原论文 Figure 3（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.11929)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式或操作

本地代码把论文决定性操作实现为确定性的 reference kernel，并显式输出门控、选择、投影、图边或状态更新统计；测试覆盖公式不变量和边界条件。

### 论文离线与线上效果

论文报告统一 8B-MoT 模型在理解和生成任务上的综合结果。 这些数字来自原论文，不与本地缩小实验直接比较；论文未报告线上 A/B 时不推断线上收益。

## 本地复现

三种子指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。

### 复现边界

本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。
