# EGR：共享 LLM 的原生向量生成式召回

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2607.23038](https://arxiv.org/abs/2607.23038) |
| 公司/机构 | Snap Inc.（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-07-25（arXiv v1） |
| 原文开源代码 | 否：论文未提供官方/作者代码（核查日期：2026-09-02） |
| Adapter | `egr` |
| 本地复现代码 | [`src/auto_research/reproductions/egr/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/egr/) |

## 原始论文总结

### 背景与主要改动

同一编码骨干产生 item 索引向量和 user query 向量，并让 item representation learning 与 next-item prediction 全程联合训练。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["egr 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["论文定义的直接基线"]
  C --> E["统一指标与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![EGR：共享 LLM 的原生向量生成式召回 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2607.23038v1/methodology.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2607.23038)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\\mathcal L=\\mathcal L_{IRL}+\\lambda_t\\mathcal L_{NIP},\\quad s(u,i)=q_u^\\top z_i.
$$

### 论文离线与线上效果

- Snap DPA 两周 10%/10% 流量，曝光 +0.15%、CTR +0.23%、CVR +2.91%；随后全量部署。
- 上述数字只复述论文线上证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一全目录协议下，基线 NDCG@10 为 `0.05401`，实验组 EGR 为 `0.05025`，相对变化 **-6.95%**。这是公开代理任务的负结果，生产线上 lift 的外推不适用。

三随机种子完整结果、均值、标准差与 95% CI：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper egr --dataset-dir data --seed 42
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。
