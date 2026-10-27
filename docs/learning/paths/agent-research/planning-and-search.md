---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 规划与搜索：下一步该做什么

[Agent](index.md) / 64 个问题 · 16 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/agent-research/planning-and-search.md)

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<div class="ar-learning-levels" role="group" aria-label="学习层次">
<span>学习层次</span>
<button type="button" data-learning-level="" aria-pressed="true">全部</button>
<button type="button" data-learning-level="basics" aria-pressed="false">基础理解</button>
<button type="button" data-learning-level="mechanism" aria-pressed="false">核心机制</button>
<button type="button" data-learning-level="comparison" aria-pressed="false">方法对比</button>
<button type="button" data-learning-level="implementation" aria-pressed="false">实现细节</button>
</div>
<p class="ar-learning-status" data-learning-status role="status">64 个问题 · 16 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:drago" data-paper-title="Repairing LLM-Generated Specifications with Deterministic Diagnosis" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Repairing LLM-Generated Specifications with Deterministic Diagnosis Agent University of Oxford 2026-10-15 形式规格“能运行”不等于“忠实表达了题意”。DRAGO 将 SMT-LIB2、MiniZinc 和 PDDL 的契约、求解器探针及题意对齐检查转为可定位诊断，再要求模型定向修复。候选必须保留语法/词表/输出合同，严格降低阻塞诊断，并满足防退化条件；参考形式化和最终标签只用于最后评分。方法 §3、附录 A.2 原图建议：原论文 Figure 2 为诊断/接纳消融；Figure 3 为 Planetarium 输入渲染缺陷。它们分别解释算法贡献和评测风险。 原文用 4×A100 服务30B/31B模型，跨5个 benchmark 多seed、多臂重评估，完整实验成本过高，不复现（审查 DONE）。实现 grounded STRIPS/PDDL 方向的诊断算子子集；component_only / L1 CPU。实现 grounded STRIPS/PDDL 方向的诊断算子子集；不冒充完整三形式化语言框架。CPU fixture 随机化走廊规模，实际执行无前提路径、联合目标冲突、预算耗尽、证据支持的初态修复，以及“删掉目标就算修好”的负对照。proposal 回调只拿公开 Problem 和 Diagnosis，不拿金标准。  规划与搜索 形式规格诊断与保守修复 Agent 规划与搜索：下一步该做什么 让 LLM 把自然语言题目写成形式规格时，DRAGO 要防哪类“看似成功”？ 模型可能生成能解析、能求解，却遗漏要求的规格，后续求解器只会忠实解决这个错误版本。DRAGO 关注自然语言到形式系统的转换可靠性，用可定位诊断约束修复，而不是把拿到一个解当作原题已解决；规格和求解是两个需要分开检查的环节。 例如题目要求两人都被安排，规格漏写一人后排班更容易有解，但这个“成功”恰好暴露了形式化阶段的遗漏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-drago-838b0a34" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-58adcfc64a04a3e1">让 LLM 把自然语言题目写成形式规格时，DRAGO 要防哪类“看似成功”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adrago">Repairing LLM-Generated Specifications with Deterministic Diagnosis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型可能生成能解析、能求解，却遗漏要求的规格，后续求解器只会忠实解决这个错误版本。DRAGO 关注自然语言到形式系统的转换可靠性，用可定位诊断约束修复，而不是把拿到一个解当作原题已解决；规格和求解是两个需要分开检查的环节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如题目要求两人都被安排，规格漏写一人后排班更容易有解，但这个“成功”恰好暴露了形式化阶段的遗漏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22568">原论文</a> · <a href="../../../../agent-research/2610.22568-drago/">实现解读</a> · <a href="#qa-58adcfc64a04a3e1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:drago" data-paper-title="Repairing LLM-Generated Specifications with Deterministic Diagnosis" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Repairing LLM-Generated Specifications with Deterministic Diagnosis Agent University of Oxford 2026-10-15 形式规格“能运行”不等于“忠实表达了题意”。DRAGO 将 SMT-LIB2、MiniZinc 和 PDDL 的契约、求解器探针及题意对齐检查转为可定位诊断，再要求模型定向修复。候选必须保留语法/词表/输出合同，严格降低阻塞诊断，并满足防退化条件；参考形式化和最终标签只用于最后评分。方法 §3、附录 A.2 原图建议：原论文 Figure 2 为诊断/接纳消融；Figure 3 为 Planetarium 输入渲染缺陷。它们分别解释算法贡献和评测风险。 原文用 4×A100 服务30B/31B模型，跨5个 benchmark 多seed、多臂重评估，完整实验成本过高，不复现（审查 DONE）。实现 grounded STRIPS/PDDL 方向的诊断算子子集；component_only / L1 CPU。实现 grounded STRIPS/PDDL 方向的诊断算子子集；不冒充完整三形式化语言框架。CPU fixture 随机化走廊规模，实际执行无前提路径、联合目标冲突、预算耗尽、证据支持的初态修复，以及“删掉目标就算修好”的负对照。proposal 回调只拿公开 Problem 和 Diagnosis，不拿金标准。  规划与搜索 形式规格诊断与保守修复 Agent 规划与搜索：下一步该做什么 为什么求解器返回可解，还不能证明形式规格忠实表达了题意？ 求解器只判断写下来的约束，不知道自然语言要求是否被遗漏或偷换。DRAGO 把词表合同、可达性探针与题意对齐分开诊断，修复必须严格减少阻塞且不删除目标来投机；探针耗尽预算只能报未知，不能捏造成已证明无解。 例如题目要求同时到达两处，错误规格只写一处也可能可解；删掉困难目标会降低求解难度，却不是正确修复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:drago" data-paper-title="Repairing LLM-Generated Specifications with Deterministic Diagnosis" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Repairing LLM-Generated Specifications with Deterministic Diagnosis Agent University of Oxford 2026-10-15 形式规格“能运行”不等于“忠实表达了题意”。DRAGO 将 SMT-LIB2、MiniZinc 和 PDDL 的契约、求解器探针及题意对齐检查转为可定位诊断，再要求模型定向修复。候选必须保留语法/词表/输出合同，严格降低阻塞诊断，并满足防退化条件；参考形式化和最终标签只用于最后评分。方法 §3、附录 A.2 原图建议：原论文 Figure 2 为诊断/接纳消融；Figure 3 为 Planetarium 输入渲染缺陷。它们分别解释算法贡献和评测风险。 原文用 4×A100 服务30B/31B模型，跨5个 benchmark 多seed、多臂重评估，完整实验成本过高，不复现（审查 DONE）。实现 grounded STRIPS/PDDL 方向的诊断算子子集；component_only / L1 CPU。实现 grounded STRIPS/PDDL 方向的诊断算子子集；不冒充完整三形式化语言框架。CPU fixture 随机化走廊规模，实际执行无前提路径、联合目标冲突、预算耗尽、证据支持的初态修复，以及“删掉目标就算修好”的负对照。proposal 回调只拿公开 Problem 和 Diagnosis，不拿金标准。  规划与搜索 形式规格诊断与保守修复 Agent 规划与搜索：下一步该做什么 删除松弛与完整 BFS 都检查可达性，为什么不能互相替代？ 删除松弛忽略 delete effect，固定点中仍不出现的目标可判不可达；出现则未必能联合实现。完整 BFS 保留删除效果，穷尽状态才证明无解，预算耗尽只能未知。前者较便宜、结论单向，后者更严格却受搜索规模限制。 例如拿走钥匙会失去另一个条件，两个目标各自在松弛中可达，却可能无法同时满足；完整状态搜索才看见冲突。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-43baaeea36e72a90">删除松弛与完整 BFS 都检查可达性，为什么不能互相替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adrago">Repairing LLM-Generated Specifications with Deterministic Diagnosis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>删除松弛忽略 delete effect，固定点中仍不出现的目标可判不可达；出现则未必能联合实现。完整 BFS 保留删除效果，穷尽状态才证明无解，预算耗尽只能未知。前者较便宜、结论单向，后者更严格却受搜索规模限制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如拿走钥匙会失去另一个条件，两个目标各自在松弛中可达，却可能无法同时满足；完整状态搜索才看见冲突。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22568">原论文</a> · <a href="../../../../agent-research/2610.22568-drago/">实现解读</a> · <a href="#qa-43baaeea36e72a90">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:drago" data-paper-title="Repairing LLM-Generated Specifications with Deterministic Diagnosis" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Repairing LLM-Generated Specifications with Deterministic Diagnosis Agent University of Oxford 2026-10-15 形式规格“能运行”不等于“忠实表达了题意”。DRAGO 将 SMT-LIB2、MiniZinc 和 PDDL 的契约、求解器探针及题意对齐检查转为可定位诊断，再要求模型定向修复。候选必须保留语法/词表/输出合同，严格降低阻塞诊断，并满足防退化条件；参考形式化和最终标签只用于最后评分。方法 §3、附录 A.2 原图建议：原论文 Figure 2 为诊断/接纳消融；Figure 3 为 Planetarium 输入渲染缺陷。它们分别解释算法贡献和评测风险。 原文用 4×A100 服务30B/31B模型，跨5个 benchmark 多seed、多臂重评估，完整实验成本过高，不复现（审查 DONE）。实现 grounded STRIPS/PDDL 方向的诊断算子子集；component_only / L1 CPU。实现 grounded STRIPS/PDDL 方向的诊断算子子集；不冒充完整三形式化语言框架。CPU fixture 随机化走廊规模，实际执行无前提路径、联合目标冲突、预算耗尽、证据支持的初态修复，以及“删掉目标就算修好”的负对照。proposal 回调只拿公开 Problem 和 Diagnosis，不拿金标准。  规划与搜索 形式规格诊断与保守修复 Agent 规划与搜索：下一步该做什么 修复接纳时只要求阻塞权重不增加够吗？ 不够。必须严格下降，不新增阻塞轴、不减少目标数，对象数量只朝公开题意靠近，且原先可解规格不得退化为无解或未知；拒绝时保留旧对象并停止。只用非增加条件可能接纳无效改写，删除困难目标则会投机降低诊断。 例如旧规格有两项阻塞，新规格仍有两项，只改了措辞不应接纳；删掉一个目标虽降阻塞也应被防退化检查拒绝。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dd525846f866a39f">修复接纳时只要求阻塞权重不增加够吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adrago">Repairing LLM-Generated Specifications with Deterministic Diagnosis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不够。必须严格下降，不新增阻塞轴、不减少目标数，对象数量只朝公开题意靠近，且原先可解规格不得退化为无解或未知；拒绝时保留旧对象并停止。只用非增加条件可能接纳无效改写，删除困难目标则会投机降低诊断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧规格有两项阻塞，新规格仍有两项，只改了措辞不应接纳；删掉一个目标虽降阻塞也应被防退化检查拒绝。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22568">原论文</a> · <a href="../../../../agent-research/2610.22568-drago/">实现解读</a> · <a href="#qa-dd525846f866a39f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:janus" data-paper-title="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-10-09 在研究图中先生成未执行提案，再预测价值提升、信息增益和探索收益；稀疏 pairwise tournament 拟合软 Bradley–Terry 分数。执行选中实验后，从成功/失败抽象 intra/cross-task 技能并更新预测、探索、协调协议。事实来源：原文全文。 不同浮点 backend 也不能在未验证时声称 logits bit-exact，见 PyTorch 官方 SDPA 说明。当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始几何可行程序；原文对照完整自主研究框架；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  autonomous-research world-model evolving-skills Agent 规划与搜索：下一步该做什么 Janus 为什么把尚未执行的提案也放入研究图？ 未执行提案代表可以竞争预算的研究方向，预测价值提升、信息增益和探索收益后再决定执行哪个。图同时保存实际实验反馈与抽象技能，使下一轮提案依赖已有证据；提案预测只是选择依据，不能当作完成实验或已获得的分数。 例如一个新模型改动和一个失败原因诊断都可先作为候选，系统按剩余预算决定先花算力测哪一个。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-janus-c8240d07" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-be862a584cf61633">Janus 为什么把尚未执行的提案也放入研究图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajanus">Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未执行提案代表可以竞争预算的研究方向，预测价值提升、信息增益和探索收益后再决定执行哪个。图同时保存实际实验反馈与抽象技能，使下一轮提案依赖已有证据；提案预测只是选择依据，不能当作完成实验或已获得的分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个新模型改动和一个失败原因诊断都可先作为候选，系统按剩余预算决定先花算力测哪一个。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13194">原论文</a> · <a href="../../../../reproductions/2610.13194-janus/">实现解读</a> · <a href="#qa-be862a584cf61633">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:janus" data-paper-title="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-10-09 在研究图中先生成未执行提案，再预测价值提升、信息增益和探索收益；稀疏 pairwise tournament 拟合软 Bradley–Terry 分数。执行选中实验后，从成功/失败抽象 intra/cross-task 技能并更新预测、探索、协调协议。事实来源：原文全文。 不同浮点 backend 也不能在未验证时声称 logits bit-exact，见 PyTorch 官方 SDPA 说明。当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始几何可行程序；原文对照完整自主研究框架；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  autonomous-research world-model evolving-skills Agent 规划与搜索：下一步该做什么 为什么实验提案先做成对比较，再拟合价值分数，而不是直接选描述最精彩的方案？ 成对比较让价值提升、信息增益与探索收益形成可校准的相对次序，稀疏锦标赛再用 Bradley–Terry 分数连接这些局部判断。预测用于分配实验预算，执行后的成功与失败又更新模型和技能；预测高分不等于实验已成功，也不能替代真实执行。 例如方案甲预期涨分高、乙更能排除关键假设，可按剩余预算调整探索权重，而不是把两句漂亮承诺当作结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:janus" data-paper-title="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-10-09 在研究图中先生成未执行提案，再预测价值提升、信息增益和探索收益；稀疏 pairwise tournament 拟合软 Bradley–Terry 分数。执行选中实验后，从成功/失败抽象 intra/cross-task 技能并更新预测、探索、协调协议。事实来源：原文全文。 不同浮点 backend 也不能在未验证时声称 logits bit-exact，见 PyTorch 官方 SDPA 说明。当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始几何可行程序；原文对照完整自主研究框架；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  autonomous-research world-model evolving-skills Agent 规划与搜索：下一步该做什么 只按预测涨分选实验，与同时计入信息增益和探索收益有何区别？ 单看涨分偏向当前最有希望的方向，可能反复利用已有区域；信息增益重视排除不确定假设，探索收益则给未知方向机会。Janus 随进度和剩余预算调整权重，体现探索利用取舍，但预测误差仍需由真实执行纠正。 例如甲预期小幅涨分但结论已很确定，乙不一定涨分却能区分两种机制，早期预算可给乙更多机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9e6ceb7d58c0979f">只按预测涨分选实验，与同时计入信息增益和探索收益有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajanus">Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单看涨分偏向当前最有希望的方向，可能反复利用已有区域；信息增益重视排除不确定假设，探索收益则给未知方向机会。Janus 随进度和剩余预算调整权重，体现探索利用取舍，但预测误差仍需由真实执行纠正。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如甲预期小幅涨分但结论已很确定，乙不一定涨分却能区分两种机制，早期预算可给乙更多机会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13194">原论文</a> · <a href="../../../../reproductions/2610.13194-janus/">实现解读</a> · <a href="#qa-9e6ceb7d58c0979f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:janus" data-paper-title="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-10-09 在研究图中先生成未执行提案，再预测价值提升、信息增益和探索收益；稀疏 pairwise tournament 拟合软 Bradley–Terry 分数。执行选中实验后，从成功/失败抽象 intra/cross-task 技能并更新预测、探索、协调协议。事实来源：原文全文。 不同浮点 backend 也不能在未验证时声称 logits bit-exact，见 PyTorch 官方 SDPA 说明。当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为初始几何可行程序；原文对照完整自主研究框架；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  autonomous-research world-model evolving-skills Agent 规划与搜索：下一步该做什么 稀疏锦标赛的软比较如何形成提案价值分数？ 对比较边的软偏好用 BCE 拟合 sigmoid(g_m-g_n)，得到相对 Bradley–Terry 分数，再按三类收益加权。它连接局部偏好，不提供绝对成功概率；实验后再更新图与技能，不能用预测器自产分数替代 sandbox 的真实结果。 例如甲略优于乙、乙优于丙，可拟合相对次序；甲得分更高仍不意味着它的实验已经超过当前最好模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-aca159e2d90903f9">稀疏锦标赛的软比较如何形成提案价值分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajanus">Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对比较边的软偏好用 BCE 拟合 sigmoid(g_m-g_n)，得到相对 Bradley–Terry 分数，再按三类收益加权。它连接局部偏好，不提供绝对成功概率；实验后再更新图与技能，不能用预测器自产分数替代 sandbox 的真实结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如甲略优于乙、乙优于丙，可拟合相对次序；甲得分更高仍不意味着它的实验已经超过当前最好模型。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、结果、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13194">原论文</a> · <a href="../../../../reproductions/2610.13194-janus/">实现解读</a> · <a href="#qa-aca159e2d90903f9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-lookahead" data-paper-title="Code Owns the Simulation, Jev Owns the Evaluation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Code Owns the Simulation, Jev Owns the Evaluation Agent The Chinese University of Hong Kong 2026-10-01 让可执行代码负责模拟每个动作的后继状态，让 Jev 只负责比较动作带来的进展。除了当前动作和下一观察，还显式提供“执行后新出现的可用动作”，降低纯语义动作评分难以预判长期可达性的缺陷。 L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；本地实验使用显式词法诊断 provider，没有调用真实 Jev，也不是 ALFWorld 成功率复现。尚未运行真实 Jev checkpoint/托管 API、ALFWorld 或机器人环境；本次不新增 CUDA 路径，不宣称 GPU 验证或 Evolve 能力提升。System One 方法索引保留交叉入口。运行 PYTHONPATH=src python scripts/run_oct04_seven_papers.py。  模拟前瞻与动作选择 System One Agent 规划与搜索：下一步该做什么 代码模拟和模型评价在 lookahead 中分别承担什么责任？ 代码在当前状态的独立副本执行合法动作，产生实际后继观察；模型比较公开后果并选择动作。分工减少仅凭文字想象环境变化的错误，但依赖模拟器正确隔离与忠实转移，选择函数本身不应擅自改变真实环境。 例如打开抽屉先在副本中检查出现了什么，再决定是否真实打开；评分器不负责凭空编造抽屉内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-jev-lookahead-d66c9de4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8e02b08a2591a3de">代码模拟和模型评价在 lookahead 中分别承担什么责任？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-lookahead">Code Owns the Simulation, Jev Owns the Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>代码在当前状态的独立副本执行合法动作，产生实际后继观察；模型比较公开后果并选择动作。分工减少仅凭文字想象环境变化的错误，但依赖模拟器正确隔离与忠实转移，选择函数本身不应擅自改变真实环境。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如打开抽屉先在副本中检查出现了什么，再决定是否真实打开；评分器不负责凭空编造抽屉内容。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01834">原论文</a> · <a href="../../../../agent-research/2610.01834-jev-lookahead/">实现解读</a> · <a href="#qa-8e02b08a2591a3de">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-lookahead" data-paper-title="Code Owns the Simulation, Jev Owns the Evaluation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Code Owns the Simulation, Jev Owns the Evaluation Agent The Chinese University of Hong Kong 2026-10-01 让可执行代码负责模拟每个动作的后继状态，让 Jev 只负责比较动作带来的进展。除了当前动作和下一观察，还显式提供“执行后新出现的可用动作”，降低纯语义动作评分难以预判长期可达性的缺陷。 L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；本地实验使用显式词法诊断 provider，没有调用真实 Jev，也不是 ALFWorld 成功率复现。尚未运行真实 Jev checkpoint/托管 API、ALFWorld 或机器人环境；本次不新增 CUDA 路径，不宣称 GPU 验证或 Evolve 能力提升。System One 方法索引保留交叉入口。运行 PYTHONPATH=src python scripts/run_oct04_seven_papers.py。  模拟前瞻与动作选择 System One Agent 规划与搜索：下一步该做什么 提供“后继状态新出现的可用动作”，比只给下一观察多了什么？ 下一观察描述眼前变化，新动作集合则揭示该步打开了哪些后续通路，有助于比较短期无收益但长期有价值的动作。代码在克隆状态中负责真实模拟，决策模型只评公开后果；模拟器 reward 或正确计划不能作为偷偷提供给评分器的答案。 例如拿到钥匙暂时没有完成任务，却新增“打开侧门”的合法动作；看见这一机会才能评价取钥匙的长期意义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-lookahead" data-paper-title="Code Owns the Simulation, Jev Owns the Evaluation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Code Owns the Simulation, Jev Owns the Evaluation Agent The Chinese University of Hong Kong 2026-10-01 让可执行代码负责模拟每个动作的后继状态，让 Jev 只负责比较动作带来的进展。除了当前动作和下一观察，还显式提供“执行后新出现的可用动作”，降低纯语义动作评分难以预判长期可达性的缺陷。 L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；本地实验使用显式词法诊断 provider，没有调用真实 Jev，也不是 ALFWorld 成功率复现。尚未运行真实 Jev checkpoint/托管 API、ALFWorld 或机器人环境；本次不新增 CUDA 路径，不宣称 GPU 验证或 Evolve 能力提升。System One 方法索引保留交叉入口。运行 PYTHONPATH=src python scripts/run_oct04_seven_papers.py。  模拟前瞻与动作选择 System One Agent 规划与搜索：下一步该做什么 与纯语义动作打分相比，一步模拟增加什么信息而仍不保证最优？ 语义打分主要依据动作名称与任务描述，一步模拟额外给出下一观察和新可用动作，可揭示解锁后续机会。它仍只前瞻有限一步，评分模型也可能误判，因此不能把新增动作列表当完整长期规划 oracle。 例如“拿钥匙”看似不接近终点，但模拟后出现开门动作；若门后还有未知障碍，一步信息仍不能保证最终成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0bcf1b77a4cca239">与纯语义动作打分相比，一步模拟增加什么信息而仍不保证最优？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-lookahead">Code Owns the Simulation, Jev Owns the Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义打分主要依据动作名称与任务描述，一步模拟额外给出下一观察和新可用动作，可揭示解锁后续机会。它仍只前瞻有限一步，评分模型也可能误判，因此不能把新增动作列表当完整长期规划 oracle。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“拿钥匙”看似不接近终点，但模拟后出现开门动作；若门后还有未知障碍，一步信息仍不能保证最终成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01834">原论文</a> · <a href="../../../../agent-research/2610.01834-jev-lookahead/">实现解读</a> · <a href="#qa-0bcf1b77a4cca239">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-lookahead" data-paper-title="Code Owns the Simulation, Jev Owns the Evaluation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Code Owns the Simulation, Jev Owns the Evaluation Agent The Chinese University of Hong Kong 2026-10-01 让可执行代码负责模拟每个动作的后继状态，让 Jev 只负责比较动作带来的进展。除了当前动作和下一观察，还显式提供“执行后新出现的可用动作”，降低纯语义动作评分难以预判长期可达性的缺陷。 L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；L1 核心机制诊断：真实克隆环境、执行分支和调用既有 provider 协议；本地实验使用显式词法诊断 provider，没有调用真实 Jev，也不是 ALFWorld 成功率复现。尚未运行真实 Jev checkpoint/托管 API、ALFWorld 或机器人环境；本次不新增 CUDA 路径，不宣称 GPU 验证或 Evolve 能力提升。System One 方法索引保留交叉入口。运行 PYTHONPATH=src python scripts/run_oct04_seven_papers.py。  模拟前瞻与动作选择 System One Agent 规划与搜索：下一步该做什么 fork 返回不同对象是否已经足以保证分支隔离？ 不足。深层可变状态、随机数生成器和外部资源也要隔离，不能因对象身份不同就共享真实文件或模拟状态。step 只返回可观察字符串，reward、gold plan 和成功标签不传给决策器；选择结果还需属于合法候选，并由调用方执行。 例如两个浅拷贝共享同一背包列表，在副本拿钥匙会修改真实背包；这种实现虽有不同对象，仍破坏前瞻隔离。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f3aefdd9ad5723f6">fork 返回不同对象是否已经足以保证分支隔离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-lookahead">Code Owns the Simulation, Jev Owns the Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不足。深层可变状态、随机数生成器和外部资源也要隔离，不能因对象身份不同就共享真实文件或模拟状态。step 只返回可观察字符串，reward、gold plan 和成功标签不传给决策器；选择结果还需属于合法候选，并由调用方执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个浅拷贝共享同一背包列表，在副本拿钥匙会修改真实背包；这种实现虽有不同对象，仍破坏前瞻隔离。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01834">原论文</a> · <a href="../../../../agent-research/2610.01834-jev-lookahead/">实现解读</a> · <a href="#qa-f3aefdd9ad5723f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-spawn" data-paper-title="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces Agent 原文首页未列第一作者机构 2026-09-30 先从自然语言任务构造有限 compositional action space，以 Jev 分布并行保留多个分支；反馈更新后验并保留备选以支持恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Jev Agent 推理 分支搜索 Agent 规划与搜索：下一步该做什么 Agent 一条执行路线走不通时，JevSpawn 希望保留怎样的选择余地？ 长任务的早期判断可能不准，若过早把预算押在唯一行动，遇到反证就得重新寻找方案。JevSpawn 关注自适应推理分配：把任务的可选行动组织成可保留的组合分支，再根据执行反馈调整投入；保留的是备选机会，不是保证穷尽所有路线。 例如先检查本地资料或先联网搜索都可能合理，第一条路受阻后还应能接续另一条已准备路线，而不从空白计划重来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-jev-spawn-dc827975" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5a841ad22d666429">Agent 一条执行路线走不通时，JevSpawn 希望保留怎样的选择余地？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-spawn">JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长任务的早期判断可能不准，若过早把预算押在唯一行动，遇到反证就得重新寻找方案。JevSpawn 关注自适应推理分配：把任务的可选行动组织成可保留的组合分支，再根据执行反馈调整投入；保留的是备选机会，不是保证穷尽所有路线。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先检查本地资料或先联网搜索都可能合理，第一条路受阻后还应能接续另一条已准备路线，而不从空白计划重来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00437">原论文</a> · <a href="../../../../agent-research/2610.00437-jev-spawn/">实现解读</a> · <a href="#qa-5a841ad22d666429">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-spawn" data-paper-title="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces Agent 原文首页未列第一作者机构 2026-09-30 先从自然语言任务构造有限 compositional action space，以 Jev 分布并行保留多个分支；反馈更新后验并保留备选以支持恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Jev Agent 推理 分支搜索 Agent 规划与搜索：下一步该做什么 为什么保留多个动作分支，而不在第一次分布输出后立刻只留最高分？ 早期概率可能不准，多个组合动作保留了遇到反证时恢复的余地。新反馈对先验重新加权，后验应影响后续探索而不是回写过去的成功标签；分支数同时消耗预算，因此并行保留是风险与计算的取舍，不是自动穷尽所有可能。 例如先保留“搜索资料”和“检查本地文件”两条路，搜索无结果后仍能转向已保留的检查分支，而不必从零重建计划。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-spawn" data-paper-title="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces Agent 原文首页未列第一作者机构 2026-09-30 先从自然语言任务构造有限 compositional action space，以 Jev 分布并行保留多个分支；反馈更新后验并保留备选以支持恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Jev Agent 推理 分支搜索 Agent 规划与搜索：下一步该做什么 保留分支与每轮重新独立采样方案，恢复机制有何不同？ 保留分支保存早期未选方案的概率和状态，反馈后可继续利用；独立重采样可能重复旧错误或丢失已有进展。分支保留也占计算和记忆，不能只因保留更多候选就声称成本更低，需在相同预算下比较。 例如搜索分支失效后可转向已有文件检查分支；重新采样则可能又提出同一次无效搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-089d2009fb0016d1">保留分支与每轮重新独立采样方案，恢复机制有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-spawn">JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>保留分支保存早期未选方案的概率和状态，反馈后可继续利用；独立重采样可能重复旧错误或丢失已有进展。分支保留也占计算和记忆，不能只因保留更多候选就声称成本更低，需在相同预算下比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索分支失效后可转向已有文件检查分支；重新采样则可能又提出同一次无效搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00437">原论文</a> · <a href="../../../../agent-research/2610.00437-jev-spawn/">实现解读</a> · <a href="#qa-089d2009fb0016d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-spawn" data-paper-title="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces Agent 原文首页未列第一作者机构 2026-09-30 先从自然语言任务构造有限 compositional action space，以 Jev 分布并行保留多个分支；反馈更新后验并保留备选以支持恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Jev Agent 推理 分支搜索 Agent 规划与搜索：下一步该做什么 p(a)·exp(feedback) 更新后为什么仍需归一化与分支预算？ 乘法只给未归一化权重，必须除以所有候选权重和才能得到分布，再按有限预算保留分支。零先验分支无法仅靠这种乘法恢复，极大反馈也要注意数值稳定；本地仅验证有限后验和 top-branch retention，未调用 Jev checkpoint。 例如两分支原概率各一半，反馈分别为零和一，权重变为一比 e，不能直接把后一项 e/2 当合法概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e7e9f27b9bbfb974">p(a)·exp(feedback) 更新后为什么仍需归一化与分支预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-spawn">JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>乘法只给未归一化权重，必须除以所有候选权重和才能得到分布，再按有限预算保留分支。零先验分支无法仅靠这种乘法恢复，极大反馈也要注意数值稳定；本地仅验证有限后验和 top-branch retention，未调用 Jev checkpoint。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两分支原概率各一半，反馈分别为零和一，权重变为一比 e，不能直接把后一项 e/2 当合法概率。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00437">原论文</a> · <a href="../../../../agent-research/2610.00437-jev-spawn/">实现解读</a> · <a href="#qa-e7e9f27b9bbfb974">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-reasoning" data-paper-title="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning Agent Meta Superintelligence Labs 2026-09-29 把对象级工作交给 worker，把控制本身拆成 Assess、Propose、Evaluate 和 Dispatch；控制器只携带紧凑状态，通过持久 artifact memory 复用既有工作，并在统一调用预算内决定继续、分叉或停止。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agent 推理 元推理控制 预算调度 Agent 规划与搜索：下一步该做什么 对象级 worker 与元推理控制器的任务有什么不同？ worker 直接完成检索、编码或分析等任务内容，控制器则评估当前进度、提出继续或分叉动作、比较收益并派发。控制也会消耗模型调用预算，不能把控制器成本排除后再声称同预算更高效；持久工件帮助避免反复重复已有工作。 例如 worker 写测试文件，控制器决定下一步修失败、开另一方案还是停止；二者产物和成本不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-meta-reasoning-f28ad63c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-eae12a50db1347c2">对象级 worker 与元推理控制器的任务有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ameta-reasoning">Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>worker 直接完成检索、编码或分析等任务内容，控制器则评估当前进度、提出继续或分叉动作、比较收益并派发。控制也会消耗模型调用预算，不能把控制器成本排除后再声称同预算更高效；持久工件帮助避免反复重复已有工作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 worker 写测试文件，控制器决定下一步修失败、开另一方案还是停止；二者产物和成本不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38147">原论文</a> · <a href="../../../../agent-research/2609.38147-meta-reasoning/">实现解读</a> · <a href="#qa-eae12a50db1347c2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-reasoning" data-paper-title="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning Agent Meta Superintelligence Labs 2026-09-29 把对象级工作交给 worker，把控制本身拆成 Assess、Propose、Evaluate 和 Dispatch；控制器只携带紧凑状态，通过持久 artifact memory 复用既有工作，并在统一调用预算内决定继续、分叉或停止。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agent 推理 元推理控制 预算调度 Agent 规划与搜索：下一步该做什么 为什么控制器使用紧凑状态，却把完整工作成果放到 artifact memory？ 控制决策只需掌握进度、候选动作和剩余预算，完整材料若反复进入提示会增加成本。持久工件保存可复用证据，控制器按需引用，再通过 Assess、Propose、Evaluate、Dispatch 分工决定继续或分叉；压缩控制状态不应把真实成果一并丢掉。 例如两名 worker 已各写一份分析，控制器只保留结论与文件引用，需要核对时再打开原工件，无需每轮重抄全文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-reasoning" data-paper-title="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning Agent Meta Superintelligence Labs 2026-09-29 把对象级工作交给 worker，把控制本身拆成 Assess、Propose、Evaluate 和 Dispatch；控制器只携带紧凑状态，通过持久 artifact memory 复用既有工作，并在统一调用预算内决定继续、分叉或停止。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agent 推理 元推理控制 预算调度 Agent 规划与搜索：下一步该做什么 分成 Assess、Propose、Evaluate、Dispatch 与单次直接控制有什么取舍？ 拆分使状态总结、候选生成、比较和执行责任更明确，也能分别检查预算可行性；但增加控制步骤并非免费，任务过简单时可能不划算。直接控制更紧凑却可能混淆评估与执行，比较应计入全部调用与最终任务结果。 例如只有一步计算的任务可能无需四轮控制；复杂研究中先评估是否值得分叉则可能避免昂贵重复实验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6ef66348377903db">分成 Assess、Propose、Evaluate、Dispatch 与单次直接控制有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ameta-reasoning">Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>拆分使状态总结、候选生成、比较和执行责任更明确，也能分别检查预算可行性；但增加控制步骤并非免费，任务过简单时可能不划算。直接控制更紧凑却可能混淆评估与执行，比较应计入全部调用与最终任务结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只有一步计算的任务可能无需四轮控制；复杂研究中先评估是否值得分叉则可能避免昂贵重复实验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38147">原论文</a> · <a href="../../../../agent-research/2609.38147-meta-reasoning/">实现解读</a> · <a href="#qa-6ef66348377903db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:meta-reasoning" data-paper-title="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning Agent Meta Superintelligence Labs 2026-09-29 把对象级工作交给 worker，把控制本身拆成 Assess、Propose、Evaluate 和 Dispatch；控制器只携带紧凑状态，通过持久 artifact memory 复用既有工作，并在统一调用预算内决定继续、分叉或停止。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agent 推理 元推理控制 预算调度 Agent 规划与搜索：下一步该做什么 本地选择器如何处理预期价值与调用成本，哪些能力尚未验证？ 实现先排除预算不可行的 action，再按预期价值与调用成本选择，完整 artifact 留在持久 memory、控制 state 保持紧凑。预期值来自明确输入，不是已训练前沿 worker 的真实成功预测；当前三 seed 诊断只验证调度和状态分离。 例如剩两次调用时，需要三次的候选应直接不可行，即使预期价值最高；不能先派发后把超预算部分从账中删掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c44534433f4a5cec">本地选择器如何处理预期价值与调用成本，哪些能力尚未验证？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ameta-reasoning">Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实现先排除预算不可行的 action，再按预期价值与调用成本选择，完整 artifact 留在持久 memory、控制 state 保持紧凑。预期值来自明确输入，不是已训练前沿 worker 的真实成功预测；当前三 seed 诊断只验证调度和状态分离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如剩两次调用时，需要三次的候选应直接不可行，即使预期价值最高；不能先派发后把超预算部分从账中删掉。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38147">原论文</a> · <a href="../../../../agent-research/2609.38147-meta-reasoning/">实现解读</a> · <a href="#qa-c44534433f4a5cec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage-planner" data-paper-title="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners Agent 原文首页未列机构 2026-09-28 执行前用符号前置条件门阻止不安全动作并给出类型化原因；失败时只重写相关子目标的后缀，保留已完成前缀。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  规划 安全门 局部恢复 Agent 规划与搜索：下一步该做什么 符号 action gate 为什么要在动作执行前检查前置条件？ 前置条件用于判断当前世界是否允许动作，执行前拦截可避免已知不合法或不安全操作，并给规划器类型化原因。门只覆盖已建模规则，不能因为符号检查通过就宣称现实绝对安全；环境状态与规则若不完整仍可能失效。 例如抓取前要求手为空且物体可达，门可在执行前拦截“手里已有物体”的动作，而不是撞错后再解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-sage-planner-6e4e53de" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1a809b5b36798f25">符号 action gate 为什么要在动作执行前检查前置条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asage-planner">SAGE: Symbolic Action-Gating and Editing for LLM Task Planners</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前置条件用于判断当前世界是否允许动作，执行前拦截可避免已知不合法或不安全操作，并给规划器类型化原因。门只覆盖已建模规则，不能因为符号检查通过就宣称现实绝对安全；环境状态与规则若不完整仍可能失效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如抓取前要求手为空且物体可达，门可在执行前拦截“手里已有物体”的动作，而不是撞错后再解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34268">原论文</a> · <a href="../../../../agent-research/2609.34268-sage/">实现解读</a> · <a href="#qa-1a809b5b36798f25">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage-planner" data-paper-title="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners Agent 原文首页未列机构 2026-09-28 执行前用符号前置条件门阻止不安全动作并给出类型化原因；失败时只重写相关子目标的后缀，保留已完成前缀。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  规划 安全门 局部恢复 Agent 规划与搜索：下一步该做什么 失败后为什么只编辑相关子目标的后缀，而不重写整条计划？ 已完成前缀对应真实执行状态，全部重写容易重复动作或假设环境回到了起点。符号门先依据前置条件拦截并给类型化原因，再让规划器修复受影响的后续部分；保留前缀不是盲目坚持旧计划，而是维持与当前世界一致的执行历史。 例如杯子已经洗净、下一步发现柜门锁住，应修改放置方案，而不再把“洗杯子”重复执行并假设柜门早已打开。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage-planner" data-paper-title="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners Agent 原文首页未列机构 2026-09-28 执行前用符号前置条件门阻止不安全动作并给出类型化原因；失败时只重写相关子目标的后缀，保留已完成前缀。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  规划 安全门 局部恢复 Agent 规划与搜索：下一步该做什么 类型化失败原因与一段自由文本“失败了”相比有什么用？ 类型化原因把缺少资源、前提不满足或相关子目标问题区分开，局部编辑器可据此重写受影响后缀。泛化失败文本容易引发整计划重写或重复已完成动作；更明确的反馈也依赖符号状态正确，不能替代真实环境反馈。 例如“柜门上锁”应触发取钥匙或换位置，而“物体不存在”应触发重新感知，两者不是同一种恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-642090c6a6e8840c">类型化失败原因与一段自由文本“失败了”相比有什么用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asage-planner">SAGE: Symbolic Action-Gating and Editing for LLM Task Planners</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>类型化原因把缺少资源、前提不满足或相关子目标问题区分开，局部编辑器可据此重写受影响后缀。泛化失败文本容易引发整计划重写或重复已完成动作；更明确的反馈也依赖符号状态正确，不能替代真实环境反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“柜门上锁”应触发取钥匙或换位置，而“物体不存在”应触发重新感知，两者不是同一种恢复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34268">原论文</a> · <a href="../../../../agent-research/2609.34268-sage/">实现解读</a> · <a href="#qa-642090c6a6e8840c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage-planner" data-paper-title="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SAGE: Symbolic Action-Gating and Editing for LLM Task Planners Agent 原文首页未列机构 2026-09-28 执行前用符号前置条件门阻止不安全动作并给出类型化原因；失败时只重写相关子目标的后缀，保留已完成前缀。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  规划 安全门 局部恢复 Agent 规划与搜索：下一步该做什么 零 token gate 能证明完整 LLM 规划器已低成本复现吗？ 不能。零 token 只指符号门自身不调用语言模型，计划生成与后缀改写仍有各自成本。本地只执行 gate 和局部后缀编辑 reference，未运行 AI2-THOR；三 seed fixture 通过不能当真实具身任务成功率或端到端推理成本。 例如门用一个布尔检查拒绝开柜子，并不包含生成新计划的模型调用；只统计该检查会遗漏实际恢复成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4cc215ec54fd020d">零 token gate 能证明完整 LLM 规划器已低成本复现吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asage-planner">SAGE: Symbolic Action-Gating and Editing for LLM Task Planners</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。零 token 只指符号门自身不调用语言模型，计划生成与后缀改写仍有各自成本。本地只执行 gate 和局部后缀编辑 reference，未运行 AI2-THOR；三 seed fixture 通过不能当真实具身任务成功率或端到端推理成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如门用一个布尔检查拒绝开柜子，并不包含生成新计划的模型调用；只统计该检查会遗漏实际恢复成本。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34268">原论文</a> · <a href="../../../../agent-research/2609.34268-sage/">实现解读</a> · <a href="#qa-4cc215ec54fd020d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searchatlas" data-paper-title="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs Agent Duke University 2026-09-09 把搜索轨迹转为 query—evidence—answer 有向图，审计证据是否真正覆盖问题约束和最终回答。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  搜索 Agent 过程审计 Agent 规划与搜索：下一步该做什么 query—evidence—answer 图中的边为什么比网页清单更有解释力？ 边显式说明一次查询找到什么证据、证据支持哪个约束或回答片段，可追踪信息如何进入结论。网页清单只显示访问过的来源，无法自动证明推理支持关系；图解析本身也可能错误，因此边存在不等于事实已被可靠证实。 例如来源都在讨论价格，图可显示“当地可购买”结论没有入边，而一串十个链接不容易暴露这个缺口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-searchatlas-1aefb816" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-86d14a866c7a95dd">query—evidence—answer 图中的边为什么比网页清单更有解释力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearchatlas">SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>边显式说明一次查询找到什么证据、证据支持哪个约束或回答片段，可追踪信息如何进入结论。网页清单只显示访问过的来源，无法自动证明推理支持关系；图解析本身也可能错误，因此边存在不等于事实已被可靠证实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如来源都在讨论价格，图可显示“当地可购买”结论没有入边，而一串十个链接不容易暴露这个缺口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10901">原论文</a> · <a href="../../../../agent-research/2609.10901-searchatlas/">实现解读</a> · <a href="#qa-86d14a866c7a95dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searchatlas" data-paper-title="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs Agent Duke University 2026-09-09 把搜索轨迹转为 query—evidence—answer 有向图，审计证据是否真正覆盖问题约束和最终回答。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  搜索 Agent 过程审计 Agent 规划与搜索：下一步该做什么 为什么搜索很多网页仍可能在 evidential query graph 中暴露证据缺口？ 网页数量不是约束覆盖率。查询、证据与回答的有向关系要说明哪条证据支持哪个问题条件，最终结论是否跨越了未验证的边。图审计因此能区分重复搜到相同内容与真正补齐推理链；建立图的接口通过，也不等于搜索模型已经能可靠取证。 例如十篇网页都只说明产品价格，却没有一篇确认地区可用性；最终宣称“当地可以买到”仍缺少对应证据边。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searchatlas" data-paper-title="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs Agent Duke University 2026-09-09 把搜索轨迹转为 query—evidence—answer 有向图，审计证据是否真正覆盖问题约束和最终回答。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  搜索 Agent 过程审计 Agent 规划与搜索：下一步该做什么 搜索多样性与约束覆盖率为什么不是同一个指标？ 多样性描述查询或来源差别，覆盖率关注问题要求是否被证据支持。不同网站可能重复相同事实，少数高质量来源也可能覆盖多个要求；SearchAtlas 的图审计强调支持结构，不能只用访问域名数替代有效证据链。 例如来自五个网站的同一产品参数仍未回答售后政策，而一个官方政策页就可能补齐这个特定条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ff16d943d79eb7e9">搜索多样性与约束覆盖率为什么不是同一个指标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearchatlas">SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多样性描述查询或来源差别，覆盖率关注问题要求是否被证据支持。不同网站可能重复相同事实，少数高质量来源也可能覆盖多个要求；SearchAtlas 的图审计强调支持结构，不能只用访问域名数替代有效证据链。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如来自五个网站的同一产品参数仍未回答售后政策，而一个官方政策页就可能补齐这个特定条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10901">原论文</a> · <a href="../../../../agent-research/2609.10901-searchatlas/">实现解读</a> · <a href="#qa-ff16d943d79eb7e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:searchatlas" data-paper-title="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs Agent Duke University 2026-09-09 把搜索轨迹转为 query—evidence—answer 有向图，审计证据是否真正覆盖问题约束和最终回答。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  搜索 Agent 过程审计 Agent 规划与搜索：下一步该做什么 本地证据传播边验证是否包含论文搜索 Agent 和自动解析模型？ 不包含。本地只在公开 fixture 上构造与检查证据传播边，未运行论文五个搜索 Agent。原文 edge F1 是自动图解析与人工标注的一致性，不是本地问答准确率；图接口可执行也不能代表真实网页证据抽取和事实判断能力。 例如预先给定“证据甲支持约束乙”的边后验证连通性，不能证明模型能从任意网页正确抽取这条支持关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2deaaf979c81c85e">本地证据传播边验证是否包含论文搜索 Agent 和自动解析模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asearchatlas">SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不包含。本地只在公开 fixture 上构造与检查证据传播边，未运行论文五个搜索 Agent。原文 edge F1 是自动图解析与人工标注的一致性，不是本地问答准确率；图接口可执行也不能代表真实网页证据抽取和事实判断能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预先给定“证据甲支持约束乙”的边后验证连通性，不能证明模型能从任意网页正确抽取这条支持关系。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10901">原论文</a> · <a href="../../../../agent-research/2609.10901-searchatlas/">实现解读</a> · <a href="#qa-2deaaf979c81c85e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deeprepro" data-paper-title="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-08-27 一次性全局计划会在文件、依赖和接口持续变化时失效。DeepRepro 在每个阶段读取当前 repository state 和执行反馈，重写细粒度 subplan，再由 repository-aware orchestration 推进实现。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现 repository snapshot、state-aware subplan 与 runtime-feedback repair。未运行官方 PaperBench Code-Dev，也未把 deterministic plan/answer 满分包装成论文结果；本地验证的是状态驱动重规划路径。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300，并记录 state snapshots、subplan revisions 与 repairs。  论文到代码状态子规划 Agent 规划与搜索：下一步该做什么 论文复现为什么是一项持续变化的软件工程任务，而不只是翻译算法公式？ 公式只是部分规格，真实复现还会遇到依赖、数据格式、接口和测试约束。前一步实现会改变下一步可做的工作，DeepRepro 因而研究如何在不断演进的仓库中推进实现与验证，重点是维持论文目标和实际工程状态的联系，而非一次写出长计划就完成。 例如网络结构已经写好，数据加载却暴露新轴顺序要求，后续训练代码需适配真实接口，不能只照论文段落顺序继续补文件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-deeprepro-1ec5a199" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6b5488f16f6f2b49">论文复现为什么是一项持续变化的软件工程任务，而不只是翻译算法公式？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adeeprepro">DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式只是部分规格，真实复现还会遇到依赖、数据格式、接口和测试约束。前一步实现会改变下一步可做的工作，DeepRepro 因而研究如何在不断演进的仓库中推进实现与验证，重点是维持论文目标和实际工程状态的联系，而非一次写出长计划就完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如网络结构已经写好，数据加载却暴露新轴顺序要求，后续训练代码需适配真实接口，不能只照论文段落顺序继续补文件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26557">原论文</a> · <a href="../../../../agent-research/2608.26557-deeprepro/">实现解读</a> · <a href="#qa-6b5488f16f6f2b49">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deeprepro" data-paper-title="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-08-27 一次性全局计划会在文件、依赖和接口持续变化时失效。DeepRepro 在每个阶段读取当前 repository state 和执行反馈，重写细粒度 subplan，再由 repository-aware orchestration 推进实现。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现 repository snapshot、state-aware subplan 与 runtime-feedback repair。未运行官方 PaperBench Code-Dev，也未把 deterministic plan/answer 满分包装成论文结果；本地验证的是状态驱动重规划路径。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300，并记录 state snapshots、subplan revisions 与 repairs。  论文到代码状态子规划 Agent 规划与搜索：下一步该做什么 为什么论文到代码的子计划必须读取当前仓库状态，而不能只按论文顺序展开？ 实现过程中接口、依赖和文件会不断变化，上一阶段成立的假设可能已失效。细粒度子计划把当前 repository state 与执行反馈作为输入，重新决定下一步；论文定义提供目标约束，仓库状态提供可执行条件，二者都不能由初始的一份静态清单替代。 例如论文下一步要接评测器，但仓库刚改了数据接口；子计划应先适配新合同，而非照旧生成无法连接的实验脚本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deeprepro" data-paper-title="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-08-27 一次性全局计划会在文件、依赖和接口持续变化时失效。DeepRepro 在每个阶段读取当前 repository state 和执行反馈，重写细粒度 subplan，再由 repository-aware orchestration 推进实现。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现 repository snapshot、state-aware subplan 与 runtime-feedback repair。未运行官方 PaperBench Code-Dev，也未把 deterministic plan/answer 满分包装成论文结果；本地验证的是状态驱动重规划路径。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300，并记录 state snapshots、subplan revisions 与 repairs。  论文到代码状态子规划 Agent 规划与搜索：下一步该做什么 检查已有产物与重新执行复现流程，分别能回答什么问题？ 产物检查能核对代码、日志和测试记录是否对应指定论文与版本，适合审计已有执行；重新执行还要实际安装依赖、调用模型和运行测试，才能观察当前环境能否重现结果。两者证据范围不同，DeepRepro 本地 replay 的一致性不能代替一次完整 Code-Dev 执行。 教学例：日志里有测试通过记录，可检查它对应哪个提交；换到干净环境能否再次通过，仍需真实安装与运行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2b3ad56805903811">检查已有产物与重新执行复现流程，分别能回答什么问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adeeprepro">DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>产物检查能核对代码、日志和测试记录是否对应指定论文与版本，适合审计已有执行；重新执行还要实际安装依赖、调用模型和运行测试，才能观察当前环境能否重现结果。两者证据范围不同，DeepRepro 本地 replay 的一致性不能代替一次完整 Code-Dev 执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：日志里有测试通过记录，可检查它对应哪个提交；换到干净环境能否再次通过，仍需真实安装与运行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26557">原论文</a> · <a href="../../../../agent-research/2608.26557-deeprepro/">实现解读</a> · <a href="#qa-2b3ad56805903811">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:deeprepro" data-paper-title="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories Agent Institute of Computing Technology, Chinese Academy of Sciences 2026-08-27 一次性全局计划会在文件、依赖和接口持续变化时失效。DeepRepro 在每个阶段读取当前 repository state 和执行反馈，重写细粒度 subplan，再由 repository-aware orchestration 推进实现。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现 repository snapshot、state-aware subplan 与 runtime-feedback repair。未运行官方 PaperBench Code-Dev，也未把 deterministic plan/answer 满分包装成论文结果；本地验证的是状态驱动重规划路径。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300，并记录 state snapshots、subplan revisions 与 repairs。  论文到代码状态子规划 Agent 规划与搜索：下一步该做什么 产物 replay 能否算作已经重新执行官方 PaperBench Code-Dev？ 不能。replay 读取固定 revision 的真实导出，按论文和状态顺序检查计划、执行步骤与测试覆盖；它没有重新支付模型 API 和完整实现实验成本。确定性 mini-suite 满分也只验证状态驱动路径，不能与官方复现能力或成本直接横比。 例如回放旧测试记录能检查某次改计划是否覆盖失败项，但没有在当前环境重新生成代码并运行全部测试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c8ddcad1b744e2a8">产物 replay 能否算作已经重新执行官方 PaperBench Code-Dev？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adeeprepro">DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。replay 读取固定 revision 的真实导出，按论文和状态顺序检查计划、执行步骤与测试覆盖；它没有重新支付模型 API 和完整实现实验成本。确定性 mini-suite 满分也只验证状态驱动路径，不能与官方复现能力或成本直接横比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如回放旧测试记录能检查某次改计划是否覆盖失败项，但没有在当前环境重新生成代码并运行全部测试。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26557">原论文</a> · <a href="../../../../agent-research/2608.26557-deeprepro/">实现解读</a> · <a href="#qa-c8ddcad1b744e2a8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loongreflect" data-paper-title="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation Agent Authors did not disclose affiliation 2026-08-12 把 reflect/backtrack 视为可逆轨迹树的 memory-control actions，以 privileged teacher 快通道和 outcome GRPO 慢通道协调训练。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  反思 Agentic RL Agent 规划与搜索：下一步该做什么 长程搜索 Agent 为什么需要能恢复路线的反思，而不只在结尾解释失败？ 搜索常包含多跳取证与尝试，早期选错方向可能让后续步骤都围绕错误证据展开。LoongReflect 希望反思能改变当前信息状态和继续路径，让 Agent 在任务结束前恢复；结尾总结即使写得合理，也已经无法改善这次执行的后续取证。 例如一路搜索只找到同一报道的转载，Agent 应及时回到先前分叉换来源，而不是最终答案写完后才承认证据单一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-loongreflect-7debd709" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-29d2ec8bb15b0afd">长程搜索 Agent 为什么需要能恢复路线的反思，而不只在结尾解释失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aloongreflect">LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>搜索常包含多跳取证与尝试，早期选错方向可能让后续步骤都围绕错误证据展开。LoongReflect 希望反思能改变当前信息状态和继续路径，让 Agent 在任务结束前恢复；结尾总结即使写得合理，也已经无法改善这次执行的后续取证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一路搜索只找到同一报道的转载，Agent 应及时回到先前分叉换来源，而不是最终答案写完后才承认证据单一。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11967">原论文</a> · <a href="../../../../agent-research/2608.11967-loongreflect/">实现解读</a> · <a href="#qa-29d2ec8bb15b0afd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loongreflect" data-paper-title="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation Agent Authors did not disclose affiliation 2026-08-12 把 reflect/backtrack 视为可逆轨迹树的 memory-control actions，以 privileged teacher 快通道和 outcome GRPO 慢通道协调训练。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  反思 Agentic RL Agent 规划与搜索：下一步该做什么 为什么 reflect/backtrack 要建模为可逆的 memory-control actions？ 长搜索不仅选择外部动作，也要控制保留哪些轨迹、回到哪个分叉点。把反思和回退显式纳入策略，才能学习何时改变记忆状态；特权教师提供训练信号，结果奖励补充长期成败，但评测时不能把教师的全局视角或未来答案直接交给学生。 例如搜索走入死胡同后应回到前一个分支并保留失败原因；仅追加一段反思文字却不改变轨迹状态，不能实现真正回退。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loongreflect" data-paper-title="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation Agent Authors did not disclose affiliation 2026-08-12 把 reflect/backtrack 视为可逆轨迹树的 memory-control actions，以 privileged teacher 快通道和 outcome GRPO 慢通道协调训练。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  反思 Agentic RL Agent 规划与搜索：下一步该做什么 privileged teacher 快通道与 outcome GRPO 慢通道监督什么不同信号？ 快通道通过教师视角为反思相关决策提供细粒度蒸馏，慢通道用轨迹最终结果优化长程策略。前者提供局部引导，后者检验整体有效性；特权信息只能留在训练教师或评分侧，部署学生不能读取 gold 结果来选择回溯。 例如教师可指出某次搜索缺少关键证据，最终奖励再检验完整回答是否成功；学生在线仍只能根据已有观察行动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b29d7bd63cdc6137">privileged teacher 快通道与 outcome GRPO 慢通道监督什么不同信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aloongreflect">LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>快通道通过教师视角为反思相关决策提供细粒度蒸馏，慢通道用轨迹最终结果优化长程策略。前者提供局部引导，后者检验整体有效性；特权信息只能留在训练教师或评分侧，部署学生不能读取 gold 结果来选择回溯。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师可指出某次搜索缺少关键证据，最终奖励再检验完整回答是否成功；学生在线仍只能根据已有观察行动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11967">原论文</a> · <a href="../../../../agent-research/2608.11967-loongreflect/">实现解读</a> · <a href="#qa-b29d7bd63cdc6137">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:loongreflect" data-paper-title="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation Agent Authors did not disclose affiliation 2026-08-12 把 reflect/backtrack 视为可逆轨迹树的 memory-control actions，以 privileged teacher 快通道和 outcome GRPO 慢通道协调训练。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  反思 Agentic RL Agent 规划与搜索：下一步该做什么 本地 mini-suite 的低 average cost 能代表真实长上下文模型节省吗？ 不能。当前确定性 suite 验证反思、回溯与过程状态，不调用真实浏览器、外部工具或论文大模型。成本字段属于该诊断定义，正确率饱和时更应检查实际分支与记录，不将代理调用数直接换算真实 token 或 API 费用。 例如一个规则分支只记零点几单位成本，并不表示真实模型反思这一步只耗同样比例的 token 或时间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d989382ef608ad22">本地 mini-suite 的低 average cost 能代表真实长上下文模型节省吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aloongreflect">LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前确定性 suite 验证反思、回溯与过程状态，不调用真实浏览器、外部工具或论文大模型。成本字段属于该诊断定义，正确率饱和时更应检查实际分支与记录，不将代理调用数直接换算真实 token 或 API 费用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个规则分支只记零点几单位成本，并不表示真实模型反思这一步只耗同样比例的 token 或时间。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11967">原论文</a> · <a href="../../../../agent-research/2608.11967-loongreflect/">实现解读</a> · <a href="#qa-d989382ef608ad22">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toollift" data-paper-title="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning Agent Authors did not disclose affiliation 2026-08-04 把工具级历史轨迹提升为可跨工具集迁移的 function workflow graph，再解耦 workflow planning 与 tool selection。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 图结构 Agent 规划与搜索：下一步该做什么 工具集合经常更换时，ToolLIFT 希望迁移的是哪一部分经验？ 不同服务的 API 名、参数和返回格式会变，但任务常有稳定的功能步骤，例如先查身份再读取记录。ToolLIFT 关注保留这些程序性经验，再在当前工具目录里寻找实现方式，避免旧轨迹一换服务就报废；具体接口仍必须重新核对。 例如从甲系统迁到乙系统后，查客户再查订单的需求仍在，但原先两个函数名和字段不能直接复制到新系统。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-toollift-dbb897af" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-aa0bc3a2fde6af6b">工具集合经常更换时，ToolLIFT 希望迁移的是哪一部分经验？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoollift">ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同服务的 API 名、参数和返回格式会变，但任务常有稳定的功能步骤，例如先查身份再读取记录。ToolLIFT 关注保留这些程序性经验，再在当前工具目录里寻找实现方式，避免旧轨迹一换服务就报废；具体接口仍必须重新核对。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从甲系统迁到乙系统后，查客户再查订单的需求仍在，但原先两个函数名和字段不能直接复制到新系统。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03468">原论文</a> · <a href="../../../../agent-research/2608.03468-toollift/">实现解读</a> · <a href="#qa-aa0bc3a2fde6af6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toollift" data-paper-title="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning Agent Authors did not disclose affiliation 2026-08-04 把工具级历史轨迹提升为可跨工具集迁移的 function workflow graph，再解耦 workflow planning 与 tool selection。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 图结构 Agent 规划与搜索：下一步该做什么 把轨迹提升为 function workflow graph，为什么有利于换一套工具后复用计划？ 功能图保留“需要完成哪种操作及其依赖”，把具体工具名称与接口推迟到执行时选择。换工具集后仍可沿功能关系规划，再按当前 schema 找实现；这不是忽略参数合同，功能节点仍须由具备所需输入输出能力的真实工具完成。 例如旧工具叫 search_web、新工具叫 lookup，若二者都实现查找证据功能，工作流可复用，但参数与返回格式还须重新匹配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toollift" data-paper-title="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning Agent Authors did not disclose affiliation 2026-08-04 把工具级历史轨迹提升为可跨工具集迁移的 function workflow graph，再解耦 workflow planning 与 tool selection。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 图结构 Agent 规划与搜索：下一步该做什么 功能 workflow graph 与可直接执行的工具调用计划，分别需要哪些信息？ 功能图描述目标操作与状态依赖，可跨工具目录保留程序性结构；可执行计划还必须把每个节点绑定到当前 API、参数和实际可用对象。前者提供迁移用的抽象，后者承担接口落地，缺少任一层都不能保证执行：图合理不等于参数合法，调用合法也不等于功能完整。 教学例：功能图写“查客户→查订单”；落地时仍要确认新服务返回 customer_id 还是 account_id，以及订单接口接受哪个字段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9cee31815ddb00c9">功能 workflow graph 与可直接执行的工具调用计划，分别需要哪些信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoollift">ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>功能图描述目标操作与状态依赖，可跨工具目录保留程序性结构；可执行计划还必须把每个节点绑定到当前 API、参数和实际可用对象。前者提供迁移用的抽象，后者承担接口落地，缺少任一层都不能保证执行：图合理不等于参数合法，调用合法也不等于功能完整。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：功能图写“查客户→查订单”；落地时仍要确认新服务返回 customer_id 还是 account_id，以及订单接口接受哪个字段。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03468">原论文</a> · <a href="../../../../agent-research/2608.03468-toollift/">实现解读</a> · <a href="#qa-9cee31815ddb00c9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toollift" data-paper-title="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning Agent Authors did not disclose affiliation 2026-08-04 把工具级历史轨迹提升为可跨工具集迁移的 function workflow graph，再解耦 workflow planning 与 tool selection。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 图结构 Agent 规划与搜索：下一步该做什么 Lift 与 Select 两步实现时，为什么要保留状态依赖而不只存功能列表？ 图边说明后一步需要前一步产生的证据或对象，Select 还要根据当前状态选择工具。无序功能列表会丢掉变量来源和执行前提；本地 mini-suite 只验证提升与选择控制流，未调用真实工具集，不能用其满分推断未见服务泛化。 例如先查订单得到 order_id，再取消该订单；只存“查询、取消”而不绑定 ID，会让第二步无法构造合法调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c8419e689fae8c59">Lift 与 Select 两步实现时，为什么要保留状态依赖而不只存功能列表？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoollift">ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图边说明后一步需要前一步产生的证据或对象，Select 还要根据当前状态选择工具。无序功能列表会丢掉变量来源和执行前提；本地 mini-suite 只验证提升与选择控制流，未调用真实工具集，不能用其满分推断未见服务泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先查订单得到 order_id，再取消该订单；只存“查询、取消”而不绑定 ID，会让第二步无法构造合法调用。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03468">原论文</a> · <a href="../../../../agent-research/2608.03468-toollift/">实现解读</a> · <a href="#qa-c8419e689fae8c59">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagent" data-paper-title="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents Agent University of New South Wales 2026-07-31 把工具建模为 input-schema→output-schema 超边，先构造 Task DAG，再按状态缺口扩展 producer tool support graph。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 超图 Agent 规划与搜索：下一步该做什么 为什么找到一个名称相关的工具，还不足以完成多步工具任务？ 工具能不能调用取决于输入是否已经取得，输出又可能是后一步必需的资源。HyperAgent 研究如何把任务要求与这些生产依赖联系起来，补齐当前状态缺口，而不只挑文字最相似的接口；完整流程需要多个合法转移共同形成。 例如检索到“退款”工具仍不能直接退款，可能还需订单标识和付款记录，任务首先缺的是产生这些输入的步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-hyperagent-a4e2dd7a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0427e40b15649248">为什么找到一个名称相关的工具，还不足以完成多步工具任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahyperagent">HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of New South Wales</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具能不能调用取决于输入是否已经取得，输出又可能是后一步必需的资源。HyperAgent 研究如何把任务要求与这些生产依赖联系起来，补齐当前状态缺口，而不只挑文字最相似的接口；完整流程需要多个合法转移共同形成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如检索到“退款”工具仍不能直接退款，可能还需订单标识和付款记录，任务首先缺的是产生这些输入的步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02650">原论文</a> · <a href="../../../../agent-research/2608.02650-hyperagent/">实现解读</a> · <a href="#qa-0427e40b15649248">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagent" data-paper-title="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents Agent University of New South Wales 2026-07-31 把工具建模为 input-schema→output-schema 超边，先构造 Task DAG，再按状态缺口扩展 producer tool support graph。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 超图 Agent 规划与搜索：下一步该做什么 工具为什么用输入到输出的超边表示，而不只按名称做相似度检索？ 一个工具可能同时要求多种输入并产生多个输出，超边能表达这些联合前提。任务 DAG 先明确缺什么状态，再沿 producer 关系寻找能补齐输入的工具链；名称相似只说明文字接近，不能保证所选工具拿得到必需参数或能生成后续所需字段。 例如发票工具同时需要订单号与税号，前一步只找到订单号还不能执行；超图会继续寻找税号生产者，而不直接调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagent" data-paper-title="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents Agent University of New South Wales 2026-07-31 把工具建模为 input-schema→output-schema 超边，先构造 Task DAG，再按状态缺口扩展 producer tool support graph。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 超图 Agent 规划与搜索：下一步该做什么 任务 DAG 与 producer support graph 分别描述需求还是供给？ 任务 DAG 表达目标状态之间的依赖，说明完成后续子任务还缺哪些输入；producer support graph 从工具 schema 描述谁能生产这些输入，以及生产者自身还需要什么。两张结构配合才能把需求连成可执行工具链；工具有生产能力并不表示该输出已经存在。 教学例：任务要求给订单退款，DAG 暴露订单号缺口；support graph 找到查订单工具，再检查它需要的用户标识能否先取得。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f1e6035a16e9d1f6">任务 DAG 与 producer support graph 分别描述需求还是供给？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahyperagent">HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of New South Wales</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务 DAG 表达目标状态之间的依赖，说明完成后续子任务还缺哪些输入；producer support graph 从工具 schema 描述谁能生产这些输入，以及生产者自身还需要什么。两张结构配合才能把需求连成可执行工具链；工具有生产能力并不表示该输出已经存在。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：任务要求给订单退款，DAG 暴露订单号缺口；support graph 找到查订单工具，再检查它需要的用户标识能否先取得。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02650">原论文</a> · <a href="../../../../agent-research/2608.02650-hyperagent/">实现解读</a> · <a href="#qa-f1e6035a16e9d1f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hyperagent" data-paper-title="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents Agent University of New South Wales 2026-07-31 把工具建模为 input-schema→output-schema 超边，先构造 Task DAG，再按状态缺口扩展 producer tool support graph。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  工具规划 超图 Agent 规划与搜索：下一步该做什么 扩展 producer 时，如何避免把工具输出当成已经存在的状态？ 图中的生产能力仅代表调用后可能得到字段，执行前仍需确认所有输入实际可用，并在真实结果后更新状态。当前本地在确定性 planbench 验证依赖路径，未运行 AppWorld；图节点齐全或 mini-suite 满分不能替代实际 API 返回和任务验证。 例如图显示查客户可产出 customer_id，不代表 ID 已可用；必须真正查询并核对结果，不能凭 schema 直接填一个 ID。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-24ccc7bcfe4e43ea">扩展 producer 时，如何避免把工具输出当成已经存在的状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahyperagent">HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of New South Wales</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图中的生产能力仅代表调用后可能得到字段，执行前仍需确认所有输入实际可用，并在真实结果后更新状态。当前本地在确定性 planbench 验证依赖路径，未运行 AppWorld；图节点齐全或 mini-suite 满分不能替代实际 API 返回和任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图显示查客户可产出 customer_id，不代表 ID 已可用；必须真正查询并核对结果，不能凭 schema 直接填一个 ID。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02650">原论文</a> · <a href="../../../../agent-research/2608.02650-hyperagent/">实现解读</a> · <a href="#qa-24ccc7bcfe4e43ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sira" data-paper-title="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval Agent Meta Superintelligence Labs / Rice University（工作完成于 Meta） 2026-05-07 冻结 LLM 先生成相关证据可能使用、但原查询缺失的词汇，再用倒排索引中的文档频率过滤不存在或过于常见的词；原查询与验证后的扩展只执行一次加权 BM25。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。三种子诊断：metrics/mechanism-seeds42-44.json  Agent 检索 语料感知查询扩展 BM25 Agent 规划与搜索：下一步该做什么 SIRA 为什么关注“用户问法与证据用词不同”的检索困难？ 倒排检索依赖词项重合，用户可能描述一个现象，文档却使用专业术语或另一种表达，相关证据因此排不到前面。SIRA 利用冻结 LLM 补充可能的证据词汇，再以当前语料约束扩展，目标是改善查询与文档之间的词汇桥接，而非训练新的答案生成器。 例如用户问“程序越跑越占内存”，技术文档可能写 memory leak；补上该术语有机会召回原问句未命中的材料。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-sira-e870822f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d078f361bd045793">SIRA 为什么关注“用户问法与证据用词不同”的检索困难？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asira">Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / Rice University（工作完成于 Meta）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>倒排检索依赖词项重合，用户可能描述一个现象，文档却使用专业术语或另一种表达，相关证据因此排不到前面。SIRA 利用冻结 LLM 补充可能的证据词汇，再以当前语料约束扩展，目标是改善查询与文档之间的词汇桥接，而非训练新的答案生成器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户问“程序越跑越占内存”，技术文档可能写 memory leak；补上该术语有机会召回原问句未命中的材料。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.06647">原论文</a> · <a href="../../../../agent-research/2605.06647-sira/">实现解读</a> · <a href="#qa-d078f361bd045793">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sira" data-paper-title="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval Agent Meta Superintelligence Labs / Rice University（工作完成于 Meta） 2026-05-07 冻结 LLM 先生成相关证据可能使用、但原查询缺失的词汇，再用倒排索引中的文档频率过滤不存在或过于常见的词；原查询与验证后的扩展只执行一次加权 BM25。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。三种子诊断：metrics/mechanism-seeds42-44.json  Agent 检索 语料感知查询扩展 BM25 Agent 规划与搜索：下一步该做什么 生成的扩展词为什么还要用倒排索引里的文档频率过滤？ LLM 可能提出语义合理却不在语料里的词，也可能加入到处都出现、没有区分力的词。文档频率约束先验证这些扩展确实可检索且不过泛，再与原查询做一次加权 BM25；它保留词法检索路径，不是让模型想象词存在就当成已找到证据。 例如查询稀有疾病时，扩展出语料没有的缩写不会带来召回；扩展成“研究”又太泛，过滤后才有有效词项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sira" data-paper-title="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval Agent Meta Superintelligence Labs / Rice University（工作完成于 Meta） 2026-05-07 冻结 LLM 先生成相关证据可能使用、但原查询缺失的词汇，再用倒排索引中的文档频率过滤不存在或过于常见的词；原查询与验证后的扩展只执行一次加权 BM25。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。三种子诊断：metrics/mechanism-seeds42-44.json  Agent 检索 语料感知查询扩展 BM25 Agent 规划与搜索：下一步该做什么 单次加权 BM25 扩展与多轮 agent 搜索在控制流上有何不同？ SIRA 先生成并过滤缺失词，再将原查询与扩展共同用于一次加权检索，没有每轮看结果后再规划搜索的长闭环。它减少交互结构复杂度，也限制了对初次失败的适应性；不能因名称含 agent 就假定存在多轮自纠错。 例如一次扩展得到三个术语后直接返回排名，不会自动阅读首轮网页再提出另一组问题，除非另加外层流程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-229c1af05a1fd56e">单次加权 BM25 扩展与多轮 agent 搜索在控制流上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asira">Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / Rice University（工作完成于 Meta）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SIRA 先生成并过滤缺失词，再将原查询与扩展共同用于一次加权检索，没有每轮看结果后再规划搜索的长闭环。它减少交互结构复杂度，也限制了对初次失败的适应性；不能因名称含 agent 就假定存在多轮自纠错。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次扩展得到三个术语后直接返回排名，不会自动阅读首轮网页再提出另一组问题，除非另加外层流程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.06647">原论文</a> · <a href="../../../../agent-research/2605.06647-sira/">实现解读</a> · <a href="#qa-229c1af05a1fd56e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sira" data-paper-title="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval Agent Meta Superintelligence Labs / Rice University（工作完成于 Meta） 2026-05-07 冻结 LLM 先生成相关证据可能使用、但原查询缺失的词汇，再用倒排索引中的文档频率过滤不存在或过于常见的词；原查询与验证后的扩展只执行一次加权 BM25。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，也不把公开离线结果写成线上 A/B。三种子诊断：metrics/mechanism-seeds42-44.json  Agent 检索 语料感知查询扩展 BM25 Agent 规划与搜索：下一步该做什么 DF 条件的零值、上界和原查询权重应怎样处理？ 扩展词必须满足 0&lt;DF(t)≤τ|C|，零频词与超过上界的词都排除；最终分数保留原查询 BM25，再加 w 倍扩展部分。不能用扩展替换原查询或悄悄改变为多轮检索，本地只实现该 gate 和组合，没有论文规模索引与 LLM。 例如过滤后扩展为空，系统仍应由原查询产生结果，而不是因没有新词就把整个查询丢掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fc6b1d788aba3b86">DF 条件的零值、上界和原查询权重应怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asira">Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / Rice University（工作完成于 Meta）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>扩展词必须满足 0&lt;DF(t)≤τ|C|，零频词与超过上界的词都排除；最终分数保留原查询 BM25，再加 w 倍扩展部分。不能用扩展替换原查询或悄悄改变为多轮检索，本地只实现该 gate 和组合，没有论文规模索引与 LLM。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如过滤后扩展为空，系统仍应由原查询产生结果，而不是因没有新词就把整个查询丢掉。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.06647">原论文</a> · <a href="../../../../agent-research/2605.06647-sira/">实现解读</a> · <a href="#qa-fc6b1d788aba3b86">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lats" data-paper-title="LATS" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LATS Agent University of Illinois Urbana-Champaign 2023-10-06 ReAct 等方法通常沿单条轨迹行动，失败后缺少系统搜索。LATS 把 LM 同时作为 agent、value function 和 optimizer，嵌入 Monte Carlo Tree Search；环境执行提供外部 reward，失败轨迹生成 reflection，帮助后续搜索避开错误。 本页实现 UCT 式树搜索、完整 trajectory rollout、环境 reward、反思与回溯。保留 MCTS statistics、环境反馈、reflection 与回溯；本地树以完整计划为叶节点，未调用 LM value model、HumanEval executor 或 WebShop，搜索规模远小于论文。每个 PlanBench episode 搜索四条完整计划轨迹；环境返回 exact plan reward，失败轨迹产生 reflection/backtrack，再按累计 value 选最终路径。  Agent 搜索 Agent 规划与搜索：下一步该做什么 为什么在工具任务中生成一条看似合理的推理链，还不足以完成 LATS 要处理的问题？ 工具或环境可能返回与预想不同的结果，单一路线失败后也未必能继续。LATS 把推理和行动放进可探索的搜索树，让候选通过执行反馈接受检验，并利用失败反思尝试其他路线。目标是把语言提案与环境结果连接起来，搜索预算和判断错误仍会限制效果。 教学例：网页搜索第一条结果没有所需价格，Agent 可以回到先前搜索节点改关键词，而不是沿错误页面继续编答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-lats-45a406fd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a4512e5b0943abd6">为什么在工具任务中生成一条看似合理的推理链，还不足以完成 LATS 要处理的问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alats">LATS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具或环境可能返回与预想不同的结果，单一路线失败后也未必能继续。LATS 把推理和行动放进可探索的搜索树，让候选通过执行反馈接受检验，并利用失败反思尝试其他路线。目标是把语言提案与环境结果连接起来，搜索预算和判断错误仍会限制效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：网页搜索第一条结果没有所需价格，Agent 可以回到先前搜索节点改关键词，而不是沿错误页面继续编答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.04406">原论文</a> · <a href="../../../../agent-research/2310.04406-lats/">实现解读</a> · <a href="#qa-a4512e5b0943abd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lats" data-paper-title="LATS" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LATS Agent University of Illinois Urbana-Champaign 2023-10-06 ReAct 等方法通常沿单条轨迹行动，失败后缺少系统搜索。LATS 把 LM 同时作为 agent、value function 和 optimizer，嵌入 Monte Carlo Tree Search；环境执行提供外部 reward，失败轨迹生成 reflection，帮助后续搜索避开错误。 本页实现 UCT 式树搜索、完整 trajectory rollout、环境 reward、反思与回溯。保留 MCTS statistics、环境反馈、reflection 与回溯；本地树以完整计划为叶节点，未调用 LM value model、HumanEval executor 或 WebShop，搜索规模远小于论文。每个 PlanBench episode 搜索四条完整计划轨迹；环境返回 exact plan reward，失败轨迹产生 reflection/backtrack，再按累计 value 选最终路径。  Agent 搜索 Agent 规划与搜索：下一步该做什么 UCT 中探索项为什么能让暂时低分的动作仍获得尝试？ 平均价值反映已见回报，探索项随父节点访问增多、子动作访问稀少而变大，给不确定分支试验机会。执行反馈再更新价值，失败反思帮助后续扩展；若仅反复选当前最高估值，就可能过早锁定错误分支，模型自评分也不能替代环境反馈。 例如动作甲试了十次均一般，乙只试一次失败，UCT 可能再探乙以减少不确定性，而不是从此把它永久排除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lats" data-paper-title="LATS" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LATS Agent University of Illinois Urbana-Champaign 2023-10-06 ReAct 等方法通常沿单条轨迹行动，失败后缺少系统搜索。LATS 把 LM 同时作为 agent、value function 和 optimizer，嵌入 Monte Carlo Tree Search；环境执行提供外部 reward，失败轨迹生成 reflection，帮助后续搜索避开错误。 本页实现 UCT 式树搜索、完整 trajectory rollout、环境 reward、反思与回溯。保留 MCTS statistics、环境反馈、reflection 与回溯；本地树以完整计划为叶节点，未调用 LM value model、HumanEval executor 或 WebShop，搜索规模远小于论文。每个 PlanBench episode 搜索四条完整计划轨迹；环境返回 exact plan reward，失败轨迹产生 reflection/backtrack，再按累计 value 选最终路径。  Agent 搜索 Agent 规划与搜索：下一步该做什么 LATS 的 MCTS 与按层保留若干 thought 的搜索，在预算分配上有什么区别？ MCTS 沿已有树反复选择分支、执行 rollout，再回传回报与访问统计，可把后续预算投向值得重访的路径；按层保留 thought 的方法通常在同一深度比较并裁剪前沿。两者都依赖候选与评价质量，区别是搜索组织和反馈利用方式，不能据此断言某类任务必然更优。 教学例：深度二的一条路线曾接近成功，MCTS 可再深入它；固定层宽搜索则可能在该层只按当前评价保留若干候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ffb7fa4c1fedb88d">LATS 的 MCTS 与按层保留若干 thought 的搜索，在预算分配上有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alats">LATS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MCTS 沿已有树反复选择分支、执行 rollout，再回传回报与访问统计，可把后续预算投向值得重访的路径；按层保留 thought 的方法通常在同一深度比较并裁剪前沿。两者都依赖候选与评价质量，区别是搜索组织和反馈利用方式，不能据此断言某类任务必然更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：深度二的一条路线曾接近成功，MCTS 可再深入它；固定层宽搜索则可能在该层只按当前评价保留若干候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.04406">原论文</a> · <a href="../../../../agent-research/2310.04406-lats/">实现解读</a> · <a href="#qa-ffb7fa4c1fedb88d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lats" data-paper-title="LATS" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="LATS Agent University of Illinois Urbana-Champaign 2023-10-06 ReAct 等方法通常沿单条轨迹行动，失败后缺少系统搜索。LATS 把 LM 同时作为 agent、value function 和 optimizer，嵌入 Monte Carlo Tree Search；环境执行提供外部 reward，失败轨迹生成 reflection，帮助后续搜索避开错误。 本页实现 UCT 式树搜索、完整 trajectory rollout、环境 reward、反思与回溯。保留 MCTS statistics、环境反馈、reflection 与回溯；本地树以完整计划为叶节点，未调用 LM value model、HumanEval executor 或 WebShop，搜索规模远小于论文。每个 PlanBench episode 搜索四条完整计划轨迹；环境返回 exact plan reward，失败轨迹产生 reflection/backtrack，再按累计 value 选最终路径。  Agent 搜索 Agent 规划与搜索：下一步该做什么 本地完整计划叶节点搜索是否等同论文的 LM value 搜索？ 不等同。当前保留 MCTS 统计、环境奖励、反思与回溯，但以完整计划作为叶节点，未调用 LM value、HumanEval executor 或 WebShop。其确定性 mini-suite 满分只能验证搜索路径，不能当成论文代码生成或网页任务成功率。 例如四条预构造完整路线中选到合法路线，和在真实网页逐步生成行动、评估中间节点不是同等任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9671962608dc8011">本地完整计划叶节点搜索是否等同论文的 LM value 搜索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alats">LATS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等同。当前保留 MCTS 统计、环境奖励、反思与回溯，但以完整计划作为叶节点，未调用 LM value、HumanEval executor 或 WebShop。其确定性 mini-suite 满分只能验证搜索路径，不能当成论文代码生成或网页任务成功率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四条预构造完整路线中选到合法路线，和在真实网页逐步生成行动、评估中间节点不是同等任务。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.04406">原论文</a> · <a href="../../../../agent-research/2310.04406-lats/">实现解读</a> · <a href="#qa-9671962608dc8011">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rewoo" data-paper-title="ReWOO" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReWOO Agent Microsoft Research 2023-05-29 ReAct 在每次工具返回后重新调用 LLM，token 和推理成本随轨迹增长。ReWOO 的 Planner 用变量引用写出完整多步计划，Worker 只负责填入工具证据，Solver 最后读取计划与证据生成答案，因此 Planner 不被中间观察反复打断。 ReWOO 先一次性生成带依赖的完整计划，再由 Worker 执行工具，最后由 Solver 汇总；避免 ReAct 每一步都把不断增长的 observation 送回 Planner。实现 Planner/Worker/Solver 解耦、显式依赖与证据汇总；本地没有真实搜索 API 和多尺寸 LLM，因此只验证控制流与调用计数，不复刻 HotpotQA 的语言生成分数。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.5000，生成 120 份完整计划并执行 360 次 worker/tool action。  解耦规划 Agent 规划与搜索：下一步该做什么 多步工具任务为什么可能把大量费用花在重复阅读既有内容上？ 若每次工具返回都重新让规划模型读取任务、旧计划和全部证据，输入会随流程增长，即使下一步只是填入一个已知结果。ReWOO 研究将规划、工具执行和最后综合分工，减少重复的规划工作；它适合可预先表达依赖的流程，意外情况仍需恢复设计。 例如先找作者再查出生地，两步结构已清楚，不必每拿到一个字符串都重新生成整份计划和重读之前所有证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-rewoo-abc51544" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f60bde583743c4b5">多步工具任务为什么可能把大量费用花在重复阅读既有内容上？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arewoo">ReWOO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若每次工具返回都重新让规划模型读取任务、旧计划和全部证据，输入会随流程增长，即使下一步只是填入一个已知结果。ReWOO 研究将规划、工具执行和最后综合分工，减少重复的规划工作；它适合可预先表达依赖的流程，意外情况仍需恢复设计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先找作者再查出生地，两步结构已清楚，不必每拿到一个字符串都重新生成整份计划和重读之前所有证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18323">原论文</a> · <a href="../../../../agent-research/2305.18323-rewoo/">实现解读</a> · <a href="#qa-f60bde583743c4b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rewoo" data-paper-title="ReWOO" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReWOO Agent Microsoft Research 2023-05-29 ReAct 在每次工具返回后重新调用 LLM，token 和推理成本随轨迹增长。ReWOO 的 Planner 用变量引用写出完整多步计划，Worker 只负责填入工具证据，Solver 最后读取计划与证据生成答案，因此 Planner 不被中间观察反复打断。 ReWOO 先一次性生成带依赖的完整计划，再由 Worker 执行工具，最后由 Solver 汇总；避免 ReAct 每一步都把不断增长的 observation 送回 Planner。实现 Planner/Worker/Solver 解耦、显式依赖与证据汇总；本地没有真实搜索 API 和多尺寸 LLM，因此只验证控制流与调用计数，不复刻 HotpotQA 的语言生成分数。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.5000，生成 120 份完整计划并执行 360 次 worker/tool action。  解耦规划 Agent 规划与搜索：下一步该做什么 Planner 不反复读取中间观察，为什么仍能表达工具之间的依赖？ 它先把依赖写成变量引用，Worker 执行时把已得到证据填入后续工具参数，Solver 最后统一使用成果。因此减少的是反复规划调用，不是删除数据流；若后续路线真的依赖尚未知的观察而初始计划没有表达，静态计划也会受适应性限制。 例如先查人物出生地记为 E1，再用 E1 查当地人口；第二步的具体城市可晚绑定，而无需 Planner 每次重新生成整段计划。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rewoo" data-paper-title="ReWOO" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReWOO Agent Microsoft Research 2023-05-29 ReAct 在每次工具返回后重新调用 LLM，token 和推理成本随轨迹增长。ReWOO 的 Planner 用变量引用写出完整多步计划，Worker 只负责填入工具证据，Solver 最后读取计划与证据生成答案，因此 Planner 不被中间观察反复打断。 ReWOO 先一次性生成带依赖的完整计划，再由 Worker 执行工具，最后由 Solver 汇总；避免 ReAct 每一步都把不断增长的 observation 送回 Planner。实现 Planner/Worker/Solver 解耦、显式依赖与证据汇总；本地没有真实搜索 API 和多尺寸 LLM，因此只验证控制流与调用计数，不复刻 HotpotQA 的语言生成分数。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.5000，生成 120 份完整计划并执行 360 次 worker/tool action。  解耦规划 Agent 规划与搜索：下一步该做什么 ReWOO 与 ReAct 在适应中间异常方面有什么取舍？ ReAct 每轮观察后重新推理，可调整后续路线但重复模型调用成本较高；ReWOO 先规划后执行，减少规划器反复读取证据，却更依赖初始依赖计划可行。遇到意外错误需要额外恢复设计，不能把静态计划天然视为完整闭环。 例如首个查询返回多个同名人时，ReAct 可立即加消歧；ReWOO 原计划若未安排该分支，需要外层处理而非盲目继续。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b757f2600787d3fc">ReWOO 与 ReAct 在适应中间异常方面有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arewoo">ReWOO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ReAct 每轮观察后重新推理，可调整后续路线但重复模型调用成本较高；ReWOO 先规划后执行，减少规划器反复读取证据，却更依赖初始依赖计划可行。遇到意外错误需要额外恢复设计，不能把静态计划天然视为完整闭环。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如首个查询返回多个同名人时，ReAct 可立即加消歧；ReWOO 原计划若未安排该分支，需要外层处理而非盲目继续。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18323">原论文</a> · <a href="../../../../agent-research/2305.18323-rewoo/">实现解读</a> · <a href="#qa-b757f2600787d3fc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rewoo" data-paper-title="ReWOO" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReWOO Agent Microsoft Research 2023-05-29 ReAct 在每次工具返回后重新调用 LLM，token 和推理成本随轨迹增长。ReWOO 的 Planner 用变量引用写出完整多步计划，Worker 只负责填入工具证据，Solver 最后读取计划与证据生成答案，因此 Planner 不被中间观察反复打断。 ReWOO 先一次性生成带依赖的完整计划，再由 Worker 执行工具，最后由 Solver 汇总；避免 ReAct 每一步都把不断增长的 observation 送回 Planner。实现 Planner/Worker/Solver 解耦、显式依赖与证据汇总；本地没有真实搜索 API 和多尺寸 LLM，因此只验证控制流与调用计数，不复刻 HotpotQA 的语言生成分数。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.5000，生成 120 份完整计划并执行 360 次 worker/tool action。  解耦规划 Agent 规划与搜索：下一步该做什么 Worker 何时能并行执行，何时必须等待证据变量？ 没有未满足依赖的调用可以并行，引用前面 E 变量的调用必须等结果可用。Solver 最后同时读取计划与真实证据，不能用 Planner 想象的结果代替工具观察；本地只验证控制流与计数，没有真实搜索 API 或多尺寸 LLM 比较。 例如两个独立城市天气查询可并行，但“查询刚找到的城市天气”必须等城市检索结果，不能提前猜参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-124386a640c92e78">Worker 何时能并行执行，何时必须等待证据变量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arewoo">ReWOO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有未满足依赖的调用可以并行，引用前面 E 变量的调用必须等结果可用。Solver 最后同时读取计划与真实证据，不能用 Planner 想象的结果代替工具观察；本地只验证控制流与计数，没有真实搜索 API 或多尺寸 LLM 比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个独立城市天气查询可并行，但“查询刚找到的城市天气”必须等城市检索结果，不能提前猜参数。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18323">原论文</a> · <a href="../../../../agent-research/2305.18323-rewoo/">实现解读</a> · <a href="#qa-124386a640c92e78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tree-of-thoughts" data-paper-title="Tree of Thoughts" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Tree of Thoughts Agent Princeton University 2023-05-17 自回归生成和单条 CoT 很难撤销早期错误。ToT 将中间推理视为可独立评价的 thought，在树上生成多个候选，使用语言模型 value 函数选择 BFS/DFS frontier，并允许 lookahead 和 backtracking。 value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。本页实现 thought 单元的分支扩展、BFS beam 选择、value evaluation 与回溯，不是单条 Chain-of-Thought。实现 thought tree、BFS、value pruning 和回溯；value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。  推理搜索 Agent 规划与搜索：下一步该做什么 ToT 为什么适合需要试探、发现死路再回退的推理任务？ 这类任务的局部选择会影响后续可行性，一次从头写到底容易把错误决定带到结尾。ToT 将过程表示成可继续展开的中间状态，允许保留多个方向、判断进展和回退；前提是中间状态确实可评价，搜索本身不会自动提供可靠的判断标准。 教学例：算式拼到一半已无法得到目标数时，可以换前一步的组合，而不必把整道题的完整解释再生成一遍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-tree-of-thoughts-32a1f51e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0e3e4144da090e88">ToT 为什么适合需要试探、发现死路再回退的推理任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atree-of-thoughts">Tree of Thoughts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这类任务的局部选择会影响后续可行性，一次从头写到底容易把错误决定带到结尾。ToT 将过程表示成可继续展开的中间状态，允许保留多个方向、判断进展和回退；前提是中间状态确实可评价，搜索本身不会自动提供可靠的判断标准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：算式拼到一半已无法得到目标数时，可以换前一步的组合，而不必把整道题的完整解释再生成一遍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10601">原论文</a> · <a href="../../../../agent-research/2305.10601-tree-of-thoughts/">实现解读</a> · <a href="#qa-0e3e4144da090e88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tree-of-thoughts" data-paper-title="Tree of Thoughts" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Tree of Thoughts Agent Princeton University 2023-05-17 自回归生成和单条 CoT 很难撤销早期错误。ToT 将中间推理视为可独立评价的 thought，在树上生成多个候选，使用语言模型 value 函数选择 BFS/DFS frontier，并允许 lookahead 和 backtracking。 value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。本页实现 thought 单元的分支扩展、BFS beam 选择、value evaluation 与回溯，不是单条 Chain-of-Thought。实现 thought tree、BFS、value pruning 和回溯；value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。  推理搜索 Agent 规划与搜索：下一步该做什么 把推理切成 thought 再做树搜索，与一次生成多条完整答案有什么不同？ 中间 thought 是可单独评价和扩展的状态，可以在早期保留多种方向、剪去死路并回退。多条完整答案则常在终点才比较，重复支付错误前缀的成本；ToT 的收益仍受价值估计和搜索宽深预算限制，树结构本身不保证评价正确。 例如算术题第一步有三种分解，先检验哪种保留可行余量再扩展，能避免把明显不可能的分解一路写到完整答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tree-of-thoughts" data-paper-title="Tree of Thoughts" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Tree of Thoughts Agent Princeton University 2023-05-17 自回归生成和单条 CoT 很难撤销早期错误。ToT 将中间推理视为可独立评价的 thought，在树上生成多个候选，使用语言模型 value 函数选择 BFS/DFS frontier，并允许 lookahead 和 backtracking。 value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。本页实现 thought 单元的分支扩展、BFS beam 选择、value evaluation 与回溯，不是单条 Chain-of-Thought。实现 thought tree、BFS、value pruning 和回溯；value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。  推理搜索 Agent 规划与搜索：下一步该做什么 ToT 的 BFS 与 DFS 各怎样安排有限的搜索预算？ BFS 同时维护一层的多个状态，便于在相近进度上比较方向，但需要保存并评价较宽前沿；DFS 先沿一条路径深入，遇到不合适状态再回退，前沿较窄却可能在坏分支耗费深度。选择宽度、深度和剪枝阈值时，仍要考虑具体任务的评价可靠性。 教学例：有三种开局，BFS 各走一步后比较；DFS 可能先把第一种走到尽头，再决定是否回头试第二种。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f19cba5da4346653">ToT 的 BFS 与 DFS 各怎样安排有限的搜索预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atree-of-thoughts">Tree of Thoughts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>BFS 同时维护一层的多个状态，便于在相近进度上比较方向，但需要保存并评价较宽前沿；DFS 先沿一条路径深入，遇到不合适状态再回退，前沿较窄却可能在坏分支耗费深度。选择宽度、深度和剪枝阈值时，仍要考虑具体任务的评价可靠性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：有三种开局，BFS 各走一步后比较；DFS 可能先把第一种走到尽头，再决定是否回头试第二种。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10601">原论文</a> · <a href="../../../../agent-research/2305.10601-tree-of-thoughts/">实现解读</a> · <a href="#qa-f19cba5da4346653">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tree-of-thoughts" data-paper-title="Tree of Thoughts" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="Tree of Thoughts Agent Princeton University 2023-05-17 自回归生成和单条 CoT 很难撤销早期错误。ToT 将中间推理视为可独立评价的 thought，在树上生成多个候选，使用语言模型 value 函数选择 BFS/DFS frontier，并允许 lookahead 和 backtracking。 value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。本页实现 thought 单元的分支扩展、BFS beam 选择、value evaluation 与回溯，不是单条 Chain-of-Thought。实现 thought tree、BFS、value pruning 和回溯；value 是确定性 workflow coherence，未调用 GPT-4 自评，也未运行 Game of 24，因此 1.0 只验证搜索机制。  推理搜索 Agent 规划与搜索：下一步该做什么 本地 workflow coherence value 能代表 GPT-4 自评质量吗？ 不能。本地在小型 PlanBench 上用确定性 workflow coherence、固定 beam 与回溯检查 thought tree 控制流，未调用 GPT-4 或运行 Game of 24。节点数和回溯次数可说明搜索实际发生，满分不代表语言价值函数已学会判断开放推理。 例如规则可判某动作顺序违反前提，却不能证明大模型能给创意写作片段打出同样可靠的未来价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2f4d0f638f26d58e">本地 workflow coherence value 能代表 GPT-4 自评质量吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atree-of-thoughts">Tree of Thoughts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地在小型 PlanBench 上用确定性 workflow coherence、固定 beam 与回溯检查 thought tree 控制流，未调用 GPT-4 或运行 Game of 24。节点数和回溯次数可说明搜索实际发生，满分不代表语言价值函数已学会判断开放推理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规则可判某动作顺序违反前提，却不能证明大模型能给创意写作片段打出同样可靠的未来价值。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10601">原论文</a> · <a href="../../../../agent-research/2305.10601-tree-of-thoughts/">实现解读</a> · <a href="#qa-2f4d0f638f26d58e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:react" data-paper-title="ReAct" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReAct Agent Princeton University 2022-10-06 纯 CoT 容易在封闭知识上幻觉，纯 action agent 又缺少计划与状态跟踪。ReAct 让模型交替生成自然语言推理和环境 action，再把 observation 放回下一步上下文，使推理可以纠错、行动可以获取外部事实。 本页实现 Thought → Action → Observation 的交替循环，并记录实际 reasoning/action 次数；不是把直接返回答案包装成 ReAct。保留交替 trace 和工具动作计数，但 observation 来自确定性 mini-suite；未调用 Wikipedia、WebShop 或付费 LLM，因此本地 1.0 只说明执行循环正确，不能对标论文。ScaleMCP mini 固定 120 episodes、seed 42；每个 required tool 前执行一次 reasoning，随后记录 action/observation。  推理与行动 Agent 规划与搜索：下一步该做什么 ReAct 为什么把回答问题和与外部世界交互放在同一个循环里？ 仅凭模型内部知识，Agent 可能缺少最新事实，也无法知道动作是否真的成功。ReAct 让模型一边推理一边调用工具或环境，并把返回结果用于后续决定，适用于信息获取与行动交织的任务。真实观察增加纠错机会，但工具错误和错误解释观察仍可能导致失败。 教学例：查某商品是否有货，Agent 先查询库存，再根据返回结果决定继续下单还是找替代品，不能只凭常识猜库存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<span id="paper-agent-research-react-96535df9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-546c38878e07ca4b">ReAct 为什么把回答问题和与外部世界交互放在同一个循环里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Areact">ReAct</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅凭模型内部知识，Agent 可能缺少最新事实，也无法知道动作是否真的成功。ReAct 让模型一边推理一边调用工具或环境，并把返回结果用于后续决定，适用于信息获取与行动交织的任务。真实观察增加纠错机会，但工具错误和错误解释观察仍可能导致失败。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：查某商品是否有货，Agent 先查询库存，再根据返回结果决定继续下单还是找替代品，不能只凭常识猜库存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2210.03629">原论文</a> · <a href="../../../../agent-research/2210.03629-react/">实现解读</a> · <a href="#qa-546c38878e07ca4b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:react" data-paper-title="ReAct" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReAct Agent Princeton University 2022-10-06 纯 CoT 容易在封闭知识上幻觉，纯 action agent 又缺少计划与状态跟踪。ReAct 让模型交替生成自然语言推理和环境 action，再把 observation 放回下一步上下文，使推理可以纠错、行动可以获取外部事实。 本页实现 Thought → Action → Observation 的交替循环，并记录实际 reasoning/action 次数；不是把直接返回答案包装成 ReAct。保留交替 trace 和工具动作计数，但 observation 来自确定性 mini-suite；未调用 Wikipedia、WebShop 或付费 LLM，因此本地 1.0 只说明执行循环正确，不能对标论文。ScaleMCP mini 固定 120 episodes、seed 42；每个 required tool 前执行一次 reasoning，随后记录 action/observation。  推理与行动 Agent 规划与搜索：下一步该做什么 为什么 observation 必须回到下一轮上下文，而不能让模型只继续自己的 reasoning？ 动作的意义在于获得真实外部反馈，下一轮据此修正信念与计划。若只沿原推理续写，模型可能把预期当成实际结果，失去行动与认知的闭环；ReAct 的关键是推理、可执行动作和观察交替，不是单纯在文本里写出几个工具名称。 例如模型猜文件存在后执行读取，工具实际返回不存在；下一步应改变搜索路径，而非沿“文件已读到”的想象继续分析。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:react" data-paper-title="ReAct" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReAct Agent Princeton University 2022-10-06 纯 CoT 容易在封闭知识上幻觉，纯 action agent 又缺少计划与状态跟踪。ReAct 让模型交替生成自然语言推理和环境 action，再把 observation 放回下一步上下文，使推理可以纠错、行动可以获取外部事实。 本页实现 Thought → Action → Observation 的交替循环，并记录实际 reasoning/action 次数；不是把直接返回答案包装成 ReAct。保留交替 trace 和工具动作计数，但 observation 来自确定性 mini-suite；未调用 Wikipedia、WebShop 或付费 LLM，因此本地 1.0 只说明执行循环正确，不能对标论文。ScaleMCP mini 固定 120 episodes、seed 42；每个 required tool 前执行一次 reasoning，随后记录 action/observation。  推理与行动 Agent 规划与搜索：下一步该做什么 ReAct 与纯 CoT 在错误暴露的时机上有什么差别？ 纯 CoT 可一直在内部假设上推演，错误未必接触外部事实；ReAct 通过行动获得观察，可在途中修正计划。外部反馈也可能不完整或工具失败，因此交替结构不保证事实正确，仍要核对工具结果和最终支持关系。 例如假设某书作者是甲，检索发现作者为乙后可及时修正；纯内部推演可能继续围绕甲生成更多错误细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9ab5d46e1652d0e4">ReAct 与纯 CoT 在错误暴露的时机上有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Areact">ReAct</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>纯 CoT 可一直在内部假设上推演，错误未必接触外部事实；ReAct 通过行动获得观察，可在途中修正计划。外部反馈也可能不完整或工具失败，因此交替结构不保证事实正确，仍要核对工具结果和最终支持关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如假设某书作者是甲，检索发现作者为乙后可及时修正；纯内部推演可能继续围绕甲生成更多错误细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2210.03629">原论文</a> · <a href="../../../../agent-research/2210.03629-react/">实现解读</a> · <a href="#qa-9ab5d46e1652d0e4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:react" data-paper-title="ReAct" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/planning-and-search" data-search="ReAct Agent Princeton University 2022-10-06 纯 CoT 容易在封闭知识上幻觉，纯 action agent 又缺少计划与状态跟踪。ReAct 让模型交替生成自然语言推理和环境 action，再把 observation 放回下一步上下文，使推理可以纠错、行动可以获取外部事实。 本页实现 Thought → Action → Observation 的交替循环，并记录实际 reasoning/action 次数；不是把直接返回答案包装成 ReAct。保留交替 trace 和工具动作计数，但 observation 来自确定性 mini-suite；未调用 Wikipedia、WebShop 或付费 LLM，因此本地 1.0 只说明执行循环正确，不能对标论文。ScaleMCP mini 固定 120 episodes、seed 42；每个 required tool 前执行一次 reasoning，随后记录 action/observation。  推理与行动 Agent 规划与搜索：下一步该做什么 ReAct 的训练或评估为何要区分生成 token 与环境 token？ 工具观察是外部提供的状态，不是策略选择的动作，不能把它们当作模型生成能力或策略梯度目标。当前本地确定性 suite 只验证循环与计数，另有隔离能力协议也需保持 policy 不读 reference；两种证据范围不能因方法相同就混合。 例如工具返回一百个词不应算成策略成功生成的一百个词，更不能把其中隐藏答案写入可见 reference 字段帮助决策。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 规划与搜索：下一步该做什么</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c090c3330236ebe6">ReAct 的训练或评估为何要区分生成 token 与环境 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Areact">ReAct</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具观察是外部提供的状态，不是策略选择的动作，不能把它们当作模型生成能力或策略梯度目标。当前本地确定性 suite 只验证循环与计数，另有隔离能力协议也需保持 policy 不读 reference；两种证据范围不能因方法相同就混合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具返回一百个词不应算成策略成功生成的一百个词，更不能把其中隐藏答案写入可见 reference 字段帮助决策。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2210.03629">原论文</a> · <a href="../../../../agent-research/2210.03629-react/">实现解读</a> · <a href="#qa-c090c3330236ebe6">问题链接</a></p>
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
