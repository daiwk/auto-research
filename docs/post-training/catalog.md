# LLM 后训练方法索引

本页维护后训练方法的统一索引。入口页只展示整体进度；每篇论文的背景、架构、公式、
原文效果和本地实验放在独立详情页。

## 已实现论文

| 方向 | 方法 | 论文信息 | 原作者代码 | 本地入口 |
|---|---|---|---|---|
| On-policy distillation | [Lightning OPD](2604.13010-lightning-opd/README.md) | MIT HAN Lab / Jet AI，2026-04-14 | [已开源](https://github.com/jet-ai-projects/Lightning-OPD) | `lightning-opd` |
| 多目标 RL | [GPRL](2605.18721-gprl/README.md) | Stanford / Oklahoma，2026-05-18 | 未发现 | `gprl` |
| 过程奖励 | [TCR](2607.19824-tcr/README.md) | 作者团队，2026-07-22 | 未发现 | `tcr` |

## 公平基线

- **DPO**（[arXiv 2305.18290](https://arxiv.org/abs/2305.18290)）：直接用偏好对优化
  隐式奖励，作为非在线偏好优化基线，本地键为 `dpo`。
- **GRPO**（[arXiv 2402.03300](https://arxiv.org/abs/2402.03300)）：在同一 prompt
  的候选组内标准化 reward，作为 group-relative RL 基线，本地键为 `grpo`。

所有方法共享候选集合、训练/验证划分、步数和 seed；详细口径见
[统一评测协议](benchmark.md)。

## 后续方向

后续论文按“偏好优化、在线 RL、蒸馏、过程奖励、数据合成与过滤、安全对齐”归档。
一个方法只有在以下内容齐全时才标记为“已实现”：

1. 训练更新不是名称占位，而是落实论文的核心状态和目标；
2. 有公开数据或明确的本地 mini-suite；
3. 有固定 seed 的稳定指标与基线；
4. 有独立论文页和可复现命令；
5. 明确说明相对原论文的折损。
