# MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2508.20400](https://arxiv.org/abs/2508.20400) |
| 公司/机构 | Kuaishou Technology |
| 首次公开日期 | 2025-08-28（arXiv v1） |
| 原文开源代码 | 否：论文未提供官方/作者代码（核查日期：2026-08-09） |
| Adapter | `mpformer` |
| 本地复现代码 | [`src/auto_research/reproductions/mpformer/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/mpformer/) |

## 原始论文总结

### 背景与主要改动

以 objective token 驱动同一序列检索器完成多种行为目标，并按任务难度动态分配容量和候选配额。

```mermaid
flowchart LR
 A["公开输入 / 历史"] --> B["mpformer 核心路径"]
 B --> C["论文特有状态或目标"]
 C --> D["同预算评测"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever 原论文 Figure 1](assets/paper-figure-01.png)](https://ar5iv.labs.arxiv.org/html/2508.20400/assets/mpformer_model1_update.png)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2508.20400)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
z_m=F([e_m;h]),\quad\mathcal L=\sum_m q_m(h)\mathcal L_m,\quad\sum_mq_m=1.
$$

### 论文离线与线上效果

快手 Watch Time +0.426%；训练资源 -60%，serving 资源 -66.7%。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer，实验组只加入 `mpformer` 核心机制；相对 NDCG@10 -7.15%。

MovieLens-100K、260 users / 420 items、seed 42：NDCG@10 0.0354 → **0.0329（-7.15%）**。基线是共享 transition + content scorer；实验组只加入论文核心路径。

```bash
auto-research reproduce --paper mpformer --dataset-dir data --seed 42
auto-research evolve --model rankmixer --dataset movielens-100k --direction "组合 mpformer 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。 本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。
