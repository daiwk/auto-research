# 已确认的 Google/Meta 优先短名单（9）

这 9 项是有原文作者/机构或参与角色证据的优先项，不是全部候选的机构穷尽结论。
没有现有可运行实现/指标匹配；完整实验成本建议与低成本组件机会分别列出。
本轮只核查，不实施、不训练、不改原账本；9项完整实验的成本/来源终态已写在本轮报告，
后续同步原账本与新分类器属于数据修复，而不是重新启动这些完整实验。
成本终态只关闭完整实验，不把尚未实现的低成本组件变成已实现。

## 2610.07289 · Catching Developers in the Flow: Low-Latency Agentic Program Repair at Google Scale

- 机构/角色：一作及全部作者均Google（New York）；官方HTML作者块。
- 作者代码：Data Availability明确无法公开reproduction package或数据；未发现作者源码。
- 可负担对象：可另定公开APR任务上的忠实有界核心：pre/post abstention过滤、真实LLM ReAct generate-and-validate、实际补丁应用/测试执行与时延记录。不能声称内部Google生产复现；尚未证明该独立小实验全部成本。
- 完整实验：完整生产验证依赖私有源码、内部CI/开发工具、内部模型和数百万changes；公共复现不可得，应关闭完整原环境复现而不是无限实施欠账。
- 本轮完整实验终态：私有生产环境不可公开复现，审查 DONE
- 低成本范围建议：保留已有accepted但明确分出公共核心范围再评估；完整Google生产实验不复现（私有资源），不是待GPU队列。
- 证据：[原文](https://arxiv.org/html/2610.07289v1)；逐段定位见 [Google 对账](data/google-review.json)。

## 2610.06616 · Video Encoders Built on Image Representations

- 机构/角色：一作Stanford；DeepMind共同作者仅advisory capacity，不能宣传Google一作论文。
- 作者代码：所读官方HTML未发现论文作者源码仓库；未据此宣称绝对未发布。
- 可负担对象：原文Appendix C.1明确training-free selection-only独立变体：对真实冻结图像encoder特征保留source position，执行question relevance/DPP diversity/cross-frame correspondence的固定token预算选择；不带learned refiner。可先做CPU算法恒等/预算/源位置诊断；真实7B/8B checkpoint小样本需另核资源与GPU门禁，不把随机特征当能力复现。
- 完整实验：Appendix C.3：65K Video-ChatGPT子集、2epochs、8×A100×12h=96GPUh，仅refiner；另三backbone/13benchmark。完整实验成本过高，不复现（建议审查DONE）；低成本selection-only不能被96GPUh统一否定。
- 本轮完整实验终态：成本过高，不复现（审查 DONE）
- 低成本范围建议：关闭完整refiner/全表实验；将selection-only作为明确保真边界的可负担核心候选，未实现。
- 证据：[原文](https://arxiv.org/html/2610.06616v1)；逐段定位见 [Google 对账](data/google-review.json)。

## 2610.00497 · Gumbel Straight Flow: Distilling Autoregressive Models into One-step Flow Maps

- 机构/角色：原文作者脚注：一作工作作为Google DeepMind Amsterdam Student Researcher完成。
- 作者代码：所读官方HTML无作者实现仓库链接；未作全网穷尽未发布断言。
- 可负担对象：可另定小词表/短序列真实AR teacher+flow-map student的L1：posterior Gumbel sampling、单调Gaussianization、diagonal CE与off-diagonal semigroup self-consistency、实际梯度和1-step sampling。必须两个真实训练模型且保留核心损失，不可仅直线插值fixture；该缩小实验仍未估算/实现。
- 完整实验：Appendix C原文batch512，teacher/GSF-FM/GSF最高1M steps；主学生167.8M，另多数据/条件任务及teacher训练。完整公平campaign估计远超短时单A100/A30，成本过高不复现（建议审查DONE）。
- 本轮完整实验终态：成本过高，不复现（审查 DONE）
- 低成本范围建议：完整实验高成本关闭；廉价公式/训练机制仅为待定有界候选，不是现成GPU交付承诺。
- 证据：[原文](https://arxiv.org/html/2610.00497v1)；逐段定位见 [Google 对账](data/google-review.json)。

## 2602.16490 · From Growing to Looping: A Unified View of Iterative Computation in LLMs

- 机构/角色：TUM/Helmholtz AI/Google Paradigms of Intelligence合作；非可确认为Google单独主导。
- 作者代码：既有原审及本轮所读官方HTML未找到作者实现仓库。
- 可负担对象：可另定小Transformer真实训练机制：复制中间层及AdamW状态实现depth-growing，再在真实前向上复用该block做inference looping；记录参数/训练/推理预算，并只在validation选择loop配置。仅实现复制/loop不等于验证论文推理收益，完整缩小训练方案还需廉价成本核定。
- 完整实验：正文§4.1：SmolLM360M/1.7B分别约200B/400B tokens；22benchmark、growing/looping配方与后续训练对照。完整训练明显超当前单卡/本机预算，成本过高不复现（建议审查DONE）。
- 本轮完整实验终态：成本过高，不复现（审查 DONE）
- 低成本范围建议：关闭原规模训练；有界真实小模型机制需单独验收，不把200B预训练留为实施欠账。
- 证据：[原文](https://arxiv.org/html/2602.16490v1)；逐段定位见 [Google 对账](data/google-review.json)。

## 2510.15831 · VISTA: A Test-Time Self-Improving Video Generation Agent

- 机构/角色：官方project：一作Google Student Researcher/NUS，其他Google作者。
- 作者代码：官方project只见论文、demo和prompts，未见作者源码入口；所读页面不是全网穷尽。
- 可负担对象：能廉价验证的只是tournament/champion/三维批评/DTPA提示修订编排合同；没有真实视频生成和多模态judge时只能L0/诊断，不是核心复现。定义性路径仍需每轮实际重生成视频，因此本轮不认为已存在可直接接单的低成本能力实现。
- 完整实验：正文§4：100 MovieGen prompts+161内部prompts，Gemini2.5Flash+Veo3；§4.3每轮约0.7M tokens+28视频，视频生成token不包含。多轮、多baseline完整campaign高成本，且内部数据不可得；建议完整实验成本过高不复现（审查DONE）。
- 本轮完整实验终态：成本过高，不复现（审查 DONE）
- 低成本范围建议：完整VISTA复现高成本关闭；保留资料，不将固定视频/分数fixture当实现或evolve能力。
- 证据：[原文](https://arxiv.org/html/2510.15831v1)；逐段定位见 [Google 对账](data/google-review.json)。

## 2610.09159 · SpecGuard: Proving a Task Is Broken Before the Agent Cheats

- 机构/角色：一作Param Biyani为MATS；合作者Krishnamurthy Dvijotham为Google DeepMind，非Google一作。
- 作者代码：作者真实公共Apache2.0仓库https://github.com/prmbiy/specguard，含src/conflict_certifier、configs、data、scripts、tests、RESULTS。
- 可负担对象：优先可落地的忠实小范围：真实模型从D+C但不读T生成spec.lean；独立TestAgent生成tests.lean；真实Certifier连接并交Lean kernel，保留conflict/no-conflict/inconclusive和语义忠实性审计。少量公开/自建任务可不训练模型；不得手写gold规范绕过autoformalization或把Lean通过等同原意正确。
- 完整实验：§5同模型三Agent，SpecAgent120bash turns，各Agent10次Lean反馈，task timeout1h；349SWE任务+模型/重复/基线+187VERINA+95LiveCodeBench等。论文报告USD 0.26/task，仅349任务单臂估USD 90.74、三重复约USD 272.22（由论文均费推算，不是本地支出），完整campaign多小时应成本关闭；不能据此否定真实少量任务核心。
- 本轮完整实验终态：成本过高，不复现（审查 DONE）
- 低成本范围建议：保留小样本真实Lean核心作为最优先可负担候选，仍未实现；完整多模型全基准不承诺复现。
- 证据：[原文](https://arxiv.org/html/2610.09159v1)；逐段定位见 [Google 对账](data/google-review.json)。

## 2610.06064 · TrustMI: Causally controlling how assistants trust their users

- 机构：Meta 作者/合作机构已由原文核实。
- 原文资源：Official original §4, Appendix C/D.2/D.4: six 7B-70B models; learned steering matrices trained 10 epochs, 120B judge on H100, multiple agent and capability benchmarks, mostly three repetitions. Full campaign should not be treated as an affordable automatic TODO; smaller faithful scope requires explicit cost assessment.
- 当前缺项：Exact ID/title/name search in docs/src/tests found review artifacts only, no reproduction directory, adapter, runnable paper implementation or local metrics for this identity.
- 本轮完整实验终态：成本过高，不复现（审查 DONE）。若拆廉价保真组件，应先另立明确范围；不以固定模拟器/图答案冒充核心算法。
- 证据：[原文](https://arxiv.org/html/2610.06064v1)；§4; Appendix C; Appendix D.2-D.4 (web lines 164-170, 763-802)；仓库定位见 [Meta 对账](data/meta-review.json)。

## 2610.04721 · Knossos and Ariadne: Benchmarking and Learning Complete Diagram Topology Extraction with Vision-Language Models

- 机构：Meta 作者/合作机构已由原文核实。
- 原文资源：Official original Appendix E.1/Table10: NODE1125, EDGE5960, TRACE5801 steps for each 8B/9B backbone; 4 A100 GPUs, QLoRA. Full original reproduction exceeds single A100/A30 campaign budget; ledger has not recorded terminal cost closure.
- 当前缺项：Exact ID/title/name search in docs/src/tests found review artifacts only, no reproduction directory, adapter, runnable paper implementation or local metrics for this identity.
- 本轮完整实验终态：成本过高，不复现（审查 DONE）。若拆廉价保真组件，应先另立明确范围；不以固定模拟器/图答案冒充核心算法。
- 证据：[原文](https://arxiv.org/html/2610.04721v1)；Appendix E.1 Table10 (web lines 681-693)；仓库定位见 [Meta 对账](data/meta-review.json)。

## 2610.09484 · MIMESIS: Learning User Simulators as Training Environments for Interactive Agents

- 机构：Meta 作者/合作机构已由原文核实。
- 原文资源：Official original A.1/Table4: mid-training32 A100 for about4.8days, 9.51B tokens; SFT8 A100; A.3/Table7 simulator RL16 A100/500steps/512rollouts; D.1/Table13 actor RL16 A100. No repository cost terminal is recorded.
- 当前缺项：Exact ID/title/name search in docs/src/tests found review artifacts only, no reproduction directory, adapter, runnable paper implementation or local metrics for this identity.
- 本轮完整实验终态：成本过高，不复现（审查 DONE）。若拆廉价保真组件，应先另立明确范围；不以固定模拟器/图答案冒充核心算法。
- 证据：[原文](https://arxiv.org/html/2610.09484v1)；Appendix A.1 Table4, A.3 Table7, D.1 Table13 (web lines 304-328, 382-427, 658-678)；仓库定位见 [Meta 对账](data/meta-review.json)。

## 覆盖边界

大部分旧候选未保留可独立验证的完整作者机构块。
本轮对现有 45 份作者字段缓存做保险检查，另定向读取优先项官方作者块；部分缓存字段本身不完整。
因此不能断言其余候选没有 Google/Meta 合作者，更不能把使用 Gemini/Llama 当成机构证据。
