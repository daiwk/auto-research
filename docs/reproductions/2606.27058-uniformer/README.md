# UniFormer：工业推荐的统一模型中心扩展

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2606.27058](https://arxiv.org/abs/2606.27058) |
| 公司/机构 | Kuaishou（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-06-25（arXiv v1） |
| 原文开源代码 | 否：论文未提供官方/作者代码（核查日期：2026-09-02） |
| Adapter | `uniformer` |
| 本地复现代码 | [`src/auto_research/reproductions/uniformer/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/uniformer/) |

## 原始论文总结

### 背景与主要改动

把 item-independent/dependent 特征与不同任务拆成语义 token，通过统一交互模块共同扩展序列、特征和任务空间。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["uniformer 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["论文定义的直接基线"]
  C --> E["统一指标与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![UniFormer：工业推荐的统一模型中心扩展 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2606.27058v1/uniformer.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2606.27058)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
H'=\\operatorname{Attn}([T_{ind};T_{dep};T_{task}]),\\quad \\hat y_k=g_k(H'_{task,k}).
$$

### 论文离线与线上效果

- 快手主站与极速版 7 天 5% 流量，极速版停留时长 +0.260%、观看时长 +1.113%；用户物品解耦使 QPS +48%。
- 上述数字只复述论文线上证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一全目录协议下，基线 NDCG@10 为 `0.05401`，实验组 UniFormer 为 `0.04131`，相对变化 **-23.50%**。这是公开代理任务的负结果，生产线上 lift 的外推不适用。

三随机种子完整结果、均值、标准差与 95% CI：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper uniformer --dataset-dir data --seed 42
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。
