# RoleGen：休眠用户反事实角色推理

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2602.13134](https://arxiv.org/abs/2602.13134) |
| 公司/机构 | Beihang University（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-02-13（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-05） |
| Adapter | `rolegen` |
| 本地复现代码 | [`src/auto_research/reproductions/rolegen/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/rolegen/) |

## 原始论文总结

### 背景与主要改动

RoleGen 让 LLM Reasoner 判断物品在转化轨迹中的功能角色，并通过反事实路径估计其工具性作用；候选再进入 SID 生成骨干，通过推理—执行—反馈—反思闭环迭代，降低休眠用户兴趣坍缩。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["rolegen 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![RoleGen：休眠用户反事实角色推理 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2602.13134v1/model.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2602.13134)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\Delta_i=\mathbb E[Y|do(i)]-\mathbb E[Y|do(\neg i)],\qquad s_i=s_{backbone,i}+\lambda\Delta_i.
$$

### 论文离线与线上效果

- Kuaishou 电商离线 Recall@1 +6.2%，线上订单量 +7.3%。
- 上述数字只复述论文证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.05605`，相对变化 **+3.78%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子的完整结果、均值、标准差与 95% CI 见：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper rolegen --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
