# HARNESS-LM：强文档塔与轻量查询塔的三阶段检索训练

> **Fidelity: 核心机制复现**。Teacher、L2 embedding alignment、冻结 teacher document index 的 contrastive refinement 三阶段均实际执行。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2605.23572](https://arxiv.org/abs/2605.23572) |
| 公司/机构 | Microsoft AI / Bing Ads |
| 首次公开日期 | 2026-05-22（arXiv v1） |
| 原文开源代码 | 否：未找到作者公开代码（核查日期：2026-07-16） |
| Adapter | `harness-lm` |
| 本地复现代码 | [`src/auto_research/reproductions/harness_lm/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/harness_lm/) |

## 原始论文总结

### 背景与主要改动

Sponsored Search 可以离线使用昂贵文档编码器，却要求在线 query encoder 足够小。HARNESS-LM 先训练强 teacher，再让小 query encoder 直接对齐 teacher query 空间，最后冻结 teacher 文档塔做监督对比精修，避免重建索引。

```mermaid
flowchart LR
  A[大 query/doc teacher] --> B[冻结 teacher 文档索引]
  A --> C[L2 对齐小 query encoder]
  C --> D[监督对比精修]
  B --> E[非对称在线检索]
  D --> E
```

### 核心公式

$$
s(q,d)=\langle f_Q(q),f_D(d)\rangle,\qquad \mathcal L_{align}=\sum_i\|f_Q^S(q_i)-f_Q^T(q_i)\|_2^2.
$$

精修阶段冻结 $f_D^T$，只更新 $f_Q^S$ 的 InfoNCE。

### 论文离线与线上效果

Bing Ads 上线后 Revenue `+1.0%`、Impressions `+0.6%`、Clicks `+0.4%`，服务约 1.9 亿广告。

## 本地复现

> **本地对照口径**：基线是小型对称内容 retriever；实验组 HARNESS-LM 使用强协同文档空间、L2 对齐与对比精修，相对基线 Hit@10 **`-23.08%`**、NDCG@10 **`-28.05%`**。

alignment MSE `0.02375→0.02115`、contrastive loss `7.1900→5.8921`，说明三阶段优化正常收敛，但 test retrieval 未迁移。稳定指标见 [`metrics/movielens-100k-seed42.json`](metrics/movielens-100k-seed42.json)。

```bash
auto-research reproduce --paper harness-lm --seed 42
```

## 复现边界

协同 SVD+内容代理 Qwen3-Embedding teacher；未复刻 4B/0.6B 规模、GPT expansion 与 CPU pruning frontier。
