# Trajectory Learnability for Offline On-Policy Distillation

> **复现级别：L1 核心机制诊断。** 本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Trajectory Learnability for Offline On-Policy Distillation](https://arxiv.org/abs/2609.18321) |
| 公司/机构 | National University of Singapore（按第一作者署名单位） |
| 首次公开日期 | 2026-09-16（arXiv v1） |
| 原文开源代码 | 否：截至 2026-09-19 未找到原作者公开实现仓库 |
| Adapter / 方法 | `trajectory-learnability` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20260919.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/post_training/latest_20260919.py) |

## 原始论文总结

### 背景与主要改动

用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[trajectory-learnability 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Trajectory Learnability for Offline On-Policy Distillation 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2609.18321#page=5)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.18321)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、权重、状态转换或调度规则，并把中间量写入指标产物；具体公式与变量对应见实现函数及测试中的不变量断言。

### 论文离线与线上效果

论文报告的线上、benchmark、训练效率或推理速度只作为原文结果。本地三种子 artifact 只验证核心机制、形状和状态不变量，不与论文数字直接横比。指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。

## 复现边界

本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。
