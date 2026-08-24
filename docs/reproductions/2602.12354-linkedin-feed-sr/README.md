# An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2602.12354](https://arxiv.org/abs/2602.12354) |
| 公司/机构 | LinkedIn |
| 首次公开日期 | 2026-02-12（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `linkedin-feed-sr` |
| 本地复现代码 | [`src/auto_research/reproductions/linkedin_feed_sr/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/linkedin_feed_sr/) |

## 原始论文总结

### 背景与主要改动

将 Feed 候选、交互历史和上下文统一成超长序列，采用 HSTU 式目标注意力、负样本自由评估及增量服务优化。

```mermaid
flowchart LR
 A["长 Feed 历史"] --> B["Sequential Recommender"] --> C["全候选排序"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking 原论文 Figure 3](assets/paper-figure-01.png)](https://arxiv.org/html/2602.12354v2/pics/system_diagram.png)

> **原论文 Figure 3（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2602.12354)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
h_t=\operatorname{HSTU}(e_{1:t}),\quad s_i=\langle h_t,e_i\rangle
$$

### 论文离线与线上效果

原文线上证据：**time spent +2.10%**（production A/B，Section 7 / Table 5）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `linkedin-feed-sr` 核心机制，相对 NDCG@10 -0.12%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0539（-0.12%）**，Hit@10 0.1091 → 0.1091。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper linkedin-feed-sr --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
