# Effective Knowledge Transfer for Multi-Task Recommendation Models

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2605.05730](https://arxiv.org/abs/2605.05730) |
| 公司/机构 | Huawei Technologies |
| 首次公开日期 | 2026-05-07（arXiv v1） |
| 原文开源代码 | 否：原文未提供官方/作者代码（核查日期：2026-08-24） |
| Adapter | `ektm` |
| 本地复现代码 | [`src/auto_research/reproductions/ektm/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/ektm/) |

## 原始论文总结

### 背景与主要改动

让 CTR 表示按 CVR 任务相似度向多个转化塔迁移，并以难例感知损失抑制负迁移，保持多任务部署成本可控。

```mermaid
flowchart LR
 A["CTR/CVR 多任务"] --> B["相似度知识迁移"] --> C["难例增强预测"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Effective Knowledge Transfer for Multi-Task Recommendation Models 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2605.05730v1/EKTM.PNG)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2605.05730)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
F_i=\operatorname{mean}(f_{ctr},\hat s_{i1}f^1_{cvr},\ldots,\hat s_{iT}f^T_{cvr})
$$

### 论文离线与线上效果

原文线上证据：**eCPM +3.93%**（5%→20%→50%→100% traffic，Section 4.4.2 / Figure 3）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `ektm` 核心机制，相对 NDCG@10 +10.98%。

MovieLens-100K、220 users / 360 items、seed 42：NDCG@10 0.0540 → **0.0599（+10.98%）**，Hit@10 0.1091 → 0.1182。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper ektm --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
