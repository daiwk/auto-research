# 11月23日近期论文与Google目录补录

[English](../../en/research-audits/nov23-latest/README.md)

本轮9篇：8篇11月20日首发、本次相较11月21日元数据新捕获；另有Google合作的SPOT-Bench，4月27日首发、核对11月5日v2的历史目录补录。不是11月23日新发9篇。

## 范围与证据

官方重叠池1260条、旧公告1081个身份只作召回；本次核到160条11月20日首发，未核到11月21—23日首发，公告身份新增0。提交、修订、公告、发现和审查日期分开，不猜新选题公告日。有限选题不是全来源审查，水位保持11月15日。

Google DeepMind DISCO优先收录；SPOT按固定v2一作NUS、Yale Song署名Google，不因官方目录调换一作。官方目录54/56页面完成链接解析，两份Meta落地页缺少完整出版清单。14条Google目录增量是对Nov15有限目录的差，不是14篇新首发；SearchInject/LogAct等已有条目不因push重开。缺全文的硬件AI线索作为来源限制归档。

交付7个L1机制/计分组件，全部CPU三seed，AIMuon另有真实A100三seed；没有下载模型/数据或调用API。CTRL与CoEvoBench只收录，高成本完整实验不复现（审查DONE），不是待跑TODO。其余7篇的完整能力实验同样不复现；机制负控与合成分数不等于论文benchmark，不接Evolve晋级。

[任务范围](task-scope.json) · [覆盖](source-coverage.json) · [优先来源](priority-primary-selection.json) · [预算](preflight.json) · [CPU实跑](raw-cpu.json) · [A100实跑](raw-cuda.json)

## 完整清单

| 领域 | 论文 | 首发 | 交付 |
| --- | --- | --- | --- |
| foundation-models | [Reliable Behavior Discovery via False Discovery Rate Control](../../foundation-models/2611.27104-disco/README.md) | 2026-11-20 | L1组件 |
| agent-research | [From Acting to Learning: Experience Selection toward Continually Learning Agents](../../agent-research/2611.27159-acting-to-learning/README.md) | 2026-11-20 | L1组件 |
| agent-research | [$R^2$: Recognizing and Reducing Redundant Visual Tool Use](../../agent-research/2611.27070-r2-tool-redundancy/README.md) | 2026-11-20 | L1组件 |
| agent-research | [CoEvoBench: Can LLMs Drive Recursive Co-Evolution of Agentic Systems?](../../agent-research/2611.27116-coevobench/README.md) | 2026-11-20 | 高成本不复现 |
| post-training | [Distillation with Errors: Sparse Unbiased Backpropagation for Knowledge Distillation](../../post-training/2611.27131-dwe/README.md) | 2026-11-20 | L1组件 |
| post-training | [How Far Does Lossless Re-tokenization Move an RLVR Update?](../../post-training/2611.27083-retokenization-update/README.md) | 2026-11-20 | L1组件 |
| post-training | [CTRL: Concurrent Training and Rollout for LLM Reinforcement Learning via GPU Co-Residency](../../post-training/2611.27119-ctrl/README.md) | 2026-11-20 | 高成本不复现 |
| foundation-models | [Accelerating Muon with Spectral Residual Correction](../../foundation-models/2611.27077-aimuon/README.md) | 2026-11-20 | L1组件 |
| foundation-models | [Don't Pause! Every prediction matters in a streaming video](../../foundation-models/2604.24317-spot-bench/README.md) | 2026-04-27 | L1组件 |
