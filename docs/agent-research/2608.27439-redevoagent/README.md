# RedEvoAgent：经验驱动的自动红队技能进化

> **复现级别：核心机制 + deterministic mini-suite。** 实现工具效果画像、Deciding-Tool Attribution 和 held-out validation ratchet。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2608.27439](https://arxiv.org/abs/2608.27439) |
| 公司 / 机构 | 香港城市大学（第一作者第一署名单位） |
| 首次公开日期 | 2026-08-27（arXiv v1） |
| 原作者代码 | 否：未发现原作者公开代码（核查日期：2026-08-31） |
| 本地 adapter / 方法 | `redevoagent` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260831.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260831.py) |

## 原始论文总结

### 背景与主要改动

RedEvoAgent 不直接检索冗长攻击轨迹，而把跨案例经验蒸馏成可读技能；只归因真正决定成败的工具，并且新技能必须在留出验证集上优于 incumbent 才能晋级。

```mermaid
flowchart LR
  T[攻击轨迹] --> A[Deciding-Tool Attribution]
  A --> S[候选技能]
  S --> V{held-out validation}
  V -->|提升| I[替换 incumbent]
  V -->|未提升| R[拒绝更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![RedEvoAgent：经验驱动的自动红队技能进化 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2608.27439v1/fig1_overview.png)

> **原论文 Figure 1（关键图）**：展示原论文的训练流程与关键优化环节。图片来自[原论文](https://arxiv.org/abs/2608.27439)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
s_{new}=\begin{cases}s_c,&Eval(s_c)>Eval(s_{inc})\\s_{inc},&\text{otherwise.}\end{cases}
$$

## 本地复现

planbench-mini、120 episodes：joint success **1.0000**、average cost **0.4300**；关键价值是 validation ratchet/归因计数，而非简单任务的满分。指标见 [`metrics/planbench-mini-seed42.json`](metrics/planbench-mini-seed42.json)。

## 复现边界

未对真实产品 Agent 执行越权攻击；mini-suite 只验证安全的技能更新控制流。
