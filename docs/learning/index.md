---
hide:
  - toc
---

# 论文学习

每篇论文按四层学习：**基础理解 → 核心机制 → 方法对比 → 实现细节**。先试着回答，再展开解释和教学例子；可以只看某一层，也可以继续给同一篇补充问题。

<div class="ar-learning-actions" markdown="1">

[专题精读](deep-dives/index.md){ .md-button .md-button--primary }
[搜索全部问答](all.md){ .md-button }
[最近新增问题](recent.md){ .md-button }

</div>

## 按主题学习

目录按主题折叠。想串起多篇论文，选择“精读对比”；想逐篇学习，选择子主题问题库。每张精读卡片包含机制对照、取舍分析与多个跨论文问答，并随新论文小幅更新。

<!-- learning-topics:start -->

6 个主题 · 31 个子主题 · 4143 个问题 / 1034 篇论文

<div class="ar-learning-topics">
<article class="ar-learning-topic-tile">
<h2><a href="paths/recommendation/">搜广推</a></h2>
<p>从找候选走到排序与展示：学习语义表征、用户知识、长历史、生成式推荐、反馈与服务。</p>
<p class="ar-learning-topic-meta">7 个子主题 · 1283 问 / 319 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/recommendation/retrieval-matching/">候选生成与搜索匹配</a><span>144 问<a class="ar-learning-deep-link" href="deep-dives/recommendation/retrieval-matching/">精读对比</a></span></li>
<li><a href="paths/recommendation/content-semantic-ids/">语义表征、用户知识与冷启动</a><span>240 问<a class="ar-learning-deep-link" href="deep-dives/recommendation/content-semantic-ids/">精读对比</a></span></li>
<li><a href="paths/recommendation/history-ranking-backbones/">用户历史与排序骨干</a><span>299 问<a class="ar-learning-deep-link" href="deep-dives/recommendation/history-ranking-backbones/">精读对比</a></span></li>
<li><a href="paths/recommendation/generative-retrieval-reasoning/">生成式召回与推理推荐</a><span>240 问<a class="ar-learning-deep-link" href="deep-dives/recommendation/generative-retrieval-reasoning/">精读对比</a></span></li>
<li><a href="paths/recommendation/feedback-multitask-causality/">学习信号、多任务与反馈偏差</a><span>140 问<a class="ar-learning-deep-link" href="deep-dives/recommendation/feedback-multitask-causality/">精读对比</a></span></li>
<li><a href="paths/recommendation/slates-business-value/">重排、展示与长期价值</a><span>144 问<a class="ar-learning-deep-link" href="deep-dives/recommendation/slates-business-value/">精读对比</a></span></li>
<li><a href="paths/recommendation/research-serving-loop/">自动研究与高效上线</a><span>76 问<a class="ar-learning-deep-link" href="deep-dives/recommendation/research-serving-loop/">精读对比</a></span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/foundation-models/">基础模型</a></h2>
<p>理解模型怎样读取上下文、分配计算和训练预算，以及压缩、生成与能力评测的取舍。</p>
<p class="ar-learning-topic-meta">6 个子主题 · 568 问 / 142 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/foundation-models/context-and-state/">长上下文：注意力、递归状态与记忆</a><span>124 问<a class="ar-learning-deep-link" href="deep-dives/foundation-models/context-and-state/">精读对比</a></span></li>
<li><a href="paths/foundation-models/conditional-compute/">按需计算：专家、弹性深宽与查表记忆</a><span>104 问<a class="ar-learning-deep-link" href="deep-dives/foundation-models/conditional-compute/">精读对比</a></span></li>
<li><a href="paths/foundation-models/training-budget/">训练预算：数据配比、目标与优化器</a><span>112 问<a class="ar-learning-deep-link" href="deep-dives/foundation-models/training-budget/">精读对比</a></span></li>
<li><a href="paths/foundation-models/compression-and-cache/">推理压缩：权重、KV 缓存与服务带宽</a><span>116 问<a class="ar-learning-deep-link" href="deep-dives/foundation-models/compression-and-cache/">精读对比</a></span></li>
<li><a href="paths/foundation-models/generation-paths/">生成路径：草稿验证、并行去噪与少步迭代</a><span>60 问<a class="ar-learning-deep-link" href="deep-dives/foundation-models/generation-paths/">精读对比</a></span></li>
<li><a href="paths/foundation-models/evaluation-and-evidence/">能力证据：评测采样、读出与可靠性</a><span>52 问<a class="ar-learning-deep-link" href="deep-dives/foundation-models/evaluation-and-evidence/">精读对比</a></span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/system-one/">结构化决策</a></h2>
<p>把语言模型用于有限候选决策：先看如何读出分布，再检验不变性、推理预算与持续反馈。</p>
<p class="ar-learning-topic-meta">3 个子主题 · 64 问 / 16 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/system-one/typed-readout/">类型化读出：从生成句子到候选分布</a><span>36 问<a class="ar-learning-deep-link" href="deep-dives/system-one/typed-readout/">精读对比</a></span></li>
<li><a href="paths/system-one/candidate-invariance/">候选不变性：顺序、竞争者与概率校准</a><span>12 问<a class="ar-learning-deep-link" href="deep-dives/system-one/candidate-invariance/">精读对比</a></span></li>
<li><a href="paths/system-one/adaptive-decisions/">按需决策：选择性推理、迁移与持续反馈</a><span>16 问<a class="ar-learning-deep-link" href="deep-dives/system-one/adaptive-decisions/">精读对比</a></span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/multimodal-models/">多模态</a></h2>
<p>围绕三件事学习：对齐不同模态、分配视觉证据预算、预测状态与动作的后果。</p>
<p class="ar-learning-topic-meta">3 个子主题 · 232 问 / 58 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/multimodal-models/alignment-interfaces/">跨模态对齐：表征、连接器与监督</a><span>80 问<a class="ar-learning-deep-link" href="deep-dives/multimodal-models/alignment-interfaces/">精读对比</a></span></li>
<li><a href="paths/multimodal-models/visual-evidence-budget/">视觉证据预算：选 Token、选帧与按需回看</a><span>64 问<a class="ar-learning-deep-link" href="deep-dives/multimodal-models/visual-evidence-budget/">精读对比</a></span></li>
<li><a href="paths/multimodal-models/world-state-actions/">视觉世界建模：状态、生成与动作条件</a><span>88 问<a class="ar-learning-deep-link" href="deep-dives/multimodal-models/world-state-actions/">精读对比</a></span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/post-training/">LLM 后训练</a></h2>
<p>先分清反馈来自哪里，再看策略更新、步骤信用、教师监督，以及数据和算力如何分配。</p>
<p class="ar-learning-topic-meta">6 个子主题 · 960 问 / 240 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/post-training/preference-and-alignment/">偏好与对齐：先看反馈长什么样</a><span>100 问<a class="ar-learning-deep-link" href="deep-dives/post-training/preference-and-alignment/">精读对比</a></span></li>
<li><a href="paths/post-training/policy-optimization/">策略优化：谁在采样，谁在被更新</a><span>216 问<a class="ar-learning-deep-link" href="deep-dives/post-training/policy-optimization/">精读对比</a></span></li>
<li><a href="paths/post-training/reward-and-credit/">奖励与信用：正确结果该奖励哪些步骤</a><span>144 问<a class="ar-learning-deep-link" href="deep-dives/post-training/reward-and-credit/">精读对比</a></span></li>
<li><a href="paths/post-training/student-trajectory-distillation/">在策略蒸馏：沿学生实际走过的前缀学习</a><span>160 问<a class="ar-learning-deep-link" href="deep-dives/post-training/student-trajectory-distillation/">精读对比</a></span></li>
<li><a href="paths/post-training/teacher-and-context/">教师与纠错：额外信息何时能帮到学生</a><span>188 问<a class="ar-learning-deep-link" href="deep-dives/post-training/teacher-and-context/">精读对比</a></span></li>
<li><a href="paths/post-training/data-and-budget/">数据与预算：下一份算力花在哪里</a><span>152 问<a class="ar-learning-deep-link" href="deep-dives/post-training/data-and-budget/">精读对比</a></span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/agent-research/">Agent</a></h2>
<p>从下一步行动到完整执行流程：依次学习规划、记忆、工具协作、自进化、训练与独立评测。</p>
<p class="ar-learning-topic-meta">6 个子主题 · 1036 问 / 259 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/agent-research/planning-and-search/">规划与搜索：下一步该做什么</a><span>64 问<a class="ar-learning-deep-link" href="deep-dives/agent-research/planning-and-search/">精读对比</a></span></li>
<li><a href="paths/agent-research/memory-and-skills/">记忆与技能：让经验可取回、可失效</a><span>220 问<a class="ar-learning-deep-link" href="deep-dives/agent-research/memory-and-skills/">精读对比</a></span></li>
<li><a href="paths/agent-research/tools-and-collaboration/">工具与协作执行：把计划变成可检查的动作</a><span>196 问<a class="ar-learning-deep-link" href="deep-dives/agent-research/tools-and-collaboration/">精读对比</a></span></li>
<li><a href="paths/agent-research/harness-and-self-improvement/">运行流程与自进化：改的是哪一层</a><span>172 问<a class="ar-learning-deep-link" href="deep-dives/agent-research/harness-and-self-improvement/">精读对比</a></span></li>
<li><a href="paths/agent-research/agent-policy-learning/">交互策略学习：把轨迹反馈变成更新</a><span>212 问<a class="ar-learning-deep-link" href="deep-dives/agent-research/agent-policy-learning/">精读对比</a></span></li>
<li><a href="paths/agent-research/evaluation-and-reliability/">评测与可靠性：如何知道真的做对了</a><span>172 问<a class="ar-learning-deep-link" href="deep-dives/agent-research/evaluation-and-reliability/">精读对比</a></span></li>
</ul></details>
</article>
</div>

<!-- learning-topics:end -->

## 最近新增问题

新增论文和补充给旧论文的新问题，都会同时进入对应主题、全部问答和这里。

<!-- learning-recent:start -->

<div class="ar-learning-recent"><ul>
<li><a href="all/#qa-5741411042653d97">HGE为什么分别预测容器成交、内部商品购买概率和数量，而不只回归一个门店GMV？</a><span>2026-10-27 · hge</span></li>
<li><a href="all/#qa-18f65c0f1ef11458">HGE 残差与融合 gate 为什么不能按真实成交标签硬切路？</a><span>2026-10-27 · hge</span></li>
<li><a href="all/#qa-96dc7e4b12d4bae4">HGE 的商品购买 sigmoid 与互斥 softmax，为什么对应不同业务假设？</a><span>2026-10-27 · hge</span></li>
<li><a href="all/#qa-c32f38715552fb0a">HGE 的 top-K 商品是要展示的 K 个推荐结果，还是同一容器内部的输入？</a><span>2026-10-27 · hge</span></li>
<li><a href="all/#qa-36db4c81ae6babb0">OPST为什么只把学生全部匹配候选答案的题当作过易，全部一致但答成别的答案不能删？</a><span>2026-10-27 · opst</span></li>
<li><a href="all/#qa-4d8e4b8770738e55">OPST的EMA β是旧教师动量还是新学生权重？</a><span>2026-10-27 · opst</span></li>
<li><a href="all/#qa-789c0a70700a8a7a">OPST的过易过滤与简单学生共识过滤有什么差别？</a><span>2026-10-27 · opst</span></li>
<li><a href="all/#qa-f0ef826534a90cdf">OPST为什么连问题与特权线索也自生成？</a><span>2026-10-27 · opst</span></li>
</ul></div>

<!-- learning-recent:end -->

[查看全部最近新增 →](recent.md)

专题精读比较机制和假设，逐篇问答解释具体论文；原始来源与本地实验记录都可继续查阅。
