# Contextual Information Policy Optimization for Search Agents

> **复现级别：核心机制 mini-suite。** 本地实现执行论文特有的 搜索 Agent RL 算子；不把确定性小型评测写成论文完整复现。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2608.06128](https://arxiv.org/abs/2608.06128) |
| 公司/机构/学校 | Beihang University |
| 首次公开日期 | 2026-08-06（arXiv v1） |
| 原文开源代码 | 否：未发现原作者公开代码（核查日期：2026-08-09） |
| Adapter | `cipo` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260809.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260809.py) |

## 原始论文总结

### 背景与主要改动

**主题：搜索 Agent RL。** 只奖励最终答案会让检索退化成确认偏见。CIPO 识别受外部证据影响的后续动作，给予 dense turn credit，并与全局 outcome reward 联合优化。

### 主要架构

```mermaid
flowchart LR
    N0["搜索请求"] --> N1
    N1["外部证据"] --> N2
    N2["evidence influence"] --> N3
    N3["turn-level credit"] --> N4
    N4["global outcome"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Contextual Information Policy Optimization for Search Agents 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2608.06128v1/x2.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2608.06128)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$A_t=\lambda A_t^{evidence}+(1-\lambda)A^{outcome}$

### 论文离线效果

7 个域内/域外基准上减少 prior-driven reasoning，并在多数任务取得最佳或有竞争力结果。

## 本地复现

稳定指标保存在本论文目录的 [`metrics/planbench-mini-seed42.json`](metrics/planbench-mini-seed42.json)，不提交 checkpoint 或原始运行目录。

```bash
auto-research agent-research --method cipo --benchmark planbench-mini --episodes 120 --seed 42
```

> **本地对照口径**：`cipo` 与同一公开 mini-suite 的无该机制控制组比较；仅报告本地产物中的指标，不把原文大模型/真实环境结果移植为本地提升。

## 复现边界

- 复现论文特有的状态、信用或选择算子，而非只改方法名。
- 未运行原文大模型、专有环境或昂贵 judge；这些缺口不会标注为“已接入”。
- `cipo` 已加入统一 evolve 候选发现；组合 genome 仍受公共评测与预算约束。
