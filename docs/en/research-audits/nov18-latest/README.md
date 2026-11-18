<!-- source-sha256: b07ff22256dade883d467d6624d8a0175e46d0d414a9523bcef8a79be7a3fa43 -->
# November16–18 paper refresh and delivery

[简体中文](../../../research-audits/nov18-latest/README.md)

47 items:46 papers first published in the window and1 historical paper with a new official code release;35 bounded components and12 review-only high-cost papers.22 CUDA components were executed on a real A100 with three seeds.189 bilingual questions and47 same-topic deep-dive updates.

## Scope and evidence

This is finite selection and delivery, not full-text exhaustion across every source/paper. The3369 metadata identities include November13 overlap, older revisions and cross-lists; they are neither3369 new papers nor an implementation backlog. The global review watermark is unchanged.

Google/Meta official directories, public repository events and fixed-paper bylines were prioritized. Meta VisHead-Spec has bounded operators. Google efficient_evals was released on November16 for a March2 paper and is counted as historical new-code backfill. Offline production-derived replay, including KVUse, is not mislabeled production A/B.

Local L0/L1 diagnostics establish neither model capability, production lift nor Evolve promotion. High-cost full experiments are explicitly not reproduced, review DONE, with no automatic retry. An incorrect WM-Quant grid diagnostic remains preserved as invalidated; corrected source was frozen and executed again.

Sources: [coverage](../../../research-audits/nov18-latest/source-coverage.json), [Google/Meta primary selection](../../../research-audits/nov18-latest/priority-primary-selection.json), [delivery ledger](../../../research-audits/nov18-latest/task-scope.json), [cost preflight](../../../research-audits/nov18-latest/preflight.json), [actual CUDA run](../../../research-audits/nov18-latest/raw-cuda.json).

## Delivery list

| Domain | Paper | First publication | Local delivery |
| --- | --- | --- | --- |
| agent-research | [Instant Weight-Space Consolidation for Long-Term Memory in LLMs](../../../agent-research/2611.20759-clam-memory/README-en.md) | 2026-11-16 | Review only; full campaign not reproduced |
| agent-research | [DetourBench: Trajectory-Level Evaluation of Interactive Agents with Exact Minimum-Action Bounds](../../../agent-research/2611.20844-detourbench/README-en.md) | 2026-11-16 | l1_mechanism |
| agent-research | [Evaluation-Free Recursive Self-Improvement for Coding Agents](../../../agent-research/2611.21056-elite-eval-free/README-en.md) | 2026-11-16 | l0_interface |
| agent-research | [Verifying Agents in Rubric-Graded Environments](../../../agent-research/2611.22841-gandalf-bvb/README-en.md) | 2026-11-17 | Review only; full campaign not reproduced |
| agent-research | [MetaAct: Self-Evolving Executable Action Constraints for Embodied Language Agents](../../../agent-research/2611.20655-metaact/README-en.md) | 2026-11-16 | l1_mechanism |
| agent-research | [The Resolution Hypothesis: Agent Evolution's Key Is Identifying Improvements](../../../agent-research/2611.23068-resolution-hypothesis/README-en.md) | 2026-11-17 | l1_mechanism |
| agent-research | [SciResearch-Eval: Evaluating Scientific Judgment in Autonomous Experimental Agents](../../../agent-research/2611.21541-sciresearch-eval/README-en.md) | 2026-11-16 | l1_mechanism |
| agent-research | [Do LLM Agents Still Need to Be Told How to Self-Improve?](../../../agent-research/2611.23219-self-organized-learning/README-en.md) | 2026-11-17 | Review only; full campaign not reproduced |
| agent-research | [Invariant-Aware Harness Enforcement to Protect LLM Agents from Silent API Failures](../../../agent-research/2611.20595-silentguard/README-en.md) | 2026-11-16 | l1_mechanism |
| agent-research | [SkillBuffBench: Measuring What Agent Skills Contribute across Harnesses, Models, Skill Access Modes and Memory](../../../agent-research/2611.22017-skillbuffbench/README-en.md) | 2026-11-17 | Review only; full campaign not reproduced |
| foundation-models | [Beyond Bitwidth: Deployment-Constrained Mixed-Precision Quantization for Multilingual LLM Inference on NVIDIA Blackwell](../../../foundation-models/2611.21974-beyond-bitwidth/README-en.md) | 2026-11-16 | Review only; full campaign not reproduced |
| foundation-models | [CascadeJEPA: Enhancing 3D Geometric Representations via Spatially Coupled Cascaded Prediction](../../../foundation-models/2611.22686-cascadejepa/README-en.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Deal With It: On Better Schedules for Listwise Reranking](../../../foundation-models/2611.22392-dealrank/README-en.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Communicate the Change: Efficient Expert Parallelism via Activation Compression](../../../foundation-models/2611.22215-echomoe/README-en.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Rich Insights from Cheap Signals: Efficient Evaluations via Tensor Factorization](../../../foundation-models/2603.02029-efficient-evals-tensor/README-en.md) | 2026-03-02 | l1_mechanism |
| foundation-models | [FM-Mamba: An Efficient Native 2D Selective State Space Model with Stability-Aware Discretization](../../../foundation-models/2611.22061-fm-mamba/README-en.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [GaugeRoPE: RoPE-Compatible Executable Latent Attention](../../../foundation-models/2611.20524-gaugerope/README-en.md) | 2026-11-16 | l1_mechanism |
| foundation-models | [InfuseLoop: Cross-Trajectory Latent Injection for Scalable Parallel Looped Transformers](../../../foundation-models/2611.22426-infuseloop/README-en.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [The Kernel Reality Check: Benchmarking and Distilling Efficient Attention at Scale](../../../foundation-models/2611.22947-lara-plus-plus/README-en.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Latent Feedback Is a Compute and Data Amplifier](../../../foundation-models/2611.20404-latent-feedback-scaling/README-en.md) | 2026-11-16 | Review only; full campaign not reproduced |
| foundation-models | [RISA: Recoverable Sparse Attention for Block-Diffusion Language Models](../../../foundation-models/2611.22191-risa/README-en.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [SIMQ: A Single Graph-based Index for Multi-Vector Query](../../../foundation-models/2611.22079-simq/README-en.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [Spool: Low-Latency Streaming Inference for Hybrid Vision-Language Models](../../../foundation-models/2611.23228-spool/README-en.md) | 2026-11-17 | l1_mechanism |
| foundation-models | [UniGraph: A Unified Graph-based Index for Dynamic Hybrid Dense-Sparse Vector Retrieval](../../../foundation-models/2611.20758-unigraph/README-en.md) | 2026-11-16 | l1_mechanism |
| foundation-models | [VisHead-Spec: Head-Routed Visual Attention for Multimodal Speculative Decoding](../../../foundation-models/2611.21839-vishead-spec/README-en.md) | 2026-11-16 | l1_mechanism |
| foundation-models | [WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models](../../../foundation-models/2611.21882-wm-quant/README-en.md) | 2026-11-16 | l1_mechanism |
| multimodal-models | [Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers](../../../multimodal-models/2611.22287-dwd/README-en.md) | 2026-11-17 | Review only; full campaign not reproduced |
| post-training | [Ambient LLMs: Data-Efficient Supervised Fine-tuning via Temperature Matching](../../../post-training/2611.23229-ambient-sft/README-en.md) | 2026-11-17 | l1_mechanism |
| post-training | [Get Hint-Augmented GRPO Done Right Through Activation Steering](../../../post-training/2611.23124-ash-hint-steering/README-en.md) | 2026-11-17 | Review only; full campaign not reproduced |
| post-training | [Contrastive Activation-Guided Zeroth-Order Preference Optimisation for Memory-Efficient LLM Alignment](../../../post-training/2611.20635-ca-zodpo/README-en.md) | 2026-11-16 | l1_mechanism |
| post-training | [Teaching Language Models to Adapt Answer Granularity to Their Confidence](../../../post-training/2611.21211-confidence-adaptive-granularity/README-en.md) | 2026-11-16 | l0_interface |
| post-training | [Learning Design Taste through Verifiable Synthetic Environments and Agentic Reinforcement Learning](../../../post-training/2611.20612-design-taste-admission/README-en.md) | 2026-11-16 | l0_interface |
| post-training | [GPRM: Global Perspective Process Reward Model](../../../post-training/2611.20755-gprm/README-en.md) | 2026-11-16 | Review only; full campaign not reproduced |
| post-training | [Jev-as-a-Reward: Validating Probabilistic Safety Judges for Reinforcement Learning](../../../post-training/2611.20955-jev-safety-reward/README-en.md) | 2026-11-16 | l0_interface |
| post-training | [LEAF-OPD: Learning to Forget from Privileged Contexts via On-Policy Distillation](../../../post-training/2611.20674-leaf-opd/README-en.md) | 2026-11-16 | l1_mechanism |
| post-training | [Margin Dynamics for Large Language Model Alignment](../../../post-training/2611.21766-margin-dynamics-tpo/README-en.md) | 2026-11-16 | l1_mechanism |
| post-training | [Sample-efficient Personalization of Large Language Model Alignment with Multidimensional User Preference Data](../../../post-training/2611.22210-mpg-dpo/README-en.md) | 2026-11-17 | Review only; full campaign not reproduced |
| post-training | [Optimistic Verifiers Get Hacked: Reward Hacking Under an Exact Process Oracle](../../../post-training/2611.21538-optimistic-verifier-audit/README-en.md) | 2026-11-16 | l1_mechanism |
| post-training | [Regularized Score Centering](../../../post-training/2611.21791-regularized-score-centering/README-en.md) | 2026-11-16 | l1_mechanism |
| post-training | [Rethinking Supervision Scaling in On-Policy Distillation: From Dense Supervision to Stochastic Horizons](../../../post-training/2611.20687-sh-opd/README-en.md) | 2026-11-16 | l1_mechanism |
| post-training | [SpeCal: Spectral Calibration for Unsupervised RLVR](../../../post-training/2611.20691-specal/README-en.md) | 2026-11-16 | l1_mechanism |
| post-training | [Streaming On-Policy Distillation: Decoupling Three Clocks for Stage-Wise Supervision Consumption](../../../post-training/2611.22298-streaming-opd/README-en.md) | 2026-11-17 | l1_mechanism |
| post-training | [TAILROLL: Tail-Aware Rollout Acceleration for RL-Based LLM Post-Training](../../../post-training/2611.22206-tailroll/README-en.md) | 2026-11-17 | Review only; full campaign not reproduced |
| recommendation | [COTTI: Contrastive Training and Time-Aware Inference for Robust Industrial Recommendation under Promotional Drift](../../../recommendation-components/2611.22597-cotti/README-en.md) | 2026-11-17 | l1_mechanism |
| recommendation | [CutAgent: Creative-Gene-Driven Planning and Experience-Guided Self-Refinement for High-CTR E-commerce Advertising Video Creation](../../../recommendation-components/2611.22418-cutagent/README-en.md) | 2026-11-17 | Review only; full campaign not reproduced |
| recommendation | [IntentFlow: An Intent-Driven Real-Time Multimodal Search System with Image-Text Queries at Xiaohongshu](../../../recommendation-components/2611.20448-intentflow/README-en.md) | 2026-11-16 | l1_mechanism |
| recommendation | [From Relevance to Utility: Rubric Alignment in Yuanbao Search](../../../recommendation-components/2611.22503-yuanbao-rubric/README-en.md) | 2026-11-17 | l1_mechanism |
