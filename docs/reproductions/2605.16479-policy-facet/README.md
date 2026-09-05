# 策略约束的动态职位搜索 Facet 推荐

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2605.16479](https://arxiv.org/abs/2605.16479) |
| 公司/机构 | LinkedIn（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-05-15（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-02） |
| Adapter | `policy-facet` |
| 本地复现代码 | [`src/auto_research/reproductions/policy_facet/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/policy_facet/) |

## 原始论文总结

### 背景与主要改动

先由人工与 LLM 维护符合产品策略的 facet taxonomy，再用 embedding SLM 召回候选，以生成式 SLM 做单 token 点式评分；前缀缓存和批处理满足实时延迟。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["policy-facet 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![策略约束的动态职位搜索 Facet 推荐 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2605.16479#page=3)

> **原论文 Figure 2（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2605.16479)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\\mathcal C_K=\\operatorname{TopK}_{c\\in\\mathcal T}\\cos(e_{u,q},e_c),\\qquad s_c=\\log p_\\theta(\\mathrm{Okay}\\mid u,q,c).
$$

### 论文离线与线上效果

- LinkedIn Job Search 线上 A/B：Facet CTR +34.8%、申请/曝光比 +2.6%、成功搜索会话 +1.6%。
- 上述数字只复述论文线上证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.04713`，相对变化 **-12.73%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子完整结果、均值、标准差与 95% CI：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper policy-facet --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
