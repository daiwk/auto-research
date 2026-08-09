# RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction

> **复现级别：核心机制 mini-suite。** 本地实现执行论文特有的 生成式奖励模型 算子；不把确定性小型评测写成论文完整复现。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv 2608.06310](https://arxiv.org/abs/2608.06310) |
| 公司/机构/学校 | Northeastern University |
| 首次公开日期 | 2026-08-06（arXiv v1） |
| 原文开源代码 | 是：[https://github.com/wangclnlp/RRC](https://github.com/wangclnlp/RRC) |
| Adapter | `rrc` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20260809.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/post_training/latest_20260809.py) |

## 原始论文总结

### 背景与主要改动

**主题：生成式奖励模型。** 生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。RRC 用组内自竞争排序和少量 anchor 排序构造中心化 reward。

### 主要架构

```mermaid
flowchart LR
    N0["候选回答组"] --> N1
    N1["生成式 RM 比较"] --> N2
    N2["self-competitive rank"] --> N3
    N3["anchor-guided rank"] --> N4
    N4["策略更新"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2608.06310v1/x2.png)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2608.06310)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$r_i=\frac{\operatorname{rank}(y_i)-\bar r}{K-1}+\lambda r_i^{anchor}$

### 论文离线效果

AlpacaEval2 由 35.8% 提至 41.3%，ArenaHardV2 由 8.0% 提至 11.2%。

## 本地复现

稳定指标保存在本论文目录的 [`metrics/arithmetic-smoke-seed42.json`](metrics/arithmetic-smoke-seed42.json)，不提交 checkpoint 或原始运行目录。

```bash
auto-research post-train --algorithm rrc --dataset arithmetic-smoke --steps 120 --seed 42
```

> **本地对照口径**：`rrc` 与同一公开 mini-suite 的无该机制控制组比较；仅报告本地产物中的指标，不把原文大模型/真实环境结果移植为本地提升。

## 复现边界

- 复现论文特有的状态、信用或选择算子，而非只改方法名。
- 未运行原文大模型、专有环境或昂贵 judge；这些缺口不会标注为“已接入”。
- `rrc` 已加入统一 evolve 候选发现；组合 genome 仍受公共评测与预算约束。
