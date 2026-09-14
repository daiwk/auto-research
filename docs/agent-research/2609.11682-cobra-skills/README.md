# COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization

> **复现级别：L1 核心机制诊断。** 本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization](https://arxiv.org/abs/2609.11682) |
| 公司/机构 | The Chinese University of Hong Kong, Shenzhen（按第一作者署名单位） |
| 首次公开日期 | 2026-09-10 |
| 原文开源代码 | 是：[https://github.com/Jerry-LuP/COBRA-Skills](https://github.com/Jerry-LuP/COBRA-Skills) |
| Adapter / 方法 | `cobra-skills` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260914.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260914.py) |

## 原始论文总结

### 背景与主要改动

把技能优化视为动态候选空间中的预算化 contextual bandit，优先评估高收益或高信息量技能，再依据执行反馈演化。

```mermaid
flowchart LR
  I[输入与公开状态] --> M[cobra-skills 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.11682v1/frameworks.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.11682)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式或操作

本地代码把论文决定性操作实现为确定性的 reference kernel，并显式输出门控、选择、投影、图边或状态更新统计；测试覆盖公式不变量和边界条件。

### 论文离线与线上效果

六个 benchmark、三个模型上成本降低 55%–58%，相对无技能 Agent 提升 13.1/26.9/22.5 pp。 这些数字来自原论文，不与本地缩小实验直接比较；论文未报告线上 A/B 时不推断线上收益。

## 本地复现

三种子指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。

### 复现边界

本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。
