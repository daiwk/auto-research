# LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation

> **复现级别：L1 核心机制诊断。** 本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation](https://arxiv.org/abs/2609.11739) |
| 公司/机构 | University of Washington（按第一作者署名单位） |
| 首次公开日期 | 2026-09-10 |
| 原文开源代码 | 否：未找到作者公开仓库（核查日期：2026-09-14） |
| Adapter / 方法 | `locus` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20260914.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/post_training/latest_20260914.py) |

## 原始论文总结

### 背景与主要改动

学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。

```mermaid
flowchart LR
  I[输入与公开状态] --> M[locus 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2609.11739#page=3)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.11739)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式或操作

本地代码把论文决定性操作实现为确定性的 reference kernel，并显式输出门控、选择、投影、图边或状态更新统计；测试覆盖公式不变量和边界条件。

### 论文离线与线上效果

Pythia 输出最高缩短 39.84%，Qwen 缩短 14.87%–17.58%，训练参数约 0.24%–0.28%。 这些数字来自原论文，不与本地缩小实验直接比较；论文未报告线上 A/B 时不推断线上收益。

## 本地复现

三种子指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。

### 复现边界

本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。
