---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 候选不变性：顺序、竞争者与概率校准

[结构化决策](index.md) / 子主题导学 · 约 3 分钟 · 3 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 3 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models 基础模型 Independent Researcher 2026-10-21 当一个列表有多个正确选项时，模型可能把大部分概率分给其中一个正确项，另一个正确项虽高于所有干扰项，概率仍低于均匀基线。单选 top-1 或“正确项都排在干扰项之前”因此会掩盖完整集合恢复的失败。论文同时分析 JEV、Luna 和 Gemini，避免把所有现象都归因于某一种架构。特别要区分两种输出：一个候选列表内总和约为1的类别份额，以及对每个选项独立询问“是否正确”得到的二元概率。前者不能直接当作后者的校准置信度。 完整三模型、大规模候选列表实验：成本过高，不复现（审查 DONE）。原文的全量阈值曲线是同一数据上的回溯诊断。本地诊断只检查8项评分/隔离契约：排序与集合恢复的差别、低份额正确项计数、固定验证阈值、数据不重叠、拒答处理、公开回调无标签、五拷贝差距参考值、低概率箱排除的重新归一化。三种子不把固定评分夹具变成正式能力比较，不接入 evolve promotion。  System One / JEV 多正确选项与概率校准审计 结构化决策 候选不变性：顺序、竞争者与概率校准">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<h2 id="paper-foundation-models-jev-multicorrect-937628d2">When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models</h2>
<p class="ar-learning-card__meta">Independent Researcher · 论文公开：2026-10-21</p>
<p><strong>方法要点：</strong>当一个列表有多个正确选项时，模型可能把大部分概率分给其中一个正确项，另一个正确项虽高于所有干扰项，概率仍低于均匀基线。单选 top-1 或“正确项都排在干扰项之前”因此会掩盖完整集合恢复的失败。论文同时分析 JEV、Luna 和 Gemini，避免把所有现象都归因于某一种架构。特别要区分两种输出：一个候选列表内总和约为1的类别份额，以及对每个选项独立询问“是否正确”得到的二元概率。前者不能直接当作后者的校准置信度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整三模型、大规模候选列表实验：成本过高，不复现（审查 DONE）。原文的全量阈值曲线是同一数据上的回溯诊断。本地诊断只检查8项评分/隔离契约：排序与集合恢复的差别、低份额正确项计数、固定验证阈值、数据不重叠、拒答处理、公开回调无标签、五拷贝差距参考值、低概率箱排除的重新归一化。三种子不把固定评分夹具变成正式能力比较，不接入 evolve promotion。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29217v1">原论文</a> · <a href="../../../../system-one/2610.29217-jev-multicorrect/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="Prism-1: Position- and Rival-Independent Scoring for System One Models 基础模型 Nanyang Technological University 2026-10-15 JEV/System One 选择模型希望在一次前向中选出工具、意图或界面元素。普通多选提示会让答案依赖选项顺序和无关选项。§2–4 由 Luce 选择公理推导：每个选项的分数只能看共享状态、问题和该选项本身；最后对独立分数做 softmax。只在输出层加 softmax、不隔离 attention 或不重置位置，都不能保证这一性质。 作者每模型/方法使用2–3种子，单次 H100 50–85分钟，完整多臂训练和评估超出本轮预算，成本过高，不复现（审查 DONE）。诊断指标与GPU回执保存实际设备、提交与执行源码哈希。不下载数据或权重。固定 revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1；seeds42/43/44。真实微型 Transformer 用随机初始化、共享绝对位置嵌入、2层、24维、3 heads；三个不同长度的整数 token 选项。一次任意标签交叉熵更新只检查梯度，不是测试答案或任务能力评估。  JEV与单步决策 选项隔离与选择不变性 结构化决策 候选不变性：顺序、竞争者与概率校准">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<h2 id="paper-foundation-models-prism-1-45b3ae20">Prism-1: Position- and Rival-Independent Scoring for System One Models</h2>
<p class="ar-learning-card__meta">Nanyang Technological University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>JEV/System One 选择模型希望在一次前向中选出工具、意图或界面元素。普通多选提示会让答案依赖选项顺序和无关选项。§2–4 由 Luce 选择公理推导：每个选项的分数只能看共享状态、问题和该选项本身；最后对独立分数做 softmax。只在输出层加 softmax、不隔离 attention 或不重置位置，都不能保证这一性质。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>作者每模型/方法使用2–3种子，单次 H100 50–85分钟，完整多臂训练和评估超出本轮预算，成本过高，不复现（审查 DONE）。诊断指标与GPU回执保存实际设备、提交与执行源码哈希。不下载数据或权重。固定 revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1；seeds42/43/44。真实微型 Transformer 用随机初始化、共享绝对位置嵌入、2层、24维、3 heads；三个不同长度的整数 token 选项。一次任意标签交叉熵更新只检查梯度，不是测试答案或任务能力评估。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22066">原论文</a> · <a href="../../../../foundation-models/2610.22066-prism-1/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval 基础模型 Tsinghua University 2026-10-10 合法结构化输出不能保证问题彼此独立。论文分离三种干预：增加请求问题时保持证据和目标命题不变；增加证据时保持原目标、候选资格不变；增加可选候选时保持全部显示证据不变。这样可以区分问题 schema 依赖、真实上下文改变和候选归一化效应。论文对 TREC DL2019/2020 的 92 个 query 构造 276 个三段落状态，按 0/1/2 个正例平衡场景；它不是生产分布。输入不包含 qrels、原始文档 ID 或场景名。 已实现三种不混淆通道的干预构造器、gold-free 独立编译器、数值稳定的标签质量/条件概率计算、保留 A/B 偏好、严格翻转和 tie、阈值动作、二元正确率与动作正确率差。  System One / JEV 公共评测与能力边界 结构化决策 候选不变性：顺序、竞争者与概率校准">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<h2 id="paper-foundation-models-jev-request-audit-c38888e5">The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-10-10</p>
<p><strong>方法要点：</strong>合法结构化输出不能保证问题彼此独立。论文分离三种干预：增加请求问题时保持证据和目标命题不变；增加证据时保持原目标、候选资格不变；增加可选候选时保持全部显示证据不变。这样可以区分问题 schema 依赖、真实上下文改变和候选归一化效应。论文对 TREC DL2019/2020 的 92 个 query 构造 276 个三段落状态，按 0/1/2 个正例平衡场景；它不是生产分布。输入不包含 qrels、原始文档 ID 或场景名。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>已实现三种不混淆通道的干预构造器、gold-free 独立编译器、数值稳定的标签质量/条件概率计算、保留 A/B 偏好、严格翻转和 tie、阈值动作、二元正确率与动作正确率差。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14631">原论文</a> · <a href="../../../../system-one/2610.14631-request-audit/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
