# Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2604.07420](https://arxiv.org/abs/2604.07420) |
| 公司/机构 | Kuaishou Technology |
| 首次公开日期 | 2026-04-08（arXiv v1） |
| 原文开源代码 | 否：未发现/未发布原作者官方代码仓库（核查日期：2026-08-08） |
| Adapter | `dual-rerank` |
| 本地复现代码 | [`src/auto_research/reproductions/dual_rerank/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/dual_rerank/) |

## 原始论文总结

### 背景与主要改动

AR 教师学习物品间顺序依赖，NAR 学生并行估计名次；效用蒸馏把效果与延迟共同写入训练目标。

```mermaid
flowchart LR
 A["公开输入 / 历史"] --> B["dual-rerank 核心路径"]
 B --> C["论文特有状态或目标"]
 C --> D["同预算评测"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2604.07420v1/figures/Dual-Rerank-Overview.png)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2604.07420)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\mathcal L=\mathcal L_{rank}+\lambda\,D_{KL}(p_{AR}\Vert p_{NAR})+\gamma\mathcal L_{utility}.
$$

### 论文离线与线上效果

快手搜索 5% 流量一个月：Long View +1.107%，并降低平均与 P99 延迟。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer，实验组只加入 `dual-rerank` 核心机制；相对 NDCG@10 +10.66%。

MovieLens-100K、260 users / 420 items、seed 42：NDCG@10 0.0354 → **0.0392（+10.66%）**。基线是共享 transition + content scorer；实验组只加入论文核心路径。

```bash
auto-research reproduce --paper dual-rerank --dataset-dir data --seed 42
auto-research evolve --model rankmixer --dataset movielens-100k --direction "组合 dual-rerank 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。 本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。
