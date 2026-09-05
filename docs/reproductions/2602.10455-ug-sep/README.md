# UG-Sep：用户计算只做一次

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2602.10455](https://arxiv.org/abs/2602.10455) |
| 公司/机构 | ByteDance AML（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-02-11（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-05） |
| Adapter | `ug-sep` |
| 本地复现代码 | [`src/auto_research/reproductions/ug_sep/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/ug_sep/) |

## 原始论文总结

### 背景与主要改动

通过注意力/TokenMixer mask 阻断候选向用户 token 的反向信息流，使用户侧表示能在同一请求的多个候选间复用；Information Compensation 额外恢复被 mask 抑制的用户—候选交互。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["ug-sep 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![UG-Sep：用户计算只做一次 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2602.10455v2/tokenmixer-0520.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2602.10455)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
H_u'=\mathrm{Mixer}(H_u;M_{UG}),\qquad s(u,i)=f(H_u',e_i)+g(H_u',e_i).
$$

### 论文离线与线上效果

- 论文报告工业场景推理延迟最高降低 20%，并以 W8A16 缓解复用后的内存瓶颈。
- 上述数字只复述论文证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.04934`，相对变化 **-8.65%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子的完整结果、均值、标准差与 95% CI 见：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper ug-sep --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
