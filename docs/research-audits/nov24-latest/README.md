# 11月24日期间增量选题与Google历史补录

[English](../../en/research-audits/nov24-latest/README.md)

本轮8篇：6篇11月23日首发、Pinterest Weight Coding为11月22日；Google最新博客带出DCA（2025年2月10日首发、核对2025年7月23日v2）历史遗漏。不是8篇今天新发。VOPD有Google DeepMind合作者，一作仍Stanford；DCA一作UCI，不改写机构。

官方重叠池2597条、11月23日公告883个身份仅作召回。相对上批新捕获的近日期首发分布为{'2026-11-20': 406, '2026-11-21': 302, '2026-11-22': 300, '2026-11-23': 464}，并不代表同等数量符合标准或待实现。未观察到11月24日首发；不猜选题公告日。本轮不是全来源审查闭环，审查水位仍11月15日。

7个L1低成本机制组件完成CPU三seed，DCA另有真实单A100三seed。MORSE仅收录；所有完整高成本实验明确不复现（审查DONE），无自动重试。没有模型/数据下载或API调用，没有能力排名或Evolve晋级。Weight Coding核对正文§4.7/Table4真实线上A/B，但source-attributed收益不能冒充站点总收益。

[范围](task-scope.json) · [覆盖](source-coverage.json) · [优先来源](priority-primary-selection.json) · [预算](preflight.json) · [CPU](raw-cpu.json) · [GPU](raw-cuda.json)

## 完整清单

| 领域 | 论文 | 首发 | 交付 |
| --- | --- | --- | --- |
| foundation-models | [DeepCrossAttention: Supercharging Transformer Residual Connections](../../foundation-models/2502.06785-deep-cross-attention/README.md) | 2025-02-10 | L1组件 |
| foundation-models | [The KL Divergence Is Never Negative, Except in PyTorch](../../foundation-models/2611.30835-stablekl/README.md) | 2026-11-23 | L1组件 |
| agent-research | [Optimistic Online Learning for Coding Agents with Aggregate Feedback](../../agent-research/2611.30405-ooas/README.md) | 2026-11-23 | L1组件 |
| agent-research | [Transport-Safe Evaluation of LLM Agents: Trajectory-Dependent Judge Error and Anytime-Valid Auditing](../../agent-research/2611.30742-transport-safe-audit/README.md) | 2026-11-23 | L1组件 |
| agent-research | [MORSE: Optimizing Streaming Memory Design via Open-World Auto-Research](../../agent-research/2611.30011-morse/README.md) | 2026-11-23 | 高成本不复现 |
| post-training | [Verifiable On-Policy Distillation](../../post-training/2611.30325-vopd/README.md) | 2026-11-23 | L1组件 |
| post-training | [Sparse Hodge Preference Optimization: Fine-Tuning Language Models toward Alignment beyond Transitive Preferences](../../post-training/2611.30135-shpo/README.md) | 2026-11-23 | L1组件 |
| recommendation | [Weight Coding: Evolving Web-Scale Recommenders through Direct Weight Edits with LLM Agents](../../recommendation-components/2611.29613-weight-coding/README.md) | 2026-11-22 | L1组件 |
