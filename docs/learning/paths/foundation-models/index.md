<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 基础模型

理解模型怎样读取上下文、分配计算和训练预算，以及压缩、生成与能力评测的取舍。

选择一个子主题，从具体论文问题开始。新论文和新增问题会继续加入对应问题库。

<div class="ar-learning-topics">
<article class="ar-learning-topic-tile">
<h2><a href="context-and-state/">长上下文：注意力、递归状态与记忆</a></h2>
<p>上下文变长时，模型保留的是可寻址的历史 token，还是压缩后的递归状态？</p>
<p class="ar-learning-topic-meta">124 个问题 · 31 篇论文</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="conditional-compute/">按需计算：专家、弹性深宽与查表记忆</a></h2>
<p>同一参数预算下，每个 token 应该激活哪些参数、运行多少步？</p>
<p class="ar-learning-topic-meta">104 个问题 · 26 篇论文</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="training-budget/">训练预算：数据配比、目标与优化器</a></h2>
<p>有限训练预算应该先改数据、更新方向，还是模型规模？</p>
<p class="ar-learning-topic-meta">112 个问题 · 28 篇论文</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="compression-and-cache/">推理压缩：权重、KV 缓存与服务带宽</a></h2>
<p>显存或时延不够时，真正占资源的是模型权重、历史状态，还是服务搬运？</p>
<p class="ar-learning-topic-meta">116 个问题 · 29 篇论文</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="generation-paths/">生成路径：草稿验证、并行去噪与少步迭代</a></h2>
<p>如何减少逐 token 串行生成的等待，同时说清输出分布是否改变？</p>
<p class="ar-learning-topic-meta">60 个问题 · 15 篇论文</p>
</article>
<article class="ar-learning-topic-tile">
<h2><a href="evaluation-and-evidence/">能力证据：评测采样、读出与可靠性</a></h2>
<p>怎样确认高分来自目标能力，而非语言、输入顺序、读出方式或统计偏差？</p>
<p class="ar-learning-topic-meta">52 个问题 · 13 篇论文</p>
</article>
</div>

[返回全部主题](../../index.md)
