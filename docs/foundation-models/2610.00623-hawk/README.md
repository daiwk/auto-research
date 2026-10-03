# HAWK: Rethinking Multimodal Drafting for Speculative Decoding

> **复现级别：L1 核心机制诊断。** 执行层混合与 shifted target 隔离；未实现专用解码 kernel。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1](https://arxiv.org/abs/2610.00623) |
| 公司/机构 | 原文首页未列第一作者机构（按第一作者署名单位） |
| 首次公开日期 | 2026-09-30（arXiv v1） |
| 原文开源代码 | 否：截至 2026-10-03 未找到原作者公开实现 |
| Adapter | `hawk` |
| 本地复现代码 | [`src/auto_research/foundation_latest_20261003.py`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/foundation_latest_20261003.py) |

## 原始论文总结

### 背景与主要改动

从 target 多层隐藏状态学习混合，给浅层 drafter 提供压缩视觉表示，并用 drafter 自己提议后的 shifted trajectory 训练。

```mermaid
flowchart LR
  I[输入与当前状态] --> M[hawk 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![HAWK: Rethinking Multimodal Drafting for Speculative Decoding 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2610.00623v1/HAWK_framework.png)

> **原论文 Figure 1（关键图）**：展示原论文的训练流程与关键优化环节。图片来自[原论文](https://arxiv.org/abs/2610.00623)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$h_d=\sum_l softmax(a)_l h_l$，监督来自 shift 后 target 分布。

### 论文离线与线上效果

论文报告 LVLM 投机解码接受率和无损速度提升。

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。

## 复现边界

执行层混合与 shifted target 隔离；未实现专用解码 kernel。
