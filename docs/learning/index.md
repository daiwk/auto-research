---
hide:
  - toc
---

# 学习卡片

每次只学一个问题。从主题进入，读一张导学卡，再沿阅读路线看论文。

<div class="ar-learning-actions" markdown="1">

[搜索全部论文卡片](all.md){ .md-button .md-button--primary }
[阅读本期精选](002-rankmixer-tokenmix.md){ .md-button }

</div>

## 按主题开始

在目录的“主题与精选”中展开一个主题，单篇论文留在子主题页中查找。

<!-- learning-topics:start -->

6 个主题 · 31 张导学卡 · 1034 张论文卡

<div class="ar-learning-topics">
<article class="ar-learning-topic-tile">
<h2><a href="paths/recommendation/">搜广推</a></h2>
<p>从找候选走到排序与展示：学习语义表征、用户知识、长历史、生成式推荐、反馈与服务。</p>
<p class="ar-learning-topic-meta">7 个子主题 · 319 张论文卡</p>
<details><summary>查看子主题与导学卡</summary><ul>
<li><a href="paths/recommendation/retrieval-matching/">候选生成与搜索匹配</a><span>36</span></li>
<li><a href="paths/recommendation/content-semantic-ids/">语义表征、用户知识与冷启动</a><span>60</span></li>
<li><a href="paths/recommendation/history-ranking-backbones/">用户历史与排序骨干</a><span>73</span></li>
<li><a href="paths/recommendation/generative-retrieval-reasoning/">生成式召回与推理推荐</a><span>60</span></li>
<li><a href="paths/recommendation/feedback-multitask-causality/">学习信号、多任务与反馈偏差</a><span>35</span></li>
<li><a href="paths/recommendation/slates-business-value/">重排、展示与长期价值</a><span>36</span></li>
<li><a href="paths/recommendation/research-serving-loop/">自动研究与高效上线</a><span>19</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/foundation-models/">基础模型</a></h2>
<p>理解模型怎样读取上下文、分配计算和训练预算，以及压缩、生成与能力评测的取舍。</p>
<p class="ar-learning-topic-meta">6 个子主题 · 142 张论文卡</p>
<details><summary>查看子主题与导学卡</summary><ul>
<li><a href="paths/foundation-models/context-and-state/">长上下文：注意力、递归状态与记忆</a><span>31</span></li>
<li><a href="paths/foundation-models/conditional-compute/">按需计算：专家、弹性深宽与查表记忆</a><span>26</span></li>
<li><a href="paths/foundation-models/training-budget/">训练预算：数据配比、目标与优化器</a><span>28</span></li>
<li><a href="paths/foundation-models/compression-and-cache/">推理压缩：权重、KV 缓存与服务带宽</a><span>29</span></li>
<li><a href="paths/foundation-models/generation-paths/">生成路径：草稿验证、并行去噪与少步迭代</a><span>15</span></li>
<li><a href="paths/foundation-models/evaluation-and-evidence/">能力证据：评测采样、读出与可靠性</a><span>13</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/system-one/">结构化决策</a></h2>
<p>把语言模型用于有限候选决策：先看如何读出分布，再检验不变性、推理预算与持续反馈。</p>
<p class="ar-learning-topic-meta">3 个子主题 · 16 张论文卡</p>
<details><summary>查看子主题与导学卡</summary><ul>
<li><a href="paths/system-one/typed-readout/">类型化读出：从生成句子到候选分布</a><span>9</span></li>
<li><a href="paths/system-one/candidate-invariance/">候选不变性：顺序、竞争者与概率校准</a><span>3</span></li>
<li><a href="paths/system-one/adaptive-decisions/">按需决策：选择性推理、迁移与持续反馈</a><span>4</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/multimodal-models/">多模态</a></h2>
<p>围绕三件事学习：对齐不同模态、分配视觉证据预算、预测状态与动作的后果。</p>
<p class="ar-learning-topic-meta">3 个子主题 · 58 张论文卡</p>
<details><summary>查看子主题与导学卡</summary><ul>
<li><a href="paths/multimodal-models/alignment-interfaces/">跨模态对齐：表征、连接器与监督</a><span>20</span></li>
<li><a href="paths/multimodal-models/visual-evidence-budget/">视觉证据预算：选 Token、选帧与按需回看</a><span>16</span></li>
<li><a href="paths/multimodal-models/world-state-actions/">视觉世界建模：状态、生成与动作条件</a><span>22</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/post-training/">LLM 后训练</a></h2>
<p>先分清反馈来自哪里，再看策略更新、步骤信用、教师监督，以及数据和算力如何分配。</p>
<p class="ar-learning-topic-meta">6 个子主题 · 240 张论文卡</p>
<details><summary>查看子主题与导学卡</summary><ul>
<li><a href="paths/post-training/preference-and-alignment/">偏好与对齐：先看反馈长什么样</a><span>25</span></li>
<li><a href="paths/post-training/policy-optimization/">策略优化：谁在采样，谁在被更新</a><span>54</span></li>
<li><a href="paths/post-training/reward-and-credit/">奖励与信用：正确结果该奖励哪些步骤</a><span>36</span></li>
<li><a href="paths/post-training/student-trajectory-distillation/">在策略蒸馏：沿学生实际走过的前缀学习</a><span>40</span></li>
<li><a href="paths/post-training/teacher-and-context/">教师与纠错：额外信息何时能帮到学生</a><span>47</span></li>
<li><a href="paths/post-training/data-and-budget/">数据与预算：下一份算力花在哪里</a><span>38</span></li>
</ul></details>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="paths/agent-research/">Agent</a></h2>
<p>从下一步行动到完整执行流程：依次学习规划、记忆、工具协作、自进化、训练与独立评测。</p>
<p class="ar-learning-topic-meta">6 个子主题 · 259 张论文卡</p>
<details><summary>查看子主题与导学卡</summary><ul>
<li><a href="paths/agent-research/planning-and-search/">规划与搜索：下一步该做什么</a><span>16</span></li>
<li><a href="paths/agent-research/memory-and-skills/">记忆与技能：让经验可取回、可失效</a><span>55</span></li>
<li><a href="paths/agent-research/tools-and-collaboration/">工具与协作执行：把计划变成可检查的动作</a><span>49</span></li>
<li><a href="paths/agent-research/harness-and-self-improvement/">运行流程与自进化：改的是哪一层</a><span>43</span></li>
<li><a href="paths/agent-research/agent-policy-learning/">交互策略学习：把轨迹反馈变成更新</a><span>53</span></li>
<li><a href="paths/agent-research/evaluation-and-reliability/">评测与可靠性：如何知道真的做对了</a><span>43</span></li>
</ul></details>
</article>
</div>

<!-- learning-topics:end -->

## 本期精选

<div class="ar-learning-featured" markdown="1">

### RankMixer 的特征怎么交互？

用四行看懂 TokenMix：固定重排让特征相遇，独立 FFN 学习如何组合。

**约 3 分钟 · 特征交互 · 2026-10-26**

[阅读本期学习卡片 →](002-rankmixer-tokenmix.md){ .md-button .md-button--primary }

</div>

## 往期精选

- [001：长历史要不要每层都重新计算？](001-hstu-longer-slimper.md) — HSTU、LONGER、SlimPer，约 5 分钟。

## 查找某一篇论文

每篇已收录论文都有一张小卡片，集中展示机制摘要和本地实现边界。可以按主题、子主题筛选，或搜索论文、机构和机制。每次显示 12 张，按需继续加载；本地范围与边界可以单独展开。因成本等原因未复现的论文保留明确说明。

[浏览全部论文小卡片 →](all.md){ .md-button }

小卡片随论文实现文档同步更新，摘要摘自现有文档。新论文尚未完成主题判断时，进入[待归类的新论文](inbox.md)，不会从汇总中消失。论文公开日期用于查找资料；阅读和实验结论以卡片中的来源与边界为准。

## 怎么使用

- **只有 5 分钟**：读一期精选，想一想结尾的场景问题。
- **刚看到一篇新论文**：到小卡片汇总中搜索，先了解机制与本地做到了哪一步。
- **准备选型或做实验**：从卡片进入原论文、完整复现说明和指标。

没读过的卡片留在这里，随时查阅，无需逐篇补完。
