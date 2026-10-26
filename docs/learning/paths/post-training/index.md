<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# LLM 后训练

先分清反馈来自哪里，再看策略更新、步骤信用、教师监督，以及数据和算力如何分配。

每次选一个问题，先读导学卡，再按阅读顺序看代表论文。

<div class="ar-learning-topics">
<article class="ar-learning-topic-tile">
<h2><a href="preference-and-alignment/">偏好与对齐：先看反馈长什么样</a></h2>
<p>只有“更喜欢哪个回答”或单条点赞时，怎样把反馈变成可学习目标？</p>
<p class="ar-learning-topic-meta">导学约 3 分钟 · 25 张论文卡</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="policy-optimization/">策略优化：谁在采样，谁在被更新</a></h2>
<p>在线采样、旧策略概率与当前策略更新之间，哪些量必须分开？</p>
<p class="ar-learning-topic-meta">导学约 3 分钟 · 54 张论文卡</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="reward-and-credit/">奖励与信用：正确结果该奖励哪些步骤</a></h2>
<p>一个最终分数，怎样转成不会奖励错误步骤的训练信号？</p>
<p class="ar-learning-topic-meta">导学约 3 分钟 · 36 张论文卡</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="student-trajectory-distillation/">在策略蒸馏：沿学生实际走过的前缀学习</a></h2>
<p>学生总在自己的错误前缀上继续生成，为什么只模仿教师完整答案可能教不到那里？</p>
<p class="ar-learning-topic-meta">导学约 3 分钟 · 40 张论文卡</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="teacher-and-context/">教师与纠错：额外信息何时能帮到学生</a></h2>
<p>教师看到了答案、图像证据或专长提示，怎样把帮助传给没有这些信息的学生？</p>
<p class="ar-learning-topic-meta">导学约 3 分钟 · 47 张论文卡</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="data-and-budget/">数据与预算：下一份算力花在哪里</a></h2>
<p>预算有限时，应该多生成问题、多做rollout，还是把监督集中在更有价值的位置？</p>
<p class="ar-learning-topic-meta">导学约 3 分钟 · 38 张论文卡</p>
</article>
</div>

[返回全部主题](../../index.md)
