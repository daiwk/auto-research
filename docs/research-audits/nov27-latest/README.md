# 11月27日重叠池与版本补录

[English](../../en/research-audits/nov27-latest/README.md)

本轮7项不是7篇今天新发：5篇11月24日首发、1篇11月25日首发；ELBO-TDS最早2025年发表，本次由11月25日v2带出。7个L1机制组件，不是完整模型/Agent能力复现，均未接入Evolve晋级。

实际捕获2091条元数据和1157个公告身份；最新首发仍11月25日，公告仍11月26日，未观察到11月26日新首发。新增捕获不等于新增发表，API重叠边界抓全也不等于逐篇审查闭环。水位保持11月15日。

Google/Meta优先核验：相对上一批Google目录新增0；Meta新JEP-AV仓库仅ComingSoon，未有可核方法/论文身份；Habitats是source-only框架，Psyre/COrigami及DISCO的维护/释码不伪称新论文。来源异常保留。

所有组件完成CPU三seed，ELBO-TDS另有真实A100三seed。DeCo是CPU低精度数学仿真，不是A100原生FP4核/加速测试。Compute-aware完整公开模拟可能可负担，未承接完整范围，不硬标高成本；其余昂贵完整实验终态不复现（审查DONE）。0模型/训练数据下载、0模型API。

[固定范围](task-scope.json) · [来源覆盖](source-coverage.json) · [优先主源](priority-primary-selection.json) · [CPU](raw-cpu.json) · [GPU](raw-cuda.json)

## 完整清单

| 领域 | 论文 | 首发 | 交付 |
| --- | --- | --- | --- |
| foundation-models | [Integral DeltaNet: Improved Linear Attention with Adaptive Memory Integration](../../foundation-models/2611.32063-integral-deltanet/README.md) | 2026-11-24 | L1机制组件 |
| foundation-models | [DeCo-Attention: Decompose to Compensate for Low-Precision Attention](../../foundation-models/2611.32035-deco-attention/README.md) | 2026-11-24 | L1机制组件 |
| post-training | [Scoring What Matters: Exact Feedback Reduction for Language Model Comparison](../../post-training/2611.31931-cafa/README.md) | 2026-11-24 | L1机制组件 |
| post-training | [The Teacher Is Already Inside: Self-Distilling Looped Language Models Beyond Their Last Loop](../../post-training/2611.32452-elpsd/README.md) | 2026-11-24 | L1机制组件 |
| agent-research | [LLM Agent Authorization Across Context Compaction](../../agent-research/2611.32194-compaction-authorization/README.md) | 2026-11-24 | L1机制组件 |
| agent-research | [Compute-Aware Submodular Online Learning in Open Multi-Agent Systems](../../agent-research/2611.34211-budgeted-submapl/README.md) | 2026-11-25 | L1机制组件 |
| recommendation | [ELBO_TDS: Temporal Distribution Shift Generalization for Industry-Scale Recommender Systems](../../recommendation-components/2511.21032-elbo-tds/README.md) | 2025-11-26 | L1机制组件 |
