# 11月21日增量扫描与重叠窗口选题

[English](../../en/research-audits/nov21-latest/README.md)

本轮7篇：旧公告池新选题6篇（5篇11月19日首发、MV-JEPA为11月18日首发），另补录官方仓库事件带出的Meta MemLife（9月30日首发）；都不是今天新发表。官方公告仍停在11月20日，本轮捕获元数据中没有核到11月20—21日首发。

## 范围与证据

883条重叠元数据、1081条公告只是召回池；公告身份相较上批新增0条，不是待实现积压。有限选题不代表全来源穷尽，全库审查水位保持11月15日。

Google/Meta优先核对。Meta whole-page ranking正文明确其工业收益是离线referee估计、A100时间是批摊销而非线上延迟，没有核到量化生产A/B，因此不在此悄悄放宽搜广推门槛。Google Duplex新博客不是独立公开算法论文；不可用页面保留为来源例外。

官方目录的56次抓取中54次为来源例外；另2份DeepMind响应原本为gzip，已保留原字节和初始回执后离线重解析。Google目录不能完整比较，未观察到的旧链接不记成已移除。官方仓库事件只是线索，不能把push日当论文首发。

交付7个低成本L1组件；CPU三种子执行全部7项，真实A100验证MV-JEPA一项。完整训练/生成/生产系统实验均为成本过高不复现（审查DONE），不自动重试。本地不是完整模型或Agent能力复现，也不作为Evolve晋级证据。ForeSpark已有高成本终态，本轮不因仓库push自动重开。

[覆盖](source-coverage.json) · [优先核对](priority-primary-selection.json) · [任务账本](task-scope.json) · [运行预算](preflight.json) · [真实A100产物](raw-cuda.json)

## 完整清单

| 领域 | 论文 | 首发 | 本地交付 |
| --- | --- | --- | --- |
| foundation-models | [FrontierReplay: Split-Free Exact Prefix Caching for Hybrid Language Models](../../foundation-models/2611.26020-frontier-replay/README.md) | 2026-11-19 | l1_mechanism |
| foundation-models | [MV-JEPA: Post-Training Video Encoders for Cross-View Understanding](../../foundation-models/2611.25172-mv-jepa/README.md) | 2026-11-18 | l1_mechanism |
| agent-research | [Sage-Evolve-Preview: Adaptive Observation for Post-Training Self-Improvement](../../agent-research/2611.26132-sage-evolve/README.md) | 2026-11-19 | l1_mechanism |
| agent-research | [MemFolder: Structure-Guided Memory Folding for Efficient Agent Memory Management](../../agent-research/2611.26427-memfolder/README.md) | 2026-11-19 | l1_mechanism |
| post-training | [Decision-Focused Reinforcement Learning for LLM Post-Training](../../post-training/2611.25597-dfrl/README.md) | 2026-11-19 | l1_mechanism |
| foundation-models | [Sequential Anytime Valid Tests for Efficient Inference-Time Alignment](../../foundation-models/2611.26413-e-rwsc/README.md) | 2026-11-19 | l1_mechanism |
| agent-research | [MemLife: Curating and Reasoning over Long-Term Egocentric Video Memories](../../agent-research/2609.40195-memlife/README.md) | 2026-09-30 | l1_mechanism |
