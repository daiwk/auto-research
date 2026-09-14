# Negative Self-Distillation: Learning to Reason by Avoiding Flaws

> **复现级别：L1 核心机制诊断。** 本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Negative Self-Distillation: Learning to Reason by Avoiding Flaws](https://arxiv.org/abs/2609.11699) |
| 公司/机构 | University of Virginia（按第一作者署名单位） |
| 首次公开日期 | 2026-09-10 |
| 原文开源代码 | 是：[https://github.com/Prongcan/NSD](https://github.com/Prongcan/NSD) |
| Adapter / 方法 | `nsd` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20260914.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/post_training/latest_20260914.py) |

## 原始论文总结

### 背景与主要改动

让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。

```mermaid
flowchart LR
  I[输入与公开状态] --> M[nsd 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Negative Self-Distillation: Learning to Reason by Avoiding Flaws 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.11699v1/intro.png)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2609.11699)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式或操作

本地代码把论文决定性操作实现为确定性的 reference kernel，并显式输出门控、选择、投影、图边或状态更新统计；测试覆盖公式不变量和边界条件。

### 论文离线与线上效果

七个数学 benchmark 上，1.7B/4B/8B 模型平均提升 2.3%/7.5%/6.0%。 这些数字来自原论文，不与本地缩小实验直接比较；论文未报告线上 A/B 时不推断线上收益。

## 本地复现

三种子指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。

### 复现边界

本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。
