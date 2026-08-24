# L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2605.26717](https://arxiv.org/abs/2605.26717) |
| 公司/机构 | NetEase Cloud Music |
| 首次公开日期 | 2026-05-26（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `l2rec` |
| 本地复现代码 | [`src/auto_research/reproductions/l2rec/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/l2rec/) |

## 原始论文总结

### 背景与主要改动

共享 LLM 中插入按用户路由的双视图 LoRA-MoE，分别适配语义视图和行为视图，再由自适应跨视图门控融合。

```mermaid
flowchart LR
 A["语义/行为双视图"] --> B["个性化 LoRA-MoE"] --> C["跨视图融合"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2605.26717v1/HARTforPDF.png)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2605.26717)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\Delta W_v(u)=\sum_{e\in TopK(g_v(u))}g_{v,e}(u)B_{v,e}A_{v,e}
$$

### 论文离线与线上效果

原文的主要线上证据为 **CTR +9.24%**（6% user traffic, one month; p<0.01）。论文离线表与线上指标使用私有或论文指定口径，不能与下面的 MovieLens 数字直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在相同用户、物品、全库候选和 seed 上只加入 `l2rec` 核心机制，相对 NDCG@10 -5.04%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0513（-5.04%）**，Hit@10 0.1091 → 0.1045。验证集只用于选择机制混合权重，测试集没有参与调参。

```bash
auto-research reproduce --paper l2rec --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。 本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 `omitted_core_components`，本地相对变化不得与原文 A/B 提升混写。
