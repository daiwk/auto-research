# 11月25日近期论文增量选题

[English](../../en/research-audits/nov25-latest/README.md)

本轮9篇均为11月24日首发、11月25日选题交付，不是9篇今天新发：LazUnirec、LARF、UDVR、Thresholded LongCE、EPRO、Agent-Kernel、CAPE、CriticJEPA、RecurSciBench。前两篇有正文生产A/B；Google/Meta官方新增线索、旧论文和仓库release另作优先核验，不把开仓/push日期当新论文。

官方重叠池1982条、11月24日公告2128个身份仅作召回。相对Nov24批次，新捕获近期首发分布为{'2026-11-23': 277, '2026-11-24': 557}，不是合格论文数量或实现积压。未观察到11月25日首发；不猜本轮选题公告日。有限增量不等于全窗口审查闭环，审查水位仍11月15日。

7个L1局部机制/协议组件完成CPU三seed；LazUnirec另有真实单A100三seed。CriticJEPA与RecurSciBench仅资料收录。所有高成本完整矩阵均不复现（审查DONE），无自动重试。没有checkpoint/数据下载、API调用、完整模型/Agent能力复现或Evolve晋级。CAPE小型诊断为求最优实际校准全20格，没有取得校准节省，负结果保留；不能套用论文速度收益。

[范围](task-scope.json) · [覆盖](source-coverage.json) · [优先来源](priority-primary-selection.json) · [预算](preflight.json) · [CPU](raw-cpu.json) · [GPU](raw-cuda.json)

## 完整清单

| 领域 | 论文 | 首发 | 交付 |
| --- | --- | --- | --- |
| foundation-models | [Weight Scale Rebalancing: Transferable Training Recipes for Transformers](../../foundation-models/2611.32866-udvr/README.md) | 2026-11-24 | L1组件 |
| foundation-models | [Eliciting the Recall Capacity of Linear Attention](../../foundation-models/2611.32969-thresholded-longce/README.md) | 2026-11-24 | L1组件 |
| foundation-models | [CriticJEPA: World Models Are Better Critics Than Optimizers](../../foundation-models/2611.32357-criticjepa/README.md) | 2026-11-24 | 高成本不复现 |
| agent-research | [fork() for Agents: Agent Kernel for Non-blocking LLM Orchestration](../../agent-research/2611.31727-agent-kernel/README.md) | 2026-11-24 | L1组件 |
| agent-research | [CAPE: Coordinating Calibration and Search for Tool-Use Policies](../../agent-research/2611.31938-cape/README.md) | 2026-11-24 | L1组件 |
| agent-research | [RecurSciBench: Benchmarking Recursive Self-Improvement in Data-Driven Scientific Research](../../agent-research/2611.32508-recurscibench/README.md) | 2026-11-24 | 高成本不复现 |
| post-training | [EPRO: Robust Policy Optimization Through an Imperfect Execution-Policy Predictor](../../post-training/2611.32810-epro/README.md) | 2026-11-24 | L1组件 |
| recommendation | [LARF: Learning-aligned Reasoning Framework for Search Relevance](../../recommendation-components/2611.32125-larf/README.md) | 2026-11-24 | L1组件 |
| recommendation | [LazUnirec: Unifying Retrieval and Ranking in Multi-scenario Industrial Recommendation](../../recommendation-components/2611.32590-lazunirec/README.md) | 2026-11-24 | L1组件 |
