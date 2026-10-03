# MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs

> **复现级别：L1 核心机制诊断。** 执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1](https://arxiv.org/abs/2610.01434) |
| 公司/机构 | 原文首页未列第一作者机构（按第一作者署名单位） |
| 首次公开日期 | 2026-10-01（arXiv v1） |
| 原文开源代码 | 否：截至 2026-10-03 未找到原作者公开实现 |
| Adapter | `mwop` |
| 本地复现代码 | [`src/auto_research/foundation_latest_20261003.py`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/foundation_latest_20261003.py) |

## 原始论文总结

### 背景与主要改动

在同一注意力头内分别剪 V2V/T2V/T2T 路径，并为视觉、文本执行选择不同 FFN 通道；注意力剪枝后重新估计 FFN 重要性。

```mermaid
flowchart LR
  I[输入与当前状态] --> M[mwop 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2610.01434v1/MWOP-methods.png)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2610.01434)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$I(w)pprox|w\partial L/\partial w|$，不同模态路径独立 top-k。

### 论文离线与线上效果

论文在多种 MLLM 上报告较高压缩率下的精度保持与吞吐收益。

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。

## 复现边界

执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。
