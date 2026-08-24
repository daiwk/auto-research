# 2026-01-01 至 2026-08-24 历史扫描清单与实现批次

> 本页不是把原始关键词命中冒充入选论文。机器可读全集见
> [`2026-historical-candidates.json`](2026-historical-candidates.json)：每个去重后的新候选都保留检索来源、初筛桶和计划状态。

## 漏斗与状态

| 项目 | 数量 |
|---|---:|
| 去重后的新候选 | 3906 |
| 需要全文审查 | 404 |
| 当前 PR 已实现 | 22 |
| 固定后续实现队列 | 52 |
| 仍待全文决定、未承诺实现 | 331 |
| P2 或查询碰撞（保留审计记录） | 3501 |

`fulltext-review-backlog` 不是拒绝。只有核验机构、正文实验、代码状态和与现有实现的增量后，才能晋级后续批次或写入带原因的终态。工业搜广推继续执行量化线上 A/B/明确全流量硬门槛。

## 固定实现批次

### B00：当前 PR 已完成

- [2607.26369](https://arxiv.org/abs/2607.26369) ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling — PR #120 / ClockRoPE
- [2607.27475](https://arxiv.org/abs/2607.27475) OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval — PR #120 / OneShot
- [2607.24789](https://arxiv.org/abs/2607.24789) NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model — PR #120 / NEXT
- [2606.26859](https://arxiv.org/abs/2606.26859) AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems — PR #120 / AgentX

### B01：8 月工业生成推荐与多模态（已完成）

- [2608.21012](https://arxiv.org/abs/2608.21012) From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation — 搜广推与 LLM 应用
- [2608.18322](https://arxiv.org/abs/2608.18322) Multimedia Asset Personalization via Multimodal Embeddings at Netflix — 搜广推与 LLM 应用
- [2608.17613](https://arxiv.org/abs/2608.17613) Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs — 搜广推与 LLM 应用
- [2608.09634](https://arxiv.org/abs/2608.09634) IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation — 搜广推与 LLM 应用
- [2608.07989](https://arxiv.org/abs/2608.07989) PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation — 搜广推与 LLM 应用

### B02：7 月工业生成推荐、Agent harness 与搜索（已完成）

- [2607.29241](https://arxiv.org/abs/2607.29241) RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems — 搜广推与 LLM 应用
- [2607.29213](https://arxiv.org/abs/2607.29213) GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System — 搜广推与 LLM 应用
- [2607.27789](https://arxiv.org/abs/2607.27789) From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation — 搜广推与 LLM 应用
- [2607.14835](https://arxiv.org/abs/2607.14835) LLM-Based Re-Ranking for Real Estate Search — 搜广推与 LLM 应用
- [2607.14418](https://arxiv.org/abs/2607.14418) Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment — 搜广推与 LLM 应用
- [2607.26073](https://arxiv.org/abs/2607.26073) Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap — 搜广推与 LLM 应用
- [2606.31031](https://arxiv.org/abs/2606.31031) GenPage: Towards End-to-End Generative Homepage Construction at Netflix — 搜广推与 LLM 应用

### B03：6–5 月序列建模、生成搜索与多场景排序（已完成）

- [2606.19108](https://arxiv.org/abs/2606.19108) JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling — 搜广推与 LLM 应用
- [2605.26717](https://arxiv.org/abs/2605.26717) L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation — 搜广推与 LLM 应用
- [2605.25514](https://arxiv.org/abs/2605.25514) From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark — 搜广推与 LLM 应用
- [2605.23702](https://arxiv.org/abs/2605.23702) TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery — 搜广推与 LLM 应用
- [2605.21752](https://arxiv.org/abs/2605.21752) PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation — 搜广推与 LLM 应用
- [2605.17863](https://arxiv.org/abs/2605.17863) DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems — 搜广推与 LLM 应用

### B04：推荐 RL、知识迁移与 Semantic ID

- [2605.16344](https://arxiv.org/abs/2605.16344) A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems — 搜广推与 LLM 应用
- [2605.05730](https://arxiv.org/abs/2605.05730) Effective Knowledge Transfer for Multi-Task Recommendation Models — 搜广推与 LLM 应用
- [2604.23522](https://arxiv.org/abs/2604.23522) Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale — 搜广推与 LLM 应用
- [2604.12234](https://arxiv.org/abs/2604.12234) UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute — 搜广推与 LLM 应用
- [2603.24226](https://arxiv.org/abs/2603.24226) UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking — 搜广推与 LLM 应用
- [2603.22916](https://arxiv.org/abs/2603.22916) GateSID: Adaptive Gating for Balancing Semantic and Collaborative Signals in Recommendation — 搜广推与 LLM 应用

### B05：电商生成、搜索融合与工业排序

- [2603.19710](https://arxiv.org/abs/2603.19710) AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation — 搜广推与 LLM 应用
- [2603.19585](https://arxiv.org/abs/2603.19585) SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search — 搜广推与 LLM 应用
- [2603.03988](https://arxiv.org/abs/2603.03988) SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders — 搜广推与 LLM 应用
- [2603.00632](https://arxiv.org/abs/2603.00632) Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale — 搜广推与 LLM 应用
- [2602.20995](https://arxiv.org/abs/2602.20995) Generative Pseudo-Labeling for Pre-Ranking with LLMs — 搜广推与 LLM 应用
- [2602.17058](https://arxiv.org/abs/2602.17058) A Long-term Value Prediction Framework In Video Ranking — 搜广推与 LLM 应用

### B06：2 月召回、广告、长序列与 LLM 排序

- [2602.12968](https://arxiv.org/abs/2602.12968) RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems — 搜广推与 LLM 应用
- [2602.12354](https://arxiv.org/abs/2602.12354) An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking — 搜广推与 LLM 应用
- [2602.11410](https://arxiv.org/abs/2602.11410) CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer — 搜广推与 LLM 应用
- [2602.09744](https://arxiv.org/abs/2602.09744) DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation — 搜广推与 LLM 应用
- [2602.09401](https://arxiv.org/abs/2602.09401) SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking — 搜广推与 LLM 应用
- [2602.09194](https://arxiv.org/abs/2602.09194) ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest — 搜广推与 LLM 应用
- [2602.01023](https://arxiv.org/abs/2602.01023) Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment — 搜广推与 LLM 应用

### B07：LLM 架构、长上下文、KV cache 与评测基础设施

- [2608.12831](https://arxiv.org/abs/2608.12831) Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing — LLM 后训练、搜广推与 LLM 应用
- [2608.10296](https://arxiv.org/abs/2608.10296) Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension — 基础模型
- [2608.08878](https://arxiv.org/abs/2608.08878) DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference — 基础模型、LLM 后训练
- [2608.06849](https://arxiv.org/abs/2608.06849) Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry — 基础模型
- [2608.05000](https://arxiv.org/abs/2608.05000) Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes — 基础模型
- [2608.01672](https://arxiv.org/abs/2608.01672) Learning What to Remember: Test-Time Training via Context Distillation — 基础模型
- [2608.02032](https://arxiv.org/abs/2608.02032) DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling — 基础模型
- [2607.29032](https://arxiv.org/abs/2607.29032) TransMem: Transforming Hidden States into Memory for Large Language Models — Agent、基础模型
- [2607.17715](https://arxiv.org/abs/2607.17715) C$^2$KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference — 基础模型

### B08：OPD 与多教师/过程蒸馏

- [2608.19408](https://arxiv.org/abs/2608.19408) Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress — LLM 后训练
- [2608.09745](https://arxiv.org/abs/2608.09745) SR-OPSD: Self-Referenced On-Policy Self-Distillation — LLM 后训练
- [2608.05802](https://arxiv.org/abs/2608.05802) On-Policy Delta Distillation for Multilingual Math Reasoning — LLM 后训练
- [2608.03673](https://arxiv.org/abs/2608.03673) CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning — LLM 后训练
- [2608.03092](https://arxiv.org/abs/2608.03092) SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation — LLM 后训练
- [2608.00782](https://arxiv.org/abs/2608.00782) Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance — LLM 后训练

### B09：Rubric、外部 rollout 与多奖励 RL

- [2608.16072](https://arxiv.org/abs/2608.16072) Learn What's Left, Not What's Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization — LLM 后训练
- [2608.11669](https://arxiv.org/abs/2608.11669) Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL — LLM 后训练
- [2608.01717](https://arxiv.org/abs/2608.01717) Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models — LLM 后训练
- [2607.28026](https://arxiv.org/abs/2607.28026) Contrastive Reinforced Policy Optimization via Privileged Self-Distillation — Agent、LLM 后训练
- [2607.26873](https://arxiv.org/abs/2607.26873) SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning — LLM 后训练
- [2607.19331](https://arxiv.org/abs/2607.19331) ISO: An RLVR-Native Optimization Stack — LLM 后训练

### B10：Agentic RL 与长时序 credit assignment

- [2608.19842](https://arxiv.org/abs/2608.19842) SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning — Agent
- [2608.19197](https://arxiv.org/abs/2608.19197) SPADE: Self-Play in Adaptive Synthetic Executable Environments — Agent、LLM 后训练
- [2608.18682](https://arxiv.org/abs/2608.18682) RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training — Agent
- [2608.17289](https://arxiv.org/abs/2608.17289) PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs — Agent
- [2608.16156](https://arxiv.org/abs/2608.16156) TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents — Agent
- [2608.11967](https://arxiv.org/abs/2608.11967) LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation — Agent、基础模型、LLM 后训练

### B11：Agent 记忆、工具规划与自进化系统

- [2608.15703](https://arxiv.org/abs/2608.15703) HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation — Agent
- [2608.09380](https://arxiv.org/abs/2608.09380) OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks — Agent
- [2608.06811](https://arxiv.org/abs/2608.06811) Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution — Agent
- [2608.03468](https://arxiv.org/abs/2608.03468) ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning — Agent
- [2608.02650](https://arxiv.org/abs/2608.02650) HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents — Agent
- [2607.28527](https://arxiv.org/abs/2607.28527) MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems — Agent

## 全部 404 个全文审查候选

状态含义：`Bxx` 为固定实现批次；`B00` 已完成；`待全文` 表示尚未承诺实现，但不会从账本消失。

| 日期 | 领域 | 论文 | 初筛 | 计划 |
|---|---|---|---|---|
| 2026-08-21 | Agent | [2608.21101](https://arxiv.org/abs/2608.21101) ClawSentry: A Progressive Multi-Tier Security Monitor for Safeguarding Autonomous LLM Agents | manual-review | 待全文 |
| 2026-08-21 | 基础模型 | [2608.21030](https://arxiv.org/abs/2608.21030) COMET: Contrastive Motion-Enhanced Temporal Reasoning for Video Multimodal Large Language Models | manual-review | 待全文 |
| 2026-08-21 | 搜广推与 LLM 应用 | [2608.21012](https://arxiv.org/abs/2608.21012) From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation | industrial-fulltext-review | B01 |
| 2026-08-21 | Agent | [2608.20844](https://arxiv.org/abs/2608.20844) TRACE: Agentic Catalog Enrichment with Multi-source Evidence Grounding | manual-review | 待全文 |
| 2026-08-21 | Agent | [2608.20631](https://arxiv.org/abs/2608.20631) Weighted Memory Tree: Remembering What Matters for Long-Horizon LLM Agents | manual-review | 待全文 |
| 2026-08-20 | 基础模型 / LLM 后训练 | [2608.20331](https://arxiv.org/abs/2608.20331) G-CARL: Grounded Checklist-Aligned Reward Learning for Patient-Oriented Medical Report Interpretation | manual-review, p2-deferred-review | 待全文 |
| 2026-08-20 | 基础模型 | [2608.20315](https://arxiv.org/abs/2608.20315) Explainable Transformer Models for Clinical Prediction Tasks on Structured Electronic Health Records | manual-review | 待全文 |
| 2026-08-20 | Agent | [2608.20314](https://arxiv.org/abs/2608.20314) MidTool: Mid-training Data Synthesis for Agentic Tool Use | manual-review | 待全文 |
| 2026-08-20 | Agent | [2608.19842](https://arxiv.org/abs/2608.19842) SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning | manual-review | B10 |
| 2026-08-20 | Agent / LLM 后训练 | [2608.19803](https://arxiv.org/abs/2608.19803) MileGPO: Milestone Inference with Local Evidence for Graph-Based Policy Optimization of Long-Horizon LLM Agents | manual-review, p2-deferred-review | 待全文 |
| 2026-08-20 | Agent / 基础模型 | [2608.19662](https://arxiv.org/abs/2608.19662) ReCache: Efficient KV Cache Reuse and Compression for Tool-Augmented LLM Agents | manual-review, p2-deferred-review | 待全文 |
| 2026-08-20 | Agent | [2608.19564](https://arxiv.org/abs/2608.19564) Remember, Verify, or Ask? Cross-Family Evaluation of Memory Commitment in LLM Agents | manual-review | 待全文 |
| 2026-08-19 | LLM 后训练 | [2608.19408](https://arxiv.org/abs/2608.19408) Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress | manual-review | B08 |
| 2026-08-19 | 基础模型 | [2608.19395](https://arxiv.org/abs/2608.19395) HYDRA: A Heterogeneous Chiplet DSE Framework for Serving Dynamic Hybrid LLM Workloads | manual-review | 待全文 |
| 2026-08-19 | Agent / LLM 后训练 | [2608.19197](https://arxiv.org/abs/2608.19197) SPADE: Self-Play in Adaptive Synthetic Executable Environments | manual-review, p2-deferred-review | B10 |
| 2026-08-19 | Agent | [2608.18884](https://arxiv.org/abs/2608.18884) Training-Free Inference-Time Self-Reflection and Cost-Bounded Early Stopping for Large Language Models | manual-review | 待全文 |
| 2026-08-19 | 基础模型 | [2608.18733](https://arxiv.org/abs/2608.18733) Flama: a Python framework for development and deployment of production-ready APIs, machine learning, and LLM services | manual-review | 待全文 |
| 2026-08-19 | Agent | [2608.18682](https://arxiv.org/abs/2608.18682) RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training | manual-review | B10 |
| 2026-08-19 | 基础模型 | [2608.18656](https://arxiv.org/abs/2608.18656) FlashAttention for Scalable Vector Architectures | manual-review | 待全文 |
| 2026-08-19 | 搜广推与 LLM 应用 | [2608.18637](https://arxiv.org/abs/2608.18637) PILOT Technical Report | manual-review | 待全文 |
| 2026-08-19 | 基础模型 | [2608.18628](https://arxiv.org/abs/2608.18628) When Safety Overrides Vision: Exploring Dynamics between Vision Influence and Safety Alignment in Vision-Language Models | manual-review | 待全文 |
| 2026-08-19 | 基础模型 / LLM 后训练 | [2608.18578](https://arxiv.org/abs/2608.18578) Compress and Forget: bitsandbytes Quantization Amplifies Proactive Interference in LLMs | manual-review, p2-deferred-review | 待全文 |
| 2026-08-19 | Agent | [2608.18423](https://arxiv.org/abs/2608.18423) FM-Bench: A Benchmark for Long-Horizon Management with Competing Agents | manual-review | 待全文 |
| 2026-08-18 | 搜广推与 LLM 应用 | [2608.18322](https://arxiv.org/abs/2608.18322) Multimedia Asset Personalization via Multimodal Embeddings at Netflix | industrial-fulltext-review | B01 |
| 2026-08-18 | Agent / 基础模型 / LLM 后训练 | [2608.18008](https://arxiv.org/abs/2608.18008) Policy-Invariant Reward Shaping from LLM Feedback: A Framework for Hybrid RL Agents | manual-review, p2-deferred-review | 待全文 |
| 2026-08-18 | 基础模型 | [2608.17950](https://arxiv.org/abs/2608.17950) Do Large Language Models Play Six Degrees of Separation? Measuring Topological Compression in Long-Context Manifolds | manual-review | 待全文 |
| 2026-08-18 | 搜广推与 LLM 应用 | [2608.17613](https://arxiv.org/abs/2608.17613) Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs | industrial-fulltext-review | B01 |
| 2026-08-18 | Agent / LLM 后训练 | [2608.17524](https://arxiv.org/abs/2608.17524) Evaluating RL Explainability Methods by How Much They Help Fix Bugs in Agents | manual-review, p2-deferred-review | 待全文 |
| 2026-08-18 | 搜广推与 LLM 应用 | [2608.17316](https://arxiv.org/abs/2608.17316) Empowering Compact LLMs with Fusion of Layer-wise Exits for Recommendation | manual-review | 待全文 |
| 2026-08-18 | Agent | [2608.17289](https://arxiv.org/abs/2608.17289) PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs | manual-review | B10 |
| 2026-08-17 | Agent / 基础模型 | [2608.17209](https://arxiv.org/abs/2608.17209) Teach and Grow: An Agent-Centered Architecture for General Robot Learning | manual-review, p2-deferred-review | 待全文 |
| 2026-08-17 | Agent / 基础模型 | [2608.18171](https://arxiv.org/abs/2608.18171) Looped Language Models Improve Compositional Tool Calling | manual-review, p2-deferred-review | 待全文 |
| 2026-08-17 | Agent / 基础模型 | [2608.16889](https://arxiv.org/abs/2608.16889) Don't Drop the BATON: Long-Horizon Robot Manipulation via Agentic Subtask Exploration and Transition-aware Memory | manual-review, p2-deferred-review | 待全文 |
| 2026-08-17 | 基础模型 | [2608.16844](https://arxiv.org/abs/2608.16844) Proteus: Incremental Memory Activation for Long-Context Sequence Modeling | manual-review | 待全文 |
| 2026-08-17 | 基础模型 | [2608.16514](https://arxiv.org/abs/2608.16514) Matched Outcomes, Divergent Gaze: How Foveated MLLMs Search Compared to Humans | manual-review | 待全文 |
| 2026-08-17 | Agent | [2608.16447](https://arxiv.org/abs/2608.16447) HaReCAP: Habitual-action Grounding for Recursive Large Language Model Agents | manual-review | 待全文 |
| 2026-08-17 | 基础模型 / LLM 后训练 | [2608.16419](https://arxiv.org/abs/2608.16419) PertMind: Eliciting Emergent Biological Reasoning in LLM via Reinforcement Learning on Cellular Perturbation Data | manual-review, p2-deferred-review | 待全文 |
| 2026-08-17 | 基础模型 / LLM 后训练 | [2608.16316](https://arxiv.org/abs/2608.16316) Deep Thought Alignment: Trajectory-Level Latent Distillation for Video Reasoning | manual-review, p2-deferred-review | 待全文 |
| 2026-08-17 | Agent / 基础模型 | [2608.16168](https://arxiv.org/abs/2608.16168) QUMem: Personalized Memory for Query-Conditioned User-State Inference in LLM Agents | manual-review, p2-deferred-review | 待全文 |
| 2026-08-17 | Agent | [2608.16156](https://arxiv.org/abs/2608.16156) TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents | manual-review | B10 |
| 2026-08-17 | LLM 后训练 | [2608.16072](https://arxiv.org/abs/2608.16072) Learn What's Left, Not What's Mastered: Saturation Aware Advantage Reweighting for Multi-Reward Policy Optimization | manual-review | B09 |
| 2026-08-16 | 基础模型 | [2608.15962](https://arxiv.org/abs/2608.15962) SEER: Long-Context Reasoning via Selective Visual-Text Compression | manual-review | 待全文 |
| 2026-08-16 | Agent / LLM 后训练 / 搜广推与 LLM 应用 | [2608.15949](https://arxiv.org/abs/2608.15949) Ask to Be Sure: Informative Interactions for Confident Multi-Turn LLM Recommendation | manual-review | 待全文 |
| 2026-08-16 | Agent | [2608.15703](https://arxiv.org/abs/2608.15703) HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation | manual-review | B11 |
| 2026-08-16 | 基础模型 / LLM 后训练 | [2608.15602](https://arxiv.org/abs/2608.15602) FluxBin: Flexible LUT-based Ultra-low-bit LLM Inference by Algorithm-Kernel Synergy | manual-review, p2-deferred-review | 待全文 |
| 2026-08-16 | Agent | [2608.15579](https://arxiv.org/abs/2608.15579) Kozuchi Agent: A Language-Agnostic Open-Weight Agent for Software Repair | manual-review | 待全文 |
| 2026-08-15 | Agent | [2608.15175](https://arxiv.org/abs/2608.15175) LAPF: LLM-Agent-Based Path Finder Using the UAVScenes Dataset | manual-review | 待全文 |
| 2026-08-15 | Agent / 基础模型 | [2608.15032](https://arxiv.org/abs/2608.15032) Handoff-H1: An Orchestrated Vision-Agent System for Material Quantity Takeoff from Construction Blueprints | manual-review, p2-deferred-review | 待全文 |
| 2026-08-15 | Agent | [2608.15016](https://arxiv.org/abs/2608.15016) Hierarchical Agentic Incident Response with Digital-Twin-Validated Attack Inference | manual-review | 待全文 |
| 2026-08-14 | 基础模型 | [2608.14198](https://arxiv.org/abs/2608.14198) MINT: A Universal Zero-Shot Predictor for Transaction Data | manual-review | 待全文 |
| 2026-08-14 | Agent / 搜广推与 LLM 应用 | [2608.14068](https://arxiv.org/abs/2608.14068) MACS: A Hybrid Multi-Agent Framework for Reliable Conversational E-Commerce Recommendation | manual-review | 待全文 |
| 2026-08-14 | Agent / 基础模型 | [2608.13900](https://arxiv.org/abs/2608.13900) Agentic Transaction: Towards ACID-Compliant Agent Systems | manual-review, p2-deferred-review | 待全文 |
| 2026-08-14 | LLM 后训练 | [2608.13854](https://arxiv.org/abs/2608.13854) Bootstrapping Niche Multilingual Code Translation via Reinforcement Learning with Execution-Based Verifiable Supervision | manual-review | 待全文 |
| 2026-08-13 | Agent | [2608.13681](https://arxiv.org/abs/2608.13681) Fine-Tuning Qwen3-27B for C-to-Rust Code Translation: A Three-Stage Curriculum of Pretraining, Debugging-Aware SFT, and Task-Specific SFT | manual-review | 待全文 |
| 2026-08-13 | Agent / 基础模型 / LLM 后训练 | [2608.13505](https://arxiv.org/abs/2608.13505) Intern-S2-Preview: Scientific Agentic Foundation Model | manual-review, p2-deferred-review | 待全文 |
| 2026-08-13 | Agent / 基础模型 | [2608.13463](https://arxiv.org/abs/2608.13463) MLLM-Routed Heterogeneous Ensembles for Robust Cross-Dataset Image Classification | manual-review, p2-deferred-review | 待全文 |
| 2026-08-13 | 基础模型 | [2608.13426](https://arxiv.org/abs/2608.13426) Reduced Matrix Multiplication: Input-Adaptive Matrix-Product Reduction for LLM Inference | manual-review | 待全文 |
| 2026-08-13 | Agent | [2608.13317](https://arxiv.org/abs/2608.13317) StateBridge: Training-free Hidden-state Alignment for Latent Communication in LLM Multi-Agent Systems | manual-review | 待全文 |
| 2026-08-13 | 搜广推与 LLM 应用 | [2608.12986](https://arxiv.org/abs/2608.12986) STAR: Structured Tokenization and Target-Aware Interest Representation for PCVR Prediction | manual-review | 待全文 |
| 2026-08-13 | LLM 后训练 / 搜广推与 LLM 应用 | [2608.12831](https://arxiv.org/abs/2608.12831) Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing | industrial-fulltext-review, query-collision | B07 |
| 2026-08-13 | 搜广推与 LLM 应用 | [2608.12778](https://arxiv.org/abs/2608.12778) DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation | industrial-fulltext-review | 待全文 |
| 2026-08-12 | 基础模型 | [2608.12099](https://arxiv.org/abs/2608.12099) RT-SEMamba: Real-Time Speech Enhancement Mamba via Progressive Knowledge Distillation | manual-review | 待全文 |
| 2026-08-12 | 搜广推与 LLM 应用 | [2608.11973](https://arxiv.org/abs/2608.11973) Sci-Surf: Navigating Scientific Literature Discovery through Human Feedback and Intelligent Summarization | manual-review | 待全文 |
| 2026-08-12 | Agent / 基础模型 / LLM 后训练 | [2608.11967](https://arxiv.org/abs/2608.11967) LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation | manual-review, p2-deferred-review | B10 |
| 2026-08-12 | LLM 后训练 | [2608.11715](https://arxiv.org/abs/2608.11715) When the API Speaks the Wrong Language: Revisiting Post-Training for Multilingual Tool Use | manual-review | 待全文 |
| 2026-08-12 | LLM 后训练 | [2608.11669](https://arxiv.org/abs/2608.11669) Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL | manual-review | B09 |
| 2026-08-11 | LLM 后训练 | [2608.11350](https://arxiv.org/abs/2608.11350) Self-Evolving Embodied Agents via Skill-Harness Evolution | manual-review | 待全文 |
| 2026-08-11 | Agent / LLM 后训练 | [2608.11191](https://arxiv.org/abs/2608.11191) Test-Time Self-Evolving GUI Visual Grounding via Reflection-Guided On-Policy Self-Distillation | manual-review, p2-deferred-review | 待全文 |
| 2026-08-11 | Agent / 基础模型 / LLM 后训练 | [2608.11152](https://arxiv.org/abs/2608.11152) Scheduling Mixed RL Rollouts Beyond Prefix Locality | manual-review, p2-deferred-review | 待全文 |
| 2026-08-11 | 基础模型 | [2608.10908](https://arxiv.org/abs/2608.10908) Order Matters: LVLMs as Judges for Temporal Reasoning in Image Sequences | manual-review | 待全文 |
| 2026-08-11 | LLM 后训练 | [2608.10812](https://arxiv.org/abs/2608.10812) Reference-Free Post-Training of Open Large Language Models for Multilingual Machine Translation | manual-review | 待全文 |
| 2026-08-11 | Agent | [2608.10530](https://arxiv.org/abs/2608.10530) On Understanding, Identifying, and Mitigating Vulnerabilities in Agentic Large Language Models | manual-review | 待全文 |
| 2026-08-11 | 搜广推与 LLM 应用 | [2608.10447](https://arxiv.org/abs/2608.10447) Towards Efficient Reasoning in LLM-Based Recommender Systems via Model Merging | manual-review | 待全文 |
| 2026-08-11 | Agent / 基础模型 | [2608.10430](https://arxiv.org/abs/2608.10430) Actionable Hallucination Detection: Translating Latent Uncertainty into Agentic Critique | manual-review, p2-deferred-review | 待全文 |
| 2026-08-10 | 基础模型 | [2608.10296](https://arxiv.org/abs/2608.10296) Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension | manual-review | B07 |
| 2026-08-10 | 基础模型 / LLM 后训练 / 搜广推与 LLM 应用 | [2608.10182](https://arxiv.org/abs/2608.10182) From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation | industrial-fulltext-review, p2-deferred-review, query-collision | 待全文 |
| 2026-08-10 | Agent / LLM 后训练 | [2608.10126](https://arxiv.org/abs/2608.10126) Procedural Fairness Failures in RLHF from Preference Averaging | manual-review, p2-deferred-review | 待全文 |
| 2026-08-10 | LLM 后训练 | [2608.10090](https://arxiv.org/abs/2608.10090) CHORUS: Complementary Experts for High-Coverage Testbench Stimulus Generation | manual-review | 待全文 |
| 2026-08-10 | LLM 后训练 | [2608.09745](https://arxiv.org/abs/2608.09745) SR-OPSD: Self-Referenced On-Policy Self-Distillation | manual-review | B08 |
| 2026-08-10 | 搜广推与 LLM 应用 | [2608.09634](https://arxiv.org/abs/2608.09634) IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation | industrial-fulltext-review | B01 |
| 2026-08-10 | 搜广推与 LLM 应用 | [2608.09605](https://arxiv.org/abs/2608.09605) TSPORec: Token Selection via Preference Optimization for LLM-Based Sequential Recommendation | manual-review | 待全文 |
| 2026-08-10 | Agent | [2608.09380](https://arxiv.org/abs/2608.09380) OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks | manual-review | B11 |
| 2026-08-10 | LLM 后训练 | [2608.09217](https://arxiv.org/abs/2608.09217) Beyond Solvability: Task Learnability as a Static Prior for LLM RL Post-Training | manual-review | 待全文 |
| 2026-08-10 | Agent | [2608.09119](https://arxiv.org/abs/2608.09119) Motif 3: Technical Report | manual-review | 待全文 |
| 2026-08-09 | 基础模型 / LLM 后训练 | [2608.08878](https://arxiv.org/abs/2608.08878) DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference | manual-review, p2-deferred-review | B07 |
| 2026-08-09 | 基础模型 / LLM 后训练 | [2608.08744](https://arxiv.org/abs/2608.08744) Can We Optimize the Performance-Carbon Emission Break-Even Point?: The Quest for Greener LLMs | manual-review, query-collision | 待全文 |
| 2026-08-08 | 基础模型 | [2608.08081](https://arxiv.org/abs/2608.08081) RotaryQuant: Fitting 120B MoE Models on Consumer Hardware via Fused Compressed-Space Attention | manual-review | 待全文 |
| 2026-08-08 | 搜广推与 LLM 应用 | [2608.07989](https://arxiv.org/abs/2608.07989) PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation | industrial-fulltext-review | B01 |
| 2026-08-07 | 基础模型 / 搜广推与 LLM 应用 | [2608.07816](https://arxiv.org/abs/2608.07816) Preserving Item Semantics for Free: Rethinking Token Initialization in LLM-Based Generative Recommendation | manual-review, p2-deferred-review | 待全文 |
| 2026-08-07 | 搜广推与 LLM 应用 | [2608.10008](https://arxiv.org/abs/2608.10008) Do LLM Recommenders Know When They're Hallucinating? Auditing Confidence Calibration in Catalog Faithfulness | manual-review | 待全文 |
| 2026-08-07 | Agent / LLM 后训练 | [2608.07418](https://arxiv.org/abs/2608.07418) ResidencyRL: Reinforcement Learning in Simulated Clinical Environments | manual-review, p2-deferred-review | 待全文 |
| 2026-08-07 | 基础模型 | [2608.07193](https://arxiv.org/abs/2608.07193) An AI4AI Framework for Visual Token Pruning | manual-review | 待全文 |
| 2026-08-07 | 搜广推与 LLM 应用 | [2608.07055](https://arxiv.org/abs/2608.07055) Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation | industrial-fulltext-review | 待全文 |
| 2026-08-07 | 基础模型 | [2608.06901](https://arxiv.org/abs/2608.06901) Prune Once: Retraining-Free Task-Agnostic Pruning for Vision-Language Models | manual-review | 待全文 |
| 2026-08-07 | 基础模型 | [2608.06849](https://arxiv.org/abs/2608.06849) Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry | manual-review | B07 |
| 2026-08-07 | Agent | [2608.06811](https://arxiv.org/abs/2608.06811) Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution | manual-review | B11 |
| 2026-08-07 | 搜广推与 LLM 应用 | [2608.06792](https://arxiv.org/abs/2608.06792) Progressive Alignment of Recommender Foundation Model through Multi-Phase Post-Training | industrial-fulltext-review | 待全文 |
| 2026-08-06 | LLM 后训练 | [2608.06526](https://arxiv.org/abs/2608.06526) GRASP: Reinforcing Language Model Anonymizers with Group Relative Policy Optimization | manual-review | 待全文 |
| 2026-08-06 | Agent | [2608.06474](https://arxiv.org/abs/2608.06474) WebGrader: Training LLMs for Web Development with Self-Evolving Programmatic Grader | manual-review | 待全文 |
| 2026-08-06 | 搜广推与 LLM 应用 | [2608.06068](https://arxiv.org/abs/2608.06068) Cleo: A Transparent and Controllable Chatbot for Conversational Commerce | manual-review | 待全文 |
| 2026-08-06 | LLM 后训练 | [2608.05802](https://arxiv.org/abs/2608.05802) On-Policy Delta Distillation for Multilingual Math Reasoning | manual-review | B08 |
| 2026-08-06 | Agent | [2608.05792](https://arxiv.org/abs/2608.05792) When Agentic AI Meets Integrated Sensing and Communication | manual-review | 待全文 |
| 2026-08-06 | 搜广推与 LLM 应用 | [2608.05655](https://arxiv.org/abs/2608.05655) Is Personalized Modality Weighting Actually Personalized? A Controlled Audit of Per-User Weighting Claims in Multimodal Recommenders | priority-fulltext-review | 待全文 |
| 2026-08-05 | 搜广推与 LLM 应用 | [2608.07593](https://arxiv.org/abs/2608.07593) Weather- and Location-Aware Agentic Dining Recommendation: Leveraging LLM World Knowledge for Region-Sensitive Contextual Reasoning | priority-fulltext-review | 待全文 |
| 2026-08-05 | 基础模型 | [2608.05000](https://arxiv.org/abs/2608.05000) Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes | manual-review | B07 |
| 2026-08-05 | 搜广推与 LLM 应用 | [2608.04807](https://arxiv.org/abs/2608.04807) WatchLens: A Configurable Platform for Online Video Recommendation Experiments | industrial-fulltext-review | 待全文 |
| 2026-08-05 | 基础模型 | [2608.04678](https://arxiv.org/abs/2608.04678) Kathleen Writes: Autoregressive Generation and Data Scaling Without Attention | manual-review | 待全文 |
| 2026-08-05 | LLM 后训练 | [2608.04646](https://arxiv.org/abs/2608.04646) Evaluating Theory of Mind in Reasoning Models: Robustness over Reasoning | manual-review | 待全文 |
| 2026-08-04 | 基础模型 | [2608.03930](https://arxiv.org/abs/2608.03930) Logic Before Language: Pre-pretraining on Formal Derivations Fosters Skill Acquisition and Compressibility | manual-review | 待全文 |
| 2026-08-04 | 搜广推与 LLM 应用 | [2608.03899](https://arxiv.org/abs/2608.03899) ATLAS: Learning to Recommend Across Unseen Domains | manual-review | 待全文 |
| 2026-08-04 | 基础模型 | [2608.03855](https://arxiv.org/abs/2608.03855) Bi-semantic Chemical Embedder for Joint Representation Learning of SMILES and Natural Language | manual-review | 待全文 |
| 2026-08-04 | Agent | [2608.03800](https://arxiv.org/abs/2608.03800) Autoreflection: How Agentic Strange Loops Turn Human Culture into AI Infrastructure | manual-review | 待全文 |
| 2026-08-04 | 搜广推与 LLM 应用 | [2608.03722](https://arxiv.org/abs/2608.03722) When Outputs Disperse, Does Epistemic Revision Follow? A Black-Box Diagnostic for Machine Collectives | priority-fulltext-review | 待全文 |
| 2026-08-04 | LLM 后训练 | [2608.03673](https://arxiv.org/abs/2608.03673) CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning | manual-review | B08 |
| 2026-08-04 | 搜广推与 LLM 应用 | [2608.03659](https://arxiv.org/abs/2608.03659) How Closely Do LLM Reviews Align with Human Peer Review? | priority-fulltext-review | 待全文 |
| 2026-08-04 | LLM 后训练 | [2608.03545](https://arxiv.org/abs/2608.03545) Hi-TTRL: Regulating Consensus with Hints for Test-Time Reinforcement Learning | manual-review | 待全文 |
| 2026-08-04 | Agent / 基础模型 / LLM 后训练 | [2608.03502](https://arxiv.org/abs/2608.03502) Hybrid LLM-Augmented Reinforcement Learning Agents for Complex Sequential Decision Tasks | manual-review, p2-deferred-review | 待全文 |
| 2026-08-04 | Agent | [2608.03468](https://arxiv.org/abs/2608.03468) ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning | manual-review | B11 |
| 2026-08-04 | 基础模型 | [2608.11249](https://arxiv.org/abs/2608.11249) Diffuse to Compress: Leveraging Diffusion LMs for Lossless Compression | manual-review | 待全文 |
| 2026-08-04 | 搜广推与 LLM 应用 | [2608.03272](https://arxiv.org/abs/2608.03272) Attacking and Defending Multi-Agent Collaborative Filtering Systems Through Connectivity | manual-review | 待全文 |
| 2026-08-04 | LLM 后训练 | [2608.03204](https://arxiv.org/abs/2608.03204) Aligning Large Vision-Language Models at Test Time: A Trajectory-Guided Structured Sampling Approach | manual-review | 待全文 |
| 2026-08-04 | LLM 后训练 | [2608.03092](https://arxiv.org/abs/2608.03092) SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation | manual-review | B08 |
| 2026-08-04 | LLM 后训练 | [2608.03077](https://arxiv.org/abs/2608.03077) PAMT: Process-Aligned Reinforcement Learning for Multi-Domain Machine Translation | manual-review | 待全文 |
| 2026-08-04 | 基础模型 / LLM 后训练 | [2608.03048](https://arxiv.org/abs/2608.03048) PI-Mem: Pushing Long-Context Reasoning to 3.6M Tokens with Parallel-Iterative Memory | manual-review, p2-deferred-review | 待全文 |
| 2026-08-03 | 基础模型 / LLM 后训练 | [2608.02867](https://arxiv.org/abs/2608.02867) BODHI: Do LLMs Branch Out and Discover Heterogeneous Inferences? | manual-review, p2-deferred-review | 待全文 |
| 2026-08-03 | LLM 后训练 | [2608.02831](https://arxiv.org/abs/2608.02831) Reinforcement Learning with Evolving Rubrics as Rewards for Audio Reasoning | manual-review | 待全文 |
| 2026-08-03 | 基础模型 | [2608.02560](https://arxiv.org/abs/2608.02560) Structured Memory for Edge Language Models: Persistent Context and Corpus Retrieval via O(1) SSM State Injection | manual-review | 待全文 |
| 2026-08-03 | Agent / LLM 后训练 | [2608.02391](https://arxiv.org/abs/2608.02391) Cooperative Coevolution for Resource-Constrained Agentic LLM Post-Training | manual-review, p2-deferred-review | 待全文 |
| 2026-08-03 | LLM 后训练 | [2608.02139](https://arxiv.org/abs/2608.02139) Self-Improving Large Language Models via Progressive Experience Evolution | manual-review | 待全文 |
| 2026-08-03 | 基础模型 / LLM 后训练 | [2608.02110](https://arxiv.org/abs/2608.02110) IACM-RL: Intent-Aware Context Management and Reinforcement Learning for Complex Tool Invocation under Dynamic Intent Fluctuations | manual-review, p2-deferred-review | 待全文 |
| 2026-08-03 | LLM 后训练 | [2608.02087](https://arxiv.org/abs/2608.02087) Instruction-Conditioned Exploration for Reinforcement Learning with Self-Distillation to an Unconditioned Policy | manual-review | 待全文 |
| 2026-08-03 | 基础模型 | [2608.02032](https://arxiv.org/abs/2608.02032) DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling | manual-review | B07 |
| 2026-08-03 | 基础模型 | [2608.02031](https://arxiv.org/abs/2608.02031) Learning-Based Collaborative MEC for LLM Inference with Soft-Deadline Awareness via Transformer-Enhanced PPO | manual-review | 待全文 |
| 2026-08-03 | LLM 后训练 | [2608.01804](https://arxiv.org/abs/2608.01804) LEAP: Lean Environment-Feedback via Adaptive Pruning for Code RL in GPU Kernel Generation | manual-review | 待全文 |
| 2026-08-03 | 搜广推与 LLM 应用 | [2608.01732](https://arxiv.org/abs/2608.01732) X-KGRank: A Knowledge Graph RAG Framework for Explainable Recommendations via Pattern Mining and LLM Re-Ranking | manual-review | 待全文 |
| 2026-08-03 | Agent | [2608.01719](https://arxiv.org/abs/2608.01719) MNC: Scope-Bound Semantic Declassification for Private LLM-Agent Communication | manual-review | 待全文 |
| 2026-08-03 | LLM 后训练 | [2608.01717](https://arxiv.org/abs/2608.01717) Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models | manual-review | B09 |
| 2026-08-03 | Agent | [2608.01684](https://arxiv.org/abs/2608.01684) GABench: A Comprehensive Benchmark for Evaluating LLM Agents on Graph Analysis Tasks | manual-review | 待全文 |
| 2026-08-03 | Agent / LLM 后训练 | [2608.01678](https://arxiv.org/abs/2608.01678) Progressive Agent Skill Generation via Reinforcement Learning | manual-review, p2-deferred-review | 待全文 |
| 2026-08-03 | 基础模型 | [2608.01676](https://arxiv.org/abs/2608.01676) Understanding Sparse Attention Selectivity in Long-Context Foundation Models via Counterfactual Evaluation | manual-review | 待全文 |
| 2026-08-03 | 基础模型 | [2608.01672](https://arxiv.org/abs/2608.01672) Learning What to Remember: Test-Time Training via Context Distillation | manual-review | B07 |
| 2026-08-03 | Agent | [2608.02683](https://arxiv.org/abs/2608.02683) $S^3$: Improving Agent Safety through Multi-Stage Defense | manual-review | 待全文 |
| 2026-08-03 | Agent | [2608.01558](https://arxiv.org/abs/2608.01558) Securing Agentic AI: From Per-Action Checks to Trajectory Assurance | manual-review | 待全文 |
| 2026-08-02 | 基础模型 | [2608.01536](https://arxiv.org/abs/2608.01536) Celty: SpMspV GPU Kernel and SIMT Co-Design for Efficient Dual-Sparse LLM Inference | manual-review | 待全文 |
| 2026-08-02 | LLM 后训练 | [2608.01359](https://arxiv.org/abs/2608.01359) EviSD: Evidence-Conditioned Self-Distillation for Search-Augmented Agents | manual-review | 待全文 |
| 2026-08-02 | 搜广推与 LLM 应用 | [2608.00938](https://arxiv.org/abs/2608.00938) GRACE: Generative Recommender Acceleration Engine for Real-Time Ads Retrieval | manual-review | 待全文 |
| 2026-08-01 | 搜广推与 LLM 应用 | [2608.00816](https://arxiv.org/abs/2608.00816) Exponential Reward Weighting for Fine-Tuning Generative Recommenders under Sparse and Noisy Feedback | manual-review | 待全文 |
| 2026-08-01 | LLM 后训练 | [2608.00782](https://arxiv.org/abs/2608.00782) Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance | manual-review | B08 |
| 2026-08-01 | Agent | [2608.00718](https://arxiv.org/abs/2608.00718) Adversarial Attacks in Multi-Agent LLM Pipelines: Unveiling Structural Vulnerabilities in Agentic AI Architectures | manual-review | 待全文 |
| 2026-08-01 | Agent | [2608.00558](https://arxiv.org/abs/2608.00558) AiFlow: Token-Native Reactive Orchestration with Bounded Backpressure for Streaming LLM Applications | manual-review | 待全文 |
| 2026-07-31 | Agent / LLM 后训练 | [2608.00335](https://arxiv.org/abs/2608.00335) RMSWeb: Reflection, Failure-Mode Mining, and Salvage-DS for Web Agent Reinforcement Learning | manual-review, p2-deferred-review | 待全文 |
| 2026-07-31 | Agent | [2608.02650](https://arxiv.org/abs/2608.02650) HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents | manual-review | B11 |
| 2026-07-31 | LLM 后训练 | [2608.00220](https://arxiv.org/abs/2608.00220) Verifier-Induced Support Reshaping in On-Policy Optimization | manual-review | 待全文 |
| 2026-07-31 | Agent / LLM 后训练 | [2608.00175](https://arxiv.org/abs/2608.00175) Inference-Time Policy Alignment for Fair Reinforcement Learning | manual-review, p2-deferred-review | 待全文 |
| 2026-07-31 | 搜广推与 LLM 应用 | [2608.11241](https://arxiv.org/abs/2608.11241) RecSys Factory: Bounding LLM Agent Autonomy to Decision Points in the Industrial Recommender Lifecycle | manual-review | 待全文 |
| 2026-07-31 | 搜广推与 LLM 应用 | [2607.29241](https://arxiv.org/abs/2607.29241) RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems | industrial-fulltext-review | B02 |
| 2026-07-31 | 搜广推与 LLM 应用 | [2607.29213](https://arxiv.org/abs/2607.29213) GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System | industrial-fulltext-review | B02 |
| 2026-07-31 | LLM 后训练 | [2607.29185](https://arxiv.org/abs/2607.29185) Learning Latent Reasoning Traces for Scalar Reward Models End-to-End | manual-review | 待全文 |
| 2026-07-31 | Agent / 基础模型 | [2607.29032](https://arxiv.org/abs/2607.29032) TransMem: Transforming Hidden States into Memory for Large Language Models | manual-review, p2-deferred-review | B07 |
| 2026-07-31 | 搜广推与 LLM 应用 | [2607.28971](https://arxiv.org/abs/2607.28971) Don't Contrast the Impossible: Region-Constrained Batching for Contrastive User Modeling on a Local Community Platform | industrial-fulltext-review | 待全文 |
| 2026-07-31 | 搜广推与 LLM 应用 | [2607.28940](https://arxiv.org/abs/2607.28940) TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings | industrial-fulltext-review | 待全文 |
| 2026-07-30 | 搜广推与 LLM 应用 | [2607.28895](https://arxiv.org/abs/2607.28895) LLM-Based Generative Retrieval for Snapchat Content Recommendation | industrial-fulltext-review | 待全文 |
| 2026-07-30 | Agent | [2607.28840](https://arxiv.org/abs/2607.28840) Benchmarks Are Not Validation: A System-Level View of Financial LLM Applications | manual-review | 待全文 |
| 2026-07-30 | Agent / 基础模型 / LLM 后训练 | [2607.28826](https://arxiv.org/abs/2607.28826) Distilling Knowledge from Large Language Models into Lightweight Reinforcement Learning Agents for Autonomous Cyber Operations | manual-review, p2-deferred-review | 待全文 |
| 2026-07-30 | Agent | [2607.28527](https://arxiv.org/abs/2607.28527) MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems | manual-review | B11 |
| 2026-07-30 | LLM 后训练 | [2607.28457](https://arxiv.org/abs/2607.28457) SVR: Self-Verifying Refinement via Joint Verdict-Confidence Reinforcement Learning for Adaptive Test-Time Compute | manual-review | 待全文 |
| 2026-07-30 | LLM 后训练 | [2607.28301](https://arxiv.org/abs/2607.28301) HARGO: Heterogeneity-Aware Reward-Guided Optimization for RL Post-Training of LLMs on HPC Tasks | manual-review | 待全文 |
| 2026-07-30 | LLM 后训练 | [2607.28127](https://arxiv.org/abs/2607.28127) FinSMART: Financial Sentiment Analysis for Algorithmic Trading through Market-Aligned Reinforcement Learning | manual-review | 待全文 |
| 2026-07-30 | LLM 后训练 | [2607.28077](https://arxiv.org/abs/2607.28077) LEEPS: Latent-Guided Explore-Exploit Prompt Sampling for Efficient RLVR in Large Language Models | manual-review | 待全文 |
| 2026-07-30 | Agent / LLM 后训练 | [2607.28026](https://arxiv.org/abs/2607.28026) Contrastive Reinforced Policy Optimization via Privileged Self-Distillation | manual-review, p2-deferred-review | B09 |
| 2026-07-30 | 搜广推与 LLM 应用 | [2607.27944](https://arxiv.org/abs/2607.27944) Interpretable Representation via LLM-Driven Generative Disentanglement for Local-Life Service Recommendation | manual-review | 待全文 |
| 2026-07-30 | 搜广推与 LLM 应用 | [2607.27789](https://arxiv.org/abs/2607.27789) From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation | industrial-fulltext-review | B02 |
| 2026-07-30 | 搜广推与 LLM 应用 | [2607.27760](https://arxiv.org/abs/2607.27760) Hierarchical Latent Reasoning for LLM-based Recommendation | manual-review | 待全文 |
| 2026-07-30 | 搜广推与 LLM 应用 | [2607.27647](https://arxiv.org/abs/2607.27647) LoopMemGR: From Behavior Logs to Evolving Memory for Generative Recommendation | manual-review | 待全文 |
| 2026-07-30 | LLM 后训练 | [2607.27610](https://arxiv.org/abs/2607.27610) Kalman Meets Curriculum: Efficient Dynamic Prompt Selection for Adaptive RL Finetuning | manual-review | 待全文 |
| 2026-07-30 | Agent | [2607.27562](https://arxiv.org/abs/2607.27562) DeepResearch Agent System | manual-review | 待全文 |
| 2026-07-29 | 搜广推与 LLM 应用 | [2607.27475](https://arxiv.org/abs/2607.27475) OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval | industrial-fulltext-review | B00 |
| 2026-07-29 | 搜广推与 LLM 应用 | [2607.26893](https://arxiv.org/abs/2607.26893) Beyond Action Imitation: Learning a Decision-Aware User Simulator for Online Advertising | manual-review | 待全文 |
| 2026-07-29 | LLM 后训练 | [2607.26873](https://arxiv.org/abs/2607.26873) SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning | manual-review | B09 |
| 2026-07-29 | Agent | [2607.26724](https://arxiv.org/abs/2607.26724) UrbanDS: A Graph-Guided LLM Multi-Agent System for Data-Intensive Urban Tasks | manual-review | 待全文 |
| 2026-07-29 | 搜广推与 LLM 应用 | [2607.26621](https://arxiv.org/abs/2607.26621) WhisperRec: Latent Reasoning for Efficient Foundation Recommendation Models | manual-review | 待全文 |
| 2026-07-29 | LLM 后训练 | [2608.14644](https://arxiv.org/abs/2608.14644) DUET: Dual-Teacher On-Policy Distillation via Same-Weight Disagreement for Prohibition Compliance | manual-review | 待全文 |
| 2026-07-29 | 搜广推与 LLM 应用 | [2607.26500](https://arxiv.org/abs/2607.26500) Multi-Decoder OneRec: Controllable Generative Retrieval for Multi-Objective Industrial Recommendation | industrial-fulltext-review | 待全文 |
| 2026-07-29 | LLM 后训练 | [2607.26457](https://arxiv.org/abs/2607.26457) DHRCL:Training Code LLMs with Dense Hierarchical Rewards and Curriculum Learning | manual-review | 待全文 |
| 2026-07-29 | 搜广推与 LLM 应用 | [2607.26427](https://arxiv.org/abs/2607.26427) PSG: Pair-Space Generation for Efficient Generative Reranking | manual-review | 待全文 |
| 2026-07-29 | 搜广推与 LLM 应用 | [2607.26418](https://arxiv.org/abs/2607.26418) DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval | industrial-fulltext-review | 待全文 |
| 2026-07-29 | 搜广推与 LLM 应用 | [2607.26369](https://arxiv.org/abs/2607.26369) ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling | industrial-fulltext-review | B00 |
| 2026-07-29 | Agent / LLM 后训练 | [2607.26358](https://arxiv.org/abs/2607.26358) Post-Training at the Edge of Detectability: A Game-Theoretic Approach to Fine-Tuning | manual-review, p2-deferred-review | 待全文 |
| 2026-07-28 | 搜广推与 LLM 应用 | [2607.25823](https://arxiv.org/abs/2607.25823) Hypothesis-Driven Shelf Generation for Personalised Recommendation | manual-review | 待全文 |
| 2026-07-28 | 搜广推与 LLM 应用 | [2607.25640](https://arxiv.org/abs/2607.25640) LLM-as-a-Judge for Evaluating System Responses in Conversational Music Recommendation | manual-review | 待全文 |
| 2026-07-28 | 搜广推与 LLM 应用 | [2607.25346](https://arxiv.org/abs/2607.25346) The Case Against Generation for Retrieval: Discriminative Language Models as Effective Retrievers | manual-review | 待全文 |
| 2026-07-28 | 搜广推与 LLM 应用 | [2607.25344](https://arxiv.org/abs/2607.25344) Reward Guided Decoding for Generative Recommendation | industrial-fulltext-review | 待全文 |
| 2026-07-28 | 搜广推与 LLM 应用 | [2607.25339](https://arxiv.org/abs/2607.25339) SPARC: Sequence-aware Progressive Attribute Routing and Compression Framework for Generative Recommendation | manual-review | 待全文 |
| 2026-07-28 | 搜广推与 LLM 应用 | [2607.25276](https://arxiv.org/abs/2607.25276) FunnelAL: Retrieve-then-Rank Active Learning for Single-Class Discovery | manual-review | 待全文 |
| 2026-07-28 | LLM 后训练 | [2607.26094](https://arxiv.org/abs/2607.26094) Meta-Learned Reward Shaping for Reinforcement Learning from Human Feedback | manual-review | 待全文 |
| 2026-07-27 | 搜广推与 LLM 应用 | [2607.25110](https://arxiv.org/abs/2607.25110) Memory Layer: Train the In-Model Cache for Recommendation Models | industrial-fulltext-review | 待全文 |
| 2026-07-27 | Agent / LLM 后训练 | [2607.25091](https://arxiv.org/abs/2607.25091) Towards Robust Reinforcement Learning for Small-Scale Language Model Agents | manual-review, p2-deferred-review | 待全文 |
| 2026-07-27 | LLM 后训练 | [2607.24900](https://arxiv.org/abs/2607.24900) Inverse RL Helps Align AI by Imitating Humans | manual-review | 待全文 |
| 2026-07-27 | LLM 后训练 | [2607.24522](https://arxiv.org/abs/2607.24522) FlowCTS: On-policy Continuous Trajectory Supervision of Flow Models | manual-review | 待全文 |
| 2026-07-27 | 搜广推与 LLM 应用 | [2607.24213](https://arxiv.org/abs/2607.24213) Integrating Factual and Normative Industrial Knowledge via Constraint-Aware Graph Attention for Process Plan Recommendation | manual-review | 待全文 |
| 2026-07-27 | 搜广推与 LLM 应用 | [2607.24092](https://arxiv.org/abs/2607.24092) ConAlign: Conditional Alignment Framework for Balancing Biased and Unbiased Recommendation | industrial-fulltext-review | 待全文 |
| 2026-07-27 | 基础模型 / 搜广推与 LLM 应用 | [2607.24025](https://arxiv.org/abs/2607.24025) SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation | industrial-fulltext-review, p2-deferred-review | 待全文 |
| 2026-07-27 | 搜广推与 LLM 应用 | [2607.23986](https://arxiv.org/abs/2607.23986) MEMOIR: Temporal Behavioral Memory for Recommendation Across the Preference-Drift Spectrum | manual-review | 待全文 |
| 2026-07-26 | 搜广推与 LLM 应用 | [2607.24869](https://arxiv.org/abs/2607.24869) Ranked by Position: Order Sensitivity as an Exploitable Attack Surface in LLM Listwise Recommenders | manual-review | 待全文 |
| 2026-07-26 | Agent | [2607.23678](https://arxiv.org/abs/2607.23678) Focus Is All You Need: Adaptive Goal-aware Attention Orchestration for Multi-Agent Graph Systems | manual-review | 待全文 |
| 2026-07-26 | 搜广推与 LLM 应用 | [2607.23561](https://arxiv.org/abs/2607.23561) Towards a Relevance Posterior in Neural Information Access | manual-review | 待全文 |
| 2026-07-26 | LLM 后训练 | [2607.23488](https://arxiv.org/abs/2607.23488) Learning Sampling Parameters for Diffusion Models | manual-review | 待全文 |
| 2026-07-26 | LLM 后训练 | [2607.23420](https://arxiv.org/abs/2607.23420) LA-RL: Label-Aware Self-Reflection for Reinforcement Learning in Information Extraction | manual-review | 待全文 |
| 2026-07-25 | LLM 后训练 | [2607.23125](https://arxiv.org/abs/2607.23125) Self-Boosting Vision-Language Models with Noisy Student On-Policy Self-Distillation | manual-review | 待全文 |
| 2026-07-25 | 搜广推与 LLM 应用 | [2607.23038](https://arxiv.org/abs/2607.23038) EGR: Embedding-Native Generative Retrieval with a Shared LLM | manual-review | 待全文 |
| 2026-07-24 | 搜广推与 LLM 应用 | [2607.24846](https://arxiv.org/abs/2607.24846) Two Views, One Voice: Evidence-Grounded Conversational Music Recommendation | manual-review | 待全文 |
| 2026-07-24 | LLM 后训练 | [2608.07531](https://arxiv.org/abs/2608.07531) Search-G1: Grounded Search Agents via Representation-Based Intrinsic Rewards | manual-review | 待全文 |
| 2026-07-24 | 基础模型 / LLM 后训练 | [2607.21971](https://arxiv.org/abs/2607.21971) Teaching LLMs to Self-Evolve: Cultivating Core Meta-Skills with Reinforcement Learning | manual-review, p2-deferred-review | 待全文 |
| 2026-07-23 | 搜广推与 LLM 应用 | [2607.21519](https://arxiv.org/abs/2607.21519) Diffusion Language Model for Recommendation | manual-review | 待全文 |
| 2026-07-23 | LLM 后训练 | [2607.21090](https://arxiv.org/abs/2607.21090) Training Large Language Models for Self-Explanation Faithfulness | manual-review | 待全文 |
| 2026-07-23 | LLM 后训练 | [2607.20952](https://arxiv.org/abs/2607.20952) The Weight of Silence: A Causal Case for Weights Over the Scratchpad in Latent Chess Reasoning | manual-review | 待全文 |
| 2026-07-23 | 搜广推与 LLM 应用 | [2607.24829](https://arxiv.org/abs/2607.24829) Improving Rare Medication Recommendation with Counterfactual Data Augmentation and Large Language Models | manual-review | 待全文 |
| 2026-07-22 | LLM 后训练 | [2607.20090](https://arxiv.org/abs/2607.20090) Reinforcement Learning for Large Language Model Selective Evidence Adoption from Contaminated Retrieval Results | manual-review | 待全文 |
| 2026-07-21 | LLM 后训练 | [2607.19331](https://arxiv.org/abs/2607.19331) ISO: An RLVR-Native Optimization Stack | manual-review | B09 |
| 2026-07-21 | 搜广推与 LLM 应用 | [2608.11219](https://arxiv.org/abs/2608.11219) From Monolithic to Modular: Segment-level Automatic Prompt Optimization | priority-fulltext-review | 待全文 |
| 2026-07-21 | LLM 后训练 | [2607.19219](https://arxiv.org/abs/2607.19219) Beyond Score Prediction: LLM-Based Essay Scoring and Feedback Generation via Reinforcement Learning with Rubric Rewards | manual-review | 待全文 |
| 2026-07-21 | Agent / 基础模型 / LLM 后训练 | [2607.19450](https://arxiv.org/abs/2607.19450) REGEN: Replay-recycling for Expert-to-Generalist distillation with Offline Reinforcement Learning | manual-review, p2-deferred-review | 待全文 |
| 2026-07-21 | Agent / 基础模型 | [2608.07527](https://arxiv.org/abs/2608.07527) DocAtlas: Long-Document Understanding as Mutable-State Interaction | manual-review, p2-deferred-review | 待全文 |
| 2026-07-20 | Agent | [2607.18485](https://arxiv.org/abs/2607.18485) Trusted Credentials, Untrusted Behavior: Benchmarking LLM-Agent Security in High-Performance Computing | manual-review | 待全文 |
| 2026-07-20 | Agent | [2607.18147](https://arxiv.org/abs/2607.18147) LLMs and Agentic AI Systems for Smart Grids: A Tutorial on Architectures and Applications | manual-review | 待全文 |
| 2026-07-20 | 基础模型 | [2607.17715](https://arxiv.org/abs/2607.17715) C$^2$KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference | manual-review | B07 |
| 2026-07-19 | Agent | [2607.17038](https://arxiv.org/abs/2607.17038) Reward-Driven LLM Agent Workflows: Synthesizing POMDP Routing and Self-Correction for Autonomous Decision-Making | manual-review | 待全文 |
| 2026-07-18 | 搜广推与 LLM 应用 | [2607.16633](https://arxiv.org/abs/2607.16633) Beyond Fixed Depths and Widths: Optimizing Textual Decoding Tries in LLM-based Generative Recommendation | manual-review | 待全文 |
| 2026-07-16 | 搜广推与 LLM 应用 | [2607.15440](https://arxiv.org/abs/2607.15440) Stochastic Reset Pathfinding: Path-Level Regret for Cascading Bandits over Graph Paths | priority-fulltext-review | 待全文 |
| 2026-07-16 | Agent | [2607.15257](https://arxiv.org/abs/2607.15257) SearchOS-V1: Towards Robust Open-Domain Information-Seeking Agent Collaboration | manual-review | 待全文 |
| 2026-07-16 | 搜广推与 LLM 应用 | [2607.14835](https://arxiv.org/abs/2607.14835) LLM-Based Re-Ranking for Real Estate Search | industrial-fulltext-review | B02 |
| 2026-07-16 | 搜广推与 LLM 应用 | [2607.14604](https://arxiv.org/abs/2607.14604) Accelerating A/B-Tests with Counterfactual Estimation: Reducing Variance through Policy Overlap | priority-fulltext-review | 待全文 |
| 2026-07-15 | LLM 后训练 | [2607.13753](https://arxiv.org/abs/2607.13753) Post-Training Shifts Confidence: A Three-Stage Analysis of How SFT, RL, and OPD Shape CoT Calibration | manual-review | 待全文 |
| 2026-07-13 | 搜广推与 LLM 应用 | [2607.26073](https://arxiv.org/abs/2607.26073) Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap | industrial-fulltext-review | B02 |
| 2026-07-12 | 搜广推与 LLM 应用 | [2607.10910](https://arxiv.org/abs/2607.10910) ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation | industrial-fulltext-review | 待全文 |
| 2026-07-11 | 搜广推与 LLM 应用 | [2607.10239](https://arxiv.org/abs/2607.10239) Multilingual Semantic Retrieval for Apple Music Search | industrial-fulltext-review | 待全文 |
| 2026-07-11 | 搜广推与 LLM 应用 | [2607.10235](https://arxiv.org/abs/2607.10235) Consensus vs. Dissent: Dynamic LLM Modeling of Subjective Preferences in Group Recommenders | manual-review | 待全文 |
| 2026-07-10 | 搜广推与 LLM 应用 | [2607.10016](https://arxiv.org/abs/2607.10016) Tokenizing Numerical and Embedding Features for LLM RecSys | manual-review | 待全文 |
| 2026-07-10 | 搜广推与 LLM 应用 | [2607.09988](https://arxiv.org/abs/2607.09988) An LLM-powered Agentic Recommendation System for Connected TV Content Discovery | manual-review | 待全文 |
| 2026-07-09 | 搜广推与 LLM 应用 | [2607.08703](https://arxiv.org/abs/2607.08703) MPFlow: Learning Budgeted Max-Flow Optimization on the Lightning Network with Deep Graph Reinforcement Learning | industrial-fulltext-review | 待全文 |
| 2026-07-09 | Agent / 基础模型 | [2607.08497](https://arxiv.org/abs/2607.08497) Cognitive-structured Multimodal Agent for Multimodal Understanding, Generation, and Editing | manual-review, p2-deferred-review | 待全文 |
| 2026-07-09 | 搜广推与 LLM 应用 | [2607.08365](https://arxiv.org/abs/2607.08365) DaV-Gen: End-to-End Generative Retrieval via Draft-and-Verify | manual-review | 待全文 |
| 2026-07-08 | 搜广推与 LLM 应用 | [2607.06979](https://arxiv.org/abs/2607.06979) Robust Federated Learning Under Real-World Client Churn | priority-fulltext-review | 待全文 |
| 2026-07-08 | 搜广推与 LLM 应用 | [2607.06963](https://arxiv.org/abs/2607.06963) Large Language Models (LLMs) and Generative AI in Cybersecurity and Privacy: A Survey of Dual-Use Risks, AI-Generated Malware, Explainability, and Defensive Strategies | priority-fulltext-review | 待全文 |
| 2026-07-05 | 搜广推与 LLM 应用 | [2607.04270](https://arxiv.org/abs/2607.04270) LBR: Towards Mitigating Length Bias in Large Language Models for Recommendation | manual-review | 待全文 |
| 2026-07-03 | 基础模型 | [2607.03089](https://arxiv.org/abs/2607.03089) STELLA: Efficient Sensor-to-LLM Translation for On-Device Human Activity Recognition | manual-review | 待全文 |
| 2026-07-01 | 搜广推与 LLM 应用 | [2607.01170](https://arxiv.org/abs/2607.01170) Diffusion-GR2: Diffusion Generative Reasoning Re-ranker | manual-review | 待全文 |
| 2026-06-30 | 搜广推与 LLM 应用 | [2606.31984](https://arxiv.org/abs/2606.31984) GR2 Technical Report | manual-review | 待全文 |
| 2026-06-30 | Agent / 搜广推与 LLM 应用 | [2606.31693](https://arxiv.org/abs/2606.31693) ShopX: A Foundation Model for Intent-to-Item Fulfillment in Agentic Shopping | manual-review, p2-deferred-review | 待全文 |
| 2026-06-30 | 搜广推与 LLM 应用 | [2606.31031](https://arxiv.org/abs/2606.31031) GenPage: Towards End-to-End Generative Homepage Construction at Netflix | industrial-fulltext-review | B02 |
| 2026-06-29 | 搜广推与 LLM 应用 | [2606.29946](https://arxiv.org/abs/2606.29946) POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation | industrial-fulltext-review | 待全文 |
| 2026-06-28 | 搜广推与 LLM 应用 | [2606.29341](https://arxiv.org/abs/2606.29341) Monosemanticity in Recommender Systems | manual-review | 待全文 |
| 2026-06-27 | 基础模型 / 搜广推与 LLM 应用 | [2606.28933](https://arxiv.org/abs/2606.28933) FinInvest-GTCN: Explainable Graph-Temporal-Causal Modeling for Risk-Aware Investment Decision Optimization | p2-deferred-review, priority-fulltext-review | 待全文 |
| 2026-06-27 | 搜广推与 LLM 应用 | [2607.24789](https://arxiv.org/abs/2607.24789) NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model | manual-review | B00 |
| 2026-06-26 | 搜广推与 LLM 应用 | [2606.28059](https://arxiv.org/abs/2606.28059) Fast and Feasible: Permutation-based Constrained Reranking for Revenue Maximization | industrial-fulltext-review | 待全文 |
| 2026-06-25 | 搜广推与 LLM 应用 | [2606.27058](https://arxiv.org/abs/2606.27058) UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation | industrial-fulltext-review | 待全文 |
| 2026-06-25 | 搜广推与 LLM 应用 | [2606.26859](https://arxiv.org/abs/2606.26859) AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems | manual-review | B00 |
| 2026-06-25 | LLM 后训练 | [2606.26787](https://arxiv.org/abs/2606.26787) AIGP: An LLM-Based Framework for Long-Term Value Alignment in E-Commerce Pricing | manual-review | 待全文 |
| 2026-06-24 | 搜广推与 LLM 应用 | [2606.25496](https://arxiv.org/abs/2606.25496) Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale | industrial-fulltext-review | 待全文 |
| 2026-06-22 | 搜广推与 LLM 应用 | [2606.23911](https://arxiv.org/abs/2606.23911) Scaling Dense Retrieval with LLM-Annotated Training Data: Structured Mining and Progressive Curriculum for E-Commerce Sponsored Search | industrial-fulltext-review | 待全文 |
| 2026-06-22 | 搜广推与 LLM 应用 | [2606.23057](https://arxiv.org/abs/2606.23057) Who Owns the AI Recommendation? A Multi-Industry Empirical Map of Brand Category Ownership Across Large Language Models | priority-fulltext-review | 待全文 |
| 2026-06-19 | 搜广推与 LLM 应用 | [2606.21590](https://arxiv.org/abs/2606.21590) Radial Basis Function Networks as Projection Heads in Self-Supervised Learning | priority-fulltext-review | 待全文 |
| 2026-06-17 | 搜广推与 LLM 应用 | [2606.19108](https://arxiv.org/abs/2606.19108) JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling | industrial-fulltext-review | B03 |
| 2026-06-17 | 搜广推与 LLM 应用 | [2606.18814](https://arxiv.org/abs/2606.18814) LensKit-Auto | priority-fulltext-review | 待全文 |
| 2026-06-17 | 搜广推与 LLM 应用 | [2606.18750](https://arxiv.org/abs/2606.18750) Ensuring Trustworthy Online A/B Testing: Addressing Five Key Questions on CUPED | industrial-fulltext-review | 待全文 |
| 2026-06-16 | 搜广推与 LLM 应用 | [2606.18451](https://arxiv.org/abs/2606.18451) A Cross-Model VLM-Judge Protocol for Single-Image 3D Mesh Quality (and Why Cheap Proxies Fall Short) | priority-fulltext-review | 待全文 |
| 2026-06-15 | 搜广推与 LLM 应用 | [2606.16838](https://arxiv.org/abs/2606.16838) OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation | industrial-fulltext-review | 待全文 |
| 2026-06-15 | 搜广推与 LLM 应用 | [2606.16641](https://arxiv.org/abs/2606.16641) PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization | industrial-fulltext-review | 待全文 |
| 2026-06-12 | 搜广推与 LLM 应用 | [2606.14932](https://arxiv.org/abs/2606.14932) Retrieval-as-a-Service:A System-Oriented Analysis of Industrial Retrieval Pipelines in Web Systems | manual-review | 待全文 |
| 2026-06-12 | 搜广推与 LLM 应用 | [2606.14817](https://arxiv.org/abs/2606.14817) Combining Retrieval-Augmented Text Generation with LLMs for Reading Content Recommendations | priority-fulltext-review | 待全文 |
| 2026-06-11 | LLM 后训练 | [2606.14801](https://arxiv.org/abs/2606.14801) QPILOTS: Efficient Test-Time Q-Steering for Flow Policies | manual-review | 待全文 |
| 2026-06-11 | 搜广推与 LLM 应用 | [2606.12984](https://arxiv.org/abs/2606.12984) SkillChain: Closing the Loop on Skill Evolution for Image-Based E-Commerce AI Assistants | industrial-fulltext-review | 待全文 |
| 2026-06-10 | 搜广推与 LLM 应用 | [2606.12281](https://arxiv.org/abs/2606.12281) CCKS: Consensus-based Communication and Knowledge Sharing | priority-fulltext-review | 待全文 |
| 2026-06-10 | 搜广推与 LLM 应用 | [2606.12198](https://arxiv.org/abs/2606.12198) LLM-Based User Personas for Recommendations at Scale | industrial-fulltext-review | 待全文 |
| 2026-06-09 | 搜广推与 LLM 应用 | [2606.10907](https://arxiv.org/abs/2606.10907) From Prompt to Purchase: How AI Brand Recommendations Move Consumers on the Open Web | priority-fulltext-review | 待全文 |
| 2026-06-09 | 搜广推与 LLM 应用 | [2606.10357](https://arxiv.org/abs/2606.10357) Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations | industrial-fulltext-review | 待全文 |
| 2026-06-08 | 搜广推与 LLM 应用 | [2606.10243](https://arxiv.org/abs/2606.10243) DUET -- Dual User Embedding Transformers for Offsite Conversion Prediction | industrial-fulltext-review | 待全文 |
| 2026-06-07 | 搜广推与 LLM 应用 | [2606.08604](https://arxiv.org/abs/2606.08604) Gryphon: A Unified Architecture for Semantic-ID Generation and Item-Level Scoring in Industrial Recommendations | industrial-fulltext-review | 待全文 |
| 2026-06-07 | LLM 后训练 / 搜广推与 LLM 应用 | [2606.08480](https://arxiv.org/abs/2606.08480) Adaptive Loss Balancing for Noise-Robust GRPO in Generative Recommendation | industrial-fulltext-review, p2-deferred-review | 待全文 |
| 2026-06-07 | 搜广推与 LLM 应用 | [2606.08466](https://arxiv.org/abs/2606.08466) ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants | industrial-fulltext-review | 待全文 |
| 2026-06-05 | 搜广推与 LLM 应用 | [2606.07068](https://arxiv.org/abs/2606.07068) Bias in Filter Feature Selection Evaluation: A Meta-Analysis of Datasets, Baselines, and Experimental Design Choices | priority-fulltext-review | 待全文 |
| 2026-06-05 | 搜广推与 LLM 应用 | [2606.06970](https://arxiv.org/abs/2606.06970) SSRLive: Live Streaming Recommendation with Dynamic Semantic ID | industrial-fulltext-review | 待全文 |
| 2026-06-03 | 搜广推与 LLM 应用 | [2606.04448](https://arxiv.org/abs/2606.04448) Bridging Short Videos and Live Streams: Reasoning-Guided Multimodal LLMs for Cross-Domain Representation Learning | industrial-fulltext-review | 待全文 |
| 2026-06-03 | 搜广推与 LLM 应用 | [2606.04387](https://arxiv.org/abs/2606.04387) Rethinking Sales Lead Scoring with LLM-based Hierarchical Preference Ranking | industrial-fulltext-review | 待全文 |
| 2026-06-02 | 搜广推与 LLM 应用 | [2606.04110](https://arxiv.org/abs/2606.04110) Variance Reduction for Heavy-Tailed Monetization Metrics in Ranking Experiments via Post-Stratification | industrial-fulltext-review | 待全文 |
| 2026-06-02 | LLM 后训练 / 搜广推与 LLM 应用 | [2606.03866](https://arxiv.org/abs/2606.03866) Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation | industrial-fulltext-review, p2-deferred-review | 待全文 |
| 2026-05-29 | 搜广推与 LLM 应用 | [2606.00282](https://arxiv.org/abs/2606.00282) Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems | industrial-fulltext-review | 待全文 |
| 2026-05-27 | 搜广推与 LLM 应用 | [2605.29141](https://arxiv.org/abs/2605.29141) Toward User Preference Alignment in LLM Recommendation via Explicit Context Feedback | priority-fulltext-review | 待全文 |
| 2026-05-27 | 搜广推与 LLM 应用 | [2605.28888](https://arxiv.org/abs/2605.28888) Generative Spatiotemporal Intent Sequence Recommendation via Implicit Reasoning in Amap | industrial-fulltext-review | 待全文 |
| 2026-05-26 | 搜广推与 LLM 应用 | [2605.27704](https://arxiv.org/abs/2605.27704) Joint Optimization of Relevance and Engagement in Multi-Task Ranking for E-Commerce with Efficient LLM Supervision | industrial-fulltext-review | 待全文 |
| 2026-05-26 | 搜广推与 LLM 应用 | [2607.19357](https://arxiv.org/abs/2607.19357) Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems | industrial-fulltext-review | 待全文 |
| 2026-05-26 | 搜广推与 LLM 应用 | [2605.27103](https://arxiv.org/abs/2605.27103) MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music | industrial-fulltext-review | 待全文 |
| 2026-05-26 | 搜广推与 LLM 应用 | [2605.27043](https://arxiv.org/abs/2605.27043) Causal Representation Learning for Generalisable Recommendation | industrial-fulltext-review | 待全文 |
| 2026-05-26 | 搜广推与 LLM 应用 | [2605.26717](https://arxiv.org/abs/2605.26717) L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation | industrial-fulltext-review | B03 |
| 2026-05-26 | 搜广推与 LLM 应用 | [2605.26424](https://arxiv.org/abs/2605.26424) Uniboost: Global Coordination with Value Alignment for Fair and Efficient Traffic Allocation | industrial-fulltext-review | 待全文 |
| 2026-05-25 | 搜广推与 LLM 应用 | [2605.25726](https://arxiv.org/abs/2605.25726) SIREN: Unified Multi-Granularity Semantic Interaction for Multi-Modal Lifelong User Interest Modeling | industrial-fulltext-review | 待全文 |
| 2026-05-25 | 搜广推与 LLM 应用 | [2605.25514](https://arxiv.org/abs/2605.25514) From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark | industrial-fulltext-review | B03 |
| 2026-05-24 | 搜广推与 LLM 应用 | [2605.25007](https://arxiv.org/abs/2605.25007) Meta-Modal Agent: Sequential Evidence Routing for Missing-Modality Candidate Reranking | priority-fulltext-review | 待全文 |
| 2026-05-22 | 搜广推与 LLM 应用 | [2605.23702](https://arxiv.org/abs/2605.23702) TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery | industrial-fulltext-review | B03 |
| 2026-05-20 | 搜广推与 LLM 应用 | [2605.21752](https://arxiv.org/abs/2605.21752) PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation | industrial-fulltext-review | B03 |
| 2026-05-19 | 搜广推与 LLM 应用 | [2605.20559](https://arxiv.org/abs/2605.20559) Group-Aware Matrix Estimation and Latent Subspace Recovery | priority-fulltext-review | 待全文 |
| 2026-05-18 | 搜广推与 LLM 应用 | [2605.18696](https://arxiv.org/abs/2605.18696) Ensembling Tabular Foundation Models - A Diversity Ceiling And A Calibration Trap | priority-fulltext-review | 待全文 |
| 2026-05-18 | 搜广推与 LLM 应用 | [2605.17863](https://arxiv.org/abs/2605.17863) DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems | industrial-fulltext-review | B03 |
| 2026-05-15 | 搜广推与 LLM 应用 | [2605.16479](https://arxiv.org/abs/2605.16479) Policy-Grounded Dynamic Facet Suggestions for Job Search | industrial-fulltext-review | 待全文 |
| 2026-05-13 | 搜广推与 LLM 应用 | [2605.13052](https://arxiv.org/abs/2605.13052) RAG-Enhanced Large Language Models for Dynamic Content Expiration Prediction in Web Search | industrial-fulltext-review | 待全文 |
| 2026-05-12 | 搜广推与 LLM 应用 | [2605.11732](https://arxiv.org/abs/2605.11732) AgentDisCo: Towards Disentanglement and Collaboration in Open-ended Deep Research Agents | priority-fulltext-review | 待全文 |
| 2026-05-11 | 搜广推与 LLM 应用 | [2605.11118](https://arxiv.org/abs/2605.11118) A Cascaded Generative Approach for e-Commerce Recommendations | industrial-fulltext-review | 待全文 |
| 2026-05-11 | 搜广推与 LLM 应用 | [2605.10367](https://arxiv.org/abs/2605.10367) AgentGR: Semantic-aware Agentic Group Decision-Making Simulator for Group Recommendation | priority-fulltext-review | 待全文 |
| 2026-05-09 | 搜广推与 LLM 应用 | [2605.08731](https://arxiv.org/abs/2605.08731) Choosing a JPEG Decoder for PyTorch DataLoaders: Workload-Specific Throughput on Four CPUs | priority-fulltext-review | 待全文 |
| 2026-05-08 | 搜广推与 LLM 应用 | [2605.07129](https://arxiv.org/abs/2605.07129) RRCM: Ranking-Driven Retrieval over Collaborative and Meta Memories for LLM Recommendation | priority-fulltext-review | 待全文 |
| 2026-05-08 | 搜广推与 LLM 应用 | [2605.16344](https://arxiv.org/abs/2605.16344) A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems | industrial-fulltext-review | B04 |
| 2026-05-07 | 搜广推与 LLM 应用 | [2605.06981](https://arxiv.org/abs/2605.06981) Bridging Textual Profiles and Latent User Embeddings for Personalization | priority-fulltext-review | 待全文 |
| 2026-05-07 | 搜广推与 LLM 应用 | [2605.05855](https://arxiv.org/abs/2605.05855) Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling | industrial-fulltext-review | 待全文 |
| 2026-05-07 | 搜广推与 LLM 应用 | [2605.05730](https://arxiv.org/abs/2605.05730) Effective Knowledge Transfer for Multi-Task Recommendation Models | industrial-fulltext-review | B04 |
| 2026-05-04 | 搜广推与 LLM 应用 | [2606.07546](https://arxiv.org/abs/2606.07546) Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling | industrial-fulltext-review | 待全文 |
| 2026-05-01 | 搜广推与 LLM 应用 | [2605.00353](https://arxiv.org/abs/2605.00353) Negative Data Mining for Contrastive Learning in Dense Retrieval at IKEA.com | industrial-fulltext-review | 待全文 |
| 2026-04-30 | 搜广推与 LLM 应用 | [2605.00068](https://arxiv.org/abs/2605.00068) Human-in-the-Loop Meta Bayesian Optimization for Fusion Energy and Scientific Applications | priority-fulltext-review | 待全文 |
| 2026-04-30 | 搜广推与 LLM 应用 | [2604.27321](https://arxiv.org/abs/2604.27321) Toward Autonomous SOC Operations: End-to-End LLM Framework for Threat Detection, Query Generation, and Resolution in Security Operations | priority-fulltext-review | 待全文 |
| 2026-04-29 | 搜广推与 LLM 应用 | [2604.26390](https://arxiv.org/abs/2604.26390) Meta-Learning and Targeted Differential Privacy to Improve the Accuracy-Privacy Trade-off in Recommendations | priority-fulltext-review | 待全文 |
| 2026-04-28 | 搜广推与 LLM 应用 | [2604.25834](https://arxiv.org/abs/2604.25834) Action-Aware Generative Sequence Modeling for Short Video Recommendation | industrial-fulltext-review | 待全文 |
| 2026-04-28 | 搜广推与 LLM 应用 | [2604.25732](https://arxiv.org/abs/2604.25732) Personalized Multi-Interest Modeling for Cross-Domain Recommendation to Cold-Start Users | priority-fulltext-review | 待全文 |
| 2026-04-26 | 搜广推与 LLM 应用 | [2604.23522](https://arxiv.org/abs/2604.23522) Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale | industrial-fulltext-review | B04 |
| 2026-04-25 | 搜广推与 LLM 应用 | [2604.23088](https://arxiv.org/abs/2604.23088) Code Broker: A Multi-Agent System for Automated Code Quality Assessment | priority-fulltext-review | 待全文 |
| 2026-04-20 | 搜广推与 LLM 应用 | [2604.18146](https://arxiv.org/abs/2604.18146) Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations | industrial-fulltext-review | 待全文 |
| 2026-04-20 | 搜广推与 LLM 应用 | [2604.17878](https://arxiv.org/abs/2604.17878) RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems | industrial-fulltext-review | 待全文 |
| 2026-04-17 | 搜广推与 LLM 应用 | [2604.15937](https://arxiv.org/abs/2604.15937) Polarization by Default: Auditing Recommendation Bias in LLM-Based Content Curation | priority-fulltext-review | 待全文 |
| 2026-04-15 | 搜广推与 LLM 应用 | [2604.14352](https://arxiv.org/abs/2604.14352) PROXIMA: A Reliability Scoring Framework for Proxy Metrics in Online Controlled Experiments | industrial-fulltext-review | 待全文 |
| 2026-04-15 | 搜广推与 LLM 应用 | [2604.13796](https://arxiv.org/abs/2604.13796) Driving Engagement in Daily Fantasy Sports with a Scalable and Urgency-Aware Ranking Engine | industrial-fulltext-review | 待全文 |
| 2026-04-14 | 搜广推与 LLM 应用 | [2604.12965](https://arxiv.org/abs/2604.12965) Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation | priority-fulltext-review | 待全文 |
| 2026-04-14 | 搜广推与 LLM 应用 | [2604.14223](https://arxiv.org/abs/2604.14223) TRACE: A Conversational Framework for Sustainable Tourism Recommendation with Agentic Counterfactual Explanations | priority-fulltext-review | 待全文 |
| 2026-04-14 | 搜广推与 LLM 应用 | [2605.04076](https://arxiv.org/abs/2605.04076) A Regulatory Governance Framework for AI-Driven Financial Fraud Detection in U.S. Banking: Integrating OCC, SR 11-7, CFPB, and FinCEN Compliance Requirements for Model Development, Validation, and Monitoring Lifecycles | priority-fulltext-review | 待全文 |
| 2026-04-14 | 搜广推与 LLM 应用 | [2604.12234](https://arxiv.org/abs/2604.12234) UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute | industrial-fulltext-review | B04 |
| 2026-04-13 | 搜广推与 LLM 应用 | [2604.11440](https://arxiv.org/abs/2604.11440) R3-VAE: Reference Vector-Guided Rating Residual Quantization VAE for Generative Recommendation | industrial-fulltext-review | 待全文 |
| 2026-04-12 | 搜广推与 LLM 应用 | [2604.10471](https://arxiv.org/abs/2604.10471) SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search | industrial-fulltext-review | 待全文 |
| 2026-04-09 | 搜广推与 LLM 应用 | [2604.08181](https://arxiv.org/abs/2604.08181) Long-Term Embeddings for Balanced Personalization | industrial-fulltext-review | 待全文 |
| 2026-04-08 | 搜广推与 LLM 应用 | [2605.27374](https://arxiv.org/abs/2605.27374) ICG: Improving Cover Image Generation via MLLM-based Prompting and Personalized Preference Alignment | priority-fulltext-review | 待全文 |
| 2026-04-06 | 搜广推与 LLM 应用 | [2604.09698](https://arxiv.org/abs/2604.09698) Evaluating Scene-based In-Situ Item Labeling for Immersive Conversational Recommendation | priority-fulltext-review | 待全文 |
| 2026-04-05 | 搜广推与 LLM 应用 | [2604.03949](https://arxiv.org/abs/2604.03949) Semantic IDs for Recommender Systems at Snapchat: Use Cases, Technical Challenges, and Design Choices | industrial-fulltext-review | 待全文 |
| 2026-03-30 | 搜广推与 LLM 应用 | [2603.28124](https://arxiv.org/abs/2603.28124) RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation | industrial-fulltext-review | 待全文 |
| 2026-03-27 | 搜广推与 LLM 应用 | [2603.26085](https://arxiv.org/abs/2603.26085) AgenticRS-Architecture: System Design for Agentic Recommender Systems | industrial-fulltext-review | 待全文 |
| 2026-03-26 | 搜广推与 LLM 应用 | [2603.25070](https://arxiv.org/abs/2603.25070) An Explainable Ensemble Learning Framework for Crop Classification with Optimized Feature Pyramids and Deep Networks | priority-fulltext-review | 待全文 |
| 2026-03-26 | 搜广推与 LLM 应用 | [2603.24963](https://arxiv.org/abs/2603.24963) Design Once, Deploy at Scale: Template-Driven ML Development for Large Model Ecosystems | priority-fulltext-review | 待全文 |
| 2026-03-25 | 搜广推与 LLM 应用 | [2603.24226](https://arxiv.org/abs/2603.24226) UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking | industrial-fulltext-review | B04 |
| 2026-03-24 | 搜广推与 LLM 应用 | [2603.22916](https://arxiv.org/abs/2603.22916) GateSID: Adaptive Gating for Balancing Semantic and Collaborative Signals in Recommendation | industrial-fulltext-review | B04 |
| 2026-03-23 | 搜广推与 LLM 应用 | [2603.21481](https://arxiv.org/abs/2603.21481) TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation | industrial-fulltext-review | 待全文 |
| 2026-03-20 | 搜广推与 LLM 应用 | [2603.20062](https://arxiv.org/abs/2603.20062) The End of Rented Discovery: How AI Search Redistributes Power Between Hotels and Intermediaries | priority-fulltext-review | 待全文 |
| 2026-03-20 | 搜广推与 LLM 应用 | [2603.19710](https://arxiv.org/abs/2603.19710) AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation | industrial-fulltext-review | B05 |
| 2026-03-20 | 搜广推与 LLM 应用 | [2603.19665](https://arxiv.org/abs/2603.19665) GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce | industrial-fulltext-review | 待全文 |
| 2026-03-20 | 搜广推与 LLM 应用 | [2603.19585](https://arxiv.org/abs/2603.19585) SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search | industrial-fulltext-review | B05 |
| 2026-03-19 | 搜广推与 LLM 应用 | [2603.18765](https://arxiv.org/abs/2603.18765) Implicit Grading Bias in Large Language Models: How Writing Style Affects Automated Assessment Across Math, Programming, and Essay Tasks | priority-fulltext-review | 待全文 |
| 2026-03-17 | 搜广推与 LLM 应用 | [2604.13057](https://arxiv.org/abs/2604.13057) A Multi-Model Approach to English-Bangla Sentiment Classification of Government Mobile Banking App Reviews | priority-fulltext-review | 待全文 |
| 2026-03-17 | 搜广推与 LLM 应用 | [2603.16088](https://arxiv.org/abs/2603.16088) RecBundle: A Next-Generation Geometric Paradigm for Explainable Recommender Systems | priority-fulltext-review | 待全文 |
| 2026-03-12 | 搜广推与 LLM 应用 | [2603.11486](https://arxiv.org/abs/2603.11486) Quantized Inference for OneRec-V2 | industrial-fulltext-review | 待全文 |
| 2026-03-04 | 搜广推与 LLM 应用 | [2603.04227](https://arxiv.org/abs/2603.04227) Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds | industrial-fulltext-review | 待全文 |
| 2026-03-04 | 搜广推与 LLM 应用 | [2603.03988](https://arxiv.org/abs/2603.03988) SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders | industrial-fulltext-review | B05 |
| 2026-03-01 | 搜广推与 LLM 应用 | [2603.00980](https://arxiv.org/abs/2603.00980) Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations | industrial-fulltext-review | 待全文 |
| 2026-02-28 | 搜广推与 LLM 应用 | [2603.00632](https://arxiv.org/abs/2603.00632) Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale | industrial-fulltext-review | B05 |
| 2026-02-28 | 搜广推与 LLM 应用 | [2603.00502](https://arxiv.org/abs/2603.00502) Trinity: A Scenario-Aware Recommendation Framework for Large-Scale Cold-Start Users | industrial-fulltext-review | 待全文 |
| 2026-02-27 | 搜广推与 LLM 应用 | [2602.23717](https://arxiv.org/abs/2602.23717) Recommending Search Filters To Improve Conversions At Airbnb | industrial-fulltext-review | 待全文 |
| 2026-02-26 | 搜广推与 LLM 应用 | [2602.23530](https://arxiv.org/abs/2602.23530) Unified Learning-to-Rank for Multi-Channel Retrieval in Large-Scale E-Commerce Search | industrial-fulltext-review | 待全文 |
| 2026-02-25 | 搜广推与 LLM 应用 | [2602.21600](https://arxiv.org/abs/2602.21600) AQR-HNSW: Accelerating Approximate Nearest Neighbor Search via Density-aware Quantization and Multi-stage Re-ranking | priority-fulltext-review | 待全文 |
| 2026-02-25 | 搜广推与 LLM 应用 | [2603.19249](https://arxiv.org/abs/2603.19249) Spelling Correction in Healthcare Query-Answer Systems: Methods, Retrieval Impact, and Empirical Evaluation | priority-fulltext-review | 待全文 |
| 2026-02-24 | 搜广推与 LLM 应用 | [2602.20995](https://arxiv.org/abs/2602.20995) Generative Pseudo-Labeling for Pre-Ranking with LLMs | manual-review | B05 |
| 2026-02-23 | 搜广推与 LLM 应用 | [2603.06631](https://arxiv.org/abs/2603.06631) T-REX: Transformer-Based Category Sequence Generation for Grocery Basket Recommendation | industrial-fulltext-review | 待全文 |
| 2026-02-20 | 搜广推与 LLM 应用 | [2602.18348](https://arxiv.org/abs/2602.18348) Explaining AutoClustering: Uncovering Meta-Feature Contribution in AutoML for Clustering | priority-fulltext-review | 待全文 |
| 2026-02-20 | 搜广推与 LLM 应用 | [2602.17976](https://arxiv.org/abs/2602.17976) In-Context Pure Exploration in Continuous Decision Spaces | priority-fulltext-review | 待全文 |
| 2026-02-19 | 搜广推与 LLM 应用 | [2602.17058](https://arxiv.org/abs/2602.17058) A Long-term Value Prediction Framework In Video Ranking | industrial-fulltext-review | B05 |
| 2026-02-16 | LLM 后训练 / 搜广推与 LLM 应用 | [2602.15005](https://arxiv.org/abs/2602.15005) Learning User Interests via Reasoning and Distillation for Cross-Domain News Recommendation | industrial-fulltext-review, p2-deferred-review | 待全文 |
| 2026-02-14 | 搜广推与 LLM 应用 | [2602.13581](https://arxiv.org/abs/2602.13581) Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following | industrial-fulltext-review | 待全文 |
| 2026-02-13 | 搜广推与 LLM 应用 | [2602.13134](https://arxiv.org/abs/2602.13134) Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning | industrial-fulltext-review | 待全文 |
| 2026-02-13 | 搜广推与 LLM 应用 | [2602.12972](https://arxiv.org/abs/2602.12972) Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework | industrial-fulltext-review | 待全文 |
| 2026-02-13 | 搜广推与 LLM 应用 | [2602.12968](https://arxiv.org/abs/2602.12968) RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems | industrial-fulltext-review | B06 |
| 2026-02-13 | 搜广推与 LLM 应用 | [2602.12593](https://arxiv.org/abs/2602.12593) RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction | industrial-fulltext-review | 待全文 |
| 2026-02-13 | 搜广推与 LLM 应用 | [2602.12564](https://arxiv.org/abs/2602.12564) CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval | industrial-fulltext-review | 待全文 |
| 2026-02-12 | 搜广推与 LLM 应用 | [2602.12354](https://arxiv.org/abs/2602.12354) An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking | industrial-fulltext-review | B06 |
| 2026-02-12 | 搜广推与 LLM 应用 | [2602.12041](https://arxiv.org/abs/2602.12041) Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems | industrial-fulltext-review | 待全文 |
| 2026-02-12 | 搜广推与 LLM 应用 | [2602.11562](https://arxiv.org/abs/2602.11562) LASER: An Efficient Target-Aware Segmented Attention Framework for End-to-End Long Sequence Modeling | industrial-fulltext-review | 待全文 |
| 2026-02-11 | 搜广推与 LLM 应用 | [2602.11410](https://arxiv.org/abs/2602.11410) CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer | industrial-fulltext-review | B06 |
| 2026-02-11 | 搜广推与 LLM 应用 | [2602.10455](https://arxiv.org/abs/2602.10455) Compute Only Once: UG-Separation for Efficient Large Recommendation Models | industrial-fulltext-review | 待全文 |
| 2026-02-10 | 搜广推与 LLM 应用 | [2602.09901](https://arxiv.org/abs/2602.09901) QP-OneModel: A Unified Generative LLM for Multi-Task Query Understanding in Xiaohongshu Search | industrial-fulltext-review | 待全文 |
| 2026-02-10 | 搜广推与 LLM 应用 | [2602.09744](https://arxiv.org/abs/2602.09744) DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation | industrial-fulltext-review | B06 |
| 2026-02-10 | 搜广推与 LLM 应用 | [2602.09401](https://arxiv.org/abs/2602.09401) SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking | industrial-fulltext-review | B06 |
| 2026-02-10 | 搜广推与 LLM 应用 | [2602.09386](https://arxiv.org/abs/2602.09386) SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity | industrial-fulltext-review | 待全文 |
| 2026-02-09 | 搜广推与 LLM 应用 | [2602.09194](https://arxiv.org/abs/2602.09194) ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest | industrial-fulltext-review | B06 |
| 2026-02-09 | 搜广推与 LLM 应用 | [2602.08530](https://arxiv.org/abs/2602.08530) PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation | industrial-fulltext-review | 待全文 |
| 2026-02-08 | 搜广推与 LLM 应用 | [2602.07987](https://arxiv.org/abs/2602.07987) Learning to Alleviate Familiarity Bias in Video Recommendation | industrial-fulltext-review | 待全文 |
| 2026-02-03 | 搜广推与 LLM 应用 | [2602.03324](https://arxiv.org/abs/2602.03324) SCASRec: A Self-Correcting and Auto-Stopping Model for Generative Route List Recommendation | industrial-fulltext-review | 待全文 |
| 2026-02-01 | 搜广推与 LLM 应用 | [2602.01023](https://arxiv.org/abs/2602.01023) Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment | industrial-fulltext-review | B06 |
| 2026-01-31 | 搜广推与 LLM 应用 | [2602.02582](https://arxiv.org/abs/2602.02582) Uncertainty and Fairness Awareness in LLM-Based Recommendation Systems | priority-fulltext-review | 待全文 |
| 2026-01-31 | 搜广推与 LLM 应用 | [2602.00758](https://arxiv.org/abs/2602.00758) Temporal Leakage in Search-Engine Date-Filtered Web Retrieval: A Retrospective Forecasting Case Study | priority-fulltext-review | 待全文 |
| 2026-01-30 | 搜广推与 LLM 应用 | [2601.22820](https://arxiv.org/abs/2601.22820) User-Adaptive Meta-Learning for Cold-Start Medication Recommendation with Uncertainty Filtering | priority-fulltext-review | 待全文 |
| 2026-01-29 | 搜广推与 LLM 应用 | [2601.21285](https://arxiv.org/abs/2601.21285) Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation | industrial-fulltext-review | 待全文 |
| 2026-01-28 | 搜广推与 LLM 应用 | [2601.20215](https://arxiv.org/abs/2601.20215) Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation | industrial-fulltext-review | 待全文 |
| 2026-01-28 | 搜广推与 LLM 应用 | [2601.20199](https://arxiv.org/abs/2601.20199) MERGE: Next-Generation Item Indexing Paradigm for Large-Scale Streaming Recommendation | industrial-fulltext-review | 待全文 |
| 2026-01-26 | 搜广推与 LLM 应用 | [2601.18664](https://arxiv.org/abs/2601.18664) S$^2$GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation | industrial-fulltext-review | 待全文 |
| 2026-01-26 | 搜广推与 LLM 应用 | [2604.09549](https://arxiv.org/abs/2604.09549) Beyond Offline A/B Testing: Context-Aware Agent Simulation for Recommender System Evaluation | industrial-fulltext-review | 待全文 |
| 2026-01-25 | 搜广推与 LLM 应用 | [2601.17836](https://arxiv.org/abs/2601.17836) Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction | industrial-fulltext-review | 待全文 |
| 2026-01-24 | 搜广推与 LLM 应用 | [2601.17472](https://arxiv.org/abs/2601.17472) Adversarial Alignment and Disentanglement for Cross-Domain CTR Prediction with Domain-Encompassing Features | industrial-fulltext-review | 待全文 |
| 2026-01-20 | 搜广推与 LLM 应用 | [2601.14333](https://arxiv.org/abs/2601.14333) Hierarchical Contextual Uplift Bandits for Catalog Personalization | industrial-fulltext-review | 待全文 |
| 2026-01-11 | 搜广推与 LLM 应用 | [2601.06873](https://arxiv.org/abs/2601.06873) Applying Embedding-Based Retrieval to Airbnb Search | industrial-fulltext-review | 待全文 |
| 2026-01-08 | 搜广推与 LLM 应用 | [2601.04674](https://arxiv.org/abs/2601.04674) PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations | industrial-fulltext-review | 待全文 |
| 2026-01-08 | 搜广推与 LLM 应用 | [2601.04554](https://arxiv.org/abs/2601.04554) Exploring Recommender System Evaluation: A Multi-Modal User Agent Framework for A/B Testing | industrial-fulltext-review | 待全文 |
| 2026-01-06 | 搜广推与 LLM 应用 | [2601.02955](https://arxiv.org/abs/2601.02955) Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency | industrial-fulltext-review | 待全文 |
| 2026-01-05 | 搜广推与 LLM 应用 | [2601.02002](https://arxiv.org/abs/2601.02002) Exploring Approaches for Detecting Memorization of Recommender System Data in Large Language Models | priority-fulltext-review | 待全文 |

## 执行约束

1. 每批开始前重新读论文正文，若不存在声称的证据则从批次移出，并在机器账本写明理由。
2. 每篇必须有独立机制代码、公开数据/mini-suite 指标、完整论文信息、原文关键图和复现边界。
3. 可接入 evolve 的机制必须同时注册 mutation；负结果照常保存。
4. B01–B11 全部关闭前，后续扫描仍以本历史账本为基线；关闭后才恢复近期增量扫描。
