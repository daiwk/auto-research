---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 评测与可靠性：如何知道真的做对了

[Agent](index.md) / 43 个问题 · 43 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">43 个问题 · 43 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:physical-engineering-exam" data-paper-title="PLE: Physical-Engineering&#x27;s Last Exam" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PLE: Physical-Engineering&#x27;s Last Exam Agent Google Cloud AI Research 2026-10-21 PLE把专业工程工作组织为85项长时任务，覆盖结构、土木、电气及机械；输入是多格式项目文件，输出是可审查的工程产物。任务由专家编写，或经Creator–Solver迭代后由专家复核；裁判与参考解不向solver暴露。正文、实验及附录已读，最新公开提交协议另按固定代码版本核验。本地只执行配置、产物检查与给定外部评分的聚合；图中的独立grader仍是未运行的外部步骤。不会把合成文件当作真实工程结果。 因此成本过高，不复现（审查 DONE），不下载任务镜像/大权重、不启动昂贵试跑或自动重试。10月23日官方代码固定29项public dev、56项hidden test。任务配置的原始YAML SHA256为 c36cab6f0f3a1ab613e5b507e13dad80f56d3eec370019969965f5a32edaed1e，对应配置内数据revision为 535cf0a8af68126e3f00a1441cf736754a0cda4b。测试夹具仅含公开配置转成的JSON，不含题目环境、grader、参考解或任务答案。  公开评测协议 工程产物验收与来源隔离 Agent 评测与可靠性：如何知道真的做对了 约束型任务为什么用硬门 G 切断目标分，而非让目标优化抵消硬约束失败？ 工程产物可能目标值漂亮却违反必须满足的条件，硬门要求全部硬约束通过才计算那部分收益。约束比例仍提供分项信息，完整任务分母保留缺失项为零；本地评分聚合只消费外部裁判，不具备判断物理可行性或专业规范的独立能力。 例如设计重量很低但关键承载条件失败，不能让轻量化高分抵消硬失败；缺交产物也不能从平均分里删掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-physical-engineering-exam-2277e47a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-481c8954021f31c4">约束型任务为什么用硬门 G 切断目标分，而非让目标优化抵消硬约束失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aphysical-engineering-exam">PLE: Physical-Engineering&#x27;s Last Exam</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工程产物可能目标值漂亮却违反必须满足的条件，硬门要求全部硬约束通过才计算那部分收益。约束比例仍提供分项信息，完整任务分母保留缺失项为零；本地评分聚合只消费外部裁判，不具备判断物理可行性或专业规范的独立能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如设计重量很低但关键承载条件失败，不能让轻量化高分抵消硬失败；缺交产物也不能从平均分里删掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30537v1">原论文</a> · <a href="../../../../agent-research/2610.30537-physical-engineering-exam/">实现解读</a> · <a href="#qa-481c8954021f31c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scope-replay" data-paper-title="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning Agent Peking University 2026-10-16 修改机器人控制程序可能修好新场景却破坏旧场景。SCOPE 从开发执行证据建立失败前沿图，区分有证据支持、被反驳和未知检查，按局部修补、阶段重设或策略重生成继续搜索。它记录过去成功实例的完整 API tape，在候选源变化时，抽取至多三个历史见证进行本地有状态重放；重放有分歧的实例才可能安排稀疏真实环境诊断。§3 原论文 Figure 2 是有状态 API 重放与认证图；Figure 1 是整体搜索流程。需保留二者区别。原图由本批统一资源流程处理。 完整实验成本过高，不复现（审查 DONE）；不实现视觉 critic、失败前沿图、LLM repair 或真实环境诊断。component_only / L1 CPU 状态重放组件；不是机器人 Agent、完整程序搜索或 held-out 能力评测。真实执行可信 Python 回调的 API 记录与重放：有限标量、字符串键 dict、list、tuple，包含可变容器别名、循环引用、API 返回值指向既有容器、原地副作用和白名单内建异常。前后状态来自同一对象身份表；不能用逐项 deepcopy 破坏别名。另对最终公共状态做保守匹配，防止最后一次 API 之后的本地修改被误认证。  规划、推理与工具使用 有状态重放与实例认证 Agent 评测与可靠性：如何知道真的做对了 API tape 重放成功，为什么不能当作所有输入的程序等价证明或候选接纳门？ 重放只检查记录实例在给定状态、返回和异常下是否一致，未见输入仍未知。它用于选择值得真实环境诊断的差异，不决定成功候选必须回滚；原生环境成功才更新 accepted program，重放分歧也只是证据差异，不能直接记成环境失败。 例如旧案例的返回顺序与新程序不同，可触发重点复测；若新程序已在真实环境完成当前任务，不能仅因旧 tape 不兼容就擅自拒绝。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-scope-replay-4a09ab7b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9bb2e7154e6a7783">API tape 重放成功，为什么不能当作所有输入的程序等价证明或候选接纳门？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascope-replay">SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重放只检查记录实例在给定状态、返回和异常下是否一致，未见输入仍未知。它用于选择值得真实环境诊断的差异，不决定成功候选必须回滚；原生环境成功才更新 accepted program，重放分歧也只是证据差异，不能直接记成环境失败。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧案例的返回顺序与新程序不同，可触发重点复测；若新程序已在真实环境完成当前任务，不能仅因旧 tape 不兼容就擅自拒绝。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23128">原论文</a> · <a href="../../../../agent-research/2610.23128-scope-replay/">实现解读</a> · <a href="#qa-9bb2e7154e6a7783">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-perturb" data-paper-title="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations Agent The Hong Kong University of Science and Technology (Guangzhou) 2026-10-15 Agent 失败不一定来自模型推理：用户请求缺信息、技能规范过时、历史上下文出错和工具说明漂移都可能沿轨迹传播。AgentPerturb 交叉组织四个目标——用户请求、过程规范、继承上下文、工具契约 ——与缺失、冗余、错误三类扰动，得到12个家族。每对只改一个目标，其余三个、后端和成功 oracle 不变。原文 §3、附录 F 候选不能因为“JSON合法”就入选：与生成器独立的语义 verifier 必须确认单目标、目标不变、仍可求解、可执行四项全部通过，再结合原生 validator。 原文完整配置为10个前沿模型×2真实环境×25任务×12类扰动，单任务可达200轮、约30分钟上限，还需生成/语义验证 API，成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现扰动边界、独立验证与配对记录，不生成官方任务，不声称语法检查能够证明语义保持。每 seed 在无外部副作用的算术/工具契约 fixture 上实际执行全部12家族，actor 只解析公开输入，grader 单独判分。独立的领域 verifier 拒绝改变真实目标的编辑；语法-only负对照会错误放行这些编辑。  公共评测与协议 交互输入扰动与稳健性 Agent 评测与可靠性：如何知道真的做对了 为什么扰动候选通过 JSON 检查后，还必须独立确认目标不变且仍可求解？ 结构合法只保证可解析，扰动可能不小心换了任务或删掉必需信息到无法恢复。单目标语义验证保持其他因素、后端与 oracle 不变，才能解释性能差来自交互压力；缺失评分要报告配对覆盖和界限，不能删掉失败对后宣称鲁棒性良好。 例如只改工具说明措辞应不改工具真实行为；若同时移除唯一必需工具，失败就混入不可解性，不能当同一扰动效果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-agent-perturb-def3e837" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0b56c1b86c3904f6">为什么扰动候选通过 JSON 检查后，还必须独立确认目标不变且仍可求解？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-perturb">AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>结构合法只保证可解析，扰动可能不小心换了任务或删掉必需信息到无法恢复。单目标语义验证保持其他因素、后端与 oracle 不变，才能解释性能差来自交互压力；缺失评分要报告配对覆盖和界限，不能删掉失败对后宣称鲁棒性良好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只改工具说明措辞应不改工具真实行为；若同时移除唯一必需工具，失败就混入不可解性，不能当同一扰动效果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21624">原论文</a> · <a href="../../../../agent-research/2610.21624-agent-perturb/">实现解读</a> · <a href="#qa-0b56c1b86c3904f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:disagreement-routing" data-paper-title="Disagreement-Guided Weak-to-Strong Routing" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Disagreement-Guided Weak-to-Strong Routing Agent University of Pennsylvania 2026-10-15 “弱模型可能答错”不等于“强模型能补救”。原文用弱强分歧减去强模型自身分歧，估计升级调用的增益。离线只需对模型回答/动作做等价性比较，不需要判断哪个回答正确；测试时仅运行弱模型的表示和两个轻量 probe，路由决定升级时才查询强模型。原图出处：原论文 Figure 1。 完整 8B 弱模型、多个强模型、每步 K=10、WebShop 数千任务和多预算长 rollout 在单 A100/A30/Mac 下成本过高，成本过高，不复现（审查 DONE）。component_only / CPU 诊断：实现论文目标估计、两个真实拟合的 probe 和 validation 阈值合同。合成表示不是 LLM hidden state，不把机制检查写成 BFCL/WebShop 能力提升；不进入 Evolve。每 seed 生成 128 个独立合成 prompt-vector，80 train / 24 validation / 24 test；每 prompt 两个弱响应、12 个强响应采样。  专家模型编排 Agent 评测与可靠性：如何知道真的做对了 为什么要从弱强分歧里减去强模型自身分歧？ 弱强不同可能因为强模型也不稳定，而非升级能纠正弱模型。用不同采样索引估计强模型自分歧，扣除这部分后更接近调用增益线索；分数可为负，并非成功概率，测试时应只跑弱表示与 probe，决定升级后才付强模型调用成本。 例如强模型自己两次答案都相反，弱强分歧很高不一定值得升级；若强模型内部一致而与弱模型不同，信号才更明确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-disagreement-routing-3ad2d018" class="ar-learning-paper-anchor"></span>
<h2 id="qa-15d5ca65c5b0168c">为什么要从弱强分歧里减去强模型自身分歧？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adisagreement-routing">Disagreement-Guided Weak-to-Strong Routing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>弱强不同可能因为强模型也不稳定，而非升级能纠正弱模型。用不同采样索引估计强模型自分歧，扣除这部分后更接近调用增益线索；分数可为负，并非成功概率，测试时应只跑弱表示与 probe，决定升级后才付强模型调用成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如强模型自己两次答案都相反，弱强分歧很高不一定值得升级；若强模型内部一致而与弱模型不同，信号才更明确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22245">原论文</a> · <a href="../../../../agent-research/2610.22245-disagreement-routing/">实现解读</a> · <a href="#qa-15d5ca65c5b0168c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gacc-bench" data-paper-title="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models Agent Fudan University 2026-10-15 长期上下文压缩常在具体后续问题尚未知时执行，但用户可能已给出高层目标。GACC-Bench 按 context–goal 组织多道后续问题，压缩器只能看到来源、目标和预算；固定 reader 用同一压缩记忆逐题回答，再由固定 judge 对照原文和参考答案评分，检验是否保全整组目标证据。 其长来源、多问题和多模型调用总成本高，成本过高，不复现（审查 DONE）；evaluation_protocol_interface / L1 CPU 合同诊断。接口可接真实 compressor、reader、judge 和 tokenizer；本轮仅固定 token-ID/规则 fixture，没有运行官方数据或 LLM，不声称实现了新的压缩模型。每 seed 初始化两段小字符串来源、四个目标、12 个问题。规则 compressor 只挑目标所在行，规则 reader 只解析已保留字段，fixture judge 做精确比较；这三者不是 LLM。  公共评测与协议 上下文压缩 Agent 评测与可靠性：如何知道真的做对了 同一 context–goal–budget 为什么只生成一次记忆供所有后续问题复用？ 压缩时只知高层目标，不知具体问题，复用能检验一份记忆是否保全整组所需证据。若逐题重压缩，压缩器已获得额外查询信息，任务就变了；严格 token 截断、零预算空记忆与不补 padding 也决定 reader 的真实输入，不能只报名义预算。 例如目标是了解一次项目决策，后续分别问日期和原因，应读同一份预先压缩记忆，而非每题再偷取原文做定向摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-gacc-bench-1c3f337b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2f9e0b46e42d85cd">同一 context–goal–budget 为什么只生成一次记忆供所有后续问题复用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agacc-bench">GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>压缩时只知高层目标，不知具体问题，复用能检验一份记忆是否保全整组所需证据。若逐题重压缩，压缩器已获得额外查询信息，任务就变了；严格 token 截断、零预算空记忆与不补 padding 也决定 reader 的真实输入，不能只报名义预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如目标是了解一次项目决策，后续分别问日期和原因，应读同一份预先压缩记忆，而非每题再偷取原文做定向摘要。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21893">原论文</a> · <a href="../../../../agent-research/2610.21893-gacc-bench/">实现解读</a> · <a href="#qa-2f9e0b46e42d85cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-decomposition" data-paper-title="Harness-Delta Attribution: Dissecting Gains From Harness Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Harness-Delta Attribution: Dissecting Gains From Harness Evolution Agent Amazon 2026-10-15 同一个冻结模型的 Harness 可以靠更多推理算力，也可以靠基准捷径涨分。甚至 held-out 数据也可能共享相同捷径。HDA 先对 baseline/evolved 的逐样本差做双侧 paired bootstrap；收益不显著时停止归因。显著时，构造算力匹配 baseline 与移除已检测捷径的 evolved，且两种控制的构造都需要任务相关人审。方法 §3 原图建议：原论文 Figure 2，PDF 第3页，四臂及三类差值关系。 原文25配置跨模型/演化框架/任务，含 SWE-bench 容器与多轮昂贵重评估，完整矩阵成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现归因算子和控制接纳，不自动证明 Harness 可泛化。接口要求四臂 item ID 顺序完全一致、逐样本有限分数、Harness SHA256 和同单位平均推理成本；控制必须携带人审者与依据。CPU 内核实际重采样10,000次，计算区间、双侧 p 值、原始差值、展示份额及数值恒等式误差。算力匹配容差是本地显式参数，不是假定原论文常数。没有人审、错配样本、错配预算一律拒绝；零增益/噪声对照不归因。  公共评测与协议 Harness进化归因与过拟合审计 Agent 评测与可靠性：如何知道真的做对了 HDA 的残余 G 为什么只能视作泛化改进上界，而不是直接的迁移证据？ 算力匹配减掉额外计算，已检测捷径中和再剥离一部分过拟合，但未发现捷径仍可能留在残余里。控制构造需要任务相关人审，且先确认原收益显著才归因；代数分解保证账目一致，不保证每项已被完整因果识别或适用于新分布。 例如去掉已知文件名捷径后仍涨分，也可能还利用隐藏目录顺序；不能把剩下全部提升都宣称是真正通用推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-harness-decomposition-8f77338c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c188a5254d4945dd">HDA 的残余 G 为什么只能视作泛化改进上界，而不是直接的迁移证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-decomposition">Harness-Delta Attribution: Dissecting Gains From Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amazon</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>算力匹配减掉额外计算，已检测捷径中和再剥离一部分过拟合，但未发现捷径仍可能留在残余里。控制构造需要任务相关人审，且先确认原收益显著才归因；代数分解保证账目一致，不保证每项已被完整因果识别或适用于新分布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如去掉已知文件名捷径后仍涨分，也可能还利用隐藏目录顺序；不能把剩下全部提升都宣称是真正通用推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22466">原论文</a> · <a href="../../../../agent-research/2610.22466-harness-decomposition/">实现解读</a> · <a href="#qa-c188a5254d4945dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:librarian-agents" data-paper-title="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries Agent Stanford University 2026-10-15 常规 RAG 每次查询后才检索，重复探索跨文档关系。Librarian 在还未看到评测问题时，由可学习 builder 把原始语料组织成可复用层级文件系统；固定 answerer 后续导航，必要时沿 provenance 回退到 raw docs。CreateFile、MergeFiles、Delete、Stop 形成有限 horizon MDP，Delete 永远不能删原文。 单 A100/A30 或本地 Mac、零 API/训练预算下，成本过高，不复现（审查 DONE）。adapter: null，仅诊断，不允许 Evolve 晋级。本地为 evaluation_protocol_interface：真实文件系统/provenance 合同与官方 compact score records 的 CPU 复算。没有训练 RL builder，没有以静态摘要替代论文核心模型；adapter: null，仅诊断，不允许 Evolve 晋级。官方 revision 455ac88c81c639c10a8404464dabf71a7fbb563e；  公共评测与协议 层级记忆与预见式工作区 Agent 评测与可靠性：如何知道真的做对了 builder 尚未看到评测问题，为什么不能按已知问题把层级文件系统专门整理成答案索引？ 目标是预先组织可复用工作区，固定 answerer 后续面对未知查询导航。提前看题会把整理变成针对答案的检索捷径，失去跨问题价值；来源回退还要保留原文，Delete 不得删除原始语料，一般成本公式也不能冒称主训练实际用了非零成本 shaping。 例如先按公司和日期整理资料可供多种问题使用；若提前知道要问某数字并只把它写在首页，评测就不再检验通用整理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-librarian-agents-828f2c36" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3498243647684558">builder 尚未看到评测问题，为什么不能按已知问题把层级文件系统专门整理成答案索引？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alibrarian-agents">Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是预先组织可复用工作区，固定 answerer 后续面对未知查询导航。提前看题会把整理变成针对答案的检索捷径，失去跨问题价值；来源回退还要保留原文，Delete 不得删除原始语料，一般成本公式也不能冒称主训练实际用了非零成本 shaping。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先按公司和日期整理资料可供多种问题使用；若提前知道要问某数字并只把它写在首页，评测就不再检验通用整理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22273">原论文</a> · <a href="../../../../agent-research/2610.22273-librarian-agents/">实现解读</a> · <a href="#qa-3498243647684558">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:probe" data-paper-title="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents Agent Mohamed bin Zayed University of Artificial Intelligence 2026-10-15 任务完成并不等于按业务/隐私政策完成；只测试最终状态或有害文本也可能漏掉多轮工具调用中的违规。PROBE 训练扮演正常客户的 auditor，与冻结 target 交互，私有 verifier 从完整 trace 判断违规；奖励综合违规、可信客户行为、工具流程进展和策略多样性，比较 GRPO、DPO 和 GFlowNet。 成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。只实现惰性 trace/verifier/reward 接口和四个独立规则示例；没有训练审计模型，也没有接入完整 SkyAssist 或真实目标服务。每 seed 构造 12 条惰性 trace，随机化重复轮数，不执行任何工具。四个示例核验 required fields、当前 mutation intent 的确认、限制目的地及人数；它们不是原文完整 20 策略套件。第五个明确 unsupported 的语义策略留在 coverage 分母。  公共评测与协议 Agent RL Agent 评测与可靠性：如何知道真的做对了 为什么违规奖励对同一政策重复命中递减，却仍保留原始 yield 统计？ 递减训练奖励防止 auditor 靠反复触发同一漏洞刷分，鼓励覆盖更多政策；原始 yield 则描述实际命中事件，可超过每百 episode 一百次。两种统计对象不同，去重覆盖和事件总量应分列，局部奖励实现也不等于完成整套审计 RL。 例如一段对话连续三次触发同一违规，训练可依次少奖或不奖，但事件日志仍应记录三次，不能为去重而丢原始证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-probe-e4f99af8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bbf997d26ce06409">为什么违规奖励对同一政策重复命中递减，却仍保留原始 yield 统计？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprobe">PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>递减训练奖励防止 auditor 靠反复触发同一漏洞刷分，鼓励覆盖更多政策；原始 yield 则描述实际命中事件，可超过每百 episode 一百次。两种统计对象不同，去重覆盖和事件总量应分列，局部奖励实现也不等于完成整套审计 RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一段对话连续三次触发同一违规，训练可依次少奖或不奖，但事件日志仍应记录三次，不能为去重而丢原始证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22124">原论文</a> · <a href="../../../../agent-research/2610.22124-probe/">实现解读</a> · <a href="#qa-bbf997d26ce06409">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scipivot" data-paper-title="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents Agent University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核） 2026-10-15 26 个跨六科学领域项目、六个月人类纠偏记录构成 248 个关键决策：一个选项是原 LLM 方案，另一个为人类纠正方案。评测器选择更适当的后续研究计划，不是预测项目最终成功。构建 reference 可以看后续记录，但被测模型最多只能看纠偏前项目状态，不能看未来轨迹、正确标签或方案来源身份。 完整实验成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。本地只接入已发布的 options-only：公开输入与 grader references 分离、双顺序计划、严格解析、完整失败分母、case 等权与 bootstrap。没有调用模型、没有完整项目记录，也没有本地科学研究能力分数。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。  公共评测与协议 科学研究判断与纠偏 Agent 评测与可靠性：如何知道真的做对了 为什么交换选项位置后要重开独立会话，并按 case 而非两次回答重采样？ 位置交换用于检查选择是否稳定，独立会话避免第一次回答污染第二次；两种顺序仍来自同一项目决策，不能当成两个独立样本。被测模型只能看纠偏前状态，后续记录可用于构建参考，却不能作为输入，更不能暴露哪项来自人类或原 LLM。 例如同一计划甲乙分别放 A/B 和 B/A，若在同一会话里连问，模型可能记住先前选择而非重新判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-scipivot-7482a1e6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9fb1bddc37dbff1d">为什么交换选项位置后要重开独立会话，并按 case 而非两次回答重采样？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascipivot">SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置交换用于检查选择是否稳定，独立会话避免第一次回答污染第二次；两种顺序仍来自同一项目决策，不能当成两个独立样本。被测模型只能看纠偏前状态，后续记录可用于构建参考，却不能作为输入，更不能暴露哪项来自人类或原 LLM。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一计划甲乙分别放 A/B 和 B/A，若在同一会话里连问，模型可能记住先前选择而非重新判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21082">原论文</a> · <a href="../../../../agent-research/2610.21082-scipivot/">实现解读</a> · <a href="#qa-9fb1bddc37dbff1d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:shortcut-sensitivity" data-paper-title="Shortcut Sensitivity in Agent-Safety Evaluations" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Shortcut Sensitivity in Agent-Safety Evaluations Agent Kontext 2026-10-15 Agent 安全评测会把轨迹长度、工具名、来源标记和重复交互带入输入。高分有时来自这些构造特征，未必测到了真正的风险判断。论文建立三级推断阶梯：①线索能否预测标签；②线索与 guard 决策是否相关；③仅改变线索的配对干预是否改变决策。前一级只能提出下一级的检查目标，不能自动推导“模型走了捷径”。原图出处：原文 Figure 1：三级 shortcut audit。 单 A100/A30/Mac 无相应 API/多模型预算且整体成本仍高，成本过高，不复现（审查 DONE）。本地是 component_only / CPU 机制诊断，不是安全 guard。本地是 component_only / CPU 机制诊断，不是安全 guard。读标签的工具名查表只用于证明 benchmark 标签可预测性，不能作为 Agent、安全检测能力或 Evolve 晋级证据。  公共评测与协议 Agent 评测与可靠性：如何知道真的做对了 工具名能预测标签，为什么还不能断言 guard 使用了这个捷径？ 第一层只说明数据构造存在相关线索，第二层检查 guard 决策相关性，第三层保持其余条件只改线索，才更接近行为依赖证据。配对效应还需控制随机不一致与安慰剂，不能把相关性、无符号翻转率和有符号效应混成同一结论。 例如危险样本常用某工具名，只训练名字查表能高分；要证明 guard 走捷径，还需改名不改行为并观察其决策是否改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-shortcut-sensitivity-1f4bb949" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fb9c6ae3c3a0bb7e">工具名能预测标签，为什么还不能断言 guard 使用了这个捷径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ashortcut-sensitivity">Shortcut Sensitivity in Agent-Safety Evaluations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kontext</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第一层只说明数据构造存在相关线索，第二层检查 guard 决策相关性，第三层保持其余条件只改线索，才更接近行为依赖证据。配对效应还需控制随机不一致与安慰剂，不能把相关性、无符号翻转率和有符号效应混成同一结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如危险样本常用某工具名，只训练名字查表能高分；要证明 guard 走捷径，还需改名不改行为并观察其决策是否改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22243">原论文</a> · <a href="../../../../agent-research/2610.22243-shortcut-sensitivity/">实现解读</a> · <a href="#qa-fb9c6ae3c3a0bb7e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tool-bottleneck-bench" data-paper-title="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets Agent University of Osaka 2026-10-15 工具 Agent 的失败不只取决于模型：工具目录、可见菜单、工作流和返回记录编码会与 token/call/turn 上限交互。论文固定请求、事实和决策，分别操纵注册目录 R、可见菜单 V、认证工作流 W、返回状态 D。原协议有 36 个 family、12 个企业意图；routed menu 使用真值辅助缩窄，不能视为无需 oracle 的能力方案。 成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。单测中的无模型 public-handoff controller 只是 sandbox/合同诊断，不是论文 Agent。本地为 evaluation_protocol_interface：有限任务编译器、真实状态沙箱、九义务 exact grader，以及一组官方历史行的 CPU 复算。adapter: null、diagnostic_only: true、promotion_eligible: false、evolve_integrated: false；没有评测新的 Agent。  公共评测与协议 工具 Agent 与 harness 预算 Agent 评测与可靠性：如何知道真的做对了 为什么把失败记作“首个未满足义务”，不等于已经完成因果归因？ 义务顺序提供一致标签，但后面还可能有其他失败，首个检查项未通过并不能证明它是唯一根因。固定请求事实再操纵目录、菜单、工作流和返回状态才能研究压力影响；真值辅助 routed menu 属诊断条件，不能被当无需 oracle 的部署能力。 例如工具没检索到先标可用性失败，参数逻辑也许同样错误；修复第一项后才可能暴露第二项，标签顺序不是因果证明。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-tool-bottleneck-bench-4ca26883" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c5fe57bc8a85b2fa">为什么把失败记作“首个未满足义务”，不等于已经完成因果归因？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atool-bottleneck-bench">ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Osaka</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>义务顺序提供一致标签，但后面还可能有其他失败，首个检查项未通过并不能证明它是唯一根因。固定请求事实再操纵目录、菜单、工作流和返回状态才能研究压力影响；真值辅助 routed menu 属诊断条件，不能被当无需 oracle 的部署能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具没检索到先标可用性失败，参数逻辑也许同样错误；修复第一项后才可能暴露第二项，标签顺序不是因果证明。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21098">原论文</a> · <a href="../../../../agent-research/2610.21098-tool-bottleneck-bench/">实现解读</a> · <a href="#qa-c5fe57bc8a85b2fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:alpha-diana" data-paper-title="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks Agent Hong Kong Baptist University 2026-10-14 同一模型装进不同 Harness 后，提示、工具、恢复策略和记忆都会影响结果。只报告成功任务或平均 token，容易把丢失评分、运行失败、反复重试的成本掩盖掉。AlphaDiana 用统一任务、采样和资源政策比较完整的“模型—Harness”系统，同时保留各 Harness 的原生执行方式。原文 §2、附录 A–B 本地保留四项可独立执行的协议： 原文多模型、多 Harness、多任务矩阵使用 16×A100-80GB，并包含27B/31B模型和远程模型，完整实验成本过高，不复现（审查 DONE）。这些是合成协议诊断，不是新模型能力或真实tokenizer费用。evaluation_protocol_interface / L1 CPU。实现记录、状态和计量合同，不实现新的推理 Agent，不冒充官方 benchmark 接入。CPU fixture 让 actor 从公开算式计算答案，单独 grader 持有 reference；注入执行失败、评分中断和错误答案，实际运行重试、状态管理和汇总。  公共评测与协议 Harness 配对测量与状态隔离 Agent 评测与可靠性：如何知道真的做对了 重试为什么只增加 attempt，而不增加逻辑样本分母或挑最好的一次？ 同一 task/sample 的重试仍是在解决同一请求，多算分母或挑最好记录会改变采样含义并隐藏失败成本。报告取最新记录、总成本累加所有 attempt，运行状态与评分状态分开；未评分是未知，不应伪装正确或从计划样本中静默删除。 例如同题先超时再成功，两次 token 都计成本，但样本仍是一份；不能只留下便宜的成功日志，让第一次尝试仿佛没发生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-alpha-diana-d2460928" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5990e05270ed514c">重试为什么只增加 attempt，而不增加逻辑样本分母或挑最好的一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aalpha-diana">AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong Baptist University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一 task/sample 的重试仍是在解决同一请求，多算分母或挑最好记录会改变采样含义并隐藏失败成本。报告取最新记录、总成本累加所有 attempt，运行状态与评分状态分开；未评分是未知，不应伪装正确或从计划样本中静默删除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同题先超时再成功，两次 token 都计成本，但样本仍是一份；不能只留下便宜的成功日志，让第一次尝试仿佛没发生。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20675">原论文</a> · <a href="../../../../agent-research/2610.20675-alpha-diana/">实现解读</a> · <a href="#qa-5990e05270ed514c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coda" data-paper-title="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents Agent Alibaba Token Hub, Alibaba Group 2026-10-14 策略与技能库共同训练后的最高成绩可能依赖技能原有措辞，一旦部署后技能被改写就退化。CODA 不把 delivered bank 的峰值当唯一结果，而是在相同任务上评估 T1 意义保持改写、T2 内容缺失、T3 误导内容及 no-skill anchor。原文 §3–4、附录 E要求先在原始库检索一次，固定选中集合和 retrieval-side 字段，只替换内容；不能重新检索引入额外混杂。 完整评测需要四类训练后的策略／技能对、五个真实环境和多种扰动重复，整体对单 A100/A30 或 Mac 成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现内容改写边界和配对指标，不重训共进化策略，不生成“语义保持”保证。每 seed 生成 32 个二值结果 fixture，在全部六条件上保留同一 ID 集合，实际执行内容字段替换和配对计算。独立计数验证全分母 RR；负对照故意改成条件分母，保存偏差。拒绝漏任务、修改检索字段和改写未选中技能。结果见 CPU 产物，不代表任何策略的真实稳健性。  公共评测与协议 技能漂移与共进化稳健性 Agent 评测与可靠性：如何知道真的做对了 对技能内容做意义保持改写时，为什么必须固定原始检索选中集合？ 重新检索会同时改变拿到哪些技能，无法区分策略依赖措辞还是检索器排名变化。先固定选中身份及检索字段，只替换内容，才能更集中测技能表达的脆弱性；意义等价也不能靠字符串相似度证明，整体成功率不变仍可能隐藏双向 outcome flip。 例如把同一流程改写为同义句，应仍提供原来三份技能；若改写后换了另外三份，性能变化就不再只由措辞导致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-coda-3d28333f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e2716653480cf5c0">对技能内容做意义保持改写时，为什么必须固定原始检索选中集合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoda">Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Token Hub, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重新检索会同时改变拿到哪些技能，无法区分策略依赖措辞还是检索器排名变化。先固定选中身份及检索字段，只替换内容，才能更集中测技能表达的脆弱性；意义等价也不能靠字符串相似度证明，整体成功率不变仍可能隐藏双向 outcome flip。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把同一流程改写为同义句，应仍提供原来三份技能；若改写后换了另外三份，性能变化就不再只由措辞导致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20845">原论文</a> · <a href="../../../../agent-research/2610.20845-coda/">实现解读</a> · <a href="#qa-e2716653480cf5c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ctxgap" data-paper-title="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports Agent Tencent 2026-10-14 编码 Agent 的最终报告可能“听起来完整”，却不足以让用户恢复真实任务状态。CTXGAP 不用任务完成率替代信息质量，而是从执行记录抽取原子事实，生成有参考答案的探针，在同一问题上比较只读累积报告的观察者、读取完整执行视图的观察者，以及直接询问执行 Agent 的条件。重要事实的类别权重防止“多生成简单问题”稀释遗漏。37 个主任务包含 148 个检查点、4,855 个探针，其中 4,799 个有效；公开文本探针及公开执行材料只是子集。 完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。本地完成的是官方冻结数值表的 CPU 复算与公开评测协议接口，不是新 Agent 的能力评测。完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。冻结统计复算：只下载五份固定数值表（约 1.65 MB），逐文件 SHA256 核验。按作者 reproduce_all.py 的统计口径独立组织复算；10,000 次聚类 bootstrap、固定 seed 0，结果与固定版本 data/reproduced_all.json 逐项相同。没有调用模型、没有下载完整轨迹。  公共评测与协议 任务状态可恢复性与报告审计 Agent 评测与可靠性：如何知道真的做对了 公开执行材料为什么不能重命名为 T_full 来复算完整报告差距？ 原完整视图包含部分不公开推理或记忆证据，公开子集缺这些事实，观察者能力和可回答问题范围会改变。同题配对与重要原子权重用于衡量报告遗漏，仍须区分公共与完整条件；按 task/run 聚类也避免把同任务大量探针当独立样本。 例如某端口只记录在私有记忆里，公开日志没有；用公开日志观察者答不出，不能说它代表原论文完整执行视图的上限。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-ctxgap-b6a0f849" class="ar-learning-paper-anchor"></span>
<h2 id="qa-823db16c649a2ab8">公开执行材料为什么不能重命名为 T_full 来复算完整报告差距？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Actxgap">What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原完整视图包含部分不公开推理或记忆证据，公开子集缺这些事实，观察者能力和可回答问题范围会改变。同题配对与重要原子权重用于衡量报告遗漏，仍须区分公共与完整条件；按 task/run 聚类也避免把同任务大量探针当独立样本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某端口只记录在私有记忆里，公开日志没有；用公开日志观察者答不出，不能说它代表原论文完整执行视图的上限。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与统计单位；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20003">原论文</a> · <a href="../../../../agent-research/2610.20003-ctxgap/">实现解读</a> · <a href="#qa-823db16c649a2ab8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbench" data-paper-title="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics Agent FAIR at Meta 2026-10-13 AutoformBench 不只要求补一个孤立证明，而是让 Agent 在固定 Lean/Mathlib 上构造支撑高级数学命题的定义、辅助引理和证明。341 个任务来自 24 个数学来源，共有 1,155 个需要完成的证明义务；一个任务只有全部义务均通过可信验证才算成功。最容易混淆的是两个不同实验条件：论文排行榜向 Agent 提供非形式化原文（source-present）；公开仓库则发布不含教材摘录/参考证明的 source-free 工作区。 原研究的九类 frontier 模型、341 题长轨迹及教材/工具链准备超出单张 A100/A30 或本地 Mac 的低成本预算，成本过高，不复现（审查 DONE）。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；本页是 CPU 评测协议接口，不是模型/Agent 能力复现。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；不提供本地 source-free 成功率，不接入 Evolve 晋级。在项目根目录、已安装项目的 Python 环境中运行：  形式化数学 Agent 评测协议与结果导入 Agent 评测与可靠性：如何知道真的做对了 source-present 与 source-free 为什么不能仅凭相同 task ID 直接比较分数？ 可见材料不同会改变形式化难度：原文或参考论证提供定义与思路，公开无来源工作区则要求更多自主构建。两者即使目标同名也不是同一信息条件，所有证明义务还必须一起通过；失败、超预算或基础设施行不能从固定任务分母里静默删掉。 例如同一个高等数学命题，一组能读教材证明、另一组只有 Lean 骨架，成绩差不应直接归因模型强弱，而要先匹配来源条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-autoformbench-7806e713" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e4b095973d365cfd">source-present 与 source-free 为什么不能仅凭相同 task ID 直接比较分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbench">AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可见材料不同会改变形式化难度：原文或参考论证提供定义与思路，公开无来源工作区则要求更多自主构建。两者即使目标同名也不是同一信息条件，所有证明义务还必须一起通过；失败、超预算或基础设施行不能从固定任务分母里静默删掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一个高等数学命题，一组能读教材证明、另一组只有 Lean 骨架，成绩差不应直接归因模型强弱，而要先匹配来源条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://github.com/facebookresearch/autoformbench/blob/af1aa38fd44e019e566bce0b5a168609a886d8e6/paper.pdf">原论文</a> · <a href="../../../../agent-research/autoformbench/">实现解读</a> · <a href="#qa-e4b095973d365cfd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:clasharness" data-paper-title="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline Agent Google / Emory University（共同署名） 2026-10-13 多个 Agent 共享文件、网页和任务上下文时，其他参与者可能给出错误事实、过期状态或矛盾指令。CLASHarness 要求被测 Agent 依据可见环境核对信息并完成任务，而不只是识别一段文字冲突。核心不是随机插入干扰，而是先确定任务真实状态，再用参考执行验证任务确实可解。八阶段管线先生成共享世界、角色规则与多轮场景；在每轮固定真实值，构造参考执行计划并在隔离环境实际执行，从轨迹效果编译确定性和语义检查，最后做一致性、视觉和渲染验收。前轮状态带入后轮，要求区分应遵循的用户意图与有冲突的 peer 消息。 完整原实验成本过高，不复现（审查 DONE）。缺清单时只报 observed-check 诊断，完整成功值为 null。本地提供固定版本参考资料导入、审计校验和外部 verdict 聚合接口。没有运行计算机使用 Agent，也没有重建完整多轮环境；官方分数不当作本地能力。完整原实验成本过高，不复现（审查 DONE）。固定参考导入：四个官方 JSON，合计不足 0.6 MB，固定 commit 与 SHA256；重算标签计数、306 项保守并集、死轮次数和精选行完整性。没有下载默认 8.5 GB 任务/轨迹包，没有运行模型。  公共评测与协议 多 Agent 冲突与计算机使用 Agent 评测与可靠性：如何知道真的做对了 为什么生成冲突场景前要固定真实状态并执行参考计划证明任务可解？ 否则失败可能只是场景自相矛盾或界面不可操作，而非 Agent 不会处理 peer 冲突。可执行参考建立真实状态、允许目标和检查义务，再检验被测者能否依据环境完成；空 required 集合或缺失 verdict 不能自动算成功，公平性调整也应预先声明。 例如 peer 声称文件已删除，真实文件仍在且参考操作可完成任务；这样才可测 Agent 是否核对环境，而非面对无解场景。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-clasharness-f0eec5c3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8c034b18ddbd1802">为什么生成冲突场景前要固定真实状态并执行参考计划证明任务可解？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aclasharness">CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Emory University（共同署名）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>否则失败可能只是场景自相矛盾或界面不可操作，而非 Agent 不会处理 peer 冲突。可执行参考建立真实状态、允许目标和检查义务，再检验被测者能否依据环境完成；空 required 集合或缺失 verdict 不能自动算成功，公平性调整也应预先声明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 peer 声称文件已删除，真实文件仍在且参考操作可完成任务；这样才可测 Agent 是否核对环境，而非面对无解场景。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与公平性口径；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19128">原论文</a> · <a href="../../../../agent-research/2610.19128-clasharness/">实现解读</a> · <a href="#qa-8c034b18ddbd1802">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ontrack" data-paper-title="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport Agent Cribl AI 2026-10-08 Agent 最终失败时，单个答案分数解释不了中间发生了什么。OnTrack 把事件组织成带依赖边的图，将当前执行前缀和成功参考轨迹作非平衡结构化对齐；无参考时则明确退化为循环、重试和信息停滞检测。 未运行官方 SWE-bench 容器或重新生成 Agent 轨迹；本地实现是公开日志回放监控，不执行日志命令，也不是 Agent 解题成功率或生产安全认证。运行器下载固定版本的公开 sailplane/swe-agent-trajs（约 92 MB）和 all-MiniLM-L6-v2。嵌入和监控均为 CPU 路径，无需 GPU。轨迹里的命令始终作为不可信文本，不会执行。缓存默认在 .cache/ontrack-public。  Agent 安全 实时轨迹监控与非平衡最优传输 Agent 评测与可靠性：如何知道真的做对了 事件不断增加时，为什么不把旧前缀节点质量每次改成 1/t？ 重缩放会让历史节点的权重仅因来了新事件而变化，混淆实际对齐进展与归一化效应。固定前缀质量、流式 warm-start 和结构耦合保留时间比较语义；准备干预时还要扩大求解预算重判，不可逆动作门不能依赖过期缓存前沿。 例如新增一次日志读取不应自动削弱此前关键编辑的质量；否则监控分数变化可能只是分母改变，而非行为真的偏离。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-ontrack-56d9bc62" class="ar-learning-paper-anchor"></span>
<h2 id="qa-655da0c786f78c79">事件不断增加时，为什么不把旧前缀节点质量每次改成 1/t？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aontrack">OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cribl AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重缩放会让历史节点的权重仅因来了新事件而变化，混淆实际对齐进展与归一化效应。固定前缀质量、流式 warm-start 和结构耦合保留时间比较语义；准备干预时还要扩大求解预算重判，不可逆动作门不能依赖过期缓存前沿。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新增一次日志读取不应自动削弱此前关键编辑的质量；否则监控分数变化可能只是分母改变，而非行为真的偏离。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12375">原论文</a> · <a href="../../../../agent-research/2610.12375-ontrack/">实现解读</a> · <a href="#qa-655da0c786f78c79">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:option-channel-attack" data-paper-title="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails Agent University of Southern California 2026-10-08 类型化模型对调用方给定的选项输出概率，但选项名字本身也进入模型输入。保持动作、可信策略定义不变，仅把允许选项换成误导性标签，就可能让本来正确的拒绝变成放行。论文把危险的 fail-open 与妨碍使用的 fail-closed 分开评价。 当前原始报告和归档协议均明确为 L1 合成守门诊断。真实 Laya checkpoint 的安全机制诊断，不是 Agent 任务成功率或生产安全认证。六种合成策略，每种校准/评测各 24 条，校准 seed=42、评测 seed=43；只在校准集从 escalate/deny/stop/lantern 选标签。A100 上运行公开 Laya checkpoint。没有调用真实外部工具，也没有执行被测动作。  Agent 安全 类型化守门模型 Agent 评测与可靠性：如何知道真的做对了 动作和可信政策不变，只改选项标签，为什么仍可能改变 guard 的放行决定？ 标签同样进入模型输入，语义暗示会影响类型化输出读出，即使底层动作没变。评测要把危险误放行与无害误拒绝分开，并在干净输入正确拒绝的禁止集合上算条件攻击率；分母为空应未定义，不能记零来假装防御完美。 例如禁止动作仍是同一调用，却把“拒绝”选项改成误导性名称；模型可能因标签理解变化选错，但不代表政策本身改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-option-channel-attack-6cce967b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7e849af5852a4fa5">动作和可信政策不变，只改选项标签，为什么仍可能改变 guard 的放行决定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aoption-channel-attack">One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>标签同样进入模型输入，语义暗示会影响类型化输出读出，即使底层动作没变。评测要把危险误放行与无害误拒绝分开，并在干净输入正确拒绝的禁止集合上算条件攻击率；分母为空应未定义，不能记零来假装防御完美。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如禁止动作仍是同一调用，却把“拒绝”选项改成误导性名称；模型可能因标签理解变化选错，但不代表政策本身改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12292">原论文</a> · <a href="../../../../agent-research/2610.12292-option-channel-attack/">实现解读</a> · <a href="#qa-7e849af5852a4fa5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:specguard" data-paper-title="SpecGuard: Proving a Task Is Broken Before the Agent Cheats" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SpecGuard: Proving a Task Is Broken Before the Agent Cheats Agent MATS 2026-10-06 当测试意外或恶意违背任务描述，coding agent 可能修改测试或硬编码结果，而不是报告任务不可满足。SpecGuard 在编码前拆开两个信息来源：SpecAgent 只看描述与源码、完全不看测试；TestAgent 独立翻译测试；Certifier 对齐两侧语义，由 Lean kernel 核验冲突证明。不能忠实表达或对齐时允许 inconclusive。论文 §3–4 完整多模型全基准实验：成本过高，不复现（审查 DONE）；忠实缩小的 component_only / L1 micro-suite。保留真实模型生成与真实 Lean kernel，不用手写规范或固定模型输出替代核心过程。完整多模型全基准实验：成本过高，不复现（审查 DONE）；这不等于小范围实验已取得论文效果。先准备已有的小型 coding checkpoint 和官方 Lean 4.24.0 二进制；不需要 Mathlib、REPL、Docker 或训练数据。  Agent 安全 形式化验证 任务规范与测试冲突 Agent 评测与可靠性：如何知道真的做对了 为什么 SpecAgent 完全不看测试，Lean 证明通过后仍可能是 inconclusive？ 不看测试让意图规范独立于可能错误或恶意的测试要求，Certifier 再检查两侧冲突。但形式证明只针对翻译和 connector 表达，若无法忠实对齐自然语言语义，就不能把 kernel 通过解释为原任务已被证明损坏，必须保留未确定结果。 例如题意要求排序，测试却要求反序，可分别形式化后证明冲突；若“稳定排序”含义翻译不清，不能仅凭一个有限证明就下结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-specguard-31696f7e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-837e8a2527eb3a28">为什么 SpecAgent 完全不看测试，Lean 证明通过后仍可能是 inconclusive？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspecguard">SpecGuard: Proving a Task Is Broken Before the Agent Cheats</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MATS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不看测试让意图规范独立于可能错误或恶意的测试要求，Certifier 再检查两侧冲突。但形式证明只针对翻译和 connector 表达，若无法忠实对齐自然语言语义，就不能把 kernel 通过解释为原任务已被证明损坏，必须保留未确定结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如题意要求排序，测试却要求反序，可分别形式化后证明冲突；若“稳定排序”含义翻译不清，不能仅凭一个有限证明就下结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.09159">原论文</a> · <a href="../../../../agent-research/2610.09159-specguard/">实现解读</a> · <a href="#qa-837e8a2527eb3a28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:defa" data-paper-title="DeFA: Dependency-Guided Failure Attribution for LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="DeFA: Dependency-Guided Failure Attribution for LLM Agents Agent Qwen DianJin Team, Alibaba Cloud Computing 2026-10-01 融合 protocol relation 和语义依赖构造 event dependency graph，再从违规事件逆向追踪 source 与下游影响，形成 failure propagation graph 并定位 decisive error。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  失败归因 依赖图 技能进化 Agent 评测与可靠性：如何知道真的做对了 为什么定位 decisive error 要保留依赖传播子图，而不是只标最后一个失败动作？ 最后失败可能由早期错误事实、参数或跨 Agent 消息导致，逆向依赖把责任源和受影响节点连接起来。协议关系提供结构，语义依赖补信息流，二者结合才能更具体解释传播；启发式最大错误分仍需证据，不是自动获得完整因果证明。 例如最后部署失败来自最早读取了旧配置，单责怪部署命令会漏掉源头；传播图可指出旧字段怎样一路传到错误参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-defa-2f35dc42" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6828861af8c1cd51">为什么定位 decisive error 要保留依赖传播子图，而不是只标最后一个失败动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adefa">DeFA: Dependency-Guided Failure Attribution for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen DianJin Team, Alibaba Cloud Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最后失败可能由早期错误事实、参数或跨 Agent 消息导致，逆向依赖把责任源和受影响节点连接起来。协议关系提供结构，语义依赖补信息流，二者结合才能更具体解释传播；启发式最大错误分仍需证据，不是自动获得完整因果证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最后部署失败来自最早读取了旧配置，单责怪部署命令会漏掉源头；传播图可指出旧字段怎样一路传到错误参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01256">原论文</a> · <a href="../../../../agent-research/2610.01256-defa/">实现解读</a> · <a href="#qa-6828861af8c1cd51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pace-capability" data-paper-title="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents Agent 原文首页未列第一作者机构 2026-10-01 在每次工具副作用发生前，根据认证请求编译出的 authority 与输入 provenance 同时检查 effect；入库时安全不代表执行时可信。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 安全 工具权限 provenance Agent 评测与可靠性：如何知道真的做对了 为什么记忆入库时安全，不能保证其内容在工具执行时有 authority？ 入库检查只处理当时内容，执行还要根据认证请求限制实际副作用，并追踪输入来源是否可信。provenance 与 authority 同时满足才放行，避免不可信记忆借合法工具越权；文本声称被授权不能代替系统认证，也不能只在写库时检查一次。 例如网页文字被存入记忆后要求删除文件，入库未发现危险不代表用户授权删除；执行前仍须核对 effect 和来源。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-pace-capability-eec90992" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5ab360b3ac4766b4">为什么记忆入库时安全，不能保证其内容在工具执行时有 authority？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apace-capability">PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>入库检查只处理当时内容，执行还要根据认证请求限制实际副作用，并追踪输入来源是否可信。provenance 与 authority 同时满足才放行，避免不可信记忆借合法工具越权；文本声称被授权不能代替系统认证，也不能只在写库时检查一次。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如网页文字被存入记忆后要求删除文件，入库未发现危险不代表用户授权删除；执行前仍须核对 effect 和来源。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01349">原论文</a> · <a href="../../../../agent-research/2610.01349-pace-capability/">实现解读</a> · <a href="#qa-5ab360b3ac4766b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:safe-self-improvement" data-paper-title="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover Agent 原文首页未列第一作者机构 2026-10-01 把检测、当前可执行实现选择和下一轮编辑源分开；所有候选必须对当前条件重新验证，若无候选通过则回滚 founder，而不是继续运行已失败 incumbent。 未调用论文编辑模型，也未复现 Amazon Bedrock 实验。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  RSI 安全 验证 回滚 Agent 评测与可靠性：如何知道真的做对了 为什么当前可执行版本与下一轮编辑源要分开选择？ 最有改进潜力的编辑父本未必在当前条件下安全可运行，运行版本必须重新验证后从合格集合选。无候选通过时回到 founder，而不是继续使用已经失败的 incumbent；恢复执行与继续搜索是两项职责，不能把历史曾通过当成永久有效资格。 例如新环境使现任版本检查失败，仍可保留它作分析编辑来源，但实际任务应切到当前验证合格版本或执行 founder 回滚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-safe-self-improvement-450abfd4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-48504ee29677188e">为什么当前可执行版本与下一轮编辑源要分开选择？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asafe-self-improvement">Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最有改进潜力的编辑父本未必在当前条件下安全可运行，运行版本必须重新验证后从合格集合选。无候选通过时回到 founder，而不是继续使用已经失败的 incumbent；恢复执行与继续搜索是两项职责，不能把历史曾通过当成永久有效资格。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新环境使现任版本检查失败，仍可保留它作分析编辑来源，但实际任务应切到当前验证合格版本或执行 founder 回滚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01073">原论文</a> · <a href="../../../../agent-research/2610.01073-safe-self-improvement/">实现解读</a> · <a href="#qa-48504ee29677188e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:veriharness" data-paper-title="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks Agent Google Cloud AI Research 2026-10-01 同一基础模型得到 workspace、证据工具和可复用验证技能；disagreement resolver 查证冲突 claim，consensus challenger 主动质疑共同 claim 和遗漏要求。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 验证 证据工具 长程任务 Agent 评测与可靠性：如何知道真的做对了 多个验证者达成共识后，为什么还需要 consensus challenger？ 共同结论也可能来自共享错误或共同遗漏，只有处理显式分歧无法发现所有人都没检查的要求。challenger 主动质疑共识与缺口，resolver 则针对冲突取证，职责互补；支持与反驳应来自证据工具，而不是把赞同票数当作真值。 例如三名审查者都只看页面截图，没人检查下载文件；challenger 可提出产物遗漏问题，即使原讨论完全没有分歧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-veriharness-6d6ee53b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2be905d50052cea6">多个验证者达成共识后，为什么还需要 consensus challenger？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Averiharness">VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共同结论也可能来自共享错误或共同遗漏，只有处理显式分歧无法发现所有人都没检查的要求。challenger 主动质疑共识与缺口，resolver 则针对冲突取证，职责互补；支持与反驳应来自证据工具，而不是把赞同票数当作真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三名审查者都只看页面截图，没人检查下载文件；challenger 可提出产物遗漏问题，即使原讨论完全没有分歧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00972">原论文</a> · <a href="../../../../agent-research/2610.00972-veriharness/">实现解读</a> · <a href="#qa-2be905d50052cea6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:user-proxy-bench" data-paper-title="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training Agent 原文未列机构 2026-09-29 UFS 与 agent task reward 独立：每个 episode 的所有适用 user-contract criteria 必须全部通过，episode 才计 1。重点审计 premature disclosure，即用户模拟器在 agent 请求之前就泄露私有字段；这可能维持任务成功，却让 agent 少做本应评测的信息收集。 复现级别：L1 评测机制。复现级别：L1 评测机制。实现严格 User Fidelity Score 与 premature disclosure 审计；不运行闭源 proxy。本地实现 Eq. (1) 的 all-criteria product，并按时间顺序审计 request/disclosure。它只接收 rubric pass/fail 和公开交互事件，不把私有 blueprint 暴露给被评 agent；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 375 个企业任务和七种 proxy。  Agent 评测 用户模拟器 信息泄漏审计 Agent 评测与可靠性：如何知道真的做对了 为什么用户模拟器提前透露私有字段，可能提高任务成功却降低 UFS？ Agent 原本应主动询问信息，模拟器抢先给出就绕过了被测的信息收集能力。UFS 单独检查每 episode 全部适用用户合同，而非复用任务回报，能暴露这种捷径；任务完成和用户扮演忠实是两条不同证据，不能只看成功率就认定模拟器好。 例如 Agent 尚未问订单号，模拟用户已主动报出，退款容易成功；但评测不再检验 Agent 是否知道何时询问关键字段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-user-proxy-bench-da315c41" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b9940179a02b78e4">为什么用户模拟器提前透露私有字段，可能提高任务成功却降低 UFS？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Auser-proxy-bench">UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Agent 原本应主动询问信息，模拟器抢先给出就绕过了被测的信息收集能力。UFS 单独检查每 episode 全部适用用户合同，而非复用任务回报，能暴露这种捷径；任务完成和用户扮演忠实是两条不同证据，不能只看成功率就认定模拟器好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 Agent 尚未问订单号，模拟用户已主动报出，退款容易成功；但评测不再检验 Agent 是否知道何时询问关键字段。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38043">原论文</a> · <a href="../../../../agent-research/2609.38043-userproxybench/">实现解读</a> · <a href="#qa-b9940179a02b78e4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:certified-selective-eval" data-paper-title="Certified Selective Automation of LLM Agent Evaluation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Certified Selective Automation of LLM Agent Evaluation Agent Independent Researcher 2026-09-28 按任务簇而非轨迹独立假设做 bootstrap，给自动判断区域的错误率建立上置信界，只有证书低于预算才自动接管。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent 评测 选择性自动化 统计证书 Agent 评测与可靠性：如何知道真的做对了 为什么自动评分区域的错误证书要按任务簇 bootstrap，而非把所有轨迹当独立样本？ 同任务多条轨迹共享难度与结构，独立抽样会低估相关性和不确定性。按簇重采样为自动判断区域建立错误率上界，只有低于预算才接管，其余保留人工或外部评估；低平均错误不等于任何阈值都可认证，证书还受校准分布与选择规则限制。 例如一个任务生成一百条近似轨迹，不能当一百份独立成功证据压窄区间；应把这批一起作为任务簇处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-certified-selective-eval-1bfcfcb0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1a0d4910bf52da75">为什么自动评分区域的错误证书要按任务簇 bootstrap，而非把所有轨迹当独立样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acertified-selective-eval">Certified Selective Automation of LLM Agent Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同任务多条轨迹共享难度与结构，独立抽样会低估相关性和不确定性。按簇重采样为自动判断区域建立错误率上界，只有低于预算才接管，其余保留人工或外部评估；低平均错误不等于任何阈值都可认证，证书还受校准分布与选择规则限制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个任务生成一百条近似轨迹，不能当一百份独立成功证据压窄区间；应把这批一起作为任务簇处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34320">原论文</a> · <a href="../../../../agent-research/2609.34320-certified-selective-eval/">实现解读</a> · <a href="#qa-1a0d4910bf52da75">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-design-study" data-paper-title="An Empirical Study of Harness Design for Coding Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="An Empirical Study of Harness Design for Coding Agents Agent University of Massachusetts Amherst 2026-09-17 固定底层执行循环，分别控制 planning、action space 与 context management，隔离 coding-agent harness 中真正影响效果和成本的因素。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。  编程 Agent Harness 设计 Agent 评测与可靠性：如何知道真的做对了 固定底层执行循环后分别改 planning、action space 与 context，为什么更能解释 harness 收益？ 完整框架对比常同时改变多个因素，无法判断涨分来自更多推理、易用动作还是更好状态管理。保持循环不变并单独控制组件，减少混杂，再分别看效果与成本；组件参考实现或统计合同并不等于已经运行原文大规模编码任务。 例如只把文件编辑接口换成精确替换，其他提示与预算不变，才能更集中评价动作空间，而非把同时换模型的收益一起算入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-harness-design-study-2ead25c3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d229d83150e67e88">固定底层执行循环后分别改 planning、action space 与 context，为什么更能解释 harness 收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-design-study">An Empirical Study of Harness Design for Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Massachusetts Amherst</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整框架对比常同时改变多个因素，无法判断涨分来自更多推理、易用动作还是更好状态管理。保持循环不变并单独控制组件，减少混杂，再分别看效果与成本；组件参考实现或统计合同并不等于已经运行原文大规模编码任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只把文件编辑接口换成精确替换，其他提示与预算不变，才能更集中评价动作空间，而非把同时换模型的收益一起算入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20804">原论文</a> · <a href="../../../../agent-research/2609.20804-harness-design-study/">实现解读</a> · <a href="#qa-d229d83150e67e88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:fuse-evaluator" data-paper-title="Verifiable Social Reasoning for LLM Assistants" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Verifiable Social Reasoning for LLM Assistants Agent Google Research / Hebrew University of Jerusalem / University of Cambridge 2026-09-15 用隐藏动机可验证的多 Agent 模拟评测用户转述、framing bias 与社会推理。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent 评测 社会推理 Agent 评测与可靠性：如何知道真的做对了 隐藏动机可验证的模拟，为什么比只看用户转述是否流畅更适合测社会推理？ 转述可能带偏见或遗漏，流畅回应未必识别各方真实目标。模拟环境保留不向被测者公开的动机与事件条件，评分侧据此检查推断，而非用表面措辞一致度代替；隐藏参考只能给验证器，固定逻辑 fixture 也不能冒充多 Agent 的真实语义交互。 例如用户把同事拒绝请求说成敌意，模拟真因可能是资源冲突；评测应看助手是否据可见证据区分，而非附和转述。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-fuse-evaluator-e12e2808" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8a95517ba8ccb520">隐藏动机可验证的模拟，为什么比只看用户转述是否流畅更适合测社会推理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afuse-evaluator">Verifiable Social Reasoning for LLM Assistants</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / Hebrew University of Jerusalem / University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>转述可能带偏见或遗漏，流畅回应未必识别各方真实目标。模拟环境保留不向被测者公开的动机与事件条件，评分侧据此检查推断，而非用表面措辞一致度代替；隐藏参考只能给验证器，固定逻辑 fixture 也不能冒充多 Agent 的真实语义交互。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户把同事拒绝请求说成敌意，模拟真因可能是资源冲突；评测应看助手是否据可见证据区分，而非附和转述。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17496">原论文</a> · <a href="../../../../agent-research/2609.17496-fuse-evaluator/">实现解读</a> · <a href="#qa-8a95517ba8ccb520">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:silr" data-paper-title="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents Agent Institute of Science Tokyo 2026-09-03 系统已经违规时，安全门不能简单拒绝所有仍不安全的动作，而要允许逐步恢复。SiLR 先 shadow-execute 提案，再比较每个受约束分支的严重度；只有在乘积序上不恶化的动作可进入真实环境，同一结构信号还能作为 GRPO 过程奖励。 复现级别：CPU 准入算子。复现级别：CPU 准入算子。ShadowGate 在真实传入的 simulator 深拷贝上执行动作，比较逐分支严重度；legacy 文本 mini-suite 没有 simulator，不生成安全或过程奖励结论。本实现不替代真实系统 simulator；没有确定性、覆盖充分的 verifier 时不能据此宣称安全。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Structure-preserving verifier and reward Agent 评测与可靠性：如何知道真的做对了 系统已违规时，为什么安全门不能把所有仍不完全安全的动作都拒绝？ 恢复可能需要经过尚有残余风险的中间状态，全拒绝会让系统被锁死。SiLR 先 shadow-execute，再要求每个受约束分支的严重度都不恶化，允许逐步改善；只看一个总分可能掩盖某分支变坏，shadow 结果也仍需对应真实执行合同。 例如两个权限问题中先撤销一个，另一个暂时保留，整体尚未完全安全却是有效恢复；不能要求一步消除全部问题才允许动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-silr-f498d510" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2e48dd4d8eb6dd50">系统已违规时，为什么安全门不能把所有仍不完全安全的动作都拒绝？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asilr">SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Science Tokyo</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>恢复可能需要经过尚有残余风险的中间状态，全拒绝会让系统被锁死。SiLR 先 shadow-execute，再要求每个受约束分支的严重度都不恶化，允许逐步改善；只看一个总分可能掩盖某分支变坏，shadow 结果也仍需对应真实执行合同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个权限问题中先撤销一个，另一个暂时保留，整体尚未完全安全却是有效恢复；不能要求一步消除全部问题才允许动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04629">原论文</a> · <a href="../../../../agent-research/2609.04629-silr/">实现解读</a> · <a href="#qa-2e48dd4d8eb6dd50">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:redevoagent" data-paper-title="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution Agent City University of Hong Kong 2026-08-27 RedEvoAgent 不直接检索冗长攻击轨迹，而把跨案例经验蒸馏成可读技能；只归因真正决定成败的工具，并且新技能必须在留出验证集上优于 incumbent 才能晋级。 复现级别：核心机制 + deterministic mini-suite。复现级别：核心机制 + deterministic mini-suite。实现工具效果画像、Deciding-Tool Attribution 和 held-out validation ratchet。未对真实产品 Agent 执行越权攻击；mini-suite 只验证安全的技能更新控制流。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300；关键价值是 validation ratchet/归因计数，而非简单任务的满分。  红队技能进化 Agent 评测与可靠性：如何知道真的做对了 为什么经验技能晋级要在留出集优于 incumbent，而非只看原攻击轨迹成功？ 原轨迹只能证明一次情境有效，技能抽象可能过拟合措辞或误把无关工具当关键因素。留出比较检验复用价值，严格提升才替换现任，避免持续累加低质经验；可读技能与真实执行之间仍需验证，本地筛选器不能代替完整评测行为。 例如一条审计经验只在某个样例有效，换同类新场景失效，就不应仅凭原日志成功把它升级为默认技能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-redevoagent-15b9a312" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f7faccca6551b9dd">为什么经验技能晋级要在留出集优于 incumbent，而非只看原攻击轨迹成功？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aredevoagent">RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原轨迹只能证明一次情境有效，技能抽象可能过拟合措辞或误把无关工具当关键因素。留出比较检验复用价值，严格提升才替换现任，避免持续累加低质经验；可读技能与真实执行之间仍需验证，本地筛选器不能代替完整评测行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条审计经验只在某个样例有效，换同类新场景失效，就不应仅凭原日志成功把它升级为默认技能。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27439">原论文</a> · <a href="../../../../agent-research/2608.27439-redevoagent/">实现解读</a> · <a href="#qa-f7faccca6551b9dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spec-driven-tests" data-paper-title="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation Agent Google 2026-08-17 直接让模型编写单元测试，可能遗漏输入边界或隐含的行为约定。本文先让Agent读取修复后的源码，写出每个代码单元的描述、前置条件、后置条件与测试建议；把条件标为已测试或未测试，保存为.spec.md，之后才允许生成测试。中间可由开发者修订规范；论文自动比较没有启用人工干预。 成本过高，不复现（审查 DONE）。L1协议诊断，不是代码Agent能力复现。三seed的确定性小整数fixture检查阶段顺序、公共字段隔离、相同测试双执行、非法源码修改拒绝、编译错误负控及按bug汇总。回调并非LLM，actual_llm_calls=0；其通过只是协议工作正常，不是Agent成功率。CPU诊断指标 Specification保存唯一代码单元及D/Pre/Post/Sug，输出Markdown；未测试条件须有建议。本地结构校验比论文提示约束更严格，但不把它当语义正确性证明。  工具使用 代码 Agent 与测试 Agent 评测与可靠性：如何知道真的做对了 先写前后置条件再生成测试，为什么能暴露直接写单测时的覆盖盲点？ 规范把每个代码单元的输入限制与应保证行为显式列出，再标记已测未测条件，测试生成才有可检查的覆盖目标。它仍来源于读取源码与解释，不能自动保证规范忠实；论文自动比较没有人工修订，也不应把可选开发者步骤算成已执行条件。 例如函数要求空输入返回空列表，规范可把它列为未测后置条件；直接模仿现有正常样例写测试可能一直漏掉边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-spec-driven-tests-4c06eb29" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d27f4aa512ac8b25">先写前后置条件再生成测试，为什么能暴露直接写单测时的覆盖盲点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspec-driven-tests">Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规范把每个代码单元的输入限制与应保证行为显式列出，再标记已测未测条件，测试生成才有可检查的覆盖目标。它仍来源于读取源码与解释，不能自动保证规范忠实；论文自动比较没有人工修订，也不应把可选开发者步骤算成已执行条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如函数要求空输入返回空列表，规范可把它列为未测后置条件；直接模仿现有正常样例写测试可能一直漏掉边界。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17177v1">原论文</a> · <a href="../../../../agent-research/2608.17177-spec-driven-tests/">实现解读</a> · <a href="#qa-d27f4aa512ac8b25">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessopt-bench" data-paper-title="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization Agent Scale AI 2026-08-06 主题：Harness 优化评测。在固定 target-evaluation 预算下，让优化器修改 prompt、工具、控制流和记忆；隐藏测试集与可信执行环境隔离搜索反馈，保留候选版本以供审计。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness 优化评测算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness 优化评测 Agent 评测与可靠性：如何知道真的做对了 为什么评测 harness 优化器要固定 target-evaluation 预算，而不只比较最终最高分？ 更多评测本身就提供更多搜索机会，不控预算会混淆优化能力与资源投入。隐藏测试隔离候选选择，可信环境及版本档案支持审计改了什么；报告相对收益还需注意基线尺度，不能把搜索反馈里见过的最佳候选成绩当最终未见表现。 例如一套优化器试一千次、另一套只试十次，即便前者最后更高，也不能直接说明更会优化；应先匹配评测调用预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-harnessopt-bench-502f5ddb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3dd81229ff5366d7">为什么评测 harness 优化器要固定 target-evaluation 预算，而不只比较最终最高分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnessopt-bench">HarnessOpt-Bench: Evaluating LLMs at Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Scale AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>更多评测本身就提供更多搜索机会，不控预算会混淆优化能力与资源投入。隐藏测试隔离候选选择，可信环境及版本档案支持审计改了什么；报告相对收益还需注意基线尺度，不能把搜索反馈里见过的最佳候选成绩当最终未见表现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一套优化器试一千次、另一套只试十次，即便前者最后更高，也不能直接说明更会优化；应先匹配评测调用预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06301">原论文</a> · <a href="../../../../agent-research/2608.06301-harnessopt-bench/">实现解读</a> · <a href="#qa-3dd81229ff5366d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:finance-harness-protocol" data-paper-title="FinanceHarness: Autonomous Financial Deep Research Framework" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="FinanceHarness: Autonomous Financial Deep Research Framework Agent Google Cloud AI Research 2026-07-30 FinanceHarness 围绕时点限定的搜索环境组织金融工具、分层加载技能与报告证据；FinanceGym 再把评分分为截止日前可检索的证据和只能在截止日后核实的预测。Agent 只能看到问题与截止日，thesis、评分 rubric、未来证据留在提交后的评测器。 完整实验成本过高，不复现（审查 DONE）；诊断使用历史/当日/未来/未知日期构造负控，另验证 live-web 审计会使运行无效，以及 1 条/3 条 rubric 的两题应均分为 0.5 而非 0.25；L1 纯 CPU 协议组件，diagnostic only，不是金融调研 Agent 能力，不提供投资建议。完整实验成本过高，不复现（审查 DONE）；无能力 adapter、未接入 Evolve。PointInTimeStore 保留外部检索排名，但过滤未来/日期未知文档，read 再独立检查，防止跳过搜索直接读未来材料。提交检查记录 live-web 使用或未读引用；触发后不可评分。  评测与可验证Agent 时点隔离与深度调研 Agent 评测与可靠性：如何知道真的做对了 截止日后可核实的预测，为什么必须留在提交后的评测器而非给研究 Agent？ 研究输入只能使用截止日前已可检索证据，未来材料若提前出现会把预测变成复述。thesis 与 rubric 也留在评分侧，分题归一后再平均以免题目条目数改变权重；时点泄漏使运行无效，不是随意记零或删行后继续汇总。 例如报告预测下一季度趋势，后来公布的业绩只能在提交后核查，不能倒填进截止日前证据包让模型看似提前判断正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-finance-harness-protocol-8c1ac9fa" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9ffeae55e9d1c6ba">截止日后可核实的预测，为什么必须留在提交后的评测器而非给研究 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afinance-harness-protocol">FinanceHarness: Autonomous Financial Deep Research Framework</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究输入只能使用截止日前已可检索证据，未来材料若提前出现会把预测变成复述。thesis 与 rubric 也留在评分侧，分题归一后再平均以免题目条目数改变权重；时点泄漏使运行无效，不是随意记零或删行后继续汇总。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如报告预测下一季度趋势，后来公布的业绩只能在提交后核查，不能倒填进截止日前证据包让模型看似提前判断正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27853v1">原论文</a> · <a href="../../../../agent-research/2607.27853-finance-harness-protocol/">实现解读</a> · <a href="#qa-9ffeae55e9d1c6ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:os-shepherd" data-paper-title="OSReward / OS-Shepherd" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OSReward / OS-Shepherd Agent The University of Hong Kong 2026-07-30 电脑操作 Agent 需要 reward model 判断完整轨迹是否真的完成任务，但普通 accuracy 会掩盖“几乎全判成功”的宽松偏差。OSReward 汇集 Windows、macOS、Ubuntu、Android 的人工验证任务与轨迹，同时发布 Hard 和 Multi 子集；统一报告 success recall、fail recall 与两者均值 balanced accuracy，并用 OS-Shepherd-100K 训练开放 9B/35B judge。 本页实现论文的 success/fail 双类召回、balanced accuracy 与 leniency 审计协议；确定性 mini-suite 不冒充官方人工标注轨迹或 OS-Shepherd 模型训练。本地没有下载官方截图轨迹或训练 9B/35B VLM judge，只把论文最重要的评测契约变成可执行基础设施。结果不能与官方模型表直接比较。本地 osreward-mini 覆盖四个平台与四类任务，显式区分“界面有活动”“有完成证据”和“仍有未完成要求”。判分器不能只信 Agent 的成功声明；  CUA Reward 评测 Agent 评测与可靠性：如何知道真的做对了 为什么普通 accuracy 会掩盖“几乎全判成功”的 reward model？ 若成功样本占多数，宽松裁判把所有轨迹判成功也可能得到不错总准确率，却漏掉真实失败。分别报告 success recall、fail recall 及其均值能揭示两类能力；跨系统与困难子集还需真实验证标签，不能把几条接口诊断当开放 judge 的能力测量。 例如九成样本成功，全判成功有九成 accuracy，但 fail recall 为零，balanced accuracy 只有一半，暴露对失败完全失明。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-os-shepherd-3f53da9c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-dc27e01fb888a3e5">为什么普通 accuracy 会掩盖“几乎全判成功”的 reward model？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aos-shepherd">OSReward / OS-Shepherd</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若成功样本占多数，宽松裁判把所有轨迹判成功也可能得到不错总准确率，却漏掉真实失败。分别报告 success recall、fail recall 及其均值能揭示两类能力；跨系统与困难子集还需真实验证标签，不能把几条接口诊断当开放 judge 的能力测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如九成样本成功，全判成功有九成 accuracy，但 fail recall 为零，balanced accuracy 只有一半，暴露对失败完全失明。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28609">原论文</a> · <a href="../../../../agent-research/2607.28609-osreward/">实现解读</a> · <a href="#qa-dc27e01fb888a3e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentdebugx" data-paper-title="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents Agent University of Illinois Urbana-Champaign 2026-07-21 AgentDebugX 在不可变原始轨迹外叠加 Detect、Attribute、Recover、Rerun 产物。DeepDebug 先全局读，再按单/多 Agent 结构独立定位；候选不一致时交叉质询，最终给出责任步骤、证据和具体建议。修复只生成建议，实际重跑仍经过人或 policy gate；不会从导入日志擅自重放任意外部工具。 完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；仅研究资料，没有可执行本地 adapter、模型指标或 Evolve 集成。完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。本地仅核对正文 §3/4 和 Appendix C、固定作者仓库及原图。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；DeepDebug 约 5 次模型调用，在 25 条样本上平均 12.8K token/诊断。  自进化与经验复用 轨迹调试与因果归因 Agent 评测与可靠性：如何知道真的做对了 为什么修复建议不能自动从导入日志重放任意外部工具？ 日志是观察资料，可能过时、缺权限或包含有副作用的调用；检测归因与授权执行应分开。不可变原轨迹上叠加假设和建议，真实重跑经人或 policy gate 后形成独立证据；诊断器若有参考答案等特权输入，也必须与无答案在线能力明确区分。 例如日志里有删除临时目录命令，调试器不能仅因导入了它就重新执行；应先建议修复，再由有权限的运行流程决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-agentdebugx-4b7d80dc" class="ar-learning-paper-anchor"></span>
<h2 id="qa-762711639f7eb829">为什么修复建议不能自动从导入日志重放任意外部工具？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentdebugx">AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>日志是观察资料，可能过时、缺权限或包含有副作用的调用；检测归因与授权执行应分开。不可变原轨迹上叠加假设和建议，真实重跑经人或 policy gate 后形成独立证据；诊断器若有参考答案等特权输入，也必须与无答案在线能力明确区分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如日志里有删除临时目录命令，调试器不能仅因导入了它就重新执行；应先建议修复，再由有权限的运行流程决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与评测边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18754v1">原论文</a> · <a href="../../../../agent-research/2607.18754-agentdebugx/">实现解读</a> · <a href="#qa-762711639f7eb829">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:logact" data-paper-title="LogAct: Enabling Agentic Reliability via Shared Logs" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LogAct: Enabling Agentic Reliability via Shared Logs Agent Meta 2026-04-09 LogAct 将 Agent 拆成 Driver、Voter、Decider 和 Executor，用持久共享日志记录意图、独立投票、commit/abort和执行结果，只有达到批准条件的已提交动作才能执行。它将安全审查与动作执行解耦，并保留崩溃后的不确定状态；外部副作用恢复仍需要明确的幂等或事务契约，不能只凭对话记录盲目重放。 模型具体身份、内部系统和完整复现费用无法用本轮单 A100/A30 或 Mac 的短时预算确定，依成本门槛标为成本过高，不复现（审查 DONE），不探测付费接口、不展开多机或长轨迹实验。DurableLogAct 用单机 SQLite 的 WAL、synchronous=FULL 和事务，将意图/投票/决策/执行状态与追加日志共同落盘。策略和 bus identity 在创建时固定，重开数据库不能悄悄降低 quorum；同一个 intent ID 也不能绑定另一动作。每个逻辑 Agent 至多一个未完成意图，失败未决会阻止后续意图越过它。  工具调用与环境执行 动作投票、持久提交与故障恢复 Agent 评测与可靠性：如何知道真的做对了 动作已在共享日志 commit，崩溃后为什么仍不能无条件再次执行？ 日志提交说明批准意图，不一定能确定外部副作用是否已经发生；崩溃可能出现在调用成功但回执未写入之间。恢复需幂等键或事务契约区分未执行与已执行，独立投票也只控制批准过程，不能凭对话记录保证外部 exactly-once。 例如付款调用成功后进程崩溃，日志没有结果；直接重放可能重复扣款，应依赖幂等或事务查询，而非只看 commit 状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-logact-bec0d56e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-219db6899dfab0c3">动作已在共享日志 commit，崩溃后为什么仍不能无条件再次执行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alogact">LogAct: Enabling Agentic Reliability via Shared Logs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>日志提交说明批准意图，不一定能确定外部副作用是否已经发生；崩溃可能出现在调用成功但回执未写入之间。恢复需幂等键或事务契约区分未执行与已执行，独立投票也只控制批准过程，不能凭对话记录保证外部 exactly-once。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如付款调用成功后进程崩溃，日志没有结果；直接重放可能重复扣款，应依赖幂等或事务查询，而非只看 commit 状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07988v1">原论文</a> · <a href="../../../../agent-research/2604.07988-logact/">实现解读</a> · <a href="#qa-219db6899dfab0c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tfrbench" data-paper-title="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems Agent Google Cloud AI Research / University of Kentucky 2026-04-07 预测值接近真值不保证推理有根据，流畅推理也可能导致错误预测。论文联合 Search、Reason、Forecast、Verify、Summary 构建数值与推理同时合格的参考轨迹。标签参与参考筛选与反馈，因此这个构建过程不能直接作为留出能力成绩。原文 Algorithm 1 完整实验成本过高，不复现（审查 DONE）。CPU 评分与参考构建协议，当前仅 L0 固定回调验证。有标签参考构建不是无泄露预测评测。完整实验成本过高，不复现（审查 DONE）。ForecastView 只含 history、reasoning、horizon、description，不包含未来 target。未来值由 OutcomeEvaluator 持有。Python 回调是受信任代码，不是安全沙箱，不能阻止外部 callback 自行读取文件或闭包中的目标值；接真实模型时还要审计提供方信息流。  Agent 评测 时间序列预测推理 Agent 评测与可靠性：如何知道真的做对了 长推理轨迹达到参考门槛，为什么摘要还要单独预测并再次过门？ 摘要可能省掉决定预测的关键证据或条件，不能继承原轨迹的正确性。数值误差与推理一致性共同约束参考，且标签参与筛选只说明构建质量，不是留出能力成绩；历史尺度为零时指标未定义，应拒绝而非加任意 epsilon 制造良好结果。 例如长轨迹解释季节变化并预测正确，摘要只剩“趋势向上”后重新预测可能失准，需要独立验证压缩是否保留了依据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-tfrbench-2bbb3dcd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9748b5565a2ace11">长推理轨迹达到参考门槛，为什么摘要还要单独预测并再次过门？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atfrbench">TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / University of Kentucky</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>摘要可能省掉决定预测的关键证据或条件，不能继承原轨迹的正确性。数值误差与推理一致性共同约束参考，且标签参与筛选只说明构建质量，不是留出能力成绩；历史尺度为零时指标未定义，应拒绝而非加任意 epsilon 制造良好结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长轨迹解释季节变化并预测正确，摘要只剩“趋势向上”后重新预测可能失准，需要独立验证压缩是否保留了依据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05364">原论文</a> · <a href="../../../../agent-research/2604.05364-tfrbench/">实现解读</a> · <a href="#qa-9748b5565a2ace11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:convapparel" data-paper-title="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders Agent Google 2026-02-18 模拟用户能完成购物目标，不等于像真人。论文将验证拆成三条互补证据：PLSA 比较行为分布；HLS 检查训练过的真假对话判别器能否识别模拟；反事实验证把仅在一种推荐策略下训练的模拟器放到另一策略下。PLSA 的全称是 Population-Level Statistical Alignment，不是同名主题模型。原文 §4 完整实验成本过高，不复现（审查 DONE）。本地为 CPU evaluation_protocol_interface，不是完整模拟器复现。公开固定刺激只检验 L0 接口；完整实验成本过高，不复现（审查 DONE）。也可传 --input conversations.json 代替 --fixture-demo：JSON 顶层为 train 与 heldout 数组，每行有 session_id、participant_id、policy、user_turns、布尔 is_human、可选 annotations。  Agent 评测 用户模拟器与分布对齐 Agent 评测与可靠性：如何知道真的做对了 为什么模拟购物目标成功，并不能证明用户模拟器像真人？ 任务成功只反映与当前推荐策略配合完成目标，模拟器可能语气、行为分布或响应规律都不真实。群体统计、训练过的真假判别与跨策略反事实分别检查不同维度，互相不能替代；HLS 是判别器真人概率，不是购物成功率或人类真实认可。 例如模拟用户每次立刻接受第一款商品，目标完成很快，却不像真人反复比较；换另一推荐策略时还可能完全失效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-convapparel-e8aab87b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cd3497205b271356">为什么模拟购物目标成功，并不能证明用户模拟器像真人？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aconvapparel">ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务成功只反映与当前推荐策略配合完成目标，模拟器可能语气、行为分布或响应规律都不真实。群体统计、训练过的真假判别与跨策略反事实分别检查不同维度，互相不能替代；HLS 是判别器真人概率，不是购物成功率或人类真实认可。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模拟用户每次立刻接受第一款商品，目标完成很快，却不像真人反复比较；换另一推荐策略时还可能完全失效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16938">原论文</a> · <a href="../../../../agent-research/2602.16938-convapparel/">实现解读</a> · <a href="#qa-cd3497205b271356">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-armor" data-paper-title="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution Agent Google Cloud AI Research 2026-02-08 在高权限动作前，分别去掉用户请求与不可信工具段，比较同一个动作的似然变化。工具段的归因高于用户时，只清洗命中段，再遮蔽首个命中点后的 assistant 内容并重新提案。§3–4、Algorithm 1 完整实验：成本过高，不复现（审查 DONE）。CPU 诊断记录 component_only / L1。真实似然算子与安全失败的干预接口，不是已验证的注入检测器。完整实验：成本过高，不复现（审查 DONE）。7 项 CPU 契约测试通过：LOO 分离、动作长度归一化、margin 严格边界、选择性清洗、历史遮蔽、缺回调扣留和非高权限跳过。固定 fixture 仅验证公式，不计算安全准确率。CPU 诊断记录  Agent 安全 提示注入防御 因果归因 Agent 评测与可靠性：如何知道真的做对了 去掉不可信工具段后动作似然下降，为什么还不能直接称作因果安全证明？ 留一消融是操作性归因，表明该段影响同一动作概率，但删除也可能改变上下文结构或移走合法证据。方法与用户请求归因比较，只清洗命中段，再遮蔽受污染后续并重新提案；阈值方向与重算流程需保持原义，单个低用户归因不是攻击结论。 例如网页某段既含必要数值也含可疑指令，删段使动作概率下降不全是恶意影响；还需比较来源与具体动作的关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-causal-armor-73cc1cba" class="ar-learning-paper-anchor"></span>
<h2 id="qa-58882c2ee223a900">去掉不可信工具段后动作似然下降，为什么还不能直接称作因果安全证明？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acausal-armor">CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>留一消融是操作性归因，表明该段影响同一动作概率，但删除也可能改变上下文结构或移走合法证据。方法与用户请求归因比较，只清洗命中段，再遮蔽受污染后续并重新提案；阈值方向与重算流程需保持原义，单个低用户归因不是攻击结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如网页某段既含必要数值也含可疑指令，删段使动作概率下降不全是恶意影响；还需比较来源与具体动作的关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07918">原论文</a> · <a href="../../../../agent-research/2602.07918-causal-armor/">实现解读</a> · <a href="#qa-58882c2ee223a900">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:airs-bench" data-paper-title="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents Agent FAIR at Meta / University of Oxford 2026-02-06 以问题、数据集、指标和人工SOTA定义20个任务。Agent自行提出方法、实现训练、分析实验并修订，不提供基线解法；协议区分Agent、搜索scaffold与运行harness，比较顺序MLGym和树搜索AIRA-dojo。原文§3–5 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；任务规范收录不等于已接入benchmark。原文每次运行24小时、独占1张H200，20个任务；附录D还列每任务10至20次运行。单A100/A30或Mac下，成本过高，不复现（审查 DONE）。原文附录C–D  自动研究 研究Agent评测协议 Agent 评测与可靠性：如何知道真的做对了 为什么只给问题、数据与指标，而不直接给基线解法，更能测研究 Agent？ 研究过程包括提出方法、实现训练、分析实验和修订，给出完整基线方案会缩小自主设计部分。协议还要区分 Agent、搜索 scaffold 与运行 harness，避免把外层树搜索收益全归模型；任务上人工 SOTA 是参照，不是行动者可偷读的答案脚本。 例如给分类数据与评分规则，让 Agent 自己决定模型和实验；若已提供最佳训练代码，评测更接近执行脚本而非研究设计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-airs-bench-3e226cbd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a7d53ec839366385">为什么只给问题、数据与指标，而不直接给基线解法，更能测研究 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aairs-bench">AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究过程包括提出方法、实现训练、分析实验和修订，给出完整基线方案会缩小自主设计部分。协议还要区分 Agent、搜索 scaffold 与运行 harness，避免把外层树搜索收益全归模型；任务上人工 SOTA 是参照，不是行动者可偷读的答案脚本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给分类数据与评分规则，让 Agent 自己决定模型和实验；若已提供最佳训练代码，评测更接近执行脚本而非研究设计。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06855">原论文</a> · <a href="../../../../agent-research/2602.06855-airs-bench/">实现解读</a> · <a href="#qa-a7d53ec839366385">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lifeagentbench" data-paper-title="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning Agent University of California San Diego 2026-01-20 LifeAgentBench 用可执行 SQL / 程序在饮食、睡眠、活动和情绪记录上生成确定性答案，覆盖长期窗口、跨维度与跨用户任务。LifeAgent 是另一个工具推理基线：先分解子问题，维护证据缓存与中间统计，再根据新证据修订计划并合成回答，不能把 benchmark scorer 当成该 Agent。 完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。仅研究资料，未实现 LifeAgent 或运行 benchmark。完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。正文 Appendix E 明确开放模型推理约 300–500 GPU 小时；含 70B 的较大模型使用 4×A6000，另有闭源 API 和多轮工具基线。这不是单次小样本推理可以重现的整套比较。完整实验成本过高，不复现（审查 DONE）；不下载生活记录、权重或大数据，不运行推理，也不生成本地 metrics / GPU receipt。后续不会自动重试。  评测与可验证Agent 长期异构记录推理 Agent 评测与可靠性：如何知道真的做对了 SQL scorer 能算出确定答案，为什么不等于已实现 LifeAgent 的工具推理？ scorer 持有规则与记录来验证最终答案，不承担分解问题、检索证据、维护中间统计和修订计划。基准与工具基线的职责不同，不能让行动者直接读参考计算或把通过字段检查当成长期健康记录推理；这里只说明数据任务协议，不提供健康决策建议。 例如验证器能计算一周平均睡眠，Agent 仍须自己选时间窗、查询记录并核对缺失项；调用参考答案函数会绕过这些步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-lifeagentbench-23550dc3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d23f60fee3459ab1">SQL scorer 能算出确定答案，为什么不等于已实现 LifeAgent 的工具推理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alifeagentbench">LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>scorer 持有规则与记录来验证最终答案，不承担分解问题、检索证据、维护中间统计和修订计划。基准与工具基线的职责不同，不能让行动者直接读参考计算或把通过字段检查当成长期健康记录推理；这里只说明数据任务协议，不提供健康决策建议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如验证器能计算一周平均睡眠，Agent 仍须自己选时间窗、查询记录并核对缺失项；调用参考答案函数会绕过这些步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13880v1">原论文</a> · <a href="../../../../agent-research/2601.13880-lifeagentbench/">实现解读</a> · <a href="#qa-d23f60fee3459ab1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coreflect" data-paper-title="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation Agent University of Illinois Urbana-Champaign 2026-01-18 Sec.2.1–2.5 / Appendix G：953条通过真实LLM一致性检查的persona-scenario；planner/simulator/evaluator/analyzer是核心语义模型。只写JSON状态机、对给定数字求均值或手工替换rubric都不能复现其核心，因此不强建低成本heuristic adapter。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  Agent评测与自进化 对话模拟与rubric共演化 Agent 评测与可靠性：如何知道真的做对了 为什么只更新 rubric 字符串或对给定分数求均值，不能复现 CoReflect 的反思共演化？ 核心需要语义 planner 生成情境、simulator 产生对话、evaluator 评价，再由 analyzer 依据理由发现不足并同时改任务与准则。机械状态转移只实现外壳，没有这些语义判断与真实交互证据；原方法公式用于解释流程，不能被当成本地模块已运行。 例如分析器应发现某类同理心评价遗漏再产生新情境，手工把权重从一改成二并不会自动获得这类语义反思能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-coreflect-7d1f277e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9336a21730fbc0d6">为什么只更新 rubric 字符串或对给定分数求均值，不能复现 CoReflect 的反思共演化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoreflect">CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>核心需要语义 planner 生成情境、simulator 产生对话、evaluator 评价，再由 analyzer 依据理由发现不足并同时改任务与准则。机械状态转移只实现外壳，没有这些语义判断与真实交互证据；原方法公式用于解释流程，不能被当成本地模块已运行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如分析器应发现某类同理心评价遗漏再产生新情境，手工把权重从一改成二并不会自动获得这类语义反思能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12208v1">原论文</a> · <a href="../../../../agent-research/2601.12208-coreflect/">实现解读</a> · <a href="#qa-9336a21730fbc0d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sopbench-protocol" data-paper-title="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints Agent University of California, Santa Barbara 2025-03-11 SOPBench 将服务规范写成有向约束图：Agent 必须先调用 helper 检验必要条件，再执行服务。它不仅核对最终数据库是否正确，还检查服务本身是否被允许、必要验证是否真正且按要求发生，防止“猜中结果”绕过流程。 完整实验成本过高，不复现（审查 DONE）；诊断只检查构造轨迹的顺序、错误用户、错误状态及 oracle 负控，报告 fixture 数，不报模型成功率。L1 纯 CPU 协议组件，diagnostic only，不是模型能力或七域环境复现。完整实验成本过高，不复现（审查 DONE）；未接入 Evolve。Rule 以嵌套表达式表示约束；evaluate_trace 对每一次服务调用只看其之前的 helper 前缀，并将三项检查联合。参考约束真值、oracle 最终状态都只由轨迹提交后的评测器使用，没有传给任何被测策略。拒绝服务可以通过，但必须与 oracle 的数据库结果一致；  工具使用与环境 SOP约束与程序验收 Agent 评测与可靠性：如何知道真的做对了 数据库最终状态正确，为什么仍可能在 SOPBench 判失败？ 服务还需被允许，必要 helper 验证也要实际且按规定顺序发生。And、Or 与 Chain 表达不同前提逻辑，不能仅凭猜中结果绕过流程；完整通过要求资格、数据库与程序共同成立，把三者合并成最终状态检查会遗漏协议遵循能力。 例如退款金额碰巧正确，但 Agent 没先验证订单资格，仍违反 SOP；Chain 要求先查资格再操作，事后补查不能抵消。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-sopbench-protocol-97674f6a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bf216373788d6b3c">数据库最终状态正确，为什么仍可能在 SOPBench 判失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asopbench-protocol">SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>服务还需被允许，必要 helper 验证也要实际且按规定顺序发生。And、Or 与 Chain 表达不同前提逻辑，不能仅凭猜中结果绕过流程；完整通过要求资格、数据库与程序共同成立，把三者合并成最终状态检查会遗漏协议遵循能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如退款金额碰巧正确，但 Agent 没先验证订单资格，仍违反 SOP；Chain 要求先查资格再操作，事后补查不能抵消。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.08669v1">原论文</a> · <a href="../../../../agent-research/2503.08669-sopbench-protocol/">实现解读</a> · <a href="#qa-bf216373788d6b3c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gaia" data-paper-title="GAIA" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GAIA Agent Meta AI 2023-11-21 以 466 个真实问题联合考查推理、多模态、网页浏览与工具使用，采用精确短答案和三级难度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。gaia-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.4000。  通用 Agent 评测 Agent 评测与可靠性：如何知道真的做对了 精确短答案为什么仍能考查多工具推理，而不只是记忆问答？ 简短输出只是评分接口，得到答案可能需要浏览、多模态理解、计算与跨来源核对。规范化匹配把终点判断变得明确，却不显示中间证据质量，也不能独立解释失败来自哪一步；答对率需与真实执行轨迹区分，参考短答案不能提前进 Agent 提示。 例如最终只输出一个年份，但需要先从图片识别人名，再浏览资料查事件并核对时间；短输出并不代表求解过程简单。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-gaia-62649810" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7f1f7590b48a18a3">精确短答案为什么仍能考查多工具推理，而不只是记忆问答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agaia">GAIA</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>简短输出只是评分接口，得到答案可能需要浏览、多模态理解、计算与跨来源核对。规范化匹配把终点判断变得明确，却不显示中间证据质量，也不能独立解释失败来自哪一步；答对率需与真实执行轨迹区分，参考短答案不能提前进 Agent 提示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最终只输出一个年份，但需要先从图片识别人名，再浏览资料查事件并核对时间；短输出并不代表求解过程简单。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.12983">原论文</a> · <a href="../../../../agent-research/2311.12983-gaia/">实现解读</a> · <a href="#qa-7f1f7590b48a18a3">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

怎样区分模型成功、环境碰巧放行、评分器偏差和不安全的越权？

## 记住这一点

先固定任务、可见输入、允许动作、成功条件和预算，再讨论分数。GAIA 用需要推理与工具的真实问题考查端到端结果；扰动协议进一步控制某个输入因素变化，检验系统是否仍完成同一目标。安全评估还要问动作是否有依据、有权限，不能仅以最终答案正确为由放过越权。评分器与 actor 的信息边界是协议的一部分。

## 一个例子

给同一任务做两次运行，只改变工具说明中的一个无关冗余字段，其余后端、数据和成功条件都固定，才能研究这类扰动的影响。如果改动顺带删掉必要参数，任务已不可解，就不能简单把失败计为“不稳健”。若评分过程超时，应同时报告已评分结果和未评分数量，而非删掉未知样本。

## 什么时候要小心

语法合法不代表语义保持，模拟器高分也不等于真人或生产效果。库里的 GAIA mini-suite 和 AgentPerturb CPU 协议接口不是官方完整 benchmark 接入；安全夹具也不证明真实攻击防御率。只做文献和成本审查的条目不能出现在已验证能力清单。

## 先读这几篇

先读 GAIA，明确端到端任务与难度；再读 AgentPerturb，理解单因素、目标保持和独立验证的配对评测。阅读每篇本地边界，分别识别官方任务、CPU协议诊断和未运行部分。

1. [GAIA](../../../agent-research/2311.12983-gaia/README.md) · [原论文](https://arxiv.org/abs/2311.12983)
2. [AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations](../../../agent-research/2610.21624-agent-perturb/README.md) · [原论文](https://arxiv.org/abs/2610.21624)

## 自测一下

100项任务中只完成80项评分，其中60项成功；可以只报告75%成功率并省略剩余20项吗？

??? note "展开参考答案"

    应说明75%是已评分子集的条件成功率，同时保留完整100项分母与20项未知结果。若任务同权，整体成功率目前只能界定在60%到80%之间。进一步归因需要区分执行失败、评分中断和真正任务错误。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
