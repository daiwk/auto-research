# DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2602.09744](https://arxiv.org/abs/2602.09744) |
| 公司/机构 | Tencent |
| 首次公开日期 | 2026-02-10（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `diffureason` |
| 本地复现代码 | [`src/auto_research/reproductions/diffureason/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/diffureason/) |

## 原始论文总结

### 背景与主要改动

Thinking Tokens 形成连续潜在意图，扩散去噪逐步修正冲突兴趣，GRPO 再把连续生成与离散排序奖励端到端对齐。

```mermaid
flowchart LR
 A["Thinking Tokens"] --> B["Diffusion Refinement"] --> C["GRPO 排序"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2602.09744v2/diffureason.png)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2602.09744)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
z_{t-1}=\mu_\theta(z_t,h)+\sigma_t\epsilon,\quad J=\mathbb E[A\log\pi_\theta]
$$

### 论文离线与线上效果

原文线上证据：**ad consumption +1.15%**（20% traffic, five days，Section 4.7）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `diffureason` 核心机制，相对 NDCG@10 -6.50%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0505（-6.50%）**，Hit@10 0.1091 → 0.1045。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper diffureason --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
