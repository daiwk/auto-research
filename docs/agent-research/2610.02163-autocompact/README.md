# AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents

> **复现级别：L1 核心机制诊断。** 执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1](https://arxiv.org/abs/2610.02163) |
| 公司/机构 | 原文首页未列第一作者机构（按第一作者署名单位） |
| 首次公开日期 | 2026-10-01（arXiv v1） |
| 原文开源代码 | 否：截至 2026-10-03 未找到原作者公开实现 |
| Adapter | `autocompact` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20261003.py`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/agent_research/latest_20261003.py) |

## 原始论文总结

### 背景与主要改动

judge 同时审查何时压缩、工作摘要写什么、压缩后下一步怎么做；纠错后的输出直接进入环境，随后以 SFT+结果 RL 联合学习。

```mermaid
flowchart LR
  I[输入与当前状态] --> M[autocompact 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2610.02163v1/fig1_overview.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2610.02163)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$(d,s,a)\leftarrow JudgeCorrect(d,s,a)$ 后再执行。

### 论文离线与线上效果

SWE-bench Verified +9.2 点，SWE-PolyBench Verified +5.0 点。

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。

## 复现边界

执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。
