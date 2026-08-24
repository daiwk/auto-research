# CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2602.11410](https://arxiv.org/abs/2602.11410) |
| 公司/机构 | LinkedIn |
| 首次公开日期 | 2026-02-11（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `cadet` |
| 本地复现代码 | [`src/auto_research/reproductions/cadet/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/cadet/) |

## 原始论文总结

### 背景与主要改动

Decoder-only Transformer 先编码可缓存历史，候选打分后再注入 post-scoring context，避免训练与服务错位并统一广告 CTR 模型。

```mermaid
flowchart LR
 A["历史+候选序列"] --> B["CADET Block"] --> C["Context-conditioned CTR"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2602.11410v2/figures/paper_self_gating.png)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2602.11410)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
h_i'=h_i+\operatorname{Attn}(q(c),K(h_{\le i}),V(h_{\le i}))
$$

### 论文离线与线上效果

原文线上证据：**CTR +11.04%**（large-scale online A/B，Section 5.3 / Table 3）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `cadet` 核心机制，相对 NDCG@10 -6.20%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0507（-6.20%）**，Hit@10 0.1091 → 0.1000。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper cadet --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
