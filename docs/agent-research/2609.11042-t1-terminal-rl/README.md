# T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks

> **复现级别：L1 核心机制诊断。** 本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks](https://arxiv.org/abs/2609.11042) |
| 公司/机构 | National University of Singapore / Tencent（按第一作者署名单位） |
| 首次公开日期 | 2026-09-09 |
| 原文开源代码 | 否：未找到作者公开仓库（核查日期：2026-09-14） |
| Adapter / 方法 | `t1-terminal-rl` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260914.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260914.py) |

## 原始论文总结

### 背景与主要改动

TITO 使用 rollout 实际采样 token id 训练，turn boundary repair 修正漂移，R3 重放 MoE 路由选择。

```mermaid
flowchart LR
  I[输入与公开状态] --> M[t1-terminal-rl 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks 原论文 Figure 9](assets/paper-figure-01.png)](https://arxiv.org/html/2609.11042v1/performance_raise_0907.png)

> **原论文 Figure 9（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2609.11042)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式或操作

本地代码把论文决定性操作实现为确定性的 reference kernel，并显式输出门控、选择、投影、图边或状态更新统计；测试覆盖公式不变量和边界条件。

### 论文离线与线上效果

Terminal-Bench 2.1 从 base 43.8% 提升到 64.0%，训练—推理 log-prob gap 从 0.021 降到 0.013。 这些数字来自原论文，不与本地缩小实验直接比较；论文未报告线上 A/B 时不推断线上收益。

## 本地复现

三种子指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。

### 复现边界

本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。
