# DualGR: Generative Retrieval with Long and Short-Term Interests Modeling

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2511.12518](https://arxiv.org/abs/2511.12518) |
| 公司/机构 | USTC / Kuaishou Technology |
| 首次公开日期 | 2025-11-16（arXiv v1） |
| 原文开源代码 | 否：论文未提供官方/作者代码（核查日期：2026-08-09） |
| Adapter | `dualgr` |
| 本地复现代码 | [`src/auto_research/reproductions/dualgr/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/dualgr/) |

## 原始论文总结

### 背景与主要改动

短期兴趣与长期兴趣使用双路由器，约束 Semantic ID 前缀有效性，并以曝光感知项抑制头部坍缩。

```mermaid
flowchart LR
 A["公开输入 / 历史"] --> B["dualgr 核心路径"]
 B --> C["论文特有状态或目标"]
 C --> D["同预算评测"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![DualGR: Generative Retrieval with Long and Short-Term Interests Modeling 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2511.12518v3/x1.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2511.12518)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
p(i|h)=g(h)p_s(i|h)+(1-g(h))p_l(i|h),\quad\mathcal L=\mathcal L_{SID}+\lambda\mathcal L_{expo}.
$$

### 论文离线与线上效果

快手线上 Video Views +0.527%，Watch Time +0.432%。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer，实验组只加入 `dualgr` 核心机制；相对 NDCG@10 +6.73%。

MovieLens-100K、260 users / 420 items、seed 42：NDCG@10 0.0354 → **0.0378（+6.73%）**。基线是共享 transition + content scorer；实验组只加入论文核心路径。

```bash
auto-research reproduce --paper dualgr --dataset-dir data --seed 42
auto-research evolve --model rankmixer --dataset movielens-100k --direction "组合 dualgr 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。 本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。
