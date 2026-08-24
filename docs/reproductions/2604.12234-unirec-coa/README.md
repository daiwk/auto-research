# UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2604.12234](https://arxiv.org/abs/2604.12234) |
| 公司/机构 | Authors did not disclose affiliation / large-scale e-commerce platform |
| 首次公开日期 | 2026-04-14（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `unirec-coa` |
| 本地复现代码 | [`src/auto_research/reproductions/unirec_coa/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/unirec_coa/) |

## 原始论文总结

### 背景与主要改动

在 SID 前生成品类、卖家和品牌等属性链，用容量受限量化抑制热点 token 塌缩，并以任务上下文稳定多场景生成。

```mermaid
flowchart LR
 A["Chain-of-Attribute"] --> B["容量约束 SID"] --> C["RFT+DPO 解码"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2604.12234v4/Unirec.png)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2604.12234)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
p(a,s|u)=p(a|u)\prod_l p(s_l|a,s_{<l},u)
$$

### 论文离线与线上效果

原文线上证据：**GMV +5.60%**（20% user traffic per bucket，Section 4.2 / Table 5）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `unirec-coa` 核心机制，相对 NDCG@10 -4.93%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0513（-4.93%）**，Hit@10 0.1091 → 0.0818。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper unirec-coa --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
