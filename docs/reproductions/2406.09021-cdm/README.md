# Contextual Distillation Model for Diversified Recommendation

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2406.09021](https://arxiv.org/abs/2406.09021) |
| 公司/机构 | Kuaishou Technology |
| 首次公开日期 | 2024-06-13（arXiv v1） |
| 原文开源代码 | 否：未发现/未发布原作者官方代码仓库（核查日期：2026-08-08） |
| Adapter | `cdm` |
| 本地复现代码 | [`src/auto_research/reproductions/cdm/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/cdm/) |

## 原始论文总结

### 背景与主要改动

先用可控 MMR 教师产生兼顾相关性与多样性的列表，再把上下文边际收益蒸馏到可低延迟服务的学生。

```mermaid
flowchart LR
 A["公开输入 / 历史"] --> B["cdm 核心路径"]
 B --> C["论文特有状态或目标"]
 C --> D["同预算评测"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Contextual Distillation Model for Diversified Recommendation 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2406.09021#page=1)

> **原论文 Figure 1（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2406.09021)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
y_t=\arg\max_i[s(i)-\lambda\max_{j<t}\operatorname{sim}(i,j)],\quad\mathcal L=\|f_\theta-y_{teacher}\|^2.
$$

### 论文离线与线上效果

快手主端 Watch Time +0.406%，聚类系数 -0.957%。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer，实验组只加入 `cdm` 核心机制；相对 NDCG@10 +1.25%。

MovieLens-100K、260 users / 420 items、seed 42：NDCG@10 0.0354 → **0.0358（+1.25%）**。基线是共享 transition + content scorer；实验组只加入论文核心路径。

```bash
auto-research reproduce --paper cdm --dataset-dir data --seed 42
auto-research evolve --model rankmixer --dataset movielens-100k --direction "组合 cdm 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。 本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。
