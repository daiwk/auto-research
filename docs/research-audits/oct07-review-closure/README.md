# 2026-10-01～10-07 审查收口

本批复核日期为 2026-10-10，发表窗口仍固定在 10 月 1～7 日。

逐篇结论保留核心方法、正文位置和公开复现边界。接受项尚未在本批实现；
宽查询命中、摘要初筛、正文审查和实现分别记录。

去重共 **1022** 篇；拒绝／范围外 367；接受，待实现 494；审后延期 113；已有记录 48。

全来源完整审查水位仍为 **2026-10-02**。官方目录覆盖证据见
[来源回执](official-sources.json)，完整机器可读清单见[逐篇登记](paper-register.json)。

## 分领域召回

| 领域 | 日期窗口召回 | 月份编号补查 |
|---|---:|---:|
| recommendation | 35 | 39 |
| foundation-model | 411 | 459 |
| post-training | 177 | 201 |
| agent | 396 | 437 |

两通道存在重叠，上表数字不能相加。月份编号补查独立运行，可召回晚入索引记录。
八份召回回执均显示配置内查询取尽，失败查询和触顶查询均为 0；这只证明本轮查询矩阵的 API 召回，
不证明未命中查询的论文或官方来源已穷尽。接受项均已核查正文；范围外条目可在摘要确定研究范围后终止。

## 接受，待实现（494）

**2610.08791 · World Models' Last Exam in Physics**

[论文](https://arxiv.org/abs/2610.08791)

- **foundation-model**：40项物理关系测量任务覆盖九类现象，官方公开任务图像/提示/评估器及外部视频批评估入口，可纳入evolve公共评测候选；不是新世界模型算法，也不是已接入。
  复现边界：官方网页404但GitHub可访问。已确认论文与代码差异：论文门失败仍尝试物理测量，公开runtime gate失败直接return/physics_attempted=False；接入须保留原论文测量协议并分别报告coverage，不可把现有脚本直接宣称保真实现。难度标签基于被评模型均分事后划分；human一致性仅约53%，不是物理真值oracle。
  核查位置：§2.1–2.4/Eq1–7；§3.1–3.3/Table2；official README；docs/evaluation.md；easy/P21/evaluator/_shared/unified_evaluators/runtime.py:339–355；evaluate.py:summarize

**2610.08779 · ALIVE: Interaction-Aligned Object Insertion for First-Frame-Guided Video Editing**

[论文](https://arxiv.org/abs/2610.08779)

- **foundation-model**：ALIVE以source+noisy target通道拼接、干净首帧和按时间overlap/描述长度归一的cross-attention；Qwen VLM从同输入预测P4而不是读target。35,800对训练与两benchmark；部分基线额外P2提示不完全同条件。
  核查位置：§3；§4.2式2–4、§4.3式5；§5.1

**2610.08778 · Sherpa: Teaching LLMs to Teach Adaptively**

[论文](https://arxiv.org/abs/2610.08778)

- **post-training**：逐回合gate掩码return并按到达同回合的轨迹leave-one-out归一，训练teacher适应学生偏好；有MATH分离训练/评测及教学benchmark。

**2610.08775 · Agent in a Bottle: Can LLM Agents Turn Their Capabilities Into Cheap, Scalable Artifacts?**

[论文](https://arxiv.org/abs/2610.08775)

- **agent**：BOTTLED作为evolve可执行评测基础设施接受：Agent在预算内生成可复用artifact并完成大批无标签任务，明确隐藏gold与预算约束，兼容模型/脚本/路由器候选。
  复现边界：原实验每模型每任务两runs，零样本只抽1000；GPU成本未统一入token预算；MIT代码，MAVE CC-BY-NC4.0/ESCI Apache2.0/RAID MIT；contamination judge及Jev评测未公开，不能宣称完整污染审计复现。
  核查位置：§3.1–3.5 Eq1–6；§4.1；Ethics/Reproducibility；官方README与src/bottled/datasets/esci.py

**2610.08773 · AdvSim2Real : Training Web Agents Against Adaptive Prompt Injection in a Web World Model**

[论文](https://arxiv.org/abs/2610.08773)

- **post-training**：冻结world model与judge，分阶段课程—执行者、对手—执行者训练；三seed rollout与150任务对照，不等于真实生产A/B。
- **agent**：AdvSim2Real的三策略/两阶段训练有明确算法：课程以p≈0.5任务奖励，adversary仅获clean-success到failure flip奖励，executor fresh-rollout训练且重用历史attack inputs；可作为Agent RL核心候选。
  复现边界：攻击结果只world-model+LLM judge；Stage2未在真实浏览器测试，不能声称可执行安全；150自建form任务，3 rollout seeds非3训练seeds；攻击后可行性未经核验；去Stage1实验不compute matched，鲁棒性收益仅0.44pp。
  核查位置：§3 Environment/Threat Model/Metrics；§4 Algorithm1/Eq2–5；§5 Tables1–3；§6 Limitations

**2610.08718 · When Forgetting is not Catastrophic: On the Mechanics of Spurious Forgetting**

[论文](https://arxiv.org/abs/2610.08718)

- **foundation-model**：新事实微调造成共享表征偏移与逐事实侵蚀分离；对更新矩阵删首奇异分量的干预在OLMo2-1B有同范数随机rank1对照，可登记机制诊断候选，不能宣传为通用抗遗忘能力算法。
  复现边界：人为新旧答案首token不重叠，单预训练模型；诊断logit均值来自已知oldfact不能在线oracle使用。只采用权重干预时须独立validation选checkpoint和rank。
  核查位置：§4.1–4.4；§5.1–5.2/Figure5；§6/Limitations；Appendix D.2

**2610.08713 · SpaTime: Streaming Vision-Language Models for Spatio-temporal Reasoning**

[论文](https://arxiv.org/abs/2610.08713)

- **foundation-model**：SpaTime冻结因果几何/视觉编码器，2×2 merge投影相加，训练LoRA/state/head并建模首个Response分布作时间损失；strict只计最早回答，charitable末帧强制回答须分开。StreamVSTI训练、StreamVSI任务OOD。
  核查位置：§4.1式5；§4.2式6–8；§5；§6

**2610.08691 · ScienceClaw: Benchmarking Continual Self-Evolution of AI-for-Science Agents Across the Natural and Social Sciences**

[论文](https://arxiv.org/abs/2610.08691)

- **agent**：ScienceClaw冻结模型，以typed workflow执行修复提取linked Skill–Operator bundles，boundary/source reset replay必须实际使用新版本，只有独立validation严格提升且hard constraints/预算通过才原子晋级；符合真实evolve闭环候选。
  复现边界：主要final snapshots，作者§8承认广泛结论需重复runs和学科intervals；domain evaluator可能漏科学错误；需实际科学工具/独立verifier，不能固定轨迹fixture作为能力复现。
  核查位置：§3 Eq1–3；§4.1–4.2；§5.1–5.2 Eq5–13；§6 Tables1–2/Fig6；§8

**2610.08678 · Secure Speculative Decoding for Large Language Models**

[论文](https://arxiv.org/abs/2610.08678)

- **foundation-model**：SecureSD 按全局生成位置混合标准/宽松接受与拒绝恢复分布，早期严格验证，后续恢复快速验证；定义完整，可作为真实投机解码候选。
  复现边界：不是对任意攻击的安全保证；需目标/草稿模型、lossless/relaxed/corrected 三臂同参数对照，并把任务质量和真实延迟分开报告。原文主要 Blackwell 实测，不代表 A100 已验证。
  核查位置：§IV-B；§V Algorithm 2 / Eq7–14；§VII-A paired protocol；§VIII Tables XII–XIII

**2610.08674 · EC-RAG: Event Chain Retrieval-Augmented Generation for Long Video Understanding**

[论文](https://arxiv.org/abs/2610.08674)

- **foundation-model**：EC-RAG训练外query模态拆解、CLIP variance取帧、ASR/OCR/DET事件描述与按时间相邻链，Contriever相关事件/邻接上下文辅助回答；三长视频benchmark，不是学习因果事件图，额外工具/token预算须计。
  核查位置：§3.1–3.4式12–16；§4.1–4.2

**2610.08670 · Principled Under Pressure: Post-Training Decides Whether LLMs Act on Their Own Moral Judgment**

[论文](https://arxiv.org/abs/2610.08670)

- **post-training**：公共评测：判断—行动差距的筛选、四级测量校准与压力对照独立于训练算法；Apache-2.0 DeepSteer仓库可访问。仅74/208主情境通过screen，报告条件分布不能外推总体。
- **agent**：公共评测：判断—行动差距的筛选、四级测量校准与压力对照独立于训练算法；Apache-2.0 DeepSteer仓库可访问。仅74/208主情境通过screen，报告条件分布不能外推总体。
  核查位置：§3.1–3.5；Appendix F；作者仓库README/文件列表已只读核查

**2610.08662 · ParanoiaEval: Benchmarking Unnecessary Defensive Work in Agentic Coding**

[论文](https://arxiv.org/abs/2610.08662)

- **agent**：ParanoiaEval作为evolve行为约束评测接受：200同任务E+/E−证据对，任务oracle和多余风险处置judge分离，可同时评测完成度与证据响应。
  复现边界：公开包无结果/完整轨迹；answer cards/reference补丁只能独立scorer访问；模型native harness混杂不能声称模型净能力差异；developer study限成功runs且非部署A/B；默认same-task=none，不能打开other-arm泄漏gold。
  核查位置：§4.1–4.3；§5；§7 Code/Data；官方README、scripts/judge.py

**2610.08659 · Selective Transfer of RL Updates for Visual Reasoning**

[论文](https://arxiv.org/abs/2610.08659)

- **foundation-model**：Selective-RL隔离R−B与B−V，逐矩阵rank1 SVD后恢复原Frobenius norm，分别重构donor插值和直接加RLdelta；3个8B VLM骨干，源验证选donor，H1验证选λ后冻结，需保留非视觉模块支持对齐。
  核查位置：§3.1–3.3式1–3；§4.1；Appendix A Algorithm 1

**2610.08649 · Stable Scores, Unstable Answers: Frame Phase and Option Order in Video Multiple-Choice Evaluation**

[论文](https://arxiv.org/abs/2610.08649)

- **foundation-model**：PhaseFusion把3×8帧相位后验映射到内容空间作算术平均，独立于option排序控制；n442与32帧准确率差0.45pp不显著，origin flip率下降但order flip未解决；串行3.18s高于24帧2.86s，不能用attention单位冒充实测提速。
  核查位置：§3.2式2；§4 Table 1；§4.3

**2610.08647 · SquidAgent: Parallelize Wisely, Coordinate Efficiently**

[论文](https://arxiv.org/abs/2610.08647)

- **agent**：SquidAgent一次DAG规划同时估算输出token/层对齐成本，session fork继承上下文、预写约定，以sum(tokens)/(max(tokens)+alignment)>alpha决定并行；明确可执行Agent调度机制。
  复现边界：主要自建九任务、LLM rubric；token代理适用于生成主导场景不捕获tool/API时延；alpha1.9基于MathRef sweep设置，独立validation选择未建立；本地复现需真实LLM调用/成本不能fixture代替。
  核查位置：§3.1–3.3 Eq1–10/Algorithm1；§4.1–4.6；Tables1–4正文讨论

**2610.08639 · Forensic Reserve: Eliciting Latent Knowledge for Image Forgery Detection**

[论文](https://arxiv.org/abs/2610.08639)

- **foundation-model**：RGE用冻结DINOv3的site-wise ICA及real/fake discovery定位reserve、固定输出basis U，只训练零初始化A的残差UA h；classifier/backbone冻结，benchmark不参与discovery。可复用视觉adapter方法，当前证据仍image forensic专门任务。
  核查位置：§3.1；§3.2式3；§4.1

**2610.08622 · Agentic RCA for Internet-Scale Services Using Constrained Creativity**

[论文](https://arxiv.org/abs/2610.08622)

- **agent**：E4以固定typed DAG语法约束RCA Agent，依次选playbook、组合已有operators、合成新operators；实际执行与admission形成可复现核心控制机制。
  复现边界：§4.3用用户true-root-cause反馈admit，只能在训练/validation接收，不能test gold晋级；Accuracy@k,i允许多次尝试，不是单次accuracy；自建DSB有operator设计混杂；正文70 incident阶段统计与Table3总量不一致，图注≤56%与正文其他集0.80也不一致，headline不能无条件复用。
  核查位置：§3；§4.1–4.3；§6.1–6.5/Table3/Figs6–9；§8

**2610.08621 · Recursive Game Creator: An Agentic Product-Level Experience-Oriented Game Harness**

[论文](https://arxiv.org/abs/2610.08621)

- **agent**：Recursive Game Creator包含designer/build、可执行多策略player rollout、盲化版本review及实际artifact retention，保留偏好证据到下一轮，属于固定模型Agent迭代闭环。
  复现边界：非等预算基线，三轮与单轮混杂；用户study仅报告expert数值和playtime，未给强随机对照；97.1%coverage不是GUI速度提升；proxy player不代表人群偏好；能力复现必须实际运行游戏与policy不可gold固定轨迹。
  核查位置：§3.1–3.3；§4.1 Tables1–2；§4.2–4.4/Table3；§5

**2610.08586 · MINDSET: Energy-based Schema Evolution for Long Conversational Agent Memory**

[论文](https://arxiv.org/abs/2610.08586)

- **agent**：MINDSET以immutable episodes和versioned schemas，按distortion/contradiction/history/fragmentation/inconsistency加权能量选择reinforce/supersede/split/new，再展开原始证据检索；定义完整可复现记忆算法。
  复现边界：参数为开发集手调非最优理论，dev仅question-disjoint未证conversation-disjoint；LongContext按20k字节截断；基线为复刻，部分upstream artifacts缺失；最终stay margin而非switch margin决定行动，复现需保留这一实现细节。
  核查位置：§3.1–3.7；§4.1–4.4；§5.1–5.5；Limitations

**2610.08560 · Have I Seen Enough? Frozen Video-Language Models Encode Evidence Readiness**

[论文](https://arxiv.org/abs/2610.08560)

- **foundation-model**：Readiness Gating以冻结Qwen残差的嵌套CV logistic probe预测证据就绪，按训练分位阈值joint readiness/confidence首次停止或deadline最高readiness选答；视频级留出、crossed-quad消除图像/问题独立捷径。固定窗口policy不读证据时间，growing-prefix诊断采样依赖标注不能当部署延迟；§4.4给matched-video-seconds增益。
  核查位置：§3.1–3.3；§4.4；Appendix C/H/I

**2610.08514 · How Much Evidence Should a Coding Agent's Self-Correction Carry? Adaptive Dirichlet Evidence for Self-Distillation**

[论文](https://arxiv.org/abs/2610.08514)

- **agent**：EESD将公开执行before/after四种转移和词法相关性转为有效样本量1/sum(p²)，Dirichlet utility lower score加权CE并保留未加权forward KL；可复现Agent自修正训练机制。
  复现边界：只一轮同source适应，不是source-disjoint泛化；full update vs no-update不能归因有效质量或KL；bootstrap条件于单次训练；有效质量仅relevance集中度，不自动修复执行依赖。
  核查位置：§3.1–3.3 Eq1–11；§4.1–4.4；§5

**2610.08463 · UNREAL: Unifying Retrieval and Long-Context with a Single Model**

[论文](https://arxiv.org/abs/2610.08463)

- **foundation-model**：UNREAL用冻结decoder中层chunk表征、训练64检索token及跨层混合做MaxSim，再重编码所选文本生成；提供multi-positive InfoNCE、公开QA训练split与long-context独立验证协议。
  复现边界：测试不可注入oracle，只有训练hardnegative挖掘用gold；100M场景以稀疏证据为主，dashed延迟是FLOP外推非实测。索引离线编码存储和两次模型forward须计成本；不同baseline训练预算并非完全匹配。
  核查位置：§2.1–2.3 Eq1–7；§3/Table1；§4.2/Figure7；§6；Appendix B.1–B.3

**2610.08452 · Agentic AutoRAG: RAG Pipeline Optimization through Reasoning-Driven Agents**

[论文](https://arxiv.org/abs/2610.08452)

- **agent**：Agentic AutoRAG的检索/生成归因→Diagnoser→KB/成本引导Proposer构成明确搜索机制，可接入evolve候选；准确率实验有100验证/300独立heldout隔离。
  复现边界：医疗Pareto只报告反复优化的同一exam，非heldout能力；成本轴只含生成/扩展API，不含本地embedding/rerank；noKB/diag合并消融不能归因单组件；warmTPE获免费30次同库先验，且不是完整syftr；judge无人类一致性验证。
  核查位置：§3.1–3.3；§4；§5/Table2；Limitations

**2610.08414 · Image Bitstream Fine-grained Understanding for Privacy-Friendly AIoT**

[论文](https://arxiv.org/abs/2610.08414)

- **foundation-model**：BFG将JPEG bytes经ByteFormer分层卷积/shifted-window编码为192维，projector到512维后全局上下文融合+局部cross-attention自回归描述，另120类head；CFU-D源ID/split隔离并测试替换/删除/重复腐坏。Dogs分类58.51%采用ImageNet初始化；不解码不等价正式隐私保证，不能包装为通用大规模foundation结论。
  核查位置：§III-B式2–5；§III-C；§IV-A–D Tables I/IV/V

**2610.08403 · SSR: Sparse Segment Reduction for Ternary GEMM Acceleration**

[论文](https://arxiv.org/abs/2610.08403)

- **foundation-model**：SSR 将三值矩阵分成正负二值矩阵，按列块模式排序并剔除全零模式，以分段求和与树规约代替乘法；公开 C++/AVX2 实现可核验。
  复现边界：报告的是 CPU，部分高稀疏设置慢于 CSC/Eigen；原文未验证 GPU，不能用仓库其他项目的 GPU 目录冒充 SSR。模型级主要是改造三值 MLP 的延迟，没有公开质量保真证据。作者 README 引用 DATE2026，应标记本次 arXiv 收录而非确认首次发表。
  核查位置：§III-A/B Algorithms1–2；§IV-A/B；§IV-C TableIII；§V

**2610.08401 · GeoPID: Decomposing and Steering Visual Information in Vision-Language Models**

[论文](https://arxiv.org/abs/2610.08401)

- **foundation-model**：GeoPID从无标签校准表征估计模态共享/独占子空间，推理按I+αUUᵀ放大vision-unique；22×14组合每组100道独立校准题用标签选层/α后冻结，最终评测不读gold。任务Rényi信息分解为离线诊断，平均相对7.63%需保留308组异质/部分负收益。
  核查位置：§2.1–2.3式11；§3.1；§3.2 Table 5

**2610.08364 · Transect: Retaining Observability for Long-Horizon LLM Agent Evaluations**

[论文](https://arxiv.org/abs/2610.08364)

- **agent**：Transect为公共可执行评测观测工具：family Spec固定词表，structural/judged scanners→provenance tables→源链接报告；可用于evolve审计但不是任务能力评分器。
  复现边界：仅单案例描述，agreement/repeatability不是正确率；读文件不证明采纳、sourceorder非walltime、compaction邻近非因果；Inspect machine-global缓存可能伪造重复稳定性，独立judge重复须freshcache；扩展扫描器可能自行调用模型。
  核查位置：§2.1–2.2；§3.1/3.3–3.5；§4；official README/API

**2610.08341 · DIPrune: Task-Aware Token Pruning with Dual Importance for Efficient Multimodal Language Models**

[论文](https://arxiv.org/abs/2610.08341)

- **foundation-model**：DIPrune结合文本到视觉注意力倒置rank归一与跨层rank上升的截断归一，保留早层低但后层新出现语义token并移除对应KV；多VLM及视频骨干评测、层对齐消融。LLaVA64tokens平均保留97.7%，POPE TTFT73.23→32.50ms、额外0.24ms，需以实际TTFT而非FLOPs主张速度。
  核查位置：§5.1式6–7；§5.2式8；§6.1；§6.5 Table 4

**2610.08183 · Compact Robot Policies Need Fine-Grained Visual Representations**

[论文](https://arxiv.org/abs/2610.08183)

- **foundation-model**：CoRP用可训练DINOv2+48-query resampler/FiLM文本及小DiT flow动作，λ=.01是跨层task-classification辅助CE（不是信息瓶颈惩罚），训练后丢分类head，10步Euler输出动作chunk。LIBERO/RoboTwin为任务内分布；实机另用私有1万小时/5887任务预训练，不能当仅公开sim数据的sim2real。
  核查位置：§3.1；§3.2式4–9；§4.1；§4.7；Appendix A.5

**2610.08164 · Align, Then Correct: Training-Free Two-Stage Low-Rank Compensation for Extremely Quantized Large Language Models**

[论文](https://arxiv.org/abs/2610.08164)

- **foundation-model**：两阶段低秩补偿：非对称激活目标经全输出 Fisher 加权 SVD，再对现有适配器与 K-FAC 自然梯度之和做秩约束 SVD；第二阶段替换而非叠加 rank-r 适配器。
  复现边界：基线同 rank64、同来源校准；本法 Stage2 额外用 8K token 和逐块反向统计，不等于零训练计算。应保留校准/验证/test 隔离，以 held-out C4 和任务指标评价；论文称 training-free 指无迭代优化，不是没有梯度。
  核查位置：§4 Eq5–13；§5 Tables1–5；§6

**2610.08162 · The Failure Is in the Readout: Fine-Grained Emotion Recognition Benchmarks Measure Elicitation, Not Perception**

[论文](https://arxiv.org/abs/2610.08162)

- **foundation-model**：EmoNet读出审计以40类逐类yes/no首token概率对照自由JSON输出，包含answer-mass和单答案有效性门，可作多模态评价诊断。
  复现边界：主κ校准使用测试gold边际，是oracle上界而非可部署评测；须独立heldout校准。生成解析失败被排除、两prompt择优和类别选择需分报。FACES是摆拍表情不是实际内心情绪，须申请研究许可；不支持现实个人情绪推断。
  核查位置：§3 Protocol；§5–7；Appendix Q

**2610.08159 · Making COMET Comparable Across Scripts: Diagnosis and Correction of Tokeniser-Induced Script Bias in Indic MT Evaluation**

[论文](https://arxiv.org/abs/2610.08159)

- **recommendation**：COMET-QN 是印度语言机器翻译评价与文字系统偏差，不是工业推荐；转基础模型审查，非丢弃。
- **foundation-model**：公开COMET脚本偏差诊断与rank-safe quantile校准/LOLO纠偏统计脚本可作为评测审计基础设施候选；不是新LLM，也不是动态评估器已接入。
  复现边界：仓库只从已提交COMET/TP/IP列重算统计，无GPU也不重新运行模型；要评估新candidate须另接真实metric。QN假设同真实质量分布否则抹平真实差异；只wmt22-comet-da五Indic脚本，未量测本语料转写准确性。
  核查位置：§6.1–6.4 Eq2–4；Limitations；official README Quickstart/three sample-size bases

**2610.08155 · Token-Efficient Multi-Agent Collaboration via System One-Guided Computational Division of Labor**

[论文](https://arxiv.org/abs/2610.08155)

- **agent**：S1-MAS用冻结Laya离散决策encoder+Qwen0.6B证据定位，把Solve/Decompose/Reverse/Review/Repair/Contrast及停止交给轻量控制器，真实机制适合协同计算预算候选。
  复现边界：只记GPT输入输出token而非Laya/Qwen本地总算力，节约不是总能耗/总token全口径；代码parse仅接口不是隐藏测试正确率；未找到作者代码链接，Laya明确revision但不可用启发式替代。
  核查位置：§4.1–4.4/Alg1；§5.1–5.4 Tables3–4；Laya model-card reference

**2610.08133 · VLA-ACL: Action-Consistent Visual Token Pruning for Efficient Vision-Language-Action Models**

[论文](https://arxiv.org/abs/2610.08133)

- **foundation-model**：VLA-ACL冻结VLA仅训练5层patch scorer，Laplace soft Top-K总质量K、黑图embedding平方根gate实现可微训练，L1 full-context teacher+GT动作一致性；推理hard topK保留RoPE位置。LIBERO及实机/A100实测，K64成功97.0对96.8、63.49→46.82ms；K32 Long退化须保留。
  核查位置：§III-A/B式6–12；§IV Tables I；Appendix B

**2610.08108 · Enhancing Diffusion Language Models with Autoregressive Post-Training Weights**

[论文](https://arxiv.org/abs/2610.08108)

- **post-training**：A2D task-vector transfer与AR/diffusion增量插值有真实checkpoint benchmark；系数用anchor benchmark选取，本地复现必须改为validation隔离。

**2610.08106 · ChartBmkAgent: Harness-Governed Multi-Agent Construction of Chart QA Benchmarks from Sparse Error-Taxonomy Specifications**

[论文](https://arxiv.org/abs/2610.08106)

- **agent**：ChartBmkAgent 将错误分类/难度作为不可变根约束，由 harness 审批数据、图表、机制锚点与 QA，失败局部修复或回退；适合可审计的评测数据生成候选。
  复现边界：300条合成题；40配对seed比较31/40对21/40；每阶段初次提案外最多4次共享修复/回退。通用路径必经锚点只是模型审查估计而非形式证明；生成器亦被评估、judge重叠，非独立能力证据。原文正文未找到官方代码/数据链接，实施前需公开taxonomy/提示或明确独立实现边界。
  核查位置：Method Eq1–5 / Algorithm1；Experiments Tables2–6；Limitations

**2610.08101 · Beyond Corrected Memory: Execution Consistency in Multi-Agent Systems**

[论文](https://arxiv.org/abs/2610.08101)

- **agent**：CAVERT将义务激活/观察覆盖/有效履行分离，证据不足返回U而非无违规，LLM提取+deterministic规则+precommit read-refresh gate是明确执行一致性机制。
  复现边界：MissingL2仍25/76referenceU误判N，18/52V误判N；gate只对未提交副作用，已提交需补偿；180trace改格式146稳定不等于完全鲁棒；+24.6%token/5秒overhead。正文称supplementary snapshot+432构造trace，但未核实可下载独立repo入口，不称公共基准已接入。
  核查位置：§3.1–3.2 Eq1；§4.1–4.3；§5.1–5.3；Reproducibility；AppendixE.5

**2610.08077 · Self-Retrospection Distillation: Turning Post-hoc Experiences into Prior Foresight**

[论文](https://arxiv.org/abs/2610.08077)

- **post-training**：Salesforce SRD把成功/失败轨迹转成knowledge/pitfall前瞻输出，以带轨迹+gold答案的当前模型停梯度teacher监督不见该特权信息的foresight学生，JSD辅助loss；4/9B十基准。gold仅训练teacher可见，不能混入推理输入。
- **agent**：Salesforce SRD把成功/失败轨迹转成knowledge/pitfall前瞻输出，以带轨迹+gold答案的当前模型停梯度teacher监督不见该特权信息的foresight学生，JSD辅助loss；4/9B十基准。gold仅训练teacher可见，不能混入推理输入。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§3.1–3.2 Eq.4–9；§4.1–4.2（PDF pp.3–6）

**2610.08076 · SpeedrunBench: Challenging LLM Agents with Video Game Speedrunning**

[论文](https://arxiv.org/abs/2610.08076)

- **agent**：SpeedrunBench 在固定轮次及计分调用预算下优化可回放动作轨迹；公开三款开源游戏、固定revision和独立计分容器，适合evolve公共评测。
  复现边界：只接公开SuperTux/Tuxemon/SuperTuxKart，不附商业ROM。原实验harness曾泄露SuperTux计分密钥和STK seed，官方说明当前版本已修正，必须重跑不能继承旧分数；200次每轮评分与无评分器不是同预算。Repo根页未列LICENSE，复用前核许可；代码可读不等于已运行。
  核查位置：§3.1–3.3；§4.1–4.2；§5.1–5.3；Ethics；official README: Changes / isolation / seeds

**2610.08048 · DAEDALUS: Bootstrapping Agent Memory from Self-Generated Tasks**

[论文](https://arxiv.org/abs/2610.08048)

- **foundation-model**：DAEDALUS为agent自生成任务和程序记忆，不属基础模型track；由agent track审查。
- **agent**：DAEDALUS用自生且Explorer亲自完成的任务、失败提炼heuristic、reset后连续3次成功验收、难度调节与冻结整库注入；真实记忆生成/验证机制适合evolve候选。
  复现边界：同一生成任务上的3次成功不是独立泛化验收；LLMjudgeκ.73–.81且自写successconditions，不能视oracle；成本主表排除一次性生成并假设完美promptcache；整合会丢scope，大库并不更好；不支持用户共同控制环境，线上持续更新未获稳定增益。
  核查位置：§3；§4.1–4.2 Tables1–2；§5.1–5.3 Tables3/7；AppendixB；official GitHub contents

**2610.07990 · A Broader Look at Model Merging: Rethinking Implicit Regularization Induced by Task Arithmetic**

[论文](https://arxiv.org/abs/2610.07990)

- **foundation-model**：S-RandOpt以辅助数据梯度扩展task-vector子空间一维后随机采样选模，另比较真正weight-GD与系数GD；支持模型合并搜索研究候选。
  复现边界：WeightGD以更多compute换质量，极少aux会更差；TTA分支使用无标签test属transductive需单独标记，不能和固定模型测试混用。
  核查位置：§3.1–3.2；§4.1–4.2/Table2–3；§5.1–5.4

**2610.07987 · VisionWeave: Weaving Elastic Visual Representations as a Native Capability of MLLMs**

[论文](https://arxiv.org/abs/2610.07987)

- **foundation-model**：VisionWeave可学习gated 2×2 pooler+ViT中间granularity router，细/粗MRoPE中心对齐；三阶段teacher top512前向KL蒸馏依次pooler、soft-mix router、hard-route pooler+LLM，非OPD。训练子集校准50%节省，八bench和SGLang双A100长视频实测2.30×吞吐，FastV改为encoder后版本须标注。
  核查位置：§2.2–2.5；§2.3式10–12；§3.1；§3.4 Table 5

**2610.07972 · Can Agents Work for Everyone? Cross-User Reliability for Mobile GUI Agents in Personalized User Interfaces**

[论文](https://arxiv.org/abs/2610.07972)

- **agent**：PAIR可执行个性化GUI状态与RePAIR按跨用户UC子目标四rollout标准化优势构成可复现机制设计；接受为探索候选，接入必须重做独立validation选择。
  复现边界：31训练spec由测试persona历史baseline结果挑选，因此test-informed不是严格heldout；validation未选择K8iter5；p10–p19尚未完成语义/browser审核。只冻结visualencoder训练LoRA，单训练seed/轮派生seed不是独立重复。oracle参考路径只给reward/eval，不得给Agent。
  核查位置：§4–5 Eq1–6；§6/Table2；Appendix RePAIR training/Selection and review scope

**2610.07940 · Hybrid Latent Attention for Looped Language Models**

[论文](https://arxiv.org/abs/2610.07940)

- **foundation-model**：HLA为looped LM跨循环共享旋转潜KV并保留精确近期窗口；冻结骨干训练writer/reader，真实vLLM/A100同引擎速度与质量测量支持系统候选。
  复现边界：只改善decode；1K单请求慢26%，4K打平。微调两遍前向与标准一遍不等算力；冻结权重RULER16K仍损3.1点，超过16K未测。新增0.35B/0.70B参数必须计入。
  核查位置：§3.1–3.4 Eq1–4；§4.1–4.2；§5.1–5.5 Tables1–3；§6

**2610.07935 · SIGMA: Self-Improving Alignment Generalization from a Model Spec**

[论文](https://arxiv.org/abs/2610.07935)

- **agent**：Apple/JHU SIGMA的同模型taskdesigner+配对一事实变化+spec/rubric自验收+训练监督生成是Agent自改进候选；保留真实模型judges与GRPO，不能以规则fixture代替。
  复现边界：仅一轮selfimprove，bootstrapCI非独立训练seed；singleturn→agentic迁移不是所有domain OOD证明；安全/帮助平衡随spec变，不能只看拒绝率；8rolloutSFTAgentMisalignment3.8而RL9.0不可混用，二rolloutSFT1.1显示非单调规模收益；最终答reward不证明CoT监控性保持。
  核查位置：§2.1–2.2；§3.1/3.6 Table4；§5/Ethics

**2610.07925 · TF-PRVR: Training-Free Partially Relevant Video Retrieval**

[论文](https://arxiv.org/abs/2610.07925)

- **foundation-model**：TF-PRVR冻结VLM，帧特征速度方向变化的db4 DWT分层边界、层内语义/时间与相邻层IoU图，闭式(1−β)(I−βW)^−1传播后逐时跨尺度平均取最大检索分。三标准retrieval数据及三backbone，β=.7固定；离线图逆矩阵/特征成本应计，非新VLM训练。
  核查位置：§4.2式1–4；§4.3式5–8；§5.1–5.3

**2610.07903 · Unsupervised Long-Tailed Adaptation of Vision-Language Models**

[论文](https://arxiv.org/abs/2610.07903)

- **foundation-model**：MARS冻结CLIP学prompt/文本adapter：zero-shot视觉类中心识别unsupported概率迁移并修正weak目标，strong-view CE；再以teacher软类别频率与margin EMA控制KL/伪标签CE权重。9数据γ10/20/50三seed，未知先验但标签集合已知，非开放类别发现。
  核查位置：§3.3式3–6；§3.4式7–10；§3.5；§4.1/Table 1

**2610.07898 · FC-SWE: Failure-Conditioned RL for Long-Horizon Software Engineering Agents**

[论文](https://arxiv.org/abs/2610.07898)

- **post-training**：真实R2E-Gym训练，失败时reset并提供patch/verifier上下文；每次attempt奖励独立、未执行padding不计优势。SWE-bench结果为verifier-assisted不是独立pass@K。
- **agent**：真实R2E-Gym训练，失败时reset并提供patch/verifier上下文；每次attempt奖励独立、未执行padding不计优势。SWE-bench结果为verifier-assisted不是独立pass@K。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§3.2–3.4式3–5；§4.1–4.2 Table 1

**2610.07887 · Visual Abstention in Unified Multimodal Models**

[论文](https://arxiv.org/abs/2610.07887)

- **foundation-model**：VisTA在BAGEL上用feasible/infeasible配对：先reason再image或ABSTAIN，文本CE均训练、flowmatching仅feasible；38224对与1050对DoD图像/maze隔离。无reminder拒绝93.0%、误拒0.8%、edit74.3；paired minimal-change约束定义不可行，不能泛称现实世界不可能或安全对齐。
  核查位置：§3.1–3.3；§5.1式10；§5.2；§5.3 Table 5

**2610.07868 · CueRator: Agentic Search for Symbolic Rules to Adapt Frozen Multimodal Encoders**

[论文](https://arxiv.org/abs/2610.07868)

- **foundation-model**：CueRator在冻结ImageBind上agent发现AST约束closed-form门限式，训练数据Sobol per-video oracle仅诊断结构上限，另训练Gaussian contextual policy用K4 leave-one-out REINFORCE预测10参数；3×20候选val选后测test。可接evolve operator但不可给部署agent访问oracle GT；编码器不训练、seen-only训练且val包含unseen。
  核查位置：§3.2 Algorithm 1；§3.4–3.6；§4.1；§4.2/Table 1

**2610.07862 · A self-learning scientific agent for X-ray diffraction**

[论文](https://arxiv.org/abs/2610.07862)

- **agent**：Gan Jiang将XRD工具执行残差/失败转换为版本化skill修订并开发集成对选型、冻结后heldout比较；接受科学Agent机制及DeltaXRDbench公共评测候选，不能宣称完整闭源toolchain复现。
  复现边界：XMatcher完整实现closed-source，仅basic公开；技能三分支变更范围不同，未隔离单edit贡献且缺完整run/split/version清单。XQueryer split是同结构不同模拟seed，不是unseen structures；opXRD含私有来源，实验合成mixture不等真实混合。repo license null/README要求public redistribution前补license，数据各来源约束单独确认。
  核查位置：Main self-improving workflows/Fig4; Methods Evaluation of self-improvement; Supplementary1.1/1.2/2.4; Data/Code availability; official DeltaXRDbench README/releases

**2610.07860 · WorkflowOps: Learning Agent Collaboration Priors for Multi-Agent Workflow Orchestration**

[论文](https://arxiv.org/abs/2610.07860)

- **agent**：WorkflowOps以Minilm能力匹配、低充分性新Agent生成、合成workflow一阶转移先验添DAG软边/分层执行构成明确orchestration候选，但非经证明持续自演化。
  复现边界：历史频次不是成功因果，新增边可能提高串行约束；transitive reduction保持可达关系，本身不创造并行可执行性；池后续复用未测；基线局部适配且ADASpartial/MaASdeadlock；主成本605秒/query，不能按matcher省调用称整个系统低成本。
  核查位置：§4 Alg1–2；§5 Tables1–2；§6 Limitations

**2610.07851 · RA-MoWE: Workflow-Affinity Embeddings for Query Clustering and Agentic Workflow Generation**

[论文](https://arxiv.org/abs/2610.07851)

- **agent**：RA-MoWE离线probe outcome affinity→cluster expert search→BGE+MLP预测路由是真实可执行工作流优化候选；只能接受text-only Guided-BB路径，test measured affinity列必须诊断隔离。
  复现边界：A†用test outcome不是deployable；B三regime无预设显著收益且Haiku277/300塌单cluster，SWE全选direct。Guided-BB与CoT.3295差CI跨0；Hj已进入wholecluster反馈并非独立search验收；margin2/n非置信保证，后加分析探索性，完整guided-vs-unguided匹配实验缺失。
  核查位置：§2 Eq1–4/Alg1；§3 Tables1/Fig3；AppendixB.2 Eq34/B.3/C.13

**2610.07848 · Dynamic Positional Attention Modulation for Parameter-Efficient Fine-Tuning of Large Language Models**

[论文](https://arxiv.org/abs/2610.07848)

- **foundation-model**：DyPAM根据hidden低秩特征生成RoPE配对维度Q/K缩放，叠加head/layerbias，core PEFT公式完整且有验证选checkpoint和多seed公共任务。
  复现边界：动态不能像LoRA简单离线merge；同参数不等FLOPs需计runtime，preRoPE pair scale改变幅值非旋转角度。已核官方仓库默认master分支README及finetune.py/eval.py/dypam_models.py入口；未运行代码，不能称复现成功。
  核查位置：§3.1–3.6 Eq6–15；§4.1–4.4；App implementation

**2610.07832 · Harness Engineering for Software Engineering via Modular Executable Dev-Primitives**

[论文](https://arxiv.org/abs/2610.07832)

- **foundation-model**：HERMES软件工程agent harness与驻留LLM模块，应由agent track审查。
- **agent**：HERMES将持久文件包装为Dev-Primitive，按依赖动态激活、定向消息、执行诊断后至多3轮再激活修改；接受为文件级Agent编排核心机制。
  复现边界：F.8明确混合公开leaderboard与补跑匹配baseline，12.4pp平均不是全部统一控制实验；文件resident仅保存artifact/messages、不保存hidden state；selection precision/recall用oracle/reference只允许诊断。未发现作者代码链接；不宣称本地已运行。
  核查位置：§3; §4.1–4.3 Tables6–7; Appendix F.4–F.8/G/I

**2610.07819 · $α$Transfer: Coefficient Transfer for Efficient Model Merging**

[论文](https://arxiv.org/abs/2610.07819)

- **foundation-model**：alphaTransfer将小proxy搜索到的全局/任务/层合并系数转给同family大模型，层系数按相对深度复制/插值；目标taskvector编辑仍在大模型原生执行。
  复现边界：需要小/大对应专家checkpoint，省的仅系数搜索不含专家训练；跨family/recipe未证实，ViTB32→L14 AdaMerging++损7.02点，不可说普遍无损。
  核查位置：§3 Eq1–8；§4.1–4.3 Tables2–3；Appendix A.1

**2610.07816 · Do I Need the Cloud? Uncertainty-Aware Step-Level Handoff for Small Language Model Agents**

[论文](https://arxiv.org/abs/2610.07816)

- **agent**：StepGate以本地动作反事实失败标签训练校准门控，结合六类特征、阈值/预算、按需一致性采样逐步选择本地/验证/强模型；接受为真实模型路由机制候选。
  复现边界：只Qwen2.5一族，7B4bit代替cloud；风险特征等预算无可靠提升，标注不是授权/安全保证，token不是隐私保证。Appendix A大量should/recommend为建议规范，不能当已公开artifact事实；未核实作者代码/完整100任务发布。原单步基线调用率不一致，须用rate-matched对照。
  核查位置：§3; §4 Tables1–4; Appendix A.3/A.6–A.9; Appendix C

**2610.07810 · SIFT: Search Intent-to-Filter Transformer for Multi-Task Personalized Filter Ranking at Airbnb**

[论文](https://arxiv.org/abs/2610.07810)

- **recommendation**：SIFT 的随机身份分流与酒店扩展线上证据满足门槛。过滤器点击人数 +20%，普通 booking +0.03% 不显著；酒店扩展 marketplace uncancelled booking +0.76%。原始旅程/过滤器/容量标签未公开，接受待实现不等于已实现。

**2610.07809 · MASKerade: Token-Routed Mask Experts for Dense-to-MoE Upcycling**

[论文](https://arxiv.org/abs/2610.07809)

- **foundation-model**：MASKerade在冻结FFN上训练多专家binary mask与token router，真实hard mask+STE、top1保留softmax概率确保router梯度；等标称激活预算和mask种类对照支持多模态MoE适配候选。
  复现边界：nominal activated参数将重叠mask重复计数，不是unique权重、FLOPs或延迟；作者把重叠复用kernel留未来，不能以mask模拟声称GPU加速；对照expertwidth/LR不同须独立控制。
  核查位置：§3.1–3.4 Eq1–9；§4.1–4.2 Tables1–3；§5；Appendix Table12

**2610.07774 · Reading, Not Manipulating: Leveraging Router Logits for Multimodal Safety in MoE Vision-Language Models**

[论文](https://arxiv.org/abs/2610.07774)

- **foundation-model**：将MoE各层最终prompt token router logits拼接，train统计标准化、class-balanced L2 logistic detector，prefill后τ=.4(val选)拒绝，否则原模型生成；两MoE模型HoliSafe及OOD、MMMU。安全信息可读不等于可通过expert steering控制，残差state也有效；不宣称router独有。
  核查位置：§3.1式4–6；§3.2/Table 1；§4.1–4.4

**2610.07767 · TRACE: Rollout-Guided Quantization-Aware Training for FP4 Reinforcement Learning of MoE Language Models**

[论文](https://arxiv.org/abs/2610.07767)

- **post-training**：将训练activation相邻FP4 codeword选为更接近rollout codeword并缓存mantissa/scale；四MoE训练验证。原native NVFP4路径需相应硬件，不得A100模拟冒称原速度。

**2610.07758 · Later Is Better: Token Reduction for ViTs Under Distribution Shift**

[论文](https://arxiv.org/abs/2610.07758)

- **foundation-model**：Late-concentrated幂律层间token预算是明确可执行的ViT/VLM压缩算子，官方代码公开；多shift、多backbone和五类reducer在保守iso-GFLOPs下有收益。
  复现边界：§3一句late同预算更少FLOPs与其前后解释反向，实际应更少节约；按AppU准确预算。gamma默认依据同主基准敏感性曲线，接入须独立val；AppV只batch64两宽度吞吐不能外推全部iso延迟。部分组件非商业license；video/VLM harness释放状态未核。
  核查位置：§3 Eq1；§4–5 Tables1–6；App A/U/V；official README

**2610.07739 · Cite What You Explore: Budget-Aware LLM Reasoning over Medical KGs with Verifiable Evidence**

[论文](https://arxiv.org/abs/2610.07739)

- **post-training**：证据有/无的同snapshot预测loss差构成paired gain，叠加预算与citation integrity，REINFORCE训练检索reasoner；需真实MIMIC/PrimeKG映射，非手写分数替代。

**2610.07731 · Learning to Retrieve via Reinforcement Learning in Embedding Space**

[论文](https://arxiv.org/abs/2610.07731)

- **post-training**：vMF嵌入策略+G×G product rollout+RLOO，CMP投影降噪；ReasonRank训练、BRIGHT评测、三paired seeds。

**2610.07729 · Foveated Compression: Selective High-Resolution Preservation for Token-Efficient VLMs**

[论文](https://arxiv.org/abs/2610.07729)

- **foundation-model**：Foveated Compression的混合分辨率表示与tie-aware region selector有明确算法，适合作为token压缩/选择诊断候选；不将test-oracle或弱于resize的真实结果包装为提升。
  复现边界：完整visionencoder仍运行，不能把20.99%tokens当E2Ecompute；questionablation无收益。cachedteacher top256非精确fullKL需按论文记录；bootstrap仅样本不含训练seed，decoderuncertainty在生成后不能偷作prefillfree特征。无作者源码链接/公开仓库找到。
  核查位置：§3 Eq1–5；§4 Tables1/2；§5；App A.1–A.3/D

**2610.07706 · WASD: Wasserstein-based Knowledge Distillation for Large Language Models**

[论文](https://arxiv.org/abs/2610.07706)

- **foundation-model**：WASD用teacherembedding成本的去偏Sinkhorn divergence及stopgrad双potential差优化学生概率，有官方训练/评测脚本与等wallclock对照。
  复现边界：实做有限10iter与稀疏support是近似不是无条件精确OTgradient；约2x训练时20%memory，不能称免费；五evalseed不是五trainseed；temperature2与judge/ROUGE偏差需冻结；兼容词表内方法不能自动跨tokenizer。
  核查位置：§3.1–3.2 Eq6/10–11 Algorithms1–2；§4.1–4.2；AppC/E；官方README

**2610.07689 · Unlocking Fine-Grained Perception in CLIP via Structurally-Aware Latent Masked Modeling**

[论文](https://arxiv.org/abs/2610.07689)

- **foundation-model**：SALM通过patch关系/范数差双矩阵和teacher latent masked reconstruction改造CLIP，含无外部teacher的SALM-Self，核心loss和训练课程可保真复现。
  复现边界：same modelsize不等训练compute，RADIO是作者IN1K重训不代表全尺度原版；需隔离超参val并记录seed不确定性；teacher结构上限。官方项目页只有paper/method无源码链接，未找到作者源码发布。
  核查位置：§3.2–3.6 Eq1；§4.1–4.4；App A.1–A.3/C；official project page

**2610.07657 · Where Rules End and Judges Begin: Measuring the Judgment Boundary in Multi-Agent Systems Security**

[论文](https://arxiv.org/abs/2610.07657)

- **agent**：DEFER提供27确定/相似度检查后残余LLM panel的实际host工具/记忆安全管线、四域testbed与outcome oracle，公开MIT代码/attacks/benchmarks/logs/scripts/tests，可作安全评测候选。
  复现边界：CyberOps手调是development upper bound，跨域共用同skeleton；静态攻击非适应攻击，stub工具/合成memory。panel主要offline re-adjudication只直接后果不重生后续轨迹；v3.1主要结果与v2.2/v2.9第三方/其他模型分开，缺ACL+judge基线。未运行代码，不能宣称安全保证。
  核查位置：§II–V; §VI-A/VI-B4/VI-C; §VII-B; official README/provenance/contents/license

**2610.07654 · Does On-Policy Distillation for Safety Pose Backdoor Risks?**

[论文](https://arxiv.org/abs/2610.07654)

- **post-training**：Lazy Defense对teacher-student sampled token log-ratio双侧clipping再stop-gradient，四teacher/student组合测试仅延迟backdoor，不是保证消除。

**2610.07645 · SkillPoison: Progressive Skill Poisoning via Successful Experiences**

[论文](https://arxiv.org/abs/2610.07645)

- **agent**：SkillPoison揭示真实成功经历被提炼为脱离适用条件的技能时产生的治理漏洞，可作为防御性技能晋级回归评测/机制诊断候选，不接受为能力提升策略。
  复现边界：样本先过滤与目标无关类别，再冻结池，非全基准无条件ASR；Adoption基于自报applied_prior_skill/程序模式代理不是因果；公开README只形成经历管线，未核得完整victim技能抽取+冻结任务集+下游ASR evaluator，尚不算evolve可执行基准接入。不开启现实系统攻击，不运行攻击代码。
  核查位置：§3.1–3.4/Eq2–10; §4.1–4.4; Appendix B.1/B.3 Eq13–16/C; official repository README/LICENSE

**2610.07643 · Monte Carlo Estimation for KV Cache Eviction**

[论文](https://arxiv.org/abs/2610.07643)

- **foundation-model**：LORE-KV 从冻结模型采样多条短续写估计未来 query，以中心化 log-prob、熵和分歧加权，再按输出投影后的反事实删除代价选择 KV；采样轨迹随后丢弃。
  复现边界：只靠 attention 分数不能替代该方法；必须计入一次性 lookahead/scoring 成本，并对齐缓存预算与 lookahead token。真实未来 query 仅允许事后诊断，不可用于在线选择；不保证不可见续写性能。
  核查位置：§3.1–3.5 Eq1–8；§4.1–4.5；§5 / Reproducibility statement

**2610.07639 · HarnessSecurity-Bench: Do Security Mechanisms Really Protect Coding Agent Harnesses?**

[论文](https://arxiv.org/abs/2610.07639)

- **agent**：HarnessSecurity-Bench 在固定合法任务下对原生安全机制ON/OFF配对，分离外部确定性utility与attack-effect oracle，适合离线隔离harness回归。
  复现边界：23任务、九机制、六harness、单GLM-5.2、每组合10次；未知oracle从分母排除须公开coverage。官方仓库仅task包和utility checks，完整runner另维护；不能宣称全基准已可复现。攻击仅限隔离合成canary环境，禁止对真实凭据/外部业务运行。许可未在根页列明。
  核查位置：§5.1–5.5；§6.1；§7.1–7.3；Data Availability；official README

**2610.07587 · Large Language Model Orchestration under Heterogeneous Preferences via Explicit Persona Inference**

[论文](https://arxiv.org/abs/2610.07587)

- **post-training**：HARP外置贝叶斯persona后验及规划探索奖励，主要是推理时多代理编排而非参数后训练。
- **agent**：HARP以有限persona库、离线校准response scorer更新每Agent贝叶斯后验，posterior sampling集中规划；HARP+加reward-disagreement探索bonus。接受精确算法/机制诊断候选，不宣称开放对话Agent能力提升。
  复现边界：缩减belief不缩减planner；personas固定且response locality/independent prior限制强。Appendix A.1纠正此前static posterior后，30cases×4reps开放对话所有HARP差异CI下界不正；posterior确实更新仍无score收益。provider不支持seed，cache replay不是model随机种子匹配。未找到公开作者仓库链接。
  核查位置：§3.1–3.3 Algorithm1/Eq2–3/Assumption3.1; §4.1–4.3; Limitations; Appendix A.1 open-text boundary

**2610.07585 · REViT-v2: Hierarchical Windowed Roto-reflection Equivariant ViT for Equivariant Feature Extraction**

[论文](https://arxiv.org/abs/2610.07585)

- **foundation-model**：REViT-v2以group-equivariant QKV卷积、完整representation-field多头局部窗口及群卷积downsample构成层次ViT，O(NM²C)非globalN²；ImageNet及RotMNIST实测，含同stem global控制。需保留有限p4m群/窗口划分几何条件，不能泛称任意角旋转严格等变。
  核查位置：§2.1–2.3式1–6；§3；§4 Tables 1–2；Appendix A

**2610.07572 · Two Vectors Replace In-Context Demos: Structured Task Adaptation via Embeddings**

[论文](https://arxiv.org/abs/2610.07572)

- **foundation-model**：STAVE在frozenLM/LMM输入结构组加两向量、paired有/无demo监督，是真实2d参数适配而非gold-inference或每层模拟。
  复现边界：是每任务有监督训练不是真零shot学习；Table1评val并bestepoch不能作独立test，Tables2/3具heldout协议；反传throughfrozen仍需activationcost；不以首tokengold读取诊断冒充自由生成能力；源码入口未查到正文。
  核查位置：§3.1–3.4 Eq2–7；§4.1–4.3；AppJ

**2610.07557 · CheckerBench: Can Long-Horizon Agents Synthesize Static-Analysis Checkers?**

[论文](https://arxiv.org/abs/2610.07557)

- **agent**：CheckerBench/CheckerLab 按补丁与漏洞前后版本生成静态检查器，冻结产物后独立重建、差分、误报和语义门禁；300任务公共包及固定Linux runtime适合代码Agent评测。
  复现边界：50分钟/任务、21配置各3次；pilot允许人类指导最多2次重跑且筛选至少40步成功轨迹，非无偏任务分布。heldout verifier/reference不能挂载给agent。判断不纯确定性，Opus5参与语义/误报审查，效率只统计成功轨迹。官方要求至少100GB磁盘；第三方许可分别保留，无统一再授权。
  核查位置：§3.1 stages I–VI；§4；§5.1–5.2；official README

**2610.07533 · SkillFormer: Skill-Decomposed Adaptation for Audio Language Models**

[论文](https://arxiv.org/abs/2610.07533)

- **foundation-model**：SkillFormer question embedding kmeans六技能、r16并行adapter及question top2router，先每cluster500步再balanced2000步joint校准；50kQA、三audio模型/三bench。§2.4 PhaseB明确解冻LLM，与PhaseA“throughout冻结”用词有歧义，复现按分阶段并报告训练参数成本，不能宣传全程仅LoRA。
  核查位置：§2.1–2.4式1–3；§3.1–3.4 Table 1

**2610.07532 · Safeguarding LLMs via Model-Agnostic Latent Safety Signals from Dark Knowledge**

[论文](https://arxiv.org/abs/2610.07532)

- **foundation-model**：LADE按有害/良性首token概率差选安全token，跨tokenizer首有效子词和重复映射权重，L1归一特征到有害参考集的kNN距离门控；可实现防御机制。
  复现边界：Hex-Phi和XSTest用于提取/阈值不得再算heldout；K5/k500/quantile0.9。需安全对齐模型和logprobs，过拒与已知token自适应绕过仍在。阈值参考集自距离处理和重复映射非概率守恒应忠实核验；未找到作者代码。
  核查位置：§3.1–3.3 Eq1–5；§4.1；Appendix M

**2610.07522 · Activation Denoising: A Robustness View on Parallel vs Sequential LLM Quantization**

[论文](https://arxiv.org/abs/2610.07522)

- **foundation-model**：Activation denoising 用干净/噪声前向估计 H/C/N 二阶矩，先线性预变换权重，再在新度量下 GPTQ/QuIP# rounding，使各层可并行量化。
  复现边界：原文明确按 WikiText-2 test perplexity 选配置，不能照搬为无泄漏评测；本地须单设 validation 再冻结参数。噪声是传播的逐通道高斯近似，不是每层独立任意噪声；并行可用不等于已测单卡加速。
  核查位置：§4 Eq2–3 / Algorithm1；§5 Algorithm2；§6 Setup/Metrics/Table1；§7
- **post-training**：并行PTQ激活去噪与量化误差正则，属于量化而非RL/OPD后训练。

**2610.07457 · AlignQuant: Tile-Aligned Mixed-Precision Quantization for Efficient LLM Generation**

[论文](https://arxiv.org/abs/2610.07457)

- **foundation-model**：AlignQuant 以64×64 tile统一量化分配、打包与GPU执行；prefill/decode Fisher敏感度分别归一化后取最大值，低敏感tile使用4bit，其余8bit；实际整数路径是核心组成。
  复现边界：不能用fake quant张量当作速度实现；需实际CUDA/CUTLASS扩展、打包字节、变换和暂存开销，含TTFT可能比BF16慢。原文A100结果不代替仓库自己的A100验收。
  核查位置：§3.1–3.3 Eq1–3；§4.1–4.4 Tables1–3；official README
- **post-training**：GPU tile对齐混合精度PTQ和kernel，不是策略后训练。

**2610.07389 · Inference and learning in sparse autoencoders as natural gradient flow**

[论文](https://arxiv.org/abs/2610.07389)

- **foundation-model**：BeFOND将Bernoulli稀疏编码的推断与字典学习同时构造为natural-gradient flow，具closed-form更新、可执行官方核心与公共SAEBench任务，适合作为表示诊断/干预算子候选。
  复现边界：12–14x BatchTopK每token训练时长；1000x是6M/8Btoken比非FLOP节约；ZCA预处理看500Mtrain tokens应计额外数据。仅一个LM层，理论rare补偿依赖frozen matched moments。官方默认etd1_guarded与paperETD1须按PAPER_MODELS固定，预训练checkpoint未发布；不能用toy结果冒充Gemma干预。
  核查位置：§3 Eq9–17；§5–6；App B.6–B.7 Algorithm1；App D.1–D.3 Tables7/10；official README

**2610.07385 · Semantic Capability Acquisition and Specialization During Vision-Language Model Fine-Tuning**

[论文](https://arxiv.org/abs/2610.07385)

- **foundation-model**：SSR训练时NAME/ATTRIBUTE routed causal隔离、融合summary及可选NAME dropout=.5，评测恢复普通EOT；P3无name及CAPP反事实区分描述可读性。6CLIP类模型跨数据验证，P3轨迹峰值为回溯诊断不是可部署选模，部署按P1选择。未保留fork revision及subset生成脚本降低精确复现强度但核心训练定义可实现。
  核查位置：§3；§4.1–4.4；Appendix B（class subsets）、training environment

**2610.07376 · MemCo: Memory-Centric Collaboration for Generalizing LLM Agents to Unseen Environments**

[论文](https://arxiv.org/abs/2610.07376)

- **agent**：MemCo本地trajectory graph提取条件化规则，episode-reduced正负证据经role抽象exact-key聚合，Wilson分数促进/撤回global records，state/phase/goal检索+grounding组合；接受Agent memory核心候选。
  复现边界：unseen为agent未采集该域，其他agent可已见；必须与layout-heldout区分。Wilson是近似binomial界，episode去重不保证跨episodeIID；ablation同snapshot非独立重复。官方NOTICE说明上游GMemory无许可、再分发尚待确认，源码可读不等于可直接复制；模型/生成memory/logs不含在artifact。
  核查位置：§3.1–3.5 Eq2–10; §4/4.2; §6; Appendix D.1/F.1; official README/NOTICE

**2610.07349 · RELACE: retrospective likelihood-based action credit estimation for long-horizon language agents**

[论文](https://arxiv.org/abs/2610.07349)

- **foundation-model**：RELACE多步agent RL信用分配，应由post-training/agent track审查。
- **post-training**：执行动作原始/结果条件似然比修正局部return，终局信息仅用于训练credit；ALFWorld/WebShop真实训练，但主表混用文献baseline，应本地同预算复核。

**2610.07348 · Stepped MoE: Segment-Level Routing with Configurable Inference Complexity**

[论文](https://arxiv.org/abs/2610.07348)

- **foundation-model**：SteppedMoE以前12dense层一次预测后44层专家集合，每段首token刷新、预算embedding与多稀疏度loss缩放联合训练，真实12B模型1Ttoken支持可变计算架构候选。
  复现边界：吞吐来自NPU模拟器与真实matmul/NANDtransfer参数，不是实机端到端；总训练成本近4个static模型合计，1Ttoken不等单dense训练算力。loss缩放作者明确为简化proxy并非专家频次精确LR。
  核查位置：§2.3–2.5 Eq1–3；§3.1/Tables1–3；§3.4/Figure3；§5

**2610.07338 · Logbook: Extremely Long-form Audio Event Understanding**

[论文](https://arxiv.org/abs/2610.07338)

- **foundation-model**：Meta Logbook提供连续音频全覆盖事件分段+description：E2E10min或10s caption→text10min，Ego4D/SINS/EgoLife；fAcc主分段、OLMo atomicfacts+BARTMNLI重叠段dF1主描述。人工参考含视觉/LLM标签非上限，PFLOPs为估计非延迟。官方repo有loaders/prompts/run_e2e/run_cascade/eval评分，可接公共audio evaluator。
  核查位置：§2.1–2.4；§3；§4.1–4.2；官方README Repo layout；README: Repo layout / scripts/run_e2e.py / run_cascade.py / eval_segmentation.py / eval_descriptions.py

**2610.07335 · Selective Critique for Cost-Aware LLM Agents in Long-Horizon Decision Making**

[论文](https://arxiv.org/abs/2610.07335)

- **foundation-model**：SAG选择性critique用于长程agent，应由agent track审查。
- **agent**：SAG对可执行动作长度归一loglik分布算entropy+top2margin门控，无gold critic纠偏；每10成功episode从同base重新LoRA-SFT累计action pairs，接受真实门控+在线学习候选。
  复现边界：这是顺序test-time adaptation，先前test成功轨迹可训练后续episode，非冻结模型heldout能力；后续不回测旧episode。token效率不含训练/全候选action likelihood计算成本；WebShop只初始search后有限click动作。默认公开WebShop500/BabyAI50与论文200/100不同须固定配置；license null不可直接视作可再分发。
  核查位置：§3.1–3.4 Eq1–4; §5; Appendix G.1–G.3/H.3–H.5; official README

**2610.07332 · Structuring MoE Expert Selection for Agentic Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.07332)

- **foundation-model**：operation标签和router互信息、相邻token专家集合一致性及entropy gate联合agentic RL；AppWorld/AutomationBench真实训练，需模型路由不可用proxy。
  核查位置：§3.1–3.3；§4.1
- **post-training**：operation标签和router互信息、相邻token专家集合一致性及entropy gate联合agentic RL；AppWorld/AutomationBench真实训练，需模型路由不可用proxy。
- **agent**：operation标签和router互信息、相邻token专家集合一致性及entropy gate联合agentic RL；AppWorld/AutomationBench真实训练，需模型路由不可用proxy。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§3.1–3.3；§4.1

**2610.07324 · Scale-Invariant Training for Time Series Foundation Models**

[论文](https://arxiv.org/abs/2610.07324)

- **foundation-model**：ScaleIn将loss置于context-normalized target空间，作为时间序列基础模型training-config算子候选；本文是已存在策略的系统理论/实证审计，不宣称全新网络。
  复现边界：TimesFM49.6M减宽减深并去quantilehead非原200M；监督任务仅MASE平均1.9% WQL1.1%，非处处大增。带arcsinh非仅b^p比率，固定统计/偏置须保真；无本论文官方源码链接找到，AppendixC可执行定义可独立实现。
  核查位置：§3 Eq1–10/Theorem3.2；§4.1–4.4 Tables3/4；App C/G.1/H

**2610.07311 · Understanding and Mitigating Inference-Time Overreliance Using Agentic Memory**

[论文](https://arxiv.org/abs/2610.07311)

- **agent**：MemTrim用LLM规范化原子证据+task signature/answer support，独立key-value trie索引；删与当前重复或矛盾证据、support变化则抑制旧answer、task变化则typed reuse，接受memory治理机制候选。
  复现边界：当前query无条件优先是关键可信性假设，不能移用于攻击者query或称通用防御；support/实体canonicalization由LLM估计不是因果依赖证明。overlap sweep同时恢复answer-relevant信息，不能证明仅重复量的纯因果效应。写入parser成本被摊销、runtime仅read+generation；未找到作者代码，需独立实现且不能替换parser为fixture。
  核查位置：§2; §3.1–3.3 Eq1; §4.1–4.4; Appendix A.1/C benchmark construction

**2610.07289 · Catching Developers in the Flow: Low-Latency Agentic Program Repair at Google Scale**

[论文](https://arxiv.org/abs/2610.07289)

- **agent**：Google FlowAgent以预/后执行过滤、ReAct generate-and-validate和最终测试完成低延迟presubmit修复；核心候选接受，未实现。
  复现边界：不是随机A/B；采用有选择偏差；内部Gemini和私有数据/源码不公开，公开APR替代仅能独立机制验证。
  核查位置：PDF pp1–10; §3; §4.1; §4.2/Table2; §5; Data Availability

**2610.07261 · Verifying Coordination in Parallel Coding Agents: NP-Bench and a Scheduling Planner**

[论文](https://arxiv.org/abs/2610.07261)

- **agent**：Nerveplane被动观察git状态，按文件scope冲突着色分批并按契约依赖排序合并，NP-Bench含真实git集成与live coding agents，可作并行evolve协作评测候选。
  复现边界：scope和依赖人工给定；DAG保证不覆盖cycle-break启发式。脚本TierA仅机制诊断，live仅3–15seed简单构造；planner比baseline多获得确切契约，不隔离信息量与时机，不能宣传普遍100%协调成功。
  核查位置：§3–5 Algorithm1；§6.2–6.3；§9/reproducibility

**2610.07258 · Lineage-Aware Memory Governance: A Derivation-Gated Framework for Privacy-Preserving Column-Level Access Control in Enterprise AI Agents**

[论文](https://arxiv.org/abs/2610.07258)

- **agent**：Lineage-Aware Memory Governance以敏感列派生标签、最新安全记忆检索及定义hash冲突提示实现明确可复现的共享Agent记忆治理；接受为机制诊断候选而非生产安全能力。
  复现边界：定理仅完整lineage+fresh computation预先授权+最新policy标签；缓存key只有metric而非语义一致定义，冲突只提示不阻止；只管登记敏感列非所有ACL。未识别view/UDF内部列时解析可能静默成功，fail-closed仅在检测失败触发，故不能保证所有不完整提取安全。模拟不等能力比较；原码明确future open-source，无发布URL，独立机制实现不能冒称作者完整复现。
  核查位置：§III-A–C algorithms/Eq1–2; §IV Theorem1/Corollary3; §VI-A–E TablesVI–VII; §VII-B; §VIII

**2610.07247 · Learning What to Distill: Bilevel Top-K Token Selection for Self-Distillation in Large Language Models**

[论文](https://arxiv.org/abs/2610.07247)

- **post-training**：Soft-OR效用、softplus阈值内层与soft mask形成近似bilevel选择；阈值detach、全词表forward KL。200步最终checkpoint；TIP比较同时改变divergence，不可单独归因选择器。

**2610.07212 · Reward-Driven Learning under Prompt-Level Differential Privacy**

[论文](https://arxiv.org/abs/2610.07212)

- **post-training**：DP-GRPO以prompt group为DP-SGD裁剪记录、单更新GRPO为record loss；隐私会计与实际Qwen1.5B LoRA实验，保留DP机制而非仅加噪声示意。

**2610.07191 · Agentic Design Space Exploration for Joint Hardware Configuration Selection and Mapping of AI Inference Workloads on Heterogeneous Edge SoCs**

[论文](https://arxiv.org/abs/2610.07191)

- **agent**：TraceDSE以真实硬件执行trace→工具化critic→proposer→Pareto/exploration state组成实测搜索闭环，适合evolve算子机制候选。
  复现边界：能耗50次推理窗口采样减idle，非瞬时单次读数；跨全部算法的Pareto max归一reference依赖已观察结果；critic估计不捕获争用必须真实验证；更换模拟器不复现论文硬件收益，未找到作者发布代码；不是Google机构，仅用Gemini。
  核查位置：§3.1–3.6; §4; §5.1–5.3 Tables2–4

**2610.07177 · CLM-as-a-Judge: Evaluating an Open Contrastive Decision Model on Public Judge Benchmarks**

[论文](https://arxiv.org/abs/2610.07177)

- **post-training**：公共judge评测与校准级联协议：calibration/eval隔离、双顺序、常数baseline及成本—风险读数。arXiv官方abstract页已枚举ancillary的pins、split、per-item预测、judges/run_pass/metrics/analysis源码。托管strong judge不可固定revision；本次未运行代码，单个附件浏览器读取报错。

**2610.07132 · CroissantMiner: Automated Extraction and Validation of Croissant Metadata for ML Datasets**

[论文](https://arxiv.org/abs/2610.07132)

- **foundation-model**：CroissantMiner含102human-gold+500silver的30字段paper metadata，singlepass及4agentic抽取，rule/LLM分字段score与NULL惩罚；Sonnet4.5预填不参与排名，judge最终κ.708/hardset.663应替代初始.890。外部metadata enrichment与paper-only gold有边界冲突需分开；官方MIT仓库有data/evaluation/CLI，可接evolve信息抽取评测。
  核查位置：§3.1–3.3；§4.1；§5.1–5.3；官方README/data/evaluation；README benchmark/data/evaluation/CLI, MIT
- **agent**：CroissantMiner 提供论文到30字段Croissant metadata的单次/并行专家/triage-critique/locator/ReAct对照，以及602论文、102人工gold，可用于研究资料提取的公开评测。
  复现边界：14开发/88测试，500silver不可冒充人工gold；原文未载字段应null，部分Agent额外查外部metadata会改变任务定义，须区分paper-only与enriched。judge为模型且gold基于Sonnet预填，Sonnet4.5明确不排名；不能拿自动提取替代本项目逐篇证据核查。
  核查位置：§3.1–3.3；§4.1；§5.1；Limitations；official README

**2610.07121 · SoloQ: Calibration-Free Quantization for Diffusion Language Models**

[论文](https://arxiv.org/abs/2610.07121)

- **foundation-model**：SoloQ K-RPBH在permuted blockHadamard后Haar跨块混合，weight E8P/activation Lloyd或NVFP4分布quantizer，无校准数据；scale ||z||²/<q(z),z>修正仅恢复投影非无误差。blockdiffusion仅commit KV量化、active保持高精度。五dLLM实验，H200 accuracy/低位硬件性能须区别A100可运行性。
  核查位置：§4.2–4.5式4、7–12；§5.1–5.3；Appendix B/C
- **post-training**：SoloQ为免校准扩散模型量化与KV压缩，非策略后训练。

**2610.07118 · AMBER: Training Long-Horizon Web Agents through Append-Only Memory**

[论文](https://arxiv.org/abs/2610.07118)

- **foundation-model**：AMBER长程web agent追加记忆RL，应由agent track审查。
- **post-training**：append-only两回合memory/action共享GRPO终局优势，插入模板token mask；实验先SFT初始化，不得声称完全无SFT；需web环境。
- **agent**：append-only两回合memory/action共享GRPO终局优势，插入模板token mask；实验先SFT初始化，不得声称完全无SFT；需web环境。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§4.2式10；§5

**2610.07043 · TRIAGE: Direction-Aware Mismatch Stabilization of Native NVFP4 Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.07043)

- **post-training**：TRIAGE在负优势负gap token按segment门控并保持响应更新质量归一化，正优势加有界pseudo-Huber修复；真实NVFP4 learner/sampler实验，A100仿真不能宣称原生吞吐。

**2610.06993 · DART-ES: Difficulty-Aware Reweighting and Targeted Replay for Fine-Tuning LLMs with Evolution Strategies**

[论文](https://arxiv.org/abs/2610.06993)

- **foundation-model**：DART-ES进化策略后训练的难度重加权，由post-training track审查。
- **post-training**：DART-ES用扰动种群正确率EMA构造连续难度权重，并以掌握阈值和零成功耐心控制稀有可解样本重放；实际LLM数学ES对比，不能把历史正确率oracle放入评价agent。

**2610.06966 · APEX: Active Protection at Execution Boundaries for LLM Agents**

[论文](https://arxiv.org/abs/2610.06966)

- **agent**：APEX 冻结用户授权合同，在执行边界以 WRAP 核验效应授权，以 PLANT deception receipts 暴露未获准信息使用，失败安全延续。AgentDojo/ASB/MCPTox/MSB/Skills 公开任务支持验证。
  复现边界：0 ASR 不等于开放环境安全保证；攻击者按每个 defense 固定反馈优化，需透明报告；禁止让 skill 文本改写授权；合同误差、阻断和恢复失败单列。
  核查位置：APEX Algorithm1; WRAP/PLANT coordination; §experiments; Appendix C/D

**2610.06964 · Principles that Guide, Actions that Inform: Agent Evolution via Knowledge Abstraction**

[论文](https://arxiv.org/abs/2610.06964)

- **agent**：SAGA 将执行轨迹抽象为分层经验/原则，检索后适配当前任务，并可 SFT/GRPO 优化 actor。ScienceWorld/ALFWorld 的证据 grounding 与 utility ledger 规则可执行。
  复现边界：严格 ALFWorld 7B complete-hierarchy R1–R3 没有 L3 原则通过验证，不能将性能归因已验证原则；强 builder 弱 actor 非纯同模型自进化；API fault 不可丢弃成成功。
  核查位置：SAGA retrieval-utilization-abstraction; Algorithm1; normalized p34,44,82–90,115–116

**2610.06963 · WavePrune: One period is often enough for RoPE**

[论文](https://arxiv.org/abs/2610.06963)

- **foundation-model**：WavePrune将每个RoPE二维通道的QK贡献限制在首旋转周期，FlashWavePrune按16维组取最大窗口实现TensorCore稀疏算子，可用于推理及重新预训练。
  复现边界：是通道贡献置零而非整token的softmax mask；组近似与exact应分别校验。KV物理淘汰仍futurework，A100内核速度非整模型收益。alpha/通道消融用HELMET需新val选择后独立test，不能拿调参集提升作泛化。代码目录有kernel/训练/eval但完整README待发，许可需单独核验。
  核查位置：§3.1 Eq6；§3.3 Eq8；§4.1–4.5；official README

**2610.06950 · Learning to Decide, Not to Reason: Parameter-Efficient Decision Operators via Low-Rank Activation Steering**

[论文](https://arxiv.org/abs/2610.06950)

- **foundation-model**：DecSteer训练共享低秩activation residual与token门控，初始identity但输出支路有梯度，集中学习决策而非全模型；真实SearchQA/LiveMath BC及多基准，需保留RMS+SiLU+gate结构。
  核查位置：Abstract（输入检索工件中的完整摘要已逐条审阅）；§3；§4–5
- **post-training**：DecSteer训练共享低秩activation residual与token门控，初始identity但输出支路有梯度，集中学习决策而非全模型；真实SearchQA/LiveMath BC及多基准，需保留RMS+SiLU+gate结构。

**2610.06947 · FactorBench: A Portfolio-Aware Benchmark for Automated Factor Mining**

[论文](https://arxiv.org/abs/2610.06947)

- **post-training**：公共评测：统一symbolic/Python factor→date×asset signal契约，5市场、训练2017–21/验证2022–23/测试2024–25，组合和成本回测。官网仓库含data/evaluator/mining入口，可作为专门的自动研究任务，不宣称普适LLM能力或实盘A/B。
- **agent**：公共评测：统一symbolic/Python factor→date×asset signal契约，5市场、训练2017–21/验证2022–23/测试2024–25，组合和成本回测。官网仓库含data/evaluator/mining入口，可作为专门的自动研究任务，不宣称普适LLM能力或实盘A/B。
  核查位置：§3.1–3.3；§4；Appendix B；作者仓库README/文件列表已只读核查

**2610.06932 · RADC: Risk-Aware Dual Caching for Vision-Language Test-Time Adaptation**

[论文](https://arxiv.org/abs/2610.06932)

- **foundation-model**：RADC前景/全局双cache与高斯风险准入是具体VLM TTA候选。
  复现边界：64视图/patch获取不可换成单forward；4090 ImageNetA RADC12.26min/2084MiB，对SCA7.14min/988MiB更慢更大，只准确率更高。Gaussian风险是近似不是校准正确性保证；超参全域固定但调参验证来源须补，未找到源码链接。
  核查位置：§2.2 Eq3–7；§2.3 Eq8–9；§3.1–3.4 Table4

**2610.06892 · Axiom Satisfiability of Linear Rewards in Alignment**

[论文](https://arxiv.org/abs/2610.06892)

- **post-training**：LP3在有限偏好图上共同最小化candidate slack和线性reward margin违反，以LP松弛替代ILP；Habermas真实偏好验证，不含LLM策略训练，也不保证未见response公理。

**2610.06844 · Learning to Read the Contextual Tokens in Diffusion Transformers**

[论文](https://arxiv.org/abs/2610.06844)

- **foundation-model**：Contextual Reader用跨MM-DiT层contexttokens加layer/timestep embedding→2层Qformer→冻结LLM QA探测；核心CoAl以单早层1query aligner负cos匹配冻结SigLIP clean图teacher，jointflow训练并对null-condition加权抑制prompt捷径，推理丢aligner。COCO从零与SD3 Fine-T2I微调分开验证，不能把readoutprobe当新生成能力。
  核查位置：§3.1–3.3；§4.1；§4.2–4.3
- **post-training**：视觉扩散Transformer contextual tokens读取与对齐，属于图像生成模型训练而非LLM RL/OPD。

**2610.06843 · Recursive Video In-Context Learning for Agentic Robot**

[论文](https://arxiv.org/abs/2610.06843)

- **agent**：RV-ICL的多层示范索引与按子目标重入是明确Agent上下文访问机制；只接受示范条件化诊断候选，须将阶段目标/仿真状态来源与非gold能力评测隔离。
  复现边界：phase map含示范状态派生目标、task objects/regions，目标改写时还明确告知哪些示范无效；这不是无gold-plan自主规划证据。若本地沿用评测隐藏目标/解答计划则只能诊断，不得evolve能力晋级；旧基线与新法非同episode配对，pooled z未任务簇修正；未找到本法公开代码链接；所有实验仿真非真机。
  核查位置：§3.1–3.3 Algorithm1; §4; §5.1–5.4 Tables1–4; Appendix A/B; Limitations

**2610.06830 · MemPilot: Orchestrating On-Demand Multimodal Memory Curation for LLM Agents**

[论文](https://arxiv.org/abs/2610.06830)

- **foundation-model**：MemPilot多模态agent记忆编排策略，应由agent track审查。
- **post-training**：质量/成本/延迟分别组归一后合并，prefix probe边际答案质量修正阶段credit；训练latency用proxy estimator，不能冒称直接壁钟reward。
- **agent**：质量/成本/延迟分别组归一后合并，prefix probe边际答案质量修正阶段credit；训练latency用proxy estimator，不能冒称直接壁钟reward。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§3.3式7–13；§4.1

**2610.06829 · CLIFT: Conformal Self-Verification for Web Agent Training and Test-Time Scaling**

[论文](https://arxiv.org/abs/2610.06829)

- **post-training**：conformal自验证非负bonus和URL-stratified return优势改变credit；WAI训练、VWA bank transfer、OM2W无policy训练须分别报告。
- **agent**：conformal自验证非负bonus和URL-stratified return优势改变credit；WAI训练、VWA bank transfer、OM2W无policy训练须分别报告。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§2.2式6–7；§3 Experimental Design

**2610.06817 · Paradee: Distilling Kokoro-82M into an 8M-Parameter Single-Voice Text-to-Speech Model**

[论文](https://arxiv.org/abs/2610.06817)

- **foundation-model**：Paradee 将 Kokoro 单音色蒸馏为 8.07M TTS，分阶段训练文本与解码器，保留多分辨率频谱损失、GAN 精调和相位锁定。WikiText103 教师生成语音与 200 句评测可重建。
  复现边界：只验证 af_heart 单音色；自动 UTMOS/WER 不等于人类自然度评价；CPU 计时排除音素化；int8 是权重而非全激活量化。
  核查位置：§4.1–4.6; §5–9; Appendix A–C

**2610.06804 · Sharpen Without Search: On-Policy Distillation of Sequence-Level Power Distribution**

[论文](https://arxiv.org/abs/2610.06804)

- **post-training**：Rényi梯度对应teacher幂分布×student分布的加权MLE，SMC沿student proposal重采样；GSM8K训练不读reference答案，保留整条SMC训练链。

**2610.06782 · T-Search: An Open Agentic Retriever and Playground for Hard Multi-Step Search**

[论文](https://arxiv.org/abs/2610.06782)

- **post-training**：公共检索Agent入口：冻结语料search/save_and_advance/finalize工具及多轮证据状态，TRuST/SynthComp公开基准；官方Apache-2.0 harness已可读。final-set Recall@10与生成Agent trajectory recall不可直接横比，融合3次须计预算。

**2610.06751 · MatrixFormer: A Foundation Model for Matrix Completion**

[论文](https://arxiv.org/abs/2610.06751)

- **recommendation**：MatrixFormer 属于通用 Transformer 架构，已转基础模型全文审查。
- **foundation-model**：二维cell grid、行列轴向注意力与synthetic prior训练的78M通用矩阵补全模型，作为表格基础模型研究候选，而非工业推荐AB通过。
  复现边界：作者承认开发期间看过下游benchmark，UCIcontext为exploratory。ensemble在输入已观测未mask单元拟权重有乐观风险，heldout权重留作未来；107x是单expert固定10列H200计时，双expert需两pass。未核到作者公开模型代码。
  核查位置：§2 Eq1–11；§2.1；§3.1–3.6 Tables1–3；§4

**2610.06750 · Balancing Memory Pathways: Analyzing and Improving Memory Utilization in Hybrid LMs**

[论文](https://arxiv.org/abs/2610.06750)

- **foundation-model**：保留混合LM两条记忆路径，额外attention跨segment屏蔽的递归辅助SFT损失有公开实现，符合可执行训练operator。
  复现边界：lambda.25按Quest最优但附录未明确val选参，应本地锁val；two-pass半steps不是实测FLOPs完全等价；§6perexampleOracle与给成功/失败反馈只diagnostic，不把oracle32%当可部署。
  核查位置：§3；§4.1；§5.1–5.2；§6；AppB/C.1；官方README
- **agent**：Balancing Memory Pathways对hybrid recurrent-attention LM加auxiliary recurrent-only NTP，屏蔽跨segment注意力但保留跨段递归状态；LoRA双前向训练后完整模型正常执行。接受Agent记忆学习/后训练跨轨候选。
  复现边界：lambda.25从Quest表现挑选，须在本地validation重选/固定；未见独立多训练seed区间。成功示范实验使用同game已有成功轨迹，仅条件化效率诊断；oracle逐例选最佳路径非部署。默认不含goldwalkthrough，训练gold与评测隔离；repo未见LICENSE，公开可读不代表再分发授权。
  核查位置：§3/§4.1/§5.1–5.2 Table1; §6; AppendixB.2/C.1/C.3; official README

**2610.06748 · BazaarBench: Delegation Safety in Decentralized C2C Marketplaces Run by LLM Agents**

[论文](https://arxiv.org/abs/2610.06748)

- **agent**：BazaarBench 以可复制30天市场状态和固定20代理群做7天continuation，事件/库存真值与交易安全阶段分开，适合多Agent委托约束评测。
  复现边界：100代理、3基础市场、45continuation各单次并非多独立seed；照片是JSON不是视觉。部分风险标签依赖GPT5，idealized inspection不是实物验收，虚拟收益不是线上A/B。L0阻断库存错误而L1–L3只记录，不能直接跨条件解释因果。仅合成服务，禁止连真实交易账号。
  核查位置：§3.1–3.3；§4.1；Appendix B/C

**2610.06729 · Improving Diversity in LLM Short Story Generation**

[论文](https://arxiv.org/abs/2610.06729)

- **post-training**：DivLM的CPT指令残差恢复与群体genre/tone/style/entity多样性奖励为可执行两阶段训练配方，需真实judge与语料。

**2610.06686 · OVAL: Output-Aware Local Page Bases for KV Cache Retrieval**

[论文](https://arxiv.org/abs/2610.06686)

- **foundation-model**：OVAL 对键能量与键值输出敏感度矩阵做归一化混合，以主特征子空间构建页表示；decode 用低秩重建 logits 的 logsumexp 选页，无需每次读取值统计。
  复现边界：主表 η* 是逐设置最佳值，不是固定无泄漏结果；接入要按独立 calibration 冻结 η，并报告转换和检索开销。原文相对FreeKV有约10% decode成本，不应只报道质量提升。
  核查位置：§3 Eq1–5 / Algorithm1；§4.1；§4.3；§4.5；official README

**2610.06671 · Learning What to Imitate: Entropy-Aware Distribution Mixing**

[论文](https://arxiv.org/abs/2610.06671)

- **post-training**：ConMix/GeoMix由student top-K归一entropy控制teacher比重，用于采样SFT与forward KL；两种混合本身已有AMiD，新增是entropy调度。

**2610.06666 · What Matters for Latent Reasoning with Flow Matching**

[论文](https://arxiv.org/abs/2610.06666)

- **foundation-model**：FLaRe以symbolicCoT VAE+noise-shiftedFM和verified rollout全路径反传，包含独立可执行latent reasoning训练机制，不只是测量综述。
  复现边界：训练reference验证合法但推理不得goldcheck；decodedreading借3BautoregressiveVAE不能标无CoT效率；direct2Euler为97%CoTacc/3.9x单GPU，而默认20step需分别计budget；多samplepass16非部署selector；stage1EMA/stage2LIVE要保真，tinyarith模型不可泛化通用reasoning。
  核查位置：§2.2–2.3；§3.1/3.2.1–3.2.4；§4.1–4.5；§5；AppA.3/D/E

**2610.06650 · Wikidata Search Traces: A Dataset for Training Knowledge Graph Search Agents**

[论文](https://arxiv.org/abs/2610.06650)

- **foundation-model**：Wikidata搜索轨迹数据和RLM harness，属于agent track。
- **agent**：Wikidata约束图构造唯一可验证问题，持久Python REPL组合13类图查询函数，保留成功搜索轨迹，适合训练数据/Agent工具harness候选。
  复现边界：采集教师曾获得答案路径clue，导出prompt删除clue不等于无特权rollout；只能作教师训练数据，正式评测不得传线索。10,235条成功筛选偏差、RLM图调用远多于tool baseline，尚无小模型训练结果；必须固定图快照、匹配查询预算和heldout题。
  核查位置：§3.2–3.5；§4.1；§5 limitations

**2610.06648 · Representation-Space MMD for Diffusion Language Models**

[论文](https://arxiv.org/abs/2610.06648)

- **post-training**：冻结DLM token表示RBF-MMD，离散单denoiser pass采样后group REINFORCE，连续bootstrap后求导；OWT/GSM8K及16B DMax实验。

**2610.06647 · LoGRA: Scaling LLM Reinforcement Learning with Low-Rank Gradient Sketches**

[论文](https://arxiv.org/abs/2610.06647)

- **foundation-model**：LoGRA低秩梯度与KL步长控制用于RL后训练，由post-training track审查。
- **post-training**：直接累积随机投影gradient sketch、低秩update与predicted-KL步长；PPO实际多scale训练，H100结果不能外推A100。

**2610.06637 · Long-Horizon Textual World Modeling through Structured Reasoning**

[论文](https://arxiv.org/abs/2610.06637)

- **post-training**：真实encode-transition-decode rollout tree按兄弟组credit，predictive gain与中间状态reward共同训练；无需gold textual state。

**2610.06636 · Differentially Private Mixing of Public Datasets Improves Private Learning**

[论文](https://arxiv.org/abs/2610.06636)

- **foundation-model**：DP-MixMin对公共预训练源权重进行有隐私会计的凸代理优化，是基础LM数据混合候选，不仅医疗应用；GPT2-Medium两个文本域有完整预训练/DP微调实验。
  复现边界：理论依赖MixMin reduction/Bayesoptimal假设，实证代理不保证；noise会计不可用普通SGD替代，imagepilot/validation选择额外隐私使用需单列，canary下界不能证明全上界。Enron148users且仅sent避免多人归属，不等于任意邮箱级DP；原作者源码未找到。
  核查位置：§4.1–4.2 Algorithm1；§5.2–5.3 Tables1/2；App A.3.2/A.7/A.8

**2610.06617 · RealtimeWAM: One-Step Asynchronous World Action Models**

[论文](https://arxiv.org/abs/2610.06617)

- **foundation-model**：RealtimeWAM以teacher10步endpoint的interval velocity锚定CD，λ=.2等价1/t² endpoint权重，frozenvideo共享KV只LoRA action；CUDA双stream每层KV projection后event、action attention才wait的wavefront保持依赖。LIBERO/RoboTwin/Plus及同训练distill控制，延迟含VAE不含episode一次文本。
  核查位置：§4.1式6–9；§4.2式10–13；§5.1–5.4

**2610.06616 · Video Encoders Built on Image Representations**

[论文](https://arxiv.org/abs/2610.06616)

- **foundation-model**：image-first视频输入保留源位置，固定token预算下DPP/跨帧关联选择加可选18M时序refiner；Appendix C.1训练自由对照已隔离额外训练。
  复现边界：固定输出token不等于全路径零开销；refiner训练65K VideoChatGPT过滤后两epoch96 A100 GPU小时；本文报告不替代仓库GPU收据。
  核查位置：§2–3；§4.1–4.4/Table1/Table2；Appendix C.1–C.3/Table4/Table5

**2610.06611 · Lens3D: Target-Conditioned Visual Foveation for Fine-Grained 3D Understanding**

[论文](https://arxiv.org/abs/2610.06611)

- **foundation-model**：Lens3D先grounder目标box→depth-visible voxel增量coverage选多视图并wireframe标注→2DVLM；LensDistill privileged teacher caption监督native3DLLM+目标center，无test额外view/VLM。LensBench2068object/141valscene与561train分离但reference为3模型silver，100object人评；GTbox版本不得混作端到端grounding。
  核查位置：§3.2式3–5；§3.3–3.4式6；§4.1 Tables 1–2

**2610.06598 · SimForcing: Distilling Simulation Motion Priors into Real-Domain Robot World Models**

[论文](https://arxiv.org/abs/2610.06598)

- **foundation-model**：SimForcing动作条件视频worldmodel，真实轨迹sim重放扰动训teacher，pairedsim/real同noise/time的相邻cleanlatent差L2蒸馏；逐block zero-initconv simcondition按样本共享dropout并噪声腐坏。Bridge/InternData视频质量及LIBERO下游，世界预训练不预测动作，sim侧刻意排除objectinteraction不能夸大为学通用物理。
  核查位置：§3.1–3.3式1–12；§4.1–4.3；Appendix A

**2610.06479 · Behavior-Preserving KV Cache Compression**

[论文](https://arxiv.org/abs/2610.06479)

- **foundation-model**：Behavior-Preserving KV 以全缓存下一token分布为目标，投影删除扰动经最终norm Jacobian/LM head近似到logits，用singleton候选池和mask-level边际KL贪心优化缓存。
  复现边界：残差直通传播是近似，不能宣称精确输出保真；仅使用可见prompt尾或已生成query，不能读取未来答案。预填充仍需全缓存，选择开销更高；正文仅找到kvpress基线链接，未找到作者实现。
  核查位置：§4.1–4.4 Eq1–8；§5.1 / Table1；§6；Limitations

**2610.06454 · AgentPrivArena: Evaluating and Auditing Real-world AI Agent Privacy**

[论文](https://arxiv.org/abs/2610.06454)

- **agent**：AgentPrivArena/AgentPrivAudit 在六个容器服务中做389可执行隐私任务，读后提取来源/主体/接收方信息流、写前Pass/Abstract/Block，可作为真实工具状态评测与防护策略候选。
  复现边界：493来源只转成389，群聊缺失造成覆盖偏差；分数来自2/3模型judge尚未人工核验，fail-open不能作为对抗安全保证。敏感原观察仍进模型，不是隔离机制；公开MIT代码，PrivacyLens需单独按上游许可准备，所有记录合成。
  核查位置：§3.1–3.4；§4.1–4.2；§5；Limitations/Ethics；official README

**2610.06446 · The Assistance Dilemma: Learning to Teach via Multi-Turn Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.06446)

- **foundation-model**：Eduardo教学多轮RL奖励设计，由post-training track审查。
- **post-training**：tutor无gold solution；masked近迁移post-test只保留学生tokens，配合correctness/no-handover gate；冻结学生与跨benchmark评估。

**2610.06439 · Better Call Reward: Reward Hacking as Strategic Abstention in Legal Reasoning Models**

[论文](https://arxiv.org/abs/2610.06439)

- **post-training**：公开reward hacking诊断入口：LegalBench16任务分离surface proxy、真实可解析正确性、CTS与滚动GDM；Apache-2.0仓库有notebook与结果。刻意错误proxy训练用于检测format/abstention坍塌，不得宣传为能力改进。

**2610.06413 · SpatialChain: A Benchmark for Auditing Spatial Reasoning Faithfulness in VLMs**

[论文](https://arxiv.org/abs/2610.06413)

- **foundation-model**：SpatialChain用GQA scenegraph生成/answer过滤28,350train+899test CoT，评测模型输入image/question，judge可读GT graph评AC/RF/RC；surface overlap不证明faithfulness，RF是graph一致性非模型因果忠实性。官方data+eval+judge CLI齐全，可作公共评测；需把gold/reference与agent隔离。
  核查位置：§3.2–3.3；§4.1–4.3；§5；Appendix L；官方README；README Dataset/Repository Structure/eval/judge

**2610.06406 · What Did the Agent Actually Do? Evidence-Grounded Oversight for Long-Horizon Agents**

[论文](https://arxiv.org/abs/2610.06406)

- **foundation-model**：EBG和AgentMonBench用于长程agent监督，应由agent track审查。
- **agent**：EBG确定性证据→行为→scope图、需求驱动一跳扩展及原文回核；AgentMonBench分离遗漏规范、测试不变语义替换和事后反馈前缀，接受监督机制与条件性公共评测候选。
  复现边界：FeedbackTrace以之后pushback选样但监控不见后续，属于选择性监督任务非实时发生率；EHR只需命中一证据不是完整充分性；Codex5case非因果一般化证据。公开Drive输入入口存在但此环境未列出档案，完整冻结数据下载未验证；dataset-specific release terms pending，上游CCBY/ODCBy需分别遵守；不得宣称benchmark已执行/全部许可无条件。
  核查位置：§3.1–3.4; §4.1–4.3 Eq1–2; §5.1–5.2; AppendixD.1/F; official README/dataset_card

**2610.06404 · Quantifying the Stability of Multi-Step Reasoning via Error Amplification**

[论文](https://arxiv.org/abs/2610.06404)

- **foundation-model**：随机有序子采样CoT步骤与STE量化感知SFT组合，降低step-to-step误差放大；CLRS-Text/LEGO上可复现实验及Jacobian诊断。
  复现边界：不是直接Jacobian罚项训练；2000train/200val/200test，λ和bits只val调。10%长度外推主结果，20%所有方法低于25%，不能宣传长推理普适提升。图算法/符号7任务和Qwen1.5B，非开放文本证明。
  核查位置：§3 error amplification；§4 Algorithm1；§5.1/Table1；Appendix B

**2610.06324 · Readout Blindness: VLM Scores Miss the Spatial Direction Their Frozen Encoders Retain**

[论文](https://arxiv.org/abs/2610.06324)

- **foundation-model**：ADR冻结encoder patch/独立词特征做Sinkhorn excess coupling或dense定位质心，再根据解析subject-object关系轴作有符号位移；无新训练且context-free/unary盲性定理有前提，不能泛称所有VLM encoder无法方向。九模型五direction-balanced集，derangement null校正grounded gain抵消语言prior；适合readout方法与diagnostic evaluator。
  核查位置：§4 Theorems；§5 Algorithm 1；§6；§7 Tables 1–2；Appendix D

**2610.06286 · DeferKV: Rethinking Eviction Timing for One-Shot KV Cache Compression**

[论文](https://arxiv.org/abs/2610.06286)

- **foundation-model**：DeferKV 等首个真实生成token进入decode获得query后再压缩prompt缓存；将其与尾部prompt query按时间折扣融合，沿用底层方法的平滑/预算/选择。
  复现边界：首个decode前仍需全prompt KV；额外生成token的KV须保留。η=0.7来自LongBench敏感度实验，本地应单独验证选择；不默认适配MLA/混合线性状态缓存。
  核查位置：§4.1–4.3 Eq6–9；§5.1；§5.4–5.6 Table4；Limitations

**2610.06269 · Evolving in Thought Space: Training a Small Model at Test Time Unlocks Better Discoveries**

[论文](https://arxiv.org/abs/2610.06269)

- **agent**：Guidance-TTT仅训练小guidance LoRA，用archive parent summary提策略、冻结executor读完整parent落实、独立verifier给reward；adaptive entropic LOO advantage+centered base correction的实际RL闭环，接受高优先evolve候选。
  复现边界：多数最佳search结果不等于跨任务泛化；固定program三/五重复的std非独立训练seed；TriMul历史archive baselines与新配对timing不能混合置信区间。GPTOSS同executor成本比较83.19低于TTT83.72，是便宜但略低分。官方README明确paper records是历史结果非当前port新运行；H100结果不是本地A100验证。
  核查位置：§3.1–3.4; §4.1–4.3; Appendix A.3/C.4–C.5/D.3; official guidance-ttt-support recipe README/LICENSE

**2610.06226 · LeAVJEPA: A Minimalist Architecture for Audio-Visual Self-Supervised Learning**

[论文](https://arxiv.org/abs/2610.06226)

- **foundation-model**：LeAVJEPA以共享早期融合ViT、模态专属局部视图、对称不变性与SIGReg构成可训练视听JEPA；附录C.3表A3同编码器/30epoch/批量512的控制实验证实局部视图机制。仅接受为研究候选，不宣称SOTA或已复现。
  复现边界：多项为单次训练；原始视听数据可访问性需实现前确认；本次官方页面未找到作者代码链接。
  核查位置：§3.1–3.4；§4.1–4.4/Table2/Table4；Appendix B.1；Appendix C.3/TableA3

**2610.06193 · Correct Code, Broken Contributions? SWE-CC: Benchmarking Repository Policy Compliance for Coding Agents**

[论文](https://arxiv.org/abs/2610.06193)

- **agent**：SWE-CC 将12个SWE-bench仓库的823条贡献政策编译成有前置条件的确定性检查器，同时评估轨迹与补丁，适合作为代码Agent合同评测候选。
  复现边界：合规率必须联报触发率、withheld和功能成功率，少做任务不能冒充更合规。150个人工抽审平均接受87.2%，未经人工修正的checker有错误；文档版本与任务历史版本需绑定。官方MIT发布任务、checkers、runner和8千次outcome，但没有完整历史轨迹，不能独立复判所有旧运行。
  核查位置：§3.1–3.5；§4.1–4.2；Appendix B/D；official README

**2610.06192 · Copies or Sources? Measuring How LLM Aggregators Count Restated Evidence in Multi-Agent Systems**

[论文](https://arxiv.org/abs/2610.06192)

- **agent**：用精确Bayes可数来源任务测复制证据权重，比较去重声明、抽取唯一读数、只转发引用三种通信干预，可加入多Agent证据聚合诊断。
  复现边界：抽取多一次模型调用且可能漏证据；引用须能解析到原始来源，层级摘要仍重复，不能靠声明假定相互独立。Web文档摘要复制消除较弱，真实复杂知识任务收益尚未建立。
  核查位置：§2–3 testbeds；§5.1–5.3；Appendix G prompts

**2610.06191 · Judged Useless, Queried Anyway: Tool-Using Agents Rarely Turn Their Own Evidence Judgments into Stopping Decisions**

[论文](https://arxiv.org/abs/2610.06191)

- **agent**：根据Agent自身USELESS判断累计失败检索，在连续五次无用时由harness触发整合/停止；固定步数对比和新300题确认，适合工具预算控制候选。
  复现边界：side-channel判断额外3–5次调用应计费，keyword reader只部分模型有效；阈值针对最多三次恢复的模拟故障，晚恢复会过早停止。gold只供评测不得用于停止信号；离开工具后凭记忆回答仍需安全/准确性检查。
  核查位置：§2 setting；§5–6；Limitations；Appendix D

**2610.06161 · Introducing Code-Switched Contexts to Cognitively-Inspired Bilingual Model Training**

[论文](https://arxiv.org/abs/2610.06161)

- **foundation-model**：字典/POS受控code-switch与四阶段密度课程是可执行数据增强候选，适合小型双语预训练机制诊断；必须同时保留英中退化负结果。
  复现边界：只英荷/英中小尺度，英荷收益而英中grammar/translationretrieval下降；不能称普适跨语言提升或认知忠实模型。词典/POS噪声和word/token预算区分需显式记录；未找到作者源码链接，独立实现保留语料版本与词典构建预算。
  核查位置：§3.1–3.2/Table1；§4–5；§7/Limitations；App A/B/D

**2610.06147 · Efficient Test-time Adaptation through Candidate Verification and Divergence Shifts**

[论文](https://arxiv.org/abs/2610.06147)

- **foundation-model**：TTC候选memory子空间稳定性校正，公开代码/特征包使其适合作为无梯度VLM适配候选。
  复现边界：Table5预提features且无augmentation，是适配阶段而非端到端2x；top3外准确率必0，受伪标记memory污染/空类coldstart限制。labeled train memory与label-free协议不得混报，test_l只用于最后评分。
  核查位置：§3 Eq1–8；§4.1/4.3/4.4；App B/C/D；作者README

**2610.06100 · From Traces to Agentic Worlds: Agentic Language World Models for Interactive Environment Simulation**

[论文](https://arxiv.org/abs/2610.06100)

- **agent**：Trace2Env从trace构造冻结worldbook，区分跨episode知识、当前state与逐步memory；适用性gate、schema/约束验证分阶段commit，配真实环境重放W2R评测，接受世界模型/Agent环境候选。
  复现边界：gate只schema/约束而非真实转移证明；模型提案合法即接收，拒绝时清effects但仍返回原observation，可能状态叙述不一致；所有主表single run，judge失败样本排除需coverage。除Terminal外冻结worldbooks/原traces/results多为on-request，可重采样但非精确复现；SciWorld建模用goldpath只限构建train，不得给测试taskagent；CR不是逐轨迹一致性概率。
  核查位置：§4.1–4.3 Eq3–8; §5.1–5.4 Tables1–3; AppendixC.3 Table13; official REPRODUCING.md

**2610.06064 · TrustMI: Causally controlling how assistants trust their users**

[论文](https://arxiv.org/abs/2610.06064)

- **agent**：TrustMI以冻结LM的全层BiPO steering矩阵+正向trust NLL抑制likelihood displacement；用户span和assistant span分别训练，Agent主实验把user-trained矩阵加到所有用户及工具输出。接受Meta高优先安全机制及公共评测候选。
  复现边界：仅用户span steering反而提高Qwen注入ASR；必须包括tool spans。moderate α能力平均近似保持不等于每子任务无损；α/γ等需另设validation，原文仅1800/200未明确独立调参集。因果activation干预不证明唯一纯trust心理变量；相关doubt/sycophancy未解耦，judge替换不可直接比较原benchmark绝对分。
  核查位置：§3–6；Appendix B/C/D.3–4/D.6/E；官方README、LICENSE/数据许可

**2610.06026 · Differentiable Bit-Widths: Co-optimizing Pruning and Quantization via SVD for Ultra-Efficient LLM Compression**

[论文](https://arxiv.org/abs/2610.06026)

- **foundation-model**：DBW按SVD分量学习含0的位宽，STE加Hamilton剩余位分配、矩阵级预算和奇异值熵正则，联合剪枝与低比特量化。公开训练/评估实现适合压缩算子候选。
  复现边界：4096×2048 RedPajama校准、1.61bpw与group128；需统计U/V尺度和真实packed存储而非fake quant。64token时多GEMM启动不如OmniQuant快，长序列优势不能泛化成低延迟decode。GPU训练和内核须独立A100/A30验证；官方许可未在首页明确。
  核查位置：§2.2/Eq1–4/Algorithm1；§2.3；§3.1–3.2；official README

**2610.06021 · Scalable Minimal-Change Learning for Controllable Image Editing**

[论文](https://arxiv.org/abs/2610.06021)

- **foundation-model**：Arro VLM分别审计未实现/意外变化，group内LLM去重统一rubric再VLM Boolean核验，负count两channel独立标准化→加权→batch重归一后flowGDPO；不是简单单reward求和。MinEval10k/600disjoint另MagicBrush/AnyBench/EmuEdit，模型judge分数非生产AB，需计group auditor预算与外部judges。
  核查位置：§3.2–3.4式4–8；§4.1–4.4；Appendix B/E/F
- **agent**：ARRO以VLM列出未实施与意外修改，再用组共享原子rubric二次审核，分别group-normalize两通道奖励并batch-renormalize优势，以flow-GDPO训练编辑器。适合多模态后训练/Agent reward跨轨收录。
  复现边界：约10K MinEval训练与heldout分离；EditScore与分割OffTarget-L1依赖judge/perception，不能当完整语义正确率。单训练种子且未建立diffusion迁移；约束保留Kontext真实训练，启发式audit只能诊断。
  核查位置：§3.2–3.4；§4；§5 Limitations；Appendix B/E/F

**2610.06001 · AgentSpy: Making AI Agent Behavior Observable**

[论文](https://arxiv.org/abs/2610.06001)

- **agent**：AgentSpy 在隔离microVM外记录进程树系统调用/网络，再按命令、文件、主机的归一化计数构造star graph与weighted Jaccard，可作为独立可观测性机制候选。
  复现边界：77/87任务、三次运行；超时选择性重试/丢弃会改变样本。资源相似不代表任务正确、读取skill不代表使用知识；RQ2作者在指标可见下标注，非盲验证。安全五类只检测四类，不能宣称完整防护。Linux microVM/内核权限需独立验证，所有监控仅限授权沙箱，源码入口未在原文找到。
  核查位置：§3.1–3.4；§4.1–4.2；Threats to validity；§6

**2610.05994 · How (and How Not) to Use Data Augmentation in VLA Post-Training**

[论文](https://arxiv.org/abs/2610.05994)

- **recommendation**：VLA 数据增强为具身基础模型方向，已转基础模型审查。
- **foundation-model**：VLA PPO critic-only图像增强在clean actor/rollout上通过advantage影响策略，是真实可复现训练干预；可作后训练/机器人研究候选，不是工业推荐结果。
  复现边界：critic-only需要额外backbone forward，matched epochs不等FLOPs；每配置一个训练seed，重复同checkpoint评估不是训练重复；最佳增强类型/强度应另设validation，仿真结果不等真实机器人。
  核查位置：§3/Table1；§4/Tables2–3；§5；Limitations
- **post-training**：使用既有PPO/Flow-SDE比较augmentation placement，贡献是critic-only增强经验规则，而非新的RL/OPD核心算法。

**2610.05993 · From Transformation to Target State: Rethinking Query Representation for Zero-Shot Composed Image Retrieval**

[论文](https://arxiv.org/abs/2610.05993)

- **foundation-model**：ASAP-CIR冻结MLLM把reference+edit重构多holistic静态target描述与weighted atomicfacts，CLIP global及patchsoftmax匹配分别query-wise zscore融合。FashionIQ val/CIRR test1/CIRCO test，无任务训练但有dataset-specific prompts，不能称无任务设计/无额外MLLM成本。
  核查位置：§3.2式1–3；§3.3式4起；§4.1–4.4

**2610.05981 · Mechanizing the User's Eye: Pre-Registered Deployment of a Sabotage-Validated Fail-Plausible Observer in a Production LLM Agent Runtime**

[论文](https://arxiv.org/abs/2610.05981)

- **agent**：接受小规模Agent可靠性回归基准：五确定性signals→带verbatim substring证据闸门的LLM judge；14例公开offline corpus+逐detector sabotage+固定manifest/评分器，适合evolve防退化diagnostic而非通用能力分。
  复现边界：24 incidents中16结构不可见；规则由历史例设计，CategoryA是回归非泛化；4个heldout太小，不能让优化器看gold/期望signal。官方仓库修正旧约70%user发现为13/22=59%，论文继承旧数，引用必须标版本。无独立标注，2/14日缺失；公共runner未在本轮执行。
  核查位置：§3–5 Tables1–3；§6 Table4；§7 Table5；§9；官方docs/fail_plausible_bench.md与LICENSE

**2610.05978 · Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation**

[论文](https://arxiv.org/abs/2610.05978)

- **foundation-model**：Byte模型256vocab+hash ngram/DeltaNetconv16+前30%四byte TST后70%NTP，与subword做IsoFLOPs而非相同text exposure；late-layer pooledspan干预为诊断，200M分段模型不可省略。speculative仅给定evaltext的oracle simulation非真实decoded latency，不能把3.4×接受token当3.4×提速。
  核查位置：§2.1–2.4；§3.2；§4.2/Table 3；Appendix G

**2610.05940 · ReMem: Streaming Video Understanding With Long Context Retention**

[论文](https://arxiv.org/abs/2610.05940)

- **foundation-model**：ReMem训练外SCM以固定generalquery注意力选择递归压缩、保留RoPE原位+时间offset；RVM clip pooledkey与query向量cos检索topclip，有限FIFO淘汰，非无限无损记忆。Streaming/OVO/长视频与NIAH；r=.7在StreamingBench SQA选择，正式复现必须重建validation并不能把调参集成绩作为独立test。
  核查位置：Methodology/SCM/GQC/RVM式1–3；Experiments；Appendix A compression-ratio study

**2610.05935 · ThunderSyncRL: Lossless Acceleration of Agentic Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.05935)

- **post-training**：ThunderSyncRL用固定策略版本、GRPO双梯度累积和OPD按token延迟归一化在单次optimizer barrier前流式计算，数学更新等价；B200/H200数值核查和真实agent训练，不应把异步陈旧梯度代理当复现。
- **agent**：ThunderSyncRL用固定策略版本、GRPO双梯度累积和OPD按token延迟归一化在单次optimizer barrier前流式计算，数学更新等价；B200/H200数值核查和真实agent训练，不应把异步陈旧梯度代理当复现。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§3.3–3.4 Eq.1–9；§4

**2610.05897 · Fitting Vision Adapters at Frontier Scales**

[论文](https://arxiv.org/abs/2610.05897)

- **foundation-model**：仅约50M vision projector连接冻结encoder/reader，sharedvocab affine embedding对齐初始化、SFT空think后仅adapter CISPO image-math RL恢复reasoning，正reward需非空reason/answer。Qwen4–32B同recipe可控，550/743B MoE训练/奖励不同不能规模因果比较；blind/图像破坏验证是关键。
  核查位置：§3.1–3.3式3–5；§4.1–4.4；Appendix A.2/C

**2610.05896 · TasteRoute: Personalized Routing for Video Generation**

[论文](https://arxiv.org/abs/2610.05896)

- **foundation-model**：TasteRoute frozen request embedding+generator/user embedding与交叉特征，BTpairwise+ordinalquality，general五fold prompt隔离、personal每annotator独立train/val/test且userdropout.4；不生成video直接预算内排序。仅9annotator/3128video，冲突偏好准确55.2%增益有限，不泛化到大众用户，oracle verifier结果不可作可部署能力。
  核查位置：§4；§6.1–6.2式1–3；§7；§9.2

**2610.05885 · The Optimization Landscape of Learning Compacted Context Models**

[论文](https://arxiv.org/abs/2610.05885)

- **foundation-model**：Fast Diamond简化Perceiver KV writer有明确单次/递归压缩及预算对照，保留为学习型KV压缩算法；正文readout矛盾已由canonical附录解读为frozen并显式记录。
  复现边界：§5末句leave trainable与前文frozen及AppA冲突，必须以canonical冻结契约并保留偏差注记；code/data承诺camera-ready未公开，医学OOD固定集需补资源；16/32k反复压缩弱于StreamingH2O；归一utility非原始acc，不能把questionexcludedbudget作总内存。
  核查位置：§2–5；§6.1–6.3；§8；AppA Table2/G Fig20

**2610.05879 · Learning to Learn a Language**

[论文](https://arxiv.org/abs/2610.05879)

- **foundation-model**：PFLM以每序列新采样的recurrent SCM先验进行byte-level预训练，再冻结权重从长前缀学习预测；核心数据生成定义与300M模型/权重公开，属于基础模型新训练范式候选。
  复现边界：BPB跨语言UTF8字节成本不同，不能当语言理解排名；未胜现代自然文本LM，数值任务大量shots不等零样本。官方repo核实model/HF integration/stream scoring，未证完整SCM生成/训练pipeline已释放；若复现训练须精确AppA prior不能用任意随机串替代。
  核查位置：§2.1–2.4 Eq1–3/Table1；§3–4 Table2；App A/B/D；official README

**2610.05872 · Off-Policy Merging Beats On-Policy Self-Distillation for Continual Learning**

[论文](https://arxiv.org/abs/2610.05872)

- **foundation-model**：以离策略donor微调增量、retention Fisher/KFAC敏感方向投影与缩放合并到当前模型，Qwen/OLMo持续学习验证；不同于2610.00767信念移植及旧GRAFT2609.37868轨迹交换。
  核查位置：Abstract（输入检索工件中的完整摘要已逐条审阅）；§4 Algorithm 1；§5
- **post-training**：以离策略donor微调增量、retention Fisher/KFAC敏感方向投影与缩放合并到当前模型，Qwen/OLMo持续学习验证；不同于2610.00767信念移植及旧GRAFT2609.37868轨迹交换。

**2610.05861 · Imagine to Act: High-Fidelity Data Synthesis via Image Editing World Model for Scalable GUI Agent Training**

[论文](https://arxiv.org/abs/2610.05861)

- **foundation-model**：Infinite-Dreamer训练时从before/after/action/nextaction提delta；合成时AppDesigner text→delta驱动FLUX2Klein截图编辑，VLM筛step后SFT GUIactor。worldmodel AndroidControl train/val，actor仅合成、AndroidWorld/MobileWorld在线评；合成可用future设计但评测agent不能读gold nextstate/plan，worldmodel并非真实应用状态机。
  核查位置：§3.2–3.5式1–8；§4.1；Appendix A.5/A.6

**2610.05842 · HLA: Expressive Hybrid Linear Attention via Chunk-Wise Dynamic Mixing**

[论文](https://arxiv.org/abs/2610.05842)

- **foundation-model**：HLA以query gate对完整chunk仿射GDN transition作identity插值并按时序复合，核心不同于固定state加权，适合长上下文结构operator。
  复现边界：历史chunk状态随序列增长，不是常量memory或比原GDN更快；2x省存对tokenKV且未含所有router/activation；chunk/pool按LongBenchV2最优且trainp16evalp32需validation复核；静态任务，额外模块预算非FLOPs匹配。
  核查位置：§3 Eq1–13；§4.1；§4.2–4.3 Tables1–4

**2610.05833 · Request Order Matters: Cache-History Sensitivity in Selective KV-Cache Reuse for Rolling Agents**

[论文](https://arxiv.org/abs/2610.05833)

- **agent**：接受Agent长时rolling context的KV重计算机制诊断：固定5% token预算，按doc均值deviation选择整span及连续余量；对照token-top-k和其他连续块，核心证据支持contiguity而非document边界/评分本身。
  复现边界：仅逐字复制current文档的合成rolling任务，非真实Agent能力提升；chronological fullprefill fidelity86.8vs85.4无显著差异，reverse doc仅54.3%；latency仅prefill非端到端。未发现作者代码/完整工作负载发布，原数字复现受限；接受独立机制验证，不冒充论文完整复现。
  核查位置：§2.2–3 Eq1与document-aligned selector；§4设置；§5 Tables1–4；§6

**2610.05778 · MedicalHarness: A Controlled Evaluation of LLMs and Agent Harnesses on Medical Tasks**

[论文](https://arxiv.org/abs/2610.05778)

- **agent**：MedicalHarness 的MH-Lab在相同执行循环中切换摘要、显式计划和工具发现接口，并将回答率、正确率、轨迹和成本分开；公开代码/MedTool可作为harness消融候选。
  复现边界：107任务三seed，grader/gold隔离，bootstrap按任务；产品harness对比不是完全单因素，MH-Lab才是组件控制实验。MedMemory病历文本私有且单独提供，不能标整套107任务可公开复现；MedWeb等需上游资产与条款，官方smoke使用脚本响应不是模型能力。只离线研究，不做临床部署。
  核查位置：§3–6.1；§6.3/7；Appendix C/D/H；official README

**2610.05774 · AdaSpark: Adaptive DSpark with Online Learning for Tree Verification and N-gram Fill**

[论文](https://arxiv.org/abs/2610.05774)

- **foundation-model**：AdaSpark将DSpark候选与请求内ngram合并，按路径接受概率排序合法树前缀，用在线低分位延迟模型和接受率模型选择验证宽度；可作为推测解码控制器候选。
  复现边界：贪心而非任意sampling保证；空store冷启动55–67轮成本计入，跨请求持久化需绑定硬件/权重/内核。42会话95回复，循环到cap和单delta回复部分剔除；主增益含引擎优化，在线宽度仅打平最优固定宽度，不能全部归因新调度。官方Rust Metal/CUDA/CPU版本多变需pin。
  核查位置：§3.1–3.4；§4.1/4.5–4.6；§5；official imparo README

**2610.05744 · CIPHER-MoE: Balancing Efficiency and Routing Fidelity in Trillion-Scale MoE Training**

[论文](https://arxiv.org/abs/2610.05744)

- **foundation-model**：CIPHER-MoE保持tokenTopK，专家端cosine affinity与capacity admission加locality loss，区分严格drop与reroute，有真实大规模SFT效率/质量证据。
  复现边界：定理依赖球面/条件recall假设仅保证信号保留非质量；zeroassignment梯度及weight renorm实现必须严格还原；code正文willrelease未公开；非工业在线AB结论、不能把1.6T OOM对比当数值speedup。
  核查位置：§3.2 Eq4–10；§4 Tables2–3；AppA.4/A.5

**2610.05715 · Rotated, but How Far? Diagnosing and Improving Object-Rotation Reasoning in VLMs**

[论文](https://arxiv.org/abs/2610.05715)

- **foundation-model**：RotationCue 使用三个可学习关系查询，顺序预测对象同一性、旋转存在与角度范围，将条件化角度提示注入冻结 VLM。ALOI/ModelNet40 可构造训练，OR-Bench 为对象隔离的完整测试集。
  复现边界：Oracle 角度提示仅诊断；方位旋转不是二维图像旋转；应保留对象级隔离和打乱提示对照。
  核查位置：§3–5.4; Appendix F/H

**2610.05709 · Nexus: An Execution Fabric for AI Agents Across Cloud, Edge, and Devices**

[论文](https://arxiv.org/abs/2610.05709)

- **agent**：Nexus将调用持久化为task，使用invocation-scoped委托、operation journal、device receipt及cursor恢复，明确已提交结果重用与不确定外部副作用的资源端协调。接受执行基础设施候选。
  复现边界：单宿主OpenWrt/Android虚拟化控制实验，各机制未在一个版本端到端组合；24 paired任务中22共同成功延迟比较，不能忽略失败。Cloud admission/settlement仍中心依赖，CPU ceiling下降非实际商业成本；重复副作用抑制需资源配合。
  核查位置：§3–4；§5.7；§6.1–6.3；Software and Documentation；Appendix D/E

**2610.05697 · From Token-Max to Outcome-Max: How You Use AI Determines Its Productivity**

[论文](https://arxiv.org/abs/2610.05697)

- **agent**：TokenEcom按verified output/cost而非token量设模拟监督策略，跨代只传递可重用playbook，执行反馈提炼双方skill。公共SWE/HumanEval/GSM8K/MATH适合cost-aware evolve评测候选。
  复现边界：人类由LLM模拟，directive同时改变停止行为，不能孤立归因纯奖励；310 matched主SWE对中hard任务正确率下降。skill20训练15heldout且100validation，gold仅外部评分；经济账户/审计罚款是假设，不是真实工作场所因果证据。
  核查位置：§3–5；Appendix A.5 Algorithm1；C/D

**2610.05685 · Spend Bytes on Breadth: Precision-Count Trade-offs for Decode-Time KV Compression in Long Chain-of-Thought Reasoning**

[论文](https://arxiv.org/abs/2610.05685)

- **foundation-model**：BreadthKV在相同decode KV字节预算下联合KIVI量化和SnapKV-D淘汰，以独立AIME22–23校准位宽，研究更广低精度缓存优于少量高精度缓存。
  复现边界：prompt保留且不计预算，fp16残差128–191token，预算误差约5%须另报实际memory-time；R1-Qwen AIME24是开发集而非测试。只有单sampling seed；内核H200一层一step并未端到端更快，int2反而慢。公开代码入口正文未找到，独立实现需保持真实packed量化与校准/测试分离。
  核查位置：§3 Eq1；§4–5.1；§5.7/kernel；Limitations；Appendix A/B

**2610.05664 · StageVLN: Spatial and Trajectory Auxiliary Guidance for Efficient Vision-Language Navigation**

[论文](https://arxiv.org/abs/2610.05664)

- **foundation-model**：StageVLN多层current-image cosine对齐冻结geometryteacher，历史相对heading sin/cos与expert forward步比例progress辅助训练，pre-action hidden避免teacherforce读GT当前action。jointR2R/RxR train、valunseen，推理去teacher/projectors/heads；progress不是成功率也不是STOP规则。
  核查位置：§III-C式2–5；§III-D式6–12；§III-E；§IV-A–D

**2610.05637 · Visual Grounding Safety in Vision-Language Models**

[论文](https://arxiv.org/abs/2610.05637)

- **foundation-model**：grounding safety以相同intent VQA/定位匹配评测，SFT混harmfulrefusal+有中性证据的benignselfdistill+1548capabilitygrounding；plain和placeholder格式分别训LLM。最终坐标/回答而非think判refusal，定位失败也可能假安全故单列PointArena能力/overrefusal；placeholder非真实可执行坐标。
  核查位置：§2.1–2.3；§3.1–3.4 Table 3；Appendix A

**2610.05630 · Atomic Visual Entailment: Enhancing Zero-Shot Vision-Language Reasoning through Atomic Fact Decomposition and Learned Selection**

[论文](https://arxiv.org/abs/2610.05630)

- **foundation-model**：AVE冻结Decomposer原句拆atoms，两VLM direct/atomic候选pool；XGBoost以labelscore/entropy/agreement等meta预测最终label，非必选pool已有label，再取代表justification GroundingDINO定位。47,203train中20%val选后固定SNLI-VE dev/test，94%oracle不能当部署结果；Flickr30kEntities是近似证据定位非完整faithfulness。
  核查位置：§3.1–3.4；§4.1；§4.3–4.6

**2610.05622 · UndoBench: Separating Task Competence from Recovery Capability in Tool-Using AI Agents**

[论文](https://arxiv.org/abs/2610.05622)

- **agent**：UndoBench 对相同seed执行control/fault配对试验，以独立mutation log与state oracle区分能力、恢复、重复和漏执行，适合工具Agent容错评测。
  复现边界：36工作流14/10/12开发验证测试，20seed仍只有12独立测试cluster。主实验只单次lost-ACK，其他边界是后续扩展；CRSR零control成功时必须N/A。EvoUndo零权限约束不代表其完整能力，B6是事后对照，EOR由日志事后重算。只能本地模拟API，不连接真实支付/生产服务；冻结版本而非读取最新变化。
  核查位置：§2–3；§6；Limitations；Appendix G/K/L；official README

**2610.05615 · DREAM: Dynamic Resolution Assignment For Multimodal Multi-agent Debate**

[论文](https://arxiv.org/abs/2610.05615)

- **foundation-model**：DREAM多agent辩论动态视觉分辨率，由agent track审查。
- **agent**：DREAM用多分辨率probe的ANLL均值减标准差形成confident set，五分支分配visual payload；丢弃probe历史后debate，按每agent ANLL轨迹回滚早期低不确定答案，再judge。适合多模态Agent推理候选。
  复现边界：500例每benchmark、3推理seed；probe全响应logprobs真实计算，不能用伪置信度。α=.5在同测试benchmark sweep最优，与无tuning说法冲突，须validation重选。tokens增加，非节省总成本；LLaVA Div-MAD例外下降。代码仅承诺发布，未找到现有repo。
  核查位置：§3.2–3.3 Eq3–4；§4–6；Appendix A/B/F/G

**2610.05572 · Disentangling Task Difficulty from Run-Level Failure in Agent Failure Prediction**

[论文](https://arxiv.org/abs/2610.05572)

- **agent**：分解pooled AUROC为同任务/跨任务比较，以task-grouped交叉验证和绝对turn prefix区分任务难度与当前run失败信号，适合统一预算控制评测。
  复现边界：oracle历史难度和半合成监控只诊断；按最终轨迹比例截断泄漏未来长度。早停相对预算分配无显著收益，阈值0.84–0.93不是通用规律；干预是recorded replay而非live，不能宣称已改善Agent。
  核查位置：§4.2–4.8 Eq1–2；§6.2–6.3；§7 scope

**2610.05563 · G-CARB: Graph-Localized Conformal Agent Risk Budget for Compositional Harm**

[论文](https://arxiv.org/abs/2610.05563)

- **agent**：CARB对stopped-prefix全episode harm ledger做finite-grid corrected conformal risk calibration；G-CARB只向固定scorer提供prefix-visible source-to-sink依赖路径，保留proposal空结果与threshold nesting。接受安全门控机制候选。
  复现边界：保证是exchangeable episode期望loss，并非每轨迹安全或shift保证；ledger未独立误差审计。AgentDojo同corpus200重划分percentile非独立CI；equal-size随机context自然数据同等收益，图优势仅构造诊断。record-count节省非tokens/延迟，online64episode仅一致性诊断；未定位代码包。
  核查位置：§3–5 Algorithm1；Appendix B/C/D/G

**2610.05540 · SALUS: Automated Auditing of NL-to-SQL Benchmarks through Weak Supervision of Multi-Agent Output**

[论文](https://arxiv.org/abs/2610.05540)

- **agent**：SALUS对多agent候选SQL执行/结构/intent弱标记建generative label model，均衡高置信伪标签训练SQL-feature条件化agent reliability decision plane，融合verdict检测基准错误。适合评测质量基础设施候选。
  复现边界：human审计298 BIRD-Clean-xs仅评估、训练/选择用弱标签；错误率37%为模型估计非全量gold。stacking65536规则上界明确使用eval gold只能oracle诊断；自动SQL修正只44%Incorrect SQL且不能修复问题歧义/数据错误。保留dev选择与heldout测试，勿由correlated模型一致推论真值。
  核查位置：§3.1–3.4；§4–5.1；§5.6；§6.1；Appendix A/B

**2610.05538 · LiFT: Loop Flow Transformers**

[论文](https://arxiv.org/abs/2610.05538)

- **foundation-model**：LiFT以随机连续深度坐标监督共享DiT核心的逐步速度修正，stop-gradient初始速度锚与prelude辅助损失保留核心机制；同训练token、块设计、执行深度与近等FLOPs的dense对照支持接入研究候选。
  复现边界：B/2所有成本点落后dense，所有LiFT在训练深度也落后；单次训练/样本，只有256图像无CFG。报告的是解析FLOPs非硬件速度。最优循环/采样步数来自公开FID sweep，未来接入须另设validation选配置。
  核查位置：§3.1–3.2 Eq4–9；§4.1–4.6 Tables1–2；Limitations；Appendix D.5.1/Table17

**2610.05532 · DelegationBench: Measuring When AI Agents Should Ask Before Acting**

[论文](https://arxiv.org/abs/2610.05532)

- **recommendation**：DelegationBench 是 Agent 委派评测，已转 Agent 评测基础设施审查。
- **agent**：接受为evolve权限/信息需求分离的评测基础设施；156场景48matched pairs、Act/Ask/Request/Refuse分别计分，Tool-Loop与post-approval测试行动而非只问判断。
  复现边界：无provider客户端，需独立API wrapper；三学生标签为参考非gold真理；工具无持久state；13matched pairs多因素变更；完整raw输出受provider条款未发，explicit-rule研究未发；author notes与reference label严禁给Agent。
  核查位置：§3–4；§5.2–5.4/Tables1–2；§6–7；AppendixO；官方README

**2610.05484 · Universal Test-Time Training**

[论文](https://arxiv.org/abs/2610.05484)

- **foundation-model**：uTTT通过跨层共享快权重池与分离读写路由形成新长上下文算法；同总状态/活跃计算/训练token控制支持核心贡献。
  复现边界：RULER仍低于full attention16.52/34.16；超32K检索衰减；原始实测不替代本仓库A100/A30复现。
  核查位置：§3；§4.1–4.3/Table2；§5.1–5.2；Appendix D–E

**2610.05481 · CodeForge-MA: Execution-Verified Multi-Agent Learning with Language-Conditioned LoRA for Multilingual Code Generation**

[论文](https://arxiv.org/abs/2610.05481)

- **post-training**：PPO+SFT本身是标准配方，但语言条件稀疏Mixture-of-LoRA门控是可执行新增参数机制；Qwen1.8B与72B API实验。应复现路由和辅助约束，非仅重命名PPO。
- **agent**：PPO+SFT本身是标准配方，但语言条件稀疏Mixture-of-LoRA门控是可执行新增参数机制；Qwen1.8B与72B API实验。应复现路由和辅助约束，非仅重命名PPO。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§IV-C–D Eq.12–20；实验配置

**2610.05473 · Hierarchical Reinforcement Learning with Stable Temporal Abstraction for Language Model Agents**

[论文](https://arxiv.org/abs/2610.05473)

- **agent**：STAC在HiPER归一化boundary advantage上按已采样KEEP/SWITCH减去过早重规划与过时保留成本，PPO仅boundary token改变，reward/critic/subgoal/action保持host算法。适合hierarchical Agent RL。
  复现边界：正文实验是固定μshort=μstale=.1、dmin2/dmax8，并未实施adaptive dual/budget保证。最高validation checkpoint及类别成绩在同validation报告，应另设test。3seed区间宽，ablation成功率差异未显著；需真实层级policy训练，不能规则keep切换冒充。未定位新源码。
  核查位置：§2–4 Eq5–11；Appendix A/B/C/F

**2610.05425 · Unmentioned Checklist Findings Change How Reinforcement Learning Appears to Improve Chest Radiograph Report Checking**

[论文](https://arxiv.org/abs/2610.05425)

- **foundation-model**：胸片报告checklist标签协议对RL效果影响，领域评测诊断。
- **post-training**：公开checklist/reader格式稳健性诊断：图像writer不读待查句，checker不读图；matched-label pair和三个checker区分omission/order影响。官方代码/格式/analysis可访问，CheXpert数据须注册协议；医学专门诊断不作临床效益或通用视觉提升证据。

**2610.05418 · EvoMem-VLA: State-Evolution Memory for Long-Horizon Robot Manipulation**

[论文](https://arxiv.org/abs/2610.05418)

- **foundation-model**：EvoMem-VLA冻结paired DINO delta tokenizer，initial+recent+事件state/delta交织记忆，keyframehead预测未来record offset只在时间到达提交；task routing是配置而非learned classifier。训练GTsubtask/test生成subtask有暴露偏差，闭环只读已观测，RMBench/RoboMME+双embodiment80实机episodes。
  核查位置：§3.1–3.4式2–6；§4.1–4.4

**2610.05417 · Render to Reason: Novel-View Semantic Prediction Improves Spatial Understanding in VLMs**

[论文](https://arxiv.org/abs/2610.05417)

- **foundation-model**：Meta Render2Reason以VGGT geometry/camera与视觉crossattention融合，aux新视角16×16九类semantic query并行CE+QA CE，避免teacherforce邻接GT标签捷径；训练target图仅供frozenVGGT提camera，QA推理无target。4B控制实验与8Bsystem不同数据需分开，Appendix A.5有target泄露控制；实现必须维持此边界。
  核查位置：§3.1–3.3式1–3；§4.1–4.3；Appendix A.5

**2610.05402 · Task Vector Descent: Learning from Non-IID Batches**

[论文](https://arxiv.org/abs/2610.05402)

- **foundation-model**：TVD将连续同分布小批更新的task vector部分整合，同时插值Adam一阶矩/步数、平方根空间二阶矩；固定样本预算与训练/评价分离，覆盖SFT及GRPO。
  核查位置：Abstract（输入检索工件中的完整摘要已逐条审阅）；§3.1 Eq.3–4；§3.2–3.3；§4
- **post-training**：TVD将连续同分布小批更新的task vector部分整合，同时插值Adam一阶矩/步数、平方根空间二阶矩；固定样本预算与训练/评价分离，覆盖SFT及GRPO。

**2610.05398 · MMPostTrainBench: Benchmarking Autonomous Research for Multimodal Post-Training**

[论文](https://arxiv.org/abs/2610.05398)

- **agent**：MMPostTrainBench将多模态训练任务封装成Harbor独立verifier，MMResearch把媒体证据、假设、干预结果构成图并配global/core/archive记忆，适合多模态evolve控制器。
  复现边界：原实验Qwen3-Omni30B、8GPU×24h，单卡缩小必须注明；候选test轨迹仅事后审计不可反馈调参。每对三loop但完整审计只抽一个，违规loop回退base不等于全程防泄漏。
  核查位置：§3.2–3.4；§4.1；§4.3–4.4

**2610.05383 · Sibyl: An Efficient Small-large Model Collaboration Framework for Long-horizon Tasks**

[论文](https://arxiv.org/abs/2610.05383)

- **agent**：Sibyl先hindsight skill OPD+RL增强本地policy，失败prefix replay找单次cloud action能逆转结果的decisive disagreement冷启动call_cloud，再以trajectory/matched-state/consultation counterfactual credit联合训练和skill internalization。适合Agent RL/OPD跨轨。
  复现边界：无matched local continuation时cf credit=0；摘要95.2/80.4是绝对success，非同比提升百分比。Seen140/Unseen134、WebShop500官方test，训练需隔离skill/task/validation；成本break-even排除149.7/205.7训练GPUhours。云上下文传输和服务不可用未解决，需真实checkpoint及环境。
  核查位置：§4.2–4.4 Eq9–21；§5；Appendix A/D/F

**2610.05373 · Towards Unbiased On-Policy Distillation for Block Diffusion Language Models**

[论文](https://arxiv.org/abs/2610.05373)

- **post-training**：Un-OPD筛选可见上下文对齐的block决策，对高teacher-support位置混合teacher与detach student logits校准，并复用rollout；真实BDLM实验。标题unbiased不可扩展为任意复用无偏保证。

**2610.05367 · AIProver: Agentic Auto-Formalization of Mathematical Research via Certificate-Driven Evolving Harness**

[论文](https://arxiv.org/abs/2610.05367)

- **post-training**：AIProver交替训练模型与进化harness，SAM双视图对比及CE、证书RLSF和独立fitness集accept/rollback；需真实形式验证链，不得用gold证明fixture替代。
- **agent**：AIProver交替训练模型与进化harness，SAM双视图对比及CE、证书RLSF和独立fitness集accept/rollback；需真实形式验证链，不得用gold证明fixture替代。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§4（SAM与HarnessEvolve）；Table 3

**2610.05342 · IRSTD-Agent: Agentic Infrared Small Target Detection via Zoom-Guided Interaction Learning**

[论文](https://arxiv.org/abs/2610.05342)

- **foundation-model**：IRSTD-Agent红外小目标工具搜索，由agent track审查。
- **agent**：IRSTD-Agent用proposal/zoom/detect/drop/refine视觉工具，基于train mask构造target-preserving/offset-recovery/negative trajectories，SFT预测工具及坐标，测试从native image获得证据。可作为多模态主动视觉Agent候选。
  复现边界：GT只用于训练trajectory/外部评分，不得eval crop oracle。proposal为多空间滤波+FFT无学习，refine image区域连通mask；该工具单独不是MLLM策略复现。27B实际CUDA训练需receipt。Full2000 specialized detector F1更高，agent优势主要Large44原尺寸分组；matched IoU只匹配目标非整体成功。未定位官方源码。
  核查位置：§3；§4；Appendix A.1–A.4/B.1–B.2

**2610.05334 · AgentDiscover: Autonomous Discovery with Minimal Search Scaffolding**

[论文](https://arxiv.org/abs/2610.05334)

- **foundation-model**：AgentDiscover自主发现搜索框架，由agent track审查。
- **agent**：AgentDiscover用sandbox coding agent自行查询idea/candidate/session/lesson图数据库并提交隔离评分，跨session fresh context保留tools/skills；meta agent从trace提炼搜索指导，可接开放搜索evolve。
  复现边界：单run主表无variance；historical AtCoder publiccases搜索/officialsystem测试分开。须保留privatefutureworkload隔离、不返回候选stdout/异常、禁止pickle在scorer反序列化；signalprocessing残余错误metric明确未修，分数不可当真实denoise能力。费用是list-price估算非账单；未找到原创代码公开链接。
  核查位置：§3.2；§4–5；Appendix A/B/C/D

**2610.05318 · Robust Parameter-Efficient LLM Adaptation on Analog Hardware**

[论文](https://arxiv.org/abs/2610.05318)

- **foundation-model**：冻结base用功能等价通道缩放，LoRA用校准异常通道拆分及数字残差累积保留亚阈值更新；可作为模拟硬件误差下的训练机制诊断。
  复现边界：只AIHWKit模拟，异常通道受保护perfect-I/O假设，未量测真实模拟芯片/能耗/通信或延迟。64校准batch固定统计，2000steps、固定512QA与100heldoutNLL；部分消融单点。不得宣称真实analog加速或工业部署。未找到论文官方代码入口。
  核查位置：§3.1–3.3/Eq1–5；§4 setup；§5 limitations

**2610.05308 · RubricArmor: Adversarial Evolution Improves LLM-Based Rubric Generation**

[论文](https://arxiv.org/abs/2610.05308)

- **post-training**：RubricArmor独立质量判断确认满分但有缺陷的攻击，再经降分与独立review双验收迭代修补rubric；有2K WildChat、三policy真实GRPO验证。核心是可执行reward构造循环，须保留验证者非简单字符串rubric。

**2610.05303 · ASCENT: Online Test-Time Training of Long-Horizon Agents via Self-Distillation of Verified Experience**

[论文](https://arxiv.org/abs/2610.05303)

- **foundation-model**：ASCENT在线agent自蒸馏后训练，由agent/post-training track审查。
- **post-training**：ASCENT单次在线episode仅对已验证成功轨迹更新LoRA，以固定初始模型读过滤的自身hindsight作为teacher、forward-KL训练不见hindsight的student；无外部gold答案，须严格prequential协议。
- **agent**：ASCENT单次在线episode仅对已验证成功轨迹更新LoRA，以固定初始模型读过滤的自身hindsight作为teacher、forward-KL训练不见hindsight的student；无外部gold答案，须严格prequential协议。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§3.3 Eq.6–12；§4.1

**2610.05300 · MESH-Harness: Self-Improving Agent Harnesses via Bandit-Guided Compositional Evolution**

[论文](https://arxiv.org/abs/2610.05300)

- **agent**：MESH-Harness固定slot接口与容量池，缓存embedding、full-covariance LinUCB+混合起点coordinate search选择完整组合，每5评估trace驱动两slot变异与evict，保留surrogate统计。可接组合harness evolve。
  复现边界：40次candidate evaluations，3次是同一冻结harness测试重跑而非训练种子；不同初始化影响增益。validation生成/选择后冻结test，LCB private tests仅评分，数学检索433926对须先去评测重复。mean仍加性，full covariance提供联合不确定度，不是任意非线性交互建模；未定位官方代码。
  核查位置：§3–5；Appendix B/C.1/C.3/C.5

**2610.05295 · Readable Before Actionable: Causal Tracing of Indirect Prompt Injection**

[论文](https://arxiv.org/abs/2610.05295)

- **agent**：Readable Before Actionable用content/format反事实role probe、component activation patch和独立hijacked-resisted suite差分方向，检验pre-action/tool-span固定activation edit对AgentDojo攻击行为影响。可收录安全steering实验机制。
  复现边界：role probe权重与edit direction不同，不得以高AUROC直接声称防御。方向由train估计、AgentDojo family-out测试；Llama adaptiveattackASR26.3→27.4无改善，crosschannel不迁移。随layer/context rebound、spanwide多次edit成本需记录；synthetic operating-point选择和正式heldout分开，未定位代码。
  核查位置：§3–7；Appendix Q/V Table23

**2610.05284 · Fusion is the New Mutation: Bandit-Guided Evolution on Workflow Graphs**

[论文](https://arxiv.org/abs/2610.05284)

- **agent**：DAGO将工作流搜索记录为generation lineage DAG，固定五parent组合arm，缓存concat embeddings，shared diagonal LinUCB从退火score-softmax提案中选择fusion；LLM从最强parent开始按总结做targeted融合，绝对子代validation成绩更新bandit。适合harness evolve算法。
  复现边界：DAG是生成谱系不是workflow执行图；diagonal近似既改变coefficients也改变探索，非full-ridge等价或校准CI。100评估含10root与最多30child×3，3次测试是同一冻结harness重跑非搜索seed。六公共任务val/test隔离；81.7 vs 80.3及11.2%搜索成本降幅为macro/aggregate，QA任务成本反升。边仅记录suppliedparent不证明继承；理论受residual/proposal coverage假设约束，无一般sublinear regret保证。未定位官方源码。
  核查位置：§3–5；Appendix B/C/E/F/G

**2610.05282 · Red-TTT: Test-Time Training for Automated Jailbreaking Large Language Models**

[论文](https://arxiv.org/abs/2610.05282)

- **post-training**：Red-TTT按单目标test-time LoRA适应，softmax(beta reward)-uniform风险偏好优势、随轮增强beta与elite replay；固定120查询预算研究。仅列算法研究，不实施攻击。

**2610.05274 · Answer with Evidence: Consistency-Aware Grounded Visual Question Answering for Roadside Traffic Scenes**

[论文](https://arxiv.org/abs/2610.05274)

- **foundation-model**：EtA先box再answer的规范序列；ECPO Grollout跨样本IoU聚类≥max(2,ceil(.25G))形成consensus pseudobox，Hungarian覆盖reward+format+referenceanswer后GRPO，不用GTboxes于RL但非无标签。RoadSceneVQA/gRefCOCO/CARPK跨任务，结构一致性存在性证明不保证真实完整grounding。
  核查位置：§IV-A式5–8；§IV-B式9–11/Algorithm 1；§V

**2610.05273 · When and What to Prune? Stage-Aware Visual Token Pruning for Efficient VLA**

[论文](https://arxiv.org/abs/2610.05273)

- **foundation-model**：SAPrune无reward校准actionattention三depth稳定层，再QR解释度×attention集中度调top-attn/functionaldiversity双路径budget；只prunevisual保留text/action。三VLA LIBERO/SIMPLER+4实机，RTX5090 SDPA latency需保留与FA2区别，不借FLOPs替代实测。
  核查位置：§3.2式5–9；§3.3式10–14起；§4.1–4.4；Appendix B.4.3

**2610.05247 · templar: agentic induction and evolution of standardized radiology reporting templates from large-scale clinical corpora**

[论文](https://arxiv.org/abs/2610.05247)

- **agent**：TEMPLAR把模板与anatomical/diagnostic provenance graph作持久状态，Span-Triple双视图BM25/embedding图Leiden聚类归纳slot，结构reducer约束修订，外证据grounding及train结构化反馈校准粒度。可作多模态/医疗Agent机制候选。
  复现边界：训练findings归纳、training impressions建诊断图，test impressions只judge；重构当前z是唯一patient事实，训练检索句仅语言先验。四临床数据需复核可下载英文报告与许可，非临床安全有效性证明；diagnostic fidelity为LLM参考评分非真实诊断准确率。温度0仍有截断/重试与本地模型context失配；未定位源码。
  核查位置：§3.1–3.4；§4；Appendix A/B/C.1/C.6/F

**2610.05190 · FORGE: Verification-Gated Behavioral Repair for Generative Language Models**

[论文](https://arxiv.org/abs/2610.05190)

- **foundation-model**：FORGE通过prefix/LOO定位毒性，候选token分类后用lm_head低秩QP或MLP零空间编辑，重新生成验证再commit/rollback；可作可审计权重修复机制候选。
  复现边界：固定hidden下线性margin证书只覆盖参与修复的样本/位置，不能宣称heldout安全保证。毒性oracle非真实安全真值，QP与nullspace保证不同；同评估任务上反复修复不得用于泛化提升证据；全文未定位官方代码。
  核查位置：§III-C–F；§IV-A/G/H；§V limitations

**2610.05185 · Recurrent Latent Visual Search for GUI Grounding**

[论文](https://arxiv.org/abs/2610.05185)

- **foundation-model**：ReLaViS LVS latent slots递归spatial distribution/evidence向量回灌，CWC对每candidate质量下界+final截断Gaussian KL；三阶段warmup/GTlatentteacherforce/predictedselfcondition，test只screenshot+query，3×3峰邻域坐标。100ktrain/5kval隔离五GUIbench，grounding非端到端agent任务。
  核查位置：§3.1–3.4式1–9；§4.1–4.3

**2610.05176 · AECG: Asymmetric Experience Consolidation and Governance In Multi-Agent Systems**

[论文](https://arxiv.org/abs/2610.05176)

- **agent**：AECG按team/event/agent保留scope，成功与归因可信失败不对称入账，slow累积/fast折扣Beta-style信念检出退化并按downstream exposure有限预算review；narrow/repair版本仅paired failure+disjoint success replay通过再启用。适合Agent memory/RSI。
  复现边界：Beta-style用于scoring非完整Bayesposterior，noise-corrected drift非校准显著性概率，reachability exposure非causal传播。独立AgentBoard dev参数，四publicbench三independentseed；controlled corruption是机制诊断，应另测自然漂移。失败局部归因质量是依赖，须报告未归因/误归因。
  核查位置：§3–4；Appendix B.1–B.4/C

**2610.05162 · Memadapter: Counterfactual Adaptation Against Memory-induced Sycophancy**

[论文](https://arxiv.org/abs/2610.05162)

- **agent**：MemAdapter对冻结retrieved memories先造counterfactual任务归纳条件使用边界，再当前context反思限定inferential角色，最终evidence-based回答；不改上游memory/retrieval。适合记忆可靠性机制。
  复现边界：同一memorysystem同instance固定retrieval公平对照；gold/reference只官方judge，不能用于usage induction。75 controlled instances含人工重构只诊断，正式三publicbenchmark另报。PersistBench beneficial-memory failure部分上升，不能笼统所有metric提升；三stage额外calls/cost需记录，温度.2不等于独立多seed。
  核查位置：§3–4；Appendix A/B/D/G/H

**2610.05139 · Hidden in the Comments: A Context-Injection Attack Surface in Code LLMs**

[论文](https://arxiv.org/abs/2610.05139)

- **post-training**：公开安全评测：双条件Flask prompt、generation harness、5组件detector及comment position对照。Zenodo API已证实open/published、Manuscript_Codes.zip及校验和。非同scaffold配对且task类型混淆；detector以实验条件作参考非漏洞gold，不能当纯因果或真实漏洞准确率。

**2610.05132 · SpecAgent: Empowering Program Verification with Agentic Synthesis of Formal Program Specifications**

[论文](https://arxiv.org/abs/2610.05132)

- **agent**：SpecAgent用函数/loop dependency计划与ACSL知识RAG生成annotation，Frama-C/WP反馈可回修upstream contract，critique用双次同input调用return equality completeness probe辨弱spec并继续修订。public C/SV-COMP任务适合formal-method Agent候选。
  复现边界：只许改annotation不能改实现；goldspec仅precision/recall judge，verification goals与工具证明不等于完整semantics。return唯一性probe覆盖有限，Frama-C/WP不完备可能false-negative；50程序14repo/811 targets非所有语言，需保持solver/version及超时公平，正式code未定位。
  核查位置：§3–5；Threats to Validity

**2610.05126 · Selecting Repetition Counts Across Model Scales in Data-Constrained Pretraining**

[论文](https://arxiv.org/abs/2610.05126)

- **foundation-model**：小尺度重复次数loss曲线经seedbootstrap+logN回归选top3、以及双项曲线argmin，是明确的预训练数据预算选择operator，target预测前冻结且测试独立。
  复现边界：r同时改genericexposure/训练长度不是纯重复因果；65.6%省6ND是只跑retained假设成本，实际全7grid验证；later80M/520M pointcheck/9,11探索非prospective；预测offset未知，不能称绝对loss无需大模型数据。
  核查位置：§3.1–3.2；§5.1–5.3 Eq6–8；§6.1–6.3；§7

**2610.05124 · Memory Canonicalization: A Framework and Benchmark for Cross-Model Drift in Persistent LLM Memory**

[论文](https://arxiv.org/abs/2610.05124)

- **agent**：写入记忆时做结构消歧、情绪字段提取与独立验证，CMSC-E以统一自然语言渲染隔离内容改写和JSON格式因素，适合作为记忆漂移诊断。
  复现边界：四次写时LLM调用及store-aware冲突检索成本未量；pilot多重校正后未建立显著收益，不能标改进能力。保留raw与canonical不破坏证据，情绪字段不应冒充真实人的心理诊断。
  核查位置：§IV pipeline；§IV-I three-arm；§VI statistics；conclusion/Code Availability

**2610.05107 · SearchJev: A Fast and Calibrated System-1 Model for Search Agents**

[论文](https://arxiv.org/abs/2610.05107)

- **agent**：SearchJev对schema legal-option token logits直接readout，CE+Brier softlabel按来源weight训练LoRA，再独立validation按outputtype温度校准；uncertain decisions交System2。可作Jev/Agent search跨轨算法。
  复现边界：公开原始任务可构建语义等价评测，但SearchDecision-Bench完整bundle与官方代码未定位，勿宣称复刻其数据成绩；100BrowseCompPlus一run有限sample。AR baseline未经taskSFT有训练混淆须另matchedSFT；OOD calibration并非普遍提升，latency只batch1 decision非完整系统成本，gold仅训练标签/外部judge。
  核查位置：§2–5；SearchDecision-Bench split；SLCD Eq；BrowseComp-Plus protocol

**2610.05099 · Small Agents with Semantic Search: Efficient Multilingual Code Localization**

[论文](https://arxiv.org/abs/2610.05099)

- **post-training**：代码定位使用既有质量加权SFT、Dr.GRPO/DAPO和领域F1/轮数奖励，主要新贡献semantic-search harness及数据，不是新核心训练算法；gold只用于训练权重。 该决定仅限后训练核心track，Agent方法/数据公共入口由Agent track独立判断，不能据此全局拒绝。
- **agent**：Compact code-localization agent用colgrep late-interaction CPU index，goldonlytrain turnweights SFT再DrGRPO/DAPO dynamicfilter异步rollout训练；publicSWE-Lite/MultiSWE-Flash按basecommit定位文件，可接Agent后训练候选。
  复现边界：referencepatch位置仅一种解，fileF1非issue resolution。goldoracle top10 subset仅retrievalupperbound，推理agent不能见patch。train排除benchmarkrepo/sharedhistory，teacherquery前state固定；fiveevalseed非five训练。CPU/GPU latency排除预建index成本，工具接口训练对照均须重造demonstration；官方源码未定位。
  核查位置：§3–5；§6 Limitations；Appendix A.5–A.7

**2610.05097 · ReMAP: Restoring the Perceptual Cycle with Reasoning-Time Latent Visual Memory**

[论文](https://arxiv.org/abs/2610.05097)

- **foundation-model**：ReMAP使用全局/局部latent视觉memory、region定位器和分阶段形成/访问训练，再用RL学习何时取证；十基准，必须保留真实视觉memory而非文本oracle。
  核查位置：Abstract（输入检索工件中的完整摘要已逐条审阅）；§3.1–3.2；§4
- **post-training**：ReMAP使用全局/局部latent视觉memory、region定位器和分阶段形成/访问训练，再用RL学习何时取证；十基准，必须保留真实视觉memory而非文本oracle。

**2610.05066 · Salvation Lies Within: Eliciting Inherent Style Transfer in Step-Distilled Diffusion Models**

[论文](https://arxiv.org/abs/2610.05066)

- **foundation-model**：StyleForge无训练agent提render/color-light/composition/referencecontent四状态，统计色/亮度约束后按固定编译顺序保留style弱化composition排除referencecontent，再交few-stepFLUX2Klein；31style×16prompt及三Qwenjudge对照，非新扩散模型/蒸馏loss。可复用structuredprompt operator，judge自动分不当human偏好或生产AB。
  核查位置：§3.1–3.4；§4.1–4.3

**2610.05047 · Beyond Task Completion: Measuring Interaction Cost in Terminal User Interfaces**

[论文](https://arxiv.org/abs/2610.05047)

- **agent**：TUINaut用Docker+Tmux共享真实TUI输入输出，独立状态oracle检验完成度；Agent-KLM分报推理token与原子按键数，适合交互Agent成本诊断。
  复现边界：84任务15仓库，30任务有指纹，不能仅凭屏幕含某词宣告完成。token与按键单位不同不相加、不等同人类认知时间；必须真实TUI而非返回预期状态fixture。仓库网页读取失败待用API复核，不影响独立机制定义。
  核查位置：§2.2 Eq3–5；§3.2–3.4；§6.3

**2610.05039 · Causal Improvement Graph for Agentic Harness Optimization**

[论文](https://arxiv.org/abs/2610.05039)

- **agent**：CIG以Evidence–Hypothesis–Intervention–Outcome typed graph作persistent improvement state，Observe/Plan/PlanSelect/Implement/Evaluate/Update局部proposer调用，由外部validation结果修订hypothesis assessments再portfolio选择。可接Agent harness RSI/evolve。
  复现边界：Causal名称并不识别统计因果；七ordinal criteria及pairwise redundancy是LLM评估。固定预算val选择后heldouttest，testoracle regret仅外部诊断不可进入selector；8candidate/3或5runs短搜索不证明跨任务长期迁移，wide/deep schedule需匹配，code未定位。
  核查位置：§3–4；Appendix A.3–A.8

**2610.05030 · EVISKILL: Grounding Skill Evolution in Replayable Evidence**

[论文](https://arxiv.org/abs/2610.05030)

- **agent**：EviSkill由train trajectory span构建Replayable Evidence Cards链接局部edits，恢复prefix状态重执行验证/反思，globalvalidation更新ValidatedSkill；全局拒绝时仅replay支持edits留WorkingSkill ledger跨epoch再检验。适合Agent skill RSI。
  复现边界：真实env恢复和rerun是定义性机制，不能LLMjudge静态旧trace替代；local replay acceptance不等于globalpromotion。训练/validation/test独立，最终只ValidatedSkill冻结test；跨epochcontrast仅train。局部evidence及edit需防case memorization，card数量/extra replaycalls/cost应报告，六backbone不等于独立训练seed。
  核查位置：§3–4；Appendix B/E/F prompt templates

**2610.05026 · GeoBridge-VLA: Geometry-Aware Residual Adaptation for Vision-Language-Action Models**

[论文](https://arxiv.org/abs/2610.05026)

- **foundation-model**：GeoBridge-VLA nativevisual中间feature→bridge/K4邻域geometrydecoder，stage1 simdepth或实机DA3pseudodepth监督；stage2冻结geometry+VLM，zero-init1×1residual gate≈.002对nativepatch相加，flow+RMSresidual罚。SmolVLA LIBERO/OMY，仅保持tokencount非零新增decoder计算；跨backbone未验证。
  核查位置：§III-A式1–2；§III-B式3–4；§IV-A–C；§V

**2610.05025 · Triggering Generalist Reasoning via Predictive Uncertainty for Dual-System VLA**

[论文](https://arxiv.org/abs/2610.05025)

- **foundation-model**：TUD将π0拆heavyPaliGemma generalistcache与currentSigLIP/Qformer/actionexpert，同anchor跨观测重预测固定slot std衡量plan变化；runningmean阈值online百分位p70+maxskip触发刷新，执行仍committedchunk非每次probeaction。VLA-Arena/CALVIN/实机，variance是stalenessproxy非校准epistemic uncertainty，额外probe成本需计。
  核查位置：§3.1–3.3式2–6；§4.1–4.4；Appendix B/C

**2610.05024 · LightVLN: Efficient Aerial Vision-and-Language Navigation with Compact Memory and History-Guided Local Aggregation**

[论文](https://arxiv.org/abs/2610.05024)

- **foundation-model**：LightVLN每historicalframe learnedquery单token FIFO，historyselectinstruction指导current16×16grid固定32局部区域attention汇聚，保留空间覆盖。OpenFly/AerialVLN分开训及未见campus，完整模型1.276B非仅.5B，4090profile/闭环路径应分别记；无额外memoryencoder不等于无visionbackbone。
  核查位置：§III-B/C式1–5；§III-D/E；§IV-A–D

**2610.05023 · Look Where You Say You're Looking: Self-Grounded Attention for Visual Reasoning**

[论文](https://arxiv.org/abs/2610.05023)

- **foundation-model**：Self-Grounded Attention以GroundingDINO为每个CoT观察步骤定位，选定attentionheads的区域显著性得分加答案exactmatch/judge与format奖励后GRPO；head选择依VisualCoT相关性，不能将attention当因果忠实性。SaliencyR1-8k训练与25个VQA lmms-eval评测；需保留真实定位器/辅助judge和8H100训练预算，不能用答案窥视fixture代替。
  核查位置：§3.2–3.5（saliency reward、GRPO、head selection）；§4.1–4.2/Table1

**2610.04991 · CIPO: Counterfactual Imagination Policy Optimization for Adaptive Tool Granularity Selection**

[论文](https://arxiv.org/abs/2610.04991)

- **agent**：CIPO用预算BPE挖成功train工具链并实例化可binding/trace/interrupt技能，G4 rollout中两base各在first eligible state替换atomic/skill并同policy继续，bounded outcome difference补充reward再GRPO。适合Agent RL/toolgenome。
  复现边界：branch只训练，test不见goldchain；须复制真实envstate而非读最终答案。主TSR将partial计success、五judge重复不是五训练；L.1另yesonly及ToolAthlon三训练seed实环境验证须分别展示。Comp/Raw减policydecisions不等于tokens/latency，基线是同simulator改写非原实现，code未定位。
  核查位置：§3–4；Appendix D/E/L.1/O/P

**2610.04961 · Building LLM Agent Systems the Deep Learning Way: From Modular Design to Architecture Search**

[论文](https://arxiv.org/abs/2610.04961)

- **foundation-model**：深度学习式agent架构搜索和prompt优化，由agent track审查。
- **agent**：LLM building blocks将单调用/历史递归/ToT/GoT/多queryRAG组合为可执行harness，自反思更新metaprompt，Optuna在train30%搜索max tokens/head/retrieve参数后70%test冻结。publicGSM8K/StrategyQA/TSP可实现模块化架构搜索。
  复现边界：Transformer/RNN等是workflow类比不是训练新神经架构；feedback propagation是prompt文本编辑非梯度。Related-multi只afterreviewrelease，不能宣称已有原完整结果；检索F1对citationreference不等于related-work质量，外部gold仅评分，120trial成本与randombaselinebudget匹配。
  核查位置：§3–4；Appendix B/C/D Optuna ranges

**2610.04950 · How Should Teachers Be Prepared? RL on Student-Induced States for On-Policy Distillation**

[论文](https://arxiv.org/abs/2610.04950)

- **post-training**：Prep-OPD先让teacher在固定初始student产生的prefix状态上RL，再冻结teacher做OPD，实测DeepMath及8数学基准；无gold解法灌入teacher，需保留两阶段状态分布。

**2610.04940 · Software World Models: From Consequence Prediction to Decision Value**

[论文](https://arxiv.org/abs/2610.04940)

- **agent**：SWM 从恢复的训练世界执行反事实变化，SFT warmup+GRPO 学习 downstream blast set，再以采样概率决策迁移和付费检查；真实开源库与独立 synthetic world 可验证。
  复现边界：不是静态图可达性替代：结构与学习互补；expert exploration 用特权图，仅训练对照；预测 F1 与决策 regret 不能混成同一优势；公开软件环境重放仍需核验。
  核查位置：§3.1–3.3/Algorithm1; §4; Appendix D.5–D.13

**2610.04927 · Assembling Insights for Agentic Machine Learning Engineering Systems**

[论文](https://arxiv.org/abs/2610.04927)

- **agent**：MLE-InsightForge 从源竞赛 gold 解法提炼 competition/domain/improvement insight，按触发-动作条件注入 ReAct 解法树；160 Kaggle 任务/12域的源-目标隔离协议可验证。
  复现边界：绝不能读目标任务 winning solution；私有测试输入在最终选中后外部重跑；Kaggle 登录/许可与下载资格要逐项核验；预训练污染仍不被源任务隔离消除。
  核查位置：§3–5; normalized p33,44–55

**2610.04921 · Complex Agents, Shallow Tests: Demystifying and Enhancing Test Adequacy of Agent Harness in the Wild**

[论文](https://arxiv.org/abs/2610.04921)

- **agent**：HarnessTester用coverage找未覆盖LLM依赖代码，AST精确检索构造器/fixture/mock绑定，指导保留调用契约并生成不同分支测试，适合harness工程测试候选。
  复现边界：同模型120分钟预算，scope与general基线需分开；mock必须符合真实provider结构与注入点。覆盖率或mutant kill不能替代真实模型能力，历史bug评测要隔离已知patch，官方artifact链接未从提取文本恢复。
  核查位置：§6 HarnessTester；§7 coverage/mutants；§8 H-Bench；threats/artifact statement

**2610.04918 · Residual Visual Credit Optimization: Conserved Evidence Routing for Multimodal Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.04918)

- **foundation-model**：RVCO多模态RL token信用分配，由post-training track审查。
- **post-training**：RVCO用图像patch干预似然构建证据分数、IQR/entropy路由及residual校正精确保留响应credit质量；ViRL39K四VLM家族训练，需真视觉干预而非固定token启发式。

**2610.04916 · PreAct-Nav: Agentic Reasoning Before Action for Urban Navigation**

[论文](https://arxiv.org/abs/2610.04916)

- **agent**：PreAct-Nav 用 Navigation Memory 的中期子目标和按需 Predictive Sandbox 生成行动未来线索，冻结 VLM 先审后行动，证据未决或修订无效则回退原 policy。UrbanNav/CityWalker 可验证。
  复现边界：预测只由当前观测与拟议动作产生，不可查真实未来；统一行动格式/决策预算；预测工具、记忆、审查成本须全部计入；seen/unseen 分开。
  核查位置：Method action-review loop; normalized p36–55; Appendix D/F/G

**2610.04915 · Are We Measuring Scientific Intelligence? Rethinking the Evaluation of AI Scientists**

[论文](https://arxiv.org/abs/2610.04915)

- **agent**：以null/withdrawal/flip三类经统计量验证的反事实数据评估科学Agent是否依证据作答，并用EGA区别答对旧key与响应新证据，可接研究完整性评测。
  复现边界：18单细胞题+4合成遗传统计题，人工反事实与少量模型；统一清理文件名/gzipheader/raw层等避免答案泄漏。参考统计与gold仅verifier可见，证据响应不等于完整科学质量，不能用旧答案评分flip。
  核查位置：§4.1–4.3 Eq2–5；§5；Appendix B/D；Limitations

**2610.04899 · Rewrite What Matters: Adaptive Multilingual Query Rewriting for Reasoning via Agentic Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.04899)

- **post-training**：mRewriter-R1以冻结下游准确率奖励训练query重写，正文明确使用标准GRPO；aspect/operator规划属于应用框架而非核心优化器创新。 该决定仅限后训练核心track，Agent方法/数据公共入口由Agent track独立判断，不能据此全局拒绝。
- **agent**：mRewriter-R1 顺序执行 language/structural/semantic 三类有限算子，由 GRPO 优化冻结下游模型结果。MGSM/BELEBELE/XCOPA 明确训练和标准语言测试可验证。
  复现边界：不是无约束自由 rewrite；语义/数字/实体保持并非完美，需测变坏实例；三次推理平均不是独立训练种子；下游正确答案只能奖励训练/测试评分。
  核查位置：§3/GRPO; Appendix A/D/F; normalized p16,29,82–106

**2610.04889 · ForkPilot: Self-Evolving Policy for Retrospective Search in Long-Horizon Agents**

[论文](https://arxiv.org/abs/2610.04889)

- **agent**：ForkPilot 使用恢复同状态的 search-vs-skip 成对完成轨迹训练 task-bootstrap ensemble，结合成本、支持度与校准边际决定 commit/probe/skip，任务内冻结、跨已完成源任务更新。六个公开 benchmark 可验证。
  复现边界：必须真正恢复环境且隔离并行写入；经验只在任务完成后更新，不使用当前未来结果；source-only 选 λ/阈值；conformal 覆盖针对 realized paired target 而非保证闭环均值。
  核查位置：PDF pp3–6; Algorithm1 p21; Appendix D.3/Table6

**2610.04882 · ResOPD: Tail Residualization for Sparse On-Policy Distillation**

[论文](https://arxiv.org/abs/2610.04882)

- **post-training**：ResOPD完整top-k质量加tail bucket基线，每步coarse梯度与稀有tail残差组成无偏估计（仅全支持祖先采样）；主数学实验top-p=.95/top-k20不满足该无偏条件，必须分别报告机制与成绩。

**2610.04868 · From Memory to Guide: Spatio-Temporal Composer for Procedural Coding Memory**

[论文](https://arxiv.org/abs/2610.04868)

- **agent**：Composer 由 Selector 选择 Skill 并保留 whyNow，将规则绑定当前实体形成 Runtime Guide，按完成/失效条件终止并重新进入任务要求。固定 Skill Bank 的程序记忆适配机制可实施。
  复现边界：论文13项 EngramBench/8小时级私有长任务包的下载和权限未核验；7.2pp/32.2% 数字不能挪用为公开通用 benchmark 结果；guide 不能包含未来正确修复。
  核查位置：Method/Algorithm1; normalized p28–51; Experiments p52–63

**2610.04851 · CURIO: Curiosity-Driven Test-Time Learning for Open-Ended Discovery**

[论文](https://arxiv.org/abs/2610.04851)

- **post-training**：CURIO训练hidden-state transition预测器并缓存更新前残差，epoch归一后只在非top-k采样token加bonus；它不是语义新颖性保证，encoder/predictor仍可能collapse；有科学发现任务实测。

**2610.04845 · Which Preferences to Train On? End-to-End Multi-Objective Alignment with an Adversarial Preference Distribution**

[论文](https://arxiv.org/abs/2610.04845)

- **post-training**：MAESTRO用Dirichlet对抗偏好分布DirUEG更新，独立adversary/policy批次、向量reward GAE后偏好标量化；多目标HH/Beaver与摘要faithfulness实验。

**2610.04824 · Agent Behavior as Code: Efficient and Robust LLM Agents with Programmatic Specifications**

[论文](https://arxiv.org/abs/2610.04824)

- **foundation-model**：ABCAgent符号程序规定agent行为，由agent track审查。
- **agent**：ABCAgent 以有未绑定输入变量的程序规定 agent 行为，代码 executor 管理作用域和类型状态，LM 负责设计/修改。GAIA、WorkArena、GSM-Symbolic、tau2 的公开基础任务可验证。
  复现边界：原作者实现与 augmented GAIA/WorkArena-CF 称接收后发布，不能声称已复现扩展18题；GAIA dev 是原文评测集需防后验修改程序；不同实例不允许固化答案。
  核查位置：ABCAgent design/execution separation; Experiments; Appendix C/D; normalized p15,22,24–27

**2610.04805 · ExStereo: Lifting 2D Vision-Language-Action Models to 3D with Explicit Stereo Representations**

[论文](https://arxiv.org/abs/2610.04805)

- **foundation-model**：ExStereo由冻结FastFoundationStereo、标定fxB/d和桌面RANSAC构造4方向正交depth/xyz/valid显式表示，以actionquery crossattention残差接入VLA；不替换prefix/VLM。7个3500episodes midtraining与10个评测任务/对象不交叠，post每任务100episodes；RoboTwin和三实机任务20次各验证。上游深度计算和标定必须计成本，不能把平均成功率百分点改写相对提升。
  核查位置：§IV-A–C；§V-A–C/TableI；§VI/TableIII

**2610.04794 · Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It**

[论文](https://arxiv.org/abs/2610.04794)

- **agent**：可接入记忆治理诊断基础设施：区分 active/superseded/retracted/expired 与 current/past/change 意图，比较无值的状态摘要、返回记录 tags、简单名称 lookup，含444条同问题反事实存储版本。正文明确公开代码与数据，可忠实实现监测协议。
  复现边界：这是监测诊断而非新 Agent 能力算法；gold 构造 oracle tags 仅作上界，不得在能力路径读入。仅40个合成人物，部分子组30条；匹配 AUROC 为事后分析且71比较未校正。提及检测未收集人工标签，没有证据说明判断改善答案，未实现 backend 写入维护机制。
  核查位置：§3 pp.2–3 lifecycle / coverage；§4–8 controls；§9 p.8 limitations；Reproducibility p.9

**2610.04792 · Do More Modalities Always Help? A Geometric Perspective on Missing-Modality Robustness**

[论文](https://arxiv.org/abs/2610.04792)

- **foundation-model**：GU针对缺失图像的Grassmann子空间编辑可作为多模态稳健算子。
  复现边界：需要额外训练matchedT模型，不能仅宣称编辑毫秒总成本；Table4含reference cost。geodesic最短距离不是任务最优证明。k/η/层仅development挑选，test隔离；未找到作者代码。
  核查位置：§3–4；§5 Eq1–5；§6.1–6.5 Tables2–4；App D/E

**2610.04779 · Asymmetric Repository Lineage Modeling and Verifier-Guided Coordination in Concurrent AI Coding Agents**

[论文](https://arxiv.org/abs/2610.04779)

- **agent**：MergeGym 区分 open-time authored-file overlap、真实 git merge-tree 冲突与调度重放；229 heldout repositories 的 T1、5936 可重放 T2 与97仓库调度任务是可执行基础设施候选。
  复现边界：T3 固定历史标签、duration 和非反应 agent，不是因果生产试验；oracle gate 不是可部署策略；31不能重建的 patch 不得计为干净；语义冲突仍未解决。
  核查位置：MergeGym T1/T2/T3; lineage replay; normalized p24–41,59

**2610.04753 · More Value per Key: Asymmetric Sparse Attention for Faster LLM Decoding**

[论文](https://arxiv.org/abs/2610.04753)

- **foundation-model**：SAGA 解耦key/value头数，结合周期刷新阈值的近似top-N；预训练GQA转换通过数据加权key合并、最小权匹配和KL+CE蒸馏，而非简单删头。
  复现边界：初始化推导忽略RoPE；长上下文速度不能外推短序列，且质量确有下降。原文H200/B200 timing、约23K蒸馏迭代，A100需重新测；Atop-N不是固定恰好N项。
  核查位置：§3.1–3.2；§4.1 Eq13–18；§5.1–5.3 Tables1–2；§6；official repository

**2610.04721 · Knossos and Ariadne: Benchmarking and Learning Complete Diagram Topology Extraction with Vision-Language Models**

[论文](https://arxiv.org/abs/2610.04721)

- **foundation-model**：Meta合著Ariadne先预测nodeinventory，再每组3active source对全predicted nodes输出typed edges，确定性并集后单独trace；推理不读GTinventory。Knossos六域18k/1200不同seed，另TopoBench162图外测；模板内seed隔离非未见grammar泛化。公开dataset/repo链接明确，方法与图结构评测皆有独立价值。
  核查位置：§2.3–2.5；§3.1–3.3式1–2；§4.1–4.4；Appendix B.5；README Quickstart/Ariadne/Code and Assets；adapter weights not included

**2610.04699 · Not Self-Decidable: LLMs Cannot Draw the Boundary of What an Agent Verifier Can Check**

[论文](https://arxiv.org/abs/2610.04699)

- **agent**：CoVer 将模型 corroboration 只用于提名，生成 fact-slot+规则并用 structure/groundedness/invariance/sensitivity 四门验证；使用基础设施 attested 字段、缺失或异常则 fail closed。
  复现边界：73规则/36合成记录狭窄；precision 不比同消除率 unanimity 更优，不能宣传解决 decidability；LLM 自己填写 consent 字段不是外部授权证据；人工/LLM ground truth 分开。
  核查位置：§6/CoVer Algorithm1; normalized p53–60; Appendix A/E

**2610.04687 · Understanding Errors in LLM-Based Question Answering over Imperfect Tables**

[论文](https://arxiv.org/abs/2610.04687)

- **agent**：GBDI 对表格随机行排列做五个独立发现 context，映射回原行合并 union ledger，再按可验证证据 Edit/Drop/No-op。RADAR-T313例/53任务/27表可验证。
  复现边界：已人工修复表仅 oracle 上界，实际 agent 必须自行验证；行顺序依赖题不适用；source-table clustered 区间；读取 observed table 而非 clean source/gold repair。
  核查位置：GBDI workflow; normalized p11,29,39,45,55–61; Appendix A/B/E/F

**2610.04658 · RETRACE: From Entangled Repair Histories to Reusable Experience for CI Repair**

[论文](https://arxiv.org/abs/2610.04658)

- **agent**：RETRACE 从 CI 完成修复历史做 endpoint 向后与开发历史向前的变更归因，生成 problem-level 三层可复用经验。CI-Repair-Bench565 PR/101仓库、最早30%历史与408后续目标可验证。
  复现边界：历史目标时间隔离必须维持；CI 依赖/custom actions 有不可本地复现项；轻量局部检查不等于完整 CI 修复成功；不读取目标未来 endpoint。
  核查位置：RETRACE bidirectional attribution/three abstraction levels; normalized p55–57,67–68; Appendix A

**2610.04651 · GS-Codec: A Gaussian-Splatting Bottleneck for Neural Audio Coding**

[论文](https://arxiv.org/abs/2610.04651)

- **foundation-model**：GS-Codec以连续1D Gaussian内循环拟合潜变量+stopgradient/commitment训练编解码，再训练latent重建预测器替代300步Adam，训练后heldout校准的kmeans scalar量化参数；固定centers不传位置，bitrate仍离散。LibriTTS/LJSpeech/LibriSpeech评测需区分2339h与54kh配置，部分基线引文非重跑；L40S7.9ms仅encoder且3秒非因果片段，不是流式端到端延迟。
  核查位置：§3.1–3.2；§4.1–4.3/Table4；limitations
- **post-training**：GS-Codec神经音频编码瓶颈与高斯splatting，关键词post-training是bitrate控制。

**2610.04646 · SEIS: Self-Evolving Inference Systems**

[论文](https://arxiv.org/abs/2610.04646)

- **agent**：SEIS 给 agent 私有代码 worktree、固定 correctness/throughput scorer 和预算，成功核验继承实际推理引擎/kernels；公开 Qwen 与真实 GPU 工作负载可验证代码自进化。
  复现边界：不是仅 registry 接入；解码/自然 EOS 和生成能力必须核验，原文14次终止失败被拒；MMLU prefill 一致不能证明 decode 等价；单请求吞吐不是并发 serving。
  核查位置：SEIS session/harness gates; §5–6; normalized p16–22,36–54; Appendix B/F

**2610.04641 · Back to the Future: Regressing Readability Features from LLMs**

[论文](https://arxiv.org/abs/2610.04641)

- **agent**：BTTF将AST-tagged片段embedding几何/聚类、冻结codeLM的构造级surprisal与32/256token上下文差及传统代码特征组合；跨模型稳定性共识选11特征，再以数据集等权的Ridge(alpha200)回归分位化可读性，输出具符号的特征贡献。
  复现边界：公开1100人评分样本以Java为主；feature选择使用所有六数据集，因此LODO只验证固定表示后的预测迁移，不验证完整选择过程的无泄漏迁移。插补/裁剪/标准化必须fold内训练。13变换是可读性方向诊断，解析合法不证明语义保持/功能正确；可作为coding-agent质量辅助评估，不能当执行正确奖励。
  核查位置：§2.1–2.2、Table1、§3.2–3.4、§4.6、AppendixA/B、§8

**2610.04616 · PerturBot: Breaking Shortcut Priors in Vision-Language-Action Models with Perturbative Training**

[论文](https://arxiv.org/abs/2610.04616)

- **foundation-model**：PerturBot的V/C/R分别保持任务的视角干扰、状态/技能语言重标、已执行偏差运动重标，按原flow loss混合，不虚构失败目标恢复。配对GroundFscore以共享noise前向分别测null不变和causal敏感，需两条同状态expert记录标定Δaction，分母floor与过滤明确；这是诊断非任务能力证书。50种真实PnP布局与RoboTwin50任务含等预算/全因子消融，84%成功率非只离线分数。
  核查位置：§3.1–3.3 Eq3–4；§4.1–4.3/Table1；AppendixA/F

**2610.04611 · Practical Runtime Enforcement of First-Order Temporal Requirements**

[论文](https://arxiv.org/abs/2610.04611)

- **agent**：EnfFlash 将 MFOTL 可执行片段编译为表式 EF 因果/抑制运行时，用参考解释器及真实 trace 比较，是 agent 外部强制策略后端候选。40 formula/Agent 环境有可验证基线。
  复现边界：只支持声明 fragment，未来/过去嵌套需要改写；实时 enforce 不是 LLM 语义授权判断；MonPoly 只 monitor 不是完全同任务；必须保留 timeout 和最大延迟。
  核查位置：§4/EF Algorithm2; §5; normalized p50–53,139–148

**2610.04607 · ForeAct3D: Policy-Grounded Future World Modeling for VLA Policies**

[论文](https://arxiv.org/abs/2610.04607)

- **foundation-model**：ForeAct3D从policy features的6queries解码当前/未来depth/3classmask/pose，未来仅接policy-generated action，训练用background staticity、按GTinstance的Kabsch rigidity、kinematics，推理不需要未来或GT。samepixel对应只是短时近似，强监督与刚体假设是实质限制；LIBERO98.3/CALVIN3.73与实机37.8%有消融。几何预测对照horizon不同且预测mask定位仍使用GTinstance，不可称无GT实例检测。
  核查位置：§3.1–3.4 Eq3–5；§4/Tables1–2；AppendixA.1–A.4/Table8；limitations

**2610.04604 · Anticipating the Consequences of Curriculum Decisions with Large Language Models**

[论文](https://arxiv.org/abs/2610.04604)

- **post-training**：LLM指导Craftax学习课程，但训练对象为环境RL learner而非LLM后训练。
- **agent**：LLM curriculum 根据完整 Craftax256目标文本构建跨任务关系/可行性图，与历史 learning progress 联合决定训练任务。公开环境和完整目标成功判定可训练验证。
  复现边界：LLM图先验不是实际因果迁移测量；只能使用当前训练表现；公开全目标表不等于允许使用测试回报选 curriculum；同样训练/eval成本和种子。
  核查位置：§3–4/curriculum; Appendix C.1; normalized p28,37,47,87–90

**2610.04596 · DiffGate: Difficulty-Gated Teacher Guidance for On-Policy Distillation**

[论文](https://arxiv.org/abs/2610.04596)

- **post-training**：DiffGate将teacher-student logratio以2tanh(delta/2)有界映射，并按组成功率只对失败轨迹调节teacher指导；固定8B teacher、0.6/1.7B学生数学代码训练。

**2610.04580 · Strong Helps Weak: Directional Cross-Modal Alignment Transfer in Multi-modal LLMs**

[论文](https://arxiv.org/abs/2610.04580)

- **foundation-model**：DCAT是有清晰闭式求解与公开项目代码入口的跨模态对齐迁移候选。
  复现边界：不是任意跨架构合并或所有模态都益处；alignment是理论假设下proxy非真实MI测量。逐组重收数据和fp64solve计成本，η/β设置须在独立validation固定；test收益不能反选donor。
  核查位置：§4 Eq5–11；§5；App C.3–C.5/D/F；官方项目页

**2610.04575 · From Probe Scores to Alarm Policies: Operational Validity of Activation Monitors for Language-Model Agents**

[论文](https://arxiv.org/abs/2610.04575)

- **agent**：按语义task/case聚合any-alarm maxima，fit/calibration/test严格分离；由独立负单位次序统计量Beta上界选择最大可认证rank并strict-exceedance报警，支持不足则abstain。observable/activation/joint同horizon比较，哈希绑定模型、阈值与一次性test，fail-closed claim compiler避免AUROC被升级成部署保证。
  复现边界：这是评测/校准合同，不是新detector或新定理；公开artifact仅score-level replay，不能声称重生轨迹/激活或端到端训练。ST-Web23negative不足59/29，零报警属机械abstain；AgentDojo38positive不足40，10%预算testFPR18.67%显示shift。Qwen14B对照非compute-match，人审/拦截/干预收益未测；证书依赖独立同分布负单位，不是适应攻击或familywise保证。
  核查位置：§3 pp.3–4 Eq4–6、§4 pp.5–6 Fig2/Table4、§5、§6.3 p.8

**2610.04555 · $\mathrm{TRIZ}^{a}$: Guiding Agent Evolution from Pattern Recognition to Solution Invention**

[论文](https://arxiv.org/abs/2610.04555)

- **agent**：TRIZ-a 先冻结矛盾与比较协议，声明40类 typed mutation 的契约，再执行候选并根据固定参考群体的 useful/harmful 功能信息选择。公开三网络安全数据可验证。
  复现边界：FI 依赖预定义群体和预算，不保证单调进化；hash/split/preprocessing必须匹配；V17/V18不是正式V2证据；安全高风险动作仍需人授权。
  核查位置：TRIZ typed mutation/functional information; Eq/Appendix B; normalized p14–21,38–39,81

**2610.04518 · Length Generalization Needs Proper Regularization**

[论文](https://arxiv.org/abs/2610.04518)

- **foundation-model**：VPAD为每token非中心化激活计算保均值/方差的affine dropout，明确作用于RMSNorm后共享mask，具公开训练/评测/权重，可列长度泛化训练算子候选。
  复现边界：方差只按坐标匹配，projection covariance有残差，不声称完全保真分布。Fig1按RULER4–8k选bestseed，正式报告三seedFig4；SmolLMBase额外100B训练不可当同数据因果对照。投影各独立mask是官方额外功能非paper路径，8k版本还改attention scaling须拆消融。
  核查位置：§4.2–4.4 Eq12–13；§5.1–5.5；App C.1/C.2；official README

**2610.04517 · EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution**

[论文](https://arxiv.org/abs/2610.04517)

- **agent**：EvoCast 将 LLM 的机制假设/源码修改与确定性 evaluator/晋升权威分开；先基线+可执行 ablation，再每轮有界源程序结构变异。TFB 公开预测任务支持真实实验。
  复现边界：必须只改模型边界、不能改评估路径；训练统计拟合不看 val/test；最终模型用 validation 选，论文结果是特定预测任务不是通用科学能力。
  核查位置：EvoCast Algorithm1; normalized p28–39,53–59

**2610.04512 · Correctness Is a Direction: Geometric Answer Selection in Language Models**

[论文](https://arxiv.org/abs/2610.04512)

- **foundation-model**：Geometric Answer Selection用50个标注校准问题的正确减错误平均归一hidden形成方向，对每候选一次前向投影选答案；适合冻结模型读出算子。
  复现边界：非零样本，20%验证选择层；TQA校准必须和测试隔离。固定候选任务不能直接扩展自由生成，跨任务方向并不通用；配对比较不应照搬独立两比例z检验；未找到作者代码。
  核查位置：§3.1 Eq1–4；§5.1/Table4；§6.3；Limitations

**2610.04506 · EgoExo-Next:Benchmarking Vision-Language Models on Visual-Option Next-State and Cross-View Reasoning**

[论文](https://arxiv.org/abs/2610.04506)

- **foundation-model**：EgoExo-Next提供2503视觉4选1题、四个ego/exo当前匹配与未来状态任务，后续干扰帧防最远未来捷径；candidate-only/打乱序列/mismatch及CLIP/DINO检查支持诊断价值。官方HF有输入图、input_meta、分离answers与加载契约；仅输入元信息/图给模型，gold/time不给模型。注意论文§4.1两方向平均与HF样例both-directions-correct表述不一致，接入须固定评分版本并报告；源图继承六套许可、注释限非商业研究，不是统一开放商用。
  核查位置：§3.1–3.2；§4.1–4.3/Table2–3；官方HF Data format/Loading/Licensing；Datasetcard Subtasks/Repository structure/Data format/Loading/Licensing（已访问）；论文评分契约与card的方向聚合表述需区分

**2610.04488 · Can LLM Agents Automate Reinforcement Learning for Text-to-Speech?**

[论文](https://arxiv.org/abs/2610.04488)

- **agent**：TTS agent 在 CosyVoice2 上搜索 LM-carrier DPO 与 flow-carrier GRPO，再组合互补策略。AISHELL3/LibriTTS固定5000条件与 Seed-TTS-Eval 提供真实训练和外部观察指标。
  复现边界：原文报告测试集通过合同未读通道泄露、pivot proxy未受合同保护和 reward inflation，不能复用这些受污染迭代为正式改进；merge scale人为选择；保留独立最终test。
  核查位置：RL design space/data-proxy-algorithm; §4.2–4.3; Tables1–3

**2610.04432 · Video2World: Benchmarking Coding Agents for Interactive World Modeling from Embodied Videos**

[论文](https://arxiv.org/abs/2610.04432)

- **agent**：Video2World将视频重建交互仿真作为coding-agent任务，分离可执行性、几何、动力学和功能oracle，公开222实例数据与评分接口可作为多模态Agent候选。
  复现边界：189视频39任务族，180分钟单构建无统一token预算，比较完整系统而非裸模型。gt_pkg/hidden仅verifier可见，禁止直接写状态伪造动力学；HAR含源标注非公平Agent。三类sim依赖与GPU/Vulkan需真实环境验证，单纯读HAR日志不算接入。
  核查位置：§3.2–3.3；§4.1；official README Data/Usage

**2610.04429 · Asking Earns Nothing: Scoring the Decision to Act in BFCL Multi-Turn**

[论文](https://arxiv.org/abs/2610.04429)

- **agent**：将BFCL base与miss_func/miss_param配对，机械定位唯一empty-gold anchor；从结构化rollout辨别world-changing尝试而非lookup，计完整信息下act与缺失信息下hold的balanced accuracy。过滤坏key/多anchor/不匹配并人工认证成223pairs，strict与独立授权步骤credited分开。
  复现边界：不读取gold给actor；gold只离线定位/评分。该指标不是任务完成率或通用安全率，50%无信息基线；拒绝执行的尝试也计act，缺失function幻觉仍计，prose不算调用。134只读pair不混入避免always-hold满分；31坏key及8构造错误明确记录。Gemma默认系统prompt与native工具模型不是clean capability对照；判断回复内容的LLM仅诊断不进入主score。
  核查位置：§3、§4.1–4.3 Eq1、§5.3–5.4、AppendixC–F

**2610.04409 · Understanding and Mitigating Hallucination Escape in Tool-Using LLM Agents**

[论文](https://arxiv.org/abs/2610.04409)

- **agent**：EscapeGuard 从冻结 LLM hidden state 学冲突 probe，按 selection/argument 阶段对当前 tool name/description/schema token 加 conflict强度 attention bias。BFCL/Seal/Glaive 有公开测评来源。
  复现边界：核心是实际注意力干预，不能替代关键词 heuristic；probe/阈值要训练/validation隔离；正文 code/data承诺发表后发布；攻击/冲突配置不能用gold选介入。
  核查位置：EscapeGuard §5.1–5.3; normalized p39–49; Appendix A–H

**2610.04381 · Beyond Plausibility: Verifiable Fine-Grained Image Editing on Structured Assets**

[论文](https://arxiv.org/abs/2610.04381)

- **foundation-model**：VeriEdit-Bench用可编辑SVG/chart/HTML源渲染确定目标与保护区，Lab距离分解fidelity/preservation/localization/magnitude及逐例调和分，可补图像编辑可执行评估。
  复现边界：编辑器只看图和指令，目标/mask仅verifier可见；1740例22cell等权与逐例均值分别报告，no-op应0/100/0/0。渲染噪声门与一像素膨胀是具体协议，不是通用图像美学评价。
  核查位置：§3.1–3.2 Eq1–5；§4/Table1；Appendix B.1/B.2

**2610.04379 · AgentPersonaBench: Benchmarking Persona-Driven User Simulation**

[论文](https://arxiv.org/abs/2610.04379)

- **agent**：AgentPersonaBench用2460任务跨survey/chat/web/app检验persona约束是否转化成行为，自动泄漏检查加独立人审、确定性与LLM判据分报，适合用户模拟Agent评测候选。
  复现边界：只是指定特征的可控性，不是现实人群分布/真实个人预测；主榜单单次、部分arms三次重跑。78.5%确定性判据外仍有judge；web/app须真实环境而非文本假执行。机构按论文一作归属，资助Meta/OpenAI不能作作者归属。
  核查位置：§3.2–3.3；§4；Appendix E/F；official repository

**2610.04375 · Do Tool Calls Execute as Intended? Measuring and Repairing Intent-Execution Correspondence in LLM Agents**

[论文](https://arxiv.org/abs/2610.04375)

- **agent**：IEC 以各跳接收器 parser 检测 intent-to-execution 第一个变异 hop，并单跳修复重放确认；IntAct 为对应 wrapper/process 边界生成不被改写的传递形式或拒绝。公开合成payload/CLI路径可验证。
  复现边界：私有历史 shell corpus不能公开伪重建；观察 witness 不再次执行危险命令，修复实验应隔离且授权；exit0/stdout不是参数一致证据；Windows/Linux边界分别测。
  核查位置：IEC/IntAct Algorithm1/Table1; §experiments; normalized p15,30,45,66–67

**2610.04371 · Functionally Equivalent or Not? Graph-Grounded Differential Surrogate Execution for Code Equivalence**

[论文](https://arxiv.org/abs/2610.04371)

- **agent**：FEAgent 基于 repository图义务与盲化双程序 surrogate 轨迹提出可执行反例，由确定性对账返回 Equivalent/Inequivalent/Unclear。EquiBench/SWE-bench Verified 可做二次审计。
  复现边界：不是形式证明；所有报告 divergence 必须直接执行确认；额外行为是否可取需issue要求；固定输入域/环境/observable，不可见反例后改scope。
  核查位置：FEAgent five phases; §assessment/Eq1; normalized p20–29,67–79,111

**2610.04344 · Hierarchical Credit Assignment for RLVR on Fused Gromov-Wasserstein Geometry**

[论文](https://arxiv.org/abs/2610.04344)

- **post-training**：HarA用正确/错误轨迹各自hidden-state位置图FGW重心，按span到重心贡献赋予正/负不同幂credit再乘GRPO优势；真实多模型多基准，不能以欧氏token分数替换FGW。

**2610.04328 · Bidirectional Preference Synthesis: Learning Prompt-Conditioned Preferences from Boundary Failures**

[论文](https://arxiv.org/abs/2610.04328)

- **post-training**：BPS是独立离线偏好构造算法而非新loss：从部分失败生成student修正与安全/非泄漏achieved prompt，cycle-consistency验证后同一response pair在两prompt反向成crossed anchor，再标准DPO。IFBench及function-call有机制/下游实验；不把teacher同源的ranking诊断误当独立泛化。
- **agent**：BPS 将部分正确输出在原prompt作为 rejected，又为其构造真实已达成prompt成为 chosen，经独立teacher cycle-consistency筛选，混合forward/reverse pair做标准DPO。公开指令/工具bench可验证。
  复现边界：这是偏好数据算法，应归后训练交叉主题；不改DPO loss；reverse不得把事实/数学错误洗成正确；Gemini同teacher probe非teacher-independent泛化；rho约.195来自282验证通过。
  核查位置：BPS crossed-anchor construction; normalized p17–34,37–42,73–83

**2610.04318 · Rethinking Long-Video Efficiency: A Joint Allocation Perspective on Frames, Pixels, and Front-End Latency**

[论文](https://arxiv.org/abs/2610.04318)

- **foundation-model**：LoHi把一次解码的同一帧池分成低分辨率视频和少量高分辨率图像，统一token与前端解码预算；SemDiv用query相关性加DPP挑高分帧。
  复现边界：同预算5760视觉token仍不同解码帧数，应拆decode/encode/prefill；现代动态分辨率VLM适用，旧LLaVA未证实。熵门限在benchmark10%heldout调只属探索，需固定切分；双流靠文本cue而非新训练跨流模块。未找到官方代码链接。
  核查位置：§4.1–4.4 Eq2–6；§5 setup；Appendix C.6/E

**2610.04303 · What to Preserve in Recursive Computation: A Local Predictive Sufficiency Principle**

[论文](https://arxiv.org/abs/2610.04303)

- **foundation-model**：局部预测充分性用完整协方差平衡的ridge有限测试估计压缩缺损，并将真实optimizer proposal投影到分组预测约束半空间；覆盖语言记忆、TGN、VLA及递归策略，具备新可训练机制与对应控制。
  复现边界：理论population保证须独立样本/测试覆盖条件，不能把经验surrogate等同保证。TGN训练epoch1.9–2.2倍、参数+10.1%，推理±3%；VLA只heldout初始化非广泛OOD；SRI主表选择modifiedtask需另报全六任务。未来能力测试仍需匹配总训练算力。
  核查位置：§3.1–3.4/Algorithm2/Propositions2–3；§4/Table1–2；Limitations；Appendix E/Tables18–19

**2610.04299 · Questioning the Questions: Sustaining Self-Evolution in Reasoning Models**

[论文](https://arxiv.org/abs/2610.04299)

- **post-training**：R-Quest有效性初始化与采样成对新颖性门控改变questioner–solver自演化反馈；真实两家族实验。但正文按每域最高测试benchmark均值选checkpoint，复现必须另设validation，不能继承该选择为无偏正式成绩。

**2610.04292 · LMBuild: Evaluating LLM Agents for Generating Buildable and Functional Structures**

[论文](https://arxiv.org/abs/2610.04292)

- **agent**：LMBuild用可检索/生成零件的交互工具生成3D结构，按结构、功能、设计和物理实现分层评测，适合多模态coding-agent能力候选。
  复现边界：全部实验只200Core而非2549Full；三轮修订仅小幅改善，显式功能规格提升不能当自进化发现。物理可行评分是代理而非真的生产/装配，CAD来源许可证不同应逐件保留，不把医学器械设计当可用产品。
  核查位置：§2.2–2.3；§3.1/3.4；official repository

**2610.04261 · Playing social deduction games with reinforcement fine-tuned large language models**

[论文](https://arxiv.org/abs/2610.04261)

- **post-training**：社交推理/影响reward与同侧共享策略的GRPO应用；正文标准group normalization/PPOclip/KL，无新增优化器，归Agent环境研究。 该决定仅限后训练核心track，Agent方法/数据公共入口由Agent track独立判断，不能据此全局拒绝。
- **agent**：社交推理 RFT 在狼人/Avalon 对同阵营共享policy训练，私有可见角色+公共历史形成prompt；用隐藏角色预测和后续投票影响奖励，终局win作外部观察。明确游戏引擎可构建验证。
  复现边界：隐藏state只reward计算，不能给玩家完整gold角色；固定对手不能证明非平稳多智能体泛化；影响奖励非严格因果说服；模型盲评非真实人类交互，后者后续。
  核查位置：AgentEvolver Game Arena methods; normalized p110–133; social cognition RFT; Limitations

**2610.04225 · FlashGaze: Training-Free Multi-Scale Patch Pruning For Efficient Video Understanding**

[论文](https://arxiv.org/abs/2610.04225)

- **foundation-model**：FlashGaze 在视觉编码前按运动补偿误差选择 Drop/Merge/Keep，以三层四叉树动态规划满足像素预算。Qwen3-VL/NVILA 与公开视频基准可验证。
  复现边界：首帧完整保留且豁免预算；端到端 TTFT 必须包含预处理与视觉编码；H200 速度不可直接视为 A100 结果。
  核查位置：§3.1–3.3/Eq1–6/Algorithm1; §4.1; Appendix A/B

**2610.04204 · Clean: Second-order LLM Training at Linear Memory Cost via Nyström Sketching**

[论文](https://arxiv.org/abs/2610.04204)

- **foundation-model**：Clean/Q-Clean以Nyström双侧薄因子及四互补块moment降低优化器状态，定义足够明确且有LLM预训练实测，可作为新optimizer候选。
  复现边界：线性仅固定r的state非parameter/gradient/activation，r随d增长不保证渐近线性；13B展示fitmemory非完成13B能力训练；bestval和缩短sweep需冻结选择协议，无报告trainingseedCI；QClean12.10并非优于所有baseline。
  核查位置：§3 Eq6–16/Alg1；§4；§6 Table3/Fig5；AppA/B/D

**2610.04196 · Asynchronous Is Nearly Free for Evolution Strategies on Long-Horizon Agentic Tasks**

[论文](https://arxiv.org/abs/2610.04196)

- **agent**：AsyncES 以参数版本记录 rollout lag，接受 bounded-staleness 回报、按 accepted cohort 标准化奖励并更新中央 ES 参数；worker 恢复无扰动权重并重放更新后再扰动。
  复现边界：Qwen2.5-7B/ALFWorld，2083 train/100 validation/300 test；三 evaluation seeds 仅为同一训练 checkpoint，不是三训练 seeds。异步 lag=1 接近同步、lag=4/8退化；ES FLOPs 约 GRPO 3.99倍，不能只比墙钟。需真实模型扰动、丢弃与版本日志，不可 fixture 奖励替代。
  核查位置：§2–5、Appendix A/B

**2610.04178 · SHarP: Saliency-based Pruning of Agent Harnesses**

[论文](https://arxiv.org/abs/2610.04178)

- **agent**：SHarP 对手工定义 harness 模块逐一禁用，以 dev 任务分数/成本的相对中位数及 paired t-test 判断 saliency；保护显著性能贡献模块，按效率信号剪枝后独立评测。
  复现边界：四公开任务组；held-out 三次运行/任务。模块边界与耦合先定义，selection 仅 dev；p-value不是因果重要性或效应量。需真正禁用工具/指令/模块并匹配预算；成本公式 mean 与图 median 分开。
  核查位置：§3–4、saliency definition and pruning procedure

**2610.04152 · Kepler4D: Controllable Future Video Generation via 4D Scene State Evolution**

[论文](https://arxiv.org/abs/2610.04152)

- **foundation-model**：Kepler4D 通过 DA3、SAM2 和 VLM 获取观测对象代理，Chain-of-Motion 产生结构化运动并渲染 3D 控制给 VerseCrafter。DL3DV/DAVIS 可做条件化延续实验。
  复现边界：评测使用由完整视频估计的未来相机轨迹作为给定条件；禁止宣传为无条件预测，禁止未来帧进入初始状态；Dynamic Degree 不是运动正确率。
  核查位置：§3.1–3.4; §4; Appendix B

**2610.04140 · ExpertMuon-Compass: Alignment-Guided Step Sizes for Mixture-of-Experts Training**

[论文](https://arxiv.org/abs/2610.04140)

- **foundation-model**：ExpertMuon-Compass保持Muon矩阵方向，以familyalignment和rowalignment标量半径调整expert步长，独立tuningseed与配对评测充分定义训练operator。
  复现边界：4–7%wallclock额外；短8.2Mtoken明显未充分训练，262M/1.05B接近NorMuon，最有力是变化数据顺序；N/H与N/N必须区分避免把momentum更改归因Compass；FP32结果不直接外推BF16/大型MoE。
  核查位置：§3.1–3.4 Eq1–8；§4.1–4.4 Tables1–4；§5；AppA/C

**2610.04139 · From Sight to Foresight: Predictive Spatial Reasoning in Vision-Language Models**

[论文](https://arxiv.org/abs/2610.04139)

- **foundation-model**：SpatialMind 以有界对数深度修正、度量和运动编码对齐视觉 token，分 GROUND/CURRENT/DYNAMICS/FUTURE 训练状态链与答案。外部 VSI/OSI/VLM4D 支持迁移检验。
  复现边界：自建 30677 训练 QA/2000 benchmark 的实际发布需后续核验；未来状态只能作为训练目标和离线评分，推理只读观测前缀。
  核查位置：§3; §4/Eq4–6; §5.1–5.3; Appendix A–C

**2610.04134 · Agentic Resource Allocation for Batch Multi-Objective Bayesian Optimization in Autonomous Materials Discovery**

[论文](https://arxiv.org/abs/2610.04134)

- **agent**：MultiTaskGP 在每轮 qEHVI 与 diversified qUCB 六种配比之间分配实验batch；LLM根据近期HV/MI、历史和预算事件选择option，Adaptive还选β。
  复现边界：25配对seed，但ground truth是数据拟合random forest而非真实材料实验；HV reference使用全枚举oracle空间，只能作为离线评分，不给决策器未来真值。预算变化预告一轮、离散空间与每组q=5固定；不声称现实发现因果提升。
  核查位置：§2.2–2.6、optimization campaigns、Data availability

**2610.04132 · PB-GRPO: Learning Socially Adaptive LLM Agents from Persona-Driven Simulation with Preference-Batched GRPO**

[论文](https://arxiv.org/abs/2610.04132)

- **post-training**：PB-GRPO保持prompt-local均值，但在同潜在偏好bucket内合并方差作为分母；128训练persona/100未见persona真实Qwen7B，初步单设置证据需保守。
- **agent**：PB-GRPO保持prompt-local均值，但在同潜在偏好bucket内合并方差作为分母；128训练persona/100未见persona真实Qwen7B，初步单设置证据需保守。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§3公式；§4/Table1

**2610.04118 · LongSocialBench: Do Long-Context LLMs Understand Online Discussion Threads?**

[论文](https://arxiv.org/abs/2610.04118)

- **foundation-model**：LongSocialBench公开1462题/94完整讨论及精确MCQ协议，长上下文结构化社会推理覆盖有价值；只纳入无gold推理评测，oracle单列diagnostic。
  复现边界：正文只对parsed responses计accuracy须同时报告coverage/invalid全分母结果；Gold-Scope和criterion-label带gold不得evolve优化能力；公开数据只有test需冻结episode级holdout避免泄漏；README旧Tracyyyy1997命名与页面xinyiliu-research应pin实际revision；未发现完整作者runner。
  核查位置：§3；§4；§5.5–5.6；AppD.2/I；官方HF README

**2610.04047 · Periscope: Extending Frozen Language Models Beyond Their Context Window**

[论文](https://arxiv.org/abs/2610.04047)

- **foundation-model**：Periscope明确给出冻结模型的局部/跨距探测与证据图，可作为长上下文推理和retrieval算子候选。
  复现边界：每token读两次，9k不是总处理量；W²/c是长度界非准确率保证。单probeKV不同于批量residentmemory；应计全部probe和embedding/readback模型。finite-choice单tokenreadout限制、多文档弱；top20缺选项fallback需代码单测。
  核查位置：§3；§4.2–4.3 Tables1–4；§5–6；App A.1/A.2；作者README

**2610.04009 · SUAVE: Unified Video-Action Models via Masked Diffusion**

[论文](https://arxiv.org/abs/2610.04009)

- **foundation-model**：SUAVE统一离散视频/动作masked diffusion为真实新模型训练候选。
  复现边界：实际不生成语言/不测语义泛化；co-trainingvs仅pretrain统计不可分，single-seedbootstrap只是rollout不确定性。真实1.03schunk5action不等5Hz闭环，reported2.5actions/s。tokenizer限制FVD，未定位作者独立代码库。
  核查位置：§III-A–D；§IV-A–C；§V Limitations

**2610.04008 · SkillScriptBench: Benchmarking Self-Evolution of Executable Agent Skill Packages Beyond Markdown**

[论文](https://arxiv.org/abs/2610.04008)

- **agent**：SkillScriptBench评估SKILL.md和脚本一致性，AST-guided revision绑定需求到唯一语法节点，局部修改并显式保留正确行为，适合可执行skill/RSI迭代候选。
  复现边界：350任务中300故障和50clean分开，Pass@3与三次全成功不同；surrogate verifier必须独立于隐藏官方test。基于原/初修版本的unique匹配失败应fail-closed，不能不受控覆盖用户代码；公开作者数据包仍需核验。
  核查位置：§2.1–2.4；§3.1–3.4；§4.1；Appendix A/D

**2610.04002 · Do Language Models Need a Trainable Input Embedding Table? Fixed Minimal Token Codes at 1.7B-Class Scale**

[论文](https://arxiv.org/abs/2610.04002)

- **foundation-model**：固定最小二进制token身份+确定lift可作为可执行架构/机制诊断变体，公开checkpoint；不作为质量或效率优胜算法。
  复现边界：只是无trainable input table非lookup-free或无embedding函数；参数/几何/输入尺度同改；单run且resume不恢复sampler游标，未等FLOPs；无测得系统优势，MMLU/CSQA近chance。
  核查位置：§3.2–3.5；§4.1–4.4；§5/Table2；§8/AppE

**2610.03994 · Solving VeriContest with a Lean-Backed Rust Verifier**

[论文](https://arxiv.org/abs/2610.03994)

- **agent**：Rust-Prover 将 Verus spec 转 Rust specification、由 Charon/Aeneas 转 Lean，proof agent给定不变代码/theorem迭代证明，干净clone复核byte identity与Lean axioms。
  复现边界：1007problem/1325theorem是公共固定benchmark；349spec未经全量测试、translation仅部分差分覆盖，翻译器在信任边界。禁sorry/admit/native_decide/bv_decide；public Verus proof可能提供先验，未见Lean证明不等于无间接污染。不能以字符串proof成功代替Lean kernel。
  核查位置：§3.1–3.4、§4、§4.5

**2610.03984 · Teaching Agents to Code Reliably**

[论文](https://arxiv.org/abs/2610.03984)

- **post-training**：在mutation/sibling补丁上给测试断言按加权coverage Shapley credit，门控正轨迹优势再注入assertion token，属新credit机制；gold tests仅scorer可见。全500例先诊断后230训练270holdout，不应宣称完全未接触测试。
- **agent**：在mutation/sibling补丁上给测试断言按加权coverage Shapley credit，门控正轨迹优势再注入assertion token，属新credit机制；gold tests仅scorer可见。全500例先诊断后230训练270holdout，不应宣称完全未接触测试。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§2.3 Eq.2–5；§3

**2610.03938 · MLLMs Fail to Refuse when Using Tools Agentically**

[论文](https://arxiv.org/abs/2610.03938)

- **agent**：同一MLLM在no-tool与ReAct四视觉工具条件下配对，测拒绝失败；按tool次数诊断context dilution，并逐轮重注入原请求比较缓解。
  复现边界：三公开视觉安全集、11模型，RFR是GPT-5.2judge拒绝代理而非真实危害结果；tool次数相关性不单独证明因果。Gemini native agent工具不可控制，另报。须真实图像/OCR/tagging/crop执行，re-injection不是完全防护。
  核查位置：§3.1–3.2、§4.1–4.3、§5、Appendix A–D

**2610.03894 · Proxy Confidence: Auditing Black-Box LLM Agents with a Surrogate's Log-Probabilities**

[论文](https://arxiv.org/abs/2610.03894)

- **agent**：ProxyConfidence 用独立开放 surrogate 的 teacher-forced/PMI与YES-NO/tool竞争logprob为blackbox actor行动打分，按regime校准方向后融合，并用于audit/修正选择。
  复现边界：BFCL/xLAM/AppWorld等可判定工具任务，外部事实不可从context判断时无保障。teacher-forcing符号会反转，orientation只能validation确定，不可跨regime复制；actor去标识影响复刻、≤8B scorer未测、多租户latency未测。
  核查位置：§3–7、§9、readout definitions

**2610.03820 · From Requirements to Attack Trees: Grounded LLM Agents for Design-Time Security Review**

[论文](https://arxiv.org/abs/2610.03820)

- **agent**：从需求与架构图抽取带信任边界的实体图，按目标分派攻击树 worker；联合验证后只重建受影响分支，保留稳定 ID，最多三次。公开 Microsoft IoT Edge 威胁模型可作为参考任务，核心流程可进入安全 Agent 实现队列。
  复现边界：合成 OLB/EHS 各12威胁与开放案例不可混为统一覆盖率；开放案例无完整 gold，一名专家评分无评审者一致性。相同 seed 重复调用不是独立训练种子；建议架构未证明已实现安全，PRD/图仍是可信输入，未验证提示注入防御。未定位原作者代码 URL。
  核查位置：§3.2.1–3.2.6 grounding / attack-tree / validation；§4–6 evaluation

**2610.03796 · ProsaBuddy: Assisting Mechanized Real-Time Schedulability Analysis with LLM-based Agents**

[论文](https://arxiv.org/abs/2610.03796)

- **agent**：ProsaBuddy primary两阶段lemma decomposition+领域guidelines/skills→隔离subagents，Rocq结果在独立OS进程AST审计：proofbody仅ProofStep/Query，外部只允许trustedimports，库readonly，禁止改theorem/axiom。17lemma成功、去skills12/去decomp14/去paperhints15；完整headline含人工proofhint必须分为hint-assisted不当无gold能力。Audit TCB超kernel未形式验证，难题弱模型省略非全矩阵。
  核查位置：§III-B–E；§IV-A–C；§V

**2610.03780 · OceanMind: A multi-agent AI system for ocean diagnosis**

[论文](https://arxiv.org/abs/2610.03780)

- **agent**：OceanMind 六角色按 query routing→skill planning→确定性工具编排→证据综合分析海洋状态，缺工具由受限 CodingAgent 补充，数据 artifact 通过引用与 role-specific memory 传递。
  复现边界：CMEMS公开但部分 in-situ CTD需申请；定量诊断不等于通用Agent提升，gold chain仅评分。first-pass、四门槛通过与step效率分别记录，效率惩罚少步骤也惩罚多步骤。案例单次web响应、默认采样不支持统计优势。
  核查位置：Methods: agent architecture、benchmark; Data/Code availability

**2610.03741 · Logit-Aware MIMO AirComp for Distributed Mixture-of-Experts LLM Inference over Wireless Edge Networks**

[论文](https://arxiv.org/abs/2610.03741)

- **foundation-model**：以有限差分估计MoE聚合块对next-token logits敏感度，驱动有功率约束的MIMO AirComp收发器加权优化，可做无线噪声条件下的模型机制诊断。
  复现边界：无线模拟器、隐藏状态高斯扰动回放和295例ARC闭环是三种不同证据；不能将500例GSM8K回放当真实无线部署。额外forward/CSI/敏感度刷新成本须计入，更多SNR/channel seed和完整基准未建立。
  核查位置：§III-A–C Eq17/34/35 Algorithm1；§IV-A/C/E

**2610.03695 · Language Models that Play Chess and Explain Their Moves**

[论文](https://arxiv.org/abs/2610.03695)

- **foundation-model**：Queen 连接冻结 Leela 棋局编码器与 SmolLM3，先四阶段空间/时间课程，再依据 Stockfish 核验的递归子局解释进行七轮自进化 SFT。Lichess/公开棋引擎与持出棋题可验证。
  复现边界：Stockfish 是明确的训练与验证 oracle，不是无教师 RSI；语言裁判不能替代合法性/PV 错误检验；应隔离根局面和测试棋题。
  核查位置：§3.1–3.3/Algorithm1; §4.1–4.3; Appendix A/B

**2610.03632 · World Embedding Benchmark**

[论文](https://arxiv.org/abs/2610.03632)

- **foundation-model**：World Embedding Benchmark公开物理视频/文本检索、回归、pair判别及新模型评测入口，适合作为embedding物理理解公共评测基础设施。
  复现边界：同物理族参数迁移非完全新规律OOD；JEPA只做回归与MLLM直接pair不可跨任务排序；contrastive适配改善检索却损伤回归。需冻结family/split manifests，公开test不能evolve反复选参。
  核查位置：§2.1–2.2；§3.1–3.3；官方README Evaluation

**2610.03631 · NeutronGym: Physics-Graded Neutron Instrument Design for LLM Agents**

[论文](https://arxiv.org/abs/2610.03631)

- **agent**：NeutronGym 22 MCP tools管理McStas真实仪器、缓存编译后参数仿真；syntax/runtime/structure/science四级reward，程序化族经过无模型规则及固定答案shortcut admission，再GRPO训练。
  复现边界：核心必须实际McStas仿真不能LLM judge；固定layout参数任务不等于topology设计。T3 unscored、两隐藏参考未公开，9reward failure披露；11→77为一族，第二seed69，其他族部分单seed，非设施实测证明。
  核查位置：§3、§4–5、§6、Appendix B/G

**2610.03591 · HazardWeaver: Scientific Route Selection for Hazard Analysis Agents**

[论文](https://arxiv.org/abs/2610.03591)

- **agent**：HazardWeaver 从文献编译Satisfied/Violated/Unresolved科学条件，以typed capability graph找可执行route，LLM在两者交集选择/修复，独立hidden route/时点/provenance/预算评分。
  复现边界：141 sealed科学任务及11track，模型/solver必须真实产物；未找到route≠证明无可行route。DCA与native科学误差分开，不把异质数字合一；gold route和cutoff后数据隐藏，领域图注册范围决定可验证性。
  核查位置：§3.1–3.4 Eq2–8、§4、Appendix A/C/E

**2610.03585 · Threat-Preserving Representation Sensitivity in Agent-Security Benchmarks**

[论文](https://arxiv.org/abs/2610.03585)

- **agent**：TPRS 固定任务、harm objective、policy、scorer与环境，仅替换tool representation，对ASB/MCPTox/AgentDojo分别量化ASR与benign utility。
  复现边界：28904runs；ASB A2改任务仅diagnostic，部分名称变化不语义等价，不能归因为威胁词单因素。MCPTox form-matched neutral control解释多数变化；按benchmark独立比较，invoke与committed成功定义不可混。
  核查位置：§III methodology、Tables I–III、limitations

**2610.03574 · HyperBrowseComp: A Multilingual and Multimodal Stress Test for Web-Browsing Agents**

[论文](https://arxiv.org/abs/2610.03574)

- **agent**：HyperBrowseComp 423人工多语/多模态证据链短答，以no-internet过滤容易题；统一ReAct25步与provider-native/Exa/OWL三条件，保存实际web trace和短答judge。
  复现边界：13语stress-test非自然查询分布，live web时点/地域漂移。OWL distinct harness不能只归于model；2400s失败留denominator。encoded dataset deliberate解码，gold/solution trace不能给actor；same-model judge敏感性小但不无偏。
  核查位置：§3.1–3.2、§4.1–4.4、Appendix B、Limitations

**2610.03524 · From Benchmarks to Production: A Text-to-SQL System for Complex Financial Data**

[论文](https://arxiv.org/abs/2610.03524)

- **agent**：FLINT lookup从reference表解析opaque ID，检索专家query bank结构示例，FK-chain schema linking→SQL→执行error reflection；多步骤并行。
  复现边界：核心金融数据私有，但Appendix G四公共域可复现配置路径。查询bank与评测disjoint，人工规则成本实报；执行成功≠语义正确，AST/output/judge分级评分且read-only SQL。生产部署非量化A/B，不提升为工业搜广推证据。
  核查位置：§3.1–3.6、evaluation、Appendix G、Limitations

**2610.03516 · XGenAct: Geometry-Enhanced World Action Models through Cross-Task Generation**

[论文](https://arxiv.org/abs/2610.03516)

- **foundation-model**：XGenAct确定性几何codec与共享视频flow任务混合，可作world-action联合训练候选。
  复现边界：几何模态在训练具有sim标签，部署不可用未来GT；futureperception按本策略行动后sim状态评分，≥10mm执行偏差排除须另报coverage。最优menu依task，不能test挑menu；代码权重仅承诺将发布，未核到公开仓库。
  核查位置：§3.1–3.4 Eq1–6；§4.1–4.4；App B/C/E/G/H；Reproducibility

**2610.03448 · Passing the Test You Trained On: Re-evaluating Prompt-Injection Detectors for LLM Agents**

[论文](https://arxiv.org/abs/2610.03448)

- **agent**：重评15 injection detectors：差分replay构造clean/injected tool输出，按default阈值/lowFPR测TPR，审训练重叠，并用task-aware yes/no logprob judge诊断缺失任务语境。
  复现边界：低1%FPR阈值在评测benign集选择仅乐观上界，部署须独立calibration；gold toolcall只为固定数据生成不供受测agent。合成YAML/JSON输出与真实web差异、固定template非adaptive attack，去重同权重InjecGuard/PIGuard。
  核查位置：§4.1–4.4、§5、§6、Appendix C

**2610.03389 · From Patching to Pruning Visual Computation in Vision Language Models**

[论文](https://arxiv.org/abs/2610.03389)

- **foundation-model**：P2P 用视觉投影缓存均值替换分析，前缀/后缀敏感度扫描选择安全层，真实跳过视觉 attention/MLP，可结合 patched-graph LoRA。公开七基准与独立 proxy/validation/test 可复现。
  复现边界：必须真实绕过算子才可声称加速，不能 dense 计算后替换；保留两个连续失效边界与 3% 容忍协议。
  核查位置：§3; §4.1–4.5; §5.1; Appendix A.6

**2610.03315 · Lightweight, Rubric-Guided Trajectory Evaluation for Production AI Agents**

[论文](https://arxiv.org/abs/2610.03315)

- **agent**：LiteTrajEval 离线domain rule profiles，在线规范化trace/弱failure hints，格式compaction+重复引用、tier waterfall预算与MMR证据选取，单rubric judge输出故障诊断。
  复现边界：公共Magentic-One/τ-retail轨迹；规则与预算仅dev构建，human failure annotations仅评分。字符budget非token数；hardtruncate保留路径可能损失证据。成本减少不等于task能力提升，弱heuristic hints不是groundtruth rootcause。
  核查位置：§II.A–D、Eq1–3、Algorithm1、evaluation

**2610.03226 · D2K-Bench: Can LLM Agents Turn Expert Designs into Efficient GPU Kernels?**

[论文](https://arxiv.org/abs/2610.03226)

- **agent**：D2K-Bench 配对26task/85workload有无专家L1–3设计guidance，agent iterative Triton编辑/compile/profile/submit；数值与stateupdate、implement validity全通过才按geomean speedup选候选。
  复现边界：B200实测原结果不能移植为A100性能；本项目若实现CUDA必须A100/A30 receipt。专家source隐藏、source judge隐藏timing，指导不含tuning参数。生成期间workload feedback不是heldout泛化；objective score与LLM design rubric分开。
  核查位置：§2.1–2.3、§3.1–3.3、§4、Appendix evaluator

**2610.03213 · Toward SLM-based agentic task-tool intent matching**

[论文](https://arxiv.org/abs/2610.03213)

- **agent**：Gemma task-tool relevance 以Base→GEPA→LoRA SFT→DrGRPO curriculum，deterministic格式/标签/长度reward，候选逐工具Boolean判断。
  复现边界：12 MCP servers分server-disjoint；selection validation F1，test冻结。parse失败计E2E失败，成功parse分类指标另报。数据从tool description合成且curator筛选，不证明真实多工具执行能力；95%为人工门槛，非安全保障。
  核查位置：§2.1–2.3、§3、§4

**2610.03199 · Predicting and Repairing Merge Collapse in Large Language Models**

[论文](https://arxiv.org/abs/2610.03199)

- **foundation-model**：Prism对norm缩放后平均taskvector按跨专家方差softthreshold，并用cancellation/dispersion门避免删独有知识；确定性数据自由repair定义完整。
  复现边界：通用阈值1.9e-3只在考察family规模，不能当架构不变量；repair常回base水平不代表融合全部能力；安全未评。须保留显式系数双缩放与normmatched控制，不能误当standard平均。
  核查位置：§3.1–3.3 Eq1–3；§4.1–4.3 Eq4–5；§5.1–5.5/Table4；§6

**2610.03198 · KV$^2$: A Self-Refining KV Cache**

[论文](https://arxiv.org/abs/2610.03198)

- **foundation-model**：KV²用KeyDiff跨层/头均值选chunk内稀疏重构query，append在完整cache后做真实因果前向；局部max-attention评分合成全局保留，也可迭代替换proxy。已在原队列，补全证据不重复计新文。
  复现边界：重构query位置是context之后，不是原位置；global-conditioning/local-scoring需保留。作者kvpress实现仅mask并未物理compact，因此只证压缩阶段runtime/memory，不能宣称decode缓存节省。多轮refinement可能更慢，完整evolve未接入。
  核查位置：§3 Eq1–4；§4.1；§5.1–5.4；Limitations

**2610.03190 · Not Until the Evidence Says So: Teaching LLM Investigators When to Close a Case**

[论文](https://arxiv.org/abs/2610.03190)

- **post-training**：Nautil提供证据索引/request工具、close/open任务、来源内balanced accuracy及删关键证据对照；官方MIT代码/数据/模型公开。RLVR checkpoint选择用过64测试中22条，必须改验证集隔离，不能照搬其headline为无泄漏泛化。

**2610.03123 · Foresight: planning future perception in streaming VLMs without retraining**

[论文](https://arxiv.org/abs/2610.03123)

- **foundation-model**：Foresight 将共享冻结模型分为写入视频的 Ingest 与只读快照的 Think；规划采样率、保留类别、压缩和响应时间。StreamingBench/OVO 允许真实因果流式验证。
  复现边界：匿名补充实现/完整 harness 尚未公开核验；必须只读当前视频前缀、计入异步墙钟时间；20% 校准与 80% 持出不能混用。
  核查位置：§3.1–3.2/Algorithm1; §4.1; Appendix H/Table10

**2610.03102 · Ask, Relax, or Act? Evaluating Actionable Indeterminacy in LLM Preference Reasoning**

[论文](https://arxiv.org/abs/2610.03102)

- **agent**：Ask/Relax/Act 以admissible preferences/objectives下accepted action交集判定可行动/需问，infeasible则最小允许repair；四finite结构exact solver生成matched intervention pairs。
  复现边界：4320prompts/36cells，exactchecker而非LLM judge；gold completions/solutions隐藏。单source不解决多源priority。BareJSON/Markdown拒绝与reasoning失败分开，FC与decision/IFC分报；工具调用不是必需且不能声称现实决策效果。
  核查位置：§2.1–2.2、§3–5、Appendix M/O

**2610.03099 · Beyond Single Videos: Benchmarking and Active Evidence Seeking for E-Commerce Cross-Video Reasoning**

[论文](https://arxiv.org/abs/2610.03099)

- **agent**：AdsCVR/AdSeek 多视频frame/audio选择逐轮证据，GRPO correctness+.1format，过滤no-tool/zero-var group并最多三次resample；teacher诊断missing evidence/reasoning→定向rectify→assistant-mask SFT。
  复现边界：训练gold可reward/teacher使用，测试actor只metadata与真实perception。需要原视频和真实Qwen-VL/ASR工具，fixture文字不是多模态能力。Teacher成功条件筛选有额外成本，corrected append仅train；73.57与混合源74.30分开。
  核查位置：§3、§4.1–4.3、§5、Appendix B

**2610.03089 · Securing Computer-Use Agents Against Branch Steering Attacks**

[论文](https://arxiv.org/abs/2610.03089)

- **agent**：COBRA trusted-input预规划并承诺程序，BRH以先定branch/field约束解析观察，HTTP/MCP代理强制operation、参数、approved schema hash；fused5plans保留合法alternative。
  复现边界：恶意观察仍能选合法branch但不能扩权限；无approved sitemap仅domain allowlist弱约束，非HTTP GUI effect在边界外。真实browser/proxy必须运行；OSWorld matched86与MCP全套不混，multiple-attempt预算与单plan区分。
  核查位置：§3–5、Appendix A/D/E/F

**2610.03084 · NegT2IBench: When Negation Changes the Picture. A Polarity Benchmark for Text-to-Image Models**

[论文](https://arxiv.org/abs/2610.03084)

- **foundation-model**：NegT2IBench以六类4800个正负属性/关系prompt和对象存在性先决条件，用detector/SAM/depth/SigLIP2逐条判分；可补图像生成的否定遵循评估。
  复现边界：模糊dead-zone时正关系失败、负关系通过，是协议选择不能当严格逻辑真值。image accuracy与4图任一成功prompt accuracy分开；140明确人评图参与阈值比较需另留独立评估。六类等权不是所有模型普适视觉能力。
  核查位置：§3.1；§4 human validation；§5；Appendix C.1/C.3/E.2

**2610.03063 · HARPO: Hallucination-Aware Reinforcement Learning for Faithful and Creative Language Generation**

[论文](https://arxiv.org/abs/2610.03063)

- **post-training**：HARPO训练hallucination-span reward model，只有预测零幻觉才激活写作reward，并配创作到忠实cosine课程；属层级多目标reward机制，不是新的GRPO；gate不保证真实无幻觉。

**2610.03039 · HyperThink: Text-to-Parameter Hypernetworks for Efficient Reasoning**

[论文](https://arxiv.org/abs/2610.03039)

- **foundation-model**：HyperThink以查询生成冻结LLM层bias并经VQ约束，保留独立算法候选。
  复现边界：不是完全零附加compute；需包含queryencoder/hypernetwork和5samples，不能与单sample混比。训练2H200、测试1H200未替代本仓A100验证。代码声明未来发布，未找到公开实现；epoch/commitment细项接入前固定，选超参不可用MATH500测试。
  核查位置：§3；§4 Tables1–2/Fig4；App C；Reproducibility Statement

**2610.03036 · WebFovea: When the Model Is Right but the Click Is Wrong -- Reliable Round Trips for Vision-Based Web Agents on Live Websites**

[论文](https://arxiv.org/abs/2610.03036)

- **foundation-model**：WebFovea网页agent harness加固，由agent track审查。
- **agent**：WebFovea hardens视觉action roundtrip：解析特殊token、坐标space映射、select/fill实际读回、反馈状态、五截图history与bounded DOM text通道，executor约束动作预算。
  复现边界：核心是真实browser执行可观测结果，不fixture点击。仅ClaudeOpus4.6，dev70/holdout30，16site不可达后25scorable不能静默删 denominator。31→57四官方提交不是同模型随机A/B；每组件1–24小样本，liveweb重复波动。CAPTCHA工具不在本轮执行范围。
  核查位置：§4.1–4.6、§5.1–5.5、§6.2、Appendix A

**2610.03034 · Adaptive Second-Order Solvers for Fast Stochastic Diffusion Sampling**

[论文](https://arxiv.org/abs/2610.03034)

- **foundation-model**：PI 扩散求解器基于 stochastic Heun 一二阶误差和前次误差调步，将自适应轨迹聚合为静态模态专用时间表。FFHQ/ImageNet64、LM1B 与公开 EDM 检查点可验证。
  复现边界：需保留拒绝步骤与随机过程处理；公平比较平均 NFE 而非只看步数；LM PPL 改善伴随熵下降；时间表不能跨模态无条件复用。
  核查位置：§4/Algorithm1; §5; §6.1–6.4; Appendix B–D

**2610.03020 · DyadMem: A Long-Term Memory Benchmark of How Agents Work with Users**

[论文](https://arxiv.org/abs/2610.03020)

- **agent**：DyadMem 分Capture/Update/Recall与full pipeline，six memory types含agent-user协作URAM，chronological delete/add/dedup，terminal valid-bank recall与grounded QA并测。
  复现边界：standalone Update/Recall和GoldMemory QA显式gold-conditioned diagnostic，不得当无goldagent；能力需模型自建bank。no-change排除Update score另报，empty/parsefailed不删。QA文本0/1表述有不一致须以公式/code核定；judge与semanticmatcher阈值冻结。
  核查位置：§3.1–3.3、§4、Appendix G

**2610.03014 · Beyond Predefined Sinks: Security-Aware Dependency Analysis for LLM Agents**

[论文](https://arxiv.org/abs/2610.03014)

- **agent**：AgentSecGraph permissive sensitive-op anchor→framework normalization→typed Security-ADG，Python AST backward trace识别覆盖constant切断，JS lexical trace，保留guard/trust-boundary provenance。
  复现边界：may_guard不是安全证明、matchedsink不是漏洞；local dependency有限、alias/dynamic/TS type不完全；敏感case待披露部分不公开。真实source snapshots冻结，precision/coverage与attackability分开，不输出自动漏洞保证。
  核查位置：§3.1–3.4、§4、§5.3、Data availability

**2610.03002 · Recursive Self-Improvement in Unified Multimodal Models**

[论文](https://arxiv.org/abs/2610.03002)

- **foundation-model**：统一多模态RSI以执行验证的绘图程序产生训练真值，诊断仅决定数据分布，分别更新生成/理解专家再合并，具备同训练步数与同verified数量控制，可作为多模态自改进研究候选。
  复现边界：新bench仍由同模型家族U0评分需独立外部审计；StructT2I11.0→11.9很小且continued11.7，BizGen约4%；MMBench -2.6/MMMU -3.0。不能把对chart的改善推广通用自改进。
  核查位置：§2.1–2.5 Eq1–4；§3；§4.1–4.5 Tables1–3

**2610.02986 · OLMo-Detect: A Multi-Stage, Confounder-Controlled Benchmark for Membership Inference on Large Language Models**

[论文](https://arxiv.org/abs/2610.02986)

- **post-training**：OLMo-Detect是跨pre/mid/post训练membership审计任务，member/nonmember按质量、时间、词汇匹配，15无监督/3监督MIA与dev/test分离；官方仓库有数据和评分pipeline。评估成员识别/污染风险，不等同提升LLM推理。

**2610.02970 · A Guideline-Augmented Multi-Agent Framework for Schema-as-Code Biomedical Named Entity Recognition**

[论文](https://arxiv.org/abs/2610.02970)

- **agent**：GAMA 从train gold归纳annotation rules并按train支持验证，TopN/type guideline memory→ranked span/type plan→schema-as-code→grounding/type/structure双环修复。
  复现边界：五公共BioNER数据，testgold绝不用于规则或修复，N/attempts validation冻结。结构有效不等于NER正确，exactspan/type F1同预算比较；无新增trainableparameter但LLM calls/induction成本要计。
  核查位置：§III.A–E、§IV experiments

**2610.02952 · GTDD: Generative Test-Driven Development for AI Coding Agents with Adversarial Testing**

[论文](https://arxiv.org/abs/2610.02952)

- **agent**：GTDD candidate/config先commit，source-informed或blind tester生成valid input不生成期望输出，可信reference差分、最短prefix/operation删减、最多k反馈；fresh审计与开发tests分离。
  复现边界：新审计是条件独立随机样本且protected材料restore，population结果不给coder/tester。600历史候选freshaudit分析是精确概率计算非真实gate执行试验；known-test通过不证明generalization。jointrepository与simultaneous-family multiplicity不同，acceptance规则不可混。
  核查位置：§3.1–3.3、§4、§5–6、Appendix B

**2610.02951 · Dynamic Expert Pruning for Multi-Agent Systems**

[论文](https://arxiv.org/abs/2610.02951)

- **foundation-model**：DEP已在既有队列：请求级文本encoder+MLP预测逐层expert topK，影响标签BCE与softmask自蒸馏KL联合训练，CPU专家池向GPU槽位差量加载；维持候选不重复新增。
  复现边界：K>=router k且tie须精确预算；shared experts不剪。路由mask不等于省显存，需真实host expert residency/delta transfer；每retention训练一个predictor，输入只当前可得prompt/context，不看未来agent生成。原文pruned仍落后dense，不能宣传免费压缩。
  核查位置：§3.1–3.4 Eq1–6；§4；Appendix H
- **agent**：DEP prompt+input小encoder/MLP预测逐层topK expert mask，REAP impact BCE与dense→softmasked self-KL联合训练；router -inf约束、delta-load host tensors只换差集。
  复现边界：训练calibration transcripts与evaluation隔离，K≥routerk，ties需确保恰K。masked routing≠显存节省，必须真实resident buffers与delta-transfer测量；prefetch仅已知workflow topology。accuracy比dense仍下降、每retention训练一predictor，CUDA路径需A100/A30实跑。
  核查位置：§3.1–3.4、§4、Appendix H

**2610.02928 · Discriminating Fixture Coverage in Agent-Infrastructure Verification Suites**

[论文](https://arxiv.org/abs/2610.02928)

- **agent**：Discriminating Fixture Coverage 冻结projection suite/hash后对外部mutants测kill，instrument区分未激活与污染未可见，按预测七input维度加fixture、原oracle不改复测。
  复现边界：5/10 challenge-set不是自然fault检测率，repair10/10同challenge不是第二heldout。optionalhook skip需单列、first/higher-order mutants分开；能力是软件verifier覆盖审计非Agent task提升。
  核查位置：§3–5、Table1、§6

**2610.02925 · Positive-Unlabeled Learning for Agent Safety False Alarm Auditing**

[论文](https://arxiv.org/abs/2610.02925)

- **agent**：Safe-alarm PU ranking以OOF role boundary transfer TN、mass-constrained soft-protection减弱误警负梯度；frozen references median rank/reliability-gated distillation，hierarchical TN与cross-alarm约束KL rank refinement。
  复现边界：targetfeatures transductive可用但safetylabels sealed，40TN/510targetalarm小样本；softmass非全局FP prevalence，安全monitor冻结。不是自动取消警报，Topbudget仅human审查排序；reference共享bias不由agreement消除，所有三个stage需真实训练非heuristic替换。
  核查位置：§3.1–3.3 Eq1–8、§4.1、Appendix A/B/C

**2610.02887 · Revealing Epistemic Uncertainty in MLLMs via Causal-Invariant Masking**

[论文](https://arxiv.org/abs/2610.02887)

- **foundation-model**：CIM 对保留问题相关 ROI 的遮罩输入比较语义分布，以 EED 期望嵌入漂移估计不确定性。VQAv2/OKVQA/AdVQA/POPE/MME 有公开数据与等采样预算对照。
  复现边界：因果不变性依赖 ROI 质量，不能视为已证明的因果识别；保留遮罩生成、校准与 AUROC，而非仅合成分数。
  核查位置：§3.2–3.4; §4.1–4.2; Appendix C.8/E

**2610.02885 · PsyEvo: A Personalized Counseling Agent That Self-Evolves at Test Time**

[论文](https://arxiv.org/abs/2610.02885)

- **agent**：PsyEvo HBSP固定population skill prior加client Gaussian posterior采样，SOCA双顺序agreement DAG选回复与mean-preserving ordinal delayedcredit；session间group-normalized weighted DPO更新shared LoRA。
  复现边界：shared cohort在线适配是test-time training条件，不是冻结heldout；client memory私有、adapter session内固定且更新仅影响新session。external judge不回馈learning，内部反馈与报告分离。模拟counseling偏好不等于临床疗效，human小样本不能宣称治疗安全；需实际adapter loss更新。
  核查位置：§2.1–2.4 Eq2–9、Algorithm1、§3、Appendix G/H/I

**2610.02880 · Found but Not Read: When Extracted Text Closes the Retrieval-Reading Gap in Document Vision-Language Models**

[论文](https://arxiv.org/abs/2610.02880)

- **foundation-model**：FoveDoc-Bench固定ColQwen2 top16页，对比同页图像与图像+CPU OCR/PDF text，lexical top16块各300字符；适合区分检索与读取瓶颈的受控诊断。
  复现边界：PDF真文本是上界，gold evidence crop/recall只是诊断不能作为常规检索输入。FoveDoc收益13–16pp而MMLongBench总收益约0.004，图表可能受损；1173文档与训练/验证QA隔离，按模态和recall分层。
  核查位置：§2 paired protocol；§4–6

**2610.02876 · Seeing, Saying, but Not Using: From Reportable Spatial Facts to Usable States in Multimodal Large Language Models**

[论文](https://arxiv.org/abs/2610.02876)

- **foundation-model**：OSS 对同一空间事实规范化并跨上下文对齐，以答案、状态对齐、状态轨迹三池标准自回归训练。派生样本继承 observation world 的原始切分，可验证 SpaceConflict 三类与成对评分。
  复现边界：注入真实状态仅 oracle 诊断；训练状态目标不能来自验证/测试世界；公开仓库链接为论文给出，尚未本轮核验可访问性。
  核查位置：§2.1–2.3; §4.1–4.3; §5.1–5.4; Appendix D.3/D.4

**2610.02856 · Adaptive Mutual Distillation for Balanced Multi-Task Post-Training of Large Language Models**

[论文](https://arxiv.org/abs/2610.02856)

- **post-training**：AMD对MFT/平滑SFT两分支互蒸馏，三类全局短probe从相同状态试增减/保持权重，丢弃probe参数后按各任务方向validation选择；6基准多骨干实测，probe成本必须计入。

**2610.02841 · How Robust Is Multimodal Claim Verification to LLM Rewriting?**

[论文](https://arxiv.org/abs/2610.02841)

- **foundation-model**：SciClaimEval同claim配支持/反驳图像，比较自然改写和单词注入引起的verdict变化，可作为多模态判别与reward鲁棒性诊断。
  复现边界：704dev/872test配对后样本，10条推理采样得到0.1步长support概率，不是logprob校准。改写可能改变语义，CT数值hedging须审核；仅一语料一主rewrite模型，不能宣称通用事实验证器升级。
  核查位置：§3 rewrite strategies；§4.1–4.4；§7/Appendix B/H

**2610.02840 · PointWAM: 3D World Action Modeling for Dexterous Robotic Manipulation**

[论文](https://arxiv.org/abs/2610.02840)

- **foundation-model**：PointWAM统一场景/手3D轨迹预训练再动作retargeting，符合机器人基础模型候选。
  复现边界：3evalseed不是3训练seed；RoboDojo单seed。人视频CoTracker/VGGTdepth预处理成本与噪声不可省；point细节/透明物失败。项目明确Code soon，未发布代码；不宣称语言泛化（DexJoCo每任务固定指令）。
  核查位置：§3.1–3.4 Eq1–7；§4.1–4.4；App B/C；官方项目页

**2610.02835 · All Work And No Play Makes Jack a Dull Boy: Understanding and Preventing Catastrophic Strategy Collapse in RLVR**

[论文](https://arxiv.org/abs/2610.02835)

- **post-training**：MeshLearning固定离线coach策略前缀（无中间计算和答案）探索，对正确轨迹相对pre-RLVR reference的策略logprob增长做uniform-KL均衡；推理时无coach，真实数学科学代码训练。

**2610.02832 · FastOPD: On-Policy Distillation for Lightweight VLA Deployment**

[论文](https://arxiv.org/abs/2610.02832)

- **foundation-model**：FastOPD单次学生flow-map跳跃采样on-policy状态匹配teacher对角velocity，并用中点自一致传播到有限步map；LIBERO/RoboTwin及真机器人，单步action-expert训练必须真checkpoint。
  核查位置：Abstract（输入检索工件中的完整摘要已逐条审阅）；§3 Eq.3；§4.1–4.2
- **post-training**：FastOPD单次学生flow-map跳跃采样on-policy状态匹配teacher对角velocity，并用中点自一致传播到有限步map；LIBERO/RoboTwin及真机器人，单步action-expert训练必须真checkpoint。

**2610.02828 · FSPO: Policy-Consistent Risk and Pareto-Feasible Control for Budgeted LLM RL Post-Training**

[论文](https://arxiv.org/abs/2610.02828)

- **post-training**：FSPO policy-consistent risk-to-go ensemble、decision-conditioned calibration与Pareto continuation证书控制训练动作；正文区分24case ledger机制与Qwen3B真实GRPO trainer研究。接纳机制，不能把固定ledger效率当LLM能力提升。

**2610.02814 · VeriPy Source-Preserving Verification and Compatibility Checking for Python Components**

[论文](https://arxiv.org/abs/2610.02814)

- **agent**：VeriPy 保留Python executable AST，显式admission/environment将spec直接降Dafny或Lean，proof sidecar与axiom gate、hash-bound guards、原body/model differential tests及scoped compatibility。
  复现边界：支持片段/精确builtin/Unicode scalar/snapshot信任边界明确；basedpyright不是功能证明，guard可生成不代表proof。ambientFalse sidecar历史漏洞说明需精确proposition及假设审计；兼容历史关系目前Dafny，Lean覆盖不同。必须实际compiler/solver执行。
  核查位置：§3.1–3.3、§4、§7、Appendix G

**2610.02781 · OPD Before RL: Warm-Starting Rubric-Based RL with On-Policy Distillation**

[论文](https://arxiv.org/abs/2610.02781)

- **post-training**：RP-OPD先用rubric特权teacher top256 forward-KL暖启动，再切换rubric reward GRPO；三rubric领域多学生。HealthBench正文另列重叠/不重叠评价，正式复现须使用完全隔离数据。

**2610.02740 · Prospective Hindsight: Self-Calibrating Reinforcement Learning via Prediction-Reality Gaps**

[论文](https://arxiv.org/abs/2610.02740)

- **agent**：PH同policy共享参数自评只见state/action不可见privilegedfuture，ternary多数票与实际结果不一致则stopgrad(1+alpha)乘base RL/OPD/Combined loss；未知类中性。OLMo3-7B单轮verifier/多轮PRM+用户模拟、随机同质量reweight控制。校准解释非保证，alpha2可坍缩成预测失败；额外M forward训练开销必须计，不能让测试gold流入自评。
  核查位置：§3.1–3.4 Eq4–5；§4.1/4.3；AppendixC

**2610.02718 · Revisiting Visual Representation Enhancement of VLMs via Kernel Canonical Correlation Analysis**

[论文](https://arxiv.org/abs/2610.02718)

- **foundation-model**：3vKCCA将CLIP视觉、冻结DINO与文本作三视图投影训练，可作为带理论限制的视觉对齐候选。
  复现边界：零值是KKT必要非充分，实做列归一化避免全W=0但不能声称解了原KCCA/eigenproblem；必须保留归一化并监控投影rank/相关性。2×5090训练非A100验证，单表无seed方差/独立调参说明；未找到作者代码。
  核查位置：§3 Eq1–3；§4 Table1；App A/C Eq18–21

**2610.02713 · WakeKV: Reactive, Reversible KV Residency for Heads That Change Their Minds**

[论文](https://arxiv.org/abs/2610.02713)

- **foundation-model**：WakeKV保存完整CPU reservoir，GPU按头LRU驻留并在需求变化时可逆取回，适合缓存迁移实验候选。
  复现边界：大部分cache-miss对照来自完整attention轨迹oracle，不等于在线延迟；真实FlexiCache/vLLM桥接单一模型硬件，R16增益同时减少attention工作。需保持因果需求预测、计入PCIe取回和CPU全量存储，不能复制oracle命中率冒充能力。
  核查位置：§3；§4–5；§6 limitations

**2610.02710 · Self-Supervised Scaling of Terminal Environments for Scientific Domains**

[论文](https://arxiv.org/abs/2610.02710)

- **agent**：SWR将500真实workflow包装成3000任务，public IO/hidden judge隔离；typed scenario、replay反例与hidden完美一致筛SFT，重复采样只是重权重非新轨迹。SWR100是同workflow的新task不是unseen-workflow；35k开发校验与独立200case冻结后audit分开，2%误接/误拒；oracle public-output选择仅反捷径诊断，不能供agent。方法可复用，正文未给可定位作者完整释放入口。
  核查位置：Title and complete abstract

**2610.02700 · Learning from Evolving Errors: Adaptive Iterative Repair for On-Policy Distillation**

[论文](https://arxiv.org/abs/2610.02700)

- **post-training**：AIR-OPD按首个错误anchor开始，保留1-epsilon纠正概率质量的块边界repair区域；多轮指导teacher特权蒸馏和gamma深度/rho即时成功归一权重；参考答案只训练分支，实际DAPO训练。

**2610.02697 · GeoScaffold: Learning Compact Geometric Latents via Reconstruction for Efficient Vision-Language Navigation**

[论文](https://arxiv.org/abs/2610.02697)

- **foundation-model**：GeoScaffold 先训练冻结深度 VQ-VAE，再用八个几何 query 重建深度码/深度图/连通性/可通行性，联合模仿学习；部署移除重建头与 tokenizer。R2R-CE/RxR-CE 可验证。
  复现边界：Matterport 数据有访问许可；深度和 oracle 轨迹仅训练使用；混合 attention mask 与 query 保留在推理；完整论文训练约 1500 A100 小时不可当轻量验证。
  核查位置：§3.2–3.3/Eq5–9; §4.1–4.4

**2610.02695 · Test-time Calibration Learning for Large Language Model Reasoning**

[论文](https://arxiv.org/abs/2610.02695)

- **post-training**：TTCL按答案一致性构造pseudo正确性/置信目标，reasoning-answer和confidence token分离优势，逐epoch冻结EMA目标cache；同benchmark无标签适应再评测，属于transductive TTT非独立未见测试。

**2610.02687 · Decoupling Memory from Context: Structured Memory for Token-Efficient Test-Time Continual Learning**

[论文](https://arxiv.org/abs/2610.02687)

- **foundation-model**：GraphMemory agent上下文记忆优化，由agent track审查。
- **agent**：GraphMemory对ACE新增compact index entry选择与有向证据图，2hop/12nodes/2500tokens BFS，Beta(1+help,1+harm)均值排序，生成归因仅允许已载入节点，Curator显式创建/删除边。不是端到端O(1)，index随库增长；FiNER/Formula val选memory、heldout test，省token但query约1.8倍慢且部分准确率低，不能宣称全面优越。
  核查位置：Title and complete abstract

**2610.02683 · RAOA: Alternating-Operator Neural Computation with Programmable Radio Propagation**

[论文](https://arxiv.org/abs/2610.02683)

- **foundation-model**：RAOA交替归一化能量梯度problem步和Hadamard mixer步，重复共享两个控制参数；零初始化残差adapter可在冻结LLM中研究递归结构。
  复现边界：只算子与传播模拟，无真实RF速度能耗或量子优势；4B主实验depth1不是深度scaling。Qwen深度收益平、768token GSM8K配对bootstrap未区分RAOA/MLP/frozen，应保留负结果并匹配计算量。
  核查位置：§3 Eq1–4；§4 design；§6 scope；Appendix H

**2610.02670 · LEAP: Learning Efficient Action Proposals For LLM Agents**

[论文](https://arxiv.org/abs/2610.02670)

- **foundation-model**：LEAP学习agent动作proposal，由agent track审查。
- **agent**：LEAP target canonical-action LoRA NLL训练tinydraft，无targetlogits；克隆环境先proposal，再同GPU并行targetverify、只提交匹配前缀并移交克隆状态不重复工具。OpenAGI/TaskBench无工具执行，tau2/BFCL为localbackend；1.10–1.63x whole-task speedup有任务配对bootstrap。真实外部副作用不能安全clone则不适用，targetauthorship不保证并发下trajectoryidentity。
  核查位置：Title and complete abstract

**2610.02666 · CHASE-VLA: Post-Training Quantization Framework for Vision-Language-Action Models with Chunk-Aware Scale Estimation**

[论文](https://arxiv.org/abs/2610.02666)

- **foundation-model**：CHASE-VLA以先前生成action chunk预测逐层/去噪step组的激活尺度分布，分位损失与方差联合训练尺度估计器，保持W4A4 action expert。
  复现边界：输入必须是之前实际生成的chunk而非GT未来动作；首chunk使用基础校准。LIBERO每任务20episode；A100延迟只量action expert而不是整个视觉语言动作流水线，部署还需真实packed低比特验证。
  核查位置：§3.2–3.3；§4.1/4.4

**2610.02657 · Context-Tower Conversion Preserves Generation While Freezing Retains Knowledge: Low-Budget AR-to-Diffusion Conversion of MoE LLMs**

[论文](https://arxiv.org/abs/2610.02657)

- **foundation-model**：低预算AR转diffusion通过frozencontexttower和layerKVconcat有匹配token/参数协议与公开任务证据，作为研究型转换operator而非serving加速接入。
  复现边界：arms还改loss/block/corruption不能只归因freezing；trainabletowergeneration无显著差但MMLU差13pt；BS1吞吐只有servedAR .134/.168，工程2x是自身基线；+150Mtoken S16 confounded；seed2仅tower，250M中途复验失败。
  核查位置：§3；§4/Table2；§5；§6；§7/Limitations

**2610.02638 · Batched Speech Decisions Without Decoding: Single-Token Supervision Lets a Frozen LLM Hear Beyond the Transcript**

[论文](https://arxiv.org/abs/2610.02638)

- **agent**：DuplexJev冻结ASR/LLM只训connector，内容transcriptKL与决策单letterCE混合；typed选项随机位置；共享prefix KV+blockdiagonal suffix mask+restartposition精确批量logits读出。A多层fusion不胜B末层，speaker-disjoint真人语音，情绪训练ZJUcontent仍降6–17点、混loss非全解决。流式160–200ms仅部署构想未测。可纳语音决策/批量readout基础算子非完整duplexagent。
  核查位置：§2.1–2.4；§3；§4.1/4.3

**2610.02626 · Imagine the Future, Internalize the Gist: Efficient VLA Reasoning via Internalized Spatiotemporal Imagination**

[论文](https://arxiv.org/abs/2610.02626)

- **foundation-model**：IG-VLA未来latent差分推理再SceneGist蒸馏形成明确低成本动作策略候选。
  复现边界：K/λ/层数由LIBERO消融选择，接入必须独立validation；6.38x针对引用基线，A6000 169.5ms不是独立同机baseline复测。UR3仅77demos×16trial，62.5%比56.2%仅一例差，不当稳健胜出。未找到作者代码。
  核查位置：§3.1–3.2 Eq1–10；§4.1–4.4 Tables1–5；App A

**2610.02617 · WebUIProof: Benchmarking WebUI Code Generators with UI-Agent Execution Harness**

[论文](https://arxiv.org/abs/2610.02617)

- **agent**：WebUIProof以DOM+视觉UI agent执行测试，build failure计零、Full+0.5Partial聚合，判定依赖grounding/stepbudget，100例人工一致率约80%非确定oracle；VisRL组合截图/交互/analyzer reward PPO。官方公开149general任务和build/eval/compute_acc代码，但论文219含70个3D任务未见repo对应，复现先限定149，RL/3D不能默认已开源。
  核查位置：Title and complete abstract

**2610.02616 · VERSE: Verified Self-Evolving Optimizer for Agent Harnesses**

[论文](https://arxiv.org/abs/2610.02616)

- **agent**：VERSE在固定权重harnessoptimizer上增加trace minimization、draft验证双通过、replay/perturb、失败模式audit与optimizer自身prompt/tool/hook更新。110train50val108Marchtest与107JulyOOD隔离；每行一次evolution、test重复3次，不是3个独立搜索seed，compute不完全相同。静态验证器/预算及val选择要保留；不能把单次flip当修复。
  核查位置：Title and complete abstract

**2610.02614 · What Is Lost in Post-Training? Default Collapse and the Loss of In-Context Steerability Across Diverse Perspectives**

[论文](https://arxiv.org/abs/2610.02614)

- **post-training**：SDM以相关性judge筛prompt、stance judge分桶，在维度群体分布上惩罚目标偏离并PPO；Llama8B两设置初步训练，不能把群体分布约束说成逐prompt保证。

**2610.02597 · GRAFT: Growing Agglomerative Foundation Models via Continual Teacher Distillation**

[论文](https://arxiv.org/abs/2610.02597)

- **foundation-model**：GRAFT以历史student单anchor保存旧教师功能，TSRT与image-text关系KL接纳新视觉teacher，是定义清晰的持续蒸馏operator。
  复现边界：main表异构teacher/data非公平排名，warmstartDUNE成本未重付；LoRA retention移除adapter恢复base与共享student不等价；下游需新head/decoderfinetune不是零shot；未查到正文官方源码入口，复现需补完整schedule/source。
  核查位置：§3.1–3.3 Eq1–10；§4.1–4.3 Tables1–2；AppA

**2610.02593 · Fisher-Guided Submodular Data Selection for Continual Pre-Training of Large Language Models**

[论文](https://arxiv.org/abs/2610.02593)

- **foundation-model**：Fisher双几何与流式submodular数据选择是明确的CPT算法候选，不以工业上线结果接入。
  复现边界：不是用F惩罚更新；LoRA对角F、warmup/投影皆近似，1/2−ε仅surrogate。相同token预算另计候选梯度/参考F成本；医学域两backbone结果不外推通用。未找到作者代码，不能用PPL启发式代替双logdet。
  核查位置：§3；§4.1–4.4 Tables1–2；App A/B/E
- **post-training**：Fisher/submodular数据选择用于continual pretraining，转基础模型track。

**2610.02588 · Open-Endedness Bench: Measuring Epistemic Process from Agent Records**

[论文](https://arxiv.org/abs/2610.02588)

- **agent**：OEB将轨迹转act/proposition证据卡，substring核验引用、三次closed-question投票建epistemic图、确定性聚合；无机会abstain且<5机会不计。四能力轴与persona分离，不能总分混加。90人工audit、119已有runs/12tasks，相关非因果；median652judgecalls不宜伪称低价在线reward。官方MIT pipeline/converters及HF scored runs已核。
  核查位置：Title and complete abstract

**2610.02569 · Pincer: Resource Authorization for Agents using a Digital Twin**

[论文](https://arxiv.org/abs/2610.02569)

- **agent**：Pincer以OS完整资源中介与隔离twin为TCB；可信用户state+PRF逐路径段去语义accesspattern、content与precommittedpolicy三票合取。PRF保护只针对资源名优势，非全系统注入免疫；历史access不等于用户授权。合成两persona各单模型、条件ASR/BGR是资源gate非终局任务成功，implementation/data正文称即将发布，算法可候选但数据集不可声称已公开可运行。
  核查位置：Title and complete abstract

**2610.02542 · How To Train Your World Model: Fine-tuning vs RAG for LM-based World Modeling**

[论文](https://arxiv.org/abs/2610.02542)

- **agent**：LM worldmodel研究FT与RAG并提出HWM：同episode排除的历史transition检索条件NTP，query用observation/action分层检索可选；frozenpolicy统一规划流程。五模型环境20组合17胜是作者实验；oracle实际环境与top20后验gold重排只diagnostic，不能给部署策略。非constructedWM在9/20胜说明外推有限，transitionfidelity与taskutility必须分报。
  核查位置：Title and complete abstract

**2610.02525 · Learning What to Investigate Next: Meta-Reasoning for Long-Horizon Research Agents**

[论文](https://arxiv.org/abs/2610.02525)

- **agent**：MIRA固定curation/executor仅训练外层workorder/terminate研究决策；共享actorcritic以单token离散return分布KL、决策级GAE与跨版本bootstrap bridge，ratio范围外mask policygradient但保留logratio²penalty，actor/critic独立buffer及optimizer顺序更新。四研究环境、proxy/gold分开；shared初始化来自critic故消融不隔离参数共享本身，内层tool/实验token不训练。
  核查位置：Title and complete abstract

**2610.02523 · Hypothesis-guided discovery of cognitive algorithms via program refinement**

[论文](https://arxiv.org/abs/2610.02523)

- **agent**：从人写FlipPy认知程序出发，Game提出behavioral revision、Coding实现、Audit最多5修复、Inference算行为likelihood；846候选733可执行后语义cluster选24代表，不是全自主理论发现。heldout trial未参与生成/选择，72/137改善；synthetic recovery仅8.4%回收75%预测差距，限制明显。特定领域应用，但受约束程序改进与heldout likelihood选择可形成通用evolve算子；匿名OSF未提供可定位链接，不能声称材料已核实。
  核查位置：Title and complete abstract

**2610.02480 · MEA: A Reward-Driven Multi-Agent System for Faithful Model Explanations**

[论文](https://arxiv.org/abs/2610.02480)

- **agent**：MEA共享backbone Proposer工具策略/Actor解释，以遮挡再query原classifier衡量faithfulness，两段统一terminalGRPO advantage；vision mask面积λ.3与toolcountλ.05抑制gaming，text/tabular top25%约束。三模态及未训练Q8/Q9；遮挡是模型行为诊断非现实因果证明，必须保留真实classifier/XAI调用，不用LLM自评代替。
  核查位置：Title and complete abstract

**2610.02478 · Tropical Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.02478)

- **agent**：Tropic对deterministic resettable环境维护已观测状态/片段图，每轮冻结actor重评分，max-plus prefix/suffix求最佳verified可达路径，frontier补采样与topL拼接必须整路径重放验证；best+低覆盖archive路径per-tokenNLL更新，无rewardbaseline/负向项。四环境两backbone三trainingseeds、heldout实例；不能用gold路径或不具可重置性真实API冒充。
  核查位置：Title and complete abstract

**2610.02472 · APDMem: Agent-Controlled Progressive Disclosure for Query-Adaptive Long-Term Memory**

[论文](https://arxiv.org/abs/2610.02472)

- **agent**：APDMem L0摘要索引/L3原文先建，L1事实/L2turnnotes按需缓存；hybrid+RRF search与agent自主drill，reflection无新证据或20步停，draft→organizednotes→answer。LongMemEvalS500，baseline从文献取非全重跑；onlinecost只本方法有且排除共享answergenerator，不能宣称等预算优于全baseline。
  核查位置：Title and complete abstract

**2610.02462 · Capability Scaling-Down Laws for LLM Compression**

[论文](https://arxiv.org/abs/2610.02462)

- **foundation-model**：按能力分别预测剪枝、量化和蒸馏损失：共享剪枝密度形状、位宽/组大小网格插值，以及独立数据量和训练曝光的蒸馏关系，可用于evolve的预算分配。
  复现边界：系数跨模型家族不可直接迁移；Table2带†规则是在看测试后选择，必须新val冻结；测量节省≠能力提升。官方提供分析/测量镜像但不含原教师文本及adapter权重，V47freeze缺失以V70替代明确披露；不得将分析旧日志算新训练。
  核查位置：§3–4 Eq3–4；§5.1/Table1；§5.2/Table2；official README

**2610.02460 · CUEing User Simulators: Calibrated User Embeddings for Multi-Turn Benchmarking**

[论文](https://arxiv.org/abs/2610.02460)

- **agent**：CUE将userturn与前序assistant attention编码、slotcommanddecoder及latentdiffusion采样，content抑制不保证去除任务/结果信息。completed-human-trajectory条件replay是回顾校准而非未来预测；无目标轨迹的sampledpersona才新用户模拟，sessionmixture不等于人群分布。483tauUSI及heldout SimulatorArena/PRISM；官方Apache2 runtime/training和HF模型/annotation/examplepool入口可用，未执行代码。
  核查位置：Title and complete abstract

**2610.02444 · Counterexample Generation via Per-Theorem Symbolic Verifiers: When Imitation Hurts and Reinforcement Repairs**

[论文](https://arxiv.org/abs/2610.02444)

- **post-training**：SymCE公开反例任务/逐定理Python verifier/结构schema和dense/sparse reward，可作RLVR/evolve评测；作者仓库含corpus/splits、oracle/sandbox、runner及逐条结果。schema由canonical witness构造，需审查是否泄漏答案形状，隔离任意Python执行。

**2610.02425 · Finding the Move Is Not Winning the Game: XiangqiBench for Closed-Loop Evaluation of LLM Agents**

[论文](https://arxiv.org/abs/2610.02425)

- **agent**：XiangqiBench119搜索+人工验证残局（非形式证明），gold解法不入agent工具；40ply/depth18固定defender、三次连续非法失败、简化重复规则。8568轨迹12模型2设置3trial，pass@3与全部成功分报；Sighted/Restricted提示也不同。官方MIT run/score与数据卡公开，PikafishGPL另计，原NNUE被替换须冻结engine+network不可直接换新版。
  核查位置：Title and complete abstract

**2610.02404 · Trained Agentic Context Management**

[论文](https://arxiv.org/abs/2610.02404)

- **foundation-model**：自调用与上下文管理训练属于agent track。
- **agent**：训练agenticcontextmanagement：最小read_chunk/spawn工具，SFT oracle合成tree-reduce/sequential-fold/边界扩读策略，非成功RL方法（RL退化）。RULER每type5、OOLONG每family10且nativebaselinecontext不同，8kagentbudget可扩展但未正式量化成本；temperature经验选需另设validation，不能把oracle训练脚本开放给评测agent。
  核查位置：Title and complete abstract

**2610.02396 · Inherit-MAS: Test-Time Evolution of Multi-Agent Systems through Workflow and Execution Inheritance**

[论文](https://arxiv.org/abs/2610.02396)

- **agent**：InheritMAS对latest-incumbent DAG先prune再一次edit，最终单独judgelexicographic排名；继承仅exact resolvedrequest含模型/参数/上游/环境指纹且recordhash有效的只读节点，statechanging sink每次live。WorkBench/HotpotQA，部分baseline retrievalbudget非完全同，inheritedtoken只是等价历史量不是实际消耗；judge最高不保证真实utility单调。
  核查位置：Title and complete abstract

**2610.02388 · Octrees as an Explicit 3D Language**

[论文](https://arxiv.org/abs/2610.02388)

- **foundation-model**：OctLLM 以稀疏六级 octree、独立 3D 分支和 3D RoPE 共用冻结 Qwen2.5-VL，另训占据补全并接 TRELLIS 解码。Objaverse-XL/HSSD/ABO/ShapeNet 与 Toys4K/PointLLM200 可验证。
  复现边界：195k 资产排除 PointLLM200；12 分支约 2.8B 可训练参数，非微小 adapter；TRELLIS 外部解码和许可必须保留；正文称已发布但本轮未核验链接。
  核查位置：§3.1–3.4; §4.1–4.3; Appendix A/B/D/E

**2610.02361 · SEDIMA: Cross-Run Hierarchical Insight Memory for Evolutionary Search Agents**

[论文](https://arxiv.org/abs/2610.02361)

- **agent**：SEDIMA每evaluation写raw→LLMinsight→attentioncentroid cluster，mutation前cluster/insight检索与证据trace→3建议，不改evolve搜索器。AlgoTune/ALE私有评分与publicfitness分离、memory由disjoint问题建；cold也在线写记忆。100候选匹配不等token/calls，主表单run，ablation/transfer才3seeds；boundedcontext非总检索常数成本。
  核查位置：Title and complete abstract

**2610.02359 · Lexicographic Multi-Objective On-Policy Distillation**

[论文](https://arxiv.org/abs/2610.02359)

- **post-training**：LMOPD按最高优先未满足reward路由expert，再对centered log-policy correction一次顺序投影成virtual teacher；真实多expert实验，但专有训练语料、单次非正交投影不保证全部约束或reward级无退化。

**2610.02351 · DeReAct: Decomposed Reasoning and Acting for Reliable AI Agents**

[论文](https://arxiv.org/abs/2610.02351)

- **agent**：DeReAct Brain提intent/command、独立Critic按约束failclosed gate、CM只保环境支持state并判完成，Brain另见首5+recentwindow。GAIA165/SWE489 native非LLM成功评分，3attempt pass1与pass3，groundingjudge另算；CM是模型判定非形式验证，Claudecritic/CM固定且非真实外部副作用验证，不能把successflag替换真实benchmarktest。
  核查位置：Title and complete abstract

**2610.02349 · MIRROR: Multipath Quorum Integrity for LLM Multi-Agent Communication**

[论文](https://arxiv.org/abs/2610.02349)

- **agent**：MIRROR发送端一次生成canonicalbytes，5逻辑路由3payload2digest majority恢复；unkeyedhash非认证，安全完全依诚实endpoint且受控routes<半数/二次原像。AutoGen/CAMEL/MetaGPT和Gemma/Gemini评测只logicalroutes同backend、无真实独立故障域/时延测量；只抗in-transit篡改，不抗已被注入sender，须保留此条件。
  核查位置：Title and complete abstract

**2610.02344 · Drive vs. Decay: On the Training Dynamics of Joint-Embedding Predictive Architectures**

[论文](https://arxiv.org/abs/2610.02344)

- **foundation-model**：ResidualPred以残差预测器和对角注意力初始化抑制JEPA塌缩；表5五种子、同ImageNet1K30epoch预算控制支持新机制。
  复现边界：线性drive/decay理论不直接证明非线性网络；90epoch优势缩小；未跑完整官方I-JEPA规模。
  核查位置：§4；§5；§6.1–6.2/Table4/Table5；§7–8

**2610.02330 · Choosing Before Acting: Comparative Value Estimation for Long-Horizon Tool-Use Agents**

[论文](https://arxiv.org/abs/2610.02330)

- **agent**：CITA/CIM由observed同context成功率、Bayesian图synthetic无真实API、LLM模拟比较三源训练valueBCE+gapMSE+transitivity/confidence，Vc排名nexttool，confidenceweightedvalue与taskreward混合GRPO。Toolathlon/TOUCAN/TRAJECT、Qwen7B/Llama8B；value不是因果反事实真值，sandbox必须标synthetic，真实闭环评估不可由自身CIM评分替代。
  核查位置：Title and complete abstract

**2610.02324 · Slow-Fast Multi-Teacher On-Policy Distillation for Capability Preservation**

[论文](https://arxiv.org/abs/2610.02324)

- **post-training**：SF-MOPD维持EMA慢学生，以slow-fast logprob方向去除teacher冲突部分并JSD蒸馏+原MOPD正则；QwenVL2/4/8B多domain实测，需真实EMA参数而非固定reference替代。

**2610.02323 · World-Calibrated Proposal-to-Action Flow for Vision-Language-Action Models**

[论文](https://arxiv.org/abs/2610.02323)

- **foundation-model**：ProAct具有完整公开训练核心，proposal/world-calibration/anisotropic flow可进入候选，先限LIBERO可执行路径。
  复现边界：非counterfactualworldmodel，专家未来而非proposal执行未来。公开无trainedProActweights/完整RoboTwinrollout；π0.5初始化不能冒称复现权重。规范化Da已在pipeline吸收不可双乘，history只已执行并episode重置；cacheframe latency不含传输/仿真不等闭环速度。
  核查位置：§2.2–2.4 Eq2–11；§3；App A/E/F；官方README

**2610.02304 · SimuVerity: Benchmarking Agents for Engineering-Grade Simulink Model Generation**

[论文](https://arxiv.org/abs/2610.02304)

- **agent**：SimuVerity101任务10工程域，publicspec/profile与hidden场景阈值隔离；交付/执行/工程qualification三gate后六维评分，非交付/候选故障计失败、基础设施故障重跑。6agent每任务3次，10强任务消融为选择性子集非总体因果。官方Apache2仓库公开101任务/scenarios/scorers/reference或importrecipe与结果验证；运行依赖逐任务MATLAB/Simulink商业产品和第三方资产许可。
  核查位置：Title and complete abstract

**2610.02298 · EditHero: A Benchmark for Long-Horizon Part-Level 3D Editing and Vibe Modeling**

[论文](https://arxiv.org/abs/2610.02298)

- **foundation-model**：EditHero由part library与操作日志重建457链2755turn的精确3D目标，self-rollout分开编辑区/保持区与no-op/regeneration对照，可补多轮生成评价。
  复现边界：被测方法可见当轮目标render但不可见操作日志/GT3D；VoxHammer另给gold mask，属不同信息条件。只完成turn平均会受失败删失影响，须分报完成率；conditioning/heldout views分开，资产许可证逐源核。
  核查位置：§3 construction；§4 protocol；§5.1；Appendix9/12/18
- **agent**：EditHero457链2755编辑252hosts，exact日志隔离；自rollout、1conditioning+3heldout视图，IF/CC分别编辑/未编辑区域。Agent仅55链416turn可见编辑选择子集，均值按已完成turn故须同时报coverage。已读方法/实验，但官方README中benchmark engine/eval code及HF edit-chain发布仍未勾选，无法接公共执行入口，暂缓不是未读。
  核查位置：Title and complete abstract

**2610.02206 · KaliBench: A Fine-Grained Benchmark for Cybersecurity Tool Use on Kali Linux with Runtime-Free Verifiable Rewards**

[论文](https://arxiv.org/abs/2610.02206)

- **post-training**：KaliBench公开8504 query-command/1642工具数据与runtime-free shlex评分，三个信息条件、alias-aware参数匹配可作工具使用评测。仅离线命令字符串评分，不等同实际环境执行成功；不得自动对真实目标执行命令。
- **agent**：KaliBench公开8504 query-command/1642工具数据与runtime-free shlex评分，三个信息条件、alias-aware参数匹配可作工具使用评测。仅离线命令字符串评分，不等同实际环境执行成功；不得自动对真实目标执行命令。
  核查位置：§3 Evaluation Protocol；§4；Appendix L；作者仓库README/文件列表已只读核查

**2610.02204 · Reconstruct, Practice, Go Real: Guided Self-Improvement for Embodied Agents**

[论文](https://arxiv.org/abs/2610.02204)

- **agent**：RPG从ABC视频重建MuJoCo任务并人工检查冻结evaluator；Runtime只部署观测，privileged独立episode供failureanalysis，Implementor修改skill/prompt，paired5seeds跨22任务gate平均增且单任务不降超.2，merge后重测。15轮单run/候选compute不匹配；savedround heldoutseed回顾评测非未见task，3实机各10trial统一标定冻结，不把privileged轨迹当部署policy。
  核查位置：Title and complete abstract

**2610.02202 · ScholarCatalyst: A Benchmark for Retrieving Papers That Inspire New Research**

[论文](https://arxiv.org/abs/2610.02202)

- **agent**：ScholarCatalyst207真实项目894查询（207Core/687Sub）作者验证inspiration与hard negatives，删solution泄漏并按源论文完成时间截断corpus。Recall标签不完备；oracle候选重排只诊断不供agent。公开191k文档、evaluation及受限本地corpus agentic-search脚本，CCBYNC4，适合检索/科研评测入口而非新训练loss。
  核查位置：Title and complete abstract

**2610.02196 · InterEvolve: Test-Time Evolution of Reward Programs for Humanoid Loco-Manipulation**

[论文](https://arxiv.org/abs/2610.02196)

- **foundation-model**：InterEvolve 在冻结 forward-backward 运动先验上进化分阶段奖励程序，内层 CMA-ES 调参数、外层 LLM 调结构，固定场景验证并复用已核验技能。OMOMO/GRAB 与模拟八类任务可验证。
  复现边界：必须保持 verifier/进化场景与最终测试隔离；奖励可使用特权模拟状态但不能将测试正确计划交给策略；真实 G1 硬件演示不等于本地可验证。
  核查位置：§3.1–3.4; §4.1–4.4; Appendix B/D/E

**2610.02191 · The Missing Primitive: Diagnosing and Repairing Mathematical Reasoning in Large Language Models**

[论文](https://arxiv.org/abs/2610.02191)

- **post-training**：Absorb以数学primitive为训练teacher特权，用reverse-KL单侧clamp限制压低学生偏好的强度，保留正向teacher指导；Prim/HLE/HMMT/Omni实测。gold primitive不得进入被评价student。

**2610.02190 · Trust the Direction, Search the Step: Zero-and-First-Order Methods for LLM Fine-Tuning**

[论文](https://arxiv.org/abs/2610.02190)

- **post-training**：ZFO沿基础一阶optimizer方向，用同batch正负两次前向估二三阶导，Taylor/Padé区间择步并奇点fallback；真实LLM微调与开销实验，须匹配额外前向预算。

**2610.02161 · DuoMind: Enabling Distributed Multi-Robot Coordination with Semantic Communication**

[论文](https://arxiv.org/abs/2610.02161)

- **agent**：DuoMind每机器人VLM高层orchestrator、VLA动作，四字段意图/子目标/信念/可选不确定性通信，无联合特殊训练；7RoboPoly+8RoboTwin双臂改分布、每任务50双机器人demo转100单体训练。共享global相机+本地wrist，模拟两机器人非实机大群体；通信与π0替换消融支持模块可复用，不能宣称更大规模部署。
  核查位置：Title and complete abstract

**2610.02150 · From Knowledge Access to Source Learning: Developing Source-Specific Competence**

[论文](https://arxiv.org/abs/2610.02150)

- **agent**：SourceLearn持久source-grounded实体表示，Inspect/Deepen/Connect自学+consolidate；taskguided只用训练guidance答案诊断缺证据并重读source，更新representation/prompt不是模型权重。五任务、3次30/70guidance/test分割与AppWorld官方split；测试答案不得进入memory，QA judge与原生执行指标分开。
  核查位置：Title and complete abstract

**2610.02140 · Finetuning with Sampling: SFT Learns Better Than You Think**

[论文](https://arxiv.org/abs/2610.02140)

- **post-training**：Projection Sampling用expert条件proposal与Metropolis-Hastings分块采样使信息保留轨迹靠近base，再SFT；化学/数学/开放域真实训练。不得将有限MCMC近似等同理想投影精确采样。

**2610.02091 · GeoLatent: Geometry-Guided Latent Structuring with Routed Optimization for 3D Reasoning**

[论文](https://arxiv.org/abs/2610.02091)

- **foundation-model**：GeoLatent 分离共享几何成分与残差，用三阶段路由优化阻断答案的视觉捷径；DA3/VGGT 训练目标只辅助潜变量。SPAR/SpatialLadder、SPBench/ViewSpatial 可真实验证。
  复现边界：几何教师仅训练使用；37 个同 ScanNet 场景需去重报告；必须做路由干预检验，不能只加几何标签并称阻断捷径。
  核查位置：§3.2–3.4; §4.1–4.4; Appendix B

**2610.02019 · Controllable Multi-label Video Safety Detection via Adaptive Tversky Policy Optimization**

[论文](https://arxiv.org/abs/2610.02019)

- **foundation-model**：ATPO针对视频安全的自适应Tversky RL奖励，由post-training track审查。
- **post-training**：ATPO以FN/FP EMA log-ratio误差反馈调Tversky alpha/beta，固定和为2，可全局/类别控制多标签reward；真实VideoVLM训练，新增自适应reward控制器而非重命名标准GRPO。

**2610.02005 · Counting Moves, Weighing Voices: Bayesian Dialectical Argumentation for Calibrated Multi-LLM Councils under Persistent Adversaries**

[论文](https://arxiv.org/abs/2610.02005)

- **agent**：BDA把Propose/Challenge/Concede转签名endorsement counts，积分Beta可靠性的DawidSkene式汇聚，约25标签校准同预算比较；K>2伪似然需tempering，校准理论仅二类无challenge等条件。标签身份稳定学习在位置MCQ失效，sleeper攻击/可靠性突变不保证；是新聚合机制非无条件鲁棒获胜。
  核查位置：Title and complete abstract

**2610.01962 · SIEVE: Selective attention-value Suppression for Vision-Language Models Unlearning**

[论文](https://arxiv.org/abs/2610.01962)

- **foundation-model**：SIEVE 交替优化 forget 的负 CE+attention value 归零和 retain 的正 CE+冻结参考 value 匹配，定义目标明确。合成 Profile Visual-QA/Textual-QA 可做选择性遗忘。
  复现边界：不直接约束 attention 权重；不能声称满足真实隐私/GDPR 删除；须分别测文本与视觉访问、保留集损害及重新学习。
  核查位置：§3.2.1–3.2.3/Eq4–8/Algorithm1; §4.1/4.4; Appendix C

**2610.01955 · Do Your Own Research: Learning to Forecast by Learning to Search**

[论文](https://arxiv.org/abs/2610.01955)

- **post-training**：prime-forecast公开工具环境/历史问题/rollout记录，point-in-time过滤、封锁市场价格、Brier和弃答插补可独立评估研究预测；训练/测试按解决日期隔离。实时检索和API过滤非静态可复现，过滤的完美小样本结果不是无泄漏证明。
- **agent**：prime-forecast公开工具环境/历史问题/rollout记录，point-in-time过滤、封锁市场价格、Brier和弃答插补可独立评估研究预测；训练/测试按解决日期隔离。实时检索和API过滤非静态可复现，过滤的完美小样本结果不是无泄漏证明。
  核查位置：§2–4；Appendix C；作者仓库README/文件列表已只读核查

**2610.01921 · Cross-Lingual Alignment for Decoder-Only Models using MoE Routers**

[论文](https://arxiv.org/abs/2610.01921)

- **foundation-model**：XLR以平行语料的sequence-mean sparse router概率KL进行中层跨语言对齐，核心CPT辅助loss+packing优化明确，官方训练/评测公开，符合基础模型训练候选。
  复现边界：中层两个小模型按图主观选择，长预训练/更多语言未证；routeronly非可靠fulltraining替代。稀疏KL需核epsilon/zero处理，不能改全softmax而不披露。官方明示清理私有路径后未测试、非开箱即用；公开代码存在≠复现通过，需计英语extra compute。
  核查位置：§3 Eq1；§4.1–4.4；§5/Table1–2；App C/F；official README/contrastive_training README

**2610.01917 · MoLE: Mixture of Latent Experts for Complementary Visual Reasoning**

[论文](https://arxiv.org/abs/2610.01917)

- **foundation-model**：MoLE的路由视觉证据、专家value变换与隔离潜在专家/summary拓扑构成可辨识新视觉推理结构，公开数据+详细附录足够作为保真实现候选。
  复现边界：潜在token不是FFNexpert；ESVA只路由edge改V不能全局替换；gold只answer训练label不能影响inference routing。相同8latents不等FLOPs且额外参数；K2等按benchmark消融最优需另val冻结；专有基线来自外部且部分CVBench分项推算。未找到作者源码链接。
  核查位置：§3.2 Eq4–13；§4 Table1；App A.1–A.4/A.7

**2610.01892 · Selection-Based Structured Reasoning: Toward Efficient Multimodal Search Agents**

[论文](https://arxiv.org/abs/2610.01892)

- **post-training**：SSR全文不是普通工具应用：六共享推理模板以batched teacher-forced mean-logprob softmax选择，再插入全文生成action；SFT selector NLL+action NLL，GRPO一个categorical selector ratio+action token ratios，插入模板不逐token训练。AppendixB实际detach rollout竞争分数仅首步概率精确、后续近似。Qwen3VL2B/4B七multimodal搜索任务，效率须计候选prefill；保留原post摘要漏判并由正文纠正。
- **agent**：SSR全文不是普通工具应用：六共享推理模板以batched teacher-forced mean-logprob softmax选择，再插入全文生成action；SFT selector NLL+action NLL，GRPO一个categorical selector ratio+action token ratios，插入模板不逐token训练。AppendixB实际detach rollout竞争分数仅首步概率精确、后续近似。Qwen3VL2B/4B七multimodal搜索任务，效率须计候选prefill；保留原post摘要漏判并由正文纠正。
  核查位置：Title and complete abstract

**2610.01815 · Debias Anything: Fairness with Diversity without Supervision in Diffusion Models**

[论文](https://arxiv.org/abs/2610.01815)

- **foundation-model**：Debias Anything 在冻结扩散模型上训练语义 adapter，以属性方向、目标比例引导和 disagreement 多样性项进行批级去偏。公开人脸/扩散检查点可检验质量公平性权衡。
  复现边界：训练的是 adapter，不能宣传整个流程 training-free；批级比例公平不证明个体公平；公开代码链接尚未核验。
  核查位置：§4.1–4.3; §5.1–5.2; Appendix C/D
- **post-training**：图像diffusion公平与多样性guidance，不是语言模型RL/OPD。

**2610.01769 · CONTRA: Discovering and Qualifying Behavior-Changing Questions for Selective Clarification in LLM Code Generation**

[论文](https://arxiv.org/abs/2610.01769)

- **agent**：CONTRA先多轮发现问题，再要求相关且原需求未解决；每种可能答案采3程序、>=7共同输入，组内2/3稳定且至少一输入跨组不同才保留，失败非等价证明；history自适应选问或stop。419欠指定+80完整任务最多5问，GPT4o三票gold匹配；四模型macro F1 41.20vs27.32，程序隔离执行。通用执行证据澄清算子，plugin部署非线上A/B。
  核查位置：Title and complete abstract

**2610.01741 · ATI-VLA: Action-Centric Predictive Vision-Language-Action Models via Actionable Alignment Then Adaptive Injection**

[论文](https://arxiv.org/abs/2610.01741)

- **foundation-model**：ATI-VLA共享动作/观察量化空间与分层侧路注入符合VLA新算法候选。
  复现边界：推理不需未来帧/真实动作，不可用其填sidepath；量化gradient/codebook超参需作者实现补齐。8H100训练/5090部署，checkpoint按benchmarkvalidation挑选需重划独立seed/scene测试。多基线引用与reproduced须区分，项目页存在但未核到公开源码。
  核查位置：§2.2 Eq5–15/Alg1；§3；App A/B/E

**2610.01710 · CoEvolve: Construct-to-Edit Visual Grounding with Bidirectional State Refinement**

[论文](https://arxiv.org/abs/2610.01710)

- **foundation-model**：CoEvolve 以 RER-GRPO 训练有序多步 bbox 进展，再用 BDR 坐标去噪保留推理文本。RefCOCOg 训练和 RefCOCO/+ 持出评测可验证。
  复现边界：受控损坏恢复 58.8→86.19 不等于自然错误恢复；DIOR 是域内再训练而非零样本；GT 坐标仅奖励/训练目标。
  核查位置：§3.2–3.3; §4.1–4.5; Appendix B/E

**2610.01687 · Architectural Sampling: Test-Time Scaling via Computational Diversity in Frozen Vision-Language Models**

[论文](https://arxiv.org/abs/2610.01687)

- **foundation-model**：Architectural Sampling 重复冻结 VLM 的层窗口，组合递归次数得到结构 rollout，再以无标签自奖励 TTRV-GRPO 训练。公开多模型/十二基准可验证。
  复现边界：Pass@k oracle 覆盖率不等于可用 Pass@1；有效选择器和 TTRV 单独测；层重复增加计算，需等 FLOP/token 预算；不能用于仅 API 黑盒。
  核查位置：§3.1–3.3; §4.1–4.2; §5/Table5; Appendix E

**2610.01670 · Do MLLM Judges Judge the Edit? Auditing Bias in Image Editing Evaluation with Verified Quality Preservation**

[论文](https://arxiv.org/abs/2610.01670)

- **foundation-model**：EditJudgeBias以13个保质cue与sham/真实损伤阳性对照审计VLM judge，方法可复用；发布明确排除benchmark图、人评及judge/validator响应，不能重建原1196triplet实证。
  复现边界：五数据名实为三个独立content pools，需cluster配对；保质由SSIM/校准VLM/少量人评共同验证，不能直接假定每个像素改动不影响质量。仅初步减偏pilot，不宣称成熟修复算法。
  核查位置：§3.1–3.4；§4 metrics；reproducibility statement；Appendix A
- **post-training**：EditJudgeBias独立judge偏差审计：quality-preserving cues、sham/retest噪声基线、顺序互换、paired统计。官方仓库有cue/judge/metric CLI，可评新judge，但不含全部图像/人工注释/作者I2EBench输出，不能宣称精确复现原数值。

**2610.01649 · CrossGMN: Graph Metanetworks for Cross-Architecture Weight-Space Transformations**

[论文](https://arxiv.org/abs/2610.01649)

- **foundation-model**：CrossGMN可作为小模型架构压缩/evolve元算子研究候选，不能宣称已支持LLM压缩。
  复现边界：最高约200k参数；须访问teacher参数且输入输出兼容。理论plainGMN与实验ScaleGMN区别；teacher群训练摊销成本不能忽略，MLP仅1.04x且5%失败，非普遍加速。未找到公开源码；anchor选择需validation而非test最优。
  核查位置：§3 Eq1–3；§4 Eq4–5/Theorem1；§5.1–5.4；Limitations；App D.1–D.7

**2610.01640 · Not All Error Yields to Scale: Where Scaling Stops in Vision-Language Inference**

[论文](https://arxiv.org/abs/2610.01640)

- **foundation-model**：Separable Inference Scaling Law按backbone参数和真实视觉token数分别拟合误差floor+幂律，结合成本面选择heldout配置；可作为多模态预算规划诊断。
  复现边界：26预训练模型650cells，N不含encoder/projector且家族其组件也变，不能将系数解作纯backbone因果效应。成本只prompt backbone FLOPs不含视觉前端/解码，非端到端延迟；HRBench4K/8K相同题应配对resample。需新验证网格后独立test，不在全benchmark拟合又报告选择收益。
  核查位置：§2.2–2.3；§5.1–5.3；Appendix evaluation grid

**2610.01637 · Fusing Visual and Textual Representations via Multi-layer Fusing Transformers for Vietnamese Visual Question Answering**

[论文](https://arxiv.org/abs/2610.01637)

- **foundation-model**：MFT 将 PhoBERT/ViT 多层双向跨模态 attention 融合用于越南语 VQA 分类。公开 ViVQA 可训练并测 EM/token F1，作为窄域多模态算法候选。
  复现边界：不是生成式 LLM；随机 80/20 无独立 validation 的正文协议需改成明确 train/validation/test；不能直接用他人已发表数值宣称公平重跑。
  核查位置：§3.1–3.4; §4.1–4.5

**2610.01625 · Beyond Domain-Level Adaptation: Margin-Oriented Semantic-Appearance Interaction Correction for Personalized Federated Vision-Language Models**

[论文](https://arxiv.org/abs/2610.01625)

- **foundation-model**：MOSAIC 在冻结 CLIP 上联合共享/私有 prompt、域类交互残差与低秩类别修正及样本门控。Office31/Home/DomainNet 的公开联邦域分类可验证。
  复现边界：正文报告每轮最大测试准确率且无独立验证，接入必须换为 validation 选轮并说明协议差异；真类残差减法只诊断，推理须对所有候选类计算。
  核查位置：Method/Eq10–13; Experiments; Appendix B/F

**2610.01605 · Hob-VL: A Benchmark for Visually Grounded Boolean Reasoning**

[论文](https://arxiv.org/abs/2610.01605)

- **foundation-model**：Hob-VL提供符号/NL视觉布尔组合及DeMorgan一致性公开评测，可执行新provider推理并离线严格评分。
  复现边界：共享场景、等价改写不能当独立样本；不把dummy/offline-placeholder当真实模型；模型仅图+谓词/问题无truthassignment；gen脚本未公开，但固定评测材料与运行入口已公开。
  核查位置：§4构建；§5.1；官方README evals.verify_release/results

**2610.01595 · Before It Fades: Reinforcing Temporal Representations at Inference Time in VideoLLMs**

[论文](https://arxiv.org/abs/2610.01595)

- **foundation-model**：TAI 比较视频正序/逆序的逐层激活差异，取输入特定峰值向量按衰减注入后层；冻结三 VideoLLM、四公开时间推理基准可验证。
  复现边界：双路正逆序推理不是零成本；保留非时间任务对照与完整额外 FLOP；禁止以正确答案挑层。
  核查位置：§3.1–3.2; §4; §5; Appendix evaluation protocol

**2610.01569 · Managing Context and Communication in Distributed Agentic UAV Swarms**

[论文](https://arxiv.org/abs/2610.01569)

- **foundation-model**：分布式无人机agent上下文及通信管理，agent track范围。
- **agent**：分布式UAV新增peer-tag残差embedding+recency novelty最小距离gossip，管理员离线双阈值决定discard/compact/full，接收queue只是邻居已知的估计；三内存tokenFIFO、ID/path/TTL去重。10机SITL搜救，80211n解析模型非实机网络；proposal全完成而flood70–85%，后续耗时/误差仅成功run条件统计，不可只看省6–7MB到<0.5MB。通信/记忆策略可泛化候选。
  核查位置：Title and complete abstract

**2610.01564 · Chaining Skills to Hijack LLM Agents**

[论文](https://arxiv.org/abs/2610.01564)

- **agent**：APEX跨skill中间artifact将工作进度错误提升为授权，独立sandbox执行反馈优化chain；防御taint+原请求核验。690attempt四定向families512成功，family任务重叠，utility按checks权重不是整任务成功；workloop token增不自动构成越权。官方MIT执行/trace判据/参考controlled variants公开，SkillsBench另取；只纳防御沙箱评测，不执行外部攻击。
  核查位置：Title and complete abstract

**2610.01560 · AURAL: Adaptive Latent Reasoning with Joint Chunk for Speech Language Models**

[论文](https://arxiv.org/abs/2610.01560)

- **post-training**：AURAL用对角+低秩协方差GMM联合latent chunks、CSA、可微两遍scheduled sampling，再按latent坐标归一ratio做GRPO；真实语音/文本基准和延迟，应保持整个latent模型。

**2610.01537 · FedFit: Federated Fine-Tuning of LLMs via Vector-Bank Parameterization and Quantization**

[论文](https://arxiv.org/abs/2610.01537)

- **foundation-model**：FedFit的双disjoint向量库、交替联邦聚合与低比特通信具有可复现研究价值；保留公式歧义核对门槛。
  复现边界：RSC是在bank空间的近似，不是原层空间最优；加入双残差产生cross项，不能称完全恢复SoP。Eq29写Q(e)但邻接文字/30要求Q(y+e)，实施前须明确记录勘误并测守恒。90/10eval被用于停止，无独立test表述；需新增隔离validation/test。多数单seed；通信字节不等真实无线延迟，未找到作者代码。
  核查位置：§III Eq3–8；§IV Eq10–22/Alg1；§V Eq23–31；§VII TablesI–XIII

**2610.01513 · Decision Titan: Test-Time Training for Long-Term Memory in Offline Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.01513)

- **foundation-model**：Decision Titan 将 RTG/state/action DT 与 Titans fast-weight 神经记忆联合，按轨迹 chunk 更新记忆。X-Maze 重复记忆任务可验证长度外推。
  复现边界：每个 episode 必须重置记忆、保留 chunk 顺序与 no-grad 跨 chunk；符号 X-Maze 不是物理导航能力；1.7 倍训练速度与 20 倍上下文有编码假设。
  核查位置：§3.1–3.2; §4.1–4.4; §5
- **post-training**：Decision Titan在X-Maze用TTT增强Decision Transformer记忆，非语言模型后训练。

**2610.01508 · OverAct: Measuring and Mitigating Proactive Over-Authorization in LLM Tool-Calling Agents**

[论文](https://arxiv.org/abs/2610.01508)

- **agent**：OverAct以保守literal-minimal工具集定义越界（非普适授权法则），8域48tools/240双标原题扩720paraphrase，set操作无LLMjudge。SelfAudit先request-grounded justification再preexecution filter不需oracle，filter承担多数收益，justificationalone反恶化；TCR .94→.89。可纳入权限过滤机制候选，本文称附材有logs但未定位公开下载，不把720题宣称已接入可执行benchmark。
  核查位置：Title and complete abstract

**2610.01506 · MCRI: A Four-Dimensional Framework for Analyzing and Evaluating Agent Skills**

[论文](https://arxiv.org/abs/2610.01506)

- **agent**：MCRI可执行文本rubric四维Metadata/Constraints/Resources/Instructions先各1–5再task-conditioned aggregate，重复mean score×mean confidence选skill。3公共bench50subtasks/345Mind2Websteps，58275calls；相关/popularity不等于因果或通用质量。AppendixD完整评分器足以作为候选预筛机制，但F明确/Resources未包含且无公开repo，不能声称复现实验或公开全数据。
  核查位置：Title and complete abstract

**2610.01499 · VTR-Bench: A Systematic Benchmark for Evaluating Visual Text Rendering in Video Generation**

[论文](https://arxiv.org/abs/2610.01499)

- **foundation-model**：VTR-Bench公开300prompt、CoQ及carrier转录WER评测入口，支持新视频模型产物；核心keyframe agentic策略亦可研究但不能用未匹配预算增益作效率结论。
  复现边界：HF已生成视频private需申请，但公开prompt/checklist+执行代码足够生成新评测；缺失ID被排除必须固定全300coverage。参考人评100video偏可读三模型，不能外推全失败分布；clearest occurrence WER不单独测全时段一致性。Agentic预算显著增加，需等budget。
  核查位置：§3.1–3.4；§4.1–4.5；AppC.2；官方README Evaluation/Agentic Generation

**2610.01496 · SALD: Self-Referenced Advantage Learning for Diffusion Models**

[论文](https://arxiv.org/abs/2610.01496)

- **foundation-model**：SALD 同模型 easy-noise 无梯度教师与 hard-noise 学生比较，保留 batch-normalized 可微优势权重、样本 EMA 噪声课程和频域差异门控。公开扩散数据/检查点可真实训练。
  复现边界：优势权重和空间权重不能随意 detach；最终仍是加权 hard 残差损失，非直接 easy-hard 蒸馏；频域门控不是逐像素因果解释；两次前向成本需等预算。
  核查位置：§2.1–2.5/Eq6–17; §3; Appendix D/E

**2610.01492 · Q-SPT: Learnable Query-Based Compression for Low-Frame-Rate Speech Tokenization**

[论文](https://arxiv.org/abs/2610.01492)

- **foundation-model**：Q-SPT 用滑窗 query 交叉注意力降采样 SenseVoice/DAC 特征，语义 FSQ+条件声学 RVQ，联合频谱/对抗/文本重建等训练。LibriSpeech 重建、ASR/TTS 支持公开验证。
  复现边界：文本重建头仅训练存在；不同码率/stride 的修改 baseline 必须明确；不能仅用量化 toy 证明 ASR/TTS 性能。
  核查位置：§2.1–2.2/Eq1–5; §3.1–3.3

**2610.01316 · What Wins a Vote? Formatting, Length, and Lexical Diversity in the French Compar:IA LLM Arena**

[论文](https://arxiv.org/abs/2610.01316)

- **recommendation**：ComparIA 的偏好风格效应转后训练方向审查。
- **post-training**：公开偏好评估分析入口：投票时截断对话、风格/长度/词汇联合Bradley–Terry与model内对照；官方代码及derived data可读，原French ComparIA数据有gate。137293 decisive votes/116 models，complete-case127092；调整rank不是已证实更接近能力，不能因观察关联推断风格因果效应。

**2610.01286 · Dyna3: VLM-Guided Training-Free 4D Reconstruction via Depth Foundation Models**

[论文](https://arxiv.org/abs/2610.01286)

- **foundation-model**：Dyna3 用 DA3 特征跨帧最佳匹配相似度判运动，Qwen2-VL/SAM3 语义 mask 协同分离静态聚合和逐帧动态点云。DAVIS/TUM/Sintel/DyCheck 可验证。
  复现边界：不能将真实 DA3/SAM3 替换为 GT mask；所有 VLM/分割/重建开销须计入；公开检查点兼容性仍需实际验证。
  核查位置：§3.2–3.6/Eq2; §4.1–4.6; Appendix A

**2610.01278 · SCOPE-AD: Sequential cost-aware ordinal-belief planning with energy-based models for diagnostic agents**

[论文](https://arxiv.org/abs/2610.01278)

- **post-training**：SCOPE-AD以观测ordinal belief、离线soft Bellman EBM规划teacher，再masked KL蒸馏到Qwen；ADNI患者级1552/333/333，真实未取得值隐藏。限医学离线规划非通用OPD或临床部署。
- **agent**：SCOPE-AD以观测ordinal belief、离线soft Bellman EBM规划teacher，再masked KL蒸馏到Qwen；ADNI患者级1552/333/333，真实未取得值隐藏。限医学离线规划非通用OPD或临床部署。
  复现边界：复用正文审查而非本代理重读；公共artifact可执行性未在本条再次核验；接受是研究候选，不是实现完成。
  核查位置：§2.2–2.4 Eq.3–4；§3

**2610.01243 · When the Judge Acts: Auditing VLM-Guided Image Selection on Culturally Situated Prompts**

[论文](https://arxiv.org/abs/2610.01243)

- **foundation-model**：JudgeActs固定CulturalFrames候选池，三次cyclic顺序检查与预设abstention gate，对照精确随机期望及事后人评oracle；可作VLM选择可靠性审计。
  复现边界：人评/作者/国家元数据不入judge；300主集按prompt hash独立于30dev，bootstrap按prompt不按调用。3旋转非全排列，跨模型视觉预算/schema不同；abstention必须同时报覆盖，源码公开不表示底层图像有再分发许可。
  核查位置：§3 measures；§4.1–4.5；§7

**2610.01238 · Mixture-Trained Merging for Unified Multi-Objective Models**

[论文](https://arxiv.org/abs/2610.01238)

- **post-training**：MTM训练mixture-biased soft experts，以merge-simplex多目标BO选分支混合并迭代复用merged起点；真实Qwen4B/OLMo7B多域与think模式，必须validation选择并计入搜索训练。

**2610.01192 · FlashBack: Knowing When to Remember in Streaming Vision-Language Models**

[论文](https://arxiv.org/abs/2610.01192)

- **foundation-model**：FlashBack 分隔原生流式状态和临时 Recall 分支，以时间证据路由选择历史检索/SideKV，Recall 推理不写回原生历史。公开视频基准可测因果长期记忆。
  复现边界：原作者代码称后续公布；记忆库只能含观测前缀，禁止全视频离线检索；需计入临时检索/推理成本。
  核查位置：§3.2–3.4; §4.1–4.4; §6

**2610.01172 · Learning Rate Transfer for Hybrid Transformer-SSM Architectures**

[论文](https://arxiv.org/abs/2610.01172)

- **foundation-model**：混合Transformer-SSM的naive μP+AdamW跨width学习率迁移给出可执行参数化/选参配方，可作研究配置operator而非新理论保证。
  复现边界：离散LR网格0gap非连续最佳；WT2训练多epochtrainloss最优1.0与val0.1不同必须本地val；24.9Btoken仅单LR单seed，不是大规模完整sweep；Mamba simplifiedZOH固定state16不等理论trueZOHgrowstate；coordinate-check失败不推出普适充分条件。
  核查位置：§3.1–3.4；§4.1–4.3；§5.1–5.4；Limitations/AppA.3

**2610.01128 · Grounding Large Language Models in DSGE Simulators for Policy Generation and Forecasting**

[论文](https://arxiv.org/abs/2610.01128)

- **post-training**：公开DSGE语言Agent环境：Snowdrop结构模拟器的状态深克隆、action校验、rolling forecast只提交首步、不可重写历史；matched PPO/GRPO共享起点/冲击。作者repo已可读，可作领域仿真任务；不是现实政策建议/实盘因果证据。

**2610.01127 · Counting and Min-Cost Encoding for Tokenization in Large Language Models**

[论文](https://arxiv.org/abs/2610.01127)

- **foundation-model**：CNF–MCE以直接substring统计/实际使用过滤建词表，再用带边界成本的全局DP分词，属清晰基础模型tokenizer算法候选。
  复现边界：8B mix250k对qwen152k词表/embedding量不同，不是同总参数比较；compression数字不自动等latency，MCE tokenizer本身成本须计。训练预算与字符曝光须重新严格匹配，已有LM直接替换segmentation分布不保证能力。未找到作者公开代码/词表链接；保留完整Unicode单位与DP成本而非仅最长匹配。
  核查位置：§3.1 Algorithms1/2；§3.2 Eq1–4；§4.1–4.6 Tables5–8；App B.1

**2610.01076 · GLoC-EHR: Evidence-Cited Clinical Reasoning over Global Context and Local EHR Events**

[论文](https://arxiv.org/abs/2610.01076)

- **post-training**：GLoC-EHR新增global/local EHR memory接口与分阶段alignment、evidence-only sufficiency辅助loss；128350患者7:1:2隔离及外院验证。RL本身标准GRPO，接纳架构/grounded训练机制，gold只teacher/scorer可见。

**2610.01054 · Capturing In-Context Learning Dynamics with Task Operators**

[论文](https://arxiv.org/abs/2610.01054)

- **foundation-model**：Task Operator从ICL前向提取逐head/位置的乘性softmax质量与加性context value，用于无demo replay；解析定义、公开实现、明确answer-excluded验证和测试分离满足候选条件。
  复现边界：generation不是GT答案，必须剥除test标签并保持GPQA non-Diamond demos/val；验证只收未hitbudgetcompletion应报告过滤数。任务template映射不能用同一最后token偏置替代，多shot易不稳；额外提取/逐site验证成本计入，非训练free等于无成本。
  核查位置：§3 Eq1–7；§4.1/Table1；App B/C/E；official README

**2610.01037 · SLIM: Simplex-Lattice Interpolation Merging**

[论文](https://arxiv.org/abs/2610.01037)

- **foundation-model**：SLIM用专家顶点与两两中点最小simplex二次格点设计拟合合并性能，再约束优化预测AVG；与同36次预算随机设计比较且另有heldout OOD。
  复现边界：ID不是独立test；Gemma SLIM OOD50.30低于bestlattice51.85，Llama47.27更高；120eval cubic OOD反降。二次非concave无globalopt保证，36只是辨识模型下界非找好merge普适下界。
  核查位置：§3.1–3.4 Eq1–8；§4.1/Table1；§5/Tables2–3；§6

**2610.01023 · Groundability, Not Scale Alone: When Weak Reviewers Can Audit Strong Coding Agents**

[论文](https://arxiv.org/abs/2610.01023)

- **agent**：reviewability框架区分agent testimony/结构化/独立grounded证据；冻结cascade先空patch/新增staticerror再generatedtest（须base行为失败）再8Breview+abstain。official hidden test仅upperbound不能部署；32Django设计后121/122 GPT+59Gemini一次test，risk .33/.26、overreject .66/.67，generatedpass非证明。可纳独立核验/弃权策略候选，不能宣称可靠弱审强或总成本优势。
  核查位置：§3；§4；§6 Algorithm1/6.2；§7

**2610.01017 · Pay for the Fault, Not the Flow: Label-Free In-Flow Multi-Agent Workflow Optimization**

[论文](https://arxiv.org/abs/2610.01017)

- **agent**：InFlowOp cost=-log rubricsmatch造workflow，topdown拆/bottomup合并，运行中declaredinput/output contract判decomposition/assignment错，先换agent再局部重拆，invalidates descendants重跑之外缓存。无gold但semanticmatch非oracle；rollback不劣仅在检查可信/副作用可还原条件下。Braid8域，3闭源仅5域，singleLLM没工具无法读文件基线弱；同turnbudget单agent比较更有意义，profile成功筛选避免test跨样本泄漏。
  核查位置：§3.1–3.2 Eq3–8；§4；§5.1–5.3；AppendixD/E

**2610.00983 · The Devil Is in the Reconstruction Loss Scale: Rethinking Optimization in LLM Quantization**

[论文](https://arxiv.org/abs/2610.00983)

- **foundation-model**：将PTQ重构MSE改为分组RMSE，使非零误差的输出梯度范数不依赖损失尺度；sample/channel/token/element是同一家族，可接现有PTQ训练对照。
  复现边界：模型家族的token/channel默认按整体实验表现选，需独立val；零误差处需数值安全处理并验证梯度；同训练超参、calibration和精度预算，不把fakequant数值改善当真实推理加速。
  核查位置：§3 Eq6–8；§4.1–4.3；Appendix A
- **post-training**：PTQ重建loss用RMSE进行梯度归一化，属于量化优化。

**2610.00981 · NarrativeFlow: Flow-Based Vision-Language-Action Model Using Robot Velocity Fields**

[论文](https://arxiv.org/abs/2610.00981)

- **foundation-model**：NarrativeFlow双任务token与叙述差分训练监督增强语言条件机器人flow，可作算法候选。
  复现边界：主贡献flow不是完整endtoend新VLA；固定相机且起始末端可见，需配既有flowcontrolpolicy。无原指令样本由初/终图生成指令，须区分人工自然指令测试；goal/GTflow只train/oracle，不得常规inference读取。项目页存在但未核作者源码，teacherforcinghistory到rollout偏移须测。
  核查位置：§3.1–3.5 Eq1–5；§4.1；§5.1–5.2；App B/E

**2610.00979 · RISED: RubrIcs for agentic multi-environment Selection and sElf-Distillation**

[论文](https://arxiv.org/abs/2610.00979)

- **agent**：RISED固定rubric词表(4环境82/主3环境59)，Qwen32B异步tag每rollout；环境roundrobin定quota下MMR pooled相关−已选冗余选64/128groups，正负rubric选样但teacher仅top3positive union，k3OPD重要性比+GRPO，负rubric用于steer。3环境Qwen3/4B，强baseline仅+1.2/.6pp；半optimizer步不等半总成本，62.9%zero-variance组OPD仍有信号；删distill消融同时删negative steering要注明。
  核查位置：§2.2/2.4；§3 Eq2；§4.1/4.3；§5

**2610.00977 · ABSENTIA: Detecting Broken Access Control Vulnerabilities in Web Applications**

[论文](https://arxiv.org/abs/2610.00977)

- **agent**：ABSENTIA应用profile→双LLM抽pattern并集构routegraph→逐route声明invariant、查enforcer并source-grounded反例→共享file跨routecomposition，byte-identical依赖闭包缓存跨commit复用。BAC30已披露漏洞25项目，advisory/fix仅oracle；fixednegative仅对应bug非全repo安全，precision独立human73sample未确认LLMjudge增益。静态白盒defensive审计算子合格，代码正文willavailable不能声明已发布。
  核查位置：§4.1–4.4；§5.1–5.2；§7；Code Availability

**2610.00952 · A Matched-Budget Audit Framework for Recaptioned Image-Text Supervision Distributions**

[论文](https://arxiv.org/abs/2610.00952)

- **foundation-model**：Matched-Budget Recaption Audit在同源图片同文本预算下比较caption覆盖、prefix集中度、CBU密度与图像支持风险，适合作预训练数据筛选诊断。
  复现边界：词窗和regex lexical单位不同必须忠实记录；CBU提取固定Qwen、judge换Gemma并未完全独立，人评仅43resolvedclaims。只caption监督审计，不证明下游T2I训练更好；490Mcaption不可自动当作有权重发源图片，安全/PII/去重仍由训练管道处理。
  核查位置：§4.1–4.2；§5.2–5.4；§6–7

**2610.00899 · TOAST: Stochastic Robot Action Tokenization for Autoregressive Vision-Language-Action Models**

[论文](https://arxiv.org/abs/2610.00899)

- **foundation-model**：TOAST动作分词随机监督是清晰的基础VLA训练算子，可优先在公开LIBERO做同预算验证。
  复现边界：不是动作噪声增广；同step不代表同targettoken FLOPs，需记实际token长度。真实4任务mean50.8相对det+15.8，不能外推开放任务；invalidtokenchunk丢弃重试需统计。项目页声明code但本次未提取到公开代码库链接，OpenPI仅基座。
  核查位置：§IV；§V-A–D TablesIII/V；官方项目页

**2610.00885 · FORALL-LEAN-AGENT for Auditable Reasoning in Formal Mathematics and Software Verification**

[论文](https://arxiv.org/abs/2610.00885)

- **agent**：Forall-Lean-Agent隔离actor与fresh readonly reviewer、同artifact digest双批准；proofbodyless检索、OS全进程树sandbox/provider-only proxy、syntax/name-shadow/axiom审计，再serial clean验证。100VSB/672Putnam与2LeanEval；benchmarkrule/strict/independentkernel分母不同，legacy参考泄漏与filedrift有排除不能算能力。成本/compile/review预算非一致，不把harness收益归单模块。
  核查位置：§3.1–3.6；§4；§5.3；§6

**2610.00878 · UniTrackPLA: Unified Panorama-Language-Action Model for Instruction-Guided Navigation and Dynamic Person Tracking**

[论文](https://arxiv.org/abs/2610.00878)

- **foundation-model**：UniTrackPLA 将 DINOv2/SigLIP 全景多视图输入与时间/方位编码映射到机器人航点，WAC 预测动作后的潜变量并以观测误差触发重规划。OmniTrack/OmniVLN 可做路由隔离验证。
  复现边界：数据实际可下载与训练 checkpoint 尚待实现前核验；EP@0.2 不是 Success Rate；真实 Go2-W 硬件证据不能替代本地测试。
  核查位置：§III; §IV; Tables I–III

**2610.00864 · Kinematic MeanFlow: One-Step Action Generation Policy for Robotic Foundation Models**

[论文](https://arxiv.org/abs/2610.00864)

- **foundation-model**：K-MF将MeanFlow时间导数拆成双区间JVP，提供真实的一步动作生成训练机制。
  复现边界：双JVP训练增时≤33%，一步不是无额外训练；H20训练/L40与Orin延迟未替代A100。正文futurecode，mainREADME404不等全库不存在，发布状态未验证；不能拿Euler单步替核心loss，不涵盖全身/灵巧手。
  核查位置：§3.2 Eq5–9；§4.1–4.5；App C/E；Limitations/Reproducibility

**2610.00779 · Effective Synthetic Data Curation Requires Group-Level Signals**

[论文](https://arxiv.org/abs/2610.00779)

- **post-training**：group-level influence评估下游训练效用，以组内梯度diversity优先分配昂贵group oracle调用，未审组用individual proxy；真实pretrain/RLVR训练，需隔离reference与test。

**2610.00767 · Pre-training interventions, ex post facto: Grafting model beliefs across checkpoints**

[论文](https://arxiv.org/abs/2610.00767)

- **post-training**：在base checkpoint学synthetic-document增量再加到post-trained模型，减少reality drift；多个模型及284B规模实测，区别于旧GRAFT的轨迹交换。

**2610.00717 · Sequential Functional Structured Tucker Compression for Large Language Model Attentions**

[论文](https://arxiv.org/abs/2610.00717)

- **foundation-model**：FTC真实顺序student激活度量、共享QKV Tucker与稀疏core联合字节预算、WO独立teacher-map校准，含同度量SeqSVD/等存储core消融，作为模型压缩候选。
  复现边界：主表本法256校准窗口而baseline128，Qwen2.5-7B强压缩128时PPL12.55→43.90，不能宣称全部等数据净收益；实际2:4 core强压缩58.50，不能把非结构稀疏直接当GPU加速；未核到作者代码。
  核查位置：§3.1–3.5 Eq1–4；§4.1–4.3 Tables1–3；Appendix A.4 Tables17–18
- **post-training**：FTC顺序Tucker attention压缩，无RL/OPD；已转基础模型轨道，不能作为全局淘汰理由。

**2610.00710 · ReLiveGym: Evaluating Long-Lived Agents over Weeks of Replayed Reality**

[论文](https://arxiv.org/abs/2610.00710)

- **agent**：ReLiveGym8任务真实流回放数周，clock只在wait推进不模拟LLM延迟，observations按timestamp隔离；deterministic timedcommit score+hardcostwallet，sleep/watcher/cron和dailyhindsightmemory/BoNprune。BoN仅过去已结算反馈选次日，无未来gold；某任务得益非全面。官方代码/8scorer/config公开但无数据随仓，DATA提供公开重建而bundle链接占位；需33GB，时间推断有误差，Linux无OSfence仅禁shell。
  核查位置：§3.1–3.3；§4.1–4.2；§5.3；官方README与DATA.md

**2610.00675 · LabBook: Harnessing Experimental History for Efficient LLM-Driven Discovery**

[论文](https://arxiv.org/abs/2610.00675)

- **agent**：LabBook单自由文本semanticmemory+losslessexperimentlog，latest完整code/result+best/stagnation信息自动入context，agent最多5次History/Code/Result只读检索并共同输出完整新program与memory，不强制bestparent。49FrontierCS+9公开任务同模型prompt/evaluator，去memory/去retrieval、fullhistory/最高分检索消融；跨任务分数按各task最佳归一仅聚合，测试选择应validation隔离。代码willrelease但机制完整可候选。
  核查位置：§3.1–3.3 Eq1–3；§4.1–4.4；Code availability

**2610.00666 · VisionQ: VLM-as-a-Judge Taxonomy, Dataset and Benchmark for Qualitative Analysis in Computer Vision**

[论文](https://arxiv.org/abs/2610.00666)

- **foundation-model**：VisionQ具备新VLM judge基准执行与DPO训练代码，可作作者声明一致性的诊断评测，不能包装为客观视觉质量或自动审稿能力。
  复现边界：groundtruth作者声称winner未经独立人类验证；overall gain95%CI[-1.9,+7.0]，明确有效主要位置偏差减少；position swap与symmetry无独立归因；checkpoint900选择须另设val；figure crops仅非商业，公开源污染未排除。
  核查位置：§3.2–3.4；§4；§5.1–5.4；§6；官方README Benchmark/Judge

**2610.00663 · Backdoor Containment via Expert Quarantine and Shutdown in LLMs**

[论文](https://arxiv.org/abs/2610.00663)

- **foundation-model**：QES用attention-derived软trigger定位、sample peakiness调制、四routing约束训练expert LoRA并关闭隔离expert；不依赖gold trigger，实际两任务三攻击多模型。
  复现边界：独立核读§4–6和App.D：对Sleeper数字trigger、GQA下VPI稀有token及自适应/句法隐蔽trigger有明确失败；attention定位不是可靠oracle。§5默认超参依据单cell ablation，未来须独立validation选择。
  核查位置：Abstract（完整摘要逐条审查）；§4.1–4.2 Eq.1–8；§5
- **post-training**：QES用attention-derived软trigger定位、sample peakiness调制、四routing约束训练expert LoRA并关闭隔离expert；不依赖gold trigger，实际两任务三攻击多模型。

**2610.00661 · Exploring More, Reasoning Better: Stepwise Risk-Sensitive GRPO for Diffusion Language Models**

[论文](https://arxiv.org/abs/2610.00661)

- **post-training**：StepRS-GRPO按denoising maskedness调风险系数并变换组优势，保留原diffusion trainer；binary reward下仅状态/题目重加权，真实SDAR1.7/4B训练和mass/RMS controls。

**2610.00651 · Agent Evaluation Reliability: More Tasks Won't (Always) Fix An Agent Leaderboard**

[论文](https://arxiv.org/abs/2610.00651)

- **agent**：Bernoulli-logit Bayesian交叉variance分解区分model与model-scaffold部署对象，π²/3剩余项因单cell重试不足不可再分。29,923HAL/54model13scaffold，D-study后验传播显示加任务不能消掉model×scaffold/benchmark方差；均衡exchangeable且setupcost假设下的breadth结论非任意新任务更好。官方MIT R/Stan tests+公开outcomes、美元是价格假设非实测，可纳评测可靠性/预算分配分析工具。
  核查位置：§3.1–3.5 Eq2/8/9；§4；§5.3；官方README

**2610.00648 · Incident-Arena: Getting agents to the last nine of reliability**

[论文](https://arxiv.org/abs/2610.00648)

- **agent**：IncidentArena20K8s故障3substrates，hidden deterministic outcomeSLI+restart/reattack安全gate，healthy阈值先冻结，oracle/noop+adversarial QA；nativeharness3000trials，13Slack导致coverage不均、reasoning差异CI宽，rewardhack posthocjudge不等hidden scorer。官方Apache2任务/Harborfork公开，LinuxDocker8CPU16GB40–77GB；需隔离cluster/secret并不能用生产权限直跑。
  核查位置：§3.1–3.4；§4；§5.3–5.4；§6；官方README

**2610.00613 · Spatial Strategies, Not Actions: Vector-Quantized Geodesics as Tools for LLM-Driven Agents**

[论文](https://arxiv.org/abs/2610.00613)

- **agent**：离线250geodesic五步片段原点归一VQ/Kmedoids压5prototype，加5primitivewait工具；LLM一次描述、运行只选五步openloop，optionalcollisionfilter仅已观察障碍。单QwenVL格世界无高维泛化，signedmeasure动态增skill纯proposal未测；需保留真实geodesic采样与VQ，不用手写技能冒充。机制可作spatialtool建库候选。
  核查位置：§4.1–4.4；§5/Table1；§6

**2610.00604 · MIKASA-Robo-VLA: Benchmarking Memory in VLA Models for Long-Horizon Manipulation**

[论文](https://arxiv.org/abs/2610.00604)

- **foundation-model**：MIKASA-Robo-VLA提供ManiSkill3 90任务、两RGB+7D状态/动作统一接口、success_once与22500示范，可补真实执行的VLA记忆评估候选。
  复现边界：示范oracle 1.0是成功筛选后不是原始成功率，privileged simulator只允许teacher/评测。LeRobot无per-step reward且两格式无共享episode ID，不可按indexjoin。基线只14任务单checkpoint、无历史，与记忆因果结论不同；任务gap非完全factorial，机器人实物迁移未测。
  核查位置：§3.1/3.4–3.6；§4.1–4.2；§6；Appendix D

**2610.00574 · Make Sparse Rewards Count: Density-Aware Reward Aggregation for Multi-Reward RL**

[论文](https://arxiv.org/abs/2610.00574)

- **post-training**：DARA按各reward活跃group密度sqrt(max-density/density)有上限加权，Asym仅放大正优势再batch normalize；ToolRL/BFCL-v4与数学真实训练。

**2610.00573 · FORTE: Adaptive Scoring and Exact Keyframe Selection for Long-Video Question Answering**

[论文](https://arxiv.org/abs/2610.00573)

- **foundation-model**：FORTE 在有限打分预算内用带状 RBF-GP 估计帧相关度和时间覆盖边际收益，再用精确 O(KN) 上包络动态规划选 64 帧。公开长视频 QA 可验证。
  复现边界：原作者代码仅承诺发表后开放；GP 打分编码计入预算；相对 uniform 没有端到端速度提升证据；不得在测试基准选最佳参数。
  核查位置：§3.2–3.3; §4.1–4.4; Appendix C/D

**2610.00568 · Emergent Unfaithfulness: How Alignment Training Causes Language Models to Silently Override Task Faithfulness**

[论文](https://arxiv.org/abs/2610.00568)

- **post-training**：FaithConflict公开940对确认/冲突文档、FaithGap与8行为/7推理类型judge，22 checkpoint×prompt条件；官方代码数据已可读。任务忠实性和事实正确性必须分开，不能以复述有害虚构文档作为安全改善指标。

**2610.00559 · PhysVista: Benchmarking Physical Intelligence in VLMs via a Perception-Reasoning-Assessment Loop**

[论文](https://arxiv.org/abs/2610.00559)

- **foundation-model**：PhysVista以公开视频帧和题目定义感知/因果/物理评估多任务，补充物理VLM评测覆盖，可接入为公共基础设施候选。
  复现边界：outcome uncertainty正确答案恒Indeterminate易shortcut；实景统一score5，real/generated域线索；人工反事实标签非物理模拟金标。官方README笼统其余accuracy与论文localizationIoU冲突，接入必须核并保留论文定位指标，不称已有完整harness。
  核查位置：§3.2–3.4；§4.1–4.5；官方README Data Loading/Model Input

**2610.00541 · Random Recursive Models**

[论文](https://arxiv.org/abs/2610.00541)

- **foundation-model**：RRM逐样本逐步均匀有放回选择可复用层，真实随机递归训练；TRM+RRM保持完整TRM设置只换层顺序提供核心控制，纳入小规模递归架构研究候选，不称大模型能力已证实。
  复现边界：三seed主要是固定checkpoint的推理随机seed，不是独立训练。CIFAR/Zebra增加深度常平台或退化；深度监督不可移除。PTRM100轨迹仅固定1000题子集，非单样本能力。
  核查位置：§3 Eq4–6；§4；§5.1–5.5 Tables1–6

**2610.00499 · Denoising Surface: Modeling and Predicting Inference Cost for Diffusion LLM Serving**

[论文](https://arxiv.org/abs/2610.00499)

- **foundation-model**：DWS将扩散解码负载分解为block存活概率和条件denoise-step存活概率，MiniLM两阶段多尺度/Brier监督，CPU INT8预测加硬件成本剖面驱动SJF。
  复现边界：100k训练含10k验证、10k独立测试；真实成本模型测试用GT轨迹必须与prompt预测分开。模型家族、block大小、解码阈值改变需重训；batch96/SGLang实测不保证其他引擎，等待30秒折扣10%的aging要保留。
  核查位置：§4 Eq6–8；§5 limitations；§6.1–6.4

**2610.00497 · Gumbel Straight Flow: Distilling Autoregressive Models into One-step Flow Maps**

[论文](https://arxiv.org/abs/2610.00497)

- **foundation-model**：Google DeepMind Amsterdam参与GSF：AR Gumbel耦合直路径+单调Gaussianization+diagonal教师/semigroup自一致flow-map损失，官方正文含同架构同迭代FMLM-re控制及teacher-forced后验Gumbel训练算法。
  复现边界：最优路径直线性假设充足容量，真实student远落后ARteacher；四步D-MMD更好但模型近2倍。多数外部baseline用原文值；温度sweep需独立validation，不能以测试最优当固定配置；接入须计teacher成本。
  核查位置：§3.1–3.2 Eq6–8；§4.1–4.3 Tables2/6–8；Appendix C Algorithms1–2；Appendix D–E

**2610.00487 · ScaffoldM3C: A Multimodal Sequential Monte Carlo Framework for Generative Stable Construction Planning**

[论文](https://arxiv.org/abs/2610.00487)

- **foundation-model**：ScaffoldM3C 以 Gemma 条件编码和位置/类别/候选似然三头生成砌块，SMC 对碰撞修复位移惩罚、采样重加权并选最长稳定构建序列。StableText2Brick 可重建监督。
  复现边界：必须逐步检查支撑稳定性而非仅末态；SMC 是模型候选后验，不是直接读取目标序列；真实 xArm 不必纳入模拟能力声明；自建13条件序列未核验发布。
  核查位置：§III-C/Algorithm1; §IV/Eq6–7; §V; §VI–VIII; Appendix A

**2610.00435 · How AI Agents Discover Scientific Equations: From Hydrotope Rediscovery to New Water-Wave Amplitudes**

[论文](https://arxiv.org/abs/2610.00435)

- **agent**：PI 将解析与数值探索分配给两位学生，共享记录并独立用 BG 递归找反例，重建跨频率 chamber 的全局振幅公式。
  复现边界：团队计算量高于单代理；两次团队成功不是统计总体成功率，140 个精确测试不是全域解析证明；官方公式和测试答案须仅供最终验证。固定 SR split 的模型选择边界须重做独立 validation。
  核查位置：§3.1–3.2、§5.1–5.4、Appendix C/E

**2610.00432 · XOR-Trellis: Ultra-Low-Complexity Dequantization and Curvature-Aware Hadamard-Free LLM Quantization**

[论文](https://arxiv.org/abs/2610.00432)

- **foundation-model**：XOR-Trellis以16位状态和每步2位分支生成四值FP4 palette，LDLQ调整目标加D加权Viterbi保留曲率，无需Hadamard旋转。
  复现边界：384 RedPajama、seed0、无finetune；2.25有效bpw含组32 scale，必须实现状态/位流而不是独立round。简单指令解码不自动证明端到端CUDA速度，FP4原生硬件收益不能在A100以模拟声称。
  核查位置：§3 FP4 palettes；§4.2–4.3；§5/Table1–3；Appendix D

**2610.00431 · ChainLoRA: Geometry-Preserving Task Vector Merging for Continual Learning in LLMs**

[论文](https://arxiv.org/abs/2610.00431)

- **post-training**：ChainLoRA按QR carrier链式初始化、一侧几何正则，归档后SVD共同carrier与Procrustes对齐再共享/残差merge；真实持续学习三套数据。

**2610.00400 · Representation Transitions Reveal Emerging Safety Risks in Multi-Turn LLM Agents**

[论文](https://arxiv.org/abs/2610.00400)

- **agent**：DART 用危害减良性 transition 均值方向，去除良性均值和主协方差方向，在 segment 边界累积投影，阈值触发后定位最大贡献段并添加提醒再生成。
  复现边界：层/rank 在 inner validation 选择、良性 calibration 定阈值；必须真实 hidden-state transition。ASR/Utility 为最终是否拒绝代理指标，不是工具危害成功率；检测全中仍25%成功说明提醒存在失败。模型相关方向不得通用复制。
  核查位置：§3–5、Algorithm 1、Appendix A/F/G

**2610.00399 · Metacognitive Reasoning in Energy Based Models using Instance Based Learning Theory**

[论文](https://arxiv.org/abs/2610.00399)

- **foundation-model**：MERITED以191M EBT能量分布+问题embedding的经验相似性选择MCMC深度或逐步stop，20训练记忆例构建状态动作回报，可作动态计算机制诊断。
  复现边界：原实验450配置在同评估集选且实际一split/seed，误差条是两任务变化，不是10独立run；OpenBookQA用train。optimal-stop计时预缓存测试trajectory energy，未计状态取得成本；须改为实时state和独立val/test才可声称效率/泛化，保留论文协议回放为诊断。
  核查位置：Algorithm2–3；Tasks and Data Splits；IBL State, Memory, and Depth Control Eq7–8；Metrics, Timing, and Statistical Analysis

**2610.00385 · FAER: Auditable Utility-Aligned Trajectory Replay for Language Model Post-Training**

[论文](https://arxiv.org/abs/2610.00385)

- **post-training**：FAER-UTILITY在非target calibration块拟合梯度对齐/metadata replay权重并无放回抽样，trace冻结后才join正确性；正文完成learner行用normalized alignment，optimizer-aware虚步仅扩展/诊断，不能混称已验证。

**2610.00372 · When Harnesses Lose the Signal: Causal Evaluation of Recovery in LLM Agents**

[论文](https://arxiv.org/abs/2610.00372)

- **agent**：CIR 从同一环境状态配对重放 refresh/不 refresh，区分 rescue 与 harm；三 logistic 模型分别预测异常及两种成功，OOF 阈值在 clean-harm 约束下选择，按时间最多刷新一次。
  复现边界：93拟合任务与75prefix-feasible测试任务分离；成功筛选 cohort 不代表全 ALFWorld。边际概率相乘只是 rescue/harm score，非联合因果概率；干预位置用预录事实轨迹25%是评测设计，在线控制不能访问未来。
  核查位置：§3–5、Eq.1–7、§5.1

**2610.00354 · Proof-Gated Signing: Solver-Checked Transaction Guards that Hold Under State Drift for Onchain AI Agents**

[论文](https://arxiv.org/abs/2610.00354)

- **agent**：Proof-Gated Signing 先模拟交易抽取资产变化，再由 Z3 验证价格区间内策略，编译余额/收款/allowance/owner 后置条件，由钱包原子执行与回滚防止 check-to-inclusion 状态漂移。
  复现边界：保障依赖guard持钥、诚实tracked token、价格带和策略；untracked资产与offchain permit不覆盖。260设计同源脚本不是heldout，9个in-policy慢损失只是session上界而非阻止；须本地链运行不能仅返回ALLOW。
  核查位置：§2 Theorem/Table1、Algorithm1、§3–4

**2610.00313 · Rules to Tools: Executable Checks for LLM Agents in Scientific Computing**

[论文](https://arxiv.org/abs/2610.00313)

- **agent**：Rules to Tools 将公开物理方程/边界/输出约束编成可调用checker，修复时提供artifact实际残差，独立隐藏grader给最终成绩；匹配text与tool组保持书面规则、探针和budget一致。
  复现边界：prepared checker 是支持包处理效应，非证明tool格式本身因果更优；八任务差值CI[-12.5,43.75]pp。flow text点值与tool网格L2 gate不完全等价，开发暴露任务和heldout任务分开。hidden参考数组/评分代码不得进入repair容器。
  核查位置：§3–5、Eq.1–3、Appendix B/C/D/G

**2610.00251 · The Null Is the Hard Part: Exact Tests for Memorization in Generative Models**

[论文](https://arxiv.org/abs/2610.00251)

- **recommendation**：生成模型记忆审计的精确统计零假设与多重校正，转基础模型/多模态评估审查。
- **foundation-model**：模型级随机标签置换与图像级匹配控制conformal/BH审计可补生成记忆评估，官方公开代码含真实测试入口与测量输出。仅接纳为研究评测候选，非已运行或可证明模型不记忆。
  复现边界：SD无随机训练/heldout split，exchangeability是假设；近重复尺度不覆盖语义复制；模型级PCA/Alpha计算限制2000图；失去认证不等于删除记忆。
  核查位置：§2 Propositions1–3；§3/Table1–2；§4–6；Reproducibility statement；official README experiments/genmem.py and genmem_sscd.py

**2610.00204 · Query Independent Variable Rate Visual Token Coding**

[论文](https://arxiv.org/abs/2610.00204)

- **foundation-model**：RDTok 在 query-independent PCA 基底上建逐 token 量化率失真曲线，以整数动态规划分配总 bit 预算。ChartQA/COCO 公共图像及冻结 VLM 可验证压缩。
  复现边界：token 数不减少；必须真实 bit-packing 并计变换元数据而非 fp16 张量声称压缩；PCA 仅训练数据拟合；query 不参与码率分配。
  核查位置：§2.1–2.3/Eq4–5; §3.1–3.4

**2610.00182 · Localizing Post-Wire Semantic Changes in MCP Agent Frameworks**

[论文](https://arxiv.org/abs/2610.00182)

- **agent**：MCP post-wire差分测试用allowlisted projector保留语义atom与compartment，分别检查协议合法、类型语义留存、特定consumer可访问性，并沿各框架公开carrier边界定位。
  复现边界：324捕获与3次新进程是确定性稳定性，不是模型质量样本；H4仅本地provider request，未远端调用；新2026-07-28协议未测。v4包仅重建归一化capture，不重跑框架环境；明确missing与null、text恢复与structured槽不能混计。
  核查位置：§III method、§IV evaluation、Ethics/Reproducibility

**2610.00097 · DramaAgent: Agentic Storytelling Video Generation**

[论文](https://arxiv.org/abs/2610.00097)

- **foundation-model**：DramaAgent长故事视频分层控制与修补，agent track负责。
- **agent**：DramaAgent 层级分镜、固定角色reference、逐scene候选视频与音频生成，以身份/语义/时序/音画加权评估，针对最弱维度改写并有限次数重生成。
  复现边界：真实video/audio生成是定义核心，文字fixture不能称复现；τ=.8、epsilon=.02、R=2与K预算冻结并validation选。API/backbone、候选数和重试成本匹配，VLM评分与人工偏好分开；音画兼容非严格lip-sync。
  核查位置：§3.1–3.5、Eq.1–9、Appendix B/D

**2610.00040 · DSSR-3D: Decoupled Reasoning for View-Dependent Referring in 3D Gaussians**

[论文](https://arxiv.org/abs/2610.00040)

- **foundation-model**：DSSR-3D 用 FLAN-T5 分析目标/方位/锚点，语义 Gaussian softmax 定位锚点，在相机 XZ 平面做局部方向衰减并融合目标分数。Ref-LERF 公开场景支持验证。
  复现边界：近水平视角、单锚点限制；语义场已预训练，非全流程 training-free；ViewRef-GS 生成 GT 使用 GroundingSAM，应避免同源评价泄露；自建场景发布需另核验。
  核查位置：§3.2–3.6; §4.1–4.2; §5.2–5.3; §6

**2610.00025 · Measuring the Microtask Eligibility Gap: When Is an Off-the-Shelf SLM Enough for an Agent Harness?**

[论文](https://arxiv.org/abs/2610.00025)

- **agent**：四microtask用非LLM基线预定质量门槛和CI判定SLM eligibility；calibration上选logprob operating point，memory BM25 shortlist→SLM rerank及tool基线gating。
  复现边界：0/16是固定prompt/模型条件，非所有SLM不行。oracle-on-test仅可达上界，不可部署；量化T2/T4材料不足以重构完整ranking/selection，因此只能diagnostic。阈值为单部署者偏好，质量eligibility不含真实成本。
  核查位置：§3–7、Table1–2、Appendix G–I

**2610.00012 · When Do Causal World Models Help Modular LLM Agents**

[论文](https://arxiv.org/abs/2610.00012)

- **agent**：FedCausalCompose的局部干预响应匹配、边发现与组合约束可作诊断性Agent世界模型候选；真实实现必须学习边，不能以oracle边替代。
  复现边界：实际为集中式trace harness而非部署的联邦隐私系统；人工模块/oracle理论假设强，ALFWorld对正确边比例非单调30/45/20/35/40，部分划分退化25pp，多数单种子；AndroidWorld未运行。
  核查位置：§4；§5/Table1；§6–7；官方仓库README

**2610.00010 · Heavy-Tailed Memory Traces in Long-Horizon Language Agents**

[论文](https://arxiv.org/abs/2610.00010)

- **agent**：CTWM以访问排名幂律预算分配核心/尾部记忆，适合作为可执行记忆压缩机制候选；不能将近零任务成功率的token节约宣传成能力提升。
  复现边界：图紧凑基线156.4token比CTWM160.7更低但错误更高；ALFWorld one-shot均0/18，three-shot图1/18而CTWM0/18，LongMemEval77例CTWM0而图3正确；24.48%省token不构成任务能力改善。τ=1手选；不得凭该诊断直接evolve晋级。
  核查位置：§4；§5.4–5.7 Tables3–5；AppendixA.1/B；官方仓库README

**2602.16490 · From Growing to Looping: A Unified View of Iterative Computation in LLMs**

[论文](https://arxiv.org/abs/2602.16490)

- **foundation-model**：Google合作历史漏收录：grow-first/loop-later组合配方与中间block recurrence有真实SmolLM训练、22公共任务及参数/训练/推理三类预算对照；可纳入循环模型研究候选，不称10月新文。
  复现边界：2倍仅部分reasoning primitives，额外loop增加推理计算；知识/语言任务loop可退化；block/数学源在下游基准上做ablation选择，正式复现需独立validation。官方全文/Google页未找到作者代码链接。
  核查位置：§3.1–3.2/Table1；§5.1–5.3/Table2/Table3；Appendix A；Appendix C.3/Figure17；Appendix D–E

**2510.15831 · VISTA: A Test-Time Self-Improving Video Generation Agent**

[论文](https://arxiv.org/abs/2510.15831)

- **agent**：Google高优先历史补发现：结构化prompt规划、双向tournament保留champion、三维normal/adversarial/meta批评、DTPA修订后实际重生成/再选，属于可执行Agent自改进闭环而非视频主干创新。
  复现边界：首次2025-10-17，不计2026新论文；官方项目仅demo/prompts和论文，未发现作者源码发布；内部161prompt不可得；约.7M token/轮且排除视频生成cost；复现需实际多模态judge和video generator，非固定视频打分fixture。
  核查位置：§2.1–2.2/Algorithms1–2/Eq1–3；§4.1/Table2正文；§4.2；§4.3/Tables3–4；Limitations；官方project


## 已有记录（48）

**2610.03702 · LESSER: Post-Training Data Selection with Output-Layer Gradients**

[论文](https://arxiv.org/abs/2610.03702)

- **post-training**：ledger已实现LESSER；记录为L1输出层梯度/选择诊断，不等于LLM训练benchmark。

**2610.03675 · FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution**

[论文](https://arxiv.org/abs/2610.03675)

- **agent**：仓库已有FrugalEvo；本轮摘要与旧全文+代码审查一致，不重复登记实现。
  核查位置：Title and complete abstract

**2610.03665 · Pivot-SD: Efficient Self-Distillation for Masked Diffusion Language Models**

[论文](https://arxiv.org/abs/2610.03665)

- **post-training**：ledger已全文审查Pivot-SD但尚未实现真实扩散轨迹训练，保留既有unresolved状态。

**2610.03634 · Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents**

[论文](https://arxiv.org/abs/2610.03634)

- **agent**：仓库已收录DepGPO command依赖图信用分配，不重复登记。
  核查位置：Title and complete abstract

**2610.03515 · Learning from Repaired Reasoning: Root-Cause-Guided On-Policy Distillation**

[论文](https://arxiv.org/abs/2610.03515)

- **post-training**：ledger已审查RC-OPD方法及作者评测仓库；真实repair-continuation与训练仍未实现。

**2610.03361 · Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT**

[论文](https://arxiv.org/abs/2610.03361)

- **post-training**：ledger已实现FTW；L1 FIFO/top-K/KL CPU机制诊断，尚无Search-R1/Sokoban训练证据。
- **agent**：FTW已收录，critic-free cross-entropy replay ordinal filter。
  核查位置：Title and complete abstract

**2610.03223 · AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.03223)

- **post-training**：ledger已实现AdaStep；L1合成returns方差算子，没有agent policy训练。
- **agent**：AdaStep已收录，step credit信号/方差shrinkage。
  核查位置：Title and complete abstract

**2610.02994 · Sentry: Learning to Recover from LLM Agent Failures at Test Time**

[论文](https://arxiv.org/abs/2610.02994)

- **agent**：Sentry已收录且旧审查为全文+仓库；reward-blind故障恢复，不重复。
  核查位置：Title and complete abstract

**2610.02199 · TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning**

[论文](https://arxiv.org/abs/2610.02199)

- **foundation-model**：ledger已收录taco-optimizer，沿用既有结论。

**2610.02163 · AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents**

[论文](https://arxiv.org/abs/2610.02163)

- **foundation-model**：ledger已收录autocompact，沿用既有结论。
- **post-training**：ledger已在Agent目录收录AutoCompact，避免跨track重复实现。

**2610.02148 · Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation**

[论文](https://arxiv.org/abs/2610.02148)

- **foundation-model**：ledger已收录omni-embed-mini，沿用既有结论。

**2610.02117 · Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes**

[论文](https://arxiv.org/abs/2610.02117)

- **foundation-model**：ledger已收录where-opd，沿用既有结论。
- **post-training**：ledger已实现Where-OPD，保留synthetic scene privileged spatial指导的既有结论。

**2610.02076 · LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them**

[论文](https://arxiv.org/abs/2610.02076)

- **foundation-model**：ledger已收录llm2jev，沿用既有结论。

**2610.02057 · Optimizing Effective Training Time for Large-Scale Recommendation Systems**

[论文](https://arxiv.org/abs/2610.02057)

- **recommendation**：ETT 已在统一 manifest 实现，不重复登记为新增。

**2610.02039 · CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.02039)

- **post-training**：ledger已实现CARM逐token绝对log-ratio response masking。

**2610.02002 · Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents**

[论文](https://arxiv.org/abs/2610.02002)

- **foundation-model**：ledger已收录mem-plus-plus，沿用既有结论。
- **agent**：Mem++已收录，完整文档时点过滤与lexical/semantic读时融合。
  核查位置：Title and complete abstract

**2610.01973 · Token-Level Video Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.01973)

- **foundation-model**：ledger已收录tvrl，沿用既有结论。

**2610.01896 · Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis**

[论文](https://arxiv.org/abs/2610.01896)

- **post-training**：ledger已实现GMC-GRPO，对异步组importance weight作mass capping。

**2610.01785 · VETO: Video Efficient Token Optimization for Vision Language Models**

[论文](https://arxiv.org/abs/2610.01785)

- **foundation-model**：ledger已收录veto，沿用既有结论。

**2610.01705 · AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation**

[论文](https://arxiv.org/abs/2610.01705)

- **recommendation**：AgentWebRec 已实现；只复核注册，不重复列作本轮新增。

**2610.01548 · Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals**

[论文](https://arxiv.org/abs/2610.01548)

- **post-training**：ledger已实现Range-GRPO，以conformal reward interval pairwise relation计算优势。

**2610.01533 · Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)**

[论文](https://arxiv.org/abs/2610.01533)

- **recommendation**：GrIS 已实现；只复核注册，不重复列作本轮新增。

**2610.01511 · GAW-PO: Preference Optimization with Gradient-Aligned Token Weights**

[论文](https://arxiv.org/abs/2610.01511)

- **post-training**：ledger已实现GAW-PO，按梯度对齐给DPO rejected token重新加权。

**2610.01509 · Sharpening Tax in Post-Training**

[论文](https://arxiv.org/abs/2610.01509)

- **foundation-model**：ledger已收录sharpening-tax，沿用既有结论。
- **post-training**：ledger已实现Sharpening Tax/PTGS，避免将已收录diagnostic误作新候选。
- **agent**：Sharpening Tax/PTGS已收录，难度posterior温度采样。
  核查位置：Title and complete abstract

**2610.01434 · MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs**

[论文](https://arxiv.org/abs/2610.01434)

- **foundation-model**：ledger已收录mwop，沿用既有结论。

**2610.01415 · Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States**

[论文](https://arxiv.org/abs/2610.01415)

- **agent**：PoS显式belief state与trapping恢复已收录。
  核查位置：Title and complete abstract

**2610.01395 · AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models**

[论文](https://arxiv.org/abs/2610.01395)

- **foundation-model**：ledger已收录af-muon，沿用既有结论。

**2610.01349 · PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents**

[论文](https://arxiv.org/abs/2610.01349)

- **agent**：PACE已收录，影响路径cut/能力effect执行前门控。
  核查位置：Title and complete abstract

**2610.01270 · Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders**

[论文](https://arxiv.org/abs/2610.01270)

- **recommendation**：REPAIR 已实现；只复核注册，不重复列作本轮新增。

**2610.01256 · DeFA: Dependency-Guided Failure Attribution for LLM Agents**

[论文](https://arxiv.org/abs/2610.01256)

- **agent**：DeFA依赖/失败传播图归因已收录。
  核查位置：Title and complete abstract

**2610.01207 · Dependency-Aware Reward Shaping for Agentic Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.01207)

- **agent**：DARS依赖图predicate potential reward shaping已收录。
  核查位置：Title and complete abstract

**2610.01161 · My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.01161)

- **post-training**：ledger已实现My FAULT自诊断terminal credit redistribution，保持既有保真度声明。
- **agent**：FAULT自诊断错误成本与terminal credit redistribution已收录。
  核查位置：Title and complete abstract

**2610.01073 · Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover**

[论文](https://arxiv.org/abs/2610.01073)

- **agent**：RSI Safety当前contract验证/validated rollback已收录。
  核查位置：Title and complete abstract

**2610.01026 · It Takes Workflows to Evolve Better Workflows**

[论文](https://arxiv.org/abs/2610.01026)

- **post-training**：ledger已在Agent目录实现FloWright，非新候选。
- **agent**：FloWright结构分层奖励/多role共演化已收录。
  核查位置：Title and complete abstract

**2610.00972 · VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks**

[论文](https://arxiv.org/abs/2610.00972)

- **agent**：VeriHarness disagreement/consensus evidence verifier已收录。
  核查位置：Title and complete abstract

**2610.00964 · RPTune: Learned Context Curation for LLM Catalog Search**

[论文](https://arxiv.org/abs/2610.00964)

- **foundation-model**：ledger已收录rptune，沿用既有结论。
- **post-training**：Google RPTune已收录；ledger注明七商家实验及本地L1 curation，不能重复纳新。

**2610.00958 · Role-aware Heuristic Episodic Attention for Conversational LLMs**

[论文](https://arxiv.org/abs/2610.00958)

- **foundation-model**：ledger已收录rea，沿用既有结论。

**2610.00906 · ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization**

[论文](https://arxiv.org/abs/2610.00906)

- **agent**：ActiveSaddler非平稳failure-pattern bandit课程已收录。
  核查位置：Title and complete abstract

**2610.00872 · MemFit: Efficient Long-Term Agentic Memory**

[论文](https://arxiv.org/abs/2610.00872)

- **agent**：MemFit append-only原始turn/多路径cross-encoder retrieval已收录。
  核查位置：Title and complete abstract

**2610.00838 · SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.00838)

- **post-training**：已有SHARPO条目；ledger L12601，沿用既有实现/证据边界，不重复收录。
- **agent**：SHARPO分段teacher-student优势重加权已有post-training/sharpo目录，本轮不重复收录。
  核查位置：Title and complete abstract

**2610.00650 · Self-Evolving Coding Rules for AI Coding Agents**

[论文](https://arxiv.org/abs/2610.00650)

- **agent**：RuleEvolve编码规则池变异-评测已有agent-research/rule-evolve目录，不重复收录。
  核查位置：Title and complete abstract

**2610.00623 · HAWK: Rethinking Multimodal Drafting for Speculative Decoding**

[论文](https://arxiv.org/abs/2610.00623)

- **foundation-model**：输入标注已实现HAWK，需引用ledger既有记录。

**2610.00437 · JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces**

[论文](https://arxiv.org/abs/2610.00437)

- **agent**：JevSpawn组合动作空间与反馈分支选择已有agent-research/jev-spawn目录。
  核查位置：Title and complete abstract

**2610.00426 · IrekoGPT: Turning Structured Pruning into Post-Hoc Slimmable LLMs**

[论文](https://arxiv.org/abs/2610.00426)

- **foundation-model**：输入标注已实现IrekoGPT，需引用ledger既有记录。

**2610.00388 · T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.00388)

- **post-training**：已有T2SPO；ledger L12689明确仅真实TabPFN CPU合成状态+objective，无LLM任务训练。
- **agent**：T2SPO用TabPFN轨迹剩余距离产生step credit已有post-training/t2spo目录。
  核查位置：Title and complete abstract

**2610.00333 · LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation**

[论文](https://arxiv.org/abs/2610.00333)

- **foundation-model**：输入标注已实现LEGO-OPD，需引用ledger既有记录。
- **post-training**：已有LEGO-OPD条目，ledger L12603；沿用既有factorized teacher证据。

**2610.00332 · The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.00332)

- **post-training**：已有Weakest Link，ledger L12690明确L1 exact-vocab梯度及小策略prefix约束，无LLMbenchmark声明。

**2610.00317 · DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies**

[论文](https://arxiv.org/abs/2610.00317)

- **foundation-model**：输入标注已实现DriftOPD，需引用ledger既有记录。
- **post-training**：已有DriftOPD条目，ledger L12604；沿用既有一跳drifting/critic证据边界。


## 待审（0）


## 审后延期（113）

**2610.08720 · WorldSolver: Can LLM Agents Simulate the Physical Dynamics via Solver Generation?**

[论文](https://arxiv.org/abs/2610.08720)

- **agent**：WorldSolver的168物理求解器任务/固定scaffold/执行+VLM视觉+物理规则评分适合evolve，但官方链接github.com/sirujiang/WorldSolver网页与API均404，暂不能确认公开任务/评分器/许可，等待可执行发布。
  复现边界：60分pass阈值仅演示非验证标准；评分规则对Agent隐藏；不同模型用不同harness；VLM judge也参与被测模型，需独立审核；代码不可达不是算法无价值。
  核查位置：§2.1–2.3 Eq1–10；§3.1–3.3/Table3；Limitations；官方仓库/API访问2026-10-07

**2610.08526 · WareFly-VLA: A Vision-Language-Action Framework for UAV Navigation and Human Tracking in Smart Warehouses**

[论文](https://arxiv.org/abs/2610.08526)

- **foundation-model**：WareFly-VLA定义507飞行轨迹、4DoF连续动作及431/76 episode级固定split，有独立UAV评测价值；§6仅ground-truth帧上的open-loop MAE/correlation及轨迹积分，非闭环飞行成功率。§Data availability明确数据/runner仍access on request、acceptance后公开，故等待公开入口而非未读完。
  核查位置：§3；§5.2；§6.1 Tables 5–6；§7 limitations；Data availability

**2610.08513 · Wiki-Talkie: Multilingual Benchmarking of Persona-Based Agents on Real-World Discussions**

[论文](https://arxiv.org/abs/2610.08513)

- **agent**：Amazon Wiki-Talkie的五语人口行为分布评测有公共评测价值，但官方amazon-science/wikitalkie返回404，数据又明确申请访问非开放镜像；模型A–D及extractor匿名，现阶段审结待资源。
  复现边界：behavior从用户50随机threads提炼，接入需重新核严格时间/目标排除；history与profile非信息量配平，profile长度分层不能证明因果；模型匿名阻原数值复现；saltedhash不消除文本反识别，群体研究不得个体冒充。
  核查位置：§3.1；§4；§5.2；Limitations/Ethics；official GitHub API2026-10-07

**2610.08400 · Atom-JEPA: Joint-Embedding Predictive Architecture for 3D Atomistic Systems**

[论文](https://arxiv.org/abs/2610.08400)

- **foundation-model**：Atom-JEPA具备真实SE(3)等变原子/子结构预测算法与公开迁移结果，但严格等预算新目标归因尚未满足：§G.1同Uni-Mol atom-only与atom+pool的批量384/128、学习率2.42e-4/1.4e-4不同；§B未做同架构其他SSL比较。需明确可接受的匹配控制或补齐预算证据，不能把scratch对比当等预训练预算。
  核查位置：§3；§4.2/Table4；Appendix B；Appendix G.1/Table26；Appendix H.1.1

**2610.08327 · MedZERO: Self-Evolving Agents for Open-Ended Medical Reasoning Through Controlled Knowledge Accumulation**

[论文](https://arxiv.org/abs/2610.08327)

- **agent**：MedZERO交替训练Examiner/Reasoner与临时→持久KG准入是合格Agent机制；正文明确投稿时不发布代码、计划出版后发布，grounding scorer/映射阈值等关键实现不足，记审结待发布。
  复现边界：多数一致性不是医学正确率；持久准入缺独立事实验证，仍可能自我强化错误；MCQ选项只给后置judge不应给被测Reasoner；临床效用未建立，KG/web/judge依赖明显，正文未充分规定grounding评分函数。
  核查位置：§3 Eq1–21；§4.1–4.2；§5；AppendixB；Open access checklist

**2610.08250 · MASC: A Multi-Agent Self-Calibration Framework with Latent Construct Alignment for Consistent Client Role-Playing in Psychological Counseling**

[论文](https://arxiv.org/abs/2610.08250)

- **agent**：MASC以预测情绪/状态/动作、三Agent五步辩论、投票一致性优先和两轮失败记忆重试维持角色；方法与CRPC评测有关联价值，但官方仓库description明确code and data coming soon且无license。
  复现边界：38profiles及同套构念/提示限制外推；Hetero与Homo骨干不同不能隔离多样性原因；73.97%最终匹配，44.19%是以最终收敛为条件的重试占比非修复概率；KL仅群体标签频率不是治疗真实性。
  核查位置：Multi-Agent Self-Calibration §方法 Eq1–16/Alg1；Experiment Tables2–3；官方GitHub API

**2610.08246 · LeanPlan: Optimal Planning with LLM-Generated Heuristics and Admissibility Proofs**

[论文](https://arxiv.org/abs/2610.08246)

- **agent**：LeanPlan生成Lean启发式+可采纳性证明，controller拒绝sorry/admit/native_decide/新公理且独立重编译与训练任务验收，符合可验证Agent/evolve机制；作者明确代码/benchmark/log接受后才发布，审结待发布。
  复现边界：SCP预算曾用test suite调优，原对照非严格完整test隔离；每domain单次Agent生成，无多seed；证明仅对certificate通过且成本<B计划，不证明unsat，依赖未验证parser/compiler；3test certificate拒绝计未解。
  核查位置：§3–5；§7 Limitations；Reproducibility

**2610.08215 · Learn2Play Bench: How Well Do LLM Agents Learn from Experience in Unfamiliar Environments?**

[论文](https://arxiv.org/abs/2610.08215)

- **agent**：Learn2Play20隐藏规则游戏、deterministic terminal scoring、10fixed/10reshuffled与跨episode学习曲线适合evolve；官网指向Learn2Play-Bench但repo/API/rawREADME均404，未证公共执行/许可，审结待发布。
  复现边界：单instance_seed不等跨seed泛化；max挑顶尖人类不代表普通人均值，游戏hardness由pilot选；rule-discovery证据可含评分窗后episode，不能代替窗内任务成绩；harness批动作/反馈去重与memory机制混合影响成本。
  核查位置：§3；§4.1–4.2/4.6；§5；official project GitHub link/API

**2610.07969 · EmbodiedSmith: Scaling Embodied Data through Recursive Self-Improvement Flywheel in Simulation**

[论文](https://arxiv.org/abs/2610.07969)

- **foundation-model**：EmbodiedSmith完整审查确认数据生成/验证流程有价值，但公开harness、typed skills与最终接受任务包未定位，暂缓基础设施接入。
  复现边界：deformable部分统一材质且释放回弹不全，physicalasset接scene仍futurework；场景内10任务sim数据不证明sim2real/generalist。无可重放源码任务包无法真实验收RSI，不能用预知plan的policy替实现。
  核查位置：§3.1–3.3；§4.1–4.3 Table4；Appendix9/10

**2610.07948 · Confidence Reasoning Graphs: Structured Confidence Estimation for LLM Agents**

[论文](https://arxiv.org/abs/2610.07948)

- **foundation-model**：CRG是agent轨迹的结构化置信度推断框架，应由agent track审查。
- **agent**：CRG成功命题递归必要充分子声明、证据有源引用、叶置信乘积聚合为明确可审计评测器；官方megagonlabs/crg_ce返回404，审结待公开实现。
  复现边界：乘积是条件独立近似，不是概率保证；重叠叶可能重复扣不确定性，缺引用会漏后续修复；BAS改善不等任务能力/辨别率全面提升；官方论文说repo有脚本但本次无法访问。
  核查位置：§4 Eq2–5；§5；§6.2–6.4 Tables3–4；AppendixA.3/A.14.3；official GitHub API

**2610.07863 · ReFold: Training-Free Reversible Inter-Turn Context Folding for Long-Horizon Agents**

[论文](https://arxiv.org/abs/2610.07863)

- **foundation-model**：ReFold属于agent交互上下文可逆渲染层，应由agent track审查。
- **agent**：ReFold append-only原始history、exact重复stub、模型标stale后fold、chunk边界缓存保护及restore追加机制明确，适合上下文优化；正文仅承诺will release code/scripts，当前审结待发布。
  复现边界：高并发解题增益主要包含服务拥塞/超时效应不能称纯推理能力；fullwindow每cell单次taskrecord，非多seed；k扫20SWE任务选参数需独立validation重建；chunk/reversible消融为固定轨迹rerender不是能力比较；A100需另实测。
  核查位置：§3 Eq1–7；§4.1/4.3/4.4；Reproducibility

**2610.07835 · DHCG: Dynamic Construction of Hierarchical Collaboration Graphs for LLM-Based Multi-Agent Reasoning**

[论文](https://arxiv.org/abs/2610.07835)

- **agent**：DHCG逐层动态角色/稀疏routing/Expand或Finalize及action-aware加权DPO机制合格；关键训练datafilter、valuegap阈值/λγ/预算指向AppendixB却官方HTML/PDF均未附，未找到代码，审结待补材料。
  复现边界：缺AppendixB使精确训练/污染核查不可完成；Pass@5为有oracle选择的上界非可执行Agent能力；不能用静态DAG或heuristicplanner代替训练policy；所谓RL实际offlineweightedDPO。
  核查位置：§3.1–3.3 Eq1–14；§4.1–4.5；官方PDF9页（末2页references，无被引用AppendixB）

**2610.07817 · One Step at a Time: Trading LLM Autonomy for Process Predictability**

[论文](https://arxiv.org/abs/2610.07817)

- **agent**：One Step at a Time的SOP-MCP逐步server执行与审计有集成价值，但修订SOP、工具spec、trace、分析代码明确upon publication才发布；正文审查完成，精确公开评测暂缓。
  复现边界：pilot调试同测试任务非独立dev且只MCP trace；逐步呈现/控制/元指令三机制捆绑。coverage只tool名不查顺序参数/输出消费，grounded≠流程正确；mock tools与fuzzy matcher未规模人工验证。不得将≈.3%ungrounded称真实安全或信任提升。
  核查位置：§3; §4.1–4.5 Tables3–4; §5.3; Limitations1–12; Artifacts

**2610.07763 · ST-Bench: A Spatial-Temporal Benchmark for Multi-Agent System Generation on Scientific Research Tasks**

[论文](https://arxiv.org/abs/2610.07763)

- **agent**：ST-Bench 的100科学任务、2067查询及连续reward适合多Agent工作流评测，但原文未给可验证任务/预处理文件/评分器下载入口，暂缓官方接入。
  复现边界：1184/391/492 train/val/test；reward按0.1合法性+0.4阈值+0.5单Agent参考，不是复算科学结果的充分证明；所有指标由Agent报告，须增加产物复算。至少一个正数/-1判无效可能误伤真实非正科学指标。MAS收益主要覆盖率，1.85–4.5倍时间，token成本仅部分可测，不能宣称同预算全面更强。
  核查位置：§2.1–2.2；§3.1–3.3；§4.1–4.5；Appendix C.2

**2610.07757 · Acquiring and Verifying Repository Norms for Coding Agents**

[论文](https://arxiv.org/abs/2610.07757)

- **agent**：RepoNorm有明确显式规范抽取、隐式总体检查/反例修订、独立证据验证、只读规范包机制及RepoNormBench；正文审查完成，但所称官方代码/数据地址API返回404，公开执行待发布。
  复现边界：源码共性不是强制规范，必须保留required/recommended/observed。任务共享repo版本使task bootstrap可能低估不确定性；每cell一次运行；文档checker漏39误导文档变体。33.65%更多coding tokens且记录不完整。
  核查位置：§3.1–3.5 Eq1–2/Algorithm1; §4.1–4.5 Tables2–5; §5; §8

**2610.07753 · From Evidence to Action: How Tool-Using Agents Fail**

[论文](https://arxiv.org/abs/2610.07753)

- **agent**：SafeActBench 用隐藏前置条件、来源绑定Evidence Ledger和确定性轨迹计分，区分调查后不行动、单步与依赖DAG；概念符合评测方向，官方项目页本次读取失败，尚未确认公开case和evaluator。
  复现边界：656合成案例、五协议、每case配置3次；必须保留隐藏gold、返回值来源和行动前观测，不可简化成最终状态正确。内部团队参考轨迹全过不等于被测Agent成功，亦非真实业务安全认证。
  核查位置：§3.1–3.3；§4.1–4.3；§5.1–5.3；Ethics/Reproducibility

**2610.07751 · How Well Do LLMs Reason with Noisy Evidence? An Active Visual Reasoning Benchmark**

[论文](https://arxiv.org/abs/2610.07751)

- **agent**：VisualNoiseQA 将VLM作为随机视觉sensor，文本Agent询问并观察抽样回答/语义一致性；1000人工可解难例适合active reasoning评测，但明确代码数据待发表后发布。
  复现边界：初筛用11样本中gold命中1–5次，只能发生在基准构建；运行时一致性是回答间语义一致而非gold置信度，不能泄漏。5轨迹对GPT-5Mini单次不可同样解释方差；BP只是任务prompt上界非新训练算法。
  核查位置：§3.1–3.2 Eq1–3；§4.1–4.2；Limitations；release footnote

**2610.07625 · Stateless Language Agents: Scaling Long-Horizon Automated Research**

[论文](https://arxiv.org/abs/2610.07625)

- **agent**：SLA由harness重建无状态Advisor/Worker上下文，证据分组分配实验、保留局部候选、独立protected evaluator及Landlock隔离，强相关evolve核心候选；正文已审，但官方仓库当前仅assets目录，无代码/README/许可证，公开原实现暂缓。
  复现边界：ablation仍全部stateless，只改变上下文/隔离/分配，不直接证明stateless优于stateful；token匹配不含实验/评估compute成本；intra-task search反复看aggregate scores，不是heldout task泛化。不能将论文大量token或GPU实验称本地完成。
  核查位置：§3.1–3.3; §4.1–4.2 Tables1–3; §5; Appendix B.1–B.2

**2610.07588 · Personal-Agent Mediated Recommendation with Cross-Platform User History**

[论文](https://arxiv.org/abs/2610.07588)

- **agent**：PAMO以full/去cross-history rationale loglik差估支持，NDCG cutoff advantage固定正负质量、value-floor约束指数分配后GRPO；算法可作为Agent/后训练交叉候选。MediateRec明确internal approval后发布，当前固定splits/platform ranking未公开，官方复现暂缓。
  复现边界：gold target保证在50候选，非end-to-end retrieval；catalog/负采样popularity用全时段产生时间泄漏边界；support是模型相对依赖非因果正确，value-preservation仅固定rollout组不保证policy/test单调；未见多训练seed/CI；无生产AB不能纳推荐工业条目。
  核查位置：§3–5 Eq8/17–21; §6.1–6.2 Table3; Appendix A.5; introduction release footnote

**2610.07570 · Unanimously Wrong: Certified Abstention from How Medical LLM Consensus Forms**

[论文](https://arxiv.org/abs/2610.07570)

- **agent**：ProbeGuard的过程信号+反证检索重回答+分层LTT弃权机制已审，有Agent风险控制价值；官方仓库404，且标准化隔离细节未核实，已审暂缓精确复现。
  复现边界：定理要求固定逐样本评分及同分布IID；正文per-dataset z(keep)+z(RSE)未明确统计量是否在独立数据固定，需核实现，不能直接背书分布无关证书；RSE实际互相蕴含均值非熵；全MedQA覆盖约32%，不能把一致层55.3%说成全流60%；MCQ非临床效果，probe额外中位114秒/4381token；官方contents HTTP404。
  核查位置：§3.1–3.3 Eq3–6; §4.1/4.4; §5.1–5.3; Appendix D Algorithm2/E proof/J; author GitHub API

**2610.07556 · Decoupled Multi-Agent Orchestration**

[论文](https://arxiv.org/abs/2610.07556)

- **agent**：DeOrch把DAG分解/协作operation两阶段RL与worker matcher解耦，嵌套rollout分别归因，density-corrected probes+6维匿名pool特征、MMR/Thompson适配有可复现算法；官方匿名代码入口not_connected，原实现暂缓。
  复现边界：新worker要55,676 probe calls不算免费；约410k训练orchestrations/4H200，不以轻量heuristic代替。独立probe/train/test与adapt-heldout边界须保留；best-single为hindsight reference。无训练seed方差结论，匿名源码未读取成功。
  核查位置：§3.1–3.4; §4.1–4.5 Tables2–5; Appendix B.1–B.5

**2610.07553 · Which and When to Admit: Gradient Admission for Data-Centric Small Language Model Finetuning**

[论文](https://arxiv.org/abs/2610.07553)

- **foundation-model**：GRADE样本梯度对齐与EMA更新门确为新训练机制，但公开正文预算与选择协议存在未解决缺口：Appendix A成本仅anticipated并承诺未来表；U保留TBD；T一处称读取held-out最高Avg、另一处称早期validation-loss预选。需公开实测成本与选择记录，不能仅凭Meta合作署名接纳。
  核查位置：§4.1–4.2；§5.1–5.2/Table1；Appendix A；Appendix O.4；Appendix T/Table3；Appendix U

**2610.07518 · Harmful SFT Leaves a Continuous Trace in LLM Checkpoint Updates**

[论文](https://arxiv.org/abs/2610.07518)

- **post-training**：TRACE以有效SFT权重增量核与纯目标参考bank做非负拟合，sH是几何关联而非有害样本比例；4个7/8B骨干有checkpoint审计实验。匿名作者代码入口暂不可读，公共审计执行资源待确认；不是NVFP4的同名TRACE。 补充直接HTTP检查为401。

**2610.07473 · PsyCIDRA: A Dual-Agent Framework for Psychiatric Interviewing and Diagnostic Reasoning**

[论文](https://arxiv.org/abs/2610.07473)

- **agent**：PsyCIDRA用五类notepad+60expert skills/ICDlookup访谈Agent与独立transcript诊断Agent；模拟患者研究评测可有价值，但所称代码/134profile官方库当前仅README '# PsyCIDRA'，正文已审、公开执行暂缓。
  复现边界：human参考只同transcript专家共识非独立临床诊断；非population代表样本、4早期safety-stop排除。PsyCIRA3/49安全flags含2crisis，Direct2/52；不能称临床有效/安全或ready even supervised。人类对话不公开；源码/模拟profile亦尚未实际发布。
  核查位置：§4.1–4.2; §5.1–5.3; §6.1–6.2; Limitations/Ethics; official repository

**2610.07423 · 2d-fet-bench: from spatial reasoning to fet design on flakes**

[论文](https://arxiv.org/abs/2610.07423)

- **agent**：2D-FET-Bench 用真实flake轮廓和隐藏几何约束评测布局Agent，但128任务与代码明确待发表后公开，暂缓官方评测接入。
  复现边界：KLayout保存后XOR固定图层校验是独立必需项，不能只运行交互verifier；7680次结果中自动通过不等于制造可用，专家仅认可56.4–63.5%的抽样通过布局。主要ReAct-3对照为事后选择、不同模型推理模式有差异；MoSe2/WSe2只是graphene轮廓上的角色标签。
  核查位置：§3 Eq1–2；§4；§5；§7；Appendix J/L

**2610.07355 · Tracking Is Not Permanence: What Video World Models Keep of a Hidden Object**

[论文](https://arxiv.org/abs/2610.07355)

- **foundation-model**：正文已审：latent/pixel/AR二世界hidden-region距离探针与never-shown/exit控制，合成curriculum改变V-JEPA记忆；主要renderer为训练同源，IntPhys只dev且部分公开协议未复现，Appendix J明确不是全体worldmodel结论。可作诊断评测但未找到作者公开renderer/runner入口；暂缓公共评测接入，不把GT参考world作为agent可读输入。
  核查位置：§3.1–3.5；§4.4–4.6；Appendix I/J

**2610.07127 · PlaySuite: A Large-Scale Benchmark for Interactive Visual Intelligence**

[论文](https://arxiv.org/abs/2610.07127)

- **foundation-model**：复用Agent reviewer已核§3–6及App A.3：5734games/14models网络隔离worker+共享vLLM，1fps Qwen3.5-9B milestone ordinal0–4非完成比例；暂停游戏等待推理非实时，60video/6human评判一致性有限。官方README code+data coming soon，尚无可公开执行runner；PyWeek/itch许可也不能统一作开源。
  核查位置：§3–6；Appendix A.3；官方README code/data coming soon；agent-fulltext-decisions.json；README release status；agent reviewer已核查并共享
- **agent**：PlaySuite闭环键鼠/统一视频milestone评分及5734游戏具有evolve公共评测价值，但官方README明确code/data/harness/judge coming soon且API license=null，保留待发布而非按benchmark拒绝。
  复现边界：progress为序数均值不是完成比例；推理时暂停游戏，不测实时反应；PyWeek仅未修改免费分发授权，itch.io免费可访问不等于开源统一许可；公开游戏污染不可排除。
  核查位置：§3–4；§5/Table2正文；§6/Limitations；AppendixA.3；官方README

**2610.07105 · Beyond Successor Accuracy: State Retention for Recursive Self-Improvement in Recommendation**

[论文](https://arxiv.org/abs/2610.07105)

- **recommendation**：RecRSI 用 Amazon/Yelp、GRU4Rec/SASRec/FMLP 做离线保留率轨迹，34/36 成功轨迹不是线上实验。可保留为 RSI 研究线索，但不能借 RSI 标签绕开工业推荐门槛；需单独学术例外批准。

**2610.07089 · Towards a Unified Misuse Monitoring Benchmark**

[论文](https://arxiv.org/abs/2610.07089)

- **agent**：Unified Misuse Monitoring Benchmark 用固定误报预算与首次flag是否落在harm-window联合评估monitor；框架可用但官方代码仓库仍coming soon，暂缓数据集集成。
  复现边界：正文主表在evaluation选阈值，必须采用附录E.1的10% benign calibration冻结方案；单Gemma模拟全部工具输出，非真实工具执行能力。标注模型化，精确位置一致率67.5%；不能把更早阻断一律解释成安全差，时序指标依赖所定义窗口。
  核查位置：§3.1–3.4；§4.1；§5 protocol；§6/Limitations；Reproducibility

**2610.07086 · SchemaFill: Efficient LLM Tool Calling via Slot-Parallel Speculative Decoding**

[论文](https://arxiv.org/abs/2610.07086)

- **agent**：SchemaFill按公共schema/BM25预测3call slot并行draft，MAIN/SIDE隔离；side值必须在真实prefix再验证，全部结构token由target确定。解码机制符合核心候选但官方repo404，完整EAGLE头和数值一致实现未公开可取，已审暂缓。
  复现边界：4.05×是结构化response生成不是包含真实toolexecution全Agent任务；oracle skeleton仅ParallelFill诊断baseline不能给本法。贪心等价要求target logits数值/掩码/位置完全一致；stochastic用真实proposal q或pointmass与residual采样，不可用单纯argmax验证宣称distribution-preserving。论文Blackwell速度不能等同A100，未有本地执行。
  核查位置：§3.1–3.3 Eq1–2; §4.1–4.3 Algorithm1; §5.1–5.3 Table1; AppendixA/B/C.1

**2610.07004 · Topology-Consistent Task Planning over Cellular Workflow Complexes for LLM-based Agents**

[论文](https://arxiv.org/abs/2610.07004)

- **agent**：TopoPlanner将dependencygraph升为cycle-region cellular complex，queryconditioned cosheaf gate/closure retrieval再multidimensionalmessagepassing softgraph token训练planner。原TaskBench公开，但核心拓扑扩展grouped splits/构造包与代码未定位，暂缓原文评测复现。
  复现边界：merge的cyclecell不代表重复执行，loop终止仍executor负责；greedyclosure不是PCST最优。原goldtool仅NLL/外部评分；node/link F1及ACC为plan结构非真实tool success。Kmax有限不保证完整cyclebasis，固定graph motif生成query需heldouttopology审计，4H800训练缩小版不能冒充原规模。
  核查位置：§3–4；Appendix B/D/G.1/G.3/G.4

**2610.06971 · AegisFlow: A Multi-Agent Agentic AI Framework for Autonomous Remediation and Self-Healing in Fragile Data Ecosystems**

[论文](https://arxiv.org/abs/2610.06971)

- **agent**：AegisFlow 给出数据流水线 monitor/diagnose/LLM repair/shadow sandbox/hot-swap 多 agent 闭环及人工 override/rollback，正文有完整架构与实验声明。
  复现边界：审后延期：原文声明 github.com/mbilalawan/aegisflow 含数据/脚本，但本轮未确认访问及结果来源；98% on-call、300% feature velocity 不具公开可核验定义；禁止凭架构描述复述为量化线上证据。
  核查位置：PDF pp14–20,34,38–42; Shadow Sandbox; Supplementary materials

**2610.06949 · AdaLoop: Adaptive-Depth Latent Reasoning for Audio Language Models**

[论文](https://arxiv.org/abs/2610.06949)

- **foundation-model**：AdaLoop确有问题条件化多尺度循环音频connector和ACT加权输出，但§2.3 Eq6把ponder cost写为硬停止步数K，未说明对halting参数的可微余量/梯度估计；SFT只训练connector而AdaLoop第二阶段联合训练LM，能力归因需保留Fixed4控制并澄清真实训练损失。
  复现边界：论文公式所示硬K对halting概率几乎处处零梯度，与声称ponder训练机制不完整；未见官方代码补足实现。
  核查位置：§2.1–2.3 Eq1–6；§3.1–3.4 Tables1–2；§4

**2610.06923 · RadOnc-Agent: An LLM-Orchestrated Framework for AI Workflows Across the Radiotherapy Care Pathway**

[论文](https://arxiv.org/abs/2610.06923)

- **agent**：RadOnc-Agent 用26标准化函数schema接通17临床与9辅助功能，LLM选函数和参数，controller dispatch、异步影像处理及结构化结果回传。
  复现边界：2600问题×3session技术选择/schema/dispatch指标，不是临床效果；核心代码明确不公开、真实病人数据受IRB隐私限制。公开SynthRAD部分不能替代完整临床工作流。
  核查位置：§II.1–2、evaluation、Code and Data availability

**2610.06910 · GAMEGO: Training Game-Dev Agents with Synthetic Trajectories Anchored in Real-World Assets**

[论文](https://arxiv.org/abs/2610.06910)

- **agent**：GameGo 从真实game seeds经多阶段PRD/asset grounding/query compression，生成55060 sandbox轨迹做assistant-mask SFT，再用真实headless browser playtester与judge评估。
  复现边界：124bench seed先切分，training核心需真实可运行game轨迹。附录声明实现待acceptance后公开且不含GameGoData轨迹，与摘要全开放承诺不一致；等待训练数据/模型可核实。build通过不等于game行为正确，judge偏好/asset license单列。
  核查位置：§3–5、Appendix E、reproducibility statement

**2610.06861 · When Does External Guidance Help LLM Reasoning? A Bias-Variance Theory of Guidance-Augmented GRPO**

[论文](https://arxiv.org/abs/2610.06861)

- **post-training**：GA-GRPO独立混合无指导/指导rollout梯度，以σ0²/(σ0²+Rmax²δ²T)调权，正文有Qwen2.5-Math-7B九benchmark及8×A100训练。关键adaptive TV divergence估计、方差估计和IS clipping实现未在已查方法/实现段具体定义，且T兼作rollout horizon/训练步的解释有歧义；不能凭曲线把核心算法忠实实现条件记为已闭合。

**2610.06825 · PlotGround: Grounding Plot Digitization in Real Scientific Figures and Their Source Data**

[论文](https://arxiv.org/abs/2610.06825)

- **foundation-model**：PlotGround图表到源数据重建recipe与1119题人工核验基准适合评估，但正文明确pipeline和PlotGround-1k将于接收后发布，当前不能复现原任务包。
  复现边界：判分±5%及±2%相对误差需零值规则；源表是标签构造依据，纯图像评测不可泄漏。figure/table Agent是不同输入条件，不能算同信息模型提升；模型API默认推理预算不同。
  核查位置：§3.1–3.4；§4.1–4.2/4.6；Limitations

**2610.06695 · MedPrune: Topology-Efficient Multimodal Multi-Agent Communication Evolution for Medical VQA Tasks**

[论文](https://arxiv.org/abs/2610.06695)

- **foundation-model**：MedPrune医疗多agent通信拓扑优化，由agent track判定，非基础模型架构。
- **post-training**：MedPrune优化多代理通信图节点/边，主要结构搜索，不是LLM参数后训练。
- **agent**：MedPrune通过policy-gradient学习异质时空通信图，再节点weighted-degree及核范数正则边剪枝，机制相关但关键采样/训练协议不足且无作者代码链接，审完暂缓忠实实现。
  复现边界：正文one-shot节点剪枝与Algorithm1每training step剪枝不一致；row-softmax图采样概率只乘保留边，DAG采样分布未明；自然语言输出加权求和如何转prompt未明；few-shot10/20/40而测试含原train+test全量，训练示例排除未说明；validation选择/患者级隔离未报告。核范数促低秩不自动稀疏，不能声称临床鲁棒/完全抑制恶意。
  核查位置：§3 Eq2–10; §4 Tables1–2; AppendixB.1–B.3; PDFp14 Algorithm1; D.2/D.3

**2610.06597 · Can Agent Harnesses and Inference Engines Hear Each Other? The HEAR Protocol for Agentic LLM Serving**

[论文](https://arxiv.org/abs/2610.06597)

- **agent**：HEAR双向harness-engine协议区分intent/control、偏好/要求、观察/保证及接受/完成；cache+等待保护与角色配置实例有可接入执行优化价值，但作者匿名repo not_connected，完整补丁/manifest不可取，已审暂缓。
  复现边界：非劣证明不足，DRB只89共同有效配对不可替代全部100分母；Mooncake100%负载session+cache+guard吞吐反降至.89×，组合非单调；cache近似配置不保持数值模型语义完全相同。Judge在不同GPU运行；调参/离线profiling不计运行总时长；公开匿名API返回not_connected。
  核查位置：§3.1–3.4; §4.1–4.4 Tables3–5; AppendixA.1/A.3–4; B Table17/JudgeProvenance

**2610.06576 · Before Agent Tells The Lie: Has Deception Already Been Represented?**

[论文](https://arxiv.org/abs/2610.06576)

- **agent**：深核MMD白盒前缀探针与类型平衡CAA诚实方向干预有Agent监控诊断价值；全文已审，但官方匿名代码not_connected且关键训练/部署选择不足，已审暂缓。
  复现边界：decisive-step事后对齐不是可在线知道的时点，prefix幸存者/任务长度变化可混杂；无taskgrouped分割/验证集规模、正则项完整定义；alpha2按最佳结果选但未说明validation。labels是行为非内在意图；7/500无效不能丢，诚实保持72.9%说明干预代价；未核公共资源。
  核查位置：§3.1–3.4 Eq3–9; §4.1–4.4 Table1/Figs3–4; §5; Reproducibility

**2610.06563 · HERA: Harness-Environment Co-Evolution for Reliable Agentic Abstention**

[论文](https://arxiv.org/abs/2610.06563)

- **agent**：HERA构建同任务feasible/infeasible环境对，失败驱动环境及harness共同进化，独立15pair validation上Abstain/Pair非退化选型；高相关evolve候选。公开base/final harness与runner已有，但README明确120实例数据私有需授权，完整评测暂缓。
  复现边界：infeasible通过替代路径/逆mutation/语义审查认证非形式证明；pair衍生需group split，task-disjoint不等于environment/domain-disjoint。validation单rollout/15pairs，未证明可靠长期泛化；未核到公开完整co-evolution训练管线。
  核查位置：§3.1–3.2; §4; §5 Table1; Appendix B.3/B.4/C.1; official README

**2610.06514 · ANT: A Multi-Granularity Network Traffic Dataset and Benchmark for Agents Behavior Auditing**

[论文](https://arxiv.org/abs/2610.06514)

- **agent**：ANT 是网络侧Agent行为/隐私审计数据集，可作为辅助观测评测；匿名公开入口读取失败，尚未核实104GB数据与执行包，暂缓接入。
  复现边界：3114episode/47primitive；按episode切分、屏蔽IP，不能把同轨迹segment散入训练测试。209测试episode仅20恶意，拒绝轨迹排除会改变分布。只允许授权隔离实验，不捕获真实用户流量；这是流量分类而非Agent任务能力提升。
  核查位置：§3.1；§4.1；§5；Ethics/Reproducibility

**2610.06411 · From Benchmark to Bench: Can Agents Survive Real-World Drug Discovery?**

[论文](https://arxiv.org/abs/2610.06411)

- **agent**：MAGI由MCP编排REINVENT/ADMET/结构预测，五轮版本化目标修订与候选保留；实用研究控制机制，但完整九项目含未披露AstraZeneca和受限项目scorer。
  复现边界：终点是预测不是新湿实验；一backend一trajectory、无静态目标对照，无法隔离agent贡献。Sanofi时间截断不能排除预训练暴露，不应在本库伪造私有评分数据。仅公开子集可另立后续边界。
  核查位置：§3.1–3.2；§4 protocol；§6–7；supplement code DOI

**2610.06401 · RAISED: Self-Distillation for Robustness to Prompt Injection in LLM Agents**

[论文](https://arxiv.org/abs/2610.06401)

- **agent**：RAISED自生成真实可执行工具链，独立clean教师分布监督clean/注入学生同response tokens，保留top256+残余桶forwardKL；防御训练机制符合候选，但官方仓库404，完整数据/脚本受阻已审暂缓。
  复现边界：离线固定clean teacher轨迹而非on-policy rollout distillation；只能抗静态注入，AppF自适应攻击reward为零的失败优化明确不算鲁棒证据；成功check由同model生成且筛选，自蒸馏可能保留原错误行为；soft桶是coarsenedKL不是fullvocab精确KL；算教师生成/15GB分布存储成本，不能用hardSFT冒充。
  核查位置：§3 threat; §5.1–5.2 Eq3–4; §6; AppendixC.5.1/E Table14/F/G; official GitHubAPI

**2610.06204 · Do Small Language Models Learn to Negotiate? A Controlled Scaling Study of RL-Trained Sellers**

[论文](https://arxiv.org/abs/2610.06204)

- **foundation-model**：小模型谈判GRPO学习率/规模比较，领域后训练经验研究。
- **post-training**：独立双边谈判ledger环境：私有Dirichlet效用、JSON counter/accept、12轮封顶与held-out买家/领域，具公共评测潜力。正文给协议但未找到作者环境/场景生成器发布链接；跨size有架构/计算混淆，不能据此结论能力scale。
- **agent**：Gemma谈判RL受控规模/学习率研究，未提出新的Agent核心训练方法。
  核查位置：Title and complete abstract

**2610.06190 · Bridging the Evidence-to-Execution Gap:A Reflective Agent for Multi-Objective Peptide Design**

[论文](https://arxiv.org/abs/2610.06190)

- **agent**：EASER把离线学习固定低秩蛋白属性控制接口与证据Agent的probe再分配采样结合，可迁移的多目标搜索控制机制；作者明确代码/矩阵/划分将发布，已审暂缓原实验复现。
  复现边界：所有活性/安全/CPP效果只是预测器分数，无湿实验或临床证据；搜索受内部predictor偏差，不能用安全分数断言安全；equal候选不等LLM/检索总预算；候选/矩阵/curated evidence resource尚未发布，不能简化为标量随机搜索冒充定义算法。
  核查位置：§3.1–3.3 Eq1–2; §4; §5.2 Table3/§5.3–5.4; AppendixB/C.1 Algorithm1/G

**2610.06163 · Where Did the Repair First Go Wrong? Localizing the Origins of Silent Failures in Agentic Vulnerability Repair**

[论文](https://arxiv.org/abs/2610.06163)

- **agent**：SAGE 用prefix-only安全推理量表和逐次代码快照定位已确认silent failure的最早可观察偏离，适合作为轨迹诊断；官方Zenodo数据入口本次读取失败，完整normalizer/judge脚本未核实，暂缓。
  复现边界：5400尝试只3684有效进入验证，95确认案例来自19任务；失败锚点仅供事后定位，不得喂给被测Agent或逐步评分judge。重复judge一致不等于正确或因果归因，人工标注仅覆盖代码来源/引入写入。SecurityEval无测试套件，L1仅语法/导入/结构不足以保证功能。
  核查位置：§3.2–3.4；§4.3；§5.1–5.2；Data Availability

**2610.06122 · Benchmarking Jailbreak Guardrails for Embodied Agents**

[论文](https://arxiv.org/abs/2610.06122)

- **agent**：固定具身Agent后端对比感知/计划/控制阶段guardrail，联合测bypass、模拟器hazard、正常任务完成与成本；匿名补充材料未给可验证公开入口，保留已审暂缓。
  复现边界：仅AI2-THOR的300安全/300不安全任务，部分结果依赖GPT4o比较reference plan而非环境真值；不是实机安全认证。只可隔离模拟器防御评测，不能连接物理机器人执行有害指令。不同guardrail的误拦截与延迟必须同时报告，不按单一bypass排名。
  核查位置：§3 taxonomy/metrics；§4.1–4.3；§6；Reproducibility/Ethics

**2610.06056 · ROT: Rotating Hidden States towards Contextual Vectors for Hallucination Mitigation in LVLMs**

[论文](https://arxiv.org/abs/2610.06056)

- **foundation-model**：ROT核心旋转/平滑与实验已核，但保真配置仍缺trigger τ和模型specific layer zone；正文LLaVA6–26与AppendixAlgorithm1从1到Lmid不一致，无法确认作者路径，保留具体待补项。
  复现边界：附录给α/β/γ未给τ；从3000CHAIR选layer且未交代独立验证划分，不能在test调阈。MME只三perception子集非全任务，POPE也不超过全部baselines；缓存previouslayer preFFN与正文hk−1语义须确定。官方正文无源码链接，搜索未找到作者公开源码，不以抽象heuristic替代。
  核查位置：§3.1–3.2 Eq1；§4.1–4.2 Eq2–6；§5 Tables1–3；App A Algorithm1/C/D

**2610.05982 · Breaking the Tie: A Cluster-Aware Routing Framework for Large Language Models**

[论文](https://arxiv.org/abs/2610.05982)

- **foundation-model**：CASLR对查询聚类，用簇内专家正确数构造masked软标签训练BERT router；算法清晰，但独立训练/校准/测试切分和标签统计范围未交代完整，先暂缓能力对比。
  复现边界：正确性只能用于训练集标注，不能用待测集构造簇级utility；正文未找到具体split/seed或作者代码。1.13秒router成本应如实计入，不称几乎零开销；新专家加入需重新统计而非直接泛化。
  核查位置：§4 Eq4–9；§5.2–5.3；§5 routing cost；Appendix A

**2610.05586 · AgentDoxx: Agentic Re-identification of Anonymized Text with Web Search**

[论文](https://arxiv.org/abs/2610.05586)

- **agent**：AgentDoxx对Agent去标识文本再识别风险做评测，但822合成访谈仍基于真实身份，作者明确不发布文本/gold，受控托管评测仅筹备中；暂缓接入。
  复现边界：仅保留防御性隐私审计启示：联合测输出/检索泄露与匿名化效用。不得重建真实身份关联、抓取私人访谈或发布识别结果。真实1250访谈无身份gold，43匹配不能作准确率；样本只含主动公开身份者，不代表总体风险。纯虚构身份离线canary可以研究，但不得冒充官方AgentDoxx复现。
  核查位置：§3.1–3.2；§4.1；§5/Limitations；Ethics/Data and release policy

**2610.05559 · Cut Binary Cross Entropy: Efficient Large-Vocabulary Loss and Gradient Kernels for Sequential Recommendation**

[论文](https://arxiv.org/abs/2610.05559)

- **recommendation**：Google CutBCE 公开 JAX/Pallas TPU kernel，在 Yambda50M/SASRec 上测显存与速度；不是线上 A/B。TPU v5e/v6e 定义算子尚无本项目可验证环境，不能将普通 CUDA BCE 冒充复现，也不转基础模型以规避门槛。
- **foundation-model**：已审明确TPU JAX/Pallas exactBCE基础设施，可保留研究候选；没有工业AB、不是LLM实验，当前NVIDIA复现路径不能代替原TPU内核，需TPU环境与单独接入范围批准。
  复现边界：65.7%HBM与225.9%速度是TPUv6e，NVIDIA未验证；不能重命名foundation绕工业AB门槛。
  核查位置：§III-A Eq1–2；§IV-B/TableIII；§V

**2610.05399 · Adaptive Code Revision Attacks on AI Pull Request Reviewers**

[论文](https://arxiv.org/abs/2610.05399)

- **agent**：AFCRA以reviewer反馈改代码并保留同CVE property，fresh evaluator执行PoC且在historicalfix阻断才认exploitable，159 runnable PR可作安全评测。正文仅提replication package未给可定位公开包，暂缓等待任务及容器/PoC发布。
  复现边界：attacker可获目标PoC属显式威胁模型；reviewer无gold/referencefix外查。Upper-bound有额外target信息只oracle诊断；33先前成功attack上的防御/false-reject结果非全量安全保证，历史CVE污染不可消除。
  核查位置：§3–4；§5 RQ1–4；Threats to Validity

**2610.05387 · GNN-CB: A Graph Neural Network Competition Benchmark for Human and LLM Evaluation**

[论文](https://arxiv.org/abs/2610.05387)

- **agent**：GNN-CB用18个图学习竞赛和隐藏test评分检验plan→code→执行修复，可作为CPU coding/evolve基准；论文只承诺将发布MIT基础设施，未定位可用官方评分包，暂缓接入。
  复现边界：API每调用10k输出而agent是native session预算，不完全等算力；单次greedy、人类LLM辅助无法完全审计；不同指标不可简单均值排名。必须拿到官方split/scorer，不能重新编造同名任务。
  核查位置：§3.1–3.3；§5/Limitations；Data and Code Availability

**2610.05380 · VHDL-REPOBENCH: A Repository-Level Benchmark for Evaluating Large Language Models on VHDL Design Generation**

[论文](https://arxiv.org/abs/2610.05380)

- **foundation-model**：VHDL-RepoBench保留跨文件依赖，四类补全/摘要/模块生成任务与GHDL、VUnit/Cocotb验证；暂未在正文定位官方完整任务包/构建依赖发布。
  复现边界：大部分Pass@k实际仅编译成功，只有135个SMG模块子集要求testbench；不能将所有分数称功能正确率。约100仓库公开代码污染和测试隔离未明确；摘要ROUGE/偏好不等于仿真正确。
  核查位置：§III-A–C；§IV metrics；§V

**2610.05319 · Understanding the Hierarchical Structure and Functional Landscape of the Model Context Protocol Ecosystem**

[论文](https://arxiv.org/abs/2610.05319)

- **agent**：MCPacific静态提取百万tools，node级LLM设计/独立pilot修订taxonomy再embedding routing+人审，提供same-enabled-tool hierarchical retrieval对照，适合tool discovery基础设施。但作者仅承诺release且未定位完整corpus/taxonomy/runner，暂缓。
  复现边界：功能可比不保证schema或行为等价；Semgrep alert非confirmed漏洞。静态pattern漏dynamictool；GPT5.4兼被测与judge，claim coverage不是执行任务成功，工具来源仅公开七语言。
  核查位置：§3.1–3.3 Algorithm1；§4 RQ4；Threats to Validity/Ethics

**2610.05241 · StateWise: Diagnosing and Repairing Persistent Operational State Before Agent Actions**

[论文](https://arxiv.org/abs/2610.05241)

- **agent**：StateWise固定其他context逐record反事实replan归因，read-only环境验证/开发者intent澄清+typed evidence binding纠正scoped持久记录，再独立state-action执行检查。方法清楚，但仅声明artifact repository，缓存正文无可定位URL；待公开150 executable cases/manifest/audit/source包后进入复现。
  复现边界：40dev与150test分离，跨模型独立20case；150为设计/既有研究启发coding cases，不是自然故障发生率。93.3%及零unsafe仅有限case结果，不能视安全保证；手写verifier/state接口需保留，gold只外部outcome judge，普通permissions仍独立生效。
  核查位置：§3–5；§6；Data Availability

**2610.05223 · Look Before You Leap: Thermodynamic Arbitration of Parametric and Non-Parametric Knowledge in LLM Agents via Self-Regulating Memory Architectures**

[论文](https://arxiv.org/abs/2610.05223)

- **foundation-model**：MARTA agent检索记忆框架，由agent track审查。
- **agent**：MARTA以冻结LLM entropy/margin/hidden variance投影到BiGRU memory-header affordance，用Sparsemax含bypass gate，CEA硬负NCE只训练controller。核心可执行但自建procedural/semantic/episodic多模态suite、正负utility标签、checkpoint/split与代码未定位，暂缓待完整资源。
  复现边界：gold-document acceptance只是oracle retrieval诊断，非answer质量；SQuAD unanswerable判定不等于一般epistemic awareness。12ms/3.7x取决于L4及450ms检索配置，熵下降不保证真值；多backbone不证明universal invariant，必须真实logit/hidden及heldout标定。
  核查位置：§3–4；Appendix A Algorithm1/2；B profiling

**2610.05219 · Safe Context Switching for Agents in the Wild: Mitigating Subspace Interference via Orthogonal Adaptation**

[论文](https://arxiv.org/abs/2610.05219)

- **agent**：AURA顺序冻结旧LoRA，以B子空间projection/Frobenius惩罚分离新adapter，Chain-of-Pollution测试保留KV。正文代码/data loader仅upon acceptance发布；链式配对数据与cache/activation协议未公开明确，暂缓。
  复现边界：正交soft penalty非hard安全保证，不支持无限扩展；TruthfulQA不是adversarial safety benchmark，logit cosine及KL非安全行为指标。rank64、λ.5需validation独立选择，论文忽略统计不确定性；共享cache跨adapter的真实一致性须执行验证，不能模拟正交矩阵冒充。
  核查位置：§3–5；Appendix A/C/D

**2610.05119 · LexiHorizon: Stabilizing Reinforcement Learning for Long-Horizon Deep Search**

[论文](https://arxiv.org/abs/2610.05119)

- **agent**：LexiHorizon以128K context、完整reason/action trace但旧toolobservations换marker，非零answer reward门控30call饱和effort bonus，GSPO G16 live webrollout；aux reset丢弃片段仍计成本。训练数据与live backend/代码checkpoint未定位，等待可重放public契约。
  复现边界：8轨迹平均accuracy非pass@8或8train seeds；policytokens不含tooltokens。99.88valid answer非correct；金答案只外部judge。samebenchmark sweep/90%上下文压缩需validation隔离，live web变化无法以cachedfixture当原算法真实训练；9B128K GPU预算需真验证。
  核查位置：§3.2–3.3；§4；Appendix A.2–A.3

**2610.05103 · VulValidate: Auditing Function-Level Vulnerability Labels with Executable Evidence**

[论文](https://arxiv.org/abs/2610.05103)

- **agent**：VulValidate对漏洞函数标签建立历史源码绑定、脆弱/修复版本同条件动态证据、函数级归因和cold replay，方法可用于防御评测审计，但完整官方镜像/索引未定位，暂缓直接接入。
  复现边界：必须隔离历史脆弱程序，只在授权本地fixture执行；构建成功不代表源码保真，崩溃不自动证明被标函数漏洞，触发失败不等于安全。35,849审计实例含未解决项和人工裁决，不能以合成返回值替代真实包。
  核查位置：§2.1–2.5；§3.1/3.5；§5 threats

**2610.05037 · SparseCraft: Agentic Hardware-Software Co-Optimization for Sparse Computing**

[论文](https://arxiv.org/abs/2610.05037)

- **agent**：SparseCraft用LLM受限MCP变异Gemmini Chisel RTL/memory/schedule，经hash immutable harness、legality/elaboration/Verilator bitwise gold/synthesis/Pareto admission与bounded repair形成15轮闭环。source-code仅标链接名，完整bundle未定位，且需Chipyard/EDA验证边界，暂缓。
  复现边界：单512×512GraphChallenge INT8 workload、一个328min run，无heldoutworkloadgeneralization或searchseedvariance。5.61 perf/W与11.8EDP含counter-based energy/SRAM面积模型非硅实测，2ns固定clock；gold在外部检查不能LLM写改，必须真实EDA gate不可用伪性能替代。
  核查位置：§II–IV Algorithm1；Gate ladder；Workload

**2610.04973 · TrajLong: Co-Designing Agentic and Long-Context Supervision for Mid-Training**

[论文](https://arxiv.org/abs/2610.04973)

- **agent**：TrajLong把agenttrajectory清洗重排成Retrieval/MultidocQA/StateTracking，context+multipleQA全tokenCPT，10Bcompiled与30Bbackground固定mixture，之后统一SFT。未定位完整compiled/contextsource及background数据/checkpoint，暂缓原方法规模复现，编译器可另作小规模研究。
  复现边界：256K40BtokenCPT须保持原loss/背景mix契约，玩具QA不等于原复现；sourcelevel去benchmark污染，任一derivedQA命中全源移除。ρ1仅四settings相关非因果；Avg@3/BoN@3要分开且不是trainingseed，finaltest不用于挑checkpoint。
  核查位置：§3–4；Appendix A.2/A.3/C/D.1

**2610.04914 · Monitorability Disposition in Large Reasoning Models**

[论文](https://arxiv.org/abs/2610.04914)

- **post-training**：monitorability disposition是独立自报告/关闭监控工具协议：两channel topology×四directive、三类150条既有任务与外部judge。附录有prompt，但未找到作者可执行runner/结果数据公开入口；需要公共执行资源核实，不因无新loss拒绝。

**2610.04888 · No Hindsight for LLM Fact-Checkers: Measuring Leakage Channels in Misinformation Detection**

[论文](https://arxiv.org/abs/2610.04888)

- **post-training**：point-in-time fact-checking分离检索未来证据和参数结果泄漏，有日期trust-tier、时间split、冻结LLM瓶颈/MI head；正文明确date cache、split、K文本与code将在camera-ready发布。当前不能确认公共重现入口；K含label信息与未知日期丢弃是已知限制。

**2610.04777 · ARISE: Adaptive Agentic Reasoning with Image-grounded Self-Evaluation for Interpretable IBD Assessment**

[论文](https://arxiv.org/abs/2610.04777)

- **foundation-model**：ARISE炎症性肠病诊断agent，专用医疗工作流。
- **agent**：ARISE 从训练图像标签和专家视觉词汇构造可检查临床假设，validation 精炼后转 FOL/Z3 修复冲突；已读定义算法及 CrohnIPI/C-TRUS 评测。
  复现边界：审后延期：专家 finding annotations 与13患者切分、全提示/实现发布尚未核验；临床 satisfiable 不等于医学正确；不得在诊断测试阶段向 agent 提供病变标签。
  核查位置：ARISE state/refinement/Z3; normalized p13–22,30–32

**2610.04740 · Toward a Locally Deployable Agentic Co-Scientist: Small-Model Planning for Early-Stage Drug Discovery**

[论文](https://arxiv.org/abs/2610.04740)

- **agent**：小模型 Co-Scientist 以 UMS 分块状态和18科学工具构造依赖合法计划，用路径先行的1263 query-plan 对 LoRA，再由 rule evaluator 反馈重规划。
  复现边界：审后延期：自建 query-plan 数据与内部工具/外部服务完整可执行链未公开核验；query-level split 不是 workflow-type 隔离；schema-valid-only 分母指标不能当端到端科学成功率。
  核查位置：System/UMS/Planner; normalized p11–20,103,130–131; Appendix A/B

**2610.04716 · Towards Automatically Pruning Logging Code with Coding Agents: How Far Are We?**

[论文](https://arxiv.org/abs/2610.04716)

- **agent**：LogRem从真实合入的Python/Java日志删除历史，经静态识别和人工核验构造387任务；给agent改前源文件和不暴露目标行的描述，比较日志删除集合、无关代码保留及完整轨迹。可选历史讨论与10类模式/11类原因提示用于上下文消融。
  复现边界：可解析输出不等于功能正确；RWCA仅对齐历史开发者补丁，不是唯一正确解。最终输出validity95.6–100%但RWCA11.1–19.6%。历史commit/discussion可能含未来意图，应与无历史条件分开并防补丁泄漏；同一任务不得供evolve选参。正文未定位LogRem387标注/原始执行轨迹公开下载，暂缓精确benchmark复现，不能用自造日志case冒充。
  核查位置：§3–5 pp.3–6、Tables4–11 pp.8–11、§8 p.12

**2610.04672 · MASBench: Benchmarking LLM-based Multi-Agent Collaboration under Partial Observability**

[论文](https://arxiv.org/abs/2610.04672)

- **agent**：MASBench将Hotpot证据、日程约束和资源地图拆给部分可观察的不同Agent，检验记忆/协议/路由组合；官方数据和执行包尚未验证，暂缓同名benchmark接入。
  复现边界：通信成本只统计跨Agent消息不含本地推理；信息隔离必须在运行时保持，不能把联合gold或完整约束交给每个Agent。不同任务归一分数与每千token效率应分报。
  核查位置：§3.1–3.2；§4.1–4.3；§5.1

**2610.04504 · The Same Zero: Why Identical ASR Can Imply Different Guarantees in LLM-Agent Security**

[论文](https://arxiv.org/abs/2610.04504)

- **agent**：The Same Zero 提供 VAL 保证来源分类、攻击升级下的 zero-stability 与 agent 真实效应评测；正文有 AgentDojo 全 banking 比较及失败机制。
  复现边界：审后延期：主要测试床与 action级原始 receipts 发布未核验；banking per-task traces 丢失、shipped gate已修字段不能复刻旧统计；同0 ASR不能宣称同安全，25%utility崩溃要明确。
  核查位置：§6.1/6.5; Appendix A.4/A.6; normalized p11,53–54,93

**2610.04441 · LocusRL: Diagnosing LLM Reward and Policy Interventions in Competitive Games**

[论文](https://arxiv.org/abs/2610.04441)

- **post-training**：LocusRL的学习者/奖励/执行/证据5层审计与terminal replay certificate可作诊断入口，单次修复仅证明该state充分修正，20证书不是20独立局面。作者LocusRL-Pub链接两次不可读，待公开代码核实。 补充直接HTTP检查返回404。

**2610.04378 · COPEX: Benchmarking LLM Robustness to Adversarial Context Across Model Context Protocol Layers**

[论文](https://arxiv.org/abs/2610.04378)

- **agent**：COPEX固定MCP stack隔离25类攻击在Agent/client/server/transport的入口，含125场景和独立oracle；完整官方场景包尚未定位，暂缓正式benchmark接入。
  复现边界：response扫描发生在调用之后不能撤销副作用；schema仅注册扫描，失败fail-open；15类LLMjudge非客观ground truth，防御每变体一run。仅授权隔离的虚构canary/本地测试，ASR不代表现实可利用率。
  核查位置：§3 observation boundary；§4.1–4.3；§5.1；§6 limitations

**2610.04302 · From Valid to Useful: Post-Verification Acquisition for Recursive Self-Improving Recommendation**

[论文](https://arxiv.org/abs/2610.04302)

- **recommendation**：DA-RSIR 对验证后策略用 MC dropout 与分歧分桶获取数据，四数据集三模型离线对比；§7 明确在线评估未做。保留 RSI 线索，工业推荐实现需例外批准。

**2610.04255 · Grounded in Time: A Multi-Source Dataset and Benchmark for Temporal Grounding in Robotic Manipulation**

[论文](https://arxiv.org/abs/2610.04255)

- **foundation-model**：Grounded-in-Time用前episode视频与反事实A/B场景定义历史语义操作，ManiSkill3与真机双源评测；未定位官方数据/环境任务包，无法忠实重放。
  复现边界：基线π0.5无前历史输入，低SR并不直接证明记忆结构劣；模拟每task60次，真机10次，pair只逐例分数。未来接入须真正环境执行并报告SR与阶段PSR，不能用历史答案标签生成动作。
  核查位置：§III-A–D；§IV-A/C/D；TableV

**2610.04246 · Benchmarking Psychological Dynamics in Generative Agents**

[论文](https://arxiv.org/abs/2610.04246)

- **agent**：PsyDyBench将300合成人格六天同一事件叙事交给不同模型，比较个体内外方差、关联与人类规范，适合作为persona诊断；官方仓库读取失败，暂缓正式基准接入。
  复现边界：仅6天AR估计有短panel偏差、四指标单因子未识别而改特征谱；共享LLM叙事不是实际人类纵向数据。方向一致不表示定量心理保真，不能用于现实个人心理诊断/预测。
  核查位置：§3.1–3.3；§4；§6/reproducibility

**2610.04156 · Trajectory-Derived Confidence for Reliable, Resource-Aware Clinical Text-to-SQL Agents**

[论文](https://arxiv.org/abs/2610.04156)

- **agent**：Sentinel 两 ModernBERT heads 从问题及轨迹前缀预测 answerability/correctness；calibration 定退出门、isotonic map 和 early-stop，交付时用 Chow λ/(1+λ) 拒答规则。
  复现边界：EHRSQL/MIMIC-III需受控数据访问，原始训练轨迹/heads仓库未定位。按模板切6179/2160/2101，官方test未碰；26%困难case judge分歧、单训练seed、heads每agent重训；接近满分answerability部分来自短模板。等待可用数据/轨迹，不用虚构SQL奖励。
  核查位置：§3.1–3.4、§4.1、Limitations、Appendix I

**2610.03935 · General Decision Models: Benchmarking and Insights Beyond Jev**

[论文](https://arxiv.org/abs/2610.03935)

- **foundation-model**：InnerJev的Reasoning-to-Readout Self-Distillation是实际新算法而非仅JEVal benchmark；已核两条自推理软目标、冻结输出层、一epoch训练与独立dev选checkpoint。但主对比混合不同规模/训练来源，未确认同训练预算替代蒸馏损失基线，需补资格证据而非按benchmark直接丢弃。
  核查位置：§4.1；§6.1–6.3；Appendix F.2/Table42；Appendix F.3；Appendix F.4/Table43

**2610.03902 · When Evidence Changes: Evaluating Memory Repair and Re-reading in Language-Model Agents**

[论文](https://arxiv.org/abs/2610.03902)

- **agent**：Versioned dependency memory以snapshot/readset事务commit处理撤销和替换；比较re-read/cache/rebuild/local repair/quarantine/no-propagation，源允许表约束回答。
  复现边界：eICU demo公开，但冻结scenario/原始轨迹/代码均明确未公开、接受后释放。样本3–20patient/cell，posthoc词法scorer、同患者reuse、部分预注册遗漏；不是repair因果差。Gold support只评分，source-filtered重读是重要信息匹配对照。
  核查位置：§3–5、§6.2–6.5、§8、Appendix A/B

**2610.03525 · Structured Composition of Verifiable Atomic Insights for Table-to-Report Generation**

[论文](https://arxiv.org/abs/2610.03525)

- **agent**：ComInsight SQL grammar枚举atomic insights，校准统计filter及SFT+DPO interestingness judge，typed关系graph/Leiden社区与causal paths合成有SQL provenance报告。
  复现边界：轻量judge依赖1200标注/600偏好对，原始训练包或checkpoint未定位；不能用通用judge/手写分数声称核心复现。Granger+LLM mechanism仅causal hypothesis非干预因果。290calibration/train实例应从bench test去重，top50与阈值validation冻结。
  核查位置：§IV.A–D、§V、Appendix B

**2610.03476 · MobiAgent: Dual-Loop Recursive Policy Self-Improvement for Long-Horizon Mobile Manipulation**

[论文](https://arxiv.org/abs/2610.03476)

- **agent**：MobiAgent 内环VLM receding-horizon planner+shared VLM/skill-specific flow experts+visualcritic重试/重规划；外环分段verify、skill clustering与真实rollout finetune。
  复现边界：BEHAVIOR-1K/RoboCasa仿真及Astribot硬件、π0.5完整action专家训练不可用文本fixture替代。代码URL存在但政策权重/curated startup数据尚未在正文定位；暂待确认可运行仿真资产。真实动作能力必须实测，不算普通Agent路线图改写即接入。
  核查位置：§3.1–3.2、§4、Appendix prompt/case studies

**2610.03421 · CLIMB: Confidence-Guided Complementary Evidence for Multimodal Retrieval-Augmented Generation**

[论文](https://arxiv.org/abs/2610.03421)

- **foundation-model**：CLIMB固定MMR证据池、R/E/C critic、至多3轮pool内重排且置信严格增加才接受；方法有价值，但视觉critic与正文指定text-only Llama3.1-8B的具体接口未交代且无作者实现可核。
  复现边界：置信是相对自评分而非校准正确概率；须单独计critic/facet多次调用预算，不能拿多轮对单次检索直接声称效率。InfoSeek validation作为报告集须另划开发集，冻结split；明确视觉接口后再实现。
  核查位置：§3.2–3.4 Eq1–4；§4 implementation；Limitations；Appendix prompts

**2610.03356 · ReFract: Benchmarking Perspective Awareness in Language Model Agents with Text World Models**

[论文](https://arxiv.org/abs/2610.03356)

- **agent**：ReFract 用专家domain Pred/Cap/Know及consume/produce关系构造工业maintenance text worlds；区分authority与knowledge，QTS/FTS测试perspective-aware action可执行性。
  复现边界：150条expert transcript task与domain/goal完整公开包未定位；不能把手写通关路径伪装为原benchmark。Gold goal仅judge，工具data dependency/role gate每步检查。小样本五工业角色非general agent，也非真实工业效益。
  核查位置：§3.1–3.3、§4–5、Appendix A/F

**2610.03324 · To Jev or Not? Evaluating the Accuracy and Efficiency of Structured Decision Models for Hate-Speech Moderation**

[论文](https://arxiv.org/abs/2610.03324)

- **foundation-model**：HateDecide不是新JEV训练算法，但其定义依从、去重分组与阈值校准控制可作为决策评测基础设施；正文列出完整prompt/数据协议，未找到官方公开可执行代码或冻结评测artifact，基础设施接入资格待公开材料核实。
  复现边界：评测四个已有英文数据集且预训练曝光未知；必须保留Dynamic跨split扰动分组去重，阈值只在200validation题选择，不得使用测试gold供模型读取。
  核查位置：§3.1–3.4；§5；Appendix prompts；Appendix threshold-tuned control/Table11

**2610.03252 · COSMI: COmpositional Synthesis of Multi-object Interactions**

[论文](https://arxiv.org/abs/2610.03252)

- **foundation-model**：COSMI 将带接触的单物体人体动作组合、镜像和几何筛选，训练共享物体槽的文本条件扩散模型，按未见物体和五种未见组合评测。定义算法可读，但特定组合数据与模型仅承诺发布。
  复现边界：审后延期：222k 组合序列、发布流水线与检查点尚未核验公开；不能用随意拼接或 toy 动作替代官方接触筛选与组合隔离；源人体数据受许可限制。
  核查位置：§3–5; Appendix C/D

**2610.03195 · Source Preference in the Wild: How LLM Agents Favor Items by Source, and How to Reduce It**

[论文](https://arxiv.org/abs/2610.03195)

- **post-training**：请求满足度匹配+循环Latin-square位置控制+BT-Davidson source preference形成独立Agent诊断协议；URL显隐/置换实验。正文Reproducibility明确code/dataset待publication发布，当前不视为公共执行入口，转Agent待跟进。
- **agent**：搜索来源偏好因果操作与prompt干预经验研究，非独立新算法。
  核查位置：Title and complete abstract

**2610.03153 · EvoRiskBench: An Evolving Benchmark for Runtime Security Risks in Workspace Agents**

[论文](https://arxiv.org/abs/2610.03153)

- **agent**：EvoRiskBench 9entry×5effect的执行case构建/refinement，sandbox agent与外部系统event/state共同佐证技术risk，冻结450case跨9model-harness。
  复现边界：cases/platform明确要artifact safety后才释放；当前无法复现完整450。合成business/mockcredentials仅sandbox，ASR与TSR并列；judge严重度≠真实系统危害，不拿trace文字代替side-effect证据。
  核查位置：§3.1–3.3、§4、§5、artifact statement

**2610.03135 · Page-EntroKV: Hardware-Aligned, Entropy-Weighted KV-Cache Eviction under Grouped-Query Attention**

[论文](https://arxiv.org/abs/2610.03135)

- **foundation-model**：Page-EntroKV用去sink的Renyi-2熵加权GQA组内注意力，再按物理页分配预算，机制可辨认，但公开证据与正文关键系统结论不一致，暂不列成熟实现候选。
  复现边界：官方仓库称结构N180全部jaccard0/UOR1，不支持4.75倍bloat；sink只有layer0十头；NIAH只有958/1474/1990长度；LongBench仅4完成、11空行且无dense基线；无8/32/64页大小扫描和serving表。需对齐论文版本与原始证据后再评估，不把缓存mask诊断当端到端收益。
  核查位置：§4.1–4.2；§7–8；official README evidence scope

**2610.03056 · MOF-VERIFY: A Failure-Aware Agentic Harness for MOF Hypothesis Verification**

[论文](https://arxiv.org/abs/2610.03056)

- **agent**：MOF-Verify identity/CIF digest grounded lookup、verified local DOI全文抽取、evidence sufficiency与deterministic verdict routing；需计算时真实SevenNet执行含精度/seed/convergence。
  复现边界：公开benchmark存在，但trusted实验CIF/CSD可能许可限制、expert-local全文与curated alias corpus尚未定位完整释放；T4不能用返回固定property替代MLIP。oracle证据是上界非检索能力，Yes/Re-run/Human-review与文学Yes/No/Uncertain分开。
  核查位置：§3、§4.1–4.2、Appendix A.5

**2610.03055 · hacktrace: behavior-supervised detection of reward hacking during code generation**

[论文](https://arxiv.org/abs/2610.03055)

- **agent**：HackTrace 按problem-disjoint act/outcome labels监督generation residual读数，problem-group CV选88linear readouts与layers18/24 top8 MultiMax，结合final AST特征；GRPO penalty抑制shortcut。
  复现边界：公开URL是https://github.com/XXXX/HackTrace占位，heads/activation/GRPOlabels声明后续加，不能视已可用。隐藏oracle只评价；partialprefix预测completedlabel不是当前已发生危害。可编辑test阳性98.2%修改test，强penalty与honest-correct/成本同报。
  核查位置：§3.1–3.4、§4.4、§5、release statement

**2610.03025 · Verifiable, Articulable, and Tacit Components of Preference**

[论文](https://arxiv.org/abs/2610.03025)

- **recommendation**：VAT/Creative Preferences 关注后训练偏好算法，已转后训练审查，不在工业推荐轨作无线上拒绝。
- **post-training**：已读v2主文pp1–16及数据inventory p32并对照v1方法。v2将verifiability gap由v1摘要/引言的VAT−V明确改为VA−V，articulability仍VAT−VA；训练/评估流程仍是四路metric发现、fidelity优化、capture-recapture上界及nuisance审计。42任务/2.8M文本/317M preference acts，其中仅16M逐条决策/评论/投票，其余聚合engagement；不是317M独立标注者。LoRA单seed/任务、grouped 80/10/10、generated-text部分只是cross-model ranking无RL运行。公共数据/runner仍未找到可核验作者下载入口；正文有release声明但不足确认当前公共执行，故全文已审后deferred。

**2610.02878 · Evaluating VQA in Vision Language Models using Cooperative Principles**

[论文](https://arxiv.org/abs/2610.02878)

- **foundation-model**：Grice视觉/关系modifier构造语义不变VQA对照，有三人投票纠错，但开放回答主评分依赖新增AMT人评，匿名数据发布与自动判分范围尚未核实。
  复现边界：正文995总题与438+42+493分类计数不一致；不能以原答案自动判开放回答替代原人类偏好指标。改写者和答题者同模型的独立会话、多次采样不确定性需控制；先暂缓作为统一evolve evaluator。
  核查位置：§3/3.1；§4–5；§7

**2610.02549 · Evaluating Multi-Dimensional Generalization of Large Language Models in Temporal Extraction Tasks**

[论文](https://arxiv.org/abs/2610.02549)

- **foundation-model**：TimeBank/i2b2 timex/eventx跨域、扰动及长度泛化诊断与Hungarian-LCS分数有价值，但临床数据受限且作者完整变体、划分和评分包未定位，不能直接接统一评测。
  复现边界：仅保留含目标句，不能代表含空输出分布；Dense与MoE active参数8B/17B等不匹配，架构因果结论不足。少样本实例与测试文档需隔离，表面span提取并非高级时序推理。
  核查位置：§2.1–2.4；§3 model architecture；Limitations

**2610.02521 · Spatial Memory Intelligence: Endowing World Models with Understanding-Driven Long-Term Memory**

[论文](https://arxiv.org/abs/2610.02521)

- **foundation-model**：Spatial Memory Intelligence 训练 MLLM 的空间聚类、稀疏化、动作检索和可靠性过滤，控制 HY1.5/Wan2.2 长视频生成记忆。正文读完但操作监督与 benchmark 仅承诺发布。
  复现边界：审后延期：100 示范及约千条清洗 rollout 未确认公开；不能将人工规则当作已训练记忆策略；VBench/GPT 裁判与重访重建不是完整生成能力证明。
  核查位置：§4.3–4.4; §5.1–5.5; §7; Appendix F

**2610.02241 · Hardware-Native Joint Sparse-Quantization for Trillion-Scale Mixture-of-Experts**

[论文](https://arxiv.org/abs/2610.02241)

- **foundation-model**：moesq用Gumbel支持模式与量化值联合优化，router加权expert重构，paired4:8 NVFP4和Blackwell SpTC grouped kernel是论文定义性路径；现有A100/A30不能验证该原生路径。
  复现边界：SGPTQ初始化512×4096、refine8192、val128同混合语料；router冻结并缓存专家输入，再按压缩prefix逐层校准。核心是NVFP4 sparse MMA，CPU/CUDA fakequant只能机制诊断；真实B200系统验证尚缺，不冒称A100等价。
  核查位置：§3.1–3.4 Eq1–5；§4；Appendix B/D.1

**2610.01908 · Same Reward, Different Skills: When Multimodal RL Learns to Look**

[论文](https://arxiv.org/abs/2610.01908)

- **post-training**：counterfactual scene生成/target stable-switch-invariance对照与独立confirmatory set可构成视觉grounding评测；普通GRPO只训练discovery。匿名代码入口不可读，需验证scene生成器与固定dev/test公开，不能以benchmark增益替代视觉依赖证据。

**2610.01833 · Continuous Process-Level Evaluation for Evolving Enterprise AI Agent Skills**

[论文](https://arxiv.org/abs/2610.01833)

- **agent**：企业skill评测独立API计算oracle→runtimeplaceholder模板→规则/少量LLM语义judge→依赖图归因，process/outcome分离有复用价值。但当前仅真实9应用Instana/Kubecost/Cloudability两私有业务skill、104/80模板；240trials MD/TXT同时改内容，liveAPI快照漂移且图根非因果。未定位公开完整模板/trace/可执行环境，无法作为公共回归入口；已读不是未审。
  核查位置：Title and complete abstract

**2610.01794 · Continuous Conditioning of VLAs with Augmenting EMG and Visual Task Descriptors**

[论文](https://arxiv.org/abs/2610.01794)

- **foundation-model**：EMG/visual-conditioned VLA 将低通 EMG 与 proprio 拼接，另在 RoboCasa 以对象 mask 条件化动作；正文可验证设计，但真实三人 EMG 数据不公开。
  复现边界：审后延期：真实 EMG 数据和原作者训练实现未找到；人类持续纠正不是自主 agent；RoboCasa 条件来自 simulator segmentation，是特权目标 mask，不能伪称 vision-only 公平优势。
  核查位置：§III-A/B; §IV-A/B; §V; Appendix VI-B/C

**2610.01138 · Auditing Action Settlement in LLM Agent Environments: Order, Progress, and Replay**

[论文](https://arxiv.org/abs/2610.01138)

- **agent**：typed proposals冻结snapshot，五仲裁策略，位置不依顺序需单move/唯一占位等假设，不推全state公平。2160脚本episodes与独立oracle/replay注错充分，但LLM archives无有效争用、pilot不平衡且正文明确artifacts local非publicrelease。方法非新同步架构、公共结算回归harness未释放，已审暂缓。
  核查位置：§2.1–2.3；§3.1/3.4–3.5；§4

**2610.01066 · Probe with Participation Trophies: Random-Reward RL as a Probe of LLM Capability**

[论文](https://arxiv.org/abs/2610.01066)

- **post-training**：随机奖励checkpoint响应诊断有固定rollout交叉、16配对replicate及任务/奖励/输入控制，不是新的可靠能力训练。官方rl-random-prob仓库当前明确empty，缺公共脚本/数据，待补发后评估诊断入口。

**2610.01042 · Beyond Final Accuracy: Auditing Communication in LLM Multi-Agent Systems**

[论文](https://arxiv.org/abs/2610.01042)

- **agent**：ICR冻结三agent原始轨迹、六有向单hop独立revision，gold只离线分四correctness strata，no-message控制；CR/PR/SR/SCR需分报，SI可掩保留与复制两种行为。430question/2580events选择至少一错，Acc†含未观测推断，latent成本不完整不能speedup。公共评测值得纳入但作者匿名repo curl超时/web不可达，无法核任务/代码/许可，待资源可读。
  核查位置：§3.1–3.3；§4.1；AppendixG与成本；Reproducibility

**2610.00969 · A Citation-Grounded Benchmark for Trustworthy Earnings Call Transcript Analysis with Large Language Models**

[论文](https://arxiv.org/abs/2610.00969)

- **foundation-model**：ECTs-100数字证据以type/value/unit归一比较claim/citation/context，分开grounding与correctness；原完整transcript/题库/执行器发布未定位，先暂缓benchmark接入。
  复现边界：空数字默认1会虚高，须伴随coverage；相同数字不同主体/财期仍会匹配，不等于语义蕴涵。无专家对照校准，只有GPT4.1一种底座六配置，自动生成gold不能冒充金融专业真值；文档级聚合与公司切分必要。
  核查位置：§2.2–2.4；§3.2–3.4；Appendix A

**2610.00855 · Lang3DSeg: Annotation-Free Open-Vocabulary 3D Segmentation with Point Transformers**

[论文](https://arxiv.org/abs/2610.00855)

- **foundation-model**：Lang3DSeg 用 SAM3 文本集成 mask 经 LiDAR 遮挡/多视图一致性过滤作为 PTv3 加权 CE/Lovasz/CLIP 监督。nuScenes/SemanticKITTI 原始数据公开。
  复现边界：审后延期：原文代码 URL 为 github.com/<org>/Lang3DSeg 占位符且称接收后发布；关键伪标注筛选产物未提供；不能借 GT 类标取代语言伪标注。
  核查位置：§III-A–C; §IV-A–D; §V

**2610.00825 · Align Then Reason: A Multimodal Lip-Sync Judge for Dubbing**

[论文](https://arxiv.org/abs/2610.00825)

- **foundation-model**：ATR 以 AutoAVSR/XPhoneBERT 单调 CTC 关联视觉嘴型和音素，训练局部软 token judge 与标量校准；50k 多语对话/2100 测试定义清楚。
  复现边界：审后延期：自建配音训练/专业评价语料与实现未核验公开；未见语言使用 300 genuine target clips 校准，不是无目标数据零样本；Hungarian 块匹配和单 clip 指标须分开。
  核查位置：§2.1–2.3; §3.1–3.5; Appendix A/B

**2610.00673 · Closing the Loop: Practical Training Recipes for Looped Language Models**

[论文](https://arxiv.org/abs/2610.00673)

- **foundation-model**：Closing the Loop有可执行新转换配方：单标量输入重注入+平滑exit加权LM损失，正文完成核查；但本文同数据/步数不等训练FLOPs，尚缺预算匹配控制，不能将额外循环训练当成算法净收益。
  复现边界：从头配方LoopLM总9.9e21FLOPs，对同参数dense2.5e21和3.9B dense7.1e21；不能用310B对Ouro7.7T直接归因架构优越。
  核查位置：§3.1–3.6；§4.1–4.5 Eq1–2；§5.3/Table4；Appendix I/Table21

**2610.00636 · CompMat-Bench: Benchmarking AI Agents for Computational Materials Science**

[论文](https://arxiv.org/abs/2610.00636)

- **agent**：CompMat94任务由15研究65steps复现生成，precomputed HPC vs实际workflow分离，4guidance/span条件、8workflow，gold/graders隔离与fixedrule。强模型fullguidance单任务饱和，workflow需128CPU239GB/5h，42题full/reduced一样且硬件预算不齐。作者官网明确Code and data forthcoming，完整task/eval未公开，不能公共执行；已审暂缓。
  核查位置：§3.1–3.3；§4；§5；§6；作者项目页

**2610.00609 · Legal Research Bench: Measuring End-to-End Reliability in Long-Horizon Legal Research Agents**

[论文](https://arxiv.org/abs/2610.00609)

- **agent**：LRB413律师问题asofdate+allpassrubric（任何invalidcite整体fail），5public/200val/208test；15题45responses校准judge后用于全部，单trial不测runvariance。公开仓只有5样题+harness，README平台需审批与VALSkey，408正式题不公开，不能无授权接入公共evolve基准；已审暂缓。
  核查位置：§3.1–3.3；§4.2；§6；官方README Platform

**2610.00465 · AIR-LLM: Broadcasting AI Weights over Radio for Memory-Free Edge LLM Inference via RF Computing**

[论文](https://arxiv.org/abs/2610.00465)

- **foundation-model**：AIR-LLM以无线权重广播、射频乘法与校准单元执行GEMV；需专用RF硬件与测量曲线，当前GPU环境不能证明主硬件结论。
  复现边界：城市传播由Sionna光追，实物只在有线无噪条件测RF mixer误差再注入；两名默认用户按约4/3 ENOB选取，不是所有用户端到端分布。不得把模拟噪声注入命名为真实无线LLM复现。
  核查位置：§3 RF engine/calibration；§4.1–4.2；§5.1

**2610.00425 · Code That Works, Environments That Don't: Measuring Environment Reproducibility in AI-Generated Software**

[论文](https://arxiv.org/abs/2610.00425)

- **agent**：Gen→Repair 在干净 Docker 中最多 10 次修复，比较初始声明、最终安装、ptrace 动态加载三层依赖集。
  复现边界：论文称 50×4×3 主实例加400重复均手工执行，承诺开放材料但正文未定位任务包。动态加载仅覆盖被执行路径且漏掉 C++ header-only；C++ transitive=1 是定义，不能当模型改善。待官方任务/容器/解析器发布。
  核查位置：§2–5、§6.6

**2610.00316 · DuplexSpeechBench-Document Grounding: Benchmarking Document Grounding and Hallucinations in Voice Agents**

[论文](https://arxiv.org/abs/2610.00316)

- **agent**：DSB-DG 50文档1636QA、20对话，以固定证据的递增context tier、probe-distractor-repeat与不同refresh频次比较语音grounding与延迟。
  复现边界：需官方完整QA/音频/对话/scorer包，当前仅定位项目页；ground truth仅judge可读。GDS接近0需结合初始GA，FTED是用户语音结束至首token，不是完整语音时延；平台context注入和ASR错误需独立记录。
  核查位置：§2–4、Appendix B–E/H

**2610.00197 · Comedic Fool's Gold: Reward Exploits and Countermeasures in Conversational Humor**

[论文](https://arxiv.org/abs/2610.00197)

- **post-training**：对话幽默reward审计有笑声通道、全speaker归一与并发scorer噪声诊断；仪器修正后微小taste gain消失，遗留token漏洞未封全。未找到公开数据/runner入口，不能仅凭内部archived声明认定公共评测可执行。

**2610.00092 · BudgetSchemaBench: A Budget-Swept Diagnostic for Schema Context in Text-to-SQL**

[论文](https://arxiv.org/abs/2610.00092)

- **agent**：BudgetSchemaBench的预算扫描/数据库命名空间验证/执行评分适合evolve评测，但官方仓库只有339字节README.MD，明确Code under organization's review and will be released soon，公开执行发布阻塞。
  复现边界：gold-guaranteed上下文仅诊断不可给被测Agent；移除gold表仍94.6%命中提示污染但非证明；serialization≤2pp且CI±4不是等价(δ3TOST未成立)。正文声称BSD3发布与官方现状不符，仓库license=null、没有runner/manifest。
  核查位置：§3；§4 Tables4–5；§5；官方README.MD及contents API 2026-10-07

**2610.00054 · The First Token Is Not the Verdict: Hidden Costs of Reading LLM Judges Without Generating**

[论文](https://arxiv.org/abs/2610.00054)

- **recommendation**：LLM judge 首 token 读取的位置偏差审计，转后训练评测；不能当推荐线上研究。
- **post-training**：提出first-token compliance检查与不合规才生成的judge读数协议，具有通用评测价值；1678/11596需要生成，85.5%节省但合规子集仍0–5.5%读数错误，不能把首token当最终裁决。未找到作者代码/预测数据公共入口；等待可执行资源确认，不记已接入。

**2610.00015 · From Proposal to Verified Effect: Praxa, an Evidence-Bound Harness for Governed AI Agent Execution**

[论文](https://arxiv.org/abs/2610.00015)

- **agent**：Praxa 由model提案，经确定性authority gate、broker执行、read-back evidence绑定状态，并对recursive specialist候选以protected/resource gate核验。
  复现边界：核心authority executor私有，public SDK不含执行器。Terminal-Bench12任务pilot固定顺序与rebuild不对称、verifier未全计预算；recursive topology是synthetic proxy且optimizer未运行。HOLD确认性试验零次，registry/config wiring不能称真实改进。待公开核心实现或许可。
  核查位置：§3–6、§8–11


## 拒绝／范围外（367）

**2610.08781 · IdeaAnchor: Teaching LLMs to Turn Literature into Research Ideas**

[论文](https://arxiv.org/abs/2610.08781)

- **post-training**：正文为anchor数据/特权监督范式，优化器仍标准SFT、self-training和GRPO；可作为Agent科研数据方法，不纳入核心优化器实现。 该决定仅限后训练核心track，Agent方法/数据公共入口由Agent track独立判断，不能据此全局拒绝。

**2610.08668 · Semantic Behavioral Watermarking: Paraphrase-Robust and Forgery-Resistant Provenance for LLM Agents**

[论文](https://arxiv.org/abs/2610.08668)

- **agent**：SBW的语义聚类/历史keyed PRF/弃权margin为Agent行为溯源水印算法，主要优化归因检测而非Agent规划、学习、工具使用或任务能力，排除本轮核心能力收录。
  复现边界：§7明示ToolBench无环境执行反馈；复制/链式replay未解决；utility只是动作与argmax一致率，不是任务成功率；部分鲁棒审计artifacts未保留。
  核查位置：§3 threat model；§4.1–4.3；§5；§6.1/6.3/6.4 Tables2/4/5；§7

**2610.08651 · A Case Study in Assuring AI-Written Software**

[论文](https://arxiv.org/abs/2610.08651)

- **agent**：医疗软件治理案例研究，无独立Agent算法贡献。
  核查位置：Title and complete abstract

**2610.08630 · Towards In-Parameter Memory Augmentation for Large Language Models**

[论文](https://arxiv.org/abs/2610.08630)

- **agent**：参数记忆综述，无新核心算法。
  核查位置：Title and complete abstract

**2610.08561 · Reinforcement Learning for Hierarchical Reasoning Rewards: Minimax-Optimal Rates with Transformers**

[论文](https://arxiv.org/abs/2610.08561)

- **post-training**：定义depth curriculum/prefix自适应查询actor-critic并证明最小极大速率，但本文是形式化理论设置，未核实实际LLM训练benchmark；不列能力复现。

**2610.08539 · RSJEV: Discriminative Remote Sensing Scene Classification with Multimodal Large Language Models**

[论文](https://arxiv.org/abs/2610.08539)

- **foundation-model**：RSJEV把已有JEV/Mapika式候选条件化单token判别读出及CE+Brier目标用于遥感分类；正文核查未发现区别于已登记LLM2Jev/既有Decider的新核心训练机制，作为专门领域复用不另立基础模型算法。
  核查位置：§I–III；§IV.A–E；TableII

**2610.08528 · MedCORE: Criteria-Grounded Clinical Reasoning for Interpretable Medical Image Diagnosis**

[论文](https://arxiv.org/abs/2610.08528)

- **foundation-model**：MedCORE面向皮肤、超声、视网膜病理诊断的临床标准图网络；属于特定医疗应用而非通用基础模型算法。

**2610.08482 · Knee3DVLM: Dual-Sequence Full-Volume Vision-Language Modeling for Comprehensive Knee MRI Assessment**

[论文](https://arxiv.org/abs/2610.08482)

- **foundation-model**：Knee3DVLM为膝关节MRI双序列57诊断目标建模，属特定医疗模型应用。

**2610.08430 · NeMo-DCR: Bit-Exact Delta-Compressed Refit for Scalable Agentic RL at Trillion-Parameter Scale**

[论文](https://arxiv.org/abs/2610.08430)

- **agent**：NeMo-DCR权重同步/精确delta传输系统，归训练基础设施而非Agent策略。
  核查位置：Title and complete abstract

**2610.08407 · Seeing the Context: Enhancing Recommender Systems with Image-Derived Contextual Signals**

[论文](https://arxiv.org/abs/2610.08407)

- **recommendation**：ICE-Fuse 在 TripAdvisor 图文上下文上做 RMSE/消融；未提供线上分流或部署实验，不满足工业搜广推准入。

**2610.08337 · Machine Learning for German Redispatch Forecasting under Data Delays and Temporal Distribution Shift**

[论文](https://arxiv.org/abs/2610.08337)

- **foundation-model**：德国电网再调度概率预测比较，属于能源时序应用而非基础模型核心算法。

**2610.08331 · Transferable Spatial Temporal Coherence Adversarial Attack on Black-Box Vision Language Models for Autonomous Driving**

[论文](https://arxiv.org/abs/2610.08331)

- **foundation-model**：自动驾驶视频VLM迁移攻击研究，主贡献为攻击构造而非基础模型能力训练/推理方法。

**2610.08300 · Memory Depth and Reconstructed Context Width: A Controlled Evaluation of Hierarchical Retrieval**

[论文](https://arxiv.org/abs/2610.08300)

- **foundation-model**：分层会话检索深度/上下文宽度的控制实验，主要为系统诊断而非新的基础模型核心算法。

**2610.08245 · Aligning Performance with Contribution: Towards Contribution-Aware Fair Recommendation**

[论文](https://arxiv.org/abs/2610.08245)

- **recommendation**：CPFR 使用 MovieLens 100K/1M、Amazon Office 的贡献公平性离线实验；公平损失有效性与工业线上证据是两回事。

**2610.08232 · Behavior-Mining, Generative Conversations, and Collaborative Advisory: the Future of Travel and Tourism Recommender Systems**

[论文](https://arxiv.org/abs/2610.08232)

- **recommendation**：旅游推荐的研究展望/立场综述，提出未来 advisory 方向而非可复现的新算法与实验。

**2610.08208 · STRUCTURALCOST: A controlled reading time dataset for modeling human sentence processing difficulty**

[论文](https://arxiv.org/abs/2610.08208)

- **foundation-model**：STRUCTURALCOST人类句法阅读时长数据，暂无直接基础模型能力/evolve执行任务契约。

**2610.08200 · Finding the Heads and the Neurons Responsible for Network Information Retrieval in Language Models**

[论文](https://arxiv.org/abs/2610.08200)

- **foundation-model**：内部头/神经元实体检索定位为解释性分析，未定义独立可执行能力评测。

**2610.08136 · Adapting Generative Recommenders for Multi-Turn Interaction**

[论文](https://arxiv.org/abs/2610.08136)

- **recommendation**：INTEGER 用 Amazon Beauty/Toys 与 Tencent Hy3 生成多轮对话，报告离线命中/NDCG/对话质量；未提供生产线上对照。

**2610.08129 · Do LLMs Act on What They Know? From Partner Representations to Cooperative Actions**

[论文](https://arxiv.org/abs/2610.08129)

- **recommendation**：Hanabi 合作约定是 Agent 协同研究，转 Agent 审查，不作为工业搜广推收录。
- **agent**：Hanabi受控接收决策的knowing-doing机制诊断，非完整自主合作；本轮不作为能力实现接入，保留为oracle/表征泄漏负面参考。
  复现边界：不能把oracle规则/代码翻译动作当evaluated Agent能力；activation实验仅Qwen3-8B和recorded states，完整游戏增益未证；未发现可执行公共基准/代码发布链接。
  核查位置：§3.1–3.3；§4.1–4.3；§5.1/5.7；AppendixI/Limitations

**2610.08097 · When Tools Lie: Reliability of Mathematical Agents Under Corrupted Tool Feedback**

[论文](https://arxiv.org/abs/2610.08097)

- **agent**：31数学任务的工具损坏与验证频率对照，作者明确不能控制比较verifier质量。
  核查位置：Title and complete abstract

**2610.08090 · Explainable Rule Mining of IPv6 Extension-Header Presence Patterns from Paired-Vantage Captures**

[论文](https://arxiv.org/abs/2610.08090)

- **foundation-model**：IPv6扩展头规则挖掘的网络测量负结果，不属于基础模型算法。

**2610.08082 · POLAR: Ontology-Guided Risk Prevention for Tool-Calling LLM Agents**

[论文](https://arxiv.org/abs/2610.08082)

- **post-training**：通过可逆性本体和动作剪枝实现推理时护栏，不更新模型或RL/蒸馏目标；转Agent方向。
- **agent**：POLAR当前不进入能力/安全改进复现队列：人工Datalog可逆本体弱链min评分+veto机制明确，但收益不能区分结构反搜与blanket veto，关键实现/本体/日志私存且原配置不可追溯。
  复现边界：Escalate/Advisory存档均值与表冲突而撤回比较；不同arm各自errorfilter，baseline adaptation不等算力；不能把可逆等同授权/安全；保留否定性对照价值，不据此claim运行通过。
  核查位置：§3.2–3.6 Eq1；§4.1–4.6 Tables3–6；Limitations/Resource declaration

**2610.08068 · PhysTacGen: Physics-Aware Visual-Tactile Sensor Image Generation**

[论文](https://arxiv.org/abs/2610.08068)

- **foundation-model**：PhysTacGen服务视觉到触觉传感器图像生成，主要为特定机器人模态合成流水线；后训练机制可由对应track审查。

**2610.08018 · Structured but Silent: Probing Capability Requirements in LLM Hidden States**

[论文](https://arxiv.org/abs/2610.08018)

- **agent**：TACIT隐藏状态线性probe诊断能力需求，非执行策略。
  核查位置：Title and complete abstract

**2610.07982 · M3SunAgent: Monocular 3D Spatial Understanding Agent for Metric Depth Estimation and 3D Visual Grounding**

[论文](https://arxiv.org/abs/2610.07982)

- **foundation-model**：M3SunAgent为工具协调的3D空间规划agent，应由agent track审查。

**2610.07966 · Feature Encoding in VAE-based Audio Decoders: Effects of Input, Depth and Distribution**

[论文](https://arxiv.org/abs/2610.07966)

- **foundation-model**：RAVE/EnCodec内部特征探针与聚类分析，主要为表示解释性诊断。

**2610.07954 · Revisiting Numerical Forecasting Models for Language-Based Trajectory Prediction**

[论文](https://arxiv.org/abs/2610.07954)

- **foundation-model**：MoRE为行人/运动员轨迹预测的专用RL奖励迁移，非通用基础模型算法。

**2610.07937 · Leveraging a four-quadrant approach for evaluating Redpine Science**

[论文](https://arxiv.org/abs/2610.07937)

- **agent**：Redpine Science检索服务四象限评测报告，非新Agent算法。
  核查位置：Title and complete abstract

**2610.07913 · Multimodal Knowledge Distillation for Gastric Adenocarcinoma Classification from Whole-Slide Images**

[论文](https://arxiv.org/abs/2610.07913)

- **foundation-model**：胃腺癌病理图像蒸馏是特定医疗应用，不是通用基础模型方法。

**2610.07886 · ShanLiangRen: A Nutrition Agent for Personalized Daily Meal Planning**

[论文](https://arxiv.org/abs/2610.07886)

- **agent**：ShanLiangRen是领域约束检索+LLM proposal/repair+确定营养计算+Pareto筛选demo，当前不纳通用Agent核心复现：无公开155万recipe/6万ingredient知识库与300评测实例，未拆解核心模块贡献或给预算/迭代配置。
  复现边界：PCS是单项约束满足百分比不等于临床安全；nutrient interval/成分表与总量正确不证明可用于过敏或疾病处方。Pareto机制非独特通用策略且关键资料不可验证；保留领域应用线索，不实施医疗建议。
  核查位置：§3 five-module System Design; §4; §5 Table1; §6

**2610.07881 · Self-Referenced Social Preferences: Cooperation without Observing Others Rewards**

[论文](https://arxiv.org/abs/2610.07881)

- **agent**：传统MARL自参照奖励社会偏好，无LLM/工具Agent方法。
  核查位置：Title and complete abstract

**2610.07842 · Privileged Context as Drift in On-Policy Self-Distillation**

[论文](https://arxiv.org/abs/2610.07842)

- **post-training**：27个adapter的特权上下文content×source控制研究；目标任务与既有lm-evaluation-harness留存benchmark，加逐token/逐序列KL和LoRA几何诊断。未定义独立新任务或评分器，作为OPSD风险/消融参考，不新增核心算法/公共评测入口。

**2610.07825 · Forecast Accuracy Is Not Trading Profit: Evolving Small Recurrent Networks for Stock Return Prediction**

[论文](https://arxiv.org/abs/2610.07825)

- **foundation-model**：股票收益预测与交易策略中小循环网络进化比较，属于金融时序应用。

**2610.07787 · OOPMAS: Object-Oriented Multi-Agent Systems for Query-Level Workflow Generation**

[论文](https://arxiv.org/abs/2610.07787)

- **agent**：OOPMAS的OOP agent/workflow生成机制可作训练内搜索诊断，但当前论文的主要分数来自同批query反复正确性反馈并选skill开/关较高者，不满足隔离测试能力复现门槛。
  复现边界：baseline workflow格式不兼容造成0分，成本baseline为估计；正文$35/$15同时称约7×算术不一致。run-local技能库不跨部署持久化。若重做train/val/test独立实验才可另审，不能把oracle评分给被评估Agent。
  核查位置：§3.1–3.3 Algorithm1; §4.1–4.6 Table1; Appendix A/B

**2610.07782 · Persistent Memory in Multi-Agent LLM Inference: What It Costs, What It Buys, and When You Can Tell**

[论文](https://arxiv.org/abs/2610.07782)

- **agent**：持久记忆消融的测量修正与null结果研究，不是独立新策略。
  核查位置：Title and complete abstract

**2610.07781 · Quantization Effects on Tool-Failure Recovery Vary Across Prompts and Evaluation Designs**

[论文](https://arxiv.org/abs/2610.07781)

- **post-training**：4/8bit代理故障恢复的提示/评分协议评测，无训练算法。
- **agent**：量化Agent恢复对prompt/筛选/scoring敏感性的实验诊断。
  核查位置：Title and complete abstract

**2610.07761 · Contrastive Learning for Aspect Representation towards Explainable Recommendation**

[论文](https://arxiv.org/abs/2610.07761)

- **recommendation**：CLARER 在 TripAdvisor HK、Yelp 2019、Amazon Movies/TV 做 RMSE/MAE/BLEU/ROUGE 离线对照；未给线上 A/B 或部署结果。

**2610.07755 · Trustworthy Method Comparison with AI Judges: Estimation and Design under Order, Batch, and Aggregation Effects**

[论文](https://arxiv.org/abs/2610.07755)

- **foundation-model**：AI judge统计设计与Markov GLMM推断研究，非基础模型训练或推理核心算法。

**2610.07730 · SanSi: A Looped Typed Decision Model for System 1.5 Thinking**

[论文](https://arxiv.org/abs/2610.07730)

- **post-training**：主要贡献为循环typed-decision模型架构和逐循环proper scoring，转基础模型审查。

**2610.07704 · Independent Multi-Agent Reinforcement Learning with Counterfactual Semantic-Social World Models**

[论文](https://arxiv.org/abs/2610.07704)

- **agent**：CASTLE独立PPO和双world model传统MARL，无LLM Agent执行。
  核查位置：Title and complete abstract

**2610.07668 · CACHEFORGE: LLM-Guided End-to-End Generative Cache Replacement Policy for Performance and Hardware Efficiency**

[论文](https://arxiv.org/abs/2610.07668)

- **foundation-model**：CACHEFORGE用LLM进化CPU硬件cache替换策略，不是LLM KV缓存算法；属agent辅助硬件设计。
- **post-training**：LLM生成C++缓存策略并在模拟器演化，不是LLM参数后训练；转Agent研究。

**2610.07640 · Towards the Automatic Synthesis of Interpretable Chess Tactics**

[论文](https://arxiv.org/abs/2610.07640)

- **agent**：PAL归纳逻辑学习国际象棋符号战术，不是LLM Agent方法。
  核查位置：Title and complete abstract

**2610.07615 · AFA-BANDIT: Provably Near-Optimal Online Multi-Feature Classification Under Budget Constraints**

[论文](https://arxiv.org/abs/2610.07615)

- **agent**：AFA-BANDIT在线特征获取bandit分类，不是LLM Agent。
  核查位置：Title and complete abstract

**2610.07594 · BiGym 2.0: Benchmarking Learned and Agent-Developed Policies for Humanoid Household Manipulation**

[论文](https://arxiv.org/abs/2610.07594)

- **agent**：BiGym2人形机器人家务基准，对照VLA/IL/RL/编码Agent，不是新语言策略。
  核查位置：Title and complete abstract

**2610.07578 · Cooperating with Future Collaborators: Multi-Agent RL under Staggered Participation**

[论文](https://arxiv.org/abs/2610.07578)

- **agent**：SPL错峰传统MARL训练增广，无LLM策略。
  核查位置：Title and complete abstract

**2610.07576 · CETUS: How Far Do Representations Trained on Earth Transfer to Cassini SAR of Titan?**

[论文](https://arxiv.org/abs/2610.07576)

- **foundation-model**：CETUS地球到土卫六SAR表征迁移评测，摘要明确比较无法隔离预训练效应；属于专用领域诊断。

**2610.07569 · OpenSplatGraph: From Dense Semantic Maps to Structured Scene Graphs for Open-Vocabulary Robot Perception**

[论文](https://arxiv.org/abs/2610.07569)

- **foundation-model**：OpenSplatGraph在线3D高斯语义地图转场景图，属于机器人感知地图系统。

**2610.07550 · Foundation Model-Aided Multi-Agent Reinforcement Learning for Wireless Random Access Network Optimization**

[论文](https://arxiv.org/abs/2610.07550)

- **agent**：FM辅助无线随机接入actor-critic，非LLM工具Agent。
  核查位置：Title and complete abstract

**2610.07545 · Quality-Aware Self-Correcting Speech Translation on an Edge Device**

[论文](https://arxiv.org/abs/2610.07545)

- **post-training**：明确无需重训的边缘语音翻译QE/MBR推理纠正。

**2610.07535 · Disentangling Models from Personas in Heterogeneous LLM Simulations**

[论文](https://arxiv.org/abs/2610.07535)

- **agent**：异构模型社会仿真影响研究，无新执行算法。
  核查位置：Title and complete abstract

**2610.07534 · The EPIC Framework for Spec-Driven Development**

[论文](https://arxiv.org/abs/2610.07534)

- **agent**：EPIC规格质量实践框架/访谈与相关性研究，非Agent算法。
  核查位置：Title and complete abstract

**2610.07509 · On Open-Ended Information Seeking for Information Elicitation Agents**

[论文](https://arxiv.org/abs/2610.07509)

- **agent**：信息引出偏好受模型影响的受控行为研究。
  核查位置：Title and complete abstract

**2610.07491 · Who Bears the Burden? Learning Responsibility for Shared Constraints in Multi-Agent Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.07491)

- **agent**：LiRA共享约束传统MARL福利梯度，不是LLM策略。
  核查位置：Title and complete abstract

**2610.07489 · Deep Defence on Wheels: A Dual Intrusion Detection System Architecture for Comprehensive In-Vehicle Network Security**

[论文](https://arxiv.org/abs/2610.07489)

- **foundation-model**：车内CAN网络双入侵检测器的FPGA部署，不属基础模型研究。

**2610.07475 · Adapting to Changes in Agent Behavior via Finite-Depth Policy Sensitivity**

[论文](https://arxiv.org/abs/2610.07475)

- **agent**：有限深度RL策略敏感性估计与追逃博弈，无语言Agent。
  核查位置：Title and complete abstract

**2610.07460 · ElasticFit: Fit-Aware 3D Object Insertion via VLM Reasoning and Generative Adaptation**

[论文](https://arxiv.org/abs/2610.07460)

- **foundation-model**：ElasticFit为3D物体插入和几何约束适配流水线，非通用多模态基础模型训练。

**2610.07426 · AccentCL: Robust Accent Classification with Incremental Expansion**

[论文](https://arxiv.org/abs/2610.07426)

- **foundation-model**：AccentCL英语口音分类及类别增量扩展，属于特定语音分类任务。

**2610.07402 · Rethinking Semantic ID Construction for Generative Recommendation: SimHash with Parallel Decoding and Semantic Alignment**

[论文](https://arxiv.org/abs/2610.07402)

- **recommendation**：FLASH 在四类 Amazon 数据上做 Recall/NDCG 与 early stopping；作者开源不替代工业线上证据。

**2610.07359 · Evaluate the Stack, Not the Layer: Do Deterministic and LLM Gates for Agent Actions Fail Independently?**

[论文](https://arxiv.org/abs/2610.07359)

- **agent**：确定规则与LLM gate错误耦合的统计评测，不是新策略。
  核查位置：Title and complete abstract

**2610.07339 · A doctrine-grounded visual question answering dataset for Tactical Combat Casualty Care**

[论文](https://arxiv.org/abs/2610.07339)

- **foundation-model**：TC3-VQA战术伤救视觉问答数据集，主要贡献是领域数据与来源锚定。

**2610.07269 · What Words Keep of a Place: Zero-Shot Language Reasoning for Cross-View Geo-Localization**

[论文](https://arxiv.org/abs/2610.07269)

- **foundation-model**：GeoLingual跨视角定位语言描述的可辨识性与负结果诊断，主要是应用评估。

**2610.07243 · Hybrid Cross-Modal Attention Network for Early Breast Cancer Detection in Low-Resource Clinical Settings**

[论文](https://arxiv.org/abs/2610.07243)

- **foundation-model**：HCMAN乳腺癌临床图像/结构化资料融合，专用医疗模型应用。

**2610.07226 · Minimal Witness Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.07226)

- **post-training**：MWRL核心是集合格上的minimal-witness策略梯度；LLM实验冻结Qwen并搜索head/MLP子集，不是训练LLM语言策略，转电路发现/通用RL。

**2610.07168 · A theory of platonic representations in language models**

[论文](https://arxiv.org/abs/2610.07168)

- **foundation-model**：跨语言柏拉图表征理论及合成语言诊断，主贡献是解释规律而非新基础模型算法。

**2610.07091 · Smart Content Ingestion for Generative AI Workloads**

[论文](https://arxiv.org/abs/2610.07091)

- **foundation-model**：企业多格式内容抽取系统与检索评估，非基础模型核心算法。

**2610.07062 · Learning to Simulate Individuals from Macro Social Signals**

[论文](https://arxiv.org/abs/2610.07062)

- **foundation-model**：macro2mind市场信号训练用户模拟器，属专用后训练应用。

**2610.07060 · Skillful Data-Driven Subseasonal Soil Moisture Forecasting: Prospects and Limits for Flash Drought Prediction**

[论文](https://arxiv.org/abs/2610.07060)

- **foundation-model**：土壤湿度次季节预测的特定气象模型与问题表述。

**2610.07032 · Investigating Model Compression for Neural Machine Translation in the Biomedical Domain**

[论文](https://arxiv.org/abs/2610.07032)

- **foundation-model**：法英生医翻译的已有蒸馏量化结合，属于领域压缩应用。

**2610.07023 · Beyond Refusal Patterns: Safe-Role Internalization for Robust and Generalizable LLM Safety Alignment**

[论文](https://arxiv.org/abs/2610.07023)

- **post-training**：SSRFT核心是安全角色QA生成扩展与常规SFT的安全对齐数据流程，未形成新增优化器/蒸馏算法；保留安全数据研究价值但不收入本轮核心算法。

**2610.07014 · DTFormer: Text-Guided Semantic Alignment for RGB-D Segmentation**

[论文](https://arxiv.org/abs/2610.07014)

- **foundation-model**：DTFormer RGB-D分割加入文本语义原型，为专用分割网络。

**2610.06977 · Visual-Invariance-Augmented Feature Optimal Alignment for Transferable Adversarial Attacks against Closed-Source MLLMs**

[论文](https://arxiv.org/abs/2610.06977)

- **foundation-model**：IAU-FOA多模态迁移攻击，非基础模型能力算法。

**2610.06972 · BoT-Feedback: Grounding Multimodal Reasoning in Biomechanical Evidence for Explainable Human Action Feedback**

[论文](https://arxiv.org/abs/2610.06972)

- **foundation-model**：BoT-Feedback生物力学指导动作教学反馈，专用应用框架。

**2610.06962 · Verdicts Without Annotated Evidence: Rejection Sampling or Label-Only Post-Training for Evidence Recovery?**

[论文](https://arxiv.org/abs/2610.06962)

- **post-training**：ContractNLI既有任务上的label-only SFT与RSFT比较，document split无重叠但单seed；新内容是两种监督的证据质量解耦分析，未形成独立公开任务/评分器。作为evidence recovery消融参考，非新增入口。

**2610.06918 · Learning from Unreliable Trajectories: Adversarially-Robust Federated Q-Learning**

[论文](https://arxiv.org/abs/2610.06918)

- **agent**：Robust Async-Fed-Q联邦表格RL理论，不是语言Agent。
  核查位置：Title and complete abstract

**2610.06902 · Tree Navigation Without LLM Summaries: A Matched-Cost Study of Hierarchical Retrieval for Long-Document QA**

[论文](https://arxiv.org/abs/2610.06902)

- **foundation-model**：NavTree确定性层级RAG检索导航，agent track范围。

**2610.06896 · Medical Image Alignment Assessment as a Test of Generalist Visual Reasoning in Frontier Multimodal Models**

[论文](https://arxiv.org/abs/2610.06896)

- **foundation-model**：医疗图像对齐的前沿多模态模型评估，无新核心算法。

**2610.06874 · Statistical Turbulence and High-Fidelity Disturbance Fields for Quadrotor Flight Control**

[论文](https://arxiv.org/abs/2610.06874)

- **agent**：风场保真度对四旋翼PPO控制器的交叉评测，非LLM Agent研究。
  核查位置：Title and complete abstract

**2610.06851 · Base Models Can Reason By Taking a Cue From Training Data**

[论文](https://arxiv.org/abs/2610.06851)

- **post-training**：通过起始token及预训练数据因果干预研究reasoning cue，非新的后训练算法。

**2610.06833 · Towards Looped Models Done Right, Part II: Rethinking at Fixed Points**

[论文](https://arxiv.org/abs/2610.06833)

- **post-training**：循环模型固定点、depth prior和正交注入主要为架构/训练基础，交由基础模型track。

**2610.06790 · Back to the Future: Rethinking EDA Infrastructure for Agentic Systems in Chip Design Verification**

[论文](https://arxiv.org/abs/2610.06790)

- **agent**：BTTF主要贡献是领域专用VCD→SQLite及标准分工/自纠错Agent工程；未公开150查询/RTL波形/评分器，缺独立通用Agent算法和可接入评测包，不通过当前复现门槛。
  复现边界：SVA规则匹配/已观测波形检查不是完整formal verification；作者“hallucination-free production”超出单自建集证据，无随机生产AB；未报告多次独立运行/heldout划分/代码数据链接。
  核查位置：§3.1–3.2; §4 Tables1–2; §5; Appendix A

**2610.06784 · How to scale your HEP ML models: A recipe for robust architecture comparisons at scale**

[论文](https://arxiv.org/abs/2610.06784)

- **foundation-model**：高能物理jet模型的缩放律比较方法，非当前语言/视觉/多模态基础模型算法范围。

**2610.06744 · ufakzeka-karar: An Open Turkish Typed-Decision Model with Order-Invariant Option Scoring**

[论文](https://arxiv.org/abs/2610.06744)

- **post-training**：土耳其typed-decision模型头与数据发布；主要比较交叉熵和REINFORCE，非新LLM策略算法。

**2610.06726 · Decoupling Time and Space: A Temporally Conditioned Refinement for EEG Source Imaging**

[论文](https://arxiv.org/abs/2610.06726)

- **foundation-model**：EEG源定位时间条件细化，属于医疗信号逆问题专用模型。

**2610.06715 · Domain adaptation of Russian ModernBERT for long legal documents**

[论文](https://arxiv.org/abs/2610.06715)

- **foundation-model**：俄语法律ModernBERT领域继续预训练比较，摘要未提出新的通用训练算法。

**2610.06703 · Reading the Mood: Emotion-Guided Book-to-Music Recommendation via CGANs and LLMs**

[论文](https://arxiv.org/abs/2610.06703)

- **recommendation**：SAGA-CDR 使用 Amazon 2023 图书到音乐、Douban 交叉验证与多 seed 离线冷启动评价；没有线上流量实验。

**2610.06685 · Aligning Multimodal Patient Evidence with Biomedical Knowledge Graphs for Clinical LLMs**

[论文](https://arxiv.org/abs/2610.06685)

- **foundation-model**：MM-KG临床证据与生医知识图融合，属于医疗知识系统应用。

**2610.06670 · Reward Stealing Attack on Large Language Models**

[论文](https://arxiv.org/abs/2610.06670)

- **foundation-model**：ReSA逆RL提取代理安全奖励用于攻击，主贡献为攻击而非基础模型能力算法。
- **post-training**：ReSA逆RL抽取代理安全reward后在推理时反转解码，主要攻击/推理方法而非训练改进。

**2610.06651 · Considering Context: When World Models Need Context Encoders**

[论文](https://arxiv.org/abs/2610.06651)

- **agent**：模型式RL context predictive-sufficiency诊断理论，无LLM Agent算法。
  核查位置：Title and complete abstract

**2610.06614 · FREA: A Multi-Source Expert Benchmark for Reaction Feasibility Verification**

[论文](https://arxiv.org/abs/2610.06614)

- **agent**：FREA反应可行性专家benchmark与forward model训练，非Agent策略。
  核查位置：Title and complete abstract

**2610.06603 · Word-Level Text Unmixing via Evidence-Preserving Ownership Routing with Language Models**

[论文](https://arxiv.org/abs/2610.06603)

- **agent**：EPOR逐词文本源归属重建监督方法，不是Agent行动算法。
  核查位置：Title and complete abstract

**2610.06590 · SPRIG: Semantic-ID-enhanced Paths for Knowledge Graph-based Generative Recommendation**

[论文](https://arxiv.org/abs/2610.06590)

- **recommendation**：SPRIG 将知识图谱与 SID 结合，在 ML1M/LFM2B 上比较；属于公开离线推荐研究，未满足线上准入。

**2610.06584 · Does AI Help Cyber Attackers or Defenders? Evidence from Nonpublic Vulnerabilities and Subsequent Attacks**

[论文](https://arxiv.org/abs/2610.06584)

- **agent**：非公开漏洞攻防能力评测，不是新Agent方法。
  核查位置：Title and complete abstract

**2610.06582 · Mind the Execution Gap: Action-Semantic Mismatch in World-Model Control**

[论文](https://arxiv.org/abs/2610.06582)

- **foundation-model**：异步执行与控制器动作语义纠正接口，主要为控制系统诊断与接口修复。

**2610.06571 · BrainTRACE: Tracing Longitudinal, Multimodal, and Volumetric Evidence in Brain MRI Clinical Reasoning**

[论文](https://arxiv.org/abs/2610.06571)

- **foundation-model**：BrainTRACE纵向脑MRI证据链benchmark，非基础模型新算法。

**2610.06409 · FlashCart: Fast Cartesian Tensor Products for Equivariant Interatomic Potentials**

[论文](https://arxiv.org/abs/2610.06409)

- **foundation-model**：FlashCart为原子势能等变张量积GPU内核与结构，属于专用原子模拟模型而非当前基础模型范围。

**2610.06394 · Harnessing Multimodal Large Language Models for Training-Free Human-Object Interaction Detection**

[论文](https://arxiv.org/abs/2610.06394)

- **foundation-model**：HarnessHOI用MLLM主动交互假设进行HOI检测，属于视觉应用harness，而非基础模型训练。

**2610.06387 · Scaling Down the Scaling Laws: Parameter Efficiency and Compute-Optimal Training in Resource-Constrained Large Language Models**

[论文](https://arxiv.org/abs/2610.06387)

- **foundation-model**：资源受限LLM缩放律综述，没有新的原始核心算法。

**2610.06360 · Ontology Concept Overlap as a Training Signal: Knowledge-Grounded Reinforcement Learning for Clinical Question Answering**

[论文](https://arxiv.org/abs/2610.06360)

- **post-training**：UMLS concept overlap+judge+consistency属于任务reward组合，GRPO目标标准；贡献限临床3–3.8B且7B全collapse，不当作通用新优化器。

**2610.06320 · CRAFTER: Causality-based Self-adaptation for Autonomous IoT Systems**

[论文](https://arxiv.org/abs/2610.06320)

- **agent**：CRAFTER因果RL自适应IoT系统，非LLM Agent。
  核查位置：Title and complete abstract

**2610.06293 · VepAgent: Bridging Causal-Transition via Tool-Augmented Reinforcement Learning for Video Event Prediction**

[论文](https://arxiv.org/abs/2610.06293)

- **foundation-model**：VepAgent视频事件预测的工具增强RL，由agent track审查。

**2610.06251 · Shared Stopping Decisions Change Answers in HQQ Cache Quantization**

[论文](https://arxiv.org/abs/2610.06251)

- **foundation-model**：HQQ共享停止条件导致跨请求干扰的实现诊断与修复，无新基础模型核心算法。

**2610.06207 · AI-Decision Checkpoints for AI-Augmented Business Process Management: Framework and Educational Instantiation**

[论文](https://arxiv.org/abs/2610.06207)

- **agent**：AI-decision checkpoints业务流程教学框架，非算法。
  核查位置：Title and complete abstract

**2610.06196 · EORestore-Agent: Fidelity-Guided Agentic Restoration of Remote Sensing Images with Composite Degradations**

[论文](https://arxiv.org/abs/2610.06196)

- **foundation-model**：EORestore遥感图像恢复agent，属领域工具编排系统。

**2610.06148 · Reinforcement Learning-Based Optimization of Workload-Aware Power Delivery Networks**

[论文](https://arxiv.org/abs/2610.06148)

- **agent**：PDN电网DQN线宽优化，非语言Agent。
  核查位置：Title and complete abstract

**2610.06083 · Boosting Transferable Adversarial Attacks against Deep Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.06083)

- **agent**：DQN/DDQN CartPole迁移对抗扰动，非LLM Agent。
  核查位置：Title and complete abstract

**2610.06069 · Attention Tax, Handoff Tax: A Stylised Model of When Multi-Agent LLM Systems Help**

[论文](https://arxiv.org/abs/2610.06069)

- **foundation-model**：多agent可靠性/通信代价理论模型，由agent track审查。
- **agent**：多Agent可靠性的stylised attention/handoff理论与测量，非独立新执行算法。
  核查位置：Title and complete abstract

**2610.06063 · Vision Transformer Ensembles for Panoramic Street Segmentation**

[论文](https://arxiv.org/abs/2610.06063)

- **foundation-model**：街景分割挑战现有架构集成，无新基础模型方法。

**2610.06050 · MATE: Adaptive Long- and Short-Term User Memory for LLM-Based Recommendation**

[论文](https://arxiv.org/abs/2610.06050)

- **recommendation**：MATE 在 ML10M、Amazon Luxury Beauty、KuaiRec2.0 做完整目录离线 streaming replay，预测先于记忆更新；不是线上曝光试验。

**2610.06047 · Let the Agent Do It? How Software Practitioners Understand and Make Permission Decisions in Agentic AI Assistants**

[论文](https://arxiv.org/abs/2610.06047)

- **agent**：从业者权限决策访谈/调查，非算法。
  核查位置：Title and complete abstract

**2610.06039 · MercerFlow: Flow Matching in a Kernel-Induced Latent Space for Probabilistic Forecasting**

[论文](https://arxiv.org/abs/2610.06039)

- **foundation-model**：MercerFlow针对概率时序预测的核潜空间建模，未宣称通用基础模型预训练。

**2610.06025 · Grounded Joint-Attention Other-Play for Zero-Shot Coordination**

[论文](https://arxiv.org/abs/2610.06025)

- **agent**：MATE视觉joint-attention传统MARL，非LLM工具Agent。
  核查位置：Title and complete abstract

**2610.06019 · Adaptive Expert Guidance for Efficient On-Policy Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.06019)

- **agent**：PPO learner/expert控制份额联合学习，传统RL无语言Agent。
  核查位置：Title and complete abstract

**2610.06018 · Investigating Query-Insensitive Behavior in Spatio-Temporal Video Grounding**

[论文](https://arxiv.org/abs/2610.06018)

- **foundation-model**：视频grounding查询不敏感的诊断，无新能力训练算法。

**2610.05961 · Strategic Multi-Agent Learning for Interpretable Action Valuation of All Players in Football**

[论文](https://arxiv.org/abs/2610.05961)

- **agent**：足球球员动态博弈action valuation，非LLM Agent。
  核查位置：Title and complete abstract

**2610.05949 · Technical Report on the Turba Fertilizer Machine Learning Stack in Morocco**

[论文](https://arxiv.org/abs/2610.05949)

- **recommendation**：Turba 是摩洛哥施肥建议函数的代理回归和数据工程，不是互联网搜广推或通用 LLM 算法。

**2610.05874 · Global Communication or Graph-Specific Memory?**

[论文](https://arxiv.org/abs/2610.05874)

- **foundation-model**：静态图Transformer全局共享记忆有效性诊断，非当前基础模型核心算法。

**2610.05863 · CCQ: A Multi-State Child Care Quality Dataset to Support AI for Children's Health Research**

[论文](https://arxiv.org/abs/2610.05863)

- **foundation-model**：CCQ儿童照护质量数据集及预测基准，非基础模型算法。

**2610.05828 · Data-Driven Personas for Survey Simulation: Insights into Simulation Alignment Across Data-Access Regimes**

[论文](https://arxiv.org/abs/2610.05828)

- **agent**：群体persona调查仿真对数据来源敏感性分析。
  核查位置：Title and complete abstract

**2610.05787 · Constraint-Aware Conversational Job Recommendation in Code-Mixed Low-Resource Settings**

[论文](https://arxiv.org/abs/2610.05787)

- **recommendation**：JobCCC/W-SCAR 用 988 标注对话与 22,410 个职位比较离线检索/多目标排序，没有线上部署或 A/B 证据。

**2610.05750 · Beyond Semantic Similarity: Performance and Costs of Agentic Retrieval for Complex Tasks**

[论文](https://arxiv.org/abs/2610.05750)

- **agent**：既有ReAct检索成本/效果研究，无独立新核心机制。
  核查位置：Title and complete abstract

**2610.05699 · Planetary Geospatial Foundation Models for Global Public Health**

[论文](https://arxiv.org/abs/2610.05699)

- **foundation-model**：Google PDFM五项公共卫生下游案例均以已有embedding为固定协变量，不是新基础模型训练算法；原预训练代码专有、下游脚本不公开且多健康数据受限，不能当现成公共evolve执行任务。
  复现边界：部分US v0 embedding公开，其余研究申请；不能将公共教程误称完整论文复现源码。
  核查位置：§1–2/Table1；§4 Methods/PDFM Embeddings；Data Availability；Code Availability

**2610.05690 · Errors of LLM-Assisted Literature Retrieval in Environmental Science: A Comparison Study of Abstract versus Full-text Based Prompts**

[论文](https://arxiv.org/abs/2610.05690)

- **foundation-model**：环境科学文献检索错误比较，不提出新基础模型方法。

**2610.05681 · Automatic Speech Recognition for Low-Resource Sinhala: A Critical Review of Methods, Challenges, and Future Directions**

[论文](https://arxiv.org/abs/2610.05681)

- **foundation-model**：僧伽罗语ASR综述，无原始核心算法。

**2610.05670 · Generate What You Can Trust: Content Credibility in Generative Recommenders**

[论文](https://arxiv.org/abs/2610.05670)

- **recommendation**：CreGR 的证据为 PolitiFact/GossipCop/MHMisinfo 公共标签数据离线实验；正文承认更大规模评估仍待进行，未达到工业内容审核准入。

**2610.05600 · An LLM-in-the-loop RL Framework for Bioinformatics Feature Selection**

[论文](https://arxiv.org/abs/2610.05600)

- **post-training**：RL用于生物特征选择，LLM提供建议和奖励但不更新LLM策略本身。
- **agent**：LLM为bioinformatics feature selection的DQN提供soft行动建议和validation+知识奖励，策略为传统select/skip DQN，核心为领域特征筛选而非LLM后训练或通用Agent新机制。
  复现边界：允许T=5d重复探索；标签应仅train/validation，下游test独立。公开数据名称不等于可复建split，未报告独立seed/源码；GPT4o生物建议非真实医学验证。
  核查位置：§2–4；Experimental Evaluation

**2610.05591 · What Is a Repeated Token Worth? The Scaling Geometry of Multi-Epoch Pretraining**

[论文](https://arxiv.org/abs/2610.05591)

- **foundation-model**：属于重复预训练经验缩放/数据排列研究，具体重分词干预直接采用既有BPE-dropout；不另建新算法adapter，可作为重复次数选择/数据预算审计的支撑文献。
  复现边界：frontier是拟合曲面不是额外isoFLOP实测；无weightdecay/dropout配方，常数不能外推frontierLLM；BPE改变token数所以同bytes未必同FLOPs；不把lawanalysis当已验证通用选择器。
  核查位置：§3 Eq1–2；§4.1–4.4 Eq3–5；§6.2–6.3；§7 Limitations

**2610.05569 · Factoriax: A GPU-Accelerated Factorio-Style Simulator for Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.05569)

- **agent**：Factoriax工厂JAX模拟器与PPO基准，不是LLM Agent。
  核查位置：Title and complete abstract

**2610.05501 · Logic-Logit: A Logic-Based Approach to Choice Modeling**

[论文](https://arxiv.org/abs/2610.05501)

- **recommendation**：Logic-Logit 用列生成和 Frank-Wolfe 拟合规则，实验是合成数据、2013 Expedia Kaggle 与 MIMIC-IV 离线选择预测；不含线上随机对照。

**2610.05463 · Human-Like Attention? A Psychophysical Comparison of Visual Search in Humans and MLLMs**

[论文](https://arxiv.org/abs/2610.05463)

- **foundation-model**：人类与MLLM视觉搜索心理物理比较，属于认知评测。

**2610.05461 · AI Safety via Debate is Compromised by Cognitive Biases**

[论文](https://arxiv.org/abs/2610.05461)

- **agent**：人类辩论裁决认知偏差实验，无新Agent策略。
  核查位置：Title and complete abstract

**2610.05446 · Hierarchical Time-aware Bootstrapping for Off-Policy Subgoal Value Learning**

[论文](https://arxiv.org/abs/2610.05446)

- **post-training**：HIRO类AntFall层次控制的off-policy subgoal value learning，无语言模型后训练。

**2610.05413 · A Strong Baseline for Evaluating Vision Encoders in Multimodal Large Language Models**

[论文](https://arxiv.org/abs/2610.05413)

- **foundation-model**：RAVEL视觉编码器评价指标，非基础模型能力新算法。

**2610.05400 · CASE: Cost-Aware Stopping for Efficient Long-Video Agents**

[论文](https://arxiv.org/abs/2610.05400)

- **foundation-model**：CASE长视频agent停止决策，由agent track审查。

**2610.05369 · AutoDP-LLM: Automating Data Pre-processing for Intrusion Detection Systems using Large Language Models**

[论文](https://arxiv.org/abs/2610.05369)

- **agent**：AutoDP-LLM为IDS生成受约束preprocessing代码，host固定budget/selection、semantic-RF-MI特征筛选和resampling；主要是领域数据工程应用，未提供通用Agent策略或新的LLM训练算法。
  复现边界：train-only profiler/validation选择冻结test为正确边界；多个backbone可执行pipeline非Agent能力通用提升。HPC并行仅未来工作，不能宣称实现。
  核查位置：§III；§IV；Appendix A/B prompts

**2610.05329 · Understanding the Weight Averaging Mechanism in LLM Training for Post-Training Quantization**

[论文](https://arxiv.org/abs/2610.05329)

- **post-training**：预训练权重平均与PTQ的理论和kernel，属于基础模型量化。

**2610.05306 · Kinematics-Centric Continuous Sign Language Retrieval with Gloss-Guided Boundary-Aware Alignment**

[论文](https://arxiv.org/abs/2610.05306)

- **foundation-model**：手语运动学文本检索与gloss对齐，属于专用手语理解模型。

**2610.05305 · Characterizing Parallelism Strategies in LLM Inference: Fundamental Compute-Communication Trade-offs**

[论文](https://arxiv.org/abs/2610.05305)

- **foundation-model**：主要是现有tensor/pipeline/hybrid并行的分析与8×A100测量，没有新的可执行训练/模型/调度算法，本轮不新增论文adapter，可作为系统性能背景。
  复现边界：单机8GPU NVLink固定ISL1000/OSL200，无法在单卡A100证明同样并行收益；正文vLLM0.15.0与表0.15.1不一致。理论prefill/decode结论不能当作所有batch/网络的定律。
  核查位置：§2 TP/PP/HB analytical model；§3.1/3.4；Table2/Figure8–9

**2610.05292 · Erased, Rerouted, or Rescaled? Post-Training and the Causal Quotient of a Language Model's Belief State**

[论文](https://arxiv.org/abs/2610.05292)

- **foundation-model**：后训练信息擦除/路由/缩放是机制理论与因果解释，未形成独立通用任务评测。
- **post-training**：分析post-training对belief state的抹除/重路由/缩放及KL保护，非新训练算法。

**2610.05265 · Loopy: Low-Bit Quantization Framework for Looped Language Models**

[论文](https://arxiv.org/abs/2610.05265)

- **post-training**：循环模型低bit PTQ及校准预算分配，无RL/OPD。

**2610.05249 · ArticuTable: Generating Instance-Level Interactive Rigid-Articulated 3D Tabletop Scenes from a Single Image**

[论文](https://arxiv.org/abs/2610.05249)

- **foundation-model**：ArticuTable单图交互3D桌面场景重建，为专用场景资产生成系统。

**2610.05220 · Ranking Bandits for Carousel Interfaces with Observable Browsing Depth**

[论文](https://arxiv.org/abs/2610.05220)

- **recommendation**：OD-ranking bandit 用 RecGaze 日志标定的模拟评价；正文明确真实在线评估为后续工作，不能把算法中的 online learning 当线上 A/B。

**2610.05200 · Learning without Overwriting: A Theory of Self-Distillation and Supervised Fine-Tuning in Continual Reasoning**

[论文](https://arxiv.org/abs/2610.05200)

- **post-training**：OPSD/SFT持续推理的DAG理论解释，摘要未给出新的训练方法。

**2610.05131 · RoMod: Temporal Routing Modulation via Mixture-of-Experts for Video Anomaly Detection**

[论文](https://arxiv.org/abs/2610.05131)

- **foundation-model**：RoMod利用MoE路由特征检测视频异常，主要是专用异常检测头。

**2610.05129 · Representation--Behavior Alignment for Explainable Weakly-Supervised Video Anomaly Detection**

[论文](https://arxiv.org/abs/2610.05129)

- **foundation-model**：RBA少量注意力层适应专用视频异常检测，非通用基础模型能力路径。

**2610.05125 · Bayesian Entropy-based Reordering for Calibrated Diffusion Language Models**

[论文](https://arxiv.org/abs/2610.05125)

- **post-training**：BayesER为后验不确定性引导扩散推理token提交，无adapter训练。

**2610.05114 · Belief-Trajectory Energy: Measuring the Path to a Prediction**

[论文](https://arxiv.org/abs/2610.05114)

- **foundation-model**：BTE层间信念轨迹能量用于难度和生成来源识别，主要解释性度量。

**2610.05111 · InstMoE: Adaptive Multimodal Routing with Specialized Experts**

[论文](https://arxiv.org/abs/2610.05111)

- **foundation-model**：InstMoE以预抽BERT/COVAREP等特征在CMU-MOSEI/CH-SIMS情感任务训练轻量Transformer，InfoNCE+五个T/A/V/TA/TV dense加权专家，centroid bias初始化。核心是监督情感fusion模型，未适配基础生成模型/通用agent或独立公共评测协议；与本轮foundation算法范围不符。
  核查位置：§3.2–3.3式1–9；§4.1–4.2

**2610.05100 · METRO: Metric-Enhanced Token Routing Operator**

[论文](https://arxiv.org/abs/2610.05100)

- **foundation-model**：METRO神经算子网格/PDE的Mahalanobis路由，非当前基础模型范围。

**2610.05041 · Communication Shapes Collective Inference in Self-Adapting LLM Societies: Evidence from Mafia**

[论文](https://arxiv.org/abs/2610.05041)

- **agent**：Mafia自适应LLM群体通信行为研究，非通用新算法。
  核查位置：Title and complete abstract

**2610.05036 · Characterizing Security Effects of OSS Vulnerabilities in Agent Systems**

[论文](https://arxiv.org/abs/2610.05036)

- **agent**：OSS漏洞在Agent层传播的安全影响诊断，非Agent能力方法。
  核查位置：Title and complete abstract

**2610.05029 · SPACE-CLIPv2: Decoding Local Geometry from Frozen CLIP for Monocular Depth Estimation**

[论文](https://arxiv.org/abs/2610.05029)

- **foundation-model**：SPACE-CLIPv2专用冻结CLIP深度解码器，非通用视觉基础模型训练。

**2610.05009 · Rethinking Tool Design for Agentic RCA: A Controlled Empirical Study**

[论文](https://arxiv.org/abs/2610.05009)

- **agent**：RCA工具抽象/组合受控对照研究，非新算法。
  核查位置：Title and complete abstract

**2610.04977 · Do LLMs Understand Sequential Structure? A Controlled Study of Inference and Generation**

[论文](https://arxiv.org/abs/2610.04977)

- **agent**：RPS/n-gram序列结构能力受控研究。
  核查位置：Title and complete abstract

**2610.04976 · Priced Guidance: Can Language Models Generate Future Research Ideas?**

[论文](https://arxiv.org/abs/2610.04976)

- **foundation-model**：Priced Guidance评估器可见目标，最多研究想法机制诊断，不能作evolve能力提升证据。

**2610.04957 · Trinity: One Differentiable Physics for Training, Refining and Scoring Generative Floorplanners**

[论文](https://arxiv.org/abs/2610.04957)

- **foundation-model**：Trinity芯片floorplanning生成/精化，专用工程优化。

**2610.04893 · SFlexRCA: Lightweight, Scalable, and Flexible Root Cause Analysis for IIoT Edge Systems**

[论文](https://arxiv.org/abs/2610.04893)

- **foundation-model**：SFlexRCA工业IoT传感器根因分析，非基础模型算法。

**2610.04878 · Bounded Reasoning: Cognitive Hierarchy in Human-versus-AI Cyber Defense**

[论文](https://arxiv.org/abs/2610.04878)

- **agent**：人/DQN网络防御认知层次实验，无LLM策略。
  核查位置：Title and complete abstract

**2610.04867 · Greedy Local Learning for Language Model Pretraining: Gaps and Objective Design**

[论文](https://arxiv.org/abs/2610.04867)

- **foundation-model**：正文明确定位为局部学习测量研究而非具体新方法；不单独新增算法adapter，可保留为局部预测/JEV目标设计对照文献。
  复现边界：单seed且token非compute匹配，单GPU模拟stage不能证明分布式吞吐；论文称release但已查正文未见可核官方repo入口；不把memory机制诊断当能力改进。
  核查位置：§3.1–3.4；§4.1–4.5 Tables1–4；§5 Limitations

**2610.04862 · GitSwarm: Decentralized Compounding Inference**

[论文](https://arxiv.org/abs/2610.04862)

- **foundation-model**：GitSwarm持久git记忆多agent推理，由agent track审查。

**2610.04832 · Agent Skill Evolution: How Revisions Affect Coding Agents**

[论文](https://arxiv.org/abs/2610.04832)

- **agent**：SKILL修订对Agent遵守/成本的经验研究，无新算法。
  核查位置：Title and complete abstract

**2610.04802 · Multi-Agent Spectrum Sharing**

[论文](https://arxiv.org/abs/2610.04802)

- **agent**：认知雷达多Agent频谱meta-RL，非LLM Agent。
  核查位置：Title and complete abstract

**2610.04639 · When Talk Isn't Code: Comparing LLM Agents That Simulate and Develop Software**

[论文](https://arxiv.org/abs/2610.04639)

- **agent**：LLM仿真/开发协议安全受控比较，非新方法。
  核查位置：Title and complete abstract

**2610.04636 · Does Neural Complexity Improve Health Misinformation Detection? A Leakage-Controlled Cross-Corpus Benchmark**

[论文](https://arxiv.org/abs/2610.04636)

- **foundation-model**：健康虚假信息架构比较benchmark，非基础模型新算法。

**2610.04589 · StegoMemory: Agentic Memory Acts as Covert Steganographic Channel**

[论文](https://arxiv.org/abs/2610.04589)

- **agent**：StegoMemory多种隐写scheme跨会话风险测量，无新能力策略。
  核查位置：Title and complete abstract

**2610.04569 · From Transformers to Weighted Automata: Towards the Verification of Large Language Models**

[论文](https://arxiv.org/abs/2610.04569)

- **foundation-model**：Transformer到加权自动机的形式验证理论，不是能力训练或推理效率算法。

**2610.04544 · Label Agreement Does Not Measure Authorization**

[论文](https://arxiv.org/abs/2610.04544)

- **agent**：label ontology管线授权/输出完整性审计案例研究，非通用算法。
  核查位置：Title and complete abstract

**2610.04541 · Autonomous Structuring of Radiology Reports Across Modalities at Archive Scale Using an Open-Weight Large Language Model**

[论文](https://arxiv.org/abs/2610.04541)

- **foundation-model**：放射报告档案模板化流水线，专用医疗部署。

**2610.04528 · Quantifying Collusion Among Autonomous LLM Agents: A Statistical Analysis of the Collusion Wiki Incident**

[论文](https://arxiv.org/abs/2610.04528)

- **agent**：Collusion Wiki事件统计分析，非算法。
  核查位置：Title and complete abstract

**2610.04507 · LoRA's Second Descent Extends Beyond Parameter Parity**

[论文](https://arxiv.org/abs/2610.04507)

- **foundation-model**：LoRA rank与双下降噪声实验，主要是经验诊断而非新方法。
- **post-training**：LoRA rank和label noise下double descent现象研究，不是新后训练算法。

**2610.04502 · Localization Lens for Improving Medical Vision-Language Models**

[论文](https://arxiv.org/abs/2610.04502)

- **foundation-model**：医学解剖定位表示、pixel shuffle和DCL改进Med-VQA，专用医疗适应。

**2610.04499 · Homogeneous Semantic Alignment and Hierarchical Expert Routing for Radiology Report Generation**

[论文](https://arxiv.org/abs/2610.04499)

- **foundation-model**：HSA-HER专用放射报告生成网络。

**2610.04494 · DreamTest: World-Model Surrogates for Search-Based Testing of Deep Reinforcement Learning Agents**

[论文](https://arxiv.org/abs/2610.04494)

- **agent**：DreamTest传统DRL world model测试代理，无语言Agent。
  核查位置：Title and complete abstract

**2610.04433 · What Does a Harness Buy? Tokens, Mostly**

[论文](https://arxiv.org/abs/2610.04433)

- **agent**：固定模型harness随机重跑/成本效应研究，无新算法。
  核查位置：Title and complete abstract

**2610.04425 · AgroGround: Multi-Granularity Grounded Recognition in Agriculture**

[论文](https://arxiv.org/abs/2610.04425)

- **foundation-model**：AgroGround农业grounding数据与任务训练，主要专用数据benchmark。

**2610.04424 · On the Trade-off Between Information Loss and Generalization in Sparse Attention**

[论文](https://arxiv.org/abs/2610.04424)

- **foundation-model**：稀疏注意力JS误差/泛化界理论，无提出新能力实现算法。

**2610.04418 · CORE-RL: Confidence-Oriented Reliability Evaluation of Black-Box Reinforcement Learning Policies**

[论文](https://arxiv.org/abs/2610.04418)

- **agent**：CORE-RL黑盒连续控制可靠性评估，不是LLM Agent。
  核查位置：Title and complete abstract

**2610.04413 · Specific Algorithmic Interpretability of Neural Networks: A Case Study on Textures**

[论文](https://arxiv.org/abs/2610.04413)

- **foundation-model**：散射纹理分类的可解释初始化及PAC-Bayes理论，非基础模型。

**2610.04412 · Large Language Models and Augmented Democracy**

[论文](https://arxiv.org/abs/2610.04412)

- **post-training**：数字孪生增强民主的学位综合研究，非明确独立RL/OPD核心算法候选。
- **agent**：Augmented Democracy 是社会政治偏好建模/议会数字孪生领域的论文集合，以开放投票/人口学特征微调和观点代理讨论。
  复现边界：没有本候选池所需的通用 Agent 核心算子/可执行能力改进；政治偏好预测不等于工具/规划/self-evolve 实现，不能为扩大范围硬收录。
  核查位置：Thesis chapters preference prediction/digital twins; normalized p17,25–33,60–61,69–120

**2610.04403 · Saying, Not Knowing: Aggressively GGUF-Quantized Small Language Models Still Write Rare Words They Can No Longer Define**

[论文](https://arxiv.org/abs/2610.04403)

- **foundation-model**：GGUF小语言模型词汇能力量化审计，无新量化算法。
- **post-training**：GGUF低bit模型词义能力测量，属于量化评测。

**2610.04366 · Human Behavior-Informed Crash Scenario Generation with Real-World Crash Priors for Autonomous Vehicle Safety Evaluation**

[论文](https://arxiv.org/abs/2610.04366)

- **agent**：CrashSim多Agent交通生成，LLM仅辅助诊断，核心不是语言Agent。
  核查位置：Title and complete abstract

**2610.04278 · Do RUL explanations hold up? Faithfulness and stability of attributions on C-MAPSS**

[论文](https://arxiv.org/abs/2610.04278)

- **foundation-model**：设备剩余寿命解释性方法审计，专用预测维护应用。

**2610.04272 · Rethinking Self-Distillation for Multi-Teacher Capability Merging**

[论文](https://arxiv.org/abs/2610.04272)

- **post-training**：控制数据和超参比较MOPD/SFT/soft-label及已有merge方法，贡献为公平基线诊断。

**2610.04269 · Self-Reflection Fine-Tuning: Enhancing Agent Security against Prompt Injection Attacks from Failure Experience**

[论文](https://arxiv.org/abs/2610.04269)

- **post-training**：SRFT将失败动作分析成安全思考+动作样本，正文标准负loglikelihood LoRA SFT；数据/安全框架有价值但无新增核心后训练算法。 该决定仅限后训练核心track，Agent方法/数据公共入口由Agent track独立判断，不能据此全局拒绝。

**2610.04263 · Multimodal Dual-Encoder Retrieval for Automated ICD Coding**

[论文](https://arxiv.org/abs/2610.04263)

- **foundation-model**：ICD医疗编码双编码检索及LLM rerank，专用临床应用。

**2610.04168 · Agentic Cognitive Depth: Operational Criteria for Evaluating LLM Agents**

[论文](https://arxiv.org/abs/2610.04168)

- **agent**：Agent认知深度操作标准/诊断提案，无已执行新算法。
  核查位置：Title and complete abstract

**2610.04158 · How RL Reshapes LLM Reasoning: Transferability, Coverage, and Scaling Laws**

[论文](https://arxiv.org/abs/2610.04158)

- **post-training**：RL策略选择、transfer/coverage/scaling理论与测量，未提出新的训练机制。

**2610.04138 · Dual-Scale Relational Graph Transformers for Ecosystem-Aware Fraud Detection**

[论文](https://arxiv.org/abs/2610.04138)

- **foundation-model**：HERMES银行反欺诈图模型，属于工业风险业务而非基础模型track；生产证据应专门审查。

**2610.04133 · Auditing Pairwise Equivalence Judgments: Self-Critique Effects and Diversity Measurement in Multi-Agent Hypothesis Generation**

[论文](https://arxiv.org/abs/2610.04133)

- **agent**：假设等价判定、自我批评和多样性measurement研究。
  核查位置：Title and complete abstract

**2610.04125 · Representational Control over Self-Report & Behavior Coherence in LLM Risk-Taking**

[论文](https://arxiv.org/abs/2610.04125)

- **agent**：风险偏好自报告/行为activation表征对照，主要机制诊断。
  核查位置：Title and complete abstract

**2610.04104 · Where Does the Semantic Gain Come From? A Reproduction and Extension of Semantic Knowledge-driven Contrastive Learning for Long-Tailed Recognition**

[论文](https://arxiv.org/abs/2610.04104)

- **foundation-model**：SKCL复现与预算混淆审计，未建立稳定新算法增益。

**2610.04083 · Self-Propagating Misalignment in LLM Agents, and Why Auditing or Disabling Memory Is Not Enough**

[论文](https://arxiv.org/abs/2610.04083)

- **agent**：memory/文件自传播失配目标的威胁评测，无新防御算法。
  核查位置：Title and complete abstract

**2610.04053 · The Cost of a Hop: Benchmarking NLIP and A2A**

[论文](https://arxiv.org/abs/2610.04053)

- **agent**：NLIP/A2A通信协议延迟对照，不是Agent策略。
  核查位置：Title and complete abstract

**2610.04040 · Agent Policy-Value Audit: Separating Transition Composition from Event Selection in Financial LLM Agents**

[论文](https://arxiv.org/abs/2610.04040)

- **agent**：金融Agent收益的transition composition vs selection统计审计。
  核查位置：Title and complete abstract

**2610.03972 · Probabilistic Algorithms for Ising Machines from Optimization to Generative AI**

[论文](https://arxiv.org/abs/2610.03972)

- **foundation-model**：Ising概率算法与硬件协同设计综述。
- **post-training**：Ising机器概率算法综述，不是新LLM后训练论文。

**2610.03969 · How Do Coding Agents Optimize Software and Report Performance Validation? A Large-Scale Empirical Study of Open-Source Pull Requests**

[论文](https://arxiv.org/abs/2610.03969)

- **agent**：Agent性能PR实践/测量的大规模经验研究。
  核查位置：Title and complete abstract

**2610.03923 · Learning Robust Personalized Prompts for LLM-Driven Sequential Recommendation**

[论文](https://arxiv.org/abs/2610.03923)

- **recommendation**：LRPRec 在 MovieLens/Steam/LastFM 时间切分上报告离线排名；文中 A/B 是提示更改的假设应用场景，并非已经执行的生产实验。

**2610.03830 · Memory-State Critic for Asymmetric Actor-Critic with Application to Vision-Based Pursuit-Evasion**

[论文](https://arxiv.org/abs/2610.03830)

- **agent**：memory-state critic传统视觉追逃RL，无语言Agent。
  核查位置：Title and complete abstract

**2610.03792 · What Do Verifiable Rewards Teach Video-Language Models About Time? A Controlled Multi-Model Study**

[论文](https://arxiv.org/abs/2610.03792)

- **foundation-model**：视频RLVR时间理解控制诊断，由post-training track审查。

**2610.03759 · BridgeCast: Bridging Ocean Wave Forecasts to Reanalysis via Flow Matching with Exogenous Variables**

[论文](https://arxiv.org/abs/2610.03759)

- **foundation-model**：BridgeCast海浪预测偏差流匹配校正，专用科学预测应用。

**2610.03713 · What Should World Models Forget? Stratified Retention for Continual Adaptation**

[论文](https://arxiv.org/abs/2610.03713)

- **foundation-model**：世界模型按不变时间尺度分层保留的观点和度量提议，摘要未提供新训练算法实证。

**2610.03620 · UniIntervene++: An Adaptive Intervention Agent for Efficient Real-World Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.03620)

- **agent**：UniIntervene++ 是机器人SERL任务policy加availability-masked SMDP Double-DQN option调度，选择RL/示范轨迹correction/CodePolicy，并用Adaptive RL Probe估计能力。
  复现边界：五真实机器人任务依赖硬件与示范；scheduler本身经典RL而非通用LLM/Agent学习算法。CodePolicy不足以把整项变成当前文本/软件Agent复现，未来机器人主题可重新评估。
  核查位置：§III、Eq scheduler、§IV.C

**2610.03617 · DEPICT: Scoring Text-to-Image Alignment by Answer Agreement**

[论文](https://arxiv.org/abs/2610.03617)

- **foundation-model**：DEPICT图文一致性评价指标，非基础模型能力算法。

**2610.03604 · Mastering Atari 2600 Games with Discovered Options**

[论文](https://arxiv.org/abs/2610.03604)

- **agent**：Wayfarer Atari深度RL options，无语言Agent。
  核查位置：Title and complete abstract

**2610.03598 · When a Correct Reward Is Not Enough: Diagnosing and Guiding PPO in an Analytically Solved Broker-Trader Game**

[论文](https://arxiv.org/abs/2610.03598)

- **agent**：连续金融broker PPO诊断，非LLM Agent。
  核查位置：Title and complete abstract

**2610.03567 · Writerslogic at the CLEF 2026 SimpleText Track: Multi-Candidate LLM Simplification and Stacked Complexity Spotting**

[论文](https://arxiv.org/abs/2610.03567)

- **foundation-model**：CLEF SimpleText系统参赛报告，领域prompt选择与NLI适应。
- **post-training**：SimpleText共享任务系统：候选重排与DeBERTa NLI微调，无新LLM策略算法。

**2610.03529 · Divergence controls entropy in distillation**

[论文](https://arxiv.org/abs/2610.03529)

- **foundation-model**：蒸馏散度控制熵的理论/实证分析，后训练track可审，不是新基础架构。
- **post-training**：蒸馏divergence对entropy影响的理论与控制实验，未提出独立新训练方法。

**2610.03502 · Certified Mechanistic Edits: Behavioral Guarantees for Skill Removal and Preservation**

[论文](https://arxiv.org/abs/2610.03502)

- **foundation-model**：小网络连续输入域技能删除形式验证，不属于基础模型规模能力算法。

**2610.03480 · Metropolis-Hastings Dominates Importance Resampling for Policy Composition**

[论文](https://arxiv.org/abs/2610.03480)

- **post-training**：MH对比importance resampling的policy composition推理采样理论，不更新LM。

**2610.03468 · A Vision-Language Model (VLM)-based Pipeline for End-to-End Procedural Modeling of Field-Grown Maize from Point Clouds**

[论文](https://arxiv.org/abs/2610.03468)

- **foundation-model**：玉米点云程序化重建，专用农业几何流水线。

**2610.03463 · Generalization of Transformer-Based Neural Quantum States via In-Context Learning**

[论文](https://arxiv.org/abs/2610.03463)

- **foundation-model**：Transformer量子态ICL泛化理论，非当前基础模型范围。

**2610.03454 · Measure Less, Know More: Self-Supervised Test-Time Feature Acquisition**

[论文](https://arxiv.org/abs/2610.03454)

- **post-training**：RL用于测试时模态获取策略，目标为任意foundation表示，非LLM后训练机制。

**2610.03445 · Corrupted but Correct: Why Vision-Language Models Lie to Themselves Internally**

[论文](https://arxiv.org/abs/2610.03445)

- **foundation-model**：VLM攻击训练/推理落差的机制诊断，无新的能力方法。

**2610.03369 · Mixture-of-Experts for Cryptocurrency Order Execution: Training Stability, Tail Risk, and Failure Modes**

[论文](https://arxiv.org/abs/2610.03369)

- **post-training**：加密货币订单DDQL/MoE多seed控制研究，无语言模型训练。

**2610.03289 · Architecture-Dependent Fusion Pathways in MLLMs**

[论文](https://arxiv.org/abs/2610.03289)

- **foundation-model**：MLLM跨层融合表征诊断，未提出新能力算法。

**2610.03220 · Evolving Hybrid Quantum-Classical Architectures for Image Classification**

[论文](https://arxiv.org/abs/2610.03220)

- **foundation-model**：量子经典电路架构搜索图像分类，不属当前基础模型范围。

**2610.03215 · StanceEval 2026: The Second Stance Detection Shared Task**

[论文](https://arxiv.org/abs/2610.03215)

- **foundation-model**：StanceEval阿语立场检测共享任务概览。

**2610.03193 · Bridging Research and Practice: A Systematic Evaluation of Generalist and Dermatology-Specific Models in Clinical Skin Lesion Classification**

[论文](https://arxiv.org/abs/2610.03193)

- **foundation-model**：皮肤病模型的系统临床benchmark，无新方法。

**2610.03187 · Lightweight and Resource-Efficient Perception for Robotic Guide Dogs**

[论文](https://arxiv.org/abs/2610.03187)

- **foundation-model**：机器导盲犬360相机/LiDAR感知系统，专用应用。

**2610.03185 · Gains and Collapse in On-Policy Distillation:A Reinforcement Learning Perspective**

[论文](https://arxiv.org/abs/2610.03185)

- **post-training**：OPD收益/崩溃机制分析，缓解为截断响应loss mask和既有SFT warmup，保持原优化配方；不是独立新核心算法，但是ResOPD等复现的重要风险证据。

**2610.03141 · Behavior Pack Optimization for Video MLLM Post-Training**

[论文](https://arxiv.org/abs/2610.03141)

- **foundation-model**：BPO视频MLLM反事实行为包RL，由post-training track审查。

**2610.03136 · Investigating the Role of Reasoning-Language Alignment in Monolingual Retrieval-Augmented Generation**

[论文](https://arxiv.org/abs/2610.03136)

- **agent**：德语RAG推理语言对照，非新核心算法。
  核查位置：Title and complete abstract

**2610.03112 · Building Interpretable Feature Representations for Resume-Vacancy Matching by Distilling Production LLM Signals**

[论文](https://arxiv.org/abs/2610.03112)

- **foundation-model**：招聘匹配蒸馏上线系统，属recommendation工业应用，非foundation；生产反馈一致率不是AB。

**2610.03109 · Emergent Structure in the Marginal Attention Space of Language Models**

[论文](https://arxiv.org/abs/2610.03109)

- **post-training**：marginal attention结构与KV eviction预算，属于推理/基础模型。

**2610.03098 · Predictor-Guided Latent Space Codon Optimization for Maximizing Protein Expression**

[论文](https://arxiv.org/abs/2610.03098)

- **foundation-model**：mRNA密码子潜空间优化专用生命科学设计。

**2610.03057 · When Does Synthetic Relational Data Teach Models to Use Relations? Tracing Predictive Structure from Pretraining Data to Model Behavior**

[论文](https://arxiv.org/abs/2610.03057)

- **foundation-model**：四种合成关系数据对模型行为的归因诊断，未提出新核心训练方法。

**2610.03033 · When Numbers Start Talking: Numerical Signalling and Strategic Behaviour Among LLMs**

[论文](https://arxiv.org/abs/2610.03033)

- **agent**：数值消息/自然语言战略博弈行为研究。
  核查位置：Title and complete abstract

**2610.03016 · From Expression to Reaction: Role-aware Visual Transfer and Stimulus-guided Reasoning for Interlocutor Emotion Recognition**

[论文](https://arxiv.org/abs/2610.03016)

- **foundation-model**：对话情绪识别比赛专用视觉迁移/边界推理。

**2610.03010 · Engineering Sustainable Agents: A Systematic Comparison of Agentic LLMs for Developer Workflows**

[论文](https://arxiv.org/abs/2610.03010)

- **agent**：开发Agent能耗/延迟/效果配置对照研究。
  核查位置：Title and complete abstract

**2610.02974 · From Language Priors to Field Adaptation: Preference Learning for Traversability Estimation**

[论文](https://arxiv.org/abs/2610.02974)

- **foundation-model**：机器人可通行性偏好学习，专用地形估计。

**2610.02957 · Understanding Trajectory Heterogeneity in Federated World Model Learning**

[论文](https://arxiv.org/abs/2610.02957)

- **foundation-model**：联邦临床世界模型轨迹异质性benchmark，专用诊断。

**2610.02910 · Frequency Is Not Sensitivity Identifying Safety-Sensitive Experts in Sparse MoE LLM**

[论文](https://arxiv.org/abs/2610.02910)

- **foundation-model**：安全敏感MoE专家抑制攻击/诊断，非能力增强算法。

**2610.02886 · Misinformation Without Triggers: From Factual Answers to Downstream Decisions**

[论文](https://arxiv.org/abs/2610.02886)

- **post-training**：无trigger数据投毒对事实与下游决策影响的控制评测，不是后训练方法。

**2610.02847 · Turnover-Orthogonal Credit Assignment for Open-Team Multi-Agent Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.02847)

- **agent**：TOCA开放团队传统MARL信用分解，无语言Agent。
  核查位置：Title and complete abstract

**2610.02839 · To Explore The Strange New World Beyond Data Distribution: System Behavior, Causality Tax, and Non-causal Base Model**

[论文](https://arxiv.org/abs/2610.02839)

- **foundation-model**：SBD/GSH目前是lazy-training NTK谱的理论概念验证，作者明确无端到端语言模型能力实证；不新增基础模型/evolve算法adapter。
  复现边界：非因果shell依赖启发式重归一与block执行；NTK谱SNR不能代替语言建模准确率或证明普遍causality tax。保留理论背景，不把未来backprop-free设想写成已验证训练算法。
  核查位置：§5.2–5.3；§6.1–6.2

**2610.02819 · Text-Centric Post-Training for Omni-Modal Reasoning**

[论文](https://arxiv.org/abs/2610.02819)

- **post-training**：Text-centric Omni是文本/多模态数据与SFT/RL配方系统研究，梯度正交仅诊断，未提出新核心optimizer；保留训练范式结论而不新增适配器。

**2610.02766 · Exact Memory-Time Optimization for Prefix-Cached Language Model Serving**

[论文](https://arxiv.org/abs/2610.02766)

- **post-training**：prefix缓存timeout最小割/closure优化，纯serving系统算法。

**2610.02755 · FiberGeoText: A Vision-Language Model for Population- Level Organization of Superficial White Matter**

[论文](https://arxiv.org/abs/2610.02755)

- **foundation-model**：FiberGeoText脑白质纤维聚类专用医疗模型。

**2610.02744 · EpiWorld: Grounding LLM Policy Agents in Epidemiological World Models**

[论文](https://arxiv.org/abs/2610.02744)

- **post-training**：EpiWorld模拟器counterfactual与技能经验记忆，不是明确LLM参数后训练。
- **agent**：EpiWorld图流行病worldmodel+protocol/skill/lesson库，teacher按失败事件提炼并supersession替换，非参数RL；51州真实回顾数据与两SEIR模拟，所有policy共用同worldmodel，独立mechanistic重执行仍非真实干预因果证据。跨疫情lesson不可迁移、ensemble区间欠离散。新增模型/规则高度疾病域特定，未形成通用Agent核心机制或公共通用评测新增。
  核查位置：§3.2–3.5；§4.1–4.2；§5.2；Limitations

**2610.02702 · Silent Dissent: LLM Agents That Yield to the Majority Still Represent Their Original Premise**

[论文](https://arxiv.org/abs/2610.02702)

- **agent**：从众后隐藏bridge仍存在的J-lens表征诊断，非成熟新策略。
  核查位置：Title and complete abstract

**2610.02659 · Distributed Learning with Selective State Space Models: Architecture-Aware Convergence Analysis**

[论文](https://arxiv.org/abs/2610.02659)

- **foundation-model**：SSM联邦学习收敛理论与现有算法比较，无新训练算法。

**2610.02654 · Coherence-Driven Belief Formation and Population Dynamics of Contagion in LLM Agents**

[论文](https://arxiv.org/abs/2610.02654)

- **agent**：LLM社会信念传播kernel/群体动力学分析。
  核查位置：Title and complete abstract

**2610.02611 · Scale-Recursive Rectified Flows for Few-Step Precipitation Ensembles**

[论文](https://arxiv.org/abs/2610.02611)

- **foundation-model**：降雨场尺度递归flow采样，专用气象模型。

**2610.02610 · Seer: Maximum Likelihood Regression for Learning-Speed Curves**

[论文](https://arxiv.org/abs/2610.02610)

- **recommendation**：Seer 是 1995 年 UIUC 博士论文的晚上传，研究经典分类器学习曲线；不能按 2026 arXiv 编号称为新 LLM 方法。

**2610.02600 · When History Misleads: Asymmetric Margin Supervision for Instruction-Guided LLM Generative Recommendation**

[论文](https://arxiv.org/abs/2610.02600)

- **recommendation**：Meta AIMS 保留完整历史，以删除反事实形成仅更新竞争项的非对称 margin 监督。六 backbone、私有日志与 Qilin/KuaiSearch-Lite 的 Recall/NDCG 全为离线；生产 SID/生产日志不是线上部署实验。已读方法、结果、结论和附录，未找到 A/B 或全量发布效果，故不满足工业准入。

**2610.02554 · Test-time Multi-agent Coordination by Decomposed Value Gradient Flow**

[论文](https://arxiv.org/abs/2610.02554)

- **post-training**：SCOUT为offline MARL生成先验和SVGD action refinement，不是语言模型后训练。
- **agent**：SCOUT flow prior/SVGD传统offline MARL，不是LLM Agent。
  核查位置：Title and complete abstract

**2610.02513 · From Fragments to Global Maps: Learning Vectorized Map Aggregation with Large Language Models**

[论文](https://arxiv.org/abs/2610.02513)

- **foundation-model**：MapMergeLLM道路矢量图聚合，专用自动驾驶地图任务。

**2610.02507 · MeshQuery: Agentic Seam Planning for UV Parametrization**

[论文](https://arxiv.org/abs/2610.02507)

- **foundation-model**：MeshQuery三维网格UV展开agent，由agent track审查。

**2610.02497 · LiteEMG-FM: An Efficient and Deployable Foundation Model for Robust EMG Sensing**

[论文](https://arxiv.org/abs/2610.02497)

- **foundation-model**：LiteEMG-FM 是 8M EMG 频谱掩码自编码 CNN/Transformer，覆盖跨用户电信号任务与 ESP32 部署；并非本次基础 LLM/VLM 范围。
  复现边界：不因名字含 foundation 就纳入通用大模型；其训练统计与零校准指标是专用传感器任务。
  核查位置：§4.1–4.3; §5.1–5.9; §6

**2610.02486 · From Retrieval to Typed Decisions: Calibrated System One Models from Biomedical Sentence Encoders**

[论文](https://arxiv.org/abs/2610.02486)

- **post-training**：生物sentence encoder转typed-decision模型和RLCD诊断，主要架构/校准研究。

**2610.02466 · SD-DPC: Sparse Dictionary Differentiable Predictive Control**

[论文](https://arxiv.org/abs/2610.02466)

- **post-training**：SINDy字典稀疏非线性控制policy，不涉及LM。

**2610.02452 · Reinforcement Learning Techniques for the Optimization of Target Polarization in Nuclear Physics Scattering Experiments**

[论文](https://arxiv.org/abs/2610.02452)

- **agent**：核物理极化GP surrogate与传统RL控制，无语言Agent。
  核查位置：Title and complete abstract

**2610.02451 · A Simulation-Grounded Agentic VLM Framework for Wildfire Monitoring and Reporting**

[论文](https://arxiv.org/abs/2610.02451)

- **foundation-model**：野火监控仿真与多模态记忆agent，专用应用由agent track审查。

**2610.02442 · AI-driven Thermal-aware Data Center Capacity Planning**

[论文](https://arxiv.org/abs/2610.02442)

- **foundation-model**：数据中心热感知容量规划CFD替代器，非基础模型核心算法。

**2610.02432 · Evaluating and Improving the Robustness of Large Language Models to Input Sequence Variations**

[论文](https://arxiv.org/abs/2610.02432)

- **agent**：Agent相关正文是MCPSec/MCPBench与AttestMCP固定权限表+HMAC、CommitBoundary容器/静态检查/输出验证，§5.3明确沿用2025前作[11]（arXiv2601.17549）。847案例及ASR53.7→12.4为组合安全工程评估，无本轮独立新Agent算法/新公共入口；HMAC只保完整性不授权，允许参数内恶用仍通过。按重复综合工程而非仅benchmark无loss排除。
  核查位置：Title and complete abstract

**2610.02386 · Social bot detection in the age of ChatGPT: Challenges and opportunities**

[论文](https://arxiv.org/abs/2610.02386)

- **foundation-model**：社交机器人检测综述，无新基础模型算法。

**2610.02376 · Coco: An Agentic Copilot for the Hardware--Software Co-Design Lifecycle**

[论文](https://arxiv.org/abs/2610.02376)

- **agent**：Google/Google DeepMind与MIT的Coco已有TPU架构师日常部署，但正文仅系统设计和两个case study，未提供可复核算法benchmark/量化对照；不通过本轮独立复现门槛，保留高优先部署研究线索。
  复现边界：2× time-to-simulation/time-to-insight是明确headline target，不是实测提升；无A/B、无对照实验表，未发现代码或数据发布链接。
  核查位置：全文§1–6；§3四层stack；§4 Early experience；§5.1–5.2两个案例

**2610.02375 · EviDent-CBCT: Evidence-Bottlenecked Report Generation from Dental CBCT under Non-Exhaustive Report Supervision**

[论文](https://arxiv.org/abs/2610.02375)

- **foundation-model**：牙科CBCT报告离散证据瓶颈，专用医疗应用。

**2610.02369 · Automating the Application of HCI Principles: Skills for On-Demand UI Construction, the Human-AI Space to Think, and the Future of HCI**

[论文](https://arxiv.org/abs/2610.02369)

- **agent**：HCI原则作为skills的研究议程/概念框架，无实际新算法评测。
  核查位置：Title and complete abstract

**2610.02320 · DeskForge: Dense Supervision from Desktop Environments for Computer-Use Agents**

[论文](https://arxiv.org/abs/2610.02320)

- **foundation-model**：DeskForge桌面交互数据与benchmark，agent track范围。

**2610.02284 · Effects of interpulse-interval variation on deep-learning classification of bat vocalizations**

[论文](https://arxiv.org/abs/2610.02284)

- **foundation-model**：蝙蝠物种声学分类时间间隔因素实验，非基础模型算法。

**2610.02270 · Reliability Stress Tests and Decision-Time Routing for Chest X-ray Vision-Language Models**

[论文](https://arxiv.org/abs/2610.02270)

- **foundation-model**：胸片VLM可靠性压力测试与多agent路由，专用医疗评测。

**2610.02267 · Fast Models, Slow Evidence: A Paired and Self-Audited Evaluation of System-1 Decision Models for LLM Agent Harnesses**

[论文](https://arxiv.org/abs/2610.02267)

- **agent**：Laya/Jev System1决策模型成对评测及自审，非新模型。
  核查位置：Title and complete abstract

**2610.02247 · Toward Controlling Biology with Language:Offline Learning of Prompt-Conditioned Interventions for Cells, Organoids, and Biobots**

[论文](https://arxiv.org/abs/2610.02247)

- **foundation-model**：既有生物干预档案的语言检索与离线映射应用，无通用基础模型算法。

**2610.02189 · Generative modeling of intrinsically disordered protein regions by reinforcing sparse autoencoder features**

[论文](https://arxiv.org/abs/2610.02189)

- **post-training**：蛋白IDR专用LM及SAE功能控制，非本track的通用LLM RL/OPD能力方向。

**2610.02181 · OmniSeek: Native Tool Integration for Multi-turn Audio-Visual Reasoning**

[论文](https://arxiv.org/abs/2610.02181)

- **foundation-model**：OmniSeek多轮视听主动搜索工具策略与RL训练，由agent track审查。

**2610.02173 · Every Ablation Is a Dose: Counterweights and the Semblance of Self-Repair**

[论文](https://arxiv.org/abs/2610.02173)

- **post-training**：组件ablation的self-repair因果解释，非后训练算法。

**2610.02159 · When Do Intrinsic Rewards Lead to Exploration?**

[论文](https://arxiv.org/abs/2610.02159)

- **agent**：intrinsic reward反事实信息探索理论，非LLM策略。
  核查位置：Title and complete abstract

**2610.02144 · Faynt: Scaling and Optimizing Policies for Competitive Melee**

[论文](https://arxiv.org/abs/2610.02144)

- **foundation-model**：Faynt针对SmashBros游戏的专用RL策略，非通用基础模型算法。

**2610.02142 · Keyword Harnesses Fail Open: A Cheap Diagnostic Ladder for Tool-Use Claims in Small Language Models**

[论文](https://arxiv.org/abs/2610.02142)

- **foundation-model**：关键词harness安全诊断与修补实验，核心为agent诊断。

**2610.02074 · Homomorphic Advantage Operator: Stabilizing Reinforcement Learning Under Fully Homomorphic Encryption Constraints**

[论文](https://arxiv.org/abs/2610.02074)

- **agent**：FHE约束传统RL homomorphic advantage算子。
  核查位置：Title and complete abstract

**2610.02045 · Form and Void: Entangled Composition through an Autonomous AI Agent**

[论文](https://arxiv.org/abs/2610.02045)

- **foundation-model**：FaV-A多阶段图像构图agent，无新可训练基础模型机制。

**2610.02038 · Mimir: Physics-Grounded LLM Agents for Long-Horizon Irrigation Control**

[论文](https://arxiv.org/abs/2610.02038)

- **agent**：Mimir以固定水量物理模拟+候选格点/lex选择/投影shield保护LLM建议，ACE事件记忆只改context。19cropyears6938days/4环境时序60/40、九季memory冻结test；repair消融109.1→180.5cost但各消融不同slice不能横比。核心是灌溉特定ACE+MPC/运行时保障组合，未提出本库待补的通用学习/搜索机制或公共通用评测入口。
  核查位置：Title and complete abstract

**2610.02021 · Task-Adaptive Grounded 3D-Programmers Using 2D VLMs**

[论文](https://arxiv.org/abs/2610.02021)

- **foundation-model**：3D-Prog冻结2D VLM的坐标框架与反馈编程，agent track范围。

**2610.02015 · On Language Drift during RLVR Post-Training**

[论文](https://arxiv.org/abs/2610.02015)

- **post-training**：语言漂移的RLVR理论条件及经验分析，不提出新训练机制。

**2610.02012 · Bellman Meets Lyapunov: Unsupervised Reinforcement Learning via Mastering Chaos**

[论文](https://arxiv.org/abs/2610.02012)

- **agent**：F-CIP dynamics内生intrinsic reward传统RL，非语言Agent。
  核查位置：Title and complete abstract

**2610.01999 · From Reasoning Failures to Composable Video Spatial Intelligence**

[论文](https://arxiv.org/abs/2610.01999)

- **foundation-model**：CROSS训练自由几何技能库与空间agent，不是基础模型训练算法。

**2610.01981 · Universal interpolation for deep residual self-attention networks**

[论文](https://arxiv.org/abs/2610.01981)

- **foundation-model**：残差自注意力通用插值数学保证，无可比较的训练算法实证。

**2610.01944 · Anti-Persona: Disrupting Unauthorized Identity Binding and Recognition in Personalized Vision--Language Models**

[论文](https://arxiv.org/abs/2610.01944)

- **foundation-model**：Anti-Persona图像扰动隐私防护，不改变基础模型训练或推理核心。

**2610.01939 · Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens**

[论文](https://arxiv.org/abs/2610.01939)

- **foundation-model**：PyRUA-Lean机器人代码执行与选择性观测harness，agent track范围。

**2610.01894 · A foundation for systematic analysis of transformers and RNNs for tractography**

[论文](https://arxiv.org/abs/2610.01894)

- **recommendation**：dMRI tractography 的 RNN/Transformer 训练与医学成像验证，不属于当前互联网推荐或通用 LLM 研究范围。

**2610.01882 · Flowing Faster to Coordinate: One-Step Online Multi-Agent Flow Policies**

[论文](https://arxiv.org/abs/2610.01882)

- **agent**：OMAF传统多Agent flow policy，无LLM Agent。
  核查位置：Title and complete abstract

**2610.01846 · Beyond Decodability: Do Acoustic Factors Drive Predictions in Speech-Based Alzheimer's Assessment?**

[论文](https://arxiv.org/abs/2610.01846)

- **foundation-model**：阿尔茨海默语音评估声学干预诊断，无新通用模型算法。

**2610.01835 · Varda-single-1.0: deterministic data-driven weather forecasting at 1 km resolution over Switzerland's complex topography**

[论文](https://arxiv.org/abs/2610.01835)

- **foundation-model**：瑞士区域天气模型工程与验证，非通用基础模型新机制。

**2610.01828 · The Asymptotics of Language Model Alignment with Memory**

[论文](https://arxiv.org/abs/2610.01828)

- **post-training**：Markov生成下best-of-n与KL-RL渐近关系理论，未提出新训练算法。

**2610.01821 · Beyond Linear Concepts: Discovering and Aligning Non-Linear Concept Manifolds in Large Language Models**

[论文](https://arxiv.org/abs/2610.01821)

- **foundation-model**：非线性概念流形解释性分析与CBA度量，无新能力训练算法。

**2610.01766 · VideoEvolve: Evolving Agent Harnesses for Video Temporal Grounding**

[论文](https://arxiv.org/abs/2610.01766)

- **foundation-model**：VideoEvolve演化视频定位agent harness，由agent track审查。

**2610.01754 · Cog-VADU: A Training-Free Cognitive Reasoning Framework for Video Anomaly Detection and Understanding**

[论文](https://arxiv.org/abs/2610.01754)

- **foundation-model**：Cog-VADU训练自由时序提示及重排，专用异常检测agent工作流。

**2610.01746 · End-to-End Learning vs. Modular Architectures: Comparative Insights into Autonomous Driving Systems**

[论文](https://arxiv.org/abs/2610.01746)

- **recommendation**：自动驾驶端到端/模块化架构比较综述与二值决策框架，非当前 LLM/Agent 新训练算法。

**2610.01578 · The hidden advantage of mask resampling: a theory of masked autoencoders**

[论文](https://arxiv.org/abs/2610.01578)

- **foundation-model**：MAE掩码重采样的理论与既有机制解释，摘要未提出新算法。

**2610.01531 · Towards Reliable Vision-Language Models for Autonomous Driving**

[论文](https://arxiv.org/abs/2610.01531)

- **foundation-model**：自动驾驶VLM损坏鲁棒性评估及已有VEA应用，无新核心算法。

**2610.01530 · Calibrating Prediction Timeliness Through Multi-Objective Hyperparameter Optimization for Remaining Useful Life Prediction**

[论文](https://arxiv.org/abs/2610.01530)

- **foundation-model**：剩余寿命预测多目标超参优化，专用预测维护应用。

**2610.01514 · How the Audit Rule Shapes Faithful Factor Explanations in LLMs**

[论文](https://arxiv.org/abs/2610.01514)

- **agent**：解释factor审计规则激励理论/实验，非Agent执行算法。
  核查位置：Title and complete abstract

**2610.01491 · Auditing Web Agent Evaluation on WebArena-Lite: Human Review of Outcomes and Trajectories**

[论文](https://arxiv.org/abs/2610.01491)

- **agent**：WebArenaLite165固定任务、MASM动作分析+memory与proceduralGuide观察性比较；失败human纠正仅GPT非Qwen，25步净+6但pairedp=.392，一次rollout/任务。正文§6承认Guide一例暴露中间答案与一例statecarryover；55.2%有progress且人工audit非新公共自动执行器。不能把guide当无gold策略能力，也未形成有独立新增核心的合格算法/公共评测入口。
  核查位置：Title and complete abstract

**2610.01490 · The Persona Is Still There, but Who Is Speaking? Latent Identity Reversion in Persistent AI Agents**

[论文](https://arxiv.org/abs/2610.01490)

- **agent**：persona system anchor丢失的行为事故/受控研究。
  核查位置：Title and complete abstract

**2610.01451 · A Multi-Agent LLM Framework for Personalized Health Checkup Interpretation and Guidance**

[论文](https://arxiv.org/abs/2610.01451)

- **agent**：健康检查系统29intents/13mapped agents确定路由最多4intent，并行RAG后固定顺序+LLM合成，属于专域工程集成非新通用算法。120韩文compound queries/5合成records且Single限定单intent，比较包含结构性coverage差异；7类仅4类测试，memory/prefilter未评估，非临床安全证据，critical failures15→13.3%类似。
  核查位置：Title and complete abstract

**2610.01389 · AiSearch: Interactive Multi-Modal Search with VLMs**

[论文](https://arxiv.org/abs/2610.01389)

- **foundation-model**：AiSearch交互多模态检索框架利用既有VLM，无新基础模型核心机制。

**2610.01364 · LLM-Driven Multi-Agent Control for Skill-Based Smart Manufacturing**

[论文](https://arxiv.org/abs/2610.01364)

- **agent**：智能制造MCP包装OPCUA、MQTT通信、外部state注入+物理toolmask，比较标准orchestrator/peer/mono三拓扑无新通用规划学习算法。9模拟任务各10run、单Gemma4 31B，成功run条件耗时token；mono/peer93%/orchestrator87%，silentfault子任务相反，不是实厂部署或通用公共评测新增。
  核查位置：Title and complete abstract

**2610.01345 · ARCCS: An Automated Regulatory Compliance Checking System**

[论文](https://arxiv.org/abs/2610.01345)

- **agent**：ARCCS用法规结构分段→原子requirement→scope适用/证据RAG→四标签confidence门槛的人机审查webapp，无新通用优化/规划机制。GDPR三terms文档100requirement、90LLMjudge无deterministicgold；采购100合成trace×12规则是受控sanity非真实法务覆盖。专门监管工具/小合成集不作为通用Agent或evolve公共新增。
  核查位置：§2.1–2.3；§3.1–3.3；§4；§5

**2610.01325 · PPO-HRAP: Proximal Policy Optimization with a Hybrid Regime-Aware Policy for Risk-Controlled Trading**

[论文](https://arxiv.org/abs/2610.01325)

- **agent**：PPO-HRAP金融波动先验混合传统RL，非语言Agent。
  核查位置：Title and complete abstract

**2610.01275 · Know When to Hold 'em: Correct-Token Retention in Uniform-State Diffusion Language Models**

[论文](https://arxiv.org/abs/2610.01275)

- **post-training**：USDM correct-token retention辅助loss属于扩散模型预训练/架构训练，转基础模型。

**2610.01257 · Science Utopia? Closed-Loop LLM Simulation of Academic Research Ecosystems**

[论文](https://arxiv.org/abs/2610.01257)

- **agent**：Suto模拟10年学术生态：研究者从当年可得SciEvo真实论文选择artifact而非实际开展科研，三reviewer均分+定额accept，grant rank与预算淘汰构成闭环。5000researcher worlds研究制度仿真，topic探索/资金等结果由建模机制驱动，非新通用Agent优化或真实科研能力基准。
  核查位置：§2.1–2.2；§3.1–3.4；§5

**2610.01234 · ASCRIBE: Atomic and Significance-Based Reasoning for Thai Clinical SOAP Note Generation**

[论文](https://arxiv.org/abs/2610.01234)

- **post-training**：ASCRIBE原子事实/临床重要性结构化推理、五类领域reward，正文LoRA SFT+标准GRPO；无新增核心优化器或蒸馏机制，归临床应用。

**2610.01195 · Federated Agent Optimization**

[论文](https://arxiv.org/abs/2610.01195)

- **agent**：Federated Agent Optimization问题定义/议程，无实现新算法。
  核查位置：Title and complete abstract

**2610.01184 · ReCast: Contract-Preserving Protection for Fixed-Interface Multimodal Reasoning**

[论文](https://arxiv.org/abs/2610.01184)

- **foundation-model**：ReCast隐私媒体重构与远程解题agent工作流，agent track范围。

**2610.01180 · Skeleton-and-Strategy Prompting: Training-Free Negation Understanding for Vision-Language Models**

[论文](https://arxiv.org/abs/2610.01180)

- **foundation-model**：SSP否定理解检索示例及提示策略，无新可训练核心模型。

**2610.01166 · CineMR: Tool-Integrated Vision-Language Reasoning for Quantitative Cardiac MRI Assessment**

[论文](https://arxiv.org/abs/2610.01166)

- **foundation-model**：CineMR心脏MRI工具使用医学agent，专用应用。

**2610.01102 · MASkillBlender: Decentralized Whole-Body Coordination for Multi-Humanoid Loco-Manipulation via Skill Blending**

[论文](https://arxiv.org/abs/2610.01102)

- **agent**：MASkillBlender多humanoid传统RL技能blending，无LLM策略。
  核查位置：Title and complete abstract

**2610.01093 · OrbitTAMP: Grounding Language Models for Task and Motion Planning in Spacecraft Rendezvous**

[论文](https://arxiv.org/abs/2610.01093)

- **agent**：OrbitTAMP自然语言→partial MissionConfig→行为-时间图枚举/评估→waypoint→SCP；字段已指定则保留，安全来自后级约束优化非LLM。1000test是10%on-grid模块数据且无语言/behaviorselection；最终采用greedywaypoint非学习proposal。航天特定图/动力学TAMP组合，未见可独立通用Agent优化新增。
  核查位置：§III-A–B；§IV-D/E；§V-A/TableIII

**2610.01027 · LawCompass: Navigating from Legal QA to Multi-Agent Deep Research with Grounded Evidence**

[论文](https://arxiv.org/abs/2610.01027)

- **agent**：LawCompass三模式QA/retrieval/deepresearch，LangGraph planner3–5任务、schema修复+固定fallback，executor检索后citationcatalog合成。20query top5人工检索+主观usability，未验证长程法律任务可执行正确性。专门法规RAG/工程路由组合，无新增通用核心算子或公共task/scorer。
  核查位置：§4.1–4.5；§5.1–5.2

**2610.00991 · Adapter Thickets: Splitting an RLVR Budget Beats Concentrating It**

[论文](https://arxiv.org/abs/2610.00991)

- **post-training**：Adapter thickets固定训练/160推理rollout预算，随机分片独立LoRA+标准GRPO再投票，是预算分配/集成实证而非新核心训练loss。

**2610.00988 · Auditable Algebraic Counting Field for Cryptic-Pocket Detection from Apo Structures**

[论文](https://arxiv.org/abs/2610.00988)

- **post-training**：apo蛋白结构cryptic-pocket监督algebraic field，无LM后训练。

**2610.00984 · HADRec: A Hierarchy-Aware Drug Recommendation Framework by Fusing Molecular Knowledge and Electronic Health Record**

[论文](https://arxiv.org/abs/2610.00984)

- **recommendation**：HADRec 是临床药物推荐，在 MIMIC 医疗数据融合分子/EHR 与 ATC 层级，不是当前互联网搜广推；不把医疗离线指标转述为部署。

**2610.00973 · Concept Driven Domain Adaptation: Finding an Abstract Needle in a Haystack**

[论文](https://arxiv.org/abs/2610.00973)

- **foundation-model**：CDDA专用于中学物理概念视频检索，应用域适配而非通用基础模型算法。

**2610.00954 · Beyond Leaderboards: Tokenomics of Agentic Small Language Model Ensembles**

[论文](https://arxiv.org/abs/2610.00954)

- **post-training**：SLM ensemble推理反馈及token/cost评测，无参数后训练。
- **agent**：SLM ensemble tokenomics case study，摘要主张评测而非新核心训练方法。
  核查位置：Title and complete abstract

**2610.00922 · EyeTAG: Eye Trajectory-Aware Gaze Estimation**

[论文](https://arxiv.org/abs/2610.00922)

- **foundation-model**：EyeTAG注视估计专用时序运动先验，非通用基础模型机制。

**2610.00917 · Finding the Right Fit: Model-Harness Interactions across Agent Tasks**

[论文](https://arxiv.org/abs/2610.00917)

- **agent**：66配置对3固定agentbench的model-harness实证，nativepair非必最好但model/context/tool/timeout原生设置不同；一个countedrun任务、infra重跑取last/缺失零，无法识别单组件因果。无新训练/规划方法或新公共任务/执行评分器；轨迹提案未测，不以排名调查作为新增能力候选。
  核查位置：§3.1–3.4；§4.1；§7–8

**2610.00905 · Understanding Issues, Causes and Solutions in Open-Source LLM-based Multi-Agent Systems**

[论文](https://arxiv.org/abs/2610.00905)

- **agent**：开源多Agent issue原因/解决方案经验研究。
  核查位置：Title and complete abstract

**2610.00903 · Sharpen Before You Adapt: Data-Free Entry-State Sharpening for Test-Time Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.00903)

- **post-training**：Entry-state sharpening统一分析SPIRAL、R-Zero和多数一致性伪样本SFT的TTRL准备效果，正文不绑定新算法，仍为现有GRPO与自蒸馏配方。

**2610.00898 · When Do Biological Reasoning Models Use Their Biological Inputs?**

[论文](https://arxiv.org/abs/2610.00898)

- **post-training**：公开bio-mirage干预/冲突评测核实存在，但输入依赖Evo2/蛋白/单细胞等专门生物编码器与KEGG/ChatNT/C2S任务；不是本轮通用LLM后训练或通用Agent评测入口，生物模态方向另列参考。

**2610.00890 · Cross-Benchmark Transfer from RL on Agentic Coding Tasks**

[论文](https://arxiv.org/abs/2610.00890)

- **agent**：KimiK2.7Code rank32LoRA既有GSPO，1700专家repo/terminal任务、pass-to-pass全过gate乘fail-to-pass分数，tooltokensmasked、overlongfiltered，64H200一epoch。六bench/五独立集transfer有实证且finalcheckpoint预固定；部分publicbaseline、TB3trained8infra排除、单recipe无法归因新算法。未提出新增RL/OPD核心或公开1700task执行入口，保留实验参考不纳新实现。
  核查位置：§3.3；§4.1–4.3；§5–6/Table2；§8

**2610.00888 · Match the Distribution, Not the Compute: Post-Training Multi-Token Prediction Heads**

[论文](https://arxiv.org/abs/2610.00888)

- **post-training**：MTP head训练及speculative verification serving控制，转基础模型，不是RL/OPD核心。

**2610.00883 · DeBERTa-ConPara: Attack-Aware and Deployment-Realistic Detection of AI-Generated Text**

[论文](https://arxiv.org/abs/2610.00883)

- **foundation-model**：DeBERTa生成文本检测器Unicode预处理研究，专用检测应用。

**2610.00881 · Machine Translation for Sign Languages**

[论文](https://arxiv.org/abs/2610.00881)

- **foundation-model**：手语机器翻译综述，无新算法。

**2610.00870 · An Educator-Guided LLM Pedagogical Agent for Scaffolded Feedback in Conceptual Database Design**

[论文](https://arxiv.org/abs/2610.00870)

- **agent**：教育ERD四阶段由教师控制披露，LLM选预写问题/模板填槽/后级反馈，episode memory非持续学生模型。63课程学生48完成、383自愿episode，仅186后续artifact，71.1%targetincorporation条件于改图不等正确率；无对照因果学习收益。专域教学部署，无新通用agent核心/可执行公开评测入口。
  核查位置：§3.2–3.4；§4课堂/4.2/4.3；§5

**2610.00852 · Child-Adapted Structured Phonological Representations for Interpretable Speech Sound Analysis**

[论文](https://arxiv.org/abs/2610.00852)

- **post-training**：儿童语音phonological表示适配，非语言模型策略训练。

**2610.00849 · Learning Multiple Timescales for Goal-Conditioned Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.00849)

- **agent**：GITA多timescale传统offline goal-conditioned RL，无LLM Agent。
  核查位置：Title and complete abstract

**2610.00848 · Geometric Similarity in VLM Low-Level Vision Representations**

[论文](https://arxiv.org/abs/2610.00848)

- **foundation-model**：GeoSim多层几何表征相似性解释框架，无新基础模型训练算法。

**2610.00809 · Paying for Too Many Tokens? Valid and Cost-Efficient Multimodal LLM Annotation with Simple Heuristics**

[论文](https://arxiv.org/abs/2610.00809)

- **foundation-model**：视频社会科学标注的采样与网格启发式评估，无新核心模型。

**2610.00795 · Can large language models unlock discrete data in ophthalmic diagnostic reports?**

[论文](https://arxiv.org/abs/2610.00795)

- **foundation-model**：眼科PDF结构化提取20例概念验证，专用医学应用。

**2610.00758 · Scalable Multi-Task Inverse Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.00758)

- **agent**：低秩多任务逆强化学习及状态覆盖理论，非LLM Agent核心控制/记忆/工具算法。
  核查位置：Title and complete abstract

**2610.00705 · Meta-Multi-Agent Reinforcement Learning for Fast Adaptation of Interactive Policies with Applications to Autonomous Driving**

[论文](https://arxiv.org/abs/2610.00705)

- **agent**：Markov games的meta-NE/gradient-play快速适应与自动驾驶策略，非LLM Agent研究方向。
  核查位置：Title and complete abstract

**2610.00694 · How Divergence Becomes Decision Flips in Compressed Language Models**

[论文](https://arxiv.org/abs/2610.00694)

- **foundation-model**：压缩模型TV与决策翻转的测量关系，主要分析非新能力算法。

**2610.00680 · Curvature Under Attack in hZACH-ViT: Gauge Symmetry, Boundary Saturation, and Adversarial Failure**

[论文](https://arxiv.org/abs/2610.00680)

- **foundation-model**：小型ViT曲率与对抗边界饱和诊断，未提出通用基础模型算法。

**2610.00677 · Harnessing Vision-Language Models for Perceptual Quality Assessment and Autonomous Content Adjustment in Augmented Reality**

[论文](https://arxiv.org/abs/2610.00677)

- **foundation-model**：RateAR感知质量benchmark及AR自动调整应用，无新基础模型核心机制。

**2610.00665 · Analysis of Quantized and Efficiently Adapted Protein Language Models**

[论文](https://arxiv.org/abs/2610.00665)

- **foundation-model**：蛋白语言模型现有QLoRA量化适配评估，无新核心算法。

**2610.00654 · When More Data Is Not Enough: The Context-Sufficiency Frontier in Generative AI Personalization**

[论文](https://arxiv.org/abs/2610.00654)

- **recommendation**：家居零售商语境充足性研究明确是两个构造用户、单请求、主模型的 32×10 离线因子实验；有零售商品目录不代表线上 A/B。

**2610.00629 · ASAD: Adaptive Software Agents for Debugging**

[论文](https://arxiv.org/abs/2610.00629)

- **agent**：ASAD主agent依据静态复杂度特征prompt决定simplefix或生成顺序角色，再逐agent最多3修订/全局5迭代；职责/优先级由LLM自由生成，非新增明确优化器。三既有debugbench与100sample5run，testpassing不等correct、223Defects4J人工核验；结尾runtime反馈/多文件协作仍未来。主要标准planner-specialist-review组织组合，不作为新核心算法。
  核查位置：§III-B–D；§IV-C；§V-D；§VII；Conclusion

**2610.00622 · Understanding and Mitigating Library-Related Issues in LLM-Generated Code**

[论文](https://arxiv.org/abs/2610.00622)

- **agent**：Analyzer抽JSON依赖→搜索官方doc/抽imports/snippets→Generator→compile/import+LLMValidator迭代，本质既有library-grounded RAG/selfrefine工程组合。300tasks5models消融有实测但compile不执行logic，自动pip依赖不证明semanticcorrect/安全，检索版本未构新协议；无新算法或独立公共评分器增量。
  核查位置：§IV-A–E；§V；§VI-A/消融

**2610.00619 · Beyond Supra-Competitive Outcomes: Collusive Behaviour in Deep Reinforcement Learning for Optimal Execution Games**

[论文](https://arxiv.org/abs/2610.00619)

- **agent**：金融执行博弈PPO合谋行为与惩罚诊断，非LLM Agent方法。
  核查位置：Title and complete abstract

**2610.00610 · Explainable Suicide Risk Assessment on Social Media with Multi-Task QLoRA**

[论文](https://arxiv.org/abs/2610.00610)

- **post-training**：自杀风险共享任务系统为标准multi-task QLoRA、概率平均/交叉折聚合，领域应用而非通用算法/新增公共评测协议。

**2610.00592 · ALER: Adaptive Learnable Experience Rewriting for Reinforcement Learning**

[论文](https://arxiv.org/abs/2610.00592)

- **foundation-model**：ALER部分可观测RL槽记忆agent，agent track范围。
- **agent**：LSTM+slot memory的传统部分可观测RL经验重写，非LLM Agent方法。
  核查位置：Title and complete abstract

**2610.00590 · Towards Hierarchical Cyber Defense with Large Language Models: From Planning to Execution**

[论文](https://arxiv.org/abs/2610.00590)

- **agent**：Cyberwheel把subnet planner/primitiveexecutor各换PPO或frozenLLM，noisydetector局部观测且同seed20episode100steps；LLM+LLM强模型胜而小模型不稳定。是已有层级控制三配置在专用网络防御sim的实证，单global seed不能泛化鲁棒性，无新增通用训练/规划算子或公共任务定义增量。
  核查位置：§3.2–3.5；§4.1–4.4；§5.1–5.3

**2610.00562 · Can LLMs Reason Over Long Horizons? An Empirical Evaluation of Context Strategies for Longitudinal Clinical Reasoning**

[论文](https://arxiv.org/abs/2610.00562)

- **foundation-model**：MedLoCoMo临床长时上下文策略对比，专用评估。

**2610.00557 · No One Architecture Fits All: A Cross-Environment Evaluation of Hierarchical Red Team Agents**

[论文](https://arxiv.org/abs/2610.00557)

- **agent**：跨CybORG/Cyberwheel比较已有RL+RL及LLM+LLM架构并分析瓶颈，主要评价研究不提出新机制。
  核查位置：Title and complete abstract

**2610.00540 · Assessing the Impact of Language Disparity on Multilingual Linguistic Ability in Large Language Models**

[论文](https://arxiv.org/abs/2610.00540)

- **post-training**：既有MultiBLiMP四读出与101语言对比，贡献为语言知情评测解释，摘要无独立新增benchmark/训练算法。

**2610.00511 · Before Agents Decide: Epistemic Action in LLM-Based Systems**

[论文](https://arxiv.org/abs/2610.00511)

- **agent**：认识性行动的概念分类与设计论证，未呈现实现算法或实验证据。
  核查位置：Title and complete abstract

**2610.00430 · Memetic Trojans: Social Contagions as Carriers of Adversarial Payloads in Agent Networks**

[论文](https://arxiv.org/abs/2610.00430)

- **agent**：社会传播携带对抗payload的漏洞/网络模拟分析，未提供提升Agent核心能力的方法。
  核查位置：Title and complete abstract

**2610.00406 · LLM-as-a-Judge for Low-Resource Languages: Adapting Ragas and Comparative Ranking for Romanian**

[论文](https://arxiv.org/abs/2610.00406)

- **foundation-model**：罗马尼亚语RAG评判策略与benchmark，无新核心模型机制。

**2610.00398 · WIPSNet: Deep Learning for Paediatric Wheeze Detection from Overnight Impedance Pneumography**

[论文](https://arxiv.org/abs/2610.00398)

- **foundation-model**：WIPSNet儿科阻抗呼吸测量专用3D ResNet分类，无通用模型机制。

**2610.00374 · Faithful Chart Generation for Multimodal Deep Research: Frame-Evidence Co-Adaptation**

[论文](https://arxiv.org/abs/2610.00374)

- **foundation-model**：FECA证据自适应图表计划agent工作流，无新基础模型核心算法。

**2610.00367 · MoRA: MoE Pruning via Router Bias Learning and Expert Approximation**

[论文](https://arxiv.org/abs/2610.00367)

- **post-training**：MoRA学习router bias及expert输出仿射近似做MoE剪枝，转基础模型轨道，非全局拒绝。

**2610.00363 · Deep Learning for Anomaly Detection in Railway Systems: A Structured Survey**

[论文](https://arxiv.org/abs/2610.00363)

- **foundation-model**：铁路异常检测结构化综述，无新算法。

**2610.00302 · Decoding the Disaster: Multi-Task Geospatial Reasoning with Vision-Language Models and Crowdsourced Imagery for Disaster Mapping**

[论文](https://arxiv.org/abs/2610.00302)

- **foundation-model**：GRDisaster灾难街景地理定位与损毁严重度，专用领域应用benchmark，暂不接入通用能力任务。

**2610.00256 · Verification Pulses and the Cost of Escaping Wrong Consensus**

[论文](https://arxiv.org/abs/2610.00256)

- **post-training**：binary consensus register的verification-pulse控制理论及LM响应实验，schedule对比区间均含零，未形成独立通用LLM能力训练/评测组件。

**2610.00253 · System Attribution in LLM Brand Recommendations: Single Responses Identify the System, Aggregated Brand Profiles Do Not Transfer**

[论文](https://arxiv.org/abs/2610.00253)

- **recommendation**：研究模型输出归属与品牌偏差审计，不是线上推荐算法；转通用评价审查。
- **foundation-model**：采用已有字符n-gram/随机森林解释特定品牌推荐采集语料，域与harness未交叉且聚合profile跨域失败；非新基础模型算法，分析代码/完整数据仍请求提供，暂无独立公开通用evolve任务。
  核查位置：§1–4；§6.4–6.5；§7；Data Availability/Code Availability

**2610.00223 · A Holistic Assessment of the Carbon Footprint of Noor, a Very Large Arabic Language Model**

[论文](https://arxiv.org/abs/2610.00223)

- **foundation-model**：Noor碳足迹整体评估，无新模型算法。

**2610.00196 · GPEC: Efficient Pre-LLM Gaussian Process Embedding Correction for Cardiac Video Caption Generation**

[论文](https://arxiv.org/abs/2610.00196)

- **foundation-model**：GPEC心脏视频caption的GP残差适配，专用医疗应用。

**2610.00188 · Uncertainty-Aware RL-Controlled Adaptive 3D Mapping**

[论文](https://arxiv.org/abs/2610.00188)

- **agent**：RL调控TSDF体素细分的3D建图策略，非LLM Agent方法。
  核查位置：Title and complete abstract

**2610.00106 · SyntheticHLS: Building Diverse Synthetic High-Level Synthesis Datasets using LLMs**

[论文](https://arxiv.org/abs/2610.00106)

- **foundation-model**：SyntheticHLS硬件综合数据生成与变异agent，无通用基础模型核心训练。

**2610.00096 · FACET at WMT 2026 Automated Translation Quality Evaluation Task**

[论文](https://arxiv.org/abs/2610.00096)

- **post-training**：FACET为WMT共享任务三次固定model prompt分解翻译质量，无训练组件，专门提交报告且无新增通用执行框架。

**2610.00093 · Safety in Self-Evolving Agents: A Survey**

[论文](https://arxiv.org/abs/2610.00093)

- **agent**：自演化Agent安全综述与SAVER分类框架，不是新可复现算法。
  核查位置：Title and complete abstract

**2610.00084 · Scientific Agents: Evaluating Profession-Specific System Prompts on Scientific Tasks**

[论文](https://arxiv.org/abs/2610.00084)

- **agent**：503职业系统prompt的对照评价和成本负结果，无新Agent能力机制。
  核查位置：Title and complete abstract

**2610.00069 · A Framework for Egocentric and Exocentric Procedural Understanding via Temporal Segmentation and Semantic Abstraction**

[论文](https://arxiv.org/abs/2610.00069)

- **foundation-model**：冻结DINOv2/VJEPA2工作事件记忆设计及评估提纲，agent概念框架。

**2610.00047 · Characterizing a Configuration Where Inference-Time PRM-Pruned Fragment Grafting Is Inert: Evidence from Three Reasoning LMs**

[论文](https://arxiv.org/abs/2610.00047)

- **post-training**：PPFG推理fragment grafting特定配置的零效应/等价检验，可作为负结果参考；不新增训练算法或独立通用benchmark。

**2610.00035 · Integrating Fairness and Explainability in a Multiple Instance Reinforcement Learning System**

[论文](https://arxiv.org/abs/2610.00035)

- **post-training**：教育风险RL-MIL与fairness hypernetwork，非语言模型训练/通用LLM评测。
- **agent**：学生风险预测的RL-MIL公平超网络及mode collapse分析，非LLM Agent方法。
  核查位置：Title and complete abstract

**2610.00031 · Seeing the City or Recognizing the Place? What Street-View Imagery Adds Beyond Existing Urban Data in VLM-Based Urban Sensing**

[论文](https://arxiv.org/abs/2610.00031)

- **foundation-model**：街景预测对地理记录依赖的城市数据质量诊断，专用城市感知而非通用评测任务。

**2610.00024 · Encoded but Disconnected: Decomposing Vision-Language Model Failures under a Patching Null**

[论文](https://arxiv.org/abs/2610.00024)

- **foundation-model**：VLM中层patching负结果及oracle标签干预；论文明确非部署方法，不能用于evolve能力提升。
