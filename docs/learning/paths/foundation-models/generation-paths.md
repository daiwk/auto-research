---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 生成路径：草稿验证、并行去噪与少步迭代

[基础模型](index.md) / 60 个问题 · 15 篇论文

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
<p class="ar-learning-status" data-learning-status role="status">60 个问题 · 15 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:langdit" data-paper-title="Designing Transformers for Continuous Diffusion Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Designing Transformers for Continuous Diffusion Language Models 基础模型 Dots Studio, Xiaohongshu 2026-10-15 连续扩散语言模型要从带高斯噪声的 token 嵌入恢复离散分布。原文§3把架构改动分为三个位置：backbone 的 RMS/QK 归一与噪声条件容量；词表 likelihood shortcut 的显式码本梯度路由和有界校准；训练期 bootstrap self-conditioning 的置信度衰减。LangFlow 的表示、交叉熵和采样器保持不变；Plaid 适配只迁移兼容子集，不能把两套梯度规则混为一谈。 成本过高，不复现（审查 DONE）。修复后已重新在 A100 覆盖四种极值及梯度检查，诊断记录与GPU回执绑定最终执行源码。无公开大数据/模型下载。revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1，seeds42/43/44。实际微型 denoiser 为2层、16维、2 heads、19词，保留球面码本、RMS/QK归一、RoPE、噪声条件残差门、未绑定词表head、零初始化输入融合和校准。  扩散语言模型 噪声条件与自条件 基础模型 生成路径：草稿验证、并行去噪与少步迭代 LangDiT 为什么在连续 noisy embedding 之外增加 likelihood shortcut？ 它用码本与带噪状态的关系补充词表后验，并配合噪声条件backbone和有界校准。离散恢复不只依赖一个普通输出head，梯度路由与训练自条件也需对应具体分支。 示意：噪声较低时，当前状态接近哪些词的码本向量，可作为恢复token的一条额外线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-langdit-ba73a77f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e37db734cbc08d6b">LangDiT 为什么在连续 noisy embedding 之外增加 likelihood shortcut？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alangdit">Designing Transformers for Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dots Studio, Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用码本与带噪状态的关系补充词表后验，并配合噪声条件backbone和有界校准。离散恢复不只依赖一个普通输出head，梯度路由与训练自条件也需对应具体分支。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>噪声较低时，当前状态接近哪些词的码本向量，可作为恢复token的一条额外线索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22330">原论文</a> · <a href="../../../../foundation-models/2610.22330-langdit/">实现解读</a> · <a href="#qa-e37db734cbc08d6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:langdit" data-paper-title="Designing Transformers for Continuous Diffusion Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Designing Transformers for Continuous Diffusion Language Models 基础模型 Dots Studio, Xiaohongshu 2026-10-15 连续扩散语言模型要从带高斯噪声的 token 嵌入恢复离散分布。原文§3把架构改动分为三个位置：backbone 的 RMS/QK 归一与噪声条件容量；词表 likelihood shortcut 的显式码本梯度路由和有界校准；训练期 bootstrap self-conditioning 的置信度衰减。LangFlow 的表示、交叉熵和采样器保持不变；Plaid 适配只迁移兼容子集，不能把两套梯度规则混为一谈。 成本过高，不复现（审查 DONE）。修复后已重新在 A100 覆盖四种极值及梯度检查，诊断记录与GPU回执绑定最终执行源码。无公开大数据/模型下载。revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1，seeds42/43/44。实际微型 denoiser 为2层、16维、2 heads、19词，保留球面码本、RMS/QK归一、RoPE、噪声条件残差门、未绑定词表head、零初始化输入融合和校准。  扩散语言模型 噪声条件与自条件 基础模型 生成路径：草稿验证、并行去噪与少步迭代 LangDiT为什么只detach似然shortcut中的显式码本，而不把带噪输入整体detach？ 显式shortcut与输入构造共享码本，切断前者可控制该路径的梯度，码本仍应通过带噪输入路径学习；整体detach会错误阻断这条训练关系。训练期自条件用熵衰减不可靠反馈，推理却使用未加权后验均值，不能把训练门控直接搬到采样器。 例如同一张词向量表既生成带噪输入又参与快捷打分，只冻结快捷乘法的一侧；把输入也冻结，会让本来应学习的码本通路消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-999cd9aaee6ecf4c">LangDiT为什么只detach似然shortcut中的显式码本，而不把带噪输入整体detach？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alangdit">Designing Transformers for Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dots Studio, Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>显式shortcut与输入构造共享码本，切断前者可控制该路径的梯度，码本仍应通过带噪输入路径学习；整体detach会错误阻断这条训练关系。训练期自条件用熵衰减不可靠反馈，推理却使用未加权后验均值，不能把训练门控直接搬到采样器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一张词向量表既生成带噪输入又参与快捷打分，只冻结快捷乘法的一侧；把输入也冻结，会让本来应学习的码本通路消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22330">原论文</a> · <a href="../../../../foundation-models/2610.22330-langdit/">实现解读</a> · <a href="#qa-999cd9aaee6ecf4c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:langdit" data-paper-title="Designing Transformers for Continuous Diffusion Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Designing Transformers for Continuous Diffusion Language Models 基础模型 Dots Studio, Xiaohongshu 2026-10-15 连续扩散语言模型要从带高斯噪声的 token 嵌入恢复离散分布。原文§3把架构改动分为三个位置：backbone 的 RMS/QK 归一与噪声条件容量；词表 likelihood shortcut 的显式码本梯度路由和有界校准；训练期 bootstrap self-conditioning 的置信度衰减。LangFlow 的表示、交叉熵和采样器保持不变；Plaid 适配只迁移兼容子集，不能把两套梯度规则混为一谈。 成本过高，不复现（审查 DONE）。修复后已重新在 A100 覆盖四种极值及梯度检查，诊断记录与GPU回执绑定最终执行源码。无公开大数据/模型下载。revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1，seeds42/43/44。实际微型 denoiser 为2层、16维、2 heads、19词，保留球面码本、RMS/QK归一、RoPE、噪声条件残差门、未绑定词表head、零初始化输入融合和校准。  扩散语言模型 噪声条件与自条件 基础模型 生成路径：草稿验证、并行去噪与少步迭代 LangDiT 的训练 entropy gate，与推理后验均值应使用同样权重吗？ 文档训练bootstrap按置信度衰减并stop-gradient，推理使用未加权后验均值pC，不额外bootstrap。训练启发式不是更优后验估计保证，不能直接移到推理阶段。 示意：训练时低置信反馈被减弱，不代表推理时也把同样的概率质量再次打折。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-11b5da4d78a813dc">LangDiT 的训练 entropy gate，与推理后验均值应使用同样权重吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alangdit">Designing Transformers for Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dots Studio, Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档训练bootstrap按置信度衰减并stop-gradient，推理使用未加权后验均值pC，不额外bootstrap。训练启发式不是更优后验估计保证，不能直接移到推理阶段。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时低置信反馈被减弱，不代表推理时也把同样的概率质量再次打折。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22330">原论文</a> · <a href="../../../../foundation-models/2610.22330-langdit/">实现解读</a> · <a href="#qa-11b5da4d78a813dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:langdit" data-paper-title="Designing Transformers for Continuous Diffusion Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Designing Transformers for Continuous Diffusion Language Models 基础模型 Dots Studio, Xiaohongshu 2026-10-15 连续扩散语言模型要从带高斯噪声的 token 嵌入恢复离散分布。原文§3把架构改动分为三个位置：backbone 的 RMS/QK 归一与噪声条件容量；词表 likelihood shortcut 的显式码本梯度路由和有界校准；训练期 bootstrap self-conditioning 的置信度衰减。LangFlow 的表示、交叉熵和采样器保持不变；Plaid 适配只迁移兼容子集，不能把两套梯度规则混为一谈。 成本过高，不复现（审查 DONE）。修复后已重新在 A100 覆盖四种极值及梯度检查，诊断记录与GPU回执绑定最终执行源码。无公开大数据/模型下载。revision synthetic-packed-options-and-noisy-tokens@oct17-supplement-foundation-v1，seeds42/43/44。实际微型 denoiser 为2层、16维、2 heads、19词，保留球面码本、RMS/QK归一、RoPE、噪声条件残差门、未绑定词表head、零初始化输入融合和校准。  扩散语言模型 噪声条件与自条件 基础模型 生成路径：草稿验证、并行去噪与少步迭代 LangDiT 校准 aψ 为什么既要初始化为1，又限制到[0.5,2]？ 初始化为1保留初始shortcut尺度，有界指数校准避免无约束放大或缩小；文档还保留前5000步warmup。实现应检查实际范围与梯度路径，不能换成无界任意系数后称相同配置。 示意：校准网络输出很大时仍须被clip限制，而不是令shortcut压过整个词表head。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a19870609b8abb9b">LangDiT 校准 aψ 为什么既要初始化为1，又限制到[0.5,2]？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alangdit">Designing Transformers for Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dots Studio, Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>初始化为1保留初始shortcut尺度，有界指数校准避免无约束放大或缩小；文档还保留前5000步warmup。实现应检查实际范围与梯度路径，不能换成无界任意系数后称相同配置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>校准网络输出很大时仍须被clip限制，而不是令shortcut压过整个词表head。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22330">原论文</a> · <a href="../../../../foundation-models/2610.22330-langdit/">实现解读</a> · <a href="#qa-a19870609b8abb9b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doublecat-semicat" data-paper-title="On the Design Space of Continuous Diffusion Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On the Design Space of Continuous Diffusion Language Models 基础模型 University of Oxford / Apple（在 Apple 期间完成） 2026-10-09 One-hot continuous flow 在接近终点时训练几乎只看见低熵顶点，但推理跟随有熵 denoiser 概率，产生轨迹错配。DoubleCat 在高斯路径内部再插入 simplex prior 到 one-hot 的插值，把训练质量移到更像推理的 simplex 内部。另一个问题是高维高斯噪声范数约，而 one-hot 信号范数仅为 1，已有 token 难以辨识。 cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。三模型参数 L2 变化分别约 0.1345；  扩散语言模型 Self-conditioning 基础模型 生成路径：草稿验证、并行去噪与少步迭代 SemiCat 为什么把一部分 token 提前 reveal 成干净 one-hot？ 高维高斯噪声范数较大，而one-hot信号范数为1，token身份可能难辨。随机reveal让部分位置成为稳定离散锚点并永久保留，训练只监督尚未reveal的位置。 示意：已确认的词保持干净可见，剩余位置继续去噪，不再把确认词重新加噪。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-doublecat-semicat-01018306" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5c0323d9b9c7012e">SemiCat 为什么把一部分 token 提前 reveal 成干净 one-hot？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoublecat-semicat">On the Design Space of Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Oxford / Apple（在 Apple 期间完成）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高维高斯噪声范数较大，而one-hot信号范数为1，token身份可能难辨。随机reveal让部分位置成为稳定离散锚点并永久保留，训练只监督尚未reveal的位置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>已确认的词保持干净可见，剩余位置继续去噪，不再把确认词重新加噪。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13834">原论文</a> · <a href="../../../../reproductions/2610.13834-doublecat-semicat/">实现解读</a> · <a href="#qa-5c0323d9b9c7012e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doublecat-semicat" data-paper-title="On the Design Space of Continuous Diffusion Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On the Design Space of Continuous Diffusion Language Models 基础模型 University of Oxford / Apple（在 Apple 期间完成） 2026-10-09 One-hot continuous flow 在接近终点时训练几乎只看见低熵顶点，但推理跟随有熵 denoiser 概率，产生轨迹错配。DoubleCat 在高斯路径内部再插入 simplex prior 到 one-hot 的插值，把训练质量移到更像推理的 simplex 内部。另一个问题是高维高斯噪声范数约，而 one-hot 信号范数仅为 1，已有 token 难以辨识。 cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。三模型参数 L2 变化分别约 0.1345；  扩散语言模型 Self-conditioning 基础模型 生成路径：草稿验证、并行去噪与少步迭代 DoubleCat的双层插值与SemiCat的永久reveal，为什么是两个不同的修正？ 双层插值把训练分布移向更接近推理的单纯形内部，缓解低熵端点错配；永久揭示则让已确定词元成为干净信号，不再被高维噪声淹没。后者只监督未揭示位置并保持已揭示结果，条件揭示概率需随剩余时间调整，两者也不默认增加自条件前向。 例如一句话里已确定的主语可永久保留，其他位置继续去噪；训练输入中模拟有熵概率结构，则是在解决另一种轨迹分布差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d81c0b5a5fbc8665">DoubleCat的双层插值与SemiCat的永久reveal，为什么是两个不同的修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoublecat-semicat">On the Design Space of Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Oxford / Apple（在 Apple 期间完成）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>双层插值把训练分布移向更接近推理的单纯形内部，缓解低熵端点错配；永久揭示则让已确定词元成为干净信号，不再被高维噪声淹没。后者只监督未揭示位置并保持已揭示结果，条件揭示概率需随剩余时间调整，两者也不默认增加自条件前向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一句话里已确定的主语可永久保留，其他位置继续去噪；训练输入中模拟有熵概率结构，则是在解决另一种轨迹分布差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13834">原论文</a> · <a href="../../../../reproductions/2610.13834-doublecat-semicat/">实现解读</a> · <a href="#qa-d81c0b5a5fbc8665">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doublecat-semicat" data-paper-title="On the Design Space of Continuous Diffusion Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On the Design Space of Continuous Diffusion Language Models 基础模型 University of Oxford / Apple（在 Apple 期间完成） 2026-10-09 One-hot continuous flow 在接近终点时训练几乎只看见低熵顶点，但推理跟随有熵 denoiser 概率，产生轨迹错配。DoubleCat 在高斯路径内部再插入 simplex prior 到 one-hot 的插值，把训练质量移到更像推理的 simplex 内部。另一个问题是高维高斯噪声范数约，而 one-hot 信号范数仅为 1，已有 token 难以辨识。 cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。三模型参数 L2 变化分别约 0.1345；  扩散语言模型 Self-conditioning 基础模型 生成路径：草稿验证、并行去噪与少步迭代 DoubleCat 双层插值是否等于训练时多跑一次 denoiser 做 self-conditioning？ 不是。双层插值本身不调用denoiser来构造输入，SemiCat也不要求额外SC前向。标准bootstrap SC是可另开消融，开启时额外调用必须计入，不能把它混进默认同预算结果。 示意：一次优化默认只做一次真实模型前向，不能隐藏第二次bootstrap调用的成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-102a07e552e2b869">DoubleCat 双层插值是否等于训练时多跑一次 denoiser 做 self-conditioning？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoublecat-semicat">On the Design Space of Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Oxford / Apple（在 Apple 期间完成）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。双层插值本身不调用denoiser来构造输入，SemiCat也不要求额外SC前向。标准bootstrap SC是可另开消融，开启时额外调用必须计入，不能把它混进默认同预算结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次优化默认只做一次真实模型前向，不能隐藏第二次bootstrap调用的成本。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13834">原论文</a> · <a href="../../../../reproductions/2610.13834-doublecat-semicat/">实现解读</a> · <a href="#qa-102a07e552e2b869">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doublecat-semicat" data-paper-title="On the Design Space of Continuous Diffusion Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On the Design Space of Continuous Diffusion Language Models 基础模型 University of Oxford / Apple（在 Apple 期间完成） 2026-10-09 One-hot continuous flow 在接近终点时训练几乎只看见低熵顶点，但推理跟随有熵 denoiser 概率，产生轨迹错配。DoubleCat 在高斯路径内部再插入 simplex prior 到 one-hot 的插值，把训练质量移到更像推理的 simplex 内部。另一个问题是高维高斯噪声范数约，而 one-hot 信号范数仅为 1，已有 token 难以辨识。 cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。cpu-diagnostic-seed42.json保留先前 byte-dit-v1 的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 诊断：当时默认标准 SC 开启，且未采用 Appendix E.1 L2 weighting，不能代表当前无额外前向核心协议。三模型参数 L2 变化分别约 0.1345；  扩散语言模型 Self-conditioning 基础模型 生成路径：草稿验证、并行去噪与少步迭代 SemiCat 最后一步 hazard 为1与永久 carry-over，应如何一起检查？ 最后一步要保证所有剩余位置reveal；已经reveal的位置输入与输出始终保留。连续Euler使用未温调概率，categorical commit才用温度，三处规则不能互换。 示意：某词第2步已reveal，第3步不得因新采样又改成另一词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6986d7d1c325c468">SemiCat 最后一步 hazard 为1与永久 carry-over，应如何一起检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoublecat-semicat">On the Design Space of Continuous Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Oxford / Apple（在 Apple 期间完成）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最后一步要保证所有剩余位置reveal；已经reveal的位置输入与输出始终保留。连续Euler使用未温调概率，categorical commit才用温度，三处规则不能互换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某词第2步已reveal，第3步不得因新采样又改成另一词。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13834">原论文</a> · <a href="../../../../reproductions/2610.13834-doublecat-semicat/">实现解读</a> · <a href="#qa-6986d7d1c325c468">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-space-iteration" data-paper-title="Few-Step Generation via Data-Space Iteration" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Few-Step Generation via Data-Space Iteration 基础模型 ByteDance Seed 2026-10-08 常规 few-step flow generator 需要预设时间离散化，每步在加噪/去噪轨迹上前进。Data-Space Iteration 改为固定同一份噪声，用共享网络反复改进数据预测；每步 index 只表示 refinement，不是 flow time。训练沿用 distribution matching distillation：真实冻结 teacher 与逐步拟合生成分布的 fake 给出方向，前缀 rollout 无梯度，仅当前 refinement 更新 generator。 本地定位：L1 实际训练核心机制诊断。本地定位：L1 实际训练核心机制诊断。已在真实 A100 从公开图像训练 flow teacher，再执行冻结 teacher、可训练 fake model 与共享 generator 的交替 DMD；不是随机教师、固定合成 reward 或只画迭代示意图。三个种子有正有负，不能宣称稳定质量提升。安装实际运行依赖（包含距离计算所需的 SciPy）：python -m pip install -e &#x27;.[data-space-gpu]&#x27;。  生成模型 少步生成与蒸馏 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Data-Space Iteration 反复更新的是数据预测，还是噪声时间轨迹？ 它固定同一份原始噪声，用共享网络逐次改进数据预测；迭代编号表示refinement而非flow time。训练仍有用于DMD的加噪时间τ，不能把这两个变量混为一项。 示意：第3次精炼不意味着一定走到噪声日程的t=3，而是对同一噪声的预测再改一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-data-space-iteration-cef25f24" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-48133a6bbe3428ba">Data-Space Iteration 反复更新的是数据预测，还是噪声时间轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-space-iteration">Few-Step Generation via Data-Space Iteration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它固定同一份原始噪声，用共享网络逐次改进数据预测；迭代编号表示refinement而非flow time。训练仍有用于DMD的加噪时间τ，不能把这两个变量混为一项。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第3次精炼不意味着一定走到噪声日程的t=3，而是对同一噪声的预测再改一次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12102">原论文</a> · <a href="../../../../foundation-models/2610.12102-data-space-iteration/">实现解读</a> · <a href="#qa-48133a6bbe3428ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-space-iteration" data-paper-title="Few-Step Generation via Data-Space Iteration" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Few-Step Generation via Data-Space Iteration 基础模型 ByteDance Seed 2026-10-08 常规 few-step flow generator 需要预设时间离散化，每步在加噪/去噪轨迹上前进。Data-Space Iteration 改为固定同一份噪声，用共享网络反复改进数据预测；每步 index 只表示 refinement，不是 flow time。训练沿用 distribution matching distillation：真实冻结 teacher 与逐步拟合生成分布的 fake 给出方向，前缀 rollout 无梯度，仅当前 refinement 更新 generator。 本地定位：L1 实际训练核心机制诊断。本地定位：L1 实际训练核心机制诊断。已在真实 A100 从公开图像训练 flow teacher，再执行冻结 teacher、可训练 fake model 与共享 generator 的交替 DMD；不是随机教师、固定合成 reward 或只画迭代示意图。三个种子有正有负，不能宣称稳定质量提升。安装实际运行依赖（包含距离计算所需的 SciPy）：python -m pip install -e &#x27;.[data-space-gpu]&#x27;。  生成模型 少步生成与蒸馏 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Data-Space Iteration为什么固定同一噪声反复改进预测，而不把迭代编号当flow时间？ 共享生成器在数据空间逐步修正同一预测，编号表示细化轮次，原始噪声保持不变。训练仍用真实教师与拟合生成分布的假模型给出DMD方向，前缀无梯度，仅当前细化更新；不是每轮直接回归真实图片。本地微型实验不能替代原文大规模图像指标。 例如从同一个噪声起点先画轮廓再修细节，后一步利用前一步预测；若每轮换噪声或随意当作新的扩散时间，就改变了迭代机制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-039b91ebbdf6cbe4">Data-Space Iteration为什么固定同一噪声反复改进预测，而不把迭代编号当flow时间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-space-iteration">Few-Step Generation via Data-Space Iteration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享生成器在数据空间逐步修正同一预测，编号表示细化轮次，原始噪声保持不变。训练仍用真实教师与拟合生成分布的假模型给出DMD方向，前缀无梯度，仅当前细化更新；不是每轮直接回归真实图片。本地微型实验不能替代原文大规模图像指标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从同一个噪声起点先画轮廓再修细节，后一步利用前一步预测；若每轮换噪声或随意当作新的扩散时间，就改变了迭代机制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12102">原论文</a> · <a href="../../../../foundation-models/2610.12102-data-space-iteration/">实现解读</a> · <a href="#qa-039b91ebbdf6cbe4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-space-iteration" data-paper-title="Few-Step Generation via Data-Space Iteration" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Few-Step Generation via Data-Space Iteration 基础模型 ByteDance Seed 2026-10-08 常规 few-step flow generator 需要预设时间离散化，每步在加噪/去噪轨迹上前进。Data-Space Iteration 改为固定同一份噪声，用共享网络反复改进数据预测；每步 index 只表示 refinement，不是 flow time。训练沿用 distribution matching distillation：真实冻结 teacher 与逐步拟合生成分布的 fake 给出方向，前缀 rollout 无梯度，仅当前 refinement 更新 generator。 本地定位：L1 实际训练核心机制诊断。本地定位：L1 实际训练核心机制诊断。已在真实 A100 从公开图像训练 flow teacher，再执行冻结 teacher、可训练 fake model 与共享 generator 的交替 DMD；不是随机教师、固定合成 reward 或只画迭代示意图。三个种子有正有负，不能宣称稳定质量提升。安装实际运行依赖（包含距离计算所需的 SciPy）：python -m pip install -e &#x27;.[data-space-gpu]&#x27;。  生成模型 少步生成与蒸馏 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Data-space generator 直接回归真实图片，与文档中的 DMD 训练等价吗？ 不等价。DMD由真实冻结teacher与拟合生成分布的fake给出方向，generator利用这条分布匹配信号；直接以真实图片作每步回归target会替换定义性训练链路。 示意：生成样本上的teacher−fake方向，不是给每个随机噪声预先配一张真实图片。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e76cd9b0d0ef4e4b">Data-space generator 直接回归真实图片，与文档中的 DMD 训练等价吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-space-iteration">Few-Step Generation via Data-Space Iteration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等价。DMD由真实冻结teacher与拟合生成分布的fake给出方向，generator利用这条分布匹配信号；直接以真实图片作每步回归target会替换定义性训练链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成样本上的teacher−fake方向，不是给每个随机噪声预先配一张真实图片。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12102">原论文</a> · <a href="../../../../foundation-models/2610.12102-data-space-iteration/">实现解读</a> · <a href="#qa-e76cd9b0d0ef4e4b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-space-iteration" data-paper-title="Few-Step Generation via Data-Space Iteration" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Few-Step Generation via Data-Space Iteration 基础模型 ByteDance Seed 2026-10-08 常规 few-step flow generator 需要预设时间离散化，每步在加噪/去噪轨迹上前进。Data-Space Iteration 改为固定同一份噪声，用共享网络反复改进数据预测；每步 index 只表示 refinement，不是 flow time。训练沿用 distribution matching distillation：真实冻结 teacher 与逐步拟合生成分布的 fake 给出方向，前缀 rollout 无梯度，仅当前 refinement 更新 generator。 本地定位：L1 实际训练核心机制诊断。本地定位：L1 实际训练核心机制诊断。已在真实 A100 从公开图像训练 flow teacher，再执行冻结 teacher、可训练 fake model 与共享 generator 的交替 DMD；不是随机教师、固定合成 reward 或只画迭代示意图。三个种子有正有负，不能宣称稳定质量提升。安装实际运行依赖（包含距离计算所需的 SciPy）：python -m pip install -e &#x27;.[data-space-gpu]&#x27;。  生成模型 少步生成与蒸馏 基础模型 生成路径：草稿验证、并行去噪与少步迭代 一次 refinement 更新中，prefix、fake 和 generator 的梯度边界如何区分？ 前缀rollout不建梯度图，仅优化当前最后一步；fake训练使用detach的生成样本，generator训练时teacher/fake不积累梯度，方向stop-gradient。把全部步骤连起来反传是另一种训练配置。 示意：第4步更新generator时，不能顺手把前3步和冻结teacher都当成可训练路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-718c6f2b28293a39">一次 refinement 更新中，prefix、fake 和 generator 的梯度边界如何区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-space-iteration">Few-Step Generation via Data-Space Iteration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前缀rollout不建梯度图，仅优化当前最后一步；fake训练使用detach的生成样本，generator训练时teacher/fake不积累梯度，方向stop-gradient。把全部步骤连起来反传是另一种训练配置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第4步更新generator时，不能顺手把前3步和冻结teacher都当成可训练路径。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12102">原论文</a> · <a href="../../../../foundation-models/2610.12102-data-space-iteration/">实现解读</a> · <a href="#qa-718c6f2b28293a39">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pumba" data-paper-title="On Trajectory-Aware Training for Masked Diffusion Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On Trajectory-Aware Training for Masked Diffusion Language Models 基础模型 Apple 2026-09-29 训练时沿模型自己的 progressive-unmasking 轨迹连续展开多个 denoising step，把隐藏 carry 传给下一步，并在固定窗口内通过时间反向传播，使前一步学会产生对后续有用的 carry。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Trajectory-aware training BPTT 基础模型 生成路径：草稿验证、并行去噪与少步迭代 PUMBA 为什么使用模型自己的 progressive-unmasking 训练轨迹？ 独立随机噪声样本不一定覆盖模型实际多步去噪会遇到的状态。沿自身轨迹展开并传递carry，使训练面对连续决策及前一步为后一步留下的表示。 示意：前一步揭示了某些词后，下一步看到的状态由模型自己决定，而非重新随机造一份无关噪声。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-pumba-d6ea4c98" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-142bd7ecbfaa617c">PUMBA 为什么使用模型自己的 progressive-unmasking 训练轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apumba">On Trajectory-Aware Training for Masked Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立随机噪声样本不一定覆盖模型实际多步去噪会遇到的状态。沿自身轨迹展开并传递carry，使训练面对连续决策及前一步为后一步留下的表示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>前一步揭示了某些词后，下一步看到的状态由模型自己决定，而非重新随机造一份无关噪声。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37974">原论文</a> · <a href="../../../../foundation-models/2609.37974-pumba/">实现解读</a> · <a href="#qa-142bd7ecbfaa617c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pumba" data-paper-title="On Trajectory-Aware Training for Masked Diffusion Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On Trajectory-Aware Training for Masked Diffusion Language Models 基础模型 Apple 2026-09-29 训练时沿模型自己的 progressive-unmasking 轨迹连续展开多个 denoising step，把隐藏 carry 传给下一步，并在固定窗口内通过时间反向传播，使前一步学会产生对后续有用的 carry。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Trajectory-aware training BPTT 基础模型 生成路径：草稿验证、并行去噪与少步迭代 PUMBA为什么要让梯度穿过多个去噪步骤的carry，而不把每步当独立训练样本？ 隐藏carry会影响后续去噪，独立训练只要求当前步预测好，未必鼓励它留下对下一步有用的状态。沿模型自身逐步揭示轨迹展开，在固定窗口内反传，可让早期carry承担后续损失；窗口间仍截断，以限制成本。本地未训练完整扩散语言模型。 例如前一步留下某种实体约束，后一步据此填空，后一步误差应能指导前一步如何编码约束；每步都detach会丢掉这种关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-295de760f5896ce6">PUMBA为什么要让梯度穿过多个去噪步骤的carry，而不把每步当独立训练样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apumba">On Trajectory-Aware Training for Masked Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>隐藏carry会影响后续去噪，独立训练只要求当前步预测好，未必鼓励它留下对下一步有用的状态。沿模型自身逐步揭示轨迹展开，在固定窗口内反传，可让早期carry承担后续损失；窗口间仍截断，以限制成本。本地未训练完整扩散语言模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前一步留下某种实体约束，后一步据此填空，后一步误差应能指导前一步如何编码约束；每步都detach会丢掉这种关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37974">原论文</a> · <a href="../../../../foundation-models/2609.37974-pumba/">实现解读</a> · <a href="#qa-295de760f5896ce6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pumba" data-paper-title="On Trajectory-Aware Training for Masked Diffusion Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On Trajectory-Aware Training for Masked Diffusion Language Models 基础模型 Apple 2026-09-29 训练时沿模型自己的 progressive-unmasking 轨迹连续展开多个 denoising step，把隐藏 carry 传给下一步，并在固定窗口内通过时间反向传播，使前一步学会产生对后续有用的 carry。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Trajectory-aware training BPTT 基础模型 生成路径：草稿验证、并行去噪与少步迭代 trajectory-aware carry 训练与把每一步单独当样本，优化的依赖有何不同？ 独立训练切断前后carry关系；窗口内BPTT让后续loss影响前一步产生的carry。它需要真实连续展开，不能只把多个独立CE相加就声称已学习跨步信息传递。 示意：第2步loss应能影响第1步留下的carry，而非只更新第2步局部计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3eb472980073a93b">trajectory-aware carry 训练与把每一步单独当样本，优化的依赖有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apumba">On Trajectory-Aware Training for Masked Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立训练切断前后carry关系；窗口内BPTT让后续loss影响前一步产生的carry。它需要真实连续展开，不能只把多个独立CE相加就声称已学习跨步信息传递。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第2步loss应能影响第1步留下的carry，而非只更新第2步局部计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37974">原论文</a> · <a href="../../../../foundation-models/2609.37974-pumba/">实现解读</a> · <a href="#qa-3eb472980073a93b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pumba" data-paper-title="On Trajectory-Aware Training for Masked Diffusion Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="On Trajectory-Aware Training for Masked Diffusion Language Models 基础模型 Apple 2026-09-29 训练时沿模型自己的 progressive-unmasking 轨迹连续展开多个 denoising step，把隐藏 carry 传给下一步，并在固定窗口内通过时间反向传播，使前一步学会产生对后续有用的 carry。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Trajectory-aware training BPTT 基础模型 生成路径：草稿验证、并行去噪与少步迭代 PUMBA 应在每步还是窗口边界 detach carry？ 文档梯度在固定窗口内穿过carry，窗口间截断。每步detach会删除关键跨步梯度，完全不截断又改变内存与训练配置；当前本地reference未训练LLaDA-8B。 示意：窗口长度3时，第3步可反传到本窗前两步，但不继续穿过上一窗口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6b958073b73e1c11">PUMBA 应在每步还是窗口边界 detach carry？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apumba">On Trajectory-Aware Training for Masked Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档梯度在固定窗口内穿过carry，窗口间截断。每步detach会删除关键跨步梯度，完全不截断又改变内存与训练配置；当前本地reference未训练LLaDA-8B。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>窗口长度3时，第3步可反传到本窗前两步，但不继续穿过上一窗口。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37974">原论文</a> · <a href="../../../../foundation-models/2609.37974-pumba/">实现解读</a> · <a href="#qa-6b958073b73e1c11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tadm" data-paper-title="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation 基础模型 The University of Texas at Austin 2026-09-29 将昂贵 anchor network 的潜表示跨多个反向扩散步缓存，只周期性刷新；小型 fusion module 根据当前状态门控修正陈旧 anchor，再交给轻量 denoiser。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Latent cache 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 TADM 为什么让昂贵 anchor network 不必每个扩散步都运行？ 相邻反向扩散步可复用部分潜表示。方法周期性刷新anchor，在间隔步用轻量fusion结合当前状态修正缓存，再交给较轻denoiser，以复用昂贵计算。 示意：连续几步共用一次anchor结果，但每步仍根据当前状态形成不同修正。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-tadm-0fb9bc3b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b887b96c6f1ca604">TADM 为什么让昂贵 anchor network 不必每个扩散步都运行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atadm">Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相邻反向扩散步可复用部分潜表示。方法周期性刷新anchor，在间隔步用轻量fusion结合当前状态修正缓存，再交给较轻denoiser，以复用昂贵计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续几步共用一次anchor结果，但每步仍根据当前状态形成不同修正。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37924">原论文</a> · <a href="../../../../foundation-models/2609.37924-tadm/">实现解读</a> · <a href="#qa-b887b96c6f1ca604">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tadm" data-paper-title="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation 基础模型 The University of Texas at Austin 2026-09-29 将昂贵 anchor network 的潜表示跨多个反向扩散步缓存，只周期性刷新；小型 fusion module 根据当前状态门控修正陈旧 anchor，再交给轻量 denoiser。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Latent cache 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 TADM周期缓存anchor后，为什么还需要依当前扩散状态进行门控修正？ 跨多个反向步复用昂贵潜表示可减少主网络调用，但当前状态不断变化，旧anchor会陈旧。轻量融合模块用当前条件预测修正并门控，再交给较小去噪器，平衡复用与适配。门控不能保证陈旧信息完全恢复，本地修正核未运行完整大模型生成评测。 例如早期缓存只表达粗略句子结构，后续已确定更多词元，融合模块据新状态修正旧表示；一直原样复用可能忽略这些新约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0b7ec87ec23ca88a">TADM周期缓存anchor后，为什么还需要依当前扩散状态进行门控修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atadm">Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>跨多个反向步复用昂贵潜表示可减少主网络调用，但当前状态不断变化，旧anchor会陈旧。轻量融合模块用当前条件预测修正并门控，再交给较小去噪器，平衡复用与适配。门控不能保证陈旧信息完全恢复，本地修正核未运行完整大模型生成评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如早期缓存只表达粗略句子结构，后续已确定更多词元，融合模块据新状态修正旧表示；一直原样复用可能忽略这些新约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37924">原论文</a> · <a href="../../../../foundation-models/2609.37924-tadm/">实现解读</a> · <a href="#qa-0b7ec87ec23ca88a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tadm" data-paper-title="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation 基础模型 The University of Texas at Austin 2026-09-29 将昂贵 anchor network 的潜表示跨多个反向扩散步缓存，只周期性刷新；小型 fusion module 根据当前状态门控修正陈旧 anchor，再交给轻量 denoiser。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Latent cache 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 TADM 的门控陈旧缓存修正，与直接原样复用 h_t′ 有什么差别？ 原样复用忽略当前扩散状态变化；门控修正根据c_t与旧anchor产生增量，允许调整过期信息。它仍可能需要刷新，不能把fusion当作无误差替代所有anchor前向。 示意：去噪状态已明显变化时，旧表示可被修正，而不是一直当作刚算出的新表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5c0c8e549d5c34b5">TADM 的门控陈旧缓存修正，与直接原样复用 h_t′ 有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atadm">Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原样复用忽略当前扩散状态变化；门控修正根据c_t与旧anchor产生增量，允许调整过期信息。它仍可能需要刷新，不能把fusion当作无误差替代所有anchor前向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>去噪状态已明显变化时，旧表示可被修正，而不是一直当作刚算出的新表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37924">原论文</a> · <a href="../../../../foundation-models/2609.37924-tadm/">实现解读</a> · <a href="#qa-5c0c8e549d5c34b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tadm" data-paper-title="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation 基础模型 The University of Texas at Austin 2026-09-29 将昂贵 anchor network 的潜表示跨多个反向扩散步缓存，只周期性刷新；小型 fusion module 根据当前状态门控修正陈旧 anchor，再交给轻量 denoiser。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  扩散语言模型 Latent cache 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 TADM 的 g 与 Δ 两个输出，怎样用边界检查避免写成另一个融合？ 文档是h_t′+g⊙Δ：g=0回到旧anchor，Δ=0也回到旧anchor。若把g乘整个h_t′或删除残差就改变公式；本地仅执行cache correction，没有加载DiffusionGemma-26B。 示意：将gate全置0时，输出不应变成全零表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f04d97a265814e48">TADM 的 g 与 Δ 两个输出，怎样用边界检查避免写成另一个融合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atadm">Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档是h_t′+g⊙Δ：g=0回到旧anchor，Δ=0也回到旧anchor。若把g乘整个h_t′或删除残差就改变公式；本地仅执行cache correction，没有加载DiffusionGemma-26B。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>将gate全置0时，输出不应变成全零表示。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37924">原论文</a> · <a href="../../../../foundation-models/2609.37924-tadm/">实现解读</a> · <a href="#qa-f04d97a265814e48">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dqwen35" data-paper-title="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models 基础模型 University of Texas at Austin 2026-09-17 把 Qwen3.5 的注意力/RNN 混合骨干改成双向状态传播，再以掩码去噪目标训练为 diffusion language model。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。  扩散语言模型 网络架构 基础模型 生成路径：草稿验证、并行去噪与少步迭代 dQwen3.5 为什么把混合骨干改造成双向扩散语言模型？ masked denoising需要利用可见上下文的两侧信息，不再只做从左到右next-token预测。对attention/RNN混合骨干，这涉及双向状态传播及训练目标，而非一个attention开关。 示意：中间词被遮住时，模型可利用左右两边已知文字恢复它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-dqwen35-77ccc4a5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8797f4eb60febff3">dQwen3.5 为什么把混合骨干改造成双向扩散语言模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adqwen35">dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>masked denoising需要利用可见上下文的两侧信息，不再只做从左到右next-token预测。对attention/RNN混合骨干，这涉及双向状态传播及训练目标，而非一个attention开关。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>中间词被遮住时，模型可利用左右两边已知文字恢复它。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20751">原论文</a> · <a href="../../../../foundation-models/2609.20751-dqwen35/">实现解读</a> · <a href="#qa-8797f4eb60febff3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dqwen35" data-paper-title="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models 基础模型 University of Texas at Austin 2026-09-17 把 Qwen3.5 的注意力/RNN 混合骨干改成双向状态传播，再以掩码去噪目标训练为 diffusion language model。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。  扩散语言模型 网络架构 基础模型 生成路径：草稿验证、并行去噪与少步迭代 dQwen3.5把混合骨干改成双向传播，为什么不只是把注意力的因果mask去掉？ 混合骨干还包含递归状态，若只有注意力能看双向，递归分支仍可能保留单向信息约束。双向状态传播配合掩码去噪，才适应同时恢复多个位置的扩散任务。传播核可执行不表示检查点已经完成适配，本地未加载完整模型或复现预训练损失曲线。 例如句首空位需要句末线索，注意力分支看到了后文，而单向递归分支仍读不到；只改一个mask无法让两条路径都拥有相同信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-628204eccd8870fd">dQwen3.5把混合骨干改成双向传播，为什么不只是把注意力的因果mask去掉？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adqwen35">dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>混合骨干还包含递归状态，若只有注意力能看双向，递归分支仍可能保留单向信息约束。双向状态传播配合掩码去噪，才适应同时恢复多个位置的扩散任务。传播核可执行不表示检查点已经完成适配，本地未加载完整模型或复现预训练损失曲线。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如句首空位需要句末线索，注意力分支看到了后文，而单向递归分支仍读不到；只改一个mask无法让两条路径都拥有相同信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20751">原论文</a> · <a href="../../../../foundation-models/2609.20751-dqwen35/">实现解读</a> · <a href="#qa-628204eccd8870fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dqwen35" data-paper-title="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models 基础模型 University of Texas at Austin 2026-09-17 把 Qwen3.5 的注意力/RNN 混合骨干改成双向状态传播，再以掩码去噪目标训练为 diffusion language model。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。  扩散语言模型 网络架构 基础模型 生成路径：草稿验证、并行去噪与少步迭代 双向 masked denoising 与自回归 next-token 训练，输入可见性有什么差异？ 自回归预测受前缀因果约束；双向去噪可根据当前可见的左右上下文预测masked位置。改变目标后还需适配混合状态路径，不能借用AR解码缓存假设直接宣称等价。 示意：预测句子中间空缺时，后面的已知词是可用线索，而AR下一词预测不能读未来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a0ecca512c918406">双向 masked denoising 与自回归 next-token 训练，输入可见性有什么差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adqwen35">dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自回归预测受前缀因果约束；双向去噪可根据当前可见的左右上下文预测masked位置。改变目标后还需适配混合状态路径，不能借用AR解码缓存假设直接宣称等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预测句子中间空缺时，后面的已知词是可用线索，而AR下一词预测不能读未来。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20751">原论文</a> · <a href="../../../../foundation-models/2609.20751-dqwen35/">实现解读</a> · <a href="#qa-a0ecca512c918406">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dqwen35" data-paper-title="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models 基础模型 University of Texas at Austin 2026-09-17 把 Qwen3.5 的注意力/RNN 混合骨干改成双向状态传播，再以掩码去噪目标训练为 diffusion language model。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。  扩散语言模型 网络架构 基础模型 生成路径：草稿验证、并行去噪与少步迭代 测试混合骨干双向化时，为什么要同时检查 attention 与 recurrent 分支？ 只移除attention因果mask，RNN分支仍可能保持单向状态，未完成文档中的双向混合传播。本地CUDA kernel仅证明组件路径运行，未加载9B checkpoint或复现完整去噪训练曲线。 示意：右侧可见信息若只进入一条分支，不能把另一条仍单向的分支当成已双向改造。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b58767fde4bdf527">测试混合骨干双向化时，为什么要同时检查 attention 与 recurrent 分支？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adqwen35">dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只移除attention因果mask，RNN分支仍可能保持单向状态，未完成文档中的双向混合传播。本地CUDA kernel仅证明组件路径运行，未加载9B checkpoint或复现完整去噪训练曲线。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>右侧可见信息若只进入一条分支，不能把另一条仍单向的分支当成已双向改造。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20751">原论文</a> · <a href="../../../../foundation-models/2609.20751-dqwen35/">实现解读</a> · <a href="#qa-b58767fde4bdf527">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:aspire" data-paper-title="ASPIRE: Asynchronous Batch Self-Speculative Decoding" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ASPIRE: Asynchronous Batch Self-Speculative Decoding 基础模型 University of Southern California 2026-09-16 每个请求依据在线接受率与当前 batch 成本独立选择 draft 长度，并周期性用全注意力 refresh layer 校正自推测状态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 ASPIRE 为什么把草稿长度选择放到每个请求上？ 同一batch请求的接受率和剩余情况不同，统一草稿长度容易让简单或困难请求互相拖累。方法用在线接受率与当前batch成本分别决策，并周期性refresh校正自推测状态。 示意：一条请求经常接受长草稿，另一条经常拒绝，两者不必始终写同样多draft。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-aspire-a1351704" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ede71e564dc50d74">ASPIRE 为什么把草稿长度选择放到每个请求上？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaspire">ASPIRE: Asynchronous Batch Self-Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一batch请求的接受率和剩余情况不同，统一草稿长度容易让简单或困难请求互相拖累。方法用在线接受率与当前batch成本分别决策，并周期性refresh校正自推测状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条请求经常接受长草稿，另一条经常拒绝，两者不必始终写同样多draft。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17943">原论文</a> · <a href="../../../../foundation-models/2609.17943-aspire/">实现解读</a> · <a href="#qa-ede71e564dc50d74">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:aspire" data-paper-title="ASPIRE: Asynchronous Batch Self-Speculative Decoding" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ASPIRE: Asynchronous Batch Self-Speculative Decoding 基础模型 University of Southern California 2026-09-16 每个请求依据在线接受率与当前 batch 成本独立选择 draft 长度，并周期性用全注意力 refresh layer 校正自推测状态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 ASPIRE为什么让同一batch内的请求独立选择草稿长度，而不是统一一个长度？ 不同请求的接受率和剩余状态不同，统一长度会让低接受率请求浪费验证或让高接受率请求错失收益。调度还需结合当前批成本，而非只追求最长草稿；周期全注意力刷新用于纠正自投机状态。本地只验证调度和刷新门控，没有改造完整推理引擎。 例如一个请求连续接受较深草稿，另一个常在首词拒绝，可给它们不同长度；但批处理开销也会改变选择，不能只按单请求接受率算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3be38b55eeb6ffa7">ASPIRE为什么让同一batch内的请求独立选择草稿长度，而不是统一一个长度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaspire">ASPIRE: Asynchronous Batch Self-Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同请求的接受率和剩余状态不同，统一长度会让低接受率请求浪费验证或让高接受率请求错失收益。调度还需结合当前批成本，而非只追求最长草稿；周期全注意力刷新用于纠正自投机状态。本地只验证调度和刷新门控，没有改造完整推理引擎。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个请求连续接受较深草稿，另一个常在首词拒绝，可给它们不同长度；但批处理开销也会改变选择，不能只按单请求接受率算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17943">原论文</a> · <a href="../../../../foundation-models/2609.17943-aspire/">实现解读</a> · <a href="#qa-3be38b55eeb6ffa7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:aspire" data-paper-title="ASPIRE: Asynchronous Batch Self-Speculative Decoding" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ASPIRE: Asynchronous Batch Self-Speculative Decoding 基础模型 University of Southern California 2026-09-16 每个请求依据在线接受率与当前 batch 成本独立选择 draft 长度，并周期性用全注意力 refresh layer 校正自推测状态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 按请求独立选择 draft 长度，与完全忽略 batch 的单请求贪心相同吗？ 不同。文档明确同时依据当前batch成本，独立决策仍处于共享执行环境；单看本请求接受率可能忽略批处理资源和同步代价。异步批自推测并非把若干单请求策略直接并排。 示意：某请求多写几步虽提高自身接受数，却可能增加整个batch的验证成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3e520f7e53219a96">按请求独立选择 draft 长度，与完全忽略 batch 的单请求贪心相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaspire">ASPIRE: Asynchronous Batch Self-Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同。文档明确同时依据当前batch成本，独立决策仍处于共享执行环境；单看本请求接受率可能忽略批处理资源和同步代价。异步批自推测并非把若干单请求策略直接并排。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某请求多写几步虽提高自身接受数，却可能增加整个batch的验证成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17943">原论文</a> · <a href="../../../../foundation-models/2609.17943-aspire/">实现解读</a> · <a href="#qa-3e520f7e53219a96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:aspire" data-paper-title="ASPIRE: Asynchronous Batch Self-Speculative Decoding" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ASPIRE: Asynchronous Batch Self-Speculative Decoding 基础模型 University of Southern California 2026-09-16 每个请求依据在线接受率与当前 batch 成本独立选择 draft 长度，并周期性用全注意力 refresh layer 校正自推测状态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 本地 batch-aware scheduler 与 refresh gate，已经等于真实 vLLM serving 改造吗？ 没有。需额外验证实际请求调度、缓存状态、refresh执行和端到端时间。文档只执行对应reference，未改vLLM服务引擎，不能用计划中的草稿长度直接报告部署吞吐。 示意：记录“本请求draft=8”并不证明服务系统已按该长度异步运行并正确交接KV。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fcb5b7f9ae76d071">本地 batch-aware scheduler 与 refresh gate，已经等于真实 vLLM serving 改造吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaspire">ASPIRE: Asynchronous Batch Self-Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。需额外验证实际请求调度、缓存状态、refresh执行和端到端时间。文档只执行对应reference，未改vLLM服务引擎，不能用计划中的草稿长度直接报告部署吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>记录“本请求draft=8”并不证明服务系统已按该长度异步运行并正确交接KV。</p>
<p class="ar-learning-sources">依据：复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17943">原论文</a> · <a href="../../../../foundation-models/2609.17943-aspire/">实现解读</a> · <a href="#qa-fcb5b7f9ae76d071">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:echo" data-paper-title="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding 基础模型 Wuhan University 2026-09-15 用早层高频探索与末层低频权威校验组成双循环；两侧 bonus logits 协同补树，并保留精确拒绝采样校正。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 ECHO 为什么让早层频繁探索、末层较少次数权威校验？ 早层提案较便宜，末层提供目标模型的可靠校验；双循环与bonus logits用于协同补候选树，希望减少等待和重复工作，同时保留最终采样校正。 示意：轻量路径先扩展候选，完整深度集中验证有希望的分支。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-echo-675d4c78" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cf24dec53cc5f9b0">ECHO 为什么让早层频繁探索、末层较少次数权威校验？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aecho">ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早层提案较便宜，末层提供目标模型的可靠校验；双循环与bonus logits用于协同补候选树，希望减少等待和重复工作，同时保留最终采样校正。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>轻量路径先扩展候选，完整深度集中验证有希望的分支。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17241">原论文</a> · <a href="../../../../foundation-models/2609.17241-echo/">实现解读</a> · <a href="#qa-cf24dec53cc5f9b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:echo" data-paper-title="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding 基础模型 Wuhan University 2026-09-15 用早层高频探索与末层低频权威校验组成双循环；两侧 bonus logits 协同补树，并保留精确拒绝采样校正。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 ECHO用早层探索和末层校验，为什么bonus logits不能直接当最终采样分布？ 早层高频提出候选，末层较低频进行权威验证，两侧额外分数用于协同补充候选树，提高有效提议覆盖。探索分布可以不同于目标分布，最终仍需精确拒绝采样校正。省略校正会改变输出分布，本地候选合并与张量路径也不能证明论文吞吐。 例如早层补出一条末层原树未包含的分支，可以拿来验证；不能因它扩展了候选就直接接受，否则把草稿偏好混成了目标答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bdd24109fa6354ee">ECHO用早层探索和末层校验，为什么bonus logits不能直接当最终采样分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aecho">ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早层高频提出候选，末层较低频进行权威验证，两侧额外分数用于协同补充候选树，提高有效提议覆盖。探索分布可以不同于目标分布，最终仍需精确拒绝采样校正。省略校正会改变输出分布，本地候选合并与张量路径也不能证明论文吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如早层补出一条末层原树未包含的分支，可以拿来验证；不能因它扩展了候选就直接接受，否则把草稿偏好混成了目标答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17241">原论文</a> · <a href="../../../../foundation-models/2609.17241-echo/">实现解读</a> · <a href="#qa-bdd24109fa6354ee">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:echo" data-paper-title="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding 基础模型 Wuhan University 2026-09-15 用早层高频探索与末层低频权威校验组成双循环；两侧 bonus logits 协同补树，并保留精确拒绝采样校正。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 ECHO 的候选探索分数与最终目标采样分布，为什么要分开？ bonus logits服务提案与树扩展，不能自动等同完整目标分布；精确拒绝采样校正才维护目标口径。若直接从bonus分布输出，就改变了希望保持的采样行为。 示意：某候选因探索奖励被优先尝试，不意味着最终被接受的概率也应额外增加。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-339dbce0d5c7dcc9">ECHO 的候选探索分数与最终目标采样分布，为什么要分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aecho">ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>bonus logits服务提案与树扩展，不能自动等同完整目标分布；精确拒绝采样校正才维护目标口径。若直接从bonus分布输出，就改变了希望保持的采样行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某候选因探索奖励被优先尝试，不意味着最终被接受的概率也应额外增加。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17241">原论文</a> · <a href="../../../../foundation-models/2609.17241-echo/">实现解读</a> · <a href="#qa-339dbce0d5c7dcc9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:echo" data-paper-title="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding 基础模型 Wuhan University 2026-09-15 用早层高频探索与末层低频权威校验组成双循环；两侧 bonus logits 协同补树，并保留精确拒绝采样校正。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  推测解码 推理效率 基础模型 生成路径：草稿验证、并行去噪与少步迭代 ECHO 的候选合并通过与真实 CUDA 吞吐提升，验收对象有何不同？ 本地reference检查候选合并和lossless校正，A100回执只确认tensor路径。实际加速还需真实早/末层调度、缓存与时间测量，不能把机制三种子直接写成论文服务吞吐。 示意：校正后候选分布正确，不代表探索与验证在GPU上已经按理想流水线重叠。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d65f387fa303137c">ECHO 的候选合并通过与真实 CUDA 吞吐提升，验收对象有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aecho">ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地reference检查候选合并和lossless校正，A100回执只确认tensor路径。实际加速还需真实早/末层调度、缓存与时间测量，不能把机制三种子直接写成论文服务吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>校正后候选分布正确，不代表探索与验证在GPU上已经按理想流水线重叠。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17241">原论文</a> · <a href="../../../../foundation-models/2609.17241-echo/">实现解读</a> · <a href="#qa-d65f387fa303137c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:loopspec" data-paper-title="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers 基础模型 Seoul National University / KAIST 2026-09-15 利用循环深度的中间预测做自推测，并以流水线残差提案隐藏验证等待。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  推测解码 循环 Transformer 基础模型 生成路径：草稿验证、并行去噪与少步迭代 LoopSpec 的自推测为什么适合重复共享块的模型？ 循环深度中间就能给出较浅预测，可用作草稿而不必先训练完全独立drafter。后续更完整循环提供验证，流水线残差提案用于减少验证等待。 示意：同一模型较少循环的结果先提出候选，更多循环的路径再校验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-loopspec-856a7101" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ba81a43442fcdf04">LoopSpec 的自推测为什么适合重复共享块的模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aloopspec">LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University / KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>循环深度中间就能给出较浅预测，可用作草稿而不必先训练完全独立drafter。后续更完整循环提供验证，流水线残差提案用于减少验证等待。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一模型较少循环的结果先提出候选，更多循环的路径再校验。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17184">原论文</a> · <a href="../../../../foundation-models/2609.17184-loopspec/">实现解读</a> · <a href="#qa-ba81a43442fcdf04">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:loopspec" data-paper-title="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers 基础模型 Seoul National University / KAIST 2026-09-15 利用循环深度的中间预测做自推测，并以流水线残差提案隐藏验证等待。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  推测解码 循环 Transformer 基础模型 生成路径：草稿验证、并行去噪与少步迭代 LoopSpec为什么利用循环深度的中间预测，而不必另训练一个完全独立草稿模型？ 循环Transformer不同深度的状态可形成便宜的早期预测，再用更深计算验证；流水线残差提案试图把等待时间与后续工作重叠。中间预测只是提议，不自动拥有深层质量，真实收益取决于接受与调度开销。本地深度调度参考核没有证明GPU端到端吞吐。 例如同一模型浅循环先提议下一段，深循环随后核验；若提议常被拒绝，虽然省了独立草稿模型，也可能无法抵消流水线成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2ca2ea44d8975e44">LoopSpec为什么利用循环深度的中间预测，而不必另训练一个完全独立草稿模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aloopspec">LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University / KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>循环Transformer不同深度的状态可形成便宜的早期预测，再用更深计算验证；流水线残差提案试图把等待时间与后续工作重叠。中间预测只是提议，不自动拥有深层质量，真实收益取决于接受与调度开销。本地深度调度参考核没有证明GPU端到端吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一模型浅循环先提议下一段，深循环随后核验；若提议常被拒绝，虽然省了独立草稿模型，也可能无法抵消流水线成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17184">原论文</a> · <a href="../../../../foundation-models/2609.17184-loopspec/">实现解读</a> · <a href="#qa-2ca2ea44d8975e44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:loopspec" data-paper-title="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers 基础模型 Seoul National University / KAIST 2026-09-15 利用循环深度的中间预测做自推测，并以流水线残差提案隐藏验证等待。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  推测解码 循环 Transformer 基础模型 生成路径：草稿验证、并行去噪与少步迭代 LoopSpec 与独立小草稿模型的 speculative decoding，多复用了什么？ 它复用循环模型的中间深度预测与共享结构；独立drafter有另一套参数和运行路径。是否更快仍依赖提案质量、验证成本与实际调度，不能仅因少维护一个模型就断言加速。 示意：省去独立drafter权重，不代表每个候选都能被深层验证接受。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-98ca8dd6b68a1879">LoopSpec 与独立小草稿模型的 speculative decoding，多复用了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aloopspec">LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University / KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它复用循环模型的中间深度预测与共享结构；独立drafter有另一套参数和运行路径。是否更快仍依赖提案质量、验证成本与实际调度，不能仅因少维护一个模型就断言加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>省去独立drafter权重，不代表每个候选都能被深层验证接受。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17184">原论文</a> · <a href="../../../../foundation-models/2609.17184-loopspec/">实现解读</a> · <a href="#qa-98ca8dd6b68a1879">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:loopspec" data-paper-title="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers 基础模型 Seoul National University / KAIST 2026-09-15 利用循环深度的中间预测做自推测，并以流水线残差提案隐藏验证等待。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  推测解码 循环 Transformer 基础模型 生成路径：草稿验证、并行去噪与少步迭代 只实现 depth scheduler，是否已经实现 LoopSpec 的真实 GPU 流水线？ 没有。调度reference只能核验深度与提案状态转换，还需真实执行重叠、缓存交接及正确验证。文档明确没有论文GPU吞吐声明，不能由计划中的并行时间线推导测量结果。 示意：日志写“提案与验证重叠”，不等于两项GPU工作实际并发且没有同步瓶颈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-980fa512cb80cf33">只实现 depth scheduler，是否已经实现 LoopSpec 的真实 GPU 流水线？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aloopspec">LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University / KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。调度reference只能核验深度与提案状态转换，还需真实执行重叠、缓存交接及正确验证。文档明确没有论文GPU吞吐声明，不能由计划中的并行时间线推导测量结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>日志写“提案与验证重叠”，不等于两项GPU工作实际并发且没有同步瓶颈。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17184">原论文</a> · <a href="../../../../foundation-models/2609.17184-loopspec/">实现解读</a> · <a href="#qa-980fa512cb80cf33">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:register-tokens-dllm" data-paper-title="Register Tokens for Bounded-State Reasoning in Diffusion Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Register Tokens for Bounded-State Reasoning in Diffusion Language Models 基础模型 University of Wisconsin–Madison 2026-09-14 清除上一段文本后仅携带固定数量的连续 register hidden states，让扩散语言模型跨 chunk 推理。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  扩散语言模型 长程推理 基础模型 生成路径：草稿验证、并行去噪与少步迭代 固定数量 register tokens 为什么能作为扩散模型跨 chunk 的记忆接口？ 连续hidden states把前一块信息带到下一块，即使原文本被清除也能保留部分影响。固定数量让状态容量有界，同时也形成信息瓶颈，不能保证保存全部旧证据。 示意：下一段只接收到几个连续寄存向量，而不是上一段完整文字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-register-tokens-dllm-e9299172" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8c20693d27f0d551">固定数量 register tokens 为什么能作为扩散模型跨 chunk 的记忆接口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aregister-tokens-dllm">Register Tokens for Bounded-State Reasoning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续hidden states把前一块信息带到下一块，即使原文本被清除也能保留部分影响。固定数量让状态容量有界，同时也形成信息瓶颈，不能保证保存全部旧证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>下一段只接收到几个连续寄存向量，而不是上一段完整文字。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16372">原论文</a> · <a href="../../../../foundation-models/2609.16372-register-tokens-dllm/">实现解读</a> · <a href="#qa-8c20693d27f0d551">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:register-tokens-dllm" data-paper-title="Register Tokens for Bounded-State Reasoning in Diffusion Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Register Tokens for Bounded-State Reasoning in Diffusion Language Models 基础模型 University of Wisconsin–Madison 2026-09-14 清除上一段文本后仅携带固定数量的连续 register hidden states，让扩散语言模型跨 chunk 推理。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  扩散语言模型 长程推理 基础模型 生成路径：草稿验证、并行去噪与少步迭代 扩散模型清除上一段文本后只带固定register，为什么仍可能跨段推理又受信息瓶颈限制？ 连续register隐藏状态保存上一段提炼的信息，以固定大小传给下一段，避免上下文随段数无限增长。保留的是压缩状态而非完整文字历史，重要细节能否被编码并长期维持需要训练与评测。状态大小有界不等于推理记忆无损，本地未加载完整扩散检查点。 例如上一段确定人物关系后把摘要状态传入下一段，原句已删除；若某个姓名未进入register，后文无法凭固定状态保证精确恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8ccfd44bd0885c4e">扩散模型清除上一段文本后只带固定register，为什么仍可能跨段推理又受信息瓶颈限制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aregister-tokens-dllm">Register Tokens for Bounded-State Reasoning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续register隐藏状态保存上一段提炼的信息，以固定大小传给下一段，避免上下文随段数无限增长。保留的是压缩状态而非完整文字历史，重要细节能否被编码并长期维持需要训练与评测。状态大小有界不等于推理记忆无损，本地未加载完整扩散检查点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如上一段确定人物关系后把摘要状态传入下一段，原句已删除；若某个姓名未进入register，后文无法凭固定状态保证精确恢复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16372">原论文</a> · <a href="../../../../foundation-models/2609.16372-register-tokens-dllm/">实现解读</a> · <a href="#qa-8ccfd44bd0885c4e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:register-tokens-dllm" data-paper-title="Register Tokens for Bounded-State Reasoning in Diffusion Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Register Tokens for Bounded-State Reasoning in Diffusion Language Models 基础模型 University of Wisconsin–Madison 2026-09-14 清除上一段文本后仅携带固定数量的连续 register hidden states，让扩散语言模型跨 chunk 推理。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  扩散语言模型 长程推理 基础模型 生成路径：草稿验证、并行去噪与少步迭代 register carry 与直接保留全部旧文本或 KV，记忆对象有什么不同？ carry保留固定容量连续摘要，完整文本/KV保留更细粒度历史并随长度增长。前者控制状态规模，后者提供更直接的位置访问；不能把固定register当成无损压缩。 示意：两百页内容最终只传八个向量，其容量不会随页数增加而自动扩大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e3c98792dfdfe1ae">register carry 与直接保留全部旧文本或 KV，记忆对象有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aregister-tokens-dllm">Register Tokens for Bounded-State Reasoning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>carry保留固定容量连续摘要，完整文本/KV保留更细粒度历史并随长度增长。前者控制状态规模，后者提供更直接的位置访问；不能把固定register当成无损压缩。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两百页内容最终只传八个向量，其容量不会随页数增加而自动扩大。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16372">原论文</a> · <a href="../../../../foundation-models/2609.16372-register-tokens-dllm/">实现解读</a> · <a href="#qa-e3c98792dfdfe1ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:register-tokens-dllm" data-paper-title="Register Tokens for Bounded-State Reasoning in Diffusion Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Register Tokens for Bounded-State Reasoning in Diffusion Language Models 基础模型 University of Wisconsin–Madison 2026-09-14 清除上一段文本后仅携带固定数量的连续 register hidden states，让扩散语言模型跨 chunk 推理。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  扩散语言模型 长程推理 基础模型 生成路径：草稿验证、并行去噪与少步迭代 验证 bounded register carry 时，怎样防止上一块文本被旁路保留？ 需核对下一块输入确实只携带约定数量的register状态，清除旧文本及未声明缓存，并检查跨块状态更新。当前本地只执行bounded continuous carry，未加载LLaDA/Dream或训练diffu-GRPO。 示意：寄存器数虽固定，但若后台仍把旧文本拼到下一块输入，就不满足有界状态合同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ecf865b886448827">验证 bounded register carry 时，怎样防止上一块文本被旁路保留？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aregister-tokens-dllm">Register Tokens for Bounded-State Reasoning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需核对下一块输入确实只携带约定数量的register状态，清除旧文本及未声明缓存，并检查跨块状态更新。当前本地只执行bounded continuous carry，未加载LLaDA/Dream或训练diffu-GRPO。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>寄存器数虽固定，但若后台仍把旧文本拼到下一块输入，就不满足有界状态合同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16372">原论文</a> · <a href="../../../../foundation-models/2609.16372-register-tokens-dllm/">实现解读</a> · <a href="#qa-ecf865b886448827">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dblast" data-paper-title="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding 基础模型 Huawei Technologies Canada 2026-08-05 主题：推测解码。并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。DBLast 用跨位置共享的低秩 latent mixture 建模依赖，并以期望验证长度为训练目标。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。用 32-token Markov target 比较 unigram 独立 proposal 与 rank-4 条件 proposal，并按精确 speculative acceptance 估计接受长度。  speculative-decoding inference-efficiency stochastic-decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 并行草稿中，每个位置边际上合理，为什么整段仍可能不协调？ 独立生成各位置会忽略它们之间的联合依赖。DBLast针对并行块的这个问题，用共享latent让位置在条件独立之外仍通过共同变量关联；不能只看单位置概率判断整段质量。 示意：颜色与物体分别看都常见，独立拼接却可能形成不协调组合，共享选择可让它们保持一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-dblast-5689bd49" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dafbe6dd11decfb4">并行草稿中，每个位置边际上合理，为什么整段仍可能不协调？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adblast">DBLast: Dependent Block Drafting for Stochastic Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies Canada</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立生成各位置会忽略它们之间的联合依赖。DBLast针对并行块的这个问题，用共享latent让位置在条件独立之外仍通过共同变量关联；不能只看单位置概率判断整段质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>颜色与物体分别看都常见，独立拼接却可能形成不协调组合，共享选择可让它们保持一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05448">原论文</a> · <a href="../../../../reproductions/2608.05448-dblast/">实现解读</a> · <a href="#qa-dafbe6dd11decfb4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dblast" data-paper-title="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding 基础模型 Huawei Technologies Canada 2026-08-05 主题：推测解码。并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。DBLast 用跨位置共享的低秩 latent mixture 建模依赖，并以期望验证长度为训练目标。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。用 32-token Markov target 比较 unigram 独立 proposal 与 rank-4 条件 proposal，并按精确 speculative acceptance 估计接受长度。  speculative-decoding inference-efficiency stochastic-decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 DBLast共享latent为什么能弥补并行草稿各位置独立采样的缺陷？ 各位置在给定隐变量后可以并行，但共享隐变量使边缘联合分布带有跨位置依赖，避免把互相矛盾的高概率词元简单拼接。训练面向期望验证长度，而不只追求单位置命中率。混合结构仍需目标验证器确认，本地机制可执行不等于原文服务速度已复现。 例如后续短语需要共同选择单数或复数，共享隐变量能协调多个位置；若各自独立挑最高概率词，可能拼出不一致的语法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f6c6be038ac0c88f">DBLast共享latent为什么能弥补并行草稿各位置独立采样的缺陷？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adblast">DBLast: Dependent Block Drafting for Stochastic Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies Canada</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各位置在给定隐变量后可以并行，但共享隐变量使边缘联合分布带有跨位置依赖，避免把互相矛盾的高概率词元简单拼接。训练面向期望验证长度，而不只追求单位置命中率。混合结构仍需目标验证器确认，本地机制可执行不等于原文服务速度已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如后续短语需要共同选择单数或复数，共享隐变量能协调多个位置；若各自独立挑最高概率词，可能拼出不一致的语法。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05448">原论文</a> · <a href="../../../../reproductions/2608.05448-dblast/">实现解读</a> · <a href="#qa-f6c6be038ac0c88f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dblast" data-paper-title="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding 基础模型 Huawei Technologies Canada 2026-08-05 主题：推测解码。并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。DBLast 用跨位置共享的低秩 latent mixture 建模依赖，并以期望验证长度为训练目标。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。用 32-token Markov target 比较 unigram 独立 proposal 与 rank-4 条件 proposal，并按精确 speculative acceptance 估计接受长度。  speculative-decoding inference-efficiency stochastic-decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 共享 latent mixture 与完全独立 unigram proposal，联合概率有什么不同？ 独立proposal直接把各位置边缘概率相乘；DBLast先在同一个z下取乘积再对z积分，可表达位置相关性。两者单位置频率接近，也不意味着块级联合分布相同。 示意：每个位置都一半选A一半选B，仍可分别形成“总是AA/BB”或任意混合两种联合模式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2df450592211aa64">共享 latent mixture 与完全独立 unigram proposal，联合概率有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adblast">DBLast: Dependent Block Drafting for Stochastic Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies Canada</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立proposal直接把各位置边缘概率相乘；DBLast先在同一个z下取乘积再对z积分，可表达位置相关性。两者单位置频率接近，也不意味着块级联合分布相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>每个位置都一半选A一半选B，仍可分别形成“总是AA/BB”或任意混合两种联合模式。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05448">原论文</a> · <a href="../../../../reproductions/2608.05448-dblast/">实现解读</a> · <a href="#qa-2df450592211aa64">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dblast" data-paper-title="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding 基础模型 Huawei Technologies Canada 2026-08-05 主题：推测解码。并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。DBLast 用跨位置共享的低秩 latent mixture 建模依赖，并以期望验证长度为训练目标。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。用 32-token Markov target 比较 unigram 独立 proposal 与 rank-4 条件 proposal，并按精确 speculative acceptance 估计接受长度。  speculative-decoding inference-efficiency stochastic-decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 DBLast 的验收为什么要看精确 speculative acceptance，而不只看逐位置命中率？ 部署收益依赖可连续接受的长度与联合提案质量；逐位置单独正确不保证整块连续通过。文档本地使用Markov target和rank-4 proposal做机制对照，不是实际大模型服务吞吐。 示意：第一和第三位常猜对，但第二位总错，连续接受长度仍可能很短。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-41a53700b992ffab">DBLast 的验收为什么要看精确 speculative acceptance，而不只看逐位置命中率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adblast">DBLast: Dependent Block Drafting for Stochastic Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies Canada</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>部署收益依赖可连续接受的长度与联合提案质量；逐位置单独正确不保证整块连续通过。文档本地使用Markov target和rank-4 proposal做机制对照，不是实际大模型服务吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一和第三位常猜对，但第二位总错，连续接受长度仍可能很短。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05448">原论文</a> · <a href="../../../../reproductions/2608.05448-dblast/">实现解读</a> · <a href="#qa-41a53700b992ffab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:windowed-mtp" data-paper-title="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context 基础模型 NVIDIA 2026-07-23 内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近个 token，同时 target 继续读取完整上下文并验证所有候选。因此窗口只影响接受率和速度，不改变 target 决定的输出分布。 Fidelity: 核心机制复现。真实训练 MTP draft、切换 KV key 集并执行 target verification；缩小模型、context 和 serving runtime。本地实现训练了共享 target token embedding 的轻量 MTP head，并实际执行 sink+window attention 和逐 token target verification；没有复刻 SGLang paged-KV/Triton ring buffer、连续 batching、B200/H100 或百万 token 测试。  llm-serving speculative-decoding kv-cache long-context 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Windowed-MTP 为什么只缩小 draft 的历史读取范围？ 长上下文下草稿每步读完整KV也可能成为瓶颈。方法为draft保留sink和近期窗口，而target仍看完整历史并验证，主要改变提案成本与接受率，保留target作为最终依据。 示意：草稿只读开头几项和最近64项，校验器仍能读取整段16K历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-windowed-mtp-ad617a2b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f4622ee554153341">Windowed-MTP 为什么只缩小 draft 的历史读取范围？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awindowed-mtp">Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长上下文下草稿每步读完整KV也可能成为瓶颈。方法为draft保留sink和近期窗口，而target仍看完整历史并验证，主要改变提案成本与接受率，保留target作为最终依据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>草稿只读开头几项和最近64项，校验器仍能读取整段16K历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21535">原论文</a> · <a href="../../../../reproductions/2607.21535-windowed-mtp/">实现解读</a> · <a href="#qa-f4622ee554153341">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:windowed-mtp" data-paper-title="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context 基础模型 NVIDIA 2026-07-23 内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近个 token，同时 target 继续读取完整上下文并验证所有候选。因此窗口只影响接受率和速度，不改变 target 决定的输出分布。 Fidelity: 核心机制复现。真实训练 MTP draft、切换 KV key 集并执行 target verification；缩小模型、context 和 serving runtime。本地实现训练了共享 target token embedding 的轻量 MTP head，并实际执行 sink+window attention 和逐 token target verification；没有复刻 SGLang paged-KV/Triton ring buffer、连续 batching、B200/H100 或百万 token 测试。  llm-serving speculative-decoding kv-cache long-context 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Windowed-MTP只缩小draft窗口，为什么能省读取又不直接改变target输出分布？ 草稿只读起始保留项与近期窗口，降低其上下文读取开销；目标验证器仍读完整历史并校正所有提议。窗口改变提议质量、接受率及速度，不应改变精确验证定义的目标分布。若连验证器也截窗则条件改变，本地延迟也不能外推到原文生产硬件。 例如旧历史线索被草稿忽略导致猜错，完整目标仍可拒绝并纠正；为了再省一点内存把目标历史也删掉，就失去原分布保证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-869f887ecd35e200">Windowed-MTP只缩小draft窗口，为什么能省读取又不直接改变target输出分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awindowed-mtp">Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>草稿只读起始保留项与近期窗口，降低其上下文读取开销；目标验证器仍读完整历史并校正所有提议。窗口改变提议质量、接受率及速度，不应改变精确验证定义的目标分布。若连验证器也截窗则条件改变，本地延迟也不能外推到原文生产硬件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧历史线索被草稿忽略导致猜错，完整目标仍可拒绝并纠正；为了再省一点内存把目标历史也删掉，就失去原分布保证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21535">原论文</a> · <a href="../../../../reproductions/2607.21535-windowed-mtp/">实现解读</a> · <a href="#qa-869f887ecd35e200">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:windowed-mtp" data-paper-title="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context 基础模型 NVIDIA 2026-07-23 内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近个 token，同时 target 继续读取完整上下文并验证所有候选。因此窗口只影响接受率和速度，不改变 target 决定的输出分布。 Fidelity: 核心机制复现。真实训练 MTP draft、切换 KV key 集并执行 target verification；缩小模型、context 和 serving runtime。本地实现训练了共享 target token embedding 的轻量 MTP head，并实际执行 sink+window attention 和逐 token target verification；没有复刻 SGLang paged-KV/Triton ring buffer、连续 batching、B200/H100 或百万 token 测试。  llm-serving speculative-decoding kv-cache long-context 基础模型 生成路径：草稿验证、并行去噪与少步迭代 draft key 数大幅减少，为什么 TPOT 不会自动按同一比例下降？ 每步仍有target验证与draft前向，最终每token耗时还要除以接受长度AL。窗口可能降低接受率，因此读取节省、单次draft时间和端到端TPOT必须分开比较。 示意：一次验证便宜了，但每次只接受更少token，部分节省会被抵消。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e21f03e9bf00b0a4">draft key 数大幅减少，为什么 TPOT 不会自动按同一比例下降？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awindowed-mtp">Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每步仍有target验证与draft前向，最终每token耗时还要除以接受长度AL。窗口可能降低接受率，因此读取节省、单次draft时间和端到端TPOT必须分开比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次验证便宜了，但每次只接受更少token，部分节省会被抵消。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21535">原论文</a> · <a href="../../../../reproductions/2607.21535-windowed-mtp/">实现解读</a> · <a href="#qa-e21f03e9bf00b0a4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:windowed-mtp" data-paper-title="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context 基础模型 NVIDIA 2026-07-23 内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近个 token，同时 target 继续读取完整上下文并验证所有候选。因此窗口只影响接受率和速度，不改变 target 决定的输出分布。 Fidelity: 核心机制复现。真实训练 MTP draft、切换 KV key 集并执行 target verification；缩小模型、context 和 serving runtime。本地实现训练了共享 target token embedding 的轻量 MTP head，并实际执行 sink+window attention 和逐 token target verification；没有复刻 SGLang paged-KV/Triton ring buffer、连续 batching、B200/H100 或百万 token 测试。  llm-serving speculative-decoding kv-cache long-context 基础模型 生成路径：草稿验证、并行去噪与少步迭代 短序列中 sink 与 recent 重叠时，Windowed-MTP 应复制这些 KV 吗？ key集合是两区间的并集，重叠位置不应重复计入attention；还需保证只改draft索引，target仍读完整cache。若同时裁target，就失去原文的完整上下文验证条件。 示意：第5个位置同时属于sink和recent，也只应在draft读取集合中出现一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-02f172d22260d687">短序列中 sink 与 recent 重叠时，Windowed-MTP 应复制这些 KV 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awindowed-mtp">Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>key集合是两区间的并集，重叠位置不应重复计入attention；还需保证只改draft索引，target仍读完整cache。若同时裁target，就失去原文的完整上下文验证条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第5个位置同时属于sink和recent，也只应在draft读取集合中出现一次。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21535">原论文</a> · <a href="../../../../reproductions/2607.21535-windowed-mtp/">实现解读</a> · <a href="#qa-02f172d22260d687">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:r4t" data-paper-title="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion 基础模型 University of Illinois Urbana-Champaign / Google Research 2026-03-06 先以集合级复合奖励产生对齐目标，再把目标编译到单次扩散式 fan-out 检索器。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  生成式检索 RL 编译 基础模型 生成路径：草稿验证、并行去噪与少步迭代 R4T 为什么先得到集合级对齐目标，再训练快速检索器？ 多项结果的整体属性不一定能由单项得分保证。方法先以集合级复合奖励得到对齐目标，再将它编译进扩散式fan-out检索器，尝试用较少在线步骤生成多项结果。 示意：一组结果既要相关又要覆盖不同内容，不能只让每项各自重复最高分内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-r4t-4721c6f0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b8913b09736b8f3e">R4T 为什么先得到集合级对齐目标，再训练快速检索器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ar4t">Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多项结果的整体属性不一定能由单项得分保证。方法先以集合级复合奖励得到对齐目标，再将它编译进扩散式fan-out检索器，尝试用较少在线步骤生成多项结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组结果既要相关又要覆盖不同内容，不能只让每项各自重复最高分内容。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.06397">原论文</a> · <a href="../../../../foundation-models/2603.06397-r4t/">实现解读</a> · <a href="#qa-b8913b09736b8f3e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:r4t" data-paper-title="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion 基础模型 University of Illinois Urbana-Champaign / Google Research 2026-03-06 先以集合级复合奖励产生对齐目标，再把目标编译到单次扩散式 fan-out 检索器。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  生成式检索 RL 编译 基础模型 生成路径：草稿验证、并行去噪与少步迭代 R4T为什么先对检索集合整体对齐，再把结果编译进扩散式fan-out检索器？ 多路检索的价值不只由每条结果单独相关决定，还取决于集合覆盖与多样性。集合级复合奖励先定义这些取舍，再通过训练让单次扩散检索接近对齐目标，减少在线优化负担。奖励设计可能偏移真实需求，本地只有集合目标核，没有训练完整扩散检索器。 例如三条都高度相关却重复同一证据，可能不如覆盖不同要点的结果组；不能只把单条相关分数分别提高，就称为集合多样性优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-106925b5c8b75df1">R4T为什么先对检索集合整体对齐，再把结果编译进扩散式fan-out检索器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ar4t">Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多路检索的价值不只由每条结果单独相关决定，还取决于集合覆盖与多样性。集合级复合奖励先定义这些取舍，再通过训练让单次扩散检索接近对齐目标，减少在线优化负担。奖励设计可能偏移真实需求，本地只有集合目标核，没有训练完整扩散检索器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三条都高度相关却重复同一证据，可能不如覆盖不同要点的结果组；不能只把单条相关分数分别提高，就称为集合多样性优化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.06397">原论文</a> · <a href="../../../../foundation-models/2603.06397-r4t/">实现解读</a> · <a href="#qa-106925b5c8b75df1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:r4t" data-paper-title="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion 基础模型 University of Illinois Urbana-Champaign / Google Research 2026-03-06 先以集合级复合奖励产生对齐目标，再把目标编译到单次扩散式 fan-out 检索器。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  生成式检索 RL 编译 基础模型 生成路径：草稿验证、并行去噪与少步迭代 集合级 alignment/diversity 目标，与逐项独立排序的目标有什么差别？ 集合目标考虑结果之间的关系与整体属性；逐项分数相加可能忽略重复和覆盖交互。编译后的检索器也需要单独训练与验证，目标函数可执行不等于已得到同样的在线检索能力。 示意：三条内容各自都很相关，但几乎重复时，集合多样性仍可能很差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b272b8d4569a6c1a">集合级 alignment/diversity 目标，与逐项独立排序的目标有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ar4t">Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>集合目标考虑结果之间的关系与整体属性；逐项分数相加可能忽略重复和覆盖交互。编译后的检索器也需要单独训练与验证，目标函数可执行不等于已得到同样的在线检索能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三条内容各自都很相关，但几乎重复时，集合多样性仍可能很差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.06397">原论文</a> · <a href="../../../../foundation-models/2603.06397-r4t/">实现解读</a> · <a href="#qa-b272b8d4569a6c1a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:r4t" data-paper-title="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion 基础模型 University of Illinois Urbana-Champaign / Google Research 2026-03-06 先以集合级复合奖励产生对齐目标，再把目标编译到单次扩散式 fan-out 检索器。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  生成式检索 RL 编译 基础模型 生成路径：草稿验证、并行去噪与少步迭代 本地 R4T 组件已经包含 53.9M 参数扩散检索器训练吗？ 没有。文档只执行alignment/diversity集合目标，完整扩散检索器未训练。复用时需明确接口提供的是集合评分还是生成候选，不能把一个reward函数当作已完成的fan-out模型。 示意：能够给已有候选集合打分，不代表模块自己能从查询生成检索结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fc66c1b00e56a5d1">本地 R4T 组件已经包含 53.9M 参数扩散检索器训练吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ar4t">Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。文档只执行alignment/diversity集合目标，完整扩散检索器未训练。复用时需明确接口提供的是集合评分还是生成候选，不能把一个reward函数当作已完成的fan-out模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>能够给已有候选集合打分，不代表模块自己能从查询生成检索结果。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.06397">原论文</a> · <a href="../../../../foundation-models/2603.06397-r4t/">实现解读</a> · <a href="#qa-fc66c1b00e56a5d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:medusa" data-paper-title="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads 基础模型 Together AI / Princeton University / University of Illinois Urbana-Champaign 2024-01-19 在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 token 转移模型上执行多 future head、候选树和 backbone 验证；未复刻 GPU tree-attention kernel。本地相对变化不得与原文指标混写。本地对照口径：基线为 single-head greedy，实验组为 three future heads + tree verification，只改变论文核心机制；backbone_calls 160.0000 → 80.0000，相对基线 -50.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Medusa 为什么给同一个 hidden state 增加多个 future-token head？ 多个head分别预测不同未来偏移，能一次产生较多候选，再通过候选树验证减少串行生成调用。它增加的是未来候选提案，不是取消backbone对最终内容的验证。 示意：从h_t同时提出t+1、t+2等位置的备选，而非每个位置都先独立运行完整backbone。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-medusa-8eb57905" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-700adaef304fe397">Medusa 为什么给同一个 hidden state 增加多个 future-token head？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amedusa">Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / Princeton University / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个head分别预测不同未来偏移，能一次产生较多候选，再通过候选树验证减少串行生成调用。它增加的是未来候选提案，不是取消backbone对最终内容的验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>从h_t同时提出t+1、t+2等位置的备选，而非每个位置都先独立运行完整backbone。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10774">原论文</a> · <a href="../../../../reproductions/2401.10774-medusa/">实现解读</a> · <a href="#qa-700adaef304fe397">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:medusa" data-paper-title="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads 基础模型 Together AI / Princeton University / University of Illinois Urbana-Champaign 2024-01-19 在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 token 转移模型上执行多 future head、候选树和 backbone 验证；未复刻 GPU tree-attention kernel。本地相对变化不得与原文指标混写。本地对照口径：基线为 single-head greedy，实验组为 three future heads + tree verification，只改变论文核心机制；backbone_calls 160.0000 → 80.0000，相对基线 -50.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Medusa的多个future-token head为什么需要候选树验证，而不能各自取最高概率后直接拼接？ 各头从当前状态预测不同未来位置，预测之间未必构成一致的自回归条件链。候选树组织多种组合，主干再验证可接受分支，才可能减少串行步骤。多头训练损失本身不证明任意拼接正确，也不自动给出采样分布保证；本地小模型未复刻GPU树注意力内核。 例如第二个头预测名词、第三个头预测动词，各自首选未必能连成句子；树验证检查组合，而不是把独立预测当作已知历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-91bfb6f20f55ba61">Medusa的多个future-token head为什么需要候选树验证，而不能各自取最高概率后直接拼接？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amedusa">Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / Princeton University / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各头从当前状态预测不同未来位置，预测之间未必构成一致的自回归条件链。候选树组织多种组合，主干再验证可接受分支，才可能减少串行步骤。多头训练损失本身不证明任意拼接正确，也不自动给出采样分布保证；本地小模型未复刻GPU树注意力内核。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第二个头预测名词、第三个头预测动词，各自首选未必能连成句子；树验证检查组合，而不是把独立预测当作已知历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10774">原论文</a> · <a href="../../../../reproductions/2401.10774-medusa/">实现解读</a> · <a href="#qa-91bfb6f20f55ba61">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:medusa" data-paper-title="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads 基础模型 Together AI / Princeton University / University of Illinois Urbana-Champaign 2024-01-19 在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 token 转移模型上执行多 future head、候选树和 backbone 验证；未复刻 GPU tree-attention kernel。本地相对变化不得与原文指标混写。本地对照口径：基线为 single-head greedy，实验组为 three future heads + tree verification，只改变论文核心机制；backbone_calls 160.0000 → 80.0000，相对基线 -50.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 Medusa 的 backbone call 次数减少，为什么不等于同百分比时延减少？ 未来head、候选树构建和tree attention验证也有成本，实际时延还受batch、kernel与接受率影响。文档转移模型里的调用数变化是机制口径，不能直接替代真实GPU速度。 示意：backbone调用减半，但单次验证工作变多，端到端时间未必恰好减半。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ecbaa441479f51df">Medusa 的 backbone call 次数减少，为什么不等于同百分比时延减少？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amedusa">Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / Princeton University / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未来head、候选树构建和tree attention验证也有成本，实际时延还受batch、kernel与接受率影响。文档转移模型里的调用数变化是机制口径，不能直接替代真实GPU速度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>backbone调用减半，但单次验证工作变多，端到端时间未必恰好减半。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10774">原论文</a> · <a href="../../../../reproductions/2401.10774-medusa/">实现解读</a> · <a href="#qa-ecbaa441479f51df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:medusa" data-paper-title="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads 基础模型 Together AI / Princeton University / University of Illinois Urbana-Champaign 2024-01-19 在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 token 转移模型上执行多 future head、候选树和 backbone 验证；未复刻 GPU tree-attention kernel。本地相对变化不得与原文指标混写。本地对照口径：基线为 single-head greedy，实验组为 three future heads + tree verification，只改变论文核心机制；backbone_calls 160.0000 → 80.0000，相对基线 -50.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 训练 Medusa 第 k 个 future head 时，监督 token 应怎样位移？ 文档p_k(x_{t+k}|h_t)对应从当前位置hidden预测未来第k个目标，需对齐序列切片与有效边界。错用同一个next-token标签给所有head，会把多偏移训练退化成重复预测同一位置。 示意：第2个head在h_10上对齐x_12，而不是仍对齐x_11。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-321b91366afe4f45">训练 Medusa 第 k 个 future head 时，监督 token 应怎样位移？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amedusa">Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / Princeton University / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档p_k(x_{t+k}|h_t)对应从当前位置hidden预测未来第k个目标，需对齐序列切片与有效边界。错用同一个next-token标签给所有head，会把多偏移训练退化成重复预测同一位置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第2个head在h_10上对齐x_12，而不是仍对齐x_11。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10774">原论文</a> · <a href="../../../../reproductions/2401.10774-medusa/">实现解读</a> · <a href="#qa-321b91366afe4f45">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:speculative-decoding" data-paper-title="Fast Inference from Transformers via Speculative Decoding" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Fast Inference from Transformers via Speculative Decoding 基础模型 Google Research 2022-11-30 小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 拟合 target/draft token 模型，真实执行提议、验证和拒绝回退；target 是小型 Markov LM，不等同于 T5-XXL kernel 延迟。本地相对变化不得与原文指标混写。本地对照口径：基线为 target-only greedy decoding，实验组为 four-token draft and exact target verification，只改变论文核心机制；target_calls 160.0000 → 40.0000，相对基线 -75.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 推测解码为什么能用小 draft 帮大 target 减少串行调用？ 廉价draft先提出一段候选，target集中验证这些位置，接受连续正确部分后继续。节省来自提案和并行验证的组织，最终分布仍需精确接受/拒绝校正，不能把草稿直接当答案。 示意：一次target验证可确认多个候选，而不是每个输出token都单独调用一次target。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<span id="paper-foundation-models-speculative-decoding-bd568875" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-18b195341bdbc8b6">推测解码为什么能用小 draft 帮大 target 减少串行调用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aspeculative-decoding">Fast Inference from Transformers via Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>廉价draft先提出一段候选，target集中验证这些位置，接受连续正确部分后继续。节省来自提案和并行验证的组织，最终分布仍需精确接受/拒绝校正，不能把草稿直接当答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次target验证可确认多个候选，而不是每个输出token都单独调用一次target。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.17192">原论文</a> · <a href="../../../../reproductions/2211.17192-speculative-decoding/">实现解读</a> · <a href="#qa-18b195341bdbc8b6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:speculative-decoding" data-paper-title="Fast Inference from Transformers via Speculative Decoding" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Fast Inference from Transformers via Speculative Decoding 基础模型 Google Research 2022-11-30 小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 拟合 target/draft token 模型，真实执行提议、验证和拒绝回退；target 是小型 Markov LM，不等同于 T5-XXL kernel 延迟。本地相对变化不得与原文指标混写。本地对照口径：基线为 target-only greedy decoding，实验组为 four-token draft and exact target verification，只改变论文核心机制；target_calls 160.0000 → 40.0000，相对基线 -75.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 推测解码拒绝草稿时，为什么要从正残差分布采样，而不能直接重采一次目标分布？ 草稿按目标与提议概率比接受，接受部分已经贡献了部分目标概率质量。拒绝后从目标减去提议的正残差归一化采样，才能补足剩余质量；直接重采目标会重复计入已接受部分，改变最终分布。本地小型词转移模型验证流程，不等于大模型内核延迟。 例如草稿过度偏好某个词，拒绝事件应补偿它欠覆盖的其他词；若拒绝后仍按原目标重采，就没有正确扣除先前接受的质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bd026bc4bd6ddae3">推测解码拒绝草稿时，为什么要从正残差分布采样，而不能直接重采一次目标分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aspeculative-decoding">Fast Inference from Transformers via Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>草稿按目标与提议概率比接受，接受部分已经贡献了部分目标概率质量。拒绝后从目标减去提议的正残差归一化采样，才能补足剩余质量；直接重采目标会重复计入已接受部分，改变最终分布。本地小型词转移模型验证流程，不等于大模型内核延迟。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如草稿过度偏好某个词，拒绝事件应补偿它欠覆盖的其他词；若拒绝后仍按原目标重采，就没有正确扣除先前接受的质量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.17192">原论文</a> · <a href="../../../../reproductions/2211.17192-speculative-decoding/">实现解读</a> · <a href="#qa-bd026bc4bd6ddae3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:speculative-decoding" data-paper-title="Fast Inference from Transformers via Speculative Decoding" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Fast Inference from Transformers via Speculative Decoding 基础模型 Google Research 2022-11-30 小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 拟合 target/draft token 模型，真实执行提议、验证和拒绝回退；target 是小型 Markov LM，不等同于 T5-XXL kernel 延迟。本地相对变化不得与原文指标混写。本地对照口径：基线为 target-only greedy decoding，实验组为 four-token draft and exact target verification，只改变论文核心机制；target_calls 160.0000 → 40.0000，相对基线 -75.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 精确随机推测解码与“草稿和 target 贪心一致就接收”，保证范围相同吗？ 贪心一致只涉及确定性最高分路径；随机采样要保持完整target分布，需要按p/q接受并在拒绝时校正残差。不能用一条贪心序列相同证明所有温度下采样分布一致。 示意：两个模型最高概率词相同，第二、第三候选的概率仍可能相差很大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d5c4d20915b086ea">精确随机推测解码与“草稿和 target 贪心一致就接收”，保证范围相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aspeculative-decoding">Fast Inference from Transformers via Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>贪心一致只涉及确定性最高分路径；随机采样要保持完整target分布，需要按p/q接受并在拒绝时校正残差。不能用一条贪心序列相同证明所有温度下采样分布一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个模型最高概率词相同，第二、第三候选的概率仍可能相差很大。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.17192">原论文</a> · <a href="../../../../reproductions/2211.17192-speculative-decoding/">实现解读</a> · <a href="#qa-d5c4d20915b086ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:speculative-decoding" data-paper-title="Fast Inference from Transformers via Speculative Decoding" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/generation-paths" data-search="Fast Inference from Transformers via Speculative Decoding 基础模型 Google Research 2022-11-30 小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 WikiText-2 拟合 target/draft token 模型，真实执行提议、验证和拒绝回退；target 是小型 Markov LM，不等同于 T5-XXL kernel 延迟。本地相对变化不得与原文指标混写。本地对照口径：基线为 target-only greedy decoding，实验组为 four-token draft and exact target verification，只改变论文核心机制；target_calls 160.0000 → 40.0000，相对基线 -75.00%。  inference-serving decoding 基础模型 生成路径：草稿验证、并行去噪与少步迭代 一次拒绝后，为什么不能继续无条件提交同块后面的 draft token？ 后续草稿建立在被拒绝的前缀上，目标校正后条件已变化，应按验证协议丢弃未接受后缀并从正确前缀继续。文档本地Markov LM调用数也不等于T5-XXL真实kernel时延。 示意：第2词被改成另一个词后，第3到5词不能仍假设第2词保持原草稿值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 生成路径：草稿验证、并行去噪与少步迭代</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-54352a57f3453951">一次拒绝后，为什么不能继续无条件提交同块后面的 draft token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aspeculative-decoding">Fast Inference from Transformers via Speculative Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后续草稿建立在被拒绝的前缀上，目标校正后条件已变化，应按验证协议丢弃未接受后缀并从正确前缀继续。文档本地Markov LM调用数也不等于T5-XXL真实kernel时延。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第2词被改成另一个词后，第3到5词不能仍假设第2词保持原草稿值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.17192">原论文</a> · <a href="../../../../reproductions/2211.17192-speculative-decoding/">实现解读</a> · <a href="#qa-54352a57f3453951">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

如何减少逐 token 串行生成的等待，同时说清输出分布是否改变？

## 记住这一点

推测解码先由便宜草稿提出多个 token，再让目标模型批量验证；正确的接受概率与拒绝残差采样可保持目标分布。扩散语言模型则把生成改成多位置去噪，例如 dQwen3.5 需把含递归层的因果骨干改为双向传播。少步生成与共享网络迭代又重新安排精炼轨迹；它们改变的不是同一个层面。

## 一个例子

草稿一次提四个 token，如果目标只接受前两个，后面需要校正和继续生成；加速取决于接受率和验证成本。扩散模型可以一轮更新多个位置，但可能要多轮反复去噪。应比较整段输出质量和总时延，不能只比较一次前向写出多少位置。

## 什么时候要小心

精确推测采样的分布保证依赖完整接受与校正算法，不自动适用于任何多头草稿。扩散或蒸馏后的新模型也不因此与原自回归目标等价。本地 Markov 草稿、参考 kernel 或调用次数不能冒充大型模型的真实加速。

## 先读这几篇

先读 Fast Inference 的提出、验证与校正采样，明确保证条件；再读 dQwen3.5 的双向混合骨干与并行解码，区分“重排执行”与“训练新生成机制”。随后看自草稿、缓存和少步精炼。

1. [Fast Inference from Transformers via Speculative Decoding](../../../reproductions/2211.17192-speculative-decoding/README.md) · [原论文](https://arxiv.org/abs/2211.17192)
2. [dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models](../../../foundation-models/2609.20751-dqwen35/README.md) · [原论文](https://arxiv.org/abs/2609.20751)

## 自测一下

“推测解码不改变分布”能否直接用来描述把 AR 骨干改成扩散模型？

??? note "展开参考答案"

    不能。前者在既定目标分布下用接受/拒绝校正重排执行；后者改变模型传播方式、训练目标与解码过程。它需要独立质量评估，不能继承前者的等价采样保证。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
