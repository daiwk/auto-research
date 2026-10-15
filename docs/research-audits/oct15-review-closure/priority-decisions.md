# 本轮 P0/P1 逐篇决定

本页按审查决定展示，不是实现清单。高成本明确不复现即审查完成，不是等待运行的 TODO。
每项的实际读法、原文位置、来源指纹和成本性质保留在 [完整登记](paper-register.json) 所引用的领域回执中。
日期为原始首发；首发不明会明确写出，不用目录日期补造。

## 可负担的审查候选：14 项（未实现）

- [When Does Momentum Help in Reinforcement Learning with Verifiable Rewards?](https://arxiv.org/html/2610.20413v1) · 2026-10-14 · P1

    只接收论文原始十臂 bandit 的 bias-corrected EMA/安全 η/(1−β) 机制和解析性质检验，可用 CPU 数值运算保留原目标；不接收4B/32B RLVR或50,000-replicate完整统计活动，不据此声称LLM提升；接受为低成本审查候选，本轮未实现、未实验，亦不自动进入执行/evolve。

- [SpectrumQuant: Spectrum Alignment for LLM Quantization](https://arxiv.org/html/2610.20303v1) · 2026-10-14 · P1

    SpectrumQuant 用校准激活协方差构造闭式 alignment+mixing 正交旋转；原文7B校准约0.26 GPU小时、4.51 GiB，可保留128条真实校准样本的7B原算法路径；不承诺70B或全套多模型下游扫评；接受为低成本审查候选，本轮未实现、未实验，亦不自动进入执行/evolve。

- [Which Knowledge Should LLMs Trust? Uncovering a Generalizable Steering Direction Across Knowledge Conflicts](https://arxiv.org/html/2610.20067v1) · 2026-10-14 · P1

    知识冲突偏好方向是残差空间的线性干预，原文采用7B–9B、单卡A100、仅推理。接受真实模型上独立开发冲突对提取方向与隔离测试的核心候选；不把先按clean正确筛出的条件准确率当无条件能力，也不把评测答案送入推理。

- [One Monitor Does Not Fit All: Formalism-Agnostic Runtime Verification for Agentic AI](https://arxiv.org/html/2610.19818v1) · 2026-10-14 · P1

    AgenticRV 的 canonical events、monitor-specific projection、统一 verdict 与 effect 前阻断是可执行的运行时机制。Python/受控工作流可在 Mac 保真核验；只接受该机制，不把立即返回的 monitor 微基准冒充语义监控效果或 Agent 能力。

- [Delta Tokenizer: Reference-Identical Tokenization of Session Deltas and Segment-Parallelism for Long Prompts on Multicore CPUs](https://arxiv.org/html/2610.19801v1) · 2026-10-14 · P1

    Delta Tokenizer 的核心是由 tokenizer 拆分规则证明安全的增量接缝、精确分段及 chunk 调度，而不是简单拼接 token。CPU 核心可在本地 Mac 以真实 tokenizer 和原始文本核验一致性；不复跑 41.8B 文档或多服务器服务实验，不声称已测 TTFT。

- [Measuring and Reducing Unusable Replies of LLM Agents](https://arxiv.org/html/2610.19659v1) · 2026-10-14 · P1

    回复可用性把读者实际见过的信息作为边界，单次重写或追加明确回复要求无需训练。接受少量真实回复上的reader检查与实际重写机制候选；不能用金标可用回复替代重写器，480回复/8模型统计不视为本地结果。

- [Beyond Retrieval: Evidence Access and Event Aggregation in Agent Memory](https://arxiv.org/html/2610.19474v1) · 2026-10-14 · P1

    TallyMem 保留原始轨迹、生成事件规格并实际执行聚合，不能以金标事件集代替规格生成。接受原始日志→事件ledger→真实编译/执行的廉价核心候选；\$1.05仅属原文primary arm，不能外推全AMA/多reader成本。AMA混入开发轨迹，正式能力比较应采用25开发/99隔离仓库协议。

- [When Is Smaller Greener? Right-Sizing Language Models for Agentic AI](https://arxiv.org/html/2610.19345v1) · 2026-10-14 · P1

    本文的贡献是按成功完成任务计量能耗/成本/时间的决策公式与Pareto筛选。接受CPU数值机制候选，可从公开参数算交叉长度；15模型GPU能耗pilot并非已复现，也不能将合成可靠率下的公式结果宣传为Agent能力。

- [Truthful and Expected-Payment-Optimal Model Routing in Graph-Based Agentic Workflows](https://arxiv.org/html/2610.19316v1) · 2026-10-13 · P1

    STAR 的分配目标、工作量单调性及积分支付可在小型真实合成图上用精确求解器执行，不需要调用 LLM。接受的是拍卖/路由核心机制候选，不把合成成本或激励保证当作真实 Agent 能力提升。

- [Online Tokenization with Optimal Delay in Linear Time](https://arxiv.org/html/2610.19139v1) · 2026-10-13 · P1

    在线tokenization以稳定输出前缀与delay形式化为基础，组合special-token、pretokenizer和BPE，并给出更低delay的联合算法与不可解边界；公开Morgan Stanley上游实现可做CPU级精确ID/流式等价性验收。接受为低成本算法候选，本轮不实现、不跑完整吞吐研究。

- [Plant Memory: Technical Language Processing and a Verified Maintenance Ontology for Agent-Accessible Failure Knowledge from SAP PM Work Orders](https://arxiv.org/html/2610.19131v1) · 2026-10-13 · P1

    Plant Memory 的 rule-first TLP、带证据/审核状态的事实图及 SQLite 离线后端可低成本实现，LLM第二读者是可选项。接受规则/溯源核心候选；400条合成工单的数字只是受控机制证据，不能宣称真实工厂部署、通用Agent能力或自动evolve收益。

- [BLADE: Auditing Information Use for Failure Attribution in LLM Multi-Agent Systems](https://arxiv.org/html/2610.18780v1) · 2026-10-13 · P1

    BLADE 审计来源到决策的使用关系，区分引入、传播和修复；原文明确不输入参考答案。全文片段报告1228轨迹的 Jev 推断估算约\$1.9，属于廉价真实轨迹审查候选；仍需真实决策模型，不得用金标责任步骤做 fixture。

- [Knowing the User Is Not Knowing What We Established: Grounding Awareness in Personal Agents](https://arxiv.org/html/2610.18684v1) · 2026-10-13 · P1

    Grounding Layer 明确分开用户事实与已接受、未确认、修订和限域约定；ledger、动作前gate及回查原始对话均保留。可低成本核验真实对话到状态提取及有限动作边界；不得直接喂入oracle +Status/+Policy或gold动作当实现。只接受机制候选，不声称全基准收益。

- [Fan Out or Relay? Ownership-Aware Routing for LLM Agents Querying Siloed Tables](https://arxiv.org/html/2610.18157v1) · 2026-10-13 · P1

    OAR 仅用公开schema生成一份草拟SQL并计算owner cover，在读任何私有行前决定fan-out或relay。核心可在小型真实数据库和实际SQL草拟模型上低成本检验；不能直接喂gold SQL/owner答案替代草拟，不声称13种设置已复现。

## 窗口首发的高成本终态：369 项

点击领域展开。完整论文规模不复现；没有用小 fixture、数值单测或注册标签顶替能力比较。

<details markdown="1"><summary>搜广推 / LLM 应用：5 项</summary>

- [How to Evaluate When You Don't Know How to Evaluate? Choosing Reliable Setups for Base Language Model Benchmarking](https://arxiv.org/html/2610.19185v1) · 2026-10-13 · P1

    用单调性、非随机性和排序一致性选择 LLM 评测设置；Appendix A 实报 2B 模型约11000、较大模型约7000 GH200 GPU-hours。CPU 五分钟仅是已存在结果的元指标计算，不是整套评测成本；不复现、审查 DONE。

- [Prompt or Policy? Optimizing Physician Slate Presentations with LLM User Simulators](https://arxiv.org/html/2610.18309v1) · 2026-10-13 · P1

    固定医生 slate 上比较 GEPA、GRPO 及串联，使用患者模拟器而非生产转化 A/B。§2.2 为4B/12B full fine-tune、31B judge、4000 GEPA 调用及125×256 rollouts/H200；完整预算高，不复现、审查 DONE。

- [Web Scale on a Budget: Tail-Aware Retrieval Evaluation](https://arxiv.org/html/2610.17986v1) · 2026-10-13 · P1

    每query估计 gallery 无关的检索难度，以尾部估计预测大图库指标；不能把在5M样本的估计冒称已索引100M。五backbone、多个真实大图库的原始对照仍昂贵，完整复现不做、审查 DONE；不把200GB全库描述子成本当本方法每次必需成本。

- [MMTA: Benchmarking Multimodal Temporal Analysis with Time Series, Text, and Vision](https://arxiv.org/html/2610.17856v2) · 2026-10-13 · P1

    MMTA/TimeOmni-v 将时序编码、时间对齐、视觉/文本布局和预测头结合；已核v2 Appendix C.2，使用H200 140GB、每数据集1–8卡和约40000 padded tokens/rank。完整九域三模态训练/评测成本高，不复现、审查 DONE。

- [Many Right Answers, One Training Example: Removing Responder Noise from GRPO for LLM Recommenders](https://arxiv.org/html/2610.17771v1) · 2026-10-13 · P1

    ReMaRk 按请求均匀采样并对多回复标题并集计一次奖励，减少 responder 噪声。正文实报2B/4B/9B选中checkpoint仍31.5/41.6/49.3 GPU-hours，比较臂更贵；不是因为更快就便宜，不复现、审查 DONE。

</details>

<details markdown="1"><summary>基础模型 / 多模态 / JEPA：208 项</summary>

- [Can Learning to Answer Spatial Questions Improve Novel-View Generation?](https://arxiv.org/html/2610.20610v1) · 2026-10-14 · P1

    Ask4NV是相关多模态核心方法，非题名排除；官方原文资源搜索未核定联合训练总预算，按成本门槛不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware End-to-End Autonomous Driving](https://arxiv.org/html/2610.20609v1) · 2026-10-14 · P1

    完整VLA训练与驾驶闭环要求显著数据/仿真，已读资源段未核定单卡完整预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [VITAL: From Visual Motion to Precise Action](https://arxiv.org/html/2610.20604v1) · 2026-10-14 · P1

    visual-motion到精确action原链路不可被轨迹heuristic代替，原多GPU训练不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [GeoThinker-$F$: Endogenous Predictive World Representations for Fast Spatial Intelligence](https://arxiv.org/html/2610.20592v1) · 2026-10-14 · P1

    相对减少69.99%辅助FLOPs仍是大模型多模态训练/评估；完整预算未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Your Transformer Is Secretly Elastic](https://arxiv.org/html/2610.20588v1) · 2026-10-14 · P1

    联合 neuron/head soft-pruning 排名值得保留，但分钟级构造不是 27 模型、多数据集、六稀疏率和基线整轮成本；完整公平比较预计小时级，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Continuum Attention](https://arxiv.org/html/2610.20586v1) · 2026-10-14 · P1

    Continuum Attention 在连续分段线性K/V曲线上用闭式指数矩精确积分，含半token边界与解析梯度；研究共80训练运行、每模型3.84M tokens、5种子。完整多臂Metal复现总时长不能廉价核定，按保守成本门槛不复现、审查 DONE；不拿便宜算子单测顶替研究结论。

- [KinoGen: Customizable Humanoid Loco-Manipulation References via Kinematically Grounded Video Generation](https://arxiv.org/html/2610.20552v1) · 2026-10-14 · P1

    KinoGen视频生成、几何拟合和跟踪政策均属定义链路；官方原文未能廉价核定总预算且需实体资源，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Generative Representation Learning for Scalable Latent Tokenization](https://arxiv.org/html/2610.20533v1) · 2026-10-14 · P1

    生成式表示 tokenization 的完整训练与生成评测明显超出单卡预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ActiveEvidence: Decision-Focused Evidence Graphs with Verifiable Acquisition Gaps](https://arxiv.org/html/2610.20532v1) · 2026-10-14 · P1

    CEIG 的决定证书仅相对固定学习分数有效，语义质量另测；原文完整训练16.4 GPU-h，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [EarlyCommit: Calibrated Word-by-Word Commitment for Robots Acting Before You Finish Speaking](https://arxiv.org/html/2610.20531v1) · 2026-10-14 · P1

    EarlyCommit真值生成、RLCD与temperature fitting已核；完整多臂多seed总时长未披露，上游匿名补充未验收，不能由31–35ms推理当廉价，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Physical Time as a Missing Dimension of Robot Policy Memory Dynamics](https://arxiv.org/html/2610.20524v1) · 2026-10-14 · P1

    TFP以实测物理时间推进memory；完整训练明显高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Graph-Reweighted Behavior Cloning with Human Interventions for Precise Robotic Manipulation](https://arxiv.org/html/2610.20504v1) · 2026-10-14 · P1

    Graph-reweighted BC多基础政策训练成本高，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Decoupled Marginal Sharpening for Training-Free Inference-Time Scaling](https://arxiv.org/html/2610.20483v1) · 2026-10-14 · P1

    Decoupled Marginal Sharpening 不更新权重，但多任务/多seed长推理的完整总成本无法廉价核定，不以training-free等同廉价。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [AdaRSI: On-Demand Recursive Self-Improvement for Embodied Agents](https://arxiv.org/html/2610.20474v1) · 2026-10-14 · P1

    AdaRSI需真实子步适配及执行闭环，原文相对28%GPU节省不是绝对低成本；完整campaign未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Equal CER, Unequal Damage: Severity-Weighted Character Error Rate for OCR](https://arxiv.org/html/2610.20461v1) · 2026-10-14 · P1

    severity-weighted CER是相关OCR/VLM评测方法，不作行业题名排除。原文显式标注/评分器训练与多VLM成本高，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [The COUNT: Counting N-grams Unlocks Scaling on Host Memory and Training-Free Adaptation](https://arxiv.org/html/2610.20456v1) · 2026-10-14 · P1

    COUNT 把 CPU n-gram 计数映射到 unembedding 输入特征；主表约797GB内存，小模型表仍约17.1GB，另有训练成本。成本过高，不下载计数表、不复现，审查 DONE。

- [When Do Discrete Actions Make Good Continuous Controllers?](https://arxiv.org/html/2610.20429v1) · 2026-10-14 · P1

    离散action能否替代连续controller需匹配表征/训练对照，完整多臂预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [OrionMoE-v1.0: A Mixture-of-Experts Foundation Model for Tabular In-Context Learning](https://arxiv.org/html/2610.20418v1) · 2026-10-14 · P1

    双轴表格 Transformer 与 dataset-conditioned sparse routing 是相关核心方法；§4明确仅放推理代码/权重、不含训练代码与合成生成器，忠实预训练总成本不能廉价核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Cortex: Consolidating Context into Parametric Memory](https://arxiv.org/pdf/2610.20399v1) · 2026-10-14 · P1

    Cortex 用情景查询与上下文条件蒸馏将外部上下文写入参数记忆；4B–120B、多批次/顺序编辑。完整训练/编辑成本高，不复现、审查 DONE；HTML不可用后已取得官方PDF并核指定方法/资源段落，不把有界核对冒称整篇通读。

- [STP-GUI: Spatially-Aware Token Pruning for Efficient Web-GUI Agents](https://arxiv.org/html/2610.20390v1) · 2026-10-14 · P1

    STP-GUI不能只实现2M selector而跳过定义backbone和训练，原配置高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Beyond Expert Rankings: Contrast Calibration for Mixed-Precision MoE Quantization](https://arxiv.org/html/2610.20353v1) · 2026-10-14 · P1

    对比校准在 expert sensitivity 与内存分配间建模；不能仅凭降低推理存储推断完整量化研究廉价，成本未核定终态不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ReferFlow: Beyond Final-Target Localization for Complex Referring Expressions](https://arxiv.org/html/2610.20352v1) · 2026-10-14 · P1

    ReferFlow多阶段grounding与GRPO完整训练高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Lifted State Policy Optimization: Internalizing Self-Correction through Transition Geometry](https://arxiv.org/html/2610.20350v1) · 2026-10-14 · P1

    LSPO 用 lifted state 能量与有限转移信用再内化答案；训练约372.9h/运行，完整复现成本过高。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Read, Parse, Describe: Unified Document Parsing with Visual Element Description Generation](https://arxiv.org/html/2610.20335v1) · 2026-10-14 · P1

    统一文档parse与visual-description的模型改动相关；已读原文方法/资源片段未核定完整VLM训练/多parser对照成本，终态不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Are We Overthinking One-Step Generation?](https://arxiv.org/html/2610.20331v1) · 2026-10-14 · P1

    Priming Models 的重建初始化与分布后训练均为定义链路；相对少算十倍仍不是单卡低成本，完整训练不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Beyond Static Cues: Unified Dynamic Detection of MLLM Backdoors via Dual-Flow Trajectory Analysis](https://arxiv.org/html/2610.20319v1) · 2026-10-14 · P1

    Dual-flow backdoor detection需要实际被毒化模型/受控训练，完整资源预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Anuvani-LID: Robust and Calibrated Spoken Language Identification for Indian Languages](https://arxiv.org/html/2610.20263v1) · 2026-10-14 · P1

    Anuvani-LID的完整分阶段speech训练成本过高，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Harness Policy Distillation: Aligning Agent Policies with Runtime Semantics](https://arxiv.org/html/2610.20261v1) · 2026-10-14 · P1

    HPD 显式训练 runtime 语义，跨模型/跨harness重建回放与控制文档；完整多臂总成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Scaling Multilingual Mixture-of-Experts: How Language Coverage Changes Capacity and Compute Allocation](https://arxiv.org/html/2610.20247v1) · 2026-10-14 · P1

    多语言 MoE joint scaling law 的拟合依赖大规模从头预训练，完整实验成本过高，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ObjDream: Guiding Vision-Language-Action Models with Object-Level Understanding and Future State Prediction](https://arxiv.org/html/2610.20223v1) · 2026-10-14 · P1

    ObjDream定义的对象编码、VLM及action训练均保留，原多GPU配置不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Scaling Multilingual Safety and Reasoning Evaluation through Reasoning-Guided Translation](https://arxiv.org/html/2610.20221v1) · 2026-10-14 · P1

    低样本单语费用/延迟不代表完整多语评测合成预算，物质API成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Atomic-WAM: Execution-Grounded Atomic-Motion Reasoning for World Action Models](https://arxiv.org/html/2610.20157v1) · 2026-10-14 · P1

    原作者已缩小global batch仍昂贵，不进一步用廉价fixture替换WAM链路，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [XViewRank: Overlap-Conditioned Score Fusion for LLM-Augmented Sparse Retrieval](https://arxiv.org/html/2610.20122v1) · 2026-10-14 · P1

    XViewRank 明确开发集选择而不读测试qrels；完整索引、生成视图和多基线总资源未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [AFCS: Atomic-Fact-Conditioned Synthesis for Factual Knowledge Pretraining](https://arxiv.org/html/2610.20086v1) · 2026-10-14 · P1

    事实条件语料合成与预训练均为定义链路，整轮高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [VisualWorldBench: A Fine-Grained Multi-Task Benchmark for Evaluating Visual World Knowledge in MLLMs](https://arxiv.org/html/2610.20083v1) · 2026-10-14 · P1

    benchmark附加VLM训练/知识对照高成本，保留资源与协议不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Rethinking Prediction Horizons: Decoupling Model Queries from State Updates in Few-Step MeanFlow](https://arxiv.org/html/2610.20071v1) · 2026-10-14 · P1

    MeanFlow 将查询horizon与状态更新解耦；改动虽无额外query，但原文多臂校准和生成评测巨大，成本过高。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [FoveaVLA: Foveation Actions Replace the Wrist Camera in VLAs](https://arxiv.org/html/2610.20064v1) · 2026-10-14 · P1

    FoveaVLA foveation-action学习完整训练高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [GeoCloak: An Agentic Framework for Semantics-Preserving Geolocation Privacy via Peripheral Clue Manipulation](https://arxiv.org/html/2610.20055v1) · 2026-10-14 · P1

    GeoCloak 的保护流程需要真实模型与编辑闭环，原文资源片段未核定完整调用成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Weighted Adjoint Matching: Finetuning Flow Matching Models with Time-Dependent Control Cost](https://arxiv.org/html/2610.20035v1) · 2026-10-14 · P1

    Weighted Adjoint Matching 的时间变控制成本必须保留；不能只看小MLP参数便宣称整研究便宜，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [LintEval: Benchmarking LLMs on Linter-Guided File Refactoring](https://arxiv.org/html/2610.20027v1) · 2026-10-14 · P1

    本轮不整套执行生成/回归/再训练，原文完整多臂预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [MorphAct: Robot Policies Morphing with the Worlds They Act In](https://arxiv.org/html/2610.20019v1) · 2026-10-14 · P1

    MorphAct需实际生成权重/残差和闭环环境，公式中的单步成本不是整轮预算，未核定则不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Gray-Box Hallucination Detection in LLMs with Token Identities](https://arxiv.org/html/2610.19996v1) · 2026-10-14 · P1

    gray-box检测需要真实模型轨迹与跨任务训练，原多GPU实证不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [LatentLoop: Scaling Looped MoE Models with Asymmetric Compute Allocation](https://arxiv.org/html/2610.19975v1) · 2026-10-14 · P1

    非对称 loop MoE 的 FLOPs匹配不代表实际设备需求相同；完整训练多GPU，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Safe-FCL: Continual Risk Awareness and Fine-Grained Safety Aggregation for Federated Continual Learning of LLMs](https://arxiv.org/html/2610.19968v1) · 2026-10-14 · P1

    Safe-FCL 的风险感知与细粒度聚合不是单次adapter算子；完整联邦训练成本不确定，终态不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Choosing the Number of Attention Heads from Intrinsic Dimension: A Small-Scale Study](https://arxiv.org/html/2610.19966v1) · 2026-10-14 · P1

    内在维度选heads虽称small-scale，完整比较已经小时级且未含VAE搜索，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Complementary Future Token Pruning for World Action Models](https://arxiv.org/html/2610.19957v1) · 2026-10-14 · P1

    互补未来token剪枝不能省略原WAM前向；完整模型/评测预算在已读资源段未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [SAM3RL: Memory Control via Reinforcement Learning for Visual Object Tracking](https://arxiv.org/html/2610.19931v1) · 2026-10-14 · P1

    SAM3RL 保留真实 memory eviction policy，不能用规则代替；原配置多GPU长训练，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [When Non-Adversarial Noise Hurts Learning: Benchmarking Skill Self-Evolution in Agents](https://arxiv.org/html/2610.19910v1) · 2026-10-14 · P1

    需要真实环境执行和技能学习的长闭环；已读资源/指标段未核定完整多臂成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Frustratingly Easy Majority Voting Using Length Conditioning](https://arxiv.org/pdf/2610.19890v1) · 2026-10-14 · P1

    长度条件多数投票本身便宜，但公共任务/多模型/重复采样整轮成本未核定，不用已缓存答案公式当能力验证，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon](https://arxiv.org/html/2610.19844v1) · 2026-10-14 · P1

    SMRC/PMRC 保留子空间外残差并修正换基边界；原文60M/150M用2GPU、350M用4GPU、1.3B用8GPU预训练。完整多规模实证成本高，不复现、审查 DONE；不把单次数值测试冒称论文能力验证。

- [What Matters for World Modeling in Vision-Language-Action Models?](https://arxiv.org/html/2610.19825v1) · 2026-10-14 · P1

    必须匹配训练资源和DINOv3特征预计算，完整多臂高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [JointServe: Serving Multi-Model Agents on Memory-Constrained GPUs](https://arxiv.org/html/2610.19822v1) · 2026-10-14 · P1

    JointServe 的实际runtime传输/驻留调度必须执行；原文局部1.83s交换不是整轮成本，完整平台移植与评测预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Calibration and Risk-Budgeted Decisions with System One Models](https://arxiv.org/html/2610.19811v1) · 2026-10-14 · P1

    LTT风险选择的统计协议可借鉴，但完整模型适配与多数据集比较成本未核定，本轮不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Efficient contextual partial monitoring with general function approximation](https://arxiv.org/html/2610.19804v1) · 2026-10-14 · P1

    一般 contextual partial monitoring 理论在LLM routing有公开实证；完整公平实验与数据准备总成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Asymptotically Exact Negative Guidance of Diffusion Models via Positive-Unlabeled Learning](https://arxiv.org/html/2610.19802v1) · 2026-10-14 · P1

    PU在线训练加SMC校正的负引导核心不省略；全粒子、多条件和生成质量评测总成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Learning to Compute Is Not Learning to Retain or Reuse in Looped Transformers](https://arxiv.org/html/2610.19768v1) · 2026-10-14 · P1

    Looped Transformer 的保留/重用诊断包含大量匹配训练；MAC proxy不是实测总FLOPs，完整campaign成本过高。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Refine Actions If Needed: Adaptive Action Chunk Refinement for Robot Manipulation](https://arxiv.org/html/2610.19765v1) · 2026-10-14 · P1

    RAIN 动态路由训练与实体执行成本不能由低latency推断；官方原文总预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [CAST: History-Adaptive Spectral Clipping for LLM Pretraining](https://arxiv.org/html/2610.19761v1) · 2026-10-14 · P1

    谱clip的自适应历史尺度与阈值必须在真实预训练链路核验；多设备原配置高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Coordi-pi: Coordination-Aware Dual-Hand Action Representation for Bimanual Dexterous Manipulation](https://arxiv.org/html/2610.19753v1) · 2026-10-14 · P1

    双手action表征与控制完整训练多GPU，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [One-shot Human Video-Guided Adaptation for Vision-Language-Action Models](https://arxiv.org/html/2610.19746v1) · 2026-10-14 · P1

    CapPro one-shot指一段人类视频不是整轮零训练；已读资源段未核定模型/训练/实体总成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Discriminative Score Function: Turning Pretrained Models into Functional Generative Priors](https://arxiv.org/html/2610.19743v1) · 2026-10-14 · P1

    DSF 的training-free生成接口并非廉价一阶图像优化；完整高阶采样评测预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Does the Linguistic Register of Thinking Matter? Wenyan as a Compact Reasoning Register for Chinese LLMs](https://arxiv.org/html/2610.19741v1) · 2026-10-14 · P1

    Wenyan register压缩需真实全参训练与质量/长度比较；未公开固定GPU拓扑，完整预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ProtModernBERT: Compute-Efficient Protein Language Modeling](https://arxiv.org/html/2610.19738v1) · 2026-10-14 · P1

    ProtModernBERT 的效率改进仍需真实蛋白语料预训练和匹配对照，成本过高；原文对照成本为估计，不是本地实测。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Mitigating Video Hallucinations via Attention-Guided Representation Perturbation](https://arxiv.org/html/2610.19728v1) · 2026-10-14 · P1

    ARP-CD 的表征扰动真实前向必须保留；局部时序不足以核定完整视频质量实验总成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [TIMERSI: Towards Self-Improved Agentic Deployment for Time-Series Foundation Models](https://arxiv.org/html/2610.19725v1) · 2026-10-14 · P1

    TIMERSI 的自改进部署需要模型/数据实际回放，完整搜索与多窗口总成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Recognizing Dialogue Ambiguity via Candidate Set Visual Grounding](https://arxiv.org/html/2610.19723v1) · 2026-10-14 · P1

    候选集visual grounding 的完整ambiguity评测已经小时级，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Learning Individual Scientific Taste with Privileged Hindsight Distillation](https://arxiv.org/html/2610.19719v1) · 2026-10-14 · P1

    科学taste的特权后见蒸馏需要真实反馈/反复LLM调用，完整总成本和公共回放可用性未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ReGRA: Residual-Gradient Adaptation for Complementary Low-Rank Fine-Tuning](https://arxiv.org/html/2610.19700v1) · 2026-10-14 · P1

    ReGRA 双阶段残差梯度投影/正交化保留；多模型多任务训练与校准全预算未核定，按门槛不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Share the Symbol, Not the Vector: Training-Free Fact Communication Across Language Models](https://arxiv.org/html/2610.19696v1) · 2026-10-14 · P1

    symbol fact communication不能只做token字典lookup；原文训练free称谓不抹去J-lens构建与多模型评测成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Annealed Lévy Diffusion via Gaussian Surrogate Reverse Dynamics](https://arxiv.org/html/2610.19692v1) · 2026-10-14 · P1

    ALD以随时间变化的稳定指数、Gaussian scale-mixture及两种reverse sampler连接重尾探索和Gaussian细化。替代HTTP传输取得原文后核明完整图像训练/采样为多GPU多天，成本过高不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Beyond Distribution Matching: Selective Margin Preservation for Supervised Fine-Tuning](https://arxiv.org/html/2610.19685v1) · 2026-10-14 · P1

    SRP-SFT 的topK非目标margin hinge已核；完整多seed、排名控制与跨backbone训练明显多GPU高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Enhancing Latent World Models with Associative Memory](https://arxiv.org/html/2610.19683v1) · 2026-10-14 · P1

    关联记忆的latent dynamics仍需端到端训练与闭环规划，完整多臂总成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ACRO: Actor-Critic Rollout Orchestration](https://arxiv.org/html/2610.19677v1) · 2026-10-14 · P1

    ACRO 的actor/critic rollout编排需要真实环境，完整训练/闭环预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Accelerating VLA Inference with Perturbation Informed Execution](https://arxiv.org/html/2610.19656v1) · 2026-10-14 · P1

    扰动知情VLA执行需真实全参政策与扰动任务，原多GPU配置不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [HACHIMI-II: From Role-Play to Learner Behavior Modeling for Faithful Student Simulation](https://arxiv.org/html/2610.19654v1) · 2026-10-14 · P1

    学习者模拟虽在教育场景，但状态编译harness属于相关Agent方法，不按题名排除。已核完整摘要及原文可用资源段，真实用户历史回放/多模型调用的完整成本未能廉价核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [SPECTRA-VLA: Base-Fine Hyperspectral Token Transfer at Frozen Vision-Language-Action Interfaces](https://arxiv.org/html/2610.19651v1) · 2026-10-14 · P1

    SPECTRA-VLA 模态接口训练/传感器闭环不可用简单token替代，成本未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Sparse Autoencoders Are a Shared Coordinate System for Symbolic Matching](https://arxiv.org/html/2610.19636v1) · 2026-10-14 · P1

    SAE共享坐标系的语义匹配可借鉴，但完整多模型编码/数据比较成本高，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Self-Conditioning Enables Deep Sequential Reasoning in Flow Matching](https://arxiv.org/html/2610.19628v1) · 2026-10-14 · P1

    自条件flow的深序列推理需要真实两pass训练，不能缩成固定heuristic，原配置多GPU不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [DAGFormer: Global Topology Prediction for Transformer Cross-Layer Connections](https://arxiv.org/html/2610.19625v1) · 2026-10-14 · P1

    全局跨层拓扑预测的完整预训练与控制高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [F2A-ObjectNav: An Adaptive Agentic Architecture for Object-Goal Navigation](https://arxiv.org/html/2610.19618v1) · 2026-10-14 · P1

    advisor低于1%step率不等于低API/整体时间占比；完整导航实验总成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference](https://arxiv.org/html/2610.19605v1) · 2026-10-14 · P1

    PN-Mix 用 prefill Q/K RoPE 通道对范数分配混合精度、配合1-bit残差与sink保护；原文多模型8B–32B、长输出多任务评测的整体成本未能廉价核定，按预算门槛不复现、审查 DONE。Kitty 链接是基线，不冒称作者代码。

- [Cracking Mobile Manipulation: From Failure Diagnosis to Agentic Robot System](https://arxiv.org/html/2610.19600v1) · 2026-10-14 · P1

    移动操作Agent需要真实harness和任务环境；完整多域评测预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Who's Behind the Text? Robust Model Authorship Attribution](https://arxiv.org/html/2610.19583v1) · 2026-10-14 · P1

    模型作者归属的分支LoRA训练与跨域评估总成本未核定，按预算门槛不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Back on Track: Deployment-time Policy Improvement via World Model Planning](https://arxiv.org/html/2610.19579v1) · 2026-10-14 · P1

    部署期world-model规划的rollout、训练和闭环比较总成本未核定，不能以单GPU作为廉价证明，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [TextVerifier: Seeing Beyond Recognition to Verify Chinese Text Rendering](https://arxiv.org/html/2610.19551v1) · 2026-10-14 · P1

    局部每字符毫秒不是完整训练/质量比较成本；多GPU实证不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [GraphRAG-LTM: A Layered Threat Modeling Framework for Attacks on Graph Retrieval-Augmented Generation](https://arxiv.org/html/2610.19549v1) · 2026-10-14 · P1

    威胁建模需真实检索/图证据与权限控制，已读原文段未核定完整预算，本轮不实现攻击、不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [VLRLA: Deployment-Time Adaptation of Vision-Language-Action Models through In-Context Reinforcement Learning](https://arxiv.org/html/2610.19517v1) · 2026-10-14 · P1

    VLRLA的上下文RL训练与部署时适配链路昂贵，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [One Block Ahead: Promoting Sampler State in Diffusion Language Models](https://arxiv.org/html/2610.19510v1) · 2026-10-14 · P1

    One Block Ahead 需真实uniform-state sampler，不用固定block规则代替；单H100原backbone吞吐声明不是新方法整轮成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Structure-Preserving Document-Level Data Augmentation via Discourse Parsing](https://arxiv.org/html/2610.19497v1) · 2026-10-14 · P1

    数据增强后的训练与label-transfer核验不可省，完整campaign预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Robota-Embed: Unified VLA Embeddings for Robot In-Context Learning and Evolution](https://arxiv.org/html/2610.19495v1) · 2026-10-14 · P1

    Robota-Embed query微时序排除了SAM3/rerank/policy/robot；完整训练与pipeline成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Towards Efficient Simultaneous Inverse Text Normalization with Pretrained Text-to-Text Language Model and Read-Tag-Write Policy](https://arxiv.org/html/2610.19492v1) · 2026-10-14 · P1

    Read-Tag-Write训练和streaming对照多GPU高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [AdCoEvo: A Co-Evolving Multi-Agent Advertising Delivery System](https://arxiv.org/html/2610.19454v1) · 2026-10-14 · P1

    AdCoEvo 是三角色广告策略共进化；§5.1 的 AuctionNet 是模拟器，14.02% ADV 不是生产线上 A/B。可归 Agent/RSI，不作工业 P0。8B 三角色、5 条×50-period 序列及交替更新的完整实验成本高，不复现、审查 DONE。

- [More Than Seeing: Vision as Scalable Anchors in Native Multimodal Pre-Training](https://arxiv.org/html/2610.19443v1) · 2026-10-14 · P1

    视觉anchor效应需要真实匹配预训练而非特征fixture；已读资源段未核定完整token/总时长，成本终态不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Progress-Aware Distillation for Mitigating Stagnation in Small Language Model Agents](https://arxiv.org/html/2610.19439v1) · 2026-10-14 · P1

    ProD虽一次预处理rollout，完整teacher/student、多任务和对照成本仍未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Paraphrase Consensus Is Not Self-Consistency: Instruction Reliance and Robustness in VLA Policies](https://arxiv.org/html/2610.19438v1) · 2026-10-14 · P1

    paraphrase consensus不能充当independent policy self-consistency；完整posttraining/robot评测预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [WinARDet: Compressed Window Auto-Regression for Long-Horizon Vision-Language Grounding](https://arxiv.org/html/2610.19419v1) · 2026-10-14 · P1

    WinARDet历史压缩/自回归完整训练与检测评估预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Scaling LLM Inference via Parallelism: Throughput-Latency Trade-off](https://arxiv.org/html/2610.19405v1) · 2026-10-14 · P1

    核心问题就是多GPU并行吞吐/延迟前沿，单卡无法忠实检验完整声明，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [RCER: Reconstructing Cross-Evidence Relations for Iterative Retrieval-Augmented Generation](https://arxiv.org/html/2610.19398v1) · 2026-10-14 · P1

    RCER 需保留独立关系获取、context重建和组合推理；原文可读但廉价资源搜索未核定完整模型/调用预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [RA$^2$: Retain-Anchored Attraction Preserves Forget-Adjacent Utility in LLM Unlearning](https://arxiv.org/html/2610.19385v1) · 2026-10-14 · P1

    retain-anchor attraction的新局部保持目标相关；单臂约5分钟不能覆盖全套多数据/方法/seed比较，完整campaign成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models](https://arxiv.org/html/2610.19375v1) · 2026-10-14 · P1

    JEPA prediction-vs-planning 研究采用冻结物理状态decoder、配对规划种子、分离编码/预测误差及匹配继续训练对照；可参考其评测协议，但三环境、模型梯度阶梯与重复训练的完整总成本未能廉价核定。不重训、不复现，审查 DONE；不将协议建议当已接入evolve。

- [MMKG-R1: Constructing Multimodal Knowledge Graphs via Reinforcement Learning](https://arxiv.org/html/2610.19341v1) · 2026-10-14 · P1

    多模态KG构造的真实策略训练不可用抽取fixture代替，原多GPU路径不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [LLM-jp-4 Technical Report](https://arxiv.org/html/2610.19331v1) · 2026-10-14 · P1

    完整基座预训练及recipe搜索显然不在单A100/A30本轮预算内，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Qwenfant: Train Big Character-level BabyLMs on Concise Parallel Text](https://arxiv.org/html/2610.19294v1) · 2026-10-13 · P1

    字符化与平行简洁语料方法相关，但完整训练/尺度扫资源在已读段未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [MIND: Instruction-Conditioned Incremental Grounding for Robots](https://arxiv.org/html/2610.19262v1) · 2026-10-13 · P1

    依赖编译、event-footprint交集、semantic refresh与selection分离均属核心。0.58s evaluator与0.56s编译只覆盖59序列局部时序，排除观测、检测、规划、运动；完整多模型/感知/闭环总成本不能廉价核定，按门槛不复现，不以exact-predicate oracle单测替代真实模型。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [PACER: Process-Aware VLA Policy Learning from Human Corrections for Robotic Disassembly](https://arxiv.org/html/2610.19248v1) · 2026-10-13 · P1

    process-aware VLA人类修正需要真实训练/机器人，原多GPU多臂成本高不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Copy-Paste Language Models](https://arxiv.org/html/2610.19247v1) · 2026-10-13 · P1

    CPhead参数增加很小不代表预训练便宜；不能把未训练9B/30B速度当能力验证，完整复现成本未核定。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [LLMs program using Reusable and Composable Abstract Representations](https://arxiv.org/html/2610.19238v1) · 2026-10-13 · P1

    可重用组合抽象表示的因果比较依赖真实模型训练/干预，不复现高成本配置。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Spectral-MoE: Heterogeneous Per-Layer Expert Utilization in Dense-to-MoE Conversion](https://arxiv.org/html/2610.19232v1) · 2026-10-13 · P1

    Spectral-MoE每层异构专家预算需要真实转化/恢复训练，原多GPU配置高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [DUALVIEW: Leveraging Broad and Output-Specific Evidence for LLM-based Multi-Output Text Regression](https://arxiv.org/html/2610.19206v1) · 2026-10-13 · P1

    DUALVIEW 的广/输出特异证据完整监督训练依赖大预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Weighted Ensemble Sampling for Rare-Event Estimation in Language Models](https://arxiv.org/html/2610.19202v1) · 2026-10-13 · P1

    稀有事件估计需足够采样并报告seed级成本，已读资源段仅定义度量而未核定整套预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Into the LidarVerse: A Real-Time Unified LiDAR World Model Across Tasks and Sensors](https://arxiv.org/html/2610.19201v1) · 2026-10-13 · P1

    LidarVerse完整teacher/student与多sensor数据链路总成本未核定，不以real-time serving等同廉价训练，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Embedding Geometry Shapes LLM Routing: Tracing Failure Modes and Improving Generalization](https://arxiv.org/html/2610.19198v1) · 2026-10-13 · P1

    embedding geometry干预与router泛化需要完整数据/训练，分配资源不是最小需求，完整campaign成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [HERO: Harnessing Evidence for Test-time Refinement and Prompt Optimization in Program Generation](https://arxiv.org/html/2610.19184v1) · 2026-10-13 · P1

    HERO需完整程序执行与prompt优化，参考解只在benchmark侧；完整Agent/API/执行预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Into the Unknown: Benchmarking AI agents on open scientific research problems](https://arxiv.org/html/2610.19159v1) · 2026-10-13 · P1

    开放科学研究benchmark仅保留完整性审计教训；整套长研究执行显然高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [FACT: A Multimodal Force-Action-Track Foundation Model for Human-to-Robot Dexterity](https://arxiv.org/html/2610.19155v1) · 2026-10-13 · P1

    FACT人类到robot dexterity的完整预训练明显多设备高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [TRACER: Trace-Regularized Training Against Indirect Prompt Injection](https://arxiv.org/html/2610.19133v1) · 2026-10-13 · P1

    TRACER 需保留channel条件化与trace训练，完整训练/attack矩阵成本未核定，终态不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Unlocking Structured Pruning for Reasoning Language Models via Attention-Preserving MLP Trimming](https://arxiv.org/html/2610.19121v1) · 2026-10-13 · P1

    保留attention与decoder深度、只裁MLP的原机制；短128-step时序不是全质量评测预算，完整成本未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Genesis Steering: Better Activation Steering Through Training Data](https://arxiv.org/html/2610.19114v1) · 2026-10-13 · P1

    不能只实现向量相加代替训练数据参照的构造与公共公平评估；原文资源段未核定总预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [From Copying to Composition: How Language Models Develop In-Context Learning](https://arxiv.org/html/2610.19113v1) · 2026-10-13 · P1

    ICL复制/组合的受控学习研究成本过高；保留诊断，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Beyond Aggregate Accuracy: Item-Level Transitions in Prompt Optimization](https://arxiv.org/abs/2610.19084v1) · 2026-10-13 · P1

    RFDPO的新item级反馈真实进入后续优化；不能只用离线churn公式冒称实现，完整API调用预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [How Inner Optimizers Shape Replica Scaling](https://arxiv.org/html/2610.19064v1) · 2026-10-13 · P1

    分布式优化的replica scaling原定义需要多replica训练，完整总成本未核定且不假设多GPU，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Tracing Morphology, Semantics, and Divergence in Language Acquisition](https://arxiv.org/html/2610.19041v1) · 2026-10-13 · P1

    语言习得轨迹与checkpoint扫描成本已小时级，完整训练/评测不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [How Many Ranks Does a Token Need? A Noise-Floor Squelch for Rank-One LoRA Experts](https://arxiv.org/html/2610.19033v1) · 2026-10-13 · P1

    rank-one专家噪声门控和SURE阈值需真实LoRA训练，整轮高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Joint Subspace Sparse Attention for Efficient Long-Context Decoding](https://arxiv.org/html/2610.19026v1) · 2026-10-13 · P1

    JSSA 投影子空间与cache score-scan内核需真实权重和CUDA测评，局部ms不决定完整总成本，预算未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [How Far Can Coding Agents Go in Visual Generation?](https://arxiv.org/html/2610.19025v1) · 2026-10-13 · P1

    原文保留token/调用/费用ledger，但已读范围未核定完整成本；不把绘制primitive示例等同能力评测，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Data Density Scaling Laws for Image Self-Distillation](https://arxiv.org/html/2610.19013v1) · 2026-10-13 · P1

    Image self-distillation scaling law需匹配预训练多臂，原多GPU配置不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Discovering Undisclosed Concepts in LoRA Adapters for Diffusion-Based AIGC Models](https://arxiv.org/html/2610.18990v1) · 2026-10-13 · P1

    SGES概念发现需要真实LoRA/扩散backbone，不以低秩本身代表低费用；完整总成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts](https://arxiv.org/html/2610.18873v1) · 2026-10-13 · P1

    LoopWAM完整rollout/训练/评价总成本未核定，不用历史轨迹fixture代替闭环，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [EmbodiedEvo: Self-Evolving Coding Agent For Physical Intelligence](https://arxiv.org/html/2610.18867v2) · 2026-10-13 · P1

    无需参数更新不等于无执行/API成本；53%相对节省不能证明整套search廉价，完整总成本未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [DoubtLess: Training-Free Contrastive Decoding for Efficient Reasoning](https://arxiv.org/html/2610.18862v1) · 2026-10-13 · P1

    DoubtLess training-free仍有多模型多流长推理，完整资源预算未核定且依赖TP，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Visual Tokens on Demand: Visual Budgeting for Scalable and Efficient Multi-Image Reasoning in Multimodal LLMs](https://arxiv.org/html/2610.18858v1) · 2026-10-13 · P1

    小budgeter参数与2ms overhead不是全VLM训练/质量评测成本，完整预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Interaction Latents as Actions for Contact-Rich Manipulation](https://arxiv.org/html/2610.18855v2) · 2026-10-13 · P1

    潜交互action学习和真实/仿真闭环需要完整多臂训练，已读预算段未核定总时长，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ForceWAM: Decoupling Future and Response Learning from Demo and Play Data for Contact-Rich Manipulation](https://arxiv.org/html/2610.18852v1) · 2026-10-13 · P1

    ForceWAM未来/响应解耦的两个训练阶段必须保留，完整多任务成本高或未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [The Last Remote Sensing Model Built by Humans? Casting Any Earth Observation Task as Recursive Self-Improvement](https://arxiv.org/html/2610.18845v1) · 2026-10-13 · P1

    不是因遥感题名排除，而是完整Agent自改进run已经小时级，成本终态不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Read the Room Before Your Model Generates](https://arxiv.org/html/2610.18820v2) · 2026-10-13 · P1

    32维/小模块并不代表整轮便宜，原实报125GPUh不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Back-Translation Still Matters: Leveraging Monolingual Data for Low-Resource Machine Translation with LLMs](https://arxiv.org/pdf/2610.18818v2) · 2026-10-13 · P1

    保留反译语料与匹配LLM训练协议；已读PDF资源片段未核定整轮时长/存储，按成本门槛不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Depth Memory](https://arxiv.org/html/2610.18809v1) · 2026-10-13 · P1

    LDM的recursive-least-squares memory与inverse covariance为核心，完整预训练多GPU大token预算不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [$λ_0$: Scaling Open-World Egocentric Human Data for Humanoid Loco-Manipulation](https://arxiv.org/abs/2610.18950v1) · 2026-10-13 · P1

    跨体对齐、离线motion/refinement和midtraining需大数据/实体资源；摘要规模已明确超出本轮忠实公共复现范围，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [GreenWAM: A World Foundation Model for Robotics](https://arxiv.org/pdf/2610.18774v1) · 2026-10-13 · P1

    官方PDF显示完整跨体数据/训练链路；已读资源段未核定其总预算，不用状态codec实现替代foundation训练，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Segment Where You Look: Attention as the Interface Between Language Models and Segmenters](https://arxiv.org/html/2610.18729v1) · 2026-10-13 · P1

    attention接口的实际多模态训练与segmenter前向必须保留，原多GPU完整配置不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [UniW(A)M: A Unified Mixture-of-Experts Framework for World and World-Action Models](https://arxiv.org/html/2610.18697v1) · 2026-10-13 · P1

    MoE世界/行动统一框架的训练与全链路预算未核定，不能用轻router成本代替全部expert，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [GeoReader: Learning Latent Geometry for Spatial Reasoning in Vision-Language Models](https://arxiv.org/html/2610.18694v1) · 2026-10-13 · P1

    GeoReader真实几何迁移与VLM训练成本高，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Just Respect the Semantics: Image-Token Compression via Pre-LLM Semantic Variable-Resolution Tokenization and In-LLM Relevance Pruning](https://arxiv.org/html/2610.18690v1) · 2026-10-13 · P1

    图像semantic variable-resolution与inLLM pruning需真实双阶段前向；training-free不消除整套多模型评价成本，预算未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Does Pretraining Teach Chemical Language Models Chemistry?](https://arxiv.org/html/2610.18651v2) · 2026-10-13 · P1

    化学语言预训练的因果对照需保留；完整多臂数据/训练预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Tiny Recursive Message Passing](https://arxiv.org/html/2610.18649v1) · 2026-10-13 · P1

    摘要十分钟只覆盖最小lattice臂；完整ACT/graph/truncation/SAT/N-queens与多seed比较昂贵，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [To Align or Not To Align: Check Your COMPASS Before You Train](https://arxiv.org/html/2610.18638v1) · 2026-10-13 · P1

    kNN compatibility diagnostic便宜不等于产生监督真值与验证便宜；完整公平比较成本过高不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [VideoJev: System One Model for Video Understanding and Interaction](https://arxiv.org/html/2610.18615v1) · 2026-10-13 · P1

    SystemOne视频评分不能用缓存候选替代真实encoder；joint-forward局部延迟不决定训练/全多臂总成本，未核定则不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [DPOison-VL: Clean Preference Poisoning in Vision-Language Direct Preference Optimization](https://arxiv.org/html/2610.18609v1) · 2026-10-13 · P1

    仅保留安全风险/防御评测线索，不执行poisoning训练；原完整研究高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Beyond Answer Voting: Fine-Grained Correction of LLM Reasoning through Graph Alignment across Sampled Traces](https://arxiv.org/html/2610.18606v1) · 2026-10-13 · P1

    细粒度graph correction必须真实生成/对齐多轨迹，完整推理成本过高不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [LLM2R: From Large Language Models to 3D Reassemblers](https://arxiv.org/html/2610.18604v1) · 2026-10-13 · P1

    LLM2R真实3D表示训练/解冻与多part pose评估总成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Rethinking Projector Training in Multimodal LLMs](https://arxiv.org/html/2610.18598v1) · 2026-10-13 · P1

    不能只跑30s闭式projector构造代替定义的多阶段能力验证；完整训练小时级，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [WAVE-0: Bridging VLA Policies and WAMs with Lightweight Latent Future Prediction](https://arxiv.org/pdf/2610.18568v1) · 2026-10-13 · P1

    核对官方PDF方法及资源页：WAVE-0以真实动作监督257M潜空间世界模型，保留future/delta/counterfactual ranking三项损失；冻结世界模型后，将VLM潜动作计划预测的future tokens接入动作专家，完整模型约4.3B，不是独立轻量257M原型即可复现。论文报告LIBERO使用8张96GB RTX PRO 6000、两阶段约10+13小时；RoboTwin使用8张H100、约6+78小时（正文汇总约670 H100 GPU小时），另有8张A800的实体双臂机器人实验。相对于单A100/A30或Mac预算明确过高，不下载权重/数据、不复现（审查DONE）；不把仿真fixture或仅世界模型局部训练冒充完整方法。

- [Two For The Price Of One: Curvature-Aware Pruning Preserves Influence Functions Too](https://arxiv.org/html/2610.18516v1) · 2026-10-13 · P1

    稀疏/低秩模型与IF保持需真实裁剪及影响函数评价，相对快5–25倍不足以核定全campaign绝对预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Towards Safe Autonomy for Computer Use](https://arxiv.org/html/2610.18508v1) · 2026-10-13 · P1

    可信边界与pixel/AX一致性必须真实验证，不用状态机替代；完整环境/模型调用预算未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [EgoOmniWorld: Unifying Egocentric Understanding via Ego-Action-World Interactions](https://arxiv.org/html/2610.18499v1) · 2026-10-13 · P1

    EgoOmniWorld交互/理解数据与多GPU适配完整配置高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Graph Metanetworks for Transformer Based Language Models](https://arxiv.org/html/2610.18471v1) · 2026-10-13 · P1

    必须真实权重图学习而非网络统计量proxy，原8GPU训练不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Readout Scaling Shapes Sparse Feature Recovery](https://arxiv.org/html/2610.18462v2) · 2026-10-13 · P1

    小SAE参数并不表示整轮廉价；原CPU实测已小时级，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [EmoGenie: Benchmarking and Evaluating Expressed and Evoked Emotion in T2I Generation with MLLMs](https://arxiv.org/html/2610.18455v1) · 2026-10-13 · P1

    情感生成评价完整训练和标注成本高，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [FastEEP: Fast Intra-Instance Elastic Scaling for Expert-Parallel MoE Serving](https://arxiv.org/html/2610.18451v1) · 2026-10-13 · P1

    定义能力依赖多节点MoE迁移/通信，不假设单A100能验证，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Thinker-WM: A Unified World Model with Shared Multimodal Representations for Embodied Intelligence](https://arxiv.org/html/2610.18447v2) · 2026-10-13 · P1

    只读原文资源段未核定完整多模态训练总预算；快速后台eval准备不代表完整训练便宜，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Agaram 2.5B: The First Tamil-First Language Model Trained from Scratch with Tool Calling. A Playbook for Under-Represented Languages](https://arxiv.org/html/2610.18420v1) · 2026-10-13 · P1

    仅SFT已小时级且还有从头预训练/工具数据，成本过高不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Multi-Stream Residual Computation in Diffusion Language Models](https://arxiv.org/html/2610.18407v1) · 2026-10-13 · P1

    多流写入量的核心训练/行为对照不能由残差张量单测替代；完整预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Bifocal: Training-Free Mixed Granularity Visual Token Pruning for Multimodal LLMs](https://arxiv.org/html/2610.18399v1) · 2026-10-13 · P1

    两stage混合granularity机制相关，但training-free全评测成本未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ReDiS: Reasoning-Diagnosis Self-Evolution for Multimodal Reasoning in Remote Sensing](https://arxiv.org/html/2610.18388v1) · 2026-10-13 · P1

    真实reasoning/diagnosis共训练需大量rollouts，完整多臂资源未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Hallucination-aware Faithful Reasoning in Remote Sensing](https://arxiv.org/html/2610.18369v1) · 2026-10-13 · P1

    跨模态忠实推理后训练多GPU配置高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Pin It on Anyone: Certified Targeted Displacement of Multi-Bit LLM Watermarks Without the Key](https://arxiv.org/html/2610.18359v1) · 2026-10-13 · P1

    仅作认证边界研究输入；真实oracle每context前向的完整采样成本未核定，不实现针对性破坏，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Omni-RS: Unifying Multi-Task Understanding and Generation in Remote Sensing](https://arxiv.org/html/2610.18323v1) · 2026-10-13 · P1

    统一遥感理解/生成需完整两stage训练，原配置多GPU长训练不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Beyond Equation Search: Conjecture-Guided Discovery with SCOPE and ClosureBench](https://arxiv.org/html/2610.18938v1) · 2026-10-13 · P1

    SCOPE需真实主动实验与证据闭环，不能用方程fixture代替；官方原文无廉价可核定总执行预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [TRACESTEER: Trace Driven Activation Steering for Hallucination Mitigation in Diffusion Language Models](https://arxiv.org/html/2610.18173v1) · 2026-10-13 · P1

    TraceSteer需真实去噪轨迹提取/介入，不把简单向量fixture当方法；原文资源片段无法廉价核定总预算，终态不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [SparPR: Runtime KV-Cache Recovery for Resource-Constrained LLM Inference on Consumer Hardware](https://arxiv.org/html/2610.18140v1) · 2026-10-13 · P1

    SparPR 用 query-aware 块选择、动态预算与按需局部重算恢复KV；虽然仅8GB笔记本，原文8K负载单次仍需44分钟，完整多长度/比例/消融会显著增长。按完整实验成本门槛不复现、审查 DONE，不启动小探针证明它慢。

- [A CaLLM Judge is a Better Judge: Mitigating Bias in LLM-as-a-judge](https://arxiv.org/html/2610.18108v1) · 2026-10-13 · P1

    后处理校准有低成本潜力，但已读片段未核定公开完整score矩阵与全bias发现/校准预算；不从仅方法名或便宜回归接受，按成本不确定性不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ResearchFlow-Eval: Tracing the Execution Gap in End-to-End Multi-Claim Autoresearch](https://arxiv.org/html/2610.18088v2) · 2026-10-13 · P1

    ResearchFlow-Eval完整多claim科研执行本身高成本，仅保留审计协议，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Same Function, Different Trajectory: No Standard Optimizer Is Equivariant to Transformer Reparameterization](https://arxiv.org/html/2610.18085v1) · 2026-10-13 · P1

    优化器非等变性的多规模匹配训练已经多GPU小时级，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [inLoRA-MINT: Internal Representations for Auditing Training Data in Domain-adapted LLMs](https://arxiv.org/html/2610.18051v1) · 2026-10-13 · P1

    inLoRA-MINT需真实内部activation和适配训练，完整公共数据/运行预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Data-Free Continual Learning for World Action Model with Rectified Generative Replay](https://arxiv.org/html/2610.18038v2) · 2026-10-13 · P1

    单次replay18分钟不覆盖约108分钟finetune、多task和多臂，成本过高不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [SHELDON: Reasoning through Dual Search over Hypothesis and Observation Spaces](https://arxiv.org/html/2610.18025v1) · 2026-10-13 · P1

    SHELDON完整双搜索与证据反馈总模型/执行预算未核定，不用固定候选树冒称RSI能力，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Match the Canvas, Not Just the Answer: Predictability-Aware SFT for Diffusion Language Models](https://arxiv.org/html/2610.18001v1) · 2026-10-13 · P1

    predictability-aware SFT完整最小预算本身小时级，成本过高不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ReEnvision: Future-Guided Selective Action Repair for Long-Horizon Manipulation](https://arxiv.org/html/2610.17977v2) · 2026-10-13 · P1

    145ms执行成本比110ms base低开销不代表训练/多task比较便宜；完整预算未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [BELT : BEhavior-Aligned Low-Rank KV Cache Compression with Learned Top-k Rank Allocation](https://arxiv.org/html/2610.17966v1) · 2026-10-13 · P1

    闭式key-side surrogate不能替代rank分配器与真实long-context质量/吞吐评测；总预算未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Virtual Head Attention](https://arxiv.org/html/2610.17959v1) · 2026-10-13 · P1

    虚拟head的核心architecture需实际训练/forward；已读资源段未核定完整token与设备预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [HaloBlock: Faster and Better Decoding for Diffusion Large Language Models](https://arxiv.org/html/2610.17948v1) · 2026-10-13 · P1

    block decoding真实多模型推理配置需多GPU，完整评测成本高，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [MERIT: Multimodal Evidence Reasoning over Image Tables](https://arxiv.org/html/2610.17937v1) · 2026-10-13 · P1

    table视觉感知与reasoning训练均需保留，不把gold支持事实交给被测Agent当能力；完整训练/评测预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Batch-Paced: Fixed-Budget Batch Decoding in Discrete Diffusion Language Models](https://arxiv.org/html/2610.17917v1) · 2026-10-13 · P1

    预算匹配的probe-decode原文排除在主表之外，不能省略其成本；全campaign预算未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [DriveWLA: Unifying Future Dynamics and Scene Semantics through World-Language-Action Modeling for Autonomous Driving](https://arxiv.org/html/2610.17903v1) · 2026-10-13 · P1

    完整world-language-action与RL训练多GPU高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [FlashMask-3: Efficient and Expressive Mask-Aware Distributed Attention](https://arxiv.org/html/2610.17901v1) · 2026-10-13 · P1

    Hopper专有内核与分布式声明不能在单A100/A30忠实验证，成本/硬件门槛不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Prefilling-dLLM v2: Learned Chunk Routing for Long-Context Diffusion Language Models](https://arxiv.org/html/2610.17868v1) · 2026-10-13 · P1

    chunk routing继续训练原配置多GPU，完整训练/长度扫成本高或未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [MicroCLIP: Connecting Text and Microscopy Images via Contrastive Language--Image Pretraining](https://arxiv.org/html/2610.17866v1) · 2026-10-13 · P1

    完整跨文本/显微图CLIP预训练高成本，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [DVTR-KD: Distilling Vision-Language Models via Intermediate Visual Token Reconstruction](https://arxiv.org/html/2610.17853v1) · 2026-10-13 · P1

    需真实视觉teacher与token reconstruction训练，原多GPU配置不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [What Makes a Good Visual Representation for Spatial Understanding in MLLMs?](https://arxiv.org/html/2610.17844v1) · 2026-10-13 · P1

    完整视觉表示空间理解迁移训练64GPU高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Diff Diffusion: Predicting Edit Paths with Diffusion Models for Efficient Code Editing](https://arxiv.org/html/2610.17831v1) · 2026-10-13 · P1

    DiffDiffusion的编辑路径模型、SFT/RL与多语评测需真实大规模训练，成本过高；本文未以本审查替代工业A/B细节验收。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [MHVF: Training-Free GUI Grounding via Verification-Guided Multi-Hypothesis Search](https://arxiv.org/html/2610.17792v1) · 2026-10-13 · P1

    MHVF training-free多假设搜索仍需大量真实VLMforward；完整多benchmark预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Full-duplex Spoken Language Modeling with Discrete Diffusion](https://arxiv.org/html/2610.17780v1) · 2026-10-13 · P1

    完整speech generator/listening/policy链路多节点高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [DT-LoRA: Reaching Beyond the Tangent Space of Low-Rank Adaptation](https://arxiv.org/html/2610.17730v1) · 2026-10-13 · P1

    低秩自身不是整轮廉价证据；已读资源片段未核定多任务训练预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [From Token Correction to Claim Admission: Training-Free Hallucination Mitigation for Large Vision-Language Models](https://arxiv.org/html/2610.17706v1) · 2026-10-13 · P1

    claim admission真实视觉证据与校准/多任务比较不可替代；单GPU可放下不等于总campaign便宜，预算未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [OccWAM: Occupancy World-Action Models with Joint Scene-to-Ego Flow Matching](https://arxiv.org/html/2610.17688v1) · 2026-10-13 · P1

    完整occupancy/action模型多GPU训练高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Encoding Context into LLM Weights: What Makes It Context?](https://arxiv.org/html/2610.17686v1) · 2026-10-13 · P1

    parametric context核心需真实多chunk优化和保持能力评价；单固定例效率仅补充不是全预算，未核定不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Code2Worlds-2: Physically Plausible Agent Harness for Embodied World Simulation](https://arxiv.org/html/2610.17651v1) · 2026-10-13 · P1

    物理可执行world构造需要真实几何/仿真与Agent闭环，完整调用/生成/执行预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [MemAct: Streaming Spatial Understanding with Memory and Active Exploration](https://arxiv.org/html/2610.17640v1) · 2026-10-13 · P1

    MemAct记忆写/读与主动探索均需真实长上下文训练及rollout，原多GPU/大数据高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Acting Through Registers](https://arxiv.org/html/2610.17638v1) · 2026-10-13 · P1

    Acting Through Registers需真实world/action训练，已读资源片段未核定完整预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Mixed Precision Scaling Laws for Quantized Pretraining](https://arxiv.org/html/2610.17637v1) · 2026-10-13 · P1

    混合精度scaling需完整预训练多臂，已读范围未核定总token/时长，不凭低bit推断便宜，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [The Tokens Strike Back: Safety-Aware Denoising with Directional Embedding-based Revision](https://arxiv.org/html/2610.17636v1) · 2026-10-13 · P1

    SADDER需要真实去噪路径/activation信号，完整多设置总预算未核定，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [From Pixels to Executable Physics: Behavior-Grounded World Models for Embodied Action Consequence Prediction](https://arxiv.org/html/2610.17630v1) · 2026-10-13 · P1

    真实生成物理与后果评估链路不能用规则占位；已读资源段未核定模型/数据/运行总预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [4LC: 4D Latent Cache for Efficient Conditioning in Dynamic World Modeling](https://arxiv.org/html/2610.17625v1) · 2026-10-13 · P1

    4Dlatent cache条件adapter/controlbranch完整训练高成本不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Revisiting the 16x Pretraining Compute Gap between Diffusion and Autoregressive Language Models](https://arxiv.org/html/2610.17590v1) · 2026-10-13 · P1

    16倍差距的再评估需真实预训练大网格；已读资源段未核定完整绝对预算，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [TwinPrune: Density-Aware Two-Phase Token Pruning for Vision-Language Models](https://arxiv.org/html/2610.17530v1) · 2026-10-13 · P1

    prefill/decode两phase剪枝需真实模型与完整质量/延迟/显存三轴评测，原多GPU最大模型/整轮成本高，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [ATTUNE: Agentic Throughput Tuning for LLM Training](https://arxiv.org/html/2610.17528v1) · 2026-10-13 · P1

    核心throughput调优目标是集群规模训练，不能只做配置编辑代替真实收敛验证，成本过高不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Box-WAM: Box Trajectories as Compact State Representations for World Action Models](https://arxiv.org/html/2610.17526v1) · 2026-10-13 · P1

    单步runtime优势不核定完整WAM训练/数据/闭环成本，原文资源片段无全budget，终态不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

- [Foundation Models for Event Prediction Across Heterogeneous Event Logs](https://arxiv.org/html/2610.17503v1) · 2026-10-13 · P1

    FEP attention非参数推断架构相关，但完整pretrain与每数据集多模型/6config/5seed对照明显多GPU大campaign，不复现。 成本过高或完整运行成本仍有实质不确定性，且只读核对后无法消除：不复现，审查DONE；不作本地实测声明。

</details>

<details markdown="1"><summary>后训练 / Agentic RL / OPD：80 项</summary>

- [Co-Evolving Acting and Forecasting for Language Agents](https://arxiv.org/html/2610.20597v1) · 2026-10-14 · P1

    CoPE 以成功 on-policy 轨迹的多步后续动作监督同一 backbone，不能替换成固定成功动作表。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [One Task, Many Interfaces: Simple Cross-Interface Consistency Training Improves LLM Agent Robustness](https://arxiv.org/html/2610.20576v1) · 2026-10-14 · P1

    CIPR 对去语义工具 ID、孪生接口和等价动作分布施加一致性 KL；原始双接口训练不能只用一个 KL 数值样例冒充。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Recovering Reliable Supervision via Critique-Guided On-Policy Distillation](https://arxiv.org/html/2610.20572v1) · 2026-10-14 · P1

    CriticOPD 让教师批评错误轨迹，学生修订，教师用特权 critique 打分；训练4张A100（学生2/教师2）、最长16384响应，评测8–32次采样。即使学生较小也不是低成本完整复现，不复现、审查 DONE。作者仓库已核为 kzhao5/CriticOPD。

- [Manacá-1B-Instruct-2: Reproducible Safety Alignment for a Native Brazilian-Portuguese LLM. Negative DPO Results, a Controlled Composition Scan, and a Silent Failure Mode of the LLM Judge](https://arxiv.org/html/2610.20570v1) · 2026-10-14 · P1

    Manacá公开三次负DPO、三轮Safety-SFT与数据配比扫描；负结果和judge拒绝评分的有效N问题应保留，不能以reward margin冒充生成能力。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [PrismaCoder: Pushing the Boundaries of Open Multimodal Code Intelligence through Decomposed Rubric Synthesis](https://arxiv.org/html/2610.20538v1) · 2026-10-14 · P1

    PrismaForge 将分解 rubric 同时用于多模态代码数据过滤和 RL reward，PrismaCoder 包含完整数据/训练链路。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [VASPO: Self-Distillation with Privileged Value Estimation](https://arxiv.org/html/2610.20516v1) · 2026-10-14 · P1

    VASPO 将同一特权上下文下 critic 的 PPO advantage 与自教师的有界概率比结合；原配置8 H200、full-parameter、200 rollout更新、每题8响应，成本过高，不复现、审查 DONE。

- [Hindsight-Privileged RLVR: Single-Rollout Token Credit Without Group Sampling](https://arxiv.org/html/2610.20497v1) · 2026-10-14 · P1

    HP-RLVR 用生成快照在因果/后见上下文中的 JS 差构造单轨迹 token credit，不读取参考答案。8B三任务100-step配对训练仍有大量绝对运行成本，不能因比GRPO相对更快当便宜；不复现、审查 DONE。

- [Training Language Models to Fail Gracefully](https://arxiv.org/html/2610.20401v1) · 2026-10-14 · P1

    GracefulRL 以 success/fallback/error 的 log-barrier/TailRL 目标和 smoothing 避免仅fallback坍缩；不能用手写回退规则替代策略学习。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [TreeFlex: Agents Navigating Their Own Search Trees](https://arxiv.org/html/2610.20334v1) · 2026-10-14 · P1

    TreeFlex 的Reflection/Execution共享policy导航自身search tree，并以tree-aware GRPO训练，真实工具/状态恢复不可换成预设搜索树。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [CASI: Credit Assignment via Set Intervention for Agentic Retrieval](https://arxiv.org/html/2610.20293v1) · 2026-10-14 · P0

    CASI 在固定检索快照上做集合干预，经 Shapley 归因和有界零和投影构造动作信用；正文 §4.5 随机七天、10% 生产流量 A/B，Advv +3.51%，工业证据通过。生产回放/教师与完整训练规模未公开，不能廉价核定忠实复现成本；按预算门槛不复现，审查 DONE。

- [Repairing Speech Access After Text Updates with Frozen Affine Fields](https://arxiv.org/html/2610.20253v1) · 2026-10-14 · P1

    AFFIRM 以冻结base修正加零均值query-conditioned affine correction修复speech access；不能把operator参数小误认整个获取/训练链路便宜。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [What Makes a Social Agent's Interactions Effective? Learning from Verifiable Outcomes in Paired Worlds](https://arxiv.org/html/2610.20195v1) · 2026-10-14 · P1

    PaCPO 在paired worlds中以逐turn暂定计划的可行性差异分配信用；隐藏私有约束由checker持有，被评测Agent不能直接读取两世界金标计划。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [RM-OPD: On-Policy Distillation for Generative Reward Models](https://arxiv.org/html/2610.20174v1) · 2026-10-14 · P1

    RM-OPD 先训练领域 GRPO 教师，再通过路由 OPD/领域权重合并生成奖励模型；74K 偏好、训练2节点×8 H800、评测8 H800，成本过高，不复现、审查 DONE。

- [MemDuet: Learning Dual-Process Memory for Long-Context Reasoning](https://arxiv.org/html/2610.19928v1) · 2026-10-14 · P1

    MemDuet 以小模型parallel evidence selection与大模型memory verification/update组成三阶段SFT/GRPO/joint策略训练。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [MolHop: Scaffold-Hopping Molecular Design with Agentic Reinforcement Learning](https://arxiv.org/html/2610.19920v1) · 2026-10-14 · P1

    MolHop 在约160万scaffolds层次空间内导航/编辑，并通过Agentic RL训练跨骨架发现策略。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Not All Criteria Matter: Importance-Aware Criteria Weighting for Rubric-Based LLM Evaluation](https://arxiv.org/html/2610.19915v1) · 2026-10-14 · P1

    ICW 通过LLM两两重要性比较、一致性修订和principal eigenvector导出rubric权重，不能以随机构造比较矩阵替代LLM比较再宣称后训练增益。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Rent-Seeking Language Models: Reward Models Set the Prices, Frequent Audits Curb the Rent](https://arxiv.org/html/2610.19832v1) · 2026-10-14 · P1

    Rent-Seeking 以proxy/gold reward和审计频率研究RL过优化，须保留固定测试床、同准确率proxy及真实训练，不能只模拟租金标量。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Learning Perception to Action Rules through Reinforcement Learning for Theory-of-Mind Reasoning](https://arxiv.org/html/2610.19796v1) · 2026-10-14 · P1

    ToM rule-GRPO 显式连接perception/belief/action并训练规则生成；须在development选择checkpoint且test隔离，不能用手写if-then取代模型学习。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [More Methods, Better Agents? A Reality Check on Self-Distillation in Agentic Reinforcement Learning](https://arxiv.org/pdf/2610.19789v1) · 2026-10-14 · P1

    Self-distillation reality check 比较十种方法与GRPO，132训练运行、12124.4 H800 GPU-hours；只保留公平比较结论，绝不整套重跑。成本过高、不复现，审查 DONE。

- [Qwen-MT-Lumen at WMT2026: Instruction-Specialized Translation via Quality-Aware Training and On-Policy Distillation](https://arxiv.org/html/2610.19758v1) · 2026-10-14 · P1

    Qwen-MT-Lumen包含CPT/SFT、online M2PO、教师OPD和结构修复的四阶段翻译系统，不是单一轻量损失函数。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [RouteWeaver: Weaving Mode Selection and Execution into Unified LLM Routing](https://arxiv.org/html/2610.19705v1) · 2026-10-14 · P1

    RouteWeaver 用COMET-GRPO拆分mode/execution信用，并以progressive exploration学习三类routing mode。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Function-Space Temporal Self-Distillation for Policy Optimization](https://arxiv.org/html/2610.19687v1) · 2026-10-14 · P1

    FSPO 保留稀疏历史next-token分布进行函数空间时序巩固，并结合特权纠偏与可靠性调节。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Model What Matters: Decision-Guided Selective World Modeling for Language Agents](https://arxiv.org/html/2610.19642v1) · 2026-10-14 · P1

    DGS-WM 依据后续策略决策选择observation单元，并用预测置信度调整辅助世界模型损失。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Divergent Paths: Learning an Outcome-Predictive Representation of LLM Agent Trajectories](https://arxiv.org/html/2610.19614v1) · 2026-10-14 · P1

    Precog-RM 学习轨迹表征并以few-shot outcome预测提前终止GRPO；47.3%是相对FLOPs节约，不是低成本绝对预算。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [PA1-OPD: One-Step Prefix-Augmented On-Policy Distillation for Language Model Pretraining](https://arxiv.org/html/2610.19601v1) · 2026-10-14 · P1

    PA1-OPD 在语料prefix后增加一步学生转移的教师监督，使用共享prefix tree-attention而非离线KD替代。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [INTACT: Inducing Latent Reasoning on a Frozen Backbone](https://arxiv.org/html/2610.19568v1) · 2026-10-14 · P1

    INTACT 在冻结backbone上训练外部latent encoder，先蒸馏written reasoning再以答案正确性RL强化；小可训练参数不等于短训练。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [$τ$-Emotion-Bench: Exposing the Interaction Fragility of LLM Agents through Real-World User Emotions](https://arxiv.org/html/2610.19560v1) · 2026-10-14 · P1

    τ-Emotion-Bench/Tracer以可中止的情绪用户交互筛选监督轨迹，并训练真实tool-calling policy，不是只改情绪标签。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Retrieve What Helps, Only When It Helps: Agentic Reinforcement Learning for Selective Retrieval-Augmented Machine Translation](https://arxiv.org/html/2610.19528v1) · 2026-10-14 · P1

    SRAT 通过agentic RL学习何时检索/检索何物，并联合Plackett–Luce与质量对比训练retriever。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Diagnosing and Correcting Reward Hacking in Verifiable Instruction Following](https://arxiv.org/html/2610.19525v1) · 2026-10-14 · P1

    CaLIF 用请求本身的冻结reference likelihood，在两条离线anchor界定的区域内补奖励，抑制空泛约束满足和likelihood inflation。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [ActICL: Post-Training for Agentic Multimodal In-Context Learning](https://arxiv.org/html/2610.19475v1) · 2026-10-14 · P1

    ActICL 联合学习多模态demonstration acquisition和answering，必须保留多turn检索/筛选与两阶段训练。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [MIPS: Mitigating Mode Collapse in Reinforcement Learning for Large Outcome Spaces](https://arxiv.org/html/2610.19457v1) · 2026-10-14 · P1

    MIPS 以学习的反向轨迹模型做marginal IPS，不能把真实结果概率直接送给被评测策略来替代定义机制。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [ForkGRPO: Efficient Exploration and Fine-Grained Credit Assignment for Diffusion Language Models](https://arxiv.org/html/2610.19408v1) · 2026-10-14 · P1

    ForkGRPO 在高熵中间状态fork，多组续写提供state内与state间segment credit，Fast分支仍需真实rollout训练。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Learning What to Keep: Transfer-Aware Personal Skill Learning from User Feedback](https://arxiv.org/html/2610.19380v1) · 2026-10-14 · P1

    SkillGrain 以原子rule transferability、rubric reward和细分credit联合优化skill induction/conditioned generation。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Beyond Corrected Actions: Training LLM Agents on Textual Critiques](https://arxiv.org/html/2610.19367v1) · 2026-10-14 · P1

    CAFT 对学生错误action同时生成专家纠正和文字critique再真实微调，并比较RL warm start。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Where to Start, How to Move: Analyzing Curricula under GRPO for Long-Horizon LLM Agents](https://arxiv.org/html/2610.19349v1) · 2026-10-14 · P1

    Guide-assisted GRPO 比较训练起点、handoff粒度与curriculum移动规则；成功reference前缀只限训练，不能在无辅助评测泄漏。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [DTDD: Divergence-Triggered Dynamic Distillation for Reliable On-Policy Supervision](https://arxiv.org/html/2610.19302v1) · 2026-10-13 · P1

    DTDD 用片段分歧触发教师接管，学生前缀继续 OPD、教师后缀行为克隆；原研究23实验臂、约22 serial hours和43M教师生成 tokens，成本过高，不复现、审查 DONE。

- [Verifier-Grounded Agentic RL for Provably Correct Code](https://arxiv.org/html/2610.19298v1) · 2026-10-13 · P1

    形式验证RL使用proof-obligation进度、隐藏probe和优先完整性审计，并有冻结proof specialist；简单单测奖励不能替代正式验证链路。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Outcome-Routed Distillation and Reinforcement Learning for Diffusion Language Models](https://arxiv.org/html/2610.19271v1) · 2026-10-13 · P1

    Outcome-routed dLLM训练对mixed groups用ratio-free REINFORCE，全失败但教师成功时走canvas KL，并以锚定KL保留能力。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Titan-Llama: Retrofitting Pre-trained LLMs with External Neural Memory Modules](https://arxiv.org/html/2610.19210v1) · 2026-10-13 · P1

    Titan-Llama 将部分attention换为可测试时更新的神经memory，需保留冻结/适配层和真实长上下文训练，非普通KV缓存演示。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Demystifying On-Policy Distillation: Where Does the Teacher's Advantage Live?](https://arxiv.org/html/2610.19145v1) · 2026-10-13 · P1

    OPD 教师优势分析用受控 token flips 与分叉续写拆解教师纠正收益；每个分歧又生成多次长续写，整套多模型/多分叉配置无法廉价核定运行预算，按成本门槛不复现、审查 DONE，不自动重跑。

- [Contextual Credit Policy Optimization](https://arxiv.org/html/2610.19103v1) · 2026-10-13 · P1

    CCPO 使用上下文相似度加权 observation-matched peers，并结合历史与未来信用；附录每次8 H200、约19200轨迹，完整复现成本高，不复现、审查 DONE。

- [GroundGUI: GUI Grounding by High-Quality Data and Distillation-to-Reinforcement Learning](https://arxiv.org/html/2610.19100v1) · 2026-10-13 · P1

    GroundGUI 以ScreenRef真实图文grounding数据进行SFT，再OPSD→RLOO的D2RL，不能只测point-in-box reward取代模型训练。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Backpropagating Verifier Rewards Through Continuous Flow Language Models](https://arxiv.org/html/2610.19080v1) · 2026-10-13 · P1

    连续flow LM以中间embedding critic绕过离散decode、反传pathwise verifier reward，须保留critic随policy更新的链路。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Who Should We Listen to More? Welfare-Aware Preference Acquisition for Pluralistic Alignment](https://arxiv.org/html/2610.19035v1) · 2026-10-13 · P1

    WAPA 用辅助reference估计个体supervision utility和marginal welfare gain，预算标签效率与完整推理/训练成本必须分开；oracle标签仅用于比较上界。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Tev: Scaling Long-Horizon Agentic Environments with Dense Progress Rewards](https://arxiv.org/html/2610.18868v1) · 2026-10-13 · P1

    Tev 以latent-world-first合成可验证环境，并用progress potential shaping训练长时程Agent；隐藏完整世界规范不能给被评测Agent读取。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Hybrid Reasoning Agents](https://arxiv.org/html/2610.18861v1) · 2026-10-13 · P1

    HybridAgent 以HybridLink在latent reasoning与文本tool interaction间切换，需保留HybridSFT/HybridRL和跨turn连续memory。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Two Clocks: Why Larger Rollout Batches Learn Slower but Fail on Schedule in Reinforcement Learning with Verifiable Rewards](https://arxiv.org/html/2610.18853v1) · 2026-10-13 · P1

    Two Clocks区分RLVR采样进度与collapse时钟，检验batch/sqrt-LR缩放及switch schedule；训练实证不能由二次近似数值图代替。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [MFG: Multi-turn Feedback Guided Molecular Optimization](https://arxiv.org/html/2610.18851v1) · 2026-10-13 · P1

    MFG 以跨turn property/similarity feedback与反馈对齐reward训练分子优化LLM，不能只用现成property打分器模拟学习。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [SkillScaffold: Scaffolding Agentic Reinforcement Learning with Policy-Adaptive Skill Credit Assignment and Selective Injection](https://arxiv.org/html/2610.18807v1) · 2026-10-13 · P1

    SkillScaffold 用verified trajectories的outcome-aware likelihood估计skill utility与选择/弃用，联合Generator/Executor训练；不允许金标成功轨迹被评测Agent直接读取。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Rubrics from the Task, Verdicts from Evidence: Pointwise Rubric Rewards with Tool-Augmented Judges](https://arxiv.org/html/2610.18766v1) · 2026-10-13 · P1

    ReVeR 以instruction-only rubric和tool-augmented pointwise judge做label-blind蒸馏，标签只过滤teacher outputs，不能泄漏到生成。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [PreciseCoder: Faithful and Generalizable Debugging Beyond Unit-Test Rewards](https://arxiv.org/html/2610.18755v1) · 2026-10-13 · P1

    PreciseCoder 在unit-test reward外增加语义核验的局部edit信用，并评估仓库级迁移；不能只以减少diff行数作为正确性奖励。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Enabling Token-wise Importance Sampling in Off-Policy RLVR with Proximal KL Regularization](https://arxiv.org/html/2610.18738v1) · 2026-10-13 · P1

    Proximal KL 将proximal reference与behavior policy分离，用token-wise IS及future KL credit替代clip；tabular保证的coverage/expressiveness条件不自动适用于Transformer。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [A Refresh Interval Does Not Fully Specify a Refresh Schedule: Learning-Rate-Dependent Placement in Kronecker-Preconditioned Language Model Training](https://arxiv.org/html/2610.18695v1) · 2026-10-13 · P1

    Kronecker refresh placement研究固定refresh数下的LR相关排序反转，是训练调度实证，不以单次数值测试冒充完整跨LR结论。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [ProAS: A Progress-Aware Advantage Shaping Framework for Multi-Turn Agentic Reinforcement Learning](https://arxiv.org/html/2610.18683v1) · 2026-10-13 · P1

    ProAS 动态Agentic Reference Graph支持无效正信用mask与不对称负信用重分配，保留ARG定义而非用金标计划直接决策。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [MultiAlloc: Budget-Aware Precision Allocation for KV Cache Quantization](https://arxiv.org/html/2610.18642v1) · 2026-10-13 · P1

    MultiAlloc 通过离线layer sensitivity/token importance profiling，在固定KV预算内联合分配层与token保真精度。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Can an Agent Learn to Predict Its Own Failure? Outcome-Grounded Confidence Calibration in LLM Agents](https://arxiv.org/html/2610.18614v1) · 2026-10-13 · P1

    Outcome-grounded confidence用每step置信度对最终episode outcome的proper scoring rule训练，必须分离任务难度、深度与attempt foresight。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Does self-distillation improve reasoning?](https://arxiv.org/html/2610.18613v1) · 2026-10-13 · P1

    Self-distillation reasoning复核区分OOD泛化、thinking-mode迁移和梯度对齐；保留其负结果，不能重新标成普适收益。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [LLM Agents for Automated Post-Training via Structured Recipe Optimization](https://arxiv.org/html/2610.18572v1) · 2026-10-13 · P1

    SRO 让Recipe-Space Designer显式定义可组合选择，再用结构化trial evidence和multi-objective BO搜索多域post-training配方。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Imprinting: Knowledge Distillation Can Shift Student Behavior](https://arxiv.org/html/2610.18517v1) · 2026-10-13 · P1

    Imprinting研究教师安全倾向经普通任务distillation迁移，并比较divergence-token mask/rewriting与后续偏好优化；是多教师-学生因果比较，不是单步loss检查。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [How Low Can You Go: Fine-Tuning LLMs with Bayesian Optimization (LlMBO)](https://arxiv.org/html/2610.18504v1) · 2026-10-13 · P1

    LlMBO 在TinyLoRA低维参数上做Gaussian-process BO并直接优化greedy accuracy；优化参数很少仍需大量LLM生成。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [ReTerm: Recovery Training for Self-Improving Terminal Agents](https://arxiv.org/html/2610.18484v1) · 2026-10-13 · P1

    ReTerm 先以恢复demonstration SFT，再从自身failure states fork多条恢复rollout做ReTerm-GRPO。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Teacher-Guided Tool Learning for Small Language Models via Bidirectional KL Constraints](https://arxiv.org/html/2610.18459v1) · 2026-10-13 · P1

    SeTPO 以低reward轨迹reverse-KL advantage加持续forward-KL示范监督协调探索；0.5B能放入单卡不等于完整对照预算已核定。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Copying Is Not Grounding: Training Faithful Long-Form RAG with Authored-Sentence Credit](https://arxiv.org/html/2610.18442v1) · 2026-10-13 · P1

    ASC 将faithfulness reward/advantage移到authored sentence，排除copy与空泛句并基于同query所有sentences作比较。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Teach Me After You Learn It: Lookahead Self-Distillation for RLVR](https://arxiv.org/html/2610.18256v1) · 2026-10-13 · P1

    LEAD 以disjoint on-policy子组做virtual RL lookahead teacher，再cross-group token distillation并调和GRPO信号。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [TextualRL: Textual Reinforcement Learning for Context Management](https://arxiv.org/html/2610.18216v1) · 2026-10-13 · P1

    TextualRL 以同任务rollout组做critique，并跨组证据审查bounded context patches，候选采用由held-out validation决定，不能换成金标脚本策略。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [A Few More Tokens Ahead: Reinforcing Parallelism in Diffusion LLMs](https://arxiv.org/html/2610.18200v1) · 2026-10-13 · P1

    RePara 用连续短token blocks的group-relative policy updates强化dLLM并行生成，不能只改decode quota冒充RL训练。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Failure Recovery via Belief Updates and World Modeling for Long-Horizon Agents](https://arxiv.org/html/2610.18082v1) · 2026-10-13 · P1

    BELIEFWEAVER 以跨尝试relational belief和IWM预测修复方向，且将IWM组件SFT/OPD到9B学生，非简单backtrack状态机。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [WorkRover: Scaling Long-Horizon Cowork Agent Training Via Recursive Environment Evolution](https://arxiv.org/html/2610.18067v1) · 2026-10-13 · P1

    WorkRover 用dependency-closed factorial replay选择最小validated环境修订，并以VTCA给真实workspace进度分配credit；不能把静态registry标签当可执行自进化。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Correcting or Continuing? What On-Policy Distillation Learns from Student Errors](https://arxiv.org/html/2610.18011v1) · 2026-10-13 · P1

    错误集中OPD研究比较五机制、八配置与非失败集中positive control；保留accuracy下降和训练KL仍下降的负结果，不把diagnostic当改进。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Fish Audio Drama 3 Technical Report](https://arxiv.org/html/2610.18010v2) · 2026-10-13 · P1

    Fish Audio Drama 3 v2是35B-A3B语音生成模型的三阶段pretraining、SFT和human-preference RL报告，推理单H200不代表训练可单卡复制。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Agent-Reflex: Teaching Language Agents to Act Reflectively](https://arxiv.org/html/2610.17953v1) · 2026-10-13 · P1

    Agent-Reflex包含噪声grounded skill discovery、ReSFT与reflection-guided on-policy RL三阶段，不以提示反思模板替代训练。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [PaceReasoner: Label-Free Learning to Answer Briefly from Long Reasoning](https://arxiv.org/html/2610.17900v1) · 2026-10-13 · P1

    PaceReasoner 用LONG consensus监督SHORT，配行为reward与ratio controller；label-free不等于低生成成本，也须保持adaptation/test边界。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Training LLMs for Multi-Agent Collaboration with Verifiable Information Rewards](https://arxiv.org/html/2610.17893v1) · 2026-10-13 · P1

    CoSIR 以Bayesian team-surprisal下降奖励信息披露/请求/使用，并以self-play后训练迁移合作行为；评价器可用正确option，但Agent不得读取它。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Efficiently Learning To Reason or Not to Reason: Root-token Policy Optimization for Adaptive Thinking](https://arxiv.org/html/2610.17767v1) · 2026-10-13 · P1

    RPO 只训练是否think的root token，但必须采样两mode真实长轨迹形成group-relative advantage，不能把人工difficulty gate当复现。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Explore with Memory, Learn without It: In-Context Exploration and Self-Distillation for LLM Reasoning](https://arxiv.org/html/2610.17734v1) · 2026-10-13 · P1

    LEAF 以动态problem-specific memory辅助探索，再将有记忆行为self-distill到无记忆policy；记忆和validation/test边界不能省略。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [CoCA: Criterion-Aware Credit Assignment for Rubric-Based Reinforcement Learning](https://arxiv.org/html/2610.17733v1) · 2026-10-13 · P1

    CoCA 由criterion group-relative outcome建立credit，再按criterion-induced distribution shifts分配token，非直接模仿privileged teacher。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [TSRL: Trigger-based Supervised Reinforcement Learning for Continual Agent Training](https://arxiv.org/html/2610.17726v1) · 2026-10-13 · P1

    TSRL 在RL中只对失败hard states触发SFT，研究持续学习遗忘；不能用成功轨迹oracle替代真实expert supervision。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [DeltaTTG: Training Multi-Turn Agents with a Token-to-Go Progress Meter](https://arxiv.org/html/2610.17666v1) · 2026-10-13 · P1

    DeltaTTG 以真实多策略成功轨迹训练TTG progress meter，再冻结meter重分配actor outcome advantage；meter不能以已知剩余金标计划长度替代。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [Decouple to Forget: Semantic Mediation for Sensitive Unlearning in Large Language Models](https://arxiv.org/html/2610.17654v1) · 2026-10-13 · P1

    D2F 先拆解敏感fact mediator、生成保持非敏感内容的反事实，再做preference-based unlearning；单A10040GB和2epochs路径可容纳，但不能忽略GPT-4o构造/审计和双benchmark全链路。核对官方方法/资源片段后，完整忠实复现的总成本仍有实质不确定性，按单卡预算门槛收口；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

- [RELAY: Selective Self-Distillation with Adaptive Hand-off for Rubric-Based Reinforcement Learning](https://arxiv.org/html/2610.17623v2) · 2026-10-13 · P1

    RELAY v2按positive/low-zero-advantage选择蒸馏rollouts，并以loss plateau停用教师后继续GRPO；已按v2而非v1审查。原文资源配置超出本轮单卡低预算范围；成本过高，不复现（审查 DONE），不进入自动重试或 evolve。

</details>

<details markdown="1"><summary>Agent / RSI：76 项</summary>

- [Player-1: Learning to Play from Synthetic Experience](https://arxiv.org/html/2610.20584v1) · 2026-10-14 · P1

    Player-1 的SFT与多环境PPO是核心；官方HTML附录D.3明确每模型SFT为32×H200约24h、RL为64×H200约36h，另有512并发环境。成本显著超出单卡预算，不复现。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Latent Compaction with Test-Time Training](https://arxiv.org/html/2610.20582v1) · 2026-10-14 · P1

    Latent Compaction 冻结模型但对每份文档做attention fitting和端到端cache蒸馏，并非零训练压缩。原文建议两个阶段各1000更新，RULER每task-length有20文档；完整准备/多模型评测成本明显，单卡预算内无法廉价确认总耗时。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Beyond LLM Judge: Mechanical Verification for Agentic Autoformalization](https://arxiv.org/html/2610.20573v1) · 2026-10-14 · P1

    该工作结合LLM语义复核、numerical/vacuity checks，不能只跑零费用vacuity check当完整验证器。附录F给1539项numerical约\$314.18/77s每项、back-translation约\$99.57，完整机械/模型联合研究成本高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Scaling Discovery Requires Forgetting](https://arxiv.org/pdf/2610.20563v1) · 2026-10-14 · P1

    Forgetting 清空搜索会话/历史而保留best candidate，机制有价值；但研究包含多agent、四种可执行科研任务、30提案续跑与多replicate。PDF费用表与图证实是持续搜索预算，不能以常量缓存重置fixture代替完整发现过程。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [PhySGA: A Physics-Space Grounded Agentic Framework for Generalizable and Interactive 3D Composition](https://arxiv.org/html/2610.20560v1) · 2026-10-14 · P1

    PhySGA 需Assembly/Critic、真实物理primitive、skill反馈和Isaac Sim完整资产链。§4.1在120 prompts上用GPT-5.5与Isaac Sim 4.2.0；硬件、资产准备及反复物理闭环总成本仍无法廉价核定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [From Relevance to Validity: Zero-Shot Tool Selection via Functional and Contextual Validation](https://arxiv.org/html/2610.20388v1) · 2026-10-14 · P1

    工具transfer-validity方法需representation extraction、训练与capability ranking，并在缓存工具环境中调用实际backbones/judge。附录I.4三张95GB卡、三seed及分离远端模型；完整预算单卡下不能廉价确认。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Reflect After Failure: Brain-Inspired Self-Evolving Agents for Embodied Spatial Intelligence](https://arxiv.org/html/2610.20312v1) · 2026-10-14 · P1

    HiMeco 结合PEP诊断、策略bank和可执行skill；原文八A6000/API、208固定episode共1664 planned executions，成本高。相同episode四round适配与独立跨episode转移必须区分；诊断可看reference snapshot，不得把它输入在线agent或当隔离test改进。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [P2Patch: Exploit-Guided Vulnerability Repair](https://arxiv.org/html/2610.20245v1) · 2026-10-14 · P1

    P2Patch 在每次repair后生成独立同漏洞exploit并累计PoV，保留construction/held-out oracle隔离。101真实CVE、多模型攻修闭环与原文明确增加的end-to-end成本超过便宜候选范围。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [SWE-Stream: Scaling Executable Training Data for SWE Agents via Progressive Construction and Elastic Streaming](https://arxiv.org/html/2610.20193v1) · 2026-10-14 · P1

    SWE-Stream 的渐进任务构造和elastic streaming必须实际重建/验证仓库。80,874任务、118,688轨迹、30B训练；受控scheduler实验达到500任务也需23.06h，完整复现成本过高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Why Generate a Click? Plug-in Decision Heads for Web Agents](https://arxiv.org/html/2610.20107v1) · 2026-10-14 · P1

    Plug-in heads 需要先有213K web steps训练出的4B/8B generator，再训练heads与级联；不是仅加一个小线性层。附录B两GPU训练、4B joint约11小时及96GB卡配置，成本过高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [EvalBuilder: Can LLMs Build Efficient Benchmarks?](https://arxiv.org/html/2610.20099v1) · 2026-10-14 · P1

    EvalBuilder 要实际为昂贵reference benchmark生成/迭代proxy并核验held-out ranking，不能只写一个打分器。附录B.1真实运行4h33m、7h9m、13h7m和16h上限，超出本轮廉价复现预算。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Memorizing Who, Knowing How: Benchmarking Personal and Procedural Memory for Persistent Assistants](https://arxiv.org/html/2610.20022v1) · 2026-10-14 · P1

    PraxisMem 联合维护个人/程序记忆，并通过privileged joint-state监督、location-aware GRPO和OPSD训练manager。不能以读取gold state的fixture替代可部署manager；训练及20长trajectory成本仍无法廉价核定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [A Strong Harness Narrows the Model Gap: A Comparative Evaluation for Legislative Document-to-XML Conversion](https://arxiv.org/html/2610.19999v1) · 2026-10-14 · P1

    立法XML pipeline 的关键是实际工具、持久状态和citation authority lookup，而不是只切分文档。正文明确未记录tokens/latency/\$，153 bills×3harness×3模型完整总成本不可从保留产物恢复；不廉价试跑探测。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [AtomSearch: Evidence-Grounded Tree Search for Agent Skill Optimization](https://arxiv.org/html/2610.19951v1) · 2026-10-14 · P1

    AtomSearch 对证据支持的原子技能修改做 skill-state 树搜索与回归/修复记忆；单实验约923–17200 item evaluations且多个目标模型，完整搜索成本高，不复现、审查 DONE。

- [Explorer-Zero: Improving Self-Play for Long-Horizon Tasks with Decomposable Verifiable Rewards](https://arxiv.org/html/2610.19868v1) · 2026-10-14 · P1

    Explorer-Zero 需要proposer/solver交替自博弈并保存环境checkpoint作训练奖励。附录D是8×H100、每ALFWorld运行约15 node-hours、AppWorld约29；不能以小fixture或只实现reward函数当作自博弈复现。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Euler: Towards Human-Centered Multi-Agent Mathematical Discovery](https://arxiv.org/html/2610.19864v1) · 2026-10-14 · P1

    Euler 用research graph与saved team state组织长期数学探索，并具备预算reservation。三数学case不能证明其全流程廉价；已查resource accounting与case范围，frontier调用/证明工具/长期继续的真实复现预算仍不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [DeltaStreamer: Towards Human-Like Agentic Streaming Video Understanding](https://arxiv.org/html/2610.19849v1) · 2026-10-14 · P1

    DeltaStreamer 的change-aware记忆、planner和历史视频replay均需27B多模态模型。§4.1是8×A100 BF16、1fps处理，不能以文本摘要fixture代替视频观察/回放。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [LAGO: Language Agents with Reusable Growing Options](https://arxiv.org/html/2610.19843v1) · 2026-10-14 · P1

    LAGO 的meta-agent/agent-option library需要真实问题分解、工具执行和结果核验。35B-A3B、500 SWE任务及150任务重跑对照，长真实仓库运行总成本高，不能用预定options或gold decomposition替代。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [EGCForest: Structured Agent Memory Organization for Enterprise Group Chats](https://arxiv.org/html/2610.19836v1) · 2026-10-14 · P1

    EGCForest 的三forest、Placement Map与结构桥需要实际summary构造和embedding。206MB/65ms是存储和在线retrieval，不包括三基准离线建库/回答；0.6B encoder虽小，完整LLM建库预算仍不确定，不因低在线延迟接受。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [ActionOPD: Distilling Decisions, Not Tokens](https://arxiv.org/html/2610.19820v1) · 2026-10-14 · P1

    ActionOPD 必须在学生遇到的状态上采样学生/教师动作并用语义一致度做policy optimization；不能只做offline token imitation。4B/8B、多teacher、每状态4candidates与闭环工具评测，完整成本仍无法廉价核定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Evolve Together, Fall into Place: How Social Scaffolding Shapes Self-Evolving Multi-Agent Systems](https://arxiv.org/html/2610.19799v1) · 2026-10-14 · P1

    AGORA 研究社会scaffolding如何改变自演化team，而原实验8张96GB RTX PRO 6000、900秒session、多次重复。完整进化和控制组成本过高，不把组织标签或静态角色配置当实现。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [StateCraft: Augmenting Video World Models with Abstract-State Reasoning](https://arxiv.org/html/2610.19795v1) · 2026-10-14 · P1

    StateCraft 将持久抽象状态与视频diffusion共同训练；原文两个backend各约400 H200 GPU-hours、约2000条×300动作轨迹，完整链路超预算。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [PRISMATIC : Prescription Risk Inspection System for Multi-Agent Treatment Interaction in Clinical Decision-Making](https://arxiv.org/html/2610.19762v1) · 2026-10-14 · P1

    PRISMATIC 的DSWA/DFPC需要多专科代理迭代并跨病例更新。已查MIMIC-IV病例/处方数据和blackboard方法；访问受限病历、LLM多轮总调用与医学复核成本未能廉价界定，不启动试跑，也不将金标处方作为代理输入。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [New Model, Old Habits: Behavior Transfer under Model Swapping in Multi-Session LLM Agents](https://arxiv.org/html/2610.19712v1) · 2026-10-14 · P1

    DASH 按交换方向和历史作者选择原始历史/摘要，需在多session真实任务上反复换模。已查重复交换设置和局限；闭环任务、原始推理可见性及多模型组合的总调用成本仍无法在单卡/Mac预算下廉价核定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [C3: Rethinking Process Supervision via Confidence-Guided Credit Correction in Multi-Turn Reinforcement Learning](https://arxiv.org/html/2610.19695v1) · 2026-10-14 · P1

    C3 在base RL advantage估计后按置信度修改坏span正信用，必须保留真实RL训练。Qwen3-8B search、4B full-parameter WebShop、critic与critic-free多臂及检索模型成本高/仍材料性不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [MCAIR: Monitoring and Correcting Agent Unfaithfulness via Internal Representations](https://arxiv.org/html/2610.19679v1) · 2026-10-14 · P1

    MCAIR 的CPU probe单次低于0.2ms仅是在hidden state已经提取之后，不含模型生成和纠正。原文8B/12B/14B、两张RTX A6000、分层扫描和三次纠正实验；完整采样/表征提取成本仍高或不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [JevCoder: When Does Decision Delegation Pay Off in Code Repair?](https://arxiv.org/html/2610.19596v1) · 2026-10-14 · P1

    JevCoder 的低费率judge不代表repair agent整体便宜。原文compute段明确两张L40S、约200 GPU-hours和\$1500 API，完整研究超预算。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [L3M: A Verifiable Harness and Runtime for Self-Extending and Self-Improving Agents](https://arxiv.org/html/2610.19591v1) · 2026-10-14 · P1

    L3M 包含 Git 状态轨迹、能力收窄授权和 Lean 内核检查的运行时；未核定可直接复用的完整上游实现，Terminal-Bench全套调用成本也未能廉价确定。按预算门槛不复现、审查 DONE；不能用Python状态机假装Lean证明。

- [XferAgent: Cross-Agent Experience Transfer for Self-Improving LLM Agents](https://arxiv.org/html/2610.19581v1) · 2026-10-14 · P1

    XferAgent 在执行前从local/shared graphs路由经验、执行后用结果更新；不是静态共享提示。四域、异构framework、多task-pass构造和真实回归评测的总成本经现有方法/ALFWorld设置仍不能廉价确认。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Mission (Im)Possible: Towards Autonomous Discovery of Autopilot Logic Flaws in Open-Source Drone Frameworks](https://arxiv.org/pdf/2610.19566v1) · 2026-10-14 · P1

    IMF 需三agent协作静态slicing、真实模拟测试和log oracle验证；PX4/Ardupilot105个新发现不是可廉价重跑的单脚本。已查官方PDF执行例子，构建/仿真/长frontier调用预算仍材料性不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [MemCode: Discrete Semantic Representations for Long-Term Agent Memory](https://arxiv.org/html/2610.19472v1) · 2026-10-14 · P1

    MemCode 不能只做cheap在线检索而省略ISQ学习。附录B给64,935 DailyDialog训练对、T5-base VQ-VAE、10epochs、32GB GPU/90GB RAM；离线训练与LLM原子写入总成本仍高/不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [PFedMA: Who Should Join Next as Federated Multi-Agent Orchestration Evolves?](https://arxiv.org/html/2610.19458v1) · 2026-10-14 · P1

    PFedMA 的orchestrator经PPO训练，privacy规则还要双向跨client演化；不能只实现agent selection打分。附录E.3为batch64、最多220步，闭环跨客户/安全评测完整预算仍材料性不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [EvoProbe: Evaluation-Driven Benchmark Evolution for LLM Agents](https://arxiv.org/html/2610.19433v1) · 2026-10-14 · P1

    EvoProbe 的新task生成、可执行subtask验证、多judge诊断和反馈再生均在核心闭环中。66个网络安全任务、八模型两轮并需人工quality review，完整成本与任务基础设施仍无法廉价界定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [VideoHarness-SRSI: Structured Recursive Self-Improvement for Video Understanding Harness](https://arxiv.org/html/2610.19424v1) · 2026-10-14 · P1

    VideoHarness-SRSI 保留content-free反馈、probe-race、factorial组合和独立验证边界；原研究分析4000多个演化候选、四视频基准和三seed，不能廉价完整搜索。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Beyond the Trial-and-Error Loop: Hybrid Projection and Automated Tuning for Distributed Training](https://arxiv.org/html/2610.19423v1) · 2026-10-14 · P1

    Primus Projection 具有CPU simulation路径，但原论文的tuning收益依赖真实GPU微基准校准与多节点验证；671B/1024GPU、235B/256GPU均不在预算。只跑未校准CPU仿真不能宣称复现其吞吐预测或agent tuning效果。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [AgentSafeEvo: Adversarial Co-Evolution for LLM Agent Safety](https://arxiv.org/html/2610.19422v1) · 2026-10-14 · P1

    AgentSafeEvo 必须执行attacker/defender RL共同演化与learnability weighting。附录D.1每role4GPU、120steps、64batch和16Kresponse，成本过高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [From Failures to Learnable Worlds: Policy-Conditioned Environment Generation for Navigation Agents](https://arxiv.org/html/2610.19420v1) · 2026-10-14 · P1

    WEDGE 用失败差异生成并验证weakness，再针对性生成导航世界和训练。正文4.4仍需约21K policy rollouts才得到4.2K候选；十次LLM弱点发现不是整个开销。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [SERO: Learning from Executable Oracle Continuations for Long-Horizon Agentic Reinforcement Learning](https://arxiv.org/html/2610.19397v1) · 2026-10-14 · P1

    SERO 的可执行oracle续写、状态恢复和policy-reachability加权是中心，oracle应只用于training。附录E.1为每batch16×8rollouts、50步horizon、1.5B/7B及多optimizer，完整训练和oracle续写预算仍高/不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [STRATA: Self-Maintaining Structured Experience Graphs for Self-Evolving Language Agents](https://arxiv.org/html/2610.19386v1) · 2026-10-14 · P1

    STRATA 的typed graph、reflector、community induction、GC和contrast edges需真实在线任务流。4基准、2backbones、7baselines、三seed且WebArena812题，多模型完整闭环成本高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [EvoWeave: Composing Reusable Agent Experience through Operation Level Graphs](https://arxiv.org/html/2610.19381v1) · 2026-10-14 · P1

    EvoWeave 依靠真实operation contracts、directed connections及执行后的reflection，不是仅注册一张图。四基准/五设置/三backbones；附录F坦言不同成本项不能合并成统一总成本，完整预算仍不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [DeLoop: Repeated Actions as Self-Supervision for Long-Horizon Agents](https://arxiv.org/html/2610.19376v1) · 2026-10-14 · P1

    DeLoop 从真实rollout重复动作挖negative、后续首个非loop动作作positive并DPO，不能用gold action冒充。8B/14B/32B、上千收集episode和跨环境对照的训练/采样总成本仍高/不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Policy-Verified Self-Training: Learning Agent Compliance from Verifiable Policy Rewards](https://arxiv.org/html/2610.19372v1) · 2026-10-14 · P1

    PVST 把确定性policy gate变为RFT/DPO监督，但正文也说明verifier受attack-goal设计、部分binding弱于原条款。8B/4B多臂训练及AgentDojo闭环rollout的总成本经已有正文配置仍不确定；不把仅编译gate登记为训练能力。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [MemeTrace: A Multimodal LLM-Based Agent for Safety-Aware Meme Provenance Analysis](https://arxiv.org/html/2610.19267v1) · 2026-10-13 · P1

    MemeTrace 每meme平均18.46步骤、11.54次多模态调用和3.92次search；原文平均\$0.1259/111秒。仅100例主集已约3.1串行小时（由论文均值估算，非本地实测），另有多模型/消融/鲁棒性运行，完整复现成本高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [ChunkAct: Action Chunking for Agentic Robotics](https://arxiv.org/html/2610.18874v1) · 2026-10-13 · P1

    ChunkAct 必须真实执行VLA/分割/失败退出后重新规划；原文LIBERO-Pro多套件、GPT-5.6-sol high、每episode最多100 calls。完整VLA和仿真资源成本未能廉价界定，不用固定动作chunks冒充机器人能力。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [SEAR: Self-Evolving Agentic Robotics](https://arxiv.org/html/2610.18792v1) · 2026-10-13 · P1

    SEAR 区分保留经验与重复尝试、privileged state和预算，审查价值高；330模拟/5物理任务、四年以上累计agent runtime以及多小时practice/AR配置明显超预算。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Beyond the Verdict: Agentic Code Judging with Verifiable Feedback](https://arxiv.org/html/2610.18760v1) · 2026-10-13 · P1

    ARBITER 为35B MoE verifier经RL学习真正生成可执行counterexample；每candidate平均35.0K–46.9K输出tokens。训练及多次refinement成本高，不能用官方失败样例或judge标签替代反例生成。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Kwai Summary Attention V2 Technical Report](https://arxiv.org/html/2610.18654v1) · 2026-10-13 · P1

    KSA V2 结合 Summary→Meta KV 压缩与 summary-guided 原始块稀疏索引；1.9B/4B、128K上下文及数十亿tokens分阶段训练，成本过高，不复现、审查 DONE。

- [Knowledge Graphs as Files: An Agent Harness Where Tool Creation and Tool Use Co-Evolve](https://arxiv.org/html/2610.18616v1) · 2026-10-13 · P1

    DKGI 将完整 KG 作为文件，让工具创建和使用共进化；三图谱和frontier模型，每次最多300 turns/1800秒，多次评测成本高，不复现、审查 DONE。作者仓库 leopoldwhite/DKGI 已核。

- [The Last Mile of Coding Agents for Long-Document Tasks: An Empirical Study on Clinical Trial Protocol Digitization](https://arxiv.org/html/2610.18507v1) · 2026-10-13 · P1

    TrialScribe 将domain skills和verification loop用于协议PDF数字化；真实27B推理/工具执行不能用gold提取字段替代。原文§4.2两A100、150长协议且多模型/metric，对单卡预算成本过高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Judges Follow the Reference: The Derivation Gap in Verifying Tool-Call Arguments](https://arxiv.org/html/2610.18497v1) · 2026-10-13 · P1

    DeRef 用不见candidate的独立deriver从完整历史生成参考，而不是给judge直接喂gold。原文27B deriver、多个大bench、长历史并报告每reference调用秒级成本；完整多judge/多设置总运行成本高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [MemoryVLN: From Ego-Aware Memory Representation to Cross-Context Memory Reuse in Vision-Language Navigation](https://arxiv.org/html/2610.18478v1) · 2026-10-13 · P1

    MemoryVLN 的压缩、ego-aware多模态表示、层次memory与write-back需实际VLN训练。附录A.3给64GPU global batch64，另有VGGT/Habitat链路，成本过高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Reliable Memory from Unstable Growth: Curating Self-Written Agent Playbooks with Randomized Experiments](https://arxiv.org/html/2610.18427v1) · 2026-10-13 · P1

    RBC 用随机block inclusion估计lesson效果，并用fresh practice选择curated/whole/no-playbook，保留test隔离。原文19settings、每项3growth runs和三eval seeds，每score数百到数千真实episodes，完整成本高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Delegating Earth science model calibration to knowledge-guided LLM agents](https://arxiv.org/pdf/2610.18378v1) · 2026-10-13 · P1

    GCH 将agent声明冻结后交给确定性数值搜索，完整六模型calibration包含80–600 evaluations与三seed，并不等于只写配置。已查官方PDF表B3及附录C，模型执行/知识基础设施和完整搜索耗时仍材料性不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Urbex: Agentic Spatial Grounding for City-Scale 3D Scenes](https://arxiv.org/html/2610.18356v1) · 2026-10-13 · P1

    Urbex 的active spatial search政策要真实渲染/工具交互并RL训练。原文hardware段是16×H20训练；单H20约3.2s/query只代表在线推理，不含offline scene preprocessing。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Beyond Answer Sharing: TrueMAD for Targeted Peer Engagement in Multi-Agent Debate](https://arxiv.org/html/2610.18240v1) · 2026-10-13 · P1

    TrueMAD 的targeted peer advice必须由真实同伴模型生成，不能用gold critique。主设置30B-A3B、多agent、多round及三个reasoning基准；完整多臂预算经原文设置仍无法廉价界定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [The Agentic Scientist: Orchestrating Coding Agents for Automated Scientific (Co-)Discovery](https://arxiv.org/html/2610.18933v1) · 2026-10-13 · P1

    The Agentic Scientist 是完整研究编排/验证管线，不是仅多agent对话。附录有20–60 ideation cycles、每candidate最长3小时、250epochs和最高1B环境steps等任务配置，超本轮预算。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [APT: Feedback-Driven Agentic Post-Training for Text-to-Image Generation](https://arxiv.org/html/2610.18097v1) · 2026-10-13 · P1

    APT 的核心是agent生成评测/诊断/训练分布后实际RL更新图像生成模型。多base generator、多benchmark与迭代生成/训练成本高或材料性不确定；只做prompt选择不能算其复现。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [AReaL-RSI: Adaptive Scaling and Coordination of Recursive Self-Improvement](https://arxiv.org/html/2610.18083v1) · 2026-10-13 · P1

    AReaL-RSI 需leader、conditional memory sharing及campaign后的证据复盘。原文KernelBench每researcher1小时、RSIBench每researcher2小时、四agent对照，多个任务/backbone成本高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Cost-Efficient Privacy Enforcement for Email-Generating LLM Agents under Strategic Information Requests](https://arxiv.org/html/2610.18007v1) · 2026-10-13 · P1

    本法需真实Gemma contract-conditioned重写再由PrivacyChecker检查；只保证remote-token节省，不代表total compute降低。已查defender objective/§5.1，local overhead换算和完整多策略email闭环成本仍材料性不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Learning How to Remember: Memory Modality Selection for GUI Agents](https://arxiv.org/html/2610.17928v1) · 2026-10-13 · P1

    SwitchMem 对同一retrieved demonstration实际比较text/image并学习step-level router；必须保留真实VLM hidden-state probe/两种memory。9B actor、三GUI基准、配对标注/训练和后续closed-loop预算仍高/不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Interaction-as-a-Judge](https://arxiv.org/html/2610.17895v2) · 2026-10-13 · P1

    Interaction-as-a-Judge 用真实电脑交互评估和修复应用，训练奖励还需交互轨迹。v2附录G为Qwen3.5-9B、384prompts×8采样=3072轨迹/batch；完整推理与RL链路成本过高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [ECMR: Evidence-Aware Deliberation Control for Multi-Agent LLM Reasoning](https://arxiv.org/html/2610.17869v1) · 2026-10-13 · P1

    ECMR 的state-conditioned controller需要真实支持独立性/矛盾/验证/role-action闭环；9000 held-out records和多策略、多domain完整成本高且总资源口径仍不确定。不能只回放gold state或把normalized audit cost当美元/运行时间。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [State-Aware Generation of Deployable Websites from Visual Prototypes and Requirements](https://arxiv.org/html/2610.17861v1) · 2026-10-13 · P1

    VisStateCoder 需真实prototype grounding、图指导生成、render evidence和限域更新，不是静态Project State Graph。官方HTML§4.4五模型、每call最高16384输出、最多4round；baseline每task7200秒，完整网站生成/部署矩阵预算不确定且重。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Socratic Skill Learning: Interleaving Teaching and Practice for Transferable Agent Skills](https://arxiv.org/html/2610.17860v1) · 2026-10-13 · P1

    SSL 要实际Educator/Student交错教练、唯一Student操作环境并验证可迁移skill。35families/408cases、主22family/155case、66run/schedule及多模型pair，完整技能获取预算高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Agentic-MatriBO: Capability-Compiled Agentic Bayesian Optimization for Materials and Chemical Design](https://arxiv.org/html/2610.17832v1) · 2026-10-13 · P1

    Agentic-MatriBO 保留capability compiler、证据gate与提交后才可查oracle的边界；不是提前扫描全pool金标。四candidate pools×五seed×多baseline/agent调用，完整执行预算与依赖仍无法廉价核定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Agentic4PDM: Host-Governed Evidence Admissibility for Industrial Fault Diagnosis](https://arxiv.org/html/2610.17786v1) · 2026-10-13 · P1

    Agentic4PDM 的host治理不等于无需检索/推理。正文附录F显示按样本的复杂调查与DTW基线超过千秒，原系统还需要预训练表征、类别参考和真实工业数据；完整成本无法廉价界定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Beyond Belief Nesting: Rethinking Higher-Order Theory of Mind in Large Language Models](https://arxiv.org/html/2610.17777v1) · 2026-10-13 · P1

    HopTrace 一次编码透视记录并确定性回答多层ToM问题，不能用gold belief graph替代编码器。原完整比较100 narrative/500主问题、其他基准与多模型，报告4–217秒/story且开放大模型4×A800；本轮不能廉价界定忠实完整配置成本。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Coupled Harness--Model Evolution for Scientific Equation Discovery](https://arxiv.org/html/2610.17740v1) · 2026-10-13 · P1

    Coupled Harness–Model Evolution 同时演化可执行工具并用GPT-5.5成功轨迹对Qwen controller做LoRA，不是只有工具库注册。完整工具搜索、教师轨迹和学生训练成本经现有配置仍材料性不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [SkillScreen: High-Recall Screening of Malicious Agent Skills with Decision Models](https://arxiv.org/html/2610.17727v2) · 2026-10-13 · P1

    SkillScreen 用2B决策模型的NLI分数筛查技能，以验证集冻结99%召回阈值；必须保留陌生良性来源FPR升高与仅扫描SKILL.md的限制。v2明确每次单epoch仍需3.4–3.9小时（10GB H100 MIG），还有多划分/多种子；成本过高不复现、审查 DONE，不能因显存小就当便宜。

- [Evidence-First Agentic Verification](https://arxiv.org/html/2610.17724v1) · 2026-10-13 · P1

    Sauron 的bounded queries/faithfulness checks减少相对成本，但不是便宜全评测。原文100episodes单Sol配置\$297.69，TRAIL为\$841；仍有多backbone/故障注入/消融，完整复现过高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Adaptive-Group Process Rewards for GUI Agents](https://arxiv.org/html/2610.17710v1) · 2026-10-13 · P1

    Adaptive-Group process reward需要VLM按动作和subgoal group评估，再用GRPO真实训练GUI agent。两process reward基准和OSWorld三个application组，完整reward scoring/rollout/训练成本仍材料性不确定。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [RALI@iKAT 2026: Retrieval-aware User Profile Denoising via Personalized Conversational Dense Retrieval](https://arxiv.org/html/2610.17673v1) · 2026-10-13 · P1

    PCDR 需先训练会话retriever，再联合投影用户profile。原文基础conv-Qwen3使用四GPU、batch480、20epochs和跨GPU negatives；不能只用固定embedding替代denoising学习。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Cowork-Gym: Synthesizing Interactive Work Environments at Scale](https://arxiv.org/html/2610.17670v1) · 2026-10-13 · P1

    Cowork-Gym 的build-execute-revise环境构造和SFT/RL/OPD是中心。64.9K环境、14场景、9B/27B/35B-A3B训练规模明显超预算，不以少数合成环境fixture代替训练。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [Executable Prefix Values for Locating Agent Failures](https://arxiv.org/html/2610.17633v1) · 2026-10-13 · P1

    Executable Prefix Values 需要重建中间repo状态并多次真实续跑来估计V(h_t)，不是给judge标签重打分。150 SWE任务、47/60条失败曲线与多种restart schedule需要大量continuations，完整成本过高。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [MAS-Gate: Unlocking Multi-Agent System Lifecycle via Node-Centric Quantification](https://arxiv.org/pdf/2610.17613v1) · 2026-10-13 · P1

    MAS-Gate 用reference-answer likelihood变化提供训练utility、paired轨迹训练Editor；金标只可留在训练/评分侧。官方PDF p18是8×H100、batch256、group16、15Kprompt/8192response，完整训练过高，不能把gold量化fixture推广为inference算子。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

- [EdgeWise: Bringing Long-Horizon Agents to the Edge via Selective Cloud Delegation](https://arxiv.org/html/2610.17560v1) · 2026-10-13 · P1

    EdgeWise 的核心是joint solving/delegation step-level RL，而不只是路由标签。9B本地模型、frontier云模型、80turn长任务和RL采样/对照总成本仍明显不确定，不以62%相对省钱当完整复现便宜。 成本过高，不复现（审查 DONE）；不进入自动重试、实现或evolve。

</details>

## 旧文补发现、已知修订版与官方身份：13 项

这些不是本窗口新首发；只关闭当前记录的复现成本决定，旧实现证据不自动升级。

- [Google Earth AI Geospatial Reasoning Agent: Capabilities and a Systematic Evaluation](https://research.google/pubs/google-earth-ai-geospatial-reasoning-agent-capabilities-and-a-systematic-evaluation/) · 2026-10-11 · P1

    Gemini 驱动模块化地理技能与前置规划；官方公开两个 benchmark 的 development splits。arXiv 首发 2026-10-11，目录/博客更新不是新首发。完整 Gemini/地理工具评测成本未能廉价核定，按预算门槛不复现，审查 DONE。

- [DRanker: A Transformer-Based Multi-Task Ranking Model for the Disney+ Homepage](https://arxiv.org/html/2610.15696v1) · 2026-10-11 · P0

    DRanker 的约 7M 参数 encoder-only 多任务排序器结合因果去偏，正文有线上 A/B 与全局上线结果；不是只有摘要宣称部署。训练依赖数月 Disney 私有交互与数亿训练样本，无法在公开数据和单卡预算下忠实核验生产设置；不复现、审查 DONE。首发 arXiv 2026-10-11，属旧文补发现，不是本窗口新首发。

- [Vela: User Behavior as Supervision Sparks LLM Intelligence](https://arxiv.org/html/2610.14709v1) · 2026-10-10 · P1

    Vela 把长期用户行为变为任务与轨迹；属于 LLM 数据/训练方案而非已证实的工业业务线上 A/B。35B-A3B、131072 长度、75K 轨迹，两 epoch；附录 RL 使用 48 GPUs（32 训练/16 rollout）。成本过高，不复现、审查 DONE。

- [Do LLMs Learn from Rewards in Context? : Rethinking the role of reward in In-Context RL](https://arxiv.org/html/2610.11152v3) · 2026-10-08 · P1

    v3用奖励翻转/随机/移除及轨迹打乱等对照，发现直接ICRL收益多由ICL上下文驱动；不能把论文结论推广到所有推理时RL。原文Computational Cost实报单A100上ScienceWorld十episode约5h、代码约3h，整套多模型对照成本高，不复现、审查 DONE。

- [Self-Retrospection Distillation: Turning Post-hoc Experiences into Prior Foresight](https://arxiv.org/html/2610.08077v3) · 2026-10-06 · P1

    SRD v3用事后经验监督行动前不可见轨迹的foresight，推理无需生成foresight；训练时可用hindsight不等于评测agent可读未来。Appendix C.2为4B/9B thinking-on、8 H200、每步128轨迹及十种agent任务，成本高，不复现、审查 DONE。

- [Imagine the Future, Internalize the Gist: Efficient VLA Reasoning via Internalized Spatiotemporal Imagination](https://arxiv.org/html/2610.02626v3) · 2026-10-02 · P1

    IG-VLA v3先学习未来SigLIP状态，再将时空reasoning内化为gist；不是仅重复当前帧。§4.1原文训练reasoning用8 H100、gist用4 A6000，LIBERO 100K步和VLABench61K步。成本高，不复现、审查 DONE，单卡推理延迟结果不替代训练验收。

- [Token Utility for On-Policy Distillation via Local Trust-Region Optimization](https://arxiv.org/html/2610.18883v1) · 2026-10-01 · P1

    FUW/Token Utility 用 Fisher 几何的 token utility 调整蒸馏权重；1.7B/4B学生、8B/14B/30B教师，279步×256序列×8192上下文，成本过高不复现、审查 DONE。arXiv首发2026-10-01，必须记旧文补漏而非10月14日新首发。

- [The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation](https://arxiv.org/html/2609.36484v2) · 2026-09-29 · P1

    RIDE v2逐层使用RL教师相对base的hidden-state残差构造外推回归目标，需额外冻结base前向；不将output-space概率外推等同hidden-space方法。当前版本方法与配置已核，整套teacher/base/student长rollout和多任务总成本无法廉价核定，不重训、审查 DONE。旧L1实现/回执保留，不因版本元数据变动宣布新版能力完成。

- [Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL](https://arxiv.org/html/2608.11669v2) · 2026-08-12 · P1

    Rubric Dropout v2仍要求同prompt同step共享mask；还讨论相似criteria按block联合drop，至少保留三criteria及full-rubric评测。独立gold judge不是绝对真值，多数配置单run。1.7B–8B、16rollouts、600steps及双API judge完整多臂成本高，不复现、审查 DONE；不宣称旧adapter已覆盖v2 block方案。

- [SPARK: Learning from Verification in Speculative GRPO Rollouts](https://arxiv.org/html/2608.04962v2) · 2026-08-05 · P1

    v2由SpecRoll改为SPARK：同prompt group共享并每rollout清零的低秩logit correction，以top-16+tail的verifier反馈更新、跨rollout学习投影，原target verifier保持不变。与旧fast/slow SpecRoll不是仅名称变化；本地旧实现不算SPARK。21模型数据设置+GRPO训练全套成本高，不复现、审查 DONE；旧论文页已加版本警示。

- [UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute](https://arxiv.org/html/2604.12234v5) · 2026-04-14 · P0

    UniRec v5已明确Shopee机构，含capacity-constrained SID、CoA、CDC以及RFT+DPO；§4.2生产A/B的PVCTR/订单/GMV证据通过，不能把离线token-hit和业务收益混写。训练依赖9天数十亿私有交互和三场景，忠实新版全套不复现、审查 DONE；旧CoA本地实验不自动升级为v5全方案。

- [AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics](https://github.com/facebookresearch/autoformbench/blob/main/paper.pdf) · 首发日未确认 · P1

    身份已确认是 Meta 的 Lean 数学 AutoformBench，不是 2603.29832 文档理解同名作。官方页 2026-10-13，论文首页文稿日期 2026-10-05，软件 CITATION 日期 2026-09-30，语义不同，不能合成已证实的首次公开日。341 题×9 frontier 模型、长轨迹/最高每题 \$200 上限（不是实际统一花费）超出本轮预算，不复现、审查 DONE；保留低成本结果导入价值，不声称已接入。

- [CATWILD: Compiler Autotuning For TPU workloads in the Wild](https://research.google/pubs/catwild-compiler-autotuning-for-tpu-workloads-in-the-wild/) · 首发日未确认 · P1

    官方页可确认 CATWILD 的 TPU fleet 编译器 autotuning 与五年生产运行，但只列 2026 年，无可下载原文/精确首发日期；只读官方页和精确标题检索后仍不能确认固定窗口。原系统依赖 TPU fleet，单卡 A100/A30 不具备，成本过高不复现；日期例外归档，不计 accepted。

## 评测参考、边界与来源例外：3 项

<details markdown="1"><summary>展开其余 P0/P1 决定（均非本轮能力实现）</summary>

- [Hide and Seek: HIDE Concepts to SEEK explanations for black box models](https://arxiv.org/html/2610.13935v3) · 2026-10-09 · P1

    已读v3摘要、定义方法/评测及Appendix A成本分解：VLM检索concept真实图像、定位遮挡后查询黑盒输出差；查询成本随每概念图像数变化，encoder可复用不等于全流程免费。只完成当前版本审查，不虚构与缺失旧基线的逐项语义diff，不升级实现。

- [NOMOS: Compiling Written Policies into Statically Verified Tool-Call Gates for LLM Agents](https://arxiv.org/html/2610.11030v2) · 2026-10-08 · P1

    NOMOS v2以四阶段编译器生成静态可验证的工具调用gate，并与宽松、policy prompt、动态LLM gate对照；不把schema checker冒称完整policy编译器。正文明确banking benign utility被用于policy修订，不是held-out utility；原稿长agent/26B/70B judge全套不在本轮执行。只做修订审查，无新版能力验收。

- [The Dice Roll Method: A Standardized Protocol for Repeated-Query Auditing of Large Language Model Brand Recommendations](https://arxiv.org/html/2609.04047v2) · 2026-09-03 · P1

    Dice Roll v2明确撤回v1由notebook合成数据覆盖和“Research”计数字段产生的固定次数tiers及若干不可复算表；改为先pilot再依方差分量求次数，不能继续引用固定5/10/15次建议。仓库没有该算法实现，保留旧审查快照并新增本勘误，不把旧接受判断当新版验证。

</details>

全量 P2 / 范围外 / 历史日期分流见领域 JSON 与 [完整登记](paper-register.json)，不再堆入默认阅读页。
