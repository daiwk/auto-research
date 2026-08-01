# LLM 后训练论文与资料索引

本页维护后训练方法的统一索引。入口页只展示整体进度；正式论文与关键网页资料的背景、
架构、公式、原文效果和本地实验放在独立详情页。

## 已实现论文与资料

| 方向 | 方法 | 论文信息 | 原作者代码 | 本地入口 |
|---|---|---|---|---|
| 直接偏好优化 | [DPO](2305.18290-dpo/README.md) | Stanford，2023-05-29 | [已开源](https://github.com/eric-mitchell/direct-preference-optimization) | `dpo` |
| 二元反馈对齐 | [KTO](2402.01306-kto/README.md) | Contextual AI / Stanford，2024-02-02 | [已开源](https://github.com/ContextualAI/HALOs) | `kto` |
| 单阶段偏好 | [ORPO](2403.07691-orpo/README.md) | KAIST，2024-03-12 | [已开源](https://github.com/xfactlab/orpo) | `orpo` |
| 在线推理 RL | [DeepSeekMath / GRPO](2402.03300-grpo/README.md) | DeepSeek-AI，2024-02-05 | [已开源](https://github.com/deepseek-ai/DeepSeek-Math) | `grpo` |
| 训推失配校正 | [TIS](web-2025-tis/README.md) | UC San Diego / Microsoft Research，2025-08-05 | 未发布独立算法仓库 | `tis` |
| MoE 训推失配 | [IcePop](2510.18855-icepop/README.md) | Ant Group / Inclusion AI，2025-10-21 | 未发现 IcePop 独立算法源代码 | `icepop` |
| 纯在线训推校正 | [Online IcePop](web-2025-online-icepop/README.md) | Jian Hu / Ant Group Bailing Team，2025-12-16 | 未发布独立源代码 | `online-icepop` |
| 几何信任域 | [RIPO](2607.10169-ripo/README.md) | 论文作者团队，2026-07-11 | 未发现官方代码 | `ripo` |
| 异步训推失配 | [KPop](2606.15079-kpop/README.md) | Ling / Ring 技术报告作者团队，2026-06-13 | 未发现独立算法开源仓库 | `kpop` |
| 梯度保留 clip | [GPPO](2508.07629-gppo/README.md) | Klear-Reasoner 作者团队，2025-08-11 | 未发现独立算法开源仓库 | `gppo` |
| GRPO 聚合偏置 | [Dr. GRPO](2503.20783-dr-grpo/README.md) | SAIL 研究团队，2025-03-26 | [已开源](https://github.com/sail-sg/understand-r1-zero) | `dr-grpo` |
| Reference anchor | [ARMOR](2607.10481-armor/README.md) | 论文作者团队，2026-07-11 | 未发现官方代码 | `armor` |
| 全局优势估计 | [REINFORCE++](2501.03262-reinforce-plus/README.md) | 论文作者团队，2025-01-04 | 未发现官方代码 | `reinforce-plus` |
| Token 信用校准 | [TACO](2607.07976-taco/README.md) | 论文作者团队，2026-07-08 | [已开源](https://github.com/xiuyilou/TACO) | `taco` |
| SFT-RL 动态混合 | [CHORD](2508.11408-chord/README.md) | Alibaba Group / ModelScope，2025-08-15 | [已开源](https://github.com/modelscope/Trinity-RFT/tree/main/examples/mix_chord) | `chord` |
| Critic PPO | [VAPO](2504.05118-vapo/README.md) | 论文作者团队，2025-04-07 | 未发现官方代码 | `vapo` |
| 分布保持 RL | [ReCo](2607.26862-reco/README.md) | Seoul National University，2026-07-29 | 未发布独立仓库 | `reco-grpo` |
| 经典 RLHF | [InstructGPT / PPO-RLHF](2203.02155-ppo-rlhf/README.md) | OpenAI，2022-03-04 | [部分开源](https://github.com/openai/following-instructions-human-feedback) | `ppo-rlhf` |
| 经典 RLHF | [RLOO](2402.14740-rloo/README.md) | Cohere For AI / Cohere，2024-02-22 | 未发布独立仓库 | `rloo` |
| 经典 RLHF | [ReMax](2310.10505-remax/README.md) | CUHK-Shenzhen / SRIBD / Nanjing University，2023-10-16 | [已开源](https://github.com/liziniu/ReMax) | `remax` |
| 经典 On-policy distillation | [GKD](2306.13649-gkd/README.md) | Google DeepMind / Mila / University of Toronto，2023-06-23 | 原作者未发布独立仓库；[TRL 后续实现](https://github.com/huggingface/trl/blob/main/docs/source/distillation_trainer.md) | `gkd` |
| Reverse-KL distillation | [MiniLLM](2306.08543-minillm/README.md) | Tsinghua University / Microsoft Research，2023-06-14 | [已开源](https://github.com/microsoft/LMOps/tree/main/minillm) | `minillm` |
| On-policy self-distillation | [OPSD](2601.18734-opsd/README.md) | UCLA / HKU / Meta Superintelligence Labs，2026-01-26 | [已开源](https://github.com/siyan-zhao/OPSD) | `opsd` |
| Context distillation | [OPCD](2602.12275-opcd/README.md) | Microsoft Research，2026-02-12 | [已开源](https://github.com/microsoft/LMOps/tree/main/opcd) | `opcd` |
| On-policy self-distillation | [β-OPSD](2607.28582-beta-opsd/README.md) | University of Maryland，2026-07-30 | 未发现官方代码 | `beta-opsd` |
| Context distillation | [Flux-OPD](2607.28022-flux-opd/README.md) | Peking University / Kling Team / Tsinghua / SJTU，2026-07-30 | 未发现官方代码 | `flux-opd` |
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
| 序列概率校准 | [SLiC-HF](2305.10425-slic-hf/README.md) | Google DeepMind / Google Research，2023-05-17 | 未发布独立实现 | `slic-hf` |
| 多属性可控 SFT | [SteerLM](2310.05344-steerlm/README.md) | NVIDIA，2023-10-09 | [NeMo-Aligner](https://github.com/NVIDIA/NeMo-Aligner) | `steerlm` |
| 自博弈微调 | [SPIN](2401.01335-spin/README.md) | UCLA，2024-01-02 | [已开源](https://github.com/uclaml/SPIN) | `spin` |
| On-policy distillation | [Relay-OPD](2607.26057-relay-opd/README.md) | Zhejiang University / Alibaba Group Yuvion Team，2026-07-28 | [已开源](https://github.com/ZJU-REAL/Relay-OPD) | `relay-opd` |
| Token-level credit assignment | [CoRT](2607.25659-cort/README.md) | ByteDance internship / academic author team，2026-07-28 | 未发现 | `cort` |

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
