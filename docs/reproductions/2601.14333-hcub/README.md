# HCUB：层级上下文增量 Bandit

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2601.14333](https://arxiv.org/abs/2601.14333) |
| 公司/机构 | Dream11（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-01-20（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-05） |
| Adapter | `hcub` |
| 本地复现代码 | [`src/auto_research/reproductions/hcub/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/hcub/) |

## 原始论文总结

### 背景与主要改动

在用户与系统上下文树上动态选择粒度，并让父节点奖励向稀疏子节点继承以改善冷启动；策略直接估计动作的增量收益，而不是只拟合观察到的绝对点击。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["hcub 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![HCUB：层级上下文增量 Bandit 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2601.14333v1/g290.png)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2601.14333)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
a_t=\arg\max_a\hat\tau(a\mid c_t)+\beta U(a,c_t),\qquad R(c)=\eta R_{local}+(1-\eta)R_{parent}.
$$

### 论文离线与线上效果

- Dream11 线上报告收入 +0.51%、互动 +0.42%，离线 regret 降低约 4%–5%。
- 上述数字只复述论文证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.04886`，相对变化 **-9.53%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子的完整结果、均值、标准差与 95% CI 见：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper hcub --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
