# TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2605.23702](https://arxiv.org/abs/2605.23702) |
| 公司/机构 | Tubi |
| 首次公开日期 | 2026-05-22（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `tubifm` |
| 本地复现代码 | [`src/auto_research/reproductions/tubifm/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/tubifm/) |

## 原始论文总结

### 背景与主要改动

以统一 user story 序列描述跨页面旅程，同一个生成式 foundation model 通过任务提示完成 item、carousel 与 search 三种排序。

```mermaid
flowchart LR
 A["跨表面 User Story"] --> B["统一生成模型"] --> C["三任务排序"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2605.23702#page=2)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2605.23702)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
s(i|h,\tau)=\log p_\theta([ITEM=i]|\operatorname{serialize}(h,\tau))
$$

### 论文离线与线上效果

原文的主要线上证据为 **total viewing time +3.90%**（production A/B; p<0.05）。论文离线表与线上指标使用私有或论文指定口径，不能与下面的 MovieLens 数字直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在相同用户、物品、全库候选和 seed 上只加入 `tubifm` 核心机制，相对 NDCG@10 +0.45%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0543（+0.45%）**，Hit@10 0.1091 → 0.1045。验证集只用于选择机制混合权重，测试集没有参与调参。

```bash
auto-research reproduce --paper tubifm --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。 本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 `omitted_core_components`，本地相对变化不得与原文 A/B 提升混写。
