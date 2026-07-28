# LLM 后训练方法索引

本页维护后训练方法的统一索引。入口页只展示整体进度；每篇论文的背景、架构、公式、
原文效果和本地实验放在独立详情页。

## 已实现论文

| 方向 | 方法 | 论文信息 | 原作者代码 | 本地入口 |
|---|---|---|---|---|
| 直接偏好优化 | [DPO](2305.18290-dpo/README.md) | Stanford，2023-05-29 | [已开源](https://github.com/eric-mitchell/direct-preference-optimization) | `dpo` |
| 二元反馈对齐 | [KTO](2402.01306-kto/README.md) | Contextual AI / Stanford，2024-02-02 | [已开源](https://github.com/ContextualAI/HALOs) | `kto` |
| 单阶段偏好 | [ORPO](2403.07691-orpo/README.md) | KAIST，2024-03-12 | [已开源](https://github.com/xfactlab/orpo) | `orpo` |
| 在线推理 RL | [DeepSeekMath / GRPO](2402.03300-grpo/README.md) | DeepSeek-AI，2024-02-05 | [已开源](https://github.com/deepseek-ai/DeepSeek-Math) | `grpo` |
| 经典 RLHF | [InstructGPT / PPO-RLHF](2203.02155-ppo-rlhf/README.md) | OpenAI，2022-03-04 | [部分开源](https://github.com/openai/following-instructions-human-feedback) | `ppo-rlhf` |
| 经典 RLHF | [RLOO](2402.14740-rloo/README.md) | Cohere For AI / Cohere，2024-02-22 | 未发布独立仓库 | `rloo` |
| 经典 RLHF | [ReMax](2310.10505-remax/README.md) | CUHK-Shenzhen / SRIBD / Nanjing University，2023-10-16 | [已开源](https://github.com/liziniu/ReMax) | `remax` |
| 长推理 RL | [DAPO](2503.14476-dapo/README.md) | ByteDance Seed / Tsinghua AIR，2025-03-18 | [已开源](https://github.com/BytedTsinghua-SIA/DAPO) | `dapo` |
| 稳定序列 RL | [GSPO](2507.18071-gspo/README.md) | Alibaba Qwen Team，2025-07-24 | 原论文无独立仓库；[ROLL 后续实现](https://alibaba.github.io/ROLL/docs/User%20Guides/Algorithms/GSPO/) | `gspo` |
| On-policy distillation | [Lightning OPD](2604.13010-lightning-opd/README.md) | MIT HAN Lab / Jet AI，2026-04-14 | [已开源](https://github.com/jet-ai-projects/Lightning-OPD) | `lightning-opd` |
| 多目标 RL | [GPRL](2605.18721-gprl/README.md) | Stanford / Oklahoma，2026-05-18 | 未发现 | `gprl` |
| 过程奖励 | [TCR](2607.19824-tcr/README.md) | 作者团队，2026-07-22 | 未发现 | `tcr` |
| 偏好正则 | [IPO](2310.12036-ipo/README.md) | Google DeepMind，2023-10-18 | 未发布独立仓库 | `ipo` |
| Reference-free 偏好 | [SimPO](2405.14734-simpo/README.md) | Princeton，2024-05-23 | [已开源](https://github.com/princeton-nlp/SimPO) | `simpo` |
| 长度无偏 RL | [LUSPO](2602.05261-luspo/README.md) | 作者团队，2026-02-05 | 未发现 | `luspo` |
| 能力边界课程 | [CoBA-RL](2606.22317-coba-rl/README.md) | Zhejiang / NUS，2026-06-21 | 未发现 | `coba-rl` |
| AI 反馈安全对齐 | [Constitutional AI](2212.08073-constitutional-ai/README.md) | Anthropic，2022-12-15 | [补充材料](https://github.com/anthropics/ConstitutionalHarmlessnessPaper) | `constitutional-ai` |
| 全排序偏好 | [RRHF](2304.05302-rrhf/README.md) | Alibaba DAMO / Tsinghua，2023-04-11 | [已开源](https://github.com/GanjinZero/RRHF) | `rrhf` |
| Reward 选优微调 | [RAFT](2304.06767-raft/README.md) | HKUST / UIUC，2023-04-13 | [LMFlow](https://github.com/OptimalScale/LMFlow) | `raft` |

## 公平基线

所有后训练方法都与同一未训练 candidate policy 比较；DPO 与 GRPO 已从“薄基线”
升级为独立机制复现，不能再把它们写成未实现的名字占位。

所有方法共享候选集合、训练/验证划分、步数和 seed；详细口径见
[统一评测协议](benchmark.md)。

## 后续方向

系统谱系、明确的 P1 与暂缓原因见[论文谱系与缺口](lineage.md)。后续论文按
“偏好优化、在线 RL、蒸馏、过程奖励、数据合成与过滤、安全对齐”归档。
一个方法只有在以下内容齐全时才标记为“已实现”：

1. 训练更新不是名称占位，而是落实论文的核心状态和目标；
2. 有公开数据或明确的本地 mini-suite；
3. 有固定 seed 的稳定指标与基线；
4. 有独立论文页和可复现命令；
5. 明确说明相对原论文的折损。
