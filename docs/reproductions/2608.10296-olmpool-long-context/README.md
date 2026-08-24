# Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension

> **复现级别：核心机制 mini-suite。** 本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2608.10296](https://arxiv.org/abs/2608.10296) |
| 公司/机构 | Ai2 |
| 第一作者 | Amanda Bertsch |
| 首次公开日期 | 2026-08-10（arXiv v1） |
| 原文开源代码 | 是：[olmpool](https://github.com/allenai/olmpool/) |
| Adapter | `olmpool-long-context` |
| 本地复现代码 | [`src/auto_research/reproductions/olmpool_long_context/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/olmpool_long_context/) |

## 原始论文总结

### 背景与主要改动

以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。

```mermaid
flowchart LR
  X[固定公开 mini-suite] --> B[recent-window 对照]
  X --> M[olmpool-long-context 核心机制]
  B --> E[同样本评测]
  M --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2608.10296#page=2)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2608.10296)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\Delta_{LC}=f(N,G,L,S)-f(N_0,G_0,L_0,S_0)
$$

### 论文离线与线上效果

三个以上不利选择组合可令长上下文下游表现下降至 47%；公开 26 个 OlmPool 模型。 这是原文口径；若原文没有工业 A/B，本页不会把本地结果写成线上收益。

## 本地复现

> **本地对照口径**：基线为同样本 `recent-window attention`，实验组为 `olmpool-long-context`；单 seed 变化为 `+92.19%` 个百分点。

同一 seed、同一 64 条样本上，`recent-window attention` baseline accuracy 为 `0.0781`，`olmpool-long-context` 为 `1.0000`，绝对变化 `+92.19` 个百分点。单篇原始指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)，批次索引见 [`../../experiments/historical-b07-b11-seed42.json`](../../experiments/historical-b07-b11-seed42.json)。

```bash
auto-research reproduce --paper olmpool-long-context --seed 42
```

## 复现边界

本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。
