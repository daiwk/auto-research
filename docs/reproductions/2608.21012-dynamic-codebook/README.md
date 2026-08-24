# From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2608.21012](https://arxiv.org/abs/2608.21012) |
| 公司/机构 | Kuaishou Technology |
| 首次公开日期 | 2026-08-21（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `dynamic-codebook` |
| 本地复现代码 | [`src/auto_research/reproductions/dynamic_codebook/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/dynamic_codebook/) |

## 原始论文总结

### 背景与主要改动

把多级小语义码本压缩为动态更新的单级大码本，再保留独立碰撞码；既减少自回归步数，也用曝光加权更新抵抗码本漂移。

```mermaid
flowchart LR
 A["多级 SID"] --> B["动态大码本"] --> C["碰撞码与短解码"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2608.21012#page=7)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2608.21012)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
r_i=e_i-c_{s_i},\quad c_k\leftarrow(1-\eta)c_k+\eta\frac{\sum_i w_i e_i\mathbf1[s_i=k]}{\sum_i w_i\mathbf1[s_i=k]}
$$

### 论文离线与线上效果

原文的主要线上证据为 **primary consumption +0.79%**（2.5% traffic, 5 days）。论文离线表与线上指标使用私有或论文指定口径，不能与下面的 MovieLens 数字直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在相同用户、物品、全库候选和 seed 上只加入 `dynamic-codebook` 核心机制，相对 NDCG@10 -18.73%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0439（-18.73%）**，Hit@10 0.1091 → 0.0818。验证集只用于选择机制混合权重，测试集没有参与调参。

```bash
auto-research reproduce --paper dynamic-codebook --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。 本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 `omitted_core_components`，本地相对变化不得与原文 A/B 提升混写。
