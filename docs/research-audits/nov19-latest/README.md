# 11月19日论文扫描与交付

[English](../../en/research-audits/nov19-latest/README.md)

本轮23项：21篇11月18日新首发、1篇11月17日首发/今日公告补录的Meta AVM、1篇11月2日Google SearchInject历史目录补录。18个低成本组件/接口、5篇高成本仅收录；7个CUDA组件在真实A100完成42/43/44三种子验证。92道逐题校对中英问答、23条同主题深读更新。

## 范围与证据

这是有限选题扫描，不是全来源/全机构穷尽审查。2781条重叠元数据与1082条当前公告不是新增论文数，也不是实现待办。本轮不改变全库审查水位。论文首发、公告、目录新增和仓库push分开记录。

Google/Meta优先：MLE Agents核对Meta作者栏和真实A/B，同时保留延迟护栏退化；AVM完整8M视频训练高成本不复现；SearchInject只证明检索暴露控制，不证明攻击成功下降。CWM作者当前为Brown/AMI与NYU/AMI，不凭熟悉姓名标Meta；X-split原文未列机构，不猜Yandex。

本地均为L0/L1诊断，不是模型能力、线上收益或Evolve晋级。高成本完整实验明确成本过高，不复现（审查 DONE），不自动重试。交叉复核发现的ECA/MRPD掩码指数溢出已在冻结前修复并加入极端值负控。

最终跨主题复核补入Jeveration、EgoJev和JEPA Dots。EgoJev的显式概率CPU后处理用独立冻结组执行；已完成的17组件主体和7个A100结果保持原样，不覆盖或冒充再次测量。新增两篇的完整生成/机器人训练仅收录、不复现。

[来源覆盖](source-coverage.json) · [优先来源核对](priority-primary-selection.json) · [完整交付账本](task-scope.json) · [成本与执行预算](preflight.json) · [真实CUDA产物](raw-cuda.json)

## 完整清单

| 领域 | 论文 | 首发 | 本地交付 |
| --- | --- | --- | --- |
| agent-research | [Agentic Harness Engineering Beta: Requirement-Centered Evolution of Agent Harnesses](../../agent-research/2611.24924-ahe-beta/README.md) | 2026-11-18 | l0_interface |
| agent-research | [Can Programs Replace LLM Judges? Executable Program Judges for Scalable and Efficient Relevance Labeling](../../agent-research/2611.24849-execjudges/README.md) | 2026-11-18 | l0_interface |
| agent-research | [Kaer: Security-Aware Replanning for Multi-Agent Systems](../../agent-research/2611.24839-kaer/README.md) | 2026-11-18 | l1_mechanism |
| agent-research | [RSIBench-Infra: Can Agents Optimize Their Own Training and Inference Infrastructure at Production Scale?](../../agent-research/2611.24395-rsibench-infra/README.md) | 2026-11-18 | 高成本仅收录，不复现 |
| agent-research | [Safe Personal RSI: Evaluating and Repairing Personal-Agent Updates](../../agent-research/2611.23651-safe-personal-rsi/README.md) | 2026-11-18 | l1_mechanism |
| agent-research | [SearchInject: Retrieval Exposure Control for Indirect Prompt Injection in Language-Model Search](../../agent-research/2611.02643-searchinject/README.md) | 2026-11-02 | l1_mechanism |
| agent-research | [Reducing Inference Cost of Coding Agents with Timeout Cascades](../../agent-research/2611.24324-timeout-cascades/README.md) | 2026-11-18 | l1_mechanism |
| foundation-models | [Counterfactual World Models: JEPAs That Reason About "What If"](../../foundation-models/2611.24778-counterfactual-wm/README.md) | 2026-11-18 | l1_mechanism |
| foundation-models | [Kernel Ridge Attention: Nonlinear Memory with Selective Forgetting](../../foundation-models/2611.23896-kernel-ridge-attention/README.md) | 2026-11-18 | l1_mechanism |
| foundation-models | [LoopCache: Accelerating Long-Context Self-Speculative Decoding for Looped Transformers](../../foundation-models/2611.24301-loopcache-interface/README.md) | 2026-11-18 | l0_interface |
| foundation-models | [NarrowSpec: Draft Hidden Width Need Not Match the Target in Speculative Decoding](../../foundation-models/2611.23835-narrow-spec/README.md) | 2026-11-18 | l1_mechanism |
| multimodal-models | [Autoregressive View Model](../../multimodal-models/2611.23417-autoregressive-view-model/README.md) | 2026-11-17 | 高成本仅收录，不复现 |
| multimodal-models | [JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control](../../multimodal-models/2611.24062-jepa-dots/README.md) | 2026-11-18 | 高成本仅收录，不复现 |
| post-training | [How Reward Gain Imbalance Shapes Ranking: Rethinking Rubric-Based Reward Aggregation](../../post-training/2611.24005-dcc-aggregation/README.md) | 2026-11-18 | l1_mechanism |
| post-training | [Evidence-Based Credit Assignment for Search-Augmented Language Models](../../post-training/2611.23824-eca-credit/README.md) | 2026-11-18 | l1_mechanism |
| post-training | [HINT-WAM: Hindsight-Informed Training for World Action Models](../../post-training/2611.24789-hint-wam/README.md) | 2026-11-18 | 高成本仅收录，不复现 |
| post-training | [Beyond Replacement: Levenshtein Editing for Diffusion Language Models](../../post-training/2611.23750-led-edits/README.md) | 2026-11-18 | l1_mechanism |
| post-training | [Replay, Don't Resample: Off-Policy Consolidation of Long-Horizon RL Experts](../../post-training/2611.24059-mrpd-replay/README.md) | 2026-11-18 | l1_mechanism |
| recommendation | [MARS Technical Report](../../recommendation-components/2611.24006-mars-fapo/README.md) | 2026-11-18 | l1_mechanism |
| recommendation | [MLE Agents: Autonomous ML Engineering in Large-scale Recommendation Systems](../../recommendation-components/2611.23910-mle-agents/README.md) | 2026-11-18 | l0_interface |
| recommendation | [X-split Argus: Learning Reusable History Tokens for Efficient CTR Prediction](../../recommendation-components/2611.24283-xsplit-argus/README.md) | 2026-11-18 | l1_mechanism |
| system-one | [EgoJev: Finding Evidence in Egocentric Video by Reading VLM Decisions](../../system-one/2611.24616-egojev/README.md) | 2026-11-18 | l1_mechanism |
| system-one | [Jeveration: System One Models Now Generate](../../system-one/2611.24738-jeveration/README.md) | 2026-11-18 | 高成本仅收录，不复现 |
