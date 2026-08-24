# UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2603.24226](https://arxiv.org/abs/2603.24226) |
| 公司/机构 | Taobao & Tmall Group / Alibaba |
| 首次公开日期 | 2026-03-25（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `uniscale` |
| 本地复现代码 | [`src/auto_research/reproductions/uniscale/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/uniscale/) |

## 原始论文总结

### 背景与主要改动

ES³ 从曝光外全空间扩充数据，HHSFT 分层融合异构样本；数据规模和模型容量协同扩展，并配合低成本部署。

```mermaid
flowchart LR
 A["Entire-Space 数据"] --> B["HHSFT 分层融合"] --> C["搜索排序"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2603.24226v4/overview.png)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2603.24226)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
h^{l+1}=h^l+\sum_d g_d(h^l)\,FFN_d(h^l)
$$

### 论文离线与线上效果

原文线上证据：**GMV +2.04%**（5% traffic, ten days，Section 4.5）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `uniscale` 核心机制，相对 NDCG@10 -2.20%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0528（-2.20%）**，Hit@10 0.1091 → 0.1045。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper uniscale --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
