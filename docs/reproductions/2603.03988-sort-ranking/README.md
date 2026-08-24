# SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2603.03988](https://arxiv.org/abs/2603.03988) |
| 公司/机构 | Alibaba International Digital Commerce |
| 首次公开日期 | 2026-03-04（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `sort-ranking` |
| 本地复现代码 | [`src/auto_research/reproductions/sort_ranking/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/sort_ranking/) |

## 原始论文总结

### 背景与主要改动

系统重做特征 token 化、注意力和 FFN，并以面向工业硬件的结构压缩长序列，使单一 Transformer 替代传统 DLRM。

```mermaid
flowchart LR
 A["工业特征 Tokens"] --> B["优化 Attention/FFN"] --> C["多场景排序"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2603.03988v2/sort_arch.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2603.03988)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
H'=H+\operatorname{MHA}(H),\quad H''=H'+\operatorname{FFN}(H')
$$

### 论文离线与线上效果

原文线上证据：**orders +6.35%**（three production scenarios，Section 4.7 / Table 5）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `sort-ranking` 核心机制，相对 NDCG@10 -13.11%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0469（-13.11%）**，Hit@10 0.1091 → 0.0909。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper sort-ranking --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
