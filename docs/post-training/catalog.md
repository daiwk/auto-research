# LLM 后训练论文与资料索引

本页由 `docs/research-manifest.json` 自动生成；论文元数据只在统一 manifest
维护。背景、架构、公式、原文效果和本地实验请进入独立详情页。

## 已实现论文与资料

<div class="ar-method-index" markdown>

| 方向 | 方法 | 一作机构与日期 | 原作者代码 | 本地入口 |
|---|---|---|---|---|
| 搜索增强 OPD + RL | [OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning](2608.24310-opd-search-plus/README.md) | University of Chinese Academy of Sciences，2026-08-25 | 未发现官方代码 | `opd-search-plus` |
| 可验证奖励 OPD | [OPDVR: On-Policy Distillation with Verifiable Rewards](2608.24696-opdvr/README.md) | LeapLab, Tsinghua University，2026-08-25 | [已开源](https://github.com/LeapLabTHU/OPDVR) | `opdvr` |
| 输入侧 Query-KL | [Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization](2608.23311-erpo/README.md) | AMAP, Alibaba Group，2026-08-24 | [已开源](https://github.com/alibaba/ERPO) | `erpo` |
| 反思式 token 信用 | [SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning](2608.23493-srpo/README.md) | Wuhan University，2026-08-24 | [已开源](https://github.com/Galleons2029/SRPO) | `srpo` |
| OPD | [Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress](2608.19408-r2-opd/README.md) | Authors did not disclose affiliation，2026-08-19 | 未发现官方代码 | `r2-opd` |
| 多奖励 RL | [Learn What's Left, Not What's Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization](2608.16072-sa-mrpo/README.md) | University of Florida，2026-08-17 | 未发现官方代码 | `sa-mrpo` |
| 多模态上下文偏好校准 | [Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization](2608.12158-c2-dpo/README.md) | Korea University，2026-08-12 | [已开源](https://github.com/mlvlab/C2-DPO) | `c2-dpo` |
| 几何约束 RL | [GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs](2608.11674-gcpo/README.md) | Shanghai AI Laboratory，2026-08-12 | [已开源](https://github.com/Icarus1411/GCPO) | `gcpo` |
| 前瞻偏好树 | [Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations](2608.12062-pto/README.md) | Reichman University，2026-08-12 | 未发现官方代码 | `pto` |
| Rubric RL | [Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL](2608.11669-rubric-dropout/README.md) | Scale AI，2026-08-12 | 未发现官方代码 | `rubric-dropout` |
| OPD | [SR-OPSD: Self-Referenced On-Policy Self-Distillation](2608.09745-sr-opsd/README.md) | Independent Researcher，2026-08-10 | 未发现官方代码 | `sr-opsd` |
| 自适应自蒸馏 | [DASH](2608.06243-dash/README.md) | Nanjing University，2026-08-06 | [已开源](https://github.com/DBtxy/DASH-OPSD) | `dash` |
| OPD | [On-Policy Delta Distillation for Multilingual Math Reasoning](2608.05802-opd2/README.md) | NAVER AI Lab，2026-08-06 | [已开源](https://github.com/naver-ai/opd2) | `opd2` |
| 推理枢纽蒸馏 | [RP-OPSD](2608.06347-rp-opsd/README.md) | Nanjing University，2026-08-06 | [已开源](https://github.com/NJUNLP/RP-OPSD) | `rp-opsd` |
| 生成式奖励模型 | [RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction](2608.06310-rrc/README.md) | Northeastern University，2026-08-06 | [已开源](https://github.com/wangclnlp/RRC) | `rrc` |
| 无监督自蒸馏 | [U-OPSD](2608.06296-u-opsd/README.md) | University of California, San Diego，2026-08-06 | 未发现官方代码 | `u-opsd` |
| rollout 预算分配 | [Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning](2608.05080-rail/README.md) | University of Notre Dame / Amazon，2026-08-05 | 未发现官方代码 | `rail` |
| RL rollout 加速 | [SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts](2608.04962-specroll/README.md) | VNU University of Engineering and Technology / Viettel AI，2026-08-05 | [已开源](https://anonymous.4open.science/r/SpecRoll-26062006) | `specroll` |
| 回报相关奖励塑形 | [ADRS](2608.03223-adrs/README.md) | University of Science and Technology of China，2026-08-04 | [已开源](https://github.com/gitrxh/ADRS-arxiv) | `adrs` |
| OPD | [CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning](2608.03673-causal-opd/README.md) | Authors did not disclose affiliation，2026-08-04 | 未发现官方代码 | `causal-opd` |
| OPD | [SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation](2608.03092-smopd/README.md) | Alibaba / Qwen，2026-08-04 | 未发现官方代码 | `smopd` |
| 外部 rollout | [Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models](2608.01717-erils/README.md) | Seoul National University，2026-08-03 | 未发现官方代码 | `erils` |
| 持续一致性蒸馏 | [PCSD](2608.01837-pcsd/README.md) | 论文未列机构，2026-08-03 | 未发现官方代码 | `pcsd` |
| OPD | [Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance](2608.00782-rstg/README.md) | Tianjin University，2026-08-01 | 未发现官方代码 | `rstg` |
| OPD | [Contrastive Reinforced Policy Optimization via Privileged Self-Distillation](2607.28026-crpo/README.md) | Authors did not disclose affiliation，2026-07-30 | 未发现官方代码 | `crpo` |
| Context distillation | [Flux-OPD](2607.28022-flux-opd/README.md) | Peking University，2026-07-30 | 未发现官方代码 | `flux-opd` |
| 多模态证据归因蒸馏 | [VAD](2607.28590-vad/README.md) | Shanghai Jiao Tong University，2026-07-30 | [已开源](https://github.com/DeepExperience/VAD_Multimodal_OPD) | `vad` |
| On-policy self-distillation | [β-OPSD](2607.28582-beta-opsd/README.md) | University of Maryland, College Park，2026-07-30 | 未发现官方代码 | `beta-opsd` |
| 分布保持 RL | [ReCo](2607.26862-reco/README.md) | Seoul National University，2026-07-29 | 未发现官方代码 | `reco-grpo` |
| Rubric RL | [SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning](2607.26873-serpo/README.md) | Authors did not disclose affiliation，2026-07-29 | 未发现官方代码 | `serpo` |
| Token-level credit assignment | [CoRT](2607.25659-cort/README.md) | ByteDance internship，2026-07-28 | 未发现官方代码 | `cort` |
| On-policy distillation | [Relay-OPD](2607.26057-relay-opd/README.md) | Zhejiang University，2026-07-28 | [已开源](https://github.com/ZJU-REAL/Relay-OPD) | `relay-opd` |
| post-training | [Co-Evolving LLM Evaluators and Policies via DynamicRubric](../reproductions/2607.20083-dynamic-rubric/README.md) | WeChat / Tencent，2026-07-22 | 未发现官方代码 | `dynamic-rubric` |
| 过程奖励 | [TCR](2607.19824-tcr/README.md) | 论文未列机构，2026-07-22 | 未发现官方代码 | `tcr` |
| RLVR | [ISO: An RLVR-Native Optimization Stack](2607.19331-iso-rlvr/README.md) | The University of Texas at Austin，2026-07-21 | [已开源](https://github.com/zhuhanqing/ISO) | `iso-rlvr` |
| rlvr | [Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information](../reproductions/2607.19313-off-context-grpo/README.md) | Meta AI，2026-07-21 | [已开源](https://github.com/AgPriyank/OC-GRPO) | `off-context-grpo` |
| 教师奖励重权重 | [Distilled RL](2607.17247-distilled-rl/README.md) | Nankai University，2026-07-19 | [已开源](https://github.com/597358816/Distilled-RL) | `distilled-rl` |
| Reference anchor | [ARMOR](2607.10481-armor/README.md) | University of Science and Technology of China，2026-07-11 | 未发现官方代码 | `armor` |
| 几何信任域 | [RIPO](2607.10169-ripo/README.md) | Tsinghua University，2026-07-11 | 未发现官方代码 | `ripo` |
| Token 信用校准 | [TACO](2607.07976-taco/README.md) | Johns Hopkins University，2026-07-08 | [已开源](https://github.com/xiuyilou/TACO) | `taco` |
| post-training | [Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment](../reproductions/2607.04728-sis/README.md) | Renmin University of China，2026-07-06 | 未发现官方代码 | `sis` |
| 多教师能力整合 | [MOPD](2606.30406-mopd/README.md) | Xiaomi，2026-06-29 | 未发现官方代码 | `mopd` |
| 能力边界课程 | [CoBA-RL](2606.22317-coba-rl/README.md) | Zhejiang University，2026-06-21 | 未发现官方代码 | `coba-rl` |
| Entropy 稳定 | [STARE](2606.19236-stare/README.md) | Tsinghua University，2026-06-17 | [已开源](https://github.com/hp-luo/STARE) | `stare` |
| 异步训推失配 | [KPop](2606.15079-kpop/README.md) | Ling / Ring Team，2026-06-13 | 未发现官方代码 | `kpop` |
| AR-to-Diffusion 蒸馏 | [OPDLM](2606.06712-opd-lm/README.md) | Texas A&M University，2026-06-04 | 未发现官方代码 | `opd-lm` |
| 多目标 RL | [GPRL](2605.18721-gprl/README.md) | Stanford University，2026-05-18 | 未发现官方代码 | `gprl` |
| 对比序列 RL | [ConSPO](2605.12969-conspo/README.md) | Beijing Institute of Technology，2026-05-13 | 未发现官方代码 | `conspo` |
| 异步 off-policy | [Missing Old Logits](2605.12070-missing-old-logits/README.md) | Tianjin University，2026-05-12 | 未发现官方代码 | `missing-old-logits` |
| On-policy distillation | [Lightning OPD](2604.13010-lightning-opd/README.md) | MIT HAN Lab，2026-04-14 | [已开源](https://github.com/jet-ai-projects/Lightning-OPD) | `lightning-opd` |
| Context distillation | [OPCD](2602.12275-opcd/README.md) | Microsoft Research，2026-02-12 | [已开源](https://github.com/microsoft/LMOps/tree/main/opcd) | `opcd` |
| 长度无偏 RL | [LUSPO](2602.05261-luspo/README.md) | Meituan，2026-02-05 | 未发现官方代码 | `luspo` |
| On-policy self-distillation | [OPSD](2601.18734-opsd/README.md) | University of California, Los Angeles，2026-01-26 | [已开源](https://github.com/siyan-zhao/OPSD) | `opsd` |
| 纯在线训推校正 | [Online IcePop](web-2025-online-icepop/README.md) | Ant Group，2025-12-16 | 未发现官方代码 | `online-icepop` |
| 稳定 MoE RL | [Stabilizing RL with LLMs](2512.01374-minirl/README.md) | Alibaba Qwen Team，2025-12-01 | 未发现官方代码 | `minirl` |
| MoE 训推失配 | [IcePop](2510.18855-icepop/README.md) | Ant Group，2025-10-21 | 未发现官方代码 | `icepop` |
| SFT-RL 动态混合 | [CHORD](2508.11408-chord/README.md) | Alibaba Group，2025-08-15 | [已开源](https://github.com/modelscope/Trinity-RFT/tree/main/examples/mix_chord) | `chord` |
| 梯度保留 clip | [GPPO](2508.07629-gppo/README.md) | Alibaba Group，2025-08-11 | 未发现官方代码 | `gppo` |
| 训推失配校正 | [TIS](web-2025-tis/README.md) | University of California, San Diego，2025-08-05 | 未发现官方代码 | `tis` |
| 稳定序列 RL | [GSPO](2507.18071-gspo/README.md) | Alibaba Qwen Team，2025-07-24 | [已开源](https://alibaba.github.io/ROLL/docs/User%20Guides/Algorithms/GSPO/) | `gspo` |
| 自博弈课程 | [SPIRAL](2506.24119-spiral/README.md) | Apple，2025-06-30 | [已开源](https://github.com/spiral-rl/spiral) | `spiral` |
| 长上下文 RL | [CISPO / MiniMax-M1](2506.13585-cispo/README.md) | MiniMax，2025-06-16 | [已开源](https://github.com/MiniMax-AI/MiniMax-M1) | `cispo` |
| 自置信奖励 | [INTUITOR](2505.19590-intuitor/README.md) | University of California, Berkeley，2025-05-26 | [已开源](https://github.com/sunblaze-ucb/Intuitor) | `intuitor` |
| 零数据自博弈 | [Absolute Zero](2505.03335-absolute-zero/README.md) | Tsinghua University，2025-05-06 | [已开源](https://github.com/LeapLabTHU/Absolute-Zero-Reasoner) | `absolute-zero` |
| 测试时强化学习 | [TTRL](2504.16084-ttrl/README.md) | PRIME-RL author team，2025-04-22 | [已开源](https://github.com/PRIME-RL/TTRL) | `ttrl` |
| 离策略推理 RL | [LUFFY](2504.14945-luffy/README.md) | University of Washington，2025-04-21 | [已开源](https://github.com/Simplified-Reasoning/LUFFY) | `luffy` |
| Critic PPO | [VAPO](2504.05118-vapo/README.md) | ByteDance Seed，2025-04-07 | 未发现官方代码 | `vapo` |
| GRPO 聚合偏置 | [Dr. GRPO](2503.20783-dr-grpo/README.md) | SAIL 研究团队，2025-03-26 | [已开源](https://github.com/sail-sg/understand-r1-zero) | `dr-grpo` |
| 长推理 RL | [DAPO](2503.14476-dapo/README.md) | ByteDance Seed，2025-03-18 | [已开源](https://github.com/BytedTsinghua-SIA/DAPO) | `dapo` |
| 全局优势估计 | [REINFORCE++](2501.03262-reinforce-plus/README.md) | Independent researchers，2025-01-04 | 未发现官方代码 | `reinforce-plus` |
| Reference-free 偏好 | [SimPO](2405.14734-simpo/README.md) | Princeton University，2024-05-23 | [已开源](https://github.com/princeton-nlp/SimPO) | `simpo` |
| 单阶段偏好 | [ORPO](2403.07691-orpo/README.md) | KAIST，2024-03-12 | [已开源](https://github.com/xfactlab/orpo) | `orpo` |
| 经典 RLHF | [RLOO](2402.14740-rloo/README.md) | Cohere For AI，2024-02-22 | 未发现官方代码 | `rloo` |
| 在线推理 RL | [DeepSeekMath / GRPO](2402.03300-grpo/README.md) | DeepSeek-AI，2024-02-05 | [已开源](https://github.com/deepseek-ai/DeepSeek-Math) | `grpo` |
| 二元反馈对齐 | [KTO](2402.01306-kto/README.md) | Contextual AI，2024-02-02 | [已开源](https://github.com/ContextualAI/HALOs) | `kto` |
| 自奖励 | [Self-Rewarding LM](2401.10020-self-rewarding/README.md) | Meta AI，2024-01-18 | 未发现官方代码 | `self-rewarding` |
| 自博弈微调 | [SPIN](2401.01335-spin/README.md) | University of California, Los Angeles，2024-01-02 | [已开源](https://github.com/uclaml/SPIN) | `spin` |
| 自动过程奖励 | [Math-Shepherd](2312.08935-math-shepherd/README.md) | Peking University，2023-12-14 | 未发现官方代码 | `math-shepherd` |
| 偏好正则 | [IPO](2310.12036-ipo/README.md) | Google DeepMind，2023-10-18 | 未发现官方代码 | `ipo` |
| 经典 RLHF | [ReMax](2310.10505-remax/README.md) | 香港中文大学（深圳）/ 深圳市大数据研究院，2023-10-16 | [已开源](https://github.com/liziniu/ReMax) | `remax` |
| 多属性可控 SFT | [SteerLM](2310.05344-steerlm/README.md) | NVIDIA，2023-10-09 | [已开源](https://github.com/NVIDIA/NeMo-Aligner) | `steerlm` |
| AI 反馈 | [RLAIF](2309.00267-rlaif/README.md) | Google Research，2023-09-01 | 未发现官方代码 | `rlaif` |
| 经典 On-policy distillation | [GKD](2306.13649-gkd/README.md) | Google DeepMind，2023-06-23 | [已开源](https://github.com/huggingface/trl/blob/main/docs/source/distillation_trainer.md) | `gkd` |
| Reverse-KL distillation | [MiniLLM](2306.08543-minillm/README.md) | Tsinghua University，2023-06-14 | [已开源](https://github.com/microsoft/LMOps/tree/main/minillm) | `minillm` |
| 过程监督 | [Let's Verify Step by Step](2305.20050-process-supervision/README.md) | OpenAI，2023-05-31 | [已开源](https://github.com/openai/prm800k) | `process-supervision` |
| 直接偏好优化 | [DPO](2305.18290-dpo/README.md) | Stanford University，2023-05-29 | [已开源](https://github.com/eric-mitchell/direct-preference-optimization) | `dpo` |
| 序列概率校准 | [SLiC-HF](2305.10425-slic-hf/README.md) | Google DeepMind，2023-05-17 | 未发现官方代码 | `slic-hf` |
| Reward 选优微调 | [RAFT](2304.06767-raft/README.md) | HKUST，2023-04-13 | [已开源](https://github.com/OptimalScale/LMFlow) | `raft` |
| 全排序偏好 | [RRHF](2304.05302-rrhf/README.md) | Alibaba DAMO Academy，2023-04-11 | [已开源](https://github.com/GanjinZero/RRHF) | `rrhf` |
| AI 反馈安全对齐 | [Constitutional AI](2212.08073-constitutional-ai/README.md) | Anthropic，2022-12-15 | [已开源](https://github.com/anthropics/ConstitutionalHarmlessnessPaper) | `constitutional-ai` |
| 经典 RLHF | [InstructGPT / PPO-RLHF](2203.02155-ppo-rlhf/README.md) | OpenAI，2022-03-04 | [已开源](https://github.com/openai/following-instructions-human-feedback) | `ppo-rlhf` |

</div>

分类浏览：

- [按机构/公司/学校](catalog/by-organization.md)
- [按主题](catalog/by-topic.md)
- [按年份](catalog/by-year.md)
