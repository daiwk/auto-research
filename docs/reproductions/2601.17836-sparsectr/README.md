# SparseCTR：面向长期行为的演化稀疏注意力

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2601.17836](https://arxiv.org/abs/2601.17836) |
| 公司/机构 | Institute of Software, Chinese Academy of Sciences（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-01-25（arXiv v1） |
| 原文开源代码 | 是：[https://github.com/laiweijiang/SparseCTR](https://github.com/laiweijiang/SparseCTR) |
| Adapter | `sparsectr` |
| 本地复现代码 | [`src/auto_research/reproductions/sparsectr/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/sparsectr/) |

## 原始论文总结

### 背景与主要改动

TimeChunking 按个体行为时间间隔自适应分块；EvoAttention 并联全局 chunk、兴趣转移和局部窗口三路注意力，RelTemporal 再注入时间间隔、小时和周末相对偏置。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["sparsectr 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![SparseCTR：面向长期行为的演化稀疏注意力 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2601.17836v1/model.png)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2601.17836)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
H=\alpha_gA_{global}+\alpha_tA_{transition}+\alpha_lA_{local},\qquad A=\mathrm{softmax}(QK^\top/\sqrt d+B_{time})V.
$$

### 论文离线与线上效果

- 论文在 1% 流量、7 天线上实验中报告 CTR +1.72%、CPM +1.41%，序列长度从 128 扩展到 1024。
- 上述数字只复述论文证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.05519`，相对变化 **+2.19%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子的完整结果、均值、标准差与 95% CI 见：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper sparsectr --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
