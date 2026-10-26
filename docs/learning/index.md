---
hide:
  - toc
---

# 论文问答

每篇论文从一个具体问题开始。先试着回答，再展开解释和教学例子；一篇论文可以继续积累多个问题。

<div class="ar-learning-actions" markdown="1">

[搜索全部问答](all.md){ .md-button .md-button--primary }
[最近新增问题](recent.md){ .md-button }

</div>

## 按主题找问题

目录支持折叠。选择子主题后，直接查看该主题所有论文的问题；主题导读与阅读路线也保留在页面中。

<!-- learning-topics:start -->

6 个主题 · 31 个子主题 · 1042 个问题 / 1034 篇论文

<div class="ar-learning-topics">
<article class="ar-learning-topic-tile">
<h2><a href="paths/recommendation/">搜广推</a></h2>
<p>从找候选走到排序与展示：学习语义表征、用户知识、长历史、生成式推荐、反馈与服务。</p>
<p class="ar-learning-topic-meta">7 个子主题 · 327 问 / 319 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/recommendation/retrieval-matching/">候选生成与搜索匹配</a><span>36 问</span></li>
<li><a href="paths/recommendation/content-semantic-ids/">语义表征、用户知识与冷启动</a><span>60 问</span></li>
<li><a href="paths/recommendation/history-ranking-backbones/">用户历史与排序骨干</a><span>81 问</span></li>
<li><a href="paths/recommendation/generative-retrieval-reasoning/">生成式召回与推理推荐</a><span>60 问</span></li>
<li><a href="paths/recommendation/feedback-multitask-causality/">学习信号、多任务与反馈偏差</a><span>35 问</span></li>
<li><a href="paths/recommendation/slates-business-value/">重排、展示与长期价值</a><span>36 问</span></li>
<li><a href="paths/recommendation/research-serving-loop/">自动研究与高效上线</a><span>19 问</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/foundation-models/">基础模型</a></h2>
<p>理解模型怎样读取上下文、分配计算和训练预算，以及压缩、生成与能力评测的取舍。</p>
<p class="ar-learning-topic-meta">6 个子主题 · 142 问 / 142 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/foundation-models/context-and-state/">长上下文：注意力、递归状态与记忆</a><span>31 问</span></li>
<li><a href="paths/foundation-models/conditional-compute/">按需计算：专家、弹性深宽与查表记忆</a><span>26 问</span></li>
<li><a href="paths/foundation-models/training-budget/">训练预算：数据配比、目标与优化器</a><span>28 问</span></li>
<li><a href="paths/foundation-models/compression-and-cache/">推理压缩：权重、KV 缓存与服务带宽</a><span>29 问</span></li>
<li><a href="paths/foundation-models/generation-paths/">生成路径：草稿验证、并行去噪与少步迭代</a><span>15 问</span></li>
<li><a href="paths/foundation-models/evaluation-and-evidence/">能力证据：评测采样、读出与可靠性</a><span>13 问</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/system-one/">结构化决策</a></h2>
<p>把语言模型用于有限候选决策：先看如何读出分布，再检验不变性、推理预算与持续反馈。</p>
<p class="ar-learning-topic-meta">3 个子主题 · 16 问 / 16 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/system-one/typed-readout/">类型化读出：从生成句子到候选分布</a><span>9 问</span></li>
<li><a href="paths/system-one/candidate-invariance/">候选不变性：顺序、竞争者与概率校准</a><span>3 问</span></li>
<li><a href="paths/system-one/adaptive-decisions/">按需决策：选择性推理、迁移与持续反馈</a><span>4 问</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/multimodal-models/">多模态</a></h2>
<p>围绕三件事学习：对齐不同模态、分配视觉证据预算、预测状态与动作的后果。</p>
<p class="ar-learning-topic-meta">3 个子主题 · 58 问 / 58 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/multimodal-models/alignment-interfaces/">跨模态对齐：表征、连接器与监督</a><span>20 问</span></li>
<li><a href="paths/multimodal-models/visual-evidence-budget/">视觉证据预算：选 Token、选帧与按需回看</a><span>16 问</span></li>
<li><a href="paths/multimodal-models/world-state-actions/">视觉世界建模：状态、生成与动作条件</a><span>22 问</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/post-training/">LLM 后训练</a></h2>
<p>先分清反馈来自哪里，再看策略更新、步骤信用、教师监督，以及数据和算力如何分配。</p>
<p class="ar-learning-topic-meta">6 个子主题 · 240 问 / 240 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/post-training/preference-and-alignment/">偏好与对齐：先看反馈长什么样</a><span>25 问</span></li>
<li><a href="paths/post-training/policy-optimization/">策略优化：谁在采样，谁在被更新</a><span>54 问</span></li>
<li><a href="paths/post-training/reward-and-credit/">奖励与信用：正确结果该奖励哪些步骤</a><span>36 问</span></li>
<li><a href="paths/post-training/student-trajectory-distillation/">在策略蒸馏：沿学生实际走过的前缀学习</a><span>40 问</span></li>
<li><a href="paths/post-training/teacher-and-context/">教师与纠错：额外信息何时能帮到学生</a><span>47 问</span></li>
<li><a href="paths/post-training/data-and-budget/">数据与预算：下一份算力花在哪里</a><span>38 问</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/agent-research/">Agent</a></h2>
<p>从下一步行动到完整执行流程：依次学习规划、记忆、工具协作、自进化、训练与独立评测。</p>
<p class="ar-learning-topic-meta">6 个子主题 · 259 问 / 259 篇</p>
<details><summary>展开子主题问题库</summary><ul>
<li><a href="paths/agent-research/planning-and-search/">规划与搜索：下一步该做什么</a><span>16 问</span></li>
<li><a href="paths/agent-research/memory-and-skills/">记忆与技能：让经验可取回、可失效</a><span>55 问</span></li>
<li><a href="paths/agent-research/tools-and-collaboration/">工具与协作执行：把计划变成可检查的动作</a><span>49 问</span></li>
<li><a href="paths/agent-research/harness-and-self-improvement/">运行流程与自进化：改的是哪一层</a><span>43 问</span></li>
<li><a href="paths/agent-research/agent-policy-learning/">交互策略学习：把轨迹反馈变成更新</a><span>53 问</span></li>
<li><a href="paths/agent-research/evaluation-and-reliability/">评测与可靠性：如何知道真的做对了</a><span>43 问</span></li>
</ul></details>
</article>
</div>

<!-- learning-topics:end -->

## 最近新增问题

新增论文和补充给旧论文的新问题，都会同时进入对应主题、全部问答和这里。

<!-- learning-recent:start -->

<div class="ar-learning-recent"><ul>
<li><a href="all/#qa-5741411042653d97">HGE为什么分别预测容器成交、内部商品购买概率和数量，而不只回归一个门店GMV？</a><span>2026-10-27 · hge</span></li>
<li><a href="all/#qa-36db4c81ae6babb0">OPST为什么只把学生全部匹配候选答案的题当作过易，全部一致但答成别的答案不能删？</a><span>2026-10-27 · opst</span></li>
<li><a href="all/#qa-e7694d8cca75156c">MART-GRPO屏蔽最后未恢复错误之后的惩罚，为什么不重新算组优势或有效token分母？</a><span>2026-10-27 · mart-grpo</span></li>
<li><a href="all/#qa-32b91700ff0ec00d">为什么给 action logits 加 log(Nref/Na)，能抵消完全复制动作 Token 带来的注意力总权重变化？</a><span>2026-10-27 · uniaction</span></li>
<li><a href="all/#qa-c8472fbb022dc303">FlexGlue 为什么只在峰值附近的局部窗口读坐标，而不对全图坐标求期望？</a><span>2026-10-27 · flexglue</span></li>
<li><a href="all/#qa-2dc91c86955e14a5">PathJev的重要贡献为什么不能缩成病理图像上接一个softmax？</a><span>2026-10-27 · pathjev</span></li>
<li><a href="all/#qa-4d16236f11c750b3">EditJev离线要运行所有编辑器，为什么推理时却只运行被选中的一个？</a><span>2026-10-27 · editjev</span></li>
<li><a href="all/#qa-07079ed5e9b5243c">为什么未来 latent 要由历史预测，而真实未来只交给训练期的目标编码器？</a><span>2026-10-27 · dt-jepa</span></li>
</ul></div>

<!-- learning-recent:end -->

[查看全部最近新增 →](recent.md)

## 专题串读

需要把几篇论文放在一起比较时，可以阅读专题串讲。

- [长历史要不要每层都重新计算？](001-hstu-longer-slimper.md) — HSTU、LONGER、SlimPer。
- [RankMixer 的特征怎么交互？](002-rankmixer-tokenmix.md) — 四行看懂 TokenMix。

问答讲解论文机制，教学例子用来帮助理解。原始论文和实现解读都保留来源链接，实验结论以各自记录为准。
