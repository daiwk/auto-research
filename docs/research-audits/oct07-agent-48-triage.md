# 上轮 48 条 Agent 召回：逐条初筛（2026-10-07）

这不是 48 篇已实现，也不是 48 篇全文审核完成。48 条来自上轮**请求窗口 10-02～10-06**；扫描额外包含 10-01 重叠日，合计 117 条窗口内未审标题。旧报告把两种窗口放在相邻位置容易误读；原始记录并未丢失。

本表逐条阅读标题和摘要；“全文”只用于确实阅读了方法的条目。“待全文”保持候选状态，不计作终结性拒绝或已实现。

| 论文 | 核查层级 | 本轮处理 | 理由/仍缺的证据 |
|---|---|---|---|
| [2610.03675 · FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution](https://arxiv.org/abs/2610.03675) | 全文+代码 | 本轮实现 | 强弱模型程序进化；真实 GPU 实验及负结果随详情页登记 |
| [2610.03631 · NeutronGym: Physics-Graded Neutron Instrument Design for LLM Agents](https://arxiv.org/abs/2610.03631) | 摘要 | 环境候选 | 依赖 McStas 物理仿真和隐藏科学 verifier；未接入 |
| [2610.03620 · UniIntervene++: An Adaptive Intervention Agent for Efficient Real-World Reinforcement Learning](https://arxiv.org/abs/2610.03620) | 摘要 | 环境候选 | 真实机器人干预与 options；需物理或匹配模拟器验证 |
| [2610.03604 · Mastering Atari 2600 Games with Discovered Options](https://arxiv.org/abs/2610.03604) | 摘要 | 范围外 | Atari 深度 RL options，不是本批 LLM/工具 Agent 算法 |
| [2610.03598 · When a Correct Reward Is Not Enough: Diagnosing and Guiding PPO in an Analytically Solved Broker-Trader Game](https://arxiv.org/abs/2610.03598) | 摘要 | 范围外 | 金融控制 PPO 诊断，不是本批 LLM 后训练 |
| [2610.03591 · HazardWeaver: Scientific Route Selection for Hazard Analysis Agents](https://arxiv.org/abs/2610.03591) | 摘要+作者链接 | 待全文 | HazardWeaver 有代码，需领域数据、科学工具和多路线 verifier |
| [2610.03585 · Threat-Preserving Representation Sensitivity in Agent-Security Benchmarks](https://arxiv.org/abs/2610.03585) | 摘要 | 评测线索 | 安全表述敏感性实验，不是可直接登记的新策略算法 |
| [2610.03574 · HyperBrowseComp: A Multilingual and Multimodal Stress Test for Web-Browsing Agents](https://arxiv.org/abs/2610.03574) | 摘要 | 评测候选 | 多语多模态浏览；需真实检索、媒体工具与授权 API 预算 |
| [2610.03525 · Structured Composition of Verifiable Atomic Insights for Table-to-Report Generation](https://arxiv.org/abs/2610.03525) | 摘要 | 待全文 | ComInsight 的 SQL 原子证据与组合算子值得审查 |
| [2610.03524 · From Benchmarks to Production: A Text-to-SQL System for Complex Financial Data](https://arxiv.org/abs/2610.03524) | 摘要 | 待全文 | 金融 SQL 专用 schema/参考库；生产声明不等于工业搜广推 A/B |
| [2610.03476 · MobiAgent: Dual-Loop Recursive Policy Self-Improvement for Long-Horizon Mobile Manipulation](https://arxiv.org/abs/2610.03476) | 摘要 | 环境候选 | MobiAgent 需 flow-matching 技能、机器人 rollout 与 RoboCasa/BEHAVIOR 环境 |
| [2610.03448 · Passing the Test You Trained On: Re-evaluating Prompt-Injection Detectors for LLM Agents](https://arxiv.org/abs/2610.03448) | 摘要 | 评测线索 | 提示注入检测的分布迁移复核；不能当新 Agent 能力实现 |
| [2610.03356 · ReFract: Benchmarking Perspective Awareness in Language Model Agents with Text World Models](https://arxiv.org/abs/2610.03356) | 摘要 | 评测候选 | ReFract 角色权限基准；需核对公开任务与文本世界环境 |
| [2610.03315 · Lightweight, Rubric-Guided Trajectory Evaluation for Production AI Agents](https://arxiv.org/abs/2610.03315) | 摘要 | 待全文 | LiteTrajEval 的压缩预算与 rubric judge；需核对标注数据 |
| [2610.03226 · D2K-Bench: Can LLM Agents Turn Expert Designs into Efficient GPU Kernels?](https://arxiv.org/abs/2610.03226) | 摘要 | 评测候选 | D2K-Bench GPU kernel 设计评测；原环境 B200，需硬件适配而非虚报同口径 |
| [2610.03213 · Toward SLM-based agentic task-tool intent matching](https://arxiv.org/abs/2610.03213) | 摘要 | 待全文 | SLM 任务-工具意图匹配；需数据和训练协议 |
| [2610.03195 · Source Preference in the Wild: How LLM Agents Favor Items by Source, and How to Reduce It](https://arxiv.org/abs/2610.03195) | 摘要 | 分析线索 | 来源偏好和去偏实验，暂不登记独立策略 |
| [2610.03153 · EvoRiskBench: An Evolving Benchmark for Runtime Security Risks in Workspace Agents](https://arxiv.org/abs/2610.03153) | 摘要 | 等待公开产物 | 摘要明确安全与复现检查后才发布 benchmark/平台 |
| [2610.03136 · Investigating the Role of Reasoning-Language Alignment in Monolingual Retrieval-Augmented Generation](https://arxiv.org/abs/2610.03136) | 摘要 | 评测线索 | 德语 RAG 推理语言消融，非新核心结构 |
| [2610.03102 · Ask, Relax, or Act? Evaluating Actionable Indeterminacy in LLM Preference Reasoning](https://arxiv.org/abs/2610.03102) | 摘要 | 评测候选 | solver-grounded 行动/澄清/约束修复，需要可信求解器 |
| [2610.03099 · Beyond Single Videos: Benchmarking and Active Evidence Seeking for E-Commerce Cross-Video Reasoning](https://arxiv.org/abs/2610.03099) | 摘要 | 待全文 | AdSeek 主动多视频证据获取与 RL-SFT-RL，归多模态候选 |
| [2610.03089 · Securing Computer-Use Agents Against Branch Steering Attacks](https://arxiv.org/abs/2610.03089) | 摘要 | 待全文 | COBRA 可信分支+能力约束；需要真实浏览器与 STEER-Bench |
| [2610.03056 · MOF-VERIFY: A Failure-Aware Agentic Harness for MOF Hypothesis Verification](https://arxiv.org/abs/2610.03056) | 摘要+作者链接 | 环境候选 | MOF 结构/文献/MLIP 科学验证，领域工具尚未接入 |
| [2610.03055 · hacktrace: behavior-supervised detection of reward hacking during code generation](https://arxiv.org/abs/2610.03055) | 摘要 | 待全文 | HACKTRACE 内部状态监督监测；需真实轨迹、隐藏状态与作弊标签 |
| [2610.03036 · WebFovea: When the Model Is Right but the Click Is Wrong -- Reliable Round Trips for Vision-Based Web Agents on Live Websites](https://arxiv.org/abs/2610.03036) | 摘要 | 环境候选 | WebFovea 浏览器执行接口修复，需真实网页回放验证 |
| [2610.03033 · When Numbers Start Talking: Numerical Signalling and Strategic Behaviour Among LLMs](https://arxiv.org/abs/2610.03033) | 摘要 | 分析线索 | 多 Agent 数字信号博弈，非本批训练算法 |
| [2610.03020 · DyadMem: A Long-Term Memory Benchmark of How Agents Work with Users](https://arxiv.org/abs/2610.03020) | 摘要 | 评测候选 | DyadMem 的记忆捕获/更新/召回分解；需公开数据及全流水线 |
| [2610.03014 · Beyond Predefined Sinks: Security-Aware Dependency Analysis for LLM Agents](https://arxiv.org/abs/2610.03014) | 摘要 | 待全文 | AgentSecGraph 静态依赖与安全上下文，需真实源码分析验证 |
| [2610.03010 · Engineering Sustainable Agents: A Systematic Comparison of Agentic LLMs for Developer Workflows](https://arxiv.org/abs/2610.03010) | 摘要 | 分析线索 | 不同 Agent 配置的能耗/准确率测量，不是新算法 |
| [2610.02994 · Sentry: Learning to Recover from LLM Agent Failures at Test Time](https://arxiv.org/abs/2610.02994) | 全文+仓库 | 本轮实现 | 失败条件检索与 reward-blind 恢复验证；作者源码未发布，采用独立实现 |
| [2610.02970 · A Guideline-Augmented Multi-Agent Framework for Schema-as-Code Biomedical Named Entity Recognition](https://arxiv.org/abs/2610.02970) | 摘要 | 待全文 | GAMA biomedical NER 规则记忆与代码 schema；不能用通用 mini-suite 替代 |
| [2610.02952 · GTDD: Generative Test-Driven Development for AI Coding Agents with Adversarial Testing](https://arxiv.org/abs/2610.02952) | 摘要 | 待全文 | GTDD 自适应测试与独立验收；需要生成器、可信 oracle 和新鲜审计样本 |
| [2610.02951 · Dynamic Expert Pruning for Multi-Agent Systems](https://arxiv.org/abs/2610.02951) | 全文 | 待实现 | 需要真实 MoE 专家路由、预测器训练和 delta-loading，不能用 dense 模型掩码替代 |
| [2610.02928 · Discriminating Fixture Coverage in Agent-Infrastructure Verification Suites](https://arxiv.org/abs/2610.02928) | 摘要 | 工程线索 | mutation testing 区分输入未激活与 oracle 不可观测；不当作论文能力实现 |
| [2610.02925 · Positive-Unlabeled Learning for Agent Safety False Alarm Auditing](https://arxiv.org/abs/2610.02925) | 摘要 | 待全文 | 安全误报警 PU 排序，需真实安全参考/报警池，不访问报警金标训练 |
| [2610.02885 · PsyEvo: A Personalized Counseling Agent That Self-Evolves at Test Time](https://arxiv.org/abs/2610.02885) | 摘要+作者链接 | 环境候选 | PsyEvo 心理咨询模拟和偏好更新，涉及专用评测，不把模拟收益当临床效果 |
| [2610.02847 · Turnover-Orthogonal Credit Assignment for Open-Team Multi-Agent Reinforcement Learning](https://arxiv.org/abs/2610.02847) | 摘要 | 范围外 | 开放团队 MARL 人口变动信用，非本批语言模型方法 |
| [2610.02814 · VeriPy Source-Preserving Verification and Compatibility Checking for Python Components](https://arxiv.org/abs/2610.02814) | 摘要+作者链接 | 工程线索 | VeriPy Dafny/Lean 形式验证；未接入 verifier 工具链 |
| [2610.02744 · EpiWorld: Grounding LLM Policy Agents in Epidemiological World Models](https://arxiv.org/abs/2610.02744) | 摘要 | 环境候选 | EpiWorld 流行病世界模型与干预，需领域数据和仿真器 |
| [2610.02740 · Prospective Hindsight: Self-Calibrating Reinforcement Learning via Prediction-Reality Gaps](https://arxiv.org/abs/2610.02740) | 摘要 | 待全文 | Prospective Hindsight 预测-结果差异加权，需核对梯度与训练配方 |
| [2610.02710 · Self-Supervised Scaling of Terminal Environments for Scientific Domains](https://arxiv.org/abs/2610.02710) | 摘要 | 待全文 | 科学终端环境重建与隐藏 verifier；需 500 workflows 和真实执行环境 |
| [2610.02702 · Silent Dissent: LLM Agents That Yield to the Majority Still Represent Their Original Premise](https://arxiv.org/abs/2610.02702) | 摘要 | 分析线索 | J-lens 观察从众后的潜在表征，不能直接标成自改进策略 |
| [2610.02687 · Decoupling Memory from Context: Structured Memory for Token-Efficient Test-Time Continual Learning](https://arxiv.org/abs/2610.02687) | 摘要 | 待全文 | GraphMemory 查询子图检索与记忆更新，需核对更新/合并规则 |
| [2610.02670 · LEAP: Learning Efficient Action Proposals For LLM Agents](https://arxiv.org/abs/2610.02670) | 摘要 | 待全文 | LEAP 小模型动作序列蒸馏与目标验证，需真实延迟和成功率对照 |
| [2610.02654 · Coherence-Driven Belief Formation and Population Dynamics of Contagion in LLM Agents](https://arxiv.org/abs/2610.02654) | 摘要 | 分析线索 | 社会信念传播实验，不是新通用 Agent 算子 |
| [2610.02638 · Batched Speech Decisions Without Decoding: Single-Token Supervision Lets a Frozen LLM Hear Beyond the Transcript](https://arxiv.org/abs/2610.02638) | 摘要 | 待全文 | DuplexJev ASR 隐状态连接器与单 token 决策；归 System-1/多模态候选 |
| [2610.02617 · WebUIProof: Benchmarking WebUI Code Generators with UI-Agent Execution Harness](https://arxiv.org/abs/2610.02617) | 摘要 | 评测候选 | WebUIProof 真实浏览器执行测试与 RL；未启用真实 UI 训练环境 |
| [2610.02616 · VERSE: Verified Self-Evolving Optimizer for Agent Harnesses](https://arxiv.org/abs/2610.02616) | 摘要+作者链接 | 待全文 | VERSE 验证驱动的双层 harness 自进化；需隔离代码执行和 SWE 任务 |

