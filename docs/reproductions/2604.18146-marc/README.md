# MARC：模块化表征压缩

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2604.18146](https://arxiv.org/abs/2604.18146) |
| 公司/机构 | Shanghai Jiao Tong University（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-04-20（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-05） |
| Adapter | `marc` |
| 本地复现代码 | [`src/auto_research/reproductions/marc/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/marc/) |

## 原始论文总结

### 背景与主要改动

论文发现 LLM 的中间层在推荐压缩后可能优于末层（MRA）。MARC 将压缩模块与任务适配模块显式拆开，并用信息约束解耦代理任务和推荐任务，保留任务相关信息的同时降低表征维度。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["marc 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![MARC：模块化表征压缩 原论文 Figure 5](assets/paper-figure-01.png)](https://arxiv.org/pdf/2604.18146#page=5)

> **原论文 Figure 5（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2604.18146)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
z=P_k\big(h_{mid}-\Pi_{nuisance}h_{mid}\big),\qquad s(i)=\langle z_u,z_i\rangle.
$$

### 论文离线与线上效果

- 商业搜索广告线上 A/B 的 eCPM 提升 2.82%。
- 上述数字只复述论文证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.04693`，相对变化 **-13.11%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子的完整结果、均值、标准差与 95% CI 见：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper marc --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
