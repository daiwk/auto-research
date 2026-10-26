---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 候选不变性：顺序、竞争者与概率校准

[结构化决策](index.md) / 3 个问题 · 3 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">3 个问题 · 3 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-multicorrect" data-paper-title="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="When Multiple Choices Are Correct: Asymmetric Probability Allocation in Jev and Other Decision Models 基础模型 Independent Researcher 2026-10-21 当一个列表有多个正确选项时，模型可能把大部分概率分给其中一个正确项，另一个正确项虽高于所有干扰项，概率仍低于均匀基线。单选 top-1 或“正确项都排在干扰项之前”因此会掩盖完整集合恢复的失败。论文同时分析 JEV、Luna 和 Gemini，避免把所有现象都归因于某一种架构。特别要区分两种输出：一个候选列表内总和约为1的类别份额，以及对每个选项独立询问“是否正确”得到的二元概率。前者不能直接当作后者的校准置信度。 完整三模型、大规模候选列表实验：成本过高，不复现（审查 DONE）。原文的全量阈值曲线是同一数据上的回溯诊断。本地诊断只检查8项评分/隔离契约：排序与集合恢复的差别、低份额正确项计数、固定验证阈值、数据不重叠、拒答处理、公开回调无标签、五拷贝差距参考值、低概率箱排除的重新归一化。三种子不把固定评分夹具变成正式能力比较，不接入 evolve promotion。  System One / JEV 多正确选项与概率校准审计 结构化决策 候选不变性：顺序、竞争者与概率校准 多个正确选项都排在干扰项前面，为什么完整正确集合仍可能恢复失败？ 候选份额总和受限，一个正确项吸走大部分质量时，另一个正确项虽排名靠前却可能低于阈值或均匀基线。排序正确与集合恢复因此不同，列表份额也不能直接当独立二元概率。部署阈值只可在验证集拟合后冻结，不能从测试曲线挑最佳点。 例如两个正确选项分到很不均的份额，阈值只保留一个，尽管干扰项都更低；这说明单选命中不能替代完整集合的检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<span id="paper-foundation-models-jev-multicorrect-937628d2" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:prism-1" data-paper-title="Prism-1: Position- and Rival-Independent Scoring for System One Models" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="Prism-1: Position- and Rival-Independent Scoring for System One Models 基础模型 Nanyang Technological University 2026-10-15 JEV/System One 选择模型希望在一次前向中选出工具、意图或界面元素。普通多选提示会让答案依赖选项顺序和无关选项。§2–4 由 Luce 选择公理推导：每个选项的分数只能看共享状态、问题和该选项本身；最后对独立分数做 softmax。只在输出层加 softmax、不隔离 attention 或不重置位置，都不能保证这一性质。 作者每模型/方法使用2–3种子，单次 H100 50–85分钟，完整多臂训练和评估超出本轮预算，成本过高，不复现（审查 DONE）。诊断指标与GPU回执保存实际设备、提交与执行源码哈希。不下载数据或权重。固定 revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1；seeds42/43/44。真实微型 Transformer 用随机初始化、共享绝对位置嵌入、2层、24维、3 heads；三个不同长度的整数 token 选项。一次任意标签交叉熵更新只检查梯度，不是测试答案或任务能力评估。  JEV与单步决策 选项隔离与选择不变性 结构化决策 候选不变性：顺序、竞争者与概率校准 Prism-1为什么既隔离选项注意力，又让各选项从相同位置编号开始？ 每个选项分数只能依赖共享状态、问题和自身，隔离注意力避免读取其他选项，相同起始位置则排除顺序带来的位置差异。最后统一softmax允许分母变化，却应保留旧选项相对赔率。该假设不适合必须跨选项比较的以上皆非，也不防共享状态中的注入。 例如新增第三个工具可成为赢家，也会降低旧工具的份额，但不应仅因插入位置就让原来两个工具交换排名；同位置与隔离共同约束读出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<span id="paper-foundation-models-prism-1-45b3ae20" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-request-audit" data-paper-title="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/candidate-invariance" data-search="The Company a Question Keeps: Auditing Open Jev-Style Models for Retrieval 基础模型 Tsinghua University 2026-10-10 合法结构化输出不能保证问题彼此独立。论文分离三种干预：增加请求问题时保持证据和目标命题不变；增加证据时保持原目标、候选资格不变；增加可选候选时保持全部显示证据不变。这样可以区分问题 schema 依赖、真实上下文改变和候选归一化效应。论文对 TREC DL2019/2020 的 92 个 query 构造 276 个三段落状态，按 0/1/2 个正例平衡场景；它不是生产分布。输入不包含 qrels、原始文档 ID 或场景名。 已实现三种不混淆通道的干预构造器、gold-free 独立编译器、数值稳定的标签质量/条件概率计算、保留 A/B 偏好、严格翻转和 tie、阈值动作、二元正确率与动作正确率差。  System One / JEV 公共评测与能力边界 结构化决策 候选不变性：顺序、竞争者与概率校准 请求独立性审计为什么要把加问题、加证据与加候选分成三种干预？ 加问题应保持目标命题和证据不变，才是在测无关请求干扰；加证据会真实改变上下文，加候选则引入归一化效应。混做一次无法定位翻转原因。候选扩展应比较原两项条件赔率，评分端持有的相关性标签、场景名与文档身份不能进入预测输入。 例如仅多问一个无关问题就翻转原答案值得警惕；加入新证据后翻转可能合理，加入第三候选导致原概率变小也未必改变相对偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 候选不变性：顺序、竞争者与概率校准</a></p>
<span id="paper-foundation-models-jev-request-audit-c38888e5" class="ar-learning-paper-anchor"></span>
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
