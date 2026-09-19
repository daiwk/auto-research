# CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents

> **复现级别：L1 核心机制诊断。** 本地执行熟悉度路由与定向更新；未训练论文规模专家策略。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents](https://arxiv.org/abs/2609.18779) |
| 公司/机构 | IIIS, Tsinghua University（按第一作者署名单位） |
| 首次公开日期 | 2026-09-16（arXiv v1） |
| 原文开源代码 | 否：截至 2026-09-19 未找到原作者公开实现仓库 |
| Adapter / 方法 | `cera-moa` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260919.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260919.py) |

## 原始论文总结

### 背景与主要改动

用中层隐藏状态估计 Agent 对样本的熟悉度，以累计阈值自适应选专家，并把训练样本定向分配给相应专家。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[cera-moa 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.18779v1/cera-moa.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.18779)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、权重、状态转换或调度规则，并把中间量写入指标产物；具体公式与变量对应见实现函数及测试中的不变量断言。

### 论文离线与线上效果

论文报告的线上、benchmark、训练效率或推理速度只作为原文结果。本地三种子 artifact 只验证核心机制、形状和状态不变量，不与论文数字直接横比。指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。

## 复现边界

本地执行熟悉度路由与定向更新；未训练论文规模专家策略。
