# HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning

> **复现级别：核心机制 mini-suite。** 本地实现执行论文特有的 搜索轨迹 hindsight 算子；不把确定性小型评测写成论文完整复现。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2608.01597](https://arxiv.org/abs/2608.01597) |
| 公司/机构/学校 | Santa Clara University |
| 首次公开日期 | 2026-08-03（arXiv v1） |
| 原文开源代码 | 是：[https://anonymous.4open.science/r/hindsearch-anon-EBDC](https://anonymous.4open.science/r/hindsearch-anon-EBDC) |
| Adapter | `hindsearch` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260809.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260809.py) |

## 原始论文总结

### 背景与主要改动

**主题：搜索轨迹 hindsight。** 冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。

### 主要架构

```mermaid
flowchart LR
    N0["搜索 rollout"] --> N1
    N1["最终 verifier"] --> N2
    N2["失败轨迹"] --> N3
    N3["gold-aware critique"] --> N4
    N4["GRPO + distillation"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2608.01597v1/x1.png)

> **原论文 Figure 2（关键图）**：展示原论文的训练流程与关键优化环节。图片来自[原论文](https://arxiv.org/abs/2608.01597)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$\mathcal L=\mathcal L_{GRPO}+\lambda\mathcal L_{distill}(\pi_\theta,\text{critique})$

### 论文离线效果

论文在搜索增强推理任务报告稳定改善，详情页保留原文口径；本地不把 judge 使用 gold answer 伪装成部署时能力。

## 本地复现

稳定指标保存在本论文目录的 [`metrics/planbench-mini-seed42.json`](metrics/planbench-mini-seed42.json)，不提交 checkpoint 或原始运行目录。

```bash
auto-research agent-research --method hindsearch --benchmark planbench-mini --episodes 120 --seed 42
```

> **本地对照口径**：`hindsearch` 与同一公开 mini-suite 的无该机制控制组比较；仅报告本地产物中的指标，不把原文大模型/真实环境结果移植为本地提升。

## 复现边界

- 复现论文特有的状态、信用或选择算子，而非只改方法名。
- 未运行原文大模型、专有环境或昂贵 judge；这些缺口不会标注为“已接入”。
- `hindsearch` 已加入统一 evolve 候选发现；组合 genome 仍受公共评测与预算约束。
