# 11月20日论文扫描与交付

[English](../../en/research-audits/nov20-latest/README.md)

本轮11项：7篇11月19日首发、3篇11月18日首发/今日公告补录、1篇11月12日Canon历史补录。9个低成本组件/接口、2篇高成本仅收录；4个CUDA组件在真实A100完成42/43/44三种子验证。44道逐题校对中英问答和11条同主题深读更新。

## 范围与证据

1884条重叠元数据、1081条公告是召回池，不是新增论文或待办数量。仅对固定选题和显式排除做相应层级的原文核对，不宣称全来源穷尽；全库审查水位保持11月15日不变。首发、公告、目录观察和仓库push分开记录。

Google BuggyMLE与Meta舰队特征优化优先核验；Canon当前一作机构为Allen-Zhu Research，FAIR/Meta是实验执行来源，不改写成当前Meta署名。LSER线上A/B未启用LLM辅助特征，不能把整体线上收益归给LLM。

全部运行是L0/L1诊断，不是模型能力、线上收益或Evolve晋级。高成本完整实验明确不复现、审查DONE，不自动重试。VisAlloc半精度与HiSA无符号位置问题均在最终冻结前修复，早期未执行快照与旧独立CPU事实保留。GrepMem只是新组件的显式日志查询，不读取本机Codex记录，也不提供磁盘压缩。

[覆盖](source-coverage.json) · [优先来源](priority-primary-selection.json) · [任务账本](task-scope.json) · [执行预算](preflight.json) · [真实A100产物](raw-cuda.json)

## 完整清单

| 领域 | 论文 | 首发 | 本地交付 |
| --- | --- | --- | --- |
| agent-research | [BuggyMLE: Scaling Machine Learning Engineering Difficulty with Bug Injection](../../agent-research/2611.25088-buggymle-cci/README.md) | 2026-11-18 | l0_interface |
| agent-research | [Forget Freely, Grep Later: Lossless, Index-Free Memory for Long-Horizon LLM Agents](../../agent-research/2611.25123-grepmem/README.md) | 2026-11-18 | l1_mechanism |
| system-one | [Stop Going in Circles:Loop-Triggered Routing for System 1 Decision Agents](../../system-one/2611.25363-looproute/README.md) | 2026-11-19 | l1_mechanism |
| foundation-models | [HiSA: Sparsifying the Hidden Dimension of RoPE Attention in LLMs](../../foundation-models/2611.26363-hisa/README.md) | 2026-11-19 | l1_mechanism |
| foundation-models | [Physics of Language Models: Part 4.2, Canon Layers at Scale where Synthetic Pretraining Resonates in Reality](../../foundation-models/2611.24963-canon-layers-scale/README.md) | 2026-11-12 | 高成本仅收录，不复现 |
| post-training | [Policy Improvement-Guided Replay for Continual Reinforcement Learning](../../post-training/2611.25989-colir-replay/README.md) | 2026-11-19 | l1_mechanism |
| post-training | [VisAlloc: Allocating Visual Supervision for On-Policy Self-Distillation](../../post-training/2611.25069-visalloc/README.md) | 2026-11-18 | l1_mechanism |
| recommendation | [Cost-Aware Agentic Feature Optimization System for Fleet-Scale Ranking Models](../../recommendation-components/2611.26531-fleet-feature-optimization/README.md) | 2026-11-19 | l1_mechanism |
| recommendation | [DNA: Unlocking Depth Scaling in CTR Models](../../recommendation-components/2611.25659-dna/README.md) | 2026-11-19 | l1_mechanism |
| recommendation | [From Sessions to Serving: Integrating LLM-Based Embeddings into Retrieval for Production Content Recommendation](../../recommendation-components/2611.26096-lser-serving/README.md) | 2026-11-19 | l0_interface |
| recommendation | [Antom 3-in-1 Transformer: A Payment Foundation Model](../../recommendation-components/2611.25403-antom-3-in-1/README.md) | 2026-11-19 | 高成本仅收录，不复现 |
