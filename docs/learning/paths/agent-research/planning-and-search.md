---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 规划与搜索：下一步该做什么

[Agent](index.md) / 子主题导学 · 约 3 分钟 · 16 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 16 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Repairing LLM-Generated Specifications with Deterministic Diagnosis Agent University of Oxford 2026-10-15 形式规格“能运行”不等于“忠实表达了题意”。DRAGO 将 SMT-LIB2、MiniZinc 和 PDDL 的契约、求解器探针及题意对齐检查转为可定位诊断，再要求模型定向修复。候选必须保留语法/词表/输出合同，严格降低阻塞诊断，并满足防退化条件；参考形式化和最终标签只用于最后评分。方法 §3、附录 A.2 原图建议：原论文 Figure 2 为诊断/接纳消融；Figure 3 为 Planetarium 输入渲染缺陷。它们分别解释算法贡献和评测风险。 原文用 4×A100 服务30B/31B模型，跨5个 benchmark 多seed、多臂重评估，完整实验成本过高，不复现（审查 DONE）。实现 grounded STRIPS/PDDL 方向的诊断算子子集；component_only / L1 CPU。实现 grounded STRIPS/PDDL 方向的诊断算子子集；不冒充完整三形式化语言框架。CPU fixture 随机化走廊规模，实际执行无前提路径、联合目标冲突、预算耗尽、证据支持的初态修复，以及“删掉目标就算修好”的负对照。proposal 回调只拿公开 Problem 和 Diagnosis，不拿金标准。  规划与搜索 形式规格诊断与保守修复 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-drago-838b0a34">Repairing LLM-Generated Specifications with Deterministic Diagnosis</h2>
<p class="ar-learning-card__meta">University of Oxford · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>形式规格“能运行”不等于“忠实表达了题意”。DRAGO 将 SMT-LIB2、MiniZinc 和 PDDL 的契约、求解器探针及题意对齐检查转为可定位诊断，再要求模型定向修复。候选必须保留语法/词表/输出合同，严格降低阻塞诊断，并满足防退化条件；参考形式化和最终标签只用于最后评分。方法 §3、附录 A.2 原图建议：原论文 Figure 2 为诊断/接纳消融；Figure 3 为 Planetarium 输入渲染缺陷。它们分别解释算法贡献和评测风险。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原文用 4×A100 服务30B/31B模型，跨5个 benchmark 多seed、多臂重评估，完整实验成本过高，不复现（审查 DONE）。实现 grounded STRIPS/PDDL 方向的诊断算子子集；component_only / L1 CPU。实现 grounded STRIPS/PDDL 方向的诊断算子子集；不冒充完整三形式化语言框架。CPU fixture 随机化走廊规模，实际执行无前提路径、联合目标冲突、预算耗尽、证据支持的初态修复，以及“删掉目标就算修好”的负对照。proposal 回调只拿公开 Problem 和 Diagnosis，不拿金标准。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22568">原论文</a> · <a href="../../../../agent-research/2610.22568-drago/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-10-09 在研究图中先生成未执行提案，再预测价值提升、信息增益和探索收益；稀疏 pairwise tournament 拟合软 Bradley–Terry 分数。执行选中实验后，从成功/失败抽象 intra/cross-task 技能并更新预测、探索、协调协议。事实来源：原文全文。 不同浮点 backend 也不能在未验证时声称 logits bit-exact，见 PyTorch 官方 SDPA 说明。当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始几何可行程序；原文对照完整自主研究框架；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  autonomous-research world-model evolving-skills Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-janus-c8240d07">Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models</h2>
<p class="ar-learning-card__meta">Institute of Computing Technology, Chinese Academy of Sciences · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>在研究图中先生成未执行提案，再预测价值提升、信息增益和探索收益；稀疏 pairwise tournament 拟合软 Bradley–Terry 分数。执行选中实验后，从成功/失败抽象 intra/cross-task 技能并更新预测、探索、协调协议。事实来源：原文全文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不同浮点 backend 也不能在未验证时声称 logits bit-exact，见 PyTorch 官方 SDPA 说明。当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始几何可行程序；原文对照完整自主研究框架；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13194">原论文</a> · <a href="../../../../reproductions/2610.13194-janus/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Code Owns the Simulation, Jev Owns the Evaluation Agent The Chinese University of Hong Kong 2026-10-01 让可执行代码负责模拟每个动作的后继状态，让 Jev 只负责比较动作带来的进展。除了当前动作和下一观察，还显式提供“执行后新出现的可用动作”，降低纯语义动作评分难以预判长期可达性的缺陷。 L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；本地实验使用显式词法诊断 provider，没有调用真实 Jev，也不是 ALFWorld 成功率复现。尚未运行真实 Jev checkpoint/托管 API、ALFWorld 或机器人环境；本次不新增 CUDA 路径，不宣称 GPU 验证或 Evolve 能力提升。System One 方法索引保留交叉入口。运行 PYTHONPATH=src python scripts/run_oct04_seven_papers.py。  模拟前瞻与动作选择 System One Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-jev-lookahead-d66c9de4">Code Owns the Simulation, Jev Owns the Evaluation</h2>
<p class="ar-learning-card__meta">The Chinese University of Hong Kong · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>让可执行代码负责模拟每个动作的后继状态，让 Jev 只负责比较动作带来的进展。除了当前动作和下一观察，还显式提供“执行后新出现的可用动作”，降低纯语义动作评分难以预判长期可达性的缺陷。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；本地实验使用显式词法诊断 provider，没有调用真实 Jev，也不是 ALFWorld 成功率复现。尚未运行真实 Jev checkpoint/托管 API、ALFWorld 或机器人环境；本次不新增 CUDA 路径，不宣称 GPU 验证或 Evolve 能力提升。System One 方法索引保留交叉入口。运行 PYTHONPATH=src python scripts/run_oct04_seven_papers.py。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01834">原论文</a> · <a href="../../../../agent-research/2610.01834-jev-lookahead/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces Agent 原文首页未列第一作者机构 2026-09-30 先从自然语言任务构造有限 compositional action space，以 Jev 分布并行保留多个分支；反馈更新后验并保留备选以支持恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Jev Agent 推理 分支搜索 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-jev-spawn-dc827975">JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-09-30</p>
<p><strong>方法要点：</strong>先从自然语言任务构造有限 compositional action space，以 Jev 分布并行保留多个分支；反馈更新后验并保留备选以支持恢复。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00437">原论文</a> · <a href="../../../../agent-research/2610.00437-jev-spawn/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning Agent Meta Superintelligence Labs 2026-09-29 把对象级工作交给 worker，把控制本身拆成 Assess、Propose、Evaluate 和 Dispatch；控制器只携带紧凑状态，通过持久 artifact memory 复用既有工作，并在统一调用预算内决定继续、分叉或停止。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agent 推理 元推理控制 预算调度 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-meta-reasoning-f28ad63c">Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning</h2>
<p class="ar-learning-card__meta">Meta Superintelligence Labs · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>把对象级工作交给 worker，把控制本身拆成 Assess、Propose、Evaluate 和 Dispatch；控制器只携带紧凑状态，通过持久 artifact memory 复用既有工作，并在统一调用预算内决定继续、分叉或停止。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38147">原论文</a> · <a href="../../../../agent-research/2609.38147-meta-reasoning/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners Agent 原文首页未列机构 2026-09-28 执行前用符号前置条件门阻止不安全动作并给出类型化原因；失败时只重写相关子目标的后缀，保留已完成前缀。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  规划 安全门 局部恢复 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-sage-planner-6e4e53de">SAGE: Symbolic Action-Gating and Editing for LLM Task Planners</h2>
<p class="ar-learning-card__meta">原文首页未列机构 · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>执行前用符号前置条件门阻止不安全动作并给出类型化原因；失败时只重写相关子目标的后缀，保留已完成前缀。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34268">原论文</a> · <a href="../../../../agent-research/2609.34268-sage/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs Agent Duke University 2026-09-09 把搜索轨迹转为 query—evidence—answer 有向图，审计证据是否真正覆盖问题约束和最终回答。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  搜索 Agent 过程审计 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-searchatlas-1aefb816">SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs</h2>
<p class="ar-learning-card__meta">Duke University · 论文公开：2026-09-09</p>
<p><strong>方法要点：</strong>把搜索轨迹转为 query—evidence—answer 有向图，审计证据是否真正覆盖问题约束和最终回答。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10901">原论文</a> · <a href="../../../../agent-research/2609.10901-searchatlas/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-08-27 一次性全局计划会在文件、依赖和接口持续变化时失效。DeepRepro 在每个阶段读取当前 repository state 和执行反馈，重写细粒度 subplan，再由 repository-aware orchestration 推进实现。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现 repository snapshot、state-aware subplan 与 runtime-feedback repair。未运行官方 PaperBench Code-Dev，也未把 deterministic plan/answer 满分包装成论文结果；本地验证的是状态驱动重规划路径。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300，并记录 state snapshots、subplan revisions 与 repairs。  论文到代码状态子规划 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-deeprepro-1ec5a199">DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories</h2>
<p class="ar-learning-card__meta">Institute of Computing Technology, Chinese Academy of Sciences · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>一次性全局计划会在文件、依赖和接口持续变化时失效。DeepRepro 在每个阶段读取当前 repository state 和执行反馈，重写细粒度 subplan，再由 repository-aware orchestration 推进实现。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现 repository snapshot、state-aware subplan 与 runtime-feedback repair。未运行官方 PaperBench Code-Dev，也未把 deterministic plan/answer 满分包装成论文结果；本地验证的是状态驱动重规划路径。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300，并记录 state snapshots、subplan revisions 与 repairs。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26557">原论文</a> · <a href="../../../../agent-research/2608.26557-deeprepro/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation Agent Authors did not disclose affiliation 2026-08-12 把 reflect/backtrack 视为可逆轨迹树的 memory-control actions，以 privileged teacher 快通道和 outcome GRPO 慢通道协调训练。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  反思 Agentic RL Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-loongreflect-7debd709">LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation</h2>
<p class="ar-learning-card__meta">Authors did not disclose affiliation · 论文公开：2026-08-12</p>
<p><strong>方法要点：</strong>把 reflect/backtrack 视为可逆轨迹树的 memory-control actions，以 privileged teacher 快通道和 outcome GRPO 慢通道协调训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11967">原论文</a> · <a href="../../../../agent-research/2608.11967-loongreflect/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning Agent Authors did not disclose affiliation 2026-08-04 把工具级历史轨迹提升为可跨工具集迁移的 function workflow graph，再解耦 workflow planning 与 tool selection。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 图结构 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-toollift-dbb897af">ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning</h2>
<p class="ar-learning-card__meta">Authors did not disclose affiliation · 论文公开：2026-08-04</p>
<p><strong>方法要点：</strong>把工具级历史轨迹提升为可跨工具集迁移的 function workflow graph，再解耦 workflow planning 与 tool selection。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03468">原论文</a> · <a href="../../../../agent-research/2608.03468-toollift/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents Agent University of New South Wales 2026-07-31 把工具建模为 input-schema→output-schema 超边，先构造 Task DAG，再按状态缺口扩展 producer tool support graph。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 超图 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-hyperagent-a4e2dd7a">HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents</h2>
<p class="ar-learning-card__meta">University of New South Wales · 论文公开：2026-07-31</p>
<p><strong>方法要点：</strong>把工具建模为 input-schema→output-schema 超边，先构造 Task DAG，再按状态缺口扩展 producer tool support graph。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02650">原论文</a> · <a href="../../../../agent-research/2608.02650-hyperagent/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval Agent Meta Superintelligence Labs / Rice University（工作完成于 Meta） 2026-05-07 冻结 LLM 先生成相关证据可能使用、但原查询缺失的词汇，再用倒排索引中的文档频率过滤不存在或过于常见的词；原查询与验证后的扩展只执行一次加权 BM25。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。三种子诊断：metrics/mechanism-seeds42-44.json  Agent 检索 语料感知查询扩展 BM25 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-sira-e870822f">Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval</h2>
<p class="ar-learning-card__meta">Meta Superintelligence Labs / Rice University（工作完成于 Meta） · 论文公开：2026-05-07</p>
<p><strong>方法要点：</strong>冻结 LLM 先生成相关证据可能使用、但原查询缺失的词汇，再用倒排索引中的文档频率过滤不存在或过于常见的词；原查询与验证后的扩展只执行一次加权 BM25。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。三种子诊断：metrics/mechanism-seeds42-44.json</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.06647">原论文</a> · <a href="../../../../agent-research/2605.06647-sira/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LATS Agent University of Illinois Urbana-Champaign 2023-10-06 ReAct 等方法通常沿单条轨迹行动，失败后缺少系统搜索。LATS 把 LM 同时作为 agent、value function 和 optimizer，嵌入 Monte Carlo Tree Search；环境执行提供外部 reward，失败轨迹生成 reflection，帮助后续搜索避开错误。 本页实现 UCT 式树搜索、完整 trajectory rollout、环境 reward、反思与回溯。保留 MCTS statistics、环境反馈、reflection 与回溯；本地树以完整计划为叶节点，未调用 LM value model、HumanEval executor 或 WebShop，搜索规模远小于论文。每个 PlanBench episode 搜索四条完整计划轨迹；环境返回 exact plan reward，失败轨迹产生 reflection/backtrack，再按累计 value 选最终路径。  Agent 搜索 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-lats-45a406fd">LATS</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2023-10-06</p>
<p><strong>方法要点：</strong>ReAct 等方法通常沿单条轨迹行动，失败后缺少系统搜索。LATS 把 LM 同时作为 agent、value function 和 optimizer，嵌入 Monte Carlo Tree Search；环境执行提供外部 reward，失败轨迹生成 reflection，帮助后续搜索避开错误。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现 UCT 式树搜索、完整 trajectory rollout、环境 reward、反思与回溯。保留 MCTS statistics、环境反馈、reflection 与回溯；本地树以完整计划为叶节点，未调用 LM value model、HumanEval executor 或 WebShop，搜索规模远小于论文。每个 PlanBench episode 搜索四条完整计划轨迹；环境返回 exact plan reward，失败轨迹产生 reflection/backtrack，再按累计 value 选最终路径。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.04406">原论文</a> · <a href="../../../../agent-research/2310.04406-lats/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReWOO Agent Microsoft Research 2023-05-29 ReAct 在每次工具返回后重新调用 LLM，token 和推理成本随轨迹增长。ReWOO 的 Planner 用变量引用写出完整多步计划，Worker 只负责填入工具证据，Solver 最后读取计划与证据生成答案，因此 Planner 不被中间观察反复打断。 ReWOO 先一次性生成带依赖的完整计划，再由 Worker 执行工具，最后由 Solver 汇总；避免 ReAct 每一步都把不断增长的 observation 送回 Planner。实现 Planner/Worker/Solver 解耦、显式依赖与证据汇总；本地没有真实搜索 API 和多尺寸 LLM，因此只验证控制流与调用计数，不复刻 HotpotQA 的语言生成分数。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.5000，生成 120 份完整计划并执行 360 次 worker/tool action。  解耦规划 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-rewoo-abc51544">ReWOO</h2>
<p class="ar-learning-card__meta">Microsoft Research · 论文公开：2023-05-29</p>
<p><strong>方法要点：</strong>ReAct 在每次工具返回后重新调用 LLM，token 和推理成本随轨迹增长。ReWOO 的 Planner 用变量引用写出完整多步计划，Worker 只负责填入工具证据，Solver 最后读取计划与证据生成答案，因此 Planner 不被中间观察反复打断。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>ReWOO 先一次性生成带依赖的完整计划，再由 Worker 执行工具，最后由 Solver 汇总；避免 ReAct 每一步都把不断增长的 observation 送回 Planner。实现 Planner/Worker/Solver 解耦、显式依赖与证据汇总；本地没有真实搜索 API 和多尺寸 LLM，因此只验证控制流与调用计数，不复刻 HotpotQA 的语言生成分数。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.5000，生成 120 份完整计划并执行 360 次 worker/tool action。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18323">原论文</a> · <a href="../../../../agent-research/2305.18323-rewoo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Tree of Thoughts Agent Princeton University 2023-05-17 自回归生成和单条 CoT 很难撤销早期错误。ToT 将中间推理视为可独立评价的 thought，在树上生成多个候选，使用语言模型 value 函数选择 BFS/DFS frontier，并允许 lookahead 和 backtracking。 value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。本页实现 thought 单元的分支扩展、BFS beam 选择、value evaluation 与回溯，不是单条 Chain-of-Thought。实现 thought tree、BFS、value pruning 和回溯；value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。  推理搜索 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-tree-of-thoughts-32a1f51e">Tree of Thoughts</h2>
<p class="ar-learning-card__meta">Princeton University · 论文公开：2023-05-17</p>
<p><strong>方法要点：</strong>自回归生成和单条 CoT 很难撤销早期错误。ToT 将中间推理视为可独立评价的 thought，在树上生成多个候选，使用语言模型 value 函数选择 BFS/DFS frontier，并允许 lookahead 和 backtracking。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。本页实现 thought 单元的分支扩展、BFS beam 选择、value evaluation 与回溯，不是单条 Chain-of-Thought。实现 thought tree、BFS、value pruning 和回溯；value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10601">原论文</a> · <a href="../../../../agent-research/2305.10601-tree-of-thoughts/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReAct Agent Princeton University 2022-10-06 纯 CoT 容易在封闭知识上幻觉，纯 action agent 又缺少计划与状态跟踪。ReAct 让模型交替生成自然语言推理和环境 action，再把 observation 放回下一步上下文，使推理可以纠错、行动可以获取外部事实。 本页实现 Thought → Action → Observation 的交替循环，并记录实际 reasoning/action 次数；不是把直接返回答案包装成 ReAct。保留交替 trace 和工具动作计数，但 observation 来自确定性 mini-suite；未调用 Wikipedia、WebShop 或付费 LLM，因此本地 1.0 只说明执行循环正确，不能对标论文。ScaleMCP mini 固定 120 episodes、seed 42；每个 required tool 前执行一次 reasoning，随后记录 action/observation。  推理与行动 Agent 规划与搜索：下一步该做什么">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<h2 id="paper-agent-research-react-96535df9">ReAct</h2>
<p class="ar-learning-card__meta">Princeton University · 论文公开：2022-10-06</p>
<p><strong>方法要点：</strong>纯 CoT 容易在封闭知识上幻觉，纯 action agent 又缺少计划与状态跟踪。ReAct 让模型交替生成自然语言推理和环境 action，再把 observation 放回下一步上下文，使推理可以纠错、行动可以获取外部事实。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现 Thought → Action → Observation 的交替循环，并记录实际 reasoning/action 次数；不是把直接返回答案包装成 ReAct。保留交替 trace 和工具动作计数，但 observation 来自确定性 mini-suite；未调用 Wikipedia、WebShop 或付费 LLM，因此本地 1.0 只说明执行循环正确，不能对标论文。ScaleMCP mini 固定 120 episodes、seed 42；每个 required tool 前执行一次 reasoning，随后记录 action/observation。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2210.03629">原论文</a> · <a href="../../../../agent-research/2210.03629-react/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
