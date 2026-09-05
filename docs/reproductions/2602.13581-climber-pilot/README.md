# Climber-Pilot：非短视指令跟随召回

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2602.13581](https://arxiv.org/abs/2602.13581) |
| 公司/机构 | NetEase Cloud Music（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-02-14（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-05） |
| Adapter | `climber-pilot` |
| 本地复现代码 | [`src/auto_research/reproductions/climber_pilot/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/climber_pilot/) |

## 原始论文总结

### 背景与主要改动

Climber-Pilot 用时间感知多物品预测把长周期、多物品消费前瞻蒸馏进单步生成模型；条件引导稀疏注意力在 attention 内注入类目和业务约束，无需额外过滤或多步推理。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["climber-pilot 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![Climber-Pilot：非短视指令跟随召回 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2602.13581v2/Overall_Framework_fix.png)

> **原论文 Figure 1（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2602.13581)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\mathcal L_{TAMIP}=-\sum_{k=1}^{K}w_k\log p(i_{t+k}|H_t),\qquad A'=A\odot M_c.
$$

### 论文离线与线上效果

- 网易云音乐线上 A/B 的核心业务指标提升 4.24%。
- 上述数字只复述论文证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.09251`，相对变化 **+71.29%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子的完整结果、均值、标准差与 95% CI 见：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper climber-pilot --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
