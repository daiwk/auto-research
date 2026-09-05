# SID-Coord：语义 ID 协同排序

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2604.10471](https://arxiv.org/abs/2604.10471) |
| 公司/机构 | Kuaishou Technology（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-04-12（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-05） |
| Adapter | `sid-coord` |
| 本地复现代码 | [`src/auto_research/reproductions/sid_coord/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/sid_coord/) |

## 原始论文总结

### 背景与主要改动

SID-Coord 不把语义信号仅作为普通稠密特征，而是构造多层离散 SID；再通过层级融合、目标感知 HID–SID 门控和历史兴趣对齐，在头部物品记忆与长尾泛化之间逐样本协调。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["sid-coord 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![SID-Coord：语义 ID 协同排序 原论文 Figure 3](assets/paper-figure-01.png)](https://arxiv.org/html/2604.10471v1/fig3.png)

> **原论文 Figure 3（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2604.10471)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
s_i=(1-g_i)s_{HID,i}+g_i\sum_l\alpha_l s_{SID_i^l}+\lambda\,\operatorname{Align}(u,i).
$$

### 论文离线与线上效果

- 短视频搜索线上 A/B：长播率 +0.664%，播放时长 +0.369%。
- 上述数字只复述论文证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.04970`，相对变化 **-7.97%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子的完整结果、均值、标准差与 95% CI 见：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper sid-coord --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
