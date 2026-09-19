# RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning

> **复现级别：L1 核心机制诊断。** 本地执行退休判据与学生更新；未训练论文规模 Agent 教师。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2609.20784) |
| 公司/机构 | Zhejiang University（按第一作者署名单位） |
| 首次公开日期 | 2026-09-17（arXiv v1） |
| 原文开源代码 | 是：[https://github.com/ZJU-REAL/SDAR](https://github.com/ZJU-REAL/SDAR) |
| Adapter / 方法 | `retire-opd` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20260919.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/post_training/latest_20260919.py) |

## 原始论文总结

### 背景与主要改动

给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[retire-opd 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning 原论文 Figure 3](assets/paper-figure-01.png)](https://arxiv.org/html/2609.20784v1/method.png)

> **原论文 Figure 3（关键图）**：展示原论文的训练流程与关键优化环节。图片来自[原论文](https://arxiv.org/abs/2609.20784)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、权重、状态转换或调度规则，并把中间量写入指标产物；具体公式与变量对应见实现函数及测试中的不变量断言。

### 论文离线与线上效果

论文报告的线上、benchmark、训练效率或推理速度只作为原文结果。本地三种子 artifact 只验证核心机制、形状和状态不变量，不与论文数字直接横比。指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。

## 复现边界

本地执行退休判据与学生更新；未训练论文规模 Agent 教师。
