# LLM-Based Re-Ranking for Real Estate Search

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2607.14835](https://arxiv.org/abs/2607.14835) |
| 公司/机构 | QuintoAndar |
| 首次公开日期 | 2026-07-16（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `real-estate-rerank` |
| 本地复现代码 | [`src/auto_research/reproductions/real_estate_rerank/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/real_estate_rerank/) |

## 原始论文总结

### 背景与主要改动

把对话需求、结构化房源属性、文本描述和候选集合统计交给 LLM 重排，用候选间比较补足向量召回的局部相关性。

```mermaid
flowchart LR
 A["对话与用户画像"] --> B["候选集合 LLM 重排"] --> C["房源顺序"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![LLM-Based Re-Ranking for Real Estate Search 原论文 Figure 4](assets/paper-figure-01.png)](https://arxiv.org/html/2607.14835v2/figures/dataset_construction.png)

> **原论文 Figure 4（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2607.14835)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
s_i=f_\theta(q,p_u,x_i,\operatorname{Agg}(X))
$$

### 论文离线与线上效果

原文的主要线上证据为 **CTR +5.30%**（production A/B）。论文离线表与线上指标使用私有或论文指定口径，不能与下面的 MovieLens 数字直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在相同用户、物品、全库候选和 seed 上只加入 `real-estate-rerank` 核心机制，相对 NDCG@10 -8.21%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0496（-8.21%）**，Hit@10 0.1091 → 0.1000。验证集只用于选择机制混合权重，测试集没有参与调参。

```bash
auto-research reproduce --paper real-estate-rerank --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。 本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 `omitted_core_components`，本地相对变化不得与原文 A/B 提升混写。
