# 11月16–18日论文更新与交付

[English](../../en/research-audits/nov18-latest/README.md)

本批47项：46篇区间内新论文，1篇旧论文新开源补录；35个低成本组件，12篇高成本仅收录。22个CUDA组件已在真实A100执行三种子验证。189道中英学习题、47条同主题深读更新。

## 范围与证据

这是有限选题扫描和交付，不是所有来源/所有论文的全文穷尽审查。3369条含11月13日起重叠、旧稿修订及跨类去重的元数据不是3369篇新论文，也不是待实现积压。本次不改全库审查水位。

优先核对Google/Meta官方目录、公开仓库事件及固定原文作者栏。Meta VisHead-Spec已实现低成本算子；Google efficient_evals是11月16日新开源、3月2日首发旧论文，单独计补漏。KVUse等生产离线回放未被误当线上A/B。

所有本地指标都是L0/L1诊断，不是模型能力、生产提升或Evolve晋级证据。高成本完整实验明确不复现，审查DONE，不自动重试。WM-Quant旧错误网格诊断被作废保留，修复后以新源码重新执行。

来源与范围：[来源覆盖](source-coverage.json)、[Google/Meta原文选择](priority-primary-selection.json)、[完整交付账本](task-scope.json)、[成本预检](preflight.json)、[实际GPU结果](raw-cuda.json)。

## 交付清单

| 领域 | 论文 | 首发日期 | 本地交付 |
| --- | --- | --- | --- |
| agent-research | [Instant Weight-Space Consolidation for Long-Term Memory in LLMs](../../agent-research/2611.20759-clam-memory/README.md) | 2026-11-16 | 高成本仅收录，不复现 |
| agent-research | [DetourBench: Trajectory-Level Evaluation of Interactive Agents with Exact Minimum-Action Bounds](../../agent-research/2611.20844-detourbench/README.md) | 2026-11-16 | l1_mechanism |
| agent-research | [Evaluation-Free Recursive Self-Improvement for Coding Agents](../../agent-research/2611.21056-elite-eval-free/README.md) | 2026-11-16 | l0_interface |
| agent-research | [Verifying Agents in Rubric-Graded Environments](../../agent-research/2611.22841-gandalf-bvb/README.md) | 2026-11-17 | 高成本仅收录，不复现 |
| agent-research | [MetaAct: Self-Evolving Executable Action Constraints for Embodied Language Agents](../../agent-research/2611.20655-metaact/README.md) | 2026-11-16 | l1_mechanism |
| agent-research | [The Resolution Hypothesis: Agent Evolution's Key Is Identifying Improvements](../../agent-research/2611.23068-resolution-hypothesis/README.md) | 2026-11-17 | l1_mechanism |
| agent-research | [SciResearch-Eval: Evaluating Scientific Judgment in Autonomous Experimental Agents](../../agent-research/2611.21541-sciresearch-eval/README.md) | 2026-11-16 | l1_mechanism |
| agent-research | [Do LLM Agents Still Need to Be Told How to Self-Improve?](../../agent-research/2611.23219-self-organized-learning/README.md) | 2026-11-17 | 高成本仅收录，不复现 |
| agent-research | [Invariant-Aware Harness Enforcement to Protect LLM Agents from Silent API Failures](../../agent-research/2611.20595-silentguard/README.md) | 2026-11-16 | l1_mechanism |
| agent-research | [SkillBuffBench: Measuring What Agent Skills Contribute across Harnesses, Models, Skill Access Modes and Memory](../../agent-research/2611.22017-skillbuffbench/README.md) | 2026-11-17 | 高成本仅收录，不复现 |
| foundation-models | [Beyond Bitwidth: Deployment-Constrained Mixed-Precision Quantization for Multilingual LLM Inference on NVIDIA Blackwell](../../foundation-models/2611.21974-beyond-bitwidth/README.md) | 2026-11-16 | 高成本仅收录，不复现 |
| foundation-models | [CascadeJEPA: Enhancing 3D Geometric Representations via Spatially Coupled Cascaded Prediction](../../foundation-models/2611.22686-cascadejepa/README.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Deal With It: On Better Schedules for Listwise Reranking](../../foundation-models/2611.22392-dealrank/README.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Communicate the Change: Efficient Expert Parallelism via Activation Compression](../../foundation-models/2611.22215-echomoe/README.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Rich Insights from Cheap Signals: Efficient Evaluations via Tensor Factorization](../../foundation-models/2603.02029-efficient-evals-tensor/README.md) | 2026-03-02 | l1_mechanism |
| foundation-models | [FM-Mamba: An Efficient Native 2D Selective State Space Model with Stability-Aware Discretization](../../foundation-models/2611.22061-fm-mamba/README.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [GaugeRoPE: RoPE-Compatible Executable Latent Attention](../../foundation-models/2611.20524-gaugerope/README.md) | 2026-11-16 | l1_mechanism |
| foundation-models | [InfuseLoop: Cross-Trajectory Latent Injection for Scalable Parallel Looped Transformers](../../foundation-models/2611.22426-infuseloop/README.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [The Kernel Reality Check: Benchmarking and Distilling Efficient Attention at Scale](../../foundation-models/2611.22947-lara-plus-plus/README.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Latent Feedback Is a Compute and Data Amplifier](../../foundation-models/2611.20404-latent-feedback-scaling/README.md) | 2026-11-16 | 高成本仅收录，不复现 |
| foundation-models | [RISA: Recoverable Sparse Attention for Block-Diffusion Language Models](../../foundation-models/2611.22191-risa/README.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [SIMQ: A Single Graph-based Index for Multi-Vector Query](../../foundation-models/2611.22079-simq/README.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Spool: Low-Latency Streaming Inference for Hybrid Vision-Language Models](../../foundation-models/2611.23228-spool/README.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [UniGraph: A Unified Graph-based Index for Dynamic Hybrid Dense-Sparse Vector Retrieval](../../foundation-models/2611.20758-unigraph/README.md) | 2026-11-16 | l1_mechanism |
| foundation-models | [VisHead-Spec: Head-Routed Visual Attention for Multimodal Speculative Decoding](../../foundation-models/2611.21839-vishead-spec/README.md) | 2026-11-16 | l1_mechanism |
| foundation-models | [WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models](../../foundation-models/2611.21882-wm-quant/README.md) | 2026-11-16 | l1_mechanism |
| multimodal-models | [Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers](../../multimodal-models/2611.22287-dwd/README.md) | 2026-11-17 | 高成本仅收录，不复现 |
| post-training | [Ambient LLMs: Data-Efficient Supervised Fine-tuning via Temperature Matching](../../post-training/2611.23229-ambient-sft/README.md) | 2026-11-17 | l1_mechanism |
| post-training | [Get Hint-Augmented GRPO Done Right Through Activation Steering](../../post-training/2611.23124-ash-hint-steering/README.md) | 2026-11-17 | 高成本仅收录，不复现 |
| post-training | [Contrastive Activation-Guided Zeroth-Order Preference Optimisation for Memory-Efficient LLM Alignment](../../post-training/2611.20635-ca-zodpo/README.md) | 2026-11-16 | l1_mechanism |
| post-training | [Teaching Language Models to Adapt Answer Granularity to Their Confidence](../../post-training/2611.21211-confidence-adaptive-granularity/README.md) | 2026-11-16 | l0_interface |
| post-training | [Learning Design Taste through Verifiable Synthetic Environments and Agentic Reinforcement Learning](../../post-training/2611.20612-design-taste-admission/README.md) | 2026-11-16 | l0_interface |
| post-training | [GPRM: Global Perspective Process Reward Model](../../post-training/2611.20755-gprm/README.md) | 2026-11-16 | 高成本仅收录，不复现 |
| post-training | [Jev-as-a-Reward: Validating Probabilistic Safety Judges for Reinforcement Learning](../../post-training/2611.20955-jev-safety-reward/README.md) | 2026-11-16 | l0_interface |
| post-training | [LEAF-OPD: Learning to Forget from Privileged Contexts via On-Policy Distillation](../../post-training/2611.20674-leaf-opd/README.md) | 2026-11-16 | l1_mechanism |
| post-training | [Margin Dynamics for Large Language Model Alignment](../../post-training/2611.21766-margin-dynamics-tpo/README.md) | 2026-11-16 | l1_mechanism |
| post-training | [Sample-efficient Personalization of Large Language Model Alignment with Multidimensional User Preference Data](../../post-training/2611.22210-mpg-dpo/README.md) | 2026-11-17 | 高成本仅收录，不复现 |
| post-training | [Optimistic Verifiers Get Hacked: Reward Hacking Under an Exact Process Oracle](../../post-training/2611.21538-optimistic-verifier-audit/README.md) | 2026-11-16 | l1_mechanism |
| post-training | [Regularized Score Centering](../../post-training/2611.21791-regularized-score-centering/README.md) | 2026-11-16 | l1_mechanism |
| post-training | [Rethinking Supervision Scaling in On-Policy Distillation: From Dense Supervision to Stochastic Horizons](../../post-training/2611.20687-sh-opd/README.md) | 2026-11-16 | l1_mechanism |
| post-training | [SpeCal: Spectral Calibration for Unsupervised RLVR](../../post-training/2611.20691-specal/README.md) | 2026-11-16 | l1_mechanism |
| post-training | [Streaming On-Policy Distillation: Decoupling Three Clocks for Stage-Wise Supervision Consumption](../../post-training/2611.22298-streaming-opd/README.md) | 2026-11-17 | l1_mechanism |
| post-training | [TAILROLL: Tail-Aware Rollout Acceleration for RL-Based LLM Post-Training](../../post-training/2611.22206-tailroll/README.md) | 2026-11-17 | 高成本仅收录，不复现 |
| recommendation | [COTTI: Contrastive Training and Time-Aware Inference for Robust Industrial Recommendation under Promotional Drift](../../recommendation-components/2611.22597-cotti/README.md) | 2026-11-17 | l1_mechanism |
| recommendation | [CutAgent: Creative-Gene-Driven Planning and Experience-Guided Self-Refinement for High-CTR E-commerce Advertising Video Creation](../../recommendation-components/2611.22418-cutagent/README.md) | 2026-11-17 | 高成本仅收录，不复现 |
| recommendation | [IntentFlow: An Intent-Driven Real-Time Multimodal Search System with Image-Text Queries at Xiaohongshu](../../recommendation-components/2611.20448-intentflow/README.md) | 2026-11-16 | l1_mechanism |
| recommendation | [From Relevance to Utility: Rubric Alignment in Yuanbao Search](../../recommendation-components/2611.22503-yuanbao-rubric/README.md) | 2026-11-17 | l1_mechanism |
