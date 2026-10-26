---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 规划与搜索：下一步该做什么

[Agent](index.md) / 16 个问题 · 16 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">16 个问题 · 16 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:drago" data-paper-title="Repairing LLM-Generated Specifications with Deterministic Diagnosis" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Repairing LLM-Generated Specifications with Deterministic Diagnosis Agent University of Oxford 2026-10-15 形式规格“能运行”不等于“忠实表达了题意”。DRAGO 将 SMT-LIB2、MiniZinc 和 PDDL 的契约、求解器探针及题意对齐检查转为可定位诊断，再要求模型定向修复。候选必须保留语法/词表/输出合同，严格降低阻塞诊断，并满足防退化条件；参考形式化和最终标签只用于最后评分。方法 §3、附录 A.2 原图建议：原论文 Figure 2 为诊断/接纳消融；Figure 3 为 Planetarium 输入渲染缺陷。它们分别解释算法贡献和评测风险。 原文用 4×A100 服务30B/31B模型，跨5个 benchmark 多seed、多臂重评估，完整实验成本过高，不复现（审查 DONE）。实现 grounded STRIPS/PDDL 方向的诊断算子子集；component_only / L1 CPU。实现 grounded STRIPS/PDDL 方向的诊断算子子集；不冒充完整三形式化语言框架。CPU fixture 随机化走廊规模，实际执行无前提路径、联合目标冲突、预算耗尽、证据支持的初态修复，以及“删掉目标就算修好”的负对照。proposal 回调只拿公开 Problem 和 Diagnosis，不拿金标准。  规划与搜索 形式规格诊断与保守修复 Agent 规划与搜索：下一步该做什么 为什么求解器返回可解，还不能证明形式规格忠实表达了题意？ 求解器只判断写下来的约束，不知道自然语言要求是否被遗漏或偷换。DRAGO 把词表合同、可达性探针与题意对齐分开诊断，修复必须严格减少阻塞且不删除目标来投机；探针耗尽预算只能报未知，不能捏造成已证明无解。 例如题目要求同时到达两处，错误规格只写一处也可能可解；删掉困难目标会降低求解难度，却不是正确修复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-drago-838b0a34" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f6e1c82bffcc2da5">为什么求解器返回可解，还不能证明形式规格忠实表达了题意？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adrago">Repairing LLM-Generated Specifications with Deterministic Diagnosis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>求解器只判断写下来的约束，不知道自然语言要求是否被遗漏或偷换。DRAGO 把词表合同、可达性探针与题意对齐分开诊断，修复必须严格减少阻塞且不删除目标来投机；探针耗尽预算只能报未知，不能捏造成已证明无解。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如题目要求同时到达两处，错误规格只写一处也可能可解；删掉困难目标会降低求解难度，却不是正确修复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22568">原论文</a> · <a href="../../../../agent-research/2610.22568-drago/">实现解读</a> · <a href="#qa-f6e1c82bffcc2da5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:janus" data-paper-title="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-10-09 在研究图中先生成未执行提案，再预测价值提升、信息增益和探索收益；稀疏 pairwise tournament 拟合软 Bradley–Terry 分数。执行选中实验后，从成功/失败抽象 intra/cross-task 技能并更新预测、探索、协调协议。事实来源：原文全文。 不同浮点 backend 也不能在未验证时声称 logits bit-exact，见 PyTorch 官方 SDPA 说明。当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始几何可行程序；原文对照完整自主研究框架；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  autonomous-research world-model evolving-skills Agent 规划与搜索：下一步该做什么 为什么实验提案先做成对比较，再拟合价值分数，而不是直接选描述最精彩的方案？ 成对比较让价值提升、信息增益与探索收益形成可校准的相对次序，稀疏锦标赛再用 Bradley–Terry 分数连接这些局部判断。预测用于分配实验预算，执行后的成功与失败又更新模型和技能；预测高分不等于实验已成功，也不能替代真实执行。 例如方案甲预期涨分高、乙更能排除关键假设，可按剩余预算调整探索权重，而不是把两句漂亮承诺当作结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-janus-c8240d07" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d051e2e09bf28dfd">为什么实验提案先做成对比较，再拟合价值分数，而不是直接选描述最精彩的方案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajanus">Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成对比较让价值提升、信息增益与探索收益形成可校准的相对次序，稀疏锦标赛再用 Bradley–Terry 分数连接这些局部判断。预测用于分配实验预算，执行后的成功与失败又更新模型和技能；预测高分不等于实验已成功，也不能替代真实执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如方案甲预期涨分高、乙更能排除关键假设，可按剩余预算调整探索权重，而不是把两句漂亮承诺当作结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13194">原论文</a> · <a href="../../../../reproductions/2610.13194-janus/">实现解读</a> · <a href="#qa-d051e2e09bf28dfd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-lookahead" data-paper-title="Code Owns the Simulation, Jev Owns the Evaluation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Code Owns the Simulation, Jev Owns the Evaluation Agent The Chinese University of Hong Kong 2026-10-01 让可执行代码负责模拟每个动作的后继状态，让 Jev 只负责比较动作带来的进展。除了当前动作和下一观察，还显式提供“执行后新出现的可用动作”，降低纯语义动作评分难以预判长期可达性的缺陷。 L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；本地实验使用显式词法诊断 provider，没有调用真实 Jev，也不是 ALFWorld 成功率复现。尚未运行真实 Jev checkpoint/托管 API、ALFWorld 或机器人环境；本次不新增 CUDA 路径，不宣称 GPU 验证或 Evolve 能力提升。System One 方法索引保留交叉入口。运行 PYTHONPATH=src python scripts/run_oct04_seven_papers.py。  模拟前瞻与动作选择 System One Agent 规划与搜索：下一步该做什么 提供“后继状态新出现的可用动作”，比只给下一观察多了什么？ 下一观察描述眼前变化，新动作集合则揭示该步打开了哪些后续通路，有助于比较短期无收益但长期有价值的动作。代码在克隆状态中负责真实模拟，决策模型只评公开后果；模拟器 reward 或正确计划不能作为偷偷提供给评分器的答案。 例如拿到钥匙暂时没有完成任务，却新增“打开侧门”的合法动作；看见这一机会才能评价取钥匙的长期意义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-jev-lookahead-d66c9de4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bb996b26be801ddf">提供“后继状态新出现的可用动作”，比只给下一观察多了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-lookahead">Code Owns the Simulation, Jev Owns the Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>下一观察描述眼前变化，新动作集合则揭示该步打开了哪些后续通路，有助于比较短期无收益但长期有价值的动作。代码在克隆状态中负责真实模拟，决策模型只评公开后果；模拟器 reward 或正确计划不能作为偷偷提供给评分器的答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如拿到钥匙暂时没有完成任务，却新增“打开侧门”的合法动作；看见这一机会才能评价取钥匙的长期意义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01834">原论文</a> · <a href="../../../../agent-research/2610.01834-jev-lookahead/">实现解读</a> · <a href="#qa-bb996b26be801ddf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-spawn" data-paper-title="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces Agent 原文首页未列第一作者机构 2026-09-30 先从自然语言任务构造有限 compositional action space，以 Jev 分布并行保留多个分支；反馈更新后验并保留备选以支持恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Jev Agent 推理 分支搜索 Agent 规划与搜索：下一步该做什么 为什么保留多个动作分支，而不在第一次分布输出后立刻只留最高分？ 早期概率可能不准，多个组合动作保留了遇到反证时恢复的余地。新反馈对先验重新加权，后验应影响后续探索而不是回写过去的成功标签；分支数同时消耗预算，因此并行保留是风险与计算的取舍，不是自动穷尽所有可能。 例如先保留“搜索资料”和“检查本地文件”两条路，搜索无结果后仍能转向已保留的检查分支，而不必从零重建计划。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-jev-spawn-dc827975" class="ar-learning-paper-anchor"></span>
<h2 id="qa-03aec54a5d1918af">为什么保留多个动作分支，而不在第一次分布输出后立刻只留最高分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-spawn">JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早期概率可能不准，多个组合动作保留了遇到反证时恢复的余地。新反馈对先验重新加权，后验应影响后续探索而不是回写过去的成功标签；分支数同时消耗预算，因此并行保留是风险与计算的取舍，不是自动穷尽所有可能。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先保留“搜索资料”和“检查本地文件”两条路，搜索无结果后仍能转向已保留的检查分支，而不必从零重建计划。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00437">原论文</a> · <a href="../../../../agent-research/2610.00437-jev-spawn/">实现解读</a> · <a href="#qa-03aec54a5d1918af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-reasoning" data-paper-title="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning Agent Meta Superintelligence Labs 2026-09-29 把对象级工作交给 worker，把控制本身拆成 Assess、Propose、Evaluate 和 Dispatch；控制器只携带紧凑状态，通过持久 artifact memory 复用既有工作，并在统一调用预算内决定继续、分叉或停止。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agent 推理 元推理控制 预算调度 Agent 规划与搜索：下一步该做什么 为什么控制器使用紧凑状态，却把完整工作成果放到 artifact memory？ 控制决策只需掌握进度、候选动作和剩余预算，完整材料若反复进入提示会增加成本。持久工件保存可复用证据，控制器按需引用，再通过 Assess、Propose、Evaluate、Dispatch 分工决定继续或分叉；压缩控制状态不应把真实成果一并丢掉。 例如两名 worker 已各写一份分析，控制器只保留结论与文件引用，需要核对时再打开原工件，无需每轮重抄全文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-meta-reasoning-f28ad63c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-df8ee4a8b86d9461">为什么控制器使用紧凑状态，却把完整工作成果放到 artifact memory？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ameta-reasoning">Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>控制决策只需掌握进度、候选动作和剩余预算，完整材料若反复进入提示会增加成本。持久工件保存可复用证据，控制器按需引用，再通过 Assess、Propose、Evaluate、Dispatch 分工决定继续或分叉；压缩控制状态不应把真实成果一并丢掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两名 worker 已各写一份分析，控制器只保留结论与文件引用，需要核对时再打开原工件，无需每轮重抄全文。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38147">原论文</a> · <a href="../../../../agent-research/2609.38147-meta-reasoning/">实现解读</a> · <a href="#qa-df8ee4a8b86d9461">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage-planner" data-paper-title="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners Agent 原文首页未列机构 2026-09-28 执行前用符号前置条件门阻止不安全动作并给出类型化原因；失败时只重写相关子目标的后缀，保留已完成前缀。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  规划 安全门 局部恢复 Agent 规划与搜索：下一步该做什么 失败后为什么只编辑相关子目标的后缀，而不重写整条计划？ 已完成前缀对应真实执行状态，全部重写容易重复动作或假设环境回到了起点。符号门先依据前置条件拦截并给类型化原因，再让规划器修复受影响的后续部分；保留前缀不是盲目坚持旧计划，而是维持与当前世界一致的执行历史。 例如杯子已经洗净、下一步发现柜门锁住，应修改放置方案，而不再把“洗杯子”重复执行并假设柜门早已打开。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-sage-planner-6e4e53de" class="ar-learning-paper-anchor"></span>
<h2 id="qa-30cc5def5f86c48d">失败后为什么只编辑相关子目标的后缀，而不重写整条计划？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asage-planner">SAGE: Symbolic Action-Gating and Editing for LLM Task Planners</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>已完成前缀对应真实执行状态，全部重写容易重复动作或假设环境回到了起点。符号门先依据前置条件拦截并给类型化原因，再让规划器修复受影响的后续部分；保留前缀不是盲目坚持旧计划，而是维持与当前世界一致的执行历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如杯子已经洗净、下一步发现柜门锁住，应修改放置方案，而不再把“洗杯子”重复执行并假设柜门早已打开。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34268">原论文</a> · <a href="../../../../agent-research/2609.34268-sage/">实现解读</a> · <a href="#qa-30cc5def5f86c48d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searchatlas" data-paper-title="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs Agent Duke University 2026-09-09 把搜索轨迹转为 query—evidence—answer 有向图，审计证据是否真正覆盖问题约束和最终回答。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  搜索 Agent 过程审计 Agent 规划与搜索：下一步该做什么 为什么搜索很多网页仍可能在 evidential query graph 中暴露证据缺口？ 网页数量不是约束覆盖率。查询、证据与回答的有向关系要说明哪条证据支持哪个问题条件，最终结论是否跨越了未验证的边。图审计因此能区分重复搜到相同内容与真正补齐推理链；建立图的接口通过，也不等于搜索模型已经能可靠取证。 例如十篇网页都只说明产品价格，却没有一篇确认地区可用性；最终宣称“当地可以买到”仍缺少对应证据边。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-searchatlas-1aefb816" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f159d742140bf711">为什么搜索很多网页仍可能在 evidential query graph 中暴露证据缺口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearchatlas">SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>网页数量不是约束覆盖率。查询、证据与回答的有向关系要说明哪条证据支持哪个问题条件，最终结论是否跨越了未验证的边。图审计因此能区分重复搜到相同内容与真正补齐推理链；建立图的接口通过，也不等于搜索模型已经能可靠取证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十篇网页都只说明产品价格，却没有一篇确认地区可用性；最终宣称“当地可以买到”仍缺少对应证据边。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10901">原论文</a> · <a href="../../../../agent-research/2609.10901-searchatlas/">实现解读</a> · <a href="#qa-f159d742140bf711">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deeprepro" data-paper-title="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-08-27 一次性全局计划会在文件、依赖和接口持续变化时失效。DeepRepro 在每个阶段读取当前 repository state 和执行反馈，重写细粒度 subplan，再由 repository-aware orchestration 推进实现。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现 repository snapshot、state-aware subplan 与 runtime-feedback repair。未运行官方 PaperBench Code-Dev，也未把 deterministic plan/answer 满分包装成论文结果；本地验证的是状态驱动重规划路径。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300，并记录 state snapshots、subplan revisions 与 repairs。  论文到代码状态子规划 Agent 规划与搜索：下一步该做什么 为什么论文到代码的子计划必须读取当前仓库状态，而不能只按论文顺序展开？ 实现过程中接口、依赖和文件会不断变化，上一阶段成立的假设可能已失效。细粒度子计划把当前 repository state 与执行反馈作为输入，重新决定下一步；论文定义提供目标约束，仓库状态提供可执行条件，二者都不能由初始的一份静态清单替代。 例如论文下一步要接评测器，但仓库刚改了数据接口；子计划应先适配新合同，而非照旧生成无法连接的实验脚本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-deeprepro-1ec5a199" class="ar-learning-paper-anchor"></span>
<h2 id="qa-07944eab0463db0d">为什么论文到代码的子计划必须读取当前仓库状态，而不能只按论文顺序展开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adeeprepro">DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实现过程中接口、依赖和文件会不断变化，上一阶段成立的假设可能已失效。细粒度子计划把当前 repository state 与执行反馈作为输入，重新决定下一步；论文定义提供目标约束，仓库状态提供可执行条件，二者都不能由初始的一份静态清单替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如论文下一步要接评测器，但仓库刚改了数据接口；子计划应先适配新合同，而非照旧生成无法连接的实验脚本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26557">原论文</a> · <a href="../../../../agent-research/2608.26557-deeprepro/">实现解读</a> · <a href="#qa-07944eab0463db0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loongreflect" data-paper-title="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation Agent Authors did not disclose affiliation 2026-08-12 把 reflect/backtrack 视为可逆轨迹树的 memory-control actions，以 privileged teacher 快通道和 outcome GRPO 慢通道协调训练。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  反思 Agentic RL Agent 规划与搜索：下一步该做什么 为什么 reflect/backtrack 要建模为可逆的 memory-control actions？ 长搜索不仅选择外部动作，也要控制保留哪些轨迹、回到哪个分叉点。把反思和回退显式纳入策略，才能学习何时改变记忆状态；特权教师提供训练信号，结果奖励补充长期成败，但评测时不能把教师的全局视角或未来答案直接交给学生。 例如搜索走入死胡同后应回到前一个分支并保留失败原因；仅追加一段反思文字却不改变轨迹状态，不能实现真正回退。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-loongreflect-7debd709" class="ar-learning-paper-anchor"></span>
<h2 id="qa-47d09fe862087bb4">为什么 reflect/backtrack 要建模为可逆的 memory-control actions？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aloongreflect">LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长搜索不仅选择外部动作，也要控制保留哪些轨迹、回到哪个分叉点。把反思和回退显式纳入策略，才能学习何时改变记忆状态；特权教师提供训练信号，结果奖励补充长期成败，但评测时不能把教师的全局视角或未来答案直接交给学生。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索走入死胡同后应回到前一个分支并保留失败原因；仅追加一段反思文字却不改变轨迹状态，不能实现真正回退。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11967">原论文</a> · <a href="../../../../agent-research/2608.11967-loongreflect/">实现解读</a> · <a href="#qa-47d09fe862087bb4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toollift" data-paper-title="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning Agent Authors did not disclose affiliation 2026-08-04 把工具级历史轨迹提升为可跨工具集迁移的 function workflow graph，再解耦 workflow planning 与 tool selection。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 图结构 Agent 规划与搜索：下一步该做什么 把轨迹提升为 function workflow graph，为什么有利于换一套工具后复用计划？ 功能图保留“需要完成哪种操作及其依赖”，把具体工具名称与接口推迟到执行时选择。换工具集后仍可沿功能关系规划，再按当前 schema 找实现；这不是忽略参数合同，功能节点仍须由具备所需输入输出能力的真实工具完成。 例如旧工具叫 search_web、新工具叫 lookup，若二者都实现查找证据功能，工作流可复用，但参数与返回格式还须重新匹配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-toollift-dbb897af" class="ar-learning-paper-anchor"></span>
<h2 id="qa-830b9099c62167a8">把轨迹提升为 function workflow graph，为什么有利于换一套工具后复用计划？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoollift">ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>功能图保留“需要完成哪种操作及其依赖”，把具体工具名称与接口推迟到执行时选择。换工具集后仍可沿功能关系规划，再按当前 schema 找实现；这不是忽略参数合同，功能节点仍须由具备所需输入输出能力的真实工具完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧工具叫 search_web、新工具叫 lookup，若二者都实现查找证据功能，工作流可复用，但参数与返回格式还须重新匹配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03468">原论文</a> · <a href="../../../../agent-research/2608.03468-toollift/">实现解读</a> · <a href="#qa-830b9099c62167a8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagent" data-paper-title="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents Agent University of New South Wales 2026-07-31 把工具建模为 input-schema→output-schema 超边，先构造 Task DAG，再按状态缺口扩展 producer tool support graph。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 超图 Agent 规划与搜索：下一步该做什么 工具为什么用输入到输出的超边表示，而不只按名称做相似度检索？ 一个工具可能同时要求多种输入并产生多个输出，超边能表达这些联合前提。任务 DAG 先明确缺什么状态，再沿 producer 关系寻找能补齐输入的工具链；名称相似只说明文字接近，不能保证所选工具拿得到必需参数或能生成后续所需字段。 例如发票工具同时需要订单号与税号，前一步只找到订单号还不能执行；超图会继续寻找税号生产者，而不直接调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-hyperagent-a4e2dd7a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-032d0f4e9ed49d5e">工具为什么用输入到输出的超边表示，而不只按名称做相似度检索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahyperagent">HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of New South Wales</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个工具可能同时要求多种输入并产生多个输出，超边能表达这些联合前提。任务 DAG 先明确缺什么状态，再沿 producer 关系寻找能补齐输入的工具链；名称相似只说明文字接近，不能保证所选工具拿得到必需参数或能生成后续所需字段。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如发票工具同时需要订单号与税号，前一步只找到订单号还不能执行；超图会继续寻找税号生产者，而不直接调用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02650">原论文</a> · <a href="../../../../agent-research/2608.02650-hyperagent/">实现解读</a> · <a href="#qa-032d0f4e9ed49d5e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sira" data-paper-title="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval Agent Meta Superintelligence Labs / Rice University（工作完成于 Meta） 2026-05-07 冻结 LLM 先生成相关证据可能使用、但原查询缺失的词汇，再用倒排索引中的文档频率过滤不存在或过于常见的词；原查询与验证后的扩展只执行一次加权 BM25。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。三种子诊断：metrics/mechanism-seeds42-44.json  Agent 检索 语料感知查询扩展 BM25 Agent 规划与搜索：下一步该做什么 生成的扩展词为什么还要用倒排索引里的文档频率过滤？ LLM 可能提出语义合理却不在语料里的词，也可能加入到处都出现、没有区分力的词。文档频率约束先验证这些扩展确实可检索且不过泛，再与原查询做一次加权 BM25；它保留词法检索路径，不是让模型想象词存在就当成已找到证据。 例如查询稀有疾病时，扩展出语料没有的缩写不会带来召回；扩展成“研究”又太泛，过滤后才有有效词项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-sira-e870822f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c8aad7a618c0f02b">生成的扩展词为什么还要用倒排索引里的文档频率过滤？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asira">Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / Rice University（工作完成于 Meta）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>LLM 可能提出语义合理却不在语料里的词，也可能加入到处都出现、没有区分力的词。文档频率约束先验证这些扩展确实可检索且不过泛，再与原查询做一次加权 BM25；它保留词法检索路径，不是让模型想象词存在就当成已找到证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如查询稀有疾病时，扩展出语料没有的缩写不会带来召回；扩展成“研究”又太泛，过滤后才有有效词项。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.06647">原论文</a> · <a href="../../../../agent-research/2605.06647-sira/">实现解读</a> · <a href="#qa-c8aad7a618c0f02b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lats" data-paper-title="LATS" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LATS Agent University of Illinois Urbana-Champaign 2023-10-06 ReAct 等方法通常沿单条轨迹行动，失败后缺少系统搜索。LATS 把 LM 同时作为 agent、value function 和 optimizer，嵌入 Monte Carlo Tree Search；环境执行提供外部 reward，失败轨迹生成 reflection，帮助后续搜索避开错误。 本页实现 UCT 式树搜索、完整 trajectory rollout、环境 reward、反思与回溯。保留 MCTS statistics、环境反馈、reflection 与回溯；本地树以完整计划为叶节点，未调用 LM value model、HumanEval executor 或 WebShop，搜索规模远小于论文。每个 PlanBench episode 搜索四条完整计划轨迹；环境返回 exact plan reward，失败轨迹产生 reflection/backtrack，再按累计 value 选最终路径。  Agent 搜索 Agent 规划与搜索：下一步该做什么 UCT 中探索项为什么能让暂时低分的动作仍获得尝试？ 平均价值反映已见回报，探索项随父节点访问增多、子动作访问稀少而变大，给不确定分支试验机会。执行反馈再更新价值，失败反思帮助后续扩展；若仅反复选当前最高估值，就可能过早锁定错误分支，模型自评分也不能替代环境反馈。 例如动作甲试了十次均一般，乙只试一次失败，UCT 可能再探乙以减少不确定性，而不是从此把它永久排除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-lats-45a406fd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f04ceb7a00b1ae2c">UCT 中探索项为什么能让暂时低分的动作仍获得尝试？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alats">LATS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平均价值反映已见回报，探索项随父节点访问增多、子动作访问稀少而变大，给不确定分支试验机会。执行反馈再更新价值，失败反思帮助后续扩展；若仅反复选当前最高估值，就可能过早锁定错误分支，模型自评分也不能替代环境反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如动作甲试了十次均一般，乙只试一次失败，UCT 可能再探乙以减少不确定性，而不是从此把它永久排除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.04406">原论文</a> · <a href="../../../../agent-research/2310.04406-lats/">实现解读</a> · <a href="#qa-f04ceb7a00b1ae2c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rewoo" data-paper-title="ReWOO" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReWOO Agent Microsoft Research 2023-05-29 ReAct 在每次工具返回后重新调用 LLM，token 和推理成本随轨迹增长。ReWOO 的 Planner 用变量引用写出完整多步计划，Worker 只负责填入工具证据，Solver 最后读取计划与证据生成答案，因此 Planner 不被中间观察反复打断。 ReWOO 先一次性生成带依赖的完整计划，再由 Worker 执行工具，最后由 Solver 汇总；避免 ReAct 每一步都把不断增长的 observation 送回 Planner。实现 Planner/Worker/Solver 解耦、显式依赖与证据汇总；本地没有真实搜索 API 和多尺寸 LLM，因此只验证控制流与调用计数，不复刻 HotpotQA 的语言生成分数。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.5000，生成 120 份完整计划并执行 360 次 worker/tool action。  解耦规划 Agent 规划与搜索：下一步该做什么 Planner 不反复读取中间观察，为什么仍能表达工具之间的依赖？ 它先把依赖写成变量引用，Worker 执行时把已得到证据填入后续工具参数，Solver 最后统一使用成果。因此减少的是反复规划调用，不是删除数据流；若后续路线真的依赖尚未知的观察而初始计划没有表达，静态计划也会受适应性限制。 例如先查人物出生地记为 E1，再用 E1 查当地人口；第二步的具体城市可晚绑定，而无需 Planner 每次重新生成整段计划。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-rewoo-abc51544" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b9de714c020722cd">Planner 不反复读取中间观察，为什么仍能表达工具之间的依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arewoo">ReWOO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它先把依赖写成变量引用，Worker 执行时把已得到证据填入后续工具参数，Solver 最后统一使用成果。因此减少的是反复规划调用，不是删除数据流；若后续路线真的依赖尚未知的观察而初始计划没有表达，静态计划也会受适应性限制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先查人物出生地记为 E1，再用 E1 查当地人口；第二步的具体城市可晚绑定，而无需 Planner 每次重新生成整段计划。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18323">原论文</a> · <a href="../../../../agent-research/2305.18323-rewoo/">实现解读</a> · <a href="#qa-b9de714c020722cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tree-of-thoughts" data-paper-title="Tree of Thoughts" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Tree of Thoughts Agent Princeton University 2023-05-17 自回归生成和单条 CoT 很难撤销早期错误。ToT 将中间推理视为可独立评价的 thought，在树上生成多个候选，使用语言模型 value 函数选择 BFS/DFS frontier，并允许 lookahead 和 backtracking。 value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。本页实现 thought 单元的分支扩展、BFS beam 选择、value evaluation 与回溯，不是单条 Chain-of-Thought。实现 thought tree、BFS、value pruning 和回溯；value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。  推理搜索 Agent 规划与搜索：下一步该做什么 把推理切成 thought 再做树搜索，与一次生成多条完整答案有什么不同？ 中间 thought 是可单独评价和扩展的状态，可以在早期保留多种方向、剪去死路并回退。多条完整答案则常在终点才比较，重复支付错误前缀的成本；ToT 的收益仍受价值估计和搜索宽深预算限制，树结构本身不保证评价正确。 例如算术题第一步有三种分解，先检验哪种保留可行余量再扩展，能避免把明显不可能的分解一路写到完整答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-tree-of-thoughts-32a1f51e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8b8a8b99244ced83">把推理切成 thought 再做树搜索，与一次生成多条完整答案有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atree-of-thoughts">Tree of Thoughts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>中间 thought 是可单独评价和扩展的状态，可以在早期保留多种方向、剪去死路并回退。多条完整答案则常在终点才比较，重复支付错误前缀的成本；ToT 的收益仍受价值估计和搜索宽深预算限制，树结构本身不保证评价正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如算术题第一步有三种分解，先检验哪种保留可行余量再扩展，能避免把明显不可能的分解一路写到完整答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10601">原论文</a> · <a href="../../../../agent-research/2305.10601-tree-of-thoughts/">实现解读</a> · <a href="#qa-8b8a8b99244ced83">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:react" data-paper-title="ReAct" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReAct Agent Princeton University 2022-10-06 纯 CoT 容易在封闭知识上幻觉，纯 action agent 又缺少计划与状态跟踪。ReAct 让模型交替生成自然语言推理和环境 action，再把 observation 放回下一步上下文，使推理可以纠错、行动可以获取外部事实。 本页实现 Thought → Action → Observation 的交替循环，并记录实际 reasoning/action 次数；不是把直接返回答案包装成 ReAct。保留交替 trace 和工具动作计数，但 observation 来自确定性 mini-suite；未调用 Wikipedia、WebShop 或付费 LLM，因此本地 1.0 只说明执行循环正确，不能对标论文。ScaleMCP mini 固定 120 episodes、seed 42；每个 required tool 前执行一次 reasoning，随后记录 action/observation。  推理与行动 Agent 规划与搜索：下一步该做什么 为什么 observation 必须回到下一轮上下文，而不能让模型只继续自己的 reasoning？ 动作的意义在于获得真实外部反馈，下一轮据此修正信念与计划。若只沿原推理续写，模型可能把预期当成实际结果，失去行动与认知的闭环；ReAct 的关键是推理、可执行动作和观察交替，不是单纯在文本里写出几个工具名称。 例如模型猜文件存在后执行读取，工具实际返回不存在；下一步应改变搜索路径，而非沿“文件已读到”的想象继续分析。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-react-96535df9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e6518cb3d9714fda">为什么 observation 必须回到下一轮上下文，而不能让模型只继续自己的 reasoning？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Areact">ReAct</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动作的意义在于获得真实外部反馈，下一轮据此修正信念与计划。若只沿原推理续写，模型可能把预期当成实际结果，失去行动与认知的闭环；ReAct 的关键是推理、可执行动作和观察交替，不是单纯在文本里写出几个工具名称。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型猜文件存在后执行读取，工具实际返回不存在；下一步应改变搜索路径，而非沿“文件已读到”的想象继续分析。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2210.03629">原论文</a> · <a href="../../../../agent-research/2210.03629-react/">实现解读</a> · <a href="#qa-e6518cb3d9714fda">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

任务长、反馈晚时，怎样决定下一步行动，并撤销早先的错误选择？

## 记住这一点

把一次回答改成可观察的决策过程：当前知道什么、缺什么、下一步行动能带来什么证据。ReAct 交替推理与行动，让环境返回纠正计划；树搜索把中间状态分支化，通过评价、保留与回溯分配预算。两者都需要状态记录，但增加分支会增加模型和工具调用。学习时先画清状态、动作、观察三者，再判断是否需要搜索。

## 一个例子

假设要定位一次单元测试失败。当前只有报错摘要，先读取失败栈，发现错误来自输入维度，再检查调用方。若有“数据切分错”和“模型形状错”两条解释，可以分别设计一个小检查，保留与观察一致的分支。这个教学例子中，计划的价值在于决定下一条证据如何取得；把同一句推理改写三遍，仍没有增加环境证据。

## 什么时候要小心

模型给分不是独立正确性证明。搜索更多节点也不能弥补错误状态和有偏评价；比较时需要匹配总调用预算。阅读路线中的本地 thought/action 循环或确定性搜索只支持机制检查，不等同于原论文的任务成功率；测试答案、未来观察和隐藏计划不得放进 actor 的可见输入。

## 先读这几篇

先读 ReAct，建立推理—行动—观察的基本循环；再读 Tree of Thoughts，看分支、评价和回溯增加了什么；最后读 ReWOO，比较先规划后执行如何减少重复调用。

1. [ReAct](../../../agent-research/2210.03629-react/README.md) · [原论文](https://arxiv.org/abs/2210.03629)
2. [Tree of Thoughts](../../../agent-research/2305.10601-tree-of-thoughts/README.md) · [原论文](https://arxiv.org/abs/2305.10601)
3. [ReWOO](../../../agent-research/2305.18323-rewoo/README.md) · [原论文](https://arxiv.org/abs/2305.18323)

## 自测一下

同样预算下，连续写出五条计划与执行两次能区分假设的工具检查，是否属于同一种“搜索”？

??? note "展开参考答案"

    不属于。前者可能仅扩写文本；后者会改变可观察状态并排除假设。要称为分支搜索，还需明确分支状态、扩展规则、评价方式及保留/回溯。选择哪种方式，要看信息收益与工具成本，不能仅数生成的计划条数。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
