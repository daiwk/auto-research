# PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2605.21752](https://arxiv.org/abs/2605.21752) |
| 公司/机构 | TikTok |
| 首次公开日期 | 2026-05-20（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `pearl-percentile` |
| 本地复现代码 | [`src/auto_research/reproductions/pearl_percentile/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/pearl_percentile/) |

## 原始论文总结

### 背景与主要改动

用多次对比而不是单个偏置标签估计行为 percentile，并按价值加权、bootstrap 和长期共训练扩展到多个排序目标。

```mermaid
flowchart LR
 A["多样本对比"] --> B["无偏 Percentile"] --> C["多目标排序"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2605.21752#page=4)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2605.21752)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\hat p_i=\frac1N\sum_{j=1}^{N}\mathbf1[y_i>y_j],\quad Var(\hat p)=p(1-p)/N
$$

### 论文离线与线上效果

原文的主要线上证据为 **Watch Duration +2.10%**（week-long online A/B）。论文离线表与线上指标使用私有或论文指定口径，不能与下面的 MovieLens 数字直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在相同用户、物品、全库候选和 seed 上只加入 `pearl-percentile` 核心机制，相对 NDCG@10 -10.65%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0483（-10.65%）**，Hit@10 0.1091 → 0.1000。验证集只用于选择机制混合权重，测试集没有参与调参。

```bash
auto-research reproduce --paper pearl-percentile --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。 本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 `omitted_core_components`，本地相对变化不得与原文 A/B 提升混写。
