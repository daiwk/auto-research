# OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2603.02999](https://arxiv.org/abs/2603.02999) |
| 公司/机构 | Tencent |
| 首次公开日期 | 2026-03-03（arXiv v1） |
| 原文开源代码 | 否：未发现/未发布原作者官方代码仓库（核查日期：2026-08-08） |
| Adapter | `oneranker` |
| 本地复现代码 | [`src/auto_research/reproductions/oneranker/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/oneranker/) |

## 原始论文总结

### 背景与主要改动

用 fake item token 统一生成、点击价值估计和广告排序，并通过分布一致性约束让生成概率与 value head 保持同一偏好。

```mermaid
flowchart LR
 A["公开输入 / 历史"] --> B["oneranker 核心路径"]
 B --> C["论文特有状态或目标"]
 C --> D["同预算评测"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2603.02999v3/x2.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2603.02999)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\mathcal L=\mathcal L_{gen}+\lambda_v\mathcal L_{value}+\lambda_cD_{KL}(p_{gen}\Vert p_{rank}).
$$

### 论文离线与线上效果

微信视频号广告全量部署：GMV +1.34%。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer，实验组只加入 `oneranker` 核心机制；相对 NDCG@10 -7.65%。

MovieLens-100K、260 users / 420 items、seed 42：NDCG@10 0.0354 → **0.0327（-7.65%）**。基线是共享 transition + content scorer；实验组只加入论文核心路径。

```bash
auto-research reproduce --paper oneranker --dataset-dir data --seed 42
auto-research evolve --model rankmixer --dataset movielens-100k --direction "组合 oneranker 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。 本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。
