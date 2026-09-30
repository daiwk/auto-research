# Fractional State Space Transition for Long Sequence Modeling

> **复现级别：L1 核心机制诊断。** 执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Fractional State Space Transition for Long Sequence Modeling](https://arxiv.org/abs/2609.36314) |
| 公司/机构 | Huawei Noah's Ark Lab, Montreal Research Center（按第一作者署名单位） |
| 首次公开日期 | 2026-09-28（arXiv v1） |
| 原文开源代码 | 是：[https://github.com/anasiri/frac-ssm](https://github.com/anasiri/frac-ssm) |
| Adapter / 方法 | `frac-ssm` |
| 本地复现代码 | [`src/auto_research/foundation_latest_20260930_closure.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/foundation_latest_20260930_closure.py) |

## 原始论文总结

### 背景与主要改动

以对数间隔的有限指数模态逼近分数阶动力学的幂律记忆，在有界递归状态下兼顾长尾记忆和并行训练。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[frac-ssm 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/更新状态]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Fractional State Space Transition for Long Sequence Modeling 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2609.36314#page=6)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.36314)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、掩码、递归、信用权重或晋级条件；测试同时检查梯度隔离、类型边界和确定性。

### 论文离线与线上效果

论文中的 benchmark、速度或训练曲线属于原文结果。本地三种子 mini-suite 仅检验机制和不变量，不与论文规模结果横比，也不外推线上收益。

## 本地复现

三种子诊断见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。其中 `diagnostic_only=true`，不能进入正式能力排名。

## 复现边界

执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。
