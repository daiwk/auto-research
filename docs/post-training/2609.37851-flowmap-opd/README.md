# FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators

> **复现级别：L1 核心机制诊断。** 执行 rollout state detach 与 local kernel KL；未训练图像 flow-map generator。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2609.37851](https://arxiv.org/abs/2609.37851) |
| 公司/机构 | Georgia Institute of Technology（按第一作者署名单位） |
| 首次公开日期 | 2026-09-29（arXiv v1） |
| 原文开源代码 | 是：[https://github.com/ZhiqiLi-CG/Flowmap_OPD_source](https://github.com/ZhiqiLi-CG/Flowmap_OPD_source) |
| Adapter | `flowmap-opd` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20261001.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/post_training/latest_20261001.py) |

## 原始论文总结

### 背景与主要改动

把生成状态的 rollout 分布与 teacher/student 比较 kernel 解耦：rollout 只负责提供具有正确边缘分布的状态，优化 kernel 在这些冻结状态上比较 flow map、诱导速度或瞬时速度。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[flowmap-opd 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/更新状态]
```

<!-- paper-figure:start -->
### 原论文关键图

[![FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.37851v1/flowmap_opd_teaser.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.37851)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$L(\theta)=\mathbb E_{z\sim\rho^\theta}[\ell(\theta,T;z)]$。本地从计算图中 detach rollout state，仅让 local KL kernel 更新 student。

### 论文离线与线上效果

原文在 ImageNet 和多 specialist teacher consolidation 上验证 few-step student；本地只验证 rollout/kernel 梯度隔离。

## 本地复现

> **本地对照口径**：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。

三种子诊断见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。`diagnostic_only=true`，只证明核心状态转换、梯度或调度不变量可执行，不能进入正式能力排名。

## 复现边界

执行 rollout state detach 与 local kernel KL；未训练图像 flow-map generator。
