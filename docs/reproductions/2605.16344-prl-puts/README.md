# A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2605.16344](https://arxiv.org/abs/2605.16344) |
| 公司/机构 | Pinterest |
| 首次公开日期 | 2026-05-08（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `prl-puts` |
| 本地复现代码 | [`src/auto_research/reproductions/prl_puts/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/prl_puts/) |

## 原始论文总结

### 背景与主要改动

双头 Q 网络分别估计 Repin 与 P2P utility，再通过 Pareto sweeping 离线筛选不劣策略；线上仅切换可治理的权重策略，不更换模型。

```mermaid
flowchart LR
 A["双目标 Q 网络"] --> B["Pareto 策略扫描"] --> C["用户分群策略"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems 原论文 Figure 3](assets/paper-figure-01.png)](https://arxiv.org/html/2605.16344v1/content/resources/production_structure.png)

> **原论文 Figure 3（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2605.16344)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
a^*=\arg\max_a[\alpha Q_{repin}(s,a)+(1-\alpha)Q_{p2p}(s,a)]
$$

### 论文离线与线上效果

原文线上证据：**P2P impressions +0.30%**（1% per arm, two weeks，Section 6.4 / Table 1）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `prl-puts` 核心机制，相对 NDCG@10 +39.64%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0754（+39.64%）**，Hit@10 0.1091 → 0.1318。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper prl-puts --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
