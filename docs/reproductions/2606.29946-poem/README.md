# POEM：偏序增强的实时序列建模

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2606.29946](https://arxiv.org/abs/2606.29946) |
| 公司/机构 | Kuaishou（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-06-29（arXiv v1） |
| 原文开源代码 | 否：论文未提供官方/作者代码（核查日期：2026-09-02） |
| Adapter | `poem` |
| 本地复现代码 | [`src/auto_research/reproductions/poem/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/poem/) |

## 原始论文总结

### 背景与主要改动

把当前请求多个排序目标产生的相对次序转成偏序信号，动态构造比纯时间序更贴近实时兴趣的训练序列。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["poem 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["论文定义的直接基线"]
  C --> E["统一指标与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![POEM：偏序增强的实时序列建模 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2606.29946v1/poem_arch_v4.png)

> **原论文 Figure 1（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2606.29946)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
i\\succ j\\iff \\sum_m\\mathbf1[r_m(i)<r_m(j)]>\\sum_m\\mathbf1[r_m(j)<r_m(i)].
$$

### 论文离线与线上效果

- 快手 7 天 5%/5% 流量，主站人均时长 +0.249%，极速版 +0.213%；7 天 5%/5% A/B。
- 上述数字只复述论文线上证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一全目录协议下，基线 NDCG@10 为 `0.05401`，实验组 POEM 为 `0.05009`，相对变化 **-7.25%**。这是公开代理任务的负结果，生产线上 lift 的外推不适用。

三随机种子完整结果、均值、标准差与 95% CI：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper poem --dataset-dir data --seed 42
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。
