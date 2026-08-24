# Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry

> **复现级别：核心机制 mini-suite。** 本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2608.06849](https://arxiv.org/abs/2608.06849) |
| 公司/机构 | Institute of Computing Technology, Chinese Academy of Sciences |
| 第一作者 | Yehan Yang |
| 首次公开日期 | 2026-08-07（arXiv v1） |
| 原文开源代码 | 否：截至 2026-08-24 未发现原作者公开代码 |
| Adapter | `autonomy-heads` |
| 本地复现代码 | [`src/auto_research/reproductions/autonomy_heads/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/autonomy_heads/) |

## 原始论文总结

### 背景与主要改动

直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。

```mermaid
flowchart LR
  X[固定公开 mini-suite] --> B[recent-window 对照]
  X --> M[autonomy-heads 核心机制]
  B --> E[同样本评测]
  M --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry 原论文 Figure 11](assets/paper-figure-01.png)](https://arxiv.org/html/2608.06849v1/H2Share.png)

> **原论文 Figure 11（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2608.06849)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
M_h=W_{K,h}^{\top}W_{Q,h},\quad r_{eff}(M_h)=\exp H(\sigma(M_h))
$$

### 论文离线与线上效果

50% 稀疏度平均保留 96.5% full-attention 表现；prefill/decode 时延最高下降 41.4%/66.0%。 这是原文口径；若原文没有工业 A/B，本页不会把本地结果写成线上收益。

## 本地复现

> **本地对照口径**：基线为同样本 `recent-window attention`，实验组为 `autonomy-heads`；单 seed 变化为 `+92.19%` 个百分点。

同一 seed、同一 64 条样本上，`recent-window attention` baseline accuracy 为 `0.0781`，`autonomy-heads` 为 `1.0000`，绝对变化 `+92.19` 个百分点。单篇原始指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)，批次索引见 [`../../experiments/historical-b07-b11-seed42.json`](../../experiments/historical-b07-b11-seed42.json)。

```bash
auto-research reproduce --paper autonomy-heads --seed 42
```

## 复现边界

本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。
