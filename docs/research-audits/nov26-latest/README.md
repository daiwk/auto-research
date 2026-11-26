# 11月26日近期论文增量选题

[English](../../en/research-audits/nov26-latest/README.md)

本轮11篇均为11月25日首发，不是11篇今天新发。低成本交付为RAP、DuoMI、BRIAR、FEAST、HoMe、OneQuery、CAMAR七个L1机制组件及DualPM一个L0回调接口；JEPA EU、CARE-OPD、Agentic LongLive三篇高成本仅收录。OneQuery/CAMAR均核对正文生产A/B，作者线上结果与本地小组件分开。

本轮官方重叠池1200条、当前公告1157个身份仅作召回；相对上一批新捕获近期首发分布为{'2026-11-24': 194, '2026-11-25': 595}，不是合格论文数量或实现积压。日期口径见覆盖记录，不推定选题公告日。有限选题不等于全窗口审查闭环，水位仍11月15日。

八个组件/接口完成CPU三seed，CAMAR另有真实单A100三seed。RAP核心CPU实验本身可负担，本轮未执行其完整公开评测矩阵，标not_run_scope_limited而非伪造高成本；其余已评估为高成本的完整训练/API矩阵终态不复现（审查DONE），无自动重试。没有checkpoint/训练数据下载、API调用、完整能力复现或Evolve晋级。

Google/Meta优先目录与仓库核验见优先来源记录：新Google博客对应已有FUSE，旧论文释码/普通维护不当新论文；SCALE4D官方技术报告单列原文成本审查与首次公开日期限制，不把submit号当正式arXiv身份。

[范围](task-scope.json) · [覆盖](source-coverage.json) · [优先来源](priority-primary-selection.json) · [预算](preflight.json) · [CPU](raw-cpu.json) · [GPU](raw-cuda.json)

## 完整清单

| 领域 | 论文 | 首发 | 交付 |
| --- | --- | --- | --- |
| foundation-models | [RAP: Radial-Angular Random Projection for Hyperbolic Representations](../../foundation-models/2611.34298-rap/README.md) | 2026-11-25 | L1组件 |
| foundation-models | [DuoMI: Dual Mutual Information Regularization for Expert Reuse in Looped Transformers](../../foundation-models/2611.33952-duomi/README.md) | 2026-11-25 | L1组件 |
| foundation-models | [Not all world models can doubt: how training objective and architecture shape epistemic uncertainty in JEPA and RSSM world models](../../foundation-models/2611.34830-jepa-eu/README.md) | 2026-11-25 | 高成本不复现 |
| agent-research | [HoMe: Toward Practical Harness Optimization of Memory Systems for AI Assistants](../../agent-research/2611.34624-home/README.md) | 2026-11-25 | L1组件 |
| agent-research | [Failure Broadens, Success Sharpens: Continual Adaptation of Tool-Use Agents Across Diverse Tasks with Dual-Polarity Memory](../../agent-research/2611.33612-dualpm/README.md) | 2026-11-25 | L0接口 |
| multimodal-models | [Agentic LongLive: Asynchronous Agentic Memory for Long Video Generation](../../multimodal-models/2611.34907-agentic-longlive/README.md) | 2026-11-25 | 高成本不复现 |
| post-training | [BRIAR: Martingale Belief Smoothing on Bifurcation-Guided Reasoning Trees](../../post-training/2611.34746-briar/README.md) | 2026-11-25 | L1组件 |
| post-training | [FEAST: Fair and Efficient Adaptive Sampling for Task-Free On-Policy Learning](../../post-training/2611.33827-feast/README.md) | 2026-11-25 | L1组件 |
| post-training | [Collect for Coverage, Replay with Evidence: Adaptive and Efficient On-Policy Distillation for Long-Horizon Agents](../../post-training/2611.34756-care-opd/README.md) | 2026-11-25 | 高成本不复现 |
| recommendation | [OneQuery: Unified Sequence-to-Structure Generation for Multilingual E-commerce Query Understanding](../../recommendation-components/2611.33653-onequery/README.md) | 2026-11-25 | L1组件 |
| recommendation | [Multi-Modal Causal Disentanglement for Multi-Domain Sequential Audio Recommendation](../../recommendation-components/2611.33628-camar/README.md) | 2026-11-25 | L1组件 |
