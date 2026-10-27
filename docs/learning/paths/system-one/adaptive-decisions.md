---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 按需决策：选择性推理、迁移与持续反馈

[结构化决策](index.md) / 16 个问题 · 4 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

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
<p class="ar-learning-status" data-learning-status role="status">16 个问题 · 4 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-dlc" data-paper-title="Jev-DLC: Decision-Level Continual Learning from Typed Feedback" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Jev-DLC: Decision-Level Continual Learning from Typed Feedback 基础模型 The Hong Kong University of Science and Technology (Guangzhou) 2026-10-22 类型化决策能给出明确 accept 或 revoke(旧选择→新选择)。Jev-DLC 不把完整历史重新塞进模型，而是在冻结 scorer 上维护两个紧凑通道：保守通道记住重复动作的语义计数与局部方向；响应通道只存当前修正方向。反馈只能影响之后的请求，不能先看当前正确答案再报成功。 成本过高，不复现（审查 DONE）；三种子指标仅验证独立PA-I最小化参考、双通道/几何混合、反馈时序、硬掩码、revision和reset；外部给定随机logits/表示，不加载JEV、不生成任务答案。没有把1.0契约通过率标为模型准确率，也不根据合成反馈宣称能力提升。纯CPU路径无需CUDA回执。  System One / JEV 类型反馈与持续适配 结构化决策 按需决策：选择性推理、迁移与持续反馈 Jev-DLC持续适配时需要保存整段交互历史吗？ 方法在冻结评分器上保留两个紧凑状态：保守通道的语义计数与方向，以及响应通道的当前修正方向。历史反馈被压入状态，不是把所有旧对话不断塞回上下文。 例如用户反复纠正同类路由，系统更新计数和方向，而不无限拼接所有旧工单。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<span id="paper-foundation-models-jev-dlc-8eed7f0b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-58e39b989e85825c">Jev-DLC持续适配时需要保存整段交互历史吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-dlc">Jev-DLC: Decision-Level Continual Learning from Typed Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>方法在冻结评分器上保留两个紧凑状态：保守通道的语义计数与方向，以及响应通道的当前修正方向。历史反馈被压入状态，不是把所有旧对话不断塞回上下文。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户反复纠正同类路由，系统更新计数和方向，而不无限拼接所有旧工单。</p>
<p class="ar-learning-sources">依据：背景与主要改动、双通道、PA-I与可靠性；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31521v1">原论文</a> · <a href="../../../../system-one/2610.31521-jev-dlc/">实现解读</a> · <a href="#qa-58e39b989e85825c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-dlc" data-paper-title="Jev-DLC: Decision-Level Continual Learning from Typed Feedback" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Jev-DLC: Decision-Level Continual Learning from Typed Feedback 基础模型 The Hong Kong University of Science and Technology (Guangzhou) 2026-10-22 类型化决策能给出明确 accept 或 revoke(旧选择→新选择)。Jev-DLC 不把完整历史重新塞进模型，而是在冻结 scorer 上维护两个紧凑通道：保守通道记住重复动作的语义计数与局部方向；响应通道只存当前修正方向。反馈只能影响之后的请求，不能先看当前正确答案再报成功。 成本过高，不复现（审查 DONE）；三种子指标仅验证独立PA-I最小化参考、双通道/几何混合、反馈时序、硬掩码、revision和reset；外部给定随机logits/表示，不加载JEV、不生成任务答案。没有把1.0契约通过率标为模型准确率，也不根据合成反馈宣称能力提升。纯CPU路径无需CUDA回执。  System One / JEV 类型反馈与持续适配 结构化决策 按需决策：选择性推理、迁移与持续反馈 Jev-DLC为什么用更新前的通道预测评估可靠性，并只让反馈影响之后请求？ 可靠性应衡量通道在看见反馈前的决策，否则修正后再评分会把学习信息当成预测能力。保守通道积累重复语义经验，响应通道跟踪当前修正，二者通过可靠性混合。反馈只能对应已提交决策，不能伪造重放；冻结评分器上的持续状态也不能读取当前金标再预测。 例如用户撤销一次工具选择后，系统才能更新两个通道并处理下一次请求；不能先用这次正确工具修正状态，再回填为本次成功预测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-06eefc2e388ae998">Jev-DLC为什么用更新前的通道预测评估可靠性，并只让反馈影响之后请求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-dlc">Jev-DLC: Decision-Level Continual Learning from Typed Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可靠性应衡量通道在看见反馈前的决策，否则修正后再评分会把学习信息当成预测能力。保守通道积累重复语义经验，响应通道跟踪当前修正，二者通过可靠性混合。反馈只能对应已提交决策，不能伪造重放；冻结评分器上的持续状态也不能读取当前金标再预测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户撤销一次工具选择后，系统才能更新两个通道并处理下一次请求；不能先用这次正确工具修正状态，再回填为本次成功预测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、双通道、PA-I与可靠性；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31521v1">原论文</a> · <a href="../../../../system-one/2610.31521-jev-dlc/">实现解读</a> · <a href="#qa-06eefc2e388ae998">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-dlc" data-paper-title="Jev-DLC: Decision-Level Continual Learning from Typed Feedback" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Jev-DLC: Decision-Level Continual Learning from Typed Feedback 基础模型 The Hong Kong University of Science and Technology (Guangzhou) 2026-10-22 类型化决策能给出明确 accept 或 revoke(旧选择→新选择)。Jev-DLC 不把完整历史重新塞进模型，而是在冻结 scorer 上维护两个紧凑通道：保守通道记住重复动作的语义计数与局部方向；响应通道只存当前修正方向。反馈只能影响之后的请求，不能先看当前正确答案再报成功。 成本过高，不复现（审查 DONE）；三种子指标仅验证独立PA-I最小化参考、双通道/几何混合、反馈时序、硬掩码、revision和reset；外部给定随机logits/表示，不加载JEV、不生成任务答案。没有把1.0契约通过率标为模型准确率，也不根据合成反馈宣称能力提升。纯CPU路径无需CUDA回执。  System One / JEV 类型反馈与持续适配 结构化决策 按需决策：选择性推理、迁移与持续反馈 Jev-DLC保守通道与响应通道为什么要分开？ 前者积累重复行为形成稳定先验，后者较快响应当前修正；可靠性混合允许二者在稳定与变化环境中有不同影响。单一状态难以同时表达长期习惯和近期转向。 例如用户长期偏好A但近期临时改用B，两通道可分别保留长期与即时信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d6fc3fb543805f86">Jev-DLC保守通道与响应通道为什么要分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-dlc">Jev-DLC: Decision-Level Continual Learning from Typed Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者积累重复行为形成稳定先验，后者较快响应当前修正；可靠性混合允许二者在稳定与变化环境中有不同影响。单一状态难以同时表达长期习惯和近期转向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户长期偏好A但近期临时改用B，两通道可分别保留长期与即时信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、双通道、PA-I与可靠性；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31521v1">原论文</a> · <a href="../../../../system-one/2610.31521-jev-dlc/">实现解读</a> · <a href="#qa-d6fc3fb543805f86">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-dlc" data-paper-title="Jev-DLC: Decision-Level Continual Learning from Typed Feedback" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Jev-DLC: Decision-Level Continual Learning from Typed Feedback 基础模型 The Hong Kong University of Science and Technology (Guangzhou) 2026-10-22 类型化决策能给出明确 accept 或 revoke(旧选择→新选择)。Jev-DLC 不把完整历史重新塞进模型，而是在冻结 scorer 上维护两个紧凑通道：保守通道记住重复动作的语义计数与局部方向；响应通道只存当前修正方向。反馈只能影响之后的请求，不能先看当前正确答案再报成功。 成本过高，不复现（审查 DONE）；三种子指标仅验证独立PA-I最小化参考、双通道/几何混合、反馈时序、硬掩码、revision和reset；外部给定随机logits/表示，不加载JEV、不生成任务答案。没有把1.0契约通过率标为模型准确率，也不根据合成反馈宣称能力提升。纯CPU路径无需CUDA回执。  System One / JEV 类型反馈与持续适配 结构化决策 按需决策：选择性推理、迁移与持续反馈 Jev-DLC为何拒绝伪造、重放或过期Decision的反馈？ 反馈必须针对当前实例已提交的选择，否则可把任意目标注入状态或重复累积同一经验。更新完成后释放当前公开缓存，硬安全掩码不能被适配状态覆盖。 例如同一次撤回事件发送两遍，不能让系统把它当两次独立用户纠正。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cfa09967908de8b9">Jev-DLC为何拒绝伪造、重放或过期Decision的反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-dlc">Jev-DLC: Decision-Level Continual Learning from Typed Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反馈必须针对当前实例已提交的选择，否则可把任意目标注入状态或重复累积同一经验。更新完成后释放当前公开缓存，硬安全掩码不能被适配状态覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一次撤回事件发送两遍，不能让系统把它当两次独立用户纠正。</p>
<p class="ar-learning-sources">依据：背景与主要改动、双通道、PA-I与可靠性；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31521v1">原论文</a> · <a href="../../../../system-one/2610.31521-jev-dlc/">实现解读</a> · <a href="#qa-cfa09967908de8b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:selective-reasoning" data-paper-title="Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop 基础模型 University of Electronic Science and Technology of China 2026-10-14 Typed decision model 从明确候选中返回选择，适合 JEV / System One 式判断，但直接读出不一定足以完成多步推理。始终生成很长的推理又浪费算力。本论文在冻结 Qwen3.5-4B 上拟合共享 candidate-answer reader，让空推理前缀和中间推理前缀都能返回候选分布。控制器将三个问题分开：benefit gate 决定是否启动推理；从自然生成状态出发的 trigger 决定何时发起显式答案读取；归一化熵阈值决定是否接受当前候选并取消后续生成。 完整在线多策略实验为成本过高，不复现（审查 DONE）。本地完成的是固定原作者测量的 CPU 统计复核与不读取 gold 的控制器接口，不是 Qwen3.5-4B 在线能力复现。公开包不含原始 token trace / feature cache，不能据复算通过声称核实了 exact-prefix 关系。完整在线多策略实验为成本过高，不复现（审查 DONE）。本地对照口径：重算原作者公开 records.csv，以同题 / 同组配对、dataset / ProofWriter subtype 分层的 bootstrap 复核均值、差值、比值及pointwise区间。  System One / JEV 自适应推理与提前退出 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 Selective Reasoning为什么不让所有题都生成同样长的推理？ 有些有限候选任务直接读出已足够，另一些需要额外步骤；按预期收益启动推理，并在中间读取答案，可把计算分配给仍需要它的题，而非固定长度。 例如简单意图选择直接返回，多步算术才进入推理，并在足够确定时结束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<span id="paper-foundation-models-selective-reasoning-8fcddd3e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-201239c10b97ba7e">Selective Reasoning为什么不让所有题都生成同样长的推理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aselective-reasoning">Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有些有限候选任务直接读出已足够，另一些需要额外步骤；按预期收益启动推理，并在中间读取答案，可把计算分配给仍需要它的题，而非固定长度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如简单意图选择直接返回，多步算术才进入推理，并在足够确定时结束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19644">原论文</a> · <a href="../../../../system-one/2610.19644-selective-reasoning/">实现解读</a> · <a href="#qa-201239c10b97ba7e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:selective-reasoning" data-paper-title="Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop 基础模型 University of Electronic Science and Technology of China 2026-10-14 Typed decision model 从明确候选中返回选择，适合 JEV / System One 式判断，但直接读出不一定足以完成多步推理。始终生成很长的推理又浪费算力。本论文在冻结 Qwen3.5-4B 上拟合共享 candidate-answer reader，让空推理前缀和中间推理前缀都能返回候选分布。控制器将三个问题分开：benefit gate 决定是否启动推理；从自然生成状态出发的 trigger 决定何时发起显式答案读取；归一化熵阈值决定是否接受当前候选并取消后续生成。 完整在线多策略实验为成本过高，不复现（审查 DONE）。本地完成的是固定原作者测量的 CPU 统计复核与不读取 gold 的控制器接口，不是 Qwen3.5-4B 在线能力复现。公开包不含原始 token trace / feature cache，不能据复算通过声称核实了 exact-prefix 关系。完整在线多策略实验为成本过高，不复现（审查 DONE）。本地对照口径：重算原作者公开 records.csv，以同题 / 同组配对、dataset / ProofWriter subtype 分层的 bootstrap 复核均值、差值、比值及pointwise区间。  System One / JEV 自适应推理与提前退出 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 Selective Reasoning为什么区分启动推理、触发读取与接受答案，而不能只写一个置信阈值？ 启动门判断推理是否值得，触发器决定何时从自然生成前缀发起答案读取，读取后的归一化熵才决定是否接受并取消后续生成。三者作用在不同状态。预算耗尽的强制返回必须单独标记，不能算阈值成功早停；控制器拟合也不能使用评测金标。 例如模型值得推理但暂未到可读状态时继续生成；读取后仍不确定就再推理，直到预算结束也不确定时应标强制返回而非自信停止。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4819b57ce6202fe0">Selective Reasoning为什么区分启动推理、触发读取与接受答案，而不能只写一个置信阈值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aselective-reasoning">Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>启动门判断推理是否值得，触发器决定何时从自然生成前缀发起答案读取，读取后的归一化熵才决定是否接受并取消后续生成。三者作用在不同状态。预算耗尽的强制返回必须单独标记，不能算阈值成功早停；控制器拟合也不能使用评测金标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型值得推理但暂未到可读状态时继续生成；读取后仍不确定就再推理，直到预算结束也不确定时应标强制返回而非自信停止。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19644">原论文</a> · <a href="../../../../system-one/2610.19644-selective-reasoning/">实现解读</a> · <a href="#qa-4819b57ce6202fe0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:selective-reasoning" data-paper-title="Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop 基础模型 University of Electronic Science and Technology of China 2026-10-14 Typed decision model 从明确候选中返回选择，适合 JEV / System One 式判断，但直接读出不一定足以完成多步推理。始终生成很长的推理又浪费算力。本论文在冻结 Qwen3.5-4B 上拟合共享 candidate-answer reader，让空推理前缀和中间推理前缀都能返回候选分布。控制器将三个问题分开：benefit gate 决定是否启动推理；从自然生成状态出发的 trigger 决定何时发起显式答案读取；归一化熵阈值决定是否接受当前候选并取消后续生成。 完整在线多策略实验为成本过高，不复现（审查 DONE）。本地完成的是固定原作者测量的 CPU 统计复核与不读取 gold 的控制器接口，不是 Qwen3.5-4B 在线能力复现。公开包不含原始 token trace / feature cache，不能据复算通过声称核实了 exact-prefix 关系。完整在线多策略实验为成本过高，不复现（审查 DONE）。本地对照口径：重算原作者公开 records.csv，以同题 / 同组配对、dataset / ProofWriter subtype 分层的 bootstrap 复核均值、差值、比值及pointwise区间。  System One / JEV 自适应推理与提前退出 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 按自然生成状态读取与每隔固定词元盲读有何差别？ 自然状态触发器尝试在更适合显式答案读取的位置发起查询，间隔控制只限制频率。读取是否可靠还由共享reader与熵判定决定，触发不等于已经有正确答案。 例如刚完成一个推导小结时可能比算式写到一半更适合读取，但仍需检查候选分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9efe14ad02e454e6">按自然生成状态读取与每隔固定词元盲读有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aselective-reasoning">Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自然状态触发器尝试在更适合显式答案读取的位置发起查询，间隔控制只限制频率。读取是否可靠还由共享reader与熵判定决定，触发不等于已经有正确答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如刚完成一个推导小结时可能比算式写到一半更适合读取，但仍需检查候选分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19644">原论文</a> · <a href="../../../../system-one/2610.19644-selective-reasoning/">实现解读</a> · <a href="#qa-9efe14ad02e454e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:selective-reasoning" data-paper-title="Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop 基础模型 University of Electronic Science and Technology of China 2026-10-14 Typed decision model 从明确候选中返回选择，适合 JEV / System One 式判断，但直接读出不一定足以完成多步推理。始终生成很长的推理又浪费算力。本论文在冻结 Qwen3.5-4B 上拟合共享 candidate-answer reader，让空推理前缀和中间推理前缀都能返回候选分布。控制器将三个问题分开：benefit gate 决定是否启动推理；从自然生成状态出发的 trigger 决定何时发起显式答案读取；归一化熵阈值决定是否接受当前候选并取消后续生成。 完整在线多策略实验为成本过高，不复现（审查 DONE）。本地完成的是固定原作者测量的 CPU 统计复核与不读取 gold 的控制器接口，不是 Qwen3.5-4B 在线能力复现。公开包不含原始 token trace / feature cache，不能据复算通过声称核实了 exact-prefix 关系。完整在线多策略实验为成本过高，不复现（审查 DONE）。本地对照口径：重算原作者公开 records.csv，以同题 / 同组配对、dataset / ProofWriter subtype 分层的 bootstrap 复核均值、差值、比值及pointwise区间。  System One / JEV 自适应推理与提前退出 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 候选数变化时为什么用H除以logK来算certainty？ 不同候选数的最大熵不同，归一化后确定度阈值才有可比意义。仍需区分取消生成与预算耗尽，门控的标准化统计及权重在评测前冻结，不能用测试反馈重拟合。 例如四选一与十选一原始熵量级不同，直接使用相同原始熵阈值会改变停止标准。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-70fdfa05895d5b96">候选数变化时为什么用H除以logK来算certainty？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aselective-reasoning">Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同候选数的最大熵不同，归一化后确定度阈值才有可比意义。仍需区分取消生成与预算耗尽，门控的标准化统计及权重在评测前冻结，不能用测试反馈重拟合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四选一与十选一原始熵量级不同，直接使用相同原始熵阈值会改变停止标准。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19644">原论文</a> · <a href="../../../../system-one/2610.19644-selective-reasoning/">实现解读</a> · <a href="#qa-70fdfa05895d5b96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-regional-transfer" data-paper-title="Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages 基础模型 Universitas Budi Luhur 2026-10-09 “输出概率校准良好”不等于“能可靠排序自己的错误”。本文在 NusaX 的 12 种语言和 NusaTranslation 的 7 种平行语言上，分别研究准确率、校准、错误排序、翻译和所需人工标签量。英语/印尼语和区域语言共享句子 ID，因此跨语言比较需要以句子为聚类单位，而不是把语言版本当独立样本。方法是先让低成本决策模型回答所有样本，再把低置信度的一部分交给本地分类器或 LLM。原作者以验证集宏 F1 选择最小路由比例，再冻结该比例评测测试集；不是在测试结果中挑最优点。本文不提出新的模型架构。 本地提供公开预测复算、15 等宽右闭区间 ECE、Brier、NLL、作者稳定排序 AURC、额外的置信度 tie-grouped AURC，以及按验证集宏 F1 选比例的级联。两个 AURC 的 tie 规则不同，因此名称分开。固定预测标签可能与公开四舍五入概率的 argmax 不一致；保留标签计算准确率，另报概率 argmax 准确率与不一致数量，校准/风险覆盖按作者概率 argmax 口径。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 区域语言研究为什么同时报告准确率、校准与风险覆盖？ 准确率描述整体命中，校准描述概率与频率是否一致，风险覆盖描述按置信筛选是否能留下更可靠样本。三个维度不同，共同决定是否适合低成本模型与强后端级联。 例如总体准确率相同的两个模型，低置信样本能否集中错误可能差很多。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<span id="paper-foundation-models-jev-regional-transfer-a226a6c0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-135330e6b4948bc8">区域语言研究为什么同时报告准确率、校准与风险覆盖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-regional-transfer">Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Universitas Budi Luhur</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>准确率描述整体命中，校准描述概率与频率是否一致，风险覆盖描述按置信筛选是否能留下更可靠样本。三个维度不同，共同决定是否适合低成本模型与强后端级联。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如总体准确率相同的两个模型，低置信样本能否集中错误可能差很多。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14112">原论文</a> · <a href="../../../../system-one/2610.14112-regional-transfer/">实现解读</a> · <a href="#qa-135330e6b4948bc8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-regional-transfer" data-paper-title="Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages 基础模型 Universitas Budi Luhur 2026-10-09 “输出概率校准良好”不等于“能可靠排序自己的错误”。本文在 NusaX 的 12 种语言和 NusaTranslation 的 7 种平行语言上，分别研究准确率、校准、错误排序、翻译和所需人工标签量。英语/印尼语和区域语言共享句子 ID，因此跨语言比较需要以句子为聚类单位，而不是把语言版本当独立样本。方法是先让低成本决策模型回答所有样本，再把低置信度的一部分交给本地分类器或 LLM。原作者以验证集宏 F1 选择最小路由比例，再冻结该比例评测测试集；不是在测试结果中挑最优点。本文不提出新的模型架构。 本地提供公开预测复算、15 等宽右闭区间 ECE、Brier、NLL、作者稳定排序 AURC、额外的置信度 tie-grouped AURC，以及按验证集宏 F1 选比例的级联。两个 AURC 的 tie 规则不同，因此名称分开。固定预测标签可能与公开四舍五入概率的 argmax 不一致；保留标签计算准确率，另报概率 argmax 准确率与不一致数量，校准/风险覆盖按作者概率 argmax 口径。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 校准良好的模型为什么仍可能不适合按低置信度路由错误样本？ 校准检验概率与总体正确频率是否匹配，路由则要求错误比正确样本更常出现在低置信区，两种性质并不等价。级联比例应在验证宏F1上选定并冻结，再用测试集评估；平行语言共享句子身份，统计比较需按句子聚类，不能当作独立重复样本。 例如两组样本的平均置信与准确率吻合，但错题分散在各个置信区；此时总体校准不错，挑最低置信部分交给强模型却未必省成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bb07aec9629be972">校准良好的模型为什么仍可能不适合按低置信度路由错误样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-regional-transfer">Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Universitas Budi Luhur</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>校准检验概率与总体正确频率是否匹配，路由则要求错误比正确样本更常出现在低置信区，两种性质并不等价。级联比例应在验证宏F1上选定并冻结，再用测试集评估；平行语言共享句子身份，统计比较需按句子聚类，不能当作独立重复样本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两组样本的平均置信与准确率吻合，但错题分散在各个置信区；此时总体校准不错，挑最低置信部分交给强模型却未必省成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14112">原论文</a> · <a href="../../../../system-one/2610.14112-regional-transfer/">实现解读</a> · <a href="#qa-bb07aec9629be972">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-regional-transfer" data-paper-title="Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages 基础模型 Universitas Budi Luhur 2026-10-09 “输出概率校准良好”不等于“能可靠排序自己的错误”。本文在 NusaX 的 12 种语言和 NusaTranslation 的 7 种平行语言上，分别研究准确率、校准、错误排序、翻译和所需人工标签量。英语/印尼语和区域语言共享句子 ID，因此跨语言比较需要以句子为聚类单位，而不是把语言版本当独立样本。方法是先让低成本决策模型回答所有样本，再把低置信度的一部分交给本地分类器或 LLM。原作者以验证集宏 F1 选择最小路由比例，再冻结该比例评测测试集；不是在测试结果中挑最优点。本文不提出新的模型架构。 本地提供公开预测复算、15 等宽右闭区间 ECE、Brier、NLL、作者稳定排序 AURC、额外的置信度 tie-grouped AURC，以及按验证集宏 F1 选比例的级联。两个 AURC 的 tie 规则不同，因此名称分开。固定预测标签可能与公开四舍五入概率的 argmax 不一致；保留标签计算准确率，另报概率 argmax 准确率与不一致数量，校准/风险覆盖按作者概率 argmax 口径。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 区域语言级联把低置信样本交给后端，与先翻译所有样本再判断有什么不同？ 级联按低成本模型的置信度选择一部分样本追加处理，翻译中转则先改变输入语言条件。二者改变的轴分别是计算分配和语言表示，不能把翻译收益直接解释成路由器找错能力。路由比例还必须在验证集选定后冻结。 教学例子：只将难例交强后端，未必翻译文本；把全部区域语言句子翻成印尼语，则对易例也改变了输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-447b34f6708c8cbe">区域语言级联把低置信样本交给后端，与先翻译所有样本再判断有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-regional-transfer">Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Universitas Budi Luhur</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>级联按低成本模型的置信度选择一部分样本追加处理，翻译中转则先改变输入语言条件。二者改变的轴分别是计算分配和语言表示，不能把翻译收益直接解释成路由器找错能力。路由比例还必须在验证集选定后冻结。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只将难例交强后端，未必翻译文本；把全部区域语言句子翻成印尼语，则对易例也改变了输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14112">原论文</a> · <a href="../../../../system-one/2610.14112-regional-transfer/">实现解读</a> · <a href="#qa-447b34f6708c8cbe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-regional-transfer" data-paper-title="Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages 基础模型 Universitas Budi Luhur 2026-10-09 “输出概率校准良好”不等于“能可靠排序自己的错误”。本文在 NusaX 的 12 种语言和 NusaTranslation 的 7 种平行语言上，分别研究准确率、校准、错误排序、翻译和所需人工标签量。英语/印尼语和区域语言共享句子 ID，因此跨语言比较需要以句子为聚类单位，而不是把语言版本当独立样本。方法是先让低成本决策模型回答所有样本，再把低置信度的一部分交给本地分类器或 LLM。原作者以验证集宏 F1 选择最小路由比例，再冻结该比例评测测试集；不是在测试结果中挑最优点。本文不提出新的模型架构。 本地提供公开预测复算、15 等宽右闭区间 ECE、Brier、NLL、作者稳定排序 AURC、额外的置信度 tie-grouped AURC，以及按验证集宏 F1 选比例的级联。两个 AURC 的 tie 规则不同，因此名称分开。固定预测标签可能与公开四舍五入概率的 argmax 不一致；保留标签计算准确率，另报概率 argmax 准确率与不一致数量，校准/风险覆盖按作者概率 argmax 口径。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 级联比例与本地温度分别允许用什么数据选择？ 都只能在验证预测上选择，比例按规定网格与宏F1规则，温度按验证NLL；冻结后评测测试。温度校准是本地扩展，不能混成作者原始训练步骤。 例如测试发现多转交一些更好，也不能回头改路由比例后继续报同一独立测试分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-460794680805d9e1">级联比例与本地温度分别允许用什么数据选择？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-regional-transfer">Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Universitas Budi Luhur</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>都只能在验证预测上选择，比例按规定网格与宏F1规则，温度按验证NLL；冻结后评测测试。温度校准是本地扩展，不能混成作者原始训练步骤。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试发现多转交一些更好，也不能回头改路由比例后继续报同一独立测试分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14112">原论文</a> · <a href="../../../../system-one/2610.14112-regional-transfer/">实现解读</a> · <a href="#qa-460794680805d9e1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-capability" data-paper-title="Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks 基础模型 Dalian Maritime University 2026-10-08 论文用有限候选选择评估 Jev 的知识、推理和多语言能力。每题只提交问题与候选，运行一次；数学任务表现弱于知识任务。原文中的供应商分数与作者实测并非统一提示协议，本地实现因此分别记录，不混成可比排名。本文是评测研究，不提供新架构或训练目标。 规范化的 13 种 schema、候选排列、标签隔离、文件哈希和引用 / 实测分离已有行为测试。2026-10-10 在 A100 上使用固定 NanoJev checkpoint 对 ARC-Challenge 官方全部 1,172 道 test 题执行一次，327 题正确，准确率 27.90%，Wilson 95% 区间 25.41%–30.54%；没有用测试题训练、选参或重试。数据与 checkpoint revision 见脱敏 GPU 证据。该结果仅对应开放 NanoJev，不是论文闭源 Jev 的 97.6%。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 Jev能力论文为何属于评测而非新架构？ 它在有限候选接口下测知识、推理和多语言表现，贡献在协议与能力边界证据，没有提出新的训练目标。实现评测器不表示已经实现或提升被测模型。 例如把公开题规范成四选一并统计表现，是测量工具，而不是新的推理模块。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<span id="paper-foundation-models-jev-capability-899cdbd2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2a74c52e1db4ea30">Jev能力论文为何属于评测而非新架构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-capability">Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian Maritime University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它在有限候选接口下测知识、推理和多语言表现，贡献在协议与能力边界证据，没有提出新的训练目标。实现评测器不表示已经实现或提升被测模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把公开题规范成四选一并统计表现，是测量工具，而不是新的推理模块。</p>
<p class="ar-learning-sources">依据：背景与主要改动、数据与评测契约；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11978">原论文</a> · <a href="../../../../system-one/2610.11978-jev-capability/">实现解读</a> · <a href="#qa-2a74c52e1db4ea30">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-capability" data-paper-title="Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks 基础模型 Dalian Maritime University 2026-10-08 论文用有限候选选择评估 Jev 的知识、推理和多语言能力。每题只提交问题与候选，运行一次；数学任务表现弱于知识任务。原文中的供应商分数与作者实测并非统一提示协议，本地实现因此分别记录，不混成可比排名。本文是评测研究，不提供新架构或训练目标。 规范化的 13 种 schema、候选排列、标签隔离、文件哈希和引用 / 实测分离已有行为测试。2026-10-10 在 A100 上使用固定 NanoJev checkpoint 对 ARC-Challenge 官方全部 1,172 道 test 题执行一次，327 题正确，准确率 27.90%，Wilson 95% 区间 25.41%–30.54%；没有用测试题训练、选参或重试。数据与 checkpoint revision 见脱敏 GPU 证据。该结果仅对应开放 NanoJev，不是论文闭源 Jev 的 97.6%。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 Jev能力评测为什么不能把供应商分数与本地实测直接拼成统一排名？ 提示、后端和数据协议不一致会让数值差异混入非能力因素。有限候选评测应固定公开问题、候选与一次决策协议，答案只在评分端汇合，同时记录任务语言和缺失覆盖。该论文是能力审计而非新训练算法，某类任务表现也不能外推为所有推理场景。 例如供应商用另一版提示得到数学分数，本地用固定候选接口得到知识分数；两者可以分别记录，不能据不同协议的数字判定模型整体胜负。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bb0935a34d3a1a2c">Jev能力评测为什么不能把供应商分数与本地实测直接拼成统一排名？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-capability">Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian Maritime University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提示、后端和数据协议不一致会让数值差异混入非能力因素。有限候选评测应固定公开问题、候选与一次决策协议，答案只在评分端汇合，同时记录任务语言和缺失覆盖。该论文是能力审计而非新训练算法，某类任务表现也不能外推为所有推理场景。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如供应商用另一版提示得到数学分数，本地用固定候选接口得到知识分数；两者可以分别记录，不能据不同协议的数字判定模型整体胜负。</p>
<p class="ar-learning-sources">依据：背景与主要改动、数据与评测契约；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11978">原论文</a> · <a href="../../../../system-one/2610.11978-jev-capability/">实现解读</a> · <a href="#qa-bb0935a34d3a1a2c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-capability" data-paper-title="Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks 基础模型 Dalian Maritime University 2026-10-08 论文用有限候选选择评估 Jev 的知识、推理和多语言能力。每题只提交问题与候选，运行一次；数学任务表现弱于知识任务。原文中的供应商分数与作者实测并非统一提示协议，本地实现因此分别记录，不混成可比排名。本文是评测研究，不提供新架构或训练目标。 规范化的 13 种 schema、候选排列、标签隔离、文件哈希和引用 / 实测分离已有行为测试。2026-10-10 在 A100 上使用固定 NanoJev checkpoint 对 ARC-Challenge 官方全部 1,172 道 test 题执行一次，327 题正确，准确率 27.90%，Wilson 95% 区间 25.41%–30.54%；没有用测试题训练、选参或重试。数据与 checkpoint revision 见脱敏 GPU 证据。该结果仅对应开放 NanoJev，不是论文闭源 Jev 的 97.6%。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 知识题强与数学题弱能直接推出模型完全没有推理能力吗？ 不能。观察只约束所测任务、提示与候选接口，还可能受语言和数据覆盖影响。应分别报告任务结果与缺失范围，不把一个维度的差异扩成所有场景的断言。 例如某种算术题失败，尚不足以判断工具规划或其他数学形式也全部失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-821d51d1732bfd58">知识题强与数学题弱能直接推出模型完全没有推理能力吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-capability">Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian Maritime University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。观察只约束所测任务、提示与候选接口，还可能受语言和数据覆盖影响。应分别报告任务结果与缺失范围，不把一个维度的差异扩成所有场景的断言。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某种算术题失败，尚不足以判断工具规划或其他数学形式也全部失败。</p>
<p class="ar-learning-sources">依据：背景与主要改动、数据与评测契约；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11978">原论文</a> · <a href="../../../../system-one/2610.11978-jev-capability/">实现解读</a> · <a href="#qa-821d51d1732bfd58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-capability" data-paper-title="Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks 基础模型 Dalian Maritime University 2026-10-08 论文用有限候选选择评估 Jev 的知识、推理和多语言能力。每题只提交问题与候选，运行一次；数学任务表现弱于知识任务。原文中的供应商分数与作者实测并非统一提示协议，本地实现因此分别记录，不混成可比排名。本文是评测研究，不提供新架构或训练目标。 规范化的 13 种 schema、候选排列、标签隔离、文件哈希和引用 / 实测分离已有行为测试。2026-10-10 在 A100 上使用固定 NanoJev checkpoint 对 ARC-Challenge 官方全部 1,172 道 test 题执行一次，327 题正确，准确率 27.90%，Wilson 95% 区间 25.41%–30.54%；没有用测试题训练、选参或重试。数据与 checkpoint revision 见脱敏 GPU 证据。该结果仅对应开放 NanoJev，不是论文闭源 Jev 的 97.6%。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈 Jev能力评测的预测输入为什么只提交问题与候选一次？ 固定一次公开决策可避免用答案或重试策略额外帮助模型。金标在预测后由评分端读取，不同供应商协议的数字分别记录；漏测项也应明示，而非从总体分母悄悄删除。 例如题库记录含答案字段，构造预测请求时必须先剔除，再由另一评分流程核对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7390391cb4bb71f5">Jev能力评测的预测输入为什么只提交问题与候选一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-capability">Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian Maritime University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定一次公开决策可避免用答案或重试策略额外帮助模型。金标在预测后由评分端读取，不同供应商协议的数字分别记录；漏测项也应明示，而非从总体分母悄悄删除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如题库记录含答案字段，构造预测请求时必须先剔除，再由另一评分流程核对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、数据与评测契约；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11978">原论文</a> · <a href="../../../../system-one/2610.11978-jev-capability/">实现解读</a> · <a href="#qa-7390391cb4bb71f5">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

哪些请求值得追加推理，哪些反馈应该影响下一次选择？

## 记住这一点

Selective Reasoning 把是否启动推理、何时读取答案、何时接受并停止分成三个控制动作，以共享 reader 读取空前缀和推理中途的候选分布。Jev-DLC 在冻结 scorer 之上保留有界的动作记忆与修正方向，把 accept/revoke 反馈作用于之后的请求。迁移评测还要检验换语言和标签预算后是否仍成立。

## 一个例子

用户把上次的工具 A 改成 B，可作为后续相似请求的反馈，却不能在收到修正后回头把上次报成成功。另一个难题若需要推理，可中途读取候选分布并按预先确定的停止规则结束；“预算耗尽”应另记，不能冒充有把握的早停。

## 什么时候要小心

低熵只表示模型集中，并不等于答案正确，门控与阈值必须在评测前冻结。反馈序列要保持时间顺序；迁移和持续适配不能用未来标签。当前本地包含原测量统计复算或随机输入上的接口诊断，高成本完整模型链路未复现。

## 先读这几篇

先读 Selective Reasoning 的启动/读取/停止分工，理解单个请求内的预算；再读 Jev-DLC 的有界反馈状态与时间协议，理解请求之间的适配。然后看公共能力与跨语言迁移的边界。

1. [Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop](../../../system-one/2610.19644-selective-reasoning/README.md) · [原论文](https://arxiv.org/abs/2610.19644)
2. [Jev-DLC: Decision-Level Continual Learning from Typed Feedback](../../../system-one/2610.31521-jev-dlc/README.md) · [原论文](https://arxiv.org/abs/2610.31521v1)

## 自测一下

某题得到正确答案反馈后立刻更新并重答，能算持续学习带来的线上成功吗？

??? note "展开参考答案"

    不能。它已观察当前目标，不再是该题独立预测。应先记录本次原始选择和反馈，再只用更新后的状态评价之后尚未揭晓的请求，并与无反馈或固定策略作同序列比较。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
