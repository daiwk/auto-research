# MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off

> **复现级别：核心机制 mini-suite。** 本地实现执行论文特有的 端到端 Agent 记忆 算子；不把确定性小型评测写成论文完整复现。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2608.04843](https://arxiv.org/abs/2608.04843) |
| 公司/机构/学校 | Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS |
| 首次公开日期 | 2026-08-05（arXiv v1） |
| 原文开源代码 | 否：未发现原作者公开代码（核查日期：2026-08-09） |
| Adapter | `memorycpt` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260809.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260809.py) |

## 原始论文总结

### 背景与主要改动

**主题：端到端 Agent 记忆。** QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。

### 主要架构

```mermaid
flowchart LR
    N0["长交互历史"] --> N1
    N1["QAD 离线蒸馏"] --> N2
    N2["RRF 检索"] --> N3
    N3["QAR + GRPO"] --> N4
    N4["压缩上下文"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2608.04843v1/x1.png)

> **原论文 Figure 1（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2608.04843)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$QPC=Q(answer)/C_{inference}$

### 论文离线效果

LoCoMo 与 LongMemEval 上改善质量—成本折衷；消融验证 QAD、RRF、QAR 与成本 reward 的贡献。

## 本地复现

稳定指标保存在本论文目录的 [`metrics/planbench-mini-seed42.json`](metrics/planbench-mini-seed42.json)，不提交 checkpoint 或原始运行目录。

```bash
auto-research agent-research --method memorycpt --benchmark planbench-mini --episodes 120 --seed 42
```

> **本地对照口径**：`memorycpt` 与同一公开 mini-suite 的无该机制控制组比较；仅报告本地产物中的指标，不把原文大模型/真实环境结果移植为本地提升。

## 复现边界

- 复现论文特有的状态、信用或选择算子，而非只改方法名。
- 未运行原文大模型、专有环境或昂贵 judge；这些缺口不会标注为“已接入”。
- `memorycpt` 已加入统一 evolve 候选发现；组合 genome 仍受公共评测与预算约束。
