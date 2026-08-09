# CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents

> **复现级别：核心机制 mini-suite。** 本地实现执行论文特有的 代码检索 Agent 算子；不把确定性小型评测写成论文完整复现。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2608.05886](https://arxiv.org/abs/2608.05886) |
| 公司/机构/学校 | NetEase Guangzhou AI Lab |
| 首次公开日期 | 2026-08-06（arXiv v1） |
| 原文开源代码 | 否：未发现原作者公开代码（核查日期：2026-08-09） |
| Adapter | `codegrep` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260809.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260809.py) |

## 原始论文总结

### 背景与主要改动

**主题：代码检索 Agent。** 以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。

### 主要架构

```mermaid
flowchart LR
    N0["issue"] --> N1
    N1["并行 grep/glob/read"] --> N2
    N2["GRPO 检索策略"] --> N3
    N3["候选文件"] --> N4
    N4["冻结 coding agent"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2608.05886v1/figures/training_curves_main.png)

> **原论文 Figure 2（关键图）**：展示原论文的训练流程与关键优化环节。图片来自[原论文](https://arxiv.org/abs/2608.05886)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$R=R_{resolve}-\lambda_{tok}C_{tok}-\lambda_{round}C_{round}$

### 论文离线效果

SWE-Bench Verified 500 题 resolve 25.8%→27.0%（+1.2pp），成功样本 rounds -15%、tokens -19%。

## 本地复现

稳定指标保存在本论文目录的 [`metrics/planbench-mini-seed42.json`](metrics/planbench-mini-seed42.json)，不提交 checkpoint 或原始运行目录。

```bash
auto-research agent-research --method codegrep --benchmark planbench-mini --episodes 120 --seed 42
```

> **本地对照口径**：`codegrep` 与同一公开 mini-suite 的无该机制控制组比较；仅报告本地产物中的指标，不把原文大模型/真实环境结果移植为本地提升。

## 复现边界

- 复现论文特有的状态、信用或选择算子，而非只改方法名。
- 未运行原文大模型、专有环境或昂贵 judge；这些缺口不会标注为“已接入”。
- `codegrep` 已加入统一 evolve 候选发现；组合 genome 仍受公共评测与预算约束。
