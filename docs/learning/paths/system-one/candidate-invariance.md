---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 候选不变性：顺序、竞争者与概率校准

[结构化决策](index.md) / 12 个问题 · 3 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/system-one/candidate-invariance.md)

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
<p class="ar-learning-status" data-learning-status role="status">12 个问题 · 3 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-multicorrect" data-paper-title="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models 基础模型 Independent Researcher 2026-10-21 当一个列表有多个正确选项时，模型可能把大部分概率分给其中一个正确项，另一个正确项虽高于所有干扰项，概率仍低于均匀基线。单选 top-1 或“正确项都排在干扰项之前”因此会掩盖完整集合恢复的失败。论文同时分析 JEV、Luna 和 Gemini，避免把所有现象都归因于某一种架构。特别要区分两种输出：一个候选列表内总和约为1的类别份额，以及对每个选项独立询问“是否正确”得到的二元概率。前者不能直接当作后者的校准置信度。 完整三模型、大规模候选列表实验：成本过高，不复现（审查 DONE）。原文的全量阈值曲线是同一数据上的回溯诊断。本地诊断只检查8项评分/隔离契约：排序与集合恢复的差别、低份额正确项计数、固定验证阈值、数据不重叠、拒答处理、公开回调无标签、五拷贝差距参考值、低概率箱排除的重新归一化。三种子不把固定评分夹具变成正式能力比较，不接入 evolve promotion。  System One / JEV 多正确选项与概率校准审计 结构化决策 候选不变性：顺序、竞争者与概率校准 多正确选项任务要求返回一个答案，还是一个完整正确集合？ 目标是恢复所有正确候选组成的集合，集合大小可能超过一。返回一个正确项只满足单选式命中，仍可能漏选；返回所有项也可能误选干扰项。因此先把输出单位从“一个赢家”改成“一个集合”，再理解排序、阈值与exact-set指标。 教学例子：正确集合是{甲,乙}时，仅返回甲不算完整恢复；返回甲乙丙也因多出丙而不满足精确集合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<span id="paper-foundation-models-jev-multicorrect-937628d2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b551d438465d2f51">多正确选项任务要求返回一个答案，还是一个完整正确集合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-multicorrect">When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是恢复所有正确候选组成的集合，集合大小可能超过一。返回一个正确项只满足单选式命中，仍可能漏选；返回所有项也可能误选干扰项。因此先把输出单位从“一个赢家”改成“一个集合”，再理解排序、阈值与exact-set指标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>正确集合是{甲,乙}时，仅返回甲不算完整恢复；返回甲乙丙也因多出丙而不满足精确集合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、方法与本地协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29217v1">原论文</a> · <a href="../../../../system-one/2610.29217-jev-multicorrect/">实现解读</a> · <a href="#qa-b551d438465d2f51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-multicorrect" data-paper-title="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models 基础模型 Independent Researcher 2026-10-21 当一个列表有多个正确选项时，模型可能把大部分概率分给其中一个正确项，另一个正确项虽高于所有干扰项，概率仍低于均匀基线。单选 top-1 或“正确项都排在干扰项之前”因此会掩盖完整集合恢复的失败。论文同时分析 JEV、Luna 和 Gemini，避免把所有现象都归因于某一种架构。特别要区分两种输出：一个候选列表内总和约为1的类别份额，以及对每个选项独立询问“是否正确”得到的二元概率。前者不能直接当作后者的校准置信度。 完整三模型、大规模候选列表实验：成本过高，不复现（审查 DONE）。原文的全量阈值曲线是同一数据上的回溯诊断。本地诊断只检查8项评分/隔离契约：排序与集合恢复的差别、低份额正确项计数、固定验证阈值、数据不重叠、拒答处理、公开回调无标签、五拷贝差距参考值、低概率箱排除的重新归一化。三种子不把固定评分夹具变成正式能力比较，不接入 evolve promotion。  System One / JEV 多正确选项与概率校准审计 结构化决策 候选不变性：顺序、竞争者与概率校准 多个正确选项都排在干扰项前面，为什么完整正确集合仍可能恢复失败？ 候选份额总和受限，一个正确项吸走大部分质量时，另一个正确项虽排名靠前却可能低于阈值或均匀基线。排序正确与集合恢复因此不同，列表份额也不能直接当独立二元概率。部署阈值只可在验证集拟合后冻结，不能从测试曲线挑最佳点。 例如两个正确选项分到很不均的份额，阈值只保留一个，尽管干扰项都更低；这说明单选命中不能替代完整集合的检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f127e2b1238febde">多个正确选项都排在干扰项前面，为什么完整正确集合仍可能恢复失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-multicorrect">When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选份额总和受限，一个正确项吸走大部分质量时，另一个正确项虽排名靠前却可能低于阈值或均匀基线。排序正确与集合恢复因此不同，列表份额也不能直接当独立二元概率。部署阈值只可在验证集拟合后冻结，不能从测试曲线挑最佳点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个正确选项分到很不均的份额，阈值只保留一个，尽管干扰项都更低；这说明单选命中不能替代完整集合的检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、方法与本地协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29217v1">原论文</a> · <a href="../../../../system-one/2610.29217-jev-multicorrect/">实现解读</a> · <a href="#qa-f127e2b1238febde">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-multicorrect" data-paper-title="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models 基础模型 Independent Researcher 2026-10-21 当一个列表有多个正确选项时，模型可能把大部分概率分给其中一个正确项，另一个正确项虽高于所有干扰项，概率仍低于均匀基线。单选 top-1 或“正确项都排在干扰项之前”因此会掩盖完整集合恢复的失败。论文同时分析 JEV、Luna 和 Gemini，避免把所有现象都归因于某一种架构。特别要区分两种输出：一个候选列表内总和约为1的类别份额，以及对每个选项独立询问“是否正确”得到的二元概率。前者不能直接当作后者的校准置信度。 完整三模型、大规模候选列表实验：成本过高，不复现（审查 DONE）。原文的全量阈值曲线是同一数据上的回溯诊断。本地诊断只检查8项评分/隔离契约：排序与集合恢复的差别、低份额正确项计数、固定验证阈值、数据不重叠、拒答处理、公开回调无标签、五拷贝差距参考值、低概率箱排除的重新归一化。三种子不把固定评分夹具变成正式能力比较，不接入 evolve promotion。  System One / JEV 多正确选项与概率校准审计 结构化决策 候选不变性：顺序、竞争者与概率校准 列表份额与独立二元概率为什么需要不同校准解释？ 列表份额受同组其他候选影响，总和受限；独立二元概率允许多个选项同时很高。直接用同一阈值或可靠性解释，会把候选竞争误解为对错置信。 例如再加入一个正确项会分走列表质量，却不必降低原项独立正确的可能性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fa4dc8b32ee9fc84">列表份额与独立二元概率为什么需要不同校准解释？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-multicorrect">When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>列表份额受同组其他候选影响，总和受限；独立二元概率允许多个选项同时很高。直接用同一阈值或可靠性解释，会把候选竞争误解为对错置信。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如再加入一个正确项会分走列表质量，却不必降低原项独立正确的可能性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、方法与本地协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29217v1">原论文</a> · <a href="../../../../system-one/2610.29217-jev-multicorrect/">实现解读</a> · <a href="#qa-fa4dc8b32ee9fc84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-multicorrect" data-paper-title="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models 基础模型 Independent Researcher 2026-10-21 当一个列表有多个正确选项时，模型可能把大部分概率分给其中一个正确项，另一个正确项虽高于所有干扰项，概率仍低于均匀基线。单选 top-1 或“正确项都排在干扰项之前”因此会掩盖完整集合恢复的失败。论文同时分析 JEV、Luna 和 Gemini，避免把所有现象都归因于某一种架构。特别要区分两种输出：一个候选列表内总和约为1的类别份额，以及对每个选项独立询问“是否正确”得到的二元概率。前者不能直接当作后者的校准置信度。 完整三模型、大规模候选列表实验：成本过高，不复现（审查 DONE）。原文的全量阈值曲线是同一数据上的回溯诊断。本地诊断只检查8项评分/隔离契约：排序与集合恢复的差别、低份额正确项计数、固定验证阈值、数据不重叠、拒答处理、公开回调无标签、五拷贝差距参考值、低概率箱排除的重新归一化。三种子不把固定评分夹具变成正式能力比较，不接入 evolve promotion。  System One / JEV 多正确选项与概率校准审计 结构化决策 候选不变性：顺序、竞争者与概率校准 测试集阈值能根据测试exact-set曲线重新选择吗？ 不能。可部署协议只在验证集网格选阈值，再冻结测试；原文同数据阈值曲线属于回溯诊断。预测器也不接收正确集合，避免监督信息直接决定选择。 例如看完测试曲线才挑最佳点，只能说明事后上界，不能称作未见数据的效果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8028e759e705e072">测试集阈值能根据测试exact-set曲线重新选择吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-multicorrect">When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。可部署协议只在验证集网格选阈值，再冻结测试；原文同数据阈值曲线属于回溯诊断。预测器也不接收正确集合，避免监督信息直接决定选择。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如看完测试曲线才挑最佳点，只能说明事后上界，不能称作未见数据的效果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、方法与本地协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29217v1">原论文</a> · <a href="../../../../system-one/2610.29217-jev-multicorrect/">实现解读</a> · <a href="#qa-8028e759e705e072">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:prism-1" data-paper-title="Prism-1: Position- and Rival-Independent Scoring for System One Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="Prism-1: Position- and Rival-Independent Scoring for System One Models 基础模型 Nanyang Technological University 2026-10-15 JEV/System One 选择模型希望在一次前向中选出工具、意图或界面元素。普通多选提示会让答案依赖选项顺序和无关选项。§2–4 由 Luce 选择公理推导：每个选项的分数只能看共享状态、问题和该选项本身；最后对独立分数做 softmax。只在输出层加 softmax、不隔离 attention 或不重置位置，都不能保证这一性质。 作者每模型/方法使用2–3种子，单次 H100 50–85分钟，完整多臂训练和评估超出本轮预算，成本过高，不复现（审查 DONE）。诊断指标与GPU回执保存实际设备、提交与执行源码哈希。不下载数据或权重。固定 revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1；seeds42/43/44。真实微型 Transformer 用随机初始化、共享绝对位置嵌入、2层、24维、3 heads；三个不同长度的整数 token 选项。一次任意标签交叉熵更新只检查梯度，不是测试答案或任务能力评估。  JEV与单步决策 选项隔离与选择不变性 结构化决策 候选不变性：顺序、竞争者与概率校准 Prism-1加入第三个选项后，要求旧两项概率数值完全不变吗？ 不要求。新增项会加入softmax分母，旧项份额可以同时下降；要求保持的是旧两项之间的相对赔率与排序。新项也可以成为赢家。这是候选选择的一种一致性约束，不能误读成模型必须无视所有新增选项。 教学例子：甲乙原为2比1，加入丙后可变成0.4和0.2；份额变了，但甲乙仍为2比1。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<span id="paper-foundation-models-prism-1-45b3ae20" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-746ef6fbeaffa986">Prism-1加入第三个选项后，要求旧两项概率数值完全不变吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aprism-1">Prism-1: Position- and Rival-Independent Scoring for System One Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不要求。新增项会加入softmax分母，旧项份额可以同时下降；要求保持的是旧两项之间的相对赔率与排序。新项也可以成为赢家。这是候选选择的一种一致性约束，不能误读成模型必须无视所有新增选项。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲乙原为2比1，加入丙后可变成0.4和0.2；份额变了，但甲乙仍为2比1。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22066">原论文</a> · <a href="../../../../foundation-models/2610.22066-prism-1/">实现解读</a> · <a href="#qa-746ef6fbeaffa986">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:prism-1" data-paper-title="Prism-1: Position- and Rival-Independent Scoring for System One Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="Prism-1: Position- and Rival-Independent Scoring for System One Models 基础模型 Nanyang Technological University 2026-10-15 JEV/System One 选择模型希望在一次前向中选出工具、意图或界面元素。普通多选提示会让答案依赖选项顺序和无关选项。§2–4 由 Luce 选择公理推导：每个选项的分数只能看共享状态、问题和该选项本身；最后对独立分数做 softmax。只在输出层加 softmax、不隔离 attention 或不重置位置，都不能保证这一性质。 作者每模型/方法使用2–3种子，单次 H100 50–85分钟，完整多臂训练和评估超出本轮预算，成本过高，不复现（审查 DONE）。诊断指标与GPU回执保存实际设备、提交与执行源码哈希。不下载数据或权重。固定 revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1；seeds42/43/44。真实微型 Transformer 用随机初始化、共享绝对位置嵌入、2层、24维、3 heads；三个不同长度的整数 token 选项。一次任意标签交叉熵更新只检查梯度，不是测试答案或任务能力评估。  JEV与单步决策 选项隔离与选择不变性 结构化决策 候选不变性：顺序、竞争者与概率校准 Prism-1为什么既隔离选项注意力，又让各选项从相同位置编号开始？ 每个选项分数只能依赖共享状态、问题和自身，隔离注意力避免读取其他选项，相同起始位置则排除顺序带来的位置差异。最后统一softmax允许分母变化，却应保留旧选项相对赔率。该假设不适合必须跨选项比较的以上皆非，也不防共享状态中的注入。 例如新增第三个工具可成为赢家，也会降低旧工具的份额，但不应仅因插入位置就让原来两个工具交换排名；同位置与隔离共同约束读出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f8589f6603d77f11">Prism-1为什么既隔离选项注意力，又让各选项从相同位置编号开始？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aprism-1">Prism-1: Position- and Rival-Independent Scoring for System One Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个选项分数只能依赖共享状态、问题和自身，隔离注意力避免读取其他选项，相同起始位置则排除顺序带来的位置差异。最后统一softmax允许分母变化，却应保留旧选项相对赔率。该假设不适合必须跨选项比较的以上皆非，也不防共享状态中的注入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新增第三个工具可成为赢家，也会降低旧工具的份额，但不应仅因插入位置就让原来两个工具交换排名；同位置与隔离共同约束读出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22066">原论文</a> · <a href="../../../../foundation-models/2610.22066-prism-1/">实现解读</a> · <a href="#qa-f8589f6603d77f11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:prism-1" data-paper-title="Prism-1: Position- and Rival-Independent Scoring for System One Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="Prism-1: Position- and Rival-Independent Scoring for System One Models 基础模型 Nanyang Technological University 2026-10-15 JEV/System One 选择模型希望在一次前向中选出工具、意图或界面元素。普通多选提示会让答案依赖选项顺序和无关选项。§2–4 由 Luce 选择公理推导：每个选项的分数只能看共享状态、问题和该选项本身；最后对独立分数做 softmax。只在输出层加 softmax、不隔离 attention 或不重置位置，都不能保证这一性质。 作者每模型/方法使用2–3种子，单次 H100 50–85分钟，完整多臂训练和评估超出本轮预算，成本过高，不复现（审查 DONE）。诊断指标与GPU回执保存实际设备、提交与执行源码哈希。不下载数据或权重。固定 revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1；seeds42/43/44。真实微型 Transformer 用随机初始化、共享绝对位置嵌入、2层、24维、3 heads；三个不同长度的整数 token 选项。一次任意标签交叉熵更新只检查梯度，不是测试答案或任务能力评估。  JEV与单步决策 选项隔离与选择不变性 结构化决策 候选不变性：顺序、竞争者与概率校准 Prism-1的独立选项假设，与“以上皆非”这类候选为什么不相容？ 独立分数只看共享状态、问题和该选项自身；“以上皆非”的正确含义却取决于其他选项是否成立，需要跨选项信息。这样的任务不能直接要求相同Luce约束。它说明结构假设的适用边界，不是模型多加训练即可消除的普通误差。 教学例子：把一个正确答案加入候选后，“以上皆非”应变错；若该项根本不能读取其他候选，就无法表达这层依赖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-48222e52dee00817">Prism-1的独立选项假设，与“以上皆非”这类候选为什么不相容？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aprism-1">Prism-1: Position- and Rival-Independent Scoring for System One Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立分数只看共享状态、问题和该选项自身；“以上皆非”的正确含义却取决于其他选项是否成立，需要跨选项信息。这样的任务不能直接要求相同Luce约束。它说明结构假设的适用边界，不是模型多加训练即可消除的普通误差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把一个正确答案加入候选后，“以上皆非”应变错；若该项根本不能读取其他候选，就无法表达这层依赖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22066">原论文</a> · <a href="../../../../foundation-models/2610.22066-prism-1/">实现解读</a> · <a href="#qa-48222e52dee00817">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:prism-1" data-paper-title="Prism-1: Position- and Rival-Independent Scoring for System One Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="Prism-1: Position- and Rival-Independent Scoring for System One Models 基础模型 Nanyang Technological University 2026-10-15 JEV/System One 选择模型希望在一次前向中选出工具、意图或界面元素。普通多选提示会让答案依赖选项顺序和无关选项。§2–4 由 Luce 选择公理推导：每个选项的分数只能看共享状态、问题和该选项本身；最后对独立分数做 softmax。只在输出层加 softmax、不隔离 attention 或不重置位置，都不能保证这一性质。 作者每模型/方法使用2–3种子，单次 H100 50–85分钟，完整多臂训练和评估超出本轮预算，成本过高，不复现（审查 DONE）。诊断指标与GPU回执保存实际设备、提交与执行源码哈希。不下载数据或权重。固定 revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1；seeds42/43/44。真实微型 Transformer 用随机初始化、共享绝对位置嵌入、2层、24维、3 heads；三个不同长度的整数 token 选项。一次任意标签交叉熵更新只检查梯度，不是测试答案或任务能力评估。  JEV与单步决策 选项隔离与选择不变性 结构化决策 候选不变性：顺序、竞争者与概率校准 Prism-1的选项block可以看到其他选项或沿用不同起点吗？ 不能。每块可读共享上下文并在块内因果注意，但不能读其他选项，各块从同一位置编号开始。否则独立分数假设不成立；共享上下文注入也仍不受此隔离保护。 例如插入一个更长选项若推迟后面块的位置，就会引入本该消除的位置差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-19cf1c2f49d33384">Prism-1的选项block可以看到其他选项或沿用不同起点吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aprism-1">Prism-1: Position- and Rival-Independent Scoring for System One Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。每块可读共享上下文并在块内因果注意，但不能读其他选项，各块从同一位置编号开始。否则独立分数假设不成立；共享上下文注入也仍不受此隔离保护。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如插入一个更长选项若推迟后面块的位置，就会引入本该消除的位置差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22066">原论文</a> · <a href="../../../../foundation-models/2610.22066-prism-1/">实现解读</a> · <a href="#qa-19cf1c2f49d33384">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-request-audit" data-paper-title="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval 基础模型 Tsinghua University 2026-10-10 合法结构化输出不能保证问题彼此独立。论文分离三种干预：增加请求问题时保持证据和目标命题不变；增加证据时保持原目标、候选资格不变；增加可选候选时保持全部显示证据不变。这样可以区分问题 schema 依赖、真实上下文改变和候选归一化效应。论文对 TREC DL2019/2020 的 92 个 query 构造 276 个三段落状态，按 0/1/2 个正例平衡场景；它不是生产分布。输入不包含 qrels、原始文档 ID 或场景名。 已实现三种不混淆通道的干预构造器、gold-free 独立编译器、数值稳定的标签质量/条件概率计算、保留 A/B 偏好、严格翻转和 tie、阈值动作、二元正确率与动作正确率差。  System One / JEV 公共评测与能力边界 结构化决策 候选不变性：顺序、竞争者与概率校准 请求独立性为何是结构化决策输出之外的另一问题？ 合法JSON或候选标签只保证格式，模型仍可能因多了无关问题而改变原判断。独立性审计固定证据与目标，专门测请求组合是否产生额外干扰。 例如两个问题都返回合法概率，仍可能因为并排询问而使第一个结论翻转。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<span id="paper-foundation-models-jev-request-audit-c38888e5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-767199f3c4dd3bb1">请求独立性为何是结构化决策输出之外的另一问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-request-audit">The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>合法JSON或候选标签只保证格式，模型仍可能因多了无关问题而改变原判断。独立性审计固定证据与目标，专门测请求组合是否产生额外干扰。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个问题都返回合法概率，仍可能因为并排询问而使第一个结论翻转。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14631">原论文</a> · <a href="../../../../system-one/2610.14631-request-audit/">实现解读</a> · <a href="#qa-767199f3c4dd3bb1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-request-audit" data-paper-title="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval 基础模型 Tsinghua University 2026-10-10 合法结构化输出不能保证问题彼此独立。论文分离三种干预：增加请求问题时保持证据和目标命题不变；增加证据时保持原目标、候选资格不变；增加可选候选时保持全部显示证据不变。这样可以区分问题 schema 依赖、真实上下文改变和候选归一化效应。论文对 TREC DL2019/2020 的 92 个 query 构造 276 个三段落状态，按 0/1/2 个正例平衡场景；它不是生产分布。输入不包含 qrels、原始文档 ID 或场景名。 已实现三种不混淆通道的干预构造器、gold-free 独立编译器、数值稳定的标签质量/条件概率计算、保留 A/B 偏好、严格翻转和 tie、阈值动作、二元正确率与动作正确率差。  System One / JEV 公共评测与能力边界 结构化决策 候选不变性：顺序、竞争者与概率校准 请求独立性审计为什么要把加问题、加证据与加候选分成三种干预？ 加问题应保持目标命题和证据不变，才是在测无关请求干扰；加证据会真实改变上下文，加候选则引入归一化效应。混做一次无法定位翻转原因。候选扩展应比较原两项条件赔率，评分端持有的相关性标签、场景名与文档身份不能进入预测输入。 例如仅多问一个无关问题就翻转原答案值得警惕；加入新证据后翻转可能合理，加入第三候选导致原概率变小也未必改变相对偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-798da5e084b4917f">请求独立性审计为什么要把加问题、加证据与加候选分成三种干预？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-request-audit">The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>加问题应保持目标命题和证据不变，才是在测无关请求干扰；加证据会真实改变上下文，加候选则引入归一化效应。混做一次无法定位翻转原因。候选扩展应比较原两项条件赔率，评分端持有的相关性标签、场景名与文档身份不能进入预测输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如仅多问一个无关问题就翻转原答案值得警惕；加入新证据后翻转可能合理，加入第三候选导致原概率变小也未必改变相对偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14631">原论文</a> · <a href="../../../../system-one/2610.14631-request-audit/">实现解读</a> · <a href="#qa-798da5e084b4917f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-request-audit" data-paper-title="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval 基础模型 Tsinghua University 2026-10-10 合法结构化输出不能保证问题彼此独立。论文分离三种干预：增加请求问题时保持证据和目标命题不变；增加证据时保持原目标、候选资格不变；增加可选候选时保持全部显示证据不变。这样可以区分问题 schema 依赖、真实上下文改变和候选归一化效应。论文对 TREC DL2019/2020 的 92 个 query 构造 276 个三段落状态，按 0/1/2 个正例平衡场景；它不是生产分布。输入不包含 qrels、原始文档 ID 或场景名。 已实现三种不混淆通道的干预构造器、gold-free 独立编译器、数值稳定的标签质量/条件概率计算、保留 A/B 偏好、严格翻转和 tie、阈值动作、二元正确率与动作正确率差。  System One / JEV 公共评测与能力边界 结构化决策 候选不变性：顺序、竞争者与概率校准 候选扩展后原概率下降，与真正偏好翻转怎样区分？ 加入候选自然增大softmax分母，因此原项份额下降不必是行为异常。比较原两项条件赔率或严格二元翻转，才能分离归一化与相对偏好变化。 例如A从较高份额下降但仍胜B，只是新C分走质量，不等于A/B次序反了。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7e80d05c23dcc2ce">候选扩展后原概率下降，与真正偏好翻转怎样区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-request-audit">The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>加入候选自然增大softmax分母，因此原项份额下降不必是行为异常。比较原两项条件赔率或严格二元翻转，才能分离归一化与相对偏好变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如A从较高份额下降但仍胜B，只是新C分走质量，不等于A/B次序反了。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14631">原论文</a> · <a href="../../../../system-one/2610.14631-request-audit/">实现解读</a> · <a href="#qa-7e80d05c23dcc2ce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-request-audit" data-paper-title="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval 基础模型 Tsinghua University 2026-10-10 合法结构化输出不能保证问题彼此独立。论文分离三种干预：增加请求问题时保持证据和目标命题不变；增加证据时保持原目标、候选资格不变；增加可选候选时保持全部显示证据不变。这样可以区分问题 schema 依赖、真实上下文改变和候选归一化效应。论文对 TREC DL2019/2020 的 92 个 query 构造 276 个三段落状态，按 0/1/2 个正例平衡场景；它不是生产分布。输入不包含 qrels、原始文档 ID 或场景名。 已实现三种不混淆通道的干预构造器、gold-free 独立编译器、数值稳定的标签质量/条件概率计算、保留 A/B 偏好、严格翻转和 tie、阈值动作、二元正确率与动作正确率差。  System One / JEV 公共评测与能力边界 结构化决策 候选不变性：顺序、竞争者与概率校准 恰好0.5的二元预测为什么不算strict flip？ 严格翻转要求两次概率分别位于阈值两侧，乘积严格小于零；任一等于0.5另记tie。把边界点硬分边会夸大翻转，也会隐藏评分精度影响。 例如一次是0.5、另一次偏向是，只能记边界变化，不能称明确从否翻到是。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3a4343ba2fd01e84">恰好0.5的二元预测为什么不算strict flip？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-request-audit">The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>严格翻转要求两次概率分别位于阈值两侧，乘积严格小于零；任一等于0.5另记tie。把边界点硬分边会夸大翻转，也会隐藏评分精度影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次是0.5、另一次偏向是，只能记边界变化，不能称明确从否翻到是。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14631">原论文</a> · <a href="../../../../system-one/2610.14631-request-audit/">实现解读</a> · <a href="#qa-3a4343ba2fd01e84">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

只改选项顺序或加入无关候选，为什么原来的偏好可能改变？

## 记住这一点

Prism-1 从选择公理出发，让每个选项只读共享状态和自身内容，使用隔离 attention block 和相同起始位置，再对独立分数做 softmax。请求审计则把增加问题、增加证据和增加候选资格分开干预。这样才能区分模型依赖了其他题目、真正获得新证据，还是仅被归一化分母影响。

## 一个例子

原有 A、B 的指数分数是 2、1，加入分数为 5 的 C 后，A 的概率由 2/3 降到 2/8 是正常归一化；A 相对 B 的赔率仍应是 2。若旧二者排序互换，就要排查交叉选项注意力、位置变化或问题 schema 泄漏。

## 什么时候要小心

不变性不保证高准确率，也不禁止新候选 C 成为赢家。“以上皆非”等任务需要跨选项语义，不能机械套独立打分。严格翻转与恰好同分要分开，置信区间包含零也不能写成已证明没有影响；本地审计脚本不等于已生成论文模型预测。

## 先读这几篇

先读 Prism-1 的独立选项分数、block mask 和位置编号，明确不变性条件；再读请求审计的三类配对干预，学习怎样测量而不把概率归一化误判为偏好翻转。

1. [Prism-1: Position- and Rival-Independent Scoring for System One Models](../../../foundation-models/2610.22066-prism-1/README.md) · [原论文](https://arxiv.org/abs/2610.22066)
2. [The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval](../../../system-one/2610.14631-request-audit/README.md) · [原论文](https://arxiv.org/abs/2610.14631)

## 自测一下

加入 C 后 A 的绝对概率降低，就足以判定违反候选独立性吗？

??? note "展开参考答案"

    不足。先比较旧候选的条件概率 A/(A+B) 或赔率 A/B，并保持共享证据不变；分母加入 C 会自然降低 A 的绝对概率。还要区分新增有效信息与单纯候选资格变化。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
