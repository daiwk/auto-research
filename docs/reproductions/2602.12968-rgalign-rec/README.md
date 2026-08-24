# RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2602.12968](https://arxiv.org/abs/2602.12968) |
| 公司/机构 | Forth AI / Shopee / Singapore University of Technology and Design |
| 首次公开日期 | 2026-02-13（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `rgalign-rec` |
| 本地复现代码 | [`src/auto_research/reproductions/rgalign_rec/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/rgalign_rec/) |

## 原始论文总结

### 背景与主要改动

先让 LLM 从上下文生成潜在 query，再用真实排序模型的 item 偏好构建正负 query，通过 RG-SFT 与 DPO 对齐 top-rank 意图。

```mermaid
flowchart LR
 A["上下文→潜在 Query"] --> B["Ranking Guide"] --> C["RG-SFT+DPO"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems 原论文 Figure 2](assets/paper-figure-01.png)](https://ar5iv.labs.arxiv.org/html/2602.12968/assets/graph/RGAlign-Rec-Solution.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2602.12968)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
L_{DPO}=-\log\sigma(\beta[\log\pi(q^w)-\log\pi(q^l)])
$$

### 论文离线与线上效果

原文线上证据：**CTR@3 incremental over QE-Rec +0.13%**（large-scale online A/B，Section 5.4 / Table 5）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `rgalign-rec` 核心机制，相对 NDCG@10 -14.03%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0464（-14.03%）**，Hit@10 0.1091 → 0.0727。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper rgalign-rec --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
