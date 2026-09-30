# Telescopic Language Models

> **复现级别：L1 核心机制诊断。** 验证随机深度和 full anchor 的梯度路径；未做 20B-token 预训练。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Telescopic Language Models](https://arxiv.org/abs/2609.35769) |
| 公司/机构 | University of Cambridge（按第一作者署名单位） |
| 首次公开日期 | 2026-09-28（arXiv v1） |
| 原文开源代码 | 否：截至 2026-09-30 未找到原作者公开仓库 |
| Adapter / 方法 | `telescopic-lm` |
| 本地复现代码 | [`src/auto_research/foundation_latest_20260930_closure.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/foundation_latest_20260930_closure.py) |

## 原始论文总结

### 背景与主要改动

每步随机抽一个网络深度前缀做 next-token 监督，同时保留全深度 anchor，使同一 checkpoint 的每个深度都成为可用语言模型。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[telescopic-lm 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/更新状态]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Telescopic Language Models 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2609.35769#page=2)

> **原论文 Figure 1（关键图）**：展示原论文的训练流程与关键优化环节。图片来自[原论文](https://arxiv.org/abs/2609.35769)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、掩码、递归、信用权重或晋级条件；测试同时检查梯度隔离、类型边界和确定性。

### 论文离线与线上效果

论文中的 benchmark、速度或训练曲线属于原文结果。本地三种子 mini-suite 仅检验机制和不变量，不与论文规模结果横比，也不外推线上收益。

## 本地复现

三种子诊断见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。其中 `diagnostic_only=true`，不能进入正式能力排名。

## 复现边界

验证随机深度和 full anchor 的梯度路径；未做 20B-token 预训练。
